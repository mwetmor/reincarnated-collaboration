#!/usr/bin/env python3
"""eor_plate_scan.py — locate frames carrying Grim Dawn's hovered-monster nameplate.

galadriel / visual-perception seam. Third-extraction pass (KC2-SIM Phase C).

Geometry measured on a known-good plate (s2 t=854.30, "Galakros, the Mountain"):
  full-frame ROI            x 600..1350, y 0..120
  name text rows            17..34   (light glyphs, min(R,G,B) > 120)
  monster LEVEL numeral     44..58   (red glyphs, R>150 and R-B>40)
  bar track / gold frame    59..63
  monster family label      91..103

The detector's only job is to say WHERE to look. Every reported level numeral is
an eye-read of a magnified exact-seek crop.

  scan  <video> <t0> <t1> <fps> <out.json>
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

ROI = (600, 0, 1350, 120)          # x0, y0, x1, y1 full-frame
NAME_ROWS = (17, 35)
LEVEL_ROWS = (43, 59)
FAM_ROWS = (90, 105)


def _masks(a: np.ndarray):
    """a: HxWx3 int array of the ROI. Returns (light, warm) boolean masks."""
    mn = a.min(2)
    R, B = a[:, :, 0], a[:, :, 2]
    light = mn > 120
    warm = (R > 150) & (R - B > 40)
    return light, warm


def score_roi(a: np.ndarray) -> dict:
    light, warm = _masks(a)
    nm = light[NAME_ROWS[0]:NAME_ROWS[1]]
    lv = warm[LEVEL_ROWS[0]:LEVEL_ROWS[1]]
    fam = light[FAM_ROWS[0]:FAM_ROWS[1]]
    cols = nm.any(0)
    xs = np.nonzero(cols)[0]
    return {
        "name_px": int(nm.sum()),
        "name_rows": int((nm.sum(1) > 8).sum()),
        "name_x0": int(xs[0] + ROI[0]) if xs.size else None,
        "name_x1": int(xs[-1] + ROI[0]) if xs.size else None,
        "lvl_px": int(lv.sum()),
        "fam_px": int(fam.sum()),
    }


def scan(video: str, t0: float, t1: float, fps: float, out: str,
         chunk: float = 30.0) -> list:
    """Series pass. Crops the ROI inside ffmpeg so decode cost stays low."""
    x0, y0, x1, y1 = ROI
    rows = []
    tmpd = tempfile.mkdtemp()
    t = t0
    while t < t1:
        dur = min(chunk, t1 - t)
        for f in os.listdir(tmpd):
            os.remove(os.path.join(tmpd, f))
        subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-t", f"{dur}",
             "-vf", f"crop={x1-x0}:{y1-y0}:{x0}:{y0},fps={fps}",
             "-y", os.path.join(tmpd, "f_%05d.png")], check=True)
        files = sorted(os.listdir(tmpd))
        for i, fn in enumerate(files):
            a = np.asarray(Image.open(os.path.join(tmpd, fn)).convert("RGB")).astype(int)
            r = score_roi(a)
            r["t"] = round(t + i / fps, 3)
            rows.append(r)
        t += dur
    json.dump(rows, open(out, "w"))
    return rows


def plate_frames(rows, name_px=40, name_rows=6):
    """Frames whose name-text band looks like a rendered nameplate."""
    return [r for r in rows if r["name_px"] >= name_px and r["name_rows"] >= name_rows]


if __name__ == "__main__":
    rows = scan(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]),
                float(sys.argv[4]), sys.argv[5])
    hit = plate_frames(rows)
    print(f"{len(rows)} frames, {len(hit)} plate candidates")
    for r in hit[:60]:
        print(r["t"], r["name_px"], r["name_rows"], r["lvl_px"], r["fam_px"],
              r["name_x0"], r["name_x1"])
