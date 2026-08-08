#!/usr/bin/env python3
"""Locate in-world monster HP readout strings `(current/max)` in Grim Dawn frames.

The readout is small white text (glyph height ~7 px, cap band ~9-10 px at 1920x1080)
rendered directly above a monster's health bar, anywhere in the play area. The scene
at Crucible wave 160 is a wall of coloured combat VFX; the discriminator that survives
it is *achromatic brightness*: min(R,G,B) is high only for white text, and low for
every saturated VFX colour.

This module LOCATES only. Every reported value is eye-read from a magnified crop.

  scan   <video> <t0> <t1> <fps> <outdir>     stream frames, dump blob crops + index
"""
import sys, os, json, subprocess
import numpy as np
from PIL import Image

W, H = 1920, 1080

# Whiteness gate. Text core sits at min-channel ~150-180 over the red arena; VFX
# saturated colours have min-channel far below this even when very bright.
MIN_CH = 135

# HUD rectangles (x0, y0, x1, y1) that carry white text which is NOT monster HP.
# Excluded to keep the eye-read sheets legible. Stated as a limit in the note.
HUD = [
    (0,    0,   300,  86),    # game clock
    (1150, 0,   1660, 210),   # wave badge / mutator row / score multiplier
    (1640, 20,  1920, 275),   # minimap disc
    (1600, 260, 1920, 380),   # objectives panel
    (0,    985, 1920, 1080),  # bottom HUD bar, globes, skill tray
]

MIN_W, MAX_W = 55, 300      # px; "(103,912/103,912)" ~ 165 px, 7-digit pair ~ 205 px
MIN_H, MAX_H = 5, 16
GAP = 6                     # horizontal dilation to bridge inter-character gaps


def in_hud(x0, y0, x1, y1):
    for a, b, c, d in HUD:
        if x0 >= a and x1 <= c and y0 >= b and y1 <= d:
            return True
        # partial overlap of >60% area also suppressed
        ox = max(0, min(x1, c) - max(x0, a))
        oy = max(0, min(y1, d) - max(y0, b))
        if ox * oy > 0.6 * max(1, (x1 - x0) * (y1 - y0)):
            return True
    return False


def blobs(frame):
    """frame: HxWx3 uint8. Returns list of (x0, y0, x1, y1) candidate text runs."""
    mn = frame.min(axis=2)
    m = mn > MIN_CH
    if not m.any():
        return []
    # horizontal dilation by GAP to join glyphs of one string
    d = m.copy()
    for k in range(1, GAP + 1):
        d[:, k:] |= m[:, :-k]
        d[:, :-k] |= m[:, k:]
    # vertical dilation by 1 to bridge the anti-aliased comma/apostrophe rows
    d[1:, :] |= d[:-1, :]
    d[:-1, :] |= d[1:, :]

    out = []
    lab = np.zeros(d.shape, dtype=np.int32)
    cur = 0
    ys, xs = np.where(d)
    seen = np.zeros(d.shape, dtype=bool)
    # iterative flood fill (stack) over the dilated mask
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        cur += 1
        stack = [(y0, x0)]
        seen[y0, x0] = True
        minx = maxx = x0
        miny = maxy = y0
        n = 0
        while stack:
            y, x = stack.pop()
            n += 1
            lab[y, x] = cur
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < d.shape[0] and 0 <= nx < d.shape[1] and d[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        w = maxx - minx + 1
        h = maxy - miny + 1
        if not (MIN_W <= w <= MAX_W and MIN_H <= h <= MAX_H):
            continue
        if in_hud(minx, miny, maxx, maxy):
            continue
        # density of true (undilated) white pixels inside the box: text is sparse
        core = m[miny:maxy + 1, minx:maxx + 1]
        dens = core.mean()
        if not (0.04 <= dens <= 0.55):
            continue
        out.append((int(minx), int(miny), int(maxx), int(maxy), round(float(dens), 3), int(n)))
    return out


def scan(video, t0, t1, fps, outdir):
    os.makedirs(outdir, exist_ok=True)
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nbytes = W * H * 3
    idx = []
    i = 0
    while True:
        buf = p.stdout.read(nbytes)
        if len(buf) < nbytes:
            break
        fr = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3)
        t = t0 + i / fps
        for (x0, y0, x1, y1, dens, n) in blobs(fr):
            idx.append({"t": round(t, 4), "box": [x0, y0, x1, y1],
                        "w": x1 - x0 + 1, "h": y1 - y0 + 1, "dens": dens})
        i += 1
        if i % 50 == 0:
            print(f"  ... {i} frames, {len(idx)} blobs", flush=True)
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "fps": fps,
               "min_ch": MIN_CH, "frames": i, "blobs": idx},
              open(os.path.join(outdir, "index.json"), "w"), indent=1)
    print(f"frames={i} blobs={len(idx)}")


if __name__ == "__main__":
    if sys.argv[1] == "scan":
        scan(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
             float(sys.argv[5]), sys.argv[6])
