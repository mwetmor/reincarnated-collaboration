# Dispatch — 2026-06-02 — EAA-3 — Kit-space output schema (additive)

**From:** knight-rider (orchestrator)
**Primary owner:** rocket (engine emit schema; generation seam)
**Co-owners:** elrond (data layer / ingest schema) + star-lord (output pipeline; export seam)
**Cycle:** cycle-16-eaa-engine-architectural-amendment (Phase 1)
**Authority:** Matt 2026-06-02 Pattern B substantive design session + Locks A-P (LOCK K active for engine schema design authority)
**Wave tag:** `EAA-3`
**Wave-open dispatch:** `agentic_orchestration/dispatches/2026-06-02-cycle-16-eaa-engine-architectural-amendment-wave-open.md` (READ FIRST)
**State file:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
**Wave-open Gate-1 finding:** `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` (PASS-with-INFO)
**Estimated horizon:** ~2-3 sessions including jack-ryan Gate cycles
**Gates:** jack-ryan Gate-1 pre-fire on this dispatch + Gate-2 on schema spec

---

## 1. Authoritative reading (READ IN ORDER before any action)

1. `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 (continuous kit space properties) + § 3.4 (chronicle) — binding
2. `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` — pool.json schema patterns reference (lineage tag patterns per WS1A.Q18 model)
3. Existing season manifest schema (e.g., a recent season_000XXX manifest.json) — backward-compat reference
4. Wave-open dispatch (see header) — chain context

---

## 2. Scope

Design the **per-kit JSON entry schema** for the continuous kit space. This is NOT a per-season manifest schema; the kit space is continuous, addressable by stable kit-id (not season-numbered), and grows as engine fires kit-space-expansion events.

**Per canonical record § 3.3 (continuous kit space properties):**
- Each kit has a stable kit-id (not season-numbered; permanent space identifier)
- Kits added via engine parameter scope expansion events (chronicled per EAA-4)
- Player can browse the full space at Stage A (not restricted to "current season's roster")
- Kits don't expire / get retired by dev-imposed lifecycle

**Schema requirements:**

### 2.1 Per-kit JSON entry (the addressable unit)

Minimum required fields (rocket + elrond + star-lord coordinate on full set):
- `kit_id` — stable permanent identifier; format TBD per LOCK K discretion (e.g., kit_000001, kit_<UUID-fragment>, kit_<primary>_<sequence>)
- `primary_element` — one of canonical-7+1 (fire / water / earth / wind / lightning / holy / shadow / physical)
- `cultural_tradition` — substrate input reference
- `period` — substrate input reference (ANCIENT / MEDIEVAL / MODERN per WS2.P2 substrate)
- `chain_composition` — chain selection metadata
- `t4_selection` — T4 selection metadata
- `supporting_chain` — supporting chain metadata
- `skills` — array of per-skill entries (each with `flavor_decision: bool`, `flavor_word_used: str | null` per EAA-1), `skill_name`, role/archetype metadata
- `emergent_kit_concept` — e.g., "Necromancer" (derived from primary + cultural-tradition + period + chain composition + T4)
- `substrate_trace` — record of substrate inputs that produced this kit (provenance for kit-space chronicle composition)
- `kit_space_expansion_event_id` — link to chronicle entry that recorded the expansion event producing this kit (composes with EAA-4)
- `engine_version` — engine sha that generated this kit
- `generation_timestamp`

### 2.2 Lineage tags (per WS1A.Q18 model)

Adopt lineage-tag pattern from pool.json v1.1 schema (4 additive fields). Per-kit lineage tag values format:
- `kit-space-expansion-<event-id>-<timestamp>`
- `engine-<sha>-<expansion-event-id>`

LOCK K discretion on exact tag schema.

### 2.3 Backward compatibility

- Existing per-season manifest schema PRESERVED for historical seasons (per canonical record § 6 Path α; not migrated)
- New schema is ADDITIVE — distinct namespace; doesn't overwrite season manifest schema
- If reincarnated-engine `seasons/` directory continues to hold per-season manifests for historical seasons, new kit-space entries land in a parallel directory structure (e.g., `kits/` or `kit_space/`)

### 2.4 ADR-004 MIGRATION.md (REQUIRED per LOCK K)

Cross-seam contract change MUST land with MIGRATION.md per ADR-004:
- old contract: per-season manifest (preserved; not deprecated)
- new contract: per-kit JSON entry in kit space directory
- backward-compatibility: BOTH coexist; per-season historical preserved; new generation emits per-kit
- consumer-side impact: drax loadout app needs to handle BOTH per-season-historical AND per-kit-space (LOCK O scope for drax)

---

## 3. Sub-tasks

### 3.1 Per-kit JSON schema spec (rocket primary; DRAFT until elrond ingest-compat confirmed)

- Author per-kit JSON schema with field list + types + nullability + lineage tag values
- Compose against existing skill JSON schema (preserve consumer compat for skills; EAA-1 metadata fields land additively)
- Compose against pool.json lineage tag patterns
- **DRAFT discipline (per jack-ryan Gate-1 Phase 1 INFO-B):** Rocket schema spec is a DRAFT until elrond confirms ingest-compat per § 3.2; one iteration cycle expected before Gate-2. If elrond ingest constraints require schema adjustments, the revision cycle is in-scope per LOCK K.
- **kit_space_expansion_event_id coordination (per jack-ryan Gate-1 Phase 1 cross-dispatch INFO):** Rocket and elrond MUST coordinate `kit_space_expansion_event_id` format jointly before finalizing spec. Format must match EAA-4 `event_id` schema EXACTLY (foreign-key linkage). Confirm format with EAA-4 owner (elrond) before Gate-2 submission.

### 3.2 Ingest schema (elrond)

- Confirm elrond ingest pipeline can consume per-kit JSON entries
- If schema extension needed for substrate DB (kit-space-entries table), author additively per LOCK K
- MIGRATION.md notes ingest-side handling
- **Iterate with rocket per § 3.1 DRAFT discipline:** if rocket's draft schema requires adjustment to fit elrond ingest patterns, iterate before Gate-2 submission

### 3.3 Output pipeline integration (star-lord)

- Engine emit path emits per-kit JSON entry to kit space directory
- Per-kit emit replaces per-season manifest emit when EAA-2 skip flags are active
- Coordinate with EAA-4 chronicle emit (each kit-space-expansion event records chronicle entry alongside per-kit entries)

### 3.4 Smoke-test discipline (Disc #2)

- Smoke-test single-kit emit with new schema against full pipeline
- Verify schema validation passes (no rejected fields; nullability correct)
- Verify backward-compat: existing season manifest path unchanged (when EAA-2 skip flags inactive, legacy emit path still works)

### 3.5 ADR-004 MIGRATION.md authoring

Author MIGRATION.md at standard cross-seam contract location per established pattern (e.g., `reincarnated-engine/MIGRATION.md` updates or per-cycle MIGRATION docs). Cover:
- Old contract (per-season manifest)
- New contract (per-kit JSON entry)
- Backward-compatibility (BOTH coexist)
- Consumer-side amendments needed (drax LOCK O scope; elrond ingest schema; star-lord output pipeline)
- Reversibility per LOCK J ADDITIVE-AND-REVERSIBLE heuristic

---

## 4. Out of scope (explicit non-goals)

- **Existing season manifests migration** — preserved as historical per canonical record § 6 Path α; NOT migrated
- **Drax loadout app consumption logic** — EAA-6 scope; LOCK O drax discretion within MVP-component constraint
- **Kit space chronicle schema** — EAA-4 scope; this dispatch defines the link field but not the chronicle schema itself
- **Player-facing kit-id surface format** — out of scope; engine kit-id is canonical; player-facing surface (browse UI labels) is EAA-6/7 scope
- **Per-kit visual asset references** — out of scope; per canonical record § 7.3 MM-P1 scope; deferred per LOCK P
- **Per-kit engagement telemetry** — out of scope; deferred per canonical record § 7.4

---

## 5. Cross-seam contract (Principle 6)

**Cross-seam touches:**
- rocket (engine emit schema; generation/) ↔ elrond (ingest schema; substrate DB) ↔ star-lord (output pipeline; export/)
- Downstream: drax (LOCK O consumes per-kit JSON; EAA-6 scope)

**Discipline:** ALL ADDITIVE per LOCK J + LOCK K. ADR-004 MIGRATION.md REQUIRED. Backward-compat with per-season historical seasons preserved.

**Round-trip:** if any consumer (elrond / star-lord / drax) cannot consume new schema additively, escalate per LOCK J escape clause.

---

## 6. Acceptance criterion

EAA-3 PASSES when:
1. Per-kit JSON entry schema specified (full field list + types + nullability + lineage tag values)
2. ADR-004 MIGRATION.md authored covering old/new contracts + backward-compat + consumer-side handling
3. Engine emit path emits per-kit entries (when EAA-2 skip flags active)
4. Smoke-test demonstrates schema validation pass + backward-compat preserved
5. elrond ingest + star-lord output pipeline confirm consumption compat
6. jack-ryan Gate-2 PASS on schema spec + MIGRATION.md

---

## 7. Tag intent

- Intermediate: `rocket/v1.4-eaa-3-kit-space-schema-<n>`
- Coordinated cross-seam tag per ADR-004 when elrond + star-lord branches converge
- Wave-close milestone tag deferred to EAA-8

---

## 8. Auto-commit + auto-push

Per Matt 2026-06-02 explicit cycle-push authorization + CLAUDE.md addendum 2026-05-25:
- Auto-commit work-products as you go
- Auto-push per established cycle-push pattern
- Update wave-state file workstream status table on completion

---

## 9. References

- **Authoritative architectural commitment:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 + § 3.4
- **Pool.json v1.1 schema patterns:** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`
- **ADR-004 cross-seam MIGRATION:** `agentic_orchestration/GOVERNANCE.md`
- **Wave-state:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- **Generation seam owner:** rocket operating procedure
- **Data steward seam owner:** elrond operating procedure
- **Output pipeline seam owner:** star-lord operating procedure
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

