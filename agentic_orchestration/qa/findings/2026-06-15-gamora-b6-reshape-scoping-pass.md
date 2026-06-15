# Finding — 2026-06-15 — gamora-b6-reshape-scoping-pass

**Reviewer:** jack-ryan
**Severity:** INFO (CONFIRM-WITH-CAVEAT — diagnostic is sound; the recommendation HEADLINE needs reframing before it reaches the gandalf+Matt scoping call)
**Target:** tag `gamora/v1.x-b6-reshape-scoping-pass` (→ `6f7820a`); durability commit `7a7c529`
**Developer:** gamora
**Mode:** DEV-MODE — Gate-2, diagnostic-integrity (NOT a build PASS/FAIL gate)
**Principles applied:** #1 (math-note governed the run), #11 (empirical, not assumed), #12 (no new semantic), #2.1 (resource bound), Review-Principle #1 (math-before-code), #5 (severity matters)

## Disposition: CONFIRM-WITH-CAVEAT

The diagnostic is **reliable** for the downstream design call. The signature was applied honestly, the decisive caster leg was genuinely not steered, the INCONCLUSIVE-not-collapse distinction is legitimate (not an escape hatch), and the artifact supports the evidence. The single caveat is a **framing** issue on the recommendation headline (Q2), not a defect in the run — and it is exactly the qualifier I pre-flagged at signature Gate-1 (`ddf47ce` Action to Matt). No BLOCK; no re-run needed.

## What I found

I verified the four integrity questions against the artifact (`output/g7-reshape-scoping-b6-20260615.json`) and the harness, not on trust.

**Q1 — Caster leg honestly NOT steered: CONFIRMED.** The verdict is `INCONCLUSIVE`, `n_cells_1b_satisfied=0`, `widening_fired=true`, `widening_runs=16` → 4 base + 16 widening = 20 caster evals (seeds +101/+202/+303 then power-60 × 4 cells). I read every caster eval: `1b_swarm_over_ceiling` is `false` on all 20; the maximum swarm WR observed is 0.4889, never approaching the 0.80 ceiling. The over-ceiling-swarm precondition that triggers the floor-to-suppress genuinely never arose. Casters converge at moderate modifiers (0.1183–0.6287), never floored — so element-1a is also unsatisfied independently. The budget was genuinely walked to exhaustion. Critically, the INCONCLUSIVE was **NOT** quietly converted to a de-facto ENVELOPE_SPECIFIC: the harness's ENVELOPE_SPECIFIC branch (`g7_reshape_scoping_b6_2026_06_15.py:522`) requires `cells_1b AND nocollapse_cells`, which is unreachable with `n_cells_1b_satisfied=0` — it correctly fell through to the INCONCLUSIVE branch (`:527`). The convenient answer was structurally foreclosed, not merely avoided by discretion.

**Q2 — Recommendation overclaim: PARTIAL — the headline is over-proportioned to the evidence (the caveat).** gamora's AGENT_STATE headline reads "ENVELOPE-SPECIFIC mechanism, with an honest INCONCLUSIVE caveat." The body is impeccably honest — it states plainly that this is INCONCLUSIVE on the strict signature, that casters never got hot, and that casters fail by a different mechanism. But the *headline word* "envelope-specific" claims more than the evidence licenses. The evidence supports: *the specific hot-swarm-floors-the-modifier dynamic was reproduced ONLY on the envelope arm (one cell, rogue); it could NOT be tested on casters because casters never produced the precondition within budget.* That is **untestable-within-budget**, not **disproven-on-casters**. "Envelope-specific" connotes the latter. The honest framing for gandalf+Matt is: *"envelope-specific for the tested dynamic; caster generalization remained untestable within the bounded budget because the caster swarm tier never went hot — casters have the opposite (cold-swarm) problem."* The body already says this; the headline should match the body.

**Q3 — A2 fold real: STRUCTURALLY YES; NOT EMPIRICALLY EXERCISED this run.** `CASTER_SHAPE_EXISTS` / `M_SWEEP` is implemented (`:243-286`) as the symmetric analog of envelope-2b: a fixed-modifier sweep over `M_SWEEP={0.01,0.0316,0.1,0.316,1.0,3.16}` asking whether ANY single modifier clears all three upper tiers, reusing the engine's own `_evaluate_class` + `_compute_per_tier_win_rates` + `_compute_kills_only_tier_rates` (no new engine semantic — Discipline #12 clean). The shape-vs-broken line is drawn correctly in code, and it is correctly gated to fire ONLY where `1a∧1b∧2a` hold (`:453`). Because no caster cell ever satisfied 1b, `CASTER_SHAPE_EXISTS` **never executed** — so its discriminating power was not exercised against live data this run. This is acceptable (it cannot introduce looseness if it never fires), but it means the soft seam I closed at Gate-1 was closed in principle, not stress-tested in practice. The branch-precedence (A2-iii) and binding-widening (A2-ii) halves of A2 WERE exercised and behaved correctly.

