# Dispatch — 2026-05-16 — star-lord — Per-fight observed-MS telemetry emission (per gandalf handoff #5)

**From:** knight-rider (authored per gandalf's 2026-05-16 Day 4 movement-speed-baseline commission handoff item #5 + Matt's "author and fire... star lord" directive)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 explicit one-liner
**Status:** PENDING — ACTIVE
**Estimated effort:** ~1 hour per gandalf handoff (small telemetry-schema addition + recorder wiring + smoke)
**Acceptance:** Per-fight observed-MS telemetry emission lands as a new field on `class_fight_loadouts` (or appropriate telemetry table) capturing the actual movement_speed value used during simulation per fight; small additive schema change; recorder wired; smoke test confirms persistence; MIGRATION.md entry per ADR-004.

---

## Context — why this dispatch exists

Per gandalf's 2026-05-16 movement-speed-baseline commission handoff item #5:

> **Optional star-lord dispatch** — per-fight observed-MS telemetry emission. ~1h; not VS2a-gating.

Gandalf marked it OPTIONAL; Matt explicitly authorized it via "author and fire... star lord" — promoting from optional to part of the day's coordinated fire batch.

**Why the dispatch is valuable even though not VS2a-gating:**
- Once gamora's Stage A2 movement-speed-aware sim extension lands (post-VS2a tight follow per gandalf handoff #3), the per-fight observed-MS field becomes the empirical evidence for whether the sim consumption matches the locked baseline (5.75 base; 7.5 mid VS2a target)
- Provides empirical signal during the VS2a → post-VS2a window — telemetry shows current movement-speed-blind behavior; once Stage A2 lands, telemetry shows movement-speed-aware behavior; the delta is observable
- Cross-validates rocket's schema-additive movement_speed field (parallel dispatch this turn) — if rocket emits the field correctly, the recorder captures it correctly per fight, the empirical loop is closed

## What this dispatch does

### Step 1 — Schema addition (v2.2 telemetry migration)

Following the pattern from your v2.1 telemetry schema work (per `dispatches/2026-05-16-star-lord-telemetry-schema-b10-v2-fields.md`):

Append a new migration entry to `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (v2.2):

**class_fight_loadouts:**
```sql
ALTER TABLE class_fight_loadouts ADD COLUMN observed_movement_speed REAL;
```

NULL-permitting (consistent with v2.0 → v2.1 → v2.2 pattern; historical rows carry NULL; fresh rows post-migration carry the actual value).

**Field semantics:**
- `observed_movement_speed: REAL` — the movement_speed value (in m/s) the simulator actually used during this fight for the player-class. For the current (movement-speed-blind) simulator, this should be the rocket-emitted default value (5.75) per fight. For the future (Stage A2 movement-speed-aware) simulator, this captures the actual per-fight value the sim consumed including any per-archetype + per-buff scaling.

### Step 2 — Recorder wiring

Update `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (or whichever module owns the relevant `record_*` functions per your seam):

- `record_class_fight_loadouts` (or equivalent): accept `observed_movement_speed` from the fight_log dict; write in the INSERT when present
- **Defensive nulls:** if a fight_log dict lacks the field (V1 sim code paths or pre-rocket-schema-shipped paths), write NULL — do NOT error
- **Source field:** the simulator's per-fight movement_speed value (currently movement-speed-blind = rocket-emitted default; future movement-speed-aware = sim-computed)

### Step 3 — Smoke test

