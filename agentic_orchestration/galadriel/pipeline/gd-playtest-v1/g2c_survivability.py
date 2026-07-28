#!/usr/bin/env python3
"""G-2c -- survivability as a fourth causal channel (charter SS9 ripple 1) and
the temporal/denominator structure of R2's >=10%-EHP hits (ripple 2).

RUNS ONLY AFTER g2c_gate0.py PASSES. The gate is re-asserted in-process here;
on failure nothing downstream fires.

GRAIN: harness-v1 per R-KC1-8 -- encounter = kill-event run with internal gaps
> 5.0 s split, pad 3.0 s; burst <= 1.5 s. No re-segmentation is performed in
this pass. (The source-agnostic versioned refactor of tb_rollup.py is a routed
follow-up work item, NOT done here.)

EHP DENOMINATOR -- two readings, never mixed:
  * `hp_max_seen`  -- max CURRENT-hp observed in the window. This is what
    tb_rollup.py used, so it is what produced the charter's "27 drops >= 10%
    EHP" figure. It is a LOWER BOUND on true max HP: if the player never
    touched full health in the window the denominator is understated and every
    percentage is OVERSTATED.
  * `max_hp_modal` -- the modal right-operand of the full "cur/max" read. This
    is the true pool where it was read at all. Reported alongside as the
    primary sensitivity, because the whole question 2 is a denominator
    question and answering it on a lower-bound denominator would be circular.
"""
import gzip
import json
import math
import os
import statistics as st
import subprocess
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tb_windows as TW  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TA = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1",
                  "ta-full-2fps-gated.csv")
TB = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1-tb")
OUT = os.path.join(ROOT, "captures", "2026-07-28-gd-playtest-v1-g2c")

BURST_B = 1.5   # harness-v1 pack-proxy


# ---------------------------------------------------------------- utilities
def sp(x, y):
    """Spearman with n and p. Returns None if degenerate."""
    if len(x) < 4 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    r, p = stats.spearmanr(x, y)
    return dict(rho=round(float(r), 4), p=round(float(p), 6), n=len(x))


def partial_sp(x, y, z):
    """Partial Spearman of x,y controlling z: Pearson on rank-residuals."""
    if len(x) < 5:
        return None
    rx, ry, rz = (stats.rankdata(v) for v in (x, y, z))
    if np.std(rz) == 0:
        return None
    def resid(r):
        b = np.polyfit(rz, r, 1)
        return r - np.polyval(b, rz)
    ex, ey = resid(rx), resid(ry)
    if np.std(ex) < 1e-9 or np.std(ey) < 1e-9:
        return dict(rho=None, p=None, n=len(x),
                    note="control absorbs all rank variance in one argument")
    r, p = stats.pearsonr(ex, ey)
    return dict(rho=round(float(r), 4), p=round(float(p), 6), n=len(x))


def summ(v, nd=3):
    if not v:
        return None
    s = sorted(v)
    def q(p):
        return s[min(len(s) - 1, max(0, int(math.ceil(p * len(s))) - 1))]
    return dict(n=len(v), mean=round(st.mean(v), nd),
                median=round(st.median(v), nd), min=round(min(v), nd),
                p25=round(q(.25), nd), p75=round(q(.75), nd),
                max=round(max(v), nd),
                sd=round(st.stdev(v), nd) if len(v) > 1 else None)


# ---------------------------------------------------------------- load
def load_ta():
    import csv
    rows = []
    with open(TA) as fh:
        for r in csv.DictReader(fh):
            def i(k):
                v = r[k]
                return int(v) if v not in ("", "None") else None
            rows.append(dict(pts_s=float(r["pts_s"]), play_time=i("play_time"),
                             kills=i("kills"), deaths=i("deaths"),
                             max_level=i("max_level"),
                             dps=float(r["dps"]) if r["dps"] not in ("", "None")
                             else None))
    return rows


def pts_to_play_time(rows):
    pts = [(r["pts_s"], r["play_time"]) for r in rows
           if r["play_time"] is not None]
    return pts


def nearest(pairs, t):
    lo, hi = 0, len(pairs) - 1
    best, bd = None, 1e18
    while lo <= hi:
        m = (lo + hi) // 2
        d = abs(pairs[m][0] - t)
        if d < bd:
            bd, best = d, pairs[m][1]
        if pairs[m][0] < t:
            lo = m + 1
        else:
            hi = m - 1
    return best, bd


