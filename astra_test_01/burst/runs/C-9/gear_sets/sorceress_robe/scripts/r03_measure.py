# R-C9-120: measure a skinned robe on her clips, in pure glTF (linear-blend skinning in numpy, the body's own clip curves).
#   python3 r03_measure.py <robe.glb> <body.glb> <out.json> [--clips walk,run,cast_fireball,cast_meteor]
# STRETCH  edges longer than 2x their rest length (and > 5 cm) in any frame -- worst frame per clip.
# JERK     the hem's blockiness: the hem ring (vertices in the bottom 3% of the robe's height, ordered round the body axis),
#          each ring segment's direction per frame; angular speed w(t) = the angle a segment turns between frames;
#          jerk = |w(t+1) - w(t)| (deg / frame^2). A hem riding the shins in blocks shows as segments that snap.
#          Reported: p95 and max over segments and frames, per clip.
import json, sys
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); G_ = __import__('55_clip_graft')
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_robe/scripts')
D = __import__('r01_diagnose')
a = sys.argv[1:]; ROBE, BODY, OUT = a[0], a[1], a[2]
CLIPS = a[a.index('--clips') + 1].split(',') if '--clips' in a else ["walk", "run", "cast_fireball", "cast_meteor"]
js, b, ni, jn, P, J, Wt, I = D.load(ROBE)
sk = js['skins'][js['nodes'][ni]['skin']]
ibm = L.read_accessor(js, b, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
Mbind = D.node_world(js)[sk['joints'][0]] @ ibm[0]
Ploc = None
# the mesh-space positions (POSITION), for skinning
pos = []
for p in js['meshes'][js['nodes'][ni]['mesh']]['primitives']:
    pos.append(L.read_accessor(js, b, p['attributes']['POSITION']))
Ploc = np.hstack([np.vstack(pos), np.ones((len(P), 1))])
bj, bb = L.load_glb(BODY); bn = {n.get('name'): i for i, n in enumerate(bj['nodes'])}
e = np.vstack([I[:, [0, 1]], I[:, [1, 2]], I[:, [2, 0]]]); e = np.unique(np.sort(e, 1), axis=0)
L0 = np.linalg.norm(P[e[:, 0]] - P[e[:, 1]], axis=1)
y = P[:, 1]; hf = (y - y.min()) / (y.max() - y.min())
hem = np.where(hf < 0.03)[0]
cx, cz = np.median(P[:, 0]), np.median(P[:, 2])
order = hem[np.argsort(np.arctan2(P[hem, 2] - cz, P[hem, 0] - cx))]
ring = order[:: max(1, len(order) // 160)]
seg = np.stack([ring, np.roll(ring, -1)], 1)
seg = seg[np.linalg.norm(P[seg[:, 0]] - P[seg[:, 1]], axis=1) < 0.08]      # not across the front split
rep = {}
for clip in CLIPS:
    an = next(x for x in bj['animations'] if x.get('name') == clip)
    trk = G_.tracks(bj, bb, an)
    times = sorted(set(float(t) for tr in trk.values() for (tt, _, _) in tr.values() for t in tt))
    worst, dirs = 0, []
    worst_skirt = 0                                                     # edges below 0.6 of the robe's height (the skirt, not the sleeve-hip junction)
    stretched_frames = 0
    for t in times:
        Gb, _ = G_.globals_from(bj, G_.local_mats(bj, trk, t, True))
        Mj = np.stack([Gb[bn[n]] @ ibm[k] for k, n in enumerate(jn)])
        V = np.zeros((len(P), 3))
        for c in range(4):
            V += Wt[:, c:c + 1] * np.einsum('vij,vj->vi', Mj[J[:, c]], Ploc)[:, :3]
        Lt = np.linalg.norm(V[e[:, 0]] - V[e[:, 1]], axis=1)
        mm = (Lt > 2 * L0) & (Lt > 0.05); n_ = int(mm.sum()); worst = max(worst, n_); stretched_frames += n_ > 0
        worst_skirt = max(worst_skirt, int((mm & (hf[e[:, 0]] < 0.6) & (hf[e[:, 1]] < 0.6)).sum()))
        d = V[seg[:, 1]] - V[seg[:, 0]]; dirs.append(d / np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-9))
    dirs = np.array(dirs)
    w = np.degrees(np.arccos(np.clip((dirs[1:] * dirs[:-1]).sum(2), -1, 1)))
    jerk = np.abs(np.diff(w, axis=0))
    jk = np.unravel_index(int(np.argmax(jerk)), jerk.shape); sv = seg[jk[1]]
    rep[clip] = dict(frames=len(times), stretched_edges_worst_frame=worst, skirt_stretched_edges_worst_frame=worst_skirt,
                     jerk_max_at=dict(frame=int(jk[0]) + 1, seg_mid=np.round(0.5 * (P[sv[0]] + P[sv[1]]), 3).tolist(), seg_len_m=round(float(np.linalg.norm(P[sv[0]] - P[sv[1]])), 3)), frames_with_stretch=int(stretched_frames),
                     hem_jerk_deg_per_frame2_p95=round(float(np.percentile(jerk, 95)), 3), hem_jerk_max=round(float(jerk.max()), 3),
                     hem_angular_speed_p95=round(float(np.percentile(w, 95)), 3))
    print("MEAS %-14s %s" % (clip, rep[clip]))
json.dump(dict(robe=ROBE, body=BODY, hem_ring_segments=int(len(seg)), clips=rep), open(OUT, 'w'), indent=1)
