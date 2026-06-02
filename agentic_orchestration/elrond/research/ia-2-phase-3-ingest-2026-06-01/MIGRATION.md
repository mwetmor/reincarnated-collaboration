# MIGRATION — IA-2 Phase 3 Weapon-Substrate Ingest + period_tag Schema Extension

> **STATUS:** CURRENT (IA-2 Phase 3; ADR-004 cross-seam coordination record for additive `period_tag` schema extension + 125-weapon ingest + retroactive-primary-tagging methodology)

**Authored:** 2026-06-01
**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Authority:**
- Matt 2026-06-01 strategic reset + pre-commitment ratification LOCK E (Phase 3 elrond autonomous)
- LOCK J § 5 (additive `period_tag` schema autonomous within seam authority)
- jack-ryan IA-2.P3 Gate-1 PASS-with-INFO (commit `1cd73a5`)

**Owning seam:** elrond (substrate library; `weapon_knowledge_entries` table)
**Consumer seams:** rocket (Phase 2c substrate binding); star-lord (telemetry export); drax (loadout app consumer)

**Companion docs:**
- `agentic_orchestration/dispatches/2026-06-01-elrond-ia-2-phase-3-weapon-substrate-ingest.md` (dispatch)
- `agentic_orchestration/elrond/audits/2026-06-01-magic-weapons-across-periods-audit.md` (Phase 1 audit; § 7.4 retroactive-tagging methodology surface)
- `agentic_orchestration/gandalf/notes/2026-06-01-ia-2-phase-2-anchors-batch.json` (102 gandalf anchors; binding ingest source)
- `agentic_orchestration/legolas/research/ia-2-phase-2-supplementary-crawl-2026-06-01/` (23 legolas crawl entries; binding ingest source)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 IMMUTABLE Architecture A; 7 rotating primaries)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3 (Option α/β/C; INFO-2 caster-class consistency)
- `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md` (LOCK E + LOCK J § 5 + escape clause)
- `agentic_orchestration/qa/findings/2026-06-01-ia-2-p3-and-ia-3-p1-gate-1.md` (combined Gate-1 PASS-with-INFO)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md` (prior MIGRATION.md pattern reference)
- `agentic_orchestration/research/scripts/ia2_phase3_weapon_substrate_ingest.py` (ingest script — reproducible)
- `agentic_orchestration/GOVERNANCE.md` ADR-004 (cross-seam coordination + MIGRATION.md requirement)

---

## 1. Migration scope

Three operations on `weapon_knowledge_entries` in `~/Games/reincarnated-loadout/data/telemetry.db`:

1. **Additive schema extension** — `period_tag` column (TEXT, nullable, enum-by-contract)
2. **125-weapon ingest** — 102 gandalf anchors + 23 legolas crawl
3. **Retroactive-primary-tagging pass** — 137 magic-weapon-eligible primary-unattributed substrate rows tagged with primary-element associations per audit § 7.4

**NO destructive changes; no column renames; no row deletions.** Backwards-compatible — existing consumer queries continue to function; new columns + structured-properties fields surface for new consumers.

### 1.1 Tables affected

| Table | DB | Change |
|---|---|---|
| `weapon_knowledge_entries` | `~/Games/reincarnated-loadout/data/telemetry.db` | ADD `period_tag` column (nullable; default NULL for legacy rows); INSERT 125 IA-2 entries; UPDATE 137 rows' `structured_properties` JSON (retroactive-tagging pass) |
| `weapon_sim_props` | (same DB) | UNCHANGED (IA-2 entries have no sim-prop rows yet; future SC-6b-equivalent backfill could add) |

### 1.2 Columns added

| Column | Type | Constraint (enforced at contract / consumer) | Semantic |
|---|---|---|---|
| `period_tag` | TEXT | enum: `ancient` \| `medieval` \| `modern` \| NULL (for legacy pre-ingest rows) | Per LOCK J § 5; coarse-grained IA-2 period bin orthogonal to existing `historical_period_canonical` (which is 8-enum fine-grained). Coarse bin enables IA-2 / WS2-style queries without joining keyword logic. |

**SQLite CHECK note:** `ALTER TABLE ADD COLUMN` does not support adding CHECK constraints to existing tables (would require table-rebuild). **Constraint enforcement strategy:**
1. **Ingest-side**: ingest script asserts `period_tag` against the 3-enum before INSERT; rejects invalid values
2. **Consumer-side**: rocket / star-lord / drax queries SHOULD validate the 3-enum at read time; emit Phase 2c errors on violation per Discipline #8
3. **Future strategy**: if a `weapon_knowledge_entries_v2` table-rebuild lands (Phase D cleaning or post-Cycle-14 schema consolidation), CHECK constraint adds at that point

### 1.3 structured_properties JSON fields added (NEW data via JSON; not first-class columns)

Per LOCK J § 5 the autonomous schema extension is **`period_tag` only**. Adding `primary_element` / `cultural_tradition` / `form` / `register` as first-class columns would be a SEMANTIC contract change requiring Matt + gandalf approval per ADR-002 Tier A. Per Discipline #41 (substrate-led; minimal-additive) AND following the existing `engine_authored_gap_fill_v1` encoding convention, IA-2 metadata is stored in `structured_properties` JSON.

**For IA-2-ingested rows (125 entries), structured_properties keys:**

| Key | Type | Source | Semantic |
|---|---|---|---|
| `primary_element` | string (7-enum: fire/water/earth/wind/lightning/holy/shadow) | gandalf/legolas JSON `primary_element` | Q18-rotating-primary attribution |
| `cultural_tradition` | string | gandalf/legolas JSON | Free-text cultural lineage (more specific than `cultural_lineage_canonical` enum) |
| `form` | string | gandalf/legolas JSON | Weapon form description (richer than `weapon_kind` enum) |
| `register` | string | gandalf/legolas JSON | Free-text register (mythological/divine/epic/etc.; richer than `register_canonical` enum) |
| `substrate_validation_lineage` | string | gandalf/legolas JSON | Anchor lineage tag (gandalf-authored-magic-anchor-{period}-2026-06-01 OR legolas-crawl-magic-supplementary-{period}-2026-06-01) |
| `novel_design_flag` | bool | gandalf/legolas JSON | Whether the entry is a novel-design composition vs canonical reference |
| `ia2_ingest_lineage` | string | this script | `"gandalf-anchor"` \| `"legolas-crawl"` |
| `design_rationale` | string (gandalf-only) | gandalf JSON | Design-rationale narrative |
| `source_citation` | string (legolas-only) | legolas JSON | Published source citation |
| `weapon_id_source` | string (gandalf-only) | gandalf JSON | Source weapon_id from gandalf JSON (round-tripping anchor) |

**For retroactive-tagged rows (137 entries), structured_properties keys:**

| Key | Type | Semantic |
|---|---|---|
| `primary_element_retroactive` | string \| NULL | Inferred primary-element attribution; NULL when multi-match ambiguity flagged |
| `primary_element_retroactive_confidence` | float [0, 1] | 1.0 = single-keyword match; 0.75 = name-only-priority multi-match; 0.5 = uncertain multi-match |
| `primary_element_retroactive_lineage` | string | `"elrond-retroactive-primary-tag-2026-06-01"` |
| `primary_element_retroactive_uncertain` | bool | True for multi-match ambiguity (flagged for future review) |
| `primary_element_retroactive_candidates` | list[string] | All matched primaries (for uncertain rows; informs follow-on disambiguation) |
| `primary_element_retroactive_matching_policy` | string | `option_alpha_martial_5tuple` \| `option_beta_caster_attribute_level` \| `option_c_cross_attribute` per row's `proxy_attribute_class` (INFO-2 consistency) |

### 1.4 INFO-2 caster-class consistency (per Gate-1)

Per INFO-2 from jack-ryan Gate-1 PASS-with-INFO + canonical composition policy v1 § 3:

- **Option α — Martial cells** (STR or DEX primary; physical-element coupling; 5-tuple substrate-binding at Phase 2)
- **Option β — Caster cells** (INT or WIS primary; non-physical-element coupling; attribute-level match at Phase 2)
- **Option C — Cross-attribute hybrid cells** (STR_or_WIS; cross-attribute permitted with ω-penalty)

Retroactive-primary-tagging respects this routing by recording `matching_policy` per row based on `proxy_attribute_class`:
- STR / DEX → `option_alpha_martial_5tuple`
- INT / WIS / INT_or_WIS / WIS_or_INT → `option_beta_caster_attribute_level`
- STR_or_WIS → `option_c_cross_attribute`
- NULL / unknown → `option_beta_caster_attribute_level` (safe default; downstream consumers handle uncertainty)

**Semantic clarification (INFO-2 nuance):** the substrate `primary_element_retroactive` tag identifies the row's elemental coding (e.g., Mjölnir → lightning). The `matching_policy` preserves the martial-vs-caster routing distinction (Mjölnir's `proxy_attribute_class` is martial → STR-coded; matching_policy = Option α). Downstream consumers (rocket, gamora) use `matching_policy` to route caster-vs-martial behavior; `primary_element_retroactive` to route flavor/element behavior. **No STR-coded melee row has been retroactively tagged with caster-routing semantics.** This preserves Discipline #41 (substrate-led) AND Option α/β/C separation.

---

## 2. Backfill scope

| Op | Source / algorithm | Coverage | Effort |
|---|---|---|---|
| `period_tag` extension | `ALTER TABLE ADD COLUMN period_tag TEXT` | Schema-only; 0 rows affected (column defaults NULL for legacy) | <1 second |
| Gandalf anchor INSERT | 102 entries from `2026-06-01-ia-2-phase-2-anchors-batch.json` (commit `07191ee`) | 102 rows inserted; `period_tag` populated per JSON `period` field | ~1 second |
| Legolas crawl INSERT | 23 entries from 3 JSONL files (commit `6bb68b2`) | 23 rows inserted; `period_tag` per file (9 ancient + 9 medieval + 5 modern per INFO-1) | ~1 second |
| Retroactive-primary-tagging | Scan 7,590 ANCIENT+MEDIEVAL rows; filter to magic-weapon-eligible per audit § 1.3; Q18 vocabulary-match → primary attribution; respect INFO-2 caster-class consistency | 137 rows tagged (127 high-confidence + 10 uncertain multi-match); 543 magic-eligible rows had no vocabulary signal; 6,839 not magic-eligible per audit criteria; 71 already had primary signal | ~2 seconds |

**Total backfill execution: <10 seconds.**

---

## 3. Cross-seam impact + round-trip clause

### 3.1 Consumer: rocket Phase 2c (substrate binding)

Rocket's Phase 2c substrate-binding query reads `weapon_sim_props` joined with `weapon_knowledge_entries` (see `src/reincarnated/generation/substrate_weapon_binding.py`). Post-IA-2.P3 ingest:

**Backward-compat (no rocket code change required):**
- New `period_tag` column is additive; existing queries ignore it; legacy queries continue to function
- IA-2 entries have `v1_scope = 0`; rocket's `WHERE v1_scope = 1` filter excludes IA-2 entries from Phase 2c binding by default (preserves v1 scope behavior; IA-2 entries enter v1+ scope post-validation)
- Existing `engine_authored_gap_fill_v1` row count preserved (43 rows; smoke-test verified)

**Optional forward-compat consumption (rocket-side adoption when ready):**
- Rocket may query `period_tag` to bucket weapons by IA-2 period (e.g., for period-coherent kit composition at Phase 5 cohesion-judge)
- Rocket may read `structured_properties.primary_element` for IA-2 entries to route flavor-element bindings
- Rocket may read `structured_properties.primary_element_retroactive` for legacy magic-weapon rows (where `confidence ≥ 0.75`) to route legacy weapons to Q18 primaries
- Rocket SHOULD respect `structured_properties.primary_element_retroactive_matching_policy` to route Option α/β/C correctly per INFO-2

### 3.2 Round-trip smoke clause (per ADR-004)

> Rocket's existing substrate-binding query continues to round-trip unchanged. Smoke-test (this MIGRATION.md § 4) verifies:
> - `weapon_knowledge_entries` legacy SELECT works
> - `weapon_knowledge_entries JOIN weapon_sim_props` works
> - `engine_authored_gap_fill_v1` row count preserved (43)
> - `period_tag` is queryable
> - 90,220 legacy rows have `period_tag = NULL` (additive, non-destructive)
> - Total row count: 90,345 (90,220 pre-ingest + 125 IA-2 ingest)

**Round-trip smoke result:** ALL CHECKS PASS (per `ingest-summary-stats.json` § `step_5_smoke_test_backward_compat`).

### 3.3 Consumer: star-lord (engine telemetry export)

No direct DB write contract on `weapon_knowledge_entries`; star-lord reads weapon-substrate-derived character JSON emitted by rocket Phase 2c. **No upstream wait on elrond beyond IA-2.P3 landing.**

Optional: if star-lord telemetry-export schemas want to surface `period_tag` or `primary_element` at character-JSON layer for downstream analytics, a small additive emission (Phase 5 cohesion-judge output) could include these. Out of scope for this MIGRATION.

### 3.4 Consumer: drax (loadout app)

Drax consumes character JSON emitted by rocket. No direct DB dependency. Backward-compat preserved; IA-2 entries surface to drax once rocket adopts forward-compat consumption (per § 3.1).

### 3.5 Consumer: galadriel (visual benchmark; CV pipeline)

No impact. `weapon_aesthetic` table unaffected. IA-2 entries do not yet have visual aesthetic data (gates on future visual-benchmark coverage if needed).

### 3.6 Consumers NOT impacted

- `weapon_sim_props` — unchanged; no schema mutation
- `weapons` (operational weapon table; distinct from `weapon_knowledge_entries` substrate) — unchanged
- `seasons`, `classes`, `gear` (engine telemetry tables) — unchanged
- `substrate_density`, `weapon_tags`, `weapon_sources`, `weapon_readiness`, `weapon_aesthetic` — unchanged
- `cycle13_characters.db` (loadout-side season data) — unchanged

---

## 4. Backward-compat verification (smoke-test)

Per ingest script § `step_5_smoke_test_backward_compat`:

| Check | Method | Pre-ingest | Post-ingest | Result |
|---|---|---|---|---|
| Legacy column read | `SELECT id, canonical_name, source_library, historical_period_canonical, register_canonical, weapon_kind, proxy_attribute_class, v1_scope FROM weapon_knowledge_entries LIMIT 5` | OK | OK | PASS |
| Substrate weapon binding JOIN | `SELECT wke.id, wke.canonical_name, wsp.primary_stat, wsp.weapon_type_family FROM weapon_knowledge_entries wke JOIN weapon_sim_props wsp ON wsp.weapon_id = wke.id WHERE wke.v1_scope = 1 LIMIT 5` | OK | OK | PASS |
| `engine_authored_gap_fill_v1` count preserved | `SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library = 'engine_authored_gap_fill_v1'` | 43 | 43 | PASS |
| `period_tag` queryable | `SELECT period_tag, COUNT(*) FROM weapon_knowledge_entries WHERE period_tag IS NOT NULL GROUP BY period_tag` | (column absent) | `{ancient: 33, medieval: 38, modern: 54}` (= 125; matches ingest count) | PASS |
| Legacy rows `period_tag = NULL` | `SELECT COUNT(*) FROM weapon_knowledge_entries WHERE period_tag IS NULL` | (column absent) | 90,220 (= pre-ingest baseline; additive verified) | PASS |
| Total row count | `SELECT COUNT(*) FROM weapon_knowledge_entries` | 90,220 | 90,345 (= 90,220 + 125) | PASS |

**ALL 6 BACKWARD-COMPAT CHECKS PASS.**

---

## 5. Rollback plan

If IA-2.P3 ingest produces incorrect values OR consumer feedback surfaces issues:

### 5.1 Single-row / per-source rollback (most common)

`DELETE FROM weapon_knowledge_entries WHERE source_library = 'gandalf-authored-magic-anchor-ancient-2026-06-01';` etc. — removes specific lineage cohort. Per-lineage rollback at any granularity.

### 5.2 Full IA-2 ingest rollback

```sql
DELETE FROM weapon_knowledge_entries
WHERE source_library LIKE 'gandalf-authored-magic-anchor-%-2026-06-01'
   OR source_library LIKE 'legolas-crawl-magic-supplementary-%-2026-06-01';
