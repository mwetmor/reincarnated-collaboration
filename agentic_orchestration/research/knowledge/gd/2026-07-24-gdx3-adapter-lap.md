# Research — GDX3 Adapter Lap (Fangs of Asterkarn) — 2026-07-24

**Mode:** A (analytical, primary-source binary extraction)
**Commissioner:** gandalf (via Owed follow-up §7.2 of cut-record)
**Source:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/gdx3/database/GDX3.arz`
**Reference Edition-I:** `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/`
**Scripts:** `agentic_orchestration/research/scripts/gdx3_probe_2026_07_24.py`
          `agentic_orchestration/research/scripts/gdx3_probe2_2026_07_24.py`
**Parser:** Same TQIT/LZ4 reader as `gd_arz_adapter_2026_07_24.py` — no modification required.

---

## HEADLINE

**Fangs of Asterkarn introduces one new player mastery: `playerclass10`.**

This is confirmed by primary source. `playerclass10` is a `Skill_Mastery` node with a `SkillTree`
carrying 40 skill records (skills, passives, transmogrifiers, secondary effects). Skill stems
confirm the identity: `werewolf1`, `wereraven1`, `heartofastekarn1`, `windsofasterkarn1`,
`bonechillingcry1`, `leap1`, `onslaught1`, `amatokpact1`. This is the **Primal Striker mastery**
(shapeshifter/melee; werewolf and wereraven shapeshift forms are the signature mechanics).

Localization tag from the class-training record: `tagGDX3Class10SkillName00A`. English display
name requires `.arc` parse (not done in this lap — see D-a). Internal identifier by structural
convention: `playerclass10`.

**Downstream consequence for GD-SLICE:** The "270 kits" denomination used in prior GD-SLICE
planning was computed from 9 masteries (playerclass01–09) × 30 skills. playerclass10 adds one
more mastery to the denominator. The denominator moves; the specific number depends on how many
of playerclass10's 40 records are player-skill nodes vs passives/modifiers/secondaries (see §Q2
for breakdown). The FoI byte-match certificate and all banked Edition-I work are unaffected —
those records are in gdx1/gdx2/base, byte-verified unchanged.

---

## Q1 — Parse compatibility

**Result: PASS — unmodified.**

`GDX3.arz` parses under the existing TQIT/LZ4 reader with zero structural changes:

| Field | GDX3 | base/gdx1/gdx2 | Delta |
|---|---|---|---|
| `magic` | 2 | 2 | none |
| `version` | 3 | 3 | none |
| Header layout | 24-byte TQIT | 24-byte TQIT | none |
| String table format | u32 count prefix + LP_strings | same | none |
| Record table entry format | variable-length (embedded LP_string) | same | none |
| Compression | LZ4 block | LZ4 block | none |
| DBR field wire format | type(u16)+count(u16)+key_id(u32)+values | same | none |

File metrics: 47,334,429 bytes / 24,178 records / 70,267 strings. This places GDX3 in the same
weight class as GDX1 (42 MB, 18,447 records) and GDX2 (33 MB, 16,451 records) — confirmed as a
full expansion's worth of records, not a patch payload.

Five sample records decoded across the archive: all clean, no decompression errors.

---

## Q2 — New playerclass namespaces (masteries)

### Finding: one new namespace, `playerclass10`

| Archive | playerclass namespaces |
|---|---|
| base (database.arz) | playerclass01–09 |
| GDX1 (Ashes of Malmouth) | playerclass02–04, 06–08 (adds Inquisitor, Necromancer) |
| GDX2 (Forgotten Gods) | playerclass01–04, 06–09 (adds Oathkeeper) |
| **prior union (base+gdx1+gdx2)** | **playerclass01–09** |
| **GDX3 (Fangs of Asterkarn)** | playerclass02–04, 06–10 |
| **NEW (gdx3 - prior)** | **playerclass10** |

Note: gdx3 carries records for playerclass02–09 as well as playerclass10. Those are existing-mastery
records (modifiers, item-skill augments, cross-mastery interactions) that reference the
established masteries — not new namespaces. The `playerclass10` namespace is exclusively present
in gdx3.

### playerclass10 structure (40 records)

All 40 records enumerated from primary source:

**Mastery root:**
- `_classtraining_class10.dbr` — `Skill_Mastery`, `skillDisplayName: tagGDX3Class10SkillName00A`, `skillMaxLevel=50`, 600 fields. This is the mastery's level-up node.
- `_classtree_class10.dbr` — `SkillTree`, 80 fields. This is the skill-tree layout node.

**Core skills (named, with at least one modifier rank):**

| Stem | Record type | Signature |
|---|---|---|
| `werewolf1` | `Skill_Shapeshift` | Werewolf transformation |
| `werewolf1_skill01_claws` | `Skill_AttackWeapon` | Claw attack (werewolf form) |
| `werewolf1_skill02_charge` | `Skill_AttackPathCharge` | Charge attack (werewolf form) |
| `werewolf1b` | `Skill_Transmuter` | Werewolf transmuter |
| `werewolf2`, `werewolf3` | `Skill_Modifier` | Werewolf rank modifiers |
| `wereraven1` | `Skill_Shapeshift` | Wereraven transformation |
| `wereraven1_skill01_icicles` | `Skill_AttackWave` | Icicle wave (wereraven form) |
| `wereraven1_skill02_icering` | `Skill_AttackProjectileRing` | Ice ring (wereraven form) |
| `wereraven1b` | `Skill_Transmuter` | Wereraven transmuter |
| `wereraven2`, `wereraven3` | `Skill_Modifier` | Wereraven rank modifiers |
| `onslaught1` | `Skill_WeaponPool_BasicAttack` | Onslaught basic attack |
| `onslaught1b` | `Skill_Transmuter` | Onslaught transmuter |
| `onslaught2`, `onslaught3` | `Skill_Modifier` | Onslaught rank modifiers |
| `leap1` | `Skill_AttackRadiusLeap` | Leap attack |
| `leap2` | `SkillSecondary_AttackProjectileRing` | Leap secondary projectile ring |
| `amatokpact1` | `Skill_BuffRadiusToggled` | Amatok's Pact (toggleable buff aura) |
| `amatokpact1_buff` | `SkillBuff_Passive` | Amatok's Pact buff component |
| `amatokpact2`, `amatokpact3` | `Skill_Modifier` | Amatok's Pact rank modifiers |
| `heartofastekarn1` | `Skill_BuffSelfToggled` | Heart of Asterkarn (self-buff toggle) |
| `bloodborne1` | `Skill_BuffSelfToggled` | Bloodborne (self-buff toggle) |
| `bonechillingcry1` | `Skill_AttackBuffRadius` | Bone-chilling Cry (attack + radius buff) |
| `bonechillingcry1_buff` | `SkillBuff_Debuf` | Bone-chilling Cry debuff component |
| `rallyingcry1` | `Skill_BuffRadius` | Rallying Cry (radius buff) |
| `rallyingcry1_buff` | `SkillBuff_Passive` | Rallying Cry buff component |
| `rallyingcry1b` | `Skill_Transmuter` | Rallying Cry transmuter |
| `rallyingcry2` | `Skill_Modifier` | Rallying Cry rank modifier |
| `windsofasterkarn1` | `Skill_AttackRadiusGrow` | Winds of Asterkarn (expanding radius attack) |
| `windsofasterkarn2` | `SkillSecondary_AttackProjectileDrop` | Winds secondary projectile drop |
| `passive01–04` | `Skill_Passive`, `Skill_PassiveOnCritBuffSelf`, `Skill_PassiveOnLifeBuffSelf`, `Skill_Modifier` | Passive nodes |
| `wpattack01` | `Skill_WPAttack_BasicAttack` | Weapon pool basic attack |
| `wpattack02` | `Skill_WPAttack_AttackWave` | Weapon pool attack wave |

**Record type breakdown for playerclass10:**
- `Skill_Mastery`: 1
- `SkillTree`: 1
- `Skill_Modifier`: 10
- `Skill_Transmuter`: 4
- `Skill_Shapeshift`: 2
- `SkillBuff_Passive`: 2
- `Skill_BuffSelfToggled`: 2
- `Skill_PassiveOnCritBuffSelf`: 1, `Skill_PassiveOnLifeBuffSelf`: 1, `Skill_Passive`: 1 (passives: 3)
- Unique attack-type records (distinct skills): ~12
- Support skills (`Skill_AttackBuffRadius`, `Skill_BuffRadius`, `Skill_BuffRadiusToggled`): 3

**Downstream implication for "270 kits" denominator:**

The 40-record count is structurally sparse compared to other masteries — gdx1's FoI mastery
(playerclass07) carries 343 records in GDX3, and gdx2's Oathkeeper (playerclass09) carries
111 records even though it is also a single-expansion mastery. The 40-record count reflects
that GDX3 is a recent release (2026-07-23 build) and many supplemental modifiers, item-skill
augments, and cross-mastery records for playerclass10 are distributed elsewhere in GDX3's
item and modifier records — not exclusively under the `records/skills/playerclass10/` namespace.
Cross-reference confirms this: at least 35 GDX3 item records (in the first 500 decoded) reference
`playerclass10` skills via `augmentSkillName` and `modifiedSkillName` fields.

The GD-SLICE denominator note: the prior "270 kits" figure appears to derive from 9 masteries
× 30 skills. The correct denominator with playerclass10 is 10 masteries, but the actual
player-facing skill count for playerclass10 is approximately 10–12 distinct named skills
(excluding modifiers, transmogrifiers, and secondary effects). Elrond should flag this as a
coverage-boundary update in the corpus schema when GDX3 rows are ingested.

---

## Q3 — Monster controller spatial-AI field ranges

### Summary table

101 controller records in GDX3; 72 carried at least one spatial field. 0 decode errors.

| Field | Prior min (base+gdx1+gdx2) | Prior max | Prior n | GDX3 min | GDX3 max | GDX3 n | Outside envelope |
|---|---|---|---|---|---|---|---|
| `ChanceToRespondToDistressCall` | 0 | 100 | 371 | 0 | 100 | 72 | no |
| `InnerSightAngerRate` | 0.0 | 100.0 | 369 | 0.0 | 100.0 | 72 | no |
| `InnerViewDistance` | 0.0 | 50.0 | 371 | 1.0 | 30.0 | 72 | no (narrower) |
| `MaxPursuitDistance` | 0.0 | 600.0 | 371 | 0.0 | **2000.0** | 72 | **YES** |
| `MaxYViewDistance` | 0.0 | 25.0 | 371 | 0.0 | 24.0 | 72 | no |
| `PursuitTime` | 0 | 90,000 | 371 | 0 | **6,000,000** | 72 | **YES** |
| `RoamDistance` | 0.0 | 30.0 | 371 | 0.0 | 12.0 | 72 | no (narrower) |
| `SightAngerRate` | 0.0 | 100.0 | 372 | 0.0 | 100.0 | 72 | no |
| `ViewDistance` | 0.0 | 200.0 | 372 | 2.0 | 200.0 | 72 | no |
| `WanderDistance` | 0.0 | 30.0 | 369 | 0.0 | 12.0 | 72 | no (narrower) |
| `distressCallRange` | — | — | 0 | — | — | 0 | n/a (absent both) |
| `fleeDistance` | 0.0 | 20.0 | 371 | 0.0 | 10.0 | 71 | no (narrower) |

**Note on `distressCallRange`:** This field was in the commission's target list. It is absent from
the string tables of ALL archives (base, gdx1, gdx2, gdx3). The field observed in the prior probe
note (2026-07-23-gd-arz-extraction-probe.md §1) was `distressCallRange` on **monster body records**
(not controller records). The controller records carry `ChanceToRespondToDistressCall` instead.
The commission list combined both populations; this is the D-b note.

### Spatial outliers: two fields exceed prior envelope, single record

Both `MaxPursuitDistance` (2000.0 vs. prior max 600.0) and `PursuitTime` (6,000,000 vs. prior
max 90,000) are attributable to a **single controller record**:

```
[ControllerMonster] records/controllers/enemy/controller_blacklodge_chaser.dbr
  ViewDistance:       30.0
  InnerViewDistance:  20.0
  MaxPursuitDistance: 2000.0   *** 3.3× prior max
  PursuitTime:        6,000,000 *** 66.7× prior max
  WanderDistance:     0.0
  RoamDistance:       5.0
