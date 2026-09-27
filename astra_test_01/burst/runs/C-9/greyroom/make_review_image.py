#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C-9 · P2' — THE M2 REVIEW IMAGE.
The cathedral grey room BESIDE the arena trace it is built on, with the
mapping labelled on both halves. Matt's gate-M2 packet image.

Reads only this directory's own outputs + the sha-verified geometry file.
Paints nothing.

Usage: python3 make_review_image.py
"""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
# C9_DIR points at a debug build (greyroom/_debug) so the composer can be
# exercised without a full-scale run.  Default is the deliverable directory.
ROOT = os.environ.get("C9_DIR") or HERE
COLLAB = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
G_IMG_DIR = os.path.join(COLLAB, "agentic_orchestration", "drax", "captures",
                         "2026-09-20-kc2-play-g-img")
sys.path.insert(0, G_IMG_DIR)
import make_g_img_mock as mock                                    # noqa: E402

W, H = 3400, 2560
PANEL_W = 1560
MARGIN = 80
HEADER = 210
GAP = 120

BG = (20, 20, 24)
INK = (238, 236, 231)
DIM = (150, 148, 156)
RULE = (74, 72, 84)
C_ANNO = (0, 235, 235)
C_CALL = (255, 196, 66)
C_ROT = (150, 235, 110)

MAPROWS = [
    ("1", "North corridor + red door (spawn)",
     "Entry through the choir screen into the crossing", "screen_passage"),
    ("2", "Central oval",
     "The crossing under the lantern: the brightest, calmest floor",
     "crossing"),
    ("3", "NW / NE lobes", "The transept arms", "transept_w"),
    ("4", "Two long thin E/W interior walls (OB-1, OB-2)", "Choir stalls",
     "choir_stall"),
    ("5", "SW / S / SE lobes; the two small S islands (OB-3, OB-4)",
     "Ambulatory chapels; the altar and a tomb", "ambulatory_floor"),
    ("6", "Six green DoT zones",
     "Rot-soaked chapel floor. ENTERABLE: never collision, never a pit",
     "rot_zone"),
]


def main():
    man = json.load(open(os.path.join(ROOT, "greyroom_manifest.json")))
    geom = mock.load_geometry()
    u = man["scale_figures"]["u_m_per_native_px"]
    hb = geom["hard_boundary"]
    cw, ch = man["canvas"]["size_px"]
    x0 = man["canvas"]["x_min_m"]
    y0 = man["canvas"]["y_min_m"]
    ppm = man["camera"]["px_per_m_east"]
    sina = man["camera"]["px_per_m_south_ground"] / ppm

    s = PANEL_W / cw
    ph = int(round(ch * s))
    cls = {c["name"]: c for c in man["id_mask"]["classes"]}

    def wpx(mx, my):
        """world metres -> panel-local px"""
        return ((mx - x0) * ppm * s, (my - y0) * ppm * sina * s)

    def npx(v):
        return wpx(v[0] * u, v[1] * u)

    # ---- right panel: the grey room ---------------------------------------
    guide = Image.open(os.path.join(ROOT, "guide.png")).convert("RGB")
    guide = guide.resize((PANEL_W, ph), Image.LANCZOS)

    # ---- left panel: the arena trace, drawn from the geometry file ---------
    trace = Image.new("RGB", (PANEL_W, ph), (26, 26, 31))
    td = ImageDraw.Draw(trace)
    ring = [npx(v) for v in hb["outer_ring"]["vertices_native"]]
    td.polygon(ring, fill=(58, 58, 66))
    for ob in hb["interior_obstructions"]:
        td.polygon([npx(v) for v in ob["vertices_native"]], fill=(118, 96, 60),
                   outline=(190, 150, 80))
    k = man["dot_zones"]["k_disjoint"]
    ov = Image.new("RGBA", trace.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for z in geom["green_zones"]["zones"]:
        cx, cy = npx(z["interior_point_minimap_px"])
        rx = z["radius_upper_bound_px"] * u * ppm * s
        ry = rx * sina
        td.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                   outline=C_ROT, width=3)
        od.ellipse([cx - rx * k, cy - ry * k, cx + rx * k, cy + ry * k],
                   fill=C_ROT + (70,))
    trace = Image.alpha_composite(trace.convert("RGBA"), ov).convert("RGB")
    td = ImageDraw.Draw(trace)
    walked, unw = mock.split_ring(ring, hb["unwalked_arcs"], len(ring))
    for run in walked:
        td.line(run, fill=C_ANNO, width=3)
    for run in unw:
        mock.dashed_path(td, run, (255, 110, 110), 4, dash=16, gap=12)
    gx, gy = wpx(0.0, 0.0)
    td.line([(gx - 16, gy), (gx + 16, gy)], fill=C_ANNO, width=3)
    td.line([(gx, gy - 16), (gx, gy + 16)], fill=C_ANNO, width=3)

    # ---- callout anchors, from the manifest's own class centroids ----------
    anchors = {}

    def centroid(name):
        cx, cy = cls[name]["centroid_px"]
        return (cx * s, cy * s)

    anchors["1"] = [centroid("screen_passage")]
    anchors["2"] = [centroid("crossing")]
    anchors["3"] = [centroid("transept_w"), centroid("transept_e")]
    anchors["4"] = []
    for ob in hb["interior_obstructions"]:
        vs = [npx(v) for v in ob["vertices_native"]]
        c = (sum(p[0] for p in vs) / len(vs), sum(p[1] for p in vs) / len(vs))
        if ob["id"] in ("OB-1", "OB-2"):
            anchors["4"].append(c)
        else:
            anchors.setdefault("5", []).append(c)
    anchors["5"].append(centroid("ambulatory_floor"))
    anchors["6"] = [npx(z["interior_point_minimap_px"])
                    for z in geom["green_zones"]["zones"]]


    def callouts(img, faint=False):
        d = ImageDraw.Draw(img, "RGBA")
        f = mock.font(34, bold=True)
        for k, pts in anchors.items():
            for (cx, cy) in pts:
                r = 22
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          fill=(12, 12, 14, 225), outline=C_CALL, width=3)
                d.text((cx, cy - 2), k, font=f, fill=C_CALL, anchor="mm")

    callouts(trace)
    callouts(guide)

    # ---- compose -----------------------------------------------------------
    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)
    f_h1 = mock.font(46, bold=True)
    f_h2 = mock.font(27)
    f_lbl = mock.font(30, bold=True)
    f_num = mock.font(23, mono=True)
    f_row = mock.font(26)
    f_rowb = mock.font(26, bold=True)
    f_small = mock.font(22)

    dr.text((MARGIN, 40), "C-9 · P2' — CATHEDRAL GREY ROOM ON THE CRUCIBLE "
            "ARENA  ·  Matt gate M2", font=f_h1, fill=INK)
    a = man["camera"]
    line2 = ("canvas %d x %d px   ·   %.4f m/px east, %.4f m/px south-ground   "
             "·   world %.2f x %.2f m   ·   arena %.2f x %.2f m at u = %.3f "
             "m/native-px" % (
                 cw, ch, a["m_per_px_east"], a["m_per_px_south_ground"],
                 man["canvas"]["width_m"], man["canvas"]["height_m"],
                 man["arena"]["extent_m"][0], man["arena"]["extent_m"][1], u))
    line3 = ("camera: ratified player_lock — yaw 47°, pitch α = %.4f°, "
             "orthographic   ·   %.3f px/m up-screen   ·   plate-law "
             "cross-check PASSED   ·   nothing painted, no burst fired"
             % (a["pitch_alpha_deg"], a["px_per_m_up_screen"]))
    dr.text((MARGIN, 104), line2, font=f_h2, fill=DIM)
    dr.text((MARGIN, 142), line3, font=f_h2, fill=DIM)
    dr.line([(MARGIN, HEADER - 24), (W - MARGIN, HEADER - 24)], fill=RULE,
            width=2)

    lx, rx = MARGIN, MARGIN + PANEL_W + GAP
    py = HEADER
    dr.text((lx, py - 2), "THE MEASURED ARENA  (galadriel trace v1, 177-vertex "
            "ring)", font=f_lbl, fill=INK)
    dr.text((rx, py - 2), "THE CATHEDRAL GREY ROOM  (Antwerp plan on that "
            "footprint)", font=f_lbl, fill=INK)
    py += 44
    img.paste(trace, (lx, py))
    img.paste(guide, (rx, py))
    dr.rectangle([lx, py, lx + PANEL_W, py + ph], outline=RULE, width=2)
    dr.rectangle([rx, py, rx + PANEL_W, py + ph], outline=RULE, width=2)

    # Panel captions, wrapped inside their own panel width.  The first cut let
    # both single lines run to their natural length and they collided in the
    # gutter; a caption that overprints another caption is not a caption.
    def caption(x, y, text, width):
        words, line, lines = text.split(), "", []
        for wd in words:
            t = (line + " " + wd).strip()
            if dr.textlength(t, font=f_small) > width:
                lines.append(line)
                line = wd
            else:
                line = t
        lines.append(line)
        for i, L in enumerate(lines):
            dr.text((x, y + i * 26), L, font=f_small, fill=DIM)
        return len(lines)

    cap = py + ph + 10
    n1 = caption(lx, cap,
                 "cyan = walked perimeter · red dashed = the two mapped-but-"
                 "never-walked arcs · amber = the 4 interior obstructions · "
                 "green outline = DoT radius UPPER BOUND · green fill = the "
                 "disjoint-preserving disc the grey room actually carries",
                 PANEL_W)
    n2 = caption(rx, cap,
                 "walkable floor is the brightest and calmest (brief § 4) · "
                 "full-bleed: no void, no border, no sky · amber = declared "
                 "lantern and choir screen · cyan = the measured ring · dashed "
                 "green = the rot envelope",
                 PANEL_W)

    # ---- mapping table ------------------------------------------------------
    ty = cap + max(n1, n2) * 26 + 24
    dr.line([(MARGIN, ty), (W - MARGIN, ty)], fill=RULE, width=2)
    ty += 18
    dr.text((MARGIN, ty), "THE MAPPING  (refs README · dispatch § The mapping)",
            font=f_lbl, fill=INK)
    ty += 46
    colx = [MARGIN, MARGIN + 60, MARGIN + 760, MARGIN + 1810, MARGIN + 2560]
    dr.text((colx[1], ty), "ARENA FEATURE", font=f_rowb, fill=DIM)
    dr.text((colx[2], ty), "CATHEDRAL ELEMENT", font=f_rowb, fill=DIM)
    dr.text((colx[3], ty), "GREY-ROOM CLASS", font=f_rowb, fill=DIM)
    dr.text((colx[4], ty), "DERIVED FROM", font=f_rowb, fill=DIM)
    ty += 38
    derivation = {
        "1": "ring north of y_join, inside its own measured x-extent",
        "2": "floor from y_join to the choir band",
        "3": "floor north of y_join, outside that x-extent",
        "4": "OB-1 / OB-2 polygons, verbatim",
        "5": "floor south of the choir band; OB-3 altar, OB-4 tomb",
        "6": "measured interior point + radius UPPER BOUND, clipped to floor",
    }
    for n, arena, cath, klass in MAPROWS:
        dr.ellipse([colx[0], ty + 2, colx[0] + 34, ty + 36],
                   fill=(12, 12, 14), outline=C_CALL, width=2)
        dr.text((colx[0] + 17, ty + 19), n, font=f_num, fill=C_CALL,
                anchor="mm")
        dr.text((colx[1], ty + 4), arena, font=f_row, fill=INK)
        dr.text((colx[2], ty + 4), cath, font=f_row, fill=INK)
        c = cls[klass]
        dr.rectangle([colx[3], ty + 6, colx[3] + 28, ty + 32],
                     fill=tuple(c["guide_grey"]), outline=RULE)
        dr.rectangle([colx[3] + 34, ty + 6, colx[3] + 62, ty + 32],
                     fill=tuple(c["rgb"]), outline=RULE)
        dr.text((colx[3] + 72, ty + 4), "%s%s" % (
            klass, "  (walkable)" if c["walkable"] else ""),
            font=f_row, fill=INK if c["walkable"] else DIM)
        dr.text((colx[4], ty + 4), derivation[n], font=f_small, fill=DIM)
        ty += 46

    # ---- the two things Matt is being asked ---------------------------------
    ty += 16
    dr.line([(MARGIN, ty), (W - MARGIN, ty)], fill=RULE, width=2)
    ty += 18
    dz = man["dot_zones"]
    dr.text((MARGIN, ty), "OPEN AT M2", font=f_lbl, fill=C_CALL)
    ty += 42
    asks = [
        ("ROT EXTENT", "the six radii are UPPER BOUNDS, not measurements. At "
         "the raw bound the discs cover %.1f %% of the walkable floor AND "
         "overlap each other — which contradicts the geometry file's own "
         "finding of six MUTUALLY DISTINCT zones, and contradicts brief § 4 "
         "'walkable = brightest and calmest'. The guide, the ID mask and "
         "dot_zone_mask.png therefore carry k = %.4f (%.1f %% of the floor) — "
         "the largest scale that keeps all six disjoint, which is drax's call, "
         "not a measurement. The raw bound ships beside them as "
         "dot_zone_mask_upper_bound.png (%.1f %%) and is drawn on the guide as "
         "a dashed green envelope: the rot is inside that line, nowhere else. "
         "Matt may overrule in either direction."
         % (100 * dz["envelope_floor_fraction"], dz["k_disjoint"],
            100 * dz["primary_floor_fraction"],
            100 * dz["envelope_floor_fraction"])),
        ("HEIGHT", "masonry rises %.1f m (reusing the KP-18(b) allowance "
         "already ruled for this arena) and is cut to %.1f m wherever rising "
         "would occlude play space. The VAULT is NOT on this plate: at %.1f "
         "px/m up-screen a true Antwerp springing would cover the northern "
         "half of it. It belongs on the Overhead layer (z3)."
         % (man["near_side_and_back_walls"]["rise_m"],
            man["near_side_and_back_walls"]["near_cut_m"],
            a["px_per_m_up_screen"])),
        ("PAINT COST", "%d chunks of %d×%d with %d px overlaps, grid origin "
         "chosen to keep the least walkable floor under the seams. That is %d "
         "images per style arm — the conductor may want the ZOOM-GD "
         "precedent (KP-B1a: paint at 0.752040 × and upscale 1.329717 ×) "
         "instead."
         % (man["chunk_grid"]["n_chunks"], man["chunk_grid"]["chunk_px"][0],
            man["chunk_grid"]["chunk_px"][1],
            man["chunk_grid"]["overlap_px"][0],
            man["chunk_grid"]["n_chunks"])),
    ]
    for head, body in asks:
        dr.text((MARGIN, ty), head, font=f_rowb, fill=C_CALL)
        words = body.split()
        line, lines = "", []
        for wd in words:
            t = (line + " " + wd).strip()
            if dr.textlength(t, font=f_small) > W - MARGIN - 260:
                lines.append(line)
                line = wd
            else:
                line = t
        lines.append(line)
        for i, L in enumerate(lines):
            dr.text((MARGIN + 210, ty + i * 28), L, font=f_small, fill=DIM)
        ty += max(34, len(lines) * 28 + 12)

    out = os.path.join(ROOT, "M2_review_cathedral_greyroom.png")
    img.crop((0, 0, W, min(H, ty + 30))).save(out)
    print("[review] %s  %dx%d" % (out, W, min(H, ty + 30)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
