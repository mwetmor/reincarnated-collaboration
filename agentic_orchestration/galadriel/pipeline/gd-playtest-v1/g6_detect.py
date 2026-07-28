#!/usr/bin/env python3
"""
G-6 pass 2: precise UI-window detection by fixed-region template correlation.

Established by inspection of frame 352 (native 1920x1080):
  * the SKILL window ("Berserker | Devotion | Select Class" tab bar) renders at
    a FIXED screen position -- the window is centred, not anchored to content.
  * the CHARACTER window (paperdoll + stat panel, frames 121/300) likewise.

So a single native-resolution reference strip per window type, correlated
against the same strip in every frame, separates the classes with no OCR.

Correlation is normalised cross-correlation (zero-mean, unit-norm) on the
grayscale strip -- brightness-invariant, which matters because the game world
behind a translucent panel edge changes.

Outputs: g6-window-detect.csv  (per frame, per template score)
"""
import csv
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")

# native pixel boxes (x0,y0,x1,y1)
TEMPLATES = {
    # skill window tab bar: "Berserker  Devotion  Select Class" + ornate frame
    "skilltab": (520, 236, 1180, 262),
    # skill window mastery-level track at the panel foot (1 5 10 15 20 25 32 40 50)
    "masterybar": (520, 830, 1180, 862),
    # character window: paperdoll frame left column of equip slots
    "charpaper": (700, 260, 900, 300),
}
REF_FRAME = {"skilltab": 352, "masterybar": 352, "charpaper": 300}


def gray(fid, box):
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        c = im.convert("L").crop(box)
    return np.asarray(c, dtype=np.float32)


def ncc(a, b):
    a = a - a.mean()
    b = b - b.mean()
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-6 or nb < 1e-6:
        return 0.0
    return float((a * b).sum() / (na * nb))


def main():
    ids = sorted(int(f.name[12:-5]) for f in SRC.iterdir()
                 if f.name.startswith("Screenshot (") and f.name.endswith(").png"))
    refs = {k: gray(REF_FRAME[k], box) for k, box in TEMPLATES.items()}
    rows = []
    for i in ids:
        row = {"id": i}
        for k, box in TEMPLATES.items():
            row[k] = round(ncc(refs[k], gray(i, box)), 4)
        rows.append(row)
        if i % 40 == 0:
            print(f"  ..{i}", flush=True)
    with open(OUT / "g6-window-detect.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id"] + list(TEMPLATES))
        w.writeheader()
        w.writerows(rows)

    def runs(pred):
        hits = [r["id"] for r in rows if pred(r)]
        out, start, prev = [], None, None
        for i in hits:
            if start is None:
                start = prev = i
            elif i == prev + 1:
                prev = i
            else:
                out.append((start, prev))
                start = prev = i
        if start is not None:
            out.append((start, prev))
        return hits, out

    for k in TEMPLATES:
        hits, rr = runs(lambda r, k=k: r[k] > 0.80)
        print(f"\n{k}: {len(hits)} frames > 0.80")
        print("  runs:", ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in rr))


if __name__ == "__main__":
    main()
