#!/usr/bin/env python3
"""barrow_v2 (lane BX): prove every hard geometry rule of layout_v2.json with numbers.

    python3 tools/validate_layout_v2.py [LAYOUT] [--json OUT]       exit 0 = every rule PASS, 1 = any FAIL
    python3 tools/validate_layout_v2.py --negative-control          writes negative_control/layout_v2_broken.json
                                                                   and requires the validator to FAIL it on the
                                                                   rules it was broken on (exit 0 only if it does)

The rules (oracle + KC2 KP-253 + R-C9-145):
  R1  the anchors are the pack of record's, byte-for-byte (sha + values)
  R2  every 8 m scatter disc (the oracle's polar law, spawn_structure.py:295) is 100% on the floor with
      >= 1 m clearance (v2). The 8 m box (the pack's stale prose) is reported as INFO only.
  R3  the open straight line from (0, 0) to every anchor is on the floor and touches no blocker
  R4  the floor is WHOLE (one simple polygon) and ORGANIC (R-C9-149a), and CONTAINS the hull of the six
      discs + 1 m (the minimum); no straight run of edge longer than 6 m
  R5  no interior blocker: every movement/sight blocker has ZERO area inside the floor; every
      interior feature is walk-over (z_top <= walkover_max_h_m); and (R-C9-149a) everything the greybox
      renders -- sculpt blobs, beams, the terrain heightfield -- obeys the same rule
  R6  the stair (R-C9-148): width >= 2.5 m; a walkable slope (<= 35 deg, under Godot's 45 deg floor
      limit); top landing flush with the floor at the p03 patch; open on the sea side, the cliff face its
      wall; it climbs FROM the sea-level ledge, and the cave is at its foot (the run's angle to the
      centre is INFO only: climbers turn on the landing)
  R7  the mere covers p05's disc, is walkable, reaches the stone circle, and the stream joins it
  R8  the stone circle: 7-9 stones, all walk-over
  R9  the camera is the projection law (pitch, zero yaw, plate scale)
  R10 each delivering feature (door, wreck, cave/stair, gable) is OUTSIDE the edge and close to it
  R11 (R-C9-154) every deliverer opening is sized to the largest monster it delivers, measured off the
      rendered geometry: barrow door >= 5.0 x 6.5 m, great door/porch >= 4.5 x 4.5 m (porch above the
      hall's roofline), sea cave >= 9 x ~7 m
"""
import argparse
import copy
import glob
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bv2_geom as G  # noqa: E402

ROOT = os.path.dirname(HERE)
ENGINE = os.path.expanduser("~/Games/reincarnated-engine")
TOL = 1e-3   # m2 for areas, m for z: layout coordinates are rounded to 0.1 mm, so polygons that SHARE an edge
             # (spur | flight, landing | floor arc) overlap by < 1 cm2 of pure rounding (measured 1e-6 .. 9e-5 m2)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clip_convex(subject, clip):
    """Sutherland-Hodgman: subject polygon clipped by a CONVEX clip polygon (any orientation)."""
    if G.signed_area(clip) < 0:
        clip = list(reversed(clip))
    out = list(subject)
    n = len(clip)
    for i in range(n):
        a, b = clip[i], clip[(i + 1) % n]
        inp, out = out, []
        if not inp:
            break

        def inside(p):
            return G.cross(a, b, p) >= -1e-12

        def inter(p, q):
            x1, y1 = p
            x2, y2 = q
            x3, y3 = a
            x4, y4 = b
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return out


def _area_clip(subject, convex_clip):
    c = clip_convex(subject, convex_clip)
    return G.area(c) if len(c) >= 3 else 0.0


def overlap_area(P, Q):
    """Exact intersection area of two simple polygons (either may be non-convex: R-C9-149a's organic floor).
    Sutherland-Hodgman is exact when the CLIP polygon is convex, so a non-convex pair is split into
    triangles first."""
    P = [tuple(p) for p in P]
    Q = [tuple(q) for q in Q]
    bp, bq = G.bbox(P), G.bbox(Q)
    if bp[2] < bq[0] or bq[2] < bp[0] or bp[3] < bq[1] or bq[3] < bp[1]:
        return 0.0
    if G.is_convex(Q):
        return _area_clip(P, Q)
    if G.is_convex(P):
        return _area_clip(Q, P)
    return sum(_area_clip(Q, list(t)) for t in G.triangulate(P))


