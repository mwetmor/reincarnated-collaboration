#!/usr/bin/env python3
"""PROBE-MEASURE — silhouette wall profile of the magenta probe box.

The box is world-axis-aligned, viewed roughly corner-on under a pitched-down
camera, so the magenta silhouette is roughly hexagonal. Its LEFT and RIGHT
extremes are the two true VERTICAL box edges (ground-corner -> top-corner);
above and below those edges the boundary slants away along top-face and
ground-face silhouette edges.

Instrument: for every row y, report x_left(y) = min magenta x and
x_right(y) = max magenta x, at three chroma thresholds (tight / nominal /
generous). The vertical edge is the PLATEAU in that profile; the corner is the
row at which the plateau breaks. Nothing is fitted -- the plateau and its break
are read off the printed table (GL-17).

magenta-ness m = min(R,B) - G
"""
import argparse, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--tight", type=int, default=200)
ap.add_argument("--nominal", type=int, default=128)
ap.add_argument("--generous", type=int, default=40)
ap.add_argument("--minrun", type=int, default=1,
                help="min contiguous magenta px in a row for that row to count")
ap.add_argument("--json", default=None)
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
A = np.asarray(im, dtype=np.int16)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
m = np.minimum(R, B) - G
H, W = m.shape

THRS = [("tight", a.tight), ("nominal", a.nominal), ("generous", a.generous)]
prof = {}
for name, t in THRS:
    mask = m >= t
    rows = {}
    for y in range(H):
        xs = np.nonzero(mask[y])[0]
        if xs.size >= a.minrun:
            rows[y] = (int(xs.min()), int(xs.max()), int(xs.size))
    prof[name] = rows

nom = prof["nominal"]
ys = sorted(nom)
print(f"== {a.src} ==")
print(f"nominal(m>={a.nominal}) row span y[{ys[0]}..{ys[-1]}]  n_rows={len(ys)}")
print(f"tight(m>={a.tight})      row span y[{min(prof['tight'])}..{max(prof['tight'])}]  n_rows={len(prof['tight'])}")
print(f"generous(m>={a.generous})   row span y[{min(prof['generous'])}..{max(prof['generous'])}]  n_rows={len(prof['generous'])}")
print()
print("  y   | tight  L    R  n | nomin  L    R  n | gener  L    R  n |")
print("------+------------------+------------------+------------------+")
y0 = min(min(prof[n]) for n, _ in THRS)
y1 = max(max(prof[n]) for n, _ in THRS)
for y in range(y0, y1 + 1):
    cells = []
    for name, _ in THRS:
        r = prof[name].get(y)
        cells.append(f"{r[0]:5d}{r[1]:5d}{r[2]:4d}" if r else "    -    -   -")
    print(f" {y:4d} | " + " | ".join(cells) + " |")

out = {"src": a.src, "w": W, "h": H,
       "thresholds": {n: t for n, t in THRS},
       "profile": {n: {str(k): v for k, v in prof[n].items()} for n, _ in THRS}}
if a.json:
    with open(a.json, "w") as f:
        json.dump(out, f)
