#!/usr/bin/env python3
# ============================================================================
# xrow_component_curve.py — galadriel, 2026-08-25.
#
# PURPOSE: rule on whether `significant_components` is fit for a shape-distance
# operator. This script DOES NOT SCORE Q1-Q5 and does not touch the cross-row
# leg at all. It re-derives ONE descriptor (and its continuous neighbours) on
# the SAME masks drax's `s2b_xrow_rows37.py` built, across the SAME floor
# ladder, so the integer's stability can be READ rather than argued.
#
# Operator, stated so no number below travels without its frame (#64):
#   mask   = (fx - MATCHED novfx ctl), per-pixel max-channel |d| >= FLOOR
#   frames = 1920x1080, ratified combat camera FOV 40 / pitch -55 / yaw 47 / dist 34
#   label  = scipy.ndimage.label, DEFAULT 4-CONNECTIVITY (verbatim from drax)
#   sig    = count of components whose size >= 0.01 * total authored px (verbatim)
#
# ANTI-TUNING: no effect is changed by anything here. No replacement descriptor
# is scored against the corpus. Candidates are REPORTED as candidates only.
# ============================================================================
import os, sys, json, math
import numpy as np
from PIL import Image
from scipy import ndimage

CAP = os.path.expanduser("~/Games/reincarnated-godot/harness_logs/s2b_rows37_2026-08-24")
FLOORS = [1, 2, 3, 4, 6, 8, 10, 12, 16, 24, 32, 48]
LADDER = [2, 4, 6, 8, 10, 12, 16, 24]


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int16)


def delta(fx, ctl):
    return np.abs(load(fx) - load(ctl)).max(axis=2)


def comps(mask):
    """drax's descriptor, verbatim, plus the continuous neighbours it hides."""
    n = int(mask.sum())
    if n < 40:
        return None
    lbl, ncomp = ndimage.label(mask)
    sizes = np.bincount(lbl.ravel())[1:] if ncomp else np.array([0])
    sizes = np.sort(sizes)[::-1]
    frac = sizes / n
    sig = int((sizes >= 0.01 * n).sum())
    # continuous candidates (REPORTED, NOT SCORED)
    p = frac[frac > 0]
    H = float(-(p * np.log(p)).sum())          # component-size entropy (nats)
    eff = float(math.exp(H))                   # perplexity == "effective count"
    inv_hhi = float(1.0 / (frac ** 2).sum())   # inverse Herfindahl
    return {
        "authored_px": n,
        "raw_components": int(ncomp),
        "significant_components": sig,
        "largest_component_frac": float(frac[0]),
        "second_component_frac": float(frac[1]) if frac.size > 1 else 0.0,
        "px_outside_largest": int(n - sizes[0]),
        "effective_count_exp_entropy": eff,
        "effective_count_inv_hhi": inv_hhi,
        "top5_component_px": [int(x) for x in sizes[:5]],
        "one_pct_gate_px": 0.01 * n,
    }


ARMS = {}
for stage in ("cathedral", "arena"):
    for e in ("fire", "water", "earth", "wind"):
        ARMS["single_target/%s@%s" % (e, stage)] = (
            "st_%s_%s_03-flight-mid.png" % (stage, e),
            "st_%s_novfx_03-flight-mid.png" % stage)
        ARMS["line/%s@%s" % (e, stage)] = (
            "ln_%s_%s_05-full-line.png" % (stage, e),
            "ln_%s_novfx_05-full-line.png" % stage)
    ARMS["multi_projectile_count1@%s" % stage] = (
        "mp_%s_count1_04-impacts.png" % stage,
        "mp_%s_count1_novfx_04-impacts.png" % stage)

if __name__ == "__main__":
    out = {"operator": ("mask = (fx - MATCHED novfx ctl), max-channel |d| >= FLOOR; "
                        "1920x1080; ratified combat camera FOV 40 / pitch -55 / yaw 47 / "
                        "dist 34; scipy.ndimage.label 4-connectivity; significant = "
                        "component size >= 1 % of authored px"),
           "capture_dir": CAP, "curves": {}}
    for name, (fxn, ctln) in ARMS.items():
        fx, ctl = os.path.join(CAP, fxn), os.path.join(CAP, ctln)
        if not (os.path.exists(fx) and os.path.exists(ctl)):
            continue
        d = delta(fx, ctl)
        row = {}
        for f in FLOORS:
            r = comps(d >= f)
            row[str(f)] = r
        out["curves"][name] = {"fx": fxn, "ctl": ctln, "by_floor": row}
        line = " ".join("%d:%s" % (f, (row[str(f)]["significant_components"] if row[str(f)] else "-"))
                        for f in FLOORS)
        print("%-34s sig_comp by floor  %s" % (name, line))
    with open(sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv
              else "/tmp/xrow_component_curve.json", "w") as fh:
        json.dump(out, fh, indent=2)
