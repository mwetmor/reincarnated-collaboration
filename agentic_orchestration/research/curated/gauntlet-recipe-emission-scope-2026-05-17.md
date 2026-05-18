# Gauntlet Recipe Emission — Scope Document
**Date:** 2026-05-17
**Author:** star-lord
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-star-lord-gauntlet-recipe-emission-scout.md`
**Status:** Scout complete — awaiting Matt review before implementation

---

## Background and gap summary

The engine's `build_reference_gauntlet()` produces 12 opponents structured as:
- 6 swarm PackProxy slots (each wraps a base monster with `pack_size=8`, HP×8, AOE deals 8× damage)
- 2 magic-tier 1v1 slots
- 2 elite-tier 1v1 slots
- 1 mini-boss slot
- 1 boss slot

The demo's `buildGauntlet()` in `gauntlet.ts` builds a 7-wave structure using:
- Wave 1: 4 trash mobs (1 primary + 3 pack adds at PACK_HP_MULT=0.18 / PACK_DMG_MULT=0.25)
- Wave 2: 1 standard + 2 trash adds
- Wave 3: 1 elite + 3 trash adds
- Wave 4: 1 mini-boss + 3 range-filtered trash adds
- Wave 5: 1 boss + 1 elite + 4 trash adds
- Waves 6-7: act-boss 1v1 (from classes.json, not monsters.json)

These are structurally different fights. The engine balances classes against 6 PackProxy swarms plus 6 named non-pack opponents. The demo presents entirely different tier counts (no PackProxy semantics; trash tier instead of swarm tier; different primary/add topology). Class WR tuning was done against the engine composition. The player is fighting a different fight than balance saw.

An existing `reference_gauntlet.json` is already written per-season by `season_writer.py` at line 131-134. It currently emits only a flat list of monster IDs (with `_pack` suffix for swarm slots). Example from season_002011:
```json
["monster_00001_pack","monster_00002_pack","monster_00003_pack",
 "monster_00004_pack","monster_00005_pack","monster_00006_pack",
 "monster_00013","monster_00014","monster_00033","monster_00034",
 "monster_00041","monster_00043"]
