# KC2-PM4 · LAP X — THE MITIGATION-PIPELINE DECODE (both directions) — **FINDINGS**

> **Run:** KC2-PM4 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Commission:** `R-PM4-61 part 5`
> **Seat:** legolas (UNKNOWN-RESEARCHER) · **2026-08-15** · **READ-ONLY on every source**
> **Preregistration:** `PREREGISTRATION.md`, committed **ALONE and FIRST** at meta commit
> **`64eea319fef4def32431d4f4821e686941c35e4c`**, before any Lap-X instrument existed.
> **Laws carried:** Law 3 NO tuning (referent numbers are GRADES, never inputs) · GL-12
> decode-never-estimate · NOTE-9 basis-per-quantity · R-PM4-25 · R-PM4-27 part 3 (both limbs at a
> fork, never picked by grade) · R-PM4-29 · R-PM4-55 · R-PM4-56 part 4 (new mechanisms NAMED, not
> decoded) · `NOTE D-V2-1` (no vtable base trusted) · **all standing DO-NOT blocks from Laps V,
> V-2 and W remain binding.**

---

## § 0 — THE HEADLINE

**The whole mitigation stack is in the corpus, verbatim, and the engine evaluates it by variable
name — so the `.dbr` equations are the implementation, not a description of it.** All 31 pipeline
field names and all 11 equation-variable names (`sumProtectionDV`, `sumAbsorptionDV`,
`blockChanceModifierDV`, …) resolve as strings inside `Game.dll` and **none** inside `Engine.dll`.

**And the decode says the intake seam is not where the referent's survival lives.** A median
band-A body on the wave-151 board lands **478 HP** of applied damage per attack round against a
20,005 pool — **2.4 % of the pool per body per round**. The board figure is *linear in the number
of bodies in melee contact*, and **this lap does not decode that count** — it is named
`UNREACHED-X-3` and handed to I-23 as the multiplier, not folded as a number.

**And the armour — all 3,557 of it, absorbing 98–100 % — is almost irrelevant to this board.** On the
worked example (§ 7) the armour stack turns a 1,612-point physical line into **17.6** applied, while
the same attack's lightning line, which armour never touches, delivers **451.8** through an at-cap
80 % resistance. **96.2 % of a run-of-record band-A hit arrives on damage types armour cannot see.**

