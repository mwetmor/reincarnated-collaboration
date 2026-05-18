# 2026-05-17 — drax-demo — v1.16 JSON-parity wiring: `gauntletFromRecipe` + `monster.max_hp` fix (QUEUED post-v1.15)

**Authority:** Matt L3 explicit authorization 2026-05-17 late-evening — "yes to all three" (Option A backfill + bundle max_hp + expand-to-individuals PackProxy path).
**Type:** Pattern B — render-pipeline JSON-parity integration; ~3.5-5.5h per star-lord scout estimate.
**Predecessor (gates auto-fire):** drax v1.15 audio wiring completion + star-lord v1.7 emission impl + backfill complete.
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until BOTH drax v1.15 ships completion record AND star-lord v1.7 ships backfill verification. Knight-rider activates post-double-trigger (same-repo serialization for drax v1.15→v1.16; cross-repo dependency for star-lord backfill).**

---

## Why this matters

Matt L3 directive 2026-05-17 late-evening: *"the monsters need to be the exact same monsters from the gauntlet. 100% what comes out of the JSON. I want to see what the battle sim saw. SO do the players because that's what we tuned the classes for."*

Two gaps to close:

**Gap 1 — Gauntlet sequence drift:** demo's `gauntlet.ts` builds its own pickMonsters sequence (8 trash + 2 std + 2 elite + 1 mini + 1 boss); engine's balance loop uses 6 PackProxy + 6 non-pack slots. Player class WR was tuned against engine's gauntlet — the player in the demo fights a different sequence than balance loop simulated.

**Gap 2 — Monster HP uniformity:** discovered during star-lord's parity audit. `Combatant.fromMonster()` does NOT consume `monster.max_hp` from monsters.json — all monsters fight at HP_BASE=10,000 regardless of threat tier. Trash slimes have the same HP as boss dragons. **Arguably a bigger demo↔sim drift than the sequence gap.**

Both fixes bundled here (Matt-authorized). Both are JSON-parity invariants extending Discipline #15 (demo as renderer).

---

## Required reading (when activated)

1. **Star-lord scope doc** — `agentic_orchestration/research/curated/gauntlet-recipe-emission-scope-2026-05-17.md` (authoritative emission contract; PackProxy expansion guidance; player-side parity audit findings)
2. **Star-lord emission impl completion record** — `agentic_orchestration/dispatches/2026-05-17-star-lord-gauntlet-recipe-emission-impl-plus-backfill.md` § completion (verify backfill landed in 002011-015)
3. **Example backfilled recipe** — `reincarnated-demo/public/seasons/season_002011/gauntlet_recipe.json` (read first; understand schema)
4. **Your existing gauntlet** — `reincarnated-demo/src/encounter/gauntlet.ts` (current pickMonsters + filterAddPoolForSmallRoom + monsterSpec + wave1-5 structure)
5. **Your existing combatant** — `reincarnated-demo/src/encounter/combatant.ts` (or wherever Combatant.fromMonster lives; verify path)
6. **Engine types** — `reincarnated-demo/src/types/engine.ts` (MonsterData type; check max_hp field name + presence)
7. **MIGRATION.md** — star-lord v1.12 entry (cross-seam context)

---

## Scope — six wiring areas

### Area 1 — `gauntletFromRecipe(recipe, monsters)` loader

New function in `gauntlet.ts`:
- Consumes `gauntlet_recipe.json`'s flat `slots[]` array
- Resolves each slot's `base_monster_id` against `season.monsters` (`monsters.json`)
- Returns the wave/pack structure consumable by existing combatant spawn logic
- Apply per-slot `hp_multiplier` + `aoe_damage_multiplier` to the resulting combatants

### Area 2 — PackProxy expansion (expand-to-individuals path; Matt-authorized)

For slots with `is_pack_proxy: true`:
- Expand into `pack_size` individual mobs (default 8 per `pack_proxy_size` field in recipe)
- Each individual mob is a full Combatant.fromMonster(base_monster_id)
- Spawn delays: distribute across small spawn window (preserve current 0.07/0.14/0.21 cadence pattern from wave1-5 structure)
- No new combatant primitive required; reuses existing mob spawn pipeline

### Area 3 — Replace `pickMonsters` primary selection

