# Research — Grim Dawn level-13 reference envelope (WR3 calibration referent) — 2026-07-30

**Mode:** A (analytical / primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR)
**Authority:** Matt's signed target-state ruling **R-WR3-2**
**Access mode:** read-only throughout. Writes confined to this note and
`legolas/scratch/2026-07-30-gd-l13-envelope/`.

**Companions (this note stands on them, and corrects one):**
- `legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` (the L12 ledger — **its HP column is corrected here**)
- `legolas/notes/2026-07-28-kitcal1-g7-gdc-save-findings.md` (the `.gdc` fixture parse — supplies the measured anchors)

**Grading key:** **M** = MEASURED (read verbatim from `.arz`/`.gdc`) · **D** = DERIVED (computed;
operator stated) · **E** = bounded ESTIMATE (assumption named) · **U** = UNRESOLVED.

---

## Summary

Five things, in order of how much they should change what happens next.

1. **A composition rule in the banked L12 ledger was wrong, and a measured anchor caught it.** The
   G-5a note composed monster HP by *summing* the difficulty/multiplayer pak's
   `characterLifeModifier` into the skill-passive pool. Confronted against the one **measured**
   monster pool we possess — Primordian, **15,822**, read off the `.gdc` `play_stats` block at
   player level 13 — the additive rule overshoots by **1.8×**. The **multiplicative** rule (pak as a
   separate stage) lands at **15,891, a 0.4 % miss**. Every HP figure in G-5a is therefore **~1.45×
   too high for trash and ~1.81× too high for champion/hero/boss.** Corrected ledger in §2.
2. **This retires G-5a's largest open caveat by unifying the rule.** G-5a had already concluded, *by
   contradiction*, that the pak's damage modifier must be a separate multiplicative stage. It kept
   life additive. One rule now governs both, and the life half is confirmed by measurement rather
   than by elimination.
3. **Boss:player HP is 22.8× against the pool the player actually fought in** (werewolf-form 1600),
   or 48.1× against human-form 759. The fixture's 19.5× is a **13 % under-read** of the werewolf
   figure — materially close.
4. **The fixture's heavy hit is the outlier, not its HP ratios.** GD's worst *observed* hit across
   the entire run was **260.498 (M)** = 34.3 % of the human pool / 16.3 % of the werewolf pool. The
   fixture's nova reaches ~55 % of pool — **1.6–3.4× larger as a pool fraction** than anything GD
   L13 actually threw.
5. **The player does not outrun this boss.** Player `characterRunSpeed` **0.93 (M)** vs Warden ph.1
   **0.943** and ph.2 **1.148** after the pak's −18 %. Ratio **0.99 and 0.81** — parity, then
   deficit. The fixture's 5.75 vs 4.025 m/s (**1.43×** player advantage) inverts GD's relationship.

A sixth finding is off-commission but load-bearing enough to state: **`werewolf1.dbr` carries no
`characterLife` field at any rank (M).** It is a pure form-swap — replacement mesh, anims, granted
skills, 170 energy. The 759 → 1600 HP step at the R2/R3 boundary is **not** the werewolf toggle.
This closes G-7's **U-1** and falsifies the charter's working hypothesis. See §5.

---

## 1. The envelope table

Player level 13, Grim Dawn base campaign + expansions, **Normal difficulty, 1 player**, Act 1
(Warden Krieg territory). Fixture column is the diff target supplied in the commission — not
researched here.

### 1a. Player

