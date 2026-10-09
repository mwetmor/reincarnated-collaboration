#!/usr/bin/env python3
"""BV2F LV (R-C9-331): the WRECK BEACH -> STONE CIRCLE route, checked the same way as the sea-cave route (lv_walkability.py):
walk_check.gd (heavy lock, guarded) surveys the colliders along the straight centreline (every 0.05 m) and DRIVES v1's knight
through the waypoints. PT's walk film found the bounds' thin double-wall spike at u ~ -20.5 (v -3.7 .. 18.1) fencing the beach
off the site, so walkers detoured across the frozen mere; this route crosses that line directly.

BARS: every centreline sample a floor (hit, body not inside a collider), slope <= 35 deg (the beach's rise), no riser above v1's
step height, and the knight DRIVEN from the beach to the ring reaches it without leaving the floor.

    python3 fid/lv/tools/lv_walk_beach.py   -> fid/lv/walk/beach_ring/{walk_spec.json, walk_check.json, beach_ring.json}
"""
import json
import math
import os
import sys

import lv_walkability as W

OUT = os.path.join(W.LV, "walk", "beach_ring")
# the wreck beach (its shingle slope NE of the hull, z ~ -1) -> across the old spike line -> up the slope -> the ring's W edge
WPS = [(-24.2, 8.6), (-20.0, 7.5), (-14.0, 4.5), (-9.0, 1.5), (-5.4, 0.2)]
SLOPE_MAX = 35.0


def main():
    samples = []
    for a_, b_ in zip(WPS, WPS[1:]):
        k = max(1, int(round(math.dist(a_, b_) / W.DS)))
        for i in range(k):
            f = i / k
            samples.append([round(a_[0] + (b_[0] - a_[0]) * f, 4), round(a_[1] + (b_[1] - a_[1]) * f, 4)])
    samples.append(list(WPS[-1]))
    xs = [q[0] for q in samples]
    ys = [q[1] for q in samples]
    spec = {"samples": samples, "sections": [], "waypoints": [list(q) for q in WPS], "waypoint_radius_m": 0.5, "drive_timeout_s": 90.0,
            "stills": {"play_aim": [-15.0, 4.5, -0.5], "him_uv": list(WPS[1]),
                       "topdown": [round((max(xs) + min(xs)) / 2, 3), round((max(ys) + min(ys)) / 2, 3), 14.0, 2000, 1400]}}
    W.OUT = OUT
    if "--no-run" not in sys.argv:
        W.run_godot(spec)
    R = json.load(open(os.path.join(OUT, "walk_check.json")))
    S = R["survey"]
    step_h = R["knight"]["step_height_m"]
    breaks = []
    for i, r in enumerate(S[:len(samples)]):
        if not r["hit"] or r["body_blocked"] or r["slope_deg"] > SLOPE_MAX:
            breaks.append({"i": i, "uv": r["uv"], "why": "no floor" if not r["hit"] else ("body inside a collider" if r["body_blocked"] else "slope %.1f" % r["slope_deg"])})
        elif i + 1 < len(samples) and S[i + 1]["hit"] and abs(S[i + 1]["z"] - r["z"]) > step_h:
            breaks.append({"i": i, "uv": r["uv"], "why": "riser %.3f m" % abs(S[i + 1]["z"] - r["z"])})
    # a SINGLE "no floor" sample between two walkable neighbours 0.05 m either side (and within a step of each other) is the
    # down-ray slipping through the heightfield shape's seam, not a hole: listed separately, not a break (the knight's driven
    # track over the same line is the check of record -- every frame on the floor)
    def ok_(j):
        return 0 <= j < len(samples) and S[j]["hit"] and not S[j]["body_blocked"] and S[j]["slope_deg"] <= SLOPE_MAX
    seams = [b for b in breaks if b["why"] == "no floor" and ok_(b["i"] - 1) and ok_(b["i"] + 1) and abs(S[b["i"] + 1]["z"] - S[b["i"] - 1]["z"]) <= step_h]
    breaks = [b for b in breaks if b not in seams]
    D = R["drive"]
    off = sum(1 for q in R["track"] if not q[3])
    zs = [r["z"] for r in S[:len(samples)] if r["hit"]]
    res = {"_what": __doc__.split("\n")[0], "waypoints_uv": WPS, "samples": len(samples), "breaks": breaks[:40], "n_breaks": len(breaks), "ray_seams": seams,
           "max_slope_deg": round(max(r["slope_deg"] for r in S[:len(samples)] if r["hit"]), 2), "z_range": [round(min(zs), 2), round(max(zs), 2)],
           "drive": {k: D[k] for k in ("reached_last_waypoint", "time_s", "frames", "end_uv", "end_z")}, "drive_frames_off_floor": off}
    res["PASS"] = bool(len(breaks) == 0 and D["reached_last_waypoint"] and off == 0)
    json.dump(res, open(os.path.join(OUT, "beach_ring.json"), "w"), indent=1)
    print("[beach_ring] %d samples, %d breaks (+%d single-sample ray seams), max slope %.1f deg, z %s; knight reached %s in %.1f s (%d off the floor) -> %s" % (
        len(samples), len(breaks), len(seams), res["max_slope_deg"], res["z_range"], D["reached_last_waypoint"], D["time_s"], off, "PASS" if res["PASS"] else "FAIL"))
    for b in breaks[:8]:
        print("  ", b)
    return 0 if res["PASS"] else 4


if __name__ == "__main__":
    sys.exit(main())
