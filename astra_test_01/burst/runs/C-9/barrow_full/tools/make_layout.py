#!/usr/bin/env python3
"""C-9 T10-2 step 1 -- THE FROST KING'S BARROW, FULL AREA: the layout, from the spec table (v2).

Contract: agentic_orchestration/gandalf/notes/2026-09-29-barrow-full-area-blockout-spec.md, v2
(corrected after blockout v1, commit 1e4cf69c2). This file turns that table into ONE layout that
everything downstream reads: the Godot scene builds from it, the map is drawn from it, and the
acceptance numbers are measured against it. Nothing about the layout is decided anywhere else.

WHAT IS THE SPEC'S AND WHAT IS MINE is kept apart in the output:
  * `spec_uv`  -- the table's own number, verbatim (null for a piece the table does not place);
  * `uv`       -- the point actually used. Equal to spec_uv unless a deviation says otherwise.
Pieces the table implies but does not place carry `derived_from`.

FRAME. (u, v) are true metres on the ground, +u screen-right and +v up-screen, both from the
play camera's own basis (pitch 52.95354112560294, yaw 47) projected onto the ground:
    u_hat = ( cos47, 0, -sin47)      v_hat = (-sin47, 0, -cos47)      world = u*u_hat + v*v_hat
The arena is centred at (0, 1); the origin is only the origin (spec v2 § 1).

THE WINDOW (v2) is the 4 x 4 paint-chunk grid, 5376 x 3328 px, centred at (-2, -3).

THE CAMERA MARGIN RULE, AND THE PART OF IT THE SPEC'S NUMBERS LEAVE OUT. The play camera is
centred on him with a 55 px LIFT (barrow_world's CAM_LIFT_PX: he stands 55 px below frame
centre), so the frame reaches 960 px across, 595 px up-screen and 485 px down-screen from his
feet -- 9.54 m, 7.41 m and 6.04 m of ground. The spec's 6.72 m is the symmetric half-height.
So every reachable point must lie in u [-19.17, 15.17], v [-17.68, 10.31], and that box is what
routes the bounds: the right wall comes in to u 15.35, the top wall down to v 10.6, the door's
threshold stops him by v 10.10.

Outputs (all regenerated on every run; the .bin is gitignored and this script is its source):
    ../barrow_full_layout.json            the design layout (finalize.py merges the built numbers in)
    ../godot/data/barrow_full_layout.json the copy the scene reads
    ../godot/data/barrow_full_splat.bin   the ground-tint weight map (world-xz raster), PNG bytes
"""
import hashlib
import json
import math
import pathlib
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import geom2d as G  # noqa: E402

ROOT = HERE.parent
GODOT = ROOT / "godot"
VERSION = 2

# --- the frame -----------------------------------------------------------------------------
PPM = 100.617553710938                    # px per metre across the screen (the project's own)
PITCH_DEG = 52.95354112560294             # R-C9-68
YAW_DEG = 47.0
SP = math.sin(math.radians(PITCH_DEG))
CP = math.cos(math.radians(PITCH_DEG))
COT = CP / SP                             # a vertical metre's up-screen shift in ground metres
PX_UP = PPM * SP                          # px per ground metre up-screen = 80.3076
CY = math.cos(math.radians(YAW_DEG))
SY = math.sin(math.radians(YAW_DEG))
GUIDE_PX = (5376, 3328)
WIN_CENTRE = (-2.0, -3.0)
U_HALF = GUIDE_PX[0] / 2.0 / PPM          # 26.7150 m
V_HALF = GUIDE_PX[1] / 2.0 / PX_UP        # 20.7202 m
WIN_U = (WIN_CENTRE[0] - U_HALF, WIN_CENTRE[0] + U_HALF)
WIN_V = (WIN_CENTRE[1] - V_HALF, WIN_CENTRE[1] + V_HALF)
CHUNK = {"cols": 4, "rows": 4, "canvas_px": [1536, 1024], "stride_px": [1280, 768]}
# the play camera, as barrow_world frames it at 1920 x 1080
CAM_LIFT_PX = 55.0
FRAME_HALF_U = 960.0 / PPM
FRAME_UP = (540.0 + CAM_LIFT_PX) / PX_UP
FRAME_DOWN = (540.0 - CAM_LIFT_PX) / PX_UP
REACH_U = (WIN_U[0] + FRAME_HALF_U, WIN_U[1] - FRAME_HALF_U)
REACH_V = (WIN_V[0] + FRAME_DOWN, WIN_V[1] - FRAME_UP)
CAPSULE_R = 0.35
WALL_HALF_T = 0.15


def uv_to_xz(u, v):
    return (u * CY - v * SY, -u * SY - v * CY)


def xz_to_uv(x, z):
    return (x * CY - z * SY, -x * SY - z * CY)


def r3(x):
    return round(float(x), 4)


# --- asset sizes -------------------------------------------------------------------------------
BA = json.loads((HERE / "barrow_assets.src.json").read_text())["models"]
KA = json.loads((HERE / "kit_assets.src.json").read_text())["models"]
LIB = json.loads((HERE / "footprint_lib.json").read_text())   # local hulls measured on v1

# --- the spec table (v2), verbatim ------------------------------------------------------------
MOUND = {"centre": (0.0, 13.0), "axes": (12.0, 9.0), "rise_about": 4.0}
RING = {"centre": (0.0, 2.0), "r": 9.0}
RING_STONES = [  # theta (clockwise from +v), class, note
    (155, "stone_tall", "gate stone"), (-155, "stone_tall", "gate stone"),
    (135, "stone_mid", ""), (-135, "stone_mid", ""),
    (115, "stone_short", ""), (-115, "stone_short", ""),
    (95, "stone_tall", ""), (-95, "stone_tall", "FALLEN, lying outward"),
    (75, "stone_mid", ""), (-75, "stone_mid", ""),
    (55, "stone_tall", "the raven's perch"), (-55, "stone_tall", ""),
    (35, "stone_short", "at the mound's foot"), (-35, "stone_short", "at the mound's foot"),
]
ARENA = {"centre": (0.0, 1.0), "r": 7.0}
PATH = {"points": [(0.0, -6.2), (-1.0, -10.0), (-3.0, -16.0)], "width": 4.0}
TARN = {"centre": (-13.5, -5.0), "axes": (12.0, 9.0)}
OUTCROPS = [(17, -12), (18, -3), (17, 6), (10, -15), (-19, -13), (-19, 4), (-13, 13), (13, 13)]
COVER = {"uv": (-12.5, 4.7), "size": (3.0, 2.0), "h": 1.4}
GROVES = {"G1": ((7.0, -11.0), 5), "G2": ((-10.0, 9.5), 4), "G3": ((13.0, -6.0), 4),
          "G4": ((10.0, 12.0), 3)}
FALLEN_TREE = (-7.0, -12.0)
GRAVES = [(-7.0, 11.0), (7.0, 11.0)]
CAIRNS = [(2.5, -9.0), (-5.0, -14.0), (-16.0, 1.0)]
ENTRY_GAP = [(-5.0, -16.0), (-1.0, -16.0)]

# --- the choices the table leaves to the builder (each one stated) --------------------------
RING_INWARD_TURN_DEG = 20.0          # ratified on v1: +-20 toward the ring's axis
# THE MOUND. "Footprint 12 x 9 m, rise about 4.0 m, kerbed." Rise 4.2, not 4.0, and the reason
# is arithmetic, not taste: the lintel's top stands at 3.185 m (measured on v1), so the cover
# rule needs the surface at >= 3.485 m directly behind the door; the camera-margin rule needs
# the door's threshold at v <= 10.66 (him stopping 0.35 m short, frame top 7.41 m further);
# and between those two, a 4.0 m kerbed dome leaves no door position at all. 4.2 m with a
# steep kerb (exponent 0.35: 1.9 m high 5% in from the foot, flat on top) leaves ~0.25 m of
# play for the door and puts 0.41-0.48 m of mound over the lintel.
MOUND_RISE = 4.2
MOUND_EXP = 0.35
# THE KERB'S TOE. (1 - rho^2)^0.35 alone rises ~1.9 m inside the outer 5% -- one or two 0.1 m
# mesh cells -- and the faceted near-vertical face drew the pen's crease at every cell and took
# shadow acne (the first v2 capture; tools/probe_kerb.gd A/B'd shadows, pen and ramp bands).
# A smoothstep over the outer 8% of rho spreads the rise over 4-5 cells: still a steep kerb.
MOUND_TOE = 0.08
# THE DOOR, SET INTO THE MOUND: posts at v 10.6 under the lintel's ends (the manifest yaws),
# the lintel's front face at v 10.30, a stone-lined FACADE at v 10.5 behind the posts' fronts
# so the door frame stands a hand proud of it, and a CUTTING 2.6 m wide (the spec: >= 1.6 m;
# 2.6 lets the whole 2.28 m lintel be seen) from the mound's foot to the facade, floor y = 0.
DOOR_V = 10.6
POST_OFFSET_M = 0.90                 # ratified on v1: the 1.37 m opening
CUTTING = {"half_w": 1.30, "wall_t": 0.40, "v_facade": 10.5, "facade_t": 0.30, "floor_y": 0.0,
           "_walk": "walkable to the facade; the facade's collider spans the opening, so he stops IN the doorway (centre <= v 10.15)",
           "_facade_at_10_5": "on the mound's 0.1 m grid, 0.115 m behind the posts' fronts and 0.2 m behind the lintel's, so the door frame stands proud of it"}