| Our metric | GD L13 value / range | Grade | Source | Fixture | Diff |
|---|---|---|---|---|---|
| Health pool — human form | **759** | **M** | play-test v1 telemetry (charter) | 759 | **exact (this is the referent)** |
| Health pool — werewolf form | **1,600** | **M** | play-test v1 telemetry | — | the form the boss was fought in |
| Base attribute pool (pre-gear, pre-mastery) | **454** | **M** | `.gdc` `character_bio`; closes to the byte from `playerlevels.dbr` | — | the layer *below* max HP |
| — of which: mastery bar r5 | +135 life | M | `_classtraining_class10.dbr` | — | |
| — of which: weapon | +220 life | M | `b015b_blunt.dbr` `characterLife` | — | one item = 29 % of the human pool |
| Energy pool | **250** | **M** | `.gdc`; `manaIncrement` 16/pt, 0 pts spent | — | |
| Energy pacing | werewolf 170 to enter · Feral Claws **5**/hit · Rip and Tear **42** | M | `werewolf1/…claws/…charge.dbr` | — | entry costs **68 % of the pool** |
| Attributes | physique 122 / cunning 74 / spirit 50 | M | `.gdc` | — | |
| Damage per hit (Feral Claws r16) | **≈ 310** | **D** | 237 flat Pierce→Chaos + (14–40)×1.50×(1+122/245) + poison | — | corroborated: `.gdc` `lastHit` **312.888 (M)** — 1 % |
| Damage per hit (Rip and Tear r16) | **≈ 820**, ~1,070 on crit | D | 375 flat + 295 % weapon + 270 bleed/3 s | — | corroborated: `greatestDamageInflicted` **1093.807 (M)** |
| Attack cadence | **1.0 – 2.0 /s** | **E** | base interval is in the `.anm` binaries, **not** the `.arz` — see U-1 | — | **the envelope's weakest number** |
| Single-target DPS | **310 – 620 HP/s** (central ≈ 450) | **E** | 310/hit × cadence band | ~250 HP/s | fixture is **at or below GD's floor** |
| Cleave breadth | up to **5 targets**, **150°** arc | M | `…claws.dbr` `skillTargetNumber` 5, `skillTargetAngle` 150 | — | pack throughput up to 5× single-target |
| Run speed | **0.93** (engine multiplier) | **M** | `records/creatures/pc/malepc01.dbr` | 5.75 m/s | absolute m/s not in `.arz`; use **ratios** |
| Gap-closer | Rip and Tear: **+200 % run**, 4 s cooldown, 0.5 s knockdown | M | `…skill02_charge.dbr` | — | player has one too |

Class-spread caveat the commission asked for: the fixture is a **single-mastery Berserker
(`playerclass10`, GDX3)** with `masteriesAllowed = 2` and only one taken (M). I did **not**
substitute a 2-3 class spread from community build guides, because at level 13 the dominant term is
the **flat** skill component (237 of ~310 damage per hit is one flat number off one rank array), and
that flat term is per-skill, not per-class. A cross-class spread built from tertiary sources would
have looked more authoritative than it was. Named as a gap in §6, U-3.

### 1b. Monsters — corrected L13 ledger

Spawn levels resolved at `averagePlayerLevel = 13` from `records/proxies/lvN_*.dbr` (M):
weak 12 · normal 12–13 · strong 13 · champion 14 · hero 15–16 · uber-hero 16 · boss 16–17.
`charL` is after the monster record's own `charLevel` remap (M). **HP is the corrected
(multiplicative) figure**; the G-5a column is shown so the correction is auditable.

