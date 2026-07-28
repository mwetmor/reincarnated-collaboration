#!/usr/bin/env python3
"""T-B step 3 -- regime-partitioned rollup (G-1 intake) + G-2 damage derivation.

NEVER POOLED. Verdict SS3: kills/engagement runs 3.3 -> 8.4 -> 11.9 across
R1/R2/R3 because pack size rides build power, so any statistic pooled across
the three describes a run that never happened. Every number below is emitted
per regime, on the SS2-corrected boundaries: R1 358-1134, R2 1134-6052,
R3 6052-7094 on `play_time` (build break 1134 NOT 1757; DoT boundary 6052 NOT
6816).

COVERAGE GATES (declared, not silent)
  Two families are reported side by side and never mixed:
    * TOTALS  -- per-engagement intake totals, restricted to engagements whose
      frame coverage >= COV_GATE. A total from a half-read engagement is not a
      total, it is a fragment; including it would bias every mean downward.
    * RATES   -- intake per COVERED second, over every engagement with at
      least MIN_COVERED_S of admissible delta time. A rate is defensible under
      partial coverage in a way a total is not.
  n_included / n_total is printed for both. Nothing is interpolated.

EHP NORMALISATION
  Max HP moves 250 -> 1734 over the run (levelling + gear + werewolf form), so
  absolute HP is not comparable across regimes. Each engagement is also scored
  in units of its own observed max HP (`hp_max_seen`), which is a LOWER BOUND
  on true max HP -- if the player never touched full HP in the window the
  denominator is under-stated and the EHP fraction is over-stated. Windows
  where the observed max is not corroborated by the full "cur/max" read are
  flagged.

G-2 -- DAMAGE SPENT (monster-EHP UPPER BOUND)
  GD's panel `dps` is a TRAILING ROLLING MEAN. Its kernel width was MEASURED,
  not assumed: over 22 clean falling edges in the T-A ledger the field decays
  to zero in 5.0 s (p50; p90 6.5; max 7.5). Total damage over an engagement is
  therefore the integral of dps from the engagement start to end+K, which
  recovers the underlying damage integral for engagements long against K.
  Engagements shorter than DMG_MIN_DUR are EXCLUDED, per the standing kernel
  caveat. The resulting damage-per-kill is an UPPER BOUND on monster EHP: it
  is inflated by overkill, by damage to monsters killed outside the window,
  and by any damage that misses.
"""
import argparse
import csv
import json
import math
import statistics as st

COV_GATE = 0.80
MIN_COVERED_S = 2.0
DMG_K_S = 5.0            # MEASURED trailing-kernel width
DMG_MIN_DUR = 12.0       # >= 2x kernel; the "engagements >> 6 s" caveat
REGIMES = ("R1", "R2", "R3")


def q(v, p):
    if not v:
        return None
    s = sorted(v)
    i = min(len(s) - 1, max(0, int(math.ceil(p * len(s))) - 1))
    return s[i]


def load_dps(path):
    out = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            d = r["dps"]
            out.append((float(r["pts_s"]),
                        float(d) if d not in ("", "None") else None))
    return out


def integrate_dps(series, a, b):
    """Trapezoid over [a,b] on the 0.5 s grid. Returns (damage, coverage)."""
    seg = [(t, v) for t, v in series if a - 1e-6 <= t <= b + 1e-6]
    if len(seg) < 2:
        return None, 0.0
    have = [x for x in seg if x[1] is not None]
    cov = len(have) / len(seg)
    tot = 0.0
    for (t0, v0), (t1, v1) in zip(seg, seg[1:]):
        if v0 is None or v1 is None:
            continue
        tot += 0.5 * (v0 + v1) * (t1 - t0)
    return tot, cov