**Three things the commission asked for do not exist in this build, and the reasons are records:**
shield block is **DECODED-ABSENT** (two-handed weapon; the game's own sheet prints 0/0/0), and
**`Overguard` is not in the allocation at all** — the commission named it, the played save does not
carry it. Both are reported as **commission-premise corrections**, and § 0.1 discloses that I knew
both before I preregistered.

**Four pre-registered predictions passed, four failed, one is UNREACHED, and the two that failed
hardest are the two I bet on hardest.** `P-X-4b` bet the sheet's Armor Rating was the SUM of the
six pieces; it is the **hit-weighted AVERAGE** (reconstruction lands −2.59 % of the camera-read
3,557 against a SUM model that overshoots by ×4.26). `P-X-5c` bet the band-A roster carries resist
reduction; it carries **none** — zero `offensive*ResistanceReduction*` rows across both censused
waves. Both losses are reported as losses and neither prediction's wording has been rewritten.

---

### 0.1 ⚑ SCOPING DISCLOSURE, CARRIED FORWARD FROM THE PREREG

`PREREGISTRATION.md § 0.2` lists exactly what I had read before writing the prereg. The
consequences that bind this note:

* **`T-C` (block) and the `Overguard` clause of `T-D` are PREREG-SIGHTED, not discoveries.** I knew
  from Lap A's sheet and Lap G's kit census that the build is two-handed and `Overguard`-free.
  `P-X-3` was therefore written as a *falsifiable confirmation with a named falsifier*, and is
  graded that way in § 6.
* Everything in `P-X-1`, `P-X-2`, `P-X-4`, `P-X-5` was genuinely uncomputed at prereg time.

---

## § 1 — THE HEADLINE TABLE

| # | target | verdict | key number |
|---|---|---|---|
| **T-A** | armour absorption | **DECODED** — two branches verbatim; **per-hit-region**, not aggregate | absorption **70.0 %** base, **98–100 %** on this build; regions 15/15/12/26/20/12 |
| **T-A′** | sheet Armor Rating semantics | **DECODED — it is the hit-weighted AVERAGE** (my SUM bet lost) | recon **3,465.0** vs camera **3,557** = **−2.59 %** |
| **T-B** | resistance caps + order | **caps DECODED; ORDER UNREACHED — both limbs published** | `playerDefenseCap` **80/80/80**, `monsterDefenseCap` **100/100/100** |
| **T-B′** | monster-side resist reduction | **DECODED-ABSENT on the censused roster** | **0** `*ResistanceReduction*` rows; **1** damage-reduction debuff (w160 Korvaak, −50 % for 5 s) |
| **T-C** | shield block | **DECODED-ABSENT** | chance 0 / amount 0 / recovery 0 (camera); `defensiveBlock` = 0 everywhere in the build |
| **T-D** | defensive procs, record-truth | **DECODED, 21 rows, no uptime modelled** | `Ascension` = **30 FLAT** absorb, not 30 % (UI-string discriminated) |
| **T-E1** | intake operand | **DECODED at per-skill grain**, 374 rows | board **11,882 HP/round** at 28-in-contact; **478 HP/body/round** median |
| **T-E2** | kill-rate operand | **DECODED** | full-vector median **6.317** ticks/body ⇒ **1.80–2.16 bodies/s** solo |

**Pre-registered predictions:** `P-X-1a` **FAILED** · `P-X-1b` **PASSED** · `P-X-1c` **FAILED** ·
`P-X-2a` **PASSED** · `P-X-2b` **PASSED** · `P-X-3a` **PASSED** · `P-X-4a` **PASSED** ·
`P-X-4b` **FAILED** · `P-X-5a` **PASSED** · `P-X-5b` **UNREACHED (order)** / PASSED (type scope) ·
`P-X-5c` **FAILED**.

---

## § 2 — T-A · THE ARMOUR LAW

### 2.1 The formula, verbatim from the game's own record

```
records/game/combatformulas.dbr                                       [archive: base]
  physcialDamageDefenseEquationDLEP = physicalDamageDV * (1 - sumAbsorptionDV)
  physicalDamageDefenseEquationDGP  = (sumProtectionDV * (1 - sumAbsorptionDV))
                                      + (physicalDamageDV - sumProtectionDV)

  combatRegionHeadChance            = 15      combatRegionTorsoChance = 26
  combatRegionShouldersChance       = 15      combatRegionLegsChance  = 20
  combatRegionArmsChance            = 12      combatRegionFeetChance  = 12
  combatRegionFullyProtectedChance  = 0       combatRegionUnprotectedChance = 0     [Σ = 100]

records/game/gameengine.dbr
  armorDefensiveAbsorption          = 70.0
  defaultCombatManagerRecord        = records/game/combatformulas.dbr
```

Read it plainly: **armour absorbs `absorption %` of the damage it *covers*; every point of damage
above the armour value passes through untouched.** Two branches, `damage ≤ armour` (DLEP) and
`damage > armour` (DGP). Lap L decoded the same two branches on the monster side; this lap
establishes that the *same two branches* are the player side, from the same record, and that the
record is the `defaultCombatManagerRecord` for both actors.

### 2.2 ⚑ WHICH DAMAGE TYPES — armour is **PHYSICAL ONLY** (`P-X-5b` type-scope PASSED)

`combatformulas.dbr` declares **exactly two** damage-defence equations and both name
`physicalDamageDV`. There is no fire, cold, lightning, poison, aether, chaos, pierce, vitality or
bleeding armour equation anywhere in the record. **Armour does not touch nine of the ten damage
types.** Everything else answers only to resistance.

### 2.3 ⚑ PER-PIECE, NOT AGGREGATE (`P-X-4a` PASSED)

`combatRegion*Chance` summing to exactly 100 over six regions, against a build with exactly six
armour-bearing slots, is a **hit-location roll**. The armour that enters `sumProtectionDV` on a
given hit is **the armour of the piece covering the rolled region** — not the sheet number.

| slot | region field | flat `defensiveProtection` | local % | after global +56 % | region chance | absorption (ADDITIVE limb, clamped) |
|---|---|---:|---:|---:|---:|---:|
| chest | `combatRegionTorsoChance` | 1,908 | 0 | **2,976.5** | 26 % | 98.0 % |
| legs | `combatRegionLegsChance` | 1,501 | 8 | **2,528.9** | 20 % | **100.0 %** |
| head | `combatRegionHeadChance` | 1,666 | 0 | **2,599.0** | 15 % | 98.0 % |
| shoulders | `combatRegionShouldersChance` | 1,666 | 0 | **2,599.0** | 15 % | **100.0 %** |
| feet | `combatRegionFeetChance` | 1,105 | 0 | **1,723.8** | 12 % | 98.0 % |
| hands | `combatRegionArmsChance` | 1,104 | 0 | **1,722.2** | 12 % | 98.0 % |

Global flat armour **+636** (waist 96, ring-2 component 75, `defensiveBonusProtection` 120 Warborn
3pc + 35 legs component, devotions 310). Global % armour **+56** (Field Command 22 @rank 14,
devotions 8 + 10, Gladiator's Persistence 8, Presence of Might 8). Full per-source provenance —
175 rows — in `pm4x_player_defense_terms.csv`.

### 2.4 ⚑ THE SHEET IS THE AVERAGE, AND I BET IT WAS THE SUM (`P-X-4b` **FAILED**)

Five candidate models were computed and all five are published. The camera-read sheet value is
**3,557**.

| model | value | residual vs 3,557 |
|---|---:|---:|
| `M-SUM-PLUS-GLOBALFLAT` | 15,141.5 | **+11,584.5** |
| `M-SUM-PIECESONLY` | 14,149.3 | +10,592.3 |
| `M-SUM-FLAT-ONLY` | 8,950.0 | +5,393.0 |
| **`M-AVG-PLUS-GLOBALFLAT`** | **3,465.0** | **−92.0 (−2.59 %)** ← winner |
| `M-AVG-GLOBALFLAT-UNSCALED` | 3,108.9 | −448.1 |
| `M-AVG-PIECESONLY` | 2,472.9 | −1,084.1 |

`M-AVG-PLUS-GLOBALFLAT` = `(Σ_s w_s · piece_s(after local %) + global flat) × (1 + global %/100)`,
with `w_s` the region chances. **I pre-registered SUM. SUM is wrong by a factor of 4.26. The
prediction's wording is not rewritten.**

> **⚑ THE RESIDUAL IS NAMED, NOT SWEPT.** −92 armour (−2.59 %) is unexplained. Solving the winner
> model for the global-% term that would close it gives **+60.1 %** against the **+56 %** the census
> reaches, so the deficit is ≈ **4 percentage points of global armour** from a source this census
> does not reach. `UNREACHED-X-1`, OPEN. **DO NOT close it by adjusting a term.**

### 2.5 ⚑ ABSORPTION IS AT OR NEAR ITS CEILING ON THIS BUILD — and the ceiling is DECLARED, not read

The build carries `defensiveAbsorptionModifier` **+48** total: legs component 8 (local), shoulders
component 12 (local), Warborn 3pc 10 (global), **Scars of Battle** rank 5 = 18 (global).

| composition limb | head/chest/feet/hands | legs | shoulders |
|---|---:|---:|---:|
| **ADDITIVE-POINTS** `70 + mods` | 98.0 | 106.0 → **clamped 100** | 110.0 → **clamped 100** |
| **MULTIPLICATIVE** `70 × (1 + mods/100)` | 89.6 | 95.2 | 98.0 |

**No corpus field expresses the clamp.** It is applied at 100 and graded `DERIVED-CLAMPED:CEILING`,
exactly the treatment Lap L § 6.2 gave the resistance clamp. **Both composition limbs are
published; the fold must carry both** (`R-PM4-27 part 3`). Under either, the player absorbs
**≈90–100 % of every physical point up to ~1,700–2,980 depending on which body part is hit.**

### 2.6 The attacker-level interaction — NAMED, not a modifier on armour

`gameengine.dbr : monsterLevelGapFixer = [0, 5, 7]`, template description *"Index by difficulty 0 to
2 — adds to monster level"*. On Ultimate (index 2, from the played save's difficulty byte) it adds
**+7 to monster level**. **It is not an armour term.** It is an upstream level shift that would move
every level-indexed monster array. **`R-PM4-56 part 4`: NAMED, not decoded, not folded** — folding
it would move the whole eHP and damage substrate on a term this lap did not measure through.

---

## § 3 — T-B · THE RESISTANCE PIPELINE

### 3.1 Caps (`P-X-5a` **PASSED**)

```
records/game/gameengine.dbr
  playerDefenseCap  = [80.0, 80.0, 80.0]      # index by difficulty 0..2
  monsterDefenseCap = [100.0, 100.0, 100.0]
  playerReflectCap  = 30.0
```

The referent build is on **Ultimate = index 2 ⇒ cap 80**. The Lap-A sheet reads **80** on
**eight** types (fire, cold, lightning, acid/poison, pierce, vitality, aether, chaos) — the player
sits **exactly at cap** on all eight. Bleeding reads **85** (above the base cap — the build carries
`defensiveBleedingMaxResist = +5` from Gladiator's Distinction, which raises the cap for that one
type; measured in the census). Physical reads **16**, far below cap and the type armour covers.

**Monster resistances cap at 100, not 80** — which is exactly why Lap L's 23 records with
`defensivePhysical = 500` are *immune*, not healing, and why the clamp Lap L declared is the right
one.

### 3.2 ⚑ THE ORDER IS **UNREACHED**, AND BOTH LIMBS ARE PUBLISHED (`P-X-5b` order)

No record field expresses whether armour is applied before or after resistance. `Game.dll` carries
both equations by name but the call order is not readable by string residency, and `NOTE D-V2-1`
forbids me trusting a vtable base to find it. **This is a fork; I refuse to pick it by grade.**

**Worked numerically on one 5,000-point physical hit** against aggregate armour 3,557, absorption
70 %, physical resist 16 %:

```
ARMOUR then RESIST:  DGP(5000, 3557, .70) = 3557*0.30 + (5000-3557) = 2510.1
                     × (1 - 0.16)                                    = 2108.484
RESIST then ARMOUR:  5000 × (1 - 0.16)                               = 4200.0
                     DGP(4200, 3557, .70) = 3557*0.30 + (4200-3557)  = 1710.100

                     Δ = 398.384  —  18.9 % of the smaller limb
```

**Every intake number in this note is computed ARMOUR-then-RESIST**, which is the *larger* (more
conservative-against-the-player) limb and the order Lap L already used on the monster side; the
other limb is published here so I-23 can carry both. `UNREACHED-X-4`.

### 3.3 ⚑ MONSTER-SIDE RESIST REDUCTION: **NONE** (`P-X-5c` **FAILED** — my bet lost)

The full `offensive*ResistanceReduction*` census (six families × Min/Chance/Duration/Global/XOR)
over every skill in the closure of every record rolled at waves **151** and **160**:

| family | rows found |
|---|---:|
| `offensiveTotalResistanceReductionAbsolute` | **0** |
| `offensiveTotalResistanceReductionPercent` | **0** |
| `offensiveElementalResistanceReduction*` | **0** |
| `offensivePhysicalResistanceReduction*` | **0** |
| **`offensiveTotalDamageReductionPercent`** | **2** (the same skill, both level limbs) |

**I predicted at least one true resistance-reduction field and there are none.** The player's 80s
are, on this roster, the whole story.

**What the census found instead is a KILL-RATE-side term, not an intake-side one:**
`statue_korvaaktombguardian.dbr` → `tombguardian_celestialbreath.dbr` @ rank 27 carries
`offensiveTotalDamageReductionPercentMin = 50.0`, `DurationMin = 5.0 s`, `Global = False`,
`XOR = False`, **wave 160 only**. That is a **−50 % player damage output debuff for 5 s on the
referent's death wave.** It is reported, not folded — the debuff's application semantics
(uptime, refresh, stacking) are I-23's, and its `Chance` field reads 0.0, which is itself a
structural question I do not resolve (`UNREACHED-X-5`).

---

## § 4 — T-C · SHIELD BLOCK: **DECODED-ABSENT**, and precisely why

### 4.1 The equations exist and are complete

```
records/game/combatformulas.dbr
  meleeBlockEquation                = (blockChanceDV + blockChanceModifierDV)
  projectileBlockEquation           = (blockChanceDV + blockChanceModifierDV)
  shieldDamageReductionEquationDLEB = damageDV * ((100 - shieldAbsorptionDV) / 100)
  shieldDamageReductionEquationDGB  = damageDV - (shieldDefenseDV * (shieldAbsorptionDV / 100))
records/resources/Text_EN.arc :: tags_ui.txt
  ShieldBlockRecoveryTime = {%.2f0} second Block Recovery
```

> **⚑ WHAT BLOCK APPLIES TO, DECODED FROM THE EQUATION SET, NOT FROM LORE.** There are **exactly
> two** block equations — `melee` and `projectile` — and they are **character-identical**. There is
> **no** `spellBlockEquation`. So block covers melee attacks and projectiles at the same chance, and
> **non-projectile spell damage is not blockable.** That is a first-of-kind statement for this run
> and it is readable straight off the record.

### 4.2 This build blocks nothing (`P-X-3a` **PASSED**; the named falsifier did **not** fire)

The prereg's falsifier named four fields: `defensiveBlock`, `defensiveBlockChance`,
`blockAbsorption`, `blockRecoveryTime`. **A census of all 13 equipped items + affixes + components +
augments + the Warborn set + every allocated skill + every allocated devotion returns ZERO non-zero
rows on all four.** The game's own sheet agrees: `chance_to_block 0`, `damage_blocked 0`,
`block_recovery 0`. Cause: `records/items/gearweapons/melee2h/d107_blunt2h.dbr` (Gutsmasher)
occupies both hands, so no shield record can contribute `defensiveBlock`.

> **⚑ AND THE CENSUS FOUND THREE BLOCK-FAMILY *MODIFIERS*, WHICH I REPORT RATHER THAN SUPPRESS.**
> `defensiveBlockAmountModifier` +8 (ring-1 component) and **+40** (Haven, `presenceofvirtue2` @rank
> 10), and `defensiveBlockModifier` **+10** (Haven). None is one of the four named fields, so the
> falsifier is correctly not fired — but `meleeBlockEquation` is written **additively**
> (`blockChanceDV + blockChanceModifierDV`), which on its face would let a modifier produce block
> chance from nothing. **The discriminator is the camera:** the game itself computed and printed
> **0**. The modifiers are therefore gated on a shield being equipped, or `defensiveBlockModifier`
> is not `blockChanceModifierDV`. **I do not resolve which** — `UNREACHED-X-6`. The *outcome* is
> decided (block is absent) by the game's own display; only the *mechanism of the zero* is open.

### 4.3 `Menhir's Will` — decoded, and it is **not** a shield skill

`records/skills/playerclass01/willtolive1.dbr`, class `Skill_PassiveOnLifeBuffSelf`, rank **5**
(allocated 1 + all-skills 1 + Soldier 3):

| field | value |
|---|---|
| trigger | `LowHealth` at **33.0 %** |
| `skillActiveDuration` | **10.0 s** |
| `skillCooldownTime` | **21.0 s** |
| `characterLifeRegen` | **+120.0 HP/s** |
| `skillLifePercent` | **35.0 %** |

It is a **low-health circuit breaker**, not a block passive. **Uptime is NOT modelled here** — the
commission assigns it to I-23 and these are per-activation record-truths.

### 4.4 ⚑ COMMISSION-PREMISE CORRECTIONS (`R-PM4-29` basis carried)

Two, both reported and neither executed as written:

1. **`R-PM4-61 part 5 (c)` calls shield block "the Warlord's load-bearing defensive layer."** For
   *this* referent build it is **not a layer at all**. The premise is true of Warlords generally and
   false of `EoRWarlGuts`. **Basis:** Lap A frame 519 (camera) + this lap's equipment census.
2. **`R-PM4-61 part 5 (d)` names `Overguard`.** `Overguard` is **absent from the played save's
   allocation** — the full Soldier/Oathkeeper allocation is 28 skills and `Overguard` is not among
   them. **Basis:** `pm4g_played_kit.csv` (325 rows, digest pinned in `PREREGISTRATION.md § 1.3`),
   independently re-read here. The defensive-active set that *does* exist is § 5.

Both were **prereg-sighted** (§ 0.1) and are reported as corrections, not as findings.

---

## § 5 — T-D · THE DEFENSIVE PROCS, RECORD-TRUTH ONLY. **NO UPTIME.**

21 rows in `pm4x_defensive_procs.csv`. The load-bearing ones:

| skill | class | rank | trigger | magnitude (record-truth) | duration | cooldown |
|---|---|---:|---|---|---:|---:|
| **Ascension** | `Skill_BuffSelfDuration` | 2 | manual | `damageAbsorption` = **30 (FLAT)** | 10.0 s | 24.0 s |
| **Turtle Shell** (devotion `tier1_29e`) | `Skill_BuffSelfShield` | 25 | `LowHealth` 50 %, 100 % chance | `damageAbsorption` = **6,100 (FLAT)** | — | 8.0 s |
| **Arcane Barrier** (devotion `tier2_17c`) | `Skill_BuffSelfShield` | 20 | `HitByEnemy` 30 % | `damageAbsorption` = **2,900 (FLAT)** | — | 3.0 s |
| **Menhir's Will** | `Skill_PassiveOnLifeBuffSelf` | 5 | `LowHealth` 33 % | `characterLifeRegen` +120 · `skillLifePercent` 35 | 10.0 s | 21.0 s |
| **War Cry** | `Skill_AttackRadius` | 16 | manual | `offensiveTotalDamageReductionPercentMin` = **29 %** (radius 18.0 m @rank 16) | — | 7.5 s |
| **Field Command** | `SkillBuff_Passive` | 14 | always-on aura | `defensiveProtectionModifier` **+22 %** · `characterDefensiveAbility` +100 | — | — |
| **Presence of Might** | `Skill_BuffSelfToggled` | 1 | toggled | `defensiveProtectionModifier` **+8 %** | — | — |
| **Divine Mandate** | `Skill_BuffSelfToggled` | 13 | toggled | `defensiveTotalSpeedResistance` +26 | — | — |
| **Maul** (devotion payload) | `SkillBuff_Debuf` | 20 | `AttackEnemy` 20 % | `defensiveProtectionModifier` **−35 %** *on the enemy* | 5.0 s | — |
| **Assassin's Mark** (devotion payload) | `SkillBuff_Debuf` | 25 | `AttackEnemyCrit` 100 % | `defensivePhysical` **−32** *on the enemy* | 18.0 s | — |

### 5.1 ⚑ `damageAbsorption` IS FLAT, AND THE DISCRIMINATOR IS A SHIPPED STRING

The template declares `damageAbsorption` with **no description**, so the flat-vs-percent question is
not resolvable from the schema. It is resolvable from the shipped UI:

```
resources/Text_EN.arc :: tags_ui.txt
  SkillDamageAbsorption        = {%.0f0} {^E}Damage Absorption          ← NO percent sign
  SkillDamageAbsorptionPercent = {%.0f0}% {^E}Damage Absorption         ← the percent one
```

Two distinct fields, two distinct format strings, one with a `%` and one without. **`Ascension` at
rank 2 grants a 30-point flat absorb, not 30 % mitigation** — which is 0.15 % of a 20,005 pool, and
anyone modelling it as 30 % would hand the player a defensive layer the records do not give him.
The rank array confirms the reading: `[20, 30, 40, … 290]` for Ascension vs `[500, 700, … 6100]` for
Turtle Shell — both flat pools, different scales.

**The two constellation shields are the real absorb layer: 6,100 + 2,900 = 9,000 flat**, i.e. 45 %
of the pool, gated on `LowHealth 50 %` (100 % chance, 8 s cd) and `HitByEnemy 30 %` (3 s cd).
**Their uptime is I-23's and is not modelled here.**

---

## § 6 — T-E · THE OPERANDS, BOTH DIRECTIONS

### 6.1 ⚑ THE ROW GRAIN IS THE FINDING — and my first build got it wrong

`pm4x_monster_offense.csv` is **one row per `(record, level-limb, SKILL)`** — 374 rows, 178 carrying
damage, across the 13 records rolled at w151 and the 4 at w160.

> **⚑ `D-X-1` — MY OWN DEFECT, CAUGHT BEFORE ANY GRADE WAS COMPUTED.** The first build of this
> instrument **summed the whole skill closure** into one per-record damage figure. That is an
> over-read by the size of the closure: a monster fires **one** skill on an attack round, not all of
> them. It produced a wave-151 board of **42,947 HP per round** — 2.1× the player's entire pool from
> a board he demonstrably survived. **The repair is the row grain, not a coefficient.** Disposition
> in § 8.

Because the corpus does not declare a skill-**selection** policy, three limbs are published and the
consumer chooses explicitly:

| limb | definition | w151 board / round | w160 board / round |
|---|---|---:|---:|
| `DEFAULT` | only the record's declared `attackSkillName` | **5,399.0** | 3,128.5 |
| **`RUNREC`** | `attackSkillName` where declared (5 of 13 w151 records); the closure's deepest hitter where not | **11,881.7** | **3,128.5** |
| `MAX` | the single deepest hitter, always | 12,245.8 | 14,972.4 |
| `SUMALL` | every damaging skill at once — a strict upper bound, **not physical** | 22,369.5 | 33,020.8 |

**Skill selection among the non-default skills is an AI/cooldown policy that lives in the engine,
not the corpus. `R-PM4-56 part 4`: NAMED, not decoded, not folded** (`UNREACHED-X-7`).

### 6.2 The intake side — damage-type composition of the deepest hitters

`raw` = the record's `offensive<Type>Min` at its own rank, × `(1 + (own `offensiveTotalDamageModifier`
+ wave modifier)/100)`. Wave-151 modifier **+82.0 %**, wave-160 **+83.0 %** (Lap I, pinned).

| wave | skill | record | rank | raw total | composition |
|---|---|---|---:|---:|---|
| 160 | `kymon1_meteor` | `nemesis_kymon_01` | 28 | **5,612** | phys 2,305 · fire 2,205 · chaos 1,102 |
| 160 | `aetherialvanguard_aethermeteor` | `nemesis_aetherialvanguard_01` | 28 | 4,510 | phys 2,305 · aether 2,205 |
| 160 | `tombguardian_megapunch` | `statue_korvaaktombguardian` | 27 | 3,326 | phys 1,907 · cold 810 · poison 609 · **%currentLife 15** |
| 160 | `wendigo_necroticnovainverse` | `nemesis_wendigo_01` | 28 | 3,235 | pierce 1,249 · vitality 1,986 · **%currentLife 18** |
| **151** | `infernal_embernova` | `swampgolem_h05` | 27 | **2,500** | phys 936 · fire 1,564 |
| 151 | `swampgolem_doubleswipe` | `swampgolem_h01/h02/h05` | 27 | 1,822 | phys 942 · poison 880 |
| **151** | **`infernal_emberburstproc`** | `swampgolem_h05` | 27 | 1,772 | phys 521 · fire 1,251 |

> **⚑ POSITIVE CONTROL ON THE COMMISSION'S OWN NAME.** `R-PM4-61 part 5` named
> `infernal_emberburstproc.dbr` as the sim's deepest w151 hitter. It is **present in the corpus on
> the w151 roster**, on `swampgolem_h05.dbr`, at rank 27, raw 1,772 (521 physical + 1,251 fire) —
> and it is **not** the deepest one there: `infernal_embernova` on the same body is 2,500.

**⚑ A DAMAGE TYPE THE PIPELINE DOES NOT MITIGATE.** `offensivePercentCurrentLife` appears on four
w160 skills and several w151 ones (board total 127 % at w151 under `RUNREC`, 36 % at w160). Its UI
string is `DamagePercentCurrentLife = {%t0}% Reduction to Enemy's Health`, and the answering
defence is `DefensePercentCurrentLife` — **which this build carries at +26 (Rebuke,
`presenceofvirtue3` @rank 11) and nowhere else.** It bypasses armour entirely and is carried in the
sidecar as a **percentage**, never summed into an HP figure. Its semantics (percent of *current*
life, per hit) are I-23's to model.

