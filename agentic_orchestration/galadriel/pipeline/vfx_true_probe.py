#!/usr/bin/env python3
"""Pixel-level probe: what, if anything, separates the WW effect from a warm
sandstone venue?  Run on named rectangles so the answer is a measurement and
not an impression."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma, sat_val  # noqa: E402
from vfx_true_recon import hue_sat, probe, valid_map  # noqa: E402


def grab(path, t, w, h):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path,
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out[:w * h * 3], np.uint8).reshape(h, w, 3)


def stats(name, f, y0, y1, x0, x1):
    sub = f[y0:y1, x0:x1]
    L = luma(sub)
    sA, _ = sat_val(sub)
    hh, _ = hue_sat(sub)
    hw = np.where(hh > 180, hh - 360, hh)     # wrap for a red-centred mean
    return {"name": name, "box": [x0, y0, x1 - x0, y1 - y0],
            "rgb_mean": [round(float(sub[..., k].mean()), 1) for k in range(3)],
            "L": {"p20": round(float(np.percentile(L, 20)), 4),
                  "p50": round(float(np.median(L)), 4),
                  "p95": round(float(np.percentile(L, 95)), 4),
                  "ratio": round(float(np.percentile(L, 95) / max(np.percentile(L, 20), 1e-6)), 3)},
            "S": {"p20": round(float(np.percentile(sA, 20)), 4),
                  "p50": round(float(np.median(sA)), 4),
                  "p80": round(float(np.percentile(sA, 80)), 4)},
            "hue_deg": {"p20": round(float(np.percentile(hw, 20)), 1),
                        "p50": round(float(np.median(hw)), 1),
                        "p80": round(float(np.percentile(hw, 80)), 1)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--boxes", required=True, help="name:x,y,w,h;name:x,y,w,h")
    ap.add_argument("--out")
    a = ap.parse_args()
    w, h, *_ = probe(a.clip)
    f = grab(a.clip, a.t, w, h)
    rows = []
    for spec in a.boxes.split(";"):
        nm, rest = spec.split(":")
        x, y, ww, hh_ = [int(v) for v in rest.split(",")]
        rows.append(stats(nm, f, y, y + hh_, x, x + ww))
    for r in rows:
        print("%-16s rgb%-18s L p20/p50/p95 %.3f/%.3f/%.3f  ratio %5.2f  S %.3f/%.3f/%.3f  hue %6.1f/%6.1f/%6.1f"
              % (r["name"], str(r["rgb_mean"]), r["L"]["p20"], r["L"]["p50"], r["L"]["p95"],
                 r["L"]["ratio"], r["S"]["p20"], r["S"]["p50"], r["S"]["p80"],
                 r["hue_deg"]["p20"], r["hue_deg"]["p50"], r["hue_deg"]["p80"]))
    if a.out:
        Path(a.out).write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
