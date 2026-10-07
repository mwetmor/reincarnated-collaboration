#!/usr/bin/env python3
"""R-C9-191: PH's INDEPENDENT verification of LV's sea-cave walkability (fid/lv/tools/lv_walkability.py, commit 52e099d05),
plus a constructed RED that must FAIL.

Independence: PH does not reuse LV's analyse(). It reads LV's RAW Godot survey (fid/lv/walk/walk_check.json: down-ray hits,
slopes, body-in-collider flags, sideways free runs, the driven track) -- the colliders are the level's own -- and re-derives:
  (a) the step height from first principles and from the knight's own script (knight.gd: CapsuleShape3D r = 0.35 x
      figure scale; one plain move_and_slide(); no floor_max_angle / step-up code -> Godot's default 45 deg):
      a capsule's lower hemisphere meets an edge of height h with a contact normal at acos((r - h) / r) from up; it is a
      FLOOR (mountable) only while that angle <= floor_max_angle -> h <= r (1 - cos 45 deg) = 0.1025 m;
  (b) the segments from the LAYOUT's own route polygons (flight, landing, shelf; cave = the cave frame's mouth box), not
      LV's labels -- the stair = the flight polygon plus the nosing ramp's foot, one tread (route.spec.tread) past it
      (first pass without it: 6 samples, t 9.79-10.04 < t_foot + tread, read as "shelf at 33.5 deg"; they stand on the
      ramp's foot); slope limits: stair <= 35 deg, everything else <= 10 deg;
  (c) continuity, risers, widths (contiguous walkable run across each section, capped by the free run to a collider),
      headroom and the drive, each with PH's own code;
  (d) the route's design numbers analytically: riser x count = the shelf-to-landing drop; atan(riser / tread) = pitch.
RED (constructed on the same raw survey): (1) a 0.6 m riser on the shelf (every centreline sample past the shelf's
midpoint raised 0.6 m); (2) a 1 m gap in the shelf (20 centreline samples' floor removed). Both are run through PH's
analysis AND through LV's own analyse() -- both must FAIL.
  walk_verify.py  -> results/walk_verify_r191.json"""
import copy
import importlib.util
import math
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

LVD = FID / "lv"
WALK = LVD / "walk"
DS = 0.05


def pip(p, poly):
    x, y = p
    inside = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            inside = not inside
    return inside


def step_height(knight):
    r = float(knight["capsule_radius_m"])
    a = math.radians(float(knight["floor_max_angle_deg"]))
    return r * (1 - math.cos(a)), {"r_m": r, "floor_max_angle_deg": round(math.degrees(a), 3), "derived_m": round(r * (1 - math.cos(a)), 4),
                                   "lv_reported_m": round(knight["step_height_m"], 4)}


