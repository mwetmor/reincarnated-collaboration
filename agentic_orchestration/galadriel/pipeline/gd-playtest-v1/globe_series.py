#!/usr/bin/env python3
"""Read CURRENT HP from the health globe at high frame rate over a window.

Scope note: this reads the LEFT operand only (current HP). Max HP is read once
per window and asserted constant -- inside a death window there is no level-up,
so max HP is a constant and re-reading it every frame only adds a failure mode
(the '/4' glyph merge documented in globe_ocr).

Per-segment matching is safe HERE and only here: in this window the three
current-HP digits are separated by >=3 blank columns; the only merge in the
string is at the '/'-to-first-max-digit boundary, which we do not read.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

from globe_ocr import CROP, mask_of, segments, iou


def stream(video, ss, t, fps):
    c = CROP
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", str(ss), "-i", video, "-t", str(t),
           "-vf", f"fps={fps},crop={c['w']}:{c['h']}:{c['x']}:{c['y']}",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = c["h"] * c["w"] * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 8)
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield i, np.frombuffer(b, dtype=np.uint8).reshape(c["h"], c["w"], 3)
        i += 1
    p.stdout.close()
    p.wait()


def read_left(sub, tmpl, ndig_max=4, min_iou=0.72):
    m = mask_of(sub)
    ys, xs = np.nonzero(m)
    if not len(ys):
        return None, 0.0, "NO_INK"
    y0, y1 = ys.min(), ys.max()
    if y1 - y0 + 1 > 16:
        return None, 0.0, "TALL"
    band = m[y0:y1 + 1]
    segs = [(a, b) for a, b in segments(band)
            if b - a + 1 >= 2 and band[:, a:b + 1].sum() >= 8]
    if len(segs) < 4:
        return None, 0.0, f"NSEG{len(segs)}"
    # digits run until the first WIDE segment (the '/'+digit merge) or a '/'
    out, confs = [], []
    for a, b in segs:
        g = band[:, a:b + 1]
        best, bv = None, -1.0
        for ch, tl in tmpl.items():
            for t in tl:
                v = iou(g, t)
                if v > bv:
                    best, bv = ch, v
        if best == "/" or (b - a + 1) > 10:
            break
        if bv < min_iou or best is None or not best.isdigit():
            return None, bv, "LOWCONF"
        out.append(best)
        confs.append(bv)
        if len(out) > ndig_max:
            return None, min(confs), "TOOLONG"
    if not out:
        return None, 0.0, "NODIG"
    return int("".join(out)), min(confs), "OK"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--templates", required=True)
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    tmpl = {k: [np.array(b, dtype=bool) for b in v]
            for k, v in json.load(open(args.templates)).items()}
    with open(args.out, "w") as fh:
        for i, sub in stream(args.video, args.ss, args.t, args.fps):
            hp, conf, st = read_left(sub, tmpl)
            fh.write(json.dumps(dict(pts_s=round(args.ss + i / args.fps, 4),
                                     hp=hp, conf=round(float(conf), 3),
                                     st=st)) + "\n")
            if i % 1200 == 0:
                print(f"  {args.ss + i / args.fps:.1f}s hp={hp} {st}",
                      file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
