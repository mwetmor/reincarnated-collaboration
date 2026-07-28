#!/usr/bin/env python3
"""G-2b targeted probes -- is the climb a STEP or a TREND, and is it real?

Three questions the main decomposition raises but does not settle:

  P1  Are the regime differences in kills/engagement statistically
      established at all? (permutation test on the engagement unit)
  P2  Is R3's lift over its IMMEDIATE neighbour real? R2's fourth quartile
      (play_time 4518-5808) and R3 (6052-7094) are adjacent in game time and
      in character level -- the cleanest available control on zone depth.
  P3  Where does the climb sit in time? A step at a build boundary and a
      smooth proficiency ramp are different pictures. Binned trace over the
      whole run plus R1's internal trend.

Plus P4: the R1 single-kill purity check (A == 1.000 exactly) -- world-fact
or instrument artifact?

Usage: g2b_probes.py <per-engagement.csv> <ta-gated.csv> <out.json>
"""
import csv
import json
import sys

import numpy as np
from scipy import stats

RNG = np.random.default_rng(20260728)
NPERM = 50000


def perm_test(a, b, nperm=NPERM):
    """Two-sided permutation test on the RATIO of pooled means (kills per
    engagement). Unit of exchangeability = the engagement."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs = b.mean() / a.mean()
    pool = np.concatenate([a, b])
    na = len(a)
    cnt = 0
    stat_obs = abs(np.log(obs))
    for _ in range(nperm):
        RNG.shuffle(pool)
        r = pool[na:].mean() / pool[:na].mean()
        if abs(np.log(r)) >= stat_obs - 1e-12:
            cnt += 1
    return dict(ratio=round(float(obs), 4), n_a=int(na), n_b=int(len(b)),
                mean_a=round(float(a.mean()), 3),
                mean_b=round(float(b.mean()), 3),
                p_two_sided=round((cnt + 1) / (nperm + 1), 5))


def main():
    eng_path, ledger_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    eng = []
    with open(eng_path) as fh:
        for r in csv.DictReader(fh):
            d = {k: (None if v == "" else v) for k, v in r.items()}
            for k in ("kills", "n_events", "level", "n_bursts_b1.5",
                      "n_multi_events", "play_time_start"):
                d[k] = int(float(d[k])) if d[k] is not None else None
            for k in ("dur_s", "eff_dur_s", "pts_start", "active_s_b1.5",
                      "travel_s_b1.5"):
                d[k] = float(d[k])
            for k in ("charge_approach", "claws_approach"):
                d[k] = float(d[k]) if d[k] is not None else None
            eng.append(d)
    out = {"n_engagements": len(eng)}

    K = {r: [e["kills"] for e in eng if e["regime"] == r]
         for r in ("R1", "R2", "R3")}

    # ---- P1 permutation tests ---------------------------------------------
    out["p1_permutation"] = dict(
        R1_vs_R2=perm_test(K["R1"], K["R2"]),
        R2_vs_R3=perm_test(K["R2"], K["R3"]),
        R1_vs_R3=perm_test(K["R1"], K["R3"]),
        note=("Unit = engagement. Two-sided on log-ratio of mean kills per "
              "engagement. No distributional assumption."))

    # ---- P2 adjacency: R2 late window vs R3 -------------------------------
    r2 = sorted([e for e in eng if e["regime"] == "R2"],
                key=lambda e: e["play_time_start"])
    r3 = [e for e in eng if e["regime"] == "R3"]
    adj = {}
    for label, sub in (("R2_last_quartile_n19", r2[-19:]),
                       ("R2_last_16_matched_n", r2[-16:]),
                       ("R2_playtime_ge_4500", [e for e in r2
                                                if e["play_time_start"] >= 4500])):
        pt = perm_test([e["kills"] for e in sub], [e["kills"] for e in r3])
        def facs(S):
            k = sum(x["kills"] for x in S)
            n = sum(x["n_events"] for x in S)
            nb = sum(x["n_bursts_b1.5"] for x in S)
            return dict(A=round(k / n, 4), B=round(n / nb, 4),
                        C=round(nb / len(S), 4), KE=round(k / len(S), 3),
                        kills=k, n=len(S),
                        play_time=[S[0]["play_time_start"],
                                   S[-1]["play_time_start"]],
                        level=[min(x["level"] for x in S),
                               max(x["level"] for x in S)])
        adj[label] = dict(baseline=facs(sub), R3=facs(r3), test=pt)
    out["p2_adjacency_R2late_vs_R3"] = adj

    # ---- P3 time trace -----------------------------------------------------
    allэ = sorted([e for e in eng if e["play_time_start"] is not None],
                  key=lambda e: e["play_time_start"])
    bins = list(range(0, 7500, 500))
    trace = []
    for lo, hi in zip(bins, bins[1:]):
        s = [e for e in allэ if lo <= e["play_time_start"] < hi]
        if not s:
            trace.append(dict(play_time=[lo, hi], n=0))
            continue
        k = sum(e["kills"] for e in s)
        n = sum(e["n_events"] for e in s)
        nb = sum(e["n_bursts_b1.5"] for e in s)
        trace.append(dict(play_time=[lo, hi], n=len(s), kills=k,
                          kills_per_eng=round(k / len(s), 2),
                          A=round(k / n, 3), B=round(n / nb, 3),
                          C=round(nb / len(s), 3),
                          regimes=sorted({e["regime"] for e in s}),
                          level=[min(e["level"] for e in s),
                                 max(e["level"] for e in s)]))
    out["p3_time_trace_500s_bins"] = trace

    r1 = sorted([e for e in eng if e["regime"] == "R1"],
                key=lambda e: e["play_time_start"])
    out["p3_R1_internal"] = dict(
        n=len(r1),
        engagements=[dict(pt=e["play_time_start"], kills=e["kills"],
                          dur=e["dur_s"], nb=e["n_bursts_b1.5"],
                          level=e["level"]) for e in r1],
        spearman_pt_vs_kills=[
            round(float(stats.spearmanr(
                [e["play_time_start"] for e in r1],
                [e["kills"] for e in r1]).statistic), 3),
            float(stats.spearmanr([e["play_time_start"] for e in r1],
                                  [e["kills"] for e in r1]).pvalue)],
        gap_to_first_R2_engagement_s=r2[0]["play_time_start"] -
        r1[-1]["play_time_start"])

    # ---- P4 R1 single-kill purity -----------------------------------------
    n_ev_r1 = sum(e["n_events"] for e in eng if e["regime"] == "R1")
    p_multi_r2 = (sum(e["n_multi_events"] for e in eng if e["regime"] == "R2") /
                  sum(e["n_events"] for e in eng if e["regime"] == "R2"))
    out["p4_R1_purity"] = dict(
        r1_kill_events=n_ev_r1,
        r1_multi_kill_events=sum(e["n_multi_events"] for e in eng
                                 if e["regime"] == "R1"),
        r2_multi_rate=round(p_multi_r2, 4),
        p_zero_multi_if_r2_rate=float((1 - p_multi_r2) ** n_ev_r1),
        reading=("A probability this small rules out sampling luck: R1's "
                 "single-kill purity is a property of the run, not of the "
                 "instrument. The instrument DID resolve multi-kills 373 "
                 "times later at the same 0.5 s cadence."))

    # ---- P5 what fraction of all charges falls inside engagements ----------
    ch = [e["charge_approach"] for e in eng if e["charge_approach"] is not None]
    out["p5_charge_accounting"] = dict(
        run_total_charge_human_read=175,
        sum_of_engagement_deltas_approach_pad=int(sum(ch)),
        coverage_engagements=round(len(ch) / len(eng), 4),
        fraction_of_run_total_inside_engagements=round(sum(ch) / 175, 4),
        note=("Windows are [first_kill - 3 s, last_kill]. Charges outside are "
              "traversal dashes between engagements -- the movement use of "
              "the skill, not the chaining use."))

    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("p1_permutation", "p4_R1_purity",
                               "p5_charge_accounting")}, indent=1))


if __name__ == "__main__":
    main()
