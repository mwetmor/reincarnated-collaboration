#!/usr/bin/env python3
"""
G-6 pass 9: find the HOVERED node per frame, and pair it with its tooltip.

A hovered skill node in the GD mastery panel is drawn with a bright orange
highlight ring / box that nothing else in the panel carries. Detecting it gives
the node's position; the tooltip visible in that same frame therefore names and
ranks THAT node. This is what converts a pile of tooltips into a position->skill
map, which is what the rank table needs.

Also emits, per frame, a crop of the hovered node + its counter, so the node's
own "N / M" can be read next to the tooltip that names it.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
HOV = OUT / "hover"
PANEL = (455, 250, 1530, 878)
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def hover_mask(rgb):
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    return (r > 195) & (g > 120) & (g < 205) & (b < 95) & (r - b > 120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--scale", type=int, default=5)
    a = ap.parse_args()
    HOV.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = PANEL
    font = ImageFont.truetype(FONT, 24)
    res = {}
    tiles = []
    for f in (int(v) for v in a.frames.split(",")):
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            rgb = np.asarray(im.convert("RGB"))
        m = hover_mask(rgb[y0:y1, x0:x1])
        m = ndimage.binary_closing(m, np.ones((3, 3)))
        lab, n = ndimage.label(m)
        best, bestsz = None, 0
        for i, sl in enumerate(ndimage.find_objects(lab), start=1):
            h = sl[0].stop - sl[0].start
            w = sl[1].stop - sl[1].start
            if not (24 <= h <= 90 and 24 <= w <= 90):
                continue
            sz = int((lab[sl] == i).sum())
            if sz > bestsz:
                bestsz, best = sz, (x0 + sl[1].start, y0 + sl[0].start,
                                    x0 + sl[1].stop, y0 + sl[0].stop)
        res[str(f)] = {"hover_box": list(best) if best else None, "px": bestsz}
        print(f"f{f}: hover={best} px={bestsz}")
        if best:
            cb = (best[0] - 30, best[1] - 8, best[2] + 30, best[3] + 34)
            c = Image.fromarray(rgb[cb[1]:cb[3], cb[0]:cb[2]])
            c.save(HOV / f"hover_f{f}_native.png")
            up = c.resize((c.width * a.scale, c.height * a.scale), Image.LANCZOS)
            tiles.append((f, best, up))
    if tiles:
        lw = 420
        w = lw + max(t[2].width for t in tiles)
        h = sum(t[2].height + 10 for t in tiles)
        sheet = Image.new("RGB", (w, h), (10, 10, 12))
        d = ImageDraw.Draw(sheet)
        y = 0
        for f, box, up in tiles:
            d.text((6, y + up.height // 2 - 12), f"f{f} node@({box[0]},{box[1]})",
                   fill=(255, 235, 130), font=font)
            sheet.paste(up, (lw, y))
            y += up.height + 10
        sheet.save(HOV / "SHEET_hover.png")
        print(HOV / "SHEET_hover.png")
    json.dump(res, open(OUT / "g6-hover.json", "w"), indent=1)


if __name__ == "__main__":
    main()
