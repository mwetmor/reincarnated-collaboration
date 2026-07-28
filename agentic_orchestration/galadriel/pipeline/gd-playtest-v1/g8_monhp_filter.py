#!/usr/bin/env python3
"""
KIT-CAL-1 G-8: post-filter the g8_monhp candidate bands down to the ones that
are actually a monster's "(cur/max)" health readout.

The detector's job was recall; most of what it returns is character-window
tooltip text ("18-24 Physical Damage", "1.78 Attacks per Second"). The
discriminator is the PARENTHESES: the health string opens on '(' and closes on
')', and both are narrow (<=5 px) and FULL-HEIGHT, whereas tooltip lines open
on a digit or a capital (7-9 px) and close on a lowercase letter that does not
reach the cap line.

This is a shape test on the mask, not a glyph match -- deliberately. Adding '('
and ')' to the glyph model would let the greedy matcher run the whole string,
and the string still contains the unmodelled thousands comma (see g8_monhp's
header). Shape-filter, then read with the eye.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-kitcal1-g8")
SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
BRIGHT_MIN, CHROMA_MAX = 150, 50


def groups_of(colprof):
    out, run = [], None
    for i, v in enumerate(colprof):
        if v > 0:
            run = [i, i] if run is None else [run[0], i]
        elif run is not None:
            out.append(tuple(run))
            run = None
    if run:
        out.append(tuple(run))
    return out


def main():
    cands = json.load(open(OUT / "g8-monhp-candidates.json"))
    keep = {}
    dst = OUT / "monhp-confirmed"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir()
    for fid, bands in sorted(cands.items(), key=lambda kv: int(kv[0])):
        with Image.open(SRC / f"Screenshot ({fid}).png") as im:
            im = im.convert("RGB")
            a = np.asarray(im).astype(np.int16)
        for k, b in enumerate(bands):
            sub = a[b["y0"]:b["y1"] + 1, b["x0"]:b["x1"] + 1]
            mx, mn = sub.max(axis=2), sub.min(axis=2)
            m = (mn > BRIGHT_MIN) & ((mx - mn) < CHROMA_MAX)
            H = m.shape[0]
            gs = groups_of(m.sum(axis=0))
            if len(gs) < 6:
                continue
            (l0, l1), (r0, r1) = gs[0], gs[-1]
            lw, rw = l1 - l0 + 1, r1 - r0 + 1
            # parens: narrow AND spanning nearly the full cap height
            lh = np.nonzero(m[:, l0:l1 + 1].sum(axis=1))[0]
            rh = np.nonzero(m[:, r0:r1 + 1].sum(axis=1))[0]
            if not (len(lh) and len(rh)):
                continue
            lspan = lh.max() - lh.min() + 1
            rspan = rh.max() - rh.min() + 1
            if lw <= 5 and rw <= 5 and lspan >= H - 2 and rspan >= H - 2:
                keep.setdefault(fid, []).append(b)
                c = im.crop((b["x0"] - 8, b["y0"] - 5, b["x1"] + 8, b["y1"] + 5))
                c.resize((c.width * 6, c.height * 6), Image.LANCZOS).save(
                    dst / f"f{int(fid):04d}-{k}.png")
    with open(OUT / "g8-monhp-confirmed.json", "w") as f:
        json.dump(keep, f, indent=1)
    n = sum(len(v) for v in keep.values())
    print(f"{n} paren-shaped bands over {len(keep)} frames "
          f"(from {sum(len(v) for v in cands.values())} candidates / {len(cands)} frames)")
    for fid in sorted(keep, key=int):
        print(f"  f{fid}: {len(keep[fid])}")


if __name__ == "__main__":
    main()
