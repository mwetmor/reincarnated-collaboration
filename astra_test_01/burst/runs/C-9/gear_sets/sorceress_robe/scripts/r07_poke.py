# R-C9-120: BODY POKING THROUGH THE ROBE. Body vertices that are COVERED by the robe at rest (behind the nearest robe
# vertex along its outward normal) and come OUT in front of it in a frame (> 5 mm) -- per clip, the worst frame and where.
#   python3 r07_poke.py <robe.glb> <body.glb> [--clips walk,run,cast_fireball,cast_meteor] [--json out]
import json, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); G_ = __import__('55_clip_graft')
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_robe/scripts')
D = __import__('r01_diagnose')
a = sys.argv[1:]; ROBE, BODY = a[0], a[1]
CLIPS = a[a.index('--clips') + 1].split(',') if '--clips' in a else ["walk", "run", "cast_fireball", "cast_meteor"]


def piece(path):
    js, b, ni, jn, P, J, Wt, I = D.load(path)
    sk = js['skins'][js['nodes'][ni]['skin']]
    ibm = L.read_accessor(js, b, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    pr = js['meshes'][js['nodes'][ni]['mesh']]['primitives']
    pos = np.vstack([L.read_accessor(js, b, p['attributes']['POSITION']) for p in pr])
    nrm = np.vstack([L.read_accessor(js, b, p['attributes']['NORMAL']) for p in pr])
    return dict(jn=jn, P=P, J=J, W=Wt, ibm=ibm, pos=pos, nrm=nrm)


def skin(pc, Gb, bn):
    Mj = np.stack([Gb[bn[n]] @ pc['ibm'][k] for k, n in enumerate(pc['jn'])])
    M = np.zeros((len(pc['P']), 4, 4))
    for c in range(4):
        M += pc['W'][:, c, None, None] * Mj[pc['J'][:, c]]
    V = np.einsum('vij,vj->vi', M[:, :3, :3], pc['pos']) + M[:, :3, 3]
    N = np.einsum('vij,vj->vi', M[:, :3, :3], pc['nrm']); N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
    return V, N


bj, bb = L.load_glb(BODY); bn = {n.get('name'): i for i, n in enumerate(bj['nodes'])}
rb, bd = piece(ROBE), piece(BODY)
# rest: covered body vertices = within 8 cm of the robe and behind it, below the hips
G0, _ = G_.globals_from(bj, G_.local_mats(bj, {}, 0.0, True)) if False else (None, None)
tr = cKDTree(rb['P']); d0, i0 = tr.query(bd['P'])
# rest normals in world: bind
s0 = ((bd['P'] - rb['P'][i0]) * 0).sum(1)
rep = {}
for clip in CLIPS:
    an = next(x for x in bj['animations'] if x.get('name') == clip); trk = G_.tracks(bj, bb, an)
    times = sorted(set(float(t) for t_ in trk.values() for (tt, _, _) in t_.values() for t in tt))
    worst = (0, 0, None)
    covered = None
    for t in times:
        Gb, _ = G_.globals_from(bj, G_.local_mats(bj, trk, t, True))
        RV, RN = skin(rb, Gb, bn); BV, _ = skin(bd, Gb, bn)
        if covered is None:
            # covered at the clip's first frame, measured in the same skinning (robust to bind-vs-clip offsets)
            dd, ii = cKDTree(RV).query(BV)
            covered = (dd < 0.08) & (((BV - RV[ii]) * RN[ii]).sum(1) < 0) & (bd['P'][:, 1] < 0.85)
        dd, ii = cKDTree(RV).query(BV[covered])
        out = (((BV[covered] - RV[ii]) * RN[ii]).sum(1) > 0.005) & (dd < 0.10)
        if out.sum() > worst[0]:
            worst = (int(out.sum()), t, np.where(covered)[0][out])
    w = worst[2]
    rep[clip] = dict(covered=int(covered.sum()), poke_verts_worst_frame=worst[0], t=round(worst[1], 3),
                     where_rest_y_p10_50_90=np.round(np.percentile(bd['P'][w, 1], [10, 50, 90]), 3).tolist() if worst[0] else None,
                     where_rest_z_median=round(float(np.median(bd['P'][w, 2])), 3) if worst[0] else None)
    print("POKE %-14s %s" % (clip, rep[clip]))
if '--json' in a: json.dump(dict(robe=ROBE, clips=rep), open(a[a.index('--json') + 1], 'w'), indent=1)
