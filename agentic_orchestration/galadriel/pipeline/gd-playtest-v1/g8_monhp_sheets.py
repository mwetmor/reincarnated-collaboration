#!/usr/bin/env python3
"""
KIT-CAL-1 G-8: contact-sheet every plausible in-world numeric-HP band so the
whole set can be read by eye in a handful of passes.

The inline paren test in g8_monhp.py is TOO STRICT and drops real readouts --
verified against the first triage sheet, which showed "(2,184/4,702)" and
"(434/434)" on frames the paren test rejected. The cause is band merging: when
a health readout renders close to other bright text, the row-run detector
returns one band whose first/last groups are not the parentheses. Rather than
re-tune a shape heuristic against a moving target, ALL bands in the geometric
envelope of a health readout are sheeted and read.

Envelope (measured on the confirmed f281 read, "(13,571/14,812)": 146x13 px,
15 ink groups): height 12-15, width 55-200, groups 8-20.

Cheap-first: the bboxes are already banked in g8-monhp-candidates.json, so this
pass decodes each source frame ONCE and never re-runs detection.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-kitcal1-g8")

H_LO, H_HI = 12, 15
W_LO, W_HI = 55, 200
G_LO, G_HI = 8, 20

TILE_W, TILE_H, COLS = 620, 46, 2


def main():
    cands = json.load(open(OUT / "g8-monhp-candidates.json"))
    picks = []
    for fid in sorted(cands, key=int):
        for k, b in enumerate(cands[fid]):
            if (H_LO <= b["h"] <= H_HI and W_LO <= b["w"] <= W_HI
                    and G_LO <= b["n_groups"] <= G_HI):
                picks.append((int(fid), k, b))
    print(f"{len(picks)} bands in the health-readout envelope")

    tiles = []
    cur_fid, im = None, None
    for fid, k, b in picks:
        if fid != cur_fid:
            if im is not None:
                im.close()
            im = Image.open(SRC / f"Screenshot ({fid}).png").convert("RGB")
            cur_fid = fid
        c = im.crop((b["x0"] - 8, b["y0"] - 5, b["x1"] + 8, b["y1"] + 5))
        c = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
        tiles.append((f"f{fid}-{k}", c))

    rows = (len(tiles) + COLS - 1) // COLS
    sheet_rows = 12
    n_sheets = (rows + sheet_rows - 1) // sheet_rows
    for s in range(n_sheets):
        sub = tiles[s * sheet_rows * COLS:(s + 1) * sheet_rows * COLS]
        sh = Image.new("RGB", (COLS * TILE_W, sheet_rows * TILE_H), (18, 18, 18))
        d = ImageDraw.Draw(sh)
        for i, (name, t) in enumerate(sub):
            x, y = (i % COLS) * TILE_W, (i // COLS) * TILE_H
            t.thumbnail((TILE_W - 90, TILE_H - 4))
            sh.paste(t, (x + 86, y + 2))
            d.text((x + 4, y + 16), name, fill=(255, 220, 0))
        sh.save(OUT / f"g8-monhp-sheet-{s}.png")
        print(f"  sheet {s}: {len(sub)} tiles")


if __name__ == "__main__":
    main()
