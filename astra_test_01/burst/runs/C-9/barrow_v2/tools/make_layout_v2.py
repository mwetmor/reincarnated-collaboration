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

import numpy as np
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bv2_geom as G  # noqa: E402
import sculpt_v2 as SC  # noqa: E402

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
# R-C9-154 (Matt): every deliverer opening sized to the largest monster it delivers. The sea cave must be
# ~7 m high x 9 m wide, so the cliff goes back to ~7.5 m (sea -7.5, ledge -7.2); the stair widens to 5 m and
# steepens to 34.7 deg (still <= 35) so the flight + the 9 m mouth fit along the face under p03's patch.
STAIR = {"width_m": 5.0, "drop_m": 7.2, "step_rise_m": 0.18, "step_tread_m": 0.26, "sea_z_m": -7.5,
         "tangent_beta_deg": 78.0,   # beta from +x toward +y about p03; p03's own arc is 41.8..117.8 deg
         "cave_w_m": 9.0, "cave_h_m": 6.9, "cave_gap_m": 0.4,
         "top_landing_depth_m": 2.0, "bottom_landing_depth_m": 3.0}
BARROW = {"open_w": 5.0, "open_h": 6.5, "post_w": 1.4, "post_d": 1.8, "lintel_t": 1.3, "forecourt": 2.6,
          "mound_a": 20.0, "mound_b": 13.5, "rise": 10.5, "passage_len": 9.0,
          "sized_for": "yeti nemesis, ~5.6 m tall (the bosses' door)"}
