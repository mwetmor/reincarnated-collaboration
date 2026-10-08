#!/usr/bin/env python3
"""BV2F LV Phase 1' DONE item (R-C9-186 W-3): the HERO-COVERAGE table, mechanical, from the ID render of the M1' stills
(barrow_full/godot/tools/bv2f/m1_stills.gd with M1_IDS=1: the same play-camera frames, one flat colour per placed node).
A hero is VISIBLE in a still at >= MIN_PX pixels (0.5 m2 at the play camera). PASS = every one of the 7 heroes is visible in
>= 1 still where >= 1 OTHER hero is also visible.  -> fid/lv/M1p/hero_coverage.json + .md"""
import json, os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
M1 = os.environ.get("M1DIR", "M1p")
RAW = os.path.join(LV, M1, "stills_raw")
MIN_PX = 5000
HEROES = {"wreck": ["wreck"], "cave_stair": ["curtain_sea_cave_mouth", "stair_steps", "stair_treads", "stair_snow"], "barrow_door": ["barrow_front", "curtain_barrow_door"],
          "mere": ["ground_ice", "mere_plates"], "ring": ["ring_stones"], "hall_door": ["curtain_hall_great_door", "longhall"], "gable": ["fallen_gable"]}
if M1 == "M1pp":   # Phase 1'': the heroes Matt asked to see (R-C9-204/206); the rest are unchanged and outside these stills
    HEROES = {"wreck": ["wreck"], "cliffs": ["cliff_faces", "cliff_skirt_wall", "carved_rock"], "cave_stair": ["carved_passage_dark", "carved_tide_ice", "carved_wet_rock", "curtain_sea_cave_mouth"],
              "mere": ["ground_ice", "mere_cracks"], "river": ["stream_cracks", "ground_ice"], "sea_ice": ["ice_shorefast", "ice_plates", "ice_floes", "ice_floes_bob"],
              "stacks_talus": ["sea_stacks", "talus"], "ring": ["ring_stones", "ring_fallen"]}
ij = json.load(open(os.path.join(RAW, "stills_ids.json")))
code = {v["id"]: v["rgb"][0] * 65536 + v["rgb"][1] * 256 + v["rgb"][2] for v in ij["id_table"].values()}
spec = [s for s in json.load(open(os.path.join(LV, M1, "stills_spec.json"))) if "topdown" not in s]
rows = {}
for s in spec:
    a = np.asarray(Image.open(os.path.join(RAW, s["name"] + "_ids.png")).convert("RGB")).astype(np.int64)
    c = a[..., 0] * 65536 + a[..., 1] * 256 + a[..., 2]
    vals, cnts = np.unique(c, return_counts=True)
    cm = dict(zip(vals.tolist(), cnts.tolist()))
    rows[s["name"]] = {h: int(sum(cm.get(code[i], 0) for i in ids if i in code)) for h, ids in HEROES.items()}
table = {}
for h in HEROES:
    vis = [n for n, r in rows.items() if r[h] >= MIN_PX]
    with_n = [n for n in vis if sum(1 for h2 in HEROES if h2 != h and rows[n][h2] >= MIN_PX) >= 1]
    table[h] = {"visible_in": vis, "with_neighbour_in": with_n, "PASS": len(with_n) >= 1}
ok = all(t["PASS"] for t in table.values())
json.dump({"_what": __doc__.strip().splitlines()[0], "min_px": MIN_PX, "pass": ok, "heroes": table, "px_per_still": rows}, open(os.path.join(LV, M1, "hero_coverage.json"), "w"), indent=1)
md = ["| Hero | Visible in (stills) | With a neighbour hero in | |", "|---|---|---|---|"]
for h, t in table.items():
    md.append("| %s | %s | %s | %s |" % (h, ", ".join(n[:2] for n in t["visible_in"]) or "-", ", ".join(n[:2] for n in t["with_neighbour_in"]) or "-", "PASS" if t["PASS"] else "**FAIL**"))
open(os.path.join(LV, M1, "hero_coverage.md"), "w").write("\n".join(md) + "\n")
print("\n".join(md)); print("hero coverage:", "PASS" if ok else "FAIL")
