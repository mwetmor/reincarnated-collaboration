#!/usr/bin/env python3
"""WR1-GAL-2 task 4a: whole-video scan for the top-centre BOSS/HERO nameplate bar.

Geometry is inherited verbatim from g8_bossbar.py (measured on the KIT-CAL-1
screenshot corpus, same 1920x1080 UI): the gold-framed trough's interior spans
x 799..1119 at y 61..74, bar mid-row y=68. A frame "carries a nameplate" when
>=20 columns of that interior read RED at >=5 rows.

Why this is the right instrument for the composition question: GD only draws
this bar for HERO/BOSS-tier monsters. Trash and ordinary packs render a small
over-head plate instead, which does not touch this trough. So bar-present is a
boss-grade proxy that does not require reading the monster's name.

Output: one JSON row per sampled frame that carries a bar.
"""
import json
import subprocess
import sys

import numpy as np

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
# strip covering nameplate text (y20..58) + trough (y61..74)
CX, CY, CW, CH = 600, 14, 720, 78
BAR_Y_IN = 68 - CY          # row of the bar inside the strip
TX0, TX1 = 799 - CX, 1119 - CX


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
        colhit = red.sum(axis=0) >= 5
        nlit = int(colhit.sum())
        if nlit >= 20:
            nz = np.nonzero(colhit)[0]
            rows.append(dict(pts=round(ss + i / fps, 3), lit=nlit,
                             right=int(nz.max()),
                             frac=round((int(nz.max()) + 1) / (TX1 - TX0 + 1), 4)))
        i += 1
        if i % 2000 == 0:
            print(f"  {ss + i/fps:.0f}s  hits={len(rows)}", file=sys.stderr, flush=True)
    p.stdout.close()
    p.wait()
    json.dump(dict(ss=ss, dur=dur, fps=fps, n_frames=i, rows=rows), open(out, "w"))
    print(f"{i} frames, {len(rows)} carry a nameplate bar -> {out}")


if __name__ == "__main__":
    main()