# the passage beyond the door: SCENERY for a later interior (spec v2), reached by nobody
PASSAGE = {"half_w": 0.70, "v0": 10.5, "v_end": 12.5, "risers_v": [10.9, 11.3, 11.7], "riser_m": 0.2,
           "ceiling_y": 1.99, "walkable": False}
BIRCH_TRUNK_R = 0.22
BIRCH_YAWS = [315, 0, 270, 45, 225, 90, 180, 135]
LOG_ANGLES_DEG = (29.0, 35.0)
LOG_LEN = KA["log"]["size_m"][0]          # 2.6
# outcrops: (long, short, height, long-axis angle from +u in deg, outward (u, v)) -- O1..O8.
# The three on the right lie ACROSS the boundary (long axis along u) so their inner faces come in
# to u ~14.5-15.1 and the wall at 15.35 runs inside the rock.
OUTCROP_DIMS = {
    1: (5.0, 3.8, 2.2, 0.0, (1.0, 0.0)), 2: (5.8, 4.2, 3.0, 0.0, (1.0, 0.0)),
    3: (5.0, 3.8, 2.5, 0.0, (1.0, 0.0)), 4: (4.6, 3.6, 1.8, None, None),
    5: (5.0, 3.8, 2.0, None, None), 6: (5.4, 4.0, 2.6, None, None),
    7: (5.0, 3.8, 2.8, 0.0, (0.0, 1.0)), 8: (4.4, 3.6, 2.4, 0.0, (0.0, 1.0)),
}
# margin scenery (spec v2 § 1: "the margin beyond the play bounds is scenery, non-walkable and
# flat"): outcrops M1..M9 and birch tree lines, placed to read as land in every frame the
# camera can reach
MARGIN_OUTCROPS = [  # (u, v), long, short, h, angle deg, outward
    ((20.8, 14.4), 5.0, 3.8, 2.6, 20.0, (0.4, 1.0)), ((21.6, 1.2), 5.2, 4.0, 2.4, 90.0, (1.0, 0.0)),
    ((21.3, -17.8), 5.0, 3.8, 2.0, 30.0, (1.0, -0.6)), ((6.2, -20.6), 4.8, 3.6, 1.6, 0.0, (0.0, -1.0)),
    ((-12.8, -20.2), 5.2, 3.8, 1.7, -8.0, (0.0, -1.0)), ((-24.8, -17.4), 5.0, 3.8, 2.2, 60.0, (-0.8, -0.6)),
    ((-25.4, -5.2), 5.4, 4.0, 2.6, 90.0, (-1.0, 0.0)), ((-24.2, 9.8), 5.2, 3.8, 2.8, 70.0, (-0.8, 0.4)),
    ((-19.4, 15.2), 4.6, 3.6, 2.4, 10.0, (0.0, 1.0)),
]
TREE_LINES = {  # (start, end, n): birches along a line, jittered, in the margin
    "TL_top_right": ((15.8, 12.4), (24.0, 16.6), 3), "TL_right": ((23.4, -11.5), (23.0, 7.5), 4),
    "TL_bottom_right": ((10.5, -22.4), (16.5, -21.2), 2), "TL_bottom_left": ((-22.8, -22.2), (-9.0, -22.6), 3),
    "TL_left": ((-27.2, -13.0), (-27.4, 5.5), 3), "TL_top_left": ((-27.0, 14.0), (-14.5, 16.8), 3),
    "TL_behind_mound": ((-10.8, 15.4), (-7.4, 16.9), 1),
}

# THE CRUCIBLE (Matt, via the coordinator): flat decals that block nothing. Six spawn circles of
# r 1.5 on r 7.5 about the ring centre, the boss gate at the cutting's mouth, the player station.
CRUCIBLE = {
    "spawn_r_m": 1.5, "ring_r_m": 7.5, "about_uv": [0.0, 2.0], "eye_height_m": 1.70,
    "spawns": [("S1", (5.75, 6.82), "north-east, between the +55 and +35 stones"),
               ("S2", (-5.75, 6.82), "north-west, between the -55 and -35 stones"),
               ("S3", (7.05, -0.57), "east"), ("S4", (-7.05, -0.57), "west"),
               ("S5", (0.0, -5.5), "just inside the entrance: pressure from behind"),
               ("S6", (-11.5, -3.0), "out on the tarn ice: waves that rise from the frozen water")],
    "station_uv": (0.0, 1.0),
}

TINTS = {
    "snow": [0.860, 0.840, 0.800], "path": [0.580, 0.520, 0.450], "rock": [0.560, 0.555, 0.550],
    "shrub": [0.520, 0.515, 0.390], "ice": [0.700, 0.775, 0.840], "hero_grey": [0.600, 0.590, 0.570],
    "primitive_grey": [0.500, 0.480, 0.460], "mound": [0.745, 0.725, 0.665],
    "passage_dark": [0.120, 0.110, 0.105],
    "rune": [0.450, 0.780, 1.000], "boss": [0.950, 0.520, 0.200], "station": [0.980, 0.960, 0.900],
}

# --- the bounds (v2) ----------------------------------------------------------------------------
# Counter-clockwise from the entry's right post. Through O4, O5, O6 at their centres; the right
# wall at u 15.35 runs INSIDE O1-O3; the top wall at v 10.6 runs under the grave markers, G4 and
# the mound's flanks (all scenery now) and through the +-35 stones, which stand at the mound's
# foot; across the mound's front it runs inside the mound and behind the facade, so the
# cutting is inside the play area and the passage is not reachable.
BOUNDS_BASE = [(-1.0, -16.2), (10.0, -15.0), (15.35, -12.0), (15.35, -3.0), (15.35, 6.0), (15.35, 10.6),
               (7.6, 10.6), (5.1622, 9.3724), "WEDGE_R", (1.8, 10.8), (-1.8, 10.8), "WEDGE_L", (-5.1622, 9.3724), (-7.6, 10.6),
               (-12.0, 10.6), (-19.0, 4.0), (-19.0, -13.0), (-11.0, -15.9), (-5.0, -16.2)]
# THE EXIT LINE SITS AT v -16.2, 0.2 m outside the table's (-5...-1, -16). The entry gap's width
# and place are the table's; the invisible line across it moved out so cairn 2 (turned, not
# moved) clears both the path and the no-squeeze rule at the entry corner -- at -16.0 the best
# of 180 yaws left 0.035 m either way (tools: the cairn-2 yaw search in build()).


def _wedge_wall(theta, yaw):
    """THE +-35 STONES STAND AT THE MOUND'S FOOT, and between each stone and the kerb a wedge
    narrows to ~1.0 m: a dead-end notch he can step into -- a squeeze, by the v2 rule (measured
    on the first v2 build: 1.009 and 1.063 m). The wall closes it where the wedge is still 1.45 m
    wide: walking the foot from the closest approach toward the arena, the first foot point whose
    nearest stone point is 1.45 m away. The wall touches both (0.1 m into the stone, 0.2 m into
    the mound), so what is left open is >= 1.45 m everywhere."""
    s = ring_uv(theta)
    hull = placed_hull("stone_short", s, yaw)
    a_, b_ = MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
    c = MOUND["centre"]
    sgn = 1.0 if s[0] > 0 else -1.0
    ts = [-(math.pi / 2) + sgn * k * 0.002 for k in range(0, 785)]
    foot = [(c[0] + a_ * math.cos(t), c[1] + b_ * math.sin(t)) for t in ts]
    dists = [G.nearest_on(hull, q)[0] for q in foot]
    k0 = min(range(len(foot)), key=lambda k: dists[k])
    for k in range(k0, -1, -1):                      # from the closest approach toward the cutting
        if dists[k] >= 1.45:
            q = foot[k]
            _, p = G.nearest_on(hull, q)
            d = (q[0] - p[0], q[1] - p[1])
            L = math.hypot(*d)
            pin = (p[0] - d[0] / L * 0.1, p[1] - d[1] / L * 0.1)
            qin = (q[0] + d[0] / L * 0.2, q[1] + d[1] / L * 0.2)
            return [(round(pin[0], 4), round(pin[1], 4)), (round(qin[0], 4), round(qin[1], 4))], round(dists[k0], 3)
    raise SystemExit("no 1.45 m section in the +-35 wedge")


def _front_wall(sgn):
    """THE MOUND'S FRONT, BETWEEN THE CUTTING AND THE +-35 STONE, IS WALLED OFF. On the first v2
    build the stone and the kerb left a wedge that narrowed to 1.01 m (a dead-end notch -- a
    squeeze), and a chord across the wedge where it was 1.45 m wide left a 1.37 m bay beside the
    cutting instead. One straight wall from the stone to the cutting wall's front outer corner,
    0.3-0.4 m in front of the foot, closes both: he walks to the mound everywhere but along these
    3 m, where the stone stands at its foot. The vertex list runs stone -> corner on the right
    and corner -> stone on the left (counter-clockwise)."""
    hw, wt = CUTTING["half_w"], CUTTING["wall_t"]
    corner = (round(sgn * (hw + wt - 0.05), 4), round(mound_foot_v(hw + wt) - 0.3 + 0.12, 4))
    s = ring_uv(35 * sgn)
    yaw = (BA["stone_short"]["yaw_deg"] - sgn * RING_INWARD_TURN_DEG) % 360.0
    hull = placed_hull("stone_short", s, yaw)
    a_, b_ = MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
    c = MOUND["centre"]
    dmin = min(G.nearest_on(hull, (c[0] + a_ * math.cos(t), c[1] + b_ * math.sin(t)))[0]
               for t in [-(math.pi / 2) + sgn * k * 0.002 for k in range(785)])
    return ([corner] if sgn < 0 else []) + ([] if sgn < 0 else [corner]), round(dmin, 3)


