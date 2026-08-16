#!/usr/bin/env python3
"""PROBE-MEASURE — corner-break read on the silhouette walls.

For a chroma threshold, walks the left and right silhouette boundary rows and
prints the LOCAL SLOPE dx/dy over a +/-k row window. A true vertical box edge
under a pitched, un-rolled camera leans toward the nadir at a few HUNDREDTHS of
a px/row; the top-face and ground-face silhouette edges run at ~1 px/row. The
corner is the row where the slope crosses out of the near-zero band. That row is
READ off this table, not fitted.

Also prints the run-length of the extreme-x plateau, which is the same corner
seen a second way.
"""
import argparse, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--thr", type=int, default=40)
ap.add_argument("--win", type=int, default=4, help="half-window rows for slope")
ap.add_argument("--flat", type=float, default=0.25, help="px/row still called flat")
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
A = np.asarray(im, dtype=np.int16)
m = np.minimum(A[..., 0], A[..., 2]) - A[..., 1]
mask = m >= a.thr
H, W = m.shape

rows, L, R = [], [], []
for y in range(H):
    xs = np.nonzero(mask[y])[0]
    if xs.size:
        rows.append(y); L.append(int(xs.min())); R.append(int(xs.max()))
rows = np.array(rows); L = np.array(L); R = np.array(R)
n = len(rows)
k = a.win

print(f"== {a.src}  thr m>={a.thr}  slope window +/-{k} rows ==")
print(f"row extent y[{rows[0]}..{rows[-1]}]   n_rows={n}")
print("\n  y  |  Lx  dL/dy |  Rx  dR/dy |  flags")
print("-----+------------+------------+--------")
for i in range(n):
    lo, hi = max(0, i - k), min(n - 1, i + k)
    dy = rows[hi] - rows[lo]
    dL = (L[hi] - L[lo]) / dy if dy else float("nan")
    dR = (R[hi] - R[lo]) / dy if dy else float("nan")
    fl = []
    if abs(dL) <= a.flat: fl.append("L-FLAT")
    if abs(dR) <= a.flat: fl.append("R-FLAT")
    print(f"{rows[i]:5d}| {L[i]:5d} {dL:+6.2f} | {R[i]:5d} {dR:+6.2f} | {' '.join(fl)}")

# plateau runs on the extreme columns
def runs(v, extreme):
    out, start = [], None
    for i in range(n):
        if v[i] == extreme:
            if start is None: start = rows[i]
            last = rows[i]
        else:
            if start is not None: out.append((start, last)); start = None
    if start is not None: out.append((start, last))
    return out

print("\nextreme-column runs (leftmost x reached, rightmost x reached):")
for lab, v, ex in (("L", L, L.min()), ("R", R, R.max())):
    print(f"  {lab}: x={ex}  rows {runs(v, ex)}")
print("\nper-x run extents on each wall (x -> first_row..last_row, count):")
for lab, v in (("L", L), ("R", R)):
    print(f"  {lab} wall:")
    for x in sorted(set(v.tolist())):
        idx = rows[v == x]
        if len(idx) >= 2:
            print(f"    x={x:4d}  y {idx.min():4d}..{idx.max():4d}  n={len(idx)}")
