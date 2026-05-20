# Hive-Mind Operating Protocol — Per-Tier Convergence + Recompose Validation (the new tuning mechanism test)

**Authority:** Matt (mhwetmore@gmail.com), 2026-05-19 late evening — directive: *"Can you please author a new hive-mind to test this hypothesis and continue through with further development towards the new gauntlet as a tuning mechanism as you have laid out, finally testing a true season in this way?"*

**Author:** gandalf (story-and-design steward).

**Status:** **Canonical operational protocol** for the third hive-mind activation. Activates on Matt's directive to a fresh knight-rider session (the engine-rebuild hive's knight-rider is being stood down per Matt directive same evening). Distinct mission scope from engine-rebuild; inherits operating mechanics from `canonical/story/archived/hive-mind-protocol-2026-05-17.md` + `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 (autonomous-operation framing).

**Reading order:** § 0 TL;DR → § 1 The hypothesis under test → § 2 Why this is distinct from engine-rebuild → § 3 Mission scope (six phases) → § 4 Coordination matrix → § 5 Mechanics inheritance → § 6 Per-phase activation requirements → § 7 Wind-down + completion triggers → § 8 Pattern-B parking dependency (unchanged) → § 9 Activation checklist → § 10 Cross-references.

---

## § 0 — TL;DR

**The third hive-mind activation. Mission: validate that per-tier convergence with recompose enabled produces a shippable season — and ship that season under the new tuning mechanism.**

The previous hive (engine-rebuild + Phase D R2+ST math investigation) revealed an architectural insight that crystallized in Matt's late-evening framing:

> *"We may be running a fully converged season against a new tuning mechanism (new gauntlet) and asking: why doesn't this tune?"*

The shipped catalogue + S1 first-batch + S1 retry-1 all show "saturate-low + collapse-boss" not because kits are broken but because **the kits were converged for the OLD contract (aggregate-mean WR) and are being measured against the NEW contract (per-tier WR bands).** Single-modifier scaling cannot bridge this composition mismatch. **The recompose mechanism IS the bridge** — it varies kit composition (not just modifier) — but it's architecturally blocked by the floor-lock that prevents modifier from reaching the signal range where recompose operates.

**This hive's mission: unblock recompose (Option A), refine the trigger (Option B), and run a fresh season under per-tier convergence with recompose enabled. If the math we've laid out tonight is right, the season will converge naturally.**

Six phases total:
- **P0 — Option A floor widening** (unblocks recompose; HELD dispatch already authored)
- **P1 — Option B recompose-trigger re-conditioning** (architectural fix; gandalf design + jack-ryan critique + gamora implementation)
- **P2 — Fresh diagnostic regen** (single season under per-tier convergence + recompose; measure whether recompose fires + produces per-tier-satisfying kits)
- **P3 — Validation synthesis** (gandalf judgment: did the new mechanism work?)
- **P4 — Ship a true season** (if P3 validates; full production-grade regen under new mechanism)
- **P5 — Document + canonical record** (decisions-log, engineering-disciplines, hive-runs review)

Total wall time estimate: 4-7 days at full parallelization; 10-14 days serial.

**Mission scope is FIXED at these six phases.** Pattern-B remains parked (`agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`). The previous hive's findings (R2+ST math; engine-rebuild closure) stand as canonical context; this hive does not re-litigate them.

---

## § 1 — The hypothesis under test

**Hypothesis H_RC (the recompose-as-lever hypothesis):** *Per-tier WR target convergence is satisfiable for the existing generation rules — IF the recompose mechanism can fire. The composition variation that recompose produces is the lever that bridges the contract mismatch between aggregate-mean (old) and per-tier WR bands (new). The mechanism has been architecturally blocked since the per-tier targets were authored; once unblocked, fresh regens under per-tier convergence will produce shippable kits naturally.*

**Null H_RC_0:** *Even with recompose unblocked, per-tier convergence does not produce shippable kits. The generation rules themselves (archetype templates, AOE share floors, role multipliers) require revision — recompose can't fix kit composition that's structurally incompatible with per-tier targets.*

**Test:** Phase 2 fresh regen + Phase 3 synthesis. If the regen produces ≥ 60% kit-acceptable (all per-tier targets passed) at convergence, H_RC is supported. If it produces < 60% kit-acceptable, H_RC_0 cannot be rejected and generation-rule revision (Phase 5+ follow-on) becomes the actual fix.

**Confidence threshold for "ship the season":**
- **PASS strong:** ≥ 80% kit-acceptable → ship the season; declare new convergence mechanism validated
- **PASS moderate:** 60-80% kit-acceptable + diagnosable failures → ship partial; flag failing kits for kit-redesign queue
- **CANNOT REJECT NULL:** < 60% kit-acceptable → P4 ship gate fails; surface to Matt with generation-rule-rewrite as next architectural question

This is math-before-code-then-code-with-validation, structured. Each phase has an explicit gate to the next.

---

## § 2 — Why this is distinct from the engine-rebuild hive

The engine-rebuild hive (2026-05-19, first activation) accomplished:
- 7 workstreams shipped (R1, R2, R3, R5, R7, R8 + Option-A-prep + Phase D math investigation)
- Engine-rebuild batch closed at `hive-rebuild/v1.0-engine-rebuild-complete`
- VS2a kickoff completed
- Phase D math investigation produced the **insight** that this new hive operationalizes

This new hive is the **direct architectural follow-on** to that insight. It takes the synthesis ("we're running converged content against a new contract; recompose is the bridge that's blocked") and runs it through to shippable production.

Distinction summary:
- **Engine-rebuild:** measured the problem; established the contract; surfaced the lever-blocking
- **This hive (recompose validation):** unblocks the lever; tests whether the lever produces shippable kits; ships if it does

This is *not* a sequence of more engine-rebuild experiments. It is a focused validation + production cycle for the architectural insight that emerged from the engine-rebuild.

---

## § 3 — Mission scope (six phases)

### Phase 0 — Option A floor widening (unblock recompose)

**Owner:** gamora (4-line change + smoke gates + diagnostic stop-gap regen).
**Pre-authored:** dispatch HELD at `agentic_orchestration/dispatches/HELD-2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` — gandalf CONCUR + jack-ryan APPROVE-WITH-AMEND (4 amendments folded).
**Effort:** ~4 hours gamora.
**Deliverable:** modifier search floor widened from 0.05 to 0.01; named constant `MODIFIER_SEARCH_FLOOR` per Discipline #18; smoke gates A1/A2/A3 + MIGRATION.md note; stop-gap regen of 3 diagnostic seasons; `modifier_extreme_low` telemetry flag.
**Acceptance gate to Phase 1:** binary search can demonstrably reach modifier < 0.05 (confirmed by stop-gap regen telemetry); no test-assertion regressions (A2 BLOCKING smoke).
**Acceptance tag:** `recompose-hive/v0.1-option-a-floor-widened`.
**Discipline anchor:** #1 (math-before-code; the math already supports Option A per gamora's investigation).

### Phase 1 — Option B recompose-trigger re-conditioning

**Owner:** gandalf (design brief) + jack-ryan (Gate-1 critique) + gamora (implementation).
**Effort:** ~6-10 hours total (gandalf 1-2h design; jack-ryan 1-2h critique; gamora 4-6h implementation + smoke).
**Deliverable:** re-condition `MODIFIER_LOW_THRESHOLD=0.30` trigger to ALSO fire on `status=failed AND eval_modifier ≤ MODIFIER_SEARCH_FLOOR + epsilon`. This lets B14.5 V1 catch floor-lock cases (now reachable post-Option-A) and re-author kits with lower damage density via recompose levers. 25-50 LOC change per gamora's investigation § 5. Includes:
  - Re-condition logic in `balance_loop.py` recompose trigger
  - Smoke gate B1: confirm recompose fires at modifier=0.02-0.04 on test class (per gamora investigation acceptance condition)
  - MIGRATION.md note (semantic shift per Discipline #12; signal-range expanded)
  - Test additions verifying trigger fires correctly
**Acceptance gate to Phase 2:** at least 1 test class demonstrably triggers recompose at modifier < 0.05 (proves the unblocking worked); recompose levers produce non-zero delta at the widened-floor modifier.
**Acceptance tag:** `recompose-hive/v0.2-option-b-recompose-conditioned`.
**Discipline anchor:** #12 (semantic shift; documented in MIGRATION.md).

### Phase 2 — Fresh diagnostic regen (the actual test)

**Owner:** rocket (generation) + star-lord (telemetry) + gamora (convergence loop).
**Effort:** ~4-6 hours (regen + telemetry analysis).
**Deliverable:** ONE fresh season regenerated under:
  - R8-inverted pipeline (engine default per R8 disposition)
  - Per-tier WR convergence target structure (R1 disposition canonical)
  - Option A floor widening ACTIVE
  - Option B recompose trigger ACTIVE
  - Disposition-3 calibration (boss HP × 0.40, armor × 0.45, 240s timeout) ACTIVE
  - All other engine state at current HEAD

Seed: 100005 (next available diagnostic seed; not used in any prior batch). Substrate: gandalf chooses (suggested: a substrate that's been "challenging" in prior runs — earth or shadow — so the test covers archetypes with known difficulty rather than just easy cases).

Output telemetry per class (recorded during convergence):
- Final modifier
- Per-tier WR at final modifier
- Recompose trigger fire-count
- Per-trigger: delta achieved by recompose levers
- Convergence status (converged / partially-converged / failed_regenerate)

Output classification per class (rocket + star-lord post-convergence):
- kit-acceptable (all 5 per-tier targets met)
- kit-mediocre (1-2 tier failures, recompose-recoverable)
- kit-broken (3+ tier failures or modifier-saturated; recompose-irrecoverable)

**Acceptance gate to Phase 3:** the regen completes (all classes either converge or are flagged as failed_regenerate); telemetry is complete; per-class classification is reproducible from canonical output files (Discipline #11 + the new "completion-record-figure-must-be-reproducible" candidate discipline from the engine-rebuild retrospective).
**Acceptance tag:** `recompose-hive/v0.3-diagnostic-regen-complete`.
**Discipline anchor:** #11 (empirical inspection); the new candidate discipline on reproducible completion-record figures.

### Phase 3 — Validation synthesis (the verdict)

**Owner:** gandalf (synthesis) + jack-ryan (Gate-2 critique).
**Effort:** ~2-4 hours.
**Deliverable:** canonical findings document at `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` covering:
  - Per-class classification results (kit-acceptable / mediocre / broken)
  - Population-level pass rate (% kit-acceptable)
  - Verdict on H_RC vs H_RC_0
  - Per-failure-mode analysis (if any failures occurred): which sub-pattern (floor-lock-still-active, recompose-couldn't-recover, generation-rule-pathology, etc.)
  - Recommendation: ship to P4 OR diagnose further OR surface to Matt
**Acceptance gate to Phase 4:** verdict is PASS strong (≥ 80%) OR PASS moderate (60-80%) with diagnosable failures. If CANNOT REJECT NULL, P4 doesn't fire; surface to Matt for direction.
**Acceptance tag:** `recompose-hive/v0.4-validation-verdict`.

### Phase 4 — Ship a true season (the deliverable)

**Owner:** rocket (full season generation) + gamora (convergence) + star-lord (telemetry + export) + drax (loadout sync if needed).
**Effort:** ~8-12 hours.
**Deliverable:** a complete production-grade season — NOT diagnostic. Specifically:
  - Full class set per gandalf's chosen substrate roster (typically 10-12 classes for a season)
  - Full monster bestiary
  - Full gear catalog
  - Full LLM cosmology coalescence (inverted-mode naming, since that's the engine default)
  - All standard season artifacts (manifest.json, validation_report.json, etc.)
  - Per-class per-tier WR confirmed in band post-convergence
  - Recompose telemetry recorded for canonical record
  - **This is the "true season" Matt named in the directive** — the first season produced under the new tuning mechanism end-to-end
**Acceptance gate to Phase 5:** the season passes validation_report; per-tier WR distribution is in band for ≥ 80% of classes; cosmology + naming pass cohesion judgment ≥ 4.0; gear + monster sets are coherent.
**Acceptance tag:** `recompose-hive/v1.0-true-season-shipped`.
**This is the load-bearing deliverable.** If this ships, the new tuning mechanism is validated; the architectural critique tonight is resolved.

### Phase 5 — Canonical record + wind-down readiness

**Owner:** gandalf (canonical authorship) + jack-ryan (decisions-log entry) + knight-rider (CHANGELOG + state-of-hive).
**Effort:** ~4-6 hours.
**Deliverable:**
  - Updated `canonical/16-project-roadmap.md` reflecting the new tuning-mechanism validation
  - Decisions-log entry in `reincarnated-engine/design/decisions/decisions-log.md` capturing the architectural disposition (per-tier targets + recompose as canonical tuning mechanism going forward)
  - Engineering-disciplines.md amendment if any new pattern emerged (e.g., "lever-unblocking before testing" as a discipline?)
  - Hive-runs review updated (`agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html` → v5 with this hive's findings folded in)
  - State-of-hive at hive end
  - Retrospective at `agentic_orchestration/hive-mind/retrospective-recompose-validation.md`
**Acceptance gate:** all documents committed + pushed; Pattern-B PARKED thread updated (no changes; just confirmation it remains parked).
**Acceptance tag:** `recompose-hive/v1.1-canonical-record-complete`.

---

## § 4 — Coordination matrix

Per-deliverable seam assignment. Knight-rider maintains; specialists consult before cross-seam-impacting work.

| Phase | Rocket | Gamora | Star-lord | Drax | Jack-ryan | Gandalf |
|---|---|---|---|---|---|---|
| **P0 — Option A floor widening** | — | **OWNER** | telemetry consumer | — | smoke audit | spec input |
| **P1 — Option B recompose-conditioning** | — | **OWNS implementation** | telemetry consumer | — | **Gate-1 critique** | **design brief author** |
| **P2 — Fresh diagnostic regen** | **OWNS generation** | **OWNS convergence** | **OWNS telemetry + classification** | — | observes; spot-checks | watches; advises on substrate choice |
| **P3 — Validation synthesis** | reads | reads | reads | — | **Gate-2 critique** | **OWNS synthesis** |
| **P4 — True season ship** | **OWNS generation** | **OWNS convergence** | **OWNS telemetry + export** | **syncs loadout if needed** | observes ship-gate | watches cosmology cohesion |
| **P5 — Canonical record** | — | — | — | — | **OWNS decisions-log** | **OWNS canonical authorship** |

Knight-rider routes cross-seam coordination throughout; manages tag-firing + push discipline per standing ADR-006 amendment authority.

---

## § 5 — Mechanics inheritance

**All operating mechanics from `canonical/story/archived/hive-mind-protocol-2026-05-17.md` and `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` are inherited as-is.** Specifically:

### From 2026-05-17 (archived) — operating mechanics

§ 3 (Distributed authority L1/L2 with L3 routing changed per below), § 4 (Communication discipline — hive log + state-of-hive cadence), § 5 (Cadence + tagged checkpoints), § 6 (Cross-seam coordination via MIGRATION.md), § 7 (Continuous QA loop with jack-ryan continuous-observation), § 8 (Failure mode protocols), § 9 (Reversibility + tagged checkpoints), § 10 (Mission and scope discipline; scope is FIXED at the six phases).

### From engine-rebuild (2026-05-19) — autonomous-operation amendment

§ 4.0 AUTONOMOUS OPERATION: no L3-to-Matt during operation; SME agents decide within seams; gandalf decides cross-cutting design/canonical/architectural; knight-rider decides orchestration; Matt re-enters only at wind-down OR completion. **This is the authority pattern for the new hive.**

### Operational artifacts (new for this hive)

- **Hive log:** `agentic_orchestration/hive-mind/recompose-validation-log.md` (new; append-only)
- **State-of-hive cadence:** daily `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD-recompose-validation.md`
- **Scope-of-work:** `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` (knight-rider authors at activation)
- **Tag namespace:** `recompose-hive/v<X.Y>-<milestone>` (distinct from `hive-rebuild/v<X.Y>` engine-rebuild + `vs2a/v<X.Y>` VS2a)

---

## § 6 — Per-phase activation requirements

Phase 0 fires immediately after hive activation. Subsequent phases fire on their respective acceptance gates.

**P0 (Option A):**
- Read the HELD dispatch in full
- Confirm gamora has bandwidth (no in-flight conflicts with sim code)
- Fire gamora; await smoke gates A1/A2/A3 + stop-gap regen
- On acceptance: fire P0 tag; route to P1

**P1 (Option B):**
- P0 acceptance confirmed
- Gandalf authors design brief: where the trigger re-conditions; what signal range engages; what smoke gates apply
- Jack-ryan Gate-1 critique
- Gamora implements per brief + critique amendments
- Fire gamora; await smoke gate B1
- On acceptance: fire P1 tag; route to P2

**P2 (Fresh diagnostic regen):**
- P1 acceptance confirmed
- Gandalf picks substrate (suggested: earth or shadow for difficulty)
- Knight-rider authors rocket + star-lord + gamora dispatch
- Fire; await regen completion + telemetry
- On acceptance: fire P2 tag; route to P3

**P3 (Validation synthesis):**
- P2 acceptance confirmed
- Gandalf synthesizes per-class classification + verdict
- Jack-ryan Gate-2 critique
- If PASS: fire P3 tag; route to P4
- If CANNOT REJECT NULL: fire P3 tag with verdict; SURFACE TO MATT for direction; P4 does not fire autonomously

**P4 (Ship true season):**
- P3 PASS verdict confirmed
- Gandalf finalizes substrate + roster + season-naming intent
- Knight-rider authors full-season dispatch
- Fire rocket + gamora + star-lord; await full season validation
- Drax sync if loadout needs updating
- On acceptance: fire P4 tag; route to P5

**P5 (Canonical record):**
- P4 acceptance confirmed
- Gandalf + jack-ryan + knight-rider author per § 3 deliverables
- On completion: fire P5 tag; declare hive complete; surface to Matt at his next session

---

## § 7 — Wind-down + completion triggers

**Per Matt directive 2026-05-19 (autonomous-operation; engine-rebuild protocol § 4.0):**

Wind-down OR completion triggers (the hive stops at any of these):

1. **Matt declares explicit wind-down** — execute clean handoff per protocol § 4.9 (commit in-flight to safe checkpoint; ship state-of-hive; deactivate)
2. **P5 completion** — all six phases complete; canonical record filed; true season shipped; surface to Matt at his next session; deactivate
3. **P3 CANNOT REJECT NULL verdict** — H_RC refuted; surface to Matt with diagnosis; P4 doesn't fire; hive deactivates pending Matt direction on next architectural step (kit-redesign queue / generation-rule rewrite / etc.)
4. **Hard architectural blocker** — if at any phase an unforeseen architectural issue surfaces that the autonomous-operation framework can't dispose (e.g., recompose triggers BUT levers produce signal range issues OTHER than floor-lock), surface to Matt via Matt briefing in `agentic_orchestration/matt-briefing-recompose-validation-2026-05-XX.md`

**Knight-rider does NOT surface to Matt during normal operation.** SME findings + gandalf dispositions resolve within the hive. Matt re-enters only at the four trigger conditions above.

---

## § 8 — Pattern-B parking dependency

Pattern-B commercial direction remains PARKED per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. R6 (host-calibration protocol) does NOT enter this hive's dispatch cycle. **Engine-side work is the entire scope.**

If Pattern-B resolves during this hive's operation, R6 enters dispatch cycle after this hive completes, not during.

---

## § 9 — Activation checklist

The new hive activates when ALL of the following are true:

### § 9.1 — Pre-activation (gandalf, this session, COMPLETE)

- [x] This protocol authored (above)
- [x] Mission scope locked (six phases)
- [x] Hypothesis H_RC + H_RC_0 formalized
- [x] Coordination matrix authored
- [x] Mechanics inheritance documented
- [x] Engine-rebuild knight-rider stand-down (handled by Matt — separately directing the prior knight-rider session to deactivate)
- [ ] Knight-rider launch dispatch authored (next deliverable; see `agentic_orchestration/dispatches/2026-05-19-knight-rider-recompose-validation-hive-launch.md`)

### § 9.2 — Knight-rider activation (Matt fires fresh knight-rider window)

- [ ] Matt opens fresh knight-rider session in new window (NOT the wound-down engine-rebuild session)
- [ ] Matt pastes launch prompt pointing at the launch dispatch
- [ ] Knight-rider reads launch dispatch + this protocol + the HELD Option A dispatch
- [ ] Knight-rider tags pre-hive baseline: `recompose-hive/v0.0-pre-activation`
- [ ] Knight-rider creates hive log + scope-of-work + coordination matrix snapshot
- [ ] Knight-rider broadcasts activation in hive log
- [ ] Knight-rider routes P0 dispatch (Option A) immediately

### § 9.3 — Specialist readiness

Each engineering specialist (rocket, gamora, star-lord, drax) confirms in hive log when first commissioned:
- [ ] Read this protocol
- [ ] Read the launch dispatch
- [ ] Identify any in-flight work conflicts
- [ ] Acknowledge

Jack-ryan: continuous-observation rhythm established at P0 activation.
Gandalf: available for design-direction support throughout; primary author of P1 brief + P3 synthesis.
Galadriel: NOT in scope (no visual benchmark work this hive); sub-agent restriction remains operative per her agent definition.

### § 9.4 — Matt activation

- [ ] Matt confirms hive activation by firing knight-rider with the launch prompt
- [ ] Matt steps back; autonomous operation runs
- [ ] Matt re-enters at one of the four wind-down/completion triggers

---

## § 10 — Cross-references

**Mission inputs:**

- This protocol (mission scope + authority + phases)
- `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` — the AMENDED canonical findings doc with Matt's methodological correction; contains the architectural insight this hive operationalizes
- `agentic_orchestration/dispatches/HELD-2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` — Phase 0 dispatch ready to fire
- `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` — gamora's investigation establishing Option A + Option B math
- `canonical/story/r1-firstbatch-fail-disposition-2026-05-19.md` (or `s1-firstbatch-fail-disposition-2026-05-19.md`) — gandalf's S1 failure disposition + § 11 staged-approval amendment
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — the original 5-axis gap diagnosis
- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` — the queue this hive's success would render mostly unnecessary

