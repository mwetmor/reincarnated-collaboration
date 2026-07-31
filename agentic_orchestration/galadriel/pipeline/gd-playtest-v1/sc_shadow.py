#!/usr/bin/env python3
"""SHADOW-CAL instrument SC-1: separate CAST SHADOW from SPRITE, against a
temporal-median background plate.

WHY A BACKGROUND PLATE
----------------------
A shadow in a game frame is not "the dark pixels".  Grim Dawn's ground is dark,
mottled and textured; a luma threshold measures the floor, not the shadow.
What makes a shadow a shadow is that it is the SAME GROUND, MULTIPLIED DOWN:
the texture survives, the level drops.  So the discriminator is

    rho  = L_frame / L_plate            (how much darker)
    ncc  = local normalised correlation  (did the texture survive?)

A cast shadow scores rho < 1 with ncc ~ 1.  A sprite scores ncc low, because it
replaces the texture rather than scaling it.  Untextured plate patches carry no
correlation signal and are reported as such, not silently included.

The plate is the per-pixel temporal median over a camera-static window, so
"surround" is the SAME PIXELS unshadowed -- floor texture cancels by
construction, which is what makes the (c) contrast question answerable at all.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

HUD_KEEP = (slice(60, 950), slice(0, 1920))   # rows outside the HUD plates


def load(paths):
    return np.stack([np.asarray(Image.open(p).convert("RGB"), np.float32)
                     for p in paths])


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def local_ncc(f, b, k=9):
    """Local normalised cross-correlation of two images, k x k windows."""
    ones = lambda x: ndimage.uniform_filter(x, k, mode="nearest")
    mf, mb = ones(f), ones(b)
    vf = ones(f * f) - mf * mf
    vb = ones(b * b) - mb * mb
    cv = ones(f * b) - mf * mb
    den = np.sqrt(np.maximum(vf, 1e-6) * np.maximum(vb, 1e-6))
    return cv / den, np.sqrt(np.maximum(vb, 0.0))


def separate(frame, plate, sigma=None, rho_hi=0.93, rho_lo=0.12, ncc_min=0.72,
             sd_min=2.5, dl_floor=7.0, nsig=3.5, k=9):
    """Return dict of boolean masks + the fields they were cut from.

    `sigma` is the per-pixel temporal MAD of the registered stack (sc_plate).
    The change threshold is max(dl_floor, nsig*sigma), so a pixel that is
    ALWAYS restless -- swaying grass, animated water, flickering firelight --
    has to move much further than a quiet floor pixel before it counts.  Without
    it this instrument reads torch flicker as a cast shadow: texture survives a
    flicker exactly as it survives an occlusion.
    """
    Lf, Lb = luma(frame), luma(plate)
    rho = (Lf + 4.0) / (Lb + 4.0)
    ncc, sdb = local_ncc(Lf, Lb, k)
    dl = Lf - Lb
    if sigma is None:
        sigma = np.zeros_like(Lf)
    tau = np.maximum(dl_floor, nsig * sigma)
    changed = np.abs(dl) > tau

    textured = sdb > sd_min
    shadow = changed & (rho < rho_hi) & (rho > rho_lo) & (ncc > ncc_min) & textured
    sprite = changed & (ncc < 0.45)
    undecided = changed & (~shadow) & (~sprite)

    m = np.zeros_like(Lf, bool)
    m[HUD_KEEP] = True
    return {"shadow": shadow & m, "sprite": sprite & m,
            "undecided": undecided & m, "rho": rho, "ncc": ncc, "tau": tau,
            "dl": dl, "Lf": Lf, "Lb": Lb, "textured": textured & m,
            "changed": changed & m}


def clean(mask, open_r=2, close_r=3, min_px=120):
    m = ndimage.binary_opening(mask, np.ones((open_r, open_r)))
    m = ndimage.binary_closing(m, np.ones((close_r, close_r)))
    lab, n = ndimage.label(m)
    if n == 0:
        return m, lab, []
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    keep = [i + 1 for i in range(n) if sizes[i] >= min_px]
    out = np.isin(lab, keep)
    return out, lab, keep


def plate_median(stack):
    return np.median(stack, axis=0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--idx", type=int, default=None,
                    help="frame index to render; default = middle")
    a = ap.parse_args()

    paths = sorted(os.path.join(a.dir, f) for f in os.listdir(a.dir)
                   if f.endswith((".png", ".jpg")))
    st = load(paths)
    plate = plate_median(st)
    i = a.idx if a.idx is not None else len(paths) // 2
    r = separate(st[i], plate)
    sh, _, _ = clean(r["shadow"])
    sp, _, _ = clean(r["sprite"], min_px=60)

    vis = st[i].copy()
    vis[sh] = vis[sh] * 0.3 + np.array([255, 40, 40]) * 0.7
    vis[sp] = vis[sp] * 0.3 + np.array([40, 160, 255]) * 0.7
    Image.fromarray(vis.astype(np.uint8)).save(a.out, quality=92)
    print(f"{len(paths)} frames; shadow px {sh.sum()}, sprite px {sp.sum()}, "
          f"undecided px {r['undecided'].sum()} -> {a.out}")
