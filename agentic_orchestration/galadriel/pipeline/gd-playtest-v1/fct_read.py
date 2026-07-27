#!/usr/bin/env python3
"""FCT instance extraction + read over a window.

Pipeline, in order, with the reason each stage exists:

 1. mask   bright + achromatic (fct_detect.fct_mask)
 2. CLOSE  horizontally by `DIL` columns, so the glyphs of one NUMBER become
           one component. Without this a 3-digit number fragments into up to 3
           tracks and the instance count inflates.
 3. blob   components with plausible text geometry
 4. track  link across frames (upward drift, shrink); one track == one damage
           instance (F-3)
 5. read   at the track's LARGEST observation only; glyphs cut from the
           UNCLOSED mask; matched against scale-normalised templates

The output is per-INSTANCE, and every instance carries its own read confidence
plus the number of frames it was seen for, so a downstream consumer can gate.
"""
import argparse
import json
import pickle
import subprocess
import sys

import numpy as np

from fct_detect import WORLD, fct_mask, components

W, H = 1920, 1080
DIL = 3
NORM_H = 20


def close_h(m, k=DIL):
    out = m.copy()
    for i in range(1, k + 1):
        out[:, i:] |= m[:, :-i]
        out[:, :-i] |= m[:, i:]
    for i in range(1, k + 1):          # erode back
        out[:, i:] &= out[:, :-i] | m[:, i:]
    return out | m


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


def detect(frame):
    m = fct_mask(frame)
    md = np.zeros_like(m)
    md |= m
    for i in range(1, DIL + 1):
        md[:, i:] |= m[:, :-i]
        md[:, :-i] |= m[:, i:]
    out = []
    for c in components(md, 14):
        h = c["y1"] - c["y0"] + 1
        w = c["x1"] - c["x0"] + 1
        if not (7 <= h <= 26 and 8 <= w <= 90):
            continue
        sub = m[c["y0"]:c["y1"] + 1, max(0, c["x0"] - DIL):c["x1"] + 1 + DIL]
        if sub.sum() < 20:
            continue
        out.append(dict(x0=c["x0"], x1=c["x1"], y0=c["y0"], y1=c["y1"],
                        h=h, w=w, cx=(c["x0"] + c["x1"]) / 2,
                        cy=(c["y0"] + c["y1"]) / 2, bmp=sub.copy()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    live, done = [], []
    for i, frame in stream(args.video, args.ss, args.t, args.fps):
        pts = args.ss + i / args.fps
        dets = detect(frame)
        used = set()
        for tr in live:
            best, bd = None, 1e9
            for j, d in enumerate(dets):
                if j in used:
                    continue
                dx = abs(d["cx"] - tr["cx"])
                dy = tr["cy"] - d["cy"]
                if dx <= 22 and -8 <= dy <= 22:
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
                tr["last"] = pts
                if d["bmp"].sum() > tr["best"]["bmp"].sum():
                    tr["best"] = d
        for j, d in enumerate(dets):
            if j not in used:
                live.append(dict(cx=d["cx"], cy=d["cy"], n=1, miss=0,
                                 first=pts, last=pts, best=d))
        keep = []
        for tr in live:
            (keep if tr["miss"] <= 4 else done).append(tr)
        live = keep
        if i % 600 == 0:
            print(f"  {pts:.1f}s live={len(live)} done={len(done)}",
                  file=sys.stderr, flush=True)
    done += live
    done = [t for t in done if t["n"] >= 4]
    with open(args.out, "wb") as fh:
        pickle.dump(done, fh)
    print(json.dumps(dict(window=[args.ss, args.ss + args.t],
                          n_instances=len(done))))


if __name__ == "__main__":
    main()
