#!/usr/bin/env python3
"""BV2F PT (R-C9-280 step 4): score the DEV-25c A/B arms of chunk 3_0 -- READ-ONLY, PH's own instruments imported:
  a1 on band E (calibration s48 (d), B-1: the band DEV-25c's paste mask pastes; bar 8.789) -- p5v2.a_pair(2_0, arm, horiz,
     band=(0,128)) on the RAW canvases (2_0 = the kept PS4 canvas, the arm's left neighbour); band C (bar 11.045) and the
     full-256 a1 (s44, bar 9.569) reported, non-binding here
  P6a -- PH's v0.1 opening detector (p6_geometry.openings, T = s8 v1 ceiling, quarter scale) on each arm canvas placed at
     its plate position, every candidate matched to LV's declared openings (declared_openings.json, the s11 radius);
     an unmatched candidate = INVENTED
  1:1 crops of the strip boundary (x = 128 for B's paste end; x = 256 for A's), each arm, + the stitched view is not made
     (no stitch before the ruling)
-> fid/pt/ph3/ab25c/ab25c_score.json + crops/"""
import json, math, os, sys
import numpy as np
from PIL import Image
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
A9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts"
sys.path.insert(0, FID + "/ph/harness")
from common import *  # noqa
import p5v2 as V
import p6_geometry as G
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"   # (common exports a Path FID)
OUT = FID + "/pt/ph3/ab25c"
os.makedirs(OUT + "/crops", exist_ok=True)
X0, Y0 = 3 * 1280, 0          # chunk 3_0's plate origin
nb = V.load(A9 + "/BV2F-PH3-2_0/BV2F-PH3-2_0.png")
arms = {"A": A9 + "/BV2F-PH3-3_0-ab25cA/BV2F-PH3-3_0.png", "B": A9 + "/BV2F-PH3-3_0-ab25cB/BV2F-PH3-3_0.png"}
T = jload(PH / "results/p6.json")["invention"]["T_v1_ceiling"]
dec = []
for o in jload(FID + "/lv/guide_art/declared_openings.json")["openings"]:
    dec.append({"id": o["id"], "xy": tuple(o["centre_px"]), "radius_m": float(o["p6a_match_radius_m"])})
res = {"_what": __doc__.split("\n")[0], "bars": {"E": 8.789, "C": 11.045, "full_256": 9.569}, "arms": {}}
for arm, p in arms.items():
    im = V.load(p)
    r = {"sha256": V.sha(p)}
    for nm, band in (("E", (0, 128)), ("C", (128, 256)), ("full_256", None)):
        a = V.a_pair(nb, im, True, band)
        r["a1_" + nm] = {"max": round(max(a["a1"]), 3), "segments": [round(x, 3) for x in a["a1"]], "raw_mad": a["raw_mad"]}
    r["a1_E_pass"] = r["a1_E"]["max"] <= 8.789
    q = np.asarray(Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).resize((1536 // 4, 1024 // 4), Image.BOX), np.float32)
    found = G.openings(q, PPM_V1 * G.SC, T)
    cands = []
    for f in found:
        x, y = f["xy"][0] / G.SC + X0, f["xy"][1] / G.SC + Y0
        best = min(dec, key=lambda d: math.hypot(x - d["xy"][0], y - d["xy"][1]))
        dist = math.hypot(x - best["xy"][0], y - best["xy"][1]) / PPM_V1
        cands.append({"plate_xy": [round(x), round(y)], "nearest_declared": best["id"], "dist_m": round(dist, 2),
                      "matched": dist <= best["radius_m"]})
    r["p6a"] = {"candidates": cands, "invented": sum(not c["matched"] for c in cands)}
    r["p6a_pass"] = r["p6a"]["invented"] == 0
    # 1:1 crops at the strip boundary of this arm (A: x=256, B: x=128) and at the other position, 3 heights
    for xb in (128, 256):
        for yc in (180, 512, 840):
            y0 = max(0, min(1024 - 256, yc - 128)); x0 = max(0, xb - 128)
            Image.fromarray(np.clip(im[y0:y0 + 256, x0:x0 + 256], 0, 255).astype(np.uint8)).save(OUT + "/crops/arm%s_x%d_y%d.png" % (arm, xb, y0))
    res["arms"][arm] = r
# side-by-side sheets: per height, A | B at their own paste boundary (A x=256, B x=128) and both at x=256
sheet = Image.new("RGB", (4 * 256 + 24, 3 * 256 + 16), (255, 255, 255))
for j, yc in enumerate((180, 512, 840)):
    y0 = max(0, min(1024 - 256, yc - 128))
    for i, (arm, xb) in enumerate((("A", 256), ("B", 128), ("A", 128), ("B", 256))):
        sheet.paste(Image.open(OUT + "/crops/arm%s_x%d_y%d.png" % (arm, xb, y0)), (i * 264, j * 264))
sheet.save(OUT + "/crops/sheet_A256_B128_A128_B256.png")
res["sheet"] = "crops/sheet_A256_B128_A128_B256.png: columns = A at its paste end x=256 | B at its paste end x=128 | A at x=128 | B at x=256; rows y ~ 52 / 384 / 712; all 1:1"
json.dump(res, open(OUT + "/ab25c_score.json", "w"), indent=1)
print(json.dumps({a: {k: (v if not isinstance(v, dict) or k == "p6a" else v.get("max")) for k, v in r.items() if k != "p6a"} | {"p6a_invented": r["p6a"]["invented"], "p6a_n": len(r["p6a"]["candidates"])} for a, r in res["arms"].items()}, indent=1))
