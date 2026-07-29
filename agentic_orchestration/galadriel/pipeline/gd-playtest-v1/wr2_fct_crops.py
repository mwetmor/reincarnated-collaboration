#!/usr/bin/env python3
"""WR1-GAL-2: cut each FCT instance's PEAK observation as a 6x crop, and lay the
set out as one contact sheet with instance id + spawn frame burned in.

The detector's job is recall; the eye's job is precision. This is the handoff.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image, ImageDraw

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080


def frames_needed(recs):
    return sorted({r["peak_f"] for r in recs})


def grab(fs):
    f0, f1 = min(fs), max(fs)
    ss = max(0.0, (f0 - 30) / 60.0)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", f"{ss:.6f}", "-i", VIDEO, "-frames:v", str(f1 - f0 + 40),
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
    base = int(round(ss * 60))
    want = set(fs)
    out = {}
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        fn = base + i
        if fn in want:
            out[fn] = np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3).copy()
        i += 1
        if fn > f1:
            break
    p.stdout.close()
    p.wait()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fct", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--zoom", type=int, default=5)
    ap.add_argument("--pad", type=int, default=6)
    ap.add_argument("--only", default=None, help="comma list of instance ids")
    args = ap.parse_args()

    d = json.load(open(args.fct))
    recs = d["inst"]
    if args.only:
        keep = {int(v) for v in args.only.split(",")}
        recs = [r for r in recs if r["i"] in keep]
    fr = grab(frames_needed(recs))
    tiles = []
    for r in recs:
        x0, y0, x1, y1 = r["peak_box"]
        a = fr.get(r["peak_f"])
        if a is None:
            continue
        c = a[max(0, y0 - args.pad):y1 + 1 + args.pad,
              max(0, x0 - args.pad):x1 + 1 + args.pad]
        im = Image.fromarray(c)
        im = im.resize((im.width * args.zoom, im.height * args.zoom), Image.LANCZOS)
        tiles.append((r, im))
    tw = max(t[1].width for t in tiles) + 8
    th = max(t[1].height for t in tiles) + 22
    cols = args.cols
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    for k, (r, im) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * th
        sheet.paste(im, (x + 4, y + 18))
        dr.text((x + 4, y + 3), f"i{r['i']} f{r['f_spawn']} n{r['n']}", fill=(255, 255, 0))
    sheet.save(args.out, quality=95)
    print(f"{len(tiles)} crops -> {args.out} {sheet.size}")


if __name__ == "__main__":
    main()