def _bounds():
    out = []
    wedges = {}
    for v in BOUNDS_BASE:
        if v == "WEDGE_R":
            w, dmin = _front_wall(1.0)
            out += w
            wedges["right"] = {"wall_uv": [list(p) for p in w], "stone_to_foot_narrowest_m": dmin}
        elif v == "WEDGE_L":
            w, dmin = _front_wall(-1.0)
            out += w
            wedges["left"] = {"wall_uv": [list(p) for p in w], "stone_to_foot_narrowest_m": dmin}
        else:
            out.append(v)
    return out, wedges


BOUNDS, WEDGES = None, None
ENTRY_EDGE = None
BAND_SKIP_EDGES = None      # set by ensure_bounds(): the wedge walls, the edges inside the mound, the entry


def ensure_bounds():
    global BOUNDS, WEDGES, ENTRY_EDGE, BAND_SKIP_EDGES
    if BOUNDS is None:
        BOUNDS, WEDGES = _bounds()
        ENTRY_EDGE = len(BOUNDS) - 1
        im = [i for i, p in enumerate(BOUNDS) if p == (1.8, 10.8)][0]
        BAND_SKIP_EDGES = {im - 2, im - 1, im, im + 1, im + 2, ENTRY_EDGE}


def ring_uv(theta):
    a = math.radians(theta)
    return (RING["centre"][0] + RING["r"] * math.sin(a), RING["centre"][1] + RING["r"] * math.cos(a))


def rng_for(seed):
    return np.random.default_rng(seed)


def irregular_poly(centre, long, short, ang, rng, n=9, jit_r=0.07, jit_a=0.12):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n + rng.uniform(-jit_a, jit_a)
        rr = 1.0 + rng.uniform(-jit_r, jit_r)
        p = G.rot((0.5 * long * rr * math.cos(a), 0.5 * short * rr * math.sin(a)), ang)
        pts.append((centre[0] + p[0], centre[1] + p[1]))
    return G.hull2d(pts)


def scale_poly(poly, s, about=None, shift=(0.0, 0.0), turn=0.0):
    if about is None:
        about = G.centroid_area(poly)[0]
    return [(about[0] + q[0] + shift[0], about[1] + q[1] + shift[1])
            for q in (G.rot(((p[0] - about[0]) * s, (p[1] - about[1]) * s), turn) for p in poly)]


def outward_normal_at_vertex(i):
    n = len(BOUNDS)
    a, b, c = BOUNDS[i - 1], BOUNDS[i], BOUNDS[(i + 1) % n]

    def nrm(e):
        L = math.hypot(*e)
        return (e[1] / L, -e[0] / L)
    n1 = nrm((b[0] - a[0], b[1] - a[1]))
    n2 = nrm((c[0] - b[0], c[1] - b[1]))
    s = (n1[0] + n2[0], n1[1] + n2[1])
    L = math.hypot(*s)
    return (s[0] / L, s[1] / L)


def dome_h(u, v):
    a, b = MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
    r2 = ((u - MOUND["centre"][0]) / a) ** 2 + ((v - MOUND["centre"][1]) / b) ** 2
    if r2 >= 1.0:
        return 0.0
    t = min(max((1.0 - math.sqrt(r2)) / MOUND_TOE, 0.0), 1.0)
    return MOUND_RISE * (1.0 - r2) ** MOUND_EXP * t * t * (3.0 - 2.0 * t)


def mound_foot_v(u):
    a, b = MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
    return MOUND["centre"][1] - b * math.sqrt(max(0.0, 1.0 - (u / a) ** 2))


def layered(uv, long, short, h, ang, outward, seed, n_layers=3):
    rng = rng_for(seed)
    base = irregular_poly(uv, long, short, ang, rng)
    bc = G.centroid_area(base)[0]
    base = [(p[0] - bc[0] + uv[0], p[1] - bc[1] + uv[1]) for p in base]
    on = outward
    L = math.hypot(*on)
    on = (on[0] / L, on[1] / L)
    lay = [{"poly_uv": [[r3(p[0]), r3(p[1])] for p in base], "y0": 0.0, "y1": r3(0.45 * h), "top_scale": 0.90}]
    if n_layers >= 2:
        mid = scale_poly(base, 0.70, shift=(on[0] * 0.15 * long, on[1] * 0.15 * long), turn=math.radians(rng.uniform(6, 14)))
        lay.append({"poly_uv": [[r3(p[0]), r3(p[1])] for p in mid], "y0": r3(0.45 * h), "y1": r3(0.80 * h), "top_scale": 0.88})
    if n_layers >= 3:
        top = scale_poly(base, 0.42, shift=(on[0] * 0.26 * long, on[1] * 0.26 * long), turn=math.radians(-rng.uniform(5, 12)))
        lay.append({"poly_uv": [[r3(p[0]), r3(p[1])] for p in top], "y0": r3(0.80 * h), "y1": r3(h), "top_scale": 0.80})
    return lay


# --- footprints for the PRE-BUILD check (v1's measured hulls, placed; the acceptance measures
# the v2 build's own colliders instead) ---------------------------------------------------------
def placed_hull(cls, uv, yaw_deg):
    loc = LIB[cls]["low"]
    a = math.radians(yaw_deg)
    return [(uv[0] + q[0], uv[1] + q[1]) for q in (G.rot(tuple(p), a) for p in loc)]


def mound_rim_boxes():
    """The mound's collider as the scene builds it: 48 boxes on the ellipse at rho 0.97, the
    cutting's mouth left open, plus the cutting walls and the facade."""
    c = MOUND["centre"]
    a, b = MOUND["axes"][0] / 2 * 0.97, MOUND["axes"][1] / 2 * 0.97
    out = []
    nseg = 48
    cw = CUTTING["half_w"] + CUTTING["wall_t"]
    for s in range(nseg):
        t0, t1 = 2 * math.pi * s / nseg, 2 * math.pi * (s + 1) / nseg
        p0 = (c[0] + a * math.cos(t0), c[1] + b * math.sin(t0))
        p1 = (c[0] + a * math.cos(t1), c[1] + b * math.sin(t1))
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        if abs(mid[0]) < cw and mid[1] < c[1]:
            continue
        d = (p1[0] - p0[0], p1[1] - p0[1])
        L = math.hypot(*d)
        e = (d[0] / L * 0.15, d[1] / L * 0.15)
        out.append(G.thick_segment((p0[0] - e[0], p0[1] - e[1]), (p1[0] + e[0], p1[1] + e[1]), 0.15))
    hw, wt, vf = CUTTING["half_w"], CUTTING["wall_t"], CUTTING["v_facade"]
    v_start = mound_foot_v(hw + wt) - 0.3
    for s in (-1, 1):
        u0, u1 = sorted((s * hw, s * (hw + wt)))
        out.append([(u0, v_start), (u1, v_start), (u1, vf + 0.3), (u0, vf + 0.3)])
    out.append([(-hw - wt, vf), (hw + wt, vf), (hw + wt, vf + CUTTING["facade_t"]), (-hw - wt, vf + CUTTING["facade_t"])])
    return out


def fallen_stone_poly(uv, out):
    L, W = 2.71, 0.70
    n = (-out[1], out[0])
    a = uv
    b = (uv[0] + out[0] * L, uv[1] + out[1] * L)
    return [(a[0] + n[0] * W / 2, a[1] + n[1] * W / 2), (b[0] + n[0] * W / 2, b[1] + n[1] * W / 2),
            (b[0] - n[0] * W / 2, b[1] - n[1] * W / 2), (a[0] - n[0] * W / 2, a[1] - n[1] * W / 2)]


def bounds_obstacles():
    obs = []
    n = len(BOUNDS)
    for i in range(n):
        a, b = BOUNDS[i], BOUNDS[(i + 1) % n]
        d = (b[0] - a[0], b[1] - a[1])
        L = math.hypot(*d)
        e = (d[0] / L * WALL_HALF_T, d[1] / L * WALL_HALF_T)
        obs.append(("bounds", G.thick_segment((a[0] - e[0], a[1] - e[1]), (b[0] + e[0], b[1] + e[1]), WALL_HALF_T)))
    return obs


def object_of(pid):
    """One object, one group: the fallen tree's two logs are one tree, the door's posts and lintel
    one door. The no-squeeze rule is about gaps BETWEEN objects."""
    if pid.startswith("fallen_tree_log_"):
        return "fallen_tree"
    if pid.startswith("door_"):
        return "door"
    return pid


def obstacles_of(P):
    obs = bounds_obstacles()
    for poly in mound_rim_boxes():
        obs.append(("mound", poly))
    for e in P:
        if e.get("margin"):
            continue                          # outside the bounds: cannot bound a walkable gap
        cls = e["class"]
        if e["kind"] == "primitive":
            obs.append((e["id"], [tuple(p) for p in e["layers"][0]["poly_uv"]]))
        elif cls == "birch":
            obs.append((e["id"], G.circle_poly(tuple(e["uv"]), BIRCH_TRUNK_R)))
        elif e.get("tip"):
            obs.append((e["id"], fallen_stone_poly(tuple(e["uv"]), tuple(e["tip"]["outward_uv"]))))
        elif cls in LIB and e.get("uv") and cls != "lintel":
            obs.append((object_of(e["id"]), placed_hull(cls, tuple(e["uv"]), float(e["yaw_world_deg"]))))
    return obs


