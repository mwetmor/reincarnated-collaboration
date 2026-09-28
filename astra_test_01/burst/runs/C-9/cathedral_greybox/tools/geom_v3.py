#!/usr/bin/env python3
"""
CA-guides-v2{a,b,c,d} — PIER TREATMENTS.  Usage: geom_var.py <a|b|c|d>

gandalf's finding (and it is mine to own): v2's "3.99 % walkable occlusion" measured the PLATE
after the occluders had left the plate. Composited, 58.9 % of walkable sits behind the pier
layer and 67.4 % behind pier-or-vault before any fade. The indoor read worked; fight
readability did not. These four treatments are the candidates, built on one chain so the only
difference between them is the pier.

  a  GHOSTED SHAFTS  solid to 4 m, the shaft above at a fixed 35 % always
  b  RUINED ARCADE   two thirds broken off at 2-7 m (varied); the intact third chosen BY
                     MEASUREMENT as the piers that occlude least; the vault bays they carried
                     fall with them (crack law E3: a pier fails, the bays it carried come down)
  c  FEWER, SLIMMER  ~9.5 m bays, 1.4 m section, all intact
  d  GRADED GHOST    drax's fourth: solid to 4 m then opacity ramped 0.60 / 0.30 / 0.12 with
                     height. The BASE is what the player must read as an obstacle; the UPPER
                     shaft is what hides distant floor, and it is also what carries the indoor
                     read. A ramp keeps both; a flat 35 % trades them against each other.

In all four the VAULT is RIBS AND EDGES ONLY -- no filled cells.

Authority: R-C9-53 / CORRIGENDUM-FORWARD 5 (no zoom-out; the indoor feel is carried OVER and
AROUND the player), on top of R-C9-43/44/45 and the crack-law corrigenda.

Emits geometry_v2.json, canvas_v2.json, registration_v2.json, build_target.json.

World frame: X = EAST, Y = NORTH, Z = UP.  Origin = the CROSSING centre.  Godot = (x, z, -y).

A box may carry:
  f=1  FADE layer  — a prop that fades around the player (T3m). NOT in the plate: the plate must
                     carry the floor BEHIND it, or the fade reveals nothing.
  v=1  VAULT layer — the overhead/near layer (scroll > 1, edge-anchored, T3p). Not in the plate.
  ry   yaw in radians (the vault's diagonal ribs are the only non-axis-aligned geometry).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, ".."))
SPEC = json.load(open(os.path.join(PROJ, "cathedral_spec.json")))

P = SPEC["projection"]
PPM, ALPHA = P["ppm_plate"], math.radians(P["alpha_deg"])
PXG, PXE = P["px_per_m_along_view"], P["px_per_m_elevation"]
DV = np.array(P["d_plan_NW"]); RV = np.array(P["r_plan_NE"])
COT_A = 1.0 / math.tan(ALPHA)

RM = SPEC["room"]
X_W0, Y_S, X_E0, Y_N = RM["bbox_m"]
EXT_EW, EXT_NS = RM["extent_ew_m"], RM["extent_ns_m"]
AREA_TARGET = RM["walkable_area_target_m2"]
X_W, X_E = X_W0, X_E0
EL = SPEC["elevation"]
RISE_DECLARED = EL["wall_rise_m"]; CUT = EL["near_cut_m"]
ARC_TOP = EL["arcade"][1]; TRI0, TRI1 = EL["triforium"]; CLE0, CLE1 = EL["clerestory"]
DAIS_H = EL["dais_h"]; CM = EL["cross_mount"]
SUR = SPEC["surround"]
SNW, SSE = SUR["nw_m"], SUR["se_m"]
AISLE_W = SUR["aisle_w"]            # 4.5 m, lineage DECLARED -- pinned, not re-invented
WALL_T = SUR["aisle_wall"]          # 1.5 m
R_CRATER = SPEC["crater"]["radius_m"]
APRON_M = SPEC["apron"]["depth_m"]
ENT = {e["id"]: e for e in SPEC["entrances"]}
CRYPT, SEF, NCH = ENT["E-CRYPT"], ENT["E-SE-FIRE"], ENT["E-N-CHANCEL"]
VIEW_W, VIEW_H = SPEC["runtime_camera"]["view_px"]
ANC_X, ANC_Y = SPEC["runtime_camera"]["anchor_px"]

# ---- v2 DECLARED constants ------------------------------------------------------------
# CA-guides-v3 -- THE CANONICAL GUIDE SET (R-C9-55, Matt's middle option).
# "Make the ruined pillars look as if they've crumbled due to the fighting and blasts of magic
#  and fire. The broken pieces should be visible nearby somewhere but not covering the floor."
VARIANT = "3"
BREAK_FRAC = float(sys.argv[1]) if len(sys.argv) > 1 else 0.50
VP = dict(
 **{"3": dict(sec=2.0, bay=6.5, ruin=True,
              bands=[(0.0, 4.0, 1.00), (4.0, 8.0, 0.60), (8.0, 14.0, 0.30), (14.0, None, 0.12)])},
 a=dict(sec=2.0, bay=6.5,  ruin=False, bands=[(0.0, 4.0, 1.00), (4.0, None, 0.35)]),
 b=dict(sec=2.0, bay=6.5,  ruin=True,  bands=[(0.0, None, 1.00)]),
 c=dict(sec=1.4, bay=9.5,  ruin=False, bands=[(0.0, None, 1.00)]),
 z=dict(sec=2.0, bay=6.5,  ruin=False, bands=[(0.0, None, 1.00)]),   # v2 BASELINE, for the row
 d=dict(sec=2.0, bay=6.5,  ruin=False, bands=[(0.0, 4.0, 1.00), (4.0, 8.0, 0.60),
                                              (8.0, 14.0, 0.30), (14.0, None, 0.12)]),
)[VARIANT]
GHOST_CLS = ["nave_pier", "pier_ghost_1", "pier_ghost_2", "pier_ghost_3"]
BREAK_TOP = 1.0        # the jagged, blasted zone at the top of a broken stub
DEBRIS_PER_PIER = 3
DEBRIS_KINDS = [("drum", 1.10, 0.65), ("capital", 1.40, 0.85), ("vault_stone", 0.80, 0.45)]
DEBRIS_R_MAX = 9.0
PIER_SEC = VP["sec"]  # square pier section. "thick piers you could hide a horse behind"
                      # (crack-law sec 1, mass before grace). The lineage's arcade pier is
                      # 1.6 m; this is heavier on purpose. A horse is ~2.4 x 0.8 m, so 2.0 m
                      # square hides one end-on and most of one broadside.
BAY_TARGET = VP["bay"]  # "about 6-7 m bays"; the lineage's derived bay_m is 6.5645, in band.
BAY_LO, BAY_HI = (9.0, 10.0) if VARIANT == "c" else (6.0, 7.0)
VESS_VAULT_SPRING, VESS_VAULT_CROWN = 26.0, 34.0
AISLE_VAULT_SPRING, AISLE_VAULT_CROWN = 11.0, 14.0
RIB_SEC = 0.45
DAIS_Y0, DAIS_Y1, APSE_Y0 = 14.0, 21.0, 21.0
CEIL_BEYOND = 11.0
CRYPT_DEPTH, CRATER_DEPTH = 6.0, 3.0
PIER_PLINTH = 0.35    # the only part of a rising pier that is IN THE PLATE

LEGEND = [
 ( 0, "void_outside_frame",  (  0,200,  0), False, (  0,255,  0)),
 ( 1, "opening_to_outside",  (  0,255,  0), False, (  0,255,  0)),
 ( 2, "nave_floor",          ( 46,204, 64), True,  (228,228,222)),
 ( 3, "crossing_floor",      (  1,255,112), True,  (232,232,226)),
 ( 4, "transept_floor",      (127,219,255), True,  (224,224,219)),
 ( 5, "chancel_floor",       (255,220,  0), True,  (220,220,215)),
 ( 6, "dais",                (240, 18,190), True,  (214,214,209)),
 ( 7, "apse_floor",          (177, 13,201), True,  (210,210,205)),
 ( 8, "crater",              (255, 65, 54), False, ( 44, 40, 40)),
 ( 9, "crypt_void",          ( 17, 17, 17), False, ( 20, 20, 24)),
 (10, "apron_bluefire",      (  0,116,217), True,  (196,200,208)),
 (11, "apron_fire",          (255,133, 27), True,  (208,198,190)),
 (12, "pier",                (133, 20, 75), False, ( 84, 84, 90)),
 (13, "wall_rising",         ( 58, 58, 62), False, (120,120,126)),
 (14, "wall_cutlow",         ( 96, 96,102), False, (104,104,110)),
 (15, "room_beyond_floor",   (  0,190,200), False, (132,132,138)),
 (16, "room_beyond_wall",    ( 80, 80, 86), False, ( 74, 74, 80)),
 (17, "triforium_dark",      ( 61,153,112), False, ( 30, 30, 34)),
 (18, "clerestory_tracery",  (203,203,199), False, (150,150,154)),
 (19, "cross_mount_empty",   (255,255,255), False, ( 38, 38, 42)),
 (20, "breach_stair",        (118,112,100), False, ( 96, 92, 86)),
 (21, "exterior_ground",     (140,136,128), False, (118,116,110)),
 (22, "pool_candidate",      (255,  0,255), True,  (216,214,208)),
 # --- v2 ---
 (23, "aisle_floor",         ( 60,160,120), True,  (222,222,217)),
 (24, "nave_pier",           (220, 40,120), False, ( 76, 76, 82)),   # rising pier, FADES
 (25, "vault_rib",           ( 90,200,255), False, (128,128,134)),
 (26, "vault_cell",          ( 40,110,160), False, ( 96, 96,102)),
 (28, "pier_ghost_1",       (235,110,190), False, ( 76, 76, 82)),
 (29, "pier_ghost_2",       (250,160,215), False, ( 76, 76, 82)),
 (30, "pier_ghost_3",       (255,205,235), False, ( 76, 76, 82)),
 (31, "pier_break",         (255, 90, 40), False, ( 58, 52, 50)),
 (32, "debris",             (190,120, 50), False, ( 92, 88, 82)),
 (27, "wall_rising_fade",    (150, 90,200), False, (120,120,126)),   # the occluding W segment
]
# ⚑ Sort by index. snap() in the post pass returns a legend LIST POSITION, while IDX[name]
# returns the `index` FIELD -- and inserting new classes before older ones made those diverge.
# Consequence: `cls == IDX["debris"]` (32) compared against positions that stop at 27, so it was
# always False and the debris assertion reported "0 pixels" for 54 boxes that were rendering
# perfectly. Position == index is now an invariant of the file.
LEGEND = sorted(LEGEND, key=lambda e: e[0])
assert [e[0] for e in LEGEND] == list(range(len(LEGEND))), "legend index must equal position"
CIDX = {n: i for i, n, *_ in LEGEND}

BOXES, DISCS, PROPS, SPAWN_GALLERIES, OPENINGS = [], [], [], [], []

def box(cls, x0, x1, y0, y1, z0, z1, f=0, v=0, ry=None):
    if x1-x0 <= 1e-6 or y1-y0 <= 1e-6 or z1-z0 <= 1e-6: return
    b = dict(c=CIDX[cls], p=[(x0+x1)/2, (y0+y1)/2, (z0+z1)/2], s=[x1-x0, y1-y0, z1-z0])
    if f: b["f"] = 1
    if v: b["v"] = 1
    if ry is not None: b["ry"] = ry
    BOXES.append(b)

def rbox(cls, cx, cy, cz, sx, sy, sz, ry, f=0, v=0):
    b = dict(c=CIDX[cls], p=[cx, cy, cz], s=[sx, sy, sz], ry=ry)
    if f: b["f"] = 1
    if v: b["v"] = 1
    BOXES.append(b)

# ===================================================== 1. SOLVE THE LIMB WIDTH
# v1 solved the limb width with no piers inside the walkable. v2 punches PIER FOOTPRINTS out of
# it, and the pier COUNT depends on the width (the arms get longer as the limb narrows), so the
# solve is a fixed point, not a quadratic. Bisect, recomputing the piers at every step.
A_CRATER = math.pi * R_CRATER**2
A_CRYPT = CRYPT["size_m"][0] * CRYPT["size_m"][1]

def bay_split(lo, hi):
    """split [lo,hi] into bays as near BAY_TARGET as possible; returns the boundary positions"""
    L = hi - lo
    if L <= 1e-6: return [lo]
    def cost(n):
        p_ = L/n
        return (0.0 if BAY_LO <= p_ <= BAY_HI else min(abs(p_-BAY_LO), abs(p_-BAY_HI)),
                abs(p_-BAY_TARGET))
    n = min(range(1, max(2, int(L/3.0))+1), key=cost)
    return [lo + i * L / n for i in range(n + 1)]

def pier_layout(W):
    """pier centres for a cruciform of total limb width W. Returns (list, vessel, xp, pitches)"""
    v = W - 2.0*AISLE_W - 2.0*PIER_SEC
    if v <= 2.0: return None
    xp = v/2.0 + PIER_SEC/2.0
    pts, pitches = [], {}
    # nave, south leg and chancel leg: rows at x = +-xp
    for tag, lo, hi in (("nave_south", Y_S, -xp), ("chancel_north", xp, Y_N)):
        bs = bay_split(lo, hi)
        if len(bs) > 1: pitches[tag] = bs[1]-bs[0]
        for yv in bs:
            for sx in (-xp, xp): pts.append((sx, yv))
    # transept arms: rows at y = +-xp
    for tag, lo, hi in (("arm_west", X_W, -xp), ("arm_east", xp, X_E)):
        bs = bay_split(lo, hi)
        if len(bs) > 1: pitches[tag] = bs[1]-bs[0]
        for xv in bs:
            for sy in (-xp, xp): pts.append((xv, sy))
    uniq = sorted({(round(a, 6), round(b, 6)) for a, b in pts})
    return uniq, v, xp, pitches

def net_area(W):
    lay = pier_layout(W)
    if lay is None: return -1e9, 0
    pts = lay[0]
    gross = EXT_NS*W + EXT_EW*W - W*W
    return gross - A_CRATER - A_CRYPT - len(pts)*PIER_SEC*PIER_SEC, len(pts)

lo, hi = 14.0, 40.0
for _ in range(80):
    mid = (lo+hi)/2
    if net_area(mid)[0] < AREA_TARGET: lo = mid
    else: hi = mid
W_LIMB = (lo+hi)/2
PIERS, VESSEL_W, XP, BAY_PITCH = pier_layout(W_LIMB)
HW = W_LIMB/2.0
NET_SOLVED, N_PIERS = net_area(W_LIMB)
AREA_RESIDUAL = NET_SOLVED - AREA_TARGET

# ===================================================== 2. FLOOR RASTER
CELL = 0.20
gx0, gx1 = X_W - SNW, X_E + SSE
gy0, gy1 = Y_S - SSE, Y_N + SNW
NX = int(round((gx1-gx0)/CELL)); NY = int(round((gy1-gy0)/CELL))
xs = gx0 + (np.arange(NX)+0.5)*CELL
ys = gy0 + (np.arange(NY)+0.5)*CELL
GX, GY = np.meshgrid(xs, ys, indexing="ij")

in_nave     = (np.abs(GX) <= HW) & (GY >= Y_S) & (GY < -HW)
in_cross    = (np.abs(GX) <= HW) & (np.abs(GY) <= HW)
in_transept = (np.abs(GX) > HW) & (GX >= X_W) & (GX <= X_E) & (np.abs(GY) <= HW)
in_chancel  = (np.abs(GX) <= HW) & (GY > HW) & (GY < DAIS_Y0)
in_dais     = (np.abs(GX) <= HW) & (GY >= DAIS_Y0) & (GY < DAIS_Y1)
in_apse     = (np.abs(GX) <= HW) & (GY >= APSE_Y0) & (GY <= Y_N)
cruciform   = in_nave | in_cross | in_transept | in_chancel | in_dais | in_apse
# the aisle band: outside the vessel, inside the limb -- walkable, and it counts (R-C9-53 cl.3)
VIN0 = XP - PIER_SEC/2                      # inner face of the pier line = the vessel half-width
vessel_mask = cruciform & ((np.abs(GX) <= VIN0) | (np.abs(GY) <= VIN0))
aisle = cruciform & ~vessel_mask & ~in_dais & ~in_apse

crater = (GX**2 + GY**2) <= R_CRATER**2
ccx, ccy = CRYPT["centre_m"]; ccw, cch = CRYPT["size_m"]
crypt = (np.abs(GX-ccx) <= ccw/2) & (np.abs(GY-ccy) <= cch/2)
pier_plan = np.zeros_like(cruciform)
for (ppx, ppy) in PIERS:
    pier_plan |= (np.abs(GX-ppx) <= PIER_SEC/2) & (np.abs(GY-ppy) <= PIER_SEC/2)
walk = cruciform & ~crater & ~crypt & ~pier_plan
AREA_RASTER = float(walk.sum()) * CELL * CELL

def dilate_mask(m, r):
    k = int(math.ceil(r/CELL))
    yy, xx = np.ogrid[-k:k+1, -k:k+1]
    disk = (xx*xx + yy*yy) * CELL*CELL <= r*r
    pad = np.zeros((m.shape[0]+2*k, m.shape[1]+2*k), bool); pad[k:-k, k:-k] = m
    out = np.zeros_like(m)
    for dy in range(-k, k+1):
        for dx in range(-k, k+1):
            if disk[dy+k, dx+k]:
                out |= pad[k+dy:k+dy+m.shape[0], k+dx:k+dx+m.shape[1]]
    return out

mouth_crypt = crypt
sfx, sfy = SEF["centre_m"]; sfw = SEF["width_m"]
mouth_se = (np.abs(GX-sfx) <= sfw/2) & (np.abs(GY-sfy) <= 1.0)
ncx, ncy = NCH["centre_m"]; ncw = NCH["width_m"]
mouth_nc = (np.abs(GX-ncx) <= ncw/2) & (np.abs(GY-ncy) <= 1.0)

# ===================================================== 3. WALLS  (as v1)
def wall_axis(p0, p1):
    if abs(p1[1]-p0[1]) < 1e-9: return 0, p0[1], min(p0[0], p1[0]), max(p0[0], p1[0])
    return 1, p0[0], min(p0[1], p1[1]), max(p0[1], p1[1])
def footprint(axis, fixed, t0, t1, side, thick=WALL_T):
    a, b = (fixed, fixed+thick) if side > 0 else (fixed-thick, fixed)
    return (t0, t1, a, b) if axis == 0 else (a, b, t0, t1)
def slab(axis, fixed, t0, t1, z0, z1, cls, side, thick=WALL_T, f=0):
    if t1-t0 <= 1e-6 or z1-z0 <= 1e-6: return
    a, b = (fixed, fixed+thick) if side > 0 else (fixed-thick, fixed)
    if axis == 0: box(cls, t0, t1, a, b, z0, z1, f=f)
    else:         box(cls, a, b, t0, t1, z0, z1, f=f)
def plane(axis, fixed, t0, t1, z0, z1, cls, m=0.07, f=0):
    if t1-t0 <= 1e-6 or z1-z0 <= 1e-6: return
    if axis == 0: box(cls, t0, t1, fixed-m, fixed+m, z0, z1, f=f)
    else:         box(cls, fixed-m, fixed+m, t0, t1, z0, z1, f=f)

def sweep_occlusion(x0, x1, y0, y1, h):
    probe = h * COT_A
    acc = np.zeros_like(walk)
    for t in np.arange(0.0, probe+CELL, CELL):
        qx = GX - DV[0]*t; qy = GY - DV[1]*t
        acc |= (qx >= x0) & (qx <= x1) & (qy >= y0) & (qy <= y1)
    return float((acc & walk).sum()) * CELL * CELL

ARCH_SLABS = 5
def storey(axis, fixed, t0, n, pitch, z0, z1, sill, spring, open_frac,
           open_cls, side, wall_name, tag, skip=(), mullion=False, proxy=True, fade_bays=()):
    for k in range(n):
        b0 = t0 + k*pitch; b1 = b0 + pitch
        fk = 1 if k in fade_bays else 0
        wc = "wall_rising_fade" if fk else "wall_rising"
        if k in skip:
            plane(axis, fixed, b0, b1, z0, z1, "opening_to_outside")
            OPENINGS.append(dict(wall=wall_name, band=tag, bay=k, width_m=pitch, z=[z0, z1],
                                 centre_m=([(b0+b1)/2, fixed] if axis == 0 else [fixed, (b0+b1)/2])))
            continue
        ow = pitch*open_frac; oc = (b0+b1)/2.0
        o0, o1 = oc-ow/2, oc+ow/2; Rr = ow/2.0; apex = spring+Rr
        slab(axis, fixed, b0, o0, z0, apex, wc, side, f=fk)
        slab(axis, fixed, o1, b1, z0, apex, wc, side, f=fk)
        if sill > z0: slab(axis, fixed, o0, o1, z0, sill, wc, side, f=fk)
        for s in range(ARCH_SLABS):
            y0 = spring + Rr*s/ARCH_SLABS; y1 = spring + Rr*(s+1)/ARCH_SLABS
            hwid = math.sqrt(max(Rr*Rr - ((y0+y1)/2-spring)**2, 0.0))
            slab(axis, fixed, o0, oc-hwid, y0, y1, wc, side, f=fk)
            slab(axis, fixed, oc+hwid, o1, y0, y1, wc, side, f=fk)
        slab(axis, fixed, b0, b1, apex, z1, wc, side, f=fk)
        cls = open_cls(k) if callable(open_cls) else open_cls
        if cls and proxy:
            plane(axis, fixed, o0, o1, sill, spring, cls, f=fk)
            for s in range(ARCH_SLABS):
                y0 = spring + Rr*s/ARCH_SLABS; y1 = spring + Rr*(s+1)/ARCH_SLABS
                hwid = math.sqrt(max(Rr*Rr - ((y0+y1)/2-spring)**2, 0.0))
                plane(axis, fixed, oc-hwid, oc+hwid, y0, y1, cls, f=fk)
        if mullion:
            slab(axis, fixed, oc-0.175, oc+0.175, sill, apex, "clerestory_tracery", side, f=fk)
        ctr = [oc, fixed] if axis == 0 else [fixed, oc]
        if cls == "opening_to_outside":
            OPENINGS.append(dict(wall=wall_name, band=tag, bay=k, centre_m=ctr,
                                 z=[sill, apex], width_m=ow, faded=bool(fk)))
        elif cls == "triforium_dark":
            SPAWN_GALLERIES.append(dict(id="SG-%s-b%d" % (wall_name, k), wall=wall_name,
                                        centre_m=ctr, z=[sill, apex], width_m=ow,
                                        kind="descend_from_above"))

RISING = [
 ("R1-nave-west",     (-HW, Y_S), (-HW, -HW), -1),
 ("R2-chancel-west",  (-HW,  HW), (-HW, Y_N), -1),
 ("R3-transeptW-n",   (X_W,  HW), (-HW,  HW), +1),
 ("R5-transeptW-end", (X_W, -HW), (X_W,  HW), -1),
 ("R6-apse",          (-HW, Y_N), ( HW, Y_N), +1),
]
CUTLOW = [
 ("C1-nave-east",     ( HW, Y_S), ( HW, -HW), +1),
 ("C2-chancel-east",  ( HW,  HW), ( HW, Y_N), +1),
 ("C3-transeptW-s",   (X_W, -HW), (-HW, -HW), -1),
 ("C4-transeptE-s",   ( HW, -HW), (X_E, -HW), -1),
 ("C5-transeptE-end", (X_E, -HW), (X_E,  HW), +1),
 ("C6-south-facade",  (-HW, Y_S), ( HW, Y_S), -1),
 ("C7-transeptE-n-CUT", ( HW,  HW), (X_E,  HW), +1),   # settled R-C9-53 cl.4
]
BAY = BAY_TARGET
BREACH_WALL = "R1-nave-west"
WALL_BAYS, rise_report, fade_walls = {}, [], []
for name, p0, p1, side in RISING:
    axis, fixed, t0, t1 = wall_axis(p0, p1)
    x0, x1, y0, y1 = footprint(axis, fixed, t0, t1, side)
    hiA = sweep_occlusion(x0, x1, y0, y1, RISE_DECLARED)
    rise_report.append(dict(element=name, hidden_at_full_height_m2=hiA))
    n = max(1, int(round((t1-t0)/BAY))); pitch = (t1-t0)/n
    # PER-BAY fade test: a bay whose NW sweep hides walkable is a FADING prop (R-C9-53 cl.4,
    # "the tall WEST-wall segment that hides the west transept arm FADES"). Per bay, not per
    # wall, because the occlusion is a re-entrant-corner effect local to one end.
    fb = set()
    for k in range(n):
        b0 = t0 + k*pitch; b1 = b0 + pitch
        fx0, fx1, fy0, fy1 = footprint(axis, fixed, b0, b1, side)
        a_hi = sweep_occlusion(fx0, fx1, fy0, fy1, RISE_DECLARED)
        a_lo = sweep_occlusion(fx0, fx1, fy0, fy1, CUT)
        if a_hi - a_lo > 0.5:
            fb.add(k); fade_walls.append(dict(wall=name, bay=k, hides_m2=a_hi-a_lo,
                                              centre_m=[(b0+b1)/2, fixed] if axis == 0
                                              else [fixed, (b0+b1)/2]))
    skip = set(range(int(0.30*n), max(int(0.30*n)+1, int(0.70*n)))) if name == BREACH_WALL else set()
    WALL_BAYS[name] = dict(axis=axis, fixed=fixed, t0=t0, t1=t1, n=n, pitch=pitch, side=side,
                           breach_bays=sorted(skip), fade_bays=sorted(fb))
    storey(axis, fixed, t0, n, pitch, 0.0, ARC_TOP, 0.0, 6.0, 0.62,
           None, side, name, "arcade", proxy=False, fade_bays=fb)
    storey(axis, fixed, t0, n, pitch, TRI0, TRI1, TRI0+0.6, 15.0, 0.60,
           lambda k: "opening_to_outside" if k % 2 == 0 else "triforium_dark",
           side, name, "triforium", skip=skip, fade_bays=fb)
    storey(axis, fixed, t0, n, pitch, CLE0, CLE1, CLE0+1.5, 22.5, 0.55,
           "opening_to_outside", side, name, "clerestory", skip=skip, mullion=True, fade_bays=fb)
    for k in range(n):
        if k in skip: continue
        b0 = t0 + k*pitch
        slab(axis, fixed, b0, b0+pitch, CLE1, RISE_DECLARED,
             "wall_rising_fade" if k in fb else "wall_rising", side, f=1 if k in fb else 0)

for name, p0, p1, side in CUTLOW:
    axis, fixed, t0, t1 = wall_axis(p0, p1)
    gaps = []
    if name == "C6-south-facade": gaps = [(-2.5, 2.5), (sfx-sfw/2, sfx+sfw/2)]
    if name == "C5-transeptE-end": gaps = [(-2.0, 2.0)]
    segs = [(t0, t1)]
    for g0, g1 in gaps:
        ns = []
        for s0, s1 in segs:
            if g1 <= s0 or g0 >= s1: ns.append((s0, s1)); continue
            if g0 > s0: ns.append((s0, g0))
            if g1 < s1: ns.append((g1, s1))
        segs = ns
    for s0, s1 in segs:
        slab(axis, fixed, s0, s1, 0.0, CUT, "wall_cutlow", side)
        slab(axis, fixed, s0, s1, 0.0, 0.35, "wall_cutlow", side, thick=WALL_T*1.7)

# north chancel breach + the broken stair on the PLAYABLE side (settled R-C9-53 cl.4)
BOXES[:] = [b for b in BOXES if not (
    b["c"] in (CIDX["wall_rising"], CIDX["wall_rising_fade"]) and
    abs(b["p"][1] - (Y_N + WALL_T/2)) < WALL_T and
    b["p"][0]-b["s"][0]/2 < ncx+ncw/2 and b["p"][0]+b["s"][0]/2 > ncx-ncw/2 and
    b["p"][2]-b["s"][2]/2 < 5.0)]
plane(0, Y_N + WALL_T/2, ncx-ncw/2, ncx+ncw/2, 0.0, 5.0, "opening_to_outside", m=0.10)
OPENINGS.append(dict(wall="R6-apse", band="chancel_breach", bay=-1, centre_m=[ncx, Y_N],
                     z=[0.0, 5.0], width_m=ncw))
for i in range(5):
    if i in (2, 3): continue
    box("breach_stair", ncx-ncw/2, ncx+ncw/2, Y_N-0.75*(i+1), Y_N-0.75*i, 0.0, 2.6-i*0.52)

cmx, cb, chh, cw2, cat = CM["cx"], CM["base_h"], CM["height"], CM["width"], CM["arm_thick"]
box("cross_mount_empty", cmx-cat/2, cmx+cat/2, Y_N-0.18, Y_N+0.02, cb, cb+chh)
box("cross_mount_empty", cmx-cw2/2, cmx+cw2/2, Y_N-0.18, Y_N+0.02, cb+chh*0.62, cb+chh*0.62+cat)

# ===================================================== 4. PIERS
# A rising pier is a PROP that FADES (R-C9-53 cl.3). It is therefore NOT in the plate: if it were
# painted in, fading it would reveal nothing -- the plate must carry the floor behind it. What
# stays in the plate is a PLINTH, so the painter knows where the pier lands and the walkable mask
# excludes its footprint. The shaft ships in the FADE layer.
CROSS_CORNERS = {(round(sx*XP, 6), round(sy*XP, 6)) for sx in (-1, 1) for sy in (-1, 1)}
# Per-pier occlusion cost, MEASURED: the walkable area this pier hides at full height. Used to
# choose variant b's intact third -- "where they occlude least" is a measurement, not a taste.
pier_cost = {}
for (ppx, ppy) in PIERS:
    if (round(ppx, 6), round(ppy, 6)) in CROSS_CORNERS: continue
    pier_cost[(ppx, ppy)] = sweep_occlusion(ppx-PIER_SEC/2, ppx+PIER_SEC/2,
                                            ppy-PIER_SEC/2, ppy+PIER_SEC/2, RISE_DECLARED)
BROKEN = {}
if VP["ruin"]:
    # Break the piers whose loss buys the MOST visibility: rank by the walkable area each one
    # hides and break from the top down. R-C9-55: "break the ones whose loss buys the most".
    ranked = sorted(pier_cost, key=lambda k: pier_cost[k])
    n_break = int(round(len(ranked)*BREAK_FRAC))
    intact = set(ranked[:len(ranked)-n_break])
    # broken heights: golden-ratio low-discrepancy over [2, 7], then a pass that pushes any two
    # NEIGHBOURING piers at least 0.8 m apart, so no run of the arcade repeats a height.
    order = sorted(set(pier_cost) - intact, key=lambda k: (round(k[0], 3), round(k[1], 3)))
    prev = None
    for i, k in enumerate(order):
        h_ = 2.0 + 5.0*(((i+1)*0.6180339887498949) % 1.0)
        if prev is not None and abs(h_-prev) < 0.8:
            h_ = h_ + 0.8 if h_ >= prev else h_ - 0.8
            h_ = min(7.0, max(2.0, h_))
        BROKEN[k] = h_
        prev = h_
pier_rows = []
for (ppx, ppy) in PIERS:
    key = (ppx, ppy)
    corner = (round(ppx, 6), round(ppy, 6)) in CROSS_CORNERS
    box("nave_pier", ppx-PIER_SEC/2, ppx+PIER_SEC/2, ppy-PIER_SEC/2, ppy+PIER_SEC/2,
        -0.30, PIER_PLINTH if not corner else CUT)
    if corner:
        PROPS.append(dict(kind="crossing_pier", centre_m=[ppx, ppy],
                          footprint_m=[PIER_SEC, PIER_SEC], height_m=CUT,
                          sort_line_y_m=ppy-PIER_SEC/2, fade=False, rises=False,
                          id_class="nave_pier"))
        pier_rows.append(dict(centre_m=[ppx, ppy], corner=True, height_m=CUT, broken=False,
                              bands=[]))
        continue
    brk = BROKEN.get(key)
    use_bands = [(0.0, None, 1.00)] if brk is not None else VP["bands"]
    top_final = brk if brk is not None else None      # None = to the sprite height, set later
    bands = []
    for bi, (z0, z1, op) in enumerate(use_bands):
        cls = GHOST_CLS[min(bi, len(GHOST_CLS)-1)]
        z1e = z1
        if brk is not None:
            if z0 >= brk: break
            z1e = brk if (z1 is None or z1 > brk) else z1
        elif z1 is None:
            z1e = RISE_DECLARED                        # patched to the sprite height below
        zz0 = max(z0, PIER_PLINTH)
        if z1e is not None and z1e <= zz0: continue
        if brk is not None and z1e >= brk - 1e-6:
            # the shaft up to the blasted zone, then a jagged crown: the 2 m section is diced
            # into 0.5 m cells, each ending at its own height. No clean cut anywhere.
            shaft_top = max(zz0, brk - BREAK_TOP)
            box(cls, ppx-PIER_SEC/2, ppx+PIER_SEC/2, ppy-PIER_SEC/2, ppy+PIER_SEC/2,
                zz0, shaft_top, f=1)
            n_c = 4
            cw_ = PIER_SEC/n_c
            # the blast came from the crossing: cells on the crossing-facing side lose more
            bdir = np.array([-ppx, -ppy]); nrm = np.hypot(*bdir) or 1.0; bdir = bdir/nrm
            pk = abs(hash((round(ppx, 3), round(ppy, 3)))) % 9973
            for ci in range(n_c):
                for cj in range(n_c):
                    ox_ = ppx - PIER_SEC/2 + (ci+0.5)*cw_
                    oy_ = ppy - PIER_SEC/2 + (cj+0.5)*cw_
                    facing = float(np.dot([ox_-ppx, oy_-ppy], bdir))/(PIER_SEC/2)
                    r_ = (((pk + ci*37 + cj*101)*0.6180339887498949) % 1.0)
                    top = brk - 0.15 - 0.85*r_ - 0.55*max(facing, 0.0)
                    top = max(shaft_top + 0.12, min(brk, top))
                    box("pier_break", ox_-cw_/2, ox_+cw_/2, oy_-cw_/2, oy_+cw_/2,
                        shaft_top, top, f=1)
            bands.append(dict(cls=cls, z=[zz0, shaft_top], opacity=op, open_top=False))
            bands.append(dict(cls="pier_break", z=[shaft_top, brk], opacity=1.0, open_top=False,
                              note="jagged blast crown; SCORCH AND SHATTER ARE PAINT -- this "
                                   "class marks where the brief calls for them"))
            break
        box(cls, ppx-PIER_SEC/2, ppx+PIER_SEC/2, ppy-PIER_SEC/2, ppy+PIER_SEC/2,
            zz0, z1e, f=1)
        bands.append(dict(cls=cls, z=[zz0, z1e], opacity=op, open_top=(z1 is None and brk is None)))
    arch_top = brk if brk is not None else VESS_VAULT_SPRING
    BOXES.append(dict(c=CIDX["nave_pier"], o=1, p=[ppx, ppy, (PIER_PLINTH+arch_top)/2],
                      s=[PIER_SEC, PIER_SEC, arch_top-PIER_PLINTH]))
    PROPS.append(dict(kind="nave_pier", centre_m=[ppx, ppy],
                      footprint_m=[PIER_SEC, PIER_SEC],
                      height_m=arch_top, architectural_top_m=arch_top,
                      broken=(brk is not None), bands=bands,
                      hides_walkable_at_full_height_m2=pier_cost[key],
                      sort_line_y_m=ppy-PIER_SEC/2, fade=True, rises=(brk is None),
                      id_class="nave_pier"))
    pier_rows.append(dict(centre_m=[ppx, ppy], corner=False,
                          height_m=arch_top, broken=(brk is not None), bands=bands,
                          hides_m2=pier_cost[key]))
for fw in fade_walls:
    PROPS.append(dict(kind="fading_wall_segment", wall=fw["wall"], bay=fw["bay"],
                      centre_m=fw["centre_m"], hides_walkable_m2=fw["hides_m2"],
                      height_m=RISE_DECLARED, fade=True, id_class="wall_rising_fade",
                      sort_line_y_m=fw["centre_m"][1]))

# ===================================================== 4b. DEBRIS (R-C9-55 cl.3)
# "The broken pieces should be visible nearby somewhere but not covering the floor."
# Fallen drums, capitals and vault stones go ONLY into non-walkable dead space: the pier plinth
# footprints, the margins under the arcade arches, the crater rim, and against the cut-low walls.
# Placement is by ASSERTION, not by eye -- a piece is accepted only if its whole footprint
# rasterises clear of every walkable cell.
# ⚑ THIS OVERRIDES CRACK-LAW RULE 4's TALUS CONE. A cone at the angle of repose spills onto the
#    floor by construction; readability wins. Divergence row: DIV-debris-no-talus.
DEBRIS = []
_taken = np.zeros_like(walk)
_near_arena = ((GX >= X_W - 6.0) & (GX <= X_E + 6.0) & (GY >= Y_S - 6.0) & (GY <= Y_N + 6.0))
_dead = (~walk) & _near_arena
# First cut sampled random polar offsets and placed ZERO pieces: the dead space near a pier is
# its own 2 m plinth and a 1.5 m wall band, and random sampling of a disc essentially never
# lands a footprint wholly inside either. Scan the dead cells that actually exist, nearest first.
_KMAX = int(math.ceil(DEBRIS_R_MAX/CELL)) + 4
for pr in pier_rows:
    if not pr.get("broken"): continue
    bx_, by_ = pr["centre_m"]
    ci0 = int((bx_-gx0)/CELL); cj0 = int((by_-gy0)/CELL)
    i0 = max(ci0-_KMAX, 0); i1 = min(ci0+_KMAX+1, NX)
    j0 = max(cj0-_KMAX, 0); j1 = min(cj0+_KMAX+1, NY)
    LX = GX[i0:i1, j0:j1]; LY = GY[i0:i1, j0:j1]
    Lwalk = walk[i0:i1, j0:j1]; Ldead = _dead[i0:i1, j0:j1]
    dist = np.hypot(LX-bx_, LY-by_)
    cand = np.nonzero(Ldead & (dist <= DEBRIS_R_MAX))
    if len(cand[0]) == 0: continue
    order = np.argsort(dist[cand])
    placed = 0
    seed = abs(hash((round(bx_, 3), round(by_, 3), "deb"))) % 9973
    for oi in order:
        if placed >= DEBRIS_PER_PIER: break
        a_, b_ = cand[0][oi], cand[1][oi]
        # round BEFORE testing: the record carries a rounded centre, and a 0.5 mm shift can
        # flip a cell exactly on the footprint boundary -- which is what made the assertion
        # fire on pieces the placement test had just cleared.
        cx_ = round(float(LX[a_, b_]), 3); cy_ = round(float(LY[a_, b_]), 3)
        kind, size, hgt = DEBRIS_KINDS[(seed + placed*5 + int(oi)) % len(DEBRIS_KINDS)]
        h_ = size/2.0
        sel = (np.abs(LX-cx_) <= h_) & (np.abs(LY-cy_) <= h_)
        if not sel.any(): continue
        if (sel & Lwalk).any(): continue                     # the assertion, per candidate
        if not Ldead[sel].all(): continue
        Ltaken = _taken[i0:i1, j0:j1]
        if (sel & Ltaken).any(): continue
        _taken[i0:i1, j0:j1] |= (np.abs(LX-cx_) <= h_+0.25) & (np.abs(LY-cy_) <= h_+0.25)
        box("debris", cx_-h_, cx_+h_, cy_-h_, cy_+h_, -0.05, hgt)
        rec = dict(kind=kind, centre_m=[cx_, cy_],
                   footprint_m=[size, size], height_m=hgt,
                   from_pier_m=[bx_, by_], distance_m=round(float(dist[a_, b_]), 3),
                   sort_line_y_m=round(cy_-h_, 3))
        DEBRIS.append(rec)
        PROPS.append(dict(kind="debris_"+kind, centre_m=rec["centre_m"],
                          footprint_m=[size, size], height_m=hgt, fade=False,
                          id_class="debris", sort_line_y_m=rec["sort_line_y_m"],
                          from_pier_m=[bx_, by_]))
        placed += 1
# hard assertion, in plan, before anything is rendered
_dmask = np.zeros_like(walk)
for d_ in DEBRIS:
    cx_, cy_ = d_["centre_m"]; h_ = d_["footprint_m"][0]/2.0
    _dmask |= (np.abs(GX-cx_) <= h_) & (np.abs(GY-cy_) <= h_)
DEBRIS_ON_WALKABLE = int((_dmask & walk).sum())
# "not covering the floor" also means not HIDING much of it: a 0.85 m stone hides 0.64 m of
# floor to its north-west. Measured, not assumed.
_docc = np.zeros_like(walk)
for d_ in DEBRIS:
    cx_, cy_ = d_["centre_m"]; h_ = d_["footprint_m"][0]/2.0
    for t in np.arange(0.0, d_["height_m"]*COT_A + CELL, CELL):
        qx = GX - DV[0]*t; qy = GY - DV[1]*t
        _docc |= (np.abs(qx-cx_) <= h_) & (np.abs(qy-cy_) <= h_)
DEBRIS_OCCLUDES_M2 = float((_docc & walk).sum())*CELL*CELL
assert DEBRIS_ON_WALKABLE == 0, "debris on walkable floor: %d cells" % DEBRIS_ON_WALKABLE

# ===================================================== 5. VAULT (overhead layer)
BROKEN_PTS = [k for k in BROKEN]
def bay_fallen(x0, x1, y0, y1):
    """crack law E3: a pier fails and the bays it carried come down -- but a bay standing on
    four supports does not fall when it loses ONE. It falls on losing TWO. R-C9-55: "only the
    vault bays carried by broken piers fall; keep most of the vault"."""
    if not BROKEN: return False
    n = 0
    for cx_ in (x0, x1):
        for cy_ in (y0, y1):
            if any(abs(bx-cx_) <= PIER_SEC and abs(by-cy_) <= PIER_SEC for (bx, by) in BROKEN_PTS):
                n += 1
    return n >= 2
