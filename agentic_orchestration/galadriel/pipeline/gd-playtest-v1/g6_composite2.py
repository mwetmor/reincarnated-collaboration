#!/usr/bin/env python3
"""
G-6 pass 8b: TWO-PASS ROBUST COMPOSITE of the mastery panel.

Pass 8a (plain median) left tooltip residue: within a burst the tooltip does
move, but it clusters over the mastery portrait, so at some pixels it covers a
MAJORITY of frames and the median picks it.

Two-pass fix:
  pass 1  m0 = per-pixel median  (rough, tooltip-contaminated)
  pass 2  for each frame, mark pixels far from m0 as OUTLIER (that is what a
          tooltip is: a big, opaque, frame-specific deviation), then average
          only the inlier frames per pixel. Where every frame is an outlier --
          i.e. the tooltip genuinely covers that pixel in all of them -- the
          pixel is stamped MAGENTA so it is impossible to mistake reconstructed
          tree for occluded tree.

The magenta "no-data" stamp is the point: it makes occlusion visible instead of
silently plausible. Nothing is inpainted, ever.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6/composites")
PANEL = (448, 240, 1530, 885)
NODATA = (255, 0, 255)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tol", type=float, default=26.0)
    ap.add_argument("--tile", type=int, default=362)
    ap.add_argument("--scale", type=int, default=3)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    fids = [int(v) for v in a.frames.split(",")]
    stack = []
    for f in fids:
        with Image.open(SRC / f"Screenshot ({f}).png") as im:
            stack.append(np.asarray(im.convert("RGB").crop(PANEL), dtype=np.float32))
    S = np.stack(stack)                      # (n,H,W,3)
    m0 = np.median(S, axis=0)
    dev = np.abs(S - m0).mean(axis=3)        # (n,H,W)
    inlier = dev <= a.tol
    cnt = inlier.sum(axis=0)
    w = inlier[..., None].astype(np.float32)
    acc = (S * w).sum(axis=0)
    out = np.where(cnt[..., None] > 0, acc / np.maximum(cnt[..., None], 1), 0.0)
    nod = cnt == 0
    out[nod] = NODATA
    frac = float(nod.mean())
    img = Image.fromarray(out.astype(np.uint8))
    img.save(OUT / f"{a.tag}2-composite_native.png")
    print(f"{a.tag}: {len(fids)} frames, no-data {frac*100:.2f}% of panel")
    W, H = img.size
    for y in range(0, H, 215):
        for x in range(0, W, a.tile):
            t = img.crop((x, y, min(x + a.tile, W), min(y + 215, H)))
            t = t.resize((t.width * a.scale, t.height * a.scale), Image.LANCZOS)
            t.save(OUT / f"{a.tag}2-tile_{PANEL[0]+x}-{PANEL[1]+y}_x{a.scale}.png")


if __name__ == "__main__":
    main()
