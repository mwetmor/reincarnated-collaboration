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
