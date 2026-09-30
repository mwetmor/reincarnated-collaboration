# D2: does COLOUR separate a gear piece from the body under it?
#
#   blender -b -noaudio --python scripts/06_colour_probe.py -- <dressed.glb>
#          <base.glb> --region head
#
# Distance from the base surface does not: the two builds are separate
# generations and disagree by 4.3 mm median on bare skin, while a helmet worn
# over thick hair stands off by about the same amount. The signal sits inside
# the noise. Steel and ginger hair, on the other hand, are nowhere near each
# other, and the paint is the whole point of these sheets.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
DRESSED, BASE = a[0], a[1]
REGION = a[a.index("--region") + 1] if "--region" in a else "head"
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else -90.0
BONES = dict(head=["Head", "head_end", "headfront", "neck"],
             forearms=["LeftForeArm", "LeftHand", "RightForeArm", "RightHand"],
             torso=["Hips", "Spine", "Spine01", "Spine02", "LeftUpLeg", "RightUpLeg"],
             shoulders=["LeftShoulder", "RightShoulder", "Spine02", "neck",
                        "LeftArm", "RightArm"])
RADIUS = dict(head=0.22, forearms=0.16, torso=0.42, shoulders=0.34)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
bm_ = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
barm = next(o for o in sc.objects if o.type == 'ARMATURE')
BV = []
for o in bm_:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    BV.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
              + np.array(o.matrix_world.translation))
BV = np.vstack(BV); blo, bhi = BV.min(0), BV.max(0); BH = float(bhi[2] - blo[2])
bone_pts = {b.name: (np.array(barm.matrix_world @ b.head),
                     np.array(barm.matrix_world @ b.tail)) for b in barm.pose.bones}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=DRESSED)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
if len(objs) > 1:
    bpy.ops.object.join()
d = bpy.context.view_layer.objects.active
d.matrix_world = Matrix.Rotation(math.radians(YAW), 4, 'Z') @ d.matrix_world
bpy.context.view_layer.update()
co = np.empty(len(d.data.vertices) * 3); d.data.vertices.foreach_get("co", co)
DV = co.reshape(-1, 3) @ np.array(d.matrix_world.to_3x3()).T + np.array(d.matrix_world.translation)
s = BH / float(DV[:, 2].max() - DV[:, 2].min())
DV = DV * s
DV += np.array([np.median(BV[:, 0]) - np.median(DV[:, 0]),
                np.median(BV[:, 1]) - np.median(DV[:, 1]), blo[2] - DV[:, 2].min()])

# per-vertex colour, sampled from the build's own texture through its UVs
img = None
for sl in d.material_slots:
    if sl.material and sl.material.node_tree:
        for n in sl.material.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image:
                img = n.image
assert img, "no texture"
W, H = img.size
px = np.array(img.pixels[:], np.float32).reshape(H, W, img.channels)[..., :3]
uvl = d.data.uv_layers.active.data
UV = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
loops = np.empty(len(d.data.loops), int); d.data.loops.foreach_get("vertex_index", loops)
VC = np.zeros((len(DV), 3), np.float32); cnt = np.zeros(len(DV), np.float32)
ix = np.clip((UV[:, 0] * W).astype(int), 0, W - 1)
iy = np.clip((UV[:, 1] * H).astype(int), 0, H - 1)
np.add.at(VC, loops, px[iy, ix]); np.add.at(cnt, loops, 1)
VC /= np.maximum(cnt, 1)[:, None]
VC = np.clip(VC, 0, 1) ** (1 / 2.2)          # the image is linear; compare in sRGB

R = RADIUS[REGION]
inreg = np.zeros(len(DV), bool)
for b in BONES[REGION]:
    if b not in bone_pts:
        continue
    h, t = bone_pts[b]; ab = t - h; L2 = float(ab @ ab) or 1e-9
    u = np.clip(((DV - h) @ ab) / L2, 0, 1)[:, None]
    inreg |= np.linalg.norm(DV - (h + u * ab), axis=1) < R
mx = VC.max(1); mn = VC.min(1)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
print("region %s: %d verts" % (REGION, int(inreg.sum())))
for name, sel in (("all in region", inreg),
                  ("top 12%% of head height", inreg & (DV[:, 2] > blo[2] + 0.88 * BH))):
    if not sel.any():
        continue
    print("  %-24s sat  p10 %.3f p50 %.3f p90 %.3f | val p10 %.3f p50 %.3f p90 %.3f"
          % (name, *np.percentile(sat[sel], [10, 50, 90]),
             *np.percentile(mx[sel], [10, 50, 90])))
for lo, hi in ((0.0, 0.15), (0.15, 0.30), (0.30, 0.45), (0.45, 0.60), (0.60, 1.01)):
    sel = inreg & (sat >= lo) & (sat < hi)
    if sel.sum() < 50:
        continue
    print("    sat %.2f-%.2f : %7d verts, mean rgb %s, mean z %.3f (%.0f%% of height)"
          % (lo, hi, int(sel.sum()), np.round(VC[sel].mean(0), 3),
             DV[sel, 2].mean(), 100 * (DV[sel, 2].mean() - blo[2]) / BH))
