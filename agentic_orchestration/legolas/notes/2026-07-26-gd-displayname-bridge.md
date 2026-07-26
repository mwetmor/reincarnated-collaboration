# Legolas Probe Note — GD Display-Name → `.dbr` Record Bridge

**Date:** 2026-07-26
**Mode:** A (analytical / primary-source probe, READ-ONLY)
**Commissioner:** gandalf
**Question:** how does an on-screen GD monster nameplate (`Walking Dead`) resolve to a `.dbr` record path, so that `fixture_set.monster_record` (currently NULL on every certified row) can be populated and joined to the `.arz` statline?
**Primary sources:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (edition-pinned tree) and `/Users/admin/Games/vendor/grim-dawn/` (Edition-I working tree). Read-only, in-memory parse; **no extraction artifacts written to disk.**

---

## §0 — Headline

The bridge is a **two-hop join**, both hops verified end-to-end on the live fixture case:

```
nameplate "Walking Dead"
  → tags_creatures.txt : tagEnemyZombieA01=Walking Dead        [.arc, localization]
  → .arz Monster record field description == 'tagEnemyZombieA01' [.arz, banked format]
  → records/creatures/enemies/zombie_a01.dbr
  → characterAttributeEquations → records/creatures/enemies/bios/bio_zombie_01.dbr  [the statline]
```

**But the reverse direction is one-to-many and that is the load-bearing risk.** `tagEnemyZombieA01` is carried by **17 distinct Monster records** in `database.arz`. Display name alone does NOT uniquely determine `monster_record`. See §4.

Commission-supplied guess `records/creatures/monsters/zombie/...` is **wrong**: GD has no `creatures/monsters/` tree. Enemies live at `records/creatures/enemies/`.

---

## §1 — WHERE the display strings live

**Archive:** `resources/Text_EN.arc` (+ one per expansion). Format is **`ARC` v3**, a container distinct from `.arz` — it must be parsed separately, but by the **same LZ4-block codec** the `.arz` probe already defeated (`2026-07-23-gd-arz-extraction-probe.md` §0.3). No new dependency.

### ARC v3 format (verified empirically this probe)

```
header (28 bytes, LE):
  magic 'ARC\0' | version u32 (=3) | numFileEntries u32 | numDataRecords u32
  | recordTableSize u32 | stringTableSize u32 | recordTableOffset u32

layout: [ compressed part blobs ] [ record table ] [ string table ] [ file entries ]
  record table entry (12 B): partOffset u32, compressedSize u32, decompressedSize u32
  string table: NUL-separated filenames
  file entry (44 B): entryType u32, fileOffset u32, compSize u32, decompSize u32,
                     crc u32, fileTime u64, numParts u32, firstPartIndex u32,
                     nameLen u32, nameOffset u32

decode: for each part, if compSize == decompSize -> stored; else lz4.block.decompress(blob, uncompressed_size=decompSize)
```

`entryType == 3` on all observed entries. Single-part files throughout the text archives.

### The archives that matter (Edition-II tree, sha256 pinned)

| Archive (rel. to `grim-dawn-edition-II-20260724/`) | sha256 (first 16) | creature tag file | creature tags |
|---|---|---|---|
| `resources/Text_EN.arc` | `613457c8df72fe5a` | `tags_creatures.txt` | 980 |
| `gdx1/resources/Text_EN.arc` | `85baef4bd2a44ead` | `tagsgdx1_creatures.txt` | 366 |
| `gdx2/resources/Text_EN.arc` | `8aec9207b5dd0b33` | `tagsgdx2_creatures.txt` | 334 |
| `gdx3/resources/Text_EN.arc` | `d6e7f7810ab251e3` | `tagsgdx3_creatures.txt` | 380 |
| `survivalmode1/…/Text_EN.arc` | `af9d87ce5cc72629` | (`tags_survival2.txt` only — no creatures) | — |
| `survivalmode3/…/Text_EN.arc` | `6336cde256871225` | (`tags_survival3.txt` only) | — |
| `survivalmode2/…/text_en.arc` | `8269f89cc6eda348` | **empty archive (0 entries)** | — |
| `mods/survivalmode/…/Text_EN.arc` | `fa0689778ef0badb` | (mod overlay; not in the vanilla lane) | — |

**Merged Edition-II creature tag table: 2,060 keys.**

