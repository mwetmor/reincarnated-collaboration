# bm_mx STAGE 3 (R-C9-133): the PASSIVE arm of a one-handed clip CARRIES its weapon -- e09_hold.py's rule for ONE side. The Mixamo
# one-handed attacks swing the empty off arm freely (the axe pack's left hand to his gut, the reacts' hand to the belly), and in the
# dual kit that hand holds a blade, which then goes through him (chop: axe_l 49% inside). The side's arm chain (Shoulder, Arm, ForeArm,
# Hand) takes the LOCAL rotations of a carry pose <clip>@<t> (the idle, whose arms carry: bm09 arm mirror), constant over the target's
# own keys -- local, so the arm rides the chest as the torso turns. Binary patch: new constant outputs on the same inputs.
#   python3 bm11_hold_side.py <in.glb> <out.glb> --side L|R --from idle@1.0 --clips chop,attack [--json f]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); R_ = __import__('49_recentre'); CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
side = {'L': 'Left', 'R': 'Right'}[opt('--side')]; fc, ft = opt('--from').split('@'); ft = float(ft)
ARM = [side + x for x in ('Shoulder', 'Arm', 'ForeArm', 'Hand')]
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']
def at(n):
    tt, vv = m['anims'][fc][(nid[n], 'rotation')]; return np.array(vv[int(np.argmin(np.abs(np.array(tt) - ft)))], float)
held = {n: at(n) for n in ARM}; rep = dict(side=side, source='%s@%.4f' % (fc, ft), clips={})
for clip in opt('--clips').split(','):
    an = next(x for x in js['animations'] if x['name'] == clip)
    for n in ARM:
        ch = next(c for c in an['channels'] if c['target']['node'] == nid[n] and c['target']['path'] == 'rotation')
        s = an['samplers'][ch['sampler']]; k = L.read_accessor(js, bn, s['input']).shape[0]
        an['samplers'].append({"input": s['input'], "output": CH.add_accessor(js, bn, np.tile(held[n], (k, 1)), "VEC4"), "interpolation": "LINEAR"})
        ch['sampler'] = len(an['samplers']) - 1
    rep['clips'][clip] = ARM
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
r = L.lint(OUT); print(json.dumps(rep), '| lint', r['verdict'], r['fails'][:2])
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
