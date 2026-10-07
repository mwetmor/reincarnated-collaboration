#!/usr/bin/env python3
"""BV2F PT: class masks for PH's P11 stills (fid/ph/pilot_p11_spec.json class_masks): each still's ID pass (same camera,
pt_pilot_stills.gd) -> <name>.classes.png (8-bit, one value per class, 0 = other) + <name>.classes.json.
Id -> class (stated): rock = crags, bare rock ground, the barrow's stone facade; standing_stone = ring + slope stones;
wood = logs, palisade; sea = sea ground; wreck = the wreck; hall = longhall + fallen gable; cliff = cliff faces;
snow = snow, mound, path ground; ice = mere ice, shore ice, floes, stream; heather = shrub ground.
0 = other: shingle (neither snow nor rock), the barrow door's dark curtain, him, the 3D sprays and the snow field."""
import json, os, sys
import numpy as np
from PIL import Image
D = sys.argv[1]
SCHEMA = ["rock", "standing_stone", "wood", "sea", "wreck", "hall", "cliff", "snow", "ice", "heather"]
VAL = {c: i + 1 for i, c in enumerate(SCHEMA)}
def cls_of(i):
    if i.startswith(("crags__", "ground_rock")) or i == "barrow_front": return "rock"
    if i.startswith(("ring_stones__", "slope_stones__")): return "standing_stone"
    if i.startswith(("logs__", "palisade")): return "wood"
    if i == "ground_sea": return "sea"
    if i == "wreck": return "wreck"
    if i in ("longhall", "fallen_gable"): return "hall"
    if i.startswith("cliff_faces"): return "cliff"
    if i in ("ground_snow", "ground_mound", "ground_path"): return "snow"
    if i in ("ground_ice", "ground_shore_ice", "ground_stream") or i.startswith("blobs_shore_ice"): return "ice"
    if i == "ground_shrub": return "heather"
    return None
tab = json.load(open(os.path.join(D, "ids_table.json")))["ids"]
lut = np.zeros(256, np.uint8)
mapping = {}
for k, v in tab.items():
    c = cls_of(v["id"])
    mapping[v["id"]] = c
    if c:
        lut[int(k)] = VAL[c]
for f in sorted(os.listdir(D)):
    if not f.endswith(".ids.png"):
        continue
    nm = f[:-8]
    A = np.asarray(Image.open(os.path.join(D, f)).convert("RGB")).astype(np.int32)
    is_pl = A[..., 2] > 100
    idx = np.where(is_pl, np.clip(np.round((A[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                   + np.clip(np.round((A[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
    M = lut[np.clip(idx, 0, 255)]
    Image.fromarray(M, "L").save(os.path.join(D, nm + ".classes.png"))
    share = {c: round(float((M == VAL[c]).mean()), 4) for c in SCHEMA}
    json.dump({"ids": VAL, "share": share, "other_share": round(float((M == 0).mean()), 4),
               "source": f, "_mapping": "fid/pt/tools/pilot_class_masks.py (id -> class, stated in its header)"},
              open(os.path.join(D, nm + ".classes.json"), "w"), indent=1)
    print(nm, {k: v for k, v in share.items() if v > 0})
json.dump({"id_to_class": mapping, "values": VAL}, open(os.path.join(D, "classes_mapping.json"), "w"), indent=1)
