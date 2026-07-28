# KIT-CAL-1 — HP-table re-grade against G-8's measured monster life

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Run:** KC1-2026-07-27 (conductor: gandalf)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` (§14.10 damage hold honoured; §14.11 HP hold **discharged**; §14.15 charLevel ambiguity **closed**)
**Class:** evidentiary — measured extraction from primary source, adjudicated against measured client pixels
**Mode:** read-only. No writes outside `legolas/notes/` + `legolas/scratch/2026-07-28-kitcal1-g5a/`.

**Ground truth consumed:** `agentic_orchestration/galadriel/notes/2026-07-28-kitcal1-g8-death2-primordian-stats.md`
(ten in-world monster-HP readouts across seven frames, M-EYE at 8×).

**Predecessors amended:**
`legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` (the ledger being re-graded) ·
`legolas/notes/2026-07-28-kitcal1-primordian-proto.md` (§0.3 contamination warning **retired by measurement**; §7.3 charLevel question **closed**)

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`, or pixel read by G-8) · **D** = DERIVED (arithmetic shown, operator named) · **U** = UNRESOLVED / HELD.

---

## 0. Headline

**The provisional correction factors ×0.837 (trash) and ×0.810 (boss) are both withdrawn, and they are
withdrawn for opposite reasons.**

1. **The trash and champion tiers needed no correction at all.** Frame 287 carries four numeric
   readouts, and **all four are reproduced exactly, at one consistent charLevel, by the unmodified
   G-5a chain** — including one whose creature identity *and* level are independently fixed by the
   nameplate on the same frame. `×0.837` is **FALSIFIED**. §1.1.
2. **The boss/quest tier needs a correction, and it is not a ratio — it is a constant.** Primordian's
   14,812 is reproduced by the G-5a chain with the monster pak's `characterLifeModifier` entering
   the additive pool at **+35 instead of +50**, i.e. a flat **−15.000 pp** stage. Expressed as a
   ratio that is ×0.8101 at −71 and would be ×0.8370 at −58 — **which is exactly the provisional
   pair.** Gandalf's two factors were one rule wearing two hats; the rule is now stated once and
   generalises. §1.2.
3. **Equipped-gear life is not applied to the monster's own life pool.** The residual at charLevel 13
   is **exactly zero**, and Primordian's necklace carries an unconditional flat `characterLife 220`.
   The §0.3 "contaminated instrument" warning in my Primordian proto is **retired**: Primordian is a
   clean instrument, and it always was. §1.4.
4. **The nameplate number is the creature's `charLevel`, proven twice on two different remappers.**
   §14.15 collapses to **charLevel 13**; the cl-17-multiplicative and cl-11-plus-gear candidates are
   both dead. §1.5.
5. **The one hero-tier measurement disagrees with the model by 2.49× in the WRONG direction.**
   Thundersnout's 4,702 is **not reachable** by any record, at any charLevel, under any composition
   operator, anywhere in the four-archive corpus. **Do not propagate a downward correction to the
   hero rows** — the only hero evidence available points *up*, not down. §3.3, §4.

---

## 1. The composition rule, measured

### 1.1 — Frame 287 closes the trash and champion tiers, four-for-four

G-8 §6.2 lists four numerals on frame `287` (`play_time` 5790), plus a nameplate reading
**"Deepmire Vanguard", level 11**. All four maxima resolve at **charLevel 11** under the
**unmodified** G-5a chain

```
hp = (bioLife + Σ skillPassive characterLife) × (1 + (Σ skillPassive characterLifeModifier + pakLifeModifier)/100)
     with pakLifeModifier = +50   (Normal / 1 player, index 0)
```

| measured max | record | display name | class | `charLevel` eq | cl | computed | floor | Δ |
|---|---|---|---|---|---|---|---|---|
| **813** | `trollhalfswamp_b02.dbr` | Eastmire Warrior | Champion | `(charLevel*1)+2` | 11 | **813.2768** | **813** | 0 |
| **649** | `slitha_melee_b01.dbr` | **Deepmire Vanguard** | Champion | `charLevel*1+1` | 11 | **649.7467** | **649** | 0 |
| **326** | `trollhalfswamp_a02.dbr` | Eastmire Herder | Common | `(charLevel*1)+2` | 11 | **326.3945** | **326** | 0 |
| **326** | `trollhalfswamp_a02.dbr` | Eastmire Herder (2nd) | Common | `(charLevel*1)+2` | 11 | **326.3945** | **326** | 0 |

**Why this is a closure and not four coincidences.** Three separate constraints land together:

- The **nameplate on that very frame reads "Deepmire Vanguard", level 11** — and `slitha_melee_b01`
  *is* Deepmire Vanguard, and at `charLevel` 11 it computes to 649.75. The creature identity and the
  level are measured, not fitted. Only the HP is predicted, and it lands to the digit.
