# T6 step 2a -- render each model AS DELIVERED (no yaw, no mirror) at elevation
# 0, the four cardinal azimuths, unlit. Elevation 0 because these frames are
# matched against the PAINTED four-view plates, which are flat orthographic;
# R-C9-68's 52.95 deg is the presentation angle and is used everywhere else.
# 03_fit_orient.py then scores the four yaw x two mirror hypotheses off these.
# blender -b -noaudio --python 02_orient_render.py -- SRC OUT
import bpy, sys, os, json
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
colour_src = L.unlit(objs)
norm = L.normalise(sc, objs, yaw_deg=0.0, flip_x=False, target_h=1.0)

sc = L.setup_scene(res=640)
cam = L.make_camera(sc, 2.6)
aim = (0.0, 0.0, 0.5)
cams = {}
for az in (0, 90, 180, 270):
    pos = L.place_camera(cam, az, aim, dist=12.0, elev=0.0)
    bpy.context.view_layer.update()
    sc.render.filepath = f'{outdir}/{name}_az{az:03d}.png'
    bpy.ops.render.render(write_still=True)
    cams[az] = [round(v, 4) for v in pos]

json.dump(dict(model=name, norm=norm, colour_source=colour_src, cam_pos=cams),
          open(f'{outdir}/{name}.json', 'w'), indent=1)
print('ORIENT-RENDER', name, norm, colour_src)
