#!/usr/bin/env python3
"""Magnified exact-seek plate crop sheets. No transformation but LANCZOS upscale.

usage: crops.py <video> <tmpdir> <t,t,t...> <outprefix> <boxname> <zoom>
boxes are full-frame pixel coords at 1920x1080.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"
BOXES = {
    "name":  (780, 12, 1140, 40),     # generous: covers boss bbox 833..1084 + wider
    "namew": (600, 12, 1350, 40),     # full name band
    "lvl":   (900, 40, 1020, 62),
    "bar":   (780, 56, 1150, 80),
    "barw":  (760, 56, 1180, 82),
    "fam":   (700, 86, 1250, 108),
    "wide":  (640, 12, 1290, 110),
    "plate": (760, 12, 1180, 110),
}


def font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()


def grab(video, t, tmpd):
    p = os.path.join(tmpd, f"g_{t}.png")
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video,
                        "-frames:v", "1", "-y", p], check=True)
    return Image.open(p).convert("RGB")


def sheet(video, ts, out, box, zoom, tmpd, fsz=18):
    tiles = []
    f = font(fsz)
    for t in ts:
        im = grab(video, t, tmpd)
        c = im.crop(box)
        c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
        lab = Image.new("RGB", (c.width, c.height + fsz + 8), (0, 0, 0))
        lab.paste(c, (0, fsz + 8))
        ImageDraw.Draw(lab).text((4, 3), f"t={t}  x{zoom}  box={box}",
                                 fill=(255, 232, 110), font=f)
        tiles.append(lab)
    Wd = max(x.width for x in tiles)
    Ht = sum(x.height + 6 for x in tiles)
    sh = Image.new("RGB", (Wd, Ht), (18, 18, 18))
    y = 0
    for x in tiles:
        sh.paste(x, (0, y))
        y += x.height + 6
    sh.save(out)
    return sh.size


if __name__ == "__main__":
    video, tmpd = sys.argv[1], sys.argv[2]
    os.makedirs(tmpd, exist_ok=True)
    ts = [float(x) for x in sys.argv[3].split(",")]
    pref, which, zoom = sys.argv[4], sys.argv[5], int(sys.argv[6])
    print(sheet(video, ts, f"{pref}-{which}-x{zoom}.png", BOXES[which], zoom, tmpd))