def analyse_ph(L, spec, W, h_step):
    R = L["route"]
    P = R["polygons_uv"]
    fc = R["frames"]["cave"]
    sp = R["spec"]
    S = W["survey"]
    n_c = spec["sections"][0]["i0"] if spec["sections"] else len(spec["samples"])

    fs = R["frames"]["stair"]

    def seg(p):
        if pip(p, P["flight"]):
            return "stair"
        # the nosing RAMP (the walk surface) runs one tread past the flight polygon's foot: route.spec.tread
        dx, dy = p[0] - fs["origin_uv"][0], p[1] - fs["origin_uv"][1]
        t = dx * fs["along_uv"][0] + dy * fs["along_uv"][1]
        s_ = dx * fs["along_uv"][1] - dy * fs["along_uv"][0]
        if fs["t_foot"] <= t <= fs["t_foot"] + sp["tread"] and 0.0 <= s_ <= fs["width_m"]:
            return "stair"
        if pip(p, P["landing"]):
            return "landing"
        o, a = fc["origin_uv"], fc["along_uv"]
        dx, dy = p[0] - o[0], p[1] - o[1]
        t, s = dx * a[0] + dy * a[1], dx * a[1] - dy * a[0]
        if abs(t) <= sp["mouth_w"] / 2 + sp["cheek_w"] and sp["floor_back_s"] <= s <= sp["mouth_s"]:
            return "cave"
        if pip(p, P["shelf"]):
            return "shelf"
        return "clifftop"
    lim = {"stair": 35.0}
    breaks, segs = [], {}
    for i in range(n_c):
        r = S[i]
        g = seg(spec["samples"][i])
        d = segs.setdefault(g, {"n": 0, "max_slope": 0.0, "max_dz": 0.0})
        d["n"] += 1
        if not r["hit"]:
            breaks.append((i, g, "no floor"))
            continue
        if r["body_blocked"]:
            breaks.append((i, g, "inside a collider"))
        d["max_slope"] = max(d["max_slope"], r["slope_deg"])
        if r["slope_deg"] > lim.get(g, 10.0) + 1e-6:
            breaks.append((i, g, "slope %.1f" % r["slope_deg"]))
        if i + 1 < n_c and S[i + 1]["hit"]:
            dz = abs(S[i + 1]["z"] - r["z"])
            d["max_dz"] = max(d["max_dz"], dz)
            if dz > h_step:
                breaks.append((i, g, "riser %.3f" % dz))
    side = {s["id"]: s for s in W["sections"]}
    widths = {}
    for sec in spec["sections"]:
        recs = S[sec["i0"]: sec["i0"] + sec["n"]]
        c = max(0, min(sec["n"] - 1, int(round((sec["centre_a"] - sec["a0"]) / DS))))
        ok = lambda j: recs[j]["hit"] and not recs[j]["body_blocked"] and recs[j]["slope_deg"] <= (35.0 if sec["kind"] == "stair" else 10.0) + 1e-6
        lo = hi = c
        run = 0.0
        if ok(c):
            while lo > 0 and ok(lo - 1) and abs(recs[lo - 1]["z"] - recs[lo]["z"]) <= h_step:
                lo -= 1
            while hi < len(recs) - 1 and ok(hi + 1) and abs(recs[hi + 1]["z"] - recs[hi]["z"]) <= h_step:
                hi += 1
            run = (hi - lo + 1) * DS
        sd = side.get(sec["id"], {})
        free = min(sd.get("free_neg_0.4", 99) + sd.get("free_pos_0.4", 99), sd.get("free_neg_1.2", 99) + sd.get("free_pos_1.2", 99))
        hr = min([r["headroom_m"] for r in recs[lo:hi + 1] if r["hit"]] or [0.0])
        widths[sec["id"]] = {"kind": sec["kind"], "clear_m": round(min(run, free), 2), "headroom_m": round(hr, 2)}
    tr = W["track"]
    st = [w["clear_m"] for w in widths.values() if w["kind"] == "stair"]
    sh = [w["clear_m"] for w in widths.values() if w["kind"] == "shelf"]
    mouth = widths.get("cave_mouth", {})
    bars = {"continuous": len(breaks) == 0,
            "stair_slope_le_35": segs.get("stair", {}).get("max_slope", 99) <= 35.0,
            "shelf_slope_le_10": segs.get("shelf", {}).get("max_slope", 99) <= 10.0,
            "riser_le_step": max(d["max_dz"] for d in segs.values()) <= h_step,
            "stair_width_ge_5": bool(st) and min(st) >= 5.0, "shelf_width_ge_6": bool(sh) and min(sh) >= 6.0,
            "mouth_headroom_ge_6p9": mouth.get("headroom_m", 0) >= 6.9,
            "drive_reached": bool(W["drive"]["reached_last_waypoint"]) and sum(1 for q in tr if not q[3]) == 0}
    return {"segments": {k: {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in segs.items()},
            "breaks": breaks[:20], "n_breaks": len(breaks), "stair_min_clear_m": min(st) if st else None,
            "shelf_min_clear_m": min(sh) if sh else None, "mouth": mouth, "bars": bars, "pass": all(bars.values())}


def lv_analyse(L, spec, W):
    sp_ = importlib.util.spec_from_file_location("lv_walk_readonly", LVD / "tools/lv_walkability.py")
    m = importlib.util.module_from_spec(sp_)
    sp_.loader.exec_module(m)
    spec2, meta = m.build_spec(L)
    return m.analyse(L, spec2, meta, W)


def constructed(L, spec, W):
    R = L["route"]
    n_c = spec["sections"][0]["i0"]
    shelf_idx = [i for i in range(n_c) if pip(spec["samples"][i], R["polygons_uv"]["shelf"])
                 and not pip(spec["samples"][i], R["polygons_uv"]["flight"])]
    mid = shelf_idx[len(shelf_idx) // 2]
    riser = copy.deepcopy(W)
    for i in range(mid, n_c):                         # everything after the shelf's midpoint 0.6 m higher: one 0.6 m riser
        if riser["survey"][i]["hit"]:
            riser["survey"][i]["z"] += 0.6
    gap = copy.deepcopy(W)
    for i in range(mid, min(mid + 20, n_c)):          # 20 samples x 0.05 m = a 1 m gap in the shelf floor
        gap["survey"][i]["hit"] = False
    return {"riser_0p6m": riser, "gap_1m": gap}, {"shelf_mid_sample": mid, "shelf_samples": len(shelf_idx)}


def design_numbers(L):
    R = L["route"]
    rz, n, tread = R["riser_m"], R["spec"]["risers"], R["spec"]["tread"]
    drop = 0.0 - R["spec"]["shelf_z"]
    return {"riser_x_count_m": round(rz * n, 3), "shelf_to_landing_drop_m": drop, "agree": abs(rz * n - drop) <= 0.01,
            "atan_riser_over_tread_deg": round(math.degrees(math.atan2(rz, tread)), 2), "stair_pitch_deg": R["stair_pitch_deg"],
            "pitch_agree": abs(math.degrees(math.atan2(rz, tread)) - R["stair_pitch_deg"]) <= 0.05,
            "visual_riser_vs_step_m": [rz, "the 0.179 m visual riser is above the 0.1025 m step: the walk surface is the nosing RAMP (33.48 deg <= 35), the treads are under it"]}


if __name__ == "__main__":
    L = jload(LVD / "art/layout_bv2art.json")
    spec = jload(WALK / "walk_spec.json")
    W = jload(WALK / "walk_check.json")
    h, hd = step_height(W["knight"])
    ph = analyse_ph(L, spec, W, h)
    lv = lv_analyse(L, spec, W)
    reds, rmeta = constructed(L, spec, W)
    red_rows = {}
    for k, Wr in reds.items():
        a = analyse_ph(L, spec, Wr, h)
        b = lv_analyse(L, spec, Wr)
        red_rows[k] = {"ph": {"pass": a["pass"], "failed_bars": [x for x, v in a["bars"].items() if not v], "first_breaks": a["breaks"][:3]},
                       "lv_tool": {"verdict": b["verdict"], "failed_bars": [x["bar"] for x in b["bars"] if not x["pass"]]}}
    res = {"_what": "R-C9-191: PH's independent verification of LV's sea-cave walkability + constructed REDs",
           "inputs": {"walk_check_sha256": sha256(WALK / "walk_check.json"), "walk_spec_sha256": sha256(WALK / "walk_spec.json"),
                      "layout_bv2art_sha256": sha256(LVD / "art/layout_bv2art.json"), "lv_commit": "52e099d05"},
           "step_height": hd, "step_height_agrees": abs(hd["derived_m"] - hd["lv_reported_m"]) <= 1e-3,
           "knight_script_check": "knight.gd: CapsuleShape3D radius 0.35 x figure scale (lines 149-153, 808-812); one move_and_slide() "
                                  "(line 1145); no floor_max_angle / floor_block_on_wall / step-up code -> Godot's default 45 deg",
           "design_numbers": design_numbers(L), "ph_analysis": ph, "lv_tool_verdict": lv["verdict"],
           "constructed_reds": red_rows, "red_meta": rmeta}
    res["verified"] = ph["pass"] and lv["verdict"] == "PASS" and res["step_height_agrees"] and all(
        (not v["ph"]["pass"]) and v["lv_tool"]["verdict"] == "FAIL" for v in red_rows.values())
    dump(res, str(PH / "results/walk_verify_r191.json"))
    print(json.dumps({k: res[k] for k in ("step_height", "step_height_agrees", "design_numbers", "lv_tool_verdict", "constructed_reds", "verified")}, indent=1, default=str))
    print("PH:", ph["bars"], ph["stair_min_clear_m"], ph["shelf_min_clear_m"], ph["mouth"], ph["segments"])
