# MIGRATION — GD display-name → `.dbr` record bridge (first GD monster extraction)

**Author:** elrond (data steward) · **Date:** 2026-07-26 · **DB:** `agentic_orchestration/research/curated/corpus.db`
**Commissioner:** gandalf · **Method source:** legolas probe `legolas/notes/2026-07-26-gd-displayname-bridge.md`
**Schema-meta version:** `gd-displayname-bridge-2026-07-26` (`/M1` `/M2` `/M3` `/M4`)
**Class:** ADDITIVE. Five new tables, four new views, one single-row `UPDATE`. ZERO overwrites of banked rows.
**Fidelity grade:** **DATAMINED** — era-substrate LAW §4 (`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md`)
**Sibling ledgers:** `MIGRATION-gd-slice-exact-fields-2026-07-24.md` · `MIGRATION-gd-edition-pin-2026-07-24.md` ·
`MIGRATION-devotion-payloads-2026-07-25.md` · `MIGRATION-fixtures.md` (the fixtures-side half, M4)

---

## 0. What this closes

`fixture_set.monster_record` was NULL on every row, including the certified ones, because nothing
in the corpus mapped a GD nameplate string to a `.dbr` path. Two hops were missing and both are
now banked:

```
nameplate "Walking Dead"
  → gd_display_tag        : tagEnemyZombieA01 = 'Walking Dead'        [.arc localization]
  → gd_monster_record     : description == 'tagEnemyZombieA01'         [.arz, 25 records]
  → v_gd_monster_bridge   : the 25-way fan-out, nothing collapsed
  → gd_monster_bio        : characterLife = ((charLevel*4)^1.33)+24    [the actual statline]
```

This is a **first extraction**, not a re-extraction. Before this migration `corpus.db` held
**zero** GD monster rows of any kind and **zero** `.arc`-derived rows of any kind.

---

## 1. Provenance and edition pin

Eight source files, all sha256-verified **before a byte was parsed**; a mismatch HALTs the lane.

| Source | sha256 | Verified |
|---|---|---|
| `resources/Text_EN.arc` | `613457c8df72fe5a16de88def05dd00f518cf4e61c14cf375ef2ccab6dbd6e01` | ✅ |
| `gdx1/resources/Text_EN.arc` | `85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a` | ✅ |
| `gdx2/resources/Text_EN.arc` | `8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1` | ✅ |
| `gdx3/resources/Text_EN.arc` | `d6e7f7810ab251e3ad9e0dcf87e22d0af8f7d1611c02e1be4d431c44fd0d1f18` | ✅ |
| `database/database.arz` | `8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f` | ✅ |
| `gdx1/database/GDX1.arz` | `e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539` | ✅ |
| `gdx2/database/GDX2.arz` | `f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985` | ✅ |
| `gdx3/database/GDX3.arz` | `1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0` | ✅ |

Tree: `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`, read-only, edition `gd-edition-II-20260724`.

**Two pin FORMS, and the difference is deliberate.** `.arz` rows carry the established composite
(`edition; depot=N(name); manifest=…; arz_sha256=…`) because the freeze §4 table attests
depot↔manifest for the database depots. `.arc` rows carry
`edition; arc=<rel-path>; arc_sha256=…; depot=NOT-ATTESTED-FOR-ARC-LANE` — because **nothing in the
freeze record attests which depot ships `resources/Text_EN.arc`.** Writing a guessed depot into a
provenance column would be worse than a shorter pin. The sha256 is self-verifying against the
frozen bytes with zero dependency on any external table, so the shorter pin still passes the
steward test ("exactly which bytes produced this row, two years from now?").

**Owed:** if a future run establishes the `.arc` depot mapping, the `NOT-ATTESTED` literal is the
grep target for backfill.

---

## 2. M1 — `gd_display_tag` (the localization table)

**Script:** `research/scripts/gd_bridge_m1_display_tags_2026_07_26.py`
**Reader:** `research/scripts/gd_arc_reader_2026_07_26.py` (new; ARC v3 container, ~120 lines)

