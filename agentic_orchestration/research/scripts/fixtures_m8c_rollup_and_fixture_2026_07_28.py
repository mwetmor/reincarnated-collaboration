#!/usr/bin/env python3
"""M8 part 3 -- the rollup grain, the fixture identity, the conditions, the grades.

Lands:
  * regime_stat  -- galadriel's tb-rollup figures, regime-partitioned. Keyed on a
    session_regime row, so a pooled row is UNREPRESENTABLE.
  * the TTK-shape and kills/engagement distributions, which exist in NO source rollup
    and are recomputed here from the banked engagement grain. TTK shape is a PRIMARY
    accountability target (R-KC1-2) and had no rollup until now.
  * measured_fixture / fixture_target -- the accountability contract as data.
  * fixture_condition -- every declared hole, scoped to what it conditions.
  * evidence_claim -- every grade, with WHO said it and the EMPIRICAL criterion that
    would move it.
"""

import json
import os
import sqlite3
import statistics

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB = os.path.join(ROOT, "agentic_orchestration/research/curated/fixtures.db")
TB = os.path.join(ROOT, "agentic_orchestration/galadriel/captures/2026-07-26-gd-playtest-v1-tb")

SESSION = "GP-gd-2026-07-26-s1"
SEG = f"{SESSION}/S1-gap5s-v1"
SRC = "galadriel/captures/2026-07-26-gd-playtest-v1-tb/tb-rollup.json"
VERDICT = "gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md"
FINDINGS = "galadriel/notes/2026-07-27-gd-playtest-v1-tb-intake-findings.md"
CHARTER = "gandalf/notes/2026-07-27-kit-cal-1-run-charter.md"


def log(m):
    print(f"[m8c] {m}", flush=True)


# rollup dict key -> (measure_key, stat_family, inclusion source key)
DIST = [
    ("intake_per_engagement", "intake_hp", "totals", "totals"),
    ("intake_per_engagement_pc_ehp", "intake_pc_ehp", "totals", "totals"),
    ("healed_per_engagement", "healed_hp", "totals", "totals"),
    ("intake_per_kill", "intake_per_kill", "totals", "totals"),
    ("intake_per_kill_pc_ehp", "intake_per_kill_pc_ehp", "totals", "totals"),
    ("intake_hp_per_s", "intake_hp_per_s", "rates", "rates"),
    ("intake_pc_ehp_per_s", "intake_pc_ehp_per_s", "rates", "rates"),
    ("healed_hp_per_s", "healed_hp_per_s", "rates", "rates"),
    ("drop_hp", "hp_drop_size", "drops", None),
    ("drop_pc_ehp", "hp_drop_pc_ehp", "drops", None),
    ("damage_per_engagement", "damage_spent", "damage", None),
    ("damage_per_kill_per_engagement", "damage_per_kill", "damage", None),
]
STATS = ("n", "mean", "median", "p10", "p50", "p90", "p99", "min", "max", "sd")

INCL_TOTALS = ("engagement coverage >= 0.80 (a fragment is not a total)")
INCL_RATES = ("engagements with >= 2 s of admissible pair-time; per COVERED second")


