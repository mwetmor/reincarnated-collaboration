#!/usr/bin/env python3
"""WR1-GAL-2 task 4b: cut the top-centre nameplate (name + tier subtitle) at a
list of timestamps and lay them out for eye-reading.

The tier subtitle line under the name is what settles the composition question:
Grim Dawn writes the monster's FACTION/TIER there ("Beastkin", "Hero",
"Nemesis"), and the Primordian's plate reads "Primordian, the Forgotten One /
Beastkin" at f309084. The bar-presence detector gives recall; this sheet gives
the identification.
"""
import argparse
import subprocess

import numpy as np
from PIL import Image, ImageDraw

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080


def grab_one(t, box):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", f"{t:.4f}", "-i", VIDEO, "-frames:v", "1",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    b = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
    if len(b) < n:
        return None
    a = np.frombuffer(b[:n], dtype=np.uint8).reshape(H, W, 3)
    x0, y0, x1, y1 = box
    return Image.fromarray(a[y0:y1, x0:x1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--times", required=True, help="comma list of pts seconds")
    ap.add_argument("--out", required=True)
    ap.add_argument("--box", default="620,16,1300,80")
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--zoom", type=float, default=1.6)
    args = ap.parse_args()
    box = [int(v) for v in args.box.split(",")]
    ts = [float(v) for v in args.times.split(",")]
    tiles = []
    for t in ts:
        im = grab_one(t, box)
        if im is None:
            continue
        im = im.resize((int(im.width * args.zoom), int(im.height * args.zoom)),
                       Image.LANCZOS)
        tiles.append((t, im))
    tw, th = tiles[0][1].size
    th2 = th + 18
    cols = args.cols
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th2 * rows), (10, 10, 10))
    d = ImageDraw.Draw(sheet)
    for k, (t, im) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * th2
        sheet.paste(im, (x, y + 16))
        d.text((x + 3, y + 2), f"{t:.1f}s  f{int(round(t*60))}", fill=(255, 255, 0))
    sheet.save(args.out, quality=95)
    print(f"{len(tiles)} plates -> {args.out} {sheet.size}")


if __name__ == "__main__":
    main()
