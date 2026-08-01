#!/usr/bin/env python3
"""GD-PARITY — crop + ruler tool.

Renders a crop of a source frame at integer upscale with a labelled pixel ruler
in SOURCE-frame coordinates, so a screen-height read is directly quotable in
source pixels (and thus as a fraction of source frame height).

Usage:
  gp_ruler.py --src IMG --cx X --cy Y --w W --h H --zoom Z --out OUT.png
  gp_ruler.py --src IMG --x0 X0 --y0 Y0 --w W --h H --zoom Z --out OUT.png

Ruler: minor tick every `--minor` source px (default 10), major every
`--major` (default 50, labelled).
"""
import argparse
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--cx", type=int)
ap.add_argument("--cy", type=int)
ap.add_argument("--x0", type=int)
ap.add_argument("--y0", type=int)
ap.add_argument("--w", type=int, default=240)
ap.add_argument("--h", type=int, default=240)
ap.add_argument("--zoom", type=int, default=4)
ap.add_argument("--minor", type=int, default=10)
ap.add_argument("--major", type=int, default=50)
ap.add_argument("--gain", type=float, default=1.0, help="brightness gain")
ap.add_argument("--out", required=True)
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
W, H = im.size
if a.x0 is not None:
    x0, y0 = a.x0, a.y0
else:
    x0, y0 = a.cx - a.w // 2, a.cy - a.h // 2
x0 = max(0, min(W - a.w, x0))
y0 = max(0, min(H - a.h, y0))
crop = im.crop((x0, y0, x0 + a.w, y0 + a.h))
if a.gain != 1.0:
    crop = crop.point(lambda v: min(255, int(v * a.gain)))
z = a.zoom
big = crop.resize((a.w * z, a.h * z), Image.NEAREST)

PAD_L, PAD_T = 62, 22
canvas = Image.new("RGB", (big.size[0] + PAD_L + 8, big.size[1] + PAD_T + 8), (16, 16, 20))
canvas.paste(big, (PAD_L, PAD_T))
d = ImageDraw.Draw(canvas)

# horizontal ruler (source rows) on the left
y = y0 - (y0 % a.minor)
while y <= y0 + a.h:
    if y >= y0:
        py = PAD_T + (y - y0) * z
        major = (y % a.major == 0)
        col = (255, 60, 60) if major else (90, 200, 255)
        d.line([(PAD_L - (14 if major else 7), py), (PAD_L + big.size[0], py)],
               fill=col if major else (40, 70, 90), width=1)
        d.line([(PAD_L - (14 if major else 7), py), (PAD_L, py)], fill=col, width=1)
        if major:
            d.text((2, py - 5), f"{y}", fill=(255, 190, 190))
    y += a.minor

x = x0 - (x0 % a.minor)
while x <= x0 + a.w:
    if x >= x0:
        px = PAD_L + (x - x0) * z
        major = (x % a.major == 0)
        col = (255, 60, 60) if major else (90, 200, 255)
        d.line([(px, PAD_T - (12 if major else 6)), (px, PAD_T + big.size[1])],
               fill=col if major else (40, 70, 90), width=1)
        d.line([(px, PAD_T - (12 if major else 6)), (px, PAD_T)], fill=col, width=1)
        if major:
            d.text((px + 2, 4), f"{x}", fill=(255, 190, 190))
    x += a.minor

canvas.save(a.out)
print(f"{a.out}  src={W}x{H}  crop=({x0},{y0})+({a.w}x{a.h})  zoom={z}")
