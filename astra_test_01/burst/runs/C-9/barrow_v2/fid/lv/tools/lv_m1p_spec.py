#!/usr/bin/env python3
"""BV2F LV Phase 1' (M1'): the still list of the ART blockout, each framed on its hero(es) at v1's play camera and zoom,
him nearby for scale; each with the matching sketch A pixel (the same composition map make_bv2art.py uses).
    python3 fid/lv/tools/lv_m1p_spec.py   -> fid/lv/M1p/stills_spec.json"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
L = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
P = {p["id"]: p for p in L["placements"]}
O = {o["id"]: o for o in L["openings"]}
SP = math.sin(math.radians(52.95354112560294))
def px(u, v):
    return [round(780 + u * 24, 1), round(452 - v * 24 * SP, 1)]
def ouv(oid):
    c = O[oid]["centre_sim"]
    return (c[0], -c[1])
mere = [tuple(q) for q in L["regions"]["mere"]]
mere_c = (sum(q[0] for q in mere) / len(mere), sum(q[1] for q in mere) / len(mere))
mere_sw = min(mere, key=lambda q: q[0] + q[1])
mere_e = max(mere, key=lambda q: q[0])
wreck = tuple(P["wreck"]["uv"])
bdoor = ouv("barrow_door")
hdoor = ouv("hall_great_door")
gable = tuple(P["fallen_gable"]["uv"])
cave = ouv("sea_cave_mouth")
RP = {k: tuple(v) for k, v in L["route"]["points_uv"].items()}       # R-C9-188/189 the cave-to-clifftop route
def mid(a, b, f=0.5):
    return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
S = [("01_start_ring", (0.0, 0.0), (0.6, -1.6), 0.0, "the start in the broken stone ring", ["ring"]),
     ("02_wreck_mere", mid(wreck, mere_sw), (wreck[0] + 4.0, wreck[1] + 1.0), 0.0, "the wreck below the mere's shore", ["wreck", "mere"]),
     ("03_wreck", wreck, (wreck[0] + 5.5, wreck[1] - 1.0), 0.0, "the wreck, heeled in the shore ice, prow up", ["wreck"]),
     ("04_mere_barrow", mid(mere_e, bdoor), (mere_e[0] + 3.0, mere_e[1] - 2.0), 1.0, "the mere and the barrow door", ["mere", "barrow_door"]),
     ("05_barrow_door", (bdoor[0], bdoor[1] + 1.0), (bdoor[0] - 2.0, bdoor[1] - 3.5), 1.5, "the barrow's monumental carved door", ["barrow_door"]),
     ("06_mere", mere_c, (mere_c[0] + 2.0, mere_c[1] - 4.5), 0.0, "the frozen mere and the stream from the barrow", ["mere"]),
     ("07_ring_stair", (-2.0, -6.2), (-1.0, -4.0), -0.5, "from the ring to the clifftop stair", ["ring", "cave_stair"]),
     ("08_cave_stair", mid(RP["cave_mouth"], RP["stair_top"]), RP["shelf_mid"], -2.5, "the sea cave, the shelf and the stair up the cliff (R-C9-188/189); him on the shelf", ["cave_stair"]),
     ("09_hall_door", (hdoor[0] + 2.0, hdoor[1] + 1.0), (hdoor[0] - 3.5, hdoor[1] - 2.0), 1.5, "the burnt hall's great door, facing the start", ["hall_door"]),
     ("10_hall_gable", mid(hdoor, gable), (hdoor[0] - 3.0, hdoor[1] - 4.0), 1.0, "the hall and its fallen gable", ["hall_door", "gable"]),
     ("11_gable", gable, (gable[0] - 5.0, gable[1] + 0.5), 0.5, "the fallen gable, its own ruin", ["gable"]),
     ("12_ring_mere", mid((0.0, 0.0), mere_c, 0.45), (-2.0, 1.5), 0.0, "the ring and the mere", ["ring", "mere"])]
spec = []
for n, aim, him, h, what, heroes in S:
    spec.append({"name": n, "uv": [round(him[0], 3), round(him[1], 3)], "aim_uv": [round(aim[0], 3), round(aim[1], 3)], "aim_h": h, "facing": "S",
                 "what": what, "heroes": heroes, "sketch_px": px(*aim)})
win = L["window"]
spec.append({"name": "map_topdown", "topdown": [win["centre_uv"][0], win["centre_uv"][1], round((win["u"][1] - win["u"][0] + 3) * 2240 / 2400, 2)], "what": "the map's base (the whole window across)"})
os.makedirs(os.path.join(LV, "M1p"), exist_ok=True)
json.dump(spec, open(os.path.join(LV, "M1p", "stills_spec.json"), "w"), indent=1)
print(len(spec))
