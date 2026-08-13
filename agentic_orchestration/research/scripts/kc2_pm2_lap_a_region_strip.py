#!/usr/bin/env python3
"""KC2-PM2 Lap A helper: tile the SAME screen region across a range of frames so a
UI state change (e.g. which character-sheet tab is active) can be spotted in one look.

Usage: kc2_pm2_lap_a_region_strip.py <first> <last> <x> <y> <w> <h> <cols> <outname>
Read-only on the source volume; writes into the Lap-A working dir.
"""
import os
import sys
from PIL import Image, ImageDraw

SRC = "/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/screenshots"
OUT = os.path.join(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes",
    "2026-08-12-kc2-pm2-lap-a-player-sheet", "work", "strips",
)


def main(argv):
    if len(argv) < 9:
        print(__doc__)
        return 2
    first, last, x, y, w, h, cols = (int(v) for v in argv[1:8])
    name = argv[8]
    os.makedirs(OUT, exist_ok=True)
    nums = list(range(first, last + 1))
    rows = (len(nums) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i, n in enumerate(nums):
        p = os.path.join(SRC, f"Screenshot ({n}).png")
        if not os.path.exists(p):
            continue
        c = Image.open(p).convert("RGB").crop((x, y, x + w, y + h))
        px, py = (i % cols) * w, (i // cols) * h
        sheet.paste(c, (px, py))
        d.rectangle([px, py, px + 34, py + 12], fill=(0, 0, 0))
        d.text((px + 2, py + 2), str(n), fill=(255, 255, 0))
    out = os.path.join(OUT, name + ".png")
    sheet.save(out)
    print(out, sheet.size)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