```
Removes all 125 IA-2 entries. Schema column `period_tag` and retroactive-tagging metadata REMAIN; see § 5.3 / § 5.4 for those.

### 5.3 Retroactive-tagging-only rollback

Selective UPDATE removing retroactive-tag fields from `structured_properties`:

```sql
-- Pseudo; requires JSON path operations
UPDATE weapon_knowledge_entries
SET structured_properties = json_remove(structured_properties,
    '$.primary_element_retroactive',
    '$.primary_element_retroactive_confidence',
    '$.primary_element_retroactive_lineage',
    '$.primary_element_retroactive_uncertain',
    '$.primary_element_retroactive_candidates',
    '$.primary_element_retroactive_matching_policy')
WHERE json_extract(structured_properties, '$.primary_element_retroactive_lineage') = 'elrond-retroactive-primary-tag-2026-06-01';
```

### 5.4 Full schema rollback (drop `period_tag` column)

SQLite supports `ALTER TABLE DROP COLUMN` since 3.35 (Mar 2021). Check SQLite version (`SELECT sqlite_version();`) before relying on this.

Pre-3.35 fallback: table-rebuild preserving existing data sans `period_tag`:
```sql
-- omit period_tag from new table; SELECT all other columns
-- (specific column list elided here for brevity; see schema dump pre-migration)
```

### 5.5 Backup recovery

Full DB backup captured pre-migration:
```bash
~/Games/reincarnated-loadout/data/telemetry.db.pre-ia-2-phase-3-2026-06-01.bak
```
Restore: `cp ~/Games/reincarnated-loadout/data/telemetry.db.pre-ia-2-phase-3-2026-06-01.bak ~/Games/reincarnated-loadout/data/telemetry.db`.

---

## 6. Migration order

1. **Schema extension** — `ALTER TABLE weapon_knowledge_entries ADD COLUMN period_tag TEXT` (✓ DONE)
2. **Gandalf anchor INSERT** — 102 rows; populate `period_tag` per JSON `period` (✓ DONE)
3. **Legolas crawl INSERT** — 23 rows; populate `period_tag` per file (✓ DONE)
4. **Retroactive-primary-tagging pass** — UPDATE 137 magic-weapon-eligible primary-unattributed rows' `structured_properties` JSON (✓ DONE)
5. **Backward-compat smoke-test** — verify 6 checks (✓ DONE; ALL PASS)
6. **Consumer-side optional adoption** — rocket / star-lord / drax may read new fields when ready (NOT REQUIRED for backward-compat; their existing queries continue to work)

---

## 7. Decisions-log entry proposal

Proposed entry per `agentic_orchestration/operating-procedures/elrond.md` § decision-routing → jack-ryan owns decisions-log writes.

```
### 2026-06-01 — IA-2.P3 weapon-substrate ingest + period_tag schema extension

