#!/usr/bin/env python3
"""WR1-GAL-3: nova-ring metric instrument.

WHY THIS INSTRUMENT
-------------------
The nova is `Skill_AttackProjectileRing`: 16 projectiles, 22.5 deg apart, launched
from the caster's ground point, travelling 14 m/s over 12 m. The ring of projectile
HEADS is therefore a ground-plane circle of KNOWN world radius R(t) = 14*(t-t0).
Under this camera (fixed pitch, no roll) a ground circle projects to a screen
ellipse whose axes are screen-aligned; the axis ratio k = b/a = sin(pitch) is
constant, and a(t) = s * R(t) with s = px per metre along screen-X at the ground
plane.

So the ring is a self-calibrating scale bar: fit a(t) across frames and the slope
gives s directly (px per metre), and the intercept gives t0 (the launch frame).
Both products are needed:
  - s converts a screen separation to metres (SPATIAL anchor)
  - t0 converts an arrival TIME to metres via r = 14*(t_hit-t0)/60 (TEMPORAL anchor)
Two independent anchors on the same question.

Detection: projectile heads are the brightest cold pixels. Mask = B>150,
B-R>60, B>=G-12 (gal2's cold rule, verbatim) intersected with a brightness floor.
Trails lag behind the heads, so for a given centre the RADIAL MAXIMUM of the cold
mask is the head locus -- trails cannot inflate it.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

FRAMES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "captures", "2026-07-29-wr1-gal3", "frames")


def load(f, root):
    return np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)


def cold_mask(a, bmin=150, brmin=60, gtol=12):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (B > bmin) & ((B - R) > brmin) & (B >= G - gtol)


def blobs(m, minpx=12):
    """4-connected components via iterative label propagation (no scipy dep needed)."""
    from scipy import ndimage
    lab, n = ndimage.label(m)
    out = []
    if n == 0:
        return out
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    cy, cx = zip(*ndimage.center_of_mass(m, lab, range(1, n + 1))) if n else ((), ())
    for i in range(n):
        if sizes[i] >= minpx:
            out.append(dict(n=int(sizes[i]), cx=float(cx[i]), cy=float(cy[i])))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, required=True)
    ap.add_argument("--f1", type=int, required=True)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bright", type=int, default=200, help="head brightness floor on B")
    ap.add_argument("--x0", type=int, default=300)
    ap.add_argument("--x1", type=int, default=1500)
    ap.add_argument("--y0", type=int, default=200)
    ap.add_argument("--y1", type=int, default=1000)
    args = ap.parse_args()

    rows = []
    for f in range(args.f0, args.f1 + 1):
        p = os.path.join(args.root, f"f{f:06d}.png")
        if not os.path.exists(p):
            continue
        a = load(f, args.root)
        sub = a[args.y0:args.y1, args.x0:args.x1]
        cm = cold_mask(sub)
        head = cm & (sub[:, :, 2] > args.bright)
        bl = blobs(head, minpx=10)
        for b in bl:
            b["cx"] += args.x0
            b["cy"] += args.y0
        rows.append(dict(f=f, n_cold=int(cm.sum()), n_head=int(head.sum()),
                         blobs=sorted(bl, key=lambda d: -d["n"])[:40]))
        print(f, cm.sum(), head.sum(), len(bl), flush=True)
    json.dump(dict(f0=args.f0, f1=args.f1, rows=rows), open(args.out, "w"))


if __name__ == "__main__":
    main()
