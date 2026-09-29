#!/usr/bin/env python3
"""C-9 T9-1b: pick a variant per canvas, by measurement.

    python3 tools/choose_albedo.py                 # measure and print
    python3 tools/choose_albedo.py --apply         # also copy the winners into t9_1b/painted/

WHAT "DE-LIT" MEANS AS A NUMBER. The painted key is a LOW-SPATIAL-FREQUENCY modulation of
luma, aligned with the sun. The texture the brief asked to keep is HIGH frequency. So the
two halves of the job separate cleanly on a blur, and a variant can be scored on both at
once instead of being admired:

  * low_sd    std of luma blurred at sigma 40, over painted pixels. THIS IS THE KEY.
              Lower is the de-lighting; it is the number the step exists to move.
  * dir_grad  the mean gradient of that blurred field projected onto the sun's own screen
              direction, which build_lights derives and the scene reports as key_dir_world
              = (0.761, -0.341, -0.552) -> (+0.923, +0.349) in canvas axes. A directional
              key shows up here even when its magnitude is modest; flat light cannot.
  * high_sd   std of (luma - blur), over painted pixels. THE DETAIL. It must NOT collapse:
              a variant that wins on low_sd by smearing the picture has not de-lit it, it
              has erased it, and low_sd alone cannot tell those apart.
  * blocks_0  share of 128x128 blocks that phase-correlate to EXACTLY (0,0) against the
              original, plus the worst block offset. Every edge was to stay where it is,
              and this measures WHERE they are.

              It replaces a correlation of gradient MAGNITUDE, which was the first thing
              tried and which is not a fitness function -- it is the opposite of one.
              Removing a cast shadow removes a strong gradient, so the better a variant
              de-lights, the lower it scores; the first run of this chooser used it as a
              tie-break and it picked the less de-lit variant on two canvases out of three,
              for a reason that read like a defect ("the flatter variant moved edges") and
              was in fact the job being done. Correlating magnitudes cannot separate an
              edge that MOVED from an edge that was SUPPOSED to go. Block registration can:
              it is blind to tone by construction -- the same gradient phase correlation
              the reassembler uses, which --self-test shows locking at 700-960 sigma
              through a de-light hard enough to take near-black to zero.

And four faults that disqualify rather than score: paint pushed into the keying green,
paint retreating out of the green, pixels come back flat green, and areas blown to white.

Registration is reported for every variant from the same phase correlation the reassembler
uses, so the chunk that is chosen is the chunk whose offset is known before it is chosen.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import shutil

import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
HERE = pathlib.Path(__file__).resolve().parent.parent
ART = HERE.parent / "artifacts"
GREEN = np.array([0, 255, 0], np.int16)

# tile id -> burst id
BURSTS = {"top": "T9A-top", "bot_left": "T9A-bl", "bot_right": "T9A-br"}
# the key's travel direction in CANVAS axes, from the scene's own key_dir_world
KEY_DIR = np.array([0.92258, 0.34948])
KEY_DIR = KEY_DIR / np.linalg.norm(KEY_DIR)

_spec = importlib.util.spec_from_file_location("ra", HERE / "tools" / "reassemble_albedo.py")
ra = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ra)


def luma(a: np.ndarray) -> np.ndarray:
    return (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).astype(np.float32)


def score(ref: np.ndarray, got: np.ndarray, alpha: np.ndarray) -> dict:
    painted = alpha > 0
    clear = ~painted
    lr, lg = luma(ref), luma(got)
    br, bg = ndimage.gaussian_filter(lr, 40), ndimage.gaussian_filter(lg, 40)

    def dirgrad(b):
        gy, gx = np.gradient(b)
        return float(np.abs((gx * KEY_DIR[0] + gy * KEY_DIR[1])[painted].mean()) * 100)

    # WHERE the edges are, block by block. Blind to tone by construction.
    B = 128
    offs, skipped = [], 0
    for by in range(0, ref.shape[0] - B + 1, B):
        for bx in range(0, ref.shape[1] - B + 1, B):
            m = painted[by:by + B, bx:bx + B]
            if m.mean() < 0.5:
                skipped += 1
                continue
            a0 = ref[by:by + B, bx:bx + B].astype(np.float32)
            b0 = got[by:by + B, bx:bx + B].astype(np.float32)
            if luma(a0)[m].std() < 6.0:      # featureless: nothing for a lock to hold
                skipped += 1
                continue
            d = ra.register(a0, b0, m, limit=16)
            offs.append((d[0], d[1]))
    n = max(len(offs), 1)
    zero = sum(1 for o in offs if o == (0, 0))
    within1 = sum(1 for o in offs if abs(o[0]) <= 1 and abs(o[1]) <= 1)
    worst = max((max(abs(o[0]), abs(o[1])) for o in offs), default=0)

    is_green = np.abs(got.astype(np.int16) - GREEN).max(-1) < 24
    dy, dx, snr = ra.register(ref.astype(np.float32), got.astype(np.float32), painted)
    return {
        "offset_dy_dx": [int(dy), int(dx)], "peak_sigma": round(snr, 0),
        "mean_luma": round(float(lg[painted].mean()), 1),
        "near_black_pct": round(float((lg[painted] <= 32).mean() * 100), 2),
        "low_sd": round(float(bg[painted].std()), 2),
        "dir_grad": round(dirgrad(bg), 2),
        "high_sd": round(float((lg - bg)[painted].std()), 2),
        "blocks": len(offs), "blocks_skipped": skipped,
        "blocks_zero_pct": round(100.0 * zero / n, 1),
        "blocks_within1_pct": round(100.0 * within1 / n, 1),
        "worst_block_offset_px": int(worst),
        "paint_into_green_px": int((clear & ~is_green).sum()),
        "paint_left_green_px": int((painted & is_green).sum()),
        "blown_white_pct": round(float((lg[painted] >= 245).mean() * 100), 2),
        "_ref": {"mean_luma": round(float(lr[painted].mean()), 1),
                 "near_black_pct": round(float((lr[painted] <= 32).mean() * 100), 2),
                 "low_sd": round(float(br[painted].std()), 2),
                 "dir_grad": round(dirgrad(br), 2),
                 "high_sd": round(float((lr - br)[painted].std()), 2)},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    grid = json.loads((HERE / "t9_1b" / "t9_albedo_grid.json").read_text())
    plate = np.asarray(Image.open(HERE / grid["plate"]["file"]))
    out, picks = {}, {}

    for tid, t in grid["tiles"].items():
        x0, y0, x1, y1 = t["plate_rect"]
        ref = plate[y0:y1, x0:x1, :3]
        alpha = plate[y0:y1, x0:x1, 3]
        rows = {}
        for v in ("a", "b"):
            p = ART / BURSTS[tid] / ("%s_%s.png" % (BURSTS[tid], v))
            if not p.exists():
                continue
            im = Image.open(p).convert("RGB")
            if im.size != (x1 - x0, y1 - y0):
                rows[v] = {"SIZE": list(im.size), "expected": [x1 - x0, y1 - y0]}
                continue
            rows[v] = score(ref, np.asarray(im), alpha)
            rows[v]["file"] = str(p)
        out[tid] = rows

        ok = {v: r for v, r in rows.items() if "low_sd" in r}
        # THE RULE, written before the numbers were read: take the lower low_sd, unless it
        # got there by erasing the picture (high_sd down more than 15% against the other
        # variant) or by moving it (edge_r lower by more than 0.03).
        if len(ok) == 2:
            av, bv = ok["a"], ok["b"]
            lo, hi = ("a", "b") if av["low_sd"] <= bv["low_sd"] else ("b", "a")
            why = "lower low_sd (%.2f vs %.2f)" % (ok[lo]["low_sd"], ok[hi]["low_sd"])
            if ok[lo]["high_sd"] < ok[hi]["high_sd"] * 0.85:
                lo, hi = hi, lo
                why = "the flatter variant lost detail (high_sd %.2f vs %.2f)" % (
                    ok[hi]["high_sd"], ok[lo]["high_sd"])
            elif ok[lo]["blocks_within1_pct"] < ok[hi]["blocks_within1_pct"] - 5.0:
                lo, hi = hi, lo
                why = "the flatter variant moved the picture (blocks within 1 px %.1f%% vs %.1f%%)" % (
                    ok[hi]["blocks_within1_pct"], ok[lo]["blocks_within1_pct"])
            picks[tid] = {"variant": lo, "why": why}
        elif ok:
            picks[tid] = {"variant": next(iter(ok)), "why": "only usable variant"}

        r0 = next(iter(ok.values()))["_ref"] if ok else {}
        print("\n%-9s  plate %s\n   ORIGINAL: low_sd %.2f  dir_grad %.2f  high_sd %.2f  "
              "near-black %.2f%%  luma %.1f" % (tid, t["plate_rect"], r0.get("low_sd", -1),
              r0.get("dir_grad", -1), r0.get("high_sd", -1), r0.get("near_black_pct", -1),
              r0.get("mean_luma", -1)))
        for v, r in rows.items():
            if "low_sd" not in r:
                print("   %s  WRONG SIZE %s (expected %s)" % (v, r["SIZE"], r["expected"]))
                continue
            print("   %s  low_sd %6.2f  dir_grad %5.2f  high_sd %5.2f  near-black %5.2f%%  "
                  "luma %5.1f  off %s %.0fsig | blocks %d: %.1f%% exact, %.1f%% <=1px, worst %d"
                  "  | into-green %d  left-green %d  blown %.2f%%"
                  % (v, r["low_sd"], r["dir_grad"], r["high_sd"], r["near_black_pct"],
                     r["mean_luma"], r["offset_dy_dx"], r["peak_sigma"], r["blocks"],
                     r["blocks_zero_pct"], r["blocks_within1_pct"], r["worst_block_offset_px"],
                     r["paint_into_green_px"], r["paint_left_green_px"], r["blown_white_pct"]))
        if tid in picks:
            print("   -> %s: %s" % (picks[tid]["variant"], picks[tid]["why"]))

    dest = HERE / "t9_1b" / "painted"
    if a.apply:
        dest.mkdir(parents=True, exist_ok=True)
        for tid, p in picks.items():
            src = pathlib.Path(out[tid][p["variant"]]["file"])
            shutil.copy2(src, dest / ("t9_albedo_%s.png" % tid))
            print("copied %s -> %s" % (src.name, dest / ("t9_albedo_%s.png" % tid)))
    (HERE / "t9_1b" / "choose_albedo.json").write_text(
        json.dumps({"scores": out, "picks": picks}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