def free_fn(obs):
    """His centre can stand at (u, v): inside the bounds and at least his capsule's radius from
    every obstacle. A POINT test -- it cannot see that a pocket is walled off (v2's first
    pre-check reported a 'squeeze' inside the mound for exactly that reason); walkable_fn adds
    the connectivity."""
    polys = []
    for g, p in obs:
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        polys.append((min(xs) - 0.4, max(xs) + 0.4, min(ys) - 0.4, max(ys) + 0.4, p))

    mc, ma, mb = MOUND["centre"], MOUND["axes"][0] / 2 * 0.97, MOUND["axes"][1] / 2 * 0.97

    def f(u, v):
        if not G.in_poly((u, v), BOUNDS):
            return False
        # the mound's inside is SOLID (its rim encloses it; the physics grid confirms 0 cells
        # there): only the cutting is open. Without this the approximate fill leaked in.
        if ((u - mc[0]) / ma) ** 2 + ((v - mc[1]) / mb) ** 2 < 1.0 and not (abs(u) < CUTTING["half_w"] and v < CUTTING["v_facade"]):
            return False
        for x0, x1, y0, y1, p in polys:
            if u < x0 or u > x1 or v < y0 or v > y1:
                continue
            if G.dist_poly_pt(p, (u, v)) < CAPSULE_R:
                return False
        return True
    return f


PRE_STEP = 0.25
PRE_U = (-21.0, 18.0)
PRE_V = (-18.75, 12.0)


def walkable_fn(obs, spawn=(-3.0, -15.0)):
    """The pre-build flood fill: free cells (free_fn) on a 0.25 m grid, 4-connected from the
    entry. walkable(u, v) is the nearest cell's answer. The acceptance uses the PHYSICS flood
    fill instead; this is its stand-in so the layout can be corrected before Godot starts."""
    free = free_fn(obs)
    nu = int(round((PRE_U[1] - PRE_U[0]) / PRE_STEP)) + 1
    nv = int(round((PRE_V[1] - PRE_V[0]) / PRE_STEP)) + 1
    cache = {}

    def fr(i, j):
        k = (i, j)
        if k not in cache:
            cache[k] = free(PRE_U[0] + i * PRE_STEP, PRE_V[0] + j * PRE_STEP)
        return cache[k]
    si = int(round((spawn[0] - PRE_U[0]) / PRE_STEP))
    sj = int(round((spawn[1] - PRE_V[0]) / PRE_STEP))
    seen = set()
    stack = [(si, sj)] if fr(si, sj) else []
    seen.update(stack)
    while stack:
        i, j = stack.pop()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < nu and 0 <= nj < nv and (ni, nj) not in seen and fr(ni, nj):
                seen.add((ni, nj))
                stack.append((ni, nj))

    def f(u, v):
        return (int(round((u - PRE_U[0]) / PRE_STEP)), int(round((v - PRE_V[0]) / PRE_STEP))) in seen
    f.cells = seen
    return f


# --- groves, found rather than drawn -------------------------------------------------------------
def solve_grove(name, centre, n, fixed, walkable, seed, scenery=False):
    """Trunk positions for one grove: an organic cluster (not a row) whose centroid IS the
    table's point, and which obeys the no-squeeze rule -- every trunk-to-trunk and
    trunk-to-obstacle gap in the walkable area is < 0.60 or >= 1.50 m (the rule's 0.70 / 1.40,
    with 0.10 m of margin for this pre-check's approximate footprints). Deterministic: a
    seeded search, first solution wins."""
    rng = rng_for(seed)
    tr = BIRCH_TRUNK_R
    lo, hi = 0.60, 1.50
    for attempt in range(60000):
        pts = []
        for k in range(n):
            rr = 2.4 * math.sqrt(rng.uniform(0.05, 1.0))
            a = rng.uniform(0, 2 * math.pi)
            pts.append((rr * math.cos(a), rr * math.sin(a)))
        mx = sum(p[0] for p in pts) / n
        my = sum(p[1] for p in pts) / n
        pts = [(centre[0] + p[0] - mx, centre[1] + p[1] - my) for p in pts]
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                g = math.dist(pts[i], pts[j]) - 2 * tr
                if g < 0.25 or (lo <= g < hi and not scenery):
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        for p in pts:
            if math.dist(p, ARENA["centre"]) < ARENA["r"] + 0.8:
                ok = False
            if min(G.seg_pt(p, PATH["points"][k], PATH["points"][k + 1]) for k in range(len(PATH["points"]) - 1)) < PATH["width"] / 2 + 0.8:
                ok = False
            tc, ta, tb = TARN["centre"], TARN["axes"][0] / 2, TARN["axes"][1] / 2
            if ((p[0] - tc[0]) / ta) ** 2 + ((p[1] - tc[1]) / tb) ** 2 < 1.15:
                ok = False
            mc, ma, mb = MOUND["centre"], MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
            if ((p[0] - mc[0]) / ma) ** 2 + ((p[1] - mc[1]) / mb) ** 2 < 1.1:
                ok = False
            if not ok:
                break
            inside = G.in_poly(p, BOUNDS)
            for g_, poly in fixed:
                d = G.dist_poly_pt(poly, p) - tr
                if d < 0.25 and g_ != "bounds":
                    ok = False
                    break
                if scenery:
                    continue
                # A TRUNK INSIDE THE BOUNDS STANDS ON THE WALL OR WELL CLEAR OF IT: 0.6-1.5 m from
                # a wall is a notch he can step into (G2's first solution left 0.93 m at the corner)
                if g_ == "bounds" and inside and 0.1 <= d < hi:
                    ok = False
                    break
                if lo <= d < hi:
                    # a gap counts only if it lies in the walkable area
                    _, q1, q2 = G.closest_pair(G.circle_poly(p, tr), poly)
                    if any(walkable(q1[0] + (q2[0] - q1[0]) * t / 6, q1[1] + (q2[1] - q1[1]) * t / 6) for t in range(7)):
                        ok = False
                        break
            if not ok:
                break
        if ok:
            return pts, attempt
    raise SystemExit("grove %s: no solution in 60000 draws -- the constraints are over-tight" % name)


