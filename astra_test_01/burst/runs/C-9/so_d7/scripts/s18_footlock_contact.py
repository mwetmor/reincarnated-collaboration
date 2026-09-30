# WHY HER RUN SKATES IN THE SCENE (the integration drax, barrow_full/take/build/t12_10_feet.json: driven at the manifest's
# 3.986 m/s, her stance foot moves at 4.574 m/s relative to her body -- ratio 1.148 -- while the walk grips at 1.019).
#
#   python3 scripts/s18_footlock_contact.py <body.glb> walk,run [--hz 60] [--json f]
#
# The same in-place clip, several estimators, so the disagreement can be put on ONE cause -- the clip, the measure, or the
# in-place bake. Pure glTF evaluation (s17_loop_closure's evaluator; world metres, +Y up, she faces +Z).
#   s6        s6_footlock.py's: the ANKLES (LeftFoot / RightFoot), a joint is planted in the bottom 25% of its own height
#             range, intervals planted at both ends, the BACKWARD component, both feet pooled, the median -- at the keys
#   scene     t12_10_feet's (godot/tools/capture_painted.gd --feet): the stance side = the lower TOE (LeftToeBase /
#             RightToeBase), within 3 cm of that toe's lowest; the speed of that side's FOOT joint relative to the body; the
#             median over stance samples -- at the physics rate (--hz, 60 as the scene's). Found by elimination: of the
#             variants below it alone reproduces the scene's own numbers (walk 1.499, run 4.574 m/s) to 1%
#   and the two crossed (s6's rule on the toes, the scene's rule on the ankles), so a joint effect and a rule effect
#   are told apart. Each also as the horizontal speed's MAGNITUDE and as its BACKWARD component.
# The in-place bake is checked on its own: the hips' horizontal travel over the clip (a clip that still travels would
# add its travel speed to every foot).
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')
a = sys.argv[1:]
BODY, CLIPS = a[0], a[1].split(",")
HZ = float(a[a.index('--hz') + 1]) if '--hz' in a else 60.0
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
m = C.model(BODY)
JOINTS = {"ankle": ("LeftFoot", "RightFoot"), "toe": ("LeftToeBase", "RightToeBase")}


def path(clip, times):
    out = {}
    for x in times:
        G = C.globals_at(m, clip, float(x))
        for j in JOINTS["ankle"] + JOINTS["toe"] + ("Hips",):
            out.setdefault(j, []).append(G[m['nid'][j]][:3, 3].copy())
    return {k: np.array(v) for k, v in out.items()}


def vel(P, t):                      # per interval: horizontal velocity (x, z), metres per second
    d = np.diff(P[:, [0, 2]], axis=0) / np.diff(t)[:, None]
    return d


def rule_range(P, t, joints):       # s6: bottom 25% of each joint's range, planted at both ends of an interval
    back, mag = [], []
    for j in joints:
        y = P[j][:, 1]; thr = y.min() + 0.25 * (y.max() - y.min()); v = vel(P[j], t)
        for i in range(len(t) - 1):
            if y[i] < thr and y[i + 1] < thr:
                back.append(-v[i, 1]); mag.append(float(np.hypot(*v[i])))
    return back, mag


def rule_lowest(P, t, joints):      # the scene: the lower joint of the two, within 3 cm of that joint's lowest
    lo = {j: P[j][:, 1].min() for j in joints}
    back, mag = [], []
    for i in range(len(t) - 1):
        j = min(joints, key=lambda jj: P[jj][i, 1])
        if P[j][i, 1] <= lo[j] + 0.03:
            v = vel(P[j][i:i + 2], t[i:i + 2])[0]
            back.append(-v[1]); mag.append(float(np.hypot(*v)))
    return back, mag


def rule_scene(P, t, joints):       # the scene exactly: the stance SIDE = the lower toe, within 3 cm of that toe's lowest;
    toes, ankles = JOINTS["toe"], JOINTS["ankle"]                   # its speed = that side's FOOT joint (the ankle)
    lo = {j: P[j][:, 1].min() for j in toes}
    back, mag = [], []
    for i in range(len(t) - 1):
        k = min((0, 1), key=lambda s_: P[toes[s_]][i, 1])
        if P[toes[k]][i, 1] <= lo[toes[k]] + 0.03:
            v = vel(P[ankles[k]][i:i + 2], t[i:i + 2])[0]
            back.append(-v[1]); mag.append(float(np.hypot(*v)))
    return back, mag


