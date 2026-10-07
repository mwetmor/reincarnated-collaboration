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
LOCK = os.path.join(os.path.dirname(C9), "C-7", "conductor_scripts", "heavy_lock.py")
GODOT = os.environ.get("GODOT", "/Applications/Godot.app/Contents/MacOS/Godot")
OUT = os.path.join(LV, "walk")
DS = 0.05
SLOPE = {"cave": 10.0, "shelf": 10.0, "stair": 35.0, "landing": 10.0, "clifftop": 10.0}
WIDTH = {"stair": 5.0, "shelf": 6.0}


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
    R = L["route"]
    sp = R["spec"]
    st = frame(R["frames"]["stair"])
    cv = frame(R["frames"]["cave"])
    fs = R["frames"]["stair"]
    t0, t_top = fs["t_landing"]
    t_foot, W = fs["t_foot"], fs["width_m"]
    hw, cw = sp["mouth_w"] / 2, sp["cheek_w"]
    shelf_s = (sp["mouth_s"] + sp["shelf_out_s"]) / 2
    # the centreline, segment by segment: (name, polyline)
    wp = [("cave", cv(0.0, sp["floor_back_s"] + 0.6)), ("cave", cv(0.0, sp["mouth_s"])), ("shelf", cv(0.0, shelf_s)),
          ("shelf", cv(-hw - cw - 1.0, shelf_s)), ("shelf", st(t_foot + 0.6, W / 2)), ("stair", st(t_top, W / 2)),
          ("landing", st((t0 + t_top) / 2, W / 2)), ("landing", st((t0 + t_top) / 2, 0.0)), ("clifftop", st((t0 + t_top) / 2, -2.5))]
    samples, seg_of = [], []
    for (na, a), (nb, b) in zip(wp[:-1], wp[1:]):
        n = max(1, int(round(math.dist(a, b) / DS)))
        for i in range(n):
            f = i / n
            samples.append([round(a[0] + (b[0] - a[0]) * f, 4), round(a[1] + (b[1] - a[1]) * f, 4)])
            seg_of.append(nb if nb == na else (na if f < 0.5 else nb))
    samples.append([round(wp[-1][1][0], 4), round(wp[-1][1][1], 4)])
    seg_of.append(wp[-1][0])
    # each centreline sample's segment is WHERE IT STANDS (not which leg of the waypoint list it is on)
    co, ca = R["frames"]["cave"]["origin_uv"], R["frames"]["cave"]["along_uv"]
    so, sa = fs["origin_uv"], fs["along_uv"]
    shelf_poly = R["polygons_uv"]["shelf"]

    def tsf(p, o, a):
        dx, dy = p[0] - o[0], p[1] - o[1]
        return dx * a[0] + dy * a[1], dx * a[1] - dy * a[0]

    def where(p):
        t, s = tsf(p, so, sa)
        if 0.0 <= s <= W and t_top <= t <= t_foot + sp["tread"]:
            return "stair"
        if 0.0 <= s <= W and t0 <= t < t_top:
            return "landing"
        tc, sc = tsf(p, co, ca)
        if abs(tc) <= hw + cw and sp["floor_back_s"] <= sc <= sp["mouth_s"]:
            return "cave"
        if point_in_poly(p, shelf_poly):
            return "shelf"
        return "clifftop"
    seg_of = [where(q) for q in samples]
    n_centre = len(samples)
    # cross-sections: the stair every 0.5 m (across: -1 .. W+1), the shelf every 0.5 m (across: s -1 .. shelf_out + 1),
    # the cave mouth (across the mouth, just inside)
    sections = []
    ns = (fs["along_uv"][1], -fs["along_uv"][0])
    nc = (R["frames"]["cave"]["along_uv"][1], -R["frames"]["cave"]["along_uv"][0])
    dc = R["frames"]["cave"]["along_uv"]

    def add_section(sid, kind, centre, a0, a1, axis, origin):
        idx0 = len(samples)
        k = int(round((a1 - a0) / DS))
        for i in range(k + 1):
            x = a0 + i * DS
            samples.append([round(origin[0] + axis[0] * x, 4), round(origin[1] + axis[1] * x, 4)])
        sections.append({"id": sid, "kind": kind, "centre": [round(centre[0], 4), round(centre[1], 4)], "across": [axis[0], axis[1]],
                         "i0": idx0, "n": k + 1, "a0": a0, "centre_a": round(((centre[0] - origin[0]) * axis[0] + (centre[1] - origin[1]) * axis[1]), 4)})
    t = t_top + 0.25
    j = 0
    while t <= t_foot - 0.2:
        add_section("stair_%02d" % j, "stair", st(t, W / 2), -1.0, W + 1.0, ns, st(t, 0.0))
        t += 0.5
        j += 1
    # the shelf: from the stair foot east to the mouth's west edge, sections across the cave frame's s
    t_c_foot = ((st(t_foot, W / 2)[0] - R["frames"]["cave"]["origin_uv"][0]) * dc[0] + (st(t_foot, W / 2)[1] - R["frames"]["cave"]["origin_uv"][1]) * dc[1])
    tc = t_c_foot + 0.6
    j = 0
    while tc <= -hw + 0.01:
        s_in = sp["mouth_s"] if tc >= -hw - cw - 0.01 else sp["shelf_in_s"]
        add_section("shelf_%02d" % j, "shelf", cv(tc, (s_in + sp["shelf_out_s"]) / 2), -1.0, sp["shelf_out_s"] + 1.0, nc, cv(tc, 0.0))
        tc += 0.5
        j += 1
    add_section("cave_mouth", "cave", cv(0.0, sp["mouth_s"] - 0.1), -hw - cw - 1.0, hw + cw + 1.0, dc, cv(0.0, sp["mouth_s"] - 0.1))
    pa = cv(0.0, sp["mouth_s"])
    pb = st(t0, W / 2)
    xs = [q[0] for q in samples[:n_centre]]
    ys = [q[1] for q in samples[:n_centre]]
    w_m, h_m = max(xs) - min(xs) + 8.0, max(ys) - min(ys) + 8.0
    spec = {"samples": samples, "sections": sections, "waypoints": [list(q) for _, q in wp], "waypoint_radius_m": 0.5, "drive_timeout_s": 90.0,
            "stills": {"play_aim": [round((pa[0] + pb[0]) / 2, 3), round((pa[1] + pb[1]) / 2, 3), -2.5], "him_uv": list(st((t_top + t_foot) / 2, W / 2)),
                       "topdown": [round((max(xs) + min(xs)) / 2, 3), round((max(ys) + min(ys)) / 2, 3), round(max(h_m, w_m * 1400 / 2000), 2), 2000, 1400]}}
    meta = {"n_centre": n_centre, "seg_of": seg_of, "waypoint_names": [n for n, _ in wp]}
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
    bars = [
        ("continuous walk surface, cave -> clifftop (every 0.05 m)", "%d of %d centreline samples walkable; %d breaks" % (sum(r["walkable"] for r in rows.values()), nC, len(breaks)), len(breaks) == 0),
        ("stair slope <= 35 deg", "%.2f deg (collider); treads %.2f deg" % (rows["stair"]["max_slope_deg"], L["route"]["stair_pitch_deg"]), rows["stair"]["max_slope_deg"] <= 35.0),
        ("shelf slope <= 10 deg", "%.2f deg" % rows["shelf"]["max_slope_deg"], rows["shelf"]["max_slope_deg"] <= 10.0),
        ("no riser above v1's step height (%.3f m)" % step_h, "max %.3f m between samples 0.05 m apart (treads' visual riser %.3f m is under the ramp)" % (max(r["max_dz_m"] for r in rows.values()), L["route"]["riser_m"]),
         max(r["max_dz_m"] for r in rows.values()) <= step_h),
        ("stair clear width >= 5 m", "min %.2f m over %d sections" % (min(s["clear_width_m"] for s in st_secs), len(st_secs)), min(s["clear_width_m"] for s in st_secs) >= 5.0),
        ("shelf clear width >= 6 m", "min %.2f m over %d sections" % (min(s["clear_width_m"] for s in sh_secs), len(sh_secs)), min(s["clear_width_m"] for s in sh_secs) >= 6.0),
        ("cave mouth clear height ~7 m", "%.2f m headroom; mouth %.2f m wide" % (mouth["min_headroom_m"], mouth["clear_width_m"]), mouth["min_headroom_m"] >= 6.9),
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
              "Where it stands: %s" % L["route"]["moved_from_sketch_A"]]
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
