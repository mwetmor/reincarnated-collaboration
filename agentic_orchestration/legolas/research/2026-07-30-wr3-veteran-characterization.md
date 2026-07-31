# Research — WR3 Veteran characterization: the full price of the referent world — 2026-07-30

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf, RUN-CONDUCTOR, run WR3-KITE-COMMIT (charter R-WR3-29 / R-WR3-30)
**Matt, verbatim:** *"Veteran setting is an optional modifier for normal mode which increases monster
stats, density, hero spawns, and grants +10% experience. I must have been playing on veteran. Can you
research this?"*
**Sources:** vendor pin `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (`database.arz` +
GDX1–3), `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` and `Game.dll` (65,229 strings),
the referent `player.gdc`, three third-party `.gdc` saves. Web used as **tertiary** corroboration only.
**Scratch (read-only):** `agentic_orchestration/legolas/scratch/2026-07-30-wr3-veteran/`
(`v1_dump.py` … `v13_degeneracy.py`)

**Grades:** **M** = measured/read directly from a primary artifact · **C** = concluded from M by stated
arithmetic · **D** = derived with a modelling assumption · **T** = tertiary (community/official web)

---

## 0. VERDICT

**Every one of Matt's four channels is confirmed at the record, and one of them lands on the exact
number he quoted. But the finding that matters most is not in his list.**

1. **Matt's lookup is corroborated field-by-field (M).** Damage/stats: `+40 %` total damage, `+10 %`
   physical, `+140 %` life, `+25` OA, `+15` DA, `+5 %` attack/cast/run speed. Density: **`spawnMaxAdj
   +1`**. Hero/champion spawns: **`spawnChampionMaxAdj +2`**. XP: **`challengeExperienceEquation` is
   the base XP equation with a literal `*1.1` appended** — *the +10 % is one multiplication sign in
   `records/game/experienceformulas.dbr`*, and it evaluates to exactly 1.1000× at every parameter I
   tested. The record is reached from `gameengine.dbr → challengeAdjustment`, whose template
   description reads **"GameAdjustment for Normal"** (M) — the corpus itself calls Veteran a Normal-mode
   overlay.

2. **U-3 is NOT closed, and it is the load-bearing unknown of the whole cascade.** The Veteran record
   is `Class = GameAdjustment`, a **third** class distinct from both `AttributePak` (the difficulty pak)
   and `Mutator` (the Crucible/SR system). `Game.dll` exports `GameEngine::GetChallengeAdjustment()`
   returning `const GameAdjustment&` and **no consumer symbol at all** — the application site is
   inlined. I give a structural argument for **own-stage ×1.40** (§3) and grade it **C, lean**, not M.

3. **THE HEADLINE — the cl-13/rank-4 + Veteran cell and the charter's existing cl-18/rank-5 no-Veteran
   column are the SAME FIXTURE to within 5 %, on every channel.** Mean ratio **0.951**, spread
   0.909–0.971, dispersion ≤4.4 % across nova/wave/blizzard/melee/DoT (§4.3). The HP degeneracy the
   difficulty probe found at 0.4 % is not a coincidence of one anchor — **it is a property of the whole
   kit.** Consequence for conduct: **U-4 (boss level 13 vs 18) does not need to be closed before
   stage-2c, provided U-3 resolves to own-stage.** The run has been prioritising the wrong unknown.

4. **U-4 advanced, one branch killed, a new branch surfaced.** `greatestMonsterKilledLevel` is
   **engine-truth, not community convention** — it appears as a literal string in `Game.dll` beside
   `PlayStats::GetGreatestMonsterKilledLevel()` / `SetGreatestMonsterKilledLevel(unsigned int)`, in a
   co-named triple with Name and LifeAndMana, both unambiguously monster-side. **"Player level at kill"
   is dead.** But the field does not distinguish *proxy spawn level* from *post-remap `charLevel`*, and
   the spawn reading yields a **third cell, cl 16 / rank 5**, which I have priced. (Same sweep also
   **falsifies R-WR3-26(6)'s U-1 premise**: `greatestDamageReceived` and `greatestDamageInflicted` are
   *also* engine-truth strings in `Game.dll`. §6.2.)

5. **The encounter mix has a MEASURED answer sitting in the referent save, and nobody had read it.**
   `play_stats` carries **`championKills = 7`** and **`heroKills = 3`** against **882 kills** — the
   referent player's own elite mix, **1.13 %**, measured. Veteran's modelled uplift is **+73 % champions
   / +56 % hero-per-pack / +16 % bodies per pack** (§5). A Veteran-blind trash fixture under-prices the
   mix by those factors — but the *absolute* rate must be pinned to 7/3/882, not to my model, which
   over-predicts champions 10× and is honest about it.

---

## 1. Q1 — complete Veteran enumeration

### 1.1 Wiring — three records, three distinct classes, one chain

```
records/game/gameengine.dbr
    monsterAttributePak  → balancingadjustment_mp+difficulty_enemies01.dbr   Class=AttributePak   (12-slot array)
    challengeAdjustment  → balancingadjustment_challengemode_enemies01.dbr   Class=GameAdjustment (scalars) ← VETERAN
records/game/gameascendant.dbr                                                        [GDX3]
    ultimateChallangeAdjustment → balancingadjustment_ultramode_enemies01.dbr Class=GameAdjustment ← ASCENDANT
records/game/gameengine.dbr
    experienceRecord     → records/game/experienceformulas.dbr                        ← the XP channel
```
All **M**. Template descriptions (`templates.arc`, M): `challengeAdjustment :: "GameAdjustment for
Normal"` · `ultimateChallangeAdjustment :: "GameAdjustment for Ultimate+"` (Crate's typo preserved).
The inbound-reference sweep over all four archives found **exactly these two live citations** plus five
`records/sandbox/arthur/archive/gameengine *.dbr` historical copies (M — dead, not loaded).

### 1.2 The Veteran record — EVERY nonzero field

`records/game/balancingadjustment_challengemode_enemies01.dbr`, 608 fields, **14 nonzero** (M,
`v1_dump.py`). This is the complete list; there is nothing else on the record.

