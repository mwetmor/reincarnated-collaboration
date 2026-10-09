#!/usr/bin/env python3
"""C-2 (jack-ryan site Gate-2; s59) + D-1 (r339 delta Gate-2, R-C9-348: items 90, 91; item 17 re-centred): re-cut the 12 stale M3' packet crops from the FINAL r339 painting at their recorded
boxes -> results/site_r339/c2_recrops/*.jpg + c2_recrops.json (box, scale, how the box was established, sha256).
J08-J12: crop_box from pt/ph3/final/m3p_packet/index.json. Eye/P6a items: the box from the file name (x, y = top-left;
scale from the name), CONFIRMED by NCC against painting_pre_l5.png (the painting they were cut from) where it locates;
before/after pairs are re-cut as ONE panel (the final state)."""
import hashlib
import json
import sys
import os
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa

PAINT = FID / "pt/ph3/final/painting_ph3_r339_full.png"
OUT = PH / "results/site_r339/c2_recrops"
EYE = [("12_matt_eye_p6a_0_4_candidates", (480, 3700, 1600, 4096), 1.0, "name x,y top-left; NCC 0.984 vs pre_l5"),
       ("13_matt_eye_group1_playzoom", (0, 1536, 1520, 2560), 0.5, "name x,y; scale 0.5 located by NCC (0.53) at (16,1536)"),
       ("14_matt_eye_stern", (880, 2040, 1354, 2400), 1.0, "name x,y top-left; NCC 0.86 vs pre_l5 (after panel)"),
       ("15_matt_eye_cave_top", (2700, 2140, 3694, 2560), 1.0, "name x,y top-left; located by NCC at (2706,2140)"),
       ("17_p6a_fp_p6a_0_3_c016", (0, 3148, 512, 3462), 1.0, "D-1 (R-C9-348): RE-CENTRED on the current P6a candidate painting_0_3_c016 (203, 3305), open water; 512x314 clamped at x = 0. The original item 17 came from the superseded 0_3 raw canvas; the C-2 cut centred on (505, 3270) held no current candidate (superseded, file kept)"),
       ("18_p6a_fp_p6a_2_3", (2718, 2993, 3318, 3328), 1.0, "name x,y top-left; NCC 0.81"),
       ("19_p6a_fp_p6a_1_4_candidates", (1500, 3300, 2800, 4096), 0.75, "name x,y top-left, scale 0.75; NCC-located at the same box"),
       ("90_matt_eye_heart_floe_0_3", (0, 2304, 1536, 3328), 0.5, "D-1: the whole 0_3 chunk window at half scale; NCC 0.998 vs 8e169e6331bb at this box"),
       ("91_matt_eye_cave_mouth_stepped_rocks", (2900, 2500, 3700, 3100), 1.0, "D-1: NCC-located 0.868 vs r332 at this box, 1:1")]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    P = Image.open(PAINT).convert("RGB")
    idx = jload(FID / "pt/ph3/final/m3p_packet/index.json")
    items = [(j["file"][:3] + "_" + j["join"].replace("|", "I").replace("/", "S"), tuple(j["crop_box"]), 1.0, "index.json crop_box")
             for j in idx["fail_joins"] if j["file"][:3] in ("J08", "J09", "J10", "J11", "J12")] + EYE
    rows = []
    for nm, box, s, how in items:
        im = P.crop(box)
        if s != 1.0:
            im = im.resize((int(round(im.size[0] * s)), int(round(im.size[1] * s))), Image.LANCZOS)
        fn = OUT / ("%s_r339_x%d_y%d_%s.jpg" % (nm, box[0], box[1], "1to1" if s == 1.0 else "s%03d" % int(s * 100)))
        im.save(fn, quality=92)
        rows.append({"item": nm, "box_xyxy": list(box), "scale": s, "how": how, "file": str(fn.relative_to(FID)),
                     "sha256": hashlib.sha256(fn.read_bytes()).hexdigest()})
    dump({"_what": "C-2 + D-1 re-crops from the FINAL r339 painting", "painting_sha256": sha256(PAINT), "crops": rows,
          "superseded": [{"item": "17_p6a_fp_p6a_0_3_candidate (C-2 cut)", "file": "ph/results/site_r339/c2_recrops/17_p6a_fp_p6a_0_3_candidate_r339_x249_y3113_1to1.jpg",
                          "why": "centred on (505, 3270): no current P6a candidate in its box (jack-ryan r339 delta Gate-2 D-1)"}]}, str(OUT.parent / "c2_recrops.json"))
    for r in rows:
        print(r["item"], r["box_xyxy"], r["scale"], r["sha256"][:12])


if __name__ == "__main__":
    main()
