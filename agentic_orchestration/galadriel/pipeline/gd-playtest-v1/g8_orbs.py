#!/usr/bin/env python3
"""
KIT-CAL-1 G-8: read BOTH orbs' numerals (cur/max) off every still in the
play-test-v1 screenshot corpus.

The T-A globe reader (`globe_ocr.GlobeReader`) is reused unchanged for the
health orb. The mana orb sits at the mirrored screen position -- the HUD is
symmetric about x=960 -- so the same reader is run a second time over a
mirrored crop window. Nothing about the glyph model changes; only the crop.

Why read BOTH operands here, when globe_series.py deliberately read only the
left one: globe_series ran inside a single death window where max HP is a
constant by construction. This pass spans the WHOLE run, across level-ups and
a gear step, so max HP is precisely the quantity in question. The greedy
native-width matcher in GlobeReader.read() handles the '/'-to-digit merge that
made per-segment reading unsafe; that is why read() and not read_left().
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import globe_ocr  # noqa: E402
from globe_ocr import GlobeReader  # noqa: E402

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-kitcal1-g8")
TMPL = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
            "galadriel/captures/2026-07-26-gd-playtest-v1-r2/globe-digit-templates.json")

HP_CROP = dict(globe_ocr.CROP)
# mirrored about x=960: 1920 - 584 - 118 = 1218
MANA_CROP = dict(x=1218, y=HP_CROP["y"], w=HP_CROP["w"], h=HP_CROP["h"])


def read_at(reader, frame, crop):
    globe_ocr.CROP = crop
    return reader.read(frame)


def main():
    r = GlobeReader(json.load(open(TMPL)))
    ids = sorted(int(f.name[12:-5]) for f in SRC.iterdir()
                 if f.name.startswith("Screenshot (") and f.name.endswith(").png"))
    recs = {}
    for i in ids:
        with Image.open(SRC / f"Screenshot ({i}).png") as im:
            arr = np.asarray(im.convert("RGB"))
        hp, hs, hc = read_at(r, arr, HP_CROP)
        mp, ms, mc = read_at(r, arr, MANA_CROP)
        recs[i] = {"hp": hp, "hp_raw": hs, "hp_conf": round(hc, 3),
                   "mana": mp, "mana_raw": ms, "mana_conf": round(mc, 3)}
        print(f"f{i:4d}  hp={str(hp):>12s} ({hs!r} {hc:.2f})   "
              f"mana={str(mp):>12s} ({ms!r} {mc:.2f})", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "g8-orbs-all.json", "w") as f:
        json.dump(recs, f, indent=1)


if __name__ == "__main__":
    main()
