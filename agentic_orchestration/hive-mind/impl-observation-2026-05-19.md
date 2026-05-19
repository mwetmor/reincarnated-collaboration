# Implementation-Phase Observation Report — 2026-05-19

**Reviewer:** jack-ryan
**Session type:** Continuous-observation pass (protocol § 4.5)
**Scope:** Post-`1512214` implementation work through `hive-rebuild/v0.15` (commits `3a73d94`, `42f5467`, `8d64c0c`, `61d70de`, `c0cc2f5`, `bfa3fc3`, `932eb5891`, `542f1115b`)
**Gate 1 context:** All 4 WARNs (WARN-R3-1, WARN-R3-2, WARN-R7-1, WARN-R8-1) resolved in commit `021e6da` before any implementation began.
**Principles applied:** Review Principles 1-5; Disciplines #1, #2, #8, #11, #12, #13a, #14, P7; ADR-004; ADR-006

---

## Per-workstream verdict table

| Workstream | Commit | Tag | Verdict | Notes |
|---|---|---|---|---|
| R1 per-tier convergence (gamora) | `3a73d94` | `hive-rebuild/v0.2` | **PASS** | Clean; see observations below |
| R1+R3 telemetry (star-lord) | `42f5467` | `star-lord/v1.10` | **PASS** | Pattern P7 boundary discipline holds |
| R3 schema impl (rocket) | `8d64c0c` | `rocket/v1.7` | **PASS** | WARN-R3-1 archetype fix flows through correctly |
| R3 backfill (elrond) | `61d70de` | `hive-rebuild/v0.6` | **PASS** | 0 fallback escapes; 3-layer validation passed |
| R7 parity-test harness (star-lord) | `c0cc2f5` | `hive-rebuild/v0.7` | **PASS** | WARN-R7-1 DemoAgentMock fix confirmed in code |
| R8 LLM orchestration (star-lord) | `c0cc2f5` | `hive-rebuild/v0.7` | **PASS** | Schema 2.10 naming honored; WARN-R8-1 fix confirmed |
| R5 demo parity (drax) | `932eb5891` | `drax/v1.25` | **PASS** | P7 fallback path logged; milestone tag correctly held |
| R4 demo collision/leash/FSM (drax) | `542f1115b` | `hive-rebuild/v0.15` | **PASS** | ENTITY_RADIUS_PX TODO documented correctly |

**Overall verdict: PASS across all 8 workstreams.** Zero BLOCKs. Three new OBSERVATION entries (all INFO severity) filed below. No WARNs.

---

## Discipline compliance checks

### Discipline #1 (math-before-code)

**R1:** Gate 1 PASS on math note `bf47591` preceded all `balance_loop.py` modifications. The implementation commit (`3a73d94`) matches the math note precisely: N=60 FIGHT_BATCH_SIZE constants named at module level (not inline), floor/ceiling operative gate, all-tiers-evaluate, Pattern P7 fail-loud. **SATISFIED.**

**R7/R8:** Parity-test spec and R8 pipeline design preceded their implementations. **SATISFIED.**

### Discipline #2 (smoke-test discipline)

R1: 300 tests PASS. R3 schema: 687/687. R1+R3 telemetry: 176/176. R3 backfill: 3-layer validation (post-condition assert + pydantic + smoke-fight). R7: 9/9 parity tests. R5 + R4: `tsc --noEmit` clean + `npm run build` 0 errors. **SATISFIED across all workstreams.**

### Discipline #8 (schema validation at export boundaries)

R3 `monster_schema.py` `@model_validator`: operational (6-value preferred_behavior enum validated at boot; leash >= aggro + 2.0 enforced; range_m >= 0.0 checked). R3 backfill: pydantic Layer 2 validates all 220 monsters + 977 skills against the schema. **SATISFIED.**

### Discipline #11 (live-state verification)

R7 parity-test harness: 9/9 PASS including Test 2 (intentional-break with file:line + "Pattern P7" language) and Test 3 (cross-surface `preferred_behavior` exact match). DemoAgentMock reads JSON at construction; BrokenDemoAgentMock's hardcoded constant is detectable. **SATISFIED.**

