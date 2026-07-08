# Dispatch — 2026-07-08 — gamora — pilot precondition: F3 verify + catalog-count consume + Leg-ii harness + geared-arm wire

**From:** knight-rider
**To:** gamora
**Approved by:** Matt (two-leg pilot process ratified 2026-07-08); commissioned via gandalf transmission `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`
**Estimated effort:** ~4.5–6.5 h (four beats; beat (a) is verify-not-derive per Gate-1; beat (d) geared-arm wire appended 2026-07-08 per Matt Option-3 ruling — hours-scale)
**Acceptance:** F3 STOP resolution **confirmed to hold** under the extended catalog + re-point (NOT re-derived — it was resolved 2026-07-07); gamora consumes rocket's catalog MIGRATION (count 18→N across all six guard sites + band entries) so `gauntlet_sim` imports clean AND the t4 catalog-load path runs clean over the extended catalog; Leg-ii kit-grain spatial harness prepped drawing from the seed-57000000 population.

> **Gate-1 amendment (jack-ryan, 2026-07-08 — BLOCK cleared):** the F3 `boss_damage_scale` STOP is **ALREADY RESOLVED**, verified against source: `gauntlet_lived_channel_repilot_driver.py:62` → `F3_STOP_FLAG = False  # RESOLVED`; `bds=48.0` LOCKED (`:59-60`, boss dmg = 5.0*0.03*48.0 = 7.2, F3 pop WR 0.7018 in-band); derivation math note `simulation/math/step3-f3-boss-damage-scale-2026-07-07.md` exists (2026-07-07). The commissioning transmission's §8.5 carried the STOP forward as open — a stale carry-forward (the exact class of error §8.1 retracted). **Beat (a) is therefore VERIFY-not-DERIVE.** Do NOT re-derive or re-lock the scale.

## Context

The 1800-candidate emission run was Matt-killed 2026-07-08 as mis-instrumented. Two seams supply the pilot preconditions: rocket adds the missing F4/F1 rooms + dedups the feed (companion dispatch); **you** confirm the (already-resolved, 2026-07-07) F3 STOP still holds, consume rocket's cross-seam catalog contract, and prep the Leg-ii kit-grain harness. The stratified re-fire pilot fires only when all three preconditions land (catalog · dedup · F3 fix). This dispatch fires NO run — it validates instruments and preps a harness.

Governing doc: **§8** of `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md` (§8 governs where it conflicts with §2/§3/§6).

## Required reading before starting

- **Post-mortem §8** (governs): the same-day correction — §8.2 (season_emit≡0 by construction), §8.5 (revised two-leg pilot; Leg-ii is yours).
- **Commissioning transmission:** Unit 2 (your unit) — `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`.
- **rocket's MIGRATION.md** (`generation/MIGRATION.md`, top entry — LANDED, N=20) — declares the encounter count 18→20, the **seven** count-guard sites you update (five in `gauntlet_sim.py` + `t4_sim_cycling.py:617-620` + `wave5_season_orchestrator.py:103`), and the band needs (dense_cell only; escape_lane already wired).
- Your own seam: `gauntlet_sim.py:109/667/1203/1871/1884` (count guards), `:323` (`ENCOUNTER_COHORT_KPM_BAND`), `:611-625` (`SPATIAL_ENCOUNTER_KPM_BAND` + keys=={"balanced"} assert), `:217-234` (escape_lane criterion, registered).
- `simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md` (band-derivation methodology — for the dense_cell band).
- engineering-disciplines.md: **#1** (math-before-code — F3 scale + dense_cell band), **#2/#2-FF**, **#11**, **#18.1** (substrate-voting-is-binding), **#24** (single-parameter sweep isolation).

## Math-before-code

