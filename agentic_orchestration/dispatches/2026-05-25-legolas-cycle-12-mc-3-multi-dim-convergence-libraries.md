# Dispatch — 2026-05-25 — legolas — Cycle 12 MC-3 multi-dim convergence implementation libraries consult

**From:** knight-rider
**To:** legolas (Mode A — analytical research; read-only)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — Q6 Option B substrate-led methodology consultation timing — MC-3 fires at Layer 4 start per framing brief § 8) + KR autonomously orchestrates per scope-doc § 1 + skip-confirmation re-auth 2026-05-25
**Estimated effort:** ~1 day legolas Mode A
**Acceptance:** Methodology recommendation memo at `agentic_orchestration/legolas/research/cycle-12-mc-3-multi-dim-convergence-libraries-2026-05-25/methodology-recommendation.md` covering scipy vs custom implementation choices for 5-6-dimensional convergence per math note v1.1; cheapest-refuting-test design; resource-bounds projection; sources cited

---

## Context

Cycle 12 Layer 4 (W1.13 multi-dim convergence per math note v1.1) is a load-bearing math hotspot per Discipline #18 (methodology-before-execution). Before rocket implements Layer 4, legolas Mode A consultation is REQUIRED to recommend implementation libraries for the multi-dim convergence per math note v1.1 § 5.

The convergence is **5-6 dimensions** per math note v1.1:
- per-node SP × Tier 4 keystone discrete × trigger interaction discrete × scalar modifier × gear affix vector × tier-specific coefficient

Key question per framing brief § 2 MC-3: **scipy vs custom for the 5-6-dimensional optimization**?

Layers 2 + 3 BOTH COMPLETE (✅ Layer 3 + Gate-2 PASS 2026-05-25; ✅ Layer 2 done; Layer 2 Gate-2 IN-FLIGHT parallel with this MC-3 fire). Layer 4 fires immediately after BOTH Layer 2 Gate-2 PASS + MC-3 returns.

MC-3 fires in PARALLEL with jack-ryan Gate-2 on Layer 2 (independent sub-agent invocations; both gate Layer 4 launch).

---

## Required reading before starting

### Authority-of-record (LOCKED canon)

- **`canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`** v1.1 — **primary load-bearing** (entire doc; especially § 3.6 axis-id vocabulary; § 4.2-4.3 multi-tier voting; § 5 convergence math)
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 4 ConvergenceResult contract (LOCKED) + § L5 (W1.13 multi-dim convergence as Layer 4 scope) + § 2 MC-3 (this consult scope statement)
- **`agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`** § 1 + § 5 + § 6
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md` — W1.13 rescope context (W1.13 dispatch original § 0.0 FIRE-GATE procedurally closed per Cycle 12 framing brief § 0; multi-dim convergence fires per Cycle 12 scope, not original dispatch directly)

### Methodology + critique-pair inputs (precedent + Layer 2/3 outputs to consume)

- **`agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md`** (MC-1 precedent — same Mode A methodology consult pattern)
- **`agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md`** (MC-2 precedent + downstream context — Layer 4 convergence consumes substrate-bound PlayerClass)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (earliest legolas methodology consult — pattern reference)
- Layer 2 dispatch + completion record: `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-2-bc-target-subspace-generator.md` (PlayerClassV2 shape Layer 4 will consume)
- Layer 3 dispatch + completion record: `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-3-skill-content-and-sc-3.md` (SkillTree shape with `bc_axis_contribution: dict[str, float]` 8-key vocabulary Layer 4 walks per math note v1.1 § 4.2-4.3)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-3.md` (Gate-2 on L3 verified Layer 4 walkability simulated in Gate-6 test; consume verdict)

### Engineering-disciplines

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — load-bearing: #1 (math-before-code) + #18 + #18.2 (methodology-before-execution at hotspots) + #19/#19.1 (background processes + cheapest-refuting-test) + #23 (framing-audit checklist) + #24 (single-parameter-sweep isolation if relevant)

---

## Math-before-code (per Discipline #1)

No code in this consult — Mode A research only. But methodology recommendation MUST surface:

- Mathematical objective of 5-6-dim convergence: per math note v1.1 § 5 — what's the optimization target (win-rate band [0.45, 0.55] within max_iterations=5; tier-specific coefficients per § 4.2-4.3)
- Optimization function shape: categorical × continuous × discrete; per-node SP + T4 keystone + trigger interaction + scalar modifier + gear affix vector + tier-specific coefficient interaction
- Per-dim characteristics: per-node SP is continuous bounded; T4 keystone is discrete enum; trigger interaction is discrete enum; scalar modifier is continuous; gear affix is vector; tier-specific coefficient is per-tier weight
- Convergence guarantees: under what conditions does the algorithm converge in max_iterations=5? When does it fail to converge (escape-hatch trigger)?

