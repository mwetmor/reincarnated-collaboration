# EN-E2: WHERE does a skinned body tear? Triangles whose longest-edge ratio (pose / rest) exceeds a threshold at a clip time:
# their count, the dominant bones of their vertices and the rest-pose box. (en47 gives the distribution; this gives the place.)
#   python3 scripts/en54_stretch_loc.py <body.glb> <clip@t>[,<clip@t>...] [--thr 4]
import sys, os, numpy as np
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
C = __import__('s17_loop_closure'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
BODY = sys.argv[1]; SH = [(s.split('@')[0], float(s.split('@')[1])) for s in sys.argv[2].split(',')]
THR = float(sys.argv[sys.argv.index('--thr') + 1]) if '--thr' in sys.argv else 4.0
js, b = L.load_glb(BODY); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]; rd = lambda i: np.asarray(L.read_accessor(js, b, i))
P = rd(pr['attributes']['POSITION']).astype(float); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0']).astype(float)
I = rd(pr['indices']).astype(np.int64).reshape(-1, 3)
sk = js['skins'][js['nodes'][mn]['skin']]; joints = sk['joints']; IBM = np.array(W.mat_list(js, b, sk['inverseBindMatrices'])); names = [js['nodes'][j]['name'] for j in joints]
def skin(G):
    M = np.stack([G[j] @ IBM[k] for k, j in enumerate(joints)]); Ph = np.c_[P, np.ones(len(P))]; out = np.zeros((len(P), 3))
    for k in range(4): out += Wt[:, k][:, None] * np.einsum('nij,nj->ni', M[J[:, k]], Ph)[:, :3]
    return out
G0 = W.globals_(js)[0]; X0 = skin({j: G0[j] for j in joints}); m = C.model(BODY)
def edges(X): return np.stack([np.linalg.norm(X[I[:, a]] - X[I[:, c]], axis=1) for a, c in ((0, 1), (1, 2), (2, 0))], 1)
e0 = edges(X0)
for clip, t in SH:
    r = (edges(skin(C.globals_at(m, clip, t))) / np.maximum(e0, 1e-6)).max(1); bad = np.unique(I[r > THR].ravel())
    print('STRETCH %s@%.4f: %d tris > x%.0f, %d verts' % (clip, t, (r > THR).sum(), THR, len(bad)))
    if len(bad):
        print('  dominant bones', Counter(names[J[v, np.argmax(Wt[v])]] for v in bad).most_common(8))
        print('  rest box (m) min', X0[bad].min(0).round(2), 'max', X0[bad].max(0).round(2))
# --clusters: the torn triangles grouped by shared vertices; per cluster the POSED extent (a stretched strap reads as a long bar)
if '--clusters' in sys.argv:
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    for clip, t in SH:
        X = skin(C.globals_at(m, clip, t)); r = (edges(X) / np.maximum(e0, 1e-6)).max(1); T = I[r > THR]
        if not len(T): continue
        a = np.r_[T[:, 0], T[:, 1], T[:, 2]]; c = np.r_[T[:, 1], T[:, 2], T[:, 0]]
        G = coo_matrix((np.ones(len(a)), (a, c)), shape=(len(P), len(P))); n, lab = connected_components(G, directed=False)
        vs = np.unique(T.ravel()); out = []
        for l in np.unique(lab[vs]):
            v = vs[lab[vs] == l]; ext = np.ptp(X[v], 0).max(); out.append((ext, len(v), l, v))
        out.sort(key=lambda x: -x[0])
        for ext, nv, l, v in out[:5]:
            print('  CLUSTER %s@%.3f: posed extent %.2f m (rest %.2f m), %d verts, bones %s, rest centre %s' % (clip, t, ext, np.ptp(X0[v], 0).max(), nv,
                  Counter(names[J[q, np.argmax(Wt[q])]] for q in v).most_common(3), X0[v].mean(0).round(2)))
