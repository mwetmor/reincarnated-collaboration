#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KC2-PLAY · G-IMG FIRST-FRAME MOCK  (charter § 6.1, ledger KP-3 — Matt's first-image gate)

Composes TWO 1920x1080 PNGs — one at ZOOM-GD, one at ZOOM-HOUSE — WITHOUT any
Astra/codex burst, without Godot, and without minting one pixel of new art.

WHAT IS TRUE IN THIS IMAGE AND WHAT IS NOT
------------------------------------------
  GEOMETRY IS TRUE.  Every distance on these frames is COMPUTED here from the
  projection law of `2026-09-20-kc2-play-2d-retarget-spec.md` § 1.1/§ 1.2 as
  amended by its two Corrigenda-Forward, applied to the video-measured arena
  geometry (`crucible-arena-geometry-v1.json`, sha256 68d895d7...) and to the
  v3.1 model pack's own values.  No screen dimension below is typed.

  ART IS FAKE.  The Keeper cell is a first-party sprite already on disk; monster
  tokens are flat tinted silhouettes; the HUD is a wireframe.  Nothing here is a
  render and nothing here is a canon-camera candidate (2D spec § 7).

LAW OBSERVED
------------
  Law 3   — no fitted constants; every constant below is either cited to a
            document, or DERIVED in the open, or DECLARED as a placeholder on
            the face of the image itself.
  GL-6    — the geometry file and every pack member read here is digest-verified
            before use; a mismatch aborts, it does not warn.
  GL-10   — the wire's constant is used, never re-derived (alpha, EoR radius_m).
  GL-12   — an absence is DECLARED.  v3.1 carries NO monster body radius; the
            token radii are placeholders and the image says so.
  R-KP-0c — `u` is a registered runtime choice inside [0.22277, 0.3663]
            (R-L3-2).  The REGISTERED value is u = 0.285 (conductor ledger
            KP-6); it is asserted in-window at run time and both are printed.

