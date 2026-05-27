# MIGRATION — SC-6b Substrate Weapon Enrichment (Cycle 14 Wave 0.5)

> **STATUS:** CURRENT (Cycle 14 Wave 0.5; ADR-004 cross-seam coordination record for SC-6b schema extension)

**Authored:** 2026-05-27
**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Authority:** Matt 2026-05-27 framing brief Q5 RATIFIED; SC-6 audit § 1.6 Path A; dispatch § Cross-seam contract change YES
**Owning seam:** elrond (substrate library; `weapon_sim_props` table)
**Consumer seam:** rocket (Phase 2c substrate binding at Wave 0.5); downstream gamora (consumes via rocket emission; no direct DB read)
**Companion docs:**
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md` (dispatch)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (audit basis)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (substrate weapon binding output spec) + § 4 (damage formulas)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-baseline-lut-math-2026-05-27.md` (LUT math-note)
- `agentic_orchestration/GOVERNANCE.md` ADR-004 (cross-repo coordination + MIGRATION.md requirement)

---

## 1. Migration scope

Additive schema extension to `weapon_sim_props` table in `~/Games/reincarnated-loadout/data/telemetry.db`. **NO destructive changes; no column renames; no row deletions.** Backwards-compatible — existing consumer queries continue to function; new columns surface for new consumers (rocket Phase 2c Wave 0.5+).

### 1.1 Tables affected

| Table | DB | Change |
|---|---|---|
| `weapon_sim_props` | `~/Games/reincarnated-loadout/data/telemetry.db` | ADD 5 columns (all NULLable; populated for v1_scope=1 rows; NULL elsewhere) |

### 1.2 Columns added

| Column | Type | Constraint (enforced at backfill / consumer) | Semantic |
|---|---|---|---|
| `base_physical_damage_l50` | REAL | non-NULL on v1_scope; positive value | Absolute physical damage at L50 cap, in HP points (mid-anchor: family_baseline × amplitude_mean) per doc 47 § 3.1 + § 4.2 |
| `spell_damage_modifier_pct` | REAL | non-NULL on v1_scope; range [0, 150] | `+%spell damage` modifier per doc 47 § 3.1 caster ranges (INT 30-150; WIS 30-120; STR/DEX 0-10) |
| `element_affinity_modifiers_json` | TEXT (JSON) | non-NULL on v1_scope; martial = `{}`; caster = `{}` OR `{"<element>": pct, ...}` | Per-element `+%damage` affinity per doc 47 § 3.1 caster element-specialization expectation |
| `to_skill_level_modifier_static` | TEXT (JSON) | NULL on `weapon_kind='category'`; non-NULL OR explicit-NULL on `weapon_kind IN ('unique','named_template')` per LLM-curation pass | Static `+to-skill-level` for unique-tier named weapons (substrate-attached identity; rocket per-instance roll layered atop) |
| `weapon_type_family` | TEXT | non-NULL on v1_scope; one of `['martial-heavy','martial-light','ranged','caster-arcane','caster-faith','hybrid']` | Doc 47 6-family enum; derived algorithmically per audit § 2.1 |

### 1.3 CHECK constraints

SQLite `ALTER TABLE ADD COLUMN` does NOT support adding CHECK constraints to existing tables (would require table-rebuild). **Constraint enforcement strategy:**

1. **Backfill-side**: SC-6b backfill SQL validates `weapon_type_family` values against the 6-enum before insert; rejects invalid values
2. **Consumer-side**: rocket Phase 2c substrate-binding query asserts the enum at read time; surfaces violations as Phase 2c errors per Discipline #8 schema validation at export boundaries
3. **Future strategy**: if a `weapon_sim_props_v2` table-rebuild lands (Phase D cleaning or post-Cycle-14 schema consolidation), CHECK constraint adds at that point

---

## 2. Backfill scope

| Field | Source / algorithm | Coverage | Effort |
|---|---|---|---|
| `weapon_type_family` | Algorithmic rule on `(primary_stat, proxy_range_class)` per audit § 2.1 mapping rule | 2,293 v1_scope rows (96.5% pure-algorithmic per audit § 2.1; ~81 edge cases default-fallback to most-common-family-by-primary_stat per dispatch Q-SC6b-4) | 1-2 hours |
| `base_physical_damage_l50` | LUT (math-note § 3) × `(damage_amplitude_min + damage_amplitude_max) / 2.0` | 2,293 v1_scope rows | 1 hour after `weapon_type_family` backfill (depends on it) |
| `spell_damage_modifier_pct` | `primary_stat` default: INT → uniform[30,150]; WIS → uniform[30,120]; STR/DEX → uniform[0,10] | 2,293 v1_scope rows | 0.5 hours |
| `element_affinity_modifiers_json` | Martial (STR/DEX) → `{}` (1,966 rows); caster (INT/WIS) → regex name-parse on `canonical_name` for 7 element terms (fire / water / earth / wind / lightning / holy / shadow + synonyms) (327 rows) | 2,293 v1_scope rows | 1-2 hours |
| `to_skill_level_modifier_static` | `weapon_kind='category'` → NULL (1,139 rows; rocket per-instance roll handles); `weapon_kind IN ('unique','named_template','shield','talisman','banner','horn')` → NULL pre-curation; LLM-curation deferred per dispatch Q-SC6b-3 (Q10 quality > timeline) | 2,293 v1_scope rows (1,139 NULL by design; ~1,005 deferred to follow-on curation pass) | 0.5 hours backfill + LLM-curation deferred |

