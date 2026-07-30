#!/usr/bin/env python3
"""GAL-CAM: solve the camera SHAPE from the banded pan record.

THE MODEL, AND WHY IT IS THE RIGHT ONE
--------------------------------------
Pinhole camera, no roll, looking down at a ground plane. Put y' = (screen row -
principal row). Standard projection gives, for the ground->screen scales:

    g_x(y') = s0 * G          px per metre of ground-X (screen-horizontal)
    g_y(y') = s0 * k * G^2    px per metre of ground-Z (screen-away)
    G(y')   = 1 + lambda*y'   k = sin(pitch)

Two consequences that make this falsifiable rather than merely fitted:

  (F1) g_x is LINEAR in screen row -- so it hits zero at a finite row, the
       HORIZON, whether or not the horizon is on screen.
  (F2) g_y falls off as the SQUARE of g_x. So between any two screen bands the
       measured vertical pan ratio must equal the SQUARE of the horizontal pan
       ratio. Orthographic predicts both ratios == 1.

Both are tested here and reported pass or fail.

WHAT THE PAN CLOUD GIVES
------------------------
Camera is player-locked and player ground speed is isotropic, so per band the
pan-vector covariance is diag(g_x^2, g_y^2)*sigma^2. Therefore

    sd(dy)/sd(dx) = g_y/g_x = k*G          -- no envelope percentiles needed,
                                              closed form, uses every sample

and the OFF-DIAGONAL term tests for camera roll (must be ~0).

Isotropic pixel NOISE inflates both sd's equally and therefore biases the ratio
TOWARD 1. It is estimated from the second difference of the pan time series
(the true pan is smooth; the second difference is nearly pure noise) and
SUBTRACTED in quadrature. The uncorrected number is reported alongside.

WHAT IS AND IS NOT DETERMINED
-----------------------------
Measurable without further assumption: the horizon row y_h, the product
k*lambda, and hence the FULL ground-metre-per-pixel field up to one absolute
scale. That is everything the visible-ground box needs.

NOT separately determined: k and lambda individually. They separate only if the
principal row is pinned. Assuming the principal row is the viewport centre
(row 540 of 1080) closes it; the assumption is stated, its sensitivity is
reported, and the decision-surface numbers do NOT depend on it.
"""
import argparse
import json
import math

import numpy as np


def robust_sd(x):
    return 1.4826 * float(np.median(np.abs(x - np.median(x))))


def noise_sd(series):
    """sd of measurement noise from the 2nd difference of a smooth series."""
    d2 = series[2:] - 2 * series[1:-1] + series[:-2]
    return robust_sd(d2) / math.sqrt(6.0)


