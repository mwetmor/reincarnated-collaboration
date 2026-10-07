#!/usr/bin/env python3
"""BV2F LV Phase 1.3: stitch the four guide sections into the paint envelope, cut the 9 x 11 canvases, and build the
ID + CLASS maps.

    python3 fid/lv/tools/lv_guide_stitch.py

In : fid/lv/guide/s{00,01,10,11}/{guide.png, ids.png, ids.json}  (frozen Tier-B capture_blockout / capture_ids)
Out: fid/lv/guide/guide_v7b.png            11,776 x 8,704 (the envelope, v1's px/m)
     fid/lv/guide/tiles/guide_rRR_cCC.png  9 cols x 11 rows of 1536 x 1024 on a 1280 x 768 stride
     fid/lv/guide/ids_v7b.png              per-object IDs (capture_ids code; section-local ids remapped to one global table)
     fid/lv/guide/class_v7b.png            class index map (R = index into classes) + class_v7b_rgb.png (legend colours)
     fid/lv/guide/guide_manifest.json      shas, grid, the class table, per-class pixel shares, id table
The sections abut exactly: same orthographic camera, integer px offsets (the prep chose the centres so)."""
import hashlib
import json
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
VAR = os.environ.get("LV_VARIANT", "v7b")
GD = os.path.join(LV, "guide" if VAR == "v7b" else "guide_" + VAR)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", VAR))
lvl = json.load(open(os.path.join(BF, "level.json")))
CLASSES = lvl["classes"]
ENV = lvl["frame"]["envelope"]
W, H = ENV["px"]
CAN, STRIDE, COLS, ROWS = (1536, 1024), (1280, 768), 9, 11
PAL = {"none": (0, 0, 0), "snow": (235, 232, 224), "path": (150, 120, 90), "ice": (140, 190, 235), "shrub": (130, 140, 70),
       "rock": (110, 110, 112), "mound": (200, 190, 150), "shingle": (175, 160, 125), "shore_ice": (205, 230, 245),
       "stream": (90, 150, 230), "char": (45, 38, 34), "sea": (35, 60, 95), "wood": (150, 105, 65), "passage_dark": (15, 15, 15), "ash": (120, 112, 107)}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    guide = Image.new("RGB", (W, H))
    ids_g = np.zeros((H, W), np.int32)
    gtable, gidx = {}, {}
    for s in lvl["frame"]["sections"]:
        d = os.path.join(GD, s["id"])
        x0, y0 = s["px_origin"]
        pad = int(json.load(open(os.path.join(LV, VAR, "frame_grid_%s.json" % s["id"]))).get("pad_px", 0))
        sw, sh = s["px"]
        guide.paste(Image.open(os.path.join(d, "guide.png")).convert("RGB").crop((pad, pad, pad + sw, pad + sh)), (x0, y0))
        ij = json.load(open(os.path.join(d, "ids.json")))
        a = np.asarray(Image.open(os.path.join(d, "ids.png")).convert("RGB")).astype(np.int32)[pad:pad + sh, pad:pad + sw]
        code = a[..., 0] * 65536 + a[..., 1] * 256 + a[..., 2]
        local = np.zeros(code.shape, np.int32)
        for k, rec in ij["placements"].items():
            r, g, b = rec["rgb"]
            pid = rec["id"]
            if pid not in gidx:
                gidx[pid] = len(gidx) + 1
                gtable[gidx[pid]] = {"id": pid, "class": rec["class"], "piece": rec["piece"]}
            local[code == r * 65536 + g * 256 + b] = gidx[pid]
        ids_g[y0:y0 + local.shape[0], x0:x0 + local.shape[1]] = local
    gp = os.path.join(GD, "guide_%s.png" % VAR)
    guide.save(gp)
    os.makedirs(os.path.join(GD, "tiles"), exist_ok=True)
    tiles = []
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * STRIDE[0], r * STRIDE[1]
            p = os.path.join(GD, "tiles", f"guide_r{r:02d}_c{c:02d}.png")
            guide.crop((x, y, x + CAN[0], y + CAN[1])).save(p)
            tiles.append({"row": r, "col": c, "px": [x, y], "file": os.path.relpath(p, LV), "sha256": sha(p)})
    # ID image: 24-bit global id
    idimg = np.dstack([(ids_g >> 16) & 255, (ids_g >> 8) & 255, ids_g & 255]).astype(np.uint8)
    ip = os.path.join(GD, "ids_%s.png" % VAR)
    Image.fromarray(idimg, "RGB").save(ip)
    # CLASS map
    lut = np.zeros(len(gidx) + 1, np.uint8)
    for gi, rec in gtable.items():
        lut[gi] = CLASSES.index(rec["class"]) if rec["class"] in CLASSES else 0
    cls = lut[ids_g]
    cp = os.path.join(GD, "class_%s.png" % VAR)
    Image.fromarray(cls, "L").save(cp)
    pal = np.array([PAL.get(c, (255, 0, 255)) for c in CLASSES], np.uint8)
    Image.fromarray(pal[cls], "RGB").save(os.path.join(GD, "class_%s_rgb.png" % VAR))
    shares = {CLASSES[k]: round(float((cls == k).mean()), 5) for k in range(len(CLASSES)) if (cls == k).any()}
    unassigned = float((ids_g == 0).mean())
    man = {"_what": "BV2F LV Phase 1.3 class-tinted guide of layout %s" % VAR + "  (frozen Tier-B capture_blockout + capture_ids via godot_run.sh)",
           "envelope": ENV, "canvas": CAN, "stride": STRIDE, "cols": COLS, "rows": ROWS,
           "guide": {"file": os.path.relpath(gp, LV), "sha256": sha(gp), "px": [W, H]},
           "ids": {"file": os.path.relpath(ip, LV), "sha256": sha(ip), "code": "R<<16 | G<<8 | B = global id (table below); 0 = nothing (sky / none)"},
           "class": {"file": os.path.relpath(cp, LV), "sha256": sha(cp), "classes": CLASSES, "shares": shares, "unassigned_share": round(unassigned, 5)},
           "tints_srgb": lvl["tints_srgb"], "id_table": gtable, "tiles": tiles,
           "sections": {s["id"]: {"guide_sha256": sha(os.path.join(GD, s["id"], "guide.png")), "ids_sha256": sha(os.path.join(GD, s["id"], "ids.png"))} for s in lvl["frame"]["sections"]}}
    json.dump(man, open(os.path.join(GD, "guide_manifest.json"), "w"), indent=1)
    prev = guide.copy()
    prev.thumbnail((2000, 1600))
    prev.save(os.path.join(GD, "guide_%s_preview.jpg" % VAR), quality=88)
    cprev = Image.fromarray(pal[cls], "RGB")
    cprev.thumbnail((2000, 1600))
    cprev.save(os.path.join(GD, "class_%s_preview.jpg" % VAR), quality=88)
    print("[stitch] guide %dx%d, %d tiles, %d ids, class shares %s, unassigned %.4f" % (W, H, len(tiles), len(gidx), shares, unassigned))


if __name__ == "__main__":
    main()