```

This file exists engine-side in `output/standard-demo-regen-2026-05-17/` but is NOT exported to `reincarnated-demo/public/seasons/` (only `classes.json`, `monsters.json`, `gear_pool.json`, and `metadata.json` are copied). The gap is threefold: the file is thin (IDs only), not exported, and the demo doesn't consume it.

---

## A. Emission contract proposal

### Proposed filename: `gauntlet_recipe.json`

Distinct from the existing `reference_gauntlet.json` (ID-list only, engine-internal artifact) to avoid backward-compat collision. The recipe is the richer, demo-consumable artifact.

### Recommended schema (v1.0)

```json
{
  "schema_version": "v1.0",
  "season_id": "002011",
  "source": "balance_loop_reference_gauntlet",
  "gauntlet_composition": {
    "swarm": 6,
    "magic": 2,
    "elite": 2,
    "mini-boss": 1,
    "boss": 1
  },
  "pack_proxy_size": 8,
  "slots": [
    {
      "slot_index": 0,
      "tier": "swarm",
      "is_pack_proxy": true,
      "base_monster_id": "monster_00001",
      "pack_proxy_id": "monster_00001_pack",
      "pack_size": 8,
      "hp_multiplier": 8.0,
      "aoe_damage_multiplier": 8.0
    },
    {
      "slot_index": 6,
      "tier": "magic",
      "is_pack_proxy": false,
      "base_monster_id": "monster_00013",
      "pack_proxy_id": null,
      "pack_size": 1,
      "hp_multiplier": 1.0,
      "aoe_damage_multiplier": 1.0
    }
  ],
  "total_slots": 12,
  "slot_order": "as_simulated"
}
```

### Field rationale

**Flat slots list, not rooms list.** The engine runs sequential 1v1 and 1vPack fights, not "rooms" in the dungeon sense. The dispatch's proposed `rooms[]` schema implies a room topology that does not exist in the current engine model (B10 V2 uses sequential-room semantics for the binary search, but the gauntlet data itself is a flat list of opponents). Wrapping in rooms adds indirection for no gain at this stage. If B10 V2 sequential-room geometry becomes a first-class concept, a `rooms` layer can be added additively later.

**`base_monster_id` + `pack_proxy_id` both present for swarm slots.** The demo needs the base monster ID to look up stats from `monsters.json` (which holds the base monster data, not the `_pack` synthetic ID). The `pack_proxy_id` is the engine-internal synthetic key; useful for provenance but not for stat lookup.

**`hp_multiplier` and `aoe_damage_multiplier` explicit.** `PACK_PROXY_SIZE=8` is a constant in the engine but is not in any exported file. Emitting it explicitly means the demo can implement PackProxy semantics correctly without hardcoding a magic number.

**`pack_size: 1` for non-proxy slots.** Keeps schema uniform across all slot types. Demo can branch on `is_pack_proxy`.

**No spawn delays in recipe.** The engine's fight simulator is turn-based (not real-time); spawn delays are purely a demo visual concern. The recipe should not impose demo timing constraints. Drax chooses spawn delays based on its own wave-pacing design.

**No fight-by-fight resolution telemetry.** The recipe is a spawn specification, not a replay. Full fight telemetry lives in `fights.jsonl` (engine-side, not exported). The recipe's job is to tell the demo which monsters appear and in what role, so the encounter matches what was simulated.

**`slot_order: "as_simulated"` field.** Communicates to consumers that the array order is not arbitrary — it reflects the order in which the engine ran each fight during balance convergence.

### What this schema does NOT need to capture

- Wave room variant (720px small room for Wave 4) — that is a demo-side rendering decision, not an engine constraint.
- filterAddPoolForSmallRoom output — that function exists in the demo today because it independently selects trash adds; once the demo consumes the recipe, the add pool is dictated by the recipe itself.
- The recompose gauntlet (which substitutes base monsters for PackProxy during the recompose loop) — that is an internal balance loop detail, not part of the reference gauntlet that balance converges against.

---

## B. Emission integration point

### Engine-side: `season_writer.py` (not `season_exporter.py`)

The recipe should be written at the same point as `reference_gauntlet.json` — in `write_season()` in `output/season_writer.py` at the point where `reference_gauntlet.json` is currently written (line 130-134). This ensures the recipe is part of the generation artifact alongside classes, monsters, trial, fights.jsonl, etc.

`season_exporter.py` then needs a second change: read `gauntlet_recipe.json` from the season directory and copy it verbatim into the export output directory (same as it copies metadata.json, classes.json, monsters.json, gear_pool.json). Unlike those files, there is no DB augmentation needed for the recipe — it is derived purely from `SeasonOutput.reference_gauntlet` which is already in-memory.

### Exact locations

1. `output/season_writer.py:write_season()` — after the existing `reference_gauntlet.json` write, add:
   ```python
   _write_json(season_dir / "gauntlet_recipe.json", _gauntlet_recipe(output))
   ```
   where `_gauntlet_recipe(output)` constructs the schema above from `output.reference_gauntlet` and the `GAUNTLET_TIER_COMPOSITION` constant.

2. `export/season_exporter.py:_export_season_inner()` — after `_write_json(export_dir / "gear_pool.json", ...)`, add:
   ```python
   recipe_path = season_dir / "gauntlet_recipe.json"
   if recipe_path.exists():
       shutil.copy(recipe_path, export_dir / "gauntlet_recipe.json")
   ```
   This is a passthrough copy, no transformation needed. Add `import shutil` at top.

3. `export/schemas.py` — no schema change needed for the recipe itself (it is a standalone JSON document, not a Pydantic model). The Stage B boundary validator (`_validate_stage_b_classes/_validate_stage_b_monsters`) does not need updating — the recipe is a separate file, not a field on classes or monsters.

### Per-class variance: shared, not per-class

The reference gauntlet is built once per season from the full bestiary before class generation begins (season_orchestrator.py line 357: `gauntlet = self.balance.build_reference_gauntlet(bestiary)`). All classes are then balanced against this same gauntlet. There is one gauntlet recipe per season, not one per class. Confirmed by code inspection.

The L33 and L17 per-band gauntlets (`gauntlet_l33`, `gauntlet_l17`) are currently simple flat monster lists (no PackProxy), used for band-leveling balance checks, not the reference gauntlet the recipe must capture. They are out of scope for this recipe.

---

## C. Backfill strategy for seasons 002011-015

### Recommendation: Option A (re-derive), not Option B (regen)

**Rationale:** The engine-side staging directory `output/standard-demo-regen-2026-05-17/` contains all 5 seasons in full. The `reference_gauntlet.json` flat ID list already exists for each. The `SeasonOutput.reference_gauntlet` can be re-derived from the monster IDs by:

1. Loading `monsters/<monster_id>.json` from the season directory to reconstruct each `Monster` object.
2. For each ID ending in `_pack`, stripping the suffix to get the base monster ID and marking `is_pack_proxy=True`.
3. Emitting the recipe JSON from the reconstructed data.

This requires a one-time backfill script (similar in shape to `scripts/d10_carried_gear_backfill.py`) that reads the existing staging output, constructs `gauntlet_recipe.json` for each of the 5 seasons, and writes it into both the engine staging directory and the demo's public/seasons directory.

**Option B is overkill.** Full regen would cost ~$4-5 (5 seasons × ~$0.85-1.00) and would produce different seeds for cosmological vocabulary and spirit guide voice. The gauntlet selection is deterministic from the existing bestiary — no LLM calls touch it. Re-derive is the right tool.

**Determinism check:** `build_reference_gauntlet()` is deterministic given the bestiary input. The bestiary for each 002011-015 season is already written to `output/standard-demo-regen-2026-05-17/season_002011/monsters/`. The existing flat ID list in `reference_gauntlet.json` confirms exactly which monsters were selected. The backfill script only needs to reconstruct the richer schema around the already-committed ID list — no re-running of the selection algorithm.

**Backfill script location:** `scripts/gauntlet_recipe_backfill.py` — parallel pattern to `d10_carried_gear_backfill.py`. Matt authorization needed before running (ADR-006 scope: this writes new files to the output directory, not to the telemetry DB, so the authorization bar is lower than DB migrations — but it modifies shipped demo assets, so Matt should sign off).

---

## D. Demo-side implications (handoff to drax v1.16)

This will be drax's own dispatch. Enumerated here for completeness.

### Required changes in `reincarnated-demo/src/encounter/gauntlet.ts`

1. **Add `gauntletFromRecipe()` loader function.** Reads `gauntlet_recipe.json` for the current season and builds the `WaveSpec[]` array from recipe slots rather than `pickMonsters()`. This is the primary behavioral change.

2. **PackProxy primitive in demo.** The recipe's swarm slots (`is_pack_proxy: true`) describe the engine's PackProxy semantics (hp_multiplier=8, aoe_damage_multiplier=8). The demo currently approximates swarms via `trashAdds()` with `PACK_HP_MULT=0.18 / PACK_DMG_MULT=0.25` — a completely different model. For true parity, drax needs to implement PackProxy encounter behavior: a single combatant with HP×8, takes AOE damage ×8. This is a non-trivial change. Two options for drax:

   a. **Expand to individual mobs at recipe-emit time** — the engine emits the recipe with pack slots; drax expands each pack slot into N individual PACK_HP_MULT mobs. Simpler for the demo; doesn't match engine exactly (AOE semantics differ) but approximates the encounter pressure.

   b. **Implement PackProxy combatant type** — a single `Combatant` with multiplied HP. AOE skills deal pack_size× damage to it. This matches the engine exactly. More work for drax.

   Star-lord recommendation: emit the recipe with the full PackProxy metadata (hp_multiplier, pack_size) and let drax decide. The recipe is correct regardless. If drax implements Option (a) for VS2a and (b) later, the recipe doesn't need to change.

3. **Replace pickMonsters selection.** Once consuming from the recipe, `pickMonsters()` becomes dead code for primary slot selection. It may be retained for add-pool selection if drax keeps the wave-internal add pattern, but the primary encounter slot must come from the recipe.

4. **filterAddPoolForSmallRoom — keep as-is.** This filter operates on add mobs that fill wave packs around primary opponents. Whether add mobs still come from an independent selection (current behavior) or from the recipe (ideal parity) is drax's call. Full parity would require the recipe to also specify add composition, which the engine does not currently model (adds are a demo-only concept). For now: keep the filter, keep independent add selection. The parity win is in primary slot selection, which is the fight the engine actually simulated.

5. **Graceful fallback for legacy seasons (001001-001005).** Those seasons predate the recipe. `buildGauntlet()` should detect the absence of `gauntlet_recipe.json` and fall back to the existing `pickMonsters()` logic. This makes the change non-breaking for earlier seasons.

6. **Act-boss waves (Waves 6-7) are unaffected.** Act bosses come from `classes.json` (via `getActBosses()`), not from `monsters.json`. The recipe does not touch act-boss selection.

---

## E. Cross-seam coordination

### MIGRATION.md draft entry

```markdown
## v1.5 — gauntlet_recipe.json: per-season engine gauntlet spawn recipe (2026-05-17)