---

## Scope (legolas Mode A consult)

Mode A analytical research (read-only; ~1 day budget):

### Library / implementation choice options

- **scipy.optimize** — `minimize` with method choices (Nelder-Mead, Powell, COBYLA for derivative-free; SLSQP for constrained); BFGS variants for gradient-based; differential_evolution for global; basinhopping
- **scipy.optimize.differential_evolution** — global optimizer for mixed-discrete-continuous spaces (could handle T4 keystone discrete + per-node SP continuous via wrapper)
- **Custom implementation** — hand-rolled iteration matching math note v1.1 § 5 exactly; no external library; deterministic + reproducible per generation_seed
- **Hybrid** — scipy for continuous dims (per-node SP, scalar modifier, gear affix) + custom for discrete dims (T4 keystone, trigger interaction); coordinated convergence loop

### Per-option analysis

- Per-method numerical convergence behavior (does the method converge for typical kit inputs; under what failure conditions)
- Compute envelope (per-iteration cost; per-100-kits scaling; expected wall-clock for 22-25 kits at max_iterations=5)
- Reproducibility characteristics (deterministic given seed; floating-point reproducibility considerations)
- Mixed-type support (continuous × discrete handling)
- Integration with existing engine codebase (does scipy fit cleanly; is there installation/dependency concern; does custom add maintenance burden)
- Convergence diagnostic / introspection (which method exposes iteration count, per-iteration state, etc.)

### Algorithmic refinements

- Per math note v1.1 § 4.2-4.3 multi-tier voting: how does the multi-tier voting integrate with the chosen optimization method (voting drives the per-dim adjustments per iteration)
- Per-dim ordering: should convergence cycle through dims one-at-a-time (coordinate descent) OR all-at-once (full gradient)
- max_iterations=5 cap: is this realistic for the chosen method; what's the escape-hatch behavior at cap (return best-found-so-far OR fail-to-converge)
- Bump-iterations if non-convergence detected: per scope-doc § 6 — if convergence doesn't converge within max_iterations=5, route to gamora + rocket collaboration; bump max_iterations if helpful; if structural non-convergence, route back to legolas Mode A for methodology refinement

### Cheapest-refuting-test design (Discipline #19.1)

- What's the minimal experiment that would refute a proposed Layer 4 implementation? (e.g., 30-kit smoke; convergence rate ≥80% within max_iterations=5; per-kit final_modifier within target_win_rate_band)
- Per-test pass/fail thresholds + escape-hatch criteria

### Resource-bounds projection (Discipline #1.1)

- Per-method peak memory + runtime envelope at Layer 4 implementation scale (22-25 kits × max_iterations=5)
- Background-process firing pattern if compute exceeds session-foreground budget

### Methodology recommendation memo (output)

- Proposed method + rationale
- Implementation-shape sketch (just enough for rocket Layer 4 dispatch to consume)
- Discipline #23 framing-audit application
- Cross-reference to math note v1.1 sections that drive each implementation choice

---

## Out of scope

- Algorithm Layer 4 implementation in rocket (gated on this consult + Gate-2 on L2 PASS)
- Engine code changes (Mode A is read-only)
- Architectural amendments to math note v1.1 / framing brief / composition policy (escalate to gandalf if surfaced)
- Direct testing against substrate / no DB writes
- Cross-seam consultation beyond legolas Mode A (jack-ryan Gate-2 happens AFTER rocket Layer 4 lands)
- Layer 6 § 8 wire-up design (Layer 6 scope; not L4)
- Layer 7 BDI test framework (DEFERRED to v1.1)

---

## Acceptance criteria