- **Beat (a) F3 `boss_damage_scale` — VERIFY, do not derive:** the rank-deficiency was diagnosed and the corrected scale (`bds=48.0`, boss + mini-boss tiers only) derived and LOCKED 2026-07-07 (math note `step3-f3-boss-damage-scale-2026-07-07.md`; `F3_STOP_FLAG = False`). Your job is to **confirm the resolution still holds** under the extended catalog + any driver re-point, and cite the provenance. Discipline #24 here means the INVERSE risk: **do NOT perturb the locked `boss_damage_scale=48.0`** (`repilot_driver:61`). If the re-point demonstrably invalidates the 2026-07-07 lock, STOP and escalate with the specific reason — do not silently re-derive.
- **Beat (b) dense_cell band:** derive its `ENCOUNTER_COHORT_KPM_BAND` / `SPATIAL_ENCOUNTER_KPM_BAND` entry per the w-alpha-6 methodology. **escape_lane band = wiring only** (already registered + density-verified at `:217-234`; do NOT re-derive).
- **Beat (c) Leg-ii:** no derivation; the discipline is sampling-frame correctness — draw from the seed-57000000 population, NOT fresh rolls (below).

## Cross-seam contract change? (Principle 6 gate — completed by knight-rider at authoring)

**Beat (b): YES — you are the CONSUMER of rocket's cross-seam contract change (ADR-004).** rocket's MIGRATION.md hands you the count/band contract. You update **all seven** count-guard sites — five in `gauntlet_sim.py` (`:109`, `:667`, `:1203`, `:1871`, `:1884`), `t4_sim_cycling.py:617-620` (runtime SC-6 guard), and `wave5_season_orchestrator.py:103` (module-level assert) — from 18 → 20 and add the dense_cell band entry (escape_lane needs none). All seven are in YOUR `simulation/` seam. **Ordering:** rocket lands FIRST (DONE — `rocket/v-pilot-precond-catalog-dedup-1`, commit `086fb6c`). The catalog is now 20; `import gauntlet_sim` / `import wave5_season_orchestrator` currently raise `AssertionError` (18 ≠ 20) and the t4 catalog-load path raises the SC-6 RuntimeError — this transient is expected and confined to your seam; your consume beat closes it. Do not tag any milestone while the window is open.

