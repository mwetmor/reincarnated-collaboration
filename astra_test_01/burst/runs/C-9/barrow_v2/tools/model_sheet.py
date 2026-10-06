#!/usr/bin/env python3
"""barrow_v2 MODEL SHEET at EXACTLY the game camera (lane BX, R-C9-156 check for Matt).

    python3 tools/model_sheet.py spec      -> greybox/sheet_tiles/spec.json (sizes from layout_v2.json models[])
    (render)  tools/greybox_godot.sh sheet  (godot/tools/model_sheet.gd: one model per tile, 1 m grid, 1 m cube,
              ortho, pitch = layout camera.pitch_deg, yaw 0, the V-views' light)
    python3 tools/model_sheet.py compose   -> greybox/models_sheet_gamecam.png (+ the JOIN-1 barbarian idle S frame
              composited in every tile at the tile's ppm: scale = ppm / ppm_render, anchor on its ground point;
              before/after of the toned tufts)

The FIRST sheet (commit 443150261's hand-back) was composed from BVP's normaliser stills (Blender, ortho, elevation
52.9535 deg, each model at its NORMALISATION size, not its slot size, in its own frame; no grid/cube/figure).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TD = os.path.join(ROOT, "greybox", "sheet_tiles")
HERO = os.path.join(ROOT, "..", "join1_pack", "d2-ww-barb-mx")
TONED = ("cliffplain", "crag", "cavecliff", "barrow")
ORDER = [("hall", "longhall", "longhall"), ("porch", "hall_porch", "hall_porch"), ("gable", "fallen_gable", "fallen_gable"),
         ("barrow", "barrow_front", "barrow"), ("wreck", "wreck", "wreck"), ("cavecliff", "cave_cliff", "cavecliff"),
         ("staircliff", "stair_cliff", "staircliff"), ("cliffplain", "cliff_faces", "cliffplain"), ("crag", "rock_outcrop_1", "crag")]


def spec():
    L = json.load(open(os.path.join(ROOT, "layout_v2.json")))
    M = {m["id"]: m for m in L["models"]}
    tiles = []
    for name, sid, glb in ORDER:
        m = M[sid]
        if m.get("instances"):
            w, d, h = m["instances"][0]["size_m"]
        else:
            w, d, h = m["size_m"]["w_local_x"], m["size_m"]["d_local_z"], m["size_m"]["h"]
        g = os.path.join(ROOT, "godot", "models", "build", glb + ".glb")
        tiles.append({"id": name, "slot": sid, "glb": g, "W": w, "D": d, "H": h, "variant": "after" if name in TONED else "as built"})
        if name in TONED:
            tiles.append({"id": name + "_before", "slot": sid, "glb": os.path.join(ROOT, "godot", "models", "build", "before_tufts", glb + ".glb"),
                          "W": w, "D": d, "H": h, "variant": "before"})
    os.makedirs(TD, exist_ok=True)
    json.dump({"camera": L["camera"], "tiles": tiles}, open(os.path.join(TD, "spec.json"), "w"), indent=1)
    print("spec", len(tiles), "tiles")


def compose():
    T = json.load(open(os.path.join(TD, "tiles.json")))
    idx = json.load(open(os.path.join(HERO, "matrix_index.json")))
    ppm_r = idx["camera"]["ppm_render"]
    ax, ay = idx["camera"]["anchor_px"]
    hero = Image.open(os.path.join(HERO, "cells", "idle", "S", "idle_S_00.png")).convert("RGBA")
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    fb = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    fs = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
    tiles = {t["id"]: t for t in T["tiles"]}
    cw, ch = 900, 700
    main = [n for n, _, _ in ORDER]
    befores = [n + "_before" for n in TONED]
    rows_main = 3
    sheet = Image.new("RGB", (3 * cw, 90 + rows_main * (ch + 40) + 60 + (ch // 2 + 40)), (247, 247, 244))
    d = ImageDraw.Draw(sheet)
    cam = T["camera"]
    d.text((14, 12), "barrow_v2 Tripo models, each alone at EXACTLY the game camera: orthographic, pitch %.4f deg, yaw %.1f deg (the V-views' transform, "
           "read from layout_v2.json camera); 1 m grid, 1 m blue cube, and the JOIN-1 barbarian (idle S, h 1.85 m) composited at each tile's ppm" % (cam["pitch_deg"], cam["yaw_deg"]),
           fill=(15, 15, 15), font=f)
    d.text((14, 44), "each model fitted to its slot size exactly as the scene places it; plain lit, unpainted. Rock/barrow tufts: toned (AFTER); BEFORE row at the bottom.",
           fill=(60, 60, 60), font=fs)

    def tile_img(t, scale=1.0):
        im = Image.open(os.path.join(TD, t["id"] + ".png")).convert("RGBA")
        s = t["ppm"] / ppm_r
        hh = hero.resize((max(1, int(hero.width * s)), max(1, int(hero.height * s))), Image.LANCZOS)
        px, py = t["hero_anchor_px"]
        im.alpha_composite(hh, (int(round(px - ax * s)), int(round(py - ay * s))))
        if scale != 1.0:
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        return im.convert("RGB")
    for k, n in enumerate(main):
        t = tiles[n]
        x, y = (k % 3) * cw, 90 + (k // 3) * (ch + 40)
        sheet.paste(tile_img(t), (x, y + 34))
        d.text((x + 10, y + 4), "%s -> slot %s  (%s)" % (n, t["slot"], t["variant"]), fill=(10, 30, 90), font=fb)
        d.text((x + 10, y + 34 + ch - 26), "%.1f x %.1f x %.1f m | ortho size %.2f m | %.2f px/m" % (t["W"], t["D"], t["H"], t["ortho_size_m"], t["ppm"]),
               fill=(30, 30, 30), font=fs)
    yb = 90 + rows_main * (ch + 40) + 20
    d.text((14, yb), "BEFORE (as built: bright red leafy tufts) vs AFTER (toned toward sketch A's muted rust heather, broken into smaller tufts) -- half size",
           fill=(15, 15, 15), font=fb)
    for k, n in enumerate(TONED):
        x = k * (3 * cw // 4)
        b = tile_img(tiles[n + "_before"], 0.5)
        a = tile_img(tiles[n], 0.5)
        # side by side within the quarter: before | after, each scaled to fit
        q = 3 * cw // 4 - 8
        bb = b.resize((q // 2, int(b.height * (q // 2) / b.width)))
        aa = a.resize((q // 2, int(a.height * (q // 2) / a.width)))
        sheet.paste(bb, (x + 4, yb + 36))
        sheet.paste(aa, (x + 4 + q // 2, yb + 36))
        d.text((x + 8, yb + 38), "%s before" % n, fill=(120, 20, 20), font=fs)
        d.text((x + 8 + q // 2, yb + 38), "after", fill=(20, 90, 30), font=fs)
    out = os.path.join(ROOT, "greybox", "models_sheet_gamecam.png")
    sheet.save(out, optimize=True)
    print("wrote", out, sheet.size)


if __name__ == "__main__":
    {"spec": spec, "compose": compose}[sys.argv[1]]()