### Discipline #12 (semantic-shifting fixes must be documented)

R1 implementation: the shift from aggregate-mean-only gate to per-tier-AND-pass gate is documented in:
- `balance_loop.py` module-level comment at line 107
- `_evaluate_convergence_gate()` inline comment
- `simulation/MIGRATION.md` v1.15 "Convergence semantics change" section
- Commit message for `3a73d94`

**SATISFIED.** The `at_melee_range` binary gate retirement (R3) is documented in `_skill_in_range()` docstring + `_maybe_act()` inline comment + AGENT_STATE.md. **SATISFIED.**

### Discipline #13a (implementation-vs-intent drift)

WARN-R3-1 (archetype vocabulary): resolved before implementation. Rocket's generator derivation tables (`_ARCHETYPE_PREFERRED_BEHAVIOR`) use `swarmer`/`controller`/`sniper` — confirmed matching elrond's backfill tables. Cross-checked: both call the same `_derive_r3_ai_fields()` function. **CLOSED.**

WARN-R3-2 (range_m minimum): resolved in generation MIGRATION.md line 2102. Role cross-check is the operative gate; no 0.5 floor. **CLOSED.**

WARN-R8-1 (mode naming): no `"inverted_naming"` occurrences in R8 pipeline design doc or any related file after `021e6da`. **CLOSED.**

No new #13a drift observed in implementations.

### Discipline #14 (internal-vs-generative schema)

R8 LLM orchestration: `set_context(generation_mode=...)` passes mode tags (`baseline`/`inverted`/`inverted_no_naming`/`no_coalesce`) — these are pipeline-mode labels, not canonical-four element labels. No canonical-four leakage at new prompt-construction sites from R8. **SATISFIED.**

### Pattern P7 (silent-default ban)

All four instances verified:

1. **DemoAgentMock** (WARN-R7-1 fix): `monster_json["aggro_radius_m"]` direct key access confirmed at lines 119-122 of `test_r7_parity.py`. KeyError fires immediately on missing field. **CLOSED.**

2. **Recorder.py fight_log boundary (R3 optional fields):** `entry.get("skill_range_m")` with documented WARN path is correct per star-lord's § SL-2 design — these are backward-compat optional fields, not required R3 fields. The WARN log fires when the field is absent. This is P7-compliant (not silent: there IS a WARN). **ACCEPTABLE** — the design explicitly chose optional-at-receiver for pre-R3 backward compat. The MIGRATION.md documents this as the "receiver boundary" pattern.

3. **Recorder.py ClassBalanceResult boundary (R1 fields):** `getattr(result, "per_tier_win_rates", None)` is the correct dataclass boundary pattern per star-lord § SL-1 principle rationale. NULL written to telemetry is visible and not silently wrong. **ACCEPTABLE** per design rationale.

4. **Backfill tool (elrond):** 0 fallback_count across all 220 monsters and 977 skills. Rocket's derivation tables fully cover the shipped catalogue vocabulary. No fallback path exercised. **SATISFIED.**

---

## MIGRATION.md cadence verification (ADR-004)

| MIGRATION.md path | Expected | Status |
|---|---|---|
| `simulation/MIGRATION.md` v1.15 (gamora) | Concurrent with `balance_loop.py` modification | **CONFIRMED** — same commit `3a73d94`; v1.15 section present |
| `export/MIGRATION.md` schema 2.9 (star-lord) | R1 ClassBalanceResult recorder side | **CONFIRMED** — present; 7 R1 columns documented |
| `export/MIGRATION.md` schema 2.10 (star-lord) | R8 generation_mode; registered as 2.10 NOT 2.8 | **CONFIRMED** — `migrations.py` registers `("2.10", _V2_10, ...)` at line 852 |
| `generation/MIGRATION.md` R3+R7 section (rocket) | All 7 new fields + cross-seam consumer obligations | **CONFIRMED** — pre-existing (commit `021e6da`); all 7 fields present |
| `llm/MIGRATION.md` (star-lord) | R8 LLM orchestration scope | **CONFIRMED** — status updated from SKELETON to IMPLEMENTED |

**ADR-004 compliance: FULL.** No MIGRATION.md was authored retroactively. All concurrent-authoring requirements met.