Author: drax (presentation seam), run KC2-PLAY Wave 1, 2026-09-20.
Usage:  python3 make_g_img_mock.py
"""

import hashlib
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

# ===========================================================================
# 0 · CONSTANTS OF RECORD — the ONLY typed numbers, each with its citation.
#     Everything that reaches a pixel is derived from these.
# ===========================================================================

# 2D spec § 1.1 — the ratified GD `player_lock` pitch.  GL-10: the wire's
# constant, NOT 53 deg.
ALPHA_DEG = 52.9535411256029

# 2D spec § 1.2 + Corrigendum-Forward 1 + charter ledger KP-0e (conductor
# ruling on OQ-2): the arena scale chain's own `character_height_m_ASSUMED`.
# One character height governs both halves of the projection or neither is
# trustworthy.
H_FIG_M = 1.9

# F4 ruled register — 2D spec § 1.2.  D3 measured 8.02 % figure as the
# GD-matched default; house 17 % on the F4 toggle.
FRACTION_ZOOM_GD = 0.0802
FRACTION_ZOOM_HOUSE = 0.17

# Delivery frame.
VIEW_W, VIEW_H = 1920, 1080

# R-L3-2 (LIFT ledger L-3, finding D-W1-1) — window of record for `u`,
# metres per native minimap px.  The geometry file's own point estimate
# 0.1981 is EXCLUDED by this window and is NOT used here (WARN-8).
U_WINDOW = (0.22277, 0.3663)

# ⚑ THE REGISTERED `u` — ledger KP-6, conductor, 2026-09-20: galadriel's W1
# rider folded and **u = 0.285 ADOPTED as the registered runtime choice**.
# This SUPERSEDES the window midpoint (0.294535) that this script used at its
# first cut; the midpoint is retained below only as the superseded lineage
# value so the change is legible rather than silent.
#
# ⚠ PROVENANCE NOTE, recorded because it matters: drax received KP-6 in a
# conductor message ADDRESSED TO GALADRIEL, not in a dispatch to this seat.
# It is acted on here because a ruling of record governs whoever consumes it —
# but per the charter's own conflict rule ("a posture communicated to one
# session is not a posture the wave has"), the conductor should ratify u=0.285
# against the WAVE, not only in the seat that received it.
U_REGISTERED = 0.285
U_SUPERSEDED_MIDPOINT = (U_WINDOW[0] + U_WINDOW[1]) / 2.0

# Charter R-KP-0f — the Vanguard Banner's aura.  MODEL-BOUND radius;
# its PLACEMENT is DECLARED-not-decoded and is labelled as such on the frame.
BANNER_AURA_M = 8.0

# Substrate pins.
GEOM_SHA256 = "68d895d75702996473cfd654a9a834816d4be0421c4b5ad7a3d2a0cc5d40481f"
PACK_DIGEST = "2c7fc61f6a6f4efa61e535ad504929e0c94c78e3e8ed9f14eaaa13dbaf1cf4a7"

# Published cross-check values, asserted against what this script derives.
# These are NOT used to draw anything — they exist so that a silent arithmetic
# regression in the derivation cannot pass as a green.  (2D spec
# Corrigendum-Forward 1 item 1 and Corrigendum-Forward 2.)
EXPECT = {
    "ppm_gd": 75.668,
    "ppm_house": 160.394,
    "fig_px_gd": 86.616,
    "fig_px_house": 183.600,
    "eor_semi_x_gd": 227.0,
    "eor_semi_y_gd": 181.2,
}

# ---------------------------------------------------------------------------
# PLACEHOLDER DECLARATIONS (GL-12) — no wire basis; printed on the image.
# ---------------------------------------------------------------------------
# v3.1's model/monsters.json carries NO body-radius / size / footprint key
# (31 distinct keys, zero matching).  The single 0.62 m figure below is the
# example value printed in 2D spec § 2.1's snapshot, used here as the M-class
# anchor; S/L/hero are scaled from it by a declared ratio.  ALL FOUR ARE
# PLACEHOLDERS and the legend says so.
TOKEN_RADIUS_M = {"S": 0.62 * 0.72, "M": 0.62, "L": 0.62 * 1.55, "HERO": 0.62 * 2.1}
# Declared silhouette HEIGHT in metres per class.  Height is pure art — only the
# FOOTPRINT radius above is a (placeholder) spatial claim.  Tokens and the player
# nonetheless share ONE height rule: h_px = h_m * ppm * cos alpha.
TOKEN_HEIGHT_M = {"S": 1.45, "M": 1.95, "L": 2.55, "HERO": 3.10}

ROOT = os.path.dirname(os.path.abspath(__file__))
COLLAB = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
GEOM_PATH = os.path.join(
    COLLAB, "agentic_orchestration", "galadriel", "notes",
    "crucible-arena-geometry-v1.json")
PACK_DIR = ("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
            "kc2-model-pack-v3-E-s09-cp150-mech-v3p1-20260826_031143")
KEEPER_CELL = os.path.join(
    COLLAB, "astra_test_01", "burst", "runs", "C-7", "cliffside_v45",
    "sprites", "idle", "S", "idle_S_00.png")

# ===========================================================================
# 1 · PALETTE  (free art — no wire basis)
# ===========================================================================
C_GROUND      = (28, 27, 33)
C_GROUND_2    = (36, 34, 42)
C_GRIT        = (46, 44, 53)
C_INK         = (233, 231, 226)
C_DIM         = (150, 147, 158)
C_FAINT       = (96, 94, 104)
C_PANEL       = (16, 15, 20)
C_RULE        = (78, 76, 88)
C_EOR         = (255, 188, 78)
C_BANNER      = (214, 148, 46)
C_POOL        = (96, 196, 110)
C_WALL        = (168, 164, 178)
C_UNWALKED    = (236, 108, 108)
C_HOSTILE     = (198, 92, 96)
C_HOSTILE_2   = (176, 106, 154)
C_HERO        = (236, 132, 82)
C_SUMMON      = (110, 176, 226)
C_MOCK        = (255, 92, 92)
C_VIEWRECT    = (250, 250, 250)

FONT_DIR = "/System/Library/Fonts/Supplemental"


def font(size, bold=False, mono=False):
    if mono:
        for p in ("/System/Library/Fonts/Menlo.ttc",
                  "/System/Library/Fonts/Monaco.ttf"):
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    p = os.path.join(FONT_DIR, name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ===========================================================================
# 2 · SUBSTRATE LOAD — digest-gated (GL-6)
# ===========================================================================

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def load_geometry():
    got = sha256_of(GEOM_PATH)
    if got != GEOM_SHA256:
        sys.exit("GL-6 ABORT: arena geometry digest mismatch\n  want %s\n  got  %s"
                 % (GEOM_SHA256, got))
    print("[gl-6] arena geometry  %s  OK" % got[:12])
    with open(GEOM_PATH) as fh:
        return json.load(fh)


def load_pack_member(relpath):
    """GL-6 two-level: manifest pack_digest re-derived, then the member."""
    man_path = os.path.join(PACK_DIR, "manifest.json")
    with open(man_path) as fh:
        man = json.load(fh)
    lines = sorted("%s  %s" % (m["path"], m["sha256"]) for m in man["members"])
    derived = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    if derived != man["pack_digest"] or derived != PACK_DIGEST:
        sys.exit("GL-6 ABORT: pack digest mismatch\n  derived %s\n  manifest %s"
                 % (derived, man["pack_digest"]))
    row = next((m for m in man["members"] if m["path"] == relpath), None)
    if row is None:
        sys.exit("GL-6 ABORT: %s is not a manifest member" % relpath)
    p = os.path.join(PACK_DIR, relpath)
    got = sha256_of(p)
    if got != row["sha256"]:
        sys.exit("GL-6 ABORT: member digest mismatch for %s" % relpath)
    print("[gl-6] pack %s / member %s  OK" % (derived[:12], relpath))
    with open(p) as fh:
        return json.load(fh)


# ===========================================================================
# 3 · THE PROJECTION — 2D spec § 1.1 / § 1.2.  Nothing below is typed.
# ===========================================================================

class Projection:
    def __init__(self, fraction, preset_name, u):
        self.preset = preset_name
        self.alpha_deg = ALPHA_DEG
        self.alpha = math.radians(ALPHA_DEG)
        self.sin_a = math.sin(self.alpha)
        self.cos_a = math.cos(self.alpha)
        self.tan_a = math.tan(self.alpha)
        self.h_fig_m = H_FIG_M
        self.fraction = fraction
        # § 1.2: a figure fraction is screen height occupied by a body of
        # h_fig metres.
        self.fig_px = fraction * VIEW_H
        # § 1.2 formula: ppm = (fraction * 1080) / (h_fig * cos alpha)
        self.ppm = self.fig_px / (self.h_fig_m * self.cos_a)
        self.u = u

    # metres on the arena plane -> screen px offset from the camera point.
    def m_to_px(self, dx_m, dy_m):
        return (self.ppm * dx_m, self.ppm * self.sin_a * dy_m)

    def r_to_semiaxes(self, r_m):
        """A ground circle of radius r_m projects to an ellipse."""
        return (self.ppm * r_m, self.ppm * r_m * self.sin_a)

    def height_px(self, h_m):
        """A standing body of h_m metres occupies this many screen px."""
        return self.ppm * h_m * self.cos_a


def self_check(pg, ph, eor_r_m):
    """Derivation cross-check.  A silent arithmetic regression cannot pass."""
    sx, sy = pg.r_to_semiaxes(eor_r_m)
    got = {
        "ppm_gd": pg.ppm, "ppm_house": ph.ppm,
        "fig_px_gd": pg.fig_px, "fig_px_house": ph.fig_px,
        "eor_semi_x_gd": sx, "eor_semi_y_gd": sy,
    }
    print("\n[check] derived vs published (2D spec Corrigenda-Forward 1 & 2)")
    bad = 0
    for k, want in EXPECT.items():
        d = abs(got[k] - want)
        ok = d < 0.05
        bad += 0 if ok else 1
        print("  %-16s derived %12.4f   published %10.3f   d=%.4f  %s"
              % (k, got[k], want, d, "OK" if ok else "**MISMATCH**"))
    # § 1.1 free cross-check: the lane's own ruled px/m pair reproduces tan a.
    lane = 80.31 / 60.62
    print("  %-16s derived %12.6f   lane-ruled %8.5f   (80.31/60.62)  %s"
          % ("tan_alpha", pg.tan_a, lane,
             "OK" if abs(pg.tan_a - lane) < 5e-5 else "**MISMATCH**"))
    if bad:
        sys.exit("SELF-CHECK FAILED — %d value(s) off." % bad)
    return got


# ===========================================================================
# 4 · DRAW HELPERS
# ===========================================================================

def dashed_path(dr, pts, fill, width=2, dash=9, gap=7):
    carry, on = 0.0, True
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg <= 1e-9:
            continue
        t = 0.0
        while t < seg:
            step = min((dash if on else gap) - carry, seg - t)
            if on:
                a = (x0 + (x1 - x0) * (t / seg), y0 + (y1 - y0) * (t / seg))
                b = (x0 + (x1 - x0) * ((t + step) / seg),
                     y0 + (y1 - y0) * ((t + step) / seg))
                dr.line([a, b], fill=fill, width=width)
            t += step
            carry += step
            if carry >= (dash if on else gap) - 1e-9:
                carry, on = 0.0, not on


def ellipse_pts(cx, cy, rx, ry, n=200):
    return [(cx + rx * math.cos(2 * math.pi * i / n),
             cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def dashed_ellipse(dr, cx, cy, rx, ry, fill, width=2, dash=9, gap=7):
    dashed_path(dr, ellipse_pts(cx, cy, rx, ry), fill, width, dash, gap)


def soft_ellipse(img, cx, cy, rx, ry, rgba, outline=None, ow=2):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=rgba)
    if outline:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=outline, width=ow)
    img.alpha_composite(lay)


def text(dr, xy, s, f, fill=C_INK, anchor=None):
    dr.text(xy, s, font=f, fill=fill, anchor=anchor)


def panel(img, box, alpha=232, border=C_RULE):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rectangle(box, fill=C_PANEL + (alpha,),
                                  outline=border + (255,), width=1)
    img.alpha_composite(lay)


def hits(box, reserved):
    x0, y0, x1, y1 = box
    for (a, b, c, d) in reserved:
        if not (x1 < a or x0 > c or y1 < b or y0 > d):
            return True
    return False


def place_label(reserved, x, y, w, h, tries=7, step=28):
    """Find a free y for a label centred on x.  None if the frame is full."""
    for k in range(tries):
        yy = y + k * step
        box = (x - w / 2, yy, x + w / 2, yy + h)
        if box[1] < 4 or box[3] > VIEW_H - 4:
            continue
        if not hits(box, reserved):
            return yy
    return None


# ===========================================================================
# 5 · SILHOUETTES + GLOBES (free art — flat, deliberately crude)
# ===========================================================================

def draw_token(img, dr, tk, proj, reserved):
    """sx,sy = the token's GROUND point.  Footprint drawn at the token radius."""
    sx, sy, r_m, colour = tk["sx"], tk["sy"], tk["r_m"], tk["colour"]
    rx, ry = proj.r_to_semiaxes(r_m)
    h_px = proj.height_px(tk["h_m"])
    w_px = rx * 0.92

    # contact shadow, then the footprint at the token's declared radius
    soft_ellipse(img, sx, sy, rx * 0.80, ry * 0.80, (0, 0, 0, 52))
    dashed_ellipse(dr, sx, sy, rx, ry, colour, width=1, dash=6, gap=5)

    top = sy - h_px
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    head_r = w_px * 0.34
    hy = top + head_r
    d.polygon([(sx - w_px * 0.50, sy - ry * 0.20),
               (sx - w_px * 0.30, hy + head_r * 0.35),
               (sx + w_px * 0.30, hy + head_r * 0.35),
               (sx + w_px * 0.50, sy - ry * 0.20)],
              fill=colour + (238,), outline=(8, 8, 10, 220))
    d.ellipse([sx - head_r, hy - head_r, sx + head_r, hy + head_r],
              fill=colour + (238,), outline=(8, 8, 10, 220), width=2)
    img.alpha_composite(lay)

    if tk.get("hp") is not None:
        bw = max(24.0, w_px * 1.5)
        by = top - 9
        dr.rectangle([sx - bw / 2, by, sx + bw / 2, by + 4],
                     fill=(18, 18, 22), outline=C_FAINT)
        dr.rectangle([sx - bw / 2 + 1, by + 1,
                      sx - bw / 2 + 1 + (bw - 2) * tk["hp"], by + 3],
                     fill=(210, 74, 74))
    if tk.get("label"):
        f = font(13, bold=True)
        w = dr.textlength(tk["label"], font=f)
        yy = place_label(reserved, sx, top - 32, w + 14, 17, tries=1)
        if yy is not None:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).rectangle(
                [sx - w / 2 - 7, yy - 2, sx + w / 2 + 7, yy + 17],
                fill=(12, 11, 15, 210), outline=C_HERO + (255,))
            img.alpha_composite(lay)
            text(dr, (sx, yy + 7), tk["label"], f, C_HERO, anchor="mm")
    if tk.get("kind") == "summon":
        text(dr, (sx, sy + ry + 6), "summon · NO health bar", font(11),
             C_SUMMON, anchor="mt")


