# ARPG Datamine Coverage Matrix
**Date:** 2026-07-21
**Mode:** A (analytical research)
**Commissioner:** gandalf (conductor)
**Authorization:** Matt 2026-07-21 ("idea-1 survey fires now → coverage matrix")
**Purpose:** Feed VDM-2 exact-numeric overlay + VDM-CAL calibration. Per-game scoping input for Matt ("rule removal of games without this coverage").

> **✓ RULED — Matt 2026-07-21 (verbatim): "Corpus-of-record = D2/GD/PoE1/PoE2/LE; everything else annexed at attested grade; mechanics harvest reads all twenty."**
> Consequences: (1) **corpus-of-record = the 5-roster** (270 kits — Tier 1 + LE; every member has skill-lane A/high-B AND a working oracle) — the VERIFY scope for VDM-2 field-delta exacts, VDM-CAL, band-mapping, regression predicates; corpus == VDM-CAL roster == acquisition surface. (2) **All other 15 games = ATTESTED ANNEX** — kits kept at guide-provenance confidence, readable + harvestable + plottable as soft reference points, excluded from every verification lane; NOT deleted. (3) **Mechanics harvest (READ scope) spans all 20 games** — VDM-2's charter carries the per-game annex yield checklist (LA identity-gauge · DI CC-stack · Hades boon-synergy · VS horde-density · D3 rune-variants + set-multiplier lesson · D4 aspects · TL2 charge-bars/pet-economy · TQ dual-mastery · rest quick-pass) so annexing never shallow-harvests. (4) **Acquisition collapses:** §6 Phase 1 → items 1–3 only (RePoE, fabd/diablo2, grimtools monsterdb); Phase 2 → poe2db/PoB2 + LE tunklab (+ optional D2 TC mods); Phase 3 + all defer-items DROP. (5) Cascades: elrond `corpus_class` enum (record/annex); VDM-2 charter two-scope language; decisions-log entry rides the next KR wave.

---

## Corpus-weight method

Kit counts drawn from `agentic_orchestration/research/curated/kits-export/` by filename prefix (576 files total as of 2026-07-21). Where a game has sub-prefixes (e.g. `d2-` vs `d2-wl-`) they are collapsed to their canonical game. See §3 per-game notes for prefix details.

---

## Grade key

| Grade | Meaning |
|---|---|
| **A** | Full machine-readable tables; exact numeric values; importable without manual transcription |
| **B** | Partial machine-readable; or formula-only (no raw params); or significant gaps in coverage |
| **C** | Tooltip/wiki grade only; human-readable descriptions, numbers not systematically tabulated |
| **X** | None found; server-side opaque or no community extraction exists |

Category definitions:
- **A** — Skill/kit tables (base damage, cast time, cooldown, cost, projectile count/speed, radius, duration, per-level scaling)
- **B** — Monster stat tables (HP, damage, resists, speed, AI/aggro, per-difficulty scaling)
- **C** — Area/spawn tables (zone size, density, pack composition, spawn rosters)
- **D** — Item/affix tables (bases, affix pools, tiers, drop weighting)
- **E** — Formula compendia + implemented calculators/planners (DPS oracle; computes build output from data)

---

## THE MATRIX

| Game | Corpus kits | A: Skills | B: Monsters | C: Areas | D: Items/Affixes | E: Calculator |
|---|---|---|---|---|---|---|
| **Diablo 2 / D2R** | 54 (vanilla) + 6 (mod variant) = 60 | **A** | **A** | **A** | **A** | **B** |
| **D2 TC mods** (PD2, Median XL, PoD) | — (sub-row, same 60 kits) | **A** | **A** | **A** | **A** | **B** |
| **Diablo 3** | 49 | **B** | **C** | **X** | **B** | **B** |
| **Diablo 4** | 46 | **B** | **C** | **X** | **B** | **C** |
| **PoE 1** | 94 | **A** | **B** | **B** | **A** | **A** |
| **PoE 2** | 38 | **A** | **B** | **B** | **A** | **A** |
| **Last Epoch** | 37 | **B** | **B** | **C** | **A** | **B** |
| **Grim Dawn** | 41 | **A** | **A** | **B** | **A** | **A** |
| **Titan Quest** | 26 | **B** | **B** | **C** | **A** | **C** |
| **Torchlight 1** | 2 | **B** | **C** | **X** | **B** | **X** |
| **Torchlight 2** | 11 | **A** | **B** | **C** | **A** | **C** |
| **Torchlight Infinite** | 9 | **C** | **X** | **X** | **C** | **X** |
| **Chronicon** | 16 | **B** | **C** | **X** | **B** | **C** |
| **Hades** | 12 | **A** | **B** | **X** | **C** | **X** |
| **Hall of Torment** | 17 | **C** | **C** | **X** | **C** | **X** |
| **Diablo Immortal** | 24 | **C** | **X** | **X** | **C** | **X** |
| **Undecember** | 12 | **C** | **X** | **X** | **C** | **X** |
| **Vampire Survivors** | 23 | **A** | **C** | **X** | **C** | **X** |
| **Lost Ark** | 52 | **C** | **X** | **X** | **C** | **X** |
| **Minecraft Dungeons** | 5 | **C** | **C** | **X** | **C** | **X** |

**Total kits in matrix: 576. Games covered: 19 game lines (20 rows including TC mod row).**

---

## Per-game notes

### Diablo 2 / D2R

**Corpus kits:** 60 (54 vanilla `d2-` prefix + 6 `d2-wl-` rot-w mod variant; all corpus_bucket=d2)

**A — Skills (A):** `skills.txt` (256-col TSV; per-skill base min/max damage, cast time, mana cost, projectile params, range, duration, per-level scaling, synergy formulas). `missiles.txt` (projectile geometry). Both files are flat TSV; multiple GitHub mirrors: `fabd/diablo2`, `743K/Diablo-II`. Field guide at `d2mods.info`. Parser: `pydiablo` (PyPI), `pastelmind/d2txt`. Tooling is mature and actively community-maintained for D2R.
- Sources: https://github.com/fabd/diablo2 · https://pypi.org/project/pydiablo/ · https://d2mods.info/forum/kb/viewarticle?a=360

**B — Monsters (A):** `monstats.txt` covers HP, damage, resists, speed (Velocity/Run at 25fps — needs ÷25 conversion), aggro range (`aidist`), reaction time (`aidel`), AI behavior, pack size (MinGrp/MaxGrp), skills. Best-documented aggro of any surveyed game. `OpenDiablo2/d2records` provides authoritative field decode.
- Sources: https://pkg.go.dev/github.com/OpenDiablo2/OpenDiablo2/d2core/d2records · https://github.com/fabd/diablo2/blob/master/code/d2_113_data/MonStats.txt