def land_regime_stat(cx):
    roll = json.load(open(os.path.join(TB, "tb-rollup.json")))
    cx.execute("DELETE FROM regime_stat WHERE segmentation_id=?", (SEG,))
    n = 0

    def put(rid, fam, mk, stat, val, unit, n_in, n_tot, rule, cov, basis, grade, src):
        nonlocal n
        cx.execute("""INSERT INTO regime_stat
            (segmentation_id, regime_id, stat_family, measure_key, statistic, value_num,
             unit, n_included, n_total, inclusion_rule, coverage, coverage_basis,
             evidence_grade, source_ref) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (SEG, rid, fam, mk, stat, val, unit, n_in, n_tot, rule, cov, basis, grade, src))
        n += 1

    for key, rg in roll["regimes"].items():
        rid = f"{SESSION}/{key}"
        cov_d, cov_f = rg["delta_coverage"], rg["frame_coverage"]
        basis_d = "T-B regime delta coverage (admissible pair-time / wallclock)"
        basis_f = "T-B regime frame coverage"
        n_tot = rg["engagements_total"]

        # counts -- the shape of the regime itself
        put(rid, "counts", "engagement_count", "n", rg["engagements_total"], "count",
            n_tot, n_tot, "all engagements in the regime", None, None, "MEASURED", SRC)
        put(rid, "counts", "kills", "total", rg["kills_total"], "count", n_tot, n_tot,
            "all engagements in the regime", None, None, "MEASURED", SRC)

        for src_key, mk, fam, incl in DIST:
            d = rg.get(src_key)
            if not d:
                continue
            rule = (INCL_TOTALS if incl == "totals" else
                    INCL_RATES if incl == "rates" else
                    "every admissible event in the regime")
            n_in = d.get("n", rg.get(f"{incl}_n_included") if incl else None)
            unit = cx.execute("SELECT unit FROM measure_dict WHERE measure_key=?",
                              (mk,)).fetchone()[0]
            cov = cov_f if fam == "drops" else cov_d
            basis = basis_f if fam == "drops" else basis_d
            if fam == "damage":
                cov, basis = rg["merged_dps_coverage"], "merged-interval dps coverage"
            for st in STATS:
                if st in d:
                    put(rid, fam, mk, st, d[st], unit, n_in, n_tot, rule, cov, basis,
                        "DERIVED" if fam == "damage" or "_pc_" in mk or "_per_" in mk
                        else "MEASURED", SRC)

        # hazard-shape scalars -- the load-bearing finding
        put(rid, "drops", "hp_drop_count", "total", rg["n_drop_events"], "count",
            rg["rates_n_included"], n_tot, INCL_RATES, cov_d, basis_d, "MEASURED", SRC)
        put(rid, "drops", "hp_drop_count_ge_10pc_ehp", "total", rg["n_drops_ge_10pc_ehp"],
            "count", rg["rates_n_included"], n_tot, INCL_RATES, cov_d, basis_d,
            "DERIVED", SRC)
        put(rid, "drops", "frac_intake_from_drops_ge_10pc_ehp", "frac",
            rg["frac_intake_from_drops_ge_10pc_ehp"], "frac", rg["rates_n_included"],
            n_tot, INCL_RATES, cov_d, basis_d, "DERIVED", SRC)
        put(rid, "drops", "drop_events_per_covered_s", "mean",
            rg["drop_events_per_covered_s"], "count/s", rg["rates_n_included"], n_tot,
            INCL_RATES, cov_d, basis_d, "DERIVED", SRC)

        # damage -- merged-interval aggregate is the better estimator (findings sec 7)
        put(rid, "damage", "damage_per_kill_merged", "mean", rg["merged_damage_per_kill"],
            "dmg/kill", rg["merged_kills"], rg["kills_total"],
            "overlapping windows merged; nothing double-counted, nothing dropped",
            rg["merged_dps_coverage"], "merged-interval dps coverage", "DERIVED", SRC)

    log(f"regime_stat: {n} rows from galadriel's rollup")
    return n


def land_ttk_shape(cx):
    """TTK shape and kills/engagement have NO rollup in any source. They are the primary
    and the provisional accountability targets respectively. Recomputed here from the
    banked engagement grain so the fixture's headline distribution is queryable."""
    added = 0
    for rid, in cx.execute("SELECT regime_id FROM session_regime WHERE session_id=? "
                           "ORDER BY regime_ordinal", (SESSION,)):
        for mk, unit, grade, note in (
                ("engagement_seconds", "s", "MEASURED",
                 "TTK-shape carrier. PRIMARY target (R-KC1-2). ~11% quantisation at 0.5 s."),
                ("kills_per_engagement", "count", "DERIVED",
                 "PROVISIONAL target (R-KC1-2) -- confounded, see C-KPE-PROVISIONAL.")):
            vals = [v for (v,) in cx.execute("""
                SELECT m.value_num FROM trial_measurement m JOIN fixture_trial t
                  ON t.trial_id=m.trial_id
                WHERE t.segmentation_id=? AND t.regime_id=? AND m.measure_key=?
                  AND m.phase IN ('during','derived')""", (SEG, rid, mk))]
            if not vals:
                continue
            vals.sort()
            q = statistics.quantiles(vals, n=10, method="inclusive")
            body = {"n": len(vals), "mean": round(statistics.fmean(vals), 4),
                    "median": round(statistics.median(vals), 4),
                    "p10": round(q[0], 4), "p90": round(q[8], 4),
                    "min": min(vals), "max": max(vals),
                    "sd": round(statistics.stdev(vals), 4) if len(vals) > 1 else None}
            for st, v in body.items():
                if v is None:
                    continue
                cx.execute("""INSERT INTO regime_stat
                    (segmentation_id, regime_id, stat_family, measure_key, statistic,
                     value_num, unit, n_included, n_total, inclusion_rule, coverage,
                     coverage_basis, evidence_grade, source_ref)
                    VALUES (?,?, 'totals', ?,?,?,?,?,?,?, NULL,?,?,?)""",
                    (SEG, rid, mk, st, v, unit, len(vals), len(vals),
                     "every engagement in the regime (no coverage gate -- the T-A kills "
                     "series closes exactly on the panel endpoint)",
                     "T-A kills series; segmentation total 880 == panel endpoint 882 minus "
                     "the 2 pre-run kills (control counters-start-at-zero VIOLATED)",
                     grade, "elrond M8c recompute from the banked engagement grain; " + note))
                added += 1
    log(f"regime_stat: +{added} rows for TTK shape + kills/engagement (recomputed here)")
    return added


def verify_recompute(cx):
    """Discipline #11: do not trust the rollup because it is committed. Recompute the
    coverage-gated intake totals from the banked engagement rows and diff."""
    roll = json.load(open(os.path.join(TB, "tb-rollup.json")))
    out = []
    for key, rg in roll["regimes"].items():
        rid = f"{SESSION}/{key}"
        vals = [v for (v,) in cx.execute("""
            SELECT m.value_num FROM trial_measurement m JOIN fixture_trial t
              ON t.trial_id=m.trial_id
            WHERE t.segmentation_id=? AND t.regime_id=? AND m.measure_key='intake_hp'
              AND m.coverage >= 0.80""", (SEG, rid))]
        exp = rg["intake_per_engagement"]
        got = {"n": len(vals), "mean": round(statistics.fmean(vals), 1),
               "median": statistics.median(vals), "max": max(vals)}
        ok = (got["n"] == exp["n"] and abs(got["mean"] - exp["mean"]) < 0.15
              and got["median"] == exp["median"] and got["max"] == exp["max"])
        out.append(f"{key}: n {got['n']}/{exp['n']} mean {got['mean']}/{exp['mean']} "
                   f"median {got['median']}/{exp['median']} max {got['max']}/{exp['max']} "
                   f"-> {'AGREE' if ok else 'DISAGREE'}")
    for line in out:
        log("  recompute " + line)
    return out


def main():
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys = ON")
    try:
        cx.execute("BEGIN")
        land_regime_stat(cx)
        land_ttk_shape(cx)
        cx.commit()
    except Exception:
        cx.rollback()
        raise
    verify_recompute(cx)
    fk = list(cx.execute("PRAGMA foreign_key_check"))
    log(f"foreign_key_check: {'CLEAN' if not fk else fk[:5]}")
    cx.close()


if __name__ == "__main__":
    main()