# --- the placement list --------------------------------------------------------------------------
def build():
    P = []
    dev = []
    c = MOUND["centre"]
    P.append({"id": "mound", "piece": "barrow mound", "class": "mound", "kind": "structure",
              "spec_uv": list(c), "uv": list(c), "semi_axes": [MOUND["axes"][0] / 2, MOUND["axes"][1] / 2],
              "rise_m": MOUND_RISE, "rise_spec_m": MOUND["rise_about"], "exponent": MOUND_EXP, "toe_rho": MOUND_TOE,
              "profile": "h = rise * (1 - rho^2)^0.35 * smoothstep over the outer 8% of rho: KERBED -- a ~70-75 deg kerb, flat on top; the foot's vertices on the ellipse",
              "tint": "mound", "walkable": False,
              "collider": "48 vertical boxes on the rim at rho 0.97, the cutting's mouth left open; the cutting walls; the facade",
              "door_v": DOOR_V, "cutting": CUTTING, "passage": PASSAGE,
              "_why_4_2": "the lintel's top is 3.185 m (v1, measured); the cover rule needs >= 3.485 m of mound directly behind the door and the camera-margin rule needs the threshold at v <= 10.66 -- a 4.0 m kerbed dome admits no door position, 4.2 m admits ~0.25 m of it"})
    lint = BA["lintel"]
    ang = math.radians(lint["yaw_deg"])
    ax_uv = xz_to_uv(math.sin(ang), math.cos(ang))
    P.append({"id": "door_lintel", "piece": "door lintel", "class": "lintel", "kind": "model",
              "glb": "res://models/barrow/lintel.glb", "spec_uv": None, "uv": [0.0, DOOR_V],
              "derived_from": "spec v2: the door on the centre line, set into the mound's face; v 10.6 from the cover and camera-margin rules (see the mound's _why_4_2)",
              "yaw_world_deg": lint["yaw_deg"], "axis": "across", "target_m": lint["height_m"],
              "pitch_correct": True, "width_m": None, "hull_px": 1.1, "collider": "hull",
              "stack_on": ["door_post_L", "door_post_R"], "door_piece": True})
    for side, sgn in (("L", -1.0), ("R", 1.0)):
        uv = (sgn * POST_OFFSET_M * ax_uv[0], DOOR_V + sgn * POST_OFFSET_M * ax_uv[1])
        P.append({"id": "door_post_" + side, "piece": "door post " + side, "class": "post", "kind": "model",
                  "glb": "res://models/barrow/post.glb", "spec_uv": None, "uv": [r3(uv[0]), r3(uv[1])],
                  "derived_from": "door_lintel: under its ends, %.2f m along its long axis (ratified on v1)" % POST_OFFSET_M,
                  "yaw_world_deg": BA["post"]["yaw_deg"], "axis": "height", "target_m": BA["post"]["height_m"],
                  "pitch_correct": True, "width_m": None, "hull_px": 1.1, "collider": "hull", "door_piece": True})
    for theta, cls, note in RING_STONES:
        uv = ring_uv(theta)
        sid = "ring_%s%d" % ("p" if theta > 0 else "m", abs(theta))
        turn = -RING_INWARD_TURN_DEG if uv[0] > 0 else RING_INWARD_TURN_DEG
        e = {"id": sid, "piece": "ring stone %+d" % theta + (" (%s)" % note if note else ""), "class": cls,
             "kind": "model", "glb": "res://models/barrow/%s.glb" % cls, "spec_uv": [r3(uv[0]), r3(uv[1])],
             "uv": [r3(uv[0]), r3(uv[1])], "theta_deg": theta, "axis": "height", "target_m": BA[cls]["height_m"],
             "pitch_correct": True, "width_m": None, "hull_px": 1.1, "collider": "hull"}
        if theta == -95:
            out = (uv[0] - RING["centre"][0], uv[1] - RING["centre"][1])
            L = math.hypot(*out)
            out = (out[0] / L, out[1] / L)
            inward = (-out[0], -out[1])
            beta = math.degrees(math.atan2(inward[0], -inward[1]))
            e["yaw_world_deg"] = r3(BA[cls]["yaw_deg"] + beta)
            e["tip"] = {"outward_uv": [r3(out[0]), r3(out[1])], "face": "up",
                        "placement_point": "the socket (the stone's base end)", "sink_m": 0.06}
        else:
            e["yaw_world_deg"] = r3((BA[cls]["yaw_deg"] + turn) % 360.0)
            e["_facing"] = "manifest yaw %g (carved face at -v) turned %+g toward the ring axis" % (BA[cls]["yaw_deg"], turn)
        P.append(e)
    P.append({"id": "raven", "piece": "raven", "class": "raven", "kind": "model", "glb": "res://models/barrow/raven.glb",
              "spec_uv": None, "uv": None, "perch_on": "ring_p55", "yaw_world_deg": 200.0, "axis": "height",
              "target_m": 0.28, "pitch_correct": True, "width_m": None, "hull_px": 1.1, "collider": "none",
              "derived_from": "the table: 'on the +55 stone'"})
    # OUTCROPS
    for i, cxy in enumerate(OUTCROPS):
        k = i + 1
        long, short, h, ang, outward = OUTCROP_DIMS[k]
        if ang is None:
            vi = BOUNDS.index((float(cxy[0]), float(cxy[1])))
            on = outward_normal_at_vertex(vi)
            ang_r = math.atan2(on[0], -on[1])
            outward = on
        else:
            ang_r = math.radians(ang)
        P.append({"id": "outcrop_%d" % k, "piece": "outcrop %d" % k, "class": "outcrop", "kind": "primitive",
                  "spec_uv": [float(cxy[0]), float(cxy[1])], "uv": [float(cxy[0]), float(cxy[1])],
                  "footprint_m": [long, short], "height_m": h, "outward_uv": [r3(outward[0]), r3(outward[1])],
                  "layers": layered(cxy, long, short, h, ang_r, outward, 1000 + i), "collider": "convex hull per layer",
                  "in_margin": k in (7, 8)})
    P.append({"id": "cover_outcrop", "piece": "cover outcrop (the tarn fight)", "class": "outcrop", "kind": "primitive",
              "spec_uv": list(COVER["uv"]), "uv": list(COVER["uv"]), "footprint_m": list(COVER["size"]),
              "height_m": COVER["h"], "collider": "convex hull per layer",
              "layers": layered(COVER["uv"], COVER["size"][0], COVER["size"][1], COVER["h"], 0.0, (0.0, 1.0), 2000, n_layers=2)})
    for j, (cxy, long, short, h, ang, outward) in enumerate(MARGIN_OUTCROPS):
        P.append({"id": "margin_outcrop_%d" % (j + 1), "piece": "margin outcrop M%d" % (j + 1), "class": "outcrop",
                  "kind": "primitive", "spec_uv": None, "uv": list(cxy), "footprint_m": [long, short], "height_m": h,
                  "margin": True, "derived_from": "spec v2 § 1: the margin beyond the bounds is scenery (outcrops, tree lines, scrub)",
                  "layers": layered(cxy, long, short, h, math.radians(ang), outward, 4000 + j), "collider": "convex hull per layer"})
    # SHORE ROCK: the tarn's W and SW rim
    tc, (ta, tb) = TARN["centre"], (TARN["axes"][0] / 2, TARN["axes"][1] / 2)
    for k, t in enumerate(range(150, 250, 12)):
        tr_ = math.radians(t)
        rim = (tc[0] + ta * math.cos(tr_), tc[1] + tb * math.sin(tr_))
        nrm = (math.cos(tr_) / ta, math.sin(tr_) / tb)
        L = math.hypot(*nrm)
        nrm = (nrm[0] / L, nrm[1] / L)
        tang = math.atan2(nrm[0], -nrm[1])
        rngk = rng_for(3000 + k)
        long = 1.9 + rngk.uniform(-0.2, 0.3)
        short = 1.25 + rngk.uniform(-0.15, 0.15)
        h = 0.55 + rngk.uniform(-0.12, 0.30)
        cen = (rim[0] + nrm[0] * (0.5 * short + 0.05), rim[1] + nrm[1] * (0.5 * short + 0.05))
        base = irregular_poly(cen, long, short, tang, rngk, n=8, jit_r=0.08)
        lay = [{"poly_uv": [[r3(p[0]), r3(p[1])] for p in base], "y0": 0.0, "y1": r3(h * (0.7 if k % 2 == 0 else 1.0)), "top_scale": 0.85}]
        if k % 2 == 0:
            top = scale_poly(base, 0.6, shift=(nrm[0] * 0.2, nrm[1] * 0.2), turn=math.radians(10))
            lay.append({"poly_uv": [[r3(p[0]), r3(p[1])] for p in top], "y0": r3(h * 0.7), "y1": r3(h), "top_scale": 0.8})
        P.append({"id": "shore_rock_%d" % (k + 1), "piece": "shore rock %d" % (k + 1), "class": "shore_rock",
                  "kind": "primitive", "spec_uv": None, "uv": [r3(cen[0]), r3(cen[1])], "height_m": r3(h),
                  "derived_from": "the tarn row: 'West and south-west rim is shore rock (non-walkable)' (rim angle %d deg)" % t,
                  "layers": lay, "collider": "convex hull per layer"})
    # THE SHORE BRIDGE: the chain's SW end and outcrop 5 left a 1.36 m pocket (a squeeze, by the
    # v2 rule). One more slab, laid across the gap between their closest points, closes it.
    o5 = [tuple(q) for q in next(e for e in P if e["id"] == "outcrop_5")["layers"][0]["poly_uv"]]
    shores = [e for e in P if e["class"] == "shore_rock"]
    gaps = [(G.closest_pair([tuple(q) for q in e["layers"][0]["poly_uv"]], o5), e) for e in shores]
    (dg, qa, qb), near = min(gaps, key=lambda x: x[0][0])
    if 0.0 < dg < 2.2:
        mid = ((qa[0] + qb[0]) / 2, (qa[1] + qb[1]) / 2)
        ang_b = math.atan2(qb[1] - qa[1], qb[0] - qa[0])
        rngb = rng_for(3900)
        base = irregular_poly(mid, dg + 0.9, 1.15, ang_b, rngb, n=8, jit_r=0.06)
        P.append({"id": "shore_rock_bridge", "piece": "shore rock (bridge to outcrop 5)", "class": "shore_rock",
                  "kind": "primitive", "spec_uv": None, "uv": [r3(mid[0]), r3(mid[1])], "height_m": 0.7,
                  "derived_from": "closes the %.2f m pocket between %s and outcrop 5 (the no-squeeze rule)" % (dg, near["id"]),
                  "layers": [{"poly_uv": [[r3(p_[0]), r3(p_[1])] for p_ in base], "y0": 0.0, "y1": 0.7, "top_scale": 0.85}],
                  "collider": "convex hull per layer"})

    # FALLEN TREE (ratified on v1): two kit logs, the pair centred on the table's point
    C = FALLEN_TREE
    dA = (math.cos(math.radians(LOG_ANGLES_DEG[0])), math.sin(math.radians(LOG_ANGLES_DEG[0])))
    dB = (math.cos(math.radians(LOG_ANGLES_DEG[1])), math.sin(math.radians(LOG_ANGLES_DEG[1])))
    h2 = 0.5 * LOG_LEN
    cA = (C[0] - h2 * dA[0], C[1] - h2 * dA[1])
    cB = (C[0] + h2 * dB[0], C[1] + h2 * dB[1])
    sh = (C[0] - 0.5 * (cA[0] + cB[0]), C[1] - 0.5 * (cA[1] + cB[1]))
    J = (C[0] + sh[0], C[1] + sh[1])
    for tag, a_deg, cen, flip in (("A", LOG_ANGLES_DEG[0], cA, 0.0), ("B", LOG_ANGLES_DEG[1], cB, 180.0)):
        uv = (cen[0] + sh[0], cen[1] + sh[1])
        P.append({"id": "fallen_tree_log_" + tag, "piece": "fallen tree, log " + tag, "class": "log", "kind": "kit",
                  "glb": "res://models/barrow/kit/log.glb", "spec_uv": None, "uv": [r3(uv[0]), r3(uv[1])],
                  "pair_spec_uv": list(C), "joint_uv": [r3(J[0]), r3(J[1])],
                  "derived_from": "the fallen tree at (-7, -12): two logs end to end, the pair centred on that point",
                  "yaw_world_deg": r3(a_deg + flip), "axis": "height", "target_m": KA["log"]["height_m"],
                  "pitch_correct": False, "width_m": None, "hull_px": 1.1, "collider": "hull"})
    for uv in GRAVES:
        P.append({"id": "grave_marker_%s" % ("W" if uv[0] < 0 else "E"), "piece": "grave marker (shield on spears)",
                  "class": "shield", "kind": "kit", "glb": "res://models/barrow/kit/shield.glb", "spec_uv": list(uv),
                  "uv": list(uv), "yaw_world_deg": 0.0, "axis": "height", "target_m": KA["shield"]["height_m"],
                  "pitch_correct": False, "width_m": None, "hull_px": 1.1, "collider": "hull"})
    for i, uv in enumerate(CAIRNS):
        e = {"id": "cairn_%d" % (i + 1), "piece": "cairn %d" % (i + 1), "class": "cairn", "kind": "kit",
             "glb": "res://models/barrow/kit/cairn.glb", "spec_uv": list(uv), "uv": list(uv), "yaw_world_deg": 0.0,
             "axis": "height", "target_m": KA["cairn"]["height_m"], "pitch_correct": False, "width_m": None,
             "hull_px": 1.1, "collider": "hull"}
        if i == 1:
            # TURNED, NOT MOVED (ratified on v1) -- and the angle is now SEARCHED: the yaw that
            # maximises the smaller of (its clearance from the 4 m path) and (its gap to the
            # entry corner's walls beyond the 1.40 m squeeze line), on its measured v1 hull.
            best = None
            for yaw in range(0, 180):
                hull = placed_hull("cairn", uv, yaw)
                pc = min(G.dist_poly_poly(hull, [PATH["points"][q], PATH["points"][q + 1]], q_closed=False)
                         for q in range(len(PATH["points"]) - 1)) - PATH["width"] / 2
                wg = min(G.dist_poly_poly(hull, poly) for g_, poly in bounds_obstacles())
                score = min(pc, wg - 1.40)
                if best is None or score > best[0]:
                    best = (score, yaw, pc, wg)
            e["yaw_world_deg"] = float(best[1])
            e["_yaw"] = ("turned %d deg (searched): path clearance %.3f m, gap to the entry corner %.3f m "
                         "(squeeze line 1.40) -- the v1 turn of 71.6 deg pointed its long tip at the corner"
                         % (best[1], best[2], best[3]))
        P.append(e)
    # GROVES: solved against everything above, walls included
    fixed = obstacles_of(P)
    walk = walkable_fn(fixed)
    yi = 0
    solved = {}
    for gi, (g, (cxy, n)) in enumerate(GROVES.items()):
        pts, tries = solve_grove(g, cxy, n, fixed, walk, 7000 + gi, scenery=(g == "G4"))
        solved[g] = tries
        for j, uv in enumerate(pts):
            P.append({"id": "%s_birch_%d" % (g, j + 1), "piece": "%s birch %d" % (g, j + 1), "class": "birch",
                      "kind": "model", "glb": "res://models/barrow/birch.glb", "spec_uv": None,
                      "uv": [r3(uv[0]), r3(uv[1])], "grove": g, "grove_spec_uv": list(cxy),
                      "derived_from": "grove %s at (%g, %g) x%d; members found by a seeded search (no squeezes), centroid = the grove point" % (g, cxy[0], cxy[1], n),
                      "yaw_world_deg": float(BIRCH_YAWS[yi % len(BIRCH_YAWS)]), "axis": "height",
                      "target_m": BA["birch"]["height_m"], "pitch_correct": True, "width_m": BA["birch"]["width_m"],
                      "hull_px": 0.0, "mesh_mark": 0.25, "collider": "trunk", "trunk_r": BIRCH_TRUNK_R})
            fixed.append(("%s_birch_%d" % (g, j + 1), G.circle_poly(uv, BIRCH_TRUNK_R)))
            yi += 1
    # MARGIN TREE LINES
    obs_all = [(g, p) for g, p in fixed] + [(e["id"], [tuple(q) for q in e["layers"][0]["poly_uv"]]) for e in P if e.get("margin")]
    for name, (a, b, n) in TREE_LINES.items():
        rng = rng_for(9000 + sum(map(ord, name)))
        placed = 0
        k = 0
        while placed < n and k < 400:
            t = (placed + 0.5) / n + rng.uniform(-0.12, 0.12)
            p = (a[0] + (b[0] - a[0]) * t + rng.uniform(-0.8, 0.8), a[1] + (b[1] - a[1]) * t + rng.uniform(-0.8, 0.8))
            k += 1
            if not (WIN_U[0] + 0.6 <= p[0] <= WIN_U[1] - 0.6 and WIN_V[0] + 0.6 <= p[1] <= WIN_V[1] - 0.6):
                continue
            if G.in_poly(p, BOUNDS) or min(G.seg_pt(p, BOUNDS[i], BOUNDS[(i + 1) % len(BOUNDS)]) for i in range(len(BOUNDS))) < 1.2:
                continue
            ext = path_points_extended()
            if min(G.seg_pt(p, ext[i], ext[i + 1]) for i in range(len(ext) - 1)) < PATH["width"] / 2 + 1.0:
                continue
            mc, ma, mb = MOUND["centre"], MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
            if ((p[0] - mc[0]) / ma) ** 2 + ((p[1] - mc[1]) / mb) ** 2 < 1.1:
                continue
            if any(G.dist_poly_pt(poly, p) < 0.6 for g, poly in obs_all):
                continue
            pid = "%s_%d" % (name, placed + 1)
            P.append({"id": pid, "piece": "margin tree line %s" % name, "class": "birch", "kind": "model",
                      "glb": "res://models/barrow/birch.glb", "spec_uv": None, "uv": [r3(p[0]), r3(p[1])], "margin": True,
                      "derived_from": "spec v2 § 1: tree lines in the margin", "yaw_world_deg": float(BIRCH_YAWS[yi % len(BIRCH_YAWS)]),
                      "axis": "height", "target_m": BA["birch"]["height_m"], "pitch_correct": True,
                      "width_m": BA["birch"]["width_m"], "hull_px": 0.0, "mesh_mark": 0.25, "collider": "trunk",
                      "trunk_r": BIRCH_TRUNK_R})
            obs_all.append((pid, G.circle_poly(p, BIRCH_TRUNK_R)))
            yi += 1
            placed += 1
    return P, dev, solved


