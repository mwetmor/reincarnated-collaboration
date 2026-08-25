#!/usr/bin/env python3
"""gd_fit_ground_map.py — recover the ground-plane screen<->arena map.

Consecutive world views barely overlap (the walk steps are larger than the
viewport), so direct world-view registration fails (NCC 0.18-0.42).  The green
spawn fields are, however, large STATIC world features visible from many
stations.  If blob k in shot i and blob l in shot j are the same zone then

    S_ik - S_jl  =  M . (p_i - p_j)

with p the player's arena position (known, from the minimap registration) and M
the ground-plane matrix.  For a pinhole camera with yaw phi and pitch theta over
a level plane, M has only three free parameters:

    M = s * [[ cos phi, -sin phi ],
             [ sig*sin phi, sig*cos phi ]]        sig = sin(theta)

so a bounded grid search scored by inlier count recovers it without any
hand-authored assumption about the game's camera.
"""
from __future__ import annotations

import itertools
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_AREA = 5000
TOL_PX = 70.0          # screen-px inlier tolerance


def build_M(s, sig, phi):
    c, sn = np.cos(phi), np.sin(phi)
    return s * np.array([[c, -sn], [sig * sn, sig * c]])


def main():
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    track = {n: np.array(t) for n, t in zip(meta["shots"], meta["track"])}
    green = json.load(open(os.path.join(HERE, "gd-green-blobs.json")))
    blobs = {int(k): [np.array([b["cx"], b["cy"]]) for b in v if b["area"] >= MIN_AREA]
             for k, v in green.items()}

    pairs = []
    for i, j in itertools.combinations(sorted(blobs), 2):
        dp = track[i] - track[j]
        for a in blobs[i]:
            for b in blobs[j]:
                pairs.append((a - b, dp))
    dS = np.array([p[0] for p in pairs])
    dP = np.array([p[1] for p in pairs])
    print(f"{len(pairs)} candidate blob correspondences over "
          f"{sum(len(v) for v in blobs.values())} blobs")

    best = None
    for s in np.arange(2.0, 22.01, 0.25):
        for sig in np.arange(0.25, 1.001, 0.025):
            for phid in np.arange(-75, 75.01, 1.5):
                M = build_M(s, sig, np.radians(phid))
                r = dS - dP @ M.T
                d = np.hypot(r[:, 0], r[:, 1])
                # one inlier max per correspondence; count them
                n = int((d < TOL_PX).sum())
                if best is None or n > best[0]:
                    best = (n, s, sig, phid, float(d[d < TOL_PX].mean()) if n else 9e9)
    n, s, sig, phid, mres = best
    print(f"grid best: inliers={n}  s={s:.2f} px/mmpx  sin(theta)={sig:.3f} "
          f"(theta={np.degrees(np.arcsin(sig)):.1f} deg)  yaw={phid:.1f} deg  "
          f"mean|r|={mres:.1f}px")

    # refine on the inlier set (Gauss-Newton-free: local grid)
    for _ in range(3):
        M = build_M(s, sig, np.radians(phid))
        d = np.hypot(*(dS - dP @ M.T).T)
        inl = d < TOL_PX
        bb = None
        for ds in np.linspace(-0.4, 0.4, 17):
            for dg in np.linspace(-0.05, 0.05, 21):
                for dph in np.linspace(-3, 3, 25):
                    M2 = build_M(s + ds, sig + dg, np.radians(phid + dph))
                    r = np.hypot(*(dS[inl] - dP[inl] @ M2.T).T)
                    v = float(np.mean(np.minimum(r, TOL_PX) ** 2))
                    if bb is None or v < bb[0]:
                        bb = (v, s + ds, sig + dg, phid + dph)
        _, s, sig, phid = bb
    M = build_M(s, sig, np.radians(phid))
    d = np.hypot(*(dS - dP @ M.T).T)
    print(f"refined  : inliers={int((d<TOL_PX).sum())}  s={s:.3f}  sin(theta)={sig:.4f} "
          f"(theta={np.degrees(np.arcsin(sig)):.1f} deg)  yaw={phid:.2f} deg  "
          f"mean|r|_inl={d[d<TOL_PX].mean():.1f}px")
    print("M =", np.round(M, 4).tolist())
    U, S, Vt = np.linalg.svd(M)
    print(f"SVD singular values: {S[0]:.3f} {S[1]:.3f}   ratio={S[1]/S[0]:.4f}")
    json.dump(dict(s=s, sin_theta=sig, yaw_deg=phid, M=M.tolist(),
                   Minv=np.linalg.inv(M).tolist(),
                   sv=[float(S[0]), float(S[1])],
                   inliers=int((d < TOL_PX).sum()), n_pairs=len(pairs),
                   tol_px=TOL_PX, min_area=MIN_AREA),
              open(os.path.join(HERE, "gd-ground-map.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