- The two 326s are **the same record twice** — exactly what two members of one trash type in one pack
  look like. A coincidence account has to explain a repeated value.
- `trollhalfswamp_a02` and `_b02` are **the same family at the same charLevel**, and the family is
  the Eastmire/Deepmire swamp roster the run was standing in. Two independent tiers of one family
  landing on one level is not a free parameter.
- **The two champions straddle both armour tables.** Deepmire Vanguard runs `armorbase02`
  (life-mod **−58**); Eastmire Warrior runs `armorbase03` (life-mod **−71**). **Both validate at
  +50.** So whatever the boss tier needs, it is not a property of the `−71` table. §1.3.

**M** for every measured column, **D** for the computed column (arithmetic above, no free parameters).

Corroborating fifth: **frame 87's `(58/58)`** — `zombie_a01` (Walking Dead) at charLevel 4 computes
to **58.8309 → 58** under the same unmodified chain, at a `play_time` (1560) whose nameplate is a
level-4 hero, i.e. exactly the player level that puts trash at charLevel 4. Graded **D-strong**, not
closure — 58 is a dense collision band (55 corpus hits) and it is not level-pinned by a nameplate.

**⇒ RULING: the G-5a trash and champion HP rows stand verbatim. `×0.837` is withdrawn as falsified,
not superseded.**

### 1.2 — Frame 281 fixes the boss/quest tier at −15.000 pp

Primordian, `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr`, `monsterClassification = Quest`,
`charLevel = charLevel*1+3`, bio `bio_boss_standard_01.dbr`, sole life-modifier source `armorbase05` at rank 13 = **−71** (M).

```
bio characterLife @ cl 13 = ((13*51)^1.53) + 2400            = 23,145.10792
G-5a chain (pak +50):  23,145.108 × (1 + (−71+50)/100) = ×0.79 = 18,284.64   ✗  (+23.4 % vs screen)
MEASURED (G-8, 6× M-EYE):                                            14,812   ✓
required net factor ∈ [0.6399625, 0.6400057]                   ⇒  0.640000
0.640000 = 1 + (−71 + 35)/100
```

**The pak's `characterLifeModifier` enters the additive pool at +35, not the +50 read at index 0 —
i.e. a flat −15.000 pp sits between the pool and the product.** Restated as a per-tier ratio it is
0.64/0.79 = **×0.81013** at −71 and 0.77/0.92 = **×0.83696** at −58. **Those are gandalf's
provisional ×0.810 and ×0.837 to three decimals.** The provisional pair was already this rule; what
it lacked was a single statement of it. It now has one:

> **HP composition, GD Act 1, Normal, 1 player (ratified):**
> `hp = (bioLife + Σ flat) × (1 + (Σ skillPassive characterLifeModifier + P)/100)`
> where **P = +50** for `monsterClassification ∈ {Common, Champion}` (M-closed, §1.1)
> and **P = +35** for `monsterClassification ∈ {Quest, Boss}` (M-closed at one point, §1.2)
> and **P = +50 for `Hero`** under both surviving gate hypotheses — but see §3.3, the hero tier is
> **contested by measurement in the opposite direction** and must not be treated as settled.

`characterLifeMultModifier` is 0 at Normal/1P and does not enter. **M.**

### 1.3 — Where in the chain it applies, and the one thing one anchor cannot say

Two gates were live. **One is now dead:**

| gate hypothesis | prediction for Eastmire Warrior (Champion, `armorbase03`, −71, cl 11) | verdict |
|---|---|---|
| the −15 pp rides the **`armorbase03–06` table** (the −71 family) | 658.86 | **FALSIFIED** — measured 813 |
| the −15 pp rides **`armorbase05/06`** ("For Bosses" tables) | 813.28 | survives |
| the −15 pp rides **`monsterClassification` Quest/Boss** | 813.28 | survives |

I diffed `armorbase03` against `armorbase05` field-for-field at rank 13: **the only differences are
`FileDescription` and `defensiveProtection` (23 vs 76).** Their `characterLifeModifier` arrays are
byte-identical (200 elements, flat −71 through rank 19, −66 at 20). **M.** So the surviving
"armorbase05/06" gate has no *field* to hang on — it would have to be a classification gate wearing
a record-name disguise. **The two survivors are observationally identical on every monster in the
Act-1 roster** (every `armorbase05/06` user in Act 1 is `Quest`), and I do not adjudicate between
them here.

**What one anchor genuinely cannot separate: additive −15 pp vs multiplicative ×0.81013.** They
coincide at −71 by construction. They diverge at any other rank. The falsifiable discriminator, for
whoever gets the next boss readout:

| boss at charLevel ≥ 20 (`armorbase05` drops to −66) | additive −15 pp | multiplicative ×0.81013 | separation |
|---|---|---|---|
| net life factor | **0.6900** | **0.6805** | **1.4 %** |