**Key-collision census across the four archives: ZERO.** Tag keys are namespaced by expansion (`tagEnemy…` base / `tagGDX1…` / `tagGDX2…` / `tagGDX3…`). So the merge is a plain `dict.update()` union — **no override/precedence semantics need to be modelled.** That is a real simplification: the naive worry that gdx3 shadows base strings is refuted.

**Edition stability (checked, matters for the pin):** `resources/Text_EN.arc`, `gdx1/…`, `gdx2/…` are **byte-identical between the Edition-I tree (`grim-dawn/`) and the Edition-II tree** (sha256 match). Edition-II adds gdx3 + survivalmode3 only. Every finding below therefore holds under either pin; the recommended pin is Edition-II because it is the superset and matches the banked `gd-edition-II-20260724` corpus rows.

**Non-EN archives:** `Text_{CS,DE,ES,FR,IT,JA,KO,PL,PT,RU,VI,ZH}.arc` sit alongside. Out of scope; the nameplate evidence is English.

**Wine is still absent and still not needed.** `ArchiveTool.exe` sits at the install root but is not the path; the Python ARC v3 reader above is ~40 lines and was exercised in-memory this probe.

---

## §2 — Do our ALREADY-BANKED records carry the tag keys?

**They carry the mechanism but not the rows. A re-extract IS required — but it is a first extract, not a re-extract.**

Two separate facts:

**(a) The `.arz` monster records DO carry the tag key, in a field named `description`.** Verified directly:

```
records/creatures/enemies/zombie_a01.dbr
    description             = 'tagEnemyZombieA01'
    characterRacialProfile  = 'Race005'
    monsterClassification   = 'Common'
    factions                = 'records/controllers/factions/faction_aetherial.dbr'
    characterAttributeEquations = 'records/creatures/enemies/bios/bio_zombie_01.dbr'
```

Census across the Edition-II `.arz` set (`rtype == 'Monster'`):

| Archive | records | Monster | with `tag…` description | with bio pointer |
|---|---|---|---|---|
| `database.arz` | 34,114 | 1,307 | 1,302 | 1,293 |
| `GDX1.arz` | 18,447 | 737 | 734 | 736 |
| `GDX2.arz` | 16,451 | 1,064 | 1,063 | 1,064 |
| `GDX3.arz` | 24,178 | 958 | 953 | 957 |
| **total** | — | **4,066** | **4,052 (99.7%)** | **4,050** |

1,992 distinct description tags across 4,066 records.

**(b) `corpus.db` contains ZERO GD monster rows.** Verified:
- `exact_skill` (675 rows across `database.arz`/`GDX1`/`GDX2`/`GDX3`) — record types are **all** `Skill_*` / `SkillBuff_*` / devotion-blank. **No `Monster` record_type banked.**
- `monster_numeric` — 21 monsters total, games `d2` / `poe1` / `poe2`. **No `gd` rows at all.**
- `fixtures.db.fixture_set` — 4 rows, one certified by nameplate (`L0-gd-s3-set1`, `Walking Dead`, level 6, "Vicinity of The Coffinmakers"); `monster_record` NULL on all four.

So the bridge is **not** a join over already-banked data. It is: (1) a **new** `.arc` tag-table extraction (never done — flagged PENDING in `exact_skill.name_provenance` since the GD-SLICE migration), plus (2) a **new** `.arz` Monster-record pass (never done — the `.arz` lane has only ever banked skills and devotions). Both use tooling we already own.

**Bonus validation of hop 1 on already-banked data:** `exact_skill.name_provenance` records that FoI's display name was derived from a `skillBitmapName` workaround with the authoritative tag `tagGDX1Class07SkillName04A` "PENDING". This probe resolved it: `tagsgdx1_skills.txt` contains `tagGDX1Class07SkillName04A=Flames of Ignaffar`. The same extraction retires that caveat.

---

## §3 — "Aether Corruption": CONFIRMED as the RACE line

**It is a racial-profile string, not a skill and not a champion affix.**

`records/creatures/enemies/zombie_a01.dbr` carries `characterRacialProfile = 'Race005'`. The UI prefixes `tag`; `tags_creatures.txt` resolves it:

```
tagRace005=Aether Corruption
tagRace005P=Aether Corruptions       (plural form)
```

The full GD racial table (18 entries, base `tags_creatures.txt`, each with a `…P` plural twin):