**Author:** star-lord
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-star-lord-gauntlet-recipe-emission-scout.md`
**Repos affected:** reincarnated-demo (new file to consume), reincarnated-engine (new file emitted)

### What changed

New file added to each season export: `gauntlet_recipe.json`. Captures the exact
12-slot reference gauntlet the balance loop simulated against, in machine-readable form.

This is an ADDITIVE change — existing files (classes.json, monsters.json, gear_pool.json,
metadata.json) are unchanged. Seasons without gauntlet_recipe.json (001001-001005)
continue to work.

### Schema (v1.0)

[see gauntlet-recipe-emission-scope-2026-05-17.md §A for full schema]

### Key fields

- `slots[].base_monster_id` — look up stats in `monsters.json` (exact same key)
- `slots[].is_pack_proxy` — true for swarm encounters
- `slots[].hp_multiplier` — 8.0 for swarm, 1.0 for others
- `slots[].aoe_damage_multiplier` — 8.0 for swarm, 1.0 for others
- `pack_proxy_size: 8` — PACK_PROXY_SIZE constant, now explicit in JSON

### Emission points (engine)

- `output/season_writer.py:write_season()` — written at generation time
- `export/season_exporter.py:_export_season_inner()` — passthrough copy to export dir

### Action required by drax

- drax v1.16: replace `pickMonsters()` primary selection with `gauntletFromRecipe()`
- Implement PackProxy encounter behavior (or expand-to-individual approximation)
- Add fallback for legacy seasons (no gauntlet_recipe.json → use current pickMonsters)

### Backward compatibility

- Seasons 001001-001005 do not have gauntlet_recipe.json — demo must fall back gracefully.
- Seasons 002011-015 will be backfilled via one-time script (Option A re-derive).
- Consumers that ignore unknown season files are unaffected.
```

