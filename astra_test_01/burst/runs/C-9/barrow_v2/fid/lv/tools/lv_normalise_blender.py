"""BV2F lane LV (Phase 1.2, C7 fix): normalise one reduced Tripo GLB by ONE UNIFORM scale, and render its stills.
Derived from lane BVP's bvm_normalise_blender.py; the ONLY change is the scale: per-axis (W, D, H) -> uniform
(the model's length along X becomes <length_m>; depth and height follow the build's OWN proportions), plus a
dims json with the resulting metres so the layout is fitted to the model.

    blender --background --python lv_normalise_blender.py -- <in.glb> <out.glb> <length_m> <yaw_fix_deg> <stills_dir> <name> <dims.json>

(original BVP docstring follows)

Convention of the delivered GLB (for lane BX's slots): glTF Y-up; the model's FRONT (the sheet's FRONT view) faces +Z,
which in the greybox's Godot frame (X = sim x, Y = up, Z = sim y) is SOUTH, toward the zero-yaw camera; origin at the
centre of its footprint on the ground (min y = 0). Width W along X, depth D along Z, height H along Y, metres: each axis
scaled to the layout's size (per-axis, so the footprint is exact). yaw_fix_deg rotates the raw build about Y first, for a
generator whose front is not +Z.

Stills: four turntable views (front, right, back, left at 15 deg elevation) and the GAME CAMERA view (orthographic,
pitch 52.9535 deg, zero yaw, looking north at the model's front), soft sun from the upper left. -> <stills_dir>/<name>_*.png
"""
import math, sys
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
LEN, YAW = map(float, argv[2:4])
OUT, NAME, DIMS = argv[4], argv[5], argv[6]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in bpy.context.scene.objects:
    o.select_set(o.type == "MESH")
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
# Blender is Z-up after glTF import (glTF +Z front -> Blender -Y). Rotate the raw build by yaw_fix about the up axis.
# (BX fix, R-C9-156: transform_apply silently left the rotation unapplied on these imports -- rotate the mesh data)
from mathutils import Matrix
ob.data.transform(Matrix.Rotation(math.radians(YAW), 4, "Z"))
ob.data.update()
vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
size = mx - mn
# Blender axes: X = width, -Y = toward the front (glTF +Z), Z = up
s_u = LEN / size.x                                   # BV2F LV: ONE uniform scale (C7)
sx = sy = sz = s_u
W, D, H = size.x * s_u, size.y * s_u, size.z * s_u
import json as _json
_json.dump({"name": NAME, "raw": [size.x, size.y, size.z], "uniform_scale": s_u, "W_m": W, "D_m": D, "H_m": H,
            "yaw_fix_deg": YAW, "src": src, "dst": dst}, open(DIMS, "w"), indent=1)
for v in ob.data.vertices:
    p = v.co
    v.co = Vector(((p.x - (mn.x + mx.x) / 2) * sx, (p.y - (mn.y + mx.y) / 2) * sy, (p.z - mn.z) * sz))
ob.data.update()
print("[bvm] %s raw size %.3f x %.3f x %.3f -> %.2f x %.2f x %.2f (scale %.3f %.3f %.3f)" % (NAME, size.x, size.y, size.z, W, D, H, sx, sy, sz))
bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", export_image_format="JPEG", export_jpeg_quality=90, export_yup=True, use_selection=False)

# ---- stills
sc = bpy.context.scene
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 900, 700
sc.render.film_transparent = False
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.82, 0.85, 0.9, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.8
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 2.5
sun.rotation_euler = (math.radians(50), 0, math.radians(-35))
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"
ext = max(W, D, H)
centre = Vector((0, 0, H / 2))


def shot(tag, az_deg, el_deg, scale):
    az, el = math.radians(az_deg), math.radians(el_deg)
    # az 0 = from the front (Blender -Y side), 90 = from the model's right (+X)
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.location = centre + d * (ext * 4)
    cam.rotation_euler = (d * -1).to_track_quat("-Z", "Y").to_euler()
    cam.data.ortho_scale = scale
    sc.render.filepath = "%s/%s_%s.png" % (OUT, NAME, tag)
    bpy.ops.render.render(write_still=True)


for tag, az in (("front", 0), ("right", 90), ("back", 180), ("left", 270)):
    shot(tag, az, 15, ext * 1.25)
shot("gamecam", 0, 52.9535411256029, ext * 1.25)
print("[bvm] stills ->", OUT)
