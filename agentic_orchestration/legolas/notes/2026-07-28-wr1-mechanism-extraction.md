# WR1 — mechanism extraction for M-1 / M-2 / M-4 (Grim Dawn Edition-II corpus)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Run:** WR1-2026-07-28
**Conductor:** gandalf (RUN-CONDUCTOR) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` (§1 S-6 corpus pin, §3 mechanism table)
**Class:** evidentiary — measured extraction from primary source
**Mode:** READ-ONLY throughout. Nothing written inside `vendor/`. Writes confined to
`legolas/notes/` + `legolas/scratch/2026-07-28-wr1/`.

## Provenance

Corpus `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (co-pinned 2026-07-24; SHA-256
per archive banked in `2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` — unchanged, not
re-hashed here). 93,190 records across `database.arz` (34,114) / `GDX1.arz` (18,447) /
`GDX2.arz` (16,451) / `GDX3.arz` (24,178).

Tooling reused, nothing rebuilt: `research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive`) and
`research/scripts/gd_arc_reader_2026_07_26.py` (`ArcArchive`, `parse_tag_file`).
Probes: `legolas/scratch/2026-07-28-wr1/probe{1..11}*.py`.

**One provenance exception, flagged.** The Edition-II pin ships **no `templates.arc`** — only
`database/*.arz` + `resources/Text_EN.arc`. Template-schema reads in §E-1.5 and §E-3.5 come from
the legacy sibling `~/Games/vendor/grim-dawn/database/templates.arc` (819 entries). Every such read
is marked **T‑LEGACY**. Field *values* are all Edition-II; only field *schemas/descriptions* are
T‑LEGACY.

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`) · **D** = DERIVED (arithmetic or
geometry shown, operator named) · **I** = INFERRED (reading not stated in source; reasoning given) ·
**U** = UNRESOLVED / not in corpus.

---

## 0. Headline — five numbers and one structural finding

1. **Armor mitigates PHYSICAL ONLY.** `combatformulas.dbr` defines exactly two damage-defense
   equations, both named `physical*`. There is no cold / fire / lightning / aether / pierce defense
   equation anywhere in the record. **M.** Consequence for the run: the frigidring nova is
   **~85 % cold** and armor is *structurally inert* against it. That is the mechanism by which
   mitigation changes the **shape** of danger rather than its scale — the G-A signature, sourced.
2. **Armor absorption constant = `armorDefensiveAbsorption 70.0`** (`records/game/gameengine.dbr`).
   Damage > armor → `dmg − armor×0.70`. Damage ≤ armor → `dmg × 0.30`. **M.**
3. **Player attack-speed cap = 200 % / floor 20 %** (`playerAttackSpeedCapMax/Min`). Monsters
   500 % / 20–40 % by difficulty; bosses 500 % / 50 %. **M.** The charter's "GD caps at 200 %?"
   is CONFIRMED for players, and the monster ceiling is 2.5× higher.
4. **The nova has TWO source lineages, not one.** `primordian_frigidring` (the boss's) and
   `igrixx_frigidring` (an Act-1 Wightmire *hero* slith — **"Igrixx, the Rimeheart"**, reachable
   from the same slith pools at 15–40 % champion chance). Both `Skill_AttackProjectileRing`, both
   16 projectiles at 360°, both firing `icebolt_nova_fxprojectile`. Different damage, radius and
   freeze payload. **M.** Matt's death-2 is not uniquely attributable to Primordian.
5. **Telegraph windup duration is NOT IN THE CORPUS.** `skill_attackprojectilering.tpl` defines
   **zero** timing fields — no cast time, no windup, no cooldown, no active duration (**T‑LEGACY,
   M**). All cadence lives on the *monster* record (`specialAttack2Delay/Timeout`) and all windup
   lives in `.anm` binary assets, which this pin does not ship. **U — do not improvise a number.**

---

# E-1 — Frigidring / telegraph-burst nova (feeds M-2)

## E-1.1 Candidate set — the corpus-wide sweep

Method (probe5): enumerate every record in all four archives whose `Class == Skill_AttackProjectileRing`
(**289 records**), plus every `nonplayerskills/` record whose filename matches
`frigid|nova|ring|blizzard`. Then reverse-reference (probe6): scan every
`records/creatures/**` record for fields pointing at each cold-ring candidate.

**Cold-payload ring/nova skills wired to any creature:**

| record | Class | carriers | in Act-1 slith pools? |
|---|---|---|---|
| `records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr` | `Skill_AttackProjectileRing` | `boss&quest/slith_wightmirecave01` (Primordian), `devotion/slith_h08` | **yes — via Primordian's fixed trio** |
| `records/skills/nonplayerskills/heroskills/igrixx_frigidring.dbr` | `Skill_AttackProjectileRing` | `hero/slith_h01` (**Igrixx, the Rimeheart**), `boss&quest/waveevent_wightmirerift_slith_h01`, `devotion/slith_h01`, + 11 non-Act-1 carriers | **yes — champion slot, `p_beasts_slith{a,b,c}_*`** |
| `records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr` | `Skill_BuffAttackRadiusDrop` | Primordian slot 3, + 24 others | yes (Primordian only, in Act 1) |
| `records/skills/nonplayerskills/bossskills/special/cloneice_icenova.dbr` | `Skill_AttackRadius` | `special/clone_c0*` (Nemesis) | no |
| `records/skills/nonplayerskills/bossskills/primordian_arcticblast.dbr` | `Skill_AttackProjectileAreaEffect` | **none — orphaned** | no |

All **M**. Display names bridged from `Text_EN.arc`: `tagSlithHeroH01 = "Igrixx, the Rimeheart"`,
`tagSlithBossB02 = "Primordian, the Forgotten One"`.

> **Correction owed to the fixture read.** The commission assumed one nova. There are two live in
> the same Act-1 Wightmire content. `slith_h01` (Igrixx) appears as `nameChampion5`/`nameChampion6`
> in `records/proxies/pools/p_beasts_slitha_t` (weight 6, championChance 30), `…_vt` (weight 10,
> cc 33), `…_amb_s1_n` (weight 3, cc 15), `…_xhighhero` (weight 60, cc 15), and the `slithb`/`slithc`
> equivalents — all at `levelVarianceEquation = lv6_hero`, `limit 1`. **M.** Which one killed Matt
> is not decidable from the corpus; it IS decidable from the fixture trace if the trace carries a
> damage-source label. Flagged for gandalf, not adjudicated here.

## E-1.2 `primordian_frigidring` — full measured parameter set

`records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr` · `database.arz` ·
`Class = Skill_AttackProjectileRing` · `templateName = database/templates/skill_attackprojectilering.tpl` ·
`FileDescription = "Freeze projectile ring"` · `skillMaxLevel = 60` · array length 60.

**Rank equation on the carrier:** Primordian `skillLevel7 = 'charLevel/4+1'`. At the fixture band
(player ≈ 12 → Primordian `charLevel = 17–18` per the `+3` remap, §KC1 Primordian proto §1) the
skill resolves at **rank 5**. Rank 4 (charLevel 13) is shown alongside because the KC1 charLevel
question is still **U**.

| field | r1 | **r4** | **r5** | r6 | grade |
|---|---|---|---|---|---|
| `offensiveColdMin` | 68 | **200** | **247** | 294 | M |
| `offensivePhysicalMin` | 34 | **118** | **148** | 179 | M |
| `offensiveFreezeMin` (s) | 1.2 | **1.3** | **1.3** | 1.4 | M |
| `offensiveFreezeMax` (s) | 1.6 | **1.8** | **1.8** | 1.9 | M |
| `offensiveSlowColdMin` | 17 | **60** | **77** | 92 | M |
| `skillManaCost` | 22 | 34 | 38 | 42 | M |

`offensiveColdMax = 0.0` and `offensivePhysicalMax = 0.0` — **both damage rows are Min-only**, i.e.
the **C-flag** (max clamped to min) from the G-5a ledger applies. The nova is a **flat-damage hit,
not a range roll**. **M.** ~85 % of the flat payload is cold at r5 (247 of 395).

`offensiveSlowColdDurationMin = 2.0` s (the cold DoT window). `offensiveSlowColdChance = 0.0`,
`offensiveFreezeChance` absent → **no chance gate on either CC; both apply on every hit that lands.**
**M.** (`Chance = 0` in GD's offensive-field convention means "not a chance-gated rider"; the
non-zero `*Chance` fields elsewhere in the same record are all 0 too, and the record has no
`offensiveGlobalChance`. Reading is **I**, but uniform across the record.)

**Geometry (all M):**

| field | value |
|---|---|
| `projectileLaunchNumber` | **16** |
| `projectileLaunchRotation` | **360.0°** (→ 22.5° spacing) |
| `projectileExplosionRadius` | **1.5** m |
| `projectileUsesAllDamage` | **True** — *every one of the 16 carries the full row* |
| `projectileDamageRange1` | 0.0 – 2.5 m → **50 %** scale |
| `projectileDamageRange2` | 2.5 – 9.0 m → **100 %** scale |
| `projectileDamageRange3` | 9.0 – 20.0 m → **140 %** scale |
| `distanceProfile` | `Long` |
| `ragDollDirection` / `Elevation` / `Effect` | `Push` / `Downward` / `TakeHit` |
| `skillProjectileName` | `records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr` |
| `skillSpecialAnimationName` | **`Roar`** |
| `cameraShakeAmplitude` | 0.12 |

**Projectile physics** — `records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr`
(`Class = ProjectileFireballLike`), all **M**:
`projectileVelocity = 14.0` (m/s) · `projectileDistance = 12.0` (m) · `actorRadius = 0.10` ·
`collisionShape = Sphere` · `collidesWithProjectiles = False` · `physicsFriction 4.0` ·
`projectileHitTTLMin/Max = 0.0` · `projectileMissTTLMin/Max = 0.0`.

**Derived ring kinematics (D — geometry only, no assumed constants):**

- Time-to-target at distance *d*: **t = d / 14.0** s. Melee band (1.25–2.5 m) → **0.09–0.18 s**.
  Full extent 12 m → **0.857 s**. Beyond 12 m the projectile expires (`projectileDistance`).
- Angular gap closes when `2 × explosionRadius ≥ 2πd/16`, i.e. **d ≤ 7.64 m**. Inside 7.64 m the
  ring is **gapless** — there is no "step between the bolts" dodge. Outside it, gaps open.
- Range-scale interaction: the 140 % band (9–20 m) is reachable but the projectile only lives to
  12 m, so the effective 140 % window is **9–12 m** — i.e. the nova hits *hardest* at the outer
  edge, and the 50 % band is the melee hug. **This inverts the usual "back off to survive" reflex**
  and is the single most fidelity-relevant geometric fact for M-2/M-3.

## E-1.3 `igrixx_frigidring` — the second lineage

`records/skills/nonplayerskills/heroskills/igrixx_frigidring.dbr` · `database.arz` ·
`Skill_AttackProjectileRing` · `FileDescription = "Freeze projectile ring"` · `skillMaxLevel = 60`.
Carrier `hero/slith_h01`, `skillLevel5 = 'charLevel/4+1'`, `charLevel = 'charLevel*1+5'`,
spawn `lv6_hero` → at player 12 spawn 14–15 → **charLevel 19–20 → rank 5–6**. All **M**.

| field | r1 | **r5** | **r6** |
|---|---|---|---|
| `offensiveColdMin` | 49 | **171** | 204 |
| `offensiveFreezeMin` (s) | 0.7 | **0.9** | 0.9 |
| `skillManaCost` | 20 | 40 | 45 |

`offensiveColdMax = 0.0`; `offensiveFreezeMax` **absent from the record entirely**; no
`offensivePhysical*`, no `offensiveSlowCold*`. So Igrixx's nova is **pure cold, fixed-duration
freeze, no cold DoT rider** — mechanically cleaner and weaker than Primordian's. **M.**

Geometry differs: `projectileExplosionRadius = **2.0**` (vs 1.5), `projectileLaunchNumber 16`,
`projectileLaunchRotation 360°`, `projectileUsesAllDamage True`, bands
**0–2.0 → 50 % · 2.0–10.0 → 100 % · 10.0–20.0 → 150 %** (vs 140 %). Same projectile record, so same
14 m/s / 12 m kinematics. Gapless radius = 2×2.0/(2π/16) = **10.19 m**. **M / D.**

**Wiring on `hero/slith_h01` (M):** `specialAttack2SkillName = igrixx_frigidring`,
`specialAttack2Chance = 100.0`, `specialAttack2Delay = 10.0`, `specialAttack2Timeout = 3.0`,
`specialAttack2Range = **ShortRange**`. Slot 1 is `igrixx_chillingfront` (`MediumRange`, chance 100,
delay 8.0, timeout 3.0). Also carries `igrixx_chilledweapons`. Controller
`controller_slith_melee` (`minSwingPause 0.65` / `maxSwingPause 1.20`).
Base tables: `damagebase_physical03`, `armorbase03`, `resists_heroboss` (fixed rank 2),
`passiveproperties_herodeflection`. `characterAttackSpeed = 1.0`, `numAttackSlots = 8`,
`chanceToEquipRightHand/LeftHand = 0` (unarmed — no W-flag).

## E-1.4 Primordian's full skill loadout (M) — for the "which skill is the ring nova" ask

`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr`. Rank equations verbatim.

| slot | record | `skillLevel` eq | Class | role |
|---|---|---|---|---|
| 1 | `passive/damage_totaladjuster` | `(charLevel/25)+2` | `Skill_Passive` | TDM +8 |
| 2 | `passive/damagebase_physical04` | `charLevel*1` | `Skill_Passive` | base unarmed attack |
| 3 | `passive/armorbase05` | `charLevel*1` | `Skill_Passive` | armor + TDM/life damper |
| 4 | `passive/resists_heroboss` | `3` (fixed) | `Skill_Passive` | CC/elem resists |
| 5 | `bossskills/boss_chest_01` | `1` | `Skill_OnDeathSpawnActor` | loot |
| 6 | `heroskills/chillbane_blizzard` | `charLevel/4+1` | `Skill_BuffAttackRadiusDrop` | 8 s ground hazard |
| **7** | **`bossskills/primordian_frigidring`** | **`charLevel/4+1`** | **`Skill_AttackProjectileRing`** | **THE RING NOVA** |
| 8 | `bossskills/primordian_wave` | `charLevel/4+1` | `Skill_AttackWave` | 16 m cone |
| 9 | `bossskills/primordian_icearmor` | `charLevel/4+1` | `Skill_BuffSelfDuration` | 25 % absorb / +35 % aspd |
| 10 | `bossskills/primordian_passive` | `charLevel/4+1` | `Skill_Passive` | cold rider on base attack |

Trigger wiring (**M**): `specialAttackSkillName = primordian_wave` (chance 100, delay 5.0,
timeout 5.0, MediumRange) · `specialAttack2SkillName = **primordian_frigidring**` (chance **80**,
delay **6.0**, timeout **3.0**, **MediumRange** ≤ 10 m) · `specialAttack3SkillName =
chillbane_blizzard` (chance 100, delay 10.0, timeout 8.0, LongRange ≤ 12 m) ·
`buffSelfSkillName = primordian_icearmor` (controller `BuffSelfBehavior = WhenEnemyIsSeen`).
Range bands on the creature: `shortRangeMax 4.0` / `mediumRangeMax 10.0` / `longRangeMax 12.0`.

`primordian_arcticblast.dbr` exists in the corpus (`Skill_AttackProjectileAreaEffect`, cold 201–246
@ r5, freeze 1.6–2.2 s, radius 2.0) but is **referenced by no creature** — orphaned. **M. Do not
model it.**

## E-1.5 Cooldown / telegraph — what the source does and does NOT define

**`skill_attackprojectilering.tpl` (T‑LEGACY, M) declares exactly 13 variables:**
`skillProjectileName`, `projectileLaunchRotation`, `projectileLaunchNumber`,
`projectileUsesAllDamage`, and the nine `projectileDamageRange{1,2,3}{Min,Max,Scale}` fields.
**No `skillCooldownTime`, no cast time, no windup, no `skillActiveDuration`, no charge time.**
Confirmed against the records: `primordian_frigidring` and `igrixx_frigidring` both carry
`skillCooldownReduction = 0.0` / `skillCooldownReductionModifier = 0.0` but **no
`skillCooldownTime` field at all**. **M.**

**Therefore the entire cadence model for a monster ring nova is on the CREATURE record**, via
`templatebase/monsterskillmanager.tpl` (T‑LEGACY). Only two of those fields carry authored
descriptions:

```
specialAttackDelay     "Seconds - delay for special skill use"
specialAttackTimeout   "Seconds - time out for all skill use"
specialAttackChance    "[0..100]"
```

Slots 2–7 (`specialAttack2Delay`, `specialAttack2Timeout`, …) declare the same field names with
**empty descriptions**. **M** on the schema; the per-slot semantics are **I by symmetry**:
`Delay` = per-slot cooldown between uses of *that* skill; `Timeout` = lockout gate. Whether the
slot-1 `Timeout`'s "**all** skill use" wording makes it a *global* cross-slot gate while slots 2–7
are per-slot is **U — genuinely ambiguous in source, and it changes Primordian's nova cadence by a
factor of ~2.** Both readings, stated so the spec can pick one explicitly:

- *Reading A (per-slot):* nova available every **6.0 s** (`specialAttack2Delay`) at 80 % roll.
- *Reading B (global gate + per-slot):* any special locks all specials for **5.0 s**
  (`specialAttackTimeout`, slot 1), and the nova additionally gates on its own 6.0 s / 3.0 s.

**Telegraph windup — U.** `skillSpecialAnimationName = 'Roar'` resolves through
`charAnimationTableName = records/creatures/enemies/anm/anm_slith.dbr` →
`unarmedSpecialAnimRef3 = 'Roar'` → `unarmedSpecialAnim3 =
creatures/enemies/slith/anm/slith01_cast_buff_01.anm`, at `unarmedSpecialAnimSpeed3 = 1.0`
(no speed-up). **All M — the asset is pinned by name.** But its **duration lives in the `.anm`
binary, and this corpus ships no `.anm` / `.msh` / `Creatures.arc`** (verified: `find . -name '*.anm'`
returns nothing; the only `.arc` files present are eight `Text_EN.arc`). **The windup duration is
NOT derivable from the pinned corpus.** Options for closing it are listed in §Gaps.

---

# E-2 — Armor / mitigation formulas (feeds M-1)

Sources: `records/game/gameengine.dbr` (constants + caps, `database.arz`, **no GDX override** —
re-verified across all four archives) and `records/game/combatformulas.dbr`
(`gameengine.defaultCombatManagerRecord`, `templateName = database/templates/combatequations.tpl`).

## E-2.1 The equation set, verbatim (all M)

```
probabilityToHitEquation  = ((((offensiveAbilityDV/((defensiveAbilityDV/3.5)+offensiveAbilityDV))*300)*0.3)
                            + (((((offensiveAbilityDV*3.25)+10000) - (defensiveAbilityDV*3.25))/100)*0.7)) - 50
normalPTHEquation         = probabilityToHitDV/70

offensiveAbilityEquation  = (offensiveAbilityDV + (characterLevelDV*12) + ((dexterityDV+bonusDV)*0.5)) * (1 + (offensiveAbilityModifierDV/100)) + 53
defensiveAbilityEquation  = (defensiveAbilityDV + (characterLevelDV*12) + ((strengthDV +bonusDV)*0.5)) * (1 + (defensiveAbilityModifierDV/100)) + 53

physicalDamageEquation           = (physicalDamageDV*((dexterityDV/245)+1))
physicalDamagePercentage         = (physicalDamageDV*((dexterityDV/245)+1))
physicalDurationDamageEquation   = (physicalDamageDV*((dexterityDV/215)+1))
pierceDamageEquation             =  pierceDamageDV*((dexterityDV/245)+1)
magicalDamageEquation            =  magicalDamageDV*((intelligenceDV/215)+1)
magicalDurationDamageEquation    =  magicalDamageDV*((intelligenceDV/200)+1)
physicalDamageBonus              = '0'

physicalDamageDefenseEquationDGP = (sumProtectionDV * (1 - sumAbsorptionDV)) + (physicalDamageDV - sumProtectionDV)
physcialDamageDefenseEquationDLEP=  physicalDamageDV * (1 - sumAbsorptionDV)          [sic — 'physcial' typo in source]

meleeBlockEquation               = (blockChanceDV + blockChanceModifierDV)
projectileBlockEquation          = (blockChanceDV + blockChanceModifierDV)
shieldDamageReductionEquationDGB =  damageDV - (shieldDefenseDV * (shieldAbsorptionDV / 100))
shieldDamageReductionEquationDLEB=  damageDV * ((100 - shieldAbsorptionDV) / 100)

physicsStrengthEquation          = (2*(damage/(maxLife*.3)))+4        [ragdoll impulse, min 7 max 15]
```

**Crit / PTH ladder (M):** `pthMinimum = 55.0`; thresholds `70 / 90 / 105 / 120 / 130 / 135` with
multipliers `1.0 / 1.1 / 1.2 / 1.3 / 1.4 / 1.5`. Five `critStyle` UI records + `monsterCritStyle`.
*(Relevant to M-6 crit labelling; banked here because it is in the same record.)*

**Hit-location model (M)** — `combatformulas.dbr`, sums to exactly 100:

| region | chance |
|---|---|
| Torso | **26** |
| Legs | **20** |
| Head | **15** |
| Shoulders | **15** |
| Arms | **12** |
| Feet | **12** |
| `combatRegionFullyProtectedChance` | **0** |
| `combatRegionUnprotectedChance` | **0** |

## E-2.2 The mitigation constants (all M, `gameengine.dbr`)

| constant | value | template description (T‑LEGACY) |
|---|---|---|
| `armorDefensiveAbsorption` | **70.0** | *(none)* |
| `playerDefenseCap` | **[80.0, 80.0, 80.0]** | "Index by difficulty 0 to 2" |
| `monsterDefenseCap` | **[100.0, 100.0, 100.0]** | "Index by difficulty 0 to 2" |
| `playerReflectCap` | 30.0 | — |
| `monsterLevelGapFixer` | [0, 5, 7] | — (0 on Normal) |
| `damageMagnitude` | 100.0 | — (semantics **U**) |
| `pvpDamageMultiplier` / `pvpCrowdControlDurationMultiplier` | 0.20 / 0.40 | — |
| `meleeRange` / `shortRange` / `moderateRange` / `longRange` / `maximumRange` / `bossRange` | 1.25 / 4.75 / 9.0 / 15.0 / 18.0 / 32.0 | — |
| `autoCastEquation` | `procRate * (1 + (cooldown*81)/100) * (1 - (attackDuration*11)/100)` | — |

## E-2.3 The formula chain — raw hit → HP loss

Stated as a chain so M-1 can be spec'd against it. Grade per step.

```
STEP 1  hit roll          PTH = probabilityToHitEquation(OA, DA)                       M
                          floor  pthMinimum = 55                                        M
                          damage multiplier from the PTH ladder (1.0 .. 1.5)            M
STEP 2  region roll       one of six regions, weights above                             M
                          -> selects WHICH armour piece supplies sumProtection          I
STEP 3  attribute scale   physical: dmg x ((dex/245)+1)                                 M
                          magical : dmg x ((int/215)+1)      [elemental/cold path]      M
                          pierce  : dmg x ((dex/245)+1)                                 M
STEP 4  ARMOUR            PHYSICAL ONLY (no other type has a defense equation)          M
                          if dmg  > armour:  out = armour x (1 - abs) + (dmg - armour)  M
                                             == dmg - armour x abs                      D
                          if dmg <= armour:  out = dmg x (1 - abs)                      M
                          abs = armorDefensiveAbsorption/100 = 0.70, adjusted by
                                defensiveAbsorptionModifier                             M/I
STEP 5  block (if any)    if blocked and dmg  > shieldDefense: out = dmg - shieldDefense x (shieldAbs/100)   M
                          if blocked and dmg <= shieldDefense: out = dmg x ((100 - shieldAbs)/100)           M
                          block chance = blockChance + blockChanceModifier              M
STEP 6  resistance        out x (1 - res/100), res capped at DefenseCap                 I  (see below)
STEP 7  flat/percent DR   damageAbsorptionPercent, offensiveTotalDamageModifier         U  (stacking rule not in source)
```

**Step 4 worked, at the fixture band (D).** Primordian's own armour (`armorbase05` @ charLevel 17)
= `defensiveProtection 105`, pre-pak. A 100-damage physical hit into 105 armour takes the
**DLEP** branch: `100 × (1 − 0.70) = **30**`. A 300-damage hit takes **DGP**:
`300 − 105×0.70 = **226.5**`. **Armour is a flat subtraction of `0.70 × armour` above the
armour value, and a 70 % reduction below it.** This is the whole of GD's physical mitigation curve.

**Step 4 caveat — monster absorption is modified.**
`records/game/balancingadjustment_mp+difficulty_enemies01.dbr` carries
`defensiveAbsorptionModifier = [-20.0] × 12` (**all three difficulties, all player counts — M**),
and `defensiveAbsorption = 0.0`, `defensiveProtection = 0.0`, `defensiveProtectionModifier` absent.
So **monster** absorption is 70 % adjusted by −20 %. GD's `*Modifier` convention is multiplicative
`× (1 + mod/100)` → **56 %**; a literal-subtraction reading gives **50 %**. **I — 56 % is the
convention-consistent reading, but the source does not state it. Flag it in the M-1 spec rather
than burying it.** The **player** pak
(`balancingadjustment_mp+difficulty_players01.dbr`) carries **no** absorption or protection field
at all → **player absorption is the unmodified 70 %.** **M.**

**Step 6 — the resistance cap, and why it is graded I.** No record states "resistances cap at X".
The evidence is: (a) field names `playerDefenseCap` / `monsterDefenseCap`, (b) values 80 / 100,
(c) the player pak applies its penalties to `defensiveFire/Cold/Lightning/Pierce/Poison/Aether/
Bleeding/Chaos/Life/SlowLifeLeach` — i.e. exactly the "resistance" family. The 80/100 split is
consistent and the naming is unambiguous, but the *application operator* (hard clamp vs. soft
diminishing) is not in the corpus. **I.**

**Player resistance penalties by difficulty — M, and directly load-bearing for the fixture.**
`balancingadjustment_mp+difficulty_players01.dbr` (`Class = AttributePak`), 12-element arrays,
index = `difficulty*4 + (players−1)`:

| field | Normal (idx 0–3) | Elite (4–7) | Ultimate (8–11) |
|---|---|---|---|
| `defensiveCold` / `Fire` / `Lightning` / `Pierce` / `Poison` | **0** | −25 | −50 |
| `defensiveAether` / `Bleeding` / `Chaos` / `Life` / `SlowLifeLeach` | **0** | 0 | −25 |

→ **On Normal the player takes zero resistance penalty.** The fixture is Normal/1P, so cold
resistance at death-2 is whatever Matt's gear gave him and nothing else. Also on this record:
`characterBaseAttackSpeedTag = 'CharacterAttackSpeedAverage'`.

**`defensiveAbsorption` on gear is effectively dead content (M).** A full sweep of all 93,190
records for a non-zero `defensiveAbsorption` returned **one** hit:
`records/sandbox/passive_target.dbr` = 100.0. Every shipped armour piece carries
`defensiveAbsorption = 0.0` (verified on `records/items/gearhead/c001_head.dbr`, which carries
`defensiveProtection = 61.0`, `defensiveAbsorption 0.0`, `defensiveAbsorptionModifier 0.0`).
→ **`sumAbsorptionDV` is, in practice, the global 70 % and nothing else.** That is a clean
simplification the M-1 spec can rely on.

---

# E-3 — Attack-speed / animation model (feeds M-4)

## E-3.1 Correction to the commission's framing

The commission asks to "generalize" the EoR `timeBetweenAttacks × 0.8` finding. **It does not
generalize — `timeBetweenAttacks` is not the standard-attack cadence field.** A census across all
four archives of every `records/skills/**` record carrying `timeBetweenAttacks` returns **58
records in 7 classes**, all of them channel / beam / tether / charge classes:

| Class | n | values (ms) | example |
|---|---|---|---|
| `Skill_AttackPathCharge` | 29 | 100 | `[GDX2] records/skills/base_template skills/skill_attackpathcharge.dbr` |
| `SkillSecondary_Tether` | 13 | 300, 330, 500, 600, 800 | `[GDX1] …/skill_skillsecondary_tether.dbr` |
| `Skill_AttackSpellBeam` | 6 | 50, 300 | `records/skills/itemskills/relics/relic_conflagration.dbr` |
| `Skill_AttackSpellCone` | 3 | 300 | `[GDX1] …/skill_attackspellcone.dbr` |
| **`Skill_AttackRadiusSpin`** | **3** | **200** | `[GDX2] …/skill_attackradiusspin.dbr` (**EoR's class**) |
| `Skill_AttackSpellDrain` | 2 | 300 | `[GDX1] …/skill_attackspelldrain.dbr` |
| `Skill_AttackRadiusGrow` | 2 | 200 | `[GDX3] …/skill_attackradiusgrow.dbr` |

**M.** No `Skill_Attack`, `Skill_AttackWeapon`, `Skill_AttackProjectile*` or
`Skill_AttackRadius` record carries it. Standard attacks use a different mechanism entirely (§E-3.2).
The `×0.8` in the prior EoR note came from a **developer-authored description string**, not a field,
and is specific to that skill — it must not be lifted into the general model.

## E-3.2 The standard-attack model

**Player side (M):** `records/creatures/pc/malepc01.dbr` and `femalepc01.dbr` are identical on this:

```
characterAttackSpeed        = 1.25
characterAttackSpeedModifier= 0.0
characterBaseAttackSpeedTag = 'CharacterAttackSpeedAverage'
```

All ~150 per-weapon-stance `*AttackAnimSpeed` / `*AnimSpeed` fields on the PC record are **1.0** —
i.e. no stance carries a hard-coded animation-rate override. **M.**

**Weapon side (M):** weapons carry **`characterBaseAttackSpeed`**, a signed **fractional offset**,
not an interval. Range observed: `+0.01` (fastest 1h sword) down to `−0.24` (slowest 2h gun).
`WeaponArmor_Shield` and `WeaponArmor_Offhand` carry no value at all (n = 195/127 null in
`database.arz`). Per-class ranges, `database.arz`:

| weapon class | `characterBaseAttackSpeed` range | modal band |
|---|---|---|
| `WeaponMelee_Dagger` | −0.02 (uniform, n=120) | −0.02 |
| `WeaponMelee_Sword` | −0.06 … **+0.01** | −0.02 |
| `WeaponMelee_Axe` | −0.01 … −0.10 | −0.02 … −0.07 |
| `WeaponMelee_Mace` | −0.03 … −0.17 | −0.10 |
| `WeaponMelee_Scepter` | −0.08 … −0.16 | −0.10 |
| `WeaponMelee_Sword2h` | −0.11 … −0.18 | −0.16 |
| `WeaponMelee_Axe2h` | −0.11 … −0.20 | −0.17 |
| `WeaponMelee_Mace2h` | −0.14 … −0.20 | −0.19 |
| `WeaponHunting_Ranged1h` | −0.04 … −0.12 | −0.08 |
| `WeaponHunting_Ranged2h` | −0.14 … −0.24 | −0.18 … −0.23 |

**Display band (M):** `characterBaseAttackSpeedTag` is a separate authored label, the ladder being
`tagAttackSpeedVerySlow / Slow / Average / Fast / VeryFast` (plus two vestigial `Moderate` records
and a handful of legacy `CharacterAttackSpeedAverage` literals on transmute/shield records).
Class → tag census across all four archives:

| class | dominant tag(s) |
|---|---|
| Dagger | **VeryFast** (375) · Fast (9) |
| Sword 1h | **VeryFast** (286) · Fast (51) |
| Axe 1h | **Fast** (223) · VeryFast (83) · Average (49) |
| Mace 1h | **Fast** (159) · Average (110) · Slow (54) |
| Scepter | **Average** (307) · Fast (16) |
| Sword 2h | **VerySlow** (84) · Slow (73) · Average (11) |
| Axe 2h | **VerySlow** (107) · Slow (18) · Average (8) |
| Mace 2h | **VerySlow** (112) · Slow (56) |
| Spear 2h | **Slow** (70) · VerySlow (42) |
| Gun 1h | **Average** (213) · Fast (80) · Slow (5) |
| Gun 2h | **VerySlow** (320) · Slow (64) |

**The tag and the numeric are NOT redundant — and neither one is an interval.** Daggers at a
uniform −0.02 are tagged VeryFast while swords at −0.05 are also tagged VeryFast, so the tag is
not derived from `characterBaseAttackSpeed`. **I:** `characterBaseAttackSpeed` is an offset applied
*within* a per-class-per-tag baseline that lives in the animation asset, not in the DB.

## E-3.3 Caps — the charter's question, answered (all M, `gameengine.dbr`)

| cap | value |
|---|---|
| **`playerAttackSpeedCapMax`** | **200.0** |
| **`playerAttackSpeedCapMin`** | **20.0** |
| `playerSpellCastSpeedCapMax` / `Min` | 200.0 / 20.0 |
| `monsterAttackSpeedCapMax` | 500.0 |
| `monsterAttackSpeedCapMin` | **[20.0, 30.0, 40.0]** (by difficulty) |
| `monsterSpellCastSpeedCapMax` / `Min` | 500.0 / [20, 30, 40] |
| `bossAttackSpeedCapMax` / `Min` | 500.0 / 50.0 |
| `bossSpellCastSpeedCapMax` / `Min` | 500.0 / 50.0 |
| `playerRunSpeedCapMax` / `Min` | 135.0 / 20.0 |
| `monsterRunSpeedCapMax` / `Min` | 500.0 / [20, 25, 30] |
| `bossRunSpeedCapMax` / `Min` | 500.0 / 40.0 |
| `absoluteRunSpeedCapMax` / `Min` | 350.0 / [40, 30, 20] |

**→ Player attack speed caps at 200 %, floors at 20 %. CONFIRMED.** Note the template
(T‑LEGACY) declares `playerAttackSpeedCapMax` as "Index by difficulty 0 to 2" but the shipped
value is a **scalar** — i.e. the cap is uniform across all three difficulties. **M.**

**Dual wield (M):** `gameengine.dwWeaponSpeedFactor = 0.5`, `gameengine.dwWeaponDamageFactor = 1.0`.

## E-3.4 Monster-side cadence — the KC1 opposition roster

Monsters do not use `timeBetweenAttacks`. Their cadence is **two fields**, both **M**:

1. `characterAttackSpeed` on the creature (an animation-rate multiplier, ~0.75 – 1.5), adjusted by
   `characterAttackSpeedModifier` and the pak's **−10 % on Normal only**
   (`balancingadjustment_mp+difficulty_enemies01.characterAttackSpeedModifier =
   [-10 ×4, 0 ×4, 0 ×4]` — **Elite and Ultimate carry no penalty**).
2. `minSwingPause` / `maxSwingPause` on the **controller** (`templatebase/controllermonster.tpl`,
   default `0` — T‑LEGACY), in **seconds**, an inter-swing idle. Reading: attack interval =
   (animation duration ÷ effective attack speed) + `U(minSwingPause, maxSwingPause)`. The
   *animation duration* term is **U** (asset side); the pause term is fully **M**.

| monster | record stem | `characterAttackSpeed` | controller | `minSwingPause` / `maxSwingPause` |
|---|---|---|---|---|
| Walking Dead | `zombie_a01` | 1.18 | `controller_zombiea01` | 0.45 / 1.00 |
| Wretcher | `zombie_b02h` | 1.05 | `controller_zombiea01h` | 0.50 / 1.00 |
| Plague Walker | `zombie_g01` | 1.05 | `controller_zombieburninga01` | 0.90 / 1.20 |
| Rotting Soldier | `zombie_soldiera01` | 1.15 | `controller_zombiea01` | 0.45 / 1.00 |
| Tainted Hound | `zombiehound_a01` | 1.25 | `controller_raptor` | 0.30 / 0.80 |
| Corruption (gazer) | `gazer_a01` | 1.20 | `controller_gazer` | 1.15 / 1.80 |
| Ghoul | `ghoul_a01` | 1.00 | `controller_ghoul01` | 0.20 / 0.50 |
| Stonetusk | `boar_a01` | 1.00 | `controller_wasp` | 0.10 / 0.60 |
| Gargantuan Stonetusk | `boar_a02` | 1.00 | `controller_wasp` | 0.10 / 0.60 |
| Scavenger | `scavenger_a01` | 1.00 | `controller_scavengermelee01` | 0.60 / 1.00 |
| Rifthound | `rifthound_swamp_a01` | 1.10 | `controller_raptor` | 0.30 / 0.80 |
| Cronley's Lackey | `humanoutlaw_melee_a01` | 0.85 | `controller_humanoutlaw_meleebasic` | 0.65 / 1.20 |
| Cronley's Gunman | `humanoutlaw_ranged_a01` | 0.85 | `controller_humanoutlaw_rangedbasic` | 1.05 / 1.70 |
| Bloodsworn Adulant | `humanchthonic_cultist_a01` | 0.75 | `controller_humanchthonic_meleebasic` | 0.35 / 0.90 |
| Scrapheap Rift Scourge | `prawn_a01` | 1.00 | `controller_prawn_melee` | 0.30 / 0.70 |
| Dreadweave Arachnid | `spidergianta_a01` | 1.15 | `controller_spider` | 0.10 / 0.50 |
| Boneback Gnasher | `bonerat_meleea01` | 1.10 | `controller_bonerat_melee` | 0.20 / 0.60 |
| Skeletal Warrior | `skeleton_a01` | 1.20 | `controller_zombiea01` | 0.45 / 1.00 |
| Fleshwarped Butcher | `zombiemutated_a01` | 1.30 | `controller_zombiemutanta01` | 0.50 / 1.10 |
| Fury | `zombie_c01` | 1.50 | `controller_zombiea01` | 0.45 / 1.00 |
| Ironhide Stonetusk | `boar_b01` | 1.00 | `controller_wasp` | 0.10 / 0.60 |
| **Dreadtusk** (hero) | `hero/boar_h01` | 1.00 | `controller_raptor` | 0.30 / 0.80 |
| **Abner** (hero) | `hero/zombie_h01` | 1.40 | `controller_zombiea01` | 0.45 / 1.00 |
| **Charrus** (hero) | `hero/rifthound_h01` | 1.20 | `controller_raptor` | 0.30 / 0.80 |
| **Igrixx, the Rimeheart** (hero) | `hero/slith_h01` | 1.00 | `controller_slith_melee` | 0.65 / 1.20 |
| **Warden Krieg** ph.1 | `boss&quest/warden01` | 1.05 (`weaponScale 1.3`) | `controller_boss_warden` | *(absent)* / 0.30 |
| **Warden Krieg** ph.2 | `boss&quest/warden02` | 1.20 (`weaponScale 1.3`) | `controller_boss_warden` | *(absent)* / 0.30 |
| **Primordian** | `boss&quest/slith_wightmirecave01` | **1.00** | `controller_boss_viloth` | **0.30 / 0.40** |
| Slith melee (trio) | `slitha_melee_b01` | 1.00 | `controller_slith_melee` | 0.65 / 1.20 |
| Slith shaman (trio) | `slitha_shaman_c01` | 0.75 | `controller_slith_ranged` | 1.05 / 1.60 |

All **M**. `characterAttackSpeedModifier = 0.0` on every roster entry — the only attack-speed
modifier in play on Normal is the pak's −10 %, plus, for Primordian, `primordian_icearmor`'s
**+35 %** during its 12-on / 32-off window.

**Note the boss anomaly (M):** `controller_boss_warden` declares **no `minSwingPause`** (field
absent, template default 0) with `maxSwingPause = 0.30`. Primordian's `controller_boss_viloth` has
the **tightest bounded pause in the roster (0.30–0.40 s)** — a nearly deterministic swing cadence,
where trash sits at 0.45–1.20 s. **This is the cadence signal M-4 should reproduce: boss swing
rhythm is low-variance, trash swing rhythm is high-variance.** The corpus-wide controller
pause census (probe9c, `database.arz`) shows the modal buckets are `0.30/0.80` (n=11),
`0.50/1.00` (n=10), `0.65/1.20` (n=9), `0.20/0.60` (n=8), `0.00/0.00` (n=20 — stationary/turret
controllers), `1.05/1.70` (n=6).

## E-3.5 Schema confirmations (T‑LEGACY, M)

```
controllermonster.tpl            minSwingPause              default='0'
controllermonster.tpl            maxSwingPause              default='0'
parameters_character.tpl         characterAttackSpeed       default='0'
parameters_character.tpl         characterBaseAttackSpeed   default=''
parameters_character.tpl         characterBaseAttackSpeedTag default='CharacterAttackSpeedAverage'
gameengine.tpl                   playerAttackSpeedCapMax    desc='Index by difficulty 0 to 2'
```

Neither `minSwingPause` nor `maxSwingPause` carries an authored description — the "seconds"
reading is **I**, supported by (a) magnitudes 0.1–3.0, (b) the sibling `specialAttackDelay`
description explicitly saying "Seconds", (c) the `combatIdleTime = 1.2` constant in the same units.

---

# Gaps — what I could NOT find

Every item here is a **U**. None of it has been improvised, and none of it should be.

| # | Gap | Why it is not in the corpus | Cheapest close |
|---|---|---|---|
| **G-1** | **Telegraph / windup duration for the nova (and for every monster special).** | Durations live in `.anm` binary assets. The Edition-II pin ships `database/*.arz` + `resources/Text_EN.arc` **only** — zero `.anm`, `.msh`, or `Creatures.arc`. Confirmed by exhaustive `find`. `skill_attackprojectilering.tpl` declares no timing field at all. | Either (a) re-pin the depot with the asset `.arc`s and write an `.anm` header parser — a NEW lane, my work, not the crawler's; or (b) **measure it off Matt's play-test capture** (frame-count the Roar-to-burst interval). (b) is cheaper and is a fixture the run already owns. |
| **G-2** | **Whether `specialAttackTimeout` is a global cross-slot gate or per-slot.** | Slot-1 description says "time out for **all** skill use"; slots 2–7 declare the same field with **empty** descriptions. Genuinely ambiguous. | Not closable from source. The M-2 spec must **name which reading it adopts**. Changes Primordian's nova cadence by ~2×. |
| **G-3** | **Base attack interval in seconds for a player or monster at 100 % speed.** | `characterAttackSpeed` is an animation-rate multiplier and `characterBaseAttackSpeed` a fractional offset; the baseline they multiply is the animation clip length — asset side. No DB record carries an interval for standard attacks. | Same as G-1(b): measure from capture, or adopt an explicit sim-side constant and label it a **calibration constant, not a GD value**. |
| **G-4** | **The resistance application operator (hard clamp at `playerDefenseCap` vs. soft).** | No equation in `combatformulas.dbr` mentions resistance. Only the cap constants exist. | Not closable from this corpus. Grade the M-1 spec's choice as **I**. |
| **G-5** | **Stacking rule for `damageAbsorptionPercent` / `offensiveTotalDamageModifier` / `defensiveTotalDamageModifier`.** | No formula record composes them. This is the **same unresolved clamp** the KC1 Primordian proto §3c held on — additive vs multiplicative moves output ~80 % at these ranks. | Unchanged from KC1. Still **U**. Do not compose. |
| **G-6** | **Exact monster armour absorption after `defensiveAbsorptionModifier −20`.** | Convention says `70 × 0.80 = 56 %`; literal subtraction says `50 %`. Source states neither. | Not closable. State the choice in the M-1 spec. |
| **G-7** | **Which of the two novas killed Matt at death-2.** | Both `primordian_frigidring` and `igrixx_frigidring` are live in the same Act-1 Wightmire content and fire the same `icebolt_nova` FX. Visually near-identical. | Decidable from the fixture trace **if** it carries a damage-source or monster-name label. Routed to gandalf; not adjudicated here. |
| **G-8** | **Whether `combatRegion*Chance` applies to monsters** (which have one `defensiveProtection`, not six slots). | The region weights are global in `combatformulas.dbr`; nothing scopes them to players. | **I:** for monsters `sumProtection` is slot-invariant, so the region roll is a no-op on the monster side and matters only for incoming player damage. Low risk; flagged rather than closed. |

---

# Records used (exact paths)

**Engine / formulas**
`records/game/gameengine.dbr` · `records/game/combatformulas.dbr` ·
`records/game/balancingadjustment_mp+difficulty_enemies01.dbr` ·
`records/game/balancingadjustment_mp+difficulty_players01.dbr`

**E-1 skills**
`records/skills/nonplayerskills/bossskills/{primordian_frigidring, primordian_wave, primordian_icearmor,
primordian_passive, primordian_arcticblast, boss_chest_01}.dbr` ·
`records/skills/nonplayerskills/heroskills/{chillbane_blizzard, igrixx_frigidring,
igrixx_chilledweapons, igrixx_chillingfront}.dbr` ·
`records/skills/nonplayerskills/bossskills/special/cloneice_icenova.dbr` ·
`records/skills/nonplayerskills/passive/{damage_totaladjuster, damagebase_physical03,
damagebase_physical04, armorbase03, armorbase05, resists_heroboss,
passiveproperties_herodeflection}.dbr` ·
`records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr`

**E-1 creatures / spawn / anim**
`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/creatures/enemies/hero/slith_h01.dbr` ·
`records/creatures/enemies/anm/anm_slith.dbr` ·
`records/proxies/pools/p_beasts_slith{a,b,c}_{t,vt,xhighhero}.dbr` ·
`records/proxies/pools/p_beasts_slitha_amb_s1_n.dbr` · `records/proxies/lv6_hero.dbr` ·
`records/controllers/enemy/{controller_boss_viloth, controller_slith_melee, controller_slith_ranged}.dbr`

**E-3 roster** — all 30 stems in the §E-3.4 table, under `records/creatures/enemies/` ·
their `controller` targets under `records/controllers/enemy/` ·
`records/creatures/pc/{malepc01, femalepc01}.dbr` ·
`records/items/gearhead/c001_head.dbr` (armour sample) ·
weapon census over all `records/items/**` with `Class` prefix `Weapon`

**Templates (T‑LEGACY — `~/Games/vendor/grim-dawn/database/templates.arc`, 819 entries)**
`skill_attackprojectilering.tpl` · `templatebase/monsterskillmanager.tpl` ·
`templatebase/controllermonster.tpl` · `gameengine.tpl` ·
`backup/parameters_character.tpl` · `templatebase/parameters_defensive.tpl`

**Localisation** — `{,gdx1/,gdx2/,gdx3/}resources/Text_EN.arc`, `tags*` files

**Probes** — `agentic_orchestration/legolas/scratch/2026-07-28-wr1/probe{1..11}*.py` with
outputs `p{1,2,5,6,7,8,9,10}.out`