A single boss-tier numeral at charLevel ≥ 20 settles it. Until then the rule is stated additively
because the additive form is what reproduces the provisional trash ratio as well as the boss one, and
because the multiplicative form has no candidate mechanism. **D.**

### 1.4 — The necklace reconciles to exactly zero, and that is itself a finding

My Primordian proto §0.3 warned that `greatestMonsterKilledLifeAndMana = 15,822` carried a
stochastic ≈ +300 gear term (`chanceToEquipMisc2 = 100` → `tdyn_necklace_b01_slithnecklace` →
`b001_necklace.dbr` with **unconditional flat `characterLife = 220.0`**, plus Matt's *Menacing*
prefix at `characterLife 80.0`, `lootRandomizerJitter 28`). **M.**

Solving for the flat term with the ruled factor:

```
(23,145.108 + F) × 0.640000 = 14,812.869      ⇒  F = 0.000
```

and every non-zero F is excluded by the bracket: F = +220 forces the factor to 0.63398, F = +300 to
0.63181, neither of which is a composition of anything. **The equipped necklace contributes zero to
Primordian's life pool.** The item is generated at spawn and released by `dropItems`, but its stats
are not applied to the wearer's own stat block.

Two consequences:
- **Primordian is a clean HP instrument.** The proto's recommendation to prefer a gear-free monster
  for the closure triple is **retired** — it was a correct precaution against a hazard that
  measurement has now shown does not exist.
- **The `greatestMonsterKilledLifeAndMana` triple is un-contaminated** and G-8's three-way closure
  (screen 14,812 · save 15,822 · bio mana 1,009.74) stands without a gear caveat.

**One live alternative I am naming rather than burying.** At **charLevel 11**, the *unmodified* chain
plus a rolled necklace of **F ≈ 283** also lands on 14,812 exactly
(`(18,466.6 + 283) × 0.79 = 14,812.9`), and 283 = 220 + 63 sits inside the *Menacing* jitter band.
That branch requires no −15 pp stage at all. **It is falsified by the nameplate** (§1.5) and by §1.4's
zero-residual, but it is arithmetically real and a future re-opening of the boss rule should know it
exists rather than rediscover it. **D.**

### 1.5 — The nameplate number is `charLevel`, proven on two different remappers

| frame | nameplate | record | `charLevel` eq | reading if nameplate = spawn | reading if nameplate = charLevel |
|---|---|---|---|---|---|
| 287 | Deepmire Vanguard, **11** | `slitha_melee_b01` | `charLevel*1+1` | cl 12 → **724.38** | cl 11 → **649.75** ✓ measured 649 |
| 281 | Primordian, **13** | `slith_wightmirecave01` | `charLevel*1+3` | cl 16 → no operator lands | cl 13 → **14,812.87** ✓ measured 14,812 |

**Both remappers, both readings, one answer: the number under the name is the creature's effective
`charLevel`.** §14.15's charLevel-13-vs-16 ambiguity is closed at **13**; the proto's three
candidate compositions ("cl 13, cl 17-multiplicative, cl 11+gear, all within 1–2 %") now separate —
**cl 13 survives, cl 17-multiplicative is dead** (33,673.0 × 0.435 = 14,647 ≠ 14,812), **cl 11+gear
is dead by nameplate**.

Corollary, useful for the harness: at `play_time` 5453 the player was **L10**, and Primordian's pool
is `lv6_hero` (`min = aPL+2+aPL/50`). charLevel 13 ⇒ spawn 10 ⇒ **`averagePlayerLevel` 8 at the moment
the Wightmire cave was loaded**. GD locks monster level at area-load, not at engagement. The player
levelled 8 → 10 between loading the cave and dying in it. **D, from M equations.**

---

## 2. The re-graded HP table

Player pool for the ratios: **759** (pre-gear-step, standing at both deaths) and **1,607**
(terminal — G-8 F-G8-4 corrects the banked 1600).

### 2a. Trash — Act 1, Normal, 1P, player level 12 — **UNCHANGED, now measurement-backed**

Every row below is the G-5a §2 trash table verbatim. No factor applied. The rule that produced them
is the rule that closed frame 287 four-for-four.

