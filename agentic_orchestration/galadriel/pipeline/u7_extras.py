#!/usr/bin/env python3
"""u7_extras.py — post-hoc diagnostics for the U-7 result.  DECLARED POST-HOC.

None of these can promote the verdict; the verdict is fixed by the pre-registered
rule in prereg.md.  Every one of them is capable of REFUTING or WEAKENING the
positive, which is why they are run.

  1  LAG SCAN.  R-bar as a function of the lag between heading and the density
     bearing.  This is the diagnostic that separates STEERING (heading aligns with
     density at lag <= 0 -- he moves toward where they are/will be) from BEING
     CHASED (density aligns with heading at lag > 0 -- they arrive where he went).
  2  G-e REFINED.  The joint R^2 failed as specified.  Does the residual sit in the
     minimap estimator or in the world-view pan estimator?  Re-fit restricted to
     well-locked pan samples, and report ANGULAR agreement, which is the quantity
     U-7 actually depends on.
  3  PER-WAVE and CHANNEL-ACTIVE splits.
  4  SPEED-BAND split -- is conditioning a property of the fast mill or the slow one?

  run <mm.npy> <result.json> <motion.json> <channel_summary.json> <out.json>
"""
from __future__ import annotations

import json
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import u7_analyse as U

HZ, T0 = 10.0, 682.10
WAVES = [(151, 682.10, 698.55), (152, 698.55, 715.00), (153, 715.00, 729.79),
         (154, 729.79, 743.92), (155, 743.92, 760.25), (156, 760.25, 780.47),
         (157, 780.47, 799.60), (158, 799.60, 812.79), (159, 812.79, 839.04),
         (160, 839.04, 864.75)]


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def rbar(d):
    if len(d) == 0:
        return float("nan"), float("nan")
    z = np.exp(1j * d).mean()
    return float(abs(z)), float(math.degrees(np.angle(z)))


