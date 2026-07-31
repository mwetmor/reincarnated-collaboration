#!/usr/bin/env python3
"""SHADOW-CAL instrument SC-7: which SIDE of the player is his shadow on?

WHY ONLY THE SIDE, AND WHY THAT IS ENOUGH
-----------------------------------------
A single frame cannot separate "dark ground up-screen of the player" from "the
player's own sprite", because the sprite is drawn ABOVE its ground contact and
a screen pixel above the contact point unprojects to ground BEYOND it.  Any
instrument that samples up-screen rays is therefore biased toward reporting an
up-screen shadow.  This one refuses that measurement.

What is NOT confounded is the LEFT/RIGHT axis: the sprite straddles its own
ground contact in x, so a left-right asymmetry in ground darkness cannot be
manufactured by the sprite.  So SC-7 measures exactly that, on ground sectors
that start beyond the sprite's own half-width, at the player anchor GAL-CAM
MEASURED -- (962, 595), not a guess.

    A = (L_right - L_left) / (L_right + L_left)      A > 0  =>  darker on the LEFT

Constancy of the sign of A across the whole session, across every area, is the
load-bearing half of question (a): one author, one direction, everywhere.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image

import sc_cam

ANCHOR = (962.0, 595.0)
R_IN, R_OUT, NRAD = 1.00, 2.70, 18
HALF_SECTOR = 42.0          # degrees either side of the +/-X axis
NANG = 21
DARK_Q = 0.30               # the shadow is a MINORITY of each sector's samples


def sectors(cam, anchor=ANCHOR, dz=0.0):
    """Left/right ground sectors around a point dz metres up-screen of the anchor.

    dz = 0 -> the player.  dz = -5 -> five metres DOWN-screen of him, where
    there is no player and no player shadow: the PAIRED CONTROL.  Terrain has
    its own left/right tendencies (a wall on one side, water on the other); the
    control carries them and the difference does not.
    """
    g = cam.unproject_ground([[anchor[0], anchor[1]]])
    gx, gz = float(g[0]), float(g[2]) + dz
    rad = np.linspace(R_IN, R_OUT, NRAD)
    out = {}
    for name, centre in (("right", 0.0), ("left", 180.0)):
        ang = np.radians(np.linspace(centre - HALF_SECTOR,
                                     centre + HALF_SECTOR, NANG))
        P = np.empty((NANG, NRAD, 3))
        P[..., 0] = gx + rad[None, :] * np.cos(ang)[:, None]
        P[..., 1] = 0.0
        P[..., 2] = gz + rad[None, :] * np.sin(ang)[:, None]
        uv = cam.project(P.reshape(-1, 3))
        out[name] = uv
    return out


def measure(path_or_arr, uv, ):
    a = (np.asarray(Image.open(path_or_arr).convert("RGB"), np.float32)
         if isinstance(path_or_arr, str) else np.asarray(path_or_arr, np.float32))
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    vals = {}
    for k, p in uv.items():
        x = np.clip(np.round(p[:, 0]).astype(int), 0, L.shape[1] - 1)
        y = np.clip(np.round(p[:, 1]).astype(int), 0, L.shape[0] - 1)
        vals[k] = L[y, x]
    # a shadow occupies only part of a sector, so the sector is summarised by
    # the mean of its DARKEST DARK_Q fraction -- a median would average the
    # shadow away, which is exactly what the first tuning did (control: signal
    # and null both returned A = +0.0159)
    def dark(v):
        return float(np.mean(np.sort(v)[:max(3, int(DARK_Q * len(v)))]))
    lr, ll = dark(vals["right"]), dark(vals["left"])
    if lr + ll < 8:
        return None
    return {"L_right": lr, "L_left": ll,
            "L_right_med": float(np.median(vals["right"])),
            "L_left_med": float(np.median(vals["left"])),
            "A": (lr - ll) / (lr + ll),
            "spread_right": float(np.std(vals["right"])),
            "spread_left": float(np.std(vals["left"]))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--survey", default=None)
    ap.add_argument("--uifrac", default=None)
    ap.add_argument("--fps", type=float, default=60.0)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    uv = sectors(cam)
    uvc = sectors(cam, dz=-5.0)          # paired control, 5 m down-screen
    files = sorted(f for f in os.listdir(a.dir) if f.endswith(".jpg"))
    rec = []
    for f in files:
        arr = np.asarray(Image.open(os.path.join(a.dir, f)).convert("RGB"),
                         np.float32)
        r = measure(arr, uv)
        c = measure(arr, uvc)
        if r is None or c is None:
            continue
        r["A_ctrl"] = c["A"]
        r["dA"] = r["A"] - c["A"]
        r["ctrl_L_left"] = c["L_left"]
        r["ctrl_L_right"] = c["L_right"]
        r["frame"] = int(f[1:-4])
        r["t"] = r["frame"] / a.fps
        rec.append(r)
    json.dump(rec, open(a.out, "w"))
    A = np.array([r["A"] for r in rec])
    print(f"n = {len(rec)} keyframes")
    print(f"  A median {np.median(A):+.4f}  mean {A.mean():+.4f}  sd {A.std():.4f}")
    print(f"  darker on the LEFT in {100*(A>0).mean():.1f}% of frames")
    dA = np.array([r["dA"] for r in rec])
    Ac = np.array([r["A_ctrl"] for r in rec])
    print(f"  control A (5 m down-screen, no player): median {np.median(Ac):+.4f}")
    print(f"  PAIRED dA = A_player - A_control: median {np.median(dA):+.4f}  "
          f"positive in {100*(dA>0).mean():.1f}% of frames")
