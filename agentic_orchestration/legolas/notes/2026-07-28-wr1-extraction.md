# WR1-EXT-LEG — ground-truth parameter extraction for M-1…M-4 (Edition-II corpus)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Cell:** WR1-EXT-LEG
**Run:** WR1-2026-07-28 Leg 1 · **Conductor:** gandalf
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` (§1 S-6 corpus, §3 M-1…M-4)
**Class:** evidentiary — measured extraction from primary source
**Mode:** read-only. No writes outside `legolas/notes/` + `legolas/scratch/2026-07-28-wr1-ext/`.
**Method lineage:** reuses `legolas/scratch/2026-07-28-gdc-parse-g7/{arz_index,lib_corpus}.py` and
`legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py`. Nothing rebuilt.

**Corpus (S-6):** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`
archives `database/database.arz` · `gdx1/database/GDX1.arz` · `gdx2/database/GDX2.arz` ·
`gdx3/database/GDX3.arz` (SHA-256s as banked in the G-5a ledger §Provenance, unchanged).
Later archives override earlier. Edition-I untouched.

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`) · **D** = DERIVED (arithmetic
shown, operator named) · **U** = UNRESOLVED · **CANNOT-ANSWER** = probe named, corpus silent.

---

## §0 — The fixture pin, stated once, used by all four sections

Every number below is resolved at the **death-2 instant**, `play_time` 5453 s, which the run has
now over-determined from three instruments:

| Quantity | Value | Source |
|---|---|---|
| Player level at death 2 | **10** | galadriel G-8 §5.2 (panel sweep, L10 at f250→f288) |
| Player max HP at death 2 | **747** | G-8 §4 (`0/747`, M-EYE 8×) |
| Killing blow | **hp 541 → 0 in dt 0.133 s**, engagement 82, `pts_s` 5151.43 | galadriel G-2C **§3.1 (C-1)**, `g2c-drops.jsonl`; death-counter increments 0.067 s later. **541 is a LOWER BOUND — the globe floors at 0** |
| Primordian level (nameplate) | **13** | G-8 §5.1, M-EYE 8× |
| Primordian max life | **14,812** | G-8 §6.3, M-EYE 6× |
| ⇒ Primordian `charLevel` | **13** | `charLevel*1+3` over `lv6_hero`; the nameplate number *is* charLevel (G-8 §5.1 three-instrument agreement) |

**Every rank-indexed array below is therefore sliced at `charLevel = 13`.** Where a skill's rank
equation is `charLevel/4+1`, that is **rank 4** (GD truncates to int; 13/4+1 = 4.25 → 4).

**One carried honesty note that bites all four sections.** The parsed save (`_Fresh Character 01`,
G-7) is the **level-13 end-state**. Death 2 happened at **level 10**. Any player-side item figure
below is the save's gear, not provably the death-2 gear. Where that matters I say so.

---

## §1 — M-2: Frigidring / telegraph-burst nova — the full parameter set

**Record:** `records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr`
(archive `database/database.arz`; `Class = Skill_AttackProjectileRing`,
`templateName = database/templates/skill_attackprojectilering.tpl`,
`FileDescription = "Freeze projectile ring"`, `skillMaxLevel = 60`, array length 60).

**Wiring (M):** `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr`
carries it **twice** — as `skillName7` with `skillLevel7 = charLevel/4+1` (which sets the rank)
and as `specialAttack2SkillName` (which sets the trigger).

### 1.1 — Damage row, rank 4 (charLevel 13) — M, exact-original

| field | rank-4 value | notes |
|---|---|---|
| `offensivePhysicalMin` | **118.0** | array `[34, 60, 88, 118, 148, …]`; no `offensivePhysicalMax` (field = 0.0 ⇒ **flat, not a range**) |
| `offensiveColdMin` | **200.0** | array `[68, 111, 155, 200, 247, …]`; no `offensiveColdMax` ⇒ flat |
| `offensiveFreezeMin` / `Max` | **1.3 s / 1.8 s** | arrays `[1.2, 1.3, 1.3, 1.3, 1.3, …]` / `[1.6, 1.7, 1.8, 1.8, 1.8, …]` |
| `offensiveSlowColdMin` | **60.0** | cold DoT magnitude |
| `offensiveSlowColdDurationMin` | **2.0 s** | scalar, not rank-indexed |
| `skillManaCost` | **34.0** | |

**Payload split: 200 cold / 118 physical = 62.9 % cold.** This is the single most consequential
fact for M-1 (§2.4).

`offensiveTotalDamageModifier` on the skill itself is **0.0** — the skill adds no self-multiplier.
Every other `offensive*` family (fire, lightning, poison, aether, chaos, pierce, life, stun,
knockdown, taunt, fear, confusion, convert, percentCurrentLife, and every other `offensiveSlow*`)
reads **0.0**. **M — the nova is exactly two damage types plus freeze plus a cold DoT. Nothing else.**

### 1.2 — Geometry (M, exact-original)

| field | value | reading |
|---|---|---|
| `projectileLaunchNumber` | **16** | |
| `projectileLaunchRotation` | **360.0** | uniform 22.5° spacing |
| `projectileUsesAllDamage` | **1 (True)** | **each of the 16 carries the FULL row above** |
| `projectileExplosionRadius` | **1.5** | per-projectile blast |
| `distanceProfile` | `Long` | |
| `skillSpecialAnimationName` | **`Roar`** | the telegraph animation (§1.4) |
| `cameraShakeAmplitude` | 0.12 | |
| `ragDollDirection` / `Elevation` / `Effect` / `Push` | `Push` / `Downward` / `TakeHit` / `None` | |
| `skillProjectileName` | `records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr` | |

**Distance-banded damage scaling (M) — the nova is a *reverse* falloff:**

| band | field pair | range | scale |
|---|---|---|---|
| 1 | `projectileDamageRange1Min/Max/Scale` | 0.0 – 2.5 m | **50 %** |
| 2 | `projectileDamageRange2Min/Max/Scale` | 2.5 – 9.0 m | **100 %** |
| 3 | `projectileDamageRange3Min/Max/Scale` | 9.0 – 20.0 m | **140 %** |

**The projectile record caps the reachable band (M, and this is new):**
`icebolt_nova_fxprojectile.dbr` — `projectileDistance = **12.0**`, `projectileVelocity = **14.0**`,
`actorRadius = 0.10`, `collisionShape = Sphere`, `Class = ProjectileFireballLike`.

⇒ **band 3 is only reachable over 9–12 m, not 9–20 m; the projectiles die at 12 m.**
⇒ ring outer edge is reached at **12 / 14 = 0.857 s** after launch; the 2.5 m boundary at 0.179 s,
the 9 m boundary at 0.643 s. **These are the flight times the telegraph→impact window needs.**

### 1.3 — Concurrency: how many of the 16 can hit one target (D, geometry only)

At radius *r* the arc spacing between adjacent projectile centres is `2πr/16 = 0.3927 r`. A point
target is inside the blast of every projectile whose centre passes within `projectileExplosionRadius
= 1.5 m`, so the expected number of simultaneous hits is

```
n(r) ≈ 2 × 1.5 / (0.3927 r) + 1 = 7.64/r + 1
```

| r | n(r) | band scale | raw payload delivered (phys + cold) |
|---|---|---|---|
| 2.5 m | 4.06 | 50 % | 4.06 × 159.0 = **645** |
| 5.0 m | 2.53 | 100 % | 2.53 × 318.0 = **804** |
| 9.0 m | 1.85 | 140 % | 1.85 × 445.2 = **823** |
| 12.0 m | 1.64 | 140 % | 1.64 × 445.2 = **730** |

**D — the operator is plane geometry, not source. It assumes a point target, a perfect ring, and
no projectile-vs-projectile occlusion.** It is offered because M-2's spec needs *some* honest
answer to "how much of a 16-projectile ring lands on one player," and the alternative is a guess.

### 1.4 — Telegraph and cadence

**M, exact-original — the AI trigger block on `slith_wightmirecave01.dbr`:**

| slot | skill | `Chance` | `Delay` | `Timeout` | `Range` |
|---|---|---|---|---|---|
| `specialAttack` | `primordian_wave` | 100.0 | **5.0 s** | 5.0 s | MediumRange |
| **`specialAttack2`** | **`primordian_frigidring`** | **80.0** | **6.0 s** | **3.0 s** | **MediumRange** |
| `specialAttack3` | `chillbane_blizzard` | 100.0 | 10.0 s | 8.0 s | LongRange |
| `buffSelfSkillName` | `primordian_icearmor` | — | controller `BuffSelfBehavior = WhenEnemyIsSeen` | `skillCooldownTime = 32.0 s` | self |

Range bands are **overridden on the monster record** (M): `shortRangeMax = 4.0`,
`mediumRangeMax = **10.0**`, `longRangeMax = 12.0`. (Global defaults in `gameengine.dbr` are
`shortRange 4.75 / moderateRange 9.0 / longRange 15.0 / maximumRange 18.0 / meleeRange 1.25` —
the creature's own values win.) ⇒ **the nova fires when the player is within 10 m.**

**`Delay` vs `Timeout` semantics — U, but tightly constrained by a corpus-wide sweep (D).**
No `.tpl` template files exist anywhere in the pinned corpus (`find . -name "*.tpl"` → 0 hits), so
the field descriptions are unavailable. Sweep of **8,231** `(Delay, Timeout)` pairs across every
`Class = Monster` record in all four archives:

| | min | median | max |
|---|---|---|---|
| `specialAttack*Delay` | 0.5 | **8.0** | 500.0 |
| `specialAttack*Timeout` | 0.5 | **3.0** | 30.0 |

`Delay > Timeout` in **98 %** of pairs (8,096 / 8,231; 39 inverted, 96 equal). `Delay` reaches 500 s
and `Timeout` never exceeds 30 s. **Reading: `Delay` is the re-use cooldown between casts, `Timeout`
is the bounded window in which the AI must land the cast.** This is DERIVED from the distribution,
not stated. **⇒ nova cooldown ≈ 6.0 s, cast window ≈ 3.0 s, fire probability 80 % per opportunity.**

**Telegraph duration in seconds: CANNOT-ANSWER.** Probe run: `skillSpecialAnimationName = Roar` →
`charAnimationTableName = records/creatures/enemies/anm/anm_slith.dbr` → the record was dumped in
full (725 fields). **Every one of its `*AnimSpeed*` fields is a dimensionless multiplier (all
1.0) and every `*AnimWeight*` is a selection weight (100.0). There are no durations.** The absolute
animation lengths live in `.anm` assets inside `resources/Animations.arc`; the pinned corpus
contains **only `Text_EN.arc`** under every `resources/` directory (`find . -name "*.arc"` returns
8 files, all `Text_EN`). **The telegraph length is structurally out of reach of this corpus.**
What *is* available: the 3.0 s `Timeout` bounds it from above, and the 0.179 / 0.643 / 0.857 s
projectile flight times (§1.2) give the post-cast portion exactly.

### 1.5 — CC component, and the fidelity-law reading (M)

- **Freeze: 1.3 – 1.8 s** (`offensiveFreezeMin/Max` @ rank 4). Handler
  `records/fx/damagedefault/dmgspecial_freeze_handler.dbr` — `handlerType = Freeze`, and its **only**
  other fields are cosmetic (`iceCubeName`, `icyEffectName`, three sounds: freeze/thaw/**shatter**).
  **M — there is no shatter *mechanic* in GD's freeze handler. `shatterSound` is a sound.**
  This is the source-side confirmation of the §14.23 H-1 fidelity flag: **GD freeze is a pure
  action-lock of stated duration. It carries no bonus-damage-on-frozen, no HP-threshold execute,
  nothing resembling RDR `freeze`-shatter.** Model the lock; do not port RDR's operator.
- **Cold DoT: 60 over 2.0 s** (`offensiveSlowColdMin` / `…DurationMin`).
- **No stun, no knockdown, no slow-run, no slow-attack-speed** — all read 0.0 (§1.1).
- Freeze resistance is the player-side counter (`defensiveFreeze`); **no equipped item in the
  fixture's save carries `defensiveFreeze`** (§2.3 table). The lock lands at full duration.

### 1.6 — The composition question the 541 lower bound now adjudicates (D — material, flagged)

KIT-CAL-1 §14.10/proto §3c **HELD** the hero/boss damage regime because the additive TDM sum lands
in an unmeasured clamp band. The rank-13/rank-4 TDM sources, verbatim:

| source | rank eq | rank @ cl 13 | `offensiveTotalDamageModifier` |
|---|---|---|---|
| `passive/armorbase05.dbr` | `charLevel*1` | 13 | **−78.0** |
| `passive/damage_totaladjuster.dbr` | `(charLevel/25)+2` | 2 | **+8.0** |
| monster pak, Normal/1P | — | — | **−25.0** |

Additive ⇒ **−95 %** (×0.05). **The death-2 fixture falsifies that this applies to the nova's row.**

| composition | one projectile, band 100 % | 16/16 projectiles (geometric ceiling) |
|---|---|---|
| additive TDM −95 % | 318 × 0.05 = **15.9** | **254** |
| no TDM on the skill row | **318.0** | 5,088 |

The measured killing blow is **≥ 541 delivered HP in one 0.133 s sample, after player armour and
resistances**. The additive reading cannot reach it even if all sixteen projectiles hit a point
target — which §1.3 shows is geometrically impossible. **Under the no-TDM reading the fixture's
541 falls inside the plausible band at every engagement radius** (§1.3 raw 645–823, minus ~21–35 %
player mitigation per §2.4 ⇒ **424 – 650**).

**What this does and does not establish.**
It establishes that **`offensiveTotalDamageModifier` from creature passives does NOT multiply
`Skill_Attack*` damage rows at −95 %.** It does *not* prove the multiplier is exactly 1.0 — a floor
at, say, −40 % would also clear 541 at some radii. It does not touch the base-attack composition,
which §14.10 vindicated additively against different evidence and which is a different question.
**Recommendation to gamora/gandalf: spec M-2 against the RAW row (118 phys + 200 cold per
projectile, band-scaled) and record "no creature-TDM on skill rows" as a named, testable
assumption of the build — not as a settled fact.**

### 1.7 — The rest of the trio (M, banked so the nova is not modelled alone)

The encounter is a **mandatory trio** (proto §1): Primordian + `slitha_melee_b01` +
`slitha_shaman_c01`, `spawnMin = spawnMax = 3`, all three `alwaysSpawn`. Rank-4 rows:

| skill | Class | phys | cold | rider |
|---|---|---|---|---|
| `primordian_wave` | `Skill_AttackWave` | 122 | 210 | `offensiveSlowColdMin` 70 / 3 s; `offensiveSlowDamageMultMin` **30 %**; `waveDistance 16.0`, width 3.0→6.0, `waveTime 1.4 s` |
| `chillbane_blizzard` | `Skill_BuffAttackRadiusDrop` | 58 | 111 | `offensiveSlowTotalSpeedMin` 30 % / 5 s; `dropRadius 15.0`, `skillTargetRadius 8.0`, `skillTargetInterval 2.0 s`, `skillActiveDuration 8.0 s` |
| `primordian_icearmor` | `Skill_BuffSelfDuration` | — | — | `damageAbsorptionPercent` **25**, `characterAttackSpeedModifier` **+35 %**, `offensiveColdModifier` +26 %, `retaliationSlowColdMin` 32; **12 s on / 32 s cooldown** |

---

## §2 — M-1: Armour / mitigation formulas

### 2.1 — The formula, exact-original (M)

`records/game/combatformulas.dbr` (`templateName = database/templates/combatequations.tpl`),
verbatim:

```
physcialDamageDefenseEquationDLEP = physicalDamageDV * (1 - sumAbsorptionDV)
physicalDamageDefenseEquationDGP  = (sumProtectionDV * (1 - sumAbsorptionDV)) + (physicalDamageDV - sumProtectionDV)
```

(`DLEP` = damage **L**ess-than-or-**E**qual-to **P**rotection; `DGP` = damage **G**reater-than
**P**rotection. The `physcial` typo is in the source.)

`records/game/gameengine.dbr`: **`armorDefensiveAbsorption = 70.0`**.

Both branches collapse to one closed form:

```
taken_physical = damage − absorption × min(damage, armour)          with absorption = 0.70
```

**It is neither "flat" nor "percent" — it is a percentage of the *lesser* of damage and armour.**
Against any hit at or below the armour value it removes a flat **70 %**; above it, it removes a
constant **0.70 × armour** and the excess passes through untouched. There is **no roll** — the
absorption is deterministic. Modifier field: `defensiveAbsorptionModifier`
(monster pak Normal/1P = **−20 %**; the player pak
`balancingadjustment_mp+difficulty_players01.dbr` is **all-zero on Normal**, M).

### 2.2 — The one ambiguity that dominates `mitigation_delta` (U — LOAD-BEARING)

`combatformulas.dbr` also carries a **hit-region table** summing to exactly 100 (M):

| region | chance |
|---|---|
| Torso | 26 |
| Legs | 20 |
| Head | 15 |
| Shoulders | 15 |
| Arms | 12 |
| Feet | 12 |
| `combatRegionFullyProtectedChance` / `…UnprotectedChance` | 0 / 0 |

**The source does not say whether `sumProtectionDV` is the character's total armour or the armour
of the rolled region.** The field name says "sum"; the existence of a normalised six-region table
says "roll". No template file exists to settle it (§1.4). Both readings are computed below because
**they differ by a factor of ~6 and `mitigation_delta` is exactly the quantity they disagree about.**

### 2.3 — The fixture's armour, per slot (M — save state, level 13)

| slot | base record | `defensiveProtection` | affix |
|---|---|---|---|
| head | `records/items/gearhead/a03_head002.dbr` | **76.0** | suffix `b_ar014_arje` → `defensiveProtectionModifier 4.0`; prefix `ad003a_res_cold_01` → `defensiveCold 14.0` (jitter 30) |
| shoulders | `records/items/gearshoulders/a03_shoulder01.dbr` | **65.0** | — |
| torso | `records/items/geartorso/a02_torso002.dbr` | **58.0** | suffix `b_ar002_ar` → `defensiveProtectionModifier 4.0`, `characterLife 100.0` |
| feet | `records/items/gearfeet/a02_feet02.dbr` | **52.0** | prefix `aa007a_lifemod_01` → `characterLifeModifier 5.0` |
| legs | `records/items/gearlegs/a02_legs01.dbr` | **50.0** | — |
| hands | `records/items/gearhands/a02_hands01.dbr` | **29.0** | prefix `aa010a_damod_01` → `characterDefensiveAbilityModifier 4.0` |
| waist | `records/items/gearaccessories/waist/a02_waist001.dbr` | **7.0** | — |
| amulet / ring1 / ring2 | `b001_necklace`, `a001_ring02` ×2 | — | no armour |
| **weapon1-0** | `gearweapons/blunt1h/b015b_blunt.dbr` *"Pusquill"* | — | `characterBaseAttackSpeed −0.10` (§4) |
| **weapon1-1** | `gearweapons/shields/b013a_shield.dbr` *"Bernard's Slightly-Chewed Buckler"* | — | `defensiveBlock 65.0`, `defensiveBlockChance 18.0`, `blockAbsorption 100.0`, `blockRecoveryTime 0.5` |

**Sum of base `defensiveProtection` = 337.0.** `defensiveProtectionModifier` totals 8.0 %
(4 on head, 4 on torso) — **GD convention is that this is item-local**, so:
- item-local: 76×1.04 + 58×1.04 + 65 + 52 + 50 + 29 + 7 = **342.36**
- character-global (the other reading): 337 × 1.08 = **363.96**

Nothing in the corpus disambiguates local-vs-global either; the 6 % spread is immaterial next to §2.2.

**Region-weighted armour** (the per-region reading), using the six regions that map to gear slots:
```
0.15×76 + 0.15×65 + 0.26×58 + 0.12×29 + 0.20×50 + 0.12×52 = 55.95
```
(Waist has no region row — under this reading it contributes nothing.)

### 2.4 — What `mitigation_delta` actually is for this fixture (D)

`taken = damage − 0.70 × min(damage, A)`

| incoming physical hit | A = 342.4 (sum) | A = 55.95 (region) | Δ between readings |
|---|---|---|---|
| 41 (trash base-attack, G-5a §4 median) | 12.3 (**−70.0 %**) | 12.3 (**−70.0 %**) | **0** |
| 118 (one frigidring projectile, band 100 %) | 35.4 (−70.0 %) | 78.8 (**−33.2 %**) | **43.4 HP** |
| 165 (one projectile, band 140 %) | 49.6 (−70.0 %) | 126.0 (−23.6 %) | 76.4 HP |
| 541 (the killing blow, all-physical hypothetical) | 162.3 (−70.0 %) | 501.8 (−7.3 %) | 339.5 HP |

**The two readings are IDENTICAL for every hit at or below ~56 and diverge without bound above it.**
That is the honest statement for the spec: *armour's behaviour against trash is unambiguous; its
behaviour against the burst that killed the fixture is the entire open question.*

**And the finding that outranks both:** the nova is **62.9 % cold** (§1.1), and armour in GD
applies to `physicalDamage` **only** — every other damage type routes through its `defensive<Type>`
resistance, which is a plain percentage capped by `gameengine.playerDefenseCap = [80, 80, 80]`
(monsters: `monsterDefenseCap = [100, 100, 100]`). So per projectile at band 100 %:

| component | raw | mitigator | delivered (A = 342.4) | delivered (A = 55.95) |
|---|---|---|---|---|
| physical | 118 | armour | 35.4 | 78.8 |
| cold | 200 | `defensiveCold` = 14 (head prefix, jitter 30 ⇒ 9.8–14.0) | 172.0 | 172.0 |
| **total** | **318** | | **207.4 (−34.8 %)** | **250.8 (−21.1 %)** |

**⇒ against the death-2 nova, `mitigation_delta` is 21–35 %, not 70 %.** Any spec that models
armour as "the mitigation" will over-mitigate this fixture by roughly a factor of two to three.
The galadriel armour re-crop residual (carried caveat, charter §3 M-1) pins *which* armour number
enters this table; it does **not** pin the cold leg, which is the larger one.

**One caveat with teeth:** the head prefix that supplies the entire 14 % cold resistance sits on an
**itemLevel-12** helm, and the player was **level 10** at death 2. It is not provable from the save
that the helm was worn. If it was not, the cold leg is **200 delivered**, and the totals become
**235.4 / 278.8** (−26.0 % / −12.3 %).

### 2.5 — Shield block (M, exact) — a second mitigation channel, and it was OFF

```
meleeBlockEquation      = (blockChanceDV + blockChanceModifierDV)
projectileBlockEquation = (blockChanceDV + blockChanceModifierDV)
shieldDamageReductionEquationDLEB = damageDV * ((100 - shieldAbsorptionDV) / 100)
shieldDamageReductionEquationDGB  = damageDV - (shieldDefenseDV * (shieldAbsorptionDV / 100))
```
With the fixture's buckler (`defensiveBlock 65`, `blockAbsorption 100`, `defensiveBlockChance 18`,
`blockRecoveryTime 0.5`): a blocked hit ≤ 65 takes **0**; above 65 it takes **damage − 65**.
Block chance is a flat 18 %, re-armed every 0.5 s.

**But G-8 §7.2 measured the `Shield block chance` panel row **absent** across `play_time`
2593–5785 — which contains death 2 at 5453** (present at 15.00 before, 18.00 after; 18.00 is
exactly this shield's `defensiveBlockChance`). **Corpus-side mechanism for the absence, which G-8
listed as untested:** `records/skills/playerclass10/werewolf1.dbr` is `Class = Skill_Shapeshift`
with `replacementMeshMale`, `replacementAnims`, `replacementFootsteps`, `replacementSounds`, and
`activeSkillSet = 1` — a full actor replacement. Its granted attacks
(`werewolf1_skill01_claws`, `…02_charge`) are `Skill_AttackWeapon` / `Skill_AttackPathCharge` with
`weaponDamagePct` arrays, so the **weapon** still contributes damage in form. **M for all of that;
that the shapeshift specifically suppresses the shield is NOT stated in source — U.** What is
certain from the measurement is that **block did not contribute at death 2** and the M-1 spec must
not credit it there.

---

## §3 — M-3: Dodge / evasion — the GD-side surface for the Primordian-WIN fixture

### 3.1 — Headline (D, and it is a design ruling more than a number)

**Grim Dawn has no scaling evasion stat.** An exhaustive field-name sweep of all four archives for
`dodge|evade|evasion|deflect|miss|fumble|block` returns exactly two player-facing avoidance stats:
**`characterDodgePercent`** (melee) and **`characterDeflectProjectile`** (ranged). Their magnitudes:

| stat | items | devotion | player skills | creatures |
|---|---|---|---|---|
| `characterDodgePercent` | **2 – 10 %** (105 records) | 2 – 6 % (4 nodes) | up to 100 (situational) | 25 – 100 % (37 records) |
| `characterDeflectProjectile` | **3 – 15 %** (184 records) | 2 – 6 % (4 nodes) | up to 100 | 5 – 100 % (94 records) |

**No equipped item in the fixture's save carries either field** (§2.3 table, checked explicitly).
The fixture had **zero** statistical avoidance.

⇒ **The "dodge-on-tell" in the Primordian-WIN fixture was POSITIONAL, not statistical.** Nothing
in GD's stat model could have produced it. The player left the nova's footprint. **For M-3 this
means the design surface gamora specs is a *policy over space and time* — a react-to-telegraph
reposition — not a chance-to-avoid roll.** Specifying M-3 as a dodge *chance* would model a
mechanic the fixture did not use and GD barely has.

### 3.2 — What GD *does* roll on every hit (M, exact-original)

`records/game/combatformulas.dbr`:

```
probabilityToHitEquation = ((((offensiveAbilityDV/((defensiveAbilityDV/3.5)+offensiveAbilityDV))*300)*0.3)
                          + (((((offensiveAbilityDV*3.25)+10000) - (defensiveAbilityDV*3.25))/100)*0.7)) - 50
