# LC-026 Disposition Addendum — Mana Bug Verify (W0.5)

**Constraint:** LC-026 — Mana bug (structural) — non-mana classes assigned mana by pipeline
**Author:** gamora
**Date:** 2026-05-21
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-gamora-w0-5-mana-bug-verify.md`
**Full math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-5-mana-bug-verify.md`
**AGENT_STATE record:** `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` § QD-Rebuild P0 W0.5

---

## Disposition update: RESOLVED

**Prior status:** DOCUMENTED (flagged; fix designed; implementation status requires VERIFY)
**New status:** RESOLVED — verified structurally fixed by Phase 1 dimensional refactor (commit `4c28ed6`, 2026-05-08)

---

## What the fix did

The 2026-05-08 Phase 1 dimensional refactor resolved the bug at both layers:

### Layer 1: Pool assignment (`combatant.py`)

`from_player_class()` now branches on `energy_type` before computing pool values:

- If `energy_type` in `_ENERGY_CONFIGS` (rage/combo/focus/stamina-as-resource): uses fixed pools appropriate for that energy type, bypassing stat-derived mana computation entirely.
- If `energy_type == "mana"` (or unknown): uses `compute_max_mana(intelligence, wisdom)` as before.

Pre-fix: a rage physical_warrior with int=5, wis=5 would receive a mana pool of ~12-15 units while skills cost 14-30 units — permanently locked.

Post-fix: the same warrior receives `max_mana=100.0, mana=0.0` (rage starts empty), `mana_regen=0.0`. Pool is energy-type-correct.

### Layer 2: Skill costing (`ability_grammar.py`)

`_get_energy_cost()` routes by energy_type:
- rage: `_RAGE_COST_RANGE` (25-50), calibrated to the 100-unit pool
- combo primary_attack: 0.0 (free; generates +1 combo per cast)
- combo burst_damage/area_damage: 3.0 (pool max = 5)
- focus/stamina-as-resource: role's standard range, fit within 100/150 pools respectively

No skill cost exceeds its energy type's pool maximum.

---

## Telemetry evidence (cold-start, SELECT-only, Discipline #11.1)

From `data/telemetry.db`, recent seasons (099xxx-100xxx):

| energy_type | archetype | avg_int | avg_wis | base_mana |
|---|---|---|---|---|
| rage | physical_warrior | 5.0 | 5.0 | **100.0** |
| rage | physical_grappler | 6.5 | 13.0 | **100.0** |
| combo | rogue | 11.5 | 9.0 | **5.0** |
| focus | hunter | 18.0 | 25.0 | **100.0** |
| stamina-as-resource | physical_warrior | 8.0 | 8.0 | **150.0** |

The `base_mana` values match `_ENERGY_CONFIGS` pools (100/5/100/150), NOT the stat-derived mana value that low int/wis would produce (would be ~12-25 for these stat levels).

Rage skill energy costs in season_100003: 34.1-48.5 (entirely within 25-50 target band). No sub-25 rage costs in any post-fix season.

---

## Unit test coverage

`tests/test_energy_types.py`: 54/54 PASS
- Pool initialization per energy_type
- Rage build/cap mechanics
- Combo 0-cost primary + 3-cost spender mechanics
- Focus decay + restore mechanics
- Resource tick clamping at 0 and max_mana

All energy type tests pass at 2026-05-21 engine state.

---

## Residual: base_stamina telemetry write gap

The 2026-05-08 findings noted `base_stamina` column exists in schema but is never written by `_insert_classes`. This REMAINS UNFIXED as of 2026-05-21. It is:
- A telemetry documentation gap, not a fight-engine bug
- The dodge-stamina system works correctly in the fight engine
- Does not affect Axis 5 BC dimension assignments
- Does not affect QD-rebuild P1 substrate work

This gap is out of scope for LC-026 (mana pool structural fix). Flagged for star-lord's telemetry schema awareness.

---

## Architectural compatibility

The fix is fully compatible with substrate-as-cohesion-only (QD-rebuild architectural direction). Substrate and energy_type are orthogonal axes:
- Substrate → cohesion properties (geometry affinities, ailments, vocabulary)
- Energy type → pool mechanics (size, start value, regen rate, skill costs)

No coupling between substrate cohesion and energy pool logic. Axis 5 (resource economy) BC profiling correctly reads `energy_type` from class schema as the structural signal for economy bin assignment.

---

## QD-rebuild P1 implication

The resource economy substrate surfaces (HP-economy substrate, charge-stack substrate, damage-converts substrate) can be built on a structurally sound mana pipeline. They will not inherit the original mana bug. The LC-026 constraint is cleared for P1.

Note: the separate LC-025 (`has_damage_to_resource_conversion_mechanic`) and LC-030 (HP-cost skill variety gap) remain open — those are P1 substrate extension requirements, not carry-forward bugs.
