# EN-E2: weight agreement of two skinned GLBs on the same skeleton (dense weight vectors, nearest vertex): 0.5 x L1 per vertex.
#   python3 scripts/en50_wt_compare.py <reference.glb> <test.glb>
import sys, os, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); L = __import__('21_lint_export')
def dense(p):
    js, b = L.load_glb(p); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
    pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]; rd = lambda i: np.asarray(L.read_accessor(js, b, i))
    P = rd(pr['attributes']['POSITION']); J = rd(pr['attributes']['JOINTS_0']).astype(int); W = rd(pr['attributes']['WEIGHTS_0'])
    n = len(js['skins'][js['nodes'][mn]['skin']]['joints']); D = np.zeros((len(P), n))
    for k in range(4): np.add.at(D, (np.arange(len(P)), J[:, k]), W[:, k])
    return P, D
P0, D0 = dense(sys.argv[1]); P1, D1 = dense(sys.argv[2]); d, i = cKDTree(P0).query(P1); x = 0.5 * np.abs(D1 - D0[i]).sum(1)
print('WT_COMPARE pos p50 %.5f max %.5f | disagreement p50 %.4f p95 %.4f p99 %.4f mean %.4f' % (np.median(d), d.max(), np.median(x), np.percentile(x, 95), np.percentile(x, 99), x.mean()))