```
Race001 Undead     Race002 Beastkin   Race003 Aetherial   Race004 Chthonic
Race005 Aether Corruption            Race006 Bloodsworn  Race007 Eldritch
Race008 Insectoid  Race009 Human      Race010 Construct   Race011 Riftspawn
Race012 Beast      Race013 Magical    Race014 Celestial   Race015 Arachnid
Race016 Plant      Race017 Guard      Race018 Bloodbound
```

The singular/plural pair is the tell: these are UI nouns for a creature-type taxonomy (used by "+X% damage to Aetherials" style affixes and by the nameplate), not skill names.

**One homonym exists and must not be confused with it.** An exhaustive scan of *every* EN tag file in the install returned exactly three occurrences of the literal `Aether Corruption`:

| Archive | file | line |
|---|---|---|
| `resources/Text_EN.arc` | `tags_creatures.txt` | `tagRace005=Aether Corruption` |
| `resources/Text_EN.arc` | `tags_creatures.txt` | `tagRace005P=Aether Corruptions` |
| `gdx1/resources/Text_EN.arc` | `tagsgdx1_skills.txt` | `tagGDX1CompSkillA105Name=Aether Corruption` |

The third is a **player-side item-component granted skill** (`GDX1CompSkill…` = Ashes of Malmouth component skill). It cannot be the third nameplate line on a hostile Walking Dead. **Ruling: the fixture's unexplained third line is the racial profile `Race005`.** The nameplate on our certified fixtures therefore reads `<display name> / <classification> / <race>` — all three lines are `.arz`-derivable, and the third line is in fact a **free disambiguation signal we were not using** (see §4).

---

## §4 — The ambiguity finding (the part that changes the plan)

"Walking Dead" → `tagEnemyZombieA01` is **unique in the string direction**: across the merged 2,060-entry Edition-II creature tag table, exactly one key yields "Walking Dead". (37 of 1,643 distinct display strings in the Edition-I merge are produced by more than one key — e.g. `Rover Protector` has two — so this uniqueness is a property of *this* name, not of the table.)

But **tag → record is one-to-many**. `tagEnemyZombieA01` is carried by **17** Monster records in `database.arz`:

```
records/creatures/enemies/zombie_a01.dbr                    <- the canonical world spawn
records/creatures/enemies/zombie_a01h.dbr                   (hero/veteran shell)
records/creatures/enemies/zombie_a02h.dbr
records/creatures/enemies/zombie_a01_doa.dbr
records/creatures/enemies/zombie_a01_starter.dbr
records/creatures/enemies/zombie_a01_summon.dbr
records/creatures/enemies/zombie_a01_potiondropper.dbr
records/creatures/enemies/zombie_soldiera01_lootdropper.dbr
records/creatures/enemies/zombieberserker_a01.dbr
records/creatures/enemies/boss&quest/waveevent_burrwitchrift_zombie_a01.dbr
records/creatures/enemies/special/rock01.dbr   rock02  rock03
records/creatures/enemies/special/rock_01b.dbr rock_02b rock_03b
records/sandbox/arthur/zombiedropper_a01.dbr
```

(The `special/rock*.dbr` entries are re-skinned shells that inherited the zombie description string — a content-authoring artifact, not a naming scheme.)

**Scale of the problem: 245 of 907 base-game description tags (27%) map to more than one Monster record.** Worst cases: `tagEnemyZombieA01` (17), `tagBossLoghorreanTentacleCluster` (12), `tagEnemyBloodswornA01` (11).

**Header fields do NOT discriminate.** All 17 share identical `monsterClassification='Common'`, `characterRacialProfile='Race005'`, `charLevel='charLevel*1'`, `minLevel=1`, `maxLevel=250`. 121 fields differ across the set, but they are cosmetic/loot/animation (`mesh`, `lootMisc*Item*`, `unarmed*Anim`, sounds) — nothing a nameplate screenshot can arbitrate.

### The mitigation — and it is a strong one

**The statline does not live on the Monster record.** `characterLife` on `zombie_a01.dbr` is `0.0`; the numbers come from the bio pointed at by `characterAttributeEquations`:

```
records/creatures/enemies/bios/bio_zombie_01.dbr
  characterLife              = ((charLevel*4)^1.33)+24
  characterMana              = ((charLevel*8)^1.22)+100
  characterStrength          = (charLevel*4.5)+10
  characterDexterity         = (charLevel*6.5)+10
  characterIntelligence      = (charLevel*6)+15
  characterOffensiveAbility  = (charLevel*6)+5
  characterDefensiveAbility  = (charLevel*3)+25
  characterLifeRegen         = (((charLevel/15+1) + lifeRegen) * (1 + lifeRegenMod/100))*elapsedTime
  characterManaRegen         = (((charLevel*2+10) + manaRegen) * (1 + manaRegenMod/100))*elapsedTime
```

