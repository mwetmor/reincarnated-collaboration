#!/usr/bin/env python3
"""BV2F lane LV -- barrow_v2 ART-FIRST layout of record. PHASE 1'' (Matt R-C9-204/206, plan R-C9-205): the coast, the
water and the paths rebuilt; everything else (barrow, hall, gable, ring, kit-v3) as Phase 1' placed it.

    python3 fid/lv/tools/make_bv2art.py

v1 PRACTICE, MIRRORED (barrow_full/tools/make_layout.py -> barrow_full_layout.json): ONE script turns the composition into
ONE layout everything downstream reads; the frame is v1's camera-aligned (u, v) -- true ground metres, +u screen-right,
+v up-screen, from the play camera's own basis (pitch 52.95354112560294, yaw 47).

Sketch A is drawn at about the play camera's own angle, so its pixels ARE a map (S = 24 px per metre across):
    u = (x - 780) / S          v = (452 - y - z S cos(pitch)) / (S sin(pitch))

PHASE 1'' -- TERRAIN LEVELS (R-C9-204): the PLATEAU at 0 around the start; on the W a sloped SHINGLE BEACH falling 4.2 m
over 10 m to the shore ice where the wreck lies; the SEA at -4.5 (shore-fast ice top -4.2); along the S a CURVING coast of
SEA CLIFFS 6-8 m (the clifftop crest rises to +1.5 .. +3.5 over the last 10 m of the plateau), faced by the Phase 1''
CLIFF KIT (models from sketch A's own cliffs, one uniform scale each), talus and fallen blocks at the foot, rock stacks in the
ice. The SEA CAVE is the kit's cave-arch piece in the eroded face; a natural rock SHELF runs from its mouth to a ROCK-CUT
STAIR in a notch, which climbs ACROSS the face to a flush landing on the clifftop (sketch A's order: cave W, stair E).
WATER: the MERE an organic outline of large cracked ice PLATES over dark water; the STREAM a shallow channel with snowy banks
and ice in it from the barrow to the mere; the SEA ~2/3 ice -- shore-fast ice along the coast, large irregular plates,
then floes of every size (the loose outer floes tagged to bob). NO PATHS.

Writes:
  fid/lv/art/layout_bv2art.json                 the layout of record (v1-style)
  barrow_full/godot/data/bv2f/art/level.json    + terrain_h.f32, classes_png.bin (what scripts/bv2f/bv2f_level.gd reads)
  fid/lv/art/frame_grid_s??.json                the Tier-B --frame-grid configs (2 x 2 guide sections)
"""
import hashlib
import json
import math
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree

import bv2pp_coast as K

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
BV2 = os.path.normpath(os.path.join(LV, "..", ".."))
C9 = os.path.dirname(BV2)
RUNS = os.path.dirname(C9)
BF = os.path.join(C9, "barrow_full", "godot")
OUT = os.path.join(BF, "data", "bv2f", "art")
EXT = os.path.join(BF, "data", "bv2f", "ext")
ART = os.path.join(LV, "art")

PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
SP, CP = math.sin(PITCH), math.cos(PITCH)
PX_V = PPM * SP
S = 24.0                                   # sketch px per metre across
START_PX = (780.0, 452.0)
SEA_Z = -4.5                               # Phase 1'': one sea level
ICE_TOP = SEA_Z + 0.3                      # shore-fast ice / plates freeboard 0.3 m
SEA_FLOOR = SEA_Z - 2.0
BEACH_W = 10.0                             # the shingle beach: 0 -> ICE_TOP over 10 m (23 deg)
HF_PPM = 4.0
EXT_UV = {"u": [-42.0, 42.0], "v": [-36.0, 36.0]}
CLS_PPM = 16.0
V1M = "runs/C-9/barrow_full/web_painted/models/barrow/"
AABB = json.load(open(os.path.join(LV, "models", "glb_aabb.json")))
RNG_SEED = 204


def uv(px, z=0.0):
    """sketch A ground pixel -> (u, v) metres. z < 0: the point is drawn that much lower."""
    x, y = px
    return ((x - START_PX[0]) / S, (START_PX[1] - (y + z * S * CP)) / (S * SP))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ab(glb):
    for k, v in AABB.items():
        if k.endswith(glb.replace("runs/", "", 1)) or (glb.startswith("data/bv2f/") and k.endswith("/" + glb)):
            return v["godot_xyz_m"]
    raise KeyError(glb)


def has_ab(glb):
    try:
        ab(glb)
        return True
    except KeyError:
        return False


def unit(x, y):
    n = math.hypot(x, y)
    return (x / n, y / n)


# ============ THE COMPOSITION (sketch A pixels unless _uv) ============
WRECK = {"glb": "data/bv2f/models/wreck.glb", "prow_uv": (-32.6, 6.4), "stern_uv": (-21.6, -0.6), "len_m": 13.0, "sink": 1.0}
HALL = {"glb": "data/bv2f/models/hall.glb", "door": (1290, 450), "wall_a": (1170, 395), "wall_b": (1345, 515), "len_m": 18.5}
# R-C9-188/189 (Matt): the burnt hall is CLOSED but for its one great door. The kit build's +X gable end (toward the fallen
# gable, SE) is an open burnt frame -- a plank panel closes it, in the build's own local metres (its glTF frame: x along
# the ridge, y up, z across; the end posts stand at x 14.2-16.2), inside the end frame under the roof line; it rides the
# hall's one uniform scale (it is a child of the placed build)
HALL_PANELS = [{"model": "longhall", "x_m": [14.75, 15.15], "poly_zy_m": [[-3.6, 0.0], [6.9, 0.0], [6.9, 3.7], [1.67, 9.1], [-3.6, 3.7]],
                "class": "wood", "what": "plank infill of the open +X gable end (the hall's SE end)"}]
GABLE = {"glb": "data/bv2f/models/gable.glb", "centre": (1430, 585), "size_m": 8.0}
# R-C9-222 (Matt): the BARROW LARGER, like barrow_v1's -- a broad KERBED dome across the top of the scene running off its top
# edge (v1's profile: h = rise (1 - rho^2)^0.35, the kerb steepening over its outer 8 %), kerb stones round it, the carved
# door set in its front (kit-v3 front, one uniform scale)
BARROW = {"glb": "data/bv2f/models/barrow.glb", "door": (828, 115), "width_m": 15.0}
MOUND = {"centre": (828, -84), "semi_m": (17.0, 10.4), "rise_m": 6.5, "exponent": 0.35, "kerb": 0.08}
RING_STAND = [((690, 455), 2.2, "tall"), ((722, 505), 1.7, "mid"), ((780, 385), 1.9, "tall"), ((862, 420), 2.1, "mid"), ((846, 492), 2.0, "tall")]
RING_LIE = [((742, 425), 25.0), ((805, 512), -15.0), ((830, 535), 60.0)]
SLOPE_STONES = [((600, 40), 2.4, "tall"), ((520, 105), 1.8, "mid"), ((690, 185), 2.0, "mid"), ((925, 180), 2.2, "tall"), ((1110, 125), 2.0, "mid"),
                ((1190, 90), 2.3, "tall"), ((380, 365), 1.4, "short")]     # Phase 1'': #7 (930, 700) stood on the new stair's top -- removed
CRAGS = [((1235, 175), 2.0), ((1500, 360), 2.4)]          # Phase 1'': the coastal crags are replaced by the cliff kit's talus
# THE COAST (uv). SHORE: the plateau's W edge = the beach top (land to its east), north -> south; LIP: the S clifftop edge,
# west -> east, from the beach/cliff junction J. The ROUTE stretch of the lip is ONE straight face (A -> B) the cave, the
# shelf and the stair are laid along; the rest of the lip is pushed into bays and headlands (K.wiggle).
# R-C9-226 (2/3): north of the wreck the plateau's W edge moves west (~3-6 m) so the mere can have Matt's 400-500 m2 AND
# sketch A's river can run down beside the coast inside the painted window; the wreck still lies at the beach foot
SHORE_UV = [(-31.2, 27.0), (-31.6, 18.0), (-31.8, 12.6), (-25.5, 11.0), (-19.0, 7.5), (-13.8, 3.6), (-12.6, -1.5), (-14.2, -5.0), (-17.5, -7.0)]
LIP_A, LIP_B = (-12.5, -6.6), (7.95, -19.15)
LIP_UV = [(-17.5, -7.0), (-15.2, -8.9), LIP_A, LIP_B, (11.6, -19.2), (15.4, -21.0), (20.0, -24.7), (24.2, -27.8), (28.3, -30.4), (34.2, -33.8), (40.0, -37.0)]
# R-C9-220 (Matt): the MERE at sketch A's share of the scene (~2.5-3x, ~420 m2), irregular, open snow kept round the ring
MERE_SHAPE = {"centre_uv": (-14.5, 12.2), "radii": (12.5, 7.6), "bed_z": -0.18, "plate_top": -0.04, "plate_m": 3.0}
# R-C9-226 (2): Matt's R-C9-220 size, 400-500 m2 -- an explicit irregular outline (uv) between the shore, the barrow's kerb,
# the open snow round the ring and the cave's knoll; low lobes + a ragged edge are added in main(); scaled to MERE_AREA
MERE_POLY = [(-31.0, 13.4), (-30.5, 15.0), (-28.2, 16.2), (-26.4, 17.6), (-25.4, 20.5), (-25.0, 24.4), (-22.0, 26.4), (-17.5, 26.4),
             (-14.8, 24.6), (-13.6, 21.6), (-10.6, 19.2), (-7.2, 17.4), (-3.8, 15.9), (-1.3, 12.8), (-1.1, 9.2), (-2.9, 6.3), (-6.8, 5.4),
             (-11.2, 4.8), (-14.6, 4.6), (-18.0, 7.0), (-21.8, 9.4), (-25.8, 11.6), (-29.2, 12.4)]
# (its N lobe, between the river and the barrow's W flank, runs off the window's top edge as the barrow does)
MERE_AREA = 440.0
# R-C9-218: a narrow WINDING ribbon of ice from the barrow down to the mere, running on INTO the mere (it widens and merges)
STREAM_UV = [(-3.6, 21.6), (-4.2, 20.8), (-5.0, 20.3), (-5.3, 19.4), (-6.2, 18.8), (-7.2, 18.4), (-8.0, 17.6), (-9.2, 17.0)]   # the barrow's tributary
# R-C9-220 (2): sketch A's RIVER, winding down from the top edge of the scene into the mere
# R-C9-222: the river enters at the TOP-LEFT edge and runs DOWN ALONGSIDE THE COAST, a little inland of the shore, then spreads
# into the mere (not from the barrow)
# R-C9-226 (3): the river IN the painted window (its top edge is v 22.4): it enters at the top-left, winds down beside the
# coast ~2.5 m inland of the beach top, and widens seamlessly into the mere's NW lobe
RIVER_UV = [(-28.6, 27.0), (-28.3, 24.4), (-27.4, 22.6), (-28.1, 20.8), (-27.6, 19.0), (-28.3, 17.4), (-28.6, 15.8), (-28.4, 14.6)]
# R-C9-220 (4): the OUTLET -- the mere drains west over the beach to the shore ice beside the wreck
OUTLET_UV = [(-29.5, 12.6), (-31.0, 11.6), (-32.6, 10.8), (-34.6, 10.3), (-37.0, 10.0)]
CHANNELS = [{"id": "river", "pts": RIVER_UV, "hw": 0.5, "dep": 0.3, "widen": 0.35, "press": False, "open": True},   # R-C9-227 (1): a TINY UN-FROZEN ribbon of open water
            ]   # R-C9-221: no outlet channel -- the mere turns into the sea through one graded ice field
STREAM_SHAPE = {"half_w": 0.8, "bank_w": 0.8, "depth": 0.55, "ice_top_below": 0.33}
YARD = [(1105, 385), (1300, 330), (1525, 470), (1500, 650), (1250, 660), (1140, 545)]
# R-C9-226 (5): the hall's ash yard as sketch A draws it -- trampled ash in an IRREGULAR patch round the great door and the
# fallen gable (no straight edges): YARD's outline resampled and pushed in/out by low lobes + a ragged fringe (own stream)
YARD_SEED = 226
SHRUB = [((470, 330), 70), ((380, 250), 60), ((640, 300), 50), ((600, 455), 45), ((900, 300), 55), ((1000, 470), 60), ((1060, 230), 70),
         ((720, 220), 50), ((1000, 650), 45), ((880, 610), 40), ((470, 60), 60)]
PALISADE = [[(1040, 375), (1110, 340), (1165, 312)], [(1330, 238), (1430, 262), (1530, 300)], [(1150, 560), (1200, 625), (1265, 690), (1420, 702)]]
LOGS = [((1370, 262), (1445, 302)), ((1250, 565), (1330, 622)), ((1300, 625), (1385, 660)), ((1335, 440), (1395, 475))]
# THE ROUTE (R-C9-188/189/206), in the straight-face frame: t along A -> B, s SEAWARD (negative = into the land)
# R-C9-226 (1): the STAIR climbs INLAND (up-screen, its risers facing the camera, as sketch A draws it) in a cleft cut from the
# cove's back-right corner; a stair this long fits between the cliff and the stone ring only EAST of the ring, so the cove
# sits there (cave mouth ~9 m S of the start, the stair to its right). stair_t0: the band's W edge (t); its foot on the
# cove's back line; its top flush with the clifftop there (stair_top_z, the ground's own height)
ROUTE = {"crest": 2.5, "shelf_z": SEA_Z + 1.0, "stair_w": 5.3, "risers": 17, "tread": 0.39, "rise_jitter": 0.12,
         "cave_t": 12.3, "cave_front_s": 0.3, "mouth_w": 6.0, "mouth_h": 7.0,
         "shelf_t": (-3.2, 12.0), "shelf_out_s": 8.8, "pilot_t": -3.2, "shelf_in_s": 0.3, "landing_len": 2.0,
         "stair_t0": 13.8, "stair_top_z": 0.75, "stair_s_foot": -4.6,
         "bounds_out_m": 0.2}       # shelf_t/shelf_out_s/shelf_in_s: ONLY the legacy outline the passed pack ice is partitioned against
# R-C9-212/213/214 (Matt): THE CAVE SECTION IS CARVED -- one eroded rock mass (the terrain itself, its faces eroded), minus a
# COVE the sea cut into the cliff (its floor the iced LANDING just above the water), minus the CAVE worn into the cove's back
# wall, minus the STAIR, a 5.3 m groove cut into the cove's right-hand wall along the face with a low broken uncut lip on
# the sea side (fid/lv/tools/bv2pp_carve.py). Frame t/s as ROUTE's. The coastline outside the cove is untouched.
# R-C9-226 (1) REDESIGN (fid/lv/tools/bv2pp_cove.py): a SHALLOW cove (4.6 m into the face) between the left shoulder and the
# stair; the cave in its back wall (axis angled inland-west, away from the ring); a SMALL iced landing (~6.9 x 5.5 m) at the
# mouth, the sea + floes in the cove's west side reaching into the mouth; the stair groove in the cove's right (east) wall,
# climbing east along the face, its treads separate stone blocks (slabs); every face vertical rock columns
CARVE = {"t": (-7.0, 24.0), "s": (-19.5, 5.0), "step": 0.2, "high_water": SEA_Z + 1.6, "s_face": 0.4, "lip_h": 0.5,
         # R-C9-228: NO cove -- the cliff line is continuous (cliff kit, as 3686cea98/09ba67b23); s_back = the cave mouth's s (the
         # arch is worn into the corner where the face meets the stair gully's W wall, facing the camera); parts = [] (nothing cut)
         "cove": {"t_w": 8.8, "t_e": 19.9, "s_back": -1.5, "round_r": 1.2, "parts": []},
         "landing": {"t_w": 8.8, "t_e": 19.4, "s_front": 1.95, "mouth_r": 3.0},
         "cave_axis_ts": (-0.6, -0.8), "mouth_h_cut": 7.4, "mouth_w_cut": 6.5, "cave_depth": 3.0,
         "col_spacing": 1.7, "land_thr": -1.0, "bed_below": 0.55, "head_margin": 0.4}
# THE CLIFF KIT (Phase 1'' sheets -> Tripo -> uniform scale). Until a piece exists the nearest Phase 1' build stands in.
KIT2 = {"cliffcol": "data/bv2f/models/cliffcol.glb", "cliffcape": "data/bv2f/models/cliffcape.glb",
        "cavearch": "data/bv2f/models/cavearch.glb", "seastack": "data/bv2f/models/seastack.glb"}
KIT2_STANDIN = {"cliffcol": "data/bv2f/models/cliffplain.glb", "cliffcape": "data/bv2f/models/crag.glb",
                "cavearch": "data/bv2f/models/cliffplain.glb", "seastack": "data/bv2f/models/crag.glb"}
# the cave arch's own mouth, measured on the built piece (fraction of its AABB): fid/lv/tools/lv_kit2_measure.py -> kit2/cave_mouth.json
STACKS_UV = [((-21.5, -15.5), 6.2), ((-3.5, -22.0), 4.6), ((16.5, -29.5), 5.4)]
# ================= R-C9-234 (conductor, on Matt's choice): the pilot-area blockout fixes =================
# Every new draw below comes from its OWN stream (seeds 234x) and every legacy stream keeps its draw count, so nothing Matt
# passed (cliffs, cave, stair, ring positions, river course, talus/kit slots) moves.
# (6) the BARROW's FRONT LOBE: v1's door is set INTO its mound (barrow_full_layout.json mound: door at rho ~0.47, a
# stone-lined cutting from the foot to the facade). Here a second kerbed v1-profile dome round the door (centre dv behind the
# threshold), unioned with the big dome, a cutting (half-width cut_hw, flaring at the foot) from its toe to the facade, its
# sides lined with dry-stone walls; it tapers out within mere_clear of the mere's ice
# The cutting is the portal's width (+0.8 m a side) and ends at the build's front face (0.45 m in front of the threshold);
# INSIDE the build's own footprint (its glTF vertices, placed as the level places it) the lobe adds nothing, so the mound
# meets the build's sides and back and never stands in front of its face.
# The lobe sits east of the door (the mere's ice comes to within ~6 m of the door on the west).
MOUND_FRONT = {"du": 2.0, "dv": 3.5, "semi_m": (12.0, 6.5), "rise_m": 6.0, "exponent": 0.35, "kerb": 0.10,
               "cut_hw": 4.5, "cut_flare": 1.2, "cut_back": 0.45, "mere_clear": (0.4, 1.6)}
# (4) the MERE -> SEA margin: ONE graded ice field from the mere's edge down to the beach foot (no land strip, no crease),
# land/reed islands standing out of it, cracks widening into leads and rubble toward the sea. Weight fades (noisy) to the
# south (the shingle by the wreck), to the north (the river's peninsula) and away from the mere.
CORRIDOR = {"v_south": (5.0, 8.0), "v_north": (13.0, 15.5), "d_mere": (9.0, 13.0), "river_clear": (1.4, 3.0), "noise_m": 1.6}
# (3) the SHINGLE: a ragged beach foot (width +-1.8 m of low noise), snow drifts over it (elongated E-W), ice at its foot
BEACH_NOISE = {"bw_amp": 1.8, "sigma_m": 2.2, "relief_m": 0.06}
# (2) REEDS: sketch A's tall pale reed clumps -- thin blades (class `reed`, pale straw) on a straw ground patch; on organic
# low islands in the mere and the margin, along the mere's edges and the river's banks (PT's DEV-21 cards grow from them)
REED_TINT = [0.80, 0.68, 0.46]


def chaikin(poly, f=0.22):
    """one corner-cutting pass (closed polygon): every corner worn round; no random draws"""
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
        out.append((a[0] + (b[0] - a[0]) * (1 - f), a[1] + (b[1] - a[1]) * (1 - f)))
    return out


def kit(name):
    g = KIT2[name]
    return g if has_ab(g) else KIT2_STANDIN[name]


