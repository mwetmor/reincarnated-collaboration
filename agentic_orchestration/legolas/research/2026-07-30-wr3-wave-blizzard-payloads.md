# Research — WR3 stage-2b payloads: `primordian_wave`, `chillbane_blizzard`, `primordian_icearmor`, melee — 2026-07-30

**Mode:** A (analytical / primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR, WR3-KITE-COMMIT run)
**Access mode:** read-only throughout. No game file modified; the game was never launched. Writes
confined to this note and `legolas/scratch/2026-07-30-wr3-payloads/`.

**Grading key:** **M** = MEASURED (read verbatim from a pinned binary) · **M-negative** = measured
*absence* of a field from a full record dump · **C** = COMPUTED (from M inputs under a named
operator) · **U** = UNRESOLVED.

**Sibling artifacts** (this note deepens all three and corrects two):
`legolas/research/2026-07-30-wr3-stage2-referent-extraction.md` ·
`legolas/research/2026-07-30-wr3-nova-star-geometry.md` ·
`legolas/research/2026-07-30-gd-l13-reference-envelope.md`.

---

## VERDICT

**The carried-ext numbers do not survive, and the failure is diagnosable to a single line.**

`primordian_wave` **122 / 210** is the record's **rank-4** value, exactly. `chillbane_blizzard`
**58 / 111** is *its* **rank-4** value, exactly. Both are correct extractions evaluated one rank
low. `skillLevel6/7/8 = 'charLevel/4+1'` was evaluated with `charLevel` = the **player's** level 13
(`int(13/4)+1 = 4`). The formula takes the **monster's own** level. **Rank 5 is correct** (§1.2) —
and it is correct across the entire boss-level uncertainty band, so nothing else in the chain is at
risk from it.

**Three further things the carried-ext numbers were missing, each larger than the rank error:**

1. **A whole damage stage.** Every outgoing number must pass **×0.2625** at Normal / 1-player —
   `armorbase05` + `damage_totaladjuster` (pool, additive) then the difficulty pak (multiplicative).
   The pak's `offensiveTotalDamageModifier = −25.0` was **missed by my own prior note**, which
   checked the pak for *projectile speed* and reported "nothing projectile-side." True as far as it
   went; the damage stage sits in the same record. Correction logged in §7.
2. **All riders.** The wave carries a 3.0 s cold DoT *and* an undocumented 30 % / 3 s
   damage-reduction debuff. The blizzard carries a 30 % / 5 s total-speed slow. Neither was carried.
3. **The blizzard's per-drop number is meaningless without its delivery.** 6 drops per 2.0 s tick
   over 8.0 s, scattered, ground-targeted, hit-tested by a **1.32 u splash** — that is what decides
   its contribution, not the 213 raw.

**And `primordian_icearmor` is roughly twice the ability it was described as.** 25 % absorb / 12 s /
32 s all confirm, but the record also carries **+35 % attack speed**, **total slow immunity**, **+28 %
cold damage**, and a cold retaliation DoT — none of them in the carried description. It is up
**37.5 %** of the fight.

---

## 1. Provenance, and a boss-level correction the commission should absorb

### 1.1 Pins and chain

| pin | SHA-256 | used for |
|---|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/database/database.arz` | `8cdeff128422c7652780…` | every field below |
| `…/gdx1|gdx2|gdx3/database/GDX*.arz` | — | swept for overrides — **none found on any record in this chain** |
| `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` | — | template declarations + descriptions |
| `/Users/admin/Games/vendor/grim-dawn/resources/Creatures.arc` | — | `.anm` clips (`BuffQuick`, `TailLashSunder`) |

Byte-identical `.arz` to every prior GD note — same game build.

```
records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr   "Primorian the Forgotten One"
  ├ specialAttackSkillName  / skillName8 = …/bossskills/primordian_wave.dbr     Skill_AttackWave
  ├ specialAttack3SkillName / skillName6 = …/heroskills/chillbane_blizzard.dbr  Skill_BuffAttackRadiusDrop
  │     └ skillProjectileName = records/fx/skillsother/projectile/blizzard_projectilefx.dbr  ProjectileExploding
  ├ buffSelfSkillName       / skillName9 = …/bossskills/primordian_icearmor.dbr Skill_BuffSelfDuration
  ├ skillName2 = …/passive/damagebase_physical04.dbr   ← the melee payload (unarmedOnly)
  ├ skillName3 = …/passive/armorbase05.dbr             ← the damage damper
  ├ skillName1 = …/passive/damage_totaladjuster.dbr
  └ skillName10 = …/bossskills/primordian_passive.dbr  ← flat cold rider on all attacks
```

Tools (read-only), `legolas/scratch/2026-07-30-wr3-payloads/`: `c1_dropcensus.py` (64-record class
census), `c2_ringflag.py` (1,525-record flag control test), `c3_droprows.py` (per-record table),
`c4_ranks.py`, `c5_melee.py`, `c6_pak.py`, `c7_armorbase.py` (1,307-monster census),
`c9_compose.py` (the C layer). Reused from the star note: `s3`–`s5`, `n1`–`n2`. Reader:
`research/scripts/gd_arz_adapter_2026_07_24.py`; ARC reader `gd_arc_reader_2026_07_26.py`;
`.anm` parser `legolas/scratch/2026-07-30-wr3-stage2/a4_parse.py`, `a6_all.py`, `a7_root.py`.

### 1.2 The rank derivation — and why the boss-level correction does not disturb it

The commission states boss level **16** (`charLevel 13 × 1 + 3`). **That is superseded, by my own
earlier artifact.** The boss's spawn level is not the player's level; it comes from a proxy:

```
records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr
  name1 = …/slith_wightmirecave01.dbr
  levelVarianceEquation1 = records/proxies/lv6_hero.dbr
      minVarianceEquationNormal = '(averagePlayerLevel+2)+(averagePlayerLevel/50)'
      maxVarianceEquationNormal = '(averagePlayerLevel+3)+(averagePlayerLevel/50)'