def vault_bay(x0, x1, y0, y1, spring, crown, axis=1):
    """TRANSVERSE RIBS AND SPRINGERS ONLY. First cut drew boundary ribs, diagonals and a filled
    cell and MEASURED 30.49 % floor coverage -- a rib at 34 m throws a band of its own width
    across the floor, and there is a lot of rib. "Edge-anchored, never over more than a thin
    share of the floor" means the arch you see crossing the frame, not a whole net of stone."""
    if bay_fallen(x0, x1, y0, y1):
        vault_fallen.append([x0, x1, y0, y1]); return
    if axis == 1:
        for a, b in ((y0, y0+RIB_SEC), (y1-RIB_SEC, y1)):
            box("vault_rib", x0, x1, a, b, crown-0.05, crown+0.35, v=1)
    else:
        for a, b in ((x0, x0+RIB_SEC), (x1-RIB_SEC, x1)):
            box("vault_rib", a, b, y0, y1, crown-0.05, crown+0.35, v=1)
    for ax in (x0, x1):
        for ay in (y0, y1):
            box("vault_rib", ax-RIB_SEC/2, ax+RIB_SEC/2, ay-RIB_SEC/2, ay+RIB_SEC/2,
                spring, crown, v=1)

vault_bays, vault_fallen = [], []
def vault_run(lo, hi, axis, lane_lo, lane_hi, spring, crown, tag):
    bs = bay_split(lo, hi)
    for i in range(len(bs)-1):
        n0 = len(vault_fallen)
        vault_bay(*( (lane_lo, lane_hi, bs[i], bs[i+1]) if axis == 1
                     else (bs[i], bs[i+1], lane_lo, lane_hi) ), spring, crown, axis)
        if len(vault_fallen) > n0: continue
        vault_bays.append(dict(tag=tag, span=[bs[i], bs[i+1]], lane=[lane_lo, lane_hi],
                               crown_m=crown))

