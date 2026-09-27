#!/usr/bin/env python3
"""C-9 R-C9-40 part 2: how many STRIDES does each Grok 12-frame loop actually contain?

Matt: "some of the walks and runs are too fast (roughly double) compared to what they
should be."  build_knight_frames.py sets every cell's playback from

    fps_D = 12 / keeper_stride_D

which is right only if the loop holds exactly ONE stride.  Where the cut caught two,
the knight takes four steps in the time the Keeper takes two -- exactly the doubling
Matt saw, and exactly where he saw it.

MEASURING IT.  The conductor's census counted peaks of foot separation, and got 3
peaks for several cells, which cannot happen: separation peaks twice per stride, so an
honest count is even.  The trouble is that a walk's two halves are near MIRRORS of each
other, and a silhouette cannot tell a left foot from a right one -- so a one-stride
loop and a two-stride loop have the same separation signal.  Counting harder does not
fix an ambiguous signal.

So this asks a question the whole frame can answer.  A k-stride loop repeats every
12/k frames -- INCLUDING the pollaxe, the far arm, the tabard and the shading, which do
NOT mirror between the halves of a stride.  So:

    D(p) = mean frame-to-frame distance between frame i and frame i+p (cyclic)

has a deep minimum at p = 12/k and a maximum at p = 6/k.  Two strides means D(6) is
near zero while D(3) is large; one stride means D(6) is the LARGEST value in the
profile.  The discriminator is the ratio, not a threshold on either one, so it does not
care how much the clip drifts.

The foot-separation count is still computed and printed -- as a cross-check that has to
agree in parity, not as the decider.

A THIRD ROUTE WAS TRIED AND ABANDONED, and it is worth saying why, because it looks
like the obvious one: measure the period on the SOURCE clip (145 frames at 24 fps,
twelve times the samples) and divide `stride_native_frames` by it.  It cannot work.
These clips are cinematic -- 44 to 92 native frames per stride -- so a 145-frame clip
holds about one and a half strides, and there is no periodicity in it to find.  Both
attempts returned confident numbers anyway: a mean-difference profile fell monotonically
and returned the search's own upper bound for all sixteen clips, and a normalised
autocorrelation then returned the lower bound for all sixteen.  Neither looked like an
error; both looked like answers.  The tool was deleted rather than shipped.

Writes frames/knight_stride_census.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PROJ = Path(__file__).resolve().parent.parent
RUNS_ROOT = PROJ.parents[2]
OUT = PROJ / "frames" / "knight_stride_census.json"
DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]


def load(cell_frames):
    ims = []
    for rel in cell_frames:
        p = RUNS_ROOT / rel
        a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32) / 255.0
        ims.append(a)
    return ims


def align(a):
    """Centre each frame on its own silhouette centroid, so a cell that pans (the
    figure walks across its own canvas) is compared pose to pose rather than
    position to position."""
    m = a[..., 3] > 0.3
    if not m.any():
        return a
    ys, xs = np.nonzero(m)
    dy = int(round(a.shape[0] / 2 - ys.mean()))
    dx = int(round(a.shape[1] / 2 - xs.mean()))
    return np.roll(np.roll(a, dy, 0), dx, 1)


def profile(ims):
    """D(p) for p = 1..6, on premultiplied RGB so shape and paint both count."""
    A = [align(i) for i in ims]
    P = [i[..., :3] * i[..., 3:4] for i in A]
    n = len(P)
    out = {}
    for p in range(1, n // 2 + 1):
        d = [float(np.abs(P[i] - P[(i + p) % n]).mean()) for i in range(n)]
        out[p] = float(np.mean(d))
    return out


def foot_fft(ims):
    """Dominant harmonic of the foot-separation signal over the 12-frame loop.

    A 12-sample cyclic signal: harmonic k means k oscillations per loop.  Separation
    peaks once per STEP, so k=2 is one stride and k=4 is two.  This is a PARITY check
    and nothing more -- it cannot tell a stride from its mirror, because a silhouette
    has no left and right, which is why the conductor's peak-count came back odd (3)
    for several cells.  A count of half-strides cannot honestly be odd.
    """
    sep = []
    for a in ims:
        m = a[..., 3] > 0.3
        ys, xs = np.nonzero(m)
        if len(ys) == 0:
            sep.append(0.0)
            continue
        sole = int(ys.max())
        h = max(3, (int(ys.max()) - int(ys.min())) // 12)
        band = m[max(0, sole - h):sole + 1]
        bx = np.nonzero(band.any(0))[0]
        sep.append(float(bx.max() - bx.min()) if len(bx) else 0.0)
    v = np.array(sep) - np.mean(sep)
    X = np.abs(np.fft.rfft(v))
    return int(np.argmax(X[1:]) + 1), [round(x, 1) for x in sep], \
        {str(k): round(float(X[k]), 1) for k in range(1, 7)}


def strides_of(D, k_fft):
    """1 or 2, from the two instruments, by a stated rule.

    D(6)/D(3) is the one that can actually COUNT: it compares whole frames, and the
    pollaxe, the far arm and the tabard's red flap do not swap sides between the halves
    of a stride, so a low D(6) means the loop really does repeat, not that it mirrors.
    Its weakness is margin, not validity.  The foot FFT has the resolution but not the
    authority, so it is allowed to break a tie and never to overrule a clear reading.

    Six of these were then checked by eye, half against half (walk_S, walk_SE, run_NW,
    run_S, run_SW, run_W): all six agreed with this rule.
    """
    r = D[6] / D[3]
    if r < 0.60:
        return 2, "D(6)/D(3)=%.2f < 0.60" % r
    if k_fft == 4 and r < 0.85:
        return 2, "D(6)/D(3)=%.2f and the foot signal peaks at 4 steps/loop" % r
    return 1, "D(6)/D(3)=%.2f" % r


def main():
    man = json.loads((PROJ.parent / "artifacts" / "knight_cells_manifest.json").read_text())
    cells = dict(man["cells"])
    rm = PROJ / "frames" / "knight_run_cells.json"
    if rm.exists():
        cells.update(json.loads(rm.read_text())["cells"])
    fit = json.loads((PROJ / "frames" / "knight_fit.json").read_text())
    kw = fit["keeper_walk_stride_seconds"]
    kr = fit.get("keeper_run_stride_seconds", {})

    rows, out = [], {}
    print("%-9s %7s %6s %6s %6s  %5s %5s  %7s %8s %8s"
          % ("cell", "D(6)", "D(3)", "D(2)", "D(1)", "ratio", "peaks",
             "strides", "old fps", "new fps"))
    for st in ("walk", "run"):
        for d in DIRS:
            key = "%s_%s" % (st, d)
            if key not in cells:
                continue
            ims = load(cells[key]["frames"])
            D = profile(ims)
            k_fft, sep, X = foot_fft(ims)
            k, why = strides_of(D, k_fft)
            peaks = k_fft
            stride = (kw if st == "walk" else kr)[d]
            old = 12.0 / stride
            new = 12.0 / (k * stride)
            print("%-9s %7.4f %6.4f %6.4f %6.4f  %5.2f %5d  %7d %8.3f %8.3f%s"
                  % (key, D[6], D[3], D[2], D[1], D[6] / D[3], peaks, k, old, new,
                     "   <== HALVED" if k > 1 else ""))
            out[key] = {"strides_in_loop": k, "D": {str(p): round(v, 5) for p, v in D.items()},
                        "ratio_D6_over_D3": round(D[6] / D[3], 4),
                        "reason": why,
                        "foot_fft_dominant_k": k_fft,
                        "foot_fft_magnitudes": X,
                        "foot_separation_px": sep,
                        "keeper_stride_s": stride,
                        "fps_old": round(old, 4), "fps_new": round(new, 4)}
            rows.append(key)
    agree = [k for k, v in out.items()
             if v["foot_fft_dominant_k"] == 2 * v["strides_in_loop"]]
    print("\nfoot-signal parity cross-check: %d of %d cells have the foot FFT peaking "
          "at exactly 2 x strides" % (len(agree), len(out)))
    for k in sorted(out):
        if k not in agree:
            print("   %-9s foot FFT k=%d, verdict %d stride(s)  [%s]"
                  % (k, out[k]["foot_fft_dominant_k"], out[k]["strides_in_loop"],
                     out[k]["reason"]))
    OUT.write_text(json.dumps(
        {"note": "C-9 R-C9-40: strides per 12-frame Grok loop, from whole-frame "
                 "self-similarity. Read by tools/build_knight_frames.py to set playback.",
         "cells": out}, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
