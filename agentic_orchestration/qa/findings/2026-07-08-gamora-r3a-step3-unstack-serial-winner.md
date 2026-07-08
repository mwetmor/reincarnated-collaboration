# Finding — 2026-07-08 — gamora R3a step-3 (MOB_HP un-stack + serial-engagement + winner-tally)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2)
**Severity:** INFO (verdict: **PASS**)
**Target:** tag `gamora/v-r3a-step3-unstack-serial-engagement-1` — engine commit `e649659`
**Developer:** gamora (simulation seam)
**Principles applied:** #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact / ADR-004 boundary), #5 (severity)
**Disciplines cited:** #1, #1.1, #2.1, #11, #12, #23. **Governance:** ADR-002 (tiered approval), ADR-004 (MIGRATION), rider-4/5 (Goodhart).

## What I found
Execution is correct on all six BLOCK-triggers. This gate tested EXECUTION, not the (already-ruled A/YES/YES) design. Verified empirically against the checked-out tag, not from the submission narrative. All three deliverables PASS; no conditions.

**D1 — un-stack (Goodhart guard, load-bearing): PASS.** `arena.py:49 MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` is genuinely UNTOUCHED — its last-change commit is `24cdc7e` (2026-05-19), not step-3. The un-stack is a clean caller-flag scope-retirement: `apply_mob_hp_difficulty_multiplier: bool = True` gated at `spatial_engine.py` as `flag AND scenario_id in MOB_HP_DIFFICULTY_SCENARIOS`. The ONE code caller passing `False` is `t4_sim_cycling.py:1236` (`_run_spatial_w4g_batch` — the endgame-BC gauntlet). Every other `run_spatial_fight` caller (legacy convergence via `ConvergenceUsageMode`, four-family metrology, martial-bar / armor-resist harnesses, economy pilot, smokes) uses the default → byte-identical. Scoping trigger #2 clears: legacy convergence instrument (the path the ×1.5 was ruled for) keeps ×1.5; no other endgame path reads the multiplier.

**D2 — serial-engagement: PASS.** `serial_engagement: bool = False` (default = legacy byte-identical). Radii live on the two ArenaScenario objects only (`open_arena=12.0m`, `magic_pack=9.0m`); the other scenarios leave `serial_activation_radius_m=None`. Both the movement activation gate (`_navigate_entity`) and the no-attack guard are `None`-guarded, so when off they are inert (no `continue`, mob pursues/attacks from tick-0 as before). LEASH constant `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0` genuinely reported-not-fixed — the only occurrence in the commit is in the commit MESSAGE, no code hunk touches it.

**D3 — winner-tally boundary: PASS (within-seam correct).** `StratumFightBatch.winner_tally` + `GauntletEncounterResult.tier_2_winner_tally` + `to_dict` + tier-2 assignment. Confirmed NO `write_fight_result` touch, NO `spatial_fight_results` DB column, NO export-schema field — the star-lord boundary is not crossed. Tally keys (`b_dead/a_dead/timeout`) match the `_term_for` mapping at `t4_sim_cycling.py:1241/1269` and the existing `survival_rate`/`void_timeout_rate` derivations. ADR-004: no boundary field moves → NO MIGRATION is the correct call. Within-seam = mine to approve (ADR-002).

**Math-note-first (Disc #1): PASS.** All 4 notes exist under `src/reincarnated/simulation/math/r3a-*-2026-07-08.md`. Arithmetic matches code: ÷1.5 = 39,750→26,500 (−33%); activation-radius→peak-concurrent derivation matches the smoke's staged counts; winner-tally shape sums-to-n by construction. (Submission cited paths without the `src/reincarnated/` prefix — citation shorthand, files are real; noted, not a defect.)

**Rider-4 honesty: PASS.** Commit touched exactly 10 files (2 code-adjacent dataclasses, 3 engine modules, 4 math notes, 1 smoke, AGENT_STATE). Zero kit/content/bar/band/chassis/wire/lever/leg-3 files. No content re-tuning to green a gate.

## Re-runs (empirical, this machine, on the tag)
- **Smoke** `gamora_r3a_step3_unstack_serial_winner_smoke_2026_07_08.py`: **PASS/PASS/PASS.** D1 open+chokepoint factor-drop 1.5 (39,750→26,500), magic_pack 1.0; D2 open 4/40 & magic 10/24 active@t0 (== geom within radius, staged not full-field); D3 tally sums to n, present in `to_dict`. Reproduced the submission's exact numbers.
- **Regression suite 1** (`test_spatial_gauntlet_scenarios.py` + `test_cycle13_wave5_gauntlet_sim.py`): **77 passed.**
- **Regression suite 2** (`test_wd_spatial_bc_measurement.py` + `round_trip_spatial_telemetry.py`): **87 passed.**
- Byte-neutrality confirmed by construction (default flags) + the legacy-path regression green.

Note: an initial broad `-k` collection surfaced 4 unrelated collection ERRORS (`grouping-layer-vocabulary.md` env-path, rocket/canonical seam) — NOT gamora's change and NOT the cited suites. Running the four cited suites by path is clean.

## Rationale
Disc #11 (byte-identical legacy claim) is substantiated: single flag-passing caller + 164 green regression tests + untouched constant. Disc #12 semantic-shift is framed in D1 §6 / D2 §5, not buried. ADR-004 boundary reasoning is sound (re-aggregation of an already-owned gamora-seam field into a gamora-seam JSON artifact). Goodhart rider-5 holds: no constant softened; the ×1.5 stays ruled for the legacy instrument.

## Action
- [x] jack-ryan: PASS. Cleared submission from `qa/pending/`. Within-seam set approved under ADR-002 (no cross-seam field, no new ADR).
- [ ] gamora: none required. Step-4 $0 gauntlet re-run is knight-rider's to fire.
- [ ] (tracking, NOT a condition) chokepoint-scoped `LEASH_DISTANCE_OVERRIDE_M_SWARM` re-base remains a REPORTED follow-on — carry to a future chokepoint-in-scope dispatch.

## References
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (D1 gate ~3452; D2 activation gate ~1093, no-attack guard ~2470, radius stamp ~3508)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (constant :49 UNTOUCHED; D2 field :356, open_arena :521, magic_pack :782)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` (winner_tally :291; flags passed :1236-1237; `_term_for` :1241/1269)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (D3 field :610, to_dict :648, assignment :1302)
- 4 math notes + smoke under `~/Games/reincarnated-engine/src/reincarnated/simulation/{math,scripts}/`
