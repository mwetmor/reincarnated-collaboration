# EN-E3 renders FROM THE SHIPPED GLB (never from the build scene), Workbench, flat light, texture colour, transparent film.
#   blender -b -noaudio --python scripts/n05_render.py -- <glb> look  <out.png>
#   blender -b -noaudio --python scripts/n05_render.py -- <glb> sheet <out.png> <state:clip:frame>[,...]     8 headings x states
#   blender -b -noaudio --python scripts/n05_render.py -- <glb> film  <out.mp4> <clip:repeats:dir>[,...]     play speed, 30 fps
# GAME CAMERA (sprite-cell contract § 2.3): orthographic, pitch 52.9535411256029 deg down, camera-relative headings. The creature
# turns in front of a fixed camera; heading d's yaw = 90 deg - facing_ground_bearing(d) (model faces -Y at yaw 0 = S, toward camera).
# The film writes straight to an MP4 (no frame dump on disk). Root motion is stripped in the clips; a film can add the clip's
# ground speed back as a scrolling floor grid so foot-lock reads by eye (--speeds clip=v,...).
import bpy, sys, os, math, json
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
GLB, MODE, OUT = a[0], a[1], a[2]
ARG = a[3] if len(a) > 3 else ''
SPEEDS = dict((k, float(v)) for k, v in (p.split('=') for p in a[a.index('--speeds') + 1].split(','))) if '--speeds' in a else {}
PITCH = 52.9535411256029
BEAR = dict(S=90, SW=135, W=180, NW=225, N=270, NE=315, E=0, SE=45)
DIRS = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
bpy.ops.wm.read_factory_settings(use_empty=True)
# FPS BEFORE IMPORT (found on the raptor, 2026-10-02): the glTF importer maps clip seconds onto scene frames at the scene's CURRENT
# fps; read_factory_settings leaves 24, so every earlier film played its 30 fps clips 25 % fast and every still's 'f<n>' was a
# 24 fps frame. The GLBs were right (Godot reads seconds); the renders were not.
bpy.context.scene.render.fps = 30
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene
sc.render.fps = 30
arm = next((o for o in sc.objects if o.type == 'ARMATURE'), None)
meshes = [o for o in sc.objects if o.type == 'MESH']
top = arm or meshes[0]
while top.parent: top = top.parent
# Workbench's TEXTURE colour is the material's ACTIVE image node: with an emissive map present the importer can leave the emission
# image active and the whole body renders black (found on the gazer) -- make the BASE COLOUR image active
for _m in bpy.data.materials:
    if _m.node_tree:
        _b = next((nd for nd in _m.node_tree.nodes if nd.type == 'BSDF_PRINCIPLED'), None)
        if _b and _b.inputs['Base Color'].links:
            _src = _b.inputs['Base Color'].links[0].from_node
            while _src.type != 'TEX_IMAGE' and _src.inputs and any(i.links for i in _src.inputs):
                _src = next(i.links[0].from_node for i in _src.inputs if i.links)
            if _src.type == 'TEX_IMAGE': _m.node_tree.nodes.active = _src
piv = bpy.data.objects.new('pivot', None); sc.collection.objects.link(piv)
for o in sc.objects:
    if o.parent is None and o is not piv: o.parent = piv
if arm and arm.animation_data:
    for t in arm.animation_data.nla_tracks: t.mute = True
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'TEXTURE'
sc.view_settings.view_transform = 'Standard'
sc.render.film_transparent = True

def set_clip(name):
    if not arm: return 0
    act = bpy.data.actions[name]
    ad = arm.animation_data or arm.animation_data_create()
    ad.action = act
    try:
        if act.slots and ad.action_slot is None: ad.action_slot = act.slots[0]
    except Exception: pass
    r = act.frame_range; return int(round(r[1]))

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'