| Tier | Name | charL | **HP (corrected)** | HP (G-5a, wrong) | dmg/hit | % of 759 | % of 1600 | run |
|---|---|---|---|---|---|---|---|---|
| trash | Walking Dead | 13 | **136** | 198 | 40–50 | 5.9 % | 2.8 % | 0.82 |
| trash | Rift Scourge | 13 | **151** | 221 | 41–51 | 6.0 % | 2.9 % | 0.82 |
| trash | Skeletal Warrior | 13 | **167** | 245 | 35–44 | 5.2 % | 2.5 % | 0.98 |
| trash | Dreadweave Arachnid | 13 | **175** | 256 | 40–50 | 6.0 % | 2.8 % | **1.64** |
| trash | Stonetusk | 13 | **267** | 389 | 68 flat | 8.9 % | 4.2 % | 0.74 |
| trash | Scavenger | 13 | **325** | 475 | 45–52 | 6.4 % | 3.0 % | 0.90 |
| trash | Tainted Hound | 13 | **374** | 546 | 43–54 | 6.4 % | 3.0 % | 1.07 |
| trash | Ghoul | 15 | **448** | 654 | 45–63 | 7.1 % | 3.4 % | 0.82 |
| trash | Bloodsworn Adulant | 13 | **469** | 685 | 34–43 + wpn | 5.0 % | 2.4 % | 0.54 |
| trash | Gargantuan Stonetusk | 13 | **501** | 909 | 37 flat | 4.9 % | 2.3 % | 0.70 |
| trash | Rotting Soldier | 14 | **528** | 772 | 41–54 + wpn | 6.3 % | 3.0 % | 0.74 |
| champ | Fleshwarped Butcher | 15 | **555** | 1,008 | 26–27 | 3.5 % | 1.7 % | 1.03 |
| champ | Fury | 15 | **645** | 737 | 61–85 | 9.7 % | 4.6 % | 0.82 |
| champ | Ironhide Stonetusk | 14 | **804** | 1,460 | 37 flat | 4.9 % | 2.3 % | 0.61 |
| hero | Dreadtusk | 16 | **2,486** | 4,514 | 50 flat | 6.6 % | 3.1 % | 0.53 |
| hero | Charrus | 21 | **4,288** | 6,523 | 44–54 | 6.5 % | 3.1 % | 0.98 |
| hero | Abner | 21 | **5,030** | 7,652 | 37–50 | 5.7 % | 2.7 % | 1.31 |
| **boss** | **Primordian** (measured anchor) | 18 | **15,891** | 28,860 | 63–80 | 9.4 % | 4.5 % | 0.70 |
| **boss** | **Warden Krieg ph.1** | 19 | **15,569** | 28,274 | 38–48 + wpn | 5.7 % | 2.7 % | **0.943** |
| **boss** | **Warden Krieg ph.2** | 19 | **20,940** | 38,029 | 41–51 + wpn | 6.1 % | 2.9 % | **1.148** |
| **boss** | **Warden Krieg COMBINED** | 19 | **36,509** | 66,303 | — | — | — | — |

Warden Krieg resolves at **charLevel 19** when the player is 13 — spawn 16 via `lv7_uber hero`,
then the record's own `(charLevel*1.1)+2` remap (M). Both phases are one encounter:
`warden01.chanceToSpawnOnDeath = 100.0` → `dp_wardenphase2.dbr` (M).

**Weapon-wielder floor (carried from G-5a, unclosed).** Rows flagged `+ wpn` — including **both
Warden phases**, which also carry `weaponScale = 1.3` — roll a weapon at spawn from `lootRightHandItem`
master tables. Their listed damage is the `damagebonus_physical0N` component **only**. Those damage
figures are **floors** (U-2).

### 1c. The ratios that matter

| Ratio | GD L13 | Grade | Fixture | Diff |
|---|---|---|---|---|
| **boss HP : player HP** — vs werewolf pool 1600 | **22.8×** | D | **19.5×** | fixture **−15 %** — close |
| boss HP : player HP — vs human pool 759 | 48.1× | D | — | which pool you pick moves this 2.1× |
| boss HP : player HP — **single phase** vs 1600 | ph.1 **9.7×** · ph.2 **13.1×** | D | 19.5× | fixture ≈ **1.5–2× one GD phase** |
| Boss-tier pool, single phase | ph.1 **15,569** · Primordian **15,891** | D / **M-anchored** | 14,812 · clear 16,235 | **within 5 %** — strong agreement |
| **player TTK on trash** | light **0.22–0.44 s** · mid 0.28–0.56 s · heavy **0.85–1.70 s** | E | — | |
| player TTK on champion | 1.0–2.1 s | E | — | |
| player TTK on hero | 8.1–16.2 s | E | — | |
| **boss fight duration** (both phases) | **59–118 s** | E | **65 s** | fixture at GD's **fast end** |
| boss fight duration (ph.1 only) | 25–50 s | E | — | |
| trash hit ÷ player pool | **2.5–3.4 %** (of 1600) · 5.0–7.1 % (of 759) | D | — | |
| hero hit ÷ player pool | 2.7–3.4 % (of 1600) | D | — | |
| boss base hit ÷ player pool | **2.7–3.0 %** (of 1600) | D | — | |
| **boss heavy hit** (`aethersmash`, ph.2) | **166.1** = **10.4 %** of 1600 / **21.9 %** of 759 | D | 207–415 = **up to 55 %** of 759 | **fixture 1.6–3.4× larger** |
| **worst hit actually taken, whole run** | **260.498** = **16.3 %** of 1600 / **34.3 %** of 759 | **M** | — | the hardest number in this note |
| pack pressure (4 concurrent, `numAttackSlots`) | **180/round** = 11.2 % of 1600 | D | — | pressure is **pack-shaped**, not hit-shaped |
| **player : boss run speed** | ph.1 **0.99** · ph.2 **0.81** | **M** | **1.43** | fixture inverts the relationship |
| hits inflicted : hits received (whole run) | **1606 : 500 = 3.2 : 1** | **M** | — | `.gdc` `play_stats` |
| deaths across the whole run | **2** in 7,096 s | **M** | — | R-WR3-2's "win the majority" is well satisfied in GD |

