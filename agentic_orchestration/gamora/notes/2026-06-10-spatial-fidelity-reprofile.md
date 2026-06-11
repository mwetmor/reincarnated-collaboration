# Spatial-Fidelity Throughput Re-Profile (Fable-5 consult redirect)

> **STATUS:** CURRENT — companion to `2026-06-10-sim-throughput-profile-and-runner-architecture.md` (supersedes that doc's §1/§6 headline numbers for COMBAT-FIDELITY questions; the runner architecture in §5 stands and is re-validated here)
>
> **Author:** gamora (Fable-5 / claude-opus-4-8) — 2026-06-10
> **Trigger:** Matt correction — Session-1 profile measured the CURRENT fight engine (1-vs-1 duel on a 1-D distance line), not the game's real combat. The older spatial engine ran kits through 2-D multi-actor battle (6 arena scenarios, 3–8 mobs, navigation, soft collision, AOE geometry, flanking). This note re-measures against THAT.
>
> **Scoping (per redirect):** the combinatorial-iteration wrapper that made the old spatial runs explode after ~30 runs is DISREGARDED. This measures the spatial battle cost ITSELF, isolated — projected through the 40-kits × 10-variants ≈ 4,000 strategy, no combinatorial search.

---

## 0. Discipline declaration

Same as the parent deliverable: empirical-evidence-first (every headline number below is from a live run of the surviving spatial engine, executed 2026-06-10, harness committed); resolver math untouched (read-only profiling, `telemetry_writer=None`, no DB writes); Discipline #3 (distinct seed bases per worker; probe, not a regen); Discipline #40 scaffold register at §7; surrogate-for-search / full-fidelity-for-commit guardrail baked into §5.

---

## 1. What survived, and where (deliverable item 1)

**The spatial engine code SURVIVES and still runs.** It is not an "older version" in the git-archaeology sense — it is live in the working tree:

| Artifact | Path | State |
|---|---|---|
| Spatial engine | `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (1,748 lines) | LIVE — imports and runs. 2-D positions, navigation, soft collision, AOE cone/line/circle geometry, flanking, leash logic. `SPATIAL_DAMAGE_SCALE=4.0`, `TICK_SIZE=0.1`, `REDUCED_TICK_SIZE=0.5` |
| Arena scenarios | `src/reincarnated/simulation/spatial_gauntlet/arena.py` — `ALL_SCENARIOS` | LIVE — 6 scenarios: open_arena (8 swarm), chokepoint_corridor (8), boss_with_adds (boss + 2 elite adds), magic_pack (4), elite_pack (3), mini_boss (3) |
| Balance-loop wiring | `balance_loop.py::_run_spatial_slot()` (~line 2584) | LIVE — swarm-tier convergence still routes through `run_spatial_fight()` (W0.9.1) |
| Spatial telemetry | `src/reincarnated/telemetry/telemetry.db` → `spatial_fight_results` | **7,841 fights**, sessions 2026-05-19T10:40 → 2026-05-20T21:51, 51 classes, all 6 scenarios |
| Era-matched kit data | `exports/season_001010/` (`classes.json` 10 converged classes incl. `balance_metadata.final_modifier`; `monsters.json` 44 monsters across all 6 threat tiers) | Generated 2026-05-17 — same era as the telemetry |

**Note on the "5 zones × 5 battle types" framing:** what exists on disk is 6 arena scenarios (zone geometry + battle type fused per scenario). I treated the 6 scenarios as the battle-type axis; no separate 5×5 grid survives in code or telemetry. If a 5×5 matrix existed in an earlier revision, it predates the surviving telemetry.

Because the engine itself survives, I **measured live** rather than inferring from telemetry — and used the telemetry as a fight-length validity cross-check (§2.2).

Harness: `reincarnated-engine/scripts/gamora_spatial_throughput_profile_2026_06_10.py` → report at `output/throughput-profile-2026-06-10/spatial_throughput_profile_report.json`. 60 timed fights per scenario per tick size (3 classes × 20 fights, converged `final_modifier`s), Mac M2 (4P+4E, 8 GB), Python 3.12.

---

## 2. Measured spatial per-fight cost (deliverable item 2)

### 2.1 Direct measurement (full tick 0.1 s, converged kits) — MEASURED

| Scenario | Mobs | ms/fight (mean) | range | sim-elapsed mean | cost per sim-second |
|---|---:|---:|---:|---:|---:|
| open_arena | 8 | 2.07 | 1.3–3.0 | 7.8 s | 0.266 ms |
| chokepoint_corridor | 8 | 1.99 | 1.3–2.4 | 7.0 s | 0.285 ms |
| boss_with_adds | 3 | 13.76 | 3.1–29.7 | 91.5 s | 0.150 ms |
| magic_pack | 4 | 0.59 | 0.3–0.7 | 3.0 s | 0.197 ms |
| elite_pack | 3 | 1.95 | 0.6–3.9 | 16.4 s | 0.119 ms |
| mini_boss | 3 | 9.42 | 1.7–15.9 | 118.1 s | 0.080 ms |

Cost driver confirmed: **wall cost ≈ (cost-per-sim-second, which scales with live entity count) × fight duration**. The 8-mob arenas cost the most per sim-second (~0.27–0.28 ms); boss/mini-boss fights cost the most per FIGHT because they run 90–120 sim-seconds.

### 2.2 The fight-length correction (the honest part)

The converged season_001010 kits **crush every scenario** (WR = 1.0 across nearly all cells; the engine itself logged `[R2 calibration] WR >= 0.95 ceiling` warnings throughout). Short victorious fights → the direct measurement is a **lower bound**. The surviving telemetry records what convergence-era fights actually looked like — 3–14× longer:

| Scenario | Live sim-elapsed | Telemetry mean (n) | Length-normalized ms/fight |
|---|---:|---:|---:|
| open_arena | 7.8 s | 111.3 s (2,180) | **29.6** |
| chokepoint_corridor | 7.0 s | 114.5 s (1,530) | **32.6** |
| boss_with_adds | 91.5 s | 236.2 s (2,181) | **35.5** |
| magic_pack | 3.0 s | 69.6 s (650) | **13.7** |
| elite_pack | 16.4 s | 126.8 s (650) | **15.1** |
| mini_boss | 118.1 s | 227.5 s (650) | **18.2** |

Normalization = measured cost-per-sim-second × telemetry mean fight length. Both factors are MEASURED; the linearity assumption is the scaffold (§7-S3).

### 2.3 Telemetry-mix-weighted per-fight cost — the two operating points

| Operating point | Per-fight cost | Interpretation |
|---|---:|---|
| **WARM** (converged/near-converged kits, measured directly) | **5.79 ms** | What a variant warm-started from its archetype baseline costs |
| **COLD** (convergence-era fight lengths, length-normalized) | **28.37 ms** | What early convergence iterations on off-target kits cost |
| WARM at reduced tick 0.5 s | 1.35 ms | The W0.9.4 surrogate knob — 4.28× cheaper (mix-weighted) |

Real per-kit cost is bracketed by these: early iterations near COLD, late iterations near WARM.

---

## 3. The honest multiplier over the 1-D duel (deliverable item 3)

Session-1 1-D duel baseline (measured): 0.537 ms/fight, 0.81 s/kit gauntlet pass.

| | Per-fight | Per-kit (same gauntlet shape) |
|---|---:|---:|
| **WARM spatial vs 1-D duel** | **10.8×** | 10.8× (8.7 s vs 0.81 s) |
| **COLD spatial vs 1-D duel** | **52.9×** | 52.9× (42.7 s vs 0.81 s) |

Per-kit figures assume the parent deliverable's gauntlet shape carried over: 72 cells × 30 fights = 2,160 max, T1-prune effective ≈ 1,506 fights (§7-S2). Without the prune: 12.5 s WARM / 61.3 s COLD per kit.

**The Session-1 verdict on the 3-day fear is hereby corrected.** At spatial fidelity, COLD, sequential, full-tick, no prune: 4,000 × 61.3 s ≈ **2.8 days** — Matt's ~65 s/kit back-of-envelope was approximately RIGHT *for the real combat*. Session 1 refuted it only because it measured the wrong (1-D) combat. The fear was never stale arithmetic; it was an accurate memory of spatial-engine cost. What kills it is the architecture, not the denial.

---

## 4. Re-projected 4,000-variant wall-clock (deliverable item 4)

All projections use the telemetry encounter mix and prune-effective 1,506 fights/kit unless noted. Mac parallel factor 4.5× is MEASURED (Session 1, 8 workers, M2). PC factor 12× is ASSUMED (§7-S4).

### 4.1 Naive (no architecture) — the baseline fear, quantified

| Mode | Sequential | Mac 4.5× | PC 12× (ASSUMED) |
|---|---:|---:|---:|
| COLD, full tick, no prune (2,160 f/kit) | **2.84 days** | 15.1 h | 5.7 h |
| COLD, full tick, T1 prune | 1.98 days | 10.6 h | 4.0 h |
| WARM, full tick, T1 prune | 9.7 h | 2.2 h | 0.8 h |

### 4.2 Under the §5 runner architecture (reduced-tick surrogate search on 4,000 + full-tick gate on final 400)

| Mode | Search (seq) | Gate (seq) | **Mac 4.5× total** | **PC 12× total (ASSUMED)** |
|---|---:|---:|---:|---:|
| COLD throughout (conservative) | 11.1 h | 4.8 h | **3.5 h** | **1.3 h** |
| WARM throughout (warm-start working) | 2.3 h | 1.0 h | **0.7 h** | **0.3 h** |

**Headline:** the 4,000-variant spatial sweep lands at **~3.5 h conservative / ~45 min warm-start on the Mac alone**; **~1.3 h / ~20 min on the PC's 20-core box**. **Cloud is NOT needed.** The realistic figure sits between the brackets — early exploration waves run COLD-ish, later refinement waves run WARM as archetype baselines accumulate.

### 4.3 Surrogate stability finding (new, load-bearing for W0.9.4)

The reduced-tick probe surfaced an **A3 stability violation**: mini_boss flipped WR 0.0 → 1.0 for class_0001 between tick 0.1 and 0.5 (and sim-elapsed shifted 118 s → 43 s). 1 of 18 class×scenario cells exceeded the ±0.05 WR-delta guardrail. Consequence: **the reduced-tick surrogate is search-grade only, never commit-grade** — exactly the parent deliverable's guardrail #4, now with an empirical violation in hand proving why. The full-tick gate on the final 400 is non-negotiable.

Also re-confirmed at spatial fidelity: parallel scaling holds (514 → 1,930 fights/s, 1→4 workers, ~3.75×; the 8-worker probe cell degraded only because work units were ~0.06 s and pool overhead dominated — Session 1's 4.49× at 8 workers with realistic work-unit sizes is the operative number). O(n) kit-vs-gauntlet confirmed unchanged — spatial fights are still kit-vs-environment, fully independent across kits.

---

## 5. Greenfield + contract flag updates (deliverable item 5)

1. **Wrap-don't-rebuild verdict HOLDS — and is now stress-tested at true fidelity.** Even at 53× the duel cost, the pure-Python spatial engine delivers 4,000-variant sweeps in single-digit hours under a thin parallel runner. No resolver port (numpy/numba/compiled) is justified: the PC box alone buys more than a port would, at zero math-fidelity risk. Revisit only if the per-sweep requirement drops below ~15 min at COLD lengths.
2. **Sim-side contract number (for the forward-architecture contract):** one spatial kit-variant full-tick gauntlet pass costs **~9 s (warm) to ~43 s (cold)**; a 4,000-variant sweep costs **~0.7–3.5 h (Mac) / ~0.3–1.3 h (PC, assumed)** under the surrogate-search + full-fidelity-gate pipeline.
3. **Combat-fidelity decision is the dominant cost lever — bigger than any runner choice.** 1-D duel vs spatial is 11–53×; tick size is 4.3×; parallelism is 4.5–12×. If the greenfield decision changes WHICH combat the balance loop certifies against, the throughput envelope moves by an order of magnitude. The runner architecture (§5 of parent) absorbs either answer, but the contract must name which fidelity is commit-grade.
4. **Spatial recalibration is required before any production spatial sweep** (flagged, out of scope here): converged season_001010 kits hit WR=1.0 ceilings across the board (engine's own R2-calibration warnings fired ~all cells). `SPATIAL_DAMAGE_SCALE=4.0` / `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` are stale against current kit power. This does not affect the COST profile (cost-per-sim-second is calibration-independent; fight LENGTHS are bracketed via telemetry) but it gates spatial-as-commit-fidelity.

---

## 6. Re-projection summary (the numbers Matt asked for)

| Question | Answer |
|---|---|
| Data found | Spatial engine LIVE in tree (`spatial_gauntlet/`, still wired into balance_loop swarm-tier); 7,841 spatial fights in `src/reincarnated/telemetry/telemetry.db` dated 2026-05-19/20; era-matched kits in `exports/season_001010/` |
| Real spatial per-kit cost | **8.7 s warm / 42.7 s cold** (full tick, T1-prune-effective gauntlet pass; 12.5/61.3 s without prune) |
| Multiplier over 1-D duel | **10.8× warm / 52.9× cold** |
| 4,000-variant wall-clock, naive sequential | **~2–2.8 days — the 3-day fear was REAL for spatial combat** |
| 4,000-variant wall-clock, under §5 architecture | **Mac: 0.7–3.5 h. PC 20-core (assumed): 0.3–1.3 h. Cloud: not needed.** |

---

## 7. Scaffold register (Discipline #40)

| ID | Value | Status |
|---|---|---|
| S1 | All per-fight ms, cost-per-sim-second, tick ratios, parallel scaling, telemetry fight lengths/counts | **MEASURED** (live run 2026-06-10 + telemetry DB query) |
| S2 | Gauntlet shape for spatial per-kit (72 cells × 30 fights; T1 prune → 1,506 effective) | **ASSUMED** — carried from the 1-D gauntlet structure. The spatial-era gauntlet structure was the combinatorial wrapper, disregarded per redirect. If the spatial gauntlet adopts a different cell count, per-kit scales linearly |
| S3 | Cost ∝ sim-duration linearity (used for length normalization) | **ASSUMED, supported** — tick-ratio measurement (4.28× at 5× coarser tick) is consistent with tick-loop dominance; entity-death dynamics make late ticks cheaper, so normalized COLD figures may overstate by up to ~30% |
| S4 | PC i7-14700F effective parallel factor 12× | **ASSUMED** — not yet measured on the PC; Session-1 queued action stands |
| S5 | Telemetry encounter mix as production encounter mix | **MEASURED-as-proxy** — it is the empirical mix of the only surviving spatial production run; future gauntlet design may reweight |
| S6 | WARM/COLD bracket as the per-kit operating range | **DERIVED** — endpoints measured; the realistic mid-point depends on warm-start effectiveness (Session-1 queued validation) |
| S7 | Convergence-iteration multiplier | **OUT OF MODEL** — all figures are per gauntlet pass, consistent with Session-1 framing; population-level calibration amortizes across kits |

---

## 8. Queued next actions (not authorized; named for routing)

1. Measure the PC 20-core parallel factor (replaces S4 assumption) — needs a PC-side run of the harness.
2. Spatial recalibration pass (`SPATIAL_DAMAGE_SCALE` / mob HP vs current kit power) before spatial becomes commit-fidelity — math note first (Discipline #1).
3. A3 stability audit of the reduced-tick surrogate across the full kit population (the mini_boss WR flip says 1/18 cells violate; population rate unknown).
4. Carried from Session 1: re-anchor stale `gauntlet_sim.py:1328` compute constants; implement the thin parallel runner; warm-start validation.
