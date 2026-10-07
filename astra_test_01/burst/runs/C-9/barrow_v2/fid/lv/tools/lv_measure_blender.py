"""BV2F LV: measure a normalised kit GLB (front -> +Z glTF, metres): orthographic ELEVATION renders (0 deg) and vertex stats.
    blender -b --python lv_measure_blender.py -- <in.glb> <out_prefix> [px_per_m]
Writes <out_prefix>_elev_front.png (true elevation, px_per_m known), <out_prefix>_elev_right.png, <out_prefix>_plan.png, and
<out_prefix>_measure.json: AABB; height profile (max z) along X in 0.5 m bins; depth profile (front-most y) along X."""
import bpy, sys, json, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]
src, pre = a[0], a[1]
ppm = float(a[2]) if len(a) > 2 else 40.0
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
obs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
vs = [o.matrix_world @ v.co for o in obs for v in o.data.vertices]
mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
# Blender: X width, -Y front (glTF +Z), Z up
prof = {}
for v in vs:
    k = round(math.floor(v.x / 0.5) * 0.5, 2)
    p = prof.setdefault(k, [-1e9, 1e9, -1e9])
    p[0] = max(p[0], v.z)
    p[1] = min(p[1], v.y)      # front-most (most negative y)
    p[2] = max(p[2], v.y)      # back-most
json.dump({"aabb_min": list(mn), "aabb_max": list(mx), "size": list(mx - mn),
           "x_bins": {str(k): {"z_max": round(p[0], 3), "y_front": round(p[1], 3), "y_back": round(p[2], 3)} for k, p in sorted(prof.items())}},
          open(pre + "_measure.json", "w"), indent=1)
sc = bpy.context.scene
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"
c = (mn + mx) / 2
size = mx - mn


def shot(tag, loc, rot, w_m, h_m):
    sc.render.resolution_x, sc.render.resolution_y = int(w_m * ppm), int(h_m * ppm)
    cam.data.ortho_scale = max(w_m, h_m)
    cam.location = loc
    cam.rotation_euler = rot
    sc.render.filepath = pre + "_" + tag + ".png"
    bpy.ops.render.render(write_still=True)


m = 1.0
shot("elev_front", Vector((c.x, mn.y - 50, c.z)), (math.radians(90), 0, 0), size.x + 2 * m, size.z + 2 * m)
shot("elev_right", Vector((mx.x + 50, c.y, c.z)), (math.radians(90), 0, math.radians(90)), size.y + 2 * m, size.z + 2 * m)
shot("plan", Vector((c.x, c.y, mx.z + 50)), (0, 0, 0), size.x + 2 * m, size.y + 2 * m)
print("[measure]", pre, list(size))
