#!/usr/bin/env python3
"""SHADOW-CAL: harvest figure/shadow pairs from camera-STATIC windows.

Why static windows carry the load: with the camera still, the median plate needs
no resampling at all, so the temporal noise floor drops from ~8 luma (warped) to
~0.6 luma.  A cast shadow darkens ground by 20-60 luma; at a 0.6 luma floor that
is a 30:1 signal, and every monster that walks across the frame delivers one.
Monsters roam the WHOLE frame, so a static window still samples many map
locations and many screen rows -- which is exactly what question (a) needs.

GATES, all reported rather than silently applied:
  travel   - the window must really be static (patch consensus, not assumed)
  sigma    - median temporal MAD; a loading-screen crossfade or a screen-wide
             VFX pushes this to 8-25 luma and the window is dropped
  plate    - fraction of frames contributing
"""
import argparse
import json
import os
import shutil
import traceback

import numpy as np
from scipy import ndimage

import sc_burst
import sc_cam
import sc_plate as P
import sc_run as R


def static_check(paths, k=8):
    idx = np.linspace(0, len(paths) - 1, k).astype(int)
    ref = P.patchset(P.luma(P.read(paths[idx[0]]).astype(np.float32)))
    worst = 0.0
    for i in idx[1:]:
        s, nv, nab = P.consensus(
            ref, P.patchset(P.luma(P.read(paths[i]).astype(np.float32))),
            maxshift=90)
        if s is None:
            return None, nv
        worst = max(worst, abs(s[0]), abs(s[1]))
    return worst, nv


def one(t, work, n=60, stride=10, sigma_max=3.0, travel_max=1.5,
        keep=False, draw_dir=None, max_draw=2):
    d = os.path.join(work, f"h{int(round(t)):06d}")
    if not os.path.isdir(d) or len(os.listdir(d)) < n // 2:
        sc_burst.burst(t, n, d, ext="jpg")
    paths = sorted(os.path.join(d, f) for f in os.listdir(d)
                   if f.endswith(".jpg"))
    info = {"t": t, "frames": len(paths)}
    try:
        travel, nv = static_check(paths)
        info["travel_px"] = travel
        info["voting"] = nv
        if travel is None or travel > travel_max:
            info["drop"] = "not-static"
            return info, []
        st = np.stack([P.read(p) for p in paths]).astype(np.float32)
        plate = np.median(st, axis=0)
        L = 0.2126 * st[..., 0] + 0.7152 * st[..., 1] + 0.0722 * st[..., 2]
        Lp = 0.2126 * plate[..., 0] + 0.7152 * plate[..., 1] + 0.0722 * plate[..., 2]
        sigma = (1.4826 * np.median(np.abs(L - Lp[None]), axis=0)).astype(np.float32)
        del L
        info["sigma_med"] = float(np.median(sigma))
        info["plate_luma_med"] = float(np.median(Lp))
        if info["sigma_med"] > sigma_max:
            info["drop"] = "restless"
            return info, []
        cam = sc_cam.nominal()
        # UI panels/tooltips: found on the plate (persistent) and on each frame
        # analysed (a tooltip that pops mid-window).  The screen-locked detector
        # cannot help here -- it needs camera motion, and this window has none.
        ui_plate, ui_frac_plate = R.ui_mask(plate)
        info["ui_frac_plate"] = ui_frac_plate
        info["ui_masked_pct"] = float(100 * ui_plate.mean())
        valid0 = ~R.FURN
        recs, ndraw = [], 0
        for i in range(0, len(paths), stride):
            ui_f, _ = R.ui_mask(st[i])
            ui = ui_plate | ui_f
            valid = valid0 & ~ui
            dets, shm, spm, rr = R.figures_and_shadows(st[i], plate, valid,
                                                       cam, sigma)
            for dd in dets:
                dd["frame_i"] = int(i)
                dd["t"] = t + i / 60.0
                dd["window_t"] = t
                dd["plate_luma_med"] = info["plate_luma_med"]
            recs += dets
            if draw_dir and dets and ndraw < max_draw:
                os.makedirs(draw_dir, exist_ok=True)
                R.draw(st[i], dets, shm, spm,
                       os.path.join(draw_dir,
                                    f"h{int(round(t)):06d}_{i:04d}.jpg"))
                ndraw += 1
        info["pairs"] = len(recs)
        return info, recs
    finally:
        if not keep:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--times", type=float, nargs="+", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--stride", type=int, default=10)
    ap.add_argument("--draw", default=None)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()

    os.makedirs(a.work, exist_ok=True)
    infos, allrecs = [], []
    for t in a.times:
        try:
            info, recs = one(t, a.work, n=a.n, stride=a.stride,
                             draw_dir=a.draw, keep=a.keep)
        except Exception:
            traceback.print_exc()
            continue
        infos.append(info)
        allrecs += recs
        print(f"  t={t:8.1f} travel {str(info.get('travel_px')):>6.6s} "
              f"sigma {info.get('sigma_med', float('nan')):6.2f} "
              f"plateL {info.get('plate_luma_med', float('nan')):5.1f} "
              f"{info.get('drop','') :>10s} pairs {info.get('pairs', 0):3d}",
              flush=True)
        json.dump({"windows": infos, "pairs": allrecs}, open(a.out, "w"))
    npair = len(allrecs)
    used = sum(1 for i in infos if "drop" not in i)
    print(f"windows {len(infos)}  used {used}  pairs {npair} -> {a.out}")
