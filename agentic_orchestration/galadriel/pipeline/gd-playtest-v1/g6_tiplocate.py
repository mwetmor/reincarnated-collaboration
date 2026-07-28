#!/usr/bin/env python3
"""
G-6 pass 6: locate the skill tooltip per frame, then emit a readable crop.

The GD skill tooltip is a near-black box with a thin gold ornamental border and
it renders ADJACENT TO THE HOVERED NODE, so its screen position varies frame to
frame -- a fixed box (pass 3) captures the tree in some frames and the tooltip
in others. This locator finds the box instead of assuming it:

  gold-border mask -> columns with a tall vertical run -> the two dominant
  columns bound the tooltip; rows likewise. Falls back to a wide default when
  the border is occluded.

Emits <tag>_f<id>_tip_x3.png per frame plus a JSON of located boxes.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
TIP = OUT / "tooltips"

SEARCH = (300, 190, 1600, 900)   # native search window


def gold_mask(rgb):
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    return (r > 110) & (r < 235) & (g > 90) & (g < 210) & (b < 130) & (r - b > 45) & (g - b > 25)


def locate(fid):
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        rgb = np.asarray(im.convert("RGB"))
    x0, y0, x1, y1 = SEARCH
    sub = rgb[y0:y1, x0:x1]
    m = gold_mask(sub)
    colcount = m.sum(axis=0)
    rowcount = m.sum(axis=1)
    # a tooltip border column runs most of the box height; require >= 120 px
    cols = np.where(colcount >= 120)[0]
    rows = np.where(rowcount >= 140)[0]
    if len(cols) < 2 or len(rows) < 2:
        return None
    cx0, cx1 = int(cols.min()), int(cols.max())
    ry0, ry1 = int(rows.min()), int(rows.max())
    if cx1 - cx0 < 200 or ry1 - ry0 < 150:
        return None
    return (x0 + cx0 - 6, y0 + ry0 - 6, x0 + cx1 + 8, y0 + ry1 + 8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--scale", type=int, default=3)
    a = ap.parse_args()
    TIP.mkdir(parents=True, exist_ok=True)
    boxes = {}
    for f in (int(v) for v in a.frames.split(",")):
        box = locate(f)
        boxes[f] = box
        print(f"f{f}: {box}")
        if box is None:
            continue
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            c = im.convert("RGB").crop(box)
        c.save(TIP / f"LOC_f{f}_native.png")
        c.resize((c.width * a.scale, c.height * a.scale), Image.LANCZOS).save(
            TIP / f"LOC_f{f}_x{a.scale}.png")
    json.dump({str(k): v for k, v in boxes.items()},
              open(OUT / "g6-tooltip-boxes.json", "w"), indent=1)


if __name__ == "__main__":
    main()
