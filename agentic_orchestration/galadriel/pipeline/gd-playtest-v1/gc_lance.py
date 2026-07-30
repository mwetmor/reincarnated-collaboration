#!/usr/bin/env python3
"""GAL-CAM: per-lance tip tracks from the nova, with an ALIVE-WINDOW gate.

WHY THE GAL-3 TRACKER WAS NOT ENOUGH
------------------------------------
Most of the 16 projectiles die within a few frames (boss body, cave wall), so a
regression over the whole ring lifetime mixes a live linear track with a dead
flat one and reports a slope that is neither. Fitting bin 76 over all 51 frames
gives 11.1 px/frame; fitting it over the frames where it is actually ALIVE gives
13.9. The difference is not noise, it is a modelling error.

So: per azimuth bin, find the LONGEST CONTIGUOUS RUN of frames whose tip radius
is linear in frame number to within a few px, and use only that run. A bin whose
lance died at frame 20 contributes 20 frames of good data instead of 51 frames
of bad data.

The tip itself is the RADIAL MAXIMUM of the cold-head mask in that azimuth bin:
trails lie inside the tip by construction and therefore cannot inflate it.

OUTPUT: per lance, the screen track (f, x, y). Ground azimuths are NOT assigned
here -- that is gc_ring.py's job, and it needs the camera shape first.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


def cold_mask(a, bmin=150, brmin=60, gtol=12):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (B > bmin) & ((B - R) > brmin) & (B >= G - gtol)


def envelope(f, cx, cy, nbin, rmin, rmax, bright, ytop, ybot):
    a = np.asarray(Image.open(os.path.join(FRAMES, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    m = cold_mask(a) & (a[:, :, 2] > bright)
    m[:ytop] = False
    m[ybot:] = False
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    dx, dy = xs - cx, ys - cy
    r = np.hypot(dx, dy)
    keep = (r >= rmin) & (r <= rmax)
    if not keep.any():
        return None
    dx, dy, r, xs, ys = dx[keep], dy[keep], r[keep], xs[keep], ys[keep]
    th = np.arctan2(dy, dx) % (2 * math.pi)
    b = np.floor(th / (2 * math.pi) * nbin).astype(int) % nbin
    out = np.full((nbin, 3), np.nan)
    o = np.argsort(r)
    out[b[o], 0] = r[o]
    out[b[o], 1] = xs[o]
    out[b[o], 2] = ys[o]
    return out


def longest_linear_run(fs, rs, tol, minlen, smin, smax):
    best = None
    n = len(fs)
    for i in range(n):
        for j in range(n - 1, i + minlen - 2, -1):
            if best and (j - i + 1) <= best[1] - best[0]:
                break
            x = fs[i:j + 1]; y = rs[i:j + 1]
            A = np.vstack([x - x.mean(), np.ones(len(x))]).T
            co, *_ = np.linalg.lstsq(A, y, rcond=None)
            res = y - A @ co
            if np.abs(res).max() <= tol and smin <= co[0] <= smax:
                best = (i, j, float(co[0]))
                break
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309086)
    ap.add_argument("--f1", type=int, default=309140)
    ap.add_argument("--cx", type=float, default=1024.7)
    ap.add_argument("--cy", type=float, default=568.5)
    ap.add_argument("--nbin", type=int, default=180)
    ap.add_argument("--rmin", type=float, default=25)
    ap.add_argument("--rmax", type=float, default=900)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--tol", type=float, default=5.0)
    ap.add_argument("--minlen", type=int, default=9)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    frames = [f for f in range(args.f0, args.f1 + 1)
              if os.path.exists(os.path.join(FRAMES, f"f{f:06d}.png"))]
    E = {}
    for f in frames:
        e = envelope(f, args.cx, args.cy, args.nbin, args.rmin, args.rmax,
                     args.bright, 30, 940)
        if e is not None:
            E[f] = e

    binruns = []
    for b in range(args.nbin):
        fs, rs, xs, ys = [], [], [], []
        for f in frames:
            e = E.get(f)
            if e is None or np.isnan(e[b, 0]):
                continue
            fs.append(f); rs.append(e[b, 0]); xs.append(e[b, 1]); ys.append(e[b, 2])
        if len(fs) < args.minlen:
            continue
        fs = np.array(fs, float); rs = np.array(rs)
        xs = np.array(xs); ys = np.array(ys)
        run = longest_linear_run(fs, rs, args.tol, args.minlen, 2.0, 22.0)
        if not run:
            continue
        i, j, sl = run
        binruns.append(dict(bin=b, th=(b + 0.5) * 360.0 / args.nbin,
                            n=j - i + 1, slope=sl,
                            f=fs[i:j + 1].tolist(), x=xs[i:j + 1].tolist(),
                            y=ys[i:j + 1].tolist()))
    binruns.sort(key=lambda d: d["bin"])
    print(f"{len(binruns)} bins with a linear run")

    # group adjacent bins into lances; keep the bin with the longest run
    groups, cur = [], []
    for r in binruns:
        if cur and r["bin"] - cur[-1]["bin"] <= 2:
            cur.append(r)
        else:
            if cur:
                groups.append(cur)
            cur = [r]
    if cur:
        groups.append(cur)
    if len(groups) > 1 and (binruns[0]["bin"] + args.nbin - binruns[-1]["bin"]) <= 2:
        groups[0] = groups.pop() + groups[0]

    lances = []
    for g in groups:
        best = max(g, key=lambda d: (d["n"], -abs(d["bin"] - np.mean([q["bin"] for q in g]))))
        best = dict(best)
        best["nbins"] = len(g)
        lances.append(best)
    lances.sort(key=lambda d: d["th"])
    for L in lances:
        print(f"  th={L['th']:7.2f} bins={L['nbins']:2d} n={L['n']:3d} "
              f"slope={L['slope']:6.2f} f[{L['f'][0]:.0f}-{L['f'][-1]:.0f}] "
              f"x[{L['x'][0]:.0f}->{L['x'][-1]:.0f}] y[{L['y'][0]:.0f}->{L['y'][-1]:.0f}]")
    json.dump(dict(args=vars(args), lances=lances), open(args.out, "w"), indent=1)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
