#!/usr/bin/env python3
"""WR1-GAL-2: frigidring nova detector, 60 fps, frame-indexed.

SIGNATURE (read off the death-2 cast, f309041..f309120)
-------------------------------------------------------
  WINDUP  a bright cyan/white cold bloom grows on the CASTER for ~0.75 s.
          Measured as `cold`: B>150, B-R>60, B>=G-12.
  RELEASE a red-orange torus expands from the caster AND a fan of white-headed
          frost lances is launched radially. Measured as `ring`: R>120,
          R-G>70, R-B>55, i.e. saturated red that is NOT the ambient dark-red
          cave palette (which fails the R>120 clause).

Both channels are reported per frame with pixel counts and centroids so the
release instant can be read off the `ring` onset and the windup start off the
`cold` onset -- rather than being asserted.

Scan runs on a 1/3-scale copy of the play area; the counts are therefore in
1/9-scale pixel units and are comparable only within this instrument.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
CX, CY, CW, CH = 0, 60, 1350, 880
SW, SH = CW // 3, CH // 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox", "-ss", str(args.ss), "-i", VIDEO,
           "-t", str(args.t),
           "-vf", f"fps=60,crop={CW}:{CH}:{CX}:{CY},scale={SW}:{SH}",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = SW * SH * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 16)
    f0 = int(round(args.ss * 60))
    rows, i = [], 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, dtype=np.uint8).reshape(SH, SW, 3).astype(np.int16)
        R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        cold = (B > 150) & (B - R > 60) & (B >= G - 12)
        ring = (R > 120) & (R - G > 70) & (R - B > 55)
        nc, nr = int(cold.sum()), int(ring.sum())
        rec = [f0 + i, nc, nr, -1, -1, -1, -1]
        if nc > 40:
            ys, xs = np.nonzero(cold)
            rec[3], rec[4] = int(xs.mean() * 3 + CX), int(ys.mean() * 3 + CY)
        if nr > 40:
            ys, xs = np.nonzero(ring)
            rec[5], rec[6] = int(xs.mean() * 3 + CX), int(ys.mean() * 3 + CY)
        rows.append(rec)
        i += 1
        if i % 3600 == 0:
            print(f"  f{f0+i} ({args.ss + i/60:.0f}s)", file=sys.stderr, flush=True)
    p.stdout.close()
    p.wait()
    json.dump(dict(f0=f0, n=i, cols=["frame", "cold", "ring", "cx", "cy", "rx", "ry"],
                   rows=rows), open(args.out, "w"))
    print(f"{i} frames f{f0}..{f0+i-1} -> {args.out}")


if __name__ == "__main__":
    main()