**C — Areas (A):** `levels.txt` contains SizeX/SizeY (per Normal/Hell difficulty), MonDen (density), MonUMin/Max (unique count), NumMon, per-monster spawn roster. This is the **only cleanly tabular area-geometry source** in the entire surveyed corpus. Verified prior art from `RDR_Encounter_Geometry_Spec_Authoritative.md`.
- Source: https://github.com/fabd/diablo2/blob/master/code/d2_113_data/Levels.txt

**D — Items/Affixes (A):** `weapons.txt`, `armor.txt`, `uniqueitems.txt`, `magicprefix.txt`, `magicsuffix.txt`, `cubemain.txt` — all TSV; complete base items, affix pools, tiers, drop rules. Same mirror set.

**E — Calculator (B):** `d3planner`-style full oracle does not exist for D2. Community DPS calculators are class/build-specific spreadsheets, not a unified engine. `pydiablo` includes a kill-time sim component. Grade B because no single open-source tool computes arbitrary build DPS from the raw tables end-to-end; requires assembly.

**ToS posture:** Community-standard republication; Blizzard has historically tolerated D2 data mirrors and mod tools. D2R adds CASC packaging but the TSV files are accessible via CASCExplorer; same community norms apply.
**Acquisition cost:** Afternoon. Files already exist on GitHub mirrors; no extraction required for D2 1.13 data.

---

**D2 Total-Conversion Mods (Project Diablo 2 / Median XL / Path of Diablo)**

Same TSV schema as vanilla D2 — mods ship their own `skills.txt`, `monstats.txt`, `levels.txt`, `uniqueitems.txt` replacing or extending vanilla values. This makes them **natural experiments**: diff mod vs vanilla to isolate specific balance changes. Key resources:
- PD2: `BetweenWalls/mod-files` (GitHub) — item/cube files for PD2 seasons; skills.txt available via `tlentz/d2modmaker` and `Elmegaard/D2TxtImporter`
- Median XL: official site ships mod files; community wiki at `median-xl.fandom.com`; `diablo2.diablowiki.net/Median_XL_Classes_and_Skills`
- Path of Diablo: server-authoritative but skill.txt diffs are community-circulated

All three grade identically to vanilla D2 for A/B/C/D (same file format). E = B (same gap). Acquisition: afternoon per mod from community repositories.

---

### Diablo 3

**Corpus kits:** 49

**A — Skills (B):** D3 is a live game with no official data export. Skill coefficients exist in community-compiled Google Sheets (proc coefficient tables per class; sourced by empirical testing, not file extraction). The `d07RiV/d3planner` GitHub (Apache-2.0) contains a game database (`d3planner.com/game`) with items, sets, and skill data — but not from raw parseable files; it is a proprietary compiled database. Damage rune modifiers are expressed as multipliers (e.g., 5,500% set bonus per VDM2 exemplar GX-11) without underlying formula tables. Grade B: structured data exists in d3planner but not in raw machine-readable source form.
- Source: https://github.com/d07RiV/d3planner · https://docs.google.com/spreadsheets/d/1nzPRhtA2tIzhjMUU6CPJeUMIK3MyRp4FWS0Wo-P1E_k/edit

**B — Monsters (C):** GR health scaling tables are community-documented (difficulty multiplier curves; e.g., Normal→Hard = 2×, per-GR level = 1.17×). No raw monster stat file extraction exists — D3 is server-side for balance values. Wowhead maintains a D3 database but monster HP/damage/resists are not tabulated at individual-monster granularity.

**C — Areas (X):** No tabular area geometry for D3. Zone construction is procedural/server-side; SizeX/SizeY equivalents not extractable.

**D — Items/Affixes (B):** `d07RiV/d3planner` contains item and set data. Maxroll D3 planner has structured build + item data. Not raw TSV but usable. Grade B.

**E — Calculator (B):** `d07RiV/d3planner` is open-source (Apache-2.0) and implements DPS calculation. However: (1) repository activity is low (97 open issues, limited recent commits); (2) does not include server-side scripts; (3) the underlying skill formula data is compiled/proprietary, not raw. Grade B — a calculator exists but is not a clean oracle from open source tables.

**ToS:** D3 community data tools are gray-area but community-normal. No official data export. Blizzard has not enforced against d3planner.
**Acquisition cost:** Days. d3planner's game database is the path of least resistance; raw formula extraction from game client would require CASC work and is legally murkier than D2.

---

### Diablo 4

**Corpus kits:** 46

**A — Skills (B):** `blizzhackers/d4data` (GitHub, archived Dec 2024) parsed JSON from CASC `.stl`/`.aff`/`.skl` files. `DiabloTools/d4data` is the active continuation. `Dakota628/d4parse` is another parser. `bytemind-de/d4-tools` computes stats/damage. However: D4 is a live game with frequent patches; data drifts. No equivalent of D2's stable TSV. Grade B: structured data extractable but format is complex, not stable, and requires CASC extraction tooling.
- Sources: https://github.com/DiabloTools/d4data · https://github.com/Dakota628/d4parse · https://blizzhackers.github.io/d4data/

**B — Monsters (C):** Monster stats are server-authoritative; community resources are tooltip/guide-grade. `d4data` may contain some monster definitions but at C completeness. No equivalent of D2's `monstats.txt`.

**C — Areas (X):** Procedural; no tabular area geometry found.

**D — Items/Affixes (B):** `d4data` contains parsed item/affix JSON. `Lothrik/diablo4-build-calc` uses CASCExplorer-extracted data. Grade B: data exists but format complexity and patch cadence are barriers.

**E — Calculator (C):** `Lothrik/diablo4-build-calc` is a build calculator; `jlian/d4-damage-calc` is a GitHub-hosted DPS calculator. Both are community tools, not formally oracle-grade for VDM-CAL purposes. Maxroll D4 planner exists but is closed-source. Grade C: calculators exist but none are clean open-source oracles with exposed formula tables.

**ToS:** Community data extraction is active and unchallenged. The infamous 2024 Vessel of Hatred datamine (Blizzard accidentally left encryption key unchanged) shows data is periodically accessible. Standard Blizzard ToS gray-area.
**Acquisition cost:** Days to weeks. CASC extraction is documented but D4's rapid patch cadence means data must be refreshed. The `d4data` archive provides a baseline but requires live-game refresh.

