#!/usr/bin/env python3
"""gd_footprint_vote.py — arena footprint by per-shot vote, not by mosaic threshold.

Thresholding the MEDIAN mosaic leaks: the GD minimap disc is semi-transparent and
the world bleeding through it is warm stone, which scores like mapped terrain.
The bleed is however DIFFERENT in every shot (it is the live view, and the player
moved), whereas the mapped-terrain overlay is identical in every shot that sees
that arena pixel.  So: classify inside each shot independently, register, and
take the per-pixel agreement rate.  p = votes/observations is ~1 on real terrain
and low on bleed.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image

import gd_arena_mosaic as MO
from gd_arena_trace import CAP, SHOTS

HERE = os.path.dirname(os.path.abspath(__file__))
T_SHOT = 26.0          # per-shot terrain score threshold
P_MIN = 0.62           # agreement rate required to call a pixel terrain


def main():
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    W, H, ox, oy = meta["W"], meta["H"], meta["ox"], meta["oy"]
    track = meta["track"]
    votes = np.zeros((H, W), np.int32)
    obs = np.zeros((H, W), np.int32)
    for i, n in enumerate(SHOTS):
        sub, m, dx, dy = MO.disc_rgb(os.path.join(CAP, f"Screenshot ({n}).png"))
        sc = sub.mean(axis=2) + 1.5 * (sub[:, :, 0] - sub[:, :, 2])
        px = np.round(track[i][0] + ox + dx).astype(int)
        py = np.round(track[i][1] + oy + dy).astype(int)
        ok = m & (px >= 0) & (px < W) & (py >= 0) & (py < H)
        np.add.at(obs, (py[ok], px[ok]), 1)
        t = ok & (sc > T_SHOT)
        np.add.at(votes, (py[t], px[t]), 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = np.where(obs > 0, votes / np.maximum(obs, 1), 0.0)
    np.save(os.path.join(HERE, "gd-footprint-p.npy"), p)
    np.save(os.path.join(HERE, "gd-footprint-obs.npy"), obs)
    for thr in (0.5, 0.62, 0.7, 0.8):
        print(f"p>{thr}: {int(((p > thr) & (obs >= 2)).sum())} px")
    hist, edges = np.histogram(p[obs >= 3], bins=20, range=(0, 1))
    for i in range(20):
        print(f"  p {edges[i]:.2f}-{edges[i+1]:.2f}: {hist[i]:6d} " + "#" * int(hist[i] / 500))
    img = np.clip(p * 255, 0, 255).astype(np.uint8)
    Image.fromarray(img).resize((W * 3, H * 3), Image.NEAREST).save(
        os.path.join(HERE, "gd-footprint-p.png"))


if __name__ == "__main__":
    main()