VIN = XP - PIER_SEC/2       # inner face of the pier line = the vessel
vault_run(Y_S, -XP, 1, -VIN, VIN, VESS_VAULT_SPRING, VESS_VAULT_CROWN, "nave_vessel")
vault_run(XP, Y_N, 1, -VIN, VIN, VESS_VAULT_SPRING, VESS_VAULT_CROWN, "chancel_vessel")
vault_run(X_W, -XP, 0, -VIN, VIN, VESS_VAULT_SPRING, VESS_VAULT_CROWN, "arm_west_vessel")
vault_run(XP, X_E, 0, -VIN, VIN, VESS_VAULT_SPRING, VESS_VAULT_CROWN, "arm_east_vessel")
vault_bay(-VIN, VIN, -VIN, VIN, VESS_VAULT_SPRING, VESS_VAULT_CROWN + 3.0, 1)  # crossing lantern
vault_bays.append(dict(tag="crossing_lantern", span=[-VIN, VIN], lane=[-VIN, VIN],
                       crown_m=VESS_VAULT_CROWN+3.0))
for side_lo, side_hi in ((-HW, -XP-PIER_SEC/2), (XP+PIER_SEC/2, HW)):
    vault_run(Y_S, -XP, 1, side_lo, side_hi, AISLE_VAULT_SPRING, AISLE_VAULT_CROWN, "nave_aisle")
    vault_run(XP, Y_N, 1, side_lo, side_hi, AISLE_VAULT_SPRING, AISLE_VAULT_CROWN, "chancel_aisle")
    vault_run(X_W, -XP, 0, side_lo, side_hi, AISLE_VAULT_SPRING, AISLE_VAULT_CROWN, "arm_w_aisle")
    vault_run(XP, X_E, 0, side_lo, side_hi, AISLE_VAULT_SPRING, AISLE_VAULT_CROWN, "arm_e_aisle")

