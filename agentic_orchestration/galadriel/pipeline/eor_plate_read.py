#!/usr/bin/env python3
"""eor_plate_read.py — magnified eye-read sheets for the hovered-monster nameplate.

galadriel / visual-perception seam. KC2-SIM Phase-C third-extraction pass.

Two products per requested timestamp, both from an EXACT-SEEK frame grab:

  * NAME + FAMILY strip  full-frame x 640..1290, y 12..110   (default x3)
  * LEVEL numeral strip  full-frame x 915..1005, y 39..61     (default x10)

The level numeral is the red 3-digit glyph run drawn over the plate's health-bar
track, horizontally centred on screen centre (x=960). It is the quantity the
KC2 level-rule fork needs.

  read <video> <t,t,t...> <out-prefix> [zoom_name] [zoom_lvl]
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

NAME_BOX = (640, 12, 1290, 110)
LVL_BOX = (915, 39, 1005, 61)
FONT = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"


def _font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()


def grab(video: str, t: float, tmpd: str) -> Image.Image:
    p = os.path.join(tmpd, f"g_{t}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video,
                    "-frames:v", "1", "-y", p], check=True)
    return Image.open(p).convert("RGB")


def sheet(video, ts, out, box, zoom, labels=None, font_sz=22):
    tmpd = tempfile.mkdtemp()
    tiles = []
    f = _font(font_sz)
    for i, t in enumerate(ts):
        im = grab(video, t, tmpd)
        c = im.crop(box)
        c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
        lab = Image.new("RGB", (c.width, c.height + font_sz + 8), (0, 0, 0))
        lab.paste(c, (0, font_sz + 8))
        txt = labels[i] if labels else f"t={t}"
        ImageDraw.Draw(lab).text((4, 3), txt, fill=(255, 232, 110), font=f)
        tiles.append(lab)
    W = max(x.width for x in tiles)
    H = sum(x.height + 6 for x in tiles)
    sh = Image.new("RGB", (W, H), (18, 18, 18))
    y = 0
    for x in tiles:
        sh.paste(x, (0, y))
        y += x.height + 6
    sh.save(out)
    return sh.size


if __name__ == "__main__":
    video, tss, pref = sys.argv[1], sys.argv[2], sys.argv[3]
    zn = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    zl = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    ts = [float(x) for x in tss.split(",")]
    print("name", sheet(video, ts, pref + "-name.png", NAME_BOX, zn))
    print("lvl", sheet(video, ts, pref + "-lvl.png", LVL_BOX, zl))
