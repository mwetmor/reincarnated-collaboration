# Join Surface Probe — True-Sources Flow into Engine
**Date:** 2026-07-23
**Mode:** A (analytical)
**Commissioner:** gandalf (ELICITOR brief for Matt session on true-sources plan)
**Purpose:** Evidence for the per-game-adapter-vs-baseline-vocabulary fork. READ-ONLY throughout.

---

## 1. corpus.db Schema Map

**Source:** `agentic_orchestration/research/curated/corpus.db` — `.tables`, `.schema`, `SELECT` queries only. No writes.

### Tables (relevant subset)

| Table | Role | Key columns |
|---|---|---|
| `canon_corpus` | Primary kit registry | `kit_id` (PK), `game`, `folk_name`, `corpus_class`, `tier`, `grain`, `mob_raw`, `geo_raw`, `elem_raw`, `core_skills`, `source` |
| `kit_numeric` | Exact numeric field store | `kit_id` (FK), `numeric_key`, `source_value` (REAL, immutable), `source_scale` (vocab tag), `rdr_value` (derived), `source_anchor` (verbatim quote) |
| `skill_geometry_band` | Per-skill geometry metadata | `kit_id` (FK), `skill_ordinal`, `source_skill`, `delivery_class`, `range_band`, `exact_json` (NULL until datamine ingest), `exact_source_type` |
| `kit_mapping` | Kit-level grade + mapping JSON | `kit_id`, `grade`, `terminal_state`, `mapping_json` |
| `normalization_rule` | Scale-to-RDR transform rules | `rule_id`, `source_scale`, `description`, `status` |
| `verify_ledger` | Verification verdicts | `kit_id`, `claim_family`, `claim_text`, `verdict`, `anchor_quote` |
| `kit_citations` | Source URL registry | `kit_id`, `url`, `cite_class`, `quarantined` |

### Per-game row counts (SQL: `SELECT game, COUNT(*) FROM canon_corpus GROUP BY game ORDER BY cnt DESC`)

| game | kits |
|---|---|
| poe1 | 94 |
| d2 | 60 |
| la | 57 |
| d3 | 49 |
| d4 | 46 |
| gd | 41 |
| poe2 | 38 |
| le | 37 |
| di | 25 |
| vs | 24 |
| tq | 21 |
| hot | 19 |
| chronicon | 17 |
| undecember | 17 |
| tl2 | 11 |
| tli | 9 |
| hades1 | 8 |
| hades2 | 5 |
| mcd | 5 |
| tq2 | 5 |
| tl1 | 2 |

**5-roster corpus-of-record:** d2 (60) + gd (41) + poe1 (94) + poe2 (38) + le (37) = 270 kits (per Matt 2026-07-21 ruling; la/d3/d4/di/etc. are attested-annex).

### Exact-numeric vs prose columns in canon_corpus

**Exact-numeric:** None directly in `canon_corpus` itself. All exact numerics live in `kit_numeric` (separate table, REAL typed, per `numeric_key`/`source_scale` pair).

**Prose/descriptor columns in canon_corpus:** `folk_name`, `mob_raw`, `geo_raw`, `ctrl_raw`, `def_raw`, `econ_raw`, `elem_raw` (all free-text descriptor strings). `core_skills` is a JSON array of skill name strings (prose, not numeric). `gx`, `lineage`, `grain`, `grain_note`, `source_urls` are citation/tagging prose.

**Typed-categorical:** `game`, `corpus_class` (enum: record/annex/system), `tier`, `grain`, lattice axes (`attr_val`, `range_val`, `tempo_val`, etc.) carry enum strings with associated `*_conf` REAL confidence scores.

**kit_numeric row count:** 458 rows total as of probe date. Concentrated in: `d2-fire-sorc` (188 rows), `d2-firewall-sorc` (106 rows), `poe2-bonestorm` (104 rows), `poe1-cyclone` (32 rows), `gd-flames-of-ignaffar-purifier` (26 rows). The bulk of corpus kits have zero `kit_numeric` rows — they hold prose/lattice data only.