# ===================================================== 6. FLOORS
def rects(mask, cls, z0, z1):
    m = mask.copy(); n = 0
    for i in range(NX):
        j = 0
        while j < NY:
            if not m[i, j]: j += 1; continue
            j2 = j
            while j2+1 < NY and m[i, j2+1]: j2 += 1
            i2 = i
            while i2+1 < NX and m[i2+1, j:j2+1].all(): i2 += 1
            m[i:i2+1, j:j2+1] = False
            box(cls, gx0+i*CELL, gx0+(i2+1)*CELL, gy0+j*CELL, gy0+(j2+1)*CELL, z0, z1)
            n += 1; j = j2+1
    return n

inside_bbox = (GX >= X_W) & (GX <= X_E) & (GY >= Y_S) & (GY <= Y_N)
nw_band = ((GX < X_W) | (GY > Y_N)) & (GX >= gx0) & (GY <= gy1)
se_band = ((GX > X_E) | (GY < Y_S))
beyond = ((inside_bbox & ~cruciform) | nw_band) & ~se_band
exterior = se_band & ~cruciform

def occlusion_grid(h):
    probe = h*COT_A
    out = np.zeros_like(walk)
    for t in np.arange(0.0, probe+CELL, CELL):
        qx = GX + DV[0]*t; qy = GY + DV[1]*t
        ix = np.clip(((qx-gx0)/CELL).astype(int), 0, NX-1)
        iy = np.clip(((qy-gy0)/CELL).astype(int), 0, NY-1)
        out |= walk[ix, iy]
    return out
