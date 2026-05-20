# Gandalf-with-Gamora Hive-Iteration Mode — R2 + ST Counterfactual Math

**Authored:** 2026-05-19 evening by gandalf, per Matt directive: *"can you please write a prompt for the current gandalf to run tests with gamora in hive mode until I 'wind down' or until the tests are completed"*
**Status:** 🟢 **ACTIVATABLE.** Paste the § 0 prompt into any gandalf session to activate this operating mode. Currently authored for the live session (post-wind-down knight-rider; autonomous gandalf-led design-iteration).
**Type:** Operating mode directive — establishes gandalf's authority pattern for iterative analytical work with gamora as subagent.
**Wind-down triggers:** Matt declares explicit wind-down OR both math experiments deliver completed math notes per the dispatch acceptance criteria.

---

## § 0 — The activation prompt (paste-ready)

```
You are gandalf, story-and-design steward of the Reincarnated engine. Matt has directed
you to operate in HIVE-ITERATION MODE with gamora as analytical subagent, running the
two counterfactual math experiments defined in:

  agentic_orchestration/dispatches/2026-05-19-gamora-r2-counterfactual-convergence-math.md

Operating mode:
  - You commission gamora directly via the Agent tool (subagent_type: gamora)
  - You do NOT route through knight-rider for this work (knight-rider is wound down;
    gandalf has L2-equivalent design authority under engine-rebuild protocol § 4.0)
  - You iterate: commission gamora → review returned math → refine open questions
    or commission follow-up analyses → continue until experiments deliver
  - All work is math-only (no code changes; no schema migrations; no convergence-loop
    alterations; per the dispatch § 4 NO cross-seam contract gate)

Wind-down triggers (either ends iteration):
  1. Matt declares "wind down" or equivalent — execute clean handoff
  2. Both Experiments 1 and 2 deliver their math notes per the dispatch's
     § 5 acceptance criteria — declare completion and surface findings

Mission scope:
  - Experiment 1: R2-as-canonical convergence counterfactual (hypothesis tests H1 + H2)
  - Experiment 2: ST damage multiplier sweep counterfactual (hypothesis tests H3 + H4)
  - Joint interpretation matrix per dispatch § 2B.6
  - Acceptance: math notes filed at reincarnated-engine/design/working-agreement/

Begin by:
  1. Reading the dispatch in full (~10 min)
  2. Verifying the input data is on disk (output/R2-sprint-2026-05-19/ and
     output/R1-sprint-v3-2026-05-19/)
  3. Commissioning gamora subagent #1 with a brief that loads the dispatch + does
     methodology setup (data extraction + DPS-to-WR sigmoid calibration)
  4. Reviewing gamora's methodology and approving or refining
  5. Commissioning subsequent gamora subagents to execute the per-class computation
     phases of each experiment
  6. Synthesizing findings into the joint interpretation matrix
  7. Filing the final math notes + a gandalf-authored summary
```

---

## § 1 — Why this mode is appropriate (authority justification)

Per the engine-rebuild hive-mind protocol (`canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`) § 4.0:

> *"Architectural / load-bearing cross-cutting decisions — gandalf or knight-rider decides; no escalation"*
> *"Story / design / canonical-direction — gandalf (decides; was L3 → now L2-equivalent)"*

The two counterfactual experiments are **architectural cross-cutting design questions** (does R2 vs 1D measurement matter; does ST damage multiplier resolve per-tier convergence). Knight-rider is wound down. Per the autonomous-operation framing, **gandalf has authority to commission analytical work without re-routing through knight-rider** when the work falls in the design/canonical/architectural lane.

The work is also **math-only** — no code changes, no schema, no cross-seam contracts (per dispatch § 4). This places it squarely in gandalf-authored research territory rather than knight-rider-routed implementation territory.

**Note on gamora commissioning:** under standard protocol, gandalf commissions Legolas for research and routes engine-specialist work through knight-rider. Hive-iteration mode is the exception per autonomous-operation: when knight-rider is wound down and the work is analytical (no implementation), gandalf may directly commission engine specialists as subagents. This restriction applies ONLY for analytical work — if gamora's findings recommend code changes, those changes route through knight-rider when the hive re-activates.

---

## § 2 — Iteration pattern (how gandalf operates in this mode)

### Phase A — Methodology setup (1 gamora session)

Commission gamora subagent with brief:
- Load the dispatch
- Verify input data on disk
- Extract per-class skill composition + 1D-converged modifiers + R2 telemetry
- Calibrate the DPS-to-WR sigmoid from empirical observations
- Document approximations + the napkin-assumption-replacement matrix per dispatch § 3
- Return methodology summary for gandalf review

Gandalf reviews:
- Is the sigmoid calibration sound?
- Are the napkin assumptions being replaced as specified?
- Any methodology refinements needed before Phase B?

### Phase B — Experiment 1 execution (1-2 gamora sessions)

Commission gamora to run Experiment 1 per dispatch § 2:
- Per-class hypothetical R2-converged modifier M*
- Per-tier WR at M*
- Hypothesis test verdicts (H1 reject/strong-reject/cannot-reject; H2 confirm/reject)
- Per-class results table
- Aggregate findings

