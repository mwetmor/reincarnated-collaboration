#!/usr/bin/env python3
"""eor_plate_fill.py — read the hovered-monster nameplate's health-bar fill fraction.

galadriel / visual-perception seam. KC2-SIM Phase-C third-extraction pass.

The plate's bar track runs x 800..1125 at rows 57..67 (1920x1080). The filled
part is saturated red; the empty part is a dark blue-grey. The red level numeral
is drawn OVER the track and contaminates naive column profiles, so the numeral
band (x 915..1005) is excluded from the profile and the fill edge is taken as the
last red column before a sustained run of non-red columns.

Accuracy is +-2..3 percentage points; that is what ~325 px of red-on-red at 1080p
supports and it is not upgraded past it.
"""
from __future__ import annotations

import numpy as np
from PIL import Image

TRACK = (800, 1125)
ROWS = (57, 68)
LVL_COLS = (915, 1006)


def fill(path_or_img, rows=ROWS, track=TRACK, exclude_lvl=True):
    im = path_or_img
    if isinstance(im, str):
        im = Image.open(im)
    a = np.asarray(im.convert("RGB")).astype(int)
    band = a[rows[0]:rows[1], track[0]:track[1]]
    R, G, B = band[:, :, 0], band[:, :, 1], band[:, :, 2]
    red = (R > 70) & (R - G > 28) & (R - B > 28)
    col = red.mean(0)
    if exclude_lvl:
        col = col.copy()
        col[LVL_COLS[0] - track[0]:LVL_COLS[1] - track[0]] = np.nan
    n = len(col)
    # walk from the right; the fill edge is the rightmost index whose local
    # window is predominantly red
    W = 5
    edge = 0
    for i in range(n - 1, -1, -1):
        w = col[max(0, i - W):i + W + 1]
        w = w[~np.isnan(w)]
        if w.size and w.mean() > 0.5:
            edge = i
            break
    return dict(frac=round(100.0 * (edge + 1) / n, 1), edge_px=int(edge),
                track_px=n,
                profile=[None if np.isnan(v) else round(float(v), 2) for v in col])


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        r = fill(p)
        print(p, r["frac"], "%", r["edge_px"], "/", r["track_px"])
