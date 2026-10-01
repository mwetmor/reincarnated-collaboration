# Cape stride diagnosis in pure numpy (no Blender): skin the cape with the BODY's clip globals (joints matched by name),
# report edge stretch for edges >= 5 mm at rest (decimation slivers excluded), where the worst edges sit (zf, panel).
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); C = __import__('s17_loop_closure')
BODY, CAPE = sys.argv[1], sys.argv[2]; CLIPS = sys.argv[3].split(',') if len(sys.argv) > 3 else ['walk', 'run']
m = C.model(BODY); jc, bc = L.load_glb(CAPE)
mn = next(i for i, n in enumerate(jc['nodes']) if 'skin' in n and 'mesh' in n); sk = jc['skins'][0]
names = [jc['nodes'][j]['name'] for j in sk['joints']]; ibm = W.mat_list(jc, bc, sk['inverseBindMatrices'])
prims = jc['meshes'][jc['nodes'][mn]['mesh']]['primitives']
V = np.vstack([L.read_accessor(jc, bc, p['attributes']['POSITION']) for p in prims]).astype(float)
J = np.vstack([L.read_accessor(jc, bc, p['attributes']['JOINTS_0']) for p in prims]).astype(int)
Wt = np.vstack([L.read_accessor(jc, bc, p['attributes']['WEIGHTS_0']) for p in prims]).astype(float)
Wt = Wt / Wt.sum(1, keepdims=True)
F = []; off = 0
for p in prims:
    F.append(L.read_accessor(jc, bc, p['indices']).reshape(-1, 3).astype(int) + off); off += jc['accessors'][p['attributes']['POSITION']]['count']
F = np.vstack(F); E = np.unique(np.sort(np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1), axis=0)
bid = [m['nid'][n] for n in names]
def skin(G):
    out = np.zeros_like(V)
    Vh = np.c_[V, np.ones(len(V))]
    for k in range(4):
        for jj in np.unique(J[:, k]):
            s = (J[:, k] == jj) & (Wt[:, k] > 0)
            if s.any(): out[s] += (Vh[s] @ (G[bid[jj]] @ ibm[jj]).T)[:, :3] * Wt[s, k:k + 1]
    return out
Gr, _ = W.globals_(m['nodes'] and L.load_glb(BODY)[0]); P0 = skin(Gr)
L0 = np.linalg.norm(P0[E[:, 0]] - P0[E[:, 1]], axis=1); ok = L0 >= 0.005
z0 = P0[:, 1].min(); H = 1.70
for clip in CLIPS:
    ch = m['anims'][clip]; tt = sorted({float(t) for v in ch.values() for t in v[0]}); worst = (0, None)
    for t in tt:
        P = skin(C.globals_at(m, clip, t)); r = np.linalg.norm(P[E[ok, 0]] - P[E[ok, 1]], axis=1) / L0[ok]
        if r.max() > worst[0]: worst = (float(r.max()), t, r)
    r = worst[2]; top = np.argsort(r)[-10:]; Eo = E[ok][top]
    print(clip, 'max %.2f at t %.3f; p99 %.3f; edges>1.5x: %d of %d' % (worst[0], worst[1], np.percentile(r, 99), (r > 1.5).sum(), len(r)))
    for e, rr in zip(Eo, r[top]):
        a, b = P0[e[0]], P0[e[1]]; js = [names[j] for j in J[e[0]][Wt[e[0]] > 0.05]]
        print('   %.2fx zf %.2f x %+.3f L0 %.3f  joints %s' % (rr, (a[1] - z0) / H, a[0], L0[ok][top][0], js))
