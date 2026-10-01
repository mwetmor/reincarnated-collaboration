# D2: pull a gear piece out of a DRESSED Tripo build, by SEED AND GROW.
#
#   blender -b -noaudio --python scripts/07_isolate2.py -- <dressed.glb>
#     <base.glb> <out.glb> --region head --seed "<expr>" --grow "<expr>"
#     [--yaw -90] [--minfrac 0.02]
#
# Neither signal works alone and the measurements say why:
#
#   DISTANCE from the base surface. The dressed build and the base build are
#   separate generations of the same man, and they disagree by 4.3 mm median /
#   9.2 mm p90 on bare lower legs where no gear exists. A helmet worn over
#   thick hair stands off by about that much, so the signal sits inside the
#   noise: thresholding at 4 mm keeps the whole head, at 20 mm keeps scraps of
#   helmet.
#
#   COLOUR. Steel against ginger hair is unmistakable -- the helmet dome is a
#   10.8k-vertex cluster at saturation below 0.15 sitting at 95% of height.
#   But a mail shirt's grey and the trousers' blue-grey are the same
#   saturation, and brown leather against skin is a difference of VALUE, not
#   hue. One global colour rule does not cover four pieces.
#
# So: SEED on whichever signal is unambiguous for this piece, GROW over the
# mesh graph on a looser predicate, keep the components that matter. The same
# shape that worked on the mirrored tattoo, where a colour rule alone cut the
# band in half. Predicates are given per piece because the pieces genuinely
# differ; each one is recorded in the manifest.
#
# Arrays in scope for the predicates: dist (m, to the base surface), sat, val,
# r/g/b (sRGB 0-1 -- true sRGB since the double-gamma fix; see the note at VC), z (m),
# zf (fraction of body height), inreg (bone region).
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
DRESSED, BASE, OUT = a[0], a[1], a[2]
REGION = a[a.index("--region") + 1] if "--region" in a else "head"
SEED = a[a.index("--seed") + 1]
GROW = a[a.index("--grow") + 1]
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else -90.0
MINFRAC = float(a[a.index("--minfrac") + 1]) if "--minfrac" in a else 0.02
# E1 (drax): the dressed builds wear a HORNED helm, so their bbox is taller than the base's; scaling the dressed build to the
# base's height (the barbarian's rule) would shrink him. --hratio = dressed sheet height / base sheet height (registered sheets,
# one px/m), and x/y are aligned on the LOWER LEGS (zf < 0.25) -- a long cape drags the whole-body median backwards.
HRATIO = float(a[a.index("--hratio") + 1]) if "--hratio" in a else 1.0
RADOVR = float(a[a.index("--radius") + 1]) if "--radius" in a else None
ALIGNZ = float(a[a.index("--alignz") + 1]) if "--alignz" in a else 0.25   # the cape build: feet only (its hem is in the leg band)
BONES = dict(head=["Head", "head_end", "headfront", "neck"],
             forearms=["LeftForeArm", "LeftHand", "RightForeArm", "RightHand"],
             torso=["Hips", "Spine", "Spine01", "Spine02", "LeftUpLeg", "RightUpLeg"],
             shoulders=["LeftShoulder", "RightShoulder", "Spine02", "neck",
                        "LeftArm", "RightArm"],
             # E1: the helm with its horns; the long cape (shoulders to ankles, behind); the chest plates
             helm=["Head", "head_end", "headfront", "neck"],
             cape=["Spine02", "Spine01", "Spine", "Hips", "LeftUpLeg", "RightUpLeg", "LeftLeg", "RightLeg",
                   "LeftShoulder", "RightShoulder", "neck"],
             chest=["Hips", "Spine", "Spine01", "Spine02", "neck"])
RADIUS = dict(helm=0.40, cape=0.55, chest=0.32, head=0.24, forearms=0.14, torso=0.45, shoulders=0.38)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
bmo = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
barm = next(o for o in sc.objects if o.type == 'ARMATURE')
BV, BF, off = [], [], 0
for o in bmo:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    BV.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
              + np.array(o.matrix_world.translation))
    o.data.calc_loop_triangles()
    BF.append(np.array([list(t.vertices) for t in o.data.loop_triangles]) + off)
    off += len(o.data.vertices)
BV = np.vstack(BV); BF = np.vstack(BF)
blo, bhi = BV.min(0), BV.max(0); BH = float(bhi[2] - blo[2])
bone_pts = {b.name: (np.array(barm.matrix_world @ b.head),
                     np.array(barm.matrix_world @ b.tail)) for b in barm.pose.bones}
