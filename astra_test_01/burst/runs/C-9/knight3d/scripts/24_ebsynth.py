#!/usr/bin/env python3
"""C-9 knight3d: EbSynth propagation feasibility test (R-C9-60).

    python3 scripts/24_ebsynth.py [walk]

The naive test smeared within three frames because a COLOUR guide says what a
pixel looks like, not what part of the body it is. These guides say where each
pixel comes from -- object-space bind position (weight 4), piece id (2) and
silhouette (2) -- so a patch is matched by its place on the knight rather than
by its shade.

Two variants:
  1-KEY  every frame propagated from the single Astra keyframe 00.
  2-KEY  keys at 00 and 06; each target is propagated from BOTH and the two
         results blended by TEMPORAL DISTANCE, so a frame halfway between the
         keys is half of each and a frame on a key is entirely that key. The
         blend is done inside the silhouette only; outside it there is nothing
         to blend and averaging would grey the background.

The style image is flattened on black first: EbSynth takes no alpha, and
composited on anything else the matte colour bleeds into the synthesis at the
figure's edge.
"""
import json, os, shutil, subprocess, sys, time
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out")
EBS = "/Users/admin/tools/ebsynth/bin/ebsynth"
GUIDES = [("pos", 4.0), ("part", 2.0), ("mask", 2.0)]
TMP = os.path.join(OUT, "_ebs_tmp")


def flat(path, out):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(out)
    return out


def run_one(style, gdir, src_i, tgt_i, outp):
    cmd = [EBS, "-style", style]
    for nm, w in GUIDES:
        cmd += ["-guide", os.path.join(gdir, "%s_%02d.png" % (nm, src_i)),
                os.path.join(gdir, "%s_%02d.png" % (nm, tgt_i)), "-weight", str(w)]
    cmd += ["-output", outp, "-backend", "cpu"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True)
    dt = time.time() - t
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-500:] or r.stdout.decode()[-500:])
    return dt


def main():
    gait = sys.argv[1] if len(sys.argv) > 1 else "walk"
    gdir = os.path.join(OUT, "guides_fit", gait, "E")
    astra = os.path.join(OUT, "sprites_fit_astra_a", gait, "E")
    outdir = os.path.join(OUT, "ebs_fit", gait, "E")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    N = len([f for f in os.listdir(gdir) if f.startswith("mask_")])
    keys = [0, 6] if N >= 8 else [0]

    styles = {}
    for k in keys:
        src = os.path.join(astra, "%s_E_%02d.png" % (gait, k))
        if not os.path.exists(src):
            raise SystemExit("missing Astra key: " + src)
        styles[k] = flat(src, os.path.join(TMP, "style_%02d.png" % k))

    rep = {"note": __doc__.strip().splitlines()[0], "gait": gait, "frames": N,
           "guides": [dict(name=n, weight=w) for n, w in GUIDES],
           "keys_1key": [0], "keys_2key": keys, "timing": []}

    # ---- 1-key ---------------------------------------------------------
    per = {}
    for i in range(N):
        dst = os.path.join(outdir, "k1_%02d.png" % i)
        if i == 0:
            shutil.copy(styles[0], dst); per[i] = 0.0
            continue
        per[i] = run_one(styles[0], gdir, 0, i, dst)
        print("  1-key %02d  %.2f s" % (i, per[i]))
    rep["timing"].append(dict(variant="1key", per_frame_s={str(k): round(v, 3)
                                                          for k, v in per.items()},
                              mean_s=round(float(np.mean([v for v in per.values() if v])), 3)))

    # ---- 2-key ---------------------------------------------------------
    if len(keys) > 1:
        prop = {}
        t2 = {}
        for k in keys:
            for i in range(N):
                p = os.path.join(TMP, "p%02d_%02d.png" % (k, i))
                if i == k:
                    shutil.copy(styles[k], p); prop[(k, i)] = p; continue
                t2[(k, i)] = run_one(styles[k], gdir, k, i, p)
                prop[(k, i)] = p
                print("  2-key from %02d -> %02d  %.2f s" % (k, i, t2[(k, i)]))
        for i in range(N):
            # circular temporal distance to each key
            d = {k: min((i - k) % N, (k - i) % N) for k in keys}
            tot = sum(1.0 / max(v, 0.5) for v in d.values())
            w = {k: (1.0 / max(d[k], 0.5)) / tot for k in keys}
            acc = np.zeros((512, 512, 3), np.float64)
            for k in keys:
                acc += w[k] * np.asarray(Image.open(prop[(k, i)]).convert("RGB"),
                                         dtype=np.float64)
            m = np.asarray(Image.open(os.path.join(gdir, "mask_%02d.png" % i))
                           .convert("L")) > 127
            outimg = np.zeros((512, 512, 3), np.uint8)
            outimg[m] = np.clip(acc[m], 0, 255).astype(np.uint8)
            Image.fromarray(outimg).save(os.path.join(outdir, "k2_%02d.png" % i))
        rep["timing"].append(dict(variant="2key",
                                  per_pair_s={"%d->%d" % k: round(v, 3)
                                              for k, v in t2.items()},
                                  mean_s=round(float(np.mean(list(t2.values()))), 3),
                                  total_s=round(float(np.sum(list(t2.values()))), 3)))
    with open(os.path.join(OUT, "ebsynth_%s.json" % gait), "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote", outdir)


if __name__ == "__main__":
    main()
