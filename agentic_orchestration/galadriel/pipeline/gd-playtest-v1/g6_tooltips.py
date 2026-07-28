#!/usr/bin/env python3
"""
G-6 pass 3: harvest the skill-window TOOLTIP from every skill-window frame.

The GD mastery window renders the hovered skill's tooltip at a FIXED position
over the mastery art (native box below, measured on frame 352). The tooltip
carries the highest-confidence rank evidence available in this footage:
the skill's display NAME plus an explicit "Current Level : N" line.

Frames within a burst are near-duplicates (Matt pressed PrtSc repeatedly on the
same hover), so tooltips are deduped by normalised cross-correlation before any
reading. Raw native crops are kept for every frame regardless -- dedupe affects
only what is put in front of the eye, never what is preserved.
"""
import csv
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
TIP = OUT / "tooltips"

TOOLTIP_BOX = (640, 330, 1000, 760)   # native, measured on f352
SKILL_FRAMES = None                    # loaded from detect csv


def load_skill_frames(thresh=0.80):
    ids = []
    with open(OUT / "g6-window-detect.csv") as f:
        for r in csv.DictReader(f):
            if float(r["masterybar"]) > thresh or float(r["skilltab"]) > thresh:
                ids.append(int(r["id"]))
    return sorted(ids)


def get(fid, box):
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        return im.convert("RGB").crop(box)


def ncc(a, b):
    a = np.asarray(a.convert("L"), dtype=np.float32).ravel()
    b = np.asarray(b.convert("L"), dtype=np.float32).ravel()
    a -= a.mean(); b -= b.mean()
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float((a * b).sum() / n) if n > 1e-6 else 0.0


def main():
    TIP.mkdir(parents=True, exist_ok=True)
    ids = load_skill_frames()
    print(f"skill-window frames ({len(ids)}): {ids}")
    tips = {}
    for i in ids:
        c = get(i, TOOLTIP_BOX)
        c.save(TIP / f"f{i}_tooltip_native.png")
        tips[i] = c
    # dedupe
    reps, groups = [], {}
    for i in ids:
        placed = False
        for r in reps:
            if ncc(tips[i], tips[r]) > 0.985:
                groups[r].append(i)
                placed = True
                break
        if not placed:
            reps.append(i)
            groups[i] = [i]
    print(f"\nunique tooltip states: {len(reps)}")
    for r in reps:
        print(f"  rep f{r}  <- {groups[r]}")
    for r in reps:
        c = tips[r]
        c.resize((c.width * 3, c.height * 3), Image.LANCZOS).save(
            TIP / f"REP_f{r}_x3.png")
    with open(OUT / "g6-tooltip-groups.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rep_frame", "member_frames"])
        for r in reps:
            w.writerow([r, " ".join(str(x) for x in groups[r])])


if __name__ == "__main__":
    main()
