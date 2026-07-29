#!/usr/bin/env python3
"""WR1-GAL-2: frigidring windup-vs-release discriminator, 60 fps, frame-indexed.

The plain cold-pixel count cannot tell a WINDUP from PROJECTILES IN FLIGHT --
both are cyan. What separates them is SPATIAL SPREAD:

  windup   cold pixels are one compact bloom on the caster; rms radius about
           the cold centroid stays small and roughly constant while the count
           climbs.
  release  the 16 projectiles leave the caster radially, so the rms radius
           climbs roughly linearly at the projectile speed while the count
           stays flat or falls.

So the release instant is the knee in rms-radius, and it is reported as a
measured series, not asserted. Full-res (no downscale) so the radius is in
native screen px.
"""
import argparse
import json
import subprocess

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
CX, CY, CW, CH = 0, 60, 1350, 880


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox", "-ss", str(args.ss), "-i", VIDEO,
           "-t", str(args.t), "-vf", f"fps=60,crop={CW}:{CH}:{CX}:{CY}",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = CW * CH * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 4)
    f0 = int(round(args.ss * 60))
    rows, i = [], 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, dtype=np.uint8).reshape(CH, CW, 3).astype(np.int16)
        R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        cold = (B > 150) & (B - R > 60) & (B >= G - 12)
        core = (B > 210) & (R > 190) & (G > 200)          # white projectile heads
        ring = (R > 120) & (R - G > 70) & (R - B > 55)
        rec = dict(f=f0 + i, cold=int(cold.sum()), ring=int(ring.sum()))
        if rec["cold"] > 60:
            ys, xs = np.nonzero(cold)
            mx, my = float(xs.mean()), float(ys.mean())
            rec.update(cx=round(mx + CX, 1), cy=round(my + CY, 1),
                       crms=round(float(np.sqrt(((xs - mx) ** 2 + (ys - my) ** 2).mean())), 1))
        if rec["ring"] > 60:
            ys, xs = np.nonzero(ring)
            mx, my = float(xs.mean()), float(ys.mean())
            rec.update(rx=round(mx + CX, 1), ry=round(my + CY, 1),
                       rrms=round(float(np.sqrt(((xs - mx) ** 2 + (ys - my) ** 2).mean())), 1))
        nc = int((cold & core).sum())
        rec["head"] = nc
        rows.append(rec)
        i += 1
    p.stdout.close()
    p.wait()
    json.dump(dict(f0=f0, n=i, rows=rows), open(args.out, "w"))
    print(f"{i} frames f{f0}..{f0+i-1} -> {args.out}")


if __name__ == "__main__":
    main()
