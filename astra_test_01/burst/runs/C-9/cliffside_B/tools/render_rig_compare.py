#!/usr/bin/env python3
"""C-9 R-C9-40: OLD vs NEW E walk and E run, side by side, at one third speed.

Matt has to be able to SEE the two things he asked for -- that the thigh stays joined
to the hip at every frame, and that the foot rolls heel to toe instead of riding along
flat.  Neither is visible at 1x: the walk is 0.58 s per stride and the whole heel-toe
happens inside a quarter of that.  So the clip runs both rigs from the same clock at
one third speed, in step, with a ground line drawn so the plant can be checked by eye
against something fixed.

    python3 tools/render_rig_compare.py --old <tscn> --out <mp4>
"""
import argparse
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_rig_E import Rig, PROJ                     # noqa: E402

BG = np.array([0.105, 0.115, 0.145], np.float32)
SLOW = 3.0
FPS = 30


def panel(rig, clip, t, zoom, size, origin, label, sub):
    canvas, _ = rig.render(clip, t, zoom=zoom, origin=origin, size=size)
    a = canvas[..., 3:4]
    rgb = canvas[..., :3] * a + BG[None, None, :] * (1 - a)
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.line([(0, origin[1]), (size[0], origin[1])], fill=(120, 132, 160), width=1)
    d.text((10, 8), label, fill=(255, 236, 200))
    d.text((10, 22), sub, fill=(160, 176, 205))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", default=str(PROJ / "scenes" / "knight_rig_E.tscn"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--zoom", type=float, default=3.4)
    ap.add_argument("--loops", type=int, default=3)
    a = ap.parse_args()

    old, new = Rig(Path(a.old)), Rig(Path(a.new))
    W, H = 340, 520
    origin = (150, 452)
    tmp = Path(tempfile.mkdtemp(prefix="c9_rigcmp_"))
    n = 0
    for clip in ("walk", "run"):
        L = new.anims[clip]["length"]
        total = int(round(L * SLOW * FPS)) * a.loops
        for i in range(total):
            t = (i / float(FPS) / SLOW) % L
            po = panel(old, clip, t % old.anims[clip]["length"], a.zoom, (W, H), origin,
                       "BEFORE  —  E %s" % clip.upper(),
                       "flat sabaton, rectangular hip fill")
            pn = panel(new, clip, t, a.zoom, (W, H), origin,
                       "AFTER  —  E %s" % clip.upper(),
                       "heel-toe roll, disc hip + backdrop")
            im = Image.new("RGB", (W * 2 + 6, H + 26), (16, 18, 24))
            im.paste(po, (0, 0))
            im.paste(pn, (W + 6, 0))
            d = ImageDraw.Draw(im)
            d.text((8, H + 8), "1/3 speed   t = %.3f s of %.4f s   (%s)"
                   % (t, L, "one Keeper stride"), fill=(150, 165, 195))
            im.save(tmp / ("f_%05d.png" % n))
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(tmp / "f_%05d.png"), "-c:v", "libx264", "-pix_fmt",
                    "yuv420p", "-crf", "17", "-movflags", "+faststart", a.out],
                   check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout.strip()
    print("wrote %s  (%d frames, %s s)" % (a.out, n, dur))


if __name__ == "__main__":
    sys.exit(main())
