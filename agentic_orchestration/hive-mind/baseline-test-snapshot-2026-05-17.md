# Baseline Test-Suite Snapshot — 2026-05-17

**Author:** jack-ryan  
**Captured at:** `hive/v0.0-pre-phase-1-p1` baseline (engine HEAD `f9c363e`) + post-activation commits (`93118f0` current HEAD)  
**Purpose:** Reference snapshot for drift detection. Future test-suite runs compared against this.  
**Run date:** 2026-05-17  

**Note on timing:** The baseline tag is at `f9c363e`, but 4 commits have already landed since activation (gamora D7 math note + AGENT_STATE; star-lord D6 scoping doc + AGENT_STATE). These are documentation-only commits with no code changes. Test suite state is identical between `f9c363e` and `93118f0`.

---

## § 1 — Engine test suite

### § 1.1 — Summary

| Metric | Value |
|---|---|
| Total tests collected | 2098 |
| Total PASSED | 1988 |
| Total FAILED | 3 (pre-existing) |
| Total ERRORS | 0 |
| Wall time (full suite) | ~26 min 22 sec |
| Wall time (fast suite, no integration) | ~60 sec |
| Python | 3.12.0 |
| pytest | 9.0.3 |
| Engine HEAD at capture | `93118f0` (4 commits ahead of hive baseline `f9c363e`) |
| Suite status | **GREEN (with 3 documented pre-existing failures)** |

### § 1.2 — Pre-existing failures (3)

These failures were present at `hive/v0.0-pre-phase-1-p1` baseline and are documented in scope-of-work § 4.2 as pre-Phase-1 P1 technical debt.

| Test | File | Failure reason |
|---|---|---|
| `TestGearInCombatIntegration::test_geared_player_deals_more_damage` | `tests/test_gear_cp3.py:508` | `AssertionError: assert 1.0 > 1.0` — boundary condition at 100% win rate; assertion is `a_win_rate > 1.0` which is logically impossible (rates are capped at 1.0). Likely assertion-authoring bug (should be `>= 1.0` or comparing different metrics). |
| `TestAbilityTraitWiringInFightEngine::test_cooldown_factor_applied_in_fight` | `tests/test_gear_cp5.py:347` | `assert 13 >= 18` — test expects ≥18 cooldown-affected actions but fight produces 13. Likely a fight-duration or cooldown-factor magnitude assumption that has drifted from current implementation. |
| `TestQuickSimulate::test_weak_fit_against_impossible_opponent` | `tests/test_spirit_guide.py:686` | `assert strong_fit == weak_fit` — spirit guide's `quick_simulate()` returns `strong_fit` when test expects `weak_fit` for a nominally impossible opponent. Likely a balance-loop change caused a gear/fit boundary to shift. |

**These 3 failures are the BASELINE.** Any newly failing test above this count signals Phase-1 P1 induced regression.

### § 1.3 — Test count by subdirectory / concern area

Approximate breakdown by test file category (collected from file listing):

| Category | Files | Approx test count |
|---|---|---|
| Gear / combat integration | test_gear_cp*.py (9 files), test_gear_integration.py, test_gear_generation.py, test_gear_schema.py | ~400 |
| Simulation / balance | test_balance_loop.py, test_combat_simulator.py, test_gate3b_ms_consumption.py, test_wind_controller_dps_floor.py | ~180 |
| Generation / archetype | test_b6_generator_wired.py, test_canonical_loadouts.py, test_class_generation.py, test_monster_generation.py, test_ability_grammar.py | ~250 |
| Element / foundation | test_element_selector.py, test_foundation.py, test_substrate_identity_loader.py, test_energy_types.py, test_range_profile.py | ~230 |
| Integration (end-to-end) | test_integration.py, test_canonical.py | ~250 |
| Export / telemetry | test_export.py, test_telemetry_*.py (5 files), test_recorder_fail_loud.py | ~200 |
| LLM / naming | test_naming.py, test_cosmological_vocabulary.py, test_grouping_layer_schema.py, test_no_canonical_four_in_llm_prompts.py, test_spirit_guide.py | ~150 |
| Schema / misc | test_embodiment_axis_schema.py, test_movement_speed_schema.py, test_b11_geometry*.py, test_role_orientation.py, test_skill_composition.py, test_wave_composition_rules.py, test_cp*.py | ~200 |
| **TOTAL** | 57 test files | **2098** |

