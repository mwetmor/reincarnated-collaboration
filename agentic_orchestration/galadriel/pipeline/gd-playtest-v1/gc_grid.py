#!/usr/bin/env python3
"""GAL-CAM: dense-ish GRID image-motion field, for the horizon row.

WHY A GRID AND NOT BANDS
------------------------
Bands gave the right qualitative answer (pan grows down-screen) but a poor
quantitative one, for two reasons found by looking: the band containing the
player is pinned to (0,0) by screen-locked content, and the top bands contain
CAVE WALL, which is not in the ground plane and therefore does not obey the
ground-plane motion law at all.

A grid fixes both: patches are small enough that the player poisons only one or
two of them, and per-patch residuals expose off-plane patches instead of
averaging them in.

THE LAW BEING MEASURED
----------------------
For a player-locked camera translating over a ground plane (pinhole, no roll),
the induced image motion at screen offset (x', y') from the principal point is

    dx = a*s0*G  -  b*x'*lambda*s0*sin(t)*G
    dy =        -  b*s0*sin(t)*G^2                 G = 1 + lambda*y'

where (a,b) is the camera's ground translation for that frame pair. Note what
drops out: dy does not depend on x' at all, and the x'-DEPENDENCE of dx is a
pure divergence. Divide them:

    (d dx / d x') / dy  =  lambda / G  =  1 / (y - y_h)

The camera translation (a,b) CANCELS. The scale s0 CANCELS. The pitch CANCELS.
What is left is one number, the horizon row y_h, measured per frame pair from
the shape of the motion field alone -- no isotropy assumption, no calibration
object, no known speed. That is why this instrument exists.

Second, redundant route from the same data: dy ~ G^2, so sqrt(|dy|) is LINEAR in
screen row and crosses zero at y_h. Two estimates of the same quantity from
different components of the same field.
"""
import argparse
import json
import subprocess

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080


def stream(ss, dur):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", str(ss), "-i", VIDEO, "-t", str(dur),
           "-pix_fmt", "gray", "-f", "rawvideo", "-"]
    n = W * H
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 8)
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, dtype=np.uint8).reshape(H, W)
    p.stdout.close()
    p.wait()


def parab(c, i):
    n = len(c)
    a, b, cc = c[(i - 1) % n], c[i], c[(i + 1) % n]
    d = a - 2 * b + cc
    return 0.0 if d == 0 else float(np.clip(0.5 * (a - cc) / d, -1, 1))


def phase(fa, fb, shape):
    r = fa * np.conj(fb)
    m = np.abs(r)
    m[m == 0] = 1
    c = np.fft.irfft2(r / m, s=shape)
    idx = np.unravel_index(np.argmax(c), c.shape)
    pk = float(c[idx])
    dy, dx = idx
    sy = parab(c[:, dx], dy)
    sx = parab(c[dy, :], dx)
    if dy > shape[0] // 2:
        dy -= shape[0]
    if dx > shape[1] // 2:
        dx -= shape[1]
    return dy + sy, dx + sx, pk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=float, nargs="+", required=True)
    ap.add_argument("--dur", type=float, default=3.0)
    ap.add_argument("--xc", type=int, nargs="+", default=[430, 650, 870, 1090, 1290])
    ap.add_argument("--yc", type=int, nargs="+", default=[190, 330, 470, 610, 750])
    ap.add_argument("--pw", type=int, default=280)
    ap.add_argument("--ph", type=int, default=180)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    win = np.outer(np.hanning(args.ph), np.hanning(args.pw))
    shape = (args.ph, args.pw)
    cells = [(x, y) for y in args.yc for x in args.xc]

    rows = []
    for ss in args.starts:
        prev = None
        i = 0
        for g in stream(ss, args.dur):
            cur = []
            for (x, y) in cells:
                s = g[y - args.ph // 2:y + args.ph // 2,
                      x - args.pw // 2:x + args.pw // 2].astype(np.float32)
                cur.append(np.fft.rfft2((s - s.mean()) * win))
            if prev is not None:
                v = []
                for j in range(len(cells)):
                    dy, dx, pk = phase(prev[j], cur[j], shape)
                    v.append([round(dx, 4), round(dy, 4), round(pk, 4)])
                rows.append(dict(ss=float(ss), i=i, v=v))
            prev = cur
            i += 1
        print(f"ss={ss:.0f} kept={len(rows)}", flush=True)

    json.dump(dict(cells=cells, pw=args.pw, ph=args.ph, rows=rows),
              open(args.out, "w"))
    print("wrote", args.out, len(rows))


if __name__ == "__main__":
    main()
