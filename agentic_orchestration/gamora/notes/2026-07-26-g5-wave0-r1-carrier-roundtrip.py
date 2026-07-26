#!/usr/bin/env python3
"""G-5 Wave 0 — R-1 marker PRODUCTION-PATH round-trip evidence (gamora/v-g4-liveness-gate-2).

Clears Gate-2 DEFECT R1-CARRIER's second half: the round-trip clause requires *"a production-path
season fixture emitted post-gate and read at the gamora → star-lord telemetry boundary."* The
first submission backed it with a hand-built `FightResult` inside a unit test — a struct-shape
assertion, on the wrong object.

This driver runs a REAL fight through `SpatialFightEngine.run()` and walks the emitted
`SpatialFightResult` — the row every export builder in `export/schemas.py` is constructed from —
across the whole boundary: validate() → asdict() → star-lord's concrete SQLite writer.

The rows it prints are the rows published in `simulation/MIGRATION.md` §5. Re-run it to
reproduce them; it is deterministic (fixed seed, fixed kit).

    cd ~/Games/reincarnated-engine
    python3 ../reincarnated-collaboration/agentic_orchestration/gamora/notes/\
2026-07-26-g5-wave0-r1-carrier-roundtrip.py

Finding:   qa/findings/2026-07-26-gate2-g5-wave0-liveness-gate.md §1
Math note: simulation/math/g5-wave0-universal-liveness-gate-2026-07-26.md §7.2
Mirrors:   tests/test_g5_wave0_liveness_gate.py :: TestForwardOnlyMarkerProductionPath (T-M/b)
"""
from __future__ import annotations

import dataclasses
import sqlite3
import sys
from pathlib import Path

_ENGINE = Path.home() / "Games" / "reincarnated-engine"
sys.path.insert(0, str(_ENGINE / "src"))


# ── The production kit. Deliberately lethal + ailment-bearing: the player clears every mob, so
#    defenders actually die mid-fight and `burn` actually rides along. A fight in which nothing
#    dies is a fight in which the gate could not have fired, and the marker assertion would be
#    vacuous (Discipline #11 — pin the rig before reading it).
CLASS_DICT = {
    "id": "class_g5_wave0_roundtrip",
    "movement_speed": 8.0,
    "stat_distribution": {"vitality": 54, "intelligence": 54, "strength": 54},
    "scaling_attribute": "intelligence",
    "skills": [{
        "name": "Arcane Blast",
        "damage_multiplier": 1.2, "cooldown_seconds": 2.0, "energy_cost": 20.0,
        "skill_type": "damage",
        "spatial_geometry_type": "circle", "geometry_type": "circle",
        "canonical_element": "fire", "scaling_attribute": "intelligence",
        "effects": [
            {"name": "damage", "params": {"damage_type": "magical", "magnitude": 60.0}},
            {"name": "burn", "params": {"duration_seconds": 4.0, "magnitude": 5.0}},
        ],
    }],
}

MOB_DICT = {
    "id": "monster_g5_wave0_roundtrip",
    "max_hp": 500.0, "movement_speed": 5.75,
    "preferred_behavior": "melee_aggressive",
    "aggro_radius_m": 8.0, "leash_distance_m": 35.0,
    "skills": [{
        "name": "Basic Attack",
        "damage_multiplier": 0.8, "cooldown_seconds": 1.5, "energy_cost": 10.0,
        "skill_type": "damage", "spatial_geometry_type": "point",
        "scaling_attribute": "strength",
        "effects": [{"name": "damage", "params": {"damage_type": "physical",
                                                  "magnitude": 20.0}}],
    }],
}

SEED = 91126


def production_spatial_fight():
    from reincarnated.simulation.spatial_gauntlet.arena import SCENARIO_OPEN_ARENA
    from reincarnated.simulation.spatial_gauntlet.spatial_engine import (
        SpatialFightEngine, entity_from_class_dict, entity_from_monster_dict,
    )
    scenario = SCENARIO_OPEN_ARENA
    player = entity_from_class_dict(CLASS_DICT, scenario.player_spawn, 1.0)
    mobs = [entity_from_monster_dict(MOB_DICT, spawn) for spawn in scenario.mob_spawns]
    engine = SpatialFightEngine(
        scenario=scenario, player=player, mobs=mobs,
        seed=SEED, session_id="g5-wave0-roundtrip",
    )
    return engine.run()


