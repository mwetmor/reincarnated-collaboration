#!/usr/bin/env python3
"""barrow_v2 (lane BX): prove every hard geometry rule of layout_v2.json with numbers.

    python3 tools/validate_layout_v2.py [LAYOUT] [--json OUT]       exit 0 = every rule PASS, 1 = any FAIL
    python3 tools/validate_layout_v2.py --negative-control          writes negative_control/layout_v2_broken.json
                                                                   and requires the validator to FAIL it on the
                                                                   rules it was broken on (exit 0 only if it does)

The rules (oracle + KC2 KP-253 + R-C9-145):
  R1  the anchors are the pack of record's, byte-for-byte (sha + values)
  R2  every 8 m scatter disc is 100% on the floor (and every 8 m scatter BOX, the pack's model)
  R3  the open straight line from (0, 0) to every anchor is on the floor and touches no blocker
  R4  the floor is WHOLE and convex, and contains the hull of the six discs + 1 m
  R5  no interior blocker: every movement/sight blocker has ZERO area inside the floor; every
      interior feature is walk-over (z_top <= walkover_max_h_m)
  R6  the stair: width >= 2.5 m; a walkable slope (<= 30 deg, under Godot's 45 deg floor limit);
      run aligned to the centre; top landing flush with the floor at the p03 patch; one side open
  R7  the mere covers p05's disc, is walkable, reaches the stone circle, and the stream joins it
  R8  the stone circle: 7-9 stones, all walk-over
  R9  the camera is the projection law (pitch, zero yaw, plate scale)
  R10 each delivering feature (door, wreck, cave/stair, gable) is OUTSIDE the edge and close to it
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
TOL = 1e-6


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


def overlap_area(poly, convex):
    c = clip_convex(poly, convex)
    return G.area(c) if len(c) >= 3 else 0.0


def disc_poly(c, r, n=512):
    return [(c[0] + r * math.cos(G.TAU * k / n), c[1] + r * math.sin(G.TAU * k / n)) for k in range(n)]


class Report:
    def __init__(self):
        self.rows = []

    def check(self, rule, name, ok, **nums):
        self.rows.append({"rule": rule, "check": name, "PASS": bool(ok), **nums})
        return ok

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

    # ---------------- R4 the floor ----------------
    R.check("R4", "floor polygon is convex", G.is_convex(floor), n_vertices=len(floor))
    ar = G.area(floor)
    ex = G.extents(floor)
    R.check("R4", "floor area and extents (>= the brief's ~84 x 82 m, ~4,026 m2)",
            ar >= 4026.0 - 1.0 and ex["width_x"] >= 83.0 and ex["depth_y"] >= 81.0,
            area_m2=round(ar, 2), width_x_m=round(ex["width_x"], 3), depth_y_m=round(ex["depth_y"], 3),
            x=[round(ex["x_min"], 3), round(ex["x_max"], 3)], y=[round(ex["y_min"], 3), round(ex["y_max"], 3)])
    hull_min = G.offset_hull([(a["x"], a["y"]) for a in anchors], r_disc + 1.0, n=192)
    worst = min(G.signed_clearance(p, floor) for p in hull_min)
    R.check("R4", "floor contains the hull of the six discs + 1 m (every vertex of that hull inside)",
            worst >= -1e-3, worst_vertex_clearance_m=round(worst, 4), hull_min_area_m2=round(G.area(hull_min), 2))

    # ---------------- R2 discs and boxes ----------------
    for a in anchors:
        c = (a["x"], a["y"])
        clr = G.disc_clearance(c, r_disc, floor)
        dp = disc_poly(c, r_disc)
        frac = overlap_area(dp, floor) / G.area(dp)
        R.check("R2", f"{a['id']} 8 m disc 100% on the floor", clr >= 0.0 and frac >= 1.0 - 1e-9,
                disc_on_floor_pct=round(100 * frac, 6), edge_clearance_m=round(clr, 4))
        box = [(c[0] + sx * h, c[1] + sy * h) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        bclr = min(G.signed_clearance(p, floor) for p in box)
        bfrac = overlap_area(box, floor) / G.area(box)
        R.check("R2", f"{a['id']} 8 m scatter BOX (the pack's model) 100% on the floor",
                bclr >= 0.0 and bfrac >= 1.0 - 1e-9 and G.is_convex(floor),
                box_on_floor_pct=round(100 * bfrac, 6), corner_clearance_m=round(bclr, 4))

    blockers = [f for f in feats if f["blocks_movement"] or f["blocks_sight"] or f["z_top_m"] > wmax]

    # ---------------- R3 lines to origin ----------------
    o = (0.0, 0.0)
    R.check("R3", "the start (0, 0) is on the floor", G.signed_clearance(o, floor) > 0,
            clearance_m=round(G.signed_clearance(o, floor), 4))
    for a in anchors:
        c = (a["x"], a["y"])
        on_floor = G.signed_clearance(c, floor) > 0 and G.signed_clearance(o, floor) > 0 and G.is_convex(floor)
        gaps = [(G.seg_poly_dist(o, c, [tuple(p) for p in f["footprint"]]), f["id"]) for f in blockers]
        gmin = min(gaps) if gaps else (float("inf"), None)
        R.check("R3", f"line (0,0) -> {a['id']} on the floor and clear of every blocker",
                on_floor and gmin[0] > 0, length_m=round(math.hypot(*c), 3),
                nearest_blocker=gmin[1], nearest_blocker_gap_m=round(gmin[0], 3))

    # ---------------- R5 no interior blocker ----------------
    worst = (0.0, None)
    for f in blockers:
        oa = overlap_area([tuple(p) for p in f["footprint"]], floor)
        if oa > worst[0]:
            worst = (oa, f["id"])
    gaps = sorted((G.poly_poly_gap([tuple(p) for p in f["footprint"]], floor) if overlap_area([tuple(p) for p in f["footprint"]], floor) <= TOL else 0.0, f["id"]) for f in blockers)
    R.check("R5", "every blocker (blocks movement or sight, or taller than walk-over) has zero area inside the floor",
            worst[0] <= TOL, n_blockers=len(blockers), worst_overlap_m2=round(worst[0], 6), worst_id=worst[1],
            closest_blocker_gap_m=round(gaps[0][0], 3) if gaps else None, closest_blocker=gaps[0][1] if gaps else None)
    interior = [f for f in feats if overlap_area([tuple(p) for p in f["footprint"]], floor) > TOL]
    tall = [(f["id"], f["z_top_m"]) for f in interior if f["z_top_m"] > wmax or f["blocks_movement"] or f["blocks_sight"]]
    R.check("R5", f"every interior feature is walk-over (z_top <= {wmax} m, blocks nothing)", not tall,
            n_interior=len(interior), tallest_interior_m=max((f["z_top_m"] for f in interior), default=0.0), offenders=tall)
    for key in ("mere", "stream", "path"):
        R.check("R5", f"{key} is walkable and flush (z 0)", L[key]["walkable"] and abs(L[key]["z_m"]) <= TOL)

    # ---------------- R6 the stair ----------------
    S = L["stair"]
    fl = [tuple(p) for p in S["flight"]["polygon"]]          # W_top, E_top, E_foot, W_foot
    land = [tuple(p) for p in S["top_landing"]["polygon"]]
    w_meas = min(math.dist(fl[0], fl[1]), math.dist(fl[3], fl[2]))
    run_meas = (math.dist(fl[0], fl[3]) + math.dist(fl[1], fl[2])) / 2
    drop = S["flight"]["z_top_m"] - S["flight"]["z_bottom_m"]
    slope = math.degrees(math.atan2(drop, run_meas))
    R.check("R6", "stair width >= 2.5 m (measured off the flight polygon)", w_meas >= 2.5, width_m=round(w_meas, 4))
    R.check("R6", "stair slope walkable: <= 30 deg (and under Godot's default floor_max_angle 45 deg)",
            slope <= 30.0, slope_deg=round(slope, 3), run_m=round(run_meas, 3), drop_m=drop,
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
    R.check("R6", "the run is aligned toward the centre (climbing direction vs the bearing to (0,0))", ang <= 2.0,
            misalignment_deg=round(ang, 4))
    p3 = next(a for a in anchors if a["id"] == "p03")
    north = land[:len(land) - 2]
    on_bd = max(G.dist_to_boundary(p, floor) for p in north)
    in_floor = overlap_area(land, floor)
    box3 = [(p3["x"] + sx * h, p3["y"] + sy * h) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    to_patch = min(G.seg_poly_dist(north[i], north[i + 1], box3) for i in range(len(north) - 1))
    to_disc = min(G.dist_point_seg((p3["x"], p3["y"]), north[i], north[i + 1]) for i in range(len(north) - 1)) - r_disc
    R.check("R6", "top landing flush: same z as the floor, its north edge ON the floor boundary, no overlap, abutting the p03 patch across the 1 m margin",
            abs(S["top_landing"]["z_m"] - L["floor"]["z_m"]) <= TOL and on_bd <= 1e-3 and in_floor <= TOL and to_patch <= 1.0 + 1e-3,
            north_edge_off_boundary_m=round(on_bd, 6), landing_overlap_m2=round(in_floor, 6),
            gap_to_p03_box_m=round(to_patch, 4), gap_to_p03_disc_m=round(to_disc, 4),
            landing_north_edge_len_m=round(sum(math.dist(north[i], north[i + 1]) for i in range(len(north) - 1)), 3))
    for part in ("top_landing", "flight", "bottom_landing"):
        poly = [tuple(p) for p in S[part]["polygon"]]
        R.check("R6", f"stair {part} lies OUTSIDE the floor (zero overlap)", overlap_area(poly, floor) <= TOL,
                overlap_m2=round(overlap_area(poly, floor), 6))
    # open side: nothing blocking within 1.0 m of the flight's EAST edge (outside the flight)
    east_edge = (fl[1], fl[2])
    near_e = [(G.seg_poly_dist(east_edge[0], east_edge[1], [tuple(p) for p in f["footprint"]]), f["id"]) for f in blockers]
    near_e = min(near_e) if near_e else (float("inf"), None)
    west_edge = (fl[0], fl[3])
    near_w = [(G.seg_poly_dist(west_edge[0], west_edge[1], [tuple(p) for p in f["footprint"]]), f["id"]) for f in blockers if f["kind"] == "cliff"]
    near_w = min(near_w) if near_w else (float("inf"), None)
    R.check("R6", "one side open: no blocker within 1 m of the east edge; the cliff spur forms the west wall",
            near_e[0] > 1.0 and near_w[0] <= 1e-3, east_nearest=near_e[1], east_gap_m=round(near_e[0], 3),
            west_wall=near_w[1], west_gap_m=round(near_w[0], 6))
    # the flight must not cross any blocker (a monster climbing it is never stuck on geometry)
    hit = [f["id"] for f in blockers if overlap_area([tuple(p) for p in f["footprint"]], fl) > TOL]
    R.check("R6", "nothing stands on the flight or the landings", not hit, offenders=hit)

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
    R.check("R7", "the mere covers p05's 8 m disc 100%", clr5 >= 0.0, disc_edge_clearance_m=round(clr5, 4),
            p05_box_covered_pct=round(100 * n_in / n_all, 2))
    mere_in_floor = overlap_area(mere, floor) / G.area(mere)
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
    deliver = {"p02": ["barrow_door"], "p01": ["wreck_hull"], "p04": ["hall_great_door"], "p06": ["fallen_gable"],
               "p03": ["sea_cave_mouth"]}
    for pid, ids in deliver.items():
        for fid in ids:
            f = next((x for x in feats if x["id"] == fid), None)
            if f is None:
                R.check("R10", f"{pid}: {fid} exists", False)
                continue
            poly = [tuple(p) for p in f["footprint"]]
            oa = overlap_area(poly, floor)
            gap = G.poly_poly_gap(poly, floor) if oa <= TOL else 0.0
            limit = 22.0 if pid == "p03" else 3.0
            R.check("R10", f"{pid}: {fid} is outside the walkable edge and within {limit} m of it", oa <= TOL and gap <= limit,
                    overlap_m2=round(oa, 6), gap_to_floor_m=round(gap, 3))
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
    return B, {"R2", "R3", "R4", "R5", "R6", "R7"}


def print_report(R, title):
    print(f"== {title}")
    for r in R.rows:
        nums = {k: v for k, v in r.items() if k not in ("rule", "check", "PASS")}
        print(f"  {'PASS' if r['PASS'] else 'FAIL'}  {r['rule']:<4} {r['check']}  {json.dumps(nums, ensure_ascii=False)}")
    n_fail = sum(not r["PASS"] for r in R.rows)
    print(f"== {len(R.rows)} checks, {len(R.rows) - n_fail} PASS, {n_fail} FAIL -> {'PASS' if R.ok else 'FAIL'}")


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
