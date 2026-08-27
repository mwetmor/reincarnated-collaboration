#!/usr/bin/env python3
"""Effect-PRESENCE curve on the true referent, and the HUD map that has to be
removed before any of it means anything.

Why a presence curve at all: the R-27 pass had a clip that was ONE burn with a
fade in and out, so its phase model ("action / decay / null") could be derived
from a global luma curve.  This referent is 25 s of continuous ARPG combat in
which the whirlwind is toggled on and off many times.  There is no single
action phase; there are BURSTS, and the negative control has to be the
in-clip frames BETWEEN them.  Both facts have to be measured, not assumed.

The presence statistic is deliberately NOT the statistic being anchored:
it is the count of RED-CHROMA pixels (chroma = max-min, hue near red), which
the probe shows separates the disc (C~0.57, hue~14 deg) from the sandstone
venue (C~0.20, hue~24 deg), the torches (C~0.33), the gold damage text
(hue~30-40 deg) and the gold training dummies (hue~20-33 deg, C~0.20-0.30).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma  # noqa: E402
from vfx_true_recon import frames, hue_sat, probe, valid_map  # noqa: E402

# ---------------------------------------------------------------------------
# HUD.  Diablo IV draws a fixed-position overlay.  Several of its elements are
# large, saturated and RED (health globe) or ORANGE (resource orb) -- i.e.
# exactly what any red-chroma test selects.  They are not scene and they are
# not effect.  Boxes are stated in 1920x1080 image space and are VERIFIED by
# the temporal-std map (evidence/recon-*-Lstd.png) plus direct inspection.
# ---------------------------------------------------------------------------
HUD_BOXES = [
    ("action_bar_and_globes", 300, 640, 1240, 440),   # skill bar, health globe, resource orb, buff row
    ("minimap_and_torment", 1580, 0, 340, 320),       # minimap, zone name, clock, Torment badge
    ("party_frames", 0, 380, 300, 200),               # Subo / Aldkin portraits + bars
    ("boss_bar", 620, 0, 700, 90),                    # BOSS TRAINING DUMMY header bar
]


def hud_map(h, w):
    H = np.zeros((h, w), bool)
    for _, x, y, ww, hh in HUD_BOXES:
        H[y:min(h, y + hh), x:min(w, x + ww)] = True
    return H


def chroma(f):
    a = f.astype(np.float32) / 255.0
    return a.max(2) - a.min(2)


def red_mask(hh, C, L, hue_hi=20.0, hue_lo=340.0, c_floor=0.35, l_floor=0.05):
    return ((hh < hue_hi) | (hh >= hue_lo)) & (C > c_floor) & (L > l_floor)


def coherent(M, min_px=12):
    M = ndimage.binary_opening(M, np.ones((3, 3)))
    lab, k = ndimage.label(M, np.ones((3, 3)))
    if not k:
        return np.zeros_like(M), lab, np.array([])
    sz = np.array(ndimage.sum(M, lab, range(1, k + 1)))
    keep = np.nonzero(sz >= min_px)[0] + 1
    M = np.isin(lab, keep) if keep.size else np.zeros_like(M)
    lab, k = ndimage.label(M, np.ones((3, 3)))
    sz = np.array(ndimage.sum(M, lab, range(1, k + 1))) if k else np.array([])
    return M, lab, sz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stride", type=int, default=3)
    a = ap.parse_args()

    w, h, fps, *_ = probe(a.clip)
    V = valid_map(h, w)
    HUD = hud_map(h, w)
    SCENE = V & ~HUD

    idx, area, area_nohud, big, ncomp, cx_, cy_ = [], [], [], [], [], [], []
    for i, f in frames(a.clip, w, h, stride=a.stride):
        L = luma(f)
        hh, _ = hue_sat(f)
        C = chroma(f)
        raw = red_mask(hh, C, L)
        M, lab, sz = coherent(raw & SCENE)
        idx.append(i)
        area.append(int((raw & V).sum()))
        area_nohud.append(int(M.sum()))
        ncomp.append(int(sz.size))
        if sz.size:
            big.append(int(sz.max()))
            lc = lab == int(np.argmax(sz) + 1)
            ys, xs = np.nonzero(lc)
            cy_.append(float(ys.mean()))
            cx_.append(float(xs.mean()))
        else:
            big.append(0)
            cy_.append(-1.0)
            cx_.append(-1.0)

    big = np.array(big)
    res = {"clip": a.clip, "tag": a.tag, "stride": a.stride, "fps": fps,
           "hud_boxes": [{"name": n, "x": x, "y": y, "w": ww, "h": hh} for n, x, y, ww, hh in HUD_BOXES],
           "hud_frac_of_valid": float((HUD & V).sum() / V.sum()),
           "scene_frac": float(SCENE.mean()),
           "curves": {"frame": idx, "red_area_raw_incl_hud": area,
                      "red_area_scene_coherent": area_nohud,
                      "largest_component_px": big.tolist(),
                      "n_components": ncomp,
                      "largest_cx": np.round(cx_, 1).tolist(),
                      "largest_cy": np.round(cy_, 1).tolist()},
           "summary": {"largest_median": float(np.median(big)),
                       "largest_p90": float(np.percentile(big, 90)),
                       "largest_max": float(big.max()),
                       "largest_min": float(big.min()),
                       "frac_frames_largest_over_2000": float((big > 2000).mean()),
                       "frac_frames_largest_under_500": float((big < 500).mean())}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1))
    order = np.argsort(big)[::-1]
    print("[%s] n=%d  HUD %.3f of valid" % (a.tag, len(idx), res["hud_frac_of_valid"]))
    print("  largest red component px: median %d  p90 %d  max %d  min %d"
          % (np.median(big), np.percentile(big, 90), big.max(), big.min()))
    print("  frames with largest>2000: %.3f   <500: %.3f"
          % ((big > 2000).mean(), (big < 500).mean()))
    print("  TOP frames (frame, px, t):",
          [(idx[k], int(big[k]), round(idx[k] / fps, 2)) for k in order[:8]])
    print("  BOTTOM frames:",
          [(idx[k], int(big[k]), round(idx[k] / fps, 2)) for k in order[-8:]])
    print("wrote", a.out)


if __name__ == "__main__":
    main()