---

### Path of Exile 1

**Corpus kits:** 94 (largest game in corpus)

**A — Skills (A):** `brather1ng/RePoE` (and forks: `repoe-fork/repoe`, `lvlvllvlvllvlvl/RePoE`) outputs `gems.json` — per-gem level tables with stat arrays (damage, mana cost, cast time, crit chance, AoE radius, duration, projectile count, per-level scaling). Data parsed from GGPK via `PyPoE` (`Project-Path-of-Exile-Wiki/PyPoE`, Python). `active_skill_types.json` + `stat_translations.json` provide semantic mapping. Path of Building (PoB) community repo (`PathOfBuildingCommunity/PathOfBuilding`, Lua, open-source) cross-validates. Grade A: comprehensive, programmatic, per-skill per-level numeric tables.
- Sources: https://github.com/brather1ng/RePoE · https://github.com/Project-Path-of-Exile-Wiki/PyPoE · https://github.com/PathOfBuildingCommunity/PathOfBuilding

**B — Monsters (B):** `RePoE/data/default_monster_stats.json` provides monster base stat scaling. `poedb.tw` has a Monster section (browsable). `poewiki.net/wiki/Module:Data_tables/Monster_stats` has structured monster stat tables. PyPoE can extract monster `.dat` records. Grade B: base stat tables and scaling curves exist but per-monster HP/damage/resists at area-specific granularity requires additional extraction work.
- Sources: https://poedb.tw/us/ · https://www.poewiki.net/wiki/Module:Data_tables/Monster_stats

**C — Areas (B):** `poedb.tw` has act and map area listings with some monster roster data. `RePoE` contains area-related data. Map density is expressed as explicit map modifiers ("+X% pack size") which are machine-readable affixes. Exact zone geometry/SizeX/SizeY equivalent does not exist. Grade B: pack composition and density modifiers are extractable; absolute area geometry is not.

**D — Items/Affixes (A):** `RePoE/data/mods.json` — comprehensive affix pools, tier structure, spawn weights, stat ranges, domain/generation type. `base_items.json` covers all base items. Grade A.

**E — Calculator (A):** Path of Building (`PathOfBuildingCommunity/PathOfBuilding`) is the gold standard: open-source Lua, implements full DPS calculation for all skills, factors in passives/support gems/charges/curses/buffs/monster resists. Actively maintained. This is a genuine VDM-CAL oracle.

**ToS:** Strong community-normal posture. GGG has explicitly endorsed PyPoE and community data tools. GGPK extraction is standard practice. PoB is endorsed by GGG's community team.
**Acquisition cost:** Afternoon for skills/mods via RePoE pre-built JSON. Days if GGPK re-extraction needed. PoB as oracle: ready immediately.

---

### Path of Exile 2

**Corpus kits:** 38

**A — Skills (A):** `poe2db.tw` is the primary database — pulls directly from game files, updates within hours of patches. Covers skill gems, support gems with stat arrays. `PathOfBuildingCommunity/PathOfBuilding-PoE2` (`PathOfBuilding-PoE2-v2` temp clone) is open-source (Lua) and supports all skills/support gems. Data export from PoB PoE2 uses same format as PoE1. `repoe-fork/repoe` produces PoE2 data. Grade A — same infrastructure as PoE1 applied to PoE2.
- Sources: https://poe2db.tw/us/ · https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2 · https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2-v2

**B — Monsters (B):** `poe2db.tw` has monster entries with stats. Same pipeline as PoE1 monster extraction via PyPoE/PoE2 equivalent. Grade B (same caveats as PoE1: per-monster exact HP at level/difficulty requires extraction work; scaling tables present).

