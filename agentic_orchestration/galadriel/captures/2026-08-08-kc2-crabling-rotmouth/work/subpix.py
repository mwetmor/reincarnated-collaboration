#!/usr/bin/env python3
"""Sub-pixel fill-edge estimate for the plate health bar.

Why. The run-walk estimator in eor_platebind quantises the fill edge to an integer
column. On the champion/hero/common track (~197 px long) one column is 0.51 % of
the bar, which is coarse enough that a body at 98.9 % and a body at 100 % can land
on adjacent columns. This estimator interpolates the antialiased edge instead.

Method. Redness profile r(x) = mean over the FILL_BAND rows of (R - max(G,B)).
Inside the fill r is high and flat; right of the edge it is low and flat. Take the
left plateau as the median of r over [x_fill_start+6, edge-4] and the right plateau
as the median over [edge+4, edge+20], then find the sub-pixel x where r crosses the
midpoint, by linear interpolation between the bracketing columns.

Reported with both plateaus so the estimate can be judged, and refused (None) when
the two plateaus are closer than `min_step`.
"""
import subprocess
import sys

import numpy as np

W, H = 1920, 1080
FY0, FY1 = 66, 73


def frame(video, t):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b[:W * H * 3], np.uint8).reshape(H, W, 3)


def redness(fr, x_lo, x_hi):
    a = fr.astype(np.int16)[FY0:FY1, x_lo:x_hi]
    return (a[:, :, 0] - np.maximum(a[:, :, 1], a[:, :, 2])).mean(0)


def edge(fr, track_x0, x_hi, min_step=14.0):
    x_lo = int(track_x0) - 4
    r = redness(fr, x_lo, x_hi)
    xs = np.arange(x_lo, x_hi)
    # coarse edge: largest negative gradient
    g = np.diff(r)
    k = int(np.argmin(g))
    ec = xs[k]
    li = (xs >= track_x0 + 6) & (xs <= ec - 4)
    ri = (xs >= ec + 4) & (xs <= ec + 22)
    if li.sum() < 3 or ri.sum() < 3:
        return None, None, None
    lp, rp = float(np.median(r[li])), float(np.median(r[ri]))
    if lp - rp < min_step:
        return None, lp, rp
    mid = (lp + rp) / 2.0
    # walk right from the left plateau to the first crossing below mid
    idx = np.nonzero((xs > track_x0 + 6) & (r < mid))[0]
    if idx.size == 0:
        return None, lp, rp
    j = idx[0]
    x1, y1 = xs[j], r[j]
    x0, y0 = xs[j - 1], r[j - 1]
    xe = x0 + (y0 - mid) * (x1 - x0) / (y0 - y1) if y0 != y1 else float(x0)
    return float(xe), lp, rp


CASES = [
    # label, ts, track_x0, track_x1, x_hi
    ("CRABLING  L108", [701.7333, 701.7667, 701.8], 862.0, 1059.0, 1110),
    ("CRABLING  L107", [701.9333], 862.0, 1059.0, 1110),
    ("ROTMOUTH  L107", [704.4667, 704.5, 704.5333, 704.5667, 704.6, 704.6333, 704.6667],
     862.0, 1059.0, 1110),
    ("champ neighbour (drain)", [701.9667, 702.0, 702.0667, 702.3333, 702.4667, 702.5333],
     862.0, 1059.0, 1110),
    ("plant 698.7-699.13", [698.7, 698.8, 698.9, 699.0, 699.1333], 862.0, 1059.0, 1110),
    ("BOSS control", [706.6333, 706.8, 706.9, 712.4, 712.6], 800.0, 1121.5, 1180),
]

if __name__ == "__main__":
    v = "/tmp/kc2-s2.mp4"
    for lab, ts, x0, x1, xh in CASES:
        print(f"\n== {lab}   track {x0} -> {x1}  ({x1-x0:.1f} px)")
        for t in ts:
            fr = frame(v, t)
            xe, lp, rp = edge(fr, x0, xh)
            if xe is None:
                print(f"   t={t:<10} REFUSED  plateaus L={lp} R={rp}")
                continue
            f = (xe - x0) / (x1 - x0)
            print(f"   t={t:<10} edge={xe:8.2f}  frac={f:7.4f}   plateau L={lp:6.1f} R={rp:6.1f}")