**15 of the 17 candidates resolve to the SAME bio** (`bio_zombie_01.dbr`); one resolves to `bio_zombie_01_starter.dbr`, one has no bio pointer. So for the purpose gandalf actually cares about — *predicting the statline the fixture should exhibit* — the 17-way record ambiguity collapses to a **1-way bio answer with 15/17 support**.

> **[ANALYTICAL — inference, not evidence]** At the fixture's attested `charLevel = 6`, `bio_zombie_01` yields raw
> life 92.50, mana 212.49, str 37.0, dex 49.0, int 51, OA 41, DA 43. These are **pre-modifier bio values**: the
> Monster record additionally stacks `damage_totaladjuster` / `damagebase_physical01` / `armorbase01` passives at
> `skillLevel = charLevel*1`, and difficulty-tier globals apply on top. Treat as the anchor to be adjusted, not
> as a predicted in-game HP bar.

### Recommended `monster_record` disposition

Three-column, not one:

1. **`monster_record`** — populate with the **best-supported single record** (`records/creatures/enemies/zombie_a01.dbr`), chosen by a documented tiebreak rule (prefer `records/creatures/enemies/<stem>.dbr` at tree root; exclude `special/`, `sandbox/`, `boss&quest/`, `_summon`, `_starter`, `_doa`, `*dropper`).
2. **`monster_record_candidates`** (new, JSON array) — carry all 17. Never discard the ambiguity; the tiebreak is a heuristic and must be visibly so.
3. **`monster_bio_record`** (new) — `records/creatures/enemies/bios/bio_zombie_01.dbr`. **This is the column the statline prediction should actually join on**, and it is far less ambiguous than the record path.

`monster_identity_method` should gain a value such as `tag-bridge-inferred` so a bridged row is never mistaken for `spawn-command-verbatim`.

**Genuinely unresolved:** which *specific* record a given world spawn instantiates is decided by level-spawn tables that live in `Levels.arc` / `Level Art.arc`, **not** in `.arz` and **not** parsed here. If gandalf wants true 1:1 record identity (rather than 1:1 bio identity), that is a second, larger lane. My read is that bio identity is sufficient for statline prediction and the Levels lane is not worth opening yet.

---

## §5 — Extraction-procedure sketch (NOT EXECUTED)

Per DATAMINED-grade discipline. Sketch only.

**Tooling:** one new script `agentic_orchestration/research/scripts/gd_arc_text_extract_2026_07_26.py`.
Dependencies: `struct`, `lz4.block` (already installed, already used by `gd_arz_adapter_2026_07_24.py`). The existing `ArzArchive` class is reused verbatim for the `.arz` side — **no new `.arz` parsing work.**

**Step 1 — pin + checksum the source bytes.**
```
SRC=/Users/admin/Games/vendor/grim-dawn-edition-II-20260724
shasum -a 256 $SRC/resources/Text_EN.arc $SRC/gdx{1,2,3}/resources/Text_EN.arc
shasum -a 256 $SRC/database/database.arz $SRC/gdx{1,2,3}/database/GDX{1,2,3}.arz
```
Expected values are tabled in §1 and below; a mismatch HALTs the lane.

**Step 2 — extract + merge the tag tables** (ARC v3 reader per §1). Four creature files → one dict. **Assert zero key collisions** (verified 0/0/0 this probe; any nonzero means the source changed and the merge model is wrong → HALT). Also extract `tags_skills.txt` + `tagsgdx{1,2,3}_skills.txt` in the same pass — it retires the `exact_skill.name_provenance` PENDING caveat for free.

**Step 3 — pass over the four `.arz`**, `rtype == 'Monster'`, capturing per record: `record_path`, `description` (tag key), resolved `display_name`, `characterRacialProfile` → resolved race string, `monsterClassification`, `factions`, `characterAttributeEquations` (bio path), `controller`. ~4,066 rows.

