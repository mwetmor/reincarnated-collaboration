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
