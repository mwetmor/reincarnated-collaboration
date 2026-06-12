# Gap-Register Architecture-Fit Audit — Simulation Seam (Fable-5 WRAP Refutation Test)

> **STATUS:** CURRENT — read-only architecture-fit audit. No production code modified.
>
> **Author:** gamora (simulation + spirit-guide seam) — 2026-06-11
> **Commission:** gandalf (Matt-authorized this session). Refutation test on the unmeasured axis: the 2026-06-10 WRAP-AND-EXTEND verdict measured throughput/cost; this audit measures **design-architecture divergence** — does implementing the cemented future-state EXTEND the current simulation code or FIGHT it?
> **Verdict basis docs read in full:** `canonical/story/2026-06-10-engine-greenfield-verdict-wrap-and-extend.md`; `canonical/story/2026-06-10-engine-architecture-canonical-synthesis.md` (§ 9 gap register, § 5 damage architecture, § 8 cross-seam contracts); my two 2026-06-10 throughput notes.
> **Code surveyed (read-only):** `src/reincarnated/simulation/` (fight_engine, damage_resolver, combatant, effect_resolver, resistance_matrix, trigger_handler, fight_result, batch_runner, gauntlet_sim, bounded_viability_validation, t4_sim_cycling, spatial_gauntlet/spatial_engine, spatial_gauntlet/arena) + `src/reincarnated/spirit_guide/spirit_guide.py`.
>
> **Honesty clause (per commission):** a refuted WRAP is a valid outcome. I did not set out to defend the verdict. Where the code fights the architecture I say so. Where it cleanly extends I cite the interface.

---

## 0. Instrument

Each item is classified into exactly one of:

- **EXTENDS-CLEANLY** — new code against existing stable interfaces; no resolver/internals change.
- **EXTENDS-WITH-FRICTION** — workable, but requires awkward adapters or a local refactor within the seam.
- **FIGHTS-THE-ARCHITECTURE** — requires working against the grain; rebuilding the module is cheaper than adapting it.

Evidence cites actual file/function/line names.

---

## 1. The kernel-boundary question (item A — the load-bearing one)

**The kernel boundary IS drawable at a named interface today.** The named interface is:

```
fight_engine.simulate_fight(combatant_a: CombatantState,
                            combatant_b: CombatantState,
                            max_duration, seed, ...,
                            enable_cooldown_jitter, enable_damage_variance,
                            enable_fight_damage_variance) -> FightResult
```

(`fight_engine.py:107`). This is a **pure function**: it deep-copies its inputs (`copy.deepcopy` at lines 134-135), mutates nothing shared, is deterministic per `seed`, and returns a `FightResult` value. No telemetry writer, no DB handle, no orchestration state appears anywhere in its signature or body.