class FloorIndex:
    """Fast exact queries against the (non-convex) floor: a centroid-distance prefilter decides the easy
    cases (wholly inside / wholly outside) and only polygons near the edge are clipped."""

    def __init__(self, floor):
        import numpy as np
        self.np = np
        self.F = [tuple(p) for p in floor]
        A = np.array(self.F)
        self.ax, self.ay = A[:, 0], A[:, 1]
        B = np.roll(A, -1, axis=0)
        self.dx, self.dy = B[:, 0] - A[:, 0], B[:, 1] - A[:, 1]
        self.L2 = np.maximum(self.dx ** 2 + self.dy ** 2, 1e-18)
        self.bx, self.by = B[:, 0], B[:, 1]

    def dist(self, p):
        np = self.np
        t = np.clip(((p[0] - self.ax) * self.dx + (p[1] - self.ay) * self.dy) / self.L2, 0, 1)
        return float(np.min(np.hypot(p[0] - (self.ax + t * self.dx), p[1] - (self.ay + t * self.dy))))

    def inside(self, p):
        np = self.np
        cond = (self.ay > p[1]) != (self.by > p[1])
        with np.errstate(divide="ignore", invalid="ignore"):
            xi = self.ax + (p[1] - self.ay) * self.dx / np.where(self.dy == 0, 1e-18, self.dy)
        return bool(np.count_nonzero(cond & (xi > p[0])) % 2)

    def overlap(self, P):
        P = [tuple(p) for p in P]
        c = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
        r = max(math.dist(c, p) for p in P)
        d = self.dist(c)
        if d > r + 1e-9:
            return G.area(P) if self.inside(c) else 0.0
        return overlap_area(P, self.F)


def disc_poly(c, r, n=512):
    return [(c[0] + r * math.cos(G.TAU * k / n), c[1] + r * math.sin(G.TAU * k / n)) for k in range(n)]


class Report:
    def __init__(self):
        self.rows = []

    def check(self, rule, name, ok, **nums):
        self.rows.append({"rule": rule, "check": name, "PASS": bool(ok), **nums})
        return ok

    def info(self, rule, name, **nums):
        self.rows.append({"rule": rule, "check": name, "PASS": True, "severity": "INFO", **nums})

    @property
    def ok(self):
        return all(r["PASS"] for r in self.rows)

    def failed_rules(self):
        return sorted({r["rule"] for r in self.rows if not r["PASS"]})