**Decision:** Authored MIGRATION.md + ingested 125 weapons (102 gandalf + 23 legolas)
into weapon_knowledge_entries; additive period_tag column added (LOCK J § 5);
137 retroactive primary-element tags applied to magic-weapon-eligible legacy rows
(audit § 7.4); INFO-2 caster-class consistency preserved via per-row matching_policy
recording (Option α/β/C per proxy_attribute_class).

**Reasoning:** LOCK E (Phase 3 elrond autonomous) + LOCK J § 5 + jack-ryan Gate-1
PASS-with-INFO. Substrate-led discipline (#41) preserved by storing primary_element
as structured_properties JSON rather than first-class column (which would require
ADR-002 Tier A approval). Backward-compat verified via 6 smoke-tests.

**Alternatives considered:**
- Add primary_element as first-class column — REJECTED as semantic contract change beyond LOCK J § 5 autonomous scope
- Skip retroactive-tagging — REJECTED per audit § 7.4 + dispatch § 2.4 authorization
- Tag retroactively without matching_policy — REJECTED per INFO-2 + composition policy v1 § 3

**Status:** PROPOSED for jack-ryan ratification at IA-2 Phase 4 validation pass.

**Related:** ADR-002 Tier C (data architecture decisions; elrond seam authority);
ADR-004 (MIGRATION.md cross-seam protocol); Q18 IMMUTABLE Architecture A;
weapon-substrate-composition-policy-v1 § 3 (Option α/β/C); audit § 7.4
(retroactive-tagging methodology surface).
```

Decisions-log entry routing: knight-rider → jack-ryan per ADR-004 + Matt 2026-05-23 hive-mind decision-routing directive.

---

## 8. Sign-off

**Author:** elrond (data steward seam)
**Authority chain:**
- Matt 2026-06-01 strategic reset directive
- LOCK E (Phase 3 elrond autonomous)
- LOCK J § 5 (additive period_tag schema autonomous)
- jack-ryan IA-2.P3 Gate-1 PASS-with-INFO (commit `1cd73a5`)

**Status:** CURRENT — IA-2 Phase 3 ingest COMPLETE. Awaiting IA-2 Phase 4 substrate-coverage validation pass per LOCK E autonomous.

**Disciplines composed:**
- Discipline #8 (schema validation at boundaries) — contract-side enum validation for `period_tag`
- Discipline #10 (attribution clarity) — per-row `substrate_validation_lineage` + `matching_policy` + `primary_element_retroactive_lineage` fields
- Discipline #41 (substrate-led) — minimal-additive schema extension; primary_element stored in JSON rather than first-class column
- Discipline #42 (framing-audit) — § 1.4 INFO-2 nuance explicitly documented (substrate primary tag ≠ caster-routing semantic shift)
- Discipline #25 (semantic-layer rep-audit / marginal-lineage tagging) — retroactive-tagging methodology preserves provenance per § 7

---

**End of IA-2 Phase 3 weapon-substrate ingest MIGRATION.md.**