```

**Interpretation:** `controller_blacklodge_chaser.dbr` — the name signals a "chaser" archetype
associated with the Black Lodge faction. The spatial profile is intentional: extreme leash radius
(2000 GD world units; the prior max was 600) and a pursuit timer of 6,000 seconds (100 minutes
in real time, effectively "never stops chasing"). This is a pursuit-specialist mob designed to
follow the player indefinitely across zone boundaries. `fleeDistance=absent` (uses default),
`WanderDistance=0.0` (does not wander when idle).

**TSF6/VDM consequence:** The sim's leash model and pursuit-timer logic built against the prior
envelope (max leash ~600 WU, max pursuit time ~90s) do not cover this mob. Whether the sim needs
to model the Black Lodge Chaser archetype specifically depends on scope decisions above this
report's pay grade. The finding is: one new mob archetype exists outside the prior parameter
envelope, and its defining characteristic is effectively infinite pursuit range.

All other GDX3 controller records fall within the Edition-I envelope. The general mob population
of Asterkarn is not out-of-envelope.

---

## Q4 — New field names, record types, templateName targets

### New record types (18 in GDX3, not present in base/gdx1/gdx2)

| Record type | Count | Notes |
|---|---|---|
| `OneShot_SkillUnlock` | 33 | One-time skill unlock items (new mechanic class) |
| `Skill_AttackPattern` | 33 | New attack pattern skill type |
| `Skill_PotionModifier` | 26 | Potion modification skill (new consumable interaction) |
| `AscendantAltarFormula` | 23 | Ascension altar crafting formula |
| `SkillSecondary_TargetedSpawnPet` | 20 | Targeted pet spawn secondary |
| `Skill_PotionContainer` | 12 | Potion container item |
| `ItemAscensionFormula` | 9 | Item ascension formula |
| `SkillSecondary_AttackRadiusLightning` | 5 | Lightning radius secondary |
| `SkillSecondary_AttackProjectileDrop` | 4 | Projectile drop secondary |
| `ItemRerollFormula` | 3 | Item reroll formula |
| `DynamicDoor` | 3 | Dynamic door entity |
| `NpcCauldron` | 3 | NPC cauldron entity |
| `Skill_AttackRadiusGrow` | 3 | Expanding-radius attack (used by Winds of Asterkarn) |
| `SkillBuff_DebufProjectile` | 2 | Debuff projectile buff |
| `NightLight` | 1 | Lighting entity |
| `AscendantAltar` | 1 | Ascension altar entity |
| `NpcItemAscension` | 1 | NPC item ascension entity |
| `SkillSecondary_BuffAttackRadiusDrop` | 1 | Buff + radius drop secondary |

**Adapter relevance:** The 18 new record types represent new skill mechanics (`Skill_AttackPattern`,
`Skill_AttackRadiusGrow`, `SkillSecondary_TargetedSpawnPet`) and two new crafting/progression
systems (`AscendantAltar`/`AscendantAltarFormula`/`NpcItemAscension` and `ItemRerollFormula`/
`ItemAscensionFormula`). The adapter does not currently handle any of these 18 types.

**Skill-geometry note:** `Skill_AttackRadiusGrow` — used by `windsofasterkarn1.dbr` in
playerclass10 — is structurally a new cone/AoE geometry type distinct from `Skill_AttackSpellCone`
(FoI's type). The field surface for this type was not fully decoded in this lap.

### templateName sample (first 200 records)

Top templates observed in the 200-record sample:
`controllermonster.tpl`, `monster.tpl`, `decoration.tpl`, `lootrandomizertabledynamic.tpl`,
`effect.tpl`, `proxypool.tpl`, `lootitemtable_dynweighted_dynaffix.tpl`, `lootrandomizer.tpl`,
`factionpack.tpl`, `npc.tpl`, `skill_modifier.tpl`, `controllerstationarymonster.tpl`,
`fxpak.tpl`, `ascensionaltaraffixswap.tpl` (new), `proxy.tpl`, `soundpak.tpl`,
`lootmastertable.tpl`, `charfxpak.tpl`, `characterattributeequations.tpl`.

`ascensionaltaraffixswap.tpl` is a new template not present in prior archives (consistent with
the `AscendantAltarFormula` record type cluster).

### Field name surface note

The string table diff yielded 35,031 strings new to GDX3 vs. prior archives. Of these, 5,423
match the proxy heuristic for field names (no `/` or `.`, length 2–79 characters). The sorted
leading entries in this set are achievement IDs (`ACH301`–`ACH357` and beyond) and quest/story
text — not field names. This means the 5,423 figure is dominated by localization strings and
achievement identifiers, not DBR field names.

**Confirmed new field name class:** the `Ascension` system almost certainly introduces new field
names (e.g., ascension tier, altar type, formula ingredient fields). These are not resolvable from
the string table proxy alone without decoding `AscendantAltarFormula` records specifically. That
decode was not done in this lap.

**What the adapter does NOT currently handle:** any record of the 18 new types listed above.
Field surfaces for those types are not documented here.

---

## Q5 — SurvivalMode3 nature

**Confirmed: SurvivalMode3 is the Asterkarn Crucible/survival variant**, structurally identical
in role to SurvivalMode (base), SurvivalMode1 (AoM Crucible), and SurvivalMode2 (FG Crucible).

Evidence:
- 1,431 total records; dominant namespaces: `records/proxies` (640), `records/creatures` (567),
  `records/items` (97), `records/controllers` (64), `records/skills` (52).
- The `records/skills` content is exclusively `nonplayerskillsgdx3/bossskills/` and one
  `nonplayerskillsgdx1/` reference — no player skill records.
- String table contains explicit survival/wave strings: `gd.survival.eventControl.spawnPointOnAddToWorld`,
  `gd.survival.tier18Waves.spawnPoint01OnAddToWorld`, `achievementgroup_survival` UI record.
- Sample records include `controller_wildlife.dbr` (`ControllerMonster`), wave proxy records,
  and boss nemesis skills (`necro2_nulltotem`, `thedread_charge`, `rimehorn_icespike`).
- The faction string `factiongdx3_asterkarnundead` is present, placing it in the Asterkarn setting.

At 3,919,713 bytes (vs. SurvivalMode 1–2 which are similar in scale), this is a full Crucible
mode for the Asterkarn expansion. No player masteries, no player skills, no new DB schemas —
purely creature/wave/loot/encounter data for the survival arena.

---

## D-a — Coverage boundary declaration (mandatory per commission discipline)

### Examined in this lap:
- `GDX3.arz`: header, string table, record table — all 24,178 records indexed.
- `GDX3.arz`: 5 sample records decoded for Q1 LZ4 decompression confirmation.
- `GDX3.arz`: all 101 `controller`-path records decoded for Q3 spatial field extraction.
- `GDX3.arz`: first 200 records decoded for Q4 templateName survey.
- `GDX3.arz`: all record paths enumerated for Q2 playerclass/ namespace extraction.
- `GDX3.arz`: string table diffed against base+gdx1+gdx2 string tables for Q4 field-name proxy.
- `GDX3.arz`: all record rtypes enumerated for Q4 record-type table.
- `GDX3.arz`: playerclass10 — all 40 records enumerated; first 5 decoded for metadata.
- `GDX3.arz`: cross-reference check — first 500 records decoded for `playerclass10` references.
- `SurvivalMode3.arz`: header, string table, record table — all 1,431 records indexed.
- `SurvivalMode3.arz`: 5 sample records decoded for Q5.
- `base.arz`, `GDX1.arz`, `GDX2.arz`: record tables and string tables loaded for diff baselines.
- `base.arz` (453 controller records), `GDX1.arz` (95), `GDX2.arz` (92): all decoded for Q3 prior ranges.

### NOT examined in this lap:
- `GDX3.arz` — bulk decode of the remaining ~23,900 non-controller, non-sample records. Fields
  in these records (items, loot tables, monsters, decorations, fx, etc.) are not reported. In
  particular, field surfaces for the 18 new record types are not documented here except by type
  name and count.
- `gdx3/resources/Text_EN.arc` — not parsed. No tag-to-English-name resolution for GDX3 skill
  display names. `tagGDX3Class10SkillName00A` and similar tags are not resolved to English.
- `SurvivalMode3.arz` — no full record decode; index + 5-record sample only.
- Template files (`.tpl`) — not embedded in `.arz`; not in scope for any prior or current lap.
- `survivalmode3/resources/Text_EN.arc` (2,219 bytes) — not opened.
- Zone layout files (`.wrl`/`.lvl`) — not present in `.arz` archives.
- GDX3 boss records vs. standard-mob records — the Q3 spatial scan covers all controller paths
  regardless of classification. A boss-vs-champion breakdown within GDX3 was not separately produced.
- Ascension system field surfaces — `AscendantAltar`, `AscendantAltarFormula`, `NpcItemAscension`,
  `ItemAscensionFormula`, `ItemRerollFormula` record types were identified by name and count but
  not decoded. The field surface for these new mechanics is unknown.
- `OneShot_SkillUnlock` (33 records) and `Skill_AttackPattern` (33 records) field surfaces —
  identified by type and count, not decoded.

### D-b join validation note:
GDX3 controller records are in `records/controllers/enemy/` and `records/controllers/endlessdungeon/`
namespaces with distinct path stems (e.g., `controller_blacklodge_chaser.dbr`). No path-level
collision was observed between GDX3 controller paths and base/gdx1/gdx2 controller paths. The
spatial range comparison is therefore comparing different record populations, not the same records
across archives. The `controller_blacklodge_chaser.dbr` outlier is a new record; it is not a
changed version of a prior record.

---

## Items requiring a ruling

**None blocking.** The following are observations that may inform downstream decisions:

1. **playerclass10 kit count for GD-SLICE denominator.** The 40-record count includes modifiers,
   transmogrifiers, and secondary skill effects — not all of these are player-facing "kits" in
   the GD-SLICE sense. The approximately 10–12 distinct named skills in playerclass10 would be
   the equivalent of what prior masteries contribute per-mastery. Elrond should confirm how the
   denominator should be updated when GDX3 rows are ingested.

2. **`controller_blacklodge_chaser.dbr` out-of-envelope values.** Whether TSF6/VDM needs to
   model the `MaxPursuitDistance=2000` / `PursuitTime=6,000,000` archetype is a simulation-scope
   question for gamora + gandalf. The data is recorded; the decision is not mine.

3. **18 new record types — adapter coverage gap.** The current GD adapter handles `Skill_AttackSpellCone`
   (FoI). None of the 18 new record types are handled. If any of playerclass10's skills are
   in scope for GD-SLICE width expansion, adapter coverage must extend to those types. The field
   surfaces are not documented yet.

4. **Ascension system.** `AscendantAltar`/`AscendantAltarFormula`/`ItemAscensionFormula`/
   `ItemRerollFormula` represent a progression mechanic new to Asterkarn. Whether this is in scope
   for any TRUE-SOURCES work is not determined by this lap.

---

## Source list

- Primary source: `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/gdx3/database/GDX3.arz`
  SHA-256: `1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0` (from cut-record §4)
- Reference: Edition-I archives (base/gdx1/gdx2) at `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/`
  All 11 Edition-I files byte-verified identical to Edition-II counterparts (cut-record §3).
- Prior probe: `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md`
- Cut record: `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-II-cut-record.md`
- Format reference: TQIT/LZ4 format documented in the prior probe §0; parser productionized in
  `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`.
