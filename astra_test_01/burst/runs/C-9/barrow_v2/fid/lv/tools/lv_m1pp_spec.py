#!/usr/bin/env python3
"""BV2F LV Phase 1'' (R-C9-204/205/206) M1'' packet: the still list -- each framed at v1's play camera and zoom on what Matt
asked to see (the coast, the wreck beach, the cliffs, the cave + stair twice, the mere + stream, the pack ice), with the
matching sketch A pixel for the side-by-side.   python3 fid/lv/tools/lv_m1pp_spec.py -> fid/lv/M1pp/stills_spec.json"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
L = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
RP = {k: tuple(v) for k, v in L["route"]["points_uv"].items()}
P = {p["id"]: p for p in L["placements"]}
SP, CP = math.sin(math.radians(52.95354112560294)), math.cos(math.radians(52.95354112560294))
def px(u, v, z=0.0):
    return [round(780 + u * 24, 1), round(452 - v * 24 * SP - z * 24 * CP, 1)]
mid = lambda a, b, f=0.5: (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
wreck = tuple(P["wreck"]["uv"])
mere = [tuple(q) for q in L["regions"]["mere_outline"]]
mere_c = (sum(q[0] for q in mere) / len(mere), sum(q[1] for q in mere) / len(mere))
S = [("01_coast_west", (-17.0, -8.0), (-12.0, -1.0), -2.0, "the W coast: the plateau, the shingle beach falling to the shore ice, the first sea cliffs", (-17.0, -8.0, -2.0)),
     ("02_wreck_beach", (wreck[0] + 1.5, wreck[1]), (-13.5, 2.0), -3.0, "the wreck on the shore ice at the foot of the shingle beach (4.2 m below the plateau)", (wreck[0], wreck[1], -4.2)),
     ("03_cliffs_south", (12.0, -20.5), (10.0, -12.0), -1.5, "the S sea cliffs (6-8 m), talus at the foot, a rock stack in the shore-fast ice", (12.0, -20.5, -1.5)),
     ("04_cave_stair", mid(RP["cave_mouth"], RP["stair_top"]), RP["shelf_mid"], -1.0, "the sea cave, the shelf and the rock-cut stair to the clifftop (R-C9-206)", (RP["cave_mouth"][0], RP["cave_mouth"][1], -3.5)),
     ("05_cave_mouth", RP["cave_mouth"], RP["shelf_mid"], -0.5, "the cave mouth: an eroded arch, 7.3 m clear, receding into the rock (R-C9-206)", (RP["cave_mouth"][0], RP["cave_mouth"][1], -3.5)),
     ("06_mere_stream", (mere_c[0] + 3.0, mere_c[1] + 1.0), (-5.0, 9.0), -0.2, "the mere's cracked ice plates and the stream channel from the barrow", (mere_c[0] + 3.0, mere_c[1] + 1.0, 0.0)),
     ("07_pack_ice", (-22.0, -17.0), (-12.0, -1.5), -4.2, "the sea: shore-fast ice, large plates, floes of every size (~2/3 ice)", (-22.0, -17.0, -4.2)),
     ("08_start", (0.0, -1.5), (0.0, 0.0), 0.0, "the start in the broken stone ring (unchanged)", (0.0, -1.5, 0.0))]
spec = []
for n, aim, him, h, what, sk in S:
    spec.append({"name": n, "uv": [round(him[0], 3), round(him[1], 3)], "aim_uv": [round(aim[0], 3), round(aim[1], 3)], "aim_h": h, "facing": "S",
                 "what": what, "sketch_px": px(*sk)})
win = L["window"]
spec.append({"name": "map_topdown", "topdown": [win["centre_uv"][0], win["centre_uv"][1], round((win["u"][1] - win["u"][0] + 3) * 2240 / 2400, 2)], "what": "the map's base"})
os.makedirs(os.path.join(LV, "M1pp"), exist_ok=True)
json.dump(spec, open(os.path.join(LV, "M1pp", "stills_spec.json"), "w"), indent=1)
print(len(spec))
