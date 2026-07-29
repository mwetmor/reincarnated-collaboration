#!/usr/bin/env python3
"""WR1-GAL-3: fit the nova ring as a self-calibrating scale bar.

MODEL
-----
Ground-plane circle of world radius R(t), projected by a fixed-pitch camera to a
screen ellipse with screen-aligned axes:
    a(t) = s * R(t)          (semi-axis along screen X, px)
    b(t) = k * a(t)          (k = sin(pitch), constant)
    R(t) = r0 + 14*(t - t_v)/60      (14 m/s, 60 fps)
Free parameters: cx, cy, k, and the linear law a(t) = A*(t - t0) fitted directly.
Then  s = A * 60/14  px per metre along X, and s*k px per metre along Y.

FIT PROCEDURE (deliberately dumb, so it is checkable)
-----------------------------------------------------
For a candidate (cx, cy, k) compute per-frame  a_hat(t) = max over cold-head
pixels of  rho = sqrt(((x-cx))^2 + ((y-cy)/k)^2).  The leading edge of the mask
IS the projectile head locus; trails lag, so max is the head and cannot be
inflated by the trail.  Score = R^2 of a straight line through a_hat(t).
Grid-search (cx, cy, k); report the best, and dump the residuals so a bad fit is
visible rather than silent.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


def head_pixels(f, root, bright=200, box=(300, 1500, 200, 1000)):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > bright) & ((B - R) > 60) & (B >= G - 12)
    ys, xs = np.nonzero(m)
    return xs.astype(np.float64) + x0, ys.astype(np.float64) + y0


def a_hat(px, py, cx, cy, k, q=100.0):
    rho = np.sqrt((px - cx) ** 2 + ((py - cy) / k) ** 2)
    if len(rho) == 0:
        return np.nan
    return float(np.percentile(rho, q))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309085)
    ap.add_argument("--f1", type=int, default=309110)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--q", type=float, default=99.5)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    frames = list(range(args.f0, args.f1 + 1))
    px = {}
    for f in frames:
        px[f] = head_pixels(f, args.root)
        print("loaded", f, len(px[f][0]), flush=True)

    best = None
    for cx in np.arange(1000, 1071, 2.0):
        for cy in np.arange(540, 611, 2.0):
            for k in np.arange(0.40, 0.72, 0.02):
                ah = np.array([a_hat(px[f][0], px[f][1], cx, cy, k, args.q) for f in frames])
                t = np.array(frames, dtype=float)
                A = np.polyfit(t, ah, 1)
                pred = np.polyval(A, t)
                ss = 1 - ((ah - pred) ** 2).sum() / ((ah - ah.mean()) ** 2).sum()
                if best is None or ss > best[0]:
                    best = (ss, cx, cy, k, A[0], A[1], ah.tolist())
    ss, cx, cy, k, slope, icpt, ah = best
    t0 = -icpt / slope
    s = slope * 60.0 / 14.0
    res = dict(f0=args.f0, f1=args.f1, q=args.q, r2=ss, cx=cx, cy=cy, k=k,
               slope_px_per_frame=slope, t0_frame=t0,
               s_px_per_m_x=s, s_px_per_m_y=s * k,
               a_hat={str(f): v for f, v in zip(frames, ah)})
    json.dump(res, open(args.out, "w"), indent=1)
    print(json.dumps({q: v for q, v in res.items() if q != "a_hat"}, indent=1))


if __name__ == "__main__":
    main()