ceiling = beyond & ~occlusion_grid(CEIL_BEYOND+0.6)

apron_blue = (dilate_mask(mouth_crypt, APRON_M) | dilate_mask(mouth_nc, APRON_M)) & walk
apron_fire = dilate_mask(mouth_se, APRON_M) & walk
apron_blue &= ~apron_fire
gal_mouth = np.zeros_like(walk)
for g in SPAWN_GALLERIES:
    gx_, gy_ = g["centre_m"]
    gal_mouth |= (np.abs(GX-gx_) <= g["width_m"]/2) & (np.abs(GY-gy_) <= g["width_m"]/2)
apron_blue |= dilate_mask(gal_mouth, APRON_M) & walk & ~apron_fire

base = walk & ~apron_blue & ~apron_fire
floor_classes = [
    ("aisle_floor",    aisle & base, 0.0),
    ("nave_floor",     in_nave     & base & ~aisle, 0.0),
    ("crossing_floor", in_cross    & base & ~aisle, 0.0),
    ("transept_floor", in_transept & base & ~aisle, 0.0),
    ("chancel_floor",  in_chancel  & base & ~aisle, 0.0),
    ("dais",           in_dais     & base, DAIS_H),
    ("apse_floor",     in_apse     & base, DAIS_H),
    ("apron_bluefire", apron_blue, 0.0),
    ("apron_fire",     apron_fire, 0.0),
]
n_rects = 0
for cls, m, ztop in floor_classes:
    n_rects += rects(m, cls, min(ztop-0.30, -0.30), ztop)
