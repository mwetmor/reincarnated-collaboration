# Dispatch — 2026-06-16 — gamora — DELETE the 1D battle sim + sim-side b6 handling

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-16 (relayed via gandalf dispatch to KR). **SETTLED — do NOT route back for design pushback or re-validation.**
**Estimated effort:** ~0.5–1 day (deletion + atomic balance_loop rewire + smoke)
**Acceptance:** `simulation/spatial_gauntlet/` is the SOLE battle simulation; `balance_loop.py` routes all battle through the 2D spatial path; the 1D kernel files are gone; engine imports + runs; spatial sim green. jack-ryan Gate-2 two-witness (clean-build + spatial-sim-still-green) passes.

## Context — this is a settled deletion, not a fork

Matt has RETIRED the 1D battle sim and the b6 archetype processes. Debate is closed. The 2D spatial sim IS the real battle simulation — proxy battle is wired into it and proxy is in the T4 capstones. The 1D sim is **genuinely superseded, not provisionally vestigial.** Cycle 14's loadout-blind, 1D-measured premise is what made it a nearly meaningless run.

**Read this carefully so you don't re-litigate:** your own `b6-deletion-prereq-B-g7-hold-sim` dispatch (2026-06-15) returned **HONEST_FAIL → "b6 STAYS."** That verdict is now **MOOTED** — it measured b6's value *through the 1D sim*, which is the wrong instrument. Matt's directive is precisely that the 1D-measured premise is retired. Do not treat the HONEST_FAIL as a blocker. It answered a question that no longer governs. **This deletion is NOT gated on cond.5, real-loadout re-measure, b6-parity, g7-hold-sim, or any prior gate.**

## Deletion surface (confirmed on disk; YOU pin exact file-vs-excise calls)

### DELETE (the 1D kernel + 1D estimation layer)
- `simulation/fight_engine.py`
- `simulation/proxy_combatant.py`
- `simulation/search_estimator.py`

### EXCISE 1D references (keep the module's non-1D function)
- `simulation/__init__.py`
- `simulation/verdict_types.py`
- `simulation/balance_loop.py` — the five 1D call sites gandalf flagged near `:2880 / :2939 / :3218 / :3663 / :3810` (verify exact lines; they drift)
- `simulation/damage_resolver.py`
- `simulation/effect_resolver.py`
- `simulation/combatant.py`

### EXCISE sim-side b6 handling
b6 appears in `damage_resolver.py / effect_resolver.py / balance_loop.py / combatant.py`. Remove the b6-specific path; keep each module's non-b6 function. Confirm against your own grep — KR's grep `b6` hit `damage_resolver / balance_loop / combatant` on the sim side.

### SURVIVOR
`simulation/spatial_gauntlet/` becomes the sole battle simulation.

## Clean-execution sequencing (HYGIENE, not a decision gate)

The 1D kernel is wired into `balance_loop.py` at the five call sites above. **Delete it ATOMIC-WITH (or immediately after) wiring the 2D spatial gauntlet as balance_loop's sole battle path**, so the engine never sits in a state where balance_loop calls a deleted kernel. This is "delete so it still runs," NOT "verify before deciding to delete." If the spatial path needs a thin shim at balance_loop to assume the role, **that shim is in-scope.** Look at `spatial_resolver_adapter.py` / `spatial_engine.py` as the assumption point.

## Keystone redirects (NOT orphaned)

The representative-loadout keystone (real loadouts; §6 = 6b-reference-at-T4-scope-magnitude, Matt-ruled 2026-06-16) now feeds the 2D SPATIAL sim, not the deleted 1D sim. Your node-investment wire (15/5, kills the 0.35× floor) carries forward into the spatial path **unchanged** — do not remove it. Rocket's gear materialization likewise carries forward.

## Preserve the design history (DELETE the code, ARCHIVE the why)

Stamp `STATUS: HISTORICAL` (do NOT delete) on the b6 + 1D math notes under `simulation/math/`:
- `b6-reshape-hot-caster-cell-construction-2026-06-15.md`
- `b6-reshape-scoping-per-tier-shape-degeneracy-signature-2026-06-15.md`
- `b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md`
- `m1-3-5-*` (search-estimator-related)
- any other `b6-*` / search-estimator math notes you own
A one-line stamp at top: `STATUS: HISTORICAL — documents the retired 1D-sim / b6-archetype process; superseded by the 2D spatial sim per Matt directive 2026-06-16.`

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**YES — cross-seam.** Removing sim-side b6 handling + the 1D kernel changes what the simulation seam consumes from generation (rocket) and emits to output (star-lord). **Write `simulation/MIGRATION.md`** documenting: (a) 1D kernel removed → spatial is sole path; (b) sim-side b6 handling removed → b6 archetype kits no longer specially handled; (c) any fight_log / loadout dict keys that change shape. This is the handoff rocket + star-lord read before their deletions. **You are the keystone — go first.**

