#!/usr/bin/env python3
"""barrow_v2 (Run C-9 Phase 2, lane BX): the Fjord Headland greybox layout, sim frame.

R-C9-145 (Matt): layout of record = sketch A (sites/BV3r2-A.png) + sketch B's stream from the
barrow into the mere, spawn plan sites/BV3r2-A_spawns.png, floor WHOLE (N-C9-BV2-FLOOR-WHOLE).

Sim frame: +x east, +y SOUTH, metres, origin = player start (0, 0). z = up (presentation only).

The anchors are read from the pack of record (engine, READ ONLY) at run time and their file
sha256 is written into the layout; nothing is typed by hand.

    python3 tools/make_layout_v2.py            -> barrow_v2/layout_v2.json
"""
import glob
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bv2_geom as G  # noqa: E402

ROOT = os.path.dirname(HERE)                                   # runs/C-9/barrow_v2
ENGINE = os.path.expanduser("~/Games/reincarnated-engine")
PACK_GLOB = "src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p11-*/model/arena.json"
CSV = "data/kc2/kc2_crucible_emitter_geometry_v3p8.csv"
PROJ = os.path.expanduser("~/Games/reincarnated-godot/kc2_runtime/play/kc2play_projection.gd")

# ---- the projection law's four constants (kc2play_projection.gd; re-read and asserted below) ----
ALPHA_DEG = 52.9535411256029
H_FIG_M = 1.9
FRACTION_ZOOM_GD = 0.0802
VIEW_H = 1080.0
PPM_PLATE = 100.617553710938

FLOOR_MARGIN_M = 1.0          # the brief: hull of the spawn regions + 1 m
WALKOVER_MAX_H_M = 0.40       # an interior feature at or under this reads (and plays) as walk-over
STAIR = {"width_m": 3.0, "drop_m": 7.0, "step_rise_m": 0.14, "step_tread_m": 0.36,
         "top_landing_depth_m": 2.0, "bottom_landing_depth_m": 3.0}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_anchors():
    packs = sorted(glob.glob(os.path.join(ENGINE, PACK_GLOB)))
    if not packs:
        sys.exit("HALT: no v3.11 pack arena.json under the engine")
    digests = {p: sha256(p) for p in packs}
    if len(set(digests.values())) != 1:
        sys.exit("HALT: the v3.11 packs' arena.json differ; name the pack of record")
    path = packs[-1]
    arena = json.load(open(path))
    rows = arena["⚑ v3p8_rows"]["sg1_spawn_points_gd"]
    anchors = []
    for r in rows:
        v = r["value"]
        anchors.append({"id": v["point_id"], "x": v["x"], "y": v["y"],
                        "heading_rad": v["heading_rad"], "radius_m": v["radius_m"],
                        "row_id": r["id"], "csv_emitter": v["csv_emitter"],
                        "coord_grade": v["coord_grade"]})
    anchors.sort(key=lambda a: a["id"])
    h = arena["placement_extents_m"]["value"]
    scatter = arena["presentation_defaults"]["scatter_model"]["basis"]
    prov = {
        "pack_arena_json": os.path.relpath(path, ENGINE),
        "pack_arena_json_sha256": digests[path],
        "pack_copies_identical": [os.path.relpath(p, ENGINE) for p in packs],
        "field": "⚑ v3p8_rows.sg1_spawn_points_gd[*].value.{x,y}",
        "csv": CSV, "csv_sha256": sha256(os.path.join(ENGINE, CSV)),
        "csv_note": "the CSV is the level-frame source (sm1/survivalworld_a.map); the pack's sg1 rows are its arena-centred image and are what this layout uses",
        "placement_extents_m": h,
        "scatter_model_basis_verbatim": scatter,
    }
    return anchors, h, prov


