# How does each shipped clip's time window sit on its Meshy source? (s17, the walk dispatch, 2026-09-30)
#
#   python3 scripts/s17_clip_windows.py <body.glb> <clip>=<source.glb> [...] [--loops idle,walk,run] [--json f]
#
# The D7 merge baked every clip at 24 fps from t = 0 with shipped time = source time, and every Meshy source's
# keys start one 30 fps frame in (0.0333). So a clip that was not re-cut begins with a HOLD -- the source's
# first pose, clamped, until its first key -- and may end before (a CUT) or exactly at the source's last key.
# Per clip:
#   alignment        which time map the export follows, MEASURED: joints in the hips' own frame / hips-to-head
#                    (s16's measure), export against source at shift 0 and at shift = the source's first key;
#                    the smaller median wins. A clip that barely moves (the idle) can fit both: said so.
#   hold_at_start    how long the export shows the clamped first pose before the source's motion begins
#   first_interval_speed   the share of the export's first key interval that carries motion (1 = none held):
#                    a hold h inside a first interval d plays that interval at (d - h) / d of real speed
#   cut_at_end       how much of the source's end the export leaves out (0 = none)
#   closure          loops only: pose(0) against pose(T), every skin joint, world metres
# Pure glTF evaluation (s17_loop_closure's evaluator).
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')

a = sys.argv[1:]
BODY = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
LOOPS = set((a[a.index('--loops') + 1] if '--loops' in a else "idle,walk,run").split(","))
pairs = [x.split("=", 1) for x in a[1:] if "=" in x and not x.startswith("--")]
m = C.model(BODY)
JOINTS = ["Spine02", "Head", "LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand",
          "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot"]


def keys(mm, clip):
    return np.unique(np.round(np.concatenate([v[0] for v in mm['anims'][clip].values()]), 5))


def rel(mm, clip, t):
    G = C.globals_at(mm, clip, t)
    Hi = np.linalg.inv(G[mm['nid']['Hips']])
    return np.array([(Hi @ G[mm['nid'][j]])[:3, 3] for j in JOINTS])


def span(mm, clip):
    G = C.globals_at(mm, clip, 0.0)
    return float(np.linalg.norm((np.linalg.inv(G[mm['nid']['Hips']]) @ G[mm['nid']['Head']])[:3, 3]))


rep = {}
for clip, src in pairs:
    ms = C.model(src)
    sclip = next(iter(ms['anims']))
    ek, sk = keys(m, clip), keys(ms, sclip)
    efps, sfps = 1.0 / float(np.median(np.diff(ek))), 1.0 / float(np.median(np.diff(sk)))
    he, hs = span(m, clip), span(ms, sclip)
    tt = ek[::max(1, len(ek) // 24)]
    errs = {}
    for sh in (0.0, float(sk[0] - ek[0])):
        e = [float(np.max(np.linalg.norm(rel(m, clip, t) / he - rel(ms, sclip, min(max(t + sh, sk[0]), sk[-1])) / hs, axis=1))) for t in tt]
        errs[round(sh, 4)] = float(np.median(e))
    best = min(errs, key=errs.get)
    other = max(errs, key=errs.get)
    ambiguous = errs[other] - errs[best] < 0.002
    r = dict(source=os.path.basename(src),
             export_keys=dict(first=round(float(ek[0]), 4), last=round(float(ek[-1]), 4), count=len(ek), fps=round(efps, 2)),
             source_keys=dict(first=round(float(sk[0]), 4), last=round(float(sk[-1]), 4), count=len(sk), fps=round(sfps, 2)),
             alignment_error_by_shift={"%.4f" % k: round(v, 4) for k, v in errs.items()},
             alignment=("ambiguous: the clip moves too little to tell the two time maps apart" if ambiguous else
                        ("shipped time = source time (the D7 merge)" if best == 0.0 else "re-cut: shipped 0 = the source's first key")))
    if best != 0.0 and not ambiguous:
        r.update(hold_at_start=0.0, cut_at_end=round(float((sk[-1] - sk[0]) - ek[-1]), 4))
    else:
        r.update(hold_at_start=round(float(max(0.0, sk[0] - ek[0])), 4), cut_at_end=round(float(sk[-1] - ek[-1]), 4))
    d1 = float(ek[1] - ek[0])
    r["first_interval_s"] = round(d1, 4)
    r["first_interval_speed"] = round(max(0.0, d1 - r["hold_at_start"]) / d1, 3)
    if clip in LOOPS:
        T = float(max(v[0].max() for v in m['anims'][clip].values()))     # the exact last key, not the 5-decimal one
        G0, G1 = C.globals_at(m, clip, 0.0), C.globals_at(m, clip, T)
        r["closure_worst_joint_m"] = round(float(max(np.linalg.norm(G0[j][:3, 3] - G1[j][:3, 3]) for j in m['joints'])), 5)
    rep[clip] = r
    print("  %-14s export %.4f..%.4f (%2d @ %2.0f fps) | source %.4f..%.4f (%3d @ %2.0f fps) | %-44s hold %.4f -> first interval x%.2f, cut %.4f%s"
          % (clip, ek[0], ek[-1], len(ek), efps, sk[0], sk[-1], len(sk), sfps, r["alignment"][:44], r["hold_at_start"],
             r["first_interval_speed"], r["cut_at_end"], ("  closure %.4f m" % r["closure_worst_joint_m"]) if clip in LOOPS else ""))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
