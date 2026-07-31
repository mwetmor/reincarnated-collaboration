#!/usr/bin/env python3
"""SHADOW-CAL: world-registered background plate (streaming).

The GD camera translates without rotation or zoom (GAL-CAM: roll 0 +-3 deg,
zoom flat to +-10%), so the ground moves under a pure screen shift.  Registering
every frame of a burst onto a reference lets the temporal median be taken IN
WORLD COORDINATES -- which is what makes a plate valid while the player walks
past a torch, and what makes "the same floor pixels, unshadowed" a thing that
exists.

THREE DISCIPLINES BUILT IN
--------------------------
1. CONSECUTIVE registration, cumulated.  Frame i is registered to frame i-1, not
   to a distant reference: a 1 px problem instead of a 100 px one.  A direct
   ref-to-frame correlation is then run on a subset as a CONTROL and the
   disagreement is reported, not assumed away.
2. PATCH QUORUM.  47 patches of ground vote.  A patch whose correlation peak is
   weak ABSTAINS -- in a cave most of the frame is featureless fog, and a
   textureless patch returns a confident-looking peak at a random offset.  A
   frame is accepted only if enough voting patches agree.  Abstention and
   rejection are counted separately: an instrument that cannot see is not an
   instrument that measured zero.
3. TEMPORAL MAD.  Alongside the median plate, the per-pixel median absolute
   deviation of the registered stack -- the instrument's own noise floor.
   Swaying grass, animated water and flickering firelight are all restless; a
   change mask that ignores that reads foliage as an actor and flicker as a
   shadow.  (This cell hit exactly that failure on its first pass; the mask is
   kept in the evidence directory.)
"""
import argparse
import os

import numpy as np
from PIL import Image
from scipy import ndimage

FURNITURE_BOXES = [
    (0, 0, 1920, 150),        # top nameplate / floating text band
    (0, 0, 430, 175),         # top-left debug labels
    (1020, 0, 1570, 520),     # Play Statistics + quest log
    (1540, 0, 1920, 200),     # minimap
    (0, 940, 1920, 1080),     # bottom HUD
    (780, 390, 1170, 780),    # the player and its debug label
]
PATCH = 192
PATCH_STEP = 112
PEAK_MIN = 0.12
TOL = 1.2
QUORUM = 3


def _patches():
    out = []
    for y in range(150, 940 - PATCH + 1, PATCH_STEP):
        for x in range(0, 1920 - PATCH + 1, PATCH_STEP):
            bx0, by0, bx1, by1 = x, y, x + PATCH, y + PATCH
            if any(bx0 < fx1 and fx0 < bx1 and by0 < fy1 and fy0 < by1
                   for fx0, fy0, fx1, fy1 in FURNITURE_BOXES):
                continue
            out.append((slice(by0, by1), slice(bx0, bx1)))
    return out


PATCHES = _patches()
_WIN = np.outer(np.hanning(PATCH), np.hanning(PATCH))


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def read(p):
    return np.asarray(Image.open(p).convert("RGB"), np.uint8)


def _pc(a, b, maxshift=48):
    a = (a - a.mean()) * _WIN
    b = (b - b.mean()) * _WIN
    A = np.fft.rfft2(a)
    B = np.fft.rfft2(b)
    R = A * np.conj(B)
    m = np.abs(R)
    R = np.where(m > 1e-9, R / m, 0)
    c = np.fft.fftshift(np.fft.irfft2(R, s=a.shape))
    cy, cx = a.shape[0] // 2, a.shape[1] // 2
    r = min(maxshift, cy - 1, cx - 1)
    sub = c[cy - r:cy + r + 1, cx - r:cx + r + 1]
    i0, j0 = np.unravel_index(np.argmax(sub), sub.shape)
    pk = float(sub[i0, j0])
    fy = fx = 0.0
    if 0 < i0 < sub.shape[0] - 1:
        a1, a2, a3 = sub[i0 - 1, j0], sub[i0, j0], sub[i0 + 1, j0]
        d = a1 - 2 * a2 + a3
        if abs(d) > 1e-12:
            fy = float(np.clip(0.5 * (a1 - a3) / d, -1, 1))
    if 0 < j0 < sub.shape[1] - 1:
        a1, a2, a3 = sub[i0, j0 - 1], sub[i0, j0], sub[i0, j0 + 1]
        d = a1 - 2 * a2 + a3
        if abs(d) > 1e-12:
            fx = float(np.clip(0.5 * (a1 - a3) / d, -1, 1))
    return (i0 - r) + fy, (j0 - r) + fx, pk


def patchset(L):
    return [np.ascontiguousarray(L[sl], np.float32) for sl in PATCHES]


def consensus(pa, pb, maxshift=48, tol=TOL, quorum=QUORUM):
    votes = []
    nab = 0
    for a, b in zip(pa, pb):
        dy, dx, pk = _pc(a, b, maxshift)
        if pk >= PEAK_MIN:
            votes.append((dy, dx))
        else:
            nab += 1
    if len(votes) < quorum:
        return None, len(votes), nab
    v = np.array(votes)
    med = np.median(v, axis=0)
    keep = v[(np.abs(v - med) <= tol).all(1)]
    if len(keep) < quorum:
        return None, len(votes), nab
    return tuple(np.median(keep, axis=0)), len(votes), nab