n_rects += rects(beyond, "room_beyond_floor", -0.30, 0.0)
n_rects += rects(exterior, "exterior_ground", -0.40, -0.10)
n_rects += rects(ceiling, "room_beyond_wall", CEIL_BEYOND, CEIL_BEYOND+0.6)
box("room_beyond_wall", gx0, gx0+0.8, gy0, gy1, -0.3, CEIL_BEYOND+0.6)
box("room_beyond_wall", gx0, gx1, gy1-0.8, gy1, -0.3, CEIL_BEYOND+0.6)
box("crypt_void", ccx-ccw/2, ccx+ccw/2, ccy-cch/2, ccy+cch/2, -CRYPT_DEPTH, -0.02)
DISCS.append(dict(c=CIDX["crater"], p=[0.0, 0.0, 0.01], r=R_CRATER+0.35, depth=CRATER_DEPTH))

# ===================================================== 7. POOLS  (settled: 618/622/623)
KEEP = {"Z-618", "Z-622", "Z-623"}
pool_rows = []
for p in SPEC["pool_registration"]["pools"]:
    px_, py_ = p["arena_m"]; r = p["radius_disjoint_m"]
    disc = ((GX-px_)**2 + (GY-py_)**2) <= r*r
    keep = p["id"] in KEEP
    pool_rows.append(dict(id=p["id"], arena_m=p["arena_m"], radius_disjoint_m=r,
                          verdict="KEEP" if keep else "DROP",
                          settled_by="R-C9-53 cl.4",
                          overlap_walkable_v2_m2=float((disc & walk).sum())*CELL*CELL))