normalPTHEquation        = probabilityToHitDV/70
pthMinimum               = 55.0
```

| threshold | value | damage modifier |
|---|---|---|
| `pthThreshold1` | 70.0 | `pthDamageModifier1` **1.0** |
| `pthThreshold2` | 90.0 | 1.1 |
| `pthThreshold3` | 105.0 | 1.2 |
| `pthThreshold4` | 120.0 | 1.3 |
| `pthThreshold5` | 130.0 | 1.4 |
| `pthThreshold6` | 135.0 | **1.5** |

**This is the real avoidance surface: OA-vs-DA is simultaneously a hit/miss roll *and* a damage
multiplier up to ×1.5.** A DA deficit does not merely get hit more often — it gets hit *harder*.
`pthMinimum = 55.0` floors the roll (a low-OA attacker still lands a meaningful fraction).

Outcome enumeration, from `gameengine.dbr` float-text styles (M): `hitStyle`, `critStyle`,
`missStyle`, `dodgeStyle`, `deflectStyle`, `blockStyle`, `partialBlockStyle`, `fumbleStyle`,
`invulnerableStyle` — **nine distinct resolution outcomes**, each with a pet twin.

**Primordian's offence at charLevel 13 (D, from M equations):**
`bio_boss_standard_01.dbr` → `characterOffensiveAbility = (charLevel*7)+100` = 191;
`characterDexterity = (charLevel*8)+50` = 154, ×0.95 (pak `characterDexterityModifier −5`) = 146.3.
```
OA = (191 + 0 + 13×12 + 146.3×0.5) × (1 + (−12)/100) + 53 = 422.7
DA = (134.5 + 35 + 13×12 + 121.6×0.5) × (1 + (−15)/100) + 53 = 381.4
```
(pak Normal/1P: `characterOffensiveAbility 0 / Modifier −12`, `characterDefensiveAbility +35 /
Modifier −15`.) **The fixture player's own DA at level 10 is not recoverable** — the save is the
level-13 end state (§0) and the panel does not render DA. **CANNOT-ANSWER from this corpus;** it is
a screenshot question (character sheet) if anyone needs it exactly.

### 3.3 — Fumble: the one *applied* avoidance operator (M)

`offensiveFumbleMin` (72 records) and `offensiveProjectileFumbleMin` (89 records) with paired
`…DurationMin` — an attacker-applied debuff that makes the *target* miss. This is GD's
"impose evasion on the enemy" verb, and it is a **timed debuff**, not a standing stat.
`gameengine.fumbleDamageFxPak` / `projectileFumbleDamageFxPak` confirm the render channel.
**Primordian applies none of it** (all `offensiveFumble*` on all four of its skills read 0.0).

### 3.4 — The monster's own dodge (M) — different mechanism, do not conflate

`records/controllers/enemy/controller_boss_viloth.dbr` (`Class = ControllerMonster`):

| field | value |
|---|---|
| `DodgeChance` | **50** |
| `DodgeDelay` | **3000 ms** |
| `DodgeDistance` | **2.0** |
| `MinDodgeDistance` | **4.0** |
| `RepositionChance` | 100 |
| `FleeBehavior` | `NeverFlee` |
| `ViewDistance` / `InnerViewDistance` | 15.0 / 4.0 |
| `MaxPursuitDistance` / `PursuitTime` | **75.0** / 10000 ms |
| `minSwingPause` / `maxSwingPause` | **0.30 / 0.40 s** |
| `AttackedAnger` / `AllyAttackedAnger` / `ProjectileAnger` | 16.0 / 4.0 / 3.0 |
| `SightAngerRate` / `InnerSightAngerRate` | 4.0 / 9.0 |

This is an **AI sidestep** — a 2 m lateral move, at most once per 3 s, only when the threat is
≥ 4 m away — not a damage-avoidance roll. `DodgeChance` appears on **407** controller records
corpus-wide; it is the standard monster-AI reposition, and it is the correct model for a
*telegraph-reactive movement policy* if gamora wants a source-anchored one.

---

## §4 — M-4: Attack-speed / animation model

### 4.1 — How attack rate composes (M for every field; the assembly is D)

Three multiplicands, all measured, plus one absolute that the corpus does not carry:

**(a) Base animation.** `charAnimationTableName` → `anm_*.dbr`. **All 725 fields of `anm_slith.dbr`
and all 906 of `anm_werewolf.dbr` are dimensionless**: `*AnimSpeed*` multipliers (uniformly 1.0)
and `*AnimWeight*` selection weights (uniformly 100.0). **No duration anywhere.**

**(b) Weapon term.** `characterBaseAttackSpeed` on the weapon record — the fixture's mace
`b015b_blunt.dbr` reads **−0.10**, tagged `tagAttackSpeedFast`. Corpus-wide over **2,683**
`/gearweapons/` records: range **−0.240 … +0.010**. Distribution by display tag:

| `characterBaseAttackSpeedTag` | modal `characterBaseAttackSpeed` | observed span |
|---|---|---|
| `tagAttackSpeedVeryFast` | **−0.02** | −0.06 … +0.01 |
| `tagAttackSpeedFast` | −0.06 / −0.08 | −0.10 … −0.02 |
| `tagAttackSpeedAverage` | **−0.10** | −0.13 … −0.03 |
| `tagAttackSpeedSlow` | −0.15 / −0.16 | −0.18 … −0.08 |
| `tagAttackSpeedVerySlow` | −0.18 / −0.20 | −0.24 … −0.14 |

**Sign convention, read off the ordering: more negative = slower.** So the term composes as a
**speed factor `1 + characterBaseAttackSpeed` ∈ [0.76, 1.01]** — the fixture's mace sits at
**0.90**. Note the bands **overlap heavily** (−0.10 is simultaneously modal for `Average` and
present in `Fast`): **the tag is an authored display band, not a function of the value.** Do not
derive one from the other.

**(c) Percent modifiers.** `characterAttackSpeedModifier`, summed from every source. On the monster
side the Normal/1P pak contributes **−10 %** (`balancingadjustment_mp+difficulty_enemies01.dbr`,
index 0). Primordian's own `primordian_icearmor` grants **+35 %** for 12 s of every 44 s cycle.

**(d) Dual-wield.** `gameengine.dwWeaponSpeedFactor = **0.5**` (with `dwWeaponDamageFactor = 1.0`,
`2hWeaponDamageFactor = 1.0`).

**Assembled (D):**
```
attack_rate_pct = 100 × (1 + characterBaseAttackSpeed) × characterAttackSpeed × (1 + Σ %AS/100)
                  × [dwWeaponSpeedFactor if dual-wielding]
                  clamped to the caps in §4.3
