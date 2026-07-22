# Phase-1 Datamine Acquisition Log — 2026-07-21

**Executed by:** legolas
**Authorization:** Matt 2026-07-21 corpus ruling — Phase-1 items 1-3
**Purpose:** Feed VDM-2 exact-numeric field verification + VDM-CAL calibration for 5-roster (D2/GD/PoE1/PoE2/LE)

---

## What landed

### PoE1 — brather1ng/RePoE

**Status: LANDED**
**Method:** Direct raw.githubusercontent.com fetch (no auth, no extraction tooling)
**Upstream commit:** `8023a1d696dbddc836c05ac3fcedd072da1767d2` (brather1ng/master)
**Payload:** 7 JSON files, ~41 MB total

| File | Size | Content |
|---|---|---|
| gems.json | 9.7 MB | 1,017 gems, per-level stat arrays |
| mods.json | 23.2 MB | 30,909 affixes with spawn weights/tiers |
| stat_translations.json | 4.4 MB | Stat ID to display string mapping |
| base_items.json | 2.6 MB | 4,028 base items |
| stats.json | 2.0 MB | Stat ID registry |
| default_monster_stats.json | 15.6 KB | Level 1-100 monster scaling curve (6 fields) |
| active_skill_types.json | 1.9 KB | Skill type enum |

**Coverage confirmed:** Skills A, Items/Affixes A, Monster scaling curve B (per-monster individual values not in RePoE)

**Staleness flag:** brather1ng was last updated 2022-09-06. `repoe-fork/repoe` (commit `14e3edc`, 2026-07-14) is the live-maintained fork. For current PoE1 data (3.24+), re-fetch from repoe-fork. For 94 corpus-kit verification against stable skills, current payload is sufficient.

---

### D2 — fabd/diablo2

**Status: LANDED**
**Method:** Direct raw.githubusercontent.com fetch (no auth, no extraction tooling)
**Upstream commit:** `45112569deb9384738ccafe5c24ebbb71f41c7c9` (fabd/master)
**Payload:** 34 TSV files, ~1.7 MB total (D2 1.13 data)

Priority files confirmed:

| File | Size | Columns | Content |
|---|---|---|---|
| Skills.txt | 173 KB | 256 | Per-skill base damage, cast time, mana, projectile, level-scaling formulas |
| MonStats.txt | 432 KB | 255 | Per-monster HP, damage, resists, speed (÷25), aggro, pack size |
| Levels.txt | 66 KB | 140 | Per-area SizeX/SizeY, density, spawn roster |
| TreasureClassEx.txt | 87 KB | — | Drop pool definitions |
| Armor.txt + Weapons.txt | 194 KB | — | Base items |
| MagicPrefix.txt + MagicSuffix.txt | 122 KB | — | Affix pools |
| UniqueItems.txt | 73 KB | — | All unique items |
| + 26 supplemental files | ~550 KB | — | MonStats2, MonLvl, MonAi, Properties, Sets, Runes, CubeMain, CharStats, etc. |

**Coverage confirmed:** Skills A, Monsters A, Areas A (Levels.txt is the unique area-geometry source in the entire 20-game survey), Items/Affixes A

**Version note:** D2 1.13 classic. D2R CASC extraction would supply current D2R balance values — Phase 2 item.

---

### GD — grimtools monsterdb (monsterdb.js extraction)

**Status: LANDED — PARTIAL (see gap)**
**Method:** Fetched `monsterdb.js` static asset (7.9 MB embedded-data JS file); extracted 10 named data blocks via Python; saved as individual `.js` files
**Upstream version:** GD 1.3.0.0 (embedded in file)
**Payload:** 11 files (10 extracts + source file), ~14 MB total

| File | Size | Content |
|---|---|---|
| all_monsters.js | 3.5 MB | 2,716 monsters; resistances (10 types), speed multiplier, classification, skill refs |
| all_skills.js | 3.0 MB | All GD skill definitions with formula expressions |
| monster_spawns.js | 264 KB | Per-zone spawn rosters |
| monster_data.js | 389 KB | Loot table master structure |
| monster_difficulty.js | 17 KB | Per-monster difficulty availability |
| monster_adjustments.js | 3.9 KB | Per-difficulty OA/DA/resist/speed modifier arrays |
| spawn_locations.js | 8.3 KB | Zone ID to localization tag map |
| monster_pool.js + monster_tier.js + engine.js | 7 KB | Engine constants, pool defs, tier enum |
| monsterdb.js (source) | 7.9 MB | Full provenance record |

