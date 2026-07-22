# GD Datamine Manifest

**Source:** grimtools.com/monsterdb (Grim Dawn Monster Database — community tool by Dammitt)
**Upstream URL:** https://www.grimtools.com/monsterdb/
**Retrieval method:** Fetched `monsterdb.js` (7.9 MB JavaScript file containing embedded data objects) from Cloudflare-served static asset URL; then extracted named data blocks via Python regex into individual `.js` files. No scraping storm; single HTTP request for the data payload.
**Retrieval date:** 2026-07-21
**Upstream version:** Grim Dawn Version 1.3.0.0 (embedded in `monsterdb.js` as `window.gameVersion`)
**Asset fingerprint (cache-buster):** `?1784288160` (timestamp-style; this will change on future deploys)
**Data source URL used:** `https://www.grimtools.com/monsterdb/js/monsterdb.js?1784288160`

**ARCHITECTURE NOTE:** grimtools monsterdb is a jQuery-based SPA with no exposed REST JSON API. All monster data is embedded inline as JavaScript object literals in `monsterdb.js`. The file is 7.9 MB and contains 31 `window.X=` data assignments covering monsters, skills, spawn data, difficulty scaling, and engine constants. Individual data blocks were extracted to separate files for usability.

---

## File inventory

| File | Size | Description |
|---|---|---|
| `monsterdb.js` | 7,898,908 bytes | Full source JS file — retained as provenance record. Contains all 31 data blocks. |
| `all_monsters.js` | 3,534,366 bytes | `window.allMonsters` — 2,716 monster entries. Per-monster: resistances (resFire/resCold/resLightning/resPoison/resPierce/resBleeding/resLife/resAether/resChaos/resPhysical), characterRunSpeed, monsterClassification (Normal/Champion/Hero/Boss), skill slot references (specialAttack2/3/4SkillName, specialAttackChance, specialAttackRange), skillLevel formulas (e.g. `"charLevel/4+1"`). |
| `all_skills.js` | 3,013,785 bytes | `window.allSkills` — All GD skill definitions including damage types, formulas, durations, radius, pet summoning parameters. |
| `monster_data.js` | 388,786 bytes | `window.monsterData` — masterTables (loot table compositions, weights) and additional item/loot distribution data. |
| `monster_difficulty.js` | 17,417 bytes | `window.monsterDifficulty` — Per-monster difficulty availability array (which GD difficulties/acts a monster appears in). |
| `monster_pool.js` | 6,366 bytes | `window.monsterPool` — Pack/zone monster pool definitions. |
| `monster_spawns.js` | 264,174 bytes | `window.monsterSpawns` — Per-area spawn roster (which monsters appear in each zone). |
| `spawn_locations.js` | 8,253 bytes | `window.spawnLocations` — Zone ID to localization tag mapping (e.g. `l152:"tagUGVoidlands01A"`). |
| `monster_tier.js` | 121 bytes | `window.monsterTier` — Tier classification enum. |
| `engine.js` | 315 bytes | `window.engine` — Engine constants (milestones, speed caps, armor absorption formula). |
| `monster_adjustments.js` | 3,875 bytes | `window.monsterAdjustments` — Per-difficulty stat modifier arrays for OA, DA, resists, speed, life regen, block. |

**Total raw payload:** ~14 MB (11 files; includes full monsterdb.js as provenance record)

---

## Coverage read vs matrix category grades

| Category | Matrix grade | What landed | Assessment |
|---|---|---|---|
| A — Skills | A | `all_skills.js` (3.0 MB) | CONFIRMED PARTIAL A. Skill definitions present; field structure uses formula expressions analogous to GD DBRs. Exact numeric baseline values require formula evaluation against character level. Full A coverage for skill shapes; oracle-grade exact-numeric use requires expression parser. |
| B — Monsters | A | `all_monsters.js` (2,716 monsters); `monster_adjustments.js` (per-difficulty modifiers) | CONFIRMED A for resistance structure and classification. Per-monster resistance fields confirmed (resFire, resCold, resLightning, resPoison, resPierce, resBleeding, resLife, resAether, resChaos, resPhysical). Speed field `characterRunSpeed` present as multiplier. HP/damage raw values NOT directly present in `allMonsters` — grimtools computes HP/DPS dynamically from base-stat tables and `monsterAdjustments`. See gap #1. |
| C — Areas | B | `monster_spawns.js` (264 KB) + `spawn_locations.js` | CONFIRMED B. Per-zone spawn rosters present. Zone IDs map to localization tags. Absolute area geometry (SizeX/SizeY equivalent) not tabular — confirmed gap from coverage matrix. |
| D — Items/Affixes | A | Not extracted in this pass — grimtools.com/db is the items database, separate from monsterdb | NOT FETCHED. Items/affixes are at grimtools.com/db (separate tool). Coverage matrix grades D as A via AssetManager DBR extraction. Phase 2: fetch from grimtools.com/db or use AssetManager on game install. |
| E — Calculator | A | grimtools.com/calc is the community reference — not fetched locally | NOT FETCHED. grimtools calc is the VDM-CAL oracle for GD. Not open-source but functionally a closed oracle. Available at https://www.grimtools.com/calc/. |

