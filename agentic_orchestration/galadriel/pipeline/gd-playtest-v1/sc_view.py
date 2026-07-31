#!/usr/bin/env python3
"""SHADOW-CAL: contrast-stretched, coordinate-gridded view for endpoint reading.

The cast shadows in this fixture are real but LOW CONTRAST against mottled,
fogged ground -- which is why every automatic segmenter in this cell either
grabbed the whole neighbourhood or nothing.  Stretching the luma between local
percentiles makes the shadow legible without moving any pixel: the stretch is a
DISPLAY transform only, and every quantity is afterwards measured on the
UNSTRETCHED frame through the camera model.

No silent transformation: the stretch limits are printed with the view.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw


def view(path, box, out, grid=50, zoom=2.0, lo_pct=6, hi_pct=94, gamma=0.85):
    x0, y0, x1, y1 = box
    im = np.asarray(Image.open(path).convert("RGB"), np.float32)
    c = im[y0:y1, x0:x1]
    L = 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
    lo, hi = np.percentile(L, [lo_pct, hi_pct])
    S = np.clip((L - lo) / max(hi - lo, 1e-6), 0, 1) ** gamma
    st = (np.stack([S] * 3, -1) * 255).astype(np.uint8)
    w, h = x1 - x0, y1 - y0
    W, H = int(w * zoom), int(h * zoom)
    top = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    bot = Image.fromarray(st).resize((W, H), Image.LANCZOS)
    cv = Image.new("RGB", (W, 2 * H + 26), (10, 10, 10))
    cv.paste(top, (0, 0))
    cv.paste(bot, (0, H + 26))
    d = ImageDraw.Draw(cv)
    for panel_y in (0, H + 26):
        for X in range(int(np.ceil(x0 / grid) * grid), x1, grid):
            x = (X - x0) * zoom
            d.line([(x, panel_y), (x, panel_y + H)], fill=(0, 200, 255))
            d.text((x + 2, panel_y + 2), str(X), fill=(0, 220, 255))
        for Y in range(int(np.ceil(y0 / grid) * grid), y1, grid):
            y = panel_y + (Y - y0) * zoom
            d.line([(0, y), (W, y)], fill=(0, 200, 255))
            d.text((2, y + 2), str(Y), fill=(0, 220, 255))
    d.text((6, H + 6), f"luma stretched {lo:.1f}-{hi:.1f}  gamma {gamma}  "
                       f"(DISPLAY ONLY; measurement uses the raw frame)",
           fill=(255, 255, 0))
    cv.save(out, quality=93)
    return out, float(lo), float(hi)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True)
    ap.add_argument("--box", type=int, nargs=4, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--zoom", type=float, default=2.0)
    ap.add_argument("--grid", type=int, default=50)
    a = ap.parse_args()
    o, lo, hi = view(a.frame, tuple(a.box), a.out, grid=a.grid, zoom=a.zoom)
    print(f"-> {o}   stretch {lo:.1f}..{hi:.1f}")
