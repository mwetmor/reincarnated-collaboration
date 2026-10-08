#!/usr/bin/env python3
"""BV2F LV (R-C9-188/189): the mechanical WALKABILITY check of the sea-cave route -- inside the cave, over the shelf, up
the stair, onto the clifftop -- against the art level's COLLIDERS, with v1's own knight.

    python3 fid/lv/tools/lv_walkability.py            (writes the spec, runs the Godot instrument, writes the table)
    python3 fid/lv/tools/lv_walkability.py --no-run   (re-reads fid/lv/walk/walk_check.json)

The instrument is barrow_full/godot/tools/bv2f/walk_check.gd (heavy lock, disk gate 21 GiB). It reports, off the
running level: the down-ray floor height + slope at every sample, whether a body's middle there sits inside a collider,
the headroom, the free run sideways at knee and chest height across each section, and v1's knight (knight.gd,
unmodified) DRIVEN through the waypoints by drive_dir, as barrow_full.gd's own frame-cost walk drives him.

BARS (Matt R-C9-188, the conductor's check list):
  continuous  every centreline sample (0.05 m apart) is a walkable floor: hit, body not inside a collider, and the
              height change to the next sample <= v1's STEP HEIGHT -- i.e. no riser he cannot take, anywhere
  slope       stair <= 35 deg; shelf <= 10 deg (cave floor, landing, clifftop held to the shelf's 10)
  step height v1's knight: CharacterBody3D capsule r 0.35 m, h 1.8 m (scripts/knight.gd _ready), plain move_and_slide(),
              18 m/s2 gravity, NO step-up code, floor_max_angle not set (Godot default 45 deg): an edge is mounted only
              while the contact normal is within 45 deg of up -> h <= r (1 - cos 45) = 0.103 m (read off the running node)
  widths      clear width >= 5 m on the stair, >= 6 m on the shelf (the contiguous walkable run across each section,
              capped by the free run to the nearest collider at knee and chest height)
  the drive   his capsule reaches the clifftop from inside the cave
"""
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
C9 = os.path.normpath(os.path.join(LV, "..", "..", ".."))
BF = os.path.join(C9, "barrow_full", "godot")
LOCK = os.path.join(HERE, "lv_guard_lock.py")          # R-C9-226: heavy lock + wall-clock timeout + quit on a script error
GODOT = os.environ.get("GODOT", "/Applications/Godot.app/Contents/MacOS/Godot")
OUT = os.path.join(LV, "walk")
DS = 0.05
SLOPE = {"cave": 10.0, "shelf": 10.0, "stair": 35.0, "landing": 10.0, "clifftop": 10.0}
WIDTH = {"stair": 5.0, "shelf": 5.0}


def point_in_poly(p, poly):
    x, y = p
    inside = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            inside = not inside
    return inside


def frame(f):
    o, d = f["origin_uv"], f["along_uv"]
    n = (d[1], -d[0])
    return lambda t, s: (o[0] + d[0] * t + n[0] * s, o[1] + d[1] * t + n[1] * s)


