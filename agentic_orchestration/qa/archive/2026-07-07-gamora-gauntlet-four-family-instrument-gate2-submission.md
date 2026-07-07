# Gate-2 Submission — 2026-07-07 — Q11 four-family gauntlet instrument (Lane 1 build)

**Submitter:** gamora (simulation seam)
**For review by:** jack-ryan (DEV-MODE Gate-2, BLOCK authority)
**Disposition requested:** Gate-2 review of the code + config change to the certification instrument
**Target tag:** `gamora/v-batch2-gauntlet-four-family-instrument-1` (commit `8d45f95`) — **NOT pushed** (Matt-gated)
**Math/design note (Discipline #1, committed FIRST):** `simulation/math/gauntlet-four-family-instrument-build-2026-07-07.md` (commit `657524a`)
**Governing:** dispatch `agentic_orchestration/dispatches/2026-07-07-gamora-gauntlet-four-family-instrument-build.md`; spec `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` (RATIFIED Q11 R1–R5); fire order `agentic_orchestration/gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md` §2 Lane 1

> **Lane-3 dependency (flag for KR/jack-ryan):** jack-ryan's Lane-3 metrology (bar derivation, spec §6) depends on THIS build landing — the four family arenas + registries are the instrument the bars derive on. This build produces the INSTRUMENT; it does NOT set bars.

---

## What this build does (scope, per dispatch)

Instrument construction only. NO bar derivation (Lane 3), NO re-pilot (resumed Step 3), NO F-fork adjudication, NO constant changes (`SPATIAL_DAMAGE_SCALE`, `MOB_HP_DIFFICULTY_MULTIPLIER`, KPM bands, seed ratios — all FROZEN and byte-unchanged).

1. **Four family arenas at spec §3 dims/populations** (`spatial_gauntlet/arena.py`):
   - **F1 `dense_cell`** — NEW canonical, 16×22m, ~24 (20 trash + 1 champion pack of 4, same-type magic-tier, no minions — D3 canon).
   - **F1 variants** — `chokepoint_corridor` re-populated 8→24 (funnel geometry kept); `magic_pack` re-roled champion-pack variant, +trash to 24.
   - **F2 `open_arena`** — RE-DIMENSIONED 50×50→36×36 AND re-populated 8→40 (28 free trash + 3 rare packs of 1 elite leader + 3 swarm minions; elite fraction 7.5%). THE saturation repair (dissolves the Step-1 8-mob ceiling defect).
   - **F3 `boss_with_adds`** — carried as-is + 2 timed add-waves (R5, t=80s/160s, 2 elite adds each).
   - **F4 `escape_lane`** — NEW canonical, 60×16m directional lane, continuous-reinforcement spawner (k=3 / interval 1s / engaged_cap 50), champion-elevation ×2.0, `escape_reached` win at y≥58, fixed 60s window.
   - New registries: `FAMILY_SCENARIOS`, `FAMILY_CANONICAL`, `DIAGNOSTIC_SCENARIOS`.

2. **R4 — STR boss-shell carve-out RETIRED** (`gauntlet_sim.py`): `family_certification_pass()` (four-family conjunction, ≥1 passing member per family) is the end-state gate. `gauntlet_pass()` still routes the legacy 9-of-18 floor until Lane-3 bars land (design note §9 — the swap to `return self.family_certification_pass(cohort)` is the one-line flip Lane 3 makes once four-family bars are registered; this avoids silently breaking the paused Step-3 sequence before its bars exist). Four-family verdict exported via `to_dict()` (`families_passed` / `four_family_cert`). Carve-out comments (`:205-207`, eligible_encounters_passed docstring) demoted to reflect the retirement.

3. **§4 disposition — wall demoted, six rooms survive** (`arena.py`): OLD 50×50 8-mob `open_arena` preserved as diagnostic `open_arena_wall_diag` in `DIAGNOSTIC_SCENARIOS` (the Step-1 wall + A=43 anchor lineage). Nothing deleted.

4. **Engine plumbing** (`spatial_engine.py`): F4 continuous spawner + F3 timed-wave injection (mid-fight mob-list growth via `_spawn_reinforcement`, engaged_cap rail, seeded-deterministic per Discipline #3), `escape_reached` win condition + forward-to-exit navigation, champion-elevation at the `spatial_dm` seam (NO constant change), assert relaxed for continuous scenarios. All default-OFF → six existing scenarios byte-identical.

## Cross-seam (MIGRATION.md v1.84 — star-lord telemetry boundary)

`SpatialFightResult` gains two additive/defaulted/brownfield-safe fields (`escape_reached: bool = False`, `continuous_spawned_total: int = 0`), following the established `total_displacement`/`boss_*` pattern (not `validate()`-enforced, not persisted by the SQLite `_INSERT_SQL` until a schema migration lands). Plus a Discipline-#12 range semantic-shift: `mobs_killed` is unbounded for F4 (continuous spawn). Full producer/consumer contract in `simulation/MIGRATION.md` v1.84. `winner` stays in the existing {player, monster, timeout} set (no validate() change).

## Discipline #12 semantic-shifts (framed, routed to jack-ryan decisions-log)

1. **R4 certification contract:** 9-of-18 count → four-family conjunction (STR boss failure now DISQUALIFYING, not carve-out-exempt).
2. **`open_arena` re-base:** what it MEASURES changes (8-mob 50×50 → 40-mob 36×36); bars re-derive on the new instrument (spec §6.2).
3. **`mobs_killed` range** unbounded for F4.

## Smoke (Discipline #2) — BUILD smoke, GREEN

`spatial_gauntlet/_build_smoke_four_family.py` — all four families instantiate + run a functional kit end-to-end without erroring ("does the room work," NOT a certification run, NO bar comparison). Verified mechanisms:
- F4 spawner FIRES (27–38 reinforcements minted) + `escape_reached` resolves to player win.
- F4 mob population grows 12→50 (engaged_cap rail) — the 8-mob no-respawn ceiling the Step-1 finding located is LIFTED by construction.
- F3 timed waves inject (mob list grows 3→7 mid-fight, verified in a pinned run).
- AOE engagement fires in all rooms (aoe_hits > 0 → mobs reach player, geometry lands).
- Brownfield-safe: `elite_pack`/`mini_boss` carry no spawner/elevation; wall diagnostic preserved and not in any family.

**Discipline #11 empirical note for the reviewer:** `mobs_killed == 0` in the build smoke is a smoke-FIXTURE DPS artifact — it reproduces on the KNOWN-GOOD `elite_pack`/`magic_pack` at the same harness (the flat synthetic-mob DPS path does not kill in-window). It is a Lane-3 / DPS-calibration concern, NOT a room-build signal. The build smoke validates rooms-run-end-to-end + engagement + spawner + escape + waves, not kill counts.

## Regression — 254 tests pass across 8 spatial suites

`test_spatial_gauntlet_scenarios` (27), `round_trip_spatial_telemetry`, `test_w093_usage_modes`, `test_w094_performance`, `test_w095_telemetry`, `test_w010_boss_ai_focus`, `test_wd_spatial_bc_measurement`, `test_telemetry_v23`, `test_cycle13_wave5_gauntlet_sim` (49). Two tests updated to the new instrument: `magic_pack` composition (4→24, F1 champion-pack variant); `open_arena` mob-dict helper (8→`scenario.mob_count`, tracks the re-population).

## Compute-cost estimate (Discipline #1.1)

Peak ~51 concurrent live entities (F4 engaged_cap 50 + player) on an 8 GB host — no bounds risk (small dataclasses ≪ RAM; engaged_cap is the memory rail). Full-instrument at production N ≈ ~53 min worst-case (Lane-3 planning; smoke-first per Discipline #2). Per-family build-smoke costs (a few fights) are sub-second to ~1s — in-session (below Discipline #19 detached threshold).

## Suggested review focus (BLOCK candidates)

- The R4 sequencing choice: `gauntlet_pass` keeps the legacy floor while `family_certification_pass` encodes the retired-carve-out contract (does this correctly avoid breaking the paused Step-3 sequence, and is the one-line-flip handoff to Lane 3 clean?). Design note §9.
- The MIGRATION v1.84 field additions + `mobs_killed` range shift (star-lord boundary — is the additive-field pattern honored and the range-shift adequately flagged?).
- The one-spatial-contract adherence: §3 dims read verbatim (16×22 / 36×36 / ~30 / 60×16), no runtime re-determination. Did I introduce any dim the spec did not author? (I did not; escape_threshold 58m and elevation ×2.0 are instrument PARAMETERS of the F4 room, not room DIMS.)
- Champion-elevation ×2.0 and F4 window 60s / cadence k=3/1s — these are instrument PARAMETERS (design note §4), NOT bars. Confirm they are not smuggling a pass/fail threshold.

## References

- Tag/commit: `gamora/v-batch2-gauntlet-four-family-instrument-1` (`8d45f95`); math note commit `657524a` — neither pushed
- Files: `spatial_gauntlet/arena.py`, `spatial_gauntlet/spatial_engine.py`, `spatial_gauntlet/spatial_telemetry.py`, `spatial_gauntlet/_build_smoke_four_family.py`, `gauntlet_sim.py`, `simulation/MIGRATION.md` (v1.84), `simulation/AGENT_STATE.md` (SESSION 52), `tests/test_spatial_gauntlet_scenarios.py`, `tests/test_w094_performance.py`
- Math/design note: `simulation/math/gauntlet-four-family-instrument-build-2026-07-07.md`
- Spec: `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3/§4/§5/§7/§8
- Step-1 defect this repairs: `simulation/notes/caster-bar-rederivation-2026-07-07.md`

**Signed:** gamora, 2026-07-07 — Lane 1 instrument BUILD complete + build-smoke green. Requesting Gate-2. Lane-3 metrology depends on this landing.
