#!/usr/bin/env python3
"""GAL-CAM: the DECISION SURFACE -- visible ground metres around the player.

Given the solved ground-plane camera

    g_x(y) = A * (y - y_h)          px per metre of ground-X at screen row y
    g_y(y) = C * (y - y_h)^2        px per metre of ground-Z at screen row y

the inverse map from screen to ground, taken relative to the player's anchor, is

    X(x, y) = (x - px0) / g_x(y)
    Z(y)    = 1 / (C * (y - y_h))          [note: DECREASING in y; down-screen
                                            is nearer the camera]

Because g_x depends on the row, the visible ground is a TRAPEZOID, not a
rectangle: wide at the far (up-screen) edge, narrow at the near edge. The report
gives the box at the player's own row (the honest "within X metres of me"
number) AND the trapezoid corners (the honest shape).

Two surfaces are computed, because they answer different questions:
  FRUSTUM  -- what the projection puts on the display
  DECISION -- what was actually legible to the player, i.e. frustum minus the
              opaque HUD. Ground drawn under the skill bar was not part of
              anybody's decision.

Uncertainty is propagated by Monte Carlo over A, C, y_h and the player anchor,
using the bootstrap distributions from gc_ring.py rather than a nominal +-.
"""
import argparse
import json
import math

import numpy as np


def surface(A, C, y_h, px0, xp, yp, x0, x1, y0, y1):
    gx = lambda y: A * (y - y_h)
    Z = lambda y: 1.0 / (C * (y - y_h))
    zp = Z(yp)
    out = dict(
        g_x_player=gx(yp), g_y_player=C * (yp - y_h) ** 2,
        left_at_player=(x0 - px0) / gx(yp) - (xp - px0) / gx(yp),
        right_at_player=(x1 - px0) / gx(yp) - (xp - px0) / gx(yp),
        far=Z(y0) - zp, near=Z(y1) - zp,
        halfwidth_far=(x1 - px0) / gx(y0), halfwidth_near=(x1 - px0) / gx(y1),
        g_x_top=gx(y0), g_x_bot=gx(y1),
        m_per_px_x_player=1.0 / gx(yp),
        m_per_px_y_player=1.0 / (C * (yp - y_h) ** 2),
        m_per_px_y_top=1.0 / (C * (y0 - y_h) ** 2),
        m_per_px_y_bot=1.0 / (C * (y1 - y_h) ** 2),
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ring", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--px0", type=float, default=960.0)
    ap.add_argument("--xp", type=float, default=962.0)
    ap.add_argument("--yp", type=float, default=595.0)
    ap.add_argument("--n", type=int, default=20000)
    args = ap.parse_args()

    R = json.load(open(args.ring))
    A0, C0 = R["solution"]["A"], R["solution"]["C"]
    y_h0 = R["y_h"]

    frames = dict(
        frustum=(0.0, 1919.0, 0.0, 1079.0),
        decision=(0.0, 1919.0, 60.0, 950.0),
    )

    rng = np.random.default_rng(23)
    res = {k: {} for k in frames}
    nominal = {}
    for name, (x0, x1, y0, y1) in frames.items():
        nominal[name] = surface(A0, C0, y_h0, args.px0, args.xp, args.yp,
                                x0, x1, y0, y1)
        acc = {k: [] for k in nominal[name]}
        for _ in range(args.n):
            # A and C are correlated through the solve; resample them jointly
            # by resampling the ratio and the x-scale separately within their
            # bootstrap bands (gc_ring bootstrap: g_x +-3.7%, kG +-11% at 95%)
            gx_p = rng.normal(54.47, 1.02)          # px/m at the player row
            kG = rng.normal(0.816, 0.045)
            yh = rng.uniform(-2500, -1500)
            xp = args.xp + rng.normal(0, 10)
            yp = args.yp + rng.normal(0, 20)
            A = gx_p / (yp - yh)
            C = kG * gx_p / (yp - yh) ** 2
            s = surface(A, C, yh, args.px0, xp, yp, x0, x1, y0, y1)
            for k, v in s.items():
                acc[k].append(v)
        for k, v in acc.items():
            v = np.array(v)
            res[name][k] = dict(p2_5=float(np.percentile(v, 2.5)),
                                p50=float(np.percentile(v, 50)),
                                p97_5=float(np.percentile(v, 97.5)))

    for name in frames:
        print(f"\n=== {name.upper()}  (screen box {frames[name]}) ===")
        for k in ["left_at_player", "right_at_player", "far", "near",
                  "halfwidth_far", "halfwidth_near", "g_x_player",
                  "m_per_px_x_player", "m_per_px_y_player",
                  "m_per_px_y_top", "m_per_px_y_bot"]:
            q = res[name][k]
            print(f"  {k:20s} {q['p50']:9.3f}   95% [{q['p2_5']:8.3f},"
                  f" {q['p97_5']:8.3f}]   (nominal {nominal[name][k]:.3f})")

    # --- sim geometry vs the surface ---
    d = res["decision"]
    print("\n=== SIM GEOMETRY vs THE DECISION SURFACE ===")
    tests = [("nova reach", 12.0), ("melee separation", 1.6),
             ("death-2 measured range", 1.26), ("nova explosion radius", 1.5)]
    rows = []
    for nm, m in tests:
        row = dict(name=nm, metres=m,
                   fits_left=m <= -d["left_at_player"]["p50"],
                   fits_right=m <= d["right_at_player"]["p50"],
                   fits_far=m <= d["far"]["p50"],
                   fits_near=m <= -d["near"]["p50"],
                   px_x=m * d["g_x_player"]["p50"],
                   px_y=m * (d["g_x_player"]["p50"] * 0.820))
        rows.append(row)
        print(f"  {nm:24s} {m:5.2f} m -> {row['px_x']:6.1f} px across, "
              f"{row['px_y']:6.1f} px up/down;  inside box: "
              f"L={row['fits_left']} R={row['fits_right']} "
              f"FAR={row['fits_far']} NEAR={row['fits_near']}")

    json.dump(dict(nominal=nominal, mc=res, sim=rows,
                   anchor=dict(x=args.xp, y=args.yp, px0=args.px0),
                   frames={k: list(v) for k, v in frames.items()}),
              open(args.out, "w"), indent=1)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