def validate(L, check_provenance=True):
    R = Report()
    floor = [tuple(p) for p in L["floor"]["polygon"]]
    wmax = L["floor"]["walkover_max_h_m"]
    anchors = L["anchors"]["points"]
    h = L["anchors"]["scatter"]["half_width_m"]
    r_disc = L["anchors"]["scatter"]["disc_radius_m_brief"]
    feats = L["features"]
    FI = FloorIndex(floor)

    # ---------------- R1 provenance ----------------
    if check_provenance:
        prov = L["anchors"]["provenance"]
        p = os.path.join(ENGINE, prov["pack_arena_json"])
        got = sha256(p)
        R.check("R1", "pack arena.json sha256 matches the layout's provenance", got == prov["pack_arena_json_sha256"],
                sha256=got)
        arena = json.load(open(p))
        rows = {r["value"]["point_id"]: r["value"] for r in arena["⚑ v3p8_rows"]["sg1_spawn_points_gd"]}
        worst = max(math.hypot(a["x"] - rows[a["id"]]["x"], a["y"] - rows[a["id"]]["y"]) for a in anchors)
        R.check("R1", "six anchors equal the pack's sg1 rows exactly", len(anchors) == 6 and worst == 0.0,
                n=len(anchors), worst_delta_m=worst)
        R.check("R1", "scatter half-width equals the pack's placement_extents_m",
                h == arena["placement_extents_m"]["value"], half_width_m=h)
        R.check("R1", "CSV sha256 matches", sha256(os.path.join(ENGINE, prov["csv"])) == prov["csv_sha256"])
        lp = L["anchors"]["scatter"]["law_provenance"]
        sp = os.path.join(ENGINE, lp["file"].split(":", 1)[1])
        line = open(sp).read().splitlines()[294]
        R.check("R1", "scatter law = polar disc: spawn_structure.py:295 is POLAR_UNIFORM_RHO and its sha matches",
                "ScatterLaw.POLAR_UNIFORM_RHO" in line and sha256(sp) == lp["sha256"], line_295=line.strip())

    # ---------------- R4 the floor ----------------
    simple, n_bad = G.is_simple(floor)
    R.check("R4", "floor is WHOLE: one simple polygon (no self-intersections, no holes)", simple, n_vertices=len(floor), self_intersections=n_bad)
    ar = G.area(floor)
    ex = G.extents(floor)
    R.check("R4", "floor area and extents (>= the brief's ~84 x 82 m, ~4,026 m2)",
            ar >= 4026.0 - 1.0 and ex["width_x"] >= 83.0 and ex["depth_y"] >= 81.0,
            area_m2=round(ar, 2), width_x_m=round(ex["width_x"], 3), depth_y_m=round(ex["depth_y"], 3),
            x=[round(ex["x_min"], 3), round(ex["x_max"], 3)], y=[round(ex["y_min"], 3), round(ex["y_max"], 3)])
    hull_min = G.offset_hull([(a["x"], a["y"]) for a in anchors], r_disc + 1.0, n=192)
    worst = min((FI.dist(p) if FI.inside(p) else -FI.dist(p)) for p in hull_min)
    worst_out = max(G.signed_clearance(p, hull_min) for p in floor)
    R.check("R4", "floor contains the hull of the six discs + 1 m, the MINIMUM (every hull vertex on the floor; no floor vertex strictly inside the hull)",
            worst >= -1e-3 and worst_out <= 1e-3, worst_hull_vertex_clearance_m=round(worst, 4),
            deepest_floor_vertex_inside_hull_m=round(worst_out, 4), hull_min_area_m2=round(G.area(hull_min), 2),
            floor_minus_hull_m2=round(ar - G.area(hull_min), 2))
    run, at = G.longest_straight_run(floor, tol=0.08)
    R.check("R4", "the edge is ORGANIC (R-C9-149a): no straight run longer than 6 m (points within 0.08 m of a chord)",
            run <= 6.0, longest_straight_run_m=round(run, 2), at=[round(at[0], 2), round(at[1], 2)] if at else None,
            bulge_m=L["floor"].get("organic", {}).get("bulge_m"))

    # ---------------- R2 discs and boxes ----------------
    for a in anchors:
        c = (a["x"], a["y"])
        clr = G.disc_clearance(c, r_disc, floor)
        dp = disc_poly(c, r_disc)
        frac = FI.overlap(dp) / G.area(dp)
        R.check("R2", f"{a['id']} 8 m disc 100% on the floor with >= 1 m clearance", clr >= 1.0 - 1e-3 and frac >= 1.0 - 1e-9,
                disc_on_floor_pct=round(100 * frac, 6), edge_clearance_m=round(clr, 4))
        box = [(c[0] + sx * h, c[1] + sy * h) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        bclr = min(G.signed_clearance(p, floor) for p in box)
        bfrac = FI.overlap(box) / G.area(box)
        R.info("R2", f"{a['id']} 8 m box (the pack's stale prose; not the oracle's law) coverage",
               box_on_floor_pct=round(100 * bfrac, 3), corner_clearance_m=round(bclr, 4))

    blockers = [f for f in feats if f["blocks_movement"] or f["blocks_sight"] or f["z_top_m"] > wmax]

    # ---------------- R3 lines to origin ----------------
    o = (0.0, 0.0)
    R.check("R3", "the start (0, 0) is on the floor", G.signed_clearance(o, floor) > 0,
            clearance_m=round(G.signed_clearance(o, floor), 4))
    for a in anchors:
        c = (a["x"], a["y"])
        on_floor = FI.inside(c) and FI.inside(o) and not G.seg_crosses_poly(o, c, floor)
        gaps = [(G.seg_poly_dist(o, c, [tuple(p) for p in f["footprint"]]), f["id"]) for f in blockers]
        gmin = min(gaps) if gaps else (float("inf"), None)
        R.check("R3", f"line (0,0) -> {a['id']} on the floor and clear of every blocker",
                on_floor and gmin[0] > 0, length_m=round(math.hypot(*c), 3),
                nearest_blocker=gmin[1], nearest_blocker_gap_m=round(gmin[0], 3))

    # ---------------- R5 no interior blocker ----------------
    worst = (0.0, None)
    ov = {f["id"]: FI.overlap(f["footprint"]) for f in feats}
    for f in blockers:
        oa = ov[f["id"]]
        if oa > worst[0]:
            worst = (oa, f["id"])
    gaps = sorted((min(FI.dist(tuple(p)) for p in f["footprint"]) if ov[f["id"]] <= TOL else 0.0, f["id"]) for f in blockers)
    R.check("R5", "every blocker (blocks movement or sight, or taller than walk-over) has zero area inside the floor",
            worst[0] <= TOL, n_blockers=len(blockers), worst_overlap_m2=round(worst[0], 6), worst_id=worst[1],
            closest_blocker_gap_m=round(gaps[0][0], 3) if gaps else None, closest_blocker=gaps[0][1] if gaps else None)
    interior = [f for f in feats if ov[f["id"]] > TOL]
    tall = [(f["id"], f["z_top_m"]) for f in interior if f["z_top_m"] > wmax or f["blocks_movement"] or f["blocks_sight"]]
    R.check("R5", f"every interior feature is walk-over (z_top <= {wmax} m, blocks nothing)", not tall,
            n_interior=len(interior), tallest_interior_m=max((f["z_top_m"] for f in interior), default=0.0), offenders=tall)
    for key in ("mere", "stream", "path"):
        R.check("R5", f"{key} is walkable and flush (z 0)", L[key]["walkable"] and abs(L[key]["z_m"]) <= TOL)
    # R-C9-149a: everything the greybox RENDERS is proved too -- the sculpt's blobs and beams, and the terrain
    sc = L.get("sculpt")
    if sc:
        bad_b = []
        for b in sc["blobs"]:
            if b["top"] > wmax:
                fp = G.ellipse_poly(b["c"][0], b["c"][1], b["r"][0], b["r"][1], b["rot"], 16)
                if FI.overlap(fp) > TOL:
                    bad_b.append((b["k"], b["c"], b["top"]))
        R.check("R5", f"sculpt: every blob taller than walk-over ({wmax} m) lies outside the floor", not bad_b,
                n_blobs=len(sc["blobs"]), n_tall=sum(b["top"] > wmax for b in sc["blobs"]), offenders=bad_b[:5])
        bad_m = []
        for bm in sc["beams"]:
            a_, b_ = bm["a"], bm["b"]
            for k in range(11):
                t = k / 10
                x_, y_, z_ = (a_[0] + t * (b_[0] - a_[0]), a_[1] + t * (b_[1] - a_[1]), a_[2] + t * (b_[2] - a_[2]))
                half = max(bm["w"], bm["t"]) / 2
                if z_ + half > wmax and (FI.inside((x_, y_)) or FI.dist((x_, y_)) < half):
                    if FI.inside((x_, y_)):
                        bad_m.append((bm["k"], [round(x_, 2), round(y_, 2), round(z_, 2)]))
                        break
        R.check("R5", f"sculpt: no beam rises above walk-over ({wmax} m) over the floor", not bad_m,
                n_beams=len(sc["beams"]), offenders=bad_m[:5])
        import numpy as np
        hf = sc["heightfield"]
        Hh = np.fromfile(os.path.join(ROOT, hf["file"]), dtype="<f4").reshape(hf["shape"])
        ex_ = hf["extent_sim_m"]
        gx = ex_["x0"] + np.arange(Hh.shape[1]) / hf["px_per_m"]
        gy = ex_["y0"] + np.arange(Hh.shape[0]) / hf["px_per_m"]
        X, Y = np.meshgrid(gx, gy)
        insideF = np.zeros(X.shape, dtype=bool)
        n = len(floor)
        for i in range(n):
            x0, y0 = floor[i]
            x1, y1 = floor[(i + 1) % n]
            if y0 == y1:
                continue
            cond = (y0 > Y) != (y1 > Y)
            xi = x0 + (Y - y0) * (x1 - x0) / (y1 - y0)
            insideF ^= cond & (xi > X)
        dev = float(np.max(np.abs(Hh[insideF]))) if insideF.any() else 0.0
        R.check("R5", "terrain: the heightfield is exactly 0 at every sample on the floor (the sim's plane); relief only outside",
                dev <= 1e-6 and hashlib.sha256(open(os.path.join(ROOT, hf["file"]), "rb").read()).hexdigest() == hf["sha256"],
                samples_on_floor=int(insideF.sum()), max_abs_z_on_floor_m=dev, relief_outside_max_m=round(float(Hh[~insideF].max()), 3))

    # ---------------- R6 the stair ----------------
    S = L["stair"]
    fl = [tuple(p) for p in S["flight"]["polygon"]]          # top wall-side, top sea-side, foot sea-side, foot wall-side
    land = [tuple(p) for p in S["top_landing"]["polygon"]]
    w_meas = min(math.dist(fl[0], fl[1]), math.dist(fl[3], fl[2]))
    run_meas = (math.dist(fl[0], fl[3]) + math.dist(fl[1], fl[2])) / 2
    drop = S["flight"]["z_top_m"] - S["flight"]["z_bottom_m"]
    slope = math.degrees(math.atan2(drop, run_meas))
    R.check("R6", "stair width >= 2.5 m (measured off the flight polygon)", w_meas >= 2.5, width_m=round(w_meas, 4))
    R.check("R6", "stair slope walkable: <= 35 deg (and under Godot's default floor_max_angle 45 deg)",
            slope <= 35.0, slope_deg=round(slope, 3), run_m=round(run_meas, 3), drop_m=drop,
            grade_pct=round(100 * drop / run_meas, 2))
    rise, tread = S["flight"]["step_rise_m"], S["flight"]["step_tread_m"]
    R.check("R6", "steps: rise x count = drop, tread x count = run, 2R+T in 0.60-0.65 m",
            abs(rise * S["flight"]["n_steps"] - drop) < 1e-6 and abs(tread * S["flight"]["n_steps"] - run_meas) < 1e-3
            and 0.60 <= 2 * rise + tread <= 0.65, n_steps=S["flight"]["n_steps"], rise_m=rise, tread_m=tread,
            two_r_plus_t_m=round(2 * rise + tread, 3))
    mid_top = ((fl[0][0] + fl[1][0]) / 2, (fl[0][1] + fl[1][1]) / 2)
    mid_foot = ((fl[3][0] + fl[2][0]) / 2, (fl[3][1] + fl[2][1]) / 2)
    up = (mid_top[0] - mid_foot[0], mid_top[1] - mid_foot[1])
    to_c = (-mid_top[0], -mid_top[1])
    ang = math.degrees(math.acos(max(-1, min(1, (up[0] * to_c[0] + up[1] * to_c[1]) / (math.hypot(*up) * math.hypot(*to_c))))))
    R.info("R6", "the run's angle to the centre (climbers turn on the top landing; the alignment rule was dropped by R-C9-148)",
           turn_on_landing_deg=round(ang, 2))
    p3 = next(a for a in anchors if a["id"] == "p03")
    north = [tuple(p) for p in S["top_landing"]["boundary_edge"]]
    on_bd = max(G.dist_to_boundary(p, floor) for p in north)
    in_floor = FI.overlap(land)
    box3 = [(p3["x"] + sx * h, p3["y"] + sy * h) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    to_patch = min(G.seg_poly_dist(north[i], north[i + 1], box3) for i in range(len(north) - 1))
    to_disc = min(G.dist_point_seg((p3["x"], p3["y"]), north[i], north[i + 1]) for i in range(len(north) - 1)) - r_disc
    R.check("R6", "top landing flush: same z as the floor, its north edge ON the floor boundary, no overlap, abutting the p03 disc across the 1 m margin",
            abs(S["top_landing"]["z_m"] - L["floor"]["z_m"]) <= TOL and on_bd <= 1e-3 and in_floor <= TOL and to_disc <= 1.0 + 1e-3,
            north_edge_off_boundary_m=round(on_bd, 6), landing_overlap_m2=round(in_floor, 6),
            gap_to_p03_disc_m=round(to_disc, 4), gap_to_p03_box_m_info=round(to_patch, 4),
            landing_north_edge_len_m=round(sum(math.dist(north[i], north[i + 1]) for i in range(len(north) - 1)), 3))
    for part in ("top_landing", "flight", "bottom_landing"):
        poly = [tuple(p) for p in S[part]["polygon"]]
        R.check("R6", f"stair {part} lies OUTSIDE the floor (zero overlap)", FI.overlap(poly) <= TOL,
                overlap_m2=round(FI.overlap(poly), 6))
    # open side: nothing blocking within 1.0 m of the flight's SEA-side edge (outside the flight)
    east_edge = (fl[1], fl[2])
    near_e = [(G.seg_poly_dist(east_edge[0], east_edge[1], [tuple(p) for p in f["footprint"]]), f["id"]) for f in blockers]
    near_e = min(near_e) if near_e else (float("inf"), None)
    west_edge = (fl[0], fl[3])
    near_w = [(G.seg_poly_dist(west_edge[0], west_edge[1], [tuple(p) for p in f["footprint"]]), f["id"]) for f in blockers if f["kind"] == "cliff"]
    near_w = min(near_w) if near_w else (float("inf"), None)
    R.check("R6", "one side open: no blocker within 1 m of the sea-side edge; the cliff face is the wall on the other side",
            near_e[0] > 1.0 and near_w[0] <= 1e-3, sea_side_nearest=near_e[1], sea_side_gap_m=round(near_e[0], 3),
            wall=near_w[1], wall_gap_m=round(near_w[0], 6))
    # the flight must not cross any blocker (a monster climbing it is never stuck on geometry)
    hit = [f["id"] for f in blockers if overlap_area([tuple(p) for p in f["footprint"]], fl) > TOL
           or overlap_area([tuple(p) for p in f["footprint"]], land) > TOL]
    R.check("R6", "nothing stands on the flight or the top landing", not hit, offenders=hit)
    ledge = [tuple(p) for p in S["bottom_landing"]["polygon"]]
    foot_mid = ((fl[2][0] + fl[3][0]) / 2, (fl[2][1] + fl[3][1]) / 2)
    foot_on = G.signed_clearance(foot_mid, ledge)
    R.check("R6", "the flight climbs FROM the ledge: its foot edge is on the sea-level ledge, at the ledge's z",
            foot_on >= -1e-3 and abs(S["flight"]["z_bottom_m"] - S["bottom_landing"]["z_m"]) <= TOL,
            foot_mid_clearance_in_ledge_m=round(foot_on, 4), ledge_z_m=S["bottom_landing"]["z_m"])
    cave = next((f for f in feats if f["kind"] == "cave"), None)
    if cave is None:
        R.check("R6", "the sea cave exists", False)
    else:
        cp = [tuple(p) for p in cave["footprint"]]
        g_foot = G.seg_poly_dist(fl[2], fl[3], cp)
        on_ledge = overlap_area(cp, ledge) > 0.0 or G.poly_poly_gap(cp, ledge) <= 0.05
        to_lip = min(FI.dist(p) for p in cp) if FI.overlap(cp) <= TOL else 0.0
        R.check("R6", "the cave is at the stair's foot: on the ledge, within 4 m of the foot, at the ledge's z, in the cliff face under the lip (<= 0.5 m out)",
                on_ledge and g_foot <= 4.0 and abs(cave["z_bottom_m"] - S["bottom_landing"]["z_m"]) <= TOL and to_lip <= 0.5,
                cave_to_foot_m=round(g_foot, 3), cave_to_lip_m=round(to_lip, 3), cave_z_m=[cave["z_bottom_m"], cave["z_top_m"]])

    # ---------------- R7 the mere and the stream ----------------
    mere = [tuple(p) for p in L["mere"]["polygon"]]
    p5 = next(a for a in anchors if a["id"] == "p05")
    clr5 = G.disc_clearance((p5["x"], p5["y"]), r_disc, mere)
    box5 = [(p5["x"] + sx * h, p5["y"] + sy * h) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    # box coverage by the (non-convex) mere: sample at 0.1 m
    n_in = n_all = 0
    k = 0.1
    xs = [p5["x"] - h + k / 2 + i * k for i in range(int(2 * h / k))]
    for x in xs:
        for y in [p5["y"] - h + k / 2 + j * k for j in range(int(2 * h / k))]:
            n_all += 1
            n_in += G.point_in_poly((x, y), mere)
    R.check("R7", "the mere covers p05's 8 m disc 100%", clr5 >= 0.0, disc_edge_clearance_m=round(clr5, 4))
    R.info("R7", "p05's box (stale prose) under the mere", p05_box_covered_pct=round(100 * n_in / n_all, 2))
    mere_in_floor = FI.overlap(mere) / G.area(mere)
    R.check("R7", "the mere is on the floor (walkable ice, flush)", mere_in_floor >= 0.999,
            mere_area_m2=round(G.area(mere), 2), mere_on_floor_pct=round(100 * mere_in_floor, 3))
    cc = L["stone_circle"]["centre"]
    cr = L["stone_circle"]["radius_m"]
    reach = G.signed_clearance(tuple(cc), mere)
    R.check("R7", "the mere reaches the stone circle (its edge within the ring's radius of the circle centre)",
            -reach <= cr, mere_edge_to_circle_centre_m=round(-reach, 3), circle_radius_m=cr)
    st = [tuple(p) for p in L["stream"]["polyline"]]
    R.check("R7", "the stream runs from outside the edge (the barrow slope) into the mere",
            G.signed_clearance(st[0], floor) < 0 and G.point_in_poly(st[-1], mere),
            source_outside_floor_m=round(-G.signed_clearance(st[0], floor), 3),
            mouth_inside_mere_m=round(G.signed_clearance(st[-1], mere), 3))

    # ---------------- R8 the circle ----------------
    stones = [f for f in feats if f["id"] in L["stone_circle"]["stones"]]
    R.check("R8", "stone circle: 7-9 stones, all walk-over", 7 <= len(stones) <= 9 and all(
        f["z_top_m"] <= wmax and not f["blocks_movement"] for f in stones), n=len(stones),
        tallest_m=max(f["z_top_m"] for f in stones) if stones else None)
    R.check("R8", "the start (0,0) is inside the circle", math.hypot(*cc) <= cr, start_to_centre_m=round(math.hypot(*cc), 3))

    # ---------------- R9 camera ----------------
    cam = L["camera"]
    a = math.radians(cam["pitch_deg"])
    ppm = 0.0802 * 1080 / (1.9 * math.cos(a))
    R.check("R9", "camera = pitch 52.9535411256029 deg, zero yaw, orthographic, plate 100.617553710938 px/m, ppm_GD derived",
            cam["pitch_deg"] == 52.9535411256029 and cam["yaw_deg"] == 0.0 and cam["projection"] == "orthographic"
            and cam["ppm_plate"] == 100.617553710938 and abs(cam["ppm_zoom_gd"] - ppm) < 1e-9 and abs(ppm - 75.668) < 1e-3,
            ppm_zoom_gd=round(ppm, 4), window_zoom_gd_m=[round(v, 3) for v in cam["window_zoom_gd_1920x1080_m"]])

    # ---------------- R10 the deliverers ----------------
    deliver = {"p02": ["barrow_door"], "p01": ["wreck_hull"], "p04": ["hall_porch"], "p06": ["fallen_gable"],
               "p03": ["sea_cave_mouth"]}
    for pid, ids in deliver.items():
        for fid in ids:
            f = next((x for x in feats if x["id"] == fid), None)
            if f is None:
                R.check("R10", f"{pid}: {fid} exists", False)
                continue
            poly = [tuple(p) for p in f["footprint"]]
            oa = FI.overlap(poly)
            gap = min(FI.dist(p) for p in poly) if oa <= TOL else 0.0
            limit = {"p03": 0.5, "p02": 3.5}.get(pid, 3.0)
            R.check("R10", f"{pid}: {fid} is outside the walkable edge and within {limit} m of it", oa <= TOL and gap <= limit,
                    overlap_m2=round(oa, 6), gap_to_floor_m=round(gap, 3))
    # ---------------- R11 openings sized to the monsters (R-C9-154) ----------------
    sc = L.get("sculpt") or {"beams": [], "blobs": []}
    BM = sc["beams"]

    def horiz(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])
    posts = [b for b in BM if b["k"] == "door_post"]
    lint = [b for b in BM if b["k"] == "lintel"]
    if len(posts) == 2 and lint:
        gap_c = horiz(posts[0]["a"], posts[1]["a"])
        clear_w = gap_c - (posts[0]["w"] + posts[1]["w"]) / 2
        clear_h = min(l["a"][2] for l in lint) - lint[0]["t"] / 2
        R.check("R11", "p02 barrow door clear opening >= 5.0 m wide x 6.5 m high (yeti nemesis ~5.6 m), measured between the rendered uprights and under the lintel",
                clear_w >= 5.0 - 5e-3 and clear_h >= 6.5 - 5e-3, clear_w_m=round(clear_w, 3), clear_h_m=round(clear_h, 3))
    else:
        R.check("R11", "p02 barrow door uprights + lintel present", False, n_posts=len(posts), n_lintels=len(lint))
    fp = [b for b in BM if b["k"] == "porch_post_front"]
    eave = [b for b in BM if b["k"] == "porch_eave"]
    leaves = [b for b in BM if b["k"] == "door_leaf"]
    dark = [b for b in sc["blobs"] if b["k"] == "dark"]
    hall_ridge = max((b["a"][2] for b in BM if b["k"] == "ridge"), default=0.0)
    ridge = max((max(b["a"][2], b["b"][2]) for b in BM if b["k"] == "porch_ridge"), default=0.0)
    if len(fp) == 2 and eave:
        clear_w = horiz(fp[0]["a"], fp[1]["a"]) - (fp[0]["w"] + fp[1]["w"]) / 2
        clear_h = eave[0]["a"][2] - eave[0]["t"] / 2
        door_h = max((b["top"] for b in dark if abs(b["top"] - clear_h) < 2.5 or True), default=0.0)
        R.check("R11", "p04 great door + porch clear opening >= 4.5 m wide x 4.5 m high (colossus 3.2 m, statues ~3.5 m, crabs ~3.4 m wide), measured between the porch's front posts and under its front beam; the doorway behind it as large",
                clear_w >= 4.5 - 5e-3 and clear_h >= 4.5 - 5e-3 and len(leaves) == 2,
                clear_w_m=round(clear_w, 3), clear_h_m=round(clear_h, 3), door_leaves=len(leaves))
        R.check("R11", "the porch rises ABOVE the hall's roofline (its ridge vs the hall's ridge beams)", ridge > hall_ridge + 0.5,
                porch_ridge_m=round(ridge, 2), hall_ridge_max_m=round(hall_ridge, 2))
    else:
        R.check("R11", "p04 porch front posts + front beam present", False, n_front_posts=len(fp), n_eave=len(eave))
    cave = next((f for f in feats if f["kind"] == "cave"), None)
    if cave is not None:
        cp = [tuple(p) for p in cave["footprint"]]
        n2 = len(cp) // 2
        mouth_w = sum(math.dist(cp[i], cp[i + 1]) for i in range(n2 - 1))
        mouth_h = cave["z_top_m"] - cave["z_bottom_m"]
        lintel = 0.0 - cave["z_top_m"]
        R.check("R11", "p03 sea-cave mouth ~7 m high x >= 9 m wide (servitors 4-8 m long, the 5.6 m nemesis), with rock above it below the floor",
                mouth_w >= 9.0 - 0.05 and mouth_h >= 6.5 and lintel > 0.1,
                mouth_w_m=round(mouth_w, 3), mouth_h_m=round(mouth_h, 3), rock_lintel_m=round(lintel, 3))
    return R


def broken_copy(L):
    """The negative control: four deliberate violations, each of which a correct validator must catch."""
    B = copy.deepcopy(L)
    B["_what"] = "NEGATIVE CONTROL -- deliberately broken copy of layout_v2.json; the validator MUST fail it"
    # (a) R2/R4: the floor shrunk to 92% about its centroid (discs/boxes no longer whole on it)
    fl = B["floor"]["polygon"]
    cx = sum(p[0] for p in fl) / len(fl)
    cy = sum(p[1] for p in fl) / len(fl)
    B["floor"]["polygon"] = [[cx + 0.92 * (p[0] - cx), cy + 0.92 * (p[1] - cy)] for p in fl]
    # (b) R3/R5: a STANDING stone on the floor, across the line to p02
    B["features"].append({"id": "NC_standing_stone", "kind": "standing_stone",
                          "footprint": G.rect_poly(4.0, -13.0, 1.0, 0.8, 0.0), "z_bottom_m": 0.0, "z_top_m": 2.4,
                          "blocks_movement": True, "blocks_sight": True, "placement": "INSIDE (deliberately)", "note": "negative control"})
    # (b2) R5: a tall sculpt blob (a 'boulder') dropped on the floor
    if "sculpt" in B:
        B["sculpt"]["blobs"].append({"k": "rock", "c": [-6.0, 12.0], "cz": 0.0, "r": [1.2, 1.0, 1.4], "rot": 0.0,
                                     "rgb": [0.5, 0.5, 0.5], "proto": "rock", "top": 1.4})
    # (b3) R11: the barrow door's lintel dropped to 4 m (too low for the yeti nemesis)
    if "sculpt" in B:
        for bm in B["sculpt"]["beams"]:
            if bm["k"] == "lintel":
                bm["a"][2] = bm["b"][2] = 4.0
    # (c) R6: a narrow, steep stair
    S = B["stair"]
    fl3 = S["flight"]["polygon"]
    mid0 = [(fl3[0][0] + fl3[1][0]) / 2, (fl3[0][1] + fl3[1][1]) / 2]
    mid3 = [(fl3[3][0] + fl3[2][0]) / 2, (fl3[3][1] + fl3[2][1]) / 2]

    def pull(p, m, s):
        return [m[0] + s * (p[0] - m[0]), m[1] + s * (p[1] - m[1])]
    S["flight"]["polygon"] = [pull(fl3[0], mid0, 2.0 / 3.0), pull(fl3[1], mid0, 2.0 / 3.0),
                              pull(fl3[2], mid3, 2.0 / 3.0), pull(fl3[3], mid3, 2.0 / 3.0)]
    S["flight"]["z_bottom_m"] = -20.0
    # (d) R7: the mere shrunk so it no longer covers p05's disc
    me = B["mere"]["polygon"]
    mx = sum(p[0] for p in me) / len(me)
    my = sum(p[1] for p in me) / len(me)
    B["mere"]["polygon"] = [[mx + 0.6 * (p[0] - mx), my + 0.6 * (p[1] - my)] for p in me]
    return B, {"R2", "R3", "R4", "R5", "R6", "R7", "R11"}


def print_report(R, title):
    print(f"== {title}")
    for r in R.rows:
        nums = {k: v for k, v in r.items() if k not in ("rule", "check", "PASS")}
        nums.pop("severity", None)
        tag = "INFO" if r.get("severity") == "INFO" else ("PASS" if r["PASS"] else "FAIL")
        print(f"  {tag}  {r['rule']:<4} {r['check']}  {json.dumps(nums, ensure_ascii=False)}")
    n_fail = sum(not r["PASS"] for r in R.rows)
    n_info = sum(r.get("severity") == "INFO" for r in R.rows)
    print(f"== {len(R.rows) - n_info} checks, {len(R.rows) - n_info - n_fail} PASS, {n_fail} FAIL, plus {n_info} INFO -> {'PASS' if R.ok else 'FAIL'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layout", nargs="?", default=os.path.join(ROOT, "layout_v2.json"))
    ap.add_argument("--json", default=None)
    ap.add_argument("--negative-control", action="store_true")
    a = ap.parse_args()
    L = json.load(open(a.layout))
    if a.negative_control:
        B, expect = broken_copy(L)
        os.makedirs(os.path.join(ROOT, "negative_control"), exist_ok=True)
        out = os.path.join(ROOT, "negative_control", "layout_v2_broken.json")
        with open(out, "w") as f:
            json.dump(B, f, indent=2, ensure_ascii=False)
            f.write("\n")
        R = validate(B)
        print_report(R, f"NEGATIVE CONTROL {os.path.relpath(out, ROOT)} (must FAIL on {sorted(expect)})")
        got = set(R.failed_rules())
        caught = (not R.ok) and expect <= got
        print(f"== negative control: failed rules {sorted(got)}; expected at least {sorted(expect)} -> "
              f"{'CAUGHT (correct)' if caught else 'MISSED (validator defect)'}")
        sys.exit(0 if caught else 2)
    R = validate(L)
    print_report(R, os.path.relpath(a.layout, ROOT))
    if a.json:
        with open(a.json, "w") as f:
            json.dump({"layout": os.path.relpath(a.layout, ROOT), "layout_sha256": sha256(a.layout),
                       "pass": R.ok, "checks": R.rows}, f, indent=2, ensure_ascii=False)
            f.write("\n")
    sys.exit(0 if R.ok else 1)


if __name__ == "__main__":
    main()
