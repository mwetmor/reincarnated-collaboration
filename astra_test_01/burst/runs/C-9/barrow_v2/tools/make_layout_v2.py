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
SPAWN = "src/reincarnated/simulation/kc2/spawn_structure.py"
PROJ = os.path.expanduser("~/Games/reincarnated-godot/kc2_runtime/play/kc2play_projection.gd")

# ---- the projection law's four constants (kc2play_projection.gd; re-read and asserted below) ----
ALPHA_DEG = 52.9535411256029
H_FIG_M = 1.9
FRACTION_ZOOM_GD = 0.0802
VIEW_H = 1080.0
PPM_PLATE = 100.617553710938

FLOOR_MARGIN_M = 1.0          # the brief: hull of the spawn regions + 1 m
WALKOVER_MAX_H_M = 0.40       # an interior feature at or under this reads (and plays) as walk-over
# R-C9-148: the cliff is lowered (sea at -4.5 m, ledge top -4.2 m); the stair climbs the face from the ledge.
STAIR = {"width_m": 3.0, "drop_m": 4.2, "step_rise_m": 0.15, "step_tread_m": 0.30, "sea_z_m": -4.5,
         "tangent_beta_deg": 70.0, "cave_beta_deg": 106.0,   # beta from +x toward +y about p03; p03's own arc is 41.8..117.8 deg
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
    global SPAWN_SHA
    src = open(os.path.join(ENGINE, SPAWN)).read().splitlines()
    assert "scatter: ScatterLaw = ScatterLaw.POLAR_UNIFORM_RHO" in src[294], "spawn_structure.py:295 moved; re-cite the scatter law"
    SPAWN_SHA = sha256(os.path.join(ENGINE, SPAWN))
    anchors, h, prov = read_anchors()
    cam = check_projection()
    A = {a["id"]: (a["x"], a["y"]) for a in anchors}

    # ---------------- floor: hull of every sim placement + 1 m ----------------
    box_corners = [(x + sx * h, y + sy * h) for (x, y) in A.values() for sx in (-1, 1) for sy in (-1, 1)]
    # R-C9-BX conductor ruling (2026-10-03): the floor of record is the EXACT bound, the convex hull of
    # the six 8 m scatter DISCS + 1 m. The oracle rolls a polar disc (spawn_structure.py:295,
    # ScatterLaw.POLAR_UNIFORM_RHO: theta = 2 pi u1, rho = 8 u2); the pack's box prose is a logged erratum.
    # n = 360 keeps the chord sag at 9 * (1 - cos 0.5 deg) = 0.00034 m.
    floor = G.offset_hull(list(A.values()), h + FLOOR_MARGIN_M, n=360)
    box_floor = G.offset_hull(box_corners, FLOOR_MARGIN_M, n=96)

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
    hull_c = along((0, 0), d1, e1 + 3.8)   # v2: 3.8 (was 4.9) so the hull sits ~1.4 m off the curved disc-hull edge
    feat("wreck_hull", "wreck", G.rect_poly(*hull_c, 17.0, 4.6, 90.0 - 12.0), -0.4, 3.4, True,
         "the wreck: a beached longship heeled toward the floor, its rail the floor-side gunwale (p01: up through the shore ice / over the rail)",
         heel_deg=18.0, rail_side="east (toward the floor)")
    mast_c = along(hull_c, (1.0, 0.0), -0.6)
    feat("wreck_mast", "mast", G.ellipse_poly(*mast_c, 0.25, 0.25, 0, 12), 0.0, 8.0, True, "the broken mast, raked")
    for i, (dx, dy, r) in enumerate(((-3.0, -13.0, 1.6), (-1.0, 14.0, 1.4), (2.5, -20.0, 1.2), (3.0, 20.5, 1.7))):
        c = (hull_c[0] + dx, hull_c[1] + dy)
        feat(f"shore_rock_{i + 1}", "rock", G.ellipse_poly(*c, r, r * 0.8, 20 * i, 16), -0.4, 1.1, True, "shore rock, outside the edge")

    # E, p04 + SE, p06: the burnt longhall yard -- ONE building (R-C9-148). The hall runs parallel to
    # the floor edge between p04 and p06 (the two discs' common tangent), its long west wall facing the
    # floor 1.5 m beyond that edge; the great door is on p04's ray, and the hall's own collapsed
    # south-west end (the fallen gable) is on p06's ray.
    d4 = rays["p04"]
    e4 = exits["p04"]
    d6 = rays["p06"]
    e6 = exits["p06"]
    p4, p6 = A["p04"], A["p06"]
    ax_sw = unit(p6[0] - p4[0], p6[1] - p4[1])                  # along the hall, NE -> SW
    nT = (-ax_sw[1], ax_sw[0])
    if nT[0] * p4[0] + nT[1] * p4[1] < 0:
        nT = (-nT[0], -nT[1])                                   # outward (away from the start)
    c_edge = nT[0] * p4[0] + nT[1] * p4[1] + h + FLOOR_MARGIN_M  # the floor's straight edge p04 <-> p06
    c_wall = c_edge + 1.5                                       # the hall's west (floor-facing) wall line
    HALL_D = 8.0

    def on_wall(dray):
        return along((0, 0), dray, c_wall / (dray[0] * nT[0] + dray[1] * nT[1]))
    D = on_wall(d4)                                             # the great door
    Gp = on_wall(d6)                                            # the gable's centre on the wall line
    ax_ne = (-ax_sw[0], -ax_sw[1])

    def hall_rect(s0, s1, base):
        """wall-line stretch from base + s0*ax_ne to base + s1*ax_ne, HALL_D deep outward."""
        a0 = along(base, ax_ne, s0)
        a1 = along(base, ax_ne, s1)
        return [a0, a1, along(a1, nT, HALL_D), along(a0, nT, HALL_D)]
    GABLE_BACK, GABLE_FWD, NE_PAST_DOOR = 2.0, 4.0, 6.0
    L_GD = math.dist(Gp, D)
    rot_ax = math.degrees(math.atan2(ax_ne[1], ax_ne[0]))
    feat("longhall", "hall", hall_rect(GABLE_FWD, L_GD + NE_PAST_DOOR, Gp), 0.0, 6.5, True,
         "the burnt longhall: ONE building angled NE -> SW along the floor edge between p04 and p06; its long west wall faces the floor 1.5 m beyond the edge; roof half fallen",
         axis_compass_deg_sw=G.rnd(G.compass_deg(*ax_sw), 2), length_m=G.rnd(L_GD + NE_PAST_DOOR + GABLE_BACK, 2), depth_m=HALL_D)
    feat("hall_great_door", "door", G.rect_poly(*along(D, nT, 0.3), 3.6, 0.6, rot_ax), 0.0, 3.8, True,
         "the hall's great door (p04: out of smoke), in the long west wall on p04's ray",
         faces_deg=G.rnd(G.compass_deg(-nT[0], -nT[1]), 2))
    feat("fallen_gable", "gable", hall_rect(-GABLE_BACK, GABLE_FWD, Gp), 0.0, 2.8, True,
         "the hall's OWN collapsed south-west end (p06: up out of ash): the gable fallen outward, leaning on its rubble; on p06's ray, 1.5 m beyond the floor edge")
    # the palisade, pulled back: it wraps the hall from OUTSIDE; its arms stop 1.5 m short of the floor edge
    pal = []

    def arm(deg):
        u_ = unit(math.sin(math.radians(deg)), -math.cos(math.radians(deg)))
        return along((0, 0), u_, ray_exit(floor, u_) + 1.5)
    north_arm_start = arm(62.0)
    south_arm_end = arm(140.0)
    pts = [north_arm_start, along(D, ax_ne, NE_PAST_DOOR + 5.0), along(along(D, ax_ne, NE_PAST_DOOR + 5.0), nT, HALL_D + 3.5),
           along(along(Gp, ax_ne, -GABLE_BACK - 4.0), nT, HALL_D + 3.5), along(Gp, ax_ne, -GABLE_BACK - 4.0), south_arm_end]
    gaps = {2, 3}   # two burnt-through gaps (segment index); the yard itself stays open to the floor
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        dirv = unit(b[0] - a[0], b[1] - a[1])
        segs = [(0.0, 0.42), (0.62, 1.0)] if i in gaps else [(0.0, 1.0)]
        for j, (f0, f1) in enumerate(segs):
            c = along(a, dirv, L * (f0 + f1) / 2)
            pal.append(feat(f"palisade_{i + 1}{'ab'[j] if len(segs) > 1 else ''}", "palisade",
                            G.rect_poly(*c, L * (f1 - f0), 0.35, math.degrees(math.atan2(dirv[1], dirv[0]))),
                            0.0, 3.0, True, "palisade run, pulled back outside the edge"))

    # S/SSE, p03: the headland cliff, the sea cave and the STRAIGHT stair (R-C9-145, rebuilt R-C9-148).
    # The cave is in the MAIN south cliff face directly below the floor edge under p03's patch, a rock
    # ledge at sea level in front of it; the stair climbs FROM that ledge UP the face (wall = the cliff on
    # its north side, open to the sea on its south side) to a top landing flush with the floor edge at
    # p03's patch. Its run angles across the face; climbers turn toward the centre on the landing.
    d3 = rays["p03"]
    e3 = exits["p03"]
    p3 = A["p03"]
    w = STAIR["width_m"]
    R9 = h + FLOOR_MARGIN_M
    bm = math.radians(STAIR["tangent_beta_deg"])                 # where the flight's wall line touches p03's arc
    nh = (math.cos(bm), math.sin(bm))                           # outward normal there
    u = (math.sin(bm), -math.cos(bm))                           # along the face, UP-stair = toward the east/north-east
    if u[0] < 0:
        u = (-u[0], -u[1])
    M = along(p3, nh, R9 + 0.02)
    n_steps = int(round(STAIR["drop_m"] / STAIR["step_rise_m"]))
    run = n_steps * STAIR["step_tread_m"]
    B_n = along(M, u, -run / 2)            # foot, wall side
    T_n = along(M, u, run / 2)             # top, wall side
    B_s = along(B_n, nh, w)                # foot, sea side
    T_s = along(T_n, nh, w)                # top, sea side

    def first_hit(start, d):
        best = None
        n = len(floor)
        for i in range(n):
            ax_, ay_ = floor[i]
            bx_, by_ = floor[(i + 1) % n]
            ex_, ey_ = bx_ - ax_, by_ - ay_
            den = d[0] * ey_ - d[1] * ex_
            if abs(den) < 1e-12:
                continue
            t = ((ax_ - start[0]) * ey_ - (ay_ - start[1]) * ex_) / den
            sg = ((ax_ - start[0]) * d[1] - (ay_ - start[1]) * d[0]) / den
            if t > 0 and -1e-9 <= sg <= 1 + 1e-9:
                best = t if best is None else min(best, t)
        return along(start, d, best)
    inward = (-nh[0], -nh[1])
    TL = STAIR["top_landing_depth_m"]
    E_s = along(T_s, u, TL)
    T_b = first_hit(T_n, inward)
    E_b = first_hit(E_s, inward)
    B_b = first_hit(B_n, inward)

    def arc_between(sA, sB):
        """floor vertices near this stretch of lip whose position along u lies strictly in (sA, sB), by s descending."""
        vs = [v for v in floor
              if sA + 1e-6 < (v[0] - M[0]) * u[0] + (v[1] - M[1]) * u[1] < sB - 1e-6
              and (v[0] - M[0]) * nh[0] + (v[1] - M[1]) * nh[1] > -4.0]
        return sorted(vs, key=lambda v: -((v[0] - M[0]) * u[0] + (v[1] - M[1]) * u[1]))

    def s_of(P):
        return (P[0] - M[0]) * u[0] + (P[1] - M[1]) * u[1]
    landing = [T_s, E_s, E_b] + arc_between(s_of(T_b), s_of(E_b)) + [T_b]
    landing_bd = [E_b] + arc_between(s_of(T_b), s_of(E_b)) + [T_b]
    wall_rock = [B_n, T_n, T_b] + arc_between(s_of(B_b), s_of(T_b)) + [B_b]
    ledge_z = -STAIR["drop_m"]
    # the ledge: from beyond the cave (west) to the stair's foot, 4.5 m deep, its north side on the cliff foot
    cave_beta = math.radians(STAIR["cave_beta_deg"])
    cave_at = along(p3, (math.cos(cave_beta), math.sin(cave_beta)), R9 + 0.35)
    cave_t = (math.sin(cave_beta), -math.cos(cave_beta))
    # the ledge: the cliff foot from just west of the cave to the flight's foot, 4.5 m out to sea.
    # (Its west end stays on p03's own arc, beta <= 117 deg < the 117.8 deg tangent to p01's disc, so the
    # arc points are outside the floor.)
    betas = []
    bb = cave_beta + math.radians(11.0)
    while s_of(along(p3, (math.cos(bb), math.sin(bb)), R9)) < s_of(B_n) - 0.05:
        betas.append(bb)
        bb -= math.radians(1.5)
    ledge = [along(p3, (math.cos(b_), math.sin(b_)), R9 + 0.02) for b_ in betas] + [B_n, B_s] + \
        [along(p3, (math.cos(b_), math.sin(b_)), R9 + 4.5) for b_ in reversed(betas)]
    slope_deg = math.degrees(math.atan2(STAIR["drop_m"], run))
    run_up = u
    to_c = unit(-T_n[0], -T_n[1])
    stair = {
        "id": "sea_cave_stair", "kind": "stair",
        "_ruling": "R-C9-145 (Matt) + R-C9-148 (Matt, from the walk film: 'the stairs seem to be below the sea cave which doesnt make alot of sense'): the cave sits in the MAIN south cliff face under p03's patch with a ledge at sea level; a straight stair, 3.0 m wide, climbs FROM that ledge UP the face to a top landing flush with the floor edge at p03's patch; open on the sea side; its run angles across the face (the 'aligned to centre' rule is dropped by R-C9-148); climbers turn toward the centre on the landing",
        "axis_unit_up": G.rnd(run_up, 6), "axis_compass_deg_up": G.rnd(G.compass_deg(*run_up), 3),
        "turn_on_landing_deg_info": G.rnd(math.degrees(math.acos(max(-1, min(1, run_up[0] * to_c[0] + run_up[1] * to_c[1])))), 2),
        "width_m": w,
        "top_landing": {"polygon": G.rnd(landing), "boundary_edge": G.rnd(landing_bd), "z_m": 0.0,
                        "north_edge": "follows the floor boundary vertex-for-vertex (flush, same z as the floor) at p03's patch",
                        "depth_along_run_m": TL},
        "flight": {"polygon": G.rnd([T_n, T_s, B_s, B_n]), "polygon_order": "top wall-side, top sea-side, foot sea-side, foot wall-side",
                   "z_top_m": 0.0, "z_bottom_m": ledge_z,
                   "n_steps": n_steps, "step_rise_m": STAIR["step_rise_m"], "step_tread_m": STAIR["step_tread_m"],
                   "run_m": run, "drop_m": STAIR["drop_m"], "slope_deg": slope_deg, "grade_pct": 100 * STAIR["drop_m"] / run,
                   "walk_model": "a REAL RAMP: one plane under the step nosings, the same slope as the treads' pitch line; the steps are a visual on it. Godot CharacterBody3D floor_max_angle default 45 deg > the slope, so a body walks it without a step-up solver",
                   "stair_rule_check": "2R + T = %.3f m (the comfortable band is 0.60-0.65 m)" % (2 * STAIR["step_rise_m"] + STAIR["step_tread_m"])},
        "bottom_landing": {"polygon": G.rnd(ledge), "z_m": ledge_z,
                           "note": "the rock ledge at sea level in front of the cave; the flight's foot stands on it"},
        "open_side": "SOUTH (the sea side): no wall, no rail",
        "wall_side": "NORTH: the main cliff face (stair_wall_rock fills the face between the straight flight and the curved lip)",
        "placement": "OUTSIDE the floor polygon (it climbs the cliff face). The sim never reads it; it is the visible delivery path from the cave to the p03 patch.",
    }
    feat("stair_wall_rock", "cliff", wall_rock, STAIR["sea_z_m"], 0.0, True,
         "the main cliff face between the curved lip and the straight flight: the stair's wall (outside the edge)")
    feat("sea_cave_mouth", "cave", G.rect_poly(*cave_at, 3.0, 0.7, math.degrees(math.atan2(cave_t[1], cave_t[0]))),
         ledge_z, ledge_z + 2.8, True,
         "the sea-cave mouth in the MAIN south cliff face, directly below the floor edge under p03's patch; faces the camera; the ledge in front of it",
         faces_deg=G.rnd(G.compass_deg(math.cos(cave_beta), math.sin(cave_beta)), 2))

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
    # (v2, disc hull: no flat south edge any more) the lip ends at the floor vertex nearest compass
    # 150 deg, between p03 (166) and p06 (131): east of the stair, where the hall yard begins.
    iw = min(range(len(floor)), key=lambda i: (floor[i][0], -floor[i][1]))
    ymax = max(p[1] for p in floor)
    # (R-C9-148) the lip runs from the westmost vertex round the south to Q, the floor edge at compass
    # 145 deg: east of the stair's top landing, west of the hall's fallen gable. East of Q the land
    # carries on outward under the hall yard.
    uq = unit(math.sin(math.radians(145.0)), -math.cos(math.radians(145.0)))
    Q = along((0, 0), uq, ray_exit(floor, uq))
    lip = [floor[iw]]
    i = iw
    for step in (1, -1):
        out = [floor[iw]]
        i = iw
        ok = False
        for _ in range(len(floor)):
            i = (i + step) % len(floor)
            v = floor[i]
            if v[1] > 0 and G.compass_deg(*v) < 145.0:
                ok = True
                break
            out.append(v)
        if ok and max(p[1] for p in out) >= ymax - 1e-6:
            lip = out + [Q]
            break
    xw, yw = lip[0]
    xe, ye = lip[-1]
    n36 = unit(-(A["p06"][1] - A["p03"][1]), A["p06"][0] - A["p03"][0])
    if n36[0] * Q[0] + n36[1] * Q[1] < 0:
        n36 = (-n36[0], -n36[1])
    q_out = along(Q, n36, 9.0)
    land = lip + [q_out, (66.0, q_out[1]), (66.0, -74.0), (-46.0, -74.0), (-46.0, yw)]
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
        {"id": "V7_p03_stair_top", "target": G.rnd(along(M, nh, 1.5)), "what": "the sea cave at the stair's foot, the stair rising up the cliff face to the top landing flush with p03's patch"},
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
        "version": 3,
        "_v3": "R-C9-148 (Matt, from the walk film): the sea cave moved into the main south face under p03 with a sea-level ledge; the stair climbs the face from the ledge to a flush top landing (cliff lowered, sea -4.5 m); the hall is ONE angled building, the fallen gable its own collapsed SW end; the byre removed; the palisade re-fitted",
        "_v2": "conductor ruling 2026-10-03: floor tightened from the box hull (v1, 4,670.8 m2) to the exact disc hull + 1 m; everything on the edge re-fitted by construction (deliverers, palisade, stair landing, mere clamp, views are all placed off the floor polygon)",
        "frame": {"units": "m", "x": "east", "y": "SOUTH", "z": "up (presentation only)", "origin": "player start (0, 0)",
                  "compass": "bearing clockwise from north = atan2(x, -y)",
                  "godot_axes": "X = x, Y = z (up), Z = y; the camera sits at +Z (south) looking north"},
        "camera": cam,
        "anchors": {
            "provenance": prov,
            "scatter": {"model": "DISC: polar, theta = 2 pi u1, rho = 8 u2 (ScatterLaw.POLAR_UNIFORM_RHO, the default)",
                        "disc_radius_m": h, "half_width_m": h, "disc_radius_m_brief": h,
                        "law_provenance": {"file": "engine:src/reincarnated/simulation/kc2/spawn_structure.py",
                                           "lines": "268-330, default at 295 (`scatter: ScatterLaw = ScatterLaw.POLAR_UNIFORM_RHO`)",
                                           "sha256": SPAWN_SHA, "runtime": "the arena runtime matches it bit for bit (drax G3)",
                                           "confirmed_by": "KC2 conductor via the C-9 conductor (lane BX ruling, 2026-10-03)"},
                        "⚑ pack_erratum": "The pack's arena.json presentation_defaults.scatter_model describes a per-axis BOX; that prose is stale (the oracle rolls the polar disc above). Logged as a pack erratum for star-lord. Layout v1 had built its floor on the box (4,670.8 m2); v2 uses the disc hull, as ruled."},
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
            "rule": "WHOLE and convex: EXACTLY the convex hull of the six 8 m scatter discs + 1 m (each anchor buffered 9 m, sampled at 1 deg)",
            "polygon": G.rnd(floor),
            "z_m": 0.0,
            "area_m2": G.rnd(G.area(floor), 2),
            "extents": {k: G.rnd(v, 3) for k, v in G.extents(floor).items()},
            "superseded_box_hull_info": {"rule": "layout v1's floor (hull of the 8 m boxes + 1 m), superseded; INFO only",
                                         "area_m2": G.rnd(G.area(box_floor), 2),
                                         "extents": {k: G.rnd(v, 3) for k, v in G.extents(box_floor).items()}},
            "edge_by_biome": {"N": "the barrow slope (mound toe, door, standing stones)", "W": "the shore: shingle into shore ice, the wreck",
                              "S/SSE": "the cliff lip (the floor edge IS the lip); the sea cave below, the stair", "E/SE": "the hall yard: hall wall, palisade (pulled back), the fallen gable"},
            "walkover_max_h_m": WALKOVER_MAX_H_M,
        },
        "land": {"polygon": G.rnd(land), "z_top_m": 0.0, "z_cliff_foot_m": STAIR["sea_z_m"],
                 "cliff_lip": G.rnd(lip), "note": "the headland: the floor's southern chain is the cliff lip; land continues N (barrow) and E (hall yard) outside the walkable edge"},
        "shore_ice": {"polygon": G.rnd(shore_ice), "z_m": -0.4, "note": "shore ice W and SW of the land, outside the edge"},
        "sea": {"z_m": STAIR["sea_z_m"], "extent": [[-90.0, -90.0], [90.0, 90.0]]},
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
