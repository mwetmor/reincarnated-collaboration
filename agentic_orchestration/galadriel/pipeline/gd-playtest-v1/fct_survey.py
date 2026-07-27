#!/usr/bin/env python3
"""Stream a window of the run and report FCT blob activity per frame.

Used to (a) prove FCT is present, (b) locate sustained-damage windows, and
(c) measure the false-positive floor on a known ZERO-damage stretch.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

from fct_detect import WORLD, fct_mask, components, group_glyphs

W, H = 1920, 1080


def stream(video, ss, t, fps):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox", "-ss", str(ss), "-i", video, "-t", str(t),
           "-vf", f"fps={fps}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield i, np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3)
        i += 1
    p.stdout.close()
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--fps", type=float, default=10.0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--minpx", type=int, default=10)
    args = ap.parse_args()

    with open(args.out, "w") as fh:
        for i, frame in stream(args.video, args.ss, args.t, args.fps):
            m = fct_mask(frame)
            comps = [c for c in components(m, args.minpx)
                     if 6 <= (c["y1"] - c["y0"] + 1) <= 24
                     and 2 <= (c["x1"] - c["x0"] + 1) <= 20]
            gs = group_glyphs(comps)
            gs = [g for g in gs if len(g["parts"]) >= 2]
            rec = dict(pts_s=round(args.ss + i / args.fps, 3),
                       n_glyph=len(comps), n_num=len(gs),
                       nums=[dict(x=g["x0"] + WORLD["x0"], y=g["y0"] + WORLD["y0"],
                                  w=g["x1"] - g["x0"] + 1, h=g["y1"] - g["y0"] + 1,
                                  k=len(g["parts"])) for g in gs])
            fh.write(json.dumps(rec) + "\n")
            if i % 200 == 0:
                print(f"  {rec['pts_s']:.1f} n_num={rec['n_num']}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
