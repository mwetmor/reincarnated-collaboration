#!/usr/bin/env python3
"""G-2c probes -- five checks the main pass surfaced and could not leave open.

P-1  DEATH COLLISION. The run's two death-counter increments, located on BOTH
     clocks, and checked against the drop ledger. The charter's SS9 anchor
     ("the 72.4% hit, 541 raw HP, EHP 747, late-regime") is tested against the
     death timestamps.
P-2  WITHIN-PLATEAU CLOCK TEST. Inside an EHP plateau the pool is constant.
     If behaviour still tracks play_time there, the clock -- not the pool --
     is what the between-plateau signal was riding.
P-3  BIG-HIT RATE PER COVERED SECOND, on a RAW-HP threshold (no moving
     denominator), per plateau and per early/late half. Settles the
     denominator-artifact question without using a denominator.
P-4  R2 EHP STEP SIZES vs LEVEL-UPS, plus the shield_block_chance series.
     Isolates gear events INSIDE R2.
P-5  SURVIVABILITY SIGNATURE TEST across the R2/R3 boundary. "Tankier holds
     pack centres" predicts C (bursts/engagement) and/or engagement duration
     to move. The DoT-tail hypothesis predicts B alone. Which moved?
"""
import csv
import json
import os
import statistics as st
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tb_windows as TW  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TA = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1",
                  "ta-full-2fps-gated.csv")
OUT = os.path.join(ROOT, "captures", "2026-07-28-gd-playtest-v1-g2c")
BURST_B = 1.5


def sp(x, y):
    if len(x) < 4 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    r, p = stats.spearmanr(x, y)
    return dict(rho=round(float(r), 4), p=round(float(p), 6), n=len(x))