**Round-trip smoke (Principle 6 — you complete rocket's beat-(a) round-trip):** after consuming, `import gauntlet_sim` is clean AND a gauntlet smoke over the extended catalog emits per-family verdicts including **F4 (escape_lane)** and **F1 (dense_cell)**. This smoke is the round-trip that closes the rocket→gamora contract. Cite it in your completion record.

**Beats (a) and (c): NO cross-seam contract change.** F3 scale is within-seam simulation; Leg-ii harness prep produces a sampling harness, not an inter-seam dict field. Round-trip: not applicable for (a) and (c).

## Scope

**Beat (a) — F3 `boss_damage_scale`: VERIFY resolution holds (NOT re-derive):**
- [ ] Confirm F3 STOP resolution status against source: `repilot_driver:62` (`F3_STOP_FLAG = False`), `:59-61` (`bds=48.0` LOCKED), math note `step3-f3-boss-damage-scale-2026-07-07.md`.
- [ ] Confirm the resolution holds under the extended catalog + any driver re-point; a boss-fight smoke shows non-degenerate F3 verdicts under the locked `bds=48.0`.
- [ ] Cite the resolution provenance in the completion record. If (and only if) the re-point invalidates the lock, STOP and escalate with the specific failing evidence — do NOT re-derive silently.

**Beat (b) — consume rocket's catalog MIGRATION (cross-seam):**
- [ ] Read rocket's MIGRATION.md (`generation/MIGRATION.md`, top entry — N=20); update **all SEVEN** count guards from 18 → 20, ALL in your `simulation/` seam: five in `gauntlet_sim.py` (`:109`, `:667`, `:1203`, `:1871`, `:1884`), `t4_sim_cycling.py:617-620` (runtime SC-6 guard), **plus `wave5_season_orchestrator.py:103`** — a module-level `assert len(ENDGAME_ENCOUNTER_CATALOG) == 18` (message mislabeled "ACTIVE_CELL_COUNT"; rocket surfaced this seventh guard when it tripped his pipeline import). Missing any leaves a false-clean window — the mis-fire's own signature (a guard nobody re-pointed).
- [ ] **Bands (corrected per rocket's MIGRATION):** `escape_lane` needs **NO new band entry** — its F4 criterion is already wired via the registration at `gauntlet_sim.py:883-889` (reads `tier_2_survival_rate` ≥0.80 + `tier_2_kpm` ∈ [60,150]); do NOT add an escape_lane band or re-derive it. `dense_cell` needs a **NEW** `ENCOUNTER_COHORT_KPM_BAND` + `SPATIAL_ENCOUNTER_KPM_BAND` entry (derived per w-alpha-6). The `len(ENCOUNTER_COHORT_KPM_BAND) == 6` band-count assert moves **6 → 7** when dense_cell's band lands. Respect the `:625` keys=={"balanced"} assert.
- [ ] `import gauntlet_sim` clean AND `wave5_season_orchestrator` imports clean AND the **t4 catalog-load path runs clean** (a bare import does NOT trip `t4_sim_cycling:618` — it's a runtime guard inside a function); gauntlet smoke emits per-family verdicts over the 20-encounter catalog including F4/escape_lane + F1/dense_cell (the round-trip — rocket's standalone smokes cannot verify this).

**Beat (c) — Leg-ii kit-grain spatial harness prep:**
- [ ] Harness: **18 cells × ~6 kits**, **kit-grain family verdicts** on the spatial harness.
- [ ] **Sampling discipline (MANDATORY): draw from the seed-57000000 population, NOT fresh rolls** — GRAIN must measure the actual population emission would stamp (transmission Unit 2(b); §8.5 Leg-ii).
- [ ] Harness produces the GRAIN verdict shape (within-cell verdict heterogeneity: do same-cell kits diverge on family verdicts?). Prep only — no full run fires from this dispatch.

**Beat (d) — geared-arm certification instrument: WIRE + smoke `certification_gear v0`** *(appended 2026-07-08 per Matt Option-3 ruling; authority: gandalf spec `2026-07-08-leg-i-geared-arm-certification-gear-spec.md`)*:
- [ ] **Wire `measured_gear_stats` onto the gauntlet path.** The cert gauntlet currently fights STRIPPED kits (`t4_sim_cycling.py:1222-1238` passes no `measured_gear_stats`; adapter contract "None = stripped baseline" at `spatial_resolver_adapter.py:149`). Thread cohort gear through `w5g1_gauntlet_execution → w4g1/w4g2 → _run_spatial_w4g_batch → run_spatial_fight` — the consumer already accepts it (`spatial_engine.py:3351`). This restores the Cycle-13 designed state (geared fights, `10a6193`) silently dropped by the 1D-sim-deletion repoint (`de09d8b`, 2026-06-16) and closes the §7 spec gap ("gear is a treatment variable") at the stat-power layer.
- [ ] **Implement `certification_gear(cohort, power_level=endgame_node)`** composing two already-ruled, currently-dormant instruments: Legendary-T1 weapon shell + set 2pc/4pc (keystone **6b** reference set, `combatant.py:441-475`). **Magnitudes are RULED anchors — cite, do not re-derive:** 4pc **+35% dmg** = chain-T4 band [25%,50%] MIDPOINT (Matt §6 ruling 2026-06-16); **+18% armor / +12% hp** = Legendary-T1 stat band. Four cohort tilts via `stat_preference_vector` (offense/defense/utility split, `_build_cohort_combatant_stats` `t4_sim_cycling.py:927`). Signature-compatible with the future soul-bound `express_gear(power_level, kit)` (§7) — succession = a function swap.
- [ ] **Composition detail (your implementation call under these anchors):** 6b is single-neutral (not profile-keyed) → layer the cohort tilt over the 6b skeleton; use a **fixed representative Legendary-T1 shell** (keystone archive-remeasure pattern), NOT per-kit real weapons (that would couple cert to kit-specific rolls); power-level scaling may follow the `compute_balance_gear_stats` L50 `base_mag × scalar` pattern (`gear_catalog.py:196`). Document your call.
- [ ] **Smoke (arm S vs arm G):** on a small same-seed slice (seed 57000000), demonstrate arm S (stripped, as-built) and arm G (`certification_gear v0`, all four cohorts) produce **different** WR/KPM on the same config — proving gear threads. **No full Leg-i two-arm run fires here** (that's the pilot); this beat WIRES + smokes so Leg-i CAN run both arms.
- [ ] **#2-FF rider (arm G):** instrument identity `"certification_gear v0"` printed in the run start-banner; pre-fire verification `grep -n measured_gear_stats src/reincarnated/simulation/t4_sim_cycling.py` → non-empty (proves the thread landed); first-log expectation names BOTH arms.

**Common:**
- [ ] Smoke-test passes (each beat)
- [ ] MIGRATION consumed (beat b) — round-trip smoke cited
- [ ] Round-trip smoke (beat b) / not-applicable (a, c) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag (intermediate, seam-prefixed): e.g. `gamora/v-pilot-precond-f3-consume-legii-1`

## Acceptance criteria

- [ ] F3: resolution confirmed to hold — provenance cited (`F3_STOP_FLAG=False`, `bds=48.0` locked, 2026-07-07 math note); boss-fight smoke shows non-degenerate F3 verdicts; locked `bds=48.0` NOT perturbed
- [ ] All SEVEN count guards updated 18 → 20 (`gauntlet_sim.py` ×5 + `t4_sim_cycling.py:617-620` + `wave5_season_orchestrator.py:103`)
- [ ] `python -c "import reincarnated.simulation.gauntlet_sim"` AND `python -c "import reincarnated.simulation.wave5_season_orchestrator"` both exit clean (no AssertionError) AND the t4 catalog-load path runs clean (a call exercising `t4_sim_cycling` catalog validation raises no SC-6 RuntimeError)
- [ ] dense_cell band entry present (derived); NO escape_lane band added (wired via `:883-889`); `len(ENCOUNTER_COHORT_KPM_BAND) == 7` assert holds; `:625` keys assert still holds
- [ ] Gauntlet smoke over the N-encounter catalog emits per-family verdicts incl. F4/escape_lane + F1/dense_cell (this is the beat-(b) round-trip; must exercise the t4 path, not a bare import)
- [ ] Leg-ii harness runs a smoke slice (e.g. 2 cells × 2 kits) drawing from seed-57000000 population and emits kit-grain family verdicts — full 18×~6 is prep, not fire
- [ ] Beat (d): `grep -n measured_gear_stats src/reincarnated/simulation/t4_sim_cycling.py` non-empty; arm-S-vs-arm-G smoke slice shows differing WR/KPM on the same config; `certification_gear v0` named in start-banner; magnitudes cite the ruled anchors (+35% dmg / +18% armor / +12% hp), NOT re-derived; NO bands re-fit in this dispatch (succession clause)
- [ ] Round-trip smoke: beat (b) round-trip cited (import-clean ×2 + t4 path + per-family verdicts over extended catalog). Beats (a)/(c)/(d): not applicable — within-seam (beat (d) threads an existing dormant parameter; no new cross-seam contract).

## #2-FF pre-fire verification (this dispatch names its instruments)

- **Beat (a) instrument:** F3 resolution provenance + a boss-fight sim smoke. **Pre-fire check:** `grep F3_STOP_FLAG src/reincarnated/simulation/gauntlet_lived_channel_repilot_driver.py` → `= False  # RESOLVED`; a boss-fight smoke under the locked `bds=48.0` shows non-degenerate F3 verdicts. (This is a confirm, not a derive — the STOP is already closed.)
- **Beat (b) instrument:** `import gauntlet_sim` + the t4 catalog-load path + gauntlet per-family verdict emission. **Pre-fire check (must exercise BOTH guard files):** `python -c "import reincarnated.simulation.gauntlet_sim"` exits clean AND a call through `t4_sim_cycling`'s catalog validation raises no SC-6 RuntimeError. A bare import alone is INSUFFICIENT — the t4 guard (`:618`) is runtime, not import-time. First-log-line of gauntlet smoke: `catalog N encounters | families F1..F4 all covered`.
- **Beat (c) instrument:** the Leg-ii harness's kit-grain verdict emitter. **Pre-fire check:** smoke slice log names the seed source (`population seed=57000000`, not `fresh roll`) and emits per-kit family verdicts.
- **Beat (d) instrument:** `certification_gear v0` named in the run start-banner + the arm-S/arm-G delta. **Pre-fire check:** `grep -n measured_gear_stats src/reincarnated/simulation/t4_sim_cycling.py` → non-empty (thread landed); first-log-line names both arms; smoke slice shows arm G ≠ arm S on WR/KPM for an identical config.
- **Precondition state this dispatch stands on:** four-family gate LIVE (R4 flip 2026-07-07); F3 STOP RESOLVED 2026-07-07 (`bds=48.0` locked — this dispatch confirms, does not re-open); catalog extension arrives via rocket's MIGRATION.

## Out of scope (explicit non-goals)

- **Do NOT touch `generation/endgame_encounter_catalog.py`** or `season_generation_pipeline.py` — rocket's seam. You consume the MIGRATION; you do not add rooms or dedup the feed.
- **Do NOT fire the full Leg-ii run** (18×~6 harvest) — prep + smoke slice only. No emission run of any size until the pilot's verdicts land and Matt's rulings close (post-mortem §6).
- Do NOT re-derive the escape_lane band (registered + density-verified; wiring only).
- Do NOT draw Leg-ii kits from fresh rolls — the sampling-frame is the seed-57000000 population by mandate.
- **Do NOT re-derive or re-lock `boss_damage_scale`** — the 2026-07-07 resolution (`bds=48.0`) stands unless the re-point demonstrably invalidates it (in which case STOP + escalate, do not silently change it). Do NOT co-change other scale parameters (Discipline #24 isolation).
- **Beat (d) — Do NOT re-fit KPM bands to geared distributions in this dispatch.** All live bands are fit to stripped distributions; re-fit happens at emission re-fire (gear-spec §5 succession clause), NOT now. This beat WIRES + MEASURES the stripped-vs-geared deltas; it does not move bands.
- **Beat (d) — Do NOT gear mobs.** Player kits ONLY (§7 sawtooth guard [DECISION/CRITICAL]); mobs stay depth-fixed budgets. Geared-player-vs-depth-fixed-mob is the ruled shape.
- **Beat (d) — Do NOT implement the effect layer** (legendary specific effects §7-crux, gems, per-kit idiom expression, affix RNG). The arm measures the STAT-POWER layer only; effects are measured later by the loot campaign's generate→sim→check-in-band loop.
- **Beat (d) — Do NOT expect gear to rescue F4-martial.** The gear stat surface carries NO mobility/exit-window stat (F4 honesty property); the F4-martial disposition fork (queued post-Leg-ii) is untouched by this arm.
- **Beat (d) — If `certification_gear v0` requires modifying a rocket-owned file** (e.g. `gear_catalog.py` beyond read-only import of `compute_balance_gear_stats`), STOP and flag for a MIGRATION — do not reach across the seam. Reading/importing existing functions is fine; the wire lives in your `simulation/` files (`t4_sim_cycling.py`, `combatant.py`).

## Open questions for the agent to resolve (document your calls)

- Confirming the F3 `bds=48.0` resolution holds under the extended catalog + re-point (VERIFY — cite provenance; do not re-derive).
- The dense_cell band values per w-alpha-6 methodology (math-before-code; falsifier named).
- Whether the seed-57000000 population is materialized on disk or must be regenerated deterministically from the seed for Leg-ii sampling — document the sampling mechanism either way.
- If same-cell kits diverge on family verdicts in the smoke slice: note it (it feeds the GRAIN verdict — the transmission's demo-roster-kits-get-individual-cert path). Full analysis is the pilot's, not this dispatch's.

## References

- Post-mortem §8 (governs): `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md`
- Commissioning transmission (Unit 2): `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`
- **Geared-arm gear-spec (beat d authority, Matt Option-3 ruling):** `agentic_orchestration/gandalf/notes/2026-07-08-leg-i-geared-arm-certification-gear-spec.md`
- Soul-bound gear model (succession end-state): `canonical/reap-die-rise-engine/design-decisions-session.md` §7
- `combatant.py:441-475` (6b reference set), `t4_sim_cycling.py:927/1222-1238` (cohort stats + stripped-fight site), `spatial_engine.py:3351` (measured_gear_stats consumer), `gear_catalog.py:196` (L50 base_mag×scalar pattern — read-only)
- Companion dispatch (rocket, supplies your MIGRATION): `2026-07-08-rocket-pilot-precondition-catalog-dedup.md`
- `gauntlet_sim.py:109/217-234/323/611-625/667/1203/1871/1884` (your seam)
- `simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md`
- Discipline #2-FF proposal (jack-ryan ratification queue): `agentic_orchestration/gandalf/notes/2026-07-08-discipline-2-amendment-full-fire-rider-proposal.md`

## Completion record

**Completed by:** gamora, 2026-07-08. **Tag:** `gamora/v-pilot-precond-f3-consume-legii-1` (commit `b1dec28`, engine repo). **NO run fired; NOT pushed (Matt-gated); NO milestone tag (count window open).**

- **(a) F3 VERIFY — resolution HOLDS.** Provenance cited at source: `gauntlet_lived_channel_repilot_driver.py:62` `F3_STOP_FLAG=False`, `:61` `bds=48.0` LOCKED, `:57` `mds=0.03`, `:65` `boss_hp=9000`; boss dmg = 5.0×0.03×48.0 = 7.2 (matches math note `step3-f3-boss-damage-scale-2026-07-07.md`). Extended catalog is bds-inert (F1/F4 carry no boss tier; no-leakage §1.3). Boss-fight smoke: bds=1.0 → WR=1.0 (defanged/STOP); bds=48.0 → WR=0.50 (non-degenerate). Locked 48.0 NOT perturbed.
- **(b) Consume — DONE.** All SEVEN guards moved 18→20 (five gauntlet_sim.py + t4_sim_cycling.py:618 + wave5_season_orchestrator.py:103; mislabeled "ACTIVE_CELL_COUNT" message corrected). **EIGHTH orphaned marker found + fixed** (`t4_sim_cycling.py:1891 _ENCOUNTER_CATALOG_EXPECTED_COUNT`, never-asserted false-invariant). dense_cell band DERIVED density-anchored **(12.52, 102.86)** [14s..115s @ 24 mobs]; GEOMETRY-ONLY (no distribution on disk; falsifier named) — added to BOTH `ENCOUNTER_COHORT_KPM_BAND` + `SPATIAL_ENCOUNTER_KPM_BAND` (the :622 key-set-equality forces the sibling); band-count assert 6→7 at BOTH sites (:646 + :1870/:1880); :625 balanced-only holds. Round-trip CLOSED: imports clean ×2 (count=20, bands=7×2); t4 catalog-load path clean (`w4g0_calibration_setup` → CoverageMatrix, no SC-6 raise); metrology `--beat` per-family verdicts incl **F1/dense_cell** + **F4/escape_lane** (both route + fought; dense_cell spawns 24 confirmed); `_shell_result_passed(dense_cell)` now real (was default-False). Math note `dense-cell-f1-band-derivation-2026-07-08.md`.
- **(c) Leg-ii harness — PREPPED + smoke PASS.** `simulation/leg_ii_kit_grain_spatial_harness.py`. Sampling frame: seed-57000000 population REGENERATED deterministically at emission n_samples=100 then SLICED (avoids the n_samples-dependent fresh-roll trap; population not on disk). `--slice` (2×2) PASS; kits `S1_<cell>_s0/s1`. GRAIN: same-cell kits do NOT diverge in-slice (CAVEAT: native-HP metrology bars = uncalibrated; the meaningful GRAIN read needs the calibrated lived-channel bars = the pilot's).
- **(d) Geared-arm — WIRED + smoke DIFFERS.** `certification_gear v0` (combatant.py): 6b skeleton (ruled anchors, cited) + cohort tilt, ADDITIVE (band-invariance preserved); fixed Legendary-T1 shell; gear_catalog.py NOT touched. `measured_gear_stats` threaded onto `_run_spatial_w4g_batch` → `run_spatial_fight` (consumer already accepted it). #2-FF grep proof non-empty (4 hits). Smoke: arm S vs arm G DIFFER=True on a 231k-HP boss (arm G faster; DPS tilt gains more); DIFFER=False on a trivial mob = clear-speed saturation (not a wiring gap — thread verified reaching the combatant). NO band re-fit, NO mob gear, NO effect layer, NO MIGRATION. Math note `certification-gear-v0-composition-2026-07-08.md`.
- **Regression:** 79 green (test_cycle13_wave5_gauntlet_sim + test_spatial_gauntlet_scenarios; 2 stale count-guard tests moved 18→20).
- **CROSS-SEAM FLAG (KR):** `tests/test_cycle13_wave5_season_generation.py:116` (`len(ENDGAME_ENCOUNTER_CATALOG)==18`) FAILS (now 20) — a GENERATION-seam test rocket's landing (086fb6c) left stale; NOT patched (out of gamora's fence); rocket owes the one-line fix. `ACTIVE_CELL_COUNT==18` (:122) stays (kit-gen decoupling). Also surfaced (not patched): `wave5_season_orchestrator.py:162/173` `enc_total=18` quality-vector fallback DEFAULTS (not hard guards; a change would need its own math note).
