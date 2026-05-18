# 2026-05-17 — star-lord — Scout: per-season `gauntlet_recipe.json` emission (JSON-parity Step 1)

**Authority:** Matt L3 directive 2026-05-17 late-evening: *"the monsters need to be the exact same monsters from the gauntlet. 100% what comes out of the JSON. I want to see what the battle sim saw. SO do the players because that's what we tuned the classes for."*
**Type:** Pattern A — scout / scoping (no production code yet); ~30-45 min.
**Status:** 🟢 **ACTIVE — Matt-authorized; fire immediately. Step 1 of multi-seam JSON-parity chain.**

---

## Why this matters

The demo (`reincarnated-demo/src/encounter/gauntlet.ts`) currently builds its OWN gauntlet:

> `pickMonsters(monsters, 'trash', 8); pickMonsters(monsters, 'standard', 2); pickMonsters(monsters, 'elite', 2); pickMonsters(monsters, 'mini-boss', 1); pickMonsters(monsters, 'boss', 1);`

The engine (`reincarnated-engine/src/reincarnated/simulation/balance_loop.py:258` `build_reference_gauntlet` + `:380` `_make_recompose_gauntlet`) builds a DIFFERENT structure:

> 6 PackProxy / swarm slots + 6 non-pack slots (magic×2, elite×2, mini-boss×1, boss×1) — per `math/b10-v2-sequential-room-convergence.md`

**These are different fights.** Class WR was tuned against the engine's gauntlet. The player in the demo fights a different sequence than the balance loop simulated. Matt's directive: **eliminate the gap**.

The plan: engine emits a per-season `gauntlet_recipe.json` (or whatever filename star-lord proposes) that captures the EXACT mob sequence (rooms, packs, individual mobs, spawn order) that the balance loop simulated. Demo consumes this file instead of its own pickMonsters logic. Combatant.fromMonster keeps using monsters.json for the actual stats (which is already 100% JSON-parity for stats; the gap is in **selection and sequencing**, not stat data).

---

## Required reading

1. **Engine balance loop** — `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` — `build_reference_gauntlet` (line 258) + `_make_recompose_gauntlet` (line 380) + V2 sequential-room math (`math/b10-v2-sequential-room-convergence.md`)
2. **Demo gauntlet** — `reincarnated-demo/src/encounter/gauntlet.ts` — current pickMonsters logic + pack-slot construction (filterAddPoolForSmallRoom, monsterSpec, trashAdds, wave1-5 structure)
3. **Season orchestrator** — `reincarnated-engine/src/reincarnated/orchestration/` (or wherever season-level outputs are written; star-lord knows the right path)
4. **Existing per-season outputs** — `reincarnated-demo/public/seasons/season_002011/` — currently has classes.json, gear_pool.json, metadata.json, monsters.json
5. **ADR-004** (MIGRATION.md) — cross-seam change requires migration entry
6. **Discipline #15** (demo as renderer) — this work extends the discipline from visual rendering to gameplay-state fidelity
7. **Discipline #11** (attribution clarity) — gauntlet_recipe.json provides explicit provenance for what the player is fighting

---

## Scope — scoping only (no implementation)

