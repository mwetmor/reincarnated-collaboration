# EN-E2: is an arm THINNING (a skinning collapse) or only foreshortened? For the vertices weighted > 0.6 to <bone>, their mean distance from the
# bone's axis (bone origin -> child origin) at each key of <clip>, against the same at rest (linear-blend skinning of the shipped GLB).
# Also the axis LENGTH (a stretch of the bone itself would show here; Mixamo grafts rotate only).
#   python3 scripts/en48_arm_girth.py <body.glb> <clip> <bone> <child>
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
C = __import__('s17_loop_closure'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
BODY, CLIP, BONE, CHILD = sys.argv[1:5]
js, b = L.load_glb(BODY); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]; rd = lambda i: np.asarray(L.read_accessor(js, b, i))
P = rd(pr['attributes']['POSITION']); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0'])
sk = js['skins'][js['nodes'][mn]['skin']]; joints = sk['joints']; IBM = np.array(W.mat_list(js, b, sk['inverseBindMatrices']))
names = [js['nodes'][j]['name'] for j in joints]; bi = names.index(BONE)
wb = sum(np.where(J[:, k] == bi, Wt[:, k], 0.0) for k in range(4)); vs = np.nonzero(wb > 0.6)[0]
def skin(G):
    M = np.stack([G[j] @ IBM[k] for k, j in enumerate(joints)]); Ph = np.c_[P[vs], np.ones(len(vs))]; out = np.zeros((len(vs), 3))
    for k in range(4): out += Wt[vs, k][:, None] * np.einsum('nij,nj->ni', M[J[vs, k]], Ph)[:, :3]
    return out
def girth(G):
    X = skin(G); a, c = G[joints[bi]][:3, 3], G[joints[names.index(CHILD)]][:3, 3]; u = (c - a) / np.linalg.norm(c - a)
    d = X - a; return float(np.mean(np.linalg.norm(d - np.outer(d @ u, u), axis=1))), float(np.linalg.norm(c - a))
G0 = W.globals_(js)[0]; g0, l0 = girth({j: G0[j] for j in joints})
m = C.model(BODY); ts = sorted({float(t) for v in m['anims'][CLIP].values() for t in v[0]})
rows = [(t,) + girth(C.globals_at(m, CLIP, t)) for t in ts]; mn_ = min(rows, key=lambda r: r[1])
print('GIRTH %s %s (%d verts): rest %.4f m, axis %.4f | min over the clip %.4f (x%.2f) at t %.4f, axis %.4f' % (CLIP, BONE, len(vs), g0, l0, mn_[1], mn_[1] / g0, mn_[0], mn_[2]))
