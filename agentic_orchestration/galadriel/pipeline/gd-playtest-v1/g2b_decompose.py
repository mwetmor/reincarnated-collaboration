#!/usr/bin/env python3
"""G-2b -- causal decomposition of the kills/engagement climb (GP-gd-2026-07-26-s1).

The verdict (gandalf 2026-07-26 SS3) reads the 3.3 -> 8.4 -> 11.9 kills/engagement
progression as "the build engages larger packs". Matt contests the attribution:
growing PROFICIENCY may drive part of it, via
  (a) dash-chaining between spatially distinct packs (Charge), which a gap>5 s
      segmentation MERGES into one "engagement" -- a measurement artifact; and
  (b) centre-of-pack targeting with AoE claws -- more kills per 0.5 s sample.
Pack size may ALSO have grown. This script decomposes the confound.

METHOD -- multiplicative identity, exact by construction:

    kills/engagement  ==  (kills / kill-event)          FACTOR A
                       x  (kill-events / burst)         FACTOR B
                       x  (bursts / engagement)         FACTOR C

  A -- simultaneity. Kills landing inside ONE 0.5 s sample. Jointly the AoE
       signature and a pack-density signature; the two are NOT separable at
       this sampling rate (declared, not hidden).
  B -- contact persistence. How long a single tight cluster of killing runs.
  C -- bursts per engagement. A burst is a maximal run of kill events with all
       internal gaps <= b. C > 1 means the gap>5 s window swallowed >1 tight
       cluster: exactly the dash-chain merge Matt describes. C is the
       MEASUREMENT-ARTIFACT channel.

Everything is MEASURED-grade: refusals are never interpolated, coverage is
emitted per metric, and the 106-window derivation is reproduced and asserted
against the committed T-B artifact before anything downstream fires.

Usage:
  g2b_decompose.py <ta-gated.csv> <tb-engagement-windows.json> <outdir>
"""
import csv
import importlib.util
import json
import math
import os
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DT = 0.5          # ledger cadence, seconds (2 fps)
SEG_GAP = 5.0            # verdict SS4 segmentation rule
BURST_B = (1.0, 1.5, 2.0)
BURST_PRIMARY = 1.5
SENS_GAPS = (5.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.0)
ANCHOR_TOL = 2.0         # s; max distance a gated counter read may sit from a
                         # window edge and still anchor a delta
APPROACH_PAD = 3.0       # s; charge into the first pack precedes the first kill
REGIMES = ("R1", "R2", "R3")
RNG = np.random.default_rng(20260728)
NBOOT = 20000


