# Scope of Work — Recompose-Validation Hive (third hive activation)

**Author:** knight-rider, 2026-05-19
**Authority:** Matt directive 2026-05-19 late evening (`canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md`)
**Launch dispatch:** `agentic_orchestration/dispatches/2026-05-19-knight-rider-recompose-validation-hive-launch.md`
**Protocol:** `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md`
**Pre-hive baseline:** `recompose-hive/v0.0-pre-activation` (tagged + pushed across all 4 repos)

---

## § 0 — Mission statement

Validate that per-tier WR convergence with the **recompose mechanism unblocked** produces a shippable season under the new tuning contract; ship a true season under that mechanism if validation succeeds.

The architectural insight (from engine-rebuild Phase D math investigation, AMENDED with Matt's methodological correction):

> *We were running a fully converged season (tuned for old aggregate-mean contract) against a new tuning mechanism (per-tier WR bands) and asking "why doesn't this tune?" The single modifier scalar can't bridge the contract mismatch. The recompose mechanism IS the bridge that varies kit composition — but it's been architecturally blocked by the floor-lock since per-tier targets were authored. Unblock recompose → recompose can operate → kits naturally converge to per-tier targets.*

The previous hive measured the problem. This hive ships the fix.

---

## § 1 — Hypothesis under test

**H_RC (recompose-as-lever):** *Per-tier WR target convergence is satisfiable for the existing generation rules — IF the recompose mechanism can fire. Composition variation that recompose produces is the lever that bridges the contract mismatch.*

**H_RC_0 (null):** *Even with recompose unblocked, per-tier convergence does not produce shippable kits. Generation rules require revision.*

**Test:** Phase 2 fresh regen at convergence under new mechanism + Phase 3 synthesis.

| Outcome | Threshold | Disposition |
|---|---|---|
| PASS strong | ≥ 80% kit-acceptable | Ship true season (Phase 4); declare mechanism validated |
| PASS moderate | 60-80% kit-acceptable | Ship partial; flag failures for kit-redesign queue |
| CANNOT REJECT NULL | < 60% kit-acceptable | Surface to Matt (one of four wind-down triggers) |

---

## § 2 — Six phases

| Phase | Owner(s) | Effort | Acceptance gate | Tag |
|---|---|---|---|---|
| **P0** Option A floor widening | gamora | ~4h | Binary search reaches modifier < 0.05 (stop-gap regen confirms); no test regressions (A2 BLOCKING) | `recompose-hive/v0.1-option-a-floor-widened` |
| **P1** Option B recompose-trigger conditioning | gandalf (design) + jack-ryan (Gate-1) + gamora (impl) | ~6-10h | Recompose fires at modifier < 0.05 on test class; non-zero delta from levers | `recompose-hive/v0.2-option-b-recompose-conditioned` |
| **P2** Fresh diagnostic regen | rocket + star-lord + gamora | ~4-6h | Regen complete; telemetry complete; per-class classification reproducible | `recompose-hive/v0.3-diagnostic-regen-complete` |
| **P3** Validation synthesis | gandalf + jack-ryan | ~2-4h | Verdict authored; PASS strong/moderate → P4, else surface to Matt | `recompose-hive/v0.4-validation-verdict` |
| **P4** Ship true season | rocket + gamora + star-lord (+ drax if loadout sync) | ~8-12h | validation_report passes; ≥80% per-tier WR in band; cosmology cohesion ≥ 4.0 | `recompose-hive/v1.0-true-season-shipped` |
| **P5** Canonical record | gandalf + jack-ryan + knight-rider | ~4-6h | Roadmap updated; decisions-log entry; engineering-disciplines amendment (if any); hive-runs review v5 | `recompose-hive/v1.1-canonical-record-complete` |

Total wall-time estimate: **4-7 days parallelized; 10-14 days serial.**

---

## § 3 — Operating mode

**AUTONOMOUS CONTINUATION** per engine-rebuild protocol § 4.0 (Matt directive 2026-05-19). The L3-to-Matt escalation is SUSPENDED. Matt re-enters only at one of four wind-down/completion triggers:

1. **Matt declares explicit wind-down** — clean handoff
2. **P5 completion** — true season validated + filed; surface to Matt
3. **P3 CANNOT REJECT NULL verdict** — H_RC refuted; surface to Matt for direction
4. **Hard architectural blocker** — surface via Matt briefing

Until one of these fires, **the hive runs.**

Authority pattern:

| Decision type | Authority |
|---|---|
| Implementation within a seam | Specialist (L1) |
| Cross-seam coordination | knight-rider (L2) |
| Story / design / canonical-direction | gandalf (L2-equivalent) |
| QA / discipline / process | jack-ryan (BLOCK retained, used sparingly) |
| Architectural / cross-cutting | gandalf or knight-rider — co-decide |
| Scope creep | gandalf + knight-rider co-decide |
| Session wind-down | **Matt only** |

---

## § 4 — Out-of-scope (HARD)

- **Pattern-B commercial direction** — PARKED per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. Do NOT let it pull focus.
- **R6 host-calibration protocol** — Pattern-B-conditional; not this hive's scope.
- **Engine-rebuild closure items** — already done; not re-litigated.
- **VS2a continuation work** — different track; not this hive's scope.
- **R2 modifier-sweep / Phase B.2** — different track; the H1 counterfactual test is not this hive's job.
- **Kit-redesign queue execution** — held until P3 verdict (if H_RC fails, kit-redesign becomes the next-step question, not this hive's work).

---

## § 5 — Scope-creep dispositions (mid-flight pressures)

| Pressure | Default |
|---|---|
| "Pattern-B has a new signal — should we revisit?" | REJECT for this hive's scope. File any signal in the PARKED thread; do NOT re-open during operation. |
| "Should we also retry VS2a S1 first-batch under widened floor?" | REJECT. Gated on Option B landing per the diagnostic-only temporal gate (HELD dispatch § 5). |
| "Galadriel should benchmark the new season cosmology" | DEFER to P5 or post-hive. Galadriel sub-agent restriction remains operative. |
| "Drax loadout needs syncing for the true season" | ACCEPT at P4 if loadout schema changes. Otherwise DEFER. |
| "Should we widen scope to include another archetype?" | gandalf + knight-rider co-decide; bias REJECT unless H_RC verdict explicitly requires it. |

---

## § 6 — Tag namespace + commit discipline

Tag prefix: **`recompose-hive/v<X.Y>-<milestone>`** (distinct from `hive-rebuild/`, `vs2a/`, `vs2b/`).

Standing commit + push authority per ADR-006 amendment (milestone tags + push-readiness summaries). No per-tag re-ask.

Fetch-before-commit discipline on hive log file per 2026-05-17 § 14.1.1.

---

## § 7 — Cross-references

**Mission inputs:**
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` (this hive's protocol)
- `agentic_orchestration/dispatches/2026-05-19-knight-rider-recompose-validation-hive-launch.md` (launch dispatch)
- `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` (AMENDED findings — the insight)
- `canonical/story/r1-firstbatch-fail-disposition-2026-05-19.md` (gandalf S1 disposition + § 11 staged-approval framing)
- `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` (gamora Option A + B math)
- `agentic_orchestration/dispatches/HELD-2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` (P0 dispatch — about to be renamed + fired)

**Mechanics inheritance:**
- `canonical/story/archived/hive-mind-protocol-2026-05-17.md` (operating mechanics)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 (autonomous-operation amendment)

**Operational artifacts (this hive):**
- `agentic_orchestration/hive-mind/recompose-validation-log.md` (hive log; append-only)
- `agentic_orchestration/hive-mind/coordination-matrix-recompose-validation.md` (this hive's matrix)
- `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` (this doc)
- `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD-recompose-validation.md` (daily)
- `agentic_orchestration/hive-mind/retrospective-recompose-validation.md` (at P5)

---

*Authored 2026-05-19 by knight-rider at hive activation. Mission scope locked at six phases. Autonomous operation runs until one of four wind-down/completion triggers. The road forward is clear; the hive is on it.*
