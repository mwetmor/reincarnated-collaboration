# D2 Datamine Manifest

**Source:** fabd/diablo2 (GitHub mirror of Diablo II 1.13 data files)
**Upstream URL:** https://github.com/fabd/diablo2
**Retrieval method:** Direct fetch via raw.githubusercontent.com; files at `code/d2_113_data/`. No auth, no extraction tooling required.
**Retrieval date:** 2026-07-21
**Upstream commit SHA:** 45112569deb9384738ccafe5c24ebbb71f41c7c9 (fabd/master, last pushed 2021-08-31)
**Game version:** Diablo II 1.13 (classic; not D2R CASC packaging)

**VERSION NOTE:** This mirror captures D2 1.13 data. D2R (Resurrected) contains the same TSV schema but with some balance changes (e.g. rune word adjustments). For D2R-specific values, the CASC extraction path via CASCExplorer is the Phase-2 route; community-normal and Blizzard-tolerated. For the 60-kit corpus (vanilla D2 kits), 1.13 data is the canonical reference.

---

## File inventory

| File | Size | Description |
|---|---|---|
| `Skills.txt` | 173,177 bytes | 256-column TSV. Per-skill base min/max damage, cast time, mana cost, projectile params, range, duration, per-level scaling formulas, synergy references. Primary skills lane. |
| `Missiles.txt` | 192,294 bytes | Projectile geometry — speed, velocity, range, collision, effect. Used in conjunction with Skills.txt for projectile skills. |
| `MonStats.txt` | 431,898 bytes | 255-column TSV. Per-monster HP, damage, resists, speed (Velocity/Run at 25fps — divide by 25 for m/s), aggro range (aidist), reaction time (aidel), AI behavior, pack size (MinGrp/MaxGrp), skill entries. Primary monsters lane. |
| `MonStats2.txt` | 137,931 bytes | Monster secondary stats — resistances, immunities, color, SFX. Companion to MonStats.txt. |
| `Levels.txt` | 66,476 bytes | 140-column TSV. Per-area SizeX/SizeY (Normal/Nightmare/Hell), MonDen (density), MonUMin/Max (unique count), NumMon, per-difficulty monster spawn roster. Unique tabular area-geometry source. Primary areas lane. |
| `TreasureClassEx.txt` | 87,399 bytes | Treasure class definitions — drop pool, pick count, weights. Primary for drop distribution analysis. |
| `ItemStatCost.txt` | 39,749 bytes | Per-stat metadata — encoding, min/max values, operations, display strings, carry1 flag. |
| `Armor.txt` | 76,166 bytes | Base armor items — AC range, block, sockets, requirements, durability. |
| `Weapons.txt` | 117,721 bytes | Base weapon items — damage, speed, range, sockets, requirements, two-hand flag. |
| `MagicPrefix.txt` | 56,917 bytes | Magic prefix affix pool — mod properties, levels, spawn weights, class restrictions. |
| `MagicSuffix.txt` | 65,114 bytes | Magic suffix affix pool (same schema as MagicPrefix). |
| `UniqueItems.txt` | 73,206 bytes | All unique items — base type, required level, properties (12 property slots). |
| `SetItems.txt` | 26,805 bytes | Set item definitions — base type, required level, property slots, set membership. |
| `Sets.txt` | 6,287 bytes | Set bonus definitions — partial and full set bonuses. |
| `Runes.txt` | 20,342 bytes | Rune word definitions — rune sequence, socket requirements, resulting properties. |
| `CharStats.txt` | 3,351 bytes | Per-class base stats — strength, dexterity, vitality, energy, starting values, per-level increments. |
| `Properties.txt` | 26,545 bytes | Property definitions — stat function codes, min/max set/add/multiply semantics. |
| `CubeMain.txt` | 30,364 bytes | Horadric Cube recipe table — input components, outputs, conditions. |
| `SuperUniques.txt` | 8,003 bytes | Super-unique monster definitions — name, base monster, TC, equipment. |
| `MonLvl.txt` | 14,595 bytes | Monster level table per difficulty and area act. |
| `MonProp.txt` | 2,440 bytes | Monster property mods (champion/unique affixes). |
| `MonType.txt` | 1,303 bytes | Monster type flags (demons, undead, animals). |
| `MonUMod.txt` | 2,448 bytes | Unique monster modifier pool — names and properties. |
| `MonAi.txt` | 7,538 bytes | Monster AI types and parameters. |
| `MonEquip.txt` | 1,717 bytes | Monster starting equipment definitions. |
| `MonPlace.txt` | 620 bytes | Monster placement rules. |
| `MonPreset.txt` | 3,364 bytes | Preset monster definitions per level. |
| `ItemRatio.txt` | 655 bytes | Item drop quality ratio table. |
| `ItemTypes.txt` | 8,670 bytes | Item type hierarchy — parent types, flags. |
| `ElemTypes.txt` | 181 bytes | Elemental type enum. |
| `Experience.txt` | 7,014 bytes | XP table per level per class. |
| `Gems.txt` | 7,723 bytes | Gem socketing effects per weapon/armor/shield. |
| `SkillCalc.txt` | 1,943 bytes | Skill calculator helper formulas. |
| `SkillDesc.txt` | 64,914 bytes | Skill description strings and formatting templates. |