**skill_geometry_band `exact_json` population:** 0 of 490 rows are populated. The `exact_json` and `exact_source_type` columns exist in schema (designed for datamine-lane ingest) but are NULL for all current entries. Derivation field is `dossier-prose` for all rows — geometry bands were authored from guide text, not raw files.

---

## 2. One-Skill Trace: Fire Ball / Fireball Across Three Sources

### 2a. D2 — Fire Ball, `Skills.txt` (fabd/diablo2, D2 1.13)

**File:** `agentic_orchestration/research/datamine-acquisition/d2/raw/Skills.txt` (256-column TSV)
**Row identified by:** `skill == "Fire Ball"` (col 1), `Id == 47` (col 2), `charclass == "sor"` (col 3)

Key fields extracted (SQL: Python `csv.DictReader` pass):

| Field | Value | Meaning |
|---|---|---|
| `skill` | Fire Ball | Skill name |
| `Id` | 47 | Numeric ID (join key into Missiles.txt, SkillCalc.txt) |
| `charclass` | sor | Class lock |
| `srvmissile` | fireball | Projectile definition ref |
| `reqlevel` | 12 | Minimum level to acquire |
| `maxlvl` | 20 | Skill hard cap |
| `mana` | 10 | Base mana cost at level 1 (raw integer, pre-shift) |
| `manashift` | 7 | Bit-shift divisor: actual mana = `mana >> manashift`; 10 >> 7 = ~0.078 per point (mana cost formula: `(mana + lvlmana*(slvl-1)) >> manashift`) |
| `lvlmana` | 1 | Mana cost delta per level |
| `minmana` | 1 | Minimum mana clamp |
| `EType` | fire | Element type |
| `EMin` | 12 | Base min fire damage at level 1 |
| `EMax` | 28 | Base max fire damage at level 1 |
| `EMinLev1` | 13 | Min damage delta for levels 1-8 (per level added above base) |
| `EMinLev2` | 23 | Min damage delta for levels 9-16 |
| `EMinLev3` | 28 | Min damage delta for levels 17-22 |
| `EMinLev4` | 33 | Min damage delta for levels 23-28 |
| `EMinLev5` | 38 | Min damage delta for levels 29+ |
| `EMaxLev1–5` | 15,25,30,35,40 | Max damage deltas, same band structure |
| `EDmgSymPerCalc` | `(skill('Fire Bolt'.blvl)+skill('Meteor'.blvl))*par8` | Synergy formula |
| `Param8` | 14 | Synergy damage bonus per synergy point (par8) |
| `HitShift` | 7 | Damage bit-shift for final delivery |

**Scaling shape:** BAND-DELTA system. Base `EMin`/`EMax` at level 1, then per-level increments that change in discrete bands by level tier (1-8, 9-16, 17-22, 23-28, 29+). The table does NOT store per-level absolute values; the caller reconstructs: `EMin_at_lvl = EMin + sum(EMinLevN * levels_in_band_N)`. Synergy adds a formula-computed bonus on top.

