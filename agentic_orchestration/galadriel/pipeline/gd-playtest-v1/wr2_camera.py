#!/usr/bin/env python3
"""WR1-GAL-2: camera-pan + player-screen-locus instrument.

WHY THIS INSTRUMENT AND NOT "measure the player sprite moving"
---------------------------------------------------------------
Grim Dawn's camera is player-locked. The player's SCREEN position is therefore
near-constant and a knockback shows up as WORLD SCROLL, not as player-sprite
translation. So the measurable for displacement is the camera pan, recovered by
registering consecutive world frames against each other.

Registration is by phase correlation on a grayscale, DC-removed, Hann-windowed
crop of the terrain. Sub-pixel is NOT claimed: the peak is reported at integer
px with its correlation height, so a weak/ambiguous registration is visible as
a low peak rather than silently becoming a confident wrong number.

Second product: the PLAYER LOCUS. After registering frame t+1 onto frame t, any
content that is stationary in SCREEN space (the player, the HUD) becomes a large
residual, while terrain cancels. Accumulating that residual over a movement
window and taking the peak inside the play area locates the player's screen
locus empirically -- no assumption that the camera is exactly centred.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080


def stream(ss, t, fps, cw=None):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox", "-ss", str(ss), "-i", VIDEO, "-t", str(t),
           "-vf", f"fps={fps}", "-pix_fmt", "gray", "-f", "rawvideo", "-"]
    n = W * H
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 4)
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield i, np.frombuffer(b, dtype=np.uint8).reshape(H, W)
        i += 1
    p.stdout.close()
    p.wait()


def make_win(h, w):
    return np.outer(np.hanning(h), np.hanning(w))


def grad(a):
    gx = np.zeros_like(a); gy = np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]
    gy[1:-1, :] = a[2:, :] - a[:-2, :]
    return np.sqrt(gx * gx + gy * gy)


def phase_shift(a, b, win):
    """Return (dy, dx, peak) such that b ~= a shifted by (dy,dx)."""
    fa = np.fft.rfft2((a - a.mean()) * win)
    fb = np.fft.rfft2((b - b.mean()) * win)
    r = fa * np.conj(fb)
    m = np.abs(r)
    m[m == 0] = 1
    c = np.fft.irfft2(r / m, s=a.shape)
    idx = np.unravel_index(np.argmax(c), c.shape)
    pk = float(c[idx])
    dy, dx = idx
    if dy > a.shape[0] // 2:
        dy -= a.shape[0]
    if dx > a.shape[1] // 2:
        dx -= a.shape[1]
    return int(dy), int(dx), pk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--locus", action="store_true",
                    help="also accumulate the screen-stationary residual map")
    ap.add_argument("--locus_out", default=None)
    # terrain crop used for registration (avoid HUD panel + globes)
    ap.add_argument("--rx", type=int, default=60)
    ap.add_argument("--ry", type=int, default=90)
    ap.add_argument("--rw", type=int, default=1216)
    ap.add_argument("--rh", type=int, default=768)
    ap.add_argument("--grad", action="store_true",
                    help="register on gradient magnitude (robust to VFX bloom)")
    args = ap.parse_args()

    win = make_win(args.rh, args.rw)
    prev = None
    rows = []
    acc = np.zeros((args.rh, args.rw), dtype=np.float64) if args.locus else None
    nacc = 0
    for i, g in stream(args.ss, args.t, args.fps):
        cur = g[args.ry:args.ry + args.rh, args.rx:args.rx + args.rw].astype(np.float32)
        if args.grad:
            cur = grad(cur)
        pts = round(args.ss + i / args.fps, 4)
        if prev is not None:
            dy, dx, pk = phase_shift(prev, cur, win)
            rows.append(dict(pts=pts, dy=dy, dx=dx, pk=round(pk, 5)))
            if acc is not None and abs(dx) + abs(dy) >= 3 and pk > 0.02:
                reg = np.roll(np.roll(cur, dy, axis=0), dx, axis=1)
                d = np.abs(reg - prev)
                mx = max(abs(dx), abs(dy)) + 2
                d[:mx, :] = 0
                d[-mx:, :] = 0
                d[:, :mx] = 0
                d[:, -mx:] = 0
                acc += d
                nacc += 1
        prev = cur
        if i % 300 == 0:
            print(f"  {pts:.2f}s n={len(rows)}", file=sys.stderr, flush=True)

    json.dump(dict(ss=args.ss, t=args.t, fps=args.fps,
                   reg=dict(x=args.rx, y=args.ry, w=args.rw, h=args.rh),
                   rows=rows), open(args.out, "w"))
    print(f"{len(rows)} pan samples -> {args.out}")

    if acc is not None and nacc:
        acc /= nacc
        np.save(args.locus_out or (args.out + ".locus.npy"), acc.astype(np.float32))
        k = 24
        box = np.ones((k, k)) / (k * k)
        # cheap separable box smooth
        sm = np.apply_along_axis(lambda r: np.convolve(r, np.ones(k) / k, "same"), 1, acc)
        sm = np.apply_along_axis(lambda r: np.convolve(r, np.ones(k) / k, "same"), 0, sm)
        yy, xx = np.unravel_index(np.argmax(sm), sm.shape)
        print(json.dumps(dict(n_used=nacc,
                              locus_screen_x=int(args.rx + xx),
                              locus_screen_y=int(args.ry + yy),
                              peak=float(sm[yy, xx]),
                              mean=float(sm.mean()))))


if __name__ == "__main__":
    main()