def build_spec(L):
    """R-C9-226 route: out of the cave (its axis inland), over the iced landing past the jamb, up the stair cleft INLAND (toward
    -s) to its top pad and the clifftop. Every centreline sample is labelled by the leg it lies on."""
    R = L["route"]
    sp = R["spec"]
    F = R["frame"]
    o, d = F["origin_uv"], F["along_uv"]
    n = (d[1], -d[0])
    fr = lambda t, s_: (o[0] + d[0] * t + n[0] * s_, o[1] + d[1] * t + n[1] * s_)
    P = {k: tuple(v) for k, v in R["points_uv"].items()}
    t0, t1 = F["stair_t"]
    W = F["width_m"]
    s_foot, s_top, s_land = F["s_foot"], F["s_top"], F["s_land"]
    tm = (t0 + t1) / 2
    ax = R["cave_axis_ts"]
    ct, cf = sp["cave_t"], R["carve"]["cove"]["s_back"]
    legs = [("cave", P["cave_back"], P["cave_mouth"]), ("shelf", P["cave_mouth"], P["shelf_mid"]), ("shelf", P["shelf_mid"], P["bottom_landing"]),
            ("shelf", P["bottom_landing"], fr(tm, s_foot + sp["tread"])), ("stair", fr(tm, s_foot + sp["tread"]), P["stair_top"]),
            ("landing", P["stair_top"], P["landing"]), ("landing", P["landing"], fr(tm, s_land)), ("clifftop", fr(tm, s_land), P["clifftop"])]
    samples, seg_of = [], []
    for nm, a_, b_ in legs:
        k = max(1, int(round(math.dist(a_, b_) / DS)))
        for i in range(k):
            f = i / k
            samples.append([round(a_[0] + (b_[0] - a_[0]) * f, 4), round(a_[1] + (b_[1] - a_[1]) * f, 4)])
            seg_of.append(nm)
    samples.append([round(P["clifftop"][0], 4), round(P["clifftop"][1], 4)])
    seg_of.append("clifftop")
    wp = [P["cave_back"], P["cave_mouth"], P["shelf_mid"], P["bottom_landing"], fr(tm, s_foot + sp["tread"]), P["stair_top"], P["landing"], P["clifftop"]]
    n_centre = len(samples)
    sections = []
    dvec, nvec = (d[0], d[1]), (n[0], n[1])

    def add_section(sid, kind, centre, a0, a1, axis, origin):
        idx0 = len(samples)
        k = int(round((a1 - a0) / DS))
        for i in range(k + 1):
            x = a0 + i * DS
            samples.append([round(origin[0] + axis[0] * x, 4), round(origin[1] + axis[1] * x, 4)])
        sections.append({"id": sid, "kind": kind, "centre": [round(centre[0], 4), round(centre[1], 4)], "across": [axis[0], axis[1]],
                         "i0": idx0, "n": k + 1, "a0": a0, "centre_a": round(((centre[0] - origin[0]) * axis[0] + (centre[1] - origin[1]) * axis[1]), 4)})
    # the stair: across the band (along t), every 0.5 m of its run
    s_ = s_foot - 0.25
    j = 0
    while s_ >= s_top + 0.2:
        add_section("stair_%02d" % j, "stair", fr(tm, s_), t0 - 1.5 - tm, t1 + 1.5 - tm, dvec, fr(tm, s_))
        s_ -= 0.5
        j += 1
    # the landing: across it (along s), from the cave's mouth past the jamb to the stair's foot
    j = 0
    for t_ in (ct + 3.4, ct + 3.9, t0 - 0.6, t0 - 0.1, t0 + 0.6, tm, t1 - 0.6):
        c_ = fr(t_, -2.4 if t_ < t0 else s_foot + 2.4)
        add_section("shelf_%02d" % j, "shelf", c_, -9.5, 2.5, nvec, fr(t_, 0.0))
        j += 1
    mc = fr(ct + ax[0] * 1.0, cf + ax[1] * 1.0)
    add_section("cave_mouth", "cave", mc, -sp["mouth_w"] / 2 - 3.0, sp["mouth_w"] / 2 + 3.0, dvec, mc)
    xs = [q[0] for q in samples[:n_centre]]
    ys = [q[1] for q in samples[:n_centre]]
    w_m, h_m = max(xs) - min(xs) + 8.0, max(ys) - min(ys) + 8.0
    pa, pb = P["cave_mouth"], P["landing"]
    spec = {"samples": samples, "sections": sections, "waypoints": [list(q) for q in wp], "waypoint_radius_m": 0.5, "drive_timeout_s": 90.0,
            "stills": {"play_aim": [round((pa[0] + pb[0]) / 2, 3), round((pa[1] + pb[1]) / 2, 3), -1.0], "him_uv": list(fr(tm, (s_foot + s_top) / 2)),
                       "topdown": [round((max(xs) + min(xs)) / 2, 3), round((max(ys) + min(ys)) / 2, 3), round(max(h_m, w_m * 1400 / 2000), 2), 2000, 1400]}}
    meta = {"n_centre": n_centre, "seg_of": seg_of, "waypoint_names": ["cave_back", "cave_mouth", "shelf_mid", "bottom_landing", "stair_foot", "stair_top", "landing", "clifftop"]}
    return spec, meta


