# EN-E2: does a clip STRETCH the skin (not just foreshorten)? For the triangles weighted to the named bones, the deformed edge lengths at each
# key against their rest lengths (linear-blend skinning of the shipped GLB at that key). Reports the worst p99 / max edge ratio and its key.
#   python3 scripts/en47_stretch.py <body.glb> <clip> <bone,bone,...>
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
C = __import__('s17_loop_closure'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
BODY, CLIP, BONES = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
js, b = L.load_glb(BODY); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]; rd = lambda i: np.asarray(L.read_accessor(js, b, i))
P = rd(pr['attributes']['POSITION']); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0']); idx = rd(pr['indices']).astype(int).reshape(-1, 3)
sk = js['skins'][js['nodes'][mn]['skin']]; joints = sk['joints']; IBM = np.array(W.mat_list(js, b, sk['inverseBindMatrices']))
names = [js['nodes'][j]['name'] for j in joints]; want = [names.index(n) for n in BONES]
w_sel = sum(np.where(np.isin(J[:, k], want), Wt[:, k], 0.0) for k in range(4)); tri = idx[(w_sel[idx] > 0.5).all(1)]
vs = np.unique(tri); m = C.model(BODY)
def skin(G):
    M = np.stack([G[j] @ IBM[k] for k, j in enumerate(joints)])            # per joint skin matrix
    Ph = np.c_[P[vs], np.ones(len(vs))]; out = np.zeros((len(vs), 3))
    for k in range(4):
        out += Wt[vs, k][:, None] * np.einsum('nij,nj->ni', M[J[vs, k]], Ph)[:, :3]
    return out
loc = {v: i for i, v in enumerate(vs)}; e = np.array([[loc[a], loc[c]] for t in tri for a, c in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0]))])
ts = sorted({float(t) for v in m['anims'][CLIP].values() for t in v[0]})
G0 = C.globals_at(m, CLIP, ts[0]); rest = None
from numpy.linalg import norm
Grest = {j: W.globals_(js)[0][j] for j in joints}; X0 = skin(Grest); l0 = norm(X0[e[:, 0]] - X0[e[:, 1]], axis=1); ok = l0 > 1e-6
worst = (0, 0, 0); meds = []
for t in ts:
    X = skin(C.globals_at(m, CLIP, t)); r = norm(X[e[:, 0]] - X[e[:, 1]], axis=1)[ok] / l0[ok]
    p99, mx = float(np.percentile(r, 99)), float(r.max()); meds.append(float(np.median(r)))
    if p99 > worst[0]: worst = (p99, mx, t)
print('STRETCH %s %s: worst p99 edge ratio %.3f (max %.3f) at t %.4f over %d edges; median ratio over keys %.3f..%.3f' % (CLIP, BONES, worst[0], worst[1], worst[2], ok.sum(), min(meds), max(meds)))
