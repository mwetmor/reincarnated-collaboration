#!/usr/bin/env python3
"""GD-PARITY — anchor-crop grid montage over a list of source frames.

Lays N anchor crops in a COLS-wide grid at integer zoom, each tile labelled with
its frame id and carrying a light row ruler so a height read stays quotable in
source pixels.
"""
import argparse
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--srcs", nargs="+", required=True)
ap.add_argument("--labels", nargs="+", default=None)
ap.add_argument("--cx", type=int, default=962)
ap.add_argument("--cy", type=int, default=570)
ap.add_argument("--w", type=int, default=150)
ap.add_argument("--h", type=int, default=190)
ap.add_argument("--zoom", type=int, default=2)
ap.add_argument("--cols", type=int, default=3)
ap.add_argument("--gain", type=float, default=1.6)
ap.add_argument("--rule", type=int, default=25)
ap.add_argument("--out", required=True)
a = ap.parse_args()

labels = a.labels or [str(i) for i in range(len(a.srcs))]
z = a.zoom
tw, th = a.w * z, a.h * z
LAB = 16
cols = a.cols
rows = (len(a.srcs) + cols - 1) // cols
canvas = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + LAB + 4) + 4), (16, 16, 20))
d = ImageDraw.Draw(canvas)

x0 = a.cx - a.w // 2
y0 = a.cy - a.h // 2
for i, s in enumerate(a.srcs):
    im = Image.open(s).convert("RGB")
    c = im.crop((x0, y0, x0 + a.w, y0 + a.h))
    if a.gain != 1.0:
        c = c.point(lambda v: min(255, int(v * a.gain)))
    c = c.resize((tw, th), Image.NEAREST)
    r, col = divmod(i, cols)
    px = 4 + col * (tw + 4)
    py = 4 + r * (th + LAB + 4) + LAB
    canvas.paste(c, (px, py))
    d.text((px + 2, py - LAB + 2), f"{labels[i]}", fill=(255, 220, 120))
    y = y0 - (y0 % a.rule)
    while y <= y0 + a.h:
        if y >= y0:
            yy = py + (y - y0) * z
            major = (y % 100 == 0)
            d.line([(px, yy), (px + (18 if major else 9), yy)],
                   fill=(255, 70, 70) if major else (90, 200, 255))
            d.line([(px + tw - (18 if major else 9), yy), (px + tw, yy)],
                   fill=(255, 70, 70) if major else (90, 200, 255))
            if major:
                d.text((px + 20, yy - 5), f"{y}", fill=(255, 190, 190))
        y += a.rule
canvas.save(a.out)
print(a.out, canvas.size)
