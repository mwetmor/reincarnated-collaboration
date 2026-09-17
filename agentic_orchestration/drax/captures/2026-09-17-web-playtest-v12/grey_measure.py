#!/usr/bin/env python3
"""web12 grey-peak measure. drax, 2026-09-17.

Two corrections over the web11 instrument, both found by the instrument returning
cleanly and answering the wrong question:

1. REFERENCE FRAME. web11 differenced the cast frames against a pre-cast frame taken
   before the Keeper moved. Between those two frames the camera had panned, so the
   diff mask was mostly camera drift. Here the reference is the ADJACENT frame of the
   SAME cast (f1), during which the Keeper is frozen in the cast state and the camera
   is static. Control: two adjacent non-VFX frames differ by ~300 px, so the mask is
   real VFX, not drift.

2. WHAT "GREY" MEANS. web11's criterion was saturation < 28 AND max channel > 110.
   That catches an unshaded index map (mid-grey, "pale metallic fans") AND a
   white-hot flame core (near-white) with equal enthusiasm. fire_bolt_e1_B has a
   white-hot core by design, so the raw criterion reads 11-13 % on a perfectly
   healthy kit. Split the desaturated pixels by MAX CHANNEL: 235-256 is the
   white-hot core (art); 110-235 is the unshaded-index-map band that web11's defect
   actually occupied.

usage: python3 grey_measure.py
"""
import numpy as np
from PIL import Image
import pathlib

OUT = pathlib.Path(__file__).resolve().parent


def arr(n, tag):
    return np.asarray(Image.open(OUT / f"tcast_{n:02d}_{tag}.png").convert("RGB")).astype(np.int16)


def measure(label, a, ref, x0, x1):
    m = (np.abs(a - ref).max(axis=2) > 34)
    win = np.zeros(m.shape, bool)
    win[:, x0:x1] = True
    m &= win
    px = a[m]
    n = len(px)
    if n == 0:
        print(f"{label:34s} px=     0  (no changed pixels in this window)")
        return
    mx = px.max(axis=1)
    desat = (mx - px.min(axis=1) < 28) & (mx > 110)
    core = int((desat & (mx >= 235)).sum())
    unshaded = int((desat & (mx < 235)).sum())
    warm = int((px[:, 0] > px[:, 2] + 40).sum())
    print(f"{label:34s} px={n:6d}  white-hot core={100*core/n:5.2f}%  "
          f"UNSHADED-GREY={100*unshaded/n:5.2f}%  warm={100*warm/n:5.1f}%")


if __name__ == "__main__":
    # Camera-stability controls: two adjacent frames with no VFX in either.
    measure("CONTROL cast1 f2 vs f1", arr(6, "cast1_f2"), arr(5, "cast1_f1"), 0, 1688)
    measure("CONTROL cast2 f3 vs f2", arr(13, "cast2_f3"), arr(12, "cast2_f2"), 0, 1688)
    print()
    # VFX windows picked from the changed-pixel x-histogram; they exclude the Keeper
    # sprite (his own cast animation changes, and his shirt is white) and the animated
    # campfire at x ~350-450.
    measure("cast1 impact fan  x1000-1360", arr(4, "cast1_f0"), arr(5, "cast1_f1"), 1000, 1360)
    measure("cast2 bolt aloft  x880-1010", arr(10, "cast2_f0"), arr(11, "cast2_f1"), 880, 1010)
    measure("cast3 bolt aloft  x930-1110", arr(16, "cast3_f0"), arr(17, "cast3_f1"), 930, 1110)
    # By f3 the impact flash is already gone: the only thing still changing is the
    # Keeper returning to idle. A bolt kit has no lap-3 residue phase the way the
    # burst kits do, so this window is expected to be empty.
    measure("cast1 residue     x1000-1360", arr(7, "cast1_f3"), arr(9, "cast1_f5"), 1000, 1360)
