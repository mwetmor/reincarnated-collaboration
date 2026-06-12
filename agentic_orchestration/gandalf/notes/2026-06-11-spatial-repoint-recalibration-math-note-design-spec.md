# Design-Spec Handoff — Spatial Re-Point + Recalibration Math-Note (gamora)

**STATUS:** DESIGN-SPEC HANDOFF — gandalf → gamora (via KR sequencing post-Gate-1)
**Date:** 2026-06-11
**Authority:** Matt, this session — remedy (b) AUTHORIZED ("fold the re-point into the recalibration math-note and proceed")
**Contract basis:** `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` § 3 (first application), § 8.1 disposition 3, § 8.2 amendment
**Discipline anchors:** #1 math-before-code; § 3 kernel-change protocol (math-note → golden-master capture → isolated change → predicted-delta verification → telemetry tag); #24 single-parameter isolation

---

## 1. What is authorized (one work item, not two)

**Re-point spatial commit-grade damage at `damage_resolver.resolve_skill` AND recalibrate the spatial constants — as a single math-note.** They are inseparable: `SPATIAL_DAMAGE_SCALE=4.0` (and `MOB_HP_DIFFICULTY_MULTIPLIER=1.5`) were calibrated against the simplified model (`spatial_gauntlet/spatial_engine.py` ~L886: `damage_multiplier × 500.0 × damage_modifier`); re-pointing invalidates the calibration by construction. Do not recalibrate the simplified model first and re-point second — that calibrates a model being retired.

**Design rationale (on record, contract § 8.2.1):** the simplified model cannot express kernel mechanics — chaos_immune shadow nullification (T4 DEFENSIVE_TRADEOFF; the PoE Chaos Inoculation analog), W-α1 three-path `damage_scaling_type` routing, ±15% per-hit variance (Prop 3 / KI-B6-1), buff interactions. Commit-grade fidelity must run the kernel's damage truth, single-sourced at both fidelities.

## 2. Math-note REQUIRED contents (beyond the re-point itself)

1. **Golden-master capture FIRST** (§ 3 protocol step 2): pin the current spatial engine's outputs on a reference corpus before any change. The old simplified-model path stays alive as the oracle during transition.
2. **Predicted-delta statement** for the re-point: which scenario cells should move, in which direction, and why (e.g., DEFENSIVE_TRADEOFF kits vs shadow-dealing scenarios flip; variance widens per-hit). Unpredicted movement = stop and diagnose.
3. **Recalibration of the spatial constants against the resolver-backed path** — season_001010 WR=1.0 ceiling saturation (engine's own R2-calibration warnings) is the symptom being cured; state the target WR distribution shape.
4. **Re-gate multiplier model (contract § 8.2.2 — gating production sweeps):** the § 4 sweep numbers are per-gauntlet-pass (your own scaffold S7: convergence multiplier OUT OF MODEL). Model the hybrid regime: cycling at duel fidelity; spatial = one commit-gate pass + re-gates on recomposed near-misses. Bound spatial cost growth as failing-fraction × mean re-gates with stated assumptions. No production sweep is scheduled until this bound exists.
5. **Cost-profile re-check after re-point:** resolver-backed spatial per-fight cost may differ from simplified-model cost (the measured ~9 s warm / ~43 s cold were profiled on the surviving engine). State whether § 4 contract numbers need a re-measure trigger pull.
6. **PC parallel-factor measurement rides along** (replaces re-profile S4 ASSUMED 12×): run the throughput harness on the PC 20-core box; bank the measured Mac+PC combined factor.

## 3. Interface constraint (contract § 8.2.3 — do NOT harden)

The thin parallel runner and any recompose-touching interfaces must NOT bake in flat-lever assumptions (modifier nudge / list-based skill swap). The future T4 skill profile is chains-within-trees; recompose becomes structure-aware when that design lands. Filter regime (one pass per variant) is NOT gated on T4 profile design; cycling regime IS.

## 4. Scope boundary

- Kernel files (`resolve_skill`, `fight_engine.simulate_fight` internals) are READ-ONLY except via the § 3 protocol this math-note instantiates.
- The re-point changes the *spatial engine's call target*, not the resolver.
- Telemetry tag the change per § 3 step 5 so before/after populations are separable.

**Author:** gandalf, 2026-06-11. First application of the kernel-change protocol — this math-note is also the protocol's proving run.
