# FOOT-LOCK SPEED of an in-place loop: the ground speed that pins the stance foot.
#
#   python3 scripts/57_footlock.py <body.glb> walk,run,strafe_L_armed@1:0:0 [--hz 60] [--json f]
#
# clip@dx:dy:dz: the travel direction in the model frame (default +Z, his forward; the strafes travel
# along knight.gd's strafe_dirs -- strafe_L_armed +X, strafe_R_armed -X).
#
# THE SCENE'S RULE (T12_11; so_d7/scripts/s18_footlock_contact.py, the D2 lane's rebuild of the scene's own
# instrument, godot/tools/capture_painted.gd --feet): at each sample the STANCE SIDE is the lower TOE
# (LeftToeBase / RightToeBase), if it is within 3 cm of that toe's lowest; the speed is that side's FOOT joint
# (LeftFoot / RightFoot) over the interval to the next sample, its BACKWARD component along the travel; the
# median over every stance sample, both sides pooled. Evaluated from the glTF, no importer in the loop
# (s17_loop_closure.py's evaluator). speed_m_s is the rule AT THE SCENE'S PHYSICS RATE (--hz, 60: the tick the
# scene's own instrument samples at); the same rule at the clip's own keys is reported beside it (keys_m_s -- the
# D2 lane states hers at the keys). Why the tick: measured IN THE SCENE with the same rule at 60 Hz
# (attack_lab/t12/godot/tools/strafe_probe.gd, T12_11), his strafes' stance feet move at 0.700 / 0.285 m/s; the
# 60 Hz estimate reads 0.6976 / 0.2896 (0.3% / 1.6% off), the keys 0.6925 / 0.2960 (1.1% / 3.9%).
#
# SUPERSEDED (T12_9-T12_10): s6_footlock.py's rule -- a foot planted whenever its ANKLE is in the bottom 25%
# of its own height range. In a run that band takes in the landing and the lift-off, and the median moves with
# the sampling (her run: 3.986 at the keys, 3.686 dense; the scene's rule 4.604 / 4.614, the scene 4.574).
# Still computed and reported as `s6_superseded`, so every number this replaces is stated beside its successor.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
S17 = __import__('s17_loop_closure')
F = np.array([0.0, 0.0, 1.0])
TOES = ("LeftToeBase", "RightToeBase")
FEET = ("LeftFoot", "RightFoot")
CONTACT_M = 0.03


def own_keys(m, clip):
    by = {}
    for (tt, vv) in m['anims'][clip].values():
        if len(tt) > 2:
            by.setdefault(len(tt), []).append(tt)
    return max(by.items(), key=lambda kv: (len(kv[1]), kv[0]))[1][0]


def paths(m, clip, ts):
    P = {j: [] for j in TOES + FEET}
    for t in ts:
        G = S17.globals_at(m, clip, float(t))
        for j in P:
            P[j].append(G[m['nid'][j]][:3, 3].copy())
    return {j: np.array(v) for j, v in P.items()}


def scene_rule(P, ts, fwd):
    lo = {j: float(P[j][:, 1].min()) for j in TOES}
    v, side_n = [], [0, 0]
    for i in range(len(ts) - 1):
        k = 0 if P[TOES[0]][i, 1] <= P[TOES[1]][i, 1] else 1
        if P[TOES[k]][i, 1] <= lo[TOES[k]] + CONTACT_M:
            a = P[FEET[k]]
            v.append(float(-(a[i + 1] - a[i]) @ fwd / (ts[i + 1] - ts[i])))
            side_n[k] += 1
    return v, side_n


def s6_rule(P, ts, fwd, joints):
    v = []
    for j in joints:
        y = P[j][:, 1]; lo_, hi = float(y.min()), float(y.max())
        c = y <= lo_ + 0.25 * (hi - lo_)
        v += [float(-(P[j][i + 1] - P[j][i]) @ fwd / (ts[i + 1] - ts[i])) for i in range(len(ts) - 1) if c[i] and c[i + 1]]
    return v


def med(v):
    return round(float(np.median(v)), 4) if v else None


def footlock(m, clip, fwd=None, hz=60.0):
    fwd = F if fwd is None else np.asarray(fwd, float) / np.linalg.norm(fwd)
    ks = np.asarray(own_keys(m, clip), float)
    T = float(ks[-1])
    ds = np.arange(0.0, T + 1e-9, 1.0 / hz)
    Pk, Pd = paths(m, clip, ks), paths(m, clip, ds)
    vk, nk = scene_rule(Pk, ks, fwd)
    vd, nd = scene_rule(Pd, ds, fwd)
    return dict(clip=clip, dir=[float(x) for x in fwd], keys=int(len(ks)), T_s=round(T, 4),
                speed_m_s=med(vd), hz=hz, samples=len(vd),
                keys_m_s=med(vk), keys_samples=len(vk), keys_by_side=dict(left=nk[0], right=nk[1]),
                rule="scene: stance side = the lower toe within %.0f cm of its lowest; that side's foot joint, backward along the travel; median, sides pooled" % (CONTACT_M * 100),
                s6_superseded=dict(foot_joints_m_s=med(s6_rule(Pk, ks, fwd, FEET)), toes_m_s=med(s6_rule(Pk, ks, fwd, TOES)),
                                   dense_foot_joints_m_s=med(s6_rule(Pd, ds, fwd, FEET)),
                                   rule="s6: bottom 25% of each joint's own height range, intervals planted at both ends, pooled"))


if __name__ == '__main__':
    a = sys.argv[1:]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    hz = float(a[a.index('--hz') + 1]) if '--hz' in a else 60.0
    m = S17.model(a[0])
    res = []
    for spec in a[1].split(','):
        clip, _, d = spec.partition('@')
        r = footlock(m, clip, [float(x) for x in d.split(':')] if d else None, hz); res.append(r)
        s6 = r['s6_superseded']
        print("  %-15s %2d keys, T %.4f s | foot-lock (the scene's rule): %.4f m/s at %g Hz (%d samples); %.4f at the keys (%d, L %d / R %d)"
              " | s6 (superseded): foot joints %.4f, toes %.4f, foot joints %g Hz %.4f"
              % (clip, r['keys'], r['T_s'], r['speed_m_s'], hz, r['samples'], r['keys_m_s'], r['keys_samples'], r['keys_by_side']['left'],
                 r['keys_by_side']['right'], s6['foot_joints_m_s'], s6['toes_m_s'], hz, s6['dense_foot_joints_m_s']))
    if outj:
        json.dump(res, open(outj, 'w'), indent=1)
