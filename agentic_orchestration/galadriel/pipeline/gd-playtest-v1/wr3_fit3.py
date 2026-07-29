#!/usr/bin/env python3
"""WR1-GAL-3 fit v3 — sector-envelope fit of the nova ring.

WHY v3
------
v2 maximised R^2 of a single leading-edge statistic and the optimum ran to the
grid boundary: with only ONE number per frame, (cx, cy, k) is under-determined --
many far-away centres make "distance to the furthest pixel" look linear in time.

v3 uses the whole ring at once. For a trial (cx, cy, k) every head pixel gets
    rho = sqrt((x-cx)^2 + ((y-cy)/k)^2)      [semi-major-axis units]
    phi = atan2((y-cy)/k, x-cx)              [parametric angle]
Pixels are binned by phi; each bin's MAX rho is that sector's leading edge.
Physics gives the asymmetry that identifies the model:
    a projectile CANNOT be outside the ring   -> rho > a(f) is a hard error
    a projectile CAN be missing or stopped    -> rho < a(f) is cheap (occlusion)
So the loss is one-sided (w_hi >> w_lo): it fits the UPPER ENVELOPE across all
sectors and all frames simultaneously. A wrong k makes the x-sectors and the
y-sectors disagree about a(f), which the envelope cannot absorb -- that is what
pins the pitch.

a(f) = A*(f - t0), and s = A * 60/14 px per metre along screen X.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))
NBIN = 24
W_HI, W_LO = 1.0, 0.06


def head_pixels(f, root, bright, box):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > bright) & ((B - R) > 60) & (B >= G - 12)
    ys, xs = np.nonzero(m)
    xs = xs.astype(np.float64) + x0
    ys = ys.astype(np.float64) + y0
    if len(xs) > 4000:   # subsample: the envelope statistic is a max, so density is irrelevant
        idx = np.linspace(0, len(xs) - 1, 4000).astype(int)
        xs, ys = xs[idx], ys[idx]
    return xs, ys


def sector_edges(x, y, cx, cy, k):
    dx = x - cx
    dy = (y - cy) / k
    rho = np.sqrt(dx * dx + dy * dy)
    phi = np.arctan2(dy, dx)
    b = (((phi + np.pi) / (2 * np.pi) * NBIN).astype(np.int64)) % NBIN
    cnt = np.bincount(b, minlength=NBIN)
    out = np.zeros(NBIN)
    np.maximum.at(out, b, rho)
    out[cnt < 8] = np.nan
    return out, cnt


MIN_BINS = 8


def loss(p, P, frames):
    cx, cy, k, A, t0 = p
    if not (0.15 < k < 0.95) or A <= 0:
        return 1e12
    tot = 0.0
    for f in frames:
        x, y = P[f]
        e, c = sector_edges(x, y, cx, cy, k)
        a = A * (f - t0)
        if a <= 1:
            return 1e12
        m = ~np.isnan(e)
        nb = int(m.sum())
        if nb < MIN_BINS:
            # a centre that collapses the ring into a couple of sectors is not a
            # centre; refuse it rather than let it win by having nothing to fit
            return 1e12
        d = (e[m] - a) / a
        tot += (W_HI * np.clip(d, 0, None) ** 2 + W_LO * np.clip(-d, 0, None) ** 2).sum() / nb
    return tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309089)
    ap.add_argument("--f1", type=int, default=309112)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    box = (500, 1400, 300, 900)
    frames = list(range(args.f0, args.f1 + 1))
    P = {f: head_pixels(f, args.root, args.bright, box) for f in frames}

    bounds = [(985., 1090.), (525., 635.), (0.30, 0.90), (6., 26.),
              (309068., 309088.5)]
    de = optimize.differential_evolution(loss, bounds, args=(P, frames), seed=11,
                                         popsize=24, maxiter=350, tol=1e-8,
                                         mutation=(0.4, 1.0), recombination=0.8,
                                         polish=False, init="sobol")
    best = optimize.minimize(loss, de.x, args=(P, frames), method="Nelder-Mead",
                             options=dict(maxiter=4000, xatol=1e-4, fatol=1e-10))
    if de.fun < best.fun:
        best = de
    cx, cy, k, A, t0 = best.x
    s = A * 60.0 / 14.0
    # per-frame diagnostics at the solution
    diag = []
    for f in frames:
        e, c = sector_edges(P[f][0], P[f][1], cx, cy, k)
        a = A * (f - t0)
        diag.append(dict(f=f, a_model=round(a, 2),
                         edges=[None if np.isnan(v) else round(v, 1) for v in e],
                         n_bins=int((~np.isnan(e)).sum())))
    res = dict(loss=float(best.fun), cx=float(cx), cy=float(cy), k=float(k),
               A_px_per_frame=float(A), t0_frame=float(t0),
               s_px_per_m_x=float(s), s_px_per_m_y=float(s * k),
               r0_at_launch_m=float(A * (args.f0 - t0) / s) if s else None,
               frames=frames, box=box, bright=args.bright, nbin=NBIN,
               w=[W_HI, W_LO], diag=diag)
    json.dump(res, open(args.out, "w"), indent=1)
    print(json.dumps({q: v for q, v in res.items() if q not in ("diag", "frames")}, indent=1))
    for d in diag:
        print(d["f"], d["a_model"], d["n_bins"], d["edges"])


if __name__ == "__main__":
    main()
