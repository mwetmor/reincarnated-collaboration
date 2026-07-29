#!/usr/bin/env python3
"""WR1-GAL-2: frame-accurate filmstrip extractor.

Frames are addressed by ABSOLUTE FRAME NUMBER, not by seek-time, because the
questions this run answers are frame-citation questions. ffmpeg is given a
keyframe-accurate -ss slightly before the first wanted frame and then decoded
forward, so every emitted frame carries a verified index.
"""
import argparse
import subprocess
import sys

import numpy as np
from PIL import Image

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080
FPS = 60.0


def grab(f0, f1):
    """Yield (frame_no, rgb array) for frames f0..f1 inclusive."""
    ss = max(0.0, (f0 - 12) / FPS)
    n_out = f1 - f0 + 1 + 12
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", f"{ss:.6f}", "-i", VIDEO, "-frames:v", str(n_out + 4),
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
    base = int(round(ss * FPS))
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        fn = base + i
        if f0 <= fn <= f1:
            yield fn, np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3)
        i += 1
        if fn > f1:
            break
    p.stdout.close()
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, required=True)
    ap.add_argument("--f1", type=int, required=True)
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--crop", default="700,250,600,450")   # x,y,w,h
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cx, cy, cw, ch = [int(v) for v in args.crop.split(",")]
    tiles = []
    for fn, a in grab(args.f0, args.f1):
        if (fn - args.f0) % args.step:
            continue
        im = Image.fromarray(a[cy:cy + ch, cx:cx + cw])
        if args.scale != 1.0:
            im = im.resize((int(cw * args.scale), int(ch * args.scale)), Image.LANCZOS)
        tiles.append((fn, im))
    if not tiles:
        sys.exit("no frames")
    tw, th = tiles[0][1].size
    cols = args.cols
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), (0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for k, (fn, im) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * th
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 96, y + 14], fill=(0, 0, 0))
        d.text((x + 3, y + 3), f"f{fn}", fill=(255, 255, 0))
    sheet.save(args.out, quality=95)
    print(f"{len(tiles)} tiles f{tiles[0][0]}..f{tiles[-1][0]} -> {args.out} {sheet.size}")


if __name__ == "__main__":
    main()