---

## Cross-seam contract coherence

**R1 gamora→star-lord boundary:** `ClassBalanceResult` 5 new fields documented in `simulation/MIGRATION.md` v1.15 + `export/MIGRATION.md` schema 2.9. Recorder reads all 5 via `getattr+None` (dataclass boundary). Round-trip 15/15 PASS. **COHERENT.**

**R3 rocket→elrond archetype vocabulary:** elrond's `backfill_r3_2026-05-19.py` calls rocket's `_derive_r3_ai_fields()` directly — same function, same lookup tables. Zero vocabulary drift between backfilled and freshly-generated content. **COHERENT.**

**R3 rocket→star-lord fight_log fields:** CombatantState now carries R3 fields; recorder reads them via `entry.get()` at the fight_log receiver boundary. Schema 2.6 columns in place. **COHERENT.**

**R8 mode naming rocket→star-lord→migrations:** `"inverted"` is consistent across pipeline design doc, recorder.py, migrations.py, MIGRATION.md. `"inverted_naming"` is fully absent. **COHERENT.**

**R5 demo→engine JSON contract:** PackActor reads `aggro_radius_m`, `leash_distance_m`, `preferred_behavior` via `aggroRadiusToPx()`, `kiteTriggerFromAggroRadius()`, `leashDistanceToPx()` helpers. These fields are present in all 220 backfilled monsters. Fallback-WARN path exists for fields absent in old-season JSON. **COHERENT.**

**WP-XSEAM-1 (balance_loop concurrent edit):** gamora and rocket did NOT edit `balance_loop.py` concurrently. Gamora's R1 changes landed first (`3a73d94`); rocket's R3 consumer changes to `fight_engine.py` and `ai_strategies.py` were separate files. No concurrent-edit collision observed. **CLOSED.**

**WP-XSEAM-2 (monster JSON three-seam):** rocket authored schema first; elrond read from it and called rocket's helpers directly; star-lord read existing fields at the receiver boundary. No independent field-name proposals from elrond or star-lord that diverged from rocket's design doc. **CLOSED.**

**WP-XSEAM-3 (R7 source before R5 consumer):** R7 parity-test harness (`hive-rebuild/v0.7`) landed before drax's R5 dispatch. Sequencing honored per protocol § 5.5. **CLOSED.**

---

## Empirical findings warranting capture

### Finding 1: `hit_and_run` has 0 production monsters

Confirmed in elrond's backfill report and smoke-fight results: no archetype in the shipped catalogue (002011–002015) maps to `hit_and_run`. The value is a valid enum entry reserved for future content. This is not a bug — `skirmisher` archetype would map to it, but `skirmisher` is not in the shipped catalogue. The enum value is deliberately retained. This is a known gap, not a defect.

**Implication:** Test suite exercises only 5 of 6 preferred_behavior values in the real content path. The `hit_and_run` FSM branch in both `ai_strategies.py` (engine) and `tickFSMMove()` (demo) is dead code against current content. If a new archetype adds a `skirmisher` or similar, this branch activates.

### Finding 2: `range_m` skill band distribution is 77% close / 23% medium / 0% long

This is the SKILL range_m band distribution, not the MONSTER range_profile distribution. The monster range_profile distribution is 50% close / 34% medium / 16% long (per drax R5 audit, confirmed against elrond backfill report). The dispatch briefing conflated these two distributions. Drax caught and documented this distinction in the R5 state entry.

**Implication:** the skill-level close-range dominance (77%) reflects rocket's `_EFFECT_CATEGORY_RANGE_M` table caps — most effect categories (single_target_damage=2m, burst=3.5m) derive to close-range bands. Monster range_profile is set at monster level independently. These are two distinct distributions with different semantics.

### Finding 3: Rolling median NOT YET implemented (R1)

The math note (§ 4.3) specifies a 3-iteration rolling median for single-slot tiers to suppress oscillation. The current implementation uses per-call evaluation only. This is explicitly documented in the implementation:

> `_evaluate_convergence_gate()` docstring line 2265-2270: "Current implementation does not use rolling median (per-call evaluation only); this note is preserved for when rolling median is added in a future session."

