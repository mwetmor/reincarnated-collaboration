# D2: pull one gear piece out of a DRESSED Tripo build.
#
#   blender -b -noaudio --python scripts/05_isolate.py -- <dressed.glb>
#          <base.glb> <out.glb> --region head|forearms|torso|shoulders
#          [--yaw -90] [--dist 0.004] [--report work/iso.json]
#
# Two signals, because neither alone is enough:
#
#   DISTANCE from the base body. A garment stands off the skin, so its vertices
#   are further from the base surface than the skin's own are. On its own this
#   is marginal for a mail shirt, which sits millimetres out, and the two
#   builds are separate generations so they disagree by millimetres anyway.
#
#   REGION, taken from the BASE RIG'S BONES rather than from a box. The helmet
#   is near the head bone, the bracers near the forearms, the byrnie on the
#   spine and upper legs, the mantle on the shoulders and chest. Bones are
#   already the anatomy and they cost nothing.
#
# The weld comes FIRST, before anything counts islands or components: glTF
# splits a vertex at every UV seam, and separating by loose parts on the
# delivered mesh sees one part per UV chart. That mistake removed 27% of a body
# in T8.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
DRESSED, BASE, OUT = a[0], a[1], a[2]
REGION = a[a.index("--region") + 1] if "--region" in a else "head"
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else -90.0
DIST = float(a[a.index("--dist") + 1]) if "--dist" in a else 0.004
REP = a[a.index("--report") + 1] if "--report" in a else None

BONES = dict(
    head=["Head", "head_end", "headfront", "neck"],
    forearms=["LeftForeArm", "LeftHand", "RightForeArm", "RightHand"],
    torso=["Hips", "Spine", "Spine01", "Spine02", "LeftUpLeg", "RightUpLeg"],
    shoulders=["LeftShoulder", "RightShoulder", "Spine02", "neck",
               "LeftArm", "RightArm"])
RADIUS = dict(head=0.22, forearms=0.16, torso=0.42, shoulders=0.34)


def load(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    return bpy.context.scene


# ---- base: skinned mesh + bone positions ----------------------------------
load(BASE)
sc = bpy.context.scene
bmesh_objs = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
barm = next(o for o in sc.objects if o.type == 'ARMATURE')
BV = []
for o in bmesh_objs:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    BV.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
              + np.array(o.matrix_world.translation))
BV = np.vstack(BV)
BF = []
for o in bmesh_objs:
    o.data.calc_loop_triangles()
    off = 0
    BF.append(np.array([list(t.vertices) for t in o.data.loop_triangles]) + off)
BF = np.vstack(BF)
bone_pts = {}
for b in barm.pose.bones:
    h = barm.matrix_world @ b.head
    t = barm.matrix_world @ b.tail
    bone_pts[b.name] = (np.array(h), np.array(t))
blo, bhi = BV.min(0), BV.max(0)
BH = float(bhi[2] - blo[2])
print("base: %d verts, %d tris, height %.4f m" % (len(BV), len(BF), BH))
base_tree = BVHTree.FromPolygons([Vector(p) for p in BV.tolist()],
                                 [list(map(int, f)) for f in BF])

# ---- dressed: weld, yaw, scale to the base's height ------------------------
load(DRESSED)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
if len(objs) > 1:
    bpy.ops.object.join()
d = bpy.context.view_layer.objects.active
n0 = len(d.data.vertices)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=1e-5)
bpy.ops.object.mode_set(mode='OBJECT')
print("dressed: welded %d -> %d verts" % (n0, len(d.data.vertices)))
d.matrix_world = Matrix.Rotation(math.radians(YAW), 4, 'Z') @ d.matrix_world
bpy.context.view_layer.update()
co = np.empty(len(d.data.vertices) * 3); d.data.vertices.foreach_get("co", co)
DV = co.reshape(-1, 3) @ np.array(d.matrix_world.to_3x3()).T + np.array(d.matrix_world.translation)
s = BH / float(DV[:, 2].max() - DV[:, 2].min())
d.matrix_world = Matrix.Scale(s, 4) @ d.matrix_world
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.view_layer.update()
co = np.empty(len(d.data.vertices) * 3); d.data.vertices.foreach_get("co", co)
DV = co.reshape(-1, 3) @ np.array(d.matrix_world.to_3x3()).T + np.array(d.matrix_world.translation)
# align feet and midline to the base's
off = np.array([np.median(BV[:, 0]) - np.median(DV[:, 0]),
                np.median(BV[:, 1]) - np.median(DV[:, 1]),
                blo[2] - DV[:, 2].min()])
d.matrix_world = Matrix.Translation(Vector(off.tolist())) @ d.matrix_world
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.view_layer.update()
co = np.empty(len(d.data.vertices) * 3); d.data.vertices.foreach_get("co", co)
DV = co.reshape(-1, 3) @ np.array(d.matrix_world.to_3x3()).T + np.array(d.matrix_world.translation)
print("dressed: scaled x%.5f, offset %s, height %.4f"
      % (s, np.round(off, 4), DV[:, 2].max() - DV[:, 2].min()))

# ---- distance to the base surface -----------------------------------------
dist = np.empty(len(DV), np.float32)
for i, p in enumerate(DV):
    hit = base_tree.find_nearest(Vector(p.tolist()))
    dist[i] = 1e3 if hit[0] is None else (Vector(p.tolist()) - hit[0]).length
# how well do the two builds agree where there is NO gear? the legs below the
# knee are bare in every one of these sheets
knee = blo[2] + 0.28 * BH
bare = DV[:, 2] < knee
print("agreement on the bare lower legs: median %.4f m, p90 %.4f m (%d verts)"
      % (np.median(dist[bare]), np.percentile(dist[bare], 90), int(bare.sum())))

# ---- region from the bones -------------------------------------------------
R = RADIUS[REGION]
seg = [bone_pts[b] for b in BONES[REGION] if b in bone_pts]
inreg = np.zeros(len(DV), bool)
for h, t in seg:
    ab = t - h
    L2 = float(ab @ ab) or 1e-9
    u = np.clip(((DV - h) @ ab) / L2, 0, 1)[:, None]
    proj = h + u * ab
    inreg |= np.linalg.norm(DV - proj, axis=1) < R
gear = (dist > DIST) & inreg
print("region %s: %d verts within %.2f m of its bones; %d also further than "
      "%.3f m from the body" % (REGION, int(inreg.sum()), R, int(gear.sum()), DIST))
json.dump(dict(region=REGION, dist_thr=DIST, scale=round(float(s), 6),
               offset=[round(float(v), 5) for v in off],
               bare_leg_median_m=round(float(np.median(dist[bare])), 5),
               bare_leg_p90_m=round(float(np.percentile(dist[bare], 90)), 5),
               in_region=int(inreg.sum()), gear_verts=int(gear.sum()),
               dressed_verts=int(len(DV))),
          open(REP or os.path.join(os.path.dirname(OUT), "iso_%s.json" % REGION), "w"),
          indent=1)
# ---- keep the gear, drop the rest -----------------------------------------
bm = bmesh.new(); bm.from_mesh(d.data); bm.verts.ensure_lookup_table()
kill = [v for v in bm.verts if not gear[v.index]]
bmesh.ops.delete(bm, geom=kill, context='VERTS')
bm.to_mesh(d.data); bm.free()
print("kept %d verts, %d faces" % (len(d.data.vertices), len(d.data.polygons)))
bpy.ops.object.select_all(action='DESELECT')
d.select_set(True); bpy.context.view_layer.objects.active = d
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_image_format='AUTO')
print("wrote %s (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
