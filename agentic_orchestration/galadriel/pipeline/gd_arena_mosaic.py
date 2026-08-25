#!/usr/bin/env python3
"""gd_arena_mosaic.py — build the registered arena-footprint mosaic.

Consumes gd-arena-trace-registration.json (sign-corrected here: the masked-NCC
offset t IS the player's displacement, verified by eye against shots 617/620/623
-- arena mass NE of player, N of player, NW of player respectively).

The GD minimap disc is SEMI-TRANSPARENT: outside the mapped arena footprint the
live world view bleeds through, and that bleed differs shot to shot.  The mapped
footprint does not.  A per-pixel MEDIAN over all registered observations
therefore sharpens the footprint and suppresses the bleed.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image

from gd_arena_trace import CAP, SHOTS, MM_CX, MM_CY, MM_CONTENT_R, MM_ARROW_R, MM_TOP_WEDGE

HERE = os.path.dirname(os.path.abspath(__file__))
PAD = int(MM_CONTENT_R) + 4


def disc_rgb(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float64)
    R = int(MM_CONTENT_R) + 2
    x0, y0 = int(round(MM_CX)) - R, int(round(MM_CY)) - R
    sub = im[max(y0, 0):y0 + 2 * R, x0:x0 + 2 * R]
    if sub.shape[0] < 2 * R:                       # disc clipped by frame top
        pad = np.zeros((2 * R - sub.shape[0], 2 * R, 3))
        sub = np.vstack([pad, sub])
        oy = 2 * R - (y0 + 2 * R)                  # rows lost at the top
    else:
        oy = 0
    h, w = sub.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    dx = xx - (MM_CX - x0)
    dy = yy - (MM_CY - max(y0, 0)) - oy
    d = np.hypot(dx, dy)
    m = (d < MM_CONTENT_R) & (d > MM_ARROW_R)
    ang = np.degrees(np.arctan2(dx, -dy))
    m &= ~((d > MM_TOP_WEDGE["rmin"]) & (np.abs(ang) < MM_TOP_WEDGE["half_deg"]))
    return sub, m, dx, dy


def main():
    reg = json.load(open(os.path.join(HERE, "gd-arena-trace-registration.json")))
    # sign correction: printed track was negated
    track = [(-a, -b) for a, b in reg["track_minimap_px"]]

    xs = [t[0] for t in track]; ys = [t[1] for t in track]
    x0, x1 = min(xs) - PAD, max(xs) + PAD
    y0, y1 = min(ys) - PAD, max(ys) + PAD
    W, H = int(x1 - x0) + 1, int(y1 - y0) + 1
    print(f"canvas {W}x{H}  origin(arena 0,0 = shot612 player) at px "
          f"({-x0:.0f},{-y0:.0f})")

    stack = np.full((len(SHOTS), H, W, 3), np.nan)
    for i, n in enumerate(SHOTS):
        sub, m, dx, dy = disc_rgb(os.path.join(CAP, f"Screenshot ({n}).png"))
        px = track[i][0] - x0 + dx
        py = track[i][1] - y0 + dy
        pxi = np.round(px).astype(int); pyi = np.round(py).astype(int)
        ok = m & (pxi >= 0) & (pxi < W) & (pyi >= 0) & (pyi < H)
        stack[i, pyi[ok], pxi[ok]] = sub[ok]

    cnt = np.sum(~np.isnan(stack[:, :, :, 0]), axis=0)
    med = np.nanmedian(stack, axis=0)
    med = np.nan_to_num(med)

    np.save(os.path.join(HERE, "gd-arena-mosaic-med.npy"), med)
    np.save(os.path.join(HERE, "gd-arena-mosaic-cnt.npy"), cnt)
    json.dump(dict(W=W, H=H, ox=float(-x0), oy=float(-y0),
                   track=[[round(a, 2), round(b, 2)] for a, b in track],
                   shots=SHOTS),
              open(os.path.join(HERE, "gd-arena-mosaic-meta.json"), "w"), indent=1)

    img = Image.fromarray(np.clip(med, 0, 255).astype(np.uint8))
    img.resize((W * 3, H * 3), Image.NEAREST).save(
        os.path.join(HERE, "gd-arena-mosaic.png"))
    print("coverage: pixels seen >=1:", int((cnt >= 1).sum()),
          " >=3:", int((cnt >= 3).sum()), " max obs:", int(cnt.max()))


if __name__ == "__main__":
    main()
