# Dispatch — 2026-06-02 — EAA-4 — Kit-space chronicle infrastructure

**From:** knight-rider (orchestrator)
**Primary owner:** elrond (data steward; chronicle schema + ingest)
**Co-owner:** star-lord (engine emit pipeline; chronicle event emission)
**Cycle:** cycle-16-eaa-engine-architectural-amendment (Phase 1)
**Authority:** Matt 2026-06-02 Pattern B substantive design session + Locks A-P (LOCK K active for engine schema design authority)
**Wave tag:** `EAA-4`
**Wave-open dispatch:** `agentic_orchestration/dispatches/2026-06-02-cycle-16-eaa-engine-architectural-amendment-wave-open.md` (READ FIRST)
**State file:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
**Wave-open Gate-1 finding:** `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` (PASS-with-INFO; **INFO-3 applies — see § 4 out of scope**)
**Estimated horizon:** ~1-2 sessions
**Gates:** jack-ryan Gate-1 pre-fire on this dispatch + Gate-2 on implementation

---

## 1. Authoritative reading (READ IN ORDER before any action)

1. `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.4 (engine kit-space expansion chronicle properties) — binding
2. Existing telemetry/output infrastructure in `~/Games/reincarnated-engine/src/reincarnated/output/` and `~/Games/reincarnated-engine/src/reincarnated/telemetry/`
3. Wave-open dispatch (see header) — chain context

---

## 2. Scope

Design + implement the **kit-space chronicle** — a parameter-expansion-event tracking record that captures WHEN the engine fired a kit-space-expansion event, WHAT substrate inputs changed, WHICH kits were generated, and PER-KIT substrate-trace.

**Per canonical record § 3.4 (chronicle records):**
- Parameter expansion event timestamp + scope (e.g., "2026-06-02: Q18 vocabulary lock added — 109 sub-element flavor entries; kit space expansion run produced 87 new kits")
- Per-expansion-event substrate inputs that changed
- Per-expansion-event kits generated
- Per-kit substrate-trace (what inputs produced this kit)
- Realm Expansion events (when new Maps / Acts / Game Modes released; which kit groupings the design surfaces value of)

**Replaces:** per-season chronicle on the engine page. The chronicle becomes the engine-page narrative content (per EAA-7 reframe).

---

## 3. Sub-tasks

### 3.1 Chronicle entry schema (elrond primary)

Per-event chronicle entry minimum fields (LOCK K discretion on additional fields):
- `event_id` — stable event identifier (referenced by per-kit JSON `kit_space_expansion_event_id` per EAA-3)
- `event_timestamp` — when the engine fired
- `event_scope` — human-readable description (e.g., "Q18 vocabulary lock added; 109 sub-element flavor entries operational")
- `substrate_inputs_changed` — list of substrate sources that changed since prior event (e.g., pool.json v1.1 / WS2.P2 magic weapons ingested / new cultural-traditions added)
- `engine_version_sha` — engine code sha at event-fire
- `kit_ids_generated` — array of kit_ids produced by this event (composes with EAA-3 per-kit JSON)
- `kit_count` — derived field; count of kit_ids_generated
- `event_type` — `kit-space-expansion` for now; future event types (e.g., `realm-expansion`) when those workstreams open

**Realm Expansion events (future event type):**
Per canonical record § 3.4, future event types include Realm Expansion (new Maps / Acts / Game Modes). Schema should ACCOMMODATE future Realm Expansion event records via `event_type` field; but this dispatch IMPLEMENTS only `kit-space-expansion` event type.

### 3.2 Chronicle storage (elrond + star-lord)

LOCK K discretion on storage medium:
- Option α: flat JSON file at `kit_space_chronicle.json` (parallels pool.json pattern)
- Option β: substrate DB extension table (kit_space_events table)
- Option γ: per-event JSON file in `kit_space_events/` directory

Recommendation: elrond decides per their seam authority + substrate DB conventions; ADDITIVE per LOCK K.

### 3.3 Engine emit integration (star-lord)

- Engine emits chronicle entry on each kit-space-expansion fire
- Chronicle entry lands alongside per-kit JSON entries (EAA-3)
- Single transactional emit if possible (atomic: chronicle entry + per-kit entries land together)
- LLM telemetry decisions per star-lord seam discipline

### 3.4 Smoke-test discipline (Disc #2)

Before EAA-5 first-fire consumes this infrastructure:
- Smoke-test chronicle emit on single-kit generation (verify entry written + linked from per-kit JSON via `kit_space_expansion_event_id`)
- Verify chronicle storage medium consumable by EAA-7 engine page reframe (drax can read it)
- Verify substrate-trace per-kit accurate

### 3.5 ADR-004 MIGRATION.md (required per LOCK K)

Cross-seam contract documentation:
- Old contract: per-season chronicle on engine page (legacy; not removed)
- New contract: kit-space chronicle parameter-expansion-event tracking
- Backward-compat: BOTH coexist (legacy per-season chronicle preserved if engine page still surfaces historical seasons)
- Consumer-side: drax engine page (EAA-7 scope) consumes new chronicle

---

## 4. Out of scope (explicit non-goals)

**[GATE-1 INFO-3 APPLIES — EXPLICIT BOUNDARY]**

- **Per-kit engagement telemetry (player-facing engagement tracking)** — NOT this dispatch. The chronicle is a parameter-expansion-event tracking record; it captures WHAT the engine did, NOT WHAT PLAYERS DO with kits. Per-kit engagement telemetry is a separate future workstream gated on first kit-space-expansion telemetry data and player engagement happening (per canonical record § 7.4). Do not scope per-kit engagement tracking into the EAA-4 chronicle schema.

- **Realm Expansion event records** — schema accommodates the event_type field; this dispatch implements ONLY `kit-space-expansion` event type. Future Realm Expansion content design will introduce that event type.

- **Engine page UI rendering of chronicle** — EAA-7 scope; this dispatch produces the chronicle data; EAA-7 consumes it via existing EngineStatePipelineFlow component pattern per LOCK O.

- **Realm Expansion content design (telemetry-consults-underplayed-kits mechanism)** — out of scope; gates on first Realm Expansion content design session.

- **Historical season chronicle backfill** — preserved as-is per canonical record § 6 Path α; legacy per-season chronicle data NOT migrated to new schema.

---

## 5. Cross-seam contract (Principle 6)

**Cross-seam touches:**
- elrond (data layer; chronicle storage schema + ingest) ↔ star-lord (engine emit pipeline; chronicle event emission)
- Downstream: drax (LOCK O consumes chronicle for engine page reframe; EAA-7 scope)

**Discipline:** ALL ADDITIVE per LOCK J + LOCK K. ADR-004 MIGRATION.md REQUIRED.

**Round-trip:** if storage medium choice (α/β/γ) introduces consumer-side incompat with drax engine page existing components (LOCK O constraint), escalate via LOCK O escape clause.

---

## 6. Acceptance criterion

EAA-4 PASSES when:
1. Chronicle entry schema specified (field list + types + event_type extensibility)
2. Chronicle storage medium selected + implemented (elrond discretion per LOCK K)
3. Engine emit path emits chronicle entry on each kit-space-expansion fire (star-lord integration)
4. Per-kit JSON entries (EAA-3) link to chronicle via `kit_space_expansion_event_id` (cross-cycle composition)
5. Smoke-test demonstrates chronicle + per-kit JSON co-emission + linkage integrity
6. ADR-004 MIGRATION.md authored
7. jack-ryan Gate-2 PASS

---

## 7. Tag intent

- Intermediate: `elrond/v1.4-eaa-4-chronicle-<n>`
- Cross-seam coordinated with star-lord branch per ADR-004
- Wave-close milestone tag deferred to EAA-8

---

## 8. Auto-commit + auto-push

Per Matt 2026-06-02 explicit cycle-push authorization + CLAUDE.md addendum 2026-05-25:
- Auto-commit work-products as you go
- Auto-push per established cycle-push pattern
- Update wave-state file workstream status table on completion

---

## 9. References

- **Authoritative architectural commitment:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.4
- **EAA-3 per-kit schema (composing dispatch):** `agentic_orchestration/dispatches/2026-06-02-eaa-3-kit-space-output-schema.md`
- **Wave-state:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- **Data steward seam owner:** elrond operating procedure
- **Output pipeline seam owner:** star-lord operating procedure
- **ADR-004 cross-seam MIGRATION:** `agentic_orchestration/GOVERNANCE.md`
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

**End of EAA-4 dispatch. Fires after jack-ryan Gate-1 PASS on this dispatch.**