**Total raw payload:** ~1.7 MB (34 files)

---

## Coverage read vs matrix category grades

| Category | Matrix grade | What landed | Assessment |
|---|---|---|---|
| A — Skills | A | `Skills.txt` (256 cols) + `Missiles.txt` + `SkillCalc.txt` + `SkillDesc.txt` | CONFIRMED A. 256-column TSV with per-skill base damage, cast time, mana cost, projectile params, range, duration, per-level scaling formulas (param1/ln/...), synergy references. Exact numeric values. |
| B — Monsters | A | `MonStats.txt` (255 cols) + `MonStats2.txt` + `MonLvl.txt` + `MonAi.txt` | CONFIRMED A. Per-monster HP (AC, MinHP, MaxHP), damage (MinDamage, MaxDamage), resistances (ResFi, ResCo, ResLi, ResPo, ResMa), speed (Velocity + Run = divide by 25 for game speed), aggro range (aidist), reaction time (aidel), pack size (MinGrp/MaxGrp). Best-documented monster stats of all surveyed games. |
| C — Areas | A | `Levels.txt` (140 cols) | CONFIRMED A. SizeX/SizeY per difficulty, MonDen, MonUMin/Max, NumMon, per-difficulty monster spawn roster columns (mon1-mon25). Only clean tabular area-geometry source in the entire 20-game survey. |
| D — Items/Affixes | A | `Armor.txt`, `Weapons.txt`, `MagicPrefix.txt`, `MagicSuffix.txt`, `UniqueItems.txt`, `SetItems.txt`, `Runes.txt`, `TreasureClassEx.txt`, `ItemStatCost.txt`, `Properties.txt` | CONFIRMED A. Complete base items, affix pools, unique/set items, rune words, drop tables. |
| E — Calculator | B | Not fetched — no single open-source DPS oracle exists for D2 | CONFIRMED B. `pydiablo` (PyPI) includes kill-time sim; community calculators are class/build-specific. No unified arbitrary-build DPS engine. Phase 2: evaluate pydiablo for partial oracle coverage. |

---

## Named gaps (what Phase-2 or an install would add)

1. **D2R balance delta** — This fetch reflects D2 1.13 classic. D2R (Resurrected) introduced some balance changes. CASCExplorer extraction from D2R game install would capture the current D2R TSV state. For corpus kits originally authored against 1.13, this data is canonical.

2. **D2 Total-Conversion mods (PD2, Median XL, PoD)** — These ship modified TSV files with the same schema. Phase 2 item: `BetweenWalls/mod-files` (PD2), Median XL official release (via site). Natural-experiment diffs vs vanilla TSVs isolate specific balance changes.

3. **Unified DPS oracle** — No single open-source arbitrary-build DPS calculator for D2. `pydiablo` (https://pypi.org/project/pydiablo/) covers some sim capability but is not oracle-grade. VDM-CAL grade for D2 remains B.

4. **3D6 roll interpretation** — D2 skill formulas use an expression language (param1, ..param, ln, ..to1 etc.) that requires the `SkillCalc.txt` function table to evaluate. A formula parser is needed before raw `Skills.txt` params yield numeric DPS values. `pastelmind/d2txt` and `Elmegaard/D2TxtImporter` both provide parsers.

---

## License / provenance

fabd/diablo2 is a community mirror under community-standard republication norms. Blizzard has historically tolerated D2 data mirrors and mod tool ecosystems; the D2R release did not change this posture. No auth or account required for this fetch. The TSV files are the original D2 game data files.

---

## Elrond-ready pointer

Raw data at: `agentic_orchestration/research/datamine-acquisition/d2/raw/` (gitignored)
Priority files for VDM-2 skills lane: `Skills.txt` + `Missiles.txt`
Priority files for VDM-2 monsters lane: `MonStats.txt` + `MonStats2.txt` + `MonLvl.txt`
Priority files for VDM-2 areas lane: `Levels.txt`
Priority files for VDM-2 items lane: `Armor.txt` + `Weapons.txt` + `MagicPrefix.txt` + `MagicSuffix.txt` + `UniqueItems.txt` + `TreasureClassEx.txt`