| name | record | spawn | charL | HP | HP/759 | HP/1607 |
|---|---|---|---|---|---|---|
| Walking Dead | `zombie_a01` | 11 | 11 | **163** | 0.21 | 0.10 |
| Walking Dead | `zombie_a01` | 12 | 12 | **181** | 0.24 | 0.11 |
| Wretcher | `zombie_b02h` | 12 | 12 | **181** | 0.24 | 0.11 |
| Plague Walker | `zombie_g01` | 12 | 12 | **181** | 0.24 | 0.11 |
| Scrapheap Rift Scourge | `prawn_a01` | 12 | 12 | **200** | 0.26 | 0.12 |
| Corruption (gazer) | `gazer_a01` | 12 | 12 | **222** | 0.29 | 0.14 |
| Skeletal Warrior | `skeleton_a01` | 12 | 12 | **223** | 0.29 | 0.14 |
| Rifthound | `rifthound_swamp_a01` | 12 | 12 | **226** | 0.30 | 0.14 |
| Dreadweave Arachnid | `spidergianta_a01` | 12 | 12 | **232** | 0.31 | 0.14 |
| Boneback Gnasher | `bonerat_meleea01` | 12 | 12 | **232** | 0.31 | 0.14 |
| Stonetusk | `boar_a01` | 12 | 12 | **352** | 0.46 | 0.22 |
| Scavenger | `scavenger_a01` | 12 | 12 | **430** | 0.57 | 0.27 |
| Cronley's Lackey / Gunman | `humanoutlaw_*_a01` | 12 | 12 | **447** | 0.59 | 0.28 |
| Tainted Hound | `zombiehound_a01` | 12 | 12 | **493** | 0.65 | 0.31 |
| Ghoul | `ghoul_a01` | 12 | 14 | **599** | 0.79 | 0.37 |
| Bloodsworn Adulant | `humanchthonic_cultist_a01` | 12 | 12 | **617** | 0.81 | 0.38 |
| Rotting Soldier | `zombie_soldiera01` | 12 | 13 | **702** | 0.92 | 0.44 |
| Gargantuan Stonetusk | `boar_a02` | 12 | 12 | **821** | 1.08 | 0.51 |

Grade: **D**, operator now **M-validated** at four points.

### 2b. Champion — **UNCHANGED**, and this is the first tier with a measured anchor at its own tier

| name | record | class | spawn | charL | HP | note |
|---|---|---|---|---|---|---|
| **Deepmire Vanguard** | `slitha_melee_b01` | Champion | 10 | **11** | **649.75 → 649** | **MEASURED on frame 287 (M)** |
| **Eastmire Warrior** | `trollhalfswamp_b02` | Champion | 9 | **11** | **813.28 → 813** | **MEASURED on frame 287 (M)** |
| Fury | `zombie_c01` | Champion | 13 | 14 | 676 | D |
| Fleshwarped Butcher | `zombiemutated_a01` | Champion | 13 | 14 | 923 | D |
| Ironhide Stonetusk | `boar_b01` | Champion | 13 | 13 | 1,326 | D |

**The champion derivation is graded against its first measured anchors and passes exactly.** This is
the answer to gandalf's task-2 ask about grading Thundersnout as "the FIRST measured champion
anchor": **Thundersnout is not a champion** (§3.3), and the first measured champion anchors are
Deepmire Vanguard and Eastmire Warrior, both of which the derivation reproduces to the digit.

### 2c. Hero — **UNCHANGED under the rule, but the tier is CONTESTED by measurement**

| name | record | class | charL | HP (P = +50) | HP if P = +35 |
|---|---|---|---|---|---|
| Dreadtusk, the Hunter's Bane | `hero/boar_h01` | Hero | 15 | **4,097** | 3,319 |
| Abner, the Forsaken One | `hero/zombie_h01` | Hero | 20 | **6,712** | 5,513 |
| Charrus | `hero/rifthound_h01` | Hero | 20 | **5,721** | 4,699 |
| *(Thundersnout ~ Thundering)* | `hero/boar_h07` | Hero | 10 | *1,892* | *1,533* | **measured 4,702 — §3.3** |

**Both surviving gate hypotheses put heroes at P = +50**, so the left column is the ruled value.
**But the one hero-tier pixel measurement in existence exceeds it by 2.49×.** I am not applying a
correction in either direction; I am flagging that this tier has an open, measured contradiction and
that a blanket downward re-grade of hero rows would be moving them *away* from the only evidence
there is. **U.**

### 2d. Boss / quest — **RE-GRADED, −15.000 pp**

`warden01` / `warden02` are `monsterClassification = Quest` with `armorbase05` — **structurally
identical to Primordian on both surviving gates**, so the correction applies with the same confidence
as the anchor.

| name | record | class | charL eq | charL | G-5a (P=+50) | **RE-GRADED (P=+35)** | Δ |
|---|---|---|---|---|---|---|---|
| **Primordian, the Forgotten One** | `boss&quest/slith_wightmirecave01` | Quest | `charLevel*1+3` | **13** | 18,284.6 | **14,812** (M, screen) | −19.0 % |
| **Warden Krieg** ph.1 | `boss&quest/warden01` | Quest | `(charLevel*1.1)+2` | 18 | 26,155 | **21,189** | −19.0 % |
| **Warden Krieg** ph.2 | `boss&quest/warden02` | Quest | `(charLevel*1.1)+2` | 18 | 35,198 | **28,514** | −19.0 % |
| Warden Krieg, both phases | — | — | — | 18 | 61,353 | **49,703** | −19.0 % |

