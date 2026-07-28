#!/usr/bin/env python3
"""
G-6 pass 5: node-counter TIME SERIES.

The Berserker mastery panel renders at a fixed screen position, so a given
skill node's "N / M" counter sits at a fixed native pixel box in every
skill-window still. Cropping that same box across the run's skill-window
bursts yields a rank series that can be read against the PlayStats panel's
`play_time` / `max_level` from the same frame.

Output is a labelled vertical montage per node box so the eye reads the whole
series at once, in order, with frame id + play_time + char level stamped on
each row. Native crops are written too.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
SER = OUT / "node-series"

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--box", required=True, help="x0,y0,x1,y1 native")
    ap.add_argument("--frames", required=True, help="comma list")
    ap.add_argument("--scale", type=int, default=6)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--panel", default="g6-panel-skillframes.json")
    a = ap.parse_args()
    SER.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = (int(v) for v in a.box.split(","))
    fids = [int(v) for v in a.frames.split(",")]
    try:
        panel = json.load(open(OUT / a.panel))
    except Exception:
        panel = {}
    font = ImageFont.truetype(FONT, 26)
    tiles = []
    for f in fids:
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            c = im.convert("RGB").crop((x0, y0, x1, y1))
        c.save(SER / f"{a.tag}_f{f}_native.png")
        c = c.resize((c.width * a.scale, c.height * a.scale), Image.LANCZOS)
        tiles.append((f, c))
    lw = 340
    w = lw + max(t.width for _, t in tiles)
    h = sum(t.height + 8 for _, t in tiles)
    sheet = Image.new("RGB", (w, h), (10, 10, 12))
    d = ImageDraw.Draw(sheet)
    y = 0
    for f, t in tiles:
        p = panel.get(str(f), {})
        lab = f"f{f}  pt={p.get('play_time')}  lvl={p.get('max_level')}"
        d.text((6, y + t.height // 2 - 14), lab, fill=(255, 235, 130), font=font)
        sheet.paste(t, (lw, y))
        y += t.height + 8
    p = SER / f"SERIES_{a.tag}.png"
    sheet.save(p)
    print(p)


if __name__ == "__main__":
    main()