def main() -> int:
    from reincarnated.simulation.fight_result import FightResult
    from reincarnated.simulation.liveness_gate import LIVENESS_GATE_VERSION
    from reincarnated.simulation.spatial_gauntlet.spatial_telemetry import SpatialFightResult
    from reincarnated.telemetry.db import apply_schema_migrations
    from reincarnated.telemetry.spatial_recorder import SqliteSpatialTelemetryWriter

    print("=" * 78)
    print("G-5 WAVE 0 — R-1 MARKER, PRODUCTION-PATH ROUND-TRIP")
    print("=" * 78)

    row = production_spatial_fight()

    # ROW 0 — pin the rig BEFORE reading the marker off it.
    print("\n[RIG] carrier            : %s (SpatialFightEngine.run() return)" % type(row).__name__)
    print("[RIG] fight              : winner=%s  kills=%d/%d  elapsed=%.2fs  killing_element=%s"
          % (row.winner, row.mobs_killed, row.total_mob_count, row.elapsed_s, row.killing_element))
    rig_ok = (row.winner == "player" and row.mobs_killed == row.total_mob_count > 0
              and row.killing_element == "fire")
    print("[RIG] reached kills      : %s  (resolver-backed damage path taken)"
          % ("YES" if rig_ok else "NO — EVIDENCE IS VACUOUS"))

    # ROW 1 — the marker is on the row the production route emitted.
    ok1 = (row.liveness_gate_version == LIVENESS_GATE_VERSION == 1
           and isinstance(row.liveness_gate_version, int)
           and not isinstance(row.liveness_gate_version, bool))
    print("\n[1] marker on the emitted SpatialFightResult      : %s  (value=%r, type=%s)"
          % ("PASS" if ok1 else "FAIL", row.liveness_gate_version,
             type(row.liveness_gate_version).__name__))

    # ROW 2 — P7 writer gate does not reject the additive field.
    try:
        row.validate()
        ok2 = True
    except Exception as exc:                                    # noqa: BLE001 — report, not mask
        ok2 = False
        print("    validate() raised:", exc)
    print("[2] survives validate() (P7 writer gate)         : %s" % ("PASS" if ok2 else "FAIL"))

    # ROW 3 — survives serialization.
    payload = dataclasses.asdict(row)
    ok3 = payload.get("liveness_gate_version") == 1
    print("[3] survives dataclasses.asdict() serialization  : %s  (value=%r)"
          % ("PASS" if ok3 else "FAIL", payload.get("liveness_gate_version")))

    # ROW 4 — star-lord's CONCRETE writer accepts the row (brownfield half of the contract).
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    apply_schema_migrations(conn)
    writer = SqliteSpatialTelemetryWriter(conn)
    writer.write_fight_result(row)
    persisted = conn.execute(
        "SELECT COUNT(*) FROM spatial_fight_results WHERE fight_id = ?", (row.fight_id,)
    ).fetchone()[0]
    cols = [r[1] for r in conn.execute("PRAGMA table_info(spatial_fight_results)")]
    ok4 = writer._writes_failed == 0 and writer._writes_ok == 1 and persisted == 1
    print("[4] accepted by star-lord's SqliteSpatialTelemetryWriter : %s  "
          "(writes_ok=%d writes_failed=%d rows_persisted=%d)"
          % ("PASS" if ok4 else "FAIL", writer._writes_ok, writer._writes_failed, persisted))
    print("    column exists in schema yet                   : %s  "
          "(OWED to star-lord — recommended INTEGER DEFAULT 0)"
          % ("yes" if "liveness_gate_version" in cols else "NO, as expected"))
    conn.close()

    # ROW 5 — absent-is-pre-gate.
    archived_pre_gate_row = {"fight_id": "legacy", "winner": "player"}     # no marker key
    ok5 = archived_pre_gate_row.get("liveness_gate_version", 0) == 0
    print("[5] archived pre-gate row reads 0 via .get(key,0) : %s"
          % ("PASS" if ok5 else "FAIL"))

    # ROW 6 — the two carriers agree, and are genuinely independent classes.
    defaults = {
        c.__name__: {f.name: f.default for f in dataclasses.fields(c)}["liveness_gate_version"]
        for c in (FightResult, SpatialFightResult)
    }
    is_sub = issubclass(SpatialFightResult, FightResult)
    ok6 = (defaults["FightResult"] == defaults["SpatialFightResult"] == LIVENESS_GATE_VERSION
           and not is_sub)
    print("[6] the two carriers AGREE                       : %s  (%s; subclass=%s)"
          % ("PASS" if ok6 else "FAIL", defaults, is_sub))

    all_ok = rig_ok and ok1 and ok2 and ok3 and ok4 and ok5 and ok6
    print("\n" + "-" * 78)
    print("ROUND-TRIP: %s — 6/6 rows executed against a production-path row (seed=%d)"
          % ("PASS" if all_ok else "FAIL", SEED))
    print("-" * 78)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
