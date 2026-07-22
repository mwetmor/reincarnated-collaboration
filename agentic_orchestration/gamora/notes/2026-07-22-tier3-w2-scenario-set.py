#!/usr/bin/env python3
"""
Tier-3 W2 — Phase (c) MESO/MICRO sim scenario set (RUNS in the LIVE harness).

WAVE W2 of the Tier-3 Encounter-Geometry Run (conductor: gandalf RUN-CONDUCTOR).
Builds the scenario set that renders the W1 §3.3 formation catalogue in the LIVE
spatial-gauntlet harness (engine HEAD a57ee1f), invoked BY PATH from the
collaboration repo. NO writes to the engine repo (T3-V7 namespace law).

Two jobs (charter Phase c):
  1. The PROBE-4 (§7 strain formations) where expressible — carrying the Phase-(a)
     verdicts as the caveat.
  2. Representative coverage of the §3.3 catalogue (11 families) mapped onto the
     registered arena scenarios (which sim-capacity §A3 verified express
     swarm/volley/lane/emplacement/horde). Holes stay holes.

Records per scenario: ran-clean / ran-with-caveat / could-not-run + why.

Author: named-gamora sub-agent, 2026-07-22.
Run:  python3 2026-07-22-tier3-w2-scenario-set.py
Emits: 2026-07-22-tier3-w2-scenario-run-record.json + prints a run record.
"""
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "2026-07-22-tier3-w2-scenario-run-record.json")

# Invoke the engine harness BY PATH (read/import only; zero writes to the engine repo).
ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                          "reincarnated-engine", "src"))
if not os.path.isdir(ENGINE_SRC):
    print(f"FATAL: engine src not found at {ENGINE_SRC}", file=sys.stderr)
    sys.exit(2)
sys.path.insert(0, ENGINE_SRC)

from reincarnated.simulation.spatial_gauntlet.arena import ALL_SCENARIOS  # noqa: E402
from reincarnated.simulation.spatial_gauntlet.spatial_engine import (  # noqa: E402
    run_spatial_fight,
    SpatialFightConvergenceError,
)
from reincarnated.generation.typed_monster_skills import (  # noqa: E402
    emit_skills_for_threat_tier,
)


# ---------------------------------------------------------------------------
# PROBE-4 verdicts (Phase a — established empirically at HEAD a57ee1f). These
# ride the scenario record as the strain-formation expressiveness caveat.
# ---------------------------------------------------------------------------
PROBE_VERDICTS = {
    "cbn_corridor_arc": {
        "verdict": "PARTIAL",
        "missing_capability": (
            "no projectile wall-reflection/bounce physics. Corridor geometry EXISTS "
            "(SCENARIO_CHOKEPOINT 10x50, 5m bottleneck at y=[23,27]) and beam/bolt are "
            "'line' geometry, but walls are POSITIONAL bounds only (CHOKEPOINT_Y_MIN/MAX "
            "gate target-inclusion, spatial_engine.py:3036/3122) — no LOS/occlusion, no "
            "ricochet. Chains are capped depth-0/1 ('unbounded chains degenerate + "
            "un-simulatable', spatial_engine.py:460); the 15 'reflect' hits are thorns "
            "damage-reflection, NOT geometric bounce. The corridor + line-pressure is "
            "expressible; the WALL-BOUNCE amplification is not."),
        "scenario_proxy": "chokepoint_corridor",
    },
    "cb_crossfire": {
        "verdict": "PARTIAL",
        "missing_capability": (
            "no first-class paired-emitter cross-tracking construct. Single-channeler "
            "beam-lanes ARE expressible (tick_tracking=='tracking' re-resolves against "
            "live positions, spatial_engine.py:3116; 'line' geometry). Crossfire is "
            "COMPOSABLE as two independent stationary_caster channelers at opposite ends, "
            "but there is no explicit paired-emitter positional-tracking primitive that "
            "models the beam-CROSS geometry (the forced-reposition zone where two tracked "
            "beams intersect). Expressible-by-composition, not as a native construct."),
        "scenario_proxy": "boss_with_adds",
    },
    "ts_environmental_nest": {
        "verdict": "PARTIAL",
        "missing_capability": (
            "spawner is a fixed-window GLOBAL injector, not a killable terrain-anchored "
            "entity. ContinuousSpawnSpec (arena.py:230) clones the scenario's LAST mob "
            "and injects in a rectangular band subject to engaged_cap=50 — there is NO "
            "source-entity whose DEATH stops spawning (no spawn_source/emitter-alive "
            "gate). An EMPLACEMENT grid of held emitters exists (arena.py:1343) and "
            "continuous spawning exists, but the 'destroy-the-egg-sac-to-halt-the-burst' "
            "mechanic (the environmental-nest's defining verb) is absent. Streaming-nest "
            "pressure is expressible; the killable-anchor is not."),
        "scenario_proxy": "escape_lane",
    },
    "ss_phase_transform": {
        "verdict": "CANNOT",
        "missing_capability": (
            "no mid-fight behavior/verb swap on a trigger. preferred_behavior is read "
            "ONCE at spawn (spatial_engine.py:5335/5410) and is immutable per entity for "
            "the fight; there is no HP-threshold / phase-transition / aggro-trigger that "
            "swaps an entity's behavior or skill-set mid-fight. The only trigger-like tag "
            "is 'proximity_trigger' — itself a spawn-fixed behavior, not a transform. The "
            "SHAPESHIFT verb (form-transition that BRINGS NEW ATTACK VERBS mid-fight) has "
            "no expression. Requires a new engine mechanism: a mid-fight entity-mutation "
            "hook on a trigger."),
        "scenario_proxy": "mini_boss",
    },
}

