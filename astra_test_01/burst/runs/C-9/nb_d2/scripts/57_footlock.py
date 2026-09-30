# FOOT-LOCK SPEED of an in-place loop: the ground speed that pins the planted foot.
#
#   python3 scripts/57_footlock.py <body.glb> walk,run [--json f]
#
# so_d7/scripts/s6_footlock.py's definition (the D2 drax, 2026-09-30), evaluated from the glTF with
# no importer in the loop (s17_loop_closure.py's evaluator): SAMPLED AT THE CLIP'S OWN KEYS; contact
# is RELATIVE to each foot's own height range (its bottom 25%); over every interval planted at both
# ends, the median BACKWARD velocity of that foot (his forward is +Z) is the speed the scene must
# move him at for the foot to stand still. Reported for the foot joints and for the toe joints --
# the scene's own slide probe (attack_lab tools/speed_split.gd) watches the toes.
#
# Written for the T12_9 loop re-cut (N-C9 loop check): the T8 run cut on a 24 fps grid carried a
# held first key, and it read as a slow RIGHT foot -- joints L 4.161 / R 3.054 m/s; on the re-cut
# (the source's own 30 fps keys) L 3.952 / R 4.017, as the source gives (x1.08825, the T8 fit).
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
S17 = __import__('s17_loop_closure')
F = np.array([0.0, 0.0, 1.0])
FEET = ["LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"]


def own_keys(m, clip):
    by = {}
    for (tt, vv) in m['anims'][clip].values():
        if len(tt) > 2:
            by.setdefault(len(tt), []).append(tt)
    return max(by.items(), key=lambda kv: (len(kv[1]), kv[0]))[1][0]


def footlock(m, clip):
    ks = own_keys(m, clip)
    out = {}
    for foot in FEET:
        j = m['nid'][foot]
        P = np.array([S17.globals_at(m, clip, float(t))[j][:3, 3] for t in ks])
        y = P[:, 1]; lo, hi = float(y.min()), float(y.max())
        c = y <= lo + 0.25 * (hi - lo)
        v = [float(-(P[i + 1] - P[i]) @ F / (ks[i + 1] - ks[i])) for i in range(len(ks) - 1) if c[i] and c[i + 1]]
        out[foot] = dict(m_s=round(float(np.median(v)), 4) if v else None, intervals=len(v))
    fj = [out[f]['m_s'] for f in FEET[:2] if out[f]['m_s'] is not None]
    tj = [out[f]['m_s'] for f in FEET[2:] if out[f]['m_s'] is not None]
    return dict(clip=clip, keys=int(len(ks)), T_s=round(float(ks[-1]), 4), per_foot=out,
                foot_joints_m_s=round(float(np.mean(fj)), 4) if fj else None, toes_m_s=round(float(np.mean(tj)), 4) if tj else None)


if __name__ == '__main__':
    a = sys.argv[1:]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    m = S17.model(a[0])
    res = []
    for clip in a[1].split(','):
        r = footlock(m, clip); res.append(r)
        p = r['per_foot']
        print("  %-8s %2d keys, T %.4f s | foot-lock: foot joints L %.3f R %.3f -> %.3f m/s | toes L %.3f R %.3f -> %.3f m/s"
              % (clip, r['keys'], r['T_s'], p['LeftFoot']['m_s'], p['RightFoot']['m_s'], r['foot_joints_m_s'],
                 p['LeftToeBase']['m_s'], p['RightToeBase']['m_s'], r['toes_m_s']))
    if outj:
        json.dump(res, open(outj, 'w'), indent=1)
