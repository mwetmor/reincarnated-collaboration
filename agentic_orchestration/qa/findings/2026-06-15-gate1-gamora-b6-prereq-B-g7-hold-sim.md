# Finding — 2026-06-15 — Gate-1 — gamora b6-deletion Prerequisite B (G7 HOLD-SIM sim-validation of envelope kits)

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1, pre-fire)
**Severity:** N/A (Gate-1 verdict: CLEAR-WITH-AMENDMENTS)
**Target:** `agentic_orchestration/dispatches/2026-06-15-gamora-b6-deletion-prereq-B-g7-hold-sim.md`
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity / honest-fail integrity)

## Verdict

**CLEAR-WITH-AMENDMENTS.** Letting gamora's math-note operationalize "viable fight" (with my Gate-1 on it) is the correct call — pre-baking a band in the dispatch would risk pinning the wrong metric. The cross-seam boundary handling is right (shared Skill dict, no new field per Gate-2 `b85d038`, verify-don't-assume field presence). Boundaries hold: the four `balance_loop.py` ARCHETYPE_TEMPLATES imports stay untouched, no generation-side change, no L1/L2/caster-faith. Two amendments required before firing.

## What I found
I verified the four cross-seam import sites cited in the dispatch — `balance_loop.py` lines **1884 / 1946 / 2025 / 2176** — against the engine. All four are accurate (1884/1946/2025 are single-line `from reincarnated.generation.b6_archetype_templates import ARCHETYPE_TEMPLATES`; 2176 is the `from ... import (` block start, lookup at 2183). The dispatch's untouched-imports boundary is pinned to real code. The pass criterion — envelope kits sim-validate into viable fights, not floor-test-only artifacts — is faithful to brief §2-B. Two Gate-1 gaps, both on conditionality: (1) the math-note Gate-1 that operationalizes "viable fight" is bracketed CONDITIONAL ("HALT for jack-ryan Gate-1 if the criterion warrants" / "[HALT, jack-ryan Gate-1 if warranted]"); for B the criterion-DEFINITION is the decisive act — a soft "viable fight" is precisely how a hard cross-seam deletion gate gets quietly force-passed. (2) The result Gate-2 is bracketed "jack-ryan Gate-2 on the result if it gates"; B is the hard cross-seam gate licensing a DESTRUCTIVE deletion — its result Gate-2 should be unconditional.

## Rationale
Discipline #1 (math-before-code): the "viable fight" operationalization (win-rate band? fight-length band? non-degenerate damage resolution?) is the load-bearing measurable that determines whether the gate is decisive. Per REVIEW_PROCESS Principle 5 (severity matters / honest-fail integrity), a criterion left soft is a force-pass vector. Per Principle 3 (cross-seam impact), B is the harder of the two prerequisites — it gates removal of the live safety net at the sim boundary — so neither its criterion-Gate-1 nor its result-Gate-2 can be optional.

## Required amendments (fold in before marking FIRED)
1. Make the math-note Gate-1 **mandatory**:
   > Scope item 1: "Math-note FIRST (Discipline #1) — define the measurable sim-validation pass criterion ('viable fight' operationalized: win-rate band? fight-length band? non-degenerate damage resolution?), code-cited against `balance_loop.py`. **HALT for MANDATORY jack-ryan Gate-1** (the criterion definition is the decisive act for this hard cross-seam gate; not skippable)."
   > Sequence: "...gamora math-note (sim-validation criterion) → **[HALT — MANDATORY jack-ryan Gate-1 on the criterion]** → gamora G7 HOLD-SIM run → ..."

2. Make the result Gate-2 **unconditional**:
   > Sequence: "...gamora G7 HOLD-SIM run → **jack-ryan Gate-2 on the result (UNCONDITIONAL — this is the hard cross-seam gate licensing a destructive deletion)** → KR carries B's result..."

## Action
- [ ] KR: fold both amendments into the dispatch, then mark FIRED.
- [ ] gamora: math-note "viable fight" criterion must arrive at jack-ryan Gate-1 before the sim run starts.

## References
- `agentic_orchestration/dispatches/2026-06-15-gamora-b6-deletion-prereq-B-g7-hold-sim.md`
- `agentic_orchestration/gandalf/notes/2026-06-15-b6-deletion-prerequisites-brief-for-kr.md` §2-B, §4
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` §6-quater Decision 2 (b) Prerequisite 2
- `~/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py:1884,1946,2025,2176` (the four cross-seam ARCHETYPE_TEMPLATES consumers — verified, untouched by this prerequisite)
- Gate-2 `b85d038` (Phase-2 envelope, PASS-WITH-AMENDMENTS — shared Skill dict, no new field)
