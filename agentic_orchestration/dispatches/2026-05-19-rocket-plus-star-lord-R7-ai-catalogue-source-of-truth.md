# Dispatch — 2026-05-19 — rocket + star-lord — R7 AI catalogue source of truth

**From:** knight-rider
**To:** rocket (generation seam — schema + sim consumption OWNER), star-lord (operational pipeline seam — catalogue + parity-test infrastructure OWNER)
**Approved by:** AUTONOMOUS — engine-rebuild hive activation under Matt directive 2026-05-19 (Option A "catalogue source of truth" pre-confirmed by gandalf per solutions doc § 10 Q4; parity-test infrastructure built now alongside R3 schema work, also pre-confirmed)
**Estimated effort:** 2–3 weeks; partial-parallel with R3 (shares schema)
**Acceptance:** R7 Tests 1+2+3 pass per solutions doc § 7 (parity test passes on schema change; parity test fails loudly on intentional break; 100% cross-surface behavioral consistency for 3 distinct preferred_behaviors)
**Hive context:** Engine-rebuild hive ACTIVE (second activation). R7 fixes the **drift-accumulation root cause** — three decoupled AI implementations (Python sim / TS demo / balance-loop implicit) sharing no source of truth.

---

## Context

Three decoupled AI implementations share no source of truth:

1. **Engine simulation AI** (`reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` + `fight_engine.py`) — Python, priority-rotation, 3-band scalar distance
2. **Demo runtime AI** (`reincarnated-demo/src/world/aggro.ts` + `world/movement.ts`) — TypeScript, FSM-ish, 2D pixel positions
3. **Implicit balance-loop AI assumption** (`balance_loop.py`) — what the gauntlet THINKS the player and monster will do

Per-mob behavior cannot be tuned in one place. Fixes to other axes drift back out of sync. **The catalogue must become the single source of truth.**

Gandalf has pre-confirmed Option A (per solutions doc § 10 Q4):
- Catalogue (monster JSON) is THE source of truth for AI behavior fields
- All consumers (engine-sim AI, demo runtime AI, balance loop) read from monster JSON
- Parity-test infrastructure built **now** alongside R3 schema work — cheaper than retrofitting; jack-ryan can use it as continuous-observation tooling

R7 shares the AI behavior schema with R3. Coordinate via MIGRATION.md. Rocket leads schema; star-lord leads parity-test.

## Required reading before starting

**Both, in order:**

1. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` — operating protocol (§ 4.0 autonomous-operation; § 4.5 jack-ryan continuous-observation + Pattern P7 watch; § 5.3 R7 activation requirements; § 9 engineering disciplines — Discipline #11 live-state verification is load-bearing for parity test)
2. `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 7 — R7 specification
3. `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — diagnosis (Axis 5 architectural specifically)
4. `agentic_orchestration/hive-mind/engine-rebuild-log.md` — hive log; acknowledge activation
5. `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md` § 1.3 — R7 deliverables summary
6. `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md` — R3 + R7 share schema; coordinate via MIGRATION.md cadence
7. `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md` — sibling R3 dispatch (shares schema work)
8. `reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` + `fight_engine.py` — engine-sim AI implementation
9. `reincarnated-demo/src/world/aggro.ts` + `world/movement.ts` — demo runtime AI implementation
10. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Pattern P7 (silent-default) is the central failure mode this workstream guards against

## Math-before-code

**Not math-load-bearing**, but **design-then-build pattern applies:**

1. **Parity-test specification** authored before implementation. Path: `reincarnated-engine/design/working-agreement/R7-parity-test-spec-2026-05-19.md`.

   Spec must capture:
   - What the parity test asserts (specific behavioral facets: aggro_radius response distance, leash break behavior, preferred_behavior observable, range_profile distribution)
   - How parity is measured across two dimensional substrates (engine-sim 1D vs demo runtime 2D) — what tolerance is acceptable (±10% per solutions doc § 7 Test 1)
   - Test harness architecture: does parity test instantiate both engines and run mock monster spawn? Or compare emitted telemetry from real fights? Document.
   - Pattern P7 explicit avoidance: the test MUST fail loud on silent-default fallback (no consumer accepting hardcoded TS constant or Python default)
   - Failure reporting: file:line of the divergent consumer (per Test 2 success criterion)

2. **Consumer audit** — both seams enumerate the call sites in their owned code that currently default-fall-back to constants instead of reading from JSON. Star-lord audits `world/movement.ts:74-81` and similar; rocket audits `ai_strategies.py` and `fight_engine.py` call sites. Surface enumeration in `R7-consumer-audit-2026-05-19.md`.

Jack-ryan reviews both before implementation commit.

## Cross-seam contract change? (Principle 6 gate)

**YES** — R7 shares schema with R3 (per solutions doc § 7 "Best run in parallel with R3 since they share the schema work").

**R7-specific cross-seam contracts:**
- Monster JSON AI behavior fields are READ by additional consumer: parity-test infrastructure (new consumer that didn't exist before)
- Demo runtime AI now READS from monster JSON (was hardcoded constants); this is a new cross-repo contract (engine catalogue → demo runtime)
- Parity-test surface is shared by rocket + star-lord; coordinate ownership

**MIGRATION.md:**
- Reuses R3's MIGRATION.md (`reincarnated-engine/src/reincarnated/generation/MIGRATION.md`) for the shared schema; R7-specific additions append as a section
- Star-lord authors parity-test-specific contract notes at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (or telemetry-specific location)

**Cross-repo contract change to demo runtime** is significant — this dispatch authorizes the catalogue → demo runtime read path, but actual demo-side wiring lands in R5 (drax). R7 builds the SOURCE side; R5 builds the CONSUMER side. Coordinate via dispatch chain (R5 dispatch fires when R3+R7 partial-completion checkpoint lands).

The Acceptance criteria below include the round-trip smoke clause.

## Scope (joint rocket + star-lord)

### Rocket scope (schema + engine-sim AI consumption)

- [ ] Parity-test spec authored at `reincarnated-engine/design/working-agreement/R7-parity-test-spec-2026-05-19.md` (joint with star-lord; rocket leads schema, star-lord leads test harness)
- [ ] Consumer audit of engine-sim AI call sites (P7 silent-default enumeration) at `R7-consumer-audit-2026-05-19.md`
- [ ] AI behavior schema fields integrated (shared with R3; coordinate to avoid duplicate authoring)
- [ ] Engine-sim AI (`ai_strategies.py` + `fight_engine.py`) reads from monster JSON instead of hardcoded Python constants
- [ ] Balance loop reads from monster JSON when computing expected behavior
- [ ] No silent-default fallback: missing field triggers schema validation fail-loud (Pattern P7 avoidance)
- [ ] AGENT_STATE.md updated

### Star-lord scope (catalogue + parity-test infrastructure)

- [ ] Parity-test harness implemented (per spec): runs against monster JSON + engine-sim instance + demo runtime mock; asserts behavioral equivalence within tolerance
- [ ] Parity-test discovery: harness scans monster catalogue, picks N monsters, runs parity-check
- [ ] Failure reporting: divergence reported with file:line of offending consumer
- [ ] Parity-test integrated as ongoing CI / smoke check (jack-ryan can use as continuous-observation tool)
- [ ] R7 Test 2 demonstrated: hardcoded TS-constant override in demo causes parity-test failure with file:line report (this test validates the harness itself)
- [ ] Tag: `hive-rebuild/v0.7-r7-parity-test-operational` when harness ships
- [ ] AGENT_STATE.md updated

### Joint scope (hypothesis tests)

- [ ] R7 Test 1 — Change `aggro_radius` in monster JSON from 8m → 12m. Engine sim and demo runtime both reflect new behavior within ±10%. Stored at `reincarnated-engine/output/R7-test1-aggro-radius.md`.
- [ ] R7 Test 2 — Hardcoded TS constant override → parity test fails loudly with file:line. Stored at `reincarnated-engine/output/R7-test2-intentional-break.md`.
- [ ] R7 Test 3 — 3 monsters with distinct `preferred_behavior` (melee_aggressive / ranged_kite / charge_then_melee) produce matching observed behavior on both surfaces. 100% match required. Stored at `reincarnated-engine/output/R7-test3-cross-surface.md`.
- [ ] Tag on hypothesis-test passage: `hive-rebuild/v0.8-r7-hypothesis-test-passed`
- [ ] Smoke-test GREEN throughout
- [ ] Round-trip smoke: monster JSON → engine-sim consumer read → demo runtime consumer read (mock or real); both produce equivalent behavior fingerprint. Field-presence check + behavioral check.

## Acceptance criteria

- [ ] Parity-test spec + consumer audit committed before implementation
- [ ] Engine-sim AI fully consumes monster JSON (no Python-constant fallback)
- [ ] Demo runtime AI prepared to consume monster JSON (R5 dispatch lands the demo-side wiring; R7 builds the source side)
- [ ] Parity-test harness operational; can be run on demand + integrated into smoke flow
- [ ] All 3 R7 hypothesis tests executed + results documented + passage tagged
- [ ] Smoke-test GREEN throughout
- [ ] Round-trip smoke per Principle 6: behavioral fingerprint check across engine-sim + demo runtime (or mock-demo runtime if R5 demo-side wiring not yet landed). **REQUIRED.**
- [ ] MIGRATION.md updated (shared with R3 generation MIGRATION.md; R7-specific section)
- [ ] Both seams' AGENT_STATE.md updated
- [ ] Hive log entries: STATE on each seam's start; HANDOFF when parity test ships; OBSERVATION on any Pattern P7 silent-default discoveries during audit

## Out of scope (explicit non-goals)

- R3 schema authoring itself (rocket schema work belongs to R3 dispatch; R7 consumes the schema from R3)
- Demo-side wiring of monster JSON consumption (R5 — drax seam; depends on R3 + R7 partial-completion)
- 2D spatial sub-gauntlet (R2 — separate workstream)
- Per-tier balance targets (R1 — separate workstream)
- Season-as-emergent-output (R8 — separate workstream)
- Rewriting AI strategies entirely (preserve current strategy semantics; only the source-of-truth read path changes)
- Pattern-B-conditional work (R6; parked)

## Open questions for the agents to resolve (in-seam L1 / cross-seam L2 routing)

- **Parity-test harness architecture** — instantiate-both-engines vs telemetry-comparison-from-real-fights? L1 star-lord with rocket consult; document in spec.
- **Tolerance specification** — ±10% per solutions doc § 7 Test 1; is this acceptable across all 3 tests, or do different behaviors need different tolerances? L1 star-lord; document in spec.
- **Schema field naming** — coordinate with R3 dispatch (rocket leads); avoid duplicate authoring. L2 via knight-rider if conflicts.
- **Consumer audit scope** — does rocket also audit demo runtime TS constants (cross-repo) or is that R5's job? Recommended split: R7 audits engine-side consumers (rocket) + harness scaffolding (star-lord). R5 audits demo-side TS constants (drax). L1 rocket + star-lord; document in audit doc.
- **Demo-side mock for parity test pre-R5** — does parity-test stub the demo-runtime consumer in pre-R5 phase, then swap in real consumer post-R5? L1 star-lord; document in spec.

## References

- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 7 (R7 specification)
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 10 Q4 (Option A pre-confirmed; parity test built now)
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (Axis 5 architectural diagnosis)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 5.3 (R7 activation requirements)
- `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md` (sibling R3 dispatch; shared schema)
- `reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` + `fight_engine.py`
- `reincarnated-demo/src/world/aggro.ts` + `world/movement.ts`
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Pattern P7 silent-default; Discipline #11 live-state verification)

---

## Autonomous-operation authority (no Matt-wait)

Per launch dispatch § 3 + protocol § 4.0:

- **In-seam decisions** — L1 specialist; no escalation
- **Cross-seam decisions (with R3)** — L2 via knight-rider in hive log; coordinate schema cadence
- **Design-direction question** — surface to gandalf via hive log; gandalf decides
- **No Matt-wait at any point during R7.** Matt re-enters only at wind-down.

---

*Authored 2026-05-19 by knight-rider under autonomous-operation authority. The three AIs converge on one source of truth. The parity test makes drift loud. The catalogue becomes canonical for behavior, not just for naming.*
