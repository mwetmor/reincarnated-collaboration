# Finding — 2026-07-08 — spatial-floor-saturation co-diagnosis (gamora G3 + star-lord measure-then-filter)

**Reviewer:** jack-ryan
**Mode:** DEV-MODE (Gate-2)
**Governing dispatch:** `agentic_orchestration/dispatches/2026-07-08-gamora-starlord-spatial-floor-diagnosis.md`
**Developers:** gamora (simulation seam — PRIMARY), star-lord (export/driver seam — secondary)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 6 (cross-seam round-trip), severity-matters
**Disciplines applied:** #1, #2, #11, #24
**Method:** every load-bearing claim verified against SOURCE (submissions not trusted). Both test suites + gamora smoke re-run independently.

---

## SUBMISSION 1 — gamora G3 fail-loud convergence guard

**Tag:** `gamora/v-spatial-fail-loud-convergence-guard-1` · **Commit:** `03076c0`
**Verdict: PASS**

### What I found
`03076c0` adds `SpatialFightConvergenceError` + a three-layer fail-loud guard (Layer A tick-budget, Layer B continuous-spawn catch-up cap, Layer C wall-clock watchdog) to `SpatialFightEngine.run()`, plus fail-loud propagation (log ERROR + re-raise) in `run_spatial_fight`'s batch loop. Files touched: `spatial_engine.py`, `spatial_gauntlet/__init__.py` (export), `_g3_convergence_guard_fire_smoke.py` (smoke), math note. All gamora-owned, within-seam.