**The structural headline survives the correction, and sharpens.** Across a **154× HP span**
(136 → 20,940) every tier's base attack lands in a **35–85** band and at **2.3–4.6 % of the
werewolf-form pool**. GD Act-1-Normal differentiates tiers on **HP, armor, resistance, pack size and
burst abilities** — almost never on base hit size. The designers flattened early-game hit magnitude
deliberately: `armorbase03–06` (champion/hero/boss) apply a **−79 %** damage damper at these ranks
against `armorbase01/02`'s **−44 %**, very nearly cancelling the richer `damagebase_physical03–06`
tables they pair with (M).

---

## 2. The composition correction

`records/game/gameengine.dbr` → `monsterAttributePak` →
`records/game/balancingadjustment_mp+difficulty_enemies01.dbr`, Normal/1-player slice (index 0):
`characterLifeModifier = +50 %`, `offensiveTotalDamageModifier = −25 %` (M).
`armorbase01/02` contribute `characterLifeModifier = −58`, `armorbase03–06` contribute **−71**, both
flat across every rank in play at L13 (M).

Two candidate operators, one measured anchor — Primordian, `lifeAndMana` **15,822**, at player
level 13, from the `.gdc` `play_stats` block (M). Primordian's spawn is fixed *independently* by
`p_wightmire_slitha01.dbr` → `lv6_hero` → 15–16, then `charLevel*1+3` → **charLevel 18–19** (M), so
the level was **not** fitted to the answer:

| charL | rule | predicted HP | ÷ 15,822 |
|---|---|---|---|
| 18 | additive `(1 + (−71+50)/100)` | 28,860 | **1.82×** ✗ |
| 18 | **multiplicative `(1−0.71)×(1+0.50)`** | **15,891** | **1.004×** ✓ |
| 18 | pak absent | 10,594 | 0.67× ✗ |
| 19 | additive | 31,185 | 1.97× ✗ |
| 19 | multiplicative | 17,171 | 1.09× ✓~ |
| 19 | pak absent | 11,448 | 0.72× ✗ |

**The adjudication is robust to the residual ambiguity.** Level 18-vs-19 and
`lifeAndMana`-as-life-only-vs-life-plus-mana together move the prediction by ~10 %. The
**operator choice moves it by 180 %.** Multiplicative is the only rule that lands under *any*
combination; additive fails under all. Correction factors: **×0.685** for `armorbase01/02` bearers
(trash), **×0.551** for `armorbase03–06` bearers (champion/hero/boss).

The tightest reading — charLevel 18, life-only — is a **0.4 %** miss and is also the only one
consistent with `lv6_hero`'s minimum spawn of 15. I report it as the best estimate without claiming
the 0.4 % as precision: **rank truncation alone (§6, U-4) is worth ≤ 4 %.**

**Why this matters beyond one number.** G-5a reached the multiplicative conclusion for *damage* by
contradiction (additive drove `zombiemutated_a01` and both Warden phases to negative damage) and
explicitly flagged that "multiplicative is not thereby proven, only left standing." One uniform
rule now governs life and damage, and the life half rests on a measurement. The pak is an
engine-level global stage, not a peer of the skill-passive pool.

---

## 3. Combat-rhythm norms

All fields **M** unless marked. Warden Krieg's controller is
`records/controllers/enemy/controller_boss_warden.dbr`; trash comparison is
`controller_zombiea01.dbr`.

### 3a. Attack commit and telegraphs