**End of EAA-3 dispatch. Fires after jack-ryan Gate-1 PASS on this dispatch.**

---

## Completion record — elrond co-owner sub-tasks (2026-06-02)

**Status:** 🟡 ELROND-SIDE COMPLETE; awaiting rocket DRAFT spec author + star-lord output pipeline integration + jack-ryan Gate-2

**Elrond sub-tasks delivered (per dispatch § 3.2 + composed with EAA-4):**

1. ✅ **Ingest-compat confirmed** — per-kit JSON entry shape consumable by elrond ingest pipeline; shadow tables additive per LOCK J ADDITIVE-AND-REVERSIBLE; no engine-side schema field that breaks ingest
2. ✅ **Substrate DB extension authored additively** — `engine_kit_index` + `engine_kit_space_events` shadow tables (DDL at joint spec § 3.5) — rebuildable from filesystem; reversible per LOCK J
3. ✅ **`kit_space_expansion_event_id` format LOCKED jointly with EAA-4** (per Phase 1 batch Gate-1 INFO-B amendment) — `kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>` per pre-existing coordination note at `cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md`; 27-char fixed; chronologically sortable as text; UUID-derived suffix for distributed-safe collision-resistance; future-extensible event-type prefix space (`re_` realm-expansion reserved)
4. ✅ **`kit_id` format LOCKED** — `kit_<primary>_<seq6>` (joint spec § 2); per-primary sequence; permanent (not season-numbered)
5. ✅ **5 iteration points named for rocket DRAFT** (joint spec § 4.4) — `primary_element` lowercase / `period` uppercase / `engine_version` short-sha / emit ordering chronicle-first / EAA-1 `flavor_decision`+`flavor_word_used` integrity; iteration cycle in-scope per LOCK K
6. ✅ **MIGRATION.md authored** (per dispatch § 3.5; LOCK K) — `agentic_orchestration/research/curated/MIGRATION.md` v1.8 covering old contract (per-season manifest) + new contract (per-kit JSON + chronicle) + backward-compat (BOTH coexist) + consumer-side impact + reversibility per LOCK J ADDITIVE-AND-REVERSIBLE