### Rocket impact

Option A (re-derive, recommended) has **zero rocket cost** — no regen needed.

If Matt later decides Option B (full regen for correctness audit), cost would be ~$4-5 for 5 seasons. Not recommended for this use case.

### Discipline #15 extension

The dispatch notes Discipline #15 ("demo as renderer"). The gauntlet recipe extends this from "stats come from JSON" (already true for Combatant.fromMonster) to "encounter composition comes from JSON." This is a clean extension of the same principle — the demo renders what the engine defines, rather than defining its own encounter logic.

No new discipline number is warranted. This is Discipline #15 applied to encounter selection, the same way it was applied to stat rendering.

---

## F. Player-side JSON-parity audit

### Combatant.fromClass — parity status

`Combatant.fromClass()` (combatant.ts:170-185) reads from `ClassData`:
- `stat_distribution.strength/dexterity/intelligence/wisdom/vitality` — consumed verbatim from `classes.json` (1:1)
- `energy_type` — consumed verbatim
- `skills` — consumed verbatim; ordered with `primary_attack` first (demo-side ordering, not engine-mandated)
- `dominant_element` — consumed verbatim
- `color_palette` — consumed verbatim
- `balance_metadata.final_modifier` — consumed verbatim as `_damageModifier`
- `carried_gear` — passed as optional; `computeGearStats()` applies it

**No stat drift found.** All numerical fields flow from `classes.json` without transformation.

### Known overrides (documented, not silent drift)

Three explicit demo overrides exist in `combatant.ts` — all documented inline:

1. **FOCUS_RESTORE_PER_CAST = 25.0** (line 100-101): engine spec=10, demo uses 25. Comment: "Remove once engine ships A1b." This is a known temp override, not silent drift.

2. **Combo cost clamp at 5** (lines 235-241): engine emits combo costs 13.7-30 against pool=5; demo clamps at 5 so skills are castable. Comment: "Remove once engine ships A1." Known override.

3. **COOLDOWN_GLOBAL_MULT = 1.4** (line 168): applied to all cooldowns for feel. This is a demo presentation decision, not a balance parameter — the engine's 1v1 fights are not real-time, so this doesn't affect WR.

None of these constitute hidden drift. All three have engine-side tracking comments. The carried_gear bug (referenced in dispatch) was previously addressed by the D10 carried_gear backfill.

### Combatant.fromMonster — parity status

`Combatant.fromMonster()` (lines 187-196) reads from `MonsterData`:
- `max_hp` — used via `computeMaxHp` in the base class, BUT monsters pass `vit=0, str=0`; `max_hp` is set directly via `armor` (the base armor field). **Wait — this is a gap.**

