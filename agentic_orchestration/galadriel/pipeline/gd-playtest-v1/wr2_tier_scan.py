#!/usr/bin/env python3
"""WR1-GAL-2 task 4c: HERO/BOSS-TIER detector on the top-centre nameplate.

Grim Dawn's nameplate for a normal monster is: NAME line, then the trough bar
with the level numeral centred in it. For a hero/boss it additionally renders a
FACTION/TIER SUBTITLE on its own line UNDER the bar -- the Primordian's plate
reads "Primordian, the Forgotten One" / [bar] / "Beastkin" (verified by eye at
f309084, evidence/plates-*.jpg).

So tier is decidable without OCR: measure ink in the subtitle band (y 78..98,
x 780..1140) on frames that carry a bar. Normal-tier plates leave that band
empty; hero/boss plates do not.

Reported per sampled frame so the caller can see the raw series rather than a
verdict.
"""
import json
import subprocess
import sys

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
CX, CY, CW, CH = 600, 14, 720, 92
BAR_Y_IN = 68 - CY
TX0, TX1 = 799 - CX, 1119 - CX
SUB_Y0, SUB_Y1 = 78 - CY, 98 - CY
SUB_X0, SUB_X1 = 780 - CX, 1140 - CX


def main():
    ss, dur, fps, out = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox", "-ss", str(ss), "-i", VIDEO, "-t", str(dur),
           "-vf", f"fps={fps},crop={CW}:{CH}:{CX}:{CY}", "-pix_fmt", "rgb24",
           "-f", "rawvideo", "-"]
    n = CW * CH * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 8)
    rows, i = [], 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, dtype=np.uint8).reshape(CH, CW, 3).astype(np.int16)
        strip = a[BAR_Y_IN - 4:BAR_Y_IN + 5, TX0:TX1 + 1]
        red = ((strip[:, :, 0] > 90) & (strip[:, :, 0] - strip[:, :, 1] > 55)
               & (strip[:, :, 0] - strip[:, :, 2] > 45))
        nlit = int((red.sum(axis=0) >= 5).sum())
        if nlit >= 20:
            sub = a[SUB_Y0:SUB_Y1, SUB_X0:SUB_X1]
            mn = sub.min(axis=2)
            mx = sub.max(axis=2)
            ink = int(((mn > 120) & ((mx - mn) < 70)).sum())
            cols = int((((mn > 120) & ((mx - mn) < 70)).sum(axis=0) > 0).sum())
            rows.append(dict(pts=round(ss + i / fps, 3), lit=nlit,
                             sub_ink=ink, sub_cols=cols))
        i += 1
    p.stdout.close()
    p.wait()
    json.dump(dict(ss=ss, dur=dur, fps=fps, n=i, rows=rows), open(out, "w"))
    print(f"{i} frames, {len(rows)} with a bar -> {out}")


if __name__ == "__main__":
    main()
