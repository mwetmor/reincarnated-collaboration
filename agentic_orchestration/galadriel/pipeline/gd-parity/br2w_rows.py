#!/usr/bin/env python3
"""BR2W row-profile reader — locates subject edges for manual adjudication.

Convention (gd-parity, 2026-07-31): the segmenter/profiler BRACKETS the read.
The number of record is the manually adjudicated box. This tool exists so the
adjudication is made against printed evidence rather than against an impression.

Per row y it takes the row's own median RGB over a wide window (mostly floor,
so the median is floor even with the subject present) and prints a per-column
class map over the read window:

   .  dist < t1                  floor
   +  t1 <= dist < t2            weak deviation (soft shadow, wash, AA edge)
   #  dist >= t2                 strong deviation (subject or opaque FX)
   C  cyan HUD self-marker bar   (g-r > 45 and b > 150)          EXCLUDED
   O  bright FX (L > 195)        aura ring / pool / bloom        EXCLUDED
   R  red-additive telegraph     (r-g > 70 and r-b > 55 and L>110) EXCLUDED

Excluded classes are printed but never counted in the body extent columns.
"""
import argparse
import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("--src", required=True)
p.add_argument("--y0", type=int, default=400)
p.add_argument("--y1", type=int, default=515)
p.add_argument("--x0", type=int, default=756)     # read window
p.add_argument("--x1", type=int, default=856)
p.add_argument("--refx0", type=int, default=712)  # per-row median reference window
p.add_argument("--refx1", type=int, default=908)
p.add_argument("--t1", type=float, default=20.0)
p.add_argument("--t2", type=float, default=34.0)
a = p.parse_args()

im = np.asarray(Image.open(a.src).convert("RGB"), dtype=np.float32)
H, W, _ = im.shape
L = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]

print("src %s  %dx%d" % (a.src, W, H))
print("read window x %d..%d   ref window x %d..%d   thresholds %.0f / %.0f"
      % (a.x0, a.x1 - 1, a.refx0, a.refx1 - 1, a.t1, a.t2))
print("cols: %d   (tick every 10 src px)" % (a.x1 - a.x0))
hdr = "".join("|" if (x % 10 == 0) else " " for x in range(a.x0, a.x1))
lbl = ""
x = a.x0
while x < a.x1:
    if x % 20 == 0:
        s = str(x)
        lbl += s
        x += len(s)
    else:
        lbl += " "
        x += 1
print("      " + lbl)
print("      " + hdr)
print("%-5s %-*s  %5s %5s %5s %5s" % ("y", a.x1 - a.x0, "map", "n#", "L", "R", "nHUD"))

for y in range(a.y0, a.y1):
    row = im[y, a.refx0:a.refx1]
    ref = np.median(row, axis=0)
    seg = im[y, a.x0:a.x1]
    dist = np.sqrt(((seg - ref) ** 2).sum(axis=1))
    r, g, b = seg[:, 0], seg[:, 1], seg[:, 2]
    lum = L[y, a.x0:a.x1]
    cyan = (g - r > 45) & (b > 150)
    brt = lum > 195
    red = (r - g > 70) & (r - b > 55) & (lum > 110)
    excl = cyan | brt | red
    strong = (dist >= a.t2) & ~excl
    weak = (dist >= a.t1) & (dist < a.t2) & ~excl
    chars = []
    for i in range(a.x1 - a.x0):
        if cyan[i]:
            chars.append("C")
        elif brt[i]:
            chars.append("O")
        elif red[i]:
            chars.append("R")
        elif strong[i]:
            chars.append("#")
        elif weak[i]:
            chars.append("+")
        else:
            chars.append(".")
    idx = np.nonzero(strong)[0]
    if len(idx):
        lx, rx = a.x0 + int(idx[0]), a.x0 + int(idx[-1])
    else:
        lx = rx = -1
    print("%-5d %s  %5d %5d %5d %5d"
          % (y, "".join(chars), int(strong.sum()), lx, rx, int(excl.sum())))
