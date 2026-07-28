#!/usr/bin/env python3
"""
G-6 pass 7: enumerate every skill-node RANK COUNTER ("N / M") in the mastery
panel, and crop each one for reading.

Why this and not the tooltips: the tooltip moves with the cursor (three
locator attempts failed to pin it reliably), but the TREE is position-fixed and
every reachable node renders its counter in near-white text under the icon.
Detecting the counters directly gives the whole allocation in one pass.

Occlusion handling: the tooltip covers part of the tree in any single frame, so
counters are detected independently in EVERY frame of a burst and the results
unioned by position. A counter hidden behind the tooltip in one frame is
exposed in another, because Matt hovered a different node in each.

Detection: near-white ink mask -> horizontal dilation to join "N", "/", "M"
into one blob -> connected components -> keep blobs of counter-like size and
aspect. Every kept blob is written as an 8x crop named by its native box.
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
CNT = OUT / "counters"

PANEL = (455, 245, 1530, 880)
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def white_ink(rgb):
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    return (r > 165) & (g > 160) & (b > 150)


def detect(fid):
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        rgb = np.asarray(im.convert("RGB"))
    x0, y0, x1, y1 = PANEL
    m = white_ink(rgb[y0:y1, x0:x1])
    d = ndimage.binary_dilation(m, structure=np.ones((1, 9)))
    d = ndimage.binary_dilation(d, structure=np.ones((3, 1)))
    lab, n = ndimage.label(d)
    out = []
    for sl in ndimage.find_objects(lab):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (9 <= h <= 26):
            continue
        if not (22 <= w <= 95):
            continue
        ink = m[sl].sum()
        if ink < 40:
            continue
        out.append((x0 + sl[1].start - 5, y0 + sl[0].start - 4,
                    x0 + sl[1].stop + 5, y0 + sl[0].stop + 4, int(ink)))
    return out, rgb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--tag", default="burst")
    ap.add_argument("--scale", type=int, default=7)
    a = ap.parse_args()
    CNT.mkdir(parents=True, exist_ok=True)
    fids = [int(v) for v in a.frames.split(",")]
    slots = []       # canonical positions, (cx, cy)
    picks = {}       # slot index -> (frame, box)
    for f in fids:
        boxes, rgb = detect(f)
        for (bx0, by0, bx1, by1, ink) in boxes:
            cx, cy = (bx0 + bx1) // 2, (by0 + by1) // 2
            hit = None
            for i, (sx, sy) in enumerate(slots):
                if abs(sx - cx) <= 22 and abs(sy - cy) <= 12:
                    hit = i
                    break
            if hit is None:
                slots.append((cx, cy))
                hit = len(slots) - 1
            # prefer the widest detection (least occluded)
            prev = picks.get(hit)
            if prev is None or (bx1 - bx0) > (prev[1][2] - prev[1][0]):
                picks[hit] = (f, (bx0, by0, bx1, by1))
    order = sorted(picks, key=lambda i: (slots[i][1] // 40, slots[i][0]))
    print(f"{len(order)} counter slots across frames {fids}")
    font = ImageFont.truetype(FONT, 24)
    tiles = []
    rec = {}
    for k, i in enumerate(order):
        f, box = picks[i]
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            c = im.convert("RGB").crop(box)
        c.save(CNT / f"{a.tag}_slot{k:02d}_f{f}_{box[0]}-{box[1]}_native.png")
        up = c.resize((c.width * a.scale, c.height * a.scale), Image.LANCZOS)
        tiles.append((k, f, box, up))
        rec[k] = {"frame": f, "box": list(box), "centre": list(slots[i])}
        print(f"  slot{k:02d}  f{f}  box={box}")
    lw = 420
    w = lw + max(t[3].width for t in tiles)
    h = sum(t[3].height + 10 for t in tiles)
    sheet = Image.new("RGB", (w, h), (10, 10, 12))
    d = ImageDraw.Draw(sheet)
    y = 0
    for k, f, box, up in tiles:
        d.text((6, y + up.height // 2 - 12),
               f"s{k:02d} f{f} @({box[0]},{box[1]})", fill=(255, 235, 130), font=font)
        sheet.paste(up, (lw, y))
        y += up.height + 10
    sheet.save(CNT / f"SHEET_{a.tag}.png")
    json.dump(rec, open(CNT / f"{a.tag}-slots.json", "w"), indent=1)
    print(CNT / f"SHEET_{a.tag}.png")


if __name__ == "__main__":
    main()