`ARC` v3 is a different container from `.arz` but the same LZ4-block payload codec, so no new
dependency. Format per probe §1, productionized.

### Rows: 20,490 across 11 domains

| domain | resolved | shadowed | | domain | resolved | shadowed |
|---|---:|---:|---|---|---:|---:|
| creature | 2,060 | 0 | | achievement | 483 | 0 |
| item | 7,344 | 6 | | tutorial | 324 | 0 |
| skill | 3,621 | 28 | | endlessdungeon | 184 | 0 |
| storyelement | 2,790 | 3 | | console | 117 | 0 |
| ui | 2,651 | 143 | | mutator | 54 | 0 |
| uimain | 681 | 1 | | | | |

### FINDING 1 — the probe's zero-collision claim is TRUE but domain-scoped

Probe §1: *"Key-collision census across the four archives: ZERO … the merge is a plain
`dict.update()` union — no override/precedence semantics need to be modelled."*

**Reproduced exactly for the creature domain: 0 collisions across 2,060 keys.** The bridge's own
merge model is therefore a plain union, as claimed, and that claim is load-bearing and confirmed.

**It does not generalise.** 180 cross-archive collisions exist in other domains:
item 6 · skill 28 · storyelement 2 · ui 143 · uimain 1. Most are placeholder fills — base ships
`''`, `'?'`, or a literal slot name for content that shipped later
(`tagSkillClassName07` base `'?'` → gdx1 `'Inquisitor'`; `tagFactionUser9` base `'User9'` → gdx1
`'Coven of Ugdenbog'`). But **real rewordings exist**:

```
tagDecreaseMasteryError   base 'Cannot reclaim points from the mastery.'
                          gdx1 'You cannot reset a mastery selection.'
tagCraftTabArtifactA      base 'Relics'  →  gdx2 'Relics and Runes'
```

**Consequence for the schema (elrond seam call).** Because real overrides exist, the table does
NOT collapse on merge. Every source row is banked with its `expansion`; precedence
(base < gdx1 < gdx2 < gdx3) is carried as the derived columns `expansion_rank` / `is_resolved` /
`shadowed_by`. The raw fan-out survives and the resolved lookup is a view over it
(`v_gd_display_tag_resolved`). **Discarding shadowed rows would have destroyed the only evidence
that an override is real rather than a placeholder** — the placeholder/substantive distinction is
only visible because both values are present.

### FINDING 2 — my own first cut was too narrow, and M2 caught it

The first M1 banked only `creature` + `skill`. M2 then reported **193 Monster `description` tags
resolving to nothing**. Cause: **GD does not keep monster nameplate strings in one file.**

| tag | display string | actually lives in |
|---|---|---|
| `tagNPC_Direni` | Direni | `tags_storyelements.txt` |
| `tagNPC_Guard_Female01` | Guardian | `tags_storyelements.txt` |
| `tagBreakableDermapteranA01` | Dermapteran Cluster | `tags_items.txt` |
| (86 more) | — | `tagsgdx{2,3}_endlessdungeon.txt` |

Two-domain slicing was **my imposition on the data, not a property of it**. M1 was re-run banking
every `tags*.txt` in the four archives, with `tag_domain` derived from the FILE rather than
asserted by the adapter. An unmapped filename HALTs rather than dropping silently. Resolution went
**3,862 → 4,023 of 4,066**.

### Naming (deviation from the commission's literal wording, declared)

