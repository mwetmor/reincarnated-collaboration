# E1b R-C9-141 -- THE HELM-CROWN NOTCH. Cause (measured, e58 raster): the BODY mesh's own head (char1, Meshy's helmeted head,
# dark brown) PIERCES the helm piece's crown shell by up to ~15 mm in a crescent across the front of the dome just above the
# brow (plus thin bands down both sides). From the 52.95-deg play camera that dark crescent sits above the real visor and reads
# as a second eye slit. Fix = TUCK THE BODY'S CROWN UNDER THE HELM: every body vertex above --ymin whose ray from the head
# centre C meets the helm shell within --win m is pulled in along that ray to sit >= --margin m under the shell. The delta is
# then relaxed over the moved region's 1-ring (inward only) so the tucked layer has no crease. Only POSITION changes (the
# vertex count, order, UVs, normals, skin weights, clips and texture are byte-identical); positions are written back through
# each vertex's own rest skin matrix. The helm, its emission (eye slit) and the eye sockets are not touched.
#   python3 e59_crown_tuck.py <body.glb> <helm.glb> <out_body.glb> [--margin 0.004] [--ymin 1.80] [--win 0.03] [--json out.json]
import sys, os, json, struct, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R = __import__('49_recentre')
a = sys.argv[1:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
BODY, HELM, OUT = a[:3]; MARGIN = float(opt('--margin', '0.004')); YMIN = float(opt('--ymin', '1.80')); WIN = float(opt('--win', '0.03'))
C = np.array([float(x) for x in opt('--centre', '0,1.83,-0.04').split(',')])
def skinned(path):
    js, b = L.load_glb(path); G, _ = W.globals_(js); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
    return js, bytearray(b), G, mn, W.skin_rest(js, b, mn, G)
jb, bb, Gb, mb, Vb = skinned(BODY); jh, bh, Gh, mh, Vh = skinned(HELM)
prb = jb['meshes'][jb['nodes'][mb]['mesh']]['primitives'][0]; Ib = L.read_accessor(jb, bb, prb['indices']).reshape(-1, 3).astype(int)
prh = jh['meshes'][jh['nodes'][mh]['mesh']]['primitives'][0]; Ih = L.read_accessor(jh, bh, prh['indices']).reshape(-1, 3).astype(int)
T0, T1, T2 = Vh[Ih[:, 0]], Vh[Ih[:, 1]], Vh[Ih[:, 2]]; E1, E2 = T1 - T0, T2 - T0
def hits(d):                                   # all ray-triangle t's for unit rays d (k,3) from C (Moller-Trumbore)
    p = np.cross(d[:, None, :], E2[None]); det = (E1[None] * p).sum(-1); ok = np.abs(det) > 1e-12; inv = np.where(ok, 1 / np.where(ok, det, 1), 0)
    s = C - T0; u = (s[None] * p).sum(-1) * inv; q = np.cross(s, E1); v = (d[:, None, :] * q[None]).sum(-1) * inv
    t = (E2[None] * q[None]).sum(-1) * inv; m = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)
    return np.where(m, t, np.nan)
cand = np.where(Vb[:, 1] > YMIN)[0]
D = Vb[cand] - C; r = np.linalg.norm(D, axis=1); d = D / r[:, None]
tgt = np.full(len(cand), np.nan); poke0 = np.full(len(cand), np.nan)
for s in range(0, len(cand), 64):
    T = hits(d[s:s + 64]); rr = r[s:s + 64, None]
    dist = np.where(np.isnan(T), np.inf, np.abs(T - rr)); k = dist.argmin(1); best = T[np.arange(len(k)), k]
    good = np.isfinite(dist[np.arange(len(k)), k]) & (dist[np.arange(len(k)), k] < WIN)
    tgt[s:s + 64] = np.where(good, best, np.nan); poke0[s:s + 64] = np.where(good, rr[:, 0] - (best - MARGIN), np.nan)