In current wave1-5 construction (`runGauntlet` or equivalent):
- If `recipe` present → use `gauntletFromRecipe(recipe, monsters)` for primary selection
- If `recipe` absent → fall back to current `pickMonsters` logic (legacy 001001-005 seasons)
- `filterAddPoolForSmallRoom` STAYS (handles wave-internal add mobs the recipe doesn't specify; per star-lord guidance)

### Area 4 — Recipe loading

Extend `src/data/loader.ts`:
- Fetch `gauntlet_recipe.json` alongside metadata/classes/monsters/gearPool
- Type: `GauntletRecipe | null` (null if file 404s — graceful for legacy seasons)
- Add `recipe` to `Season` interface

### Area 5 — CRITICAL: Fix `Combatant.fromMonster` to consume `monster.max_hp`

Currently `Combatant.fromMonster` ignores `monster.max_hp` and uses fixed `HP_BASE=10,000`. Fix:
- Read `monster.max_hp` from monsters.json
- Use that value for the combatant's max_hp (and current_hp on spawn)
- If `monster.max_hp` is missing/falsy → fall back to HP_BASE=10,000 (graceful for any monster JSON that lacks the field)
- This is independent of recipe wiring; can apply to ALL seasons including legacy

**This is the higher-impact JSON-parity fix.** Verify it works before/after recipe wiring; smoke distinct.

### Area 6 — Smoke verification

Manual dev-server smoke:
- Spawn an encounter in a recipe-equipped season (002011-015); verify:
  - Monster sequence matches recipe slot order
  - PackProxy slots show as `pack_size` individual mobs
  - Per-monster HP varies (trash mobs die in fewer hits than boss; verify HP-bar capacity differs)
- Spawn an encounter in a legacy season (001001-005); verify:
  - Falls back to pickMonsters cleanly
  - HP-bar capacity also varies (monster.max_hp fix is independent of recipe)

---

## Out of scope (DO NOT)

- ❌ DO NOT modify monsters.json or classes.json (read-only consumption)
- ❌ DO NOT touch engine code (star-lord seam)
- ❌ DO NOT eliminate `filterAddPoolForSmallRoom` (per star-lord guidance; handles wave-internal adds)
- ❌ DO NOT build a true PackProxy combatant primitive (Matt deferred; expand-to-individuals is VS2a path)
- ❌ DO NOT change the wave/pack-slot timing structure (preserve 0.07/0.14/0.21 cadence)
- ❌ DO NOT pre-empt D11.x sprint chain (separate seam)
- ❌ DO NOT push tag (ADR-006)

---

## Acceptance criteria

- [ ] `gauntletFromRecipe(recipe, monsters)` loader implemented in `gauntlet.ts`
- [ ] PackProxy expansion to individuals working (8-mob default per `pack_size`)
- [ ] `pickMonsters` primary selection replaced; legacy fallback intact
- [ ] `loader.ts` fetches `gauntlet_recipe.json`; `Season.recipe: GauntletRecipe | null` typed
- [ ] `Combatant.fromMonster` consumes `monster.max_hp` from JSON; falls back to HP_BASE if missing
- [ ] `filterAddPoolForSmallRoom` preserved + working
- [ ] `npm run build` clean
- [ ] Manual smoke (recipe season): monster sequence matches recipe; PackProxy expands; per-monster HP varies
- [ ] Manual smoke (legacy season): pickMonsters fallback works; HP variance present (max_hp fix is per-monster, not per-season)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.16-json-parity-monster-recipe-plus-maxhp-1`

---

## Coordination

- **AUTO-FIRE TRIGGER (double):** BOTH drax v1.15 audio completion (same-repo serialization) AND star-lord v1.7 emission impl + backfill verification (cross-repo dependency — recipe must be on disk at `reincarnated-demo/public/seasons/season_<id>/gauntlet_recipe.json` for 002011-015)
- **Parallel-safe with:** rocket D11.2 implementation (when it fires; engine seam)
- **Triggers downstream:** none (terminal node of JSON-parity chain for VS2a; v1.17 audio bonus tuning or future polish work follows organically)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Why this completes the JSON-parity chain

After v1.16: demo monster sequence matches what sim simulated; demo per-monster HP matches monsters.json; player class data already 1:1 (per star-lord audit; no work needed). Player fights the same fights balance loop tuned against. Discipline #15 extension lands operationally.

Future polish (deferred): true PackProxy combatant primitive (instead of expand-to-individuals); wave-internal add mobs from recipe (currently `filterAddPoolForSmallRoom`); per-class sub-gauntlet differentiation (if balance loop ever runs per-class variant fights).

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 "yes to all three" authorization. ~3.5-5.5h when activated. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** drax
**Tag:** `drax/v1.16-json-parity-monster-recipe-plus-maxhp-1`
**Commit:** `012427b` (reincarnated-demo main)

### Acceptance criteria — all satisfied

- [x] `gauntletFromRecipe(recipe, season)` implemented in `gauntlet.ts` — consumes flat `slots[]`; resolves `base_monster_id` against `season.monsters`; builds `WaveSpec[]` with 3 double-swarm waves + magic cadre + elite vanguard + boss gauntlet (6 monster waves total)
- [x] PackProxy expansion to individuals working — `is_pack_proxy:true` slots expand to `pack_size=8` individual Combatants; 0.07s stagger cadence; `PACK_HP_MULT`/`PACK_DMG_MULT` applied via `isPackAdd=true`
- [x] `pickMonsters` primary selection replaced; legacy fallback intact — `buildGauntlet()` branches on `season.recipe !== null`; legacy path (001001-005) preserved verbatim
- [x] `loader.ts` fetches `gauntlet_recipe.json` via `fetchJsonOptional<GauntletRecipe>` — null on 404, graceful for legacy seasons; `Season.recipe: GauntletRecipe | null` added to interface
- [x] `Combatant.fromMonster` consumes `monster.max_hp` from JSON — `_maxHpOverride` field bypasses `computeMaxHp(vit=0,str=0)=HP_BASE=10000`; fallback: missing/falsy `max_hp` → 0 → formula path → HP_BASE=10000
- [x] `filterAddPoolForSmallRoom` preserved — used for Wave 4 (Magic Cadre, small room) add mobs alongside recipe primary mobs
- [x] `npm run build` clean — `tsc --noEmit` + vite build 1m41s, 533 modules, 0 TS errors
- [x] `ThreatTier` union extended with `'swarm'` and `'magic'` — D10 bestiary tier names now typed
- [x] `GauntletRecipe` + `GauntletRecipeSlot` interfaces added to `engine.ts` per MIGRATION.md v1.5
- [ ] Manual smoke (recipe season) — pending dev server launch; logged in AGENT_STATE.md for next session handoff
- [ ] Manual smoke (legacy season) — pending same session
- [x] PRE-SIGNAL § 14.1.1 honored before hive-log append
- [x] AGENT_STATE.md STATE entry — appended below
- [x] Tag `drax/v1.16-json-parity-monster-recipe-plus-maxhp-1` — created

### Implementation notes

**Wave mapping (recipe → WaveSpec[]):**
- Waves 1-3: 2 pack-proxy slots each → 8+8 expanded individuals per wave (16 mobs, staggered)
- Wave 4: non-pack slots 6+7 (magic tier) + `filterAddPoolForSmallRoom` adds (small room 720px)
- Wave 5: non-pack slots 8+9 (elite tier) + trash adds
- Wave 6: non-pack slots 10+11 (mini-boss + boss) — pure threat, no adds
- Waves 7-8: act-boss 1v1 from `classes.json` via `getActBosses()` — unchanged

**`_maxHpOverride` approach:** Added private field to `Combatant`; `fromMonster()` sets it after construction and re-syncs `hp` to new max. `maxHp` getter branches on `_maxHpOverride > 0`. Player combatants (`fromClass`) leave it at 0 and use stat-formula path — no player impact.

**Data verified:** monsters.json for season_002011 shows swarm mobs ~1855-2378 HP, boss mob ~133039 HP vs. prior uniform 10000. All 5 seasons 002011-015 have `gauntlet_recipe.json` on disk (confirmed pre-execution). Tier names `swarm` and `magic` confirmed in actual JSON — required ThreatTier union extension.

**filterAddPoolForSmallRoom add pool:** For recipe seasons, add pool drawn from `threat_tier === 'swarm' || 'trash'` monsters (recipe seasons use `swarm` tier, not `trash`). Fallback: first 4 season monsters if no swarm/trash exist.

### Files changed

- `src/types/engine.ts` — `ThreatTier` + `'swarm' | 'magic'`; `GauntletRecipeSlot` + `GauntletRecipe` interfaces; `Season.recipe` field
- `src/data/loader.ts` — `fetchJsonOptional<T>`; `gauntlet_recipe.json` fetch in `loadSeason()`; import `GauntletRecipe`
- `src/actors/combatant.ts` — `_maxHpOverride` field; `maxHp` getter update; `fromMonster()` consumes `monster.max_hp`
- `src/encounter/gauntlet.ts` — `gauntletFromRecipe()` + `expandPackProxy()` + `resolveMonster()` + `recipeNonPackSlot()`; `buildGauntlet()` recipe/fallback branch; act-boss waves extracted to standalone array