def run_godot(spec):
    os.makedirs(OUT, exist_ok=True)
    sp = os.path.join(OUT, "walk_spec.json")
    json.dump(spec, open(sp, "w"))
    free = shutil.disk_usage("/System/Volumes/Data").free / 2 ** 30
    if free < 21:
        sys.exit("[walk] HALT: %.1f GiB free (< 21)" % free)
    log = open(os.path.join(OUT, "walk_check.log"), "w")
    env = dict(os.environ, BV2F_VARIANT="art")
    rc = subprocess.run(["python3", LOCK, "C-9", "--", GODOT, "--path", BF, "--resolution", "640x360", "--script", "tools/bv2f/walk_check.gd",
                         "--", "--out", OUT, "--spec", sp], cwd=BF, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        sys.exit("[walk] Godot rc=%d (walk_check.log)" % rc)


def analyse(L, spec, meta, W_):
    K = W_["knight"]
    step_h = K["step_height_m"]
    S = W_["survey"]
    nC = meta["n_centre"]
    seg = meta["seg_of"]

    def walkable(r, lim):
        return r["hit"] and not r["body_blocked"] and r["slope_deg"] <= lim + 1e-6
    rows = {}
    breaks = []
    for i in range(nC):
        r = S[i]
        sg = seg[i]
        R_ = rows.setdefault(sg, {"samples": 0, "walkable": 0, "max_slope_deg": 0.0, "max_dz_m": 0.0, "z": [1e9, -1e9], "min_headroom_m": 99.0})
        R_["samples"] += 1
        ok = r["hit"] and not r["body_blocked"]
        if ok:
            R_["max_slope_deg"] = max(R_["max_slope_deg"], r["slope_deg"])
            R_["z"] = [min(R_["z"][0], r["z"]), max(R_["z"][1], r["z"])]
            R_["min_headroom_m"] = min(R_["min_headroom_m"], r["headroom_m"])
        if walkable(r, SLOPE[sg]):
            R_["walkable"] += 1
        else:
            breaks.append({"i": i, "segment": sg, "uv": r["uv"], "why": "no floor" if not r["hit"] else ("body inside a collider" if r["body_blocked"] else "slope %.1f > %.0f" % (r["slope_deg"], SLOPE[sg]))})
        if i + 1 < nC and r["hit"] and S[i + 1]["hit"]:
            dz = abs(S[i + 1]["z"] - r["z"])
            R_["max_dz_m"] = max(R_["max_dz_m"], dz)
            if dz > step_h:
                breaks.append({"i": i, "segment": sg, "uv": r["uv"], "why": "riser %.3f m > step height %.3f m" % (dz, step_h)})
    # widths
    secs = []
    side = {s["id"]: s for s in W_["sections"]}
    for sec in spec["sections"]:
        recs = S[sec["i0"]: sec["i0"] + sec["n"]]
        lim = SLOPE[sec["kind"]]
        ci = int(round((sec["centre_a"] - sec["a0"]) / DS))
        ci = max(0, min(sec["n"] - 1, ci))
        lo = hi = ci
        if walkable(recs[ci], lim):
            while lo - 1 >= 0 and walkable(recs[lo - 1], lim) and abs(recs[lo - 1]["z"] - recs[lo]["z"]) <= step_h:
                lo -= 1
            while hi + 1 < len(recs) and walkable(recs[hi + 1], lim) and abs(recs[hi + 1]["z"] - recs[hi]["z"]) <= step_h:
                hi += 1
            surf = (hi - lo + 1) * DS
        else:
            surf = 0.0
        sd = side.get(sec["id"], {})
        free = min(sd.get("free_neg_0.4", 8) + sd.get("free_pos_0.4", 8), sd.get("free_neg_1.2", 8) + sd.get("free_pos_1.2", 8))
        hr = min([r["headroom_m"] for r in recs[lo:hi + 1] if r["hit"]] or [0.0])
        secs.append({"id": sec["id"], "kind": sec["kind"], "surface_width_m": round(surf, 2), "free_between_colliders_m": round(free, 2),
                     "clear_width_m": round(min(surf, free), 2), "min_headroom_m": round(hr, 2)})
    D = W_["drive"]
    tr = W_["track"]
    off_floor = sum(1 for q in tr if not q[3])
    clift = spec["waypoints"][-1]
    res = {"knight": K, "segments": rows, "breaks": breaks, "sections": secs, "drive": {k: D[k] for k in ("reached_last_waypoint", "time_s", "frames", "stuck_3s", "end_uv", "end_z")},
           "drive_frames_off_floor": off_floor, "drive_z_range": [min(q[2] for q in tr), max(q[2] for q in tr)] if tr else None}
    st_secs = [s for s in secs if s["kind"] == "stair"]
    sh_secs = [s for s in secs if s["kind"] == "shelf"]
    mouth = [s for s in secs if s["id"] == "cave_mouth"][0]
    roofed = [S[i]["headroom_m"] for i in range(nC) if seg[i] == "cave" and S[i]["hit"] and S[i]["headroom_m"] < 14.9]
    lip_h = roofed[-1] if roofed else 0.0
    deep_h = roofed[0] if roofed else 0.0
    bars = [
        ("continuous walk surface, cave -> clifftop (every 0.05 m)", "%d of %d centreline samples walkable; %d breaks" % (sum(r["walkable"] for r in rows.values()), nC, len(breaks)), len(breaks) == 0),
        ("stair slope <= 35 deg", "%.2f deg (collider); treads %.2f deg" % (rows["stair"]["max_slope_deg"], L["route"]["stair_pitch_deg"]), rows["stair"]["max_slope_deg"] <= 35.0),
        ("iced landing (in the cove) slope <= 10 deg", "%.2f deg" % rows["shelf"]["max_slope_deg"], rows["shelf"]["max_slope_deg"] <= 10.0),
        ("no riser above v1's step height (%.3f m)" % step_h, "max %.3f m between samples 0.05 m apart (treads' visual riser %.3f m is under the ramp)" % (max(r["max_dz_m"] for r in rows.values()), L["route"]["riser_m"]),
         max(r["max_dz_m"] for r in rows.values()) <= step_h),
        ("stair clear width >= 5 m", "min %.2f m over %d sections" % (min(s["clear_width_m"] for s in st_secs), len(st_secs)), min(s["clear_width_m"] for s in st_secs) >= 5.0),
        ("iced landing clear width >= 5 m (cave mouth -> past the jamb -> stair foot)", "min %.2f m over %d sections" % (min(s["clear_width_m"] for s in sh_secs), len(sh_secs)), min(s["clear_width_m"] for s in sh_secs) >= 5.0),
        ("cave mouth clear height ~7 m", "%.2f m at the arch's lip (the first centreline sample under the roof); %.2f m deeper in; the floor %.2f m clear across 1 m inside" % (
            lip_h, deep_h, mouth["clear_width_m"]), lip_h >= 6.5),
        ("v1's knight driven from inside the cave to the clifftop", "reached %s in %.1f s (%d frames, %d off the floor); ends at uv (%.2f, %.2f) z %.2f" % (
            D["reached_last_waypoint"], D["time_s"], D["frames"], off_floor, D["end_uv"][0], D["end_uv"][1], D["end_z"]), bool(D["reached_last_waypoint"])),
    ]
    res["bars"] = [{"bar": b, "measured": m, "pass": p} for b, m, p in bars]
    res["verdict"] = "PASS" if all(p for _, _, p in bars) else "FAIL"
    return res


def write_md(res, L):
    K = res["knight"]
    lines = ["# Sea-cave route -- walkability (R-C9-188/189)", "",
             "Against the art level's **colliders** (terrain HeightMapShape3D, the stair's nosing ramp, the cave hood, the bounds), by "
             "`barrow_full/godot/tools/bv2f/walk_check.gd`, driven by `fid/lv/tools/lv_walkability.py`.", "",
             "**v1's character step height:** `scripts/knight.gd` is a CharacterBody3D capsule r %.2f m, h %.2f m, on plain `move_and_slide()` with "
             "18 m/s2 gravity and no step-up code; floor_max_angle %.0f deg (Godot's default, not set): an edge is mounted only while the contact "
             "normal is within that of up, so **step height = r (1 - cos %.0f deg) = %.3f m** (read off the running node)." % (
                 K["capsule_radius_m"], K["capsule_height_m"], K["floor_max_angle_deg"], K["floor_max_angle_deg"], K["step_height_m"]), "",
             "| bar | measured | |", "|---|---|---|"]
    for b in res["bars"]:
        lines.append("| %s | %s | %s |" % (b["bar"], b["measured"], "PASS" if b["pass"] else "**FAIL**"))
    lines += ["", "**Verdict: %s**" % res["verdict"], "", "| segment | samples | walkable | max slope | max dz / 0.05 m | z range | min headroom |", "|---|---|---|---|---|---|---|"]
    for k in ("cave", "shelf", "stair", "landing", "clifftop"):
        r = res["segments"][k]
        lines.append("| %s | %d | %d | %.2f deg | %.3f m | %.2f .. %.2f | %.2f m |" % (k, r["samples"], r["walkable"], r["max_slope_deg"], r["max_dz_m"], r["z"][0], r["z"][1], r["min_headroom_m"]))
    lines += ["", "Sections (clear width = walkable run across, capped by the free run to the nearest collider at 0.4 m and 1.2 m):", "",
              "| section | surface | free between colliders | clear | headroom |", "|---|---|---|---|---|"]
    for s in res["sections"]:
        lines.append("| %s | %.2f | %.2f | %.2f | %.2f |" % (s["id"], s["surface_width_m"], s["free_between_colliders_m"], s["clear_width_m"], s["min_headroom_m"]))
    if res["breaks"]:
        lines += ["", "Breaks:", ""] + ["- %s" % json.dumps(b) for b in res["breaks"][:40]]
    lines += ["", "Stills: `route_topdown.png` (straight down, north up) and `route_play.png` (v1's play camera) -- the magenta line is "
              "the knight's DRIVEN track (a check overlay, not in the guide); him on the stair for scale.", "",
              "Where it stands: %s" % L["route"]["sketch_A"]]
    open(os.path.join(OUT, "walkability.md"), "w").write("\n".join(lines) + "\n")


def main():
    L = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
    spec, meta = build_spec(L)
    if "--no-run" not in sys.argv:
        run_godot(spec)
    W_ = json.load(open(os.path.join(OUT, "walk_check.json")))
    res = analyse(L, spec, meta, W_)
    res["_what"] = "R-C9-188/189 walkability of the sea-cave route (lv_walkability.py)"
    json.dump(res, open(os.path.join(OUT, "walkability.json"), "w"), indent=1)
    write_md(res, L)
    for b in res["bars"]:
        print("  %-62s %-90s %s" % (b["bar"], b["measured"], "PASS" if b["pass"] else "FAIL"))
    print("[walk] %s" % res["verdict"])
    return 0 if res["verdict"] == "PASS" else 4


if __name__ == "__main__":
    sys.exit(main())