**Architecture finding:** grimtools monsterdb has NO exposed REST/JSON API. Data is embedded in a single 7.9 MB JS file as JavaScript object literals. `window.allMonsters` alone is 3.5 MB covering 2,716 monsters. Individual monster records contain resistance deltas (not absolute values) and speed multipliers (not raw units). HP and DPS are computed at render time by browser JS — NOT stored directly in the payload.

**Coverage confirmed:** Monsters B-to-A (resistance structure A; HP/DPS gap — see below), Skills partial A (formula-based), Areas B (spawn rosters; no absolute geometry), Items NOT fetched (separate grimtools.com/db tool)

---

## Top three gaps

**Gap 1 — GD monster HP/DPS are absent from the pre-built payload.** `window.allMonsters` stores resistance deltas and speed multipliers, not absolute HP or DPS. The grimtools browser computes HP/DPS dynamically from base-stat tables and difficulty modifiers. Closing this gap requires either: (a) reverse-engineering the JS computation from `monsterdb.js` application code, or (b) GD game install + AssetManager DBR extraction (Crate-endorsed path, ~5 GB, half-day effort). This is the most significant gap for VDM-2 exact-numeric GD monster overlay.

**Gap 2 — PoE1 per-monster individual stat values not in RePoE.** `default_monster_stats.json` is a level-scaling curve (100 rows, 6 fields), not per-monster individual HP/damage/resists. Per-monster exact values require PyPoE GGPK extraction or poedb.tw structured data. Matrix grades this B; confirmed B.

**Gap 3 — GD and PoE1 items/affixes not fetched in Phase 1.** GD items are in grimtools.com/db (separate tool); PoE1 items ARE fetched (mods.json, base_items.json). GD item gap is a Phase-2 item: grimtools.com/db fetch or AssetManager DBR extraction.

---

## VDM-2 readiness assessment

**D2 (60 corpus kits):** Ready to begin VDM-2 field-delta verification. Skills.txt, MonStats.txt, Levels.txt all landed with exact numeric values. The only work before overlay is formula parsing for skill expressions (SkillCalc.txt provides the function table). VDM-CAL grade B (no unified oracle) — partial coverage via pydiablo.

**GD (41 corpus kits):** Partial readiness. Resistance and classification data are present (A-grade for resist overlay). Speed and spawn-roster data present. HP and DPS overlay blocked until AssetManager extraction (Phase 2) or JS computation reverse-engineering. Skills lane: formula expressions present but require evaluation step. VDM-CAL grade A (grimtools calc is the reference, even though not open-source).

**PoE1 (94 corpus kits):** Ready to begin VDM-2 skills field-delta verification. `gems.json` has 1,017 gems with per-level stat arrays. Monster overlay partial (scaling curve only, not per-monster). Items overlay ready (mods.json + base_items.json). The stat_translations.json linkage step is required before exact-numeric field matching — stat arrays use internal IDs, not display names. VDM-CAL grade A (PoB is the oracle; Phase 2: clone locally).

**Overall verdict for Elrond:** D2 is the most immediately usable source — flat TSVs, no formula evaluation required for most fields, exact numerics throughout. PoE1 skills overlay can start immediately pending stat ID mapping pass. GD requires Phase-2 HP/DPS resolution before full monster overlay is possible.

---

## Elrond-ready pointers

| Source | Raw data path | Priority files |
|---|---|---|
| PoE1 | `datamine-acquisition/poe1/raw/` | gems.json, mods.json, stat_translations.json |
| D2 | `datamine-acquisition/d2/raw/` | Skills.txt, MonStats.txt, Levels.txt, TreasureClassEx.txt |
| GD | `datamine-acquisition/gd/raw/` | all_monsters.js, all_skills.js, monster_adjustments.js, monster_spawns.js |

All raw directories are gitignored. Full per-source detail in individual MANIFEST.md files at `poe1/MANIFEST.md`, `d2/MANIFEST.md`, `gd/MANIFEST.md`.
