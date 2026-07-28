#!/usr/bin/env python3
"""G-6 helper: montage of the mastery panel across frames, at low scale.

Purpose is placement, not reading: it shows WHERE the tooltip sits in each
frame so the precise reading crop can be aimed. Reading is never done off this
montage.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6/sheets")
PANEL = (448, 230, 1530, 890)
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--w", type=int, default=330)
    ap.add_argument("--tag", default="panels")
    a = ap.parse_args()
    fids = [int(v) for v in a.frames.split(",")]
    tw = a.w
    th = int((PANEL[3] - PANEL[1]) * tw / (PANEL[2] - PANEL[0]))
    rows = (len(fids) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * tw, rows * (th + 22)), (10, 10, 12))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(FONT, 18)
    for k, f in enumerate(fids):
        r, c = divmod(k, a.cols)
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            t = im.convert("RGB").crop(PANEL).resize((tw, th), Image.LANCZOS)
        sheet.paste(t, (c * tw, r * (th + 22) + 22))
        d.text((c * tw + 4, r * (th + 22) + 2), f"f{f}", fill=(255, 230, 120), font=font)
    p = OUT / f"{a.tag}.png"
    sheet.save(p)
    print(p)


if __name__ == "__main__":
    main()