def crucible(P):
    """The wave-arena marks. A spawn circle overlapping a stone's footprint or the cutting walls
    is NUDGED ALONG ITS OWN RAY from (0, 2) by the least distance that clears it (the rule), on
    the stones' measured hulls; every move is reported."""
    stones = [(e["id"], (fallen_stone_poly(tuple(e["uv"]), tuple(e["tip"]["outward_uv"])) if e.get("tip")
                         else placed_hull(e["class"], tuple(e["uv"]), float(e["yaw_world_deg"]))))
              for e in P if e["id"].startswith("ring_")]
    hw, wt, vf = CUTTING["half_w"], CUTTING["wall_t"], CUTTING["v_facade"]
    vs_ = mound_foot_v(hw + wt) - 0.3
    walls = [("cutting_wall_%s" % s, [(min(s * hw, s * (hw + wt)), vs_), (max(s * hw, s * (hw + wt)), vs_),
                                     (max(s * hw, s * (hw + wt)), vf), (min(s * hw, s * (hw + wt)), vf)]) for s in (-1, 1)]
    obs = stones + walls
    R = CRUCIBLE["spawn_r_m"]
    about = CRUCIBLE["about_uv"]
    out = []
    for sid, xy, note in CRUCIBLE["spawns"]:
        d = (xy[0] - about[0], xy[1] - about[1])
        L = math.hypot(*d)
        d = (d[0] / L, d[1] / L)

        def clear(t):
            c = (xy[0] + d[0] * t, xy[1] + d[1] * t)
            return all(G.dist_poly_pt(poly, c) >= R for g_, poly in obs)
        t_best = 0.0
        if not clear(0.0):
            cands = [k * 0.005 for k in range(1, 801)]
            t_best = next(t for t in sorted(cands + [-c for c in cands], key=abs) if clear(t))
        c = (xy[0] + d[0] * t_best, xy[1] + d[1] * t_best)
        blocker = min(((G.dist_poly_pt(poly, xy), g_) for g_, poly in obs), key=lambda x: x[0])
        out.append({"id": sid, "spec_uv": list(xy), "uv": [r3(c[0]), r3(c[1])], "r_m": R, "note": note,
                    "ray_from_uv": list(about), "nudge_m": r3(t_best),
                    "nudge": ("none -- clear of every stone and the cutting walls" if t_best == 0.0 else
                              "%+.3f m along its own ray (%s the ring centre): its r 1.5 circle overlapped %s"
                              % (t_best, "away from" if t_best > 0 else "toward", blocker[1])),
                    "nearest_obstacle_at_spec_point": {"id": blocker[1], "centre_to_footprint_m": r3(blocker[0])}})
    mouth_v = mound_foot_v(CUTTING["half_w"])
    return {"_what": "Crucible wave-arena marks (Matt, via the coordinator): flat decals, no colliders -- the arena and flow checks are unchanged by them",
            "spawns": out, "boss_gate": {"uv": [0.0, r3(mouth_v)], "width_m": 2 * CUTTING["half_w"],
                                          "note": "the barrow door's cutting, marked at its mouth: the King walks out of his tomb"},
            "station": {"uv": list(CRUCIBLE["station_uv"]), "note": "the arena centre"},
            "eye_height_m": CRUCIBLE["eye_height_m"],
            "shown": {"app": "ON at launch; R hides them", "guide": "OFF -- a paint-over guide must not teach the painter to paint 'S1'",
                      "stills": "the marker still only", "map": "drawn"},
            "measured_by_finalize": "distance to the station, line of sight at eye height (physics raycast), walkable path length (the physics flood grid)"}