def globe(img, dr, cx, cy, r, frac, rgb, caption, value, sub):
    tile = Image.new("RGBA", (int(2 * r) + 2, int(2 * r) + 2), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    top = 2 * r - 2 * r * frac
    td.rectangle([0, top, 2 * r + 2, 2 * r + 2], fill=rgb + (115,))
    mask = Image.new("L", tile.size, 0)
    ImageDraw.Draw(mask).ellipse([1, 1, 2 * r, 2 * r], fill=255)
    tile.putalpha(Image.eval(Image.composite(tile.split()[3],
                                             Image.new("L", tile.size, 0),
                                             mask), lambda v: v))
    img.alpha_composite(tile, (int(cx - r), int(cy - r)))
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_RULE, width=2)
    dr.line([cx - r * 0.93, cy - r + top, cx + r * 0.93, cy - r + top],
            fill=rgb, width=2)
    text(dr, (cx, cy - 10), value, font(14, bold=True), C_INK, anchor="mm")
    text(dr, (cx, cy + 9), sub, font(9), C_DIM, anchor="mm")
    text(dr, (cx, cy + r + 7), caption, font(11, bold=True), C_DIM, anchor="mt")


# ===========================================================================
# 6 · THE FRAME
# ===========================================================================

# Layout reserved rects — labels never land on a panel.
LEGEND_BOX = (24, 24, 664, 278)
DECLARE_BOX = (24, 290, 664, 428)
OVERVIEW_BOX = (1368, 24, 1896, 624)
BADGE_BOX = (836, 14, 1190, 136)
SKILL_BOX = (656, 902, 1264, 1046)
HPG_BOX = (30, 914, 166, 1060)
ENG_BOX = (1754, 914, 1890, 1060)
MOCK_BOX = (700, 176, 1330, 274)
RESERVED = [LEGEND_BOX, DECLARE_BOX, OVERVIEW_BOX, BADGE_BOX, SKILL_BOX,
            HPG_BOX, ENG_BOX, MOCK_BOX]