## Sequencing across seams
1. **gamora (you) — FIRST.** Kernel delete + balance_loop spatial-rewire + sim-side b6 excise + MIGRATION.md.
2. rocket — generation b6 delete (reads your MIGRATION).
3. star-lord — output b6 excise (reads both MIGRATIONs).
4. jack-ryan Gate-2 across the full set.

## Out of scope (do NOT do)
- Do NOT touch generation b6 files (rocket's seam: `b6_archetype_templates.py`, `b6_kit_builder.py`, etc.).
- Do NOT touch `output/season_writer.py` (star-lord's).
- Do NOT re-run cond.5 / b6-parity / any prove-then-delete probe. The decision is made.
- Do NOT add proxy skills / proxy gear modifiers / Proxy-Commander profile — that is a SEPARATE forward-work dispatch sequenced after this.

## Tag intent
`gamora/v1.1-1d-sim-b6-deletion` (seam-prefixed; Matt promotes to milestone if he wants).

## Gate
jack-ryan Gate-2 on the deletion commits (two-witness: clean-build + spatial-sim-still-green after kernel removal). gandalf design-endorse NOT required for the deletion itself (Matt-settled); gandalf endorses survivor wiring if KR requests a design witness.

---

## Completion record — gamora — 2026-06-16

**Status:** COMPLETE. Two-witness Gate-2 PASS. Engine imports + runs; spatial sim green. HALTED for jack-ryan Gate-2 across the full cross-seam set (KR routes).
**Commit:** `a8b28a1` (engine repo). **Tag:** `gamora/v1.1-1d-sim-b6-deletion`. **NOT pushed** (Matt-gated).
**Math note (authored before code, Disc #1):** `simulation/math/1d-sim-b6-deletion-scoping-2026-06-16.md`.
**MIGRATION (cross-seam handoff for rocket + star-lord):** `src/reincarnated/simulation/MIGRATION.md` § v1.70.

### DELETED vs EXCISED
- **DELETED (4 files):** `fight_engine.py` (was already a deprecation tombstone shim re-exporting search_estimator), `search_estimator.py` (the ACTUAL 1D kernel — renamed from fight_engine in W-B), `proxy_combatant.py` (1D proxy entities), `batch_runner.py` (run_batch/run_batch_geared — thin loops over simulate_fight, no non-1D body; deleted as a 1D-kernel file in all but name).
- **EXCISED 1D refs:** `__init__.py` (removed simulate_fight/estimate_search_grade/run_batch from imports + __all__); `balance_loop.py` (5 call sites rewired, imports dropped); `bc_measurement.py` (deletion-marker on estimate_search_grade_bins; imports no deleted module); `combatant.py` (stale _is_trial comment); `spirit_guide/spirit_guide.py` (removed module-level fight_engine import).
- **EXCISED sim-side b6:** retagged the misleading `KI-B6-1` comments in `damage_resolver.py`/`effect_resolver.py` (a known-issue id for the modifier-range variance fix, NOT the b6 archetype) → `Prop 3 (per-hit damage variance)`. The variance ROLL is UNCHANGED + load-bearing for the spatial path. There is NO separable "b6 combatant battle path" in damage_resolver/effect_resolver/combatant — confirmed by empirical inspection (Disc #11). Sim-side b6-archetype-SPECIFIC logic is the recompose levers in balance_loop (ARCHETYPE_TEMPLATES/TIER_SCALING_BANDS), which feed the B14.5 recompose secondary loop — NOT touched (see cross-seam note).

### Atomic balance_loop rewire — SUCCEEDED
The 2D spatial gauntlet (`_run_spatial_slot` / new `_spatial_battle_slot` shim) is balance_loop's SOLE battle path for ALL tiers. Swarm was already spatial (W0.9.1); this extends spatial to magic/elite/mini-boss/boss and removes the 1D fallback. The engine is never in a state where balance_loop calls a deleted kernel (imports dropped + kernel deleted in one commit). The thin shim returns (win_rate, stub BatchResult) with synthetic FightResult rows reproducing the spatial WR so a_win_rate/a_wins/b_wins stay consistent for former 1D consumers.

### Two-witness Gate-2 result — PASS (evidence)
1. **Clean-build:** `python3 -c "import reincarnated.simulation"` (+ spirit_guide, balance_loop, t4_sim_cycling, gauntlet_sim, bc_measurement, combatant, damage_resolver, effect_resolver, verdict_types) → ALL import OK after kernel deletion.
2. **Spatial-green:** `python3 -m pytest tests/test_spatial_gauntlet_scenarios.py` → **27 passed in 0.23s** (exercises run_spatial_fight / SpatialFightEngine end-to-end).
   - NOTE: the legacy `scripts/r2_spatial_smoke.py` harness is non-runnable IN THIS ENV for PRE-EXISTING reasons UNRELATED to the deletion (proven by reverting all my work via git stash and reproducing the failure on clean HEAD): a `hash(class_id)`-derived NEGATIVE RNG seed at `spatial_engine.py:1241`, and a missing `output/standard-demo-regen-2026-05-17/season_002012/monsters.json` content file. The pytest scenario suite is the robust deterministic spatial-green witness.

### Keystone preserved
The node-investment wire (`combatant._apply_max_profile_investment` + `from_player_class(apply_max_profile_investment=False)`, 15/5 kills the 0.35× floor) is ENTIRELY outside the deletion surface and carries forward into the spatial path UNCHANGED. I touched none of it.

### Math notes stamped HISTORICAL (3)
`b6-deletion-prereq-B-g7-hold-sim-*`, `b6-reshape-hot-caster-cell-construction-*`, `b6-reshape-scoping-per-tier-shape-degeneracy-signature-*`. The `m1-3-5-*` notes were NOT stamped — on inspection they document the reduced-SPATIAL inner-loop substrate (the SURVIVOR), not the 1D search-estimator (the dispatch's "search-estimator-related" framing corrected). The `wb-typewall-rename` note left unstamped (the type-wall it primarily documents SURVIVES). Both judgments surfaced to KR.

### What surprised me / dispatch under-specifications (surfaced to KR)
1. **`fight_engine.py` was already a tombstone shim, not the 1D kernel.** The actual 1D kernel is `search_estimator.py` (W-B rename). The dispatch's three-file naming maps cleanly to the intent ("delete the 1D kernel + estimation layer"); `batch_runner.py` is a fourth 1D-kernel file (its body is the 1D loop) that I also deleted.
2. **"sim-side b6 handling" is mostly comment-tag + shared-primitive, not a b6 combatant path.** `KI-B6-1` = the modifier-range variance FIX (per-hit damage roll), not the b6 archetype — load-bearing for the spatial path; I retagged comments only, no math change. `AOE_GEOMETRIES` is a SHARED AOE-geometry frozenset, not b6 handling.
3. **CROSS-SEAM BLOCKING for rocket:** `damage_resolver.py:33` has a MODULE-LEVEL `from ...b6_archetype_templates import AOE_GEOMETRIES`. If rocket deletes `b6_archetype_templates.py` WITHOUT re-homing `AOE_GEOMETRIES` (e.g. to `generation/geometry_constants.py` or `foundation/`), `damage_resolver` breaks at IMPORT TIME → engine un-runnable. This is the load-bearing line in MIGRATION v1.70 for rocket.
4. **Recompose-lever scope question for Matt/KR:** `ARCHETYPE_TEMPLATES`/`TIER_SCALING_BANDS`/`BIAS_*` (balance_loop recompose levers) consult rocket's b6 templates. Retiring those levers is a balance-semantics change (alters convergence for every class), NOT a kernel deletion — a SEPARATE forward dispatch. I did NOT touch them (delete-so-it-still-runs; the battle-path rewire is independent).
5. **Three intrinsically-1D diagnostics had no faithful spatial scenario** (doppelganger mirror, trial gallery, spirit_guide fit signal) — RETIRED-WITH-1D and fail-loud (or return retired sentinel), framed not buried (Disc #12). Re-homing them as spatial scenarios is forward-work.
6. **~12 test files import the deleted 1D surface** (test_combat_simulator, test_wb_typewall_rename, test_balance_loop, test_spirit_guide, gear CP tests) → fail at collection. They test the deleted 1D kernel. Retiring/porting them is downstream cleanup beyond the deletion's narrow acceptance ("engine-runs + spatial-green"); NOT scope-crept here. Flagged for a cleanup decision.

No genuine blocker hit; the engine is runnable. Sequencing: rocket (b6 gen delete) is unblocked to read MIGRATION v1.70 — heed the AOE_GEOMETRIES BLOCKING contract.