PORCH = {"open_w": 4.5, "open_h": 4.5, "width": 6.4, "depth": 3.0, "eave": 5.1, "ridge": 7.8, "apron": 1.4,
         "sized_for": "colossus 3.2 m; statues ~3.5 m; crab heroes up to ~3.4 m wide"}


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
    disc_hull = G.offset_hull(list(A.values()), h + FLOOR_MARGIN_M, n=360)
    box_floor = G.offset_hull(box_corners, FLOOR_MARGIN_M, n=96)
    # R-C9-149a (Matt) BIOME-SCULPT: the walkable edge becomes ORGANIC. The disc hull + 1 m is the INNER
    # bound; the edge bulges outward per biome (sculpt_v2.organic_floor). It stays flush (cap 0) where the
    # stair lands and the cave sits; the bulge is capped small at the deliverers so their doors stay close.
    _p3 = A["p03"]
    _R9 = h + FLOOR_MARGIN_M

    def _arc(beta_deg, r=_R9):
        return (_p3[0] + r * math.cos(math.radians(beta_deg)), _p3[1] + r * math.sin(math.radians(beta_deg)))
    _p4, _p6 = A["p04"], A["p06"]
    _ax = unit(_p6[0] - _p4[0], _p6[1] - _p4[1])
    _nT = (-_ax[1], _ax[0])
    if _nT[0] * _p4[0] + _nT[1] * _p4[1] < 0:
        _nT = (-_nT[0], -_nT[1])
    _cw = _nT[0] * _p4[0] + _nT[1] * _p4[1] + _R9

    def _onedge(pid):
        d_ = unit(*A[pid])
        return along((0, 0), d_, _cw / (d_[0] * _nT[0] + d_[1] * _nT[1]))
    # (R-C9-154) the great door + porch move NE along the hall wall to where the p04 arc has fallen away
    # far enough for the grown porch + its stone apron to stay outside the floor: the first station from
    # p04's ray at which the porch+apron clears the disc hull by >= 0.75 m (0.35 m bulge cap + 0.4 m)
    _ane = (-_ax[0], -_ax[1])
    _wall = _cw + 1.5
    _d4 = unit(*A["p04"])
    _D0 = along((0, 0), _d4, _wall / (_d4[0] * _nT[0] + _d4[1] * _nT[1]))
    _nin0 = (-_nT[0], -_nT[1])
    PORCH["station"] = None
    for k_ in range(0, 80):
        st_ = k_ * 0.25
        pc_ = along(_D0, _ane, st_)
        hw_ = PORCH["width"] / 2
        dd_ = PORCH["depth"] + PORCH["apron"]
        fp_ = [along(pc_, _ane, -hw_), along(pc_, _ane, hw_), along(along(pc_, _ane, hw_), _nin0, dd_), along(along(pc_, _ane, -hw_), _nin0, dd_)]
        clr_ = min(-G.signed_clearance(q, disc_hull) for q in fp_ + [along(fp_[2], _ane, -t_) for t_ in (1.0, 2.0, 3.0, 4.0, 5.0)])
        if clr_ >= 0.75:
            PORCH["station"] = st_
            PORCH["centre0"] = pc_
            break
    assert PORCH["station"] is not None, "no station on the hall wall clears the grown porch"
    _p3arc = lambda b_: _arc(b_)
    protect = [(*_arc(STAIR["tangent_beta_deg"]), 6.5, 0.0), (*_arc(46.0), 2.5, 0.0), (*_arc(121.0), 7.0, 0.6),
               (*along(PORCH["centre0"], _nin0, 2.0), 6.5, 0.35),
               (*along((0, 0), unit(*A["p02"]), ray_exit(disc_hull, unit(*A["p02"]))), 9.0, 0.5),
               (*along((0, 0), unit(*A["p01"]), ray_exit(disc_hull, unit(*A["p01"]))), 4.0, 0.5),
               (*_onedge("p06"), 4.0, 0.4)]
    floor, bulge, organic_info = SC.organic_floor(disc_hull, protect, _p3)

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
    # (R-C9-154) a MONUMENTAL door: a clear opening of open_w x open_h between massive uprights under a
    # lintel, set back behind a paved forecourt, a deep passage cut into a larger mound, a stepped kerb
    door_plane = e2 + 0.3 + BARROW["forecourt"]                    # the uprights' front face, on p02's ray
    door_c = along((0, 0), d2, door_plane + BARROW["post_d"] / 2)
    mound_c = along((0, 0), d2, door_plane - 0.6 + BARROW["mound_b"])
    rot2 = math.degrees(math.atan2(n2[1], n2[0]))
    _cr, _sr = math.cos(math.radians(rot2)), math.sin(math.radians(rot2))
    mound_outline = []
    for k in range(96):
        th = G.TAU * k / 96
        rr = 1.0 + 0.07 * math.sin(3 * th + 0.4) + 0.05 * math.sin(5 * th + 1.9) + 0.03 * math.sin(9 * th)
        uu, vv = rr * math.cos(th) * BARROW["mound_a"], rr * math.sin(th) * BARROW["mound_b"]
        mound_outline.append((mound_c[0] + uu * _cr - vv * _sr, mound_c[1] + uu * _sr + vv * _cr))
    feat("barrow_mound", "mound", mound_outline, 0.0, BARROW["rise"], True,
         "the King's barrow: a large grassy mound, kerbed; the passage is cut deep into it behind the door",
         shape={"type": "ellipsoid_cap", "centre": G.rnd(mound_c), "semi_axes_m": [BARROW["mound_a"], BARROW["mound_b"]], "rot_deg": G.rnd(rot2), "rise_m": BARROW["rise"]})
    _bw = BARROW["open_w"] + 2 * BARROW["post_w"] + 0.8
    feat("barrow_door", "door", G.rect_poly(*door_c, _bw, BARROW["post_d"], rot2), 0.0, BARROW["open_h"] + BARROW["lintel_t"], True,
         "the King's door, MONUMENTAL (R-C9-154): two massive uprights and a lintel framing a %.1f m wide x %.1f m high clear opening (sized for the %s), behind a %.1f m paved forecourt; the passage runs %.0f m into the mound (p02, bosses: mist + rise from the grave-ground)" % (
             BARROW["open_w"], BARROW["open_h"], BARROW["sized_for"], BARROW["forecourt"], BARROW["passage_len"]),
         faces_deg=G.rnd(G.compass_deg(-d2[0], -d2[1]), 2),
         opening={"clear_w_m": BARROW["open_w"], "clear_h_m": BARROW["open_h"], "sized_for": BARROW["sized_for"],
                  "required": {"h_min_m": 6.5, "w_min_m": 5.0}})
    feat("barrow_forecourt", "forecourt", [along(along((0, 0), d2, e2 + 0.35), n2, -_bw / 2 - 0.6), along(along((0, 0), d2, e2 + 0.35), n2, _bw / 2 + 0.6),
                                           along(along((0, 0), d2, door_plane), n2, _bw / 2 + 0.6), along(along((0, 0), d2, door_plane), n2, -_bw / 2 - 0.6)],
         0.0, 0.12, True, "the paved forecourt before the King's door (flush flagstones), outside the walkable edge", blocks=False)
    for i, (t, s, ht) in enumerate(((e2 + 4.5, -13.5, 2.6), (e2 + 4.0, 13.0, 2.2), (e2 + 15.0, -21.5, 2.0), (e2 + 14.0, 21.0, 2.4))):
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
    GABLE_BACK, GABLE_FWD = 2.0, 4.0
    D_ray = D                                                   # where p04's ray meets the wall (v4's door)
    D = along(D, ax_ne, PORCH["station"])                         # (R-C9-154) the great door's station
    NE_PAST_DOOR = PORCH["width"] / 2 + 3.5
    L_GD = math.dist(Gp, D)
    rot_ax = math.degrees(math.atan2(ax_ne[1], ax_ne[0]))
    feat("longhall", "hall", hall_rect(GABLE_FWD, L_GD + NE_PAST_DOOR, Gp), 0.0, 6.5, True,
         "the burnt longhall: ONE building angled NE -> SW along the floor edge between p04 and p06; its long west wall faces the floor 1.5 m beyond the edge; roof half fallen",
         axis_compass_deg_sw=G.rnd(G.compass_deg(*ax_sw), 2), length_m=G.rnd(L_GD + NE_PAST_DOOR + GABLE_BACK, 2), depth_m=HALL_D)
    feat("hall_great_door", "door", G.rect_poly(*along(D, nT, 0.3), PORCH["open_w"] + 0.6, 0.6, rot_ax), 0.0, PORCH["open_h"] + 0.3, True,
         "the hall's GREAT door (R-C9-154): a %.1f m wide x %.1f m high clear opening (sized for the %s), in the long west wall %.2f m NE of p04's ray, where the p04 arc falls away enough for the grown porch (p04: out of smoke)" % (
             PORCH["open_w"], PORCH["open_h"], PORCH["sized_for"], PORCH["station"]),
         faces_deg=G.rnd(G.compass_deg(-nT[0], -nT[1]), 2),
         opening={"clear_w_m": PORCH["open_w"], "clear_h_m": PORCH["open_h"], "sized_for": PORCH["sized_for"],
                  "required": {"h_min_m": 4.5, "w_min_m": 4.5}}, station_ne_of_p04_ray_m=PORCH["station"])
    # the great door's gabled PORCH (BVP's bvp_porch.py form, GROWN by R-C9-154): it rises above the hall's
    # roofline (ridge 7.8 m vs the hall's ~6.4 m), carved gable finials, braziers either side, a stone apron
    PORCH["shift_ne"] = 0.0
    _pc = D
    _nin = (-nT[0], -nT[1])
    _hw = PORCH["width"] / 2
    porch_fp = [along(_pc, ax_ne, -_hw), along(_pc, ax_ne, _hw), along(along(_pc, ax_ne, _hw), _nin, PORCH["depth"]),
                along(along(_pc, ax_ne, -_hw), _nin, PORCH["depth"])]
    feat("hall_porch", "porch", porch_fp, 0.0, PORCH["ridge"] + 1.2, True,
         "the great door's gabled porch, GROWN (R-C9-154): %.1f x %.1f m, eaves %.1f m, ridge %.1f m running OUT toward p04's patch, ABOVE the hall's roofline; carved finials on its gable; the double doors stand open; smoke rolls out (p04: out of smoke)" % (
             PORCH["width"], PORCH["depth"], PORCH["eave"], PORCH["ridge"]),
         opening={"clear_w_m": PORCH["open_w"], "clear_h_m": PORCH["open_h"], "between": "the front posts, under the eave beam"},
         eave_z_m=PORCH["eave"], ridge_z_m=PORCH["ridge"], mouth_centre=G.rnd(along(_pc, _nin, PORCH["depth"])),
         faces_deg=G.rnd(G.compass_deg(*_nin), 2), source="lane BVP tools/bvp_porch.py (folded in by BX, option a)")
    _ap0 = along(_pc, _nin, PORCH["depth"])
    apron_fp = [along(_ap0, ax_ne, -_hw), along(_ap0, ax_ne, _hw), along(along(_ap0, ax_ne, _hw), _nin, PORCH["apron"]),
                along(along(_ap0, ax_ne, -_hw), _nin, PORCH["apron"])]
    feat("hall_apron", "apron", apron_fp, 0.0, 0.15, True, "the porch's short stone apron (flush), outside the walkable edge", blocks=False)
    braziers = []
    for sv in (-1, 1):
        bc_ = along(along(_pc, ax_ne, sv * (_hw + 0.9)), _nin, PORCH["depth"] * 0.55)
        braziers.append(bc_)
        feat(f"brazier_{'sw' if sv < 0 else 'ne'}", "brazier", G.ellipse_poly(*bc_, 0.55, 0.55, 0, 12), 0.0, 2.3, True,
             "a fire brazier beside the porch")
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
    # (R-C9-154) the cave mouth (9 m wide, ~7 m high) and the ledge follow the ACTUAL floor boundary
    # westward from the stair's foot: offsets along the boundary's outward normals, so they stay outside
    # the (organic) floor however the lip bites.
    nF = len(floor)
    i_foot = min(range(nF), key=lambda i: math.dist(floor[i], B_b))
    cmp_next = G.compass_deg(*floor[(i_foot + 1) % nF]) - G.compass_deg(*floor[i_foot])
    step_w = 1 if cmp_next > 0 else -1                          # walk toward increasing compass (west)

    def walk(L0, L1):
        """(point, outward normal) samples along the boundary from arc length L0 to L1 west of the foot."""
        out_, Lacc, i = [], 0.0, i_foot
        while Lacc <= L1 + 1e-9:
            if Lacc >= L0 - 1e-9:
                a_, b_ = floor[(i - step_w) % nF], floor[(i + step_w) % nF]
                tx_, ty_ = b_[0] - a_[0], b_[1] - a_[1]
                Lt = math.hypot(tx_, ty_) or 1.0
                nx_, ny_ = ty_ / Lt, -tx_ / Lt
                if nx_ * floor[i][0] + ny_ * floor[i][1] < 0:
                    nx_, ny_ = -nx_, -ny_
                out_.append((floor[i], (nx_, ny_)))
            j = (i + step_w) % nF
            Lacc += math.dist(floor[i], floor[j])
            i = j
        return out_
    gap = STAIR["cave_gap_m"]
    cave_s = walk(gap, gap + STAIR["cave_w_m"] + 1.0)
    cave_poly = [along(p_, n_, 0.06) for p_, n_ in cave_s] + [along(p_, n_, 0.45) for p_, n_ in reversed(cave_s)]
    led_s = walk(0.0, gap + STAIR["cave_w_m"] + 1.6)
    ledge = [along(p_, n_, 0.03) for p_, n_ in reversed(led_s)] + [B_n, B_s] + [along(p_, n_, 5.5) for p_, n_ in led_s[1:]]
    cave_mid = cave_s[len(cave_s) // 2][0]
    cave_w_meas = sum(math.dist(cave_s[i][0], cave_s[i + 1][0]) for i in range(len(cave_s) - 1))
    slope_deg = math.degrees(math.atan2(STAIR["drop_m"], run))
    run_up = u
    to_c = unit(-T_n[0], -T_n[1])
    stair = {
        "id": "sea_cave_stair", "kind": "stair",
        "_ruling": "R-C9-145 (Matt) + R-C9-148 (Matt, from the walk film: 'the stairs seem to be below the sea cave which doesnt make alot of sense'): the cave sits in the MAIN south cliff face under p03's patch with a ledge at sea level; a straight stair (5.0 m wide since R-C9-154) climbs FROM that ledge UP the face to a top landing flush with the floor edge at p03's patch; open on the sea side; its run angles across the face (the 'aligned to centre' rule is dropped by R-C9-148); climbers turn toward the centre on the landing",
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
    feat("sea_cave_mouth", "cave", cave_poly, ledge_z, ledge_z + STAIR["cave_h_m"], True,
         "the sea-cave mouth (R-C9-154): %.1f m wide x %.1f m high in the MAIN south cliff face under p03's patch, at the stair's foot, on the sea-level ledge; it follows the lip; a %.1f m rock lintel stays above it (sized for the servitor insectoids 4-8 m long and the 5.6 m nemesis)" % (
             cave_w_meas, STAIR["cave_h_m"], STAIR["drop_m"] - STAIR["cave_h_m"]),
         faces_deg=G.rnd(G.compass_deg(*cave_mid), 2),
         opening={"clear_w_m": G.rnd(cave_w_meas, 3), "clear_h_m": STAIR["cave_h_m"], "sized_for": "servitor insectoids 4-8 m long; the 5.6 m nemesis",
                  "required": {"h_min_m": 6.5, "w_min_m": 9.0}})

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
        stones.append(feat(f"circle_stone_{i + 1}", "fallen_stone", poly, 0.0, ht, False, form, blocks=False,
                           sculpt_stone={"c": G.rnd(c), "len": 0.6 if i in (2, 5) else 1.8, "wid": 0.5 if i in (2, 5) else 0.75,
                                         "rot": G.rnd(i * 23 if i in (2, 5) else math.degrees(ang) + 90 + 25 * ((i % 3) - 1), 2)}))
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
    # R-C9-149a: the coastline is organic too. The land is star-shaped about the start: sampled every
    # 0.5 deg of compass, its radius is
    #   S (145..215 deg): the floor's own edge -- the broken cliff lip;
    #   W (215..335): the floor's edge + a ragged shingle beach (3-8 m), with the shore ice beyond;
    #   N/E (335..100): far (the barrow slopes, the groves);
    #   SE (100..145): the hall yard's headland, closing in to the lip at Q (145 deg) along a ragged coast.
    _rng = np.random.default_rng(1492)
    _ph = _rng.uniform(0, G.TAU, 8)

    def _floor_r(cdeg):
        uu = unit(math.sin(math.radians(cdeg)), -math.cos(math.radians(cdeg)))
        return ray_exit(floor, uu), uu

    def _wrap(d):
        return d % 360.0
    land, lip, ice_outer, ice_inner = [], [], [], []
    for k in range(720):
        cdeg = k * 0.5
        rf, uu = _floor_r(cdeg)
        t = math.radians(cdeg)
        if 145.0 <= cdeg <= 215.0:
            r = rf
        elif 215.0 < cdeg < 345.0:
            ramp = min(1.0, (cdeg - 215.0) / 12.0)
            beach = 5.5 + 1.8 * math.sin(7 * t + _ph[0]) + 1.0 * math.sin(17 * t + _ph[1]) + 0.5 * math.sin(41 * t + _ph[2])
            sweep = 0.0 if cdeg < 298.0 else 95.0 * ((cdeg - 298.0) / 47.0) ** 1.3 * (1 + 0.08 * math.sin(23 * t + _ph[7]))
            r = rf + ramp * beach + sweep
            iw_ = (18.0 + 6.0 * math.sin(5 * t + _ph[3]) + 3.0 * math.sin(13 * t + _ph[4])) * (1 + 1.5 * max(0.0, (cdeg - 298.0) / 47.0))
            ice_outer.append(along((0, 0), uu, r + iw_ * min(1.0, (cdeg - 215.0) / 8.0)))
            ice_inner.append(along((0, 0), uu, r - 0.05))
        elif 95.0 < cdeg < 145.0:
            f_ = (145.0 - cdeg) / 40.0
            coast = 95.0 * min(1.0, f_) ** 1.0 * (1 + 0.10 * math.sin(19 * t + _ph[6])) + \
                (2.0 + 1.5 * math.sin(11 * t + _ph[5]) + 0.8 * math.sin(29 * t + _ph[6])) * min(1.0, f_ * 6)
            r = rf + coast
        else:
            r = 130.0
        pt = along((0, 0), uu, r)
        land.append(pt)
        if 145.0 <= cdeg <= 215.0:
            lip.append(pt)
    lip = list(reversed(lip))                     # W -> E, as before (215 -> 145 deg)
    shore_ice = ice_outer + list(reversed(ice_inner))
    xw, yw = lip[0]
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
        {"id": "V2_p02_barrow_door", "target": G.rnd(along((0, 0), d2, e2 + 2.5)), "what": "p02's patch and the King's door"},
        {"id": "V3_p01_wreck", "target": G.rnd(along((0, 0), d1, e1 - 5.0)), "what": "p01's patch on the shingle and the wreck's rail"},
        {"id": "V4_p04_hall_door", "target": G.rnd(along(_pc, _nin, PORCH["depth"] + 4.0)), "what": "p04's patch in the hall yard and the great door"},
        {"id": "V5_p06_fallen_gable", "target": G.rnd(along((0, 0), d6, e6 - 4.0)), "what": "p06's patch in the ash and the fallen gable"},
        {"id": "V6_p05_mere", "target": G.rnd((A["p05"][0] - 3.0, A["p05"][1] - 3.0)), "what": "the frozen mere over p05, the stream mouth, the circle's W stones"},
        {"id": "V7_p03_stair_top", "target": G.rnd(along(((M[0] + cave_mid[0]) / 2, (M[1] + cave_mid[1]) / 2), nh, 3.0)), "what": "the sea cave at the stair's foot, the stair rising up the cliff face to the top landing flush with p03's patch"},
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
            "rule": "WHOLE (one simple polygon, no holes) and ORGANIC (R-C9-149a): it CONTAINS the convex hull of the six 8 m scatter discs + 1 m (the minimum, the conductor's ruling) and bulges outward from it per biome; nothing inside it blocks",
            "min_disc_hull": {"rule": "the convex hull of the six 8 m discs + 1 m (each anchor buffered 9 m, sampled at 1 deg): the floor's INNER bound",
                              "polygon": G.rnd(disc_hull), "area_m2": G.rnd(G.area(disc_hull), 2),
                              "extents": {k: G.rnd(v, 3) for k, v in G.extents(disc_hull).items()}},
            "organic": organic_info,
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
    # ================= R-C9-149a BIOME-SCULPT: terrain, rocks, groves, ruined man-made pieces, ground detail =================
    def _rect_mid(fp):
        return (((fp[0][0] + fp[3][0]) / 2, (fp[0][1] + fp[3][1]) / 2), ((fp[1][0] + fp[2][0]) / 2, (fp[1][1] + fp[2][1]) / 2))
    _hall_sw = along(Gp, ax_ne, -GABLE_BACK)
    _hall_len = L_GD + NE_PAST_DOOR + GABLE_BACK
    _pad = [along(along(_hall_sw, ax_ne, -2.5), nT, -0.5), along(along(_hall_sw, ax_ne, _hall_len + 2.5), nT, -0.5),
            along(along(_hall_sw, ax_ne, _hall_len + 2.5), nT, HALL_D + 2.5), along(along(_hall_sw, ax_ne, -2.5), nT, HALL_D + 2.5)]
    _foot = []
    for cdeg in list(range(172, 250, 9)) + [124, 132]:
        uu = unit(math.sin(math.radians(cdeg)), -math.cos(math.radians(cdeg)))
        _foot.append(along((0, 0), uu, ray_exit(floor, uu) + 3.6))
    ctx = {
        "bank_gaps": [along(_pc, _nin, PORCH["depth"]), along(Gp, ax_ne, 1.0)],
        "mound": {"c": mound_c, "a": BARROW["mound_a"], "b": BARROW["mound_b"], "rot": rot2, "rise": BARROW["rise"]},
        "passage": {"c": along((0, 0), d2, door_plane), "door": along((0, 0), d2, door_plane), "u": d2, "v": n2,
                    "half_w": BARROW["open_w"] / 2 + 0.1, "len": BARROW["passage_len"] + BARROW["post_d"],
                    "forecourt_back": BARROW["forecourt"] + 0.3, "forecourt_half_w": _bw / 2 + 0.6, "barrow": BARROW},
        "braziers": braziers, "apron": apron_fp,
        "clear_zones": [ledge, cave_poly, [T_n, T_s, B_s, B_n], landing],
        "cave_frame": [(G.rnd(p_), G.rnd(n_)) for p_, n_ in cave_s],
        "hall_pad": _pad,
        "wall_rock": wall_rock,
        "rock_clusters": [(-25, -40, 6, 1.2), (30, -38, 5, 1.4), (-8, -57, 4, 1.6), (41, -23, 5, 1.1), (52, -48, 6, 1.5),
                          (62, 10, 5, 1.3), (58, 41, 4, 1.2), (-40, -21, 5, 1.2), (-30, -56, 4, 1.4), (-52, -8, 5, 0.9),
                          (-50, 30, 4, 1.0), (24, -62, 4, 1.3), (64, -34, 4, 1.2), (-44, -36, 3, 1.0)],
        "cliff_foot_rocks": _foot,
        "floes": [(-35, 48), (-25, 55), (-12, 58), (-45, 52), (-55, 47), (30, 54), (45, 52), (56, 50), (5, 60), (-20, 46)],
        "groves": [(34, -52, "birch", 8, 4.0), (-14, -63, "birch", 7, 4.0), (63, -18, "birch", 6, 3.0), (20, -60, "juniper", 6, 3.0),
                   (-33, -37, "juniper", 5, 2.5), (50, -31, "juniper", 5, 3.0), (61, 31, "juniper", 4, 2.5), (-44, -48, "juniper", 4, 2.0),
                   (46, -10, "juniper", 3, 1.5)],
        "standing_stones": [(G.rnd(tuple(sum(q[i] for q in f["footprint"]) / 4 for i in (0, 1))), f["z_top_m"]) for f in feats if f["kind"] == "standing_stone"],
        "wreck": {"c": hull_c, "rot": 90.0 - 12.0, "length": 17.0, "z": -0.25},
        "hall": {"sw": _hall_sw, "ane": ax_ne, "nT": nT, "door": D, "length": _hall_len, "depth": HALL_D,
                 "gable_len": GABLE_BACK + GABLE_FWD, "door_s": GABLE_BACK + L_GD, "porch": PORCH},
        "palisade_runs": [_rect_mid(f["footprint"]) for f in feats if f["kind"] == "palisade"],
        "circle_stones": [dict(f["sculpt_stone"], z_top_m=f["z_top_m"]) for f in feats if "sculpt_stone" in f],
    }
    B = SC.Builder(layout, ctx)
    Hf = B.terrain()
    hf_rel = "godot/data/terrain_h.f32"
    SC.write_heightfield(B.H, os.path.join(ROOT, hf_rel))
    B.dressing()
    # the simple interior pieces re-made organic (their validator footprints are unchanged)
    for f in feats:
        fp = f["footprint"]
        cx_ = sum(q[0] for q in fp) / len(fp)
        cy_ = sum(q[1] for q in fp) / len(fp)
        if f["kind"] == "grave_marker":
            B.blob("stone", (cx_, cy_), 0.32, 0.17, f["z_top_m"], -0.2, float(B.rng.uniform(0, 180)), (0.46, 0.44, 0.41), "rock")
        elif f["kind"] in ("driftwood", "beam"):
            (a_, b_) = _rect_mid(fp)
            col = (0.55, 0.47, 0.37) if f["kind"] == "driftwood" else (0.14, 0.12, 0.11)
            B.beam((a_[0], a_[1], 0.12), (b_[0], b_[1], 0.14), 0.32, 0.22, col, f["kind"])
        elif f["kind"] == "rock":
            r_ = max(math.dist(fp[0], (cx_, cy_)), 0.6) * 0.9
            B.blob("rock", (cx_, cy_), r_, r_ * 0.8, f["z_top_m"], -0.5, float(B.rng.uniform(0, 180)), (0.50, 0.49, 0.47), "rock")
    gd_counts = B.ground_detail()
    SCULPT_KINDS = {"mound", "door", "standing_stone", "wreck", "mast", "rock", "hall", "gable", "palisade", "fallen_stone",
                    "grave_marker", "driftwood", "beam", "porch", "forecourt", "apron", "brazier"}
    for f in feats:
        f["render"] = "sculpt" if f["kind"] in SCULPT_KINDS else "prism"
    feats.extend(B.features)
    layout["sculpt"] = {
        "_what": "R-C9-149a BIOME-SCULPT (tools/sculpt_v2.py): the greybox's real shape. Rendered by godot/scripts/barrow_v2_greybox.gd; proved by tools/validate_layout_v2.py (beams/blobs taller than walk-over lie outside the floor; the heightfield is exactly 0 on it).",
        "heightfield": {"file": hf_rel, "format": "float32 little-endian, row-major, rows y0 -> y1 (north -> south), cols x0 -> x1",
                        "px_per_m": SC.HF_PPM, "shape": [int(B.H.shape[0]), int(B.H.shape[1])], "extent_sim_m": SC.EXT,
                        "sha256": sha256(os.path.join(ROOT, hf_rel)), "sea_floor_z_m": SC.SEA_FLOOR_Z},
        "blobs": B.blobs, "beams": B.beams,
        "ground_detail_counts": gd_counts,
        "counts": {"blobs": len(B.blobs), "beams": len(B.beams), "sculpt_features": len(B.features)},
    }
    out = os.path.join(ROOT, "layout_v2.json")
    with open(out, "w") as f:
        json.dump(layout, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote", out, "floor area", round(G.area(floor), 1), "features", len(feats))


if __name__ == "__main__":
    main()
