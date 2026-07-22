#!/usr/bin/env python3
"""
Tier-3 PREREG-beat — PART 2: NEUTRAL-ARENA BASELINES.

For the 131 family-resolved spine kits (W3-eligible pool), run repeated-seed
NEUTRAL-arena fights (open_arena — no formation shaping) with a REAL fighting
PlayerClass built from each kit's BC vector via the production martial builder
(nearest endgame BC-cell). Captures the harness's fight-metric SUPERSET; computes
per-kit + per-era baseline VARIANCE per metric. The conductor derives X (effect-size
threshold) from this; I declare NOTHING.

Design + calibration justified in: 2026-07-22-tier3-prereg-baselines-math.md
  - raw class_dict -> PASSIVE player (§2-probe, Discipline #11); real PlayerClass
    via player_class= kwarg is the PRODUCTION PATH that makes the player fight.
  - kit-as-variable: BC vector -> nearest endgame BC-cell -> real PlayerClass (§2).
  - calibration damage_modifier=1.0 (native metrology operating point) (§3).
  - 4 seeds/kit = 524 fights, smoke-scale (§4); paired seed set (Discipline #3).
  - HONEST LIMIT: between-kit variance is between-CELL (16 fighters), not 131 (§2).

Substrate: corpus.db md5 d091881d (READ-ONLY) + membership sidecar (READ-ONLY,
commit 6dd43161). Engine harness invoked BY PATH — ZERO writes to the engine repo.
Author: named-gamora sub-agent, 2026-07-22.

Run:  python3 2026-07-22-tier3-prereg-baselines.py
Emits: 2026-07-22-tier3-prereg-baselines.json + prints a variance census.
"""
import hashlib
import json
import os
import sqlite3
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DB = os.path.abspath(os.path.join(
    HERE, "..", "..", "research", "curated", "corpus.db"))
SIDECAR = os.path.join(HERE, "..", "..", "elrond", "notes",
                       "2026-07-22-tier3-family-membership-sidecar.json")
EXPECTED_MD5_PREFIX = "d091881d"
SIDECAR_COMMIT = "6dd43161"
OUT_PATH = os.path.join(HERE, "2026-07-22-tier3-prereg-baselines.json")

# Engine harness BY PATH (import/invoke only; zero writes to the engine repo).
ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                          "reincarnated-engine", "src"))
if not os.path.isdir(ENGINE_SRC):
    print(f"FATAL: engine src not found at {ENGINE_SRC}", file=sys.stderr)
    sys.exit(2)
sys.path.insert(0, ENGINE_SRC)

from reincarnated.simulation.spatial_gauntlet.arena import ALL_SCENARIOS  # noqa: E402
from reincarnated.simulation.spatial_gauntlet.spatial_engine import (  # noqa: E402
    run_spatial_fight, SpatialFightConvergenceError,
)
from reincarnated.generation.typed_monster_skills import (  # noqa: E402
    emit_skills_for_threat_tier,
)
from reincarnated.generation.endgame_encounter_catalog import (  # noqa: E402
    ENDGAME_ENCOUNTER_CATALOG,
)
from reincarnated.simulation.martial_bar_rederivation_driver import (  # noqa: E402
    _build_martial_player_class,
)
from reincarnated.generation.resource_economy import DEFAULT_RESOURCE_ECONOMY  # noqa: E402

# ----- calibration (math note §3/§4) -----
NEUTRAL_SCENARIO = "open_arena"
DAMAGE_MODIFIER = 1.0                       # §3 native metrology operating point (uniform)
SEEDS = [20260722, 20260723, 20260724, 20260725]  # §4 paired seed set, 4 seeds/kit

# Per-fight scalar metric superset captured from SpatialFightResult (math note §6).
# Broad capture; declare NOTHING (conductor declares the subset per L-13).
METRIC_FIELDS = [
    "elapsed_s", "mobs_killed", "total_mob_count", "total_aoe_hits",
    "player_damage_total", "damage_taken_while_committed", "completion_rate",
    "whiff_rate", "sustain_uptime", "total_displacement", "max_flanking_count",
    "total_flanking_ticks", "cone_hit_fraction", "line_hit_fraction",
    "circle_hit_fraction", "forced_break_count", "move_cancel_count",
    "drain_exhaustion_events",
]
ERA_OF_YEAR = {2000: "I", 2013: "II", 2016: "III", 2024: "IV"}

