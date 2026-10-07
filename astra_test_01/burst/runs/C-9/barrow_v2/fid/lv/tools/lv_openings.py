#!/usr/bin/env python3
"""BV2F LV Phase 1.3: the DECLARED-OPENING LIST for PH's P6a overlay (charter s13 G2-B1): every deliverer opening of layout
v7b -- id, anchor, model, width/height m, facing, centre and the four corners in GUIDE-ENVELOPE PLATE px (the stitched
11,776 x 8,704 guide; v1's projection, yaw 0 in the sim frame == the play camera under the frame fix), and the P6a match
radius (half-width + 1.0 m). Source: data/bv2f/level.json `sim.openings` (bv2f_level_prep.py, from the layout's slots).
    python3 fid/lv/tools/lv_openings.py   -> fid/lv/guide/declared_openings.json"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f"))
lvl = json.load(open(os.path.join(BF, "level.json")))
PPM = 100.617553710938
P = math.radians(52.95354112560294)
env = lvl["frame"]["envelope"]
u0, v1 = env["u"][0], env["v"][1]


def px(x, y, z):
    return [round((x - u0) * PPM, 1), round((v1 + y) * PPM * math.sin(P) - z * PPM * math.cos(P), 1)]   # v = -y


out = []
for o in lvl["sim"]["openings"]:
    t = math.radians(o["faces_deg"])
    f = (math.sin(t), -math.cos(t))
    tg = (-f[1], f[0])
    cx, cy = o["centre_sim"]
    hw, z0, h = o["w"] / 2, o["z0"], o["h"]
    corners = {k: px(cx + s * hw * tg[0], cy + s * hw * tg[1], z0 + zz) for k, s, zz in
               (("bottom_a", -1, 0.0), ("bottom_b", 1, 0.0), ("top_b", 1, h), ("top_a", -1, h))}
    out.append({"id": o["id"], "point": o["point"], "model": o["model"], "w_m": o["w"], "h_m": o["h"], "faces_deg": o["faces_deg"],
                "dark_in_guide": o["dark"], "centre_sim_xy": [cx, cy], "z0_m": z0, "centre_px": px(cx, cy, z0 + h / 2), "corners_px": corners,
                "p6a_match_radius_m": round(hw + 1.0, 3),
                "faces_camera": bool(-math.cos(t) > 0.05), "note": "faces_camera = the opening's facing has a component toward the camera (screen-down); False = seen from behind/edge-on at the play camera"})
json.dump({"_what": __doc__.strip().splitlines()[0], "envelope": env, "projection": "x = (u - u0) * 100.6176; y = (v1 - v) * 80.3076 - z * 60.6137 (u = sim x, v = -sim y)",
           "openings": out}, open(os.path.join(LV, "guide", "declared_openings.json"), "w"), indent=1)
for o in out:
    print(o["id"], o["w_m"], o["h_m"], o["faces_deg"], o["centre_px"], "faces camera" if o["faces_camera"] else "FACES AWAY")