The commission asked for a table named `monster_display_tag`. The bytes are not monster-specific:
`tags_creatures.txt` also carries the 18 racial-profile nouns and their plurals, and ten further
domains sit alongside. A table so named holding race nouns, item names and UI strings would be a
name that hides what the data is. **Base table `gd_display_tag` with an explicit `tag_domain`
column** (tagged, not encoded — Discipline #14 spirit); **`monster_display_tag` exists as a VIEW**
over the resolved creature slice, so the commissioned name is a real, queryable surface.

### Authored-blank values

70 resolved rows carry an empty display string across 9 non-creature domains — e.g.
`tagEnemySkillD16=` ships literally blank in base `tags_skills.txt`. **Banked verbatim**; coercing
them to NULL would be a silent transformation. The creature domain has **zero** empties, which is
separately HALT-gated: an empty nameplate string would break the bridge.

### Out of scope, declared

`survivalmode{1,2,3}/` and `mods/survivalmode/` text archives (no creature tags; the mod overlay
changes the merge model per probe §7). Non-EN locales. ARC v3 `crc` validation (read, not checked).

---

## 3. M2 — `gd_monster_record` / `gd_monster_field` / `gd_monster_bio`

**Script:** `research/scripts/gd_bridge_m2_monster_records_2026_07_26.py` (reuses `ArzArchive`
from `gd_arz_adapter_2026_07_24.py` verbatim — no new `.arz` parsing work)

### Census — reproduces probe §2

| archive | records | Monster | probe oracle | w/desc | tag-prefixed | w/bio |
|---|---:|---:|---:|---:|---:|---:|
| `database.arz` | 34,114 | 1,307 | 1,307 | 1,305 | 1,302 | 1,293 |
| `GDX1.arz` | 18,447 | 737 | 737 | 734 | 734 | 736 |
| `GDX2.arz` | 16,451 | 1,064 | 1,064 | 1,063 | 1,063 | 1,064 |
| `GDX3.arz` | 24,178 | 958 | 958 | 953 | 953 | 957 |
| **total** | | **4,066** | **4,066** | **4,055** | **4,052** | **4,050** |

### FINDING 3 — the 4,052-vs-4,055 gap is a PREDICATE difference, not a data difference

Probe §2's column reads "with `tag…` description" — descriptions that **start with** `tag`. The
broader predicate "description is non-empty" gives 4,055. The three-record gap:

```
records/sandbox/boss_deino_35.dbr       description='xtagMonsterGraeae1'
records/sandbox/boss_enyo_35.dbr        description='xtagMonsterGraeae2'
records/sandbox/boss_pemphredo_36.dbr   description='xtagMonsterGraeae3'
```

The `x`-prefix is GD's authoring convention for a **disabled** tag. Both counts are correct under
their own predicate. **Both are now asserted in the gate** — banking one number while asserting
the other would have made a correct extraction look like a parse bug forever.

### Scope choice: FULL bestiary

All **4,066** Monster records, not the 4,052 tag-resolvable subset the commission offered as a
defensible minimum. The whole pass runs in under a minute, so the smaller scope buys nothing; and
the records that carry no tag are exactly the rows a future coverage question will ask about.
Excluding them would make their absence indistinguishable from an extraction failure.
`display_name_status` names the three states: `resolved` (4,023) / `tag-unresolved` (32) /
`no-tag` (11).

### Table shapes

**`gd_monster_record`** — 4,066 rows, PK `(record_path, source_file)`. Identity and the join
columns: `description_tag`, `display_name`, `display_name_status`, **`display_name_tag_domain`**
(which tag file supplied the nameplate — a fact worth keeping, per FINDING 2),
`racial_profile` / `racial_tag` / `race_display`, `monster_classification`, `factions_record`,
`controller_record`, **`bio_record`**, `char_level_expr`, `level_min`, `level_max`,
`experience_points`, plus the pin/grade/adapter provenance block.

**`gd_monster_field`** — 202,120 rows over 82 distinct raw fields, PK
`(record_path, source_file, raw_field)`. Long-form statline surface for the curated families
(`character*`, `defensive*`, `offensive*`, `skillLevel*`, plus level bounds / XP / anger).
Carries `raw_field` + `raw_value` **alongside** `canon_key` + `is_core` — the two-column
tagged-not-encoded convention `exact_skill_field` established. 83,034 rows carry a `canon_key`.

*Rows are banked where the field is PRESENT, including zeros.* "`characterLife` is present and
`0.0` on 3,875 of 3,895 records" is not noise — it is the load-bearing evidence that the statline
does not live on the Monster record. Compressing zeros away would have deleted the finding.

**`gd_monster_bio`** — 6,627 rows over 733 distinct bio records, PK
`(bio_record, source_file, raw_field)`. **This is where the statline actually is.** GD stores
monster attributes as formula strings over `charLevel`:

```
records/creatures/enemies/bios/bio_zombie_01.dbr
    characterLife = ((charLevel*4)^1.33)+24     characterMana = ((charLevel*8)^1.22)+100
    characterStrength = (charLevel*4.5)+10      characterDexterity = (charLevel*6.5)+10
    characterOffensiveAbility = (charLevel*6)+5 characterDefensiveAbility = (charLevel*3)+25
```

Zero referenced bio records were missing from the archives.

### Why NOT `monster_numeric`

`monster_numeric` is the cross-game **community-harvest** surface: `source_url` and `source_date`
are `NOT NULL` and every row runs the `normalization_rule` / `rdr_value` pipeline. A `.arz`
datamine has neither a URL nor a normalized value, and inventing one would be **fabricated
provenance**. GD's primary-source monster data therefore lands in its own `gd_monster_*` tables —
exactly the precedent `exact_skill` set against `kit_numeric`. `canon_key` deliberately reuses
`monster_numeric`'s existing vocabulary (`life`, `fire_resist_pct`, `accuracy`, `defense`,
`experience`, …) so a future normalization lap can promote these rows without re-deriving the map.

