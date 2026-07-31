#!/usr/bin/env python3
"""SHADOW-CAL instrument SC-4: scene-wide shadow azimuth from ground-plane
radial darkness dipoles.  Single frame, no background plate, no figure
detection.

IDEA
----
Under ONE directional light every occluder in the scene -- character, monster,
fence post, tree, crate, wall -- puts its dark side in the SAME ground
direction.  So at any point of ground, sample the luma along rays at every
azimuth (rays are traced ON THE GROUND PLANE through the GAL-CAM pinhole, then
projected to screen, so a metre is a metre at every screen row), and take the
FIRST ANGULAR HARMONIC of that profile.  Its phase points at the darker side;
its amplitude says how one-sided the darkness is.

A seed sitting on plain floor has a tiny amplitude and is discarded.  A seed
next to an occluder has a large one, and its phase is the light's azimuth.

WHAT MAKES THIS FALSIFIABLE
---------------------------
If Grim Dawn had no single shadow author, the surviving phases would be
scattered and the circular sd would be large.  A flat-lit foggy cave with no
directional shadowing is therefore run as the NULL CONTROL, and a synthetic
scene of known azimuth as the POSITIVE control.  The instrument only gets to
report on the fixture if it passes both.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage

import sc_cam
import sc_run as R

NANG = 72                      # 5 deg angular resolution
R_IN, R_OUT, NRAD = 0.45, 2.60, 12     # metres of ground along each ray


def sample_bilinear(L, xy):
    x = np.clip(xy[..., 0], 0, L.shape[1] - 2)
    y = np.clip(xy[..., 1], 0, L.shape[0] - 2)
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fx = x - x0
    fy = y - y0
    return (L[y0, x0] * (1 - fx) * (1 - fy) + L[y0, x0 + 1] * fx * (1 - fy)
            + L[y0 + 1, x0] * (1 - fx) * fy + L[y0 + 1, x0 + 1] * fx * fy)


def dipoles(frame_rgb, cam, mask_bad=None, step=64, y0=170, y1=930,
            x0=30, x1=1890, min_amp=0.055):
    a = np.asarray(frame_rgb, np.float32)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    bad = np.zeros(L.shape, bool) if mask_bad is None else mask_bad
    ang = np.arange(NANG) * (2 * np.pi / NANG)
    rad = np.linspace(R_IN, R_OUT, NRAD)
    ca, sa = np.cos(ang), np.sin(ang)

    ys = np.arange(y0, y1, step)
    xs = np.arange(x0, x1, step)
    out = []
    for sy in ys:
        for sx in xs:
            if bad[sy, sx]:
                continue
            g = cam.unproject_ground([[float(sx), float(sy)]])
            gx, gz = float(g[0]), float(g[2])
            # ground points: (NANG, NRAD, 3)
            P = np.empty((NANG, NRAD, 3))
            P[..., 0] = gx + rad[None, :] * ca[:, None]
            P[..., 1] = 0.0
            P[..., 2] = gz + rad[None, :] * sa[:, None]
            uv = cam.project(P.reshape(-1, 3)).reshape(NANG, NRAD, 2)
            if (uv[..., 0] < 2).any() or (uv[..., 0] > L.shape[1] - 3).any() \
               or (uv[..., 1] < 2).any() or (uv[..., 1] > L.shape[0] - 3).any():
                continue
            ui = np.round(uv).astype(int)
            if bad[ui[..., 1], ui[..., 0]].any():
                continue
            V = sample_bilinear(L, uv)
            prof = V.mean(1)
            m = prof.mean()
            if m < 6.0:
                continue
            a1 = (prof * ca).mean() * 2.0
            b1 = (prof * sa).mean() * 2.0
            amp = math.hypot(a1, b1) / m
            phi = math.degrees(math.atan2(-b1, -a1))   # toward the DARK side
            out.append({"x": int(sx), "y": int(sy), "amp": amp, "phi": phi,
                        "mean": float(m),
                        "contrast": float((prof.max() - prof.min()) / m)})
    return out


def circ(deg, w=None):
    a = np.radians(np.asarray(deg, float))
    w = np.ones_like(a) if w is None else np.asarray(w, float)
    C = (w * np.cos(a)).sum() / w.sum()
    S = (w * np.sin(a)).sum() / w.sum()
    Rl = math.hypot(C, S)
    mean = math.degrees(math.atan2(S, C))
    sd = math.degrees(math.sqrt(-2 * math.log(Rl))) if Rl > 1e-9 else float("nan")
    return mean, sd, Rl


def frame_azimuth(path, cam, min_amp=0.055, step=64):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    ui, _ = R.ui_mask(a)
    dbg, _ = R.debug_text_mask(a)
    bad = R.FURN | ui | dbg
    D = dipoles(a, cam, bad, step=step)
    keep = [d for d in D if d["amp"] >= min_amp]
    if len(keep) < 8:
        return None, D, keep
    m, sd, Rl = circ([d["phi"] for d in keep], [d["amp"] for d in keep])
    return {"n_seed": len(D), "n_keep": len(keep), "mean": m, "sd": sd,
            "R": Rl, "amp_med": float(np.median([d["amp"] for d in keep]))}, D, keep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", nargs="+", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--min-amp", type=float, default=0.055)
    ap.add_argument("--step", type=int, default=64)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    res = []
    for p in a.frames:
        s, D, keep = frame_azimuth(p, cam, a.min_amp, a.step)
        if s is None:
            print(f"{os.path.basename(p):>28s}  CANNOT-ANSWER  "
                  f"({len(D)} seeds, {len(keep)} above amplitude gate)")
            continue
        s["frame"] = os.path.basename(p)
        res.append(s)
        print(f"{s['frame']:>28s}  seeds {s['n_seed']:4d}  kept {s['n_keep']:4d}"
              f"  azimuth {s['mean']:+7.2f}  sd {s['sd']:6.2f}  R {s['R']:.3f}")
    if res:
        m, sd, Rl = circ([r["mean"] for r in res])
        print(f"\nacross {len(res)} frames: circular mean {m:+.2f} deg  "
              f"circular sd {sd:.2f} deg  resultant {Rl:.4f}")
    if a.out:
        json.dump(res, open(a.out, "w"))
