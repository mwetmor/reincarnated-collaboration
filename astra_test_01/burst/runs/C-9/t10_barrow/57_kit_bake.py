"""C-9 T10-1b: bake true scale, yaw and origin into a kit prop, and measure its base.

    blender --background --python 57_kit_bake.py -- <in.glb> <out.glb> <params.json>

    params: {"a0": front azimuth deg, "yaw": deg applied after canonicalising,
             "sx": .., "sy": .., "sz": ..}      scale in CANONICAL axes (front at az 0)

The T10 manifest describes its assets and lets Godot apply the transform at load. A scatter
kit cannot do that: it exists to be instanced dozens of times, and an instance's transform
should be about WHERE IT IS, not about fixing up the asset. So scale, yaw and origin are
baked into the GLB here, and `kit_assets.json` reports them as what the model already IS --
`height_m` is its measured height and `yaw_deg` is 0, so a reader that applies the manifest
the barrow way applies identity and nothing moves twice.

AXES, written out once. glTF is Y-up; Blender is Z-up and its importer maps glTF (x, y, z)
to Blender (x, -z, y). Substituting into a glTF rotation about +Y gives a Blender rotation
about +Z by the same angle and the same sign -- so `rotate_y(f)` in Godot is a +f rotation
about Blender Z here. Derived, not guessed: a sign error in this line exports cleanly.

TRANSFORMS ARE COMPOSED ONTO EACH MESH'S OWN matrix_world, not onto a parent empty.
`transform_apply` bakes an object's OWN basis and ignores its parent's, so parenting six
meshes to one empty and applying would have silently dropped every rotation and scale on
this page. Found by reading what the operator does before running it, which is cheaper than
finding it in a contact sheet where everything is merely the wrong size.

BASE COVERAGE is measured with the camera, not with geometry code. A top-down orthographic
silhouette gives the footprint; the SAME camera with its near plane pushed down to the top
of the bottom slab gives what is actually touching the ground, since clipping a downward
camera clips by height. The area ratio is the number, and it is the right one for
`snow_bed_ok`: a cairn's bottom slab is its widest stone and covers its own footprint, two
crossed spears cover almost none of theirs, and no drift banks against a spear.
"""
import json
import math
import os
import sys

import bpy
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, DST, PARAMS = argv[0], argv[1], argv[2]
p = json.load(open(PARAMS))
GRID_PX = 768

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
for o in list(bpy.context.scene.objects):
    if o.type != "MESH":
        bpy.data.objects.remove(o, do_unlink=True)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]


def push(M: mathutils.Matrix) -> None:
    """Compose M (world space) onto every mesh and bake it into the vertex data."""
    for o in meshes:
        o.matrix_world = M @ o.matrix_world
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def bounds():
    lo, hi, rad = [1e9] * 3, [-1e9] * 3, 0.0
    for o in meshes:
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                lo[i] = min(lo[i], w[i])
                hi[i] = max(hi[i], w[i])
            rad = max(rad, math.hypot(w[0], w[1]))
    return lo, hi, rad


rz = mathutils.Matrix.Rotation
# 1. canonicalise (painted FRONT to azimuth 0); 2. scale in canonical axes
#    canonical glTF (x, y, z) -> Blender (x, -z, y), so glTF (sx, sy, sz) is Blender
#    (sx, sz, sy); 3. the yaw that turns the painted front toward the play camera.
SLAB_M = 0.10       # a snow drift's toe is a physical depth, not a share of the prop
push(rz(math.radians(-p["a0"]), 4, "Z"))
if p.get("measure_only"):
    # The canonical AABB, which the driver needs BEFORE it can work out a scale: the raw
    # AABB is in Tripo's own orientation and the front turned out to be 85-115 degrees off
    # it, so it is not a permutation of the canonical one and cannot be used as a stand-in.
    lo, hi, _ = bounds()
    print("[canon] %s" % json.dumps({"size_m_gltf": [round(hi[0] - lo[0], 6),
                                                     round(hi[2] - lo[2], 6),
                                                     round(hi[1] - lo[1], 6)]}))
    sys.exit(0)
push(mathutils.Matrix.Diagonal((p["sx"], p["sz"], p["sy"], 1.0)))

# THE OBJECT'S OWN SIZE IS MEASURED HERE, BEFORE THE YAW, AND THAT IS NOT A DETAIL.
# An AABB is world-axis-aligned, so a 2.6 m log turned 47 degrees reports 1.81 m across X
# and 2.05 m across Z and is 2.6 m in neither -- it looks like a scale bug in a manifest
# that is perfectly correct. The T10 handoff states the rule ("size unrotated, placement
# after the turn") and the first pass of this file broke it anyway, which is what the
# 1.807 in the log's row was.
_l, _h, _ = bounds()
canon = [round(_h[0] - _l[0], 5), round(_h[2] - _l[2], 5), round(_h[1] - _l[1], 5)]

push(rz(math.radians(p["yaw"]), 4, "Z"))

# 4. origin: base at y = 0, centred on the footprint
lo, hi, _ = bounds()
push(mathutils.Matrix.Translation((-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2])))

lo, hi, rad = bounds()
size_b = [hi[i] - lo[i] for i in range(3)]
out = {"size_m_gltf": canon,
       "world_aabb_after_yaw_m": [round(size_b[0], 5), round(size_b[2], 5), round(size_b[1], 5)],
       "footprint_radius_m": round(rad, 5), "base_y_min": round(lo[2], 6),
       "centre_xz_residual": [round((lo[0] + hi[0]) / 2, 6), round((lo[1] + hi[1]) / 2, 6)]}

# 5. base coverage, by clipping a downward camera
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = GRID_PX
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
sh = sc.display.shading
sh.light, sh.color_type, sh.single_color = "FLAT", "SINGLE", (1, 1, 1)
sh.show_object_outline = False
cd = bpy.data.cameras.new("c")
cd.type = "ORTHO"
cd.ortho_scale = max(size_b[0], size_b[1]) * 1.06
cam = bpy.data.objects.new("c", cd)
sc.collection.objects.link(cam)
sc.camera = cam
H = size_b[2]
top = lo[2] + H * 1.2                      # camera 20% of the height above the model
cam.location = (0, 0, top)
cam.rotation_euler = (0, 0, 0)             # a default camera looks along -Z: straight down
cd.clip_end = (top - lo[2]) * 1.001
tmp = os.path.splitext(DST)[0]
slab_h = min(SLAB_M, H * 0.9)
for tag, near in (("full", 1e-4), ("slab", top - (lo[2] + slab_h))):
    cd.clip_start = max(1e-4, near)
    sc.render.filepath = "%s_%s.png" % (tmp, tag)
    bpy.ops.render.render(write_still=True)

bpy.ops.object.select_all(action="DESELECT")
cam.select_set(True)
bpy.ops.object.delete()
bpy.ops.export_scene.gltf(filepath=DST, export_format="GLB", export_image_format="JPEG",
                          export_jpeg_quality=88, export_yup=True)
out["slab_m"] = round(slab_h, 4)
print("[bake] %s" % json.dumps(out))
with open(os.path.splitext(DST)[0] + "_bake.json", "w") as f:
    json.dump(out, f, indent=1)
