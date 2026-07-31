#!/usr/bin/env python3
"""SHADOW-CAL: look sheet — crops around the player anchor, at full res and zoomed.

Discipline (gc_look.py precedent): render the pixels before believing any fit.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw

ANCHOR = (962, 595)


def crop_zoom(p, cx, cy, half=200, zoom=2):
    im = Image.open(p).convert("RGB")
    x0, y0 = max(0, cx - half), max(0, cy - half)
    x1, y1 = min(im.width, cx + half), min(im.height, cy + half)
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * zoom, c.height * zoom), Image.NEAREST)
    d = ImageDraw.Draw(c)
    # mark the anchor
    ax, ay = (cx - x0) * zoom, (cy - y0) * zoom
    d.line([(ax - 14, ay), (ax + 14, ay)], fill=(0, 255, 255), width=1)
    d.line([(ax, ay - 14), (ax, ay + 14)], fill=(0, 255, 255), width=1)
    return c


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--half", type=int, default=200)
    ap.add_argument("--zoom", type=int, default=2)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--cx", type=int, default=ANCHOR[0])
    ap.add_argument("--cy", type=int, default=ANCHOR[1])
    a = ap.parse_args()

    crops = [crop_zoom(p, a.cx, a.cy, a.half, a.zoom) for p in a.frames]
    w, h = crops[0].size
    cols = min(a.cols, len(crops))
    rows = (len(crops) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * w, rows * h), (10, 10, 10))
    d = ImageDraw.Draw(canvas)
    for i, c in enumerate(crops):
        r, cc = divmod(i, cols)
        canvas.paste(c, (cc * w, r * h))
        d.text((cc * w + 6, r * h + 6), os.path.basename(a.frames[i]),
               fill=(255, 255, 0))
    canvas.save(a.out, quality=92)
    print("->", a.out)
