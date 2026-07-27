#!/usr/bin/env python3
"""
Harvest digit glyph templates and skill-path signatures from a native
screenshot whose values are known by human read.

Templates are stored at NATIVE glyph width (ROW_H x w), because the reader
matches greedily at native width (panel_ocr G-3). Any harvested group wider
than MAX_GLYPH_W is two touching digits and is rejected rather than banked.

Ground truth used (Screenshot (352).png, play_time 118:08) -- every value was
read by galadriel from a tight native crop at 1.6x and independently matches
gandalf's verification-note §6b table:

    play_time 118 min 8 sec | total_score 0 | deaths 2 | kills 882
    health_potions 0 | mana_potions 0 | max_level 12 | dps 0.00
    defaultkickattack 19 | defaultweaponattack 74 | onslaught 54
    werewolf1 12 | werewolf1_skill01_claws 358 | werewolf1_skill02_charge 175
    life_healed 12468.06 | shield_block_chance 18.00
"""

import argparse
import json

import numpy as np
from PIL import Image

from panel_ocr import ROW_H, SKILL_INDENT, detect_L, segment, text_mask

MAX_GLYPH_W = 8

# (row y, x-search-start offset from L or None for a skill row, literal)
DIGIT_SOURCES = [
    (134, 129, "882"),        # kills            -> 8, 2
    (374, None, "358"),       # claws            -> 3, 5
    (394, None, "175"),       # charge           -> 1, 7
    (414, 88,  "12468.06"),   # life healed      -> 4, 6, ., 0
    (294, None, "19"),        # kick             -> 9
    (314, None, "74"),        # weapon attack    -> 7
]

SKILL_ROWS = {
    294: "defaultkickattack",
    314: "defaultweaponattack",
    334: "onslaught",
    354: "werewolf1",
    374: "werewolf1_skill01_claws",
    394: "werewolf1_skill02_charge",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--append-to", default=None,
                    help="merge into an existing model (banks a second "
                         "template set for the other capture instrument)")
    args = ap.parse_args()

    rgb = np.asarray(Image.open(args.shot).convert("RGB")).astype(np.int16)
    mask = text_mask(rgb)
    L = detect_L(mask)
    print("panel left edge L =", L)

    digits = {}

    def harvest(y, x0, literal):
        # split into single glyphs on ANY blank column; reject merged blobs
        groups = segment(mask, y, x0, 1915, gap=1)
        cluster = [groups[0]] if groups else []
        for g in groups[1:]:
            if g[0] - cluster[-1][1] <= 6:
                cluster.append(g)
            else:
                break
        if len(cluster) != len(literal):
            print(f"  skip y={y} '{literal}': {len(cluster)} groups {cluster}")
            return
        for (gx0, gx1), ch in zip(cluster, literal):
            w = gx1 - gx0 + 1
            if ch in digits or w > MAX_GLYPH_W:
                continue
            digits.setdefault(ch, []).append(mask[y:y + ROW_H, gx0:gx1 + 1])
            print(f"  harvested '{ch}' y={y} x={gx0}-{gx1} w={w}")

    for y, off, literal in DIGIT_SOURCES:
        if off is not None:
            harvest(y, L + off, literal)
        else:
            g = segment(mask, y, L + SKILL_INDENT, 1915, gap=6)
            if len(g) >= 2:
                harvest(y, g[-1][0], literal)

    missing = [c for c in "0123456789." if c not in digits]
    if missing:
        print("MISSING GLYPHS:", missing)

    skills = {}
    for y, name in SKILL_ROWS.items():
        g = segment(mask, y, L + SKILL_INDENT, 1915, gap=6)
        if not g:
            continue
        # profile the FULL path span (indent -> detached colon), matching
        # panel_ocr.skill_row
        colon_x0 = None
        for gx0, gx1 in g[:-1]:
            if gx1 - gx0 + 1 <= 4:
                colon_x0 = gx0
        px0 = L + SKILL_INDENT
        px1 = (colon_x0 - 2) if colon_x0 else (g[-1][0] - 6)
        prof = mask[y:y + ROW_H, px0:px1].sum(axis=0).astype(float)
        idx = np.linspace(0, len(prof) - 1, 64)
        skills.setdefault(name, []).append(list(np.interp(idx, np.arange(len(prof)), prof)))
        print(f"  skill sig '{name}' x={px0}-{px1} ({px1-px0+1}px)")

    model = {"digits": {k: [b.astype(int).tolist() for b in v]
                        for k, v in digits.items()},
             "skills": skills}
    if args.append_to:
        prev = json.load(open(args.append_to))
        for k, v in prev["digits"].items():
            model["digits"].setdefault(k, [])
            model["digits"][k] = v + model["digits"][k]
        for k, v in prev.get("skills", {}).items():
            model["skills"].setdefault(k, [])
            model["skills"][k] = v + model["skills"][k]
    json.dump(model, open(args.out, "w"))
    print(f"wrote {args.out}: {len(digits)} glyphs, {len(skills)} skill sigs")


if __name__ == "__main__":
    main()