| field | value | channel | what it does |
|---|---|---|---|
| `offensiveTotalDamageModifier` | **+40** | damage | all outgoing monster damage |
| `offensivePhysicalModifier` | **+10** | damage | physical component only, on top of the above |
| `characterLifeModifier` | **+140** | stats | monster HP **×2.40** |
| `characterOffensiveAbility` | **+25** | stats | flat OA — raises monster hit + crit rate vs player DA |
| `characterOffensiveAbilityModifier` | **+5 %** | stats | |
| `characterDefensiveAbility` | **+15** | stats | flat DA — **lowers the player's hit rate** |
| `characterDefensiveAbilityModifier` | **+5 %** | stats | |
| `characterAttackSpeedModifier` | **+5 %** | tempo | |
| `characterSpellCastSpeedModifier` | **+5 %** | tempo | |
| `characterRunSpeedModifier` | **+5 %** | tempo | |
| `characterStrengthModifier` | **+5 %** | stats | physique → small physical-damage knock-on |
| `retaliationTotalDamageModifier` | **+15** | damage | reflect; negligible (§4.2) |
| **`spawnMaxAdj`** | **+1** | **density** | pack-size **maximum** +1 |
| **`spawnChampionMaxAdj`** | **+2** | **hero/champion** | champion-slot count **maximum** +2 |

**Note the asymmetry, and it is deliberate:** `spawnMinAdj` and `spawnChampionMinAdj` are **absent from
the record** (M-negative) — they exist in `gameadjustment.tpl` and Ascendant sets `spawnMinAdj = 1`, so
their absence here is a choice, not an oversight. **Veteran raises the ceilings, not the floors.** The
smallest Veteran pack is the same as the smallest Normal pack; the biggest is bigger.

**No XP field exists on this record** (M-negative) — the +10 % lives elsewhere. See §1.4.

### 1.3 Ascendant, for contrast

`records/game/balancingadjustment_ultramode_enemies01.dbr` **[GDX3]**, 18 nonzero (M):

| field | Veteran | **Ascendant** |
|---|---|---|
| `offensiveTotalDamageModifier` | +40 | **+165** |
| `offensivePhysicalModifier` | +10 | **−56** ← *negative*, a deliberate physical carve-out |
| `characterLifeModifier` | +140 | **+850** (×9.5) |
| `characterOffensiveAbility` / `…Modifier` | +25 / +5 % | **+80** / +5 % |
| `characterDefensiveAbility` / `…Modifier` | +15 / +5 % | **+80** / +5 % |
| `characterAttackSpeedModifier` | +5 | **+12** |
| `characterSpellCastSpeedModifier` | +5 | **+12** |
| `characterRunSpeedModifier` | +5 | +5 |
| `characterLifeRegenModifier` / `characterManaRegenModifier` | — | **+120** each |
| `offensiveCritDamageModifier` | — | **+40** |
| `offensiveSlowDamageMultModifier` | — | **+30** |
| `retaliationTotalDamageModifier` | +15 | +50 |
| `spawnMinAdj` / `spawnMaxAdj` | — / +1 | **+1 / +1** ← *Ascendant raises the floor too* |
| `spawnChampionMaxAdj` | +2 | **+1** ← *fewer extra champions than Veteran* |

Plus, on `gameascendant.dbr` only (M): `ultimateChallengeTroveChance 24.0`,
`ultimateChallengeTotemChance 18.0`, `ultimateChallengeSuperBossChance 0.05` →
`thedread_01/02/03.dbr` (`superBossKillsMin 100`), and four item-ascension chances (Hero 10 % / Boss
30 % / Nemesis 25 % / 100 %) with `gameChallengeDV`-keyed equations. **Ascendant is a loot-and-spectacle
mode with a difficulty tax; Veteran is a pure difficulty tax.** Different design objects — worth
knowing when we build our own.

### 1.4 The XP channel — found, and it is one multiplication

`records/game/gameengine.dbr → experienceRecord → records/game/experienceformulas.dbr` (M). The record
holds four kill-XP equations. Written out with the shared body as `E`:

```
experienceEquation           = E
challengeExperienceEquation  = E * 1.1              ← VETERAN.  Matt's +10%, literally.
eliteExperienceEquation      = E ^ 1.03 + 20
ultimateExperienceEquation   = E ^ 1.06 + 40

E = (((monsterLevel*12.75 - (averagePartyLevel^2/50))
      + ((monsterLevel-averagePartyLevel)*(averagePartyLevel/1.12))) * 0.12)
    * (1 + monsterExperience/100) + 3
```
All **M**. Evaluated over `monsterLevel ∈ {13,15,16,18,19,20}` × `averagePartyLevel ∈ {12,13}` ×
`monsterExperience ∈ {0,50,100}`, the challenge/normal ratio is **1.1000 at every single point**
(C, `v6_xp.py`) — a flat multiplier, not a curve. **Matt's remembered number is exact.**

