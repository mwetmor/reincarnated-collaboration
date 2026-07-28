#!/usr/bin/env python3
"""G-6 helper: read-magnification grid over a composite (or raw frame).

Emits fixed-size native tiles upscaled so that the delivered pixel ratio stays
at or above ~1x native, which is the empirically established floor for reading
the mastery panel's "N / M" counters.
"""
import argparse
from pathlib import Path

from PIL import Image

BASE = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
            "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
PANEL_ORIGIN = (448, 240)   # composites are cropped from here


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--composite", help="composite png under captures/.../composites")
    ap.add_argument("--frame", type=int, help="raw frame id instead")
    ap.add_argument("--region", required=True, help="x0,y0,x1,y1 in NATIVE screen coords")
    ap.add_argument("--tw", type=int, default=280)
    ap.add_argument("--th", type=int, default=200)
    ap.add_argument("--scale", type=int, default=4)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    outdir = BASE / "grid"
    outdir.mkdir(parents=True, exist_ok=True)
    if a.frame:
        im = Image.open(SRC / f"Screenshot ({a.frame}).png").convert("RGB")
        ox, oy = 0, 0
    else:
        im = Image.open(BASE / "composites" / a.composite).convert("RGB")
        ox, oy = PANEL_ORIGIN
    x0, y0, x1, y1 = (int(v) for v in a.region.split(","))
    n = 0
    for y in range(y0, y1, a.th):
        for x in range(x0, x1, a.tw):
            box = (x - ox, y - oy, min(x + a.tw, x1) - ox, min(y + a.th, y1) - oy)
            t = im.crop(box)
            t = t.resize((t.width * a.scale, t.height * a.scale), Image.LANCZOS)
            t.save(outdir / f"{a.tag}_{x}-{y}_x{a.scale}.png")
            n += 1
    print(f"{n} tiles -> {outdir}/{a.tag}_*")


if __name__ == "__main__":
    main()