def med(x):
    return round(float(np.median(x)), 3) if len(x) else None


rep = {}
for clip in CLIPS:
    T = float(max(v[0].max() for v in m['anims'][clip].values()))
    kt = np.unique(np.round(np.concatenate([v[0] for v in m['anims'][clip].values()]), 6))
    dt = np.arange(0.0, T + 1e-9, 1.0 / HZ)
    Pk, Pd = path(clip, kt), path(clip, dt)
    r = dict(seconds=round(T, 4), keys=len(kt), dense_hz=HZ, estimators={})
    for nm, rule, joints in (("s6 (ankles, bottom 25%)", rule_range, "ankle"), ("s6 rule on the toes", rule_range, "toe"),
                             ("lowest toe within 3 cm, the toe's speed", rule_lowest, "toe"),
                             ("lowest ankle within 3 cm, the ankle's speed", rule_lowest, "ankle"),
                             ("scene: stance by the lower toe (3 cm), that side's ANKLE speed", rule_scene, "toe")):
        e = {}
        for samp, P, t in (("keys", Pk, kt), ("dense", Pd, dt)):
            b, g = rule(P, t, JOINTS[joints])
            e[samp] = dict(backward_median=med(b), magnitude_median=med(g), samples=len(b),
                           backward_iqr=round(float(np.subtract(*np.percentile(b, [75, 25]))), 3) if b else None)
        r["estimators"][nm] = e
    h = Pk["Hips"]
    r["hips_net_travel_m"] = round(float(np.hypot(*(h[-1, [0, 2]] - h[0, [0, 2]]))), 4)
    r["hips_mean_speed_m_s"] = round(float(np.hypot(*(h[-1, [0, 2]] - h[0, [0, 2]])) / T), 4)
    # where in the stance the toe and the ankle part: the ankle's backward speed while the TOE is the scene's stance foot
    lo = {j: Pd[j][:, 1].min() for j in JOINTS["toe"]}
    part = []
    for side in (0, 1):
        tj, aj = JOINTS["toe"][side], JOINTS["ankle"][side]
        vt, va = vel(Pd[tj], dt), vel(Pd[aj], dt)
        for i in range(len(dt) - 1):
            low = min(JOINTS["toe"], key=lambda jj: Pd[jj][i, 1])
            if low == tj and Pd[tj][i, 1] <= lo[tj] + 0.03:
                part.append((-vt[i, 1], -va[i, 1], Pd[aj][i, 1] - Pd[aj][:, 1].min()))
    if part:
        P_ = np.array(part)
        r["toe_stance"] = dict(samples=len(P_), toe_backward_median=med(P_[:, 0]), ankle_backward_median_same_samples=med(P_[:, 1]),
                               ankle_height_above_its_lowest_m_median=round(float(np.median(P_[:, 2])), 3))
    rep[clip] = r
    print("  %s  (%d keys, %.4f s; hips net travel %.4f m)" % (clip, len(kt), T, r["hips_net_travel_m"]))
    for nm, e in r["estimators"].items():
        print("    %-62s keys: back %s mag %s (%d)   dense %g Hz: back %s mag %s (%d)"
              % (nm, e["keys"]["backward_median"], e["keys"]["magnitude_median"], e["keys"]["samples"], HZ,
                 e["dense"]["backward_median"], e["dense"]["magnitude_median"], e["dense"]["samples"]))
    if "toe_stance" in r:
        print("    while the TOE is the stance foot: toe back %.3f, ankle back %.3f (same samples), ankle %.3f m above its lowest"
              % (r["toe_stance"]["toe_backward_median"], r["toe_stance"]["ankle_backward_median_same_samples"],
                 r["toe_stance"]["ankle_height_above_its_lowest_m_median"]))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