---

## Key data structure notes for VDM-2 use

**Monster resistances:** In `all_monsters.js`, resistance fields (`defensiveChaos`, `defensiveCold`, etc.) appear as DELTA values, not absolute percentages. The base resistance floor is set by `monsterAdjustments` difficulty arrays; per-monster fields are additive modifiers on top. VDM-2 exact-numeric comparison requires: base_resist (from `monsterAdjustments[difficulty]`) + delta (from `allMonsters[mId]`).

**Monster HP/DPS:** `allMonsters` does NOT directly contain HP or DPS numbers — these are computed by the browser JS at render time from base-stat scaling tables (which ARE in the data: `monsterAdjustments` provides life multipliers, `engine` has base parameters). Reconstruction requires either: (a) reverse-engineering the JS computation from `monsterdb.js` application code, or (b) fetching individual monster pages from grimtools and parsing rendered HTML output, or (c) using the AssetManager DBR extraction path (requires game install).

**Speed field:** `characterRunSpeed` in `allMonsters` is a multiplier relative to a base speed constant (not raw in-game units). The `engine` object and `monsterAdjustments.characterRunSpeedModifier` array supply the conversion context.

---

## Named gaps (what Phase-2 or an install would add)

1. **HP and DPS raw values** — grimtools computes these dynamically; they are not stored directly in the embedded JS data. To get absolute per-monster HP and DPS at a given level/difficulty: (a) parse the grimtools computation from `monsterdb.js` application code (feasible but requires reverse-engineering ~7.9MB of minified jQuery), or (b) individual page fetches with headless browser, or (c) AssetManager DBR extraction (game install required — the clean path). This is the primary gap for VDM-2 exact-numeric monster overlay.

2. **GD item/affix data** — `grimtools.com/db` (separate tool) covers items and affixes. The `monsterdb.js` payload contains loot table structures (`monsterData.masterTables`) but not base item stat ranges or affix pool details. Phase 2: fetch from grimtools.com/db or use `abclution/GrimDawn_DB_to_CSV_Extractor` with game install.

3. **Skill numeric parameters** — `all_skills.js` skill definitions use formula expressions (e.g. skill level as a variable). Exact numeric values at specific character/skill levels require formula evaluation. A simple expression parser would resolve most cases.

4. **AssetManager DBR path** — Full A-grade exact numerics for HP, DPS, and skill values require GD game install (Steam, ~5 GB) + AssetManager.exe extraction. This is the Phase 2 upgrade path. Crate Entertainment explicitly endorses this.

---

## License / provenance

grimtools.com is a community tool (2017-2026, by Dammitt); not affiliated with Crate Entertainment. Crate has linked to grimtools from official channels and explicitly endorses modding. No API key, auth, or account required for this fetch. The `monsterdb.js` file is publicly served as a static asset. Data originates from GD game files extracted via Crate's officially provided AssetManager.

---

## Elrond-ready pointer

Raw data at: `agentic_orchestration/research/datamine-acquisition/gd/raw/` (gitignored)
Priority file for VDM-2 monsters lane: `all_monsters.js` (resistance deltas + speed multipliers + classification; requires `monster_adjustments.js` for difficulty offsets)
Priority file for VDM-2 skills lane: `all_skills.js` (formula-based; requires expression evaluation)
Spawn/area data: `monster_spawns.js` + `spawn_locations.js`
HP/DPS gap: requires Phase-2 AssetManager extraction or grimtools compute reverse-engineering
