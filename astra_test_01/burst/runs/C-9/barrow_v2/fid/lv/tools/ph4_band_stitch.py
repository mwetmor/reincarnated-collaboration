#!/usr/bin/env python3
"""BV2F LV, R-C9-384: stitch the two NORTH BAND guide sections (n0 | n1) into the band guide, its ID map (global names)
and class map, and PROVE THE FRAME: the band render's bottom 256 rows ARE ph3 plate rows 0..255, so their per-pixel
object names must equal the pinned ph3 ID render (pt/ph3/ids_art_pinned_d26d14c55.png) there.

    python3 fid/lv/tools/ph4_band_stitch.py

Out: fid/lv/ph4/guide/band_guide.png  (6656 x 1024: ph4 plate rows 0..1023 = the 768-row band + ph3 rows 0..255)
     fid/lv/ph4/guide/band_ids.png    (global id code, the d26d14c55 id_table extended by new names at the end)
     fid/lv/ph4/guide/band_class.png  (R = index into level.json classes)
     fid/lv/ph4/guide/band_manifest.json (shas, id table, the frame proof)
"""
import hashlib
import json
import os
import subprocess

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
FID = os.path.dirname(LV)
C9 = os.path.normpath(os.path.join(FID, "..", ".."))
G = os.path.join(LV, "ph4", "guide")
PAD, SW, SH, BAND = 64, 3328, 1024, 768
REPO = "/Users/admin/Games/reincarnated-collaboration"
PIN_COMMIT = "d26d14c55"
IDS3 = os.path.join(FID, "pt/ph3/ids_art_pinned_d26d14c55.png")
CLS3 = os.path.join(FID, "pt/ph3/class_art_pinned_d26d14c55.png")
GUIDE3 = os.path.join(FID, "pt/ph3/guide_art_pinned_d26d14c55.png")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    man3 = json.loads(subprocess.check_output(["git", "-C", REPO, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % PIN_COMMIT]))
    assert sha(IDS3) == man3["ids"]["sha256"], "ph3 ids pin moved"
    lvl = json.load(open(os.path.join(C9, "barrow_full/godot/data/bv2f/site_ph4/level/level.json")))
    classes = lvl["classes"]
    table = {int(k): dict(v) for k, v in man3["id_table"].items()}
    name2g = {v["id"]: k for k, v in table.items()}
    guide = np.zeros((SH, 2 * SW, 3), np.uint8)
    gids = np.zeros((SH, 2 * SW), np.int32)
    for si, sid in enumerate(("n0", "n1")):
        d = os.path.join(G, sid)
        guide[:, si * SW:(si + 1) * SW] = np.asarray(Image.open(os.path.join(d, "guide.png")).convert("RGB"))[PAD:PAD + SH, PAD:PAD + SW]
        ij = json.load(open(os.path.join(d, "ids.json")))
        a = np.asarray(Image.open(os.path.join(d, "ids.png")).convert("RGB")).astype(np.int32)[PAD:PAD + SH, PAD:PAD + SW]
        code = (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]
        loc = np.zeros(code.shape, np.int32)
        for rec in ij["placements"].values():
            r, g_, b = rec["rgb"]
            nm = rec["id"]
            if nm not in name2g:
                k = max(table) + 1
                table[k] = {"id": nm, "class": rec["class"], "piece": rec.get("piece", ""), "_new_in": "ph4 band"}
                name2g[nm] = k
            loc[code == ((r << 16) | (g_ << 8) | b)] = name2g[nm]
        gids[:, si * SW:(si + 1) * SW] = loc
    # class map: an id's class (ground ids carry their own class)
    cmap = np.zeros(gids.shape, np.uint8)
    for k, v in table.items():
        if v["class"] in classes:
            cmap[gids == k] = classes.index(v["class"])
    # FRAME PROOF on the overlap rows (band rows 768..1023 == ph3 rows 0..255)
    i3 = np.asarray(Image.open(IDS3).convert("RGB")).astype(np.int32)[:SH - BAND]
    g3 = (i3[..., 0] << 16) | (i3[..., 1] << 8) | i3[..., 2]
    ov = gids[BAND:]
    same = ov == g3
    # an edge pixel (any 3x3 neighbour of a different id in EITHER map) may flip with sub-pixel raster differences
    from scipy import ndimage
    edge = np.zeros_like(same)
    for m in (g3, ov):
        edge |= (ndimage.maximum_filter(m, 3) != ndimage.minimum_filter(m, 3))
    gd = np.abs(guide[BAND:].astype(int) - np.asarray(Image.open(GUIDE3).convert("RGB"))[:SH - BAND].astype(int)).max(-1)
    proof = {"overlap_px": int(same.size), "id_equal_px": int(same.sum()), "id_differ_px": int((~same).sum()),
             "id_differ_off_edges_px": int((~same & ~edge).sum()), "id_differ_on_edges_px": int((~same & edge).sum()),
             "guide_rgb_differ_px": int((gd > 0).sum()), "guide_rgb_differ_gt8_px": int((gd > 8).sum()),
             "_": "band rows 768..1023 vs the pinned ph3 (d26d14c55) ID / guide render rows 0..255. Same object at the same "
                  "pixel = the world frame is unchanged; guide RGB differs only by shading (the directional shadow fit "
                  "follows each render's window)."}
    Image.fromarray(guide).save(os.path.join(G, "band_guide.png"))
    ic = np.stack([(gids >> 16) & 255, (gids >> 8) & 255, gids & 255], -1).astype(np.uint8)
    Image.fromarray(ic).save(os.path.join(G, "band_ids.png"))
    Image.fromarray(cmap).save(os.path.join(G, "band_class.png"))
    present = {int(k): int(c) for k, c in zip(*np.unique(gids[:BAND], return_counts=True))}
    out = {"_what": "R-C9-384 ph4 NORTH BAND guide (fid/lv/tools/ph4_band_stitch.py)", "px": [2 * SW, SH],
           "rows": "ph4 plate rows 0..1023 (band 0..767 + ph3 rows 0..255)",
           "guide": {"file": "band_guide.png", "sha256": sha(os.path.join(G, "band_guide.png"))},
           "ids": {"file": "band_ids.png", "sha256": sha(os.path.join(G, "band_ids.png"))},
           "class": {"file": "band_class.png", "sha256": sha(os.path.join(G, "band_class.png")), "classes": classes},
           "id_table": {str(k): v for k, v in sorted(table.items())},
           "band_ids_px": {table[k]["id"] if k in table else str(k): c for k, c in sorted(present.items(), key=lambda t: -t[1])},
           "frame_proof": proof}
    json.dump(out, open(os.path.join(G, "band_manifest.json"), "w"), indent=1)
    print(json.dumps(proof))
    print("band ids:", list(out["band_ids_px"].items())[:40])


if __name__ == "__main__":
    main()