def cam_game(aim, size):
    el = math.radians(PITCH)
    pos = Vector(aim) + Vector((0, -math.cos(el), math.sin(el))) * 30
    cam.location = pos; cam.rotation_euler = (Vector(aim) - pos).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = size

def cam_elev(aim, az_vec, elev, size):
    el = math.radians(elev); d = Vector(az_vec).normalized()
    pos = Vector(aim) + Vector((d.x * math.cos(el), d.y * math.cos(el), math.sin(el))) * 30
    cam.location = pos; cam.rotation_euler = (Vector(aim) - pos).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = size

def bbox():
    dg = bpy.context.evaluated_depsgraph_get(); lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in meshes:
        e = o.evaluated_get(dg)
        for c in e.bound_box:
            w = e.matrix_world @ Vector(c); lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    return lo, hi

def render(path, w, h):
    sc.render.resolution_x, sc.render.resolution_y = w, h; sc.render.filepath = path
    bpy.ops.render.render(write_still=True)

import subprocess, tempfile, shutil
TMP = tempfile.mkdtemp(prefix='en3r_', dir=os.environ.get('EN3_TMP', '/private/tmp/claude-501'))

def compose(cells, cols, labels, out, title):
    # system python composes (Blender's python has no PIL); the cell PNGs live in a temp dir that is deleted after
    spec = os.path.join(TMP, 'spec.json'); json.dump(dict(cells=cells, cols=cols, labels=labels, out=out, title=title), open(spec, 'w'))
    subprocess.run(['/usr/bin/env', 'python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'n06_compose.py'), spec], check=True)

if MODE == 'look':
    lo, hi = bbox(); c = (lo + hi) / 2; L = max(hi - lo) * 1.15
    views = [('front', (0, -1), 0), ('right side', (-1, 0), 0), ('back', (0, 1), 0), ('left side', (1, 0), 0), ('top', (0, -0.0001), 89.9)]
    cells, labels = [], []
    for nm, az, el in views:
        cam_elev(c, az, el, L); p = os.path.join(TMP, 'look_%s.png' % nm.replace(' ', '_')); render(p, 512, 512); cells.append(p); labels.append(nm)
    for d in ('S', 'SW', 'E'):
        piv.rotation_euler = (0, 0, math.radians(90 - BEAR[d])); bpy.context.view_layer.update()
        cam_game((0, 0, (hi.z) * 0.4), L); p = os.path.join(TMP, 'look_g%s.png' % d); render(p, 512, 512); cells.append(p); labels.append('game cam ' + d)
    compose(cells, 4, labels, OUT, os.path.basename(GLB) + ' rest')
elif MODE == 'sheet':
    rows = [r.split(':') for r in ARG.split(',')]
    set_clip(rows[0][1]); sc.frame_set(0); lo, hi = bbox()
    L = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z) * 1.35
    cells, labels = [], []
    for st, clip, fr in rows:
        set_clip(clip); sc.frame_set(int(fr))
        for d in DIRS:
            piv.rotation_euler = (0, 0, math.radians(90 - BEAR[d])); bpy.context.view_layer.update()
            cam_game((0, 0, hi.z * 0.35), L); p = os.path.join(TMP, 's_%s_%s.png' % (st, d)); render(p, 320, 320); cells.append(p)
            labels.append('%s %s f%s' % (st, d, fr))
    compose(cells, 8, labels, OUT, os.path.basename(GLB) + ' 8 headings, game camera 52.95 deg ortho')
elif MODE == 'strip':
    # one heading, many frames: <dir>|clip:frame,clip:frame,...  (debug look at deformation)
    d, rest = ARG.split('|'); items = [r.split(':') for r in rest.split(',')]
    set_clip(items[0][0]); sc.frame_set(0); lo, hi = bbox(); L = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z) * 1.15
    cells, labels = [], []
    for clip, fr in items:
        set_clip(clip); sc.frame_set(int(fr)); piv.rotation_euler = (0, 0, math.radians(90 - BEAR[d])); bpy.context.view_layer.update()
        if '--legs' in a: cam_elev((0, 0, 0.6), (0, -1, 0), 8, 2.2)
        elif '--side' in a: cam_elev((0, 0, hi.z * 0.45), (0, -1, 0), 8, L)
        else: cam_game((0, 0, hi.z * 0.35), L)
        p = os.path.join(TMP, 'st_%s_%s.png' % (clip, fr)); render(p, 400, 400); cells.append(p); labels.append('%s f%s %s' % (clip, fr, d))
    compose(cells, 6, labels, OUT, os.path.basename(GLB) + ' strip')
