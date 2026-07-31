#!/usr/bin/env python3
"""SHADOW-CAL instrument SC-5: the player's own shadow, measured while he RUNS.

WHY THIS WINDOW AND NOT ANOTHER
-------------------------------
A world-registered median plate can only reveal what TRANSLATES THROUGH THE
WORLD.  A figure standing still sits inside its own plate and is invisible by
construction -- which is why windows that merely *contain* a character yield
nothing, and why this cell's earlier passes returned zeros that meant "nobody
moved", not "no shadow".

The camera is hard-locked to the player (GAL-CAM; CAM-LOCK reproduced it), so
CAMERA SPEED IS PLAYER SPEED.  This instrument therefore finds the longest
continuous run of fast camera motion inside a burst, builds the plate from THAT
sub-run only, and measures inside it.  The player has then moved several metres
clear of his own plate footprint, and he and his shadow come out together.
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


def fast_run(shifts, min_speed=1.8, min_len=45):
    n = len(shifts)
    v = np.full(n, np.nan)
    for i in range(1, n):
        if np.isfinite(shifts[i]).all() and np.isfinite(shifts[i - 1]).all():
            v[i] = np.hypot(*(shifts[i] - shifts[i - 1]))
    ok = np.nan_to_num(v, nan=-1) >= min_speed
    best = (0, 0)
    i = 0
    while i < n:
        if ok[i]:
            j = i
            while j < n and ok[j]:
                j += 1
            if j - i > best[1] - best[0]:
                best = (i, j)
            i = j
        else:
            i += 1
    return best, v


def one(t, work, n=140, stride=6, min_speed=1.8, min_len=30, keep=False,
        draw_dir=None, max_draw=4, target_travel=170.0, min_len_trim=22):
    d = os.path.join(work, f"r{int(round(t)):06d}")
    if not os.path.isdir(d) or len(os.listdir(d)) < n // 2:
        sc_burst.burst(t, n, d, ext="jpg")
    paths = sorted(os.path.join(d, f) for f in os.listdir(d)
                   if f.endswith(".jpg"))
    info = {"t": t, "frames": len(paths)}
    try:
        shifts, ref0, diag = P.register(paths)
        (i0, i1), vel = fast_run(shifts, min_speed, min_len)
        info["run"] = [int(i0), int(i1)]
        info["run_len"] = int(i1 - i0)
        info["median_speed"] = float(np.nanmedian(vel[i0:i1])) if i1 > i0 else None
        if i1 - i0 < min_len:
            info["drop"] = "no-continuous-run"
            return info, []
        # TRAVEL CAP.  A world-registered plate is only valid for the GROUND:
        # anything with height shows parallax under camera translation (an
        # object at 3 m over a 28 m camera smears by ~11% of the travel), and
        # the plate's temporal MAD blows up with it -- measured 38 luma at 14 m
        # of travel versus ~2 luma at 3 m.  So the sub-run is trimmed about its
        # centre to `target_travel` px: far enough that the player clears his
        # own footprint, near enough that the scenery does not smear.
        mid = (i0 + i1) // 2
        j0, j1 = mid, mid + 1
        while j0 > i0 or j1 < i1:
            span = np.hypot(*(shifts[j1 - 1] - shifts[j0]))
            if span >= target_travel and (j1 - j0) >= min_len_trim:
                break
            if j0 > i0:
                j0 -= 1
            if j1 < i1:
                j1 += 1
        i0, i1 = j0, j1
        info["trimmed"] = [int(i0), int(i1)]
        sub = paths[i0:i1]
        ssh = shifts[i0:i1] - shifts[(i0 + i1) // 2]
        travel = float(max(np.ptp(ssh[:, 0]), np.ptp(ssh[:, 1])))
        info["travel_px"] = travel
        info["travel_m"] = travel / 54.47
        plate, sigma, cnt, valid, good, acc, vmask = P.build(sub, ssh,
                                                             min_samples=10)
        info["usable"] = len(good)
        info["sigma_med"] = float(np.median(sigma[valid]))
        info["plate_valid_pct"] = float(100 * valid.mean())
        ui_plate, ui_frac = R.ui_mask(plate)
        info["ui_frac"] = float(ui_frac)
        excl = R.FURN | ui_plate
        cam = sc_cam.nominal()
        recs, ndraw = [], 0
        for k, i in enumerate(good):
            if i % stride:
                continue
            fr = acc[k].astype(np.float32)
            uif, _ = R.ui_mask(fr)
            dbg, _ = R.debug_text_mask(fr)
            fv = valid & vmask[k] & ~excl & ~uif & ~dbg
            dets, shm, spm, rr = R.figures_and_shadows(fr, plate, fv, cam, sigma)
            for dd in dets:
                dd["frame_i"] = int(i0 + i)
                dd["t"] = t + (i0 + i) / 60.0
                dd["window_t"] = t
                dd["plate_luma_med"] = float(np.median(
                    0.2126 * plate[..., 0] + 0.7152 * plate[..., 1]
                    + 0.0722 * plate[..., 2]))
            recs += dets
            if draw_dir and dets and ndraw < max_draw:
                os.makedirs(draw_dir, exist_ok=True)
                R.draw(fr, dets, shm, spm,
                       os.path.join(draw_dir, f"r{int(round(t)):06d}_{i:04d}.jpg"))
                ndraw += 1
        info["pairs"] = len(recs)
        del acc, vmask
        return info, recs
    finally:
        if not keep:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--times", type=float, nargs="+", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=140)
    ap.add_argument("--stride", type=int, default=6)
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
        print(f"  t={t:8.1f} run {info.get('run_len',0):3d}f "
              f"v {info.get('median_speed') or float('nan'):4.1f}px/f "
              f"travel {info.get('travel_m', float('nan')):5.1f}m "
              f"sigma {info.get('sigma_med', float('nan')):5.2f} "
              f"{info.get('drop',''):>18s} pairs {info.get('pairs',0):3d}",
              flush=True)
        json.dump({"windows": infos, "pairs": allrecs}, open(a.out, "w"))
    print(f"windows {len(infos)}  pairs {len(allrecs)} -> {a.out}")
