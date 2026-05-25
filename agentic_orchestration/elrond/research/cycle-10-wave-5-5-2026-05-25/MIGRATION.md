# MIGRATION — Cycle 10 Wave 5.5 — Phase 0c Tier-A Subtype + Mode-C Eviction

**Date:** 2026-05-25
**Owner:** elrond (substrate seam)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-phase-0c-and-mode-c-eviction.md`
**Pattern:** Additive UPDATES-ONLY (no schema change; no ALTER TABLE)
**Precedent:** ADR-004 additive pattern + Wave 5 Phase 0a precedent (`cycle-10-stage-3-2026-05-25/MIGRATION.md`) + Sidecar B + Phase D + Phase 2 additive patterns
**Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Table:** `weapon_knowledge_entries`

---

## 1. Scope

Wave 5.5 is an updates-only pass on existing columns. **No new columns; no schema change.** All updates land on three existing columns:

1. `weapon_kind_classified_subtype` (TEXT, additive column landed Phase 0a) — populated on 7,943 Tier-A NULL-subtype rows
2. `v1_scope` (BOOLEAN, column landed Phase 2) — downgraded from `1` to `0` on 791 rows (761 Phase 0c + 30 Part B Mode-C)
3. `v1_scope_composition_trace` (TEXT, JSON column landed Phase 2) — appended (not overwritten) with new trace records on 791 rows

---

## 2. Phase 0c — `weapon_kind_classified_subtype` population

### 2.1 Update pattern

For each row matching `quality_tier='A' AND weapon_kind_classified_subtype IS NULL`:

```sql
UPDATE weapon_knowledge_entries
   SET weapon_kind_classified_subtype = <classifier_output>
 WHERE id = <id>;
```

### 2.2 Row count

7,943 rows updated. Pre: `quality_tier='A' AND weapon_kind_classified_subtype IS NULL` = 7,943; Post: same query = 0.

### 2.3 Classifier code

`classify_tier_a_subtype.py` (this directory). Per-source heuristic rules driven by `structured_properties` source-side signal plus name-token override list. Heuristic only; no LLM cost.

### 2.4 Per-source subdivision

See `phase-0c-tier-a-subtype-classification.md` § 1.3 + § 3 for per-source per-subtype distribution.

### 2.5 Source signal preserved

Each row's `weapon_kind_classified_subtype` value can be re-derived from its `structured_properties` JSON + canonical_name. The classifier is deterministic for any given input row state; re-execution against the same substrate produces identical output. Reversibility per ADR-004 spirit: classifier code + per-row rationale JSON (`phase-0c-tier-a-subtype-classification.json`) preserves full trace.

---

## 3. Phase 0c v1_scope downgrade

### 3.1 Update pattern

For each Tier-A v1_scope=1 row that classifies to a D1c-excluded subtype (siege_vehicle / armor_body_or_head / accessory_horse_or_equipment / art_object / other / ammo_consumable):

```sql
UPDATE weapon_knowledge_entries
   SET v1_scope = 0,
       v1_scope_composition_trace = <appended_json>
 WHERE id = <id>;
```

### 3.2 Row count

761 rows downgraded. Pre: `quality_tier='A' AND v1_scope=1` = 1,431; Post: same query = 670.

### 3.3 Trace JSON shape (appended, not overwritten)

```json
{
  "<existing_trace_fields_preserved>": "...",
  "wave_5_5_downgrade": {
    "rule": "d1c_excluded_scope_deferred_tier_a_post_phase_0c",
    "subtype_classified": "<one of: siege_vehicle | armor_body_or_head | accessory_horse_or_equipment | art_object | other | ammo_consumable>",
    "subtype_classifier_rationale": "<per-row rationale string from classifier; see phase-0c-tier-a-subtype-classification.json>",
    "previous_v1_scope": 1
  }
}
```

Original trace.rule preserved (e.g., "tier_a_preferred"). New `wave_5_5_downgrade` field added at top-level of the JSON. Full provenance maintained.

### 3.4 Per-subtype downgrade counts

| Subtype | Downgrade count |
|---|---:|
| armor_body_or_head | 242 |
| siege_vehicle | 197 |
| other | 120 |
| accessory_horse_or_equipment | 78 |
| ammo_consumable | 70 |
| art_object | 54 |
| **Total** | **761** |

---

## 4. Part B — Mode-C-by-semantics SQL eviction

### 4.1 Update pattern

For each row matching gandalf sign-off § 3 Condition 3 SQL signature (VERBATIM; see `mode-c-semantics-eviction.md` § 1):

```sql
UPDATE weapon_knowledge_entries
   SET v1_scope = 0,
       v1_scope_composition_trace = <appended_json>
 WHERE id = <id>;
