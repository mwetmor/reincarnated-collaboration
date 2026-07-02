# Gauntlet Metrics as Provisional Hypotheses — Recognition Record

> **STATUS:** CURRENT (load-bearing as of 2026-06-01) — Recognition record per substrate-led discipline applied to the math gauntlet itself. The discipline observation: iterating to convergence on gauntlet metrics whose empirical validity has not been established is wasted iteration; gauntlet metrics are PROVISIONAL HYPOTHESES about build-defining behavior, not validated ground truth; empirical validation gate is manifestation-milestone-enabled playtest. Authored to lock the discipline observation canonically before wave-5 closure proceeds.

**Date:** 2026-06-01
**Recognition surfaced:** Matt 2026-05-31 verbatim observation: "On phase 3 of (a) Cycle 14 wave-5 closing, I'm hesitant to see this through completely as the mathematical tests we used were created without evidence of validity. Is there a way we can close this out and move on more swiftly based on this?"
**Author:** gandalf (story-and-design steward)

**Companion artifacts:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — pattern library architecture this recognition refines
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led) + § 42a (framing-audit)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — BVV framework (gauntlet's validation framework)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — investment scaling math (gauntlet axis)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — damage architecture (gauntlet axis)
- `agentic_orchestration/research/arpg-community-axes-2026-05-29/synthesis-verdict.md` — community research instrument

---

## 0. TL;DR

**The discipline observation:** the math gauntlet that produces Cycle 14 wave-5 Phase 3/4 outputs uses metrics (KPM targets, multi-format winning criteria, cohort archetype taxonomy, encounter representativeness, BVV thresholds) that are largely **designer-asserted** rather than empirically validated. Iterating gauntlet sim results to convergence against these metrics drives the engine toward a designer-asserted ground truth whose empirical validity has not been established.

**The recognition:** gauntlet metrics are PROVISIONAL HYPOTHESES about what "build-defining" or "viable" or "winning" mean. They are not validated ground truth. They are working-state mathematical models that approximate intended gameplay behavior, awaiting empirical validation through playtest.

**The empirical validation gate:** manifestation-milestone-enabled playtest cycles (per hypothesis-flow methodology Stage 4). Same validation instrument that graduates pattern library cells; applied one layer up the stack to validate the gauntlet metrics themselves.

**The operational consequence:**
- **Wave-5 closes swiftly** at current iteration snapshot, not at gauntlet-defined convergence
- **Current Phase 4 archive is PROVISIONAL** working-state; not validated truth
- **Gauntlet metric refinement deferred** to post-manifestation-milestone (when playtest evidence enables refinement)
- **Pattern library Phase A gating strengthens** — current archive candidates are hypothesis-source material, not validated patterns

**The discipline composition:** Disc #41 substrate-led applied to gauntlet metrics + Disc #42a framing-audit applied at the metric-validity gate + recognition → empirical validation → commit applied to gauntlet itself + the hypothesis-flow methodology placeholder operationalizes the validation.

---

## 1. The recognition in Matt's words

Matt 2026-05-31 evening (immediately following gandalf's response defining the three gates — Cycle 14 wave-5 closing / WS1A landing / manifestation milestone — for pattern library Phase A):

> "On phase 3 of (a) Cycle 14 wave-5 closing, I'm hesitant to see this through completely as the mathematical tests we used were created without evidence of validity. Is there a way we can close this out and move on more swiftly based on this?"

This is a Disc #42a framing-audit observation. The question audits the pre-imposed assumption that the gauntlet metrics constitute valid ground truth that's worth iterating toward. The observation: the assumption hasn't been established empirically; iteration toward an unvalidated target is wasted effort.

The observation is correct. This record canonicalizes it.

---

## 2. Gauntlet metric validity assessment

Per-component assessment of the current math gauntlet (as of wave-5 Phase 3 work):

| Gauntlet component | Source | Validity status | Notes |
|---|---|---|---|
| **KPM thresholds per cohort** (kills per minute targets) | Designer-asserted | UNVALIDATED | Threshold values derived from design intuition; not calibrated against playtest |
| **Multi-format winning criteria** (success per encounter type) | Designer-asserted | UNVALIDATED | "Winning" definition (survival? damage output? time efficiency?) composed mostly from designer intuition |
| **Cohort archetype taxonomy** (DPS-min-maxer / Balanced / Defensive / Hybrid) | Designer-asserted | UNVALIDATED | Per `2026-05-29-designer-writes-substrate-player-names-experience-principle.md` § 4.5, the mapping to player-experience vocabulary is Cycle 15+ research-driven; currently designer-only |
| **Encounter representativeness** (which encounters represent endgame combat) | Designer-asserted | UNVALIDATED | Encounter set was chosen without empirical community-research backing |
| **Investment scaling math** (doc 51 6-pattern architecture) | Designer-derived from research | PARTIALLY VALIDATED | Better grounded than other gauntlet metrics (research-informed) but magnitude curves still designer-asserted at the calibration layer |
| **BVV thresholds** (doc 50 bounded viability validation) | Designer-asserted | UNVALIDATED | Threshold values picked from design intuition |
| **Pareto-2 reduction methodology** | Substrate-led discipline preserved | METHODOLOGY VALID; AXES PROVISIONAL | Pareto dominance reduction logic is methodologically sound; what's questioned is whether the SCORE AXES the reduction operates against are the right axes |
| **Mathematical infeasibility detection** (negative damage, zero survivability, infinite resource) | Engine sanity-check | VALID | The structural sieve catching mathematical infeasibility IS valid; this is not what's being questioned |

**Net:** the gauntlet has VALID methodology at the structural-sieve layer and at the Pareto-reduction layer. The METRICS the methodology operates against are largely designer-asserted and not empirically validated.

**Important distinction:** the gauntlet is not WORTHLESS. It serves three valid functions today:
1. Catches mathematical infeasibility (negative damage, zero survivability, infinite resources)
2. Provides a structural sieve that reduces ~639 candidates to ~33 archive entries (a 19× reduction that's mathematically sound regardless of metric validity)
3. Generates predictions that playtest will subsequently validate or refute

What's questioned: treating gauntlet outputs as DEFINING AUTHORITY for what build-defining or viable means, rather than as PROVISIONAL PREDICTIONS awaiting empirical validation.

---

## 3. Discipline composition

### 3.1 Disc #41 substrate-led applied to gauntlet metrics

Substrate-led discipline says: **substrate votes; designer doesn't pre-impose taxonomy.** The discipline has been honored at the substrate-input layer (BC axes derived from substrate library; cultural lineage from weapon library; element from canonical catalog). It has NOT been applied with comparable rigor at the gauntlet-metric layer (KPM thresholds, cohort taxonomy, encounter set, BVV thresholds — all designer-asserted).

This recognition extends Disc #41 to the gauntlet metric layer: **the gauntlet's scoring axes should be empirically validated, not designer-asserted.** The same discipline that catches pre-imposed taxonomy at the substrate-input layer should catch pre-imposed taxonomy at the metric layer.

**Discipline #41 amendment candidate (jack-ryan ratification):**
> Substrate-led discipline applies at BOTH (a) substrate-input layer (substrate library; canonical vocabulary; BC axes derived from empirical evidence) AND (b) validation-metric layer (gauntlet metrics; KPM thresholds; cohort taxonomy; BVV thresholds; encounter representativeness — derived from playtest-validated evidence). Designer-asserted metrics at the validation layer are no more substrate-led than designer-asserted taxonomy at the input layer.

### 3.2 Disc #42a framing-audit at the gauntlet-validity gate

Disc #42a applies the three-question framing-audit checklist at extension hotspots. The gauntlet metric layer is exactly such a hotspot — every wave's iteration depends on metric validity assumptions that have not been audited.

Applied to wave-5 Phase 3:
- **Q1:** What load-bearing framing assumptions does Phase 3 gauntlet iteration depend on? → KPM thresholds + multi-format winning + cohort taxonomy + encounter set + BVV thresholds are all load-bearing.
- **Q2:** What evidence currently in hand could refute these assumptions? → NONE EXISTS. The empirical-validation instrument (manifestation-milestone-enabled playtest) doesn't exist yet.
- **Q3:** If refutation evidence exists or is plausible from current scope, is the right move to refine the framing rather than execute the work as-framed? → Yes. The right move is to recognize that gauntlet iteration to convergence is converging against unvalidated metrics; close out at snapshot; defer refinement to when empirical validation can fire.

Matt's question IS the framing-audit Q3 answer surfacing. The audit was implicit in the question.

### 3.3 Recognition → empirical validation → commit applied to gauntlet itself

The recognition-validate-commit discipline (`gandalf OP § 3.4`) applies to architectural commitments. The gauntlet is an architectural commitment about what build-defining means mathematically. Per the discipline:

- **Recognition** of the gauntlet's intended function: ALREADY DONE (docs 47, 50, 51 + extensive design work)
- **Empirical validation** of the gauntlet's metrics against ground truth: NOT YET DONE (manifestation-milestone-enabled playtest is the instrument; doesn't exist yet)
- **Commit** of the gauntlet as validated authority: PREMATURE (validation hasn't fired)

Operating the gauntlet AS IF the commit phase had happened (iterating to convergence; treating outputs as defining truth) violates the discipline. The right operation is: use the gauntlet as a structural sieve + provisional predictor; mark outputs as provisional; defer commit until validation fires.

### 3.4 Hypothesis-flow methodology placeholder composition

Per `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md`, hypothesis-flow Stage 4 is playtest validation. The placeholder doc framed this as the validation instrument for pattern library cells (downstream artifacts).

This recognition extends the Stage 4 validation instrument **one layer up the stack**: playtest validates BOTH (a) hypothesis-cell patterns AND (b) the gauntlet metrics that produce those patterns. Same playtest cycles validate two layers simultaneously.

The validation protocol:
- Manifest a character from current archive (Cycle 14 wave-5 Phase 4 output)
- Playtest the character at 3+ power planes
- **Measure actual KPM** at each plane → compare to gauntlet-predicted KPM
- **Measure actual multi-format performance** → compare to gauntlet-predicted multi-format viability
- **Measure cohort-archetype mapping** → does the character feel like the gauntlet-predicted cohort archetype?
- Same comparison protocol applies to failure-mode comparison character

If gauntlet predictions match playtest observations → gauntlet metrics validate. If they diverge → gauntlet metrics refine. Either outcome is informative.

---

## 4. Wave-5 closure path (operational implications)

### 4.1 What changes about wave-5 closure

Per the recognition, wave-5 closes at **iteration snapshot** rather than **gauntlet-defined convergence**:

| Phase | Before recognition | After recognition |
|---|---|---|
| Phase 3 (gauntlet sim) | Iterate to convergence; signal stabilization | **Stop iterating; lock current results as snapshot** |
| Phase 4 (archive insertion) | Pareto-2 reduction against converged gauntlet | **Lock current archive candidates as provisional** |
| Phase 5 (cohesion judge) | Cluster against converged archive | **Cluster against snapshot archive** |
| Phase 6 / Phase 7 (joint-gate) | Sign off on converged outputs | **Sign off on snapshot outputs with PROVISIONAL marker** |
| Wave-close documentation | Canonical commitment to outputs | **Canonical commitment to outputs as provisional working-state** |

The substantive change: **PROVISIONAL** markers on all wave-5 outputs that descend from gauntlet metrics. Downstream consumers (pattern library; Cycle 15+ work; commercial pitches; jack-ryan QA) read the PROVISIONAL marker and know empirical validation hasn't fired yet.

### 4.2 What does NOT change about wave-5 closure

- Phase 1-2 substrate-input work (substrate library; weapon catalog; element vocabulary; period/register/cultural lineage) — substrate-led discipline already applied here; outputs are NOT provisional in the same sense (substrate library IS the empirical ground)
- Phase 5 cohesion judge methodology (the LLM call structure; the substrate-led discipline applied to cluster naming) — methodology is sound regardless of input archive provisionality
- Phase 7 joint-gate sign-off process (signing off on outputs as provisional is procedurally identical to signing off on outputs as final, with the marker different)
- Engine architecture (the gauntlet structural sieve remains valid; the Pareto-2 reduction methodology remains valid; only the metric-axis validity is in question)

The recognition is about **how we treat gauntlet outputs**, not about whether the gauntlet structure is valid.

### 4.3 Wave-5 close dispatch (knight-rider routing)

The operational instruction to knight-rider:

```
Wave-5 swift closure authorized per gandalf 2026-06-01 recognition record.

ROUTE TO: star-lord + gamora (engine seam owners)

ACTIONS:
1. Stop Phase 3 gauntlet sim iteration. Current state is wave-5 snapshot.
2. Lock current Phase 4 archive insertion candidates as wave-5 archive.
3. Phase 5 cohesion judge fires against snapshot archive (no changes to
   cohesion judge methodology).
4. Phase 6/7 sign-off operates on snapshot archive.
5. Wave-close documentation (jack-ryan) explicitly marks Phase 3 gauntlet
   metrics + Phase 4 archive PROVISIONAL pending manifestation-milestone-
   enabled playtest validation.

RATIONALE: per canonical/story/2026-06-01-gauntlet-metrics-as-provisional-
hypotheses-recognition.md, gauntlet metrics are designer-asserted without
empirical validation instrument; iterating to convergence is converging
toward unvalidated ground truth; closure at snapshot + provisional marker
preserves work-done while honoring substrate-led discipline at the metric
layer.

UNBLOCKS: pattern library Phase A gating (no longer waits for gauntlet
convergence; waits for manifestation milestone instead, which is the
appropriate empirical validation instrument).
```

---

## 5. Sequencing implications for pattern library work

Per `2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 5.2, pattern library Phase A gates on (a)+(b)+(c). This recognition refines the gating semantics:

| Gate (placeholder) | Refinement (this recognition) |
|---|---|
| (a) Cycle 14 wave-5 closing | **Closes faster** — at snapshot rather than gauntlet convergence. Estimated gating duration reduced. |
| (b) WS1A foundations landing | Unchanged. Substrate axis expansion + Phase 5 LLM amendment + flavor wiring remain required prerequisites. |
| (c) Manifestation milestone | **Strengthens** — playtest validates BOTH (b) hypothesis-cell patterns AND the gauntlet metrics that produce those patterns. Same playtest instrument; two-layer validation. |

**Net effect on pattern library Phase A horizon:**
- Wave-5 closes sooner (days/weeks rather than weeks/months of continued iteration)
- WS1A horizon unchanged (still 4-8 weeks)
- Manifestation milestone horizon unchanged (still 3-6 months)
- Pattern library Phase A begins after all three resolve → **horizon shortens by ~weeks** as wave-5 no longer blocks

Net Phase A start estimate: **5-11 months from now** (down from 6-12 month range in placeholder).

---

## 6. What this recognition does NOT do

- Does NOT amend doc 47 (damage scaling architecture), doc 50 (BVV), doc 51 (investment scaling). Those docs codify the gauntlet metrics' intended function; they're not invalidated. The recognition is about how we TREAT the outputs (provisional vs defining), not about whether the underlying design is flawed.
- Does NOT discard wave-5 work. All work-products are preserved; PROVISIONAL marker is the operational change.
- Does NOT block Cycle 15+ engine development. Cycle 15+ proceeds with provisional-snapshot inputs from wave-5; refinement happens at validation gate.
- Does NOT amend the substrate-led discipline canonical doc itself. The Disc #41 amendment candidate in § 3.1 is a proposal for jack-ryan ratification; this record canonicalizes the discipline observation, not the discipline amendment.
- Does NOT change Phase 5 cohesion judge methodology. The cohesion judge operates against whatever archive is provided; provisionality at the archive layer doesn't change cohesion-judge correctness.
- Does NOT obligate immediate refactoring of gauntlet code. Code remains as-is; outputs are marked provisional in documentation; refinement happens when playtest evidence enables.

---

## 7. Cross-references

### 7.1 Composes with

- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — pattern library architecture; this recognition strengthens § 5.2 gating semantics
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle; this recognition extends substrate-led discipline to the gauntlet-metric layer
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — damage architecture (gauntlet axis); recognition treats this axis as provisional at the calibration layer
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — BVV thresholds are designer-asserted; provisional
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — investment scaling math is partially-validated; calibration layer remains provisional
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led — extension proposed) + § 42a (framing-audit — applied)

### 7.2 Refines

- Cycle 14 wave-5 closeout procedure (snapshot vs convergence)
- Pattern library Phase A gating semantics (gates strengthen for (c); shorten for (a))
- Wave-close canonical write template (PROVISIONAL marker discipline)
- Recognition-validate-commit discipline applied to gauntlet itself

### 7.3 Anticipates

- **Disc #41 amendment** (jack-ryan canonical write at appropriate gate): substrate-led discipline applies at BOTH substrate-input layer AND validation-metric layer
- **Gauntlet metric refinement workstream** (Cycle 15+ post-manifestation): playtest evidence enables KPM threshold recalibration + BVV threshold validation + cohort taxonomy empirical mapping + encounter representativeness audit
- **Pattern library cell graduation discipline** (per hypothesis-flow placeholder § 6.6): graduation criteria for LIBRARY-LOCKED transition include both hypothesis-cell playtest confirmation AND gauntlet-prediction playtest confirmation. Two-layer empirical validation.

### 7.4 Does NOT amend

- Doc 38 downstream delivery strategy (this recognition is upstream of delivery)
- Doc 02 roadmap (the gates per § 5 of placeholder are already in roadmap)
- Cycle 14 v1 architecture (Cycle 14 is the cycle this recognition CLOSES; doesn't amend)
- Phase 5 LLM cohesion judge prompts (per WS1A.2 amendment scope; not this scope)

---

## 8. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-31 verbatim recognition surfaced during Pattern B dialogue on Cycle 14 wave-5 closure sequencing

**For:** the durable canonical record that:
1. **Names the discipline observation** — iterating to convergence on unvalidated metrics is wasted iteration; substrate-led discipline applies at the validation-metric layer as well as the substrate-input layer
2. **Locks the operational consequence** — wave-5 closes at snapshot; outputs marked PROVISIONAL; gauntlet metric refinement deferred to post-manifestation-milestone playtest
3. **Strengthens the hypothesis-flow methodology** — playtest validates both hypothesis-cell patterns AND gauntlet metrics; two-layer empirical validation; same instrument
4. **Refines pattern library Phase A gating** — wave-5 gate shortens (closes faster); manifestation milestone gate strengthens (validates two layers)
5. **Preserves work done** — all wave-5 outputs preserved as provisional working-state; nothing discarded

**Empirical foundation:** Matt 2026-05-31 framing-audit observation. The recognition itself is the framing audit Q3 answer surfacing. No prior empirical research was needed to surface the recognition; the discipline observation is logically prior to empirical investigation.

**Composition target:** foundational discipline observation for the gauntlet-metric layer of validation; foundation for the Cycle 15+ gauntlet refinement workstream; reference architecture for any future validation-instrument-validity audits at other engine layers.
