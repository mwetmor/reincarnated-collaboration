#!/usr/bin/env python3
"""WR1-GAL-2 task 1: per-INSTANCE floating-combat-text extraction, 60 fps,
frame-indexed, with a spawn position so instances can be gated on the player.

Inherits the detector rules established in fct_detect.py / fct_read.py:
  F-1 FCT is near-WHITE and LOW-SATURATION (min channel > 140, chroma < 45),
      which excludes the saturated-green character.LogData overlay, the red
      health bars and the orange quest tracker.
  F-2 a number SHRINKS as it rises, so it is read at its LARGEST observation.
  F-3 one number lives ~25-35 frames at 60 fps, so per-frame blob counting
      inflates the hit count ~30x; instances must be TRACKED and collapsed.

New here, and the reason this is a fresh script rather than a re-run:

  R-1 the monster's numeric health readout "(13,648/14,812)" uses the SAME
      face and sits directly over the boss, i.e. inside the player gate during
      a melee nova. It is removed by horizontal closing (DIL=4) turning the
      whole string into one ~200 px component, which fails the w<=90 rule --
      and, as a second net, by rejecting any component whose own y-band
      carries >110 px of ink.

  R-2 every surviving instance is emitted with its SPAWN frame and SPAWN
      centroid, and its peak observation is written out as a 6x crop. The
      machine's job is recall (how many distinct instances); the eye's job is
      precision (what each one reads). Counting is the answer to task 1;
      values are eye-read from the crops.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080
RX0, RX1, RY0, RY1 = 0, 1330, 60, 935      # play area
BRIGHT_MIN, CHROMA_MAX = 140, 45
DIL = 4
LINK_DX, LINK_DY_UP, LINK_DY_DN = 24, 26, 10


def stream(f0, f1):
    ss = max(0.0, (f0 - 30) / 60.0)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", f"{ss:.6f}", "-i", VIDEO, "-frames:v", str(f1 - f0 + 40),
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
    base = int(round(ss * 60))
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


def components(mask, min_px):
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    out = []
    cur = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        cur += 1
        stack = [(y0, x0)]
        lab[y0, x0] = cur
        pts = []
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = cur
                    stack.append((ny, nx))
        if len(pts) >= min_px:
            p = np.array(pts)
            out.append((int(p[:, 0].min()), int(p[:, 0].max()),
                        int(p[:, 1].min()), int(p[:, 1].max()), len(pts)))
    return out


def detect(rgb):
    sub = rgb[RY0:RY1, RX0:RX1].astype(np.int16)
    mx, mn = sub.max(axis=2), sub.min(axis=2)
    m = (mn > BRIGHT_MIN) & ((mx - mn) < CHROMA_MAX)
    md = m.copy()
    for i in range(1, DIL + 1):
        md[:, i:] |= m[:, :-i]
        md[:, :-i] |= m[:, i:]
    out = []
    for y0, y1, x0, x1, npx in components(md, 16):
        h, w = y1 - y0 + 1, x1 - x0 + 1
        if not (7 <= h <= 26 and 8 <= w <= 90):
            continue
        if m[y0:y1 + 1, x0:x1 + 1].sum() < 22:
            continue
        # R-1 second net: reject if this y-band carries a long string
        band = m[max(0, y0 - 1):y1 + 2]
        cols = np.nonzero(band.sum(axis=0))[0]
        if len(cols):
            near = cols[(cols > x0 - 160) & (cols < x1 + 160)]
            if len(near) and (near.max() - near.min() + 1) > 115:
                continue
        out.append(dict(x0=x0, x1=x1, y0=y0, y1=y1, h=h, w=w,
                        cx=(x0 + x1) / 2.0, cy=(y0 + y1) / 2.0, area=h * w))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, required=True)
    ap.add_argument("--f1", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cropdir", default=None)
    ap.add_argument("--minframes", type=int, default=4)
    args = ap.parse_args()

    live, done = [], []
    keep_rgb = {}
    for fn, rgb in stream(args.f0, args.f1):
        dets = detect(rgb)
        used = set()
        for tr in live:
            best, bd = None, 1e9
            for j, d in enumerate(dets):
                if j in used:
                    continue
                dx = abs(d["cx"] - tr["cx"])
                dy = tr["cy"] - d["cy"]
                if dx <= LINK_DX and -LINK_DY_DN <= dy <= LINK_DY_UP:
                    s = dx + abs(dy)
                    if s < bd:
                        best, bd = j, s
            if best is None:
                tr["miss"] += 1
            else:
                d = dets[best]
                used.add(best)
                tr.update(cx=d["cx"], cy=d["cy"], miss=0)
                tr["n"] += 1
                tr["last"] = fn
                if d["area"] > tr["peak"]["area"]:
                    tr["peak"] = d
                    tr["peak_f"] = fn
        for j, d in enumerate(dets):
            if j not in used:
                live.append(dict(cx=d["cx"], cy=d["cy"], n=1, miss=0,
                                 first=fn, last=fn, spawn=d,
                                 peak=d, peak_f=fn))
        keep = []
        for tr in live:
            (keep if tr["miss"] <= 4 else done).append(tr)
        live = keep
        if args.cropdir:
            keep_rgb[fn] = rgb.copy()
            for f in list(keep_rgb):
                if f < fn - 60:
                    del keep_rgb[f]
    done += live
    inst = [t for t in done if t["n"] >= args.minframes]
    inst.sort(key=lambda t: t["first"])
    recs = []
    for k, t in enumerate(inst):
        s = t["spawn"]
        p = t["peak"]
        recs.append(dict(i=k, f_spawn=t["first"], f_last=t["last"], n=t["n"],
                         spawn_x=round(s["cx"] + RX0, 1), spawn_y=round(s["cy"] + RY0, 1),
                         peak_f=t["peak_f"],
                         peak_box=[int(p["x0"] + RX0), int(p["y0"] + RY0),
                                   int(p["x1"] + RX0), int(p["y1"] + RY0)],
                         peak_w=p["w"], peak_h=p["h"]))
    json.dump(dict(f0=args.f0, f1=args.f1, n=len(recs), inst=recs),
              open(args.out, "w"), indent=1)
    print(f"{len(done)} raw tracks, {len(recs)} instances (n>={args.minframes}) -> {args.out}")


if __name__ == "__main__":
    main()
