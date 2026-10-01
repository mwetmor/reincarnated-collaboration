# POSTURE, per clip (stage H): in the ROOT frame (up +Y, forward +Z), over every key, median and worst:
#   torso_pitch  Hips -> neck vector's angle from vertical, + = leaning FORWARD (deg)
#   head_ratio   head_end height / its height at rest (rest = his standing height)
#   knee         knee flexion = angle between UpLeg->Leg and Leg->Foot, the larger of the two legs (deg; 0 = straight)
#   chin         Head -> headfront direction's elevation minus its rest elevation (deg; + = chin raised, - = head down)
#   python3 e30_posture.py <glb> [clip,clip...|all] [--json f]
import sys, os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = [x for x in sys.argv[1:] if not x.startswith('--')]; P = a[0]
m = C.model(P); nid = m['nid']
clips = list(m['anims']) if len(a) < 2 or a[1] == 'all' else a[1].split(',')
G0, _ = W.globals_(L.load_glb(P)[0])
def feats(G):
    p = lambda n: G[nid[n]][:3, 3]
    v = p('neck') - p('Hips'); pitch = math.degrees(math.atan2(v[2], v[1]))
    ang = lambda a_, b_, c_: math.degrees(math.acos(np.clip(np.dot((b_ - a_) / np.linalg.norm(b_ - a_), (c_ - b_) / np.linalg.norm(c_ - b_)), -1, 1)))
    knee = max(ang(p('LeftUpLeg'), p('LeftLeg'), p('LeftFoot')), ang(p('RightUpLeg'), p('RightLeg'), p('RightFoot')))
    hf = p('headfront') - p('Head'); chin = math.degrees(math.asin(np.clip(hf[1] / np.linalg.norm(hf), -1, 1)))
    floor = min(p('LeftToeBase')[1], p('RightToeBase')[1], p('LeftFoot')[1], p('RightFoot')[1])
    return pitch, p('head_end')[1] - floor, knee, chin
r0 = feats(G0); out = {}
for c in clips:
    tt = sorted({float(t) for v in m['anims'][c].values() for t in v[0]})
    F = np.array([feats(C.globals_at(m, c, t)) for t in tt])
    out[c] = dict(torso_pitch=[round(float(np.median(F[:, 0])), 1), round(float(F[:, 0].max()), 1)],
                  head_ratio=[round(float(np.median(F[:, 1] / r0[1])), 3), round(float(F[:, 1].min() / r0[1]), 3)],
                  knee=[round(float(np.median(F[:, 2])), 1), round(float(F[:, 2].max()), 1)],
                  chin=[round(float(np.median(F[:, 3] - r0[3])), 1), round(float((F[:, 3] - r0[3]).min()), 1)], keys=len(tt))
    print('%-16s pitch %6.1f (max %6.1f)  head %.3f (min %.3f)  knee %5.1f (max %5.1f)  chin %6.1f (min %6.1f)' % (c, *out[c]['torso_pitch'], *out[c]['head_ratio'], *out[c]['knee'], *out[c]['chin']))
if '--json' in sys.argv: json.dump(dict(file=P, rest=dict(head_end_y=r0[1], chin_elev=r0[3]), clips=out), open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