### Independent verification (source, not submission)
- **(a) BYTE-NEUTRAL on nominal fights — CONFIRMED.** Spatial regression subset re-run by me: **225 passed, 0 failures** (test_spatial_gauntlet_scenarios + telemetry_v23 + cycle13_wave5_gauntlet_sim + w093/w094/w095 + wd_spatial_bc_measurement). Smoke case D (nominal magic_pack fight) ran clean, guard INERT. The guard checks are top-of-loop early-raise conditions gated on counters that only exceed budget on non-advancement; they cannot alter a terminating fight's outcome. gamora's 312-count is her fuller superset; the 225 I re-ran + the inert smoke case corroborate byte-neutrality.
- **(b) Layers FIRE, do not spin — CONFIRMED.** I re-ran the smoke: **Layer B fired LOUD in 0.001s** (continuous-spawn `interval_s≤0` degenerate → capped at small constant, immediate raise — NOT the naive `max(interval,ε)` ~1e10 mis-bound, which gamora caught during smoke), **Layer C fired LOUD in 0.002s** (wall-clock budget). Both raise `SpatialFightConvergenceError` naming class+scenario; propagation prints `[G3 HALT-LOUD] ... re-raising (batch aborts loud, not silent)`. These are `raise` statements, verified in the diff at spatial_engine.py:2064 (Layer A), :2073 (Layer C), :2126 (Layer B).
- **(c) NO balance-constant moved — CONFIRMED INDEPENDENTLY.** `03076c0 --stat` touches NO `arena.py`. `MOB_HP_DIFFICULTY_MULTIPLIER` still reads **1.5** at `arena.py:49` (current tree). Not in this commit's diff.
- **(d) Math-before-code (Disc #1) — CONFIRMED.** `r2-calibration-fail-loud-convergence-guard-2026-07-08.md` present in the commit, header stamps "Status: authored BEFORE implementation per Discipline #1," §3 specifies the three layers the code implements.
- Layer A correctly reuses the pre-existing `_tick_counter` (defined :2027, incremented at loop bottom :2763) — single source of truth, no parallel counter.

### Rationale
Disc #24 (fail-loud, not silent-wedge) satisfied — converts the v2 29-min silent-alive wedge into an immediate named HALT. Disc #1 + #2 satisfied. Principle 3 (cross-seam impact): none — no boundary field, no export/output/telemetry file touched → correctly NO MIGRATION. This is a reliability guard, not a balance change.

### Action
- [x] Developer: none required — PASS as submitted.
- Root-cause isolation of the specific v2 spawn-cadence interaction (if it recurs) is a correctly-NAMED follow-up, not a blocker.

---

## SUBMISSION 2 — star-lord measure-then-filter

**Tag:** `star-lord/v-batch2-measure-then-filter-1` · **Commit:** `061176c`
**Verdict: PASS**

### What I found
`061176c` adds `_build_section8a1_band_report()` that measures ALL 18 candidates and persists `output/leg3_pilot_section8a1_band_measurement.json` BEFORE the TP3 emission-certification gate, so a 0/18-pass run still yields a diagnostic band report. TP3 unchanged. Files: `w3_emission_driver.py`, `test_w3_emission_driver.py` (Group F, 8 tests), `MIGRATION.md`, `AGENT_STATE.md`.

### Independent verification (source, not submission)
- **(a) THE ORDERING — CONFIRMED, and it is NOT inside a survivors-guard.** Persist at `w3_emission_driver.py:674` (`write_text`), TP3 assert at `:901` (`assert len(survivor_kit_records) > 0`). **674 < 901.** I read lines 650–685: the persist block sits at function-body indentation, unconditional, computed from `all_kits` — NOT wrapped in any `if passing_kits`/survivor conditional. A 0/18-pass run writes the file, then hits TP3 and halts; file is on disk, independently readable.
- **(b) Round-trip 0/18 smoke genuine — CONFIRMED.** `test_zero_passing_round_trip_read_back` (test file :439): builds 18 all-failing kits → persist to disk → read back → asserts `gate_outcome.wr_bracket_passing==0`, `wr_bracket_total==18`, `emission_certified is False`, bands intact, and registry-honesty riders present (NOT-EXERCISED, UNPROVEN, "17 none / 1 light / 0 heavy"). Exercises the exact dispatch-required path (Principle 6).
- **(c) Registry-honesty riders EMBEDDED — CONFIRMED.** `registry_honesty` sub-dict on every report: proxy-heavy NOT-EXERCISED, ≤7 UNPROVEN, C2 light-only, catalog 17/1/0. `test_registry_honesty_fields_present` guards this. No coverage claim beyond that.
- **(d) MIGRATION additive-only — CONFIRMED.** New entry states bundle + run_registry shape unchanged; drax NO change, gamora NO change, jack-ryan additive. New artifact is an analysis JSON in `output/` only. No cross-seam consumer action required.
- **(e) 32/32 driver tests + 0 regression — CONFIRMED INDEPENDENTLY.** I re-ran `tests/test_w3_emission_driver.py`: **32 passed, 0 failures** (~17 min; long due to full integration paths). Pre-existing Groups A–E intact, new Group F (8) all green.
- **TP3 unchanged — CONFIRMED.** The `assert len(survivor_kit_records) > 0` line does not appear in `061176c`'s added/removed lines; only its chronological relationship to the measurement changed.

### Rationale
Principle 6 (cross-seam round-trip) satisfied by the genuine 0/18 persist→read-back test. Principle 3: additive artifact, no schema break, no consumer action. The change corrects the instrument/gate conflation exactly as rider 1 specified — measurement now precedes certification; the certification gate itself is preserved.

### Action
- [x] Developer: none required — PASS as submitted.
- Recovery-mode batch-1-fossil hard-codes (`_RECOVERY_EXPECTED_SURVIVOR_COUNT`) remain a correctly-NAMED out-of-scope follow-up (rider 6), not touched here.

---

## Cross-cutting confirmations
- **Neither commit touches the other's seam.** `03076c0`: no export/output/telemetry file. `061176c`: no simulation/spatial/arena file. Verified via `--name-only`.
- **Neither commit touches the leg-3 wire beyond the certified sequencing.** TP3 assert byte-unchanged; TP1/TP2 machinery untouched; the only wire-adjacent change is star-lord's report-persist-before-gate ordering, which was the sanctioned deliverable.
- **Both critical BLOCK-triggers checked and CLEAR:** star-lord ordering claim (:674<:901) is TRUE; gamora no-constant-moved claim (arena.py:49 = 1.5) is TRUE. No BLOCK on either.

## G1 disposition — explicitly OUT of this Gate-2
gamora's G1 finding (`MOB_HP_DIFFICULTY_MULTIPLIER=1.5` is inherited-uncalibrated relative to the endgame-BC regime; WR=0.000 is a DESIGN FINDING, not a bug) is a **design disposition routed to Matt/gandalf**. No code rides on it in either commit; no constant moved. I do **not** adjudicate the scheduling decision here — it is not part of this Gate-2. Noted for the record only. Design-finding artifact: `agentic_orchestration/gamora/notes/2026-07-08-spatial-floor-saturation-g1-g2-design-finding.md`.

## References
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (guard @ :2027/:2064/:2073/:2126, propagation @ :3476+)
- `src/reincarnated/simulation/spatial_gauntlet/arena.py:49` (MOB_HP_DIFFICULTY_MULTIPLIER = 1.5 — unchanged)
- `src/reincarnated/simulation/math/r2-calibration-fail-loud-convergence-guard-2026-07-08.md`
- `src/reincarnated/export/w3_emission_driver.py` (persist @ :674, TP3 @ :901)
- `tests/test_w3_emission_driver.py` (Group F @ :439+)
- `src/reincarnated/export/MIGRATION.md` (§ MEASURE-THEN-FILTER, 2026-07-08)

## Verdict summary
| Submission | Tag | Verdict |
|---|---|---|
| gamora G3 fail-loud convergence guard | `gamora/v-spatial-fail-loud-convergence-guard-1` | **PASS** |
| star-lord measure-then-filter | `star-lord/v-batch2-measure-then-filter-1` | **PASS** |

No BLOCK. No conditions. Both cleared, moved out of `qa/pending/`.
