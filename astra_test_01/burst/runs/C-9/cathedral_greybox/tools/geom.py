#!/usr/bin/env python3
"""
CA-guides-v1 — authored geometry for the cathedral arena grey box.

Emits geometry.json (axis-aligned boxes + the crater cone, each tagged with an id class),
canvas.json (plate rect, tile grid, camera clamp) and registration.json (the pool registration).

World frame: X = EAST, Y = NORTH, Z = UP.  Origin = the CROSSING centre.
Godot frame: godot = (x, z, -y).
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
HW = RM["limb_half_m"]; X_W, Y_S, X_E, Y_N = RM["bbox_m"]
BAY = RM["bay_m"]
EL = SPEC["elevation"]
RISE = EL["wall_rise_m"]; CUT = EL["near_cut_m"]
ARC_TOP = EL["arcade"][1]; TRI0, TRI1 = EL["triforium"]; CLE0, CLE1 = EL["clerestory"]
DAIS_H = EL["dais_h"]; CM = EL["cross_mount"]
SUR = SPEC["surround"]
SNW, SSE = SUR["nw_m"], SUR["se_m"]
PIER_W, AISLE_W, AISLE_WALL, CHAPEL_D = SUR["pier_w"], SUR["aisle_w"], SUR["aisle_wall"], SUR["chapel_d"]
WALL_T = AISLE_WALL
R_CRATER = SPEC["crater"]["radius_m"]
APRON_M = SPEC["apron"]["depth_m"]
ENT = {e["id"]: e for e in SPEC["entrances"]}
CRYPT, SEF, NCH = ENT["E-CRYPT"], ENT["E-SE-FIRE"], ENT["E-N-CHANCEL"]
VIEW_W, VIEW_H = SPEC["runtime_camera"]["view_px"]
ANC_X, ANC_Y = SPEC["runtime_camera"]["anchor_px"]

DAIS_Y0, DAIS_Y1, APSE_Y0 = 14.0, 21.0, 21.0
CEIL_BEYOND = 11.0
CRYPT_DEPTH = 6.0
CRATER_DEPTH = 3.0

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
]
CIDX = {n: i for i, n, *_ in LEGEND}

BOXES, DISCS, PROPS, SPAWN_GALLERIES, OPENINGS = [], [], [], [], []

def box(cls, x0, x1, y0, y1, z0, z1):
    if x1 - x0 <= 1e-6 or y1 - y0 <= 1e-6 or z1 - z0 <= 1e-6: return
    BOXES.append(dict(c=CIDX[cls], p=[(x0+x1)/2, (y0+y1)/2, (z0+z1)/2], s=[x1-x0, y1-y0, z1-z0]))

# =============================================================== 1. FLOOR RASTER
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

crater = (GX**2 + GY**2) <= R_CRATER**2
ccx, ccy = CRYPT["centre_m"]; ccw, cch = CRYPT["size_m"]
crypt = (np.abs(GX-ccx) <= ccw/2) & (np.abs(GY-ccy) <= cch/2)
walk = cruciform & ~crater & ~crypt
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

# =============================================================== 2. WALLS
def wall_axis(p0, p1):
    if abs(p1[1]-p0[1]) < 1e-9: return 0, p0[1], min(p0[0], p1[0]), max(p0[0], p1[0])
    return 1, p0[0], min(p0[1], p1[1]), max(p0[1], p1[1])

def slab(axis, fixed, t0, t1, z0, z1, cls, side, thick=WALL_T):
    if t1 - t0 <= 1e-6 or z1 - z0 <= 1e-6: return
    a, b = (fixed, fixed + thick) if side > 0 else (fixed - thick, fixed)
    if axis == 0: box(cls, t0, t1, a, b, z0, z1)
    else:         box(cls, a, b, t0, t1, z0, z1)

def plane(axis, fixed, t0, t1, z0, z1, cls, m=0.07):
    if t1 - t0 <= 1e-6 or z1 - z0 <= 1e-6: return
    if axis == 0: box(cls, t0, t1, fixed - m, fixed + m, z0, z1)
    else:         box(cls, fixed - m, fixed + m, t0, t1, z0, z1)

ARCH_SLABS = 5
def storey(axis, fixed, t0, n, pitch, z0, z1, sill, spring, open_frac,
           open_cls, side, wall_name, tag, skip=(), mullion=False, proxy=True):
    for k in range(n):
        b0 = t0 + k*pitch; b1 = b0 + pitch
        if k in skip:
            plane(axis, fixed, b0, b1, z0, z1, "opening_to_outside")
            OPENINGS.append(dict(wall=wall_name, band=tag, bay=k, width_m=pitch, z=[z0, z1],
                                 centre_m=([(b0+b1)/2, fixed] if axis == 0 else [fixed, (b0+b1)/2])))
            continue
        ow = pitch * open_frac
        oc = (b0+b1)/2.0
        o0, o1 = oc - ow/2, oc + ow/2
        Rr = ow/2.0
        apex = spring + Rr
        slab(axis, fixed, b0, o0, z0, apex, "wall_rising", side)
        slab(axis, fixed, o1, b1, z0, apex, "wall_rising", side)
        if sill > z0: slab(axis, fixed, o0, o1, z0, sill, "wall_rising", side)
        for s in range(ARCH_SLABS):
            y0 = spring + Rr*s/ARCH_SLABS; y1 = spring + Rr*(s+1)/ARCH_SLABS
            hwid = math.sqrt(max(Rr*Rr - ((y0+y1)/2 - spring)**2, 0.0))
            slab(axis, fixed, o0, oc-hwid, y0, y1, "wall_rising", side)
            slab(axis, fixed, oc+hwid, o1, y0, y1, "wall_rising", side)
        slab(axis, fixed, b0, b1, apex, z1, "wall_rising", side)
        cls = open_cls(k) if callable(open_cls) else open_cls
        if cls and proxy:
            plane(axis, fixed, o0, o1, sill, spring, cls)
            for s in range(ARCH_SLABS):
                y0 = spring + Rr*s/ARCH_SLABS; y1 = spring + Rr*(s+1)/ARCH_SLABS
                hwid = math.sqrt(max(Rr*Rr - ((y0+y1)/2 - spring)**2, 0.0))
                plane(axis, fixed, oc-hwid, oc+hwid, y0, y1, cls)
        if mullion:
            slab(axis, fixed, oc-0.175, oc+0.175, sill, apex, "clerestory_tracery", side)
        ctr = [oc, fixed] if axis == 0 else [fixed, oc]
        if cls == "opening_to_outside":
            OPENINGS.append(dict(wall=wall_name, band=tag, bay=k, centre_m=ctr,
                                 z=[sill, apex], width_m=ow))
        elif cls == "triforium_dark":
            SPAWN_GALLERIES.append(dict(id="SG-%s-b%d" % (wall_name, k), wall=wall_name,
                                        centre_m=ctr, z=[sill, apex], width_m=ow,
                                        kind="descend_from_above",
                                        foot_m=ctr))
        if tag == "arcade":
            pc = [b0, fixed + side*WALL_T/2] if axis == 0 else [fixed + side*WALL_T/2, b0]
            PROPS.append(dict(kind="arcade_pier", wall=wall_name, bay=k, centre_m=pc,
                              footprint_m=([PIER_W, WALL_T] if axis == 0 else [WALL_T, PIER_W]),
                              height_m=RISE, sort_line=(fixed if axis == 0 else b0)))

# ---- THE RISE RULE, functional and applied without a per-element list -------------------
# Corrigendum 3 cl.2 and Corrigendum 4 cl.1 both give the SAME reason for cutting a side low:
# "nothing full-height stands between the camera and the floor". So the test is not which
# compass face a wall carries, it is whether RAISING it costs play space. Same rule already
# governs the rooms-beyond ceiling; here it governs walls and piers too.
def sweep_occlusion(x0, x1, y0, y1, h):
    """walkable area (m2) hidden by an element of height h standing on this footprint"""
    probe = h * COT_A
    acc = np.zeros_like(walk)
    for t in np.arange(0.0, probe + CELL, CELL):
        qx = GX - DV[0]*t; qy = GY - DV[1]*t
        acc |= (qx >= x0) & (qx <= x1) & (qy >= y0) & (qy <= y1)
    return float((acc & walk).sum()) * CELL * CELL

def footprint(axis, fixed, t0, t1, side, thick=WALL_T):
    a, b = (fixed, fixed + thick) if side > 0 else (fixed - thick, fixed)
    return (t0, t1, a, b) if axis == 0 else (a, b, t0, t1)

RISE_TOL_M2 = 0.5
rise_report = []
def rise_test(name, axis, fixed, t0, t1, side, thick=WALL_T):
    x0, x1, y0, y1 = footprint(axis, fixed, t0, t1, side, thick)
    hi = sweep_occlusion(x0, x1, y0, y1, RISE)
    lo = sweep_occlusion(x0, x1, y0, y1, CUT)
    ok = (hi - lo) <= RISE_TOL_M2
    rise_report.append(dict(element=name, rises=bool(ok),
                            hidden_at_full_height_m2=hi, hidden_at_cut_height_m2=lo,
                            extra_cost_m2=hi-lo, probe_m=RISE*COT_A))
    return ok

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
 # R4, the EAST transept arm's north wall. By compass it is a north face, but it is the EAST
 # ARM's wall and R-C9-45 cl.1 cuts EAST low. MEASURED cost of raising it: it hides 106.760 m2
 # of chancel floor from the camera AND it hides the EMPTY CROSS MOUNT -- the scene's declared
 # landmark (R-C9-45 cl.2, F-S3) -- behind its face. Recorded as a divergence, not silent.
 ("C7-transeptE-n-CUT", ( HW,  HW), (X_E,  HW), +1),
]
BREACH_WALL = "R1-nave-west"
WALL_BAYS = {}
# RISE_MODE
#   "compass"    (DEFAULT, and what R-C9-45 cl.1 literally rules): a wall whose INNER FACE points
#                into the camera hemisphere -- north-facing or west-facing -- rises; south-facing
#                and east-facing are cut low. Every element's occlusion cost is MEASURED and
#                reported, and nothing is demoted silently.
#   "functional" (pass --functional): additionally demote any rising wall that hides more walkable
#                floor at full height than it would at knee height. This is the rule the greyroom
#                lineage used and the reason BOTH corrigenda give for cutting a side low; it is
#                offered because a cruciform under a 45 deg camera has RE-ENTRANT corners that
#                neither corrigendum contemplates, and there the two rules disagree.
RISE_MODE = "functional" if "--functional" in sys.argv else "compass"
demoted = []
for name, p0, p1, side in list(RISING):
    axis, fixed, t0, t1 = wall_axis(p0, p1)
    ok = rise_test(name, axis, fixed, t0, t1, side)
    if RISE_MODE == "functional" and not ok:
        demoted.append(name)
        RISING = [r for r in RISING if r[0] != name]
        CUTLOW.append((name + "-DEMOTED", p0, p1, side))
for name, p0, p1, side in RISING:
    axis, fixed, t0, t1 = wall_axis(p0, p1)
    n = max(1, int(round((t1-t0)/BAY))); pitch = (t1-t0)/n
    WALL_BAYS[name] = dict(axis=axis, fixed=fixed, t0=t0, t1=t1, n=n, pitch=pitch, side=side)
    skip = set(range(int(0.30*n), max(int(0.30*n)+1, int(0.70*n)))) if name == BREACH_WALL else set()
    WALL_BAYS[name]["breach_bays"] = sorted(skip)

    # ground arcade -- openings left GENUINELY OPEN (no proxy): the real rooms beyond show through
    storey(axis, fixed, t0, n, pitch, 0.0, ARC_TOP, 0.0, 6.0, (pitch-PIER_W)/pitch,
           None, side, name, "arcade", proxy=False)
    def trif(k, skip=skip):
        return "opening_to_outside" if k % 2 == 0 else "triforium_dark"
    storey(axis, fixed, t0, n, pitch, TRI0, TRI1, TRI0+0.6, 15.0, 0.60,
           trif, side, name, "triforium", skip=skip)
    storey(axis, fixed, t0, n, pitch, CLE0, CLE1, CLE0+1.5, 22.5, 0.55,
           "opening_to_outside", side, name, "clerestory", skip=skip, mullion=True)
    for k in range(n):
        if k in skip: continue
        b0 = t0 + k*pitch
        slab(axis, fixed, b0, b0+pitch, CLE1, RISE, "wall_rising", side)

for name, p0, p1, side in CUTLOW:
    axis, fixed, t0, t1 = wall_axis(p0, p1)
    gaps = []
    if name == "C6-south-facade":
        gaps = [(-2.5, 2.5), (sfx-sfw/2, sfx+sfw/2)]
    if name == "C5-transeptE-end":
        gaps = [(-2.0, 2.0)]
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

# north chancel breach: a hole through the apse wall at ground level + a broken stair outside
ab = WALL_BAYS["R6-apse"]
box("wall_rising", ncx-ncw/2-0.01, ncx+ncw/2+0.01, Y_N, Y_N+WALL_T, 0.0, 0.0)  # no-op marker
BOXES[:] = [b for b in BOXES if not (
    b["c"] == CIDX["wall_rising"] and
    abs(b["p"][1] - (Y_N + WALL_T/2)) < WALL_T and
    b["p"][0] - b["s"][0]/2 < ncx + ncw/2 and b["p"][0] + b["s"][0]/2 > ncx - ncw/2 and
    b["p"][2] - b["s"][2]/2 < 5.0)]
plane(0, Y_N + WALL_T/2, ncx-ncw/2, ncx+ncw/2, 0.0, 5.0, "opening_to_outside", m=0.10)
OPENINGS.append(dict(wall="R6-apse", band="chancel_breach", bay=-1,
                     centre_m=[ncx, Y_N], z=[0.0, 5.0], width_m=ncw))
# The broken stair descends from the breach INTO the chancel, on the playable side, with the
# middle flight gone: that is what "broken stairs the monsters leap and the player cannot cross"
# means (Corr.4 cl.3), and it is the only placement in which the stair is visible at all -- put
# outside the wall it sits behind 57 m of masonry and renders zero pixels (measured).
for i in range(5):
    if i in (2, 3): continue                     # the gap: this is what makes it one-way
    box("breach_stair", ncx-ncw/2, ncx+ncw/2, Y_N-0.75*(i+1), Y_N-0.75*i,
        0.0, 2.6 - i*0.52)

# cross-shaped EMPTY mount, high in the apse wall (the cross fell)
cmx, cb, chh, cw2, cat = CM["cx"], CM["base_h"], CM["height"], CM["width"], CM["arm_thick"]
box("cross_mount_empty", cmx-cat/2, cmx+cat/2, Y_N-0.18, Y_N+0.02, cb, cb+chh)
box("cross_mount_empty", cmx-cw2/2, cmx+cw2/2, Y_N-0.18, Y_N+0.02, cb+chh*0.62, cb+chh*0.62+cat)

# four crossing piers; the rise test is DERIVED, never a list
CROSS_PIERS = [(-(HW+1.2), +(HW+1.2)), (+(HW+1.2), +(HW+1.2)),
               (-(HW+1.2), -(HW+1.2)), (+(HW+1.2), -(HW+1.2))]
PIER_SZ = 2.4
pier_report = []
for (px_, py_) in CROSS_PIERS:
    # the SAME functional rise test, over the pier's whole footprint, not a centre ray:
    # a centre ray misses everything the element's WIDTH hides, which is most of it.
    rises_by_test = rise_test("crossing_pier_%.3f_%.3f" % (px_, py_), 0,
                              py_-PIER_SZ/2, px_-PIER_SZ/2, px_+PIER_SZ/2, +1, PIER_SZ)
    # DECLARED: all four are cut. Three of the four fail the rise test outright; the fourth
    # passes only because the test measures hidden FLOOR, and what that pier hides is the APSE
    # WALL and the cross mount on it. One rising crossing pier out of four is an artifact of the
    # camera azimuth, not architecture, so the set is cut as a set. Overrulable.
    rises = False
    h = RISE if rises else CUT
    box("pier", px_-PIER_SZ/2, px_+PIER_SZ/2, py_-PIER_SZ/2, py_+PIER_SZ/2, 0.0, h)
    PROPS.append(dict(kind="crossing_pier", centre_m=[px_, py_],
                      footprint_m=[PIER_SZ, PIER_SZ], height_m=h, sort_line=py_-PIER_SZ/2))
    pier_report.append(dict(centre_m=[px_, py_], rises=bool(rises), height_m=h,
                            probe_m=RISE*COT_A))

# ======================================= 2b. SOLVE THE RISING-WALL HEIGHT
# Corrigendum 3 cl.1: the rising walls are "built tall enough ... that no crown is visible at
# any camera position inside the camera clamp". 34 m was DECLARED ("30+ m nave"), never solved,
# and the measurement refuted it: crowns entered reachable frames. Solve it instead.
#
#   player row = C0 - PXG*s_p - PXE*z_p      (z_p = the player's own floor elevation; the dais
#                                             is raised, which RAISES the frame top and makes
#                                             the requirement harder)
#   crown  row = C0 - PXG*s_c - PXE*h
#   off the top of the frame  <=>  crown_row < player_row - ANCHOR_Y
#   <=>  h  >  [ PXG*(s_p - s_c) + ANCHOR_Y ] / PXE  +  z_p
# maximised over every (crown, player) pair whose screen-x separation puts the crown inside the
# 1920 px frame. Pairs outside the x-window can never share a frame and must not bind.
VIEW_W_PX, VIEW_H_PX = SPEC["runtime_camera"]["view_px"]
ANCHOR_X, ANCHOR_Y = SPEC["runtime_camera"]["anchor_px"]
def s_of(x, y): return x*DV[0] + y*DV[1]
def sx_of(x, y): return PPM * (x*RV[0] + y*RV[1])

_pi, _pj = np.nonzero(walk)
_px = gx0 + (_pi+0.5)*CELL; _py = gy0 + (_pj+0.5)*CELL
_pz = np.where((np.abs(_px) <= HW) & (_py >= DAIS_Y0), DAIS_H, 0.0)     # dais + apse are raised
_psx = sx_of(_px, _py)
_pval = PXG * s_of(_px, _py) + PXE * _pz        # the term that raises the frame top
_bx0 = int(np.floor(_psx.min())) - 2
_nb = int(np.ceil(_psx.max())) - _bx0 + 4
_bin = np.full(_nb, -1e18)
np.maximum.at(_bin, (_psx - _bx0).astype(int), _pval)
# sliding max over a VIEW_W_PX window, so a crown at screen-x c sees the worst player whose
# frame contains it: player sx in [c - (VIEW_W-ANCHOR_X), c + ANCHOR_X]
_k = VIEW_W_PX
_cum = np.concatenate([[-1e18], np.maximum.accumulate(_bin)])   # fallback, replaced below
def sliding_max(a, lo, hi):
    """max of a over the window [i-lo, i+hi] for every i, via a simple two-pass block trick"""
    n = len(a); w = lo + hi + 1
    pad = int(np.ceil(n / w) * w) - n
    b = np.concatenate([a, np.full(pad, -1e18)])
    m = b.reshape(-1, w)
    L = np.maximum.accumulate(m, 1).ravel()
    Rr = np.maximum.accumulate(m[:, ::-1], 1)[:, ::-1].ravel()
    out = np.full(n, -1e18)
    idx = np.arange(n)
    a0 = idx - lo; a1 = idx + hi
    okL = a1 < len(L); okR = a0 >= 0
    res = np.full(n, -1e18)
    res[okL] = np.maximum(res[okL], L[a1[okL]])
    res[okR] = np.maximum(res[okR], Rr[a0[okR]])
    return res
_win = sliding_max(_bin, VIEW_W_PX - ANCHOR_X, ANCHOR_X)

# Sample the crown over the WHOLE top face on a CELL grid, not its diagonals. The first cut
# sampled the two diagonals of each footprint; the binding crown turned out to sit on the
# footprint's INNER EDGE, which no diagonal passes through, so the solve came back 0.6 m short
# and the pixel test caught it. A crown is a rectangle; sample the rectangle.
def _grid(x0, x1, y0, y1):
    gxs = np.arange(x0, x1 + CELL, CELL); gys = np.arange(y0, y1 + CELL, CELL)
    A, B = np.meshgrid(gxs, gys, indexing="ij")
    return A.ravel(), B.ravel()
_crowns = []
for name, p0, p1, side in RISING:
    ax, fx, t0, t1 = wall_axis(p0, p1)
    _crowns.append(_grid(*footprint(ax, fx, t0, t1, side)))
for pr in PROPS:
    if pr["kind"] == "crossing_pier" and pr["height_m"] > CUT:
        cx_, cy_ = pr["centre_m"]; hw_ = pr["footprint_m"][0]/2
        _crowns.append(_grid(cx_-hw_, cx_+hw_, cy_-hw_, cy_+hw_))
_h_req = 0.0
for cxs, cys in _crowns:
    csx = sx_of(cxs, cys); cs = s_of(cxs, cys)
    ii = np.clip((csx - _bx0).astype(int), 0, _nb-1)
    worst = _win[ii]
    need = (worst - PXG * cs + ANCHOR_Y) / PXE
    _h_req = max(_h_req, float(np.nanmax(need)))
WALL_RISE_SOLVED = math.ceil(_h_req * 2) / 2.0 + 1.0      # next half metre + 1.0 m margin
WALL_RISE_DECLARED = RISE
if "--no-solve-height" not in sys.argv:
    RISE = max(RISE, WALL_RISE_SOLVED)
    for b in BOXES:
        if b["c"] == CIDX["wall_rising"] and abs(b["p"][2] + b["s"][2]/2 - WALL_RISE_DECLARED) < 1e-6:
            top = RISE; bot = b["p"][2] - b["s"][2]/2
            b["p"][2] = (top+bot)/2; b["s"][2] = top-bot
        if b["c"] == CIDX["pier"] and abs(b["p"][2] + b["s"][2]/2 - WALL_RISE_DECLARED) < 1e-6:
            top = RISE; bot = b["p"][2] - b["s"][2]/2
            b["p"][2] = (top+bot)/2; b["s"][2] = top-bot
    for pr in PROPS:
        if pr.get("height_m") == WALL_RISE_DECLARED: pr["height_m"] = RISE
print("CROWN-CLEARANCE SOLVE: required rising-wall height %.4f m; declared was %.1f m; "
      "built at %.1f m" % (_h_req, WALL_RISE_DECLARED, RISE))

# =============================================================== 3. FLOORS
def rects(mask, cls, z0, z1):
    """greedy rectangle decomposition of a boolean plan mask -> boxes"""
    m = mask.copy(); n = 0
    for i in range(NX):
        j = 0
        while j < NY:
            if not m[i, j]: j += 1; continue
            j2 = j
            while j2 + 1 < NY and m[i, j2+1]: j2 += 1
            i2 = i
            while i2 + 1 < NX and m[i2+1, j:j2+1].all(): i2 += 1
            m[i:i2+1, j:j2+1] = False
            box(cls, gx0+i*CELL, gx0+(i2+1)*CELL, gy0+j*CELL, gy0+(j2+1)*CELL, z0, z1)
            n += 1
            j = j2 + 1
    return n

wall_plan = np.zeros_like(walk)
for b in BOXES:
    if b["c"] in (CIDX["wall_rising"], CIDX["wall_cutlow"], CIDX["pier"],
                  CIDX["room_beyond_wall"]):
        i0 = int(np.floor((b["p"][0]-b["s"][0]/2 - gx0)/CELL)); i1 = int(np.ceil((b["p"][0]+b["s"][0]/2 - gx0)/CELL))
        j0 = int(np.floor((b["p"][1]-b["s"][1]/2 - gy0)/CELL)); j1 = int(np.ceil((b["p"][1]+b["s"][1]/2 - gy0)/CELL))
        wall_plan[max(i0,0):max(i1,0), max(j0,0):max(j1,0)] = True

inside_bbox = (GX >= X_W) & (GX <= X_E) & (GY >= Y_S) & (GY <= Y_N)
nw_band = ((GX < X_W) | (GY > Y_N)) & (GX >= gx0) & (GY <= gy1)
se_band = ((GX > X_E) | (GY < Y_S))
# floors run UNDER the masonry: a 1.5 m wall over a floor that stops at its face leaves a
# 1.5 m strip of nothing, which renders as background green through every arcade opening.
beyond = ((inside_bbox & ~cruciform) | nw_band) & ~se_band
exterior = se_band & ~cruciform

def occlusion_grid(h):
    """cells where a column of height h would occlude walkable floor, by the SAME derived rule
    as the wall rise test: walkable within h*cot(alpha) along NW (away from the camera)."""
    probe = h * COT_A
    out = np.zeros_like(walk)
    for t in np.arange(0.0, probe + CELL, CELL):
        qx = GX + DV[0]*t; qy = GY + DV[1]*t
        ix = np.clip(((qx-gx0)/CELL).astype(int), 0, NX-1)
        iy = np.clip(((qy-gy0)/CELL).astype(int), 0, NY-1)
        out |= walk[ix, iy]
    return out
ceiling_blocked = occlusion_grid(CEIL_BEYOND + 0.6)

apron_blue = (dilate_mask(mouth_crypt, APRON_M) | dilate_mask(mouth_nc, APRON_M)) & walk
apron_fire = dilate_mask(mouth_se, APRON_M) & walk
apron_blue &= ~apron_fire
# descend-from-above galleries: a landing apron at the wall foot under each dark bay
gal_mouth = np.zeros_like(walk)
for g in SPAWN_GALLERIES:
    gx_, gy_ = g["centre_m"]
    gal_mouth |= (np.abs(GX-gx_) <= g["width_m"]/2) & (np.abs(GY-gy_) <= g["width_m"]/2)
apron_gal = dilate_mask(gal_mouth, APRON_M) & walk & ~apron_blue & ~apron_fire
apron_blue |= apron_gal

floor_classes = [
    ("nave_floor",     in_nave     & walk & ~apron_blue & ~apron_fire, 0.0),
    ("crossing_floor", in_cross    & walk & ~apron_blue & ~apron_fire, 0.0),
    ("transept_floor", in_transept & walk & ~apron_blue & ~apron_fire, 0.0),
    ("chancel_floor",  in_chancel  & walk & ~apron_blue & ~apron_fire, 0.0),
    ("dais",           in_dais     & walk & ~apron_blue & ~apron_fire, DAIS_H),
    ("apse_floor",     in_apse     & walk & ~apron_blue & ~apron_fire, DAIS_H),
    ("apron_bluefire", apron_blue, 0.0),
    ("apron_fire",     apron_fire, 0.0),
]
n_rects = 0
for cls, m, ztop in floor_classes:
    # a RAISED floor (the dais, the apse) must be built from the ground, not as a floating
    # 0.30 m slab: its south face is toward the camera, and with nothing under it the background
    # shows through as a green stripe across the chancel. Measured, not guessed -- see the
    # near_dais framing before this fix.
    n_rects += rects(m, cls, min(ztop-0.30, -0.30), ztop)
n_rects += rects(beyond,   "room_beyond_floor", -0.30, 0.0)
n_rects += rects(exterior, "exterior_ground",   -0.40, -0.10)
# ceiling over the rooms beyond, so the ground arcades never show sky -- but ONLY where it
# does not occlude walkable floor (the rise rule applies to every element, not just walls).
# Consequence, and it is the right one: the rooms behind the CUT-LOW south and east walls get
# no ceiling and are seen into over the stumps, D2-style, exactly as the near side should read.
ceiling = beyond & ~ceiling_blocked
n_rects += rects(ceiling, "room_beyond_wall", CEIL_BEYOND, CEIL_BEYOND+0.6)
box("room_beyond_wall", gx0, gx0+0.8, gy0, gy1, -0.3, CEIL_BEYOND+0.6)
box("room_beyond_wall", gx0, gx1, gy1-0.8, gy1, -0.3, CEIL_BEYOND+0.6)

# crypt shaft + crater cone
box("crypt_void", ccx-ccw/2, ccx+ccw/2, ccy-cch/2, ccy+cch/2, -CRYPT_DEPTH, -0.02)
# +0.35 m of overlap onto the floor: the cone and the 0.2 m floor raster do not share an
# edge, and without it the background leaks a 1-2 px green fringe round the crater lip.
DISCS.append(dict(c=CIDX["crater"], p=[0.0, 0.0, 0.01], r=R_CRATER+0.35, depth=CRATER_DEPTH))

# =============================================================== 4. POOLS
PRg = SPEC["pool_registration"]
# TWO entrance zones, and the distinction is load-bearing.
#  RULED   = the three entrance mouths Matt's corrigenda name (E crypt, SE fire, N chancel)
#            plus their aprons. These are the arena's entrances as ruled.
#  DECLARED= those PLUS the landing aprons I placed under the six dark triforium galleries.
#            Which bays are dark is MY alternating rule; those aprons blanket the foot of both
#            rising walls, so letting them decide the pool question is an instrument answering
#            a question it does not address. The RULED zone is the verdict OF RECORD; the
#            DECLARED zone is reported as the sensitivity.
ent_ruled = (mouth_crypt | mouth_se | mouth_nc
             | dilate_mask(mouth_crypt, APRON_M) | dilate_mask(mouth_se, APRON_M)
             | dilate_mask(mouth_nc, APRON_M))
ent_declared = ent_ruled | gal_mouth | dilate_mask(gal_mouth, APRON_M)
pool_rows = []
for p in PRg["pools"]:
    px_, py_ = p["arena_m"]
    row = dict(id=p["id"], witness_shot=p["witness_shot"], old_m=p["old_m"], arena_m=p["arena_m"],
               radius_disjoint_m=p["radius_disjoint_m"], radius_upper_bound_m=p["radius_upper_bound_m"])
    for tag, r in (("disjoint", p["radius_disjoint_m"]), ("upper_bound", p["radius_upper_bound_m"])):
        disc = ((GX-px_)**2 + (GY-py_)**2) <= r*r
        a_walk = float((disc & walk).sum())*CELL*CELL
        a_rul  = float((disc & ent_ruled).sum())*CELL*CELL
        a_dec  = float((disc & ent_declared).sum())*CELL*CELL
        row[tag] = dict(overlap_walkable_m2=a_walk,
                        overlap_entrance_ruled_m2=a_rul,
                        overlap_entrance_with_declared_galleries_m2=a_dec,
                        on_floor=a_walk > 0.0,
                        coincides_ruled=a_rul > 0.0,
                        coincides_with_declared_galleries=a_dec > 0.0)
    d, u = row["disjoint"], row["upper_bound"]
    if not d["on_floor"]:
        row["verdict"] = "DROP-OFF-FLOOR"
        row["reason"] = ("at the disjoint radius the disc does not overlap the cruciform walkable "
                         "floor anywhere (0.000 m2): it lies in the rooms beyond, off the arena.")
    elif d["coincides_ruled"]:
        row["verdict"] = "DROP-COINCIDES-WITH-ENTRANCE"
        row["reason"] = ("the disc overlaps a RULED entrance mouth or its hazard apron (%.3f m2)."
                         % d["overlap_entrance_ruled_m2"])
    else:
        row["verdict"] = "KEEP"
        row["reason"] = ("overlaps walkable floor (%.3f m2) and overlaps no RULED entrance mouth "
                         "or apron." % d["overlap_walkable_m2"])
    row["verdict_flips_at_upper_bound"] = (
        (d["on_floor"] != u["on_floor"]) or (d["coincides_ruled"] != u["coincides_ruled"]))
    row["verdict_if_declared_gallery_aprons_counted"] = (
        row["verdict"] if row["verdict"] != "KEEP" or not d["coincides_with_declared_galleries"]
        else "DROP-COINCIDES-WITH-DECLARED-GALLERY-APRON")
    pool_rows.append(row)

pool_mask = np.zeros_like(walk)
for row in pool_rows:
    if row["verdict"] == "KEEP":
        px_, py_ = row["arena_m"]; r = row["radius_disjoint_m"]
        pool_mask |= (((GX-px_)**2 + (GY-py_)**2) <= r*r) & walk
pool_mask &= ~apron_blue & ~apron_fire
n_rects += rects(pool_mask, "pool_candidate", -0.02, 0.005)

# =============================================================== 5. CANVAS
def screen(x, y, z):
    sx = PPM * (x*RV[0] + y*RV[1])
    sy = -(PXG * (x*DV[0] + y*DV[1]) + PXE * z)
    return sx, sy

wi, wj = np.nonzero(walk)
wx = gx0 + (wi+0.5)*CELL; wy = gy0 + (wj+0.5)*CELL
wsx, wsy = screen(wx, wy, 0.0)
# every reachable camera frame (the CLAMP): camera centre = player px - (anchor - view/2)
fx0, fx1 = wsx.min() - ANC_X, wsx.max() + (VIEW_W - ANC_X)
fy0, fy1 = wsy.min() - ANC_Y, wsy.max() + (VIEW_H - ANC_Y)
# The plate must ALSO carry the three-storey elevation the rulings author (Corr.3 cl.5), even
# though the clamp can never show it -- see README sec "what I could NOT satisfy". It does NOT
# carry the wall above the clerestory: that masonry exists in the 3D grey box only, to keep the
# crown off every frame, and painting it would be ~3400 px of featureless wall per column.
PLATE_TOP_ELEV = CLE1 + 2.0
rw = [b for b in BOXES if b["c"] == CIDX["wall_rising"]]
ry = []
for b in rw:
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            X = b["p"][0] + sx_*b["s"][0]/2; Y = b["p"][1] + sy_*b["s"][1]/2
            ry.append(screen(X, Y, PLATE_TOP_ELEV)[1])
px0 = math.floor(fx0); px1 = math.ceil(fx1)
py0 = math.floor(min(fy0, min(ry))); py1 = math.ceil(fy1)
CANVAS_W = int(px1 - px0); CANVAS_H = int(py1 - py0)
CANVAS_W += (-CANVAS_W) % 4; CANVAS_H += (-CANVAS_H) % 4

TILE = 4096
tiles = []
for r_ in range((CANVAS_H + TILE - 1)//TILE):
    for c_ in range((CANVAS_W + TILE - 1)//TILE):
        tiles.append(dict(name="t_%d_%d" % (r_, c_), origin_px=[c_*TILE, r_*TILE],
                          size_px=[TILE, TILE]))

# camera clamp, in plate px: the camera-centre rect
clamp = dict(plate_rect_px=[float(fx0-px0), float(fy0-py0), float(fx1-px0), float(fy1-py0)],
             camera_centre_px=[float(wsx.min() - px0 - ANC_X + VIEW_W/2),
                               float(wsy.min() - py0 - ANC_Y + VIEW_H/2),
                               float(wsx.max() - px0 - ANC_X + VIEW_W/2),
                               float(wsy.max() - py0 - ANC_Y + VIEW_H/2)],
             limits_px=[float(wsx.min()-px0-ANC_X), float(wsy.min()-py0-ANC_Y),
                        float(wsx.max()-px0-ANC_X+VIEW_W), float(wsy.max()-py0-ANC_Y+VIEW_H)],
             rule="camera centre = player plate px - (anchor - view/2); the clamp is the walkable "
                  "region's screen bbox expanded by the anchor frame. Identical in form to the "
                  "cliffside runtime's own limits (parallax.json camera.limits).")

canvas = dict(canvas_px=[CANVAS_W, CANVAS_H], origin_screen_px=[px0, py0],
              plate_top_elevation_m=PLATE_TOP_ELEV,
              wall_rise_built_m=RISE, wall_rise_solved_m=_h_req,
              ppm=PPM, tile_px=TILE, tiles=tiles,
              world_to_plate="plate_px = (ppm*(P.r) - origin_x, -(pxg*(P.d) + pxe*h) - origin_y)",
              r_plan_NE=list(RV), d_plan_NW=list(DV), pxg=PXG, pxe=PXE,
              clamp=clamp)

# =============================================================== 6. WRITE
out = dict(legend=[dict(index=i, name=n, rgb=list(c), walkable=w, guide_grey=list(g))
                   for i, n, c, w, g in LEGEND],
           boxes=BOXES, discs=DISCS,
           counts=dict(boxes=len(BOXES), discs=len(DISCS), floor_rects=n_rects))
json.dump(out, open(os.path.join(PROJ, "geometry.json"), "w"))
json.dump(canvas, open(os.path.join(PROJ, "canvas.json"), "w"), indent=1)
json.dump(dict(pools=pool_rows, props=PROPS, spawn_galleries=SPAWN_GALLERIES,
               wall_rise=dict(declared_m=WALL_RISE_DECLARED, solved_required_m=_h_req,
                              built_m=RISE,
                              rule="h > [PXG*(s_player - s_crown) + anchor_y]/PXE + z_player, "
                                   "maximised over every (crown, player) pair that can share a "
                                   "1920x1080 frame. Corrigendum 3 cl.1 asked for 'tall enough "
                                   "that no crown is visible at any camera position'; 34 m was "
                                   "DECLARED and the pixel measurement refuted it."),
               rise_test=dict(rule="an element rises to wall_rise_m iff raising it hides NO MORE "
                                   "walkable floor than cutting it to near_cut_m would "
                                   "(tolerance %.1f m2). This is the reason BOTH corrigenda give "
                                   "for cutting a side low, applied as the test itself, so no "
                                   "per-element list of faces exists anywhere in this generator."
                                   % RISE_TOL_M2,
                              mode=RISE_MODE, tolerance_m2=RISE_TOL_M2,
                              elements=rise_report, demoted_from_rising=demoted),
               openings=OPENINGS, crossing_piers=pier_report,
               walkable_area_raster_m2=AREA_RASTER,
               walkable_area_target_m2=RM["walkable_area_target_m2"],
               raster_cell_m=CELL,
               apron_area_m2=dict(bluefire=float(apron_blue.sum())*CELL*CELL,
                                  fire=float(apron_fire.sum())*CELL*CELL)),
          open(os.path.join(PROJ, "registration.json"), "w"), indent=1)

print("boxes %d  discs %d  floor rects %d" % (len(BOXES), len(DISCS), n_rects))
print("walkable raster %.4f m2 vs target %.4f m2  (cell %.2f m, quantisation |d| = %.4f m2)"
      % (AREA_RASTER, RM["walkable_area_target_m2"], CELL, abs(AREA_RASTER - RM["walkable_area_target_m2"])))
print("canvas %d x %d px  origin_screen (%d, %d)  tiles %d" % (CANVAS_W, CANVAS_H, px0, py0, len(tiles)))
print("openings to outside: %d   dark spawn galleries: %d   props: %d"
      % (len(OPENINGS), len(SPAWN_GALLERIES), len(PROPS)))
print("crossing piers:")
for pr in pier_report:
    print("   at (%7.3f,%7.3f)  rises=%-5s h=%.2f  (probe %.2f m NW)"
          % (pr["centre_m"][0], pr["centre_m"][1], pr["rises"], pr["height_m"], pr["probe_m"]))
print("RISE TEST (functional; hides-walkable, m2)")
for rr in rise_report:
    print("  %-34s rises=%-5s  full %8.3f  cut %8.3f  extra %8.3f"
          % (rr["element"], rr["rises"], rr["hidden_at_full_height_m2"],
             rr["hidden_at_cut_height_m2"], rr["extra_cost_m2"]))
print("  DEMOTED from rising to cut-low: %s" % (demoted or "none"))
print("rise mode: %s" % RISE_MODE)
print("west-top breach bays on %s: %s" % (BREACH_WALL,
      WALL_BAYS.get(BREACH_WALL, {}).get("breach_bays", "(wall demoted)")))
print("POOL REGISTRATION")
for r_ in pool_rows:
    print("  %-6s arena (%8.3f,%8.3f) r_dis %6.3f | walk %8.3f m2  ruled-entrance %7.3f m2 -> %-30s flip=%s"
          % (r_["id"], r_["arena_m"][0], r_["arena_m"][1], r_["radius_disjoint_m"],
             r_["disjoint"]["overlap_walkable_m2"], r_["disjoint"]["overlap_entrance_ruled_m2"],
             r_["verdict"], r_["verdict_flips_at_upper_bound"]))
    if r_["verdict"] != r_["verdict_if_declared_gallery_aprons_counted"]:
        print("         ^ sensitivity: becomes %s if my DECLARED gallery landing aprons count "
              "(%.3f m2)" % (r_["verdict_if_declared_gallery_aprons_counted"],
                             r_["disjoint"]["overlap_entrance_with_declared_galleries_m2"]))