def _load_tb_windows_module():
    spec = importlib.util.spec_from_file_location(
        "tb_windows", os.path.join(HERE, "tb_windows.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


TBW = _load_tb_windows_module()


# ---------------------------------------------------------------- ledger ---

def load_ledger(path):
    """Full ledger with every counter column kept as (value | None).

    None means the gate REFUSED or OCR returned nothing. It is never filled.
    """
    num = ("pts_s", "life_healed", "dps")
    ints = ("play_time", "kills", "deaths", "max_level", "total_score",
            "health_potions", "mana_potions", "defaultkickattack",
            "defaultweaponattack", "onslaught", "werewolf1",
            "werewolf1_skill01_claws", "werewolf1_skill02_charge")
    rows = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            d = {"gate": r["gate"]}
            for c in num:
                d[c] = float(r[c]) if r[c] else None
            for c in ints:
                d[c] = int(r[c]) if r[c] else None
            rows.append(d)
    return rows


def monotone_series(rows, col):
    """(t, v) pairs for a gated counter, keeping only non-regressing reads.

    GD's counters are monotone by construction; a read below the running max is
    an OCR misread and is DROPPED (not clamped, not interpolated). Returns the
    surviving reads plus a refusal/rejection census.
    """
    ts, vs = [], []
    hi, rejected, refused = None, 0, 0
    for r in rows:
        v = r[col]
        if v is None:
            refused += 1
            continue
        if hi is not None and v < hi:
            rejected += 1
            continue
        hi = v
        ts.append(r["pts_s"])
        vs.append(v)
    return (np.asarray(ts), np.asarray(vs),
            dict(n_total=len(rows), n_kept=len(ts), n_refused=refused,
                 n_nonmonotone_dropped=rejected,
                 coverage=round(len(ts) / len(rows), 4)))


def anchored_delta(ts, vs, t0, t1, tol=ANCHOR_TOL):
    """Counter delta across [t0, t1] using the nearest gated reads.

    Anchor at t0 = last read at or before t0 (fallback: first read after t0);
    anchor at t1 = last read at or before t1. Both anchors must sit within
    `tol` of their edge or the delta is REFUSED (returns None) -- an unanchored
    delta is an invented measurement.
    """
    if len(ts) == 0:
        return None, None
    def anchor(t, prefer_before):
        i = int(np.searchsorted(ts, t, side="right")) - 1
        cands = []
        if 0 <= i < len(ts):
            cands.append(i)
        if i + 1 < len(ts):
            cands.append(i + 1)
        if not cands:
            return None
        if prefer_before and 0 <= i < len(ts) and abs(ts[i] - t) <= tol:
            return i
        best = min(cands, key=lambda j: abs(ts[j] - t))
        return best if abs(ts[best] - t) <= tol else None
    i0 = anchor(t0, True)
    i1 = anchor(t1, True)
    if i0 is None or i1 is None:
        return None, None
    d = float(vs[i1] - vs[i0])
    slack = float(max(abs(ts[i0] - t0), abs(ts[i1] - t1)))
    return (d if d >= 0 else None), slack


# ------------------------------------------------------- segmentation ------

def segment_events(ev, gap):
    out, cur = [], [ev[0]]
    for e in ev[1:]:
        if e["pts_s"] - cur[-1]["pts_s"] > gap:
            out.append(cur)
            cur = [e]
        else:
            cur.append(e)
    out.append(cur)
    return out


def bursts_of(group, b):
    """Split one engagement's kill events into bursts at internal gaps > b."""
    out, cur = [], [group[0]]
    for e in group[1:]:
        if e["pts_s"] - cur[-1]["pts_s"] > b:
            out.append(cur)
            cur = [e]
        else:
            cur.append(e)
    out.append(cur)
    return out


# ------------------------------------------------------------ bootstrap ----

def boot_ratio(per_eng_num, per_eng_den, nboot=NBOOT):
    """Percentile CI for sum(num)/sum(den) resampling ENGAGEMENTS (the unit of
    independence). Returns (point, lo95, hi95)."""
    n = len(per_eng_num)
    if n == 0 or sum(per_eng_den) == 0:
        return (float("nan"),) * 3
    num = np.asarray(per_eng_num, float)
    den = np.asarray(per_eng_den, float)
    point = num.sum() / den.sum()
    idx = RNG.integers(0, n, size=(nboot, n))
    s = num[idx].sum(1) / np.maximum(den[idx].sum(1), 1e-12)
    return (float(point), float(np.percentile(s, 2.5)),
            float(np.percentile(s, 97.5)))


# ------------------------------------------------------------------ main ---

def main():
    ledger_path, windows_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    out = {"provenance": dict(ledger=ledger_path, tb_windows=windows_path,
                              sample_dt_s=SAMPLE_DT, seg_gap_s=SEG_GAP,
                              burst_thresholds_s=list(BURST_B),
                              burst_primary_s=BURST_PRIMARY,
                              anchor_tol_s=ANCHOR_TOL, nboot=NBOOT)}

    # ---- gate 0: reproduce the 106-window derivation, assert vs committed ---
    rows_min = TBW.load(ledger_path)
    ev = TBW.kill_events(rows_min)
    groups5 = TBW.segment(ev, SEG_GAP)
    committed = json.load(open(windows_path))
    repro = dict(n_kill_event_samples=len(ev),
                 total_kills=sum(e["delta"] for e in ev),
                 n_engagements=len(groups5),
                 dur_median=float(np.median(
                     [g[-1]["pts_s"] - g[0]["pts_s"] for g in groups5])),
                 dur_max=float(max(g[-1]["pts_s"] - g[0]["pts_s"]
                                   for g in groups5)))
    ok = (repro["n_engagements"] == committed["n_engagements"] ==
          len(committed["windows"]) == 106 and
          repro["total_kills"] == committed["total_kills"] and
          repro["n_kill_event_samples"] == committed["n_kill_event_samples"] and
          abs(repro["dur_median"] - committed["dur_median"]) < 1e-9 and
          abs(repro["dur_max"] - committed["dur_max"]) < 1e-9)
    out["gate0_reproduction"] = dict(reproduced=repro, ok=bool(ok))
    if not ok:
        json.dump(out, open(os.path.join(outdir, "g2b-decomposition.json"), "w"),
                  indent=1)
        raise SystemExit("GATE 0 FAILED -- segmentation does not reproduce; "
                         "nothing downstream may fire.")

    # regime label per engagement, taken from the committed windows
    win = committed["windows"]
    assert len(win) == len(groups5)
    for w, g in zip(win, groups5):
        assert abs(w["pts_start"] - g[0]["pts_s"]) < 1e-9
        assert w["kills"] == sum(x["delta"] for x in g)
    reg = [w["regime"] for w in win]

    rows = load_ledger(ledger_path)
    lvl_t = np.asarray([r["pts_s"] for r in rows if r["max_level"] is not None])
    lvl_v = np.asarray([r["max_level"] for r in rows
                        if r["max_level"] is not None])

    # ================================================== D1 gap structure ====
    gaps = {r: [] for r in REGIMES}
    gaps_long = {r: [] for r in REGIMES}     # engagements with dur >= 10 s
    gaps_short = {r: [] for r in REGIMES}
    for g, rg in zip(groups5, reg):
        if len(g) < 2:
            continue
        dd = [round(g[i + 1]["pts_s"] - g[i]["pts_s"], 3)
              for i in range(len(g) - 1)]
        gaps[rg] += dd
        dur = g[-1]["pts_s"] - g[0]["pts_s"]
        (gaps_long if dur >= 10.0 else gaps_short)[rg] += dd

    def gap_block(sample):
        a = np.asarray(sample, float)
        n = len(a)
        if n == 0:
            return dict(n=0)
        edges = np.arange(0.25, 5.26, 0.5)
        cnt, _ = np.histogram(a, bins=edges)
        centres = np.round(np.arange(0.5, 5.01, 0.5), 2)
        # exponential null: within-engagement kills as one homogeneous process.
        # Gaps are discretised to 0.5 s and RIGHT-TRUNCATED at 5.0 s by the
        # segmentation rule; fit lambda by MLE on the interval likelihood.
        def nll(lam):
            if lam <= 0:
                return 1e18
            F = lambda x: 1 - math.exp(-lam * x)
            p = np.array([F(c) - F(c - 0.5) for c in centres])
            p = p / F(5.0)
            p = np.clip(p, 1e-12, 1)
            return -float((cnt * np.log(p)).sum())
        lo, hi = 1e-3, 50.0
        for _ in range(200):                       # golden-section
            m1 = lo + 0.382 * (hi - lo)
            m2 = lo + 0.618 * (hi - lo)
            if nll(m1) < nll(m2):
                hi = m2
            else:
                lo = m1
        lam = 0.5 * (lo + hi)
        F = lambda x: 1 - math.exp(-lam * x)
        p = np.array([F(c) - F(c - 0.5) for c in centres]) / F(5.0)
        exp = p * n
        keep = exp >= 1.0
        chi2 = float(((cnt[keep] - exp[keep]) ** 2 / exp[keep]).sum())
        dof = max(1, int(keep.sum()) - 2)
        pval = float(stats.chi2.sf(chi2, dof))
        resid = (cnt - exp) / np.sqrt(np.maximum(exp, 1e-9))
        # trough test: is the PMF monotone-decreasing (single mode at 0.5)?
        f = cnt / n
        trough = None
        for i in range(1, len(f) - 1):
            if f[i] < f[i - 1] and any(f[j] > f[i] for j in range(i + 1, len(f))):
                trough = float(centres[i])
                break
        return dict(
            n=n, mean=round(float(a.mean()), 3),
            median=float(np.median(a)),
            pmf={str(c): round(float(x), 4) for c, x in zip(centres, f)},
            counts={str(c): int(x) for c, x in zip(centres, cnt)},
            frac_burst_le_1_5=round(float((a <= 1.5).mean()), 4),
            frac_travel_ge_2_5=round(float((a >= 2.5).mean()), 4),
            frac_travel_ge_2_5_ci=[round(v, 4) for v in
                                   boot_ratio((a >= 2.5).astype(float),
                                              np.ones(n))[1:]],
            exp_null_lambda=round(lam, 4),
            exp_null_chi2=round(chi2, 2), exp_null_dof=dof,
            exp_null_p=pval,
            exp_null_std_resid={str(c): round(float(x), 2)
                                for c, x in zip(centres, resid)},
            monotone_decreasing=(trough is None),
            first_trough_s=trough)

    out["d1_gap_structure"] = dict(
        all={r: gap_block(gaps[r]) for r in REGIMES},
        long_engagements_ge_10s={r: gap_block(gaps_long[r]) for r in REGIMES},
        short_engagements_lt_10s={r: gap_block(gaps_short[r]) for r in REGIMES},
        note=("Gaps are quantised to 0.5 s by the ledger cadence and right-"
              "truncated at 5.0 s by the segmentation rule. A single "
              "homogeneous within-engagement kill process implies a monotone-"
              "decreasing truncated-exponential PMF; a travel mode implies "
              "positive residuals in the >=2.5 s bins."))

    # ============================================ D1b sensitivity re-seg ====
    def regime_at(e):
        pt = e["play_time"]
        if pt is None:
            return None
        return TBW.regime_of(pt)
    # carrier for kill events whose play_time refused
    ptc = TBW.interp_play_time(rows_min)
    ev_reg = []
    for e in ev:
        r = regime_at(e)
        if r is None:
            r = TBW.regime_of(TBW.nearest_pt(ptc, e["pts_s"])[0])
        ev_reg.append(r)

    sens = {}
    for gp in SENS_GAPS:
        gs = segment_events(ev, gp)
        rec = {}
        for rname in REGIMES:
            sel = [g for g in gs
                   if TBW.regime_of(
                       g[0]["play_time"] if g[0]["play_time"] is not None
                       else TBW.nearest_pt(ptc, g[0]["pts_s"])[0]) == rname]
            k = [sum(x["delta"] for x in g) for g in sel]
            pt, lo, hi = boot_ratio(k, [1.0] * len(k))
            rec[rname] = dict(n_engagements=len(sel), kills=int(sum(k)),
                              kills_per_engagement=round(pt, 3),
                              ci95=[round(lo, 3), round(hi, 3)])
        base = rec["R1"]["kills_per_engagement"]
        rec["ratio_R2_over_R1"] = round(
            rec["R2"]["kills_per_engagement"] / base, 3) if base else None
        rec["ratio_R3_over_R1"] = round(
            rec["R3"]["kills_per_engagement"] / base, 3) if base else None
        rec["ratio_R3_over_R2"] = round(
            rec["R3"]["kills_per_engagement"] /
            rec["R2"]["kills_per_engagement"], 3)
        rec["n_engagements_total"] = len(gs)
        sens[f"gap_gt_{gp}"] = rec
    out["d1b_sensitivity_resegmentation"] = sens

    # ============================================ D2/D3/D4 per-engagement ===
    series = {}
    for col in ("werewolf1_skill02_charge", "werewolf1_skill01_claws",
                "defaultweaponattack", "onslaught", "werewolf1"):
        t, v, cen = monotone_series(rows, col)
        series[col] = (t, v)
        out.setdefault("series_census", {})[col] = cen

    per_eng = []
    for w, g, rg in zip(win, groups5, reg):
        t0, t1 = g[0]["pts_s"], g[-1]["pts_s"]
        dur = t1 - t0
        eff = dur + SAMPLE_DT                     # a kill event occupies a sample
        rec = dict(eng_id=w["eng_id"], regime=rg, pts_start=t0, pts_end=t1,
                   play_time_start=w["play_time_start"], dur_s=round(dur, 2),
                   eff_dur_s=round(eff, 2), n_events=len(g),
                   kills=sum(x["delta"] for x in g),
                   max_delta=max(x["delta"] for x in g),
                   n_multi_events=sum(1 for x in g if x["delta"] > 1))
        j = int(np.searchsorted(lvl_t, t0))
        rec["level"] = int(lvl_v[min(j, len(lvl_v) - 1)])
        for b in BURST_B:
            bs = bursts_of(g, b)
            active = sum((x[-1]["pts_s"] - x[0]["pts_s"]) + SAMPLE_DT
                         for x in bs)
            rec[f"n_bursts_b{b}"] = len(bs)
            rec[f"active_s_b{b}"] = round(active, 2)
            rec[f"travel_s_b{b}"] = round(eff - active, 2)
        for col, tag in (("werewolf1_skill02_charge", "charge"),
                         ("werewolf1_skill01_claws", "claws"),
                         ("defaultweaponattack", "wpn"),
                         ("onslaught", "onsl")):
            t, v = series[col]
            d_strict, s1 = anchored_delta(t, v, t0, t1)
            d_appr, s2 = anchored_delta(t, v, max(0.0, t0 - APPROACH_PAD), t1)
            rec[f"{tag}_strict"] = d_strict
            rec[f"{tag}_approach"] = d_appr
            rec[f"{tag}_slack_s"] = s2
        per_eng.append(rec)

    with open(os.path.join(outdir, "g2b-per-engagement.csv"), "w",
              newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(per_eng[0].keys()))
        wtr.writeheader()
        wtr.writerows(per_eng)

    def sel(rname):
        return [e for e in per_eng if e["regime"] == rname]

    # ---- D2 charge per engagement -----------------------------------------
    d2 = {}
    for rname in REGIMES:
        s = sel(rname)
        blk = {"n_engagements": len(s)}
        for tag in ("charge", "claws", "wpn", "onsl"):
            for mode in ("strict", "approach"):
                key = f"{tag}_{mode}"
                have = [e for e in s if e[key] is not None]
                cov = round(len(have) / len(s), 4) if s else 0.0
                if have:
                    d = [e[key] for e in have]
                    k = [e["kills"] for e in have]
                    p, lo, hi = boot_ratio(d, [1.0] * len(d))
                    pk, lok, hik = boot_ratio(d, k)
                    blk[key] = dict(
                        coverage=cov, n=len(have), total=int(sum(d)),
                        per_engagement=round(p, 3),
                        per_engagement_ci95=[round(lo, 3), round(hi, 3)],
                        per_kill=round(pk, 4),
                        per_kill_ci95=[round(lok, 4), round(hik, 4)],
                        median=float(np.median(d)),
                        frac_engagements_with_ge1=round(
                            float(np.mean([x >= 1 for x in d])), 3))
                else:
                    blk[key] = dict(coverage=cov, n=0)
        d2[rname] = blk
    # correlation: does charge track burst count within a regime?
    for rname in REGIMES:
        s = [e for e in sel(rname) if e["charge_approach"] is not None]
        if len(s) >= 8:
            c = np.array([e["charge_approach"] for e in s], float)
            nb = np.array([e[f"n_bursts_b{BURST_PRIMARY}"] for e in s], float)
            kk = np.array([e["kills"] for e in s], float)
            tv = np.array([e[f"travel_s_b{BURST_PRIMARY}"] for e in s], float)
            rho1 = stats.spearmanr(c, nb)
            rho2 = stats.spearmanr(c, kk)
            rho3 = stats.spearmanr(c, tv)
            d2[rname]["spearman"] = dict(
                charge_vs_bursts=[round(float(rho1.statistic), 3),
                                  float(rho1.pvalue)],
                charge_vs_kills=[round(float(rho2.statistic), 3),
                                 float(rho2.pvalue)],
                charge_vs_travel_s=[round(float(rho3.statistic), 3),
                                    float(rho3.pvalue)], n=len(s))
    out["d2_charge_per_engagement"] = d2

    # ---- D3 duration / rate ------------------------------------------------
    d3 = {}
    for rname in REGIMES:
        s = sel(rname)
        dur = np.array([e["dur_s"] for e in s], float)
        eff = np.array([e["eff_dur_s"] for e in s], float)
        k = np.array([e["kills"] for e in s], float)
        act = np.array([e[f"active_s_b{BURST_PRIMARY}"] for e in s], float)
        trav = np.array([e[f"travel_s_b{BURST_PRIMARY}"] for e in s], float)
        pr, lo, hi = boot_ratio(k, eff)
        pa, loa, hia = boot_ratio(k, act)
        d3[rname] = dict(
            n=len(s), kills=int(k.sum()),
            dur_median=float(np.median(dur)),
            dur_iqr=[float(np.percentile(dur, 25)),
                     float(np.percentile(dur, 75))],
            dur_mean=round(float(dur.mean()), 2), dur_max=float(dur.max()),
            eff_dur_total_s=round(float(eff.sum()), 1),
            kills_per_eff_second=round(pr, 4),
            kills_per_eff_second_ci95=[round(lo, 4), round(hi, 4)],
            active_s_total=round(float(act.sum()), 1),
            travel_s_total=round(float(trav.sum()), 1),
            travel_fraction_of_engagement_time=round(
                float(trav.sum() / eff.sum()), 4),
            kills_per_active_second=round(pa, 4),
            kills_per_active_second_ci95=[round(loa, 4), round(hia, 4)],
            spearman_dur_vs_kills=[
                round(float(stats.spearmanr(dur, k).statistic), 3),
                float(stats.spearmanr(dur, k).pvalue)])
    out["d3_duration_and_rate"] = d3

    # ---- D4 multi-kill fraction -------------------------------------------
    d4 = {}
    for rname in REGIMES:
        deltas = [e["delta"] for e, r in zip(ev, ev_reg) if r == rname]
        a = np.array(deltas, float)
        p, lo, hi = boot_ratio((a > 1).astype(float), np.ones(len(a)))
        d4[rname] = dict(
            n_kill_events=len(a), kills=int(a.sum()),
            frac_multi_kill=round(p, 4), frac_multi_kill_ci95=[round(lo, 4),
                                                               round(hi, 4)],
            mean_kills_per_event=round(float(a.mean()), 4),
            delta_histogram={str(int(x)): int((a == x).sum())
                             for x in sorted(set(a))},
            frac_ge_3=round(float((a >= 3).mean()), 4),
            frac_ge_4=round(float((a >= 4).mean()), 4))
    a_all = np.array([e["delta"] for e in ev], float)
    d4["RUN"] = dict(n_kill_events=len(a_all), kills=int(a_all.sum()),
                     frac_multi_kill=round(float((a_all > 1).mean()), 4),
                     mean_kills_per_event=round(float(a_all.mean()), 4))
    out["d4_multikill"] = d4

    # ---- ABC decomposition -------------------------------------------------
    abc = {}
    for b in BURST_B:
        blk = {}
        for rname in REGIMES:
            s = sel(rname)
            k = np.array([e["kills"] for e in s], float)
            nev = np.array([e["n_events"] for e in s], float)
            nb = np.array([e[f"n_bursts_b{b}"] for e in s], float)
            one = np.ones(len(s))
            A = boot_ratio(k, nev)
            B = boot_ratio(nev, nb)
            C = boot_ratio(nb, one)
            K = boot_ratio(k, one)
            blk[rname] = dict(
                n=len(s),
                A_kills_per_event=[round(x, 4) for x in A],
                B_events_per_burst=[round(x, 4) for x in B],
                C_bursts_per_engagement=[round(x, 4) for x in C],
                kills_per_engagement=[round(x, 4) for x in K],
                identity_check=round(A[0] * B[0] * C[0], 4))
        # log-share attribution of each pairwise climb
        for lo_r, hi_r in (("R1", "R2"), ("R2", "R3"), ("R1", "R3")):
            L = blk[lo_r]
            H = blk[hi_r]
            lg = {f: math.log(H[f][0] / L[f][0]) for f in
                  ("A_kills_per_event", "B_events_per_burst",
                   "C_bursts_per_engagement")}
            tot = sum(lg.values())
            share = {f: (round(v / tot, 4) if abs(tot) > 1e-12 else None)
                     for f, v in lg.items()}
            # bootstrap the shares
            sh_boot = {f: [] for f in lg}
            sL, sH = sel(lo_r), sel(hi_r)
            for _ in range(2000):
                iL = RNG.integers(0, len(sL), len(sL))
                iH = RNG.integers(0, len(sH), len(sH))
                def fac(S, idx):
                    k = sum(S[i]["kills"] for i in idx)
                    n = sum(S[i]["n_events"] for i in idx)
                    nb = sum(S[i][f"n_bursts_b{b}"] for i in idx)
                    return (k / n, n / nb, nb / len(idx))
                aL, bL, cL = fac(sL, iL)
                aH, bH, cH = fac(sH, iH)
                l = (math.log(aH / aL), math.log(bH / bL), math.log(cH / cL))
                t = sum(l)
                if abs(t) < 1e-9:
                    continue
                for f, v in zip(lg, l):
                    sh_boot[f].append(v / t)
            blk[f"climb_{lo_r}_to_{hi_r}"] = dict(
                total_ratio=round(H["kills_per_engagement"][0] /
                                  L["kills_per_engagement"][0], 4),
                log_terms={f: round(v, 4) for f, v in lg.items()},
                share_of_log_climb=share,
                share_ci95={f: [round(float(np.percentile(v, 2.5)), 3),
                                round(float(np.percentile(v, 97.5)), 3)]
                            for f, v in sh_boot.items()})
        abc[f"burst_b{b}"] = blk
    out["abc_decomposition"] = abc

    # ---- within-R2 proficiency probe (build held constant) -----------------
    s2 = sorted([e for e in sel("R2") if e["play_time_start"] is not None],
                key=lambda e: e["play_time_start"])
    q = np.array_split(np.arange(len(s2)), 4)
    quart = []
    for qi, idx in enumerate(q):
        ss = [s2[i] for i in idx]
        k = [e["kills"] for e in ss]
        nev = [e["n_events"] for e in ss]
        nb = [e[f"n_bursts_b{BURST_PRIMARY}"] for e in ss]
        ch = [e["charge_approach"] for e in ss if e["charge_approach"] is not None]
        quart.append(dict(
            quartile=qi + 1, n=len(ss),
            play_time_range=[ss[0]["play_time_start"],
                             ss[-1]["play_time_start"]],
            level_range=[min(e["level"] for e in ss),
                         max(e["level"] for e in ss)],
            kills=int(sum(k)),
            kills_per_engagement=round(sum(k) / len(ss), 3),
            A_kills_per_event=round(sum(k) / sum(nev), 4),
            B_events_per_burst=round(sum(nev) / sum(nb), 4),
            C_bursts_per_engagement=round(sum(nb) / len(ss), 4),
            charge_per_engagement=(round(sum(ch) / len(ch), 3) if ch else None),
            charge_coverage=round(len(ch) / len(ss), 3)))
    ptv = np.array([e["play_time_start"] for e in s2], float)
    kv = np.array([e["kills"] for e in s2], float)
    nbv = np.array([e[f"n_bursts_b{BURST_PRIMARY}"] for e in s2], float)
    av = np.array([e["kills"] / e["n_events"] for e in s2], float)
    out["within_R2_trend"] = dict(
        quartiles=quart,
        spearman_playtime_vs_kills_per_eng=[
            round(float(stats.spearmanr(ptv, kv).statistic), 3),
            float(stats.spearmanr(ptv, kv).pvalue)],
        spearman_playtime_vs_bursts=[
            round(float(stats.spearmanr(ptv, nbv).statistic), 3),
            float(stats.spearmanr(ptv, nbv).pvalue)],
        spearman_playtime_vs_A=[
            round(float(stats.spearmanr(ptv, av).statistic), 3),
            float(stats.spearmanr(ptv, av).pvalue)],
        n=len(s2))

    json.dump(out, open(os.path.join(outdir, "g2b-decomposition.json"), "w"),
              indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("gate0_reproduction", "series_census")},
                     indent=1))
    print("wrote", os.path.join(outdir, "g2b-decomposition.json"))


if __name__ == "__main__":
    main()
