# Reap. Die. Rise. — ENGINE Spec (Index + Fold Worklist)

**STATUS:** LIVE SPEC HOME (born 2026-06-30, canonical reorg Tranche 2; **stale-state corrected 2026-07-01** — the `canonical/reap-die-rise/` migration ALREADY LANDED in commit `6b9d6d1`; the six build docs live HERE and are authoritative). The numbered engine docs `canonical/37–51` remain authoritative for their content until folded/moved in per (b)/(b′).
**Author:** gandalf (scaffold + worklist). **The engine-content folds are cross-seam** — each needs a **capture-check** (is the load-bearing content already in the engine tracker or the build docs?) and may route to the owning seam (rocket / gamora / star-lord) rather than being gandalf-folded.
**Delta tracker (how far the build is from this spec):** `canonical/current-to-end-state/current-to-end-state-engine.md` (currently at `canonical/current-to-end-state/current-to-end-state-engine.md`).

---

## What this folder will hold

The buildable engine spec — generation, simulation, balance, gear/stat/T4 architecture, progression, content-emission, the build/networking/perf/render technical stack.

## ✓ MIGRATED IN from `canonical/reap-die-rise/` (DONE 2026-06-30, commit `6b9d6d1` — folder dissolved)

`build-architecture.md` · `backend-networking-stack.md` · `performance-target-specs.md` · `godot-agent-contract.md` · `vfx-pipeline.md` · `design-decisions-session.md`

## ✓ FOLDED IN — cosmograph-trio engine survivor (2026-07-01)

**Creation-flow engine contract** (from `story/2026-06-05-cosmograph-pivot.md` §4.1 + `story/2026-06-07-earth-avatar…` §12.6–12.7, folded per story-tracker A11; sources deleted): **the engine pre-generates the kit corpus; the game (Binding Rite, `reap-die-rise-story/story-expansion.md §13a`) SELECTS and LOOKS UP — nothing is generated at the altar** (composes with D7 lookup-not-generation). The rite's contract on the engine: **(1)** nearest-kit lookup over the pre-generated corpus **honoring the player-named precedent** (the elicitation-cascade INPUT ordering); **(2)** INPUT vs OUTPUT partition — inputs are player-committed (ancestry/element/weapon-form/power/style/harvest/horizon vocabulary), outputs are engine-emerged and narrated at emergence (attributes, off-hand, resource model, ailments, passives), never selected; **(3)** **coverage-filtered option display** — each cascade layer surfaces only options with non-zero substrate coverage within the committed precedent (no 0-match state reachable). Presentation halves live at game-tracker A′3; this folder owns only the lookup/emission contract.

## Folds IN — the numbered engine spine (`canonical/37–51`)

KEEP→ENGINE: `37-engine-and-game-two-products` · `38-downstream-delivery-strategy` · `39-qd-engine-end-to-end-workflow` · `40-gear-balance-guide-architecture` · `41-progression-framework` · `42-stat-sheet-modifier-partition` · `46-concentration-architecture` · `47-damage-scaling-architecture` · `49-loadout-sample-player-surface` · `50-bounded-viability-with-specialization` · `51-investment-scaling-6-pattern`
**? capture-check (Wave-N intent docs — intent may have landed in code → fold residual / kill):** `43-t4-algorithm-wave-2-intent` · `44-t4-algorithm-wave-3-phase-3-intent` · `45-spec-driven-gear-gen-wave-4-intent`

## Folds IN — engine-mechanics story docs (`canonical/story/`)

Cluster D (per fold-map): attribute-system *(carries Matt 2026-06-24 VIT-DELETE)* · skill-system · off-hand-items · v1-bc-target-intent · qd-engine-bc-axes-lock · stat-derivation-from-bc-convergence · multi-dim-convergence-algorithm · tier-4-architecture-defaults · bdi-omega-tau-tables-v1 · gear-heavy-promotion · gear-spec-element-flavor-manifest · gear-spec-generation-deferred-architecture · gear-substrate-rule-table-v1 · proxy-add-design-spec · proxy-commander-set-6-capstone-spec · six-profile-set-architecture · representative-loadout-measurement-contract · ~~seasonal-hero-h-5-hybrid-spec~~ *(DELETED 2026-07-01 Batch-1 — stale H-5 hybrid intent, captured at decisions-log #57; do not chase in the B4 fold)* · styleprofile-output-shape-ruling · thematic-registry · c-hybrid-cell-and-curation-architecture · phase-5-{cohesion-judge-calibration, llm-prompts-cohesion-judge, t4-narration-amendment} · phase-7-2-layer-joint-gate-spec · weapon-as-identity-surface-recognition · telegraph-dodge-temporal-decoupling · battle-room-presentation-decoupling · ~~arpg-physical-magical-ratio-baseline~~ *(DELETED 2026-07-01 Batch-1 — baseline captured at decisions-log #57; do not chase in the B4 fold)* · 2d-spatial-golden-oracle-spec · combat-fidelity-drift-proofing · flavor-pool-per-primary-element-lock

Substrate keeper (?): `2026-06-06-atomic-substrate-registry` (CANONICAL — →ENGINE or elrond-owned).

## Routes ELSEWHERE (not folded here, not blind-killed)

- **Methodology / principle docs → jack-ryan engineering-disciplines** (not the game spec): ~~`2026-05-29-designer-writes-substrate-player-names-experience-principle`, `v1-1-plus-design-discipline-recognitions`~~ *(DELETED 2026-07-01 per Matt "do not defer" — proposed disciplines entries stand verbatim in `gandalf/notes/2026-07-01-rulings-harvest.md` §Methodology; jack-ryan registers from there at next disciplines touch)*. **`2026-05-31-hypothesis-flow-pattern-library-architecture` RECLASSIFIED → Cluster-D engine fold** — live engine sidecar (`canonical/sidecars/emit_experiential_axes.py` + `experiential_axes_v1.json`) names it GOVERNING doc; §3.5 cell-schema + §1.7 flavor-judgment locks are engine spec content, not just methodology.
- **Team/infra architecture → build-architecture annex or keep**: `2026-06-07-federated-pc-team-architecture-commit` (**CLAUDE.md first-read** — do not orphan).
- **Substrate/lineage curation → elrond, not canonical-story**: ~~the 5 lineage dispositions + variant-cluster-policy~~ *(DELETED 2026-07-01 Batch-1 — rulings harvested to ledger)*; **tagging-pattern + cleaning-policy MOVED → `agentic_orchestration/elrond/notes/` (E2, live OP/SKILL-cited)**; legacy-categorical-cleanup-audit MOVED → `agentic_orchestration/elrond/notes/` 2026-07-01 (E2; gandalf+elrond OP/SKILL re-pointed — carries the six vestigial-retirement ruling family, harvest row pending decisions-log registration).

**Author:** gandalf, 2026-06-30. Per fold-map `agentic_orchestration/gandalf/notes/2026-06-30-canonical-reorg-fold-map.md`.
