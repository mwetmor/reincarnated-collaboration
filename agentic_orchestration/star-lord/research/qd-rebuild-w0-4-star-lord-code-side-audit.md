# QD-Rebuild W0.4 — Star-Lord Code-Side Audit
# Telemetry / Export / LLM Seam

**Date:** 2026-05-21
**Author:** star-lord (Discipline #11 survey-mode: report what EXISTS; no "should" interleaving)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-rocket-plus-gamora-plus-star-lord-w0-4-specialist-code-audit.md`
**Approved by:** gandalf attestation 2026-05-21 § 5; Matt autonomous-operation directive
**Status:** COMPLETE
**Tag fired:** `star-lord/v1.15-w0-4-code-side-audit-1`

---

## 1. HIGH-Risk LC Verdicts — Star-Lord Seam Exposure

### LC-006: Canonical-Four Element Labels Universally Exposed to LLM

**Jack-ryan Phase 1 disposition:** DRIFT-CANDIDATE
**Star-lord code-side verdict: RESOLVED (within star-lord seam)**

The LLM naming module at `/Users/admin/Games/reincarnated-engine/src/reincarnated/llm/naming.py` has fully implemented the Stage 3 cipher migration. Specific findings:

- **Lines 7-48 (module docstring):** Explicitly documents that "Canonical-four labels are now HIDDEN from all LLM-bound prompts per Discipline #14." The cipher architecture is in force.
- **Lines 74-95 (`_grouping_label()`):** Canonical substrate names are translated to grouping-layer abstract labels via `_CANONICAL_TO_GROUPING` dict (loaded at boot from the registry). The function raises `KeyError` on unknown substrate — Pattern P7 fail-loud, no silent fallback.
- **Lines 98-145 (`_seasonal_element_line()`, `_elements_summary_line()`, `_resolve_seasonal_name()`):** All three functions emit only grouping-layer labels and seasonal vocabulary names to LLM prompts. Canonical-four labels never appear in constructed prompt strings.
- **Lines 197-503 (all four naming functions — `name_skill`, `name_class`, `name_monster`, `name_gear_item`):** All use `_seasonal_element_line()` / `_elements_summary_line()` / `_resolve_seasonal_name()` exclusively. No direct `canonical_element` exposure to LLM prompt text.
- **Test guard:** Module docstring at line 48 references `tests/test_no_canonical_four_in_llm_prompts.py` which asserts no canonical-four labels appear in any constructed prompt for a 5-class smoke season.

**However:** jack-ryan's Phase 1 audit flagged `llm/naming.py:26-36`, `:87`, `:89`; `element/selector.py:43-47`, `:394-446`; `canonical/library_generator.py:85` as exposure sites. The `element/selector.py` and `canonical/library_generator.py` sites are in rocket's seam — NOT star-lord's seam. Star-lord owns `llm/naming.py` only, and that file is RESOLVED.

**Cross-seam note (ADR-004):** The `element/selector.py` and `canonical/library_generator.py` sites remain in rocket's seam. Per jack-ryan's Phase 1 audit, those sites remain DRIFT-CANDIDATE for rocket to verify in their W0.4 section.

**DEPRECATED fields in export:** `schemas.py` lines 25, 50, 51, 73, 74, 91, 92, 137 carry `canonical_element` and `dominant_element` fields on `ExportSkill`, `ExportClass`, `ExportMonster`, `ExportGearItem`, and `ExportMetadata`. These are marked `# DEPRECATED (Stage 3)` with additive `seasonal_element` / `seasonal_dominant_element` / `seasonal_elements` counterparts. The DEPRECATED fields are preserved for drax backward-compat, not newly exposed to LLM. This is the correct Stage 3 pattern — internal infrastructure preserved, generative surface hidden.

**Verdict:** RESOLVED for the star-lord seam (`llm/naming.py` + export schemas). The cipher migration is live and test-guarded. Residual `DEPRECATED` fields in export schemas are intentional backward-compat infrastructure, not LC-006 drift.

---

### LC-007: Humanoid Gear Schema — Export Packet Exposure

**Jack-ryan Phase 1 disposition:** DOCUMENTED (Position C migration locked but not yet shipped)
**Star-lord code-side verdict: VERIFIED (current state confirmed; migration not yet shipped)**

Export packet (`schemas.py`) carries the following humanoid-presupposing gear fields verbatim:

- `ExportGearItem.slot: str` — `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/schemas.py:88` — takes values `"weapon"`, `"off_hand"`, `"armor"`, `"accessory"` (humanoid slot names)
- `ExportGearItem.handedness: str` — `schemas.py:89` — takes values `"1h"` / `"2h"` (bilateral arm anatomy presupposition)
- `season_exporter.py:396-398` reads `slot` and `handedness` directly from the `gear_instances` DB table, which stores the raw values written by rocket's gear schema (`generation/gear_schema.py:198-310`)

The `gear_instances` telemetry table at `migrations.py:_V1_6` (line 363-385) carries:
- `slot TEXT NOT NULL` — weapon/armor/accessory/off_hand
- `handedness TEXT NOT NULL DEFAULT '1h'`

These field values are passed through the export chain without transformation. The export packet consumed by drax carries humanoid slot labels exactly as written by rocket.

**Cross-seam impact (ADR-004):** The star-lord seam is a passive conduit for LC-007's humanoid slot names. The generation origin is rocket (`gear_schema.py:198-310`); the telemetry persistence is star-lord (`gear_instances` table + export schemas); the consumption is drax (loadout JSON). Fixing LC-007 requires a coordinated three-seam migration: rocket renames slots, star-lord updates `gear_instances` schema + `ExportGearItem`, drax updates consumption. This is the "14-item cluster" noted in jack-ryan's audit. Any rocket-side fix dispatch MUST include a star-lord MIGRATION.md entry before tagging per ADR-004.

**Verdict:** VERIFIED. Current code state confirmed as documented. Humanoid slot names (`weapon`, `off_hand`, `armor`, `accessory`, `handedness`) appear verbatim in `schemas.py:88-89`, `season_exporter.py:396`, `migrations.py:_V1_6`. No fix in scope for this verification workstream.

---

### Other HIGH-Risk LCs — Star-Lord Seam Exposure Assessment

**LC-001 (Archetype templates):** No exposure in star-lord seam. The `classes` telemetry table stores `archetype TEXT` and `canonical_element TEXT` as strings (write-through from rocket/gamora output); recorder at `recorder.py:992-1026` reads `pc.archetype_tag` and `pc.dominant_element` verbatim. Star-lord is a passive recorder — LC-001 resolution is entirely in rocket's seam. **No star-lord action required.**

**LC-002 (Fire selection bias):** Telemetry at `recorder.py:120-166` (`record_seasonal_elements`) and `_insert_classes` (line 958-1026) write `canonical_element` and `element_name` as emitted by the element selector. Star-lord does not influence selection logic. The `seasonal_elements` table records whatever the selector emits; fire over-representation would be visible in the telemetry data but is not caused by star-lord code. **No star-lord action required; bias measurement is a jack-ryan/gamora analysis task.**

**LC-003 (Modifier floor-lock):** Star-lord's `class_balance_results` table records `room_winrate`, `per_tier_gate_passed`, and all per-tier WR columns. The `floor_lock_recompose`, `working_modifier`, and `floor_lock_detected` fields from gamora's recompose-hive Option B spec (per `simulation/MIGRATION.md` lines 2333-2344) are NOT yet in the star-lord telemetry schema. See Section 4 below for the schema-drift finding.

**LC-004 (Energy-type gradient):** No direct star-lord seam exposure. The `classes` table stores `energy_type TEXT` (schema 1.3; `migrations.py:_V1_3`), which records the downstream effect of the gradient but does not cause it.

**LC-005 (PackProxy ×8):** The `class_fight_loadouts` table records per-fight outcomes including pack fights (no filtering at write time). The `pack_proxy` distinction is not recorded as a column in telemetry — pack fights are indistinguishable from non-pack fights in the existing schema by fight type. Per W0.9 (gauntlet architecture migration), the PackProxy retirement will change what fight data is generated; star-lord will need a new column or tagging mechanism to distinguish spatial-sim fight results from legacy PackProxy results. This is a P0 W0.9 → star-lord follow-on item for the W0.9 dispatch. **No current schema action required (P0 W0.4 verification only).**

**LC-008 (STR/DEX/INT labels):** `ExportClass.stat_distribution: dict[str, int]` in `schemas.py:54` carries the raw stat dict. The keys (`str`, `dex`, `int`, etc.) flow through to the export packet as-is. The humanoid-label concern from jack-ryan's audit is correct — the LLM receives `energy_type`, `role_orientation`, `range_profile` (abstract) but stat distribution is labeled with STR/DEX/INT. However, stat distribution is NOT directly in any LLM prompt in `naming.py` — the class naming prompt includes `stats.as_dict()` at line 323 which emits the raw dict. This is a residual humanoid-label exposure path through `name_class()`. The LC-008 disposition (PRESERVE at math layer; REMOVE at LLM-visibility layer) means this line is a candidate for per-embodiment narrative reframing in a future dispatch. Current state: the raw stat dict appears in the `name_class` user prompt. **Cross-seam impact: star-lord (`naming.py:323`) is a consumption site for LC-008's LLM-visibility concern; documented but not in scope for this verification dispatch.**

**LC-012 (Foundation validator):** No star-lord seam exposure. The foundation validator is rocket's seam only.

---

## 2. § 2.8 W1.13 Telemetry Implications — ArchiveEntry Schema Gap

**Activation dispatch § 2.8 ArchiveEntry spec fields:**
```yaml
ArchiveEntry:
  bc_coordinate: [Axis1..Axis5_bins]     # 8-tuple
  node_subset: [node_id_1, ..., node_id_8]  # list
  per_node_coefficients: {node_id: rank_1_to_20}  # dict
  scalar_modifier: <float>
  per_tier_WR: {swarm, magic, elite, mini_boss, boss}  # dict
  cohesion_theme: <assigned_at_P5>
  visual_identity: <assigned_at_P6>
```

**Current schema state — none of the W1.13 ArchiveEntry fields exist anywhere in the star-lord seam:**

- `node_subset` — NOT PRESENT in `migrations.py`, `recorder.py`, or `schemas.py`
- `per_node_coefficients` — NOT PRESENT
- `scalar_modifier` — NOT PRESENT (the balance_metadata field `final_modifier` exists in the `classes` table at `migrations.py:_V1_0:line 120` and is written at `recorder.py:1015`, but this is the current scalar convergence modifier, not the W1.13 multi-dim tuning scalar)
- `bc_coordinate` — NOT PRESENT (the BC coordinate system does not yet exist in telemetry)
- `per_tier_WR` — PARTIALLY PRESENT: individual per-tier WR columns exist on `class_balance_results` as of schema 2.9 (`swarm_win_rate`, `magic_win_rate`, `elite_win_rate`, `mini_boss_win_rate`, `boss_win_rate`). These are per-class convergence results, not per-archive-entry results. The ArchiveEntry's `per_tier_WR` is at the archive-entry level, which is a new concept.
- `cohesion_theme` — NOT PRESENT (assigned at P5; no P5 infrastructure exists)
- `visual_identity` — NOT PRESENT (assigned at P6; no P6 infrastructure exists)

**Schema extension scope for P1 W1.X consumption:**

The W1.13 ArchiveEntry requires a new `archive_entries` table (or equivalent) — not an extension of existing tables. The existing `classes` and `class_balance_results` tables record per-season per-class convergence results; they do not have a concept of a BC-coordinate-targeted archive entry that can contain a node-subset reference build.

Minimum new table schema for P1 W1.X:
```sql
CREATE TABLE IF NOT EXISTS archive_entries (
    entry_id           TEXT PRIMARY KEY,        -- UUID
    season_id          TEXT,                    -- which season generated this entry
    class_id           TEXT,                    -- which class template was the source
    bc_coordinate      TEXT NOT NULL,           -- JSON-encoded 8-element bin tuple
    node_subset        TEXT NOT NULL,           -- JSON-encoded list of node_ids
    per_node_coefficients TEXT NOT NULL,        -- JSON-encoded {node_id: rank}
    scalar_modifier    REAL NOT NULL,
    per_tier_wr        TEXT,                    -- JSON-encoded {tier: WR_float}
    cohesion_theme     TEXT,                    -- NULL until P5 assignment
    visual_identity    TEXT,                    -- NULL until P6 assignment
    created_at         TIMESTAMP NOT NULL,
    schema_version     TEXT NOT NULL
);
```

This is a new-table addition, not an ALTER of existing tables. It does not conflict with current schema. The `bc_coordinate` column requires P2 BC-measurement implementation to populate; until then it stores NULL or is not written.

**Export implications:** The `ExportSeason` schema at `schemas.py:150-156` exports classes, monsters, and gear pool. It has no `archive_entries` collection. Adding archive entry export is a new schema element for P3+ (archive insertion phase). No export schema change needed in P1.

**P1 W1.X action required (star-lord):** New `archive_entries` table migration (a new `_V2_14` or later block in `migrations.py`). Matt authorization required per ADR-006 before any write migration is applied to production DB.

---

## 3. W0.8 New Schema-Field Recommendations — `bounce_count` + `spawn_count`

**Source:** `agentic_orchestration/rocket/research/qd-rebuild-w0-8-axis-2-substrate-check.md` lines 217, 442, 458-460

**W0.8 recommendation:** Add `bounce_count` (int; applicable to `chain_lightning` and `ricochet_bounce`) and `spawn_count` (int; applicable to `multi_projectile` and totem) to the Ability schema.

**Current star-lord schema state:**

The `abilities` table (created in `migrations.py:_V1_0:lines 132-159`) has:
- `geometry_type TEXT` — 24-type rich vocab geometry name (e.g., `chain_lightning`)
- `geometry_params TEXT` — JSON (reserved but no documented contents currently populated)
- `effects TEXT` — JSON array of `{name, params}` dicts

The `effects` JSON is the current parameter carrier. However, `bounce_count` and `spawn_count` are ability-level structural parameters, not per-effect parameters. They belong at the `abilities` row level for direct SQL queryability in BC measurement.

**Round-trip breakage assessment:**

Adding `bounce_count INTEGER` and `spawn_count INTEGER` as nullable columns to the `abilities` table is a standard additive `ALTER TABLE` migration (pattern consistent with all v2.x migrations in this seam). No round-trip breakage risk:
- `recorder.py:_insert_skill()` (lines 1101-1133) currently writes: `ability_id`, `season_id`, `owner_type`, `owner_id`, `name`, `role`, `canonical_element`, `geometry_type`, `timing_type`, `timing_params`, `cooldown_seconds`, `energy_cost_pct`, `effects`, `composition_mode`, `canonical_ref`, `flavor_text`, `schema_version`. Adding two nullable columns requires adding them to the INSERT column list and reading them from the `skill` object via `getattr(skill, "bounce_count", None)` + `getattr(skill, "spawn_count", None)` (Pattern P7 defensive boundary).
- `ExportSkill` in `schemas.py:21-38` would need `bounce_count: int | None = None` and `spawn_count: int | None = None` as additive optional fields. Backward-compatible; no existing consumer depends on these fields being absent.
- `season_exporter.py:_build_skill()` (lines 289-316) reads from the season JSON. The fields would need to be emitted by rocket's skill writer first.

**P1 W1.1 scope for star-lord:**
1. `migrations.py`: add `_V2_14` block: `ALTER TABLE abilities ADD COLUMN bounce_count INTEGER;` and `ALTER TABLE abilities ADD COLUMN spawn_count INTEGER;`
2. `recorder.py:_insert_skill()`: extend INSERT to include both columns, read via `getattr(skill, "bounce_count", None)` and `getattr(skill, "spawn_count", None)`
3. `schemas.py:ExportSkill`: add `bounce_count: int | None = None` and `spawn_count: int | None = None`
4. `season_exporter.py:_build_skill()`: add `bounce_count=skill_json.get("bounce_count")` and `spawn_count=skill_json.get("spawn_count")`
5. MIGRATION.md entry required (drax consumer obligation)
6. Matt authorization required for DB migration per ADR-006

This is a clean additive extension with no backward-compat risk. Total scope is approximately 4 files, ~20 lines of code change + 1 migration entry.

---

## 4. Schema Version v2.12 + v2.13 Cross-Check

**v2.12 fields — `spatial_fight_results` table:**
- Table creation confirmed LIVE in `migrations.py:_V2_12` (lines 860-916)
- 20 user fields + `id` PK: `fight_id`, `class_id`, `scenario_id`, `session_id`, `seed`, `winner`, `elapsed_s`, `player_kill`, `total_mob_count`, `mobs_killed`, `total_flanking_ticks`, `max_flanking_count`, `total_aoe_hits`, `aoe_hits_in_chokepoint`, `cone_hit_fraction`, `line_hit_fraction`, `circle_hit_fraction`, `geometry_type_dominant`, `wr_1d_fight`, `created_at`
- Migration is in MIGRATIONS list at line 968: `("2.12", _V2_12, ...)`
- Writer at `telemetry/spatial_recorder.py` (confirmed by file listing)
- AGENT_STATE.md confirms: "Production DB apply: table created; schema_meta 2.12 entry at 2026-05-19 10:19:50; 0 pre-existing rows — PASS"
- **Verdict: LIVE**

**v2.13 fields — `geometry_type_source` column on `spatial_fight_results`:**
- `ALTER TABLE spatial_fight_results ADD COLUMN geometry_type_source TEXT DEFAULT NULL;` confirmed in `migrations.py:_V2_13` (lines 918-939)
- `ExportSkill.spatial_geometry_type: str | None = None` confirmed in `schemas.py:33`
- `season_exporter.py:310` reads `skill_json.get("spatial_geometry_type")` with defensive fallback
- Migration is in MIGRATIONS list at line 969: `("2.13", _V2_13, ...)`
- AGENT_STATE.md confirms: "Production DB: migration applied 2026-05-19; column live; SCHEMA_VERSION '2.12' → '2.13'"
- **Verdict: LIVE**

**Recompose-hive P1 ratification fields — `floor_lock_recompose`, `working_modifier`, `floor_lock_detected`:**

These three fields appear in gamora's `simulation/MIGRATION.md` spec (lines 2333-2345) as new fields on the `recompose_attempts` telemetry structure and `ClassBalanceResult`. However:
- `migrations.py`: NO migration block for any of these three fields exists anywhere in the file (confirmed by explicit grep returning no output)
- `recorder.py`: NO read of `floor_lock_recompose`, `working_modifier`, or `floor_lock_detected` from any result object (confirmed by explicit grep returning no output)
- `class_balance_results` table: does NOT have columns for these fields

**DRIFT FINDING:** The gamora seam has specced `floor_lock_recompose`, `working_modifier`, and `floor_lock_detected` in `simulation/MIGRATION.md` (the Option B floor-lock recovery fields from the recompose-hive P1 ratification). These fields are NOT implemented in star-lord's telemetry schema or recorder. Jack-ryan's Phase 1 audit did not surface this specific telemetry gap as an LC; it is a cross-seam gap between gamora's Option B spec and star-lord's recorder implementation.

Per dispatch protocol § 7.4: this is NOT a new HIGH-risk LC (it is a known gap in an already-documented area — recompose-hive telemetry coverage), but it IS a drift that surfaces for P1 attention. Not blocking W0.4 completion. Routing to knight-rider for P1 dispatch scoping.

---

## 5. MEDIUM-Risk LCs — Star-Lord Seam Quick Scan

**LC-013 (Mage range constraint):** No star-lord exposure. The constraint is in `generation/b6_kit_builder.py` (rocket seam). The `class_fight_loadouts` table records per-fight range data via the V2.6 fields (`skill_range_m`, `range_band`), which measure the outcome but don't enforce the constraint.

**LC-015 (Doppelganger floor 0.30):** No star-lord schema exposure. The floor constant is in `simulation/balance_loop.py` (gamora). The `class_balance_results` table records `room_winrate` and per-tier WRs but does not record whether the 0.30 floor was active for a given fight.

**LC-016 (±25% per-fight variance):** No star-lord schema exposure. The variance is applied in `simulation/fight_engine.py` (gamora). Its effect is visible in the spread of `class_fight_loadouts.damage_dealt` values but is not tagged in telemetry.

**LC-017 (Gauntlet composition 6+6):** The `class_fight_loadouts` table records fights from all gauntlet slots. No column distinguishes PackProxy fights from non-pack fights (see LC-005 note above). When W0.9 ships (PackProxy retirement), star-lord will need a fight-type discriminator column.

**LC-018 (Energy homogeneity):** No direct star-lord schema exposure. The `abilities` table records `energy_cost_pct` (renamed from `mana_cost_pct` at schema 1.3) but does not record the resource-cycle shape that BC Axis 5 would measure.

**LC-019 (Cohesion gate not wired):** Confirmed absent from star-lord seam. No `cohesion_score`, `theme_cohesion_score`, or equivalent column exists in any telemetry table. This is consistent with LC-019's status as IMPLIED and explicitly deferred to Phase 2 (after mechanical BC measurement).

**LC-020 (Per-tier WR A1/A2 diagnostic-only):** The `class_balance_results` table records per-tier WRs (schema 2.9). These are the A3-convergence tier WRs. No separate A1/A2 diagnostic WR columns exist — the current schema does not distinguish A1/A2 diagnostic WRs from A3 primary convergence WRs. The recording matches the current designed intent (A3 primary; A1/A2 diagnostic-only with no separate persistence).

**LC-021 (Movement-modeling abstraction):** The `class_fight_loadouts.observed_movement_speed` column exists (schema 2.2; `migrations.py:_V2_2`). Currently writes NULL until rocket's movement_speed field and gamora's Stage A2 extension land. The schema is ready; the data is absent pending upstream work.

**LC-022 (Substrate-expansion archetype matrix gap):** The `seasonal_elements` table at `migrations.py:_V1_2:line 295` has a comment `-- 'fire', 'wind', 'water', 'earth'` as the role_slot values. The `record_seasonal_elements()` at `recorder.py:120-166` is already extended via D6 Coupling #9 to use `elements.slots.items()` (canonical-7-ready). The telemetry seam is ready for 7-substrate seasons; the slot values would expand to include `lightning`, `holy`, `shadow` when those substrates are active.

**LC-023 (Recompose gauntlet stripping PackProxy):** The `class_fight_loadouts` table records all fights including recompose-loop fights but has no column that identifies whether a fight was a recompose-loop evaluation vs convergence-loop evaluation. The three semantic contexts (recompose/convergence/full-telemetry) are indistinguishable in the current schema. BC measurement spec will need to source from specific fight subsets; the telemetry schema currently does not tag which context each fight came from.

**LC-024 (Dodger bin partial deferral):** No direct star-lord exposure. The sim's dodge mechanic is in gamora seam; telemetry records fight outcomes but not per-mechanic hit/miss resolution detail.

**LC-025 (Charge-stack bins deferred):** No direct star-lord exposure. The `abilities.effects` JSON could theoretically record `charge_stack` mechanics but there is no validation or tagging at the DB write boundary.

**LC-026 (Mana bug structural):** The `classes` table records `base_mana INTEGER` for all classes (schema 1.0). Non-mana classes would have this field populated if the mana bug is active, making the telemetry evidence directly queryable. Whether this field is populated for rage/combo/focus classes is an empirical question for jack-ryan's DB analysis, not a schema gap.

**LC-027 (Ailment-damage-signatures deferred):** No star-lord schema exposure. The effects schema records ailment entries in the `abilities.effects` JSON, but there is no distinction between a "primary" ailment effect and a "secondary damage signature" ailment.

**LC-028 (Single-word rule):** No star-lord schema exposure. The `seasonal_elements.element_name` field stores whatever name the selector emits, with no length or word-count validation at the DB write boundary.

**LC-030 (HP-cost skill variety gap):** The `abilities` table records `energy_cost_pct` but has no `cost_type` column to distinguish HP-cost skills from mana-cost skills. If the generation seam adds HP-cost skills, the telemetry schema cannot currently distinguish them from mana-cost skills at zero-percent.

---

## 6. Cross-Seam Boundary Check (R11(b) / ADR-004)

### LC-006 Cross-Seam Surface
- **Origin seam:** rocket (`element/selector.py`, `canonical/library_generator.py`) — jack-ryan Phase 1 flagged these sites; rocket W0.4 must verify
- **Star-lord boundary:** `llm/naming.py` — RESOLVED (cipher migration live)
- **Contract surface:** The cipher migration is complete in star-lord's LLM calls. Residual rocket-seam sites (`element/selector.py`, `canonical/library_generator.py`) are outside star-lord's scope but could still expose canonical-four labels in LLM contexts outside the naming pipeline (e.g., if the element selector makes its own LLM call exposing canonical labels). Rocket W0.4 must verify those two sites independently.

### LC-007 Cross-Seam Surface
- **Origin seam:** rocket (`generation/gear_schema.py:198-310`) — slot name definitions
- **Star-lord boundary:** `migrations.py:_V1_6` (telemetry persistence of slot names), `schemas.py:88-89` (export schema), `season_exporter.py:396` (export path)
- **Drax boundary:** Loadout JSON consumption of `slot` and `handedness` values
- **Contract:** Any LC-007 fix dispatch (Position C slot renaming per form-bias cadence) requires coordinated MIGRATION.md entries from rocket, star-lord, and drax in that sequence. Star-lord's obligation: update `gear_instances` table (new column or rename via table recreation), update `ExportGearItem`, update `_load_gear_pool()` in `season_exporter.py`.

### `floor_lock_recompose` / `working_modifier` / `floor_lock_detected` Cross-Seam Gap
- **Gamora seam:** Specced in `simulation/MIGRATION.md` (Option B floor-lock recovery)
- **Star-lord seam:** No corresponding telemetry migration or recorder read
- **Impact:** If gamora ships Option B and populates `floor_lock_recompose` on `ClassBalanceResult`, the recorder will silently drop it (no column exists). This is a P1-priority telemetry gap that should be addressed before gamora's Option B ships. Routing to knight-rider.

### LC-005 / W0.9 Cross-Seam Impact
- **W0.9 (PackProxy retirement):** When gamora retires PackProxy and routes swarm-tier through true multi-monster spatial sim, the `class_fight_loadouts` table will receive a different fight-data shape. Star-lord will need to add a `fight_context` or `gauntlet_mode` column to distinguish legacy PackProxy fights from true multi-monster fights in historical telemetry. This is a W0.9 → star-lord follow-on item.

---

## 7. Existing TODO Marker

One TODO exists in the star-lord seam that represents a deferred schema improvement:

- `recorder.py:736`: `# TODO(R3-impl): add fight_log_schema_version key to fight_log and upgrade this to WARN when version >= R3.` This is a Pattern P7 obligation for `skill_range_m` absence detection. The TODO requests a `fight_log_schema_version` key from gamora's fight log to enable version-gated WARN vs DEBUG logging. Not a blocking drift; documented for R3 follow-on work.

---

## 8. Summary — Verdicts

| LC | Star-Lord Seam Exposure | Verdict |
|---|---|---|
| LC-006 | `llm/naming.py` (cipher migration) | RESOLVED (star-lord seam) |
| LC-007 | `schemas.py:88-89`, `migrations.py:_V1_6`, `season_exporter.py:396` | VERIFIED (migration not yet shipped; code state confirmed) |
| LC-001 | Passive recorder (no enforcement) | NO STAR-LORD ACTION — rocket seam |
| LC-002 | Passive recorder (no bias) | NO STAR-LORD ACTION — rocket/gamora seam |
| LC-003 | Missing `floor_lock_*` fields | DRIFT-FROM-AUDIT (telemetry gap; see Section 4) |
| LC-008 | `naming.py:323` `stats.as_dict()` in name_class prompt | NEEDS-DOWNSTREAM-FIX (LLM visibility gap; separate dispatch) |
| LC-012 | No exposure | NO STAR-LORD ACTION — rocket seam |

---

## 9. Open Item for Knight-Rider

**Item 1 — `floor_lock_recompose` / `working_modifier` / `floor_lock_detected` telemetry gap:**
Gamora's Option B recompose-hive spec (in `simulation/MIGRATION.md`) defines three new fields that are not yet in star-lord's telemetry schema. If Option B ships before the telemetry migration, the fields will be silently dropped. Requesting a P1 star-lord dispatch to add these columns to `class_balance_results` (3 new nullable columns) before or concurrently with gamora's Option B implementation dispatch. Matt authorization required per ADR-006 for the SQL migration.

**Item 2 — W0.9 PackProxy retirement follow-on:**
When gamora's W0.9 (PackProxy retirement) ships, star-lord needs a `fight_context` discriminator column on `class_fight_loadouts` to preserve backward-compat with historical PackProxy rows while tagging new true-multi-monster rows. This is a W0.9 → star-lord follow-on; requesting knight-rider to include star-lord as a stakeholder in the W0.9 dispatch.

---

## 10. W1.13 + W0.8 Summary for P1

**W1.13 ArchiveEntry schema extension scope (P1 W1.X):**
- New table required: `archive_entries` (7 columns: `entry_id`, `bc_coordinate`, `node_subset`, `per_node_coefficients`, `scalar_modifier`, `per_tier_wr`, `cohesion_theme`, `visual_identity`, plus audit columns)
- No existing table can absorb these columns without semantic confusion
- Matt authorization required for DB migration per ADR-006
- Export schema change not needed until P3 (archive insertion phase)

**W0.8 `bounce_count` + `spawn_count` scope (P1 W1.1):**
- Additive: 2 nullable columns on `abilities` table
- 4 files: `migrations.py`, `recorder.py:_insert_skill()`, `schemas.py:ExportSkill`, `season_exporter.py:_build_skill()`
- ~20 lines code + 1 migration entry + MIGRATION.md entry
- Matt authorization required for DB migration per ADR-006
- No round-trip breakage risk (pure additive; Pattern P7 defensive getattr at recorder boundary)

---

## Completion Record

**Seam tag fired:** `star-lord/v1.15-w0-4-code-side-audit-1` on engine repo
**Deliverable also appended to:** `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/phase-2-code-side-verification.md`
**AGENT_STATE.md:** Updated