# --- regions and the splat ------------------------------------------------------------------------
def seg_dist(pu, pv, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = np.clip(((pu - ax) * dx + (pv - ay) * dy) / L2, 0.0, 1.0)
    return np.hypot(pu - (ax + t * dx), pv - (ay + t * dy)), t


def path_points_extended():
    """The table's polyline, carried on along its last direction past the window's bottom edge."""
    pts = list(PATH["points"])
    a, b = pts[-2], pts[-1]
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d)
    k = (b[1] - (WIN_V[0] - 1.0)) / (-d[1] / L)
    pts.append((r3(b[0] + d[0] / L * k), r3(b[1] + d[1] / L * k)))
    return pts


def path_dist(pu, pv):
    pts = path_points_extended()
    best = np.full(pu.shape, 1e9)
    for i in range(len(pts) - 1):
        d, t = seg_dist(pu, pv, pts[i], pts[i + 1])
        if i == 0:
            d = np.where(t <= 0.0, 1e9, d)            # butt cap at the ring entrance
        best = np.minimum(best, d)
    return best


def in_poly_np(pu, pv, poly):
    inside = np.zeros(pu.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cond = ((y1 > pv) != (y2 > pv))
        xint = x1 + (pv - y1) * (x2 - x1) / ((y2 - y1) if y2 != y1 else 1e-12)
        inside ^= cond & (pu < xint)
    return inside


def poly_boundary_dist(pu, pv, poly, closed=True, skip_edges=()):
    best = np.full(pu.shape, 1e9)
    n = len(poly)
    for i in range(n if closed else n - 1):
        if i in skip_edges:
            continue
        d, _ = seg_dist(pu, pv, poly[i], poly[(i + 1) % n])
        best = np.minimum(best, d)
    return best


def value_noise(pu, pv, cell, seed):
    rng = rng_for(seed)
    Gd = rng.uniform(-1, 1, size=(129, 129))
    x = (pu / cell) + 64.0
    y = (pv / cell) + 64.0
    x0 = np.clip(np.floor(x).astype(int), 0, 127)
    y0 = np.clip(np.floor(y).astype(int), 0, 127)
    fx = np.clip(x - x0, 0, 1)
    fy = np.clip(y - y0, 0, 1)
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    a = Gd[y0, x0]
    b = Gd[y0, x0 + 1]
    c = Gd[y0 + 1, x0]
    d = Gd[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def region_masks(pu, pv, P):
    tc, (ta, tb) = TARN["centre"], (TARN["axes"][0] / 2, TARN["axes"][1] / 2)
    rho_t = np.hypot((pu - tc[0]) / ta, (pv - tc[1]) / tb)
    ice = rho_t <= 1.0
    pd = path_dist(pu, pv)
    path = pd <= PATH["width"] / 2.0
    arena = np.hypot(pu - ARENA["centre"][0], pv - ARENA["centre"][1]) <= ARENA["r"]
    g = ring_uv(155)
    entrance = (np.abs(pu) <= g[0] + 0.3) & (np.abs(pv - g[1]) <= 1.6)
    cutting = (np.abs(pu) <= CUTTING["half_w"] + CUTTING["wall_t"] + 0.2) & (pv >= 7.9) & (pv <= CUTTING["v_facade"] + 0.4)
    warp = value_noise(pu, pv, 1.6, 71) * 0.45
    zones = {}
    sk = np.zeros(pu.shape, dtype=bool)
    for e in P:
        if e["class"] == "outcrop":
            base = [tuple(p) for p in e["layers"][0]["poly_uv"]]
            d = np.where(in_poly_np(pu, pv, base), 0.0, poly_boundary_dist(pu, pv, base))
            sk |= (d + warp) <= 2.5
    zones["outcrop_skirts"] = sk
    gv = np.zeros(pu.shape, dtype=bool)
    for e in P:
        if e["class"] == "birch":
            gv |= (np.hypot(pu - e["uv"][0], pv - e["uv"][1]) + warp) <= 1.7
    zones["under_groves_and_tree_lines"] = gv
    mc = MOUND["centre"]
    ma, mb = MOUND["axes"][0] / 2, MOUND["axes"][1] / 2
    rho_m = np.hypot((pu - mc[0]) / ma, (pv - mc[1]) / mb)
    band = (rho_m >= 0.93) & (np.hypot((pu - mc[0]) / (ma + 2.2), (pv - mc[1]) / (mb + 2.2)) + warp * 0.08 <= 1.0)
    outside_ring = np.hypot(pu - RING["centre"][0], pv - RING["centre"][1]) > RING["r"]
    zones["mound_base_outside_ring"] = band & outside_ring
    far = (rho_t > 1.0) & (np.hypot((pu - tc[0]) / (ta + 2.8), (pv - tc[1]) / (tb + 2.8)) + warp * 0.08 <= 1.0) & (pu <= tc[0] - 1.0)
    zones["tarn_far_shore"] = far
    bd = poly_boundary_dist(pu, pv, BOUNDS, closed=True, skip_edges=BAND_SKIP_EDGES)
    zones["thicket_band_ADDED"] = (bd + warp) <= 1.5
    outside = ~in_poly_np(pu, pv, BOUNDS)
    margin_patch = value_noise(pu, pv, 2.8, 191) > 0.25
    zones["margin_scrub_ADDED"] = outside & margin_patch
    shrub_zone = np.zeros(pu.shape, dtype=bool)
    for m in zones.values():
        shrub_zone |= m
    patch = value_noise(pu, pv, 2.4, 113) > -0.72
    shrub = shrub_zone & patch
    keep_out = arena | (pd <= PATH["width"] / 2.0 + 0.35) | ice | entrance | cutting
    shrub &= ~keep_out
    path &= ~ice
    return {"ice": ice, "path": path, "shrub": shrub, "zones": zones}


def gauss_blur(a, sigma_px):
    rr = int(math.ceil(sigma_px * 3))
    x = np.arange(-rr, rr + 1)
    k = np.exp(-0.5 * (x / sigma_px) ** 2)
    k /= k.sum()
    b = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, np.pad(a, rr, mode="edge"))
    b = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, b)
    return b[rr:-rr, rr:-rr]


def splat_frame():
    cs = [uv_to_xz(u, v) for u in WIN_U for v in WIN_V]
    x0, x1 = min(c[0] for c in cs) - 1.0, max(c[0] for c in cs) + 1.0
    z0, z1 = min(c[1] for c in cs) - 1.0, max(c[1] for c in cs) + 1.0
    size = math.ceil(max(x1 - x0, z1 - z0))
    return {"origin_xz": [round(x0, 2), round(z0, 2)], "size_m": [float(size), float(size)], "m_per_px": 0.05}


def make_splat(P):
    SPLAT = splat_frame()
    n = int(round(SPLAT["size_m"][0] / SPLAT["m_per_px"]))
    ii, jj = np.meshgrid(np.arange(n), np.arange(n))
    x = SPLAT["origin_xz"][0] + (ii + 0.5) * SPLAT["m_per_px"]
    z = SPLAT["origin_xz"][1] + (jj + 0.5) * SPLAT["m_per_px"]
    pu, pv = xz_to_uv(x, z)
    M = region_masks(pu, pv, P)
    cls = np.zeros((n, n), dtype=np.uint8)
    cls[M["shrub"]] = 3
    cls[M["path"]] = 1
    cls[M["ice"]] = 4
    W = np.stack([gauss_blur((cls == c).astype(np.float64), 1.6) for c in (1, 2, 3, 4)], axis=-1)
    s = W.sum(axis=-1, keepdims=True)
    W = np.divide(W, s, out=W.copy(), where=s > 1.0)
    img = Image.fromarray(np.clip(np.round(W * 255.0), 0, 255).astype(np.uint8), "RGBA")
    out = GODOT / "data" / "barrow_full_splat.bin"
    img.save(out, format="PNG", optimize=True)
    shares = {k: round(float((cls == v).mean()) * 100, 2) for k, v in (("snow", 0), ("path", 1), ("shrub", 3), ("ice", 4))}
    return {"file": "res://data/barrow_full_splat.bin", "encoding": "PNG bytes (RGBA8)", "origin_xz": SPLAT["origin_xz"],
            "size_m": SPLAT["size_m"], "m_per_px": SPLAT["m_per_px"], "px": [n, n],
            "channels": "R path, G rock (unused), B shrub (juniper and heather), A ice; snow = 1 - sum",
            "blur_sigma_m": 0.08, "class_share_pct_of_raster": shares,
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "_frame": "WORLD xz, not (u, v): the HEAD ground shader samples the splat axis-aligned in world"}


def chunks():
    out = []
    for rr in range(CHUNK["rows"]):
        for c in range(CHUNK["cols"]):
            x0, y0 = c * CHUNK["stride_px"][0], rr * CHUNK["stride_px"][1]
            x1, y1 = x0 + CHUNK["canvas_px"][0], y0 + CHUNK["canvas_px"][1]
            out.append({"key": "%d_%d" % (c, rr), "px": [x0, y0, x1, y1],
                        "ground_uv": {"u": [r3(WIN_U[0] + x0 / PPM), r3(WIN_U[0] + x1 / PPM)],
                                      "v": [r3(WIN_V[1] - y1 / PX_UP), r3(WIN_V[1] - y0 / PX_UP)]}})
    return out