def main():
    res = json.load(open(os.path.join(OUT, "g2c-survivability.json")))
    R2 = res["r2_engagements"]
    drops = [json.loads(l) for l in open(os.path.join(OUT, "g2c-drops.jsonl"))]
    rows = list(csv.DictReader(open(TA)))

    def num(r, k, f=int):
        v = r[k]
        return f(v) if v not in ("", "None") else None

    # ---------------- P-1 death collision ----------------
    deaths, prev = [], None
    for r in rows:
        d = num(r, "deaths")
        if d is None:
            continue
        if prev is not None and d > prev:
            deaths.append(dict(i=num(r, "i"), pts_s=float(r["pts_s"]),
                               play_time=num(r, "play_time"),
                               deaths=d))
        prev = d if prev is None else max(prev, d)
    dmap = {d["eng_id"]: d for d in []}
    # the biggest drop in the fixture and its neighbourhood on both clocks
    big = sorted(drops, key=lambda d: -d["mag"])[:6]
    for b in big:
        b["dist_to_nearest_death_pts_s"] = round(
            min(abs(b["t"] - d["pts_s"]) for d in deaths), 3) if deaths else None
    p1 = dict(death_increments=deaths, final_deaths=prev,
              largest_drops=big,
              note=("charter R-KC1-8 writes these two events as 'pt 2837' and "
                    "'pt 5152'; those are pts_s (video clock) values. Their "
                    "play_time values are different and are recorded here."))

    # ---------------- P-2 within-plateau clock test ----------------
    lv = {}
    for r in R2:
        if r["ehp"] is not None:
            lv.setdefault(r["ehp"], []).append(r)
    p2 = {}
    for metric, f in (
            ("kills", lambda r: r["kills"]),
            ("dur_s", lambda r: r["dur_s"]),
            ("A", lambda r: r["A"]),
            ("B", lambda r: r["B"]),
            ("n_bursts", lambda r: r["n_bursts"]),
            ("intake_hp_per_covered_s",
             lambda r: r["intake_hp"] / r["delta_covered_s"]
             if r["delta_covered_s"] >= 2.0 else None),
            ("coverage", lambda r: r["coverage"])):
        xs, ys = [], []
        for h, g in lv.items():
            if len(g) < 4:
                continue
            vals = [(r["play_time"], f(r)) for r in g]
            vals = [(a, b) for a, b in vals if b is not None]
            if len(vals) < 4 or len(set(v for _, v in vals)) < 2:
                continue
            rx = stats.rankdata([a for a, _ in vals])
            ry = stats.rankdata([b for _, b in vals])
            n = len(vals)
            xs += list((rx - (n + 1) / 2) / n)
            ys += list((ry - (n + 1) / 2) / n)
        p2[metric] = (dict(n_pooled=len(xs),
                           pearson_on_within_plateau_ranks=round(
                               float(stats.pearsonr(xs, ys)[0]), 4),
                           p=round(float(stats.pearsonr(xs, ys)[1]), 6))
                      if len(xs) >= 8 else dict(n_pooled=len(xs),
                                                note="insufficient"))

    # ---------------- P-3 raw-HP big-hit RATE per covered second -------
    cov_by_h, drops_by_h = {}, {}
    for r in R2:
        if r["ehp"] is None:
            continue
        cov_by_h[r["ehp"]] = cov_by_h.get(r["ehp"], 0.0) + r["delta_covered_s"]
    eng_ehp = {r["eng_id"]: r["ehp"] for r in R2}
    r2_eng = set(eng_ehp)
    p3 = {}
    for thr in (10, 20, 40, 75, 100):
        per = {}
        for h in sorted(cov_by_h):
            n = sum(1 for d in drops
                    if d["eng_id"] in r2_eng and eng_ehp[d["eng_id"]] == h
                    and d["mag"] >= thr)
            per[str(h)] = dict(n=n, covered_s=round(cov_by_h[h], 1),
                               per_100s=round(100.0 * n / cov_by_h[h], 2))
        p3["raw_ge_%d" % thr] = per
    # early/late split on the covered-time median (pt 3800, from the main pass)
    HALF = res["q2_big_hits"]["r2_covered_time_midpoint_play_time"]
    early_cov = sum(r["delta_covered_s"] for r in R2 if r["play_time"] < HALF)
    late_cov = sum(r["delta_covered_s"] for r in R2 if r["play_time"] >= HALF)
    eng_pt = {r["eng_id"]: r["play_time"] for r in R2}
    p3["early_late"] = dict(split_play_time=HALF,
                            early_covered_s=round(early_cov, 1),
                            late_covered_s=round(late_cov, 1))
    for thr in (10, 20, 40, 75, 100, 150):
        ne = sum(1 for d in drops if d["eng_id"] in r2_eng
                 and eng_pt[d["eng_id"]] < HALF and d["mag"] >= thr)
        nl = sum(1 for d in drops if d["eng_id"] in r2_eng
                 and eng_pt[d["eng_id"]] >= HALF and d["mag"] >= thr)
        tab = [[ne, nl], [max(early_cov, 1e-9), max(late_cov, 1e-9)]]
        # Poisson rate-ratio test on exposure
        rr = ((nl / late_cov) / (ne / early_cov)) if ne and early_cov else None
        pv = float(stats.binomtest(nl, ne + nl,
                                   late_cov / (early_cov + late_cov)).pvalue) \
            if (ne + nl) else None
        p3["early_late"]["raw_ge_%d" % thr] = dict(
            n_early=ne, n_late=nl,
            rate_early_per_100s=round(100.0 * ne / early_cov, 2),
            rate_late_per_100s=round(100.0 * nl / late_cov, 2),
            rate_ratio_late_over_early=round(rr, 2) if rr else None,
            binom_p_vs_covered_time_exposure=round(pv, 8) if pv else None)
        del tab

    # ---------------- P-4 EHP steps / level-ups / block ----------------
    lvls = []
    prev = None
    for r in rows:
        m = num(r, "max_level")
        if m is None:
            continue
        if prev is not None and m > prev:
            lvls.append(dict(pts_s=float(r["pts_s"]),
                             play_time=num(r, "play_time"), level=m))
        prev = m if prev is None else max(prev, m)
    blk, prevb = [], None
    for r in rows:
        b = num(r, "shield_block_chance", float)
        if b is None:
            continue
        if prevb is not None and b != prevb:
            blk.append(dict(pts_s=float(r["pts_s"]),
                            play_time=num(r, "play_time"),
                            frm=prevb, to=b))
        prevb = b
    plat = res["q1_confound_structure"]["plateau_spans"]
    steps = []
    keys = sorted(int(k) for k in plat)
    for a, b in zip(keys, keys[1:]):
        lo = plat[str(a)]["play_time_max"]
        hi = plat[str(b)]["play_time_min"]
        nlv = [x for x in lvls if lo < x["play_time"] <= hi]
        nbk = [x for x in blk if lo < (x["play_time"] or -1) <= hi]
        steps.append(dict(
            ehp_from=a, ehp_to=b, delta_hp=b - a,
            pct=round(100.0 * (b - a) / a, 2),
            bracket_play_time=[lo, hi], bracket_s=hi - lo,
            level_ups_in_bracket=[x["level"] for x in nlv],
            n_level_ups=len(nlv),
            hp_per_level_up=round((b - a) / len(nlv), 1) if nlv else None,
            block_changes_in_bracket=nbk))
    p4 = dict(level_ups=lvls, block_changes=blk, ehp_steps=steps,
              final_block=prevb)

    # ---------------- P-5 survivability signature across R2/R3 ---------
    W = json.load(open(os.path.join(
        ROOT, "captures", "2026-07-26-gd-playtest-v1-tb",
        "tb-intake-windows.json")))["windows"]
    kev = TW.kill_events(TW.load(TA))

    def factors(ws):
        A, B, C, D, K = [], [], [], [], []
        for w in ws:
            ev = [k for k in kev if w["pts_start"] - 1e-6 <= k["pts_s"]
                  <= w["pts_end"] + 1e-6]
            if not ev:
                continue
            bursts, cur = [], [ev[0]]
            for k in ev[1:]:
                if k["pts_s"] - cur[-1]["pts_s"] > BURST_B:
                    bursts.append(cur)
                    cur = [k]
                else:
                    cur.append(k)
            bursts.append(cur)
            A.append(w["kills"] / len(ev))
            B.append(len(ev) / len(bursts))
            C.append(len(bursts))
            D.append(w["dur_s"])
            K.append(w["kills"])
        return A, B, C, D, K

    r2last16 = [w for w in W if w["regime"] == "R2"][-16:]
    r3 = [w for w in W if w["regime"] == "R3"]
    fa, fb = factors(r2last16), factors(r3)
    names = ("A_simultaneity", "B_events_per_burst", "C_bursts_per_engagement",
             "duration_s", "kills")
    p5 = dict(baseline="R2 last 16 engagements (play_time 4604-5808)",
              comparand="R3 (play_time 6475-6847)", metrics={})
    for i, nm in enumerate(names):
        a, b = fa[i], fb[i]
        u = stats.mannwhitneyu(a, b, alternative="two-sided")
        p5["metrics"][nm] = dict(
            r2_last16_mean=round(st.mean(a), 3),
            r3_mean=round(st.mean(b), 3),
            ratio=round(st.mean(b) / st.mean(a), 3) if st.mean(a) else None,
            mannwhitney_p=round(float(u[1]), 5), n_r2=len(a), n_r3=len(b))
    p5["prediction_table"] = {
        "survivability_holds_pack_centres": "C up and/or duration up; A may rise",
        "dot_tail": "B up alone; A and C unchanged",
        "observed": "see metrics"}

    out = dict(P1_death_collision=p1, P2_within_plateau_clock=p2,
               P3_raw_threshold_rates=p3, P4_ehp_steps_and_gear=p4,
               P5_survivability_signature=p5)
    json.dump(out, open(os.path.join(OUT, "g2c-probes.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
