# Dispatch — 2026-07-06 — star-lord — batch-2 Leg B FIRE: economy pilot (gamora read)

**From:** knight-rider
**To:** star-lord (fire) · gamora (read/report)
**Approved by:** Matt 2026-07-06 (batch-2 auth) — **ADR-002 cross-seam-schema sign-off SIGNED 2026-07-06** (`resource_economy` generation→sim contract approved). GATE CLEARED — cleared to fire.
**Estimated effort:** fire minutes-to-tens-of-minutes class (variation pilot precedent: 50 kits ≈ 903s full gauntlet); report ~1–2h
**Acceptance:** the economy pilot runs on the PRODUCTION path across 2–3 coverage-sampled cells, per-cohort bucket keys live, measurement report emits (no demo-bundle coupling), and gamora reports the pre-registered GO/HALT verdict + the economy-identity read.

## Context

Leg-B build is Gate-2 PASS-WITH-FOLLOWUPS: the `resource_economy` field (Route B) is wired and the binding is CONFIRMED (C4 default corner reproduces 0.0 KPM on both shells; C3 a favorable corner moves KPM off the floor). This dispatch FIRES the economy pilot the build enables — the pre-registered GO/HALT test of whether economy space contains a floor-clearing region at all (spec §3). This is the gate for the full Leg-C fire.

**CRITICAL instrument fact (Gate-2 verified):** the economy bites ONLY on the PRODUCTION (bounded-pool) path — `from_player_class` → bounded pool. The projection/harness path pins `mana=1e9` and CANNOT starve (`spatial_resolver_adapter.py:192`). **The pilot MUST fire through the production path or the whole sweep is inert.**