**Note on kit_numeric discrepancy:** The `d2-fire-sorc` kit in `kit_numeric` (188 rows, source: rankedboost.com) shows Fire Ball at level 1 with `EMin=6`, `EMax=15` (d2_fire_hit scale), whereas `Skills.txt` shows `EMin=12`, `EMax=28`. This is because the Skills.txt values are RAW parameters that get evaluated through the hit-damage formula chain (including `HitShift=7` bit-shift and the projectile's damage multiplier); the rankedboost values are post-formula player-facing numbers. These are NOT the same field — the `source_scale` tag `d2_fire_hit` anchors the post-formula value; `EMin`/`EMax` in Skills.txt are pre-formula inputs.

### 2b. PoE1 — Fireball, `gems.json` (brather1ng/RePoE, commit 8023a1d)

**File:** `agentic_orchestration/research/datamine-acquisition/poe1/raw/gems.json`
**Key:** `gems["Fireball"]` (string key; 1,017 gem entries total)

Key fields:

| Field | Value | Meaning |
|---|---|---|
| `cast_time` | 750 | Cast time in milliseconds |
| `static.crit_chance` | 600 | Base crit chance (hundredths of %: 600 = 6.00%) |
| `static.damage_effectiveness` | 270 | Damage effectiveness % (how much added damage applies) |
| `active_skill.id` | fireball | Internal skill ID |
| `active_skill.types` | Projectile, Spell, Fire, Area, … | Type flags |
| `stat_translation_file` | (string reference) | Links to `stat_translations.json` for display mapping |
| `static.stats[0].id` | spell_minimum_base_fire_damage | Stat identifier for min fire damage |
| `static.stats[1].id` | spell_maximum_base_fire_damage | Stat identifier for max fire damage |
| `static.stats[2].id` | base_chance_to_ignite_% | Static 25% ignite chance |
| `static.stats[3].id` | fireball_base_radius_up_to_+_at_longer_ranges | Radius stat ID |

**Per-level structure** (`per_level` dict, keys 1–40):

| Level | Mana cost | Min fire dmg (stat[0]) | Max fire dmg (stat[1]) | Radius delta (stat[3]) |
|---|---|---|---|---|
| 1 | 6 | 9 | 14 | 0 |
| 5 | 9 | 28 | 42 | 2 |
| 10 | 14 | 148 | 222 | 4 |
| 20 | 25 | 1640 | 2460 | 9 |

**Scaling shape:** EXPLICIT-PER-LEVEL rows. Every level from 1 to 40 has a complete row with absolute values. No deltas, no formulas to resolve. `stats` array positional — stat[0] = min damage, stat[1] = max damage. However, stat array members use anonymous position keys (`stats[0]`, `stats[1]`) rather than named fields; the identity of each position is established by `static.stats[].id`. This ID indirection is the critical structural feature: the numeric values in `per_level[N].stats` are POSITION-matched to `static.stats[N].id`. The display name for a stat requires a separate lookup in `stat_translations.json`.

**GQL note:** `damage_effectiveness = 270` means added fire damage from gear/support gems applies at 270% effectiveness — this is a PoE-native concept with no D2 or GD equivalent.

### 2c. GD — Fire projectile skills, `all_skills.js` (grimtools monsterdb.js extraction, GD 1.3.0.0)

**File:** `agentic_orchestration/research/datamine-acquisition/gd/raw/all_skills.js`
**Structure:** JS object literal `{sk<ID>: {...}, sk<ID>: {...}, ...}` extracted from `window.allSkills`. 3.0 MB, no REST API, embedded in browser JS payload.

**No canonical "Fireball" equivalent in GD.** GD fire projectile skill examined: `sk296` (Canister Bomb-class ring-projectile, labeled `tagCompSkillA014Name`), which is the closest structural analog (fire element, projectile, AoE). Key fields:

| Field | Value/Shape | Meaning |
|---|---|---|
| `l` | `"Skill_AttackProjectileRing"` | Template/behavior class |
| `templateName` | `"t16"` | GD template ID |
| `skillMaxLevel` | 60 | GD skills go to 60 (vs D2's 20, PoE's 20/40) |
| `skillManaCost` | Array of 60 integers: [18,22,…,507] | Per-rank mana cost (absolute value each rank) |
| `offensiveFireMin` | Array of 60 integers: [57,83,…,2276] | Per-rank min fire damage |
| `offensiveFireMax` | Array of 60 integers: [85,121,…,2915] | Per-rank max fire damage |
| `projectileLaunchNumber` | 12 | Projectiles launched per cast |
| `projectileExplosionRadius` | 1.5 | Explosion AoE radius |
| `offensiveSlowFireMin` | Array of 60 integers: [10,13,…,933] | Per-rank ignite DoT damage |
| `offensiveSlowFireDurationMin` | 2 | Ignite duration |
| `projectileDamageRange1Scale` | 50 | Damage range scale parameter |

**Scaling shape:** RANK-ARRAYS. Every numeric parameter that scales with skill rank is stored as a flat integer array, one value per rank (60 values for a max-60 skill). Absolute values at every rank, no deltas, no formula indirection. Field names are GD-engine-native: `offensiveFireMin`, `offensiveFireMax`, `skillManaCost`, `projectileLaunchNumber`. Skills are identified by generated numeric IDs (`sk296`, `sk4015`, etc.) with no stable name string in the payload — the `skillDisplayName` field contains a localization tag (`tagCompSkillA014Name`), not an English string.

**HP/DPS gap (per ACQUISITION-LOG-2026-07-21.md):** GD monster HP and DPS are NOT stored in the `monsterdb.js` payload; they are computed at browser render time from base-stat tables and difficulty modifiers. This means GD's `all_skills.js` has skill values but the monster-damage lane is absent. CONFIRMED ABSENT.

### 2d. Compact comparison table

| Property | D2 Fire Ball | PoE1 Fireball | GD sk296 (fire projectile) |
|---|---|---|---|
| Level cap | 20 (+synergy) | 40 (1-20 normal, 21-40 alt qual) | 60 ranks |
| Scaling shape | Band-deltas (5 bands) | Explicit per-level rows (40 rows) | Rank-arrays (60-element arrays) |
| Min dmg at L1/R1 | EMin=12 (raw, pre-formula) | stat[0]=9 (post-formula absolute) | offensiveFireMin[0]=57 (absolute) |
| Max dmg at L1/R1 | EMax=28 (raw) | stat[1]=14 (absolute) | offensiveFireMax[0]=85 (absolute) |
| Mana cost storage | `(mana + lvlmana*(slvl-1)) >> manashift` formula | Per-level Mana integer | Per-rank array |
| Field name for min dmg | `EMin` + `EMinLev1-5` | `spell_minimum_base_fire_damage` (stat ID) | `offensiveFireMin` (array) |
| Field name for max dmg | `EMax` + `EMaxLev1-5` | `spell_maximum_base_fire_damage` (stat ID) | `offensiveFireMax` (array) |
| Stat vocabulary | Column-name positional (EMin, EMax, ELen, etc.) | ID-string in static.stats[].id, position-matched | Named per-type field (offensiveFireMin, offensivePhysicalMin, etc.) |
| Synergy/support system | EDmgSymPerCalc formula expression | Support gem stat IDs in stat_conversions | Not present in this payload |
| Damage effectiveness | Not a concept | static.damage_effectiveness = 270% | Not a concept |
| Unique ID | `Id` integer (47) + `skill` name string | `active_skill.id` string ("fireball") + gem name key | `sk<N>` generated numeric (sk296) |
| Localization | English name in `skill` column | English name as gem dict key | Localization tag string (tagCompSkillA014Name); no English |

---

## 3. Candidate Per-Game Join Keys

### How each source identifies a skill uniquely

**D2 (Skills.txt):**
- Primary key: `Id` (integer, col 2) — used internally for cross-file joins (e.g., SkillCalc.txt, Missiles.txt)
- Human key: `skill` (col 1, English string, e.g., "Fire Ball") — join key for lookup by name
- Class scope: `charclass` (col 3, e.g., "sor") — required to disambiguate same-named skills across classes (though D2 names are unique across classes in practice)
- Composite key that's stable: `(charclass, skill)` string pair

**PoE1 (gems.json):**
- Primary key: gem dict key (e.g., "Fireball") — this is the canonical English name as a dict key in the gems.json top-level object
- Internal ID: `active_skill.id` (e.g., "fireball") — snake_case version; not always a simple lowercase of the gem name
- No numeric ID exposed in RePoE; PyPoE's GGPK extraction has internal numeric IDs, but RePoE normalizes to name keys
- Kit → skill mapping: gem name string matches the skill name in corpus `core_skills` JSON array

**GD (all_skills.js):**
- Primary key: `sk<N>` numeric ID (e.g., "sk296") — generated, opaque, not a stable semantic key
- Localization ref: `skillDisplayName: "tagCompSkillA014Name"` — localization lookup tag, not English
- Display-name resolution requires a separate localization table not present in this payload
- No English skill name string is embedded in the JS payload for skills
- Functional label: `l` field (e.g., "Skill_AttackProjectileRing") — template/behavior class, not a skill name

**Corpus join conventions (from KIT-FIDELITY / `d2-fire-sorc` lineage):**
- `kit_id` in `canon_corpus`: game-prefixed composite string, e.g., `d2-fire-sorc`, `poe1-tornado-shot`, `gd-blade-trap`
- `gx` field: gap-tracking reference (e.g., `GAP-D2-01` for Fire Sorceress kits in the fire cohort)
- `source_id` in skill_geometry_band: `source_skill` column stores the English skill name as it appears in guides/core_skills (e.g., "Fire Ball", "Meteor")
- KIT-FIDELITY confirmed that `source_id = "d2-fire-sorc"` byte-joins cleanly; the kit_id IS the stable join key into corpus.db
- `skill_geometry_band` joins on `(kit_id, skill_ordinal)` — ordinal is sequential within a kit, tied to position in `mapping_json.skills[]`

**Cross-source name stability problem:** D2 uses English skill names directly (stable, canonical). PoE1 uses English gem names as dict keys (stable within RePoE). GD uses generated numeric IDs with localization tag refs — English name is NOT in the raw payload. Bridging GD `sk<N>` to English skill name requires either the localization table (not fetched) or grimtools.com/db (separate pre-built database). This means GD skill join to corpus would require an intermediate mapping table: `(gd_sk_id → English_skill_name → corpus kit_id)`.

---

## 4. Candidate Normalized Exact-Fields Schema

Eight to twelve fields that all three sources could adapt INTO. Designed to represent a single skill at a single level/rank for damage-and-cost comparison.

| Field | Description | D2 | PoE1 | GD |
|---|---|---|---|---|
| `game` | Source game identifier | Native ("d2") | Native ("poe1") | Native ("gd") |
| `skill_name` | English canonical skill name | Direct: `skill` col | Direct: gem dict key | ABSENT from raw payload; requires localization lookup |
| `level_or_rank` | Integer skill level/rank | 1–20 (derived from band formula) | 1–40 (explicit row key) | 1–60 (array index) |
| `dmg_min` | Minimum damage output (fire, physical, or primary element) | DERIVED: EMin + sum(EMinLevN * levels_in_band) + synergy; raw values are pre-formula | Direct: per_level[N].stats[0] (absolute) | Direct: offensiveFireMin[rank-1] (absolute) |
| `dmg_max` | Maximum damage output | Same derivation as dmg_min | Direct: per_level[N].stats[1] | Direct: offensiveFireMax[rank-1] |
| `mana_cost` | Resource cost per activation | DERIVED: `(mana + lvlmana*(slvl-1)) >> manashift`; formula required | Direct: per_level[N].costs.Mana | NATIVE-ARRAY: skillManaCost[rank-1] |
| `cast_time_ms` | Cast or attack time in milliseconds | ABSENT from Skills.txt directly; in Missiles.txt / animation frames (needs lookup) | Direct: `cast_time` (750 ms) | ABSENT from all_skills.js; in DBR animation records |
| `aoe_radius` | Area-of-effect radius (units TBD per game) | ABSENT (missile radius in Missiles.txt, not Skills.txt) | DERIVED: per_level[N].stats[3] value for radius stat ID | Direct: projectileExplosionRadius (1.5, units = GD map units) |
| `proj_count` | Projectile count per activation | DERIVED: in Missiles.txt (srvmissile ref) | DERIVED: count stat ID in static.stats | Direct: projectileLaunchNumber (e.g., 12) |
| `element` | Damage element type | Direct: `EType` col (e.g., "fire") | DERIVED: from active_skill.types array (look for "Fire", "Cold", etc.) | DERIVED: field name prefix (offensiveFire*, offensiveCold*, etc.) |
| `dmg_effectiveness_pct` | PoE-native added-damage scaling factor | CANNOT FILL: concept does not exist in D2 | Direct: static.damage_effectiveness (270) | CANNOT FILL: concept does not exist in GD |
| `crit_chance_pct` | Base critical strike chance | Derived from charclass base crit (D2 spells have fixed 0% crit in classic D2) | Direct: static.crit_chance / 100 (e.g., 6.00%) | Derived: offensiveCritChance field in DBR (NOT in grimtools payload for skills) |

**Fill-status summary:**

| Field | D2 fill | PoE1 fill | GD fill |
|---|---|---|---|
| game | Native | Native | Native |
| skill_name | Native | Native | ABSENT (localization required) |
| level_or_rank | Derived (band walk) | Native (row key) | Native (array index) |
| dmg_min | Derived (formula) | Native | Native |
| dmg_max | Derived (formula) | Native | Native |
| mana_cost | Derived (formula) | Native | Native |
| cast_time_ms | ABSENT (cross-file) | Native | ABSENT (cross-file) |
| aoe_radius | ABSENT (cross-file) | Derived (stat lookup) | Native |
| proj_count | ABSENT (cross-file) | Derived (stat lookup) | Native |
| element | Native | Derived (type list) | Derived (field-name prefix) |
| dmg_effectiveness_pct | CANNOT FILL | Native | CANNOT FILL |
| crit_chance_pct | CANNOT FILL (0% for spells in D2 classic) | Native | ABSENT from grimtools payload |

**Implication for adapter-vs-baseline fork:** If D2 is used as the baseline vocabulary, `dmg_min`/`dmg_max` must be derivation-outputs for all games (because D2 raw values are pre-formula); PoE's `dmg_effectiveness_pct` has no D2 carrier and would be dropped or approximated; GD's skill name requires a separate resolution step not present in D2's flat structure. If PoE1 is the baseline, D2 fields must be reconstructed via band-walk formulas; GD localization is still broken; D2 crit semantics (fixed 0%) become a special case.

No source is naturally flat enough to serve as a baseline for the others without losing structurally load-bearing fields.

---

## 5. Top-3 Collision Risks

### Collision 1: Scaling-representation heterogeneity

**Fields affected:** `dmg_min`, `dmg_max`, `mana_cost` — the three core numeric fields any adapter must populate.

D2 Skills.txt stores damage as **base-plus-banded-deltas**: `EMin=12` is the level-1 base, and each of five `EMinLev1-5` values is a per-level increment that applies within a discrete level band (1-8, 9-16, 17-22, 23-28, 29+). To get damage at level N requires knowing which bands apply and accumulating deltas — this is a formula computation, not a table lookup. Furthermore, the Skills.txt values are pre-`HitShift` raw integers; the actual delivered damage uses a bit-shift (`HitShift=7`) that the client engine applies. Mana cost also uses a bit-shift (`manashift=7`).

PoE1 gems.json stores **explicit per-level absolute values**: level 1 has `stats[0]=9`, level 20 has `stats[0]=1640`. No formula required; each level row is self-contained. But the stat array is positionally indexed with anonymous positions — the meaning of position 0 vs position 1 is established only by `static.stats[0].id = "spell_minimum_base_fire_damage"`. If the static.stats ordering changes between skills, the position mapping breaks.

GD all_skills.js stores **rank-arrays**: `offensiveFireMin:[57,83,...,2276]` (60 values, one per rank). Fully self-contained, positional by rank index. Field names encode element type (`offensiveFire*` vs `offensiveCold*` vs `offensivePhysical*`), meaning a single normalized `dmg_min` column requires knowing which element prefix to read — and a multi-element skill has multiple separate arrays.

A normalized adapter must: for D2, implement band-walk formula + bit-shift resolution before populating `dmg_min`; for PoE1, implement stat-ID position lookup + stat_translations linkage; for GD, implement element-prefix detection + array index selection. None of these can share adapter logic. A D2-shaped baseline (base + deltas) would structurally distort PoE and GD data by forcing reconstruction of delta values from their natively-absolute numbers.

### Collision 2: Stat-vocabulary and unit mismatches

**Fields affected:** `element`, `dmg_effectiveness_pct`, `crit_chance_pct`, `aoe_radius` units.

D2 uses a single `EType` column for element (value: "fire", "cold", "ltng", "pois", "mag"). The vocabulary is a short enum of game-specific abbreviations ("ltng" for lightning, "pois" for poison). Damage is measured in "fire hit points" (post-shift integer). Mana cost is a shifted integer. There is no "damage effectiveness" concept — added damage from items is additive to the formula output, not modulated by a gem-level multiplier.

PoE1 uses `static.stats[].id` string identifiers like `"spell_minimum_base_fire_damage"`, `"base_chance_to_ignite_%"`, `"fireball_base_radius_up_to_+_at_longer_ranges"` — long snake_case strings that are game-engine internal IDs. `damage_effectiveness = 270` is a PoE-native concept that controls how much added-damage from passive tree and gear applies to the skill. Crit chance is stored as hundredths of a percent (600 = 6.00%). Area radius uses game-specific units (PoE uses its own unit system; 16 units for Cyclone per corpus).

GD uses `offensiveFireMin`/`offensiveFireMax` (GD engine field names from DBR records), `projectileLaunchNumber`, `projectileExplosionRadius` in GD map units. Crit chance in DBRs uses `offensiveCritChance` (NOT present in the grimtools all_skills.js payload for most skills — it appears in DBR records, which are a separate acquisition path). GD also has `weaponDamagePct` for some skills (weapon damage scaling), a concept D2 has for some attack skills but PoE handles entirely differently via `damage_effectiveness`.

Unit systems do not align: D2 radius comes from Missiles.txt in game-internal units; PoE radius is in PoE units (16 units for Cyclone's 16-unit radius); GD radius is in GD map units (1.5 explosion radius). There is no cross-game conversion constant.

A baseline using D2's `EType` enum would fail to represent PoE's compound type system (a PoE skill can be Fire+Projectile+Area+Spell simultaneously; D2 supports only one `EType`). Conversely, a PoE stat-ID baseline would produce excessively long field names and require a translation pass for every D2 and GD field.

### Collision 3: Patch/name instability and ID-resolution fragility

**Fields affected:** `skill_name` (join key), `level_or_rank` (range), `dmg_min`/`dmg_max` (value at any given level).

D2 (1.13 classical data from fabd/diablo2): Skill names in Skills.txt are stable for the 1.13 era. However, the ACQUISITION-LOG notes that D2R current values require a separate CASC extraction (Phase 2 item) — D2 1.13 values differ from D2R values for some skills. The `kit_numeric` rows for `d2-fire-sorc` (anchored to rankedboost.com) differ from Skills.txt raw values (Fire Ball L1: corpus shows 6-15, Skills.txt shows EMin=12/EMax=28) because they represent different evaluation points of the same formula chain. A join on raw-file values vs. post-formula corpus values will produce mismatches.

PoE1 (brather1ng/RePoE, commit 8023a1d, 2022-09-06): The ACQUISITION-LOG flags this as stale — the live-maintained fork is `repoe-fork/repoe` (updated 2026-07-14). Skill stat values change between patches; the current RePoE payload represents patch-era data from 2022. For skills with patch history, `per_level` values at any given level may differ from current game values. The gem dict key ("Fireball") is stable as an English name; the internal `active_skill.id` ("fireball") is stable. However, quality_stats IDs and stat array membership can change between patches, breaking positional stat-array mapping.

GD (grimtools monsterdb.js, GD 1.3.0.0): The `sk<N>` ID system is the most fragile. These IDs are generated by the GD engine and embedded in the compiled asset; there is no guarantee that `sk296` in one game version refers to the same skill as `sk296` in another. The `skillDisplayName` localization tag (`tagCompSkillA014Name`) is more stable but requires a localization file not present in this payload. English skill names are entirely absent from the raw payload — any join to the English-named corpus (where `core_skills = ["Blackwater Cocktail", "Canister Bomb", ...]`) must go through an intermediate resolution step that is not currently implemented or scripted. This makes GD the most difficult source to join against the corpus's English-name-based kit registry.

---

## Knowledge Gaps Not Resolved

1. **D2 post-formula values vs Skills.txt raw:** The corpus `kit_numeric` for `d2-fire-sorc` anchors to rankedboost.com post-formula values, which differ from Skills.txt EMin/EMax by the HitShift formula. The exact reconciliation formula (pydiablo path or SkillCalc.txt parse) has not been executed in this probe. A normalization rule bridging D2 raw-TSV fields to corpus `source_scale = "d2_fire_hit"` is needed before the two can be joined.

2. **GD English-name-to-sk-ID mapping table:** Not available in current payload. The `all_skills.js` file does not embed English names; a secondary fetch of the GD localization strings or grimtools.com/db lookup would be required to populate a name bridge. This gap blocks GD skill-lane joins to the English-named corpus.

3. **PoE1 RePoE staleness:** The brather1ng payload is 2022-era. For 94 PoE1 kits, some values may differ from current patch. Repoe-fork fetch not executed in this probe.

4. **GD crit_chance_pct field:** `offensiveCritChance` appears in DBR records (AssetManager extraction path, Phase 2) but is absent from the grimtools all_skills.js payload used here. Crit comparison across all three sources is therefore incomplete.

5. **Cast time for D2 and GD:** `cast_time_ms` is not in Skills.txt or all_skills.js; it resides in animation frame data (D2: animation timing in .dc6 assets; GD: character animation DBRs). This field is effectively a cross-file join for two of three sources.

---

## Source List

| Source | Path / URL | Access date |
|---|---|---|
| corpus.db | `agentic_orchestration/research/curated/corpus.db` | 2026-07-23 |
| D2 Skills.txt | `agentic_orchestration/research/datamine-acquisition/d2/raw/Skills.txt` | 2026-07-23 |
| PoE1 gems.json | `agentic_orchestration/research/datamine-acquisition/poe1/raw/gems.json` | 2026-07-23 |
| GD all_skills.js | `agentic_orchestration/research/datamine-acquisition/gd/raw/all_skills.js` | 2026-07-23 |
| ACQUISITION-LOG-2026-07-21 | `agentic_orchestration/research/datamine-acquisition/ACQUISITION-LOG-2026-07-21.md` | 2026-07-23 |
| Coverage matrix | `agentic_orchestration/research/datamine-coverage-matrix-2026-07-21.md` | 2026-07-23 |
| fabd/diablo2 upstream | https://github.com/fabd/diablo2 | 2026-07-21 (per acquisition log) |
| brather1ng/RePoE upstream | https://github.com/brather1ng/RePoE | 2026-07-21 (per acquisition log) |
| grimtools monsterdb.js upstream | https://www.grimtools.com/monsterdb/ | 2026-07-21 (per acquisition log) |
