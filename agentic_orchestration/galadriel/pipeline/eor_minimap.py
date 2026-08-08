#!/usr/bin/env python3
"""eor_minimap.py — Grim Dawn minimap icon locator (1920x1080 capture).

galadriel / visual-perception seam.

The Crucible minimap is a north-up, player-centred disc in the top-right of the
HUD. It carries one icon per tracked actor and is free of the combat VFX that
swamp the in-world view, which makes it the cleanest available census surface.

Geometry (measured on the 2026-08-05 s2 capture, 1920x1080):
    disc centre (1776, 147), outer ring radius ~99 px; analysis radius 94 px.

Icon vocabulary observed:
    * gold/white starburst  -> monster (moves toward the player over a wave)
    * white skull           -> boss / nemesis-class monster
    * gold arrowhead        -> the player (saturated yellow, disc-centre-ish)
    * teal gem in gold ring -> static arena fixture (present in the prep phase
                               BEFORE any defense was purchased -> NOT a
                               player-built defense)
    * anvil / figure icons at the west + east rim -> static NPC furniture

This module only says WHERE to look and how many candidates there are. Every
count reported in a note is a galadriel eye-read of the magnified crop.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

CX, CY, R = 1776, 147, 94
CROP = (1668, 46, 1884, 244)

# HUD furniture that intrudes on the crop box but is not on the disc.
STATIC_EXCLUDE = [
    (1668, 46, 1726, 100),   # score-multiplier badge (xN) to the left of the disc
    (1750, 40, 1810, 62),    # gold top ornament + "N" marker
]


def _components(mask, min_area=8):
    H, W = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for y in range(H):
        for x in range(W):
            if mask[y, x] and not seen[y, x]:
                st = [(y, x)]
                seen[y, x] = True
                pix = []
                while st:
                    cy, cx = st.pop()
                    pix.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] \
                                    and not seen[ny, nx]:
                                seen[ny, nx] = True
                                st.append((ny, nx))
                if len(pix) >= min_area:
                    ys = np.array([p[0] for p in pix])
                    xs = np.array([p[1] for p in pix])
                    out.append(dict(x=float(xs.mean()), y=float(ys.mean()),
                                    area=len(pix),
                                    w=int(xs.max() - xs.min() + 1),
                                    h=int(ys.max() - ys.min() + 1)))
    return out


def icons(path, thr=150, min_area=8):
    """Bright-blob candidates on the minimap disc, in full-frame coordinates."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    L = a.mean(axis=2)
    m = L > thr
    H, W = m.shape
    yy, xx = np.mgrid[0:H, 0:W]
    m &= ((xx - CX) ** 2 + (yy - CY) ** 2) < R * R
    for (x0, y0, x1, y1) in STATIC_EXCLUDE:
        m[y0:y1, x0:x1] = False
    x0, y0, x1, y1 = CROP
    sub = m[y0:y1, x0:x1]
    out = []
    for c in _components(sub, min_area):
        gx, gy = c["x"] + x0, c["y"] + y0
        dx, dy = gx - CX, gy - CY
        # clock-face bearing: 12 o'clock = north = -y
        ang = (math.degrees(math.atan2(dx, -dy))) % 360.0
        clock = ((ang / 30.0) % 12)
        px = a[int(round(gy)) - 1:int(round(gy)) + 2,
               int(round(gx)) - 1:int(round(gx)) + 2].reshape(-1, 3).mean(axis=0)
        Rr, Gg, Bb = px
        if Bb > Rr + 12 and Gg > Rr + 8:
            kind = "teal-fixture"
        elif Rr > 170 and Gg > 130 and Bb < 110 and Rr - Bb > 70:
            kind = "gold"          # player arrow OR gold starburst
        else:
            kind = "pale"          # skull / white starburst
        out.append(dict(x=round(gx, 1), y=round(gy, 1), area=c["area"],
                        w=c["w"], h=c["h"], r=round(math.hypot(dx, dy), 1),
                        bearing_deg=round(ang, 1),
                        clock=round(clock, 1), kind=kind,
                        rgb=[int(v) for v in px]))
    return sorted(out, key=lambda d: -d["area"])


def annotate(path, out_png, scale=4, thr=150, min_area=8):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    for i, c in enumerate(icons(path, thr, min_area), 1):
        x, y = c["x"], c["y"]
        d.ellipse((x - 7, y - 7, x + 7, y + 7), outline=(255, 0, 255), width=1)
    d.ellipse((CX - R, CY - R, CX + R, CY + R), outline=(0, 255, 255), width=1)
    c = im.crop(CROP)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(out_png)
    return c.size


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(p)
        for c in icons(p):
            print("   ", c)