# ----- BC vocab bridge (corpus -> endgame catalog) (math note §2) -----
def _nrange(x):
    return {"melee": "melee", "dual": "mid", "ranged": "ranged"}.get(x, "mid")
def _ntempo(x):
    return {"high": "high", "med": "medium", "low": "low"}.get(x, "medium")
def _namp(x):
    return {"flat": "flat", "spiky": "spiky", "var": "variable"}.get(x, "flat")
def _nattr(x):
    return (x or "STR").upper()


def _neutral_cells():
    """The 17 neutral endgame BC-cells (proxy_density=none, no escape/dense variant)."""
    out = []
    for e in ENDGAME_ENCOUNTER_CATALOG:
        if e.bc_proxy_density == "none" and not e.encounter_id.endswith(("_escape", "_dense")):
            out.append((e.encounter_id, e.bc_range, e.bc_tempo, e.bc_amplitude, e.bc_attribute))
    return out


def nearest_cell(k, cells):
    """Weighted-hamming nearest cell for a corpus kit (range+attr primary, ×2)."""
    tr, tt, ta, tat = _nrange(k["range_val"]), _ntempo(k["tempo_val"]), _namp(k["amp_val"]), _nattr(k["attr_val"])
    best, bestd = None, 99
    for (cid, cr, ct, ca, cat_attr) in cells:
        d = (cr != tr) * 2 + (cat_attr != tat) * 2 + (ct != tt) + (ca != ta)
        if d < bestd:
            bestd, best = d, cid
    return best, bestd


