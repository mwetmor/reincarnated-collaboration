#!/usr/bin/env python3
"""PROBE-MEASURE — mask + read overlay plate.

Draws, over a zoomed crop of the source: the chroma mask boundary at all three
thresholds, and the four read endpoints of the two vertical walls. The mask is
always written before the number is believed (GAL-CAM gc_look / GD-PARITY
gp_seg precedent) -- including when it is ugly.
"""
import argparse, json
import numpy as np
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--numbers", required=True, help="pm_measure json")
ap.add_argument("--use", default="generous")
ap.add_argument("--x0", type=int, required=True)
ap.add_argument("--y0", type=int, required=True)
ap.add_argument("--w", type=int, required=True)
ap.add_argument("--h", type=int, required=True)
ap.add_argument("--zoom", type=int, default=6)
ap.add_argument("--out", required=True)
a = ap.parse_args()

D = json.load(open(a.numbers))
E = D["thresholds"][a.use]

im = Image.open(a.src).convert("RGB")
A = np.asarray(im, dtype=np.int16)
m = np.minimum(A[..., 0], A[..., 2]) - A[..., 1]

crop = im.crop((a.x0, a.y0, a.x0 + a.w, a.y0 + a.h))
z = a.zoom
big = crop.resize((a.w * z, a.h * z), Image.NEAREST)
PAD_L, PAD_T = 66, 26
cv = Image.new("RGB", (big.size[0] + PAD_L + 210, big.size[1] + PAD_T + 10), (14, 14, 18))
cv.paste(big, (PAD_L, PAD_T))
d = ImageDraw.Draw(cv)

def px(x, y): return PAD_L + (x - a.x0) * z, PAD_T + (y - a.y0) * z

# --- mask boundary at each threshold, one colour each -------------------------
COLS = {"tight": (255, 235, 60), "nominal": (60, 255, 140), "generous": (80, 190, 255)}
for name, col in COLS.items():
    thr = D["thresholds"][name]["threshold_m"]
    mask = m >= thr
    for y in range(a.y0, a.y0 + a.h):
        xs = np.nonzero(mask[y])[0]
        if not xs.size:
            continue
        for x in (int(xs.min()), int(xs.max())):
            if a.x0 <= x < a.x0 + a.w:
                X, Y = px(x, y)
                d.rectangle([X, Y, X + z - 1, Y + z - 1], outline=col)

# --- the four read endpoints --------------------------------------------------
for wall, q in E["walls"].items():
    for end in ("y_top", "y_bottom"):
        y = q[end]["read"]
        xw = q["x_top"] if end == "y_top" else q["x_bottom"]
        X, Y = px(xw, y)
        d.line([(PAD_L, Y), (PAD_L + big.size[0], Y)], fill=(255, 60, 60), width=1)
        d.ellipse([X - z, Y - z, X + 2 * z, Y + 2 * z], outline=(255, 60, 60), width=2)
        d.text((PAD_L + big.size[0] + 6, Y - 6),
               f"{wall[0].upper()}-{'top' if end=='y_top' else 'bot'}  y={y}  x={xw}"
               f"  [{q[end]['tight']}..{q[end]['generous']}]", fill=(255, 150, 150))
    # bracket band
    for end, c in (("y_top", (255, 120, 40)), ("y_bottom", (255, 120, 40))):
        for yb in (q[end]["tight"], q[end]["generous"]):
            _, Y = px(0, yb)
            d.line([(PAD_L, Y), (PAD_L + 14, Y)], fill=c, width=1)

# --- row ruler ---------------------------------------------------------------
y = a.y0 - (a.y0 % 10)
while y <= a.y0 + a.h:
    if y >= a.y0:
        _, Y = px(0, y)
        d.line([(PAD_L - 12, Y), (PAD_L, Y)], fill=(120, 200, 255), width=1)
        d.text((4, Y - 5), f"{y}", fill=(150, 210, 255))
    y += 10
x = a.x0 - (a.x0 % 10)
while x <= a.x0 + a.w:
    if x >= a.x0:
        X, _ = px(x, 0)
        d.line([(X, PAD_T - 10), (X, PAD_T)], fill=(120, 200, 255), width=1)
        d.text((X + 2, 4), f"{x}", fill=(150, 210, 255))
    x += 10

d.text((PAD_L, big.size[1] + PAD_T - 2),
       f"{D['label']}  primary={a.use}  yellow m>=200 / green m>=128 / blue m>=40",
       fill=(200, 200, 210))
cv.save(a.out)
print(f"{a.out}  crop=({a.x0},{a.y0})+({a.w}x{a.h}) zoom={z}")
