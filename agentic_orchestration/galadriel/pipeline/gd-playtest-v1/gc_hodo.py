#!/usr/bin/env python3
"""GAL-CAM: pitch from the nova HODOGRAPH (per-lance screen velocity vectors).

WHY VELOCITIES AND NOT POSITIONS
--------------------------------
gc_fit.py fitted head POSITIONS and failed (rms 35 px): the cold blobs sit all
along the projectile TRAILS, not at the heads, so a position fit is fitting a
smear. See evidence/look-309104.jpg -- the picture was looked at before the
number was believed, and the picture said the number was wrong.

Velocities are immune to that failure and to two others:

  * the ring CENTRE cancels (a velocity does not know where it started)
  * the launch frame t0 cancels (ditto)
  * the head-vs-trail offset cancels IF it is constant, because a constant
    radial offset differentiates to zero

Geometry. Ground ray at azimuth psi, speed V=14 m/s. Under an orthographic
ground projection with scale s px/m and axis ratio k = sin(pitch):

    (u, w) = (V s cos psi,  -V s k sin psi)        u = px/frame right, w = down

so the 16 velocity vectors lie on an ORIGIN-CENTRED, AXIS-ALIGNED ellipse with
semi-axes A = V s /fps and B = k A. Therefore

    k = B / A        (pure ratio -- no scale needed, no centre, no t0)
    s = A * fps / V  (scale, from the known 14 m/s)

Two independent products from one fit, and k is the one the pitch question wants.

TIP EXTRACTION
--------------
Per frame, per azimuth bin about an approximate centre, take the cold pixel of
MAXIMUM RADIUS. Trails lie inside the tip by construction, so the radial maximum
IS the tip: a trail cannot inflate it. A bin is accepted as carrying a live lance
only if its radius grows LINEARLY in frame number (R^2 gate) at a plausible rate.

PERSPECTIVE PROBE
-----------------
Under a pinhole camera the screen speed of a lance is not constant: a lance
running away from the camera decelerates, one running toward it accelerates. So
the quadratic term of r(f), signed and plotted against azimuth, is a direct test
of orthographic-vs-pinhole that needs no separate model fit.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))
FPS = 60.0
VPROJ = 14.0


def cold_mask(a, bmin=150, brmin=60, gtol=12):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (B > bmin) & ((B - R) > brmin) & (B >= G - gtol)


def envelope(f, cx, cy, nbin, rmin, rmax, bright, ytop, ybot):
    a = np.asarray(Image.open(os.path.join(FRAMES, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    m = cold_mask(a) & (a[:, :, 2] > bright)
    m[:ytop] = False
    m[ybot:] = False
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    dx = xs - cx
    dy = ys - cy
    r = np.hypot(dx, dy)
    keep = (r >= rmin) & (r <= rmax)
    if keep.sum() == 0:
        return None
    dx, dy, r, xs, ys = dx[keep], dy[keep], r[keep], xs[keep], ys[keep]
    th = np.arctan2(dy, dx) % (2 * math.pi)
    b = np.floor(th / (2 * math.pi) * nbin).astype(int) % nbin
    out = np.full((nbin, 3), np.nan)
    order = np.argsort(r)
    b_s, r_s, x_s, y_s = b[order], r[order], xs[order], ys[order]
    # last write per bin wins -> maximum radius
    out[b_s, 0] = r_s
    out[b_s, 1] = x_s
    out[b_s, 2] = y_s
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309090)
    ap.add_argument("--f1", type=int, default=309140)
    ap.add_argument("--cx", type=float, default=1024.7)
    ap.add_argument("--cy", type=float, default=568.5)
    ap.add_argument("--nbin", type=int, default=180)
    ap.add_argument("--rmin", type=float, default=30)
    ap.add_argument("--rmax", type=float, default=900)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--ytop", type=int, default=30)
    ap.add_argument("--ybot", type=int, default=940)
    ap.add_argument("--minframes", type=int, default=10)
    ap.add_argument("--r2", type=float, default=0.985)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    frames = [f for f in range(args.f0, args.f1 + 1)
              if os.path.exists(os.path.join(FRAMES, f"f{f:06d}.png"))]
    env = {}
    for f in frames:
        e = envelope(f, args.cx, args.cy, args.nbin, args.rmin, args.rmax,
                     args.bright, args.ytop, args.ybot)
        if e is not None:
            env[f] = e
        print("env", f, flush=True)

    lanes = []
    for b in range(args.nbin):
        fs, rs, xs, ys = [], [], [], []
        for f in frames:
            e = env.get(f)
            if e is None or np.isnan(e[b, 0]):
                continue
            fs.append(f); rs.append(e[b, 0]); xs.append(e[b, 1]); ys.append(e[b, 2])
        if len(fs) < args.minframes:
            continue
        fs = np.array(fs, float); rs = np.array(rs); xs = np.array(xs); ys = np.array(ys)
        # trim to the longest run of monotone-ish growth
        A = np.vstack([fs - fs.mean(), np.ones_like(fs)]).T
        co, *_ = np.linalg.lstsq(A, rs, rcond=None)
        pred = A @ co
        ss_res = float(((rs - pred) ** 2).sum())
        ss_tot = float(((rs - rs.mean()) ** 2).sum())
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        slope = float(co[0])
        if r2 < args.r2 or not (2.0 <= slope <= 22.0):
            continue
        cu, *_ = np.linalg.lstsq(A, xs, rcond=None)
        cw, *_ = np.linalg.lstsq(A, ys, rcond=None)
        # quadratic term of r(f) -> perspective probe
        A2 = np.vstack([(fs - fs.mean()) ** 2, fs - fs.mean(), np.ones_like(fs)]).T
        cq, *_ = np.linalg.lstsq(A2, rs, rcond=None)
        lanes.append(dict(bin=b, th_deg=(b + 0.5) * 360.0 / args.nbin,
                          n=len(fs), r2=r2, slope=slope,
                          u=float(cu[0]), w=float(cw[0]),
                          quad=float(cq[0]), fmid=float(fs.mean()),
                          rmid=float(rs.mean()),
                          x0=float(cu[1]), y0=float(cw[1])))

    # cluster adjacent bins into lances
    lanes.sort(key=lambda d: d["bin"])
    groups, cur = [], []
    for L in lanes:
        if cur and (L["bin"] - cur[-1]["bin"]) <= 2:
            cur.append(L)
        else:
            if cur:
                groups.append(cur)
            cur = [L]
    if cur:
        groups.append(cur)
    if len(groups) > 1 and (groups[0][0]["bin"] + args.nbin - groups[-1][-1]["bin"]) <= 2:
        groups[0] = groups[-1] + groups[0]
        groups.pop()

    L = []
    for g in groups:
        wts = np.array([x["n"] for x in g], float)
        u = float(np.average([x["u"] for x in g], weights=wts))
        w = float(np.average([x["w"] for x in g], weights=wts))
        L.append(dict(nbins=len(g), n=int(wts.sum()),
                      th_deg=float(np.average([x["th_deg"] for x in g], weights=wts)),
                      u=u, w=w, speed=float(math.hypot(u, w)),
                      quad=float(np.average([x["quad"] for x in g], weights=wts)),
                      r2=float(np.average([x["r2"] for x in g], weights=wts))))
    L.sort(key=lambda d: -d["n"])
    print(f"\n{len(L)} lance groups from {len(lanes)} bins")
    for x in L:
        print(f"  th={x['th_deg']:7.2f} bins={x['nbins']:2d} n={x['n']:4d} "
              f"u={x['u']:+7.3f} w={x['w']:+7.3f} |v|={x['speed']:6.3f} "
              f"quad={x['quad']:+.5f} r2={x['r2']:.4f}")

    # hodograph ellipse: origin-centred, axis-aligned
    def solve(sel):
        U = np.array([x["u"] for x in sel]); W = np.array([x["w"] for x in sel])
        # (u/A)^2 + (w/B)^2 = 1  ->  p*u^2 + q*w^2 = 1
        M = np.vstack([U ** 2, W ** 2]).T
        sol, *_ = np.linalg.lstsq(M, np.ones(len(sel)), rcond=None)
        if sol[0] <= 0 or sol[1] <= 0:
            return None
        return 1 / math.sqrt(sol[0]), 1 / math.sqrt(sol[1])

    sel = [x for x in L if x["nbins"] >= 2 and x["n"] >= 20]
    res = None
    if len(sel) >= 3:
        AB = solve(sel)
        if AB:
            A, B = AB
            k = B / A
            s = A * FPS / VPROJ
            res = dict(A=A, B=B, k=k, pitch_deg=math.degrees(math.asin(min(1, k))),
                       s_px_per_m=s, n_lances=len(sel))
            print(f"\nHODOGRAPH  A={A:.4f} B={B:.4f}  k={k:.4f}  "
                  f"pitch={math.degrees(math.asin(min(1,k))):.2f} deg  s={s:.2f} px/m")
            # jackknife
            ks, ss = [], []
            for i in range(len(sel)):
                sub = sel[:i] + sel[i + 1:]
                r = solve(sub)
                if r:
                    ks.append(r[1] / r[0]); ss.append(r[0] * FPS / VPROJ)
            if ks:
                print(f"  jackknife k  min={min(ks):.4f} max={max(ks):.4f} "
                      f"sd={np.std(ks, ddof=1):.4f}")
                print(f"  jackknife s  min={min(ss):.2f} max={max(ss):.2f} "
                      f"sd={np.std(ss, ddof=1):.2f}")
                res["k_jack"] = [float(min(ks)), float(max(ks)), float(np.std(ks, ddof=1))]
                res["s_jack"] = [float(min(ss)), float(max(ss)), float(np.std(ss, ddof=1))]

    json.dump(dict(args=vars(args), lanes=lanes, groups=L, hodograph=res),
              open(args.out, "w"), indent=1)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
