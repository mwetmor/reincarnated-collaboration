# KC2-PM4 · Lap L · METHOD — THE PLAYER-OFFENSE DECODE

> **Run:** KC2-PM4 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Ruling:** **R-PM4-24** (charter row L-20)
> **Seat:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-14
> **Laws:** READ-ONLY on every source · **GL-12 decode-never-estimate** · **NOTE-9** every quantity
> asserts its own basis · **R-PM4-25** (LO/HI for monotone scalars only; structural unknowns take
> pre-registered mechanism candidates + a discriminator, or route) · **OUTCOME-FIREWALLED**.

---

## 0 — The firewall, stated precisely

This lap read **no** sim output, **no** gamora landing note, **no** baton, **no** wave-duration or
ToD or HP figure. It did not open `pm4k_*`, `pm4h2_*`, or any I-series findings JSON. Its substrate
is exhaustively:

| source | used for |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (8 `.arz`, `Text_EN.arc`) | every skill/item/engine magnitude |
| `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc` (sha256 `b8e6f510…bfa5`, 98,101 B) | allocations, devotions, **equipment** |
| `…/lap-a-player-sheet/measured-player-sheet.csv` | the camera-measured character sheet (corroboration surface **and** three run-of-record scalars) |
| `…/lap-d-roster-ehp/pm4d_band_b_ehp_by_wave.csv` | the (record, wave, level, eHP) board 151–170 |
| `…/lap-i-monster-offense/pm4i_band_c_ehp_by_wave.csv` | band C 171–180 |

**Nothing is fitted to any observed clear time.** The T3 span vector is this lap's judge, not its input.

**Instrument:** `agentic_orchestration/research/scripts/pm4l_emit_2026_08_14.py`.
Log `emit.log`; machine summary `pm4l_emit_summary.json`. Life/roster machinery is **imported, never
re-implemented** (`resolve`/`Chain`/`ev` from `gamora_kc2_c1_closure_ed3_2026_08_08`, `is_body` from
`pm4d_lib`, `survival_arrays`/`surv_at`/`difficulty_pak` from `pm4i_lib`, the `.gdc` reader from
`pm4g_lib`). Reader is `E3.winner()` — whole-record replacement (the L-33 / C-9 overlay law).

---

## 1 — ⚑ THE CLIFF THAT BIT TWICE, AND IS NOW CLOSED: the played save's EQUIPMENT ARRAY

Lap A declared cliff **C-4** and Lap G inherited it as **C-G6**: *blocks 3 (inventory) and 4 (stash)
are not parsed*, because those blocks carry **nested no-bump length ints** and Lap G's blanket u8
sweep reports `clean = False` on exactly those two blocks and no others (13/15 clean).

**It is closed here, by solving rather than guessing.** The observation:

* the true reader and the blanket sweep advance the key by the **same** rule, `key ^= t[raw]` per raw
  byte — so a *missed* no-bump int introduces a key error `D` that is **constant for the rest of the
  regime**;
* a `u8` read consumes only `key & 0xFF` — so **every byte of a desynced regime is the true byte
  XORed with ONE constant mask `m = D & 0xFF`**.

Recovery is therefore a 256-way search, and a candidate is accepted only if the whole path decodes
to the legal record charset and terminates in `.dbr`. **Block 3 partitions into exactly 7 mask
regimes** — one per nested sub-block — and the **last regime is the equipment array.**

