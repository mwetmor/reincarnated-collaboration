#!/usr/bin/env python3
"""u7_analyse.py — the U-7 statistic: heading vs local-body-density bearing.

galadriel / visual-perception seam.  KC2 LIFT RUN ruling R-L6-2, item U-7.
Decision rule pre-registered at
  agentic_orchestration/galadriel/notes/2026-08-25-kc2-lift-b1-footage-lap/prereg.md
and committed ALONE (459d5610) before this file computed anything.

EVERY radius is in MINIMAP PIXELS.  U-9 (ground-px -> metres) is a declared gap on
this referent and no metric radius is asserted.

  run <mm.npy> <out.json>
"""
from __future__ import annotations

import json
import math
import sys

import numpy as np
from scipy import ndimage as ndi

CROP_X, CROP_Y = 1654, 30
HZ = 10.0
T0 = 682.10

# --- geometry, DERIVED (not seeded) --------------------------------------------
# player marker = the only disc-FIXED icon; located as the local minimum of the
# temporal-variance image (u7_sd.npy).  Cross-checks the 2026-08-24 perimeter lap's
# independently fitted disc centre (1771.98, 172.63) to 0.30 px in x, 0.04 px in y.
ANCHOR = (117.68, 142.67)                 # crop coords
CONTENT_CLEARANCE_MIN = 82.0              # px, min over 72 bearings (due south)

R_EX = 7.0                                # exclude the player's own arrow
R_MAX = 64.0                              # < CONTENT_CLEARANCE_MIN in every bearing
RADII = [12, 16, 20, 25, 30, 36, 44, 52, 60]

B_SAMPLES = 5                             # heading baseline 0.5 s at 10 Hz
D_MIN = 3.0                               # px over the baseline; below this: no heading

SHIFT_LO, SHIFT_HI = 20, 900              # time-shift null: |lag| in samples (2..90 s)
N_BOOT = 2000
BLOCK = 50                                # 5 s blocks


# --- masks ---------------------------------------------------------------------

def teal(fr):
    R, G, B = fr[..., 0].astype(np.int16), fr[..., 1].astype(np.int16), fr[..., 2].astype(np.int16)
    return (B > 110) & (G > 105) & ((B - R) > 40) & ((G - R) > 30)


def icons(fr, thr=145):
    L = fr.astype(np.float32).mean(axis=2)
    return (L > thr) & ~teal(fr)


# --- per-frame extraction -------------------------------------------------------

def extract(path):
    a = np.load(path, mmap_mode="r")
    n, H, W, _ = a.shape
    ax, ay = ANCHOR
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.hypot(xx - ax, yy - ay)
    zone = (rr > R_EX) & (rr <= R_MAX)
    gem_zone = rr <= 78.0
    zone_r = rr[zone]
    zone_x = (xx[zone] - ax)
    zone_y = (yy[zone] - ay)

    gems, cent = [], {R: np.full((n, 2), np.nan) for R in RADII}
    cnt = {R: np.zeros(n, int) for R in RADII}
    gem_cent = np.full((n, 2), np.nan)
    for i in range(n):
        fr = np.asarray(a[i])
        # gems (world-static fixtures)
        tm = teal(fr) & gem_zone
        lab, k = ndi.label(tm)
        g = []
        if k:
            objs = ndi.find_objects(lab)
            for j in range(1, k + 1):
                ys, xs = np.nonzero(lab[objs[j - 1]] == j)
                if len(ys) < 6:
                    continue
                sl = objs[j - 1]
                g.append((float(xs.mean() + sl[1].start), float(ys.mean() + sl[0].start), len(ys)))
        gems.append(g)
        if g:
            gem_cent[i] = [np.mean([p[0] for p in g]) - ax, np.mean([p[1] for p in g]) - ay]
        # monster-icon pixel mass
        m = icons(fr)[zone]
        if m.any():
            for R in RADII:
                sel = m & (zone_r <= R)
                c = int(sel.sum())
                cnt[R][i] = c
                if c:
                    cent[R][i] = [zone_x[sel].mean(), zone_y[sel].mean()]
    return n, gems, cent, cnt, gem_cent


# --- E1: gem-matched player step over an arbitrary baseline ---------------------

def gem_step(g0, g1, maxjump=22.0, min_pairs=3, spread_max=1.5):
    if len(g0) < min_pairs or len(g1) < min_pairs:
        return None
    ds = []
    for (x0, y0, _) in g0:
        best, bd = None, maxjump
        for (x1, y1, _) in g1:
            d = math.hypot(x1 - x0, y1 - y0)
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
    sp = float(np.hypot(*(keep.std(axis=0))))
    if sp > spread_max:
        return None
    mu = keep.mean(axis=0)
    return float(mu[0]), float(mu[1]), int(len(keep)), sp


