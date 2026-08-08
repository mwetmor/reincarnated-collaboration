#!/usr/bin/env python3
"""Render labelled, magnified crop sheets for eye-reading located HP readouts.

Each tile is an exact-seek frame grab (never an fps-series frame), cropped around
the readout box and extended downward to include the health bar, so the value and
the bar's class furniture (skull count, bar colour) are read from the same tile.

  sheet <video> <jobs.json> <out.png> [zoom] [below]

jobs.json: [{"t": 862.5, "box": [x0,y0,x1,y1], "label": "..."} , ...]
"""
import sys, os, json, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"


def sheet(video, jobs, out, zoom=5, below=22, above=6, padx=8):
    try:
        font = ImageFont.truetype(FONT, 20)
    except Exception:
        font = ImageFont.load_default()
    tiles = []
    tmpd = tempfile.mkdtemp()
    for j in jobs:
        t = j["t"]; x0, y0, x1, y1 = j["box"]
        tmp = os.path.join(tmpd, "f.png")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video,
                        "-frames:v", "1", "-y", tmp], check=True)
        im = Image.open(tmp).convert("RGB")
        c = im.crop((max(0, x0 - padx), max(0, y0 - above),
                     min(im.width, x1 + padx + 1), min(im.height, y1 + below + 1)))
        c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
        lab = Image.new("RGB", (c.width, c.height + 26), (0, 0, 0))
        lab.paste(c, (0, 26))
        ImageDraw.Draw(lab).text((4, 3), j.get("label", f"t={t}"),
                                 fill=(255, 232, 110), font=font)
        tiles.append(lab)
    Wm = max(t.width for t in tiles); Ht = sum(t.height + 8 for t in tiles)
    sh = Image.new("RGB", (Wm, Ht), (16, 16, 16)); y = 0
    for t in tiles:
        sh.paste(t, (0, y)); y += t.height + 8
    sh.save(out)
    print("wrote", out, sh.size, f"{len(tiles)} tiles")


if __name__ == "__main__":
    sheet(sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3],
          int(sys.argv[4]) if len(sys.argv) > 4 else 5,
          int(sys.argv[5]) if len(sys.argv) > 5 else 22)