```

### 4.2 Row count

30 rows evicted. Pre Part B: v1_scope=1 total = 2,281; Post Part B: v1_scope=1 total = 2,251.

### 4.3 Trace JSON shape (appended)

```json
{
  "<existing_trace_fields_preserved>": "...",
  "wave_5_5_mode_c_eviction": {
    "rule": "mode_c_by_semantics_evicted_wave_5_5",
    "sql_signature_authority": "gandalf sign-off `2026-05-25-stage-3-distribution-report-sign-off.md` § 3 Condition 3 VERBATIM",
    "previous_v1_scope": 1,
    "register_canonical": "<value>",
    "historical_period_canonical": "<value>",
    "cultural_lineage_canonical": "<value>",
    "named_mythological_match": "<value>"
  }
}
```

If a row was Phase-0c-downgraded AND Mode-C-evicted (none in this run; Phase 0c handles D1c-subtype-by-classification while Mode-C SQL handles D1a/D1b-subtype-allowed-but-still-mode-C — disjoint sets in practice), both trace records would be present at top-level of the JSON.

### 4.4 Per-period breakdown

See `mode-c-semantics-eviction.md` § 2.1.

---

## 5. Schema change

**NONE.** Wave 5.5 is updates-only against three existing columns (`weapon_kind_classified_subtype`, `v1_scope`, `v1_scope_composition_trace`). No `ALTER TABLE`, no new columns, no CHECK constraint changes.

---

## 6. Pre-Wave-5.5 DB backup

`backups/telemetry.db.pre-wave-5-5` (this directory; 213 MB; gitignored per Phase 0a precedent — see `.gitignore` in `backups/`).

Reversion path: restore the backup file over `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` and Wave 5.5 effects are fully reverted (no schema change; all updates revert to pre-Wave-5.5 state).

---

## 7. Round-trip + cross-seam impact

**Round-trip: NOT APPLICABLE** per Principle 6 trigger-type table — substrate-only updates; no fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; no engine code touched.

No cross-seam round-trip required.

---

## 8. Downstream consumer impact

Downstream consumers that query the substrate DB should be aware:

1. **`weapon_kind_classified_subtype` is now populated for Tier-A rows** (in addition to Tier-S per Phase 0a). Queries that previously branched on `weapon_kind_classified_subtype IS NULL AND quality_tier='A'` will now match zero rows. Phase 0c populated all 7,943 Tier-A rows.

2. **`v1_scope=1` total has shifted 3,042 → 2,251** (net -791). Downstream cells / archetypes that referenced specific counts pre-Wave-5.5 should re-query.

3. **`v1_scope_composition_trace` JSON shape extended** with two new optional top-level fields: `wave_5_5_downgrade` (on 761 rows) + `wave_5_5_mode_c_eviction` (on 30 rows). Pre-existing fields preserved. Consumers reading the trace should JSON-parse and tolerate new fields.

4. **No engine code consumes substrate DB directly** (engine telemetry vs substrate are separate concerns per ADR-004). Substrate consumers are: elrond Phase 2 sampler (will need re-fire if knight-rider routes Phase 2 micro-sample); gandalf re-audit; Wave 6 Stage 3.5 dispatch (uses cleaned v1_scope as input); Stage 4 mechanical-tagging dispatch (uses cleaned v1_scope as input).

5. **Tier-B + Tier-C rows have `weapon_kind_classified_subtype = NULL`** still. Wave 5.5 did not extend the classifier to those tiers. Future stages may.

---

## 9. Cross-references

- Phase 0a precedent (Tier-S subtype classifier): `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/MIGRATION.md`
- Phase 2 v1_scope materialization: same dir, `populate_v1_scope.py` + `MIGRATION.md` Phase 2 section
- ADR-004 cross-seam coordination + additive pattern: `agentic_orchestration/GOVERNANCE.md`
- Composition policy v1: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- gandalf sign-off § 3 Conditions: `agentic_orchestration/gandalf/notes/2026-05-25-stage-3-distribution-report-sign-off.md`

---

## 10. Sign-off

**Author:** elrond (substrate seam; Wave 5.5)
**Date:** 2026-05-25
**Authority:** dispatch FIRE-READY + ADR-004 additive pattern (updates-only; no schema change)
**Status:** Wave 5.5 migration complete; substrate DB updated; pre-Wave-5.5 backup retained for reversion if needed.
