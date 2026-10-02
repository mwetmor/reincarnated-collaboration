# so_mx S2 (R-C9-131): survey the converted Mixamo clips in their OWN rig (before any graft): duration; for each hand its peak
# speed (and when), its highest point above its shoulder, its mean distance in front of the chest; hands' min separation;
# hips travel. Tells which hand a "1H" cast throws with and whether a cast is a sky cast.  python3 so02_survey.py <glb>...
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
G = __import__('55_clip_graft'); L = __import__('21_lint_export')
rows = {}
for p in sys.argv[1:]:
    js, b = L.load_glb(p); nm = {n.get('name'): i for i, n in enumerate(js['nodes'])}
    an = js['animations'][0]; trk = G.tracks(js, b, an)
    T = sorted(set(float(t) for tr in trk.values() for (tt, _, _) in tr.values() for t in tt))
    P = {k: [] for k in ("LeftHand", "RightHand", "LeftArm", "RightArm", "Hips", "Spine", "Head")}
    for t in T:
        Gw, _ = G.globals_from(js, G.local_mats(js, trk, t, True))
        for k in P: P[k].append(Gw[nm[k]][:3, 3])
    P = {k: np.array(v) for k, v in P.items()}
    sc = 1.0 / (P['Head'][0, 1] - min(P['Hips'][:, 1].min(), 0) + 1e-9)         # roughly body-height normalised
    fwd = P['Spine'][0] - P['Hips'][0]
    r = dict(dur=round(T[-1], 3), keys=len(T))
    for h, s in (("LeftHand", "LeftArm"), ("RightHand", "RightArm")):
        v = np.linalg.norm(np.diff(P[h], axis=0), axis=1) / np.diff(T)
        i = int(np.argmax(v))
        r[h[:-4]] = dict(peak_speed=round(float(v[i] * sc), 2), at=round(T[i + 1], 3),
                         max_above_shoulder=round(float(((P[h][:, 1] - P[s][:, 1]) * sc).max()), 2))
    r['hand_sep_min'] = round(float((np.linalg.norm(P['LeftHand'] - P['RightHand'], axis=1) * sc).min()), 2)
    r['hips_travel'] = np.round((P['Hips'][-1] - P['Hips'][0]) * sc, 2).tolist()
    rows[os.path.basename(p)[:-4]] = r
    print("%-10s %s" % (os.path.basename(p)[:-4], json.dumps(r)))
