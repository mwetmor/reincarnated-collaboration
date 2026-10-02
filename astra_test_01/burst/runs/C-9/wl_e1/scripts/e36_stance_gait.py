# STAGE J scoring, per clip, in the root frame (up +Y):
#   stance   heel-to-heel LATERAL distance (Foot joints, across his facing) / hip width (LeftUpLeg-RightUpLeg), median over keys
#   hands_y  mean fist height / standing head_end height;  hand_sep  fist separation / shoulder width (LeftArm-RightArm)
#   arm_up   the higher hand's height above its shoulder joint (m, at 1.96 m; > 0 = raised above the shoulder)
#   shoulders  LeftArm-RightArm distance / its rest value (< 1 = drawn in together)
#   heel_toe  for loops: the foot's pitch (Foot -> ToeBase vs the ground) over the keys where that foot is within 4 cm of its
#            lowest: max toe-UP (heel strike) and max heel-UP (toe-off), deg. A flat-footed gait keeps both under ~8 deg.
#   python3 e36_stance_gait.py <glb> <clips|all> [--json f]
import sys, os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = [x for x in sys.argv[1:] if not x.startswith('--')]; P = a[0]; m = C.model(P); nid = m['nid']
clips = list(m['anims']) if len(a) < 2 or a[1] == 'all' else a[1].split(',')
G0, _ = W.globals_(L.load_glb(P)[0]); root = [i for i in range(len(m['nodes'])) if m['parent'].get(i) is None][0]
def pts(G):
    Ri = np.linalg.inv(G[root]); return {n: (Ri @ G[nid[n]])[:3, 3] for n in ('Hips', 'LeftUpLeg', 'RightUpLeg', 'LeftFoot', 'RightFoot', 'LeftToeBase', 'RightToeBase', 'LeftArm', 'RightArm', 'LeftHand', 'RightHand', 'head_end')}
p0 = pts(G0); H0 = p0['head_end'][1] - min(p0['LeftToeBase'][1], p0['RightToeBase'][1]); SW0 = np.linalg.norm(p0['LeftArm'] - p0['RightArm'])
K = 1.96 / H0; out = {}
for c in clips:
    tt = sorted({float(t) for v in m['anims'][c].values() for t in v[0]}); R = [pts(C.globals_at(m, c, t)) for t in tt]
    def lat(p):  # lateral axis = hips' left-right, horizontal
        ax = p['LeftUpLeg'] - p['RightUpLeg']; ax[1] = 0; ax /= np.linalg.norm(ax); return ax
    st = [abs(np.dot(p['LeftFoot'] - p['RightFoot'], lat(p))) / np.linalg.norm(p['LeftUpLeg'] - p['RightUpLeg']) for p in R]
    floor = [min(p['LeftToeBase'][1], p['RightToeBase'][1], p['LeftFoot'][1], p['RightFoot'][1]) for p in R]
    hy = [((p['LeftHand'][1] + p['RightHand'][1]) / 2 - f) / H0 for p, f in zip(R, floor)]
    sw = [np.linalg.norm(p['LeftArm'] - p['RightArm']) for p in R]
    hs = [np.linalg.norm(p['LeftHand'] - p['RightHand']) / s for p, s in zip(R, sw)]
    up = [max(p['LeftHand'][1] - p['LeftArm'][1], p['RightHand'][1] - p['RightArm'][1]) * K for p in R]
    toe_up, heel_up = [], []
    for side in ('Left', 'Right'):
        fy = np.array([p[side + 'Foot'][1] for p in R]); ty = np.array([p[side + 'ToeBase'][1] for p in R]); lo = min(fy.min(), ty.min())
        for p in R:
            if min(p[side + 'Foot'][1], p[side + 'ToeBase'][1]) - lo < 0.04 / K:
                v = p[side + 'ToeBase'] - p[side + 'Foot']; pit = math.degrees(math.atan2(v[1], np.hypot(v[0], v[2])))
                toe_up.append(pit); heel_up.append(-pit)
    rest_pitch = math.degrees(math.atan2((p0['LeftToeBase'] - p0['LeftFoot'])[1], np.hypot(*(p0['LeftToeBase'] - p0['LeftFoot'])[[0, 2]])))
    h2h = [abs(np.dot(p['LeftFoot'] - p['RightFoot'], lat(p))) * K for p in R]
    out[c] = dict(stance=round(float(np.median(st)), 2), heel_to_heel_m=round(float(np.median(h2h)), 3), hip_joint_width_m=round(float(np.linalg.norm(p0['LeftUpLeg'] - p0['RightUpLeg']) * K), 3), hands_y=round(float(np.median(hy)), 3), hand_sep=round(float(np.median(hs)), 2),
                  arm_up_m=round(float(np.median(up)), 3), shoulders=round(float(np.median(sw) / SW0), 3),
                  toe_up_deg=round(max(toe_up) - rest_pitch, 1) if toe_up else None, heel_up_deg=round(max(heel_up) + rest_pitch, 1) if heel_up else None)
    print('%-18s h2h %.3f m  stance %.2f  hands_y %.3f  hand_sep %.2f  arm_up %+.3f m  shoulders %.3f  toe_up %s  heel_up %s' % (c, out[c]['heel_to_heel_m'], out[c]['stance'], out[c]['hands_y'], out[c]['hand_sep'], out[c]['arm_up_m'], out[c]['shoulders'], out[c]['toe_up_deg'], out[c]['heel_up_deg']))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
