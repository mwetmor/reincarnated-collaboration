#!/usr/bin/env python3
"""WR1-GAL-3 fit v4 — CONCENTRICITY fit of the nova ring (the one used for record).

IDENTIFYING CONDITION
---------------------
For the true (cx, cy, k), every LIVE projectile in a given frame sits at the same
elliptic radius
        rho = sqrt((x-cx)^2 + ((y-cy)/k)^2) = s * R(f)
regardless of its azimuth. A wrong k tilts that: the sectors near screen-X and the
sectors near screen-Y disagree. So the estimator is:

    minimise, per frame, the DISPERSION of the sector leading edges (over the
    sectors that still have a live lance), and require rho(f) to be linear in f.

Live-lance selection: lances die on terrain/props, and a dead lance's sector edge
freezes. Dead sectors read LOW, never high, so the live set is taken as the top-N
sector maxima per frame; dispersion is measured on that set only. N is a declared
parameter (default 8 of 24) and the result is reported across N = 6, 8, 10 so the
sensitivity to that choice is visible rather than hidden.

Outputs: cx, cy (caster ground point, screen px), k (= sin pitch),
s = px per metre along screen X, s*k = px per metre along screen Y, and t0.
"""
import argparse
import itertools
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))
NBIN = 24


def head_pixels(f, root, bright, box):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > bright) & ((B - R) > 60) & (B >= G - 12)
    ys, xs = np.nonzero(m)
    return xs.astype(np.float64) + x0, ys.astype(np.float64) + y0


def sector_max(x, y, cx, cy, k):
    dx = x - cx
    dy = (y - cy) / k
    rho = np.sqrt(dx * dx + dy * dy)
    phi = np.arctan2(dy, dx)
    b = (((phi + np.pi) / (2 * np.pi) * NBIN).astype(np.int64)) % NBIN
    cnt = np.bincount(b, minlength=NBIN)
    out = np.zeros(NBIN)
    np.maximum.at(out, b, rho)
    out[cnt < 10] = np.nan
    return out


def score(P, frames, cx, cy, k, topn):
    disp, meds = [], []
    for f in frames:
        e = sector_max(*P[f], cx, cy, k)
        e = e[~np.isnan(e)]
        if len(e) < topn:
            return None
        top = np.sort(e)[-topn:]
        m = top.mean()
        if m <= 1:
            return None
        disp.append(top.std() / m)
        meds.append(m)
    meds = np.array(meds)
    t = np.array(frames, float)
    c = np.polyfit(t, meds, 1)
    resid = meds - np.polyval(c, t)
    lin = np.sqrt((resid ** 2).mean()) / meds.mean()
    return float(np.mean(disp) + 2.0 * lin), float(c[0]), float(c[1]), float(np.mean(disp)), float(lin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309089)
    ap.add_argument("--f1", type=int, default=309110)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    box = (450, 1400, 300, 900)
    frames = list(range(args.f0, args.f1 + 1))
    P = {f: head_pixels(f, args.root, args.bright, box) for f in frames}

    results = {}
    for topn in (6, 8, 10):
        best = None
        for cx in np.arange(1006, 1051, 1.5):
            for cy in np.arange(552, 597, 1.5):
                for k in np.arange(0.38, 0.86, 0.01):
                    r = score(P, frames, cx, cy, k, topn)
                    if r is None:
                        continue
                    if best is None or r[0] < best[0][0]:
                        best = (r, cx, cy, k)
        (sc, slope, icpt, disp, lin), cx, cy, k = best
        s = slope * 60.0 / 14.0
        results[str(topn)] = dict(score=sc, dispersion=disp, linearity=lin,
                                  cx=float(cx), cy=float(cy), k=float(k),
                                  A_px_per_frame=slope, t0_frame=-icpt / slope,
                                  s_px_per_m_x=s, s_px_per_m_y=s * k)
        print(topn, json.dumps(results[str(topn)]))
    json.dump(dict(frames=frames, box=box, bright=args.bright, nbin=NBIN,
                   results=results), open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