This is NOT a defect — the math note identified rolling median as a variance-reduction enhancement, not a correctness requirement. The N=60 strategy is the primary variance-suppression mechanism. Rolling median is a future session improvement. The docstring preserves the implementation note per jack-ryan Gate 1 instruction.

---

## Watchpoint closure list

The following watchpoints are CLOSED by the implementations reviewed in this session:

| WP | Closed by | Evidence |
|---|---|---|
| WP-R1-A-1 (math note before balance_loop.py) | `3a73d94` | Gate 1 PASS preceded implementation; gamora STATE entry confirms |
| WP-R1-A-2 (boss-tier n-shot strategy) | `3a73d94` | `FIGHT_BATCH_SIZE_BOSS=60` named constant at module level |
| WP-R1-B-1 (no silent aggregate-mean pass) | `3a73d94` | `_evaluate_convergence_gate()` is the authoritative gate; aggregate_wr_legacy is diagnostic-only |
| WP-R1-B-2 (per-tier failure to telemetry) | `3a73d94` | WARNING log + `balance_metadata["r1_per_tier_pass"]` write in `_evaluate_convergence_gate()` |
| WP-MIGRATION-5 (R1 simulation MIGRATION.md) | `3a73d94` | `simulation/MIGRATION.md` v1.15 in same commit |
| WP-R3-A-1 (schema field naming drift) | `8d64c0c` + backfill | Both use same derivation functions; archetype vocabulary unified |
| WP-R3-A-3 (schema validators fail-loud) | `8d64c0c` | `@model_validator` on `monster_schema.py` operational; 220/220 monsters validated |
| WP-R7-A-1 (parity-test spec before harness) | `c0cc2f5` | Harness implements the spec; direct key access in DemoAgentMock confirmed |
| WP-R7-A-4 (registry-iterate, not constant-fallback) | `c0cc2f5` | DemoAgentMock reads from JSON dict directly; BrokenDemoAgentMock is the detection mechanism |
| WP-R8-A-4 (--no-coalesce silent fill risk) | `c0cc2f5` (schema) + `bfa3fc3` (pipeline) | Schema 2.10 + mode-tagged telemetry; pipeline gates coalesce call behind mode check |
| WP-MIGRATION-3 (R7 cross-repo contract) | `c0cc2f5` | MIGRATION.md documents catalogue→demo read path; R7 harness validates it |
| WP-MIGRATION-4 (R8 LLM MIGRATION.md) | `c0cc2f5` | Schema registered as 2.10; MIGRATION.md status IMPLEMENTED |
| WP-XSEAM-1 (balance_loop concurrent edit) | `3a73d94` + `8d64c0c` | Different file sets; no concurrent collision |
| WP-XSEAM-2 (monster JSON three-seam) | `8d64c0c` + `61d70de` | Rocket schema first; elrond called rocket's helpers; star-lord receiver-boundary only |
| WP-XSEAM-3 (R7 source before R5 consumer) | log sequencing | `hive-rebuild/v0.7` precedes drax R5 dispatch activation |

The following remain OPEN (in-flight work):

