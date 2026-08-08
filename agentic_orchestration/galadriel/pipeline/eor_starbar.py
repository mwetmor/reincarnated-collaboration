#!/usr/bin/env python3
"""eor_starbar.py — detect Grim Dawn's in-world health-bar RANK FURNITURE.

galadriel / visual-perception seam. KC2-SIM Phase-C third-extraction pass.

Grim Dawn flanks a monster's in-world health bar with rank furniture:

    plain (no flanking glyph)   -> lowest tier observed
    one gold five-point star    -> champion/hero tier
    double skull, red           -> nemesis tier
    double skull, bone/pale     -> boss tier

The star pass keys on the PAIR, not the glyph: two pale-warm components of
star-like size sitting at the same row band, 40..380 px apart, with a run of
saturated-red bar pixels between them. The pairing constraint is what makes it
survive an arena full of pale VFX.

Positive control: s2 t=803.6 (wave 158) carries two star-flanked bars,
max HP 448,397 and 458,794.

Every reported hit is eye-verified on a magnified crop; this module only says
where to look and holds the count reproducible.
"""
from __future__ import annotations

import numpy as np
from PIL import Image


def _components(mask, min_area, max_area):
    H, W = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    idx = np.argwhere(mask)
    for y0, x0 in idx:
        if seen[y0, x0]:
            continue
        st = [(y0, x0)]
        seen[y0, x0] = True
        pix = []
        while st:
            cy, cx = st.pop()
            pix.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        st.append((ny, nx))
        if min_area <= len(pix) <= max_area:
            ys = np.array([p[0] for p in pix])
            xs = np.array([p[1] for p in pix])
            h = ys.max() - ys.min() + 1
            w = xs.max() - xs.min() + 1
            if 10 <= w <= 30 and 10 <= h <= 30 and 0.55 <= w / h <= 1.8:
                out.append(dict(x=float(xs.mean()), y=float(ys.mean()),
                                area=len(pix), w=int(w), h=int(h)))
    return out


def stars(path, region=(0, 20, 1920, 950)):
    """Star-flanked-bar candidates. Returns list of dicts with the bar span."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    x0, y0, x1, y1 = region
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    pale = (R > 120) & (G > 95) & (B > 80) & (R - G < 70) & (R - B < 110) & (G - B > -20)
    red = (R > 110) & (R - G > 55) & (R - B > 55)
    comps = _components(pale, 35, 260)
    hits = []
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            A, Bc = comps[i], comps[j]
            if abs(A["y"] - Bc["y"]) > 7:
                continue
            L, Rt = (A, Bc) if A["x"] < Bc["x"] else (Bc, A)
            gap = Rt["x"] - L["x"]
            if not (40 <= gap <= 380):
                continue
            yy = int(round((A["y"] + Bc["y"]) / 2))
            band = red[max(0, yy - 4):yy + 5, int(L["x"]) + 8:int(Rt["x"]) - 7]
            if band.size == 0:
                continue
            if band.mean() < 0.14:
                continue
            hits.append(dict(y=yy + y0, xl=round(L["x"] + x0, 1),
                             xr=round(Rt["x"] + x0, 1), gap=round(gap, 1),
                             red_frac=round(float(band.mean()), 3),
                             areaL=L["area"], areaR=Rt["area"]))
    return hits


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        h = stars(p)
        print(p, len(h))
        for x in h:
            print("   ", x)
