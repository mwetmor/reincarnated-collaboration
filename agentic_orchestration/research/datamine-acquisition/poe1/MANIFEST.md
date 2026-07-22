# PoE1 Datamine Manifest

**Source:** brather1ng/RePoE (GitHub mirror of GGG GGPK-extracted data)
**Upstream URL:** https://github.com/brather1ng/RePoE
**Retrieval method:** Direct fetch via raw.githubusercontent.com (no auth, no extraction tooling required)
**Retrieval date:** 2026-07-21
**Upstream commit SHA:** 8023a1d696dbddc836c05ac3fcedd072da1767d2 (brather1ng/master, last pushed 2022-09-06)

**IMPORTANT STALENESS NOTE:** brather1ng/RePoE has not been pushed since 2022-09-06. The actively maintained fork is `repoe-fork/repoe` (https://github.com/repoe-fork/repoe), which was last updated 2026-07-14 (commit `14e3edc89ed705bd4e4eda5c8135756431c76e81`). The data fetched here reflects a stable 3.x-era snapshot. For current league data (3.24+), re-fetch from repoe-fork. For VDM-2 verification of the 94-kit PoE1 corpus (skills fixed before 2022), brather1ng is sufficient.

---

## File inventory

| File | Size | Description |
|---|---|---|
| `gems.json` | 9,711,510 bytes | 1,017 gem entries; per-gem per-level stat tables (damage, cost, cast time, AoE radius, duration, projectile count, crit, etc.). Primary skills lane. |
| `mods.json` | 23,242,299 bytes | 30,909 affix entries; domain, generation type, spawn weights, tiers, stat ranges. Complete affix pool. |
| `stat_translations.json` | 4,391,199 bytes | Human-readable translation table mapping raw stat IDs to display strings. Required to interpret `gems.json` stat arrays. |
| `base_items.json` | 2,640,707 bytes | 4,028 base item entries; item class, drop level, implicits, inventory dimensions, properties. |
| `stats.json` | 1,977,393 bytes | Stat ID registry; maps internal stat identifiers to metadata. Companion to stat_translations. |
| `active_skill_types.json` | 1,964 bytes | Enum of active skill type flags. Small; used for skill categorization. |
| `default_monster_stats.json` | 15,584 bytes | Per-level monster base stat table (levels 1-100); fields: accuracy, ally_life, armour, evasion, life, physical_damage. This is the scaling curve table, not per-monster individual values. |

**Total raw payload:** ~41 MB

---

## Coverage read vs matrix category grades

| Category | Matrix grade | What landed | Assessment |
|---|---|---|---|
| A — Skills | A | `gems.json`: 1,017 gems, full per-level stat arrays | CONFIRMED A. Per-gem, per-level numeric tables for damage, cost, cast time, AoE, duration, projectile count, crit, stat requirements. Exact field values present. |
| B — Monsters | B | `default_monster_stats.json`: scaling curve (level 1-100, 6 stat fields) | CONFIRMED B. Scaling table present but is a base curve, not per-monster individual HP/damage/resist values. Per-monster extracted stats require PyPoE `.dat` file extraction from GGPK (Phase 2 or install path). |
| C — Areas | B | Not fetched in this pass | NOT FETCHED. Coverage matrix grades this B; `poedb.tw` and RePoE area records would supply pack composition and density modifiers. Phase 2 item. |
| D — Items/Affixes | A | `mods.json` (30,909 affixes) + `base_items.json` (4,028 bases) | CONFIRMED A. Complete affix pool with spawn weights, tiers, stat ranges, domain, generation type. |
| E — Calculator | A | Not fetched (PoB is a separate repo, ~Lua codebase) | NOT FETCHED in this pass. Path of Building (PathOfBuildingCommunity/PathOfBuilding) is the oracle; it is open-source Lua and does not require download to cite. Phase 2: clone PoB for local VDM-CAL use. |

---

## Named gaps (what Phase-2 or an install would add)

1. **Per-monster individual stat tables** — `default_monster_stats.json` provides the level-scaling curve but not per-monster HP multipliers, resistances, or damage ranges. Full per-monster coverage requires PyPoE extraction from GGPK (game install path) or sourcing from poedb.tw structured data. This is the primary B→A upgrade path for the monsters lane.

2. **Area/pack-composition records** — `RePoE` contains area-related data but was not fetched in this pass. `poedb.tw` area pages have pack composition and density modifier data. Phase 2.

3. **Current-league data staleness** — brather1ng fetch reflects pre-2022 state. PoE1 has had numerous skill reworks since then (3.16-3.24). For corpus kits referencing current skill values, re-fetch from `repoe-fork/repoe` (last updated 2026-07-14).

4. **Stat translation linkage** — `gems.json` stat arrays use internal stat IDs (e.g. `damage_effectiveness`). `stat_translations.json` maps these to human-readable strings. VDM-2 numeric comparison requires matching stat IDs to canonical VDM field names. A mapping pass is needed before exact-numeric overlay can begin.

5. **Path of Building oracle** — PoB not yet cloned locally. It is the VDM-CAL reference. Phase 2: `git clone https://github.com/PathOfBuildingCommunity/PathOfBuilding`.

---

## License / provenance

RePoE is licensed MIT (brather1ng README). Underlying data is extracted from Path of Exile game files (GGG property). GGG has explicitly endorsed PyPoE and community data tools; community-normal posture is well-established. No auth or account required for this fetch. Data is publicly accessible via GitHub.

---

## Elrond-ready pointer

Raw data at: `agentic_orchestration/research/datamine-acquisition/poe1/raw/` (gitignored)
Priority files for VDM-2 skills lane: `gems.json` + `stat_translations.json`
Priority files for VDM-2 items lane: `mods.json` + `base_items.json`
Monster scaling curve: `default_monster_stats.json`
