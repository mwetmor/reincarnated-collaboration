#!/usr/bin/env python3
"""gd_green_zones.py — detect the Chthonic green spawn-zone fields in world view.

The zones render as saturated green volumetric fields.  Detection is a simple
green-excess threshold; the HUD, the minimap disc and the player's own floating
health bar are masked out because they carry saturated greens of their own.
"""
from __future__ import annotations

import collections
import json
import os

import numpy as np
from PIL import Image

from gd_arena_trace import CAP, SHOTS

HERE = os.path.dirname(os.path.abspath(__file__))

# HUD regions to exclude (full-frame px, x0,y0,x1,y1)
HUD = [
    (1560, 0, 1920, 340),      # minimap disc + objectives block
    (1270, 0, 1640, 130),      # centre HUD bar
    (0, 920, 1920, 1080),      # action bar + globes
    (0, 0, 300, 70),           # char name + clock
    (830, 380, 1090, 450),     # player floating health bar + text
]


def green_mask(rgb):
    R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    m = (G > 70) & (G > R * 1.45) & (G > B * 1.25)
    for x0, y0, x1, y1 in HUD:
        m[y0:y1, x0:x1] = False
    return m


def blobs(m, min_area=900):
    seen = np.zeros(m.shape, bool)
    ys, xs = np.nonzero(m)
    out = []
    for y, x in zip(ys, xs):
        if seen[y, x]:
            continue
        q = collections.deque([(y, x)])
        seen[y, x] = True
        pix = []
        while q:
            cy, cx = q.popleft()
            pix.append((cy, cx))
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] \
                            and m[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
        if len(pix) >= min_area:
            p = np.array(pix)
            out.append(dict(area=len(pix),
                            cx=float(p[:, 1].mean()), cy=float(p[:, 0].mean()),
                            x0=int(p[:, 1].min()), x1=int(p[:, 1].max()),
                            y0=int(p[:, 0].min()), y1=int(p[:, 0].max())))
    out.sort(key=lambda d: -d["area"])
    return out


def main():
    res = {}
    for n in SHOTS:
        rgb = np.asarray(Image.open(
            os.path.join(CAP, f"Screenshot ({n}).png")).convert("RGB")).astype(float)
        bs = blobs(green_mask(rgb))
        res[n] = bs
        print(f"{n}: {len(bs)} blobs  " + "  ".join(
            f"[{b['area']:6d} @({b['cx']:6.0f},{b['cy']:6.0f}) "
            f"{b['x1']-b['x0']:4d}x{b['y1']-b['y0']:4d}]" for b in bs[:6]))
    json.dump(res, open(os.path.join(HERE, "gd-green-blobs.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
