#!/usr/bin/env python3
"""KC2-PM2 Lap A helper: build contact sheets from the eor-test-2 screenshot corpus
so UI-bearing frames (character sheet / tooltips / skill windows) can be spotted
cheaply before high-resolution crops are taken.

Read-only on the source volume. Writes only into the Lap-A working dir.
"""
import os
import sys
from PIL import Image, ImageDraw

SRC = "/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/screenshots"
OUT = os.path.join(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes",
    "2026-08-12-kc2-pm2-lap-a-player-sheet", "work", "contact",
)

TILE_W, TILE_H = 480, 270
COLS, ROWS = 4, 4


def frames():
    out = []
    for name in os.listdir(SRC):
        if not name.lower().endswith(".png"):
            continue
        num = "".join(ch for ch in name if ch.isdigit())
        if num:
            out.append((int(num), os.path.join(SRC, name)))
    return sorted(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    fr = frames()
    per = COLS * ROWS
    for s in range(0, len(fr), per):
        chunk = fr[s:s + per]
        sheet = Image.new("RGB", (TILE_W * COLS, TILE_H * ROWS), (0, 0, 0))
        d = ImageDraw.Draw(sheet)
        for i, (num, path) in enumerate(chunk):
            im = Image.open(path).convert("RGB").resize((TILE_W, TILE_H), Image.LANCZOS)
            x, y = (i % COLS) * TILE_W, (i // COLS) * TILE_H
            sheet.paste(im, (x, y))
            d.rectangle([x, y, x + 62, y + 18], fill=(0, 0, 0))
            d.text((x + 4, y + 4), str(num), fill=(255, 255, 0))
        first, last = chunk[0][0], chunk[-1][0]
        p = os.path.join(OUT, f"contact-{first}-{last}.png")
        sheet.save(p)
        print(p)


if __name__ == "__main__":
    sys.exit(main())
