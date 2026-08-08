#!/usr/bin/env python3
"""Ruler-annotated plate-bar evidence sheet.

Draws, over a x4 LANCZOS upscale of the unmodified bar band:
  cyan   ticks + labels every 20 full-frame px
  yellow the MEASURED sub-pixel fill edge
  red    the column a competing census fraction WOULD have produced
so the exclusion argument is visible rather than merely asserted.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"
BOX = (840, 56, 1120, 82)          # full-frame px
Z = 4


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


def tile(video, t, tmpd, edge, marks, label):
    im = grab(video, t, tmpd)
    c = im.crop(BOX).resize(((BOX[2] - BOX[0]) * Z, (BOX[3] - BOX[1]) * Z), Image.LANCZOS)
    hdr, ftr = 20, 34
    out = Image.new("RGB", (c.width, c.height + hdr + ftr), (12, 12, 12))
    out.paste(c, (0, hdr))
    d = ImageDraw.Draw(out)
    f9, f11 = font(11), font(13)
    d.text((4, 4), label, fill=(255, 232, 110), font=f11)
    for x in range(BOX[0], BOX[2] + 1):
        if x % 20 == 0:
            px = (x - BOX[0]) * Z
            d.line([(px, hdr + c.height - 6), (px, hdr + c.height)], fill=(0, 220, 220))
            d.text((px - 12, hdr + c.height + 2), str(x), fill=(0, 220, 220), font=f9)
    if edge is not None:
        px = (edge - BOX[0]) * Z
        d.line([(px, hdr), (px, hdr + c.height)], fill=(255, 240, 60), width=2)
        d.text((px + 3, hdr + 2), f"edge {edge:.2f}", fill=(255, 240, 60), font=f9)
    for (mx, ml) in marks:
        px = (mx - BOX[0]) * Z
        d.line([(px, hdr + c.height - 20), (px, hdr + c.height)], fill=(255, 70, 70), width=1)
        d.text((px + 2, hdr + c.height - 32), ml, fill=(255, 110, 110), font=f9)
    return out


def sheet(video, rows, out, tmpd):
    tiles = [tile(video, t, tmpd, e, m, l) for (t, e, m, l) in rows]
    W = max(x.width for x in tiles)
    H = sum(x.height + 8 for x in tiles)
    sh = Image.new("RGB", (W, H), (24, 24, 24))
    y = 0
    for x in tiles:
        sh.paste(x, (0, y)); y += x.height + 8
    sh.save(out)
    return sh.size


if __name__ == "__main__":
    V, T = "/tmp/kc2-s2.mp4", "/tmp/crgrab"
    E = "../evidence/"
    X0, X1 = 862.0, 1059.43
    def px(f):
        return X0 + f * (X1 - X0)
    rows = [
        (701.7333, 1059.20, [(px(1.0), "1.0000=1059.4"), (px(0.98848), "0.98848=1057.2"),
                             (px(0.95397), "0.95397=1050.3")],
         "CRABLING L108  t=701.7333   frac 0.9988"),
        (701.8, 1059.21, [(px(1.0), "1.0000"), (px(0.98848), "0.98848"), (px(0.76633), "0.76633")],
         "CRABLING L108  t=701.8000   frac 0.9989"),
        (701.9333, 1057.36, [(px(1.0), "1.0000"), (px(0.95399), "0.95399")],
         "CRABLING L107  t=701.9333   frac 0.9895  NO-MATCH on frame"),
        (704.4667, 1059.42, [(px(1.0), "1.0000"), (px(0.19749), "0.19749")],
         "ROTMOUTH L107  t=704.4667   frac 1.0000  DEGENERATE (3 bodies at full)"),
        (702.4667, 1025.25, [(px(0.82856), "0.82856=1025.6")],
         "CALIBRATION CHECK  Mudflinger t=702.4667  binds 367,509/443,554 at +0.33 px"),
    ]
    print(sheet(V, rows, E + "plate-bar-ruler-x4.png", T))