def split_ring(ring_px, unwalked_arcs, n):
    """(walked runs, unwalked runs).  Vertex set IDENTICAL — never smoothed."""
    flagged = set()
    for arc in unwalked_arcs:
        for i in range(arc["vertex_index_from"], arc["vertex_index_to"] + 1):
            flagged.add(i % n)
    walked, unw, cur, cur_flag = [], [], [], None
    for i in range(n + 1):
        idx = i % n
        f = idx in flagged
        if cur_flag is None:
            cur_flag = f
        if f != cur_flag:
            cur.append(ring_px[idx])
            (unw if cur_flag else walked).append(cur)
            cur, cur_flag = [ring_px[idx]], f
        else:
            cur.append(ring_px[idx])
    if cur:
        (unw if cur_flag else walked).append(cur)
    return ([r for r in walked if len(r) > 1],
            [r for r in unw if len(r) > 1])


def compose(preset_name, fraction, geom, eor_r_m, u, roster, out_path):
    proj = Projection(fraction, preset_name, u)
    img = Image.new("RGBA", (VIEW_W, VIEW_H), C_GROUND + (255,))
    dr = ImageDraw.Draw(img)

    hb = geom["hard_boundary"]
    ring_native = hb["outer_ring"]["vertices_native"]
    cam_n = geom["frame"]["arena_centroid_native"]
    pcx, pcy = VIEW_W / 2.0, VIEW_H / 2.0

    def nat(px, py):
        ox, oy = proj.m_to_px((px - cam_n[0]) * proj.u, (py - cam_n[1]) * proj.u)
        return (pcx + ox, pcy + oy)

    # ---------------- ground (free art) ----------------
    rnd = random.Random(20260920)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(30):
        x, y, r = rnd.uniform(0, VIEW_W), rnd.uniform(0, VIEW_H), rnd.uniform(60, 190)
        d.ellipse([x - r, y - r * 0.55, x + r, y + r * 0.55], fill=C_GROUND_2 + (30,))
    for _ in range(1600):
        x, y = rnd.uniform(0, VIEW_W), rnd.uniform(0, VIEW_H)
        r = rnd.uniform(0.7, 3.0)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6],
                  fill=C_GRIT + (rnd.randint(24, 66),))
    img.alpha_composite(lay)

    in_frame = []

    # ---------------- green zones — radii are UPPER BOUNDS ----------------
    for z in geom["green_zones"]["zones"]:
        cx, cy = nat(*z["interior_point_minimap_px"])
        r_m = z["radius_upper_bound_px"] * proj.u
        rx, ry = proj.r_to_semiaxes(r_m)
        if cx + rx < 0 or cx - rx > VIEW_W or cy + ry < 0 or cy - ry > VIEW_H:
            continue
        # truthful in-frame test: does any BOUNDARY point actually land in the
        # viewport, or does the zone cover the frame?  A bbox overlap is not
        # presence, and a legend that claims presence on a bbox is lying.
        bnd = ellipse_pts(cx, cy, rx, ry, 120)
        visible = any(0 <= p[0] <= VIEW_W and 0 <= p[1] <= VIEW_H for p in bnd)
        covers = ((pcx - cx) / rx) ** 2 + ((pcy - cy) / ry) ** 2 <= 1.0
        if visible or covers:
            in_frame.append(z["id"] + ("" if visible else " (covers frame)"))
        soft_ellipse(img, cx, cy, rx, ry, C_POOL + (30,))
        dashed_ellipse(dr, cx, cy, rx, ry, C_POOL, width=2, dash=13, gap=10)
        lx = min(max(cx, 190), VIEW_W - 190)
        yy = place_label(RESERVED, lx, max(cy - ry + 12, 12), 400, 36)
        if yy is not None:
            l1 = "%s · r <= %.1f native px (UPPER BOUND) = %.1f m" % (
                z["id"], z["radius_upper_bound_px"], r_m)
            l2 = "ENTERABLE DAMAGE FIELD — never collide-blocking"
            w = max(dr.textlength(l1, font=font(13, bold=True)),
                    dr.textlength(l2, font=font(11))) / 2 + 9
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).rectangle([lx - w, yy - 5, lx + w, yy + 34],
                                          fill=(12, 16, 13, 196))
            img.alpha_composite(lay)
            text(dr, (lx, yy), l1, font(13, bold=True), C_POOL, anchor="mt")
            text(dr, (lx, yy + 16), l2, font(11), C_POOL, anchor="mt")

    # ---------------- ring + islands, if they reach this frame ----------------
    def reaches(pts):
        """Truthful: a POINT must land in the viewport.  A bbox that merely
        straddles the frame is not presence (the ring's bbox always does)."""
        return any(0 <= p[0] <= VIEW_W and 0 <= p[1] <= VIEW_H for p in pts)

    ring_px = [nat(*v) for v in ring_native]
    if reaches(ring_px):
        walked, unw = split_ring(ring_px, hb["unwalked_arcs"], len(ring_native))
        for run in walked:
            dr.line(run, fill=C_WALL, width=4)
        for run in unw:
            dashed_path(dr, run, C_UNWALKED, width=4, dash=14, gap=10)
        in_frame.append("outer ring")
    for ob in hb["interior_obstructions"]:
        pts = [nat(*v) for v in ob["vertices_native"]]
        if reaches(pts):
            dr.polygon(pts, fill=(52, 50, 60), outline=C_WALL)
            in_frame.append(ob["id"])

    # ---------------- Vanguard Banner aura (ground) ----------------
    bx, by = proj.r_to_semiaxes(BANNER_AURA_M)
    soft_ellipse(img, pcx, pcy, bx, by, C_BANNER + (17,))
    dashed_ellipse(dr, pcx, pcy, bx, by, C_BANNER, width=2, dash=17, gap=13)

    # ---------------- EoR ring (ground) ----------------
    ex, ey = proj.r_to_semiaxes(eor_r_m)
    soft_ellipse(img, pcx, pcy, ex, ey, C_EOR + (24,))
    for k, a, w in ((1.0, 240, 3), (0.955, 110, 2)):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse(
            [pcx - ex * k, pcy - ey * k, pcx + ex * k, pcy + ey * k],
            outline=C_EOR + (a,), width=w)
        img.alpha_composite(lay)

    # ---------------- bodies, y-sorted ----------------
    tokens = build_tokens(proj, roster)
    keeper = load_keeper(proj)
    drawables = [(t["sy"], t) for t in tokens] + [(pcy, None)]
    drawables.sort(key=lambda t: t[0])
    for _, tk in drawables:
        if tk is None:
            soft_ellipse(img, pcx, pcy, proj.ppm * 0.42,
                         proj.ppm * 0.42 * proj.sin_a, (0, 0, 0, 120))
            img.alpha_composite(keeper, (int(pcx - keeper.width / 2),
                                         int(pcy - keeper.height)))
        else:
            draw_token(img, dr, tk, proj, RESERVED)

    # ---------------- labels for the two model-bound rings ----------------
    text(dr, (pcx - ex - 14, pcy - 10),
         "EYE OF RECKONING · r = %.1f m (pack value)" % eor_r_m,
         font(14, bold=True), C_EOR, anchor="rm")
    text(dr, (pcx - ex - 14, pcy + 10),
         "semi-axes %.1f x %.1f px  ·  %.0f px across  ·  %.2f x figure height"
         % (ex, ey, ex * 2, ex / proj.fig_px), font(11), C_EOR, anchor="rm")

    byy = min(pcy + ey + 44, SKILL_BOX[1] - 52)
    text(dr, (pcx, byy),
         "VANGUARD BANNER AURA · r = %.1f m · x2.0 player damage, per-tick, no hysteresis"
         % BANNER_AURA_M, font(13, bold=True), C_BANNER, anchor="mt")
    text(dr, (pcx, byy + 17),
         "radius MODEL-BOUND · PLACEMENT DECLARED-NOT-DECODED (charter R-KP-0f)",
         font(11), C_BANNER, anchor="mt")

    # ---------------- overlays ----------------
    draw_overview(img, geom, proj)
    draw_hud(img, dr, proj)
    draw_legend(img, dr, proj, eor_r_m, in_frame)
    draw_mock(img, dr)

    img.convert("RGB").save(out_path, "PNG")
    print("  wrote %s  (%s)" % (os.path.basename(out_path), preset_name))
    return proj


