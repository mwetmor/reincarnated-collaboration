#!/usr/bin/env python3
"""u7_validate.py — coverage gates G-a and G-e for the U-7 minimap instrument.

G-a  E1 (matched teal-fixture centroids) vs E2 (masked ZNCC terrain registration),
     two independent estimators of the same player step on the same surface.
     ⚑ The first E2 pass reported a 16.18 px median disagreement.  It was NOT a
     disagreement: `u7_analyse.terrain_step` returns the shift that aligns the LATER
     frame ONTO the earlier one, i.e. the NEGATIVE of the content translation, and
     the comparison in `u7_analyse.run` differenced the two conventions.  The check
     ran, returned cleanly, and answered a different question from the one asked.
     Re-derived here with the sign resolved BY MEASUREMENT (both signs are scored and
     the better-agreeing one is reported alongside the worse) rather than by assertion.

G-e  external reproduction: the minimap-derived player step against the world-view
     screen pan (`s2-motion-20hz.json`) — a DIFFERENT surface, a DIFFERENT algorithm,
     produced by a different lap.  If the two are related by a fixed 2x2 linear map
     with R^2 >= 0.70, the minimap heading instrument is corroborated off-surface.
     The fitted map is the isometric ground->screen projection; recovering it here is
     a by-product and is REPORTED, not promoted.

  run <mm.npy> <s2-motion-20hz.json> <out.json>
"""
from __future__ import annotations

import json
import sys

import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import u7_analyse as U

HZ = 10.0
T0 = 682.10
B = U.B_SAMPLES


def gems_of(fr, dm):
    tm = U.teal(fr) & dm
    lab, k = ndi.label(tm)
    out = []
    for j in range(1, k + 1):
        ys, xs = np.nonzero(lab == j)
        if len(ys) < 6:
            continue
        out.append((float(xs.mean()), float(ys.mean()), len(ys)))
    return out


def zncc_step(f0, f1, dm, S=16):
    l0 = f0.astype(np.float32).mean(axis=2)
    l1 = f1.astype(np.float32).mean(axis=2)
    H, W = l0.shape
    w0 = dm & ~U.teal(f0) & (l0 < 150)
    w1 = dm & ~U.teal(f1) & (l1 < 150)
    best = (-2.0, 0, 0)
    second = -2.0
    for dy in range(-S, S + 1):
        for dx in range(-S, S + 1):
            y0a, y1a = max(0, dy), min(H, H + dy)
            x0a, x1a = max(0, dx), min(W, W + dx)
            wg = w0[y0a:y1a, x0a:x1a] & w1[y0a - dy:y1a - dy, x0a - dx:x1a - dx]
            if wg.sum() < 2500:
                continue
            A = l0[y0a:y1a, x0a:x1a][wg]
            Bm = l1[y0a - dy:y1a - dy, x0a - dx:x1a - dx][wg]
            A = A - A.mean(); Bm = Bm - Bm.mean()
            den = np.sqrt((A * A).sum() * (Bm * Bm).sum())
            if den <= 0:
                continue
            c = float((A * Bm).sum() / den)
            if c > best[0]:
                second = best[0]; best = (c, dx, dy)
            elif c > second:
                second = c
    if best[0] < -1 or abs(best[1]) == S or abs(best[2]) == S:
        return None
    return best[0], float(best[1]), float(best[2]), best[0] - second


def run(mmpath, motionpath, out):
    a = np.load(mmpath, mmap_mode="r")
    n, H, W, _ = a.shape
    ax, ay = U.ANCHOR
    yy, xx = np.mgrid[0:H, 0:W]
    dm = np.hypot(xx - ax, yy - ay) <= 78.0

    # ---- G-a -----------------------------------------------------------------
    same, opp, ncc, sharp = [], [], [], []
    e1, e2 = [], []
    for i in range(0, n - B, 5):
        f0 = np.asarray(a[i]); f1 = np.asarray(a[i + B])
        g = U.gem_step(gems_of(f0, dm), gems_of(f1, dm))
        z = zncc_step(f0, f1, dm)
        if g is None or z is None:
            continue
        gx, gy = g[0], g[1]
        same.append(np.hypot(gx - z[1], gy - z[2]))
        opp.append(np.hypot(gx + z[1], gy + z[2]))
        ncc.append(z[0]); sharp.append(z[3])
        e1.append([gx, gy]); e2.append([z[1], z[2]])
    same = np.array(same); opp = np.array(opp)
    d = opp if np.median(opp) < np.median(same) else same
    ga = {
        "n_jointly_locked": int(len(d)),
        "convention_resolved_by_measurement": "E2_NEGATED" if np.median(opp) < np.median(same) else "AS_IS",
        "median_disagree_AS_IS_px": round(float(np.median(same)), 3),
        "median_disagree_NEGATED_px": round(float(np.median(opp)), 3),
        "median_disagree_px": round(float(np.median(d)), 3),
        "frac_within_1_5px": round(float((d <= 1.5).mean()), 4),
        "frac_within_3px": round(float((d <= 3.0).mean()), 4),
        "zncc_peak_median": round(float(np.median(ncc)), 4),
        "zncc_peak_p05": round(float(np.percentile(ncc, 5)), 4),
        "PASS": bool(np.median(d) <= 1.5 and (d <= 3.0).mean() >= 0.80),
    }

    # ---- G-e -----------------------------------------------------------------
    M = json.load(open(motionpath))
    mrows = M["rows"]
    mt = np.array([r["t"] for r in mrows])
    mdx = np.array([r["dx"] for r in mrows])
    mdy = np.array([r["dy"] for r in mrows])
    cx = np.concatenate([[0.0], np.cumsum(mdx)])
    cy = np.concatenate([[0.0], np.cumsum(mdy)])
    tgrid = np.concatenate([mt, [mt[-1] + 0.05]])

    X, Y = [], []
    for i in range(0, n - B):
        f0 = np.asarray(a[i]); f1 = np.asarray(a[i + B])
        g = U.gem_step(gems_of(f0, dm), gems_of(f1, dm))
        if g is None:
            continue
        t0 = T0 + i / HZ
        t1 = t0 + B / HZ
        sx = np.interp(t1, tgrid, cx) - np.interp(t0, tgrid, cx)
        sy = np.interp(t1, tgrid, cy) - np.interp(t0, tgrid, cy)
        X.append([g[0], g[1]]); Y.append([sx, sy])
    X = np.array(X); Y = np.array(Y)
    A, *_ = np.linalg.lstsq(X, Y, rcond=None)
    pred = X @ A
    ss_res = float(((Y - pred) ** 2).sum())
    ss_tot = float(((Y - Y.mean(axis=0)) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot
    # per-axis
    r2x = 1 - float(((Y[:, 0] - pred[:, 0]) ** 2).sum()) / float(((Y[:, 0] - Y[:, 0].mean()) ** 2).sum())
    r2y = 1 - float(((Y[:, 1] - pred[:, 1]) ** 2).sum()) / float(((Y[:, 1] - Y[:, 1].mean()) ** 2).sum())
    ge = {
        "n": int(len(X)),
        "fitted_map_minimap_to_screen": [[round(float(A[0, 0]), 4), round(float(A[0, 1]), 4)],
                                         [round(float(A[1, 0]), 4), round(float(A[1, 1]), 4)]],
        "R2_joint": round(r2, 4), "R2_screen_x": round(r2x, 4), "R2_screen_y": round(r2y, 4),
        "PASS": bool(r2 >= 0.70),
    }

    res = {"G_a": ga, "G_e": ge}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