def check_projection():
    src = open(PROJ).read()
    for name, val in (("ALPHA_DEG", ALPHA_DEG), ("H_FIG_M", H_FIG_M),
                      ("FRACTION_ZOOM_GD", FRACTION_ZOOM_GD), ("PPM_PLATE", PPM_PLATE)):
        tok = f"const {name} := "
        i = src.index(tok) + len(tok)
        got = float(src[i:src.index("\n", i)].strip())
        assert abs(got - val) < 1e-12, (name, got, val)
    a = math.radians(ALPHA_DEG)
    ppm_gd = FRACTION_ZOOM_GD * VIEW_H / (H_FIG_M * math.cos(a))
    return {"source": "reincarnated-godot/kc2_runtime/play/kc2play_projection.gd",
            "source_sha256": sha256(PROJ),
            "law": "screen_x = ppm*x ; screen_y = ppm*sin(a)*y - ppm*cos(a)*z ; zero yaw (x screen-right, +y toward camera = screen-down)",
            "pitch_deg": ALPHA_DEG, "yaw_deg": 0.0, "projection": "orthographic",
            "ppm_plate": PPM_PLATE, "ppm_zoom_gd": ppm_gd,
            "window_zoom_gd_1920x1080_m": [1920.0 / ppm_gd, VIEW_H / (ppm_gd * math.sin(a))],
            "window_plate_1920x1080_m": [1920.0 / PPM_PLATE, VIEW_H / (PPM_PLATE * math.sin(a))],
            "godot_camera": "Camera3D orthographic, keep_aspect KEEP_HEIGHT, size = viewport_rows / ppm, rotation_degrees = (-pitch, 0, 0), placed at target + D*(0, sin(pitch), cos(pitch)) in Godot axes (X = x, Y = up, Z = y)"}


def ray_exit(poly, d, start=(0.0, 0.0)):
    """Distance along unit d from start to where the ray leaves the convex polygon."""
    best = None
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-12:
            continue
        t = ((ax - start[0]) * ey - (ay - start[1]) * ex) / den
        s = ((ax - start[0]) * d[1] - (ay - start[1]) * d[0]) / den
        if t > 0 and -1e-9 <= s <= 1 + 1e-9:
            best = t if best is None else max(best, t)
    return best


def unit(x, y):
    L = math.hypot(x, y)
    return (x / L, y / L)


def along(o, d, t, n=None, s=0.0):
    x = o[0] + d[0] * t
    y = o[1] + d[1] * t
    if n is not None:
        x += n[0] * s
        y += n[1] * s
    return (x, y)