# ---------------------------------------------------------------------------
# §3.3 formation catalogue (11 families) -> best-available registered scenario.
# The mapping follows sim-capacity §A3's formation->primitive table: swarm ->
# open_arena/dense_cell, volley-fan -> ranged-hold packs, lane -> chokepoint,
# emplacement -> held emitters, horde -> scenario_overrun. Holes recorded as holes.
# ---------------------------------------------------------------------------
FORMATION_SCENARIO_MAP = [
    # (family, representative formation_id, scenario_id, formation_class, note)
    ("MELEE-STRIKE", "ms_swarm_surround", "open_arena", "swarm",
     "massed melee runners close-and-surround; open_arena = 40-mob F2 swarm grammar"),
    ("MELEE-STRIKE", "ms_wedge_advance", "chokepoint_corridor", "lane-wedge",
     "organized wedge holds at a chokepoint; chokepoint 5m funnel expresses the wedge"),
    ("TOTEM-SENTRY", "ts_anchor_screen", "magic_pack", "anchor-screen",
     "emplaced anchor + mobile screen; magic_pack rare-champion + trash approximates "
     "anchor(champion)+screen(trash)"),
    ("DOT-AILMENT", "da_field_retreat", "dense_cell", "field",
     "casters stack DoT fields + chaff drives player in; dense_cell 24-mob close grammar"),
    ("MULTI-PROJECTILE-VOLLEY", "mpv_fan_from_position", "open_arena", "volley-fan",
     "ranged fan from position; open_arena ranged-hold packs (heading-aim fix live) = fan"),
    ("TRAP-MINE", "tm_preseed_corridor", "chokepoint_corridor", "preseed-lane",
     "pre-seeded corridor detonation field; chokepoint corridor + proximity_trigger "
     "emitters approximate pre-seed (static; no true detonation-on-advance)"),
    ("WHIRLWIND", "ww_converge_spin", "dense_cell", "converge",
     "converging spin-body pins-and-closes; dense_cell tight-offset packs approximate "
     "the converge (no true rotating-body geometry)"),
    ("AURA", "aura_carrier_pack", "magic_pack", "carrier-anchor",
     "hidden aura-carrier buffs the pack; magic_pack champion-as-carrier approximates "
     "(aura mechanics resolve; identify-and-kill-carrier is roster-semantic, not sim)"),
    ("CHANNELED-BEAM", "cb_lane_hold", "boss_with_adds", "beam-lane",
     "caster channels a directed beam + melee screen; boss_with_adds = channeler(boss) "
     "+ screen(adds), single-channeler lane expressible"),
    ("CHANNELED-BEAM", "cb_crossfire", "boss_with_adds", "beam-crossfire",
     "SEE PROBE cb_crossfire — single-beam expressible, PAIRED cross-tracking NOT native"),
    ("CHAIN-BOUNCE", "cbn_corridor_arc", "chokepoint_corridor", "corridor-arc",
     "SEE PROBE cbn_corridor_arc — corridor expressible, wall-bounce NOT"),
    ("TOTEM-SENTRY", "ts_environmental_nest", "escape_lane", "environmental-nest",
     "SEE PROBE ts_environmental_nest — streaming-nest expressible, KILLABLE anchor NOT"),
    ("SHAPESHIFT", "ss_phase_transform", "mini_boss", "transform",
     "SEE PROBE ss_phase_transform — mid-fight verb-swap CANNOT express"),
    ("DASH-STRIKER", "ds_flank_burst", "elite_pack", "flank-burst",
     "dash-and-stab from a flank; elite_pack isolated-pack + flank offsets approximate "
     "(dash-in/repos is a movement idiom, no dedicated dash-skill primitive)"),
    # HORDE overrun — the sim-capacity ≥50 cert shell (proves the concurrent-floor regime)
    ("(density)", "scenario_overrun_horde", "scenario_overrun", "horde",
     "sim-capacity ≥50 concurrent horde cert shell (55 mobs); proves the density regime "
     "the formations deal into"),
]

