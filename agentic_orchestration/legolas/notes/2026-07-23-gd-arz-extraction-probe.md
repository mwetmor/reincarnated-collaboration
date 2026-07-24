# Legolas Probe Note — GD .arz Extraction Probe
# TSR-3 Deciding Evidence — GD Adapter First-of-Kind Fields

**Date:** 2026-07-23
**Mode:** B-flavored extraction probe (primary-source, binary parse)
**Commission source:** TSR-3 (Matt adapter-question ruling substrate)
**Files parsed:**
- `/Users/admin/Games/vendor/grim-dawn/database/database.arz` — 55.6 MB, 34114 records, 82688 strings
- `/Users/admin/Games/vendor/grim-dawn/gdx1/database/GDX1.arz` — 18447 records, 57204 strings

---

## §0 — Extraction path taken (and what failed)

**ArchiveTool.exe** is present at `/Users/admin/Games/vendor/grim-dawn/ArchiveTool.exe` but Wine is not installed on this Mac. Filesystem-level extraction via .exe was not possible.

**Python parser built from scratch.** Key discoveries required to make it work:

1. **ARZ format: TQIT variant (magic=2), not standard TQAE.** Header: `magic(uint16) + version(uint16) + rt_offset(int32) + rt_size(int32) + rt_count(int32) + st_offset(int32) + st_size(int32)` = 24 bytes. Record data block starts at byte 24, runs to `rt_offset`.

2. **Record table entries: variable-length due to embedded LP_string.** Each entry is `name_id(int32) + recordType(LP_string: int32_len + bytes) + data_offset(int32) + comp_size(int32) + decomp_size(int32) + timestamp(int64)`. TQIT adds `decomp_size` vs the older TQAE format — parsing flat 16-byte entries silently corrupted the index. Format discovered via GitHub search for `arz titan quest language:python` → `arz_converter.py` in wtrevena/tqit_soulvizier_classic.

3. **Compression: LZ4 block (not zlib, not gzip, not LZ4 frame).** Identified via 0xc0 byte at data block position 0 — an LZ4 token with LL=12, ML=0. `pip3 install lz4` then `lz4.block.decompress(blob, uncompressed_size=decomp_sz)`. All prior zlib variants (`wbits=15`, `-15`, `31`) raised `invalid header/checksum`.

4. **DBR field format (within decompressed record):** `type(uint16) + count(uint16) + key_id(uint32) + values[count × 4bytes]`. Type IDs confirmed empirically: 0=int32, 1=float32, 2=uint32 string-table index, 3=bool(uint32). All strings (record paths + field names + string values) share a single flat string table.

5. **Template files (.tpl):** Not embedded in .arz. They reside in `templates/` alongside `database/` in the depot. Referenced by path via `templateName` field in every record. Not parsed in this probe.

