"""barrow_v2 hero models (lane BVP, drax): normalise one reduced Tripo GLB to the layout's metres, and render its stills.

    blender --background --python bvm_normalise_blender.py -- <in.glb> <out.glb> <W> <D> <H> <yaw_fix_deg> <stills_dir> <name>

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
W, D, H, YAW = map(float, argv[2:6])
OUT, NAME = argv[6], argv[7]

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
ob.rotation_euler = (0, 0, math.radians(YAW))
bpy.ops.object.transform_apply(rotation=True)
vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
size = mx - mn
# Blender axes: X = width, -Y = toward the front (glTF +Z), Z = up
sx, sy, sz = W / size.x, D / size.y, H / size.z
for v in ob.data.vertices:
    p = v.co
    v.co = Vector(((p.x - (mn.x + mx.x) / 2) * sx, (p.y - (mn.y + mx.y) / 2) * sy, (p.z - mn.z) * sz))
ob.data.update()
print("[bvm] %s raw size %.3f x %.3f x %.3f -> %.2f x %.2f x %.2f (scale %.3f %.3f %.3f)" % (NAME, size.x, size.y, size.z, W, D, H, sx, sy, sz))
bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", export_image_format="JPEG", export_jpeg_quality=90, export_yup=True, use_selection=False)

# ---- stills
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderEngine.bl_rna.properties["bl_idname"].enum_items.keys() else "BLENDER_EEVEE"
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
