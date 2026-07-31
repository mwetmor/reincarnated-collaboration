#!/usr/bin/env python3
"""SHADOW-CAL control SC-C1: does the estimator recover a KNOWN azimuth and a
KNOWN shadow-length ratio?

A box of known height is placed on the ground at a known point and projected
through the GAL-CAM pinhole; its shadow is the same box sheared onto the ground
by a known azimuth and a known cot(elevation) and projected through the SAME
camera.  The masks are then handed to exactly the estimator that runs on the
footage.  Truth in, truth out -- or the estimator does not get to report on the
footage.

This also measures the estimator's own row-dependence: the same ground azimuth
subtends a different SCREEN angle at the top and the bottom of the frame, which
is the whole reason the measurement is done on the ground plane.
"""
import argparse
import json
import math

import numpy as np
from scipy import ndimage

import sc_cam


def box_points(base_xz, h, w=0.55, d=0.35, n=90):
    x = np.linspace(-w / 2, w / 2, 14)
    z = np.linspace(-d / 2, d / 2, 10)
    y = np.linspace(0.0, h, n)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    P = np.stack([X.ravel() + base_xz[0], Y.ravel(),
                  Z.ravel() + base_xz[1]], -1)
    return P


def rasterise(cam, P, shape=(1080, 1920)):
    uv = cam.project(P)
    m = np.zeros(shape, bool)
    u = np.round(uv[:, 0]).astype(int)
    v = np.round(uv[:, 1]).astype(int)
    ok = (u >= 0) & (u < shape[1]) & (v >= 0) & (v < shape[0])
    m[v[ok], u[ok]] = True
    return ndimage.binary_closing(m, np.ones((3, 3)))


def synth(cam, base_xz, h, az_deg, ratio):
    P = box_points(base_xz, h)
    fig = rasterise(cam, P)
    a = math.radians(az_deg)
    S = P.copy()
    S[:, 0] += P[:, 1] * ratio * math.cos(a)
    S[:, 2] += P[:, 1] * ratio * math.sin(a)
    S[:, 1] = 0.0
    sha = rasterise(cam, S) & ~fig
    return fig, sha


def estimate(cam, fig, sha):
    ys, xs = np.nonzero(fig)
    y_bot = int(ys.max())
    bx = float(np.median(xs[ys >= y_bot - 4]))
    by = float(y_bot)
    ty = float(ys.min())
    base = cam.unproject_ground([[bx, by]])
    h_est = cam.solve_height((base[0], base[2]), ty)
    sy, sx = np.nonzero(sha)
    g = cam.unproject_ground(np.stack([sx, sy], 1).astype(float))
    dd = g[:, [0, 2]] - np.array([base[0], base[2]])
    rad = np.hypot(dd[:, 0], dd[:, 1])
    tip = dd[rad >= np.quantile(rad, 0.97)].mean(0)
    cen = dd.mean(0)
    dc = dd - cen
    ev, evec = np.linalg.eigh(dc.T @ dc / len(dc))
    ax = evec[:, -1]
    if ax @ tip < 0:
        ax = -ax
    return {
        "h_est": float(h_est),
        "az_tip": float(math.degrees(math.atan2(tip[1], tip[0]))),
        "az_cen": float(math.degrees(math.atan2(cen[1], cen[0]))),
        "az_pca": float(math.degrees(math.atan2(ax[1], ax[0]))),
        "len": float(np.hypot(*tip)),
        "ratio": float(np.hypot(*tip) / h_est),
        "base_px": [bx, by],
    }


def wrap(d):
    return (d + 180) % 360 - 180


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    rows = []
    # ground points chosen to land the figure at several screen rows
    for target_row in (280, 450, 595, 760, 880):
        g = cam.unproject_ground([[960.0, float(target_row)]])
        base = (float(g[0]), float(g[2]))
        for h in (1.8, 2.4):
            for az in range(0, 360, 30):
                for ratio in (0.80, 1.14, 1.60, 2.50):
                    fig, sha = synth(cam, base, h, az, ratio)
                    if fig.sum() < 200 or sha.sum() < 200:
                        continue
                    e = estimate(cam, fig, sha)
                    rows.append({
                        "row": target_row, "h": h, "az": az, "ratio": ratio,
                        "h_est": e["h_est"], "ratio_est": e["ratio"],
                        "az_tip": e["az_tip"], "az_pca": e["az_pca"],
                        "d_az_tip": float(wrap(e["az_tip"] - az)),
                        "d_az_pca": float(wrap(e["az_pca"] - az)),
                        "d_h_pct": float(100 * (e["h_est"] - h) / h),
                        "d_ratio_pct": float(100 * (e["ratio"] - ratio) / ratio),
                    })
    R = rows
    da = np.array([r["d_az_tip"] for r in R])
    dp = np.array([r["d_az_pca"] for r in R])
    dh = np.array([r["d_h_pct"] for r in R])
    dr = np.array([r["d_ratio_pct"] for r in R])
    print(f"n = {len(R)} synthetic figure/shadow pairs")
    print(f"  azimuth error (tip): bias {da.mean():+.2f} deg  "
          f"rms {np.sqrt((da**2).mean()):.2f}  |max| {np.abs(da).max():.2f}")
    print(f"  azimuth error (pca): bias {dp.mean():+.2f} deg  "
          f"rms {np.sqrt((dp**2).mean()):.2f}  |max| {np.abs(dp).max():.2f}")
    print(f"  height error:        bias {dh.mean():+.2f} %     "
          f"rms {np.sqrt((dh**2).mean()):.2f}  |max| {np.abs(dh).max():.2f}")
    print(f"  RATIO error:         bias {dr.mean():+.2f} %     "
          f"rms {np.sqrt((dr**2).mean()):.2f}  |max| {np.abs(dr).max():.2f}")
    for ratio in (0.80, 1.14, 1.60, 2.50):
        s = np.array([r["d_ratio_pct"] for r in R if r["ratio"] == ratio])
        t = np.array([r["d_az_tip"] for r in R if r["ratio"] == ratio])
        print(f"    truth ratio {ratio:.2f}: ratio bias {s.mean():+6.2f}% "
              f"rms {np.sqrt((s**2).mean()):5.2f}%   az rms {np.sqrt((t**2).mean()):5.2f} deg")
    for row in (280, 450, 595, 760, 880):
        s = np.array([r["d_az_tip"] for r in R if r["row"] == row])
        q = np.array([r["d_ratio_pct"] for r in R if r["row"] == row])
        print(f"    screen row {row}: az rms {np.sqrt((s**2).mean()):5.2f} deg   "
              f"ratio rms {np.sqrt((q**2).mean()):5.2f}%")
    if a.out:
        json.dump(R, open(a.out, "w"))
        print("->", a.out)
