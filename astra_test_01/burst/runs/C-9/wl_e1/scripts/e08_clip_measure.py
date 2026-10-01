# Per clip: duration, key count/fps, hand separation (a two-handed grip keeps the hands together), wrist heights, hips travel.
#   python3 e08_clip_measure.py anims/*.glb
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')
out = {}
for p in sys.argv[1:]:
    m = C.model(p); nid = m['nid'] if 'nid' in m else {n.get('name'): i for i, n in enumerate(m['nodes'])}
    clip = list(m['anims'])[0]; ch = m['anims'][clip]
    T = max(float(v[0][-1]) for v in ch.values()); nk = max(len(v[0]) for v in ch.values())
    ts = np.linspace(0, T, 31); sep, hz, hip = [], [], []
    for t in ts:
        G = C.globals_at(m, clip, t)
        r, l = G[nid['RightHand']][:3, 3], G[nid['LeftHand']][:3, 3]
        sep.append(np.linalg.norm(r - l)); hz.append((r[1] + l[1]) / 2); hip.append(G[nid['Hips']][:3, 3])
    hip = np.array(hip); unit = 0.01 if np.abs(hip).max() > 10 else 1.0
    rec = dict(clip=clip, T=round(T, 4), keys=nk, fps=round((nk - 1) / T, 2), hand_sep_m=[round(min(sep) * unit, 3), round(float(np.median(sep)) * unit, 3), round(max(sep) * unit, 3)],
               hands_y_m=[round(min(hz) * unit, 3), round(max(hz) * unit, 3)], hips_travel_m=round(float(np.linalg.norm((hip[-1] - hip[0])[[0, 2]])) * unit, 3))
    out[os.path.basename(p)] = rec; print(os.path.basename(p), rec)
json.dump(out, open(os.path.join(os.path.dirname(HERE), 'work', 'clip_measure.json'), 'w'), indent=1)
