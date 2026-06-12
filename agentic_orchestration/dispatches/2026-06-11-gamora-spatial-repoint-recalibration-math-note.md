# Dispatch — 2026-06-11 — gamora — Spatial Re-Point + Recalibration Math-Note (first § 3 application)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-11 (this session, via gandalf Pattern-B dialogue) — remedy (b) AUTHORIZED, "fold the re-point into the recalibration math-note and proceed"
**Estimated effort:** multi-day (Pattern B) — math-before-code, kernel-protocol proving run
**Acceptance:** the kernel-change protocol (contract § 3) completes its FIRST end-to-end application: kernel interface declared in MIGRATION.md → golden-master captured → approved math-note → isolated re-point + recalibration → every output delta predicted-or-STOP → telemetry tag shipped. Spatial earns commit-grade fidelity status (§ 5 gate) only on protocol completion. Gate-2 (jack-ryan) PASS at close.

## Context (why this matters)

This is the **first application of the forward-architecture contract's § 3 kernel-change protocol — it is therefore also the protocol's proving run.** It is the test case that proves the protocol before anything heavier (the id-substrate rebuild, future resolver changes) walks the same door. Get the worked reference right and every subsequent kernel change inherits a concrete template; get it loose and the protocol is undefined on first use.

Two facts make the re-point and the recalibration **one inseparable work item, not two:** commit-grade spatial currently runs a *simplified* damage model (`spatial_gauntlet/spatial_engine.py` ~L886: `damage_multiplier × 500.0 × damage_modifier`) that bypasses `damage_resolver.resolve_skill`. The constants `SPATIAL_DAMAGE_SCALE=4.0` and `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` were calibrated *against that simplified model*. Re-pointing commit-grade at `resolve_skill` invalidates the calibration by construction — so recalibrating the simplified model first and re-pointing second would calibrate a model being retired. Do both in one math-note. The simplified model cannot express kernel mechanics (chaos_immune shadow nullification, W-α1 three-path `damage_scaling_type` routing, ±15% per-hit variance per Prop 3 / KI-B6-1, buff interactions); a DEFENSIVE_TRADEOFF kit gauntleted under it is graded on combat where its build-defining covenant does not exist. Commit-grade must run the kernel's damage truth, single-sourced at both fidelities.

## Sequencing — Phase 0 is a HARD GATE (jack-ryan Gate-1 WARN)

Jack-ryan's Gate-1 on the contract returned **PASS-with-INFO** with one **WARN (Dimension 1):** contract § 2 names kernels by *description*; the enforceable boundary lives in MIGRATION.md declarations that this first dispatch must produce **before** any consuming code lands. Per § 2 line 50, "undeclared kernel entry-points are not consumed." KR is holding this dispatch to that ordering. **No new consuming code is authored before the Phase 0 interface declaration commits.**

The simulation audit (commit `477dee3`) already proved the boundary is drawable today at `fight_engine.simulate_fight(...) -> FightResult` (`fight_engine.py:107`) — a pure deep-copying function, grep-confirmed zero telemetry/DB/LLM/HTTP coupling across all 7 kernel files. Phase 0 binds that signature in MIGRATION.md as the enforceable wrap boundary. The audit hands you the exact signature to declare.

## Required reading before starting

- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` — **§ 3** (kernel-change protocol, the 5 ordered steps), **§ 8.1 disposition 3** (the two-damage-path finding), **§ 8.2.1** (re-point authorization), **§ 8.2.2** (cycling-cost-model + re-gate multiplier requirement), **§ 8.2.3** (T4-native interface non-hardening), **§ 5** (combat-fidelity lock / the gate this work satisfies)
- `agentic_orchestration/gandalf/notes/2026-06-11-spatial-repoint-recalibration-math-note-design-spec.md` — the design-spec; **this is the dispatch's substance, read in full**. § 2 lists the six required math-note contents.
- `agentic_orchestration/qa/findings/2026-06-11-forward-architecture-contract-gate-1.md` — Gate-1; Dimension 1 WARN (Phase 0 gate) + INFO-1 (golden-master corpus must be concretely fixed — size, encounter types, archetypes, pin path, commit convention)
- `agentic_orchestration/gamora/notes/2026-06-11-gap-register-architecture-fit-audit-simulation.md` (`477dee3`) — your own audit; the `simulate_fight` boundary evidence + the disposition-3 spatial-precision flag
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — append target for Phase 0 (versioned changelog; add a new top entry)
- Latest `~/Games/reincarnated-engine/design/decisions/decisions-log.md` entry (jack-ryan's combined greenfield-verdict + contract entry, this session — carries the § 8.2.3 T4-sequencing gate)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code), #7 (telemetry tag), #24 (single-parameter isolation), #1.1 (pre-fire resource-bounds projection — spatial gauntlet is full-tick)

## Phases (execute in order; do not parallelize across the Phase 0 gate)

### Phase 0 — Kernel interface declaration (HARD GATE — commits before any other phase)
Declare the simulation-kernel interface in `simulation/MIGRATION.md` per contract § 2's interface-naming obligation: bind `fight_engine.simulate_fight(...) -> FightResult` (`fight_engine.py:107`) as the enforceable wrap boundary — input schema, output schema (`FightResult` shape), purity guarantee (deep-copying, zero telemetry/DB/LLM/HTTP coupling across the 7 kernel files), and the explicit statement that this is the read-only kernel boundary all spatial/runner consuming code calls through. New top entry in the versioned changelog. **Commit Phase 0 standalone before opening Phase 1.** This satisfies the Gate-1 WARN and makes "undeclared kernel entry-points are not consumed" enforceable on the first pass.

### Phase 1 — Golden-master capture FIRST (§ 3 step 2)
Pin the **current** spatial engine's outputs on a reference corpus as the oracle, BEFORE any change. The old simplified-model path stays alive as oracle during transition. **Per Gate-1 INFO-1, fix the corpus concretely — this is the protocol's worked reference for every future application:** N fights, which encounter types, which kit archetypes (cover the cases the re-point should move — DEFENSIVE_TRADEOFF / chaos_immune kits vs shadow-dealing scenarios), the pinned commit path, and the commit convention. Capture before, not after.

### Phase 2 — Math-note authoring (math BEFORE code — Discipline #1)
Author the § 3-protocol math-note carrying **all six design-spec § 2 required contents**:
1. Golden-master corpus definition (from Phase 1, now formalized in the note).
2. **Predicted-delta statement** for the re-point — which scenario cells move, in which direction, why (DEFENSIVE_TRADEOFF/chaos_immune flips; per-hit variance widens). Unpredicted movement at Phase 4 = STOP + diagnose.
3. **Recalibration of `SPATIAL_DAMAGE_SCALE` + `MOB_HP_DIFFICULTY_MULTIPLIER` against the resolver-backed path** — season_001010 WR=1.0 ceiling saturation (engine R2-calibration warnings) is the symptom being cured; state the target WR distribution shape.
4. **Re-gate multiplier model (contract § 8.2.2 — GATES production sweeps):** model the hybrid regime (cycling at duel fidelity 1/11–1/53 spatial cost; spatial = one commit-gate pass + re-gates on recomposed near-misses only). Bound spatial cost growth as failing-fraction × mean re-gates, assumptions stated. **No production sweep is scheduled until this bound exists.**
5. **Cost-profile re-check after re-point** — resolver-backed spatial per-fight cost may differ from the simplified-model ~9 s warm / ~43 s cold; state whether contract § 4 numbers need a re-measure-trigger pull.
6. **PC parallel-factor measurement (replaces ASSUMED 12×, re-profile S4).** See the PC coordination note below.

Math-note routes through gandalf design-lean already on record (remedy (b)); the note argues recalibration with numbers. Gate-2 reviews the note + implementation together at close.

### Phase 3 — Re-point + recalibration implementation (per APPROVED math-note only)
Re-point spatial commit-grade's call target from the simplified model to `damage_resolver.resolve_skill`; apply the recalibrated constants. **The re-point changes the spatial engine's call target, not the resolver** — the resolver and `simulate_fight` internals stay READ-ONLY (kernel; § 4 scope boundary). **Discipline #24 single-parameter isolation:** the re-point and the recalibration are derived as one coupled change in the math-note, but implement so the diff is auditable and the predicted deltas attributable. No other behavior rides along.

### Phase 4 — Predicted-delta verification + telemetry tag (§ 3 steps 4–5)
Re-run the golden-master. **Every output delta is either (a) predicted by the math-note, or (b) a STOP** — unpredicted deltas mean the change is not understood; revert and re-derive, do not paper over. On clean verification, ship the **telemetry tag (Discipline #7)** so before/after populations are separable and the kernel-version lineage is queryable. Spatial earns commit-grade status (§ 5) at this point and not before.

## Interface constraint — carry VERBATIM into the runner/recompose interfaces (contract § 8.2.3)

The thin parallel runner and any recompose-touching interfaces this work brushes **must NOT bake in flat-lever assumptions** (modifier nudge / list-based skill swap). The future T4 skill profile is chains-within-trees; recompose becomes structure-aware when that design lands. The filter regime (one pass per variant) is NOT gated on T4 profile design; the cycling regime IS. Declare any recompose-lever vocabulary you touch as **T4-profile-native-pending**. Do not harden formations the skill system cannot legally express.

## PC parallel-factor measurement — coordination note (design-spec § 2.6)

The PC-side throughput harness run (20-core box) that replaces the ASSUMED 12× factor **requires a PC-side execution** — it cannot run on the Mac box. The PC seam (mantis/david-h) is currently in-flight on the **manifestation spike wave**. Therefore:
- Treat the PC parallel-factor measurement as a **SEPARABLE sub-task** that rides ALONGSIDE the math-note, not a blocker on Phases 0–4.
- The Mac-side math-note and re-point/recalibration complete on the Mac measured single-box numbers; the combined Mac+PC factor is banked when the PC run lands.
- Coordinate the PC run via david-h's PC seam. If PC is saturated by the manifestation spike, **flag to KR and proceed** — the ASSUMED 12× remains explicitly flagged ASSUMED in the math-note (per contract § 8.2.2, banking the combined number is BANNED until measured) and the separable PC sub-task is queued behind the spike wave. Do not block the kernel-protocol proving run on PC availability.

## Math-before-code (Discipline #1)
Phase 2 math-note is fully authored and approved BEFORE Phase 3 implementation. The predicted-delta statement (content 2) is the contract against which Phase 4 verifies — it must be specific enough that an unpredicted delta is unambiguous.

## Cross-seam contract change? (Principle 6 gate — KR completes at authoring time)

Does this dispatch add, modify, rename, or remove any field on a telemetry schema table / fight_log dict key / loadout dict key / export packet structure?

- **Phase 0** writes a kernel-interface DECLARATION to `simulation/MIGRATION.md` — this is the ADR-004 cross-seam artifact itself; the `simulate_fight(...) -> FightResult` boundary is what star-lord's telemetry and the runner consume. No schema field change, but the declaration IS the consumable contract — star-lord should be aware the boundary is now formally named.
- **Phase 4** ships a telemetry tag (Discipline #7) so before/after spatial populations are separable — this is a tag, not a schema-field change, but flag to star-lord at the telemetry boundary so the kernel-version lineage is queryable downstream.
- The re-point changes a call target internal to the spatial engine; `resolve_skill` and `simulate_fight` signatures are READ-ONLY and unchanged. No fight_log / loadout / export-packet field churn expected. **If the resolver-backed path surfaces any new fight_log key vs the simplified model, that IS a cross-seam change → MIGRATION.md entry + star-lord notification before tagging.**

## Out of scope (prevents scope creep)
- Modifying `resolve_skill` or `fight_engine.simulate_fight` internals — kernel, READ-ONLY except via this very § 3 protocol (and this math-note re-points the CALLER, it does not change the kernel).
- Designing the full T4 skill-profile / chains-within-trees recompose (upstream of the cycling regime per § 8.2.3; this dispatch must only avoid HARDENING against it, not build it).
- Scheduling any production spatial sweep — gated on the Phase 2 re-gate multiplier bound existing; not authorized here.
- The id-generation-substrate module-targeted greenfield (§ 8.1 disposition 1) — rocket seam, separate dispatch.
- Retiring the simplified model's CODE path — it stays alive as the Phase 1 oracle through transition; physical removal is a later step, not this dispatch.

## Gate-2 at close
**jack-ryan (DEV-MODE, Gate-2, BLOCK authority)** reviews the completed math-note + implementation + golden-master verification + telemetry tag as one unit. Submit to `agentic_orchestration/qa/pending/`. Gate-2 PASS is acceptance. As the protocol's proving run, jack-ryan also assesses whether the worked reference (corpus fix, predicted-delta convention, re-gate model) is reusable as the template for subsequent § 3 applications.

## Completion record

**Status:** Phases 0/1/2 COMPLETE + committed (engine repo). Phase 3/4 GATED on Gate-2 approval of the math-note (Discipline #1 + dispatch "Phase 3 — per APPROVED math-note only"). Architecture-fit clean — STOP-clause blocker did NOT fire.
**Date:** 2026-06-11
**Author:** gamora

### Phase-by-phase

| Phase | Status | Engine commit |
|---|---|---|
| 0 — Kernel interface declaration (HARD GATE) | DONE, standalone commit | `5f2349f` |
| 1 — Golden-master capture (oracle BEFORE change) | DONE; determinism proven 0/60; 95% WR≥0.9 saturation baseline | `5a7b079` |
| 2 — Math-note (all 6 contents, measured numbers) | DONE; semantic-shift declared | `2e77c28` |
| 3 — Re-point + recalibration implementation | GATED on Gate-2 math-note approval | — |
| 4 — Predicted-delta verify + telemetry tag | follows Phase 3 | — |

### MIGRATION.md
v1.64 written: `simulate_fight(...)->FightResult` (fight_engine.py:107) + `resolve_skill(...)` (damage_resolver.py:278) declared as enforceable wrap boundary. Satisfies Gate-1 Dimension-1 WARN. Star-lord notified the boundary is now formally named (no schema field change; declaration IS the consumable contract).

### Golden master
`scripts/gamora_spatial_golden_master_2026_06_11.py` (capture/verify); oracle `spatial_gauntlet/golden_master/spatial_golden_master_season_001010_2026_06_11.json`. Corpus: 10 season_001010 classes × 6 ArenaScenario types = 60 cells; N=10 fights/cell; seed 770011. Self-verify: 0/60 moved (exit 0) — bit-stable. Baseline: 57/60 cells (95%) WR≥0.9 — the saturation symptom.

### Math-note headline numbers (`simulation/math/spatial-repoint-recalibration-2026-06-11.md`)
- **Predicted-delta (season_001010 corpus):** WR moves DOWN / surface de-saturates / per-fight variance widens / clears slow. Mechanism: simplified flat `dmg_mult×500` (1050–7250 spatial per-hit) one-/two-shots mobs (HP ~2019→3028) → WR=1.0; resolver adds armor/resistance mitigation + attribute scaling + ±15% per-hit variance + effects-differentiation. Geometry-hit counts predicted UNCHANGED (negative contract).
- **T4 flips predicted SEPARATELY (corpus is pre-T4 — load-bearing):** chaos_immune shadow→0 flips + three-path damage_scaling_type re-ordering require a T4-bearing golden-master follow-on; NOT verifiable in this proving run.
- **Recalibration:** SPATIAL_DAMAGE_SCALE swept ALONE first (Disc #24), MOB_HP_DIFFICULTY_MULTIPLIER second only if needed. Target shape: per-scenario WR spread ≥0.4; saturation ≤50%; floor ≤30%. Form `SDS_new ≈ 4.0 / r_effective`; VALUE measured at Phase-3 sweep.
- **Re-gate bound (GATES production sweeps):** `SpatialCost = N·C_s·(1 + F·g)`; F≤0.30, g≤2 ASSUMED → multiplier ≤1.6 → hybrid ≤1.6× filter. F,g MEASURED before any production sweep.
- **Cost-profile re-check:** per-fight predicted <2×; re-measure trigger pulled iff measured >1.5× (>8.7 ms warm).
- **PC 12× factor:** SEPARABLE sub-task; remains ASSUMED; combined Mac+PC number NOT banked (BANNED per contract § 8.2.2); flagged to KR behind the manifestation spike wave.

### Architecture-fit resolution (the STOP-clause assessment)
Production caller `balance_loop._run_spatial_slot:2625` already holds full `PlayerClass`/`Monster` objects (`model_dump()`'d DOWN to dicts only to feed the simplified model's dict interface). The resolver-ready objects are present at the call boundary → **the resolver CAN serve spatial's call pattern without kernel modification.** The STOP-clause named blocker does NOT fire. The export-JSON path is lossy (strict Pydantic fields absent) but is NOT the production path. Phase 3 is a clean caller-side change (adapter + `_apply_skill_damage` rewrite), bounded but multi-day (the adapter requires threading PlayerClass/Monster through `entity_from_class_dict`/`entity_from_monster_dict`, which currently take only dicts — a signature change across `run_spatial_fight` + `_run_spatial_slot` + `gauntlet_modes` + the golden-master harness).

### Star-lord flag
FIRED (notification only, no schema change yet): the `simulate_fight(...)->FightResult` boundary is now formally named in MIGRATION.md v1.64; star-lord's telemetry + the parallel runner consume through it. NO new fight_log/SpatialFightResult key added in Phase 0–2. Principle-6 watch carried into Phase 3: `resolve_skill` returns `(damage, events)` — the `events` list (e.g. `on_chaos_immune`) is NEW info; default for this proving run is to DROP events (parity with simplified model's information content). If a future change carries events into telemetry, that IS a cross-seam change → MIGRATION.md + star-lord notification before tagging.

### Notes for jack-ryan (Gate-2)
- Submitted unit for Gate-2: the math-note (Phase 0/1/2 artifacts) — Phase 3 implementation locks values against the approved predicted-delta contract.
- Semantic-shift declared (Disc #12): spatial WR is no longer the same quantity post-re-point → decisions-log entry requested (R-series recalibration lineage continues).
- Proving-run template assessment requested: corpus fix (60 cells, seed-pinned, committed oracle, self-verify determinism), predicted-delta convention (direction = contract, magnitude = recalibrated, negative non-movement contract, exit-1=predicted-or-STOP), and re-gate bound model are offered as the reusable template for subsequent § 3 applications (id-substrate rebuild next).
