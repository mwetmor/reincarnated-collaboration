# G-7 — Grim Dawn `.gdc` save findings — "Fresh Character 01" — 2026-07-28

**Mode:** A (analytical / primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf · **Authority:** R-KC1-4 + charter §14.2, `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md`
**Work package:** KIT-CAL-1 **G-7**
**Access mode:** read-only throughout. The only writes were this note and `legolas/scratch/2026-07-28-gdc-parse-g7/`.

**Companion:** `agentic_orchestration/legolas/notes/2026-07-28-gd-gdc-save-probe.md` (STEP-1 lane map; this note is STEP 2).

**Session note.** The parse ran in a prior session that died on a stream timeout before writing
findings. The parse artifacts survived complete on disk. This session **consumed the artifacts,
did not re-derive the format**, and added the one piece the dead session never reached: the
**`.arc` tag → English display-name bridge** (§3), plus the `.arz` identification of `werewolf1b`
(§5) and the level-arithmetic reconciliation (§6).

---

## Headline

- **Fixture identity PROVEN.** `playTime` 7096 s vs the run's ≈7094 s (**2 s drift**), `deaths` 2
  (exact telemetry match), SHA-256 matches the share copy. The end-of-run state is intact and
  un-played-past.
- **All four of Matt's attested item names match CHARACTER-FOR-CHARACTER (4/4 EXACT).** The
  `.arc` bridge resolves the measured record paths to exactly the strings Matt read off screen.
- **`werewolf1b` = "Blight of Ch'thon"** — a `Skill_Transmuter`, `skillMaxLevel 1`, a discrete
  point-purchasable node in the Berserker skill tree (`_classtree_class10.dbr` `skillName23`). It
  converts **100 % Pierce → Chaos** and swaps the werewolf mesh. Rank 1 is a **real hard skill
  point**. This **CONTRADICTS** attested claim §14.1(4) "werewolf line unallocated".
- **Level is 13, not 12** — proven twice independently by `.arz` arithmetic (§6), not merely
  asserted by a field.
- **Devotion conjunctive test PASSES**; **potions 0/0 MEASURED**.
- **`uid` is 16 zero bytes** → the `save_identity` join key artifact-verification §505 asked for
  **does not exist in this save**. Fall back to SHA-256. See §9.

---

## 1 — Fixture identity proof

| # | Datum | Value | Grade | Source |
|---|---|---|---|---|
| 1.1 | File | `player.gdc`, 15,473 bytes | MEASURED | `parsed.json` `file_size` |
| 1.2 | SHA-256 | `0be3a99f6ead980210a5c06cd12a09bfe51235c09b9da7d41745fa4eacd5ee91` | MEASURED | `shasum -a 256 player.gdc.scratch` — matches charter §14.2 |
| 1.3 | Character name | `Fresh Character 01` | MEASURED | header @ `0xc` |
| 1.4 | Class tag | `tagSkillClassName10` → **Berserker** | MEASURED | header; `.arc` bridge |
| 1.5 | Sex / hardcore | male (`sex=1`) / `hardcore=0` | MEASURED | header |
| 1.6 | `playTime` | **7096 s** (run's ≈7094 → **2 s drift**) | MEASURED | `play_stats` @ `0x3ad1` |
| 1.7 | `deaths` | **2** — exact match to run telemetry | MEASURED | `play_stats` @ `0x3ad5` |
| 1.8 | `kills` | 882 · `championKills` 7 · `heroKills` 3 | MEASURED | `play_stats` |
| 1.9 | `hitsInflicted` / `hitsReceived` | 1606 / 500 | MEASURED | `play_stats` |
| 1.10 | `criticalHitsInflicted` / `…Received` | 66 / **0** | MEASURED | `play_stats` |
| 1.11 | `greatestDamageInflicted` / `…Received` | 1093.807 / 260.498 | MEASURED | `play_stats` |
| 1.12 | `difficulty` / `greatestDifficulty` | 128 / 0 (Normal) | MEASURED | `character_info` |
| 1.13 | File version / block versions | file v8; `inventory` v11, `character_stash` v11, `character_skills` v8, `ui_settings` v7, `play_stats` v12 | MEASURED | `parsed.json` `notes` |

**Verdict — identity: CONFIRMED.** 2 s of `playTime` and an exact `deaths` match are not
coincidence; this is the play-test-v1 end state, untouched.

**Parse-completeness caveat (carried, not hidden).** One block failed and was resynced:
`ui_settings` (`string length 4294967295 implausible at 0x34dd`); the parser skipped 1,392 bytes
and re-found the next block sentinel cleanly. `ui_settings` holds hotbar layout only — **no field
this note reports comes from it**. Every other block parsed to completion with 0 trailing bytes.

---

## 2 — ATTESTED → MEASURED: the five claims

Charter §14.1 banked five claims *before* instruments returned, precisely so testimony would be
confronted rather than inherited. Result: **3 clean, 1 contradicted, 1 partial.**

| # | ATTESTED (charter §14.1) | MEASURED | Verdict | Grade |
|---|---|---|---|---|
| **A1** | **Devotion = 0** | `devotionPointsUnspent` **3** == `totalDevotionUnlocked` **3**; `devotionReclamationPointsUsed` **0**; **all 62** skill entries `devotionLevel = 0` | ✅ **CONFIRMED** — conjunctive three-part test PASSES. 3 devotion points earned, **0 ever assigned**, none refunded. The assigned-then-refunded loophole is closed. Corroborated: `play_stats.shrinesRestored` = **3** = points earned. | MEASURED |
| **A2** | **Onslaught pressed-but-inert** | `onslaught1` rank **13** (of `skillMaxLevel` 16), `enabled=1`. `werewolf1.activeSkillSet=1`; `werewolf1`'s two `grantedSkills` carry `enabled=0` at save time | ✅ **CONSISTENT** — the rank was real and substantial (13), which is exactly why the inertness mattered. Second-source support for G-4's skillSet partition: the transform declares its own `activeSkillSet`. | MEASURED |
| **A3** | **Gear: 4 items, all green (rare); major = weapon + amulet, minor = armor + belt** | **All four names EXACT** (§3). Rarity structure: weapon + amulet bases are `itemClassification = Rare`; armor + belt bases are `Common` carrying **Rare-class suffixes** | ⚠️ **PARTIAL — names 4/4 EXACT, rarity claim imprecise.** Matt's own "major vs minor" split maps **exactly** onto the measured base-rarity-vs-affix-rarity distinction — the intuition was right, the label "all green" was not. See §3.3. | MEASURED |
| **A4** | **Werewolf line unallocated (werewolf2/3/1b = 0)** | `werewolf1b` = **rank 1** | 🚨 **CONTRADICTED — LOUD.** `werewolf1b` is "Blight of Ch'thon", a point-purchasable transmuter (§5). `werewolf2` and `werewolf3` **are** absent (measured-absent). | MEASURED |
| **A5** | **Potions used = 0** | `healthPotionsUsed` **0**, `manaPotionsUsed` **0** | ✅ **CONFIRMED** | MEASURED |
| **A6** | *(level, attested in passing)* **level 12** | `character_bio.level` **13**, corroborated by two independent `.arz` arithmetic checks (§6) | 🚨 **CONTRADICTED — LOUD.** Level is **13**. `play_stats.maxLevel` reads 12 and is the field that lags. | MEASURED |

> **Reconciliation already on record.** Charter §14.5 banks Matt's verbatim response to A4 and
> A6: *"I did level to 13, you're right… I did level the two werewolf nodes."* Both contradictions
> are **resolved in the measurement's favour**. This note is the underlying evidence, filed so
> the ruling has a source.

---

## 3 — Equipped-gear ledger (the `.arz` join keys + English names)

**Method.** Record paths came from the `.gdc` inventory block; `itemNameTag` / `lootRandomizerName`
/ `itemStyleTag` from the `.arz` corpus; English from **four `Text_EN.arc` files merged with
expansion-override precedence** (20,245 tags). GD composes a display name as
`prefix + [styleTag] + baseTag + suffix`.

### 3.1 — Full equipped set (12 slots; 10 filled + 2 weapon)

| Slot | **English display name** | Base record (`.arz` join key) | Prefix record | Suffix record | Base class / ilvl |
|---|---|---|---|---|---|
| 0 head | Sheltering Salvaged Helmet of the Dranghoul | `records/items/gearhead/a03_head002.dbr` | `…/prefix/ad003a_res_cold_01.dbr` | `…/suffix/b_ar014_arje.dbr` | Common / 12 |
| 1 amulet | **Menacing Putrid Necklace of Protection** | `records/items/gearaccessories/necklaces/b001_necklace.dbr` | `…/prefix/b_ar022_ar.dbr` | `…/suffix/a019b_ch_da_02.dbr` | **Rare** / 8 (req 8) |
| 2 torso | **Mystic Salvaged Armor of Menhir's Wall** | `records/items/geartorso/a02_torso002.dbr` | `…/prefix/aa006a_spimod_01.dbr` | `…/suffix/b_ar002_ar.dbr` | Common / 9 |
| 3 legs | Glacial Patchwork Leggings of the Fox | `records/items/gearlegs/a02_legs01.dbr` | `…/prefix/b_ar030_ar.dbr` | `…/suffix/a005b_ch_att_cunspi_02.dbr` | Common / 9 |
| 4 feet | Vigorous Reinforced Greaves | `records/items/gearfeet/a02_feet02.dbr` | `…/prefix/aa007a_lifemod_01.dbr` | — | Common / 9 |
| 5 hands | Stalwart Hide Gloves of Frostbite | `records/items/gearhands/a02_hands01.dbr` | `…/prefix/aa010a_damod_01.dbr` | `…/suffix/a029e_off_dmg%cold_01_ar.dbr` | Common / 7 |
| 6 ring1 | Vampiric Silver Band | `records/items/gearaccessories/rings/a001_ring02.dbr` | `…/prefix/ao008a_lifeleech_01.dbr` | — | Common / 8 |
| 7 ring2 | Silver Band of Prowess | `records/items/gearaccessories/rings/a001_ring02.dbr` | — | `…/suffix/a001a_ch_att_cun_02.dbr` | Common / 8 |
| 8 waist | **Mystic Woven Cord of Soulwarding** | `records/items/gearaccessories/waist/a02_waist001.dbr` | `…/prefix/aa006b_spimod_01.dbr` | `…/suffix/b_ar103_ar_a.dbr` **(GDX1)** | Common / 8 |
| 9 shoulders | Magestorm Fur-lined Mantle of Frostbite | `records/items/gearshoulders/a03_shoulder01.dbr` | `…/prefix/b_ar104_ar_a.dbr` **(GDX1)** | `…/suffix/a029e_off_dmg%cold_01_ar.dbr` | Common / — |
| 10 medal | *(empty)* | — | — | — | — |
| 11 relic | *(empty)* | — | — | — | — |
| **w1-0 weapon** | **Poisoned Pusquill's Tail of Corrosion** | `records/items/gearweapons/blunt1h/b015b_blunt.dbr` | `…/prefix/ao006b_poison_02.dbr` | `…/suffix/a032c_off_dmg%acid_01_we.dbr` | **Rare** |
| **w1-1 off-hand** | Bernard's Slightly-Chewed Buckler of Protection | `records/items/gearweapons/shields/b013a_shield.dbr` | — | `…/suffix/a019a_ch_da_01.dbr` | **Rare** |
| w2-0/1 swap | *(empty; `weaponSwapEnabled = 0`)* | — | — | — | — |

All rows **MEASURED**. No component (`componentName`) or augment (`augmentName`) on any slot —
the fixture is **un-componented**, which simplifies any stat reconstruction. Additional carried
items: 8 in the inventory sack, 13 in the single stash tab (not enumerated; out of G-7 scope).

### 3.2 — Name-match verdict against Matt's four attested names

| Attested (charter §14.1) | Measured | Verdict |
|---|---|---|
| Weapon — *Poisoned Pusquill's Tail of Corrosion* | `Poisoned` + `Pusquill's Tail` + `of Corrosion` | ✅ **EXACT** |
| Amulet — *Menacing Putrid Necklace of Protection* | `Menacing` + `Putrid Necklace` + `of Protection` | ✅ **EXACT** |
| Armor — *Mystic Salvaged Armor of Menhir's Wall* | `Mystic` + `Salvaged` + `Armor` + `of Menhir's Wall` | ✅ **EXACT** |
| Belt — *Mystic Woven Cord of Soulwarding* | `Mystic` + `Woven Cord` + `of Soulwarding` | ✅ **EXACT** |

**4/4 exact, character-for-character.** Every constituent tag resolved from a single, unambiguous
`.arc` (no expansion override collisions — verified per-arc):

| Tag | Resolves in | Value |
|---|---|---|
| `tagWeaponBluntB015` | `resources/Text_EN.arc` | `Pusquill's Tail` |
| `tagShieldB014` | `resources/Text_EN.arc` | `Bernard's Slightly-Chewed Buckler` |
| `tagStyle018` | `resources/Text_EN.arc` | `Salvaged` |
| `tagTorsoA005H` | `resources/Text_EN.arc` | `Armor` |
| `tagGDX1SuffixB103_Ar_A` | `gdx1/resources/Text_EN.arc` | `of Soulwarding` |

This is a **hard test of the whole chain** — `.gdc` byte offsets → record path → `.arz` name tag
→ `.arc` string. Four independent end-to-end hits against strings Matt read off a screen two days
earlier. **The `.gdc` parse lane is verified, not merely plausible.**

### 3.3 — Where the "all green (rare)" sub-claim goes imprecise

| Attested item | Base `itemClassification` | Rare-class affix present? | What it actually is |
|---|---|---|---|
| Weapon | **Rare** | prefix Magical, suffix Magical | Rare **base** (monster-infrequent tier) |
| Amulet | **Rare** | prefix `b_ar022_ar` **Rare** | Rare **base** + rare prefix |
| Armor | Common | suffix `b_ar002_ar` **Rare** | Common base + **rare affix** |
| Belt | Common | suffix `b_ar103_ar_a` **Rare** (GDX1) | Common base + **rare affix** |

**DERIVED reading (flagged as inference, not measurement):** Matt's "two **major** items (weapon,
amulet) and two **minor** items (armor, belt)" partitions the set *exactly* along the
base-rarity boundary. The perception was structurally correct; only the word "green" over-reached.
This is testimony holding up better than its own vocabulary.

**Also measured:** the **shield is equipped and its base is Rare too** — a fifth rare-touched item.
Consistent with charter §11.2's finding that the shield was worn long before level 12, and
therefore not part of the level-12 acquisition event Matt was describing. No contradiction; a
scope clarification.

---

## 4 — Skill-rank ledger

`character_skills` v8 holds **62** entries. 8 are engine defaults, 45 are GDX3 potion-modifier
stubs. The build is these 8 rows:

| Record (`.arz` join key) | **English** | Rank | `enabled` | `skillMaxLevel` | `Class` | Point-consuming? |
|---|---|---|---|---|---|---|
| `records/skills/playerclass10/_classtraining_class10.dbr` | **Berserker** (mastery bar) | **5** | 1 | 50 | `Skill_Mastery` | **YES — 5** |
| `records/skills/playerclass10/amatokpact1.dbr` | **Amatok's Pact** † | **1** | 1 | — | `Skill_BuffRadiusToggled` | **YES — 1** |
| `records/skills/playerclass10/onslaught1.dbr` | **Onslaught** | **13** | 1 | 16 | `Skill_WeaponPool_BasicAttack` | **YES — 13** |
| `records/skills/playerclass10/werewolf1.dbr` | **Werewolf** | **16** *(hard max)* | 1 | 16 | `Skill_Shapeshift` | **YES — 16** |
| `records/skills/playerclass10/werewolf1b.dbr` | **Blight of Ch'thon** | **1** | 1 | 1 | `Skill_Transmuter` | **YES — 1** |
| `records/skills/playerclass10/werewolf1_skill01_claws.dbr` | **Feral Claws** | **16** | **0** | 16 | `Skill_AttackWeapon` | **NO — granted** |
| `records/skills/playerclass10/werewolf1_skill02_charge.dbr` | **Rip and Tear** | **16** | **0** | 16 | `Skill_AttackPathCharge` | **NO — granted** |
| `records/skills/playerclass10/passive02.dbr` | **Battle Surge** | **1** | 1 | 12 | `Skill_PassiveOnCritBuffSelf` | **YES — 1** |

All ranks **MEASURED**. † `amatokpact1.dbr` carries no `skillDisplayName` of its own; the name
lives on its buff child `amatokpact1_buff.dbr` → `tagGDX3Class10SkillName06A` → **"Amatok's Pact"**
(DERIVED via the documented `buffSkillName` link — a one-hop resolution, not a guess).

**Measured-absent (the spec's sensitivities):** `werewolf2`, `werewolf3`, `onslaught1b`,
`onslaught2`, `onslaught3`, `passive01`, `passive03`, `passive04`, `rallyingcry*`, `wereraven*`,
`leap*`, `bloodborne1`, `heartofastekarn1`, `windsofasterkarn*`, `bonechillingcry1`,
`amatokpact2/3`. **`werewolf2` (bleed + leech) is confirmed unallocated** — the largest G-4 §7.3
sensitivity stays closed.

### 4.1 — Are the saved ranks BASE hard points?

**Verdict: YES. The saved `level` is the hard-allocated rank; no `+skills` inflation exists in
this fixture.** Three independent lines:

| # | Test | Result | Grade |
|---|---|---|---|
| 4.1a | Scan every equipped base/prefix/suffix record for `augmentAllLevel`, `augmentMasteryLevel*`, `augmentSkillLevel*` targeting `playerclass10` | **Zero hits.** The only `+skill` grants present are `augmentSkillLevel1/2` targeting `playerclass03` (Blood of Dreeg), `playerclass04`, `playerclass05`, `playerclass08` — **none of which this Berserker has**. No `augmentAllLevel` on any equipped item. | MEASURED |
| 4.1b | `character_skills.itemSkills` list length | **0** — no item-granted skills at all | MEASURED |
| 4.1c | Point-budget arithmetic (below) | Closes to within 1 point of the level-derived budget, with `skillPointsUnspent = 0` | DERIVED |

**Budget arithmetic.** `records/creatures/pc/playerlevels.dbr` (base `database.arz`) gives
`skillModifierPoints = [3, 3, 3, … ]` (3/level for levels 1–49) and `initialSkillPoints = 0`.
Level 13 ⇒ **12 level-ups × 3 = 36** skill points from levelling.

```
5 (mastery bar) + 1 (Amatok's Pact) + 13 (Onslaught) + 16 (Werewolf)
                + 1 (Blight of Ch'thon) + 1 (Battle Surge)          = 37 hard points
```

37 allocated, `skillPointsUnspent = 0`, 36 from levels ⇒ **1 point from quest reward(s)** (GD
grants skill points as quest rewards; the specific quest is not recoverable from the save).
**Grade: DERIVED.** The residual is +1 and the direction is correct — quest points can only add.

**Why Feral Claws / Rip and Tear at 16 are NOT purchases.** `werewolf1.dbr` declares
`grantedSkills = [werewolf1_skill01_claws.dbr, werewolf1_skill02_charge.dbr]` — MEASURED from
`GDX3.arz`. Their ranks **mirror** `werewolf1`'s 16. Counting them as purchases would put the
build at **69** points against a 36–37 budget — arithmetically impossible. Their `enabled = 0`
records that the character was **not transformed at save time**, which is second-source
confirmation of the G-4 skillSet partition (`werewolf1.activeSkillSet = 1`).

**Detail worth carrying:** at rank 13, `onslaught1.skillComboChargeLevel[13] = **5**` (the array
saturates at 5 from rank 9 onward). Onslaught was at full combo-charge capacity all run —
and inert inside werewolf form regardless.

---

## 5 — `werewolf1b` identified

**`records/skills/playerclass10/werewolf1b.dbr` — source `gdx3/database/GDX3.arz`.**

| Field | Value | Grade |
|---|---|---|
| `recordType` / `Class` | `Skill_Transmuter` | MEASURED |
| `skillDisplayName` | `tagGDX3Class10SkillName01D` → **"Blight of Ch'thon"** | MEASURED |
| `skillMaxLevel` / `skillUltimateLevel` | **1 / 1** (single-point node, no ultimate ranks) | MEASURED |
| `skillTier` / `skillMasteryLevelRequired` | 2 / 0 | MEASURED |
| `conversionInType` → `conversionOutType` | **Pierce → Chaos** | MEASURED |
| `conversionPercentage` | **100.0** | MEASURED |
| `shapeshiftMeshOverrideMale` | `creatures/pc/werewolf/hero_werewolf01b.msh` | MEASURED |
| Every offensive / defensive / retaliation field | **0.0 across the board** | MEASURED |
| `skillBaseDescription` | *"The corrupted blood of Ch'thon has taken hold within you, twisting your transformation into a ravenous abomination bent on destruction."* | MEASURED |
| Tree membership | `_classtree_class10.dbr` `skillName23` — sits directly beside `werewolf1` (`skillName22`) | MEASURED |

**What the 1 point buys.** Exactly one mechanic and one cosmetic:

1. **100 % of the character's Pierce damage is converted to Chaos damage.** Nothing else — every
   other stat field on the record is zero. It is a *pure damage-type conversion transmuter*.
2. A **different werewolf mesh** (`hero_werewolf01b`, the "blighted" variant).

**Ruling on the contradiction.** `werewolf1b` is a discrete, player-allocatable transmuter node,
not an auto-grant: it is a distinct `_classtree_class10` entry, `Skill_Transmuter` is GD's
one-point exclusive-modifier class, and it is **not** listed in `werewolf1.grantedSkills` (which
names only claws and charge). Rank 1 therefore **is** a spent skill point, and attested claim
§14.1(4) is **contradicted**. Matt has since reconciled (charter §14.5).

**Downstream consequence — the kit spec must carry this.** A 100 % Pierce→Chaos conversion is not
cosmetic to a damage model. Any B-signature or sim reconstruction of this fixture that models the
werewolf's Pierce component as Pierce is **wrong**; it resolved as Chaos for the entire run.
Whether the werewolf's attacks carry a Pierce component at all is a `werewolf1` / `claws` /
`charge` rank-array question **not answered here** (see §10, U-1).

---

## 6 — The level discrepancy, resolved

| Field | Value |
|---|---|
| `header.level` | **13** |
| `character_bio.level` | **13** |
| `character_bio.experience` | **23,710** |
| `play_stats.maxLevel` | **12** |
| Matt attested | 12 |

**The format does explain it, and the `.arz` settles it independently — twice.**

**Check 1 — experience threshold.** `playerlevels.dbr` gives
`experienceLevelEquation = (((((L*L*L)^1.16)*32)+((L*L)*300))*0.1)+36`, read as the cumulative XP
threshold to *be* level L+1:

| L | threshold | vs `experience` 23,710 |
|---|---|---|
| 11 | 17,130.7 | above → at least level 12 |
| **12** | **22,582.4** | **above → at least level 13** |
| **13** | **29,186.9** | **below → not yet level 14** |

⇒ **exactly level 13.** (The alternative "per-level increment" reading is falsified: it puts
cumulative-to-13 at 107,493, five-fold off.) Grade: **DERIVED**, from a MEASURED equation.

**Check 2 — attribute arithmetic (fully independent of XP).** `playerlevels.dbr`:
`characterModifierPoints = 1`/level, `strengthIncrement = dexterityIncrement =
intelligenceIncrement = 8`, `lifeIncrement = 20`, `lifeIncrementDexterity = 8`,
`manaIncrement = 16`. `malepc01.dbr` base = **50 / 50 / 50**, life 250, energy 250.

```
physique 122 = 50 + 9×8   ->  9 points
cunning   74 = 50 + 3×8   ->  3 points
spirit    50 = 50 + 0×8   ->  0 points
                             ----------
                             12 attribute points, attributePointsUnspent = 0
```
12 points × 1/level ⇒ **exactly 12 level-ups ⇒ level 13.**

And the derived pools close to the byte:
`health = 250 + 9×20 (physique) + 3×8 (lifeIncrementDexterity) = 250 + 180 + 24 = **454**` —
the save reads **454.0**. `energy = 250 + 0×16 = **250**` — the save reads **250.0**. Both exact.

**Conclusion.** `character_bio.level = 13` is authoritative. **`play_stats.maxLevel` lags by one**
— it is a statistics-block counter updated on a different cadence than the bio block's live
level, and the ding to 13 was not resynced into it before the save was written. Matt's attested
"12" matches the lagging field and the player's own last-seen HUD; the true end-state level is
**13**. Grade: **MEASURED** (level) + **DERIVED** (the lag explanation — the format does not
self-document `maxLevel`'s write trigger).

### 6.1 — `greatestMonsterKilledName`

| Datum | Value | Grade |
|---|---|---|
| Tag | `tagSlithBossB02` → **"Primordian, the Forgotten One"** | MEASURED (`resources/Text_EN.arc`) |
| `.arz` record | `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` (`recordType = Monster`) | MEASURED (`database/database.arz`) |
| `monsterClassification` | **Quest** | MEASURED |
| `charLevel` formula | `charLevel*1+3` | MEASURED |
| Level at kill | **13** | MEASURED (`play_stats.perDifficulty[0]`) |
| `lifeAndMana` at kill | **15,822** | MEASURED |
| `lastMonsterHit` | `tagEnemyZombieSoldierA01` → **"Rotting Soldier"** | MEASURED |
| `lastMonsterHitBy` | `tagEnemyZombieG01` → **"Plague Walker"** | MEASURED |
| `lastHit` / `lastHitBy` (damage) | 312.888 / 273.704 | MEASURED |

The record carries `characterLife = 0.0` (pool is level-scaled at spawn, not stored), so **15,822
is the only source of this boss's actual pool** — it is an observed value, and a usable
opposition anchor for G-5a. Difficulty slots 1 and 2 are empty (Normal only).

---

## 7 — Attributes and pools

| Field | Value | Grade |
|---|---|---|
| physique | **122.0** (base 50 + 9 points) | MEASURED |
| cunning | **74.0** (base 50 + 3 points) | MEASURED |
| spirit | **50.0** (base 50 + 0 points) | MEASURED |
| health (base pool) | **454.0** | MEASURED |
| energy (base pool) | **250.0** | MEASURED |
| `attributePointsUnspent` | 0 | MEASURED |
| `skillPointsUnspent` | 0 | MEASURED |
| `money` | 7,860 | MEASURED |
| `masteriesAllowed` | 2 (only one taken) | MEASURED |
| `skillReclamationPointsUsed` | 0 | MEASURED |
| `devotionReclamationPointsUsed` | 0 | MEASURED |
| lore notes collected | 3 (`loreobject_lowercrossinga02`, `creedsjournala01`, `creedsjournala02`) | MEASURED |

> **⚠️ Analytical note — INFERENCE, explicitly NOT measurement.** The charter's telemetry records
> a max-HP step **759 → 1600 (2.11×)** at the R2/R3 boundary. The save's `health` **454** is the
> **base, pre-modifier attribute pool** — a *different layer* from in-game max HP. Do **not** read
> 454-vs-1600 as a contradiction. As a shape check only: 454 → 759 is 1.67× (plausible from gear
> + 5 points of Berserker mastery), and 759 → 1600 is 2.11× (the shape a shapeshift transform
> produces). This is **consistent with**, and mildly corroborative of, the charter's reading that
> the step is the Werewolf toggle. It is **not** evidence — closing it requires reading
> `werewolf1`'s `characterLife*` rank arrays from `GDX3.arz`, which G-7 did not do (§10, U-1).

---

## 8 — Class + provenance summary

| Fact | Value | Grade |
|---|---|---|
| Mastery | `playerclass10` = **Berserker** (GDX3 / *Fangs of Asterkarn*) | MEASURED |
| Second mastery | none (`masteriesAllowed = 2`, one used) — **pure single-class fixture** | MEASURED |
| Skills source archive | `gdx3/database/GDX3.arz` (all 8 build skills) | MEASURED |
| Skill text source | `gdx3/resources/Text_EN.arc` | MEASURED |
| Gear bases + most affixes | `database/database.arz` + `resources/Text_EN.arc` | MEASURED |
| Two affixes | `gdx1/database/GDX1.arz` + `gdx1/resources/Text_EN.arc` (belt suffix `b_ar103_ar_a`, shoulder prefix `b_ar104_ar_a`) | MEASURED |

**Lane requirement for anyone reproducing this join:** you need **base + GDX1 + GDX3** for both
`.arz` and `.arc`. A base-game-only corpus resolves neither the belt suffix nor any skill name.

---

## 9 — `uid` is all zeros — the `save_identity` finding

| Datum | Value |
|---|---|
| Offset | `0x5a` |
| Raw | `00000000000000000000000000000000` (16 zero bytes) |
| Grade | **MEASURED** |

The STEP-1 lane map (`2026-07-28-gd-gdc-save-probe.md` §170, §281) designated `uid` as the
`save_identity` join key that artifact-verification **§505** flagged as missing from
`(save_identity, play_time_ms)`. **That key does not exist in this save.** The field is present,
correctly located, and null.

**Interpretation (DERIVED).** A zeroed `uid` is consistent with a save created in the console-
enabled `save\user\` slot (charter §14.4 C-5). Whether GD populates `uid` at all in that path, or
whether it is written only under Steam-cloud/`save\main\`, is **not determinable from one save** —
it needs a second save from `save\main\` to compare. Until then, treat zero-`uid` as a **property
of this acquisition path**, not a proven property of the format.

**Recommendation to elrond / gandalf.** `fixture_session.save_identity` must fall back to the
**SHA-256 of `player.gdc`**:

```
save_identity = sha256:0be3a99f6ead980210a5c06cd12a09bfe51235c09b9da7d41745fa4eacd5ee91
```

Carry the substitution as an explicit provenance caveat on every row it keys, because the two
have **different semantics**: `uid` is stable across play sessions (it identifies the *character*);
the SHA identifies *one byte-state* and changes on every save. For the `(save_identity,
play_time_ms)` continuity key this is **adequate for v1** — the fixture is a single frozen
artifact — but it will **not** stitch two sittings of the same character together. If play-test
v2 produces a multi-sitting fixture, this key breaks and needs the character name + a session
ordinal instead. Flagging now, cheaply, rather than at v2 ingest.

---

## 10 — Unresolved

| # | Item | Status | What would close it |
|---|---|---|---|
| **U-1** | **`werewolf1` / `claws` / `charge` rank-array values at rank 16** — damage types (incl. whether a Pierce component exists for Blight of Ch'thon to convert), `characterLife` modifiers, weapon-damage %, cadence | **UNRESOLVED — and the highest-value follow-on.** G-7 measured *ranks*; it did not extract the *values those ranks select*. Blocks both the Pierce→Chaos consequence (§5) and the max-HP-step hypothesis (§7). | One `GDX3.arz` pass over the three records, indexing rank arrays at 16. Cheap — the reader exists (`scratch/arz_index.py`). |
| **U-2** | `play_stats.v` list: `[{werewolf1.dbr: 1}, {werewolf1_skill02_charge.dbr: 7}]` | **UNRESOLVED — semantics unknown.** Recorded verbatim. Plausibly a most-used-skill or skill-unlock-notification tracker; the numbers 1 and 7 fit neither obviously. **Not interpreted.** | Community format reference for `play_stats` v12, or a second save to diff. |
| **U-3** | The **+1 skill point** above the level-derived budget (§4.1) | DERIVED as quest reward; the specific quest is **not recoverable** from the save | Not worth closing. |
| **U-4** | `ui_settings` block (hotbar layout) | **UNPARSED** — string-length field read as `0xFFFFFFFF`; 1,392 bytes skipped, resync clean | v7 struct reference. No G-7 field depends on it. |
| **U-5** | Sack (8 items) and stash (13 items) contents | **NOT EXTRACTED** — out of G-7 scope (equipped set only) | Same resolver, wider input. Parsed offsets already exist in `parsed.json`. |
| **U-6** | Whether zero-`uid` is a `save\user\` property or a format-wide property | **UNRESOLVED** (§9) | A second `.gdc` from `save\main\`. |
| **U-7** | Base-game rarity *display colour* rules (green vs yellow) | **NOT ASSERTED.** §3.3 reports `itemClassification` from the `.arz` — the data field — and deliberately does **not** claim what colour GD renders | GD UI colour-mapping source. Deliberately left open rather than guessed. |

---

## 11 — Artifacts

`agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/` (committed; save copy and
`__pycache__` excluded — the save's canonical home is the share):

| File | Role |
|---|---|
| `gdc_parse.py` | `.gdc` block parser (prior session) |
| `parsed.json` | full block-level parse output |
| `resolve_gear.py` / `gear_resolved.json` | gear record paths → `.arz` name tags (prior session) |
| `arc_text.py` | **`.arc` v3 reader + tag loader** — first `.arc` bridge in a legolas note |
| **`name_resolve.py`** | **NEW (this session)** — tag → English join for gear, skills, monsters |
| **`gear_named.json` / `skills_named.json`** | **NEW** — resolved display-name ledgers |
| **`arz_index.py`** | **NEW** — `.arz` record-name enumerator + full field dumper (the shipped adapter exposes `read_record` only; enumeration was needed to find `playerlevels.dbr`, `_classtree_class10.dbr`, and the Primordian record) |
| `explore.py`, `trace.py`, `solve_*.py` | prior-session block solvers |

**Source corpus (read-only):** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` —
`database/database.arz`, `gdx1/database/GDX1.arz`, `gdx3/database/GDX3.arz`,
`resources/Text_EN.arc`, `gdx1/resources/Text_EN.arc`, `gdx3/resources/Text_EN.arc`.
**Save (read-only, mode 444):** `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_Fresh Character 01/player.gdc`.

---

**Signed:** legolas (UNKNOWN-RESEARCHER), 2026-07-28.