under = ~np.isnan(tgt)                          # body verts that have the helm shell over them
move = under & (poke0 > 0)
delta = np.zeros(len(Vb)); idx_c = {v: i for i, v in enumerate(cand)}
delta[cand[move]] = poke0[move]                 # inward distance along the ray, metres
# relax: 1-ring max-blend over UNDER-the-helm verts only, 3 passes (inward only; never moves a vert not covered by the helm)
cov = np.zeros(len(Vb), bool); cov[cand[under]] = True
nb = {}
for f in Ib:
    if cov[f].any():
        for i in f:
            nb.setdefault(i, set()).update(f)
for _ in range(3):
    nd = delta.copy()
    for i, ns in nb.items():
        if not cov[i]: continue
        ns = [j for j in ns if cov[j]]; m_ = np.mean(delta[ns]) if ns else 0.0
        nd[i] = max(delta[i], 0.5 * m_)
    delta = nd
sel = np.where(delta > 1e-6)[0]
dirs = np.zeros((len(Vb), 3)); dirs[cand] = d
newV = Vb.copy(); newV[sel] -= dirs[sel] * delta[sel, None]
# back to mesh-local through each vertex's own rest skin matrix
sk = jb['skins'][jb['nodes'][mb]['skin']]; ibm = W.mat_list(jb, bb, sk['inverseBindMatrices'])
J = L.read_accessor(jb, bb, prb['attributes']['JOINTS_0']).astype(int); Wt = L.read_accessor(jb, bb, prb['attributes']['WEIGHTS_0']).astype(np.float64)
P = L.read_accessor(jb, bb, prb['attributes']['POSITION']).astype(np.float64)
names = [jb['nodes'][j]['name'] for j in sk['joints']]
for i in sel:
    M = sum(Wt[i, k] * (Gb[sk['joints'][J[i, k]]] @ ibm[J[i, k]]) for k in range(4) if Wt[i, k] > 0)
    P[i] = (np.linalg.inv(M) @ np.append(newV[i], 1.0))[:3]
acc = jb['accessors'][prb['attributes']['POSITION']]; bv = jb['bufferViews'][acc['bufferView']]
base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0); stride = bv.get('byteStride') or 12
assert acc['componentType'] == 5126
for i in sel: struct.pack_into('<3f', bb, base + i * stride, *P[i])
acc['min'] = P.min(0).astype(np.float32).tolist(); acc['max'] = P.max(0).astype(np.float32).tolist()
R.write_glb(OUT, jb, bb)
# verification on the written file
js2, b2 = L.load_glb(OUT); G2, _ = W.globals_(js2); V2 = W.skin_rest(js2, b2, mb, G2)
dom = J[sel, :][np.arange(len(sel)), Wt[sel].argmax(1)]; dn = {}
for x in dom: dn[names[x]] = dn.get(names[x], 0) + 1
headw = float(np.mean([sum(Wt[i, k] for k in range(4) if names[J[i, k]] == 'Head') for i in sel])) if len(sel) else None
rep = dict(body=BODY, helm=HELM, out=OUT, margin_m=MARGIN, ymin_m=YMIN, centre=C.tolist(), candidates=int(len(cand)), under_helm=int(under.sum()),
           piercing_before=int(move.sum()), pierce_max_mm=round(float(np.nanmax(poke0[move]) * 1000 + MARGIN * 1000), 2) if move.any() else 0.0,
           moved=int(len(sel)), delta_max_mm=round(float(delta.max() * 1000), 2), delta_p50_mm=round(float(np.median(delta[sel]) * 1000), 2) if len(sel) else 0,
           moved_dominant_bones=dn, moved_mean_head_weight=round(headw, 4) if headw is not None else None,
           rest_err_max_mm=round(float(np.abs(V2[sel] - newV[sel]).max() * 1000), 4) if len(sel) else 0,
           unmoved_err_max_mm=round(float(np.abs(np.delete(V2, sel, 0) - np.delete(Vb, sel, 0)).max() * 1000), 4),
           crown_before_m=round(float(Vb[:, 1].max()), 5), crown_after_m=round(float(V2[:, 1].max()), 5),
           moved_y_range_m=[round(float(Vb[sel, 1].min()), 4), round(float(Vb[sel, 1].max()), 4)] if len(sel) else None)
print(json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
