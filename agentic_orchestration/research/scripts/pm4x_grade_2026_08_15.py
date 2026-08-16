#!/usr/bin/env python3
"""KC2-PM4 · Lap X · THE GRADE.  Gated on re-hashing `pm4x_prediction.json` EXACT.

The prediction was emitted and hashed by `pm4x_decode_2026_08_15.py` BEFORE any quantity was
computed.  This instrument re-hashes it and HALTs on mismatch, so no grade can be produced against
a prediction that moved.  Referent numbers appear ONLY as the § 5 grade surface.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-15.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import statistics
import sys

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
OUT = META / "agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-x-mitigation-decode"

PRED_SHA = "1037207f410b5b33751d9c53880dd44d42c87470bfe70da85b6ae03d6bd07164"

#: the GRADE surface, quarantined (PREREGISTRATION.md § 5)
G = {"G-1_w151_duration_s": 16.0, "G-1_w151_terminal": "CLEARED",
     "G-2_mean_hp_fraction": 0.932, "G-2_full_health_dwell_s": 1.6166,
     "G-3_concurrent_living_w151": [19, 36], "G-4_implied_kill_rate_bodies_per_s": 28 / 16.0,
     "G-5_pool_hp": 20005.0, "G-5_regen_hp_per_s": 129.38,
     "G-6_w160_duration_s": 29.0, "G-6_w160_terminal": "DEATH"}

LAPL_MEDIAN_TICKS = 7.62          # Lap L § 7.1, physical-only, over the 790-record BAND
TICK_S_LO, TICK_S_HI = 0.087820, 0.081633


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    got = sha(OUT / "pm4x_prediction.json")
    if got != PRED_SHA:
        raise SystemExit(f"HALT — prediction digest moved.\n expected {PRED_SHA}\n got      {got}")
    pred = json.loads((OUT / "pm4x_prediction.json").read_text())
    board = json.loads((OUT / "pm4x_intake_board.json").read_text())
    defense = json.loads((OUT / "pm4x_player_defense.json").read_text())
    forms = json.loads((OUT / "pm4x_formulas.json").read_text())
    with (OUT / "pm4x_ttk_by_body.csv").open() as f:
        ttk = list(csv.DictReader(f))
    with (OUT / "pm4x_monster_resist_reduction.csv").open() as f:
        rr = list(csv.DictReader(f))

    b151 = board["151"]
    runrec = b151["board_per_round_HP"]["RUNREC"]["direct_perpiece"]
    grid = b151["per_second_at_declared_cadence_grid_RUNREC"]
    per_body = b151["per_body_RUNREC_perpiece"]["median"]

    # ── P-X-1 ────────────────────────────────────────────────────────────────────────────────
    lo, hi = pred["P-X-1a"]["lo"], pred["P-X-1a"]["hi"]
    inband = {k: (lo <= v <= hi) for k, v in grid.items()}
    p1a = "FAILED" if not any(inband.values()) else (
        "PASSED" if all(inband.values()) else "SPLIT-BY-CADENCE")
    p1b = "PASSED" if min(grid.values()) > pred["P-X-1b"]["threshold"] else "FAILED"
    thr = pred["P-X-1c"]["threshold"]
    p1c = "PASSED" if max(grid.values()) < thr else "FAILED"
    # the reported implication (referent used ONLY as a yardstick, never as an input)
    contact_for_1c = {c: thr * float(c[:-1]) / per_body for c in grid}

    # ── P-X-2 ────────────────────────────────────────────────────────────────────────────────
    def med(col):
        v = [float(r[col]) for r in ttk if r[col]]
        return statistics.median(v)
    m_phys_lo, m_full_lo = med("ticks_to_kill_physonly_LO"), med("ticks_to_kill_fullvector_LO")
    m_full_hi = med("ticks_to_kill_fullvector_HI")
    d_same_pop = 100.0 * (m_full_lo - m_phys_lo) / m_phys_lo
    d_vs_lapl = 100.0 * (m_full_lo - LAPL_MEDIAN_TICKS) / LAPL_MEDIAN_TICKS
    p2a = "PASSED" if abs(d_vs_lapl) < pred["P-X-2a"]["tolerance_pct"] else "FAILED"
    kill_lo = 1.0 / (m_full_lo * TICK_S_LO)
    kill_hi = 1.0 / (m_full_hi * TICK_S_HI)
    p2b = "PASSED" if kill_lo >= pred["P-X-2b"]["threshold_bodies_per_s"] else "FAILED"

    # ── P-X-3 ────────────────────────────────────────────────────────────────────────────────
    NAMED = {"defensiveBlock", "defensiveBlockChance", "blockAbsorption", "blockRecoveryTime"}
    fired = [r for r in defense["block_census"]["rows"] if r["field"] in NAMED]
    others = [r for r in defense["block_census"]["rows"] if r["field"] not in NAMED]
    p3a = "PASSED" if not fired else "FAILED"

    # ── P-X-4 ────────────────────────────────────────────────────────────────────────────────
    cf = forms["combatformulas.dbr"]["fields"]
    regions = {k: v for k, v in cf.items() if k.startswith("combatRegion")}
    p4a = "PASSED" if sum(float(v) for v in regions.values()) == 100.0 else "FAILED"
    a = defense["armour"]
    p4b = "PASSED" if a["winner"].startswith("M-SUM") else "FAILED"

    # ── P-X-5 ────────────────────────────────────────────────────────────────────────────────
    caps = defense["resist_caps"]["playerDefenseCap"]
    sheet = defense["sheet"]
    at_cap = [k for k in sheet if k.startswith("resist_") and sheet[k].isdigit()
              and float(sheet[k]) == float(caps[2])]
    p5a = "PASSED" if float(caps[2]) == 80.0 and len(at_cap) >= 8 else "FAILED"
    armour_eqs = [k for k in cf if "DefenseEquation" in k]
    p5b_typescope = "PASSED" if all("physcial" in k or "physical" in k for k in armour_eqs) else "FAILED"
    true_rr = [r for r in rr if "ResistanceReduction" in r["family"]]
    dmg_red = [r for r in rr if "DamageReduction" in r["family"]]
    p5c = "PASSED" if len(true_rr) >= pred["P-X-5c"]["threshold"] else "FAILED"

    # ── the ORDER fork, worked numerically on one real hit ───────────────────────────────────
    raw = 5000.0
    armour = float(sheet["armor_rating"])
    absorb = a["base_absorption_pct"]
    resp = float(sheet["resist_physical"])

    def arm(x, A, ab):
        return x * (1 - ab / 100.0) if x <= A else A * (1 - ab / 100.0) + (x - A)
    order_AR = arm(raw, armour, absorb) * (1 - resp / 100.0)
    order_RA = arm(raw * (1 - resp / 100.0), armour, absorb)

    grade = {
        "prediction_digest_reverified": got,
        "P-X-1a": {"grade": p1a, "band": [lo, hi], "per_second_grid": grid,
                   "in_band_by_cadence": inband,
                   "note": "graded under the prereg's OWN definition — ALL 28 bodies in contact. "
                           "The melee-contact count is NOT decoded by this lap "
                           "(UNREACHED-X-3); the board figure is linear in it."},
        "P-X-1b": {"grade": p1b, "threshold": pred["P-X-1b"]["threshold"],
                   "min_over_grid": min(grid.values())},
        "P-X-1c": {"grade": p1c, "threshold": thr, "max_over_grid": max(grid.values()),
                   "reported_implication_contact_count_that_satisfies_it": contact_for_1c,
                   "note": "the threshold is a REFERENT-DERIVED yardstick; it graded the "
                           "prediction and entered no decoded value"},
        "P-X-2a": {"grade": p2a, "median_ticks_physonly_LO": m_phys_lo,
                   "median_ticks_fullvector_LO": m_full_lo,
                   "delta_pct_same_population": d_same_pop,
                   "delta_pct_vs_LapL_band_median_7.62": d_vs_lapl,
                   "population_caveat": "Lap L's 7.62 is the median over the 790-record BAND; "
                                        "this lap's is over the 13 records actually ROLLED at "
                                        "w151. The same-population delta is the clean number."},
        "P-X-2b": {"grade": p2b, "kill_rate_bodies_per_s_LO": kill_lo,
                   "kill_rate_bodies_per_s_HI": kill_hi,
                   "threshold": pred["P-X-2b"]["threshold_bodies_per_s"],
                   "note": "solo, one body in the disc; the disc is uncapped so k bodies in the "
                           "ring die in the same window (Lap L § 7)."},
        "P-X-3a": {"grade": p3a, "named_falsifier_fields_fired": fired,
                   "other_block_family_fields_present": others,
                   "camera_anchor": {"chance_to_block": sheet.get("chance_to_block"),
                                     "damage_blocked": sheet.get("damage_blocked"),
                                     "block_recovery": sheet.get("block_recovery")},
                   "prereg_sighted": True},
        "P-X-4a": {"grade": p4a, "regions": regions, "sum": sum(float(v) for v in regions.values())},
        "P-X-4b": {"grade": p4b, "bet": "SUM", "winner": a["winner"],
                   "models": a["models"], "sheet_armor_rating": a["sheet_armor_rating"],
                   "residual": a["winner_residual"], "residual_pct": a["winner_residual_pct"]},
        "P-X-5a": {"grade": p5a, "playerDefenseCap": caps,
                   "monsterDefenseCap": defense["resist_caps"]["monsterDefenseCap"],
                   "sheet_rows_at_cap": at_cap},
        "P-X-5b": {"grade_type_scope": p5b_typescope, "armour_equations": armour_eqs,
                   "grade_order": "UNREACHED",
                   "order_fork_worked_example": {
                       "raw_physical": raw, "aggregate_armour": armour,
                       "absorption_pct": absorb, "player_res_physical_pct": resp,
                       "ARMOUR_then_RESIST": order_AR, "RESIST_then_ARMOUR": order_RA,
                       "delta": order_AR - order_RA,
                       "note": "no record field expresses the order. BOTH limbs published "
                               "(R-PM4-27 part 3); the fold must carry both."}},
        "P-X-5c": {"grade": p5c, "n_true_resistance_reduction_rows": len(true_rr),
                   "n_damage_reduction_rows_found_instead": len(dmg_red),
                   "damage_reduction_rows": dmg_red,
                   "note": "the directional bet LOST. The 151/160 roster carries ZERO "
                           "`offensive*ResistanceReduction*`. What it does carry is one "
                           "`offensiveTotalDamageReductionPercent` = 50 for 5 s on the w160 "
                           "Korvaak Tomb Guardian — a term on the KILL-RATE side, not the "
                           "intake side."},
        "grade_surface": G,
        "w160_positive_control": {
            "board_per_round_RUNREC_HP": board["160"]["board_per_round_HP"]["RUNREC"]["direct_perpiece"],
            "rounds_to_empty_pool": board["160"]["rounds_to_empty_20005_pool_RUNREC"],
            "per_second_grid": board["160"]["per_second_at_declared_cadence_grid_RUNREC"],
            "referent_w160_duration_s": G["G-6_w160_duration_s"],
            "reading": "5 bodies, 6.39 rounds to empty a 20,005 pool with no sustain at all. "
                       "Reported as a scale check on the pipeline, NOT as a fit: no referent "
                       "number entered the computation."},
    }
    p = OUT / "pm4x_grade.json"
    p.write_text(json.dumps(grade, indent=1, sort_keys=True, default=str))
    print(json.dumps({k: (v.get("grade") or v.get("grade_order"))
                      for k, v in grade.items() if isinstance(v, dict) and
                      ("grade" in v or "grade_order" in v)}, indent=1))
    print("pm4x_grade.json", sha(p))


if __name__ == "__main__":
    main()