Per Discipline #2:
- Existing tests in `tests/test_telemetry.py` pass
- New unit test for v2.2 migration + recorder wiring
- Small end-to-end smoke: run a 5-class smoke season (using the current movement-speed-blind sim); verify `observed_movement_speed` populated on fresh rows with the rocket-emitted default value (5.75 per fight for all classes; 5.75 for trash monsters per per-fight semantics)
- Verify NULL handling: a V1-code-path call should write NULL (test with the v2.1 pattern's NullRecorder approach)

### Step 4 — MIGRATION.md

Append a v2.2 entry to `reincarnated-engine/src/reincarnated/export/MIGRATION.md`. Cover:

- New `observed_movement_speed` field with semantics (per-fight movement_speed value the simulator used)
- Cross-reference to rocket's movement_speed schema dispatch (`dispatches/2026-05-16-rocket-movement-speed-schema-field.md`) as the upstream schema source
- Cross-reference to gandalf's movement-speed-baseline doc (`canonical/story/movement-speed-baseline.md`) as the values source-of-truth
- Downstream consumer note for gamora (Stage A2 movement-speed-aware sim extension): once Stage A2 lands, observed_movement_speed will reflect the sim-computed value (currently movement-speed-blind = rocket-emitted default)
- Downstream consumer note for drax (Damage×TTK projection switch + future per-fight visualization): observed_movement_speed enables per-fight movement-speed visualization correctness

### Step 5 — AGENT_STATE + completion record

Update `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md`:
- v2.2 telemetry schema migration shipped
- Cross-seam-coordination: rocket movement_speed schema dispatch (parallel; same turn) is the upstream supply; gamora Stage A2 is the future downstream consumer

Fill in the completion record at the bottom of this dispatch.

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.2-observed-ms` at the commit closing migration + recorder + tests pass.
- **Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

## Cross-seam considerations

- **Rocket:** READ-ONLY upstream (rocket's parallel-fire movement_speed schema dispatch supplies the field at generation; your recorder captures it at per-fight time). If you find a field-semantic mismatch with rocket's schema, surface as a finding; coordinate via knight-rider.
- **Gamora:** READ-ONLY future consumer. Stage A2 movement-speed-aware sim extension (per gandalf handoff #3; post-VS2a tight follow) will SET the observed_movement_speed value per fight from sim-computed-vs-rocket-default. Until then, the field captures the rocket-default value (5.75 per fight).
- **Drax:** READ-ONLY downstream. Per-fight observed-MS enables Damage×TTK projection per-fight movement-speed weighting (future work).
- **Knight-rider:** notify at completion. Telemetry v2.2 schema becomes available for downstream consumers.

## Out of scope (explicit)

- **NO simulator-side movement-speed consumption logic.** Gamora's Stage A2 work; separate dispatch (post-VS2a tight follow per gandalf handoff #3).
- **NO rocket schema work.** Parallel-fire dispatch authored separately (`dispatches/2026-05-16-rocket-movement-speed-schema-field.md`).
- **NO drax rendering work.** Drax dispatch HELD pending decisions-log entry per gandalf handoff #2 + #4.
- **NO per-fight movement_speed validation logic.** Schema is descriptive (records what the sim used); validation lives at higher layers.
- **NO existing v2.0 → v2.1 → v2.2 migration re-architecture.** Append v2.2 entry following the pattern; do NOT alter v2.0 or v2.1.
- **NO production DB migration write** (the DB migration on `data/telemetry.db` requires Matt authorization per ADR-006; full regen lands separately).

## Required reading

- `canonical/story/movement-speed-baseline.md` (gandalf locked values + design-family framing)
- `agentic_orchestration/gandalf/requests/2026-05-16-movement-speed-baseline-vs2a-gating.md` (gandalf commission; handoff item #5 is your assigned scope)
- `agentic_orchestration/dispatches/2026-05-16-star-lord-telemetry-schema-b10-v2-fields.md` (your prior v2.1 schema dispatch; the pattern reference)
- `agentic_orchestration/dispatches/2026-05-16-rocket-movement-speed-schema-field.md` (parallel-fire upstream schema source)
- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (your target file; v2.1 entry is the pattern reference)
- `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (your target file)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 1 strategic-axis lock (movement_speed lives at substrate-mechanical layer)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke-test); #11 (attribution: cite gandalf's locked-values commit in MIGRATION.md note); #12 (semantic-shifting: observed_movement_speed is a meaningful field after this lands; will shift meaning post-Stage-A2)

## Acceptance criteria

- [ ] migrations.py v2.2 entry added; `observed_movement_speed` column created
- [ ] Recorder wired to write observed_movement_speed from fight_log dicts; defensive null handling
- [ ] Existing telemetry tests pass; new v2.2 unit test passes
- [ ] Smoke season verifies field population with rocket-emitted default (5.75 m/s per fight) under current movement-speed-blind sim
- [ ] MIGRATION.md v2.2 entry filed (cross-references rocket dispatch + gandalf baseline doc)
- [ ] Intermediate tag `star-lord/v1.3-telemetry-schema-v2.2-observed-ms` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

---

## Completion record

**Completed:** 2026-05-16 by star-lord (claude-sonnet-4-6)
**Migration version (v2.2):** V2.2 — `observed_movement_speed REAL` on `class_fight_loadouts`
**Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.2-observed-ms` at commit `db4aa09` — pushed to origin
**Smoke status:** PASSED — 20 new tests in `tests/test_telemetry_v22.py`, all pass. Pre-rocket defensive-null smoke: 5-class × 3-fight, 15/15 rows observed_movement_speed IS NULL (correct: rocket schema not yet landed). Post-rocket emulation smoke: 15/15 rows at 5.75 m/s. 62 total telemetry tests pass; full suite clean.
**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — "Schema 2.1 → 2.2" section appended

**Notes for knight-rider:**

1. **Rocket's parallel-fire movement_speed dispatch NOT yet landed.** All fresh `class_fight_loadouts` rows currently carry `observed_movement_speed IS NULL`. This is the correct pre-rocket behavior — defensive null wiring confirmed by smoke. Once rocket's `movement_speed` schema field lands, balance_loop will emit the field and the recorder picks it up automatically (no further star-lord work needed).

2. **DB migration NOT applied to `data/telemetry.db`.** Schema V2.2 is in `migrations.py` and will apply on next `apply_schema_migrations()` call. Live DB remains at V2.1 until next full regen or explicit migration application. Requires Matt authorization per ADR-006 for the write.

3. **Gamora Stage A2 is the next meaningful consumer.** Once gamora's Stage A2 movement-speed-aware sim extension lands (post-VS2a tight follow per gandalf handoff #3), `observed_movement_speed` will carry sim-computed per-fight values. The recorder wiring is already in place — no star-lord change needed at Stage A2 time. Semantic shift: NULL → 5.75 uniform (post-rocket) → sim-computed per-fight (post-Stage-A2). All three phases observable via the field values.

4. **Drax dispatch HELD.** Per-fight Damage×TTK MS weighting by `observed_movement_speed` remains drax-scope future work, pending decisions-log entry (gandalf handoff #2 + knight-rider sequencing). No drax action from this dispatch.
