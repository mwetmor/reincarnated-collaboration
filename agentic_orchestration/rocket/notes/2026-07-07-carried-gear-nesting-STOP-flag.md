# carried_gear nesting unification — STOP-and-flag (design note, Discipline #1)

> **Dispatch:** `2026-07-07-rocket-gamora-carried-gear-nesting-unification.md` (Gate-1 RATIFIED-WITH-CONDITIONS)
> **Author:** rocket, 2026-07-07
> **Verdict:** the dispatch's named fix site (`season_generation_pipeline.py:472` un-nest) is founded on a false premise and MUST NOT be executed as written. The real defect is in **star-lord's `export/` seam** (`cycle13_normal_season_export.py:_derive_carried_gear`). Flagging per OP §3.1 (do not patch across seam lines) and per the dispatch's own STOP clause ("if your shape decision would break something, STOP and flag").

---

## 1. What the dispatch assumed vs. what the engine actually is

The dispatch models `gear_representative` and `carried_gear` as **the same dict at different nesting depths**, so that "un-nesting `:472`" would unify them. That is empirically false.

They are **two distinct structures with two distinct correct shapes:**

### `gear_representative` (the emission DECL intermediate, serialized to phase2 JSON at `:472`, `:517`)
`gear_representative.main_weapon` is a **full gear-slot entry** built from `gear_set` at legendary_t1 rarity (`season_generation_pipeline.py:442-448`). Empirically (Discipline #11), its keys are:
```
['gear_instance_id', 'slot', 'rarity', 'partition_modifiers',
 'capability_modifiers', 't4_annotation', 'set_bonus', 'set_bonus_rank',
 'is_unique', 'triggered_passive']
```
The substrate binding is **deliberately** attached as a SUB-KEY `substrate_binding` (`:468,:472`) precisely so it does NOT collide with these 10 slot fields. This is nested-BY-DESIGN, not a bug.

### `carried_gear` (the loadout dict handed to `combatant.from_player_class()`)
Canonical shape (documented in `simulation/MIGRATION.md:4126-4130` + `generation/MIGRATION.md:325`): **the weapon-data dict DIRECTLY under the slot key** — `{"main_weapon": <binding>}` with `spell_damage_modifier` at top level. The pilot builder produces exactly this (`:1604`); the reader consumes exactly this (`combatant.py:893-901`).

**These two shapes SHOULD differ. `gear_representative.main_weapon` = slot-entry + `substrate_binding` sub-key. `carried_gear.main_weapon` = the binding directly.**

## 2. Why un-nesting `:472` is wrong (three failures)

1. **It doesn't fix the actual bug.** The 0.0 comes from `carried_gear`, not `gear_representative`.
2. **It breaks the export weapon-descriptor emitter** (`export/cycle14_unified_bundle_emitters.py:545,571`), which reads `main_weapon_gear.get("substrate_binding")` for identity fields AND `main_weapon_gear.get("gear_instance_id")` at the slot level. Flattening collapses that two-level structure.
3. **It breaks the reconstruction reader (`:1885-1890`) and validator (`:2308-2322`)** — but these are only "consumers that break" *because* `:472` was named as the site. They read the nested `substrate_binding` sub-key of `gear_representative` and are CORRECT today. (Gate-1 condition 4 correctly predicted they'd break on an un-nest; the right conclusion is: don't un-nest — they're fine.)

The reconstruction reader is in fact the **bridge** between the two shapes: `:1885-1890` pulls `substrate_binding` OUT of nested `gear_representative` → `KitCandidate.substrate_weapon_binding` (`:1926`) → `:1604` re-wraps it flat into `carried_gear`. So the JSON-decl → KitCandidate → PlayerClass → combatant round-trip **already produces the correct flat `carried_gear`.**

## 3. The ACTUAL defect (star-lord's seam)

`export/cycle13_normal_season_export.py:367-378` — `_derive_carried_gear(char_data)` returns the WHOLE `gear_representative` dict verbatim as `carried_gear`:
```python
def _derive_carried_gear(char_data):
    gear_rep = char_data.get("gear_representative")
    return gear_rep  # <-- nested shape passed through as carried_gear
```
So `ClassData.carried_gear.main_weapon` = the nested gear-slot entry (binding hidden under `substrate_binding`). Persisted to `classes.carried_gear` TEXT (`recorder.py:1211-1222`), read back (`season_exporter.py:725` `carried_gear=db_data.get("carried_gear")`) into a ClassData that builds a combatant → `combatant.py:896` `.get("main_weapon")` = slot dict → `.get("spell_damage_modifier")` = absent → **0.0**. This is the vanishing caster pool.

**Correct fix:** in `_derive_carried_gear`, transform `gear_representative` → the flat `carried_gear` shape: pull `main_weapon.substrate_binding` up to `carried_gear["main_weapon"]` (matching `:1604`). One function, in `export/`.

## 4. Seam call

`export/cycle13_normal_season_export.py` and `export/cycle14_unified_bundle_emitters.py` are **star-lord's seam** (`export/`). The reader `combatant.py` is **gamora's**. My seam (`generation/`) sites (`:472`, `:1885`, `:2308`) are all CORRECT as-is and should NOT change.

Therefore this dispatch, as scoped to rocket, has **no correct in-seam edit**. Executing the named `:472` change would be a regression (breaks export emitter, doesn't fix the bug). Per OP §3.1, I do not patch `export/`. Routing to knight-rider for re-scope to star-lord.

## 5. Recommendation to knight-rider

- Re-target the fix to **star-lord**: `export/cycle13_normal_season_export.py:_derive_carried_gear` — transform nested `gear_representative.main_weapon.substrate_binding` → flat `carried_gear["main_weapon"]` binding. Add a round-trip smoke: DECL char JSON → `_derive_carried_gear` → combatant reads non-zero `spell_damage_modifier` for INT; pilot path unchanged.
- generation/ + simulation/ sites are correct; MIGRATION already documents the two-shape contract accurately (`generation/MIGRATION.md:325`, `simulation/MIGRATION.md:4126-4130`). No lockstep edit needed there beyond possibly a clarifying note that `_derive_carried_gear` must flatten.
- The inversion finding (physical pool empty, caster +88%) is unaffected by this shape fix and remains a later design fork (gandalf §8.2/§8.4).

**Signed:** rocket, 2026-07-07. The two dicts were never the same shape; the bug is a conflation of them in the export derive-step, one seam over.
