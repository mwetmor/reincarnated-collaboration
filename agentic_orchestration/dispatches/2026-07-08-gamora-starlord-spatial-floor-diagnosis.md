# Dispatch — 2026-07-08 — gamora + star-lord — Tier-1 spatial-gauntlet floor-saturation: diagnosis + measure/filter decoupling + fail-loud guard

**From:** knight-rider
**To:** gamora (simulation seam — PRIMARY) + star-lord (export/driver seam — secondary). **Pattern B co-fire** — two seams, own sessions, coordinate via MIGRATION if a boundary field moves.
**Approved by:** Matt 2026-07-07 (via gandalf Lane-C v3-aware verdict — GO on co-diagnosis, gamora PRIMARY / star-lord secondary, 8 binding riders folded below).
**Estimated effort:** gamora medium (diagnosis + fail-loud guard). star-lord small–medium (report/gate decoupling). Multi-session.

## Why this exists (the empirical wall)
The leg-3 Tier-1 $0 dry-run (`dry_run_flavor=True`, seed 56000000, n_samples=1, 18 candidates) was fired three times and never produced §8-A1 band measurements:
- **v2 (`/tmp/leg3_pilot_n1_run.log`):** HUNG in STEP 3/4 live gauntlet — R2 spatial-calibration wedged, log froze 23:15, process sat silent-alive 29 min, vanished 23:44. Unbounded hang, fail-loud violated.
- **v3 (`/tmp/leg3_n1_v3.log`, identical params):** gauntlet COMPLETED (25,530 fights, 1588s) but **WR-bracket season_emit gate = 0 passing / 18 failing**. Zero survivors ⇒ TP3 HALT-LOUD (`survivor_kit_records is EMPTY`) ⇒ no bundle, no bands, $0 spent.
- **Floor-saturation is population-wide:** ~11 of 12 endgame BC classes pin WR=0.000 (≤0.05 floor) in ≥1 scenario (323 floor events vs 278 ceiling). The log's own R2 warning names the trigger+remedy: *"If ≥80% of classes floor-saturate: reduce MOB_HP 1.5→1.25 per L1 authority"* (`MOB_HP_DIFFICULTY_MULTIPLIER=1.5`, `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0`).

**Credit where due (rider 8):** the failure infrastructure WORKED — TP3 refused a degenerate empty bundle, round-trip smoke proved the leg-3 wire (`round_trip_smoke_pass=True`), registry-honesty framing held, $0. **The leg-3 wire is PROVEN. What's broken is upstream of it.** This dispatch does not touch the wire.

## THIS DIAGNOSIS GATES LEG C (rider 3 — critical path, not pilot hygiene)
v3 shows floor-saturation is population-wide, so the full Leg-C summoner campaign hits this same wall. **Nothing Tier-1+ re-fires — pilot OR Leg C — until the calibration state is dispositioned by this dispatch.** Treat as critical path.

---

## gamora — PRIMARY (simulation seam): diagnosis + fail-loud guard