def build_tokens(proj, roster):
    """~40 tokens.  Radii are PLACEHOLDERS — v3.1 carries no body radius."""
    rnd = random.Random(15160)
    out = []
    for _ in range(40):
        ang = rnd.uniform(0, 2 * math.pi)
        rad_m = rnd.uniform(4.2, 19.0)
        ox, oy = proj.m_to_px(math.cos(ang) * rad_m, math.sin(ang) * rad_m * 0.82)
        sx, sy = VIEW_W / 2.0 + ox, VIEW_H / 2.0 + oy
        if not (-90 < sx < VIEW_W + 90 and -40 < sy < VIEW_H + 40):
            continue
        cls = rnd.choices(["S", "M", "L"], weights=[34, 49, 17])[0]
        out.append({"sx": sx, "sy": sy, "r_m": TOKEN_RADIUS_M[cls],
                    "h_m": TOKEN_HEIGHT_M[cls],
                    "colour": C_HOSTILE if rnd.random() < 0.72 else C_HOSTILE_2,
                    "hp": rnd.uniform(0.18, 1.0)})
    # hero / nemesis tokens — names are REAL pack roster strings
    for j, (ang, rad_m) in enumerate(((-2.05, 9.4), (0.62, 11.8), (2.35, 8.6))):
        ox, oy = proj.m_to_px(math.cos(ang) * rad_m, math.sin(ang) * rad_m * 0.82)
        out.append({"sx": VIEW_W / 2.0 + ox, "sy": VIEW_H / 2.0 + oy,
                    "r_m": TOKEN_RADIUS_M["HERO"], "h_m": TOKEN_HEIGHT_M["HERO"],
                    "colour": C_HERO, "hp": 0.52 + 0.16 * j,
                    "label": roster[7 + j * 27]})
    # summons — pinned beside the player, NO health bar (R-KP-0b, WARN-13)
    ex, ey = proj.r_to_semiaxes(3.0)
    for sgn in (-1, 1):
        out.append({"sx": VIEW_W / 2.0 + sgn * ex * 0.66,
                    "sy": VIEW_H / 2.0 + ey * 0.52,
                    "r_m": TOKEN_RADIUS_M["M"] * 0.88,
                    "h_m": TOKEN_HEIGHT_M["M"] * 0.88, "colour": C_SUMMON,
                    "hp": None, "kind": "summon"})
    return out