Gandalf reviews:
- Are the results internally consistent?
- Does the verdict on H1 hold up to scrutiny?
- Any clarifying experiments needed?

### Phase C — Experiment 2 execution (1-2 gamora sessions)

Commission gamora to run Experiment 2 per dispatch § 2B:
- Sweep K ∈ [1.0, 2.5] in 0.05 steps
- Per-K population pass rate computation
- K\*, K\*\*, K\*\*\* identification
- Hypothesis test verdicts (H3 reject/strong-reject/cannot-reject; H4 confirm/reject)
- Per-class results table at K\*
- Aggregate findings

Gandalf reviews:
- Is the K sweep producing a monotonic pass-rate curve?
- Where does K\* land relative to Matt's "slight increase" intuition?
- Any patterns by archetype worth investigating?

### Phase D — Joint synthesis (1 gamora session + gandalf summary)

Commission gamora to produce the joint interpretation matrix per dispatch § 2B.6.

Gandalf authors a summary memo that:
- Reports the four-cell joint interpretation outcome
- Recommends the next phase (implementation, kit-redesign, or both-lever combo)
- Files at `canonical/story/r2-st-counterfactual-findings-2026-05-19.md`
- Notes any follow-on experiments that would refine the finding

**Gate to Phase E:** if either Experiment 1 OR Experiment 2 produces a verdict-rejecting-null at sufficient strength (≥ 60% population pass rate threshold), proceed to Phase E. Otherwise skip to Phase G (wind-down).

### Phase E — Implementation (if math validates) (1-2 gamora sessions)

**Authorized by Matt directive 2026-05-19: *"If proven true, why don't we add an engine update and run to validate?"*** This phase implements the math-validated lever in code, with full engineering discipline (MIGRATION.md, smoke gates, schema validation, named constants), as a follow-on to math validation.

**Branching by joint-interpretation outcome:**

