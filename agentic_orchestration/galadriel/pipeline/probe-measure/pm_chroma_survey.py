#!/usr/bin/env python3
"""PROBE-MEASURE — chroma survey of the magenta probe box.

Instrument, not oracle. Surveys the distribution of "magenta-ness" over a whole
frame so a threshold can be READ off the data rather than guessed (GL-17).

magenta-ness m = min(R, B) - G   (0..255, high = strong R+B with low G)

Prints: histogram of m over the frame; per-band pixel counts; bbox of each band.
"""
import argparse, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--json", default=None)
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
A = np.asarray(im, dtype=np.int16)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
m = np.minimum(R, B) - G

H, W = m.shape
out = {"src": a.src, "w": int(W), "h": int(H)}

print(f"== {a.src}  {W}x{H} ==")
print("m = min(R,B)-G   histogram (bin width 8, only non-empty bins >= 0):")
hist = {}
for lo in range(0, 264, 8):
    n = int(((m >= lo) & (m < lo + 8)).sum())
    if n:
        hist[lo] = n
        print(f"  m [{lo:3d},{lo+8:3d})  {n:9d}")
out["hist_bin8"] = hist

print("\ncumulative counts at candidate thresholds, with bbox:")
bands = []
for thr in [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]:
    mask = m >= thr
    n = int(mask.sum())
    row = {"thr": thr, "n": n}
    if n:
        ys, xs = np.nonzero(mask)
        row.update(x0=int(xs.min()), x1=int(xs.max()),
                   y0=int(ys.min()), y1=int(ys.max()))
        print(f"  m>={thr:3d}: n={n:8d}  bbox x[{xs.min()}..{xs.max()}] "
              f"y[{ys.min()}..{ys.max()}]  w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1}")
    else:
        print(f"  m>={thr:3d}: n=0")
    bands.append(row)
out["bands"] = bands

# what do the strongest pixels actually look like
core = m >= 200
if core.sum():
    px = A[core]
    print(f"\ncore (m>=200) n={core.sum()}  "
          f"R med {np.median(px[:,0]):.0f} G med {np.median(px[:,1]):.0f} B med {np.median(px[:,2]):.0f}")
    print(f"  R range {px[:,0].min()}..{px[:,0].max()}  "
          f"G range {px[:,1].min()}..{px[:,1].max()}  B range {px[:,2].min()}..{px[:,2].max()}")
    out["core_med"] = [float(np.median(px[:, i])) for i in range(3)]

if a.json:
    with open(a.json, "w") as f:
        json.dump(out, f, indent=1)