**Artifacts:**
- Joint spec note: `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` (10 sections)
- MIGRATION.md v1.8: `agentic_orchestration/research/curated/MIGRATION.md` (most-recent-first; v1.8 entry at top)
- Wave-state update: `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md` § 3 (EAA-3 + EAA-4 rows updated)

**Next moves:**
- Rocket: author per-kit JSON schema DRAFT per joint spec § 4 with format locks applied; iterate against 5 iteration points if engine-side surfaces divergence
- Star-lord: implement chronicle emit FIRST then per-kit JSONs SECOND (atomicity discipline § 5); source `engine_version_sha` consistently
- Elrond: shadow-table CREATE script + ingest script deferred to EAA-3 + EAA-4 implementation phase post-Gate-2
- KR: route rocket DRAFT review + jack-ryan Gate-2 on schema spec + MIGRATION.md with format locks attached

**Signed:** elrond (data steward; LOCK K + LOCK E seam authority; EAA-3 co-owner)

---

## Completion record — rocket primary (2026-06-02)

**Completed by:** rocket
**Date:** 2026-06-02
**Status:** DRAFT v2 COMPLETE (SEQ-3 corrected) — rocket spec authored + 63/63 smoke tests PASS; awaiting jack-ryan Gate-2 + star-lord emit integration