elif MODE == 'film':
    segs = [r.split(':') for r in ARG.split(',')]
    set_clip(segs[0][0]); sc.frame_set(0); lo, hi = bbox()
    L = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z) * 1.6
    # bake the sequence into one NLA-free timeline: per output frame choose clip + local frame
    seq = []
    for clip, rep, d in segs:
        n = set_clip(clip)
        for r in range(int(rep)):
            for f in range(n if int(rep) > 1 else n + 1): seq.append((clip, f, d))
    sc.render.film_transparent = False
    sc.world = bpy.data.worlds.new('w'); sc.world.color = (0.62, 0.58, 0.52)
    # floor grid that scrolls at the clip's ground speed (root motion is stripped, so the floor moves instead)
    # a CHECKER floor (0.5 m squares) that scrolls at the clip's ground speed: Workbench does not draw wire in a render, so the
    # floor is a texture (made in numpy, written to the temp dir) -- foot-lock reads by eye when a planted foot moves with the floor
    import numpy as _np
    _n = 2000; _q = 50; _yy, _xx = _np.mgrid[0:_n, 0:_n]; _c = (((_xx // _q) + (_yy // _q)) % 2).astype(_np.float32)
    _img = bpy.data.images.new('chk', _n, _n); _px = _np.ones((_n, _n, 4), _np.float32)
    _px[..., 0] = 0.50 + 0.08 * _c; _px[..., 1] = 0.47 + 0.08 * _c; _px[..., 2] = 0.42 + 0.08 * _c; _img.pixels.foreach_set(_px.ravel())
    bpy.ops.mesh.primitive_plane_add(size=20); fl = bpy.context.active_object
    fm = bpy.data.materials.new('floor'); fm.use_nodes = True; _tn = fm.node_tree.nodes.new('ShaderNodeTexImage'); _tn.image = _img
    fm.node_tree.links.new(_tn.outputs['Color'], fm.node_tree.nodes['Principled BSDF'].inputs['Base Color']); fl.data.materials.append(fm)
    fl.location.z = -0.002
    sc.display.shading.color_type = 'TEXTURE'
    sc.frame_start, sc.frame_end = 1, len(seq)
    sc.render.resolution_x, sc.render.resolution_y = 768, 768
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    sc.render.filepath = os.path.join(TMP, 'film_')
    frames = []
    for i in range(len(seq)):
        clip, f, d = seq[i]; set_clip(clip); sc.frame_set(f)
        piv.rotation_euler = (0, 0, math.radians(90 - BEAR[d]))
        v = SPEEDS.get(clip, 0.0); fwd = Vector((math.cos(math.radians(BEAR[d])), -math.sin(math.radians(BEAR[d])), 0))
        fl.location = -(fwd * ((v * i / 30.0) % 1.0)); fl.location.z = -0.002
        bpy.context.view_layer.update()
        cam_game((0, 0, hi.z * 0.35), L)
        p = os.path.join(TMP, 'f_%05d.png' % i); sc.render.image_settings.file_format = 'PNG'; render(p, 768, 768); frames.append(p)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(TMP, 'f_%05d.png'), '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '20', OUT], check=True)
    print('film %s: %d frames %.2f s' % (OUT, len(seq), len(seq) / 30))
shutil.rmtree(TMP, ignore_errors=True)
