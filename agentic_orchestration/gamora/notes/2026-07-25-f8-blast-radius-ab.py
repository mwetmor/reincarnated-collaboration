#!/usr/bin/env python3
"""F8 hard-CC consumer wiring — BLAST-RADIUS A/B driver.

THE QUESTION (dispatch 2026-07-25-gamora-f8-cc-consumer-wiring.md §2):
    Did historical balance verdicts for control kits depend on CC landing?
Answered EMPIRICALLY, not by inference: one control-oriented kit and one damage-baseline kit
(control arm) are driven through the production balance instrument PRE-wiring vs POST-wiring.
The delta IS the blast radius.

DESIGN (Disciplines #2, #3, #11):
  • SAME-BINARY ABLATION. The two arms differ ONLY by `spatial_engine.WIRE_HARD_CC` (False = the
    pre-wiring engine, byte-reproducing the G1-A audit's § 6 row; True = the wired engine).
    No git checkout ⇒ no checkout drift confound, and no possibility of a parallel regen of the
    same seed (Discipline #3): the arms run SEQUENTIALLY in one process.
  • SMOKE FIRST (Discipline #2): --smoke runs 2 kits × 2 encounters × 2 cohorts × 2 seeds.
    --full widens the encounter/seed frame. No full regen is required to answer the routed
    question; the instrument is per-cell, not a season re-derivation.
  • Kits are the REAL season-001 endgame population (`build_population`, the Gate-2-blessed
    boss-harness builder reused verbatim), NOT synthetic — a synthetic kit carries no CC and
    would answer nothing.
  • Instrument is `w4g2_tier_2_full_sim` (the tier-2 direct call the blessed boss/clear-room
    harnesses use), which routes to `run_spatial_fight` — the one live loop with 20 production
    importers (G1-A audit § 1).

READ-ONLY w.r.t. telemetry: no telemetry writer is passed; nothing is written to telemetry.db.

Author: gamora (simulation seam), 2026-07-25.
Run:  python3 2026-07-25-f8-blast-radius-ab.py --smoke
      python3 2026-07-25-f8-blast-radius-ab.py --full
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import logging
import os
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "reincarnated-engine"))
sys.path.insert(0, os.path.join(ENGINE_REPO, "src"))

# Disjoint seed namespace (Discipline #3 — distinct base from every prior run recorded in the
# harness lineage; the clear-room harness recorded a used span ending at 7,337,003 and asked
# later phases to base at >= 8,000,000).
F8_AB_SEED_BASE = 8_100_000

# The two kits are selected by POPULATION INDEX, not by legendary_id.
#
# WHY (a defect found in the first pass of this driver, recorded rather than quietly fixed):
# `build_population()` returns 66 CONFIGS collapsing to 30 legendary_id LABELS — 20 labels carry
# more than one config (the boss-harness docstring: "3 samples per cell share a legendary_id").
# Selecting a kit by legendary_id therefore picks an ARBITRARY sample. For this population that is
# not a cosmetic ambiguity: index 24 and index 27 share the label
# `endgame_bc_ranged_medium_variable_int_none_t4_chain_1` and differ in exactly the thing under
# test — 27 carries 4 chill effects, 24 carries none. A label-keyed pick silently ran the ZERO-CC
# sample as the "control kit" and produced a meaningless 16/16-identical first result.
#
# The resulting pair is close to ideal for the A/B: SAME BC cell, SAME legendary label, SAME t4
# chain, SAME cohort declaration and scope — differing in whether the sampled chain carries CC.
IDX_CONTROL = 27     # ...int_none_t4_chain_1, chill x4  (slow_percent 0.35, 3.0 s)
IDX_BASELINE = 24    # ...int_none_t4_chain_1, chill x0  — the damage-baseline control arm

CC_NAMES = frozenset({"stun", "freeze", "root", "chill", "silence"})

SMOKE_SHELLS = ("open_arena", "magic_pack")
FULL_SHELLS = ("open_arena", "chokepoint_corridor", "magic_pack", "elite_pack")
SMOKE_SEEDS = (0, 1)
FULL_SEEDS = (0, 1, 2, 3)


def _quiet():
    """Generation is chatty on stdout; the A/B numbers must not drown."""
    logging.disable(logging.CRITICAL)
    return contextlib.redirect_stdout(io.StringIO())


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", ENGINE_REPO, *args], capture_output=True, text=True)
    return r.stdout.strip()


# ---------------------------------------------------------------------------
# CC census — what CC does this population actually LAND? (Discipline #11)
# ---------------------------------------------------------------------------

def cc_census(pop) -> dict:
    """Per-config CC count, keyed by INDEX (labels are not unique — see IDX_CONTROL note)."""
    out = {}
    mags = {}
    for _i, p in enumerate(pop):
        pc = p["player_class"]
        n = 0
        for s in getattr(pc, "skills", []):
            for e in getattr(s, "effects", []) or []:
                nm = getattr(e, "name", None)
                if nm in CC_NAMES:
                    n += 1
                    mags.setdefault(nm, set()).add(
                        json.dumps(dict(getattr(e, "params", {}) or {}), sort_keys=True)
                    )
        out[_i] = {"legendary_id": p["legendary_id"], "cc_effects": n}
    return {"per_config": out, "magnitudes": {k: sorted(v) for k, v in mags.items()}}


# ---------------------------------------------------------------------------
# EXERCISE INSTRUMENTATION (Discipline #11: prove the mechanism was reached)
#
# A "no delta" result is only meaningful if the wired consumers were actually REACHED. These
# counters wrap the ailment applier and the two F8 consumer predicates and report, per arm:
#   • ailment application ATTEMPTS and LANDINGS by name (so we know what the population lands
#     at all, and specifically whether any CC lands);
#   • consumer observations — how many selector calls saw an action lock, how many nav calls saw
#     a movement lock or a live slow factor.
# All are pure observers: no RNG draw, no mutation. Installed around an arm and removed after.
# ---------------------------------------------------------------------------

_COUNTS: dict = {}


def _install_instrumentation():
    from reincarnated.simulation import damage_resolver as DR
    from reincarnated.simulation.spatial_gauntlet import spatial_engine as SE

    _COUNTS.clear()

    def bump(k):
        _COUNTS[k] = _COUNTS.get(k, 0) + 1

    _orig_ail = DR._try_apply_ailment

    def ail(name, effect, attacker, defender, rng, buff_dmg_mult=1.0, skill=None):
        bump("attempt:" + name)
        before = len(defender.active_effects)
        r = _orig_ail(name, effect, attacker, defender, rng, buff_dmg_mult, skill=skill)
        if len(defender.active_effects) > before:
            bump("landed:" + name)
        return r

    DR._try_apply_ailment = ail

    _orig_sel = SE._select_skill_for_entity

    def sel(entity, targets, elapsed, policy_config=SE._POLICY_BLIND_CONFIG):
        bump("select_calls")
        if SE._f8_action_locked(entity):
            bump("select_action_locked")
        return _orig_sel(entity, targets, elapsed, policy_config=policy_config)

    SE._select_skill_for_entity = sel

    _orig_nav = SE._navigate_entity

    def nav(entity, nav_target, arena, dt):
        bump("nav_calls")
        if SE._f8_move_locked(entity):
            bump("nav_move_locked")
        if SE._f8_slow_factor(entity) < 1.0:
            bump("nav_slowed")
        return _orig_nav(entity, nav_target, arena, dt)

    SE._navigate_entity = nav

    def restore():
        DR._try_apply_ailment = _orig_ail
        SE._select_skill_for_entity = _orig_sel
        SE._navigate_entity = _orig_nav

    return restore


# ---------------------------------------------------------------------------
# The cell runner
# ---------------------------------------------------------------------------

def run_cell(player_class, encounter, cohort, scope, seed):
    from reincarnated.simulation.t4_sim_cycling import w4g2_tier_2_full_sim
    batch, sg_result, in_band = w4g2_tier_2_full_sim(
        player_class=player_class,
        encounter=encounter,
        cohort=cohort,
        scope=scope or "character_wide",
        base_seed=seed,
    )
    fights = list(batch.fights)
    return {
        "n_fights": batch.n_fights,
        "wins": batch.wins,
        "survival_rate": round(batch.survival_rate, 6),
        "observed_kpm": round(batch.observed_kpm, 6),
        "mean_duration_s": round(statistics.fmean(f.duration_s for f in fights), 6),
        "mean_player_damage_dealt": round(
            statistics.fmean(f.player_damage_dealt for f in fights), 6),
        "mean_player_damage_taken": round(
            statistics.fmean(getattr(f, "player_damage_taken", 0.0) for f in fights), 6),
        "termination": {
            k: sum(1 for f in fights if f.termination_reason == k)
            for k in sorted({f.termination_reason for f in fights})
        },
    }


def run_arm(wire_hard_cc: bool, kits, encounters, cohorts, seeds) -> dict:
    from reincarnated.simulation.spatial_gauntlet import spatial_engine as SE
    SE.WIRE_HARD_CC = wire_hard_cc
    assert SE.WIRE_HARD_CC is wire_hard_cc
    restore = _install_instrumentation()

    cells = []
    for kit_label, entry in kits:
        pc = entry["player_class"]
        scope = entry.get("scope")
        for e_i, enc in enumerate(encounters):
            for c_i, cohort in enumerate(cohorts):
                for s_i, s in enumerate(seeds):
                    seed = F8_AB_SEED_BASE + e_i * 10_000 + c_i * 1_000 + s
                    with _quiet():
                        rec = run_cell(pc, enc, cohort, scope, seed)
                    rec.update({
                        "kit": kit_label,
                        "legendary_id": entry["legendary_id"],
                        "encounter_id": enc.encounter_id,
                        "shell": enc.scenario_shell_id,
                        "cohort": cohort,
                        "seed": seed,
                    })
                    cells.append(rec)
                    print(f"    [{'ON ' if wire_hard_cc else 'OFF'}] {kit_label:9s} "
                          f"{enc.scenario_shell_id:22s} {cohort:10s} seed={seed} "
                          f"surv={rec['survival_rate']:.4f} kpm={rec['observed_kpm']:.3f} "
                          f"dur={rec['mean_duration_s']:.2f} "
                          f"dmg={rec['mean_player_damage_dealt']:.1f}")
    exercise = dict(_COUNTS)
    restore()
    print(f"    exercise[{'ON' if wire_hard_cc else 'OFF'}]: "
          f"{json.dumps({k: v for k, v in sorted(exercise.items())})}")
    return {"wire_hard_cc": wire_hard_cc, "cells": cells, "exercise": exercise}


def _key(c):
    return (c["kit"], c["encounter_id"], c["cohort"], c["seed"])


def compare(pre: dict, post: dict) -> dict:
    pre_map = {_key(c): c for c in pre["cells"]}
    post_map = {_key(c): c for c in post["cells"]}
    assert set(pre_map) == set(post_map), "arm cell sets must be identical"

    METRICS = ["survival_rate", "observed_kpm", "mean_duration_s",
               "mean_player_damage_dealt", "mean_player_damage_taken"]
    per_cell = []
    identical = 0
    for k in sorted(pre_map):
        a, b = pre_map[k], post_map[k]
        d = {m: round(b[m] - a[m], 6) for m in METRICS}
        same = all(abs(v) < 1e-9 for v in d.values()) and a["termination"] == b["termination"]
        identical += int(same)
        per_cell.append({
            "cell": list(k), "kit": a["kit"], "shell": a["shell"],
            "pre": {m: a[m] for m in METRICS}, "post": {m: b[m] for m in METRICS},
            "delta": d, "byte_identical": same,
            "termination_pre": a["termination"], "termination_post": b["termination"],
        })

    by_kit = {}
    for kit in sorted({c["kit"] for c in per_cell}):
        rows = [c for c in per_cell if c["kit"] == kit]
        agg = {}
        for m in METRICS:
            pv = statistics.fmean(r["pre"][m] for r in rows)
            qv = statistics.fmean(r["post"][m] for r in rows)
            agg[m] = {
                "pre_mean": round(pv, 6), "post_mean": round(qv, 6),
                "abs_delta": round(qv - pv, 6),
                "rel_delta_pct": (round(100.0 * (qv - pv) / pv, 4) if abs(pv) > 1e-12 else None),
            }
        by_kit[kit] = {
            "n_cells": len(rows),
            "n_byte_identical": sum(1 for r in rows if r["byte_identical"]),
            "metrics": agg,
        }

    return {
        "n_cells": len(per_cell),
        "n_byte_identical": identical,
        "by_kit": by_kit,
        "per_cell": per_cell,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    mode = "full" if args.full else "smoke"
    shells = FULL_SHELLS if mode == "full" else SMOKE_SHELLS
    seeds = FULL_SEEDS if mode == "full" else SMOKE_SEEDS
    out_path = args.out or os.path.join(HERE, f"2026-07-25-f8-blast-radius-ab-{mode}.json")

    print(f"F8 blast-radius A/B — mode={mode}")
    print(f"  engine HEAD={_git('rev-parse', '--short', 'HEAD')}  "
          f"branch={_git('rev-parse', '--abbrev-ref', 'HEAD')}")

    with _quiet():
        from reincarnated.simulation.clean_boss_numbers_harness_2026_06_19 import build_population
        from reincarnated.generation.endgame_encounter_catalog import ENDGAME_ENCOUNTER_CATALOG
        pop, n_kits = build_population()

    census = cc_census(pop)
    cc_configs = {i: v for i, v in census["per_config"].items() if v["cc_effects"] > 0}
    print(f"  population: {len(pop)} configs from {n_kits} kits; "
          f"{len(cc_configs)} carry CC-bearing effects")
    print(f"  CC magnitudes landed by this population: "
          f"{json.dumps(census['magnitudes'], sort_keys=True)}")
    for i, v in sorted(cc_configs.items()):
        print(f"     idx {i:3d}  {v['legendary_id']}  cc={v['cc_effects']}")

    control_entry = pop[IDX_CONTROL]
    baseline_entry = pop[IDX_BASELINE]
    assert census["per_config"][IDX_CONTROL]["cc_effects"] > 0, "control kit must carry CC"
    assert census["per_config"][IDX_BASELINE]["cc_effects"] == 0, "baseline kit must carry none"
    print(f"  CONTROL kit : idx {IDX_CONTROL} {control_entry['legendary_id']} "
          f"(CC effects: {census['per_config'][IDX_CONTROL]['cc_effects']})")
    print(f"  BASELINE kit: idx {IDX_BASELINE} {baseline_entry['legendary_id']} "
          f"(CC effects: {census['per_config'][IDX_BASELINE]['cc_effects']})")

    encounters = [e for e in ENDGAME_ENCOUNTER_CATALOG if e.scenario_shell_id in shells]
    # Deterministic per-shell pick: the lexicographically-first encounter of each shell.
    picked = []
    for sh in shells:
        cand = sorted((e for e in encounters if e.scenario_shell_id == sh),
                      key=lambda e: e.encounter_id)
        if cand:
            picked.append(cand[0])
    encounters = picked
    cohorts = ["baseline", "geared"]
    from reincarnated.simulation.clean_boss_numbers_harness_2026_06_19 import ALL_COHORTS
    cohorts = [c for c in ALL_COHORTS][:2]

    kits = [("control", control_entry), ("baseline", baseline_entry)]
    print(f"  frame: {len(kits)} kits × {len(encounters)} encounters × {len(cohorts)} cohorts "
          f"× {len(seeds)} seeds = {len(kits)*len(encounters)*len(cohorts)*len(seeds)} cells/arm")
    print(f"  encounters: {[e.encounter_id for e in encounters]}")
    print(f"  cohorts:    {cohorts}")

    # ── SEQUENTIAL, same process. PRE first, then POST (Discipline #3).
    print("\n  ARM 1/2 — PRE-wiring (WIRE_HARD_CC=False; reproduces the audit § 6 engine)")
    pre = run_arm(False, kits, encounters, cohorts, seeds)
    print("\n  ARM 2/2 — POST-wiring (WIRE_HARD_CC=True)")
    post = run_arm(True, kits, encounters, cohorts, seeds)

    cmp_ = compare(pre, post)
    result = {
        "mode": mode,
        "engine_head": _git("rev-parse", "HEAD"),
        "seed_base": F8_AB_SEED_BASE,
        "cc_census": census,
        "control_kit": {"idx": IDX_CONTROL, "legendary_id": control_entry["legendary_id"]},
        "baseline_kit": {"idx": IDX_BASELINE, "legendary_id": baseline_entry["legendary_id"]},
        "encounters": [e.encounter_id for e in encounters],
        "cohorts": cohorts,
        "seeds": list(seeds),
        "pre": pre, "post": post, "comparison": cmp_,
        "exercise_pre": pre["exercise"], "exercise_post": post["exercise"],
    }
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1)

    print("\n  ── BLAST RADIUS ──")
    print(f"  cells per arm: {cmp_['n_cells']}   byte-identical pre-vs-post: "
          f"{cmp_['n_byte_identical']}/{cmp_['n_cells']}")
    for kit, agg in cmp_["by_kit"].items():
        print(f"  [{kit}] identical {agg['n_byte_identical']}/{agg['n_cells']}")
        for m, v in agg["metrics"].items():
            print(f"      {m:28s} pre={v['pre_mean']:12.4f} post={v['post_mean']:12.4f} "
                  f"Δ={v['abs_delta']:+12.4f} ({v['rel_delta_pct']}%)")
    print(f"\n  written: {out_path}")


if __name__ == "__main__":
    main()
