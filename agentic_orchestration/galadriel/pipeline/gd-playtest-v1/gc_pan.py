#!/usr/bin/env python3
"""GAL-CAM: camera-pan hodograph, banded by screen row.

WHY THIS INSTRUMENT
-------------------
The nova is a scale bar but a poor PITCH bar: most of its 16 lances die on the
boss body or the cave wall within a few frames, leaving a one-sided fan (see
evidence/look-sheet.jpg). A one-sided fan pins an ellipse's axis ratio badly.

The camera itself is a better calibration target, and it runs for 1h53m.

Grim Dawn's camera is player-locked, so when the player moves 1 m of GROUND the
whole world translates on screen by the ground-plane scale in that direction:

    (dx, dy) = ( s * X_m ,  -s * k * Z_m )        k = sin(pitch)

Player ground speed is ISOTROPIC (a character does not run faster east than
north). So over a long session the cloud of per-frame pan vectors fills an
ORIGIN-CENTRED ellipse whose semi-axes are in the ratio B/A = k. Reading the
axis ratio of that cloud's boundary gives the pitch with no skill parameters, no
projectile physics, and no ring centre.

BANDS -> THE PERSPECTIVE TEST
-----------------------------
Under an ORTHOGRAPHIC ground projection every screen row translates by the SAME
number of pixels for the same world motion. Under a PINHOLE camera it does not:
near ground (down-screen) is drawn larger, so it sweeps MORE pixels than far
ground (up-screen) for the same metres. Correlating separate horizontal BANDS of
the play area therefore measures the scale gradient d(px/m)/d(screen y) directly
-- as a ratio of measured pan magnitudes, with no camera model interposed.

That ratio is the operand the decision-surface question actually needs: how many
ground metres a pixel is worth at the top of the frame versus the bottom.

Sub-pixel peak by 3-point parabolic interpolation on the phase-correlation
surface; the raw integer peak and its height are kept so a weak registration
stays visible instead of silently becoming a confident wrong number.
"""
import argparse
import json
import math
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


def parab(c, i, n):
    a, b, cc = c[(i - 1) % n], c[i], c[(i + 1) % n]
    d = (a - 2 * b + cc)
    return 0.0 if d == 0 else 0.5 * (a - cc) / d


def phase(fa, fb, shape):
    r = fa * np.conj(fb)
    m = np.abs(r)
    m[m == 0] = 1
    c = np.fft.irfft2(r / m, s=shape)
    idx = np.unravel_index(np.argmax(c), c.shape)
    pk = float(c[idx])
    dy, dx = idx
    sy = parab(c[:, dx], dy, c.shape[0])
    sx = parab(c[dy, :], dx, c.shape[1])
    if dy > shape[0] // 2:
        dy -= shape[0]
    if dx > shape[1] // 2:
        dx -= shape[1]
    return dy + sy, dx + sx, pk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=float, nargs="+", required=True)
    ap.add_argument("--dur", type=float, default=3.0)
    ap.add_argument("--x0", type=int, default=260)
    ap.add_argument("--x1", type=int, default=1540)
    ap.add_argument("--bands", type=int, nargs="+",
                    default=[150, 330, 510, 690, 870])
    ap.add_argument("--bh", type=int, default=180)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    hann_y = np.hanning(args.bh)
    hann_x = np.hanning(args.x1 - args.x0)
    win = np.outer(hann_y, hann_x)
    shape = (args.bh, args.x1 - args.x0)

    rows = []
    for ss in args.starts:
        prev = None
        n = 0
        for g in stream(ss, args.dur):
            cur = []
            for by in args.bands:
                sub = g[by:by + args.bh, args.x0:args.x1].astype(np.float32)
                cur.append(np.fft.rfft2((sub - sub.mean()) * win))
            if prev is not None:
                rec = dict(ss=float(ss), i=n)
                ok = True
                for j, by in enumerate(args.bands):
                    dy, dx, pk = phase(prev[j], cur[j], shape)
                    rec[f"b{by}"] = [float(dx), float(dy), float(pk)]
                    if abs(dx) > 60 or abs(dy) > 60:
                        ok = False
                if ok:
                    rows.append(rec)
            prev = cur
            n += 1
        print(f"ss={ss:.1f} frames={n} kept={len(rows)}", flush=True)

    json.dump(dict(bands=args.bands, bh=args.bh, x0=args.x0, x1=args.x1,
                   dur=args.dur, rows=rows), open(args.out, "w"))
    print("wrote", args.out, len(rows), "pairs")


if __name__ == "__main__":
    main()