# Families with NO formation dealt in any era (guest-family, catalogue-only this run) —
# recorded as holes, never faked (charter §1 guest-family fork).
CATALOGUE_ONLY_HOLES = ["MINION-PET", "IDENTITY-GAUGE"]


def _functional_kit() -> dict:
    """A functional damage kit strong enough to clear the scenarios (smoke floor)."""
    return {
        "id": "w2_scenario_kit",
        "max_hp": 20000.0,
        "energy": 100.0, "max_energy": 100.0,
        "armor": 120.0,
        "skills": [
            {"name": "cleave", "damage_multiplier": 1.4, "cooldown": 0.4,
             "geometry_type": "cone", "role": "damage", "energy_cost": 6.0,
             "aoe_radius_m": 4.0},
            {"name": "bolt", "damage_multiplier": 1.0, "cooldown": 0.3,
             "geometry_type": "single_target", "role": "damage", "energy_cost": 4.0},
        ],
        "movement_speed": 7.5,
    }


def _mob_dicts_for(scenario) -> list[dict]:
    """Build mob_dicts matching scenario.mob_spawns count, using the engine's own
    threat-tier skill emitter (the smoke-pattern approach). Tier read from each spawn."""
    out = []
    for spawn in scenario.mob_spawns:
        tier = getattr(spawn, "threat_tier", None) or "swarm"
        elem = "fire"
        if tier in ("boss", "mini-boss", "miniboss", "elite"):
            skills = emit_skills_for_threat_tier(tier, signature_element=elem)
            hp = 8000.0 if "boss" in tier else 2500.0
        else:
            skills = emit_skills_for_threat_tier(tier)
            hp = 150.0
        out.append({
            "id": f"mob_{len(out)}", "max_hp": hp, "energy": 100.0, "max_energy": 100.0,
            "armor": 20.0, "skills": skills, "movement_speed": 5.5,
        })
    return out