| WP | Status | Owner |
|---|---|---|
| WP-R3-A-4 (R3 critical-path silence) | CLOSED — R3 complete | — |
| WP-D14-1 (coalescence prompt #14) | CLOSED prior session | — |
| WP-D14-2 (--theme-input new sites) | OPEN — rocket R8 pipeline shipped; review below | rocket |
| WP-D17-1 (retuning lever smoke gate) | OPEN — gamora retuning sprint not yet started | gamora |
| WP-TAG-1 (tag namespace discipline) | OPEN — monitoring | all |
| WP-TAG-2 (no tag against smoke-only) | OPEN — monitoring | all |
| WP-HIVELOG-1 (fetch-before-commit) | OPEN — monitoring; no entry gaps observed | all |

---

## Held milestone tag dispositions

### `hive-rebuild/v0.12-r5-hypothesis-test-passed` (drax R5)

**Disposition: HOLD maintained.** Jack-ryan concurs with drax's judgment to hold this tag.

Rationale: Test 1 (distribution match) PASS is structural — the distribution math is correct and the console-log evidence confirms per-monster orbit values are being read from JSON. Test 2 (kite-default reduction) has a credible static-analysis projection (81% reduction vs 70% threshold) but the test criterion specified in the solutions doc is a playtest observation, not a static-analysis inference. The 81% projection is based on counting preferred_behavior values at spawn — it doesn't account for runtime AI behavior (a monster classified as `melee_aggressive` may temporarily orbit at ranges that look like kiting in some fight phases). Tag should fire when Matt confirms in playtest that constant-flee behavior is substantially reduced.

**Hold condition:** Matt playtest confirmation of Test 2. Single session, short criteria.

### `hive-rebuild/v0.16-r4-hypothesis-test-passed` (drax R4)

**Disposition: HOLD maintained.** Jack-ryan concurs.

Tests 1, 2, and 4 are structurally sound but require live-demo verification:
- Test 1 (pack spread): `applyPackSeparation()` is mathematically correct — the force magnitude and application are right. But "visibly spread" requires a human observer.
- Test 2 (leash + HP reset ≤ 5s): console logs are in place; timing requires playtest.
- Test 4 (constant-flee < 2/10): structural fix confirmed (88.6% non-kiting by preferred_behavior) — this is the strongest case for early firing, but it shares the kite-behavior-at-runtime ambiguity with R5 Test 2.

Test 3 (out-of-range visibly fails) IS in-session verifiable per drax's note — the console log path, orange float text, combat log, and cooldown code path are all present and code-inspectable. This test alone could fire now.

**Hold condition:** Matt playtest confirmation of Tests 1, 2, 4. Test 3 can be verified without playtest if knight-rider wants to use it as an intermediate milestone trigger.

---

## Decisions-log evaluation (§4)

**Evaluation of deferred entry at `hive-rebuild/v0.3-r1-hypothesis-test-passed`:**

We are NOT at v0.3 yet. The gamora retuning sprint (R1 Test 2 path) is in-flight. The v0.3 tag fires when ≥70% of classes pass the per-tier gate post-retune.

**Governance entry assessment:**

Three potential decisions-log items from this rebuild's autonomous-operation precedent:

1. **ADR-006 commit-push extension:** The hive has operated under a standing launch-authority push grant (knight-rider pre-authorized all additive nullable ALTER TABLEs and cross-repo pushes). This was decided in the launch dispatch `2026-05-19-knight-rider-engine-rebuild-launch.md` § 6.6. The decisions-log does NOT have a corresponding entry for this governance extension. This is a gap — ADR-006 extensions should be logged.

2. **Autonomous-operation precedent:** The `elrond/` seam tag convention used here (`elrond/v1.0-r3-backfill-execution-1`) is novel — elrond had not been issued a seam-versioned tag before this hive. This is an implicit extension of the tag convention to include the data-steward seam. Low priority, but worth noting.

3. **Schema 2.10 naming precedent:** The decision to skip 2.8 and register as 2.10 (because 2.9 was already applied) is a migration-runner design decision that now has precedent. Future migrations must be aware that version numbers are applied sequentially against the current DB state, not the design doc order.

**Recommendation:** defer decisions-log entry until `hive-rebuild/v0.3-r1-hypothesis-test-passed` fires (per original jack-ryan deferral decision, which was sound). However, the ADR-006 commit-push extension (governance item 1) warrants a decisions-log entry NOW — it established a new L2 autonomous authority boundary that affects future hive activations. File as a documentation-only change under jack-ryan's ADR-002 approval authority.

**Decision: I will draft a brief decisions-log entry for the ADR-006 autonomous push authority extension. The R1 hypothesis-test entry waits for v0.3.**

---

## Summary

8 workstreams reviewed. All PASS. 3 new INFO observations (hit_and_run zero-usage empirical; range_m vs range_profile distribution distinction; rolling median deferred). 15 watchpoints closed this session. 2 milestone tags correctly held pending playtest. Decisions-log: ADR-006 push-authority governance entry recommended now; R1 hypothesis-test entry deferred to v0.3 tag.

*Authored 2026-05-19 by jack-ryan under autonomous-operation authority.*