**Total backfill: ~4-5 hours focused execution + LLM-curation pass deferred (multi-session per dispatch anti-stall # 3).**

---

## 3. Cross-seam impact + round-trip clause

### 3.1 Consumer: rocket Phase 2c (Wave 0.5)

Rocket's Phase 2c substrate-binding query reads `weapon_sim_props` joined with `weapon_knowledge_entries` on `weapon_id = id` to populate `character_json.gear_representative.main_weapon.*`. Post-SC-6b columns enable the 8-field round-trip per dispatch acceptance criteria amended by jack-ryan Gate-1 finding #2:

| character_json field | Source after SC-6b |
|---|---|
| `base_physical_damage` (stat-formula #1) | `wsp.base_physical_damage_l50 × ROLL(wsp.damage_amplitude_min, wsp.damage_amplitude_max) / amplitude_mean` (rocket gen-time lottery) |
| `spell_damage_modifier` (stat-formula #2) | `wsp.spell_damage_modifier_pct` |
| `element_affinity_modifiers` (stat-formula #3) | `wsp.element_affinity_modifiers_json` (parsed) |
| `to_skill_level_modifiers` (stat-formula #4) | `wsp.to_skill_level_modifier_static` if non-NULL, else rocket per-rarity-tier roll |
| `attribute_requirement` (stat-formula #5) | `wsp.primary_stat` (reused from existing column; no enrichment needed) |
| `weapon_type_family` (stat-formula #6) | `wsp.weapon_type_family` |
| `substrate_weapon_id` (identity #1) | `wsp.weapon_id` (= `weapon_knowledge_entries.id`) |
| `substrate_canonical_name` (identity #2) | `wke.canonical_name` |

### 3.2 Round-trip smoke clause (per ADR-004 + Gate-1 Amendment 2)

> Rocket Phase 2c substrate query consumes new `weapon_sim_props` columns; per-character `gear_representative.main_weapon` contains all 8 substrate weapon fields populated with non-null values for the substrate rows that drove selection. **NULL-policy exceptions:**
> - `to_skill_level_modifier_static` is NULL by design for `weapon_kind='category'` (1,139 rows; rocket per-instance roll handles); rocket emits character JSON `to_skill_level_modifiers` from per-instance roll, not from substrate NULL, so the character-JSON field is non-null even when substrate field is NULL
> - `element_affinity_modifiers_json` is `{}` (empty JSON object, non-NULL) for martial primary_stat=STR/DEX rows by design; character JSON field is non-null = `{}`

### 3.3 Consumer: gamora (Wave 0.5 damage_resolver)

No direct DB dependency. Gamora reads `character_json.gear_representative.main_weapon.*` emitted by rocket Phase 2c. **No upstream wait on elrond beyond SC-6b's Wave 0.5 landing.** Doc 47 § 4.2 + § 4.3 formulas consume the 6 stat-formula fields per skill `damage_scaling_type` routing.

### 3.4 Consumers not impacted

- **galadriel**: substrate weapon stat audit doesn't touch CV / aesthetic surface; `weapon_aesthetic` table unaffected
- **star-lord**: no telemetry schema change in engine repo; loadout DB enrichment doesn't propagate
- **drax**: loadout app reads what rocket emits

---

## 4. Rollback plan

If SC-6b backfill produces incorrect values OR rocket Pattern-A query surfaces calibration amendment requiring re-tune:

1. **Single-column rollback** (most common case — e.g., rocket prefers different `martial-heavy` baseline): `UPDATE weapon_sim_props SET base_physical_damage_l50 = <new_lut[family]> × (damage_amplitude_min + damage_amplitude_max) / 2.0 WHERE weapon_id IN (SELECT id FROM weapon_knowledge_entries WHERE v1_scope=1);` — re-runs in seconds against 2,293 rows
2. **Full backfill rollback**: `UPDATE weapon_sim_props SET base_physical_damage_l50 = NULL, spell_damage_modifier_pct = NULL, element_affinity_modifiers_json = NULL, to_skill_level_modifier_static = NULL, weapon_type_family = NULL WHERE weapon_id IN (SELECT id FROM weapon_knowledge_entries WHERE v1_scope=1);` — clears all 5 new columns; schema columns themselves remain
3. **Full schema rollback**: SQLite doesn't support `ALTER TABLE DROP COLUMN` natively pre-3.35; requires table-rebuild. If full schema rollback needed: `CREATE TABLE weapon_sim_props_pre_sc6b AS SELECT weapon_id, range_min_units, range_max_units, base_attack_speed, charge_time_s, hits_per_attack, aoe_radius_units, primary_stat, secondary_stat, damage_amplitude_min, damage_amplitude_max, sim_viable, sim_viability_notes, sim_verified_date FROM weapon_sim_props; DROP TABLE weapon_sim_props; ALTER TABLE weapon_sim_props_pre_sc6b RENAME TO weapon_sim_props;` (PRESERVES existing data; removes 5 new columns).

**Backup recommended pre-migration**: `cp ~/Games/reincarnated-loadout/data/telemetry.db ~/Games/reincarnated-loadout/data/telemetry.db.pre-sc6b-2026-05-27.bak` — captured pre-fire.

---

## 5. Rocket Pattern-A query (cross-seam coordination record)

Per dispatch § Pre-kickoff Q-SC6b-1: this query content captured in math-note § 5 + here for KR sub-agent routing OR for rocket to consume at Wave 0.5 round-trip smoke. **SC-6b backfill proceeds with Path A defaults per dispatch authorization; rocket amendments trigger single-column rollback per § 4.1 above.**

Query content: see `sc-6b-baseline-lut-math-2026-05-27.md` § 5 (Q1 = magnitude alignment with gauntlet-sim per-skill damage scale; Q2 = one-column mean-anchor vs two-column min/max; Q3 = hybrid baseline when Option C cells enter substrate).

**Status as of SC-6b backfill execution**: query content recorded; routed-via-MIGRATION.md (this doc) per hive-mind protocol § 5.5.4 file-write constraint pattern (KR captures sub-agent invocations on behalf of elrond when direct invocation tool not surfaced; OR rocket consumes at Wave 0.5 round-trip smoke kickoff). **Path A defaults stand absent rocket amendment.**

---

## 6. Decisions-log entry proposal

Per audit § 4.4 + ADR-002 (architectural commitment with cross-seam impact): SC-6b's commitment to substrate-side `base_physical_damage_l50` absolute-HP column warrants a decisions-log entry. **Proposed entry (elrond proposes; jack-ryan writes per decisions-log ownership):**

> **2026-05-27 — Substrate weapon base_physical_damage carries L50 absolute baseline at substrate layer (Path A vs Path B)**
>
> **Decision:** `weapon_sim_props.base_physical_damage_l50` is the authoritative substrate-side absolute physical damage at L50 cap (HP points). Computed at SC-6b backfill as `family_baseline × amplitude_mean` per `sc-6b-baseline-lut-math-2026-05-27.md` § 3. Rocket Phase 2c integrates the `damage_amplitude_min/max` lottery at gen time via per-instance amplitude_roll. Doc 47 § 4.2 `base` parameter consumes from substrate, not from engine-side calibration constants.
>
> **Reasoning:** Path A (substrate carries the magnitude) keeps the damage formula auditable end-to-end from substrate row → fight log per Discipline #11; locates the L50 baseline as a property of the weapon-as-substrate-object (the greatsword does 250 base because of what it IS, not what the engine assigns). Path B (engine-side calibration LUT) would lock magnitudes inside code where they're harder to inspect and harder to balance.
>
> **Alternatives considered:** Path B (engine-side calibration). Rejected per audit § 1.6 elrond recommendation on architectural-cleanliness grounds.
>
> **Status:** RATIFIED 2026-05-27 (Matt framing brief Q5 + SC-6 audit per-field disposition).
>
> **Related:** `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 + § 4; SC-6 audit; SC-6b dispatch + MIGRATION.md.

---

## 7. Sign-off

**Author:** elrond
**Status:** CURRENT — SC-6b cross-seam migration record. ADR-004 compliance: cross-seam contract change documented; consumer (rocket) round-trip clause defined; rollback plan captured.

**Cross-references:**
- Engineering disciplines: #1 math-before-code (LUT); #8 schema validation at export boundaries (rocket Phase 2c assertion); #11 empirical inspection (audit-grounded backfill); #14 internal-vs-generative schema separation (substrate library is internal; rocket emits generative-facing JSON); #18 methodology-before-execution (LUT gates backfill); #38 damage-scaling-path discipline (substrate-side prerequisite)
- Hive-mind protocol § 4 (seam decision-routing: rocket consultation via Pattern-A query content in § 5); § 5.5.4 (file-write constraint pattern: query content routed via MIGRATION.md)

**For Wave 0.5 cross-seam coordination:** rocket Phase 2c reads SC-6b new columns; round-trip smoke at character JSON emission validates 8-field substrate→character pipeline.
