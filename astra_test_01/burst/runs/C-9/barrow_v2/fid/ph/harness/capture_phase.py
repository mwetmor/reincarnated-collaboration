#!/usr/bin/env python3
"""CAPTURE PHASE (R-C9-272; PT r268: v1's stills sit at sub-pixel phases 0.23-0.66 px, the pilot's at 0.00).
A still's screen pixel (x, y) shows plate pixel X = X_c + (x - W/2), Y = Y_c + (y - H/2) (+ the ground height's vertical
term), with X_c = (u_c - u0) * 100.6176 and Y_c = (v1 - v_c) * 80.3076 from the still's camera centre_ground_uv. The
fractional part of that offset is the capture PHASE. Measured, not assumed: on open-snow 128-px patches of the still
(class mask snow, or the pixel snow rule) the residual sub-pixel shift between the still and the painting at the integer
offset is read by iterative Lucas-Kanade on L* (sigma 0.7), so measured offset = integer offset + shift; the view's phase =
the median over patches of frac(measured offset) (x and y), with its spread.
  phase_of(still, painting, frame(u0, v1), centre_uv) -> {"phase_x", "phase_y", "n", "iqr"...}
  constructed check: the painting itself resampled at a known (px, py) must read back within +-0.05."""
import json
import math
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import pilot_harness as PHn

PXV = 80.3076


def _L(img):
    return ndimage.gaussian_filter(rgb_to_lab(img)[..., 0], 0.7)


def phase_of(still, painting, u0, v1, centre_uv, snow_mask=None, patch=128, max_patches=40, seed=272):
    S = load_rgb(still) if not isinstance(still, np.ndarray) else still
    Pn = load_rgb(painting) if not isinstance(painting, np.ndarray) else painting
    H, W = S.shape[:2]
    Xc = (centre_uv[0] - u0) * PPM_V1
    Yc = (v1 - centre_uv[1]) * PXV
    ox, oy = Xc - W / 2.0, Yc - H / 2.0
    LS, LP = _L(S), None
    if snow_mask is None:
        lab = rgb_to_lab(ndimage.gaussian_filter(S, (2, 2, 0)))
        snow_mask = (lab[..., 0] >= 78) & (lab[..., 2] >= -6)
    cov = ndimage.uniform_filter(snow_mask.astype(np.float32), patch) >= 0.95
    ys, xs = np.where(cov[patch // 2:H - patch // 2:32, patch // 2:W - patch // 2:32])
    ys, xs = ys * 32 + patch // 2, xs * 32 + patch // 2
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(ys))[:max_patches]
    rows = []
    for i in idx:
        y0, x0 = int(ys[i]) - patch // 2, int(xs[i]) - patch // 2
        X0, Y0 = int(math.floor(x0 + ox)), int(math.floor(y0 + oy))
        if X0 < 8 or Y0 < 8 or X0 + patch + 8 > Pn.shape[1] or Y0 + patch + 8 > Pn.shape[0]:
            continue
        a = LS[y0:y0 + patch, x0:x0 + patch]
        if LP is None:
            LP = _L(Pn)
        b = LP[Y0 - 8:Y0 + patch + 8, X0 - 8:X0 + patch + 8]
        # find s with painting(X0 + s + .) ~ still(.)  (LK on the painting window, inner region)
        s = np.zeros(2)
        yy, xx = np.mgrid[0:patch, 0:patch].astype(float)
        gy, gx = np.gradient(a)
        M = np.array([[np.sum(gy * gy), np.sum(gy * gx)], [np.sum(gx * gy), np.sum(gx * gx)]])
        if np.linalg.det(M) < 1e-6:
            continue
        for _ in range(15):
            Bw = ndimage.map_coordinates(b, [yy + 8 + s[0], xx + 8 + s[1]], order=3, mode="nearest")
            e = Bw - a
            ds = -np.linalg.solve(M, np.array([np.sum(gy * e), np.sum(gx * e)]))
            s += ds
            if np.hypot(*ds) < 1e-3:
                break
        if np.hypot(*s) > 1.5:
            continue                      # not this place (3D content / height): skip
        resid = float(np.abs(ndimage.map_coordinates(b, [yy + 8 + s[0], xx + 8 + s[1]], order=3, mode="nearest") - a).mean())
        rows.append({"x": x0, "y": y0, "off_x": X0 - x0 + s[1], "off_y": Y0 - y0 + s[0], "resid_L": round(resid, 3)})
    if not rows:
        return {"n": 0}
    fx = np.array([r["off_x"] % 1.0 for r in rows])
    fy = np.array([r["off_y"] % 1.0 for r in rows])
    # circular median (phases wrap at 1)
    def cmed(f):
        ang = np.angle(np.mean(np.exp(2j * np.pi * f))) / (2 * np.pi)
        ang = ang % 1.0
        d = ((f - ang + 0.5) % 1.0) - 0.5
        return (ang + float(np.median(d))) % 1.0, float(np.percentile(np.abs(d), 75))
    px, sx = cmed(fx)
    py, sy = cmed(fy)
    return {"n": len(rows), "phase_x": round(px, 3), "phase_y": round(py, 3), "spread_x_p75": round(sx, 3), "spread_y_p75": round(sy, 3),
            "expected_from_camera": [round(ox % 1.0, 3), round(oy % 1.0, 3)], "resid_L_median": round(float(np.median([r["resid_L"] for r in rows])), 3)}


def constructed_check(painting, u0, v1, centre_uv, W=1920, H=1080, phases=((0.0, 0.0), (0.25, 0.5), (0.44, 0.60), (0.7, 0.1))):
    """the PAINTING resampled (bilinear, as a texture lookup at the screen grid) at known sub-pixel offsets = a still at a
    known phase; the estimator must read each back within +-0.05 px"""
    Pn = load_rgb(painting)
    Xc = (centre_uv[0] - u0) * PPM_V1
    Yc = (v1 - centre_uv[1]) * PXV
    out = []
    for px, py in phases:
        ox, oy = math.floor(Xc - W / 2.0) + px, math.floor(Yc - H / 2.0) + py
        yy, xx = np.mgrid[0:H, 0:W].astype(float)
        st = np.stack([ndimage.map_coordinates(Pn[..., c], [yy + oy, xx + ox], order=1, mode="nearest") for c in range(3)], -1)
        cu = (u0 + (ox + W / 2.0) / PPM_V1, v1 - (oy + H / 2.0) / PXV)      # the centre that implies this offset exactly
        r = phase_of(st, Pn, u0, v1, cu)
        out.append({"set": [px, py], "read": [r.get("phase_x"), r.get("phase_y")], "n": r.get("n"),
                    "ok": r.get("n", 0) > 0 and min(abs(r["phase_x"] - px), 1 - abs(r["phase_x"] - px)) <= 0.05
                    and min(abs(r["phase_y"] - py), 1 - abs(r["phase_y"] - py)) <= 0.05})
    return out