Primordian, re-graded, against the player pool: **14,812 / 759 = 19.5×**; **/1,607 = 9.2×**.
Warden Krieg combined: **65.5×** / **30.9×**.

Primordian across the level band, for a harness that wants to sweep it (**D**, P = +35):

| charLevel | 11 | 12 | **13** | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|
| HP | 11,818 | 13,283 | **14,812** | 16,407 | 18,063 | 19,778 | 21,551 | 23,380 |

---

## 3. Grading the six trash maxima against the G-5a spawn-pool predictions

| frame | `play_time` | max | verdict | attribution | grade |
|---|---|---|---|---|---|
| 87 | 1560 | **58** | **CONSISTENT** | `zombie_a01` Walking Dead @ cl 4 → 58.8309 → 58. Player was ~L4 (Barrog nameplate = 4); `lv2_normal` puts trash at aPL−1..aPL. Zombie country (Burrwitch). | **D-strong** — 58 is a dense collision band (55 corpus hits); not level-pinned |
| 287 | 5790 | **326** ×2 | **EXACT** | `trollhalfswamp_a02` **Eastmire Herder**, Common, `(charLevel*1)+2`, cl 11 → **326.3945** | **M-closed** |
| 287 | 5790 | **649** | **EXACT** | `slitha_melee_b01` **Deepmire Vanguard**, Champion, cl 11 → **649.7467** — *and the frame's own nameplate names it, at level 11* | **M-closed** |
| 287 | 5790 | **813** | **EXACT** | `trollhalfswamp_b02` **Eastmire Warrior**, Champion, `(charLevel*1)+2`, cl 11 → **813.2768** | **M-closed** |
| 176 | 3046 | **434** | **UNRESOLVED** | see §3.2 | **U** |
| 176 | 3046 | **1,820** | **UNRESOLVED** | see §3.2 | **U** |

**No G-5a row is falsified by any of the six.** Four are reproduced exactly and one strongly; the two
that resist are both on frame 176, and they resist *together with* the champion/hero anchor on the
same three-frame cluster (§3.2) — which is a pattern, not six independent failures.

### 3.1 — On "1,820 looks high for trash — champion mislabel? hero pet?", named honestly

**Neither, and I cannot name it.** 1,820 is entirely ordinary for a *champion* (Deepmire Evocator
reaches 1,050 at cl 13; Gargantuan Voidtusk 2,201 at cl 16), so "too high for trash" is right and
"champion" is the correct tier guess. But the specific value does not land: under the ratified
champion rule (P = +50) the only corpus records flooring to exactly 1,820 are `wendigo_a01`,
`scorpion_a01` and `dranghoul_a01` **at charLevel 20** — all Act 3+ rosters at twice the run's level.
**There is no Act-1 beast record at any charLevel that produces 1,820.** It is not a mislabel of a
row I have; it is a value my model cannot make. Hero pet is excluded: the run has no pets and no
summon on frame 176.

### 3.2 — Frame 174–176 is a coherent anomaly, not three unlucky reads

The three unresolved values (**4,702** at f174/175, **434** and **1,820** at f176) are all inside one
35-second window, and **all three are unreachable while both other clusters close exactly.**

I ran an exhaustive negative: every creature record in all four archives
(`records/creatures/**`, ~3,000 records with `Class = Monster` and a bio), at every `charLevel`
reachable from spawn levels 1–35, under **eight** composition hypotheses — P = +35, P = +50,
multiplicative `(1+Σ/100)×1.50`, no-pak, raw bio, and three challenge-layer variants built from
`balancingadjustment_challengemode_enemies01.dbr` (`characterLifeModifier = +140`, M). Life
contributions were summed both `Skill_Passive`-only and class-agnostic.

**Hits floor-equal to 4,702: zero, under every hypothesis.** Nearest approaches within ±25 are all
charLevel 19+ monsters from later acts. The `~ Thundering` archetype contributes nothing —
I read all twenty `heroskills/archetypes/*_passivestatmodifier.dbr` records and
**every one has `characterLifeModifier = 0` and `characterLife = 0` (M)**. `boar_h07` equips only
components, a crafting mat and a constitution potion (`chanceToEquipMisc1/2/3` → `mt_comp_*`,
`craft_ancientheart`, `tdyn_constitution_b01`) — none of which are stat-bearing.

**Reading (D, offered as a lead, not a finding):** an unmodelled spawn-time adjustment layer applied
to that encounter — the most likely candidates being a devotion-shrine guardian wave, a rift/wave
event, or a challenge layer — would explain all three at once and explains nothing about the other
two clusters, which is the right shape for the evidence. I did not find the record that does it.

### 3.3 — Correction to G-8: Thundersnout is a **Hero**, and `~ Affix` is not a tier marker

