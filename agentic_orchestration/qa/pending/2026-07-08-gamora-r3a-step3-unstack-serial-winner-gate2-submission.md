# Gate-2 SUBMISSION — 2026-07-08 — gamora R3a step 3: MOB_HP un-stack + serial-engagement + winner-tally

**Submitter:** gamora (simulation seam)
**For:** jack-ryan Gate-2 (DEV-MODE, post-output; BLOCK authority)
**Governing dispatch:** `agentic_orchestration/dispatches/2026-07-08-gamora-r3a-step3-unstack-serial-engagement.md` (§6 fork PRE-RULED A/YES/YES, Matt 2026-07-08)
**Tag:** `gamora/v-r3a-step3-unstack-serial-engagement-1`
**Boundary call (Principle 6 / ADR-004):** WITHIN-SEAM. **NO MIGRATION.** D3 landed as in-JSON gamora-side aggregate, no star-lord boundary crossed.
**Disciplines applied:** #1 (math-before-code — 4 notes), #1.1 (resource projection), #2.1 (smoke), #11 (attribution — the `1.5→1.25` log remedy DISPROVEN, not applied), #12 (semantic shift, framed), #23 (framing-audit on D2 math).

---

## The coordinated set (all within-seam, one tag)

### D1 — un-stack `MOB_HP_DIFFICULTY_MULTIPLIER` from the endgame-BC gauntlet path (Option A)
- **Change:** `run_spatial_fight` gains `apply_mob_hp_difficulty_multiplier: bool = True` (default = every existing caller BYTE-IDENTICAL). Internal gate: `flag AND scenario_id in MOB_HP_DIFFICULTY_SCENARIOS`. The endgame-BC path (`t4_sim_cycling._w4g_run_fight_batch`) passes `False`.
- **`arena.py:49 = 1.5` UNTOUCHED** — scope-retirement of a STACKING, NOT a constant move. Legacy convergence instrument keeps its ×1.5.
- **Budget effect:** open_arena/chokepoint swarm eff-HP 39,750→26,500 (÷1.5, −33%). magic_pack unchanged (never in scope — this is why the log's `1.5→1.25` remedy was structurally incapable, Disc #11).
- **Math note:** `simulation/math/r3a-d1-mob-hp-unstack-endgame-2026-07-08.md`.

### D2 — serial-engagement (pack-local activation) for open_arena + magic_pack
- **Change:** new `CombatantState.is_activated` (latching) + `serial_activation_radius_m`, gated behind `run_spatial_fight(serial_engagement=True)`. Activation gate in `_navigate_entity` (hold-at-spawn until player within R) + no-attack-while-unactivated in the mob action phase. Endgame path passes `True`.
- **Radii (gamora-derived from geometry, framing-audit Disc #23):** open_arena **12m** (peak concurrent ~4; ~3-4 bites), magic_pack **9m** (shallow 14m room; peak ~8-9; ~3 bites). Set on the two ArenaScenario objects only; chokepoint/elite/boss/legacy = None (inert, byte-identical).
- **LEASH decision:** did NOT re-base the shared `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0` — it is shared by three incompatible-geometry rooms (chokepoint OUT OF SCOPE). The activation gate SUBSUMES the concern in the two in-scope rooms (magic: 35m never fires in a 35.6m-diag room; open: fires only on full-room-flee = genre-correct reset). Shared-constant re-base is REPORTED as a chokepoint-scoped follow-on, not fixed.
- **Math note:** `simulation/math/r3a-d2-serial-engagement-2026-07-08.md`.

### D3 — winner-tally recording flip (BOUNDARY: within-seam, NO MIGRATION)
- **Change:** `StratumFightBatch.winner_tally` property ({player=b_dead, monster=a_dead, timeout=timeout}) + `GauntletEncounterResult.tier_2_winner_tally` field + `to_dict` + assignment at the tier-2 site. In-JSON gamora-side aggregate of `FightSummary.termination_reason` (a value the sim already owns).
- **Boundary call:** I confirm gandalf §5.2-AMEND lean — no star-lord export boundary crossed, no `spatial_fight_results` DB column, **NO MIGRATION**. Did NOT flag KR for star-lord.
- **Math note:** `simulation/math/r3a-d3-winner-tally-recording-flip-2026-07-08.md`.

## Smoke results (Disc #2.1)
`simulation/scripts/gamora_r3a_step3_unstack_serial_winner_smoke_2026_07_08.py` — **PASS/PASS/PASS**:
- D1: open+chokepoint factor-drop = 1.5 on un-stack; magic_pack = 1.0 (unchanged). Legacy build shows 39,750; endgame 26,500.
- D2: open_arena 4/40 active at tick-0 (== geom within 12m); magic_pack 10/24 (== geom within 9m) — staged, NOT whole-field. Activation matches geometry exactly.
- D3: winner_tally {player:3, monster:2, timeout:1} sums to 6, surfaced in `to_dict`.

## Regression (Disc #11 — legacy byte-identical claim)
- `test_spatial_gauntlet_scenarios` + `test_cycle13_wave5_gauntlet_sim`: **77 passed**.
- `test_wd_spatial_bc_measurement` + `round_trip_spatial_telemetry`: **87 passed**.
- E2E: 3-fight open_arena + magic_pack ran clean on BOTH endgame (un-stacked+serial) and legacy (default) paths.

## Resource projection (Disc #1.1)
Step-4 re-run: **~25-35 min, <5MB peak** — same class as R2 (~25 min, <5MB). D1 (down) / D2 (up) partly offset; 120s cap unchanged. Note: `simulation/math/r3a-step3-resource-projection-2026-07-08.md`.

## Scope discipline (out-of-scope non-goals honored)
NO ×1.5 constant move; NO content/kit re-tune (rider 4); NO Lever-4 change; NO step-4 run (KR fires); NO leg-3 wire/chassis/bars/bands/kit touches; NO multiplier extension to magic_pack.

## Files changed (all gamora seam)
- `simulation/spatial_gauntlet/spatial_engine.py` (D1 gate + flag; D2 activation gate + no-attack + mob-build stamp)
- `simulation/spatial_gauntlet/arena.py` (D2 ArenaScenario field + open_arena=12m / magic_pack=9m)
- `simulation/t4_sim_cycling.py` (D1+D2 flags at `_w4g_run_fight_batch`; D3 `winner_tally` property)
- `simulation/gauntlet_sim.py` (D3 `tier_2_winner_tally` field + to_dict + tier-2 assignment)
- 4 math notes + 1 smoke + AGENT_STATE.md update
