#!/usr/bin/env python3
"""BV2F LV Phase 1'' close-out (R-C9-226 item 7): the M1'' still list -- each framed at v1's play camera and zoom on one
feature, with the sketch A pixel of THE SAME FEATURE for the side-by-side crop (picked by eye off sketch A, not projected:
the blockout moves features off sketch A's own spots where the scene needs room -- e.g. the cove sits ~9 m east of sketch
A's cave -- so a projected pixel would crop the wrong thing).
    python3 fid/lv/tools/lv_m1pp_spec.py -> fid/lv/M1pp/stills_spec.json"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
L = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
RP = {k: tuple(v) for k, v in L["route"]["points_uv"].items()}
P = {p["id"]: p for p in L["placements"]}
mid = lambda a, b, f=0.5: (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
wreck = tuple(P["wreck"]["uv"])
mere = [tuple(q) for q in L["regions"]["mere_outline"]]
mere_c = (sum(q[0] for q in mere) / len(mere), sum(q[1] for q in mere) / len(mere))
cove_c = mid(RP["cave_mouth"], RP["bottom_landing"])
# name, aim (uv), him (uv), aim height, caption, sketch A px of the same feature
S = [("01_coast_west", (-17.0, -7.0), (-12.0, -1.0), -2.0, "the W coast: the plateau, the shingle beach falling to the shore ice, the first sea cliffs", (330, 600)),
     ("02_wreck_beach", (wreck[0] + 1.5, wreck[1]), (-13.5, 2.0), -3.0, "the wreck heeled into ragged shore-fast ice at the beach foot (no rectangle, R-C9-228)", (150, 440)),
     ("03_cliffs_south", (12.0, -20.5), (10.0, -12.0), -1.5, "the S sea cliffs (6-8 m): rock-kit columns, talus, a stack in the shore-fast ice", (1050, 860)),
     ("04_cove_close", mid(RP["cave_mouth"], RP["stair_foot"]), RP["shelf_mid"], -2.0,
      "CLOSE: the cave worn into the cliff face at the waterline, the stair in a natural gully beside it (R-C9-228)", (600, 780)),
     ("05_cave_mouth", RP["cave_mouth"], RP["shelf_mid"], -1.0, "the cave mouth: a dark tide-worn arch in the face, 7 m clear, sea and floes at its mouth, a small iced ledge", (560, 790)),
     ("06_mere", (mere_c[0] + 2.0, mere_c[1] - 1.0), (-5.0, 8.0), -0.2, "the mere (~440 m2): mostly continuous ice, a few long branching cracks, reed islands (R-C9-227)", (430, 250)),
     ("07_pack_ice", (-22.0, -17.0), (-12.0, -1.5), -4.2, "the sea: irregular pack -- huge and tiny plates, rubble zones, leads of every width (~2/3 ice, R-C9-227)", (250, 840)),
     ("08_start", (0.0, -1.5), (0.0, 0.0), 0.0, "the start in the stone circle (4 standing, 2 fallen low blocks)", (780, 470)),
     ("09_stair_close", mid(RP["stair_foot"], RP["stair_top"]), RP["bottom_landing"], -1.5,
      "CLOSE: the stair -- every tread its own stone (snow on top, bare stone at the front), 5 m clear, climbing inland", (645, 740)),
     ("10_cove_wide", cove_c, (cove_c[0] - 1.0, cove_c[1] + 6.0), -1.5,
      "WIDE: the continuous cliff line -- the cave in the face, the stair gully between rock columns", (610, 770)),
     ("11_mere_sea", (-29.0, 9.0), (-22.0, 6.0), -1.5, "the mere turning into the sea: irregular cracks widening westward into leads and rubble, reed islands (R-C9-229)", (170, 330)),
     ("12_river_mere", (-25.5, 17.5), (-18.0, 13.0), 0.0, "the river: a tiny UN-FROZEN ribbon of open water down the coast into the mere's ice (R-C9-227)", (230, 110)),
     ("13_hall_yard", (12.5, 2.5), (6.0, 0.0), 0.0, "the burnt hall's ash yard: an irregular trampled patch, no straight edges", (1290, 520))]
spec = []
for n, aim, him, h, what, sk in S:
    spec.append({"name": n, "uv": [round(him[0], 3), round(him[1], 3)], "aim_uv": [round(aim[0], 3), round(aim[1], 3)], "aim_h": h, "facing": "S",
                 "what": what, "sketch_px": list(sk)})
win = L["window"]
spec.append({"name": "map_topdown", "topdown": [win["centre_uv"][0], win["centre_uv"][1], round((win["u"][1] - win["u"][0] + 3) * 2240 / 2400, 2)], "what": "the map's base"})
os.makedirs(os.path.join(LV, "M1pp"), exist_ok=True)
json.dump(spec, open(os.path.join(LV, "M1pp", "stills_spec.json"), "w"), indent=1)
print(len(spec))