GD does animate-lock attacks, but the **commit duration is not in the `.arz`** — every
`*AttackAnimSpeed*` field is a **multiplier of 1.0** and the interval lives in the `.anm` binaries
this lane does not parse (U-1). What the `.arz` *does* carry is the telegraph geometry, and it is
explicit:

| Ability | Class | Telegraph / commit evidence | Reach |
|---|---|---|---|
| `aethersmash_warden` (ph.2 heavy) | `Skill_AttackRadius` | **`expansionTime = 0.5 s`** — the damage radius grows over half a second; `cameraShakeDurationSecs = 0.5` | `skillTargetRadius` **9.0** |
| `aetherwave_warden` | `Skill_AttackWave` | `waveTime 1.5 s` over `waveDistance 8` → **5.3 units/s — comfortably dodgeable**; `skillCooldownTime 5.0` | 8 |
| `aetherarc_warden` | `Skill_AttackWave` | `waveTime 0.3 s` over 8 → **26.7 units/s — effectively undodgeable on reaction** | 8 |
| `aetherstreak_warden2` | `Skill_AttackWave` | `waveTime 0.5 s` over **16** → 32 units/s; cooldown 5.0 | 16 |
| `wardenspikes1` | `Skill_AttackProjectileBurst` | `distanceProfile = Long` | ranged |

So: **yes, telegraphed heavies — and the tell is spatial expansion (0.5 s), not a wind-up pose.**
The mix is deliberately mixed-fairness: one slow dodgeable wave, one fast unavoidable arc.

### 3b. Gap-closers — both phases have one, and both punish repositioning

| Ability | Effect |
|---|---|
| `warden_charge` (ph.1) | **+120 % run speed**, `skillTargetAngle 90°`, `maxDistanceBuffer 6`, `distanceProfile Melee` |
| `warden2_charge` (ph.2) | same, plus `skillCooldownTime 5.0` |
| `aetherarc_warden` (ph.1) | **−33 % run speed for 3 s** |
| `aetherstreak_warden2` (ph.2) | **−50 % total speed for 4 s**, at 16 units of reach |

The anti-kiting design is legible in the data: a gap-closer per phase **plus** a movement debuff per
phase, the ph.2 debuff being twice as strong at twice the reach. Kiting is available but actively
taxed.

### 3c. Melee-range residency (**D** — inferred from fields, not observed)

| Field | Warden | Trash (zombie) | Reading |
|---|---|---|---|
| `RepositionChance` | **100** | 0 | the boss **always** repositions; trash never does |
| `enemyTooClose` | **0.0** | 5.0 | the boss **never backs off**; trash disengages at 5 units |
| `maxSwingPause` | **0.3 s** | 1.0 s | the boss swings ~**3.3× more continuously** |
| `EmoteBeforePursuingChance` | 20 % | — | a 1-in-5 pre-pursuit tell |
| `RoamBehavior` | **NeverRoam** | Roam (dist 4) | boss holds its arena |
| `ChanceToRespondToDistressCall` | 20 % | 75 % | the boss largely fights alone |

Composite (**D**): a boss that never disengages, always repositions, and pauses only 0.3 s between
swings produces a fight where the player is at melee range **most of the time**, punctuated by
forced exits on the 5 s-cooldown waves and the expanding nova — call it **~70–80 % melee residency**,
with repositioning driven by *boss ability cooldowns* rather than player preference. This is the
softest claim in the note: it is a reading of controller fields, not a measurement of play. Flagged.

### 3d. Movement and leashing

| Datum | Value | Grade |
|---|---|---|
| Player run speed | **0.93** | M (`malepc01.dbr`) |
| Warden ph.1 / ph.2 run speed | 1.15 / 1.40 raw → **0.943 / 1.148** after pak −18 % | M |
| **Player : boss speed ratio** | **0.99 / 0.81** | D |
| `MaxPursuitDistance` (both Warden and trash) | **75.0** units | M |
| `PursuitTime` | **10,000 ms** | M |
| `FleeBehavior` | **NeverFlee** (both) | M |
| `ViewDistance` / `InnerViewDistance` | 15.0 / 4.0 | M |
| `gameengine.alertDistance` / `bossRange` | 6.0 / 32.0 | M |
| Monster run speed, all tiers | uniformly **−18 %** on Normal | M |
| Charge abilities | **+120 %** run for the duration | M |

