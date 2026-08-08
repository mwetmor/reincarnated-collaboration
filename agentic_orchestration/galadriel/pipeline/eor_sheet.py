#!/usr/bin/env python3
"""eor_sheet.py — labelled magnified contact sheets for eye-reading.

galadriel / visual-perception seam. Companion to eor_badge_ocr.py etc.

The CV layer's only job is to find WHERE to look and to magnify enough that a
human/agent read is defensible. No OCR result is ever reported as a value.

Usage (as a library):

    from eor_sheet import crop_sheet
    crop_sheet(files, roi=(1470, 98, 1545, 126), scale=7,
               labels=[...], out='sheet.png', cols=2)
"""
from __future__ import annotations

import os
import re

from PIL import Image, ImageDraw, ImageFont

FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial.ttf",
]


def _font(size: int):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def t_of(path: str) -> float:
    """Pull the float timestamp out of a `..._<t>.png` filename."""
    m = re.findall(r"([0-9]+\.[0-9]+)", os.path.basename(path))
    return float(m[-1]) if m else 0.0


def crop_sheet(files, roi, scale=6, labels=None, out="sheet.png", cols=2,
               label_w=210, font_size=30, pad=8, bg=(12, 12, 12),
               fg=(255, 230, 120)):
    """Magnified ROI crops from `files`, laid out column-major with big labels."""
    x0, y0, x1, y1 = roi
    cw, ch = int((x1 - x0) * scale), int((y1 - y0) * scale)
    n = len(files)
    rows = (n + cols - 1) // cols
    W = cols * (label_w + cw + pad) + pad
    H = rows * (ch + pad) + pad
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f = _font(font_size)
    if labels is None:
        labels = [os.path.basename(p) for p in files]
    for i, (path, lab) in enumerate(zip(files, labels)):
        col, row = divmod(i, rows)
        x = pad + col * (label_w + cw + pad)
        y = pad + row * (ch + pad)
        im = Image.open(path).convert("RGB")
        c = im.crop((x0, y0, x1, y1)).resize((cw, ch), Image.LANCZOS)
        d.text((x, y + ch // 2 - font_size // 2), str(lab), fill=fg, font=f)
        sheet.paste(c, (x + label_w, y))
    sheet.save(out)
    return sheet.size


def tile_sheet(images, labels, out="tiles.png", cols=4, pad=10, lab_h=34,
               font_size=26, bg=(12, 12, 12), fg=(255, 230, 120)):
    """Contact sheet from already-cropped PIL images, label above each tile."""
    tw = max(im.width for im in images)
    th = max(im.height for im in images)
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad,
                              rows * (th + lab_h + pad) + pad), bg)
    d = ImageDraw.Draw(sheet)
    f = _font(font_size)
    for i, (im, lab) in enumerate(zip(images, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + lab_h + pad)
        d.text((x + 2, y + 2), str(lab), fill=fg, font=f)
        sheet.paste(im, (x, y + lab_h))
    sheet.save(out)
    return sheet.size