Produce a scope document at `reincarnated-collaboration/agentic_orchestration/research/curated/gauntlet-recipe-emission-scope-2026-05-17.md` (or similar; star-lord's call on path) covering:

### A. Emission contract proposal

What fields should `gauntlet_recipe.json` contain? Suggested skeleton (star-lord refines):

```json
{
  "schema_version": "v1.0",
  "season_id": "002011",
  "source": "balance_loop_reference_gauntlet",
  "rooms": [
    {
      "room_id": 0,
      "room_type": "magic" | "elite" | "mini-boss" | "boss",
      "packs": [
        {
          "pack_id": 0,
          "pack_type": "primary" | "pack-add" | "swarm-proxy",
          "monsters": [
            {
              "monster_id": "<key from monsters.json>",
              "spawn_delay_s": 0.0,
              "instance_index": 0
            }
          ]
        }
      ],
      "hp_carryover_in": 1.0,
      "hp_carryover_out": null
    }
  ],
  "total_rooms": 12,
  "total_mob_instances": <int>,
  "estimated_kpm_floor": <int> | null
}
```

Star-lord should evaluate:
- Is this the right shape? Does it capture everything the demo needs to reproduce the fight sequence?
- Does PackProxy need expansion (the demo doesn't have a PackProxy primitive currently — does it need one, or does demo expand swarms into individual mobs?)
- What about wave-internal spawn delays? (demo currently has 0.07/0.14/0.21/etc.)
- Does the demo need fight-by-fight resolution telemetry, or just the spawn recipe?

### B. Emission integration point

Where in the engine does this get emitted? Star-lord knows the seam — propose:
- File path output: `<season_dir>/gauntlet_recipe.json`
- Trigger: same point where monsters.json + classes.json + gear_pool.json are written (likely `season_orchestrator.py` finalize step)
- Per-class variance: does the recipe differ per class (each class faces a different sub-gauntlet), or is it shared across all classes in a season? (Per balance-loop math, it's shared — verify.)

### C. Backfill strategy for staged seasons

002011-015 are already shipped. Two options:
- **Option A (re-derive):** Run a one-time `build_reference_gauntlet` against staged seasons + dump the recipes — no regen needed
- **Option B (regen):** Trigger rocket to re-emit 002011-015 with new recipe field — full regen
- Star-lord recommends one based on determinism / cost

### D. Demo-side implications (handoff to drax)

Briefly note what drax v1.16 will need to do (will be its own dispatch):
- Replace `pickMonsters` in `gauntlet.ts` with a `gauntletFromRecipe(recipe, monsters)` loader
- Add `PackProxy` primitive to demo (or expand swarms to individual mobs at recipe-emit time)
- Preserve `filterAddPoolForSmallRoom` ergonomic shaping? Or eliminate?
- Mock fallback if recipe missing (graceful degrade to current pickMonsters for legacy seasons)

### E. Cross-seam coordination

- **Rocket impact:** if Option B (regen), what's the cost? (Hint: small if recipe is one-line emission)
- **MIGRATION.md entry** drafted (per ADR-004)
- **Discipline #15 extension** — is this a clean extension of "demo as renderer" or does it deserve its own discipline number?

### F. Player-side JSON-parity check

Matt's directive said "SO do the players because that's what we tuned the classes for." Briefly audit:
- Does Combatant.fromClass (demo) use classes.json fields 1:1?
- Are any class fields derived/randomized in demo code? (Carried_gear backfill bug exposed one drift; any others?)
- Are stats / skills / traits / cooldowns all consumed verbatim?
- If yes, no work needed on player side; if no, flag the gaps

### G. Scope estimate

- Star-lord side (emission): ___ hours
- Rocket side (backfill or regen): ___ hours
- Drax side (consume): ___ hours
- Total chain: ___ hours

---

## Acceptance criteria

- [ ] Scope document authored at the proposed path
- [ ] Emission contract proposed with explicit JSON schema
- [ ] Integration point identified in engine code (specific file + function)
- [ ] Backfill strategy chosen (Option A or B) with rationale
- [ ] Demo-side implications enumerated (drax handoff list)
- [ ] MIGRATION.md draft entry
- [ ] Player-side parity audit completed
- [ ] Scope estimate (hours) per agent
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `star-lord/v1.6-gauntlet-recipe-emission-scout-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT write the emission code yet (this is scope-only; full impl is post-Matt-review)
- ❌ DO NOT modify balance_loop.py logic (emission is additive read-only inspection of the reference gauntlet)
- ❌ DO NOT regen any seasons (rocket seam; queued post-scout)
- ❌ DO NOT touch demo code (drax seam; queued post-scout)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with**: gandalf D11.2 (in flight); drax v1.14 (in flight — sprite pool expansion is COMPLEMENTARY to JSON-parity, NOT conflicting); jack-ryan #121 capture (also active)
- **Triggers downstream**: rocket regen/backfill chain → drax v1.16 JSON-parity wiring (will reorder ahead of v1.15 audio per Matt priority signal)
- **Cross-seam impact**: HIGH — engine emission + rocket regen + drax consumption; MIGRATION.md required

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 JSON-parity directive. ~30-45 min scout. Append completion record + scope doc when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** star-lord
**Duration:** ~45 min
**Tag:** `star-lord/v1.6-gauntlet-recipe-emission-scout-1` — pending Matt review (not yet pushed per ADR-006)

### Acceptance criteria status

- [x] Scope document authored: `agentic_orchestration/research/curated/gauntlet-recipe-emission-scope-2026-05-17.md`
- [x] Emission contract proposed with explicit JSON schema (flat slots, not rooms; see §A)
- [x] Integration point identified: `output/season_writer.py:write_season()` + `export/season_exporter.py:_export_season_inner()` (§B)
- [x] Backfill strategy chosen: Option A (re-derive from existing ID list + monster JSONs; no regen; §C)
- [x] Demo-side implications enumerated (§D): gauntletFromRecipe, PackProxy expand vs true-proxy, fallback for legacy seasons, filterAddPoolForSmallRoom retention
- [x] MIGRATION.md draft entry (§E)
- [x] Player-side parity audit completed (§F): fromClass is 1:1 with classes.json; fromMonster has a max_hp gap (flagged, separate dispatch)
- [x] Scope estimate: star-lord ~2.5h / rocket 0h (Option A) / drax ~3.5-5.5h (§G)
- [x] PRE-SIGNAL § 14.1.1 — signaled to Matt before hive-log append (see below)
- [x] AGENT_STATE.md updated with session record
- [x] Tag pending Matt review

### PRE-SIGNAL § 14.1.1

**Signal to Matt:** Scout complete. Key findings before you review:

1. **Existing `reference_gauntlet.json` is thin (IDs only) and not exported to demo.** The richer `gauntlet_recipe.json` is a new additive file.

2. **Engine gauntlet shape is NOT rooms — it is a flat 12-slot sequence.** The dispatch's proposed `rooms[]` schema was simplified to a flat `slots[]` array because the engine has no room topology in the gauntlet object. Rooms can be added additively later when B10 V2 sequential-room geometry becomes first-class.

3. **Backfill is Option A (re-derive).** No regen needed. 5-season backfill script writes ~5 small JSON files. Needs your authorization before running (writes to demo public/seasons/ and engine staging).

4. **Extra gap found: monster max_hp not consumed by demo.** `Combatant.fromMonster()` ignores `monster.max_hp` from monsters.json — all monsters fight at HP_BASE=10,000. This is separate from the gauntlet recipe work. Flagged for a separate dispatch.

5. **Three documented demo overrides in combatant.ts** (focus regen, combo clamp, cooldown mult) — all intentional and tracked. No hidden drift.

### Key paths

- Scope doc: `reincarnated-collaboration/agentic_orchestration/research/curated/gauntlet-recipe-emission-scope-2026-05-17.md`
- AGENT_STATE.md: `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md`
- Implementation targets (pending approval): `output/season_writer.py`, `export/season_exporter.py`, `export/MIGRATION.md`, `scripts/gauntlet_recipe_backfill.py`