**Note:** Initial commit 1d4ad87 (tag v1) implemented UUID-hex event_id format per joint spec § 1.1-1.2 body text. Jack-ryan Gate-2 BLOCK finding identified this as documentation drift; SEQ-3 is authoritative per CHRONICLE_SCHEMA.md § 3. v2 commit ca45b5d corrects to SEQ-3.

### Commits

| Sha | Tag | Repo | Contents |
|---|---|---|---|
| `1d4ad87` | `rocket/v1.4-eaa-3-kit-space-schema-1` | reincarnated-engine | Initial DRAFT: `kit_space_schema.py` + 51 smoke tests + MIGRATION.md EAA-3 entry (UUID-hex; superseded by v2) |
| `ca45b5d` | `rocket/v1.4-eaa-3-kit-space-schema-2` | reincarnated-engine | v2 SEQ-3 corrected: `mint_kit_space_expansion_event_id` + `count_chronicle_events_today` + UUID-hex rejection in validator; 63/63 PASS |

### Rocket sub-tasks delivered (per dispatch § 3.1)

1. ✅ **Per-kit JSON schema spec authored** — `src/reincarnated/generation/kit_space_schema.py` implements:
   - `new_kit_space_expansion_event_id() -> tuple[str, str]` — locked FK format per joint spec § 1.3
   - `mint_kit_id(primary, prior_count) -> str` — locked kit_id format per joint spec § 2.4
   - `validate_event_id(event_id)` + `validate_kit_id(kit_id)` — format validators
   - `validate_per_kit_entry(entry) -> list[str]` — full schema validation covering all 5 iteration points
   - `build_kit_entry(...) -> dict` — per-kit JSON entry builder for star-lord emit path
   - `count_kits_by_primary(kits_dir) -> dict` — directory glob for mint_kit_id prior count
2. ✅ **All 5 elrond iteration points enforced** at emit time:
   - IP-1: `primary_element` lowercase canonical-7+1 (validated + normalised in `mint_kit_id`)
   - IP-2: `period` ANCIENT/MEDIEVAL/MODERN uppercase (validated in `build_kit_entry` + `validate_per_kit_entry`)
   - IP-3: `kit_space_expansion_event_id` SEQ-3 regex `^kse_\d{8}_\d{3}$` (validated in `validate_event_id`; UUID-hex explicitly rejected)
   - IP-4: `engine_version` presence check (validated in `validate_per_kit_entry`)
   - IP-5: `flavor_decision` + `flavor_word_used` integrity enforced at per-skill level (validated in `validate_per_kit_entry`)
3. ✅ **MIGRATION.md EAA-3 entry authored** — `src/reincarnated/generation/MIGRATION.md` (field table, consumer obligations, backward-compat, iteration points, identifier generation rules)
4. ✅ **Event-id length empirical correction** — joint spec § 1.1 states 27 chars but locked format produces 26; regex is authoritative; test asserts 26 + documents discrepancy
5. ✅ **Lineage tags auto-built** matching pool.json v1.1 pattern (4-field: kit_space_lineage, engine_provenance, substrate_provenance, generation_cohort_date)

### Smoke-test results

63/63 PASS (v2 SEQ-3). Coverage per dispatch § 3.4:
- event_id mint (SEQ-3): regex, length, prefix, seq-001, seq-002, seq-padding, different-date, no-uuid-hex (8 tests)
- count_chronicle_events_today: empty, same-day events, missing file (3 tests)
- kit_id mint: all 8 primaries, sequencing, zero-padding, titlecase normalisation, invalid primary, regex (7 tests)
- validate_event_id: SEQ-3 PASS + UUID-hex FAIL + 4 other FAIL paths (6 tests)
- validate_kit_id: PASS + 4 FAIL paths
- validate_per_kit_entry PASS: minimal, all periods, physical opt-out, flavor=true+word, flavor=false+null, seq3-002 (6 tests)
- validate_per_kit_entry FAIL: all 5 IPs (IP-3 tested twice: UUID-hex + bad_id) + missing kit_id + empty skills + wrong schema_version (10 tests)
- build_kit_entry: valid entry, schema_version, lineage_tags, timestamp, invalid event_id, UUID-hex raises, invalid period, JSON-serialisable (8 tests)
- count_kits_by_primary: empty dir, with kit files, non-kit files ignored (3 tests)
- lineage_tags: 4 fields, date extraction, field content (4 tests)
- round-trip: event_id mint -> kit_id mint -> build_kit_entry -> validate -> JSON round-trip (1 test)

