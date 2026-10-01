# R-C9-98 stage 2, step 1 of the isolation: FIT the dressed Tripo build onto her shipped body and DUMP per-vertex
# features, so pieces can be classified in numpy (fast, iterable) instead of one Blender run per predicate (07_isolate2).
#
#   blender -b -noaudio --python s21_features.py -- <dressed.glb> <base_body.glb> <out_prefix> [--yaw -90]
#
# THE FIT. 07_isolate2 scales the dressed build to the base's full height. That is wrong for this set: the HOOD rises
# above her crown (sheet: ~10 px of 736 in the front view), so a height fit would shrink her ~1.4%. Instead: the
# 07 placement first, then a SCALE SEARCH about the soles (0.88-1.04) and an x/y re-centre, minimising the median
# distance of ANCHOR vertices to the base surface -- the parts this set does not cover: the BOOT FEET (zf < 0.07) and
# the FACE skin (skin-coloured, zf > 0.84, in front of the head). Both are unchanged by the edit, so they must coincide.
#
# Writes <prefix>_dressed_fit.glb (the welded, fitted build, UVs and texture kept) and <prefix>_feat.npz:
#   P (n,3) fitted positions, VC (n,3) sRGB colour, dist (n,) to the base surface, side (n,) +1 outside / -1 inside,
#   bone (n,) the dominant deform bone of the NEAREST base vertex (index into bones), bones, zf, edges (m,2), fit report.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
DRESSED, BASE, PRE = a[0], a[1], a[2]
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else -90.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
barm = next(o for o in sc.objects if o.type == 'ARMATURE')
if barm.animation_data:
    barm.animation_data.action = None
for pb in barm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
bmo = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
BV, BF, BB, off = [], [], [], 0
for o in bmo:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    BV.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T + np.array(o.matrix_world.translation))
    o.data.calc_loop_triangles()
    BF.append(np.array([list(t.vertices) for t in o.data.loop_triangles]) + off)
    gn = {g.index: g.name for g in o.vertex_groups}
    dom = []
    for v in o.data.vertices:
        gs = sorted(((g.weight, gn[g.group]) for g in v.groups), reverse=True)
        dom.append(gs[0][1] if gs else "")
    BB += dom
    off += len(o.data.vertices)
BV = np.vstack(BV); BF = np.vstack(BF)
bones = sorted(set(BB)); bidx = {b: i for i, b in enumerate(bones)}
BBi = np.array([bidx[b] for b in BB])
blo, bhi = BV.min(0), BV.max(0); BH = float(bhi[2] - blo[2])
tree = BVHTree.FromPolygons([Vector(p) for p in BV.tolist()], [list(map(int, f)) for f in BF])
print("base: %d verts, height %.4f m, %d deform bones" % (len(BV), BH, len(bones)))

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
P0 = co.reshape(-1, 3)
s0 = BH / float(P0[:, 2].max() - P0[:, 2].min())

# colour per vertex (07_isolate2's sampling, with its gamma fix)
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
VC = np.zeros((len(P0), 3), np.float32); cnt = np.zeros(len(P0), np.float32)
np.add.at(VC, loops, px[np.clip((UV[:, 1] * H).astype(int), 0, H - 1), np.clip((UV[:, 0] * W).astype(int), 0, W - 1)])
np.add.at(cnt, loops, 1)
VC = np.clip(VC / np.maximum(cnt, 1)[:, None], 0, 1)
if img.is_float:
    VC = VC ** (1 / 2.2)
r, g, b = VC[:, 0], VC[:, 1], VC[:, 2]
mx, mn = VC.max(1), VC.min(1)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
gr = np.where(r > 1e-6, g / np.maximum(r, 1e-6), 9.0)


def place(s, dx=0.0, dy=0.0):
    P = P0 * s
    P = P + np.array([np.median(BV[:, 0]) - np.median(P[:, 0]) + dx, np.median(BV[:, 1]) - np.median(P[:, 1]) + dy,
                      blo[2] - P[:, 2].min()])
    return P


def nearest(P, idx):
    out = np.empty(len(idx), np.float32)
    for k, i in enumerate(idx):
        h = tree.find_nearest(Vector(P[i].tolist()))
        out[k] = 1e3 if h[0] is None else (Vector(P[i].tolist()) - h[0]).length
    return out


