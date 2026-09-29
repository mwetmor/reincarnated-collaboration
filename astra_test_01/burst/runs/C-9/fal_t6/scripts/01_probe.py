# T6 step 1 -- probe. Import one GLB AS DELIVERED and report its native frame,
# structure and texture set, then render four low-res unlit views round the Z
# axis so the model's real facing can be READ off a sheet rather than assumed.
# Nothing is rotated here. blender -b -noaudio --python 01_probe.py -- SRC OUT
import bpy, sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mathutils import Vector
import t6lib as L

src, outdir = sys.argv[sys.argv.index('--') + 1:][:2]
os.makedirs(outdir, exist_ok=True)
name = os.path.splitext(os.path.basename(src))[0]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
sc = bpy.context.scene
objs = L.mesh_objects(sc)

tri = 0
for o in objs:
    o.data.calc_loop_triangles()
    tri += len(o.data.loop_triangles)
verts = sum(len(o.data.vertices) for o in objs)

imgs = []
for im in bpy.data.images:
    if im.source in ('FILE', 'GENERATED') and im.size[0]:
        imgs.append(dict(name=im.name, w=im.size[0], h=im.size[1], ch=im.channels))
mats = sorted({s.material.name for o in objs for s in o.material_slots if s.material})

P = L.verts_world(objs)
mn, mx = P.min(0), P.max(0)
span = mx - mn

info = dict(
    model=name, src=src, glb_bytes=os.path.getsize(src),
    objects=len(sc.objects), meshes=len(objs),
    armatures=[o.name for o in sc.objects if o.type == 'ARMATURE'],
    shape_keys=sum(1 for o in objs if o.data.shape_keys),
    verts=verts, tris=tri, materials=mats, images=imgs,
    uv_layers=sorted({l.name for o in objs for l in o.data.uv_layers}),
    color_attrs=sorted({a.name for o in objs for a in o.data.color_attributes}),
    bbox_min=[round(v, 4) for v in mn.tolist()],
    bbox_max=[round(v, 4) for v in mx.tolist()],
    span=[round(v, 4) for v in span.tolist()],
    tallest_axis='XYZ'[int(np.argmax(span))],
)

# --- probe renders: no rotation, camera ring at the T6 elevation -------------
L.unlit(objs)
sc = L.setup_scene(res=256)
h = float(span.max())
aim = Vector(((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2))
cam = L.make_camera(sc, h * 1.25)
sigs = {}
for az in (0, 90, 180, 270):
    L.place_camera(cam, az, aim, dist=10 * h)
    bpy.context.view_layer.update()          # depsgraph, or matrix_world lies
    sc.render.filepath = f'{outdir}/{name}_az{az:03d}.png'
    bpy.ops.render.render(write_still=True)
    sigs[az] = os.path.getsize(sc.render.filepath)
info['probe_png_bytes'] = sigs
info['probe_views_differ'] = len(set(sigs.values())) > 1   # cheap sanity gate

json.dump(info, open(f'{outdir}/{name}.json', 'w'), indent=1)
print('PROBE', name, 'tris', tri, 'span', info['span'], 'differ', info['probe_views_differ'])
