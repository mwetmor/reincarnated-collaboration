#!/usr/bin/env python3
"""G-6 crop utility: extract NATIVE-RES regions from a still, optionally
upscaled for human/multimodal reading.

Discipline (no silent transformation): every crop is written with its source
frame id and native pixel box encoded in the filename, and the RAW native crop
is always written alongside any upscaled version.

usage: g6_crop.py <frame_id> <x0> <y0> <x1> <y1> [scale] [tag]
"""
import sys
from pathlib import Path
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6/crops")


def crop(fid, box, scale=1, tag=""):
    OUT.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = box
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        c = im.convert("RGB").crop((x0, y0, x1, y1))
    stem = f"f{fid}_{x0}-{y0}-{x1}-{y1}" + (f"_{tag}" if tag else "")
    raw = OUT / f"{stem}_native.png"
    c.save(raw)
    paths = [raw]
    if scale != 1:
        up = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
        p = OUT / f"{stem}_x{scale}.png"
        up.save(p)
        paths.append(p)
    return paths


if __name__ == "__main__":
    fid = int(sys.argv[1])
    box = tuple(int(v) for v in sys.argv[2:6])
    scale = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    tag = sys.argv[7] if len(sys.argv) > 7 else ""
    for p in crop(fid, box, scale, tag):
        print(p)
