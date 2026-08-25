#!/usr/bin/env python3
"""gd_arena_trace.py — Crucible-of-the-Dead arena boundary trace.

galadriel / visual-perception seam.  KC2 MODEL-COMPLETION run, (h-a') baton row,
conductor ruling R-L64-1.

Input : 21 Grim Dawn 1920x1080 captures of Matt's continuous perimeter walk
        (`Screenshot (612).png` .. `Screenshot (632).png`).
Method: the HUD minimap is a north-up, PLAYER-CENTRED disc.  The mapped arena
        terrain inside it is a fixed world-space image that TRANSLATES as the
        player moves.  Masked normalised cross-correlation of consecutive discs
        therefore recovers (a) a single mosaic of the whole arena footprint and
        (b) the player's arena-local track, in minimap pixels.

        The world view is then tied to the minimap by pairing, per consecutive
        shot pair, the screen-space translation of the static world with the
        minimap-space displacement of the player.  Least-squares over all pairs
        yields a 2x2 ground-plane matrix M (screen px per minimap px).  SVD of M
        gives the camera pitch; the character-height anchor then gives metres.

Nothing here invents a rule.  Everything is a measurement of the reference with
a stated assumption and a stated uncertainty.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image
from scipy.signal import fftconvolve

CAP = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "captures", "2026-08-24-crucible-arena-perimeter",
)
SHOTS = list(range(612, 633))

# --- minimap disc geometry, fitted from the bright ring of shot 612 -----------
# iterative algebraic circle fit on luminance>110 pixels gated to |d-r|<0.1r
MM_CX, MM_CY = 1771.98, 172.63     # full-frame px; == the player's world position
MM_RING_R = 126.63                 # bright ring centreline
MM_CONTENT_R = 119.0               # usable map content inside the ring bevel
MM_ARROW_R = 10.0                  # player arrowhead occludes the disc centre

# HUD furniture that overlaps the disc: the gold "N" ornament + compass letter.
MM_TOP_WEDGE = dict(rmin=95.0, half_deg=11.0)   # centred on north


def disc(path):
    """Return (grayscale float array, valid mask) for one minimap disc."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float64)
    x0, y0 = int(MM_CX - 140), 0
    sub = im[y0:y0 + 320, x0:x0 + 280]
    g = sub.mean(axis=2)
    h, w = g.shape
    yy, xx = np.mgrid[0:h, 0:w]
    dx, dy = xx - (MM_CX - x0), yy - (MM_CY - y0)
    d = np.hypot(dx, dy)
    m = (d < MM_CONTENT_R) & (d > MM_ARROW_R)
    ang = np.degrees(np.arctan2(dx, -dy))          # 0 = north, +ve = east
    m &= ~((d > MM_TOP_WEDGE["rmin"]) & (np.abs(ang) < MM_TOP_WEDGE["half_deg"]))
    return g, m


def masked_ncc(f, mf, g, mg, max_shift):
    """Padfield masked normalised cross-correlation.

    Returns (dy, dx, peak) where shifting `g` by (dy,dx) aligns it onto `f`.
    """
    f = f * mf
    g = g * mg
    mfF, mgF = mf.astype(np.float64), mg.astype(np.float64)

    def corr(a, b):
        return fftconvolve(a, b[::-1, ::-1], mode="full")

    N = corr(mfF, mgF)
    Sfg = corr(f, g)
    Sf = corr(f, mgF)
    Sg = corr(mfF, g)
    Sf2 = corr(f * f, mgF)
    Sg2 = corr(mfF, g * g)

    with np.errstate(divide="ignore", invalid="ignore"):
        num = Sfg - Sf * Sg / N
        d1 = Sf2 - Sf ** 2 / N
        d2 = Sg2 - Sg ** 2 / N
        den = np.sqrt(np.clip(d1, 0, None) * np.clip(d2, 0, None))
        ncc = np.where(den > 1e-9, num / den, 0.0)

    ncc[N < 0.30 * mfF.sum()] = 0.0            # demand real overlap
    h, w = f.shape
    cy, cx = h - 1, w - 1                       # zero-shift index in 'full'
    yy, xx = np.mgrid[0:ncc.shape[0], 0:ncc.shape[1]]
    ncc[np.hypot(yy - cy, xx - cx) > max_shift] = 0.0
    k = int(np.argmax(ncc))
    py, px = divmod(k, ncc.shape[1])
    return py - cy, px - cx, float(ncc[py, px])


def world(path):
    """Grayscale world view with HUD regions masked out."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float64)
    g = im.mean(axis=2)
    m = np.ones(g.shape, bool)
    m[0:340, 1580:1920] = False        # minimap + objectives
    m[0:120, 1280:1620] = False        # centre HUD bar / xp
    m[930:1080, :] = False             # action bar + globes
    m[0:60, 0:260] = False             # char name + clock
    m[380:460, 780:1140] = False       # floating HP bar over the player
    return g, m


def main():
    paths = [os.path.join(CAP, f"Screenshot ({n}).png") for n in SHOTS]
    discs = [disc(p) for p in paths]
    worlds = [world(p) for p in paths]

    # --- sequential minimap registration -------------------------------------
    track = [(0.0, 0.0)]
    mm_steps, wv_steps, peaks = [], [], []
    for i in range(len(paths) - 1):
        f, mf = discs[i]
        g, mg = discs[i + 1]
        dy, dx, pk = masked_ncc(f, mf, g, mg, max_shift=110)
        # (dy,dx) shifts shot i+1's terrain onto shot i's frame.  The terrain
        # moves opposite to the player, so the player's displacement is -(dy,dx).
        mm_steps.append((-dx, -dy))
        peaks.append(pk)
        track.append((track[-1][0] - dx, track[-1][1] - dy))

        wf, wmf = worlds[i]
        wg, wmg = worlds[i + 1]
        sy, sx, spk = masked_ncc(wf[::2, ::2], wmf[::2, ::2],
                                 wg[::2, ::2], wmg[::2, ::2], max_shift=200)
        wv_steps.append((sx * 2, sy * 2, spk))

    out = dict(
        shots=SHOTS,
        track_minimap_px=[[round(a, 2), round(b, 2)] for a, b in track],
        mm_steps=[[round(a, 2), round(b, 2)] for a, b in mm_steps],
        mm_peaks=[round(p, 4) for p in peaks],
        wv_steps=[[a, b, round(c, 4)] for a, b, c in wv_steps],
    )
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "gd-arena-trace-registration.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    for n, t, p in zip(SHOTS, track, [1.0] + peaks):
        print(f"{n}  track=({t[0]:8.1f},{t[1]:8.1f})  ncc={p:.3f}")


if __name__ == "__main__":
    main()
