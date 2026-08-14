#!/usr/bin/env python3
"""KC2-PM4 Lap M -- Q2 discriminator: DISCRETE PROJECTILE BLOB TRACKING at the death frame.

The Q1 table says the ONLY mechanism class that reaches 20,005 post-mitigation in one sim tick is
a multi-projectile nova whose projectiles CO-LAND.  That hypothesis makes a falsifiable visual
prediction the colour-fraction instrument cannot test:

    N discrete bright blobs should exist at a RADIUS from the player anchor a few tenths of a
    second before the kill, their radii should DECREASE monotonically, and they should
    extinguish at/near the anchor in the kill window.

The null (a melee/ground event) predicts ink that APPEARS at the anchor and does not travel.

Instrument: per-frame saturated-colour connected components in two colour classes
(cyan/blue and green), area-gated, with ground-plane de-projection (K = 0.537, Lap H-2 D2) so
"radius" is a ground distance, not a screen distance.  Emits every blob, every frame -- no
tracking heuristic, no association model, so nothing can be smuggled in by the linker.
"""
from __future__ import annotations

import csv
import pathlib
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pm4m_video_2026_08_14 import grab                      # noqa: E402

K, PX, PY = 0.537, 960.0, 429.0
OUT = pathlib.Path("/tmp/pm4m")
MIN_AREA, MAX_AREA = 40, 4000


def masks(a: np.ndarray):
    A = a.astype(np.int16)
    R, G, B = A[..., 0], A[..., 1], A[..., 2]
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    bright = (mx > 150) & ((mx - mn) > 70)
    cyan = bright & (B >= mx) & (G > B * 0.65) & (R < B * 0.75)
    green = bright & (G >= mx) & (R < G * 0.75) & (B < G * 0.85)
    return dict(cyan=cyan, green=green)


def blobs(m: np.ndarray, tag: str, t: float):
    lab, n = ndimage.label(m)
    if n == 0:
        return []
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs, start=1):
        area = int((lab[sl] == i).sum())
        if not (MIN_AREA <= area <= MAX_AREA):
            continue
        ys, xs = np.nonzero(lab[sl] == i)
        cy = float(ys.mean() + sl[0].start)
        cx = float(xs.mean() + sl[1].start)
        r = float(np.hypot(cx - PX, (cy - PY) / K))
        out.append(dict(t_s=round(t, 4), colour=tag, area=area,
                        cx=round(cx, 1), cy=round(cy, 1), ground_r_px=round(r, 1)))
    return out


def main():
    t0, t1, fps = 864.0000, 864.9000, 60
    rows = []
    s = t0
    while s < t1 - 1e-6:
        d = min(0.5, t1 - s)
        F = grab(s, d, fps)
        for i, fr in enumerate(F):
            t = s + i / fps
            for tag, m in masks(fr).items():
                rows += blobs(m, tag, t)
        del F
        s += d
    p = OUT / "pm4m_blobs_864.0_864.9.csv"
    with p.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["t_s", "colour", "area", "cx", "cy", "ground_r_px"])
        w.writeheader()
        w.writerows(rows)
    print("rows", len(rows), "->", p)

    # per-frame summary: blob count and the radius distribution, by colour
    import collections
    byt = collections.defaultdict(list)
    for r in rows:
        byt[(round(r["t_s"], 4), r["colour"])].append(r["ground_r_px"])
    ts = sorted({k[0] for k in byt})
    print(f"{'t_s':>10} | {'cyanN':>5} {'cyan_min':>8} {'cyan_med':>8} | "
          f"{'grnN':>4} {'grn_min':>8} {'grn_med':>8} | {'N r<120':>7}")
    for t in ts:
        c = sorted(byt.get((t, "cyan"), []))
        g = sorted(byt.get((t, "green"), []))
        near = sum(1 for x in c + g if x < 120)
        print(f"{t:10.4f} | {len(c):5d} {(c[0] if c else 0):8.0f} "
              f"{(c[len(c)//2] if c else 0):8.0f} | {len(g):4d} {(g[0] if g else 0):8.0f} "
              f"{(g[len(g)//2] if g else 0):8.0f} | {near:7d}")


if __name__ == "__main__":
    main()
