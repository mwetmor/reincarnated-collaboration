#!/usr/bin/env python3
"""SHADOW-CAL: frame grabber + contact sheet.

Pulls frames at given timestamps (seconds) from the GD fixture MP4 and writes
them as PNGs, plus an optional contact sheet for eyeballing.

Usage:
  sc_grab.py --t 100 250 400 --out DIR
  sc_grab.py --every 120 --out DIR --sheet
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

SRC = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
DUR = 6816.516667
FPS = 60.0


def grab(t, out_png, src=SRC):
    """Accurate-ish grab: fast keyframe seek to t-2, then precise decode to t."""
    pre = max(0.0, t - 2.0)
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-ss", f"{pre:.4f}", "-i", src,
        "-ss", f"{t - pre:.4f}",
        "-frames:v", "1", "-q:v", "1",
        out_png,
    ]
    subprocess.run(cmd, check=True)
    return out_png


def grab_seq(t0, n, out_dir, stride=1, src=SRC, prefix="f"):
    """Grab n consecutive frames (stride in frames) starting at time t0."""
    os.makedirs(out_dir, exist_ok=True)
    pre = max(0.0, t0 - 2.0)
    vf = f"select='not(mod(n\\,{stride}))'" if stride > 1 else "null"
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-ss", f"{pre:.4f}", "-i", src,
        "-ss", f"{t0 - pre:.4f}",
        "-vf", vf, "-vsync", "0",
        "-frames:v", str(n), "-q:v", "1",
        os.path.join(out_dir, f"{prefix}%05d.png"),
    ]
    subprocess.run(cmd, check=True)
    return sorted(
        os.path.join(out_dir, f) for f in os.listdir(out_dir)
        if f.startswith(prefix) and f.endswith(".png")
    )


def sheet(paths, out, cols=6, w=480, labels=None):
    ims = [Image.open(p).convert("RGB") for p in paths]
    h = int(w * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
    from PIL import ImageDraw
    d = ImageDraw.Draw(canvas)
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        canvas.paste(im.resize((w, h), Image.LANCZOS), (c * w, r * h))
        lab = labels[i] if labels else os.path.basename(paths[i])
        d.text((c * w + 6, r * h + 6), str(lab), fill=(255, 255, 0))
    canvas.save(out, quality=88)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--t", type=float, nargs="*", default=None)
    ap.add_argument("--every", type=float, default=None)
    ap.add_argument("--start", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--cols", type=int, default=6)
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    ts = a.t if a.t else list(np.arange(a.start, DUR - 30, a.every))
    paths = []
    for t in ts:
        p = os.path.join(a.out, f"t{int(round(t*1000)):09d}.png")
        if not os.path.exists(p):
            grab(t, p)
        paths.append(p)
        print(f"{t:9.2f}  {p}", file=sys.stderr)
    if a.sheet:
        sheet(paths, a.sheet, cols=a.cols,
              labels=[f"{t:.0f}s" for t in ts])
        print("sheet ->", a.sheet)
