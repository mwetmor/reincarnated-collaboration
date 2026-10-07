#!/usr/bin/env python3
"""BV2F LV 0.2: prove the frame transform's SIGN (python3 fid/lv/test_frame.py; exit 0 = all PASS).

T1  v1's analytic camera basis equals the LIVE painting-camera basis recorded independently in
    barrow_heather.gd:43-45 (CAM_RIGHT / CAM_UP / CAM_FWD) -- the camera we project through is v1's.
T2  two-anchor (and four-anchor) screen test at v1's play camera: p02 (barrow door) screen-UP of the start,
    p01 (wreck) screen-LEFT, p04 (hall) screen-RIGHT, p03 (sea cave) screen-DOWN -- as in sketch A.
T3  exactness: for every anchor and a grid of sim points incl. height, v1camera(world(sim)) equals the
    layout's yaw-0 law to < 1e-6 px -- i.e. the play camera sees exactly the composition layout_v2 was
    authored for (sketch A's frame).
T4  negative controls: yaw -47 (wrong sign) and yaw 0 (R-C9-159, site unrotated) must FAIL T2/T3.
T5  round trip world_to_sim(sim_to_world(p)) = p; rot_y maps a sim-yawed model's +x to the rotated +x.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import frame as F  # noqa: E402

BV2 = os.path.normpath(os.path.join(HERE, "..", ".."))
HEATHER = os.path.normpath(os.path.join(BV2, "..", "barrow_full", "godot", "scripts", "barrow_heather.gd"))
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
A = {a["id"]: (a["x"], a["y"]) for a in L["anchors"]["points"]}
out = {"checks": [], "anchors_screen_px": {}}
ok_all = True


def check(name, ok, **kw):
    global ok_all
    ok_all &= bool(ok)
    out["checks"].append(dict(test=name, PASS=bool(ok), **kw))
    print(("PASS " if ok else "FAIL ") + name + ("  " + json.dumps(kw) if kw else ""))


def vec(line):
    import re
    return tuple(float(t) for t in re.findall(r"-?\d+\.\d+", line.split("Vector3", 1)[1]))


# T1
cam = {}
for ln in open(HEATHER):
    for k in ("CAM_RIGHT", "CAM_UP", "CAM_FWD"):
        if ln.startswith(f"const {k} "):
            cam[k] = vec(ln)
r, u, f = F.v1_camera_basis()
d = max(max(abs(a - b) for a, b in zip(r, cam["CAM_RIGHT"])), max(abs(a - b) for a, b in zip(u, cam["CAM_UP"])),
        max(abs(a - b) for a, b in zip(f, cam["CAM_FWD"])))
check("T1 analytic v1 camera basis == barrow_heather.gd live basis", d < 1e-6, max_abs_diff=d,
      right=[round(t, 6) for t in r], up=[round(t, 6) for t in u], fwd=[round(t, 6) for t in f])


def screen(pid, yaw):
    x, y = A[pid]
    return F.project_v1(F.sim_to_world(x, y, 0.0, yaw_deg=yaw))


def two_anchor(yaw):
    s = {k: screen(k, yaw) for k in A}
    ang = lambda p: math.degrees(math.atan2(-s[p][1], s[p][0]))   # screen angle CCW from screen-right
    res = {"p02_up": s["p02"][1] < 0 and abs(s["p02"][0]) < abs(s["p02"][1]),
           "p01_left": s["p01"][0] < 0 and abs(s["p01"][1]) < abs(s["p01"][0]),
           "p04_right": s["p04"][0] > 0 and abs(s["p04"][1]) < abs(s["p04"][0]),
           "p03_down": s["p03"][1] > 0 and abs(s["p03"][0]) < abs(s["p03"][1])}
    return res, s, {k: round(ang(k), 2) for k in s}


def exact(yaw):
    worst = 0.0
    pts = list(A.values()) + [(x, y) for x in range(-60, 61, 15) for y in range(-60, 61, 15)]
    for (x, y) in pts:
        for z in (0.0, -7.5, 6.5):
            a = F.project_v1(F.sim_to_world(x, y, z, yaw_deg=yaw))
            b = F.project_yaw0_layout(x, y, z)
            worst = max(worst, abs(a[0] - b[0]), abs(a[1] - b[1]))
    return worst


# T2 + T3 (the fix)
res, s, ang = two_anchor(F.FRAME_YAW_DEG)
out["anchors_screen_px"] = {k: [round(v[0], 2), round(v[1], 2)] for k, v in s.items()}
out["anchors_screen_angle_deg_ccw_from_right"] = ang
check("T2 p02 screen-UP of the start and p01 screen-LEFT (yaw +47)", res["p02_up"] and res["p01_left"],
      p02_px=out["anchors_screen_px"]["p02"], p01_px=out["anchors_screen_px"]["p01"])
check("T2b p04 screen-RIGHT and p03 screen-DOWN (yaw +47)", res["p04_right"] and res["p03_down"],
      p04_px=out["anchors_screen_px"]["p04"], p03_px=out["anchors_screen_px"]["p03"])
w = exact(F.FRAME_YAW_DEG)
check("T3 v1camera(R_y(+47).sim) == layout yaw-0 law (anchors + 81-pt grid x 3 heights)", w < 1e-6, worst_px=w)

# T4 negative controls
for yaw, label in ((-F.PL_YAW_DEG, "wrong sign, yaw -47"), (0.0, "R-C9-159, site unrotated")):
    r4, s4, a4 = two_anchor(yaw)
    w4 = exact(yaw)
    failed = (not all(r4.values())) or w4 > 1.0
    check(f"T4 negative control ({label}) is REJECTED", failed, two_anchor=r4, worst_px=round(w4, 1),
          screen_angle_deg=a4)

# T5
worst = 0.0
for (x, y) in A.values():
    X = F.sim_to_world(x, y, 1.25)
    b = F.world_to_sim(*X)
    worst = max(worst, abs(b[0] - x), abs(b[1] - y), abs(b[2] - 1.25))
# a model yawed by rot_y in sim: its local +x points (cos t, -sin t) in (X, Z) = sim (cos t, -sin t) in (x, y)
t = math.radians(-132.99)                                  # longhall godot_rot_y_deg (sim)
sim_dir = (math.cos(t), -math.sin(t))
w_dir = F.sim_to_world(*sim_dir)
tw = math.radians(F.rot_y_to_world(-132.99))
d5 = math.hypot(w_dir[0] - math.cos(tw), w_dir[2] + math.sin(tw))
check("T5 round trip + model yaw (rot_y_world = rot_y_sim + 47)", worst < 1e-12 and d5 < 1e-12, roundtrip=worst, yaw_dir_err=d5)

out["transform"] = {"world": "R_y(+47 deg) . (x, z, y)  [Godot: Basis(Vector3.UP, deg_to_rad(47)) * Vector3(x, z, y)]",
                    "rot_y_world": "rot_y_sim + 47", "yaw_deg": F.FRAME_YAW_DEG}
out["pass"] = ok_all
os.makedirs(os.path.join(HERE, "frame_proof"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "frame_proof", "test_frame_output.json"), "w"), indent=1)
print("ALL PASS" if ok_all else "FAILURES")
sys.exit(0 if ok_all else 1)