def register(paths, ref=None, control_every=20):
    """Cumulative consecutive registration + a direct-to-ref control."""
    n = len(paths)
    ref = n // 2 if ref is None else ref
    P_prev = None
    ref_patches = None
    step = np.full((n, 2), np.nan)
    diag = {"n_patches": len(PATCHES), "abstain": [], "voting": []}
    for i in range(n):
        L = luma(read(paths[i]).astype(np.float32))
        ps = patchset(L)
        if i == 0:
            step[0] = (0.0, 0.0)
        else:
            s, nv, nab = consensus(P_prev, ps)
            step[i] = s if s is not None else (np.nan, np.nan)
            diag["voting"].append(nv)
            diag["abstain"].append(nab)
        P_prev = ps
        if i == ref:
            ref_patches = ps
    cum = np.zeros((n, 2))
    ok = np.ones(n, bool)
    acc = np.zeros(2)
    for i in range(n):
        if i and not np.isfinite(step[i]).all():
            ok[i:] = False
            break
        acc = acc + (step[i] if i else np.zeros(2))
        cum[i] = acc
    shifts = np.where(ok[:, None], cum - cum[ref], np.nan)

    ctrl = []
    if ref_patches is not None:
        for i in range(0, n, control_every):
            if not ok[i] or i == ref:
                continue
            L = luma(read(paths[i]).astype(np.float32))
            s, nv, nab = consensus(ref_patches, patchset(L), maxshift=90)
            if s is not None:
                ctrl.append((i, float(shifts[i][0] - s[0]),
                             float(shifts[i][1] - s[1])))
    diag["control"] = ctrl
    if ctrl:
        e = np.array([[c[1], c[2]] for c in ctrl])
        diag["control_rms_px"] = float(np.sqrt((e ** 2).sum(1).mean()))
        diag["control_max_px"] = float(np.abs(e).max())
    return shifts, ref, diag


def warp_u8(img_u8, dy, dx, order=1):
    if abs(dy) < 1e-6 and abs(dx) < 1e-6:
        return img_u8.copy(), np.ones(img_u8.shape[:2], bool)
    out = np.empty(img_u8.shape, np.float32)
    for c in range(3):
        out[..., c] = ndimage.shift(img_u8[..., c].astype(np.float32),
                                    (-dy, -dx), order=order,
                                    mode="constant", cval=-1.0)
    v = out.min(-1) >= -0.5
    return np.clip(out, 0, 255).astype(np.uint8), v


def build(paths, shifts, min_samples=15, band=120):
    """Streaming world-registered median plate + temporal MAD."""
    good = [i for i in range(len(paths)) if np.isfinite(shifts[i]).all()]
    h, w = 1080, 1920
    acc = np.zeros((len(good), h, w, 3), np.uint8)
    vmask = np.zeros((len(good), h, w), bool)
    for k, i in enumerate(good):
        im = read(paths[i])
        acc[k], vmask[k] = warp_u8(im, float(shifts[i][0]), float(shifts[i][1]))
    cnt = vmask.sum(0)
    plate = np.zeros((h, w, 3), np.float32)
    sigma = np.zeros((h, w), np.float32)
    for y0 in range(0, h, band):
        y1 = min(h, y0 + band)
        a = acc[:, y0:y1].astype(np.float32)
        a[~vmask[:, y0:y1]] = np.nan
        with np.errstate(all="ignore"):
            p = np.nanmedian(a, axis=0)
            L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
            Lp = 0.2126 * p[..., 0] + 0.7152 * p[..., 1] + 0.0722 * p[..., 2]
            s = 1.4826 * np.nanmedian(np.abs(L - Lp[None]), axis=0)
        plate[y0:y1] = np.nan_to_num(p)
        sigma[y0:y1] = np.nan_to_num(s)
        del a, L
    valid = cnt >= min_samples
    return plate, sigma, cnt, valid, good, acc, vmask


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    paths = sorted(os.path.join(a.dir, f) for f in os.listdir(a.dir)
                   if f.endswith((".png", ".jpg")))
    sh, ref, diag = register(paths)
    plate, sigma, cnt, valid, good, acc, vm = build(paths, sh)
    print(f"{len(paths)} frames, ref {ref}; usable {len(good)} "
          f"({100*len(good)/len(paths):.0f}%)")
    print(f"  patches {diag['n_patches']}; voting median "
          f"{np.median(diag['voting']):.0f}, abstaining median "
          f"{np.median(diag['abstain']):.0f}")
    if "control_rms_px" in diag:
        print(f"  CONTROL cumulative-vs-direct registration: rms "
              f"{diag['control_rms_px']:.3f} px, max {diag['control_max_px']:.3f} px "
              f"(n={len(diag['control'])})")
    fin = sh[np.isfinite(sh[:, 0])]
    print(f"  camera travel dy {fin[:,0].min():.1f}..{fin[:,0].max():.1f}, "
          f"dx {fin[:,1].min():.1f}..{fin[:,1].max():.1f} px")
    print(f"  plate valid {100*valid.mean():.1f}%;  temporal MAD median "
          f"{np.median(sigma[valid]):.2f} luma, p95 {np.percentile(sigma[valid],95):.2f}")
    if a.out:
        v = plate.copy()
        v[~valid] = 0
        Image.fromarray(v.astype(np.uint8)).save(a.out, quality=92)
        print("  ->", a.out)
