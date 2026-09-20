#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KC2-PLAY · Wave-1 addendum — THE ARENA GREY-ROOM GUIDE SET
(charter ledger KP-12: ONE painted arena plate is in scope; `KP-B1a` paints ONE
image over this guide, then HALTs for Matt's style/register review.)

WHAT THIS IS
------------
  The grey-room / blockout guide the Astra paint-over burst paints ON TOP OF —
  the arena's equivalent of the cliffside blockout (scene-builder-workflow § 3
  step 1: orthographic canvas + ID mask + depth map; step 2's walkable/collision
  is NOT this seat's output here, the runtime owns collision).

  GEOMETRY IS TRUE.  Every distance is COMPUTED from the projection law of
  `2026-09-20-kc2-play-2d-retarget-spec.md` § 1.1/§ 1.2 (as amended by its two
  Corrigenda-Forward) applied to the video-measured arena geometry
  (`crucible-arena-geometry-v1.json`) at the registered `u` — all of which are
  IMPORTED FROM `make_g_img_mock.py`, not retyped.  This script adds exactly
  four numbers of its own; three of them are DECLARED placeholders and the
  fourth is READ from a file (§ 0 below).

  THE GUIDE IS DRESSING-NEUTRAL.  G5 (interior nave vs exterior arena) is Matt's
  open call.  Nothing here commits it: the wall is drawn as a GROUND BAND, not
  an extruded wall, because a nave's wall height and an arena's wall height are
  not the same number and neither is measured.

LAW OBSERVED
------------
  GL-6   — the geometry file is digest-verified before use (mock.load_geometry).
  GL-10  — the wire's constants are used, never re-derived.
  GL-12  — an absence is DECLARED.  Wall-band thickness, island height and the
           Banner's placement have NO wire basis; they are declared here, printed
           on the plate, and carried in the manifest.
  Law 3  — no fitted constants.

Author: drax (presentation seam), run KC2-PLAY Wave 1 addendum, 2026-09-20.
Usage:  python3 make_arena_guide.py
Writes NOTHING under astra_test_01/burst/ — the far_ruins layer is READ ONLY.
"""

import hashlib
import json
import math
import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.dirname(os.path.abspath(__file__))
CAPTURES = os.path.dirname(ROOT)
COLLAB = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
G_IMG_DIR = os.path.join(CAPTURES, "2026-09-20-kc2-play-g-img")
BLOCKOUT_META = os.path.join(
    CAPTURES, "2026-09-13-cliffside-blockout", "blockout_meta_v2.json")
BLOCKOUT_META_V1 = os.path.join(
    CAPTURES, "2026-09-13-cliffside-blockout", "blockout_meta.json")
FAR_RUINS = os.path.join(
    COLLAB, "astra_test_01", "burst", "runs", "C-7", "cliffside_v45",
    "parallax", "layers", "far_ruins.png")

# The G-IMG mock is the source of every projection constant and of the
# projection class itself.  Importing it (rather than retyping alpha, h_fig,
# u, the F4 fractions, the Banner radius or the geometry digest) is the point:
# a later move of `u` or of `h_fig` moves this guide with it, automatically.
sys.path.insert(0, G_IMG_DIR)
import make_g_img_mock as mock                                    # noqa: E402


# ===========================================================================
# 0 · THE FOUR NUMBERS THIS SCRIPT ADDS.  Everything else is imported.
# ===========================================================================

# (1) READ, not typed — the authored plate scale of the cliffside orthographic
#     canvas (drax P0-c; R-C3-44).  Lives in this seat's own blockout meta.
def read_ppm_plate():
    with open(BLOCKOUT_META) as fh:
        oc = json.load(fh)["ortho_canvas_v2"]
    return oc["px_per_m_screen_x"], oc


# (2) DECLARED PLACEHOLDER — wall-band thickness.  NO WIRE BASIS.  Grim Dawn's
#     minimap paints WALKABLE FLOOR ONLY, so the arena geometry file records the
#     hard boundary (the floor's edge) and nothing outside it.  The band exists
#     so the painter has a surface to paint a wall on.  Its INNER edge is the
#     measured ring and is load-bearing; its OUTER edge is free.
WALL_BAND_THICKNESS_M = 2.0

# (3) RULED — island height.  Was a DECLARED placeholder at 1.0 m; conductor
#     ledger KP-18 (c): "Islands are low stumps/rubble <= 0.5 m visual."  The
#     superseded value is kept beside it so the change is legible, never silent.
ISLAND_HEIGHT_M = 0.5
ISLAND_HEIGHT_SUPERSEDED_M = 1.0

# (3b) RULED — the wall-face elevation allowance.  Conductor ledger KP-18 (b),
#     folding Matt's G5 call: INTERIOR NAVE.  "The painting may raise
#     north/east/west wall faces into `beyond` above the band within a declared
#     elevation allowance <= 6 m; south face stays low."  The px figure is
#     DERIVED (h * ppm * cos alpha), never typed.
WALL_FACE_ALLOWANCE_M = 6.0

# (4) DECLARED — the cathedral reference cut.  A hand-chosen bbox on
#     far_ruins.png (native px, left/top/right/bottom) around the lower-left
#     burning gothic cathedral (C-3 R-C3-72 / `CS-cathedral`), framed to include
#     both banner columns and the terrace it stands on.
CATHEDRAL_BBOX = (300, 960, 900, 1400)

# --- free layout / art (no spatial claim) ----------------------------------
MARGIN_PX = 96
TITLE_W, TITLE_H = 1620, 430

IDX = {"beyond": 0, "floor": 1, "wall": 2, "island": 3, "pool": 4,
       "allowance": 5}
ID_COLOUR = {                       # flat index colours for id_mask.png
    0: (0, 0, 0),                   # beyond     #000000
    1: (46, 204, 64),               # floor      #2ECC40
    2: (255, 65, 54),               # wall       #FF4136
    3: (0, 116, 217),               # island     #0074D9
    4: (255, 220, 0),               # pool       #FFDC00
    5: (177, 13, 201),              # allowance  #B10DC9
}
GUIDE_GREY = {
    0: (0, 0, 0),                   # beyond — the parallax layer's job later
    1: (110, 110, 110),             # floor
    2: (58, 58, 58),                # wall band (darker)
    3: (138, 138, 138),             # island side face
    4: (122, 122, 122),             # pool disc base (hatched on top)
    5: (40, 40, 40),                # wall-face allowance (paintable elevation)
}

# ---------------------------------------------------------------------------
# B1a CHUNK PALETTE — the CLIFFSIDE grey-room convention (Astra's habit).
# The three grey-room classes are READ from the cliffside blockout's own
# `layer_id.legend_rgb8`, never retyped.  Two arena classes have no cliffside
# equivalent and are DECLARED extensions.  `#00ff00` is the lane's void colour
# and is RESERVED here even though KP-19 leaves no void in this mask.
# ---------------------------------------------------------------------------
B1A_VOID_RGB = (0, 255, 0)              # lane void / green-screen, exact
B1A_POOL_RGB = (255, 0, 0)              # ARENA EXTENSION — damage field
B1A_ISLAND_RGB = (0, 0, 255)            # ARENA EXTENSION — stump / rubble
C_ISLAND_TOP = (172, 172, 172)
C_HATCH = (79, 79, 79)
C_ANNO = (0, 255, 255)              # cyan == ANNOTATION.  NEVER paint it.
C_ANNO_DIM = (0, 150, 150)


# ===========================================================================
# 1 · PROJECTION — the mock's own class, at three scales.
# ===========================================================================

def projection_at_ppm(ppm, name, u):
    """mock.Projection takes a FIGURE FRACTION, so invert § 1.2 to reach an
    arbitrary ppm.  Nothing new is introduced: fraction and ppm are the same
    statement written two ways."""
    alpha = math.radians(mock.ALPHA_DEG)
    fraction = ppm * mock.H_FIG_M * math.cos(alpha) / mock.VIEW_H
    p = mock.Projection(fraction, name, u)
    assert abs(p.ppm - ppm) < 1e-9, "ppm round-trip failed"
    return p


def plate_law_cross_check(ppm_plate, oc):
    """FREE CROSS-CHECK, the § 1.1 kind: the cliffside plate was authored with
    its own independently-ruled px/m figures.  If the plate is under the SAME
    projection law as the arena, then ppm*sin(alpha) and ppm*cos(alpha) must
    reproduce them.  Nothing is imposed; this only asks whether they agree."""
    a = math.radians(mock.ALPHA_DEG)
    rows = [("ground depth  ppm*sin", ppm_plate * math.sin(a),
             oc["px_per_ground_m_screen_y"]),
            ("vertical      ppm*cos", ppm_plate * math.cos(a),
             oc["px_per_vertical_m_screen_y"])]
    print("\n[plate] cliffside canvas vs the arena's projection law")
    for k, got, want in rows:
        d = abs(got - want)
        print("  %-24s derived %14.10f   authored %14.10f   d=%.2e  %s"
              % (k, got, want, d, "OK" if d < 1e-6 else "**MISMATCH**"))
        if d >= 1e-6:
            sys.exit("PLATE CROSS-CHECK FAILED — the cliffside canvas is NOT "
                     "under alpha = %.10f deg." % mock.ALPHA_DEG)
    return rows


# ===========================================================================
# 2 · RASTERISER — one code path, called at plate scale and at ZOOM-GD.
# ===========================================================================

class Rect:
    """A world-metre rectangle pinned to a pixel size at a given ppm.
    +x = EAST, +y = SOUTH (the geometry file's own frame; no flip applied)."""

    def __init__(self, proj, centre_m, size_px):
        self.proj = proj
        self.W, self.H = int(size_px[0]), int(size_px[1])
        self.cx, self.cy = centre_m
        self.half_w_m = self.W / 2.0 / proj.ppm
        self.half_h_m = self.H / 2.0 / (proj.ppm * proj.sin_a)
        self.x0, self.x1 = self.cx - self.half_w_m, self.cx + self.half_w_m
        self.y0, self.y1 = self.cy - self.half_h_m, self.cy + self.half_h_m

    def to_px(self, mx, my):
        return ((mx - self.x0) * self.proj.ppm,
                (my - self.y0) * self.proj.ppm * self.proj.sin_a)

    def to_sq(self, mx, my):
        """Square (world-isotropic) raster: y NOT compressed.  Masks are built
        here so that a metre is a metre in both axes, then squashed by sin a."""
        return ((mx - self.x0) * self.proj.ppm,
                (my - self.y0) * self.proj.ppm)

    @property
    def sq_size(self):
        return (self.W, int(round((self.y1 - self.y0) * self.proj.ppm)))

    def world_rect(self):
        return {"x_min_m": self.x0, "x_max_m": self.x1,
                "y_min_m": self.y0, "y_max_m": self.y1,
                "width_m": self.x1 - self.x0, "height_m": self.y1 - self.y0,
                "centre_m": [self.cx, self.cy],
                "size_px": [self.W, self.H],
                "axes": "+x = EAST, +y = SOUTH (minimap frame, no flip)"}


def build_index_map(rect, geom, u, pocket_source=None):
    """Returns the class index map at rect.size, built in SQUARE space (so the
    wall band is a true Euclidean offset in metres) and squashed by sin(alpha).

    `pocket_source` = (square_index_map, its Rect) from the PLATE.  Enclosure is
    a GLOBAL fact — whether a hole is the outside world or the inside of a wall
    mass cannot be decided inside a 1920x1080 window — so the crop asks the
    plate rather than guessing from its own border.  The plate decides it for
    itself (`close_pockets` below)."""
    sw, sh = rect.sq_size
    img = Image.new("L", (sw, sh), IDX["beyond"])
    dr = ImageDraw.Draw(img)
    hb = geom["hard_boundary"]

    def sq(nx, ny):
        return rect.to_sq(nx * u, ny * u)

    ring = [sq(*v) for v in hb["outer_ring"]["vertices_native"]]
    dr.polygon(ring, fill=IDX["floor"])
    floor = np.asarray(img) == IDX["floor"]

    # pools — flat discs, clipped to the floor.  Radii are UPPER BOUNDS.
    pool_img = Image.new("L", (sw, sh), 0)
    pd = ImageDraw.Draw(pool_img)
    pool_rows = []
    for z in geom["green_zones"]["zones"]:
        cx, cy = sq(*z["interior_point_minimap_px"])
        r_px = z["radius_upper_bound_px"] * u * rect.proj.ppm
        pd.ellipse([cx - r_px, cy - r_px, cx + r_px, cy + r_px], fill=1)
        pool_rows.append((z, cx, cy, r_px))
    pool = (np.asarray(pool_img) == 1) & floor

    # wall band — every pixel OUTSIDE the floor within THICKNESS metres of it.
    # Exact Euclidean in metres because this raster is world-isotropic.
    dist_px = ndimage.distance_transform_edt(~floor)
    band = (~floor) & (dist_px <= WALL_BAND_THICKNESS_M * rect.proj.ppm)

    idx = np.zeros((sh, sw), dtype=np.uint8)
    idx[floor] = IDX["floor"]
    idx[pool] = IDX["pool"]
    idx[band] = IDX["wall"]

    # ENCLOSED POCKETS.  A fixed-thickness band does not fill a wall spur
    # thicker than 2*THICKNESS, so the spur's core falls out as `beyond` — a
    # black hole in the MIDDLE of the wall.  `beyond` means "the parallax
    # layers' region"; a pocket sealed inside a wall mass is not that, it is
    # wall.  Reclassify every `beyond` component that does not reach the
    # outside world.
    pockets = 0
    if pocket_source is None:                       # the plate decides for itself
        lab, n = ndimage.label(idx == IDX["beyond"])
        border = set(np.unique(np.concatenate(
            [lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])))
        border.discard(0)
        enclosed = (lab > 0) & ~np.isin(lab, list(border))
        pockets = int(enclosed.sum())
        idx[enclosed] = IDX["wall"]
    else:                                           # a window asks the plate
        src_idx, src_rect = pocket_source
        ys, xs = np.nonzero(idx == IDX["beyond"])
        if len(xs):
            mx = rect.x0 + xs / rect.proj.ppm
            my = rect.y0 + ys / rect.proj.ppm
            px = np.rint((mx - src_rect.x0) * src_rect.proj.ppm).astype(int)
            py = np.rint((my - src_rect.y0) * src_rect.proj.ppm).astype(int)
            ok = ((px >= 0) & (px < src_idx.shape[1]) &
                  (py >= 0) & (py < src_idx.shape[0]))
            hit = np.zeros(len(xs), dtype=bool)
            hit[ok] = src_idx[py[ok], px[ok]] == IDX["wall"]
            pockets = int(hit.sum())
            idx[ys[hit], xs[hit]] = IDX["wall"]

    isl_img = Image.new("L", (sw, sh), 0)
    idr = ImageDraw.Draw(isl_img)
    for ob in hb["interior_obstructions"]:
        idr.polygon([sq(*v) for v in ob["vertices_native"]], fill=1)
    idx[np.asarray(isl_img) == 1] = IDX["island"]

    squashed = Image.fromarray(idx).resize((rect.W, rect.H), Image.NEAREST)
    return np.asarray(squashed).copy(), pool_rows, idx, pockets


def extrude_islands(idx, rect):
    """Vertical extrusion is a SCREEN displacement, not a squash, so it happens
    in plate space.  Returns (idx, elevation_mm, top_face_mask).

    A pixel p shows the HIGHEST island surface above it: elevation(p) = max e in
    [0, h] with (p + e*ppm*cos a upward) still over the footprint.  Ascending
    overwrite gives that max for free."""
    k_px = ISLAND_HEIGHT_M * rect.proj.ppm * rect.proj.cos_a
    steps = int(round(k_px))
    foot = idx == IDX["island"]
    elev = np.zeros(idx.shape, dtype=np.uint16)
    top = np.zeros(idx.shape, dtype=bool)
    if not foot.any() or steps <= 0:
        return idx, elev, top, k_px
    for s in range(0, steps + 1):
        shifted = np.zeros_like(foot)
        if s == 0:
            shifted = foot
        else:
            shifted[:-s, :] = foot[s:, :]
        mm = int(round(ISLAND_HEIGHT_M * 1000.0 * s / steps))
        idx[shifted] = IDX["island"]
        elev[shifted] = mm
        if s == steps:
            top = shifted
    return idx, elev, top, k_px


# ===========================================================================
# 3 · PAINTERS
# ===========================================================================

def sweep_wall_faces(idx, rect):
    """KP-18 (b): the painting may raise wall faces into `beyond` above the
    band, up to WALL_FACE_ALLOWANCE_M.  Sweep the wall band UP-SCREEN and keep
    only what lands on `beyond`.

    The direction rule falls out of the geometry and is not hand-authored:
    up-screen is NORTH, so a north/east/west band sweeps into `beyond` and
    claims an allowance, while the SOUTH band sweeps into the arena FLOOR and
    claims nothing.  'South face stays low' is therefore enforced by the sweep,
    not by a list of faces."""
    k_px = WALL_FACE_ALLOWANCE_M * rect.proj.ppm * rect.proj.cos_a
    steps = int(round(k_px))
    wall = idx == IDX["wall"]
    if not wall.any() or steps <= 0:
        return idx, 0, k_px
    claim = np.zeros(idx.shape, dtype=bool)
    for s in range(1, steps + 1):
        shifted = np.zeros_like(wall)
        shifted[:-s, :] = wall[s:, :]
        claim |= shifted
    claim &= (idx == IDX["beyond"])
    idx[claim] = IDX["allowance"]
    return idx, int(claim.sum()), k_px


def guide_rgb(idx, elev, top, rect, geom, u, stamp_lines, title=None):
    lut = np.zeros((len(IDX), 3), dtype=np.uint8)
    for k, v in GUIDE_GREY.items():
        lut[k] = v
    arr = lut[idx]
    arr[top] = C_ISLAND_TOP
    img = Image.fromarray(arr, "RGB").convert("RGBA")
    dr = ImageDraw.Draw(img)
    hb = geom["hard_boundary"]

    # pool hatch — 45 deg, drawn only where the class is pool
    pool = idx == IDX["pool"]
    if pool.any():
        hatch = Image.new("L", img.size, 0)
        hd = ImageDraw.Draw(hatch)
        pitch = max(8, int(round(rect.proj.ppm * 0.35)))
        for c in range(-img.height, img.width, pitch):
            hd.line([(c, 0), (c + img.height, img.height)], fill=255, width=2)
        h = (np.asarray(hatch) > 0) & pool
        a = np.asarray(img).copy()
        a[h] = C_HATCH + (255,)
        img = Image.fromarray(a, "RGBA")
        dr = ImageDraw.Draw(img)

    def px(nx, ny):
        return rect.to_px(nx * u, ny * u)

    # the ring's INNER edge — the one measured, load-bearing edge.
    # SOLID where walked; DASHED across the two mapped-but-never-walked arcs.
    ring_px = [px(*v) for v in hb["outer_ring"]["vertices_native"]]
    walked, unw = mock.split_ring(ring_px, hb["unwalked_arcs"],
                                  len(ring_px))
    lw = max(2, int(round(rect.proj.ppm / 34.0)))
    for run in walked:
        dr.line(run, fill=C_ANNO, width=lw)
    for run in unw:
        mock.dashed_path(dr, run, C_ANNO, lw, dash=lw * 9, gap=lw * 7)

    # island contact lines (the y-sort line lives on these)
    for ob in hb["interior_obstructions"]:
        pts = [px(*v) for v in ob["vertices_native"]]
        dr.line(pts + [pts[0]], fill=C_ANNO_DIM, width=max(1, lw // 2))

    # Vanguard Banner aura footprint — thin line, DECLARED PLACEMENT.
    bx, by = rect.proj.r_to_semiaxes(mock.BANNER_AURA_M)
    ox, oy = rect.to_px(0.0, 0.0)
    mock.dashed_path(dr, mock.ellipse_pts(ox, oy, bx, by, 400), C_ANNO,
                     max(1, lw // 2), dash=lw * 6, gap=lw * 5)

    # frame origin == north gate
    r = max(10, int(round(rect.proj.ppm * 0.22)))
    dr.line([(ox - r, oy), (ox + r, oy)], fill=C_ANNO, width=max(2, lw))
    dr.line([(ox, oy - r), (ox, oy + r)], fill=C_ANNO, width=max(2, lw))
    f = mock.font(max(14, int(round(rect.proj.ppm * 0.26))), bold=True)
    dr.text((ox + r + 8, oy - r), "frame origin = NORTH GATE (0, 0)",
            font=f, fill=C_ANNO)

    if title:
        draw_title(img, dr, idx, rect, title)
    if stamp_lines:
        fs = mock.font(20, mono=True)
        y = img.height - 14 - 22 * len(stamp_lines)
        for ln in stamp_lines:
            dr.text((16, y), ln, font=fs, fill=C_ANNO)
            y += 22
    return img.convert("RGB")


def draw_title(img, dr, idx, rect, rows):
    """Placed in a corner that is 100 % `beyond`.  ASSERTED, not assumed."""
    m = MARGIN_PX // 2
    cands = [(m, m), (img.width - TITLE_W - m, m),
             (m, img.height - TITLE_H - m),
             (img.width - TITLE_W - m, img.height - TITLE_H - m)]
    spot = None
    for (x, y) in cands:
        if x < 0 or y < 0:
            continue
        if (idx[y:y + TITLE_H, x:x + TITLE_W] == IDX["beyond"]).all():
            spot = (x, y)
            break
    if spot is None:
        sys.exit("TITLE BLOCK ABORT: no corner of the plate is entirely "
                 "`beyond`; the block would cover paintable surface.")
    x, y = spot
    dr.rectangle([x, y, x + TITLE_W, y + TITLE_H], outline=C_ANNO, width=2)
    fb, fm = mock.font(30, bold=True), mock.font(19, mono=True)
    dr.text((x + 18, y + 14), "ARENA GREY-ROOM GUIDE — PLATE", font=fb,
            fill=C_ANNO)
    yy = y + 58
    for k, v in rows:
        dr.text((x + 18, yy), k, font=fm, fill=C_ANNO_DIM)
        dr.text((x + 300, yy), v, font=fm, fill=C_ANNO)
        yy += 23


def draw_scale_bars(img, rect, ppm_plate):
    """Ground metre bars (x and y differ — y is compressed by sin alpha) and the
    two figure heights this plate has to reconcile."""
    dr = ImageDraw.Draw(img)
    f = mock.font(19, mono=True)
    x0, y0 = MARGIN_PX // 2 + 18, img.height - MARGIN_PX // 2 - 260
    ten_x = 10.0 * rect.proj.ppm
    ten_y = 10.0 * rect.proj.ppm * rect.proj.sin_a
    dr.line([(x0, y0), (x0 + ten_x, y0)], fill=C_ANNO, width=4)
    dr.text((x0, y0 + 8), "10 m EAST  = %.2f px" % ten_x, font=f, fill=C_ANNO)
    dr.line([(x0, y0 + 40), (x0, y0 + 40 + ten_y)], fill=C_ANNO, width=4)
    dr.text((x0 + 14, y0 + 40), "10 m SOUTH = %.2f px  (ground depth)" % ten_y,
            font=f, fill=C_ANNO)
    return x0, y0


def figure_heights(ppm_plate, oc):
    """The register question, in numbers.  Both are heights of a standing body
    on THIS plate; they do not agree, and the guide cannot make them agree."""
    a = math.radians(mock.ALPHA_DEG)
    arena_px = ppm_plate * mock.H_FIG_M * math.cos(a)
    cliff_px = oc["proxy_silhouette_spawn_ortho"]["height_px_1080"]
    implied_h = cliff_px / (ppm_plate * math.cos(a))
    return {
        "arena_h_fig_m": mock.H_FIG_M,
        "arena_figure_px_on_plate": arena_px,
        "cliffside_keeper_px_on_plate": cliff_px,
        "cliffside_keeper_frac_1080":
            oc["proxy_silhouette_spawn_ortho"]["height_frac"],
        "cliffside_implied_h_fig_m": implied_h,
        "ratio_cliffside_over_arena": cliff_px / arena_px,
    }


def draw_figure_bars(img, x0, y0, fh):
    dr = ImageDraw.Draw(img)
    f = mock.font(19, mono=True)
    bx = x0 + 560
    for i, (label, h, col) in enumerate((
            ("arena h_fig %.1f m" % fh["arena_h_fig_m"],
             fh["arena_figure_px_on_plate"], C_ANNO),
            ("cliffside Keeper (implies %.4f m)" % fh["cliffside_implied_h_fig_m"],
             fh["cliffside_keeper_px_on_plate"], (255, 0, 255)))):
        x = bx + i * 340
        base = y0 + 230
        dr.rectangle([x, base - h, x + 34, base], outline=col, width=3)
        dr.text((x + 44, base - h), "%s\n%.3f px" % (label, h), font=f,
                fill=col)


# ===========================================================================
# 4 · MAIN
# ===========================================================================

def sha(path):
    return mock.sha256_of(path)


def main():
    print("KC2-PLAY Wave-1 addendum · ARENA GREY-ROOM GUIDE (ledger KP-12)")
    print("=" * 78)
    geom = mock.load_geometry()                       # GL-6, digest-gated
    u = mock.U_REGISTERED
    if not (mock.U_WINDOW[0] <= u <= mock.U_WINDOW[1]):
        sys.exit("registered u outside the window of record")
    print("[kp-6]  u = %.6f m per native minimap px (in window [%.5f, %.4f])"
          % (u, mock.U_WINDOW[0], mock.U_WINDOW[1]))

    ppm_plate, oc = read_ppm_plate()
    print("[p0-c]  ppm_plate = %.12f px/m  (cliffside ortho canvas, R-C3-44)"
          % ppm_plate)
    cross = plate_law_cross_check(ppm_plate, oc)

    plate_proj = projection_at_ppm(ppm_plate, "PLATE", u)
    gd_proj = mock.Projection(mock.FRACTION_ZOOM_GD, "ZOOM-GD", u)
    print("\n[scales] plate %.6f px/m · ZOOM-GD %.6f px/m · ratio %.10f"
          % (plate_proj.ppm, gd_proj.ppm, gd_proj.ppm / plate_proj.ppm))

    # ---- plate extent: the content bbox in world metres + a free margin ----
    hb = geom["hard_boundary"]
    pts_m = [(v[0] * u, v[1] * u) for v in hb["outer_ring"]["vertices_native"]]
    xs = [p[0] for p in pts_m]
    ys = [p[1] for p in pts_m]
    pad = WALL_BAND_THICKNESS_M
    bx0, bx1 = min(xs) - pad, max(xs) + pad
    by0, by1 = min(ys) - pad, max(ys) + pad
    W = int(math.ceil((bx1 - bx0) * plate_proj.ppm)) + 2 * MARGIN_PX
    H = int(math.ceil((by1 - by0) * plate_proj.ppm * plate_proj.sin_a)) \
        + 2 * MARGIN_PX
    # extra headroom for the islands' extrusion (a screen displacement)
    H += int(math.ceil(ISLAND_HEIGHT_M * plate_proj.ppm * plate_proj.cos_a))
    # ... and for the KP-18 (b) wall-face allowance, which rises UP-SCREEN off
    # the NORTH band.  Without this the plate has no room to hold the allowance
    # it declares — the first cut had a 96 px margin against a 363.7 px rise.
    # The whole addition goes on TOP: shift the world centre north by half.
    allow_px = WALL_FACE_ALLOWANCE_M * plate_proj.ppm * plate_proj.cos_a
    head = int(math.ceil(allow_px))
    H += head
    cy = (by0 + by1) / 2.0 - (head / 2.0) / (plate_proj.ppm * plate_proj.sin_a)
    plate = Rect(plate_proj, ((bx0 + bx1) / 2.0, cy), (W, H))
    print("[plate]  %d x %d px  ·  %.4f x %.4f m" %
          (W, H, plate.x1 - plate.x0, plate.y1 - plate.y0))

    # ---- rasterise the plate ----
    print("[raster] plate ...")
    p_idx, pool_rows, p_sq, p_pockets = build_index_map(plate, geom, u)
    print("  enclosed `beyond` pockets sealed into the wall mass: %d square px"
          % p_pockets)
    p_idx, p_allow_px_count, allow_k = sweep_wall_faces(p_idx, plate)
    print("  KP-18(b) wall-face allowance: %.3f m -> %.3f px up-screen; "
          "%d px claimed on the plate" % (WALL_FACE_ALLOWANCE_M, allow_k,
                                          p_allow_px_count))
    p_idx, p_elev, p_top, k_px = extrude_islands(p_idx, plate)
    figh = figure_heights(ppm_plate, oc)

    title_rows = [
        ("ppm_plate", "%.9f px/m   (authored; cliffside ortho canvas)"
         % ppm_plate),
        ("alpha", "%.10f deg   sin %.9f  cos %.9f"
         % (mock.ALPHA_DEG, plate_proj.sin_a, plate_proj.cos_a)),
        ("ground depth", "%.9f px per metre SOUTH (ppm*sin a)"
         % (ppm_plate * plate_proj.sin_a)),
        ("vertical", "%.9f px per metre UP (ppm*cos a)"
         % (ppm_plate * plate_proj.cos_a)),
        ("u  REGISTERED", "%.6f m per native minimap px (ledger KP-6)" % u),
        ("wall band", "%.2f m thick — DECLARED, no wire basis. INNER edge is "
                      "the measured ring." % WALL_BAND_THICKNESS_M),
        ("island height", "%.2f m — RULED KP-18(c), low stumps/rubble "
                          "(supersedes %.2f m); %.3f px up-screen"
         % (ISLAND_HEIGHT_M, ISLAND_HEIGHT_SUPERSEDED_M, k_px)),
        ("wall-face allow.", "<= %.1f m = %.3f px up-screen — KP-18(b), G5 "
                             "INTERIOR NAVE. Paintable elevation; TOP edge "
                             "free, BOTTOM is the frozen inner ring edge."
         % (WALL_FACE_ALLOWANCE_M, allow_k)),
        ("Banner aura", "r = %.1f m footprint at the frame origin — PLACEMENT "
                        "DECLARED-NOT-DECODED" % mock.BANNER_AURA_M),
        ("pools", "6 · radii are UPPER BOUNDS · enterable damage fields, "
                  "NEVER collide-blocking"),
        ("unwalked arcs", "2 · shape MEASURED, walkability NOT — dashed inner "
                          "edge, SOLID `wall` in the id mask"),
        ("CYAN", "ANNOTATION. Not a surface, not in the id mask. NEVER PAINT."),
        ("G5", "interior vs exterior is Matt's OPEN call — this guide is "
               "geometry only and dresses neither"),
        ("geometry", "crucible-arena-geometry-v1.json  sha %s"
         % mock.GEOM_SHA256[:12]),
    ]
    plate_img = guide_rgb(p_idx, p_elev, p_top, plate, geom, u, None,
                          title=title_rows)
    sx, sy = draw_scale_bars(plate_img, plate, ppm_plate)
    draw_figure_bars(plate_img, sx, sy, figh)
    out_plate = os.path.join(ROOT, "guide_plate_full.png")
    plate_img.save(out_plate, "PNG", optimize=True)
    print("  wrote guide_plate_full.png")

    # ---- the ONE review crop: 1920x1080 at ZOOM-GD, centred on the frame
    #      origin.  RE-RENDERED at ZOOM-GD from the same geometry and the same
    #      draw routine — NOT a resample of the plate.
    crop = Rect(gd_proj, (0.0, 0.0), (mock.VIEW_W, mock.VIEW_H))
    print("[raster] review crop ...")
    c_idx, _, _, c_pockets = build_index_map(crop, geom, u,
                                             pocket_source=(p_sq, plate))
    print("  pocket pixels resolved against the plate: %d" % c_pockets)
    c_idx, c_allow_count, _ = sweep_wall_faces(c_idx, crop)
    c_idx, c_elev, c_top, _ = extrude_islands(c_idx, crop)
    present = sorted({k for k, v in IDX.items() if (c_idx == v).any()})
    print("  classes present in the crop: %s" % ", ".join(present))
    print("  depth non-zero px: %d" % int((c_elev > 0).sum()))

    stamp = [
        "ARENA GREY-ROOM GUIDE — REVIEW CROP · ZOOM-GD %.6f px/m · u %.6f "
        "· alpha %.7f deg" % (gd_proj.ppm, u, mock.ALPHA_DEG),
        "world rect  x [%.6f, %.6f] m EAST   y [%.6f, %.6f] m SOUTH   "
        "centred on the frame origin (north gate)"
        % (crop.x0, crop.x1, crop.y0, crop.y1),
        "CYAN = annotation, never paint.  Grey = surface.  Every id-mask edge "
        "is frozen.  G5 undressed.",
    ]
    crop_img = guide_rgb(c_idx, c_elev, c_top, crop, geom, u, stamp)
    out_crop = os.path.join(ROOT, "guide_review_crop_1920x1080.png")
    crop_img.save(out_crop, "PNG", optimize=True)
    print("  wrote guide_review_crop_1920x1080.png")

    lut = np.zeros((len(IDX), 3), dtype=np.uint8)
    for k, v in ID_COLOUR.items():
        lut[k] = v
    out_mask = os.path.join(ROOT, "id_mask.png")
    Image.fromarray(lut[c_idx], "RGB").save(out_mask, "PNG", optimize=True)
    print("  wrote id_mask.png")

    out_depth = os.path.join(ROOT, "depth_mm.png")
    Image.fromarray(c_elev.astype("<u2"), mode="I;16").save(out_depth, "PNG",
                                                            optimize=True)
    print("  wrote depth_mm.png")

    # ---- the cathedral reference cut — READ ONLY, verbatim, native res ----
    src_sha = sha(FAR_RUINS)
    ref = Image.open(FAR_RUINS).convert("RGBA").crop(CATHEDRAL_BBOX)
    out_ref = os.path.join(ROOT, "ref_cathedral_far_ruins.png")
    ref.save(out_ref, "PNG")
    print("  wrote ref_cathedral_far_ruins.png  (%dx%d, native, no resample)"
          % ref.size)

    # ---- island sort lines (plate space + metres) ----
    islands = []
    for ob in hb["interior_obstructions"]:
        vm = [(v[0] * u, v[1] * u) for v in ob["vertices_native"]]
        pxs = [plate.to_px(*p) for p in vm]
        south_m = max(p[1] for p in vm)
        islands.append({
            "id": ob["id"],
            "footprint_vertices_m": [[round(a, 6), round(b, 6)] for a, b in vm],
            "footprint_bbox_m": [min(p[0] for p in vm), min(p[1] for p in vm),
                                 max(p[0] for p in vm), max(p[1] for p in vm)],
            "y_sort_line_world_y_m": south_m,
            "y_sort_line_plate_px_y": max(p[1] for p in pxs),
            "declared_height_m": ISLAND_HEIGHT_M,
            "top_face_offset_px_on_plate": k_px,
            "in_review_crop": False,
        })

    pools = []
    for z in geom["green_zones"]["zones"]:
        c_m = (z["interior_point_minimap_px"][0] * u,
               z["interior_point_minimap_px"][1] * u)
        pools.append({
            "id": z["id"],
            "centre_m": [round(c_m[0], 6), round(c_m[1], 6)],
            "radius_UPPER_BOUND_m": z["radius_upper_bound_px"] * u,
            "radius_upper_bound_native_px": z["radius_upper_bound_px"],
            "clipped_to_floor": True,
            "collision": "NONE — enterable damage field (geometry file "
                         "green_zones.class_note)",
        })

    # PAINT_NOTES is written BEFORE the manifest so the manifest can carry its
    # digest.  The manifest is the one output whose own sha it cannot hold.
    out_notes = write_paint_notes(ppm_plate, gd_proj, crop)
    print("  wrote PAINT_NOTES.md")

    outputs = {}
    for p in (out_plate, out_crop, out_mask, out_depth, out_ref, out_notes):
        row = {"sha256": sha(p), "bytes": os.path.getsize(p)}
        if p.endswith(".png"):
            row["size_px"] = list(Image.open(p).size)
        outputs[os.path.basename(p)] = row
    outputs["guide_manifest.json"] = {
        "sha256": "SELF — a manifest cannot carry its own digest; hash the "
                  "file on disk", "bytes": None}

    manifest = {
        "generated": "2026-09-20",
        "author": "drax (presentation seam), run KC2-PLAY Wave 1 addendum",
        "gate": "charter ledger KP-12 — the grey-room guide burst KP-B1a "
                "paints over",
        "burst_fired": False, "godot_launched": False, "new_art_minted": False,
        "writes_under_astra_burst": False,
        "generator": "make_arena_guide.py (imports make_g_img_mock.py for every "
                     "projection constant and the Projection class)",

        "px_per_m": {
            "ppm_plate": ppm_plate,
            "ppm_plate_source": "agentic_orchestration/drax/captures/"
                                "2026-09-13-cliffside-blockout/"
                                "blockout_meta_v2.json :: "
                                "ortho_canvas_v2.px_per_m_screen_x (R-C3-44)",
            "ppm_zoom_gd": gd_proj.ppm,
            "ppm_zoom_house": mock.Projection(
                mock.FRACTION_ZOOM_HOUSE, "ZOOM-HOUSE", u).ppm,
            "ratio_gd_over_plate": gd_proj.ppm / ppm_plate,
            "ratio_plate_over_gd": ppm_plate / gd_proj.ppm,
            "alpha_deg": mock.ALPHA_DEG,
            "sin_alpha": plate_proj.sin_a, "cos_alpha": plate_proj.cos_a,
            "plate_px_per_metre_east": ppm_plate,
            "plate_px_per_metre_south_ground": ppm_plate * plate_proj.sin_a,
            "plate_px_per_metre_up_screen": ppm_plate * plate_proj.cos_a,
            "u_registered_m_per_native_px": u,
            "u_window": list(mock.U_WINDOW),
            "h_fig_m": mock.H_FIG_M,
            "plate_equivalent_figure_fraction":
                ppm_plate * mock.H_FIG_M * plate_proj.cos_a / mock.VIEW_H,
            "cliffside_plate_law_cross_check": [
                {"quantity": k, "derived": g, "authored": w, "delta": abs(g - w)}
                for (k, g, w) in cross],
        },

        "register_divergence": dict(figh, status="RULED — KP-18 (a)", note=(
            "RAISED by drax as a conflict; RULED by the conductor. `h_fig` "
            "1.9 m STANDS (the ring/body and monster/body ratios are the feel). "
            "The cliffside's 130.000 px Keeper is a CLIFFSIDE CONVENTION, not a "
            "figure of record, and is NOT inherited — it is a register "
            "divergence row. The painter's scale figure for the arena is the "
            "Keeper cell at %.3f px on the plate (`b1a_scale_figure.png`). "
            "Recorded so the %.4f m the cliffside implies can never be quietly "
            "re-quoted as a body height."
            % (figh["arena_figure_px_on_plate"],
               figh["cliffside_implied_h_fig_m"]))),
        "wall_face_allowance": {
            "status": "RULED — KP-18 (b); Matt G5 = INTERIOR NAVE",
            "metres": WALL_FACE_ALLOWANCE_M,
            "px_up_screen_at_plate": allow_k,
            "class": "allowance (index 5)",
            "rule": "the painting may raise north/east/west wall faces into "
                    "`beyond` above the band. BOTTOM edge = the wall band's "
                    "inner edge, FROZEN. TOP edge = FREE. South face stays low "
                    "— enforced by the sweep direction (up-screen is north), "
                    "not by a list of faces.",
            "plate_px_claimed": p_allow_px_count,
            "canvas_note": "the plate canvas was GROWN by %d px on top to hold "
                           "this. The first cut had a 96 px margin against a "
                           "%.1f px rise — it declared an allowance it had no "
                           "room for." % (head, allow_k),
        },

        "plate": {
            "file": "guide_plate_full.png",
            "world_rect": plate.world_rect(),
            "margin_px": MARGIN_PX,
        },
        "review_crop": {
            "file": "guide_review_crop_1920x1080.png",
            "preset": "ZOOM-GD",
            "centre": "the frame origin = the north gate = native (0, 0) "
                      "(geometry frame.origin; the mock labels this point "
                      "'north gate (frame origin)')",
            "world_rect_m": crop.world_rect(),
            "derivation": "RE-RENDERED at ZOOM-GD from the same geometry and "
                          "the same draw routine — NOT a resample of "
                          "guide_plate_full.png.",
            "equivalent_plate_px_rect": {
                "x": plate.to_px(crop.x0, crop.y0)[0],
                "y": plate.to_px(crop.x0, crop.y0)[1],
                "w": (crop.x1 - crop.x0) * ppm_plate,
                "h": (crop.y1 - crop.y0) * ppm_plate * plate_proj.sin_a,
                "note": "the painting comes back at %.6f x plate scale and "
                        "must be UPSCALED %.6f x to land on the plate"
                        % (gd_proj.ppm / ppm_plate, ppm_plate / gd_proj.ppm)},
            "classes_present": present,
            "depth_nonzero_px": int((c_elev > 0).sum()),
            "annotation_stamp": "3 cyan lines, bottom-left; floor underneath; "
                                "paint over it",
        },
        "id_mask": {
            "file": "id_mask.png",
            "classes": {k: {"index": v, "rgb": list(ID_COLOUR[v]),
                            "hex": "#%02X%02X%02X" % ID_COLOUR[v]}
                        for k, v in IDX.items()},
            "note": "flat index colours, NEAREST only. NOT the cliffside "
                    "grey-room palette — #00FF00 is NOT void here; floor is "
                    "#2ECC40. Do not key on the cliffside convention.",
            "frozen": "every edge in this mask is frozen for the paint-over.",
            "enclosed_pocket_rule":
                "a fixed %.2f m band does not fill a wall spur thicker than "
                "%.2f m, so the spur's core first fell out as `beyond` — a "
                "black hole in the MIDDLE of a wall. Every `beyond` component "
                "that does not reach the outside world is reclassified `wall`. "
                "Enclosure is a GLOBAL fact, so the crop resolves its pockets "
                "AGAINST THE PLATE, not against its own border. Plate: %d "
                "square px sealed; crop: %d px."
                % (WALL_BAND_THICKNESS_M, 2 * WALL_BAND_THICKNESS_M,
                   p_pockets, c_pockets),
            "not_in_the_mask": ["the Vanguard Banner aura footprint",
                                "the frame-origin cross", "the ring edge line",
                                "the island contact lines", "all cyan text"],
        },
        "depth_mm": {
            "file": "depth_mm.png",
            "encoding": "uint16 PNG (I;16), value = MILLIMETRES OF ELEVATION "
                        "above the arena floor plane",
            "why_not_camera_distance":
                "the arena floor is ONE FLAT PLANE, so camera distance over it "
                "is an exact affine function of screen y and a map carries no "
                "information a constant does not. Elevation is the only "
                "non-trivial vertical fact, and at 53 deg oblique it is what "
                "displaces a surface up-screen: dy_px = h_m * ppm * cos(alpha).",
            "floor_plane_affine": {
                "screen_y_px_per_metre_south": ppm_plate * plate_proj.sin_a,
                "up_screen_px_per_metre_elevation":
                    ppm_plate * plate_proj.cos_a},
            "content": "island tops %d mm, island side faces ramp 0 -> %d mm, "
                       "everything else 0. The wall band is 0 because it is "
                       "drawn as a GROUND BAND, not an extruded wall — wall "
                       "height is G5-dependent and is not authored."
                       % (int(ISLAND_HEIGHT_M * 1000), int(ISLAND_HEIGHT_M * 1000)),
            "honest_limit": "for THIS crop the map is identically zero: no "
                            "island reaches the crop, and the wall that does "
                            "reach it carries 0 elevation by construction "
                            "(ground band, not extruded). So for the review "
                            "crop this file adds nothing the id mask does not "
                            "already carry. It is emitted for pipeline parity "
                            "with the cliffside guide, and it stops being "
                            "trivial the moment G5 rules interior and the wall "
                            "acquires a height.",
        },

        "declared_not_decoded": [
            {"what": "wall-band thickness", "value_m": WALL_BAND_THICKNESS_M,
             "why": "the minimap paints walkable floor only; nothing outside "
                    "the hard boundary is measured. INNER edge = the measured "
                    "ring (load-bearing). OUTER edge = free."},
            {"what": "island height", "value_m": ISLAND_HEIGHT_M,
             "why": "the geometry file carries 2-D polygons only. 1.0 m is "
                    "dressing-neutral: plinth or rubble mound, same sort line."},
            {"what": "Vanguard Banner PLACEMENT",
             "value_m": mock.BANNER_AURA_M,
             "why": "radius is model-bound (R-KP-0f); placement is not. Drawn "
                    "at the frame origin so it is visible, NOT a claim."},
            {"what": "pool extents",
             "why": "green_zones.geometry_provenance = INTERIOR-POINT-MEASURED "
                    "/ EXTENT-UNMEASURED. Radii are UPPER BOUNDS and the discs "
                    "are clipped to the floor polygon."},
            {"what": "the cathedral reference bbox",
             "value_px": list(CATHEDRAL_BBOX),
             "why": "hand-chosen framing on a first-party painted layer."},
        ],

        "scene_layer_conventions": {
            "authority": "canonical/reap-die-rise-game/painted-2d-pipeline/"
                         "scene-builder-workflow.md § 3 step 7 (T3l, R-C3-71)",
            "z_order": "foreground tiles (z0) < Shadows z1 < Actors z2 "
                       "(y-sorted) < Overhead z3 < near Parallax2D z4 "
                       "(scroll > 1) < Air z5",
            "the_painted_plate_is": "a FOREGROUND TILE at z0, below Shadows. It "
                                    "y-sorts against nothing.",
            "islands": islands,
            "island_y_sort_rule":
                "an island PAINTED INTO the plate cannot occlude an actor — it "
                "is z0 and actors are z2. If an island must occlude, it has to "
                "be cut as a separate y-sorted sprite in Actors with its sort "
                "line at the footprint's southernmost point (per island above). "
                "At a declared 1.0 m that occlusion is %.1f px — decide before "
                "the paint, not after." % k_px,
            "wall_band_collision": "NONE. The wall band is PAINT SURFACE ONLY. "
                                   "The runtime owns collision, at the measured "
                                   "ring polyline (the band's inner edge). "
                                   "Painting a wall does not make one.",
            "pools_collision": "NONE, and this is a hard rule: the zones are "
                               "ENTERABLE DAMAGE FIELDS, never collide-blocking "
                               "(geometry file green_zones.class_note, Matt "
                               "attestation L-64).",
            "beyond_the_wall": "BLACK on this guide. It is the parallax "
                               "layers' region (scroll 0.12 / 0.25 / 0.45 / "
                               "0.70) and is NOT painted into the plate.",
            "pools_data": pools,
        },

        "cathedral_reference": {
            "file": "ref_cathedral_far_ruins.png",
            "source": "astra_test_01/burst/runs/C-7/cliffside_v45/parallax/"
                      "layers/far_ruins.png",
            "source_sha256": src_sha,
            "source_size_px": [2784, 1834],
            "bbox_lrtb_native_px": list(CATHEDRAL_BBOX),
            "cut_size_px": list(ref.size),
            "resample": "NONE — verbatim native-resolution cut, RGBA, alpha "
                        "255 everywhere in this region",
            "subject": "the lower-left burning gothic cathedral of the "
                       "cliffside far_ruins layer (C-3 R-C3-72 / CS-cathedral), "
                       "framed with both banner columns and its terrace",
            "use": "FIRST-PARTY reference for the H1 register and the "
                   "building's identity. Register only — it is a PARALLAX "
                   "layer asset and its scale is not this plate's scale.",
            "read_only": True,
        },

        "outputs": outputs,
        "substrate": {
            "arena_geometry_sha256": mock.GEOM_SHA256,
            "far_ruins_sha256": src_sha,
            "blockout_meta": "agentic_orchestration/drax/captures/"
                             "2026-09-13-cliffside-blockout/blockout_meta_v2.json",
        },
    }
    out_man = os.path.join(ROOT, "guide_manifest.json")
    with open(out_man, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print("  wrote guide_manifest.json")

    # =======================================================================
    # THE B1a PAINT CHUNK (ledger KP-19) + the lane reference set
    # =======================================================================
    print("\n[b1a] chunk (KP-19: art leads the boundary) ...")
    (chunk, b_id, b_guide, b_annot, b_fig, floor_rgb, pools_in, n_pool,
     fig_h_px, fig_base_y) = build_b1a_chunk(geom, u, plate_proj, figh,
                                             ppm_plate)
    print("  world rect x [%.4f, %.4f] m EAST  y [%.4f, %.4f] m SOUTH"
          % (chunk.x0, chunk.x1, chunk.y0, chunk.y1))
    print("  pools reaching the chunk: %s (%d px)" % (", ".join(pools_in),
                                                      n_pool))
    b_out = {}
    for name, im, mode in (("b1a_guide_1536x1024.png", b_guide, "PNG"),
                           ("b1a_id_1536x1024.png", b_id, "PNG"),
                           ("b1a_annot.png", b_annot, "PNG"),
                           ("b1a_scale_figure.png", b_fig, "PNG")):
        p = os.path.join(ROOT, name)
        im.save(p, mode, optimize=True)
        b_out[name] = p
        print("  wrote %s  %dx%d" % (name, im.width, im.height))

    # the register exemplar — a native-scale crop of a cliffside painted
    # foreground tile (floor + rim rock + warm upper-left light)
    tile_src = os.path.join(COLLAB, TILE_SRC)
    tile = Image.open(tile_src).convert("RGBA").crop(TILE_CROP)
    opaque = float((np.asarray(tile)[:, :, 3] > 0).mean())
    if opaque < 1.0:
        sys.exit("REGISTER EXEMPLAR ABORT: the tile crop is %.1f %% opaque. An "
                 "exemplar with void in it teaches the void, not the register."
                 % (opaque * 100.0))
    print("  tile crop opacity ASSERTED at %.1f %%" % (opaque * 100.0))

    # ---- the lane reference set the burst consumes (KP-19) ----
    refs = os.path.join(COLLAB, REFS_DIR)
    os.makedirs(refs, exist_ok=True)
    # The exemplar is a LANE reference, not a capture artifact, so it is
    # written straight into the reference root — one copy, not two.  At 3.4 MB
    # a second identical copy in the captures dir would be bytes for nothing.
    p_tile = os.path.join(refs, "ref_cliffside_tile_crop.png")
    tile.save(p_tile, "PNG")
    print("  wrote %s  (%dx%d, native, no resample)"
          % (os.path.relpath(p_tile, COLLAB), tile.width, tile.height))

    ref_set = [b_out["b1a_guide_1536x1024.png"], b_out["b1a_annot.png"],
               b_out["b1a_scale_figure.png"], out_ref]
    copied = [os.path.relpath(p_tile, COLLAB)]
    for src in ref_set:
        dst = os.path.join(refs, os.path.basename(src))
        shutil.copyfile(src, dst)
        copied.append(os.path.relpath(dst, COLLAB))
    copied.sort()
    print("  reference set: %d files in %s" % (len(copied), REFS_DIR))

    b_outputs = {}
    for p in list(b_out.values()) + [p_tile] + \
            [os.path.join(refs, os.path.basename(s)) for s in ref_set]:
        b_outputs[os.path.relpath(p, COLLAB)] = {
            "sha256": sha(p), "bytes": os.path.getsize(p),
            "size_px": list(Image.open(p).size)}

    b_manifest = {
        "generated": "2026-09-20",
        "author": "drax (presentation seam), run KC2-PLAY Wave 1 addendum",
        "gate": "conductor ledger KP-19 — Matt's ruling on the mock: "
                "ART LEADS THE BOUNDARY",
        "supersedes": "the KP-18 chunk brief (wall band + wall-face allowance "
                      "class + `beyond` in the chunk mask). See "
                      "kp18_chunk_infeasibility below — that brief was also "
                      "GEOMETRICALLY UNBUILDABLE, independently of KP-19.",
        "burst_fired": False, "godot_launched": False, "new_art_minted": False,

        "chunk": {
            "guide": "b1a_guide_1536x1024.png",
            "id": "b1a_id_1536x1024.png",
            "annot": "b1a_annot.png",
            "scale_figure": "b1a_scale_figure.png",
            "size_px": [CHUNK_W, CHUNK_H],
            "ppm_plate": ppm_plate,
            "alpha_deg": mock.ALPHA_DEG,
            "px_per_metre_east": ppm_plate,
            "px_per_metre_south_ground": ppm_plate * plate_proj.sin_a,
            "px_per_metre_up_screen": ppm_plate * plate_proj.cos_a,
            "u_registered_m_per_native_px": u,
            "world_rect_m": chunk.world_rect(),
            "gate_position_px": [CHUNK_W / 2.0, GATE_Y_FRAC * CHUNK_H],
            "gate_position_note": "native (0,0), the north gate, ASSERTED at "
                                  "the horizontal centre and %.2f of the "
                                  "height" % GATE_Y_FRAC,
            "paints_at": "PLATE SCALE — KP-18(d). No round-trip: the painting "
                         "lands on the plate 1:1, no upscale.",
            "depth_map": "NOT EMITTED. Under KP-19 the chunk is one flat floor "
                         "plane with no authored elevation, so an elevation "
                         "map would be identically zero and a camera-distance "
                         "map is an exact affine function of screen y "
                         "(%.9f px per metre SOUTH). Both are stated here "
                         "instead of shipped as a constant image."
                         % (ppm_plate * plate_proj.sin_a),
        },

        "id_palette": {
            "convention": "the CLIFFSIDE grey-room convention (Astra's habit). "
                          "The grey-room colours are READ from the cliffside "
                          "blockout's own layer_id.legend_rgb8, not retyped.",
            "source": "agentic_orchestration/drax/captures/"
                      "2026-09-13-cliffside-blockout/blockout_meta.json :: "
                      "layer_id.legend_rgb8",
            "classes": [
                {"class": "floor", "rgb": list(floor_rgb),
                 "hex": "#%02X%02X%02X" % floor_rgb,
                 "origin": "cliffside `path` — the walkable ground surface",
                 "frozen": "YES — this is the floor PLANE and its SCALE. The "
                           "plane is frozen; no boundary is."},
                {"class": "pool", "rgb": list(B1A_POOL_RGB),
                 "hex": "#%02X%02X%02X" % B1A_POOL_RGB,
                 "origin": "ARENA EXTENSION — the cliffside has no damage "
                           "fields, so no legend colour exists to inherit",
                 "frozen": "NO — SUGGESTED hazard. Positions and radii come "
                           "from the geometry as a STARTING POINT (radii are "
                           "UPPER BOUNDS, extent unmeasured)."},
            ],
            "reserved_not_present": [
                {"class": "void / beyond", "hex": "#00FF00",
                 "why": "the lane's void colour, reserved so Astra's habit "
                        "stays safe. There is NO void in this chunk — KP-19 "
                        "makes the whole chunk paintable."},
                {"class": "island", "hex": "#%02X%02X%02X" % B1A_ISLAND_RGB,
                 "why": "arena extension, defined but not present: no island "
                        "reaches this chunk."},
                {"class": "wall band / wall-face allowance",
                 "hex": "#%02X%02X%02X / #%02X%02X%02X"
                        % (tuple(read_cliffside_legend()["cliff_rock"])
                           + tuple(read_cliffside_legend()["near_rock"])),
                 "why": "REMOVED BY KP-19. Would have been the cliffside's "
                        "`cliff_rock` (light grey = rim verge / rock top) and "
                        "`near_rock` (dark grey = faces). Kept here so the "
                        "mapping is on record if the boundary is ever frozen "
                        "again."},
            ],
            "hazard": "this chunk's palette is NOT the palette of "
                      "`id_mask.png` in this same directory (that one is the "
                      "geometry record and uses flat index colours). Two "
                      "palettes, two purposes — do not cross them.",
        },

        "annotation_overlay": {
            "file": "b1a_annot.png",
            "rule": "NOT PAINT. Nothing in it is a surface and nothing in it "
                    "is in the id mask.",
            "contains": ["the suggested ring boundary (dashed cyan)",
                         "the two mapped-but-never-walked arcs (dashed red)",
                         "the island contact lines (dashed dim cyan)",
                         "the Vanguard Banner aura footprint (dashed amber)",
                         "the north-gate origin cross + label",
                         "the caption block"],
            "why_separate": "KP-19 (2). In the first cut these lived in the "
                            "guide RGB, where nothing but a colour convention "
                            "stopped a paint-over baking them in.",
        },

        "scale_figure": {
            "file": "b1a_scale_figure.png",
            "subject": "the Keeper idle S cell, first-party, already on disk",
            "source": os.path.relpath(mock.KEEPER_CELL, COLLAB),
            "height_px": fig_h_px,
            "height_basis": "h_fig %.1f m * ppm_plate * cos(alpha) — KP-18(a): "
                            "1.9 m STANDS; the cliffside's 130 px is a "
                            "cliffside convention and is NOT inherited"
                            % mock.H_FIG_M,
            "height_convention": "the scaled height is the cell's ALPHA BBOX "
                                 "height, the same convention the G-IMG mock "
                                 "uses (`load_keeper`). The Keeper carries a "
                                 "staff, so the bbox is the silhouette's, not "
                                 "strictly the body's — stated rather than "
                                 "implied. If the painter needs body-only, the "
                                 "baseline mark is the reliable datum.",
            "background": "flat #%02X%02X%02X (lane void)" % B1A_VOID_RGB,
            "baseline_mark": {"row_px": fig_base_y, "width_px": 1,
                              "rgb": [255, 0, 255],
                              "meaning": "the figure's FOOT — where the body "
                                         "meets the floor plane"},
            "use": "IMAGE 2 for the painter. This is the only scale device in "
                   "the set; the guide RGB carries no grid and no text.",
        },

        "mask_from_paint": {
            "status": "OWED after Matt passes a painting (KP-19 (4))",
            "recommendation": "MY OWN SCRIPT, with Matt-judged thresholds — "
                              "NOT a CHECK burst.",
            "why": "the instrument has to be RE-RUNNABLE and DETERMINISTIC. A "
                   "derived collision mask is not a one-off opinion about a "
                   "picture: every repaint re-derives it, and a boundary that "
                   "changes because a model was sampled twice is a boundary "
                   "nobody can debug. A CHECK burst gives a judgement; a "
                   "script gives a function.",
            "instrument": [
                "1. Astra paints on flat #00FF00 OUTSIDE the nave (the lane's "
                "own isolation convention, R-C3-62/64) — so 'not floor' is "
                "keyed, not guessed. This is the single cheapest thing that "
                "makes the rest reliable and it costs the painter nothing.",
                "2. Key the void -> raw blocked mask; morphological close/open "
                "at a Matt-judged radius in METRES (not px) to kill speckle.",
                "3. Largest connected walkable component from the gate; fill "
                "enclosed pockets (the same rule this script already runs on "
                "the wall band).",
                "4. Pools: keep the SUGGESTED discs unless the painting moved "
                "them; if it did, key the painted hazard colour instead.",
                "5. Emit walkable.json in the lane's existing exporter shape "
                "(runs/C-7/cliffside_v45/parallax/walkable.json), so the "
                "runtime consumes it with no new code, + an overlay PNG for "
                "Matt to eyeball.",
                "6. Gate: a headless edge-escape probe, the cliffside's own "
                "probe_move.gd (workflow § 3 step 2/10).",
            ],
            "cost": "~half a session to build against the first painting, "
                    "then ~minutes per repaint. No model calls, no burst "
                    "budget, no Grok. The one thing it NEEDS from the burst "
                    "is clause 1 — paint the outside on #00FF00. Without that "
                    "I am thresholding a painting's luminance, which is a "
                    "guess dressed as a measurement, and I will not ship it.",
            "if_clause_1_is_refused": "then a CHECK burst is the honest "
                                      "fallback, because a human-or-model "
                                      "judgement openly labelled as one beats "
                                      "a threshold pretending to be geometry.",
        },

        "kp18_chunk_infeasibility": {
            "finding": "the KP-18 chunk brief could not have been built, and "
                       "this was MEASURED before KP-19 arrived.",
            "required": "the north gate at lower-middle AND >= %.2f px of "
                        "`beyond` above the wall band, inside 1536x1024 at "
                        "plate scale." % (WALL_FACE_ALLOWANCE_M * ppm_plate
                                          * plate_proj.cos_a),
            "measured": "a 1536x1024 chunk with the gate at %.2f of the height "
                        "contains ZERO `beyond` pixels. The gate is deep "
                        "inside the arena: the nearest `beyond` straight up "
                        "from the origin is 2473 px (~30.8 m). The nearest "
                        "wall pixel anywhere on the plate with a full 6 m of "
                        "`beyond` above it is 1361.6 px away (dx -5.146 m, "
                        "dy -15.68 m) — outside any chunk holding the gate."
                        % GATE_Y_FRAC,
            "disposition": "MOOT, not wrong — KP-19 removes the requirement. "
                           "Recorded because an escalation overtaken by events "
                           "still needs a disposition, and because the same "
                           "arithmetic will bite again if a future brief asks "
                           "for a wall face near the gate.",
        },

        "outputs": b_outputs,
        "lane_reference_set": {
            "dir": REFS_DIR,
            "pattern": "a NEW per-run dir, the C-6-beside-C-7 pattern, "
                       "authorised by the conductor (KP-19)",
            "manifest_covered": False,
            "manifest_check": "astra_test_01/burst/MANIFEST.sha256 carries no "
                              "runs/ entries; nothing under lane/, export/, "
                              "tests/ or bible/ was touched",
            "files": copied,
        },
    }
    p_bman = os.path.join(ROOT, "b1a_manifest.json")
    with open(p_bman, "w") as fh:
        json.dump(b_manifest, fh, indent=2)
    print("  wrote b1a_manifest.json")

    print("\n[figure] arena h_fig %.1f m -> %.3f px on the plate; cliffside "
          "Keeper %.3f px -> implies %.4f m (ratio %.6f)"
          % (figh["arena_h_fig_m"], figh["arena_figure_px_on_plate"],
             figh["cliffside_keeper_px_on_plate"],
             figh["cliffside_implied_h_fig_m"], figh["ratio_cliffside_over_arena"]))
    print("DONE.")


# ===========================================================================
# 5 · THE B1a PAINT CHUNK — conductor ledger KP-19, "ART LEADS THE BOUNDARY"
#
#     Matt's ruling on the mock: the video-measured ring is a SUGGESTION.  The
#     painting places the nave's structures where they fit and the playable
#     boundary is DERIVED from the painting afterwards.  So this chunk's id
#     mask carries ONLY what is frozen — the floor plane and the pools as
#     SUGGESTED hazards.  No wall band, no allowance class, no `beyond`: the
#     whole chunk is paintable.  Everything geometric moves to the annotation
#     overlay.  SCALE STAYS TRUE even though the boundary does not.
# ===========================================================================

GATE_Y_FRAC = 0.78          # free layout: the gate sits in the lower middle
CHUNK_W, CHUNK_H = 1536, 1024      # the lane's chunk size (R-C3-45/46)
TILE_SRC = os.path.join("astra_test_01", "burst", "runs", "C-7",
                        "cliffside_v45", "parallax", "tiles", "tile_0_0.png")
# DECLARED framing: a 100 %-opaque window of the cliffside's painted foreground
# tile, chosen by SEARCHING the tile's alpha for full coverage (the first cut
# was 40 % transparent — an exemplar of the void, not of the register).  Cut at
# the chunk's own size so the painter compares like with like.
TILE_CROP = (1792, 1792, 1792 + CHUNK_W, 1792 + CHUNK_H)
REFS_DIR = os.path.join("astra_test_01", "burst", "runs", "KC2-PLAY",
                        "artifacts", "B1a-refs")


def read_cliffside_legend():
    """The cliffside grey-room class colours, READ from the blockout's own
    `layer_id.legend_rgb8`.  Astra's habit lives here; it is not retyped."""
    with open(BLOCKOUT_META_V1) as fh:
        return json.load(fh)["layer_id"]["legend_rgb8"]


def build_b1a_chunk(geom, u, plate_proj, figh, ppm_plate):
    legend = read_cliffside_legend()
    floor_rgb = tuple(legend["path"])          # the cliffside's walkable ground
    # Origin (native 0,0 = the north gate) at (W/2, GATE_Y_FRAC*H).
    cy = -(GATE_Y_FRAC - 0.5) * CHUNK_H / (plate_proj.ppm * plate_proj.sin_a)
    chunk = Rect(plate_proj, (0.0, cy), (CHUNK_W, CHUNK_H))
    ox, oy = chunk.to_px(0.0, 0.0)
    assert abs(ox - CHUNK_W / 2.0) < 1e-6, "gate not horizontally centred"
    assert abs(oy - GATE_Y_FRAC * CHUNK_H) < 1e-6, "gate not in the lower third"

    # ---- id: floor everywhere, pools as SUGGESTED hazards ----
    idx = np.full((CHUNK_H, CHUNK_W), 1, dtype=np.uint8)      # 1 = floor
    pool_img = Image.new("L", (CHUNK_W, CHUNK_H), 0)
    pd = ImageDraw.Draw(pool_img)
    pools_in = []
    for z in geom["green_zones"]["zones"]:
        cx, cyp = chunk.to_px(z["interior_point_minimap_px"][0] * u,
                              z["interior_point_minimap_px"][1] * u)
        rx, ry = plate_proj.r_to_semiaxes(z["radius_upper_bound_px"] * u)
        pd.ellipse([cx - rx, cyp - ry, cx + rx, cyp + ry], fill=1)
        if cx + rx > 0 and cx - rx < CHUNK_W and cyp + ry > 0 and \
                cyp - ry < CHUNK_H:
            pools_in.append(z["id"])
    idx[np.asarray(pool_img) == 1] = 2                        # 2 = pool
    n_pool = int((idx == 2).sum())

    lut = np.zeros((3, 3), dtype=np.uint8)
    lut[1] = floor_rgb
    lut[2] = B1A_POOL_RGB
    id_img = Image.fromarray(lut[idx], "RGB")

    # ---- guide RGB: flat floor + hatched pools.  NOTHING ELSE. ----
    g = np.zeros((CHUNK_H, CHUNK_W, 3), dtype=np.uint8)
    g[:] = GUIDE_GREY[1]
    g[idx == 2] = GUIDE_GREY[4]
    hatch = Image.new("L", (CHUNK_W, CHUNK_H), 0)
    hd = ImageDraw.Draw(hatch)
    pitch = max(8, int(round(plate_proj.ppm * 0.35)))
    for c in range(-CHUNK_H, CHUNK_W, pitch):
        hd.line([(c, 0), (c + CHUNK_H, CHUNK_H)], fill=255, width=2)
    g[(np.asarray(hatch) > 0) & (idx == 2)] = C_HATCH
    guide_img = Image.fromarray(g, "RGB")

    # ---- annotation overlay: everything geometric, on transparency ----
    an = Image.new("RGBA", (CHUNK_W, CHUNK_H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(an)
    hb = geom["hard_boundary"]

    def px(nx, ny):
        return chunk.to_px(nx * u, ny * u)

    # 1 m GROUND GRID.  KP-19 leaves the paint guide a flat grey rectangle —
    # true to scale and mute about it.  The grid is the only thing that shows
    # a painter the 53 deg oblique (1 m EAST and 1 m SOUTH are different
    # lengths on screen), so it belongs here, in the overlay, where a
    # paint-over cannot bake it in.  Lines are DERIVED, not drawn by eye.
    step_x = plate_proj.ppm
    step_y = plate_proj.ppm * plate_proj.sin_a
    grid = (C_ANNO_DIM[0], C_ANNO_DIM[1], C_ANNO_DIM[2], 46)
    k = 0
    while ox - k * step_x > 0 or ox + k * step_x < CHUNK_W:
        for gx in ({ox - k * step_x, ox + k * step_x}):
            if 0 <= gx <= CHUNK_W:
                ad.line([(gx, 0), (gx, CHUNK_H)], fill=grid, width=1)
        k += 1
    k = 0
    while oy - k * step_y > 0 or oy + k * step_y < CHUNK_H:
        for gy in ({oy - k * step_y, oy + k * step_y}):
            if 0 <= gy <= CHUNK_H:
                ad.line([(0, gy), (CHUNK_W, gy)], fill=grid, width=1)
        k += 1

    ring = [px(*v) for v in hb["outer_ring"]["vertices_native"]]
    walked, unw = mock.split_ring(ring, hb["unwalked_arcs"], len(ring))
    for run in walked:
        mock.dashed_path(ad, run, C_ANNO + (255,), 3, dash=16, gap=12)
    unw_here = False
    for run in unw:
        if any(0 <= p[0] <= CHUNK_W and 0 <= p[1] <= CHUNK_H for p in run):
            unw_here = True
        mock.dashed_path(ad, run, (236, 108, 108, 255), 3, dash=10, gap=9)
    for ob in hb["interior_obstructions"]:
        pts = [px(*v) for v in ob["vertices_native"]]
        mock.dashed_path(ad, pts + [pts[0]], C_ANNO_DIM + (255,), 2, 8, 7)
    bx, by = plate_proj.r_to_semiaxes(mock.BANNER_AURA_M)
    mock.dashed_path(ad, mock.ellipse_pts(ox, oy, bx, by, 500),
                     (214, 148, 46, 255), 2, dash=14, gap=11)
    r = 26
    ad.line([(ox - r, oy), (ox + r, oy)], fill=C_ANNO + (255,), width=3)
    ad.line([(ox, oy - r), (ox, oy + r)], fill=C_ANNO + (255,), width=3)
    ad.text((ox + r + 8, oy - 26), "NORTH GATE — frame origin, native (0,0)",
            font=mock.font(20, bold=True), fill=C_ANNO + (255,))
    cap = [
        "ANNOTATION OVERLAY — NOT PAINT, NOT A SURFACE.",
        "DASHED RING = SUGGESTED BOUNDARY — ART LEADS (ledger KP-19).",
        "  The painting places the nave where it fits; the playable mask is",
        "  DERIVED FROM THE PAINTING afterwards.",
        "  Amber = Vanguard Banner aura r %.1f m, placement DECLARED-NOT-"
        % mock.BANNER_AURA_M,
        "  DECODED — a runtime overlay, never paint." +
        ("  Red = the two arcs mapped but never walked." if unw_here else
         "  (no unwalked arc reaches this chunk.)"),
        "FAINT GRID = 1 m on the GROUND: %.3f px EAST, %.3f px SOUTH. They "
        "differ — that is the 53 deg oblique." % (step_x, step_y),
        "SCALE IS TRUE AND IS NOT A SUGGESTION: %.6f px/m, alpha %.7f deg."
        % (ppm_plate, mock.ALPHA_DEG),
        "world rect  x [%.4f, %.4f] m EAST   y [%.4f, %.4f] m SOUTH"
        % (chunk.x0, chunk.x1, chunk.y0, chunk.y1),
    ]
    f = mock.font(17, mono=True)
    yy = CHUNK_H - 16 - 20 * len(cap)
    for ln in cap:
        ad.text((16, yy), ln, font=f, fill=C_ANNO + (255,))
        yy += 20

    # ---- scale figure: the Keeper cell at the arena's figure height ----
    h_px = figh["arena_figure_px_on_plate"]
    kp = Image.open(mock.KEEPER_CELL).convert("RGBA")
    kp = kp.crop(kp.getbbox())
    s = h_px / kp.height
    kp = kp.resize((max(1, int(round(kp.width * s))),
                    max(1, int(round(h_px)))), Image.LANCZOS)
    pad = 48
    fig = Image.new("RGBA", (kp.width + 2 * pad, kp.height + pad + 40),
                    B1A_VOID_RGB + (255,))
    fig.alpha_composite(kp, (pad, pad // 2))
    base_y = pad // 2 + kp.height - 1          # the figure's foot row
    ImageDraw.Draw(fig).line([(0, base_y), (fig.width, base_y)],
                             fill=(255, 0, 255, 255), width=1)
    return (chunk, id_img, guide_img, an, fig.convert("RGB"), floor_rgb,
            pools_in, n_pool, h_px, base_y)


# ---- the 6-line brief note, emitted so its numbers cannot drift ----
def write_paint_notes(ppm_plate, gd_proj, crop):
    notes = [
        "# PAINT_NOTES — arena grey-room guide (KP-B1a, ONE image, then HALT)",
        "1. FLOOR = #2ECC40 in `id_mask.png` (flat grey in the guide): the "
        "walkable arena plate. WALL = #FF4136: paint surface only, %.2f m band, "
        "DECLARED thickness — the runtime owns collision at its inner edge. "
        "ISLAND = #0074D9 (raised %.2f m, DECLARED). POOL = #FFDC00: enterable "
        "damage fields, NEVER walls. BEYOND = #000000: leave black, the "
        "parallax layers own it."
        % (WALL_BAND_THICKNESS_M, ISLAND_HEIGHT_M),
        "2. MAY BE EMBELLISHED, freely and within the class: surface (stone, "
        "grit, cracks, stain, wear), rubble and debris that does not read as "
        "an obstacle, light and its falloff, the fire register of the "
        "reference. Paint the picture, not the diagram.",
        "3. MAY NOT MOVE: every edge in `id_mask.png` — the ring's inner edge, "
        "the wall band, the four island footprints, the six pool discs. The "
        "painting must register 1:1 with the mask at %d x %d. A moved edge is a "
        "moved distance and the geometry is measured."
        % (mock.VIEW_W, mock.VIEW_H),
        "4. CYAN (#00FFFF) IS ANNOTATION, NOT SURFACE: the frame-origin cross, "
        "the ring edge line, the island contact lines, the Vanguard Banner "
        "aura footprint (r %.1f m, placement DECLARED not decoded) and all "
        "text. Paint floor straight over them — but do NOT bake the Banner "
        "ring into the floor: it is a runtime overlay."
        % mock.BANNER_AURA_M,
        "5. REGISTER: `ref_cathedral_far_ruins.png` — a native cut from the "
        "cliffside's own far_ruins layer, bbox %s, the burning gothic "
        "cathedral (R-C3-72 / CS-cathedral). Match its H1 line register and "
        "its identity. It is a PARALLAX asset: copy the register, not the "
        "scale." % (list(CATHEDRAL_BBOX),),
        "6. DO NOT DRESS G5: interior nave vs exterior arena is Matt's open "
        "call. Plate scale %.6f px/m; this crop is ZOOM-GD %.6f px/m; world "
        "rect x [%.4f, %.4f] m EAST, y [%.4f, %.4f] m SOUTH, centred on the "
        "frame origin (north gate)."
        % (ppm_plate, gd_proj.ppm, crop.x0, crop.x1, crop.y0, crop.y1),
    ]
    out = os.path.join(ROOT, "PAINT_NOTES.md")
    with open(out, "w") as fh:
        fh.write("\n\n".join(notes) + "\n")
    return out


if __name__ == "__main__":
    main()
