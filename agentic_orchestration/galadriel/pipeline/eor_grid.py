#!/usr/bin/env python3
"""eor_grid.py — labelled GRID crop sheets from exact-seek frame grabs.

galadriel / visual-perception seam. KC2-SIM fourth-extraction pass.

`eor_cropsheet.py` stacks tiles vertically. That was fine for one wave; across
five waves it produces sheets thousands of pixels tall, which are downsampled to
illegibility at read time and therefore cannot be eye-read - the exact failure
mode the sheet exists to prevent. This module lays tiles out in a grid with a
bounded page height and paginates, so every tile reaches the eye at full zoom.

Every tile is an EXACT-SEEK frame grab (`ffmpeg -ss <t> -i <v> -frames:v 1`),
never an fps-series frame.

  jobs: [{"t": 692.2, "box": [x0,y0,x1,y1], "label": "..."}, ...]
"""
from __future__ import annotations

import math
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"


def _font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()


def grab(video, t, tmpd):
    p = os.path.join(tmpd, f"g{t}.png")
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video,
                        "-frames:v", "1", "-y", p], check=True)
    return Image.open(p).convert("RGB")


def tiles(video, jobs, zoom=5, padx=8, above=6, below=22, font_sz=17):
    tmpd = tempfile.mkdtemp()
    f = _font(font_sz)
    out = []
    for j in jobs:
        im = grab(video, j["t"], tmpd)
        x0, y0, x1, y1 = j["box"]
        c = im.crop((max(0, x0 - padx), max(0, y0 - above),
                     min(im.width, x1 + padx + 1), min(im.height, y1 + below + 1)))
        c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
        lab = Image.new("RGB", (c.width, c.height + font_sz + 8), (0, 0, 0))
        lab.paste(c, (0, font_sz + 8))
        ImageDraw.Draw(lab).text((3, 2), j.get("label", f"t={j['t']}"),
                                 fill=(255, 232, 110), font=f)
        out.append(lab)
    return out


def page(tl, out, cols=None, max_w=1500, bg=(18, 18, 18), pad=6):
    """Lay tiles out in a grid. cols auto-fits to max_w if not given."""
    tw = max(t.width for t in tl)
    th = max(t.height for t in tl)
    if cols is None:
        cols = max(1, min(len(tl), max_w // (tw + pad)))
    rows = math.ceil(len(tl) / cols)
    sh = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + pad) + pad), bg)
    for i, t in enumerate(tl):
        sh.paste(t, (pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + pad)))
    sh.save(out)
    return sh.size


def sheet(video, jobs, out, zoom=5, padx=8, above=6, below=22, cols=None,
          max_w=1500, per_page=None):
    """Build one or several paginated grid sheets. Returns list of paths."""
    tl = tiles(video, jobs, zoom, padx, above, below)
    if per_page is None or len(tl) <= per_page:
        page(tl, out, cols, max_w)
        return [out]
    paths = []
    base, ext = os.path.splitext(out)
    for k in range(math.ceil(len(tl) / per_page)):
        p = f"{base}-p{k+1}{ext}"
        page(tl[k * per_page:(k + 1) * per_page], p, cols, max_w)
        paths.append(p)
    return paths
