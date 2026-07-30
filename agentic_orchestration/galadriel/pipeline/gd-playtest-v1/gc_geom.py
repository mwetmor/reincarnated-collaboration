#!/usr/bin/env python3
"""GAL-CAM: horizon row y_h from the grid motion field, by three routes.

ROUTE 1 -- DIVERGENCE (the strong one; assumes nothing but the ground plane)
    (d dx / d x') / dy  =  1 / (y - y_h)
  Camera translation, scale and pitch all cancel. Per frame pair, per grid row,
  one estimate of y_h. Needs a frame pair with real vertical motion.

ROUTE 2 -- sqrt(dy) LINEARITY
    dy ~ G^2  =>  sqrt(|dy|) is linear in screen row and crosses zero at y_h.

ROUTE 3 -- dx LINEARITY
    dx ~ G    =>  |dx| is linear in screen row and crosses zero at y_h.

Routes 2 and 3 must agree with each other AND with route 1. If route 2 and
route 3 give different y_h then dy is not going as the square of dx and the
ground-plane pinhole model is wrong -- that is the point of running all three.

Orthographic camera => infinite y_h (dx and dy both flat across rows). So a
finite, reproducible y_h IS the perspective finding, and its magnitude is the
strength of the perspective.
"""
import argparse
import json
import math

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pkmin", type=float, default=0.03)
    ap.add_argument("--dymin", type=float, default=2.5)
    ap.add_argument("--dxmin", type=float, default=2.5)
    args = ap.parse_args()

    d = json.load(open(args.grid))
    cells = d["cells"]
    xs = sorted(set(c[0] for c in cells))
    ys = sorted(set(c[1] for c in cells))
    idx = {(c[0], c[1]): i for i, c in enumerate(cells)}
    rows = d["rows"]
    print(f"{len(rows)} frame pairs; grid x={xs} y={ys}")

    V = np.array([r["v"] for r in rows])          # (N, ncell, 3)
    SS = np.array([r["ss"] for r in rows])

    # --- per-row aggregates per frame pair ---
    r1, r2, r3 = [], [], []
    dyx_dep = []
    for n in range(len(rows)):
        rowdat = {}
        for y in ys:
            dx, dy, ok = [], [], []
            for x in xs:
                vx, vy, pk = V[n, idx[(x, y)]]
                if pk >= args.pkmin:
                    dx.append((x, vx)); dy.append((x, vy))
            if len(dx) >= 4:
                rowdat[y] = (np.array(dx), np.array(dy))
        if len(rowdat) < 4:
            continue

        # ROUTE 1: divergence / dy, per row
        for y, (DX, DY) in rowdat.items():
            dyv = np.median(DY[:, 1])
            if abs(dyv) < args.dymin:
                continue
            xx = DX[:, 0] - np.mean(DX[:, 0])
            A = np.vstack([xx, np.ones(len(xx))]).T
            sol, *_ = np.linalg.lstsq(A, DX[:, 1], rcond=None)
            resid = DX[:, 1] - A @ sol
            if np.abs(resid).max() > 1.2:
                continue
            s = sol[0]
            if abs(s) < 1e-4:
                continue
            r1.append(y - dyv / s)
            # does dy depend on x'? (model says no)
            solq, *_ = np.linalg.lstsq(A, DY[:, 1], rcond=None)
            dyx_dep.append(abs(solq[0]) * 500.0 / max(abs(dyv), 1e-6))

        yy = np.array(sorted(rowdat))
        dyv = np.array([np.median(rowdat[y][1][:, 1]) for y in yy])
        dxv = np.array([np.median(rowdat[y][0][:, 1]) for y in yy])
        # ROUTE 2
        if np.all(np.abs(dyv) > args.dymin) and (np.sign(dyv) == np.sign(dyv[0])).all():
            t = np.sqrt(np.abs(dyv))
            A = np.vstack([yy, np.ones(len(yy))]).T
            sol, *_ = np.linalg.lstsq(A, t, rcond=None)
            pr = A @ sol
            if abs(sol[0]) > 1e-6 and np.abs(t - pr).max() < 0.06 * t.mean():
                r2.append(-sol[1] / sol[0])
        # ROUTE 3
        if np.all(np.abs(dxv) > args.dxmin) and (np.sign(dxv) == np.sign(dxv[0])).all():
            t = np.abs(dxv)
            A = np.vstack([yy, np.ones(len(yy))]).T
            sol, *_ = np.linalg.lstsq(A, t, rcond=None)
            pr = A @ sol
            if abs(sol[0]) > 1e-6 and np.abs(t - pr).max() < 0.06 * t.mean():
                r3.append(-sol[1] / sol[0])

    def rep(name, v, lo=-20000, hi=2000):
        v = np.array([x for x in v if lo < x < hi])
        if len(v) < 20:
            print(f"  {name}: only {len(v)} usable estimates -> CANNOT-ANSWER")
            return None
        q = np.percentile(v, [16, 25, 50, 75, 84])
        rng = np.random.default_rng(5)
        bs = [np.median(rng.choice(v, len(v))) for _ in range(2000)]
        ci = np.percentile(bs, [2.5, 97.5])
        print(f"  {name}: n={len(v):5d}  median={q[2]:9.1f}  IQR=[{q[1]:.0f},{q[3]:.0f}]"
              f"  boot95=[{ci[0]:.0f},{ci[1]:.0f}]")
        return dict(n=int(len(v)), median=float(q[2]), p16=float(q[0]),
                    p84=float(q[4]), boot95=[float(ci[0]), float(ci[1])])

    print("\nHORIZON ROW y_h (screen row; negative = above the top of the frame):")
    o1 = rep("route 1 divergence ", r1)
    o2 = rep("route 2 sqrt(dy)   ", r2)
    o3 = rep("route 3 |dx|       ", r3)
    if dyx_dep:
        print(f"\n  dy dependence on x' (model says 0): median "
              f"{np.median(dyx_dep) * 100:.1f}% per 500 px  (n={len(dyx_dep)})")

    json.dump(dict(route1=o1, route2=o2, route3=o3, xs=xs, ys=ys,
                   dy_x_dependence_med=float(np.median(dyx_dep)) if dyx_dep else None),
              open(args.out, "w"), indent=1)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
