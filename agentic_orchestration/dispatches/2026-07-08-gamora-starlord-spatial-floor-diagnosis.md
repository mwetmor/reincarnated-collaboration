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
*(appended by gamora + star-lord on completion)*