# --- E2: masked terrain registration over the same baseline --------------------

def terrain_step(f0, f1, S=16):
    l0 = f0.astype(np.float32).mean(axis=2)
    l1 = f1.astype(np.float32).mean(axis=2)
    H, W = l0.shape
    ax, ay = ANCHOR
    yy, xx = np.mgrid[0:H, 0:W]
    dm = np.hypot(xx - ax, yy - ay) <= 78.0
    w0 = dm & (l0 < 140) & ~teal(f0)
    w1 = dm & (l1 < 140) & ~teal(f1)
    best, bx, by = np.inf, 0, 0
    for dy in range(-S, S + 1):
        for dx in range(-S, S + 1):
            y0a, y1a = max(0, dy), min(H, H + dy)
            x0a, x1a = max(0, dx), min(W, W + dx)
            wg = w0[y0a:y1a, x0a:x1a] & w1[y0a - dy:y1a - dy, x0a - dx:x1a - dx]
            s = int(wg.sum())
            if s < 1500:
                continue
            d = np.abs(l0[y0a:y1a, x0a:x1a] - l1[y0a - dy:y1a - dy, x0a - dx:x1a - dx])
            c = float(d[wg].mean())
            if c < best:
                best, bx, by = c, dx, dy
    if not np.isfinite(best) or abs(bx) == S or abs(by) == S:
        return None
    return float(bx), float(by), best


# --- circular statistics --------------------------------------------------------

def Rbar(delta):
    if len(delta) == 0:
        return float("nan"), float("nan")
    z = np.exp(1j * delta)
    m = z.mean()
    return float(abs(m)), float(math.degrees(np.angle(m)))


