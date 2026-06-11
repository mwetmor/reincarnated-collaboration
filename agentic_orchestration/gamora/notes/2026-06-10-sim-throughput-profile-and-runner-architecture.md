# Battle-Sim Throughput Profile + Runner Architecture for ~400 Balanced Kits

**STATUS:** CURRENT — Pattern A-deep verdict (Fable-5 consult); empirical profile measured 2026-06-10
**Author:** gamora (simulation + spirit-guide seam)
**Commission:** `agentic_orchestration/gandalf/notes/2026-06-10-gamora-fable5-sim-throughput-consult-commission.md` (gandalf, commit `84ecaca`)
**Harness:** `reincarnated-engine/scripts/gamora_throughput_profile_2026_06_10.py` (committed; reproducible)
**Raw artifacts:** `reincarnated-engine/output/throughput-profile-2026-06-10/` (report JSON + cProfile dumps)
**Host measured:** Mac Mini, Apple M2 (4P+4E, 8 cores), 8 GB RAM, macOS 15.6.1, Python 3.12.0

---

## 0. Disciplines declared (per commission § Required discipline)

1. **Empirical-evidence-first (Discipline #11):** every load-bearing number below was produced by running the production sim path on this host during this session, or extracted from production telemetry JSONs written by prior production runs. Measured-vs-assumed is marked on every number; the scaffold register is § 8.
2. **Resolver math preserved (crown jewel):** nothing here touches resolver math. The recommendation is a runner-layer design; the resolver-port question is answered NO (§ 6).
3. **Discipline #18 (math hotspot):** the surrogate-filter methodology (§ 5.3) is treated as a math-hotspot decision — the surrogate is the *existing, already-validated* two-tier T1 quick-estimate, used for search-ordering only, with bands identical to full-sim bands.
4. **Surrogate-for-search / full-fidelity-for-commit:** baked in as a hard gate (§ 5.3, § 5.6). The final 400 ship only through the full 18-encounter × 4-cohort × T2 gauntlet.
5. **Recognition-validate-commit (Discipline #40):** scaffold register at § 8, including one **stale in-code scaffold that this profile empirically falsifies** (§ 1.4).

---

## 1. Empirical profile (core deliverable)

### 1.1 Headline table — all MEASURED unless marked

| Quantity | Value | Provenance |
|---|---|---|
| Cost per fight (boss encounter, real Season-001 kit) | **3.24 ms** mean (range 0.39–6.11 across kit × encounter) | MEASURED (498 timed fights, micro-bench) |
| Cost per fight (production gauntlet mix, amortized) | **0.54 ms** | MEASURED (81,320 fights / 43.6 s) |
| deepcopy of combatant pair (per-fight entry cost) | 0.29 ms (~9% of a boss fight) | MEASURED (500 reps) |
| Fights per full-fidelity kit validation | **1,506** actual (2,160 theoretical max; T1 REJECT short-circuits ~30%) | MEASURED (81,320 / 54 kits) |
| **Wall-clock per kit (full 18-enc × 4-cohort gauntlet)** | **0.81 s** | MEASURED (54 kits in 43.6 s) |
| Single-process gauntlet throughput | 1,864 fights/s | MEASURED |
| 8-worker aggregate throughput (multiprocess) | 4.49× single = ~8,370 fights/s gauntlet-mix | MEASURED scaling × measured base |
| Population-level calibration cost (binary-search convergence) | 17 gauntlet calls ≈ 185 s for an 18-kit reference population | MEASURED (rerun-4 telemetry JSON, `total_gauntlet_calls=17`, `wall_time_s≈185`) |
| Convergence iterations (population calibration) | 8–12 expected per math note; 17 observed incl. profile sweeps | MEASURED (telemetry) / math-note expectation |
| **Projected: 4,000 kit-variants, sequential, current setup, full fidelity** | **~54 minutes** (4,000 × 0.81 s) + ~3–15 min fixed calibration | PROJECTED from measured per-kit cost |

Cross-check against independent production telemetry (not produced by this session): 12 prior production gauntlet runs in `cycle-14-wave-5-season-001/` show 103,960–112,520 fights in 46.5–55.4 s (66 kits, ~0.75 s/kit) — consistent with this session's fresh measurement to within 10%.

### 1.2 The 3-day figure is refuted

**Measured sequential wall-clock for ~4,000 kit-variants is ~1 hour, not 3 days — the back-of-envelope was off by ~70×.** The iteration loop is not dead; it is not even strained at current scale. With the runner architecture in § 5 it drops to ~12 minutes.

### 1.3 Where the time goes (decomposition, % of total fight cost)

cProfile over 300 boss fights (25.9M function calls; relative shares are the signal — profiler inflates absolute time ~5×):

| Component | Share | Notes |
|---|---|---|
| **Pure-Python tick-loop bookkeeping** (`_maybe_act`, `can_use_skill`, `_tick_resources`, `_tick_cooldowns`, status predicates `is_silenced`/`is_rooted`/`is_ready`, `_update_distance`, builtins `max`/`min`/`any`/`dict.get`) | **~85%** | ~2,400 tick-function invocations per fight (≈1,200 ticks × 2 combatants); each tick does tiny scalar work — cost is interpreter overhead, not math |
| `copy.deepcopy` of both combatants at fight entry | ~8% | 477,000 deepcopy calls / 300 fights |
| `damage_resolver.resolve_skill` (the actual damage math) | **~4%** | 17,054 calls / 300 fights |
| Everything else (auto-attack, effects, potions) | ~3% | |
| **LLM API calls** | **0%** | § 2 — none exist in the loop |
| **I/O / serialization** | **~0% in-loop; ≈2–7 s once per gauntlet run** | single JSON write at gauntlet end; kit-load ~1.0 s once per process |
| DB access in hot loop | 0% | none; gauntlet path touches no DB |

**Interpretation:** the sim is 100% CPU-bound pure-Python, embarrassingly parallel, with the cost in the tick loop's interpreter overhead — *not* in the resolver math, not in I/O, not in any external service.

### 1.4 Empirical falsification of an in-code scaffold (Discipline #40 case)

`gauntlet_sim.py:1328` projects wall-clock at **0.34 s/fight**; measured production cost is **0.54 ms/fight — the scaffold is stale by ~630×**. Consequences observed live during this profile: a 44-second run logged `WARNING ... 116640 fights exceeds max 104000 (flag: >10 hrs wall-clock)`. `GAUNTLET_COMPUTE_BUDGET_MAX_FIGHTS = 104_000` is calibrated to the same stale constant. **This stale scaffold is the most plausible origin of the 3-day fear** (116,640 fights × 0.34 s ≈ 11 hrs/sweep; multiplied by calibration iterations ≈ days). Recommended within-seam follow-up (ADR-002 tier): re-anchor the constant to measured 0.54 ms/fight (with margin), retire or recalibrate the budget warning. Flagged for jack-ryan visibility since the false WARNING actively misleads operators.

---

## 2. LLM-in-loop audit — RULED OUT

**There is no LLM call anywhere in the balance hot loop.** Verified by grep across the full call graph of the gauntlet/calibration path (`fight_engine`, `damage_resolver`, `combatant`, `effect_resolver`, `trigger_handler`, `resistance_matrix`, `batch_runner`, `t4_sim_cycling`, `gauntlet_sim`, `unified_calibration_loop`, `season_generation_pipeline`): zero matches for LLM/Anthropic/OpenAI/HTTP clients.

LLM calls exist in exactly one seasonal phase: **Phase 5 cohesion-judge** (`wave5_season_orchestrator.py` § 10 — faction clusters, season naming, per-kit identity). That phase is:
- **downstream of balance** (consumes balance output; never inside any convergence or validation loop),
- suppressed entirely in smoke mode,
- cost-capped in code (`DEGENERACY_MAX_LLM_COST_USD = 0.60`).

Phase 5 scaling for 400 kits is a *cost* question (per-kit identity calls × 400), not a balance-throughput question — out of scope here, but flagged to star-lord/KR as the only LLM-scaling surface in the season pipeline.

**LLM latency × 4,000 × iterations = 0. The prime 3-day-killer candidate does not exist.**

## 3. Parallelizability — CONFIRMED O(n)

- **Algorithm class:** each kit is validated against a **fixed 18-encounter catalog** (kit-vs-gauntlet). No kit-vs-kit matchup matrix exists anywhere in the seasonal balance path (audited `gauntlet_sim`, `t4_sim_cycling`, `wave5_season_orchestrator`, `balance_loop`). The legacy B14.5 doppelganger gate is kit-vs-own-clone — also O(n). Solo/PvE holds. **No loud flag needed: the algorithm class is O(n).**
- **Fight independence:** every fight is seeded independently (`simulate_fight(seed=...)`, deterministic per seed, deep-copies inputs, mutates nothing shared). Kit-level work units share zero state; results merge by concatenation.
- **Measured parallel scaling (this host):** 1 worker = 466 fights/s (boss-only probe); 2 = 1.81×; 4 = 3.44×; 8 = **4.49×**. The sub-linear tail is the M2's 4P+4E core asymmetry, not coordination cost. Speedup ceiling on this host ≈ 4.5×; on a symmetric many-core box it should approach core count.
- **Overhead costs (measured):** process-pool spawn ~0.5–1.1 s per pool; per-worker one-time kit/import load ~1–2 s — amortized to noise when each worker handles dozens of kits. Discipline #3 (no parallel regens of same seed) is satisfied by partitioning *kits* across workers; no two workers ever run the same (kit, seed) cell.

## 4. Pushback on the commission framing (seam authority)

The framing modeled per-kit cost as ~65 s with a convergence-from-cold loop per kit. The actual current architecture differs in gamora's favor:

1. **Calibration is population-level, not per-kit.** The unified calibration loop binary-searches a *global* scale factor against a reference population's median boss KPM (8–12 iterations expected; 17 gauntlet calls measured including sweeps). Its cost is **fixed (~3–15 min) and does not scale with 4,000 variants** — calibration uses a reference subset, not the full variant population.
2. **Per-variant cost is one validation gauntlet: 0.81 s**, with the T1 quick-estimate already short-circuiting ~30% of fights.
3. The only path where per-kit iteration loops appear is the **Track 2 / Option A per-kit calibration forward-link (Matt D3, deferred)**. Worst case there: 12 full-gauntlet iterations × 0.81 s ≈ 10 s/kit → 10.8 hr sequential for 4,000. That is the scenario the runner architecture below is sized to kill (§ 5.5: reference-cell iteration + warm-start → back to ~1.3 s/kit).

## 5. Recommended runner architecture

Design principle: the resolver and gauntlet are healthy; **build a thin parallel batch-runner around them, change nothing inside them.**

### 5.1 Parallelism — local multiprocess; no cloud
`multiprocessing.Pool` (spawn) over **kit-partitions**: each worker receives a contiguous slice of kit-configs, runs the existing `run_gauntlet_sim` path unmodified, writes a per-worker shard JSON; a merge step concatenates shards into the standard quality-report schema (star-lord schema untouched — merge produces the same artifact shape; if shard artifacts are to persist, that needs a MIGRATION.md entry first).
- 8 workers on the M2 ⇒ measured 4.49× ⇒ **4,000 full-fidelity validations ≈ 12 min**.
- **On-demand cloud cluster: NOT recommended.** At 12 min/sweep there is no problem for a cluster to solve; cloud adds artifact-shipping, environment-skew, and seed-discipline risks for negative ROI at this scale. Revisit only if variant count grows ≥100× beyond 4,000. (The PC's i7-14700F 20c/28t is the natural overflow host before any cloud — ASSUMED ~3–4× Mac throughput, unmeasured.)

### 5.2 Seed discipline under parallelism
Preserve the existing seed-namespace arithmetic (`base + config_idx·100_000 + cohort_idx·10_000 + enc_idx`) — it is partition-invariant as long as workers receive *global* config indices, not per-shard indices. The runner must pass the global index into each shard. This keeps any parallel run bit-identical to the sequential run (verifiable: shard-merge output == sequential output for the same population; make that equality check the runner's smoke test).

### 5.3 Surrogate filter — use the existing T1 tier; hard full-fidelity gate (math hotspot — Discipline #18)
- **Surrogate = the already-validated T1 quick-estimate** (10 fights/cell, identical bands to T2 routing). T1-only sweep over a kit ≈ 0.31 s/kit (measured: 30,780 T1 fights / 54 kits). No new surrogate math is introduced — this matters: a novel regression/analytic surrogate would itself be a math-hotspot requiring methodology consultation; the T1 tier is already canon (B14.5 V1 adaptive quick-estimate lineage).
- Search flow: **T1-prune the 4,000 → survivors get T2 → the final 400 ALWAYS run the complete 18×4×(T1+T2) full-fidelity gauntlet before ship.** The full-fidelity gate is structural in the runner (the ship-manifest is emitted *only* from full-gauntlet quality reports; T1-only results are physically unable to reach the manifest — different artifact type).
- **Guardrail (non-negotiable, per commission):** surrogate results never become source-of-truth. T1 numbers route; they do not ship. This is bit-for-bit how production already behaves; the runner preserves it.

### 5.4 Warm-start from archetype baselines
Under the 40-archetypes × 10-variants structure, variants of one archetype share a converged neighborhood. Concretely: when Track 2 per-kit calibration fires, initialize each variant's binary search at the **archetype baseline's converged scale factor** with a narrow initial bracket (±10–15%), instead of cold full-range. Expected iteration count drops from 8–12 to ~2–4 (ASSUMED — must be validated empirically on the first archetype family before being relied on; cheap to measure: one archetype × 10 variants ≈ seconds).

### 5.5 Variation axes as deltas — use for ORDERING, never for COMMIT
Element swap / T4 reversal / racial trait / experience mix all pass through nonlinear routing (resistance matrix, T4 condition checks), so an analytic delta-model is *not* trustworthy as a balance verdict. But it doesn't need to be: **at 0.3–0.8 s per real sim, the correct delta model is the simulator itself.** Recommendation: use crude delta heuristics only to *order* variant exploration (which variants to try first), and warm-start (§ 5.4) to make each variant's convergence cheap. Do not build a delta-prediction layer that bypasses sims — the throughput numbers remove its justification, and it would create exactly the surrogate-becomes-source-of-truth failure the commission forbids.
- Additionally, when per-kit calibration iterates, each iteration should run the **reference cell only** (boss_with_adds × reference cohort, ~30–60 fights ≈ 0.02–0.04 s) — the calibration objective reads only median boss KPM — with the full gauntlet run once at convergence. Per-kit cost under full Track 2: ~0.5 s calibration + 0.81 s final gauntlet ≈ **1.3 s/kit**.

### 5.6 Runner pipeline (end-to-end shape)

```
4,000 variants
  → [parallel T1 surrogate sweep]          ~0.31 s/kit ÷ 4.49  ≈  5 min
  → survivors (assume ~40–60%)             T2 + warm-start calibration
  → [parallel full pipeline on survivors]  ~1.3 s/kit ÷ 4.49   ≈  10–13 min
  → candidate 400 selected
  → [FULL-FIDELITY GATE: complete gauntlet, all 4 cohorts, 18 encounters]
                                            400 × 0.81 s ÷ 4.49 ≈  1.2 min
  → ship manifest emitted ONLY from full-gauntlet quality reports
```

## 6. Resolver-port assessment — **NO. Do not port; leave the resolver alone.**

After parallelism (the only architecture change needed) and de-LLM-ing (nothing to de-LLM), raw per-fight Python cost is **not the wall**: the entire 4,000-variant sweep is ~12 minutes. A numpy-batch/numba/compiled port could plausibly buy 10–50× on the tick loop (~85% of fight cost is interpreter overhead), but:
- the project's iteration metabolism is already healthy at minutes-scale;
- the resolver + fight engine are the single most empirically validated asset in the engine; a same-math port still carries regression risk across thousands of seed-dependent branches (variance streams, jitter, distance bands, trigger ordering) for zero felt benefit;
- engineering time is better spent on the thin parallel runner (§ 5.1), which is ~a day of work and risk-free to the math.

**Re-open criterion (empirical, not time-based):** if variant count grows ≥100× (≥400K sims/sweep) or the resolver moves in-game/server-side per-request, port via numba/numpy-batch with the **old resolver as oracle**: identical seeds, assert per-fight equality on termination_reason + KPM within float tolerance across a ≥100K-fight corpus spanning all encounter types × archetypes, plus distribution-level KS tests on duration/KPM. That plan is documented here so it exists; it is not recommended now.

## 7. Bearing on the battle-sim greenfield decision (load-bearing flag)

**Throughput provides NO justification for a greenfield sim rebuild.** The measured engine does ~1,900 full-fidelity fights/s single-process on a laptop-class core. The sim layer should be **wrapped (thin parallel runner), not rebuilt.** If the greenfield case is argued, it must be argued on other grounds (e.g., feature architecture, UE-side integration) — the 3-day throughput fear is empirically dead, and its likely origin is a stale in-code cost scaffold (§ 1.4). For the generation↔sim forward-architecture contract: the sim side can commit to a contract of **"~1 s per kit-variant full validation; ~12 min per 4,000-variant sweep on current Mac hardware"** with measured headroom.

## 8. Scaffold register (Discipline #40) — measured vs assumed, every number

| Item | Status |
|---|---|
| 0.54 ms/fight (gauntlet mix), 3.24 ms (boss), 0.81 s/kit, 43.6 s/54 kits, 81,320 fights | **MEASURED** this session (harness in repo; reproducible) |
| 1,864 fights/s single-process; 4.49× at 8 workers | **MEASURED** this session |
| 0.75 s/kit, 46–55 s/66 kits across 12 prior production runs | **MEASURED** (production telemetry JSONs, cycle-14-wave-5-season-001) |
| 17 gauntlet calls / ~185 s population calibration | **MEASURED** (rerun-4 telemetry) |
| 8–12 calibration iterations expected | math-note expectation, partially confirmed (17 observed incl. sweeps) |
| ~54 min sequential / ~12 min parallel for 4,000 variants | **PROJECTED** from measured per-kit cost (linear scaling assumption; justified by O(n) + fight independence) |
| T1-prune survivor rate ~40–60% | **ASSUMED** (depends on variant-generation aggressiveness; does not change the order of magnitude) |
| Warm-start drops iterations 8–12 → 2–4 | **ASSUMED** — validate on first archetype family before relying on it |
| Per-worker memory footprint (~100–200 MB) | **ASSUMED** — fine on 8 GB at 8 workers by observation (no swap during probe), not formally measured (Discipline #1.1 note: measure RSS before any >8-worker config) |
| PC (i7-14700F) ≈ 3–4× Mac throughput | **ASSUMED** — unmeasured; measure before relying on PC as overflow host |
| `gauntlet_sim.py` 0.34 s/fight + 104K-fight budget cap | **STALE SCAFFOLD, EMPIRICALLY FALSIFIED** (§ 1.4) — recommend re-anchor |
| "3 days / 65 s per kit" commission figure | **REFUTED** by measurement (~70× overestimate) |

## 9. Recommended next actions (queued; not executed without authorization)

1. Within-seam (ADR-002): re-anchor `gauntlet_sim.py` compute-budget constants to measured cost; kill the false >10-hr WARNING. Math note + smoke per Disciplines #1/#2.
2. Within-seam: implement the thin parallel kit-partition runner (§ 5.1–5.2) with the sequential-equality smoke test. ~1 day. No resolver changes, no schema changes (shard-merge emits existing artifact shape).
3. First Track-2 family fires: measure warm-start iteration counts on one archetype × 10 variants (validates § 5.4 assumption; seconds of compute).
4. Cross-seam flag to star-lord/KR: Phase 5 LLM per-kit identity calls are the only LLM-scaling surface at 400 kits (cost question, not throughput).

---

**Sign-off:** gamora. The balance loop's metabolism at 4,000 kit-variants is ~12 minutes under the recommended runner, ~54 minutes even with zero changes run sequentially. Dominant cost is pure-Python tick-loop CPU — parallel-friendly, LLM-free, O(n). No resolver port. Wrap, don't rebuild.
