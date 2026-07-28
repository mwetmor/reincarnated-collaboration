#!/usr/bin/env python3
"""
G-6 pass 8: per-burst MEDIAN COMPOSITE of the mastery panel.

The problem: in every single still the hovered-skill tooltip covers part of the
skill tree, and the tooltip moves with the cursor, so no one frame shows the
whole allocation.

The fix, exploiting how Matt shot the footage: each burst contains 5-6 frames
in which he hovered a DIFFERENT node, so the tooltip sits somewhere different
in each. A per-pixel median across a burst therefore returns the tree
everywhere the tooltip covers a minority of frames -- which is everywhere,
since no two frames in a burst share a tooltip position.

NO SILENT TRANSFORMATION: the composite is a derived artifact, written under an
explicit `-composite` name, and every counter read off it is re-verified
against at least one raw single frame before it is graded. The composite is a
finding aid, not evidence of record.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6/composites")
PANEL = (448, 240, 1530, 885)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tile", type=int, default=362)
    ap.add_argument("--scale", type=int, default=3)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    fids = [int(v) for v in a.frames.split(",")]
    stack = []
    for f in fids:
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            stack.append(np.asarray(im.convert("RGB").crop(PANEL), dtype=np.uint8))
    med = np.median(np.stack(stack), axis=0).astype(np.uint8)
    comp = Image.fromarray(med)
    comp.save(OUT / f"{a.tag}-composite_native.png")
    W, H = comp.size
    n = 0
    for y in range(0, H, 215):
        for x in range(0, W, a.tile):
            t = comp.crop((x, y, min(x + a.tile, W), min(y + 215, H)))
            t = t.resize((t.width * a.scale, t.height * a.scale), Image.LANCZOS)
            t.save(OUT / f"{a.tag}-tile_{PANEL[0]+x}-{PANEL[1]+y}_x{a.scale}.png")
            n += 1
    print(f"{a.tag}: composite {W}x{H} from {fids}; {n} tiles")


if __name__ == "__main__":
    main()
