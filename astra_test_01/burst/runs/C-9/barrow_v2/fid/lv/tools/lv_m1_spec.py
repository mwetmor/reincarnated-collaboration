#!/usr/bin/env python3
"""BV2F LV M1: the still list (fid/lv/M1/stills_spec.json) from layout v7b: the start, each spawn disc (him at the anchor),
each deliverer approach (him on the floor 2.5 m in from the edge on the deliverer's lane). (u, v) = (x, -y)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
sys.path.insert(0, os.path.normpath(os.path.join(LV, "..", "..", "tools")))
import bv2_geom as G
L = json.load(open(os.path.join(LV, "layout_v7b.json")))
floor = [tuple(p) for p in L["floor"]["polygon"]]
uv = lambda p: [round(p[0], 3), round(-p[1], 3)]
spec = [{"name": "01_start", "uv": [0.0, 0.0], "facing": "S", "what": "the start, in the stone circle"}]
names = {"p01": "wreck", "p02": "barrow_door", "p03": "sea_cave_stair", "p04": "hall_great_door", "p05": "mere_ambush", "p06": "fallen_gable"}
n = 2
for a in L["anchors"]["points"]:
    spec.append({"name": "%02d_disc_%s_%s" % (n, a["id"], names[a["id"]]), "uv": uv((a["x"], a["y"])), "facing": "S", "what": "%s's spawn disc" % a["id"]})
    n += 1
for ln in L["lanes"]:
    cl = ln["centreline"]
    pick = None
    for p in cl:
        if G.point_in_poly(tuple(p), floor) and G.signed_clearance(tuple(p), floor) >= 1.0:
            pick = p
            break
    pick = pick or cl[-1]
    spec.append({"name": "%02d_approach_%s" % (n, ln["opening"]), "uv": uv(pick), "facing": "N", "what": "approach to the %s (%s)" % (ln["opening"], ln["point"])})
    n += 1
import math
fx=[p[0] for p in floor]; fy=[p[1] for p in floor]
spec.append({"name": "map_topdown", "topdown": [(min(fx)+max(fx))/2, -(min(fy)+max(fy))/2, 112.0], "what": "the map's base: straight down, +u right, +v up"})
os.makedirs(os.path.join(LV, "M1"), exist_ok=True)
json.dump(spec, open(os.path.join(LV, "M1", "stills_spec.json"), "w"), indent=1)
print(len(spec), [s["name"] for s in spec])
