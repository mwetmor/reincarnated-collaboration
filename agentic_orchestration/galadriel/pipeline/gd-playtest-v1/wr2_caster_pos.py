#!/usr/bin/env python3
"""WR1-GAL-2 task 3: locate the CASTER on screen, per frame, from its over-head
numeric health readout.

Grim Dawn draws "(cur/max)" directly above the monster the cursor is on. That
string is a rigid, machine-findable marker for that monster's screen position:
bright achromatic ink, 8-16 px tall, 45-260 px wide, with >=6 ink groups and a
paren at each end (the shape test is g8_monhp.py's, verbatim in intent).

The readout sits above the monster's head; the horizontal centre of the string
is the monster's screen X. Its Y is reported as-is and the vertical offset from
head to ground is NOT guessed -- the caller compares like with like by using
the SAME marker convention for the player (whose screen locus is measured
independently by wr2_camera --locus).
"""
import argparse
import json
import subprocess

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080
Y0, Y1, X0, X1 = 100, 940, 40, 1330
BRIGHT_MIN, CHROMA_MAX = 150, 50


def bands(rows):
    out, run = [], None
    for i, v in enumerate(rows):
        if v:
            run = [i, i] if run is None else [run[0], i]
        elif run is not None:
            out.append(tuple(run))
            run = None
    if run:
        out.append(tuple(run))
    return out


def find(rgb):
    sub = rgb[Y0:Y1, X0:X1].astype(np.int16)
    mx, mn = sub.max(axis=2), sub.min(axis=2)
    m = (mn > BRIGHT_MIN) & ((mx - mn) < CHROMA_MAX)
    hits = []
    for by0, by1 in bands(m.sum(axis=1) > 0):
        h = by1 - by0 + 1
        if not (8 <= h <= 16):
            continue
        prof = m[by0:by1 + 1].sum(axis=0)
        nz = np.nonzero(prof)[0]
        if not len(nz):
            continue
        runs, s, prev = [], nz[0], nz[0]
        for x in nz[1:]:
            if x - prev > 12:
                runs.append((s, prev))
                s = x
            prev = x
        runs.append((s, prev))
        for rx0, rx1 in runs:
            w = rx1 - rx0 + 1
            if not (45 <= w <= 260):
                continue
            band = m[by0:by1 + 1, rx0:rx1 + 1]
            gs, run = [], None
            for gi, gv in enumerate(band.sum(axis=0)):
                if gv > 0:
                    run = [gi, gi] if run is None else [run[0], gi]
                elif run is not None:
                    gs.append(tuple(run))
                    run = None
            if run:
                gs.append(tuple(run))
            if len(gs) < 6:
                continue
            (l0, l1), (r0, r1) = gs[0], gs[-1]
            lh = np.nonzero(band[:, l0:l1 + 1].sum(axis=1))[0]
            rh = np.nonzero(band[:, r0:r1 + 1].sum(axis=1))[0]
            if not (len(lh) and len(rh)):
                continue
            if not ((l1 - l0 + 1) <= 5 and (r1 - r0 + 1) <= 5
                    and (lh.max() - lh.min() + 1) >= h - 2
                    and (rh.max() - rh.min() + 1) >= h - 2):
                continue
            hits.append(dict(x0=int(X0 + rx0), x1=int(X0 + rx1),
                             y0=int(Y0 + by0), y1=int(Y0 + by1),
                             cx=round(X0 + (rx0 + rx1) / 2.0, 1),
                             cy=round(Y0 + (by0 + by1) / 2.0, 1),
                             w=int(w), groups=len(gs)))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, required=True)
    ap.add_argument("--f1", type=int, required=True)
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--fps", type=float, default=None,
                    help="if given, sample by fps filter over [f0/60, f1/60] instead of every frame")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.fps:
        ss = args.f0 / 60.0
        dur = (args.f1 - args.f0) / 60.0
        cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
               "-hwaccel", "videotoolbox", "-ss", f"{ss:.6f}", "-i", VIDEO,
               "-t", f"{dur:.3f}", "-vf", f"fps={args.fps}",
               "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
        n = W * H * 3
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
        rows, i = [], 0
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                break
            a = np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3)
            hits = find(a)
            if hits:
                rows.append(dict(f=int(round((ss + i / args.fps) * 60)), hits=hits))
            i += 1
        p.stdout.close(); p.wait()
        json.dump(dict(f0=args.f0, f1=args.f1, n_sampled=i, rows=rows), open(args.out, "w"))
        print(f"{i} sampled, {len(rows)} with readouts -> {args.out}")
        return
    ss = max(0.0, (args.f0 - 30) / 60.0)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", f"{ss:.6f}", "-i", VIDEO, "-frames:v", str(args.f1 - args.f0 + 40),
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
    base = int(round(ss * 60))
    rows = []
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        fn = base + i
        if args.f0 <= fn <= args.f1 and (fn - args.f0) % args.step == 0:
            a = np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3)
            rows.append(dict(f=fn, hits=find(a)))
        i += 1
        if fn > args.f1:
            break
    p.stdout.close()
    p.wait()
    json.dump(dict(f0=args.f0, f1=args.f1, rows=rows), open(args.out, "w"))
    print(f"{len(rows)} frames -> {args.out}")


if __name__ == "__main__":
    main()
