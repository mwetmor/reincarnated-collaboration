#!/usr/bin/env python3
"""gd_zone_occupancy.py — is the player standing inside a green field, and is
the health bar down?

Both questions are answerable WITHOUT the screen->arena map, because the camera
is player-locked: the player's ground point is a fixed screen coordinate.

    * occupancy  = green-field pixel fraction in a disc around the player's feet
    * hp_frac    = filled length of the floating health bar (x 924..996, y 429)

The health bar is the cleaner instrument than OCR of the numerals: it is a
fixed-geometry 73 px bar and needs no character recognition.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image

from gd_arena_trace import CAP, SHOTS
from gd_green_zones import green_mask

HERE = os.path.dirname(os.path.abspath(__file__))
FEET = (960, 565)
BAR_X0, BAR_X1, BAR_Y = 924, 996, 429


def main():
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    track = dict(zip(meta["shots"], meta["track"]))
    out = []
    print(f"{'shot':>5} {'arena(x,y)':>16} {'g@r<60':>7} {'g@r<140':>8} "
          f"{'hp_bar_px':>10} {'hp_frac':>8}")
    for n in SHOTS:
        rgb = np.asarray(Image.open(
            os.path.join(CAP, f"Screenshot ({n}).png")).convert("RGB")).astype(float)
        m = green_mask(rgb)
        yy, xx = np.mgrid[0:1080, 0:1920]
        d = np.hypot(xx - FEET[0], yy - FEET[1])
        f60 = float(m[(d < 60)].mean())
        f140 = float(m[(d < 140)].mean())

        row = rgb[BAR_Y, BAR_X0:BAR_X1 + 1]
        R, G, B = row[:, 0], row[:, 1], row[:, 2]
        filled = (G > 110) & (G > R * 1.6) & (G > B * 1.6)
        npx = int(filled.sum())
        frac = npx / (BAR_X1 - BAR_X0 + 1)
        t = track[n]
        out.append(dict(shot=n, arena=[round(t[0], 1), round(t[1], 1)],
                        g60=round(f60, 3), g140=round(f140, 3),
                        hp_bar_px=npx, hp_frac=round(frac, 4)))
        flag = "  <-- IN ZONE" if f60 > 0.10 else ""
        print(f"{n:>5} ({t[0]:7.1f},{t[1]:7.1f}) {f60:7.3f} {f140:8.3f} "
              f"{npx:10d} {frac:8.4f}{flag}")
    json.dump(out, open(os.path.join(HERE, "gd-zone-occupancy.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