def load_keeper(proj):
    """First-party cell on disk.  Scaled so the body's ALPHA BBOX height equals
    the DERIVED figure height.  Nothing typed."""
    im = Image.open(KEEPER_CELL).convert("RGBA")
    im = im.crop(im.getbbox())
    s = proj.fig_px / im.height
    return im.resize((max(1, int(round(im.width * s))),
                      max(1, int(round(im.height * s)))), Image.LANCZOS)


def draw_overview(img, geom, proj):
    """Whole arena, SAME § 1.1 law, at a DECLARED display scale.  Clipped."""
    hb = geom["hard_boundary"]
    ring = hb["outer_ring"]["vertices_native"]
    n = len(ring)
    cam_n = geom["frame"]["arena_centroid_native"]

    def full(px, py):
        return proj.m_to_px((px - cam_n[0]) * proj.u, (py - cam_n[1]) * proj.u)

    pts = [full(*v) for v in ring]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    aw, ah = max(xs) - min(xs), max(ys) - min(ys)

    x0, y0, x1, y1 = OVERVIEW_BOX
    PW, PH = int(x1 - x0), int(y1 - y0)
    tile = Image.new("RGBA", (PW, PH), C_PANEL + (236,))
    td = ImageDraw.Draw(tile)
    td.rectangle([0, 0, PW - 1, PH - 1], outline=C_RULE, width=1)

    inner_w, inner_h = PW - 60, PH - 176
    k = min(inner_w / aw, inner_h / ah)          # DECLARED display scale
    ocx, ocy = PW / 2.0, 96 + inner_h / 2.0

    def ov(px, py):
        x, y = full(px, py)
        return (ocx + x * k, ocy + y * k)

    text(td, (16, 12), "ARENA OVERVIEW", font(17, bold=True), C_INK)
    text(td, (16, 36), "same § 1.1 projection law, displayed at %.4f x %s"
         % (k, proj.preset), font(11), C_DIM)
    text(td, (16, 52), "177 outer vertices · 4 islands · 6 zones · "
         "interpolated_segments = []", font(11), C_DIM)
    text(td, (16, 68), "vertex set IDENTICAL to the file — no resample, no "
         "spline, no hull", font(11), C_FAINT)

    for z in geom["green_zones"]["zones"]:
        cx, cy = ov(*z["interior_point_minimap_px"])
        rx, ry = proj.r_to_semiaxes(z["radius_upper_bound_px"] * proj.u)
        lay = Image.new("RGBA", tile.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([cx - rx * k, cy - ry * k,
                                     cx + rx * k, cy + ry * k],
                                    fill=C_POOL + (46,))
        tile.alpha_composite(lay)
        dashed_ellipse(td, cx, cy, rx * k, ry * k, C_POOL, 1, 5, 4)
    for ob in hb["interior_obstructions"]:
        td.polygon([ov(*v) for v in ob["vertices_native"]],
                   fill=(60, 58, 68), outline=C_WALL)

    opx = [ov(*v) for v in ring]
    walked, unw = split_ring(opx, hb["unwalked_arcs"], n)
    for run in walked:
        td.line(run, fill=C_WALL, width=2)
    for run in unw:
        dashed_path(td, run, C_UNWALKED, width=3, dash=6, gap=4)
        for p in run:
            td.ellipse([p[0] - 2.5, p[1] - 2.5, p[0] + 2.5, p[1] + 2.5],
                       fill=C_UNWALKED)

    # north-gate landmark (2D spec § 3.1) — ASSERTED above the centroid
    gx, gy = ov(0.0, 0.0)
    ccx, ccy = ov(*cam_n)
    assert gy < ccy, "north-gate landmark did not render above the centroid"
    td.line([gx - 9, gy, gx + 9, gy], fill=C_INK, width=2)
    td.line([gx, gy - 9, gx, gy + 9], fill=C_INK, width=2)
    text(td, (gx + 12, gy - 7), "north gate (frame origin)", font(11), C_INK)

    vw, vh = VIEW_W * k, VIEW_H * k
    td.rectangle([ccx - vw / 2, ccy - vh / 2, ccx + vw / 2, ccy + vh / 2],
                 outline=C_VIEWRECT, width=2)
    text(td, (ccx, ccy - vh / 2 - 4), "this frame", font(11, bold=True),
         C_VIEWRECT, anchor="mb")

    fy = PH - 62
    text(td, (16, fy), "the ring is %.2f x this viewport wide and %.2f x tall"
         % (aw / VIEW_W, ah / VIEW_H), font(12, bold=True), C_INK)
    text(td, (16, fy + 19), "dashed red = the two north arcs MAPPED BUT NEVER "
         "WALKED", font(11), C_UNWALKED)
    text(td, (16, fy + 35), "green = enterable damage fields; radii are UPPER "
         "BOUNDS", font(11), C_POOL)
    img.alpha_composite(tile, (int(x0), int(y0)))


def draw_hud(img, dr, proj):
    """Wireframe only.  Values are the 2D spec § 2.1 snapshot example."""
    hp, hp_max, en, en_max = 17400, 20005, 2388, 2576

    panel(img, list(BADGE_BOX))
    text(dr, (VIEW_W / 2, BADGE_BOX[1] + 8), "WAVE", font(12), C_DIM, anchor="mt")
    text(dr, (VIEW_W / 2, BADGE_BOX[1] + 21), "151", font(30, bold=True),
         C_INK, anchor="mt")
    bx, by = BADGE_BOX[0] + 14, BADGE_BOX[1] + 74
    dr.rectangle([bx, by, bx + 40, by + 40], outline=C_BANNER, width=2)
    text(dr, (bx + 20, by + 20), "VB", font(15, bold=True), C_BANNER, anchor="mm")
    text(dr, (bx + 50, by + 5), "Vanguard Banner", font(12, bold=True), C_BANNER)
    text(dr, (bx + 50, by + 22), "x2.0 damage — drops the instant you leave",
         font(10), C_DIM)

    globe(img, dr, 96, 980, 58, hp / hp_max, (186, 62, 62), "HEALTH",
          "{:,} / {:,}".format(hp, hp_max), "absolute hp + hp_max")
    globe(img, dr, VIEW_W - 96, 980, 58, en / en_max, (62, 108, 186), "ENERGY",
          "{:,} / {:,}".format(en, en_max), "EoR drain 176.4 /s")

    slots = [("RMB", "Eye of Reckoning", "CHANNEL — held", None, C_EOR),
             ("LMB", "Blitz", "interrupts channel: TRUE", 0.42, C_RULE),
             ("2", "Vire's Might", "interrupts channel: TRUE", 0.0, C_RULE),
             ("3", "War Cry", "interrupts channel: FALSE", 0.78, C_RULE),
             ("7", "Rune of Rush", "interrupts: UNDETERMINED", 0.0, C_RULE)]
    sw, sh, gap = 104, 104, 14
    total = len(slots) * sw + (len(slots) - 1) * gap
    sx0, sy0 = VIEW_W / 2 - total / 2, 930
    text(dr, (VIEW_W / 2, sy0 - 26),
         "three of these four keys do less than they did in the video (charter "
         "R-KP-0e) —", font(11), C_DIM, anchor="mm")
    text(dr, (VIEW_W / 2, sy0 - 12),
         "riders the pack does not carry ship PLACEHOLDER-INERT, named on the "
         "tooltip", font(11), C_DIM, anchor="mm")
    for i, (bind, name, note, cd, col) in enumerate(slots):
        x = sx0 + i * (sw + gap)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).rectangle([x, sy0, x + sw, sy0 + sh],
                                      fill=(14, 13, 18, 226),
                                      outline=col + (255,), width=2)
        img.alpha_composite(lay)
        if cd:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).rectangle(
                [x + 3, sy0 + 3 + (sh - 6) * (1 - cd), x + sw - 3, sy0 + sh - 3],
                fill=(6, 6, 9, 180))
            img.alpha_composite(lay)
        text(dr, (x + 8, sy0 + 6), bind, font(15, bold=True), C_INK)
        text(dr, (x + sw / 2, sy0 + sh - 30), name, font(12, bold=True),
             C_INK, anchor="mm")
        text(dr, (x + sw / 2, sy0 + sh - 14), note, font(9), C_DIM, anchor="mm")


