#!/usr/bin/env python3
"""C-9 MIX v3 -- THE HEAD AGAINST THE TAIL: is the ball of fire darker and deeper than its tail? drax.

  python3 tools/head_tail.py --dir work/mix3/fall [--json OUT]

The frames come from godot/tools/probe_rock_match.gd (the default MIX v3, --as-web, 1920 x 1080, --fixed-fps 60):
per fall frame a still and the head's screen point (the comet's ball sits on the slot's rock point; MIX v3 draws
no rock). The travel's screen direction is taken from the neighbouring frames' points.

  HEAD  -- effect pixels in a disc of the ball's screen radius round the head point
  TAIL  -- effect pixels in a band 1.6 to 4.5 radii BEHIND it along the travel, one radius either side
Effect pixels: chroma > 28 or L* < 30 (the snow, its warm light and the shadow are light and low-chroma).
Per region: mean L*, the dark share (L* < 30) and the bright share (L* > 80), averaged over the frames.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

BALL_M = 0.5          # the comet cap's radius (meteor_fx._comet_mesh R)
CAP_OFF = 0.3         # the cap's centre sits this far behind the comet's origin (the slot's rock point)
ROCK_R = 0.34         # what rock_r_px measures (meteor_fx ROCK_R)


def lab(img):
    a = np.asarray(img.convert("RGB"), dtype=np.float64) / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = lin @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16
    return L, np.hypot(500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2]))


def stats(L, C, mask):
    fx = mask & ((C > 28) | (L < 30))
    v = L[fx]
    if v.size < 30:
        return None
    return {"px": int(v.size), "mean_L": float(v.mean()), "dark": float((v < 30).mean()), "bright": float((v > 80).mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--json")
    o = ap.parse_args()
    F = json.load(open(os.path.join(o.dir, "rock_frames.json")))["frames"]
    rows = []
    for k, f in enumerate(F):
        if k == 0 or k == len(F) - 1:
            continue
        p = np.array(f["rock_px"])
        v = np.array(F[k + 1]["rock_px"]) - np.array(F[k - 1]["rock_px"])
        if np.linalg.norm(v) < 1e-3:
            continue
        u = v / np.linalg.norm(v)
        R = f["rock_r_px"] * BALL_M / ROCK_R
        p = p - u * f["rock_r_px"] * CAP_OFF / ROCK_R      # the ball's centre
        L, C = lab(Image.open(os.path.join(o.dir, f["file"])))
        h, w = L.shape
        yy, xx = np.mgrid[0:h, 0:w]
        dx, dy = xx - p[0], yy - p[1]
        head = dx * dx + dy * dy < R * R
        along = -(dx * u[0] + dy * u[1])            # behind the head is positive
        across = np.abs(dx * u[1] - dy * u[0])
        tail = (along > 1.6 * R) & (along < 4.5 * R) & (across < R)
        sh, st = stats(L, C, head), stats(L, C, tail)
        if sh and st:
            rows.append({"t": round(f["t"], 3), "head": sh, "tail": st})
    mean = {r: {k: round(float(np.mean([x[r][k] for x in rows])), 4) for k in ("mean_L", "dark", "bright")} for r in ("head", "tail")}
    out = {"what": "C-9 MIX v3: the fall's head (the ball of fire with its dark core) against its tail, same frames, play camera, phone look",
           "dir": o.dir, "frames": len(rows), "ball_m": BALL_M, "mean": mean,
           "head_minus_tail": {k: round(mean["head"][k] - mean["tail"][k], 4) for k in ("mean_L", "dark", "bright")}, "rows": rows}
    print(json.dumps({k: out[k] for k in ("frames", "mean", "head_minus_tail")}, indent=1))
    if o.json:
        json.dump(out, open(o.json, "w"), indent=1)


if __name__ == "__main__":
    main()