**Step 4 — bank** as `gd_monster_identity` (new table) with per-row provenance: `source_file`, `record_path`, `source_version` = the Edition-II composite pin, `tag_key`, `tag_source_arc`, `tag_source_arc_sha256`, `adapter`, `schema_version`, `created_date`. Follow `MIGRATION-gd-slice-exact-fields-2026-07-24.md` shape (elrond's `canon_key`/`raw_field` two-column tagged-not-encoded convention).

**Step 5 — backfill `fixtures.db.fixture_set`** via `monster_display_name → tag_key → record`, writing all three columns from §4 and stamping `monster_identity_method`.

**Proposed edition pin string** (extends the elrond composite convention; the `.arc` bytes are now load-bearing, so they must be pinned too):
```
gd-edition-II-20260724; depot=<base>; arz_sha256=8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f;
text_en_arc_sha256=613457c8df72fe5a16de88def05dd00f518cf4e61c14cf375ef2ccab6dbd6e01
```

**Verification tiers (TSR-4 shape):**
- *Tier 1 family anchor:* `tagEnemyZombieA01 → "Walking Dead"`, `tagRace005 → "Aether Corruption"`, `tagGDX1Class07SkillName04A → "Flames of Ignaffar"` — all three verified this probe; they are the regression oracle.
- *Tier 2 in-pipe asserts:* zero tag-key collisions on merge; ≥99% of Monster records carry a `tag`-prefixed `description`; every resolved display name is non-empty; every `characterRacialProfile` resolves to a `tagRace…` entry.
- *Tier 3 spot-check:* re-derive the 17-record `tagEnemyZombieA01` fan-out and the 15/17 bio collapse.

**Cost estimate:** the full four-archive Monster pass ran in-memory during this probe in well under a minute. This is a small lane, not a crawl. **Recommended executor: `legolas-crawler`** — the method is now mapped, the schema is known, the asserts are specified.

---

## §6 — Direct answers to the four deliverables

1. **Where the strings live.** `resources/Text_EN.arc` + `gdx{1,2,3}/resources/Text_EN.arc`, in `tags*_creatures.txt`. It is an `ARC` v3 container requiring a parser — but LZ4-block, i.e. the same codec the `.arz` lane already defeated. Wine not required.
2. **Do banked records carry the tag keys?** The `.arz` records do (`description` field, 4,052/4,066 coverage). `corpus.db` does **not** — zero GD Monster rows are banked, so this is a **first extract**, not a join over existing rows. Both halves reuse tooling we own.
3. **Extraction sketch.** §5. Not executed.
4. **Confirm/refute.** "Walking Dead" → `tagEnemyZombieA01` → **`records/creatures/enemies/zombie_a01.dbr` — CONFIRMED**, with the material caveat that 16 other records share the same tag (statline collapses to one bio, 15/17). "Aether Corruption" → **`tagRace005`, the racial-profile line** (`characterRacialProfile='Race005'` on the record) — **not** a skill and **not** a champion affix on this fixture. A same-named *player* component skill (`tagGDX1CompSkillA105Name`) exists in gdx1 and is a homonym only.

---

## §7 — Gaps not resolved

- **World-spawn → specific record identity.** Requires `Levels.arc` / `Level Art.arc` spawn-table parsing; not attempted. Bio identity is the recommended substitute.
- **Applied-modifier chain.** `characterLife` bio formula is the base; `damage_totaladjuster` / `armorbase01` passives and difficulty globals stack on top and were not traced. Needed before a fixture HP prediction can be scored.
- **Non-EN tag tables.** Present, unexamined, out of scope.
- **`mods/survivalmode/…`** overlay archives exist in the Edition-II tree and were excluded; if any fixture is captured in a mod/survival context the merge model changes.
- **ARC v3 `crc` field** was read but not validated against payloads; a stricter extractor should verify it.

---

## §8 — Source list

Primary (local, read-only, this probe):
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/{resources,gdx1,gdx2,gdx3}/resources/Text_EN.arc`
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/{database,gdx1,gdx2,gdx3}/database/*.arz`
- `/Users/admin/Games/vendor/grim-dawn/` (Edition-I tree; base/gdx1/gdx2 text archives byte-identical to Edition-II)

Banked artifacts consulted:
- `agentic_orchestration/research/curated/corpus.db` (`exact_skill`, `monster_numeric`, schema)
- `agentic_orchestration/research/curated/fixtures.db` (`fixture_set`, `v_fixture_bank_certified`)
- `agentic_orchestration/research/curated/MIGRATION-gd-slice-exact-fields-2026-07-24.md`
- `agentic_orchestration/research/curated/MIGRATION-gd-edition-pin-2026-07-24.md`
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive` reused)
- `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md` (LZ4-block + TQIT lineage)
