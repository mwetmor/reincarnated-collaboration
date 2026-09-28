#!/usr/bin/env python3
"""C-9 meshy_t2 step 12: propagate the six two-key directions with EbSynth.

    python3 scripts/16_ebsynth.py <clip> [--variant a|b] [--dirs S,NE,...]
                                         [--force] [--dry-run]

E and SE are painted every frame (D+1) and assembled straight through by
15_assemble.py. The other six directions get two painted keys each (frames 0
and n/2) and EbSynth fills the rest (D+2), guided exactly as the R-C9-60
feasibility test was:

    pos  weight 4    the REST-pose vertex position baked per vertex, so it is
                     invariant to the animation -- "where on the body am I"
    part weight 2    a flat colour per dominant bone group; never lets a hock
                     match an elbow
    mask weight 2    the silhouette

A colour guide cannot carry correspondence -- it says what a pixel LOOKS
like, not what part of the body it IS -- which is why the naive test smeared
within three frames. Same reason these three are used and no fourth.

TWO KEYS, blended by circular temporal distance, so a frame sitting on a key
is entirely that key and a frame halfway between is half of each. Blending
happens inside the silhouette only; outside it there is nothing to blend and
averaging would grey the background.

EbSynth takes no alpha, so every style and guide is flattened on BLACK first
-- composited on anything else the matte colour bleeds into the synthesis at
the figure's edge. The output's alpha comes back from the render's own mask.

Resumable: an output that already exists is skipped unless --force. At about
7.5 s a frame this matters -- a full four-clip pass is 528 EbSynth runs.

--selftest replaces the Astra keys with this pipeline's OWN RENDERED frames.
It paints nothing and needs no Astra: it propagates render frame k to every
other frame through the same guides and then compares the result against the
render that actually exists there. So it answers two questions before any
paint is spent -- does the machinery run end to end (binary, guide flattening,
blend, alpha, file layout), and does pos/part/mask correspondence hold on a
QUADRUPED, which is the generality T2 exists to test. The knight's equivalent
scored 36.5 mean absolute error against 56.8 for an unguided propagation.
"""
import argparse, json, os, shutil, subprocess, sys, time
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
SPR = os.path.join(ROOT, "sprites_t2")
WORK = os.path.join(ROOT, "work", "ebs")
EBS = "/Users/admin/tools/ebsynth/bin/ebsynth"
GUIDES = [("pos", 4.0), ("part", 2.0), ("mask", 2.0)]
KEY_DIRS = ["S", "NE", "N", "NW", "W", "SW"]
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}
FRAME = 512


def flat(src, dst):
    im = Image.open(src).convert("RGBA")
    bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(dst)
    return dst


def guide_path(clip, d, i):
    return {
        "pos": os.path.join(OUT, clip, "guides_pos", d, "pos_%s_%02d.png" % (d, i)),
        "part": os.path.join(OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i)),
        "mask": os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i)),
    }


def prep_guides(clip, d, n, tmp):
    """Flatten every guide once per direction; EbSynth reads them repeatedly."""
    os.makedirs(tmp, exist_ok=True)
    got = {}
    for i in range(n):
        gp = guide_path(clip, d, i)
        for nm, _w in GUIDES:
            src = gp[nm]
            if not os.path.exists(src):
                return None
            got[(nm, i)] = flat(src, os.path.join(tmp, "%s_%02d.png" % (nm, i)))
    return got


