#!/usr/bin/env python3
"""eor_bearing.py — arena-anchored bearings for minimap monster icons.

galadriel / visual-perception seam.

The Grim Dawn minimap is player-centred, so raw icon bearings measured from the
disc centre are PLAYER-relative and swing as the player moves. The Crucible
arena carries a ring of static teal-gem fixtures; their centroid is a usable
proxy for the arena centre, which lets bearings be re-expressed arena-relative.

Provenance of anything this module emits: ESTIMATED-FOOTAGE. The teal ring is
only partially inside the disc when the player is off-centre, which biases the
centroid; the module reports how many fixtures it used so the bias is visible.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image

import eor_minimap as mm


def _cc(sub, min_area):
    seen = np.zeros_like(sub)
    hh, ww = sub.shape
    out = []
    for y in range(hh):
        for x in range(ww):
            if sub[y, x] and not seen[y, x]:
                st = [(y, x)]
                seen[y, x] = True
                pix = []
                while st:
                    cy, cx = st.pop()
                    pix.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < hh and 0 <= nx < ww and sub[ny, nx] \
                                    and not seen[ny, nx]:
                                seen[ny, nx] = True
                                st.append((ny, nx))
                if len(pix) >= min_area:
                    out.append((float(np.mean([p[1] for p in pix])),
                                float(np.mean([p[0] for p in pix])), len(pix)))
    return out


def teal_fixtures(path, min_area=9):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W, _ = a.shape
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (B > 90) & (G > 85) & (B - R > 35) & (G - R > 25)
    yy, xx = np.mgrid[0:H, 0:W]
    m &= ((xx - mm.CX) ** 2 + (yy - mm.CY) ** 2) < 94 * 94
    x0, y0, x1, y1 = mm.CROP
    return [(x + x0, y + y0, a_) for x, y, a_ in _cc(m[y0:y1, x0:x1], min_area)]


def arena_bearings(path, thr=140, min_area=12):
    """Monster icons with bearings taken from the teal-fixture centroid."""
    tf = teal_fixtures(path)
    if tf:
        ax = float(np.mean([t[0] for t in tf]))
        ay = float(np.mean([t[1] for t in tf]))
    else:
        ax, ay = mm.CX, mm.CY
    out = []
    for c in mm.icons(path, thr=thr, min_area=min_area):
        dx, dy = c["x"] - ax, c["y"] - ay
        ang = math.degrees(math.atan2(dx, -dy)) % 360.0
        out.append(dict(x=c["x"], y=c["y"], area=c["area"],
                        clock=round((ang / 30.0) % 12, 1),
                        deg=round(ang, 1), r=round(math.hypot(dx, dy), 1),
                        kind=c["kind"], rgb=c["rgb"]))
    return dict(anchor=(round(ax, 1), round(ay, 1)), n_fixtures=len(tf),
                icons=sorted(out, key=lambda d: -d["area"]))
