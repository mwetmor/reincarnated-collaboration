# 2026-05-17 — star-lord — JSON-parity Step 2: `gauntlet_recipe.json` emission impl + Option A backfill for 002011-015

**Authority:** Matt L3 explicit authorization 2026-05-17 late-evening — "yes to all three" (Option A backfill + bundle max_hp + expand-to-individuals).
**Type:** Pattern B — implementation + one-time backfill run; ~2.5 hours per your scout estimate.
**Predecessor (complete):** your scout at `agentic_orchestration/research/curated/gauntlet-recipe-emission-scope-2026-05-17.md` (tag `star-lord/v1.6-gauntlet-recipe-emission-scout-1`).
**Status:** 🟢 **ACTIVE — fire immediately. Matt-authorized.**

---

## Why this matters

The demo currently fights a different gauntlet sequence than the balance loop simulated; class WR was tuned against the engine's gauntlet, so the player experience drifts from balance intent. This dispatch closes the gap on the engine side: emit per-season `gauntlet_recipe.json` so the demo (drax v1.16, queued) can consume the exact sequence.

Backfill is critical because 002011-015 are already shipped + Matt's playtesting them — the recipe must be present in those seasons for drax v1.16 to wire against. Re-derive from existing `reference_gauntlet.json` ID lists (Option A; $0 cost).

---

## Required reading

1. **Your scout doc** — `agentic_orchestration/research/curated/gauntlet-recipe-emission-scope-2026-05-17.md` (your authoritative spec)
2. **Engine balance loop** — `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` — `build_reference_gauntlet` (line 258); `_make_recompose_gauntlet` (line 380); PACK_PROXY_SIZE source
3. **Engine output writer** — `reincarnated-engine/src/reincarnated/output/season_writer.py` — `write_season()` (integration site per scout)
4. **Engine exporter** — `reincarnated-engine/src/reincarnated/export/season_exporter.py` — `_export_season_inner()` (passthrough copy site per scout)
5. **Existing reference_gauntlet.json** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/reference_gauntlet.json` (and 002012-015; backfill source-of-truth)
6. **Demo seasons (target)** — `reincarnated-demo/public/seasons/season_002011/` … 002015/ (backfill writes `gauntlet_recipe.json` here)
7. **MIGRATION.md** — `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (gamora just appended v1.11; you append v1.12 for emission)

---

## Scope — five deliverables

### Deliverable 1 — Emission code in `season_writer.py:write_season()`

Per your scout's flat `slots[]` contract:

```json
{
  "schema_version": "v1.0",
  "season_id": "002011",
  "source": "balance_loop_reference_gauntlet",
  "pack_proxy_size": 8,
  "slots": [
    {
      "slot_id": 0,
      "base_monster_id": "<key from monsters.json>",
      "is_pack_proxy": false,
      "hp_multiplier": 1.0,
      "aoe_damage_multiplier": 1.0,
      "pack_size": 1
    }
  ],
  "total_slots": 12
}
```

- Read source from the balance-loop's reference gauntlet at season finalize
- Write to `<season_dir>/gauntlet_recipe.json`
- Same trigger point as monsters.json + classes.json + gear_pool.json
- No Pydantic model change required (per your scout)

### Deliverable 2 — Passthrough in `season_exporter.py:_export_season_inner()`

Copy `gauntlet_recipe.json` to the export dir alongside monsters.json. One-line addition.

### Deliverable 3 — Backfill script

New script at `reincarnated-engine/scripts/backfill_gauntlet_recipe_002011_015.py` (or your naming preference):