seconds_per_swing = base_animation_seconds / (attack_rate_pct / 100)
```

### 4.2 — CANNOT-ANSWER: the absolute base interval

**Probe run, and it terminates cleanly.** (i) The `anm_*.dbr` records carry only multipliers (§4.1a).
(ii) A field-name sweep of all four archives for any absolute attack interval
(`*attack*` ∩ `*time|interval|duration|rate|swing|cadence*`) returns **only** slow-debuff durations
(`offensiveSlowAttackSpeedDuration*`), the `specialAttack*Timeout` family, and
`timeBetweenAttacks` (68 records — an intra-skill multi-hit gap, e.g. 100 ms on the werewolf
charge). **There is no base swing time in the database.** (iii) It lives in `.anm` assets inside
`resources/Animations.arc`, and the pinned corpus contains **no `.arc` other than `Text_EN`**
(8 files, verified by `find`). **⇒ Every attack-speed figure in this section is a RELATIVE
multiplier. Any DPS number downstream must supply its own base interval and declare it.**
This is the same wall G-5a §6.2 and the Primordian proto §7.4 hit; it is structural to Edition-II,
not a gap in the pass.

### 4.3 — Caps (M, exact-original — `gameengine.dbr`)

| cap | value |
|---|---|
| `playerAttackSpeedCapMin` / `Max` | **20.0 / 200.0** |
| `playerSpellCastSpeedCapMin` / `Max` | 20.0 / 200.0 |
| `monsterAttackSpeedCapMin` / `Max` | **[20.0, 30.0, 40.0]** (per difficulty) / 500.0 |
| `monsterSpellCastSpeedCapMin` / `Max` | [20.0, 30.0, 40.0] / 500.0 |
| `bossAttackSpeedCapMin` / `Max` | **50.0 / 500.0** |
| `bossSpellCastSpeedCapMin` / `Max` | 50.0 / 500.0 |
| `playerRunSpeedCapMin` / `Max` | 20.0 / **135.0** |
| `monsterRunSpeedCapMin` / `Max` | [20, 25, 30] / 500.0 |
| `absoluteRunSpeedCapMin` / `Max` | [40, 30, 20] / 350.0 |
| `combatIdleTime` | 1.2 s |
| `maxPlayerRotationSpeed` / `minPlayerRotationSpeed` | 30.0 / 19.0 |
| `maxRotationSpeed` / `minRotationSpeed` (monsters) | 16.0 / 8.0 |

**⇒ The player attack-speed cap is 200 % (2× base); monsters and bosses cap at 500 %.**
The asymmetry is a real design fact and belongs in the spec.

### 4.4 — The fixture opposition set (M, exact-original)

`characterAttackSpeed` on each monster record, before and after the pak's −10 %:

| monster | record | raw | after pak | `characterSpellCastSpeed` | tag |
|---|---|---|---|---|---|
| **Primordian** (boss) | `boss&quest/slith_wightmirecave01.dbr` | 1.00 | **0.900** | 1.00 | `CharacterAttackSpeedAverage` |
| Deepmire Vanguard (escort) | `slitha_melee_b01.dbr` | 1.00 | **0.900** | 1.00 | Average |
| Slith shaman (escort) | `slitha_shaman_c01.dbr` | 0.75 | **0.675** | 1.00 | Average |
| Walking Dead (trash) | `zombie_a01.dbr` | 1.18 | 1.062 | 1.00 | Average |
| Eastmire Herder | `trollhalfswamp_a02.dbr` | 1.00 | 0.900 | 1.00 | Average |
| Dreadtusk (hero) | `hero/boar_h01.dbr` | 1.00 | 0.900 | 1.00 | Average |
| Warden Krieg ph.1 (boss) | `boss&quest/warden01.dbr` | 1.05 | 0.945 | 1.05 | Average |

Primordian also carries `characterAttackSpeedModifier = 0.0` on the record itself, so its only
dynamic term is `primordian_icearmor`'s **+35 %** during its 12 s window ⇒ effective **1.215**
for 12 s of every 44 s. Melee cadence floor from the controller: `minSwingPause 0.30` /
`maxSwingPause 0.40` s (§3.4) — **this is the closest thing to an absolute cadence the corpus
gives, and it is an AI pause between swings, not the swing itself.**

---

## §5 — CANNOT-ANSWER ledger (probes named, per L-N)

| # | Question | Probe run | Why it terminates |
|---|---|---|---|
| CA-1 | Nova **telegraph duration in seconds** | `skillSpecialAnimationName = Roar` → `anm_slith.dbr` dumped (725 fields) — all multipliers/weights, zero durations | Absolute lengths live in `.anm` assets in `resources/Animations.arc`; corpus has only `Text_EN.arc` (8 `.arc` files, all Text_EN) |
| CA-2 | **Base attack interval** (seconds) for any actor | (a) `anm_*.dbr` dumped; (b) corpus-wide field-name sweep for absolute attack intervals → only slow-durations, `specialAttack*Timeout`, `timeBetweenAttacks` | Same wall as CA-1. All §4 figures are relative multipliers |
| CA-3 | `specialAttack*Delay` vs `Timeout` **semantics** | `find . -name "*.tpl"` → 0 hits; 8,231-pair distribution sweep as substitute | No template files in the pinned corpus; reading in §1.4 is D, not M |
| CA-4 | Is `sumProtectionDV` **total or per-region** armour? | `combatformulas.dbr` dumped in full; region table present and normalised; no template | Source carries both signals and adjudicates neither. **This is the M-1 blocker — §2.2** |
| CA-5 | Is `defensiveProtectionModifier` **item-local or character-global**? | Both affix records dumped; no scope field | 6 % spread; immaterial next to CA-4 |
| CA-6 | Fixture player's **DA / OA / armour at level 10** | Save parsed (G-7) — it is the level-13 end state; panel does not render DA | Not in the corpus. Character-sheet screenshot is the only route |
| CA-7 | Does the **shapeshift suppress shield block**? | `werewolf1.dbr` dumped — `Skill_Shapeshift`, four `replacement*` fields, `activeSkillSet 1`; no block field | Mechanism plausible, not stated. **The measurement (G-8 §7.2) already establishes block was absent at death 2** — that is what the spec should use |
| CA-8 | Exact **TDM treatment of `Skill_Attack*` rows** | §1.6 adjudication against the 541 lower bound | Falsifies −95 % additive; does **not** prove ×1.0. Build assumption must be named |

---

## §6 — Records used (exact paths)

**Combat / engine** `records/game/combatformulas.dbr` · `records/game/gameengine.dbr` ·
`records/game/balancingadjustment_mp+difficulty_enemies01.dbr` ·
`records/game/balancingadjustment_mp+difficulty_players01.dbr`

**Nova + trio** `records/skills/nonplayerskills/bossskills/{primordian_frigidring, primordian_wave,
primordian_icearmor, primordian_passive}.dbr` ·
`records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr` ·
`records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr` ·
`records/fx/damagedefault/dmgspecial_freeze_handler.dbr`

**Creature + AI** `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/creatures/enemies/bios/bio_boss_standard_01.dbr` ·
`records/creatures/enemies/anm/anm_slith.dbr` ·
`records/controllers/enemy/controller_boss_viloth.dbr` ·
`records/creatures/enemies/{slitha_melee_b01, slitha_shaman_c01, zombie_a01, trollhalfswamp_a02}.dbr` ·
`records/creatures/enemies/hero/boar_h01.dbr` · `records/creatures/enemies/boss&quest/warden01.dbr` ·
`records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr`

**Scaling passives** `records/skills/nonplayerskills/passive/{armorbase05, damage_totaladjuster,
damagebase_physical04, resists_heroboss}.dbr`

**Player side** `records/skills/playerclass10/{werewolf1, werewolf1_skill01_claws,
werewolf1_skill02_charge}.dbr` (GDX3) · `records/creatures/pc/anm_werewolf.dbr` (GDX3) ·
`records/items/gearhead/a03_head002.dbr` · `records/items/gearshoulders/a03_shoulder01.dbr` ·
`records/items/geartorso/a02_torso002.dbr` · `records/items/gearlegs/a02_legs01.dbr` ·
`records/items/gearfeet/a02_feet02.dbr` · `records/items/gearhands/a02_hands01.dbr` ·
`records/items/gearaccessories/waist/a02_waist001.dbr` ·
`records/items/gearaccessories/necklaces/b001_necklace.dbr` ·
`records/items/gearaccessories/rings/a001_ring02.dbr` ·
`records/items/gearweapons/blunt1h/b015b_blunt.dbr` ·
`records/items/gearweapons/shields/b013a_shield.dbr` ·
`records/items/lootaffixes/{prefix,suffix}/*` per §2.3

**Corpus-wide sweeps** all four archives, `Class = Monster` (8,231 `specialAttack*` pairs);
`/gearweapons/` (2,683 `characterBaseAttackSpeed`); full field-name census for
`dodge|evade|deflect|miss|fumble|block` and for attack-interval-shaped names.

**Tooling** `legolas/scratch/2026-07-28-wr1-ext/{resolve.py, gear_def.py}` →
`legolas/scratch/2026-07-28-gdc-parse-g7/{lib_corpus.py, arz_index.py}` →
`research/scripts/gd_arz_adapter_2026_07_24.py`. Read-only throughout.

---

## §7 — What gamora should carry into the builds

1. **M-2 nova, per projectile, rank 4:** 118 physical + 200 cold flat, ×{0.50 / 1.00 / 1.40} by
   range band {0–2.5 / 2.5–9 / 9–12 m}; 16 projectiles at 22.5° spacing, 1.5 m blast each,
   14 m/s, 12 m life; freeze **1.3–1.8 s**; cold DoT 60 over 2 s. Fires within 10 m, 80 % chance,
   ~6 s cooldown, 3 s cast window. **Expect 1.6–4.1 projectiles on a point target (§1.3).**
2. **Do NOT reuse RDR `freeze`-shatter.** GD's freeze handler has no shatter operator — only a
   sound (§1.5). Model an action-lock of stated duration.
3. **M-1 must split the payload.** Armour touches only the 37 % physical leg. Effective
   `mitigation_delta` for the death-2 nova is **21–35 %**, not 70 % (§2.4). Resolve CA-4 (total vs
   region armour) *before* pinning the number — it is a 43–340 HP swing per hit.
4. **Block was OFF at death 2** (measured). Do not credit it.
5. **M-3 is a spatial policy, not a roll.** GD gives the fixture zero dodge stats; the win was
   positional (§3.1). If a statistical surface is wanted anyway, the honest source-anchored ones are
   OA-vs-DA PTH (which is *also* a damage multiplier up to ×1.5, §3.2) and the AI reposition
   parameters in §3.4.
6. **M-4 is relative only.** Compose `(1 + characterBaseAttackSpeed) × characterAttackSpeed ×
   (1 + Σ%AS)`, clamp to 20–200 % (player) / 20–500 % (monster) / 50–500 % (boss). **Declare your
   base interval; the corpus does not have one (CA-2).**
7. **§1.6 is a named build assumption, not a fact.** Spec the nova against the raw row and record
   "creature `offensiveTotalDamageModifier` does not apply to `Skill_Attack*` rows" as testable.

---

*Downstream: gandalf (`RUN-CONDUCTOR`) for the M-1/M-2/M-3 specs; gamora for M-1…M-4 builds;
jack-ryan at Gate-2 for §1.6 and §2.2 (both are assumptions that must survive review, not
findings that close). No canonical doc amended by this note.*
