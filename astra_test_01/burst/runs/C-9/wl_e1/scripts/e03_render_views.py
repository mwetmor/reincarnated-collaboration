# Render a GLB from 4 (or N) horizontal headings, orthographic, unlit (emission of base colour) + alpha, for
# silhouette IoU against the sheet's cut-outs and for eyes.
#   blender -b -noaudio --python e03_render_views.py -- <in.glb> <outprefix> [--n 4] [--res 768] [--pitch 0]
import bpy, sys, math, os
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUTP = a[0], a[1]
N = int(a[a.index('--n') + 1]) if '--n' in a else 4
RES = int(a[a.index('--res') + 1]) if '--res' in a else 768
PITCH = float(a[a.index('--pitch') + 1]) if '--pitch' in a else 0.0
YAW0 = float(a[a.index('--yaw0') + 1]) if '--yaw0' in a else 0.0
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
for o in sc.objects:
    if o.type == 'ARMATURE' and o.animation_data:
        o.animation_data.action = None
        for pb in o.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
ms = [o for o in sc.objects if o.type == 'MESH']
pts = []
for o in ms:
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    M = o.matrix_world
    co = np.empty(len(me.vertices)*3); me.vertices.foreach_get('co', co); co = co.reshape(-1,3)[::max(1, len(me.vertices)//4000)]
    Mn = np.array(M); pts += list(co @ Mn[:3,:3].T + Mn[:3,3])
P = np.array(pts); lo, hi = P.min(0), P.max(0); c = (lo + hi) / 2; H = hi[2] - lo[2]
for o in ms:
    for s in o.material_slots:
        m = s.material
        if not m or not m.node_tree: continue
        nt = m.node_tree; out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        tex = next((n for n in nt.nodes if n.type == 'TEX_IMAGE'), None)
        em = nt.nodes.new('ShaderNodeEmission')
        if tex: nt.links.new(tex.outputs['Color'], em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = RES
sc.view_settings.view_transform = 'Standard'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(H, hi[0]-lo[0], hi[1]-lo[1]) * 1.08
for i in range(N):
    yaw = math.radians(YAW0 + 360.0 * i / N); pit = math.radians(PITCH)
    d = Vector((math.sin(yaw) * math.cos(pit), -math.cos(yaw) * math.cos(pit), math.sin(pit)))
    cam.location = Vector(c) + d * (H * 4)
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = '%s_%03d.png' % (OUTP, round(YAW0 + 360.0 * i / N))
    bpy.ops.render.render(write_still=True)
print('bbox lo', lo, 'hi', hi, 'H', H)