def ratio_through_origin(a, b, vmin):
    """robust slope of a on b through the origin, using both components."""
    m = np.hypot(*b.T) > vmin
    if m.sum() < 40:
        return None, 0
    num = (a[m] * b[m]).sum(axis=1)
    den = (b[m] * b[m]).sum(axis=1)
    return float(np.median(num / den)), int(m.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pkmin", type=float, default=0.03)
    ap.add_argument("--vmin", type=float, default=2.0)
    ap.add_argument("--py0", type=float, default=540.0)
    args = ap.parse_args()

    d = json.load(open(args.pan))
    bands, bh = d["bands"], d["bh"]
    rows = d["rows"]
    yc = {b: b + bh / 2.0 for b in bands}
    V = {b: np.array([r[f"b{b}"][:2] for r in rows]) for b in bands}
    PK = {b: np.array([r[f"b{b}"][2] for r in rows]) for b in bands}
    SS = np.array([r["ss"] for r in rows])
    IX = np.array([r["i"] for r in rows])
    print(f"{len(rows)} pairs; bands {bands} (centres "
          f"{[yc[b] for b in bands]}), bh={bh}")

    out = dict(bands=bands, band_centres={str(b): yc[b] for b in bands},
               n_pairs=len(rows), py0_assumed=args.py0)

    # ---------- per-band: sd ratio (= k*G), roll, noise ----------
    out["band"] = {}
    print("\nPER-BAND covariance (k*G = sd_y/sd_x):")
    for b in bands:
        g = PK[b] > args.pkmin
        Vb = V[b][g]
        sp = np.hypot(*Vb.T)
        m = sp > args.vmin
        if m.sum() < 200:
            print(f"   band {b}: too few moving samples ({m.sum()})")
            continue
        # noise from the 2nd difference within contiguous windows
        nx, ny = [], []
        for ss in sorted(set(SS.tolist())):
            sel = (SS == ss) & g
            if sel.sum() < 40:
                continue
            o = np.argsort(IX[sel])
            nx.append(noise_sd(V[b][sel][o, 0]))
            ny.append(noise_sd(V[b][sel][o, 1]))
        n_x = float(np.median(nx)) if nx else 0.0
        n_y = float(np.median(ny)) if ny else 0.0
        sx, sy = robust_sd(Vb[m, 0]), robust_sd(Vb[m, 1])
        cx = math.sqrt(max(sx ** 2 - n_x ** 2, 1e-9))
        cy = math.sqrt(max(sy ** 2 - n_y ** 2, 1e-9))
        # roll: normalised off-diagonal after de-scaling
        z = np.vstack([Vb[m, 0] / cx, Vb[m, 1] / cy]).T
        C = np.cov(z.T)
        roll = 0.5 * math.degrees(math.atan2(2 * C[0, 1], C[0, 0] - C[1, 1]))
        # residual angular anisotropy (4th harmonic of the de-scaled direction)
        th = np.arctan2(z[:, 1], z[:, 0])
        h2 = float(abs(np.mean(np.exp(2j * th))))
        h4 = float(abs(np.mean(np.exp(4j * th))))
        rec = dict(n=int(m.sum()), sd_x=sx, sd_y=sy, noise_x=n_x, noise_y=n_y,
                   sd_x_corr=cx, sd_y_corr=cy, ratio_raw=sy / sx,
                   ratio=cy / cx, roll_deg=roll, h2=h2, h4=h4,
                   peak_med=float(np.median(PK[b])))
        out["band"][str(b)] = rec
        print(f"   y={yc[b]:6.1f}  n={rec['n']:5d}  sd=({sx:5.2f},{sy:5.2f}) "
              f"noise=({n_x:4.2f},{n_y:4.2f})  ratio raw={sy/sx:.4f} "
              f"corr={cy/cx:.4f}  roll={roll:+.2f}deg  h2={h2:.3f} h4={h4:.3f}")

    # ---------- band-to-band pan ratios: the perspective test ----------
    usable = [b for b in bands if str(b) in out["band"]]
    ref = usable[len(usable) // 2]
    print(f"\nBAND-RATIO PERSPECTIVE TEST (reference band centre y={yc[ref]}):")
    print("   ortho predicts rho_x == rho_y == 1 ; pinhole predicts rho_y == rho_x^2")
    out["ratios"] = {}
    for b in usable:
        g = (PK[b] > args.pkmin) & (PK[ref] > args.pkmin)
        a, bb = V[b][g], V[ref][g]
        sp = np.hypot(*bb.T)
        mx = sp > args.vmin
        # separate x- and y-dominated subsets so the two ratios are independent
        ang = np.abs(np.arctan2(bb[:, 1], bb[:, 0]))
        selx = mx & ((ang < math.radians(35)) | (ang > math.radians(145)))
        sely = mx & (np.abs(np.abs(ang) - math.pi / 2) < math.radians(35))
        rx = float(np.median(a[selx, 0] / bb[selx, 0])) if selx.sum() > 30 else None
        ry = float(np.median(a[sely, 1] / bb[sely, 1])) if sely.sum() > 30 else None
        out["ratios"][str(b)] = dict(y=yc[b], rho_x=rx, rho_y=ry,
                                     nx=int(selx.sum()), ny=int(sely.sum()),
                                     rho_x_sq=rx ** 2 if rx else None)
        print(f"   y={yc[b]:6.1f}  rho_x={rx if rx else float('nan'):.4f} "
              f"(n={int(selx.sum())})   rho_y={ry if ry else float('nan'):.4f} "
              f"(n={int(sely.sum())})   rho_x^2="
              f"{rx**2 if rx else float('nan'):.4f}")

    # ---------- horizon row from the linearity of g_x ----------
    ys = np.array([yc[b] for b in usable], float)
    rx = np.array([out["ratios"][str(b)]["rho_x"] for b in usable], float)
    ok = ~np.isnan(rx)
    # rho_x(y) = (y - y_h)/(y_ref - y_h)  -> linear fit rho_x = m*y + c, y_h = -c/m
    A = np.vstack([ys[ok], np.ones(ok.sum())]).T
    sol, *_ = np.linalg.lstsq(A, rx[ok], rcond=None)
    y_h_x = float(-sol[1] / sol[0])
    pred = A @ sol
    rms_x = float(np.sqrt(np.mean((rx[ok] - pred) ** 2)))
    # same from sqrt(rho_y): sqrt(rho_y) must be the same line
    ry = np.array([out["ratios"][str(b)]["rho_y"] for b in usable], float)
    ok2 = ~np.isnan(ry) & (ry > 0)
    sry = np.sqrt(ry[ok2])
    A2 = np.vstack([ys[ok2], np.ones(ok2.sum())]).T
    sol2, *_ = np.linalg.lstsq(A2, sry, rcond=None)
    y_h_y = float(-sol2[1] / sol2[0])
    print(f"\nHORIZON ROW  from g_x linearity : y_h = {y_h_x:9.1f}  (rms {rms_x:.4f})")
    print(f"             from sqrt(g_y)      : y_h = {y_h_y:9.1f}")

    # ---------- k*G(y) linear in y -> k*lambda and a 3rd horizon estimate ----
    kg = np.array([out["band"][str(b)]["ratio"] for b in usable], float)
    A3 = np.vstack([ys, np.ones(len(ys))]).T
    sol3, *_ = np.linalg.lstsq(A3, kg, rcond=None)
    y_h_r = float(-sol3[1] / sol3[0])
    klam = float(sol3[0])
    print(f"             from k*G slope      : y_h = {y_h_r:9.1f}  "
          f"k*lambda = {klam:.6f} /px")

    y_h = float(np.median([y_h_x, y_h_y, y_h_r]))
    lam = 1.0 / (args.py0 - y_h)
    k = klam / lam
    print(f"\nADOPTED y_h = {y_h:.1f}")
    print(f"  with principal row assumed {args.py0:.0f}:  lambda = {lam:.6f}/px  "
          f"k = {k:.4f}  pitch = {math.degrees(math.asin(min(1,max(0,k)))):.2f} deg")
    for alt in (500.0, 520.0, 540.0, 560.0, 580.0):
        la = 1.0 / (alt - y_h)
        kk = klam / la
        print(f"    sensitivity: principal row {alt:.0f} -> k={kk:.4f} "
              f"pitch={math.degrees(math.asin(min(1,max(0,kk)))):.2f} deg")

    out["solution"] = dict(y_h_from_gx=y_h_x, y_h_from_gy=y_h_y,
                           y_h_from_ratio=y_h_r, y_h=y_h, k_lambda=klam,
                           ref_band=ref, ref_y=yc[ref],
                           lam=lam, k=k,
                           pitch_deg=math.degrees(math.asin(min(1, max(0, k)))))

    # ---------- drift: per-window sd_x at the reference band ----------
    print("\nZOOM/SPEED DRIFT  (sd_x of the reference band, per window):")
    W = []
    for ss in sorted(set(SS.tolist())):
        sel = (SS == ss) & (PK[ref] > args.pkmin)
        Vb = V[ref][sel]
        m = np.hypot(*Vb.T) > args.vmin
        if m.sum() < 60:
            continue
        W.append(dict(ss=float(ss), n=int(m.sum()),
                      sd_x=robust_sd(Vb[m, 0]), sd_y=robust_sd(Vb[m, 1]),
                      p95=float(np.percentile(np.hypot(*Vb[m].T), 95)),
                      p99=float(np.percentile(np.hypot(*Vb[m].T), 99))))
    out["windows"] = W
    if W:
        p95 = np.array([w["p95"] for w in W])
        p99 = np.array([w["p99"] for w in W])
        sdx = np.array([w["sd_x"] for w in W])
        for w in W:
            print(f"   ss={w['ss']:6.0f} n={w['n']:5d} sd_x={w['sd_x']:5.2f} "
                  f"sd_y={w['sd_y']:5.2f} p95={w['p95']:6.2f} p99={w['p99']:6.2f}")
        print(f"\n   p95 speed across {len(W)} windows: med={np.median(p95):.2f} "
              f"min={p95.min():.2f} max={p95.max():.2f} "
              f"cv={p95.std(ddof=1)/p95.mean():.3f}")
        print(f"   p99 speed across windows: med={np.median(p99):.2f} "
              f"min={p99.min():.2f} max={p99.max():.2f} "
              f"cv={p99.std(ddof=1)/p99.mean():.3f}")
        out["drift"] = dict(n_windows=len(W),
                            p95_med=float(np.median(p95)), p95_min=float(p95.min()),
                            p95_max=float(p95.max()),
                            p95_cv=float(p95.std(ddof=1) / p95.mean()),
                            p99_med=float(np.median(p99)), p99_min=float(p99.min()),
                            p99_max=float(p99.max()),
                            p99_cv=float(p99.std(ddof=1) / p99.mean()),
                            sdx_med=float(np.median(sdx)))

    json.dump(out, open(args.out, "w"), indent=1)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
