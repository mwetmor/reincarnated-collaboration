#!/usr/bin/env python3
"""
kc2_clk2_geography.py — SB-1 Cell CLK-2. TURNS A DIGEST INTO A GEOGRAPHY.

    python3 kc2_clk2_geography.py A.png B.png --label p1-vs-p2 --out DIR [--amplify 12]

WHY THIS EXISTS. A red FG-10 leg hands you two 64-hex digests and the sentence
"these frames are not the same frame". That sentence cannot tell apart

    one pixel of dither in the smoke bed      (cosmetic, ±1, confined)
    the FX ring firing a frame early          (structural, large, localised)
    the whole trajectory having diverged      (everything, everywhere)

and those three want three different fixes. So this reports, for a frame pair:

  n_differing_pixels / pct_of_frame   how much moved
  bbox                                where it moved, tightest rectangle
  max_abs_delta + the ±1 share        whether it is dither or drawing
  a 4x4 region grid                   which part of the picture, so a layer
                                      (FX ring / glow / smoke bed / ground /
                                      subject) can be named rather than guessed
  an amplified difference PNG         the eyeball's copy, x{amplify}

⚑ THE ±1 SHARE IS THE DISCRIMINATOR, NOT THE PIXEL COUNT. A frame can differ in
  two million pixels and still be the same picture if every one of those pixels
  is off by a single channel step: that is a GPU rounding a blend differently,
  not a scene rendering differently. CLK-1 used exactly this split. A pixel
  count alone cannot tell the two verdicts apart, and NOTE-72 says a probe that
  cannot tell two verdicts apart is not a probe.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def load(p: Path) -> np.ndarray:
    im = Image.open(p).convert("RGB")
    return np.asarray(im).astype(np.int16)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a", type=Path)
    ap.add_argument("b", type=Path)
    ap.add_argument("--label", default="pair")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--amplify", type=int, default=12)
    ap.add_argument("--grid", type=int, default=4)
    args = ap.parse_args()

    A, B = load(args.a), load(args.b)
    if A.shape != B.shape:
        print(f"  {args.label}: SHAPE MISMATCH {A.shape} vs {B.shape}")
        return 2

    H, W, _ = A.shape
    d = np.abs(A - B)
    dmax = d.max(axis=2)              # per-pixel worst channel
    mask = dmax > 0
    n = int(mask.sum())
    total = H * W

    rep = {
        "label": args.label,
        "a": str(args.a), "b": str(args.b),
        "frame_wh": [W, H],
        "n_differing_pixels": n,
        "pct_of_frame": round(100.0 * n / total, 6),
        "max_abs_delta": int(dmax.max()),
        "mean_abs_delta_over_differing": (
            round(float(dmax[mask].mean()), 4) if n else 0.0),
    }

    if n:
        ys, xs = np.nonzero(mask)
        rep["bbox_xyxy"] = [int(xs.min()), int(ys.min()),
                            int(xs.max()), int(ys.max())]
        rep["bbox_wh"] = [int(xs.max() - xs.min() + 1),
                          int(ys.max() - ys.min() + 1)]
        vals = dmax[mask]
        rep["delta_histogram"] = {
            "eq1": int((vals == 1).sum()),
            "eq2": int((vals == 2).sum()),
            "in_3_8": int(((vals >= 3) & (vals <= 8)).sum()),
            "gt8": int((vals > 8).sum()),
        }
        rep["pct_of_differing_that_are_pm1"] = round(
            100.0 * rep["delta_histogram"]["eq1"] / n, 3)
        g = args.grid
        cells = []
        for gy in range(g):
            row = []
            for gx in range(g):
                sub = mask[gy * H // g:(gy + 1) * H // g,
                           gx * W // g:(gx + 1) * W // g]
                row.append(int(sub.sum()))
            cells.append(row)
        rep["region_grid_counts"] = cells
        rep["region_grid_pct_of_diff"] = [
            [round(100.0 * c / n, 2) for c in row] for row in cells]

        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            amp = np.clip(d * args.amplify, 0, 255).astype(np.uint8)
            Image.fromarray(amp).save(
                args.out / f"diff-{args.label}-amplified-x{args.amplify}.png")

    print(json.dumps(rep, indent=2))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / f"geography-{args.label}.json").write_text(
            json.dumps(rep, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
