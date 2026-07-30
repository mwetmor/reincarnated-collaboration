#!/usr/bin/env python3
"""GAL-CAM: FULL-FRAME nova-projectile head census.

WHY A SECOND DETECTOR
---------------------
wr3_ring.py (GAL-3) ran inside a x[300,1500] y[200,1000] window. That window was
correct for GAL-3's question -- the compact ring at the damage frame -- but it
CLIPS the mature ring: at 12 m and ~63 px/m the ring reaches rho ~ 760 px, i.e.
x in [265,1785] and y in [25,1115]. Every far head was cut.

GAL-CAM needs exactly those far heads: the perspective signal (is this camera
orthographic or pinhole?) lives entirely in the LARGE-radius behaviour. So the
mask rule is kept VERBATIM from wr3_ring (gal2's cold rule + brightness floor),
and only the spatial window changes -- full frame, minus the two HUD bands whose
cold pixels are UI, not projectiles.

Excluded bands (measured from the frames, not assumed):
  y >= 940   -- skill bar / globes / belt
  y <= 30    -- top edge letterbox + boss plate glow
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


def cold_mask(a, bmin=150, brmin=60, gtol=12):
    """gal2's cold rule, verbatim."""
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (B > bmin) & ((B - R) > brmin) & (B >= G - gtol)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, required=True)
    ap.add_argument("--f1", type=int, required=True)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--minpx", type=int, default=8)
    ap.add_argument("--ytop", type=int, default=30)
    ap.add_argument("--ybot", type=int, default=940)
    args = ap.parse_args()

    rows = []
    for f in range(args.f0, args.f1 + 1):
        p = os.path.join(args.root, f"f{f:06d}.png")
        if not os.path.exists(p):
            continue
        a = np.asarray(Image.open(p).convert("RGB")).astype(np.int16)
        cm = cold_mask(a)
        head = cm & (a[:, :, 2] > args.bright)
        head[: args.ytop] = False
        head[args.ybot:] = False
        lab, n = ndimage.label(head)
        bl = []
        if n:
            sizes = ndimage.sum(head, lab, range(1, n + 1))
            coms = ndimage.center_of_mass(head, lab, range(1, n + 1))
            for i in range(n):
                if sizes[i] >= args.minpx:
                    bl.append(dict(n=int(sizes[i]),
                                   cx=float(coms[i][1]), cy=float(coms[i][0])))
        bl.sort(key=lambda d: -d["n"])
        rows.append(dict(f=f, n_head=int(head.sum()), blobs=bl[:80]))
        print(f, int(head.sum()), len(bl), flush=True)
    json.dump(dict(f0=args.f0, f1=args.f1, rows=rows), open(args.out, "w"))


if __name__ == "__main__":
    main()