### DRAFT discipline note

This spec is DRAFT per dispatch § 3.1 + jack-ryan Phase 1 batch Gate-1 INFO-B. Elrond ingest-compat is CONFIRMED per joint spec § 4.4 for all 5 iteration points. No divergence detected. If star-lord emit implementation surfaces schema adjustments, iterate against elrond joint spec before Gate-2 submission.

### Next moves

- jack-ryan: Gate-2 review on schema spec (kit_space_schema.py + MIGRATION.md EAA-3 entry + 5 iteration point coverage)
- star-lord: implement chronicle emit + per-kit JSON emit using `build_kit_entry()` + `validate_per_kit_entry()` from this module; emit chronicle FIRST then per-kit entries (joint spec § 5)
- EAA-3 acceptance criterion 3 (engine emit path): pending star-lord integration; in-scope for star-lord's EAA-3 co-owner scope

**Signed:** rocket (generation seam; LOCK K co-owner; EAA-3 primary owner)

---

## Completion record — star-lord co-owner (EAA-3 § 3.3 emit integration) (2026-06-02)

**Completed by:** star-lord
**Date:** 2026-06-02
**Status:** ✅ COMPLETE — star-lord emit integration delivered; AC-3 MET; jack-ryan Gate-2 PASS-with-INFO

### Commits

| Sha | Tag | Repo | Contents |
|---|---|---|---|
| `23b42ed` | `star-lord/v1.4-eaa-3-eaa-4-emit-integration-1` | reincarnated-engine | `src/reincarnated/export/kit_space_emitter.py` + `tests/test_kit_space_emitter.py` + MIGRATION.md § v1.72 + AGENT_STATE.md |

### Star-lord sub-tasks delivered (per dispatch § 3.3)

1. ✅ **Engine emit path emits per-kit JSON entry to kit space directory** — `emit_kit_space_expansion_event()` in `kit_space_emitter.py`; writes per-kit JSONs atomically (`.tmp` → `os.replace`) to `data/kit_space/kits/kit_<primary>_<seq6>.json`
2. ✅ **Per-kit emit coordinated with EAA-4 chronicle emit** — chronicle entry written FIRST per CHRONICLE_SCHEMA.md § 5 emit-order discipline; per-kit JSONs written SECOND; FK `kit_space_expansion_event_id` verified in round-trip tests
3. ✅ **EAA-2 skip-flag compose rule implemented** — `should_use_kit_space_emit()` returns True only when BOTH `skip_theme_coalescence=True` AND `skip_cosmological_vocabulary=True`; legacy path untouched (LOCK M Stage 1)
4. ✅ **Schema validation at write boundary** (Discipline #8) — `validate_per_kit_entry()` called before each kit JSON write; errors surfaced in `KitSpaceEmitStats`
5. ✅ **MIGRATION.md § v1.72 authored** — old/new contracts, consumer obligations, backward-compat, smoke results

### Acceptance criteria MET (EAA-3 § 6)

| AC | Status |
|---|---|
| 1. Per-kit JSON entry schema specified | ✅ COMPLETE — rocket (kit_space_schema.py) |
| 2. ADR-004 MIGRATION.md authored | ✅ COMPLETE — star-lord MIGRATION.md § v1.72 (engine seam); elrond MIGRATION.md v1.8+v1.9 (collab seam) |
| 3. Engine emit path emits per-kit entries | ✅ COMPLETE — this star-lord delivery |
| 4. Smoke-test pass + backward-compat preserved | ✅ COMPLETE — 31/31 new + 317/317 combined PASS; skip-flag guard confirmed |
| 5. elrond ingest + star-lord output pipeline confirm | ✅ COMPLETE — elrond ingest-compat CONFIRMED (joint spec § 4.4); star-lord emit implemented |
| 6. jack-ryan Gate-2 PASS | ✅ COMPLETE — PASS-with-INFO; finding `qa/findings/2026-06-02-eaa-3-eaa-4-star-lord-emit-gate-2.md` |

**EAA-3 FULLY CLOSED at star-lord seam.**

**Signed:** star-lord (export seam; LOCK K co-owner; EAA-3 co-owner) 2026-06-02