def main():
    anchors, h, prov = read_anchors()
    cam = check_projection()
    A = {a["id"]: (a["x"], a["y"]) for a in anchors}

    # ---------------- floor: hull of every sim placement + 1 m ----------------
    box_corners = [(x + sx * h, y + sy * h) for (x, y) in A.values() for sx in (-1, 1) for sy in (-1, 1)]
    floor = G.offset_hull(box_corners, FLOOR_MARGIN_M, n=96)
    disc_floor = G.offset_hull(list(A.values()), h + FLOOR_MARGIN_M, n=192)

    # ---------------- the edge features, each placed on its anchor's ray ----------------
    feats = []

    def feat(fid, kind, poly, z0, z1, zone_edge, note, blocks=True, **kw):
        d = {"id": fid, "kind": kind, "footprint": G.rnd(poly), "z_bottom_m": z0, "z_top_m": z1,
             "blocks_movement": blocks, "blocks_sight": blocks and z1 > WALKOVER_MAX_H_M,
             "placement": "OUTSIDE the walkable edge" if zone_edge else "INSIDE the floor (walk-over)",
             "note": note}
        d.update(kw)
        feats.append(d)
        return d

    rays = {k: unit(*A[k]) for k in A}
    exits = {k: ray_exit(floor, rays[k]) for k in A}

    # N, p02: the barrow mound, its carved door just outside the edge
    d2 = rays["p02"]
    n2 = (-d2[1], d2[0])
    e2 = exits["p02"]
    door_c = along((0, 0), d2, e2 + 1.4)
    mound_c = along((0, 0), d2, e2 + 1.5 + 10.0)
    rot2 = math.degrees(math.atan2(n2[1], n2[0]))
    feat("barrow_mound", "mound", G.ellipse_poly(*mound_c, 15.0, 10.0, rot2, 64), 0.0, 7.0, True,
         "the King's barrow: grass/heather mound, kerbed; its near toe 1.5 m beyond the floor edge on p02's ray",
         shape={"type": "ellipsoid_cap", "centre": G.rnd(mound_c), "semi_axes_m": [15.0, 10.0], "rot_deg": G.rnd(rot2), "rise_m": 7.0})
    feat("barrow_door", "door", G.rect_poly(*door_c, 3.2, 1.2, rot2), 0.0, 3.2, True,
         "carved lintel door (p02, bosses: mist + rise from the grave-ground); threshold 0.8 m beyond the floor edge on the ray (its outer corners clear the edge too)",
         faces_deg=G.rnd(G.compass_deg(-d2[0], -d2[1]), 2))
    for i, (t, s, ht) in enumerate(((e2 + 4.0, -11.0, 2.6), (e2 + 3.0, 10.5, 2.2), (e2 + 13.0, -16.0, 2.0), (e2 + 12.0, 15.5, 2.4))):
        c = along((0, 0), d2, t, n2, s)
        feat(f"barrow_standing_stone_{i + 1}", "standing_stone", G.rect_poly(*c, 0.9, 0.6, rot2 + 17 * i), 0.0, ht, True,
             "standing stone on the barrow slope (stands up, so it lives outside the edge)")

    # the frozen stream, from high on the barrow's west flank down into the mere (sketch B)
    # W, p01: the wreck. Hull outside the edge, rail toward the floor; shore ice beyond.
    d1 = rays["p01"]
    e1 = exits["p01"]
    hull_c = along((0, 0), d1, e1 + 4.9)
    feat("wreck_hull", "wreck", G.rect_poly(*hull_c, 17.0, 4.6, 90.0 - 12.0), -0.4, 3.4, True,
         "the wreck: a beached longship heeled toward the floor, its rail the floor-side gunwale (p01: up through the shore ice / over the rail)",
         heel_deg=18.0, rail_side="east (toward the floor)")
    mast_c = along(hull_c, (1.0, 0.0), -0.6)
    feat("wreck_mast", "mast", G.ellipse_poly(*mast_c, 0.25, 0.25, 0, 12), 0.0, 8.0, True, "the broken mast, raked")
    for i, (dx, dy, r) in enumerate(((-3.0, -13.0, 1.6), (-1.0, 14.0, 1.4), (2.5, -20.0, 1.2), (3.0, 20.5, 1.7))):
        c = (hull_c[0] + dx, hull_c[1] + dy)
        feat(f"shore_rock_{i + 1}", "rock", G.ellipse_poly(*c, r, r * 0.8, 20 * i, 16), -0.4, 1.1, True, "shore rock, outside the edge")

    # E, p04 + SE, p06: the burnt longhall yard
    d4 = rays["p04"]
    e4 = exits["p04"]
    hall_w = along((0, 0), d4, e4 + 1.8)            # the hall's west wall crossing on p04's ray
    hall_x0 = hall_w[0]
    hall_poly = [(hall_x0, -10.0), (hall_x0 + 8.5, -10.0), (hall_x0 + 8.5, 13.0), (hall_x0, 13.0)]
    feat("longhall", "hall", hall_poly, 0.0, 6.5, True,
         "the burnt longhall, long axis N-S, roof half fallen; its west wall 1.8 m beyond the floor edge on p04's ray")
    feat("hall_great_door", "door", G.rect_poly(hall_x0, hall_w[1], 0.6, 3.6, 0.0), 0.0, 3.8, True,
         "the hall's great door (p04: out of smoke), in the west wall on p04's ray",
         faces_deg=270.0)
    d6 = rays["p06"]
    n6 = (-d6[1], d6[0])
    e6 = exits["p06"]
    gable_c = along((0, 0), d6, e6 + 2.6)
    rot6 = math.degrees(math.atan2(n6[1], n6[0]))
    feat("fallen_gable", "gable", G.rect_poly(*gable_c, 7.0, 2.6, rot6), 0.0, 2.8, True,
         "the fallen gable end (p06: up out of ash), leaning on its own rubble; 1.3 m beyond the floor edge on p06's ray")
    hut_c = along((0, 0), d6, e6 + 8.6)
    feat("gable_hut", "hall", G.rect_poly(*hut_c, 8.0, 6.0, rot6), 0.0, 4.2, True, "the byre the gable fell from")
    # the palisade, pulled back: it wraps the hall and byre from OUTSIDE; its arms stop 1.5 m short of the floor edge
    pal = []
    north_arm_start = along((0, 0), unit(math.sin(math.radians(62)), -math.cos(math.radians(62))),
                            ray_exit(floor, unit(math.sin(math.radians(62)), -math.cos(math.radians(62)))) + 1.5)
    south_arm_end = along((0, 0), unit(math.sin(math.radians(158)), -math.cos(math.radians(158))),
                          ray_exit(floor, unit(math.sin(math.radians(158)), -math.cos(math.radians(158)))) + 1.5)
    pts = [north_arm_start, (hall_x0 + 13.0, north_arm_start[1] - 1.0), (hall_x0 + 15.5, 8.0),
           (hall_x0 + 13.5, 30.0), (hut_c[0] + 3.0, hut_c[1] + 8.5), south_arm_end]
    gaps = {2, 4}   # two burnt-through gaps (segment index); the yard itself stays open to the floor
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        dirv = unit(b[0] - a[0], b[1] - a[1])
        if i in gaps:
            segs = [(0.0, 0.42), (0.62, 1.0)]
        else:
            segs = [(0.0, 1.0)]
        for j, (f0, f1) in enumerate(segs):
            c = along(a, dirv, L * (f0 + f1) / 2)
            pal.append(feat(f"palisade_{i + 1}{'ab'[j] if len(segs) > 1 else ''}", "palisade",
                            G.rect_poly(*c, L * (f1 - f0), 0.35, math.degrees(math.atan2(dirv[1], dirv[0]))),
                            0.0, 3.0, True, "palisade run, pulled back outside the edge"))

    # S/SSE, p03: the headland cliff, the sea cave and the STRAIGHT stair (R-C9-145)
    d3 = rays["p03"]
    n3 = (-d3[1], d3[0])                    # left-hand normal of the run going down = EAST-ish? (checked below)
    # make n3 point WEST-ish (the cliff spur side); the open side is east
    if n3[0] > 0:
        n3 = (-n3[0], -n3[1])
    w = STAIR["width_m"]
    e3 = exits["p03"]
    top_mid = along((0, 0), d3, e3)
    # the landing's north edge follows the floor boundary exactly (flush): each side line's exit point
    sideW = along((0, 0), n3, w / 2)
    sideE = along((0, 0), n3, -w / 2)
    tW = ray_exit(floor, d3, start=sideW)
    tE = ray_exit(floor, d3, start=sideE)
    lip_W = along(sideW, d3, tW)
    lip_E = along(sideE, d3, tE)
    # floor vertices strictly between the two side lines on this stretch of lip, W -> E
    between = [v for v in floor
               if abs(v[0] * n3[0] + v[1] * n3[1]) < w / 2 - 1e-9 and (v[0] * d3[0] + v[1] * d3[1]) > e3 - 3.0]
    between.sort(key=lambda v: -(v[0] * n3[0] + v[1] * n3[1]))
    tl = STAIR["top_landing_depth_m"]
    t_land = max(tW, tE) + tl
    land_W = along(sideW, d3, t_land)
    land_E = along(sideE, d3, t_land)
    n_steps = int(round(STAIR["drop_m"] / STAIR["step_rise_m"]))
    run = n_steps * STAIR["step_tread_m"]
    foot_W = along(land_W, d3, run)
    foot_E = along(land_E, d3, run)
    bl = STAIR["bottom_landing_depth_m"]
    bot_W = along(foot_W, d3, bl)
    bot_E = along(foot_E, d3, bl)
    slope_deg = math.degrees(math.atan2(STAIR["drop_m"], run))
    stair = {
        "id": "sea_cave_stair", "kind": "stair",
        "_ruling": "R-C9-145 (Matt): B's straighter stair, one side open to the cliff edge, wide, run aligned toward the centre, top landing flush with the p03 patch; monsters must climb it without getting stuck",
        "axis_unit_down": G.rnd(d3, 6), "axis_compass_deg_down": G.rnd(G.compass_deg(*d3), 3),
        "axis_points_at": "the origin (0, 0): the run is ON the ray origin -> p03, so climbing monsters face the centre",
        "width_m": w,
        "top_landing": {"polygon": G.rnd([lip_W] + between + [lip_E, land_E, land_W]), "z_m": 0.0,
                        "north_edge": "follows the floor boundary vertex-for-vertex between the two side lines (flush, same z as the floor)",
                        "depth_m_min": tl},
        "flight": {"polygon": G.rnd([land_W, land_E, foot_E, foot_W]), "z_top_m": 0.0, "z_bottom_m": -STAIR["drop_m"],
                   "n_steps": n_steps, "step_rise_m": STAIR["step_rise_m"], "step_tread_m": STAIR["step_tread_m"],
                   "run_m": run, "drop_m": STAIR["drop_m"], "slope_deg": slope_deg, "grade_pct": 100 * STAIR["drop_m"] / run,
                   "walk_model": "a REAL RAMP: one plane under the step nosings, the same slope as the treads' pitch line; the steps are a visual on it. Godot CharacterBody3D floor_max_angle default 45 deg > the slope, so a body walks it without a step-up solver",
                   "stair_rule_check": "2R + T = %.3f m (the comfortable band is 0.60-0.65 m)" % (2 * STAIR["step_rise_m"] + STAIR["step_tread_m"])},
        "bottom_landing": {"polygon": G.rnd([foot_W, foot_E, bot_E, bot_W]), "z_m": -STAIR["drop_m"],
                           "note": "the shelf at the sea-cave mouth, just above the water"},
        "open_side": "EAST: no wall, no rail -- the cliff drop is beside the treads the whole way down",
        "wall_side": "WEST: the headland spur's rock face (cliff_spur)",
        "placement": "OUTSIDE the floor polygon (it descends the cliff). The sim never reads it; it is the visible delivery path from the cave to the p03 patch.",
    }
    spur_W0 = along(lip_W, n3, 4.5)
    spur = [lip_W, bot_W, along(bot_W, n3, 4.0), spur_W0]
    feat("cliff_spur", "cliff", spur, -STAIR["drop_m"], 0.0, True,
         "the headland spur the stair is cut into; its east face is the stair's wall; its top is land (z 0) outside the edge")
    cave_c = along(along(foot_W, n3, 2.3), d3, 1.2)
    feat("sea_cave_mouth", "cave", G.rect_poly(*cave_c, 3.4, 1.4, math.degrees(math.atan2(n3[1], n3[0]))),
         -STAIR["drop_m"], -STAIR["drop_m"] + 3.6, True,
         "the sea-cave mouth in the spur's south-facing foot (p03: climb the cliff lip / steps); faces the camera",
         faces_deg=G.rnd(G.compass_deg(*d3), 2))

    # ---------------- interior: walk-over features only ----------------
    # the stone circle (centre, small and broken), 8 stones: 6 fallen flat, 2 low stumps
    circ_c = (2.5, -1.5)
    circ_r = 5.2
    stones = []
    for i in range(8):
        ang = math.radians(15 + i * 45 + (7 if i % 2 else -9))
        c = (circ_c[0] + circ_r * math.cos(ang), circ_c[1] + circ_r * math.sin(ang))
        if i in (2, 5):
            poly, ht, form = G.rect_poly(*c, 0.6, 0.5, i * 23), 0.35, "low stump (snapped off at the base)"
        else:
            poly, ht, form = G.rect_poly(*c, 1.8, 0.75, math.degrees(ang) + 90 + 25 * ((i % 3) - 1)), 0.30, "fallen, lying flat"
        stones.append(feat(f"circle_stone_{i + 1}", "fallen_stone", poly, 0.0, ht, False, form, blocks=False))
    # grave-ground markers, low
    for i, (x, y) in enumerate(((2.0, -24.0), (5.5, -21.5), (13.5, -22.5), (17.0, -25.0), (-2.5, -28.0), (6.5, -27.0), (19.5, -20.0))):
        feat(f"grave_marker_{i + 1}", "grave_marker", G.rect_poly(x, y, 0.5, 0.25, 8 * i - 20), 0.0, 0.30, False,
             "low grave marker, half sunk", blocks=False)
    for i, (x, y, L, r) in enumerate(((-30.0, 14.0, 3.2, 70), (-37.5, 1.0, 2.6, 110), (-27.5, 4.5, 2.0, 30), (-35.0, 16.5, 1.8, 150))):
        feat(f"driftwood_{i + 1}", "driftwood", G.rect_poly(x, y, L, 0.35, r), 0.0, 0.30, False, "driftwood on the shingle", blocks=False)
    for i, (x, y, L, r) in enumerate(((29.0, 1.0, 4.0, 15), (34.0, 12.0, 3.5, 80), (25.0, 13.5, 3.0, 140), (21.5, 23.5, 3.8, 35), (27.5, 20.0, 2.8, 100))):
        feat(f"yard_beam_{i + 1}", "beam", G.rect_poly(x, y, L, 0.4, r), 0.0, 0.25, False, "fallen roof beam, flat in the ash", blocks=False)

    # ---------------- the mere (p05), irregular, fed by the stream ----------------
    p5 = A["p05"]
    mc = (-14.0, -12.0)
    mere = []
    N = 72
    for k in range(N):
        t = G.TAU * k / N
        u = (math.cos(t), math.sin(t))
        # the disc's far boundary along this ray from mc, so the mere covers p05's 8 m disc + 0.7 m
        fx, fy = mc[0] - p5[0], mc[1] - p5[1]
        b = fx * u[0] + fy * u[1]
        cc = fx * fx + fy * fy - (h + 0.7) ** 2
        need = -b + math.sqrt(max(b * b - cc, 0.0))
        base = 11.5 + 2.2 * math.sin(3 * t + 0.6) + 1.3 * math.sin(5 * t + 2.0) + 0.8 * math.sin(8 * t + 1.1)
        # elongate toward the NW (toward the stream mouth), pull in toward the S
        base += 4.0 * max(0.0, math.cos(t - math.radians(225))) ** 2
        room = ray_exit(floor, u, start=mc) - 1.5       # keep the whole mere on the floor, 1.5 m in
        r = max(need, min(base, room))
        assert r <= room, ("the mere cannot cover p05 and stay on the floor along", round(math.degrees(t), 1))
        mere.append((mc[0] + r * u[0], mc[1] + r * u[1]))
    stream = [(1.0, -55.0), (-3.0, -47.0), (-7.5, -40.0), (-11.0, -33.5), (-15.0, -27.5)]
    # the mouth: 2.5 m inside the mere from its shore point nearest the stream's last bend
    shore = min(mere, key=lambda v: math.dist(v, stream[-1]))
    inward = unit(mc[0] - shore[0], mc[1] - shore[1])
    stream.append(along(shore, inward, 2.5))

    # ---------------- the worn path: barrow door -> through the circle -> the stair top ----------------
    path = [G.rnd(along((0, 0), d2, e2 - 0.2)), [9.0, -30.0], [6.0, -16.0], [3.0, -6.0], [2.0, 2.0], [4.5, 14.0], [7.5, 27.0],
            G.rnd(along((0, 0), d3, e3 - 0.2))]

    # ---------------- the land (headland) and the sea ----------------
    # The floor's lower chain is the cliff lip from its westmost to its eastmost vertex; the land
    # extends N (barrow slope) and E (hall yard) beyond the walkable edge.
    # The cliff lip runs from the floor's westmost vertex, round the south, to the east end of its
    # flat south edge (y = y_max, beneath p03); east of that the edge is the hall yard, and the land
    # carries on outward (SE) under the gable and the byre.
    iw = min(range(len(floor)), key=lambda i: (floor[i][0], -floor[i][1]))
    ymax = max(p[1] for p in floor)
    ie = max((i for i in range(len(floor)) if floor[i][1] >= ymax - 1e-6), key=lambda i: floor[i][0])

    def chain(i0, i1, step):
        out = [floor[i0]]
        i = i0
        while i != i1:
            i = (i + step) % len(floor)
            out.append(floor[i])
        return out
    c1 = chain(iw, ie, 1)
    c2 = chain(iw, ie, -1)
    lip = c1 if max(p[1] for p in c1) >= ymax - 1e-6 and len(c1) <= len(c2) else c2
    xw, yw = lip[0]
    xe, ye = lip[-1]
    land = lip + [(xe + 7.0, ye + 7.0), (66.0, ye + 7.0), (66.0, -74.0), (-46.0, -74.0), (-46.0, yw)]
    # the cliff lip is the S part of that chain (compass 100..250 from the origin), the shore W of it
    shore_ice = [(-46.0, -60.0), (-46.0, yw), (xw, yw)] + [p for p in lip if G.compass_deg(*p) >= 235.0] + \
        [(-30.0, 46.0), (-62.0, 46.0), (-62.0, -60.0)]

    zones = {
        "_how": "soft colour zones on the floor; the ground class map (greybox/ground_class_map.png, 4 px/m) is the paint + crater-v5 surface driver. Priority: mere > stream > circle > path (overlay) > the seeded biomes (nearest weighted seed, blended over blend_m at the seams)",
        "blend_m": 3.0,
        "classes": {
            "grave_ground": {"rgb": [0.58, 0.47, 0.50], "surface": "heather_snow", "seeds": [[9.5, -29.0], [0.0, -30.0], [20.0, -26.0]], "reason": "the barrow's dead: heather over the graves in front of the King's door"},
            "shore_shingle": {"rgb": [0.62, 0.66, 0.70], "surface": "shingle", "seeds": [[-34.0, 9.5], [-36.0, -4.0], [-30.0, 22.0]], "reason": "the beach the wreck drove onto; shingle running into shore ice"},
            "cliff_top_rock": {"rgb": [0.70, 0.69, 0.66], "surface": "rock_scree", "seeds": [[8.0, 32.0], [-12.0, 30.0], [-22.0, 34.0]], "reason": "wind-scoured headland: thin snow on bare rock and scree above the sea"},
            "hall_yard_ash": {"rgb": [0.47, 0.44, 0.42], "surface": "ash", "seeds": [[31.0, 6.8], [20.8, 18.0], [26.0, -6.0]], "reason": "the burnt hall's yard: trampled ash and soot-black snow"},
            "snow_field": {"rgb": [0.90, 0.89, 0.86], "surface": "snow", "seeds": [[-10.0, 14.0], [12.0, 8.0], [-20.0, -32.0]], "reason": "open snow binding the biomes (the seams melt into it)"},
            "mere_ice": {"rgb": [0.70, 0.82, 0.92], "surface": "ice", "polygon": "mere", "reason": "the frozen mere, fed by the barrow stream; p05's dead burst up through it"},
            "stream_ice": {"rgb": [0.66, 0.79, 0.90], "surface": "ice", "polyline": "stream", "width_m": 2.6, "reason": "the frozen stream running down from the barrow into the mere (sketch B)"},
            "circle": {"rgb": [0.80, 0.78, 0.72], "surface": "trodden_snow_stone", "disc": {"centre": list(circ_c), "r_m": circ_r + 1.2}, "reason": "the broken stone circle at the start: a landmark you walk through"},
            "path": {"rgb": [0.68, 0.60, 0.50], "surface": "trodden_snow", "polyline": "path", "width_m": 1.6, "reason": "the worn path from the King's door through the circle to the cliff stair"},
        },
    }

    zg = math.radians(ALPHA_DEG)
    ppm = cam["ppm_zoom_gd"]
    win = cam["window_zoom_gd_1920x1080_m"]
    # Each door view is centred between the patch and its deliverer so both are in the 25 x 18 m
    # window (centred on the anchor, the 16 m patch fills the frame and the door is cut off).
    views = [
        {"id": "V1_start", "target": [0.0, 0.0], "what": "the start inside the broken circle; the mere's edge W"},
        {"id": "V2_p02_barrow_door", "target": G.rnd(along((0, 0), d2, e2 - 5.0)), "what": "p02's patch and the King's door"},
        {"id": "V3_p01_wreck", "target": G.rnd(along((0, 0), d1, e1 - 5.0)), "what": "p01's patch on the shingle and the wreck's rail"},
        {"id": "V4_p04_hall_door", "target": G.rnd(along((0, 0), d4, e4 - 4.0)), "what": "p04's patch in the hall yard and the great door"},
        {"id": "V5_p06_fallen_gable", "target": G.rnd(along((0, 0), d6, e6 - 4.0)), "what": "p06's patch in the ash and the fallen gable"},
        {"id": "V6_p05_mere", "target": G.rnd((A["p05"][0] - 3.0, A["p05"][1] - 3.0)), "what": "the frozen mere over p05, the stream mouth, the circle's W stones"},
        {"id": "V7_p03_stair_top", "target": G.rnd(along((0, 0), d3, e3 + 1.0)), "what": "p03's patch edge, the top landing flush with the floor, the stair down"},
    ]
    for v in views:
        v["window_m"] = G.rnd(win)
        v["ppm"] = ppm

    layout = {
        "_what": "barrow_v2 'Fjord Headland' GREYBOX layout, sim frame (Run C-9 Phase 2, lane BX, drax). Built by tools/make_layout_v2.py; proved by tools/validate_layout_v2.py.",
        "_rulings": {
            "R-C9-145": "layout of record = sketch A (sites/BV3r2-A.png) + sketch B's stream into the mere; spawn plan sites/BV3r2-A_spawns.png; floor WHOLE; straight sea-cave stair, one side open, wide, aligned to centre, top landing flush with p03",
            "R-C9-144": "Fjord Headland; walkable edge = the land itself per biome; small broken stone ring; larger irregular mere fed by the barrow stream; mini-biomes blending at seams",
            "N-C9-BV2-FLOOR-WHOLE": "Sim Session option (c): the floor is whole; feel-smaller by art only; a flat/walk-over central feature at (0, 0)",
            "N-C9-KP253-ANCHORS": "the floor contains all six anchor scatter regions and the open lines to origin",
        },
        "version": 1,
        "frame": {"units": "m", "x": "east", "y": "SOUTH", "z": "up (presentation only)", "origin": "player start (0, 0)",
                  "compass": "bearing clockwise from north = atan2(x, -y)",
                  "godot_axes": "X = x, Y = z (up), Z = y; the camera sits at +Z (south) looking north"},
        "camera": cam,
        "anchors": {
            "provenance": prov,
            "scatter": {"model": "BOX (per-axis U(-h, +h) about the anchor)", "half_width_m": h,
                        "disc_radius_m_brief": h,
                        "⚑ finding": "The pack's presentation_defaults.scatter_model says the sim rolls a per-axis BOX of half-width 8 m, NOT an 8 m disc (box corner 11.31 m from the anchor). The brief's 8 m disc is contained in the box. This floor contains every BOX (+1 m), so every body the sim can place is on the floor; it therefore also contains every disc (+1 m) and the brief's ~4,026 m2 disc hull."},
            "points": [dict(a, compass_deg=G.rnd(G.compass_deg(a["x"], a["y"]), 2),
                            dist_from_start_m=G.rnd(math.hypot(a["x"], a["y"]), 3),
                            delivered_by={"p01": "the wreck (up through the shore ice / over the rail)",
                                          "p02": "the barrow door (bosses: mist + rise from the grave-ground)",
                                          "p03": "the sea cave (climb the stair to the top landing)",
                                          "p04": "the hall's great door (out of smoke)",
                                          "p05": "the frozen mere (4 s of cracks, then burst through the ice)",
                                          "p06": "the fallen gable (up out of ash)"}[a["id"]])
                       for a in anchors],
        },
        "floor": {
            "rule": "WHOLE and convex: the convex hull of the six 8 m scatter BOXES + 1 m (Minkowski sum with a 1 m disc, sampled at 3.75 deg)",
            "polygon": G.rnd(floor),
            "z_m": 0.0,
            "area_m2": G.rnd(G.area(floor), 2),
            "extents": {k: G.rnd(v, 3) for k, v in G.extents(floor).items()},
            "min_disc_hull_reference": {"rule": "the brief's minimum: hull of the six 8 m discs + 1 m",
                                        "polygon": G.rnd(disc_floor, 3), "area_m2": G.rnd(G.area(disc_floor), 2),
                                        "extents": {k: G.rnd(v, 3) for k, v in G.extents(disc_floor).items()}},
            "edge_by_biome": {"N": "the barrow slope (mound toe, door, standing stones)", "W": "the shore: shingle into shore ice, the wreck",
                              "S/SSE": "the cliff lip (the floor edge IS the lip); the sea cave below, the stair", "E/SE": "the hall yard: hall wall, palisade (pulled back), the fallen gable"},
            "walkover_max_h_m": WALKOVER_MAX_H_M,
        },
        "land": {"polygon": G.rnd(land), "z_top_m": 0.0, "z_cliff_foot_m": -STAIR["drop_m"],
                 "cliff_lip": G.rnd(lip), "note": "the headland: the floor's southern chain is the cliff lip; land continues N (barrow) and E (hall yard) outside the walkable edge"},
        "shore_ice": {"polygon": G.rnd(shore_ice), "z_m": -0.4, "note": "shore ice W and SW of the land, outside the edge"},
        "sea": {"z_m": -STAIR["drop_m"] - 0.3, "extent": [[-90.0, -90.0], [90.0, 90.0]]},
        "mere": {"polygon": G.rnd(mere), "z_m": 0.0, "walkable": True, "surface": "ice, flush with the floor",
                 "covers": "p05's 8 m disc + 0.7 m; reaches the stone circle", "area_m2": G.rnd(G.area(mere), 2)},
        "stream": {"polyline": G.rnd(stream), "width_m": 2.6, "z_m": 0.0, "walkable": True,
                   "note": "frozen; rises up the barrow's west flank outside the edge (z follows the land), flush ice where it crosses the floor, ends in the mere"},
        "stone_circle": {"centre": list(circ_c), "radius_m": circ_r, "n_stones": 8,
                         "stones": [s["id"] for s in stones], "note": "small, broken; 6 fallen flat (0.30 m), 2 snapped stumps (0.35 m); the worn path runs through it"},
        "path": {"polyline": path, "width_m": 1.6, "z_m": 0.0, "walkable": True},
        "zones": zones,
        "stair": stair,
        "features": feats,
        "views": views,
        "walk_film": {"route": [[0.0, 0.0], [2.0, -12.0], G.rnd(along(A["p02"], d2, -3.0)), [-6.0, -20.0],
                                G.rnd(A["p05"]), G.rnd(along(A["p01"], d1, -2.0)), [-12.0, 22.0],
                                G.rnd(along((0, 0), d3, e3 - 1.0)), [18.0, 18.0], G.rnd(along(A["p04"], d4, -2.0)), [0.0, 0.0]],
                      "speed_mps": 8.0, "camera": "ZOOM-GD window, following the walker"},
    }
    out = os.path.join(ROOT, "layout_v2.json")
    with open(out, "w") as f:
        json.dump(layout, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote", out, "floor area", round(G.area(floor), 1), "features", len(feats))


if __name__ == "__main__":
    main()
