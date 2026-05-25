# Round-Trip Smoke — Stage 4 Mechanical-Tagging — Second Leg (star-lord)

**Date:** 2026-05-25
**Author:** star-lord
**Wave:** 7
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md` § 5 + § 5.5
**Leg:** Second leg (fight_log → star-lord export packet boundary verification)
**Prior leg:** gamora first leg PASS — `agentic_orchestration/gamora/notes/2026-05-25-wave-7-round-trip-smoke-fight-log.json` + gamora sign-off in fight_log

---

## 1. Scope

Per dispatch § 5.5 + KR scope-clarification reframe: round-trip smoke scoped at **fight_log-construction-boundary level**. gamora demonstrated fight_log-construction works (first leg). Star-lord second leg verifies field-presence at the **gamora fight_log → star-lord export packet boundary**.

Weapon under test: `weapon_id=209667` (Basket hilt sword, historical register, quality_tier=A).

---

## 2. Step 1 — fight_log read + required field enumeration

**Source:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-05-25-wave-7-round-trip-smoke-fight-log.json`

**weapon_sim_props node in fight_log:**

| Field | Value | Non-null |
|---|---|---|
| `damage_amplitude_min` | 0.7 | YES |
| `damage_amplitude_max` | 1.6 | YES |
| `primary_stat` | STR | YES |
| `range_min_units` | 0.5 | YES |
| `range_max_units` | 2.5 | YES |
| `base_attack_speed` | 1.5 | YES |
| `hits_per_attack` | 1 | YES |
| `aoe_radius_units` | 0.0 | YES |
| `sim_viable` | 1 | YES |

All 8 required fields present and non-null. `damage_amplitude_min=0.7` and `damage_amplitude_max=1.6` match the DB row confirmed in `weapon_sim_props` table (`reincarnated-loadout/data/telemetry.db`).

**gamora field_presence_verification block:** `result: PASS` (included in fight_log at key `field_presence_verification`).

**Result: PASS**

---

## 3. Step 2 — Export pipeline run

**Export pipeline invoked:** `reincarnated.export.season_exporter.export_season(season_id='season_001005', ...)`

**Engine telemetry DB:** `reincarnated-engine/src/reincarnated/telemetry/telemetry.db`

**Season dir:** `reincarnated-engine/seasons/season_001005/`

Export completed without exception. Stage B validators (`_validate_stage_b_classes`, `_validate_stage_b_monsters`) passed.

**Export packet files produced:**
- `classes.json` — 11 classes
- `monsters.json`
- `gear_pool.json`
- `metadata.json` — `format_version: "1.0"`
- `damage_formula.md`, `design_context.md`

**Result: PASS — export pipeline runs cleanly**

---

## 4. Step 3 — Export packet field-presence check

### 4.1 Stage B required fields (existing validators)

All Stage B required class fields present on all 11 exported classes:

```
id, name, archetype_tag, energy_type, role_orientation, range_profile,
dominant_element, is_act_boss, stat_distribution, skills, balance_metadata,
movement_speed
```

**Stage B validator result: PASS**

### 4.2 weapon_sim_props fields at export boundary

Checked all three export files (`classes.json`, `gear_pool.json`, `metadata.json`) for the 8 weapon_sim_props fields:

| Field | classes.json | gear_pool.json | metadata.json |
|---|---|---|---|
| `damage_amplitude_min` | ABSENT | ABSENT | ABSENT |
| `damage_amplitude_max` | ABSENT | ABSENT | ABSENT |
| `primary_stat` | ABSENT | ABSENT | ABSENT |
| `range_min_units` | ABSENT | ABSENT | ABSENT |
| `range_max_units` | ABSENT | ABSENT | ABSENT |
| `base_attack_speed` | ABSENT | ABSENT | ABSENT |
| `hits_per_attack` | ABSENT | ABSENT | ABSENT |
| `aoe_radius_units` | ABSENT | ABSENT | ABSENT |

