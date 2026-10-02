# COPIED from so_d7/scripts for R-C9-119 (read-only there): also measures cast_fireball_m.
# RELEASE_S RE-DERIVED ON THE SHIPPED CLIP'S OWN KEYS (the sorceress v2, conductor 2026-09-30: "re-derive release_s from
# the re-cut clips; it lands on the source grid -- don't copy 0.9167 or 1.625").
#
#   python3 scripts/s18_release.py <body.glb>[,<body.glb>...] [--sources cast_fireball=a.glb,cast_meteor=b.glb] [--json f]
#
# --sources: the same estimators on the Meshy files, on THEIR clock (keys from 0.0333), and mapped to a re-cut's clock
# (source time - the source's first key) -- the re-cut clip and its source must agree to the key.
#
# The estimators are s5_casts.py's, unchanged in what they measure:
#   FIRE BALL  a THROW: the leading hand's peak FORWARD speed; release_s = the key that ENDS the fastest interval
#   METEOR     a CALL-DOWN: the hand's highest point above the head, then the fastest DOWNWARD interval after it;
#              release_s = the key that ends that interval; the hand = the better (height x drop) of the two
# What changes is WHERE they are read. s5 read Meshy's source files in Blender at the scene's 24 fps integer frames, and
# counted time from frame 1 -- the source's first key sits at frame 0.8, rounded -- so its release_s was measured on a
# clock that starts 1/24 s late, and landed on a 24 fps grid. This reads the SHIPPED clip in pure glTF (s17_loop_closure's
# evaluator), at its own keys, on the clip's own clock: the number the scene and the renderer use is the number measured.
# glTF world metres: +Y up, she faces +Z.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/wl_e1/scripts")
C = __import__('s17_loop_closure')
a = sys.argv[1:]
BODIES = a[0].split(",")
OUTJ = a[a.index('--json') + 1] if '--json' in a else None


def keys(m, clip):
    return np.unique(np.round(np.concatenate([v[0] for v in m['anims'][clip].values()]), 6))


def track(m, clip):
    t = keys(m, clip)
    P = {b: [] for b in ("Spine", "Head", "LeftHand", "RightHand")}
    for x in t:
        G = C.globals_at(m, clip, float(x))
        for b in P:
            P[b].append(G[m['nid'][b]][:3, 3].copy())
    return t, {b: np.array(v) for b, v in P.items()}


def throw(t, P):
    best = None
    for hand, nm in (("L", "LeftHand"), ("R", "RightHand")):
        vf = np.diff(P[nm][:, 2]) / np.diff(t)                          # forward = +Z
        i = int(np.argmax(vf))
        rec = dict(hand=hand, peak_fwd_speed=round(float(vf[i]), 3), interval_s=[round(float(t[i]), 4), round(float(t[i + 1]), 4)],
                   release_s=round(float(t[i + 1]), 4), release_key=i + 1)
        if best is None or rec["peak_fwd_speed"] > best["peak_fwd_speed"]:
            best = rec
    return best


def call(t, P):
    best = None
    for hand, nm in (("L", "LeftHand"), ("R", "RightHand")):
        rise = P[nm][:, 1] - P["Head"][:, 1]
        ip = int(np.argmax(rise))
        vz = np.diff(P[nm][:, 1]) / np.diff(t)
        j = int(np.argmin(vz[ip:])) + ip if ip < len(vz) else len(vz) - 1
        drop = float(-vz[j])
        rec = dict(hand=hand, peak_above_head_m=round(float(rise[ip]), 4), peak_s=round(float(t[ip]), 4),
                   peak_down_speed=round(drop, 3), interval_s=[round(float(t[j]), 4), round(float(t[j + 1]), 4)],
                   release_s=round(float(t[j + 1]), 4), release_key=j + 1, score=round(max(rise[ip], 0) * max(drop, 0), 4))
        if best is None or rec["score"] > best["score"]:
            best = rec
    return best


out = {}
for body in BODIES:
    m = C.model(body)
    r = {}
    # R-C9-119: also the MIRRORED Fire Ball (the wand hand throws) when the body carries it
    for clip, fn in [(c, f) for c, f in (("cast_fireball", throw), ("cast_fireball_m", throw), ("cast_meteor", call)) if c in m['anims']]:
        t, P = track(m, clip)
        rec = fn(t, P)
        rec.update(keys=len(t), fps=round(1.0 / float(np.median(np.diff(t))), 2), duration_s=round(float(t[-1]), 4))
        r[clip] = rec
        print("  %-28s %-14s %s hand, %s at %.4f s (key %d of %d, %.0f fps)%s"
              % (os.path.relpath(body), clip, rec["hand"],
                 ("peak forward %.2f m/s" % rec["peak_fwd_speed"]) if "peak_fwd_speed" in rec else
                 ("%.3f m over the head at %.4f s, then down %.2f m/s" % (rec["peak_above_head_m"], rec["peak_s"], rec["peak_down_speed"])),
                 rec["release_s"], rec["release_key"], rec["keys"], rec["fps"], ""))
    out[os.path.relpath(body)] = r
SRCS = dict(x.split("=", 1) for x in a[a.index('--sources') + 1].split(",")) if '--sources' in a else {}
FN = {"cast_fireball": throw, "cast_meteor": call}
for clip, src in SRCS.items():
    m = C.model(src); sc = next(iter(m['anims']))
    t, P = track(m, sc); rec = FN[clip](t, P)
    rec.update(keys=len(t), first_key_s=round(float(t[0]), 4), release_on_recut_clock_s=round(float(t[rec["release_key"]] - t[0]), 4))
    out.setdefault("sources", {})[clip] = dict(rec, file=os.path.relpath(src))
    print("  source %-21s %-14s %s hand, release at SOURCE time %.4f (key %d) -> %.4f on a re-cut's clock"
          % (os.path.relpath(src), clip, rec["hand"], rec["release_s"], rec["release_key"], rec["release_on_recut_clock_s"]))
if OUTJ:
    json.dump(out, open(OUTJ, "w"), indent=1)