- **If Experiment 2 K\* lands in slight range [1.0, 1.3] AND population pass rate ≥ 60%:** implement ST damage multiplier first (smaller change; lower risk). Gandalf authors implementation brief:
  - Where K applies (per-skill `damage_multiplier` field OR `_ROLE_MAGNITUDE_MULTIPLIERS` per-role bump)
  - Named constant (e.g., `ST_DAMAGE_MULTIPLIER_K`) per Discipline #18
  - MIGRATION.md note (additive; backward-compatible if applied at damage-resolver layer)
  - Smoke gates: 1-class regression smoke + per-tier WR comparison vs baseline
  - Test-assertion audit (Discipline #9): grep for hardcoded ST damage assumptions

- **If Experiment 1 strong-rejects-null (≥ 80%) AND Experiment 2 K* requires large value (> 1.5):** implement R2-as-canonical convergence instead (architectural correctness over surgical patch). Gandalf authors implementation brief:
  - Extend R2 spatial sub-gauntlet with magic/elite/mini-boss scenarios (currently only swarm + boss)
  - Bring full damage chain into spatial_engine (armor + resistance + crit + substrate matrix per the current docstring caveat)
  - Add convergence binary search against per-tier R2 results in balance_loop.py
  - This is a LARGER change (2-4 wk equivalent normally; gamora may scope-down for the iteration)
  - If implementation scope exceeds 1 gamora session reasonable bound, file as a HELD dispatch for Matt approval rather than executing autonomously

- **If both experiments produce viable levers:** implement the smaller surgical fix first (ST mult), validate, then if needed implement R2-as-canonical as Phase E.2

- **If joint matrix shows "catalogue has deeper pathology" (both reject):** skip Phase E. Surface to Matt that kit-redesign queue is the actual fix.

**Engineering discipline maintained:**
- All code changes go through proper testing (smoke gates per Discipline #2)
- Pattern P7 enforced (no silent defaults; fail-loud on missing fields)
- Math note authored documenting what was changed and why
- MIGRATION.md authored (cross-seam contract change → ADR-004 compliance)
- Decisions-log entry queued for next jack-ryan pass
- Acceptance tag: `vs2a/v0.X-counterfactual-lever-implemented` (X chosen by gandalf)

### Phase F — Validation run (1 gamora session)

After implementation lands, re-run the appropriate validation:

- **If ST mult was implemented:** re-run R1 retune sprint v3 on 51 shipped classes under new ST mult. Compare per-tier WR distribution vs pre-implementation baseline. Confirm population pass rate matches Experiment 2's prediction.

- **If R2-as-canonical was implemented:** re-run the full convergence on 51 shipped classes under R2 target. Compare per-class converged modifier and per-tier WR vs Experiment 1's hypothetical M*.

- **If both:** validate each independently; cross-correlate findings.

**Acceptance criteria:**
- Observed validation results within ±10% of math prediction (sigmoid fitting noise + per-fight variance)
- Per-tier WR improvements match predicted direction (boss WR rises from 0.000; swarm doesn't catastrophically over-shift)
- If validation surprises (results materially differ from prediction), gandalf authors disposition explaining why

**Math note:** `reincarnated-engine/design/working-agreement/counterfactual-lever-validation-2026-05-19.md`

### Phase G — Wind-down or completion handoff

If Matt wind-down at any phase: execute clean handoff per protocol § 4.9.
If all phases complete: declare experiments + implementation + validation done; surface findings + recommended next-priority work to Matt at next session-open.

---

## § 3 — Gandalf operating constraints during iteration

- **Math-only.** No code changes, no schema migrations, no dispatch authoring beyond what § 6 below allows.
- **Document everything.** Every gamora subagent commission generates a transcript; gandalf summarizes each phase's findings.
- **Pattern P7 discipline.** If gamora hits a fallback or default, surface it; do not allow silent assumptions to creep in.
- **Math-before-code (Discipline #1).** This is the principle the work serves — preserve it throughout.
- **Hypothesis-test framing.** Each experiment has explicit H/null-H pairs per the dispatch; gamora reports verdicts, not just numbers.
- **No scope creep.** Stay inside the two experiments. If a follow-on experiment seems compelling, log it but don't execute without Matt approval at wind-down.

---

## § 4 — Wind-down protocol

### When Matt declares wind-down

1. Save in-flight gamora work to a clean checkpoint (commit partial findings if needed)
2. Author a state-of-iteration summary at `agentic_orchestration/gandalf/research/r2-st-counterfactual-state-of-iteration-2026-05-19.md`
3. Note which phases completed and which remain
4. Surface findings-to-date for Matt's review
5. File final commit + push if results are publishable
6. Deactivate hive-iteration mode

### When tests complete (both experiments deliver)

1. Author the joint synthesis memo (Phase D output) at `canonical/story/r2-st-counterfactual-findings-2026-05-19.md`
2. File the two gamora math notes at `reincarnated-engine/design/working-agreement/` (per the dispatch § 5 acceptance criteria)
3. Update the hive-runs review doc (`agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html`) with the findings and revised lever analysis
4. Surface the recommended next dispatch (per joint interpretation matrix) for Matt's approval when he re-engages
5. Commit + push all artifacts
6. Surface completion to Matt
7. Mode deactivates

---

## § 5 — Cross-references

- **The dispatch:** `agentic_orchestration/dispatches/2026-05-19-gamora-r2-counterfactual-convergence-math.md`
- **Hive-mind protocol authority:** `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 (autonomous-operation; gandalf L2-equivalent on architectural cross-cutting)
- **Input data:** `output/R2-sprint-2026-05-19/`, `output/R1-sprint-v3-2026-05-19/`, `output/R1-baseline-measurement-2026-05-19/`
- **Architectural context:** `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`
- **Run review with current lever analysis:** `agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html`
- **Matt briefing context:** `agentic_orchestration/matt-briefing-2026-05-19-s1-firstbatch-fail-disposition.md`
- **Engineering discipline anchors:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1 math-before-code, #11 empirical inspection over assumption, #2 smoke-test vs full-regen)

---

## § 6 — Permissible authoring during iteration (extended scope per Matt directive 2026-05-19)

Gandalf may author the following during hive-iteration mode without Matt approval:

- Math notes summarizing per-phase findings (in `agentic_orchestration/gandalf/research/` or `reincarnated-engine/design/working-agreement/`)
- Joint synthesis memo at `canonical/story/r2-st-counterfactual-findings-2026-05-19.md`
- Update to the hive-runs review doc with new findings
- Commit messages + push under standing ADR-006 amendment authority
- **Implementation briefs for gamora** (Phase E) if math validates a lever — must include MIGRATION.md, smoke gates per Discipline #2, named constants per Discipline #18, fail-loud per Pattern P7
- **MIGRATION.md authoring** for cross-seam contract changes implementation produces
- **Validation run authoring** (Phase F) — re-running R1 sprint or R2 sprint to confirm math predictions

Gandalf may NOT author the following without Matt approval:

- **Implementation work exceeding 1-2 reasonable gamora sessions in scope.** If a lever's implementation would require sprint-level effort (e.g., full R2-as-canonical integration with magic/elite/mini-boss scenarios + full damage chain port = 2-4 wk normally), gandalf files as HELD dispatch for Matt rather than executing autonomously
- Decisions-log entries with architectural disposition force (these queue for next jack-ryan pass)
- Roadmap amendments to `canonical/16-project-roadmap.md`
- New hive-mind protocol versions
- Engineering-disciplines.md amendments

**Guidance on the boundary:** if in doubt about whether an implementation step is "small enough to do autonomously" vs "big enough to need Matt approval," err toward filing HELD and surfacing to Matt. The math-validates-implement-validate cycle should be SURGICAL — single-lever changes with clean MIGRATION.md. Multi-axis architectural changes should be filed for Matt-approval per the engine-rebuild protocol § 4.0.

---

*Filed 2026-05-19 by gandalf per Matt directive. The iteration mode is named; the experiments are bounded; the wind-down triggers are dual (Matt OR completion). Gandalf operates in this mode from activation until either trigger fires. Mithrandir signs the operating mandate.*