### § 1.4 — Substrate identity loader tests (D1-relevant)

`test_substrate_identity_loader.py` — 107 tests, **all PASS**.

Critical finding: the substrate identity loader (`src/reincarnated/foundation/substrate_identity_loader.py`) and all 7 YAML declarations (`config/substrate_identities/*.yaml`) EXIST on disk and pass 107 tests, but are **untracked in git** (rocket has authored D1 in working tree but not yet committed). The 2098 test total INCLUDES these 107 tests running against the working-tree loader.

**Drift-detection implication:** If rocket commits D1 and the loader shape changes, the 107 tests provide the conformance gate.

---

## § 2 — Loadout test suite

### § 2.1 — Summary

| Metric | Value |
|---|---|
| Test runner | vitest |
| Total tests | 23 |
| PASSED | 21 |
| FAILED | 2 (pre-existing) |
| Wall time | ~297 ms |
| Loadout HEAD at capture | `90db544` (hive baseline) |
| Suite status | **DEGRADED (2 pre-existing failures — jest API used in vitest context)** |

### § 2.2 — Pre-existing failures (2)

Both failures are in `src/__tests__/cipher-no-leak.test.ts`:

| Test | Failure |
|---|---|
| `warns for v1.5 manifest missing seasonal_elements (fail-loud)` | `ReferenceError: jest is not defined` at line 163 |
| Related test (same file) | Same `jest.spyOn` call |

**Root cause:** Two tests use `jest.spyOn` which is a Jest API, but the loadout project uses vitest. These were likely authored against a different test-runner expectation. The `jest` global is not injected by vitest by default.

**Scope-of-work § 4.2 note:** This gap was noted in the hive invocation as "drax cipher-no-leak.test.ts gap." Pre-existing; not a Phase-1 P1 regression.

**Fix path (for drax):** Replace `jest.spyOn(console, 'warn')` with `vi.spyOn(console, 'warn')` from vitest. Drax can fix during Phase-1 P1 loadout work.

---

## § 3 — Demo test suite

### § 3.1 — Summary

| Metric | Value |
|---|---|
| Test runner | vitest |
| Total tests | 326 |
| PASSED | 326 |
| FAILED | 0 |
| Wall time | ~606 ms |
| Demo HEAD at capture | `0e4599b` (`drax/v0.20.9` hive baseline `692c555`) |
| Suite status | **GREEN** |
| TypeScript build | CLEAN (tsc --noEmit exits 0) |

Demo test suite is fully GREEN at hive baseline. This is the cleaner baseline of the two front-end suites.

---

## § 4 — MIGRATION.md baseline state

Per coordination-matrix § 4, each seam maintains a MIGRATION.md. Baseline state at hive activation:

| Seam | Path | Present | Last entry |
|---|---|---|---|
| rocket (generation) | `src/reincarnated/generation/MIGRATION.md` | YES | 2026-05-16 — wind_controller DPS floor (no schema-shape change) |
| rocket (element) | `src/reincarnated/element/MIGRATION.md` | YES | 2026-05-17 — Drift-14 pool-cull + D1 rubric selector (5 new PoolElement fields, all additive) |
| gamora (simulation) | `src/reincarnated/simulation/MIGRATION.md` | YES | 2026-05-16 — B10 V2 sequential-room semantics (RoomResult dataclass + new telemetry fields) |
| star-lord (export) | `src/reincarnated/export/MIGRATION.md` | YES | 2026-05-14 — gear_pool.json per-item stats (ExportGearItem v1.1, additive) |
| drax (loadout) | `reincarnated-loadout/MIGRATION.md` | **NO** | Absent. Drax v0.21 cipher consumption (Stage 3) was documented in loadout AGENT_STATE and in star-lord's export MIGRATION.md, but no standalone loadout MIGRATION.md exists. |
| drax (demo) | `reincarnated-demo/MIGRATION.md` | **NO** | Absent. |

