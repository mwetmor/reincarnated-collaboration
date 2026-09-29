# T6 step 3 -- the deliverable renders, from ONE normalised frame per model.
#
#   (a) UNLIT base colour, 8 directions, elevation 52.95354112560294 (R-C9-68)
#   (b) LIT CLAY, 4 directions (S, E, N, SE), same elevation, texture stripped
#   (c) HEAD close-up, unlit, from S at the same elevation
#   (d) SILHOUETTE set: front/right/back/left at elevation 0, to be matched
#       against the painted plates. Elevation 0 here and ONLY here, because the
#       plates are flat orthographic and an IoU against them has to be measured
#       in their own projection. Doubles as the side-on geometry read.
#
# Framing is a per-SUBJECT constant, not per-model, so the rows of a contact
# sheet show real proportion differences instead of six figures each fitted to
# its own box. Every model is height-normalised to 1.0 m, feet on z = 0.
# blender -b -noaudio --python 04_render.py -- SRC OUTROOT YAW
import bpy, sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mathutils import Vector
import t6lib as L

a = sys.argv[sys.argv.index('--') + 1:]
src, root, yaw = a[0], a[1], float(a[2])
name = os.path.splitext(os.path.basename(src))[0]
subject = name.split('_')[0]
for sub in ('unlit', 'clay', 'head', 'silh'):
    os.makedirs(f'{root}/{sub}', exist_ok=True)

FRAME = dict(knight=dict(ortho=1.25, aim_z=0.50, head_ortho=0.42, res=512),
             manticore=dict(ortho=2.05, aim_z=0.50, head_ortho=0.58, res=512))[subject]
SILH = dict(knight=1.25, manticore=2.05)[subject]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
sc = bpy.context.scene
objs = L.mesh_objects(sc)
colour_src = L.unlit(objs)
norm = L.normalise(sc, objs, yaw_deg=yaw, flip_x=False, target_h=1.0)

P = L.verts_world(objs)
zmax = float(P[:, 2].max())
head = P[P[:, 2] > zmax - 0.18]                     # the helm / the man's head
head_c = [float(np.median(head[:, 0])), float(np.median(head[:, 1])), float(head[:, 2].mean())]

# ---------- (a) unlit, 8 directions, R-C9-68 elevation -----------------------
sc = L.setup_scene(res=FRAME['res'])
cam = L.make_camera(sc, FRAME['ortho'])
aim = (0.0, 0.0, FRAME['aim_z'])
seen = {}
for d in L.DIRS:
    pos = L.place_camera(cam, L.AZI[d], aim, dist=12.0)
    bpy.context.view_layer.update()
    sc.render.filepath = f'{root}/unlit/{name}_{d}.png'
    bpy.ops.render.render(write_still=True)
    seen[d] = [round(v, 4) for v in pos]

# ---------- (d) silhouettes, elevation 0, the plates' own projection ---------
cam.data.ortho_scale = SILH
for v, az in L.INPUT_AZI.items():
    L.place_camera(cam, az, (0.0, 0.0, 0.5), dist=12.0, elev=0.0)
    bpy.context.view_layer.update()
    sc.render.filepath = f'{root}/silh/{name}_{v}.png'
    bpy.ops.render.render(write_still=True)

# ---------- (c) head close-up, unlit, S ------------------------------------
cam.data.ortho_scale = FRAME['head_ortho']
L.place_camera(cam, 0, head_c, dist=12.0)
bpy.context.view_layer.update()
sc.render.filepath = f'{root}/head/{name}_S.png'
bpy.ops.render.render(write_still=True)

# ---------- (b) lit clay, 4 directions -------------------------------------
L.clay(objs)
L.key_light(sc, (0.0, 0.0, FRAME['aim_z']), 1.0)
cam.data.ortho_scale = FRAME['ortho']
for d in ('S', 'E', 'N', 'SE'):
    L.place_camera(cam, L.AZI[d], aim, dist=12.0)
    bpy.context.view_layer.update()
    sc.render.filepath = f'{root}/clay/{name}_{d}.png'
    bpy.ops.render.render(write_still=True)

json.dump(dict(model=name, yaw_applied=yaw, flip_x=False, norm=norm,
               colour_source=colour_src, head_centre=[round(v, 4) for v in head_c],
               elevation_deg=L.ELEV, ortho=FRAME, cam_pos_unlit=seen),
          open(f'{root}/{name}_render.json', 'w'), indent=1)
print('RENDER', name, 'yaw', yaw, 'head', head_c, 'colour', colour_src)
