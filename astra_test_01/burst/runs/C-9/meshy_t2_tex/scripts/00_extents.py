# What shape is this creature from each of the eight directions? A uniform grid
# is only the right layout if the views are roughly the same aspect; on a
# quadruped they are not, and the approved MC-1 sheet already gives the wide
# side views wide cells. Measure before choosing.
#
#   blender -b -noaudio --python scripts/00_extents.py -- <blend>
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
BLEND = a[0]
ELEV = 19.77
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135,
       "N": 180, "NW": 225, "W": 270, "SW": 315}

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH']
arms = [o for o in sc.objects if o.type == 'ARMATURE']
P = []
for o in objs:
    M = np.array(o.matrix_world.to_3x3()).T
    co = np.empty(len(o.data.vertices) * 3)
    o.data.vertices.foreach_get("co", co)
    P.append(co.reshape(-1, 3) @ M + np.array(o.matrix_world.translation))
P = np.vstack(P)
print("meshes: %s   armatures: %s" % ([o.name for o in objs], [o.name for o in arms]))
print("world bbox lo %s hi %s  span %s"
      % (np.round(P.min(0), 4).tolist(), np.round(P.max(0), 4).tolist(),
         np.round(P.max(0) - P.min(0), 4).tolist()))

# screen basis straight off a real camera, not a derived formula: the camera is
# what the render will use, and a hand-derived basis is one sign error from a
# mirrored sheet.
cam = bpy.data.objects.new('probe', bpy.data.cameras.new('probe'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
el = math.radians(ELEV)
aim = Vector((0.0, 0.0, float(P[:, 2].max() - P[:, 2].min()) * 0.5))
rows = {}
for d in DIRS:
    A = math.radians(AZI[d])
    pos = aim + Vector((math.sin(A) * math.cos(el), math.cos(A) * math.cos(el),
                        math.sin(el))) * 20.0
    cam.location = pos
    cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()
    # matrix_world is only recomputed on depsgraph evaluation. Without this the
    # camera reads as identity and every direction returns the WORLD bbox span
    # -- eight identical rows, which is how this was caught: a quadruped cannot
    # look the same from the front as from the side, and a constant is a tell.
    bpy.context.view_layer.update()
    R = np.array(cam.matrix_world.to_3x3())
    right, up = R[:, 0], R[:, 1]
    x = P @ right; y = P @ up
    w = float(x.max() - x.min()); h = float(y.max() - y.min())
    rows[d] = dict(width_m=round(w, 4), height_m=round(h, 4),
                   aspect=round(w / h, 4),
                   cx=round(float((x.max() + x.min()) * 0.5), 5),
                   cy=round(float((y.max() + y.min()) * 0.5), 5))
    print("  %-3s  %6.3f m wide x %6.3f m tall   aspect %5.3f" % (d, w, h, w / h))
mx = max(r["width_m"] for r in rows.values())
my = max(r["height_m"] for r in rows.values())
print("worst-case box over all 8 views: %.3f x %.3f m  (aspect %.3f)"
      % (mx, my, mx / my))
json.dump(dict(elevation_deg=ELEV, per_dir=rows,
               worst_width_m=round(mx, 4), worst_height_m=round(my, 4),
               world_span=np.round(P.max(0) - P.min(0), 4).tolist()),
          open(os.path.join(os.path.dirname(os.path.dirname(
              os.path.abspath(__file__))), "work", "extents.json"), "w"), indent=1)