tree = BVHTree.FromPolygons([Vector(p) for p in BV.tolist()],
                            [list(map(int, f)) for f in BF])

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
n0 = len(d.data.vertices)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=1e-5)
bpy.ops.object.mode_set(mode='OBJECT')
d.matrix_world = Matrix.Rotation(math.radians(YAW), 4, 'Z') @ d.matrix_world
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
co = np.empty(len(d.data.vertices) * 3); d.data.vertices.foreach_get("co", co)
P = co.reshape(-1, 3)
s = BH * HRATIO / float(P[:, 2].max() - P[:, 2].min())
P = P * s
P[:, 2] += blo[2] - P[:, 2].min()
_bl = BV[:, 2] < blo[2] + ALIGNZ * BH; _pl = P[:, 2] < blo[2] + ALIGNZ * BH
_mid = lambda Q: (np.percentile(Q, 2, axis=0) + np.percentile(Q, 98, axis=0)) / 2   # band CENTRE, not median: vertex density is lopsided
P += np.r_[(_mid(BV[_bl, :2]) - _mid(P[_pl, :2])), 0.0]
d.data.vertices.foreach_set("co", P.ravel()); d.data.update()
print("dressed: welded %d -> %d, scaled x%.5f" % (n0, len(P), s))

img = None
for sl in d.material_slots:
    if sl.material and sl.material.node_tree:
        for n in sl.material.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image:
                img = n.image
W, H = img.size
px = np.array(img.pixels[:], np.float32).reshape(H, W, img.channels)[..., :3]
uvl = d.data.uv_layers.active.data
UV = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
loops = np.empty(len(d.data.loops), int); d.data.loops.foreach_get("vertex_index", loops)
VC = np.zeros((len(P), 3), np.float32); cnt = np.zeros(len(P), np.float32)
np.add.at(VC, loops, px[np.clip((UV[:, 1] * H).astype(int), 0, H - 1),
                        np.clip((UV[:, 0] * W).astype(int), 0, W - 1)])
np.add.at(cnt, loops, 1)
VC = np.clip(VC / np.maximum(cnt, 1)[:, None], 0, 1)
# ONE GAMMA, NOT TWO (fixed for D7 pass 2; found on D7's robe). For an 8-bit sRGB image,
# Blender's img.pixels are ALREADY sRGB-encoded, so the unconditional `** (1 / 2.2)` this line
# used to apply encoded them a second time -- brightening and desaturating everything (D7's red
# robe: 70.5% red-ish texels at g/r 0.560 as read, 6.5% at 0.719 after the extra gamma). Only a
# FLOAT image stores linear values and wants the encode. r/g/b/sat/val are now true sRGB.
#
# D2's four predicates were fitted to the double-gamma values, so they were RE-DERIVED, exactly,
# into this space (x = x2 ** 2.2 per channel, so each threshold maps monotonically):
#   val < t   ->  val < t ** 2.2            sat < t  ->  sat < 1 - (1 - t) ** 2.2
#   b <= r + c, (r - b) < c  compare ENCODED channels and have no single-threshold form, so they
#   keep their meaning as  b**(1/2.2) <= r**(1/2.2) + c  and  (r**(1/2.2) - b**(1/2.2)) < c.
# Re-run with these on D2's own inputs, every piece came out IDENTICAL to the shipped D2 piece
# (same vertex and face counts, same vertex positions; proof in so_d7/work/nb_d2_gamma_proof.json):
#   helmet  (head)       seed (sat<0.3537650006021934)&(zf>0.905)
#                        grow ((sat<0.5145645458896095)|((val<0.4854354541103905)&(sat<0.7315904790866863)))&(zf>0.868)
#   bracers (forearms)   seed (val<0.40086363305114275)&(sat>0.4210938998435668)&(zf>0.50)&(zf<0.66)
#                        grow (val<0.6120655998656237)&(zf>0.47)&(zf<0.69)
#   byrnie  (torso)      seed (sat<0.318580701090861)&(b**(1/2.2)<=r**(1/2.2)+0.02)&(zf>0.56)&(zf<0.90)
#                        grow (sat<0.5437365416035296)&(b**(1/2.2)<=r**(1/2.2)+0.05)&(zf>0.42)&(zf<0.92)
#   mantle  (shoulders)  seed (zf>0.79)&(zf<0.92)&(ax>0.14)&(val<0.6462349993978065)&((r**(1/2.2)-b**(1/2.2))<0.30)
#                        grow (zf>0.72)&(zf<0.95)&((r**(1/2.2)-b**(1/2.2))<0.30)&~((val>0.7176234019070601)&(sat>0.4844037103512485)&(sat<0.8010560565560372))
# The ORIGINAL strings in pieces/*.json describe the runs that made those pieces, under the old
# double gamma; with this script, use the strings above.
if img.is_float:
    VC = VC ** (1 / 2.2)
