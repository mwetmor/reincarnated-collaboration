#!/usr/bin/env python3
"""Measure the plate health-bar TRACK geometry per rank, from the pixels.

Method (same as the w152 skull-plate note s 4.1, which measured the BOSS track):
  - fill left edge  : first column of the FILL_BAND rows whose redness run starts
  - track inner right edge : the gold end-cap ornament's warm onset, i.e. the
    column where (R-B) of the bevel/ornament rows jumps clear of the dark track
Reports both, per frame, with the column profiles so nothing is hidden.
"""
import subprocess
import sys

import numpy as np

W, H = 1920, 1080
FY0, FY1 = 66, 73          # FILL_BAND rows
BY0, BY1 = 59, 65          # BEVEL_BAND rows
X0, X1 = 760, 1180


def frame(video, t):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b[:W * H * 3], np.uint8).reshape(H, W, 3)


def profile(fr):
    a = fr.astype(np.int16)
    fill = a[FY0:FY1, X0:X1]
    R, G, B = fill[:, :, 0], fill[:, :, 1], fill[:, :, 2]
    red = ((R > 70) & (R - G > 40) & (R - B > 40)).sum(0)
    redness = (R - np.maximum(G, B)).mean(0)
    bev = a[BY0:BY1, X0:X1]
    warm = (bev[:, :, 0] - bev[:, :, 2]).mean(0)
    bright = bev.max(2).mean(0)
    return red, redness, warm, bright


def report(video, ts, label):
    print(f"\n===== {label} =====")
    for t in ts:
        fr = frame(video, t)
        red, redness, warm, bright = profile(fr)
        cols = np.nonzero(red >= 5)[0]
        # left-anchored run
        if cols.size:
            lo = cols[0]
            cur = lo
            for v in cols[1:]:
                if v - cur <= 4:
                    cur = v
                else:
                    break
            fill0, fill1 = X0 + lo, X0 + cur
        else:
            fill0 = fill1 = None
        # gold end-cap: first column right of the fill where bevel brightness
        # rises above 90 AND stays for >= 3 columns
        cap = None
        if fill1:
            for x in range(fill1 - X0 + 1, X1 - X0 - 4):
                if (bright[x:x + 4] > 95).all():
                    cap = X0 + x
                    break
        print(f"t={t:<10} fill {fill0}..{fill1}  gold-cap-onset {cap}")
        print("   red-cols  " + " ".join(f"{X0+i}:{int(red[i])}" for i in range(0, X1 - X0)
                                         if red[i] >= 3)[:0] or "", end="")
        # compact: print red run summary + bright profile near the right end
        seg = [(X0 + i, int(bright[i]), int(warm[i])) for i in range(X1 - X0)
               if 1040 <= X0 + i <= 1140]
        print("   bright/warm 1040..1140: " + " ".join(f"{x}:{b}/{w}" for x, b, w in seg))


if __name__ == "__main__":
    v = "/tmp/kc2-s2.mp4"
    report(v, [701.7333, 701.7667, 701.8, 701.9333], "CRABLING (common / white)")
    report(v, [704.4667, 704.5333, 704.6333], "ROTMOUTH (hero / orange)")
    report(v, [701.9667, 702.0667, 702.3333], "champion neighbour (partial bar)")
    report(v, [706.8, 712.4], "BOSS (Haraxis) - control")
