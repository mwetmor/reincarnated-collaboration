#!/usr/bin/env python3
"""R11 under the RULED porch region (R-C9-182), exactly as pre-registered in calibration.md § 19 (commit 904ac6dc0):
region = the porch-width strip from hall_porch's OUTER FACE back to the hall's RIDGE LINE; body = the rest of the hall.
  p6prime_r11.py   -> results/p6prime_r11_r182.json"""
import math
import sys

import numpy as np
from matplotlib.path import Path

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p6prime as PP
import p6_phase1 as Q


def region(L):
    M = {m["id"]: m for m in L["models"]}
    fp = np.array(M["hall_porch"]["footprint"], float)
    c = np.array(M["longhall"]["pos"], float)
    t = math.radians(float(M["longhall"]["godot_rot_y_deg"]))
    ax = np.array([math.cos(t), -math.sin(t)])                 # the slot's local x (the long axis) in sim (x, y)
    # outer face = the footprint edge farthest from the hall centre
    edges = [(fp[i], fp[(i + 1) % len(fp)]) for i in range(len(fp))]
    def dist_line(p):
        return abs((p - c)[0] * ax[1] - (p - c)[1] * ax[0])     # distance of p from the ridge line
    P1, P2 = max(edges, key=lambda e: dist_line((e[0] + e[1]) / 2))
    foot = lambda p: c + ax * float(np.dot(p - c, ax))
    poly = np.array([P1, P2, foot(P2), foot(P1)])
    nrm = (P1 - foot(P1)) / max(np.linalg.norm(P1 - foot(P1)), 1e-9)   # unit, ridge -> outer face
    return poly, P1, P2, nrm, M


def reading(V, inside, z0):
    h_p = float(V[inside, 2].max()) - z0
    h_b = float(V[~inside, 2].max()) - z0
    return {"porch_h": round(h_p, 4), "body_h": round(h_b, 4), "margin_m": round(h_p - h_b, 4), "pass": bool(h_p > h_b + 0.5)}


if __name__ == "__main__":
    L = jload(Q.LV / "layout_v7c.json")
    poly, P1, P2, nrm, M = region(L)
    m = M["longhall"]
    ins = PP._instances(m)[0]
    V, _ = PP.placed_vertices(m, ins, {})
    z0 = float(m["z"])
    inside = Path(poly).contains_points(V[:, :2])
    ruled = reading(V, inside, z0)
    # constructed RED: in-region mesh clipped to <= body + 0.5
    Vr = V.copy()
    cap = z0 + (float(V[~inside, 2].max()) - z0) + 0.5        # unrounded body height
    Vr[inside, 2] = np.minimum(Vr[inside, 2], cap)
    red = reading(Vr, inside, z0)
    # non-binding: the registered 1.287 m footprint
    fp_in = Path(np.array(M["hall_porch"]["footprint"], float)).contains_points(V[:, :2])
    reg = reading(V, fp_in, z0)
    # the cover clause: where the tall part sits
    tall = (V[:, 2] - z0) > ruled["body_h"] + 0.5
    face_dir = (P2 - P1) / np.linalg.norm(P2 - P1)
    behind = [float(np.dot(P1 - p[:2], nrm)) for p in V[tall]]          # metres behind the outer face (into the hall)
    along = [float(np.dot(p[:2] - P1, face_dir)) for p in V[tall]]
    res = {"_what": "R11 under the ruled porch region (R-C9-182; pre-registered calibration.md § 19, 904ac6dc0)",
           "region_poly_sim_xy": poly.round(4).tolist(), "outer_face": [P1.round(4).tolist(), P2.round(4).tolist()],
           "region_depth_m": round(float(np.linalg.norm(P1 - (poly[3]))), 3), "porch_width_m": round(float(np.linalg.norm(P2 - P1)), 3),
           "verts_in_region": int(inside.sum()), "verts_body": int((~inside).sum()),
           "ruled_v7c": ruled, "constructed_red_clipped": red,
           "registered_footprint_non_binding": dict(reg, verts=int(fp_in.sum())),
           "cover_clause": {"tall_verts": int(tall.sum()), "tall_threshold_m": round(ruled["body_h"] + 0.5, 3),
                            "tall_part_behind_outer_face_m": [round(min(behind), 2), round(max(behind), 2)] if behind else None,
                            "tall_part_along_porch_width_m": [round(min(along), 2), round(max(along), 2)] if along else None,
                            "porch_height_at_the_door_m": reg["porch_h"],
                            "porch_depth_m": M["hall_porch"]["size_m"]["d_local_z"]}}
    dump(res, str(PH / "results/p6prime_r11_r182.json"))
    print(json.dumps({k: v for k, v in res.items() if k != "region_poly_sim_xy"}, indent=1))
