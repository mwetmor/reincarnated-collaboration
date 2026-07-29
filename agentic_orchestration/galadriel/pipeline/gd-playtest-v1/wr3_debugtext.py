#!/usr/bin/env python3
"""WR1-GAL-3: locate the dev-overlay entity labels (green "[id] Action State: X").

WHY
---
This capture was taken with GD's dev overlay on. Every live entity gets a green
two-line label drawn at a FIXED SCREEN OFFSET from that entity's projected world
origin. That makes the label a rigid positional marker for entities whose sprite
is occluded -- including the player, whose sprite is buried inside the boss's in
the death-2 frames.

The label anchor convention (left-aligned? centred? how far above the ground
point?) is NOT assumed. It is CALIBRATED against the caster, whose ground point
is known independently from the nova-ring centre (wr3_fit3). Whatever offset the
caster's label shows is then applied to the player's label.

Detector: saturated green ink (G>150, G-R>60, G-B>60), 8-16 px tall rows, grouped
into text lines, lines grouped into blocks by vertical proximity.
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


def green_lines(f, root, box=(300, 1750, 300, 900)):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (G > 140) & ((G - R) > 55) & ((G - B) > 55)
    rows = m.sum(axis=1) > 0
    out = []
    run = None
    for i, v in enumerate(rows):
        if v:
            run = [i, i] if run is None else [run[0], i]
        elif run is not None:
            out.append(run)
            run = None
    if run:
        out.append(run)
    lines = []
    for r0, r1 in out:
        h = r1 - r0 + 1
        if not (7 <= h <= 20):
            continue
        band = m[r0:r1 + 1]
        prof = band.sum(axis=0)
        nz = np.nonzero(prof)[0]
        if len(nz) < 10:
            continue
        # split into text runs separated by >25 px of blank
        s, prev, runs = nz[0], nz[0], []
        for x in nz[1:]:
            if x - prev > 25:
                runs.append((s, prev))
                s = x
            prev = x
        runs.append((s, prev))
        for a0, a1 in runs:
            if a1 - a0 < 25:
                continue
            lines.append(dict(x0=int(x0 + a0), x1=int(x0 + a1),
                              y0=int(y0 + r0), y1=int(y0 + r1),
                              ink=int(band[:, a0:a1 + 1].sum())))
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, nargs="+", required=True)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = {}
    for f in args.frames:
        ls = green_lines(f, args.root)
        res[str(f)] = ls
        print("f", f)
        for l in sorted(ls, key=lambda d: (d["y0"], d["x0"])):
            print(f"   x[{l['x0']:5d}-{l['x1']:5d}] y[{l['y0']:4d}-{l['y1']:4d}] ink={l['ink']}")
    json.dump(res, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
