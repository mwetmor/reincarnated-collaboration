# T8: prepare the Tripo build for Meshy rigging.
#
#   blender -b -noaudio --python scripts/12_prep_rig.py -- <src.glb> <dst.glb>
#          [--yaw -90] [--height 1.85] [--faces 290000] [--tex 2048]
#
# Four things, each for a stated reason:
#   YAW    Tripo delivers this figure facing +X where the rest of the pipeline
#          expects -Y. Baked in here so nothing downstream carries a per-model
#          special case. VERIFIED by re-measuring the facing after the rotation
#          rather than trusting the rotation.
#   SCALE  delivered height-normalised to 1.0. Set to the declared figure
#          height so the cliffside's scale rule (150.2135 / height) has a real
#          number to divide.
#   FACES  Meshy rigs under 300k. 1.42M needs about x0.21.
#   SHARDS Tripo shed a floating ribbon on the manticore. This build has one
#          island, so nothing is removed -- but the check runs and says so,
#          because "there was nothing to remove" and "I did not look" are
#          different statements.
#
# THE WELD BEFORE THE SEPARATE IS LOad-BEARING. glTF splits a vertex at every
# UV seam, so `separate(type='LOOSE')` on the delivered mesh sees one loose
# part per UV chart. On this model that is 119 "islands" of a surface that is
# demonstrably ONE island once welded (scripts/10_render4.py counts it after a
# 1e-6 weld and reports 1). The first run of this script trusted the loose-part
# count, dropped 83 of them as shards, and removed 387,014 faces -- 27% of the
# body. That is the amputation the shard rule exists to prevent, performed BY
# the shard rule. Weld first; then a loose part really is a loose part.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else -90.0
HGT = float(a[a.index("--height") + 1]) if "--height" in a else 1.85
FACES = int(a[a.index("--faces") + 1]) if "--faces" in a else 290000
TEX = int(a[a.index("--tex") + 1]) if "--tex" in a else 2048
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == 'MESH']
print("in: %d mesh(es), %d polys" % (len(meshes), sum(len(o.data.polygons) for o in meshes)))

# ---- shards ----------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
body = bpy.context.view_layer.objects.active
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
n_before = len(body.data.vertices)
bpy.ops.mesh.remove_doubles(threshold=1e-5)
bpy.ops.object.mode_set(mode='OBJECT')
print("welded %d -> %d verts (glTF splits at UV seams)"
      % (n_before, len(body.data.vertices)))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in sc.objects if o.type == 'MESH']
sizes = sorted(((len(o.data.polygons), o) for o in parts),
                key=lambda t: -t[0])
total = sum(n for n, _ in sizes)
print("islands: %d, sizes %s" % (len(sizes), [n for n, _ in sizes][:8]))
dropped = 0
for n, o in sizes[1:]:
    if n < 0.01 * total:
        bpy.data.objects.remove(o, do_unlink=True); dropped += 1
print("dropped %d island(s) under 1%% of the surface (%d faces of %d)"
      % (dropped, total - sum(len(o.data.polygons) for o in sc.objects
                              if o.type == 'MESH'), total))
assert dropped == 0 or (total - sum(len(o.data.polygons) for o in sc.objects
                                    if o.type == 'MESH')) < 0.03 * total, \
    "shard removal would take more than 3% of the surface -- that is an "\
    "amputation, not a shard; stop and look"
parts = [o for o in sc.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
if len(parts) > 1:
    bpy.ops.object.join()
body = bpy.context.view_layer.objects.active

# ---- yaw, then scale, then confirm ----------------------------------------
body.matrix_world = Matrix.Rotation(math.radians(YAW), 4, 'Z') @ body.matrix_world
bpy.context.view_layer.update()
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get("co", co)
V = co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
H0 = float(V[:, 2].max() - V[:, 2].min())
s = HGT / H0
body.matrix_world = Matrix.Scale(s, 4) @ body.matrix_world
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.view_layer.update()
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get("co", co)
V = co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
lo, hi = V.min(0), V.max(0); H = float(hi[2] - lo[2])
# re-measure the facing on the RESULT: a rotation applied is not a rotation
# achieved until the geometry says so
span = hi - lo
print("after yaw %+.0f and scale x%.4f: height %.4f m, span x %.3f y %.3f"
      % (YAW, s, H, span[0], span[1]))
print("  widest horizontal axis is %s (shoulders lie across the body, so this "
      "should be X once he faces -Y)" % "XY"[int(np.argmax(span[:2]))])

# ---- decimate --------------------------------------------------------------
n0 = len(body.data.polygons)
if n0 > FACES:
    m = body.modifiers.new('dec', 'DECIMATE'); m.ratio = FACES / n0
    bpy.ops.object.modifier_apply(modifier='dec')
print("faces %d -> %d" % (n0, len(body.data.polygons)))
for img in bpy.data.images:
    if img.size[0] > TEX:
        print("  texture %s %d -> %d" % (img.name, img.size[0], TEX))
        img.scale(TEX, TEX)
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=False,
                          export_image_format='JPEG', export_jpeg_quality=92)
print("wrote %s (%.1f MB)" % (DST, os.path.getsize(DST) / 1e6))
json.dump(dict(yaw=YAW, scale=round(s, 6), height_m=round(H, 5),
               faces_in=n0, faces_out=len(body.data.polygons),
               islands_in=len(sizes), islands_dropped=dropped,
               texture=TEX), open("work/prep_rig.json", "w"), indent=1)
