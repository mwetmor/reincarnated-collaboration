#!/usr/bin/env python3
"""GAL-CAM: absolute scale from the nova, RECTIFIED against the measured horizon.

THE RECTIFICATION
-----------------
With the horizon row y_h known (gc_geom.py), the ground-plane scales are

    g_x(y) = A * (y - y_h)          px per metre of ground-X
    g_y(y) = C * (y - y_h)^2        px per metre of ground-Z

for two unknown constants A and C. Define the RECTIFIED coordinates

    a = (x - px0) / (y - y_h)       so ground X = a / A
    b = 1 / (y - y_h)               so ground Z = b / C  (+const)

A projectile flying in a straight ground line at constant speed must therefore
have a and b LINEAR IN FRAME NUMBER even though its screen track is curved.
That linearity is a test of the camera model that costs nothing extra, and it is
reported.

SOLVING A AND C
---------------
Each tracked lance gives one equation, because its ground speed is known:

    (adot/A)^2 + (bdot/C)^2 = (14/60)^2

Two lances -> two equations, linear in (1/A^2, 1/C^2). Solvable.

THE FREE CHECK
--------------
A and C are solved from SPEED only. But the ring is 16 rays at 22.5 deg, so the
ground azimuths implied by the solved A and C must differ by a multiple of
22.5 deg. Nothing was fitted to make that true. It is reported as a residual in
degrees, and if it comes out at some arbitrary angle the solution is withdrawn.
"""
import argparse
import json
import math

import numpy as np


def rectify(x, y, y_h, px0):
    dy = y - y_h
    return (x - px0) / dy, 1.0 / dy


def lin(f, v):
    A = np.vstack([f - f.mean(), np.ones(len(f))]).T
    sol, *_ = np.linalg.lstsq(A, v, rcond=None)
    res = v - A @ sol
    return float(sol[0]), float(np.sqrt(np.mean(res ** 2))), float(np.abs(res).max())