def run_one(scenario_id: str, n_fights: int = 4) -> dict:
    """Run a short smoke of one registered scenario. Returns a run-record row."""
    scenario = ALL_SCENARIOS[scenario_id]
    kit = _functional_kit()
    mobs = _mob_dicts_for(scenario)
    rec = {"scenario_id": scenario_id, "mob_count": len(mobs), "n_fights": n_fights}
    try:
        result = run_spatial_fight(
            scenario=scenario,
            class_dict=kit,
            mob_dicts=mobs,
            n_fights=n_fights,
            session_id=f"w2_probe_{scenario_id}",
            base_seed=20260722,
            season_id="tier3-w2",
        )
        # Pull headline aggregate fields defensively (schema may vary).
        wr = result.get("win_rate", result.get("wins", None))
        mmk = result.get("mean_mobs_killed", None)
        elapsed = result.get("mean_elapsed_s", None)
        aoe_hits = result.get("total_aoe_hits", None)
        # COMBAT-EVIDENCE: a scenario "ran-clean" only if real combat transpired
        # (time advanced AND hits/kills registered) — not merely a non-crash no-op.
        combat_evidenced = bool((elapsed or 0) > 0 and ((aoe_hits or 0) > 0 or (mmk or 0) > 0))
        rec["status"] = "ran-clean" if combat_evidenced else "ran-no-combat"
        rec["win_rate"] = wr
        rec["mean_mobs_killed"] = mmk
        rec["mean_elapsed_s"] = elapsed
        rec["total_aoe_hits"] = aoe_hits
        rec["combat_evidenced"] = combat_evidenced
        rec["smoke_kit_note"] = (
            "smoke kit is a fixed functional damage kit; WR reflects kit-vs-mob-HP tuning, "
            "NOT harness health. done-predicate = scenario RUNS (executes + resolves combat), "
            "which combat_evidenced confirms.")
        rec["result_keys"] = sorted(result.keys())[:14]
    except SpatialFightConvergenceError as e:
        rec["status"] = "could-not-run"
        rec["error_class"] = "SpatialFightConvergenceError"
        rec["error"] = str(e)[:300]
    except Exception as e:
        rec["status"] = "could-not-run"
        rec["error_class"] = type(e).__name__
        rec["error"] = str(e)[:300]
        rec["traceback_tail"] = traceback.format_exc().splitlines()[-3:]
    return rec


