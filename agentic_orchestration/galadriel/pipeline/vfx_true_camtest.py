#!/usr/bin/env python3
"""Camera-registration feasibility test on the TRUE referent.

The battery's effect segmentation is CONTROL-DIFFERENCING.  The reference has
no control arm.  On the old (wrong) referent the substitute was a hue-sector
mask, which was well-posed there because the scene was teal and the effect was
fire.  ⚑ THAT IS NOT TRUE HERE: recon measures 80-84% of this referent's
chromatic luminance already inside the warm sector (the venue is a warm
sandstone dungeon).  A warm-hue mask on this clip selects ~1/3 of the frame.

So the segmentation has to come from somewhere else, and the strongest
available candidate is a MOTION-COMPENSATED TEMPORAL MEDIAN: if the camera
motion is a global 2-D translation to within a small residual, frames can be
warped into a common frame, the per-pixel median taken as a background plate,
and the effect recovered by differencing -- which is the same *kind* of
instrument the battery uses, rather than an appearance prior.

THIS SCRIPT DOES NOT ASSUME THAT WORKS.  It measures:
  (a) the per-frame global shift, by phase correlation on the scene region
  (b) the correlation PEAK HEIGHT, which is the tell for "no single global
      shift exists" -- the failure mode that produced a confident (0,0) on a
      translating camera in the lap-2 pass (note § 5, seventh instance)
  (c) the RESIDUAL after registration, on a background-only region, against
      the residual of the unregistered pair -- i.e. does registration actually
      buy anything
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma  # noqa: E402
from vfx_true_recon import BLACK_MASKS, frames, probe, valid_map  # noqa: E402


def phase_corr(a, b, win):
    """Return (dy, dx, peak_height, peak_ratio).

    peak_ratio = peak / (2nd-highest outside a 5 px exclusion) -- a global
    translation gives a sharp isolated peak; a scene with depth parallax gives
    a broad low mound and a ratio near 1.
    """
    A = np.fft.rfft2(a * win)
    B = np.fft.rfft2(b * win)
    R = A * np.conj(B)
    R /= np.maximum(np.abs(R), 1e-9)
    c = np.fft.irfft2(R, s=a.shape)
    idx = np.unravel_index(np.argmax(c), c.shape)
    peak = float(c[idx])
    cc = c.copy()
    y0, x0 = idx
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            cc[(y0 + dy) % c.shape[0], (x0 + dx) % c.shape[1]] = -1
    second = float(cc.max())
    dy = idx[0] if idx[0] < a.shape[0] // 2 else idx[0] - a.shape[0]
    dx = idx[1] if idx[1] < a.shape[1] // 2 else idx[1] - a.shape[1]
    return dy, dx, peak, peak / max(second, 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stride", type=int, default=6)
    ap.add_argument("--gap", type=int, default=1, help="frames between the pair")
    a = ap.parse_args()

    w, h, fps, codec, pix = probe(a.clip)
    V = valid_map(h, w)

    # region used for registration: the scene, minus the HUD-heavy bottom
    # strip, minus the minimap corner, minus the frame centre where the
    # action is.  Registration must be driven by BACKGROUND, not by the thing
    # being segmented -- otherwise the shift tracks the effect.
    reg = np.zeros((h, w), bool)
    reg[120:700, 260:1660] = True
    reg &= V
    cy, cx = 540, 960
    yy, xx = np.mgrid[0:h, 0:w]
    action = ((yy - cy) ** 2 + (xx - cx) ** 2) < 420 ** 2
    reg &= ~action

    ys, xs = np.nonzero(reg)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    hh_, ww_ = y1 - y0, x1 - x0
    wy = np.hanning(hh_)[:, None]
    wx = np.hanning(ww_)[None, :]
    win = wy * wx

    prev = None
    rows = []
    for i, f in frames(a.clip, w, h, stride=a.stride):
        L = luma(f)[y0:y1, x0:x1].astype(np.float32)
        if prev is not None:
            dy, dx, pk, ratio = phase_corr(L, prev, win)
            # residual test: unregistered vs registered, on the reg region only
            un = float(np.abs(L - prev).mean())
            sh = np.roll(np.roll(prev, dy, 0), dx, 1)
            m = np.ones_like(L, bool)
            if dy > 0:
                m[:dy] = False
            elif dy < 0:
                m[dy:] = False
            if dx > 0:
                m[:, :dx] = False
            elif dx < 0:
                m[:, dx:] = False
            rg = float(np.abs(L - sh)[m].mean())
            rows.append({"frame": i, "dy": int(dy), "dx": int(dx),
                         "peak": pk, "peak_ratio": ratio,
                         "resid_unreg": un, "resid_reg": rg})
        prev = L

    d = np.array([[r["dy"], r["dx"]] for r in rows], float)
    pk = np.array([r["peak"] for r in rows])
    pr = np.array([r["peak_ratio"] for r in rows])
    un = np.array([r["resid_unreg"] for r in rows])
    rg = np.array([r["resid_reg"] for r in rows])
    mag = np.hypot(d[:, 0], d[:, 1])

    res = {"clip": a.clip, "tag": a.tag, "stride": a.stride, "n_pairs": len(rows),
           "reg_region": {"y": [int(y0), int(y1)], "x": [int(x0), int(x1)],
                          "action_disc_excluded_r": 420},
           "shift_px_per_sampled_pair": {
               "median_mag": float(np.median(mag)), "p90_mag": float(np.percentile(mag, 90)),
               "max_mag": float(mag.max()), "frac_zero": float((mag == 0).mean()),
               "cumulative_dy": float(d[:, 0].sum()), "cumulative_dx": float(d[:, 1].sum())},
           "peak": {"median": float(np.median(pk)), "min": float(pk.min()),
                    "median_ratio": float(np.median(pr)), "min_ratio": float(pr.min())},
           "residual": {"unregistered_median": float(np.median(un)),
                        "registered_median": float(np.median(rg)),
                        "improvement_ratio": float(np.median(un) / max(np.median(rg), 1e-9))},
           "rows": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1))
    print("[%s] n=%d  shift median %.2f px  p90 %.2f  max %.2f  zero-frac %.3f"
          % (a.tag, len(rows), np.median(mag), np.percentile(mag, 90), mag.max(), (mag == 0).mean()))
    print("     cumulative drift  dy %+.0f  dx %+.0f px" % (d[:, 0].sum(), d[:, 1].sum()))
    print("     phase peak median %.4f (min %.4f)   peak/2nd ratio median %.2f (min %.2f)"
          % (np.median(pk), pk.min(), np.median(pr), pr.min()))
    print("     residual  unreg %.5f -> reg %.5f   improvement %.2fx"
          % (np.median(un), np.median(rg), np.median(un) / max(np.median(rg), 1e-9)))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
