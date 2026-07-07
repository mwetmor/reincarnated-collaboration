# Gate-2 Review Request — carried_gear export-path flatten (batch-2 step 2)

**Submitted by:** star-lord
**Date:** 2026-07-07
**Tag:** `star-lord/v-batch2-carried-gear-export-flatten-1`
**Dispatch:** `agentic_orchestration/dispatches/2026-07-07-star-lord-carried-gear-export-flatten.md`
**Authority:** Matt 2026-07-06/07 (step 2 of batch-2 5-step sequence, re-scoped from rocket after STOP-flag `b3e5658`/`802cf5e`)

## What changed

Single function fix in `export/cycle13_normal_season_export.py:_derive_carried_gear` (lines 367-378 → expanded to ~60 lines with contract docstring).

**Before:** returned `char.gear_representative` verbatim as `carried_gear`. `gear_representative["main_weapon"]` is a 10-field gear-slot entry with `substrate_binding` as a sub-key. Combatant reads `.get("spell_damage_modifier", 0.0)` at top level → **0.0 for all INT/caster classes on the persisted path.**

**After:** extracts `gear_representative["main_weapon"]["substrate_binding"]` → `carried_gear["main_weapon"]` (flat). `spell_damage_modifier` is now at top level of `main_weapon`. Null-safe when binding is absent.

## Files changed

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export.py` — `_derive_carried_gear` fixed (the only code change)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` — new batch-2 step 2 entry (full shape contract + round-trip results)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — clarification note appended to line 325 (opaque TEXT / shape contract)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — key-alias note + persisted-path clarification appended to lines 4126-4130
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` — checkpoint updated

## Why this is Principle 6 / Gate-2 territory

`carried_gear` is a persisted cross-seam contract: export → telemetry DB (TEXT column) → `season_exporter.py` read-back → `PlayerClass.carried_gear` → `combatant.from_player_class()`. Changing its internal shape on the persisted path requires Gate-2 sign-off per ADR-004 and Principle 6.

## Seam-owner decision (open question 1)

**FLATTEN IS SAFE.** No loadout or telemetry consumer reads `carried_gear.main_weapon` substrate fields:
- Demo `CarriedGear` interface (`weapon/off_hand/armor/accessory`) is a separate contract
- Loadout has `carried_gear: null` for all v2_narrow_phase_5 and cycle-13 classes
- Loadout WeaponDescriptor (`main_weapon` field) comes from `_derive_main_weapon()` reading `gear_representative` directly — NOT `carried_gear`
- Telemetry DB stores `carried_gear` as opaque TEXT (no internal shape validation)
- Sim combatant (`combatant.py:893-901`) is the SOLE consumer of `carried_gear["main_weapon"]["spell_damage_modifier"]`

## Confirmations

- `cycle14_unified_bundle_emitters.py` — UNAFFECTED (zero references to `carried_gear`; reads `gear_representative` exclusively). Confirmed by grep.
- In-memory pilot/gauntlet path — UNCHANGED. The pilot builder (`season_generation_pipeline.py:1604`) already produced the correct flat shape; this fix makes the export path match it.
- `gear_representative` shape — UNCHANGED. The fix extracts from it; does not modify it.
- Combatant reader (`combatant.py:893-901`) — UNCHANGED per out-of-scope constraint.

## Round-trip smoke (Principle 6) — ALL PASS

```
SMOKE TEST 1: _derive_carried_gear flat output
  Input: gear_representative.main_weapon.substrate_binding.spell_damage_modifier = 0.72
  Output: carried_gear = {"main_weapon": {"spell_damage_modifier": 0.72, ...}} (flat)
  PASS: top-level SDM, no substrate_binding sub-key, no gear_instance_id

SMOKE TEST 2: combatant from_player_class read path
  _carried.get("main_weapon").get("spell_damage_modifier") = 0.72 (was 0.0 before fix)
  PASS: combatant reads non-zero spell_damage_modifier

SMOKE TEST 3: null-safety (4 cases)
  No gear_representative → None
  No main_weapon → None
  No substrate_binding key → None
  substrate_binding = None (static cycle-13 pattern) → None
  PASS: all null-safety cases return None correctly

SMOKE TEST 4: in-memory pilot path unchanged
  fixed exporter output == pilot_carried_gear (byte-equivalent)
  PASS: fixed exporter output is byte-equivalent to pilot builder shape

SMOKE TEST 5: real cycle-13 static char (S1_endgame_int_01_standard_wizard)
  substrate_binding = None → result = None (correct scaffold sentinel)
  PASS: real cycle-13 data handled correctly
```

## Out of scope (confirmed not touched)

- No constant changes (BASE_SPELL, multipliers, SC-6b)
- No change to `gear_representative` shape or `season_generation_pipeline.py:472`
- No change to `combatant.py:893-901`
- No change to pilot/gauntlet path behavior
- No loot-operator work
- No caster bar re-derivation (gamora step 1, separate dispatch)
- No physical gear_set/pool change (inversion finding is a later fork)

## jack-ryan review scope

1. Verify `_derive_carried_gear` fix is correctly scoped (extracts substrate_binding, null-safe, matches pilot builder shape)
2. Verify MIGRATION.md updates accurately describe the shape contract change in all 3 files
3. Verify round-trip smoke arguments are sound (combatant reader reads top-level SDM)
4. Confirm no other `carried_gear` consumer in scope that the seam-owner decision missed
