# KIT-CAL-1 — Primordian, the Forgotten One: raw proto from the Edition-II corpus

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Run:** KC1-2026-07-27 (conductor: gandalf)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` (§14.10–§14.11 held rules honoured)
**Class:** evidentiary — measured extraction from primary source
**Mode:** read-only. No writes outside `legolas/notes/`.
**Predecessor:** `legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` (damage rows since corrected ×0.74-additive; HP composition falsified 16–19 % high)

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`) · **D** = DERIVED (arithmetic shown,
operator named) · **U** = UNRESOLVED / HELD.

---

## 0. Headline — three findings, one of which corrects the charter

1. **`tagSlithBossB02` *is* Primordian.** They are not two entities. The charter's closing line
   ("Primordian is the natural hero/boss-tier scenario candidate **alongside Slith**", §14.11 lanes
   block) reads them as distinct; the corpus does not. `tagSlithBossB02 = "Primordian, the Forgotten
   One"` is the **only** tag in the 20,394-tag `Text_EN` bridge containing that string, and exactly
   one creature record in the whole corpus carries it. **M.**
   → §14.11's "Slith cross-check: FAIL by +22 %" *was already a Primordian check.* There is one
   hero/boss scenario candidate, not two. G-5's tier roster shrinks accordingly.

2. **`charLevel = charLevel*1+3`.** Primordian is a **+3 remapper** (per the G-5a §1b class of
   quirk). Its spawn pool is `lv6_hero`, so at averagePlayerLevel *L* the creature resolves at
   **charLevel ≈ L+5 … L+6**. **M.** Consequence: if the save's
   `greatestMonsterKilledLevel = 13` is the *charLevel*, Matt was ≈ player level 7–8 at the kill —
   not 12–13. If it is the *spawn* level, the internal charLevel was **16**. The two readings give
   HP figures 33 % apart. §14.11's integrality argument assumed charLevel 13 directly; that
   assumption is now load-bearing and **should be stated, not inherited**.

