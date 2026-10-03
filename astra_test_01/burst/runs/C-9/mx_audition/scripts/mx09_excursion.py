# MX audition (R-C9-149): the hips' largest HORIZONTAL distance from the record's origin over each clip (m) -- after deroot a
# one-shot that travels mid-clip (a leap, a stagger) still leaves the sprite anchor; the contract renders about the origin.
#   python3 scripts/mx09_excursion.py <aud.glb> -> prints and merges 'hips_excursion_m' into work/meas_<tag>.json (tag from the name)
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'en_e2', 'scripts')); C = __import__('s17_loop_closure')
g = sys.argv[1]; tag = os.path.basename(g)[4:-4]; m = C.model(g); h = m['nid']['Hips']
mj = 'work/meas_%s.json' % tag; M = json.load(open(mj))
for clip in M['clips']:
    T = sorted({float(t) for ch in m['anims'][clip].values() for t in ch[0]})
    P = np.array([C.globals_at(m, clip, t)[h][:3, 3] for t in T]); e = float(np.max(np.hypot(P[:, 0], P[:, 2])))
    M['clips'][clip]['hips_excursion_m'] = round(e, 3); print('%-14s hips excursion %.3f m' % (clip, e))
json.dump(M, open(mj, 'w'), indent=1)