## Required reading before starting
- `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` §3 (the pilot spec — cells, sampling, instrumentation, PRE-REGISTERED GO/HALT) + §8 D2/D4/D5.
- `agentic_orchestration/batch2-run-state-2026-07-06.md` — full Gate-1/Gate-2 state, the frozen contract, the instrument fact.
- `simulation/notes/legB-economy-consume-math-2026-07-06.md` (gamora) — how the economy binds + the production-path fact.
- `generation/resource_economy.py` — `sample_resource_economy(cell_base_seed, samples_per_stratum=4)` (the LHS-within-6-strata sampler you request per cell).
- `agentic_orchestration/qa/pending/2026-07-06-legB-economy-build-gate2-jackryan.md` — Gate-2 followups (esp. FU-2).
- `export/measurement_report_writer.py` + `MIGRATION.md §v2.10` — the measurement-report path (no demo-bundle coupling).
- The variation-pilot precedent: `variation-pilot-run-state-2026-07-06.md` (the detached-run + measurement-report pattern; Discipline #19).

## Scope
- [ ] **Cells (2–3, spanning the INT space, spec §3):** 1 **plain-caster** (proxy ~0 — the floor test) · 1 **summoner** (proxy ≥0.25 — the C2 band-2 certification) · optionally 1 hybrid/mid cell IFF marginal cost ~zero at config time (§8 D2 — your + gamora call, documented).
- [ ] **Sampling:** ~24–25/cell via `sample_resource_economy` (LHS-within-6-strata, Gate-1 ratified) — coverage across the axis ranges, NEVER clustered at a point.
- [ ] **Production path only** — assert the run threads `from_player_class` / bounded pool. A projection/harness-path fire is a HARD FAIL of this dispatch.
- [ ] **FU-2 (Gate-2):** `assert WIRE_RESOURCE_ECONOMY is True` on the PILOT run path (not just the build smoke) — inert sweep must be impossible to fire silently.
- [ ] **Per-cohort bucket keys LIVE (first use)** — proxy cohorts measure separately (fixes the empty caster_proxy class of miss); economy identity must NOT collapse into shared buckets.
- [ ] **Measurement report** via `measurement_report_writer.py` — zero demo-bundle coupling, valid with zero monsters/gear.
- [ ] **Run discipline:** SEQUENTIAL in ONE registered run (§8 D5), seed+SHA+config reproducibility. Detached OS-process per Discipline #19 if the run exceeds a few minutes; canonical-JSON checkpoint before the gauntlet.
- [ ] **gamora reads/reports** the pre-registered GO/HALT + the economy-identity read (§3, and gandalf G2: report in Axis-5 identity terms — "generator-spender cleared" — not lever-coordinates).

## PRE-REGISTERED GO/HALT (registered at spec §3 — do NOT move the goalposts)
- **GO** = (i) ≥1 **CONTIGUOUS** region of economy space in the plain-caster cell clears **bar_lo solo on BOTH shells** (9.90 KPM open_arena AND 11.65 KPM chokepoint), AND (ii) summoner-band certification executes with per-cohort measurement intact (kit+proxy composite scored; solo timeout non-disqualifying per C2).
- **HALT** = zero economy configs clear → **escalates to Matt with the MEASURED LANDSCAPE** (the finding: caster viability is blocked below the economy layer; deeper structural work precedes any 18-roster fire). HALT is a designed outcome, NOT a failure.
- **Default-corner regression inside the run:** the default corner must still read 0.0 KPM (the C4 anchor) — a built-in sanity check that the sweep is live.

## Cross-seam contract change? (Principle 6 gate)
**NO new contract in this dispatch** — the `resource_economy` contract landed + passed Gate-2 in the B-build. This is a FIRE + MEASURE run consuming it. `Round-trip: not applicable — no contract field added; this dispatch exercises the already-Gate-2-verified contract on the production path.`

## Out of scope (explicit non-goals)
- **NO Leg-C fire, NO full 18-roster emission** — that gates on this pilot's GO + Matt's Axis-5 ruling + the C1 vocab fix.
- **NO band re-tune, NO re-emit of pilot/pre-axes kits** (provenance law §5 — only the eventual Leg-C population votes in the derivation).
- **NO structural-bin economies** (the 3 unreachable Axis-5 bins).
- **NO goalpost-moving** on the pre-registered GO/HALT — the criteria are frozen at spec §3.

## Open questions for the agents to resolve (document your answers)
- Third (hybrid/mid) cell: include or not, per §8 D2 marginal-cost test.
- Detached vs in-session: pick per Discipline #19 based on the measured run time (checkpoint first either way).
- Candidate-budget output shape for Leg C (viable-region bounds → per-cell budgets) — how gamora hands it forward.

## References
- Spec `batch2-build-spec-2026-07-06.md` §3/§5/§8; run-state `batch2-run-state-2026-07-06.md`
- Build tags: `rocket/v-batch2-legB-economy-emit-1` (`9eca04c`), `gamora/v-batch2-legB-economy-consume-1` (`7e1a5d1`); Gate-2 `77e634b`
- Discipline #19 (detached run), #8 (bundle/report validation), #24 (per-cohort measurement), C2 band criteria (Matt 2026-07-02/07-06)

---

## Completion record

**star-lord — 2026-07-06/07**

### Run executed — COMPLETE

**Run ID:** `617409b8-3508-4a4f-a307-107c6f564246`
**Seed base:** `62_000_000` (disjoint from T4 +500, role-split +900k, variation-pilot 60M/61M blocks)
**Wall time:** 101.3 s — run was DETACHED (nohup OS-process per Discipline #19); process PID 31410 exited 0

### Cells fired

| Cell label | Cell ID | Proxy density | N configs | Shell MOB HP (GO/HALT shells) |
|---|---|---|---|---|
| plain_caster | endgame_bc_ranged_medium_variable_int_none | none | 25 | 300k open_arena / 500k chokepoint (dmod=0.3) |
| summoner | endgame_bc_ranged_medium_variable_int_none | light | 25 | 300k open_arena / 500k chokepoint (dmod=0.3) |

**D2 decision (third cell):** EXCLUDED. Marginal cost is NOT ~zero at config time — requires a different BC cell ID; non-trivial config cost. Two INT cells span the critical space. Documented in `run_config.d2_decision`.

### FU-2 assertion (Gate-2 carry-forward)

`assert WIRE_RESOURCE_ECONOMY is True` — PASS. Written on the PILOT run path (not just the build smoke). An OFF flag now fails loudly before any sweep starts.

### Production path confirmation

Run threads `from_player_class` → bounded pool via `combatant_from_player_class`. Economy bites on the bounded pool. Confirmed live: `run_config.production_path = "from_player_class → bounded_pool (economy bites here)"`. Projection/harness path (`mana=1e9`) NOT used.

### Default-corner sanity (C4 — HARD CHECKED ASSERTION)

| Shell | Default KPM | Bar lo | Result |
|---|---|---|---|
| open_arena | 0.0 | 9.90 | PASS |
| chokepoint_corridor | 0.0 | 11.65 | PASS |

Assertion fires in driver; exit != 0 on failure. PASS — C4 anchor confirmed.

### Measurement report

**Path:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/economy_pilot/economy_pilot_measurement_report.json`
**Schema:** `economy-pilot-v1` — no demo-bundle coupling; valid with zero monsters/gear.
**Checkpoint (pre-gauntlet):** `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/economy_pilot/economy_pilot_checkpoint.json`

### Registry

Registered in run registry (ADR-006, authorized per Matt batch-2 authorization).

### Engine commits

- `bfb6097` — `economy_pilot_driver.py` (Batch-2 Leg B FIRE driver)
- `3a09a4d` — economy pilot run artifacts (checkpoint + measurement report)

### Measured landscape (for gamora read — do NOT interpret GO/HALT here)

Per the pre-registered criteria (spec §3), the measured landscape is:
- **plain_caster cell, open_arena:** max KPM across 25 configs = 1.0 (bar lo = 9.90). 0/25 configs clear.
- **plain_caster cell, chokepoint_corridor:** max KPM across 25 configs = 2.1 (bar lo = 11.65). 0/25 configs clear.
- **n_configs_clearing_both (both single-target shells):** 0

GO/HALT verdict is gamora's read. Report path handed off above.

<!-- gamora appends verdict below -->
