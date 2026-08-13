# GD hit math — OA vs DA, PTH, crit tiers, armour absorption

**Lap:** KC2-PM2 Lap B (task 2) · **Date:** 2026-08-12 · **Author:** legolas (UNKNOWN-RESEARCHER)
**Method:** every constant below was READ OUT OF THE CORPUS first (`records/game/combatformulas.dbr`,
`records/game/gameengine.dbr`, both `arz_owners = ['base']`, Edition-III on disk) and only then
compared against the public documentation. Nothing here is recalled from memory.
**Machine-readable twin:** `hit_math_constants.json` (this directory) — the raw field dump,
36 combat-formula keys + 19 engine keys, **zero ABSENT**.
**GL-17:** reference-study substrate for the private verification instrument only.

---

## 0 · Provenance grades used

| grade | meaning |
|---|---|
| **A / MEASURED×2** | present in the `.arz` AND independently confirmed by Crate's own published guide |
| **A / MEASURED** | present in the `.arz`; no independent confirmation sought or needed |
| **C / COMMUNITY** | not in the `.arz`; taken from documentation, flagged as such |
| **UNRESOLVED** | neither source settles it — named, never guessed (GL-12) |

Sources for the ×2 confirmations: Crate Entertainment's official gameplay guide,
<https://www.grimdawn.com/guide/gameplay/combat/> (accessed 2026-08-12). A Fandom-wiki
summary consulted on the same day **disagrees with both** the corpus and Crate's guide; see § 5.

---

## 1 · Probability to hit

```
PTH = ((((OA / ((DA / 3.5) + OA)) * 300) * 0.3)
     + (((((OA * 3.25) + 10000) - (DA * 3.25)) / 100) * 0.7))
     - 50
```

| item | value | field | grade |
|---|---|---|---|
| PTH equation | *(above, character-for-character as stored)* | `combatformulas.probabilityToHitEquation` | **A / MEASURED×2** |
| PTH floor | **55** | `combatformulas.pthMinimum` | **A / MEASURED×2** |

The stored equation uses the token names `offensiveAbilityDV` / `defensiveAbilityDV`; they are
renamed OA / DA above and nowhere else altered. Crate's guide publishes the identical expression.

`PTH` is a **percentage-like scalar that is allowed to exceed 100.** It is not clamped to 100 in
the data; the excess is what buys the crit tiers (§ 2).

## 2 · Crit tiers — the PTH ladder

| tier | threshold field | value | modifier field | value | grade |
|---|---|---|---|---|---|
| 1 | `pthThreshold1` | **70** | `pthDamageModifier1` | **1.0** | A / MEASURED×2 |
| 2 | `pthThreshold2` | **90** | `pthDamageModifier2` | **1.1** | A / MEASURED×2 |
| 3 | `pthThreshold3` | **105** | `pthDamageModifier3` | **1.2** | A / MEASURED×2 |
| 4 | `pthThreshold4` | **120** | `pthDamageModifier4` | **1.3** | A / MEASURED×2 |
| 5 | `pthThreshold5` | **130** | `pthDamageModifier5` | **1.4** | A / MEASURED×2 |
| 6 | `pthThreshold6` | **135** | `pthDamageModifier6` | **1.5** | A / MEASURED×2 |

*Float note (basis honesty):* the modifiers are stored as float32 and decode as
`1.100000023841858`, `1.2000000476837158`, `1.2999999523162842`, `1.399999976158142`. Those are
the exact bytes; the design intent is plainly 1.1 / 1.2 / 1.3 / 1.4. Use the design values and
say so, or use the bytes — do not silently mix.

### Sub-threshold damage scaling

```
normal_damage_multiplier = PTH / 70          # applies when PTH < pthThreshold1
```

| item | value | field | grade |
|---|---|---|---|
| divisor | **70** | `combatformulas.normalPTHEquation` = `probabilityToHitDV/70` | **A / MEASURED×2** |

### Resolution rule (how the constants are consumed)

Crate's guide states it as a single d100 roll against PTH, with the band above each threshold
being the crit band. Worked example published verbatim by Crate: *"PTH = 97, 1–89 hits, 90–97
critically hits for 1.1x damage, 98–100 misses."* At PTH ≥ 100 the attack cannot miss and further
PTH widens the higher-multiplier bands.

| item | grade |
|---|---|
| single-roll resolution + band semantics | **A / MEASURED×2 constants, C / COMMUNITY procedure** — the `.arz` stores the constants, not the resolution loop; the loop is Crate's published description |

## 3 · Where OA and DA come from

```
OA_effective = (OA_base + (charLevel * 12) + ((dexterity + bonus) * 0.5)) * (1 + OA_modifier_pct/100) + 53
DA_effective = (DA_base + (charLevel * 12) + ((strength   + bonus) * 0.5)) * (1 + DA_modifier_pct/100) + 53
```

| item | field | grade |
|---|---|---|
| OA composition | `combatformulas.offensiveAbilityEquation` | **A / MEASURED** |
| DA composition | `combatformulas.defensiveAbilityEquation` | **A / MEASURED** |

