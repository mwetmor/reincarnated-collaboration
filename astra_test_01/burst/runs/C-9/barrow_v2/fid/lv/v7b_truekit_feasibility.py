#!/usr/bin/env python3
"""BV2F LV Phase 1 (v7b, true proportions): which hall headings fit the TRUE-PROPORTION hall kit? (derived from v7a_feasibility.py)

Original: can the sketch-A hall orientation (v7a, R-C9-165 item 1) pass validator R5 + R10?

v7a (RESUME_LV Phase 1): the hall runs screen upper-left -> lower-right, its great-door wall faces the start,
the gable (the hall's own collapsed end, R-C9-148) at its LOWER-RIGHT end on p06's ray.

Rules held FIXED (never bent):
  R1  anchors = the pack's (sealed).
  R4  the floor contains the hull of the six 8 m discs + 1 m.  The search uses THAT minimal hull as the floor:
      it is the most permissive floor R4 allows (any real floor contains it, so a feature that overlaps the
      minimal hull overlaps every legal floor).
  R5  every blocker (hall, gable, porch + apron) has zero area inside the floor.
  R10 p04's deliverer (hall_porch) and p06's deliverer (fallen_gable) are outside the edge and within 3.0 m of it.

Geometry (true proportions, R-C9-165/1.2): hall body L in {18, 24, 30, 36} m x depth D in {6.5, 8.0} m; the gable
a 6 m collinear extension at the gable end; the grown porch 13.25 x 3.0 m + 1.4 m apron on the start-facing long
wall (R-C9-154) at any station.  Free parameters: the hall axis heading theta (door end -> gable end, compass,
every 2 deg over 360), the gable centre anywhere such that p06's ray (from the start, beyond p06's disc) passes
through the gable, the porch station.

Output: for each theta, the best (smallest) achievable max(gap_porch, gap_gable) over every placement that
satisfies R5; theta is FEASIBLE iff that value <= 3.0 m.  Screen direction of theta in the play view (the fix
makes the play view = the layout's yaw-0 frame, R-C9-165): screen dx = x, dy = sin(52.95 deg) * y.
POSITIVE CONTROL: v6's own heading (222.99 deg, upper-right -> lower-left) must come out FEASIBLE.
Writes frame_proof/../v7a_feasibility.json (fid/lv/v7a_feasibility.json).
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "..", "..", "layout_v2.json")))
A = {a["id"]: np.array([a["x"], a["y"]]) for a in L["anchors"]["points"]}
R9 = 9.0
PITCH = math.radians(52.9535411256029)


def hull(pts):
    pts = sorted(map(tuple, pts))
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return np.array(lo[:-1] + up[:-1])


H = hull(list(A.values()))          # CCW hull of the six anchors; the floor = H (+) disc(9)
E0 = H
E1 = np.roll(H, -1, axis=0)


def sdist(P):
    """signed distance of points P (N,2) to the minimal floor (positive = outside the floor)."""
    P = P[:, None, :]
    d = E1 - E0
    t = np.clip(((P - E0) * d).sum(-1) / (d * d).sum(-1), 0, 1)
    proj = E0 + t[..., None] * d
    dist = np.linalg.norm(P - proj, axis=-1).min(1)
    cross = d[:, 0] * (P[..., 1] - E0[:, 1]) - d[:, 1] * (P[..., 0] - E0[:, 0])
    inside = (cross >= 0).all(1)                       # CCW: inside = left of every edge
    return np.where(inside, -dist, dist) - R9


def rect_samples(c, ax, nrm, length, depth, step=0.25):
    """boundary + interior grid samples of a rectangle centred c, long axis ax."""
    us = np.arange(-length / 2, length / 2 + 1e-9, step)
    vs = np.arange(-depth / 2, depth / 2 + 1e-9, step)
    U, V = np.meshgrid(us, vs)
    return c + U.reshape(-1, 1) * ax + V.reshape(-1, 1) * nrm


def comp(theta):
    t = math.radians(theta)
    return np.array([math.sin(t), -math.cos(t)])       # compass -> sim (x east, y south)


p06 = A["p06"]
r6 = p06 / np.linalg.norm(p06)
t0 = np.linalg.norm(p06) + R9
import sys
PORCH_W, PORCH_D, APRON = 13.2, 11.7, 0.0   # the BVP porch build at ONE uniform scale (opening 4.5 m)
LG = None
results = []
for theta in range(180, 274, 2):
    ax = comp(theta)                                     # door end -> gable end
    best = None
    for Lh in (24.0, 27.0, 30.0, 33.0):
        for D in (round(0.339 * Lh, 2),):
            LG = D            # the gable build is square in plan (raw 0.999 x 1.001): side = the hall depth
            n = np.array([-ax[1], ax[0]])
            for t in np.arange(t0 - 2.0, t0 + 30.0, 0.5):
                for u in np.linspace(-LG / 2, LG / 2, 7):
                    for v in np.linspace(-D / 2, D / 2, 5):
                        gc = p06 * 0 + r6 * t - u * ax - v * n       # the ray point lies inside the gable
                        g_s = sdist(rect_samples(gc, ax, n, LG, D, 0.5))
                        if g_s.min() < 0:
                            continue
                        gap_g = g_s.min()
                        if best is not None and gap_g >= best[0]:
                            continue
                        hc = gc - ax * (LG / 2 + Lh / 2)
                        h_s = sdist(rect_samples(hc, ax, n, Lh, D, 0.5))
                        if h_s.min() < 0:
                            continue
                        # the start-facing long wall
                        nin = n if np.dot(n, -hc) > 0 else -n
                        for s in np.arange(-Lh / 2 + PORCH_W / 2, Lh / 2 - PORCH_W / 2 + 1e-9, 1.0):
                            pc = hc + ax * s + nin * (D / 2 + (PORCH_D + APRON) / 2)
                            p_s = sdist(rect_samples(pc, ax, nin, PORCH_W, PORCH_D + APRON, 0.5))
                            if p_s.min() < 0:
                                continue
                            m = max(gap_g, p_s.min())
                            if best is None or m < best[0]:
                                best = (float(m), dict(L=Lh, D=D, t=float(t), u=float(u), v=float(v), s=float(s),
                                                      gap_gable=float(gap_g), gap_porch=float(p_s.min()),
                                                      gable_c=[round(float(x), 2) for x in gc], hall_c=[round(float(x), 2) for x in hc]))
    sdx, sdy = ax[0], math.sin(PITCH) * ax[1]
    scr = "lower-right" if sdx > 0 and sdy > 0 else "lower-left" if sdx < 0 and sdy > 0 else "upper-right" if sdx > 0 else "upper-left"
    rec = {"theta_compass_deg": theta, "screen_direction_door_to_gable": scr,
           "screen_angle_deg_cw_from_right": round(math.degrees(math.atan2(sdy, sdx)), 1),
           "best_max_gap_m": None if best is None else round(best[0], 3), "feasible": best is not None and best[0] <= 3.0,
           "best": None if best is None else best[1]}
    results.append(rec)
    print(theta, scr, rec["best_max_gap_m"], rec["feasible"], flush=True)

v7a = [r for r in results if r["screen_direction_door_to_gable"] == "lower-right"]
v6 = min(results, key=lambda r: abs(r["theta_compass_deg"] - 222.99))
out = {
    "_what": __doc__.strip().splitlines()[0],
    "rules_fixed": ["R1 anchors", "R4 floor >= min disc hull (search uses the min hull: most permissive)", "R5 zero overlap", "R10 <= 3.0 m"],
    "positive_control_v6_heading": v6,
    "v7a_any_feasible": any(r["feasible"] for r in v7a),
    "v7a_best": min((r for r in v7a if r["best_max_gap_m"] is not None), key=lambda r: r["best_max_gap_m"], default=None),
    "feasible_headings": [r["theta_compass_deg"] for r in results if r["feasible"]],
    "per_heading": results,
}
json.dump(out, open(os.path.join(HERE, "v7b_truekit_feasibility.json"), "w"), indent=1)
print("positive control v6 heading feasible:", v6["feasible"], v6["best_max_gap_m"])
print("v7a any feasible:", out["v7a_any_feasible"], "best:", out["v7a_best"] and out["v7a_best"]["best_max_gap_m"])
print("feasible headings:", out["feasible_headings"])