r, g, b = VC[:, 0], VC[:, 1], VC[:, 2]
mx, mn = VC.max(1), VC.min(1)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
val = mx
z = P[:, 2]; zf = (z - blo[2]) / BH
dist = np.empty(len(P), np.float32)
for i, p in enumerate(P):
    hit = tree.find_nearest(Vector(p.tolist()))
    dist[i] = 1e3 if hit[0] is None else (Vector(p.tolist()) - hit[0]).length
bare = z < blo[2] + 0.28 * BH
print("noise floor on bare lower legs: median %.4f m, p90 %.4f m"
      % (np.median(dist[bare]), np.percentile(dist[bare], 90)))
inreg = np.zeros(len(P), bool)
for bn in BONES[REGION]:
    if bn not in bone_pts:
        continue
    h, t = bone_pts[bn]; ab = t - h; L2 = float(ab @ ab) or 1e-9
    u = np.clip(((P - h) @ ab) / L2, 0, 1)[:, None]
    inreg |= np.linalg.norm(P - (h + u * ab), axis=1) < (RADOVR or RADIUS[REGION])

# x and y as well: the fur mantle and the braid share a height band and are
# told apart by how far out from the midline they sit, not by colour.
x = P[:, 0] - float(np.median(BV[:, 0]))
y = P[:, 1] - float(np.median(BV[:, 1]))
env = dict(dist=dist, sat=sat, val=val, r=r, g=g, b=b, z=z, zf=zf, inreg=inreg,
           x=x, y=y, ax=np.abs(x), np=np)
seed = eval(SEED, env) & inreg
grow = eval(GROW, env) & inreg
print("region %s: %d verts; seed %d; grow-allowed %d"
      % (REGION, int(inreg.sum()), int(seed.sum()), int(grow.sum())))
assert seed.sum() > 200, "seed too small (%d) -- the predicate does not fire" % seed.sum()

edges = np.empty(len(d.data.edges) * 2, int)
d.data.edges.foreach_get("vertices", edges); edges = edges.reshape(-1, 2)
adj = [[] for _ in range(len(P))]
for u_, v_ in edges:
    adj[u_].append(v_); adj[v_].append(u_)
keep = seed.copy()
stack = list(np.where(seed)[0])
while stack:
    i = stack.pop()
    for j in adj[i]:
        if not keep[j] and grow[j]:
            keep[j] = True; stack.append(j)
print("grown to %d verts" % int(keep.sum()))
lab = -np.ones(len(P), int); nc = 0
for i in np.where(keep)[0]:
    if lab[i] >= 0:
        continue
    st = [i]; lab[i] = nc
    while st:
        k = st.pop()
        for j in adj[k]:
            if keep[j] and lab[j] < 0:
                lab[j] = nc; st.append(j)
    nc += 1
sizes = np.bincount(lab[keep])
big = [i for i in range(nc) if sizes[i] >= MINFRAC * keep.sum()]
final = keep & np.isin(lab, big)
print("%d components, keeping %d of them (>= %.0f%% each): %d verts"
      % (nc, len(big), 100 * MINFRAC, int(final.sum())))
bm = bmesh.new(); bm.from_mesh(d.data); bm.verts.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not final[v.index]], context='VERTS')
bm.to_mesh(d.data); bm.free()
print("kept %d verts, %d faces" % (len(d.data.vertices), len(d.data.polygons)))
bpy.ops.object.select_all(action='DESELECT')
d.select_set(True); bpy.context.view_layer.objects.active = d
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_image_format='AUTO')
json.dump(dict(region=REGION, seed=SEED, grow=GROW, components=nc, kept=len(big),
               verts=len(d.data.vertices), faces=len(d.data.polygons),
               noise_floor_median_m=round(float(np.median(dist[bare])), 5),
               noise_floor_p90_m=round(float(np.percentile(dist[bare], 90)), 5)),
          open(OUT.replace(".glb", ".json"), "w"), indent=1)
print("wrote %s (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
