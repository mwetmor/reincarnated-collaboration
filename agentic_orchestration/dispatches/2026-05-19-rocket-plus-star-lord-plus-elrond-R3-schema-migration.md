# Dispatch — 2026-05-19 — rocket + star-lord + elrond — R3 per-skill range + AI behavior schema migration

**From:** knight-rider
**To:** rocket (generation seam — schema + catalogue OWNER), star-lord (operational pipeline seam — export + telemetry OWNER), elrond (data-steward seam — backfill tooling OWNER)
**Approved by:** AUTONOMOUS — engine-rebuild hive activation under Matt directive 2026-05-19 (no per-dispatch Matt approval; design + sequencing confirmed by gandalf per solutions doc § 10)
**Estimated effort:** 2–4 weeks together
**Acceptance:** R3 Tests 1+2+3 pass per solutions doc § 4 (out-ranging viability +20pp WR delta; disengage viability controller WR 0% → ≥20% on hard-counter boss; range-profile redistribution to ~30/40/30 distribution within 5pp)
**Hive context:** Engine-rebuild hive ACTIVE (second activation). R3 is the **foundation workstream** — R2, R4, R5, R7 all gate on R3 shipping. Slip in R3 slips four downstream. Cross-seam contract change with broad blast radius — MIGRATION.md REQUIRED.

---

## Context

The engine has exactly one range gate: `at_melee_range` binary flag (`fight_engine.py:161`). No per-skill range data exists in the catalogue. Skills work identically at 2m, 5m, 11m. Player cannot out-range an enemy. Player cannot disengage. **Range is not a design lever; it's a binary check.**

R3 is a **multi-part schema migration**, not a single fix. All four parts are required:

1. Per-skill range field
2. Per-mob AI behavior fields
3. Backfill across 5 shipped seasons
4. Disengage as a valid balance-loop action

Partial R3 produces inconsistent runtime; full R3 enables R2 (spatial sub-gauntlet), R4 (demo collision + leash + range), R5 (demo AI parity), R7 (catalogue source of truth).

## Required reading before starting

**All three of you, in order:**

1. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` — operating protocol (§ 4.0 autonomous-operation; § 4.4 cross-seam coordination; § 4.5 jack-ryan + Discipline #13 drift watch; § 5.2 R3 activation requirements; § 9 engineering disciplines)
2. `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 4 — R3 specification
3. `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — diagnosis (Axis 4 specifically — "no per-skill range; no out-ranging; no disengage")
4. `agentic_orchestration/hive-mind/engine-rebuild-log.md` — hive log; each seam acknowledges activation in own STATE entry
5. `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md` § 1.2 — R3 deliverables summary
6. `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md` — concurrent-edit hot-spots (monster JSON schema is multi-seam; balance_loop.py shared with R1)
7. `reincarnated-engine/src/reincarnated/simulation/fight_engine.py:155, 161` — current 1D scalar + binary melee gate
8. `agentic_orchestration/GOVERNANCE.md` — ADR-004 MIGRATION.md requirement

**Rocket additionally reads:**
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — your last checkpoint
- Current monster JSON schema across `output/<season>/monsters/*.json`
- Current skill catalogue entries

**Star-lord additionally reads:**
- `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` — your last checkpoint
- Current telemetry schema (`telemetry/recorder.py:123, 713` per substrate-coupling archaeology references)
- Current export packet structure (`season_writer.py`)

**Elrond additionally reads:**
- Past elrond dispatches on catalogue curation + research-db retirement (for migration tooling patterns)
- The 5 shipped seasons' current state on disk

## Math-before-code (Discipline #1)

**Not heavily math-load-bearing**, but **design-then-build pattern applies.** Authoring required before implementation:

1. **Schema design draft** (rocket leads; gandalf design-input consult if substrate identity declarations are touched) — captures:
   - `range_m` (numeric meters) vs `range_band: short/medium/long/extreme` (enum). Pick one; document trade-off. L1 rocket decision; surface to gandalf only if cross-cutting design tension surfaces.
   - `preferred_behavior` enum vocabulary (melee_aggressive / ranged_kite / cast_at_range / charge_then_melee / etc.). Document the closed set; rationale per archetype.
   - `telegraph_window_seconds`, `aggro_radius_m`, `leash_distance_m`, `skill_rotation_priority`, `range_profile_redistribution` — exact field semantics + defaults.
   - Backfill derivation rules: which geometry types map to which range bands; which archetypes map to which preferred_behaviors.

2. **Backfill strategy** (elrond leads; rocket + star-lord consult) — captures:
   - Re-derive from geometry-type defaults vs re-roll skills with range as generation-time field (per solutions doc § 4)
   - Idempotency strategy (re-runnable without corrupting state)
   - Validation strategy (post-backfill content passes existing engine schema validators)
   - Scope: 5 shipped seasons (which specific seasons; canonical paths)

3. **Telemetry surface** (star-lord leads) — captures:
   - What new fields are emitted per fight log + per class_balance_results
   - Whether `range_advantage_pp` (computed) is emitted alongside `skill_range_m` (raw)
   - Migration plan for existing telemetry tables (additive vs breaking)

Path: `reincarnated-engine/design/working-agreement/R3-schema-design-2026-05-19.md` (rocket authors; star-lord + elrond append sections).

Jack-ryan reviews before commit.

## Cross-seam contract change? (Principle 6 gate)

**YES — absolutely.** R3 is the canonical example of a cross-seam contract change requiring MIGRATION.md.

**Affected boundaries:**
- `monster_NNNNN.json` schema (rocket emitter → all consumers: gamora sim, drax demo, star-lord telemetry, elrond backfill)
- Skill catalogue entries (rocket emitter → simulation + demo + telemetry consumers)
- `class_balance_results` telemetry table (star-lord; new fields if R1 + R3 add per-tier-with-range telemetry)
- fight_log dict (gamora → star-lord boundary; new range-related fields)
- Season JSON `manifest.json` (engine → catalogue + loadout boundaries)

**MIGRATION.md REQUIRED, authored concurrently by rocket (producing seam) per protocol § 4.4 (inherited 2026-05-17 § 6.2):**
- Path: `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
- Format per ADR-004
- Captures: each new field, semantic meaning, default if missing, backfill plan, consumer obligations

**Star-lord authors complementary MIGRATION.md** at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` for telemetry surface changes (additive vs breaking; consumer rebuild requirements).

**Elrond's backfill tooling does NOT need its own MIGRATION.md** (it's a one-shot migration, not a contract), but elrond must document the backfill at `reincarnated-engine/output/R3-backfill-log-2026-05-19/README.md` (the tooling + the result + the validation report).

The Acceptance criteria below include the round-trip smoke clause.

## Scope (all three seams, in coordinated sequence)

### Rocket scope (schema + catalogue)

- [ ] Schema design draft authored at `reincarnated-engine/design/working-agreement/R3-schema-design-2026-05-19.md`
- [ ] MIGRATION.md authored concurrently at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
- [ ] Per-skill range field added to skill schema; integrated into skill generation
- [ ] Per-mob AI behavior fields added to monster JSON schema; integrated into monster generation
- [ ] Generators emit new fields for new content
- [ ] Engine schema validators updated to require new fields (fail-loud on missing, per Pattern P7 avoidance)
- [ ] Sim-side consumer in `fight_engine.py`: `at_melee_range` binary gate replaced with per-skill range check; out-of-range skill cannot fire
- [ ] Disengage action: player-sim and monster-sim AI can choose retreat-to-leash or kite-to-optimal-range
- [ ] Tag: `hive-rebuild/v0.4-r3-schema-draft-committed` when schema + MIGRATION.md ship
- [ ] AGENT_STATE.md updated

### Star-lord scope (export + telemetry)

- [ ] Telemetry surface updated to emit new fields (additive vs breaking; document choice in MIGRATION.md)
- [ ] Export packets reflect new schema fields
- [ ] `class_balance_results` table extended if range-related fields are needed for R1 + R3 cross-cutting analysis
- [ ] MIGRATION.md authored at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` for telemetry surface changes
- [ ] Round-trip smoke fixture exercising: generator emits new field → telemetry recorder ingests → export packet contains → loadout consumes (if loadout side needs new fields, coordinate with drax for downstream parity)
- [ ] AGENT_STATE.md updated

### Elrond scope (backfill)

- [ ] Backfill strategy authored (in shared `R3-schema-design-2026-05-19.md` doc, elrond section)
- [ ] Backfill tooling implemented (one-shot script + validation report)
- [ ] Backfill executed across the 5 shipped seasons (per solutions doc § 4)
- [ ] Validation report: post-backfill content passes existing engine schema validators
- [ ] Idempotency check: re-run backfill on already-backfilled season produces no diff
- [ ] Tag: `hive-rebuild/v0.5-r3-backfill-complete` when 5 seasons backfilled + validated
- [ ] Backfill documentation at `reincarnated-engine/output/R3-backfill-log-2026-05-19/README.md`

### Joint scope (hypothesis tests)

- [ ] R3 Test 1 (out-ranging viability) — execute per solutions doc § 4: long-range class (range_m=12) vs melee class (range_m=1.5) vs mid-range monster (range_m=8). Success: long-range WR ≥ 20pp higher. Stored at `reincarnated-engine/output/R3-test1-out-ranging.md`.
- [ ] R3 Test 2 (disengage viability) — controller class vs hard-counter boss; pre-fix 0% WR → post-fix ≥ 20% via disengage. Stored at `reincarnated-engine/output/R3-test2-disengage.md`.
- [ ] R3 Test 3 (range-profile redistribution) — pre vs post-R3 distribution; success ≈ 30/40/30 within 5pp. Stored at `reincarnated-engine/output/R3-test3-distribution.md`.
- [ ] Tag on hypothesis-test passage: `hive-rebuild/v0.6-r3-hypothesis-test-passed`
- [ ] Smoke-test GREEN throughout (each seam's commits leave engine GREEN per protocol § 4.5)
- [ ] Round-trip smoke: end-to-end fixture exercising generator → schema validator → telemetry recorder → export packet → loadout consumer (if loadout consumes). Field-presence checks at each boundary.

## Acceptance criteria

- [ ] Schema design draft + backfill strategy + telemetry surface design committed before any production code change
- [ ] MIGRATION.md (generation + export) authored concurrently with producing-seam work
- [ ] Per-skill range field operational in skill catalogue + sim consumption
- [ ] Per-mob AI behavior fields operational in monster JSON + sim consumption
- [ ] Backfill executed + validated across 5 shipped seasons (idempotent, fail-loud on validation gap)
- [ ] Disengage action operational in balance-loop AI (player + monster)
- [ ] R3 Tests 1+2+3 executed + results documented + hypothesis-test passage tagged
- [ ] Smoke-test GREEN throughout
- [ ] Round-trip smoke: generator → telemetry → export → consumer; field-presence check at each boundary. **(REQUIRED — this is a cross-seam contract change with broad blast radius.)**
- [ ] All three seams' AGENT_STATE.md updated
- [ ] Hive log entries: STATE on each seam's start; HANDOFF at producer → consumer boundaries; OBSERVATION on any Discipline #13 drift surface

## Out of scope (explicit non-goals)

- 2D spatial sub-gauntlet (R2 — depends on R3; separate workstream after R3 ships)
- Demo runtime collision/leash/range implementation (R4 — depends on R3; drax seam)
- Demo AI parity audit (R5 — depends on R3 partial; drax seam)
- AI catalogue parity test infrastructure (R7 — partial-parallel with R3; rocket + star-lord author separately under R7 dispatch)
- Per-tier balance targets (R1 — separate workstream; gamora)
- Season-as-emergent-output A/B (R8 — separate workstream; rocket + star-lord + gandalf in different scope)
- Substrate identity declaration revisions (Phase-1 P1 commitment; out-of-scope unless scope-creep table § 2.3 escalation path triggers)
- New substrate addition (out-of-scope per protocol § 2.3)

## Open questions for the agents to resolve (in-seam L1 / cross-seam L2 routing)

- **Range representation: `range_m` (numeric) vs `range_band` (enum)** — L1 rocket decision; document trade-off in schema design doc. L2 surface to knight-rider if conflict with star-lord telemetry shape.
- **Backfill derivation rules** — L1 elrond decision (with rocket consult on generation-side defaults); document in shared design doc.
- **Telemetry additive vs breaking** — L1 star-lord decision; document in MIGRATION.md. L2 surface to knight-rider if loadout consumer needs schema_version bump.
- **Disengage AI heuristic** — L1 rocket decision on the algorithm (e.g., HP-threshold-trigger; range-mismatch-trigger). L2 surface to knight-rider if cross-cutting (e.g., balance_loop.py edit collides with gamora's R1 work on the same file).
- **`fight_engine.py:155` 1D scalar distance** — L1 rocket on whether R3 retains 1D scalar with per-skill range checks or upgrades to a richer distance model. (Full 2D is R2 scope; R3 stays 1D.) Document choice.

## References

- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 4 (R3 specification)
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (Axis 4 diagnosis)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 5.2 (R3 activation requirements)
- `agentic_orchestration/GOVERNANCE.md` (ADR-004 MIGRATION.md)
- `reincarnated-engine/src/reincarnated/simulation/fight_engine.py:155, 161` (current 1D scalar + binary melee gate)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #13 drift vigilance; P7 silent-default)
- Hive log: `agentic_orchestration/hive-mind/engine-rebuild-log.md` — each seam acknowledges activation in own STATE entry

---

## Autonomous-operation authority (no Matt-wait)

Per launch dispatch § 3 + protocol § 4.0:

- **In-seam decisions** — L1 specialist; no escalation
- **Cross-seam decisions** — L2 via knight-rider in hive log; knight-rider harmonizes
- **Design-direction question** (e.g., substrate identity declaration touch) — surface to gandalf via hive log; gandalf decides
- **No Matt-wait at any point during R3.** Matt re-enters only at wind-down.

---

*Authored 2026-05-19 by knight-rider under autonomous-operation authority. R3 is the foundation. Schema first; math second; backfill third; hypothesis tests fourth. The range becomes a real lever; the disengage becomes a real choice; the gauntlet remembers what 11m means.*
