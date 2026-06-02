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