**Gap noted:** Both drax MIGRATION.md files are absent. Phase-1 P1 will introduce cross-seam contract changes (D17 Court vessel browser surface; D19 VFX rendering; D21 substrate browser; D22 embodiment display) that require drax MIGRATION.md authoring. Per coordination-matrix § 4, these must be created concurrent with drax's producing work. Jack-ryan watchpoint established.

---

## § 5 — Cross-seam contract checkpoints

Known cross-seam contracts at baseline and their current status:

| Contract | Producer | Consumer | Current state |
|---|---|---|---|
| `PoolElement` schema (`element/schema.py`) | rocket | gamora, star-lord, drax | 5 new fields added (Drift-14 v1.4 SHIPPED); star-lord Coupling #9 (`telemetry/recorder.py`) NOT YET updated to iterate registry (backlog for D2) |
| `Element.identity: SubstrateIdentity` field | rocket (D1) | gamora (D7+), star-lord (D6+), drax (D21+) | **WORKING TREE ONLY** — loader authored, 7 YAMLs authored, 107 tests pass, not yet committed. Consumers cannot yet consume (rocket must commit first). |
| `gamora/simulation/math/resistance-matrix-7x7-phase-1-p1.md` (D7 math note) | gamora | jack-ryan (review) | COMMITTED at `45a6014`. Math-before-code Discipline #1 satisfied. Code phase BLOCKED on jack-ryan review + rocket D1 commit. |
| `src/reincarnated/llm/PHASE-1-P1-REFACTOR-PLAN.md` (D6 plan) | star-lord | gandalf (D20 sequencing), knight-rider (scope tracking) | COMMITTED at `93118f0`. Plan phase complete. Implementation BLOCKED on gandalf D20 (grouping-vocab extension). |
| `ExportGearItem` schema v1.1 | star-lord | drax (loadout) | SHIPPED `a08bd6e`; drax v0.21 consumed (MIGRATION.md v1.2 referenced in drax AGENT_STATE). |
| `SeasonManifest` v1.5 fields (`seasonal_elements`) | star-lord | drax (loadout) | SHIPPED Stage 3 cipher migration `19d8ba0`; drax v0.21 consumed. 2 loadout tests partially broken (jest API issue). |

---

## § 6 — Hive activation progress state

At time of snapshot (2026-05-17, after hive activation):

| Deliverable | Status | Notes |
|---|---|---|
| D1 — Substrate identity loader | IN PROGRESS (working tree; not committed) | 107 tests pass on-disk; rocket has authored YAMLs + loader; commit pending |
| D7 — Resistance matrix math note | COMMITTED (`45a6014`) | Disciplines #1/#12/#13/#14-candidate all cited; jack-ryan review pending |
| D6 — LLM prompt structure refactor PLAN | COMMITTED (`93118f0`) | 9 call-site inventory; revised estimate 7-10 days; open questions for gandalf |
| D11 — Pool D1 re-score | SHIPPED (`rocket/v1.4-drift14-pool-cull-and-selector-amendment-1 @ 65e6d77`) | Counts as D11; no further work |
| D27 — Perception test session-runner | IN PROGRESS (drax-demo; active) | drax STATE entry at 09:00Z; architecture decided (standalone HTML runner) |
| All others | NOT STARTED | Awaiting D1 commit (critical path); or awaiting sequencing unblocks |

---

*Authored 2026-05-17 by jack-ryan. Reference baseline for Phase-1 P1 test-suite drift detection. Append successor snapshot files as named `baseline-test-snapshot-YYYY-MM-DD.md` on significant drift-check occasions.*