def run_one(style, g, src_i, tgt_i, outp):
    cmd = [EBS, "-style", style]
    for nm, w in GUIDES:
        cmd += ["-guide", g[(nm, src_i)], g[(nm, tgt_i)], "-weight", str(w)]
    cmd += ["-output", outp, "-backend", "cpu"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-400:] or r.stdout.decode()[-400:])
    return time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", choices=sorted(CLIPS))
    ap.add_argument("--variant", default=None,
                    help="paint_<variant>; default reads work/chosen.json")
    ap.add_argument("--dirs", default=",".join(KEY_DIRS))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="use the RENDER as the style instead of Astra paint, "
                         "and score the propagation against the true render")
    args = ap.parse_args()
    clip = args.clip
    n = CLIPS[clip]
    keys = [0, n // 2]
    dirs = args.dirs.split(",")

    variant = args.variant
    if args.selftest:
        variant = "__render__"
    elif variant is None:
        ch = json.load(open(os.path.join(ROOT, "work", "chosen.json")))
        variant = (ch.get(clip) or {}).get("keys")
        if variant is None:
            raise SystemExit("no keys variant chosen for %s; pass --variant "
                             "or set chosen.json[%r]['keys']" % (clip, clip))
    paint = (os.path.join(OUT) if args.selftest
             else os.path.join(ROOT, "paint_%s" % variant))

    def style_src(d, k):
        if args.selftest:
            return os.path.join(OUT, clip, "colour", d, "%s_%s_%02d.png" % (clip, d, k))
        return os.path.join(paint, clip, d, "%s_%s_%02d.png" % (clip, d, k))

    rep = dict(clip=clip, variant=variant, frames=n, keys=keys,
               guides=[dict(name=nm, weight=w) for nm, w in GUIDES],
               alpha_source="out/<clip>/guides_mask (the render's own silhouette); "
                            "the painted keys' silhouette drifts ~5 % from it and "
                            "that drift is deliberately NOT carried into the "
                            "propagated directions, so all eight stay aligned",
               dirs={})
    missing = []
    for d in dirs:
        for k in keys:
            p = style_src(d, k)
            if not os.path.exists(p):
                missing.append(os.path.relpath(p, ROOT))
    if missing:
        print("MISSING painted keys (%d):" % len(missing))
        for m in missing[:12]:
            print("   ", m)
        if args.dry_run:
            return
        raise SystemExit("cut back the key sheets first")
    if args.dry_run:
        print("all %d painted keys present for %s (variant %s); "
              "%d EbSynth runs would fire"
              % (len(dirs) * len(keys), clip, variant,
                 len(dirs) * len(keys) * (n - 1)))
        return

    total_t = 0.0
    for d in dirs:
        tmp = os.path.join(WORK, clip, d)
        g = prep_guides(clip, d, n, tmp)
        if g is None:
            print("  %s %s: guides missing, skipped" % (clip, d)); continue
        styles = {k: flat(style_src(d, k),
                          os.path.join(tmp, "style_%02d.png" % k)) for k in keys}
        prop, times = {}, {}
        for k in keys:
            for i in range(n):
                p = os.path.join(tmp, "p%02d_%02d.png" % (k, i))
                if i == k:
                    shutil.copy(styles[k], p); prop[(k, i)] = p; continue
                if os.path.exists(p) and not args.force:
                    prop[(k, i)] = p; continue
                times[(k, i)] = run_one(styles[k], g, k, i, p)
                prop[(k, i)] = p
                total_t += times[(k, i)]
        dd = (os.path.join(ROOT, "work", "ebs_selftest", clip, d) if args.selftest
              else os.path.join(SPR, clip, d))
        os.makedirs(dd, exist_ok=True)
        ious = []
        for i in range(n):
            dist = {k: min((i - k) % n, (k - i) % n) for k in keys}
            tot = sum(1.0 / max(v, 0.5) for v in dist.values())
            w = {k: (1.0 / max(dist[k], 0.5)) / tot for k in keys}
            acc = np.zeros((FRAME, FRAME, 3), np.float64)
            for k in keys:
                acc += w[k] * np.asarray(Image.open(prop[(k, i)]).convert("RGB"),
                                         dtype=np.float64)
            m = np.asarray(Image.open(guide_path(clip, d, i)["mask"])
                           .convert("RGBA").getchannel("A")) > 128
            rgba = np.zeros((FRAME, FRAME, 4), np.uint8)
            rgba[..., :3][m] = np.clip(acc[m], 0, 255).astype(np.uint8)
            rgba[..., 3][m] = 255
            Image.fromarray(rgba, "RGBA").save(
                os.path.join(dd, "%s_%s_%02d.png" % (clip, d, i)))
            if args.selftest:
                # score against the render that really is at frame i: mean
                # absolute error inside the silhouette, and the same figure
                # for the key held static, which is what "no propagation"
                # would have produced.
                truth = np.asarray(Image.open(style_src(d, i)).convert("RGBA"))
                tr = truth[..., :3].astype(np.float64)
                got = rgba[..., :3].astype(np.float64)
                k0 = np.asarray(Image.open(styles[keys[0]]).convert("RGB"),
                                dtype=np.float64)
                if m.sum():
                    ious.append(dict(frame=i,
                                     mae=round(float(np.abs(got[m] - tr[m]).mean()), 2),
                                     mae_static_key=round(
                                         float(np.abs(k0[m] - tr[m]).mean()), 2)))
        sel = [r for r in ious if isinstance(r, dict)]
        rep["dirs"][d] = dict(
            keys=keys, frames=n,
            selftest=(dict(per_frame=sel,
                           mae_mean=round(float(np.mean([r["mae"] for r in sel])), 2),
                           mae_static_key_mean=round(float(np.mean(
                               [r["mae_static_key"] for r in sel])), 2))
                      if sel else None),
            ebsynth_runs=len(times),
            mean_s=round(float(np.mean(list(times.values()))), 3) if times else None,
            blend="inverse circular temporal distance, inside the mask only",
            out=os.path.relpath(dd, ROOT))
        msg = ""
        if sel:
            msg = ("  MAE %.1f vs %.1f for a static key"
                   % (rep["dirs"][d]["selftest"]["mae_mean"],
                      rep["dirs"][d]["selftest"]["mae_static_key_mean"]))
        print("  %-6s %-3s  %2d runs  mean %.2f s  -> %s%s"
              % (clip, d, len(times),
                 float(np.mean(list(times.values()))) if times else 0.0,
                 os.path.relpath(dd, ROOT), msg))
    rep["total_ebsynth_s"] = round(total_t, 1)
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    json.dump(rep, open(os.path.join(
        ROOT, "work", "ebsynth_%s%s.json" % (clip, "_selftest" if args.selftest else "")),
        "w"), indent=1)
    print("%s: %d directions, %.0f s of EbSynth" % (clip, len(rep["dirs"]), total_t))


if __name__ == "__main__":
    main()
