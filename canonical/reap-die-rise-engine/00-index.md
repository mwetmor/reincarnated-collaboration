# Reap. Die. Rise. — ENGINE Spec (Index + Fold Worklist)

**STATUS:** SCAFFOLD (born 2026-06-30, canonical reorg Tranche 2). This is the **END-STATE engine spec** folder, assembled by strategy **(b) heavyweight-fold** — distilling the numbered engine docs + engine-mechanics story docs into a tight spec, deleting sources as content lands. Until the fold completes, the authoritative engine specs still live at `canonical/37–51` and `canonical/reap-die-rise/` (see tables).
**Author:** gandalf (scaffold + worklist). **The engine-content folds are cross-seam** — each needs a **capture-check** (is the load-bearing content already in the engine tracker or the build docs?) and may route to the owning seam (rocket / gamora / star-lord) rather than being gandalf-folded.
**Delta tracker (how far the build is from this spec):** `canonical/current-to-end-state/current-to-end-state-engine.md` (currently at `canonical/current-to-end-state/current-to-end-state-engine.md`).

---

## What this folder will hold

The buildable engine spec — generation, simulation, balance, gear/stat/T4 architecture, progression, content-emission, the build/networking/perf/render technical stack.

## Migrates IN from `canonical/reap-die-rise/` (at the final verified rewire pass)

`build-architecture.md` · `backend-networking-stack.md` · `performance-target-specs.md` · `godot-agent-contract.md` · `vfx-pipeline.md` · `design-decisions-session.md`

## Folds IN — the numbered engine spine (`canonical/37–51`)

KEEP→ENGINE: `37-engine-and-game-two-products` · `38-downstream-delivery-strategy` · `39-qd-engine-end-to-end-workflow` · `40-gear-balance-guide-architecture` · `41-progression-framework` · `42-stat-sheet-modifier-partition` · `46-concentration-architecture` · `47-damage-scaling-architecture` · `49-loadout-sample-player-surface` · `50-bounded-viability-with-specialization` · `51-investment-scaling-6-pattern`
**? capture-check (Wave-N intent docs — intent may have landed in code → fold residual / kill):** `43-t4-algorithm-wave-2-intent` · `44-t4-algorithm-wave-3-phase-3-intent` · `45-spec-driven-gear-gen-wave-4-intent`

## Folds IN — engine-mechanics story docs (`canonical/story/`)

Cluster D (per fold-map): attribute-system *(carries Matt 2026-06-24 VIT-DELETE)* · skill-system · off-hand-items · v1-bc-target-intent · qd-engine-bc-axes-lock · stat-derivation-from-bc-convergence · multi-dim-convergence-algorithm · tier-4-architecture-defaults · bdi-omega-tau-tables-v1 · gear-heavy-promotion · gear-spec-element-flavor-manifest · gear-spec-generation-deferred-architecture · gear-substrate-rule-table-v1 · proxy-add-design-spec · proxy-commander-set-6-capstone-spec · six-profile-set-architecture · representative-loadout-measurement-contract · seasonal-hero-h-5-hybrid-spec · styleprofile-output-shape-ruling · thematic-registry · c-hybrid-cell-and-curation-architecture · phase-5-{cohesion-judge-calibration, llm-prompts-cohesion-judge, t4-narration-amendment} · phase-7-2-layer-joint-gate-spec · weapon-as-identity-surface-recognition · telegraph-dodge-temporal-decoupling · battle-room-presentation-decoupling · arpg-physical-magical-ratio-baseline · 2d-spatial-golden-oracle-spec · combat-fidelity-drift-proofing · flavor-pool-per-primary-element-lock

Substrate keeper (?): `2026-06-06-atomic-substrate-registry` (CANONICAL — →ENGINE or elrond-owned).

## Routes ELSEWHERE (not folded here, not blind-killed)

- **Methodology / principle docs → jack-ryan engineering-disciplines** (not the game spec): `2026-05-29-designer-writes-substrate-player-names-experience-principle`, `v1-1-plus-design-discipline-recognitions`, `2026-05-31-hypothesis-flow-pattern-library-architecture`.
- **Team/infra architecture → build-architecture annex or keep**: `2026-06-07-federated-pc-team-architecture-commit` (**CLAUDE.md first-read** — do not orphan).
- **Substrate/lineage curation → elrond, not canonical-story**: the 5 lineage dispositions + tagging-pattern + variant-cluster-policy + cleaning-policy + legacy-categorical-cleanup-audit.

**Author:** gandalf, 2026-06-30. Per fold-map `agentic_orchestration/gandalf/notes/2026-06-30-canonical-reorg-fold-map.md`.
