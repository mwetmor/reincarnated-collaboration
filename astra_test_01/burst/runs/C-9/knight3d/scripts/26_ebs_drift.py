#!/usr/bin/env python3
"""C-9 knight3d: does EbSynth propagation DRIFT? (R-C9-60)

Astra painted all twelve walk frames, so there is a per-frame ground truth for
what the propagation is trying to reproduce. That turns "does it smear" from a
judgement into a measurement: per frame, the mean absolute colour error inside
the silhouette between each propagation and Astra's own paint of that frame.

Reported against two references, because either alone would mislead:
  vs ASTRA       how far from what an artist would have painted.
  vs the KEY     how far from frame 00 itself, so the curve can be read as
                 drift rather than as the pose simply changing. A propagation
                 that merely copied the key would score 0 on the second and
                 badly on the first.
The 3D raw render is scored the same way as the floor: propagation has to beat
the thing it is replacing.
"""
import json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out")


def rgb(p):
    return np.asarray(Image.open(p).convert("RGB"), dtype=np.float64)


def main():
    gait = sys.argv[1] if len(sys.argv) > 1 else "walk"
    gdir = os.path.join(OUT, "guides_fit", gait, "E")
    astra = os.path.join(OUT, "sprites_fit_astra_a", gait, "E")
    ebs = os.path.join(OUT, "ebs_fit", gait, "E")
    raw = os.path.join(OUT, "sprites_fit", gait, "E")
    N = len([f for f in os.listdir(gdir) if f.startswith("mask_")])
    rows = []
    for i in range(N):
        m = np.asarray(Image.open(os.path.join(gdir, "mask_%02d.png" % i))
                       .convert("L")) > 127
        # every image flattened on black so the comparison is of pixels only
        def flat(p):
            im = Image.open(p).convert("RGBA")
            bg = Image.new("RGBA", im.size, (0, 0, 0, 255)); bg.alpha_composite(im)
            return np.asarray(bg.convert("RGB"), dtype=np.float64)
        A = flat(os.path.join(astra, "%s_E_%02d.png" % (gait, i)))
        K = flat(os.path.join(astra, "%s_E_00.png" % gait))
        R = flat(os.path.join(raw, "%s_E_%02d.png" % (gait, i)))
        e = {}
        for tag, path in (("k1", os.path.join(ebs, "k1_%02d.png" % i)),
                          ("k2", os.path.join(ebs, "k2_%02d.png" % i))):
            if os.path.exists(path):
                P = rgb(path)
                e[tag + "_vs_astra"] = float(np.abs(P[m] - A[m]).mean())
                e[tag + "_vs_key00"] = float(np.abs(P[m] - K[m]).mean())
        e["raw3d_vs_astra"] = float(np.abs(R[m] - A[m]).mean())
        e["key00_vs_astra"] = float(np.abs(K[m] - A[m]).mean())
        rows.append(dict(frame=i, **{k: round(v, 2) for k, v in e.items()}))
    hdr = ["frame", "k1_vs_astra", "k2_vs_astra", "raw3d_vs_astra",
           "key00_vs_astra", "k1_vs_key00"]
    print("  mean |RGB| error inside the silhouette (0-255)")
    print("  " + "  ".join("%-14s" % h for h in hdr))
    for r in rows:
        print("  " + "  ".join("%-14s" % (r.get(h, "-")) for h in hdr))
    means = {h: round(float(np.mean([r[h] for r in rows if h in r])), 2)
             for h in hdr[1:]}
    print("  " + "%-14s" % "MEAN" + "  ".join("%-14s" % means[h] for h in hdr[1:]))
    out = dict(note=__doc__.strip().splitlines()[0], gait=gait,
               metric="mean absolute RGB error inside the silhouette, 0-255",
               frames=rows, means=means)
    with open(os.path.join(OUT, "ebsynth_drift_%s.json" % gait), "w") as f:
        json.dump(out, f, indent=1)
    print("  wrote", os.path.join(OUT, "ebsynth_drift_%s.json" % gait))


main()