- Iterates 002011 through 002015
- Reads existing `reference_gauntlet.json` (ID list) from `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_<id>/`
- Reads monsters.json from `reincarnated-demo/public/seasons/season_<id>/monsters.json` (or engine source — verify which has ground truth)
- For each ID, reconstructs the richer schema (base_monster_id, is_pack_proxy, hp_multiplier, aoe_damage_multiplier, pack_size) from the monster definition + PackProxy convention
- Writes `gauntlet_recipe.json` to `reincarnated-demo/public/seasons/season_<id>/gauntlet_recipe.json`
- Logs each write for verification
- Idempotent (running twice doesn't corrupt; overwrites cleanly)

### Deliverable 4 — Run the backfill

Execute the script. Verify all 5 recipes land on disk in demo public/seasons/. Sanity-check structure (read one recipe back; confirm slot count == 12; confirm IDs resolve in monsters.json).

### Deliverable 5 — MIGRATION.md v1.12 entry

Append to `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (or wherever the seam-canonical MIGRATION lives — verify gamora's v1.11 location):

- Description: per-season `gauntlet_recipe.json` emission added; demo consumes downstream (drax v1.16 queued)
- Cross-seam impact: drax must consume; legacy seasons (001001-005) lack recipe — drax fallback to pickMonsters expected
- Backfill state: 002011-015 backfilled in place via Option A
- Discipline #15 extension: demo-as-renderer extends from visual rendering to gameplay-state fidelity

---

## Acceptance criteria

- [ ] Emission code in season_writer.py — writes valid `gauntlet_recipe.json` per the v1.0 schema
- [ ] Passthrough in season_exporter.py — recipe copies to export dir
- [ ] Backfill script authored at named path
- [ ] Backfill run completed; all 5 (002011-015) recipes present in `reincarnated-demo/public/seasons/`
- [ ] Sanity check passes: one recipe read-back confirms slot count + ID resolution
- [ ] MIGRATION.md v1.12 entry appended
- [ ] `pytest` clean on engine (or whatever your seam's smoke is)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append (jack-ryan D11.2 Gate-1 + drax v1.15 audio also active)
- [ ] AGENT_STATE STATE entry
- [ ] Tag `star-lord/v1.7-gauntlet-recipe-emission-impl-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify balance_loop.py logic (emission is read-only inspection of reference gauntlet)
- ❌ DO NOT trigger any LLM calls (Option A is pure re-derivation; $0 cost)
- ❌ DO NOT regen 002011-015 (backfill writes in place; no full regen)
- ❌ DO NOT modify monsters.json or classes.json structure (recipe is additive new file)
- ❌ DO NOT touch demo code (drax v1.16 seam; queued)
- ❌ DO NOT add the new ClassBalanceResult columns from gamora's v1.11 (separate task #119; bundle when you do it)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessor:** your scout (complete)
- **Triggers downstream:** drax v1.16 JSON-parity wiring (queued; auto-fires after drax v1.15 audio completes — same-repo serialization)
- **Parallel-safe with:** jack-ryan D11.2 Gate-1 (in flight; engine seam read-only); drax v1.15 audio (in flight; demo seam)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Verification handoff to drax v1.16 (informational; not your work)

When drax wires `gauntletFromRecipe(recipe, monsters)`, drax will:
- Consume `slots[]` directly (flat array)
- Expand `is_pack_proxy: true` slots into `pack_size` individual mobs at consume time (Matt-authorized path)
- Apply `hp_multiplier` + `aoe_damage_multiplier` to the resulting combatants
- Fallback to current `pickMonsters` if recipe missing (legacy 001001-005)
- ALSO fix the separate `Combatant.fromMonster` bug to consume `monster.max_hp` from JSON (currently ignores; fixes per-tier HP variance)

You don't have to coordinate that work; drax has the dispatch queued. Just ensure your recipe schema is what drax will be consuming.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 authorization. ~2.5h per your scout estimate. Append completion record + backfill verification log when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** star-lord
**Tag:** `star-lord/v1.7-gauntlet-recipe-emission-impl-1` @ `7bbdf13` (engine)
**Demo commit:** `de72c82` (reincarnated-demo)
**LLM cost:** $0.00 (Option A; no regen)

### Acceptance criteria — all PASS

- [x] Emission code in season_writer.py — `_gauntlet_recipe()` writes valid v1.0 `gauntlet_recipe.json`
- [x] Passthrough in season_exporter.py — `shutil.copy()` recipe to export dir; absence-guarded for legacy seasons
- [x] Backfill script authored at `scripts/backfill_gauntlet_recipe_002011_015.py`
- [x] Backfill run completed; all 5 (002011-015) recipes present in `reincarnated-demo/public/seasons/`
- [x] Sanity check PASS: season 002011 read-back — 12 slots, all IDs resolve in monsters.json
- [x] MIGRATION.md v1.12 entry appended to `src/reincarnated/simulation/MIGRATION.md`
- [x] 155 export/schema tests GREEN; `_gauntlet_recipe()` unit smoke PASS
- [x] AGENT_STATE STATE entry appended
- [x] Tag `star-lord/v1.7-gauntlet-recipe-emission-impl-1` cut

PRE-SIGNAL: dispatched to Matt/knight-rider before hive-log append.

### Backfill verification log

All 5 seasons: 12 slots (6 pack-proxy + 6 1v1). All base_monster_ids resolve in demo monsters.json. Schema v1.0.

| Season | Slots | Pack | 1v1 | Smoke |
|--------|-------|------|-----|-------|
| 002011 | 12 | 6 | 6 | PASS |
| 002012 | 12 | 6 | 6 | PASS |
| 002013 | 12 | 6 | 6 | PASS |
| 002014 | 12 | 6 | 6 | PASS |
| 002015 | 12 | 6 | 6 | PASS |

Read-back (002011): slot 0 = `monster_00001` (is_pack_proxy=True, hp_mult=8.0, aoe_mult=8.0, pack_size=8); slot 6 = `monster_00013` (is_pack_proxy=False, hp_mult=1.0, aoe_mult=1.0, pack_size=1). Schema version v1.0.

### drax v1.16 unblocked

Knight-rider has the drax v1.16 dispatch queued. Drax consumes `slots[]` directly, expands `is_pack_proxy: true` slots into `pack_size` individual mobs (Matt-authorized Option A), applies multipliers, and falls back to `pickMonsters()` for legacy seasons 001001-005.