3. **Primordian wears randomly-affixed gear. Its HP is not deterministic.** `chanceToEquipMisc2 =
   100.0` / `chanceToEquipMisc2Item1 = 100` → it equips a rare necklace rolled from
   `tdyn_necklace_b01_slithnecklace.dbr` **every spawn**. The base of that table,
   `b001_necklace.dbr`, carries flat **`characterLife = 220.0`**, and the reachable rare prefix pool
   includes life rolls (Matt's "Menacing" = `characterLife 80.0`, `lootRandomizerJitter 28`). **M.**
   → **`greatestMonsterKilledLifeAndMana = 15,822` carries a stochastic gear term of ≈ +300 life
   with ±22 jitter.** It is a *contaminated* instrument. §14.11's closure path ("one more
   `greatestMonsterKilledLifeAndMana` triple from ANY other GD save pins the composition rule")
   should be narrowed: **prefer a triple from a monster with no `chanceToEquip*` slots**, or the
   second measurement inherits the same noise floor and will appear to disagree with the first for
   reasons that have nothing to do with the composition operator.

---

## 1. Record identity + classification (all M)

| field | value |
|---|---|
| **record** | `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` (archive `database`) |
| difficulty variants | **none** — single record; no Epic/Ultimate override in GDX1/2/3 |
| `Class` | `Monster` |
| `templateName` | `database/templates/monster.tpl` |
| `description` | `tagSlithBossB02` → **"Primordian, the Forgotten One"** |
| `FileDescription` | `Primorian the Forgotten One` *(sic — designer typo in source)* |
| **`monsterClassification`** | **`Quest`** — not `Hero`, not `Boss`. A quest-unique. |
| `factions` | `records/controllers/factions/faction_beast.dbr` → **Beastkin** (matches Matt's read) |
| `characterRacialProfile` | `Race002` |
| `charLevel` | **`charLevel*1+3`** |
| `minLevel` / `maxLevel` | 1 / 250 |
| `characterAttributeEquations` | `records/creatures/enemies/bios/bio_boss_standard_01.dbr` |
| `controller` | `records/controllers/enemy/controller_boss_viloth.dbr` |
| `experiencePoints` | 800 |
| `characterAttackSpeed` / `RunSpeed` | 1.0 / 0.85 (pre-pak) |
| `scale` / `actorHeight` / `actorRadius` | 1.2 / 2.0 / 0.45 |
| `numAttackSlots` / `numDefenseSlots` | **8 / 8** (trash = 4) |
| `hitThreshold` / `gibThreshold` | 100 / 175 |
| `healthGainOnKillPct` / `Difficulty` | 20 / 1 |
| `distressCallGroup` / `Range` / `Time` / `max` | `Slith` / 15.0 / 5000 ms / 1 |
| `shortRangeMax` / `mediumRangeMax` / `longRangeMax` | 4.0 / 10.0 / 12.0 |
| `defaultChestPiece` | `records/items/enemygear/gear_slithwarriorb01.dbr` (**Common, itemLevel 1, no stat fields — cosmetic**) |
| `dropItems` / `giveXP` | True / True |

### Spawn chain (M)

```
records/proxies/boss&quest/proxy_wightmire_slitha01.dbr    placementExtents = 5.0, weight1 = 100, time1 = Always
  → records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr
        spawnMin = spawnMax = 3 ; proxyPoolEquation = proxypoolequation_01 (identity on Normal)
        name1 slith_wightmirecave01   alwaysSpawn1 True  limit 1  lv6_hero
        name2 slitha_melee_b01        alwaysSpawn2 True  limit 1  lv4_champion+
        name3 slitha_shaman_c01       alwaysSpawn3 True  limit 1  lv4_champion+
```

**The encounter is a fixed trio, not a solo boss.** Primordian always spawns with one champion-tier
melee slith and one champion-tier shaman slith. Any G-5 scenario that models Primordian alone
mis-states the fight.

`lv6_hero`: `min = (averagePlayerLevel+2)+(aPL/50)`, `max = (aPL+3)+(aPL/50)`.
Area cap `limit_area001`: Normal min 1 / max 200 — uncapped.

Second (non-Act-1) spawn site, **not** the fixture's: `GDX2 records/endlessdungeon/proxies/poolsboss/slith_primordian.dbr`
— identical trio, but `levelVarianceEquation1 = lv7_uber hero`. Shattered Realm only.

### charLevel resolution table (D — evaluating the M equations)

| averagePlayerLevel | spawn (lv6_hero min–max) | **charLevel** (= spawn+3) |
|---|---|---|
| 7 | 9 | **12** |
| 8 | 10 | **13** |
| 11 | 13 | **16** |
| 12 | 14–15 | **17–18** |
| 13 | 15–16 | **18–19** |

---

## 2. HP-relevant fields, RAW (M) — staged for the moment the composition rule pins

Composition is **HELD** per §14.11 (every G-5a HP figure runs 16–19 % high). Below are the inputs
only. Nothing here is a composed HP number.

**Base equations** — `bio_boss_standard_01.dbr` (M):

```
characterLife             = ((charLevel*51)^1.53)+2400
characterMana             = ((charLevel*15)^1.27)+200
characterStrength         = (charLevel*6)+50
characterDexterity        = (charLevel*8)+50
characterIntelligence     = (charLevel*8)+50
characterOffensiveAbility = (charLevel*7)+100
characterDefensiveAbility = (charLevel*6.5)+50
characterLifeRegen        = (((charLevel/15+1) + lifeRegen) * (1 + lifeRegenMod/100))*elapsedTime
characterManaRegen        = (((charLevel*3+45) + manaRegen) * (1 + manaRegenMod/100))*elapsedTime
```

**Life-modifier sources** (the only ones on this creature):

| source | rank equation | rank @ cl 13 / 17 / 18 | `characterLifeModifier` |
|---|---|---|---|
| `passive/armorbase05.dbr` (skillName3) | `charLevel*1` | 13 / 17 / 18 | **−71 / −71 / −71** (array is flat −71 through rank 19; −66 @ 20) |
| monster pak, Normal/1P | — | — | **+50** (`characterLifeModifier`), `characterLifeMultModifier` **0** |
| **equipped necklace** (see §5) | — | — | **flat `characterLife` +220 (base) + affix roll (Matt's: +80, jitter 28 %)** |

No other `skillName` on the record touches life. `primordian_passive`, `resists_heroboss`,
`damage_totaladjuster`, `boss_chest_01` carry no life fields. **M.**

**Raw base values, per candidate charLevel (D — arithmetic only):**

| charLevel | bio `characterLife` | bio `characterMana` | str | dex | int | OA-base | DA-base |
|---|---|---|---|---|---|---|---|
| 12 | 20,754.0 | 931.5 | 122 | 146 | 146 | 184 | 128 |
| **13** | **23,145.1** | **1,009.7** | 128 | 154 | 154 | 191 | 134 |
| 16 | 30,902.7 | 1,254.1 | 146 | 178 | 178 | 212 | 154 |
| **17** | **33,673.0** | **1,338.4** | 152 | 186 | 186 | 219 | 160 |
| 18 | 36,531.0 | 1,424.1 | 158 | 194 | 194 | 226 | 167 |
| 19 | 39,474.5 | 1,511.2 | 164 | 202 | 202 | 233 | 174 |

**Reconciliation against §14.11 (D, reported not adjudicated).** Under the G-5a chain
(`life × (1 + (−71+50)/100) + mana` = `life × 0.79 + mana`) I reproduce U-1's **19,294.4 at
charLevel 13 exactly** — confirming my extraction and U-1's agree field-for-field. The factor
required to hit the measured 15,822:

| charLevel | required net life factor | vs chain 0.79 |
|---|---|---|
| 11 | 0.81051 | +2.6 % |
| 12 | 0.71748 | −9.2 % |
| **13** | **0.63997** (≈ exactly **0.64 = −36.00 %**) | −19.0 % |
| 16 | 0.47141 | −40.3 % |
| 17 | 0.43012 | −45.6 % |
| 18 | 0.39413 | −50.1 % |

Two observations, both **U**, neither closed here:
- The clean **0.64** at cl 13 is why §14.11 called integrality. It remains the single tidiest fit.
- But `(1 − 0.71) × (1 + 0.50) = 0.435` — a *multiplicative* life composition — sits within **1.1 %**
  of the cl-17 requirement (0.43012), and cl 17 is exactly what the `+3` remap gives for a
  **player-level-12** kill, which is where the fixture's timeline actually puts Matt at 5453 s.
  Adding the necklace's +220 flat moves cl 11 to within 1.3 %. **Three different (charLevel,
  operator) pairs land within ~1–2 % of the same measured scalar.** One measured number cannot
  separate them. **This is the concrete reason §14.11's "one more triple closes it" is optimistic
  unless the second triple comes from a gear-free monster at a known player level.**

---

## 3. Damage rows, RAW (M) — NOT composed, per §14.10 hold

Champion/hero/boss damage regime remains **UNRESOLVED** (unmeasured clamp). The rows below are
verbatim array slices. **They must not be multiplied through any TDM/pak stage until the clamp is
resolved.** Routing column names the table each would compose through.

### 3a. Base attack — `passive/damagebase_physical04.dbr` (skillName2, rank = `charLevel*1`)

`FileDescription = "Default Phys Dmg for Heroes and Bosses"` · `unarmedOnly = True` ·
`offensivePhysicalModifier = 15.0` @ `offensivePhysicalModifierChance = 10.0` (a 10 %-of-hits
+15 % physical spike, **not** folded in) · array length 210.

| charLevel = rank | `offensivePhysicalMin` | `offensivePhysicalMax` |
|---|---|---|
| 12 | 96 | 121 |
| **13** | **101** | **128** |
| 16 | 123 | 155 |
| **17** | **130** | **165** |
| 18 | 136 | 175 |
| 19 | 144 | 183 |

Primordian carries **no** `damagebonus_physical*` and **no** weapon (`chanceToEquipRightHand = 0`,
`chanceToEquipLeftHand = 0`). **It is not a W-flag monster** — its base attack is fully
source-resolvable once the clamp lands. That makes it a *better* damage-side fixture than Warden Krieg.

### 3b. Passive cold rider — `bossskills/primordian_passive.dbr` (skillName10, rank = `charLevel/4+1`)

`Class = Skill_Passive` (so it **does** fold into the creature's own stat block), array length 60.
Also grants `defensiveTotalSpeedResistance = 500.0`, `defensiveTrap = 500.0`.

| charLevel | rank | `offensiveColdMin` | `offensiveColdMax` |
|---|---|---|---|
| 12–15 | 4 | 16 | 38 |
| 16–19 | 5 | 20 | 46 |

### 3c. TDM sources (raw, un-composed)

| source | rank eq | rank @ 13 / 17 | `offensiveTotalDamageModifier` |
|---|---|---|---|
| `passive/armorbase05.dbr` — *"For Bosses — Damage Reduced Levels 1-20"* | `charLevel*1` | 13 / 17 | **−78 / −74** |
| `passive/damage_totaladjuster.dbr` | `(charLevel/25)+2` | 2 / 2 | **+8 / +8** |
| monster pak, Normal/1P | — | — | **−25** |

Additive (the §14.10-vindicated operator): `−78 + 8 − 25 = **−95 %**` @ cl 13;
`−74 + 8 − 25 = **−91 %**` @ cl 17. **Both survive the floor but land deep in the regime §14.10
flagged as unmeasured** — a 4-point shift in the array moves output damage by ~80 %. This is
exactly the clamp sensitivity that justifies the hold. **Do not compose.**

`armorbase05` also carries `offensiveCritDamageModifier` (−15 @ r1 → 0 @ r15) and
`defensiveProtection` (armor): **76 @ cl 13, 105 @ cl 17, 106 @ cl 18** — raw, pre-pak.

### 3d. Ability rows, RAW (skillName6–9 + `specialAttack*`) — array length 60, rank = `charLevel/4+1`

These are `Skill_Attack*` / `Skill_Buff*` classes — **separately triggered, NOT folded into base
attack**. Values are the raw array slices.

| skill | Class | rank @ cl 13 / 17–18 | `offensivePhysicalMin` | `offensiveColdMin` | rider |
|---|---|---|---|---|---|
| `bossskills/primordian_wave` | `Skill_AttackWave` | 4 / 5 | 122 / 153 | **210 / 272** | `offensiveSlowColdMin` 70/91 over 3 s; `offensiveSlowDamageMultMin` 30 % over 3 s |
| `bossskills/primordian_frigidring` | `Skill_AttackProjectileRing` | 4 / 5 | 118 / 148 | **200 / 247** | `offensiveFreezeMin/Max` **1.3–1.8 s**; `offensiveSlowColdMin` 60/77 over 2 s |
| `heroskills/chillbane_blizzard` | `Skill_BuffAttackRadiusDrop` | 4 / 5 | 58 / 76 | **111 / 137** | `offensiveSlowTotalSpeedMin` 30 % over 5 s |

Geometry (M):
- **`primordian_wave`** — `waveDistance 16.0`, `waveStartWidth 3.0 → waveEndWidth 6.0`, `waveDepth 1.0`,
  `waveTime 1.4 s`, `ragDollDirection Push`, `skillManaCost 60`. *"large cone wave with cold and poison dot."*
- **`primordian_frigidring`** — **`projectileLaunchNumber 16` at `projectileLaunchRotation 360°`**,
  `projectileExplosionRadius 1.5`, **`projectileUsesAllDamage = True`** (every one of the 16 carries
  the full row), `ragDollElevation Downward`. Range-banded scaling:
  `range1 0–2.5 m → 50 %` · `range2 2.5–9 m → 100 %` · **`range3 9–20 m → 140 %`**.
- **`chillbane_blizzard`** — `dropRadius 15.0` from `dropHeight 20.0`, `projectileLaunchNumber 6`,
  `skillTargetRadius 8.0`, `skillTargetInterval 2.0 s`, `skillActiveDuration 8.0 s`, `targetingMode Point`.
  A persistent 8-second ground hazard, not a hit.

**Trigger wiring (M) — the death mechanism:**

| slot | skill | chance | delay | timeout | range band |
|---|---|---|---|---|---|
| `specialAttack` | `primordian_wave` | 100 % | 5.0 s | 5.0 s | MediumRange (≤10) |
| `specialAttack2` | `primordian_frigidring` | 80 % | 6.0 s | 3.0 s | MediumRange (≤10) |
| `specialAttack3` | `chillbane_blizzard` | 100 % | 10.0 s | 8.0 s | LongRange (≤12) |
| `buffSelfSkillName` | `primordian_icearmor` | — | on `WhenEnemyIsSeen` (controller) | 32 s cooldown | self |

**Reading for the death at 5453 s (D, from M wiring):** the kit is **~85 % cold**, delivered as a
16-projectile 360° freeze ring (1.3–1.8 s hard freeze, `projectileUsesAllDamage`) layered over an
8-second persistent blizzard field and a 16-metre cone — against a **melee-locked** fixture kit
(claws ~245 uses, charge ~125, per frame 281). Every one of the three specials is an area denial
with a movement or action lock attached. There is no single-hit one-shot in this record; the
plausible mechanism is **freeze-lock inside the blizzard field while the ring re-fires on a 3 s
timeout**. Cross-check candidate for G-8: Matt's cold and freeze resistances at 5453 s.

---

## 4. Retaliation / aura / defensive (M)

**On the record:** `defensiveCold 35.0` · `defensivePoison 25.0` · `defensiveFreeze 500.0` ·
`defensiveKnockdown 500.0`. **No `retaliation*` field on the monster record at all.**

**Via `passive/resists_heroboss.dbr`** (skillName4, `skillLevel4 = 3` — **fixed rank 3**, not
level-scaled), 6-element arrays, rank-3 slice:
`defensiveStun 75` · `defensiveFreeze 60` · `defensivePetrify 75` · `defensiveSleep 60` ·
`defensiveTrap 50` · `defensiveKnockdown 500` · `defensiveManaBurn 500` · `defensiveManaBurnRatio 95` ·
`defensivePercentCurrentLife 88` · `defensivePercentReflectionResistance 40` ·
`defensiveTotalSpeedResistance 35` · `defensiveTaunt 20` · `defensiveSlowLifeLeach 18` ·
`defensiveConfusion / Convert / Disruption / Fear 500` (scalars).

**The only retaliation in the proto** — `bossskills/primordian_icearmor.dbr`
(`Class = Skill_BuffSelfDuration`, `instantCast`, `skillActiveDuration 12.0 s`,
`skillCooldownTime 32.0 s`, rank = `charLevel/4+1`):

| field | @ rank 4 | @ rank 5 |
|---|---|---|
| `retaliationSlowColdMin` (over `retaliationSlowColdDurationMin 2.0 s`) | 32 | 39 |
| `offensiveColdModifier` | +26 % | +28 % |
| `characterAttackSpeedModifier` | **+35 %** | +35 % |
| `damageAbsorptionPercent` | **25 %** | 25 % |
| `defensiveTotalSpeedResistance` | 500 | 500 |

So the aura is **a 12-on / 32-off cycle granting 25 % flat damage absorption, +35 % attack speed,
+~27 % cold, and a cold-DoT retaliation** — cast on first sight per `controller_boss_viloth
.BuffSelfBehavior = WhenEnemyIsSeen`. The pak applies `retaliationTotalDamageModifier = −66 %` on
Normal/1P (M, from G-5a §1e). **A melee kit that never disengages eats the retaliation and the
absorption window simultaneously** — directly relevant to the fixture.

**Controller** `controller_boss_viloth.dbr` (M, selected fields): `FleeBehavior NeverFlee` ·
`ViewDistance 15.0` (`InnerViewDistance 4.0`) · `MaxPursuitDistance **75.0**` · `PursuitTime 10000 ms` ·
`DodgeChance 50` @ `DodgeDistance 2.0` / `DodgeDelay 3000` · `AttackedAnger 16.0` ·
`RepositionChance 100` · `ChanceToRespondToDistressCall 20` (group `Slith`) ·
`ignorePetsChance 35` · `minSwingPause 0.30` / `maxSwingPause 0.40`.
**`NeverFlee` + 75 m pursuit + 50 % dodge + 100 % reposition** = a boss that kites into its own
ranged pattern and cannot be disengaged from. Second contributor to the death profile.

---

## 5. Loot — the amulet guarantee, closed to source (all M)

**Mechanism is an *equip* slot, not a drop roll:**

```
chanceToEquipMisc2      = 100.0      # necklace slot — always populated
chanceToEquipMisc2Item1 = 100        # single entry, weight 100
lootMisc2Item1          = records/items/loottables/gearaccessories/tdyn_necklace_b01_slithnecklace.dbr
dropItems               = True       # equipped gear drops on death
```

→ **100 % guaranteed necklace. Confirmed.** The `Misc2` route is why it is a guarantee and not a
chance: the item is generated at spawn and worn, and `dropItems` releases it.

`tdyn_necklace_b01_slithnecklace.dbr` (`LootItemTable_DynWeight`), bases —
all five resolve to `tagNecklaceB001` = **"Putrid Necklace"**, `itemClassification Rare`:

| entry | record | itemLevel / levelReq | weight |
|---|---|---|---|
| lootName1 | `b001_necklace.dbr` | **8 / 8** | 1000 |
| lootName5 | `b001a_necklace.dbr` | 18 / 18 | 800 |
| lootName2 | `b001b_necklace.dbr` | 32 / 32 | 800 |
| lootName3 | `b001c_necklace.dbr` | 52 / 52 | 700 |
| lootName4 | `b001d_necklace.dbr` | 70 / 70 | 650 |

Level gating: `targetLevelEquation = (parentLevel*1)-2` · `minItemLevelEquation = (parentLevel*0.95)-15` ·
`maxItemLevelEquation = (parentLevel*1)+5` · **`forceHighestLevel = True`**.

**`b001_necklace.dbr`** — `FileDescription = **"Wightmire Slith Boss"**` (the source names the
owner explicitly):
`characterLife **220.0**` · `defensivePoison 25.0` · `offensiveSlowPoisonModifier 18.0` ·
`augmentSkillName1 bloodofdreeg1 @ +2` · `augmentSkillName2 elementalinfusion1 @ +2` ·
two `modifierSkillName` entries (GDX1 monster-infrequent skill modifiers).

**Matt's exact roll, resolved:**
- prefix **"Menacing"** = `tagPrefixB022_Ar_A` → `records/items/lootaffixes/prefix/b_ar022_ar.dbr`
  (`levelRequirement 5`, `lootRandomizerJitter 28`): **`characterLife 80.0`**, `characterDexterity 16.0`,
  `characterOffensiveAbility 15.0`, `defensiveChaos 8.0`.
  **Reachability verified** — present in `prefixb01_accessory_allpoison.dbr` (the table's
  `rarePrefixTableName1`), alongside its `_b`/`_c`/`_d` level variants.
- suffix **"of Protection"** = `tagSuffixA019` → the `a019*_ch_da_*` family, all of which grant
  **`characterDefensiveAbility` only** (13 / 36 / 45 / 63 / 92 by level band). **No life, no mana.**

→ **Matt's necklace is the one Primordian was wearing, and it was worth ≈ +300 flat life *to
Primordian*.** That is the §0.3 contamination, quantified.

**Separate quest drop:** `perPartyMemberDropChance = 30`, `perPartyMemberDropItemName =
records/items/questitems/quest_slithnecklace.dbr` (`itemClassification Quest`, `questFile1
quests/sq_slithnecklaces.qst`) — the side-quest token, distinct from the wearable amulet.

**Other loot slots:** `chanceToEquipMisc1 = 45.0` over five weighted master tables
(`mt_comp_rare_a01` 5 / `mt_comp_beastscales_a01` 27 / `mt_comp_beastmutant_a01` 20 /
`materia/tdyn_comp_bonusslith_a01` 15 / `mt_crafting_ancientheart_a01` 33) ·
`chanceToEquipMisc3 = 100.0` → `misc/tdyn_constitution_a01.dbr` ·
`skillName5 = bossskills/boss_chest_01.dbr` (`Skill_OnDeathSpawnActor`, *"Boss Chest Spawner Tier 1"*)
→ spawns `records/items/lootchests/d02_bosschest_dropped.dbr` on death.

---

## 6. Records used (exact paths)

**Creature** `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/creatures/enemies/bios/bio_boss_standard_01.dbr` ·
`records/creatures/enemies/slitha_melee_b01.dbr` · `records/creatures/enemies/slitha_shaman_c01.dbr`

**Spawn** `records/proxies/boss&quest/proxy_wightmire_slitha01.dbr` ·
`records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr` ·
`records/proxies/lv6_hero.dbr` · `records/proxies/lv4_champion+.dbr` ·
`records/proxies/proxypoolequation_01.dbr` · `records/proxies/limit_area001.dbr` ·
`GDX2 records/endlessdungeon/proxies/poolsboss/slith_primordian.dbr`

**Skills** `records/skills/nonplayerskills/passive/{damage_totaladjuster, damagebase_physical04,
armorbase05, resists_heroboss}.dbr` · `records/skills/nonplayerskills/bossskills/{primordian_passive,
primordian_wave, primordian_frigidring, primordian_icearmor, boss_chest_01}.dbr` ·
`records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr`

**Present in corpus but NOT referenced by this creature** (banked for completeness; do not model):
`records/skills/nonplayerskills/bossskills/primordian_flurry.dbr` (`Skill_BuffSelfDuration`,
+50 % attack speed / +30 % run, 4 s / 12 s cd, `skillMaxLevel 1`) ·
`records/skills/nonplayerskills/bossskills/primordian_arcticblast.dbr`
(`Skill_AttackProjectileAreaEffect`, cold 201–246 @ r5, freeze 1.6–2.2 s, radius 2.0).
**M — both are orphaned in the base archive.** Likely cut content or Shattered-Realm-only wiring.

**Controller / faction** `records/controllers/enemy/controller_boss_viloth.dbr` ·
`records/controllers/factions/faction_beast.dbr`

**Items** `records/items/enemygear/gear_slithwarriorb01.dbr` ·
`records/items/loottables/gearaccessories/tdyn_necklace_b01_slithnecklace.dbr` ·
`records/items/gearaccessories/necklaces/b001{,a,b,c,d}_necklace.dbr` ·
`records/items/lootaffixes/prefix/b_ar022_ar.dbr` ·
`records/items/lootaffixes/prefix/prefixtables/prefixb01_accessory_allpoison.dbr` ·
`records/items/lootaffixes/suffix/a019{a,b}_ch_da_*.dbr` ·
`records/items/questitems/quest_slithnecklace.dbr` ·
`records/items/loottables/mastertables/{mt_comp_rare_a01, mt_comp_beastscales_a01,
mt_comp_beastmutant_a01, mt_crafting_ancientheart_a01}.dbr` ·
`records/items/loottables/materia/tdyn_comp_bonusslith_a01.dbr` ·
`records/items/loottables/misc/tdyn_constitution_a01.dbr`

**Global** `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` (Normal/1P = index 0)

**Provenance** — corpus root `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`; archive
SHA-256s as banked in the G-5a ledger §Provenance (unchanged). Display names via
`*/resources/Text_EN.arc`, 20,394 tags. Tooling:
`legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py` → gandalf's G-4 wrapper →
`research/scripts/gd_arz_adapter_2026_07_24.py`. Nothing rebuilt, nothing written outside `notes/`.

---

## 7. Confidence + what is held

### High confidence (MEASURED)
Every field in §1, §3a–3d, §4, §5, §6. The identity `tagSlithBossB02 = Primordian` (exhaustive tag
sweep + exhaustive creature-record sweep, single hit each). The `+3` charLevel remap. The 100 %
necklace-equip guarantee and its full base/prefix/suffix chain.

### DERIVED (arithmetic shown)
The charLevel table in §1 (evaluating M equations). The bio value table in §2. The required-factor
table in §2. The death-mechanism reading in §3d — grounded entirely in M wiring, but it is a
*reading*, not a measurement.

### HELD / UNRESOLVED
1. **Champion/hero/boss damage regime** — held per §14.10. §3a–3d are raw arrays only. At cl 13/17
   the additive TDM sums to −95 %/−91 %, i.e. **deep in the unmeasured clamp band where a 4-point
   array shift moves output ~80 %.** Primordian must not enter G-5 damage pinning until the clamp
   resolves. It *is*, however, a **better** clamp fixture than Warden Krieg: no weapon, no
   `damagebonus_*`, fully source-resolvable once the operator lands.
2. **HP composition** — held per §14.11. §2 stages every input; composition is one operator away.
   **But see §0.3: Primordian is a noisy instrument.** Recommend the closure triple come from a
   monster with zero `chanceToEquip*` slots.
3. **Which level the save's `13` denotes** (charLevel vs spawn level). Unresolved and now
   consequential — the `+3` remap makes the two readings differ by 3 levels ≈ 33 % HP. A
   `greatestMonsterKilled` triple from a **non-remapping** monster (`charLevel*1`) would settle the
   semantics independently of the composition operator. **This is a cheaper and more decisive ask
   than a second boss triple.**
4. **Attack cadence in seconds** — same limitation as G-5a §6.2: `characterAttackSpeed 1.0` is a
   multiplier on an animation-driven base living in `.anm` tables this lane does not parse. The
   `specialAttack*Delay` / `Timeout` values (5/6/10 s, 5/3/8 s) **are** in seconds and are M — so
   Primordian's *ability* cadence is pinned even though its *basic-attack* cadence is not.
5. **The two orphaned `primordian_*` skills** (§6) — present, unreferenced. Not modelled.
6. **`slitha_melee_b01` / `slitha_shaman_c01`** — the two mandatory champion escorts are named and
   their `lv4_champion+` variance equation is M, but their protos were not extracted (out of
   commission scope). **The G-5 scenario needs them**; a follow-on pass is ~10 minutes.

---

*Downstream: gandalf (KC1 conductor) — §0 corrections are charter-level, §2 bears on the §14.11
closure path, §6.6 is an open scope item for the G-5 harness. galadriel (G-8) — §0.3 narrows what
counts as a valid second HP triple; §3d names the cold/freeze cross-check for frame 281. No
canonical doc amended by this note.*
