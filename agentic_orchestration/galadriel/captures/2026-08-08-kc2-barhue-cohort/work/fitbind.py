#!/usr/bin/env python3
"""Self-calibrating plate<->readout binding.

For a held nameplate, the plate bar's fill EDGE and the hovered body's fraction
are related by ONE affine map that is a property of the plate art, not of the
monster:   edge = x0 + f * (x1 - x0).

So for every candidate body on camera during the hover, regress edge on
fraction. The bound body is the one that comes out LINEAR at pixel residuals;
every other body's HP moves independently of the bar and cannot. The fit also
returns the calibration, which must then be the SAME across independently bound
spans - that consistency is the check that makes it a measurement rather than a
curve-fit.
"""
import json
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline")
import eor_cohort as CO      # noqa: E402
import eor_platebind as PB   # noqa: E402


def load(scan_path, strip_path):
    fs = json.load(open(scan_path))["f"]
    st = {round(r["t"], 4): r["plate"] for r in json.load(open(strip_path))["f"]}
    for f in fs:
        p = st.get(round(f["t"], 4))
        if p:
            f["plate"] = p
    return fs


def bodies(f):
    rows = [r for r in f["rd"] if r["kind"]]
    return CO._cluster_frame(rows) if rows else []


def fit(xs, ys):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    if xs.size < 3 or xs.std() < 1e-9:
        return None
    b, a = np.polyfit(xs, ys, 1)
    pred = a + b * xs
    res = ys - pred
    ss = float(((ys - ys.mean()) ** 2).sum())
    r2 = 1 - float((res ** 2).sum()) / ss if ss > 0 else 0.0
    return {"a": float(a), "b": float(b), "rms": float(np.sqrt((res ** 2).mean())),
            "r2": r2, "n": int(xs.size), "spread": float(xs.max() - xs.min())}


def span_fits(fs, t0, t1, min_n=5, contrast_min=55.0):
    per = defaultdict(lambda: {"f": [], "e": [], "t": [], "cur": []})
    for f in fs:
        if not (t0 - 1e-6 <= f["t"] <= t1 + 1e-6):
            continue
        p = f["plate"]
        if p.get("edge") is None or p.get("contrast", 0) < contrast_min:
            continue
        for b in bodies(f):
            if not b["max"] or b["cur"] is None:
                continue
            per[b["max"]]["f"].append(b["cur"] / b["max"])
            per[b["max"]]["e"].append(p["edge"])
            per[b["max"]]["t"].append(f["t"])
            per[b["max"]]["cur"].append(b["cur"])
    out = []
    for mx, v in per.items():
        if len(v["f"]) < min_n:
            continue
        r = fit(v["f"], v["e"])
        if r:
            r["max"] = mx
            r["curs"] = sorted(set(v["cur"]))[:8]
            out.append(r)
    out.sort(key=lambda r: (r["rms"] if r["spread"] > 0.02 else 9e9))
    return out


if __name__ == "__main__":
    fs = load(sys.argv[1], sys.argv[2])
    t0, t1 = float(sys.argv[3]), float(sys.argv[4])
    lab = sys.argv[5] if len(sys.argv) > 5 else ""
    print(f"=== {t0:.4f} -> {t1:.4f}  {lab}")
    for r in span_fits(fs, t0, t1):
        print("  max=%9d n=%2d spread=%.3f rms=%6.2fpx r2=%+.4f  x0=%7.2f x1=%7.2f"
              % (r["max"], r["n"], r["spread"], r["rms"], r["r2"],
                 r["a"], r["a"] + r["b"]))