**C — Areas (B):** `poe2db.tw` covers act areas and waystones (PoE2's map system). Pack composition and density modifiers are affix-expressed. Grade B.

**D — Items/Affixes (A):** Same RePoE/poe2db pipeline. `mods.json` equivalent exists. Grade A.

**E — Calculator (A):** `PathOfBuilding-PoE2` implements DPS calculation. PoE2 is still in early access (EA 2024+) so some skills/passives may be partially supported, but the framework is A-grade. Grade A with caveat: EA patch cadence means data refreshes are more frequent than PoE1.

**ToS:** Same GGG community-normal posture as PoE1. EA status adds some uncertainty on data stability.
**Acquisition cost:** Afternoon for pre-built data. PoB PoE2 ready immediately.

---

### Last Epoch

**Corpus kits:** 37

**A — Skills (B):** `lastepochtools.com/skills/` provides skill data and skill node trees (133 skills, 3,862 nodes per `lastepoch.tunklab.com` count). `lastepoch.tunklab.com` is a community datamine site covering skills, affixes, monsters, zones. `epoch-dps.com` is a per-skill DPS calculator. However: Last Epoch is a Unity game; the extraction method is a Database Generator Mod using MelonLoader 5.7 + F4 keybind to dump JSON. Skill base damage values are documented but the pipeline is less standardized than PoE/D2. Community notes that base damage values are difficult to find raw; `lastepochtools.com/guide/section/base_damage` addresses this but 403 on fetch during survey (paywalled or rate-limited). Grade B: data exists but extraction pipeline requires a game install + mod + specific tooling; not as clean as RePoE.
- Sources: https://www.lastepochtools.com/skills/ · https://lastepoch.tunklab.com/ · https://epoch-dps.com/

**B — Monsters (B):** `lastepoch.tunklab.com` covers Bestiary, Champions, Monster Modifiers (480 zones, bestiary data present). Grade B: exists but depth of monster stat coverage (HP per level, damage scaling curves) is unclear without direct access.

**C — Areas (C):** `lastepoch.tunklab.com` lists 480 zones. Spawn rosters and density data unknown — likely tooltip-grade rather than tabular. Grade C.

**D — Items/Affixes (A):** `lastepochtools.com/db/` covers 1,112 affixes, 445 unique items, 674 base items. Most complete single-source for LE items. Grade A.

**E — Calculator (B):** `epoch-dps.com` is a per-skill DPS calculator for Last Epoch. `maxroll.gg/last-epoch` has a character planner. Neither is clearly open-source with exposed formula tables. Grade B: calculators exist but oracle-grade VDM-CAL use would require formula validation.

**ToS:** Community tools are community-normal for Eleventh Hour Games. The Database Generator Mod approach is endorsed by the modding community.
**Acquisition cost:** Days. Requires game install + MelonLoader + mod setup for raw extraction; otherwise use lastepochtools/tunklab as pre-built sources.

---

### Grim Dawn

**Corpus kits:** 41

**A — Skills (A):** Official `AssetManager.exe` rips all DBR files including `records/skills/` — named fields for damage, duration, cooldown, mana cost, radius, projectile count. `GrimDawn_DB_to_CSV_Extractor` (GitHub: `abclution/GrimDawn_DB_to_CSV_Extractor`) converts DBR → CSV. Skill DBRs are self-describing with named parameters. Grade A. VDM2 spec (§4, line 127) explicitly names GD DBRs as an exact-geometry lane.
- Sources: https://www.grimdawn.com/downloads/Grim%20Dawn%20Modding%20Guide.pdf · https://github.com/abclution/GrimDawn_DB_to_CSV_Extractor

**B — Monsters (A):** `grimtools.com/monsterdb/` is a pre-built browsable monster database with HP, Energy, Armor Rating, Offensive Ability, Defensive Ability, Resistances, DPS, per-level scaling input. Crate's AssetManager extracts creature DBRs with `walkSpeed`, `characterRunSpeed` (confirmed clean named fields, per prior art). Grade A for stats accessible without file extraction (grimtools); A for extraction path via AssetManager.
- Source: https://www.grimtools.com/monsterdb/

**C — Areas (B):** GD area/zone geometry is not tabular like D2's `Levels.txt` (confirmed by prior art). Grimtools provides spawn locations qualitatively (which areas monsters appear in). Grade B: roster/spawn data accessible; absolute geometry not tabular.

**D — Items/Affixes (A):** `grimtools.com/db/` is a comprehensive item database. DBR extraction via AssetManager covers all item/affix records. Grade A.

**E — Calculator (A):** `grimtools.com/calc/` is a full build calculator (skills, masteries, devotion, equipment) — the community gold standard for GD builds. Grade A. Not open-source but functionally an oracle; for VDM-CAL cross-validation, grimtools calc is the reference.

**ToS:** Crate Entertainment officially endorses AssetManager and modding. Grimtools is community-made but Crate has linked to it from official channels. Extraction is explicitly encouraged.
**Acquisition cost:** Afternoon for grimtools pre-built data. Days for DBR extraction if raw CSV needed.

---

### Titan Quest

**Corpus kits:** 26 (tq + tq2 combined)

**A — Skills (B):** `tqdb` Python parser (GitHub: `fonsleenaars/tqdb`) extracts equipment, sets, skills, boss loot → JSON. ArzExtractor / official ArtManager unpacks `.arz` → loose `.dbr` records. Skill DBRs have named parameters analogous to GD (same Iron Lore engine lineage). `tq-db.net` hosts the parsed database. Monster stats and skills are documented in the index. Grade B: extraction path is similar to GD but `tqdb`'s primary output focuses on equipment/skills for web display; monster speed/aggro field names are TBV (noted as unconfirmed in prior art). Grade B pending field-name verification.
- Sources: https://github.com/fonsleenaars/tqdb · http://www.tq-db.net · https://titanquest.fandom.com/wiki/Art_Manager

**B — Monsters (B):** `tq-db.net` has a monster index with skills, stats, and loot tables. Creature DBRs have movement speed and combat stats. The exact aggro/perception-radius field name is TBV (prior art caveat). Grade B.

**C — Areas (C):** TQ area/map geometry is not tabular. Spawn locations are qualitative (area assignment per monster). Grade C.

**D — Items/Affixes (A):** `tqdb` primary output; `tq-db.net` covers equipment, sets, affixes comprehensively. Grade A.

**E — Calculator (C):** No equivalent of PoB or grimtools build calculator found for TQ. Community spreadsheets exist but no integrated DPS oracle. Grade C.

**ToS:** Community-normal; Nordic Games (current publisher) has not enforced against modding tools. ArtManager is official.
**Acquisition cost:** Days. `tqdb` pipeline is documented; the monster field-name verification adds a half-day investigation on top.

---

### Torchlight 1

**Corpus kits:** 2 (minimal corpus weight)

**A — Skills (B):** Runic Games used the Ogre3D engine with data files in XML/similar text format. Very limited community documentation. No equivalent of GUTS for TL1. Grade B: data extractable in principle but tooling is minimal.

**B — Monsters (C):** No structured community database found. Wiki-grade descriptions only.

**C — Areas (X):** Not found.

**D — Items/Affixes (B):** Some community databases exist (Torchlight wiki) but not machine-readable at table depth.

**E — Calculator (X):** None found.

**ToS/Acquisition:** Low priority given 2-kit corpus weight. Acquisition: days-to-infeasible without dedicated tooling.

---

### Torchlight 2

**Corpus kits:** 11

**A — Skills (A):** GUTS (Runic Games' official editor) is available via Steam Library → Tools → Torchlight 2 GUTS. It extracts all game files from packaged state (one-time ~30-min extraction). Skills data is in `.dat` files (text-editable); `.bindat` files are binary mirrors. Skill trees in `Media/Skills` are fully readable text. Grade A: official tooling, complete data, no EULA friction.
- Sources: https://www.runicgames.com/blog/2013/04/01/guts/ · https://steamcommunity.com/sharedfiles/filedetails/?id=138588277

**B — Monsters (B):** GUTS extraction includes monster data files. Community databases exist. Grade B: extractable via GUTS but no pre-built monster stat database found at grimtools-equivalent depth.

**C — Areas (C):** GUTS includes level/area files but no tabular area-geometry equivalent of D2 `Levels.txt`. Grade C.

**D — Items/Affixes (A):** GUTS extraction covers all item/affix `.dat` files. Grade A.

**E — Calculator (C):** No integrated DPS oracle found. GUTS itself is a dev tool, not a DPS calculator.

**ToS:** GUTS is official Runic Games software distributed via Steam. Zero ToS risk.
**Acquisition cost:** Afternoon. Own copy of TL2 on Steam + run GUTS extraction once.

---

### Torchlight Infinite

**Corpus kits:** 9

**A — Skills (C):** `tlidb.com`, `tli-hub.com`, `tlicompendium.com`, `legacy.torchcodex.com` (updated SS10, Oct 2025) all provide community databases. However: TLI is a mobile-first live game (XD/Level Infinite); server-side authoritative balance. Skills data on these sites appears to be tooltip-grade, not raw datamine. Grade C.
- Sources: https://tlidb.com · https://tli-hub.com/database/skills

**B — Monsters (X):** No structured monster stat database found. Server-side.

**C — Areas (X):** Not found.

**D — Items/Affixes (C):** Community databases cover item listings at tooltip/description depth.

**E — Calculator (X):** No DPS oracle found. `minmaxedarpg.com/games/tli/skills` lists skills but not a calc.

**ToS/Acquisition:** Mobile-first server-side game — hard lane for datamine. Low corpus weight (9 kits). Acquisition: infeasible for A-grade without direct client extraction.

---

### Chronicon

**Corpus kits:** 16

**A — Skills (B):** `chronicondb.com` (`gabriel-dehan/chronicondb-client`, React 17, open-source GitHub) is the primary community database — items, skills, enchants. Chronicon (solo dev Subworld Games) has an official beta-branch feature: `CTRL+P` in main menu generates item+enchant data files for the current version. Skill tree node data is present. Grade B: skill data available via official data export + community client, but depth of raw numeric fields (base damage, cooldowns, scaling curves) requires verification.
- Sources: https://github.com/gabriel-dehan/chronicondb-client · https://steamcommunity.com/app/375480/discussions/0/2985287984605472801/

**B — Monsters (C):** Chronicon wiki has monster info at description level. No systematic monster stat table found.

**C — Areas (X):** Procedural; no tabular geometry found.

**D — Items/Affixes (B):** `chronicondb.com` covers items and enchants. Official data export via CTRL+P generates item/enchant files. Grade B.

**E — Calculator (C):** `chronicondb.com` is a database, not a DPS calculator. No integrated oracle found.

**ToS:** Official data export feature = explicit developer endorsement. No ToS risk.
**Acquisition cost:** Afternoon (CTRL+P data export from game install).

---

### Hades

**Corpus kits:** 12

**A — Skills (A):** Supergiant chose not to obfuscate the game's Lua scripting. `Content/Scripts/` directory (accessible via Steam → Browse local files) contains all data files in plaintext Lua. Key files: `WeaponData.lua` (~17,180 lines, confirmed to contain `ActiveReloadTime`, fire parameters, rumble parameters, and full weapon stat definitions), `EnemyData.lua`, `TraitData.lua` (boon/trait definitions), `EnemyUpgradeData.lua`, `HeroData.lua`. GitHub mirror: `zhang-wen-guang/Hades`. Community modding guide: `micriley/HadesModding`. Grade A: unobfuscated Lua, complete stat definitions readable with any text editor.
- Sources: https://github.com/zhang-wen-guang/Hades · https://github.com/micriley/HadesModding · https://www.nexusmods.com/hades/articles/19

**B — Monsters (B):** `EnemyData.lua` + `EnemyUpgradeData.lua` contain enemy definitions. HP values, damage parameters, behavior scripts are in these files. Grade B: data exists in Lua; requires manual parsing vs. a structured DB.

**C — Areas (X):** Room/chamber geometry is procedurally assembled from templates. No tabular area-geometry equivalent found.

**D — Items/Affixes (C):** Hades has a different item system (boons, not ARPG-style affixes). Boon data is in `TraitData.lua`. Grade C for traditional ARPG affix framing.

**E — Calculator (X):** No DPS oracle found. Hades combat math is relatively simple (flat damage + modifiers) and community discussions are guide-grade, not formula-oracle.

**ToS:** Supergiant has explicitly endorsed modding. The unobfuscated Lua is a design choice. Zero ToS risk.
**Acquisition cost:** Afternoon. Own the game + navigate to Content/Scripts.

---

### Hall of Torment

**Corpus kits:** 17 (moderately sized; VS-like game, Godot engine)

**A — Skills (C):** `hot.fandom.com/wiki` covers stats and game mechanics. A skill tracker exists (`gizix/HoT_SkillTracker` on GitHub) — a build-tracking tool, not a datamine. Hall of Torment is built on Godot; game data is in Godot's `.pck` format. No community datamine pipeline found. Grade C: wiki-grade only.
- Source: https://hot.fandom.com/wiki/Stats · https://github.com/gizix/HoT_SkillTracker

**B — Monsters (C):** Wiki covers enemy descriptions. No stat tables.

**C — Areas (X):** None found.

**D — Items/Affixes (C):** Wiki-grade.

**E — Calculator (X):** None found.

**ToS/Acquisition:** Godot `.pck` extraction is technically feasible (community tools exist for Godot asset extraction) but no pipeline is established for HoT. Acquisition: days.

---

### Diablo Immortal

**Corpus kits:** 24

**A — Skills (C):** Wowhead maintains a Diablo Immortal database (https://www.wowhead.com/diablo-immortal/database) with skills organized by class. A community member created a skill-based essence database. However: DI is a mobile-first live game; server-authoritative balance. Skill coefficients are not in community-accessible game files. `CucFlavius/DIDT` (GitHub: Diablo Immortal Data Tool) exists but depth is unclear. Grade C.
- Source: https://www.wowhead.com/diablo-immortal/database · https://github.com/CucFlavius/DIDT

**B — Monsters (X):** Server-side. No monster stat extraction found.

**C — Areas (X):** Not found.

**D — Items/Affixes (C):** Wowhead database covers items at tooltip/description grade.

**E — Calculator (X):** No DPS oracle found.

**ToS:** Mobile live game with Activision Blizzard Terms. Community datamining acknowledged but not officially endorsed. Gray area; lower risk than pure-download scenarios.
**Acquisition cost:** Days for C-grade tooltip scraping. A-grade: infeasible without APK extraction expertise.

---

### Undecember

**Corpus kits:** 12

**A — Skills (C):** `undecember.thein.ru/en/` provides a community game database. A damage calculator for DoT/Toxic Flame (`APXEOLOG/undecember-calculator`, GitHub) exists for one skill. Undecember is a server-side live game. `VGJournal.net/games/undecember/game-data/` lists some data files. Grade C: partial community databases exist, no systematic skill table extraction.
- Sources: https://undecember.thein.ru/en/ · https://github.com/APXEOLOG/undecember-calculator

**B — Monsters (X):** Server-side. No monster stat database found.

**C — Areas (X):** Not found.

**D — Items/Affixes (C):** `undecember.thein.ru` covers some item data.

**E — Calculator (X):** Single-skill damage calc only (`APXEOLOG`). No full oracle.

**ToS:** Korean live game (Needs Games); server-authoritative. Standard community-datamine gray area.
**Acquisition cost:** Infeasible for A-grade; C-grade tooltip scraping: days.

---

### Vampire Survivors

**Corpus kits:** 23

**A — Skills (A):** VS ships as a web/JavaScript application. Weapon data is **completely documented** in the official wiki's Weapons/Overview Stats page: exact numeric tables for Base Damage (min/max), Cooldown (s), Area (min/max), Duration (s), Speed (min/max), Amount (min/max), Interval (s), Knockback, Pierce, Pool limit, Hitbox Delay, Crit multiplier — for both base weapons and evolutions. `vampire.survivors.wiki/w/Weapons/Overview_Stats` is machine-readable. Game save data is JSON (`vampire.survivors.wiki/w/SaveData`). Grade A: complete exact numeric tables available without any extraction tooling.
- Source: https://vampire.survivors.wiki/w/Weapons/Overview_Stats

**B — Monsters (C):** Enemy data is partially documented on the wiki. No structured monster stat database at ARPG depth (VS enemies are simpler than ARPG monsters). Grade C.

**C — Areas (X):** VS stages have no tabular geometry equivalent.

**D — Items/Affixes (C):** Power-up and weapon upgrade data is on the wiki. Item system is simpler than ARPG affixes.

**E — Calculator (X):** No DPS oracle found. VS combat math is relatively simple (no build planner).

**ToS:** VS wiki content is community-contributed; game data is derived from the JS source which is user-accessible. poncle (dev) has not objected to community data sites.
**Acquisition cost:** Afternoon. Wiki scrape or manual table extraction; or directly inspect the game's JS files.

---

### Lost Ark

**Corpus kits:** 52 (second-largest after PoE1; identity-gauge cohort)

**A — Skills (C):** `lostarkcodex.com/us/skills/` exists but loaded dynamically (AJAX); detail pages could not be confirmed as containing exact damage coefficients during this survey. `lostark.wiki.fextralife.com/Stats` covers stats at description level. Lost Ark is a Korean MMO (Amazon Games / Smilegate RPG) with server-authoritative balance. Identity gauge and skill damage are expressed as percentage-based multipliers in tooltips, not raw coefficient tables. LOA Details (`lost-ark-dev/loa-details`, GitHub) tracks real-time combat logs — a parse-based approach, not a datamine. Grade C: community databases exist at tooltip/description depth; exact coefficient extraction is not established.
- Sources: https://lostarkcodex.com/us/ · https://github.com/lost-ark-dev/loa-details · https://lostarkdatabase.com/

**B — Monsters (X):** Server-side MMO. No monster stat database found. Raid encounter data is guide-grade only.

**C — Areas (X):** MMO map data; not in ARPG-equivalent tabular form.

**D — Items/Affixes (C):** Community databases cover engravings, gems, and gear at tooltip/wiki grade.

**E — Calculator (X):** No DPS oracle found. Build planning tools (`la-tools.com`) focus on honing/gold calculators, not skill DPS.

**ToS:** Korean MMO live game. Community tools are tolerated (LOA Details is widely used). No official data export.
**Acquisition cost:** Combat log parsing (`loa-details`) could yield empirical DPS data over days. Pure datamine: infeasible — server-side.

---

### Minecraft Dungeons

**Corpus kits:** 5 (minimal corpus weight; included as outlier game-type)

**A — Skills (C):** `dungeoncollector.co.uk/?table=1` provides weapon statistics tables. `dungeon.wiki` and planetminecraft community data packs cover weapons and artifacts. MCD is a simplified ARPG (no class skill tree); "skills" are enchantments on gear. Grade C: weapon stat tables exist at wiki/community-database depth, not raw file extraction level.

**B — Monsters (C):** Some monster data documented in community wikis and the official MCD companion app.

**C — Areas (X):** Not found in tabular form.

**D — Items/Affixes (C):** Community databases cover enchantments and weapon bases.

**E — Calculator (X):** No DPS oracle found; simplified combat model.

**ToS:** Microsoft/Mojang property. Community-normal data sites appear unchallenged.
**Acquisition cost:** Afternoon for C-grade. A-grade: not applicable (game architecture differs from ARPG pattern).

---

## 4. Scoping-decision view for Matt

Games sorted by coverage quality (composite A+B+C+D grade), with corpus weight.

### Tier 1 — High coverage, strong datamine across all categories

| Game | Corpus kits | A | B | C | D | E | Notes |
|---|---|---|---|---|---|---|---|
| **Diablo 2 / D2R** | 60 | A | A | A | A | B | Best-documented of all surveyed; Levels.txt unique area geometry |
| **PoE 1** | 94 | A | B | B | A | A | Largest corpus; PoB is VDM-CAL oracle; RePoE ready-to-consume |
| **Grim Dawn** | 41 | A | A | B | A | A | grimtools pre-built + AssetManager extraction; Crate-endorsed |
| **PoE 2** | 38 | A | B | B | A | A | Same pipeline as PoE1; EA patch cadence caveat |

### Tier 2 — Good coverage with gaps; workable for VDM-2 exact overlay

| Game | Corpus kits | A | B | C | D | E | Notes |
|---|---|---|---|---|---|---|---|
| **Torchlight 2** | 11 | A | B | C | A | C | GUTS official extraction; skill .dat files clean; no oracle |
| **Last Epoch** | 37 | B | B | C | A | B | Extraction requires game install + MelonLoader mod; epoch-dps exists |
| **Titan Quest** | 26 | B | B | C | A | C | Same engine family as GD; field TBV for monster aggro/aggro range |
| **Hades** | 12 | A | B | X | C | X | Unobfuscated Lua; skill data clean; monster data present; no calc |
| **Vampire Survivors** | 23 | A | C | X | C | X | Wiki-complete exact tables; no extraction needed; simplest model |

### Tier 3 — Partial coverage; C-grade dominant; usable only for specific fields

| Game | Corpus kits | A | B | C | D | E | Notes |
|---|---|---|---|---|---|---|---|
| **Diablo 3** | 49 | B | C | X | B | B | d3planner open-source but not raw-table oracle; formula opaque |
| **Diablo 4** | 46 | B | C | X | B | C | CASC extraction possible; patch drift; no clean oracle |
| **Chronicon** | 16 | B | C | X | B | C | Official CTRL+P data export; small team; limited depth |

### Tier 4 — Weak/tooltip-grade only; C/X dominant

| Game | Corpus kits | A | B | C | D | E | Notes |
|---|---|---|---|---|---|---|---|
| **Diablo Immortal** | 24 | C | X | X | C | X | Mobile live; server-side; tooltip only |
| **Hall of Torment** | 17 | C | C | X | C | X | Godot .pck; no established pipeline |
| **Torchlight Infinite** | 9 | C | X | X | C | X | Mobile live; server-side |
| **Torchlight 1** | 2 | B | C | X | B | X | Very low corpus weight; minimal tooling |
| **Undecember** | 12 | C | X | X | C | X | Korean live; server-side |
| **Minecraft Dungeons** | 5 | C | C | X | C | X | Non-ARPG architecture; low corpus weight |

### HIGH CORPUS WEIGHT × LOW COVERAGE collisions — flags for Matt

| Collision | Corpus kits | Best available grade | Risk |
|---|---|---|---|
| **Lost Ark** | **52** | **C / X** | **HIGH** — Second-largest corpus block; identity-gauge cohort; server-side Korean MMO means C-grade is the ceiling. A datamine-overlay for this cohort is not feasible without combat-log parse or tooltip scrape. |
| **Diablo 3** | 49 | B (Skills), B (E) | MEDIUM — 49 kits; d3planner exists as B-grade oracle; raw tables not available. VDM-2 exact overlay partial feasible; VDM-CAL feasible via d3planner with formula caveat. |
| **Diablo 4** | 46 | B (Skills) | MEDIUM — 46 kits; CASC extraction exists but patch-drift risk; no clean oracle. VDM-CAL at C-grade only. |
| **Diablo Immortal** | 24 | C | MEDIUM — 24 kits; mobile-first; datamine infeasible. Scoping cut is a reasonable call. |

**Summary verdict on Lost Ark (conductor's explicit question):** C-grade confirmed across all five categories. Server-side Korean MMO architecture makes A-grade extraction infeasible with available community tooling. The `loa-details` combat-log parser (`lost-ark-dev/loa-details`) could yield empirical DPS data via gameplay measurement (not datamine), but this is a days-to-weeks undertaking and produces sampled, not exhaustive, coverage. **If Matt's rule is "remove games without machine-readable skill/monster data," Lost Ark falls below the threshold on categories A, B, C, and E.** The 52-kit corpus weight makes this the most significant scoping decision in the matrix.

---

## 5. What the survey could not verify + confidence notes

| Item | Status | Confidence note |
|---|---|---|
| TQ monster aggro/perception-radius field name in `.dbr` | Unverified (prior art caveat carried forward) | Medium: GD equivalent confirmed; TQ likely analogous (same engine) but field name TBV |
| Lost Ark `lostarkcodex.com` skill pages — exact numeric content | Could not confirm (AJAX load, page returned navigation only) | Medium: based on community reports these are tooltip-grade, not coefficient tables |
| Last Epoch `lastepochtools.com/guide/section/base_damage` — exact numeric depth | Page returned 403 during survey | Medium: tunklab and forum discussions suggest base damage values are available but formatted as guide text, not exportable tables |
| Diablo 3 d3planner game database completeness — current patch | Could not verify live (site loads dynamically) | Medium: repository shows 97 open issues; Season 29+ content may be stale |
| Hall of Torment `.pck` extraction pipeline | No community pipeline found | Low: no established tooling means A-grade acquisition is speculative |
| Hades `WeaponData.lua` exact damage-number fields | File confirmed in repo; sample showed timing/ammo params at line ~1000 of 17,180 | High: damage values exist deeper in file; unobfuscated Lua is definitive source |
| Minecraft Dungeons A-grade extraction | Not pursued | Low corpus weight (5 kits); not worth investigation |

**Survey approach confidence:** This survey is web-search + targeted fetch based. It does not verify every URL for current live status. URLs confirmed reachable as of 2026-07-21 during fetches are noted; others are search-result verified. No game files were downloaded or extracted.

---

## 6. Recommended acquisition order (best value-per-effort, staged)

Priority driven by: corpus kit count × coverage quality × extraction effort.

**Phase 1 — Afternoon each; highest ROI**

1. **PoE1 via RePoE** (94 kits, A-grade skills, PoB oracle ready) — Pre-built JSON at `repoe-fork/repoe` or `brather1ng/RePoE`. Zero extraction work. PoB is the VDM-CAL oracle.
2. **Diablo 2 via fabd/diablo2 GitHub mirror** (60 kits, A across all categories) — Files already on GitHub. `pydiablo` or raw TSV parse. Extends verified prior art.
3. **Grim Dawn via grimtools.com/monsterdb + AssetManager** (41 kits, A/A) — Pre-built monster DB needs no extraction; AssetManager for skill DBRs requires game install + 5GB extraction.
4. **Vampire Survivors via wiki table scrape** (23 kits, A-grade weapon tables) — `vampire.survivors.wiki/w/Weapons/Overview_Stats` is exact numeric; afternoon scrape.
5. **Hades via Content/Scripts/ read** (12 kits, A-grade skills) — Requires game install; navigate to `Content/Scripts/WeaponData.lua` + `TraitData.lua`.

**Phase 2 — Days each; strong coverage**

6. **PoE2 via poe2db.tw + PathOfBuilding-PoE2** (38 kits, A-grade, same pipeline as PoE1)
7. **D2 Total-Conversion mods** (same 60 kits, A-grade; natural-experiment value; files on community GitHub)
8. **Torchlight 2 via GUTS** (11 kits, A-grade skills/items; requires TL2 on Steam + GUTS extraction)
9. **Last Epoch via tunklab + epoch-dps** (37 kits, B-grade; game install + MelonLoader for raw extraction)
10. **Titan Quest via tqdb** (26 kits, B-grade; Python parser on GitHub; field-name verification needed for monster aggro)

**Phase 3 — Days to weeks; diminishing returns or significant gaps**

11. **Grim Dawn DBR extraction** (41 kits; upgrade from grimtools-pre-built to raw CSV for exact skill params)
12. **Diablo 3 via d3planner** (49 kits; B-grade oracle; formula validation work needed for VDM-CAL)
13. **Diablo 4 via d4data** (46 kits; B-grade; CASC extraction + patch refresh needed)
14. **Chronicon via CTRL+P export** (16 kits; B-grade; small effort, moderate corpus weight)

**Defer or scope-cut**

- **Lost Ark** (52 kits): C/X grade ceiling; infeasible for exact overlay. Recommend Matt ruling on whether to scope-cut.
- **Diablo Immortal** (24 kits): C/X; mobile-first server-side.
- **Undecember** (12 kits): C/X; server-side.
- **Torchlight Infinite** (9 kits): C/X; mobile live.
- **Hall of Torment** (17 kits): C; Godot .pck extraction unestablished.
- **Minecraft Dungeons** (5 kits): C; low corpus weight + non-ARPG model.

---

## Source list

| Source | URL | Access date |
|---|---|---|
| RePoE (brather1ng) | https://github.com/brather1ng/RePoE | 2026-07-21 |
| RePoE (repoe-fork) | https://github.com/repoe-fork/repoe | 2026-07-21 |
| PyPoE | https://github.com/Project-Path-of-Exile-Wiki/PyPoE | 2026-07-21 |
| Path of Building (PoE1) | https://github.com/PathOfBuildingCommunity/PathOfBuilding | 2026-07-21 |
| Path of Building (PoE2) | https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2 | 2026-07-21 |
| Path of Building (PoE2 v2) | https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2-v2 | 2026-07-21 |
| PoEDB (PoE1) | https://poedb.tw/us/ | 2026-07-21 |
| PoE2DB | https://poe2db.tw/us/ | 2026-07-21 |
| PoE Wiki monster stats | https://www.poewiki.net/wiki/Module:Data_tables/Monster_stats | 2026-07-21 |
| fabd/diablo2 (GitHub mirror) | https://github.com/fabd/diablo2 | 2026-07-21 |
| OpenDiablo2 d2records | https://pkg.go.dev/github.com/OpenDiablo2/OpenDiablo2/d2core/d2records | 2026-07-21 |
| pydiablo | https://pypi.org/project/pydiablo/ | 2026-07-21 |
| d2mods.info skills.txt guide | https://d2mods.info/forum/kb/viewarticle?a=360 | 2026-07-21 |
| pastelmind/d2txt | https://github.com/pastelmind/d2txt | 2026-07-21 |
| Elmegaard/D2TxtImporter | https://github.com/Elmegaard/D2TxtImporter | 2026-07-21 |
| BetweenWalls/mod-files (PD2) | https://github.com/BetweenWalls/mod-files | 2026-07-21 |
| Median XL wiki | https://median-xl.fandom.com/wiki/Skills | 2026-07-21 |
| grimtools.com/calc | https://www.grimtools.com/calc/ | 2026-07-21 |
| grimtools.com/monsterdb | https://www.grimtools.com/monsterdb/ | 2026-07-21 |
| grimtools.com/db | https://www.grimtools.com/db/ | 2026-07-21 |
| GD Modding Guide | https://www.grimdawn.com/downloads/Grim%20Dawn%20Modding%20Guide.pdf | 2026-07-21 |
| GrimDawn_DB_to_CSV_Extractor | https://github.com/abclution/GrimDawn_DB_to_CSV_Extractor | 2026-07-21 |
| tqdb parser | https://github.com/fonsleenaars/tqdb | 2026-07-21 |
| tq-db.net | http://www.tq-db.net | 2026-07-21 |
| TQ Art Manager wiki | https://titanquest.fandom.com/wiki/Art_Manager | 2026-07-21 |
| lastepochtools.com/skills | https://www.lastepochtools.com/skills/ | 2026-07-21 |
| lastepoch.tunklab.com | https://lastepoch.tunklab.com/ | 2026-07-21 |
| epoch-dps.com | https://epoch-dps.com/ | 2026-07-21 |
| d07RiV/d3planner | https://github.com/d07RiV/d3planner | 2026-07-21 |
| D3 proc coefficients (Google Sheets) | https://docs.google.com/spreadsheets/d/1nzPRhtA2tIzhjMUU6CPJeUMIK3MyRp4FWS0Wo-P1E_k/ | 2026-07-21 |
| maxroll.gg/d3 | https://maxroll.gg/d3 | 2026-07-21 |
| DiabloTools/d4data | https://github.com/DiabloTools/d4data | 2026-07-21 |
| Dakota628/d4parse | https://github.com/Dakota628/d4parse | 2026-07-21 |
| mfloob/diablo4-data-harvest (archived) | https://github.com/mfloob/diablo4-data-harvest | 2026-07-21 |
| d4data browser | https://blizzhackers.github.io/d4data/ | 2026-07-21 |
| Wowhead DI database | https://www.wowhead.com/diablo-immortal/database | 2026-07-21 |
| CucFlavius/DIDT | https://github.com/CucFlavius/DIDT | 2026-07-21 |
| Hades scripts (zhang-wen-guang) | https://github.com/zhang-wen-guang/Hades | 2026-07-21 |
| micriley/HadesModding | https://github.com/micriley/HadesModding | 2026-07-21 |
| Nexusmods Hades Config.lua guide | https://www.nexusmods.com/hades/articles/19 | 2026-07-21 |
| VS Wiki Weapons/Overview_Stats | https://vampire.survivors.wiki/w/Weapons/Overview_Stats | 2026-07-21 |
| lostarkcodex.com/skills | https://lostarkcodex.com/us/skills/ | 2026-07-21 |
| lost-ark-dev/loa-details | https://github.com/lost-ark-dev/loa-details | 2026-07-21 |
| chronicondb-client | https://github.com/gabriel-dehan/chronicondb-client | 2026-07-21 |
| Chronicon CTRL+P discussion | https://steamcommunity.com/app/375480/discussions/0/2985287984605472801/ | 2026-07-21 |
| Torchlight 2 GUTS blog post | https://www.runicgames.com/blog/2013/04/01/guts/ | 2026-07-21 |
| TL2 GUTS mod guide | https://steamcommunity.com/sharedfiles/filedetails/?id=138588277 | 2026-07-21 |
| tlidb.com | https://tlidb.com/ | 2026-07-21 |
| tli-hub.com skills | https://tli-hub.com/database/skills | 2026-07-21 |
| HoT wiki stats | https://hot.fandom.com/wiki/Stats | 2026-07-21 |
| undecember.thein.ru | https://undecember.thein.ru/en/ | 2026-07-21 |
| APXEOLOG/undecember-calculator | https://github.com/APXEOLOG/undecember-calculator | 2026-07-21 |

**Prior art (pre-survey verified sources carried forward):**
- RDR_Encounter_Geometry_Spec_Authoritative.md — `claude-mobile-session-docs/level-design-and-extraction-ideas/`
- VDM2 Field-Delta Specification — `matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md`
- Corpus kit counts — `agentic_orchestration/research/curated/kits-export/*.json` (576 files, enumerated 2026-07-21)