```
All **M**. At `averagePlayerLevel = 13` (int division, `13/50 = 0`): spawn **15–16**; then the
creature's own `charLevel = 'charLevel*1+3'` → **charLevel 18–19**. This matches
`gd-l13-reference-envelope.md` §2, which anchored charLevel 18 against a **measured** `.gdc`
`lifeAndMana` of **15,822** to within **0.4 %**. The "16" reading treats the player's level as the
spawn level and is wrong.

**The skill ranks are unaffected.** `skillLevel6/7/8/9 = 'charLevel/4+1'`, integer division:

| charLevel | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|
| skill rank | 5 | 5 | **5** | **5** | 6 |

**Rank 5 is invariant across the whole 16–19 band.** Every §2–§4 payload below stands regardless of
which boss-level reading the conductor adopts. (This also retroactively secures the star note's
rank-5 frigidring block.)

**What the correction *does* move** is the two passives keyed on `charLevel*1` —
`damagebase_physical04` (the melee payload) and `armorbase05` (the damper). Those are rank **18–19**,
not 16, and §5 and §6 use 18–19 with 16 shown for audit.

### 1.3 The composition operator — stated once, used everywhere below

```
outgoing = base × (1 + Σ pool offensiveTotalDamageModifier /100) × (1 + pak /100)
```

| stage | source | value | grade |
|---|---|---|---|
| pool | `armorbase05` `offensiveTotalDamageModifier` = `−91 + rank` | **−73.0** (cl 18) · −72.0 (cl 19) | M |
| pool | `damage_totaladjuster` rank 2 (`(charLevel/25)+2`) | **+8.0** | M |
| pak | `balancingadjustment_mp+difficulty_enemies01.dbr` slot 0 | **−25.0** | M |
| **factor** | | **×0.2625** (cl 18) · ×0.2700 (cl 19) · ×0.2475 (cl 16) | **C** |

Pool additive, pak a separate multiplicative stage. This is not an assumption invented here: it is
the rule `gd-l13-reference-envelope.md` §2 adjudicated against a measured anchor (multiplicative
lands at 1.004× of the measured HP; additive misses by 1.82×; "the pak is an engine-level global
stage, not a peer of the skill-passive pool"). **`armorbase0N` is carried by 1,221 of 1,307 Monster
records — 93.4 %** (M, `c7_armorbase.py`). It is a system-wide low-level damage damper, not a
Primordian quirk, and it cannot be dropped from the composition without dropping it game-wide.

An **independent check** on the whole operator sits in §5: the composed melee figure lands inside the
envelope note's *measured* cross-tier band, computed from a different record set.

---

## 2. TARGET A — `primordian_wave`

`records/skills/nonplayerskills/bossskills/primordian_wave.dbr`, `Skill_AttackWave`, 281 fields,
`templateName database/templates/skill_attackwave.tpl`.

### 2.1 Damage block at rank 5 — raw fields first

**Note on min/max:** `offensivePhysicalMax` and `offensiveColdMax` are **scalar `0.0`, not rank
arrays** (M). There is no roll. The wave's impact damage is a **point value**, not a range. The
commission asked for "min AND max"; the answer is that max does not exist on this record.

| field | r3 | r4 | **r5 (governing)** | r6 | grade |
|---|---|---|---|---|---|
| `offensivePhysicalMin` | 91.0 | *122.0* | **153.0** | 185.0 | M |
| `offensivePhysicalMax` | — | — | **0.0** (scalar) | — | M |
| `offensiveColdMin` | 152.0 | *210.0* | **272.0** | 330.0 | M |
| `offensiveColdMax` | — | — | **0.0** (scalar) | — | M |
| `offensiveSlowColdMin` (cold DoT) | 49.0 | *70.0* | **91.0** | 113.0 | M |
| `offensiveSlowColdDurationMin` | — | — | **3.0 s** (scalar) | — | M |
| `offensiveSlowColdMax` / `…DurationMax` | — | — | **0.0** | — | M |
| `skillManaCost` | — | — | **60.0** (scalar) | — | M |

*Italicised r4 column = the carried-ext values. See §6.*

**`FileDescription` is stale:** `'large cone wave with cold and poison dot'` — every
`offensivePoison*` field on the record is **0.0** (M). The DoT is **cold**. The description was
copied from a tidal-wave ancestor (the sounds are still `spak_tidalwave_*`). Do not use it.

### 2.2 Riders — three of the four the commission asked about do not exist

| rider | present? | grade |
|---|---|---|
| **freeze** | **NO** — `offensiveFreeze*` does not appear anywhere in the 281-field record | **M-negative** |
| **knockdown** | **NO** — `offensiveKnockdown*` absent entirely | **M-negative** |
| **trauma** | **NO** — no trauma field; `offensiveSlowBleeding*` all 0.0 | **M-negative** |
| **slow (movement)** | **NO** — `offensiveSlowRunSpeedMin/Max/Duration*` all **0.0** | M |
| stun / petrify / sleep / confusion / fear / taunt / convert | NO — 0.0 or absent | M / M-negative |
| **cold DoT** | **YES** — 91.0 over **3.0 s** at rank 5 | **M** |
| **damage-reduction debuff** | **YES** — `offensiveSlowDamageMultMin` **30.0** for `offensiveSlowDamageMultDurationMin` **3.0 s** (scalars, not rank-scaled) | **M** |
| knockback | `ragDollDirection 'Push'`, `ragDollPush 'None'`, `ragDollEffect 'TakeHit'`, `ragDollAmplification 1.0` — cosmetic, **no displacement value** | M |
| camera shake | `cameraShakeAmplitude 0.12`, `cameraShakeDurationSecs 1.0` | M |

**The 30 % / 3 s damage-reduction debuff was not on the commission's list and is the wave's real
sting.** Template `templatebase/parameters_offensive.tpl` declares `offensiveSlowDamageMultMin` with
an empty description; by field-family convention (`offensiveSlow<X>` = a timed debuff applied to the
target) it reads as **"target deals 30 % less damage for 3 s."** The Normal/1p pak's
`offensiveSlowDamageMultModifier` is **0.0** at slot 0, so it lands unmodified. **U-A1: the sign
convention (target's damage reduced vs. damage-taken increased) is not established by any field
description or by corpus contrast.** Lean: reduced *outgoing* damage on the target, consistent with
every other `offensiveSlow<X>` being a debuff on the victim. **This matters for the stage-2b grill:
if the lean is right, eating a wave costs the player ~30 % of their DPS for 3 s on top of the hit.**

### 2.3 Geometry — the prior note's figures all confirm at the record

| field | prior note | **at the record** | grade |
|---|---|---|---|
| `waveStartWidth` | 3.0 | **3.0** ✓ | M |
| `waveEndWidth` | 6.0 | **6.0** ✓ | M |
| `waveDistance` | 16.0 | **16.0** ✓ | M |
| `waveDepth` | 1.0 | **1.0** ✓ | M |
| `waveTime` | 1.4 | **1.399999976** ✓ | M |
| `useTargetDir` | — | **absent → default 0** — template desc: *"Fire in direction of target (true) or forward facing dir (false)"* ⇒ **fires along the caster's facing, not at the target's position** | M-negative |
| `waveSource` | — | **absent → template default `'Source;Target'` first token = Source** ⇒ originates at the caster | M-negative |
| `fxPakName` / `fxPakSpawnDistance` / `fxPakExtents` / `fxPakRandAngle` | — | `tidalwavepoison_fxpak01.dbr` / 0.8 / 1.5 / 15.0 | M |

**Once per target, not a tick.** `skill_attackwave.tpl` declares **no interval, tick, repeat or
`skillTargetInterval` field of any kind**, and the record carries none (M-negative, verified against
the full 281-field dump and the full template variable list). The wave is a swept volume, not a
persistent zone:

| quantity | value | grade |
|---|---|---|
| front speed | `16.0 / 1.4` = **11.429 u/s** | C |
| dwell inside the 1.0-depth band | `1.0 / 11.429` = **0.0875 s** | C |
| half-width at r | `(3.0 + 3.0·r/16)/2` = 1.5 + 0.09375·r | C |
| lateral clearance needed at r = 9.0 u (cast range) | 2.344 + 0.32 = **2.66 u** = **0.334 s** @ 7.97 u/s | C |
| arrival at r = 9.0 u | **0.787 s** after release | C |

**The escape verb is lateral, and generous:** at the cast range the player has the 0.85–0.95 s
telegraph *plus* 0.787 s of travel — ~1.7 s — to cover 2.66 u. Contrast the star (0.053 s of lateral
movement inside a 0.80 s telegraph): the wave is a *wider, slower* test of the same axis.

### 2.4 Cadence and trigger — all four confirm

Creature-side (`slith_wightmirecave01.dbr`), all **M**:

| field | prior note | at the record |
|---|---|---|
| `specialAttackChance` | 100 % | **100.0** ✓ |
| `specialAttackDelay` | 5.0 s | **5.0** ✓ |
| `specialAttackTimeout` | 5.0 s | **5.0** ✓ |
| `specialAttackRange` | MediumRange | **`'MediumRange'`** ✓ |

The skill itself has **no `skillCooldownTime`** (M-negative) — gating is entirely creature-side.
U-3 from the star note carries: `'MediumRange'` has no exact match in `gameengine.dbr`
(`shortRange 4.75` / `moderateRange 9.0` / `longRange 15.0`); `moderateRange = 9.0` assumed.

Animation (`TailLashSunder` → `anm_slith.dbr` `unarmedSpecialAnimRef5` → `slith01_attack_special_sunder.anm`,
`unarmedSpecialAnimSpeed5 = 0.90`, **79 keys @ 30 fps**, `RightHandHit@f23`, all M):

| rate model | release | total |
|---|---|---|
| anim-table only (0.900) | 0.8519 s | 2.8889 s |
| + pak attack −10 % (0.810) | **0.9465 s** | **3.2099 s** |
| + pak cast −8 % (0.828) | 0.9259 s | 3.1401 s |

Same U as the parent artifact (which pak modifier applies to a monster attack-class skill anim is
not resolvable from source). Band **0.85–0.95 s** release; **2.89–3.21 s** total. The prior note
reported the no-pak figures for this skill; the pak-applied band is the one Matt's session ran under.

**New (M):** the sunder clip's root bone `Bip001` carries a translation range of **1.388 / 0.964 /
0.726** on the three axes, with **first key == last key** — an in-place lunge-and-return, **net
displacement 0.0**. (The parent artifact reported root motion 0 for the two *melee* clips and did
not profile this one.) The boss does not gain ground with the wave, but it is not statuesque
either; the cone's origin swings by up to ~1.4 u mid-animation.

### 2.5 Difficulty-pak modifiers touching this skill — **the correction**

`records/game/balancingadjustment_mp+difficulty_enemies01.dbr`, slot 0 = Normal / 1 player (index 0
of 12; confirmed by `characterAttackSpeedModifier[0] = −10.0` reproducing the parent artifact). All M:

| field | slot 0 | touches |
|---|---|---|
| **`offensiveTotalDamageModifier`** | **−25.0** | **wave impact, wave DoT, blizzard, nova, melee — everything** |
| `offensiveSlowColdModifier` | **−38.0** | the wave's 3 s cold DoT, and the nova's |
| `offensiveFreezeModifier` | −20.0 | the nova's freeze (not the wave's — it has none) |
| `offensiveStunModifier` | −30.0 | nothing here |
| `offensiveSlowPhysical/Fire/Lightning/Life/Poison/BleedingModifier` | −38.0 | nothing here |
| `offensiveSlowDamageMultModifier` | **0.0** | the wave's 30 % debuff — **unmodified** |
| `offensivePhysicalModifier` | **0.0** | — |
| `retaliationTotalDamageModifier` | −66.0 | icearmor's cold retaliation |
| `characterAttackSpeedModifier` | −10.0 | animation rates |
| `characterRunSpeedModifier` | −18.0 | boss chase speed |
| `characterSpellCastSpeedModifier` | −8.0 | animation rates |

**Nothing in the pak touches wave *timing* directly** — `waveTime`, `waveDistance` and `waveDepth`
are untouched; only the animation rate moves. **But the pak absolutely touches wave damage**, and
the star note's §5 line ("the Normal/1p slice touches attack speed, run speed, cast speed and nothing
projectile-side") is true only of *projectile kinematics*. Correction filed at §7.

### 2.6 Composed — Normal / 1-player effective (C)

| component | raw M (rank 5) | **effective, charLevel 18** | charLevel 19 |
|---|---|---|---|
| physical | 153.0 | **42.6** (×0.2625 ×1.06 pool phys) | 43.8 |
| cold | 272.0 | **71.4** | 73.4 |
| **impact total** | **425.0** | **114.0** | 117.2 |
| cold DoT | 91.0 / 3.0 s | **14.8 / 3.0 s** (×0.2625 ×0.62) | 15.2 |
| damage-reduction debuff | 30 % / 3.0 s | **30 % / 3.0 s** (pak modifier 0) | same |

The ×1.06 on physical is the pool's `offensivePhysicalModifier`
(`damage_totaladjuster` rank 2 = +6.0; `armorbase05` rank 18 = 0.0). `damagebase_physical04`'s
`offensivePhysicalModifier 15.0 @ offensivePhysicalModifierChance 10.0` is a 10 % proc and is **not**
folded in — carry it as a 10 %-of-the-time +15 % physical if the fixture models procs.

---

## 3. TARGET B — `chillbane_blizzard`

`records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr`, `Skill_BuffAttackRadiusDrop`,
726 fields. Corpus for every census below: **all 64 `Skill_BuffAttackRadiusDrop` records across all
four databases** (`c1_dropcensus.py`, `c3_droprows.py`).

### 3.1 Where the payload lives — not on the projectile

`skillProjectileName = records/fx/skillsother/projectile/blizzard_projectilefx.dbr`, class
`ProjectileExploding`, **33 fields, zero damage fields** (M — full dump). The projectile is pure FX
and kinematics. **The damage block is on the skill record.**

| field | r3 | r4 | **r5 (governing)** | r6 | grade |
|---|---|---|---|---|---|
| `offensivePhysicalMin` | 42.0 | *58.0* | **76.0** | 93.0 | M |
| `offensivePhysicalMax` | — | — | **0.0** (scalar) | — | M |
| `offensiveColdMin` | 86.0 | *111.0* | **137.0** | 163.0 | M |
| `offensiveColdMax` | — | — | **0.0** (scalar) | — | M |
| `skillManaCost` | 55.0 | 60.0 | **65.0** | 70.0 | M |

Again **no max** — point values, no roll. *Italicised r4 = carried-ext. See §6.*

**U-B1 — is the 213 block applied whole per drop, or divided by 6?** `projectileUsesAllDamage` is
**absent → False** (M-negative), and it is **False on 64 of 64** records in this class — the flag has
zero discriminating power here. Control test across the whole corpus (`c2_ringflag.py`, **1,525**
skill records declaring the field): it is **True on 59**, of which **57 are multi-projectile**; the
two singles are `Skill_AttackProjectileBurst` records where launch count is not carried by
`projectileLaunchNumber`. So the flag *is* a multiplicity flag, and a strict reading says False on a
6-launch record means the block is not applied whole. **Against that:** Crate never sets it True in
this class (0 of 32 multi-drop records), which under the strict reading means *every rain skill in
the game* divides — and 213/6 = 35.5 raw → **9.3 effective**, below the trash-mob floor the envelope
note measured (35–85). **Lean: whole block per drop.** Both figures given in §3.6; this U is the
single largest open magnitude in the note.

### 3.2 Riders per drop — one, and it is not freeze

| rider | present? | grade |
|---|---|---|
| **total-speed slow** | **YES** — `offensiveSlowTotalSpeedMin` **30.0** for `offensiveSlowTotalSpeedDurationMin` **5.0 s** | **M** |
| **freeze** | **NO** — `offensiveFreeze*` absent/0 | **M-negative** |
| **cold DoT** | **NO** — `offensiveSlowCold*` absent/0 | **M-negative** |
| stun / knockdown / petrify / sleep | NO | M-negative |
| camera shake | `cameraShakeAmplitude 0.12` | M |

`offensiveSlowTotalSpeed` is the movement **and** attack **and** cast speed debuff. The pak carries
no `offensiveSlowTotalSpeedModifier`, so **30 % / 5 s lands unmodified** (M). Note the interaction:
5 s of −30 % movement inside an 8 s storm is a compounding trap — the slow makes the *next* drop
likelier to land. That interaction is not currently in the fixture.

### 3.3 Drop mechanics — raw fields

| field | value | grade |
|---|---|---|
| `projectileLaunchNumber` | **6** (scalar, all ranks) | M |
| `skillTargetInterval` | **2.0 s** | M |
| `skillActiveDuration` | **8.0 s** | M |
| `skillTargetRadius` | **8.0** | M |
| `dropRadius` | **15.0** | M |
| `dropHeight` | **20.0** | M |
| `dropVariation` | **3.0** | M |
| `projectileExplosionRadius` | **1.0** | M |
| `skillProjectileTargetGroundOnly` | **True** | M |
| `targetingMode` | **`'Point'`** | M |
| `skillTargetNumber` | **absent** | M-negative |
| `skillCooldownTime` / `skillSpecialAnimationName` | **absent** — no own cooldown, **no named cast animation** | M-negative |
| projectile: `actorRadius` / `projectileVelocity` / `projectileDistance` / `useTrajectory` / `launchAngle` | **0.5 / 24.0 / 24.0 / False / 0.0** | M |
| projectile FX | `mesh fx/meshfx/frostorb01.msh`, `projectileFlightFX icebolt_flight_fx`, `projectileImpactFX blizzard_impact_fx01`, `scale 1.2` | M |
| audio | `skillSwipeSound spak_chillbane_blizzard_loop` | M |

Creature-side gating (M): `specialAttack3Chance 100.0`, `specialAttack3Delay 10.0`,
`specialAttack3Timeout 8.0`, `specialAttack3Range 'LongRange'`.

### 3.4 The warning window — **0.833 s, and it is the falling orb, nothing else**

| quantity | value | grade |
|---|---|---|
| fall time | `dropHeight / projectileVelocity` = `20.0 / 24.0` = **0.8333 s** | **C** |
| motion model | `useTrajectory = **False**` ⇒ straight line at constant velocity, **no gravitational acceleration** | M |
| range check | `projectileDistance 24.0 ≥ dropHeight 20.0` ⇒ no in-flight expiry | M |
| player traverse in one fall time | 7.97 × 0.8333 = **6.64 u** | C |

**U-B2 — the DBR encodes no pre-impact ground telegraph.** There is no `fxPakName`, no
`inflightGroundFxPakName`, no shadow/decal field, and no separate warning-FX field on either the
skill or the projectile record (M-negative, verified against both full dumps). **Named, per the
commission, with the lean: the warning *is* the 0.833 s of visible descent** — the `frostorb01`
mesh with `icebolt_flight_fx` trailing it, under a looping audio cue. That is the number to model.
If the shipped game draws an impact decal, it is drawn engine-side from the drop point and is not
recoverable from these records.

Also note (M-negative): `skillSpecialAnimationName` is **absent** on this record. Unlike the wave
(`TailLashSunder`) and the nova (`Roar`), the blizzard has **no named cast animation** — so there is
no *caster-side* telegraph to measure either. Everything the player gets is in the 0.833 s.

### 3.5 Re-targeting — **`targetingMode` is the field that decides it, and it says fixed**

The commission asked whether the point re-aims each tick via `skillTargetInterval 2.0`, and which
field decides. **`skillTargetInterval` is not that field.** It is a volley cadence.
**`targetingMode` is the field, and its value is `'Point'`.**

Corpus adjudication (`c1`/`c3`), all M:

- Class-wide enum (`Default;Point;Object;Target`): **58 records `'Point'`, 2 records `'Target'`, 4 absent.**
- **Crosstab, and it is clean:** both `'Target'` records (`turret_messenger_02_firestorm`,
  `madwitch_firestorm`) also carry `skillProjectileTargetGroundOnly = **False**`. `'Target'` records
  track an actor; `'Point'` records resolve to a ground point. The two fields agree perfectly on
  both records.
- `chillbane_blizzard` is `'Point'` **and** `skillProjectileTargetGroundOnly = True`.

**⇒ The storm centre is resolved once, to a ground point, at cast. It does not re-aim.**
`skillTargetInterval 2.0` fires a fresh 6-drop volley every 2.0 s at the *same* centre;
`skillActiveDuration 8.0 / 2.0` = 4 intervals ⇒ **4–5 volleys, 24–30 drops**.

Corroborating: `skillTargetNumber` — the "acquire N targets in a radius" machinery — is set on
**exactly one record in the entire corpus**, the `base_template skills` exemplar. It is unused in
shipped content, which is what you would expect if this class places a *point*, not a target list.

### 3.6 Hit test — adjudicated freshly, and it lands **opposite** to the star note

The commission is right that the star's Reading A does not transfer. It does not, and the same
census method that established Reading A there establishes the *reverse* here.

**Reading S — SPLASH (adopted, C, high confidence): the hit test is `projectileExplosionRadius`
centred on the ground impact point.** Two independent supports:

1. **`projectileExplosionRadius` is present on 64 of 64 `Skill_BuffAttackRadiusDrop` records — zero
   exceptions** (M). The star note rejected splash for the ring class because **103 of 299** ring
   records *lack* the field, so it cannot be their hit test. Running the identical census on this
   class inverts the result completely. A field that is optional in one class and **without exception**
   in another is load-bearing in the second. (It holds across the `groundOnly` split too: 44/44
   ground-only records have it, 20/20 non-ground records have it.)
2. **`skillProjectileTargetGroundOnly = True`** (M). The projectile's contact event is terrain. A
   body-collision hit test against the player is unavailable *by construction* — the projectile
   never tests against the player. The only mechanism by which a ground drop can damage a player is
   the detonation radius.

The projectile's own `actorRadius 0.5` is the visual orb (`frostorb01.msh` at `scale 1.2`), not a
hit test, under this reading.

| | half-width | grade |
|---|---|---|
| **effective hit radius** | `projectileExplosionRadius 1.0` + player `actorRadius 0.32` = **1.32 u** | **C** |

**Reading C — COLLISION (rejected, carried as the named alternative):** hit radius `0.5 + 0.32 =
0.82 u`. Rejected on support 2 — a ground-targeted projectile has no player-collision event to test.
Recorded so the adjudication is auditable, not averaged in.

**And a second adjudication the commission did not ask for but the build needs — which radius is the
scatter?** `skillTargetRadius 8.0` and `dropRadius 15.0` are both plausible on their names. Adopted:
**`skillTargetRadius = 8.0` is the scatter radius; `dropRadius` is the caster-relative radius within
which the centre is auto-placed.** Two supports, both M:

1. **All six `dropRadius == 0.0` records in the corpus are exactly the Devastation family**
   (`playerclass05/devastation`, `item_devastation` ×2, `item_devastationoutcast`,
   `arcanedevastation`, `sandbox/…skillsecondary_devastation`) — the **player-aimed** members of the
   class. A skill whose centre the player supplies needs no auto-placement radius; and those six
   still scatter, so the scatter cannot be `dropRadius`. Every NPC record has `dropRadius > 0`.
2. **`item_apocalypse` rank-scales `skillTargetRadius` *downward*: `[12.0, 9.0]`** (M). Skills
   improve with rank. A **tightening scatter** concentrates the drops on the target — an improvement.
   A shrinking *acquisition* radius would be a regression. (Caveat named: the two entries may be two
   item tiers rather than a rank progression; the argument holds under either.)

`dropVariation 3.0` is per-drop jitter on top. **U-B3: whether the jitter is positional or on the
drop height (hence a landing-time stagger).** Corpus lean is *positional*: the single record with a
sub-3 `dropVariation` (`turret_messenger_02_firestorm`, 1.25) is also the record with the smallest
`dropRadius` (2.0) — the variation tracks the radius, not the height (`dropHeight 24.0`, mid-range).
**Flagged, not used in any figure.**

### 3.7 Composed — Normal / 1-player effective (C)

**Per drop, whole-block reading (adopted lean, §3.1):**

| component | raw M (rank 5) | **effective, charLevel 18** | charLevel 19 |
|---|---|---|---|
| physical | 76.0 | **21.1** (×0.2625 ×1.06) | 21.8 |
| cold | 137.0 | **36.0** | 37.0 |
| **per-drop total** | **213.0** | **57.1** | 58.7 |
| slow rider | 30 % total speed / 5.0 s | **unchanged** | unchanged |

*Divided-by-6 reading (§3.1 alternative): raw 35.5 per drop → **9.5 effective**.*

**Landing rates** (C, stationary player at the storm centre; hit radius 1.32 u, scatter 8.0 u):

| | adopted (scatter 8.0) | rejected alt (scatter 15.0) |
|---|---|---|
| per drop | **2.7 %** | 0.8 % |
| per 6-drop volley | **15.3 %** | 4.6 % |
| over 4 volleys (24 drops) | **48 %** | 17 % |
| over 5 volleys (30 drops) | **56 %** | 21 % |

**Expected total per cast, adopted readings, stationary player:** ≈ 24–30 drops × 2.7 % × 57.1 ≈
**37–46 damage**, i.e. roughly *one* landed drop. The blizzard is a **zoning** ability, not a burst
one — its function is to make a patch of ground expensive for 8 s while the boss does something else,
and its slow rider is worth more than its damage. The player who stands still eats ~1 drop; the
player who walks 6.6 u in the first fall window eats ~0.

**A coincidence trap worth naming:** the carried-ext blizzard *physical* figure (58) and the correct
*effective per-drop total* (57.1) are numerically adjacent for entirely unrelated reasons. Do not
let that near-match launder the carried-ext number.

---

## 4. TARGET C — `primordian_icearmor`

`records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr`, `Skill_BuffSelfDuration`,
641 fields. Rank 5 (`skillLevel9 = 'charLevel/4+1'`).

### 4.1 The three commissioned figures — all confirm

| field | commission | **at the record** | grade |
|---|---|---|---|
| `damageAbsorptionPercent` | 25 % | **25.0** ✓ | M |
| `skillActiveDuration` | 12 s | **12.0** ✓ | M |
| `skillCooldownTime` | 32 s | **32.0** ✓ | M |
| `instantCast` | noted | **True** ✓ | M |

### 4.2 Four riders the carried description does not have

| field | rank 5 | reading | grade |
|---|---|---|---|
| **`characterAttackSpeedModifier`** | **+35.0** | boss swings **35 % faster** for 12 s | **M** |
| **`defensiveTotalSpeedResistance`** | **500.0** | **total immunity to slows** for 12 s | **M** |
| **`offensiveColdModifier`** | **+28.0 %** | all cold damage — wave, blizzard, nova, passive — up 28 % for 12 s | **M** |
| **`retaliationSlowColdMin`** | **39.0** over `retaliationSlowColdDurationMin` **2.0 s** | **the reflect/retaliation rider the commission asked for** | **M** |
| `charFxPakSelfNames` | `icearmor_chfxpak01.dbr` | the visual tell | M |
| `skillActivatedSound` | `spak_damage_freeze_freeze.dbr` | the audio tell | M |

**Retaliation is negligible.** Pak `retaliationTotalDamageModifier` slot 0 = **−66.0** (M), so the
composed value is ≈ 39 × 0.2625 × 0.34 ≈ **3.5 over 2 s**. Report it for completeness; it is not a
mechanic.

**The other three are not negligible.** +35 % attack speed compresses the melee cycle the parent
artifact measured (1.369 s lock → ~1.014 s) for a third of the fight, and slow-immunity nullifies any
player control tool in that window. **The `defensiveTotalSpeedResistance 500.0` is redundant in
practice** — `primordian_passive` (rank 5) carries the same 500.0 permanently (M), along with
`defensiveTrap 500.0`. The boss is slow-immune for the whole fight; icearmor's copy adds nothing.

### 4.3 Cast animation and the root question

`skillSpecialAnimationName = 'BuffQuick'` → `anm_slith.dbr` `unarmedSpecialAnimRef4 = 'BuffQuick'` →
`unarmedSpecialAnim4 = slith01_cast_attack_01.anm` at `unarmedSpecialAnimSpeed4 = **1.0**` (all M).

| quantity | value | grade |
|---|---|---|
| clip | **51 keys @ 30 fps**, `SwipeRight@f21`, `RightHandHit@f25` | M |
| duration, anim-table only | **1.6667 s** | C |
| duration, + pak attack −10 % | **1.8519 s** | C |
| duration, + pak cast −8 % | **1.8116 s** | C |
| **root motion** | **0.0** — `Bip001` translation range below the 0.01 detection threshold on all three axes | **M** |

**Does it root the boss?** The animation contains **zero root translation**, so if it plays, the boss
is stationary for **~1.81–1.85 s**. `instantCast = True` means the *effect* applies at frame 0, not
at the `RightHandHit` callback (f25 = 0.833 s) — so the 25 % absorb and +35 % attack speed are
already live during that window.

**U-C1: whether the engine permits movement or attack cancellation out of an `instantCast` buff
animation is not in the DBR** (the `instantCast` template variable has an empty description, and no
corpus contrast isolates it). **Lean: the animation plays and the boss is committed for its
duration** — root motion 0 means it stands still under either reading; what is unresolved is whether
it can *attack* out of it. Under the committed reading, the fight-shape consequence is real: the boss
buys 12 s of 25 % absorb + 35 % attack speed for **~1.8 s** of standing still, and the 12 s / 32 s
cycle means **the buff is up 37.5 % of the fight.**

---

## 5. TARGET D — melee default attack. **The chain does not dead-end.**

The boss is **unarmed**: `chanceToEquipRightHand`, `…LeftHand`, `…Head`, `…Legs`, `…Shoulders`,
`…Finger1/2` are **all 0.0** (M). Only `Misc1/2/3` are non-zero, and those are loot/attachment
tables, not weapons. So there is no equipment record to follow — and there does not need to be.

`skillName2 = records/skills/nonplayerskills/passive/damagebase_physical04.dbr` at
`skillLevel2 = 'charLevel*1'`. Class `Skill_Passive`, `unarmedOnly = **True**`, `FileDescription
'Default Phys Dmg for Heroes and Bosses'`, `skillMaxLevel 200` (all M). **This is the melee payload.**

| field | cl 16 (commission) | **cl 18** | cl 19 | grade |
|---|---|---|---|---|
| `offensivePhysicalMin` | 123.0 | **136.0** | 144.0 | M |
| `offensivePhysicalMax` | 155.0 | **175.0** | 183.0 | M |

**Note this record *does* carry a real min–max range** — unlike the three skill records above. The
melee swing rolls; the specials do not.

Plus, on the same record: `offensivePhysicalModifier 15.0` at `offensivePhysicalModifierChance 10.0`
(a 10 % proc for +15 % physical, M).
Plus `primordian_passive` rank 5: flat **`offensiveColdMin 20.0` / `offensiveColdMax 46.0`** added to
attacks (M).

**Composed — Normal / 1-player effective (C):**

| charLevel | physical | + passive cold | **total per swing** |
|---|---|---|---|
| 16 *(commission's premise)* | 32.3 – 40.7 | 4.9 – 11.4 | 37.2 – 52.0 |
| **18** *(established)* | **37.8 – 48.7** | **5.2 – 12.1** | **43.1 – 60.8** |
| 19 | 41.2 – 52.4 | 5.4 – 12.4 | 46.6 – 64.8 |

**Independent corroboration of the whole composition operator.** `gd-l13-reference-envelope.md` §1b
found, across a **154× HP span** of Act-1-Normal monsters, that *every* tier's base attack lands in a
**35–85** band. **43.1–60.8 sits squarely inside it** — and that band was derived from a different
record set (the trash/champion/hero ledger), so this is not circular. The ×0.2625 factor is doing
real work and is not an artifact.

Cadence for this payload is unchanged from the parent artifact §2.2 (weighted 1.369 s lock inside a
1.719 s cycle, 79.6 % rooted) — **except while `primordian_icearmor` is up**, when +35 % attack speed
compresses it (§4.2). That interaction is new and is not in the fixture.

---

## 6. Do the carried-ext numbers survive? **No.**

| skill | carried-ext | what it actually is | correct (rank 5, raw) | correct (rank 5, Normal/1p effective, cl 18) |
|---|---|---|---|---|
| `primordian_wave` | **122 / 210** | **the rank-4 values, exactly** | **153 / 272** | **42.6 / 71.4** (total 114.0) |
| `chillbane_blizzard` | **58 / 111** | **the rank-4 values, exactly** | **76 / 137** | **21.1 / 36.0** (total 57.1 per drop) |

**Diagnosis (this is the provenance the commission said was unclear).** Both pairs reproduce
`offensivePhysicalMin[3]` and `offensiveColdMin[3]` to the unit. Rank 4 is what
`skillLevel = 'charLevel/4+1'` returns when `charLevel` is bound to the **player's** level 13
(`int(13/4)+1 = 4`). The formula binds the **monster's own** level, which is 18–19 → **rank 5**
(§1.2). The carried-ext values are therefore *correct extractions from the right fields of the right
records, evaluated against the wrong variable.* That is a better provenance than "unclear" — whoever
produced them read the DB properly and made one substitution error.

**Three further defects, each larger than the rank error:**

1. **No damage stage.** They are raw array values. The Normal / 1-player factor is **×0.2625**
   (§1.3) — a 3.8× overstatement, dwarfing the ~25 % rank error. Whether the fixture wants raw or
   effective is the conductor's call; the numbers must be labelled either way, and carried-ext is
   labelled neither.
2. **No riders.** The wave's 3.0 s cold DoT and its 30 % / 3 s damage-reduction debuff are absent;
   the blizzard's 30 % / 5 s total-speed slow is absent. On the blizzard the slow is worth more than
   the damage.
3. **No delivery model for the blizzard.** A per-drop number without 6-per-volley, a 2.0 s cadence,
   an 8.0 s duration, an 8.0 u scatter and a 1.32 u splash radius is not usable. Expected damage per
   cast against a stationary player is ≈ **37–46**, i.e. about one landed drop — an order of
   magnitude away from what a naïve reading of "58 / 111" implies.

**If the stage-2b build needs one number per skill, these are them (Normal / 1p, charLevel 18):**
wave **114 impact + 14.8 DoT/3 s + a 30 %/3 s damage debuff**, once per cast, one application per
target · blizzard **57.1 per drop, ~1 drop landed per cast on a stationary player, + 30 %/5 s slow**.

---

## 7. Corrections owed to already-banked artifacts

| artifact | claim | correction |
|---|---|---|
| `2026-07-30-wr3-nova-star-geometry.md` §5 | "difficulty-pak modifier to projectile speed: **none** — the Normal/1p slice touches attack speed (−10 %), run speed (−18 %), cast speed (−8 %) **and nothing projectile-side**" | True of projectile **kinematics**. **False of damage.** The same record carries `offensiveTotalDamageModifier −25.0`, `offensiveSlowColdModifier −38.0`, `offensiveFreezeModifier −20.0` at slot 0. The star note's §6.2 rank-5 frigidring block (148 phys / 247 cold / 77 DoT / 1.3–1.8 s freeze) is **raw**; at Normal/1p it composes to **41.2 / 64.8 / 12.5 over 2 s / 1.04–1.44 s freeze** (cl 18). The *geometry* in §8 of that note is untouched. |
| `2026-07-30-wr3-nova-star-geometry.md` §6.2 | "Boss `charLevel = 'charLevel*1+3'` → at Matt's L13, boss level **16**" | Boss charLevel is **18–19** (§1.2), via the `p_wightmire_slitha01` → `lv6_hero` proxy chain, anchored by the envelope note's measured `lifeAndMana` 15,822. **Rank 5 is unaffected** — it is invariant over 16–19 — so no §6.2 payload figure changes. |
| commission brief (this cycle) | "Boss level at Matt's referent session: **16** … re-derive each skill's rank at level 16" | Same correction. Ranks re-derived and land on **5** anyway. The premise is wrong; the instruction's output is right. |
| `2026-07-30-wr3-stage2-referent-extraction.md` §2.2 | root motion profiled for the two melee clips only | `slith01_attack_special_sunder` (the wave) carries **1.388 / 0.964 / 0.726** root translation range with **net displacement 0.0** — an in-place lunge-and-return, not a static commit (§2.4). |

---

## 8. Knowledge gaps not resolved

| id | gap | why it resisted | impact |
|---|---|---|---|
| **U-B1** | Is the blizzard's 213-per-drop block applied **whole** per drop or **divided by 6**? | `projectileUsesAllDamage` is False on 64/64 records in the class — no discriminating power; template description empty | **Largest open magnitude in the note.** Whole = 57.1 effective/drop; divided = 9.5. **Lean: whole** (divided puts it below the game's own trash floor). |
| **U-A1** | Sign convention of `offensiveSlowDamageMult` — target deals 30 % less, or takes 30 % more? | empty template description; no corpus contrast isolates it | Decides whether the wave is a damage event or a damage-*and*-tempo event. **Lean: target deals less**, per the `offensiveSlow<X>` family convention. |
| **U-B2** | Does the game draw a pre-impact ground telegraph for the blizzard? | no FX-pak, decal, shadow or warning field on either record | If yes, the warning window exceeds 0.833 s. **Lean: no — the falling orb *is* the warning.** |
| **U-B3** | Is `dropVariation 3.0` positional jitter or drop-height (landing-time) jitter? | template description empty; the corpus correlates it weakly with both `dropRadius` and `dropHeight` | Decides whether a volley lands simultaneously or staggered over ~0.25 s. **Not used in any figure.** Lean: positional. |
| **U-C1** | Can the boss move or attack out of an `instantCast` buff animation? | `instantCast` description empty; engine-side | Decides whether icearmor costs the boss ~1.8 s of tempo or nothing. Root motion is 0 either way. **Lean: committed.** |
| **U-3** *(carried)* | `'MediumRange'` / `'LongRange'` have no exact match in `gameengine.dbr`'s range table | string enum → numeric mapping is engine-side | affects cast-trigger radii for wave (assumed `moderateRange 9.0`) and blizzard (assumed `longRange 15.0`) |
| *(carried)* | Player-side werewolf-form animation set is GDX3-`Creatures.arc`-only; all player timings remain **human form** | parent artifact §5 U-1; asset pull pending | affects the 7.97 u/s used in every dodge-cost figure |

---

## 9. Source list

All read-only, all local pinned binaries, accessed 2026-07-30.

| # | source | note |
|---|---|---|
| 1 | `…/grim-dawn-edition-II-20260724/database/database.arz` | SHA-256 `8cdeff128422c7652780…`; every record resolves here |
| 2 | `…/gdx1|gdx2|gdx3/database/GDX*.arz` | swept for overrides — **none found on this chain** |
| 3 | `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` | `skill_attackwave.tpl`, `skill_buffattackradiusdrop.tpl`, `skill_buffselfduration.tpl`, `templatebase/parameters_offensive.tpl`, `templatebase/skill_activated.tpl`, `templatebase/skill_projectilebase.tpl` |
| 4 | `/Users/admin/Games/vendor/grim-dawn/resources/Creatures.arc` | `slith01_cast_attack_01.anm`, `slith01_attack_special_sunder.anm` |
| 5 | `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` | 964 fields; skill slots, equip slots, `charLevel` |
| 6 | `records/skills/nonplayerskills/bossskills/primordian_wave.dbr` | 281 fields, full dump |
| 7 | `records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr` | 726 fields |
| 8 | `records/fx/skillsother/projectile/blizzard_projectilefx.dbr` | 33 fields, all listed — **zero damage fields** |
| 9 | `records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr` | 641 fields |
| 10 | `records/skills/nonplayerskills/passive/damagebase_physical04.dbr` · `…/armorbase05.dbr` · `…/damage_totaladjuster.dbr` · `…/resists_heroboss.dbr` · `…/bossskills/primordian_passive.dbr` | the melee + modifier chain |
| 11 | `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` | 672 fields; slot-0 vector extracted in full |
| 12 | `records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr` · `records/proxies/lv6_hero.dbr` | the spawn-level chain (§1.2) |
| 13 | `records/creatures/enemies/anm/anm_slith.dbr` · `records/creatures/pc/malepc01.dbr` · `records/game/gameengine.dbr` | animation table, player `actorRadius 0.32`, range constants |
| 14 | corpus census — **64** `Skill_BuffAttackRadiusDrop` records, all four DBs | explosion-radius universality, `targetingMode` crosstab, `dropRadius == 0` partition, `skillTargetRadius` monotonicity |
| 15 | corpus census — **1,525** skill records declaring `projectileUsesAllDamage`, all four DBs | flag-semantics control test (§3.1) |
| 16 | corpus census — **1,307** `Monster` records, base DB | `armorbase0N` carried by 93.4 % (§1.3) |
| 17 | sibling artifacts — `wr3-stage2-referent-extraction.md`, `wr3-nova-star-geometry.md`, `gd-l13-reference-envelope.md` | prior M/C figures reused and, where wrong, corrected in §7 |