`Thundersnout ~ Thundering` = `tagGDX3HeroBoar_H01`, and the **single** creature record carrying it is
`records/creatures/enemies/hero/boar_h07.dbr` (archive **GDX3**), with
**`monsterClassification = Hero`**, `charLevel = charLevel*1`, bio `bio_hero_standard_01`,
`armorbase04`. **M** (exhaustive tag sweep + exhaustive creature-record sweep, one hit each).

G-8 §6.2's naming heuristic — `Name ~ Affix` ⇒ champion, `Name, the Epithet` ⇒ hero — does not hold
in this corpus. Counter-examples, all **M**: `Groble ~ Snake Clan Scavenger` = **Common**;
`Plaguehound ~ Alpha` = **Champion**; `Thundersnout ~ Thundering`, `Ragesnout ~ Swift`,
`Traglodan ~ Voidtouched`, `Wrallan ~ Electrified` = **Hero**. The `~` infix marks a **monster
archetype affix** (the GDX1/GDX3 `heroskills/archetypes/` system), which is applied across tiers.
This does not weaken G-8's measurement — it re-files it from champion to hero, which is where the
2.49× contradiction lives.

At charLevel 10 the ruled hero value is **1,892**; the screen says **4,702**. Ratio **2.485**. There is
no integer charLevel at which `bio_hero_standard_01` produces 4,702 under any constant factor
(0.64 ⇒ cl 21.02; 0.79 ⇒ cl 18.29; 1.00 ⇒ cl 15.6 — none integral), and the nameplate says 10.
**U. Flagged, not smoothed.**

**What would close it, cheapest first:** (a) any frame carrying numerals **and** a nameplate for a
monster in the f174–176 window, which would fix the level the way frame 287 did; (b) a
`greatestMonsterKilled{Level,LifeAndMana}` triple from a save whose greatest kill is a **Hero**;
(c) a numeral readout for any hero elsewhere in the corpus of stills.

---

## 4. Harness-ready HP for the three ratified G-5 scenario tiers

All HP **D** unless marked M. Damage columns are **HELD** per §14.10 and are not restated here — see §5.

### Tier 1 — trash packs (player level 12, Act 1, Normal, 1P)

Use §2a verbatim. Pack sizing from G-5a §3 (`proxyPoolEquation_01` is identity on Normal, so pool
numbers are literal pack sizes) — unchanged:

| quantity | value | source |
|---|---|---|
| pack HP, `p_zombie_n` at 1–8 spawns | **163 – 1,448** (`zombie_a01` cl 11) | D |
| pack HP, `p_beasts_boar_n` at 2–9 spawns | **704 – 3,168** (`boar_a01` cl 12) | D |
| champion uplift | drawn from a separate `nameChampionN` roster, not a multiplier | M |
| simultaneous melee engagement cap | `numAttackSlots = 4` | M |
| median trash HP | **226** | D |
| median trash HP / 759 | **0.30** | D |

### Tier 2 — champion + hero mixed

| actor | record | charL | HP | grade |
|---|---|---|---|---|
| Deepmire Vanguard | `slitha_melee_b01` | 11 | **649** | **M** |
| Eastmire Warrior | `trollhalfswamp_b02` | 11 | **813** | **M** |
| Fury | `zombie_c01` | 14 | 676 | D |
| Fleshwarped Butcher | `zombiemutated_a01` | 14 | 923 | D |
| Ironhide Stonetusk | `boar_b01` | 13 | 1,326 | D |
| Dreadtusk, the Hunter's Bane (hero) | `hero/boar_h01` | 15 | 4,097 | D — **tier contested, §3.3** |
| Abner, the Forsaken One (hero) | `hero/zombie_h01` | 20 | 6,712 | D — **tier contested** |
| Charrus (hero) | `hero/rifthound_h01` | 20 | 5,721 | D — **tier contested** |

**Run the hero rows at the tabulated values and carry the §3.3 caveat with them.** If the harness
needs a single sensitivity knob, sweep heroes over **[1.0×, 2.5×]** rather than applying any single
correction — that is the honest span between the rule and the only measurement.

### Tier 3 — the Primordian trio at level 13

`records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr`: `spawnMin = spawnMax = 3`,
all three `alwaysSpawnN = True`, limit 1 each. **The encounter is a fixed trio. M.**

Level resolution at `averagePlayerLevel = 8` (forced by Primordian charLevel 13, §1.5):
`lv6_hero` → spawn 10 → Primordian cl 13 · `lv4_champion+` (`min = aPL+1`, `max = (aPL+1)+(aPL/50)`)
→ spawn 9 → escorts at cl 10 / cl 11. **M equations, D evaluation.**