Two design notes worth banking: (a) Elite and Ultimate use a **power law plus a flat floor**, not a
multiplier — so their XP advantage *grows* with monster level and never drops below +20/+40 per kill;
Veteran alone is a clean scalar. (b) The XP formula is `averagePartyLevel`-relative and can go
**negative** for badly over-levelled players; the `+3` (and Elite/Ultimate's `+20/+40`) is the floor
that stops that. Both are transferable shapes.

### 1.5 Density and hero spawns — where the two integers actually land

`spawnMaxAdj` and `spawnChampionMaxAdj` are declared `class=array` on `gameadjustment.tpl` (M); the
Veteran record carries them as single-element scalars, the Shattered-Realm records
(`records/endlessdungeon/difficultyscaling/balanceadjustment_0N.dbr`, GDX2/3) carry them as 85–210-entry
per-shard arrays (M) — same class, same fields, different indexing. They act on the **proxy pool**:

`records/proxies/pools/*.dbr`, `templateName = database/templates/proxypool.tpl` (M). Census over the
whole base DB: **3,067 pools carry `spawnMin`/`spawnMax`; 371 carry `championChance`** (M,
`v4_density.py`). The relevant fields:

| pool field | role | Act-1 distribution (M) |
|---|---|---|
| `spawnMin` / `spawnMax` | pack size range | median 3 / 5; `spawnMax` mode 5 |
| `championChance` | % that the pack rolls champions at all | min 3, **median 33**, mean 36.2, max 100 |
| `championMin` / `championMax` | how many champion slots when it fires | `championMax` mode **2** (137 of 254 pools) |
| `nameChampionN` / `weightChampionN` / `limitChampionN` | the champion roster, weighted draw | up to 16 entries |
| `minPlayerLevelChampionN` | **per-entry player-level gate** | the mechanism that unlocks heroes |
| `levelVarianceEquationChampionN` | per-entry level equation | `lv4_champion` / `lv5_elitechampion` / **`lv6_hero`** |

**Veteran's effect, stated exactly:** `spawnMax += 1` and `championMax += 2`. Nothing else. It does
**not** touch `championChance`, `championMin`, `spawnMin`, or any weight. It widens two ranges.

**The correction that matters (M, `v11_mix2.py`) — a champion SLOT is not a champion.** Across the 254
Act-1 pools, resolving each champion-slot entry's own `monsterClassification`:

| classification of the entry | entries | **share of draw weight** |
|---|---|---|
| `Champion` | 534 (50.9 %) | **88.9 %** |
| `Common` | 56 (5.3 %) | **7.6 %** |
| `Hero` | 459 (43.8 %) | **3.5 %** |

Heroes are **44 % of the roster by entry count and 3.5 % by weight** — Crate lists them everywhere and
weights them into near-invisibility. The Primordian's own trash (`p_beasts_slitha_t.dbr`, M) is the
clean illustration: six `hero/slith_h0N.dbr` entries at **weight 6 each** against `slitha_melee_b01` at
**200** and a plain `slitha_melee_a01` at **350** — and the plain common in a champion slot is the
single heaviest entry in the pool. Note also `p_beasts_slitha_amb_s1_n.dbr` gates its heroes at
`minPlayerLevelChampion = 22`, so **at the referent's level 13 that pool cannot produce a hero at all**
(M) — the gate, not the weight, is what governs early.

---

## 2. What the corpus says vs what the web says (tier labels, per commission)

| claim | corpus (M) | web (T) |
|---|---|---|
| increases monster stats | 12 stat/damage/tempo fields, §1.2 | "monsters are stronger and tougher" |
| increases density | `spawnMaxAdj +1` | "increased number of spawns" |
| increases hero spawns | `spawnChampionMaxAdj +2` | "noticeable increase in the spawn rate of champion and hero monsters" |
| +10 % experience | `challengeExperienceEquation = E × 1.1` | "+10 % Experience boost" |
| increased loot | **no loot field on the record** (M-negative) | "increase in the amount of loot that drops" |
| toggleable any time | `tagChallengeDifficultyDesc` (M, prior probe) | "can be toggled on/off in the main menu" |

**One correction to the community line:** the loot increase is **not a Veteran field**. There is no
loot, drop-rate, rarity or trove modifier anywhere on the record. More monsters drop more loot; that
is the whole mechanism. (Contrast Ascendant, which *does* carry explicit trove/totem/ascension
chances — §1.3.) T-source: `grimdawn.com/guide/game-settings/game-difficulties/`, accessed 2026-07-30.

---

## 3. Q2 — U-3, the composition adjudication

> Does Veteran's `+40` compose as its own multiplicative stage (**×1.40**) or pool additively with the
> `armorbase0N` skill passives (**×2.14 at cl 18**)?

### 3.1 What the corpus and the binary DO establish (M)

- **Veteran is a third class of object.** `Class = GameAdjustment` (`gameadjustment.tpl`). The
  difficulty pak is `Class = AttributePak` (`attributepak.tpl`). The Crucible/SR mutator system is
  `Mutator`, which owns *its own* `AttributePak` (`Mutator::GetAttributePak`). Three separate types.
- **`Game.dll` exports exactly three `GameAdjustment` symbols** (M): `GameEngine::GetChallengeAdjustment`,
  `ChallengeArea::GetDifficultyAdjustment`, `EndlessDungeon_Generator::GetDifficultyAdjustment` — **all
  getters, none a consumer.** There is no `GameAdjustment::Get…Attributes(CombatAttributeAccumulator&)`
  entry point. The application site is inlined and not recoverable from the symbol table.
- **By contrast the pak's entry point IS exported:**
  `AttributePak::GetOffensiveDamageAttributes(unsigned int, CombatAttributeAccumulator&, unsigned int, float)`
  — and it takes **the same accumulator type** as `Skill::AddModifierOffensiveDamageAttributes(CombatAttributeAccumulator&, float)`.
- The `ContributeMutator*` family (`Character`/`Monster`/`Pet`/`Player`/`GameEngine`) belongs to the
  **`Mutator`** system — `MutatorMode`, `FilterMutators`, `AddMutatorInbound/Outbound`,
  `ClearMutators`, and the template fields `normalMutator` / `eliteMutator` / `ultimateMutator`,
  `minMutators` / `maxMutators` / `playerMutatorPakList`. **That is Crucible and Shattered Realm, not
  Veteran.** The prior probe's citation of `ContributeMutator*` as evidence for Veteran's path is
  **superseded** — correct symbols, wrong subsystem.

### 3.2 The argument for own-stage (C, lean)

The decisive observation is not about Veteran; it is about the pak, and it is **measured**.

The envelope note adjudicated the pak against a real anchor: at charLevel 18 the multiplicative rule
`(1 − 0.71) × (1 + 0.50)` predicts Primordian's `lifeAndMana` at **15,891 vs a measured 15,822 (1.004×)**,
while the additive rule `(1 + (−71+50)/100)` predicts **28,860 (1.82×)** and fails. So: **the pak enters
through the same `CombatAttributeAccumulator` as the monster's skills, and is nevertheless a separate
multiplicative stage.** Whatever the accumulator does, it does not flatten engine-level global
adjustments into the skill bucket.

Veteran is an engine-level global adjustment of the same kind — reached from `gameengine.dbr`, applied
to every monster, indexed by nothing the creature owns. For the **pooled** reading to hold, the engine
would have to sum a `GameAdjustment`'s field into the *per-creature skill-passive* bucket specifically,
while refusing to do so for the `AttributePak` that sits one field away in the same record and enters
through a published accumulator API. **Nothing in the observed architecture supports that asymmetry.**

**Verdict: own multiplicative stage, ×1.40 — grade C, lean, NOT closed.** I decline to grade it M
because the consuming code is inlined and I have no measured Veteran-state anchor. **Both readings are
carried through §4 exactly as commissioned.**

### 3.3 What would close it

| route | cost | note |
|---|---|---|
| **One Veteran-on save with a `greatestMonsterKilledLifeAndMana` for a named monster** | ~5 min of Matt's time, on top of the T11 pull already queued | Life and damage share the operator; a life anchor settles both. `+140` vs the pak's `+50` and the skill pool's `−71` are far enough apart that the two readings differ by **1.62×** on HP — un-missable. **This is the same pull T11 already asks for; it just needs the monster killed and the level noted.** |
| Disassembly of `GameEngine::GetChallengeAdjustment`'s call sites | high | out of scope for a read-only probe |
| Community-reported Veteran monster HP | tertiary, noisy | I decline to import it as a measurement |

---

## 4. Q3 — THE FOUR-CELL PRIMORDIAN PAYLOAD GRID

### 4.1 The operator, and its validation

```
delivered = raw × MIT[component] × (1 + component_mod/100) × TOTAL_FACTOR
TOTAL_FACTOR = (1 + Σ pool offensiveTotalDamageModifier /100)
             × (1 + pak[Normal,1p] /100)
             × (1 + Veteran /100)            ← own-stage reading only; pooled folds into Σ pool
```
Player mitigation from the **measured** equipped set (`d7`/`d8`): armor 337 ⇒ **70 % physical absorb**,
cold resist 14 ⇒ **×0.86**. Component mods: pool physical `+6` (`damage_totaladjuster` r2), icearmor
cold `+28 %` (r5) / `+26 %` (r4), pak `offensiveSlowColdModifier −38` on the DoTs.

**HEADER CHECK — this operator reproduces every ratified pin to the hundredth** (C, `v9_grid.py`):

| pin | computed here | charter |
|---|---|---|
| A-WAVE-1 (S0 / S1 / S2) | **345.32 / 258.99 / 91.37** | 345.32 / 258.99 / 91.37 ✓ |
| A-BLIZ-1 (S0 / S1 / S2) | **173.61 / 130.21 / 45.93** | 173.61 / 130.21 / 45.93 ✓ |
| A-NOVA-2 far band, S1_PAK | **269.66** | 269.66 ✓ |

Nothing below rests on a re-derivation the charter has not already ratified.

### 4.2 Composite factors

| cell | Σ pool | pak | Veteran stage | **TOTAL_FACTOR** | phys mult |
|---|---|---|---|---|---|
| cl 13 / r4, no Vet | −70 | −25 | — | 0.2250 | 1.060 |
| **cl 13 / r4, Vet own** | −70 | −25 | +40 | **0.3150** | 1.166 |
| **cl 13 / r4, Vet pooled** | **−30** | −25 | — | **0.5250** | 1.160 |
| cl 16 / r5, Vet own *(third reading, §6.1)* | −67 | −25 | +40 | 0.3465 | 1.166 |
| cl 16 / r5, Vet pooled | −27 | −25 | — | 0.5475 | 1.160 |
| cl 18 / r5, **no Vet** *(charter's S2 column)* | −65 | −25 | — | 0.2625 | 1.060 |
| **cl 18 / r5, Vet own** | −65 | −25 | +40 | **0.3675** | 1.166 |
| **cl 18 / r5, Vet pooled** | **−25** | −25 | — | **0.5625** | 1.160 |

Raw payload deltas driving the rank fork (M, `v9_grid.py`): frigidring **118/200 → 148/247**, wave
**122/210 → 153/272**, blizzard **58/111 → 76/137**, icearmor cold rider **+26 % → +28 %**, passive cold
**16–38 → 20–46**, melee `damagebase_physical04` at cl 13 **101–128** vs cl 18 **136–175**.

### 4.3 THE GRID — post-mitigation, icearmor UP

Delivered damage against the measured player gear. `cl18/r5 NO-VET` is the charter's current S2_FULL
column, carried as the reference.

| channel | **cl13/r4 own** | **cl13/r4 pooled** | *cl16/r5 own* | *cl16/r5 pooled* | **cl18/r5 own** | **cl18/r5 pooled** | cl18/r5 NO-VET |
|---|---|---|---|---|---|---|---|
| nova prong, close band ×2 (50 % ea) | 81.27 | 135.34 | 112.15 | 177.06 | 118.95 | 181.91 | 83.73 |
| nova prong, mid band (100 %) | 81.27 | 135.34 | 112.15 | 177.06 | 118.95 | 181.91 | 83.73 |
| **nova prong, FAR band (140 %)** | **113.78** | **189.47** | 157.01 | 247.89 | **166.53** | **254.68** | 117.22 |
| nova cold DoT / 2 s | 12.70 | 21.16 | 18.21 | 28.77 | 19.31 | 29.56 | 13.79 |
| **wave impact** | **85.12** | **141.76** | 122.29 | 193.08 | **129.70** | **198.37** | 91.37 |
| wave cold DoT / 3 s | 14.81 | 24.69 | 21.52 | 34.00 | 22.82 | 34.94 | 16.30 |
| **blizzard per drop** | **44.28** | **73.74** | 61.47 | 97.05 | **65.19** | **99.71** | 45.93 |
| melee swing MIN | 16.59 | 27.55 | 22.54 | 35.49 | 25.57 | 39.01 | 17.13 |
| melee swing MAX | 27.07 | 45.00 | 36.33 | 57.26 | 41.11 | 62.74 | 27.90 |
| **WORST SINGLE HIT** | **113.78** | **189.47** | 157.01 | 247.89 | **166.53** | **254.68** | 117.22 |
| **÷ player pool 759** | **15.0 %** | **25.0 %** | 20.7 % | 32.7 % | **21.9 %** | **33.6 %** | 15.4 % |
| ÷ measured worst 260.498 | 0.437 | 0.727 | 0.603 | 0.952 | 0.639 | **0.978** | 0.450 |

**Icearmor DOWN** (the other 62.5 % of the fight) scales the whole table by ≈0.82 on cold-heavy
channels: worst hit **94.05 / 156.60 / 128.16 / 202.30 / 135.93 / 207.84 / 95.36**, i.e. **12.4 % /
20.6 % / 16.9 % / 26.7 % / 17.9 % / 27.4 % / 12.6 %** of the 759 pool.

**Pre-mitigation** (the units the charter's melee band uses) — melee swing band, icearmor down:

| cell | melee band (pre-mit) |
|---|---|
| **cl13/r4 Vet-own** | **42.14 – 58.98** ← charter band is 43.1–60.8 |
| cl13/r4 Vet-pooled | 69.91 – 97.90 |
| cl16/r5 Vet-own | 56.62 – 78.56 |
| cl16/r5 Vet-pooled | 89.07 – 123.63 |
| cl18/r5 Vet-own | 65.63 – 91.89 |
| cl18/r5 Vet-pooled | 99.99 – 140.06 |
| cl18/r5 NO-VET *(the charter's basis)* | 43.09 – 60.77 |

### 4.4 THE DEGENERACY — the finding that reorders the run's unknowns

Ratio of each cell to the charter's existing S2_FULL cl-18/r5 no-Veteran column, **per channel** (C,
`v13_degeneracy.py`):

| cell | mean ratio | spread across 8 channels | max dispersion |
|---|---|---|---|
| **cl 13 / r4 + Veteran own-stage** | **0.951** | 0.909 – 0.971 | **4.4 %** |
| cl 16 / r5 + Veteran own-stage | 1.327 | 1.302 – 1.339 | 1.8 % |
| cl 18 / r5 + Veteran own-stage | 1.431 | 1.400 – 1.493 | 4.3 % |
| cl 13 / r4 + Veteran pooled | 1.582 | 1.514 – 1.616 | 4.3 % |
| cl 16 / r5 + Veteran pooled | 2.094 | 2.052 – 2.115 | 2.0 % |
| cl 18 / r5 + Veteran pooled | 2.187 | 2.143 – 2.277 | 4.1 % |

**"charLevel 13 / rank 4 / Veteran-own-stage" and "charLevel 18 / rank 5 / no Veteran" are the same
fixture to within 5 %, uniformly, on nova, wave, blizzard, melee and both DoTs.** The difficulty
probe's 0.4 % HP coincidence was not a coincidence of one anchor — the rank-4-vs-rank-5 payload step
(≈0.79×) and the `armorbase05` level step (0.225 vs 0.2625, ≈0.86×) together very nearly cancel
Veteran's ×1.40. Crate did not design this; it falls out of two independent ramps.

**Conduct consequence, and it inverts R-WR3-29(5)'s sequencing:**
- If **U-3 = own-stage**, then closing **U-4 is worth ≤5 %** on the payload set. The cascade the charter
  feared — "skill rank re-derives 5 → 4 and the payload pin set re-bases" — **does not move the
  fixture**. Stage-2c can proceed on the existing pins with a ≤5 % caveat.
- If **U-3 = pooled**, every cell is **1.58–2.19×** the current column and the pins must re-base.
- **Therefore U-3 is the gate, and U-4 is not.** Both close on the *same* ~5-minute Veteran-save pull
  (§3.3), which is now the single highest-leverage item in the run.

### 4.5 Which cell best matches the referent's measured play

Honestly: **the measured datum does not discriminate, and it should not be asked to.**

- `greatestDamageReceived = 260.498` is **unattributed and lifetime-of-character** (R-WR3-26(2)), and
  R-WR3-26(3) established that re-attribution just relocates it into another damped bucket. It is a
  **lower bound** on the worst hit taken, not a Primordian measurement.
- Primordian's own kit reaches **97.8 %** of it in `cl18/r5 pooled` (254.68) and only **64 %** in
  `cl18/r5 own` (166.53). But the whole-roster S2+Veteran ceiling was **354.1 (own) / 541.9 (pooled)**
  (prior probe §5.3) — **both clear 260.498**, so the datum excludes neither.

What *does* discriminate is the charter's own design target. **CAL-1's ratified lean** is "scripted-heavy
norm ~10–15 % per projectile, with the 2× quantum reaching ≈ the 34.3 % measured worst," and §3's
outlier row is "nova up to 55 %, **1.6–3.4× OVER**." Against that:

| cell | worst hit ÷ 759 | vs CAL-1's 10–15 % norm | vs the 34.3 % measured-worst ceiling |
|---|---|---|---|
| **cl13/r4 own** | **15.0 %** | **lands ON it** | 44 % of ceiling — full headroom |
| cl13/r4 pooled | 25.0 % | 1.7× over | 73 % |
| cl16/r5 own | 20.7 % | 1.4× over | 60 % |
| cl16/r5 pooled | 32.7 % | 2.2× over | 95 % — no headroom |
| **cl18/r5 own** | **21.9 %** | 1.5× over | 64 % |
| **cl18/r5 pooled** | **33.6 %** | 2.2× over | **98 % — at the ceiling** |
| cl18/r5 NO-VET | 15.4 % | lands on it | 45 % |

**Flag, stated as a lean the conductor may veto:** the **own-stage cells** are the ones consistent with
the referent's *play*, not just its arithmetic. The referent player cleared this fight at level 13
(2 deaths in 7,096 s, `play_stats`, M) with a 759/1600 pool. A boss whose single far-band nova prong
takes **33.6 % of the human-form pool** — and whose freeze rider is 1.3–1.8 s, longer than its own
1.369 s melee lock — makes a three-prong sequence lethal from full. The pooled cells price a fight
that the save says was won comfortably twice over. **`cl13/r4 own` and `cl18/r5 own` both land in
CAL-1 territory; the pooled cells do not.** This is *soft* evidence for U-3 = own-stage, independent of
§3.2's structural argument, and I report it as such.

### 4.6 What the cells do to the pins

Post-mitigation, icearmor rider ON (the units A-WAVE-1 / A-BLIZ-1 were ratified in):

| pin | **S1_PAK (regime of record)** | cl13/r4 own | cl13/r4 pooled | cl18/r5 own | cl18/r5 pooled |
|---|---|---|---|---|---|
| A-NOVA-2 far band | 332.11 *(269.66 without the rider)* | 113.78 (0.34×) | 189.47 (0.57×) | 166.53 (0.50×) | 254.68 (0.77×) |
| A-NOVA-2 mid band | 237.22 | 81.27 (0.34×) | 135.34 (0.57×) | 118.95 (0.50×) | 181.91 (0.77×) |
| A-WAVE-1 impact | 258.99 | 85.12 (0.33×) | 141.76 (0.55×) | 129.70 (0.50×) | 198.37 (0.77×) |
| A-BLIZ-1 per drop | 130.21 | 44.28 (0.34×) | 73.74 (0.57×) | 65.19 (0.50×) | 99.71 (0.77×) |
| melee band (pre-mit) | — *(43.1–60.8 is an S2 figure)* | 42.1–59.0 | 69.9–97.9 | 65.6–91.9 | 100.0–140.1 |

**A Fork-1 re-ruling to S2_FULL + Veteran halves the pins under own-stage (×0.50) and cuts them by
about a quarter under pooled (×0.77), relative to the S1_PAK values now in force.** In no cell does
S2+Veteran reproduce S1_PAK. The two regimes are 30–200 % apart everywhere; they are not
interchangeable and the arm ruling is genuinely load-bearing.

**⚑ A unit inconsistency the charter should absorb.** A-NOVA-2 / A-WAVE-1 / A-BLIZ-1 are
**post-mitigation**; the melee band **43.1–60.8 is pre-mitigation** (its post-mitigation equivalent at
cl 18 no-Veteran is **17.13–27.90**). Both are correct in their own units, and I reproduced each in the
units it was ratified in — but the melee-graduation sweep `BOSS_DMG_SWEEP → (43.1, 52.0, 60.8)`
(R-WR3-25(9)) is deferred to stage-2c and will be compared against pins that do not share its units.
**Route to jack-ryan with the melee graduation.**

### 4.7 Veteran terms the grid does NOT price

| term | value | consequence, unpriced |
|---|---|---|
| `characterLifeModifier +140` | HP **×2.40** | §3's boss:player HP row (22.8×) and duration band (59–118 s). **Do not apply this on top of the measured 15,822** — that figure already carries whatever mutator state was live at the kill. It applies only if the fixture builds the boss from base stats. |
| `characterAttackSpeed/SpellCastSpeed/RunSpeed +5 %` each | tempo | §3's player:boss speed row (player 1.29–1.33× faster) → **1.23–1.27×**, moving the "IN BAND, 7–11 % over" verdict *toward* the fixture's 1.43×. Also compresses the 1.369 s melee lock, on top of icearmor's +35 %. |
| `characterOffensiveAbility +25`, `+5 %` | hit + crit rate vs player DA | raises *realised* boss DPS above the damage table. Not computable: **monster base OA by level is engine-internal, not in the `.arz`** (§6.3). |
| `characterDefensiveAbility +15`, `+5 %` | player hit rate vs boss DA | **lowers player DPS** — pushes §3's already-BELOW-BAND player-DPS row (250 vs 310–620 HP/s) further from the referent. |
| `characterStrengthModifier +5 %` | physique → physical damage | small; unpriced for the same base-attribute reason. |
| `retaliationTotalDamageModifier +15` | icearmor's reflect rider | **negligible**: the pak's slot-0 `retaliationTotalDamageModifier` is **−66**, so the composed value is ≈3.4–7.4 over 2 s. Report, do not model. |

---

## 5. Q4 — encounter-mix implications for R-WR3-2

### 5.1 The measured mix was in the save all along

`player.gdc` `play_stats` (M, `parsed.json`, re-read this cycle):

```
kills 882 · championKills 7 · heroKills 3 · deaths 2 · playTime 7,096 s
hitsReceived 500 · hitsInflicted 1,606 · criticalHitsInflicted 66 · criticalHitsReceived 0
```

| population | count | share of 882 kills |
|---|---|---|
| champions | **7** | **0.794 %** |
| heroes | **3** | **0.340 %** |
| **elite (combined)** | **10** | **1.134 %** |
| common | 872 | 98.866 % |

**This is the R-WR3-2 "majority of encounters" mix, measured, for the referent character.** The parser
has read these two fields since G-7; no artifact had used them. `Game.dll` confirms
`numberOfChampionKills` as an engine-truth save field (M).

### 5.2 Veteran's uplift, modelled

Model (**D** — the engine's consumption of `championChance` is not in the DBR): pack size
`~ U[spawnMin, spawnMax]`; with probability `championChance` the pack rolls `~ U[championMin,
championMax]` champion slots; each slot draws from the weighted roster filtered by
`minPlayerLevelChampionN ≤ 13`; classification resolved per entry. Veteran applies `spawnMax += 1`,
`championMax += 2`. Over the **224 Act-1 pools** carrying champion machinery (C, `v11_mix2.py`):

| quantity | Normal | **Veteran** | uplift |
|---|---|---|---|
| E[pack size] (common slots) | 4.884 | 5.384 | **1.102× (+10.2 %)** |
| E[champion slots per pack] | 0.499 | 0.863 | **1.730× (+73.0 %)** |
| E[Champion-classified per pack] | 0.452 | 0.780 | 1.727× (+72.7 %) |
| E[Hero-classified per pack] | 0.0144 | 0.0246 | 1.713× (+71.3 %) |
| **P(≥1 hero in the pack)** | **1.34 %** | **2.09 %** | **1.563× (+56.3 %)** |
| **bodies per pack** | **5.38** | **6.25** | **1.161× (+16.1 %)** |
| elite share of bodies | 8.66 % | 12.88 % | +4.2 pp |

For the referent's own trash specifically — the eleven Act-1 slith pools (C, `v10_mix.py`):
E[champions/pack] **0.406 → 0.662 (1.63×)**, P(hero) **2.70 % → 3.63 % (1.34×)**. Per-pool
`P(hero/pack)` under Veteran ranges **0 %** (`p_beasts_slitha_amb_s1_n`, heroes gated at
`minPlayerLevel 22`) to **9.03 %** (`_xhighhero` pools, whose hero weights are 60 not 6).

### 5.3 The honest reconciliation — and it is a caveat, not a match

| | champion | hero | elite |
|---|---|---|---|
| **measured (save, M)** | **0.794 %** | **0.340 %** | **1.134 %** |
| modelled Normal (D) | 8.394 % | 0.267 % | 8.661 % |
| modelled Veteran (D) | 12.490 % | 0.395 % | 12.885 % |

**The hero rate matches — the measured 0.340 % falls between the modelled Normal 0.267 % and Veteran
0.395 %, which is exactly where a run that spent part of its life below the `minPlayerLevel` gates
should land.** That is a real, if soft, corroboration of both the model and the Veteran read.

**The champion rate does not match — the model over-predicts by ~10×.** I am not going to launder that.
Three candidate causes, none resolvable from the DBR: (a) my per-pack `championChance` reading may be
wrong (it could be per-area-instance or per-slot); (b) most of the 882 kills accrued below level 13
with the `minPlayerLevelChampion` gates shut, while the model opens all of them; (c) many of the 882
are set-piece / ambush / quest spawns (`SetPiece`, `SetPiecePool`, `ProxyAmbush` — 377 records in
Act 1) that carry no champion machinery at all. **New unknown: U-V1.**

**Therefore, prescriptions for the encounter-mix fixture:**

1. **Pin the absolute rates to the save, not to my model.** Champion 0.794 %, hero 0.340 %, elite
   1.134 % of kills — those are M, and they are already Veteran-inclusive.
2. **Use the uplift ratios only for counterfactuals** — e.g. "what would this mix have been on plain
   Normal": divide by ≈1.56–1.73× on the elite channels, ≈1.16× on bodies-per-encounter. That gives a
   Normal-equivalent elite rate of ≈0.65–0.73 %.
3. **Price the pack-size effect, because it is the biggest one the fixture is currently blind to.**
   Veteran adds **+16 % bodies per pack** and, structurally, **widens the pack-size distribution
   upward without moving its floor** (`spawnMinAdj` absent). A fixture that models mean pack size
   correctly but not its *right tail* will systematically under-price the worst encounters — which are
   precisely the ones an R-WR3-2 majority-win-rate measurement turns on. **The distribution shape, not
   just its mean, is the transferable fact.**
4. **882 kills / 7,096 s = 0.124 kills/s over the whole run**, at 5.38–6.25 bodies per pack ⇒ roughly
   **141–164 pack-equivalents**. That is the denominator a "majority of encounters" acceptance
   measurement should be sized against.

---

## 6. Corrections owed to already-banked artifacts

### 6.1 U-4 — advanced, one branch dead, a third branch surfaced

**`greatestMonsterKilledLevel` is engine-truth (M).** It appears as a literal string in `Game.dll`
(`greatestMonsterKilledLevel[i]`, indexed per difficulty) beside `greatestMonsterKilledName[i]` and
`greatestMonsterKilledLifeAndMana[i]`, with the accessor pair
`PlayStats::GetGreatestMonsterKilledLevel()` / `SetGreatestMonsterKilledLevel(unsigned int)`. The
triple is co-named; Name and LifeAndMana are unambiguously monster-side. **The "player level at kill"
reading listed in R-WR3-29(5) is dead (C, high confidence).**

What the field name does *not* settle is **which** monster level:

| reading | implies | boss `charLevel` | skill rank |
|---|---|---|---|
| **(a) post-remap `charLevel` = 13** | `lv6_hero` spawn 10 ⇒ **averagePlayerLevel 7–8 at the kill** | **13** | **4** |
| **(b) proxy spawn level = 13** | ⇒ averagePlayerLevel **10–11** at the kill | **16** | **5** |
| (c) the run's current derivation | aPL 13 ⇒ spawn 15–16 | 18–19 | 5 |

Reading (b) is newly surfaced by this probe and is **more plausible on world-level grounds** — the
Wightmire is Act-1 content a level-10–11 character plausibly clears, whereas reading (a) requires the
player to have been at level 7–8. It also **reconciles the save with `gd_nova`'s charLevel-16
derivation** (R-WR3-27(5) instance 4), which the payloads note superseded. I priced cl 16 / rank 5 in
§4 so the conductor has all three.

**Bank alongside it (M):** the save's `play_stats.maxLevel = 12` while `character_bio.level = 13`.
Downstream fields decode cleanly (strings, floats, championKills all sane), so this is not a parse
drift — it is a lagging high-water mark. **Any argument that leans on a `play_stats` counter being
current at save time is on notice.**

### 6.2 R-WR3-26(6) U-1's premise is FALSIFIED

R-WR3-26(6) recorded: *"the two field labels are community convention, not engine truth (`Game.dll`
has no such symbols)."* **`Game.dll` carries `greatestDamageReceived` and `greatestDamageInflicted` as
literal strings** (M), in the same contiguous `PlayStats` field-name block as `numberOfKills`,
`numberOfChampionKills`, `maxLevel`, `playTimeInMinutes`. The labels are **engine-truth**. This does
**not** revive the swap hypothesis — `lastHit` / `lastHitBy` remain unattested (the only near symbol is
`Character::GetLastHitFrame`, unrelated) — but the stated *basis* for U-1 was wrong and the ledger
should say so. **Route to jack-ryan.**

### 6.3 The prior probe's `ContributeMutator*` citation is superseded

The difficulty probe (§1.3) cited `Mutator::GetAttributePak`,
`GameEngine::ContributeMutatorOffensiveDamageAttributes`, `FilterMutators(…, MutatorMode, …)` as
"the separate application path" for Veteran. Those symbols are real, but they belong to the
**Crucible / Shattered Realm mutator system** (`minMutators`, `maxMutators`, `playerMutatorPakList`,
`normalMutator` / `eliteMutator` / `ultimateMutator`, `ChallengeArea::GenerateMutators`). Veteran is a
`GameAdjustment` reached from `gameengine.dbr → challengeAdjustment`. **My own prior artifact,
corrected here.** The own-stage lean survives, on the different and better argument in §3.2.

---

## 7. Unknowns

| id | unknown | status | what would settle it |
|---|---|---|---|
| **U-3** | Veteran own-stage ×1.40 vs pooled ×2.14 | **OPEN — and now the run's single highest-leverage item.** Lean own-stage (C, §3.2), reinforced by the play-consistency read (§4.5) | One Veteran-on save with `greatestMonsterKilledLifeAndMana` for a named monster + its level. **Rides T11.** The two readings differ **1.62×** on HP. |
| **U-4** | Boss `charLevel` 13 / 16 / 18 | **ADVANCED** — "player level" branch dead (§6.1); three monster-side readings priced (§4) | Same T11 pull: a save whose monster level and player level demonstrably differ closes spawn-vs-final. **But §4.4 shows this is worth ≤5 % if U-3 = own-stage.** |
| **U-V1** | `championChance` semantics: per pack, per spawn slot, or per area instance? | **NEW.** Model over-predicts champions 10× vs the save; hero rate matches | In-game observation, or a save with a much larger kill count to fit against. **Consequence: use uplift ratios, pin absolutes to the save (§5.3).** |
| **U-V2** | Do `spawnMaxAdj` / `spawnChampionMaxAdj` add to the pool's value, or clamp it? | Lean: **add** (Ascendant sets `spawnMinAdj` and `spawnMaxAdj` to 1 *together*, which reads as a shift, not a clamp) | `Game.dll` has no exported consumer |
| **U-V3** | Are Veteran and Ascendant mutually exclusive, or does Ascendant stack over Veteran on Ultimate? | `tagDifficultyUltimateVeteran :: "Ascendant Mode"` and the `0x80` bit suggest Ascendant **is** Veteran-on-Ultimate (one flag, two labels) | Not needed for this run |
| **U-V4** | **Monster base life / OA / DA by level is NOT in the `.arz`** — every Monster record reads `characterLife 0.0`, and no ≥50-element `characterLife` array exists outside the six player-class training records (M-negative, `v8_baselife.py`) | **This is why the HP-anchor route to U-4 cannot be closed from corpus**, and why §4.7's OA/DA/strength terms are unpriceable. The envelope's per-monster HP figures are back-solved, not forward-computed | Engine-internal; a measured Veteran HP anchor sidesteps it entirely |

**What I did not do, deliberately:** I did not import a community Veteran HP or damage number and
present it as a measurement; §4 is parameterised over both composition readings instead. I did not
re-derive the envelope's HP figures once §6.3/U-V4 showed the base curve is not in the corpus.

---

## 8. Source list

**Primary — corpus (M).** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` —
`database/database.arz`, `gdx1/…/GDX1.arz`, `gdx2/…/GDX2.arz`, `gdx3/…/GDX3.arz`. Records cited:
`records/game/gameengine.dbr` · `records/game/gameascendant.dbr` [GDX3] ·
`records/game/balancingadjustment_challengemode_enemies01.dbr` ·
`records/game/balancingadjustment_ultramode_enemies01.dbr` [GDX3] ·
`records/game/balancingadjustment_mp+difficulty_{enemies,players,pets}01.dbr` ·
`records/game/experienceformulas.dbr` ·
`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/skills/nonplayerskills/bossskills/{primordian_frigidring,primordian_wave,primordian_icearmor,primordian_passive}.dbr` ·
`records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr` ·
`records/skills/nonplayerskills/passive/{armorbase05,damage_totaladjuster,damagebase_physical04,resists_heroboss}.dbr` ·
`records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr` ·
`records/proxies/pools/p_beasts_slith*.dbr` (11 pools) · 254 further `records/proxies/pools/*.dbr`
reached from 377 `records/proxies/area001/*` `Proxy` records ·
`records/endlessdungeon/difficultyscaling/*balanceadjustment*.dbr` [GDX2/GDX3].

**Primary — templates (M).** `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` —
`gameadjustment.tpl`, `gameascendant.tpl`, `gameengine.tpl`, `proxypool.tpl`, `proxypoolequation.tpl`,
`attributepak.tpl`.

**Primary — binary (M).** `/Users/admin/Games/vendor/grim-dawn/Game.dll`, 65,229 extracted strings.
Cited: `GameEngine::GetChallengeAdjustment` · `ChallengeArea::GetDifficultyAdjustment` ·
`EndlessDungeon_Generator::GetDifficultyAdjustment` · `AttributePak::GetOffensiveDamageAttributes` ·
`Skill::AddModifierOffensiveDamageAttributes` · `Mutator::GetAttributePak` · the `ContributeMutator*`
family · `PlayStats::{Get,Set}GreatestMonsterKilledLevel/LifeAndMana/Name` · the `PlayStats` field-name
block (`greatestDamageReceived`, `numberOfChampionKills`, …).

**Primary — saves (M).** Referent `player.gdc` via
`legolas/scratch/2026-07-28-gdc-parse-g7/{gdc_parse.py,parsed.json}`; third-party `noquesthc.gdc`,
`Hellwrathh.gdc`, `playersoldier.gdc` (read-only fetches, `github.com/ChrisElison/GDParser`).

**Tertiary (T).** `grimdawn.com/guide/game-settings/game-difficulties/`; Grim Dawn Fandom wiki,
Difficulty page. Accessed 2026-07-30. Used **only** for §2's tier table; every number in this note is
corpus-sourced.

**Prior artifacts relied on.** `research/2026-07-30-wr3-damper-difficulty-probe.md` (§1.3 Veteran
first-sighting, §5 the byte-128 read — §6.3 corrects its `ContributeMutator*` citation) ·
`research/2026-07-30-gd-l13-reference-envelope.md` §2 (the measured multiplicative adjudication that
§3.2's argument rests on) · `research/2026-07-30-wr3-wave-blizzard-payloads.md` (rank-5 payloads,
composition operator) · `research/2026-07-30-wr3-nova-star-geometry.md` §6 (distance bands, per-prong
payload) · `research/2026-07-30-wr3-damage-discriminator.md` (`d7`/`d8` mitigation model, ceilings).

**Scratch (this probe, read-only).**
`legolas/scratch/2026-07-30-wr3-veteran/` — `v1_dump.py` (balancingadjustment census) ·
`v2_wiring.py` (inbound refs + experience/spawn field sweep, all four archives) · `v3_pools.py`
(proxy-pool anatomy) · `v4_density.py` (371-pool champion census) · `v5_tpl.py` (template variable
declarations) · `v6_xp.py` (XP equations + evaluation) · `v7_hp.py` (HP chain) · `v8_baselife.py`
(U-V4: base life is not in the corpus) · `v9_grid.py` (grid + pin header check) · `v10_mix.py` /
`v11_mix2.py` (encounter mix, uncorrected then classification-corrected) · `v12_grid2.py` (pre/post
mitigation, cl-16 cell, pin re-basing) · `v13_degeneracy.py` (§4.4).
Nothing outside this deliverable and that scratch directory was modified.