### G1. Disposition the difficulty state (rider 5 — Goodhart guard, the load-bearing question)
Answer, with cited source (decisions-log / R2 calibration notes / your AGENT_STATE): **is `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` a KNOWN-UNCALIBRATED state the leg-3 pilot inherited, or the RULED endgame difficulty?**
- **If inherited-uncalibrated:** the `1.5→1.25` L1-authority reduction is a legitimate calibration fix. Apply per your calibration discipline; it becomes a balance-constant change → **jack-ryan Gate-2**.
- **If 1.5 is the RULED difficulty:** then `WR=0.000` across endgame BC candidates is a **DESIGN FINDING, not a bug** (endgame BC kits can't clear ruled difficulty). REPORT it as such; **do NOT soften the instrument to make the pilot pass** — that is drift (rider 5). Route the design finding to Matt/gandalf.
- Do not skip to the remedy. The disposition GATES whether any constant moves at all.

### G2. Bimodality is a live hypothesis, NOT a defect bucket (rider 4)
`S1_endgame_bc_melee_medium_variable_str_none_s0` reads **open_arena WR=0.000 / chokepoint_corridor WR=1.000**. That is **positional identity** — a melee kit kited to death in open ground that walls a corridor is *design signal*, not a broken class. Your brief must treat "genuinely bimodal class" as a live hypothesis. **A calibrator that demands unimodal per-class convergence fights the kit diversity the engine exists to emit** (Leg-B caster-vindication shape: 11/12 floor-saturating means the *instrument's difficulty state* is the suspect, not 11 broken classes). Characterize how many of the 12 are genuinely bimodal-by-design vs uniformly-floored.

### G3. Convergence-timeout / fail-loud guard on the R2 calibration loop (rider 2 — REQUIRED deliverable, unconditional)
Regardless of G1/G2 outcome: the R2 calibration loop must **fail loud on non-convergence, not wedge silent.** v2 proved the unbounded hang exists; v3's completion on identical params makes it **INTERMITTENT — worse, it will recur unpredictably at Leg-C scale.** v2's 29-min silent-alive wedge is a Disc-#24-shape fail-loud violation. Add a bounded-iteration / wall-clock convergence guard that HALT-LOUDs (with the offending class+scenario named) rather than spinning. This ships regardless of the difficulty disposition.

---

## star-lord — secondary (export/driver seam): MEASURE-THEN-FILTER (rider 1 — the sharpest, cheapest fix)

The pilot **conflated the certification GATE with the measurement INSTRUMENT.** §8-A1 asked for BAND MEASUREMENTS on the population; the WR-bracket is emission *certification*. The driver zeroed out its own report because the gate failed — that is backwards.

**Deliverable:** decouple the §8-A1 band REPORT from the WR-bracket GATE. A measurement dry-run must **measure all 18 candidates and report bands + gate outcomes side by side** — never HALT-LOUD-away its own report because 0 passed the bracket.
- This is **cheaper than "should the gauntlet run at all"** and it turns the next Tier-1 fire from a coin-flip into **guaranteed diagnostic yield**: §8-A1 bands are produced even if every candidate still fails the bracket.
- The TP3 HALT-LOUD guard stays as the *emission* certification gate (it was correct to refuse an empty *emitted bundle*); the change is that the *measurement report* is produced and persisted BEFORE/independent of that gate.
- Preserve registry-honesty: report carries gate outcomes truthfully (0/18 passing) alongside the measured bands; the proxy-heavy band stays NOT-EXERCISED (catalog is 17 none / 1 light / 0 heavy), C2 stays light-only, ≤7 stays UNPROVEN.

---

## Cross-seam contract change? (Principle 6 gate — knight-rider, at authoring)
**YES (star-lord side).** The measure-then-filter change alters the driver's report/artifact shape (adds a band-measurement report emitted independent of the gate). **Round-trip smoke REQUIRED:** a dry-run where 0/18 pass the WR-bracket still produces a persisted §8-A1 band-measurement report with all 18 measured + gate outcomes recorded → read back → bands intact + gate=0/18 recorded truthfully. **gamora side:** if G1 disposition moves `MOB_HP_DIFFICULTY_MULTIPLIER`, that is a balance-constant change (not the frozen 2.3384× chassis) → MIGRATION note + jack-ryan Gate-2. If no constant moves (design-finding path), Round-trip: not applicable on the gamora half — no boundary field changes.

## Scope
- [ ] **gamora G1:** difficulty-state disposition (inherited-uncalibrated vs ruled), cited source, documented.
- [ ] **gamora G2:** bimodality characterization — how many of 12 are bimodal-by-design vs uniformly-floored; `melee_medium_variable` treated as positional-identity hypothesis.
- [ ] **gamora G3:** convergence-timeout / fail-loud guard on R2 calibration loop — HALT-LOUD names offending class+scenario; ships regardless of G1.
- [ ] **gamora (conditional):** if G1=inherited, apply `1.5→1.25` per calibration discipline + MIGRATION + Gate-2. If G1=ruled, author the DESIGN-FINDING report (no softening) → Matt/gandalf.
- [ ] **star-lord:** measure-then-filter report/gate decoupling; bands produced independent of WR-bracket outcome.
- [ ] Round-trip smoke (star-lord): 0/18-pass dry-run still yields a persisted band report + truthful gate record.
- [ ] MIGRATION.md if any boundary field moves (gamora constant and/or star-lord report shape).
- [ ] AGENT_STATE.md updated (both seams).
- [ ] Tags: `gamora/v-...` , `star-lord/v-...` per seam convention.
- [ ] **Submit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (balance-constant change and/or driver report-shape change).

## Out of scope (explicit non-goals)
- **NO fixing the CONTENT to satisfy the INSTRUMENT** (rider 4) — do not re-roll/re-tune the 18 candidates to pass a suspect difficulty state.
- **NO softening the instrument to pass the pilot IF 1.5 is the ruled difficulty** (rider 5).
- **NO recovery-mode batch-1-fossil work** (rider 6 — the `700`/`2200` hard-codes in `w3_emission_driver.py`, same genus as the 2.3384× ratio) — NAMED follow-up, not this dispatch.
- **NO leg-3 wire touches** (TP1/TP2/TP3 proven; rider 8).
- **NO chassis / bars / bands / kit-constant touches** (frozen).
- **NO actual Tier-1 re-fire or Leg-C run in this dispatch** — this dispatch produces the disposition + guards + decoupling; the re-fire is a SEPARATE Matt run-auth (ADR-006) AFTER this lands.

## Open questions for the agents to resolve
- gamora: is 1.5 ruled or inherited? (the fork that gates everything downstream)
- gamora: bimodal-by-design count among the 12 endgame BC classes.
- star-lord: exact persist site + shape for the decoupled band report (your file-owner call).

## Kill-verify before any re-fire (rider 7 — process flag)
v2 sat wedged-alive 23:17→23:44 while v3 ran the SAME seed — a **parallel-same-seed window** (engineering-disciplines violation). Before ANY future Tier-1 re-fire: **verify no prior driver PID is still alive** (`ps`), and never run two same-seed emissions concurrently.

## References
- Tracker deltas: `batch2-run-state-2026-07-06.md` (v2-fail `3d2b8aa`, v3-0-survivor `6d11556`, this dispatch).
- gandalf Lane-C v3-aware verdict (Matt 2026-07-07) — 8 binding riders.
- Gate-1 finding `qa/findings/2026-07-07-rocket-leg3-summoner-emission-wire-projection-gate1.md` (§8-A1 framing, C2/C3).
- Logs: `/tmp/leg3_n1_v3.log` (completed, 0-survivor), `/tmp/leg3_pilot_n1_run.log` (v2 hang).
- Driver: `src/reincarnated/export/w3_emission_driver.py` (STEP 3/4 gauntlet call; `_recover_gauntlet_from_canonical_json` batch-1 fossil @ `_RECOVERY_EXPECTED_SURVIVOR_COUNT=700`).
- Spatial engine: `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (R2 calibration loop; `MOB_HP_DIFFICULTY_MULTIPLIER`, `LEASH_DISTANCE_OVERRIDE_M_SWARM`).
- ADR-004 (MIGRATION), ADR-006 (re-fire = Matt-gated external action), Principle 6, Disc #1, #1.1, #2.1, #23, #24.

## Completion record

### gamora (PRIMARY) — 2026-07-08 — COMPLETE

**G1 — difficulty-state disposition. VERDICT: NO CONSTANT MOVES (design-finding path).**
`MOB_HP_DIFFICULTY_MULTIPLIER=1.5` is a **KNOWN-PARKED-UNCALIBRATED state relative to the endgame-BC
regime**, and its re-calibration is an **explicitly Matt-scheduling-pending workstream**. Four verified
source citations (Discipline #11 — the log's remedy was NOT trusted as truth):
1. `arena.py:49` git-blame — the `1.5` line has had **exactly ONE commit ever** (`24cdc7e`,
   2026-05-19 R2 recalibration); never re-touched.
2. `R2-recalibration-math-2026-05-19.md §2.2` — the 1.5× was calibrated against **~2019 HP swarm**
   (old generic regime, 51-class heuristic cohort, convergence instrument).
3. `endgame_mob_stat_profile.py:8-16` — the endgame regime (26,500-HP swarm, W-α7+ Phase 3c
   2026-05-28, ~13× heavier) **explicitly declares itself "distinct from MOB_HP_DIFFICULTY_MULTIPLIER
   = 1.5 … DOES NOT modify arena.py."** The 1.5× stacks un-re-ruled on top of it.
4. `decisions-log.md` lines **4240 + 5223** — the multiplier is a **"separate, Matt-scheduling-pending"**
   workstream.
The log's `1.5→1.25` remedy is **WRONG + mis-scoped**: the 1.5× does NOT apply to `magic_pack`
(`MOB_HP_DIFFICULTY_SCENARIOS={open_arena, chokepoint}` — verified live) yet magic_pack = 111/323 floor
events. Applying it to green the pilot = Goodhart drift (rider 5). **Routed as DESIGN FINDING to
Matt/gandalf.** No MIGRATION (no boundary field moves on the gamora half).

**G2 — bimodality (rider 4, live hypothesis CONFIRMED).** Of the 12 endgame-BC classes reaching the
gauntlet surface: **10 bimodal-by-design (positional identity — BOTH a WR=1.000 ceiling AND a WR=0.000
floor), 2 ceiling-only (clear everything), 0 uniformly-floored.** ALL 12 wall `chokepoint_corridor` at
WR=1.000; the floor is **scenario-specific (open_arena + magic_pack), not class-specific.** The
instrument's difficulty state is the suspect, not 10-11 broken kits (Leg-B caster-vindication shape).
The dispatch exemplar `melee_medium_variable_str` is the population pattern, not an outlier. Content NOT
touched.

**G3 — fail-loud convergence guard (rider 2, unconditional; SHIPPED).** Math-note-first
(`simulation/math/r2-calibration-fail-loud-convergence-guard-2026-07-08.md`). Three fail-loud layers in
`SpatialFightEngine.run()`, all naming class+scenario: Layer A tick-budget, Layer B continuous-spawn
catch-up cap (small constant for the degenerate `interval_s≤0` direct-infinite-loop cause), Layer C
wall-clock watchdog (env-overridable). New `SpatialFightConvergenceError` (exported) + fail-loud
propagation in `run_spatial_fight` (log ERROR + re-raise, never swallow). **Smoke:** Layer B fires 0.001s,
Layer C 0.002s (both name class+scenario), regression-neutral inert. **Regression: 312 spatial tests pass,
0 failures** — guard byte-neutral on nominal fights. No boundary field → NO MIGRATION.

**Artifacts / tag / Gate-2:**
- Math note: `simulation/math/r2-calibration-fail-loud-convergence-guard-2026-07-08.md`
- Design finding (Matt/gandalf): `agentic_orchestration/gamora/notes/2026-07-08-spatial-floor-saturation-g1-g2-design-finding.md`
- Gate-2 submission: `agentic_orchestration/qa/pending/2026-07-08-gamora-g3-fail-loud-convergence-guard-gate2.md`
- Code: `spatial_gauntlet/spatial_engine.py` (guard) + `__init__.py` (export) + `_g3_convergence_guard_fire_smoke.py` (smoke)
- Tag: `gamora/v-spatial-fail-loud-convergence-guard-1`
- **No constant moved. No MIGRATION.** Auto-committed (not pushed — Matt-gated per ADR-006).

*(star-lord appends the driver/measure-then-filter half on completion.)*

### star-lord (secondary) — 2026-07-08 — COMPLETE

**Tag:** `star-lord/v-batch2-measure-then-filter-1`
**Gate-2:** `agentic_orchestration/qa/pending/2026-07-08-star-lord-measure-then-filter-gate2.md`
**MIGRATION.md:** `src/reincarnated/export/MIGRATION.md` § MEASURE-THEN-FILTER (prepended)

**Deliverable: MEASURE-THEN-FILTER (rider 1) — SHIPPED.**

Root cause of v3 zeroing out its own yield: `_build_section8a1_band_report()` did not exist; the
driver conflated the §8-A1 measurement instrument with the TP3 emission gate. When 0/18 candidates
passed the WR-bracket, TP3 halted before any measurement could be persisted.

**What shipped:**

1. **`_build_section8a1_band_report(all_kits, passing_kits, ...)` @ `w3_emission_driver.py`** — pure
   measurement function. Reads `kit.bc_proxy_density` + `kit.character_id` from ALL candidates;
   records per-candidate `wr_bracket_pass`. Produces `gate_outcome` / `band_summary` / `per_candidate` /
   `registry_honesty` sub-dicts. Registry-honesty riders embedded: NOT-EXERCISED (heavy), UNPROVEN (≤7),
   light-band-only (C2), 17 none / 1 light / 0 heavy (catalog distribution).

2. **`_SECTION8A1_BAND_REPORT_PATH`** — `src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json`

3. **Write site in `run_w3_emission()` — BEFORE TP3.** Inserted after `in_band_count` log, before
   kit-record build loop. A 0/18-pass run writes the report then hits TP3 HALT-LOUD; the file is on
   disk, independently readable.

4. **TP3 unchanged** — `assert len(survivor_kit_records) > 0` still refuses an empty emitted bundle
   (correct). Only the chronological relationship changed: measurement precedes the gate.

5. **Result dict extended** — `section8a1_band_report_path`, `section8a1_band_summary`,
   `section8a1_gate_outcome` added on normal-completion path.

**Round-trip smoke (Principle 6 / dispatch required):** 8 tests, Group F, ALL PASS (32/32 total,
  0 regressions). Key test: `test_zero_passing_round_trip_read_back` — 0/18 → file persisted →
  read-back → gate=0/18 truthful, bands intact, NOT-EXERCISED/UNPROVEN/17-1-0 riders present.

**MIGRATION.md:** additive — no bundle or registry schema change, no drax or gamora consumer action.

**Not in scope (confirmed):** no constant moved, no Tier-1 re-fire, no recovery-mode batch-1-fossil work,
  no simulation touches. Leg-C re-fire gated on gamora G1/G2/G3 + Matt ADR-006 run-auth.

### R2 fire (star-lord, KR-orchestrated) — 2026-07-08 — COMPLETE

**Kill-verify:** `ps aux | grep w3_emission_driver` — clean, no driver alive before commit.

**Fire params:**
- `dry_run_flavor=True`, seed 56000000, n_samples=1
- Detached PID 12819, 25,530 fights, wall-clock 1507.6s
- $0 spent (dry-run mode held throughout)

**Measure-then-filter proof:** §8-A1 band report persisted at STEP 4 (`_SECTION8A1_BAND_REPORT_PATH`)
BEFORE TP3 HALT-LOUD fired on the empty survivor set. This is the exact scenario the dispatch's rider 1
was designed to handle — the instrument now produces diagnostic yield even when 0/18 pass.

**Gate outcome:** 0/18 passing (`emission_certified=false`). Expected — instrument is known
floor-saturated. This is the before-side snapshot for R3a's before/after diff (gandalf §5.1).

**G3 convergence guard:** did NOT fire — gauntlet ran to clean completion (1507.6s), confirming
G3's guard is inert on nominal runs (regression-neutral, as gamora's smoke verified).

**Measured bands:** 17 none / 1 light / 0 heavy (NOT-EXERCISED). All 18 per-candidate records
present with `wr_bracket_pass=false`. Registry-honesty riders all present in artifact.

**Artifact committed + pushed (engine repo):**
- Path: `src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json`
- Engine commit: `75637f5` (pushed to `main`)
- No companion file committed — the band report is self-contained (generated_at 2026-07-08T05:55:13Z).
  The `cycle-13-gauntlet-sim-results-*` filename KR referenced does not exist on disk; the band
  measurement JSON IS the durable record of this fire.

**Status:** Before-side snapshot secured. R3a (recalibration + after-side diff) gated on gamora
G1/G2/G3 design-finding disposition by Matt/gandalf + fresh Matt ADR-006 run-auth.