On closer inspection: `fromMonster` sets all stat fields to 0 (`str=0, dex=0, int=0, wis=0, vit=0`). `maxHp` is computed as `computeMaxHp(vit=0, str=0) = HP_BASE + 0 + 0 = 10000`, then `_gear.bonusHp = 0` → `maxHp = 10000` always. But `monster.max_hp` from monsters.json has the actual engine-computed HP (e.g. different values per threat tier). **The demo does not use monster.max_hp from JSON.** All monsters in the demo start at the same 10,000 HP regardless of their threat tier's engine HP value.

This is a separate JSON-parity gap — not in scope for the gauntlet recipe dispatch, but it should be flagged. The `Combatant` constructor doesn't accept a direct `maxHp` override; `fromMonster` would need to pass `vitality` backwards-computed from monster.max_hp, or the constructor needs a `maxHpOverride` param.

**Flag for future dispatch**: monster `max_hp` from monsters.json is not consumed by Combatant.fromMonster. All monsters fight at the same 10,000 HP baseline regardless of tier.

### Skills, cooldowns, traits — parity status

Skills are consumed verbatim (id, role, damage_multiplier, energy_cost, cooldown_seconds, effects). No demo-side modification except the two documented overrides above. Geometry types (circle, line, cone, etc.) are read from `skills[].geometry_type` and consumed verbatim by the combat system.

---

## G. Scope estimate

### Star-lord side (emission)

- `_gauntlet_recipe()` helper in `season_writer.py`: 30 min
- `season_exporter.py` passthrough copy: 15 min
- `export/MIGRATION.md` entry: 15 min
- `AGENT_STATE.md` update: 10 min
- Backfill script (`gauntlet_recipe_backfill.py`): 45 min
- Stage B boundary validator update (add recipe file presence check): 20 min
- Smoke test: 30 min

**Star-lord subtotal: ~2.5 hours** (implementation + backfill + validation)

### Rocket side

- Zero cost if Option A (re-derive) is chosen — no regen needed.
- If Matt authorizes a fresh validation regen of 002011-015 to confirm determinism: ~4 hours machine time, ~$4-5 LLM cost.

**Rocket subtotal: 0 hours (Option A) / 4 hours (Option B)**

### Drax side (consume)

- `gauntletFromRecipe()` loader function: 1 hour
- PackProxy behavior (Option a — expand to individual mobs): 1 hour; (Option b — true PackProxy combatant): 3 hours
- Fallback for legacy seasons: 30 min
- Testing across all 5 shipped seasons: 1 hour

**Drax subtotal: ~3.5 hours (Option a) / ~5.5 hours (Option b)**

### Total chain estimate

Option A + PackProxy expand (recommended path): **~6 hours** across three seams.
Option A + true PackProxy: **~8 hours**.

---

## H. Additional finding: `monster_max_hp` parity gap

During the Combatant.fromMonster audit (Section F), a parity gap was found that is independent of the gauntlet recipe work:

`Combatant.fromMonster()` constructs monsters with all stat fields at 0 and no direct use of `monster.max_hp`. The effective result is every monster fights with `HP_BASE = 10,000` regardless of the engine's tier-scaled HP values (trash 0.50×, elite 1.50×, boss 8.00×). The engine's fight simulator sees the correct per-tier HP; the demo does not.

This gap pre-exists the gauntlet recipe work and is not caused by it. It should be tracked separately. It would be a drax-seam fix. Do not conflate with gauntlet recipe dispatch.

**Not in scope for this dispatch.** Flag to knight-rider for a separate dispatch if Matt prioritizes it.

---

## Summary recommendation

1. **Emit `gauntlet_recipe.json`** using the flat-slots schema above. Write in `season_writer.py`; passthrough-copy in `season_exporter.py`. No changes to schemas.py or Pydantic models.

2. **Backfill via Option A** (re-derive script, no regen). Write `scripts/gauntlet_recipe_backfill.py`. Matt authorizes the backfill run (modifies shipped demo assets).

3. **Drax consumes in v1.16** via `gauntletFromRecipe()`. Primary-slot parity is the goal. Add pool selection (trash adds filling waves) can remain demo-side for now — it doesn't affect the class WR signal. Implement PackProxy via expand-to-individual mobs (Option a) for VS2a; true PackProxy deferred.

4. **Monster max_hp gap** flagged to knight-rider as a separate item.

---

*Scope doc authored by star-lord 2026-05-17 per dispatch.*