**The falsifier, pre-named and passed:** the weapon slot must reproduce Lap A's *independently
camera-read* component and augment. It does, exactly — `records/items/materia/compa_sealmight.dbr`
(Seal of Might) and `records/items/enchants/b06a_enchant.dbr` (Potent Oleron's Fervor) — and the
medal slot's augment `records/items/enchants/runes/d203_rune.dbr` reproduces Lap G's independently
recovered `rush_d203 ← @14 = medal` binding.

**The equipment as PLAYED** (slot label assigned from the item record's own gear directory, never
from a positional guess):

| slot | base record | affixes | component | augment |
|---|---|---|---|---|
| head | `upgraded/gearhead/d028_head` (Warborn Visor) | `ad201_slowresist` | `compb_arcanediamond` | `c203a_enchant` |
| neck | `gearaccessories/necklaces/b201e_necklace` (Eldritch Nemesis) | `b_ar024_ar_f`, `a014b_ch_speedattack_03_je` | `compb_sealannihilation` | `b130a_enchant` |
| chest | `upgraded/geartorso/d026_torso` (Warborn Chestguard) | — | `compb_chainsofoleron` | `c104a_enchant` |
| legs | `gearlegs/b002e_legs` (Solael) | `b_ar007_ar_f`, `a007b_ch_att_all_10` | `compb_ancientarmorplate` | `c06a_enchant` |
| feet | `upgraded/gearfeet/d007_feet` (Windshear Greaves) | `ad201_slowresist` | `compa_spellscorchedplating` | `c14a_enchant` |
| hands | `gearhands/d206_hands` (Sandreaver Bracers) | — | `compa_restlessremains` | `c14a_enchant` |
| ring1 | `gearaccessories/rings/d110_ring` (Combustion Band) | — | `compa_runeboundtopaz` | `b126a_enchant` |
| ring2 | `gearaccessories/rings/b103e_ring` (Gargabol) | `aa009b_oamod_01`, `b_ar051_je_f` | `compa_bloodiedcrystal` | `b130a_enchant` |
| waist | `gearaccessories/waist/d108_waist` (Gladiator's Distinction) | — | `compa_spellscorchedplating` | `c203a_enchant` |
| shoulders | `upgraded/gearshoulders/d026_shoulder` (Warborn Pauldrons) | `ao14_oa` | `compb_livingarmor` | `c203a_enchant` |
| medal | `gearaccessories/medals/b016e_medal` (Harvoul the Earthshaker) | `b_ar024_ar_f`, `a028b_off_dmg%phys_09_je` | `compb_arcanespark` | `runes/d203_rune` |
| relic | `gearrelic/d114_relic` (Deathstalker) | completion `ao17a_oa` | — | — |
| **weapon** | `gearweapons/melee2h/d107_blunt2h` (**Gutsmasher**) | — | `compa_sealmight` | `b06a_enchant` |

**Warborn is a 3-of-4 set** (`records/items/lootsets/itemset_d025b.dbr`; head + chest + shoulders
equipped). Set arrays are read at index `pieces − 1 = 2`. This is load-bearing twice over (§ 2).

---

## 2 — ⚑ IS-L1: **EoR's effective rank is 20.** Both prior readings were wrong, in opposite directions

| surface | claim | what it missed |
|---|---|---|
| Lap A prose | "Gutsmasher grants +4 ranks" ⇒ **19** | the sheet's `+1 to all skills` |
| Lap G **IS-G1** | mastery bonuses only ⇒ **16** | the weapon's **skill-specific** augment |
| **this lap** | **20** | — |

The term IS-G1 dropped is on the Gutsmasher record itself and is unambiguous:

```
records/items/gearweapons/melee2h/d107_blunt2h.dbr        [archive gdx2]
  augmentSkillName2  = 'records/skills/playerclass09/eyeofreckoning1.dbr'
  augmentSkillLevel2 = 4
```

`augmentSkillName*` is the **skill-specific** grant (`augmentSkillName1 = savagery1`, level 4 — which
is precisely Lap A's separately-recorded `weapon_plus_savagery = 4`); it is a *different* field from
`augmentMasteryName1/2` (`playerclass01` Soldier +2, `playerclass03` Occultist +2), which is what the
sheet's `bonus_soldier_skills` / `bonus_occultist_skills` panel aggregates. IS-G1 read the mastery
row and concluded the skill row did not exist. **It does, and Lap A's CSV even carried it** —
row `weapon_plus_eye_of_reckoning = 4`, which IS-G1's own quotation omitted.

```
rank_effective = 15 (block 8, MEASURED) + 1 (bonus_all_skills, sheet frame 512)
               +  0 (bonus_oathkeeper_skills)  + 4 (augmentSkillLevel2, item record)  =  20
```

Legal: `skillMaxLevel = 16` is the **allocation** ceiling; `skillUltimateLevel = 26` is the ceiling
with bonuses. **20 ≤ 26 — check `L1-rank-ceiling` PASS.**

**What moves at rank 20 vs the IS-G1 rank 16** (`eyeofreckoning1.dbr`, `gdx2`):

| field | @16 | @20 | Δ |
|---|---:|---:|---:|
| `weaponDamagePct` | 39 | **43** | +4 pts (+10.3 %) |
| `offensivePhysicalMin` | 85 | **109** | +28 % |
| `offensivePhysicalMax` | 94 | **122** | +30 % |
| `offensiveFireMin` | 70 | **90** | +29 % (100 % converted to physical, § 3) |
| `skillManaCost` | 11 | **13** | +18 % |

**This is the first term of the very quantity R-PM4-24 was fired to find, and it was being read one
rank-band low by the run's own prior lap.**

---

## 3 — L1 · THE PER-HIT ARITHMETIC · `pm4l_eor_per_hit.csv` (42 rows)

### 3.1 Weapon damage, MEASURED — and one camera/table disagreement, reported not averaged

`d107_blunt2h.dbr`: `offensivePhysicalMin/Max = 144 / 740` — **EXACT** against Lap A's camera read
of the item tooltip (`weapon_base_damage 144-740`), two wholly independent surfaces. Check
`L1-weapon-base-vs-camera` PASS. Plus `offensiveBonusPhysicalMin/Max = 48 / 62`.

> **⚑ Reported, not averaged (charter law).** The weapon's conversions read
> `Chaos→Physical 50 %` and `Lightning→Physical 50 %` in the table; Lap A's camera read
> **55 %** and **46 %**. The table is a base record and the save's item carries a seed; whether the
> difference is affix roll, patch drift, or a camera misread is **not decidable from the corpus**
> and is carried as gap **D-L3**. Neither number is a physical-damage input for EoR (his output is
> already physical), so nothing in this lap rides on it.

### 3.2 The EoR-scoped skill modifiers — three active, one gated OFF

Gear declares `modifiedSkillName{i}` / `modifierSkillName{i}` pairs; three of them target EoR:

| source | record | what it gives EoR |
|---|---|---|
| Gutsmasher | `…/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr` | **+14 % weapon damage**, **Fire→Physical 100 %**, +330 bleed / 3 s, +50 % bleed mod, +100 % bleed duration |
| Warborn Visor | `…/upgradedgdx2/head_d028_eyeofreckoning.dbr` | **+12 % crit damage** |
| Sandreaver Bracers | `…/legendary/hands_d206_eyeofreckoning.dbr` | **+24 flat physical**, +210 bleed / 3 s |
| Warborn **set** | `…/upgradedgdx2/set_d025_eyeofreckoning.dbr` | **+5 % weapon damage — INACTIVE** |

The set modifier is gated by `itemSkillModifierControl = [0,0,0,1]` and the set's own
`augmentSkillLevel4 = [0,0,0,3]` (a further **+3 EoR ranks**) by the same 4-piece index. **He wears
three pieces.** Both are emitted `MEASURED-INACTIVE` rather than silently dropped — and the fourth
Warborn piece is worth `+5 % WD and +3 ranks` if any downstream question ever needs the counterfactual.

So **%WD at the run-of-record rank = 43 (skill) + 14 (Gutsmasher) = 57 %.**

### 3.3 ⚑ The channel cadence law — decoded, and the sheet contradicts itself

```
records/skills/playerclass09/eyeofreckoning1.dbr
  Class              = Skill_AttackRadiusSpin      (templates: skill_attackradiusspin.tpl
                                                    -> includes skillchanneled.tpl)
  timeBetweenAttacks = 200   int   "Time between hits to enemies along the path"
  duration           = 0.25        (channel re-arm; useResetsDuration = 1)
  skillTargetRadius  = 3.0   m
  rotationSpeedMultiplier = 0.35   "Multiplier applied to player rotation speed while skill is active"
  canUseWhileMoving  = 1           (positive control vs Lap G § 7 — reproduced, PASS)
```

`timeBetweenAttacks` is denominated in **0.8 ms quanta** (established at PE-1 across the whole
spin/beam family and re-cited here, not re-derived): `period@100 % AS = 200 × 0.0008 = 0.160 s`,
i.e. **6.25 hits/s at 100 % attack speed**, scaled by the attack-speed multiplier.

> **⚑ The sheet does not agree with itself, and both readings are carried.** Lap A's frame 511
> prints `Attack Speed 196 %` **and** `Attacks per second 2.66`, while frame 495 prints the item's
> `1.46` attacks/s. `2.66 / 1.46 = 1.8219`, not `1.96`. Attack speed is a **monotone scalar
> magnitude** — the one class for which **R-PM4-25 explicitly RATIFIES the LO/HI bracket** — so both
> are carried as limbs and neither is averaged:

| limb | AS multiplier | **hit period** | **hit rate** |
|---|---:|---:|---:|
| **LO** | 1.8219 (sheet's own APS ÷ item APS) | **0.087820 s** | **11.387 /s** |
| **HI** | 1.9600 (sheet's attack-speed stat line) | **0.081633 s** | **12.250 /s** |

**⚑ The HI limb is `0.081633 s` — the sim's own tick, to six decimals.** The engine's `TICK_S`
(0.08163) *is* one Eye-of-Reckoning hit at the sheet's stat-line attack speed. That is stated here
as an arithmetic identity between two independently-derived constants, and it is the cleanest
positive control in the lap.

There is **no separate revolution field**: `Skill_AttackRadiusSpin` declares no rotation-period,
`rotationSpeedMultiplier` is explicitly a *player-turning* multiplier per its own template
description, and the corpus carries no animation-cycle length. **"Revolutions per second" is
therefore not a decodable quantity; "damage ticks per second" is, and it is the one the damage rides
on.** Any visual revolution rate is gap **D-L4**, routed (a camera measure off Matt's video is the
named escalation — the same escalation Lap G named for Blitz).

### 3.4 The per-hit magnitude — what is decoded, and what is DECLARED

Decoded and emitted: rank, `weaponDamagePct` (skill + gear), skill flat physical min/max, skill
flat fire (100 % converted), gear EoR-scoped flat, bleed riders, weapon base and bonus damage,
conversions, mana per tick, cadence.

**DECLARED GAP D-L1 — the closed-form composition of those terms into the printed per-hit number
could not be reproduced from the corpus.** The game's own sheet prints
`Eye of Reckoning damage per hit = 43,691 – 59,761` (frame 511). Reconstructing it requires the
engine's rule for *which* flat damage enters the weapon-damage pool that `%WD` scales, and the
corpus declares no such rule; four candidate poolings were tried and none reproduces both the
magnitude and the 1.368 max/min ratio. **Per GL-12 the honest move is to take the measurement rather
than publish a reconstruction:** the run-of-record per-revolution *physical* magnitude is the sheet's
own `43,691 – 59,761`, graded `MEASURED-BY-CAMERA`, carried as a LO/HI pair (a monotone scalar
magnitude — legal). The tables supply everything the sheet does not print.

---

## 4 — L2 · THE MODIFIER STACK, AND ⚑ THE COMPOSITION LAW · `pm4l_modifier_stack.csv` (440 rows)

Composed from the save's **actual** allocations: 13 equipped items + their affixes + components +
augments, the Warborn 3-piece row, **55 devotion nodes**, every allocated passive/mastery/toggled
aura at its effective rank, the three `Skill_Modifier` records that ride always-on auras, and two
always-on item-granted skills. Every row carries its source record, the rank used, and the array
index.

**⚑ A block-8 correction, with its own falsifier.** Lap G read devotion allocation from
`devotion_level`; **285** rows carry a non-zero `devotion_level`. The allocation flag is
`rank_allocated`, and **exactly 55** devotion rows carry `rank_allocated == 1` — matching the sheet's
`devotion_points_spent = 55` **exactly**. Check `L2-devotion-count` PASS. `devotion_level` is the
node's own scale (1 for stars, 15–25 for bound Celestial Powers), not its allocation.

### 4.1 ⚑ THE LAW: the total-damage term is **ADDITIVE** with the type term, and it is worth **+337 %**

Two candidates were **pre-registered before the arithmetic ran**, with a measured discriminator
(R-PM4-25's required form for a structural unknown):

* **M-A (additive):** `sheet %type = Σ(type-specific) + Σ(offensiveTotalDamageModifier)`
* **M-B (multiplicative):** `damage = flat × (1+%type) × (1+%total)`, sheet prints only the type sum

**Discriminator:** on any damage type whose type-specific sum is *known and small*, M-A predicts
`sheet − table-sum` is the **same constant** for every such type; M-B predicts it is **zero**.

| type | sheet | table-sum | implied global term |
|---|---:|---:|---:|
| aether | 361 | 24 | **+337** |
| vitality | 361 | 24 | **+337** |
| cold | 447 | 110 (elemental) | **+337** |
| lightning | 447 | 110 (elemental) | **+337** |
| electrocute | 437 | 100 | **+337** |
| vitality decay | 337 | 0 | **+337** |
| acid/poison | 446 | 110 | +330 |
| pierce | 643 | 284 | +359 |
| fire | 814 | 404 | +410 |
| bleed | 1366 | 801 | +565 |
| trauma | 2407 | 1571 | +836 |
| **physical** | **3036** | **2059** | **+977** |

**M-A is confirmed on SIX independent damage types, EXACTLY, to the integer.** Check
`L2-composition-law-exact-count` PASS. M-B is falsified (it predicts 0). The rule the sim must use:

```
sheet_%type  =  Σ type-specific %  +  Σ offensiveTotalDamageModifier          [ADDITIVE, MEASURED]
damage       =  flat_of_that_type × (1 + sheet_%type / 100)
```

### 4.2 The residuals, declared rather than smoothed

* **D-L2a — the global term's own composition.** Inverting the sheet gives **337**; summing the
  tables gives **325**, a **12-point** residual. The chance-gated line
  (`b06a_enchant.offensiveTotalDamageModifier = 500` paired with
  `offensiveTotalDamageModifierChance = 10`) is **excluded by name** — including it would have
  over-shot by 488 and is exactly the class of error a "sum everything" pass makes.
* **D-L2b — physical/trauma/bleed/fire/pierce carry a further residual** (+640 / +499 / +228 / +73 /
  +22 over M-A) that the equipped-record walk does not reach. It is **type-shaped, not uniform**, so
  it is *not* another global term; the named candidates (affix rolls carried in the item seed rather
  than the base record, and buff/proc state at the capture frame) are **not decidable from the
  corpus**. **The consequence is ruled, not hidden: where the sheet prints a composed modifier, the
  SHEET governs** — it is the game's own arithmetic, camera-measured, and is a *measurement*, not an
  estimate. The table walk is published beside it so a consumer can see every term and its source.

Independently corroborated to within a point without any inversion: **crit damage** table 56 vs
sheet 57 (check PASS); **attack speed** table 118 vs sheet stat line 96 — reported, and it is the
same self-disagreement § 3.3 already brackets.

---

## 5 — L3 · TARGET MULTIPLICITY · `pm4l_target_multiplicity.csv` (14 rows)

**⚑ There is no target cap. The corpus declares no such field on this skill class.**
`skillTargetNumber`, `skillMaxTargets`, `numTargets`, `maxTargets`, `targetTypeMax`,
`skillTargetAngle` are **all MEASURED-ABSENT** on `eyeofreckoning1.dbr`. What *is* declared:
`targetingMode = 'Point'` (centred on the caster) and `skillTargetRadius = 3.0 m` — the latter equal
to the sim's `EOR_RADIUS_M`, unconverted, under the Lap-F display contract.

**Therefore multiplicity is purely GEOMETRIC and uncapped:** every body inside the 3.0 m disc is
struck by every tick. This is the structural property R-PM4-24 asked for, and it is the reason clear
rate is **density-dependent**:

```
bodies_struck_per_tick  =  |{ b : dist(player, b) ≤ 3.0 m + r_b }|          (uncapped, MEASURED-ABSENT cap)
```

The engine's own contact scalars ride beside it for the join: `meleeTargetDistance = 2.400` (= the
sim's `D_ENGAGE_M`) and `meleeAutoTargetDistance = 4.0`, both from `records/game/gameengine.dbr`.
Whether the disc test uses body centre or body radius is **not** declared — that is Lap F's
`r_b` surface, and it is left to the fold rather than invented here.

The allocated EoR modifier **Soulfire** (`eyeofreckoning2.dbr`, rank 13,
`SkillSecondary_AttackProjectileOrbiting`) is a *separate* orbiting projectile —
`skillProjectileNumber = 1`, `projectilePeriod = 0.20 s`, `projectilePiercingChance = 100 %`,
lightning damage 229 @13 — i.e. a second, slower, **pierce-everything** damage stream. It is emitted
and **not** folded into the physical per-tick figure.

---

## 6 — L4 · MONSTER-SIDE MITIGATION · `pm4l_mitigation_by_body.csv` (19,810 rows) · `pm4l_applied_damage_by_body.csv` (79,240 rows)

**937 bodies** across waves 151–180 (`is_body` filter, Lap D's), **790 distinct records** on the
reference band 151–160. **Zero named gaps** — every body resolved.

### 6.1 The defence chain, by exact parallel with the life chain

```
armor(record, L) = bio.defensiveProtection(L)  +  Σ_i  skill_i.defensiveProtection[ rank_i(L) ]
DA(record, L, w) = ( bio.characterDefensiveAbility(L) + Σ_i … + surv.characterDefensiveAbility[w-1] )
                   × (1 + (surv.characterDefensiveAbilityModifier[w-1] + ultimate…)/100)
res_T(record, L) = record.defensive<T>  +  Σ_i  skill_i.defensive<T>[ rank_i(L) ]     for the 10 types
```

Same reader, same `skillLevel{i}` equations, same wave-array law (fighting wave `w` reads the cell
**labelled** `w`, index `w−1`) that Lap D and Lap I already ratified.

### 6.2 ⚑ The armour law, verbatim from the game's own record

```
records/game/combatformulas.dbr                                            [archive base]
  physcialDamageDefenseEquationDLEP = physicalDamageDV * (1 - sumAbsorptionDV)
  physicalDamageDefenseEquationDGP  = (sumProtectionDV * (1 - sumAbsorptionDV))
                                      + (physicalDamageDV - sumProtectionDV)
records/game/gameengine.dbr
  armorDefensiveAbsorption = 70.0
```

i.e. **armour absorbs `absorption %` of the damage it covers, and everything above the armour value
passes through untouched.** Two branches, damage ≤ armour and damage > armour, both present.

> **⚑ This closes a Lap-A GAP with a measurement.** Lap A's sheet row `armor_absorption_pct` was
> filed `GAP — NOT CAPTURED … GD default is 70 % but that is NOT measured here (GL-12)`. It is
> measured now: `gameengine.armorDefensiveAbsorption = 70.0`. Check
> `L4-absorption-closes-lapA-gap` PASS. The per-hit-**location** split is also on the record and is
> carried for any future limb: head 15 / shoulders 15 / arms 12 / torso 26 / legs 20 / feet 12 = 100.

**Board distribution, waves 151–160** (`n = 7,900` body-waves): armour min 0 · median **991** ·
max 2,742; absorption **70.0 %** everywhere (no monster on this board carries
`defensiveAbsorptionModifier`); physical resist median **8 %**, p75 **25 %**.

> **⚑ DECLARED CLAMP (not silent).** 23 records carry `defensivePhysical = 500` (anomalies,
> tentacles, cluster-summons). Un-clamped, `(1 − res/100)` makes the applied damage **negative** —
> the first emission of this lap did exactly that, and it is banked as a self-caught defect. A
> resistance above 100 is **immunity**, not healing; no corpus field expresses the clamp, so the
> clamp is applied at 0, graded `DERIVED-CLAMPED:IMMUNE`, and flagged per row
> (`immune_physical`, 920 of 31,600 reference-band rows). Check `L4-no-negative-applied` PASS.

### 6.3 ⚑ THE HIT LAW — **this player cannot miss this board**

The two-slot law ratified at **C-I7-1**, applied with the player's camera-measured
`offensive_ability = 3259`:

```
PTH = ((((OA/((DA/3.5)+OA))*300)*0.3) + (((((OA*3.25)+10000)-(DA*3.25))/100)*0.7)) - 50
hit chance = normalPTHEquation = PTH / 70        pthMinimum = 55
crit tier from pthThreshold1..6 = 70 / 90 / 105 / 120 / 130 / 135
      ->  pthDamageModifier1..6 = 1.0 / 1.1 / 1.2 / 1.3 / 1.4 / 1.5
```

Board DA (waves 151–160) runs min 64 · median **844** · max **1,169**. Against OA 3,259 the PTH
range is **149.2 – 182.2** — **above the sixth and last threshold (135) on every body at every
wave.** Therefore:

* **hit chance = 1.0000 everywhere.** Check `L4-player-cannot-miss-this-board` PASS.
* the **maximum reachable** damage tier is the top one, ×1.5, on every body.

> **⚑ STRUCTURAL UNKNOWN, pre-registered candidates + routed (R-PM4-25 form).** The DBR gives the
> thresholds and the multipliers but **not the roll rule** that selects a tier on a given swing.
> Candidates: **M1** deterministic (highest threshold passed ⇒ always ×1.5); **M2** a roll banded by
> the thresholds ⇒ an expectation strictly between 1.0 and 1.5; **M3** a separate crit roll gated by
> the `+57 %` crit-damage stat. **No corpus field discriminates them.** Because the *quantity* they
> select is a **monotone scalar multiplier**, it brackets legally: every applied-damage row is
> emitted twice, `critLO = 1.0` and `critHI = 1.5`. **The tier rule itself is DECLARED-GAP D-L5 and
> is routed to the conductor** — it is worth a flat 50 % on the run's single most load-bearing term.

---

## 7 — L5 · THE COMPOSITION CHAIN

```
%WD_total(rank)          = eyeofreckoning1.weaponDamagePct[rank-1] + 14        [Gutsmasher; +5 more at 4pc]
rank                     = 15 + 1 + 4 = 20                                     [IS-L1]

raw_physical_per_tick    = 43,691 .. 59,761                                    [sheet, MEASURED-BY-CAMERA;
                                                                                the closed form is D-L1]
after_armor(b)           = raw <= armor_b ?  raw * (1 - 0.70)
                                          :  armor_b * (1 - 0.70) + (raw - armor_b)   [combatformulas]
applied(b)               = after_armor(b) * max(0, 1 - res_physical_b/100)            [clamp declared]
expected(b)              = applied(b) * hit_chance(=1.0) * crit_mult(1.0 .. 1.5)      [D-L5 bracket]

ticks_to_kill(b, w)      = eHP(b, w) / expected(b)                             [eHP from Lap D/I]
tick_period              = 0.087820 s (LO)  ..  0.081633 s (HI)                [§ 3.3 bracket]
bodies_per_tick          = k = |{b : dist <= 3.0 m}|                           [UNCAPPED, § 5]

clear_rate(bodies/s)     =  k / ( mean_b(ticks_to_kill) * tick_period )
```

### 7.1 The headline numbers

| quantity | reference band 151–160 |
|---|---|
| **applied physical per tick, per body** (post-armour, post-resist, non-immune) | **6,554 – 59,761** |
| **expected applied per tick** (× hit 1.0 × crit 1.0–1.5) | **6,554 – 89,642** |
| **tick rate** | **11.387 – 12.250 /s** |
| **target cap** | **none — MEASURED-ABSENT; geometric, radius 3.0 m** |
| **hit chance** | **1.0000, every body, every wave** |
| **ticks to kill one body** (LO damage / HI crit) | p5 1.33 · **median 7.62** · p75 11.95 · p95 53.24 · max 108.03 |
| **solo contact seconds per body** (median, at the LO tick rate) | **0.669 s** |

**A median body on the wave-151–160 board dies to about eight Eye-of-Reckoning ticks — two thirds of
a second of disc contact — and the player never misses it.** Because the disc is uncapped, `k` bodies
in the ring die in that same two thirds of a second, so the clear rate is **linear in local density**
and the term the run has never folded is exactly the term that carries the density.

### 7.2 What this lap explicitly does NOT rule

* **It does not compose a board total.** The per-body table has one row per `(record, wave)`; the
  *spawn multiplicities* that turn that into a board are Lap D/I's and gamora's fold. Summing this
  table would produce 5.18 × 10⁹ eHP, which is a **roster catalogue, not a board**, and publishing it
  as a board figure would be an invention. It is stated here so nobody makes that mistake downstream.
* **It does not choose a density policy.** `k` is a geometry-and-locomotion question (Laps F and J),
  not a decode.
* **It does not touch any observed clear time.** The T3 span vector judges this lap; it did not enter it.

---

## 8 — Verification hooks and positive controls (all PASS, 0 FAIL)

| check | result |
|---|---|
| `L1-rank-ceiling` | effective 20 ≤ `skillUltimateLevel` 26 |
| `L1-canUseWhileMoving-positive-control` | **reproduces Lap G § 7 clause 1** from this seat |
| `L1-weapon-base-vs-camera` | table 144–740 == Lap A camera 144–740 (**independent surfaces**) |
| `L2-composition-law-exact-count` | **6** damage types give the SAME global term 337 **exactly** |
| `L2-devotion-count` | 55 `rank_allocated==1` rows == sheet `devotion_points_spent` 55 |
| `L2-crit-damage-within-1pt` | table 56 vs sheet 57 |
| `L3-no-target-cap-field` | 4/4 candidate cap fields MEASURED-ABSENT |
| `L4-armor-law-source` | both branches present verbatim in `combatformulas.dbr` |
| `L4-absorption-closes-lapA-gap` | `armorDefensiveAbsorption = 70.0` — **Lap A's GAP closed** |
| `L4-two-slot-crit-law` | 6 thresholds + 6 multipliers + `pthMinimum` read |
| `L4-no-negative-applied` | min applied 6,553.65 after the declared immunity clamp |
| `L4-player-cannot-miss-this-board` | min PTH 149.2, `PTH/70` saturates at 1.0 |

**Further positive controls, cross-lap:** the equipment recovery reproduces Lap A's camera-read
weapon component **and** augment and Lap G's medal-slot rune binding; `skillTargetRadius = 3.0`
reproduces the sim's `EOR_RADIUS_M`; `meleeTargetDistance = 2.400` reproduces `D_ENGAGE_M`; the HI
tick period **0.081633 s** reproduces the sim's `TICK_S` to six decimals.

---

## 9 — Declared gaps and defects

| id | what | disposition |
|---|---|---|
| **D-L1** | The closed-form composition of `%WD × pool + flat` into the sheet's printed per-hit could not be reproduced; the engine's weapon-damage-pool rule is not in the corpus. | The **sheet's measured 43,691–59,761** is the run-of-record magnitude (LO/HI, monotone scalar). Every input term is still emitted. |
| **D-L2a** | Global total-damage term: inverted 337, table walk reaches 325 (−12). | Declared; the sheet governs. |
| **D-L2b** | Type-shaped residual on physical/trauma/bleed/fire/pierce (+640/+499/+228/+73/+22). | Declared; candidates named (seed-carried affix rolls, capture-frame buff state); **the sheet governs where it prints**. |
| **D-L3** | Weapon conversion percentages: table 50/50 vs Lap A camera 55/46. | Reported, **not averaged**. Not load-bearing for this build's output. |
| **D-L4** | Visual **revolutions** per second. `Skill_AttackRadiusSpin` declares no rotation period; `rotationSpeedMultiplier` is a *player-turning* field by its own template description. | **Not decodable.** Damage ticks (decoded) are the load-bearing cadence. Escalation if ever needed: camera measure off Matt's video. |
| **D-L5** | **The crit-tier ROLL rule** — thresholds and multipliers are on the record, the selection rule is engine-internal. | **ROUTED to the conductor.** Three candidates pre-registered (§ 6.3); bracketed `critLO 1.0 / critHI 1.5`; worth a flat **50 %** on the run's most load-bearing term. |
| **D-L6** | Whether the 3.0 m disc test uses body centre or body radius. | Left to the fold (Lap F's `r_b`); not invented here. |
| **IS-L1** | **Correction against Lap G's IS-G1 and Lap A's prose:** EoR effective rank is **20**, not 16 and not 19. | Adopted; § 2. |
| **IS-L2** | **Correction against Lap G:** devotion allocation is `rank_allocated`, not `devotion_level` (285 rows vs the true 55). | Adopted; verified against the sheet. |
| **IS-L3** | **Self-caught defect:** the first emission produced negative applied damage on 23 immune records. | Clamped, graded, flagged per row. |
| **C-G6 / C-4** | Lap A's and Lap G's inventory-block cliff. | **CLOSED** (§ 1) by constant-mask recovery, with a pre-named falsifier that passed. |

---

## 10 — Files and FULL digests

| file | rows | sha256 (all 64 hex) |
|---|---:|---|
| `pm4l_eor_per_hit.csv` | 42 | `120990d998ac23a4b2dadc134e0f5cf3e51a3f7f6eb34ee400d5e2531b26d5a8` |
| `pm4l_modifier_stack.csv` | 440 | `4d361ebe6045a6a6d4af4c477242dd01f7de42b43f5af430a5487913c238f1b0` |
| `pm4l_target_multiplicity.csv` | 14 | `9fc53083723ba47f88de063fa0977e38a0b4dfb419d56d0cd3d738bee78a102e` |
| `pm4l_mitigation_by_body.csv` | 19,810 | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` |
| `pm4l_applied_damage_by_body.csv` | 79,240 | `5a41ad7d8a9757782c2f54e7ea018bb8ade2bc81c57b64f3774dd9e42d9cee67` |

Machine summary: `pm4l_emit_summary.json` · log: `emit.log` ·
instrument: `agentic_orchestration/research/scripts/pm4l_emit_2026_08_14.py`.
