#!/usr/bin/env python3
"""KC2-PM2 Lap A helper: crop + upscale a region of a Grim Dawn screenshot so the
1920x1080 UI text is legible after the Read tool's downsample.

Usage: kc2_pm2_lap_a_crop.py <frame_number> <x> <y> <w> <h> [scale] [outname]
Coordinates are in full-resolution (1920x1080) pixel space.
Read-only on the source volume; writes into the Lap-A working dir.
"""
import os
import sys
from PIL import Image

SRC = "/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/screenshots"
OUT = os.path.join(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes",
    "2026-08-12-kc2-pm2-lap-a-player-sheet", "work", "crops",
)


def main(argv):
    if len(argv) < 6:
        print(__doc__)
        return 2
    n = int(argv[1])
    x, y, w, h = (int(v) for v in argv[2:6])
    scale = float(argv[6]) if len(argv) > 6 else 3.0
    name = argv[7] if len(argv) > 7 else f"f{n}-{x}_{y}_{w}_{h}"
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(os.path.join(SRC, f"Screenshot ({n}).png")).convert("RGB")
    c = im.crop((x, y, x + w, y + h))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    p = os.path.join(OUT, name + ".png")
    c.save(p)
    print(p, c.size)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