**Basis warning for the fight cell.** These are the *composition* equations. For the 169 roster
identities the base terms come from each creature's `characterAttributeEquations` → `bios/*.dbr`
(`characterOffensiveAbility`, `characterDefensiveAbility`), which are themselves `charLevel`
equations. Those are extracted at the roster's own level in **`tg2_monster_oa_da.csv`**
(this directory, **169/169 MEASURED**, no gaps) — columns `offensive_ability_base` /
`defensive_ability_base`, plus each creature's own flat/percent overrides and the granted-tree
passives that move OA/DA, listed but **not folded** (the fold order is gamora's ruling, not mine).

`tg2_monster_stats.csv` from the 2026-08-12 lap already carried `offensive_ability_at_level_min` /
`defensive_ability_at_level_min` at 169/169; the new file **reproduces those values exactly** and
adds the modifier/passive columns. There is no residual OA/DA gap.

## 4 · Mitigation constants (needed the moment monster damage lands on the player)

| item | value / expression | field | grade |
|---|---|---|---|
| armour absorption | **70 %** | `gameengine.armorDefensiveAbsorption` | **A / MEASURED×2** |
| physical, damage > armour | `(armour * (1 - absorption)) + (damage - armour)` | `combatformulas.physicalDamageDefenseEquationDGP` | A / MEASURED |
| physical, damage ≤ armour | `damage * (1 - absorption)` | `combatformulas.physcialDamageDefenseEquationDLEP` *(Crate's typo, preserved)* | A / MEASURED |
| shield, damage > shield block | `damage - (shieldDefense * (shieldAbsorption/100))` | `shieldDamageReductionEquationDGB` | A / MEASURED |
| shield, damage ≤ shield block | `damage * ((100 - shieldAbsorption)/100)` | `shieldDamageReductionEquationDLEB` | A / MEASURED |
| melee / projectile block chance | `blockChance + blockChanceModifier` | `meleeBlockEquation` / `projectileBlockEquation` | A / MEASURED |
| physical damage attribute scaling | `damage * ((dexterity/245) + 1)` | `physicalDamageEquation` | A / MEASURED |
| physical DoT attribute scaling | `damage * ((dexterity/215) + 1)` | `physicalDurationDamageEquation` | A / MEASURED |
| magical damage attribute scaling | `damage * ((intelligence/215) + 1)` | `magicalDamageEquation` | A / MEASURED |
| magical DoT attribute scaling | `damage * ((intelligence/200) + 1)` | `magicalDurationDamageEquation` | A / MEASURED |
| pierce damage attribute scaling | `damage * ((dexterity/245) + 1)` | `pierceDamageEquation` | A / MEASURED |
| player reflect cap | 30 | `gameengine.playerReflectCap` | A / MEASURED |
| damage magnitude / absorb scaling | 100.0 / 100.0 | `gameengine.damageMagnitude` / `absMaxDamageScaling` | A / MEASURED |
| hit-region chances (head/torso/shoulders/arms/legs/feet) | 15 / 26 / 15 / 12 / 12 / 20 | `combatRegion*Chance` | A / MEASURED |
| speed caps (monster / boss / player, attack + run + cast) | see `hit_math_constants.json` | `gameengine.*CapMin/Max` | A / MEASURED |

Read on the two physical branches: armour is a flat *protection* value; 30 % of any physical hit
gets through regardless (that is the `1 - 0.70`), and the portion above the armour value passes
undiminished. Both branch expressions are stored, so the branch selection is data, not inference.

## 5 · Contradiction surfaced — the wiki is stale

A Fandom "Game Mechanics" summary read on 2026-08-12 states a PTH floor of **60**, a
sub-threshold divisor of **75**, and a "base PTH is 90 %" framing. **All three disagree with the
shipped `.arz` (55 / 70) and with Crate's own current guide (55 / 70).** The `.arz` on disk is
first-party and current; the wiki text is almost certainly pre-patch. Recorded so nobody
re-derives from the wiki later and thinks the corpus is wrong.

## 6 · UNRESOLVED — named, not guessed

**SEM-1 · duration-damage storage semantics.** The corpus stores DoT as a value plus a duration
(`offensiveSlow<Type>Min` + `offensiveSlow<Type>DurationMin`). **Whether the value is the
per-second rate or the total over the duration is not declared anywhere on this disk.** What was
checked and what it gave:

- `database/templates.arc` → `templatebase/parameters_offensive.tpl`: the `DurationMin`/`DurationMax`
  variables carry `description = "Seconds"` (**MEASURED**); the `Min`/`Max` variables carry an
  **empty** description. The template does not say.
- `resources/Text_EN.arc`: the display strings are composed at runtime —
  `DamageDurationFire = " Burn Damage"` + `DamageSingleFormatTime = " over {%.1f0} Seconds"`.
  The number is substituted by the engine; the tag layer does not reveal which quantity.
  A separate tag `tagDurationDamageOverTime = "{%d0} Damage Every Second"` proves the engine has
  a per-second concept but does not bind it to this field.
- Public documentation: no source found that states the DBR storage convention (as opposed to the
  tooltip convention).

**Disposition (GL-12): both readings are emitted, neither is chosen.** `tg2_attack_damage.csv`
carries `dot_dps_if_field_is_per_second` (= the raw field) and `dot_dps_if_field_is_total`
(= raw ÷ duration) alongside `dot_duration_s`. The ambiguity is bounded and quantified: it
touches **718 of 4,722** damage rows (15.2 %); **716** of those carry a duration (range 1.0–12.0 s,
median **3.0 s**, modal 2.0 s) and the two readings differ by exactly that duration factor. The
remaining 2 rows carry a DoT value with no duration field and are graded `ABSENT` on
`dot_duration_s`. **gandalf/gamora rule SEM-1; I will not.**

---

*Every number above traces to a named field in a named record in a named archive. Where the
corpus is silent, this document says so rather than filling the hole.*
