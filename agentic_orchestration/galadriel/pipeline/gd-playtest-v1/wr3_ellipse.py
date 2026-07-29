#!/usr/bin/env python3
"""WR1-GAL-3: per-frame axis-aligned ellipse fit to the nova ring's OUTER edge.

Needed because the per-lance solve (wr3_lances.py) recovers only ONE long-lived
track: in this fixture most of the 16 projectiles die on mire terrain within
~10 frames, and their frost residue PERSISTS on the ground, so a wedge's
leading-edge statistic freezes at wherever that lance stopped. One live lance is
one equation in two unknowns (s and k) -- so k has to come from the ring's SHAPE
while it is still complete, which is the first ~8 frames after launch.

Method per frame:
  * cold-head mask -> furthest pixel per screen-angle sector (36 sectors)
  * fit ((x-cx)/a)^2 + ((y-cy)/b)^2 = 1 by Levenberg-Marquardt
  * iterate, dropping sectors that sit well INSIDE the fitted ellipse (a dead or
    occluded lance can only read short, so inside-outliers are dropped and
    outside-outliers are kept -- the same physical asymmetry as the v3 envelope)
Report a(f), b(f), k=b/a per frame; the slope of a(f) is s*14/60.
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


def cold(f, root, bright, box):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > bright) & ((B - R) > 60) & (B >= G - 12)
    ys, xs = np.nonzero(m)
    return xs.astype(float) + x0, ys.astype(float) + y0


def boundary(x, y, sx, sy, nsec=36, minpx=4):
    ang = np.arctan2(y - sy, x - sx)
    b = (((ang + np.pi) / (2 * np.pi) * nsec).astype(int)) % nsec
    pts = []
    r2 = (x - sx) ** 2 + (y - sy) ** 2
    for i in range(nsec):
        sel = b == i
        if sel.sum() < minpx:
            continue
        j = int(np.argmax(r2[sel]))
        pts.append((x[sel][j], y[sel][j]))
    return np.array(pts)


BOUNDS = ([985., 540., 15., 8.], [1075., 615., 950., 700.])


def fit_ellipse(pts, p0):
    """Bounded: unbounded LM ran the centre to -5e8 px and made the ellipse a
    straight line through a partial arc (rms 0.0, and meaningless). The caster
    cannot be off-screen, so the centre is boxed to the visible melee area."""
    def resid(p):
        cx, cy, a, bb = p
        return np.sqrt(((pts[:, 0] - cx) / a) ** 2 + ((pts[:, 1] - cy) / bb) ** 2) - 1.0
    p0 = np.clip(p0, np.array(BOUNDS[0]) + 1e-6, np.array(BOUNDS[1]) - 1e-6)
    r = optimize.least_squares(resid, p0, bounds=BOUNDS, method="trf", max_nfev=20000)
    return r.x, resid(r.x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, nargs="+",
                    default=list(range(309085, 309098)))
    ap.add_argument("--seedx", type=float, default=1028.0)
    ap.add_argument("--seedy", type=float, default=573.0)
    ap.add_argument("--bright", type=int, default=175)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # NB: the box must not clip the ring. An earlier run used (850,1250,450,800)
    # and the fitted semi-major axis SATURATED at the box half-width from f309092
    # on, which compressed the a(f) slope by ~40%. Sized here to hold 12 m.
    box = (300, 1750, 320, 930)   # excludes the blue mana globe at ~(1300,970)
    rows = []
    for f in args.frames:
        x, y = cold(f, args.root, args.bright, box)
        if len(x) < 60:
            continue
        pts = boundary(x, y, args.seedx, args.seedy)
        if len(pts) < 10:
            continue
        p = np.array([args.seedx, args.seedy, 60.0, 36.0])
        keep = np.ones(len(pts), bool)
        for _ in range(6):
            p, res = fit_ellipse(pts[keep], p)
            allres = np.sqrt(((pts[:, 0] - p[0]) / p[2]) ** 2 +
                             ((pts[:, 1] - p[1]) / p[3]) ** 2) - 1.0
            newkeep = allres > -0.18          # drop lances reading short only
            if newkeep.sum() < 8 or (newkeep == keep).all():
                break
            keep = newkeep
        allres = np.sqrt(((pts[:, 0] - p[0]) / p[2]) ** 2 +
                         ((pts[:, 1] - p[1]) / p[3]) ** 2) - 1.0
        rows.append(dict(f=f, n_sectors=int(len(pts)), n_used=int(keep.sum()),
                         cx=round(float(p[0]), 2), cy=round(float(p[1]), 2),
                         a=round(float(p[2]), 2), b=round(float(p[3]), 2),
                         k=round(float(p[3] / p[2]), 4),
                         rms=round(float(np.sqrt((allres[keep] ** 2).mean())), 4)))
        print(rows[-1], flush=True)

    fs = np.array([r["f"] for r in rows], float)
    aa = np.array([r["a"] for r in rows])
    c = np.polyfit(fs, aa, 1)
    s = c[0] * 60.0 / 14.0
    ks = [r["k"] for r in rows]
    res = dict(rows=rows, box=box, bright=args.bright,
               a_slope_px_per_frame=float(c[0]), a_intercept=float(c[1]),
               t0_frame=float(-c[1] / c[0]), s_px_per_m_x=float(s),
               k_median=float(np.median(ks)), k_iqr=[float(np.percentile(ks, 25)),
                                                     float(np.percentile(ks, 75))],
               s_px_per_m_y=float(s * np.median(ks)),
               cx_median=float(np.median([r["cx"] for r in rows])),
               cy_median=float(np.median([r["cy"] for r in rows])))
    json.dump(res, open(args.out, "w"), indent=1)
    print(json.dumps({q: v for q, v in res.items() if q != "rows"}, indent=1))


if __name__ == "__main__":
    main()