**Answer to the commission's question: the player does not outrun this boss.** Ph.1 is a dead heat
(0.99); ph.2 is **19 % faster than the player** — and layers a −50 % slow on top. Bosses **do**
leash: 75 units of pursuit, capped at 10 s, and they never flee. The fastest thing in Act 1 is not a
boss but a **Dreadweave Arachnid at 1.64 (1.76× the player)**.

Note the units: `characterRunSpeed` is an engine multiplier against an animation-driven base that is
**not in the `.arz`**. Absolute m/s is unavailable from this source — **compare ratios, not
magnitudes**, when diffing against the fixture's 5.75 / 4.025 m/s.

---

## 4. Pack composition — where the pressure actually comes from

`numAttackSlots = 4` caps simultaneous melee engagement (M). Act-1 pool sizes are literal —
`proxypoolequation_01.dbr` is an identity pass-through on Normal (M) — and run **1–8** (`p_zombie_n`),
**2–9** (`p_beasts_boar_n`), **8–16** (`p_undead_skeletons_amb_n`), with `championChance` 0–50 %.

So the pressure term is **4 × ~45 = 180 damage per engagement round = 11.2 % of the werewolf pool**,
against single hits worth 2.5–3.4 %. Any fixture that reproduces GD's *hit size* but not its
*concurrency* will feel far safer than GD did. `distressCallRange = 16.0` with
`distressCallTime = 2000 ms` and `maxDistressCalls = 1` means packs also **recruit**, once.

One roster fact specific to this level: `p_zombie_n` gates `minPlayerLevel3 = 12`,
`minPlayerLevelChampion4 = 12`, `maxPlayerLevel9 = 7`, `maxPlayerLevelChampion7 = 13` (M) — **the
Act-1 roster is actively churning at exactly player level 12–13.** Level 13 is not a static
sample point.

---

## 5. Off-commission but load-bearing: the 759 → 1600 step is not the werewolf

`records/skills/playerclass10/werewolf1.dbr` — every non-zero field, at rank 16 (**M**):
`Class = Skill_Shapeshift`, `skillManaCost = 170`, `activeSkillSet = 1`, `notDispelable = True`,
`grantedSkills = [claws, charge]`, `replacementMeshMale`, `replacementAnims`,
`replacementFootsteps`, `replacementSounds`, `skillMaxLevel 16`, `skillTier 1`, FX/icon/sound
records. **There is no `characterLife`, no `characterLifeModifier`, no defensive field of any kind
at any rank.**

This **closes G-7 U-1** and **falsifies** the charter's reading (banked at G-7 §7) that the 2.11×
max-HP step at the R2/R3 boundary is the Werewolf toggle. Werewolf changes the *skill set* and the
*model*; it does not change the pool.

What the `.arz` *does* account for, on the human-form side (M): base attribute pool **454** +
mastery bar rank 5 **+135** + weapon **+220** = **809**, against the measured **759** — a **+6.6 %**
overshoot, comfortably inside unmodelled gear/affix interactions. So **759 is reconstructible; 1600
is not**, from any record in the werewolf chain.

I am not proposing what does explain it — that is gandalf's call. The candidates the data leaves
open are a further gear/level event inside R3, or a telemetry semantics change in what "max HP"
counts. **Flagged, not guessed.**

Also closed from G-7 U-1: the Pierce→Chaos consequence is **real and large**. Feral Claws r16 carries
`offensivePierceMin = 237.0` and Rip and Tear r16 `offensivePierceMin = 375.0` (M) — and Blight of
Ch'thon converts **100 %** of Pierce to Chaos. **The flat Pierce component is ~76 % of the player's
per-hit damage** (237 of ~310). Modelling this fixture's damage as Pierce is wrong by three quarters
of its output.

---

## 6. Confidence and gaps

### High confidence — MEASURED, no inference
- Player pools, attributes, energy, run speed 0.93, all skill ranks, all rank-array values quoted.
- Worst hit taken all run **260.498**; hits 1606:500; deaths 2; `lastHit` 312.888. All `.gdc`.
- Primordian **15,822** — and its spawn chain fixed independently of the fit.
- All monster spawn equations, `charLevel` remaps, resistances, pool sizes, controller fields,
  ability geometry (radii, wave times, cooldowns, speed debuffs).
