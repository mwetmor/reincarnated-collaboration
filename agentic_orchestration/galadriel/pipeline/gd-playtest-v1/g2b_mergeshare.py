#!/usr/bin/env python3
"""G-2b headline -- how much of the kills/engagement climb is MERGE?

The assumption-free bound. Re-segmentation at a tighter gap threshold g only
ever SPLITS a gap>5 s engagement; it never merges two. The sub-segmentation is
therefore strictly NESTED inside the 106 windows, which means the engagement
remains a valid bootstrap unit at every threshold, and the survival of the
regime ratio under tightening is a direct measurement of how much of the climb
lived in the segmentation grain.

    merge_share(g) = 1 - log R(g) / log R(5)

where R(g) = (kills/engagement in the higher regime) / (lower regime) after
re-segmenting at gap > g. If dash-chaining manufactured the climb, R(g) -> 1
as g shrinks toward the 0.5 s sampling floor and merge_share -> 1. If the
climb is a world-fact about how many enemies died per contact, R(g) is
threshold-stable and merge_share -> 0.

Usage: g2b_mergeshare.py <ta-gated.csv> <tb-windows.json> <out.json>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GRID = (5.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.0)
RNG = np.random.default_rng(20260728)
NBOOT = 20000

spec = importlib.util.spec_from_file_location(
    "tb_windows", os.path.join(HERE, "tb_windows.py"))
TBW = importlib.util.module_from_spec(spec)
spec.loader.exec_module(TBW)


def subcount(group, g):
    """How many sub-engagements this gap>5 window breaks into at gap > g."""
    n = 1
    for i in range(len(group) - 1):
        if group[i + 1]["pts_s"] - group[i]["pts_s"] > g:
            n += 1
    return n


def main():
    ledger, winpath, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = TBW.load(ledger)
    ev = TBW.kill_events(rows)
    groups = TBW.segment(ev, 5.0)
    win = json.load(open(winpath))["windows"]
    assert len(groups) == len(win) == 106, "GATE: 106-window reproduction"

    unit = []
    for g, w in zip(groups, win):
        assert abs(g[0]["pts_s"] - w["pts_start"]) < 1e-9
        unit.append(dict(regime=w["regime"],
                         kills=sum(x["delta"] for x in g),
                         sub={gg: subcount(g, gg) for gg in GRID}))
    # nesting sanity: sub-count is non-decreasing as the threshold tightens
    for u in unit:
        s = [u["sub"][gg] for gg in GRID]
        assert all(s[i] <= s[i + 1] for i in range(len(s) - 1)), "not nested"

    by = {r: [u for u in unit if u["regime"] == r] for r in ("R1", "R2", "R3")}
    K = {r: np.array([u["kills"] for u in by[r]], float) for r in by}
    S = {r: {gg: np.array([u["sub"][gg] for u in by[r]], float) for gg in GRID}
         for r in by}

    def ratio(lo, hi, gg, iL=None, iH=None):
        kl = K[lo] if iL is None else K[lo][iL]
        sl = S[lo][gg] if iL is None else S[lo][gg][iL]
        kh = K[hi] if iH is None else K[hi][iH]
        sh = S[hi][gg] if iH is None else S[hi][gg][iH]
        return (kh.sum() / sh.sum()) / (kl.sum() / sl.sum())

    out = {"grid_s": list(GRID), "nboot": NBOOT,
           "note": ("merge_share(g) = 1 - log R(g)/log R(5). Positive means "
                    "part of the climb dissolved when the segmentation grain "
                    "was tightened -- i.e. it was merge. Negative means the "
                    "climb grew SHARPER at finer grain, which merge cannot "
                    "produce.")}
    for lo, hi in (("R1", "R2"), ("R2", "R3"), ("R1", "R3")):
        rec = {}
        base = ratio(lo, hi, 5.0)
        nL, nH = len(by[lo]), len(by[hi])
        iL = RNG.integers(0, nL, size=(NBOOT, nL))
        iH = RNG.integers(0, nH, size=(NBOOT, nH))
        b_base = np.array([ratio(lo, hi, 5.0, iL[b], iH[b])
                           for b in range(NBOOT)])
        for gg in GRID:
            r = ratio(lo, hi, gg)
            ms = 1 - math.log(r) / math.log(base)
            b_r = np.array([ratio(lo, hi, gg, iL[b], iH[b])
                            for b in range(NBOOT)])
            good = (b_base > 1.0001) & (b_r > 0)
            b_ms = 1 - np.log(b_r[good]) / np.log(b_base[good])
            rec[f"gap_gt_{gg}"] = dict(
                ratio=round(r, 4),
                ratio_ci95=[round(float(np.percentile(b_r, 2.5)), 3),
                            round(float(np.percentile(b_r, 97.5)), 3)],
                merge_share=round(ms, 4),
                merge_share_ci95=[round(float(np.percentile(b_ms, 2.5)), 3),
                                  round(float(np.percentile(b_ms, 97.5)), 3)],
                boot_usable_frac=round(float(good.mean()), 4))
        rec["surviving_ratio_at_finest_grain"] = rec[
            f"gap_gt_{min(GRID)}"]["ratio"]
        out[f"{lo}_to_{hi}"] = rec

    json.dump(out, open(out_path, "w"), indent=1)
    for k, v in out.items():
        if not isinstance(v, dict):
            continue
        print(f"== {k} ==")
        for gg in GRID:
            d = v[f"gap_gt_{gg}"]
            print(f"  gap>{gg:>4}  R={d['ratio']:>6.3f} "
                  f"[{d['ratio_ci95'][0]:>5.2f},{d['ratio_ci95'][1]:>6.2f}]   "
                  f"merge_share={d['merge_share']:>7.3f} "
                  f"[{d['merge_share_ci95'][0]:>6.2f},"
                  f"{d['merge_share_ci95'][1]:>6.2f}]")


if __name__ == "__main__":
    main()
