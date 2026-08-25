#!/usr/bin/env python3
"""gd_fit_ground_map2.py — ground-plane map by green-field consensus.

The camera is rigidly player-locked (the floating health bar sits at exactly
x[924,996] y[428,430] in every uncontaminated shot), so a single ground-plane
matrix M relates screen offset from the player to arena offset:

    arena = p_i + M^-1 . (S - P)

The green spawn fields are static world objects.  Project every shot's green
mask into arena space under a hypothesised M and the projections must AGREE.
Score = pairwise agreement rate over arena cells seen by >=2 stations:

    sum_cells G(G-1)  /  sum_cells V(V-1)

which is scale-normalised (it is a rate, not a count).  Grid-search s, sin(theta)
and yaw.  Nothing about the game's camera is assumed a priori; the search range
is deliberately wider than any plausible answer.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image

from gd_arena_trace import CAP, SHOTS
from gd_green_zones import green_mask

HERE = os.path.dirname(os.path.abspath(__file__))

P = np.array([960.0, 565.0])       # player ground anchor, screen px
WIN = (850, 620, 430)              # +-dx, -dy(up), +dy(down) around P
DS = 4                             # screen sampling stride
CELL = 2.0                         # arena grid cell, minimap px
HALF = 260                         # arena grid half-extent, minimap px
NG = int(2 * HALF / CELL)


def build_M(s, sig, phi):
    c, sn = np.cos(phi), np.sin(phi)
    return s * np.array([[c, -sn], [sig * sn, sig * c]])


def load():
    G, V = [], []
    for n in SHOTS:
        rgb = np.asarray(Image.open(
            os.path.join(CAP, f"Screenshot ({n}).png")).convert("RGB")).astype(float)
        m = green_mask(rgb)
        keep = np.zeros(m.shape, bool)
        x0, x1 = int(P[0] - WIN[0]), int(P[0] + WIN[0])
        y0, y1 = int(P[1] - WIN[1]), int(P[1] + WIN[2])
        keep[max(y0, 0):y1, max(x0, 0):x1] = True
        for hx0, hy0, hx1, hy1 in __import__("gd_green_zones").HUD:
            keep[hy0:hy1, hx0:hx1] = False
        gy, gx = np.nonzero(m & keep)
        G.append(np.c_[gx[::3], gy[::3]].astype(float) - P)
        vy, vx = np.nonzero(keep[::DS * 4, ::DS * 4])
        V.append(np.c_[vx * DS * 4, vy * DS * 4].astype(float) - P)
    return G, V


def score(M, G, V, track):
    A = np.linalg.inv(M)
    gcount = np.zeros(NG * NG, np.int32)
    vcount = np.zeros(NG * NG, np.int32)
    for i in range(len(SHOTS)):
        p = track[i]
        for src, acc in ((G[i], gcount), (V[i], vcount)):
            if len(src) == 0:
                continue
            a = src @ A.T + p
            ix = np.floor((a[:, 0] + HALF) / CELL).astype(np.int64)
            iy = np.floor((a[:, 1] + HALF) / CELL).astype(np.int64)
            ok = (ix >= 0) & (ix < NG) & (iy >= 0) & (iy < NG)
            idx = np.unique(iy[ok] * NG + ix[ok])
            acc[idx] += 1
    gg = (gcount * (gcount - 1)).sum()
    vv = (vcount * (vcount - 1)).sum()
    return (gg / vv if vv else 0.0), int(gg), int(vv)


def main():
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    track = [np.array(t) for t in meta["track"]]
    G, V = load()
    print("green sample pts/shot:", [len(g) for g in G])

    rows = []
    for s in np.arange(7.0, 25.01, 1.0):
        for sig in np.arange(0.35, 1.001, 0.05):
            for phid in np.arange(-30, 30.01, 5.0):
                M = build_M(s, sig, np.radians(phid))
                sc, gg, vv = score(M, G, V, track)
                rows.append((sc, s, sig, phid, gg, vv))
    rows.sort(reverse=True)
    print("\ntop 20 hypotheses (score, s px/mmpx, sin(theta), yaw deg):")
    for r in rows[:20]:
        print(f"  {r[0]:.4f}  s={r[1]:5.1f}  sig={r[2]:.2f} "
              f"(theta={np.degrees(np.arcsin(min(r[2],1))):4.1f})  yaw={r[3]:6.1f}  "
              f"GG={r[4]} VV={r[5]}")
    json.dump([[float(x) for x in r] for r in rows[:200]],
              open(os.path.join(HERE, "gd-ground-map-grid.json"), "w"), indent=0)


if __name__ == "__main__":
    main()
