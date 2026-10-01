# Render the body + pieces (each piece rebound to the BODY's armature) at clip times, from given cameras.
#   blender -b -noaudio --python e11_pose_render.py -- <body.glb> <tex.png|-> <outprefix> --pieces a.glb,b.glb
#       --shots clip@t:cam,...   cam = game (pitch 52.95, yaw 47, ortho 100.6 px/m) | side | front | h<deg>[p<pitch>]
#       [--res 960x540] [--ppm 100.6] [--video clip:fps:out.mp4] [--lit]
import bpy, sys, math, os, json, subprocess
import numpy as np
from mathutils import Vector, Matrix
a = sys.argv[sys.argv.index('--') + 1:]
BODY, TEX, OUTP = a[:3]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
PIECES = [p for p in opt('--pieces', '').split(',') if p]
RW, RH = (int(x) for x in opt('--res', '960x540').split('x')); PPM = float(opt('--ppm', '100.6'))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene; FPS = sc.render.fps / sc.render.fps_base
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]: bpy.data.objects.remove(o, do_unlink=True)
body = [o for o in sc.objects if o.type == 'MESH']
acts = {x.name: x for x in bpy.data.actions}
if TEX != '-':
    img = bpy.data.images.load(os.path.abspath(TEX))
    for o in body:
        for s_ in o.material_slots:
            for n in s_.material.node_tree.nodes:
                if n.type == 'TEX_IMAGE': n.image = img
for p in PIECES:
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=p)
    new = [o for o in sc.objects if o not in before]
    meshes = [o for o in new if o.type == 'MESH' and o.vertex_groups]
    junk = [o for o in new if o not in meshes]
    for o in meshes:
        mw = o.matrix_world.copy()
        for md in o.modifiers:
            if md.type == 'ARMATURE': md.object = arm
        o.parent = arm; o.matrix_parent_inverse = arm.matrix_world.inverted(); o.matrix_world = mw
    for o in junk: bpy.data.objects.remove(o, do_unlink=True)
for x in list(bpy.data.actions):
    if x.name not in acts: bpy.data.actions.remove(x)
LIT = '--lit' in a
if not LIT:
    for m in bpy.data.materials:
        if not m.node_tree: continue
        nt = m.node_tree; out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'), None); tex = next((n for n in nt.nodes if n.type == 'TEX_IMAGE'), None)
        if out is None or tex is None: continue
        em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(tex.outputs['Color'], em.inputs['Color']); nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
else:
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun)
    sun.data.energy = 3.0; sun.rotation_euler = (math.radians(50), 0, math.radians(-40))
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 1.2
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.film_transparent = False; sc.view_settings.view_transform = 'Standard'
if sc.world is None: sc.world = bpy.data.worlds.new('w')
sc.world.color = (0.78, 0.76, 0.70)
if sc.world.use_nodes: pass
sc.render.resolution_x, sc.render.resolution_y = RW, RH
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(RW, RH) / PPM
# ground disc so the figure has a floor
bpy.ops.mesh.primitive_plane_add(size=6); fl = bpy.context.active_object
fm = bpy.data.materials.new('floor'); fm.use_nodes = True; fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.62, 0.58, 0.50, 1); fl.data.materials.append(fm)
def place(spec, aim):
    if spec == 'game': yaw, pit = 47.0, 52.95
    elif spec == 'side': yaw, pit = 90.0, 5.0
    elif spec == 'front': yaw, pit = 0.0, 5.0
    else:
        yaw = float(spec[1:].split('p')[0]); pit = float(spec.split('p')[1]) if 'p' in spec else 10.0
    y, p = math.radians(yaw), math.radians(pit)
    dvec = Vector((math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), math.sin(p)))
    cam.location = aim + dvec * 30; cam.rotation_euler = (-dvec).to_track_quat('-Z', 'Y').to_euler()
def setpose(clip, t):
    ac = acts[clip]; arm.animation_data.action = ac
    if hasattr(arm.animation_data, 'action_slot') and ac.slots: arm.animation_data.action_slot = ac.slots[0]
    f = t * FPS; sc.frame_set(int(f), subframe=f % 1.0)
aim = Vector((0, 0, 0.95))
for sh in [x for x in opt('--shots', '').split(',') if x]:
    ct, cm = sh.split(':'); clip, t = ct.split('@')
    setpose(clip, float(t)); place(cm, aim)
    sc.render.filepath = '%s_%s_%s_%s.png' % (OUTP, clip, t, cm); bpy.ops.render.render(write_still=True)
V = opt('--video')
if V:
    # clip1+clip2+...:fps:out.mp4 -- each clip played once at its own length (looping clips twice), frames piped to ffmpeg
    clips, fps, out = V.split(':'); fps = float(fps); cmv = opt('--vcam', 'game')
    place(cmv, aim)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-i', '-', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-crf', '18', out], stdin=subprocess.PIPE)
    tmp = OUTP + '_vf.png'; n = 0
    for c in clips.split('+'):
        name, reps = (c.split('*') + ['1'])[:2]
        ac = acts[name]; T = (ac.frame_range[1] - ac.frame_range[0]) / FPS
        for r in range(int(reps)):
            nt = int(round(T * fps))
            for i in range(nt):
                setpose(name, ac.frame_range[0] / FPS + i / fps); sc.render.filepath = tmp; bpy.ops.render.render(write_still=True)
                ff.stdin.write(open(tmp, 'rb').read()); n += 1
    ff.stdin.close(); ff.wait(); os.remove(tmp); print('VIDEO', out, n, 'frames')