- [ ] Mode A literature scan completed; sources cited (especially scipy.optimize reference + ARPG-adjacent convergence literature)
- [ ] Per-library/implementation analysis (scipy / scipy.differential_evolution / custom / hybrid)
- [ ] Per-method numerical + computational + reproducibility analysis
- [ ] Mixed-type support analysis (continuous × discrete × categorical)
- [ ] Algorithmic refinement analysis (coordinate descent vs full gradient; multi-tier voting integration; max_iterations cap handling)
- [ ] Cheapest-refuting-test design with concrete pass/fail thresholds
- [ ] Resource-bounds projection (per Discipline #1.1)
- [ ] Methodology recommendation with implementation-shape sketch
- [ ] Discipline #23 framing-audit checklist application
- [ ] Output artifact at `agentic_orchestration/legolas/research/cycle-12-mc-3-multi-dim-convergence-libraries-2026-05-25/methodology-recommendation.md`
- [ ] Auto-commit + auto-push per legolas seam authorization (CLAUDE.md addendum)
- [ ] Tag: `legolas/cycle-12-mc-3-multi-dim-convergence-libraries-2026-05-25`

---

## Open questions for the agent to resolve

- Whether the recommended method should be deterministic or stochastic (deterministic per generation_seed for reproducibility per WARN-7 amendment; stochastic for global-optimization characteristics)
- Whether max_iterations=5 cap is right OR should be configurable per kit (e.g., harder-to-converge kits bump higher); legolas may recommend a per-dim convergence-threshold approach
- Whether to recommend gradient-based methods (require derivative; need to model continuous functions) OR derivative-free (more robust for categorical mixing); legolas Mode A judgment
- Whether MC-3 ↔ Gate-2-on-L2 dependency surfaces (e.g., MC-3 recommendation depends on PlayerClassV2 shape Layer 2 emits); legolas judgment

---

## Cross-seam impact

Round-trip: not applicable — Mode A research only; no DB writes; no cross-seam contract change. Methodology recommendation informs rocket Layer 4 dispatch authoring; round-trip happens at rocket Layer 4 output + cross-seam contract per framing brief § 4 ConvergenceResult.

---

## References

- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 (primary)
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md`
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 ConvergenceResult + § L5 + § 2 MC-3
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md` (precedent + downstream context)
- `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md` (precedent + downstream context)
- Layer 2 + Layer 3 dispatches + completion records
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1 + #18 + #18.2 + #19.1 + #23

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q6 Option B substrate-led methodology consultation timing — MC-3 fires at Layer 4 start) + Discipline #18 LOAD-BEARING gate on rocket Layer 4 implementation + skip-confirmation re-auth 2026-05-25
**Status:** FIRE — Wave 2 parallel-fire with jack-ryan Gate-2 on Layer 2; gates rocket Layer 4 dispatch authoring

**Matt-touch sequence:** consult returns → KR integrates into rocket Layer 4 dispatch authoring (parallel with Gate-2 on L2 clearance); rocket Layer 4 fires autonomously per scope-doc § 1 + skip-confirmation re-auth

---

## Completion record

**Completed:** 2026-05-25
**Status:** COMPLETE
**Output artifact:** `agentic_orchestration/legolas/research/cycle-12-mc-3-multi-dim-convergence-libraries-2026-05-25/methodology-recommendation.md`

**Recommendation summary:**
- **Primary method:** Custom implementation per math note v1.1 § 4.2-4.3 exactly. No scipy primary dependency.
- **Per-dim ordering:** three-phase blocked grouped update (Phase 1: SP voting; Phase 2: Tier 4 keystone selection; Phase 3: trigger interaction selection).
- **max_iterations=5 posture:** configurable; default 5; bump path to 10 via `resume_convergence`; return best-found-so-far on cap hit.
- **scipy use:** optional secondary only — `minimize_scalar` bounded for Dimension 5 if smoke reveals scalar bottleneck; `differential_evolution` as last-resort structural-non-convergence fallback only.
- **MC-3 ↔ Gate-2-on-L2 dependency:** NONE. Recommendation is independent of PlayerClassV2 shape. Rocket Layer 4 should verify gauntlet call interface as pre-implementation step.
- **Surprises:** T_AXIS_SENS calibration parameters (9 total per math note v1.1 § 10) are all pending Discipline #17 sweeps — rocket Layer 4 dispatch must include parametrized initial values + sweep plan in its math-before-code section.

**Cheapest-refuting-test:** 30-kit smoke; ≥80% convergence rate within max_iterations=5; ~15-22 min wall time at v1 scale.

**Acceptance criteria check:**
- [x] Mode A literature scan completed (scipy / differential_evolution / custom / hybrid compared in § 2)
- [x] Per-library/implementation analysis (§ 2 + § 2.5 summary table)
- [x] Per-method numerical + computational + reproducibility analysis (§ 2.1-2.4 + § 8.2 envelope table)
- [x] Mixed-type support analysis (§ 6)
- [x] Algorithmic refinement analysis (§ 3 coordinate descent vs full gradient; § 4 voting integration; § 5 max_iterations cap handling)
- [x] Cheapest-refuting-test design with concrete pass/fail thresholds (§ 7)
- [x] Resource-bounds projection (§ 8)
- [x] Methodology recommendation with implementation-shape sketch (§ 9)
- [x] Discipline #23 framing-audit checklist (§ 11)
- [x] Output artifact at correct path
