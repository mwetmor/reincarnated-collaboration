#!/usr/bin/env python3
"""BV2F LV (R-C9-189): does a layout change reach the PAINT PILOT window? -- a geometric pre-check, before any render.

    python3 fid/lv/tools/lv_pilot_guard.py --before DIR      (DIR: the reference level.json, terrain_h.f32, classes.png)

The pilot is guide tiles r00-r02 x c00-c02 of the 5 x 5 grid: guide px x < 4096, y < 2560 (a 1536 x 1024 canvas on a
1280 x 768 stride). Everything the art level draws is projected into guide px by v1's camera (orthographic, pitch
52.95354, 100.6176 px per metre across): x = (u - u_left) * PPM, y = (v_top - v) * PPM * sin(pitch) - h * PPM * cos(pitch).

Compared between a reference copy of the level (--before DIR; terrain_h.f32 and classes.png are git-ignored, so the
reference is a copy taken before the change -- its shas are in the report) and the working one:
  * every heightfield cell whose height changed (old AND new height, the cell grown by one cell for the mesh between)
  * every class cell that changed
  * every procedural piece added or removed: stair blocks, curtains, the cave hood, cliff faces no longer placed
A change is SAFE when it projects at y >= 2584 (24 px below the pilot's bottom edge) or x >= 4120. The render is the
proof (the 9 tile shas, lv_pilot_tiles.py); this says in advance whether a render could move them, and where.
"""
import hashlib
import io
import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
C9 = os.path.normpath(os.path.join(LV, "..", "..", ".."))
ART_DATA = os.path.join(C9, "barrow_full", "godot", "data", "bv2f", "art")
PPM = 100.617553710938
P = math.radians(52.95354112560294)
Y_MIN, X_MIN = 2584.0, 4120.0


def ref_bytes(ref, path):
    return open(os.path.join(ref, os.path.basename(path)), "rb").read()


