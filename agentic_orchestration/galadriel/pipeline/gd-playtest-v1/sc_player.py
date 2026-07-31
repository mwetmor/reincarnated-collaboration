#!/usr/bin/env python3
"""SHADOW-CAL instrument SC-8: the player's cast shadow, every clean keyframe.

SC-6 proved the measurement works when a human points at the shadow.  The
player, however, does not need pointing at: GAL-CAM MEASURED his screen anchor
at (962, 595), and the camera is hard-locked to him.  So SC-8 plants EIGHT
candidate seeds on a ring around that anchor -- one every 45 degrees of GROUND
azimuth, so no direction is favoured -- segments a dark blob from each, and
keeps the darkest one that survives the guards.

GUARDS (each one exists because of a way this went wrong):
  * chroma guard - a cast shadow is the same ground multiplied down, so its
    chroma/luma ratio matches the surrounding floor.  A sprite does not.  This
    is what stops a seed that landed on the werewolf from being reported as its
    own shadow.
  * fill guard   - a blob that fills its search disc is not a shadow, it is the
    segmenter failing on fogged low-contrast ground (the first SC-6 tuning did
    exactly this and the overlay is kept).
  * depth guard  - rho must actually be below the floor by a stated margin.
  * UI guard     - frames with panels open are dropped, not measured around.

The azimuth is measured from the ANCHOR to the blob's far tip on the GROUND
PLANE.  Up-screen azimuths remain the weak axis (the sprite is drawn above its
own contact point); the chroma guard is what keeps that from silently becoming
the answer, and the residual risk is declared rather than corrected.
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

ANCHOR = (962.0, 595.0)
SEED_R_M = 1.35
NSEED = 8
DISC_R_M = 1.7


def chroma_luma(a, m):
    c = a[..., :3].max(-1) - a[..., :3].min(-1)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    return float(np.median(c[m])), float(np.median(L[m]))


def one_frame(arr, cam, k_shadow=0.82, min_px=350, max_fill=0.62,
              chroma_tol=0.60):
    a = np.asarray(arr, np.float32)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    ui, uifrac = R.ui_mask(a)
    if uifrac > 0.0030:
        return None, "ui"
    g0 = cam.unproject_ground([[ANCHOR[0], ANCHOR[1]]])
    base = np.array([float(g0[0]), float(g0[2])])
    best = None
    for i in range(NSEED):
        th = 2 * math.pi * i / NSEED
        P = np.array([[base[0] + SEED_R_M * math.cos(th), 0.0,
                       base[1] + SEED_R_M * math.sin(th)]])
        uv = cam.project(P)
        cx, cy = float(uv[0]), float(uv[1])
        if not (40 < cx < 1880 and 170 < cy < 930):
            continue
        p1 = cam.project(np.array([[base[0] + DISC_R_M, 0.0, base[1]]]))
        r_px = float(abs(p1[0] - ANCHOR[0]))
        yy, xx = np.ogrid[:L.shape[0], :L.shape[1]]
        d2 = (xx - cx) ** 2 + (yy - cy) ** 2
        disc = d2 <= r_px ** 2
        ann = (d2 >= (1.25 * r_px) ** 2) & (d2 <= (2.3 * r_px) ** 2) & ~ui
        if ann.sum() < 900:
            continue
        floor = float(np.median(L[ann]))
        if floor < 8:
            continue
        dark = (L < k_shadow * floor) & disc & ~ui
        dark = ndimage.binary_opening(dark, np.ones((3, 3)))
        lab, n = ndimage.label(dark)
        if n == 0:
            continue
        sid = lab[int(round(cy)), int(round(cx))]
        if sid == 0:
            continue
        m = lab == sid
        npx = int(m.sum())
        if npx < min_px or npx / max(disc.sum(), 1) > max_fill:
            continue
        # SPRITE-EXCLUSION GUARD.  The chroma test alone did NOT hold: visual
        # verification of the first SC-8 pass showed blobs covering the
        # character itself (evidence/sc8-verification-v1.jpg, kept).  The
        # character is drawn in a known box above its own ground contact, so a
        # blob that covers that box is the character, not its shadow.
        torso = np.zeros(L.shape, bool)
        torso[int(ANCHOR[1]) - 105:int(ANCHOR[1]) - 30,
              int(ANCHOR[0]) - 48:int(ANCHOR[0]) + 48] = True
        if (m & torso).sum() > 0.18 * torso.sum():
            continue
        # and the blob must sit clear of the contact point on the ground
        ysq, xsq = np.nonzero(m)
        gq = cam.unproject_ground(np.stack([xsq, ysq], 1).astype(float))
        if np.hypot(*(gq[:, [0, 2]].mean(0) - base)) < 0.85:
            continue
        cs, Ls = chroma_luma(a, m)
        ca, La = chroma_luma(a, ann)
        if La <= 0 or Ls <= 0:
            continue
        rat_s, rat_a = cs / Ls, ca / La
        if abs(rat_s - rat_a) > chroma_tol * max(rat_a, 1e-6):
            continue
        rho = Ls / floor
        if rho > 0.86:
            continue
        ys, xs = np.nonzero(m)
        gg = cam.unproject_ground(np.stack([xs, ys], 1).astype(float))
        d = gg[:, [0, 2]] - base
        rad = np.hypot(d[:, 0], d[:, 1])
        tip = d[rad >= np.quantile(rad, 0.99)].mean(0)
        cen = d.mean(0)
        rec = {"seed_i": i, "px": npx, "rho": rho, "floor": floor,
               "L_shadow": Ls, "len_m": float(np.hypot(*tip)),
               "az": float(math.degrees(math.atan2(tip[1], tip[0]))),
               "az_cen": float(math.degrees(math.atan2(cen[1], cen[0]))),
               "cen_len_m": float(np.hypot(*cen)),
               "chroma_ratio_shadow": rat_s, "chroma_ratio_floor": rat_a}
        if best is None or rec["rho"] < best["rho"]:
            best = rec
    return best, (None if best else "no-blob")


def circ(deg, w=None):
    A = np.radians(np.asarray(deg, float))
    w = np.ones_like(A) if w is None else np.asarray(w, float)
    C = (w * np.cos(A)).sum() / w.sum()
    S = (w * np.sin(A)).sum() / w.sum()
    Rl = math.hypot(C, S)
    return (math.degrees(math.atan2(S, C)),
            math.degrees(math.sqrt(-2 * math.log(Rl))) if Rl > 1e-9 else float("nan"),
            Rl)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--fps", type=float, default=60.0)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    files = sorted(f for f in os.listdir(a.dir) if f.endswith(".jpg"))
    if a.limit:
        files = files[:: max(1, len(files) // a.limit)]
    rec, why = [], {}
    for f in files:
        arr = np.asarray(Image.open(os.path.join(a.dir, f)).convert("RGB"))
        r, reason = one_frame(arr, cam)
        if r is None:
            why[reason] = why.get(reason, 0) + 1
            continue
        r["frame"] = int(f[1:-4])
        r["t"] = r["frame"] / a.fps
        r["file"] = f
        rec.append(r)
    json.dump(rec, open(a.out, "w"))
    print(f"frames examined {len(files)}   measured {len(rec)}   rejected {why}")
    if rec:
        az = [r["az"] for r in rec]
        m, sd, Rl = circ(az)
        print(f"  azimuth circular mean {m:+.2f} deg  circular sd {sd:.2f}  R {Rl:.4f}")
        rho = np.array([r["rho"] for r in rec])
        fl = np.array([r["floor"] for r in rec])
        print(f"  rho median {np.median(rho):.3f}  IQR "
              f"{np.percentile(rho,25):.3f}-{np.percentile(rho,75):.3f}")
        print(f"  floor luma median {np.median(fl):.1f}")
