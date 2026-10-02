# EYE OF RECKONING SPIN, recipe (a) -- the v7 rule (R-C9-108, the barbarian's whirlwind): ONE frame of his approved stance, turned
# RIGIDLY about the vertical through his hips, counter-clockwise from above (the packet: Soulfire orbits CCW). No solver.
#   eor_spin_start  0.200 s (7 keys at 30 fps): the stance turning from rest, angle = w t^2 / (2 x 0.2), so it leaves at the loop's
#                   own angular speed w = 360 deg / 0.300 s and has turned 120 deg
#   eor_spin_loop   0.300 s (10 keys, 9 intervals of 40 deg): one revolution from 120 deg on; pose(T) == pose(0) by construction
# Every joint but the Hips holds the stance frame's local TRS; the Hips rotation is Ry(psi) . q_stance (its translation stays: the turn
# is about his own vertical). The packet's rate laws are the runtime's (rate-free authoring). He can move while channelling: the clip
# is in place; the runtime carries him.
#   python3 e48_spin.py <in.glb> <out.glb> --pose <clip>@<t> [--json f]
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
pc, pt = opt('--pose', 'idle@1.0').split('@'); pt = float(pt)
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
an = next(x for x in js['animations'] if x['name'] == pc)
joints = [n for n in m['nid'] if n in {js['nodes'][j]['name'] for j in js['skins'][0]['joints']} and n not in ('weapon_r', 'weapon_l')]
def local_at(n, path):
    k = (nid[n], path)
    if k in m['anims'][pc]:
        tt, vv = m['anims'][pc][k]; i = int(np.argmin(np.abs(tt - pt))); return np.array(vv[i], float)
    return {'translation': m['rest'][nid[n]][0], 'rotation': m['rest'][nid[n]][1]}[path]
pose = {n: (local_at(n, 'translation'), local_at(n, 'rotation')) for n in joints}
w = 2 * math.pi / 0.3
def qy(ang): return np.array([0.0, math.sin(ang / 2), 0.0, math.cos(ang / 2)])
def build(name, times, angs):
    tin = CH.add_accessor(js, bn, np.array(times), "SCALAR"); ch, sm = [], []
    for n in joints:
        tr, q = pose[n]
        if n == 'Hips':
            qs = np.array([CH.qmul(qy(g), q) for g in angs]); trs = np.tile(tr, (len(times), 1))
        else:
            qs = np.tile(q, (len(times), 1)); trs = None
        for i in range(1, len(qs)):
            if np.dot(qs[i], qs[i - 1]) < 0: qs[i] = -qs[i]
        sm.append({"input": tin, "output": CH.add_accessor(js, bn, qs, "VEC4"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": nid[n], "path": "rotation"}})
        if trs is not None:
            sm.append({"input": tin, "output": CH.add_accessor(js, bn, trs, "VEC3"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": nid[n], "path": "translation"}})
    js['animations'] = [x for x in js['animations'] if x['name'] != name] + [{"name": name, "channels": ch, "samplers": sm}]
ts = [i / 30.0 for i in range(7)]; build('eor_spin_start', ts, [w * t * t / (2 * 0.2) for t in ts])
tl = [i / 30.0 for i in range(10)]; a0 = w * 0.2 / 2; build('eor_spin_loop', tl, [a0 + 2 * math.pi * i / 9 for i in range(10)])
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
rep = dict(pose='%s@%.4f' % (pc, pt), start=dict(seconds=0.2, keys=7, turn_deg=round(math.degrees(w * 0.2 / 2), 1), exit_speed_deg_s=round(math.degrees(w), 1)),
           loop=dict(seconds=0.3, keys=10, deg_per_key=40.0, direction='CCW from above (+Y)'), joints=len(joints)); print(json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