**Result: `damage_amplitude_min` + `damage_amplitude_max` are NOT PRESENT in the export packet. No weapon_sim_props node exists at any export file boundary.**

This is expected given the current export pipeline architecture — see § 5 below.

---

## 5. Step 4 — Forward-compat gap analysis

### 5.1 Architecture gap: weapon_sim_props lives in a separate DB

The `weapon_sim_props` table lives in **`reincarnated-loadout/data/telemetry.db`** (the substrate catalogue DB owned by elrond/rocket). The season export pipeline reads from:

1. `reincarnated-engine/seasons/<season_id>/` — generated season JSON files (classes, monsters, skills)
2. `reincarnated-engine/src/reincarnated/telemetry/telemetry.db` — engine telemetry DB (gear_instances, abilities, classes.carried_gear)

These are two separate databases. The export pipeline (`season_exporter.py`) has no connection to the loadout telemetry DB and therefore cannot currently pass through `weapon_sim_props` fields.

### 5.2 Export packet schema has no weapon_sim_props surface

The export schemas (`export/schemas.py`) define:
- `ExportClass` — class identity, skills, carried_gear, balance_metadata, movement_speed
- `ExportMonster` — monster identity, skills, combat stats
- `ExportGearItem` — gear item with stats/rolled_effects/ability_modifiers
- `ExportMetadata` — season-level metadata

None of these schemas include a `weapon_sim_props` node or any of its 8 fields. There is no `ExportWeaponSimProps` schema.

### 5.3 Structural path: fight_log → telemetry DB (NOT → export packet)

The gamora fight_log is an **in-memory simulation artifact** produced during convergence. The fight_log's `weapon_sim_props` node is gamora's verification envelope for this smoke test; it is not written to the engine telemetry DB by the existing recorder (`telemetry/recorder.py`). The recorder writes to tables: `class_fight_loadouts`, `class_balance_results`, `class_monster_win_rates`, `recompose_attempts`, `fight_events`, `spatial_fight_results` — none of which include weapon_sim_props columns.

Therefore the chain is:

```
weapon_sim_props DB (loadout)
  → gamora fight_log (in-memory, during simulation)
  → gamora sign-off / smoke artifact [BOUNDARY HERE - gamora leg]
  -- NO path to engine telemetry DB --
  -- NO path to season export pipeline --
```

The export packet chain is:

```
engine seasons/ JSON files
  + engine telemetry DB (gear_instances, abilities, classes)
  → season_exporter.py
  → export packet (classes.json / gear_pool.json / metadata.json / monsters.json)
  [BOUNDARY HERE - star-lord leg]
```

These are separate paths. The Phase 2 substrate-binding work (post-Cycle-10) is what will integrate `weapon_sim_props` values into the fight engine's damage formula — at which point they would flow through the season generation pipeline and potentially into the export packet if Phase 2 design requires it.

### 5.4 Forward-compat gap classification

**Gap name:** `weapon_sim_props` not surfaced in export packet

**Gap type:** Structural — separate DB boundary + no ExportWeaponSimProps schema

**Blast radius:** None at this time. Per dispatch § 6 (out-of-scope) and the KR scope-clarification reframe, Phase 2 substrate-binding is downstream post-Cycle-10 work. Loadout app reads intermediate engine outputs at `data/<season>/classes/*.json`, NOT the export packet (per loadout-analytics-suite info-architecture).

**Forward-compat assessment:** Export packet schema is **additive-compatible** for a future `weapon_sim_props` node. The existing schema can accommodate a new `ExportWeaponSimProps` Pydantic model added to `ExportGearItem` (per-item weapon substrate, if Phase 2 binds weapon to gear) or as a standalone lookup table in the export packet. No breaking changes required.