# --- pre-build checks (approximate footprints; the acceptance measures the build) ---------------
def prebuild_checks(P):
    obs = obstacles_of(P)
    walk = walkable_fn(obs)
    cells = walk.cells

    def stand(u, v, w):
        rad = G.stand_radius(w, 0.18)            # 0.18: half a 0.25 m cell's diagonal
        k = int(math.ceil(rad / PRE_STEP))
        i0 = int(round((u - PRE_U[0]) / PRE_STEP))
        j0 = int(round((v - PRE_V[0]) / PRE_STEP))
        return any((i0 + di, j0 + dj) in cells and math.hypot(PRE_U[0] + (i0 + di) * PRE_STEP - u, PRE_V[0] + (j0 + dj) * PRE_STEP - v) <= rad
                   for di in range(-k, k + 1) for dj in range(-k, k + 1))
    sq = G.squeezes(obs, stand)
    # camera margin: every point his centre can stand on, on a 0.25 m grid, framed by the play camera
    worst = {"left_m": 0.0, "right_m": 0.0, "top_m": 0.0, "bottom_m": 0.0}
    n_bad = 0
    n_ok = 0
    for (i, j) in walk.cells:
        u = PRE_U[0] + i * PRE_STEP
        v = PRE_V[0] + j * PRE_STEP
        if True:
            n_ok += 1
            over = {"left_m": REACH_U[0] - u, "right_m": u - REACH_U[1], "bottom_m": REACH_V[0] - v, "top_m": v - REACH_V[1]}
            if max(over.values()) > 0:
                n_bad += 1
            for k in worst:
                worst[k] = max(worst[k], over[k])
    # the door's cover: the mound's surface over the passage roof against the lintel's top (v1: 3.185 m)
    lint_top = 3.185
    cover = min(dome_h(u, v) for u in np.linspace(-1.14, 1.14, 23) for v in np.linspace(CUTTING["v_facade"], PASSAGE["v_end"], 21)) - lint_top
    # the mound's silhouette at the guide's top edge
    sil = max(v + COT * dome_h(u, v) for u in np.linspace(-6, 6, 61) for v in np.linspace(8.5, 17.5, 181))
    return {"squeezes_approx": sq, "camera_margin_approx": {"walkable_samples": n_ok, "samples_outside_reach_box": n_bad,
            "worst_overshoot_m": {k: r3(v) for k, v in worst.items()}, "reach_box_u": [r3(x) for x in REACH_U],
            "reach_box_v": [r3(x) for x in REACH_V]},
            "door_cover_min_m": r3(cover), "mound_silhouette_top_v_eq": r3(sil), "guide_top_v": r3(WIN_V[1])}


def main():
    ensure_bounds()
    P, dev, solved = build()
    splat = make_splat(P)
    g155 = ring_uv(155)
    layout = {
        "_what": "C-9 T10-2 step 1 (spec v2): the Frost King's Barrow, full area, blockout layout. Design numbers from the spec table; finalize.py merges in the BUILT numbers (world transforms, measured sizes, footprints, colliders) from the Godot scene.",
        "_spec": "agentic_orchestration/gandalf/notes/2026-09-29-barrow-full-area-blockout-spec.md (v2)",
        "version": VERSION,
        "_rulings": {"R-C9-73": "fully generated: no Synty, nothing bought",
                     "R-C9-74": "one flat play floor; elevation only by architected steps",
                     "R-C9-75": "blockout first, painted over chunk by chunk"},
        "frame": {
            "units": "metres",
            "u_hat_world": [r3(CY), 0.0, r3(-SY)], "v_hat_world": [r3(-SY), 0.0, r3(-CY)],
            "origin_world": [0.0, 0.0, 0.0],
            "world_from_uv": "x = u*cos47 - v*sin47; z = -u*sin47 - v*cos47; y = height above the floor",
            "theta": "measured clockwise from +v",
            "camera": {"projection": "orthogonal", "pitch_deg": PITCH_DEG, "yaw_deg": YAW_DEG,
                       "px_per_m_across": PPM, "px_per_ground_m_up_screen": r3(PX_UP), "px_per_vertical_m": r3(PPM * CP),
                       "lift_px": CAM_LIFT_PX, "frame_px": [1920, 1080],
                       "frame_reach_from_his_feet_m": {"across": r3(FRAME_HALF_U), "up_screen": r3(FRAME_UP), "down_screen": r3(FRAME_DOWN)}},
            "guide_window": {"u": [r3(WIN_U[0]), r3(WIN_U[1])], "v": [r3(WIN_V[0]), r3(WIN_V[1])], "px": list(GUIDE_PX),
                             "centre_uv": list(WIN_CENTRE),
                             "_px_from_uv": "x = (u - u0) * 100.6176 ; y = (v1 - v) * 80.3076 - h * 60.6175"},
            "reach_box": {"u": [r3(REACH_U[0]), r3(REACH_U[1])], "v": [r3(REACH_V[0]), r3(REACH_V[1])],
                          "_": "where his centre may stand if the camera, centred on him with its 55 px lift, is to show nothing outside the window"},
            "chunks": {"cols": CHUNK["cols"], "rows": CHUNK["rows"], "canvas_px": CHUNK["canvas_px"],
                       "stride_px": CHUNK["stride_px"], "list": chunks(),
                       "_ground_uv": "the ground footprint of each canvas; anything standing up projects UP-screen into the chunk above"},
        },
        "tints_srgb": TINTS,
        "placements": P,
        "regions": {
            "arena": {"type": "disc", "centre_uv": list(ARENA["centre"]), "r": ARENA["r"],
                      "rule": "nothing placed; drifts <= 0.2 m (no 3D snow in the blockout)"},
            "ring": {"type": "circle", "centre_uv": list(RING["centre"]), "r": RING["r"]},
            "ring_entrance": {"type": "gap", "between": ["ring_p155", "ring_m155"],
                              "gate_centres_uv": [[r3(g155[0]), r3(g155[1])], [r3(-g155[0]), r3(g155[1])]]},
            "path": {"type": "polyline", "points_uv": [list(p) for p in PATH["points"]],
                     "extended_off_frame_uv": [[r3(p[0]), r3(p[1])] for p in path_points_extended()],
                     "width_m": PATH["width"], "caps": "butt at the ring entrance; runs off the window's bottom edge",
                     "rule": "path ground; nothing placed on it"},
            "ice": {"type": "ellipse", "centre_uv": list(TARN["centre"]), "axes_m": list(TARN["axes"]), "walkable": True,
                    "rule": "flat and walkable; no snow; W and SW rim is shore rock, E open"},
            "cutting": {"type": "corridor", "half_w_m": CUTTING["half_w"], "v": [r3(mound_foot_v(CUTTING["half_w"])), CUTTING["v_facade"]],
                        "floor_y": 0.0, "walkable": True},
            "shrub_zones": {"components": ["outcrop_skirts (2.5 m)", "under_groves_and_tree_lines (1.7 m per trunk)",
                                           "mound_base_outside_ring (2.2 m)", "tarn_far_shore (2.8 m, W half)",
                                           "thicket_band_ADDED (1.5 m either side of every bounds edge but the entry and the mound's)",
                                           "margin_scrub_ADDED (patches over the margin beyond the bounds)"],
                            "edge_warp_m": 0.45, "never_in": ["arena", "path (+0.35 m)", "ice", "ring_entrance", "cutting"],
                            "raster": "godot/data/barrow_full_splat.bin (PNG bytes), channel B"},
            "splat": splat,
        },
        "bounds": {"polygon_uv": [list(p) for p in BOUNDS], "entry_gap_uv": [list(p) for p in ENTRY_GAP],
                   "wedge_walls_at_the_35_stones": WEDGES,
                   "entry_edge_index": ENTRY_EDGE, "wall_half_thickness_m": WALL_HALF_T,
                   "walls": "invisible vertical boxes 0.3 m thick, 3 m tall, on every edge; the entry edge is the EXIT line (the eventual level transition)",
                   "_routed_by": "the camera-margin reach box (right wall u 15.35, top wall v 10.6) and the no-squeeze rule",
                   "_reads_as": "rock where an outcrop straddles it, G2's trunks, the mound, and the thicket band everywhere else"},
        "knight": {"spawn_uv": [-3.0, -15.0], "spawn_facing": "N", "guide_uv": list(ARENA["centre"]), "guide_facing": "S",
                   "gear_stack": 4, "_gear": "full kit: helmet, bracers, byrnie, mantle, axe, shield"},
        "camera_clamp_default": False,
        "crucible": crucible(P),
        "deviations": dev,
        "groves_search_draws": solved,
    }
    layout["design_checks_prebuild"] = prebuild_checks(P)
    txt = json.dumps(layout, indent=1)
    (ROOT / "barrow_full_layout.json").write_text(txt)
    (GODOT / "data" / "barrow_full_layout.json").write_text(txt)
    print("placements:", len(P), " splat:", splat["px"], splat["class_share_pct_of_raster"], " groves:", solved)
    print(json.dumps(layout["design_checks_prebuild"], indent=1))


if __name__ == "__main__":
    main()
