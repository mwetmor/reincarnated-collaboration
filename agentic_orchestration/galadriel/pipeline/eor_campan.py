#!/usr/bin/env python3
"""Per-frame camera translation for the Grim Dawn fixture footage.

Every screen-space velocity measured off this footage is contaminated by camera
pan -- the camera tracks the player, so a body standing still translates on screen
whenever the player moves. Nothing about monster kinematics is measurable until the
pan is removed. This module measures it.

Method: integer-pixel SAD registration of consecutive frames on the achromatic
luma of a scene band, at 1/4 resolution with a +/-6 (=+/-24 full-px) search, then a
full-resolution +/-3 refinement around the coarse winner. Combat VFX is masked out
of the cost by weighting each pixel by 1/(1+saturation): saturated fire/ice/lightning
moves independently of the camera and would otherwise dominate the cost.

Outputs per frame: (dx, dy) in full-resolution pixels, plus `resid`, the normalised
SAD at the winner. High resid = the registration did not lock (a screen-filling VFX
flash, a scene cut); those frames are reported, never silently interpolated.

A frame is CAMERA-STATIC when |dx| <= 1 and |dy| <= 1. In static runs, screen motion
IS world motion, and monster speeds can be read directly.

  pan <video> <t0> <t1> <out.json>
"""
import sys, subprocess, json
import numpy as np

W, H = 1920, 1080
FPS = 60.0
BAND = (120, 940, 60, 1860)      # y0, y1, x0, x1 -- play area, HUD and minimap excluded
DS = 4                           # coarse downsample
COARSE = 6                       # +/- steps at DS resolution
FINE = 3


def prep(fr):
    a = fr[BAND[0]:BAND[1], BAND[2]:BAND[3]].astype(np.float32)
    mx = a.max(axis=2); mn = a.min(axis=2)
    lum = mn                                        # achromatic component
    sat = (mx - mn) / (mx + 1.0)
    wgt = 1.0 / (1.0 + 6.0 * sat)                   # suppress saturated VFX
    return lum, wgt


def sad(a, wa, b, wb, dx, dy):
    """cost of aligning b shifted by (dx,dy) onto a."""
    h, w = a.shape
    y0a, y1a = max(0, dy), min(h, h + dy)
    x0a, x1a = max(0, dx), min(w, w + dx)
    y0b, y1b = y0a - dy, y1a - dy
    x0b, x1b = x0a - dx, x1a - dx
    if y1a - y0a < h // 2 or x1a - x0a < w // 2:
        return 1e18
    d = np.abs(a[y0a:y1a, x0a:x1a] - b[y0b:y1b, x0b:x1b])
    wgt = wa[y0a:y1a, x0a:x1a] * wb[y0b:y1b, x0b:x1b]
    return float((d * wgt).sum() / wgt.sum())


def pan(video, t0, t1, out):
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nb = W * H * 3
    prev = None
    rows = []
    i = 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        lum, wgt = prep(fr)
        cur = (lum[::DS, ::DS].copy(), wgt[::DS, ::DS].copy(), lum, wgt)
        if prev is not None:
            best, bdx, bdy = 1e18, 0, 0
            for dy in range(-COARSE, COARSE + 1):
                for dx in range(-COARSE, COARSE + 1):
                    c = sad(prev[0], prev[1], cur[0], cur[1], dx, dy)
                    if c < best:
                        best, bdx, bdy = c, dx, dy
            fdx, fdy = bdx * DS, bdy * DS
            best2, b2x, b2y = 1e18, fdx, fdy
            sl = (slice(None, None, 2), slice(None, None, 2))
            pa, pw = prev[2][sl], prev[3][sl]
            ca, cw = cur[2][sl], cur[3][sl]
            for dy in range(fdy // 2 - FINE, fdy // 2 + FINE + 1):
                for dx in range(fdx // 2 - FINE, fdx // 2 + FINE + 1):
                    c = sad(pa, pw, ca, cw, dx, dy)
                    if c < best2:
                        best2, b2x, b2y = c, dx * 2, dy * 2
            rows.append({"f": i, "t": round(t0 + i / FPS, 5),
                         "dx": b2x, "dy": b2y, "resid": round(best2, 3)})
        prev = cur
        i += 1
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "frames": i, "pan": rows},
              open(out, "w"))
    if rows:
        r = np.array([x["resid"] for x in rows])
        st = sum(1 for x in rows if abs(x["dx"]) <= 2 and abs(x["dy"]) <= 2)
        print(f"pan {t0}-{t1}: {i} frames, static {st} ({100*st/len(rows):.1f}%), "
              f"resid med {np.median(r):.2f} p95 {np.percentile(r,95):.2f}")


if __name__ == "__main__":
    pan(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