One mapping is worth flagging: **`defensiveLife` → `vitality_resist_pct`.** GD names *vitality*
damage "Life" internally. The raw field name is preserved so the rename is inspectable and
reversible.

### FINDING 4 — source defects, recorded so nobody rediscovers them

| What | Count | Disposition |
|---|---:|---|
| `description` tags resolving to nothing in ANY tag file | 32 | GD authoring debris (3 `xtag`-disabled; the rest dangling: `tagAnomalyA01`, `tagEnemyHarpyB02`, `tagMonsterName190`). Banked `tag-unresolved`. |
| Monster records with no `description` at all | 11 | Portals, door sequences, ritual shells, test dummies. Banked `no-tag`. |
| `characterRacialProfile` outside the `Race0NN` taxonomy | 20 | Free-form nouns (`Reanimated`, `Magical`, `Anomaly`, `Undead`) — content authored outside the taxonomy, not a broken join. **Includes one genuine GD typo: `Race10` on `chthonic_cultistportal.dbr`; the taxonomy key is `Race010`.** |

The race gate HALTs only on a **well-formed** `Race\d{3}` that fails to resolve (0 observed) —
halting on free-form nouns would be gating on my assumption about how GD authors data.

---

## 4. M3 — the bridge (`gd_monster_tiebreak` + three views)

**Script:** `research/scripts/gd_bridge_m3_bridge_and_fixtures_2026_07_26.py`

`tag → record` is one-to-many. The temptation is to pick one and store a scalar. **This schema
refuses that, in three layers:**

1. **`v_gd_monster_bridge`** — the RAW fan-out. One row per (display_name, candidate record).
   Nothing dropped. `candidate_count` and `distinct_bio_count` are on **every** row.
2. **`gd_monster_tiebreak`** (4,066 rows) — the heuristic as its **own table**, keyed to the
   record and sitting *beside* the facts rather than inside them. It can be re-scored without
   touching anything factual, and `rule_version` says which rule produced a score.
3. **`v_gd_monster_bridge_preferred`** (1,940 rows) — one row per display name carrying the
   tiebreak winner **alongside** `candidate_count`, `distinct_bio_count`, `modal_bio_record` and
   `modal_bio_support`. A consumer reading only this view still cannot fail to see the ambiguity.

Plus **`v_gd_monster_bio_modal`** — the bio mode per display name, as its own named fact.

### Tiebreak rule `path-structure-v1` (visibly a heuristic)

