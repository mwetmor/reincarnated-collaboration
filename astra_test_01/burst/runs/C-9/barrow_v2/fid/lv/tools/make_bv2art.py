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
BARROW = {"glb": "data/bv2f/models/barrow.glb", "door": (818, 150), "width_m": 11.6}
MOUND = {"centre": (830, -10), "semi_m": (15.0, 8.5), "rise_m": 5.5}
RING_STAND = [((690, 455), 2.2, "tall"), ((722, 505), 1.7, "mid"), ((780, 385), 1.9, "tall"), ((862, 420), 2.1, "mid"), ((846, 492), 2.0, "tall")]
RING_LIE = [((742, 425), 25.0), ((805, 512), -15.0), ((830, 535), 60.0)]
SLOPE_STONES = [((600, 40), 2.4, "tall"), ((520, 105), 1.8, "mid"), ((690, 185), 2.0, "mid"), ((925, 180), 2.2, "tall"), ((1110, 125), 2.0, "mid"),
                ((1190, 90), 2.3, "tall"), ((380, 365), 1.4, "short")]     # Phase 1'': #7 (930, 700) stood on the new stair's top -- removed
CRAGS = [((1235, 175), 2.0), ((1500, 360), 2.4)]          # Phase 1'': the coastal crags are replaced by the cliff kit's talus
# THE COAST (uv). SHORE: the plateau's W edge = the beach top (land to its east), north -> south; LIP: the S clifftop edge,
# west -> east, from the beach/cliff junction J. The ROUTE stretch of the lip is ONE straight face (A -> B) the cave, the
# shelf and the stair are laid along; the rest of the lip is pushed into bays and headlands (K.wiggle).
SHORE_UV = [(-25.5, 27.0), (-26.0, 18.0), (-24.5, 11.0), (-19.0, 7.5), (-13.8, 3.6), (-12.6, -1.5), (-14.2, -5.0), (-17.5, -7.0)]
LIP_A, LIP_B = (-12.5, -6.6), (7.95, -19.15)
LIP_UV = [(-17.5, -7.0), (-15.2, -8.9), LIP_A, LIP_B, (11.6, -19.2), (15.4, -21.0), (20.0, -24.7), (24.2, -27.8), (28.3, -30.4), (34.2, -33.8), (40.0, -37.0)]
MERE_SHAPE = {"centre_uv": (-15.6, 14.6), "radii": (9.4, 4.3), "bed_z": -0.18, "plate_top": -0.04, "plate_m": 2.4}
STREAM_UV = [(-5.0, 20.6), (-5.4, 19.4), (-6.6, 17.9), (-8.0, 16.6), (-9.0, 15.8)]
STREAM_SHAPE = {"half_w": 0.8, "bank_w": 0.8, "depth": 0.55, "ice_top_below": 0.33}
YARD = [(1105, 385), (1300, 330), (1525, 470), (1500, 650), (1250, 660), (1140, 545)]
SHRUB = [((470, 330), 70), ((380, 250), 60), ((640, 300), 50), ((600, 455), 45), ((900, 300), 55), ((1000, 470), 60), ((1060, 230), 70),
         ((720, 220), 50), ((1000, 650), 45), ((880, 610), 40), ((470, 60), 60)]
PALISADE = [[(1040, 375), (1110, 340), (1165, 312)], [(1330, 238), (1430, 262), (1530, 300)], [(1150, 560), (1200, 625), (1265, 690), (1420, 702)]]
LOGS = [((1370, 262), (1445, 302)), ((1250, 565), (1330, 622)), ((1300, 625), (1385, 660)), ((1335, 440), (1395, 475))]
# THE ROUTE (R-C9-188/189/206), in the straight-face frame: t along A -> B, s SEAWARD (negative = into the land)
ROUTE = {"crest": 2.5, "shelf_z": SEA_Z + 1.0, "stair_w": 5.5, "risers": 24, "tread": 0.38, "rise_jitter": 0.12,
         "cave_t": 3.5, "cave_front_s": 0.3, "mouth_w": 6.0, "mouth_h": 7.0,
         "shelf_t": (-3.2, 12.0), "shelf_out_s": 8.8, "pilot_t": -3.2, "shelf_in_s": 0.3, "foot_t": 12.0, "bottom_landing_t": 10.0, "landing_len": 2.0,
         "stair_s0": 0.45, "head_z": 5.6, "head_t": (-4.0, 10.0),
         "bounds_out_m": 0.2}
# THE CLIFF KIT (Phase 1'' sheets -> Tripo -> uniform scale). Until a piece exists the nearest Phase 1' build stands in.
KIT2 = {"cliffcol": "data/bv2f/models/cliffcol.glb", "cliffcape": "data/bv2f/models/cliffcape.glb",
        "cavearch": "data/bv2f/models/cavearch.glb", "seastack": "data/bv2f/models/seastack.glb"}
KIT2_STANDIN = {"cliffcol": "data/bv2f/models/cliffplain.glb", "cliffcape": "data/bv2f/models/crag.glb",
                "cavearch": "data/bv2f/models/cliffplain.glb", "seastack": "data/bv2f/models/crag.glb"}
