# CAPE MEASURES ON THE SIMULATED CAPE: the chain cape (its cape_* bones) skinned per film frame with the BODY's clip pose (from the
# glTF, at the dump's clip + clip time) and the CAPE BONES' simulated poses (Godot's dump, skeleton space -> the glTF model space by
# the Armature node's transform). Then e37's back-gap (back panel top third: median / p90) and e26's leg poke (share of leg vertices
# outside the cape) per clip, max and mean. The RIGID comparison: the same with the cape bones at their rest under the animated chest.
#   python3 e51_cape_sim_measure.py <body.glb> <chain cape.glb> <chest.glb> <dump.json> [--rigid] [--json f]
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = [x for x in sys.argv[1:] if not x.startswith('--')]; BODY, CAPE, CHEST, DUMP = a[:4]; RIGID = '--rigid' in sys.argv
src = open(os.path.join(HERE, 'e26_cape_poke.py')).read(); exec(src[src.index('def load('):src.index('B = load(BODY)')])
m = C.model(BODY); nid = m['nid']
B = load(BODY); CP = load(CAPE); CH = load(CHEST)
jc, bc = L.load_glb(CAPE); Gc0, _ = W.globals_(jc); cn = {nd.get('name'): i for i, nd in enumerate(jc['nodes'])}
rootB = [i for i in range(len(m['nodes'])) if m['parent'].get(i) is None][0]
RootM = np.array(m['nodes'][rootB].get('matrix') or 0) if False else W.trs(m['nodes'][rootB])
D = json.load(open(DUMP))['frames']
def M12(v): T = np.eye(4); T[:3, :3] = np.array(v[:9]).reshape(3, 3).T; T[:3, 3] = v[9:]; return T
dom = np.array([B['names'][B['J'][i][np.argmax(B['W'][i])]] for i in range(len(B['V']))]); wmax = B['W'].max(1)
legs = np.where((np.char.find(dom.astype(str), 'Leg') >= 0) | np.isin(dom, ['LeftFoot', 'RightFoot', 'LeftToeBase', 'RightToeBase']))[0]
legs = legs[wmax[legs] > 0.5][::2]; BL = dict(B, V=B['V'][legs], N=B['N'][legs], J=B['J'][legs], W=B['W'][legs])
def pose_g(P, G):  # G: name -> 4x4 (model space)
    V, N, J, Wt = P['V'], P['N'], P['J'], P['W']; out = np.zeros_like(V); on = np.zeros_like(V); Vh = np.c_[V, np.ones(len(V))]
    for k in range(4):
        for jj in np.unique(J[:, k]):
            s = (J[:, k] == jj) & (Wt[:, k] > 0)
            if s.any():
                Mm = G[P['names'][jj]] @ P['ibm'][jj]; out[s] += (Vh[s] @ Mm.T)[:, :3] * Wt[s, k:k + 1]; on[s] += (N[s] @ Mm[:3, :3].T) * Wt[s, k:k + 1]
    return out, on / np.maximum(np.linalg.norm(on, axis=1, keepdims=True), 1e-9)
capeb = [n for n in CP['names'] if n.startswith('cape_')]
# check the space mapping on Spine: glTF model global vs RootM @ dumped skeleton-space global, at the dump's first frame
f0 = D[0]; Gb = C.globals_at(m, f0['clip'], f0['tc']); chk = np.abs(Gb[nid['Spine']][:3, 3] - (RootM @ M12(f0['bones']['Spine']))[:3, 3]).max()
res = {}; K = 1.96 / 1.70
for f in D:
    Gb = C.globals_at(m, f['clip'], f['tc']); G = {n: Gb[i] for n, i in nid.items()}
    if RIGID:   # cape bones at rest under the animated chest
        for n in capeb:
            chain = []; x = cn[n]; pj = {c: i for i, nd in enumerate(jc['nodes']) for c in nd.get('children', [])}
            while jc['nodes'][x]['name'].startswith('cape_'): chain.append(x); x = pj[x]
            Mx = G[jc['nodes'][x]['name']]
            for c in reversed(chain): Mx = Mx @ W.trs(jc['nodes'][c])
            G[n] = Mx
    else:
        for n in capeb: G[n] = RootM @ M12(f['bones'][n])
    CV, CN = pose_g(CP, G); BV, _ = pose_g(B, {n: G[n] for n in B['names']}); HV, _ = pose_g(CH, {n: G[n] for n in CH['names']}); LV, _ = pose_g(BL, G)
    CV, BV, HV, LV = CV * K, BV * K, HV * K, LV * K
    top = CV[:, 1].max(); h = np.ptp(CV[:, 1]); hx = G['Hips'][0, 3] * K
    back = (CV[:, 1] > top - h / 3) & (np.abs(CV[:, 0] - hx) < 0.20)
    gap = cKDTree(np.vstack([BV[::3], HV])).query(CV[back])[0]
    lo, hi = CV.min(0), CV.max(0); fp = (LV[:, 0] > lo[0]) & (LV[:, 0] < hi[0]) & (LV[:, 1] > lo[1]) & (LV[:, 1] < hi[1])
    d, i = cKDTree(CV).query(LV); poke = float((fp & (d < 0.10) & (((LV - CV[i]) * CN[i]).sum(1) > 0.005)).mean())
    r = res.setdefault(f['clip'], dict(gap_med=[], gap_p90=[], poke=[]))
    r['gap_med'].append(float(np.median(gap))); r['gap_p90'].append(float(np.percentile(gap, 90))); r['poke'].append(poke)
out = dict(space_check_m=round(float(chk) * K, 5), mode='rigid' if RIGID else 'simulated',
           clips={c: dict(frames=len(v['poke']), back_gap_median_m=round(float(np.median(v['gap_med'])), 4), back_gap_p90_m=round(float(np.median(v['gap_p90'])), 4),
                          poke_max=round(max(v['poke']), 4), poke_mean=round(float(np.mean(v['poke'])), 4)) for c, v in res.items()})
print(json.dumps(out, indent=1))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