Penalties are additive over **path structure only** — nothing is inferred from the statline,
because the probe established the candidates are statline-identical in every header field.
Authoring-tree location is the one signal a nameplate screenshot cannot arbitrate but a curator can:

```
records/sandbox/ +100 · /special/ +90 · /boss&quest/ +80 · /npcs/ +70
stem suffix _summon|_starter|_doa +40 · 'dropper' in stem +40
ties break on (dir_depth, stem_len, path) — a function, not a coin flip
```

`tiebreak_rank = 1` is **never** a claim about which record a world spawn instantiated. That is
decided by `Levels.arc` / `Level Art.arc` spawn tables, which are not parsed. Declared open.

### FAN-OUT STATISTICS (the headline)

| | names | share |
|---|---:|---:|
| display names with exactly ONE candidate | 985 | 50.8 % |
| display names that FAN OUT (>1) | 955 | 49.2 % |
| **of those, all candidates share ONE bio** | **818** | **85.7 % of fan-outs** |

```
fan-out histogram (candidates → names)
1:985  2:559  3:173  4:88  5:44  6:39  7:13  8:10  9:3  10:5  11:3  12:3
13:4  14:2  15:1  16:2  20:2  25:1  26:1  28:1  32:1
```

Worst: `Obsidian Anomaly` 32 · `Beronath, Corruptor of Asterkarn` 28 · `Drudd Blackheart` 26 ·
`Walking Dead` 25 · `"Associate" of Riggs` 20.

**The mitigation is stronger than the problem.** Half the bestiary's display names are ambiguous
at record level, but 86 % of those ambiguities are **statline-unambiguous** — every candidate
resolves to the same bio. For the question the bridge exists to answer (*what statline should this
fixture exhibit?*) the fan-out mostly does not bite.

### Tier-1 anchor — the fixture case, both scopes

| | probe scope (`database.arz`) | edition-wide |
|---|---:|---:|
| `tagEnemyZombieA01` candidates | **17** ✅ (probe §4: 17) | **25** (17 base + 6 gdx1 + 2 gdx2) |
| resolving to `bio_zombie_01.dbr` | **15** ✅ (probe §4: "15 of the 17") | **23** |
| tiebreak winner | `records/creatures/enemies/zombie_a01.dbr` ✅ | same |

**Legolas's numbers reproduce exactly at his stated scope.** Both scopes are asserted in the gate:
asserting only one would either fail a correct probe or hide a scope difference behind a matching
number.

---

## 5. M4 — `exact_skill.name_provenance` PENDING retired

**Script:** `research/scripts/gd_bridge_m4_retire_name_pending_2026_07_26.py` · DATA-ONLY, one row.

`gd-slice-exact-fields-2026-07-24 §G4` flagged the authoritative `.arc` tag-bridge for Flames of
Ignaffar as PENDING. M1 banked it: `tagGDX1Class07SkillName04A = 'Flames of Ignaffar'` —
**identical** to the `skillBitmapName` workaround's output. The workaround is therefore
**vindicated, not superseded.**

`display_name` is **NOT** touched (identical value; rewriting it would create a spurious edit in
the audit trail). `name_provenance` **IS** rewritten, because it currently asserts something
false. A provenance column that lies about its own state is worse than a blunt one. The gate HALTs
if the authoritative tag disagrees with the workaround — that would be a real discrepancy needing
a ruling, not a silent overwrite.

---

## 6. Verification summary