def solve(L, y_h, px0, vproj=14.0, fps=60.0):
    D = []
    for l in L:
        f = np.array(l["f"], float); x = np.array(l["x"], float); y = np.array(l["y"], float)
        a, b = rectify(x, y, y_h, px0)
        ad, arms, amax = lin(f, a)
        bd, brms, bmax = lin(f, b)
        D.append(dict(th=l["th"], n=len(f), adot=ad, bdot=bd,
                      a_rms=arms, a_max=amax, a_span=float(a.max() - a.min()),
                      b_rms=brms, b_max=bmax, b_span=float(b.max() - b.min())))
    if len(D) < 2:
        return D, None
    M = np.array([[D[0]["adot"] ** 2, D[0]["bdot"] ** 2],
                  [D[1]["adot"] ** 2, D[1]["bdot"] ** 2]])
    rhs = np.array([(vproj / fps) ** 2] * 2)
    try:
        PQ = np.linalg.solve(M, rhs)
    except np.linalg.LinAlgError:
        return D, None
    if (PQ <= 0).any():
        return D, None
    A, C = 1 / math.sqrt(PQ[0]), 1 / math.sqrt(PQ[1])
    psi = [math.degrees(math.atan2(d["bdot"] * (A / C), d["adot"])) for d in D]
    dpsi = psi[1] - psi[0]
    m = round(dpsi / 22.5)
    resid = dpsi - m * 22.5
    cond = float(np.linalg.cond(M))
    return D, dict(A=A, C=C, A_over_C=A / C, psi=psi, dpsi=dpsi,
                   step=m, resid_deg=resid, cond=cond)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lances", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--y_h", type=float, default=-1900.0)
    ap.add_argument("--y_h_lo", type=float, default=-2250.0)
    ap.add_argument("--y_h_hi", type=float, default=-1600.0)
    ap.add_argument("--px0", type=float, default=960.0)
    ap.add_argument("--py0", type=float, default=540.0)
    ap.add_argument("--y_player", type=float, default=602.0)
    args = ap.parse_args()

    L = json.load(open(args.lances))["lances"]
    print(f"{len(L)} lances: " + ", ".join(f"th={l['th']:.0f} n={l['n']}" for l in L))

    D, S = solve(L, args.y_h, args.px0)
    print("\nRECTIFIED-TRACK LINEARITY (model check; rms as % of span):")
    for d in D:
        print(f"  th={d['th']:7.2f} n={d['n']:3d}  a: rms={d['a_rms']:.3e} "
              f"({100*d['a_rms']/d['a_span']:.2f}% of span)   b: rms={d['b_rms']:.3e} "
              f"({100*d['b_rms']/d['b_span']:.2f}% of span)")
    if not S:
        print("\nSOLVE FAILED -> CANNOT-ANSWER")
        return
    gx = S["A"] * (args.y_player - args.y_h)
    gy = S["C"] * (args.y_player - args.y_h) ** 2
    kG = gy / gx
    lam = 1.0 / (args.py0 - args.y_h)
    k = kG * (args.py0 - args.y_h) / (args.y_player - args.y_h)
    print(f"\nSOLUTION at y_h={args.y_h:.0f}, px0={args.px0:.0f}")
    print(f"  A={S['A']:.6f} px/m/px     C={S['C']:.3e} px/m/px^2")
    print(f"  ground azimuths: {S['psi'][0]:.2f} deg, {S['psi'][1]:.2f} deg  "
          f"-> separation {S['dpsi']:.2f} deg")
    print(f"  nearest multiple of 22.5: {S['step']} steps; RESIDUAL "
          f"{S['resid_deg']:+.2f} deg   (matrix cond {S['cond']:.1f})")
    print(f"  at the player row y={args.y_player:.0f}: "
          f"g_x={gx:.2f} px/m   g_y={gy:.2f} px/m   g_y/g_x={kG:.4f}")
    print(f"  with principal row {args.py0:.0f}: k=sin(pitch)={k:.4f} -> "
          f"pitch={math.degrees(math.asin(min(1,k))):.2f} deg")

    print("\nSENSITIVITY to the horizon row:")
    sens = []
    for yh in np.linspace(args.y_h_lo, args.y_h_hi, 8):
        _, s2 = solve(L, yh, args.px0)
        if not s2:
            continue
        g1 = s2["A"] * (args.y_player - yh)
        g2 = s2["C"] * (args.y_player - yh) ** 2
        kk = (g2 / g1) * (args.py0 - yh) / (args.y_player - yh)
        sens.append(dict(y_h=float(yh), g_x=g1, g_y=g2, kG=g2 / g1, k=kk,
                         resid_deg=s2["resid_deg"]))
        print(f"  y_h={yh:8.0f}  g_x={g1:6.2f}  g_y={g2:6.2f}  kG={g2/g1:.4f} "
              f"k={kk:.4f} pitch={math.degrees(math.asin(min(1,kk))):5.2f}  "
              f"22.5-residual={s2['resid_deg']:+.2f} deg")

    print("\nSENSITIVITY to the principal column px0:")
    for p in (900.0, 930.0, 960.0, 990.0, 1020.0):
        _, s3 = solve(L, args.y_h, p)
        if not s3:
            continue
        g1 = s3["A"] * (args.y_player - args.y_h)
        g2 = s3["C"] * (args.y_player - args.y_h) ** 2
        print(f"  px0={p:6.0f}  g_x={g1:6.2f}  g_y={g2:6.2f}  kG={g2/g1:.4f}  "
              f"22.5-residual={s3['resid_deg']:+.2f} deg")

    json.dump(dict(y_h=args.y_h, px0=args.px0, py0=args.py0,
                   y_player=args.y_player, lances=D, solution=S,
                   g_x_player=gx, g_y_player=gy, kG_player=kG, k=k,
                   pitch_deg=math.degrees(math.asin(min(1, k))),
                   sensitivity_y_h=sens), open(args.out, "w"), indent=1)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