| actor | record | class | charL eq | **charL** | **HP** | armor | OA | DA | aspd (post-pak) | run (post-pak) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Primordian, the Forgotten One** | `boss&quest/slith_wightmirecave01` | Quest | `charLevel*1+3` | **13** | **14,812** (M) | 76 | 423 | 381 | 0.90 | 0.70 |
| **Deepmire Vanguard** | `slitha_melee_b01` | Champion | `charLevel*1+1` | **10** | **577** | 7 | 276 | 275 | 0.90 | 0.71 |
| **Deepmire Evocator** | `slitha_shaman_c01` | Champion | `charLevel*1+2` | **11** | **846** | 8 | 317 | 299 | 0.68 | 0.71 |
| **encounter total** | | | | | **16,235** | | | | | |

Encounter HP against the player pool: **16,235 / 759 = 21.4×**; **/1,607 = 10.1×**.
Primordian alone is **91.2 %** of the trio's HP — the escorts are a pressure term, not a HP term.

**Escort protos — extracted this pass, closing proto §7.6 (all M unless noted):**

| field | `slitha_melee_b01` — Deepmire Vanguard | `slitha_shaman_c01` — Deepmire Evocator |
|---|---|---|
| `monsterClassification` | Champion | Champion |
| bio | (slith champion family) | (slith champion family) |
| life-modifier source | `armorbase02` @ rank = cl → **−58** | `armorbase02` @ rank = cl → **−58** |
| base-attack table | `damagebase_physical02` | `damagebase_physical02` |
| controller | `controller_slith_melee.dbr` | `controller_slith_ranged.dbr` |
| `characterAttackSpeed` / `RunSpeed` (pre-pak) | 1.00 / 0.87 | 0.75 / 0.87 |
| `numAttackSlots` / `numDefenseSlots` | 4 / 4 | 4 / 4 |
| `experiencePoints` | 100 | 200 |
| resistances | Life 10, Poison 15 | Life 10, Poison 15 |
| base dmg/hit (**D — composed under the §14.10-held damage operator; provisional**) | 36.7 – 42.8 phys + 9.6 cold | 39.2 – 49.6 phys |
| abilities (raw array slices, **NOT composed**) | `slith_tidalwave` `Skill_AttackWave` r3: phys 39, **cold 168** | `slith_tidalorb` `Skill_AttackProjectile` r3: phys 31–41, **cold 76–93** · `geyser1` `Skill_AttackProjectileAreaEffect` r3: phys 21, cold 59 · `slith_iceshield` `Skill_BuffRadiusToggled` r3 |

**The trio's damage identity is cold, on all three actors.** Primordian's kit is ~85 % cold (proto
§3d); both escorts add cold riders and the Evocator is a ranged cold caster with a toggled ice
shield. Any G-5 run of this scenario that models the escorts as generic melee filler will
under-represent the cold channel by roughly a third of the incoming events.

Alternative level branch, if the harness prefers the max-roll reading (`averagePlayerLevel = 7`,
`lv6_hero` max = aPL+3): escorts drop to spawn 8 → cl 9 / cl 10 → **507 / 749**, Primordian unchanged
at cl 13. Encounter total **16,068**. **D.**

---

## 5. Damage rows — HELD, and the ceiling they must now satisfy

**No damage row is un-held.** §14.10's hold on the champion/hero/boss damage regime stands: the
composition operator for `offensiveTotalDamageModifier` remains adjudicated by contradiction only
(G-5a §1f), and at boss tier the additive sum reaches −95 % at cl 13, deep in the unmeasured clamp
band where a 4-point array shift moves output ~80 %.

**But the hold now has a numeric ceiling, and it is not decorative.** From my sustain decomposition:
`greatestDamageReceived = 260.50`, **post-mitigation**, and **no single event in the entire run
exceeded it** — Primordian's death included.

Necessary condition for any future resolution, assuming *zero* player mitigation (the loosest
possible form of the bound), evaluated on Primordian's own raw arrays at cl 13:

| ability | raw at rank 4 | composed single-event ceiling | ⇒ boss-tier TDM multiplier must be |
|---|---|---|---|
| `primordian_wave` | 122 phys + 210 cold = **332** | ≤ 260.50 | **≤ 0.785** (TDM ≤ −21.5 %) |
| `primordian_frigidring`, outer band (`range3` 9–20 m → **140 %**) | (118 phys + 200 cold) × 1.4 = **445.2** | ≤ 260.50 | **≤ 0.585** (TDM ≤ −41.5 %) |

**So the ceiling does not falsify the additive reading** (−95 % ⇒ multiplier 0.05, far under), **but
it does falsify any clamp that floors the boss-tier TDM pool at or above ≈ −42 %.** With the player's
real mitigation folded in the true bound is strictly tighter. That is a genuine constraint on the
clamp's shape, delivered without composing a single held row. **D, from M arrays and one M client
statistic.**

---

## 6. Records and tooling