def main():
    ref = sys.argv[sys.argv.index("--before") + 1]
    old_lv = json.loads(ref_bytes(ref, os.path.join(ART_DATA, "level.json")))
    new_lv = json.load(open(os.path.join(ART_DATA, "level.json")))
    env = new_lv["frame"]["envelope"]
    u_left, v_top = env["u"][0], env["v"][1]
    assert old_lv["frame"]["envelope"] == env, "the window moved"

    def px(u, v, h):
        return (u - u_left) * PPM, (v_top - v) * PPM * math.sin(P) - h * PPM * math.cos(P)

    worst = {"y": 1e9}
    report = {"_what": __doc__.split("\n")[0], "ref_dir": ref, "ref_sha256": {f: hashlib.sha256(open(os.path.join(ref, f), "rb").read()).hexdigest() for f in ("level.json", "terrain_h.f32", "classes.png")}, "pilot_px": {"x_lt": 4096, "y_lt": 2560}, "safe_if": {"y_ge": Y_MIN, "or_x_ge": X_MIN}, "items": []}

    def judge(kind, pts):
        pp = [px(*q) for q in pts]
        unsafe = [q for q in pp if q[1] < Y_MIN and q[0] < X_MIN]
        ymin = min(q[1] for q in pp if q[0] < X_MIN) if any(q[0] < X_MIN for q in pp) else None
        report["items"].append({"what": kind, "n_points": len(pts), "min_y_px_inside_pilot_columns": None if ymin is None else round(float(ymin), 1),
                                "unsafe_points": len(unsafe)})
        if ymin is not None and ymin < worst["y"]:
            worst.update({"y": ymin, "what": kind})
        return len(unsafe)

    bad = 0
    # -- heightfield
    hf = new_lv["sim"]["heightfield"]
    H, W = hf["shape"]
    ppm = hf["px_per_m"]
    ex = hf["extent_sim_m"]
    Zo = np.frombuffer(ref_bytes(ref, os.path.join(ART_DATA, "terrain_h.f32")), "<f4").reshape(H, W)
    Zn = np.fromfile(os.path.join(ART_DATA, "terrain_h.f32"), "<f4").reshape(H, W)
    ch = np.argwhere(np.abs(Zo - Zn) > 1e-6)
    pts = []
    for j, i in ch:
        u = ex["x0"] + i / ppm
        v = -(ex["y0"] + j / ppm)
        for h in (float(Zo[j, i]), float(Zn[j, i])):
            pts.append((u, v + 1.0 / ppm, h))              # one cell north: the mesh between this cell and the next
    bad += judge("heightfield cells changed (%d)" % len(ch), pts) if pts else 0
    # -- classes
    cp = new_lv["sim"]["classes_png"]
    Co = np.asarray(Image.open(io.BytesIO(ref_bytes(ref, os.path.join(ART_DATA, "classes.png")))))
    Cn = np.asarray(Image.open(os.path.join(ART_DATA, "classes.png")))
    cc = np.argwhere(Co != Cn)
    cppm = cp["px_per_m"]
    pts = []
    for j, i in cc:
        u = ex["x0"] + (i + 0.5) / cppm
        v = -(ex["y0"] + (j + 0.5) / cppm)
        jj = min(int(j / cppm * ppm), H - 1)
        ii = min(int(i / cppm * ppm), W - 1)
        pts.append((u, v + 1.0 / cppm, float(max(Zo[jj, ii], Zn[jj, ii]))))
    bad += judge("class cells changed (%d)" % len(cc), pts) if pts else 0

    # -- procedural pieces: boxes (centre sim, along/across, yaw, z0..z1)
    def box_pts(c_sim, across, along, yaw_deg, z0, z1):
        a = math.radians(yaw_deg)
        fz = (math.sin(a), math.cos(a))                      # local +Z in sim (x, y)
        fx = (math.cos(a), -math.sin(a))                     # local +X in sim
        out = []
        for sx in (-0.5, 0.5):
            for sz in (-0.5, 0.5):
                x = c_sim[0] + fx[0] * across * sx + fz[0] * along * sz
                y = c_sim[1] + fx[1] * across * sx + fz[1] * along * sz
                for z in (z0, z1):
                    out.append((x, -y, z))
        return out

    def steps_pts(lv):
        out = []
        sz = lv["sim"]["sea_z"]
        for s in lv["sim"].get("stair_steps", []):
            out += box_pts(s["c_sim"], s["w"], s["tread"], s["yaw_deg"], sz - 0.5, s["z_top"])
        return out

    def curtain_pts(lv, oid):
        for o in lv["sim"]["openings"]:
            if o["id"] == oid:
                t = math.radians(o["faces_deg"])
                f = (math.sin(t), -math.cos(t))
                c = (o["centre_sim"][0] - f[0] * o["curtain_inset_m"], o["centre_sim"][1] - f[1] * o["curtain_inset_m"])
                return box_pts(c, o["w"], 0.3, math.degrees(math.atan2(f[0], f[1])), o["z0"], o["z0"] + o["h"])
        return []
    if json.dumps(old_lv["sim"].get("stair_steps")) != json.dumps(new_lv["sim"].get("stair_steps")):
        bad += judge("stair blocks REMOVED (the ref's)", steps_pts(old_lv))
        bad += judge("stair blocks ADDED", steps_pts(new_lv))
    oc, nc = curtain_pts(old_lv, "sea_cave_mouth"), curtain_pts(new_lv, "sea_cave_mouth")
    if oc != nc:
        bad += judge("sea cave curtain REMOVED (the ref's)", oc)
        bad += judge("sea cave curtain ADDED", nc)
    for b in new_lv["sim"].get("route", {}).get("hood", []):
        bad += judge("cave hood %s ADDED" % b["id"], box_pts(b["c_sim"], b["across"], b["along"], b["yaw_deg"], b["z0"], b["z1"]))

    # -- placed models present in one and not the other (by id), and any whose slot moved
    def insts(lv):
        out = {}
        for m in lv["sim"]["models"]:
            for k, ins in enumerate(m.get("instances") or []):
                out["%s/%d/%s" % (m["id"], k, ins.get("glb"))] = ins
            if not m.get("instances"):
                out[m["id"]] = m
        return out
    oi, ni = insts(old_lv), insts(new_lv)
    o_by = {}
    for key, ins in oi.items():
        o_by.setdefault(json.dumps(ins, sort_keys=True), key)
    n_set = {json.dumps(ins, sort_keys=True) for ins in ni.values()}
    o_set = set(o_by)
    for gone in sorted(o_set - n_set):
        ins = json.loads(gone)
        if ins.get("type") == "box":
            sm = ins["size_m"]
            bad += judge("model instance REMOVED %s" % o_by[gone], box_pts(ins["pos"], sm[0], sm[1], ins["godot_rot_y_deg"], ins["z"], ins["z"] + sm[2]))
        else:
            report["items"].append({"what": "REMOVED non-box %s" % o_by[gone], "unsafe_points": "not judged"})
    for new in sorted(n_set - o_set):
        ins = json.loads(new)
        if ins.get("type") == "box":
            sm = ins["size_m"]
            bad += judge("model instance ADDED/MOVED", box_pts(ins["pos"], sm[0], sm[1], ins["godot_rot_y_deg"], ins["z"], ins["z"] + sm[2]))
        else:
            report["items"].append({"what": "ADDED non-box", "unsafe_points": "not judged"})
    # -- hall panels ride the hall: judged by the hall's own slot (its whole box)
    if new_lv["sim"].get("hall_panels"):
        hall = next(m for m in new_lv["sim"]["models"] if m["id"] == "longhall")
        sm = hall["size_m"]
        bad += judge("hall panel (the whole hall slot)", box_pts(hall["pos"], sm["w_local_x"], sm["d_local_z"], hall["godot_rot_y_deg"], 0.0, sm["h"]))
    report["unsafe_points_total"] = bad
    report["worst"] = {"min_y_px": round(float(worst["y"]), 1), "what": worst.get("what")}
    report["verdict"] = "SAFE: no change projects into the pilot tiles (or their 24 px margin)" if bad == 0 else "UNSAFE: %d points project into the pilot" % bad
    json.dump(report, open(os.path.join(LV, "art", "pilot_guard.json"), "w"), indent=1)
    for it in report["items"]:
        print(" ", it)
    print("[pilot_guard] %s; worst %s" % (report["verdict"], report["worst"]))
    return 0 if bad == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
