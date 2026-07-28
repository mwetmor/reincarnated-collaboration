#!/usr/bin/env python3
"""G-2c sensitivity -- can the two headline results be killed by one window?

S-1  The late-R2 big-hit enrichment, recomputed (a) leaving out the death
     engagement (eng 82), (b) leaving out the whole post-death tail
     (eng 82-89), (c) counted on ENGAGEMENTS rather than drops, and
     (d) leave-one-engagement-out over every late engagement.
S-2  The within-plateau hazard-vs-clock correlation, split per plateau.
S-3  A/B/C reconciliation: ratio-of-means (G-2b's regime aggregate) vs
     mean-of-ratios (this pass's per-engagement mean) for the R2-last-16 /
     R3 contrast, so the two artifacts cannot read as a discrepancy.
"""
import json
import os
import statistics as st
import sys

from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tb_windows as TW  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TA = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1",
                  "ta-full-2fps-gated.csv")
TB = os.path.join(ROOT, "captures", "2026-07-26-gd-playtest-v1-tb")
OUT = os.path.join(ROOT, "captures", "2026-07-28-gd-playtest-v1-g2c")
HALF = 3800
BURST_B = 1.5


def rate_test(R2, drops, thr, exclude=()):
    keep = [r for r in R2 if r["eng_id"] not in exclude]
    ec = sum(r["delta_covered_s"] for r in keep if r["play_time"] < HALF)
    lc = sum(r["delta_covered_s"] for r in keep if r["play_time"] >= HALF)
    pt = {r["eng_id"]: r["play_time"] for r in keep}
    ne = sum(1 for d in drops if d["eng_id"] in pt
             and pt[d["eng_id"]] < HALF and d["mag"] >= thr)
    nl = sum(1 for d in drops if d["eng_id"] in pt
             and pt[d["eng_id"]] >= HALF and d["mag"] >= thr)
    if ne + nl == 0 or ec == 0 or lc == 0:
        return None
    p = float(stats.binomtest(nl, ne + nl, lc / (ec + lc)).pvalue)
    return dict(thr=thr, n_early=ne, n_late=nl,
                rate_early_per_100s=round(100 * ne / ec, 2),
                rate_late_per_100s=round(100 * nl / lc, 2),
                rate_ratio=round((nl / lc) / (ne / ec), 2) if ne else None,
                binom_p=round(p, 8), excluded=sorted(exclude))


def main():
    res = json.load(open(os.path.join(OUT, "g2c-survivability.json")))
    R2 = res["r2_engagements"]
    drops = [json.loads(l) for l in open(os.path.join(OUT, "g2c-drops.jsonl"))]
    r2ids = {r["eng_id"] for r in R2}
    drops = [d for d in drops if d["eng_id"] in r2ids]

    s1 = dict(full={}, no_death_engagement={}, no_post_death_tail={},
              engagement_unit={}, leave_one_out_worst={})
    tail = {82, 83, 84, 85, 86, 87, 88, 89}
    for thr in (20, 40, 75, 100):
        s1["full"]["raw_ge_%d" % thr] = rate_test(R2, drops, thr)
        s1["no_death_engagement"]["raw_ge_%d" % thr] = rate_test(
            R2, drops, thr, exclude={82})
        s1["no_post_death_tail"]["raw_ge_%d" % thr] = rate_test(
            R2, drops, thr, exclude=tail)

    # engagement unit: how many DISTINCT engagements carry a >= thr hit?
    for thr in (20, 40, 75, 100):
        eids = {d["eng_id"] for d in drops if d["mag"] >= thr}
        pt = {r["eng_id"]: r["play_time"] for r in R2}
        ne = sum(1 for e in eids if pt[e] < HALF)
        nl = sum(1 for e in eids if pt[e] >= HALF)
        te = sum(1 for r in R2 if r["play_time"] < HALF)
        tl = sum(1 for r in R2 if r["play_time"] >= HALF)
        tab = [[ne, te - ne], [nl, tl - nl]]
        s1["engagement_unit"]["raw_ge_%d" % thr] = dict(
            n_eng_early=ne, of_early=te, n_eng_late=nl, of_late=tl,
            frac_early=round(ne / te, 3), frac_late=round(nl / tl, 3),
            fisher_p=round(float(stats.fisher_exact(tab)[1]), 6))

    # leave-one-engagement-out over LATE engagements, at thr 40 and 75
    for thr in (40, 75):
        worst = None
        for r in R2:
            if r["play_time"] < HALF:
                continue
            t = rate_test(R2, drops, thr, exclude={r["eng_id"]})
            if t and (worst is None or t["binom_p"] > worst["binom_p"]):
                worst = dict(t, dropped_eng=r["eng_id"])
        s1["leave_one_out_worst"]["raw_ge_%d" % thr] = worst

    # per-engagement contribution census at thr 75
    contrib = {}
    for d in drops:
        if d["mag"] >= 75:
            contrib[d["eng_id"]] = contrib.get(d["eng_id"], 0) + 1
    s1["contributors_ge_75"] = dict(sorted(contrib.items()))

    # ---------------- S-2 ----------------
    lv = {}
    for r in R2:
        if r["ehp"] is not None and r["delta_covered_s"] >= 2.0:
            lv.setdefault(r["ehp"], []).append(r)
    s2 = {}
    for h, g in sorted(lv.items()):
        if len(g) < 4:
            s2[str(h)] = dict(n=len(g), note="n<4")
            continue
        x = [r["play_time"] for r in g]
        y = [r["intake_hp"] / r["delta_covered_s"] for r in g]
        rr, pp = stats.spearmanr(x, y)
        s2[str(h)] = dict(n=len(g), rho=round(float(rr), 4),
                          p=round(float(pp), 5),
                          median_intake_hp_per_s=round(st.median(y), 3))

    # ---------------- S-3 ----------------
    W = json.load(open(os.path.join(TB, "tb-intake-windows.json")))["windows"]
    kev = TW.kill_events(TW.load(TA))

    def agg(ws):
        tk = te = tb_ = 0
        A, B, C = [], [], []
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
            tk += w["kills"]
            te += len(ev)
            tb_ += len(bursts)
            A.append(w["kills"] / len(ev))
            B.append(len(ev) / len(bursts))
            C.append(len(bursts))
        return dict(
            n=len(ws),
            A_ratio_of_means=round(tk / te, 4), A_mean_of_ratios=round(st.mean(A), 4),
            B_ratio_of_means=round(te / tb_, 4), B_mean_of_ratios=round(st.mean(B), 4),
            C_ratio_of_means=round(tb_ / len(ws), 4), C_mean_of_ratios=round(st.mean(C), 4),
            kills_per_engagement=round(tk / len(ws), 4))

    r2l16 = [w for w in W if w["regime"] == "R2"][-16:]
    r3 = [w for w in W if w["regime"] == "R3"]
    s3 = dict(R2_last16=agg(r2l16), R3=agg(r3),
              note=("G-2b SS5d reports the RATIO-OF-MEANS form (regime "
                    "aggregate). This pass's P-5 Mann-Whitney runs on the "
                    "per-engagement distribution, hence MEAN-OF-RATIOS. Both "
                    "are printed so the two artifacts cannot read as a "
                    "discrepancy."))

    out = dict(S1_late_enrichment_sensitivity=s1,
               S2_within_plateau_hazard_by_plateau=s2,
               S3_ABC_reconciliation=s3)
    json.dump(out, open(os.path.join(OUT, "g2c-sensitivity.json"), "w"),
              indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