def main():
    engine_head = "a57ee1f"  # stamped by the driver at open; re-stamp externally if moved
    print("=" * 78)
    print("TIER-3 W2 SCENARIO SET — LIVE HARNESS RUN RECORD")
    print(f"engine src: {ENGINE_SRC}  (HEAD stamped {engine_head})")
    print("=" * 78)

    # Run each UNIQUE scenario once (multiple formations map to the same scenario;
    # run the scenario once, attribute to all its formations).
    unique_scenarios = []
    for (_fam, _fid, sid, _cls, _note) in FORMATION_SCENARIO_MAP:
        if sid not in unique_scenarios:
            unique_scenarios.append(sid)

    scenario_results = {}
    for sid in unique_scenarios:
        print(f"[run] {sid} ...", flush=True)
        scenario_results[sid] = run_one(sid)
        r = scenario_results[sid]
        extra = (f"wr={r.get('win_rate')} mmk={r.get('mean_mobs_killed')}"
                 if r["status"] == "ran-clean"
                 else f"{r.get('error_class')}: {r.get('error','')[:80]}")
        print(f"      -> {r['status']}  ({extra})")

    # Assemble per-formation records, folding in the probe verdicts as caveats.
    formation_records = []
    for (fam, fid, sid, fclass, note) in FORMATION_SCENARIO_MAP:
        sres = scenario_results[sid]
        row = {
            "family": fam, "formation_id": fid, "formation_class": fclass,
            "scenario_id": sid, "scenario_status": sres["status"], "mapping_note": note,
        }
        ran_ok = sres["status"] in ("ran-clean", "ran-no-combat")
        # If this formation is one of the 4 strain-probes, the caveat governs the verdict.
        if fid in PROBE_VERDICTS:
            pv = PROBE_VERDICTS[fid]
            row["probe_verdict"] = pv["verdict"]
            row["missing_capability"] = pv["missing_capability"]
            if ran_ok:
                if pv["verdict"] == "CANNOT":
                    row["expressiveness"] = "could-not-express (proxy scenario executes; the strain mechanic is ABSENT)"
                else:  # PARTIAL
                    row["expressiveness"] = "ran-with-caveat (proxy scenario executes; the strain mechanic is MISSING per probe)"
            else:
                row["expressiveness"] = "could-not-run (proxy scenario itself failed) + strain mechanic absent"
        else:
            # non-strain formation: expressiveness == scenario status (proxy-faithful per §A3)
            if ran_ok:
                row["expressiveness"] = "ran-clean (proxy scenario expresses the formation class per sim-capacity §A3)"
            else:
                row["expressiveness"] = f"could-not-run ({sres.get('error_class')})"
        formation_records.append(row)

    # Holes (guest-family, catalogue-only) — recorded, never faked.
    hole_records = [{"family": f, "status": "hole",
                     "note": "guest-family, catalogue-only this run (charter §1); no formation dealt, no scenario"}
                    for f in CATALOGUE_ONLY_HOLES]

    # Census
    ran_clean = sum(1 for r in formation_records if r["expressiveness"].startswith("ran-clean"))
    ran_caveat = sum(1 for r in formation_records if r["expressiveness"].startswith("ran-with-caveat"))
    could_not_express = sum(1 for r in formation_records if r["expressiveness"].startswith("could-not-express"))
    could_not_run = sum(1 for r in formation_records if r["expressiveness"].startswith("could-not-run"))

    out = {
        "artifact": "tier3-w2-scenario-run-record",
        "run": "Tier-3 Encounter-Geometry Run · Wave W2 · Phase (c)",
        "author": "named-gamora sub-agent", "date": "2026-07-22",
        "engine_head_at_run": engine_head,
        "engine_invoked_by_path": ENGINE_SRC,
        "zero_writes_to_engine_repo": True,
        "probe4_verdicts": {k: {"verdict": v["verdict"],
                                "missing_capability": v["missing_capability"],
                                "scenario_proxy": v["scenario_proxy"]}
                            for k, v in PROBE_VERDICTS.items()},
        "unique_scenario_results": scenario_results,
        "formation_records": formation_records,
        "hole_records": hole_records,
        "census": {
            "unique_scenarios_run": len(unique_scenarios),
            "scenarios_ran_clean": sum(1 for s in scenario_results.values() if s["status"] == "ran-clean"),
            "scenarios_ran_no_combat": sum(1 for s in scenario_results.values() if s["status"] == "ran-no-combat"),
            "scenarios_executed_ok": sum(1 for s in scenario_results.values() if s["status"] in ("ran-clean", "ran-no-combat")),
            "scenarios_could_not_run": sum(1 for s in scenario_results.values() if s["status"] == "could-not-run"),
            "formation_records": len(formation_records),
            "formation_ran_clean": ran_clean,
            "formation_ran_with_caveat": ran_caveat,
            "formation_could_not_express": could_not_express,
            "formation_could_not_run": could_not_run,
            "holes_catalogue_only": len(hole_records),
            "probe4_verdict_summary": {k: v["verdict"] for k, v in PROBE_VERDICTS.items()},
        },
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    print("-" * 78)
    print("PROBE-4 VERDICTS:")
    for fid, pv in PROBE_VERDICTS.items():
        print(f"  {fid:24s} {pv['verdict']}")
    print("-" * 78)
    print(f"unique scenarios run:      {len(unique_scenarios)}  "
          f"(executed-ok {out['census']['scenarios_executed_ok']} "
          f"[clean {out['census']['scenarios_ran_clean']} / no-combat "
          f"{out['census']['scenarios_ran_no_combat']}], "
          f"failed {out['census']['scenarios_could_not_run']})")
    print(f"formation records:         {len(formation_records)}")
    print(f"  ran-clean:               {ran_clean}")
    print(f"  ran-with-caveat:         {ran_caveat}")
    print(f"  could-not-express:       {could_not_express}")
    print(f"  could-not-run:           {could_not_run}")
    print(f"holes (catalogue-only):    {len(hole_records)}")
    print("=" * 78)
    print(f"wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
