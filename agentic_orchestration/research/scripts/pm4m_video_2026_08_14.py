#!/usr/bin/env python3
"""KC2-PM4 Lap M -- Q2/Q3 video instrument.  NUMERIC-FIRST, image-budget <= 3.

Reads the referent capture (digest-verified at Lap K) and measures, WITHOUT reading any image
into context:
  * per-frame colour-class ink (Lap K's I-4 masks, imported verbatim from /tmp/pm4k/k3.py)
  * a RADIAL ANNULUS profile around the player anchor -- the discriminator between a converging
    projectile ring (ink appears in an outer annulus then collapses inward onto the anchor) and a
    melee/ground event (ink appears at the anchor and stays)
  * nameplate census + contact ring (Lap H-2 instrument, LOWER BOUNDS)
Outputs arrays + CSV.  No attribution is asserted by the instrument; § in method.md does that.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import numpy as np

sys.path.insert(0, "/tmp/pm4k")
from bars import find_bars                                    # noqa: E402
from k3 import colour_classes, boss_banner, combat_text, V, K, PX, PY, RC   # noqa: E402

OUT = pathlib.Path("/tmp/pm4m")
OUT.mkdir(exist_ok=True)


def grab(s: float, dur: float, fps: int = 60) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-ss", str(s), "-t", str(dur), "-i", V,
           "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.run(cmd, capture_output=True)
    b = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(b) // (1920 * 1080 * 3)
    return b[: n * 1920 * 1080 * 3].reshape(n, 1080, 1920, 3)


#: ground-plane radius rings around the player anchor, in screen px on the x axis;
#: y is compressed by K = 0.537 (the Lap H-2 D2 ground-plane calibration).
RINGS = [(0, 60), (60, 120), (120, 200), (200, 300), (300, 450), (450, 650)]
_yy, _xx = np.mgrid[0:1080, 0:1920]
_r = np.sqrt(((_xx - PX) ** 2) + ((_yy - PY) / K) ** 2)
RING_MASKS = [((_r >= a) & (_r < b)) for a, b in RINGS]
RING_AREA = [float(m.sum()) for m in RING_MASKS]


def sat_mask(a: np.ndarray) -> np.ndarray:
    A = a.astype(np.int16)
    R, G, B = A[..., 0], A[..., 1], A[..., 2]
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    return (mx > 110) & ((mx - mn) > 55)


def green_mask(a: np.ndarray) -> np.ndarray:
    A = a.astype(np.int16)
    R, G, B = A[..., 0], A[..., 1], A[..., 2]
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    s = (mx > 110) & ((mx - mn) > 55)
    return s & (G >= mx) & (R < G * 0.75) & (B < G * 0.85)


def frame_rows(F: np.ndarray, t0: float, fps: float, do_plates: bool):
    rows = []
    for i, fr in enumerate(F):
        t = t0 + i / fps
        cc = colour_classes(fr)
        gm = green_mask(fr)
        sm = sat_mask(fr)
        row = dict(t_s=round(t, 4), **{k: round(v, 8) for k, v in cc.items()})
        for j, (a, b) in enumerate(RINGS):
            row[f"green_r{a}_{b}"] = round(float(gm[RING_MASKS[j]].sum()) / RING_AREA[j], 8)
            row[f"sat_r{a}_{b}"] = round(float(sm[RING_MASKS[j]].sum()) / RING_AREA[j], 8)
        if do_plates:
            bars = find_bars(fr)
            row["plates"] = len(bars)
            row["ring_plates"] = sum(
                1 for b in bars
                if np.hypot(b["x_c"] - PX, (b["y"] - PY) / K) <= RC)
            bb, bt = boss_banner(fr)
            row["boss_banner"], row["boss_txt_px"] = bb, bt
        rows.append(row)
    return rows


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "death"
    if mode == "death":
        t0, dur, fps, plates = 862.0000, 3.4, 60, True
        tag = "death_window_862.0_865.4_60fps"
    elif mode == "wave160":
        t0, dur, fps, plates = 838.8667, 27.0, 10, False
        tag = "wave160_838.87_865.87_10fps"
    else:
        t0, dur, fps, plates = float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), False
        tag = f"custom_{t0}_{dur}_{fps}"

    chunk = 1.0
    rows = []
    s = t0
    while s < t0 + dur - 1e-6:
        d = min(chunk, t0 + dur - s)
        F = grab(s, d, fps)
        rows += frame_rows(F, s, fps, plates)
        del F
        s += d
    import csv
    p = OUT / f"pm4m_{tag}.csv"
    with p.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {p} rows={len(rows)}")
    print(json.dumps(rows[0], indent=0)[:400])


if __name__ == "__main__":
    main()