**Empirical leakage check (read-only grep across the seven kernel files** — fight_engine, damage_resolver, combatant, effect_resolver, resistance_matrix, trigger_handler, fight_result**):** zero references to `telemetry`/`sqlite`/`.db`/`anthropic`/`openai`/`http`/`writer` as live coupling. The only hits are *comments* (e.g., `damage_resolver.py:227` describing a Discipline #12 semantic shift; `combatant.py:203` noting fields are "carried into fight_log for downstream telemetry audit"). Orchestration state does **not** leak into resolver code — the resolver reads `CombatantState` fields and returns numbers.

**The thin parallel runner already exists in embryo.** `batch_runner.py::run_batch` / `run_batch_geared` are 30-line wrappers that loop `simulate_fight` over `seed = base_seed + i`, appending `FightResult`s. The gauntlet (`gauntlet_sim.py:817-874`) already does partition-invariant seed-namespace arithmetic (`base_seed + config_idx*100_000 + cohort_idx*10_000 + enc_idx`). A `multiprocessing.Pool` over kit-partitions wraps these unchanged — the runner-architecture §5.1/§5.2 design is **new code against an existing stable interface.**

**One honest caveat that does NOT break the boundary, but narrows what "kernel" means:** there are **two damage paths**, not one. (a) The 1-D fight_engine path runs the full `damage_resolver.resolve_skill` armor/resistance/crit chain. (b) The spatial engine (`spatial_gauntlet/spatial_engine.py`, `_apply_skill_damage` ~line 855) explicitly **does NOT reuse `resolve_skill`** — it has its own simplified model `base_damage = damage_multiplier × 500.0 × damage_modifier` (line ~886), documented as "the spatial POSITIONING substrate — fidelity in hits-per-tick, not exact damage numbers." So the read-only KERNEL is cleanly drawable around the **1-D resolver** (`simulate_fight` + `damage_resolver`); the **spatial engine is a second, partially-divergent combat path** whose damage math is a separate, less-validated surface. The forward-architecture contract's "commit = spatial full-tick" decision means the *commit-grade* combat does not currently route through the most-validated kernel — that is a real divergence the contract must name (see § 4 verdict).

**Item A classification: EXTENDS-CLEANLY** (the runner orchestrates the resolver without touching it; boundary drawable at `simulate_fight`). The two-path caveat is logged as a contract flag, not a fight.

---

## 2. Classification table

| Item | Subject | Classification | Evidence |
|---|---|---|---|
| **A** | Surrogate-search + full-fidelity-gate two-stage runner; kernel = read-only resolver library | **EXTENDS-CLEANLY** | `simulate_fight` (fight_engine.py:107) is a pure `(CombatantState, CombatantState, seed)→FightResult` function; deep-copies inputs (L134-135); zero telemetry/DB/LLM coupling in the 7 kernel files (grep-confirmed, comments-only). `batch_runner.py::run_batch` already wraps it with seed arithmetic; gauntlet seed-namespace (gauntlet_sim.py:867-874) is partition-invariant. Runner = new code, no internals touched. |
| **B** | Spatial recalibration (`SPATIAL_DAMAGE_SCALE=4.0` stale) | **EXTENDS-CLEANLY** (parameter-layer) | `SPATIAL_DAMAGE_SCALE` is a module constant (`spatial_engine.py:170`) applied as `spatial_dm = damage_modifier * SPATIAL_DAMAGE_SCALE` at the call boundary (L1629), NOT baked into damage math. Recalibration = new constant value + math-note (Discipline #1) + smoke. No resolver internals. Same for `MOB_HP_DIFFICULTY_MULTIPLIER` (L1649). |
| **C-#3** | Per-level scaling formulas (doc 41 § 4 multi-node calibration) | **EXTENDS-WITH-FRICTION** | Convergence (`balance_loop.py`, `unified_calibration_loop.py`) currently calibrates a scalar/few-dim modifier at a fixed level anchor. Per-level scaling adds a level dimension to the calibration objective — a local refactor of the calibration loop's parameter vector, not the resolver. Workable; the loop is already multi-dimensional (5-6D per convergence-algorithm doc). |
| **C-#4** | W1.13 H1-H5 hypothesis tests | **EXTENDS-CLEANLY** | Hypothesis tests are new probe-harnesses run against the existing resolver (the W1.x lineage already does this; spirit-guide P1 tests W1.20-22 are the same shape). New scripts, read-only against kernel. 🔒 DEFERRED per Disc #18.2 baseline-first — sequencing constraint, not architecture friction. |
| **C-#5** | Playability gate D61 + 8-pattern degenerate-state catalog; multi-T4 sim methodology D84 | **EXTENDS-WITH-FRICTION** | Degeneracy/playability detection already has hooks (`grep` hits in balance_loop, gauntlet_sim, t4_sim_cycling, wave5_season_orchestrator). The 8-pattern catalog + D61 gate is a new evaluation pass consuming existing FightResult/gauntlet output — an additive analyzer. Friction is the catalog formalization + wiring into the gate decision, not a kernel change. D84 multi-T4 sim methodology extends `t4_sim_cycling.py` (which already cycles T4 strategies). |
| **C-#17** | WEAPON_FAMILY_L50_BASELINE fallback-vs-substrate reconciliation | **EXTENDS-CLEANLY** (from sim's view; mostly cross-seam) | `WEAPON_FAMILY_L50_BASELINE` lives in `generation/substrate_weapon_binding.py` (rocket's seam), NOT in simulation/. Sim consumes the resolved baseline as an input field on the combatant. Reconciliation is rocket-side; sim extends cleanly once the input is reconciled. Flagged to rocket, not a sim fight. |
| **C-#20** | C1-C5 vocabulary migration engine-side | **EXTENDS-CLEANLY** (gamora seam authority) | C1-C5 close-criterion vocabulary already present across `bounded_viability_validation.py`, `phase7_db.py`, `phase7_verdict.py`, `unified_calibration_loop.py`, `wave5_season_orchestrator.py`. Migration is a within-seam rename/housekeeping (Cycle 15) — semantic-shift-aware (Discipline #12) but mechanically a vocabulary pass over code I own. No grain-fight. |
| **D** | Hypothesis-flow Stage 4 playtest loop + bounded-viability harness multi-dim (doc 50 5 targets per-encounter-type; doc 51 investment-scaling Patterns 1+2) | **EXTENDS-CLEANLY** | `bounded_viability_validation.py` ALREADY implements doc 50's architecture: `target_1`…`target_5` (`TargetCheckResult`, L172-176), the 108-cell `(kit, encounter_type)` matrix (`CellResult`, L123-140), `cohort_median_kpm` + `ratio`, `KitSpecializationProfile` per-encounter (L195-204). The doc-50 architecture IS the implemented architecture. Stage-4 playtest-validation is a UE-side loop consuming this harness's output — extension layer, no sim refactor. Investment-scaling Patterns 1/2 enter as generation-side metadata the sim reads (no `investment_scaling` symbol in sim today → it's a clean new input field, not a conflicting one). |
| **E** | Two-layer T4 (Primary universal DIRECT_DAMAGE_AMP + Layer-2 strip-and-ship) at sim-consumption | **EXTENDS-CLEANLY** (already implemented) | Already in production: `gauntlet_sim.py:1746` / `:1861-1862` apply Primary T4 `DIRECT_DAMAGE_AMP` always-on via `select_primary_t4()` (imported from `generation.mechanic_alteration`, L1900/1946), with Layer-2 strategies cycling separately in `t4_sim_cycling.py`. This is exactly doc 47 § 4.6 / doc 51 § 10.8.9. The sim already consumes the cemented two-layer architecture; the Cycle-15 DDA retirement (gap-#2) swaps the Primary-slot *content*, not the consumption structure. |
| **F** | A3 violation (reduced-tick surrogate flipped mini-boss WR 0→1, 1/18 cells) → honoring full-fidelity commit-gate | **EXTENDS-CLEANLY** | Honoring the gate is a **new-runner** concern, not a structural change to how sweeps orchestrate. Tick size is already a per-call parameter (`REDUCED_TICK_SIZE=0.5` at `spatial_engine.py:58`; default tick passed by caller, L959/1567). The full-fidelity gate is enforced in the runner pipeline (§5.3-5.6 of my 2026-06-10 note: ship-manifest emits ONLY from full-tick gauntlet reports; surrogate artifacts are a different artifact type that physically cannot reach the manifest). New runner, existing parameterized engine. No grain-fight. |

---

## 3. Count summary

| Classification | Count | Items |
|---|---:|---|
| **EXTENDS-CLEANLY** | **8** | A, B, C-#4, C-#17, C-#20, D, E, F |
| **EXTENDS-WITH-FRICTION** | **2** | C-#3, C-#5 |
| **FIGHTS-THE-ARCHITECTURE** | **0** | — |

(10 audited items: A, B, F, D, E + the 5 C-register sub-entries #3/#4/#5/#17/#20.)

---

## 4. Verdict

### HEADLINE: **WRAP-CONFIRMED** (simulation seam)

**On the design-architecture-divergence axis — the axis the throughput verdict did NOT measure — the simulation code does not fight the cemented future-state. It extends it, and in several load-bearing cases (D, E) it already *is* it.** The bounded-viability harness already implements doc 50's 5-target × 108-cell architecture; the two-layer T4 (doc 47 §4.6) is already the production consumption path; the convergence loop is already the 5-6D multi-dim algorithm the canon specifies. Zero items require working against the grain. The two friction items (per-level scaling, playability-gate-D61) are local additive refactors of code I own, not rebuilds.

**Matt's challenge does not refute on this axis.** His history (greenfield-fast / modify-in-place-costly) is real, but the modify-in-place cost it predicts shows up as FIGHTS-THE-ARCHITECTURE items — and there are none in the simulation seam. The reason: the resolver is a pure function and the future-state architecture (doc 50/51/47) was authored *against the grain of how the harness already measures* (KPM, cohort-median, per-encounter-type, two-layer T4). The architecture and the code co-evolved; they are not in tension.

### KERNEL BOUNDARY: **YES — drawable at a named interface today.**

The interface is `fight_engine.simulate_fight(...) -> FightResult` (pure; deep-copies inputs; zero IO/telemetry/DB/LLM coupling across all 7 kernel files, grep-confirmed). The read-only-kernel contract gandalf is authoring **can be drawn cleanly around the 1-D resolver** (`simulate_fight` + `damage_resolver` + `combatant` + `effect_resolver` + `resistance_matrix` + `trigger_handler` + `fight_result`).

### FIGHTS items: **none.**

### One contract flag for gandalf (NOT a fight — a boundary-precision note)

The kernel boundary is clean around the **1-D resolver**, but the **spatial engine (`spatial_gauntlet/spatial_engine.py`) is a SECOND combat path with its own simplified damage model** (`base_damage = damage_multiplier × 500.0 × damage_modifier`, ~L886) that **deliberately bypasses `damage_resolver.resolve_skill`** (self-documented: "Does not reproduce the full armor/resistance/crit chain"). Since the forward-architecture contract names **spatial full-tick as commit-grade**, the contract should state explicitly: the read-only kernel guarantee covers the 1-D resolver math; the spatial engine's damage path is a *separate, less-validated* surface that either (a) needs its own kernel designation after spatial recalibration (item B), or (b) should be re-pointed at `resolve_skill` if exact damage fidelity becomes commit-required. This is the single unmeasured seam the WRAP verdict glossed — it does not refute WRAP, but it means "the resolver is the read-only kernel" is precise only for the 1-D path today.

---

## 5. Sign-off

**gamora**, 2026-06-11. Audit is read-only; no production code modified. Verdict: **WRAP-CONFIRMED for the simulation seam on the design-divergence axis; kernel boundary drawable at `simulate_fight`; zero FIGHTS items; one spatial-path contract-precision flag for gandalf.** 8 cleanly / 2 friction / 0 fights.
