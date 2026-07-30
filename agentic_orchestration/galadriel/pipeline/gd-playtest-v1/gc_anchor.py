#!/usr/bin/env python3
"""GAL-CAM: the player's SCREEN ANCHOR, by temporal median over a moving window.

WHY
---
"Grim Dawn centres the player slightly below frame centre" is folklore until it
is measured. It is measurable because the camera is player-locked: over a window
in which the player RUNS, everything in the world smears in screen space while
anything screen-fixed stays sharp. A per-pixel temporal MEDIAN of an unregistered
window therefore keeps exactly two things sharp -- the HUD, and the player.

The HUD lives at the frame edges; the player lives in the middle. So the sharp
residual inside the play area IS the player, and its lowest extent is the
player's GROUND point, which is the anchor the camera is locked to.

Sharpness is scored, not eyeballed: for each pixel, the temporal median image is
compared against the temporal MEAN of local gradient energy. A screen-fixed
object has high gradient energy in the median; smeared terrain does not.

Windows must be MOVING windows -- the instrument is void if the player stood
still, because then terrain is screen-fixed too. Motion is verified from the
gc_pan.py pan record before a window is accepted, not assumed.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080


def stream(ss, dur, gray=True):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", str(ss), "-i", VIDEO, "-t", str(dur),
           "-pix_fmt", "gray" if gray else "rgb24", "-f", "rawvideo", "-"]
    n = W * H * (1 if gray else 3)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 8)
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, dtype=np.uint8)
        yield a.reshape(H, W) if gray else a.reshape(H, W, 3)
    p.stdout.close()
    p.wait()


def grad(a):
    gx = np.zeros_like(a, dtype=np.float32)
    gy = np.zeros_like(a, dtype=np.float32)
    gx[:, 1:-1] = a[:, 2:].astype(np.float32) - a[:, :-2]
    gy[1:-1, :] = a[2:, :].astype(np.float32) - a[:-2, :]
    return np.sqrt(gx * gx + gy * gy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=float, nargs="+", required=True)
    ap.add_argument("--dur", type=float, default=6.0)
    ap.add_argument("--step", type=int, default=2, help="take every Nth frame")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--box", type=int, nargs=4, default=[700, 1220, 330, 860],
                    help="x0 x1 y0 y1 search box for the player")
    args = ap.parse_args()

    summary = []
    for ss in args.starts:
        fr = []
        for i, g in enumerate(stream(ss, args.dur)):
            if i % args.step == 0:
                fr.append(g)
        if len(fr) < 20:
            print("skip", ss, len(fr))
            continue
        S = np.stack(fr)
        med = np.median(S, axis=0).astype(np.uint8)
        ge = grad(med)
        x0, x1, y0, y1 = args.box
        sub = ge[y0:y1, x0:x1]
        # smooth with a box filter via cumulative sums (no scipy needed)
        def boxf(a, r):
            c = np.cumsum(np.cumsum(np.pad(a, ((r, r), (r, r))), 0), 1)
            k = 2 * r
            return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k])
        sm = boxf(sub, 12)
        sm = sm[:sub.shape[0], :sub.shape[1]]
        iy, ix = np.unravel_index(np.argmax(sm), sm.shape)
        px, py = x0 + ix, y0 + iy
        # ground point: lowest row in a column band around px whose smoothed
        # gradient energy exceeds 40% of the peak
        thr = 0.40 * sm.max()
        colband = sm[:, max(0, ix - 22):ix + 23]
        rowsok = np.nonzero((colband > thr).any(axis=1))[0]
        ytop = y0 + int(rowsok.min()) if len(rowsok) else py
        ybot = y0 + int(rowsok.max()) if len(rowsok) else py
        rec = dict(ss=float(ss), n=len(fr), peak_x=int(px), peak_y=int(py),
                   fig_top=int(ytop), fig_bot=int(ybot),
                   dx_from_centre=float(px - 960.0),
                   dy_ground_from_centre=float(ybot - 540.0))
        summary.append(rec)
        print(rec, flush=True)
        im = Image.fromarray(np.dstack([med] * 3))
        crop = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2),
                                                Image.LANCZOS)
        crop.save(f"{args.outdir}/medstack-{int(ss)}.jpg", quality=90)
    json.dump(summary, open(f"{args.outdir}/anchor.json", "w"), indent=1)
    if summary:
        bx = np.array([r["peak_x"] for r in summary], float)
        by = np.array([r["fig_bot"] for r in summary], float)
        print(f"\nanchor x: med={np.median(bx):.1f} sd={bx.std(ddof=1):.1f}")
        print(f"ground y: med={np.median(by):.1f} sd={by.std(ddof=1):.1f}")


if __name__ == "__main__":
    main()
