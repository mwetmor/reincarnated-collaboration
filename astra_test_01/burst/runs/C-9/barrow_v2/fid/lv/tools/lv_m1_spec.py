#!/usr/bin/env python3
"""BV2F LV M1 (R-C9-177 d): the still list for one layout variant -- every still FRAMED ON ITS HERO OBJECT at v1's play
camera and zoom, the character at the spawn disc's edge for scale.
    LV_VARIANT=v7c python3 fid/lv/tools/lv_m1_spec.py   -> fid/lv/M1/stills_spec_<variant>.json
  01        the start (camera on the start, him in the circle)
  02-07     the six deliverers, hero-centred: the opening (aimed at its mid-height); him on the disc edge facing it
  08-13     each spawn disc with its deliverer: camera halfway between the disc's centre and the opening; him at the centre
  14        the cave top + the stair (camera on the top landing)
  map       the labelled top-down base
(u, v) = (sim x, -sim y)."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
VAR = os.environ.get("LV_VARIANT", "v7c")
lvl = json.load(open(os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", VAR, "level.json"))))
L = json.load(open(os.path.join(LV, "layout_%s.json" % VAR)))
uv = lambda p: [round(p[0], 3), round(-p[1], 3)]
A = {a["id"]: (a["x"], a["y"]) for a in L["anchors"]["points"]}
OP = {o["point"]: o for o in lvl["sim"]["openings"]}
NAME = {"p01": "wreck", "p02": "barrow_door", "p03": "sea_cave", "p04": "hall_great_door", "p05": "mere", "p06": "fallen_gable"}


def facing(p, q):
    d = (q[0] - p[0], q[1] - p[1])
    return "N" if d[1] < -abs(d[0]) else "S" if d[1] > abs(d[0]) else ("E" if d[0] > 0 else "W")


spec = [{"name": "01_start", "uv": [0.0, 0.0], "aim_uv": [0.0, 0.0], "facing": "S", "what": "the start, in the stone circle", "point": "start"}]
for i, pid in enumerate(["p01", "p02", "p03", "p04", "p05", "p06"]):
    o = OP[pid]
    hc = o["centre_sim"]
    z = (o["z0"] + o["h"] / 2.0) if o.get("h") else 0.0
    a = A[pid]
    d = (hc[0] - a[0], hc[1] - a[1]); n = math.hypot(*d)
    if n < 2.0:
        d = (-a[0], -a[1]); n = math.hypot(*d)
    edge = (a[0] + 8.0 * d[0] / n, a[1] + 8.0 * d[1] / n)
    spec.append({"name": "%02d_hero_%s_%s" % (2 + i, pid, NAME[pid]), "uv": uv(edge), "aim_uv": uv(hc), "aim_h": round(z, 2), "facing": facing(edge, hc),
                 "what": "%s's deliverer, the %s, centred (him on the disc edge for scale)" % (pid, NAME[pid].replace("_", " ")), "point": pid, "hero": NAME[pid]})
for i, pid in enumerate(["p01", "p02", "p03", "p04", "p05", "p06"]):
    o = OP[pid]
    a = A[pid]
    hc = o["centre_sim"]
    mid = ((a[0] + hc[0]) / 2, (a[1] + hc[1]) / 2)
    spec.append({"name": "%02d_disc_%s_%s" % (8 + i, pid, NAME[pid]), "uv": uv(a), "aim_uv": uv(mid), "facing": facing(a, hc),
                 "what": "%s's spawn disc and its deliverer (him at the disc's centre)" % pid, "point": pid, "hero": NAME[pid]})
tl = L["stair"]["top_landing"]["polygon"]
c = (sum(q[0] for q in tl) / len(tl), sum(q[1] for q in tl) / len(tl))
spec.append({"name": "14_cave_top_stair", "uv": uv(A["p03"]), "aim_uv": uv(c), "aim_h": -3.0, "facing": "S", "what": "the cave top and the stair (R-C9-148)", "point": "p03", "hero": "stair"})
fx = [p[0] for p in L["floor"]["polygon"]]; fy = [p[1] for p in L["floor"]["polygon"]]
spec.append({"name": "map_topdown", "topdown": [(min(fx) + max(fx)) / 2, -(min(fy) + max(fy)) / 2, 112.0], "what": "the map's base: straight down, +u right, +v up"})
os.makedirs(os.path.join(LV, "M1"), exist_ok=True)
json.dump(spec, open(os.path.join(LV, "M1", "stills_spec_%s.json" % VAR), "w"), indent=1)
print(VAR, len(spec), [s["name"] for s in spec])