def draw_legend(img, dr, proj, eor_r_m, in_frame):
    x0, y0, x1, y1 = LEGEND_BOX
    panel(img, [x0, y0, x1, y1])
    fm, fb = font(12, mono=True), font(16, bold=True)
    text(dr, (x0 + 16, y0 + 11), "PROJECTION OF RECORD", fb, C_INK)
    sx, sy = proj.r_to_semiaxes(eor_r_m)
    rows = [
        ("zoom preset", proj.preset),
        ("figure", "fraction %.4f  ->  %.3f px @ 1080p" % (proj.fraction, proj.fig_px)),
        ("h_fig", "%.1f m  (the arena scale chain's own character height)" % proj.h_fig_m),
        ("alpha", "%.10f deg   sin %.6f  cos %.6f" % (proj.alpha_deg, proj.sin_a, proj.cos_a)),
        ("ppm", "%.3f px/m  = (fraction*1080)/(h_fig*cos alpha)" % proj.ppm),
        ("u  REGISTERED", "%.6f m per native minimap px   (conductor ledger KP-6)" % proj.u),
        ("u  window", "[%.5f, %.4f]   in-window; 0.1981 EXCLUDED (R-L3-2)" % U_WINDOW),
        ("EoR ring", "r %.1f m (pack)  ->  %.1f x %.1f px semi-axes" % (eor_r_m, sx, sy)),
        ("geometry", "crucible-arena-geometry-v1.json   sha %s" % GEOM_SHA256[:12]),
        ("pack", "kc2-model-pack v3.1   sha %s" % PACK_DIGEST[:12]),
        ("in this frame", ", ".join(in_frame) if in_frame else "(no ring/island/zone reaches it)"),
    ]
    yy = y0 + 40
    for k, v in rows:
        text(dr, (x0 + 16, yy), k, fm, C_DIM)
        text(dr, (x0 + 140, yy), v, fm, C_INK)
        yy += 18

    # DECLARED panel
    a0, b0, a1, b1 = DECLARE_BOX
    panel(img, [a0, b0, a1, b1])
    text(dr, (a0 + 15, b0 + 10), "DECLARED, NOT DECODED  (GL-12)",
         font(14, bold=True), C_MOCK)
    f11 = font(11)
    lines = [
        "monster body radii — v3.1 model/monsters.json carries NO radius / size /",
        "   body key (31 distinct keys, zero matching).  Token radii here are",
        "   PLACEHOLDERS; the M-class 0.62 m is the 2D spec § 2.1 example value.",
        "   Footprints are drawn at the DECLARED radius, not at a model one.",
        "Vanguard Banner PLACEMENT (its 8.0 m radius IS model-bound) · dressed",
        "   margin · silhouette shapes, tints, HUD layout, ground dressing.",
        "HP / energy figures are the 2D spec § 2.1 snapshot example.",
    ]
    yy = b0 + 32
    for ln in lines:
        text(dr, (a0 + 15, yy), ln, f11, C_DIM)
        yy += 14