**Mechanics inheritance:**

- `canonical/story/archived/hive-mind-protocol-2026-05-17.md` — Phase-1 P1 protocol (first activation); mechanics layer load-bearing
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` — engine-rebuild protocol (second activation); autonomous-operation amendments
- This protocol — recompose-validation hive (third activation)

**Operational artifacts (created at activation):**

- `agentic_orchestration/hive-mind/recompose-validation-log.md`
- `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md`
- `agentic_orchestration/hive-mind/coordination-matrix-recompose-validation.md`
- `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD-recompose-validation.md`
- `agentic_orchestration/hive-mind/retrospective-recompose-validation.md` (at P5)

**Adjacent state:**

- `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md` — remains parked
- `agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html` — will be updated to v5 at P5 with this hive's findings folded in
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — may receive new discipline entry at P5

---

## § 11 — The wizard's note

The previous hive measured the problem. This hive ships the fix.

The fix isn't a different gauntlet, isn't a different modifier scalar, isn't a different damage multiplier. **The fix is letting the architecture's existing composition lever (recompose) operate as designed** — which has been blocked since the per-tier targets were authored.

Phase 0 unblocks. Phase 1 sharpens. Phase 2 tests. Phase 3 verdict. Phase 4 ships. Phase 5 records.

If H_RC holds, the kit-redesign queue, the AOE-skew finding, the spatial-calibration question, the modifier-sweep — all of these become moot. The architecture worked all along; we just couldn't see it because we couldn't let it work.

If H_RC fails, we have the cleanest possible diagnosis of where the actual pathology lives — and the next architectural decision becomes obvious.

Either outcome resolves a major open question. Both outcomes are valuable.

*Authored 2026-05-19 late evening by gandalf. The third hive activation. Mission: validate the new tuning mechanism by shipping a true season under it. Mithrandir signs the protocol; the road awaits the launch.*
