#!/usr/bin/env python3
"""u7_minimap.py — short-radius heading conditioning off the HUD minimap.

galadriel / visual-perception seam.  KC2 LIFT RUN, ruling R-L6-2, item U-7.

WHY THE MINIMAP AND NOT THE WORLD VIEW
--------------------------------------
The discriminator U-7 asks whether the referent pilot's HEADING is conditioned on
LOCAL BODY DENSITY.  Both terms have to live in one frame.  In the world view they
do not: the player is buried under Crucible wave-150+ VFX, bodies are occluded, and
every screen-space bearing needs an isometric de-projection whose ground map M was
never recovered (2026-08-24 boundary trace, "what the shots cannot support").

The HUD minimap answers both terms in ONE north-up, rigidly player-centred frame:
  * monster icons are drawn on top of everything and are never occluded;
  * the mapped terrain is a fixed world-space image that merely TRANSLATES, so the
    player's displacement is recoverable without any camera model;
  * bearings taken from the disc anchor are already PLAYER-RELATIVE.

Everything this module emits is in MINIMAP PIXELS.  U-9 (ground-px -> metres) is a
DECLARED GAP on this referent and no metric radius is asserted anywhere.

TWO INDEPENDENT DISPLACEMENT ESTIMATORS, BY DESIGN
--------------------------------------------------
E1  teal pedestal-gem fixtures.  World-static, high-contrast, sub-pixel centroids.
    Matched frame-to-frame; the matched-set mean displacement is -(player step).
E2  masked terrain registration (SAD, icons and saturated bleed masked out).
They are cross-checked against each other; the agreement is a reported gate, not an
assumption.

  grab   <video> <t0> <t1> <hz> <out.npy>       decode the minimap crop
  anchor <in.npy> <out.json>                    locate the disc-fixed player arrow
  tracks <in.npy> <anchor.json> <out.json>      per-sample displacement + icon census
"""
from __future__ import annotations

import json
import subprocess
import sys

import numpy as np
from scipy import ndimage as ndi

# --- crop geometry (1920x1080 capture; minimap disc lives top-right) ------------
CROP_X, CROP_Y, CROP_W, CROP_H = 1654, 30, 246, 226
# disc geometry in CROP coordinates, seeded from eor_minimap and refined by ring fit
SEED_CX, SEED_CY, SEED_R = 1776 - CROP_X, 147 - CROP_Y, 94


def grab(video, t0, t1, hz, out):
    """Decode the minimap crop at `hz` into a uint8 array (n, H, W, 3)."""
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-vf", f"fps={hz},crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    nb = CROP_W * CROP_H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=nb * 4)
    frames = []
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        frames.append(np.frombuffer(buf, np.uint8).reshape(CROP_H, CROP_W, 3))
    p.stdout.close(); p.wait()
    a = np.stack(frames)
    np.save(out, a)
    print(f"grab {t0}-{t1} @ {hz}Hz -> {a.shape}")


# --- masks ---------------------------------------------------------------------

def disc_mask(r=None):
    r = SEED_R if r is None else r
    yy, xx = np.mgrid[0:CROP_H, 0:CROP_W]
    return ((xx - SEED_CX) ** 2 + (yy - SEED_CY) ** 2) < r * r


def teal(fr):
    R, G, B = fr[..., 0].astype(int), fr[..., 1].astype(int), fr[..., 2].astype(int)
    return (B > 110) & (G > 105) & ((B - R) > 40) & ((G - R) > 30)


def icon_bright(fr, thr=145):
    """Warm-cream / pale icon pixels: monster stars, skulls, the player arrow."""
    L = fr.astype(np.float32).mean(axis=2)
    return (L > thr) & ~teal(fr)


# --- E1: teal-gem displacement --------------------------------------------------

def gems(fr, dm, min_area=6):
    m = teal(fr) & dm
    lab, n = ndi.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < min_area:
            continue
        out.append((float(xs.mean()), float(ys.mean()), len(ys)))
    return out


def gem_step(g0, g1, maxjump=14.0, min_pairs=3, spread_max=1.5):
    """Rigid translation g0 -> g1 from matched gem centroids.

    Returns (dx, dy, n_pairs, spread) or None.  The spread of the individual pair
    deltas about their own mean is the estimator's self-reported error; a set that
    does not agree with itself is refused rather than averaged.
    """
    if len(g0) < min_pairs or len(g1) < min_pairs:
        return None
    ds = []
    for (x0, y0, a0) in g0:
        best, bd = None, maxjump
        for (x1, y1, a1) in g1:
            d = np.hypot(x1 - x0, y1 - y0)
            if d < bd:
                bd, best = d, (x1 - x0, y1 - y0)
        if best is not None:
            ds.append(best)
    if len(ds) < min_pairs:
        return None
    ds = np.array(ds)
    med = np.median(ds, axis=0)
    keep = ds[np.hypot(ds[:, 0] - med[0], ds[:, 1] - med[1]) <= 3.0]
    if len(keep) < min_pairs:
        return None
    mu = keep.mean(axis=0)
    spread = float(np.hypot(*(keep.std(axis=0))))
    if spread > spread_max:
        return None
    return float(mu[0]), float(mu[1]), len(keep), spread


# --- E2: masked terrain registration -------------------------------------------

