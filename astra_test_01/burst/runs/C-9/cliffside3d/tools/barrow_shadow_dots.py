#!/usr/bin/env python3
"""C-9 T10-1d -- THE SHADOW'S DOT SCREEN, measured before and after.

    python3 barrow_shadow_dots.py --before B.png --after A.png [--region x0,y0,x1,y1 ...] --out OUT.json

A regular 2-px dot grid is energy at the Nyquist checkerboard: per 2x2 block, |a - b - c + d| / 4
on luma. That is what the halftone along the shadow edges was (T10-1c, isolated by toggles in
one run: sun shadows off -> gone), so it is the instrument: the same frame, the cast shadow
applied before the bands (T10-1c's ramp) and after them (T10-1d's), measured over the whole
frame and over named regions -- the mound's flank at the painting's framing is where it was
found (x 850-960, y 15-75).

Checked on its own known cases first: a frame against itself is identical by construction, and
a synthetic 2-px checker must read far above a smooth ramp.
"""
import argparse
import json

import numpy as np
from PIL import Image


def checker(luma):
    h, w = luma.shape
    a = luma[:h - h % 2:2, :w - w % 2:2]
    b = luma[:h - h % 2:2, 1:w - w % 2:2]
    c = luma[1:h - h % 2:2, :w - w % 2:2]
    d = luma[1:h - h % 2:2, 1:w - w % 2:2]
    return np.abs(a - b - c + d) / 4.0


def luma(path):
    return np.asarray(Image.open(path).convert("L"), np.float64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--region", action="append", default=[], help="NAME=x0,y0,x1,y1")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lb, la = luma(a.before), luma(a.after)
    ramp = np.tile(np.linspace(0, 255, 256), (256, 1))
    cb = np.indices((256, 256)).sum(0) % 2 * 255.0
    rep = {"instrument_check": {"smooth_ramp": round(float(checker(ramp).mean()), 3),
                                "two_px_checker": round(float(checker(cb).mean()), 3),
                                "_expect": "the checker far above the ramp"}}
    cbm, cam = checker(lb), checker(la)
    rep["whole_frame"] = {"before": round(float(cbm.mean()), 3), "after": round(float(cam.mean()), 3),
                          "p99_before": round(float(np.percentile(cbm, 99)), 2),
                          "p99_after": round(float(np.percentile(cam, 99)), 2)}
    for spec in a.region:
        nm, box = spec.split("=", 1)
        x0, y0, x1, y1 = [int(v) for v in box.split(",")]
        rep[nm] = {"box": [x0, y0, x1, y1],
                   "before": round(float(checker(lb[y0:y1, x0:x1]).mean()), 3),
                   "after": round(float(checker(la[y0:y1, x0:x1]).mean()), 3)}
    open(a.out, "w").write(json.dumps(rep, indent=1))
    print(json.dumps(rep))


if __name__ == "__main__":
    main()