**New this pass** (all under `legolas/scratch/2026-07-28-kitcal1-g5a/`, non-production scratch):
`sweep.py`, `sweep2.py`, `sweep3.py`, `sweep4.py` (corpus-wide life-composition sweeps),
`lifeprobe.py`, `arrays.py`, `slith.py`, `tro.py`, `fam.py`, `diffab.py`, `chk.py`, `final.py`,
`dumprec.py`, `find_rec.py`, `gameprobe.py`, `ge.py`, `arch.py`, `arch2.py`.
All import `g5a_resolve.py` → gandalf's G-4 wrapper → `research/scripts/gd_arz_adapter_2026_07_24.py`.
**Nothing rebuilt. Nothing written outside `notes/` and the scratch dir.**

**Records newly read this pass:** `records/creatures/enemies/hero/boar_h07.dbr` ·
`records/creatures/enemies/trollhalfswamp_{a01,a02,b01,b02}.dbr` ·
`records/creatures/enemies/slitha_{melee_a01,melee_b01,melee_c01,melee_c02,shaman_b01,shaman_b02,shaman_c01,shaman_c02}.dbr` ·
`records/creatures/enemies/bios/{bio_hero_standard_01,bio_boss_standard_01,bio_zombie_01,bio_boar_01}.dbr` ·
`records/skills/nonplayerskills/passive/armorbase0{1..6}.dbr` (full 200-element `characterLifeModifier` arrays) ·
all twenty `*/heroskills/archetypes/*_passivestatmodifier.dbr` ·
`records/skills/nonplayerskills/{attackmelee/slith_tidalwave,attackprojectile/slith_tidalorb,…/geyser1,…/slith_iceshield}.dbr` ·
`records/game/{gameengine,balancingadjustment_challengemode_enemies01,balancingadjustment_ultramode_enemies01,gameascendant}.dbr` ·
`records/proxies/{lv2_normal,lv4_champion,lv4_champion+,lv6_hero}.dbr` ·
`records/items/loottables/misc/tdyn_constitution_{a01,b01}.dbr`

**Provenance:** corpus root `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`; archive
SHA-256s as banked in the G-5a ledger §Provenance, unchanged. Display names via `*/resources/Text_EN.arc`,
20,394 tags.

---

## 7. Confidence ledger

### M-closed (measured, exact, multiple independent constraints)
- The trash/champion composition rule at P = +50 — four exact reproductions on one frame, one of them
  identity-and-level-pinned by its own nameplate.
- The boss/quest net life factor **0.640000 ± 0.0043 pp** at charLevel 13.
- Equipped-gear life contributes **exactly zero** to a monster's life pool.
- Nameplate number = creature `charLevel`, on two different remap equations.
- `Thundersnout ~ Thundering` = `hero/boar_h07.dbr`, `monsterClassification = Hero`.
- Every field, array and equation cited in §1–§4.

### D (derived; arithmetic shown, assumption named)
- The **−15.000 pp** boss stage expressed additively. Additive vs multiplicative-×0.81013 is not
  separable from one anchor; the 1.4 % discriminator at charLevel ≥ 20 is stated in §1.3.
- Which gate carries it (`monsterClassification` Quest/Boss vs `armorbase05/06`). The `armorbase03–06`
  gate is **falsified**; the two survivors are observationally identical across the Act-1 roster.
- The Warden Krieg re-grade — same classification, same armour table, same bio family as the anchor,
  but not itself measured.
- The escort damage rows (composed under the §14.10-held operator; provisional, flagged in-table).

### U — flagged, not guessed
1. **Thundersnout's 4,702.** Unreachable by any record × charLevel × operator in the corpus.
   Exhaustive negative recorded in §3.2. The hero tier is **contested by measurement in the opposite
   direction from a correction factor** — do not apply one.
2. **434 and 1,820 on frame 176.** Same window, same failure mode. §3.1–§3.2.
3. **Whether heroes take P = +50 or P = +35.** Both surviving gates say +50; the only measurement
   says neither. Sweep the harness, don't pick.
4. **Champion/hero/boss damage regime.** HELD per §14.10, un-touched, now bounded above by §5.
5. **Attack cadence in seconds.** Unchanged from G-5a §6.2 / proto §7.4 — `characterAttackSpeed` is a
   multiplier on an animation-driven base living in `.anm` tables this lane does not parse.
6. **Veteran mode.** Still not modelled, still not located. If the fixture was played on Veteran
   rather than plain Normal, every figure here is a floor — though note that the frame-287 four-way
   closure at plain-Normal values is strong evidence the fixture was **not** on Veteran.

---

*Downstream: gandalf (KC1 conductor) — §0.1 and §0.2 are charter-level (§14.11 discharged, §14.15
closed); §2d is the ledger amendment; §4 is the harness hand-off; §5 bounds the §14.10 hold without
lifting it. galadriel — §3.3 corrects the G-8 tier attribution and §3.2 names the f174–176 window as
worth another capture pass. No canonical doc amended by this note.*
