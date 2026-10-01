# STAGE I (1): a NAMED NECK/HEAD EDIT over a clip -- "head_lift": the neck turned up by A_NECK and the head by A_HEAD more, both
# about HIS LATERAL axis (the root's X), applied in WORLD space on every key (local = parent'^-1 . R . world). Measured, not
# solved: the angles are arguments; e30_posture reads the chin after. Binary patch on the clip's own keys.
#   python3 e33_head_lift.py <in.glb> <out.glb> <clip> <neck_deg> <head_deg> [--json f]
import json, os, sys, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT, CLIP = a[:3]; AN, AH = float(a[3]), float(a[4])
rot = lambda M: M[:3, :3] / np.cbrt(np.linalg.det(M[:3, :3]))
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
root = [i for i in range(len(m['nodes'])) if m['parent'].get(i) is None][0]
an = next(x for x in js['animations'] if x['name'] == CLIP)
tt = sorted({float(t) for v in m['anims'][CLIP].values() for t in v[0]})
qs = {'neck': [], 'Head': []}
for t in tt:
    G = C.globals_at(m, CLIP, t); Rr = rot(G[root])
    wN = Rr.T @ rot(G[nid['neck']]); wH = Rr.T @ rot(G[nid['Head']]); wP = Rr.T @ rot(G[m['parent'][nid['neck']]])
    RN = W.axis_angle([1.0, 0, 0], math.radians(-AN)); RH = W.axis_angle([1.0, 0, 0], math.radians(-(AN + AH)))
    wN2 = RN @ wN; wH2 = RH @ wH
    qs['neck'].append(W.m2q(wP.T @ wN2)); qs['Head'].append(W.m2q(wN2.T @ wH2))
tin = CH.add_accessor(js, bn, np.array(tt), "SCALAR")
for j, q in qs.items():
    q = np.array(q); q /= np.linalg.norm(q, axis=1, keepdims=True)
    for i in range(1, len(q)):
        if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
    an['channels'] = [c for c in an['channels'] if not (c['target']['node'] == nid[j] and c['target']['path'] == 'rotation')]
    o = CH.add_accessor(js, bn, q, "VEC4"); an['samplers'].append({"input": tin, "output": o, "interpolation": "LINEAR"})
    an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": nid[j], "path": "rotation"}})
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
rep = dict(clip=CLIP, neck_deg=AN, head_deg=AH, keys=len(tt)); print(rep)
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