- `werewolf1` carrying zero stat fields.

### Medium confidence — DERIVED, operator stated
- **Corrected HP ladder.** Multiplicative operator now anchored to one measurement at one level.
  It is one anchor, not a curve — a second measured pool at a different level would upgrade this
  from "adjudicated" to "validated." Cheapest source: a second `.gdc` with a different
  `greatestMonsterKilled`.
- Player per-hit ≈ 310 (independently corroborated to 1 % by `lastHit`) and Rip and Tear ≈ 820/1,070
  (corroborated by `greatestDamageInflicted`).
- Boss ability damage: flat components only, after `tdmMult`, **before** weapon and before the
  8 %-chance +35 % physical spike. **Floors, not expectations.**

### Low confidence — bounded ESTIMATE
- **DPS 310–620 HP/s and every TTK / fight-duration figure derived from it.** The 2× width is
  entirely the attack-cadence unknown (U-1). If a single number is needed, the central **≈450 HP/s**
  → Warden ≈ **81 s**.
- Melee-residency ~70–80 % (§3c) — a reading of controller fields, not observed play.

### UNRESOLVED — flagged, not guessed

| # | Item | What would close it |
|---|---|---|
| **U-1** | **Base attack interval in seconds.** All `*AnimSpeed*` fields are 1.0 multipliers; the duration is in the `.anm` binaries. A tertiary Steam-forum claim ("100 % attack speed = 2 attacks/s") is the only external bound found and is **not** treated as authoritative. **This is the single highest-value follow-on** — it collapses the DPS band and every TTK with it. | An `.anm` parse, or one timed in-client observation. |
| **U-2** | **Weapon-wielder damage floors.** Both Warden phases plus 5 trash protos roll a weapon at spawn (`weaponScale 1.3` on Warden). Listed damage is the bonus component only. | Walk the `lootRightHandItem` master tables; Warden's `gear_warden_mace.dbr` is fixed in-corpus and could be resolved exactly. |
| **U-3** | **Cross-class spread at L13.** Deliberately not fabricated from build guides (§1a). | A second play-test fixture on a different mastery — far better evidence than any secondary source. |
| **U-4** | **Rank truncation.** `int()` assumed on equations like `(charLevel*.25)+1`. Round-half-up shifts some ranks by 1; effect ≤ 4 %. | Not worth closing at this precision. |
| **U-5** | **`lastHitBy` 273.704 attributed to a Plague Walker**, whose derived worst single hit is 40–50 — a **5.5× tension**, and it also *exceeds* `greatestDamageReceived` 260.498, which should be impossible for a single hit. Plague Walker carries three poison abilities (`zombie_barf` 63.3, `poisongib` 56.9, `acidpool1` 38.0 — sum 158.2, still short) on `specialAttackChance 50 %`, `specialAttackDelay 3.0 s`. Most likely the field aggregates a poison **total** or a multi-component payload rather than one impact, but **I could not close it.** | `play_stats` v12 field-semantics reference, or a second save to diff. **Until closed, prefer `greatestDamageReceived` 260.498 as the worst-hit envelope datum.** |
| **U-6** | **grimtools cross-check unavailable.** `grimtools.com/monsterdb/276` renders client-side; static fetch returns an empty template (accessed 2026-07-30). G-5a previously confirmed the underlying `monsterdb.js` carries the *same* `.arz` payload we parse — so it is not an independent source of *values*, only of parse fidelity. | Headless-browser render, or reversing the minified composition code. |
| **U-7** | **Veteran mode not modelled.** Matt's play-test was Normal (`difficulty = 128`, `greatestDifficulty = 0`). Veteran is a Normal-difficulty toggle whose adjustment record I did not locate. If the run was on Veteran, every monster figure here is a **floor**. | Locate the Veteran adjustment record; confirm the toggle state with Matt. |

---

## 7. Source list

**Primary — datamined game corpus** (read-only, `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`):
`database/database.arz` · `gdx1/database/GDX1.arz` · `gdx2/database/GDX2.arz` · `gdx3/database/GDX3.arz`
(SHA-256 per G-5a §Provenance); `*/resources/Text_EN.arc` for display names.