def level_at(rows, t):
    best, bd, lv = None, 1e18, None
    for r in rows:
        if r["max_level"] is None:
            continue
        d = abs(r["pts_s"] - t)
        if d < bd:
            bd, lv = d, r["max_level"]
    return lv, bd


# ---------------------------------------------------------------- main
def main():
    g0 = subprocess.run([sys.executable, os.path.join(HERE, "g2c_gate0.py")],
                        capture_output=True, text=True)
    if g0.returncode != 0:
        print("GATE 0 FAILED -- aborting", g0.stdout, g0.stderr)
        sys.exit(2)
    gate = json.load(open(os.path.join(OUT, "g2c-gate0.json")))
    assert gate["PASS"]

    rows = load_ta()
    ptmap = pts_to_play_time(rows)
    W = json.load(open(os.path.join(TB, "tb-intake-windows.json")))["windows"]
    kev = TW.kill_events(TW.load(TA))

    drops = [json.loads(l) for l in
             open(os.path.join(OUT, "g2c-drops.jsonl"))]
    by_eng = {}
    for d in drops:
        by_eng.setdefault(d["eng_id"], []).append(d)

    # --- per-engagement feature table -----------------------------------
    recs = []
    for w in W:
        e = w["eng_id"]
        ds = sorted(by_eng.get(e, []), key=lambda d: d["t"])
        ev = [k for k in kev if w["pts_start"] - 1e-6 <= k["pts_s"]
              <= w["pts_end"] + 1e-6]
        # bursts (harness-v1 pack-proxy, b = 1.5 s)
        bursts, cur = [], [ev[0]] if ev else []
        for k in ev[1:]:
            if k["pts_s"] - cur[-1]["pts_s"] > BURST_B:
                bursts.append(cur)
                cur = [k]
            else:
                cur.append(k)
        if cur:
            bursts.append(cur)
        # intra-engagement travel seconds (gaps > 2.5 s between kill events)
        gaps = [b["pts_s"] - a["pts_s"] for a, b in zip(ev, ev[1:])]
        travel_s = sum(g for g in gaps if g >= 2.5)
        # inter-drop gaps within the engagement
        dgaps = [b["t"] - a["t"] for a, b in zip(ds, ds[1:])]
        lv, lvd = level_at(rows, w["pts_start"])
        ehp_seen = w["hp_max_seen"]
        ehp_modal = w["max_hp_modal"]
        # the modal read is itself refusable: eng 31 returns 45 against a
        # current-HP high of 451 -- a truncated right operand. Reject any
        # modal max BELOW the window's observed current-HP high.
        modal_ok = (ehp_modal is not None and ehp_seen is not None
                    and ehp_modal >= ehp_seen)
        recs.append(dict(
            eng_id=e, regime=w["regime"], play_time=w["play_time_start"],
            pts_start=w["pts_start"], pts_end=w["pts_end"],
            level=lv, level_carrier_dist_s=round(lvd, 2),
            dur_s=w["dur_s"], kills=w["kills"], n_events=w["n_events"],
            n_bursts=len(bursts),
            A=round(w["kills"] / len(ev), 4) if ev else None,
            B=round(len(ev) / len(bursts), 4) if bursts else None,
            C=round(len(bursts) / 1.0, 4) if bursts else None,
            coverage=w["coverage"], delta_covered_s=w["delta_covered_s"],
            ehp_seen=ehp_seen, ehp_modal=ehp_modal, ehp_modal_ok=modal_ok,
            ehp=(ehp_modal if modal_ok else ehp_seen),
            intake_hp=w["intake_hp"], healed_hp=w["healed_hp"],
            n_drops=w["n_drops"],
            travel_s=round(travel_s, 2),
            active_s=round(w["dur_s"] - travel_s, 2),
            inter_drop_gap_median=round(st.median(dgaps), 4) if dgaps else None,
            n_inter_drop_gaps=len(dgaps),
            drops=[d["mag"] for d in ds]))

    R2 = [r for r in recs if r["regime"] == "R2"]
    R2 = sorted(R2, key=lambda r: r["play_time"])

    # ================================================================
    # Q1 -- is EHP an independent instrument within R2 at all?
    # ================================================================
    ehp_series = [(r["play_time"], r["ehp"], r["eng_id"]) for r in R2]
    nn = [(p, h) for p, h, _ in ehp_series if h is not None]
    mono = all(b >= a for (_, a), (_, b) in zip(nn, nn[1:]))
    levels = sorted(set(h for _, h in nn))
    # is EHP a DETERMINISTIC function of play_time? (each play_time -> one EHP)
    # and is it monotone non-decreasing? If yes, EHP has zero residual
    # variance given the clock and cannot be an independent instrument.
    plateaus = {}
    for p, h in nn:
        plateaus.setdefault(h, []).append(p)
    confound = dict(
        n_windows_with_ehp=len(nn),
        n_distinct_ehp_levels=len(levels),
        ehp_levels=levels,
        ehp_monotone_nondecreasing_in_play_time=mono,
        spearman_ehp_vs_play_time=sp([p for p, _ in nn], [h for _, h in nn]),
        spearman_ehp_vs_level=sp(
            [r["level"] for r in R2 if r["ehp"] is not None],
            [r["ehp"] for r in R2 if r["ehp"] is not None]),
        plateau_spans={str(h): dict(n=len(v), play_time_min=min(v),
                                    play_time_max=max(v),
                                    span_s=max(v) - min(v))
                       for h, v in sorted(plateaus.items())},
        ehp_ratio_within_R2=round(max(levels) / min(levels), 3))

    # --- candidate instruments, Spearman vs EHP AND vs play_time --------
    def col(rs, k):
        return [r[k] for r in rs]

    inst = {}
    base = [r for r in R2 if r["ehp"] is not None]
    defs = [
        ("engagement_duration_s", lambda r: r["dur_s"], base),
        ("kills", lambda r: r["kills"], base),
        ("kills_per_engagement_second",
         lambda r: r["kills"] / r["dur_s"] if r["dur_s"] > 0 else None, base),
        ("kills_per_active_second",
         lambda r: r["kills"] / r["active_s"] if r["active_s"] > 0 else None,
         base),
        ("A_simultaneity", lambda r: r["A"], base),
        ("B_events_per_burst", lambda r: r["B"], base),
        ("C_bursts_per_engagement", lambda r: r["n_bursts"], base),
        ("n_intake_events", lambda r: r["n_drops"], base),
        ("intake_events_per_covered_s",
         lambda r: r["n_drops"] / r["delta_covered_s"]
         if r["delta_covered_s"] >= 2.0 else None, base),
        ("intake_hp_per_covered_s",
         lambda r: r["intake_hp"] / r["delta_covered_s"]
         if r["delta_covered_s"] >= 2.0 else None, base),
        ("intake_pc_ehp_per_covered_s",
         lambda r: 100.0 * r["intake_hp"] / r["delta_covered_s"] / r["ehp"]
         if r["delta_covered_s"] >= 2.0 else None, base),
        ("intake_hp_per_engagement_covgated",
         lambda r: r["intake_hp"] if r["coverage"] >= 0.80 else None, base),
        ("intake_pc_ehp_per_engagement_covgated",
         lambda r: 100.0 * r["intake_hp"] / r["ehp"]
         if r["coverage"] >= 0.80 else None, base),
        ("intake_hp_per_kill_covgated",
         lambda r: r["intake_hp"] / r["kills"]
         if r["coverage"] >= 0.80 and r["kills"] else None, base),
        ("mean_drop_hp", lambda r: st.mean(r["drops"]) if r["drops"] else None,
         base),
        ("mean_drop_pc_ehp",
         lambda r: 100.0 * st.mean(r["drops"]) / r["ehp"] if r["drops"]
         else None, base),
        ("max_drop_hp", lambda r: max(r["drops"]) if r["drops"] else None,
         base),
        ("max_drop_pc_ehp",
         lambda r: 100.0 * max(r["drops"]) / r["ehp"] if r["drops"] else None,
         base),
        ("median_time_between_intake_events_s",
         lambda r: r["inter_drop_gap_median"], base),
        ("travel_fraction",
         lambda r: r["travel_s"] / r["dur_s"] if r["dur_s"] > 0 else None,
         base),
        ("globe_coverage", lambda r: r["coverage"], base),
    ]
    for name, f, rs in defs:
        pairs = [(r, f(r)) for r in rs]
        pairs = [(r, v) for r, v in pairs if v is not None]
        if len(pairs) < 5:
            inst[name] = dict(n=len(pairs), note="insufficient n")
            continue
        y = [v for _, v in pairs]
        ehp = [r["ehp"] for r, _ in pairs]
        pt = [r["play_time"] for r, _ in pairs]
        lvl = [r["level"] for r, _ in pairs]
        inst[name] = dict(
            n=len(pairs), summary=summ(y),
            vs_ehp=sp(ehp, y), vs_play_time=sp(pt, y), vs_level=sp(lvl, y),
            partial_ehp_given_play_time=partial_sp(ehp, y, pt),
            by_ehp_plateau={str(h): summ([v for r, v in pairs
                                          if r["ehp"] == h])
                            for h in levels
                            if len([1 for r, _ in pairs if r["ehp"] == h])},
            kruskal_across_ehp_plateaus=(lambda gs: (
                dict(H=round(float(stats.kruskal(*gs)[0]), 4),
                     p=round(float(stats.kruskal(*gs)[1]), 6),
                     k_groups=len(gs))
                if len(gs) >= 2 else None))(
                [[v for r, v in pairs if r["ehp"] == h] for h in levels
                 if len([1 for r, _ in pairs if r["ehp"] == h]) >= 3]))

    # --- EHP quartile table (G-2b style control for zone progression) ---
    qtab = []
    n = len(base)
    for qi in range(4):
        lo, hi = qi * n // 4, (qi + 1) * n // 4
        g = base[lo:hi]
        cg = [r for r in g if r["coverage"] >= 0.80]
        rg = [r for r in g if r["delta_covered_s"] >= 2.0]
        qtab.append(dict(
            quartile="Q%d" % (qi + 1), n=len(g),
            play_time=[g[0]["play_time"], g[-1]["play_time"]],
            level=[min(r["level"] for r in g), max(r["level"] for r in g)],
            ehp=[min(r["ehp"] for r in g), max(r["ehp"] for r in g)],
            kills_per_engagement=round(st.mean(col(g, "kills")), 3),
            dur_s_mean=round(st.mean(col(g, "dur_s")), 3),
            A=round(st.mean([r["A"] for r in g if r["A"]]), 3),
            B=round(st.mean([r["B"] for r in g if r["B"]]), 3),
            C=round(st.mean(col(g, "n_bursts")), 3),
            n_cov_gated=len(cg),
            intake_hp_mean_covgated=round(st.mean(col(cg, "intake_hp")), 1)
            if cg else None,
            intake_pc_ehp_mean_covgated=round(
                st.mean([100.0 * r["intake_hp"] / r["ehp"] for r in cg]), 2)
            if cg else None,
            intake_hp_per_covered_s=round(
                st.mean([r["intake_hp"] / r["delta_covered_s"] for r in rg]), 3)
            if rg else None,
            intake_pc_ehp_per_covered_s=round(
                st.mean([100.0 * r["intake_hp"] / r["delta_covered_s"] / r["ehp"]
                         for r in rg]), 4) if rg else None,
            drops_per_covered_s=round(
                st.mean([r["n_drops"] / r["delta_covered_s"] for r in rg]), 4)
            if rg else None,
            globe_coverage_mean=round(st.mean(col(g, "coverage")), 3)))

    # ================================================================
    # Q2 -- the >=10%-EHP hits in R2: temporal + denominator structure
    # ================================================================
    big = []
    allr2 = []
    for r in R2:
        ds = sorted(by_eng.get(r["eng_id"], []), key=lambda d: d["t"])
        for d in ds:
            pt, pd = nearest(ptmap, d["t"])
            row = dict(eng_id=r["eng_id"], t_pts=d["t"], play_time=pt,
                       pt_carrier_dist_s=round(pd, 2), level=r["level"],
                       raw_hp=d["mag"], hp_before=d["hp_before"],
                       hp_after=d["hp_after"],
                       ehp_seen=r["ehp_seen"], ehp_modal=r["ehp_modal"],
                       ehp_used=r["ehp"],
                       pc_ehp_seen=round(100.0 * d["mag"] / r["ehp_seen"], 3)
                       if r["ehp_seen"] else None,
                       pc_ehp_modal=round(100.0 * d["mag"] / r["ehp_modal"], 3)
                       if r["ehp_modal"] else None,
                       coverage=r["coverage"])
            allr2.append(row)
            if row["pc_ehp_seen"] is not None and row["pc_ehp_seen"] >= 10.0:
                big.append(row)
    big.sort(key=lambda r: r["play_time"])

    big_modal = [r for r in allr2
                 if r["pc_ehp_modal"] is not None and r["pc_ehp_modal"] >= 10.0]
    big_modal.sort(key=lambda r: r["play_time"])

    r2_pt0, r2_pt1 = 1134, 6052
    def posfrac(p):
        return round((p - r2_pt0) / (r2_pt1 - r2_pt0), 4)

    for r in big:
        r["r2_position_frac"] = posfrac(r["play_time"])
    for r in big_modal:
        r["r2_position_frac"] = posfrac(r["play_time"])

    # temporal test: are the 27 uniform over R2's COVERED intake time?
    # Null denominator is not wallclock -- it is admissible delta-covered time,
    # which is what the instrument could have seen a hit in. Build the covered
    # time per EHP plateau and test the observed counts against it.
    plat_cov, plat_drops, plat_big = {}, {}, {}
    for r in R2:
        h = r["ehp"]
        if h is None:
            continue
        plat_cov[h] = plat_cov.get(h, 0.0) + r["delta_covered_s"]
        plat_drops[h] = plat_drops.get(h, 0) + r["n_drops"]
    for b in big:
        plat_big[b["ehp_used"]] = plat_big.get(b["ehp_used"], 0) + 1
    tot_cov = sum(plat_cov.values())
    tot_big = len(big)
    plateau_tab = []
    for h in sorted(plat_cov):
        exp = tot_big * plat_cov[h] / tot_cov
        plateau_tab.append(dict(
            ehp=h, covered_s=round(plat_cov[h], 1),
            covered_frac=round(plat_cov[h] / tot_cov, 4),
            n_drops_all=plat_drops.get(h, 0),
            n_big=plat_big.get(h, 0), expected_big_if_uniform=round(exp, 2),
            play_time_span=[min(plateaus[h]), max(plateaus[h])]))
    obs = [p["n_big"] for p in plateau_tab]
    expv = [p["expected_big_if_uniform"] for p in plateau_tab]
    chi = None
    if min(expv) > 0:
        chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, expv))
        chi = dict(chi2=round(chi2, 3), df=len(obs) - 1,
                   p=round(float(1 - stats.chi2.cdf(chi2, len(obs) - 1)), 6),
                   note="low expected counts; report as descriptive")
    # distribution-free: Mann-Whitney of big-hit play_times vs all-drop
    # play_times, and vs the covered-time distribution
    all_pt = [r["play_time"] for r in allr2 if r["play_time"] is not None]
    big_pt = [r["play_time"] for r in big]
    mw = stats.mannwhitneyu(big_pt, [p for p in all_pt if p not in ()],
                            alternative="two-sided")
    # early/late split at R2 midpoint in COVERED time
    cum, half_pt = 0.0, None
    for r in R2:
        cum += r["delta_covered_s"]
        if half_pt is None and cum >= tot_cov / 2:
            half_pt = r["play_time"]
    q2 = dict(
        n_big_hp_max_seen_denominator=len(big),
        n_big_max_hp_modal_denominator=len(big_modal),
        n_drops_r2_total=len(allr2),
        frac_of_r2_drops=round(len(big) / len(allr2), 4),
        raw_hp=summ([r["raw_hp"] for r in big], 1),
        raw_hp_all_r2_drops=summ([r["raw_hp"] for r in allr2], 1),
        pc_ehp_seen=summ([r["pc_ehp_seen"] for r in big], 2),
        pc_ehp_modal=summ([r["pc_ehp_modal"] for r in big
                           if r["pc_ehp_modal"] is not None], 2),
        ehp_denominator_hist={},
        play_time=summ([float(r["play_time"]) for r in big], 1),
        r2_position_frac=summ([r["r2_position_frac"] for r in big], 4),
        r2_covered_time_midpoint_play_time=half_pt,
        n_big_before_covered_midpoint=sum(1 for r in big
                                          if r["play_time"] < half_pt),
        n_big_after_covered_midpoint=sum(1 for r in big
                                         if r["play_time"] >= half_pt),
        plateau_table=plateau_tab,
        chi2_uniform_over_covered_time=chi,
        mannwhitney_bigdrop_pt_vs_alldrop_pt=dict(
            U=float(mw[0]), p=round(float(mw[1]), 6),
            median_big=st.median(big_pt), median_all=st.median(all_pt)),
        spearman_raw_hp_vs_play_time_bigonly=sp(
            [r["play_time"] for r in big], [r["raw_hp"] for r in big]),
        spearman_raw_hp_vs_play_time_alldrops=sp(
            [r["play_time"] for r in allr2 if r["play_time"]],
            [r["raw_hp"] for r in allr2 if r["play_time"]]),
        spearman_raw_hp_vs_ehp_alldrops=sp(
            [r["ehp_used"] for r in allr2 if r["ehp_used"]],
            [r["raw_hp"] for r in allr2 if r["ehp_used"]]),
        rows=big)
    for r in big:
        k = str(r["ehp_used"])
        q2["ehp_denominator_hist"][k] = q2["ehp_denominator_hist"].get(k, 0) + 1

    # raw-HP-threshold re-expression: what does the SAME hit set look like if
    # you threshold on absolute HP instead of a moving denominator?
    thr = {}
    for t in (20, 30, 40, 50, 75, 100, 150, 200, 300, 500):
        sel = [r for r in allr2 if r["raw_hp"] >= t]
        sel.sort(key=lambda r: r["play_time"])
        early = sum(1 for r in sel if r["play_time"] < half_pt)
        thr[str(t)] = dict(n=len(sel), n_early=early, n_late=len(sel) - early,
                           median_play_time=st.median(
                               [r["play_time"] for r in sel]) if sel else None,
                           median_ehp=st.median([r["ehp_used"] for r in sel])
                           if sel else None)
    q2["raw_hp_threshold_sweep"] = thr

    res = dict(
        gate0=dict(PASS=True, source="g2c-gate0.json"),
        harness="harness-v1 (R-KC1-8): encounter gap>5.0s pad3.0s; burst<=1.5s",
        q1_confound_structure=confound,
        q1_instruments=inst,
        q1_ehp_quartiles=qtab,
        q2_big_hits=q2,
        r2_engagements=R2)
    json.dump(res, open(os.path.join(OUT, "g2c-survivability.json"), "w"),
              indent=1, default=str)

    # ---- CSVs ----
    import csv as _csv
    with open(os.path.join(OUT, "g2c-r2-engagements.csv"), "w",
              newline="") as fh:
        cols = ["eng_id", "play_time", "level", "dur_s", "kills", "n_events",
                "n_bursts", "A", "B", "ehp", "ehp_seen", "ehp_modal",
                "coverage", "delta_covered_s", "intake_hp", "healed_hp",
                "n_drops", "travel_s", "active_s",
                "inter_drop_gap_median"]
        wr = _csv.writer(fh)
        wr.writerow(cols)
        for r in R2:
            wr.writerow([r.get(c) for c in cols])
    with open(os.path.join(OUT, "g2c-r2-big-hits.csv"), "w", newline="") as fh:
        cols = ["eng_id", "play_time", "r2_position_frac", "level", "t_pts",
                "raw_hp", "hp_before", "hp_after", "ehp_seen", "ehp_modal",
                "ehp_used", "pc_ehp_seen", "pc_ehp_modal", "coverage"]
        wr = _csv.writer(fh)
        wr.writerow(cols)
        for r in big:
            wr.writerow([r.get(c) for c in cols])
    with open(os.path.join(OUT, "g2c-r2-all-drops.csv"), "w", newline="") as fh:
        cols = ["eng_id", "play_time", "t_pts", "raw_hp", "ehp_used",
                "pc_ehp_seen", "pc_ehp_modal", "coverage"]
        wr = _csv.writer(fh)
        wr.writerow(cols)
        for r in sorted(allr2, key=lambda r: r["t_pts"]):
            wr.writerow([r.get(c) for c in cols])

    # ---- console ----
    print("\n=== Q1 CONFOUND STRUCTURE (within R2) ===")
    print(json.dumps(confound, indent=1))
    print("\n=== Q1 INSTRUMENTS ===")
    for k, v in inst.items():
        if "vs_ehp" not in v:
            print("%-42s %s" % (k, v))
            continue
        print("%-42s n=%3d  vsEHP %-28s vsPT %-28s partial %s" % (
            k, v["n"], v["vs_ehp"], v["vs_play_time"],
            v["partial_ehp_given_play_time"]))
    print("\n=== Q1 QUARTILES ===")
    for r in qtab:
        print(json.dumps(r))
    print("\n=== Q2 ===")
    print(json.dumps({k: v for k, v in q2.items() if k != "rows"}, indent=1))
    print("\n=== Q2 the 27 rows ===")
    for r in big:
        print("eng%-3d pt=%-5s lvl=%-3s raw=%-4d ehp_seen=%-4s ehp_modal=%-5s "
              "pc_seen=%-6.2f pc_modal=%-6s pos=%.3f" % (
                  r["eng_id"], r["play_time"], r["level"], r["raw_hp"],
                  r["ehp_seen"], r["ehp_modal"], r["pc_ehp_seen"],
                  r["pc_ehp_modal"], r["r2_position_frac"]))


if __name__ == "__main__":
    main()