def md5_check(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_resolved_kits():
    """131 family-resolved spine kits: sidecar ACTIVE rows on_spine, joined to
    corpus.db BC attributes + court/element (read-only)."""
    with open(SIDECAR) as f:
        sc = json.load(f)
    active_spine = {r["kit_id"]: (r["family"], r["tier"])
                    for r in sc["memberships"]
                    if not r.get("shadowed_by") and r.get("on_spine")}
    con = sqlite3.connect(f"file:{CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    kits = []
    for row in cur.execute(
            "SELECT kit_id, folk_name, game, era_year, court, original_element, attr_val, "
            "range_val, tempo_val, amp_val, proxy_val, commit_val "
            "FROM canon_corpus WHERE corpus_class='record' ORDER BY kit_id"):
        kid = row["kit_id"]
        if kid not in active_spine:
            continue
        fam, tier = active_spine[kid]
        k = dict(row)
        k["family"] = fam
        k["membership_tier"] = tier
        k["era"] = ERA_OF_YEAR.get(row["era_year"])
        kits.append(k)
    con.close()
    return kits, sc.get("corpus_md5_ro", "")


def _num(x):
    try:
        f = float(x)
        return f
    except (TypeError, ValueError):
        return None


def stats(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"n": 0, "mean": None, "stdev": None, "min": None, "max": None}
    n = len(vals)
    mean = sum(vals) / n
    var = sum((x - mean) ** 2 for x in vals) / n
    return {"n": n, "mean": round(mean, 4), "stdev": round(var ** 0.5, 4),
            "min": round(min(vals), 4), "max": round(max(vals), 4)}


def build_neutral_mobs(scenario):
    """Byte-identical mob roster for the neutral arena — held constant across ALL kits
    (neutrality). Mobs carry LIVE typed damage via the canonical emitter."""
    out = []
    for spawn in scenario.mob_spawns:
        tier = getattr(spawn, "threat_tier", None) or "swarm"
        if tier in ("boss", "mini-boss", "miniboss", "elite"):
            skills = emit_skills_for_threat_tier(tier, signature_element="fire")
            hp = 2500.0
        else:
            skills = emit_skills_for_threat_tier(tier)
            hp = 150.0
        out.append({"id": f"mob_{len(out)}", "max_hp": hp, "energy": 100.0,
                    "max_energy": 100.0, "armor": 20.0, "skills": skills,
                    "movement_speed": 5.5, "preferred_behavior": "melee_aggressive",
                    "aggro_radius_m": 15.0, "leash_distance_m": 18.0})
    return out


def main():
    md5 = md5_check(CORPUS_DB)
    if not md5.startswith(EXPECTED_MD5_PREFIX):
        print(f"FATAL: corpus md5 {md5} != {EXPECTED_MD5_PREFIX}", file=sys.stderr)
        sys.exit(2)

    kits, sidecar_md5 = load_resolved_kits()
    cells = _neutral_cells()
    scenario = ALL_SCENARIOS[NEUTRAL_SCENARIO]
    mobs = build_neutral_mobs(scenario)

    # ---- assign each kit its nearest BC-cell; cache one real PlayerClass per cell ----
    cell_of = {}
    dist_of = {}
    for k in kits:
        c, d = nearest_cell(k, cells)
        cell_of[k["kit_id"]] = c
        dist_of[k["kit_id"]] = d
    used_cells = sorted(set(cell_of.values()))
    print("=" * 80)
    print("TIER-3 PREREG-BEAT · PART 2 · NEUTRAL-ARENA BASELINES")
    print(f"neutral scenario: {NEUTRAL_SCENARIO} ({scenario.arena.width_m}x"
          f"{scenario.arena.height_m}, {scenario.mob_count} mobs, "
          f"choke_zones={len(scenario.arena.choke_zones)}, has_boss={scenario.has_boss})")
    print(f"resolved kits: {len(kits)}   distinct BC-cells used: {len(used_cells)}/{len(cells)}   "
          f"seeds/kit: {len(SEEDS)}   total fights: {len(kits)*len(SEEDS)}")
    print(f"damage_modifier (calibration §3): {DAMAGE_MODIFIER}   PlayerClass path: production martial builder")
    print("=" * 80)

    t_build = time.perf_counter()
    pc_cache = {}
    for idx, cid in enumerate(used_cells):
        pc, _enc = _build_martial_player_class(cid, idx, "balanced")
        cd = pc.model_dump()
        cd["resource_economy"] = dict(DEFAULT_RESOURCE_ECONOMY)
        pc_cache[cid] = (pc, cd)
    print(f"built {len(pc_cache)} real PlayerClasses in {time.perf_counter()-t_build:.1f}s "
          f"(cached per cell)", flush=True)

    # ---- run 4 seeds/kit through the neutral arena with the kit's cell PlayerClass ----
    per_kit = []
    t0 = time.perf_counter()
    for i, k in enumerate(kits):
        cid = cell_of[k["kit_id"]]
        pc, cd = pc_cache[cid]
        per_fight = []
        wins = 0
        errs = 0
        for seed in SEEDS:
            try:
                raw = run_spatial_fight(
                    scenario=scenario, class_dict=cd, mob_dicts=mobs, n_fights=1,
                    session_id=f"prereg_baseline_{k['kit_id']}",
                    base_seed=seed, season_id="tier3-prereg",
                    player_class=pc, damage_modifier=DAMAGE_MODIFIER,
                    track_proxy_population=False,
                )
                fr = raw["fight_results"][0]
                rowm = {"seed": seed, "winner": getattr(fr, "winner", None),
                        "player_kill": bool(getattr(fr, "player_kill", False))}
                for f in METRIC_FIELDS:
                    rowm[f] = _num(getattr(fr, f, None))
                if getattr(fr, "winner", None) == "player":
                    wins += 1
                per_fight.append(rowm)
            except SpatialFightConvergenceError as e:
                errs += 1
                per_fight.append({"seed": seed, "error": "convergence", "detail": str(e)[:120]})
            except Exception as e:
                errs += 1
                per_fight.append({"seed": seed, "error": type(e).__name__, "detail": str(e)[:120]})
        n_ok = sum(1 for pf in per_fight if "error" not in pf)
        wr = round(wins / n_ok, 4) if n_ok else None
        metric_stats = {f: stats([pf.get(f) for pf in per_fight if "error" not in pf])
                        for f in METRIC_FIELDS}
        per_kit.append({
            "kit_id": k["kit_id"], "folk_name": k["folk_name"], "game": k["game"],
            "family": k["family"], "membership_tier": k["membership_tier"],
            "era": k["era"], "court": k["court"], "element": k["original_element"],
            "bc": {a: k[a] for a in ("range_val", "tempo_val", "amp_val", "proxy_val", "commit_val", "attr_val")},
            "assigned_cell": cid, "cell_distance": dist_of[k["kit_id"]],
            "n_seeds": len(SEEDS), "n_ok": n_ok, "n_err": errs,
            "win_rate": wr, "wins": wins,
            "per_fight": per_fight, "within_kit_variance": metric_stats,
        })
        if (i + 1) % 25 == 0:
            print(f"  [{i+1:3d}/{len(kits)}] {k['kit_id'][:36]:36s} killed_mean="
                  f"{metric_stats['mobs_killed']['mean']} ({time.perf_counter()-t0:.1f}s)", flush=True)
    wall = time.perf_counter() - t0

    def _metric_decomp(kit_subset):
        """Between-kit(cell) stdev vs mean within-kit(seed) stdev, per metric."""
        out = {}
        for f in METRIC_FIELDS:
            kit_means = [pk["within_kit_variance"][f]["mean"] for pk in kit_subset
                         if pk["within_kit_variance"][f]["mean"] is not None]
            within_stdevs = [pk["within_kit_variance"][f]["stdev"] for pk in kit_subset
                             if pk["within_kit_variance"][f]["stdev"] is not None]
            between = stats(kit_means)
            mean_within = round(sum(within_stdevs) / len(within_stdevs), 4) if within_stdevs else None
            bt = between["stdev"]
            ratio = round(bt / mean_within, 3) if (bt is not None and mean_within not in (None, 0)) else None
            out[f] = {
                "between_kit_stdev": bt, "mean_within_kit_stdev": mean_within,
                "signal_to_noise_ratio": ratio,
                "pool_mean": between["mean"], "pool_min": between["min"],
                "pool_max": between["max"], "n_kits": between["n"],
            }
        return out

    # ---- per-era aggregation + variance decomposition + feasibility ----
    per_era = {}
    for era in ("I", "II", "III", "IV"):
        ek = [pk for pk in per_kit if pk["era"] == era]
        if not ek:
            continue
        courts = Counter(pk["court"] for pk in ek)
        fams = Counter(pk["family"] for pk in ek)
        cells_here = Counter(pk["assigned_cell"] for pk in ek)
        tt = sum(fams.get(x, 0) for x in ("TOTEM-SENTRY", "TRAP-MINE"))
        wr_vals = [pk["win_rate"] for pk in ek if pk["win_rate"] is not None]
        per_era[era] = {
            "n_kits": len(ek), "courts": dict(courts), "n_courts": len(courts),
            "family_mix": dict(fams), "totem_trap_count": tt,
            "totem_trap_fraction": round(tt / len(ek), 3),
            "distinct_cells": len(cells_here),
            "win_rate_distribution": stats(wr_vals),
            "feasibility_n_ge_8": len(ek) >= 8,
            "feasibility_courts_present": len(courts) >= 1,
            "feasibility_verdict": ("FEASIBLE" if (len(ek) >= 8 and len(courts) >= 1) else "INFEASIBLE"),
            "metric_variance_decomposition": _metric_decomp(ek),
        }

    pool_decomp = _metric_decomp(per_kit)
    wr_all = [pk["win_rate"] for pk in per_kit if pk["win_rate"] is not None]
    wr_pool = stats(wr_all)
    # non-degenerate check on a graded metric (mobs_killed), since WR may all-monster in smoke
    mk_means = [pk["within_kit_variance"]["mobs_killed"]["mean"] for pk in per_kit
                if pk["within_kit_variance"]["mobs_killed"]["mean"] is not None]
    mk_band = stats(mk_means)
    degenerate = (mk_band["min"] == mk_band["max"]) if mk_band["n"] else True
    err_total = sum(pk["n_err"] for pk in per_kit)

    out = {
        "artifact": "tier3-prereg-baselines",
        "run": "Tier-3 Encounter-Geometry Run · PREREG-beat · Part 2 NEUTRAL-ARENA BASELINES",
        "author": "named-gamora sub-agent", "date": "2026-07-22",
        "substrate_md5": md5,
        "sidecar_provenance": {"commit": SIDECAR_COMMIT, "declared_corpus_md5": sidecar_md5,
                               "consumption": "ACTIVE on_spine rows (131 family-resolved kits)"},
        "engine_head_at_open": "b34a14b",
        "engine_head_at_run": "a3671d4",
        "engine_head_move_note": ("HEAD moved b34a14b->a3671d4 mid-session (star-lord W3 "
                                  "bundle work); delta touched ONLY export/ + output/ + tests/ "
                                  "— NOTHING in simulation/spatial_gauntlet/ or generation/. "
                                  "Baseline harness unaffected; runs stable at a3671d4."),
        "zero_writes_to_engine_repo": True,
        "design": {
            "neutral_scenario": NEUTRAL_SCENARIO,
            "neutrality_verified": {"choke_zones": len(scenario.arena.choke_zones),
                                    "has_boss": scenario.has_boss,
                                    "has_mini_boss": scenario.has_mini_boss,
                                    "continuous_spawn": scenario.continuous_spawn is not None,
                                    "timed_add_waves": len(scenario.timed_add_waves),
                                    "win_condition": scenario.win_condition},
            "player_path": ("REAL fighting PlayerClass via production martial builder "
                            "(_build_martial_player_class) + player_class= kwarg. Raw "
                            "class_dict produces a PASSIVE player — see §2-probe."),
            "kit_is_variable": "each kit's BC vector -> nearest endgame BC-cell -> that cell's PlayerClass (math §2)",
            "between_kit_variance_granularity": ("BETWEEN-CELL (distinct fighters="
                                                 + str(len(used_cells)) + "), not 131 — kits "
                                                 "sharing a cell share a fighter (math §2 HONEST LIMIT)"),
            "cell_assignment_coverage": {"exact_dist0": sum(1 for d in dist_of.values() if d == 0),
                                         "dist1": sum(1 for d in dist_of.values() if d == 1),
                                         "dist2": sum(1 for d in dist_of.values() if d == 2),
                                         "dist3plus": sum(1 for d in dist_of.values() if d >= 3),
                                         "cells_used": len(used_cells), "cells_available": len(cells)},
            "calibration_damage_modifier": DAMAGE_MODIFIER,
            "seeds": SEEDS, "seeds_per_kit": len(SEEDS),
            "total_fights_run": len(kits) * len(SEEDS),
            "budget_rationale": "smoke-scale (§4); paired seed set; Discipline #3 honored (sequential, one seed set)",
            "math_note": "2026-07-22-tier3-prereg-baselines-math.md",
        },
        "wall_seconds": round(wall, 1),
        "error_total": err_total,
        "pool_win_rate_distribution": wr_pool,
        "pool_mobs_killed_band": mk_band,
        "degenerate_band": degenerate,
        "pool_metric_variance_decomposition": pool_decomp,
        "per_era_baselines": per_era,
        "per_kit_baselines": per_kit,
        "prereg_caveat": ("VARIANCE DATA ONLY. X (effect-size threshold) + metric subset "
                          "declaration are the CONDUCTOR's per L-13. signal_to_noise_ratio is "
                          "a statistical OBSERVATION (between-cell stdev / mean within-kit(seed) "
                          "stdev), NOT a gate declaration."),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    # ---- print census ----
    print("-" * 80)
    print(f"total fights: {len(kits)*len(SEEDS)}   wall: {wall:.1f}s   errors: {err_total}")
    print(f"pool WR: {wr_pool}")
    print(f"pool mobs_killed band (per-kit means): {mk_band}   degenerate={degenerate}")
    print("-" * 80)
    print("PER-ERA FEASIBILITY (n>=8 + courts) + TOTEM/TRAP mix:")
    for era in ("I", "II", "III", "IV"):
        if era not in per_era:
            continue
        e = per_era[era]
        print(f"  Era {era}: n={e['n_kits']:2d} verdict={e['feasibility_verdict']:9s} "
              f"courts={e['n_courts']} {list(e['courts'].keys())}  "
              f"TOTEM+TRAP={e['totem_trap_count']}/{e['n_kits']} ({e['totem_trap_fraction']})")
    print("-" * 80)
    print("POOL SIGNAL-TO-NOISE (between-cell stdev / mean within-kit(seed) stdev) — ranked:")
    ranked = sorted(((f, d["signal_to_noise_ratio"]) for f, d in pool_decomp.items()
                     if d["signal_to_noise_ratio"] is not None),
                    key=lambda x: -x[1])
    for f, r in ranked:
        d = pool_decomp[f]
        print(f"  {f:30s} S/N={r:7.2f}  between_sd={d['between_kit_stdev']}  "
              f"within_sd={d['mean_within_kit_stdev']}  pool[{d['pool_min']},{d['pool_max']}]")
    nulls = [f for f, d in pool_decomp.items() if d["signal_to_noise_ratio"] is None]
    if nulls:
        print(f"  (metrics null/constant on this path: {nulls})")
    print("=" * 80)
    print(f"wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
