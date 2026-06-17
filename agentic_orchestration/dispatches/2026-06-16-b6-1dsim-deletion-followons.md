# Dispatch — 2026-06-16 — Follow-ons A + B to the b6-stack + 1D-sim deletion

**From:** knight-rider (Matt-authorized 2026-06-16, post-push)
**Approved by:** Matt 2026-06-16 — "push authorized, then run the two follow-ons."
**Status:** FIRED (gamora leads B; A's unambiguous sweep runs in parallel)

## Context
The b6 archetype stack + 1D battle sim deletion landed and PUSHED (engine `93b8fe0..a2deaa0`, 7 commits, Gate-2-cleared). Fallout: ~51 `.py` test files fail at **collection** because they import now-deleted modules (`b6_kit_builder`, `b6_archetype_templates`, `class_generator`, `archetype_classifier/composer`, `stat_allocator`, `composed_kit_adapter`, `season_orchestrator`, `SeasonOutput`, `season_writer`, `summary_formatter`, `fight_engine`). They test the deleted path and are OFF the live import path (live spatial suites pass 115/115). Plus one live-code repair: `t4_sim_cycling.py` still imports the deleted `fight_engine`.

`.pyc` caches in `__pycache__/` are stale duplicates — ignore (gitignored).

## Discipline (Matt, both follow-ons)
- **Delete the test file outright** if it is **entirely** about deleted module(s).
- **Extract surgically** if it mixes deleted + LIVE coverage — preserve the live coverage, drop the dead.
- Do NOT delete live coverage. If an assigned file's live coverage belongs to another seam, FLAG it (don't edit another seam's live code).
- ONLY touch your assigned files. If you hit a file you believe is mis-routed, flag it — don't edit it.

## Sequencing (Matt)
**B LEADS.** `w5r2_gauntlet_sim_integration` (gamora's `test_cycle13_wave5_gauntlet_sim.py`) is a collection failure whose ROOT CAUSE is B's `t4_sim_cycling` dangling import. gamora does B (the repair) first, makes the repoint-vs-delete call, then that test collects again and its A-disposition follows the B call — all intra-gamora. **A's unambiguous-legacy sweep (rocket gen tests, star-lord output test, gamora balance_loop-only tests) runs in parallel.** Files are disjoint across agents → safe to parallelize.

---

## Follow-on B — `t4_sim_cycling` repair + 1D-sim test cleanup (gamora, leads)

**Code repair (live):** `simulation/t4_sim_cycling.py:1018` + `:1122` both `from reincarnated.simulation.fight_engine import simulate_fight` — the deleted 1D module; breaks `w5r2_gauntlet_sim_integration`.
- **Triage liveness first:** is the `w5r2_gauntlet_sim_integration` path still wanted?
  - YES → repoint onto the 2D spatial sim's fight entry.
  - NO → delete the dead branches.
- **Stale comments:** fold in the comments that still describe "spatial runs alongside the 1D fight_engine" (`spatial_engine.py`, `spatial_gauntlet/__init__.py`) — they misdescribe the now-sole-sim reality. Dead line-number citations elsewhere are lower-priority (gamora discretion).

**1D-sim test sweep (11 `.py`, `fight_engine`-importing):** test_balance_loop, test_cycle12_layer6_t4_wireup, **test_cycle13_wave5_gauntlet_sim (= w5r2; dispose AFTER your repair call)**, test_energy_types, test_gate3b_ms_consumption, test_gear_cp5, test_gear_integration, test_r7_parity, test_range_profile, test_role_orientation, test_wb_typewall_rename.

**balance_loop-only convergence test sweep (3 `.py`):** test_a4_recompose_energy_calibration_round_trip, test_telemetry_v24, test_w093_usage_modes. (Recompose machinery is deleted → these test the deleted convergence path; delete-or-extract per discipline.)

**Close (B):** jack-ryan Gate-2 (live code change). Tag `gamora/v1.1-b6-1dsim-followon`. Do NOT push (separate Matt auth at close).

---

## Follow-on A — legacy-test collection sweep (rocket + star-lord, parallel)

### rocket — generation test sweep (36 `.py`)
test5_multishot_stability, test_b11_geometry_palette, test_b6_generator_wired, test_bc_target_subspace_generator, test_canonical_loadouts, test_cascade_r3_s3_archive_variant_preservation, test_cascade_r3_s5b_wave_b_orchestrator_integration, test_cascade_r4_followon_wave_b_persistence_plus_wave_s_integration, test_cascade_r4_path_x_pm1_input_source, test_cascade_r4_track_a_season_production, test_class_generation, test_combat_simulator, test_cosmological_vocabulary, test_cp8_gear_naming, test_cp9_gear_telemetry, test_cycle12_wave5_sim_combatant_integration, test_d2_substrate_coupling, test_d3_archetype_composer, test_dodge_gated_flag_defer, test_embodiment_axis_schema, test_gear_cp3, test_gear_cp5b, test_gear_cp6, test_grouping_layer_schema, test_integration, test_movement_speed_schema, test_naming, test_no_canonical_four_in_llm_prompts, test_role_registry, test_spirit_guide, test_spirit_guide_orchestrator_wiring, test_stage2_bc_keying, test_telemetry_tier1, test_telemetry_v21, test_wave5_swift_closure_path_x_phase4_feeds_phase5, test_wind_controller_dps_floor.

Some import `SeasonOutput`/`season_writer` too (mixed legacy) — they're yours by gen-domain primary; if any holds genuine LIVE output-seam coverage, flag for star-lord rather than delete it.

### star-lord — output test sweep (1 `.py`)
test_cycle11_schema_extensions_round_trip (imports `season_writer`). Delete-or-extract per discipline; preserve any live round-trip coverage that doesn't depend on the deleted writer.

**Close (A):** jack-ryan confirms GREEN COLLECTION (zero import-time failures across the suite). Tags `rocket/v1.1-legacy-test-sweep`, `star-lord/v1.1-legacy-test-sweep`. Do NOT push (separate Matt auth at close).

---

## Overall close
jack-ryan: Gate-2 on B (live repair) + green-collection confirmation on A. Then KR surfaces push auth to Matt. Items 4 (archetype-label monster-AI asymmetry) + 5 (Proxy-Commander forward-work) stay queued — NOT part of this dispatch.

---

## Completion record — Follow-on B (gamora, 2026-06-16, SESSION 24)

**Tag:** `gamora/v1.1-b6-1dsim-followon`. **NOT pushed** (Matt-gated at close). **Math note (Disc #1, authored first):** `simulation/math/t4-sim-cycling-spatial-repoint-2026-06-16.md`. **MIGRATION:** `simulation/MIGRATION.md v1.72`.

### PART B — live-code repair

**w5r2 repoint-vs-delete decision: REPOINT (NOT delete).** Reasoning (empirical triage, Disc #11): the W4G/W5G gauntlet KPM-sweep path is LIVE-reachable from current season production — `scripts/run_season_production.py` → `wave5_season_orchestrator.run_season_production` (Phase 3) → `season_generation_pipeline.w5r2_gauntlet_sim_integration` → `gauntlet_sim.run_gauntlet_sim` → `w5g1_gauntlet_execution` → `t4_sim_cycling.w4g1_tier_1_sweep` + `w4g2_tier_2_full_sim` (the two dangling `simulate_fight` imports). Also reached via `unified_calibration_loop` + `sc7_calibration_loop`. The functions import fine (function-scope deps) but fail-loud the instant Phase 3 fires → season production is BROKEN. Delete was wrong. **Repointed** both call sites (`t4_sim_cycling.py:1018` + `:1122`) onto the 2D spatial sim via new helper `_run_spatial_w4g_batch()` → `run_spatial_fight()` against the encounter's OWN declared arena shell (`encounter.scenario_shell_id` → `ALL_SCENARIOS`), mapping per-fight `SpatialFightResult` (`winner`/`player_kill`/`elapsed_s`) onto `FightSummary`. Mirrors the deletion-commit's `balance_loop._run_spatial_slot` pattern (sole sim, all tiers).

**SEMANTIC SHIFT declared (Disc #12), NOT buried:** `observed_kpm` is now measured on the spatial pack-clear instrument (KPM ceiling ~44) but the `COHORT_KPM_BAND` it is compared against is still the 1D-duel band (150-836). Smoke confirms the under-read (T1 kpm=0.63 → REJECT). Band recalibration to the spatial instrument is a **gandalf-seam item** (surfaced to KR at gamora SESSION 18 / WC-spike), NOT done here. Repoint restores runnability + carries the calibration debt openly (math note §4, MIGRATION v1.72, code comments at both sites). Routed to jack-ryan for a decisions-log entry.

**Stale comments fixed:** `spatial_gauntlet/spatial_engine.py` header ("Runs ALONGSIDE the 1D fight_engine.py — does NOT replace it") + `spatial_gauntlet/__init__.py` header ("running alongside the 1D fight_engine ... Both run concurrently") → both now state the 2D spatial engine is the SOLE battle sim (1D kernel deleted a8b28a1), historical co-residence framed as past. Also `wr_1d_fight=0.0 # filled by caller after 1D run comparison` → "inert since 1D-sim deletion".

**Smoke (Disc #2):** clean-build OK. Behavioral: `scripts/gamora_t4_spatial_repoint_smoke_2026_06_16.py` SMOKE PASS — w4g1 (10 fights) + w4g2 (20 fights) on a REAL catalog encounter + real emitted-skill PlayerClass populate StratumFightBatch, observed_kpm/survival finite, termination_reason ∈ {b_dead,a_dead,timeout}. Live spatial suite + retained tests: 99 passed.

### PART A — simulation-seam legacy-test sweep

**DELETED (9, entirely about deleted modules — 1D fight_engine ± rocket-deleted generators; no isolable mine-seam live island, live bits depend on rocket's deleted `class_generator`/`stat_allocator`/`season_orchestrator` fixtures):** `test_gate3b_ms_consumption.py`, `test_r7_parity.py`, `test_range_profile.py`, `test_wb_typewall_rename.py` (1D shim/type-wall), `test_balance_loop.py` (simulate_room 1D + ClassGenerator), `test_energy_types.py`, `test_role_orientation.py`, `test_gear_cp5.py`, `test_gear_integration.py`.

**EXTRACTED (1):** `test_cycle13_wave5_gauntlet_sim.py` (= w5r2 test, disposed LAST per sequencing). MIXED: §6 `TestRunGauntletSimSmoke` mocked the deleted `fight_engine.simulate_fight` + MagicMock player_class — DEAD (and post-repoint, run_gauntlet_sim routes through run_spatial_fight, so the mock target no longer exists). Dropped §6 + the two orphaned 1D-mock helpers. PRESERVED the LIVE coverage: §1–§5 (`GauntletEncounterResult`/`GauntletKitResult`/`GauntletQualityReport` data-structure + gate-math + W5G.2 round-trip) + §7 (`TestPostScriptEmpiricalCounts`, Disc #11). NOTE: 7 `TestGauntletKitResult` failures remain — VERIFIED PRE-EXISTING (identical on HEAD pre-edit; documented baseline gap in `gauntlet_pass()` gate logic, unrelated to the deletion/extraction). Triaged out-of-scope (Disc #5); coverage preserved, baseline flagged.

**KEPT (live; NOT deleted) + cross-seam FLAGS:**
- `test_w093_usage_modes.py` — LIVE (spatial usage-mode delegation). 50/50. Mine. KEEP.
- `test_a4_recompose_energy_calibration_round_trip.py` — **FLAG star-lord seam:** recorder-side `recompose_attempts` telemetry round-trip (v2.15), NOT deleted balance_loop convergence machinery. The dispatch's "recompose machinery is DELETED" premise does not hold for the recorder-side table; the balance_loop recompose LEVERS were explicitly NOT deleted in a8b28a1. LIVE, passes.
- `test_telemetry_v24.py` — **FLAG star-lord seam:** pure telemetry V2.4 migration (`modifier_flag_tier` on `class_balance_results`). 22/22. No balance_loop/fight_engine/recompose surface. LIVE.

**MIS-ROUTED FLAG (adjacent, not in my 14):** `test_cycle12_layer6_t4_wireup.py` — NO `fight_engine` import (`fight_engine_context` is a t4_wireup param name); fails on rocket's `SkillTreeGenerator.generate()` retirement (b6-stack G10). Rocket's seam — did NOT touch.

### Green-collection confirmation (my retained files)

`pytest --collect-only` on the 4 retained files: 121 tests collected, ZERO import-time failures. 9 deleted files gone. Live spatial suite + retained live tests: 99 passed.

**Close-B → jack-ryan Gate-2** (live repair + semantic-shift declaration + decisions-log entry for the spatial-instrument KPM repoint).

---

## Completion record — star-lord (Follow-on A, output-seam half)

**Completed:** 2026-06-16
**Agent:** star-lord
**Tag:** `star-lord/v1.1-legacy-test-sweep`

### Decision: PRESERVE (no changes made)

`tests/test_cycle11_schema_extensions_round_trip.py` does NOT import `season_writer`, `summary_formatter`, or `SeasonOutput`. Its imports resolve entirely against live production symbols:
- `reincarnated.export.schemas` — `ExportAlterationOutput`, `ExportClass`, `ExportWeaponDescriptor`
- `reincarnated.export.season_exporter` — `_build_alteration_output`, `_build_weapon_descriptor`, `_validate_stage_b_classes`, `export_season`

Both import paths resolve cleanly. The file collects at 40 tests and passes all 40 (0.13s). The dispatch listed it as a `season_writer`-importing failure — inspection shows this was a false positive from the grep sweep; this file never imported the deleted module. No changes made; file preserved as-is.

**Smoke test result:** `40 passed in 0.13s` — clean.

### Output-seam scope scan (per scope guard)

Scanned for other output-seam test files referencing deleted symbols (`season_writer`, `summary_formatter`, `SeasonOutput`, `write_season`, `format_summary`). Files found with deleted-symbol references:

- `test_b6_generator_wired.py` — on rocket's gen sweep (dispatch §Follow-on A rocket list). Correctly routed.
- `test_cosmological_vocabulary.py` — on rocket's gen sweep. Correctly routed.
- `test_cp8_gear_naming.py` — on rocket's gen sweep. Correctly routed.
- `test_gear_integration.py` — on rocket's gen sweep. Correctly routed.
- `test_integration.py` — on rocket's gen sweep. Correctly routed.
- `test_spirit_guide_orchestrator_wiring.py` — on rocket's gen sweep. Correctly routed.
- `test_range_profile.py` — on gamora's 1D-sim sweep. Correctly routed.
- `test_role_orientation.py` — on gamora's 1D-sim sweep. Correctly routed.

No mis-routed output-seam orphans found. All failing files with deleted-symbol imports are already assigned to rocket or gamora per the dispatch.

---

## Completion record — rocket (Follow-on A, generation-seam half)

**Completed:** 2026-06-16
**Agent:** rocket
**Tag (intended; NOT pushed — Matt-gated at close):** `rocket/v1.1-legacy-test-sweep`
**Status:** COMPLETE. All 36 assigned files dispositioned. `pytest --collect-only` on my retained files = ZERO import-time errors.

### Tally (36 = 10 DELETE + 20 EXTRACT + 6 KEEP-UNTOUCHED)

**DELETE OUTRIGHT — 10** (entirely deleted-module coverage; no salvageable live coverage):
test_b6_generator_wired, test_class_generation, test_d3_archetype_composer, test_wind_controller_dps_floor, test_integration, test_combat_simulator, test_cycle12_wave5_sim_combatant_integration, test5_multishot_stability, test_spirit_guide_orchestrator_wiring, **test_gear_cp6**.
- test_gear_cp6 imports `class_generator` at MODULE TOP LEVEL → ERRORED at collection; un-extractable (deleted producers needed throughout); its live content is gamora balance_loop → deleted to clear the collection error + FLAGGED to gamora.
- test_combat_simulator + test_cycle12_wave5_sim_combatant_integration also imported the deleted 1D `simulate_fight` → dead on the 1D-sim axis too.
- test_spirit_guide_orchestrator_wiring: 12/13 tests were dead SeasonOrchestrator wiring; the 1 live test (`build_spirit_guide_prompt` token budget) is star-lord's llm seam → FLAGGED to star-lord rather than authoring a near-empty file holding another seam's single test.

**EXTRACT (drop dead imports/fixtures/test-classes, preserve live) — 20:**
test_embodiment_axis_schema, test_movement_speed_schema, test_grouping_layer_schema, test_gear_cp3, test_gear_cp5b, test_b11_geometry_palette, test_naming, test_no_canonical_four_in_llm_prompts, test_cosmological_vocabulary, test_role_registry, test_canonical_loadouts, test_cp8_gear_naming, test_cp9_gear_telemetry, test_d2_substrate_coupling, test_telemetry_tier1, test_telemetry_v21, test_bc_target_subspace_generator, test_dodge_gated_flag_defer, test_stage2_bc_keying, test_spirit_guide.
- Notable preservations: test_b11 re-pointed `AOE_GEOMETRIES` → `geometry_constants` (the only re-homed geometry set; the other 4 b6 geometry sets were NOT re-homed → their tests dropped). test_gear_cp5b/test_gear_cp3 replaced deleted-ClassGenerator class fixtures with `_StatsOnlyClass`/`_MinimalFireMage` duck-typed stand-ins. test_cp9 inlined the deleted `_GEAR_POOL_PER_SLOT_TIER` (=10) to keep two live MECHANICS_ONLY gear-pool tests.

**KEEP UNTOUCHED — 6** (named by name-pattern but import only the LIVE `simulation.wave5_season_orchestrator` + live generation; collect clean; ZERO deleted-module refs — over-included by the grep sweep):
test_cascade_r3_s3_archive_variant_preservation, test_cascade_r3_s5b_wave_b_orchestrator_integration, test_cascade_r4_followon_wave_b_persistence_plus_wave_s_integration, test_cascade_r4_path_x_pm1_input_source, test_cascade_r4_track_a_season_production, test_wave5_swift_closure_path_x_phase4_feeds_phase5.

### Cross-seam FLAGS (live coverage of another seam dropped from my files; owning seam decides whether to rebuild with a substitute producer)

**To gamora** (balance_loop / from_player_class / spirit_guide integration needing a PlayerClass producer that no longer exists in-seam):
- test_gear_cp6 (ENTIRE FILE) — BalanceLoop gear-convergence: run_batch_geared / _evaluate_class / balance_class / balance_trial.
- test_dodge_gated_flag_defer — dropped the 3 integration classes (2026-06-15 dodge-gated two-door flag-and-defer `balance_class` coverage). Predicate unit tests preserved.
- test_stage2_bc_keying — dropped TestProductionPathRoundTrip (bc_target → from_player_class → CombatantState). Pure-fn bin-keying preserved.
- test_spirit_guide — dropped TestQuickSimulate (SpiritGuide.quick_simulate e2e). Other 3 SpiritGuide groups + helpers preserved.
- test_telemetry_tier1 (TestBalanceLoopFightLogFields), test_telemetry_v21 (TestBalanceLoopV2FightLog + TestRecorderPersistsV2FightLog), test_canonical_loadouts (TestFightLogLoadoutCapture + TestCarriedGearPopulation + TestCanonicalLoadoutSanityCheck) — balance_class fight_log/carried-gear integration. The schema-migration + recorder-persistence on synthetic rows is preserved in-file.

**To star-lord** (llm seam): test_spirit_guide_orchestrator_wiring's lone live test — `test_spirit_guide_voice_prompt_token_estimate` on `llm.spirit_guide_voice.build_spirit_guide_prompt`. Re-home into an llm test if wanted.

### Out-of-scope collateral collection failure → FLAG to knight-rider (NOT touched)
- tests/test_cycle12_layer3_skill_tree.py — NOT named in this dispatch (not mine / gamora's / star-lord's). Fails collection on `from reincarnated.generation.skill_tree import _ARCHETYPE_TEMPLATES` (symbol no longer on the live skill_tree module — b6-deletion collateral). Per scope guard, left untouched; needs routing. After my sweep this is the ONLY remaining collection error in the full `tests/` tree: `4740 tests collected, 1 error`.

### Pre-existing (NOT sweep-introduced) run-time failure observed, left untouched
- tests/test_d2_substrate_coupling.py::TestValidSlotsRegistryDriven::test_get_valid_slots_with_foundation_returns_registry — asserts canonical-four but config now has 7 rotating elements (holy/lightning/shadow). Verified failing identically at HEAD with the sweep stashed → config-drift, unrelated to the b6/1D deletion; outside this dead-import sweep's scope.
- (One trivial test-only fix WAS applied: test_no_canonical_four_in_llm_prompts used invalid archetype "bruiser" — a latent bug masked while the file failed to collect — corrected to "brute" so the preserved live coverage passes.)

### Verification
- `pytest --collect-only` on my 35 retained files: 725 tests, 0 errors.
- Full `tests/` collect-only: `4740 tests collected, 1 error` (the out-of-scope test_cycle12_layer3_skill_tree only).
- Running the non-DB-heavy retained set: 583 passed, 1 failed (the pre-existing d2 config-drift failure only).

### Notes
- Disposition rationale: `reincarnated-engine/src/reincarnated/generation/notes/legacy-test-sweep-disposition-2026-06-16.md`.
- `tests/test_dodge_gated_flag_defer.py` was UNTRACKED at HEAD (new file from the recent 2026-06-15 dodge-gated feature, not yet committed). My extracted version is staged with this commit. Its companion math note `2026-06-15-dodge-intrinsic-glass-close-st-math-note.md` (not mine) is left untracked.
- jack-ryan confirms GREEN COLLECTION across the full suite at close (the lone remaining error, test_cycle12_layer3_skill_tree, is out-of-scope and flagged to KR).

### Addendum — straggler disposition (rocket, 2026-06-16, KR-routed)
`tests/test_cycle12_layer3_skill_tree.py` (the lone remaining collection error after the three A/B sweeps) DISPOSITIONED: **EXTRACT** (mixed dead+live). Dropped Gate 1 / Gate 2 / Gate 5 / Gate 6 / EdgeCases — all drove trees via the retired `SkillTreeGenerator.generate()` and/or the deleted `_ARCHETYPE_TEMPLATES` dict. Preserved Gate 3 (`substrate_templates` shape + JSON round-trip) + Gate 4 (`off_hand_contract` SC-3 shapes) — both exercise live modules + the live `BC_AXIS_KEYS` constant the skill_tree module survives for. Result: 15 live tests collect+pass (0.11s). **Full-tree `PYTHONPATH=src python3 -m pytest tests/ --collect-only -q` = 4755 collected, ZERO errors** (was 4740 + 1 error). GREEN COLLECTION achieved. Scope-guard honored: only this one test file touched, no production code.