| Gate | Result |
|---|---|
| G1 edition pin — 8/8 source files sha256-verified pre-parse | ✅ |
| G2 creature-domain tag-key collisions = 0 (the bridge's merge claim) | ✅ |
| G2b per-domain collision counts vs regression oracle | ✅ |
| G3 tier-1 tag anchors (`tagEnemyZombieA01`, `tagRace005`, `tagGDX1Class07SkillName04A`) | ✅ |
| G4 zero empty resolved creature strings; 70 authored-blank elsewhere vs oracle | ✅ |
| G2 `.arz` census vs probe §2 (both tag predicates + bio) | ✅ |
| G3 `zombie_a01.dbr` header + `bio_zombie_01.dbr` formulas byte-match probe | ✅ |
| G4 resolution coverage + race-lane classification vs oracles | ✅ |
| G5 bridge fan-out statistics | ✅ |
| G6 fixture-case anchor, both scopes | ✅ |
| `PRAGMA integrity_check` / `foreign_key_check` after every milestone | ✅ / clean |

Every gate is a HALT, not a warning. Regression oracles are constants in the scripts so a source
change is **noticed** rather than absorbed.

---

## 7. Reversibility

1. **Re-run.** All four scripts are idempotent (`DELETE … WHERE schema_version = …` then re-land).
   Run order: M1 → M2 → M3 → M4. M2 reads M1's *banked* rows, not a re-parse, so M2 verifies M1's
   product rather than an independent copy.
2. **Backups**, pre-write, per milestone (elrond backup discipline, Discipline #8/#11):

| Milestone | Backup | md5 |
|---|---|---|
| M1 | `corpus.db.pre-bridge-m1-20260726T143526Z-backup` | `c112df4d34dfd087b2e8e313c78f4860` |
| M2 | `corpus.db.pre-bridge-m2-20260726T143653Z-backup` | `c199e19a9d1bbebe24afe38ef2acb3d3` |
| M3 | `corpus.db.pre-bridge-m3-*-backup` (pre-run copy) | — |
| M4 | `corpus.db.pre-bridge-m4-20260726T144218Z-backup` | `7387ade4de979d23ca9021c875e60869` |
| fixtures v0.2 | `fixtures.db.pre-v0.2-20260726T144128Z-backup` | `c062bf4a0ecc6747ac6ded847c784fda` |

3. **Drop.** All five tables and four views are additive and isolated; dropping them removes the
   bridge with no effect on any pre-existing table. The only non-additive write in the whole lane
   is M4's single-row `name_provenance` update, whose exact inverse is the prior string recorded
   in `MIGRATION-gd-slice-exact-fields-2026-07-24 §G4`.
4. `VACUUM` run post-M4; `integrity_check` ok.

---

## 8. Coverage-boundary declaration (Discipline D-a)

**INSPECTED — and this is the complete population:**
- All 4 `Text_EN.arc` (base + gdx1/2/3), every `tags*.txt` entry in each. 20,490 rows banked.
- All 4 `.arz`, every `rtype == 'Monster'` record. 4,066 banked, none excluded.
- Every bio record referenced by any Monster record. 733 resolved, 0 missing.

**NOT INSPECTED / OUT OF SCOPE — declared so a clean result here does not imply completeness:**
- **`Levels.arc` / `Level Art.arc` spawn tables.** The bridge cannot say which record a world
  spawn instantiates. Bio identity is the substitute; probe §4 judged the Levels lane not worth
  opening yet, and this migration does not open it.
- **Applied-modifier chain.** `characterLife` on the bio is the BASE. `damage_totaladjuster` /
  `armorbase01` passives at `skillLevel = charLevel*1` and difficulty-tier globals stack on top and
  are **not traced**. A statline prediction is not scoreable against a fixture until they are.
- **Non-`Monster` record types** (items, levels, controllers, factions) — the `factions_record` and
  `controller_record` columns are pointers only; the targets are not banked.
- **Non-EN locales**, `survivalmode*`, `mods/`, and ARC v3 `crc` validation.
- The 40 non-FoI GD `canon_corpus` kits' community-source rows are untouched by this lane.

---

## 9. Boundary note (ADR-004)

Change to elrond's own data layer (`corpus.db`, `fixtures.db`) only. **No engine telemetry schema,
no engine source, no ADR-004 cross-seam request.** The vendor tree is read-only vendor data and
nothing was written to it. Both `.db` files are gitignored — the committed artifacts are this
note, the five scripts, the fixtures ledger entry, and the `corpus_schema_meta` records inside the
regenerable DB. Auto-committed per project discipline (Matt-authorized). **NO push.**
