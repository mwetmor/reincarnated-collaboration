# Finding — 2026-07-07 — star-lord carried_gear export-path flatten (batch-2 step 2)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: PASS)
**Target:** commit `64289f0` / tag `star-lord/v-batch2-carried-gear-export-flatten-1`
**Developer:** star-lord
**Principles applied:** 3 (cross-seam impact), 6 (cross-seam round-trip), 4 (decisions-log/contract as truth); Disciplines #1 (design-before-code), #8 (schema validation at boundaries), #11 (attribution)

## What I found

The single code edit to `cycle13_normal_season_export.py:_derive_carried_gear` does exactly what the completion record claims and nothing more. The function now extracts `gear_representative["main_weapon"]["substrate_binding"]` and returns `{"main_weapon": <binding>}` flat, with four correct null-safety guards (no gear_rep, no main_weapon slot, no substrate_binding key, and falsy binding — the last covers the `substrate_binding=None` static cycle-13 pattern). I verified the produced shape is byte-identical to the pilot builder at `season_generation_pipeline.py:1604` (`carried_gear = {"main_weapon": kit.substrate_weapon_binding}`) — confirmed by reading both sources directly, not by trusting the smoke output. The combatant reader (`combatant.py:885-901`) resolves the weapon via the or-chain `main_hand → weapon → main_weapon` then reads `.get("spell_damage_modifier", 0.0)` at the top level of that dict; the flatten places the binding fields at exactly that level, so the persisted-path caster read moves from 0.0 to the real value. No scope creep: `gear_representative` shape untouched, combatant reader untouched, pilot builder untouched, `_derive_main_weapon` (the loadout WeaponDescriptor producer) confirmed to read `gear_representative` independently and is unaffected.

Open-question-1 (flatten-is-safe) holds under stress. The persist→read-back path is genuinely shape-agnostic: `recorder.py:1211-1212` does `json.dumps(pc.carried_gear)` into a TEXT column with no schema validation, and `season_exporter.py:457-465,725` does `json.loads` → passthrough. So the only contract that matters is producer↔combatant, and after this fix the export producer matches the pilot producer. I stress-tested the demo consumer, which star-lord flagged as "a different contract": the demo actively reads `carried_gear.weapon` (`main.ts:1525`, `inventory.ts:38`, `engine.ts:235`) keyed by `weapon/off_hand/armor/accessory`, NOT `main_weapon`. I inspected all 11 live demo season `classes.json` files — every non-null `carried_gear` uses the `weapon/off_hand/armor/accessory` shape from a separate emitter. The cycle-13 exporter has only ever emitted a `main_weapon` key, so it never populated the demo's `weapon` key either before or after this change. No consumer reads `carried_gear.main_weapon` expecting the 10 slot fields (rarity, gear_instance_id, etc.) — those live in `gear_representative`, which the cycle14 emitter reads and which is untouched. Nothing is starved.

## Rationale

Principle 6 (cross-seam round-trip) is satisfied: the persisted contract (export→DB→read-back→combatant) is exercised end-to-end and the producer now matches the sole consumer. Principle 3 (cross-seam impact) is satisfied: I independently verified the three other candidate consumers (loadout WeaponDescriptor, demo CarriedGear, telemetry) and none depend on the changed internal shape. Discipline #1 (design-before-code) is met — the open-question resolution is documented in the docstring and MIGRATION entries before the edit. Discipline #8 (schema-at-boundaries): the TEXT column is opaque by design, so no boundary validator regresses. Discipline #11 (attribution) is clean: commit message and all three MIGRATION notes cite dispatch, authority, re-scope lineage, and the gandalf inversion-finding §8.2 dependency.

All three MIGRATION files (ADR-004 lockstep) accurately describe the shape contract and do not lie. I read each diff against the ground-truth source: the export entry documents both shapes with correct field lists and correct line-number citations (all confirmed); the generation note at :325 correctly states recorder persists whatever the pipeline sets and the export path was the divergent producer; the simulation note at :4126+ correctly documents the or-chain and the separation between the flat `carried_gear` and nested `gear_representative` shapes.

## Action

- [x] Developer: no action required — PASS as submitted.
- [ ] Follow-up (INFO, non-blocking, star-lord's discretion): smoke tests 1-5 validate the in-memory function output and the read-side arithmetic, but do not drive an actual `recorder.persist → season_exporter read-back → combatant.from_player_class` round-trip on a real DB row. The logic is sound because the DB layer is proven opaque (verified), so this is not a gap that changes the verdict — but a single true end-to-end persisted-row smoke would harden the Principle-6 claim for the next persist-path change. Consider adding when the caster-viability sequence next touches this path.

## References

- `~/Games/reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export.py` (:367-423 fix; :430-475 `_derive_main_weapon` unaffected)
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py:1602-1604` (pilot builder — shape-of-record)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py:885-901` (sole consumer, or-chain + top-level read)
- `~/Games/reincarnated-engine/src/reincarnated/telemetry/recorder.py:1211-1212` (opaque persist)
- `~/Games/reincarnated-engine/src/reincarnated/export/season_exporter.py:457-465,725` (opaque read-back)
- `~/Games/reincarnated-demo/src/types/engine.ts:234-256`, `main.ts:1525`, `inventory.ts:38` (separate demo contract — not starved)
- `~/Games/reincarnated-demo/public/seasons/*/classes.json` (11 files inspected: all `weapon/off_hand/armor/accessory` shape)
- MIGRATION lockstep: export/MIGRATION.md (new entry), generation/MIGRATION.md:325, simulation/MIGRATION.md:4126-4130