def terrain_step(f0, f1, dm, S=14):
    """Integer SAD translation f0 -> f1 on masked terrain, parabola-refined."""
    l0 = f0.astype(np.float32).mean(axis=2)
    l1 = f1.astype(np.float32).mean(axis=2)
    w0 = dm & (l0 < 140) & ~teal(f0)
    w1 = dm & (l1 < 140) & ~teal(f1)
    H, W = l0.shape
    cost = np.full((2 * S + 1, 2 * S + 1), np.nan)
    for dy in range(-S, S + 1):
        for dx in range(-S, S + 1):
            y0a, y1a = max(0, dy), min(H, H + dy)
            x0a, x1a = max(0, dx), min(W, W + dx)
            wgt = w0[y0a:y1a, x0a:x1a] & w1[y0a - dy:y1a - dy, x0a - dx:x1a - dx]
            if wgt.sum() < 1500:
                continue
            d = np.abs(l0[y0a:y1a, x0a:x1a] - l1[y0a - dy:y1a - dy, x0a - dx:x1a - dx])
            cost[dy + S, dx + S] = float(d[wgt].mean())
    if np.all(np.isnan(cost)):
        return None
    iy, ix = np.unravel_index(np.nanargmin(cost), cost.shape)
    if iy in (0, 2 * S) or ix in (0, 2 * S):
        return None
    c0 = cost[iy, ix]
    sub = [0.0, 0.0]
    for k, (a, b) in enumerate([(cost[iy, ix - 1], cost[iy, ix + 1]),
                                (cost[iy - 1, ix], cost[iy + 1, ix])]):
        den = (a - 2 * c0 + b)
        sub[k] = 0.0 if den == 0 or np.isnan(den) else float(0.5 * (a - b) / den)
        sub[k] = max(-1.0, min(1.0, sub[k]))
    # peak sharpness: best cost vs the best cost outside a radius-2 exclusion
    yy, xx = np.mgrid[0:2 * S + 1, 0:2 * S + 1]
    far = np.hypot(xx - ix, yy - iy) > 2.5
    c_far = np.nanmin(cost[far]) if np.any(far & ~np.isnan(cost)) else np.nan
    return (float(ix - S + sub[0]), float(iy - S + sub[1]), float(c0),
            float(c_far - c0) if not np.isnan(c_far) else float("nan"))


# --- anchor ---------------------------------------------------------------------

def anchor(inp, out, stride=7):
    """The player arrowhead is the ONLY disc-fixed icon; find it as the persistent
    peak of the icon mask over the window."""
    a = np.load(inp, mmap_mode="r")
    dm = disc_mask(SEED_R - 4)
    acc = np.zeros((CROP_H, CROP_W), np.float64)
    n = 0
    for i in range(0, len(a), stride):
        acc += (icon_bright(np.asarray(a[i])) & dm)
        n += 1
    frac = acc / n
    sm = ndi.gaussian_filter(frac, 1.0)
    iy, ix = np.unravel_index(np.argmax(sm), sm.shape)
    # centroid of the persistent core
    core = frac >= 0.6 * frac[iy, ix]
    lab, _ = ndi.label(core)
    sel = lab == lab[iy, ix]
    ys, xs = np.nonzero(sel)
    cx, cy = float(xs.mean()), float(ys.mean())
    disp = float(np.hypot(xs - cx, ys - cy).max())
    res = {"n_frames_used": n, "peak_frac": float(frac[iy, ix]),
           "anchor_crop_xy": [round(cx, 2), round(cy, 2)],
           "anchor_fullframe_xy": [round(cx + CROP_X, 2), round(cy + CROP_Y, 2)],
           "core_radius_px": round(disp, 2),
           "core_area_px": int(sel.sum()),
           "seed_disc_centre_crop": [SEED_CX, SEED_CY]}
    json.dump(res, open(out, "w"), indent=1)
    np.save(out.replace(".json", "_frac.npy"), frac.astype(np.float32))
    print(json.dumps(res, indent=1))


# --- per-sample census ----------------------------------------------------------

def tracks(inp, anchor_json, out, hz=10.0, t0=0.0, r_ex=7.0, r_max=64.0):
    a = np.load(inp, mmap_mode="r")
    an = json.load(open(anchor_json))
    ax, ay = an["anchor_crop_xy"]
    dm = disc_mask(SEED_R - 4)
    yy, xx = np.mgrid[0:CROP_H, 0:CROP_W]
    rr = np.hypot(xx - ax, yy - ay)
    body_zone = dm & (rr > r_ex) & (rr <= r_max)
    rows = []
    prev = None
    for i in range(len(a)):
        fr = np.asarray(a[i])
        t = round(t0 + i / hz, 4)
        g = gems(fr, dm)
        mb = icon_bright(fr) & body_zone
        ys, xs = np.nonzero(mb)
        r = rr[ys, xs]
        row = {"t": t, "n_gem": len(g),
               "px": [[int(x), int(y)] for x, y in zip(xs, ys)] if len(xs) < 4000 else None,
               "n_body_px": int(len(xs)),
               "gem": [[round(x, 3), round(y, 3), n] for x, y, n in g]}
        rows.append(row)
        prev = fr
    json.dump({"input": inp, "hz": hz, "t0": t0, "anchor": [ax, ay],
               "r_ex": r_ex, "r_max": r_max, "rows": rows}, open(out, "w"))
    print(f"tracks: {len(rows)} samples")


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "grab":
        grab(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
             float(sys.argv[5]), sys.argv[6])
    elif c == "anchor":
        anchor(sys.argv[2], sys.argv[3])
    elif c == "tracks":
        tracks(sys.argv[2], sys.argv[3], sys.argv[4],
               hz=float(sys.argv[5]), t0=float(sys.argv[6]))