**Q4 — "Casters fail by a different mechanism" side-finding: load-bearing and correctly scoped as a SEPARATE rocket flag.** The artifact shows casters do crater mini_boss/boss (~0.0 on most cells) but at moderate converged modifiers (0.12–0.63), via a broad upper-tier-kills deficit — distinct from the envelope's hot-swarm-floors-the-modifier dynamic. gamora correctly reports this as a separate caster-composition concern flagged to rocket, explicitly NOT conflated with the per-tier-shape question and NOT part of this gate's verdict. Correctly scoped. It is load-bearing precisely because it is what makes the INCONCLUSIVE honest rather than a dodge: casters aren't "fine," they fail differently.

**Disciplines:** #1 — the signature math-note governed the run; sanity anchor fired True on B CELL-4/rogue at zero new fights (`ANCHOR_HOLDS=true`). #11 — the different-mechanism finding was surfaced, not hidden. #12 — no new engine semantic; balance_loop/composer/b6 untouched (confirmed via commit `6f7820a` touching only output/, the harness, AGENT_STATE). #2.1 — smoke-subset-first ran (204.6s, peak 61.4MB) gating the full slice (1780.5s, peak 61.8MB); both within the pre-registered ~25min+widening budget projection. Boundary precondition CLEAN on every BUILT kit, symmetric across arms; the lone non-pass is the `b6_physical_skirmisher` B-precedent KitConstraintError, classified distinctly from a field defect.

## Rationale

The decisive anti-steer (Review-Principle #1, the signature-as-truth-act) held: the symmetric pre-registration made the convenient "envelope-only" verdict structurally unreachable, and gamora reported the honest INCONCLUSIVE rather than collapsing it to a clean win. That is exactly the discipline the scoping pass was designed to enforce, and it worked.

The Q2 caveat is not a reliability defect — it is the residual-risk qualifier I pre-registered for Matt at signature Gate-1 (`ddf47ce`, final Action): an "architectural" verdict (or here, its mirror, "envelope-specific") must carry the shape-vs-broken / testable-vs-untestable qualifier before it reframes the scoping call. The body carries it; only the headline word drops it. That is an INFO-severity framing tightening for KR to apply when routing, not a re-run trigger (Discipline #5 — severity matters: the underlying evidence is sound, so this does not block).

## Action

- [ ] KR (when routing to gandalf+Matt): reframe the one-line headline from "envelope-specific mechanism" to "envelope-specific for the tested hot-swarm dynamic; caster generalization untestable within budget — casters never went hot (cold-swarm), so the dynamic could not be reproduced or ruled out on them." Carry gamora's body caveat into the headline. The recommendation's substance is unchanged; only its certainty-proportioning.
- [ ] gandalf+Matt (scoping call): the live evidence is that the per-tier-shape degeneracy is a **single-cell (rogue) envelope property** where b6 demonstrably carries the upper tiers a floored global modifier craters; warrior/grappler/skirmisher/hunter are co-broken (b6 also craters their upper tiers), so b6's "net" only actually held on rogue. The architecture-vs-envelope question is NOT settled against casters — it is untested, because the precondition never arose. If that distinction matters to the reshape decision, a follow-up that manufactures a hot-swarm caster cell (it would exercise the unexercised CASTER_SHAPE_EXISTS path) is the way to close it; otherwise the rogue-only narrowness may itself be sufficient to scope (or decline) a narrow envelope-composition fix.
- [ ] rocket (separate flag, NOT this gate's verdict): casters crater mini_boss/boss at moderate modifiers via a broad upper-tier-kills deficit — a caster-composition concern distinct from the per-tier-shape question.
- [ ] No Matt decision needed on THIS finding (INFO, within ADR-002 diagnostic-review scope).

## References

- Result artifact: `reincarnated-engine/output/g7-reshape-scoping-b6-20260615.json` (full 3-leg; verdict INCONCLUSIVE at `:357`, 20 caster evals, `n_cells_1b_satisfied=0` at `:363`)
- Smoke artifact: `reincarnated-engine/output/g7-reshape-scoping-b6-20260615-smoke.json`
- Math-note (folded A1+A2): `reincarnated-engine/src/reincarnated/simulation/math/b6-reshape-scoping-per-tier-shape-degeneracy-signature-2026-06-15.md`
- Harness: `reincarnated-engine/scripts/g7_reshape_scoping_b6_2026_06_15.py` (CASTER_SHAPE_EXISTS `:243-286`, gated `:453`; verdict branches `:517-534`; widening `:481-508`)
- Commits: `7a7c529` (durability/fold), `6f7820a` (run + AGENT_STATE); tag `gamora/v1.x-b6-reshape-scoping-pass`
- Prior Gate-1 (signature): `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-b6-reshape-scoping-signature.md` (`ddf47ce`)
- Prior Gate-1 (dispatch): `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-b6-reshape-scoping-pass.md` (`fdd8057`)
- B evidence (sanity anchor source): `reincarnated-engine/output/g7-hold-sim-b6-prereq-B-20260615.json` (CELL-4/rogue)