**v1.1+ candidate fields** (if Phase 2 design requires export-packet exposure):
- `ExportGearItem.weapon_sim_props: ExportWeaponSimProps | None = None` — additive nullable field
- Would require: `season_exporter.py` to query `weapon_sim_props` table from loadout DB (new DB connection); `ExportWeaponSimProps` Pydantic model; export validator extension

---

## 6. Acceptance criteria status

| Criterion | Status |
|---|---|
| fight_log read + parsed; required fields enumerated | PASS |
| Export pipeline run + export packet produced | PASS |
| `damage_amplitude_min` + `damage_amplitude_max` field-presence VERIFIED in export packet | GAP — fields not present in export packet (structural gap, expected at this stage; see § 5) |
| Any export-packet schema forward-compat gaps documented + surfaced | COMPLETE — documented in § 5 above |
| Output artifact at `agentic_orchestration/qa/findings/2026-05-25-stage-4-round-trip-smoke.md` | COMPLETE (this file) |

### 6.1 Clarification on acceptance criterion 3

Criterion 3 ("VERIFIED in export packet") requires clarification for jack-ryan ratification. The dispatch scope-clarification reframe (per jack-ryan Gate-2 + scope-doc § 6 known-unknown) scoped the round-trip at the **fight_log-construction-boundary level**. gamora's first leg verified field-presence at the fight_log boundary (PASS). Star-lord's second leg has verified:

1. The fight_log weapon_sim_props fields ARE correct and non-null (values match DB)
2. The export pipeline runs without error and passes Stage B validation
3. The export packet does NOT currently include weapon_sim_props fields — this is structural, not a regression

The Principle 6 cross-seam contract change (`weapon_sim_props` schema field add on a cross-seam fixture) is verified to be **correctly bounded**: `weapon_sim_props` lives in the substrate catalogue DB, flows through the fight_log boundary (gamora verified), and does NOT yet have a path to the export packet. That path is Phase 2 substrate-binding (post-Cycle-10).

**Round-trip smoke assessment:** The Stage 4 mechanical-tagging schema change (`damage_amplitude_min`/`max` + DEX constraint fix) is correctly landed in `weapon_sim_props`, correctly consumed by gamora at the fight_log boundary, and does not break the existing export pipeline. The export packet forward-compat gap is a **known design gap** (Phase 2 work item) with no blast radius at this stage.

---

## 7. Signal for jack-ryan Principle 6 ratification

Per dispatch § 5.5 acceptance criterion: "Round-trip smoke PASS" gates the `rocket/cycle-10-stage-4-mechanical-tagging-2026-05-25` tag.

**Star-lord assessment:** The round-trip smoke is STRUCTURALLY COMPLETE within the scope-clarified boundary (fight_log-construction level). The `damage_amplitude_min`/`max` fields are:
- Present and non-null in `weapon_sim_props` DB table (2,293 rows)
- Present and non-null in gamora's fight_log (weapon_id=209667, seed=42)
- Not present in the export packet (structural gap, correctly documented)

The export pipeline runs without regression. There is no silent drop, no schema drift, no broken boundary at the existing export pipeline level.

jack-ryan is the authority on whether this constitutes "Round-trip smoke PASS" for Principle 6 purposes given the scope-clarification reframe, or whether additional work is required before the tag fires.

---

## 8. References

- Dispatch: `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md`
- gamora fight_log: `agentic_orchestration/gamora/notes/2026-05-25-wave-7-round-trip-smoke-fight-log.json`
- Export schemas: `reincarnated-engine/src/reincarnated/export/schemas.py`
- Export pipeline: `reincarnated-engine/src/reincarnated/export/season_exporter.py`
- Substrate DB: `reincarnated-loadout/data/telemetry.db` (weapon_sim_props table — 2,293 rows, all non-null)
- jack-ryan Gate-2: `agentic_orchestration/qa/findings/2026-05-25-gate2-stage-4-mechanical-tagging.md`
- Cycle 10 scope-doc: `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`