### 6.3 The kill-rate side — the full damage-type vector

`pm4x_ttk_by_body.csv`, 13 records at wave 151, monster armour/absorption/resists pinned from Lap L.

| statistic | physical-only (Lap L's limb) | **full vector (this lap)** | Δ |
|---|---:|---:|---:|
| median ticks-to-kill, LO damage | 6.340 | **6.317** | **−0.36 %** |
| median ticks-to-kill, HI damage | 4.617 | 4.601 | −0.35 % |
| vs Lap L's band median **7.62** | — | 6.317 | **−17.09 %** |

**The player's kit is so nearly pure physical after conversion that adding every other type moves
the median by a third of a percent.** Pierce (155–206 flat) is the only non-converted direct type
and monster pierce resistance eats most of it. The three weapon conversions (chaos→physical 50 %,
lightning→physical 50 %, EoR-scoped fire→physical 100 %) are already inside the camera-measured
per-hit figure, which is why Lap L's physical-only read was very nearly right.

**Bleeding is a separate story and is NOT folded into TTK here.** Gutsmasher's EoR-scoped line grants
**21,117 bleeding over 3 s**; against a body at 0 % bleed resist that is **7,039 applied HP/s**, and
seven of the thirteen w151 records carry 0 % bleed resistance. **The stacking rule is
UNDECODABLE-FROM-SUBSTRATE** — `gameengine.dbr : damageMagnitude = 100.0` ("Decreasing same type
duration damage") is the only field in the neighbourhood and it does not express a stack count.
Lap I reached the same wall. **Both limbs named, neither folded:** refresh-only (one instance) vs
per-tick stacking (an ~11.4/s applier). `UNREACHED-X-8`.

---

## § 7 — THE WORKED PER-HIT ARITHMETIC, END TO END

One `swampgolem_h05` (wave 151, level 105 LO limb) swinging its **declared** basic attack
`swampgolem_stonethrash.dbr` at rank 27, against `EoRWarlGuts`:

```
1  RAW, from the skill record at its own rank        [pm4x_monster_offense.csv]
     offensivePhysicalMin[26]        =   723.0
     offensiveLightningMin[26]       = 1,013.0
     offensivePercentCurrentLifeMin  =     5.0   (a PERCENT; carried, never summed into HP)

2  SCALE  = 1 + (own offensiveTotalDamageModifier + wave-151 modifier)/100
         = 1 + (41.0 + 82.0)/100  = 2.230                             [Lap I pinned, wave 82.0]
     physical  ->  1,612.3          lightning  ->  2,259.0

3  PHYSICAL through ARMOUR — the hit rolls a region, so the expectation is region-weighted:
     region      chance   armour     absorption   branch                     after-armour
     chest       26 %     2976.5      98 %        1612.3 <= armour -> DLEP        32.25
     legs        20 %     2528.9     100 %        1612.3 <= armour -> DLEP         0.00
     head        15 %     2599.0      98 %                 "                      32.25
     shoulders   15 %     2599.0     100 %                 "                       0.00
     feet        12 %     1723.8      98 %                 "                      32.25
     hands       12 %     1722.2      98 %                 "                      32.25
   The scaled physical line is BELOW every piece's armour, so the DLEP branch fires on every
   region and 98-100 % of it is absorbed.

4  RESIST, capped at playerDefenseCap[2] = 80        (order fork: ARMOUR-then-RESIST limb)
     physical   x (1 - 0.16)  ->  region-weighted    =    17.61 HP
     lightning  x (1 - 0.80)  ->  ARMOUR NEVER TOUCHES IT  =  451.80 HP

5  APPLIED, this body, this round
     RUNREC per-piece limb        =    469.40 HP   =  17.61 physical + 451.80 lightning
     RUNREC aggregate-armour limb =    858.10 HP   <- sheet 3557 armour, absorption 70 %
     MAX limb (infernal_embernova)=    792.30 HP
     SUMALL limb                  =  2,698.25 HP   <- upper bound, not physical
```

**Against a 20,005 pool, the run-of-record number is 2.35 % per body per round.**

> **⚑ AND LOOK AT WHERE THE 469.40 COMES FROM. `96.2 % OF IT IS LIGHTNING.`** The armour stack
> annihilates the physical line — 1,612.3 raw becomes **17.61** applied, **1.1 %** — while the
> lightning line, which armour never touches, passes 20 % of 2,259.0 through an **at-cap** 80 %
> resistance and delivers **451.80**. **This build's armour is enormous and almost irrelevant,
> because band-A monsters on this board are not primarily physical attackers.** Any fold that
> models intake as armour-mitigated physical will under-read it by more than an order of magnitude.
> The naive aggregate-armour limb (858.10) is **1.83×** the per-piece limb, and the entire
> difference is the `defensiveAbsorptionModifier` stack lifting absorption from 70 % to 98–100 %.

---

## § 8 — THE PRE-REGISTERED PREDICTIONS, GRADED

| id | claim | grade | number |
|---|---|---|---|
| **`P-X-1a`** | board intake ∈ [300, 1500] HP/s with all 28 in contact | ⚑ **FAILED** | 3,960.6 – 11,881.7 across the declared cadence grid; above the band at every cadence |
| **`P-X-1b`** | board intake exceeds bare regen 129.38 HP/s | **PASSED** | min over grid 3,960.6 |
| **`P-X-1c`** | board intake below 1,250.3 HP/s | ⚑ **FAILED** | max over grid 11,881.7 |
| **`P-X-2a`** | full vector moves median TTK < ±25 % from 7.62 ticks | **PASSED** | −17.09 % vs Lap L's band median; **−0.36 %** same-population |
| **`P-X-2b`** | decoded kill rate ≥ 1.0 bodies/s | **PASSED** | **1.796** (LO) – **2.161** (HI) bodies/s solo |
| **`P-X-3a`** | shield block DECODED-ABSENT | **PASSED** *(prereg-sighted)* | 0 rows on all four named fields; camera 0/0/0 |
| **`P-X-3b`** | falsifier: any non-zero named block field | **DID NOT FIRE** | 0/4; three *modifier*-family rows reported instead (§ 4.2) |
| **`P-X-4a`** | `combatRegion*Chance` is a hit-location roll ⇒ per-piece armour | **PASSED** | six regions, Σ = 100.0 exactly |
| **`P-X-4b`** | sheet 3,557 is the **SUM** of the pieces | ⚑ **FAILED — my bet** | AVG model −2.59 %; SUM model **+325.7 %** |
| **`P-X-5a`** | `playerDefenseCap` = 80 is the resist cap; sheet is at cap | **PASSED** | 80/80/80; **8** sheet rows exactly at 80 |
| **`P-X-5b`** | armour = physical only, **before** resistance | **type scope PASSED; ORDER UNREACHED** | 2/2 armour equations name `physicalDamageDV`; order fork Δ = 398.4 on a 5,000 hit |
| **`P-X-5c`** | ≥1 record carries `offensive*ResistanceReduction*` | ⚑ **FAILED — my bet** | **0** rows; 2 `offensiveTotalDamageReductionPercent` rows found instead |

### 8.1 ⚑ WHAT `P-X-1`'s FAILURE ACTUALLY MEANS — stated so nobody over-reads it

`P-X-1` was graded **under its own prereg definition: all 28 wave-151 bodies in melee contact
simultaneously.** That definition is the prediction's, and it is almost certainly not the fight.
`meleeTargetDistance = 2.400` gives a contact ring whose geometric capacity this lap **does not
decode** (`UNREACHED-X-3`).

The useful, decoded quantity is the per-body one: **478.1 HP median per body per round** (per-piece
limb). Everything else is that number times a contact count and divided by a round length, and
**this lap decodes neither multiplier**. As a **reported implication** — the referent threshold used
purely as a yardstick, entering no decoded value — `P-X-1c` would hold at:

| declared round length | melee-contact bodies that keep intake under 1,250.3 HP/s |
|---|---:|
| 1.0 s | 2.6 |
| 1.5 s | 3.9 |
| 2.0 s | **5.2** |
| 2.5 s | 6.5 |
| 3.0 s | 7.8 |

**That is the whole intake question in one row: the pipeline is decoded, and what is left is how
many bodies touch the player at once and how fast they swing.** Neither is a mitigation term.

### 8.2 ⚑ THE WAVE-160 POSITIVE CONTROL (no referent number entered it)

Run on the identical pipeline, identical code path, wave-160 roster from the same frozen basis:

| | value |
|---|---:|
| bodies | **5** |
| `RUNREC` board per round | **3,128.5 HP** |
| rounds to empty a 20,005 pool, **zero sustain** | **6.39** |
| at a declared 2.0 s round | **12.8 s** |
| *(grade surface only)* referent wave-160 duration / terminal | *29 s / DEATH* |

The pipeline puts a 5-body wave-160 board within a factor of ~2 of emptying the pool inside the
referent's own wave-160 window **with no sustain modelled at all** — and the referent had ~21 %
ADCtH, 129.38 HP/s regen, 9,000 flat absorb and a 35 %-heal circuit breaker. **Reported as a scale
check, never as a fit.** No referent number entered the computation; the 29 s sits in the grade
surface and is quoted here beside the decode, not inside it.

---

## § 9 — DEFECT TABLE

| id | defect | seam | disposition |
|---|---|---|---|
| **`D-X-1`** | the first build summed the entire skill closure per record, producing a 42,947 HP/round w151 board — an over-read by the size of the closure | legolas (mine) | **SELF-CAUGHT before any grade was computed.** Repaired by changing the ROW GRAIN to per-skill and publishing four explicit policy limbs. Prediction wording untouched; no coefficient moved |
| **`D-X-2`** | `P-X-2a` was written against Lap L's **band** median (790 records) but is computed here over the 13 records actually **rolled** at w151 — different populations | legolas (mine) | **DECLARED, both numbers published** (−17.09 % cross-population, −0.36 % same-population). The clean number is the same-population one; the prediction is graded on the one it named |
| **`D-X-3`** | the armour reconstruction leaves **−92 (−2.59 %)** unexplained | legolas (mine) | **NAMED as `UNREACHED-X-1`, not closed.** Solving for the closing term gives +60.1 % global armour vs the +56 % censused. **DO NOT adjust a term to close it** |
| **⚑ commission premise (c)** | `R-PM4-61 part 5 (c)` calls shield block "the Warlord's load-bearing defensive layer"; this build has no shield and the game's own sheet prints 0/0/0 | conductor | **REPORTED, NOT EXECUTED.** Decoded as DECODED-ABSENT with its record cause; the block *equations* are decoded anyway (§ 4.1) so the finding is not empty |
| **⚑ commission premise (d)** | `R-PM4-61 part 5 (d)` names `Overguard`; it is absent from the played save's allocation | conductor | **REPORTED, NOT EXECUTED.** The defensive-active set that does exist is decoded instead (§ 5) |

---

## § 10 — UNREACHED CENSUS

| id | what | status |
|---|---|---|
| **`UNREACHED-X-1`** | the −92 armour residual; the ≈4 pp of global armour the census does not reach | **OPEN.** Named, not closed |
| **`UNREACHED-X-2`** | monster attack-round length. `characterBaseAttackSpeedTag` is a **string** tag; `characterAttackSpeed` is a multiplier with no readable base interval — the base is animation-driven | **OPEN.** Every per-second figure in this note rides a **DECLARED GRID**, never a decode |
| **`UNREACHED-X-3`** | how many bodies are in melee contact at once (`meleeTargetDistance = 2.400` ring capacity vs body radii) | **OPEN, and it is the largest single multiplier on the intake side** |
| **`UNREACHED-X-4`** | armour-before-resist vs resist-before-armour | **OPEN. BOTH LIMBS PUBLISHED** (Δ 398.4 on a 5,000 hit). All numbers here use ARMOUR-then-RESIST |
| **`UNREACHED-X-5`** | `tombguardian_celestialbreath`'s `offensiveTotalDamageReductionPercentChance = 0.0` — always-on, or never? | **OPEN.** The field reads zero; the semantics of a zero Chance on a non-XOR non-Global family is not in the corpus |
| **`UNREACHED-X-6`** | why the block modifiers (+40 amount, +10 chance from Haven) produce a displayed **0** given an additive `meleeBlockEquation` | **OPEN.** The *outcome* is closed by the camera; only the mechanism is open |
| **`UNREACHED-X-7`** | monster skill-SELECTION policy among non-default skills | **OPEN.** Four limbs published; NAMED not decoded (`R-PM4-56 part 4`) |
| **`UNREACHED-X-8`** | DoT stacking rule (bleeding 21,117/3 s from an ~11.4/s applier) | **OPEN.** Same wall Lap I hit; `damageMagnitude = 100.0` does not express a stack count |
| **`UNREACHED-X-9`** | the armour-absorption clamp at 100 % — no corpus field expresses it | **DECLARED-CLAMPED:CEILING.** Both composition limbs published |
| **`UNREACHED-X-10`** | `monsterLevelGapFixer = [0,5,7]` "adds to monster level" on Ultimate = **+7** | **NAMED, NOT DECODED, NOT FOLDED.** It would move the entire level-indexed substrate |
| **`D-V2-1`** (carried) | the Lap-S PE reader's export map collides vtable-symbol RVAs | **HONOURED.** No vtable base read; § 11 is string residency only, graded CORROBORATION |

---

## § 11 — BINARY CORROBORATION (`NOTE D-V2-1` honoured; no vtable base read)

| group | resident in `Game.dll` | resident in `Engine.dll` |
|---|---|---|
| pipeline field names (31: armour, regions, caps, block, absorption, PTH) | **31 / 31** | **0** |
| equation **variable** names (11: `sumProtectionDV`, `sumAbsorptionDV`, `physicalDamageDV`, `blockChanceDV`, `blockChanceModifierDV`, `shieldDefenseDV`, `shieldAbsorptionDV`, `damageDV`, `offensiveAbilityDV`, `defensiveAbilityDV`, `probabilityToHitDV`) | **11 / 11** | **0** |

Sample RVAs: `armorDefensiveAbsorption` `0x0054c31c` · `physicalDamageDefenseEquationDGP`
`0x005265bc` · `physcialDamageDefenseEquationDLEP` `0x00526654` (the shipped typo is in the binary
too) · `meleeBlockEquation` `0x0052689c` · `projectileBlockEquation` `0x0052699c` ·
`playerDefenseCap` `0x0056550c` · `sumProtectionDV` `0x005273a4` · `blockChanceModifierDV`
`0x0052746c`.

> **⚑ WHY THE VARIABLE NAMES MATTER MORE THAN THE FIELD NAMES.** Field names in a binary only prove
> the loader reads the record. **Variable names prove the loader *evaluates the expression*** — the
> engine resolves `sumProtectionDV` by name at runtime. So `combatformulas.dbr`'s equations are the
> mitigation implementation, not documentation of a hard-coded one. Graded **CORROBORATION**: it
> carries no magnitude by itself, and every magnitude in this note comes from a record.

---

## § 12 — HAND-OFF FOR I-23 (the intake fold)

### 12.1 What to consume

| sidecar | rows | what the fold takes from it |
|---|---:|---|
| `pm4x_formulas.json` | — | the two armour branches, the two block equations, the caps, the UI discriminator strings |
| `pm4x_player_defense.json` | — | per-piece armour, region weights, **both** absorption limbs, **all six** armour models, resist caps, block census |
| `pm4x_player_defense_terms.csv` | 175 | every defensive term with per-source provenance |
| `pm4x_defensive_procs.csv` | 21 | proc record-truth: magnitude + duration + cooldown + trigger. **Uptime is yours** |
| `pm4x_monster_offense.csv` | 374 | per `(record, level-limb, skill)` raw damage by type + DoT lines + `is_default_attack` |
| `pm4x_monster_resist_reduction.csv` | 2 | the w160 damage-reduction debuff (there is no resist reduction) |
| `pm4x_intake_by_wave.csv` | 66 | per-actor applied intake, **four policy limbs × three armour limbs** |
| `pm4x_intake_board.json` | — | board totals, per-body medians, rounds-to-empty, the declared cadence grid |
| `pm4x_ttk_by_body.csv` | 13 | physical-only and full-vector TTK, LO/HI |
| `pm4x_binary_anchors.json` | — | the corroboration table |
| `pm4x_prediction.json` / `pm4x_grade.json` | — | the prereg-and-grade pair, gated on the prediction's digest |

### 12.2 ⚑ DO-NOT

* **DO NOT model `Ascension` as 30 % damage absorption.** It is **30 FLAT**, and the UI format
  strings discriminate it (§ 5.1). This is the single most likely misreading in the whole set.
* **DO NOT use the sheet's 3,557 as `sumProtectionDV` for a hit.** It is the **hit-weighted
  average** across six pieces (§ 2.4). The value the equation wants is the **rolled region's**
  piece armour, 1,722–2,977.
* **DO NOT apply armour to anything but physical.** Nine of ten types never touch it (§ 2.2).
* **DO NOT model band-A intake as armour-mitigated physical damage.** On the worked example
  **96.2 %** of the applied hit is lightning, which armour never sees (§ 7). A physical-only intake
  model under-reads this board by more than an order of magnitude.
* **DO NOT pick an armour-vs-resist order by which one grades better.** `UNREACHED-X-4`; both limbs
  are published and the Δ is 18.9 % of the smaller (§ 3.2). `R-PM4-27 part 3` binds.
* **DO NOT sum a monster's skill closure into one attack.** That is `D-X-1`, it is my own defect,
  and it over-reads the w151 board by **3.6×**. Pick a limb from § 6.1 **explicitly**.
* **DO NOT fold `monsterLevelGapFixer`.** NAMED, not decoded (`UNREACHED-X-10`). Folding a +7 level
  shift would move the entire eHP and damage substrate on a term nothing here measured through.
* **DO NOT fold a melee-contact count from this lap.** `UNREACHED-X-3`. This lap gives you
  **478.1 HP per body per round**; the count is geometry (Laps F/J/R), not mitigation.
* **DO NOT quote any per-second intake figure as decoded.** Every one of them rides
  `UNREACHED-X-2`'s **declared** cadence grid. Quote per-round; carry the cadence as declared.
* **DO NOT fold the 21,117/3 s bleeding as a stacking DoT.** `UNREACHED-X-8`; the stacking rule is
  undecodable from the corpus and Lap I hit the same wall.
* **DO NOT read `P-X-1`'s failure as "the decode says the player dies instantly."** It says the
  *prereg's own 28-in-contact definition* is wrong; § 8.1 gives the contact count that satisfies the
  referent-derived yardstick.
* **DO NOT treat `%currentLife` damage as HP.** It is a percentage, it bypasses armour, and the only
  answering stat on this build is Rebuke's `defensivePercentCurrentLife` +26.
* **Laps V § 7.2, V-2 § 11.2 and W § 7.2 DO-NOT blocks remain binding in full**, carried unchanged.

### 12.3 What I recommend the conductor consider (mine to state, not to decide)

1. **The mitigation arithmetic is now decoded on both sides and it is not, by itself, either
   residual.** Per body per round the referent takes 2.4 % of his pool. What decides survival is
   *how many bodies touch him at once*, *how fast they swing*, and *the sustain layer* — three
   things this lap explicitly does not decode and two of which are geometry.
2. **The next-highest-leverage open item on the intake axis is `UNREACHED-X-3`** — the melee-contact
   ring capacity. It is the largest single multiplier on the intake side and it is a **geometry**
   question (Laps F/J/R substrate), not a mitigation one. It may be reachable without a new decode.
3. **`UNREACHED-X-2` (attack cadence) is the second.** It may not be reachable from the corpus at
   all; if the run needs it, it is a video-measurement lap, not a record lap.
4. **The kill-rate side has one real new term and it is small:** the full damage-type vector moves
   median TTK by −0.36 %. **The crowd gap is not a damage-type-composition error.** If the sim kills
   too fast, the carrier is target multiplicity or tick rate, not the mitigation vector.

---

## § 13 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 13.1 Outputs of this lap

| artefact | sha256 |
|---|---|
| `PREREGISTRATION.md` (committed **alone**, meta `64eea319fef4def32431d4f4821e686941c35e4c`) | `84843789413db57beb54ea663e3755ab0d372de0e138d27b7c6feb5794414d7b` |
| `pm4x_prediction.json` (**hashed before any quantity was computed**) | `1037207f410b5b33751d9c53880dd44d42c87470bfe70da85b6ae03d6bd07164` |
| `pm4x_grade.json` (gated on re-hashing the prediction EXACT) | `4d319eaa0a2dde1747dece1abc41217d045432dc032c828bf198d35547a9ca33` |
| `pm4x_formulas.json` | `cabc727d6711dfa3018be9f250811d841a32dbb8abcd1e41d752279bdd3f02a7` |
| `pm4x_player_defense.json` | `5fa9db84f3ae014cf48f926e1901fd9ea05c57a63162597b8c57e129f54cddf1` |
| `pm4x_player_defense_terms.csv` | `f4be3d8d4026226e6b6bfc758679f6e400ffb01aa4f6d40c73bdf06d49cdc993` |
| `pm4x_defensive_procs.csv` | `86120f387e8c36e10bedb7e5958faa475566d925318f1e04b8589c851e612f2d` |
| `pm4x_monster_offense.csv` | `4252bb0ad95d91d3aef4e968a7bb1848e1338cd6b45926b6bdb4256f2fe41a27` |
| `pm4x_monster_resist_reduction.csv` | `4dfa9dcccf071bb37d740a4ae5159a5171da0409e1aa0e9b9b6e1609e0928f2a` |
| `pm4x_intake_by_wave.csv` | `1937962ed516ae451148787e597cdaff32b994765ecd99b6633e2ebb1ab5ffe4` |
| `pm4x_intake_board.json` | `39f8ed022ed2a6dc4d3568886bffdc36bd60b85d8417e7caf3c59851b2fa5306` |
| `pm4x_ttk_by_body.csv` | `2b0a8f1ac85accfdfd92aead64c5a6c3fc67d18f409b5258fb8990b54c1d5991` |
| `pm4x_binary_anchors.json` | `6e468cdd0193698d952520e457416bdbebfc93bd2586be8647d81901444311df` |
| `pm4x_decode_summary.json` | `4bcdf5a3e674028bc0293c66fd8013654e92c00ae779a64798ed84ebea723f44` |
| `decode.log` | `7568b5b456e861cf09320bdfef11a8a607a7e676bdac6aa4c92848906b02e665` |
| `pm4x_findings.md` (this file) | **self-referential — the authority is `pm4x_digests.json :: outputs`, recomputed at commit. A file cannot carry its own digest and I do not pretend otherwise** |
| `pm4x_digests.json` (covers every output above **and** the three instruments) | *recomputed at commit — quoting it here would be self-referential in the same way* |

### 13.2 Inputs — pinned in `PREREGISTRATION.md § 1`, re-verified **24/24 EXACT** at instrument start (HALT armed; none fired)

| input | sha256 |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `edition-III/mods/survivalmode/resources/Scripts.arc` | `47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| `/Volumes/reincarnated/…/_EoRWarlGuts/player.gdc` | `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5` |
| Lap A `measured-player-sheet.csv` | `6852794382b9bf608f13433ea18be7a52d1f2f0942801e5bb7c4e1be8899badd` |
| Lap G `pm4g_played_kit.csv` | `2fd5a34792b96125bd55a40891dfd65cdeb43c385c6ef06607486342d53ce0b3` |
| Lap G `pm4g_defensive_actives.csv` | `0cdfd3af9a22e2d6d7de59ca0b8238f0e2c04c64192a16dee894ef71ae0be306` |
| Lap D `pm4d_band_b_ehp_by_wave.csv` | `3e82e72b5f35f98f9b30ac46c0aa062c42b804a38ac08791e25d74320ded5024` |
| Lap I `pm4i_dot_riders.csv` | `2dc3e380a3800b3afd14f1923d1e2a32efe9263f4ee2eaec7c69c753ed7f6ce1` |
| Lap I `pm4i_wave_damage_modifier.csv` | `f0852cec35a0362c101618b2a269446c4fba658ee0b80821aa5e4ae47eab910b` |
| Lap I `pm4i_survival_wave_arrays_full.csv` | `eab2d141cb41ad83c89b02c9da2a9c7b75ba49d6cb38b27a988a2a172dbd1ce9` |
| Lap L `pm4l_mitigation_by_body.csv` | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` |
| Lap L `pm4l_eor_per_hit.csv` | `120990d998ac23a4b2dadc134e0f5cf3e51a3f7f6eb34ee400d5e2531b26d5a8` |
| Lap L `method.md` | `d33f396d5d47950b9a13a35f1fbeb6ca5c28adaf92346deaae0b10dd8aa0db32` |
| Lap C `measured-reference-truth.csv` (**grade surface only**) | `4546046efd0d01eaceefe5548b46d14c829b8975474f162a007c586b7dcf5642` |

Both binary digests are byte-identical to Laps U, V and V-2's pinned values.

### 13.3 Instruments

| instrument | sha256 | role |
|---|---|---|
| `research/scripts/pm4x_decode_2026_08_15.py` | `babd69ea0e1d30a0e267b8c79176292c7bb9ffc694da31b593582883793d7e85` | pins · formulas · player defence · procs · monster offense · intake · TTK · **prediction emitted and hashed first** |
| `research/scripts/pm4x_grade_2026_08_15.py` | `f89c3705e88938916e6359d32fc1f9e094d48c57498f18b60113ef680183a5ce` | the grade, **gated on re-hashing the prediction** |
| `research/scripts/pm4x_binary_2026_08_15.py` | `c340072f4d1204e36794352d8de83a6689b41c5784e875a2958631b4c5e602df` | string-residency corroboration (`NOTE D-V2-1` honoured) |
| `pm4g_lib` · `pm4d_lib` · `pm4f_lib` · `pm4i_lib` · `pm4l_emit` · `gd_arz_adapter` · `gd_arc_reader` | *unchanged* | carried readers, **imported never re-implemented** (NOTE-9) |

### 13.4 Determinism ×2 (FG-10 form)

All three instruments were run a **second, real execution** end to end. **All 12 emitted artefacts
are byte-identical** to pass 1 — `pm4x_grade.json`, `pm4x_intake_board.json`,
`pm4x_monster_offense.csv`, `pm4x_player_defense.json`, `pm4x_binary_anchors.json`,
`pm4x_prediction.json`, `pm4x_ttk_by_body.csv`, `pm4x_intake_by_wave.csv`, `pm4x_formulas.json`,
`pm4x_defensive_procs.csv`, `pm4x_player_defense_terms.csv`,
`pm4x_monster_resist_reduction.csv`. The lap draws no RNG and reads no wall clock.

### 13.5 The firewall, discharged

This lap read **no** sim outcome. The one baton it touched
(`kc2-baton-v1-E-s09-cp150-20260809_052836.json`, the frozen ROSTER BASIS Lap I ratified) was read
for `(wave, record_path, level, is_champion)` only — no `path`, no `engage_*`, no `hp_max`, no
duration, no outcome field. The referent's numbers live in `PREREGISTRATION.md § 5` and
`pm4x_grade.json :: grade_surface`, and **not one of them entered a decoded value.**

---

*Lap X closed by legolas (UNKNOWN-RESEARCHER), 2026-08-15. Read-only throughout; nothing outside
this notes directory and `agentic_orchestration/research/scripts/` was written.*