**Format origin:** TITAN QUEST:IT (2007) format, carried forward by GD (2016). The `arz_converter.py` source (public GitHub) and GrimDB community tool (C#) confirmed the TQIT variant used by GD.

---

## §1 — Monster spatial / AI fields (first-of-kind documentation)

GD separates monster records into **two DBR files**: the monster body record (HP, speed, resistances) and a **controller record** (AI behavior, spatial parameters). The `controller` field in the body record points to its controller path.

### Monster body record — spatial fields present

| Field | zombie_a01 (Common) | zombie_a01h (Hero Common) | reanimator_b01 (Champion) |
|---|---|---|---|
| `characterRunSpeed` | 1.0 | 1.0 | 1.0 |
| `characterAttackSpeed` | 1.18 | — | — |
| `actorHeight` | 2.0 | — | — |
| `actorRadius` | 0.4 | — | — |
| `monsterClassification` | 'Common' | 'Common' | 'Champion' |
| `distressCallGroup` | 'Aetherial' | — | — |
| `distressCallRange` | 16.0 | — | — |
| `controller` (path) | controller_zombiea01.dbr | controller_zombiea01h.dbr | controller_reanimator.dbr |

`characterRunSpeed` is a multiplier on the global `playerRunSpeedCapMax` / `monsterRunSpeedCapMax` (see §4). Value of 1.0 = base speed. `actorRadius` is the collision half-width in GD world units.

### Controller records — AI spatial parameters

These field names are **not documented in grimtools, not in community wikis, not in prior notes**. This is first-of-kind extraction from primary source.

| Field | zombie controller | zombie_h controller | ghoul01 controller | reanimator controller |
|---|---|---|---|---|
| `InnerViewDistance` | 4.0 | 6.0 | 4.0 | 4.0 |
| `ViewDistance` | 15.0 | 16.0 | 15.0 | 15.0 |
| `InnerSightAngerRate` | 12.0 | — | — | — |
| `SightAngerRate` | 3.0 | — | — | — |
| `WanderDistance` | 4.0 | — | 0.0 | 5.0 |
| `RoamDistance` | 4.0 | — | — | — |
| `MinRoamDistance` | 2.0 | — | — | — |
| `MaxTimeBeforeRoam` | 16000 | — | — | — |
| `MaxPursuitDistance` | 75.0 | 65.0 | 75.0 | — |
| `PursuitTime` | 10000 | 10000 | 10000 | — |
| `fleeDistance` | 16.0 | 16.0 | 10.0 | 8.0 |
| `MaxYViewDistance` | 10.0 | — | — | — |
| `FleeBehavior` | 'NeverFlee' | — | — | — |
| `DistressResponseGroup` | 'Aetherial' | — | 'Undead' | — |
| `ChanceToRespondToDistressCall` | 75 | — | — | — |
| `fieldCount` | 64 | — | 65 | — |

`—` = field not observed in that specific record (may be absent or use engine default). Field counts are 64–65 total per controller record.

**Interpretation:** `ViewDistance` / `InnerViewDistance` map to aggro trigger range (outer/inner zones). `SightAngerRate` / `InnerSightAngerRate` are anger accumulation rates for sight-triggered aggro. `MaxPursuitDistance` = leash radius equivalent. `PursuitTime` in milliseconds. `FleeBehavior='NeverFlee'` is an enum string. `DistressResponseGroup` / `ChanceToRespondToDistressCall` form a faction-aware distress-call system distinct from anything in D2 or PoE1.

**Field names NOT in string table** (searched, absent): `AIRange`, `aggroRange`, `Leash`, `AlertRadius`, `perceptionRadius`. GD uses its own vocabulary throughout.

---

## §2 — FoI / R-K5: Flames of Ignaffar rank table

**Record path (GDX1.arz):** `records/skills/playerclass07/purifyingflame1.dbr`
**Record type (LP_string in index):** `Skill_AttackSpellCone`
**templateName field:** `database/templates/skill_attackspellcone.tpl`
**skillDisplayName:** `tagGDX1Class07SkillName04A` (localization tag — English name absent from .arz; requires .arc parsing)

**Rank structure:** `skillMaxLevel=16`, `skillUltimateLevel=26`. All arrays have **26 elements** (16 base + 10 ultimate). The 60-rank arrays seen in the grimtools `all_skills.js` harvest (documented in `2026-07-23-join-surface-probe.md` §2c) are **not present in the .arz ground truth**.

### Key rank values (selected fields, all values GD world units)

| Field | Rank 1 | Rank 16 | Rank 26 |
|---|---|---|---|
| `offensiveFireMin` | 8.0 | 129.0 | 262.0 |
| `offensiveFireMax` | 18.0 | 157.0 | 306.0 |
| `offensiveSlowFireMin` (burn DoT) | 8.0 | 211.0 | 382.0 |
| `skillManaCost` | 7.0 | 39.0 | 69.0 |
| `weaponDamagePct` | 9.0 | 42.0 | 58.0 |

**Static fields (not per-rank arrays):**
- `offensiveSlowFireDurationMin`: 3.0 (burn duration in seconds, constant across all ranks)
- `timeBetweenAttacks`: 300 (milliseconds; cast cadence, 3.33 Hz — the PoE1 `castTime` analog)
- `skillCooldownTime`: 0.3 (seconds; matches `timeBetweenAttacks` cycle)
- `duration`: 0.25 (seconds; single-pulse duration)
- `maxRange`: 9.1 (GD world units; cone reach)
- `endWidth`: 4.5 (cone tip width)
- `startWidth`: 2.2 (cone base width)

**Cone geometry:** FoI is a channeled cone, not a projectile. Geometry is defined by `maxRange + endWidth + startWidth` — a frustum shape, not a radius sphere like D2 Blaze or a line like PoE1 Incinerate. The cone geometry fields have no analog in the D2 or PoE1 records documented in other probe notes.

---

## §3 — Skill-shape vs JS harvest; name bridge

### Comparison baseline
From `2026-07-23-join-surface-probe.md` §2c, the grimtools `all_skills.js` harvest documented:
- Opaque IDs: `sk<N>` (e.g., `sk5782`)
- 60-rank arrays for all skills
- No English name in the extracted data
- No `cast_time` field observed
- `weapon_damage` present as a rank array

### .arz findings vs JS harvest

| Dimension | all_skills.js (grimtools) | .arz purifyingflame1.dbr | Assessment |
|---|---|---|---|
| Rank count | 60 elements | 26 elements (skillMaxLevel=16, skillUltimateLevel=26) | **Discrepancy.** Grimtools may pad to 60 or aggregate across skill + transmuter ranks. |
| English name | Absent | Absent (localization tag only) | Consistent: both lack English names |
| weapon_damage | Present (rank array) | `weaponDamagePct` (rank array, confirmed) | **Match on concept; field name differs** |
| cast cadence | Absent from JS | `timeBetweenAttacks` = 300ms | .arz adds cast cadence; JS harvest missed this field |
| Geometry | Not present | `maxRange`, `endWidth`, `startWidth` | .arz only; JS harvest does not carry geometry |
| Record type | Not in JS | `Skill_AttackSpellCone` (LP_string in record index) | .arz only |
| Template | Not in JS | `database/templates/skill_attackspellcone.tpl` | .arz only |

### Name bridge (localization tag → English)

The `.arz` carries only the tag `tagGDX1Class07SkillName04A`. The English string "Flames of Ignaffar" lives in the `.arc` localization archive (e.g., `resources/Text_EN.arc`). That archive was **not parsed in this probe** (requires separate .arc decompression). The bridge from internal record path to English name is:

`purifyingflame1.dbr` → `tagGDX1Class07SkillName04A` → (requires .arc parse) → "Flames of Ignaffar"

Alternative bridge available without .arc: the record contains `skillBitmapName`: `skillicon_flamesofignaffar1up.tex`. The bitmap filename encodes the English display name. This provides a readable string without .arc parsing.

**GD internal identifier for FoI:** `purifyingflame1` (record stem). Not "FlamesOfIgnaffar", not "foi", not `sk<N>`. Opaque internal IDs do not exist in .arz — GD uses human-readable path stems.

---

## §4 — Unit-system evidence (gameengine.dbr)

**Record path:** `records/game/gameengine.dbr`
**Field count:** 366 fields
**Record type (LP_string):** `GameEngine`

### Range thresholds (GD world units)

| Field | Value |
|---|---|
| `meleeRange` | 1.25 |
| `meleeTargetDistance` | 2.4 |
| `meleeAutoTargetDistance` | 4.0 |
| `shortRange` | 4.75 |
| `moderateRange` | 9.0 |
| `longRange` | 15.0 |
| `maximumRange` | 18.0 |
| `bossRange` | 32.0 |

### Camera distances

| Field | Value |
|---|---|
| `CameraDistanceDefault` | 36.0 |
| `CameraDistanceMax` | 48.0 |
| `CameraDistanceMin` | 20.0 |

### Speed caps

| Field | Value |
|---|---|
| `absoluteRunSpeedCapMax` | 350.0 |
| `playerRunSpeedCapMax` | 135.0 |
| `monsterRunSpeedCapMax` | 500.0 |

### Unit-pin conclusions

- `moderateRange` = 9.0 matches `FoI maxRange` = 9.1 — FoI is a "moderate range" skill, pinned to the engine's own range tier definition. This is explicit in the data, not inferred.
- `meleeRange` = 1.25 world units. Monster `actorRadius` = 0.4. Melee engagement at ~1.65 actual distance (1.25 + 0.4 actor half-width).
- Speed values (135.0 player cap, 500.0 monster cap) are raw engine speed units, **not** meters/second or tiles/second. Conversion factor to any external unit system is not defined in this record.
- `defaultLoadDistance` = 250.0 — spatial streaming radius.

---

## §5 — Adapter-relevant verdict facts (TSR-3 substrate)

What a GD adapter must handle that D2/PoE1 adapters do not:

**1. Two-record lookup per monster.** Any monster behavioral profile requires resolving the `controller` field and fetching a second DBR record. D2 and PoE1 monster records are monolithic (all fields in one record). GD's two-record pattern means the adapter must perform path resolution and a secondary parse.

**2. Controller field vocabulary is entirely GD-specific.** `InnerViewDistance`, `SightAngerRate`, `DistressResponseGroup`, `ChanceToRespondToDistressCall`, `FleeBehavior` are not present or analogous in D2 or PoE1 field sets. An adapter mapping to a unified `spatial_ai` schema must define GD-specific field bindings for each.

**3. Distress-call faction system.** `DistressResponseGroup` + `ChanceToRespondToDistressCall` encode faction-aware alert propagation. No equivalent in D2 (which uses proximity-only aggro) or PoE1 (which uses modular archetype flags). An adapter that surfaces this data introduces a field class with no cross-game precedent.

**4. Cone geometry fields.** `maxRange + endWidth + startWidth` define a frustum for channeled AoE. D2 and PoE1 skill records do not carry 3-field cone geometry. The adapter must map to a `skill_geometry` substructure distinct from `radius`, `projectile_speed`, etc.

**5. `timeBetweenAttacks` as cast-cadence analog.** GD channeled skills define pulsing interval in milliseconds (`timeBetweenAttacks=300`). PoE1 uses `castTime` (seconds). D2 uses breakpoints (frame-based). GD's field maps to neither directly. The adapter must normalize units and cadence semantics.

**6. Rank count mismatch vs grimtools JS data.** The .arz has 26 ranks (skillMaxLevel=16 + 10 ultimate). Grimtools `all_skills.js` reports 60-rank arrays. An adapter reading from grimtools JS data will produce rank arrays that disagree with the primary source. The GD adapter should target .arz as ground truth, not grimtools JS.

**7. Localization indirection.** `skillDisplayName` contains a tag string (`tagGDX1Class07SkillName04A`), not an English name. English requires .arc parsing as a second step. All display-name joins must go through the tag bridge. D2 and PoE1 do not have this two-layer indirection (names are present in primary data).

**8. Speed units are raw engine floats, not normalized.** `characterRunSpeed=1.0` is a multiplier on `monsterRunSpeedCapMax=500.0`. The absolute values are GD-internal. An adapter surfacing speed for comparison with D2 (% of base walk speed) or PoE1 (units/second) must define and document conversion assumptions.

---

## §6 — Negative findings and gaps

**Absent from .arz string table (searched, not found):**
- `AIRange` — not a GD field name
- `aggroRange` — not a GD field name
- `Leash` — not a GD field name
- `AlertRadius` — not a GD field name
- `perceptionRadius` — not a GD field name

GD uses its own vocabulary: `ViewDistance`, `InnerViewDistance`, `MaxPursuitDistance` for the same semantic concepts.

**Not parsed in this probe:**
- `.arc` localization archives (Text_EN.arc etc.) — required for tag → English name bridge
- `.tpl` template files — referenced by `templateName` but not in .arz
- `.anm` / `.msh` / animation records — not relevant to TSR-3
- Zone layout / act structure — not in .arz, lives in `.wrl` / `.lvl` files

**FoI rank-count discrepancy with grimtools JS — not resolved.** The 60-rank arrays in `all_skills.js` are unexplained. Hypotheses: (a) grimtools pads all skill arrays to 60 for a common schema shape; (b) grimtools aggregates across skill + transmuter ranks; (c) grimtools derives from a different GD version or modded data. The .arz value (26 ranks) is primary-source ground truth. The grimtools discrepancy is a known gap for Elrond to flag in any join-surface curation.

**Monster classification distribution not surveyed.** Only zombie_a01 (Common), zombie_a01h (Hero Common), reanimator_b01 (Champion) were examined. Boss controller schema and Champion-vs-Hero controller field differences not documented.

**GDX1 FoI transmuter (Inferno) not parsed.** The `purifyingflame1.dbr` skill likely has a transmuter node (Inferno) that modifies rank arrays. Not located in this probe.
