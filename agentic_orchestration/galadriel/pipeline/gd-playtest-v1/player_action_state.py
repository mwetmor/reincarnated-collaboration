#!/usr/bin/env python3
"""
P0 instrument: track the PLAYER's per-frame Action State from the green
`character.LogData` overlay, at native 60 fps.

Why this exists
---------------
gandalf's verification note (2026-07-26) §6b asks whether the PlayStats
`skill_use_count` field counts SWINGS or ACTIVATIONS. The decisive comparison
is "actual swings in a bounded window" vs "panel delta over the same window".

The green overlay renders, per entity, two lines:

    <ControllerState>
    [<entityId>] Action State: <ActionState>

The PLAYER is entity 42992 in this run (identified visually: werewolf-transform
sprite, camera-centred, controller states MoveTo / UseSkill / MoveToUseSkill).
Tracking that one line gives a per-frame, game-authored record of what the
player was doing -- an instrument from the game rather than from inference.

Method
------
1. Binary-mask the green overlay text (high G, low R/B).
2. Locate the fixed glyph block "42992" by normalised binary template
   correlation (scipy fftconvolve).
3. The overlay text is a fixed-format string, so the Action-State VALUE word
   sits at a constant pixel offset to the right of the id block. Crop it.
4. Classify the value word against exemplars harvested from the run itself
   (no external font assumptions).

Method law (protocol §4.4): crops are taken at native resolution. Nothing is
downscaled before reading. Upscaling happens only for human inspection.
"""

import argparse
import glob
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy.signal import fftconvolve

# --- green overlay mask ---------------------------------------------------
G_MIN = 140
RB_MAX = 120
G_MINUS_R = 50

# Offsets of the Action-State VALUE word relative to the left edge of the
# "42992" id-glyph block, measured on frame c_00451 of the t=4012 window.
VALUE_DX0 = 150
VALUE_DX1 = 220
VALUE_DY0 = -1
VALUE_DY1 = 15


def green_mask(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    return (
        (a[:, :, 1] > G_MIN)
        & (a[:, :, 0] < RB_MAX)
        & (a[:, :, 2] < RB_MAX)
        & ((a[:, :, 1] - a[:, :, 0]) > G_MINUS_R)
    )


def match_template(mask, tmpl, mismatch_penalty=0.6):
    """Normalised binary correlation. Returns (best_score, y, x)."""
    m = mask.astype(np.float32)
    t = tmpl.astype(np.float32)
    ones = np.ones_like(t)
    corr = fftconvolve(m, t[::-1, ::-1], mode="valid")
    cnt = fftconvolve(m, ones[::-1, ::-1], mode="valid")
    score = (corr - mismatch_penalty * (cnt - corr)) / max(t.sum(), 1.0)
    idx = int(np.argmax(score))
    y, x = np.unravel_index(idx, score.shape)
    return float(score[y, x]), int(y), int(x)


def value_signature(mask, y, x):
    """Column ink-profile of the Action-State value word. Rendering is
    deterministic, so identical words give identical signatures."""
    y0 = max(y + VALUE_DY0, 0)
    y1 = min(y + VALUE_DY1, mask.shape[0])
    x0 = max(x + VALUE_DX0, 0)
    x1 = min(x + VALUE_DX1, mask.shape[1])
    sub = mask[y0:y1, x0:x1]
    if sub.size == 0:
        return None, None
    prof = sub.sum(axis=0)
    nz = np.nonzero(prof)[0]
    if len(nz) == 0:
        return None, sub
    # trim to the ink extent so the signature is translation-invariant
    trimmed = prof[nz.min(): nz.max() + 1]
    return trimmed, sub


def sig_key(prof, nbins=24):
    """Fixed-length quantised signature for nearest-neighbour word matching."""
    if prof is None or len(prof) == 0:
        return None
    idx = np.linspace(0, len(prof) - 1, nbins)
    return np.interp(idx, np.arange(len(prof)), prof.astype(float)), len(prof)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True, help="glob for player-crop PNGs")
    ap.add_argument("--template", required=True, help="npy binary template of the id glyph block")
    ap.add_argument("--t0", type=float, required=True, help="video offset (s) of first frame")
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--min-score", type=float, default=0.55)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dump-values", default=None,
                    help="dir to dump value-word crops for exemplar labelling")
    args = ap.parse_args()

    tmpl = np.load(args.template)
    files = sorted(glob.glob(args.frames))
    if not files:
        sys.exit("no frames matched")

    if args.dump_values:
        os.makedirs(args.dump_values, exist_ok=True)

    rows = []
    for i, p in enumerate(files):
        mask = green_mask(p)
        score, y, x = match_template(mask, tmpl)
        rec = {
            "i": i,
            "t": round(args.t0 + i / args.fps, 4),
            "score": round(score, 4),
            "found": bool(score >= args.min_score),
            "y": y,
            "x": x,
        }
        if rec["found"]:
            prof, sub = value_signature(mask, y, x)
            k = sig_key(prof)
            if k is not None:
                rec["sig"] = [round(v, 2) for v in k[0]]
                rec["width"] = int(k[1])
                rec["ink"] = int(prof.sum())
            if args.dump_values and i % 10 == 0 and sub is not None and sub.size:
                Image.fromarray((sub * 255).astype(np.uint8)).resize(
                    (sub.shape[1] * 4, sub.shape[0] * 4), Image.NEAREST
                ).save(os.path.join(args.dump_values, f"v_{i:05d}.png"))
        rows.append(rec)
        if i % 200 == 0:
            print(f"  {i}/{len(files)} score={score:.2f}", file=sys.stderr)

    with open(args.out, "w") as f:
        json.dump(rows, f)
    found = sum(r["found"] for r in rows)
    print(f"wrote {args.out}: {len(rows)} frames, id located in {found} "
          f"({100.0*found/len(rows):.1f}%)")


if __name__ == "__main__":
    main()
