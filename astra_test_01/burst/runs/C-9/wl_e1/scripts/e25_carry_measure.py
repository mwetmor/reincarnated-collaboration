# CARRY MEASURES (stage G, R-C9-115 "weapon tips pointed forward"), per key of idle / walk / run (and the attack for reference):
#   tip_bearing  the haft's butt->head direction, horizontal, against his ROOT forward (+Z), degrees (0 = straight ahead)
#   elevation    the haft's angle above horizontal
#   head_y       the mace head centre's height (m, at 1.96 m)
#   helm_clear   the nearest distance from any mace vertex to any helm vertex (m)
#   pen_body     mace vertices INSIDE the body (nearest body vertex closer than 1 cm and the vertex behind its normal) as a
#                share of the mace -- a proxy (nearest-vertex, not exact triangles); and the same against the chest/pauldrons/cape
#   fists_dy     the vertical stack: |dy| / separation of the two fists (1 = stacked vertically)
#   python3 e25_carry_measure.py <body.glb> <mace.glb> <gear dir> [--json f]
import sys, os, json, math, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
BODY, MACE, GD = sys.argv[1:4]; K = 1.96 / 1.70
m = C.model(BODY); nid = m['nid']
def load(p):
    js, b = L.load_glb(p); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
    sk = js['skins'][0]; names = [js['nodes'][j]['name'] for j in sk['joints']]; ibm = W.mat_list(js, b, sk['inverseBindMatrices'])
    pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives']
    V = np.vstack([L.read_accessor(js, b, q['attributes']['POSITION']) for q in pr]).astype(float)
    J = np.vstack([L.read_accessor(js, b, q['attributes']['JOINTS_0']) for q in pr]).astype(int)
    Wt = np.vstack([L.read_accessor(js, b, q['attributes']['WEIGHTS_0']) for q in pr]).astype(float)
    Nn = np.vstack([L.read_accessor(js, b, q['attributes']['NORMAL']) for q in pr]).astype(float)
    return dict(V=V, J=J, W=Wt / Wt.sum(1, keepdims=True), N=Nn, names=names, ibm=ibm)
def pose(P, G, step=1):
    V = P['V'][::step]; J = P['J'][::step]; Wt = P['W'][::step]; Nn = P['N'][::step]
    out = np.zeros_like(V); on = np.zeros_like(V); Vh = np.c_[V, np.ones(len(V))]
    for k in range(4):
        for jj in np.unique(J[:, k]):
            s = (J[:, k] == jj) & (Wt[:, k] > 0)
            if not s.any(): continue
            M = G[nid[P['names'][jj]]] @ P['ibm'][jj]
            out[s] += (Vh[s] @ M.T)[:, :3] * Wt[s, k:k + 1]; on[s] += (Nn[s] @ M[:3, :3].T) * Wt[s, k:k + 1]
    return out * K, on / np.maximum(np.linalg.norm(on, axis=1, keepdims=True), 1e-9)
B = load(BODY); Mc = load(MACE); HELM = load(os.path.join(GD, 'wl_helm.glb'))
OTHER = [load(os.path.join(GD, 'wl_%s.glb' % p)) for p in ('chest', 'pauldrons', 'cape')]
# the haft axis in the mace's rest: PCA, head = wider end
G0, _ = W.globals_(L.load_glb(BODY)[0]); MV0, _ = pose(Mc, G0); c0 = MV0.mean(0)
_, _, vt = np.linalg.svd(MV0 - c0, full_matrices=False); ax = vt[0]; s = (MV0 - c0) @ ax
wid = lambda lo, hi: np.linalg.norm(((MV0 - c0) - np.outer(s, ax))[(s > lo) & (s < hi)], axis=1).max()
if wid(s.max() - 0.25 * np.ptp(s), s.max()) < wid(s.min(), s.min() + 0.25 * np.ptp(s)): ax = -ax; s = -s
headsel = s > s.max() - 0.30 * np.ptp(s); buttsel = s < s.min() + 0.05 * np.ptp(s)
rootn = [i for i in range(len(m['nodes'])) if m['parent'].get(i) is None and m['nodes'][i].get('name') == 'Armature'][0]
rep = {}
for clip in [c for c in ('idle', 'walk', 'run', 'attack') if c in m['anims']]:
    tt = sorted({float(t) for v in m['anims'][clip].values() for t in v[0]})
    rows = []
    for t in tt[::2]:
        G = C.globals_at(m, clip, t); Rt = np.linalg.inv(G[rootn]); Gr = {i: Rt @ G[i] * 1.0 for i in G}
        Gr = {i: (lambda M: M)(Gr[i]) for i in Gr}
        # pose everything in the ROOT frame (rig units -> metres: the root carries the 0.01 scale)
        Gm = {i: G[i] for i in G}
        MV, MN = pose(Mc, Gm); HV, _ = pose(HELM, Gm, 3); BV, BN = pose(B, Gm, 4)
        Rr = np.linalg.inv(G[rootn])[:3, :3]; Rr = Rr / np.cbrt(np.linalg.det(Rr))
        head = MV[headsel].mean(0); butt = MV[buttsel].mean(0); d = Rr @ (head - butt); d /= np.linalg.norm(d)
        bear = math.degrees(math.atan2(d[0], d[2])); elev = math.degrees(math.asin(np.clip(d[1], -1, 1)))
        hc = float(cKDTree(HV).query(MV[::5])[0].min())
        tb = cKDTree(BV); dist, idx = tb.query(MV[::3]); inside = (dist < 0.01) & (((MV[::3] - BV[idx]) * BN[idx]).sum(1) < 0)
        pen_o = 0.0
        for P in OTHER:
            OV, ON = pose(P, Gm, 3); to = cKDTree(OV); do, io = to.query(MV[::3]); pen_o = max(pen_o, float(((do < 0.01) & (((MV[::3] - OV[io]) * ON[io]).sum(1) < 0)).mean()))
        Rh = (G[nid['RightHand']])[:3, 3] * K; Lh = (G[nid['LeftHand']])[:3, 3] * K; dd = Rr @ (Rh - Lh)
        rows.append(dict(t=round(t, 4), tip_bearing=round(bear, 1), elevation=round(elev, 1), head_y=round(float(head[1] - BV[:, 1].min()), 3),
                         helm_clear=round(hc, 3), pen_body=round(float(inside.mean()), 4), pen_gear=round(pen_o, 4), fists_dy=round(float(abs(dd[1]) / max(np.linalg.norm(dd), 1e-9)), 2)))
    agg = {k: [min(r[k] for r in rows), round(float(np.median([r[k] for r in rows])), 3), max(r[k] for r in rows)] for k in rows[0] if k != 't'}
    rep[clip] = dict(min_med_max=agg, rows=rows); print(clip, json.dumps(agg))
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