pool_mask = np.zeros_like(walk)
for p, row in zip(SPEC["pool_registration"]["pools"], pool_rows):
    if row["verdict"] != "KEEP": continue
    px_, py_ = p["arena_m"]; r = p["radius_disjoint_m"]
    pool_mask |= (((GX-px_)**2 + (GY-py_)**2) <= r*r) & walk
pool_mask &= ~apron_blue & ~apron_fire
n_rects += rects(pool_mask, "pool_candidate", -0.02, 0.005)

# ============================ 7b. PER-PIER OCCLUSION MAPS (for the readability metric)
# gandalf's catch: v2 measured walkable occlusion ON THE PLATE, after the occluders had been
# moved OUT of the plate. The honest metric composites every layer. It needs, per pier, WHICH
# floor cells that pier hides and at WHAT OPACITY -- so the fade can be applied per pier and per
# player. A sight ray crosses a given pier's column exactly once, so each cell gets at most one
# band of each pier: the map is a single float per (pier, cell).
def band_occlusion(x0, x1, y0, y1, z0, z1):
    """cells hidden by the slab of this column between heights z0 and z1"""
    acc = np.zeros_like(walk)
    u0, u1 = z0*COT_A, z1*COT_A
    for t in np.arange(u0, u1+CELL, CELL):
        qx = GX - DV[0]*t; qy = GY - DV[1]*t
        acc |= (qx >= x0) & (qx <= x1) & (qy >= y0) & (qy <= y1)
    return acc & walk

occl_stack, occl_centres = [], []
for pr in pier_rows:
    if pr["corner"]:
        continue
    cx_, cy_ = pr["centre_m"]
    m = np.zeros(walk.shape, np.float32)
    for bd in pr["bands"]:
        z0, z1 = bd["z"]
        m[band_occlusion(cx_-PIER_SEC/2, cx_+PIER_SEC/2, cy_-PIER_SEC/2, cy_+PIER_SEC/2,
                         z0, z1)] = bd["opacity"]
    occl_stack.append(m); occl_centres.append([cx_, cy_])
for fw in fade_walls:
    ax, fx_, t0_, t1_ = wall_axis(*[(x, y) for x, y in
        ([( -HW, Y_S), (-HW, -HW)] if fw["wall"] == "R1-nave-west" else [(-HW, Y_S), (-HW, -HW)])])
    wb = WALL_BAYS[fw["wall"]]
    b0 = wb["t0"] + fw["bay"]*wb["pitch"]; b1 = b0 + wb["pitch"]
    fx0, fx1, fy0, fy1 = footprint(wb["axis"], wb["fixed"], b0, b1, wb["side"])
    m = np.zeros(walk.shape, np.float32)
    m[band_occlusion(fx0, fx1, fy0, fy1, 0.0, RISE_DECLARED)] = 1.0
    occl_stack.append(m); occl_centres.append(fw["centre_m"])
np.savez_compressed(os.path.join(PROJ, "occl_v3.npz"),
                    walk=walk, occl=np.array(occl_stack, np.float32),
                    centres=np.array(occl_centres, np.float64),
                    grid=np.array([gx0, gy0, CELL, walk.shape[0], walk.shape[1]]))
print("OCCL   %d fading occluders mapped" % len(occl_stack))

# ===================================================== 8. CANVAS  (as v1)
def screen(x, y, z):
    return (PPM*(x*RV[0] + y*RV[1]), -(PXG*(x*DV[0] + y*DV[1]) + PXE*z))

wi, wj = np.nonzero(walk)
wx = gx0 + (wi+0.5)*CELL; wy = gy0 + (wj+0.5)*CELL
wsx, wsy = screen(wx, wy, 0.0)
VIEW_W_PX, VIEW_H_PX = VIEW_W, VIEW_H
def s_of(x, y): return x*DV[0] + y*DV[1]
def sx_of(x, y): return PPM*(x*RV[0] + y*RV[1])
_pz = np.where((np.abs(wx) <= HW) & (wy >= DAIS_Y0), DAIS_H, 0.0)
_psx = sx_of(wx, wy); _pval = PXG*s_of(wx, wy) + PXE*_pz
_bx0 = int(np.floor(_psx.min()))-2; _nb = int(np.ceil(_psx.max()))-_bx0+4
_bin = np.full(_nb, -1e18); np.maximum.at(_bin, (_psx-_bx0).astype(int), _pval)
def sliding_max(a, lo_, hi_):
    n = len(a); w = lo_+hi_+1
    pad = int(np.ceil(n/w)*w)-n
    b = np.concatenate([a, np.full(pad, -1e18)]); m = b.reshape(-1, w)
    L = np.maximum.accumulate(m, 1).ravel()
    Rr = np.maximum.accumulate(m[:, ::-1], 1)[:, ::-1].ravel()
    idx = np.arange(n); a0 = idx-lo_; a1 = idx+hi_
    res = np.full(n, -1e18)
    ok = a1 < len(L); res[ok] = np.maximum(res[ok], L[a1[ok]])
    ok = a0 >= 0;     res[ok] = np.maximum(res[ok], Rr[a0[ok]])
    return res
_win = sliding_max(_bin, VIEW_W_PX-ANC_X, ANC_X)
def _grid(x0, x1, y0, y1):
    A, B = np.meshgrid(np.arange(x0, x1+CELL, CELL), np.arange(y0, y1+CELL, CELL), indexing="ij")
    return A.ravel(), B.ravel()
_crowns = []
for name, p0, p1, side in RISING:
    ax, fx, t0, t1 = wall_axis(p0, p1)
    _crowns.append(_grid(*footprint(ax, fx, t0, t1, side)))
_h_req = 0.0
for cxs, cys in _crowns:
    ii = np.clip((sx_of(cxs, cys)-_bx0).astype(int), 0, _nb-1)
    _h_req = max(_h_req, float(np.nanmax((_win[ii] - PXG*s_of(cxs, cys) + ANC_Y)/PXE)))
RISE = max(RISE_DECLARED, math.ceil(_h_req*2)/2.0 + 1.0)
for b in BOXES:
    if b["c"] in (CIDX["wall_rising"], CIDX["wall_rising_fade"]) \
       and abs(b["p"][2]+b["s"][2]/2 - RISE_DECLARED) < 1e-6:
        top, bot = RISE, b["p"][2]-b["s"][2]/2
        b["p"][2] = (top+bot)/2; b["s"][2] = top-bot
for pr in PROPS:
    if pr.get("height_m") == RISE_DECLARED: pr["height_m"] = RISE

fx0, fx1 = wsx.min()-ANC_X, wsx.max()+(VIEW_W-ANC_X)
fy0, fy1 = wsy.min()-ANC_Y, wsy.max()+(VIEW_H-ANC_Y)
PLATE_TOP_ELEV = CLE1 + 2.0
ry = []
for b in BOXES:
    if b["c"] not in (CIDX["wall_rising"], CIDX["wall_rising_fade"]): continue
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            ry.append(screen(b["p"][0]+sx_*b["s"][0]/2, b["p"][1]+sy_*b["s"][1]/2, PLATE_TOP_ELEV)[1])
px0 = math.floor(fx0); px1 = math.ceil(fx1)
py0 = math.floor(min(fy0, min(ry))); py1 = math.ceil(fy1)
CANVAS_W = int(px1-px0); CANVAS_H = int(py1-py0)
CANVAS_W += (-CANVAS_W) % 4; CANVAS_H += (-CANVAS_H) % 4
# PIER HEIGHT. A rising pier is a FADE-layer prop: not painted into the plate, so its height does
# not size the canvas and costs nothing. Set it so every pier's top projects ABOVE the canvas top
# -- then no pier crown can enter any frame, by construction, and the painter's pier sprite is cut
# by the canvas edge exactly as a prop that leaves the frame should be.
PIER_H = 0.0
for pr in pier_rows:
    if pr["corner"]: continue
    cx_, cy_ = pr["centre_m"]
    PIER_H = max(PIER_H, (-py0 - PXG*s_of(cx_, cy_))/PXE)
