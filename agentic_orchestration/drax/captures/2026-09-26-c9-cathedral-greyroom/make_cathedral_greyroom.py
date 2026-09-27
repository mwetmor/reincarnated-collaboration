#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C-9 · P2' — THE CATHEDRAL GREY ROOM ON THE CRUCIBLE ARENA FOOTPRINT
===================================================================
Dispatch: agentic_orchestration/dispatches/2026-09-26-drax-c9-cathedral-greyroom.md
Charter:  agentic_orchestration/gandalf/notes/2026-09-26-illuminated-archive-run-C-9-charter.md
          (phase P2', Matt gate M2 — Matt approves this grey room BEFORE any paint)
Author:   drax (presentation seam), 2026-09-26.

WHAT THIS IS
------------
  The scene-builder-workflow § 3 step-1 grey room for the cathedral scene:
  a flat-shaded orthographic guide + depth map + ID mask + walkable mask
  (+ a DoT-zone mask, which the cliffside had no equivalent of), built on the
  MEASURED Crucible arena footprint, at the ratified camera.

  It paints NOTHING and fires no burst.

WHAT IS MEASURED AND WHAT IS DECLARED
-------------------------------------
  MEASURED (imported, never retyped):
    · the 177-vertex arena ring, the 4 interior obstructions, the 6 green-zone
      interior points and their radius UPPER BOUNDS
      -> galadriel/notes/crucible-arena-geometry-v1.json, sha-verified.
    · u = 0.285 m per native minimap px  (KC2-PLAY KP-6, ratified KP-9).
      The geometry file's OWN `scale` block (0.1981, DERIVED-WEAK) is IGNORED
      per dispatch § "Required reading" 4 / Gate-1 WARN-8.
    · alpha = 52.9535411256029 deg, the plate px/m figures, the Projection class
      -> imported from make_g_img_mock.py (KC2-PLAY W1), which is the wire.
  DERIVED HERE (from the measured geometry, no free parameters):
    · y_join, the crossing's north edge: the northernmost row whose largest
      single run of floor is >= 0.75 x the arena's widest run.
    · the screen passage's x-extent: the ring's own x-extent north of the
      lobes.
    · the choir band: the y-extent of the two long thin islands OB-1/OB-2.
    · the sanctuary: south floor within one bay of OB-3/OB-4.
    · BAY_M: half the measured screen-passage width (the Gothic double-bay
      relation read off the Antwerp plan -- the RATIO is declared, the LENGTH
      it multiplies is measured).
    · the chunk-grid origin: chosen by search to put the least walkable floor
      under the seams (brief § 4 "seams hide in dead space").
  DECLARED (no measurement exists; printed on the plate and in the manifest):
    · every metre figure in section 0 below.

Usage:  python3 make_cathedral_greyroom.py
        (run it under the shared heavy lock; it holds ~1 GB peak)
"""

import hashlib
import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.dirname(os.path.abspath(__file__))
COLLAB = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
CAPTURES = os.path.join(COLLAB, "agentic_orchestration", "drax", "captures")
G_IMG_DIR = os.path.join(CAPTURES, "2026-09-20-kc2-play-g-img")
BLOCKOUT_META = os.path.join(
    CAPTURES, "2026-09-13-cliffside-blockout", "blockout_meta_v2.json")

sys.path.insert(0, G_IMG_DIR)
import make_g_img_mock as mock                                    # noqa: E402


# ===========================================================================
# 0 · THE DECLARED NUMBERS.  Every one of these is a choice, not a decode.
# ===========================================================================

DECLARED = []


def declare(name, value, unit, why):
    DECLARED.append({"what": name, "value": value, "unit": unit, "why": why})
    return value


# -- the surround: how much cathedral is carried outside the arena ring ------
SUR_W = declare("surround_west", 10.0, "m",
                "aisle + outer wall + the first of the west chapels; the rest "
                "runs off the canvas edge (brief S 4 full-bleed).")
SUR_E = declare("surround_east", 10.0, "m", "as west.")
SUR_N = declare("surround_north", 7.0, "m",
                "the back wall exits the TOP edge (brief S 4), so it needs "
                "less room than the sides: it is cut, not framed.")
SUR_S = declare("surround_south", 10.0, "m",
                "the apse end: the radiating chapels need the most depth.")

# -- the section through the wall, measured outward from the measured ring ---
DADO_M = declare("dado_band", 1.2, "m",
                 "the choir-screen / parapet band standing ON the measured "
                 "ring line. It is WHY the ring is a boundary: a 0.9 m "
                 "parapet, not an invisible wall. INNER edge = the measured "
                 "ring and is load-bearing; outer edge is free.")
AISLE_M = declare("aisle_width", 4.5, "m",
                  "the aisle beyond the arcade. Dead space: the brief's "
                  "preferred home for vignette seams.")
WALLSKIN_M = declare("aisle_wall", 1.5, "m",
                     "the masonry skin between aisle and chapels.")
CHAPEL_HALF = declare("chapel_half_depth", 2.5, "m",
                      "radiating / side chapels, every other bay.")

PIER_W = declare("pier_width", 1.6, "m",
                 "arcade pier, square in plan, standing just outside the dado.")

NEAR_CUT_M = declare("near_cut_height", 0.9, "m",
                     "D2-style knee/waist break. Every camera-facing element "
                     "is cut here so it never occludes play space.")
RISE_M = declare("wall_rise", 6.0, "m",
                 "how far masonry rises up-screen before the canvas or the "
                 "cut takes it. REUSED, not invented: it is the wall-face "
                 "elevation allowance already ruled for THIS arena at "
                 "KC2-PLAY KP-18 (b).")

STALL_H_M = declare("choir_stall_height", 1.2, "m", "a stall back.")
ALTAR_H_M = declare("altar_height", 1.0, "m", "altar block.")
TOMB_H_M = declare("tomb_height", 0.9, "m", "table tomb.")

LANTERN_R_M = declare("lantern_radius", 9.0, "m",
                      "ANNOTATION ONLY, no footprint, no class. Marks where "
                      "the light falls so the crossing is the brightest and "
                      "calmest floor (brief S 4).")

BAY_RATIO = declare("bay_ratio", 0.5, "-",
                    "bay length / central-vessel width. Read as a PROPORTION "
                    "off the Antwerp plan (square aisle bays, the standard "
                    "Gothic double-bay relation). No metre figure is imported "
                    "from the plan -- it has no scale bar.")

CHUNK_W, CHUNK_H = 1536, 1024
OVERLAP = 256
STEP_W, STEP_H = CHUNK_W - OVERLAP, CHUNK_H - OVERLAP
WALKABLE_CLIP_PX = 24              # R-C3-58

EDT_DOWN = 2                       # distance transforms run at half res

# Nothing smaller than the ring's OWN measurement uncertainty is a feature:
# hard_boundary.uncertainty_native_px = 2.5.  Runs and gaps below this are
# rasterisation noise from drawing a native-px polygon at ~29x.
GRAIN_NATIVE_PX = 2.5


# ===========================================================================
# 1 · CLASSES
# ===========================================================================

CLASSES = [
    # name,              guide grey,  id rgb,            walkable
    ("outer_wall",        (58, 58, 62),   (17, 17, 17),   False),
    ("aisle_floor",       (130, 130, 134), (0, 116, 217),  False),
    ("chapel_floor",      (112, 112, 118), (0, 190, 200),  False),
    ("arcade_pier",       (80, 80, 86),   (255, 65, 54),  False),
    ("arcade_dado",       (96, 96, 102),  (255, 133, 27), False),
    ("screen_passage",    (203, 203, 199), (61, 153, 112), True),
    ("crossing",          (228, 228, 222), (46, 204, 64),  True),
    ("transept_w",        (210, 210, 205), (1, 255, 112),  True),
    ("transept_e",        (210, 210, 205), (127, 219, 255), True),
    ("choir_floor",       (214, 214, 209), (255, 220, 0),  True),
    ("sanctuary_floor",   (208, 208, 203), (240, 18, 190), True),
    ("ambulatory_floor",  (197, 197, 193), (177, 13, 201), True),
    ("choir_stall",       (118, 112, 100), (133, 20, 75),  False),
    ("altar",             (140, 136, 128), (255, 255, 255), False),
    ("tomb",              (126, 122, 116), (170, 170, 170), False),
    ("rot_zone",          (168, 172, 150), (0, 255, 0),    True),
    ("wall_face",         (44, 44, 48),   (85, 85, 85),   False),
]
IDX = {c[0]: i for i, c in enumerate(CLASSES)}
WALKABLE_IDX = [i for i, c in enumerate(CLASSES) if c[3]]

C_ANNO = (0, 255, 255)
C_ANNO_DIM = (0, 150, 150)
C_ANNO_WARM = (255, 190, 60)


# ===========================================================================
# 2 · PROJECTION + CANVAS
# ===========================================================================

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def projection_at_ppm(ppm, name, u):
    alpha = math.radians(mock.ALPHA_DEG)
    fraction = ppm * mock.H_FIG_M * math.cos(alpha) / mock.VIEW_H
    p = mock.Projection(fraction, name, u)
    assert abs(p.ppm - ppm) < 1e-9, "ppm round-trip failed"
    return p


class Canvas:
    """World-metre rect -> plate px.  +x = EAST, +y = SOUTH (the geometry
    file's own frame, no flip).  Square space is world-isotropic; plate space
    is square space squashed by sin(alpha) in y."""

    def __init__(self, proj, x0, x1, y0, y1):
        self.proj = proj
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.W = int(round((x1 - x0) * proj.ppm))
        self.H = int(round((y1 - y0) * proj.ppm * proj.sin_a))
        self.SW = self.W
        self.SH = int(round((y1 - y0) * proj.ppm))

    def sq(self, mx, my):
        return ((mx - self.x0) * self.proj.ppm,
                (my - self.y0) * self.proj.ppm)

    def px(self, mx, my):
        return ((mx - self.x0) * self.proj.ppm,
                (my - self.y0) * self.proj.ppm * self.proj.sin_a)

    def world_rect(self):
        return {"x_min_m": self.x0, "x_max_m": self.x1,
                "y_min_m": self.y0, "y_max_m": self.y1,
                "width_m": self.x1 - self.x0, "height_m": self.y1 - self.y0,
                "size_px": [self.W, self.H],
                "square_size_px": [self.SW, self.SH],
                "axes": "+x = EAST, +y = SOUTH (minimap frame, no flip)"}


def fill_poly(size, polys, value=1):
    img = Image.new("L", size, 0)
    dr = ImageDraw.Draw(img)
    for p in polys:
        dr.polygon(p, fill=value)
    return np.asarray(img) > 0


def up(mask_small, size):
    """NEAREST-upsample a small array to (W, H)."""
    return np.asarray(Image.fromarray(mask_small).resize(size, Image.NEAREST))


def _running_union(mask, steps, up):
    """Union of `mask` shifted 1..steps rows.  up=True shifts UP-SCREEN
    (out[y] = any mask[y+s]); up=False shifts DOWN (out[y] = any mask[y-s]).

    Written as a carried single-row shift rather than a scipy filter: the
    one-sided window this needs cannot be expressed as a maximum_filter1d
    origin (scipy rejects an origin outside the kernel), and a two-sided
    filter answers the WRONG QUESTION while returning cleanly.  The
    self-test below exists because the first cut of this function did
    exactly that."""
    out = np.zeros(mask.shape, dtype=bool)
    if steps <= 0 or not mask.any():
        return out
    cur = mask.copy()
    buf = np.empty_like(cur)
    for _ in range(steps):
        if up:
            buf[:-1, :] = cur[1:, :]
            buf[-1, :] = False
        else:
            buf[1:, :] = cur[:-1, :]
            buf[0, :] = False
        cur, buf = buf, cur
        out |= cur
    return out & ~mask


def sweep_up(mask, steps):
    """Union of `mask` displaced up-screen 1..steps rows (an elevation)."""
    return _running_union(mask, steps, up=True)


def shadow_south(mask, steps):
    """True where `mask` lies within `steps` rows NORTH (smaller y) —
    i.e. where rising by `steps` would occlude `mask`."""
    return _running_union(mask, steps, up=False)


def _sweep_selftest():
    m = np.zeros((9, 3), dtype=bool)
    m[5, 1] = True
    s = sweep_up(m, 2)
    assert s[3, 1] and s[4, 1] and not s[5, 1] and not s[2, 1], \
        "sweep_up does not sweep up-screen"
    t = shadow_south(m, 2)
    assert t[6, 1] and t[7, 1] and not t[4, 1], \
        "shadow_south does not look north"


# ===========================================================================
# 3 · BUILD
# ===========================================================================

def main():
    t0 = time.time()
    _sweep_selftest()

    geom = mock.load_geometry()
    geom_sha = sha256_of(mock.GEOM_PATH)
    u = mock.U_REGISTERED
    hb = geom["hard_boundary"]

    with open(BLOCKOUT_META) as fh:
        oc = json.load(fh)["ortho_canvas_v2"]
    ppm = oc["px_per_m_screen_x"]
    # DEBUG ONLY: C9_PPM_SCALE runs the whole pipeline at a fraction of the
    # plate scale so the logic can be exercised without 58 Mpx of memory.
    # Anything it writes is NOT a deliverable; the plate-law cross-check below
    # is skipped, which is exactly how you can tell.
    dbg = float(os.environ.get("C9_PPM_SCALE", "1") or 1)
    ppm *= dbg
    proj = projection_at_ppm(ppm, "PLATE", u)

    # free cross-check: the cliffside plate's independently-ruled px/m pair
    # must fall out of alpha.  If it does not, this canvas is not the ratified
    # camera and nothing below is meaningful.
    a = math.radians(mock.ALPHA_DEG)
    for label, got, want in (
            ("ground depth", ppm * math.sin(a), oc["px_per_ground_m_screen_y"]),
            ("vertical", ppm * math.cos(a), oc["px_per_vertical_m_screen_y"])):
        if dbg != 1.0:
            print("[camera] DEBUG ppm scale %.4f — cross-check SKIPPED, "
                  "outputs are NOT deliverables" % dbg)
            break
        if abs(got - want) >= 1e-6:
            sys.exit("PLATE CROSS-CHECK FAILED (%s): %.10f vs %.10f"
                     % (label, got, want))
    print("[camera] alpha %.10f deg   ppm %.6f px/m east   %.6f px/m south "
          "ground   %.6f px/m up-screen"
          % (mock.ALPHA_DEG, ppm, ppm * math.sin(a), ppm * math.cos(a)))

    # ---- canvas -----------------------------------------------------------
    bx0, by0, bx1, by1 = [v * u for v in hb["bbox_native"]]
    cv = Canvas(proj, bx0 - SUR_W, bx1 + SUR_E, by0 - SUR_N, by1 + SUR_S)
    print("[canvas] %d x %d px   world %.3f x %.3f m   arena %.3f x %.3f m"
          % (cv.W, cv.H, cv.x1 - cv.x0, cv.y1 - cv.y0, bx1 - bx0, by1 - by0))

    SQ = (cv.SW, cv.SH)

    def nsq(v):
        return cv.sq(v[0] * u, v[1] * u)

    # ---- the measured floor ----------------------------------------------
    ring = [nsq(v) for v in hb["outer_ring"]["vertices_native"]]
    inside = fill_poly(SQ, [ring])
    obs = {}
    for ob in hb["interior_obstructions"]:
        obs[ob["id"]] = fill_poly(SQ, [[nsq(v) for v in ob["vertices_native"]]])
    islands = np.zeros(SQ[::-1], dtype=bool)
    for m in obs.values():
        islands |= m
    floor = inside & ~islands

    # ---- derived region cuts ---------------------------------------------
    # Row structure, computed ONCE.  Runs shorter than one NATIVE minimap pixel
    # and gaps narrower than one native pixel are noise from rasterising a
    # native-px polygon at 28.7x: the ring is measured to +-2.5 native px
    # (hard_boundary.uncertainty_native_px), so nothing below that scale is a
    # feature.  Without this filter the very first row of the arena reports
    # TWO runs from a sub-pixel notch at the top vertex.
    grain = max(3, int(round(GRAIN_NATIVE_PX * ppm * u)))
    rowmax = np.zeros(SQ[1], dtype=np.int32)
    rowsum = inside.sum(axis=1).astype(np.int32)
    for r in range(SQ[1]):
        row = inside[r]
        if not row.any():
            continue
        e = np.flatnonzero(np.diff(np.concatenate(
            ([0], row.view(np.int8), [0]))))
        st, en = e[0::2], e[1::2]
        merged = []
        for s_, e_ in zip(st, en):
            if merged and s_ - merged[-1][1] < grain:
                merged[-1][1] = e_
            else:
                merged.append([s_, e_])
        merged = [m for m in merged if m[1] - m[0] >= grain]
        if merged:
            rowmax[r] = max(m[1] - m[0] for m in merged)

    # the corridor head: the arena's northernmost row of real floor
    head_row_sq = int(np.flatnonzero(rowmax > 0)[0])
    head_x_sq = float(np.flatnonzero(inside[head_row_sq]).mean())

    # y_join: northernmost row whose widest single run of floor reaches 75 % of
    # the arena's widest run.  ("the transept arms have joined the passage")
    thr = 0.75 * rowmax.max()
    y_join_px = int(np.flatnonzero(rowmax >= thr)[0])
    y_join_m = cv.y0 + y_join_px / ppm

    # the screen passage's x-extent = the ring's own x-extent over the rows
    # that are CORRIDOR ONLY: north of the join, and carrying no floor beyond
    # their own widest run (rowsum ~ rowmax).  A row that also holds a lobe
    # carries more floor than its widest run does, and drops out.
    corridor = (np.arange(SQ[1]) < y_join_px) & (rowmax > 0) & \
               (rowsum <= 1.05 * rowmax)
    if not corridor.any():
        sys.exit("no corridor-only rows found — the passage rule failed")
    cols = np.flatnonzero(inside[corridor].any(axis=0))
    pass_x0_m = cv.x0 + cols.min() / ppm
    pass_x1_m = cv.x0 + (cols.max() + 1) / ppm
    vessel_w = pass_x1_m - pass_x0_m
    BAY_M = BAY_RATIO * vessel_w
    print("[derived] y_join %.3f m   screen passage x %.3f .. %.3f m "
          "(vessel %.3f m)   BAY %.4f m"
          % (y_join_m, pass_x0_m, pass_x1_m, vessel_w, BAY_M))

    # the choir band = the y-extent of the two long thin islands
    stall_ids = ["OB-1", "OB-2"]
    sanct_ids = ["OB-3", "OB-4"]
    by_id = {o["id"]: o for o in hb["interior_obstructions"]}
    sy = [v[1] * u for i in stall_ids for v in by_id[i]["vertices_native"]]
    choir_y0_m, choir_y1_m = min(sy), max(sy)
    print("[derived] choir band y %.3f .. %.3f m" % (choir_y0_m, choir_y1_m))

    yy = np.arange(SQ[1])[:, None] / ppm + cv.y0
    xx = np.arange(SQ[0])[None, :] / ppm + cv.x0

    north = floor & (yy < y_join_m)
    idx = np.zeros(SQ[::-1], dtype=np.uint8)          # default = outer_wall(0)
    idx[floor] = IDX["ambulatory_floor"]
    idx[floor & (yy >= choir_y0_m) & (yy <= choir_y1_m)] = IDX["choir_floor"]
    idx[floor & (yy >= y_join_m) & (yy < choir_y0_m)] = IDX["crossing"]
    idx[north] = IDX["screen_passage"]
    idx[north & (xx < pass_x0_m)] = IDX["transept_w"]
    idx[north & (xx > pass_x1_m)] = IDX["transept_e"]

    # sanctuary = south floor within ONE BAY of the altar/tomb footprints
    sanct_foot = np.zeros(SQ[::-1], dtype=bool)
    for i in sanct_ids:
        sanct_foot |= obs[i]
    small = ~sanct_foot[::EDT_DOWN, ::EDT_DOWN]
    d_small = ndimage.distance_transform_edt(small) * EDT_DOWN / ppm
    near_sanct = up((d_small <= BAY_M).astype(np.uint8), SQ) > 0
    del small, d_small
    idx[floor & (yy > choir_y1_m) & near_sanct] = IDX["sanctuary_floor"]
    del near_sanct

    # ---- the fabric outside the ring --------------------------------------
    small = (~inside)[::EDT_DOWN, ::EDT_DOWN]
    d_small = ndimage.distance_transform_edt(small) * EDT_DOWN / ppm
    band_small = np.digitize(
        d_small, [DADO_M, DADO_M + AISLE_M,
                  DADO_M + AISLE_M + WALLSKIN_M]).astype(np.uint8)
    band = up(band_small, SQ)
    del small, d_small, band_small
    out = ~inside
    idx[out & (band == 0)] = IDX["arcade_dado"]
    idx[out & (band == 1)] = IDX["aisle_floor"]
    idx[out & (band == 2)] = IDX["outer_wall"]
    idx[out & (band == 3)] = IDX["outer_wall"]
    del band

    # ---- bay stations: piers every bay, chapels every other bay -----------
    verts = [(v[0] * u, v[1] * u) for v in hb["outer_ring"]["vertices_native"]]
    verts.append(verts[0])
    seglen = [math.dist(verts[i], verts[i + 1]) for i in range(len(verts) - 1)]
    total = sum(seglen)
    n_bays = max(8, int(round(total / BAY_M)))
    bay_actual = total / n_bays

    stations = []
    cum, si, acc = 0.0, 0, 0.0
    for k in range(n_bays):
        s = k * bay_actual
        while si < len(seglen) - 1 and acc + seglen[si] < s:
            acc += seglen[si]
            si += 1
        t = (s - acc) / max(seglen[si], 1e-9)
        p = verts[si]
        q = verts[si + 1]
        pt = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
        tx, ty = q[0] - p[0], q[1] - p[1]
        L = math.hypot(tx, ty) or 1.0
        tx, ty = tx / L, ty / L
        n1 = (-ty, tx)
        # outward = the normal whose 0.6 m probe lands OUTSIDE the floor
        probe = cv.sq(pt[0] + n1[0] * 0.6, pt[1] + n1[1] * 0.6)
        pxi, pyi = int(probe[0]), int(probe[1])
        insidep = (0 <= pxi < SQ[0] and 0 <= pyi < SQ[1]
                   and inside[pyi, pxi])
        n = (-n1[0], -n1[1]) if insidep else n1
        stations.append({"k": k, "pt_m": pt, "n": n, "tan": (tx, ty)})
    print("[bays] ring %.3f m   %d bays of %.4f m" % (total, n_bays, bay_actual))

    def rect_poly(c, n, t, half_along, half_out, out0):
        cx = c[0] + n[0] * (out0 + half_out)
        cy = c[1] + n[1] * (out0 + half_out)
        pts = []
        for sa, so in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
            pts.append(cv.sq(cx + t[0] * sa * half_along + n[0] * so * half_out,
                             cy + t[1] * sa * half_along + n[1] * so * half_out))
        return pts

    piers, chapels = [], []
    for st in stations:
        piers.append(rect_poly(st["pt_m"], st["n"], st["tan"],
                               PIER_W / 2, PIER_W / 2, DADO_M))
        if st["k"] % 2 == 0:
            chapels.append(rect_poly(
                st["pt_m"], st["n"], st["tan"], BAY_M * 0.42, CHAPEL_HALF,
                DADO_M + AISLE_M + WALLSKIN_M))
    chapel_m = fill_poly(SQ, chapels) & out
    idx[chapel_m] = IDX["chapel_floor"]
    del chapel_m
    pier_m = fill_poly(SQ, piers) & out
    idx[pier_m] = IDX["arcade_pier"]
    del pier_m

    # ---- furniture ---------------------------------------------------------
    idx[obs["OB-1"]] = IDX["choir_stall"]
    idx[obs["OB-2"]] = IDX["choir_stall"]
    idx[obs["OB-3"]] = IDX["altar"]
    idx[obs["OB-4"]] = IDX["tomb"]

    # ---- the six DoT zones -------------------------------------------------
    # PROVENANCE: interior point MEASURED, extent UNMEASURED.  The radius in the
    # geometry file is an UPPER BOUND, not a measurement, so the disc is an
    # upper bound too.  Clipped to the floor; islands removed.
    zones = geom["green_zones"]["zones"]
    rot_full = np.zeros(SQ[::-1], dtype=bool)
    zrows = []
    for z in zones:
        cx, cy = nsq(z["interior_point_minimap_px"])
        r = z["radius_upper_bound_px"] * u * ppm
        m = fill_poly(SQ, [mock.ellipse_pts(cx, cy, r, r, 256)])
        rot_full |= m
        zrows.append({
            "id": z["id"], "witness_shot": z["witness_shot"],
            "interior_point_native_px": z["interior_point_minimap_px"],
            "interior_point_m": [z["interior_point_minimap_px"][0] * u,
                                 z["interior_point_minimap_px"][1] * u],
            "radius_upper_bound_native_px": z["radius_upper_bound_px"],
            "radius_upper_bound_m": z["radius_upper_bound_px"] * u,
            "radius_upper_bound_plate_px": r,
        })
    rot_full &= floor

    # the DISJOINT-PRESERVING scale.  The geometry file DEMONSTRATES six
    # mutually distinct zones; at the raw upper bounds the discs overlap, which
    # contradicts that.  k_disjoint is the largest uniform scale at which all
    # six stay pairwise disjoint -- a DERIVED number, not a taste number.
    k_disjoint = min(
        math.dist(p["interior_point_native_px"], q["interior_point_native_px"])
        / (p["radius_upper_bound_native_px"] + q["radius_upper_bound_native_px"])
        for i, p in enumerate(zrows) for q in zrows[i + 1:])
    rot_dis = np.zeros(SQ[::-1], dtype=bool)
    for z, row in zip(zones, zrows):
        cx, cy = nsq(z["interior_point_minimap_px"])
        r = row["radius_upper_bound_plate_px"] * k_disjoint
        rot_dis |= fill_poly(SQ, [mock.ellipse_pts(cx, cy, r, r, 256)])
        row["radius_disjoint_m"] = row["radius_upper_bound_m"] * k_disjoint
    rot_dis &= floor
    frac_full = rot_full.sum() / floor.sum()
    frac_dis = rot_dis.sum() / floor.sum()
    print("[rot] upper-bound discs cover %.1f %% of walkable floor; "
          "k_disjoint %.4f covers %.1f %%"
          % (100 * frac_full, k_disjoint, 100 * frac_dis))

    # WHICH DISC THE GUIDE AND THE ID MASK CARRY.
    # The raw upper bound is not an estimate -- it is a bound, and painting to
    # it over-paints by construction.  It also contradicts the file's OWN
    # finding: six MUTUALLY DISTINCT zones are demonstrated, and at the raw
    # bound the discs overlap.  k_disjoint is the largest scale consistent with
    # BOTH facts, so the guide, the ID mask and the primary DoT mask carry it;
    # the raw bound ships beside them as the ENVELOPE ("the rot is inside this,
    # nowhere else").  Flagged to M2: Matt may overrule either way.

    # ---- squash to plate space ---------------------------------------------
    def squash(arr):
        return np.asarray(Image.fromarray(arr).resize(
            (cv.W, cv.H), Image.NEAREST)).copy()

    idx[rot_dis] = IDX["rot_zone"]
    idxp = squash(idx)
    walk_sq = np.isin(idx, WALKABLE_IDX)
    walkp = squash(walk_sq.astype(np.uint8)) > 0
    rot_fullp = squash(rot_full.astype(np.uint8)) > 0
    rot_disp = squash(rot_dis.astype(np.uint8)) > 0
    ring_px = [cv.px(v[0] * u, v[1] * u)
               for v in hb["outer_ring"]["vertices_native"]]
    del idx, walk_sq, rot_full, rot_dis, inside, out, floor, islands, north
    del yy, xx

    # ---- elevation + the near-side cut -------------------------------------
    rise_px = int(round(RISE_M * ppm * proj.cos_a))
    near_px = int(round(NEAR_CUT_M * ppm * proj.cos_a))
    masonry = (idxp == IDX["arcade_pier"]) | (idxp == IDX["outer_wall"])
    # An element is CUT LOW iff raising it would occlude walkable floor:
    # i.e. iff walkable floor lies within rise_px NORTH of it.  Up-screen is
    # north, so this makes the near (south) side cut itself, with no list of
    # faces anywhere in this file.
    # The test is run against the play space AND the ground that reads as its
    # edge (dado + aisle), not against the walkable mask alone: a 6 m wall
    # that stops one pixel short of the floor still puts a wall between the
    # camera and the floor's edge, which is the thing brief S 4 forbids.
    seen = walkp | (idxp == IDX["arcade_dado"]) | (idxp == IDX["aisle_floor"])
    cut_low = masonry & shadow_south(seen, rise_px)
    del seen
    tall = masonry & ~cut_low
    print("[cut] masonry %d px   cut low %d px (%.1f %%)   tall %d px"
          % (masonry.sum(), cut_low.sum(),
             100.0 * cut_low.sum() / max(masonry.sum(), 1), tall.sum()))

    elev = np.zeros((cv.H, cv.W), dtype=np.uint16)
    elev[idxp == IDX["choir_stall"]] = int(STALL_H_M * 1000)
    elev[idxp == IDX["altar"]] = int(ALTAR_H_M * 1000)
    elev[idxp == IDX["tomb"]] = int(TOMB_H_M * 1000)
    elev[idxp == IDX["arcade_dado"]] = int(NEAR_CUT_M * 1000)

    face = np.zeros((cv.H, cv.W), dtype=bool)
    for mask, steps, h_m in ((tall, rise_px, RISE_M),
                             (cut_low, near_px, NEAR_CUT_M),
                             (idxp == IDX["arcade_dado"], near_px, NEAR_CUT_M),
                             (idxp == IDX["choir_stall"],
                              int(round(STALL_H_M * ppm * proj.cos_a)),
                              STALL_H_M)):
        if not mask.any() or steps <= 0:
            continue
        # ascending sweep, one row at a time, carrying the shifted mask
        # forward.  Ascending overwrite means a pixel keeps the HIGHEST
        # surface above it, for free.
        cur = mask.copy()
        buf = np.empty_like(cur)
        keep = ~mask
        for s in range(1, steps + 1):
            buf[:-1, :] = cur[1:, :]
            buf[-1, :] = False
            cur, buf = buf, cur
            sh = cur & keep
            mm = int(round(h_m * 1000.0 * s / steps))
            face |= sh
            elev[sh] = mm
        del cur, buf, keep
    idxp[face & ~masonry] = IDX["wall_face"]
    idxp[face & masonry] = IDX["wall_face"]
    elev[masonry & ~face] = 0
    del masonry, tall, cut_low, face

    # the sweep must never eat walkable floor
    bled = int((np.isin(idxp, [IDX["wall_face"]]) & walkp).sum())
    if bled:
        # a cut-low element's 0.9 m face may legitimately overhang the floor
        # edge (the D2 convention); report it, never silently allow drift.
        print("[cut] wall_face over walkable floor: %d px (%.4f %% of floor) "
              "-- cut-low overhang, expected" % (bled, 100.0 * bled / walkp.sum()))

    # ---- walkable mask (R-C3-58 clip) --------------------------------------
    walk_out = walkp.copy()
    walk_out[:WALKABLE_CLIP_PX, :] = False
    walk_out[-WALKABLE_CLIP_PX:, :] = False
    walk_out[:, :WALKABLE_CLIP_PX] = False
    walk_out[:, -WALKABLE_CLIP_PX:] = False
    clipped = int(walkp.sum() - walk_out.sum())

    # ---- chunk grid: origin chosen to keep seams off walkable floor --------
    # NOTE the names: `rowsum` above is SQUARE space over `inside`, this one is
    # PLATE space over `walkp`.  They are different lengths and mean different
    # things; the first cut of this block indexed the wrong one and the search
    # still ran clean, because plate H < square H so every index was in bounds.
    colsum_w = walkp.sum(axis=0)
    rowsum_w = walkp.sum(axis=1)
    assert len(colsum_w) == cv.W and len(rowsum_w) == cv.H
    # The search may NOT buy a better seam with an extra chunk: an extra column
    # or row is 10-11 more paint calls per style arm.  Lock the grid to the
    # minimum that covers the canvas, then move the origin inside that.
    NCOL_MIN = int(math.ceil((cv.W - OVERLAP) / STEP_W))
    NROW_MIN = int(math.ceil((cv.H - OVERLAP) / STEP_H))
    OX_MAX = NCOL_MIN * STEP_W + OVERLAP - cv.W
    OY_MAX = NROW_MIN * STEP_H + OVERLAP - cv.H
    best = None
    for ox in range(0, max(OX_MAX, 0) + 1, 16):
        ncol = NCOL_MIN
        seam_x = [c * STEP_W - ox for c in range(1, ncol)]
        seam_x += [s + CHUNK_W - 1 for s in
                   [c * STEP_W - ox for c in range(0, ncol - 1)]]
        cx = sum(int(colsum_w[s]) for s in seam_x if 0 <= s < cv.W)
        for oy in range(0, max(OY_MAX, 0) + 1, 16):
            nrow = NROW_MIN
            seam_y = [r * STEP_H - oy for r in range(1, nrow)]
            seam_y += [s + CHUNK_H - 1 for s in
                       [r * STEP_H - oy for r in range(0, nrow - 1)]]
            cy = sum(int(rowsum_w[s]) for s in seam_y if 0 <= s < cv.H)
            tot = cx + cy
            if best is None or tot < best[0]:
                best = (tot, ox, oy, ncol, nrow)
    seam_cost, OX, OY, NCOL, NROW = best
    seam_cost_at_zero = (
        sum(int(colsum_w[s]) for c in range(1, NCOL_MIN)
            for s in (c * STEP_W, c * STEP_W + CHUNK_W - 1 - STEP_W)
            if 0 <= s < cv.W)
        + sum(int(rowsum_w[s]) for r in range(1, NROW_MIN)
              for s in (r * STEP_H, r * STEP_H + CHUNK_H - 1 - STEP_H)
              if 0 <= s < cv.H))
    print("[chunks] %d x %d = %d chunks   origin offset (-%d, -%d)   "
          "seam-on-walkable %d px (vs %d at offset 0)"
          % (NCOL, NROW, NCOL * NROW, OX, OY, seam_cost, seam_cost_at_zero))

    chunks = []
    for r in range(NROW):
        for c in range(NCOL):
            ox_, oy_ = c * STEP_W - OX, r * STEP_H - OY
            x0c, y0c = max(ox_, 0), max(oy_, 0)
            x1c = min(ox_ + CHUNK_W, cv.W)
            y1c = min(oy_ + CHUNK_H, cv.H)
            if x1c <= x0c or y1c <= y0c:
                continue
            sub = walkp[y0c:y1c, x0c:x1c]
            chunks.append({
                "chunk": "cath_%d_%d" % (r, c),
                "index": [r, c],
                "origin_px": [ox_, oy_],
                "size_px": [CHUNK_W, CHUNK_H],
                "on_canvas_rect_px": [x0c, y0c, x1c - x0c, y1c - y0c],
                "walkable_fraction": round(float(sub.mean()), 4),
                "world_rect_m": {
                    "x_min": cv.x0 + ox_ / ppm,
                    "x_max": cv.x0 + (ox_ + CHUNK_W) / ppm,
                    "y_min": cv.y0 + oy_ / (ppm * proj.sin_a),
                    "y_max": cv.y0 + (oy_ + CHUNK_H) / (ppm * proj.sin_a)},
            })

    # class centroids + pixel counts, so downstream tools (the M2 review
    # composer) never need the raw index array on disk.
    stats = {}
    for i, (name, _g, _c, _wk) in enumerate(CLASSES):
        m = idxp == i
        n = int(m.sum())
        if not n:
            stats[name] = {"px": 0}
            continue
        ys, xs = np.nonzero(m)
        stats[name] = {"px": n,
                       "centroid_px": [float(xs.mean()), float(ys.mean())],
                       "area_m2": n / (ppm * ppm * math.sin(a))}
        del ys, xs, m

    # ---- emit ---------------------------------------------------------------
    outdir = os.path.join(ROOT, "_debug") if dbg != 1.0 else ROOT
    os.makedirs(outdir, exist_ok=True)
    guide_lut = np.zeros((len(CLASSES), 3), dtype=np.uint8)
    id_lut = np.zeros((len(CLASSES), 3), dtype=np.uint8)
    for i, (_, g, c, _w) in enumerate(CLASSES):
        guide_lut[i] = g
        id_lut[i] = c

    def w(name, img):
        p = os.path.join(outdir, name)
        img.save(p)
        return {"file": name, "sha256": sha256_of(p),
                "bytes": os.path.getsize(p), "size_px": list(img.size)}

    outputs = {}
    outputs["id_mask.png"] = w("id_mask.png",
                               Image.fromarray(id_lut[idxp], "RGB"))
    outputs["depth_mm.png"] = w(
        "depth_mm.png", Image.fromarray(elev.astype("<u2"), mode="I;16"))
    outputs["walkable_mask.png"] = w(
        "walkable_mask.png",
        Image.fromarray((walk_out * 255).astype(np.uint8), "L"))
    outputs["dot_zone_mask.png"] = w(
        "dot_zone_mask.png",
        Image.fromarray((rot_disp * 255).astype(np.uint8), "L"))
    outputs["dot_zone_mask_upper_bound.png"] = w(
        "dot_zone_mask_upper_bound.png",
        Image.fromarray((rot_fullp * 255).astype(np.uint8), "L"))

    # the painter's guide: flat grey + annotation
    guide = Image.fromarray(guide_lut[idxp], "RGB")
    dr = ImageDraw.Draw(guide)
    # rot hatch
    arr = np.asarray(guide).copy()
    hatch = Image.new("L", guide.size, 0)
    hd = ImageDraw.Draw(hatch)
    pitch = max(10, int(round(ppm * 0.45)))
    for c in range(-guide.height, guide.width, pitch):
        hd.line([(c, 0), (c + guide.height, guide.height)], fill=255, width=3)
    h = (np.asarray(hatch) > 0) & (idxp == IDX["rot_zone"])
    arr[h] = (124, 132, 104)
    guide = Image.fromarray(arr, "RGB")
    del arr, h, hatch
    dr = ImageDraw.Draw(guide)

    lw = max(4, int(round(ppm / 18.0)))
    walked, unw = mock.split_ring(ring_px, hb["unwalked_arcs"], len(ring_px))
    for run in walked:
        dr.line(run, fill=C_ANNO, width=lw)
    for run in unw:
        mock.dashed_path(dr, run, C_ANNO, lw, dash=lw * 9, gap=lw * 7)
    ox0, oy0 = cv.px(0.0, 0.0)
    bxr, byr = proj.r_to_semiaxes(LANTERN_R_M)

    # the rot ENVELOPE: the raw upper bound, drawn as a line, not a fill.
    # The painter fills to the hatched disc; nothing rots outside this line.
    for z in zones:
        zx, zy = cv.px(z["interior_point_minimap_px"][0] * u,
                       z["interior_point_minimap_px"][1] * u)
        rr = z["radius_upper_bound_px"] * u * ppm
        mock.dashed_path(dr, mock.ellipse_pts(zx, zy, rr, rr * proj.sin_a, 400),
                         (120, 220, 90), max(2, lw // 2),
                         dash=lw * 5, gap=lw * 5)

    # the choir screen: a line across the passage at the join.  ANNOTATION —
    # it is painted as an arch OVER the passage (Overhead, z3) and has no
    # footprint, because a screen with a doorway would punch a hole in the
    # walkable mask.
    sy_px = cv.px(0.0, y_join_m)[1]
    mock.dashed_path(dr, [(cv.px(pass_x0_m, y_join_m)[0], sy_px),
                          (cv.px(pass_x1_m, y_join_m)[0], sy_px)],
                     C_ANNO_WARM, lw, dash=lw * 4, gap=lw * 3)

    # lantern is centred on the CROSSING centroid, not the origin
    cr = (idxp == IDX["crossing"])
    cys, cxs = np.nonzero(cr)
    lcx, lcy = float(cxs.mean()), float(cys.mean())
    del cr, cys, cxs
    mock.dashed_path(dr, mock.ellipse_pts(lcx, lcy, bxr, byr, 400),
                     C_ANNO_WARM, max(3, lw), dash=lw * 8, gap=lw * 6)
    f = mock.font(max(28, int(round(ppm * 0.42))), bold=True)
    dr.text((lcx, lcy + byr + 18), "LANTERN (declared) — brightest, calmest "
            "floor", font=f, fill=C_ANNO_WARM, anchor="ma")
    dr.text((cv.px(pass_x0_m, y_join_m)[0] - 24, sy_px),
            "CHOIR SCREEN — an arch OVERHEAD, no footprint",
            font=f, fill=C_ANNO_WARM, anchor="rm")
    r = max(16, int(round(ppm * 0.30)))
    dr.line([(ox0 - r, oy0), (ox0 + r, oy0)], fill=C_ANNO, width=max(3, lw))
    dr.line([(ox0, oy0 - r), (ox0, oy0 + r)], fill=C_ANNO, width=max(3, lw))
    dr.text((ox0 + r + 14, oy0 + r + 10), "SPAWN = frame origin (0,0)",
            font=f, fill=C_ANNO, anchor="la")
    # the corridor head: the arena's northernmost floor, where the entry is
    hx = head_x_sq
    hy = head_row_sq * proj.sin_a
    dr.line([(hx - r, hy + r), (hx + r, hy + r)], fill=C_ANNO_DIM,
            width=max(3, lw))
    dr.text((hx, hy + r + 16), "CORRIDOR HEAD", font=f, fill=C_ANNO_DIM,
            anchor="ma")
    outputs["guide.png"] = w("guide.png", guide)

    # ---- manifest -----------------------------------------------------------
    man = {
        "generated": "2026-09-26",
        "author": "drax (presentation seam)",
        "run": "C-9",
        "phase": "P2' — cathedral grey room on the Crucible arena",
        "gate": "M2 — Matt approves this grey room BEFORE any cathedral paint "
                "(R-C3-55a)",
        "dispatch": "agentic_orchestration/dispatches/"
                    "2026-09-26-drax-c9-cathedral-greyroom.md",
        "generator": os.path.basename(__file__),
        "burst_fired": False, "godot_launched": False,
        "new_art_minted": False, "painting_started": False,
        "camera": {
            "yaw_deg": 47.0,
            "pitch_alpha_deg": mock.ALPHA_DEG,
            "projection": "orthographic; +x EAST -> +px right, +y SOUTH -> "
                          "+px down x sin(alpha); elevation displaces "
                          "UP-SCREEN by h*ppm*cos(alpha)",
            "px_per_m_east": ppm,
            "px_per_m_south_ground": ppm * math.sin(a),
            "px_per_m_up_screen": ppm * math.cos(a),
            "m_per_px_east": 1.0 / ppm,
            "m_per_px_south_ground": 1.0 / (ppm * math.sin(a)),
            "ppm_source": "agentic_orchestration/drax/captures/"
                          "2026-09-13-cliffside-blockout/blockout_meta_v2.json"
                          " :: ortho_canvas_v2.px_per_m_screen_x (R-C3-44)",
            "plate_law_cross_check": "PASSED (both ruled px/m figures fall out "
                                     "of alpha to < 1e-6)",
        },
        "scale_figures": {
            "u_m_per_native_px": u,
            "u_source": "KC2-PLAY charter KP-6, ratified KP-9",
            "geometry_file_own_scale_IGNORED": 0.1981,
            "why_ignored": "DERIVED-WEAK, superseded (Gate-1 WARN-8 / dispatch "
                           "required reading 4).",
            "keeper_130px_convention": 130.0,
            "keeper_130px_implies_body_m": 130.0 / (ppm * math.cos(a)),
            "kc2_h_fig_m": mock.H_FIG_M,
            "kc2_h_fig_px_on_this_plate": mock.H_FIG_M * ppm * math.cos(a),
            "note": "the dispatch names 'Keeper scale 130 px at 1080p'. That "
                    "130 px is the CLIFFSIDE convention and implies a 2.1446 m "
                    "body; KC2-PLAY KP-18 (a) already ruled that h_fig = 1.9 m "
                    "stands for this arena and that 130 px is NOT inherited. "
                    "This canvas adopts the ratified PLATE SCALE (which is what "
                    "'130 px at 1080p' pins) and carries BOTH figures rather "
                    "than silently picking one.",
        },
        "canvas": cv.world_rect(),
        "arena": {
            "bbox_m": [bx0, by0, bx1, by1],
            "extent_m": [bx1 - bx0, by1 - by0],
            "walkable_area_m2": float(walkp.sum()) / (ppm * ppm * math.sin(a)),
            "geometry_file": "agentic_orchestration/galadriel/notes/"
                             "crucible-arena-geometry-v1.json",
            "geometry_sha256": geom_sha,
        },
        "derived_from_geometry": {
            "y_join_m": y_join_m,
            "y_join_rule": "northernmost row whose widest single run of floor "
                           ">= 0.75 x the arena's widest run",
            "screen_passage_x_m": [pass_x0_m, pass_x1_m],
            "central_vessel_width_m": vessel_w,
            "bay_m": BAY_M,
            "bay_actual_m": bay_actual,
            "n_bays": n_bays,
            "ring_length_m": total,
            "choir_band_y_m": [choir_y0_m, choir_y1_m],
            "choir_band_rule": "the y-extent of OB-1 and OB-2, the two long "
                               "thin islands the mapping calls choir stalls",
            "sanctuary_rule": "south floor within one bay of OB-3 u OB-4",
        },
        "declared_not_measured": DECLARED,
        "mapping": [
            ["North corridor + red door (spawn)",
             "Entry through the choir screen into the crossing",
             "screen_passage", "the ring north of y_join, inside the "
             "passage's own measured x-extent"],
            ["Central oval", "The crossing under the lantern: brightest floor",
             "crossing", "floor from y_join to the choir band"],
            ["NW / NE lobes", "The transept arms", "transept_w / transept_e",
             "floor north of y_join, outside the passage's x-extent"],
            ["Two long thin E/W interior walls", "Choir stalls",
             "choir_stall", "OB-1 (west), OB-2 (east), verbatim polygons"],
            ["SW / S / SE lobes + the two small S islands",
             "Ambulatory chapels; the altar and a tomb",
             "ambulatory_floor / sanctuary_floor / altar / tomb",
             "floor south of the choir band; OB-3 = altar, OB-4 = tomb"],
            ["Six green DoT zones", "Rot-soaked chapel floor. ENTERABLE.",
             "rot_zone", "walkable; never collision, never a pit"],
        ],
        "id_mask": {
            "file": "id_mask.png",
            "encoding": "flat index colours, NEAREST only",
            "classes": [dict({"index": i, "name": n, "rgb": list(c),
                              "walkable": wk, "guide_grey": list(g)},
                             **stats[n])
                        for i, (n, g, c, wk) in enumerate(CLASSES)],
            "full_bleed": "TRUE — every pixel carries a class. There is no "
                          "void, no border and no #00ff00 plate in this mask: "
                          "the cathedral interior has no sky (brief S 4).",
        },
        "depth_mm": {
            "file": "depth_mm.png",
            "encoding": "uint16 PNG (I;16); value = MILLIMETRES OF ELEVATION "
                        "above the arena floor plane",
            "convention_source": "the KC2-PLAY arena guide "
                                 "(2026-09-20-kc2-play-arena-guide), which "
                                 "declared this divergence from the "
                                 "cliffside's 'mm below local rim'",
            "why_not_below_rim": "the cliffside's rim datum does not exist "
                                 "here: this interior has no void and no pit, "
                                 "so there is nothing to be below.",
            "content": {"floor + rot": 0,
                        "arcade_dado": int(NEAR_CUT_M * 1000),
                        "tomb": int(TOMB_H_M * 1000),
                        "altar": int(ALTAR_H_M * 1000),
                        "choir_stall": int(STALL_H_M * 1000),
                        "wall_face": "ramps 0 -> the element's height"},
            "max_mm": int(elev.max()),
        },
        "walkable_mask": {
            "file": "walkable_mask.png",
            "rule": "white = the measured arena floor minus the four interior "
                    "obstructions. The six rot zones ARE walkable. Aisles, "
                    "chapels, piers and the dado are NOT.",
            "clip_px": WALKABLE_CLIP_PX,
            "clip_authority": "R-C3-58",
            "clipped_px": clipped,
            "clip_note": "the floor never reaches the canvas edge (a >= 7 m "
                         "surround of cathedral fabric stands between them), "
                         "so the clip removes %d px and is a formality here."
                         % clipped,
            "walkable_px": int(walk_out.sum()),
        },
        "dot_zones": {
            "count": len(zrows),
            "class_note": geom["green_zones"]["class_note"],
            "geometry_provenance": geom["green_zones"]["geometry_provenance"],
            "derivation": "DISC = the MEASURED interior point, radius = the "
                          "file's radius_upper_bound_px x u, clipped to the "
                          "walkable floor. The radius is an UPPER BOUND, not a "
                          "measurement (green_zones.why_no_polygons: the "
                          "ground map M is unrecoverable from the 21 "
                          "stations), so the disc is an upper bound too. No "
                          "outline was traced and none is claimed.",
            "FINDING_ROUTED_TO_M2":
                "at the raw upper bounds the six discs cover %.1f %% of the "
                "walkable floor and OVERLAP each other. That contradicts the "
                "geometry file's own finding that six MUTUALLY DISTINCT zones "
                "are demonstrated, and it contradicts brief S 4 ('walkable = "
                "brightest and calmest'). An upper bound is not an estimate: "
                "painting to it over-paints by construction."
                % (100 * frac_full),
            "primary_mask": "dot_zone_mask.png",
            "primary_rule": "the upper-bound radii scaled by k_disjoint. This "
                            "is what guide.png and id_mask.png carry. DRAX'S "
                            "CALL, not a measurement; M2 may overrule it in "
                            "either direction.",
            "primary_floor_fraction": round(float(frac_dis), 4),
            "k_disjoint": k_disjoint,
            "k_disjoint_rule": "the largest uniform scale on the upper-bound "
                               "radii at which all six discs stay pairwise "
                               "disjoint -- i.e. the largest value consistent "
                               "with BOTH the radii and the six-distinct-zones "
                               "finding. DERIVED from the interior points, not "
                               "chosen. Binding pair: Z-622 / Z-623.",
            "envelope_mask": "dot_zone_mask_upper_bound.png",
            "envelope_rule": "the raw upper-bound discs, clipped to the floor. "
                             "Not a claim that the rot reaches this far -- a "
                             "claim that it goes no further. Drawn on the "
                             "guide as a dashed green line, never filled.",
            "envelope_floor_fraction": round(float(frac_full), 4),
            "zones": zrows,
        },
        "near_side_and_back_walls": {
            "rise_m": RISE_M,
            "rise_px_up_screen": rise_px,
            "near_cut_m": NEAR_CUT_M,
            "near_cut_px_up_screen": near_px,
            "rule": "a masonry element is CUT to the near-cut height iff "
                    "walkable floor lies within the rise distance NORTH of it "
                    "— i.e. iff raising it would occlude play space. Up-screen "
                    "is north, so the near (south) side cuts itself and the "
                    "back (north) walls rise and exit the top edge. No list of "
                    "faces appears anywhere in the generator.",
            "cut_low_px": int(bled),
        },
        "overhead_layer_declared_not_built": [
            {"what": "the vault", "why":
             "Antwerp's vault is far above the 6 m rise; at %0.1f px/m "
             "up-screen a true vault springing would cover the northern half "
             "of the plate. The vault belongs on the Overhead layer (z3, "
             "scene-builder-workflow S 3 step 7 / T3l), not on this plate. "
             "NOT built here." % (ppm * math.cos(a))},
            {"what": "the choir screen across the entry", "why":
             "a screen with a doorway would punch a hole in the walkable mask. "
             "It is painted as an ARCH OVER the passage on the Overhead layer, "
             "with no footprint. Annotated on the guide, not classed."},
        ],
        "chunk_grid": {
            "chunk_px": [CHUNK_W, CHUNK_H],
            "overlap_px": [OVERLAP, OVERLAP],
            "step_px": [STEP_W, STEP_H],
            "grid": [NROW, NCOL],
            "n_chunks": len(chunks),
            "origin_offset_px": [-OX, -OY],
            "origin_rule": "chosen by search over 16-px offsets to MINIMISE "
                           "the walkable floor lying under chunk seams (brief "
                           "S 4 'seams hide in dead space'). The search is "
                           "CONSTRAINED to the minimal grid: it may not buy a "
                           "better seam with an extra row or column, because "
                           "that is %d more paint calls per style arm."
                           % max(NCOL_MIN, NROW_MIN),
            "seam_on_walkable_px": seam_cost,
            "seam_on_walkable_px_at_offset_zero": seam_cost_at_zero,
            "keep_rule": "ALL — the canvas is full-bleed, every chunk carries "
                         "architecture.",
            "chunks": chunks,
        },
        "outputs": outputs,
        "substrate": {
            "arena_geometry_sha256": geom_sha,
            "blockout_meta": "agentic_orchestration/drax/captures/"
                             "2026-09-13-cliffside-blockout/blockout_meta_v2.json",
            "g_img_mock": "agentic_orchestration/drax/captures/"
                          "2026-09-20-kc2-play-g-img/make_g_img_mock.py",
            "antwerp_plan": "matt_notes_handoff_docs/"
                            "rdr-art-illuminated-archive-refs/cathedral-plan/"
                            "antwerp-cathedral-grundriss.jpg",
            "vault_reference": "matt_notes_handoff_docs/"
                               "rdr-art-illuminated-archive-refs/"
                               "cathedral-look-alt/"
                               "spinola-hours-f185-office-of-the-dead.jpg",
        },
    }
    mp = os.path.join(outdir, "greyroom_manifest.json")
    with open(mp, "w") as fh:
        json.dump(man, fh, indent=1)
    print("[done] %.1f s   -> %s" % (time.time() - t0, outdir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
