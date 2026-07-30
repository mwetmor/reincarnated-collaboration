#!/usr/bin/env python3
"""GAL-CAM: did the zoom move during the session?

TWO INDICATORS, BECAUSE ONE IS AMBIGUOUS
----------------------------------------
(1) The ellipse SEMI-AXIS of the movement-episode pan cloud, per session chunk.
    That axis is (ground run speed) x (px per metre). It moves if the ZOOM moves
    -- but also if the player's MOVEMENT SPEED moves (boots, buffs, the werewolf
    charge). This instrument alone therefore cannot attribute a change, and the
    report must not pretend otherwise.

(2) The HORIZON ROW per chunk. A dolly zoom (camera slides along its axis, the
    usual ARPG wheel-zoom) changes the scale but NOT the horizon row, because
    the horizon depends only on focal length and pitch. An FOV zoom changes both.
    So indicator (2) discriminates the KIND of change, and a stable horizon with
    a moving axis points at movement speed or a dolly, not at a lens change.

Read together: if BOTH are flat, nothing moved and the modal scale is the whole
story. That is a stronger statement than either alone.
"""
import argparse
import json
import math

import numpy as np
from scipy.optimize import least_squares


def episodes(rows, band, SS, IX, vmin=2.0, pkmin=0.03, minlen=8, dth=0.25):
    V = np.array([r[f"b{band}"][:2] for r in rows])
    PK = np.array([r[f"b{band}"][2] for r in rows])
    out = []
    for ss in sorted(set(SS.tolist())):
        m = SS == ss
        o = np.argsort(IX[m])
        vv, pk = V[m][o], PK[m][o]
        sp = np.hypot(*vv.T)
        i = 0
        while i < len(sp):
            if sp[i] < vmin or pk[i] < pkmin:
                i += 1
                continue
            j = i
            while (j + 1 < len(sp) and sp[j + 1] >= vmin and pk[j + 1] >= pkmin
                   and abs(math.atan2(vv[j + 1][1], vv[j + 1][0])
                           - math.atan2(vv[i][1], vv[i][0])) < dth):
                j += 1
            if j - i + 1 >= minlen:
                out.append([float(np.median(vv[i:j + 1, 0])),
                            float(np.median(vv[i:j + 1, 1])), float(ss)])
            i = j + 1
    return np.array(out)


def fit_ellipse(E):
    U, Wv = E[:, 0], E[:, 1]

    def res(p):
        return np.sqrt((U / p[0]) ** 2 + (Wv / p[1]) ** 2) - 1.0
    r = least_squares(res, [7.0, 5.5], loss="soft_l1", f_scale=0.10)
    return float(r.x[0]), float(r.x[1])


def horizon_chunk(grid, lo, hi, pkmin=0.03, dymin=2.5):
    cells = grid["cells"]
    xs = sorted(set(c[0] for c in cells)); ys = sorted(set(c[1] for c in cells))
    idx = {(c[0], c[1]): i for i, c in enumerate(cells)}
    est = []
    for r in grid["rows"]:
        if not (lo <= r["ss"] < hi):
            continue
        v = r["v"]
        for y in ys:
            dx, dy = [], []
            for x in xs:
                a, b, pk = v[idx[(x, y)]]
                if pk >= pkmin:
                    dx.append((x, a)); dy.append(b)
            if len(dx) < 4:
                continue
            dyv = float(np.median(dy))
            if abs(dyv) < dymin:
                continue
            D = np.array(dx)
            xx = D[:, 0] - D[:, 0].mean()
            A = np.vstack([xx, np.ones(len(xx))]).T
            sol, *_ = np.linalg.lstsq(A, D[:, 1], rcond=None)
            if np.abs(D[:, 1] - A @ sol).max() > 1.2 or abs(sol[0]) < 1e-4:
                continue
            est.append(y - dyv / sol[0])
    est = np.array([e for e in est if -20000 < e < 2000])
    return est


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pan", required=True)
    ap.add_argument("--grid", required=True)
    ap.add_argument("--band", type=int, default=320)
    ap.add_argument("--nchunk", type=int, default=6)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    d = json.load(open(args.pan))
    rows = d["rows"]
    SS = np.array([r["ss"] for r in rows]); IX = np.array([r["i"] for r in rows])
    E = episodes(rows, args.band, SS, IX)
    print(f"{len(E)} movement episodes at band y={args.band}")
    g = json.load(open(args.grid))

    t0, t1 = SS.min(), SS.max() + 1
    edges = np.linspace(t0, t1, args.nchunk + 1)
    res = []
    print("\nchunk (s)          nep    A(px/f)  B(px/f)   B/A      y_h      n_yh")
    for i in range(args.nchunk):
        lo, hi = edges[i], edges[i + 1]
        sel = (E[:, 2] >= lo) & (E[:, 2] < hi)
        rec = dict(lo=float(lo), hi=float(hi), nep=int(sel.sum()))
        if sel.sum() >= 12:
            A, B = fit_ellipse(E[sel])
            rec.update(A=A, B=B, ratio=B / A)
        yh = horizon_chunk(g, lo, hi)
        if len(yh) >= 100:
            rec.update(y_h=float(np.median(yh)), n_yh=int(len(yh)))
        res.append(rec)
        print(f"  {lo:6.0f}-{hi:6.0f}  {rec['nep']:5d}   "
              f"{rec.get('A', float('nan')):7.3f}  {rec.get('B', float('nan')):7.3f}  "
              f"{rec.get('ratio', float('nan')):6.4f}  "
              f"{rec.get('y_h', float('nan')):8.0f}  {rec.get('n_yh', 0):5d}")

    A = np.array([r["A"] for r in res if "A" in r])
    Y = np.array([r["y_h"] for r in res if "y_h" in r])
    print(f"\n  A  across chunks: med={np.median(A):.3f} min={A.min():.3f} "
          f"max={A.max():.3f}  spread={100*(A.max()-A.min())/np.median(A):.1f}%")
    print(f"  y_h across chunks: med={np.median(Y):.0f} min={Y.min():.0f} "
          f"max={Y.max():.0f}  spread={100*(Y.max()-Y.min())/abs(np.median(Y)):.1f}%")
    json.dump(dict(band=args.band, chunks=res,
                   A_med=float(np.median(A)), A_min=float(A.min()),
                   A_max=float(A.max()),
                   A_spread_pct=float(100 * (A.max() - A.min()) / np.median(A)),
                   y_h_med=float(np.median(Y)), y_h_min=float(Y.min()),
                   y_h_max=float(Y.max())), open(args.out, "w"), indent=1)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
