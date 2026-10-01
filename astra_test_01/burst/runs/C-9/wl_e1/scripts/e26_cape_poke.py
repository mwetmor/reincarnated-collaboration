# Cape POKE + STRETCH in numpy (e15's definitions, no Blender): leg vertices (dominant weight UpLeg/Leg/Foot/Toe, > 0.5) whose
# nearest cape vertex is within 10 cm, inside the cape's x/y footprint, and which sit on the cape's OUTER side (along the cape
# normal) by > 5 mm -- as a share of the leg vertices; per clip: max over keys, mean. Stretch: edges >= 5 mm at rest.
#   python3 e26_cape_poke.py <body.glb> <cape.glb> [clips] [--json f]
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = [x for x in sys.argv[1:] if not x.startswith('--')]; BODY, CAPE = a[0], a[1]
CLIPS = a[2].split(',') if len(a) > 2 and not a[2].endswith('.json') else ['walk', 'run', 'attack', 'death']
m = C.model(BODY); nid = m['nid']
def load(p):
    js, b = L.load_glb(p); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
    sk = js['skins'][0]; names = [js['nodes'][j]['name'] for j in sk['joints']]; ibm = W.mat_list(js, b, sk['inverseBindMatrices'])
    pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives']; off = 0; F = []
    for q in pr:
        F.append(L.read_accessor(js, b, q['indices']).reshape(-1, 3).astype(int) + off); off += js['accessors'][q['attributes']['POSITION']]['count']
    g = lambda k: np.vstack([L.read_accessor(js, b, q['attributes'][k]) for q in pr]).astype(float)
    Wt = g('WEIGHTS_0'); return dict(V=g('POSITION'), N=g('NORMAL'), J=g('JOINTS_0').astype(int), W=Wt / Wt.sum(1, keepdims=True), F=np.vstack(F), names=names, ibm=ibm)
def pose(P, G):
    V, N, J, Wt = P['V'], P['N'], P['J'], P['W']; out = np.zeros_like(V); on = np.zeros_like(V); Vh = np.c_[V, np.ones(len(V))]
    for k in range(4):
        for jj in np.unique(J[:, k]):
            s = (J[:, k] == jj) & (Wt[:, k] > 0)
            if s.any():
                M = G[nid[P['names'][jj]]] @ P['ibm'][jj]; out[s] += (Vh[s] @ M.T)[:, :3] * Wt[s, k:k + 1]; on[s] += (N[s] @ M[:3, :3].T) * Wt[s, k:k + 1]
    return out, on / np.maximum(np.linalg.norm(on, axis=1, keepdims=True), 1e-9)
B = load(BODY); CP = load(CAPE)
dom = np.array([B['names'][B['J'][i][np.argmax(B['W'][i])]] for i in range(len(B['V']))]); wmax = B['W'].max(1)
legs = np.where(np.char.find(dom.astype(str), 'Leg') >= 0, True, False) | np.isin(dom, ['LeftFoot', 'RightFoot', 'LeftToeBase', 'RightToeBase'])
legs = np.where(legs & (wmax > 0.5))[0][::2]; BL = dict(B, V=B['V'][legs], N=B['N'][legs], J=B['J'][legs], W=B['W'][legs])
E = np.unique(np.sort(np.vstack([CP['F'][:, [0, 1]], CP['F'][:, [1, 2]], CP['F'][:, [2, 0]]]), axis=1), axis=0)
G0, _ = W.globals_(L.load_glb(BODY)[0]); C0, _ = pose(CP, G0); unit = 0.01 if np.ptp(C0[:, 1]) > 10 else 1.0
L0 = np.linalg.norm(C0[E[:, 0]] - C0[E[:, 1]], axis=1) * unit; ok = L0 >= 0.005
rep = {}
def frame(G):
    CV, CN = pose(CP, G); LV, _ = pose(BL, G); CV *= unit; LV *= unit
    lo, hi = CV.min(0), CV.max(0); fp = (LV[:, 0] > lo[0]) & (LV[:, 0] < hi[0]) & (LV[:, 1] > lo[1]) & (LV[:, 1] < hi[1])
    d, i = cKDTree(CV).query(LV); out = fp & (d < 0.10) & (((LV - CV[i]) * CN[i]).sum(1) > 0.005)
    r = np.linalg.norm(CV[E[ok, 0]] - CV[E[ok, 1]], axis=1) / L0[ok]
    return float(out.mean()), float(r.max()), float(np.percentile(r, 99))
rest = frame(G0); rep['__rest__'] = dict(poke=round(rest[0], 4)); print('rest poke %.4f' % rest[0])
for clip in CLIPS:
    tt = sorted({float(t) for v in m['anims'][clip].values() for t in v[0]}); vals = [frame(C.globals_at(m, clip, t)) for t in tt]
    pk = [v[0] for v in vals]; rep[clip] = dict(keys=len(tt), poke_max=round(max(pk), 4), poke_mean=round(float(np.mean(pk)), 4),
                                               stretch_max=round(max(v[1] for v in vals), 3), stretch_p99=round(max(v[2] for v in vals), 3))
    print(clip, rep[clip])
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