def block_boot(delta, n=N_BOOT, block=BLOCK, seed=11):
    rng = np.random.default_rng(seed)
    N = len(delta)
    if N < block * 3:
        return float("nan"), float("nan")
    nb = int(np.ceil(N / block))
    out = np.empty(n)
    for k in range(n):
        st = rng.integers(0, N, nb)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel() % N
        out[k] = abs(np.exp(1j * delta[idx[:N]]).mean())
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def shift_null(theta_p, theta_c, obs, lo=SHIFT_LO, hi=SHIFT_HI):
    """Circular time-shift null.  Preserves each series' own autocorrelation and
    destroys only their pairing.  Rayleigh is NOT used: at 10 Hz both series are
    heavily autocorrelated and Rayleigh is anti-conservative by an unknown factor."""
    vals = []
    N = len(theta_p)
    for lag in list(range(lo, hi + 1)) + [-l for l in range(lo, hi + 1)]:
        tc = np.roll(theta_c, lag)
        ok = np.isfinite(theta_p) & np.isfinite(tc)
        if ok.sum() < 100:
            continue
        r, _ = Rbar(theta_p[ok] - tc[ok])
        vals.append(r)
    vals = np.array(vals)
    p = float((vals >= obs).sum() + 1) / float(len(vals) + 1)
    return p, len(vals), float(np.percentile(vals, 95)), float(vals.mean())


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def run(mmpath, out):
    n, gems, cent, cnt, gem_cent = extract(mmpath)
    a = np.load(mmpath, mmap_mode="r")

    # --- player heading over the baseline, from E1 -----------------------------
    step = np.full((n, 2), np.nan)
    spread = np.full(n, np.nan)
    npair = np.zeros(n, int)
    for i in range(n - B_SAMPLES):
        s = gem_step(gems[i], gems[i + B_SAMPLES])
        if s is not None:
            step[i] = [-s[0], -s[1]]          # player step = -(fixture step)
            spread[i] = s[3]
            npair[i] = s[2]
    mag = np.hypot(step[:, 0], step[:, 1])
    moving = np.isfinite(mag) & (mag >= D_MIN)
    theta_p = np.where(moving, np.arctan2(step[:, 0], -step[:, 1]), np.nan)  # 0 = north

    # heading is centred on the baseline midpoint
    half = B_SAMPLES // 2
    theta_p_c = np.full(n, np.nan)
    theta_p_c[half:half + (n - B_SAMPLES)] = theta_p[:n - B_SAMPLES]
    mag_c = np.full(n, np.nan)
    mag_c[half:half + (n - B_SAMPLES)] = mag[:n - B_SAMPLES]

    # --- E2 cross-check on every 5th baseline pair -----------------------------
    agree = []
    for i in range(0, n - B_SAMPLES, 5):
        if not np.isfinite(step[i, 0]):
            continue
        t = terrain_step(np.asarray(a[i]), np.asarray(a[i + B_SAMPLES]))
        if t is None:
            continue
        agree.append([float(-step[i, 0] - t[0]) * -1, 0.0,
                      float(math.hypot(-step[i, 0] - t[0], -step[i, 1] - t[1]))])
    agree_d = np.array([r[2] for r in agree]) if agree else np.array([])

    res = {
        "input": mmpath, "n_samples": n, "hz": HZ, "t0": T0,
        "anchor_crop": list(ANCHOR),
        "anchor_fullframe": [round(ANCHOR[0] + CROP_X, 2), round(ANCHOR[1] + CROP_Y, 2)],
        "content_clearance_min_px": CONTENT_CLEARANCE_MIN,
        "baseline_s": B_SAMPLES / HZ, "d_min_px": D_MIN,
        "coverage": {
            "gem_lock_frac": round(float(np.isfinite(mag).mean()), 4),
            "gem_pairs_median": int(np.median(npair[npair > 0])) if (npair > 0).any() else 0,
            "gem_spread_median_px": round(float(np.nanmedian(spread)), 3),
            "moving_frac_of_locked": round(float(moving.sum() / max(1, np.isfinite(mag).sum())), 4),
            "n_moving": int(moving.sum()),
            "E2_n": len(agree),
            "E2_median_disagree_px": round(float(np.median(agree_d)), 3) if len(agree_d) else None,
            "E2_frac_within_3px": round(float((agree_d <= 3.0).mean()), 4) if len(agree_d) else None,
        },
        "speed_px_per_s": {
            "median_moving": round(float(np.nanmedian(mag[moving]) / (B_SAMPLES / HZ)), 2),
            "p90_moving": round(float(np.nanpercentile(mag[moving], 90) / (B_SAMPLES / HZ)), 2),
        },
        "radii": {},
        "gem_control": {},
    }

    for R in RADII:
        c = cent[R]
        theta_c = np.where(np.isfinite(c[:, 0]),
                           np.arctan2(c[:, 0], -c[:, 1]), np.nan)
        ok = np.isfinite(theta_p_c) & np.isfinite(theta_c)
        d = wrap(theta_p_c[ok] - theta_c[ok])
        r, mu = Rbar(d)
        lo, hi = block_boot(d)
        p, nsh, p95, mnull = shift_null(theta_p_c, theta_c, r)
        r2, mu2 = Rbar(2 * d)
        # Rayleigh, DESCRIPTIVE ONLY -- explicitly not in the decision rule
        N = len(d)
        z = N * r * r
        ray = math.exp(-z) * (1 + (2 * z - z * z) / (4 * N)) if N > 10 else float("nan")
        res["radii"][str(R)] = {
            "n": int(N), "n_frames_with_icon": int((cnt[R] > 0).sum()),
            "median_icon_px_in_R": float(np.median(cnt[R][cnt[R] > 0])) if (cnt[R] > 0).any() else 0,
            "Rbar": round(r, 4), "mu_deg": round(mu, 1),
            "boot95": [round(lo, 4), round(hi, 4)],
            "shift_null_p": round(p, 5), "n_shifts": nsh,
            "null_R_p95": round(p95, 4), "null_R_mean": round(mnull, 4),
            "p_adj_bonferroni9": round(min(1.0, p * len(RADII)), 5),
            "Rbar_axial": round(r2, 4), "mu_axial_deg": round(mu2, 1),
            "rayleigh_p_DESCRIPTIVE_ONLY": ray,
            "hemisphere_frac_toward": round(float((np.abs(d) < math.pi / 2).mean()), 4),
        }

    # --- NAMED POST-HOC CONTROL: world-static arena fixtures --------------------
    # If heading correlates with the TEAL-GEM centroid bearing as strongly as with
    # the monster-density bearing, the effect is arena geometry, not bodies.
    # Declared post-hoc.  It can only WEAKEN a positive claim, never manufacture one.
    theta_g = np.where(np.isfinite(gem_cent[:, 0]),
                       np.arctan2(gem_cent[:, 0], -gem_cent[:, 1]), np.nan)
    ok = np.isfinite(theta_p_c) & np.isfinite(theta_g)
    dg = wrap(theta_p_c[ok] - theta_g[ok])
    rg, mug = Rbar(dg)
    pg, nshg, _, _ = shift_null(theta_p_c, theta_g, rg)
    res["gem_control"] = {"n": int(len(dg)), "Rbar": round(rg, 4),
                          "mu_deg": round(mug, 1), "shift_null_p": round(pg, 5)}

    np.savez(out.replace(".json", "_series.npz"),
             theta_p=theta_p_c, mag=mag_c,
             **{f"theta_c_{R}": np.where(np.isfinite(cent[R][:, 0]),
                                         np.arctan2(cent[R][:, 0], -cent[R][:, 1]),
                                         np.nan) for R in RADII},
             cnt=np.stack([cnt[R] for R in RADII]))
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