Pi = place(s0)
zf0 = (Pi[:, 2] - blo[2]) / BH
skin = (sat > 0.18) & (sat < 0.60) & (gr > 0.55) & (gr < 0.86) & (mx > 0.45) & (zf0 > 0.84)
boot = zf0 < 0.07
rng = np.random.default_rng(0)
anc = np.r_[rng.choice(np.where(boot)[0], min(3000, boot.sum()), replace=False),
            rng.choice(np.where(skin)[0], min(3000, skin.sum()), replace=False) if skin.sum() else np.array([], int)]
print("anchors: %d boot, %d face-skin (of %d / %d)" % (min(3000, boot.sum()), min(3000, skin.sum()), boot.sum(), skin.sum()))
best = None
nb_ = min(3000, int(boot.sum()))
prof = []
for f in np.linspace(0.88, 1.04, 33):
    P = place(s0 * f)
    dd = nearest(P, anc)
    m = float(np.median(dd))
    prof.append((round(float(f), 3), round(float(np.median(dd[:nb_])), 4), round(float(np.median(dd[nb_:])), 4) if len(dd) > nb_ else None, round(m, 4)))
    if best is None or m < best[0]:
        best = (m, f)
print("SCALE PROFILE (f, boot median, face median, all):")
for row in prof: print("   ", row)
f = best[1]
if "--scale" in a:
    # R-C9-98 shood: boots alone want 0.94, face alone 1.01 -- this generation's proportions differ from the base, so no
    # single scale fits both. The face governs (the hood and coif must hug it); the legs' ~1 cm residual is the class of
    # build-to-build noise (D2: 4.3 mm median / 9.2 mm p90) that clear_body's push-off absorbs.
    f = float(a[a.index("--scale") + 1])
    best = (float(np.median(nearest(place(s0 * f), anc))), f)
    print("SCALE OVERRIDE f=%.4f (anchor median %.4f m)" % (f, best[0]))
# x/y re-centre at that scale (+-4 cm)
best2 = (best[0], 0.0, 0.0)
for dx in np.linspace(-0.04, 0.04, 17):
    for dy in np.linspace(-0.04, 0.04, 17):
        m = float(np.median(nearest(place(s0 * f, dx, dy), anc)))
        if m < best2[0]:
            best2 = (m, dx, dy)
P = place(s0 * f, best2[1], best2[2])
fit = dict(profile=prof, height_scale=s0, scale_factor_vs_height_fit=round(float(f), 4), dx=best2[1], dy=best2[2],
           anchor_median_m_height_fit=round(float(np.median(nearest(place(s0), anc))), 5),
           anchor_median_m_final=round(best2[0], 5), anchors=int(len(anc)))
print("FIT", fit)
d.data.vertices.foreach_set("co", P.ravel()); d.data.update()

dist = np.empty(len(P), np.float32); side = np.empty(len(P), np.int8); nb = np.empty(len(P), np.int32)
BFl = BF.tolist()
for i, p in enumerate(P):
    v = Vector(p.tolist())
    h = tree.find_nearest(v)
    if h[0] is None:
        dist[i] = 1e3; side[i] = 1; nb[i] = 0
        continue
    dist[i] = (v - h[0]).length
    side[i] = 1 if (v - h[0]).dot(h[1]) >= 0 else -1
    tri = BFl[h[2]]
    nb[i] = BBi[min(tri, key=lambda j: (Vector(BV[j].tolist()) - h[0]).length)]
edges = np.empty(len(d.data.edges) * 2, int); d.data.edges.foreach_get("vertices", edges)
np.savez_compressed(PRE + "_feat.npz", P=P, VC=VC, dist=dist, side=side, bone=nb, bones=np.array(bones),
                    zf=(P[:, 2] - blo[2]) / BH, edges=edges.reshape(-1, 2), base_lo=blo, base_hi=bhi,
                    base_mid=np.median(BV, axis=0))
json.dump(dict(fit=fit, verts_welded=[n0, len(P)], base_height_m=BH), open(PRE + "_fit.json", "w"), indent=1)
bpy.ops.object.select_all(action='DESELECT'); d.select_set(True); bpy.context.view_layer.objects.active = d
bpy.ops.export_scene.gltf(filepath=PRE + "_dressed_fit.glb", export_format='GLB', use_selection=True, export_image_format='AUTO')
print("wrote %s_feat.npz and %s_dressed_fit.glb (%d verts)" % (PRE, PRE, len(P)))