PIER_H = math.ceil(PIER_H) + 1.0
GHOST_IDS = {CIDX[c] for c in GHOST_CLS}
for b in BOXES:
    if b.get("f") == 1 and b["c"] in GHOST_IDS and abs(b["p"][2]+b["s"][2]/2 - RISE_DECLARED) < 1e-6:
        bot = b["p"][2]-b["s"][2]/2
        b["p"][2] = (PIER_H+bot)/2; b["s"][2] = PIER_H-bot
for pr in pier_rows:
    for bd in pr.get("bands", []):
        if bd.get("open_top"): bd["z"][1] = PIER_H
TILE = 4096
tiles = [dict(name="t_%d_%d" % (r_, c_), origin_px=[c_*TILE, r_*TILE], size_px=[TILE, TILE])
         for r_ in range((CANVAS_H+TILE-1)//TILE) for c_ in range((CANVAS_W+TILE-1)//TILE)]
canvas = dict(canvas_px=[CANVAS_W, CANVAS_H], origin_screen_px=[px0, py0], ppm=PPM,
              tile_px=TILE, tiles=tiles, r_plan_NE=list(RV), d_plan_NW=list(DV),
              pxg=PXG, pxe=PXE, plate_top_elevation_m=PLATE_TOP_ELEV,
              wall_rise_built_m=RISE, wall_rise_solved_m=_h_req, pier_height_m=PIER_H,
              clamp=dict(plate_rect_px=[float(fx0-px0), float(fy0-py0), float(fx1-px0), float(fy1-py0)],
                         rule="camera centre = player plate px - (anchor - view/2)"))

# ===================================================== 9. WRITE
json.dump(dict(legend=[dict(index=i, name=n, rgb=list(c), walkable=w, guide_grey=list(g))
                       for i, n, c, w, g in LEGEND], boxes=BOXES, discs=DISCS),
          open(os.path.join(PROJ, "geometry_v3.json"), "w"))
json.dump(canvas, open(os.path.join(PROJ, "canvas_v3.json"), "w"), indent=1)
json.dump(dict(geometry="geometry_v3.json", canvas="canvas_v3.json",
               out_dir="/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/"
                       "7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/ca3_tiles",
               tscn="res://cathedral_greybox_v3.tscn",
               passes=["guide", "id", "height", "fade", "id_fade", "vault", "arch"]),
          open(os.path.join(PROJ, "build_target.json"), "w"), indent=1)
json.dump(dict(
    solve=dict(limb_width_m=W_LIMB, vessel_width_m=VESSEL_W, aisle_width_m=AISLE_W,
               pier_section_m=PIER_SEC, pier_line_x_m=XP, n_piers=N_PIERS,
               pier_footprint_total_m2=N_PIERS*PIER_SEC*PIER_SEC,
               bay_pitches_m=BAY_PITCH, bay_target_m=BAY_TARGET, bay_band_m=[BAY_LO, BAY_HI],
               gross_cruciform_m2=EXT_NS*W_LIMB+EXT_EW*W_LIMB-W_LIMB**2,
               crater_m2=A_CRATER, crypt_m2=A_CRYPT,
               net_walkable_m2=NET_SOLVED, target_m2=AREA_TARGET,
               residual_m2=AREA_RESIDUAL, raster_check_m2=AREA_RASTER,
               raster_cell_m=CELL,
               note="the pier COUNT depends on the width (the arms lengthen as the limb "
                    "narrows), so this is a fixed point, bisected, not a quadratic."),
    wall_rise=dict(declared_m=RISE_DECLARED, solved_required_m=_h_req, built_m=RISE,
                   scope="the PLATE's rising walls only. Piers are FADE-layer props and are not "
                         "in the plate, so they do not enter this solve."),
    pier_height=dict(built_m=PIER_H, architectural_springing_m=VESS_VAULT_SPRING,
                     rule="tall enough that every pier top projects above the canvas top, so no "
                          "pier crown can enter any frame. Free: the pier is not in the plate."),
    variant=VARIANT, variant_params=dict(pier_section_m=PIER_SEC, bay_target_m=BAY_TARGET,
        ruined=VP["ruin"], bands=VP["bands"], ghost_classes=GHOST_CLS),
    broken_piers={"%.3f,%.3f" % k: round(v, 3) for k, v in BROKEN.items()},
    pier_occlusion_cost_m2={"%.3f,%.3f" % k: round(v, 3) for k, v in pier_cost.items()},
    vault_fallen_bays=vault_fallen, break_fraction=BREAK_FRAC,
    debris=DEBRIS, debris_on_walkable_cells=DEBRIS_ON_WALKABLE,
    debris_footprint_total_m2=sum(d["footprint_m"][0]**2 for d in DEBRIS),
    debris_occludes_walkable_m2=DEBRIS_OCCLUDES_M2,
    debris_rule="fallen drums, capitals and vault stones only in non-walkable dead space near "
                "their own pier: plinth footprints, the margins under the arcade arches, the "
                "crater rim, against the cut-low walls. Accepted only if the whole footprint "
                "rasterises clear of every walkable cell. OVERRIDES crack-law rule 4's talus "
                "cone (DIV-debris-no-talus): a cone at the angle of repose spills onto the "
                "floor by construction.",
    break_profile="jagged: the 2 m section is diced into 0.5 m cells, each ending at its own "
                  "height, biased lower on the crossing-facing side (the blast came from the "
                  "demon gate). Class 'pier_break' marks the blasted crown -- SCORCH AND "
                  "SHATTER ARE PAINT, and this is where the brief calls for them.",
    piers=pier_rows, props=PROPS, fade_wall_bays=fade_walls,
    spawn_galleries=SPAWN_GALLERIES, openings=OPENINGS, pools=pool_rows,
    rise_report=rise_report, vault_bays=len(vault_bays),
    vault=dict(vessel_spring_m=VESS_VAULT_SPRING, vessel_crown_m=VESS_VAULT_CROWN,
               aisle_spring_m=AISLE_VAULT_SPRING, aisle_crown_m=AISLE_VAULT_CROWN,
               lantern_crown_m=VESS_VAULT_CROWN+3.0, rib_section_m=RIB_SEC, bays=len(vault_bays)),
    apron_area_m2=dict(bluefire=float(apron_blue.sum())*CELL*CELL,
                       fire=float(apron_fire.sum())*CELL*CELL),
    aisle_area_m2=float((aisle & walk).sum())*CELL*CELL),
    open(os.path.join(PROJ, "registration_v3.json"), "w"), indent=1)

print("VARIANT %s  pier %.2f m  bay target %.2f  ruined=%s  bands=%s"
      % (VARIANT, PIER_SEC, BAY_TARGET, VP["ruin"], VP["bands"]))
print("SOLVE  limb %.6f m = aisle %.3f + pier %.2f + vessel %.6f + pier %.2f + aisle %.3f"
      % (W_LIMB, AISLE_W, PIER_SEC, VESSEL_W, PIER_SEC, AISLE_W))
print("       piers %d x %.1f m^2 = %.3f m^2 of footprint" % (N_PIERS, PIER_SEC**2, N_PIERS*PIER_SEC**2))
print("       bay pitches: %s" % {k: round(v, 3) for k, v in BAY_PITCH.items()})
print("       net walkable %.6f  target %.6f  RESIDUAL %.3e m2" % (NET_SOLVED, AREA_TARGET, AREA_RESIDUAL))
print("       raster check %.4f m2 (cell %.2f m)  aisle share %.3f m2"
      % (AREA_RASTER, CELL, float((aisle & walk).sum())*CELL*CELL))
print("CROWN  walls: solved %.4f m, built %.1f m | piers (fade layer): %.1f m" % (_h_req, RISE, PIER_H))
print("FADE   %d rising piers + %d wall bays (%s)"
      % (sum(1 for p in pier_rows if not p["corner"]), len(fade_walls),
         ", ".join("%s b%d %.1fm2" % (f["wall"], f["bay"], f["hides_m2"]) for f in fade_walls)))
print("RUIN   %d broken of %d rising piers (frac %.2f); %d of %d vault bays fell"
      % (len(BROKEN), len(pier_cost), BREAK_FRAC, len(vault_fallen), len(vault_fallen)+len(vault_bays)))
print("DEBRIS %d pieces; walkable cells under a footprint: %d (assertion 0); hides %.2f m2 of floor"
      % (len(DEBRIS), DEBRIS_ON_WALKABLE, DEBRIS_OCCLUDES_M2))
print("VAULT  %d bays, %d boxes total, canvas %d x %d, tiles %d"
      % (len(vault_bays), len(BOXES), CANVAS_W, CANVAS_H, len(tiles)))
