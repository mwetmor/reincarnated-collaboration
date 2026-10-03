# EN-E2: GEOMETRIC canvas-fit estimate for a body GLB without rendering -- the skinned mesh (every 2nd key of every clip, 8 headings)
# projected through the JOIN-1 play camera (ortho, pitch 52.9535 deg, ppm_render 151.337, ground origin at pixel (384, 448)); the
# union per clip and the largest height factor that keeps the 5 % gate (38.4 px). Calibrated against a rendered pack's union when
# given --check <pack dir> (the rendered union vs the estimate's union for the same body). Clips to estimate: --clips a,b (default all).
#   python3 scripts/en63_fit_estimate.py <body.glb> [--clips ...] [--check <pack>]
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); C = __import__('s17_loop_closure'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
BODY = sys.argv[1]; a = sys.argv[2:]; PPM = 151.33680669505316; P = np.radians(52.9535411256029); GATE = 38.4
js, b = L.load_glb(BODY); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]; rd = lambda i: np.asarray(L.read_accessor(js, b, i))
Pv = rd(pr['attributes']['POSITION']).astype(float); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0']).astype(float)
sel = np.arange(0, len(Pv), 7); Pv, J, Wt = Pv[sel], J[sel], Wt[sel]                       # every 7th vertex: the silhouette is dense
sk = js['skins'][js['nodes'][mn]['skin']]; joints = sk['joints']; IBM = np.array(W.mat_list(js, b, sk['inverseBindMatrices']))
m = C.model(BODY); clips = a[a.index('--clips') + 1].split(',') if '--clips' in a else [c for c in m['anims'] if not c.startswith('Armature')]
def skin(G):
    M = np.stack([G[j] @ IBM[k] for k, j in enumerate(joints)]); Ph = np.c_[Pv, np.ones(len(Pv))]; out = np.zeros((len(Pv), 3))
    for k in range(4): out += Wt[:, k][:, None] * np.einsum('nij,nj->ni', M[J[:, k]], Ph)[:, :3]
    return out
res = {}; U = [0, 0, 0, 0]
for c in clips:
    ts = sorted({float(t) for v in m['anims'][c].values() for t in v[0]})[::2]; ext = [0, 0, 0, 0]   # left, up, right, down (px)
    for t in ts:
        X = skin(C.globals_at(m, c, t))
        for h in range(8):
            th = np.radians(45 * h); x = X[:, 0] * np.cos(th) - X[:, 2] * np.sin(th); z = X[:, 0] * np.sin(th) + X[:, 2] * np.cos(th)
            sx = x * PPM; sy = (X[:, 1] * np.cos(P) - z * np.sin(P)) * PPM
            ext = [max(ext[0], -sx.min()), max(ext[1], sy.max()), max(ext[2], sx.max()), max(ext[3], -sy.min())]
    allow = (384 - GATE, 448 - GATE, 384 - GATE, 320 - GATE); f = min(al / max(e, 1e-6) for al, e in zip(allow, ext))
    res[c] = dict(ext_px=[round(e, 1) for e in ext], fit=round(f, 3)); U = [max(u, e) for u, e in zip(U, ext)]
    print('FITEST %-10s left %5.0f up %5.0f right %5.0f down %5.0f  fit x%.3f' % (c, *ext, f))
allow = (384 - GATE, 448 - GATE, 384 - GATE, 320 - GATE); F = min(al / max(e, 1e-6) for al, e in zip(allow, U))
print('FITEST ALL union bbox (%.0f, %.0f, %.0f, %.0f)  fit x%.3f' % (384 - U[0], 448 - U[1], 384 + U[2], 448 + U[3], F))
if '--check' in a:
    d = json.load(open(os.path.join(a[a.index('--check') + 1], 'matrix_index.json'))); bb = [c['alpha_union_bbox'] for c in d['cells'].values()]
    print('CHECK rendered union', (min(x[0] for x in bb), min(x[1] for x in bb), max(x[2] for x in bb), max(x[3] for x in bb)))
