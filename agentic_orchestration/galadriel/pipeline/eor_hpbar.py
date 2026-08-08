#!/usr/bin/env python3
"""eor_hpbar.py — locate Grim Dawn in-world monster health bars in a frame.

galadriel / visual-perception seam.

Signature learned from a known full-health nemesis bar (s2 t=841.0, wave 160):
  * solid red, mean RGB ~ (176, 17, 13)
  * exactly 3-6 rows tall
  * 10-90 px wide horizontal run
  * dark rows immediately above and below (the bar sits on a dark backing plate)

The detector's only job is to say WHERE to look. Every reported count is a
galadriel eye-read of the magnified crops this module emits.
"""
from __future__ import annotations

import numpy as np
from PIL import Image

# Regions excluded from the search (HUD furniture that is also red).
EXCLUDE = [
    (0, 0, 1920, 60),        # top banner strip
    (1300, 0, 1920, 270),    # tribute / hourglass / wave badge / minimap
    (0, 860, 1920, 1080),    # bottom HUD: globes, skill bar
    (0, 0, 300, 140),        # difficulty label + wall clock
]


def _red_mask(a: np.ndarray) -> np.ndarray:
    R = a[:, :, 0].astype(int)
    G = a[:, :, 1].astype(int)
    B = a[:, :, 2].astype(int)
    return (R > 110) & (G < 75) & (B < 75) & (R - G > 65) & (R - B > 65)


def find_bars(path, min_w=10, max_w=95, min_h=3, max_h=7):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    m = _red_mask(a)
    for (x0, y0, x1, y1) in EXCLUDE:
        m[y0:y1, x0:x1] = False

    H, W = m.shape
    # label horizontal runs per row, then stack rows into bars
    runs = {}
    for y in range(H):
        row = m[y]
        if not row.any():
            continue
        idx = np.where(row)[0]
        splits = np.where(np.diff(idx) > 2)[0]
        groups = np.split(idx, splits + 1)
        for g in groups:
            if min_w <= (g[-1] - g[0] + 1) <= max_w:
                runs.setdefault(y, []).append((g[0], g[-1]))

    used = set()
    bars = []
    for y in sorted(runs):
        for (x0, x1) in runs[y]:
            if (y, x0) in used:
                continue
            ys = [y]
            cur = (x0, x1)
            yy = y + 1
            while yy in runs:
                cand = [r for r in runs[yy]
                        if abs(r[0] - cur[0]) <= 3 and abs(r[1] - cur[1]) <= 8]
                if not cand:
                    break
                used.add((yy, cand[0][0]))
                ys.append(yy)
                cur = cand[0]
                yy += 1
            h = len(ys)
            if min_h <= h <= max_h:
                # backing-plate check: rows above/below must be much darker
                ya, yb = ys[0] - 3, ys[-1] + 3
                if ya < 0 or yb >= H:
                    continue
                above = a[ya, x0:x1 + 1].astype(int).mean()
                below = a[yb, x0:x1 + 1].astype(int).mean()
                core = a[ys[0]:ys[-1] + 1, x0:x1 + 1].astype(int)[:, :, 0].mean()
                if above < core - 40 and below < core - 40:
                    bars.append(dict(x0=int(x0), x1=int(x1), y0=int(ys[0]),
                                     y1=int(ys[-1]), w=int(x1 - x0 + 1), h=h))
    return bars


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        b = find_bars(p)
        print(p, len(b), b)
