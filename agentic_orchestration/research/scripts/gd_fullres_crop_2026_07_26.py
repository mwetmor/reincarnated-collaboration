#!/usr/bin/env python3
"""
Full-resolution crop + upscale + optional vertical contact-sheet, for GD screenshot reading.

METHOD LAW (round-3 ingestion): every banked digit must come from a FULL-RESOLUTION
crop of the native 1920x1080 PNG, upscaled for legibility - never from a downscaled
full frame. This tool enforces that: it crops FIRST (lossless, from the original
pixels) and only then resamples upward.

The crop is delegated to `sips -c <h> <w> --cropOffset <y> <x>` exactly as the
commission specifies; PIL is used only to stack already-full-res crops into one
contact sheet, so that N regions cost one image read instead of N.

Usage:
  gd_fullres_crop_2026_07_26.py OUT.png SCALE  "IMG::y,x,h,w[::caption]" ...
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def crop_fullres(src, y, x, h, w, scale, tmpdir, idx):
    """sips crop from native pixels, then upscale. Returns path."""
    raw = os.path.join(tmpdir, "c%02d.png" % idx)
    up = os.path.join(tmpdir, "u%02d.png" % idx)
    subprocess.run(["sips", "-c", str(h), str(w), "--cropOffset", str(y), str(x),
                    src, "--out", raw], check=True, capture_output=True)
    subprocess.run(["sips", "--resampleWidth", str(int(w * scale)), raw, "--out", up],
                   check=True, capture_output=True)
    return up


def main():
    out, scale = sys.argv[1], float(sys.argv[2])
    specs = sys.argv[3:]
    tmpdir = tempfile.mkdtemp(prefix="gdcrop")
    tiles = []
    for i, spec in enumerate(specs):
        parts = spec.split("::")
        src, geom = parts[0], parts[1]
        cap = parts[2] if len(parts) > 2 else os.path.basename(src)
        y, x, h, w = [int(v) for v in geom.split(",")]
        tiles.append((crop_fullres(src, y, x, h, w, scale, tmpdir, i), cap))

    imgs = [(Image.open(p).convert("RGB"), c) for p, c in tiles]
    band = 22
    W = max(im.width for im, _ in imgs)
    H = sum(im.height + band for im, _ in imgs)
    sheet = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    yy = 0
    for im, cap in imgs:
        d.text((6, yy + 5), cap, fill=(255, 255, 0))
        yy += band
        sheet.paste(im, (0, yy))
        yy += im.height
    sheet.save(out)
    print("%s  %dx%d  (%d tiles, crop-first at native res, %gx upscale)"
          % (out, sheet.width, sheet.height, len(imgs), scale))


if __name__ == "__main__":
    main()
