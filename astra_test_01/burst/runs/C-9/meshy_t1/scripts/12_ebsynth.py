#!/usr/bin/env python3
"""C-9 meshy_t1: propagate the painted keys to the unpainted directions.

    python3 scripts/12_ebsynth.py <state> [--keys <dir>] [--dirs S,SW,...]

The six directions that are not painted in full get two painted KEYS each, and
EbSynth fills the rest, guided by pos (w4), part (w2) and mask (w2) -- the
combination measured at R-C9-60, where 2-key propagation scored 36.5 mean RGB
error against Astra's own per-frame paint, beating the raw render's 56.8 and
the hold-the-key baseline's 78.5, with no drift across twelve frames.

Each target is propagated from BOTH keys and the two results blended by
temporal distance, inside the silhouette only: outside it there is nothing to
blend and averaging would grey the plate.

The guides come from this pipeline's own render, so they register with the
painted cells by construction -- checked anyway before anything is spent, and
the check is cheap: a painted frame whose alpha does not agree with its guide
mask cannot be propagated meaningfully.
"""
import json, os, shutil, subprocess, sys, time
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE)
OUT = os.path.join(T1, "out")
EBS = "/Users/admin/tools/ebsynth/bin/ebsynth"
GUIDES = [("pos", 4.0), ("part", 2.0), ("mask", 2.0)]
ALL = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
PAINTED_FULL = ["E", "SE"]
FRAME = 512


def guide_paths(state, d, i):
    return {
        "pos": os.path.join(OUT, state, "guides_pos", d, "pos_%s_%02d.png" % (d, i)),
        "part": os.path.join(OUT, state, "guides_part", d, "part_%s_%02d.png" % (d, i)),
        "mask": os.path.join(OUT, state, "_mask", d, "mask_%s_%02d.png" % (d, i)),
    }


def ensure_masks(state, dirs, n):
    """The renderer emits colour+pos+part; the mask is the colour pass's alpha."""
    for d in dirs:
        md = os.path.join(OUT, state, "_mask", d)
        os.makedirs(md, exist_ok=True)
        for i in range(n):
            p = os.path.join(md, "mask_%s_%02d.png" % (d, i))
            if os.path.exists(p):
                continue
            src = os.path.join(OUT, state, "colour", d, "%s_%s_%02d.png" % (state, d, i))
            a = np.asarray(Image.open(src).convert("RGBA"))[..., 3] > 8
            Image.fromarray((a * 255).astype(np.uint8)).convert("RGB").save(p)


def flat(path, out):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(out)
    return out


def run_one(style, state, d, src_i, tgt_i, outp):
    cmd = [EBS, "-style", style]
    gs, gt = guide_paths(state, d, src_i), guide_paths(state, d, tgt_i)
    for nm, w in GUIDES:
        cmd += ["-guide", gs[nm], gt[nm], "-weight", str(w)]
    cmd += ["-output", outp, "-backend", "cpu"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-400:])
    return time.time() - t


def main():
    state = sys.argv[1]
    keyroot = sys.argv[sys.argv.index("--keys") + 1] if "--keys" in sys.argv \
        else os.path.join(T1, "paint_keys")
    dirs = sys.argv[sys.argv.index("--dirs") + 1].split(",") if "--dirs" in sys.argv \
        else [d for d in ALL if d not in PAINTED_FULL]
    rj = json.load(open(os.path.join(OUT, state, "render_%s.json" % state)))
    n = rj["frames"]
    ensure_masks(state, dirs, n)
    tmp = os.path.join(OUT, "_ebs_tmp_%s" % state)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    outdir = os.path.join(T1, "ebs_t1", state)
    keys = [0, n // 2]
    rep = {"state": state, "frames": n, "keys": keys, "guides":
           [dict(name=k, weight=w) for k, w in GUIDES], "dirs": {}}
    for d in dirs:
        kp = {}
        for k in keys:
            p = os.path.join(keyroot, state, d, "%s_%s_%02d.png" % (state, d, k))
            if not os.path.exists(p):
                print("  %s %s: missing key %02d (%s)" % (state, d, k, p)); kp = {}; break
            kp[k] = flat(p, os.path.join(tmp, "style_%s_%02d.png" % (d, k)))
        if not kp:
            continue
        # registration check before spending anything
        bad = []
        for k in keys:
            a = np.asarray(Image.open(os.path.join(
                keyroot, state, d, "%s_%s_%02d.png" % (state, d, k))).convert("RGBA"))[..., 3] > 8
            m = np.asarray(Image.open(guide_paths(state, d, k)["mask"]).convert("L")) > 127
            iou = (a & m).sum() / max((a | m).sum(), 1)
            if iou < 0.5:
                bad.append((k, round(float(iou), 3)))
        if bad:
            print("  %s %s: key/guide registration too poor %s -- skipped" % (state, d, bad))
            rep["dirs"][d] = dict(skipped="registration", detail=bad)
            continue
        os.makedirs(os.path.join(outdir, d), exist_ok=True)
        prop, times = {}, []
        for k in keys:
            for i in range(n):
                p = os.path.join(tmp, "p_%s_%02d_%02d.png" % (d, k, i))
                if i == k:
                    shutil.copy(kp[k], p)
                else:
                    times.append(run_one(kp[k], state, d, k, i, p))
                prop[(k, i)] = p
        msrc = os.path.join(OUT, state, "_mask", d)
        for i in range(n):
            dd = {k: min((i - k) % n, (k - i) % n) for k in keys}
            tot = sum(1.0 / max(v, 0.5) for v in dd.values())
            w = {k: (1.0 / max(dd[k], 0.5)) / tot for k in keys}
            acc = np.zeros((FRAME, FRAME, 3), np.float64)
            for k in keys:
                acc += w[k] * np.asarray(Image.open(prop[(k, i)]).convert("RGB"), float)
            m = np.asarray(Image.open(os.path.join(
                msrc, "mask_%s_%02d.png" % (d, i))).convert("L")) > 127
            o = np.zeros((FRAME, FRAME, 4), np.uint8)
            o[..., :3][m] = np.clip(acc[m], 0, 255).astype(np.uint8)
            o[..., 3] = np.where(m, 255, 0)
            Image.fromarray(o).save(os.path.join(outdir, d, "%s_%s_%02d.png" % (state, d, i)))
        rep["dirs"][d] = dict(propagations=len(times),
                              mean_s=round(float(np.mean(times)), 3) if times else 0)
        print("  %s %-3s %2d propagations, %.2f s each" % (state, d, len(times),
                                                           np.mean(times) if times else 0))
    shutil.rmtree(tmp)
    json.dump(rep, open(os.path.join(T1, "work", "ebsynth_%s.json" % state), "w"), indent=1)
    print("wrote", outdir)


if __name__ == "__main__":
    main()
