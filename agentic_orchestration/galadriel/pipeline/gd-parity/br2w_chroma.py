#!/usr/bin/env python3
"""BR2W fur-vs-floor chromaticity map.

On this clip the player carries a warm omni (E=5.20, 9 m, colour 1.00/0.66/0.34)
so LUMINANCE does not separate the werewolf from the floor it stands on.
CHROMATICITY does: measured on frame 1027,

    fur  (torso lit / head shaded)  b_frac 0.181 .. 0.272 , r_frac 0.45 .. 0.51
    floor(unlit right / warm left)  b_frac 0.311 .. 0.337 , r_frac 0.35 .. 0.38
    aura pool core                  b_frac 0.283 , L 219  (excluded on luminance)

Classes printed:
    F  fur        r_frac >= RT and b_frac <= BT and L <= LMAX
    o  bright FX  L > LMAX                       (aura pool / ring / bloom)
    C  cyan HUD   g-r > 45 and b > 150
    -  floor / everything else
This is a BRACKET, printed so the manual adjudication can be checked against it.
"""
import argparse
import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("--src", required=True)
p.add_argument("--x0", type=int, required=True)
p.add_argument("--x1", type=int, required=True)
p.add_argument("--y0", type=int, required=True)
p.add_argument("--y1", type=int, required=True)
p.add_argument("--rt", type=float, default=0.415, help="min r fraction for fur")
p.add_argument("--bt", type=float, default=0.285, help="max b fraction for fur")
p.add_argument("--lmax", type=float, default=190.0, help="above this = bright FX")
a = p.parse_args()

im = np.asarray(Image.open(a.src).convert("RGB"), dtype=np.float32)
L = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
s = im.sum(axis=2) + 1e-6
rf, bf, gf = im[..., 0] / s, im[..., 2] / s, im[..., 1] / s
cyan = (im[..., 1] - im[..., 0] > 45) & (im[..., 2] > 150)
fur = (rf >= a.rt) & (bf <= a.bt) & (L <= a.lmax) & ~cyan

print("src %s   fur: r_frac>=%.3f  b_frac<=%.3f  L<=%.0f" % (a.src, a.rt, a.bt, a.lmax))
lbl = ""
x = a.x0
while x < a.x1:
    if x % 10 == 0:
        lbl += str(x)
        x += len(str(x))
    else:
        lbl += " "
        x += 1
print("      " + lbl)
print("%-5s %s  %5s %5s %5s" % ("y", "map".ljust(a.x1 - a.x0), "nFur", "Lx", "Rx"))
for y in range(a.y0, a.y1):
    line = []
    for x in range(a.x0, a.x1):
        if cyan[y, x]:
            line.append("C")
        elif L[y, x] > a.lmax:
            line.append("o")
        elif fur[y, x]:
            line.append("F")
        else:
            line.append("-")
    idx = [i for i, c in enumerate(line) if c == "F"]
    lx = a.x0 + idx[0] if idx else -1
    rx = a.x0 + idx[-1] if idx else -1
    print("%-5d %s  %5d %5d %5d" % (y, "".join(line), len(idx), lx, rx))