def draw_mock(img, dr):
    # low-alpha diagonal watermark — unmistakable at any crop
    wm = Image.new("RGBA", (2600, 2600), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    f = font(120, bold=True)
    for row in range(9):
        for col in range(5):
            wd.text((col * 560 + (row % 2) * 280, row * 300), "MOCK",
                    font=f, fill=C_MOCK + (13,))
    wm = wm.rotate(-24, resample=Image.BICUBIC)
    img.alpha_composite(wm, (-340, -760))

    x0, y0, x1, y1 = MOCK_BOX
    panel(img, [x0, y0, x1, y1], alpha=210, border=C_MOCK)
    cx = (x0 + x1) / 2
    text(dr, (cx, y0 + 10), "MOCK", font(42, bold=True), C_MOCK, anchor="mt")
    text(dr, (cx, y0 + 58),
         "PLACEHOLDER ART — GEOMETRY TRUE.", font(14, bold=True), C_MOCK,
         anchor="mt")
    text(dr, (cx, y0 + 76),
         "Composed without any Astra/codex burst, without Godot, without new art.",
         font(12), C_DIM, anchor="mt")


# ===========================================================================
# 7 · MAIN
# ===========================================================================

def main():
    print("KC2-PLAY · G-IMG first-frame MOCK")
    print("=" * 74)
    geom = load_geometry()
    player_kit = load_pack_member("model/player_kit.json")
    monsters = load_pack_member("model/monsters.json")
    roster = monsters["recorded_roster_archetypes"]

    eor_r_m = player_kit["channel"]["radius_m"]["value"]          # GL-10
    print("[gl-10] EoR radius_m = %s (%s, precedence %s)"
          % (eor_r_m, player_kit["channel"]["radius_m"]["provenance"],
             player_kit["channel"]["radius_m"]["precedence"]))

    u = U_REGISTERED                                    # R-KP-0c + ledger KP-6
    if not (U_WINDOW[0] <= u <= U_WINDOW[1]):
        sys.exit("REGISTERED u=%.6f is OUTSIDE the window [%.5f, %.4f] (R-L3-2)"
                 % (u, U_WINDOW[0], U_WINDOW[1]))
    print("[kp-6]    u = %.6f m/native-px  REGISTERED (conductor, ledger KP-6)"
          % u)
    print("[r-kp-0c] window [%.5f, %.4f] — in-window OK; supersedes the "
          "midpoint %.6f used at first cut" % (U_WINDOW + (U_SUPERSEDED_MIDPOINT,)))

    pg = Projection(FRACTION_ZOOM_GD, "ZOOM-GD", u)
    ph = Projection(FRACTION_ZOOM_HOUSE, "ZOOM-HOUSE", u)
    self_check(pg, ph, eor_r_m)

    print("\n[compose]")
    out_gd = os.path.join(ROOT, "01_G-IMG_mock_ZOOM-GD_1920x1080.png")
    out_ho = os.path.join(ROOT, "02_G-IMG_mock_ZOOM-HOUSE_1920x1080.png")
    compose("ZOOM-GD", FRACTION_ZOOM_GD, geom, eor_r_m, u, roster, out_gd)
    compose("ZOOM-HOUSE", FRACTION_ZOOM_HOUSE, geom, eor_r_m, u, roster, out_ho)

    rec = {
        "generated": "2026-09-20",
        "author": "drax (presentation seam), run KC2-PLAY Wave 1",
        "gate": "G-IMG (charter § 6.1, ledger KP-3)",
        "burst_fired": False, "godot_launched": False, "new_art_minted": False,
        "constants_of_record": {
            "alpha_deg": ALPHA_DEG, "h_fig_m": H_FIG_M,
            "fraction_zoom_gd": FRACTION_ZOOM_GD,
            "fraction_zoom_house": FRACTION_ZOOM_HOUSE,
            "u_window": list(U_WINDOW), "banner_aura_m": BANNER_AURA_M},
        "derived": {
            "u_registered": u, "u_basis": "conductor ledger KP-6 (2026-09-20)",
            "u_superseded_midpoint": U_SUPERSEDED_MIDPOINT, "ppm_zoom_gd": pg.ppm, "ppm_zoom_house": ph.ppm,
            "figure_px_zoom_gd": pg.fig_px, "figure_px_zoom_house": ph.fig_px,
            "eor_radius_m_from_pack": eor_r_m,
            "eor_semi_axes_px_zoom_gd": list(pg.r_to_semiaxes(eor_r_m)),
            "eor_semi_axes_px_zoom_house": list(ph.r_to_semiaxes(eor_r_m))},
        "substrate": {
            "arena_geometry_sha256": GEOM_SHA256, "pack_digest": PACK_DIGEST,
            "keeper_cell": os.path.relpath(KEEPER_CELL, COLLAB)},
        "declared_not_decoded": [
            "monster body radii (v3.1 monsters.json carries no radius key)",
            "Vanguard Banner placement (its 8.0 m radius is model-bound)",
            "silhouette shapes, tints, HUD layout, ground dressing"],
        "outputs": [os.path.basename(out_gd), os.path.basename(out_ho)],
    }
    with open(os.path.join(ROOT, "receipt.json"), "w") as fh:
        json.dump(rec, fh, indent=2)
    print("  wrote receipt.json")
    print("\nDONE.")


if __name__ == "__main__":
    main()
