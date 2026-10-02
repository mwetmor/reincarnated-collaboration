# EYE OF RECKONING SPIN, recipe (a) -- the v7 rule (R-C9-108, the barbarian's whirlwind): ONE frame of his approved stance, turned
# RIGIDLY about the vertical through his hips, counter-clockwise from above (the packet: Soulfire orbits CCW). No solver.
#   eor_spin_start  0.200 s (7 keys at 30 fps): the stance turning from rest, angle = w t^2 / (2 x 0.2), so it leaves at the loop's
#                   own angular speed w = 360 deg / 0.300 s and has turned 120 deg
#   eor_spin_loop   0.300 s (10 keys, 9 intervals of 40 deg): one revolution from 120 deg on; pose(T) == pose(0) by construction
# Every joint but the Hips holds the stance frame's local TRS; the Hips rotation is Ry(psi) . q_stance (its translation stays: the turn
# is about his own vertical). The packet's rate laws are the runtime's (rate-free authoring). He can move while channelling: the clip
# is in place; the runtime carries him.
#   python3 e48_spin.py <in.glb> <out.glb> --pose <clip>@<t> [--loop-s 0.3] [--loop-keys 10] [--start-s 0.2] [--prefix eor_spin]
#                       [--key-weapons] [--json f]
# R-C9-133 generalisation (the barbarian's dual whirlwind, 3.75 rev/s): --loop-s / --loop-keys set the revolution (keys at 30 fps
# when loop-s = (keys-1)/30), --prefix names the pair <prefix>_start / <prefix>_loop, and --key-weapons keys weapon_r AND weapon_l
# on every key at the pose frame's local TRS, so the effect reads both blade tips off the rig. Defaults reproduce the DK's spin.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
pc, pt = opt('--pose', 'idle@1.0').split('@'); pt = float(pt)
LOOP_S = float(opt('--loop-s', '0.3')); NK = int(opt('--loop-keys', '10')); START_S = float(opt('--start-s', '0.2')); PFX = opt('--prefix', 'eor_spin'); KW = '--key-weapons' in a
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
an = next(x for x in js['animations'] if x['name'] == pc)
joints = [n for n in m['nid'] if n in {js['nodes'][j]['name'] for j in js['skins'][0]['joints']} and (KW or n not in ('weapon_r', 'weapon_l'))]
def local_at(n, path):
    k = (nid[n], path)
    if k in m['anims'][pc]:
        tt, vv = m['anims'][pc][k]; i = int(np.argmin(np.abs(tt - pt))); return np.array(vv[i], float)
    return {'translation': m['rest'][nid[n]][0], 'rotation': m['rest'][nid[n]][1]}[path]
pose = {n: (local_at(n, 'translation'), local_at(n, 'rotation')) for n in joints}
w = 2 * math.pi / LOOP_S
def qy(ang): return np.array([0.0, math.sin(ang / 2), 0.0, math.cos(ang / 2)])
def build(name, times, angs):
    tin = CH.add_accessor(js, bn, np.array(times), "SCALAR"); ch, sm = [], []
    for n in joints:
        tr, q = pose[n]
        if n == 'Hips':
            qs = np.array([CH.qmul(qy(g), q) for g in angs]); trs = np.tile(tr, (len(times), 1))
        else:
            qs = np.tile(q, (len(times), 1)); trs = np.tile(tr, (len(times), 1)) if n in ('weapon_r', 'weapon_l') else None
        for i in range(1, len(qs)):
            if np.dot(qs[i], qs[i - 1]) < 0: qs[i] = -qs[i]
        sm.append({"input": tin, "output": CH.add_accessor(js, bn, qs, "VEC4"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": nid[n], "path": "rotation"}})
        if trs is not None:
            sm.append({"input": tin, "output": CH.add_accessor(js, bn, trs, "VEC3"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": nid[n], "path": "translation"}})
    js['animations'] = [x for x in js['animations'] if x['name'] != name] + [{"name": name, "channels": ch, "samplers": sm}]
ns = int(round(START_S * 30)) + 1; ts = [START_S * i / (ns - 1) for i in range(ns)]; build(PFX + '_start', ts, [w * t * t / (2 * START_S) for t in ts])
tl = [LOOP_S * i / (NK - 1) for i in range(NK)]; a0 = w * START_S / 2; build(PFX + '_loop', tl, [a0 + 2 * math.pi * i / (NK - 1) for i in range(NK)])
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
rep = dict(pose='%s@%.4f' % (pc, pt), start=dict(name=PFX + '_start', seconds=START_S, keys=ns, turn_deg=round(math.degrees(w * START_S / 2), 1), exit_speed_deg_s=round(math.degrees(w), 1)),
           loop=dict(name=PFX + '_loop', seconds=LOOP_S, keys=NK, deg_per_key=round(360.0 / (NK - 1), 3), rev_per_s=round(1 / LOOP_S, 4), direction='CCW from above (+Y)'),
           joints=len(joints), weapons_keyed=[n for n in joints if n in ('weapon_r', 'weapon_l')]); print(json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
