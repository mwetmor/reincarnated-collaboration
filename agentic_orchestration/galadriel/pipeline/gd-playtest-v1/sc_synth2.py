#!/usr/bin/env python3
"""SHADOW-CAL control SC-C2: choose the base/top/tip estimators ON THE CONTROL.

SC-C1 showed the naive extremes are biased: the topmost pixel of a solid figure
is its far-top CORNER (which projects higher than the body's own top under a
53 deg pitch), and the bottom-most pixel is the NEAR edge of the footprint, not
its centre.  Both errors inflate the estimated height by ~23% and deflate the
length ratio by ~13%.

So the estimator variants are swept here against known truth, over a range of
body footprints, and the variant that wins is the one that runs on the footage.
The residual bias of the winner is carried as a stated correction with its own
spread -- not hidden, and not assumed to be zero.
"""
import argparse
import itertools
import json
import math

import numpy as np
from scipy import ndimage

import sc_cam
from sc_synth import box_points, rasterise, wrap


def synth(cam, base_xz, h, az_deg, ratio, w, d):
    P = box_points(base_xz, h, w=w, d=d)
    fig = rasterise(cam, P)
    a = math.radians(az_deg)
    S = P.copy()
    S[:, 0] += P[:, 1] * ratio * math.cos(a)
    S[:, 2] += P[:, 1] * ratio * math.sin(a)
    S[:, 1] = 0.0
    sha = rasterise(cam, S) & ~fig
    return fig, sha


def base_point(fig, mode):
    ys, xs = np.nonzero(fig)
    lo, hi = ys.min(), ys.max()
    if mode == "bottom_row":
        b = ys >= hi - 4
        return float(np.median(xs[b])), float(hi)
    if mode == "bottom_band":            # centroid of the lowest 12% of rows
        thr = hi - max(3, int(0.12 * (hi - lo)))
        b = ys >= thr
        return float(np.mean(xs[b])), float(np.mean(ys[b]))
    if mode == "bottom_q":               # x median of the lowest rows, y at 92nd pct
        b = ys >= hi - 4
        return float(np.median(xs[b])), float(np.percentile(ys, 92))
    raise ValueError(mode)


def top_y(fig, bx, mode):
    ys, xs = np.nonzero(fig)
    if mode == "global":
        return float(ys.min())
    if mode == "column":                 # topmost pixel near the base column
        sel = np.abs(xs - bx) <= 8
        return float(ys[sel].min()) if sel.any() else float(ys.min())
    if mode == "col_q":
        sel = np.abs(xs - bx) <= 8
        return float(np.percentile(ys[sel], 2)) if sel.any() else float(ys.min())
    raise ValueError(mode)


def tip(cam, sha, base_m, mode):
    sy, sx = np.nonzero(sha)
    g = cam.unproject_ground(np.stack([sx, sy], 1).astype(float))
    dd = g[:, [0, 2]] - np.asarray(base_m)
    rad = np.hypot(dd[:, 0], dd[:, 1])
    if mode == "q97":
        t = dd[rad >= np.quantile(rad, 0.97)].mean(0)
    elif mode == "q99":
        t = dd[rad >= np.quantile(rad, 0.99)].mean(0)
    elif mode == "max":
        t = dd[np.argmax(rad)]
    elif mode == "q90":
        t = dd[rad >= np.quantile(rad, 0.90)].mean(0)
    else:
        raise ValueError(mode)
    return t


def run(cam, bases, tops, tips, sizes, rows, ratios, azs, hs):
    """Each synthetic scene is rendered ONCE; every estimator variant is scored
    on the same scenes, so the comparison is paired."""
    variants = list(itertools.product(bases, tops, tips))
    err = {v: {"r": [], "a": [], "h": []} for v in variants}
    for target_row in rows:
        g = cam.unproject_ground([[960.0, float(target_row)]])
        bxz = (float(g[0]), float(g[2]))
        for (w, d), h, az, ratio in itertools.product(sizes, hs, azs, ratios):
            fig, sha = synth(cam, bxz, h, az, ratio, w, d)
            if fig.sum() < 200 or sha.sum() < 200:
                continue
            cache_b, cache_t = {}, {}
            for bm in bases:
                cache_b[bm] = base_point(fig, bm)
            for bm, tm, pm in variants:
                bx, by = cache_b[bm]
                key = (bm, tm)
                if key not in cache_t:
                    cache_t[key] = top_y(fig, bx, tm)
                ty = cache_t[key]
                base = cam.unproject_ground([[bx, by]])
                h_est = cam.solve_height((base[0], base[2]), ty)
                t = tip(cam, sha, (base[0], base[2]), pm)
                L = float(np.hypot(*t))
                err[(bm, tm, pm)]["r"].append(100 * (L / h_est - ratio) / ratio)
                err[(bm, tm, pm)]["h"].append(100 * (h_est - h) / h)
                err[(bm, tm, pm)]["a"].append(
                    wrap(math.degrees(math.atan2(t[1], t[0])) - az))
    out = {}
    for v, e in err.items():
        r, a, hh = np.array(e["r"]), np.array(e["a"]), np.array(e["h"])
        out[v] = {
            "n": len(r),
            "ratio_bias": float(r.mean()), "ratio_rms": float(np.sqrt((r**2).mean())),
            "ratio_sd": float(r.std()),
            "az_bias": float(a.mean()), "az_rms": float(np.sqrt((a**2).mean())),
            "h_bias": float(hh.mean()),
        }
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    sizes = [(0.45, 0.30), (0.60, 0.40), (0.90, 0.70), (1.30, 0.60)]
    rows = (300, 460, 595, 760, 870)
    ratios = (0.80, 1.14, 1.60, 2.50)
    azs = tuple(range(0, 360, 45))
    hs = (1.8, 2.4)
    res = run(cam, ["bottom_row", "bottom_band", "bottom_q"],
              ["global", "column", "col_q"], ["max", "q99", "q97", "q90"],
              sizes, rows, ratios, azs, hs)
    order = sorted(res.items(), key=lambda kv: kv[1]["ratio_rms"])
    print(f"{'base':<12}{'top':<9}{'tip':<6}{'n':>5}  "
          f"{'ratio bias%':>11}{'ratio rms%':>11}{'ratio sd%':>10}"
          f"{'az bias':>9}{'az rms':>8}{'h bias%':>9}")
    for k, v in order:
        print(f"{k[0]:<12}{k[1]:<9}{k[2]:<6}{v['n']:>5}  "
              f"{v['ratio_bias']:>11.2f}{v['ratio_rms']:>11.2f}{v['ratio_sd']:>10.2f}"
              f"{v['az_bias']:>9.2f}{v['az_rms']:>8.2f}{v['h_bias']:>9.2f}")
    if a.out:
        json.dump({f"{k[0]}|{k[1]}|{k[2]}": v for k, v in res.items()},
                  open(a.out, "w"))