def summarise(vals):
    if not vals:
        return None
    return dict(n=len(vals), mean=round(st.mean(vals), 1),
                median=round(st.median(vals), 1),
                p10=round(q(vals, .10), 1), p90=round(q(vals, .90), 1),
                min=round(min(vals), 1), max=round(max(vals), 1),
                sd=round(st.stdev(vals), 1) if len(vals) > 1 else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intake", required=True)
    ap.add_argument("--ta-csv", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    W = json.load(open(args.intake))["windows"]
    dps = load_dps(args.ta_csv)

    for w in W:
        d, c = integrate_dps(dps, w["pts_start"], w["pts_end"] + DMG_K_S)
        w["damage_spent"] = None if d is None else round(d, 1)
        w["damage_dps_coverage"] = round(c, 3)
        for k, kk in ((6.0, "damage_spent_k6"), (7.5, "damage_spent_k75")):
            d2, _ = integrate_dps(dps, w["pts_start"], w["pts_end"] + k)
            w[kk] = None if d2 is None else round(d2, 1)

    out = dict(
        source_intake=args.intake, source_ta=args.ta_csv,
        coverage_gate=COV_GATE, min_covered_s=MIN_COVERED_S,
        dps_kernel_s_measured=DMG_K_S, dmg_min_engagement_s=DMG_MIN_DUR,
        regimes={})

    for R in REGIMES:
        g = [w for w in W if w["regime"] == R]
        nf = sum(w["n_frames_decoded"] for w in g)
        nok = sum(w["n_ok"] for w in g)
        gated = [w for w in g if w["coverage"] >= COV_GATE]
        rated = [w for w in g if w["delta_covered_s"] >= MIN_COVERED_S]

        # --- hazard shape: every admissible drop in the regime -------------
        drops, drops_pc = [], []
        for w in g:
            mx = w["hp_max_seen"] or 0
            for d in w["drops"]:
                drops.append(d)
                if mx:
                    drops_pc.append(100.0 * d / mx)
        big = [d for d in drops_pc if d >= 10.0]

        # G-2 gating rides on `dps` coverage, NOT on globe coverage: damage
        # spent and damage taken are read from different instruments and one
        # instrument's refusals must not silently gate the other's sample.
        dmg = [w for w in g
               if w["dur_s"] >= DMG_MIN_DUR and w["damage_spent"] is not None
               and w["damage_dps_coverage"] >= 0.95]

        # REGIME AGGREGATE over MERGED intervals. The kernel caveat is an
        # ATTRIBUTION caveat -- a 4.5 s engagement's damage integral leaks
        # into its neighbour's. Merging overlapping [start, end+K] intervals
        # removes the attribution problem entirely (nothing is double-counted,
        # nothing is dropped), so the regime-level damage-per-kill is valid
        # over ALL engagements, not just the long ones. Reported alongside the
        # long-engagement-only figure so the two can be compared.
        iv = sorted((w["pts_start"], w["pts_end"] + DMG_K_S, w["kills"])
                    for w in g)
        merged = []
        for a, b, k in iv:
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
                merged[-1][2] += k
            else:
                merged.append([a, b, k])
        mtot, mk, mcov, mn = 0.0, 0, [], 0
        for a, b, k in merged:
            d, c = integrate_dps(dps, a, b)
            if d is None or c < 0.95:
                continue
            mtot += d
            mk += k
            mcov.append(c)
            mn += 1

        out["regimes"][R] = dict(
            engagements_total=len(g),
            kills_total=sum(w["kills"] for w in g),
            frames=nf, frames_ok=nok,
            frame_coverage=round(nok / nf, 4) if nf else None,
            delta_coverage=round(
                sum(w["delta_covered_s"] for w in g)
                / sum(w["cap_dur"] for w in g), 4) if g else None,
            greedy_path_frames=sum(w["n_greedy_path"] for w in g),
            trunc_refusals=sum(w["n_trunc_demoted"] for w in g),
            spike_refusals=sum(w["n_ocrspike_demoted"] for w in g),
            unreadable_break_s=round(
                sum(w["unreadable_break_s"] for w in g), 1),
            max_hp_range=[min([w["hp_max_seen"] for w in g
                               if w["hp_max_seen"]] or [None]),
                          max([w["hp_max_seen"] for w in g
                               if w["hp_max_seen"]] or [None])],
            zero_coverage_engagements=[w["eng_id"] for w in g
                                       if w["coverage"] == 0.0],

            # ---- TOTALS (coverage-gated) ----
            totals_n_included=len(gated), totals_n_total=len(g),
            totals_kills=sum(w["kills"] for w in gated),
            intake_per_engagement=summarise([w["intake_hp"] for w in gated]),
            intake_per_engagement_pc_ehp=summarise(
                [100.0 * w["intake_hp"] / w["hp_max_seen"]
                 for w in gated if w["hp_max_seen"]]),
            healed_per_engagement=summarise([w["healed_hp"] for w in gated]),
            intake_per_kill=summarise(
                [w["intake_hp"] / w["kills"] for w in gated if w["kills"]]),
            intake_per_kill_pc_ehp=summarise(
                [100.0 * w["intake_hp"] / w["kills"] / w["hp_max_seen"]
                 for w in gated if w["kills"] and w["hp_max_seen"]]),

            # ---- RATES (coverage-normalised) ----
            rates_n_included=len(rated),
            intake_hp_per_s=summarise(
                [w["intake_hp"] / w["delta_covered_s"] for w in rated]),
            intake_pc_ehp_per_s=summarise(
                [100.0 * w["intake_hp"] / w["delta_covered_s"] / w["hp_max_seen"]
                 for w in rated if w["hp_max_seen"]]),
            healed_hp_per_s=summarise(
                [w["healed_hp"] / w["delta_covered_s"] for w in rated]),

            # ---- HAZARD SHAPE ----
            n_drop_events=len(drops),
            drop_hp=summarise([float(d) for d in drops]),
            drop_pc_ehp=dict(
                p50=round(q(drops_pc, .5), 2) if drops_pc else None,
                p90=round(q(drops_pc, .9), 2) if drops_pc else None,
                p99=round(q(drops_pc, .99), 2) if drops_pc else None,
                max=round(max(drops_pc), 2) if drops_pc else None),
            frac_intake_from_drops_ge_10pc_ehp=round(
                sum(big) / sum(drops_pc), 4) if drops_pc else None,
            n_drops_ge_10pc_ehp=len(big),
            drop_events_per_covered_s=round(
                len(drops) / sum(w["delta_covered_s"] for w in g), 3)
            if sum(w["delta_covered_s"] for w in g) else None,

            # ---- G-2 DAMAGE SPENT ----
            damage_n_included=len(dmg), damage_n_eligible=len(
                [w for w in g if w["dur_s"] >= DMG_MIN_DUR]),
            damage_per_engagement=summarise(
                [w["damage_spent"] for w in dmg]),
            damage_spent_total=round(sum(w["damage_spent"] for w in dmg), 1),
            damage_kills_total=sum(w["kills"] for w in dmg),
            mean_damage_per_kill=round(
                sum(w["damage_spent"] for w in dmg)
                / sum(w["kills"] for w in dmg), 1)
            if sum(w["kills"] for w in dmg) else None,
            mean_damage_per_kill_k6=round(
                sum(w["damage_spent_k6"] for w in dmg)
                / sum(w["kills"] for w in dmg), 1)
            if sum(w["kills"] for w in dmg) else None,
            mean_damage_per_kill_k75=round(
                sum(w["damage_spent_k75"] for w in dmg)
                / sum(w["kills"] for w in dmg), 1)
            if sum(w["kills"] for w in dmg) else None,
            damage_per_kill_per_engagement=summarise(
                [w["damage_spent"] / w["kills"] for w in dmg if w["kills"]]),
            merged_intervals_total=len(merged),
            merged_intervals_used=mn,
            merged_kills=mk,
            merged_damage_total=round(mtot, 1),
            merged_dps_coverage=round(sum(mcov) / len(mcov), 4) if mcov else None,
            merged_damage_per_kill=round(mtot / mk, 1) if mk else None,
        )

    out["windows"] = [{k: v for k, v in w.items() if k != "drops"} for w in W]
    json.dump(out, open(args.out, "w"), indent=1)

    # per-engagement CSV for elrond ingestion (G-3). Regime-partitioned by
    # column; coverage rides with every row so no consumer can read a value
    # without reading how much of it was measured.
    cols = ["eng_id", "regime", "play_time_start", "play_time_end",
            "pts_start", "pts_end", "dur_s", "kills", "coverage",
            "delta_coverage", "delta_covered_s", "n_frames_decoded", "n_ok",
            "n_greedy_path", "n_trunc_demoted", "n_ocrspike_demoted",
            "unreadable_break_s", "hp_max_seen", "hp_min", "intake_hp",
            "healed_hp", "n_drops", "drop_p50", "drop_max",
            "damage_spent", "damage_dps_coverage"]
    with open(args.out.replace(".json", "-engagements.csv"), "w",
              newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(cols)
        for w in W:
            wr.writerow([w.get(c) for c in cols])
    for R in REGIMES:
        r = out["regimes"][R]
        print("%s  eng=%d kills=%d framecov=%.3f | TOTALS n=%d intake mean=%s "
              "med=%s (%.1f%%EHP mean) | RATE %s HP/s | drops p50=%s p90=%s "
              "max=%s HP | DMG n=%d perkill=%s" % (
                  R, r["engagements_total"], r["kills_total"],
                  r["frame_coverage"], r["totals_n_included"],
                  r["intake_per_engagement"]["mean"],
                  r["intake_per_engagement"]["median"],
                  r["intake_per_engagement_pc_ehp"]["mean"],
                  r["intake_hp_per_s"]["mean"],
                  r["drop_hp"]["median"], r["drop_hp"]["p90"],
                  r["drop_hp"]["max"], r["damage_n_included"],
                  r["mean_damage_per_kill"]))
        print("     merged-interval aggregate: %d/%d intervals, %d kills, "
              "damage/kill = %s (dps cov %.3f)" % (
                  r["merged_intervals_used"], r["merged_intervals_total"],
                  r["merged_kills"], r["merged_damage_per_kill"],
                  r["merged_dps_coverage"] or 0))


if __name__ == "__main__":
    main()
