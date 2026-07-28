#!/usr/bin/env python3
"""
G-6 pass 6b: locate the skill tooltip by its TEXT BLOCK, not its border.

Pass 6a failed because the mastery panel's own ornamental frame is the same
gold as the tooltip's, so the border mask always returned the whole panel.

The tooltip is the only object inside the panel that contains a tall, dense,
LEFT-ALIGNED block of near-white body text (the tree carries only short
"N / M" counters). So: mask near-white text, take per-column counts over the
panel band, and find the widest contiguous run of columns whose count clears a
floor. That run's x-extent is the tooltip; rows are then bounded the same way
inside it.

Reported with a `quality` field: LOCATED (clean run >= 180 px wide) or
WIDE_FALLBACK. Anything not LOCATED is read at reduced confidence.
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

BAND = (455, 250, 1525, 875)     # panel interior, native
COL_FLOOR = 12                   # text pixels in a column to count as "text"


def text_mask(rgb):
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    return (r > 140) & (g > 135) & (b > 120)


def longest_run(flags):
    best = (0, 0, 0)
    s = None
    for i, v in enumerate(list(flags) + [False]):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s > best[0]:
                best = (i - s, s, i - 1)
            s = None
    return best


def locate(fid):
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        rgb = np.asarray(im.convert("RGB"))
    x0, y0, x1, y1 = BAND
    m = text_mask(rgb[y0:y1, x0:x1])
    col = m.sum(axis=0)
    # allow single-column dropouts inside the block
    flags = col >= COL_FLOOR
    for i in range(1, len(flags) - 1):
        if not flags[i] and flags[i - 1] and flags[i + 1]:
            flags[i] = True
    w, cs, ce = longest_run(flags)
    quality = "LOCATED" if w >= 180 else "WIDE_FALLBACK"
    if quality == "WIDE_FALLBACK":
        return None, quality, w
    sub = m[:, cs:ce + 1]
    row = sub.sum(axis=1)
    rf = row >= 3
    rw, rs, re = longest_run(rf)
    box = (x0 + cs - 14, y0 + rs - 16, x0 + ce + 16, y0 + re + 14)
    return box, quality, w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--scale", type=int, default=3)
    a = ap.parse_args()
    TIP.mkdir(parents=True, exist_ok=True)
    res = {}
    for f in (int(v) for v in a.frames.split(",")):
        box, q, w = locate(f)
        res[str(f)] = {"box": box, "quality": q, "run_px": int(w)}
        print(f"f{f}: {q} run={w} box={box}")
        if box is None:
            continue
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            c = im.convert("RGB").crop(box)
        c.save(TIP / f"T2_f{f}_native.png")
        # split tall tooltips so the reading crop stays under ~400 native px wide
        c.resize((c.width * a.scale, c.height * a.scale), Image.LANCZOS).save(
            TIP / f"T2_f{f}_x{a.scale}.png")
    json.dump(res, open(OUT / "g6-tooltip-boxes2.json", "w"), indent=1)


if __name__ == "__main__":
    main()