def run(mmpath, respath, motionpath, wavepath, out):
    S = np.load(respath.replace(".json", "_series.npz"))
    tp = S["theta_p"]; mag = S["mag"]
    n = len(tp)
    t = T0 + np.arange(n) / HZ
    res = {"lag_scan": {}, "per_wave": {}, "speed_band": {}, "G_e_refined": {}}

    # --- 1 lag scan -----------------------------------------------------------
    for R in (20, 30):
        tc = S[f"theta_c_{R}"]
        rows = []
        for lag in range(-50, 51):          # +/- 5 s at 0.1 s
            s = np.roll(tc, lag)
            ok = np.isfinite(tp) & np.isfinite(s)
            r, mu = rbar(wrap(tp[ok] - s[ok]))
            rows.append([round(lag / HZ, 2), round(r, 4), round(mu, 1), int(ok.sum())])
        res["lag_scan"][str(R)] = rows
        best = max(rows, key=lambda z: z[1])
        res["lag_scan"][f"{R}_peak_lag_s"] = best[0]
        res["lag_scan"][f"{R}_peak_Rbar"] = best[1]

    # --- 3 per-wave -----------------------------------------------------------
    for R in (20, 30):
        tc = S[f"theta_c_{R}"]
        ok0 = np.isfinite(tp) & np.isfinite(tc)
        pw = []
        for (w, a, b) in WAVES:
            m = ok0 & (t >= a) & (t < b)
            r, mu = rbar(wrap(tp[m] - tc[m]))
            pw.append({"wave": w, "n": int(m.sum()), "Rbar": round(r, 4),
                       "mu_deg": round(mu, 1)})
        res["per_wave"][str(R)] = pw

    # --- 4 speed band ---------------------------------------------------------
    for R in (20, 30):
        tc = S[f"theta_c_{R}"]
        ok0 = np.isfinite(tp) & np.isfinite(tc) & np.isfinite(mag)
        q = np.nanpercentile(mag[ok0], [33, 67])
        bands = [("slow", -np.inf, q[0]), ("mid", q[0], q[1]), ("fast", q[1], np.inf)]
        bb = []
        for nm, lo, hi in bands:
            m = ok0 & (mag > lo) & (mag <= hi)
            r, mu = rbar(wrap(tp[m] - tc[m]))
            bb.append({"band": nm, "px_over_baseline": [None if not np.isfinite(lo) else round(float(lo), 2),
                                                        None if not np.isfinite(hi) else round(float(hi), 2)],
                       "n": int(m.sum()), "Rbar": round(r, 4), "mu_deg": round(mu, 1)})
        res["speed_band"][str(R)] = bb

    # --- 2 G-e refined --------------------------------------------------------
    M = json.load(open(motionpath))
    mr = M["rows"]
    mt = np.array([r["t"] for r in mr])
    mdx = np.array([r["dx"] for r in mr]); mdy = np.array([r["dy"] for r in mr])
    mlock = np.array([r.get("lock", 0.0) for r in mr])
    cx = np.concatenate([[0.0], np.cumsum(mdx)]); cy = np.concatenate([[0.0], np.cumsum(mdy)])
    tg = np.concatenate([mt, [mt[-1] + 0.05]])

    a = np.load(mmpath, mmap_mode="r")
    from scipy import ndimage as ndi
    H, W = a.shape[1], a.shape[2]
    ax, ay = U.ANCHOR
    yy, xx = np.mgrid[0:H, 0:W]
    dm = np.hypot(xx - ax, yy - ay) <= 78.0

    def gems_of(fr):
        tm = U.teal(fr) & dm
        lab, k = ndi.label(tm)
        o = []
        for j in range(1, k + 1):
            ys, xs = np.nonzero(lab == j)
            if len(ys) < 6:
                continue
            o.append((float(xs.mean()), float(ys.mean()), len(ys)))
        return o

    X, Y, LK = [], [], []
    B = U.B_SAMPLES
    for i in range(0, n - B):
        g = U.gem_step(gems_of(np.asarray(a[i])), gems_of(np.asarray(a[i + B])))
        if g is None:
            continue
        t0 = T0 + i / HZ; t1 = t0 + B / HZ
        sx = np.interp(t1, tg, cx) - np.interp(t0, tg, cx)
        sy = np.interp(t1, tg, cy) - np.interp(t0, tg, cy)
        w = (mt >= t0) & (mt < t1)
        X.append([g[0], g[1]]); Y.append([sx, sy])
        LK.append(float(np.median(mlock[w])) if w.any() else 0.0)
    X = np.array(X); Y = np.array(Y); LK = np.array(LK)

    def fit(sel):
        A, *_ = np.linalg.lstsq(X[sel], Y[sel], rcond=None)
        p = X[sel] @ A
        r2 = 1 - float(((Y[sel] - p) ** 2).sum()) / float(((Y[sel] - Y[sel].mean(axis=0)) ** 2).sum())
        return A, r2

    A_all, r2_all = fit(np.ones(len(X), bool))
    out_rows = []
    for qq in [0, 25, 50, 75, 90]:
        thr = np.percentile(LK, qq)
        sel = LK >= thr
        if sel.sum() < 50:
            continue
        _, r2 = fit(sel)
        out_rows.append({"lock_pctile_floor": qq, "n": int(sel.sum()), "R2": round(r2, 4)})
    # angular agreement: map minimap step through A_all, compare bearings, moving only
    mv = np.hypot(X[:, 0], X[:, 1]) >= U.D_MIN
    pm = X[mv] @ A_all
    ang_m = np.arctan2(pm[:, 0], -pm[:, 1])
    ang_s = np.arctan2(Y[mv][:, 0], -Y[mv][:, 1])
    dd = np.degrees(np.abs(wrap(ang_m - ang_s)))
    res["G_e_refined"] = {
        "R2_by_pan_lock_floor": out_rows,
        "fitted_map": [[round(float(A_all[0, 0]), 4), round(float(A_all[0, 1]), 4)],
                       [round(float(A_all[1, 0]), 4), round(float(A_all[1, 1]), 4)]],
        "map_axis_ratio_y_over_x": round(abs(float(A_all[1, 1])) / abs(float(A_all[0, 0])), 4),
        "angular_agreement_moving": {
            "n": int(mv.sum()),
            "median_abs_deg": round(float(np.median(dd)), 2),
            "frac_within_30deg": round(float((dd <= 30).mean()), 4),
            "frac_within_60deg": round(float((dd <= 60).mean()), 4),
        },
    }
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "lag_scan"}, indent=1))
    for R in (20, 30):
        print(f"lag scan R={R}: peak lag {res['lag_scan'][f'{R}_peak_lag_s']} s, "
              f"Rbar {res['lag_scan'][f'{R}_peak_Rbar']}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
