# Is the run's foot-lock speed a property of the MOTION or of the SAMPLING? (s17, the run re-cut)
#
#   python3 scripts/s17_footlock_check.py <body.glb>[,<body.glb>] walk,run [--json f]
#
# s6_footlock (Blender) samples each clip at the scene's integer frames (24 fps) and takes the
# median backward velocity of a planted foot. On the re-cut run (0.7333 s = 17.6 frames) it
# rounds the range to 18 frames and samples 1/60 s PAST the clip's end, and in any case a run has
# ~10 planted intervals at 24 fps, so the median moves with the sampling phase. This re-derives the
# same estimator in pure glTF (s17_loop_closure's evaluator; world metres, glTF up +Y, she faces +Z)
# at three samplings -- the clip's own keys, 24 fps from 0, and dense (480 fps) -- so the number
# the manifest carries can be chosen by what it measures, not by which sampling it happened to get.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')


def speed(m, clip, times):
    P = {b: np.array([C.globals_at(m, clip, t)[m['nid'][b]][:3, 3] for t in times]) for b in ('LeftFoot', 'RightFoot')}
    v, per = [], {}
    for b, p in P.items():
        y = p[:, 1]; thr = y.min() + 0.25 * (y.max() - y.min())
        vb = [float(-(p[i + 1, 2] - p[i, 2]) / (times[i + 1] - times[i])) for i in range(len(p) - 1) if y[i] < thr and y[i + 1] < thr]
        per[b] = round(float(np.median(vb)), 3) if vb else None; v += vb
    return dict(speed_m_s=round(float(np.median(v)), 3), intervals=len(v),
                iqr_m_s=round(float(np.percentile(v, 75) - np.percentile(v, 25)), 3), per_foot=per)


a = sys.argv[1:]
bodies, clips = a[0].split(","), a[1].split(",")
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
rep = {}
for body in bodies:
    m = C.model(body); rb = rep[os.path.basename(os.path.dirname(os.path.abspath(body))) + "/" + os.path.basename(body)] = {}
    for c in clips:
        if c not in m['anims']:                                     # a Meshy source file: its one clip, by name
            src = [n for n in m['anims'] if c in (n or '').lower()]
            if len(src) != 1:
                continue
            m['anims'][c] = m['anims'][src[0]]
        keys = np.unique(np.round(np.concatenate([v[0] for v in m['anims'][c].values()]), 5))
        T = float(keys.max())
        r = rb[c] = dict(T_s=round(T, 4), keys=len(keys))
        r['at_keys'] = speed(m, c, keys)
        t0 = float(keys.min())                                      # a source clip starts one frame in
        r['at_24fps'] = speed(m, c, np.arange(t0, T + 1e-9, 1 / 24.0))
        r['dense_480'] = speed(m, c, np.linspace(t0, T, int(round((T - t0) * 480)) + 1))
        print("  %-28s %-5s T %.4f  keys(%d) %.3f [%d, IQR %.3f]  24fps %.3f [%d]  dense %.3f [%d, IQR %.3f]"
              % (list(rep)[-1], c, T, len(keys), r['at_keys']['speed_m_s'], r['at_keys']['intervals'], r['at_keys']['iqr_m_s'],
                 r['at_24fps']['speed_m_s'], r['at_24fps']['intervals'], r['dense_480']['speed_m_s'], r['dense_480']['intervals'], r['dense_480']['iqr_m_s']))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