Records newly read for this note (beyond G-5a §5):
`records/creatures/pc/malepc01.dbr` · `records/creatures/pc/anm_werewolf.dbr` ·
`records/skills/playerclass10/{werewolf1, werewolf1_skill01_claws, werewolf1_skill02_charge, onslaught1, _classtraining_class10}.dbr` ·
`records/items/gearweapons/blunt1h/b015b_blunt.dbr` ·
`records/controllers/enemy/{controller_boss_warden, controller_zombiea01}.dbr` ·
`records/skills/nonplayerskills/{attackradius/aethersmash_warden, path/aetherwave_warden, path/aetherarc_warden, path/aetherstreak_warden2, attackcharge/warden_charge, attackcharge/warden2_charge, aoe/aetherring_warden, aoe/aetherexplosion1, bossskills/wardenspikes1, path/zombie_barf, attackprojectile/poisongib_zombie, aoe/acidpool1}.dbr` ·
`records/creatures/enemies/bios/bio_boss_standard_01.dbr` ·
`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/proxies/boss&quest/{proxy_wightmire_slitha01, boss&questpools/p_wightmire_slitha01}.dbr` ·
`records/proxies/lv1_weak.dbr … lv8_boss.dbr`.

**Primary — fixture save:** `player.gdc`, SHA-256
`0be3a99f6ead980210a5c06cd12a09bfe51235c09b9da7d41745fa4eacd5ee91`, via G-7's parse artifacts.
**Primary — play-test telemetry:** charter §14, play-test v1 (759 / 1600 / 7,094 s / boss-tier clear).

**Tertiary — consulted, and where it did and did not land:**
- `grimtools.com/monsterdb/276` — **JS-gated, no data recoverable** (2026-07-30). U-6.
- `steamcommunity.com/app/219990/discussions/…` — "100 % attack speed = 2 attacks/s; +50 % = +1/s."
  Forum-tier; used only as an outer bound on U-1, **not** as the basis of any figure.
- `grimdawn.fandom.com/wiki/The_Warden_(creature)` — confirms the two-phase structure and Krieg's
  aether/vitality vulnerability qualitatively; **carries no per-level numbers**.
- `grimdawn.fandom.com/wiki/Game_Mechanics`, `grimdawn.com/guide/character/masteries/*`,
  `techraptor.net`, `earlyguides.com` — searched for L13 class-spread stats; **none carry
  level-specific health or DPS values.** This is why U-3 is a declared gap rather than a filled row.
- Movement-speed threads (Steam, Crate forums, Nexus "Run Speed" mod) — corroborate that GD's base
  run speed is expressed as ~0.92–0.93 and that the display cap is 135 %; consistent with the
  measured 0.93, but the `.arz` is the authority used.

**Scratch artifacts:** `agentic_orchestration/legolas/scratch/2026-07-30-gd-l13-envelope/`
(`l13.py` — spawn-level + anchor-validation harness; `ledger13.py` — corrected ledger generator).

---

## 8. Handoff

**To gandalf (RUN-CONDUCTOR).** Four items want a ruling, in priority order:

1. **Which player pool is the referent** — 759 or 1600. It moves boss:player from 48.1× to 22.8×
   and is the single largest lever on how the fixture reads against R-WR3-2.
2. **The G-5a HP column is superseded** by §1b. Anything already built on those numbers is high by
   1.45× (trash) / 1.81× (champion+). This warrants a correction note against G-5a rather than a
   silent overwrite.
3. **The heavy-hit diff is the real gap** (§1c): the fixture's nova is 1.6–3.4× GD's worst *observed*
   hit as a pool fraction, while its HP ratios and fight duration are within ~15 %.
4. **The werewolf HP hypothesis is dead** (§5). The R2/R3 step needs another explanation.

**To jack-ryan**, if any of this is ratified: U-1 (attack cadence) is the load-bearing unknown behind
every TTK figure in §1c, and U-5 is an unclosed internal inconsistency in a MEASURED field.

**No canonical doc amended by this note.**

---

**Signed:** legolas (UNKNOWN-RESEARCHER), 2026-07-30.
