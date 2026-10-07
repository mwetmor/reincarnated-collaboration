#!/usr/bin/env python3
"""BV2F LV 0.2: measure sketch A's anchor patch centres (BV3r2-A_spawns.png) by fitting an ellipse to each
patch's outline colour (gold 196,140,40; p05's blue ring) -- the patch centre IS the anchor (legend: "gold
patch = where bodies appear (8 m around each point)"); the dots are the delivering doors, not anchors.
Writes frame_proof/sketch_anchor_px.json."""
import json, os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
im = np.asarray(Image.open(os.path.join(HERE, "..", "..", "sites", "BV3r2-A_spawns.png")).convert("RGB")).astype(int)
GOLD = np.array([196, 140, 40])
BOX = {"p01": (175, 370, 430, 570), "p02": (680, 150, 950, 345), "p03": (515, 510, 765, 712),
       "p04": (1010, 375, 1250, 565), "p06": (1135, 550, 1365, 730), "p05": (525, 270, 778, 465)}
START = (780.0, 452.0)    # the crosshair centre ("you start here")


def fit(xs, ys):
    D = np.stack([xs * xs, xs * ys, ys * ys, xs, ys, np.ones_like(xs)], 1).astype(float)
    _, _, vt = np.linalg.svd(D, full_matrices=False)
    a, b, c, d, e, f = vt[-1]
    den = b * b - 4 * a * c
    x0 = (2 * c * d - b * e) / den
    y0 = (2 * a * e - b * d) / den
    return (a, b, c, d, e, f), x0, y0


out = {"start": list(START)}
for pid, (x0, y0, x1, y1) in BOX.items():
    sub = im[y0:y1, x0:x1]
    if pid == "p05":
        r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
        m = (b > 140) & (r < 90) & (g < 120) & (b - r > 90)
    else:
        m = np.abs(sub - GOLD).sum(-1) < 30
    ys, xs = np.nonzero(m)
    xs = xs + x0; ys = ys + y0
    keep = np.ones(len(xs), bool)
    for _ in range(6):                       # refit, dropping the delivery line / dot pixels
        P, cx, cy = fit(xs[keep].astype(float), ys[keep].astype(float))
        a, b, c, d, e, f = P
        res = np.abs(a * xs * xs + b * xs * ys + c * ys * ys + d * xs + e * ys + f)
        thr = np.percentile(res[keep], 80)
        keep = res <= thr
    out[pid] = [round(float(cx), 1), round(float(cy), 1)]
    print(pid, out[pid], "pixels", int(m.sum()), "kept", int(keep.sum()))
os.makedirs(os.path.join(HERE, "frame_proof"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "frame_proof", "sketch_anchor_px.json"), "w"), indent=1)
