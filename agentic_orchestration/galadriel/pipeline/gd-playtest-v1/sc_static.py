#!/usr/bin/env python3
"""SHADOW-CAL: find camera-static spans from the keyframe ladder.

Adjacent keyframes are 250 source frames (4.1667 s) apart.  If the ground
registers at zero shift between two of them, the camera did not translate over
that whole span -- a window in which a temporal-median background plate is valid.

Shift by FFT phase correlation on the gameplay band, HUD excluded.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

BAND = (slice(30, 300), slice(20, 620))   # in 640x360 coords


def luma(p):
    a = np.asarray(Image.open(p).convert("RGB"), np.float32)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def phase_shift(a, b):
    """Integer (dy, dx) that best aligns b onto a; plus peak sharpness."""
    a = a - a.mean()
    b = b - b.mean()
    win = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1]))
    A = np.fft.rfft2(a * win)
    B = np.fft.rfft2(b * win)
    R = A * np.conj(B)
    m = np.abs(R)
    R = np.where(m > 1e-9, R / m, 0)
    c = np.fft.irfft2(R, s=a.shape)
    idx = np.unravel_index(np.argmax(c), c.shape)
    peak = float(c[idx])
    dy = idx[0] - (a.shape[0] if idx[0] > a.shape[0] // 2 else 0)
    dx = idx[1] - (a.shape[1] if idx[1] > a.shape[1] // 2 else 0)
    return int(dy), int(dx), peak


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=60.0)
    a = ap.parse_args()

    files = sorted(f for f in os.listdir(a.dir) if f.endswith(".jpg"))
    prev = None
    rec = []
    for f in files:
        L = luma(os.path.join(a.dir, f))[BAND]
        n = int(f[1:-4])
        if prev is not None:
            dy, dx, pk = phase_shift(prev[1], L)
            # mean abs difference at zero shift, as a second opinion
            mad = float(np.abs(prev[1] - L).mean())
            rec.append({"frame": n, "t": n / a.fps, "prev_frame": prev[0],
                        "dy": dy, "dx": dx, "peak": pk, "mad": mad})
        prev = (n, L)
    with open(a.out, "w") as fh:
        json.dump(rec, fh)

    d = np.array([[r["dy"], r["dx"]] for r in rec])
    still = (np.abs(d).max(1) == 0)
    print(f"{len(rec)} adjacent keyframe pairs")
    print(f"zero-shift pairs (camera static over the whole 4.17 s): "
          f"{still.sum()} ({100*still.mean():.1f}%)")
    mads = np.array([r["mad"] for r in rec])
    print(f"  of those, MAD median {np.median(mads[still]):.2f} "
          f"(scene change within a static camera = live actors)")
    ts = np.array([r["t"] for r in rec])
    print("first 40 static spans (t of the LATER keyframe):")
    print(np.round(ts[still][:40], 1))
