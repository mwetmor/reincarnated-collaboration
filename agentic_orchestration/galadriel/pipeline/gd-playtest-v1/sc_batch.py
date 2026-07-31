#!/usr/bin/env python3
"""SHADOW-CAL: batch over candidate windows.

Per window: pull a burst, register, build the world plate, find screen-locked
content, run SC-1, harvest figure/shadow pairs.  Per-window yield is reported so
that windows which produced nothing are visible as windows that produced
nothing, rather than quietly missing from a pooled number.
"""
import argparse
import json
import os
import shutil
import sys
import traceback

import numpy as np

import sc_burst
import sc_cam
import sc_plate as P
import sc_run as R


def one(t, work, n=120, ext="jpg", stride=10, keep=False, draw_dir=None,
        max_draw=3, min_speed=1.5):
    d = os.path.join(work, f"w{int(round(t)):06d}")
    if not os.path.isdir(d) or len(os.listdir(d)) < n // 2:
        sc_burst.burst(t, n, d, ext=ext)
    paths = sorted(os.path.join(d, f) for f in os.listdir(d)
                   if f.endswith((".png", ".jpg")))
    shifts, ref, diag = P.register(paths)
    good = [i for i in range(len(paths)) if np.isfinite(shifts[i]).all()]
    if len(good) < 25:
        if not keep:
            shutil.rmtree(d, ignore_errors=True)
        return {"t": t, "frames": len(paths), "usable": len(good),
                "reason": "registration", "pairs": 0}, []
    ctrl = diag.get("control_rms_px")
    if ctrl is not None and ctrl > 1.0:
        if not keep:
            shutil.rmtree(d, ignore_errors=True)
        return {"t": t, "frames": len(paths), "usable": len(good),
                "control_rms_px": ctrl, "reason": "registration-control",
                "pairs": 0}, []
    plate, sigma, cnt, valid, good, acc, vmask = P.build(paths, shifts)
    lock, travel = R.screen_locked(paths, shifts)
    # NOTE: `lock` is REPORTED, not applied.  Under a translating camera the
    # PLAYER is screen-locked too -- masking screen-locked pixels deletes the
    # very figure the cell is measuring.  Exclusion is carried by the fixed
    # furniture boxes + the UI detector + the debug-label colour cut instead.
    ui_plate, ui_frac = R.ui_mask(plate)
    excl = R.FURN | ui_plate
    cam = sc_cam.nominal()
    recs = []
    ndraw = 0
    # CAMERA-VELOCITY GATE.  Background differencing can only reveal what
    # TRANSLATES IN THE WORLD.  A player standing still sits inside its own
    # median plate and is invisible by construction -- which is why windows
    # that merely CONTAIN motion yield nothing.  Frames are analysed only while
    # the camera (hard-locked to the player, GAL-CAM/CAM-LOCK) is actually
    # travelling, so the figure has moved clear of its own plate footprint.
    vel = np.full(len(paths), np.nan)
    fs = shifts
    for j in range(1, len(paths)):
        if np.isfinite(fs[j]).all() and np.isfinite(fs[j - 1]).all():
            vel[j] = np.hypot(*(fs[j] - fs[j - 1]))
    fast = vel >= min_speed
    info_fast = int(np.nansum(fast))
    for k, i in enumerate(good):
        if i % stride or not fast[i]:
            continue
        fr = acc[k].astype(np.float32)
        ui_f, _ = R.ui_mask(fr)
        dbg, _ = R.debug_text_mask(fr)
        fv = valid & vmask[k] & ~excl & ~ui_f & ~dbg
        dets, shm, spm, rr = R.figures_and_shadows(fr, plate, fv, cam, sigma)
        for dd in dets:
            dd["frame_i"] = int(i)
            dd["t"] = t + i / 60.0
            dd["window_t"] = t
        recs += dets
        if draw_dir and dets and ndraw < max_draw:
            os.makedirs(draw_dir, exist_ok=True)
            R.draw(fr, dets, shm, spm,
                   os.path.join(draw_dir, f"w{int(round(t)):06d}_{i:04d}.jpg"))
            ndraw += 1
    info = {"t": t, "frames": len(paths), "usable": len(good),
            "travel_px": travel,
            "screen_locked_px": int(lock.sum()) if lock is not None else None,
            "control_rms_px": diag.get("control_rms_px"),
            "sigma_med": float(np.median(sigma[valid])),
            "ui_frac": float(ui_frac),
            "plate_valid_pct": float(100 * valid.mean()),
            "fast_frames": info_fast,
            "median_speed_px_per_frame": float(np.nanmedian(vel)),
            "pairs": len(recs)}
    del acc, vmask
    if not keep:
        shutil.rmtree(d, ignore_errors=True)
    return info, recs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--times", type=float, nargs="+", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--stride", type=int, default=10)
    ap.add_argument("--ext", default="jpg")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--draw", default=None)
    ap.add_argument("--min-speed", type=float, default=1.5)
    a = ap.parse_args()

    os.makedirs(a.work, exist_ok=True)
    infos, allrecs = [], []
    for t in a.times:
        try:
            info, recs = one(t, a.work, n=a.n, ext=a.ext, stride=a.stride,
                             keep=a.keep, draw_dir=a.draw,
                             min_speed=a.min_speed)
        except Exception:
            traceback.print_exc()
            print(f"  t={t:8.1f}  FAILED", flush=True)
            continue
        infos.append(info)
        allrecs += recs
        print(f"  t={t:8.1f}  usable {info['usable']:3d}/{info['frames']}  "
              f"travel {info.get('travel_px', float('nan')):6.1f}px  "
              f"ctrl {info.get('control_rms_px') or float('nan'):5.2f}px  "
              f"sigma {info.get('sigma_med', float('nan')):5.2f}  "
              f"fast {info.get('fast_frames', 0):3d}  "
              f"pairs {info['pairs']:3d}", flush=True)
        json.dump({"windows": infos, "pairs": allrecs}, open(a.out, "w"))
    print(f"total pairs {len(allrecs)} from {len(infos)} windows -> {a.out}")