def crest_fn(s, s_route):
    """the clifftop crest height along the lip's arc length s: 6-8 m cliffs (+1.5 .. +3.5 over the -4.5 sea), rising from
    the beach junction over its first 8 m; ROUTE['crest'] exactly along the straight route face"""
    f = 2.5 + 0.75 * math.sin(s / 8.5 + 1.2) + 0.25 * math.sin(s / 3.7 + 0.4)
    f = min(1.0, s / 8.0) * f
    a, b = s_route
    w = min(1.0, max(0.0, min(s - (a - 4.0), (b + 4.0) - s) / 4.0))
    return f * (1 - w) + ROUTE["crest"] * w


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(ART, exist_ok=True)
    os.makedirs(EXT, exist_ok=True)
    rng = np.random.default_rng(RNG_SEED)
    prng = __import__("random").Random(RNG_SEED)
    rng209 = __import__("random").Random(209)                  # R-C9-209/211 stair + shelf draws: their own stream (nothing else moves)
    # ---------------- the coast chains ----------------
    shore, _ = K.wiggle(SHORE_UV, lambda s: 0.9 * math.sin(s / 5.0 + 0.3) + 0.4 * math.sin(s / 2.3) + 0.35 * math.sin(s / 1.15 + 0.8), step=0.6, taper=3.0)   # R-C9-226 (5): no straight runs
    a_s = sum(math.dist(p, q) for p, q in zip(LIP_UV[:2], LIP_UV[1:3]))
    b_s = a_s + math.dist(LIP_A, LIP_B)
    s_route = (a_s, b_s)
    lip0, _ = K.wiggle(LIP_UV, lambda s: 1.8 * math.sin(s / 6.0 + 0.7) + 0.9 * math.sin(s / 2.7 + 2.1), step=1.0, taper=3.0,
                       keep=lambda s: min(1.0, max(0.0, max(a_s - 1.0 - s, s - (b_s + 1.0)) / 3.0)))
    # R-C9-230: the clifftop LEFT of the sea cave is no straight block -- the lip there is lobed and notched too (only the
    # stretch the carved cave + gully stand on, t >= ~7, stays straight); the pack ice is still laid out against lip0 (as passed)
    wl_ = lambda s: min(1.0, max(0.0, (a_s + 7.0 - s) / 2.0))
    lip, lip_s = K.wiggle(LIP_UV, lambda s: 1.8 * math.sin(s / 6.0 + 0.7) + 0.9 * math.sin(s / 2.7 + 2.1) + 0.6 * math.sin(s / 1.25 + 0.4) * wl_(s), step=1.0, taper=3.0,
                          keep=lambda s: min(1.0, max(0.0, max(a_s + 6.0 - s, s - (b_s + 1.0)) / 3.0)))
    shore0 = list(shore)
    shore[-1] = lip[0]
    coast = shore + lip[1:]
    coast0 = shore0[:-1] + [lip0[0]] + lip0[1:]
    lip_tree = cKDTree(np.array(lip))
    crest = np.array([crest_fn(s, s_route) for s in lip_s])
    # the route frame (straight face A -> B): t along, s seaward
    dR = unit(LIP_B[0] - LIP_A[0], LIP_B[1] - LIP_A[1])
    nR = (dR[1], -dR[0])

    def fr(t, s):
        return (LIP_A[0] + dR[0] * t + nR[0] * s, LIP_A[1] + dR[1] * t + nR[1] * s)

    def to_fr(p):
        dx, dy = p[0] - LIP_A[0], p[1] - LIP_A[1]
        return (dx * dR[0] + dy * dR[1], dx * nR[0] + dy * nR[1])
    R = ROUTE
    W_ = R["stair_w"]
    n_r = R["risers"]
    top_z = R["stair_top_z"]
    rise = (top_z - R["shelf_z"]) / n_r
    n_tr = n_r - 1
    t0s, t1s = R["stair_t0"], R["stair_t0"] + W_                 # the stair band (t)
    s_foot = R["stair_s_foot"]                                    # R-C9-228: the treads start here; seaward of it the gully's floor is the small iced ledge
    s_top = s_foot - n_tr * R["tread"]
    s_land = s_top - R["landing_len"]
    t_foot = t0s                                                  # (the landing runs from the cave mouth to here)
    # ---------------- terrain + classes over EXT_UV ----------------
    u0, u1 = EXT_UV["u"]
    v0, v1 = EXT_UV["v"]
    W = int((u1 - u0) * HF_PPM) + 1
    H = int((v1 - v0) * HF_PPM) + 1
    us = u0 + np.arange(W) / HF_PPM
    vs = v1 - np.arange(H) / HF_PPM
    U, V = np.meshgrid(us, vs)

    def mask(poly, Uq, Vq, ppm, ou, ov):
        img = Image.new("L", (Uq.shape[1], Uq.shape[0]), 0)
        ImageDraw.Draw(img).polygon([((p[0] - ou) * ppm, (ov - p[1]) * ppm) for p in poly], fill=1)
        return np.asarray(img).astype(bool)

    def dist_to_chain(chain, Uq, Vq):
        d = np.full(Uq.shape, 1e9)
        for (a, b) in zip(chain[:-1], chain[1:]):
            ax, ay, bx, by = a[0], a[1], b[0], b[1]
            dx, dy = bx - ax, by - ay
            t = np.clip(((Uq - ax) * dx + (Vq - ay) * dy) / (dx * dx + dy * dy), 0, 1)
            d = np.minimum(d, np.hypot(Uq - (ax + t * dx), Vq - (ay + t * dy)))
        return d
    land_poly = coast + [(u1 + 5, lip[-1][1]), (u1 + 5, v1 + 5), (shore[0][0], v1 + 5)]
    land = mask(land_poly, U, V, HF_PPM, u0, v1)
    land0 = mask(coast0 + [(u1 + 5, lip0[-1][1]), (u1 + 5, v1 + 5), (shore[0][0], v1 + 5)], U, V, HF_PPM, u0, v1)   # the pack's coast (as passed)
    d_shore = dist_to_chain(shore, U, V)
    d_lip = dist_to_chain(lip, U, V)
    _, near = lip_tree.query(np.c_[U.ravel(), V.ravel()])
    Hc = ndimage.gaussian_filter(crest[near].reshape(U.shape), sigma=2.0 * HF_PPM)    # smooth: no step where the nearest lip point jumps
    west = ~land & (d_shore < d_lip)
    south = ~land & ~west
    Z = np.zeros(U.shape, np.float32)
    # the clifftop rises to the crest over the last 17 m (flat within 7 m of the lip)
    rampf = np.clip(1.0 - np.maximum(0.0, d_lip - 7.0) / 10.0, 0.0, 1.0)
    rampf = rampf * rampf * (3 - 2 * rampf)
    Z = np.where(land, Hc * rampf * np.clip((d_shore + 6.0 - d_lip) / 5.0, 0.0, 1.0), Z)       # eased toward the W beach (no step)
    # W: the shingle beach 0 -> ICE_TOP over BEACH_W (a smooth slope), then the sea floor
    BW = BEACH_W - 4.0 * np.clip((V - 6.0) / 8.0, 0, 1)          # 10 m at the wreck, narrowing to 6 m north of it (sketch A: the ice comes in by the mere)

    def smooth_noise(seed, sigma_m, shape=None, aniso=(1.0, 1.0)):
        n_ = ndimage.gaussian_filter(np.random.default_rng(seed).standard_normal(shape or U.shape), (sigma_m * aniso[1] * HF_PPM, sigma_m * aniso[0] * HF_PPM))
        return n_ / (n_.std() + 1e-9)
    # R-C9-234 (3): the beach foot RAGGED -- its width wanders inward by up to bw_amp (low noise), never a parallel offset of
    # the shore; the shore ice fills the bays it leaves (the pack is still laid out against the passed beach, beach0, so no
    # legacy draw moves and no floe overlaps the slope)
    BW0 = BW
    beach0 = west & (d_shore <= BW0)
    BW = BW0 - BEACH_NOISE["bw_amp"] * np.clip((smooth_noise(2341, BEACH_NOISE["sigma_m"]) + 1.2) / 2.4, 0.0, 1.0)
    bt = np.clip(d_shore / BW, 0, 1)
    beach_z = ICE_TOP * (bt * bt * (3 - 2 * bt) * 0.35 + bt * 0.65)
    beach_z = beach_z + BEACH_NOISE["relief_m"] * smooth_noise(2342, 0.7) * np.sin(np.pi * bt)     # a little relief (not a planar slab)
    beach = west & (d_shore <= BW)
    Z = np.where(beach, beach_z, Z)
    Z = np.where(west & ~beach, SEA_FLOOR, Z)
    bay_ice = beach0 & ~beach                                    # R-C9-234 (3): the foot's bays are shore-fast ice (walkable ground)
    Z = np.where(bay_ice, ICE_TOP - 0.03, Z)
    # S: the cliff face (heightfield behind the kit) from the crest to the sea floor within 1.2 m
    Z = np.where(south, Hc - (Hc - SEA_FLOOR) * np.clip(d_lip / 1.2, 0, 1) ** 0.6, Z)
    # N: the barrow mound + forecourt cut, the snow swells
    mc = uv(MOUND["centre"])
    a_, b_ = MOUND["semi_m"]
    rho = np.hypot((U - mc[0]) / a_, (V - mc[1]) / b_)
    kerb_w = np.clip((1.0 - rho) / MOUND["kerb"], 0, 1)
    dome = MOUND["rise_m"] * np.clip(1 - rho ** 2, 0, None) ** MOUND["exponent"] * (kerb_w * kerb_w * (3 - 2 * kerb_w)) ** 0.5
    bdc = uv(BARROW["door"])
    fc = (np.abs(U - bdc[0]) < 8.5) & (V < bdc[1] + 1.0)
    dome = np.where(fc, 0.0, dome)
    # R-C9-234 (6): the FRONT LOBE round the door (v1's door set into its mound) + the cutting to the facade. Its mere taper
    # is applied once the mere exists (below); here the bare lobe
    MF = MOUND_FRONT
    lc_ = (bdc[0] + MF["du"], bdc[1] + MF["dv"])
    rho_f = np.hypot((U - lc_[0]) / MF["semi_m"][0], (V - lc_[1]) / MF["semi_m"][1])
    kw_f = np.clip((1.0 - rho_f) / MF["kerb"], 0, 1)
    lobe = MF["rise_m"] * np.clip(1 - rho_f ** 2, 0, None) ** MF["exponent"] * (kw_f * kw_f * (3 - 2 * kw_f)) ** 0.5
    v_fac = bdc[1] - MF["cut_back"]                                  # the cutting runs from the toe to just behind the facade's front
    toe_v = lc_[1] - MF["semi_m"][1]
    hw_cut = MF["cut_hw"] + MF["cut_flare"] * np.clip((v_fac - V) / max(v_fac - toe_v, 0.1), 0, 1)
    cut_w = np.clip((np.abs(U - bdc[0]) - hw_cut) / 0.9, 0, 1)            # the cutting's sides (behind the dry-stone walls)
    in_cut_v = V < v_fac
    lobe = np.where(in_cut_v, lobe * cut_w, lobe)
    # the barrow build's footprint (+0.5 m): read its vertices, placed as the level places it (yaw 0, one uniform scale,
    # the AABB centre on the slot's position)
    import struct as _st2
    _b2 = open(os.path.join(BF, BARROW["glb"]), "rb").read()
    _n2 = _st2.unpack("<I", _b2[12:16])[0]
    _J2 = json.loads(_b2[20:20 + _n2]); _o2 = 20 + _n2
    _B2 = _b2[_o2 + 8:_o2 + 8 + _st2.unpack("<I", _b2[_o2:_o2 + 4])[0]]
    _P2 = []
    for _nd in _J2["nodes"]:
        if "mesh" not in _nd:
            continue
        for _pr in _J2["meshes"][_nd["mesh"]]["primitives"]:
            _a = _J2["accessors"][_pr["attributes"]["POSITION"]]; _bv = _J2["bufferViews"][_a["bufferView"]]
            _X = np.frombuffer(_B2, "<f4", _a["count"] * 3, _bv.get("byteOffset", 0) + _a.get("byteOffset", 0)).reshape(-1, 3)
            _P2.append(_X * np.array(_nd.get("scale", [1, 1, 1])) + np.array(_nd.get("translation", [0, 0, 0])))
    _P2 = np.concatenate(_P2)
    _c2 = (_P2.min(0) + _P2.max(0)) / 2
    _sb2 = BARROW["width_m"] / ab(BARROW["glb"])[0]
    _bu, _bv_ = bdc[0], bdc[1] + 8.2 * _sb2                               # the slot centre (as placed below)
    fu = (_P2[:, 0] - _c2[0]) * _sb2 + _bu
    fv = -((_P2[:, 2] - _c2[2]) * _sb2 - _bv_)
    fp_b = np.zeros(U.shape, bool)
    fp_b[np.clip(np.round((v1 - fv) * HF_PPM).astype(int), 0, H - 1), np.clip(np.round((fu - u0) * HF_PPM).astype(int), 0, W - 1)] = True
    fp_b = ndimage.binary_closing(fp_b, iterations=3)
    fp_b = ndimage.binary_fill_holes(fp_b)
    fp_b = ndimage.binary_dilation(fp_b, iterations=2)
    lobe = np.where(fp_b, 0.0, lobe)
    lobe_excess = np.where(land, np.maximum(0.0, lobe - dome), 0.0)      # what the lobe adds over the big dome (tapered at the mere below)
    dome = np.maximum(dome, lobe)
    Z = np.where(land, np.maximum(Z, dome), Z)
    swell = 0.35 * np.sin(U / 6.3 + 1.1) * np.sin(V / 5.1 + 0.4) * np.clip((np.hypot(U, V) - 22.0) / 8.0, 0, 1)
    Z = np.where(land & (dome < 0.05) & (d_lip > 9.0), Z + np.maximum(swell, 0), Z)
    # THE MERE: an organic outline, its bed (dark water) under the plates
    K.blob(MERE_SHAPE["centre_uv"], MERE_SHAPE["radii"], prng, n=72, amp=0.18)     # (its draws keep the legacy stream's order)
    # R-C9-226 (2): MERE_POLY made organic (low lobes + a ragged fringe, own stream), then scaled about its centroid until the
    # ice ON THE LAND is MERE_AREA m2 (Matt R-C9-220: 400-500)
    rngm = __import__("random").Random(2262)
    base = K.resample(MERE_POLY + [MERE_POLY[0]], 0.5)[:-1]
    cb = K.centroid(base)
    ph1, ph2, ph3 = rngm.uniform(0, 6.3), rngm.uniform(0, 6.3), rngm.uniform(0, 6.3)
    mere0 = []
    for i, q in enumerate(base):
        a = math.atan2(q[1] - cb[1], q[0] - cb[0])
        f = 1.0 + 0.045 * math.sin(3 * a + ph1) + 0.03 * math.sin(5 * a + ph2) + 0.018 * math.sin(9 * a + ph3) + rngm.uniform(-0.012, 0.012)
        mere0.append((cb[0] + (q[0] - cb[0]) * f, cb[1] + (q[1] - cb[1]) * f))
    lo_, hi_ = 0.94, 1.12
    for _ in range(22):
        sc_ = (lo_ + hi_) / 2
        mere = [(cb[0] + (q[0] - cb[0]) * sc_, cb[1] + (q[1] - cb[1]) * sc_) for q in mere0]
        a_m = float((mask(mere, U, V, HF_PPM, u0, v1) & land).sum()) / HF_PPM ** 2
        lo_, hi_ = (sc_, hi_) if a_m < MERE_AREA else (lo_, sc_)
    mere_area_land = a_m
    mc_r = K.centroid(mere)
    mere_m = mask(mere, U, V, HF_PPM, u0, v1) & land
    # R-C9-234 (6): the front lobe eases down to the mere's edge (never a cliff into the ice)
    mere_full = mask(mere, U, V, HF_PPM, u0, v1)
    d_mere = ndimage.distance_transform_edt(~mere_full) / HF_PPM
    mc0, mc1 = MOUND_FRONT["mere_clear"]
    tap_ = np.clip((d_mere - mc0) / (mc1 - mc0), 0, 1)
    tap_ = tap_ * tap_ * (3 - 2 * tap_)
    Z = np.where(land & ~mere_m, Z - lobe_excess * (1.0 - tap_), Z)
    lobe_eff = lobe_excess * tap_
    Z = np.where(mere_m, MERE_SHAPE["plate_top"], Z)       # R-C9-208 (4): one continuous ice surface (cracks and seams are drawn on it)
    # THE STREAM: a shallow channel with snowy banks, barrow -> mere
    stream = K.resample(STREAM_UV, 0.5)
    hw_st, bw_st, dep = STREAM_SHAPE["half_w"], STREAM_SHAPE["bank_w"], STREAM_SHAPE["depth"]
    rngw = __import__("random").Random(220)                # R-C9-218/220 water draws: their own stream
    ch_fields = []

    def channel_fn(ch):
        """distance to the channel's line, its local half-width (widening over the last 3 m as it flows into the mere), its
        local depth (tapering to flush with the mere's ice at the mouth) and the mouth weight; the ice IS the channel floor"""
        cf_ = K.resample(ch["pts"], 0.1)
        cl_ = np.cumsum([0.0] + [math.dist(a, b) for a, b in zip(cf_[:-1], cf_[1:])])
        mouth = next((L_ for q, L_ in zip(cf_, cl_) if K.point_in_poly(q, mere)), cl_[-1]) if ch["widen"] > 0 else cl_[-1] + 99.0
        tree = cKDTree(np.array(cf_))

        def f(Uq, Vq):
            dq, iq = tree.query(np.c_[Uq.ravel(), Vq.ravel()])
            Lq = cl_[iq].reshape(Uq.shape)
            tm = np.clip((mouth - Lq) / 3.0, 0.0, 1.0)
            hw_q = ch["hw"] * (0.8 + 0.2 * np.sin(Lq * 1.1)) + (1.0 - tm) * ch["widen"]
            dep_q = 0.04 + (ch["dep"] - 0.04) * tm
            return dq.reshape(Uq.shape), hw_q, dep_q, tm
        return f, cf_, cl_, mouth
    for ch in CHANNELS:
        f_, cf_, cl_, mouth = channel_fn(ch)
        d_c, hw_c, dep_c_, tm_c = f_(U, V)
        prof = np.where(d_c < hw_c, 1.0, np.clip(1 - (d_c - hw_c) / bw_st, 0, 1) ** 1.5)
        where_ = (land | beach) if ch.get("beach") else land
        if ch.get("beach"):
            # the outlet: the mere's ice grading down the beach to the shore ice (a frozen run-off, flush with the ground)
            Z = np.where(where_ & (d_c < hw_c + bw_st) & ~mere_m, Z - ch["dep"] * prof, Z)
        else:
            Z = np.where(where_ & (d_c < hw_c + bw_st) & ~mere_m, Z - dep_c_ * prof, Z)
        ch_fields.append((ch, f_, cf_, cl_, mouth))
    d_st = np.min([f_(U, V)[0] for _, f_, _, _, _ in ch_fields], axis=0)
    # ================= R-C9-234 (4): THE MERE -> SEA MARGIN, ONE GRADED ICE FIELD =================
    # b = 0 at the mere's ice edge, 1 at the beach foot (the shore ice): the ground eases from the mere's ice down to the shore
    # ice along b (the beach's own profile), so there is no land strip, no crease at the old shore line and no edge between
    # the mere and the sea; wG (noisy, soft) says where the field holds -- it fades into the shingle (S), the river's
    # peninsula (N) and the open snow (E)
    def ramp(x, a, b_):
        t_ = np.clip((x - a) / (b_ - a), 0.0, 1.0)
        return t_ * t_ * (3 - 2 * t_)
    CO = CORRIDOR
    rn_c = smooth_noise(2343, CO["noise_m"])
    jit_v = 1.3 * rn_c
    sd_shore = np.where(land, -d_shore, d_shore)                      # signed: + seaward of the shore chain
    to_foot = np.maximum(BW - sd_shore, 0.3)
    b_f = np.clip(d_mere / (d_mere + to_foot), 0.0, 1.0)
    wG = ramp(V + jit_v, *CO["v_south"]) * np.where(land, 1.0 - ramp(V + jit_v, *CO["v_north"]), 1.0) * (1.0 - ramp(d_mere + 1.2 * rn_c, *CO["d_mere"])) \
        * ramp(d_st + 0.4 * rn_c, *CO["river_clear"]) * (1.0 - ramp(np.where(land, d_shore, 0.0) + 1.0 * rn_c, 6.0, 9.0))
    wG = np.where((land | beach) & ~mere_m, wG, 0.0)
    Z_G = MERE_SHAPE["plate_top"] + (ICE_TOP - MERE_SHAPE["plate_top"]) * (0.35 * b_f * b_f * (3 - 2 * b_f) + 0.65 * b_f)
    Z = np.where(wG > 0.0, Z * (1.0 - wG) + Z_G * wG, Z)
    Tq = (U - LIP_A[0]) * dR[0] + (V - LIP_A[1]) * dR[1]
    Sq = (U - LIP_A[0]) * nR[0] + (V - LIP_A[1]) * nR[1]
    # the clifftop round the top landing is held at the crest (flush on every side), easing down over 4 m
    # the clifftop round the stair's top pad is held at the pad's height (flush on every side), easing back over 7 m
    dt_ = np.maximum(0.0, np.maximum((t0s - 1.0) - Tq, Tq - (t1s + 1.0)))
    ds_ = np.maximum(0.0, np.maximum((s_land - 1.5) - Sq, Sq - (s_top + 0.5)))
    wl = np.clip(1.0 - np.hypot(dt_, ds_) / 7.0, 0.0, 1.0)
    wl = wl * wl * (3 - 2 * wl)
    Z = np.where(land & (wl > 0.0), Z + (top_z - Z) * wl, Z)
    # THE ROUTE: the shelf (natural sea-worn rock, irregular outer edge), the cave floor, the stair's notch + bed, the landing
    Tq = (U - LIP_A[0]) * dR[0] + (V - LIP_A[1]) * dR[1]
    Sq = (U - LIP_A[0]) * nR[0] + (V - LIP_A[1]) * nR[1]
    # R-C9-226 (1): the KNOLL over the cave -- only as much rock as the 7 m arch needs over it (1.3 m of roof + a margin), a
    # tapered capsule along the cave's axis (its tunnel narrows and lowers as it recedes), easing to the clifftop over 1.5 m;
    # the columns (bv2pp_cove) step it into snow-capped ledges. It stays clear of the stone ring, the mere and the beach.
    cax = unit(*CARVE["cave_axis_ts"])
    sb_ = CARVE["cove"]["s_back"]
    k_need = lambda a_c: 1.0 - 0.5 * np.clip(a_c / CARVE["cave_depth"], 0, 1)

    def head_w(tq, sq):
        a_ = (tq - R["cave_t"]) * cax[0] + (sq - sb_) * cax[1]
        a_c = np.clip(a_, -1.0, 3.6)
        dq = np.hypot(tq - (R["cave_t"] + cax[0] * a_c), sq - (sb_ + cax[1] * a_c))
        rq = CARVE["mouth_w_cut"] / 2 * k_need(a_c) + 0.9
        w_ = np.clip(1.0 - np.maximum(0.0, dq - rq) / 1.5, 0.0, 1.0)
        need = R["shelf_z"] + CARVE["mouth_h_cut"] * k_need(a_c) + 1.3 + CARVE["head_margin"]
        return w_ * w_ * (3 - 2 * w_), need
    d_water = np.minimum(ndimage.distance_transform_edt(~mere_m) / HF_PPM, d_st)
    wh, need_h = head_w(Tq, Sq)
    wh = wh * np.clip((d_water - 2.0) / 4.0, 0.0, 1.0) * np.clip((d_shore - 1.0) / 3.0, 0.0, 1.0)
    Z = np.where(land & (wh > 0.0), Z + np.maximum(0.0, need_h - Z) * wh, Z)
    head_z_max = float(np.max(np.where(land & (wh > 0.0), Z, -99.0)))
    t0_s, t1_s = R["shelf_t"]
    # the sea ice is laid out against the M1'' shelf outline (Matt passed that ice; its partition and every random draw after
    # it stay exactly as they were); R-C9-214 fills the old shelf's place with shore-fast ice of its own (below)
    shelf_legacy = K.ccw([fr(t0_s, R["shelf_in_s"])] + [fr(t, 7.6 + 0.45 * math.sin(t * 1.3 + 0.5) + 0.25 * math.sin(t * 3.1)) for t in np.arange(t0_s, t1_s + 0.01, 0.5)] +
                         [fr(t1_s + 0.3, 7.6 - 1.0), fr(t1_s + 0.3, 0.45)])
    shelf_ice_m = mask(shelf_legacy, U, V, HF_PPM, u0, v1)
    shelf_m = np.zeros(U.shape, bool)                          # R-C9-212/213/214: no separate shelf -- the landing is cut in the cove

    # THE WRECK'S CRADLE (P6' 761a48353): the hull lies heeled and half-sunk in the SHORE ICE, never in the beach -- under its
    # footprint (+1 m) the ground is the shore ice, easing back up to the beach over 2.5 m (no beach terrain clips the hull)
    wpa, wpb = WRECK["prow_uv"], WRECK["stern_uv"]
    wax = unit(wpb[0] - wpa[0], wpb[1] - wpa[1])
    wcn = ((wpa[0] + wpb[0]) / 2, (wpa[1] + wpb[1]) / 2)
    wl_ = (U - wcn[0]) * wax[0] + (V - wcn[1]) * wax[1]
    wd_ = (U - wcn[0]) * -wax[1] + (V - wcn[1]) * wax[0]
    half_l, half_b = WRECK["len_m"] / 2 + 1.0, ab(WRECK["glb"])[2] * (WRECK["len_m"] / ab(WRECK["glb"])[0]) / 2 + 1.0
    dout = np.hypot(np.maximum(0.0, np.abs(wl_) - half_l), np.maximum(0.0, np.abs(wd_) - half_b))
    # R-C9-228 (2): the cradle's outline RAGGED (no rectangle): its distance pushed in/out by low noise, a rounded footprint
    _cn = ndimage.gaussian_filter(np.random.default_rng(2281).standard_normal(U.shape), 1.6 * HF_PPM)
    _cn /= _cn.std() + 1e-9
    dout = np.maximum(0.0, np.hypot(np.maximum(0.0, np.abs(wl_) - half_l * 0.8), np.maximum(0.0, np.abs(wd_) - half_b * 0.55)) - 1.6 + 1.1 * _cn)
    cw_r = np.clip(1.0 - dout / 2.5, 0.0, 1.0)
    cw_r = cw_r * cw_r * (3 - 2 * cw_r)
    cradle = (cw_r > 0.0) & ~land & (Z > ICE_TOP - 0.03)
    Z = np.where(cradle, Z + (ICE_TOP - 0.03 - Z) * cw_r, Z)
    cradle_ice = (cw_r >= 0.999) & ~land
    # ---------------- the SEA ICE (R-C9-204 (4)): shore-fast ice, large plates, floes of every size ----------------
    solid = land0 | beach0 | shelf_ice_m                      # R-C9-234: the pack against the PASSED beach (no legacy draw moves)
    D = ndimage.distance_transform_edt(~solid) / HF_PPM

    def D_at(p):
        i = int(round((p[0] - u0) * HF_PPM))
        j = int(round((v1 - p[1]) * HF_PPM))
        if 0 <= i < W and 0 <= j < H:
            return float(D[j, i]) if not solid[j, i] else -1.0
        return 99.0

    def noise(p, f=0.11, ph=0.0):
        return 0.5 + 0.5 * math.sin(p[0] * f + 1.7 + ph) * math.cos(p[1] * f * 1.3 + 0.4 + ph)

    def zone(p):
        d = D_at(p)
        if d < 0:
            return None
        if d < 3.2 + 3.0 * noise(p):
            return "fast"
        if d < 11.0 + 5.0 * noise(p, 0.08, 2.0):
            return "plate"
        return "floe"
    box = (-40.0, -34.0, 38.0, 30.0)                      # the sea within (and around) the window: W and S of the coast
    # R-C9-208 (3): SKETCH A'S BROKEN PACK -- plates of every size (fine Voronoi cells merged by a WEIGHTED coarse partition, so
    # one plate is three cells and the next forty), varied freeboard, snow-heaped rims, pressure ridges of rubble blocks,
    # brash in the leads, irregular dark leads of varied width; dense at the shore-fast edge, looser offshore
    from scipy.spatial import cKDTree as _KD
    fine = K.jitter_seeds(box, 0.9, prng, lambda p: True)
    coarse, cz, cw = [], [], []
    for zn, sp, wl, wh in (("fast", 6.5, 0.8, 1.5), ("plate", 3.6, 0.55, 1.6), ("floe", 2.2, 0.5, 1.5)):
        got = K.jitter_seeds(box, sp, prng, lambda p, zn=zn: zone(p) == zn)
        coarse += got
        cz += [zn] * len(got)
        cw += [prng.uniform(wl, wh) for _ in got]
    ctree = _KD(np.array(coarse))
    # R-C9-227 (3): break the pack's regularity -- plate weights spread far wider (some plates huge, some tiny), gaps of very
    # different width, rough edges of varied amplitude, rubble zones; all from their OWN stream (rngs) so the legacy prng
    # draw order -- and everything placed after the pack (talus, ...) -- is unchanged
    rngs = __import__("random").Random(2272)
    rngR = __import__("random").Random(2352)                   # R-C9-234 (5): ridge rubble shapes
    cw_a = np.array([w_ * math.exp(rngs.gauss(0.0, 0.6)) for w_ in cw])
    plate_of = []
    for p in fine:
        if zone(p) is None:
            plate_of.append(-1)
            continue
        dd, ii = ctree.query(p, k=8)
        plate_of.append(int(ii[int(np.argmin(dd / cw_a[ii]))]))
    plates = K.merged_plates(fine, plate_of, box)

    def lead(p):
        return min(abs(math.sin(0.19 * p[0] + 1.3 * math.sin(0.11 * p[1] + 0.7))), abs(math.sin(0.13 * p[1] - 0.17 * p[0] + 2.0)) * 1.3)
    ice, fast_raw, rims, ridges = [], [], [], []
    for k, raw in plates.items():
        zn = cz[k]
        n_ice0, n_rim0, n_rid0 = len(ice), len(rims), len(ridges)
        rubble = zn != "fast" and rngs.random() < 0.16
        gmul = min(3.0, max(0.25, math.exp(rngs.gauss(0.0, 0.6))))
        ramp_ = rngs.uniform(0.8, 2.4)
        raw = K.ccw(K.simplify(raw, 0.35 if zn != "floe" else 0.22))
        if len(raw) < 3:
            continue
        c = K.centroid(raw)
        d = D_at(c)
        ld = lead(c) < 0.12
        if zn == "fast":
            fast_raw.append(raw)
            g = prng.uniform(0.04, 0.1) + (prng.uniform(0.25, 0.6) if ld else 0.0)
            top = ICE_TOP + prng.uniform(-0.03, 0.04)
        elif zn == "plate":
            g = 0.8 * (prng.uniform(0.12, 0.4) + 0.03 * max(0.0, d - 6.0) + (prng.uniform(0.6, 1.6) if ld else 0.0))   # R-C9-226: ~2/3 ice (pack re-rolled)
            top = ICE_TOP + prng.uniform(-0.08, 0.25)
        else:
            if prng.random() < min(0.55, 0.12 + 0.03 * max(0.0, d - 11.0)):   # R-C9-226: ~2/3 ice after the coast moved (the pack re-rolled)
                continue                                   # open water between the floes, more of it further out
            g = prng.uniform(0.15, 0.6) * math.sqrt(max(K.area(raw), 0.5)) * 0.35 + (prng.uniform(0.3, 0.9) if ld else 0.0)
            top = ICE_TOP + prng.uniform(-0.14, 0.12)
        poly = K.inset(raw, g * gmul)
        if len(poly) < 3:
            continue
        poly = K.ccw(K.roughen(poly, prng, (0.1 if zn != "fast" else 0.06) * ramp_, 0.8))
        if K.area(poly) < 0.12:
            continue
        bob = zn == "floe" and d > 15.0 and prng.random() < 0.45
        # R-C9-234 (5): the floe drawn with its corners worn round (one corner-cutting pass, no draws); its rims/ridges below
        # still follow the legacy outline so every legacy draw keeps its count
        ice.append({"zone": zn, "poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(chaikin(poly))], "top": round(top, 3), "bob": bob,
                    "poly_leg": [[round(q[0], 3), round(q[1], 3)] for q in poly]})
        A = K.area(poly)
        if zn in ("fast", "plate") and A > 4.0 and prng.random() < 0.45:
            # a snow-heaped RIM along 30-70 % of the plate's edge (the wind side heaps it)
            n_ = len(poly)
            i0 = prng.randrange(n_)
            run = max(2, int(n_ * prng.uniform(0.15, 0.4)))
            wdt = prng.uniform(0.15, 0.32)
            hh = top + prng.uniform(0.05, 0.14)
            for j in range(i0, i0 + run):
                e0, e1 = poly[j % n_], poly[(j + 1) % n_]
                L_ = math.dist(e0, e1)
                if L_ < 0.05:
                    continue
                inn = (-(e1[1] - e0[1]) / L_, (e1[0] - e0[0]) / L_)
                w0 = wdt * prng.uniform(0.6, 1.0)
                rims.append({"poly": [[round(e0[0], 3), round(e0[1], 3)], [round(e1[0], 3), round(e1[1], 3)],
                                      [round(e1[0] + inn[0] * w0, 3), round(e1[1] + inn[1] * w0, 3)], [round(e0[0] + inn[0] * w0, 3), round(e0[1] + inn[1] * w0, 3)]],
                             "z0": round(top - 0.05, 3), "z1": round(hh + prng.uniform(-0.05, 0.05), 3)})
        if zn == "plate" and A > 2.0 and prng.random() < 0.35:
            # a PRESSURE RIDGE: rubble blocks heaped along one stretch of the plate's edge
            n_ = len(poly)
            i0 = prng.randrange(n_)
            for j in range(i0, i0 + max(2, int(n_ * prng.uniform(0.2, 0.45)))):
                e0, e1 = poly[j % n_], poly[(j + 1) % n_]
                L_ = math.dist(e0, e1)
                m_ = max(1, int(L_ / 0.45))
                for t_ in range(m_):
                    f = (t_ + 0.5) / m_
                    cx, cy = e0[0] + (e1[0] - e0[0]) * f, e0[1] + (e1[1] - e0[1]) * f
                    r_ = prng.uniform(0.18, 0.42)
                    a0 = prng.uniform(0, math.pi)
                    blk = [(cx + r_ * math.cos(a0 + q * math.pi / 2) * prng.uniform(0.7, 1.2), cy + r_ * math.sin(a0 + q * math.pi / 2) * prng.uniform(0.7, 1.2)) for q in range(4)]
                    _z_legacy = prng.uniform(0.15, 0.8)                # (legacy draws kept: the talus etc. after the pack do not move)
                    # R-C9-234 (5): no square pillars -- each ridge piece a LOW irregular broken lump (5-8 sides, varied size),
                    # sparser, 5-28 cm proud of its plate (own stream 2352)
                    if rngR.random() < 0.4:
                        continue
                    rr2 = r_ * rngR.uniform(0.55, 1.5)
                    nv = rngR.randint(5, 8)
                    a1 = rngR.uniform(0, 2 * math.pi)
                    blk = [(cx + rr2 * math.cos(a1 + 2 * math.pi * q / nv + rngR.uniform(-0.3, 0.3)) * rngR.uniform(0.6, 1.15),
                            cy + rr2 * math.sin(a1 + 2 * math.pi * q / nv + rngR.uniform(-0.3, 0.3)) * rngR.uniform(0.45, 1.0)) for q in range(nv)]
                    ridges.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(blk)], "z0": round(SEA_Z - 0.2, 3), "z1": round(top + rngR.uniform(0.05, 0.28), 3)})
        if rubble and len(ice) > n_ice0:
            # a RUBBLE ZONE in place of this plate: broken blocks of every size heaped where it was (its rims/ridges go too)
            base_ = [(round(q[0], 3), round(q[1], 3)) for q in poly]     # (the legacy outline: rngs draws unchanged)
            del ice[n_ice0:], rims[n_rim0:], ridges[n_rid0:]
            bx0, by0 = min(q[0] for q in base_), min(q[1] for q in base_)
            bx1, by1 = max(q[0] for q in base_), max(q[1] for q in base_)
            for _ in range(int(K.area(base_) * 1.1) + 2):
                cx, cy = rngs.uniform(bx0, bx1), rngs.uniform(by0, by1)
                if not K.point_in_poly((cx, cy), base_):
                    continue
                r_ = rngs.uniform(0.12, 0.6) ** 1.3 * 1.6
                pg = [(cx + r_ * math.cos(a_) * rngs.uniform(0.55, 1.2), cy + r_ * math.sin(a_) * rngs.uniform(0.55, 1.2)) for a_ in np.linspace(0, 2 * math.pi, rngs.randint(4, 7), endpoint=False)]
                ice.append({"zone": zn, "poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(pg)], "top": round(ICE_TOP + rngs.uniform(-0.1, 0.35), 3), "bob": False})
    # BRASH: small broken ice in the leads beside the plates
    ice_r = np.zeros(U.shape, bool)
    for e in ice:
        ice_r |= mask([tuple(q) for q in e.get("poly_leg", e["poly"])], U, V, HF_PPM, u0, v1)     # (legacy outline: the brash draws keep their count)
    near = ndimage.binary_dilation(ice_r, iterations=4) & ~ice_r & ~solid
    brash = []
    js, is_ = np.nonzero(near)
    for j, i in zip(js[::3], is_[::3]):
        if prng.random() < 0.35:
            cx, cy = us[i] + prng.uniform(-0.12, 0.12), vs[j] + prng.uniform(-0.12, 0.12)
            if not (box[0] < cx < box[2] and box[1] < cy < box[3]):
                continue
            r_ = prng.uniform(0.1, 0.32)
            pg = [(cx + r_ * prng.uniform(0.6, 1.1) * math.cos(2 * math.pi * q / 5 + 0.3), cy + r_ * prng.uniform(0.6, 1.1) * math.sin(2 * math.pi * q / 5 + 0.3)) for q in range(5)]
            brash.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in pg], "z0": round(SEA_Z - 0.15, 3), "z1": round(SEA_Z + prng.uniform(0.04, 0.16), 3)})
    # the ice fraction, inside the paint window, by raster (the sea = not land, not beach, not the shelf)
    win_m = (U > -33.6) & (U < 32.6) & (V > -28.6) & (V < 22.4)
    sea_area = float((~solid & win_m).sum()) / HF_PPM ** 2
    # under the shore-fast ice the terrain IS the ice (walkable, never drawn): its cracks show the sea plane
    fast_m = np.zeros(U.shape, bool)
    for cell in fast_raw:
        fast_m |= mask(cell, U, V, HF_PPM, u0, v1)
    fast_m &= ~solid & ~shelf_m & (Z < ICE_TOP)
    Z = np.where(fast_m, ICE_TOP - 0.03, Z)
    ice_area = float((ice_r & win_m).sum()) / HF_PPM ** 2
    # ---- the mere's PLATES (large cracked ice over dark water) and the stream's ice ----
    mc_ = K.centroid(mere)
    mbox = (min(q[0] for q in mere) - 2, min(q[1] for q in mere) - 2, max(q[0] for q in mere) + 2, max(q[1] for q in mere) + 2)
    mseeds = K.jitter_seeds(mbox, MERE_SHAPE["plate_m"], rngw, lambda p: K.point_in_poly(p, mere))
    mere_ice, mere_cracks, mere_seams, mere_seen = [], [], [], set()
    for cell in K.voronoi_cells(mseeds, mbox):
        if len(cell) < 3:
            continue
        c = K.centroid(cell)
        fixed = []
        for q in cell:
            if K.point_in_poly(q, mere):
                fixed.append(q)
                continue
            lo, hi = 0.0, 1.0
            for _ in range(18):
                m_ = (lo + hi) / 2
                if K.point_in_poly((c[0] + (q[0] - c[0]) * m_, c[1] + (q[1] - c[1]) * m_), mere):
                    lo = m_
                else:
                    hi = m_
            fixed.append((c[0] + (q[0] - c[0]) * lo, c[1] + (q[1] - c[1]) * lo))
        if False:
            mere_ice.append({"zone": "mere", "poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(fixed)], "top": MERE_SHAPE["plate_top"], "bob": False})
        # R-C9-208 (4): the cell edges are THIN CRACKS on one continuous sheet (not gaps between plates)
        for q0, q1, in0, in1 in zip(fixed, fixed[1:] + fixed[:1], [K.point_in_poly(q, mere) for q in cell], [K.point_in_poly(q, mere) for q in cell[1:] + cell[:1]]):
            key = tuple(sorted([(round(q0[0], 2), round(q0[1], 2)), (round(q1[0], 2), round(q1[1], 2))]))
            if key in mere_seen or not (in0 or in1) or math.dist(q0, q1) < 0.2:
                continue
            mere_seen.add(key)
            if rngw.random() < 0.18:
                continue
            mid_ = ((q0[0] + q1[0]) / 2 + rngw.uniform(-0.25, 0.25), (q0[1] + q1[1]) / 2 + rngw.uniform(-0.25, 0.25))
            for e0, e1 in ((q0, mid_), (mid_, q1)):
                L_ = math.dist(e0, e1)
                if L_ < 0.05:
                    continue
                nn = (-(e1[1] - e0[1]) / L_, (e1[0] - e0[0]) / L_)
                seam = rngw.random() < 0.12
                w_ = rngw.uniform(0.1, 0.18) if seam else rngw.uniform(0.03, 0.07)
                poly = [(e0[0] - nn[0] * w_ / 2, e0[1] - nn[1] * w_ / 2), (e1[0] - nn[0] * w_ / 2, e1[1] - nn[1] * w_ / 2), (e1[0] + nn[0] * w_ / 2, e1[1] + nn[1] * w_ / 2), (e0[0] + nn[0] * w_ / 2, e0[1] + nn[1] * w_ / 2)]
                mi_, mj_ = int(round(((e0[0] + e1[0]) / 2 - u0) * HF_PPM)), int(round((v1 - (e0[1] + e1[1]) / 2) * HF_PPM))
                if not mere_m[min(max(mj_, 0), H - 1), min(max(mi_, 0), W - 1)]:
                    continue                                       # the mere on the land; past the shore the transition field takes over
                (mere_seams if seam else mere_cracks).append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in poly],
                    "z0": MERE_SHAPE["plate_top"] - 0.02, "z1": MERE_SHAPE["plate_top"] + (rngw.uniform(0.02, 0.05) if seam else 0.008)})
    # R-C9-227 (2): sketch A's mere is MOSTLY CONTINUOUS ICE with only a FEW veins -- the regular Voronoi net above is dropped
    # (its rngw draws still run, so every later water draw is unchanged). A handful of long, irregular, BRANCHING cracks of
    # varied length (meandering random walks, some running out to the shore, some ending in the open ice) and a couple of
    # pressure seams; large uncracked areas between them. Own stream (2271).
    rngk = __import__("random").Random(2271)
    mere_cracks, mere_seams = [], []
    in_m = lambda q: bool(mere_m[min(max(int(round((v1 - q[1]) * HF_PPM)), 0), H - 1), min(max(int(round((q[0] - u0) * HF_PPM)), 0), W - 1)])
    mb = (min(q[0] for q in mere), min(q[1] for q in mere), max(q[0] for q in mere), max(q[1] for q in mere))

    def vein(p, hd, length, w0, seam, depth):
        pts = [p]
        L_ = 0.0
        while L_ < length:
            hd += rngk.gauss(0.0, 0.28)
            q = (pts[-1][0] + 0.45 * math.cos(hd), pts[-1][1] + 0.45 * math.sin(hd))
            if not in_m(q):
                break
            pts.append(q)
            L_ += 0.45
            if depth < 2 and rngk.random() < 0.05:
                vein(q, hd + rngk.choice((-1, 1)) * rngk.uniform(0.5, 1.2), length * rngk.uniform(0.2, 0.5), w0 * 0.7, False, depth + 1)
        for i_ in range(len(pts) - 1):
            e0, e1 = pts[i_], pts[i_ + 1]
            f_ = 1.0 - 0.6 * i_ / max(1, len(pts) - 1)              # tapering toward its end
            w_ = w0 * f_
            nn = (-(e1[1] - e0[1]) / 0.45, (e1[0] - e0[0]) / 0.45)
            poly = [(e0[0] - nn[0] * w_ / 2, e0[1] - nn[1] * w_ / 2), (e1[0] - nn[0] * w_ / 2, e1[1] - nn[1] * w_ / 2), (e1[0] + nn[0] * w_ / 2, e1[1] + nn[1] * w_ / 2),
                    (e0[0] + nn[0] * w_ / 2, e0[1] + nn[1] * w_ / 2)]
            (mere_seams if seam else mere_cracks).append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(poly)],
                "z0": MERE_SHAPE["plate_top"] - 0.02, "z1": MERE_SHAPE["plate_top"] + (0.04 if seam else 0.008)})
    n_v = 0
    for _try in range(200):
        if n_v >= 7:
            break
        p = (rngk.uniform(mb[0], mb[2]), rngk.uniform(mb[1], mb[3]))
        if not in_m(p):
            continue
        seam = n_v < 2
        vein(p, rngk.uniform(0, 2 * math.pi), rngk.uniform(5.0, 16.0) if not seam else rngk.uniform(3.0, 7.0), rngk.uniform(0.12, 0.18) if seam else rngk.uniform(0.04, 0.08), seam, 0)
        n_v += 1
    # the sheet itself: the cells laid edge to edge (no gaps; convex pieces triangulate cleanly) -- one continuous ice surface
    # every channel's ice: continuous (the channel floor), thin transverse CRACKS and a few small open-water SEAMS; a little
    # rough pressure ice where it flows into the mere
    stream_ice, stream_cracks, stream_press = [], [], []
    for ch, f_, cf_, cl_, mouth in ch_fields:
        Lc = 0.6
        end_ = min(mouth + 1.0, cl_[-1] - 0.2)
        while Lc < end_:
            k = int(np.searchsorted(cl_, Lc))
            if k >= len(cf_) - 1:
                break
            sa_, sb_ = cf_[k], cf_[k + 1]
            dd = unit(sb_[0] - sa_[0], sb_[1] - sa_[1])
            nn = (-dd[1], dd[0])
            c_ = sa_
            _, hw_i, _, _ = f_(np.array([[c_[0]]]), np.array([[c_[1]]]))
            hw_i = float(hw_i[0, 0])
            seam = rngw.random() < 0.15
            w_ = rngw.uniform(0.08, 0.14) if seam else rngw.uniform(0.025, 0.05)
            sk = rngw.uniform(-0.35, 0.35) * hw_i
            p0 = (c_[0] - nn[0] * hw_i * 0.95 - dd[0] * sk, c_[1] - nn[1] * hw_i * 0.95 - dd[1] * sk)
            p1 = (c_[0] + nn[0] * hw_i * 0.95 + dd[0] * sk, c_[1] + nn[1] * hw_i * 0.95 + dd[1] * sk)
            L_ = math.dist(p0, p1)
            tv = ((p1[0] - p0[0]) / L_, (p1[1] - p0[1]) / L_)
            pn = (-tv[1], tv[0])
            poly = [(p0[0] - pn[0] * w_ / 2, p0[1] - pn[1] * w_ / 2), (p1[0] - pn[0] * w_ / 2, p1[1] - pn[1] * w_ / 2), (p1[0] + pn[0] * w_ / 2, p1[1] + pn[1] * w_ / 2),
                    (p0[0] + pn[0] * w_ / 2, p0[1] + pn[1] * w_ / 2)]
            zc = float(Z[min(max(int(round((v1 - c_[1]) * HF_PPM)), 0), H - 1), min(max(int(round((c_[0] - u0) * HF_PPM)), 0), W - 1)])
            stream_cracks.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(poly)], "z0": round(zc - 0.03, 3), "z1": round(zc + 0.006, 3)})
            Lc += rngw.uniform(0.9, 1.8) * (1.0 if ch["hw"] < 1.0 else 1.4)
        if ch["widen"] > 0 and ch.get("press", True):
            for k in range(6):
                q = cf_[min(len(cf_) - 1, int(np.searchsorted(cl_, mouth - rngw.uniform(0.0, 2.0))))]
                q = (q[0] + rngw.uniform(-1.2, 1.2), q[1] + rngw.uniform(-1.0, 1.0))
                r_ = rngw.uniform(0.12, 0.3)
                pg = [(q[0] + r_ * math.cos(ang_) * rngw.uniform(0.7, 1.2), q[1] + r_ * math.sin(ang_) * rngw.uniform(0.7, 1.2)) for ang_ in np.linspace(0, 2 * math.pi, 6, endpoint=False)]
                zc = float(Z[min(max(int(round((v1 - q[1]) * HF_PPM)), 0), H - 1), min(max(int(round((q[0] - u0) * HF_PPM)), 0), W - 1)])
                stream_press.append({"poly": [[round(p_[0], 3), round(p_[1], 3)] for p_ in K.ccw(pg)], "z0": round(zc - 0.05, 3), "z1": round(zc + rngw.uniform(0.06, 0.16), 3)})
    # R-C9-227 (1): the river is OPEN DARK WATER (sketch A's un-frozen trickle) -- no ice, no cracks: its crack draws above still
    # run (rngw order kept) but are dropped; the water is a ribbon of thin prisms (class sea) on the channel floor, ending where
    # it meets the mere's ice edge (the open water simply meets the ice); a few reed tufts on its snowy banks (own stream 2273)
    river_water, river_reeds = [], []
    rngr2 = __import__("random").Random(2273)
    for ch, f_, cf_, cl_, mouth in ch_fields:
        if not ch.get("open"):
            continue
        stream_cracks = []
        # R-C9-234: the open water a SMOOTH ribbon -- one short prism per 0.1 m sample (the 0.3 m prisms stepped down the slope
        # and read as a dark zig-zag notch at the pilot's top-left)
        for k in range(0, len(cf_) - 1, 1):
            ra_, rb_ = cf_[k], cf_[min(k + 1, len(cf_) - 1)]
            if K.point_in_poly(ra_, mere):
                break
            _, hw_a, dp_a, _ = f_(np.array([[ra_[0]]]), np.array([[ra_[1]]]))
            _, hw_b, _, _ = f_(np.array([[rb_[0]]]), np.array([[rb_[1]]]))
            hw_a, hw_b = float(hw_a[0, 0]) * 0.92, float(hw_b[0, 0]) * 0.92
            dd = unit(rb_[0] - ra_[0], rb_[1] - ra_[1])
            nn = (-dd[1], dd[0])
            ext = 0.06
            q = [(ra_[0] - nn[0] * hw_a - dd[0] * ext, ra_[1] - nn[1] * hw_a - dd[1] * ext), (rb_[0] - nn[0] * hw_b + dd[0] * ext, rb_[1] - nn[1] * hw_b + dd[1] * ext),
                 (rb_[0] + nn[0] * hw_b + dd[0] * ext, rb_[1] + nn[1] * hw_b + dd[1] * ext), (ra_[0] + nn[0] * hw_a - dd[0] * ext, ra_[1] + nn[1] * hw_a - dd[1] * ext)]
            zc = float(ndimage.map_coordinates(Z.astype(np.float64), [[(v1 - (ra_[1] + rb_[1]) / 2) * HF_PPM], [((ra_[0] + rb_[0]) / 2 - u0) * HF_PPM]], order=1, mode="nearest")[0])
            river_water.append({"poly": [[round(p_[0], 3), round(p_[1], 3)] for p_ in K.ccw(q)], "z0": round(zc - 0.05, 3), "z1": round(zc + 0.03, 3)})
            if False:                                      # R-C9-234: the bank reeds are reed beds now (clumps, below)
                sd_ = rngr2.choice((-1, 1)) * (hw_a + rngr2.uniform(0.25, 0.7))
                tc_ = (ra_[0] + nn[0] * sd_, ra_[1] + nn[1] * sd_)
                zt_ = float(Z[min(max(int(round((v1 - tc_[1]) * HF_PPM)), 0), H - 1), min(max(int(round((tc_[0] - u0) * HF_PPM)), 0), W - 1)])
                for _ in range(rngr2.randint(1, 3)):
                    c2 = (tc_[0] + rngr2.uniform(-0.3, 0.3), tc_[1] + rngr2.uniform(-0.3, 0.3))
                    r2 = rngr2.uniform(0.12, 0.25)
                    pg = [(c2[0] + r2 * math.cos(b2) * rngr2.uniform(0.6, 1.2), c2[1] + r2 * math.sin(b2) * rngr2.uniform(0.6, 1.2)) for b2 in np.linspace(0, 2 * math.pi, 6, endpoint=False)]
                    river_reeds.append({"poly": [[round(p_[0], 3), round(p_[1], 3)] for p_ in K.ccw(pg)], "z0": round(zt_ - 0.05, 3), "z1": round(zt_ + rngr2.uniform(0.25, 0.45), 3)})
    # R-C9-220 (1): REED ISLANDS standing out of the mere's ice (low snowy tussocks; PT plants the reeds)
    reed_islands = []
    for k in range(6):
        for _try in range(30):
            q = (mc_r[0] + rngw.uniform(-0.75, 0.75) * MERE_SHAPE["radii"][0], mc_r[1] + rngw.uniform(-0.7, 0.7) * MERE_SHAPE["radii"][1])
            if K.point_in_poly(q, mere) and all(math.dist(q, (e["c"][0], e["c"][1])) > 4.0 for e in reed_islands):
                break
        r_ = rngw.uniform(0.6, 1.5)
        pg = [(q[0] + r_ * math.cos(ang_) * rngw.uniform(0.7, 1.15), q[1] + r_ * 0.7 * math.sin(ang_) * rngw.uniform(0.7, 1.15)) for ang_ in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
        reed_islands.append({"c": q, "poly": [[round(p_[0], 3), round(p_[1], 3)] for p_ in K.ccw(pg)], "z0": round(MERE_SHAPE["plate_top"] - 0.05, 3), "z1": round(MERE_SHAPE["plate_top"] + rngw.uniform(0.12, 0.25), 3)})
    # R-C9-221 (Matt): THE MERE TURNS INTO THE SEA, seamlessly -- one graded ice field from the mere's shore across the beach
    # to the pack: plates tight with thin cracks at the mere, growing more broken westward, gaps and dark leads widening,
    # reed islands and snow-covered low rocks scattered through it; the classes blend ice -> ice_mid -> shore_ice
    # R-C9-226 (5): the field's south limit wanders (no straight edge across the beach)
    # R-C9-234 (4): the field is now the whole mere -> sea margin (wG above), on the land strip AND the beach
    trans_m = (wG > 0.5) & ~mere_m
    trans_plates, trans_rocks = [], []
    if trans_m.any():
        jj, ii = np.nonzero(trans_m)
        tb_ = (us[ii].min() - 2, vs[jj].min() - 2, us[ii].max() + 2, vs[jj].max() + 2)

        def in_trans(p):
            i_, j_ = int(round((p[0] - u0) * HF_PPM)), int(round((v1 - p[1]) * HF_PPM))
            return 0 <= i_ < W and 0 <= j_ < H and bool(trans_m[j_, i_])
        tseeds = K.jitter_seeds(tb_, 1.5, rngw, in_trans)
        # the transition's ice IS the ground (classed ice -> ice_mid -> shore_ice down the slope); its plate boundaries are
        # drawn as CRACKS that widen westward into dark LEADS -- no blocks on the slope
        # R-C9-229 (4): no regular net -- long irregular cracks wandering WEST from the mere's ice, branching, widening into
        # dark leads as the ice breaks up toward the sea, plus broken plates and rubble near its sea edge (own stream 2291)
        rngt2 = __import__("random").Random(2291)
        jq_ = lambda q: (min(max(int(round((v1 - q[1]) * HF_PPM)), 0), H - 1), min(max(int(round((q[0] - u0) * HF_PPM)), 0), W - 1))

        def tvein(p, hd, length, depth):
            L_ = 0.0
            while L_ < length:
                hd += rngt2.gauss(0.0, 0.3)
                q = (p[0] + 0.35 * math.cos(hd), p[1] + 0.35 * math.sin(hd))
                if not in_trans(q):
                    return
                jq, iq = jq_(q)
                w_ = float(b_f[jq, iq])                     # R-C9-234 (4): widening with the field's own grade (mere 0 -> sea 1)
                wd = (0.03 + 0.55 * w_ ** 1.7) * rngt2.uniform(0.6, 1.5)
                wd = min(wd, 0.04 + 0.32 * w_ ** 1.5)          # R-C9-234: leads widen toward the sea but never into dark blocks
                nn = (-math.sin(hd) * wd / 2, math.cos(hd) * wd / 2)
                poly = [(p[0] - nn[0], p[1] - nn[1]), (q[0] - nn[0], q[1] - nn[1]), (q[0] + nn[0], q[1] + nn[1]), (p[0] + nn[0], p[1] + nn[1])]
                jp, ip = jq_(p)
                zq, zp = float(Z[jq, iq]), float(Z[jp, ip])
                # R-C9-234: on the slope the lead's prism spans BOTH ends' heights (no dashed, half-buried segments)
                trans_plates.append({"cls": "lead", "poly": [[round(x[0], 3), round(x[1], 3)] for x in K.ccw(poly)], "z0": round(min(zq, zp) - 0.15, 3), "z1": round(max(zq, zp) + 0.03, 3)})
                p = q
                L_ += 0.35
                if depth < 2 and rngt2.random() < 0.06 + 0.08 * w_:
                    tvein(p, hd + rngt2.choice((-1, 1)) * rngt2.uniform(0.6, 1.4), length * rngt2.uniform(0.3, 0.7), depth + 1)
        ii_t, jj_t = ii, jj
        for _v in range(16):
            k_ = rngt2.randrange(len(ii_t))
            p0 = (us[ii_t[k_]], vs[jj_t[k_]])
            tvein(p0, math.pi + rngt2.gauss(0.0, 0.7), rngt2.uniform(3.0, 12.0), 0)
        for _r in range(70):                                # broken plates and rubble where the field meets the sea
            k_ = rngt2.randrange(len(ii_t))
            q = (us[ii_t[k_]] + rngt2.uniform(-0.2, 0.2), vs[jj_t[k_]] + rngt2.uniform(-0.2, 0.2))
            jq, iq = jq_(q)
            w_ = float(b_f[jq, iq])
            if w_ < 0.6 or rngt2.random() > w_:
                continue
            r_ = rngt2.uniform(0.12, 0.7) ** 1.4 * 1.5
            pg = [(q[0] + r_ * math.cos(b_) * rngt2.uniform(0.55, 1.2), q[1] + r_ * math.sin(b_) * rngt2.uniform(0.55, 1.2)) for b_ in np.linspace(0, 2 * math.pi, rngt2.randint(4, 7), endpoint=False)]
            zq = float(Z[jq, iq])
            trans_plates.append({"cls": "rubble", "poly": [[round(x[0], 3), round(x[1], 3)] for x in K.ccw(pg)], "z0": round(zq - 0.1, 3), "z1": round(zq + rngt2.uniform(0.08, 0.3), 3)})
        for k in range(10):                                # reed islands and snow-covered low rocks through the transition
            q = (us[ii[rngw.randrange(len(ii))]] + rngw.uniform(-0.3, 0.3), vs[jj[rngw.randrange(len(jj))]])
            q = (us[ii[(k * 37) % len(ii)]], vs[jj[(k * 37) % len(jj)]])
            r_ = rngw.uniform(0.4, 1.0)
            pg = [(q[0] + r_ * math.cos(ang_) * rngw.uniform(0.7, 1.15), q[1] + r_ * 0.75 * math.sin(ang_) * rngw.uniform(0.7, 1.15)) for ang_ in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
            zq = float(Z[min(max(int(round((v1 - q[1]) * HF_PPM)), 0), H - 1), min(max(int(round((q[0] - u0) * HF_PPM)), 0), W - 1)])
            (reed_islands if k % 2 == 0 else trans_rocks).append({"c": q, "poly": [[round(p_[0], 3), round(p_[1], 3)] for p_ in K.ccw(pg)], "z0": round(zq - 0.2, 3),
                                                                  "z1": round(zq + (rngw.uniform(0.15, 0.3) if k % 2 == 0 else rngw.uniform(0.3, 0.6)), 3)})
    # ================= R-C9-234 (2)/(4): ORGANIC LOW ISLANDS + REED BEDS (own stream 2344) =================
    # The legacy island draws above still run (their centres are kept) but no octagon pad is built: each island is the
    # GROUND itself raised in a low irregular dome (lobed outline, elongated, rotated), snow on it, reed beds on it; the
    # margin's islands are "land under the ice" showing through it. Reed clumps also stand along the mere's edges and the
    # river's banks. Every clump: a straw ground patch + thin tall blades (class `reed`), exported for PT (art/reed_beds.json)
    rngi = __import__("random").Random(2344)
    islands, clumps = [], []
    n_mere_isl = 6
    for k_, e in enumerate(reed_islands + trans_rocks):
        in_mere = k_ < n_mere_isl
        kind = "reed" if k_ < len(reed_islands) else "rock"
        islands.append({"c": tuple(e["c"]), "R": rngi.uniform(1.2, 2.4) if in_mere else rngi.uniform(0.8, 1.7), "el": rngi.uniform(0.5, 0.9),
                        "rot": rngi.uniform(0, math.pi), "ph": [rngi.uniform(0, 6.3) for _ in range(4)],
                        "h": rngi.uniform(0.12, 0.26) if kind == "reed" else rngi.uniform(0.18, 0.35), "kind": kind, "where": "mere" if in_mere else "margin"})

    def isl_rho(e, Uq, Vq):
        dx, dy = Uq - e["c"][0], Vq - e["c"][1]
        cr, sr = math.cos(e["rot"]), math.sin(e["rot"])
        x_ = dx * cr + dy * sr
        y_ = (-dx * sr + dy * cr) / e["el"]
        th = np.arctan2(y_, x_)
        p_ = e["ph"]
        rr = e["R"] * (1 + 0.22 * np.sin(2 * th + p_[0]) + 0.14 * np.sin(3 * th + p_[1]) + 0.08 * np.sin(5 * th + p_[2]) + 0.04 * np.sin(9 * th + p_[3]))
        return np.hypot(x_, y_) / rr
    for e in islands:
        rr = isl_rho(e, U, V)
        Z = np.where(rr < 1.0, Z + e["h"] * np.clip(1.0 - rr * rr, 0.0, 1.0) ** 0.6, Z)
        for _c in range(rngi.randint(2, 4) if e["kind"] == "reed" else rngi.randint(0, 1)):
            ang_c = rngi.uniform(0, 2 * math.pi)
            fr_c = rngi.uniform(0.1, 0.65)
            clumps.append({"c": (e["c"][0] + fr_c * e["R"] * math.cos(ang_c), e["c"][1] + fr_c * e["R"] * e["el"] * math.sin(ang_c)), "r": rngi.uniform(0.35, 0.75), "on": "island_" + e["where"]})
    # along the mere's edges (its W, N and S margins -- sketch A's reed fringe), clumps on the ice edge and the bank
    mo_ = K.resample(mere + [mere[0]], 0.5)
    mcc = K.centroid(mere)
    Lm, next_ = 0.0, rngi.uniform(1.0, 4.0)
    for qa, qb in zip(mo_[:-1], mo_[1:]):
        Lm += math.dist(qa, qb)
        if Lm < next_:
            continue
        next_ = Lm + rngi.uniform(3.0, 6.5)
        if qa[0] > -5.0:                                    # not round the barrow's flank / the open snow by the ring
            continue
        out_ = unit(qa[0] - mcc[0], qa[1] - mcc[1])
        o_ = rngi.uniform(-1.0, 1.2)
        clumps.append({"c": (qa[0] + out_[0] * o_, qa[1] + out_[1] * o_), "r": rngi.uniform(0.4, 0.9), "on": "mere_edge"})
    # the river's banks
    for ch, f_, cf_, cl_, mouth in ch_fields:
        if not ch.get("open"):
            continue
        Lr = rngi.uniform(0.5, 2.0)
        side = 1
        while Lr < mouth:
            k = min(int(np.searchsorted(cl_, Lr)), len(cf_) - 2)
            dd = unit(cf_[k + 1][0] - cf_[k][0], cf_[k + 1][1] - cf_[k][1])
            side = -side if rngi.random() < 0.7 else side
            o_ = side * (ch["hw"] + rngi.uniform(0.45, 0.9))
            clumps.append({"c": (cf_[k][0] - dd[1] * o_, cf_[k][1] + dd[0] * o_), "r": rngi.uniform(0.3, 0.6), "on": "river_bank"})
            Lr += rngi.uniform(2.0, 3.8)
    Z = Z.astype("<f4")
    Z.tofile(os.path.join(OUT, "terrain_h.f32"))
    # ---- classes at CLS_PPM ----
    names = ["none", "snow", "path", "ice", "shrub", "rock", "mound", "shingle", "shore_ice", "stream", "char", "sea", "wood", "passage_dark", "ash",
             "tide_ice", "wet_rock", "rime", "ice_mid", "reed"]    # R-C9-213: tidal classes; R-C9-221: the mere->sea blend band; R-C9-234: reed beds
    Wc = int((u1 - u0) * CLS_PPM)
    Hc_ = int((v1 - v0) * CLS_PPM)
    Uc, Vc = np.meshgrid(u0 + (np.arange(Wc) + 0.5) / CLS_PPM, v1 - (np.arange(Hc_) + 0.5) / CLS_PPM)
    fi = np.clip(((Uc - u0) * HF_PPM).astype(int), 0, W - 1)
    fj = np.clip(((v1 - Vc) * HF_PPM).astype(int), 0, H - 1)
    Zc = Z[fj, fi]
    landc = mask(land_poly, Uc, Vc, CLS_PPM, u0, v1)
    # R-C9-234 (3): the beach, its foot and its ice bays classed from the SMOOTH fields (bilinear at the class grid), not
    # from the 25 cm heightfield cells -- no stair-stepped edges
    def samp(A_):
        return ndimage.map_coordinates(np.asarray(A_, np.float64), [(v1 - Vc) * HF_PPM, (Uc - u0) * HF_PPM], order=1, mode="nearest")
    ds_c, bw_c, bw0_c = samp(d_shore), samp(BW), samp(BW0)
    west_c = ~landc & (ds_c < samp(d_lip))                                # (the same rule as `west`, on the smooth fields: no slivers)
    beach_c = west_c & ~landc & (ds_c <= bw_c)
    bay_c = west_c & ~landc & (ds_c > bw_c) & (ds_c <= bw0_c)
    beachc = beach_c | bay_c
    C = np.full(Uc.shape, names.index("snow"), np.uint8)
    rhoc = np.hypot((Uc - mc[0]) / a_, (Vc - mc[1]) / b_)
    C[landc & (rhoc < 1.0)] = names.index("mound")
    C[landc & (ndimage.map_coordinates(lobe_eff, [(v1 - Vc) * HF_PPM, (Uc - u0) * HF_PPM], order=1, mode="nearest") > 0.12)] = names.index("mound")             # R-C9-234 (6): the front lobe round the door

    def cnoise(seed, su, sv=None):
        n_ = ndimage.gaussian_filter(np.random.default_rng(seed).standard_normal(Uc.shape), ((sv or su) * CLS_PPM, su * CLS_PPM))
        return n_ / (n_.std() + 1e-9)
    for (p, r) in SHRUB:
        c = uv(p)
        rr = r / S
        tc_s, sc_s = to_fr(c)
        if t0s - rr - 1.5 < tc_s < t1s + rr + 1.5 and s_land - rr - 1.5 < sc_s < s_foot + rr + 1.5:
            continue                                   # R-C9-226: no heather patch over the stair's cleft or its top pad
        n_ = 0.35 * np.sin(Uc * 1.7 + p[0]) * np.sin(Vc * 1.3 + p[1])
        C[landc & (np.hypot(Uc - c[0], Vc - c[1]) < rr * (1 + n_))] = names.index("shrub")
    # R-C9-234 (3): the SHINGLE is no slab -- snow DRIFTED over it (long E-W drifts + small patches, deeper toward the top), its
    # foot ragged into the shore ice (and the foot's ice bays); the stones show between the drifts
    shin = beach_c
    C[shin] = names.index("shingle")
    btc = np.clip(ds_c / bw_c, 0, 1)
    drift = 0.85 * cnoise(2346, 1.3, 0.6) + 0.5 * cnoise(2347, 0.45) + 1.2 * (0.3 - btc)
    C[shin & (drift > -0.25)] = names.index("snow")
    C[bay_c | (shin & (btc > 0.84 + 0.07 * cnoise(2348, 0.8)))] = names.index("shore_ice")
    # R-C9-234 (4): the mere -> sea margin, classes graded along b (ice -> ice_mid -> shore_ice) with soft noisy limits
    wGc = samp(wG) + 0.22 * cnoise(2349, 0.9)
    bfc = samp(b_f) + 0.09 * cnoise(2350, 1.1)
    cor = (wGc > 0.5) & (landc | beachc)
    C[cor & (bfc < 0.36)] = names.index("ice")
    C[cor & (bfc >= 0.36) & (bfc < 0.68)] = names.index("ice_mid")
    C[cor & (bfc >= 0.68)] = names.index("shore_ice")
    C[(samp(cw_r) > 0.97) & ~landc] = names.index("shore_ice")           # the wreck's cradle: shore ice, not beach (R-C9-234: smooth edge)
    # R-C9-226 (5): the ash yard IRREGULAR -- the outline resampled, pushed in/out by low lobes, a ragged fringe of trampled
    # ash tongues; holes of snow where drifts lie inside it
    rngy = __import__("random").Random(YARD_SEED)
    ypts = K.resample([uv(p) for p in YARD] + [uv(YARD[0])], 0.4)[:-1]
    yc = K.centroid(ypts)
    yph = [rngy.uniform(0, 6.3) for _ in range(4)]
    yard = []
    for q in ypts:
        a = math.atan2(q[1] - yc[1], q[0] - yc[0])
        f = 1.0 + 0.10 * math.sin(2 * a + yph[0]) + 0.07 * math.sin(4 * a + yph[1]) + 0.05 * math.sin(7 * a + yph[2]) + 0.035 * math.sin(13 * a + yph[3])
        yard.append((yc[0] + (q[0] - yc[0]) * f, yc[1] + (q[1] - yc[1]) * f))
    ym = mask(yard, Uc, Vc, CLS_PPM, u0, v1)
    yn = ndimage.gaussian_filter(np.asarray(np.random.default_rng(YARD_SEED).standard_normal(ym.shape)), 16.0)
    yn /= yn.std() + 1e-9
    yd = ndimage.distance_transform_edt(ym) / CLS_PPM - ndimage.distance_transform_edt(~ym) / CLS_PPM
    yash = ndimage.binary_opening(yd + 0.8 * yn > 0.0, iterations=6)           # tongues of trampled ash, no specks
    yash = ndimage.binary_closing(yash, iterations=6)
    C[yash] = names.index("ash")
    C[mask(mere, Uc, Vc, CLS_PPM, u0, v1)] = names.index("ice")          # the mere's continuous ice (its thin cracks are drawn on it)
    for _, f_, _, _, _ in ch_fields:
        dstc, hwc, _, tmc = f_(Uc, Vc)
        C[landc & (dstc >= hwc) & (dstc < hwc + bw_st) & (tmc > 0.5)] = names.index("snow")   # low snowy banks along its length only (none across the mouth)
    for _, f_, _, _, _ in ch_fields:
        dstc, hwc, _, tmc = f_(Uc, Vc)
        # R-C9-227: open water, no ice. R-C9-234: drawn as the GROUND's own dark-water class along the channel floor (one
        # continuous ribbon down the slope) -- the per-segment prisms stepped and read as a dark zig-zag notch
        C[landc & (dstc < (hwc - (1.0 - tmc) * ch_fields[0][0]["widen"]) * 0.92) & ~mask(mere, Uc, Vc, CLS_PPM, u0, v1)] = names.index("sea")   # a tiny river: no flared mouth
    # R-C9-234 (2): the islands (snow on the raised ground) and the reed beds' straw ground under every clump
    for e in islands:
        C[isl_rho(e, Uc, Vc) < 0.93] = names.index("snow")
    for k_, cl in enumerate(clumps):
        c = cl["c"]
        r_ = cl["r"] * 1.2
        i0, i1 = max(0, int((c[0] - r_ * 1.5 - u0) * CLS_PPM)), min(Wc, int((c[0] + r_ * 1.5 - u0) * CLS_PPM) + 1)
        j0, j1 = max(0, int((v1 - c[1] - r_ * 1.5) * CLS_PPM)), min(Hc_, int((v1 - c[1] + r_ * 1.5) * CLS_PPM) + 1)
        if i1 <= i0 or j1 <= j0:
            continue
        uq, vq = Uc[j0:j1, i0:i1], Vc[j0:j1, i0:i1]
        th = np.arctan2(vq - c[1], uq - c[0])
        rq = r_ * (1 + 0.22 * np.sin(3 * th + k_) + 0.12 * np.sin(5 * th + 2 * k_))
        sub = C[j0:j1, i0:i1]
        sub[np.hypot(uq - c[0], vq - c[1]) < rq] = names.index("reed")
    southc = ~landc & ~beachc
    C[southc & (Zc > ICE_TOP + 0.05)] = names.index("rock")
    dlc = dist_to_chain(lip, Uc, Vc)
    C[southc & (dlc < 1.6)] = names.index("none")                         # the raw heightfield face is not drawn: the cliff skirt + the kit are the face
    Tc = (Uc - LIP_A[0]) * dR[0] + (Vc - LIP_A[1]) * dR[1]
    Sc = (Uc - LIP_A[0]) * nR[0] + (Vc - LIP_A[1]) * nR[1]
    gzy, gzx = np.gradient(Zc, 1.0 / CLS_PPM)
    steep = ndimage.binary_dilation(np.hypot(gzx, gzy) > 2.5, iterations=2)       # true faces (and the cells at their foot and lip)
    zone_r = (dlc < 2.5)
    # R-C9-208 (5): no raw heightfield face anywhere on the coast (its 25 cm cells read as vertical slats): the skirt and the kit are the face
    C[steep & zone_r] = names.index("none")
    C[(Zc <= ICE_TOP) & ~beachc] = names.index("none")                    # sea / under the ice: the sea plane and the ice draw it
    # ================= R-C9-226 (1): THE CAVE SECTION, CARVED FROM ONE ROCK-COLUMN MASS (bv2pp_cove) =================
    import bv2pp_cove as CV
    CR = CARVE
    from scipy.ndimage import map_coordinates as _mc

    def H_ts(tq, sq):
        uq = LIP_A[0] + dR[0] * tq + nR[0] * sq
        vq = LIP_A[1] + dR[1] * tq + nR[1] * sq
        return _mc(Z.astype(np.float64), [(v1 - vq) * HF_PPM, (uq - u0) * HF_PPM], order=1, mode="nearest")
    sb_ = CR["cove"]["s_back"]
    cove_t_w = CR["cove"]["t_w"]
    # R-C9-228: only the gully (stair) and the cave's corner are carved; the rest of the coast is the cliff kit as before
    core_rects = [(R["cave_t"] - 3.8, t0s, -4.5, 2.6),                                  # the cave's corner and its ledge
                  (t0s - 1.6, t1s + 1.6, s_land - 0.6, 2.6)]                          # the stair gully, its walls, its iced floor
    LD_ = CR["landing"]
    m_c = (R["cave_t"] - CR["cave_axis_ts"][0] * 1.4, sb_ - CR["cave_axis_ts"][1] * 1.4)   # the floor just out of the mouth

    def landing_fn(tq, sq):
        sfr = LD_["s_front"] + 0.55 * np.sin(tq * 0.9 + 0.4) + 0.3 * np.sin(tq * 2.3 + 1.7) + 0.15 * np.sin(tq * 5.1)   # R-C9-229 (3): lobed, ragged
        gully = (tq >= t0s - 0.2) & (tq <= t1s + 0.2) & (sq >= s_foot - 0.3) & (sq <= sfr)
        ang = np.arctan2(sq - m_c[1], tq - m_c[0])
        mouth = (np.hypot(tq - m_c[0], sq - m_c[1]) < LD_["mouth_r"] + 0.55 * np.sin(ang * 3 + 0.5) + 0.3 * np.sin(ang * 5 + 2.0)) & (sq <= sfr)
        return gully | mouth
    carve_P = {"step": CR["step"], "t0": CR["t"][0], "t1": CR["t"][1], "s0": CR["s"][0], "s1": CR["s"][1], "z0": SEA_FLOOR - 0.6, "z1": head_z_max + 1.6,
               "H": H_ts, "z_floor": SEA_FLOOR, "landing_z": R["shelf_z"], "high_water": CR["high_water"], "land_thr": CR["land_thr"],
               "col_spacing": CR["col_spacing"], "core_rects": core_rects, "core_fn": lambda tq, sq: head_w(tq, sq)[0] > 0.02,   # + the knoll
               "head_mask": lambda tq, sq: head_w(tq, sq)[0] > 0.05,
               "walk_zone": (t0s - 1.2, t1s + 1.2, s_land - 2.5, s_top + 0.3),
               "cove": dict(CR["cove"], s_b=sb_), "landing": CR["landing"], "landing_fn": landing_fn,
               "cave": {"t": R["cave_t"], "s_mouth": sb_, "w": CR["mouth_w_cut"], "h": CR["mouth_h_cut"], "depth": CR["cave_depth"], "axis": CR["cave_axis_ts"], "front": 4.0},
               "stair": {"t0": t0s, "t1": t1s, "tread": R["tread"], "n_tr": n_tr, "rise": rise, "s_foot": s_foot, "s_top": s_top, "s_land": s_land,
                         "top_z": top_z, "bed_below": CR["bed_below"], "s_open": CR["landing"]["s_front"] + 1.0}}
    carved = CV.build(carve_P)
    if os.environ.get("LV_CARVE_DEBUG"):
        np.savez(os.environ["LV_CARVE_DEBUG"], ts=carved["grid_ts"][0], ss=carved["grid_ts"][1], top2=carved["top2"], mask=carved["mask"], sd=carved["sd_plan"],
                 walk=carved["walk_h"], H=H_ts(*np.meshgrid(*carved["grid_ts"], indexing="ij")))
    # the carved mass replaces the terrain inside its MASK (an organic outline 2 m round the features -- never a box edge):
    # mask > 0.5 the terrain is not drawn, > 0.85 the heightfield drops under the rock; the carved mesh is kept from 0.3 (an
    # overlap band where both are the same ground)
    from scipy.interpolate import RegularGridInterpolator as _RGI
    _mi = _RGI(carved["grid_ts"], carved["mask"], bounds_error=False, fill_value=0.0)
    mask_hf = _mi(np.stack([Tq, Sq], axis=-1))
    mask_c = _mi(np.stack([Tc, Sc], axis=-1))
    carved_mask_at = lambda tq, sq: _mi([[tq, sq]])[0]
    C_pre = C.copy()
    C[mask_c > 0.5] = names.index("none")
    fp_hf = mask_hf > 0.85
    Z_out = np.where(fp_hf, SEA_FLOOR - 1.0, Z).astype("<f4")
    Z_out.tofile(os.path.join(OUT, "terrain_h.f32"))
    _wi = _RGI(carved["grid_ts"], carved["walk_h"], bounds_error=False, fill_value=None)
    Z_walk = np.where(fp_hf, _wi(np.stack([Tq, Sq], axis=-1)), Z).astype("<f4")
    Z_walk.tofile(os.path.join(OUT, "terrain_walk_h.f32"))
    # to the Level node's local frame (u, h, -v), classed meshes + smooth normals (welded), Godot's winding
    TT = carved["tris_ts"]
    UU = LIP_A[0] + dR[0] * TT[..., 0] + nR[0] * TT[..., 1]
    VV = LIP_A[1] + dR[1] * TT[..., 0] + nR[1] * TT[..., 1]
    loc = np.stack([UU, TT[..., 2], -VV], axis=-1)                 # (M, 3, 3) Level local
    fn = np.cross(loc[:, 1] - loc[:, 0], loc[:, 2] - loc[:, 0])
    Nts = carved["normals_ts"]
    nloc = np.stack([dR[0] * Nts[:, 0] + nR[0] * Nts[:, 1], Nts[:, 2], -(dR[1] * Nts[:, 0] + nR[1] * Nts[:, 1])], axis=1)
    flip = (fn * nloc).sum(1) > 0                                   # Godot: (b-a)x(c-a) points AWAY from the normal
    loc[flip] = loc[flip][:, [0, 2, 1]]
    key = np.round(loc.reshape(-1, 3) * 500).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    area_n = np.repeat(nloc, 3, axis=0)
    acc = np.zeros((inv.max() + 1, 3))
    np.add.at(acc, inv, area_n)
    vn = acc[inv]
    vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-9
    cen = loc.mean(1)
    ci = np.clip(((cen[:, 0] - u0) * CLS_PPM).astype(int), 0, Wc - 1)
    cj = np.clip(((v1 + cen[:, 2]) * CLS_PPM).astype(int), 0, Hc_ - 1)
    cls_names = [carved["classes"][k] for k in carved["cls"]]
    # the carved mass's UNCUT top keeps the ground's own class (snow, heather, shingle...) -- it IS that ground
    Ht = H_ts(carved["tris_ts"].mean(1)[:, 0], carved["tris_ts"].mean(1)[:, 1])
    upn = carved["normals_ts"][:, 2]
    zc_ = carved["tris_ts"].mean(1)[:, 2]
    top_uncut = (upn > 0.55) & (np.abs(zc_ - Ht) < 0.25) & (zc_ > R["shelf_z"] + 0.5)
    for k in np.nonzero(top_uncut)[0]:
        nm_ = names[int(C_pre[cj[k], ci[k]])]
        if nm_ not in ("none",):
            cls_names[k] = nm_
    C0 = C.copy()
    carved_files = {}
    groups = {}
    for k in range(len(loc)):
        groups.setdefault(cls_names[k], []).append(k)
    for cname, idx in groups.items():
        idx = np.array(idx)
        arr = np.concatenate([loc[idx].reshape(-1, 3), vn.reshape(-1, 3, 3)[idx].reshape(-1, 3)], axis=1).astype("<f4")
        fname = "carved_%s.f32" % cname
        arr.tofile(os.path.join(OUT, fname))
        carved_files[cname] = {"file": fname, "tris": int(len(idx)), "sha256": sha(os.path.join(OUT, fname))}
    # icicles hang from the high-water RIME line: off the carved rime triangles that face the open cove (seaward-ish)
    rime_k = [k for k in range(len(cls_names)) if cls_names[k] == "rime" and Nts[k, 2] < 0.3]
    Image.fromarray(C, "L").save(os.path.join(OUT, "classes.png"))
    shutil.copyfile(os.path.join(OUT, "classes.png"), os.path.join(OUT, "classes_png.bin"))

    # ---------------- placements ----------------
    models, layout_pl, openings = [], [], []
    glb_copies = {}

    def ext(glb):
        key = glb.replace("/", "__") + ".bin"
        src = os.path.join(BF, glb) if glb.startswith("data/bv2f/") else os.path.join(RUNS, glb[5:])
        if key not in glb_copies:
            shutil.copyfile(src, os.path.join(EXT, key))
            glb_copies[key] = {"from": glb, "sha256": sha(src)}
        return "data/bv2f/ext/" + key

    def yaw_of(face_uv):
        fs = (face_uv[0], -face_uv[1])
        return math.degrees(math.atan2(fs[0], fs[1]))

    def model(mid, cls, glb, c_uv, face_uv, s, z=0.0, piece=None, lie=False, note="", collider=None):
        bx, by, bz = ab(glb)
        dims = (by, bx, bz) if lie else (bx, by, bz)
        w, h, d = dims[0] * s, dims[1] * s, dims[2] * s
        ins = {"type": "box", "pos": [round(c_uv[0], 4), round(-c_uv[1], 4)], "z": round(z, 3), "godot_rot_y_deg": round(yaw_of(face_uv), 3),
               "size_m": [round(w, 4), round(d, 4), round(h, 4)], "glb": ext(glb), "uniform_scale": round(s, 5)}
        if lie:
            ins["lie_z90"] = True
        if collider:
            ins["collider"] = collider
        layout_pl.append({"id": mid, "piece": piece or mid, "class": cls, "kind": "model", "glb": glb, "uv": [round(c_uv[0], 4), round(c_uv[1], 4)],
                          "z": round(z, 3), "facing_uv": [round(face_uv[0], 4), round(face_uv[1], 4)], "scale": round(s, 5), "lying": lie,
                          "size_m": {"w": round(w, 3), "d": round(d, 3), "h": round(h, 3)}, "note": note})
        return ins

    def hz(c):
        i = int(round((c[0] - u0) * HF_PPM))
        j = int(round((v1 - c[1]) * HF_PPM))
        return float(Z[min(max(j, 0), H - 1), min(max(i, 0), W - 1)])

    def hz_min(c, r):
        return min(hz((c[0] + dx, c[1] + dy)) for dx in (-r, 0, r) for dy in (-r, 0, r))

    def group(gid, kind, insts):
        models.append({"id": gid, "kind": kind, "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": insts, "glb": None})
    # -- the wreck (W): re-seated at the beach foot on the shore ice, heeled, prow up (upper-left), its open hull to the camera
    pa, pb = WRECK["prow_uv"], WRECK["stern_uv"]
    ax_ = unit(pb[0] - pa[0], pb[1] - pa[1])
    face = (-ax_[1], ax_[0]) if -ax_[0] < 0 else (ax_[1], -ax_[0])
    if face[1] > 0:
        face = (-face[0], -face[1])
    wc = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
    sw = WRECK["len_m"] / ab(WRECK["glb"])[0]
    wins = model("wreck", "wood", WRECK["glb"], wc, face, sw, z=ICE_TOP - WRECK["sink"], note="R-C9-204: re-seated at the beach foot on the shore ice (ice top %.1f)" % ICE_TOP)
    models.append({"id": "wreck", "kind": "wreck", "pos": wins["pos"], "z": wins["z"], "godot_rot_y_deg": wins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": wins["size_m"][0], "d_local_z": wins["size_m"][1], "h": wins["size_m"][2]}, "glb": wins["glb"]})
    layout_pl[-1]["hidden_by_design"] = "see models[wreck].hidden_by_design"
    wl = WRECK["len_m"]
    wb = ab(WRECK["glb"])[2] * sw
    # HIDDEN BY DESIGN (P6' 761a48353): the part of the hull below the shore-ice top, measured on the build's own vertices
    import struct as _st
    _b = open(os.path.join(BF, WRECK["glb"]), "rb").read()
    _n = _st.unpack("<I", _b[12:16])[0]
    _J = json.loads(_b[20:20 + _n]); _o = 20 + _n
    _B = _b[_o + 8:_o + 8 + _st.unpack("<I", _b[_o:_o + 4])[0]]
    _ys = []
    for _nd in _J["nodes"]:
        if "mesh" not in _nd:
            continue
        for _pr in _J["meshes"][_nd["mesh"]]["primitives"]:
            _a = _J["accessors"][_pr["attributes"]["POSITION"]]; _bv = _J["bufferViews"][_a["bufferView"]]
            _P = np.frombuffer(_B, "<f4", _a["count"] * 3, _bv.get("byteOffset", 0) + _a.get("byteOffset", 0)).reshape(-1, 3)
            _ys.append(_P[:, 1] * np.array(_nd.get("scale", [1, 1, 1]))[1] + np.array(_nd.get("translation", [0, 0, 0]))[1])
    _ys = np.concatenate(_ys)
    _ys = (_ys - _ys.min()) * sw + wins["z"]
    wreck_hidden = {"below_shore_ice_vertex_pct": round(100.0 * float((_ys < ICE_TOP).mean()), 1), "ice_top_m": ICE_TOP, "hull_base_m": wins["z"],
                    "sink_m": WRECK["sink"], "_": "hidden by design: heeled and half-sunk in the shore ice (R-C9-162/204); the beach terrain no longer reaches the hull (a shore-ice cradle under it)"}
    models[-1]["hidden_by_design"] = wreck_hidden
    layout_pl[[q["id"] for q in layout_pl].index("wreck")]["hidden_by_design"] = wreck_hidden
    openings.append({"id": "wreck_hull", "point": "W", "model": "wreck", "centre_sim": wins["pos"], "z0": ICE_TOP, "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "h_rect", "centre": wins["pos"], "rot_deg": round(math.degrees(math.atan2(-ax_[1], ax_[0])), 3), "L": round(0.7 * wl, 3), "W": round(0.45 * wb, 3),
                               "z": round(max(ICE_TOP, hz(wc)) + 0.3, 3), "frontal_m2": round(0.7 * wl * 0.45 * wb, 3)}})
    # R-C9-234 (7): sketch A's SNAPPED MAST -- a stub standing from the hull's middle, leaning up-screen right and broken off
    # (its upper part lying on the ice beside the hull), and the fallen SPAR (the yard) lying diagonally from the gunwale
    # down across the ice toward the camera. Procedural timbers at true size (wood), one slot group
    nrm_w = (-ax_[1], ax_[0]) if -ax_[1] < 0 else (ax_[1], -ax_[0])        # across the hull, toward the camera (-v)
    lean_d = unit(0.75, 0.66)
    foot_ = (wc[0] - ax_[0] * 0.9, wc[1] - ax_[1] * 0.9)
    m_len, m_lean = 6.2, math.radians(16.0)
    top_ = (foot_[0] + lean_d[0] * m_len * math.sin(m_lean), foot_[1] + lean_d[1] * m_len * math.sin(m_lean))
    z_foot = ICE_TOP - 0.6
    def wpt(ta, tn, z=None, lift=None):
        q = (wc[0] + ax_[0] * ta + nrm_w[0] * tn, wc[1] + ax_[1] * ta + nrm_w[1] * tn)
        zq = z if z is not None else max(ICE_TOP - 0.03, hz(q)) + lift
        return [round(q[0], 3), round(-q[1], 3), round(zq, 3)]
    mast_beams = [
        {"type": "beam", "a": [round(foot_[0], 3), round(-foot_[1], 3), round(z_foot, 3)],
         "b": [round(top_[0], 3), round(-top_[1], 3), round(z_foot + m_len * math.cos(m_lean), 3)], "thickness_m": 0.38, "procedural": "log", "glb": None,
         "what": "the mast stub, snapped ~%.1f m above the ice" % (z_foot + m_len * math.cos(m_lean) - ICE_TOP)},
        {"type": "beam", "a": wpt(0.6, 1.6, z=ICE_TOP + 1.5), "b": wpt(4.6, 4.4, lift=0.12), "thickness_m": 0.24, "procedural": "log", "glb": None,
         "what": "the fallen spar (yard), from the gunwale down onto the ice"},
        ]
    group("wreck_mast", "debris", mast_beams)
    # -- the barrow front (N): its door threshold at the sketch's door, facing the camera
    bd = uv(BARROW["door"])
    sb = BARROW["width_m"] / ab(BARROW["glb"])[0]
    cb = (bd[0], bd[1] + 8.2 * sb)
    bins = model("barrow_front", "rock", BARROW["glb"], cb, (0.0, -1.0), sb, z=0.0, note="the monumental carved door; door %.2f x %.2f m" % (5.81 * sb * 25.8 / ab(BARROW["glb"])[0], 6.67 * sb * 25.8 / ab(BARROW["glb"])[0]))
    models.append({"id": "barrow_front", "kind": "barrow", "pos": bins["pos"], "z": 0.0, "godot_rot_y_deg": bins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": bins["size_m"][0], "d_local_z": bins["size_m"][1], "h": bins["size_m"][2]}, "glb": bins["glb"],
                   "burial_by_design": "R-C9-234 (6): the barrow front is SET INTO its mound (v1 practice: the door in the mound's face, a cutting "
                                       "to it): the build's back and roof run under the mound's front lobe by design; its front face, portal and door "
                                       "stand clear in the cutting (check (a) on the door)"})
    layout_pl[[q["id"] for q in layout_pl].index("barrow_front")]["burial_by_design"] = models[-1]["burial_by_design"]
    k_b = sb * 25.8 / ab(BARROW["glb"])[0]
    openings.append({"id": "barrow_door", "point": "N", "model": "barrow_front", "centre_sim": [round(bd[0], 4), round(-bd[1], 4)], "z0": 0.0,
                     "w": round(5.81 * k_b, 3), "h": round(6.67 * k_b, 3), "faces_deg": 180.0, "curtain_inset_m": 0.8, "dark": True})
    # -- the hall (E): sketch A's long side + great door facing the start; one uniform scale
    wa, wb2 = uv(HALL["wall_a"]), uv(HALL["wall_b"])
    wdir = unit(wb2[0] - wa[0], wb2[1] - wa[1])
    door = uv(HALL["door"])
    nrm = (-wdir[1], wdir[0])
    if nrm[0] * (0 - door[0]) + nrm[1] * (0 - door[1]) < 0:
        nrm = (-nrm[0], -nrm[1])
    sh = HALL["len_m"] / ab(HALL["glb"])[0]
    k_h = sh * 32.4 / ab(HALL["glb"])[0]
    fs = (nrm[0], -nrm[1])
    th = math.atan2(fs[0], fs[1])
    Xs = (math.cos(th), -math.sin(th))
    Xuv = (Xs[0], -Xs[1])
    hc = (door[0] - nrm[0] * 8.233 * k_h + Xuv[0] * 3.5875 * k_h, door[1] - nrm[1] * 8.233 * k_h + Xuv[1] * 3.5875 * k_h)
    hins = model("longhall", "wood", HALL["glb"], hc, nrm, sh, z=0.0, note="the burnt hall as sketch A draws it: long side and great door facing the start")
    models.append({"id": "longhall", "kind": "building", "pos": hins["pos"], "z": 0.0, "godot_rot_y_deg": hins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": hins["size_m"][0], "d_local_z": hins["size_m"][1], "h": hins["size_m"][2]}, "glb": hins["glb"]})
    openings.append({"id": "hall_great_door", "point": "E", "model": "longhall", "centre_sim": [round(door[0], 4), round(-door[1], 4)], "z0": 0.0,
                     "w": round(4.55 * k_h, 3), "h": round(4.75 * k_h, 3), "faces_deg": round(math.degrees(math.atan2(fs[0], -fs[1])) % 360, 3),
                     "curtain_inset_m": 1.6 * k_h, "dark": True})
    # -- the fallen gable (SE)
    gc = uv(GABLE["centre"])
    gn = unit(-gc[0], -gc[1])
    sg = GABLE["size_m"] / ab(GABLE["glb"])[0]
    gins = model("fallen_gable", "char", GABLE["glb"], gc, gn, sg, z=hz_min(gc, 3.0) - 0.05, note="its own collapsed ruin (R-C9-177/185)")
    models.append({"id": "fallen_gable", "kind": "ruin", "pos": gins["pos"], "z": gins["z"], "godot_rot_y_deg": gins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": gins["size_m"][0], "d_local_z": gins["size_m"][1], "h": gins["size_m"][2]}, "glb": gins["glb"]})
    openings.append({"id": "gable_breach", "point": "SE", "model": "fallen_gable", "centre_sim": gins["pos"], "z0": gins["z"], "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "h_rect", "centre": [round(gc[0] + gn[0] * 1.6, 4), round(-(gc[1] + gn[1] * 1.6), 4)],
                               "rot_deg": round(math.degrees(math.atan2(-gn[0], -gn[1])), 3), "L": 4.0, "W": 4.0, "z": round(gins["z"] + 0.5 * gins["size_m"][2], 3), "frontal_m2": 16.0}})
    # -- v1's stones: the broken ring at the start, the barrow-slope stones (uniform scale, rotation only)
    stone_insts, slope_insts = [], []
    for i, (p, ht, kind_) in enumerate([q for q in SLOPE_STONES if math.dist(uv(q[0]), K.centroid(mere)) > 3.0 and not K.point_in_poly(uv(q[0]), K.scale_about(mere, 1.12))]):
        g = V1M + "stone_%s.glb" % kind_
        c = uv(p)
        rot = (math.sin(i * 1.9 + 1), -abs(math.cos(i * 1.9 + 1)) - 0.2)
        slope_insts.append(model("slope_stone_%d" % i, "rock", g, c, unit(*rot), ht / ab(g)[1], z=hz_min(c, 0.6) - 0.1))
    # the KERB: standing stones round the mound's rim, along its visible (south) arc, every ~3.2 m (v1 stones, uniform)
    # R-C9-234 (6): round the UNION of the big dome and the front lobe -- the big dome's arc where the lobe does not cover
    # it, then the lobe's own arc round the door; never across the cutting's mouth, never at the mere
    a_m, b_m = MOUND["semi_m"]
    MF = MOUND_FRONT
    lfa, lfb = MF["semi_m"]
    kerb_insts = []
    kk = 0
    rho_main = lambda q: math.hypot((q[0] - mc[0]) / a_m, (q[1] - mc[1]) / b_m)
    rho_lobe = lambda q: math.hypot((q[0] - lc_[0]) / lfa, (q[1] - lc_[1]) / lfb)
    hw_toe = MF["cut_hw"] + MF["cut_flare"]
    near_mere = lambda q: K.point_in_poly(q, mere) or float(d_mere[min(max(int(round((v1 - q[1]) * HF_PPM)), 0), H - 1), min(max(int(round((q[0] - u0) * HF_PPM)), 0), W - 1)]) < 2.0
    for (ec, ea, eb, other) in ((mc, a_m, b_m, rho_lobe), (lc_, lfa, lfb, rho_main)):
        th_ = -math.pi * 0.98
        while th_ < -math.pi * 0.02:
            c = (ec[0] + ea * 1.03 * math.cos(th_), ec[1] + eb * 1.03 * math.sin(th_))
            if other(c) > 1.06 and abs(c[0] - bdc[0]) > hw_toe + 0.9 and not near_mere(c):
                kind_ = ("tall", "mid", "mid")[kk % 3]
                g = V1M + "stone_%s.glb" % kind_
                ht = (1.9, 1.5, 1.7)[kk % 3]
                out_ = unit(math.cos(th_) / ea, math.sin(th_) / eb)
                kerb_insts.append(model("kerb_stone_%d" % kk, "rock", g, c, out_, ht / ab(g)[1], z=hz_min(c, 0.4) - 0.1,
                                        note="R-C9-222/234: the barrow's kerb" + (" (front lobe)" if ec is lc_ else "")))
                kk += 1
            th_ += 3.2 / math.hypot(ea * math.sin(th_), eb * math.cos(th_))
    # the CUTTING's dry-stone walls (v1's stone-lined cutting): both sides from the lobe's toe to the facade, in ~0.9 m
    # courses, each course as high as the mound beside it (procedural rock at true size)
    cut_walls = []
    v_c = toe_v - 0.3
    while v_c < v_fac + 0.3:
        hw_v = MF["cut_hw"] + MF["cut_flare"] * min(1.0, max(0.0, (v_fac - v_c) / max(v_fac - toe_v, 0.1)))
        for side in (-1, 1):
            ui = bdc[0] + side * (hw_v - 0.05)
            uo = bdc[0] + side * (hw_v + 0.95)
            hgt = hz((bdc[0] + side * (hw_v + 1.2), v_c + 0.42))
            if hgt < 0.25:
                continue
            q4 = [(ui, v_c), (uo, v_c), (uo, v_c + 0.86), (ui, v_c + 0.86)]
            cut_walls.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(q4)], "z0": -0.3, "z1": round(min(hgt, 6.0) + 0.05, 3)})
        v_c += 0.9
    dropped_ = [q for q in slope_insts if math.hypot((q["pos"][0] - mc[0]) / a_m, (-q["pos"][1] - mc[1]) / b_m) <= 1.15]
    slope_insts = [q for q in slope_insts if math.hypot((q["pos"][0] - mc[0]) / a_m, (-q["pos"][1] - mc[1]) / b_m) > 1.15] + kerb_insts
    # R-C9-231 (P6' 78a2f41bd): a slope stone dropped inside the barrow's kerb is dropped from the layout of record too
    _dpos = {tuple(q["pos"]) for q in dropped_}
    layout_pl[:] = [e for e in layout_pl if not (e["id"].startswith("slope_stone_") and (round(e["uv"][0], 4), round(-e["uv"][1], 4)) in _dpos)]
    group("slope_stones", "stones", slope_insts)
    # R-C9-216 (Matt): a true, SYMMETRICAL stone circle -- 6 positions evenly spaced on one circle (the ring's own centre and
    # mean radius), 4 STANDING (full models, snow caps, a weathered lean <= 5 deg) and 2 FALLEN at non-adjacent positions,
    # each fallen stone ONLY its portion jutting from the ground (a low block <= 0.5 m proud, a snow drift at its base)
    ring_c = (sum(uv(p)[0] for p, _, _ in RING_STAND) / len(RING_STAND), sum(uv(p)[1] for p, _, _ in RING_STAND) / len(RING_STAND))
    ring_r = sum(math.dist(uv(p), ring_c) for p, _, _ in RING_STAND) / len(RING_STAND)
    a0 = math.atan2(uv(RING_STAND[0][0])[1] - ring_c[1], uv(RING_STAND[0][0])[0] - ring_c[0])
    ring_snow, ring_blocks = [], []
    standing_spec = [(2.2, "tall"), (1.9, "mid"), None, (2.1, "tall"), (2.0, "mid"), None]
    for i in range(6):
        ang = a0 + i * math.pi / 3
        c = (ring_c[0] + ring_r * math.cos(ang), ring_c[1] + ring_r * math.sin(ang))
        inward = unit(ring_c[0] - c[0], ring_c[1] - c[1])
        if standing_spec[i] is not None:
            ht, kind_ = standing_spec[i]
            g = V1M + "stone_%s.glb" % kind_
            ins = model("stone_%d" % i, "rock", g, c, inward, ht / ab(g)[1], z=hz_min(c, 0.4) - 0.08, note="R-C9-216: standing, ring position %d" % i)
            lean = math.radians(2.5 + 2.0 * ((i * 7) % 3) / 2)          # 2.5-4.5 deg, away from the centre
            ins["tilt_up_local"] = [round(-inward[0] * math.tan(lean), 5), 1.0, round(inward[1] * math.tan(lean), 5)]
            stone_insts.append(ins)
            r_ = ab(g)[0] * ht / ab(g)[1] * 0.42
            cap = [(c[0] + r_ * math.cos(q) * (0.85 + 0.15 * math.sin(3 * q + i)), c[1] + r_ * math.sin(q) * (0.85 + 0.15 * math.cos(2 * q + i))) for q in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
            ztop = hz_min(c, 0.4) - 0.08 + ht
            ring_snow.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(cap)], "z0": round(ztop - 0.12, 3), "z1": round(ztop + 0.06, 3)})
        else:
            tang = (-inward[1], inward[0])
            L_, B_ = 1.15, 0.55
            corners = [(-L_ / 2, -B_ / 2), (L_ / 2, -B_ / 2), (L_ / 2, B_ / 2), (-L_ / 2, B_ / 2)]
            blk = []
            for k, (x_, y_) in enumerate(corners):
                nx_, ny_ = corners[(k + 1) % 4]
                for f_ in (0.15, 0.85):
                    px = x_ + (nx_ - x_) * f_
                    py = y_ + (ny_ - y_) * f_
                    blk.append((c[0] + tang[0] * px + inward[0] * py, c[1] + tang[1] * px + inward[1] * py))
            g_lo = min(hz((q[0], q[1])) for q in blk)
            g_hi = max(hz((q[0], q[1])) for q in blk)
            # R-C9-234 (PT: "faint greybox remnant at 2_1's fallen stone"): the jutting stone no chamfered box -- the SAME
            # footprint and height as a weathered lump: a rounded irregular outline (own stream 2353) and a worn upper tier
            rngf = __import__("random").Random(2353 + i)
            ph_ = [rngf.uniform(0, 6.3) for _ in range(3)]
            lump = []
            for q in np.linspace(0, 2 * math.pi, 14, endpoint=False):
                cq, sq = math.cos(q), math.sin(q)
                sup = (abs(cq) ** 3 + abs(sq) ** 3) ** (-1 / 3)                  # a rounded box (superellipse, n = 3)
                f_ = sup * (1 + 0.07 * math.sin(2 * q + ph_[0]) + 0.05 * math.sin(3 * q + ph_[1]) + 0.04 * math.sin(5 * q + ph_[2]))
                px, py = L_ / 2 * cq * f_, B_ / 2 * sq * f_
                lump.append((c[0] + tang[0] * px + inward[0] * py, c[1] + tang[1] * px + inward[1] * py))
            ring_blocks.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(lump)], "z0": round(g_lo - 0.04, 3), "z1": round(g_hi + 0.27, 3)})
            top_ = K.scale_about(lump, 0.72)
            top_ = [(q[0] + inward[0] * 0.04, q[1] + inward[1] * 0.04) for q in top_]
            ring_blocks.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(top_)], "z0": round(g_lo - 0.04, 3), "z1": round(g_hi + 0.38, 3)})
            drift = [(c[0] + 0.95 * math.cos(q) * (1 + 0.12 * math.sin(3 * q)), c[1] + 0.75 * math.sin(q) * (1 + 0.12 * math.cos(2 * q))) for q in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
            ring_snow.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(drift)], "z0": round(g_lo - 0.04, 3), "z1": round(hz(c) + 0.12, 3)})
    group("ring_stones", "stones", stone_insts)
    crag_insts = []
    gcr = "data/bv2f/models/crag.glb"
    for i, (p, ht) in enumerate(CRAGS):
        c = uv(p)
        crag_insts.append(model("crag_%d" % i, "rock", gcr, c, unit(math.sin(i * 1.7), -1.0), ht / ab(gcr)[1], z=hz_min(c, 1.5) - 0.4))
    group("crags", "outcrop", crag_insts)
    # ================= THE CLIFF KIT along the curving S coast (R-C9-204 (2)) =================
    g_col, g_cape, g_cave, g_stk = kit("cliffcol"), kit("cliffcape"), kit("cavearch"), kit("seastack")
    cliff_insts, talus_insts = [], []
    foot_z = SEA_Z - 0.4                                   # the wave-cut notch at the waterline

    def lip_at(s):
        k = int(np.searchsorted(lip_s, s))
        k = min(max(k, 1), len(lip) - 1)
        a, b = lip[k - 1], lip[k]
        f = (s - lip_s[k - 1]) / max(lip_s[k] - lip_s[k - 1], 1e-6)
        p = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        d = unit(b[0] - a[0], b[1] - a[1])
        return p, d, (d[1], -d[0])

    def turn(s, h=3.0):
        _, d0, _ = lip_at(max(s - h, 0.5))
        _, d1, _ = lip_at(min(s + h, lip_s[-1] - 0.5))
        return math.degrees(math.atan2(d0[0] * d1[1] - d0[1] * d1[0], d0[0] * d1[0] + d0[1] * d1[1]))   # < 0: the coast turns seaward-convex
    s = 2.0
    k = 0
    prev_s, filled_gap = -99.0, False
    while s < lip_s[-1] - 1.0:
        p, d, n = lip_at(s)
        cape = turn(s) < -12.0
        g = g_cape if cape else g_col
        bx, by, bz = ab(g)
        top = float(np.interp(s, lip_s, crest)) + 1.0 + 0.3 * math.sin(k * 2.1)          # the columns stand ~1 m proud of the snow
        sc = (top - foot_z) / by
        hw_k = bx * sc / 2 - 0.8
        # R-C9-229 (1): the kit runs right up to the carved cave/gully (no bare skirt wall left showing): a piece is set
        # wherever its own width stays out of the carve mask's core
        blocked = lambda p_, d_, n_: max(float(carved_mask_at(*to_fr((p_[0] + d_[0] * k_ * hw_k - n_[0] * 1.0, p_[1] + d_[1] * k_ * hw_k - n_[1] * 1.0))))
                                         for k_ in (-1, -0.5, 0, 0.5, 1)) > 0.6
        if blocked(p, d, n):
            back = None
            if not filled_gap:
                for sb2 in np.arange(s - 0.5, prev_s - 2.5, -0.5):     # slide back toward the last piece: fill up to the carve
                    p2, d2, n2 = lip_at(sb2)
                    if not blocked(p2, d2, n2):
                        back = sb2
                        break
            filled_gap = True
            if back is None:
                s += 0.5
                continue
            s = back
            p, d, n = lip_at(s)
        else:
            filled_gap = False
        dep = bz * sc
        c = (p[0] + n[0] * (1.0 - dep / 2), p[1] + n[1] * (1.0 - dep / 2))          # front 1.0 m out: the face behind is the skirt
        cliff_insts.append(model("cliff_%d" % k, "rock", g, c, n, sc, z=foot_z, piece="cliffcape" if cape else "cliffcol", collider="trimesh",
                                 note="kit2 %s: %.1f m sea cliff (crest %.1f)" % ("cape" if cape else "column", top - SEA_Z, top)))
        # talus: fallen blocks at the foot, on the shore-fast ice
        for j in range(prng.randint(1, 3)):
            ht = prng.uniform(0.7, 2.0)
            q = (p[0] + n[0] * prng.uniform(1.4, 3.4) + d[0] * prng.uniform(-3.5, 3.5), p[1] + n[1] * prng.uniform(1.4, 3.4) + d[1] * prng.uniform(-3.5, 3.5))
            a = prng.uniform(0, 2 * math.pi)
            talus_insts.append(model("talus_%d" % len(talus_insts), "rock", g_stk, q, (math.sin(a), math.cos(a)), ht / ab(g_stk)[1], z=ICE_TOP - 0.3 * ht, piece="seastack",
                                     collider="box"))
        prev_s = s
        s += bx * sc * 0.62
        k += 1
    # -- R-C9-212/213/214: the route's rock is the CARVED mass (bv2pp_carve) -- no kit pieces, no shelf, nothing added onto it
    cave_w = R["mouth_w"]
    dep_c = CARVE["cave_depth"]
    s_back = CARVE["cove"]["s_back"]
    shelf_rocks = []
    stack_insts = []
    for i, (p, ht) in enumerate(STACKS_UV):
        a = 0.7 + i * 2.1
        stack_insts.append(model("stack_%d" % i, "rock", g_stk, p, (math.sin(a), math.cos(a)), (ht + 0.5) / ab(g_stk)[1], z=SEA_Z - 0.5, piece="seastack", collider="trimesh"))
    # R-C9-229 (1)/(2): the cliff-kit's own rounded rock round the cave and up both sides of the stair gully (seastack pieces,
    # one uniform scale each, rotation only): columns set into the gully's walls rising above the treads on both sides, two
    # on the knoll over the arch, one flanking the mouth on the face -- the carved mass behind them stays the walk surface
    rngg = __import__("random").Random(2292)
    gully_insts = []
    gbx, gby, gbz = ab(g_stk)
    sm_ = s_foot - 0.4
    while sm_ > s_top - 0.8:
        for side, t_edge, face_dir in (("w", t0s, dR), ("e", t1s, (-dR[0], -dR[1]))):
            plane_z = R["shelf_z"] + max(0.0, (s_foot + R["tread"]) - sm_) * rise / R["tread"]
            base = plane_z - 1.2
            topz = float(H_ts(np.array([t_edge + (-1.6 if side == "w" else 1.6)]), np.array([sm_]))[0]) + rngg.uniform(0.5, 1.9)
            sc_ = max(0.6, (topz - base) / gby)
            off = gbz * sc_ / 2 + 0.75 + rngg.uniform(0.0, 0.35)
            tc_ = t_edge - off if side == "w" else t_edge + off
            sc_c = sm_ + rngg.uniform(-0.4, 0.4)
            if side == "w" and sc_c + gbx * sc_ / 2 > -5.6:
                continue                                     # the cave's tunnel runs under the gully's W wall near its foot
            gully_insts.append(model("gully_col_%s_%d" % (side, len(gully_insts)), "rock", g_stk, fr(tc_, sc_c), face_dir, sc_, z=base, piece="seastack", collider="trimesh",
                                     note="R-C9-229: kit rock in the stair gully's %s wall" % side))
        sm_ -= rngg.uniform(1.8, 2.6)
    for k_, (aa, cc, zb, ht) in enumerate([(1.8, -2.1, 4.4, 2.6), (1.4, 2.0, 4.4, 2.2)]):     # on the knoll over the arch
        c_ = (R["cave_t"] + cax[0] * aa + (-cax[1]) * cc, CARVE["cove"]["s_back"] + cax[1] * aa + cax[0] * cc)
        sc_ = ht / gby
        gully_insts.append(model("cave_col_%d" % k_, "rock", g_stk, fr(*c_), nR, sc_, z=zb, piece="seastack", collider="trimesh", note="R-C9-229: kit rock over the cave's arch"))
    ht = (R["crest"] + 1.2) - (SEA_Z - 0.4)
    gully_insts.append(model("cave_col_w", "rock", g_stk, fr(R["cave_t"] - 4.4, 0.7), nR, ht / gby, z=SEA_Z - 0.4, piece="seastack", collider="trimesh",
                             note="R-C9-229: kit rock flanking the cave mouth on the face"))
    # R-C9-230: slumped rock on the eroded clifftop rim left of the cave (own stream; nothing else moves)
    rngz = __import__("random").Random(2301)
    for k_ in range(4):
        tq_ = rngz.uniform(0.5, 6.5)
        q_ = min(lip, key=lambda q: abs(to_fr(q)[0] - tq_))
        _, d_, n_ = lip_at(lip_s[lip.index(q_)])
        c_ = (q_[0] - n_[0] * rngz.uniform(0.3, 1.4), q_[1] - n_[1] * rngz.uniform(0.3, 1.4))
        ht = rngz.uniform(0.9, 1.8)
        a_ = rngz.uniform(0, 2 * math.pi)
        gully_insts.append(model("rim_slump_%d" % k_, "rock", g_stk, c_, (math.sin(a_), math.cos(a_)), ht / gby, z=hz(c_) - 0.45 * ht, piece="seastack", collider="box",
                                 note="R-C9-230: slumped rock on the clifftop rim"))
    # R-C9-231 (P6' 78a2f41bd): gully_col_e_1 stood 74 % inside the gully's E wall (undeclared) -- dropped (nothing else moves)
    _keep_ids = {e["id"] for e in layout_pl} - {"gully_col_e_1"}
    gully_insts = [q for q, e in zip(gully_insts, [e for e in layout_pl if e["id"].startswith(("gully_col", "cave_col", "rim_slump"))]) if e["id"] != "gully_col_e_1"]
    layout_pl[:] = [e for e in layout_pl if e["id"] != "gully_col_e_1"]
    group("gully_rock", "cliff", gully_insts)
    group("cliff_faces", "cliff", cliff_insts)
    group("talus", "talus", talus_insts)
    group("sea_stacks", "stack", stack_insts)
    mouth_c = fr(R["cave_t"], s_back)
    cax_uv = unit(cax[0] * dR[0] + cax[1] * nR[0], cax[0] * dR[1] + cax[1] * nR[1])      # the cave's axis, inland (uv)
    openings.append({"id": "sea_cave_mouth", "point": "S", "model": "carved_cave", "centre_sim": [round(mouth_c[0], 4), round(-mouth_c[1], 4)], "z0": R["shelf_z"],
                     "w": R["mouth_w"], "h": R["mouth_h"], "faces_deg": round(math.degrees(math.atan2(-cax_uv[0], -cax_uv[1])) % 360, 3),
                     "curtain_inset_m": round(dep_c - 0.6, 3), "curtain_w": 3.0, "curtain_h": 3.4, "dark": True,
                     "_": "R-C9-226: the cave worn into the shallow cove's back wall (its axis inland-west); a dark plane at the END of its tunnel (%.1f m in), so the mouth recedes into darkness" % (dep_c - 0.6)})
    # TIDAL SIGNS (R-C9-212/213): sea ice in the cove's water and pushed into the mouth's west side; icicles under the rime line
    LDc = CARVE["landing"]
    def sedge_f(t_):
        return LDc["s_front"] + 0.55 * math.sin(t_ * 0.9 + 0.4) + 0.3 * math.sin(t_ * 2.3 + 1.7) + 0.15 * math.sin(t_ * 5.1)
    rngc = __import__("random").Random(2263)
    cove_ice, icicles = [], []
    placed_ = []
    for k in range(80):                                   # R-C9-228: floes in the sea at the cave's mouth and off the ledge
        if len(placed_) >= 14:
            break
        ct = rngc.uniform(R["cave_t"] - 5.0, t1s + 0.8)
        cs_ = sedge_f(ct) + rngc.uniform(0.45, 2.6) if ct > R["cave_t"] - 1.5 else rngc.uniform(0.6, 2.6)
        r_ = rngc.uniform(0.25, 0.8)
        if any(math.hypot(ct - q[0], cs_ - q[1]) < r_ + q[2] + 0.15 for q in placed_):
            continue
        placed_.append((ct, cs_, r_))
        pg = [fr(ct + r_ * math.cos(a_) * rngc.uniform(0.7, 1.15), cs_ + r_ * math.sin(a_) * rngc.uniform(0.6, 1.0)) for a_ in np.linspace(0, 2 * math.pi, 7, endpoint=False)]
        cove_ice.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(pg)], "z0": round(SEA_Z - 0.3, 3), "z1": round(ICE_TOP + rngc.uniform(-0.12, 0.12), 3)})
    hwz = CARVE["high_water"]
    for k in rime_k[::max(1, len(rime_k) // 40)][:40]:     # icicles under the rime: a sliver hanging just proud of the face
        c3 = loc[k].mean(0)
        nh = nloc[k]
        nh2 = math.hypot(nh[0], nh[2]) + 1e-9
        ox, oz = nh[0] / nh2 * 0.06, nh[2] / nh2 * 0.06
        L_ = rngc.uniform(0.15, 0.45)
        w_ = rngc.uniform(0.03, 0.06)
        cu_, cv_ = c3[0] + ox, -(c3[2] + oz)
        icicles.append({"poly": [[round(cu_ - w_, 3), round(cv_, 3)], [round(cu_ + w_, 3), round(cv_, 3)], [round(cu_, 3), round(cv_ + w_, 3)]],
                        "z0": round(hwz - L_, 3), "z1": round(hwz + 0.04, 3)})
    # the OLD SHELF's place: shore-fast ice now (its own cells and draws; the rest of the pack is as Matt passed it), kept off
    # the new landing and the cove's water (seaward of s 1.4)
    old_shelf_ice = []
    rngo = __import__("random").Random(2274)
    bxs = (min(q[0] for q in shelf_legacy) - 1, min(q[1] for q in shelf_legacy) - 1, max(q[0] for q in shelf_legacy) + 1, max(q[1] for q in shelf_legacy) + 1)
    seeds2 = K.jitter_seeds(bxs, 2.6, rng209, lambda p: K.point_in_poly(p, shelf_legacy) and to_fr(p)[1] > 0.6)
    for cell in K.voronoi_cells(seeds2, bxs):
        if len(cell) < 3:
            continue
        inner = [q for q in cell if K.point_in_poly(q, shelf_legacy)]
        sh = K.shrink(cell, rng209.uniform(0.1, 0.35) * min(3.5, max(0.2, math.exp(rngo.gauss(0.0, 0.8)))))   # R-C9-227 (3): gaps of every width
        if not sh or len(inner) < 2:
            continue
        rough = K.roughen(sh, rng209, 0.1, 0.8)
        z1q = rng209.uniform(-0.06, 0.12)
        # cells that would lie in the new cove's opening (its water and the landing's front) are left out whole -- an irregular
        # edge of floes, never a clipped straight line
        if any(CARVE["cove"]["t_w"] - 0.6 < to_fr(q)[0] < CARVE["cove"]["t_e"] + 0.6 and to_fr(q)[1] < 1.3 for q in rough) or K.area(rough) < 0.3:
            continue
        old_shelf_ice.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(rough)], "z0": round(SEA_Z - 0.4, 3), "z1": round(ICE_TOP + z1q, 3)})
    # R-C9-226 (1): THE TREADS -- every tread its own stone: each row of the flight split into 3-4 blocks of varied width, with
    # cracks between them and between the rows (the groove's bed shows dark below); each block sits a little lower toward the
    # sea (its inland neighbour's sea-side face shows, grey); fronts set back unevenly, corners worn; SNOW lies on the back of
    # each block's top only -- the stone is bare along the front edge (sketch A: white treads, grey nosings), so from the
    # play camera every tread reads as its own snow-capped block, never a plank. The lowest rows rougher (R-C9-215).
    # Every top <= the walk ramp through the nosings.
    rngt = __import__("random").Random(2264)
    tread_blocks, tread_snow, treads_uv = [], [], []
    for i in range(n_tr):
        sf_ = s_foot - i * R["tread"]                       # the row's FRONT (downhill, seaward) edge; it climbs toward -s
        ztop = R["shelf_z"] + (i + 1) * rise
        rough_ = 1.0 if i >= 3 else 1.8
        nb = rngt.choice((2, 3, 3, 4))
        wts = [rngt.uniform(0.45, 1.6) for _ in range(nb)]           # R-C9-229 (2): stones of very different lengths, staggered joints
        edges = [t0s]
        for w_ in wts:
            edges.append(edges[-1] + W_ * w_ / sum(wts))
        side_drop = [rngt.uniform(0.0, 0.1) for _ in range(nb)]
        for j in range(nb):
            ta_ = edges[j] + (0.0 if j == 0 else 0.065)
            tb_ = edges[j + 1] - (0.0 if j == nb - 1 else 0.065)
            f0 = sf_ - rngt.uniform(0.0, 0.14) * rough_            # fronts only ever set BACK (inland) of the nosing line, unevenly
            f1 = sf_ - rngt.uniform(0.0, 0.14) * rough_
            bk = sf_ - R["tread"] + rngt.uniform(0.045, 0.075)
            ch = rngt.uniform(0.06, 0.12) * rough_
            fm = lambda x_: f0 + (f1 - f0) * x_
            pts_ = [(ta_, fm(0) - ch), (ta_ + ch, fm(0)), ((ta_ + tb_) / 2, fm(0.5) - rngt.uniform(0, 0.03) * rough_), (tb_ - ch, fm(1)), (tb_, fm(1) - ch),
                    (tb_, bk + ch * 0.6), (tb_ - ch * 0.6, bk), (ta_ + ch * 0.6, bk), (ta_, bk + ch * 0.6)]
            poly = [fr(q[0], q[1]) for q in pts_]
            zt = ztop - rngt.uniform(0.0, 0.03) * rough_ - side_drop[j]
            tread_blocks.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(poly)], "z0": round(ztop - rise - 0.45, 3), "z1": round(zt, 3)})
            # R-C9-229 (2): SNOW in irregular patches on the stone (drifted against the back and the gully walls), never a full-width
            # band; some stones bare
            if rngt.random() < 0.18:
                continue
            for _pt in range(rngt.choice((1, 1, 2))):
                wid = (tb_ - ta_) * rngt.uniform(0.25, 0.7)
                bias = -0.25 if j == 0 else (0.25 if j == nb - 1 else 0.0)
                tcn = ta_ + (tb_ - ta_) * min(0.85, max(0.15, 0.5 + bias + rngt.uniform(-0.25, 0.25)))
                scn = bk + (fm(0.5) - bk) * rngt.uniform(0.25, 0.55)
                dep = (fm(0.5) - bk) * rngt.uniform(0.35, 0.7)
                ph = rngt.uniform(0, 6.3)
                cap = [fr(tcn + wid / 2 * math.cos(a_) * (1 + 0.18 * math.sin(3 * a_ + ph)), scn + dep / 2 * math.sin(a_) * (1 + 0.15 * math.cos(2 * a_ + ph)))
                       for a_ in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
                tread_snow.append({"poly": [[round(q[0], 3), round(-q[1], 3)] for q in K.ccw(cap)], "z0": round(zt - 0.03, 3), "z1": round(zt + rngt.uniform(0.025, 0.05), 3)})
                treads_uv.append({"id": "tread_%02d_%d_%d" % (i, j, _pt), "z_m": round(zt, 4), "outline_uv": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(cap)]})
    json.dump({"_what": "R-C9-216/226: the stair's tread stones (each block's top), for PT's 3D snow layer (DEV-22); z = the block's top (m; the walk ramp runs through the nosings)",
               "frame": "v1 (u, v) metres", "treads": treads_uv}, open(os.path.join(ART, "stair_treads.json"), "w"), indent=1)
    jit = [0.0] * n_r
    treads, snow_lips = tread_blocks, tread_snow
    # the walk surface: one plane through the nosings, from the landing one tread out from the foot to the top pad's edge
    s_lo, s_hi = s_top, s_foot + R["tread"]
    run_h = s_hi - s_lo
    rc = fr((t0s + t1s) / 2, (s_lo + s_hi) / 2)
    theta = math.atan2(top_z - R["shelf_z"], run_h)
    dn = (nR[0], nR[1])                                    # local +Z downhill = seaward (+s)
    ramp = {"id": "stair_ramp", "c_sim": [round(rc[0], 4), round(-rc[1], 4)], "z_c": round((top_z + R["shelf_z"]) / 2, 4), "across": W_,
            "along_h": round(run_h, 4), "along": round(math.hypot(run_h, top_z - R["shelf_z"]), 4), "thick": 0.3, "yaw_deg": round(yaw_of(dn), 4),
            "pitch_deg": round(math.degrees(theta), 4), "dir_sim": [round(dn[0], 6), round(-dn[1], 6)],
            "_": "a plane through every nosing: the pad's height at the top edge, the landing one tread out from the foot; local +Z downhill (seaward)"}
    lc = fr((t0s + t1s) / 2, (s_top + s_land) / 2)
    plate = {"id": "landing_plate", "c_sim": [round(lc[0], 4), round(-lc[1], 4)], "z_c": top_z, "across": W_, "along_h": round(s_top - s_land, 4),
             "along": round(s_top - s_land, 4), "thick": 0.3, "yaw_deg": round(yaw_of(dn), 4), "pitch_deg": 0.0, "dir_sim": [round(dn[0], 6), round(-dn[1], 6)],
             "_": "the top pad's walk surface: a plate at the clifftop's height meeting the ramp's top edge"}
    # -- the palisade (procedural posts at true size) and the yard logs
    post_insts = []
    k_post = 0
    for run_ in PALISADE:
        pts = [uv(p) for p in run_]
        for a, b in zip(pts[:-1], pts[1:]):
            L = math.dist(a, b)
            n_ = max(1, int(L / 0.45))
            for j in range(n_):
                f = (j + 0.5) / n_
                c = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
                k_post += 1
                if k_post % 9 in (4, 5):
                    continue
                ht = 2.4 + 0.7 * ((len(post_insts) * 13) % 10) / 10
                z0 = hz(c) - 0.3
                lean = (0.12 * math.sin(len(post_insts)), 0.12 * math.cos(len(post_insts) * 1.3))
                post_insts.append({"type": "beam", "a": [round(c[0], 3), round(-c[1], 3), round(z0, 3)],
                                   "b": [round(c[0] + lean[0], 3), round(-(c[1] + lean[1]), 3), round(z0 + ht, 3)], "thickness_m": 0.22, "procedural": "post", "glb": None})
    group("palisade", "palisade", post_insts)
    log_insts = []
    for (pa_, pb_) in LOGS:
        a, b = uv(pa_), uv(pb_)
        log_insts.append({"type": "beam", "a": [round(a[0], 3), round(-a[1], 3), round(hz(a) + 0.17, 3)], "b": [round(b[0], 3), round(-b[1], 3), round(hz(b) + 0.17, 3)],
                          "thickness_m": 0.34, "procedural": "log", "glb": None})
    group("logs", "debris", log_insts)
    # -- the mere (an opening of its own: the ice)
    openings.append({"id": "mere_ice", "point": "NW", "model": "mere", "centre_sim": [round(mc_[0], 4), round(-mc_[1], 4)], "z0": 0.0, "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "poly", "polygon": [[round(q[0], 3), round(-q[1], 3)] for q in mere], "z": round(MERE_SHAPE["plate_top"] + 0.03, 3), "frontal_m2": round(K.area(mere), 3)}})
    for o in openings:
        if o.get("w") and "probe" not in o:
            o["probe"] = {"type": "v", "centre": o["centre_sim"], "faces_deg": o["faces_deg"], "w": o["w"], "h": o["h"], "z0": o["z0"], "frontal_m2": round(o["w"] * o["h"], 3)}

    # ---------------- the SLABS: every ice plate, floe, rime strip, tread and snow lip (procedural prisms at true size) ----
    def sim_poly(poly):
        return [[q[0], -q[1]] for q in poly]
    slabs = {"ice_shorefast": {"class": "shore_ice", "items": []}, "ice_plates": {"class": "shore_ice", "items": []},
             "ice_floes": {"class": "shore_ice", "items": []}, "ice_floes_bob": {"class": "shore_ice", "items": [], "bob": True},
             "mere_plates": {"class": "ice", "items": []}, "stream_ice": {"class": "ice", "items": []}}
    gk = {"fast": "ice_shorefast", "plate": "ice_plates", "floe": "ice_floes"}
    for e in ice:
        gid = "ice_floes_bob" if e["bob"] else gk[e["zone"]]
        slabs[gid]["items"].append({"poly": sim_poly(e["poly"]), "z0": round(SEA_Z - 0.4, 3), "z1": e["top"]})
    slabs["ice_rims"] = {"class": "snow", "items": rims}
    slabs["ice_ridges"] = {"class": "shore_ice", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in ridges]}
    slabs["ice_brash"] = {"class": "shore_ice", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in brash]}
    slabs["ice_rims"]["items"] = [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in rims]
    for e in mere_ice:
        slabs["mere_plates"]["items"].append({"poly": sim_poly(e["poly"]), "z0": MERE_SHAPE["bed_z"] - 0.05, "z1": e["top"]})
    slabs["mere_cracks"] = {"class": "sea", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in mere_cracks]}
    slabs["mere_seams"] = {"class": "snow", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in mere_seams]}
    slabs["trans_leads"] = {"class": "sea", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in trans_plates if e["cls"] == "lead"]}
    slabs["trans_rubble"] = {"class": "shore_ice", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in trans_plates if e["cls"] == "rubble"]}
    # R-C9-234 (2): no octagon pads (the islands are raised GROUND now, see above). REED BEDS: every clump a tuft of thin tall
    # blades (sketch A's pale reeds, 0.5-1.2 m, taller in the middle), class `reed`, standing on its straw ground patch
    rngb = __import__("random").Random(2351)
    blades, reed_out = [], []
    for k_, cl in enumerate(clumps):
        c = cl["c"]
        gz = hz(c)
        n_b = rngb.randint(9, 16)
        top_max = 0.0
        for _b in range(n_b):
            rr_ = cl["r"] * math.sqrt(rngb.random())
            aa_ = rngb.uniform(0, 2 * math.pi)
            bc_ = (c[0] + rr_ * math.cos(aa_), c[1] + rr_ * math.sin(aa_))
            ht_ = (0.55 + 0.6 * (1.0 - rr_ / cl["r"])) * rngb.uniform(0.75, 1.15)
            wb_, tb_ = rngb.uniform(0.05, 0.09), rngb.uniform(0.022, 0.04)
            ab_ = rngb.uniform(0, math.pi)
            ca, sa = math.cos(ab_), math.sin(ab_)
            q4 = [(bc_[0] + ca * wb_ / 2 * sx - sa * tb_ / 2 * sy, bc_[1] + sa * wb_ / 2 * sx + ca * tb_ / 2 * sy) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            g_ = hz(bc_)
            blades.append({"poly": sim_poly(K.ccw(q4)), "z0": round(g_ - 0.05, 3), "z1": round(g_ + ht_, 3)})
            top_max = max(top_max, ht_)
        reed_out.append({"id": "reed_%02d" % k_, "on": cl["on"], "centre_uv": [round(c[0], 3), round(c[1], 3)], "radius_m": round(cl["r"], 3),
                         "ground_z_m": round(gz, 3), "blades": n_b, "top_m": round(gz + top_max, 3)})
    slabs["reed_tufts"] = {"class": "reed", "items": blades}
    json.dump({"_what": "R-C9-234 (2): the reed beds of the blockout (sketch A's tall pale reeds) -- one entry per clump; class `reed` blades on a straw ground patch; for PT's DEV-21 reed cards",
               "frame": "v1 (u, v) metres", "islands": [{"centre_uv": [round(e["c"][0], 3), round(e["c"][1], 3)], "radius_m": round(e["R"], 3), "elong": round(e["el"], 3),
                                                        "rise_m": round(e["h"], 3), "where": e["where"], "kind": e["kind"]} for e in islands],
               "clumps": reed_out}, open(os.path.join(ART, "reed_beds.json"), "w"), indent=1)
    # (R-C9-234: no river_water prisms -- the river is the ground's own `sea` class along its channel)
    slabs["stream_cracks"] = {"class": "sea", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in stream_cracks]}
    slabs["stream_pressure"] = {"class": "ice", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in stream_press]}
    slabs["ring_fallen"] = {"class": "rock", "items": ring_blocks}
    slabs["barrow_cutting"] = {"class": "rock", "items": cut_walls}          # R-C9-234 (6): the cutting's dry-stone walls
    slabs["ring_snow"] = {"class": "snow", "items": ring_snow}
    slabs["cove_ice"] = {"class": "shore_ice", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in cove_ice + old_shelf_ice]}
    slabs["icicles"] = {"class": "rime", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in icicles]}
    # R-C9-228 (2): a few thin cracks wandering across the wreck's shore-fast ice cradle
    rngq = __import__("random").Random(2282)
    cr_items = []
    jj_, ii_ = np.nonzero(cradle_ice)
    for _ in range(5 if len(jj_) else 0):
        k_ = rngq.randrange(len(jj_))
        p_ = (us[ii_[k_]], vs[jj_[k_]])
        hd = rngq.uniform(0, 2 * math.pi)
        for _s in range(int(rngq.uniform(6, 22))):
            hd += rngq.gauss(0, 0.3)
            q_ = (p_[0] + 0.45 * math.cos(hd), p_[1] + 0.45 * math.sin(hd))
            iq, jq = int(round((q_[0] - u0) * HF_PPM)), int(round((v1 - q_[1]) * HF_PPM))
            if not (0 <= jq < H and 0 <= iq < W and cradle_ice[jq, iq]):
                break
            w_ = rngq.uniform(0.03, 0.07)
            nn = (-math.sin(hd) * w_ / 2, math.cos(hd) * w_ / 2)
            cr_items.append({"poly": sim_poly(K.ccw([(p_[0] - nn[0], p_[1] - nn[1]), (q_[0] - nn[0], q_[1] - nn[1]), (q_[0] + nn[0], q_[1] + nn[1]), (p_[0] + nn[0], p_[1] + nn[1])])),
                             "z0": round(ICE_TOP - 0.06, 3), "z1": round(ICE_TOP - 0.02, 3)})
            p_ = q_
    slabs["cradle_cracks"] = {"class": "sea", "items": cr_items}
    # R-C9-229 (3): a few rocks on the iced ledge, along its ragged sea edge and against the cliff (kept off the route's middle)
    rngl = __import__("random").Random(2293)
    lrocks = []
    spots = [(t_, sedge_f(t_) - rngl.uniform(0.3, 0.7)) for t_ in (rngl.uniform(R["cave_t"] - 3.5, R["cave_t"] - 1.5), rngl.uniform(t0s + 0.5, t0s + 2.0),
                                                                       rngl.uniform(t1s - 2.0, t1s - 0.4), rngl.uniform(R["cave_t"] + 0.5, t0s - 0.5))] + \
            [(t1s - rngl.uniform(0.3, 0.8), s_foot + rngl.uniform(0.3, 1.2)), (t0s + rngl.uniform(0.3, 0.8), s_foot + rngl.uniform(0.6, 1.6))]
    for (t_, s_) in spots:
        r_ = rngl.uniform(0.3, 0.7)
        base_ = [fr(t_ + r_ * math.cos(b_) * rngl.uniform(0.7, 1.2), s_ + r_ * math.sin(b_) * rngl.uniform(0.7, 1.2)) for b_ in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
        h_ = rngl.uniform(0.3, 0.8)
        for f_, dz in ((1.0, 0.0), (0.7, h_ * 0.55), (0.4, h_)):
            lrocks.append({"poly": sim_poly(K.scale_about(K.ccw(base_), f_)), "z0": round(R["shelf_z"] - 0.1, 3), "z1": round(R["shelf_z"] + h_ * 0.5 + dz, 3)})
    slabs["ledge_rocks"] = {"class": "rock", "items": lrocks}
    slabs["stair_treads"] = {"class": "rock", "items": tread_blocks}      # R-C9-226 (1): every tread its own stone
    slabs["stair_snow"] = {"class": "snow", "items": tread_snow}
    # the CLIFF SKIRT: the face behind the kit, a 0.35 m rock band along the lip from the sea to the crest (the heightfield's
    # own face cells are not drawn) -- outside the route stretch, which has its own rock
    # R-C9-208 (5): the skirt is a continuous RIBBON wall along the lip (top = the clifftop behind it), broken only at the cave's
    # mouth and the stair's landing
    lip_f = K.resample(lip, 0.5)
    runs, cur = [], []
    for a in lip_f:
        ta, sa = to_fr(a)
        gap = float(carved_mask_at(ta, sa)) > 0.3                                   # R-C9-226: the carved mass is the face there
        if gap:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        cur.append(a)
    if len(cur) > 1:
        runs.append(cur)
    skirt_runs = []
    for rn in runs:
        pts = []
        for i, a in enumerate(rn):
            b = rn[min(i + 1, len(rn) - 1)] if i < len(rn) - 1 else rn[i - 1]
            dd = unit(rn[min(i + 1, len(rn) - 1)][0] - rn[max(i - 1, 0)][0], rn[min(i + 1, len(rn) - 1)][1] - rn[max(i - 1, 0)][1])
            nn = (dd[1], -dd[0])
            top = hz((a[0] - nn[0] * 0.7, a[1] - nn[1] * 0.7)) - 0.04
            pts.append([round(a[0] - nn[0] * 0.1, 3), round(-(a[1] - nn[1] * 0.1), 3), round(max(top, ICE_TOP + 0.2), 3)])
        skirt_runs.append({"pts": pts, "z0": SEA_Z - 0.6, "thick": 0.4})
    ribbons = {"cliff_skirt_wall": {"class": "rock", "items": skirt_runs}}

    # ---------------- the window, sections, bounds, knight ----------------
    GUIDE = (1280 * 4 + 1536, 768 * 4 + 1024)
    sk_c = uv((768, 512))
    win_c = (round(sk_c[0], 3), round(sk_c[1], 3))
    half = (GUIDE[0] / 2 / PPM, GUIDE[1] / 2 / PX_V)
    wu = [win_c[0] - half[0], win_c[0] + half[0]]
    wv = [win_c[1] - half[1], win_c[1] + half[1]]
    PAD = 64
    sx, sy = 2, 2
    sw_, sh_ = GUIDE[0] // sx, GUIDE[1] // sy
    sections = []
    for j in range(sy):
        for i in range(sx):
            cx, cy = sw_ * (i + 0.5), sh_ * (j + 0.5)
            c = [wu[0] + cx / PPM, wv[1] - cy / PX_V]
            sections.append({"id": f"s{j}{i}", "px_origin": [sw_ * i, sh_ * j], "px": [sw_, sh_], "centre_uv": c,
                             "u": [c[0] - (sw_ / 2 + PAD) / PPM, c[0] + (sw_ / 2 + PAD) / PPM], "v": [c[1] - (sh_ / 2 + PAD) / PX_V, c[1] + (sh_ / 2 + PAD) / PX_V]})
    for s_ in sections:
        json.dump({"_what": "BV2F LV Tier-B --frame-grid, guide section %s of the art blockout" % s_["id"], "name": "barrow_v2 art " + s_["id"], "variant": "art",
                   "scene": "res://scenes/bv2f_barrow_v2.tscn", "guide_px": [s_["px"][0] + 2 * PAD, s_["px"][1] + 2 * PAD], "pad_px": PAD, "px_per_m_across": PPM,
                   "pitch_deg": 52.95354112560294, "yaw_deg": 47.0, "walk_grid": {"u": [-1.0, 1.0], "v": [-1.0, 1.0], "step": 0.1},
                   "topdown": {"px": [2400, 2240], "px_per_m": 30.0}, "section": s_["id"]}, open(os.path.join(ART, f"frame_grid_{s_['id']}.json"), "w"), indent=1)
    # walkable: the plateau, the beach and the shore-fast ice off it (the wreck), the route. Outer walls -7.5 .. +6; inner walls
    # stand on the clifftop wherever the plateau ends in a drop (open only at the stair's landing)
    ob = R["bounds_out_m"]
    off_shore = []
    for i, p in enumerate(shore):
        a = shore[max(i - 1, 0)]
        b = shore[min(i + 1, len(shore) - 1)]
        d = unit(b[0] - a[0], b[1] - a[1])
        n = (d[1], -d[0])                                   # land is east of a north->south chain: seaward = (d_y, -d_x) turned west
        n = n if n[0] < 0 else (-n[0], -n[1])
        bw_p = BEACH_W - 4.0 * min(1.0, max(0.0, (p[1] - 6.0) / 8.0)) + 1.5      # the beach and 1.5 m of the shore ice off it
        off_shore.append((p[0] + n[0] * bw_p, p[1] + n[1] * bw_p))
    lip_route_w = [q for q, s_ in zip(lip, lip_s) if s_ < a_s + R["shelf_t"][0] - 3.5]
    off_lip_w = []
    for i, p in enumerate(lip_route_w):
        _, d, n = lip_at(lip_s[i])
        off_lip_w.append((p[0] + n[0] * 3.0, p[1] + n[1] * 3.0))
    # R-C9-226: the outer wall runs along the cliff's edge west of the cove, across the cove's mouth just off the landing's
    # ragged edge, then along the cliff's edge east of it
    te_ = t1s + 0.6
    lip_mid = [q for q, s_ in zip(lip, lip_s) if a_s + R["shelf_t"][0] - 3.5 <= s_ and to_fr(q)[0] < R["cave_t"] - 4.0]
    route_out = lip_mid + [fr(R["cave_t"] - 4.0, 0.6)] + [fr(t_, sedge_f(t_) + 0.45) for t_ in np.arange(R["cave_t"] - 3.5, te_ + 0.01, 0.5)] + [fr(te_ + 0.3, 0.4)]
    lip_route_e = [q for q in lip if to_fr(q)[0] > te_ + 0.5]
    bpoly = [q for q in off_shore if q[1] < wv[1] + 2] + off_lip_w + route_out + lip_route_e
    bpoly = [q for q in bpoly if q[0] <= wu[1] + 2]
    bpoly += [(wu[1], bpoly[-1][1]), (wu[1], wv[1] + 2), (off_shore[0][0], wv[1] + 2)]
    iw = 0.45
    # inner walls on the clifftop's edge, each with its own height band: over the cave they start above its arch (the cave is
    # walked beneath them); along both sides of the stair's cleft (on the clifftop beside it) up to the top pad, open there
    # R-C9-228: on the clifftop's edge everywhere, over the cave's corner above its arch, along both sides of the stair gully up
    # to the top pad (open there)
    arch_z = R["shelf_z"] + CARVE["mouth_h_cut"] + 0.4
    tw_ = R["cave_t"] - 4.0
    inner = [{"pts": [(q[0] - lip_at(s_)[2][0] * iw, q[1] - lip_at(s_)[2][1] * iw) for q, s_ in zip(lip, lip_s) if to_fr(q)[0] < tw_] + [fr(tw_, -0.45)], "z": [-1.5, 6.0]},
             {"pts": [fr(tw_, -0.45), fr(t0s - 0.8, -0.45), fr(t0s - 0.8, s_foot - 0.6)], "z": [arch_z, 10.0]},
             {"pts": [fr(t0s - 0.8, s_foot - 0.6), fr(t0s - 0.8, s_top)], "z": [-1.5, 10.0]},
             {"pts": [fr(t1s + 0.8, s_top), fr(t1s + 0.8, -0.45)] + [(q[0] - lip_at(s_)[2][0] * iw, q[1] - lip_at(s_)[2][1] * iw) for q, s_ in zip(lip, lip_s) if to_fr(q)[0] > t1s + 0.8],
              "z": [-1.5, 6.0]}]
    tints = json.load(open(os.path.join(BF, "data", "barrow_full_layout.json")))["tints_srgb"]
    tints.update(json.load(open(os.path.join(LV, "DEV12_proposal.json")))["class_list"]["new_classes_DEV2_provisional"])
    # R-C9-213 tidal classes (provisional tints, for PT/PH's palette): the iced landing, the wet rock below high water, the rime line
    tints.update({"tide_ice": [0.74, 0.82, 0.87], "wet_rock": [0.36, 0.37, 0.39], "rime": [0.9, 0.93, 0.96], "ice_mid": [0.75, 0.822, 0.88]})
    tints.update({"reed": REED_TINT})                    # R-C9-234 (2): the reed beds (provisional, for PT/PH's palette)
    hf = {"file": "terrain_h.f32", "walk_file": "terrain_walk_h.f32", "shape": [H, W], "px_per_m": HF_PPM, "extent_sim_m": {"x0": u0, "x1": u1, "y0": -v1, "y1": -v0}, "sha256": sha(os.path.join(OUT, "terrain_h.f32"))}
    route_sim = {"ramp": ramp, "walk_boxes": [ramp, plate], "heightfield_collider": True, "hf_collider_v_max": 99.0, "floor_box_v_min": 999.0, "shelf_z": R["shelf_z"],
                 "hood": [], "_": "Phase 1'': the terrain is the walk collider everywhere (HeightMapShape3D); the stair's walk ramp and the landing plate (colliders only)"}
    level = {
        "_what": "BV2F lane LV Phase 1'': barrow_v2 ART blockout (sketch A, v1 practice; R-C9-204/206 coast, water, no paths) as a level of the v1 Barrow; read by scripts/bv2f/bv2f_level.gd; written by fid/lv/tools/make_bv2art.py",
        "tints_srgb": tints, "classes": names,
        "knight": {"spawn_uv": [0.0, 0.0], "spawn_facing": "S", "guide_uv": [0.0, 0.0], "guide_facing": "S", "gear_stack": 4},
        "frame": {"guide_window": {"centre_uv": sections[0]["centre_uv"], "u": sections[0]["u"], "v": sections[0]["v"]},
                  "envelope": {"u": wu, "v": wv, "px": list(GUIDE), "centre_uv": list(win_c)}, "sections": sections},
        "camera_clamp_default": False,
        "regions": {"ice": {"centre_uv": [round(mc_[0], 3), round(mc_[1], 3)], "axes_m": [2 * MERE_SHAPE["radii"][0], 2 * MERE_SHAPE["radii"][1]]}},
        "placements": [{"id": "mound", "kind": "structure", "uv": [0.0, 60.0], "semi_axes": [1.0, 1.0], "rise_m": 0.0, "exponent": 1.0, "toe_rho": 0.2,
                        "cutting": {"half_w": 0.0, "v_facade": -999.0}, "passage": {"half_w": 0.0, "v0": 0.0, "v_end": 0.0, "risers_v": [], "riser_m": 0.0},
                        "_": "STUB for the frozen capture tool's walk-grid statistics (v1's mound spec); the art mound is terrain"}],
        "bounds": {"polygon_uv": [[round(p[0], 3), round(p[1], 3)] for p in bpoly], "wall_z_m": [SEA_Z - 3.0, 6.0],
                   "inner_walls_uv": [[[round(q[0], 3), round(q[1], 3)] for q in w["pts"]] for w in inner if len(w["pts"]) >= 2], "inner_wall_z_m": [-1.5, 6.0],
                   "inner_walls_z_m": [w["z"] for w in inner if len(w["pts"]) >= 2],
                   "_": "Phase 1'': outer walls -7.5 .. +6 round the plateau, the beach, the shore ice off it and the route; inner walls on the clifftop's edge (open at the stair's landing)"},
        "crucible": {"eye_height_m": 1.6, "station": {"uv": [0.0, 0.0]}, "boss_gate": {"uv": [round(bd[0], 3), round(bd[1], 3)]}, "spawns": []},
        "sim": {"heightfield": hf, "classes_png": {"file": "classes_png.bin", "px_per_m": CLS_PPM, "extent_sim_m": hf["extent_sim_m"], "sha256": sha(os.path.join(OUT, "classes_png.bin"))},
                "sea_z": SEA_Z, "models": models, "features": [], "blobs": [], "openings": openings, "stair_steps": [], "slabs": slabs, "ribbons": ribbons,
                "carved": {"files": carved_files, "_": "R-C9-212/213/214: the cave section carved from one rock mass (bv2pp_carve.py): per class, (x, h, z) Level-local triangles + normals as <f4 [pos3, nrm3] rows"},
                "route": route_sim, "hall_panels": HALL_PANELS,
                "stair": None, "skip_models": [], "glb_copies": glb_copies, "glb_missing": [],
                "model_class": {"wreck": "wood", "wreck_mast": "wood", "barrow_front": "rock", "longhall": "wood", "fallen_gable": "char", "ring_stones": "rock", "slope_stones": "rock", "crags": "rock",
                                "cliff_faces": "rock", "gully_rock": "rock", "talus": "rock", "sea_stacks": "rock", "palisade": "wood", "logs": "wood"},
                "blob_class": {}, "colliders": True,
                "_frame": "sim (x, y) = (u, -v): the Level node's local frame IS v1's (u, v) -- no site rotation (R-C9-185)"},
    }
    json.dump(level, open(os.path.join(OUT, "level.json"), "w"), indent=1)
    win_sea = sea_area
    layout = {
        "_what": "barrow_v2 ART-FIRST layout of record, PHASE 1'' (Matt R-C9-204/206; plan R-C9-205): sketch A in v1's camera-aligned (u, v) frame; terrain levels, the sketch-A cliff kit, plated ice, pack ice, no paths. Built by fid/lv/tools/make_bv2art.py.",
        "frame": {"units": "metres", "u_hat_world": [0.682, 0.0, -0.7314], "v_hat_world": [-0.7314, 0.0, -0.682], "world_from_uv": "x = u*cos47 - v*sin47; z = -u*sin47 - v*cos47 (v1's own)",
                  "sketch_map": "u = (x - 780) / 24, v = (452 - y - z*24*cos(pitch)) / (24*sin(pitch)), sketch A px (x, y)"},
        "window": {"guide_px": list(GUIDE), "centre_uv": list(win_c), "u": wu, "v": wv, "chunks": {"cols": 5, "rows": 5, "canvas_px": [1536, 1024], "stride_px": [1280, 768]}},
        "tints_srgb": tints, "levels_m": {"plateau": 0.0, "clifftop_crest": [round(float(crest.min()), 2), round(float(crest.max()), 2)], "beach_top": 0.0,
                                          "shore_ice_top": ICE_TOP, "sea": SEA_Z, "sea_floor": SEA_FLOOR, "shelf": R["shelf_z"], "mere_bed": MERE_SHAPE["bed_z"],
                                          "sea_cliff_height_m": [round(float(crest[lip_s.index(next(x for x in lip_s if x >= 8.0)):].min()) - SEA_Z, 2), round(float(crest.max()) - SEA_Z, 2)],
                                          "beach_drop_m": round(-ICE_TOP, 2), "beach_width_m": BEACH_W},
        "regions": {"mere_outline": [[round(q[0], 3), round(q[1], 3)] for q in mere], "stream": [[round(q[0], 3), round(q[1], 3)] for q in STREAM_UV],
                    "shore_chain": [[round(q[0], 3), round(q[1], 3)] for q in shore], "lip_chain": [[round(q[0], 3), round(q[1], 3)] for q in lip],
                    "lip_crest_m": [round(float(x), 3) for x in crest], "mound": {"centre_uv": [round(mc[0], 3), round(mc[1], 3)], "semi_m": list(MOUND["semi_m"]), "rise_m": MOUND["rise_m"]},
                    "hall_yard_ash": [[round(uv(p)[0], 3), round(uv(p)[1], 3)] for p in YARD], "paths": "REMOVED (R-C9-204 (3))",
                    "sea_ice": {"cells_area_m2": round(win_sea, 1), "ice_area_m2": round(ice_area, 1), "ice_fraction": round(ice_area / max(win_sea, 1e-6), 3),
                                "pieces": {z: sum(1 for e in ice if e["zone"] == z) for z in ("fast", "plate", "floe")}, "bobbing_floes": sum(1 for e in ice if e["bob"])},
                    "mere_plates": len(mere_ice), "stream_ice_pieces": len(stream_ice)},
        "placements": layout_pl,
        "procedural": {"palisade_posts": len(post_insts), "logs": len(log_insts), "stair_treads": len(treads), "slab_groups": {k: len(v["items"]) for k, v in slabs.items()}},
        "openings": openings, "knight": level["knight"], "bounds": level["bounds"],
        "kit2": {k: {"glb": kit(k), "standin": kit(k) != KIT2[k]} for k in KIT2},
        "route": {"_what": "R-C9-212/213/214: the walkable route from inside the carved sea cave over the iced landing, up the stair groove cut in the cove's east wall, onto the clifftop (lv_walkability.py checks it)",
                  "spec": {k: (list(v) if isinstance(v, tuple) else v) for k, v in R.items()},
                  "riser_m": round(rise, 5), "riser_range_m": [round(rise * (1 + min(jit)), 4), round(rise * (1 + max(jit)), 4)], "treads": n_tr,
                  "stair_pitch_deg": round(math.degrees(math.atan2(rise, R["tread"])), 3),
                  "frame": {"origin_uv": [round(LIP_A[0], 4), round(LIP_A[1], 4)], "along_uv": [round(dR[0], 6), round(dR[1], 6)], "stair_axis": "inland",
                            "stair_t": [t0s, round(t1s, 4)], "s_foot": s_foot, "s_top": round(s_top, 4), "s_land": round(s_land, 4), "top_z": top_z, "width_m": W_,
                            "landing": {"gully_t": [t0s, round(t1s, 3)], "s": [s_foot, LDc["s_front"]], "mouth_floor_ts": [round(m_c[0], 3), round(m_c[1], 3)], "mouth_r": LDc["mouth_r"]},
                            "_": "t along A -> B, s SEAWARD; R-C9-226: the stair climbs INLAND (toward -s) in the band t in stair_t, from s_foot to s_top, a pad to s_land"},
                  "points_uv": {k: [round(q[0], 3), round(q[1], 3)] for k, q in {
                      "cave_back": fr(R["cave_t"] + cax[0] * 2.0, s_back + cax[1] * 2.0), "cave_mouth": fr(R["cave_t"], s_back),
                      "shelf_mid": fr(m_c[0], m_c[1]),
                      "bottom_landing": fr((t0s + t1s) / 2, s_foot + 2.0), "stair_foot": fr((t0s + t1s) / 2, s_foot - 0.2),
                      "stair_top": fr((t0s + t1s) / 2, s_top - 0.15), "landing": fr((t0s + t1s) / 2, (s_top + s_land) / 2), "clifftop": fr((t0s + t1s) / 2, s_land - 2.5)}.items()},
                  "carve": {k: (list(v) if isinstance(v, tuple) else v) for k, v in CARVE.items()}, "carved_files": carved_files,
                  "ramp": ramp, "plate": plate, "cave": {"width_m": cave_w, "depth_m": dep_c, "mouth_h_cut_m": CARVE["mouth_h_cut"], "floor_z": R["shelf_z"]},
                  "sketch_A": "R-C9-228: cave W, stair E as sketch A draws them -- no cove: the cave an arch worn into the face at the waterline (u %.1f), facing the camera; the stair in a natural gully of the cliff beside it, climbing INLAND (up-screen) between rock columns to the clifftop at u %.1f; a small iced ledge where its foot meets the mouth" % (fr(R["cave_t"], 0)[0], fr((t0s + t1s) / 2, s_top)[0]),
                  "cave_axis_ts": list(cax), "landing": dict(LDc), "cove": dict(CARVE["cove"]), "mere_area_m2": round(mere_area_land, 1)},
        "classes": names, "class_counts": {names[k]: int((C == k).sum()) for k in range(len(names)) if (C == k).any()},
    }
    json.dump(layout, open(os.path.join(ART, "layout_bv2art.json"), "w"), indent=1)
    print("[art pp] window %.1f x %.1f m; %d placements; cliffs %d, talus %d, stacks %d; sea ice %.0f%% (%s, %d bob); mere plates %d; stream ice %d; treads %d; kit %s" % (
        wu[1] - wu[0], wv[1] - wv[0], len(layout_pl), len(cliff_insts), len(talus_insts) + len(shelf_rocks), len(stack_insts), 100 * ice_area / max(win_sea, 1e-6),
        layout["regions"]["sea_ice"]["pieces"], layout["regions"]["sea_ice"]["bobbing_floes"], len(mere_ice), len(stream_ice), len(treads),
        {k: ("kit2" if kit(k) == KIT2[k] else "standin") for k in KIT2}))


if __name__ == "__main__":
    main()
