#!/usr/bin/env python3
"""§ 50 (c) walk-validity check on a ph_life perf trace: over the 900-frame window, no 60-frame (1 s) span with knight
displacement < 0.3 m; also waypoints reached, path length, min 1-s displacement."""
import json
import sys

import numpy as np


def check(trace):
    t = json.load(open(trace))
    k = np.array([[p[0], p[1]] for p in t["knight_uv_wp"]])
    wp = np.array([p[2] for p in t["knight_uv_wp"]])
    d1 = np.hypot(*(k[60:] - k[:-60]).T)
    still = np.where(d1 < 0.3)[0]
    step = np.hypot(*np.diff(k, axis=0).T)
    return {"frames": len(k), "loop": t.get("loop"), "min_1s_displacement_m": round(float(d1.min()), 3),
            "spans_under_0.3m": int(len(still)), "first_still_frame": int(still[0]) if len(still) else None,
            "path_m": round(float(step.sum()), 2), "waypoint_advances": int((np.diff(wp) != 0).sum()),
            "start_uv": k[0].round(2).tolist(), "end_uv": k[-1].round(2).tolist(),
            "valid": len(still) == 0}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, json.dumps(check(p)))