# the cave arch's own mouth, measured on the built piece (fraction of its AABB): fid/lv/tools/lv_kit2_measure.py -> kit2/cave_mouth.json
STACKS_UV = [((-21.5, -15.5), 6.2), ((-3.5, -22.0), 4.6), ((16.5, -29.5), 5.4)]


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
    shore, _ = K.wiggle(SHORE_UV, lambda s: 0.9 * math.sin(s / 5.0 + 0.3) + 0.4 * math.sin(s / 2.3), step=1.0, taper=3.0)
    a_s = sum(math.dist(p, q) for p, q in zip(LIP_UV[:2], LIP_UV[1:3]))
    b_s = a_s + math.dist(LIP_A, LIP_B)
    s_route = (a_s, b_s)
    lip, lip_s = K.wiggle(LIP_UV, lambda s: 1.8 * math.sin(s / 6.0 + 0.7) + 0.9 * math.sin(s / 2.7 + 2.1), step=1.0, taper=3.0,
                          keep=lambda s: min(1.0, max(0.0, max(a_s - 1.0 - s, s - (b_s + 1.0)) / 3.0)))
    shore[-1] = lip[0]
    coast = shore + lip[1:]
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
    rise = (R["crest"] - R["shelf_z"]) / n_r
    n_tr = n_r - 1
    t_foot = R["foot_t"]
    t_top = t_foot + n_tr * R["tread"]
    t_land = t_top + R["landing_len"]
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
    bt = np.clip(d_shore / BW, 0, 1)
    beach_z = ICE_TOP * (bt * bt * (3 - 2 * bt) * 0.35 + bt * 0.65)
    beach = west & (d_shore <= BW)
    Z = np.where(beach, beach_z, Z)
    Z = np.where(west & ~beach, SEA_FLOOR, Z)
    # S: the cliff face (heightfield behind the kit) from the crest to the sea floor within 1.2 m
    Z = np.where(south, Hc - (Hc - SEA_FLOOR) * np.clip(d_lip / 1.2, 0, 1) ** 0.6, Z)
    # N: the barrow mound + forecourt cut, the snow swells
    mc = uv(MOUND["centre"])
    a_, b_ = MOUND["semi_m"]
    rho = np.hypot((U - mc[0]) / a_, (V - mc[1]) / b_)
    dome = MOUND["rise_m"] * np.clip(1 - rho ** 2, 0, None) ** 0.45
    bdc = uv(BARROW["door"])
    fc = (np.abs(U - bdc[0]) < 7.0) & (V < bdc[1] + 1.0)
    dome = np.where(fc, 0.0, dome)
    Z = np.where(land, np.maximum(Z, dome), Z)
    swell = 0.35 * np.sin(U / 6.3 + 1.1) * np.sin(V / 5.1 + 0.4) * np.clip((np.hypot(U, V) - 22.0) / 8.0, 0, 1)
    Z = np.where(land & (dome < 0.05) & (d_lip > 9.0), Z + np.maximum(swell, 0), Z)
    # THE MERE: an organic outline, its bed (dark water) under the plates
    mere = K.blob(MERE_SHAPE["centre_uv"], MERE_SHAPE["radii"], prng, n=64, amp=0.16)
    mere_m = mask(mere, U, V, HF_PPM, u0, v1)
    Z = np.where(mere_m, MERE_SHAPE["plate_top"], Z)       # R-C9-208 (4): one continuous ice surface (cracks and seams are drawn on it)
    # THE STREAM: a shallow channel with snowy banks, barrow -> mere
    stream = K.resample(STREAM_UV, 0.5)
    d_st = dist_to_chain(stream, U, V)
    hw_st, bw_st, dep = STREAM_SHAPE["half_w"], STREAM_SHAPE["bank_w"], STREAM_SHAPE["depth"]
    prof = np.where(d_st < hw_st, 1.0, np.clip(1 - (d_st - hw_st) / bw_st, 0, 1) ** 1.5)
    Z = np.where(land & (d_st < hw_st + bw_st) & ~mere_m, Z - dep * prof, Z)
    Tq = (U - LIP_A[0]) * dR[0] + (V - LIP_A[1]) * dR[1]
    Sq = (U - LIP_A[0]) * nR[0] + (V - LIP_A[1]) * nR[1]
    # the clifftop round the top landing is held at the crest (flush on every side), easing down over 4 m
    dt_ = np.maximum(0.0, np.maximum((t_top - 1.0) - Tq, Tq - (t_land + 2.0)))
    ds_ = np.maximum(0.0, np.maximum((-W_ - 5.0) - Sq, Sq - 0.0))
    wl = np.clip(1.0 - np.hypot(dt_, ds_) / 4.0, 0.0, 1.0)
    Z = np.where(land & (Sq <= 0.0) & (wl > 0.0), np.maximum(Z, R["crest"] * wl * wl * (3 - 2 * wl)), Z)
    # THE ROUTE: the shelf (natural sea-worn rock, irregular outer edge), the cave floor, the stair's notch + bed, the landing
    Tq = (U - LIP_A[0]) * dR[0] + (V - LIP_A[1]) * dR[1]
    Sq = (U - LIP_A[0]) * nR[0] + (V - LIP_A[1]) * nR[1]
    # R-C9-208 (2): the cliff rises into a ROCK HEADLAND round the cave (sketch A's cave sits in a high face): the clifftop at
    # head_z over the cave's stretch, easing back to the crest over 5 m along the face and 8 m inland
    h0, h1 = R["head_t"]
    wt = np.clip(1.0 - np.maximum(0.0, np.maximum(h0 - Tq, Tq - h1)) / 7.0, 0.0, 1.0)
    ws = np.clip(1.0 - np.maximum(0.0, -Sq - 9.0) / 11.0, 0.0, 1.0)
    wh = wt * ws * np.clip((d_shore - 3.0) / 8.0, 0.0, 1.0)              # never up against the W beach
    wh = wh * wh * (3 - 2 * wh)
    Z = np.where(land & (Sq <= 0.0) & (wh > 0.0), np.maximum(Z, R["head_z"] * wh), Z)
    S0 = R["stair_s0"]
    t0_s, t1_s = R["shelf_t"]
    # R-C9-211: a natural sea-worn WAVE-CUT PLATFORM -- lobes and bays (three wavelengths), a ragged broken seaward edge, the
    # west end rounded into the cliff foot, the east end swept round the stair's foot; never a straight edge or a right angle
    # PILOT PIN (R-C9-189/211): the platform west of t = pilot_t projects into the pinned paint-pilot tiles -- there it keeps the
    # M1'' outline point for point; the natural platform is built from pilot_t east (eased in over 1.5 m)
    def shelf_leg(t):
        return 7.6 + 0.45 * math.sin(t * 1.3 + 0.5) + 0.25 * math.sin(t * 3.1)

    def shelf_out(t):
        if t < R["pilot_t"]:
            return shelf_leg(t)
        w = 1.0
        w = w * w * (3 - 2 * w)
        new = R["shelf_out_s"] + 0.95 * math.sin(t * 0.52 + 0.3) + 0.5 * math.sin(t * 1.37 + 1.1) + 0.22 * math.sin(t * 3.3 + 0.2)
        return shelf_leg(t) + (new - shelf_leg(t)) * w
    west_pts = [fr(t, shelf_leg(t)) for t in np.arange(t0_s, t1_s + 0.01, 0.5) if t < R["pilot_t"]]
    east_pts = []
    for t in np.arange(R["pilot_t"], t1_s + 0.01, 0.35):
        j_ = rng209.uniform(-0.15, 0.15)
        east_pts.append(fr(t, shelf_out(t) + j_))
    east = [fr(t1_s + 0.3 + 1.1 * math.sin(a), shelf_out(t1_s) + (S0 + W_ + 0.3 - shelf_out(t1_s)) * (1 - math.cos(a)) / 2) for a in np.linspace(0.2, math.pi - 0.2, 7)]
    west_arc = [fr(t0_s - 1.8 * math.sin(a) + rng209.uniform(-0.15, 0.15), R["shelf_in_s"] + (shelf_out(t0_s) - R["shelf_in_s"]) * (1 - math.cos(a)) / 2)
                for a in np.linspace(0.2, math.pi - 0.25, 8)]
    shelf = [fr(t0_s + 0.4, -1.6)] + west_arc + west_pts + east_pts + east + [fr(t1_s + 0.3, S0), fr(t1_s - 1.0, -1.6)]     # R-C9-212: the whole platform natural (its back runs in under the kit face)
    edge = [q for q in shelf if to_fr(q)[1] > 4.0]     # the seaward rim (rime, boulders, bounds follow it)
    shelf = K.ccw(shelf)
    shelf_m = mask(shelf, U, V, HF_PPM, u0, v1)
    # the sea ice is laid out against the M1'' shelf outline (Matt passed that ice; its partition and every random draw after
    # it stay exactly as they were) -- the new platform covers the ice where it reaches further out
    shelf_legacy = K.ccw([fr(t0_s, R["shelf_in_s"])] + [fr(t, 7.6 + 0.45 * math.sin(t * 1.3 + 0.5) + 0.25 * math.sin(t * 3.1)) for t in np.arange(t0_s, t1_s + 0.01, 0.5)] +
                         [fr(t1_s + 0.3, 7.6 - 1.0), fr(t1_s + 0.3, S0)])
    shelf_ice_m = mask(shelf_legacy, U, V, HF_PPM, u0, v1)
    # its surface: low rock RIBS across the platform (2.6 m wavelength, 4 cm), shallow POTHOLES (3 cm), easing to exactly flat
    # at the cave floor and the stair's foot (no seam); max slope ~7 deg, every step far under v1's 0.10 m
    ribs = 0.04 * np.sin(Tq * 2.4 + 1.3 * np.sin(Sq * 0.7)) * np.cos(Sq * 0.9 + 0.4)
    pot = np.zeros(U.shape)
    pot_c = [(9.6, 2.2), (6.6, 5.6), (8.7, 7.4), (7.6, 1.7), (10.6, 6.8), (-1.4, 5.9), (0.9, 3.0), (-2.4, 2.4)]
    for (pt, ps) in pot_c:
        dd = np.hypot(Tq - pt, Sq - ps)
        pot -= 0.03 * np.clip(np.cos(np.clip(dd / 0.8, 0, 1) * math.pi / 2), 0, 1) ** 2
    ease = np.clip((np.abs(Tq - R["cave_t"]) - (R["mouth_w"] / 2 + 0.5)) / 1.5, 0, 1) * np.clip((t_foot - 0.8 - Tq) / 1.5, 0, 1) * np.clip((Tq - R["pilot_t"] - 0.5) / 1.0, 0, 1)
    Z = np.where(shelf_m, R["shelf_z"] + (ribs + pot) * ease, Z)
    # the cave arch's footprint (its scale from the measured mouth): the floor inside it is the shelf's level, all of it, so no
    # cut wall of the heightfield stands inside the piece's open mouth
    g_cave0 = kit("cavearch")
    cbx, cby, cbz = ab(g_cave0)
    cmeta = json.load(open(os.path.join(LV, "kit2", "cave_mouth.json"))) if os.path.exists(os.path.join(LV, "kit2", "cave_mouth.json")) else None
    csc = R["mouth_h"] / (cmeta["mouth_h_frac"] * cby) if (cmeta and g_cave0 == KIT2["cavearch"]) else (R["crest"] + 2.0 - R["shelf_z"]) / cby
    cw_, cd_ = R["mouth_w"] / 2 + 0.7, min(cbz * csc - 0.4, 5.6)        # the mouth's own passage, not the whole piece
    cave_floor = [fr(R["cave_t"] - cw_, R["cave_front_s"] - cd_), fr(R["cave_t"] + cw_, R["cave_front_s"] - cd_), fr(R["cave_t"] + cw_, R["cave_front_s"] + 0.1),
                  fr(R["cave_t"] - cw_, R["cave_front_s"] + 0.1)]
    Z = np.where(mask(cave_floor, U, V, HF_PPM, u0, v1), R["shelf_z"], Z)

    def nosing_z(t):
        return R["shelf_z"] + (t - (t_foot - R["tread"])) * rise / R["tread"]
    # R-C9-208 (1): the flight climbs ACROSS the face, built out against it (sketch A): the strip s in [S0, S0 + W] seaward of
    # the lip, the cliff wall behind it, open to the sea in front
    in_w = (Sq >= S0) & (Sq <= S0 + W_)
    bed = np.maximum(R["shelf_z"], nosing_z(Tq) - rise - 0.05)
    Z = np.where(in_w & (Tq >= t_foot) & (Tq <= t_top), bed, Z)
    Z = np.where((Sq >= -0.7) & (Sq <= S0 + W_) & (Tq > t_top) & (Tq <= t_land), R["crest"] - 0.05, Z)    # the landing's bed (its walk surface is a plate)
    sea_side = (Sq > S0 + W_) & (Sq < S0 + W_ + 1.6) & (Tq >= t_foot - 0.5) & (Tq <= t_land)
    Z = np.where(sea_side, np.minimum(Z, SEA_FLOOR), Z)        # a sheer drop (hidden): the flight's own rock side ribbon is the face
    # THE WRECK'S CRADLE (P6' 761a48353): the hull lies heeled and half-sunk in the SHORE ICE, never in the beach -- under its
    # footprint (+1 m) the ground is the shore ice, easing back up to the beach over 2.5 m (no beach terrain clips the hull)
    wpa, wpb = WRECK["prow_uv"], WRECK["stern_uv"]
    wax = unit(wpb[0] - wpa[0], wpb[1] - wpa[1])
    wcn = ((wpa[0] + wpb[0]) / 2, (wpa[1] + wpb[1]) / 2)
    wl_ = (U - wcn[0]) * wax[0] + (V - wcn[1]) * wax[1]
    wd_ = (U - wcn[0]) * -wax[1] + (V - wcn[1]) * wax[0]
    half_l, half_b = WRECK["len_m"] / 2 + 1.0, ab(WRECK["glb"])[2] * (WRECK["len_m"] / ab(WRECK["glb"])[0]) / 2 + 1.0
    dout = np.hypot(np.maximum(0.0, np.abs(wl_) - half_l), np.maximum(0.0, np.abs(wd_) - half_b))
    cw_r = np.clip(1.0 - dout / 2.5, 0.0, 1.0)
    cw_r = cw_r * cw_r * (3 - 2 * cw_r)
    cradle = (cw_r > 0.0) & ~land & (Z > ICE_TOP - 0.03)
    Z = np.where(cradle, Z + (ICE_TOP - 0.03 - Z) * cw_r, Z)
    cradle_ice = (cw_r >= 0.999) & ~land
    # ---------------- the SEA ICE (R-C9-204 (4)): shore-fast ice, large plates, floes of every size ----------------
    solid = land | beach | shelf_ice_m
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
    cw_a = np.array(cw)
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
            g = prng.uniform(0.12, 0.4) + 0.03 * max(0.0, d - 6.0) + (prng.uniform(0.6, 1.6) if ld else 0.0)
            top = ICE_TOP + prng.uniform(-0.08, 0.25)
        else:
            if prng.random() < min(0.65, 0.25 + 0.03 * max(0.0, d - 11.0)):
                continue                                   # open water between the floes, more of it further out
            g = prng.uniform(0.15, 0.6) * math.sqrt(max(K.area(raw), 0.5)) * 0.35 + (prng.uniform(0.3, 0.9) if ld else 0.0)
            top = ICE_TOP + prng.uniform(-0.14, 0.12)
        poly = K.inset(raw, g)
        if len(poly) < 3:
            continue
        poly = K.ccw(K.roughen(poly, prng, 0.1 if zn != "fast" else 0.06, 0.8))
        if K.area(poly) < 0.12:
            continue
        bob = zn == "floe" and d > 15.0 and prng.random() < 0.45
        ice.append({"zone": zn, "poly": [[round(q[0], 3), round(q[1], 3)] for q in poly], "top": round(top, 3), "bob": bob})
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
                    ridges.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(blk)], "z0": round(SEA_Z - 0.2, 3), "z1": round(top + prng.uniform(0.15, 0.8), 3)})
    # BRASH: small broken ice in the leads beside the plates
    ice_r = np.zeros(U.shape, bool)
    for e in ice:
        ice_r |= mask([tuple(q) for q in e["poly"]], U, V, HF_PPM, u0, v1)
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
    mseeds = K.jitter_seeds(mbox, MERE_SHAPE["plate_m"], prng, lambda p: K.point_in_poly(p, mere))
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
            if prng.random() < 0.18:
                continue
            mid_ = ((q0[0] + q1[0]) / 2 + prng.uniform(-0.25, 0.25), (q0[1] + q1[1]) / 2 + prng.uniform(-0.25, 0.25))
            for e0, e1 in ((q0, mid_), (mid_, q1)):
                L_ = math.dist(e0, e1)
                if L_ < 0.05:
                    continue
                nn = (-(e1[1] - e0[1]) / L_, (e1[0] - e0[0]) / L_)
                seam = prng.random() < 0.12
                w_ = prng.uniform(0.1, 0.18) if seam else prng.uniform(0.03, 0.07)
                poly = [(e0[0] - nn[0] * w_ / 2, e0[1] - nn[1] * w_ / 2), (e1[0] - nn[0] * w_ / 2, e1[1] - nn[1] * w_ / 2), (e1[0] + nn[0] * w_ / 2, e1[1] + nn[1] * w_ / 2), (e0[0] + nn[0] * w_ / 2, e0[1] + nn[1] * w_ / 2)]
                (mere_seams if seam else mere_cracks).append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in poly],
                    "z0": MERE_SHAPE["plate_top"] - 0.02, "z1": MERE_SHAPE["plate_top"] + (prng.uniform(0.02, 0.05) if seam else 0.008)})
    # the sheet itself: the cells laid edge to edge (no gaps; convex pieces triangulate cleanly) -- one continuous ice surface
    stream_ice = []
    acc = 0.0
    sl = K.resample(STREAM_UV, 0.25)
    i = 0
    while i < len(sl) - 2:
        n_ = prng.randint(4, 9)
        j = min(i + n_, len(sl) - 1)
        a, b = sl[i], sl[j]
        d_ = unit(b[0] - a[0], b[1] - a[1])
        nn = (-d_[1], d_[0])
        hw_i = hw_st * prng.uniform(0.7, 0.95)
        g = 0.02                                           # R-C9-208 (4): thin cracks between the stream's ice pieces
        a2 = (a[0] + d_[0] * g, a[1] + d_[1] * g)
        b2 = (b[0] - d_[0] * g, b[1] - d_[1] * g)
        poly = [(a2[0] + nn[0] * hw_i, a2[1] + nn[1] * hw_i), (b2[0] + nn[0] * hw_i, b2[1] + nn[1] * hw_i),
                (b2[0] - nn[0] * hw_i, b2[1] - nn[1] * hw_i), (a2[0] - nn[0] * hw_i, a2[1] - nn[1] * hw_i)]
        poly = K.roughen(poly, prng, 0.05, 0.4)
        zc = float(Z[min(max(int(round((v1 - (a[1] + b[1]) / 2) * HF_PPM)), 0), H - 1), min(max(int(round(((a[0] + b[0]) / 2 - u0) * HF_PPM)), 0), W - 1)])
        stream_ice.append({"zone": "stream", "poly": [[round(q[0], 3), round(q[1], 3)] for q in poly], "top": round(zc + dep - STREAM_SHAPE["ice_top_below"], 3), "bob": False})
        i = j
    Z = Z.astype("<f4")
    Z.tofile(os.path.join(OUT, "terrain_h.f32"))
    # ---- classes at CLS_PPM ----
    names = ["none", "snow", "path", "ice", "shrub", "rock", "mound", "shingle", "shore_ice", "stream", "char", "sea", "wood", "passage_dark", "ash"]
    Wc = int((u1 - u0) * CLS_PPM)
    Hc_ = int((v1 - v0) * CLS_PPM)
    Uc, Vc = np.meshgrid(u0 + (np.arange(Wc) + 0.5) / CLS_PPM, v1 - (np.arange(Hc_) + 0.5) / CLS_PPM)
    fi = np.clip(((Uc - u0) * HF_PPM).astype(int), 0, W - 1)
    fj = np.clip(((v1 - Vc) * HF_PPM).astype(int), 0, H - 1)
    Zc = Z[fj, fi]
    landc = mask(land_poly, Uc, Vc, CLS_PPM, u0, v1)
    beachc = beach[fj, fi]
    C = np.full(Uc.shape, names.index("snow"), np.uint8)
    rhoc = np.hypot((Uc - mc[0]) / a_, (Vc - mc[1]) / b_)
    C[landc & (rhoc < 1.0)] = names.index("mound")
    for (p, r) in SHRUB:
        c = uv(p)
        rr = r / S
        n_ = 0.35 * np.sin(Uc * 1.7 + p[0]) * np.sin(Vc * 1.3 + p[1])
        C[landc & (np.hypot(Uc - c[0], Vc - c[1]) < rr * (1 + n_))] = names.index("shrub")
    C[beachc & ~landc] = names.index("shingle")
    C[cradle_ice[fj, fi] & ~landc] = names.index("shore_ice")             # the wreck's cradle: shore ice, not beach
    C[mask([uv(p) for p in YARD], Uc, Vc, CLS_PPM, u0, v1)] = names.index("ash")
    C[mask(mere, Uc, Vc, CLS_PPM, u0, v1)] = names.index("ice")          # the mere's continuous ice (its thin cracks are drawn on it)
    dstc = dist_to_chain(stream, Uc, Vc)
    C[landc & (dstc < hw_st + 0.1)] = names.index("sea")                  # the stream's dark water under its ice
    C[landc & (dstc >= hw_st + 0.1) & (dstc < hw_st + bw_st)] = names.index("snow")   # its snowy banks
    southc = ~landc & ~beachc
    C[southc & (Zc > ICE_TOP + 0.05)] = names.index("rock")
    dlc = dist_to_chain(lip, Uc, Vc)
    C[southc & (dlc < 1.6)] = names.index("none")                         # the raw heightfield face is not drawn: the cliff skirt + the kit are the face
    C[mask(shelf, Uc, Vc, CLS_PPM, u0, v1)] = names.index("rock")
    C[mask(cave_floor, Uc, Vc, CLS_PPM, u0, v1)] = names.index("rock")
    cave_dark = [fr(R["cave_t"] - 2.2, R["cave_front_s"] - 5.5), fr(R["cave_t"] + 2.2, R["cave_front_s"] - 5.5), fr(R["cave_t"] + 2.2, R["cave_front_s"] - 1.5), fr(R["cave_t"] - 2.2, R["cave_front_s"] - 1.5)]
    C[mask(cave_dark, Uc, Vc, CLS_PPM, u0, v1)] = names.index("passage_dark")      # R-C9-206: the floor deep inside reads dark -- the mouth recedes into darkness
    Tc = (Uc - LIP_A[0]) * dR[0] + (Vc - LIP_A[1]) * dR[1]
    Sc = (Uc - LIP_A[0]) * nR[0] + (Vc - LIP_A[1]) * nR[1]
    C[(Sc >= S0) & (Sc <= S0 + W_) & (Tc >= t_foot - 0.3) & (Tc <= t_land)] = names.index("rock")
    # the route's cut walls (the notch, the cave's sides) stand inside the kit: their heightfield cells are not drawn
    gzy, gzx = np.gradient(Zc, 1.0 / CLS_PPM)
    steep = ndimage.binary_dilation(np.hypot(gzx, gzy) > 2.5, iterations=2)       # true faces (and the cells at their foot and lip)
    cave_zone = ndimage.binary_dilation(mask(cave_floor, Uc, Vc, CLS_PPM, u0, v1), iterations=6)
    zone_r = ((Tc >= R["shelf_t"][0] - 4.0) & (Tc <= t_land + 3.0) & (Sc >= -0.6) & (Sc <= S0 + W_ + 2.5)) | (dlc < 2.5) | cave_zone
    # R-C9-208 (5): no raw heightfield face anywhere on the coast (its 25 cm cells read as vertical slats): the skirt and the kit are the face
    C[steep & zone_r] = names.index("none")
    C[(Zc <= ICE_TOP) & ~beachc] = names.index("none")                    # sea / under the ice: the sea plane and the ice draw it
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
    # -- the barrow front (N): its door threshold at the sketch's door, facing the camera
    bd = uv(BARROW["door"])
    sb = BARROW["width_m"] / ab(BARROW["glb"])[0]
    cb = (bd[0], bd[1] + 8.2 * sb)
    bins = model("barrow_front", "rock", BARROW["glb"], cb, (0.0, -1.0), sb, z=0.0, note="the monumental carved door; door %.2f x %.2f m" % (5.81 * sb * 25.8 / ab(BARROW["glb"])[0], 6.67 * sb * 25.8 / ab(BARROW["glb"])[0]))
    models.append({"id": "barrow_front", "kind": "barrow", "pos": bins["pos"], "z": 0.0, "godot_rot_y_deg": bins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": bins["size_m"][0], "d_local_z": bins["size_m"][1], "h": bins["size_m"][2]}, "glb": bins["glb"]})
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
    for i, (p, ht, kind_) in enumerate(SLOPE_STONES):
        g = V1M + "stone_%s.glb" % kind_
        c = uv(p)
        rot = (math.sin(i * 1.9 + 1), -abs(math.cos(i * 1.9 + 1)) - 0.2)
        slope_insts.append(model("slope_stone_%d" % i, "rock", g, c, unit(*rot), ht / ab(g)[1], z=hz_min(c, 0.6) - 0.1))
    group("slope_stones", "stones", slope_insts)
    for i, (p, ht, kind_) in enumerate(RING_STAND):
        g = V1M + "stone_%s.glb" % kind_
        c = uv(p)
        rot = (math.sin(i * 2.3), -abs(math.cos(i * 2.3)) - 0.2)
        stone_insts.append(model("stone_%d" % i, "rock", g, c, unit(*rot), ht / ab(g)[1], z=hz_min(c, 0.6) - 0.1))
    for i, (p, deg) in enumerate(RING_LIE):
        g = V1M + "stone_tall.glb"
        c = uv(p)
        a = math.radians(deg)
        stone_insts.append(model("fallen_stone_%d" % i, "rock", g, c, (math.sin(a), -math.cos(a)), 1.4 / ab(g)[1], z=hz_min(c, 0.5) - 0.15, lie=True,
                                 note="P6' 761a48353: seated on the terrain surface (top ~0.12 m proud of the ground)"))
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
    route_lo, route_hi = a_s + R["shelf_t"][0] - 1.0, a_s + t_land + 1.0
    s = 2.0
    k = 0
    while s < lip_s[-1] - 1.0:
        p, d, n = lip_at(s)
        if route_lo - 4.0 < s < route_hi + 4.0 and to_fr(p)[0] > R["shelf_t"][0] - 3.0 and to_fr(p)[0] < t_land + 3.0:
            s += 1.0
            continue
        cape = turn(s) < -12.0
        g = g_cape if cape else g_col
        bx, by, bz = ab(g)
        top = float(np.interp(s, lip_s, crest)) + 1.0 + 0.3 * math.sin(k * 2.1)          # the columns stand ~1 m proud of the snow
        sc = (top - foot_z) / by
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
        s += bx * sc * 0.62
        k += 1
    # -- the route's own rock: the CAVE ARCH (its mouth 7 m clear), the face under the stair (kept below the treads)
    cave_meta = json.load(open(os.path.join(LV, "kit2", "cave_mouth.json"))) if os.path.exists(os.path.join(LV, "kit2", "cave_mouth.json")) else None
    bx, by, bz = ab(g_cave)
    if cave_meta and g_cave == KIT2["cavearch"]:
        sc_cave = R["mouth_h"] / (cave_meta["mouth_h_frac"] * by)
        mouth_floor_frac = cave_meta.get("floor_frac", 0.0)
    else:
        sc_cave = (R["crest"] + 2.0 - R["shelf_z"]) / by
        mouth_floor_frac = 0.0
    dep_c = bz * sc_cave
    cc = fr(R["cave_t"], R["cave_front_s"] - dep_c / 2)
    cave_z = R["shelf_z"] - mouth_floor_frac * by * sc_cave
    cave_ins = model("cave_arch", "rock", g_cave, cc, nR, sc_cave, z=cave_z, piece="cavearch", collider="trimesh_walls",
                     note="kit2 cave arch: mouth %.1f m clear over the shelf" % R["mouth_h"])
    cliff_insts.append(cave_ins)
    cave_w = bx * sc_cave
    # the HEADLAND's face either side of the cave (base on the shelf / the sea, top 0.9 m over the headland's snow), and the
    # face from the cave's east cheek to the stair's foot
    head_top = R["head_z"] + 0.9
    for t_c, name, zb in ((R["cave_t"] - cave_w / 2 - 3.6, "w", foot_z), ((R["cave_t"] + cave_w / 2 + t_foot) / 2 + 0.6, "e", R["shelf_z"] - 0.2)):
        sc = (head_top - zb) / ab(g_col)[1]
        dep = ab(g_col)[2] * sc
        cliff_insts.append(model("cliff_route_%s" % name, "rock", g_col, fr(t_c, R["shelf_in_s"] + 0.3 - dep / 2), nR, sc, z=zb, piece="cliffcol", collider="trimesh",
                                 note="the headland's face beside the cave"))
    # R-C9-212 (2): THE HEADLAND'S FACE behind the shelf, all rock kit -- columns and capes (buttresses) of varied height,
    # their fronts stepped out and back (recesses), each topped 0.9 m over the ground behind it; the cave's mouth left open
    t = R["shelf_t"][0] - 9.0
    k2 = 0
    while t < R["bottom_landing_t"] + 1.0:
        if abs(t - R["cave_t"]) < cave_w / 2 + 1.5:
            t = R["cave_t"] + cave_w / 2 + 1.5
            continue
        cape = k2 % 3 == 1
        g = g_cape if cape else g_col
        zb = R["shelf_z"] - 0.3 if t > R["shelf_t"][0] - 1.0 else foot_z
        back = max(hz(fr(t, -1.5)), hz(fr(t + 1.5, -1.5)), hz(fr(t - 1.5, -1.5)))
        sc = (back + 0.9 + 0.4 * math.sin(k2 * 1.7) - zb) / ab(g)[1]
        wdt = ab(g)[0] * sc
        dep = ab(g)[2] * sc
        out = R["shelf_in_s"] + (0.5 if cape else 0.15) + 0.25 * math.sin(k2 * 2.3) - dep / 2
        yaw = (nR[0] * math.cos(0.12 * math.sin(k2 * 1.3)) - nR[1] * math.sin(0.12 * math.sin(k2 * 1.3)),
               nR[0] * math.sin(0.12 * math.sin(k2 * 1.3)) + nR[1] * math.cos(0.12 * math.sin(k2 * 1.3)))
        tc = min(t + wdt / 2, R["cave_t"] - cave_w / 2 - 1.0 + wdt / 2) if t < R["cave_t"] else t + wdt / 2
        cliff_insts.append(model("cliff_head_%d" % k2, "rock", g, fr(tc, out), yaw, sc, z=zb, piece="cliffcape" if cape else "cliffcol", collider="trimesh",
                                 note="R-C9-212: the headland's face, rock kit"))
        t += wdt * 0.55
        k2 += 1
    # the CLIFF WALL BEHIND THE STAIR (R-C9-208 (1)): kit columns along the face, their fronts on the flight's inner edge, each
    # standing on the tread height at its own west end, their tops 0.9 m over the clifftop; they stop short of the landing
    t = t_foot + 0.6
    while t < t_top - 1.0:
        zb = max(R["shelf_z"], nosing_z(t) - rise) - 0.25
        top_here = R["crest"] + (R["head_z"] - R["crest"]) * max(0.0, min(1.0, 1.0 - (t - R["head_t"][1]) / 5.0)) + 0.9
        sc = (top_here - zb) / ab(g_col)[1]
        wdt = ab(g_col)[0] * sc
        if t + wdt > t_top - 0.6:
            sc *= max(0.1, (t_top - 0.6 - t) / wdt)
            wdt = ab(g_col)[0] * sc
            if sc < 0.18:
                break
        dep = ab(g_col)[2] * sc
        cliff_insts.append(model("cliff_wall_%d" % int(t * 10), "rock", g_col, fr(t + wdt / 2, S0 + 0.05 - dep / 2), nR, sc, z=zb, piece="cliffcol", collider="trimesh",
                                 note="the cliff wall behind the stair"))
        t += wdt * 0.78
    # the rock UNDER the flight's open sea side: kit columns whose tops stay 0.3 m below the treads above them (open to the sea)
    t = t_foot + 0.3
    while t < t_top - 0.5:
        zt = max(R["shelf_z"], nosing_z(t) - rise) - 0.3
        sc = max(0.2, (zt - foot_z) / ab(g_col)[1])
        wdt = ab(g_col)[0] * sc
        if t + wdt > t_top + 0.5:
            break
        if zt - foot_z > 0.8:
            dep = ab(g_col)[2] * sc
            cliff_insts.append(model("cliff_under_stair_%d" % int(t * 10), "rock", g_col, fr(t + wdt / 2, S0 + W_ + 0.9 - dep / 2), nR, sc, z=foot_z, piece="cliffcol", collider="trimesh"))
        t += max(wdt * 0.8, 1.0)
    # -- the SHELF's few boulders and ice rime (R-C9-206 (c)): boulders at its outer edge and the west end, rime as ice
    shelf_rocks = []
    for (t_b, s_b, ht) in ((-2.6, None, 1.2), (0.6, None, 0.9), (5.8, None, 1.4), (9.2, None, 1.0), (-3.6, 1.6, 1.6), (11.4, None, 0.8)):
        s_b = s_b if s_b is not None else shelf_out(t_b) - 0.3
        q = fr(t_b, s_b)
        a = prng.uniform(0, 2 * math.pi)
        shelf_rocks.append(model("shelf_rock_%d" % len(shelf_rocks), "rock", g_stk, q, (math.sin(a), math.cos(a)), ht / ab(g_stk)[1], z=R["shelf_z"] - 0.25 * ht, piece="seastack", collider="box"))
    for (t_b, s_b, ht) in ((7.6, None, 0.9), (8.6, 0.35, 1.3), (5.2, None, 0.8), (10.4, 0.5, 0.9)):
        s_b = s_b if s_b is not None else shelf_out(t_b) - 0.3
        q = fr(t_b, s_b)
        a = rng209.uniform(0, 2 * math.pi)
        shelf_rocks.append(model("shelf_rock_%d" % len(shelf_rocks), "rock", g_stk, q, (math.sin(a), math.cos(a)), ht / ab(g_stk)[1], z=R["shelf_z"] - 0.25 * ht, piece="seastack", collider="box"))
    rime = []

    def rime_seg(e0, e1, w0):
        dd = unit(e1[0] - e0[0], e1[1] - e0[1])
        nn = (dd[1], -dd[0])
        rime.append({"zone": "rime", "poly": [[round(e0[0] - nn[0] * w0, 3), round(e0[1] - nn[1] * w0, 3)], [round(e1[0] - nn[0] * w0, 3), round(e1[1] - nn[1] * w0, 3)],
                                              [round(e1[0] + nn[0] * 0.05, 3), round(e1[1] + nn[1] * 0.05, 3)], [round(e0[0] + nn[0] * 0.05, 3), round(e0[1] + nn[1] * 0.05, 3)]],
                     "top": round(R["shelf_z"] + 0.04, 3), "bob": False})
    leg_edge = [fr(t, shelf_leg(t)) for t in np.arange(t0_s, t1_s + 0.01, 0.5)]
    for e0, e1 in zip(leg_edge[:-1], leg_edge[1:]):       # the M1'' rime, its draws in their M1'' order; kept west of the pilot line
        w0 = prng.uniform(0.15, 0.45)
        if to_fr(e1)[0] <= R["pilot_t"]:
            rime_seg(e0, e1, w0)
    for e0, e1 in zip(east_pts[:-1], east_pts[1:]):
        rime_seg(e0, e1, rng209.uniform(0.15, 0.45))
    # -- the ROCK STACKS in the ice
    stack_insts = []
    for i, (p, ht) in enumerate(STACKS_UV):
        a = 0.7 + i * 2.1
        stack_insts.append(model("stack_%d" % i, "rock", g_stk, p, (math.sin(a), math.cos(a)), (ht + 0.5) / ab(g_stk)[1], z=SEA_Z - 0.5, piece="seastack", collider="trimesh"))
    group("cliff_faces", "cliff", cliff_insts)
    group("talus", "talus", talus_insts + shelf_rocks)
    group("sea_stacks", "stack", stack_insts)
    mouth_c = fr(R["cave_t"], R["cave_front_s"])
    openings.append({"id": "sea_cave_mouth", "point": "S", "model": "cave_arch", "centre_sim": [round(mouth_c[0], 4), round(-mouth_c[1], 4)], "z0": R["shelf_z"],
                     "w": R["mouth_w"], "h": R["mouth_h"], "faces_deg": round(math.degrees(math.atan2(nR[0], nR[1])) % 360, 3),
                     "curtain_inset_m": 2.6, "curtain_w": 8.0, "curtain_h": 8.5, "dark": True,
                     "_": "R-C9-206/208: the kit piece's own eroded arch with its modelled depth; a dark plane 2.6 m INSIDE it, larger than the passage there, so the arch's own rock frames it -- the mouth reads as a dark eroded arch, never a black rectangle on the face"})
    # -- the ROCK-CUT STAIR (R-C9-206 (b)): individual rough treads, each a block of its own size, cut into the notch; their
    # nosings ON one plane (the walk ramp); risers uneven (+-12 %) with the tread depths moved in step, so the slope holds
    jit = [prng.uniform(-R["rise_jitter"], R["rise_jitter"]) for _ in range(n_r)]
    mj = sum(jit) / n_r
    jit = [j - mj for j in jit]
    treads, snow_lips = [], []
    tt = t_foot
    zz = R["shelf_z"]
    for i in range(n_tr):
        dz = rise * (1 + jit[i])
        zz += dz
        t_a, t_b = tt, tt + R["tread"] * (1 + jit[i + 1])
        # R-C9-209 (Matt): ROUGH NATURAL STEPS -- each riser row broken into 3-5 boulder steps of their own footprint and height,
        # their fronts staggered (no continuous tread line across the width), corners rounded and edges chipped, a few split by
        # a crack; snow on their back edges. The walk surface stays the ramp through the mean nosings.
        nb = rng209.choice((3, 4, 4, 5))
        cuts = sorted([S0] + [S0 + W_ * (k + rng209.uniform(-0.3, 0.3)) / nb for k in range(1, nb)] + [S0 + W_ + rng209.uniform(-0.2, 0.3)])
        for k in range(nb):
            sa, sb = cuts[k] + rng209.uniform(0.04, 0.12), cuts[k + 1] - rng209.uniform(0.04, 0.12)
            if sb - sa < 0.35:
                continue
            zt = zz + rng209.uniform(-0.07, 0.06)
            ta2 = t_a + rng209.uniform(-0.09, 0.07)
            tb2 = t_b + rng209.uniform(-0.05, 0.12)
            ch = min(0.12, (tb2 - ta2) * 0.3)
            rect = [fr(ta2 + ch, sa), fr(tb2 - ch, sa), fr(tb2, sa + ch * 1.4), fr(tb2, sb - ch * 1.4), fr(tb2 - ch, sb), fr(ta2 + ch, sb), fr(ta2, sb - ch * 1.4), fr(ta2, sa + ch * 1.4)]
            pieces = [rect]
            if rng209.random() < 0.18 and sb - sa > 1.0:     # a crack splits this boulder in two
                sm = (sa + sb) / 2 + rng209.uniform(-0.2, 0.2)
                pieces = [[fr(ta2, sa + 0.05), fr(tb2, sa + 0.05), fr(tb2, sm - 0.04), fr(ta2, sm + 0.04)],
                          [fr(ta2, sm + 0.1), fr(tb2, sm + 0.02), fr(tb2, sb - 0.05), fr(ta2, sb - 0.05)]]
            for pc in pieces:
                pc = K.ccw(K.roughen(pc, rng209, 0.03, 0.25))
                treads.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in pc], "z0": round(zt - rise - 0.5, 3), "z1": round(zt + rng209.uniform(-0.02, 0.02), 3)})
            sw_ = rng209.uniform(0.06, 0.14)
            snow_lips.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw([fr(tb2 - 0.02 - sw_, sa + 0.1), fr(tb2 - 0.02, sa + 0.1), fr(tb2 - 0.02, sb - 0.15), fr(tb2 - 0.02 - sw_ * 0.6, sb - 0.15)])],
                              "z0": round(zt - 0.02, 3), "z1": round(zt + rng209.uniform(0.03, 0.06), 3)})
        tt = t_b
    # ROCK SPURS and BOULDERS along both sides of the flight (R-C9-209): on the sea side spurs rising from the sea to just over
    # the step line (outside the 5 m clear line), on the wall side boulders heaped against the cliff
    stair_rocks = []
    tq = t_foot + 0.2
    while tq < t_top - 0.3:
        for side in (0, 1):
            if rng209.random() < 0.55:
                zst = max(R["shelf_z"], nosing_z(tq) - rise)
                r_ = rng209.uniform(0.35, 0.75)
                if side:
                    cs_ = S0 + W_ + r_ * 0.8 + rng209.uniform(0.0, 0.2)
                    z0_, z1_ = SEA_Z - 0.5, zst + rng209.uniform(0.15, 0.55)
                else:
                    cs_ = S0 - r_ * 0.5 + rng209.uniform(-0.1, 0.05)
                    z0_, z1_ = zst - 0.3, zst + rng209.uniform(0.3, 0.8)
                ct = tq + rng209.uniform(-0.2, 0.2)
                pg = [fr(ct + r_ * math.cos(a_) * rng209.uniform(0.7, 1.1), cs_ + r_ * math.sin(a_) * rng209.uniform(0.6, 1.0)) for a_ in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
                stair_rocks.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(pg)], "z0": round(z0_, 3), "z1": round(z1_, 3)})
        tq += rng209.uniform(0.5, 1.1)
    # the shelf's low rock RIBS and frozen POTHOLES, drawn (the walk surface is the terrain under them)
    shelf_marks, shelf_pools = [], []
    for (pt, ps) in pot_c:
        if not (R["pilot_t"] + 0.5 < pt < t1_s and ps < shelf_out(pt) - 0.6):
            continue
        r_ = rng209.uniform(0.45, 0.75)
        pg = [fr(pt + r_ * math.cos(a_) * rng209.uniform(0.8, 1.1), ps + r_ * math.sin(a_) * rng209.uniform(0.6, 0.95)) for a_ in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
        shelf_pools.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(pg)], "z0": round(R["shelf_z"] - 0.1, 3), "z1": round(R["shelf_z"] - 0.01, 3)})
    # low rock RIBS as rubble lines of lumpy stones (not strips), and loose rubble at the cliff foot
    for k in range(16):
        pt = rng209.uniform(R["shelf_t"][0] + 0.5, t_foot - 1.5)
        if abs(pt - R["cave_t"]) < R["mouth_w"] / 2 + 0.6:
            continue
        s0_, s1_ = rng209.uniform(0.8, 2.5), min(shelf_out(pt) - 0.3, rng209.uniform(4.0, 7.5))
        dt_ = rng209.uniform(-0.8, 0.8)
        n_st = max(3, int((s1_ - s0_) / 0.45))
        for j in range(n_st):
            f = j / max(1, n_st - 1)
            ct = pt + dt_ * f + 0.25 * math.sin(f * 5 + k)
            cs_ = s0_ + (s1_ - s0_) * f
            r_ = rng209.uniform(0.16, 0.34)
            pg = [fr(ct + r_ * math.cos(a_) * rng209.uniform(0.7, 1.2), cs_ + r_ * math.sin(a_) * rng209.uniform(0.7, 1.2)) for a_ in np.linspace(0, 2 * math.pi, 7, endpoint=False)]
            shelf_marks.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(pg)], "z0": round(R["shelf_z"] - 0.05, 3), "z1": round(R["shelf_z"] + rng209.uniform(0.05, 0.12), 3)})
    tq = R["shelf_t"][0] - 1.0
    while tq < R["bottom_landing_t"]:
        if abs(tq - R["cave_t"]) > R["mouth_w"] / 2 + 0.3 and rng209.random() < 0.7:
            r_ = rng209.uniform(0.25, 0.55)
            cs_ = R["shelf_in_s"] + rng209.uniform(0.1, 0.7)
            pg = [fr(tq + r_ * math.cos(a_) * rng209.uniform(0.7, 1.2), cs_ + r_ * math.sin(a_) * rng209.uniform(0.6, 1.0)) for a_ in np.linspace(0, 2 * math.pi, 7, endpoint=False)]
            shelf_marks.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw(pg)], "z0": round(R["shelf_z"] - 0.05, 3), "z1": round(R["shelf_z"] + rng209.uniform(0.15, 0.45), 3)})
        tq += rng209.uniform(0.5, 1.0)
    # the flight's sea-side face: a rough rock skirt from the sea to just under each tread (the columns stand in front of it)
    stair_side = []
    tq = t_foot - 0.3
    while tq < t_top:
        t2 = min(t_top, tq + 0.6)
        zt = max(R["shelf_z"], nosing_z(tq) - rise) - 0.2
        so = S0 + W_ + rng209.uniform(-0.1, 0.1)
        stair_side.append({"poly": [[round(q[0], 3), round(q[1], 3)] for q in K.ccw([fr(tq, so - 0.35), fr(t2, so - 0.35), fr(t2, so + 0.1), fr(tq, so + 0.1)])],
                           "z0": round(SEA_Z - 0.6, 3), "z1": round(zt, 3)})
        tq = t2
    # the walk surface: one plane through the nosings, the shelf one tread out from the foot -> the landing edge
    t_lo, t_hi = t_foot - R["tread"], t_top
    run_h = t_hi - t_lo
    rc = fr((t_lo + t_hi) / 2, S0 + W_ / 2)
    theta = math.atan2(R["crest"] - R["shelf_z"], run_h)
    dn = (-dR[0], -dR[1])                                  # local +Z downhill = toward the foot (west)
    ramp = {"id": "stair_ramp", "c_sim": [round(rc[0], 4), round(-rc[1], 4)], "z_c": round((R["crest"] + R["shelf_z"]) / 2, 4), "across": W_,
            "along_h": round(run_h, 4), "along": round(math.hypot(run_h, R["crest"] - R["shelf_z"]), 4), "thick": 0.3, "yaw_deg": round(yaw_of(dn), 4),
            "pitch_deg": round(math.degrees(theta), 4), "dir_sim": [round(dn[0], 6), round(-dn[1], 6)],
            "_": "a plane through every nosing: the crest at the landing edge, the shelf one tread out from the foot; local +Z downhill"}
    lc = fr((t_top + t_land) / 2, (S0 + W_ - 0.8) / 2)
    plate = {"id": "landing_plate", "c_sim": [round(lc[0], 4), round(-lc[1], 4)], "z_c": R["crest"], "across": S0 + W_ + 0.8, "along_h": round(t_land - t_top, 4),
             "along": round(t_land - t_top, 4), "thick": 0.3, "yaw_deg": round(yaw_of(dn), 4), "pitch_deg": 0.0, "dir_sim": [round(dn[0], 6), round(-dn[1], 6)],
             "_": "the top landing's walk surface: a plate at the crest meeting the ramp's top edge (the terrain under it 5 cm lower)"}
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
             "mere_plates": {"class": "ice", "items": []}, "stream_ice": {"class": "ice", "items": []}, "shelf_rime": {"class": "shore_ice", "items": []},
             "stair_treads": {"class": "rock", "items": [], "collider": False}, "stair_snow": {"class": "snow", "items": []}}
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
    for e in stream_ice:
        slabs["stream_ice"]["items"].append({"poly": sim_poly(e["poly"]), "z0": round(e["top"] - 0.15, 3), "z1": e["top"]})
    for e in rime:
        slabs["shelf_rime"]["items"].append({"poly": sim_poly(e["poly"]), "z0": round(R["shelf_z"] - 0.1, 3), "z1": e["top"]})
    # the CLIFF SKIRT: the face behind the kit, a 0.35 m rock band along the lip from the sea to the crest (the heightfield's
    # own face cells are not drawn) -- outside the route stretch, which has its own rock
    # R-C9-208 (5): the skirt is a continuous RIBBON wall along the lip (top = the clifftop behind it), broken only at the cave's
    # mouth and the stair's landing
    lip_f = K.resample(lip, 0.5)
    runs, cur = [], []
    for a in lip_f:
        ta, sa = to_fr(a)
        gap = abs(sa) < 3.0 and (R["shelf_t"][0] - 10.0 < ta < t_land + 0.3)      # R-C9-212: the kit is the face there
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
    stair_rib = {"pts": [], "z0": SEA_Z - 0.6, "thick": 0.4}
    tq = t_foot - 0.3
    while tq <= t_land + 0.01:
        q = fr(tq, S0 + W_ + 0.05)
        stair_rib["pts"].append([round(q[0], 3), round(-q[1], 3), round(min(R["crest"], max(R["shelf_z"], nosing_z(tq) - rise)) - 0.2, 3)])
        tq += 0.25
    end_rib = {"pts": [[round(q[0], 3), round(-q[1], 3), round(R["crest"] - 0.04, 3)] for q in (fr(t_land + 0.05, S0 + W_ + 0.05), fr(t_land + 0.05, 2.5), fr(t_land + 0.05, 0.0))],
               "z0": SEA_Z - 0.6, "thick": 0.4}
    ribbons = {"cliff_skirt_wall": {"class": "rock", "items": skirt_runs}, "stair_side": {"class": "rock", "items": [stair_rib, end_rib]}}
    for e in treads:
        slabs["stair_treads"]["items"].append({"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]})
    for e in snow_lips:
        slabs["stair_snow"]["items"].append({"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]})
    slabs["stair_rocks"] = {"class": "rock", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in stair_rocks]}
    slabs["shelf_ribs"] = {"class": "rock", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in shelf_marks]}
    slabs["shelf_pools"] = {"class": "shore_ice", "items": [{"poly": sim_poly(e["poly"]), "z0": e["z0"], "z1": e["z1"]} for e in shelf_pools]}

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
    route_out = [fr(R["shelf_t"][0] - 3.5, 3.0), fr(R["shelf_t"][0] - 2.0, shelf_out(R["shelf_t"][0]) + 0.8)] + \
                [fr(t, shelf_out(t) + ob + 0.5) for t in np.arange(R["shelf_t"][0], R["shelf_t"][1] + 0.01, 1.0)] + \
                [fr(R["shelf_t"][1] + 0.3 + ob, R["shelf_out_s"] - 1.0 + ob), fr(t_foot + ob, S0 + W_ + ob), fr(t_land + ob, S0 + W_ + ob), fr(t_land + ob, 0.0)]
    lip_route_e = [q for q, s_ in zip(lip, lip_s) if s_ > a_s + t_land + 1.0]
    bpoly = [q for q in off_shore if q[1] < wv[1] + 2] + off_lip_w + route_out + lip_route_e
    bpoly = [q for q in bpoly if q[0] <= wu[1] + 2]
    bpoly += [(wu[1], bpoly[-1][1]), (wu[1], wv[1] + 2), (off_shore[0][0], wv[1] + 2)]
    iw = 0.45
    # inner walls on the clifftop's edge, each with its own height band: over the cave they start above its arch (the cave is
    # walked beneath them); behind the stair they stand clear of the flight (it is seaward of them); open at the landing
    inner = [{"pts": [(q[0] - lip_at(s_)[2][0] * iw, q[1] - lip_at(s_)[2][1] * iw) for q, s_ in zip(lip, lip_s) if s_ < a_s + R["shelf_t"][0] - 3.0] + [fr(R["shelf_t"][0] - 3.5, -iw)],
              "z": [-1.5, 6.0]},
             {"pts": [fr(R["shelf_t"][0] - 3.5, -iw), fr(R["cave_t"] + cave_w / 2 + 0.5, -iw)], "z": [R["shelf_z"] + R["mouth_h"] + 0.4, R["head_z"] + 4.0]},
             {"pts": [fr(R["cave_t"] + cave_w / 2 + 0.5, -iw), fr(t_top, -iw)], "z": [-1.5, R["head_z"] + 4.0]},
             {"pts": [fr(t_land + 0.3, -iw)] + [(q[0] - lip_at(s_)[2][0] * iw, q[1] - lip_at(s_)[2][1] * iw) for q, s_ in zip(lip, lip_s) if s_ > a_s + t_land + 0.5],
              "z": [-1.5, 6.0]}]
    tints = json.load(open(os.path.join(BF, "data", "barrow_full_layout.json")))["tints_srgb"]
    tints.update(json.load(open(os.path.join(LV, "DEV12_proposal.json")))["class_list"]["new_classes_DEV2_provisional"])
    hf = {"file": "terrain_h.f32", "shape": [H, W], "px_per_m": HF_PPM, "extent_sim_m": {"x0": u0, "x1": u1, "y0": -v1, "y1": -v0}, "sha256": sha(os.path.join(OUT, "terrain_h.f32"))}
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
                "route": route_sim, "hall_panels": HALL_PANELS,
                "stair": None, "skip_models": [], "glb_copies": glb_copies, "glb_missing": [],
                "model_class": {"wreck": "wood", "barrow_front": "rock", "longhall": "wood", "fallen_gable": "char", "ring_stones": "rock", "slope_stones": "rock", "crags": "rock",
                                "cliff_faces": "rock", "talus": "rock", "sea_stacks": "rock", "palisade": "wood", "logs": "wood"},
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
        "route": {"_what": "R-C9-188/189/206: the walkable route from inside the sea cave over the shelf, up the rock-cut stair, onto the clifftop (lv_walkability.py checks it)",
                  "spec": {k: (list(v) if isinstance(v, tuple) else v) for k, v in R.items()},
                  "riser_m": round(rise, 5), "riser_range_m": [round(rise * (1 + min(jit)), 4), round(rise * (1 + max(jit)), 4)], "treads": n_tr,
                  "stair_pitch_deg": round(math.degrees(math.atan2(rise, R["tread"])), 3),
                  "frame": {"origin_uv": [round(LIP_A[0], 4), round(LIP_A[1], 4)], "along_uv": [round(dR[0], 6), round(dR[1], 6)], "t_foot": t_foot, "t_top": round(t_top, 4),
                            "t_landing_end": round(t_land, 4), "width_m": W_, "stair_s0": S0,
                            "_": "t along A -> B, s SEAWARD; the stair strip is s in [S0, S0 + W], built out against the face (R-C9-208)"},
                  "points_uv": {k: [round(q[0], 3), round(q[1], 3)] for k, q in {
                      "cave_back": fr(R["cave_t"], R["cave_front_s"] - min(3.0, dep_c * 0.5)), "cave_mouth": fr(R["cave_t"], R["cave_front_s"]),
                      "shelf_mid": fr((R["cave_t"] + t_foot) / 2, (R["shelf_in_s"] + R["shelf_out_s"]) / 2 + 0.5),
                      "bottom_landing": fr(t_foot - 1.0, S0 + W_ / 2), "stair_foot": fr(t_foot + 0.3, S0 + W_ / 2),
                      "stair_top": fr(t_top, S0 + W_ / 2), "landing": fr((t_top + t_land) / 2, S0 + W_ / 2), "clifftop": fr((t_top + t_land) / 2, -3.0)}.items()},
                  "polygons_uv": {"shelf": [[round(q[0], 3), round(q[1], 3)] for q in shelf], "cave_floor": [[round(q[0], 3), round(q[1], 3)] for q in cave_floor]},
                  "ramp": ramp, "plate": plate, "cave": {"scale": round(sc_cave, 5), "width_m": round(cave_w, 3), "depth_m": round(dep_c, 3), "z": round(cave_z, 3),
                                                        "mouth_from": "kit2/cave_mouth.json" if cave_meta else "stand-in (no measured mouth yet)"},
                  "sketch_A": "cave W, stair E as sketch A draws them: the cave under the lip at u %.1f, the stair climbing east across the face to the clifftop at u %.1f" % (fr(R["cave_t"], 0)[0], fr(t_land, 0)[0])},
        "classes": names, "class_counts": {names[k]: int((C == k).sum()) for k in range(len(names)) if (C == k).any()},
    }
    json.dump(layout, open(os.path.join(ART, "layout_bv2art.json"), "w"), indent=1)
    print("[art pp] window %.1f x %.1f m; %d placements; cliffs %d, talus %d, stacks %d; sea ice %.0f%% (%s, %d bob); mere plates %d; stream ice %d; treads %d; kit %s" % (
        wu[1] - wu[0], wv[1] - wv[0], len(layout_pl), len(cliff_insts), len(talus_insts) + len(shelf_rocks), len(stack_insts), 100 * ice_area / max(win_sea, 1e-6),
        layout["regions"]["sea_ice"]["pieces"], layout["regions"]["sea_ice"]["bobbing_floes"], len(mere_ice), len(stream_ice), len(treads),
        {k: ("kit2" if kit(k) == KIT2[k] else "standin") for k in KIT2}))


if __name__ == "__main__":
    main()
