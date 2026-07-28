# KIT-CAL-1 U-1 — kit values at measured rank, all rolled gear stats, and the boss fixture

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Work-package:** U-1 (expanded by Matt ruling)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.6 / §14.8 (conductor: gandalf)
**Class:** evidentiary — measured extraction from primary source
**Mode:** read-only. Writes confined to this note + `legolas/scratch/2026-07-28-kitcal1-u1/`.

**Predecessors this note consumes (and does not re-derive):**
`legolas/notes/2026-07-28-kitcal1-g7-gdc-save-findings.md` (fixture identity, record paths, ranks) ·
`legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` (the five-record chain) ·
`galadriel/notes/2026-07-28-gd-playtest-v1-g6-skill-screenshots.md` (tooltip reads — the pinning instrument).

**Corpus (read-only):** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` —
`database/database.arz` (34,114) · `gdx1/database/GDX1.arz` (18,447) · `gdx2/database/GDX2.arz` (16,451) ·
`gdx3/database/GDX3.arz` (24,178). SHA-256s banked in G-5a §Provenance; unchanged.

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`) · **M-pin** = MEASURED and independently
tooltip-pinned by G-6 · **D** = DERIVED (computed; composition operator stated) · **D-range** =
roll window from source, per-seed value not pinned · **C** = CONTESTED (two instruments disagree) ·
**U** = UNRESOLVED.

**Rank-array convention (M, verified):** GD skill arrays are 0-indexed — `array[0]` is rank 1.
Verified against G-6's f153 tooltip read at rank 12 (`skillTargetNumber[11] = 4`, `skillTargetAngle[11] = 130`,
`weaponDamagePct[11] = 130` — all three match the running client) and again at rank 16.

---

## Headline

1. **Feral Claws at rank 16 is 150 % main-hand weapon damage + 237 flat Pierce, 5 targets, 150° arc,
   5 energy, no cooldown.** Every one of those five numbers is independently confirmed on G-6's f210
   tooltip. The 237 Pierce is the *entire* flat channel — and it is **100 % Chaos in play** (Blight of
   Ch'thon). The kit carries **no native Physical damage at all**; all Physical comes from the weapon.
2. **The max-HP-step hypothesis is FALSIFIED at source.** `werewolf1.dbr` grants **zero** stats at any
   rank — no `characterLife`, no modifiers, nothing but mesh/anim replacement, a granted-skill list and
   an energy figure. The 759 → 1600 step is **not** the transform. It is gear, and it now closes to
   **≈ 96 %** (§2.3), up from G-6's 87.6 %.
3. **The +Health cross-check PASSES.** Source nominal for the four attested items is **+700** with a
   roll window **[627, 773]**; G-6's tooltip-pinned **+737** sits inside it. Three of four reconcile
   item-by-item inside their own jitter windows. One residual (§2.3c).
4. **The Slith boss resolution does NOT hit 15,822 under the G-5a chain as stated — it over-predicts by
   22.0 %.** But the miss is *clean*: the client's number pins charLevel **13** and pins the net
   additive life-modifier pool at **exactly −36.00 %**, where the chain composes **−21 %**. This is the
   first live-client datum ever put against that chain, and it says the chain's HP rule is wrong by a
   flat 15 percentage points of life modifier. **Every HP figure in the G-5a ledger is ~19–23 % high.**
   See §3.2 — this is the load-bearing finding of the pass.
5. **G-6's three out-of-seam requests are all closed** (§4), including the square-vs-circle node
   identity, which the source settles by a one-bit field (`roundBitmap`).

---

## 1 — Skill rank-array values at the MEASURED rank

All eight build records live in `gdx3/database/GDX3.arz`. Tree membership from
`records/skills/playerclass10/_classtree_class10.dbr` (`SkillTree`, 39 `skillNameN` entries).

### 1.1 — `werewolf1.dbr` — Werewolf transform @ rank 16 (hard max)

`Skill_Shapeshift` · `skillMaxLevel 16` · `skillUltimateLevel 26` · `skillTier 1` · tree `skillName22`.

| Field | Value @16 | Grade |
|---|---|---|
| `skillManaCost[16]` | **170.0** (array `[50,58,66,…,170,…,250]`, +8/rank) | M |
| `activeSkillSet` | **1** | M |
| `grantedSkills` | `werewolf1_skill01_claws.dbr`, `werewolf1_skill02_charge.dbr` | M |
| `replacementMeshMale` / `Anims` / `Sounds` / `Footsteps` | werewolf set | M |
| `notDispelable` | 1 | M |
| `distanceProfile` | Short | M |
| **every `character*` stat field** | **0.0 at every rank** | **M** |
| **every `offensive*` / `defensive*` field** | **0.0 at every rank** | **M** |

**The transform grants NO stats.** Of 666 fields, the only non-default ones are the four above plus
FX/sound/UI. There is **no `characterLife`, no `characterLifeModifier`, no `characterOffensiveAbility`,
no attack-speed or run-speed modifier** — at rank 1 or rank 16 or anywhere between.

> **This closes G-7 §7 and it closes it against the hypothesis.** G-7 wrote that reading
> `werewolf1`'s `characterLife*` rank arrays was what the max-HP-step question needed. Those arrays
> **do not exist**. The 759 → 1600 step at the R2/R3 boundary cannot be the Werewolf toggle, because
> the Werewolf toggle does not touch the health pool at any rank. G-6's gear itemisation is the
> explanation, and §2.3 below closes it to ≈ 96 %.

**Not asserted:** whether `skillManaCost` on a `Skill_Shapeshift` is an activation cost or a standing
energy reserve. The field is reported verbatim; GD's toggle semantics are not stated in source and the
fixture has no tooltip frame of the transform's cost line. Graded **U**. (If it *is* a reserve, the
build reserved 170 + 50 = 220 energy against a base pool of 250 + 55 mastery = 305 — worth a look.)

### 1.2 — `werewolf1_skill01_claws.dbr` — Feral Claws @ rank 16

`Skill_AttackWeapon` · `skillMaxLevel 16` · `skillUltimateLevel 26` · `skillSet 1` ·
`distanceProfile Melee` · `skillSpecialAnimationName DoubleClaw` · tree `skillName26`.

| Field | @ rank 16 | G-6 f210 tooltip | Grade |
|---|---|---|---|
| `weaponDamagePct` | **150.0** | "150% Main Hand Damage" | **M-pin** |
| `offensivePierceMin` | **237.0** | "237 Piercing Damage" | **M-pin** |
| `offensivePierceMax` | *(absent — flat, not a range)* | — | M |
| `skillTargetNumber` | **5** | "5 Target Maximum" | **M-pin** |
| `skillTargetAngle` | **150.0°** | "150 Degree Attack Arc" | **M-pin** |
| `skillManaCost` | **5.0** | "5 Energy Cost" | **M-pin** |
| `skillCooldownTime` | *(absent — **no cooldown**)* | *(no recharge line)* | **M-pin** |
| `characterAttackSpeed` | 0.0 (no modifier) | — | M |
| `characterBaseAttackSpeedTag` | `CharacterAttackSpeedAverage` | — | M |
| every other damage type | **0.0** | — | **M** |

**Full 26-element rank curves (M).** Ranks 1–16 are the reachable band; 17–26 are ultimate ranks
(`+skills`), unreachable in this fixture.

| rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | **16** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `offensivePierceMin` | 12 | 27 | 42 | 57 | 72 | 87 | 102 | 117 | 132 | 147 | 162 | 177 | 192 | 207 | 222 | **237** |
| `weaponDamagePct` | 70 | 77 | 84 | 90 | 95 | 100 | 105 | 110 | 115 | 120 | 125 | 130 | 135 | 140 | 145 | **150** |
| `skillTargetNumber` | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | **5** |
| `skillTargetAngle` | 90 | 90 | 110 | 110 | 110 | 110 | 110 | 130 | 130 | 130 | 130 | 130 | 150 | 150 | 150 | **150** |
| `skillManaCost` | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | **5** |

`offensivePierceMin` is **exactly linear at +15/rank** across 1→16. This is the array behind G-6's
dated A-step (F-G6-5) and it confirms that ledger row-for-row: cap reached at rank 13, not 16.

> **G-6's one UNCERTAIN damage row, resolved.** G-6 flagged f153's rank-12 claws reading "103 Piercing
> Damage" against a spec interpolation of ~177. The array says rank 12 = **177** exactly. The pixel read
> was wrong, not the source; rank 16 = 237 matches on both instruments. Graded **M** (source) with the
> pixel disagreement recorded, not averaged.

### 1.3 — `werewolf1_skill02_charge.dbr` — Rip and Tear @ rank 16

`Skill_AttackPathCharge` · `skillMaxLevel 16` · `skillUltimateLevel 26` · `skillSet 1` ·
`distanceProfile Long` · `targetingMode Point` · tree `skillName28`.

| Field | @ rank 16 | G-6 f210 tooltip | Grade |
|---|---|---|---|
| `weaponDamagePct` | **295.0** | "295% Main Hand Damage" | **M-pin** |
| `offensivePierceMin` | **375.0** | "375 Piercing Damage" | **M-pin** |
| `offensiveSlowBleedingMin` | **270.0** | — | M |
| `offensiveSlowBleedingDurationMin` | **3.0 s** | "810 Bleeding Damage over 3 Seconds" | **M-pin** |
| `skillManaCost` | **42.0** | "42 Energy Cost" | **M-pin** |
| `skillCooldownTime` | **4.0 s** | "4 Second Skill Recharge" | **M-pin** |
| `skillTargetRadius` | **2.5 m** | "2.5 Meter Target Area" | **M-pin** |
| `waveDistance` | **14.0 m** | "14 Meter Range" | **M-pin** |
| `characterRunSpeedModifier` | **+200 %** | "+200% Movement Speed" | **M-pin** |
| `offensiveKnockdownMin` | **0.5 s** | "Knockdown target for 0.5 Seconds" | **M-pin** |
| `timeBetweenAttacks` | 100 ms | — | M |
| `endRadiusMultiplier` / `maxMoveRatio` / `secondarySkillDistance` | 1.5 / 2.0 / 1.0 | — | M |
| `ragDollAmplification` / `ragDollDirection` | 1.8 / Push | — | M |
| `skillAllowsWarmUp` | 1 (warm-up FX + cast sound) | — | M |

**The bleed DoT's units are settled (D, one arithmetic step).** `offensiveSlowBleedingMin = 270` with
`…DurationMin = 3.0` renders as **810 over 3 s** — so `offensiveSlowBleedingMin` is **damage per
second** and the GD tooltip prints the *total*. 270 × 3 = 810, exact. This is a reusable unit rule for
every `offensiveSlow*Min` field in the corpus and it was not stated anywhere in G-4/G-5a/G-6.

**Full 26-element rank curves (M):**

| rank | 1 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | **16** | 20 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `offensivePierceMin` | 15 | 39 | 87 | 135 | 183 | 231 | 279 | 327 | **375** | 491 | 718 |
| `offensiveSlowBleedingMin` (/s) | 15 | 32 | 66 | 100 | 134 | 168 | 202 | 236 | **270** | 346 | 484 |
| `weaponDamagePct` | 100 | 113 | 139 | 165 | 191 | 217 | 243 | 269 | **295** | 331 | 385 |
| `skillManaCost` | 12 | 14 | 18 | 22 | 26 | 30 | 34 | 38 | **42** | 50 | 62 |

`offensivePierceMin` +24/rank, bleed +17/rank, `weaponDamagePct` +13/rank — all exactly linear 1→16.
**`skillCooldownTime`, `skillTargetRadius`, `waveDistance`, `characterRunSpeedModifier` and
`offensiveKnockdownMin` are scalars, not arrays** — they do not scale with rank at all.

**Off-hand (G-6's unmodelled line).** The record carries **no** off-hand field. G-6's f210
"295% Off-Hand Damage (177 – 181)" is the engine applying `weaponDamagePct` to the *shield* as a
second weapon (`b013a_shield.dbr` carries `offensivePhysicalMin = 34`, §2.2). The dual-wield handling
lives in `gameengine.dbr` (`dwWeaponDamageFactor = 1.0`, `dwWeaponSpeedFactor = 0.5`,
`2hWeaponDamageFactor = 1.0`) — **not** in the skill record. Graded **D**; the exact off-hand
arithmetic is **U** (see §5).

### 1.4 — `werewolf1b.dbr` — Blight of Ch'thon @ rank 1 (confirmed)

`Skill_Transmuter` · `skillMaxLevel 1` · `skillUltimateLevel 1` · `skillTier 2` · tree `skillName23`.

| Field | Value | Grade |
|---|---|---|
| `conversionInType` → `conversionOutType` | **Pierce → Chaos** | **M-pin** (G-6 f351 tooltip) |
| `conversionPercentage` | **100.0** | **M-pin** |
| `shapeshiftMeshOverrideMale` / `Female` | `hero_werewolf01b.msh` / `heroine_werewolf01b.msh` | M |
| every offensive / defensive / character field | **0.0** | M |

**Confirmed from the record fields as the commission asked.** The 100 % Pierce→Chaos is the *only*
mechanic; there is nothing else on the record. Composed with §1.2/§1.3: **claws' 237 and charge's 375
flat Pierce resolve as Chaos**, and since neither skill carries a Physical term, the kit's *entire*
native damage channel is Chaos. Physical/Acid arrive only via `weaponDamagePct` off the weapon.

### 1.5 — `passive02.dbr` — Battle Surge @ rank 1 (confirmed)

`Skill_PassiveOnCritBuffSelf` · `skillMaxLevel 12` · `skillUltimateLevel 22` · `skillTier 2` ·
`roundBitmap 1` · tree `skillName38`.

| Field | @ rank 1 | G-6 f213/f352 tooltip | Grade |
|---|---|---|---|
| `onHitActivationChance` | **100.0** (scalar) | "100% Chance of Activating" | **M-pin** |
| `skillCooldownTime[1]` | **6.0 s** | "6 Second Skill Recharge" | **M-pin** |
| `skillActiveDuration` | **3.0 s** (scalar) | "3 Second Duration" | **M-pin** |
| `skillLifePercentBuffDuration[1]` | **8.0 %/s** | "Restores 8% Health Per Second" | **M-pin** |
| `characterManaRegen[1]` | **4.0/s** | "+4 Energy Regenerated per second" | **M-pin** |
| `skillActivatedAuraName` | `records/fx/skillclass10/battlesurge_fx.dbr` | — | M |

**CONFIRMED, 5/5, exactly as G-6 read it.** Rank curves (22 elements):
`skillLifePercentBuffDuration = [8,9,9,10,10,11,11,12,12,13,13,14,…,18]` ·
`skillCooldownTime = [6.0, 5.5, 5.1, 4.8, 4.5, …, 2.4]` · `characterManaRegen = [4.0, 5.2, 6.4, …]`.

**Sustain magnitude (D):** 8 %/s × 3 s = **24 % of max HP per proc**, gated on a crit, 100 % chance,
6 s recharge ⇒ theoretical ceiling **4 % max-HP/s**. Against the fixture's 66 `criticalHitsInflicted`
over 7,096 s, an upper bound of 66 procs × 24 % — at the post-step pool of ~1600 that is **≤ 25,344
HP healed**, comfortably bracketing the charter's measured `life_healed = 12,468.06`. Battle Surge is
therefore a *sufficient* explanation for the whole healed channel, not merely a contributor.
Graded **D** — proc count is bounded by crits, not measured per-proc.

### 1.6 — `amatokpact1.dbr` — Amatok's Pact @ rank 1: the cold aura, identified

**This is G-6's "reserved cold aura".** `amatokpact1.dbr` is a 4-field stub
(`Skill_BuffRadiusToggled`) whose entire payload is `buffSkillName → amatokpact1_buff.dbr`
(`SkillBuff_Passive`, `skillMaxLevel 12`, `skillTier 2`). Tree `skillName2`. Identified via the
documented one-hop `buffSkillName` link (the same link G-7 §4 used for the display name).

| Field (on `amatokpact1_buff.dbr`) | @ rank 1 | G-6 tooltip | Grade |
|---|---|---|---|
| `characterManaLimitReserve[1]` | **50.0** | "50 Energy Reserved" | **M-pin** |
| `skillTargetRadius` | **12.0 m** (scalar) | "12 Meter Radius" | **M-pin** |
| `defensiveProtection[1]` | **16.0 Armor** | "+16 Armor" | **M-pin** |
| `characterDefensiveAbility[1]` | **20.0** | "+20 Defensive Ability" | **M-pin** |
| `offensiveColdMin[1]` / `Max[1]` | **5.0 – 6.0** | "8–10 Cold Damage" (f316) | **C → resolved below** |
| `offensiveSlowPhysicalGlobal` / `XOR`, `offensiveSlowBleedingGlobal` / `XOR` | 1 | — | M |

Rank curves (22 elements): `defensiveProtection` +16/rank · `characterDefensiveAbility` +20/rank ·
`characterManaLimitReserve` +10/rank · `offensiveColdMin` 5,7,9,11,… · `offensiveColdMax` 6,9,12,15,…

**G-6's open question — "it scales with something the tooltip does not name" — is answered (D).**
The aura's cold damage read 6–8 at f211, 8–10 at f316, 9–10 at f350 while the rank never left 1. Two
multipliers explain it, both from source:

1. **Summed `+% Cold Damage` affixes** — gloves suffix `a029e` (7 nominal), shoulders suffix `a029e`
   (7 nominal), legs prefix `b_ar030_ar` `offensiveColdModifier` (12 nominal) ⇒ **≈ +28 %** at end of
   run (G-6 pinned the gloves/shoulders rolls at 8 % each).
2. **The Spirit term** in `records/game/combatformulas.dbr`:
   `magicalDamageEquation = magicalDamageDV * ((intelligenceDV / 215) + 1)`. End-of-run Spirit ≈ 82–99
   (save base 50, + legs prefix/suffix Intelligence, × chest/belt `characterIntelligenceModifier`).

Worked at Spirit ≈ 82.5: `5 × 1.28 × (82.5/215 + 1) = 8.9` and `6 × 1.28 × 1.384 = 10.6` ⇒ **9 – 11**
against G-6's **9 – 10** at f350. The *growth over the run* is gear acquisition on both terms, not a
rank change. Graded **D** (arithmetic shown, Spirit input approximate).

### 1.7 — `onslaught1.dbr` @ rank 13 — **INERT** (extracted for completeness only)

`Skill_WeaponPool_BasicAttack` · `skillMaxLevel 16` · `skillTier 1` · tree `skillName5`.

> ⚠️ **NEVER TRIGGERED.** `werewolf1.skillSet = 1` / `activeSkillSet = 1` partitions weapon-pool skills
> out of the transform (charter §13; G-6 F-G6-4 quotes the game's own tooltip: *"…cannot trigger weapon
> pool skills"*). Every number below was live in the character sheet and **applied zero times in play**.
> Do not let it into a damage model.

| Field | @ rank 13 | Grade |
|---|---|---|
| `weaponDamagePct` | 158.0 | M |
| `offensiveColdMin` | 83.0 (flat; no Max) | M |
| `skillManaCost` | 6.0 | M |
| `skillComboChargeLevel` | **5** (array saturates at 5 from rank 9) | M |
| `skillComboChargeDuration` | 5.0 s (scalar) | M |
| `distanceProfile` | Melee | M |

Combo-charge multipliers live in `gameengine.dbr`:
`skillComboChargeMultipliers = [15, 30, 45, 60, 75, 90, …]` (+15/step) with
`skillComboChargeTime = 0.35 s`. At charge level 5 that is **+75 %**. All inert.

### 1.8 — Tree membership (M) — `_classtree_class10.dbr`

`skillName1` `_classtraining_class10` · `2` `amatokpact1` · `5` `onslaught1` · `22` `werewolf1` ·
`23` `werewolf1b` · `24` `werewolf3` · `26` `…skill01_claws` · `27` `werewolf2` · `28` `…skill02_charge` ·
`38` `passive02` · `39` `passive03`. **All six point-consuming build nodes are distinct tree entries**;
claws and charge are tree entries *and* `grantedSkills` (that is why they mirror the parent's rank
without consuming points — G-7 §4.1).

**Mastery bar `_classtraining_class10.dbr` @ rank 5 (M)** — 100-element arrays, all exactly linear:
`characterLife` +27/rank ⇒ **+135** · `characterMana` +11/rank ⇒ **+55** · `characterStrength`
+4/rank ⇒ **+20** · `characterDexterity` +4/rank ⇒ **+20** · `characterIntelligence` +2/rank ⇒ **+10**.

---

## 2 — ALL equipped items' rolled stats (12 slots, not four)

Join keys are the `.gdc`-measured record paths from G-7 §3.1, carried verbatim.
Per-item `seed` from the save is given because it is the roll key — the same base+affix triple with a
different seed rolls different numbers.

### 2.1 — The roll mechanic, established (M)

**Affix stats are nominal-value + jitter; base-record stats are flat.**

- Every prefix/suffix record is `Class = LootRandomizer` and carries **`lootRandomizerJitter`** (a
  percentage). The listed stat is the **nominal**; the realised roll is drawn about it. Observed
  jitters in this fixture: **0, 20, 25, 28, 30, 35, 40**.
- **Item *base* records carry no jitter field.** Their stats are flat — proven by three exact
  base-to-tooltip hits: chest `defensiveProtection 58` → "58 Armor"; belt `defensiveProtection 7` →
  "7 Armor"; weapon `offensivePhysicalMin/Max 14/40` → "14–40 Physical" and
  `offensiveBasePoisonMin/Max 6/12` → "6–12 Acid". **Four exact, zero drift.**
- **Jitter direction is bidirectional (D, and load-bearing).** Downward-only is falsified: chest
  suffix `b_ar002_ar.characterDefensiveAbility = 12` nominal reads **13** on G-6's f324, and the
  amulet's flat +Health only closes if its prefix rolled **above** nominal 80 (§2.3). I therefore
  report ranges as **nominal × (1 ± jitter/100)**. Graded **D** — the direction is inferred from the
  pinned reads, not stated in source.
- **Damage-type vocabulary (M).** GD renders `offensiveBasePoison*` as **"Acid"** (instant) and
  `offensiveSlowPoison*` as **"Poison"** (DoT). They are two different fields on the same record.

### 2.2 — Per-slot ledger

Ranges shown as `nominal [low – high]`. **M-pin** rows carry G-6's tooltip value in bold.

#### Slot 0 — head · *Sheltering Salvaged Helmet of the Draughul* · seed 71443720

| Part | Record (`.arz` join key) | Stat | Source value | Roll range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearhead/a03_head002.dbr` (`ArmorProtective_Head`, Common, ilvl 12, **Heavy**) | `defensiveProtection` | **76.0** | flat | — | M |
| prefix | `…/lootaffixes/prefix/ad003a_res_cold_01.dbr` (Magical, jitter **30**) | `defensiveCold` | 14.0 | 9.8 – 18.2 | "+% Cold Res" | D-range |
| suffix | `…/lootaffixes/suffix/b_ar014_arje.dbr` (**Rare**, jitter **28**, lvlReq 5) | `characterOffensiveAbility` | 16.0 | 11.5 – 20.5 | "+OA" | D-range |
| | | `characterDefensiveAbility` | 12.0 | 8.6 – 15.4 | "+DA" | D-range |
| | | `characterLifeRegenModifier` | 10.0 | 7.2 – 12.8 | "+% Health Regen" | D-range |
| | | `defensiveProtectionModifier` | 4.0 | 2.9 – 5.1 | — | D-range |

#### Slot 1 — amulet · *Menacing Putrid Necklace of Protection* · seed 1665904519

| Part | Record | Stat | Source value | Roll range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearaccessories/necklaces/b001_necklace.dbr` (`ArmorJewelry_Amulet`, **Rare / MI**, ilvl 8, lvlReq 8, `FileDescription = "Wightmire Slith Boss"`) | `characterLife` | **220.0** | flat | — | M |
| | | `defensivePoison` | **25.0** | flat | — | M |
| | | `offensiveSlowPoisonModifier` | **18.0** | flat | **"+21% Poison Damage"** | C (§2.6a) |
| | | `augmentSkillName1/2` +2 | `playerclass03/bloodofdreeg1`, `playerclass05/elementalinfusion1` | — | — | M (**inert** — Berserker has neither) |
| prefix | `…/prefix/b_ar022_ar.dbr` (**Rare**, jitter **28**, lvlReq 5) | `characterLife` | 80.0 | 57.6 – 102.4 | ⇒ **101** implied | D-range |
| | | `characterDexterity` | 16.0 | 11.5 – 20.5 | **14** | **M-pin** |
| | | `characterOffensiveAbility` | 15.0 | 10.8 – 19.2 | — | D-range |
| | | `defensiveChaos` | 8.0 | 5.8 – 10.2 | — | D-range |
| suffix | `…/suffix/a019b_ch_da_02.dbr` (Magical, jitter **20**) | `characterDefensiveAbility` | 22.0 | 17.6 – 26.4 | — | D-range |

> **The amulet is the boss's own drop.** `b001_necklace.dbr`'s `FileDescription` is *"Wightmire Slith
> Boss"*, and `slith_wightmirecave01.dbr` carries
> `lootMisc2Item1 = records/items/loottables/gearaccessories/tdyn_necklace_b01_slithnecklace.dbr` at
> `chanceToEquipMisc2 = 100 %`. **Matt's greatest kill (§3) dropped the amulet he finished the run
> wearing** — a guaranteed monster-infrequent. Graded **M**, both directions of the join.

#### Slot 2 — torso · *Mystic Salvaged Armor of Menhir's Wall* · seed 770620553

| Part | Record | Stat | Source value | Roll range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/geartorso/a02_torso002.dbr` (Common, ilvl 9, **Heavy**) | `defensiveProtection` | **58.0** | flat | **58 Armor** | **M-pin** |
| prefix | `…/prefix/aa006a_spimod_01.dbr` (Magical, jitter **40**) | `characterIntelligenceModifier` | 5.0 | 3.0 – 7.0 | **+5 % Spirit** | **M-pin** |
| suffix | `…/suffix/b_ar002_ar.dbr` (**Rare**, jitter **28**, lvlReq 5) | `characterLife` | 100.0 | 72.0 – 128.0 | **+76** | **M-pin** |
| | | `characterDefensiveAbility` | 12.0 | 8.6 – 15.4 | **+13** | **M-pin** |
| | | `defensiveBleeding` | 10.0 | 7.2 – 12.8 | "+Bleeding Res" | D-range |
| | | `defensiveProtectionModifier` | 4.0 | 2.9 – 5.1 | — | D-range |

> G-6 also read "(+Physical Res)" on this item. **No `defensivePhysical` field exists on any of its
> three records.** The only percentage-armour term is `defensiveProtectionModifier` (+4 % Armor), which
> GD renders adjacent to resistances. Graded **C**, resolved in the source's favour.

#### Slot 3 — legs · *Glacial Patchwork Leggings of the Fox* · seed 1325224510

| Part | Record | Stat | Source value | Roll range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearlegs/a02_legs01.dbr` (Common, ilvl 9, **Light**) | `defensiveProtection` | **50.0** | flat | "16 Armor" | **C (§2.4)** |
| prefix | `…/prefix/b_ar030_ar.dbr` (**Rare**, jitter **28**, lvlReq 5) | `offensiveColdModifier` | 12.0 | 8.6 – 15.4 | "+Cold" | D-range |
| | | `offensiveSlowColdModifier` | 12.0 | 8.6 – 15.4 | "+Frostburn" | D-range |
| | | `offensiveSlowColdDurationModifier` | 15.0 | 10.8 – 19.2 | — | D-range |
| | | `characterIntelligence` | 12.0 | 8.6 – 15.4 | — | D-range |
| | | `defensiveAether` | 8.0 | 5.8 – 10.2 | — | D-range |
| suffix | `…/suffix/a005b_ch_att_cunspi_02.dbr` (Magical, jitter **30**) | `characterDexterity` | 11.0 | 7.7 – 14.3 | **+8 Cunning** | **M-pin** |
| | | `characterIntelligence` | 11.0 | 7.7 – 14.3 | "+38 Spirit" | **C** — max possible from both records is 29.7 |

#### Slot 4 — feet · *Vigorous Reinforced Greaves* · seed 611621621

| Part | Record | Stat | Source value | Roll range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearfeet/a02_feet02.dbr` (Common, ilvl 9, **Heavy**) | `defensiveProtection` | **52.0** | flat | "12 Armor" | **C (§2.4)** |
| prefix | `…/prefix/aa007a_lifemod_01.dbr` (Magical, jitter **40**) | **`characterLifeModifier`** | **5.0 %** | 3.0 – 7.0 % | **"+75 Health"** | **M-pin — see §2.3d** |

> **This is a percentage, not a flat.** G-6 read it as "+75 Health"; the record says **+5 % Health**.
> That is not a conflict — it is the tooltip rendering the *resolved* value, and it turns out to be the
> single best cross-check in the whole gear set. See §2.3d.

#### Slot 5 — hands · *Stalwart Hide Gloves of Frostbite* · seed 1657793230

| Part | Record | Stat | Source | Range | Grade |
|---|---|---|---|---|---|
| base | `records/items/gearhands/a02_hands01.dbr` (Common, ilvl 7, **Light**) | `defensiveProtection` | **29.0** | flat | M |
| prefix | `…/prefix/aa010a_damod_01.dbr` (Magical, jitter **0**) | `characterDefensiveAbilityModifier` | **4.0 %** | **fixed** | **M** |
| suffix | `…/suffix/a029e_off_dmg%cold_01_ar.dbr` (Magical, jitter **25**) | `offensiveColdModifier` | 7.0 | 5.25 – 8.75 | D-range |
| | | `offensiveSlowColdModifier` | 7.0 | 5.25 – 8.75 | D-range |

*(A zero-jitter affix exists. `aa010a_damod_01` rolls the same 4 % every time — worth knowing before
anyone models all affixes as randomised.)*

#### Slots 6 / 7 — rings · *Vampiric Silver Band* / *Silver Band of Prowess* · seeds 1128683692 / 1728378561

| Slot | Part | Record | Stat | Source | Range | Grade |
|---|---|---|---|---|---|---|
| 6 | base | `records/items/gearaccessories/rings/a001_ring02.dbr` (Common, ilvl 8) | `characterManaRegen` | **0.70/s** | flat | M |
| 6 | prefix | `…/prefix/ao008a_lifeleech_01.dbr` (Magical, jitter **35**) | `offensiveLifeLeechMin` | 5.0 | 3.25 – 6.75 | D-range |
| 7 | base | *(same record `a001_ring02.dbr`)* | `characterManaRegen` | **0.70/s** | flat | M |
| 7 | suffix | `…/suffix/a001a_ch_att_cun_02.dbr` (Magical, jitter **30**) | `characterDexterity` | 13.0 | 9.1 – 16.9 | D-range |

#### Slot 8 — waist · *Mystic Woven Cord of Soulwarding* · seed 1611211945

| Part | Record | Stat | Source | Range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearaccessories/waist/a02_waist001.dbr` (Common, ilvl 8) | `defensiveProtection` | **7.0** | flat | **7 Armor** | **M-pin** |
| prefix | `…/prefix/aa006b_spimod_01.dbr` (Magical, jitter **30**) | `characterIntelligenceModifier` | 8.0 % | 5.6 – 10.4 | **+6 % Spirit** | **M-pin** |
| suffix | `…/suffix/b_ar103_ar_a.dbr` (**GDX1**, **Rare**, jitter **28**, lvlReq 5) | `characterLife` | 80.0 | 57.6 – 102.4 | **+98** | **M-pin** |
| | | `offensivePhysicalModifier` | 12.0 % | 8.6 – 15.4 | **+11 % Physical** | **M-pin** |
| | | `offensiveLifeModifier` | 14.0 % | 10.1 – 17.9 | **+17 % Vitality** | **M-pin** |
| | | `defensiveAether` | 10.0 | 7.2 – 12.8 | — | D-range |
| | | `augmentSkillLevel1` | 2 | 1.4 – 2.6 | — | D-range |

> **Five of six stats on this one item are tooltip-pinned and every one lands inside its jitter
> window.** This is the cleanest single-item validation of the roll model in the set.

#### Slot 9 — shoulders · *Magestorm Fur-lined Mantle of Frostbite* · seed 1527029074

| Part | Record | Stat | Source | Range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearshoulders/a03_shoulder01.dbr` (Common, ilvl 14, **Light**) | `defensiveProtection` | **65.0** | flat | "16 Armor" | **C (§2.4)** |
| prefix | `…/prefix/b_ar104_ar_a.dbr` (**GDX1**, **Rare**, jitter **28**, lvlReq 5) | `offensiveLightningModifier` | 8.0 | 5.8 – 10.2 | **+8 % Lightning** | **M-pin** |
| | | `offensiveAetherModifier` | 8.0 | 5.8 – 10.2 | "+9 % Pierce" | **C** — no Pierce field on any of its records |
| | | `defensiveLife` | 8.0 | 5.8 – 10.2 | **+8 % Vitality Res** | **M-pin** |
| | | `characterOffensiveAbility` | 7.0 | 5.0 – 9.0 | **+8 OA** | **M-pin** |
| suffix | `…/suffix/a029e_off_dmg%cold_01_ar.dbr` (Magical, jitter **25**) | `offensiveColdModifier` | 7.0 | 5.25 – 8.75 | **+8 % Cold** | **M-pin** |
| | | `offensiveSlowColdModifier` | 7.0 | 5.25 – 8.75 | — | D-range |

#### Slots 10 / 11 — medal / relic — **EMPTY** (M). No component or augment on any slot (M).

#### Weapon slot w1-0 — *Poisoned Pusquill's Tail of Corrosion* · seed 809831844

| Part | Record | Stat | Source | Range | Pinned | Grade |
|---|---|---|---|---|---|---|
| base | `records/items/gearweapons/blunt1h/b015b_blunt.dbr` (`WeaponMelee_Mace`, **Rare / MI**, ilvl 12, lvlReq 12, `FileDescription = "Pusquill"`) | `offensivePhysicalMin/Max` | **14.0 / 40.0** | flat | **14–40 Physical** | **M-pin** |
| | | `offensiveBasePoisonMin/Max` | **6.0 / 12.0** | flat | **6–12 Acid** | **M-pin** |
| | | `offensiveSlowPoisonMin` | **6.0**/s | flat | — | M |
| | | `offensiveSlowPoisonDurationMin` | **5.0 s** | flat | **"over 5 Seconds"** | **M-pin** |
| | | `offensiveSlowPoisonModifier` | **20.0 %** | flat | — | M |
| | | `offensiveSlowPoisonDurationModifier` | **50.0 %** | flat | "+64 % Duration" | **C (§2.6b)** |
| | | `characterLife` | **220.0** | flat | **"+242 Health"** | **C (§2.3c)** |
| | | `characterBaseAttackSpeed` | **−0.10** · tag `tagAttackSpeedFast` | flat | **1.78 attacks/s** | M |
| | | `attributeScalePercent` | **8.0** | flat | — | M (only base in the set that has it) |
| | | `augmentSkillName1/2` +3 | `playerclass04/wpattack4`, `playerclass03/curse2` | — | "+3 Nidalla's Hidden Hand / +3 Vulnerability" | M (**inert** for a Berserker) |
| prefix | `…/prefix/ao006b_poison_02.dbr` (Magical, jitter **25**) | **`conversionInType/OutType`** | **Physical → Poison** | — | **"18 % Physical → Acid"** | **M-pin** |
| | | `conversionPercentage` | 15.0 | **11.25 – 18.75** | **18** | **M-pin** |
| | | `offensiveSlowPoisonMin` | 3.0/s | 2.25 – 3.75 | — | D-range |
| | | `offensiveSlowPoisonDurationMin` | 5.0 s | 3.75 – 6.25 | — | D-range |
| suffix | `…/suffix/a032c_off_dmg%acid_01_we.dbr` (Magical, jitter **20**) | `offensivePoisonModifier` | 16.0 | 12.8 – 19.2 | **+18 % Acid** | **M-pin** |
| | | `offensiveSlowPoisonModifier` | 16.0 | 12.8 – 19.2 | ⇒ 18 | **M-pin** |

> **The weapon's "+38 % Poison Damage" decomposes exactly (D, one step):**
> base `offensiveSlowPoisonModifier 20` (flat) **+** suffix roll **18** (nominal 16, jitter 20 %,
> and the *same* roll that produced the tooltip's "+18 % Acid" from the co-located
> `offensivePoisonModifier 16`) **= 38**. Both suffix stats share one roll factor of 1.125. This is
> **direct evidence that a LootRandomizer applies ONE roll across all its stats** — which in turn is
> why the chest suffix's 0.76-vs-1.083 split (§2.6c) is worth flagging rather than smoothing.

#### Off-hand slot w1-1 — *Bernard's Slightly-Chewed Buckler of Protection* · seed 642633620

| Part | Record | Stat | Source | Range | Grade |
|---|---|---|---|---|---|
| base | `records/items/gearweapons/shields/b013a_shield.dbr` (`WeaponArmor_Shield`, **Rare**, ilvl 6, lvlReq 6) | `defensiveBlock` | **65.0** | flat | M |
| | | `defensiveBlockChance` | **18.0 %** | flat | M |
| | | `blockAbsorption` | **100.0 %** | flat | M |
| | | `blockRecoveryTime` | **0.5 s** | flat | M |
| | | `offensivePhysicalMin` | **34.0** | flat | M |
| | | `offensivePhysicalModifier` / `offensiveSlowPhysicalModifier` | **8.0 %** each | flat | M |
| | | `defensivePoison` | **15.0** | flat | M |
| suffix | `…/suffix/a019a_ch_da_01.dbr` (Magical, jitter **30**) | `characterDefensiveAbility` | 7.0 | 4.9 – 9.1 | D-range |

**The shield is a damage source.** `offensivePhysicalMin = 34` is what charge's `weaponDamagePct` acts
on for its off-hand line (§1.3), and `blockAbsorption = 100 %` with `defensiveBlockChance = 18 %` and
`defensiveBlock = 65` is an unmodelled mitigation channel — 18 % of incoming hits absorb up to 65
damage **in full**. Against a trash hit of 33–49 (G-5a §4) that is a **complete negation** on ~1 hit in
5.5. Not in the G-4 kit spec. Flagged for gandalf.

### 2.3 — The +737 flat-Health cross-check: **PASS**, and the step closes further

#### 2.3a — Every `characterLife` source in the equipped set (M — exhaustive sweep of all 12 slots)

| Slot | Record carrying it | Nominal | Jitter | Roll range | G-6 pinned |
|---|---|---|---|---|---|
| weapon | `…/blunt1h/b015b_blunt.dbr` (**base**) | 220.0 | **none (flat)** | 220 | **242** |
| amulet | `…/necklaces/b001_necklace.dbr` (**base**) | 220.0 | **none (flat)** | 220 | — |
| amulet | `…/prefix/b_ar022_ar.dbr` | 80.0 | 28 % | 57.6 – 102.4 | — |
| amulet | *(base + prefix, as displayed)* | 300.0 | — | 277.6 – 322.4 | **321** ✓ |
| torso | `…/suffix/b_ar002_ar.dbr` | 100.0 | 28 % | 72.0 – 128.0 | **76** ✓ |
| waist | `…/suffix/b_ar103_ar_a.dbr` (GDX1) | 80.0 | 28 % | 57.6 – 102.4 | **98** ✓ |
| **four attested items, flat total** | | **700.0** | | **627.2 – 772.8** | **737** ✓ |
| feet | `…/prefix/aa007a_lifemod_01.dbr` | **5.0 %** (multiplicative) | 40 % | 3.0 – 7.0 % | **"+75"** — §2.3d |

**No other equipped record carries `characterLife` or `characterLifeModifier`.** Sweep was exhaustive
across base + prefix + suffix of all 12 slots.

#### 2.3b — Verdict

**PASS.** G-6's tooltip-pinned **+737** sits at the **52nd percentile** of the source's roll window
[627.2, 772.8] around a nominal 700. Three of the four items reconcile *individually* inside their own
jitter windows — amulet (implied prefix roll 101 ∈ [57.6, 102.4]), torso (76 ∈ [72, 128]), waist
(98 ∈ [57.6, 102.4]). **The `.arz` roll model and the running client's tooltips agree.**

Against the T-A measured step 759 → 1600 = **+841**:

| Reading | Flat +Health | % of the +841 step |
|---|---|---|
| Source nominal (roll-agnostic) | 700 | 83.2 % |
| **G-6 tooltip-pinned** | **737** | **87.6 %** (reproduces G-6 F-G6-9 exactly) |
| Weapon read at source-flat 220 instead of 242 | 715 | 85.0 % |

All three leave G-6's conclusion — *the gear step is four flat `+Health` affixes, not a fitted
parameter* — **intact**. `ehp_multiplier` need not enter G-5 as a free parameter.

#### 2.3c — The one residual: the weapon's 220 vs 242

The weapon's `+Health` sits on a **base** field with **no jitter mechanism** — `characterLife = 220.0`
flat — yet G-6 read **242** (= 220 × **1.100**, exactly). Two readings, and I decline to choose:

1. **A base-record scale exists.** `b015b_blunt.dbr` is the **only** base in the equipped set carrying
   **`attributeScalePercent = 8.0`**. It is the named candidate — but it **does not close
   arithmetically**: 220 × 1.08 = **237.6**, not 242. And the *same record's* damage fields
   (`offensivePhysicalMin/Max`, `offensiveBasePoisonMin/Max`) were pinned **exactly** unscaled, so any
   scale would have to apply to `character*` attributes only.
2. **The pixel read is off by one glyph** (`220` → `242`).

Residual **+22**, i.e. **2.6 % of the +841 step**. Graded **U** — flagged, not smoothed. It does not
move any conclusion in this note.

#### 2.3d — The boots close a further ~76, and cross-validate the 1600 endpoint

`aa007a_lifemod_01` is **`characterLifeModifier = 5.0`** — a **percentage**. G-6 rendered it as
"+75 Health" because GD tooltips print the resolved figure. Run it backwards:

```
end-of-run max HP (T-A)              = 1600
pool the +5 % applies to             = 1600 / 1.05 = 1523.8
5 % of that                          = 76.2      →  tooltip prints 75–76
G-6 read                             = 75
```

**Exact to the unit.** This is a *two-way* confirmation: it fixes the boots' roll at nominal 5 %
(not 3 or 7), **and it independently corroborates the T-A max-HP endpoint of ~1600 from an item
tooltip** — an instrument with no shared failure mode with the panel OCR.

Re-itemising the step with the multiplicative term included:

| Term | Value | Running total |
|---|---|---|
| pre-step max HP (T-A) | 759 | 759 |
| four flat `+Health` affixes (§2.3a) | +737 | 1496 |
| boots `characterLifeModifier` +5 % | ×1.05 | **1571** |
| **measured post-step (T-A)** | | **1600** |
| **unexplained residual** | | **29 — 3.4 % of the step** |

**The gear step now closes to ≈ 96.6 %**, up from G-6's 87.6 %. The residual 29 is comfortably
level-ups 11→13 (mastery `characterLife` +27/rank, §1.8) plus attribute points. Graded **D** (the
composition order — flat-then-percentage — is the standard TQ/GD stacking and is not stated in source;
the alternative order gives 1533 and a residual of 67, still ≤ 8 %).

### 2.4 — Armor ledger (M) — and a conflict with three of G-6's non-attested reads

| Slot | Record | `defensiveProtection` | Class | G-6 read |
|---|---|---|---|---|
| head | `a03_head002.dbr` | **76** | Heavy | *(not read)* |
| torso | `a02_torso002.dbr` | **58** | Heavy | **58** ✓ |
| shoulders | `a03_shoulder01.dbr` | **65** | Light | 16 ✗ |
| legs | `a02_legs01.dbr` | **50** | Light | 16 ✗ |
| feet | `a02_feet02.dbr` | **52** | Heavy | 12 ✗ |
| hands | `a02_hands01.dbr` | **29** | Light | *(not read)* |
| waist | `a02_waist001.dbr` | **7** | — | **7** ✓ |
| **base total** | | **337** | | |
| head suffix + torso suffix `defensiveProtectionModifier` | | **+4 % + 4 %** | | |
| **× 1.08** | | **364** | | |
| Amatok's Pact `defensiveProtection` (§1.6) | | **+16** | | |
| **total armour, end of run** | | **≈ 380** | | |

> **CONTESTED, and the source is the stronger instrument here.** The two slots G-6 pinned exactly —
> torso 58 and waist 7 — are the two on Matt's *attested* list, i.e. the two G-6 read at 4–5×
> magnification. The three that disagree (shoulders, legs, feet) are all from G-6's lower-confidence
> secondary rows. Two independent same-record hits at 100 % accuracy alongside three misses on a
> different confidence tier is a **read-quality** pattern, not a data pattern. I record the source
> values as **M** and G-6's three as **C**.
>
> Consequence for G-4 §1.8 / `mitigation_delta`: the armour term is **337 base → ~380 resolved**, not
> "109+ read". That is **3.5×** G-6's figure, and with `gameengine.armorDefensiveAbsorption = 70 %` it
> is a materially different mitigation model. **This should be re-read on the pixels before G-5 pins
> anything to it** — a single 4× crop of the shoulder tooltip settles it. → **REQUEST to galadriel.**

### 2.5 — The kit's realised damage channels, from source (M unless noted)

| Channel | Magnitude | Origin (`.arz`) |
|---|---|---|
| **Chaos** (was Pierce) | claws **237** flat · charge **375** flat | `…claws/charge.offensivePierceMin[16]`, retyped 100 % by `werewolf1b.dbr` |
| **Physical** | weapon **14–40**, × `weaponDamagePct` (150 % claws / 295 % charge), −18 % converted | `b015b_blunt.offensivePhysicalMin/Max` |
| **Acid** | weapon **6–12** + 18 % of Physical | `b015b_blunt.offensiveBasePoisonMin/Max`; `ao006b_poison_02` conversion |
| **Poison (DoT)** | base **6/s** + prefix roll ~**3–4/s** over **5 s** ⇒ tooltip "50 over 5 s"; ×(20 % + 18 % + amulet 18 %) | `b015b_blunt.offensiveSlowPoison*`, `ao006b_poison_02`, `a032c…`, `b001_necklace` |
| **Bleed (DoT)** | charge **270/s × 3 s = 810** | `…charge.offensiveSlowBleedingMin[16]` |
| **Cold** | Amatok aura **5–6** → ~**9–11** resolved (§1.6) | `amatokpact1_buff.offensiveColdMin/Max[1]` |
| *Cold (Onslaught)* | *83 flat — **INERT**, never fired* | `onslaught1.offensiveColdMin[13]` |
| **Physical (off-hand)** | shield **34** flat × `weaponDamagePct` | `b013a_shield.offensivePhysicalMin` |

**Two static conversions, both now source-confirmed:** 100 % Pierce→Chaos (`werewolf1b`, §1.4) and
15 % nominal / **18 % rolled** Physical→Acid (`ao006b_poison_02`, §2.2). Charter §14.6 ruled the first
compiles statically into the kit spec as retyped damage; **the second takes the identical treatment**
(G-6 REQUEST 3, answered).

**Attack cadence.** `characterBaseAttackSpeed = −0.10` with `characterBaseAttackSpeedTag =
tagAttackSpeedFast` against G-6's tooltip **1.78 attacks/sec**. As G-5a §6.2 recorded, GD's base
attack interval in seconds lives in the `.anm` tables, which this lane does not parse — so **1.78 aps
is a MEASURED value with no source derivation**, and it is the only cadence input G-5 has. Graded
**M-pin** (value) + **U** (derivation).

### 2.6 — Named residuals in the gear layer

| # | Item | Source | G-6 pinned | Status |
|---|---|---|---|---|
| a | Amulet `offensiveSlowPoisonModifier` | **18** (flat base field) | "+21 %" | **U** — a flat base field cannot roll. Off by 3. |
| b | Weapon `offensiveSlowPoisonDurationModifier` | **50** (flat) + no other duration-% source in the set | "+64 %" | **U** — off by 14; no candidate field found |
| c | Torso suffix intra-affix roll consistency | life 76/100 = **0.76**, DA 13/12 = **1.083** | both pinned | **U** — the weapon suffix (§2.2) proves one roll per affix; this one implies two |
| d | Weapon `characterLife` | **220** flat | **242** | **U** — §2.3c |
| e | Legs suffix `characterIntelligence` | 11 + 12 nominal, max window **29.7** | "+38 Spirit" | **C** — outside the window; read quality |
| f | Shoulders prefix "+9 % Pierce" | no Pierce field on any of its 3 records | "+9 % Pierce" | **C** — likely the `offensiveAetherModifier 8` line |

None of (a)–(f) moves a conclusion. All six are recorded so the next pass does not rediscover them.

---

## 3 — The boss fixture: `tagSlithBossB02` resolved, and the chain tested against a live number

### 3.1 — Identity and the resolution chain (M)

| Datum | Value | Source |
|---|---|---|
| Save tag | `tagSlithBossB02` → **"Primordian, the Forgotten One"** | `resources/Text_EN.arc` |
| **`.arz` record** | **`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr`** (`Monster`, `database/database.arz`) | uniqueness verified — a full-corpus sweep of all `Monster` records found **exactly one** with `description = tagSlithBossB02` |
| `FileDescription` | *"Primorian the Forgotten One"* (dev spelling) | M |
| `monsterClassification` | **Quest** | M |
| `charLevel` remap | **`charLevel*1+3`** | M |
| Spawn proxy | `records/proxies/boss&quest/proxy_wightmire_slitha01.dbr` → pool `…/boss&questpools/p_wightmire_slitha01.dbr` | M (found by full-corpus reverse reference sweep) |
| Pool | `spawnMin = spawnMax = 3`, `alwaysSpawn1/2/3 = True`, `limit1/2/3 = 1` — the boss **plus two named escorts** (`slitha_melee_b01`, `slitha_shaman_c01`) | M |
| `levelVarianceEquation1` | **`records/proxies/lv6_hero.dbr`** | M |
| `characterAttributeEquations` | `records/creatures/enemies/bios/bio_boss_standard_01.dbr` | M |
| `controller` | `records/controllers/enemy/controller_boss_viloth.dbr` | M |
| `numAttackSlots` / `numDefenseSlots` | **8 / 8** (vs 4/4 for trash) | M |
| `experiencePoints` | 800 | M |
| `perPartyMemberDropItemName` | `records/items/questitems/quest_slithnecklace.dbr` | M |
| **`lootMisc2Item1` @ 100 %** | `…/tdyn_necklace_b01_slithnecklace.dbr` → **the equipped amulet** (§2.2) | M |

**Save-side (M, and a correction to G-7 §6.1):**
`play_stats.perDifficulty[0].greatestMonsterKilledLevel = 13` and
`…greatestMonsterKilledLifeAndMana = 15822`. These are the **monster's** level and the **monster's**
life+mana — not the player's. G-7 §6.1 tabulated the 13 as "Level at kill", which reads as the player
level; it is the boss's. The distinction matters for everything below.

**The charLevel is independently triangulated at 13 (D, three-way):**

```
player level ≈ 8   (G-6 dated series: level 8 at play_time 3619, mid-R2)
  → lv6_hero:  min (aPL+2)+(aPL/50) = 10.16 → 10 ;  max (aPL+3)+(aPL/50) = 11.16 → 11
  → spawn 10–11
  → charLevel*1+3  =  13–14
save records monster level                          =  13   ✓
```

The player-level series, the level-variance equation, the `+3` remap and the save's own field all
agree on **13**. This is not assumed; it is over-determined.

### 3.2 — The 15,822 test: the chain **MISSES by 22 %**, and the miss is exactly 15 points of life modifier

This is the first time any figure from the G-5a resolution chain has been put against a number
produced by the running client. G-5a §6 asked for precisely this test and named it the thing to
validate first.

**Chain inputs at charLevel 13 (all M):**

| Term | Value | Record |
|---|---|---|
| `characterLife` equation | `((charLevel*51)^1.53)+2400` ⇒ **23,145.11** | `bio_boss_standard_01.dbr` |
| `characterMana` equation | `((charLevel*15)^1.27)+200` ⇒ **1,009.74** | `bio_boss_standard_01.dbr` |
| skill `characterLifeModifier` | **−71 %** (`armorbase05` @ rank `charLevel*1` = 13; the array is −71 flat for ranks 1–19) | `…/passive/armorbase05.dbr` |
| pak `characterLifeModifier` (Normal / 1P, index 0) | **+50 %** | `balancingadjustment_mp+difficulty_enemies01.dbr` |
| pak `characterLifeMultModifier` | **0 %** | same |
| pak `characterManaModifier` | **0 %** | same |

**Exhaustive check for other life sources (M):** the monster record's own `characterLife` is `0.0`;
none of its ten `skillNameN` records carries a `characterLifeModifier` other than `armorbase05`;
its `defaultChestPiece` (`gear_slithwarriorb01.dbr`) carries **no stats at all**. There is nothing else.

**Result:**

| Composition | Predicted life + mana | vs measured 15,822 |
|---|---|---|
| G-5a as stated — additive pool `−71 + 50 = −21` ⇒ ×0.79 | **19,294** | **+21.95 %** |
| Fully multiplicative — `×0.29 × 1.50` ⇒ ×0.435 | 11,078 | −30.0 % |
| **MEASURED (client)** | **15,822** | — |

**The two candidate operators bracket the truth without containing it.** G-5a §1f adjudicated
additive-vs-multiplicative *by contradiction* on the damage side and carried the same operator to
life. The live number says life is neither.

#### The residual is an exact integer, and only at charLevel 13

Solving for the net additive life-modifier pool that reproduces 15,822, across charLevels:

| charLevel | bio life | bio mana | chain (−21 %) | **required net life modifier** |
|---|---|---|---|---|
| 10 | 16,286 | 780 | 13,646 | −7.64 % |
| 11 | 18,466 | 855 | 15,443 | −18.95 % |
| 12 | 20,754 | 931 | 17,327 | −28.25 % |
| **13** | **23,145** | **1,010** | **19,294** | **−36.00 %** |
| 14 | 25,636 | 1,090 | 21,342 | −42.53 % |
| 15 | 28,223 | 1,171 | 23,467 | −48.09 % |

**Only charLevel 13 yields a whole number** — −36.0026 %, i.e. **−36 % to four significant figures**.
`23,145.11 × 0.64 + 1,009.74 = 15,822.6` → the client's int is **15,822**. Exact.

Two further consistency checks pick the same interpretation:

| Interpretation of the save field | Required modifier | Integer? |
|---|---|---|
| **life+mana, mana UNMODIFIED** | **−36.0026 %** | **✓** |
| life only (field is not life+mana) | −31.6400 % | ✗ |
| life+mana, both modified | −34.4976 % | ✗ |

Three independent cleanliness tests — charLevel, field semantics, and the modifier's integrality — all
select the same reading. **This is not curve-fitting to one datum; it is one datum selecting a unique
integer solution out of a two-dimensional grid.**

#### What is wrong

```
armorbase05  −71   (MEASURED, not in dispute)
pak          +50   (MEASURED field value, Normal/1P index 0 — index semantics proven in G-5a §1e)
             ————
chain net    −21           required net  −36           discrepancy  exactly 15 points
```

Two readings of the 15 points, and I decline to choose between them on one datum:

1. **The pak's `characterLifeModifier` does not enter the additive pool at its face value of +50.**
   The value that fits is **+35**. (Noted without weight: `+35` and `−15` both appear verbatim in the
   same pak column — `characterDefensiveAbility = 35`, `characterDefensiveAbilityModifier = −15` —
   and `50 × 0.70 = 35` while `gameengine.armorDefensiveAbsorption = 70`. These are *coincidences
   until a second datum says otherwise*, and I am recording them only so the next investigator has
   the shortlist.)
2. **There is a global −15 % monster life modifier the corpus sweep did not reach.** No such record
   was found in `records/game/` or in this monster's skill chain; the sweep is exhaustive for *this*
   creature but not for engine-level constants outside `.arz`.

#### Consequence — **every HP figure in the G-5a ledger is high**

The correction is a pure function of the creature's `armorbase` tier, so it is applyable without
re-resolving anything:

| Tier | `armorbase` lifeMod | chain ×(1+Σ+50) | pinned ×(1+Σ+35) | **G-5a HP is high by** |
|---|---|---|---|---|
| Trash (`armorbase01/02`) | −58 | 0.920 | 0.770 | **×0.837 ⇒ −16.3 %** |
| Champion / hero / boss (`armorbase03–06`) | −71 | 0.790 | 0.640 | **×0.810 ⇒ −19.0 %** |
| Hero with `passiveproperties_herodeflection` | −61 | 0.890 | 0.740 | ×0.832 ⇒ −16.9 % |

E.g. `zombie_a01` @12: G-5a **181** → **151**. Warden Krieg ph.1 @18: G-5a **26,155** → **21,190**;
ph.2 **35,198** → **28,516**; the two-phase total **61,353** → **49,706**.

> **Ruling I am making, within seam:** G-5a's HP composition is **not validated** and should be
> carried as **DERIVED-CONTESTED** until a second live datum lands. G-5a §6's own hedge — *"Not
> independently validated against a running client"* — is now discharged, and it discharged against
> the rule. Every G-5a §2 HP figure and every §4 ratio built on them (HP/759, HP/1600, TTK spans)
> shifts ~16–19 % lower. The *damage* side is untouched by this finding.
>
> **What would close it:** a second `greatestMonsterKilledLifeAndMana` from any other GD save — one
> more (creature, level, life+mana) triple discriminates hypothesis 1 from hypothesis 2 immediately,
> because a global −15 % predicts the same offset everywhere while a pak-value error predicts an
> offset that scales with the pak column. **This is a one-file ask and it is worth making.**

### 3.3 — Primordian, the Forgotten One — full stat block at charLevel 13, Normal / 1 player

Both HP columns given: **chain** = G-5a's rule as published; **pinned** = the −36 % rule that
reproduces the client. Everything else is unaffected by the dispute.

| Property | Value | Grade |
|---|---|---|
| charLevel | **13** | M (triangulated, §3.1) |
| **Life** | chain 18,285 · **pinned 14,813** | D |
| **Mana** | **1,010** | D |
| **Life + Mana** | chain 19,294 · **pinned 15,823 vs MEASURED 15,822** | **D, ±1** |
| Armor (`armorbase05` @13) | **76** | D |
| Offensive Ability | **423** | D |
| Defensive Ability | **387** | D |
| Strength / Dexterity / Intelligence | 128 / 154 / 154 (pre-pak −5 %) | D |
| `tdmMult` | **0.225** (`armorbase05` −78 @13, `damage_totaladjuster` +8 @2, pak −25 %) | D |
| Base attack (`damagebase_physical04` @13) | **101 – 128 Physical** before `tdmMult` ⇒ **≈ 23 – 29** after | D |
| `primordian_passive` cold (@4) | **16 – 38 Cold** before `tdmMult` ⇒ **≈ 4 – 9** after | D |
| Attack speed / run speed (after pak −10 % / −18 %) | **0.90 / 0.70** | D |
| Resistances (own record) | **Cold 35 · Poison 25 · Freeze 500 · Knockdown 500** | **M** |
| + `resists_heroboss` @3 | Stun 75 · Petrify 75 · Sleep 60 · Freeze 60 · Trap 50 · ManaBurn 500 · Confusion/Convert/Disruption/Fear 500 · %CurrentLife 88 · Reflect 40 · TotalSpeed 35 · LifeLeech 18 | **M** |
| `distressCall` | True, group **Slith**, range 15 m, 5,000 ms, max 1 | M |
| `healthGainOnKillPct` | 20 | M |

**Cold-heavy, and the Berserker had no Cold resistance from gear.** The boss's own Cold 35 / Poison 25
sit directly against the fixture's Acid/Poison weapon — a **25 % Poison resist against the kit's DoT
channel**, and **0 % Chaos resist against the kit's entire 237/375 flat channel** (§2.5). Primordian
is, in resistance terms, an unusually favourable matchup for this exact build.

**Burst abilities (D — flat damage × `tdmMult` 0.225; the `magicalDamageEquation` Intelligence term is
NOT applied, consistent with G-5a's treatment, so Cold figures are floors):**

| Ability | Class | Rank | Raw | After `tdmMult` | Shape |
|---|---|---|---|---|---|
| `primordian_wave.dbr` | `Skill_AttackWave` | 4 | 122 Phys + 210 Cold + 70/s Cold-DoT 3 s + 30 % damage-taken 3 s | **27.4 + 47.2**, DoT **15.8/s** | cone: `waveDistance 16`, start 3 m → end 6 m, `waveTime 1.4 s`; `specialAttackChance 100`, delay 5 s, timeout 5 s |
| `primordian_frigidring.dbr` | `Skill_AttackProjectileRing` | 4 | 118 Phys + 200 Cold + 60/s Cold-DoT 2 s + Freeze 1.3–1.8 s | **26.6 + 45.0**, DoT **13.5/s** | **16 projectiles @ 360°**, `projectileUsesAllDamage`, range-scaled 50 %/100 %/140 % by distance band; `specialAttack2Chance 80`, delay 6 s |
| `chillbane_blizzard.dbr` | `Skill_BuffAttackRadiusDrop` | 4 | 111 Cold + 58 Phys + 30 % slow 5 s | **25.0 + 13.1** | **6 drops** from 20 m over an 8 m radius, `skillTargetInterval 2 s`, `skillActiveDuration 8 s`; `specialAttack3Chance 100`, LongRange, delay 10 s |
| `primordian_icearmor.dbr` | `Skill_BuffSelfDuration` | 4 | — | — | **`damageAbsorptionPercent 25`**, `characterAttackSpeedModifier +35 %`, `offensiveColdModifier +26 %`, retaliation 32/s Cold 2 s; **12 s active / 32 s cooldown**, `instantCast`; also the record's `buffSelfSkillName` (cast on spawn) |
| `boss_chest_01.dbr` | `Skill_OnDeathSpawnActor` | 1 | — | — | boss loot chest on death |

> **A 25 % damage-absorption window on a 12-s-up / 32-s-cycle** is a hard phase structure the fixture's
> sim has no representation for: **37.5 % of the fight duration the boss takes 25 % less of everything
> and swings 35 % faster.** With three special attacks all at 80–100 % chance on 5/6/10-s delays, this
> is a genuinely patterned encounter, not a stat block. Flagged for gamora.

### 3.4 — Mid-tier scenario at player level 13 (champion + hero)

Spawn levels re-derived at `averagePlayerLevel = 13` (G-5a §1a equations), then each record's own
remap applied:

| | Champion | Hero |
|---|---|---|
| Name | **Fleshwarped Butcher** | **Abner, the Forsaken One** |
| Record | `records/creatures/enemies/zombiemutated_a01.dbr` | `records/creatures/enemies/hero/zombie_h01.dbr` |
| `monsterClassification` | Champion | Hero |
| Variance eq @ pL13 | `lv4_champion` ⇒ spawn **14** | `lv6_hero` ⇒ spawn **15 – 16** |
| `charLevel` remap | `charLevel*1+1` ⇒ **15** | `charLevel*1+5` ⇒ **20 – 21** |
| bio | `bio_zombiemutated_01.dbr` | `bio_hero_bruiser_01.dbr` |
| skill lifeMod | −71 (`armorbase03`) | −66 @20 / −61 @21 (`armorbase03` + `passiveproperties_herodeflection`) |
| **Life — chain** | 1,008 | 6,712 – 7,652 |
| **Life — pinned (−36 %)** | **817** | **5,513 – 6,362** |
| Mana | 238 | 1,599 – 1,689 |
| Armor | 27 | 40 – 45 |
| OA / DA | 433 / 367 | 545 / 485 → 565 / 503 |
| `tdmMult` | 0.180 | 0.247 – 0.255 |
| Base attack after `tdmMult` | **≈ 17 – 18 Phys** + 4 Aether (`damagebase_physical01` @15 — *a champion on the **trash** damage table*) | **≈ 21 – 29 Phys** + 9.7/s Poison-DoT 6 s (`damagebonus_physical02` @21) |
| Attack / run speed | 1.17 / 1.03 | 1.26 / **1.31** |
| Resistances | Fire 15 · Stun 50 · Knockdown 500 | **Physical 40** · Pierce 26 · Poison 15 · Knockdown 400 |
| Named skills | `aetherrage1_zombiemutant` (charged linear) @4 · `passiveproperties_zombiemutated` @4 | `pulvarion_poisoncloud` @6 · `theforsaken_plaguetouch` @6 · `theforsaken_overflowingrage` (`Skill_BuffSelfColossus`) @1 · `diseased_diseasecloud` @6 · `nightbuff_generic01` @6 · `hero_chest_all_01` |

> **Two things a harness should not miss.** (1) The champion is on `damagebase_physical01` — the
> *trash* damage table — and lands **below** trash damage after its own `armorbase03` damper. G-5a §4's
> headline (tier is expressed as HP, not hit size) holds and is sharper than it looked. (2) **Abner has
> Physical 40 / Pierce 26.** Against this fixture that is nearly irrelevant, because Blight of Ch'thon
> retyped the kit's whole flat channel to **Chaos**, against which Abner has **0**. The transmuter is
> worth more against this hero than against anything else in the ledger.

---

## 4 — G-6's three out-of-seam requests, answered

**REQUEST 1 — records for Battle Surge and the reserved cold aura.** Both found (§1.5, §1.6):
`records/skills/playerclass10/passive02.dbr` (**Battle Surge**, `Skill_PassiveOnCritBuffSelf`) and
`records/skills/playerclass10/amatokpact1.dbr` → `amatokpact1_buff.dbr` (**Amatok's Pact**,
`Skill_BuffRadiusToggled` → `SkillBuff_Passive`). **All ten tooltip values reproduce exactly from
source.** Both are already in the G-7 save ledger at rank 1 — so the pixels, the save bytes and the
`.arz` now agree three ways on both nodes.

**REQUEST 2 — which `playerclass10` records carry 12 base ranks, and which is a `Skill_Modifier`?**
Twenty-one records carry `skillMaxLevel = 12`. The discriminator G-6 needed is a **one-bit field**:

| Node | Record | `roundBitmap` | UI shape |
|---|---|---|---|
| **Battle Surge** | `passive02.dbr` | **1** | **circle** |
| *(Blood of the Berserker)* | `passive03.dbr` | 1 | circle |
| **Amatok's Pact** | `amatokpact1.dbr` / `_buff` | *absent* | **square** |
| all other 12-rank records incl. `werewolf2`, `werewolf3`, `onslaught2/3`, `passive04`, `rallyingcry2`, `wereraven2/3` | — | *absent* | square |

**Only `passive02` and `passive03` carry `roundBitmap` in the entire mastery.** Since `passive03`
is measured-absent from the save (G-7 §4), the circle 1/12 node **is** Battle Surge and the square
1/12 node **is** Amatok's Pact. **This agrees with G-6's hover cue at f352**, which is why G-6's
UNCERTAIN row (a) can be closed rather than merely arbitrated: two instruments, one conclusion.

Corollary G-6 asked for: **`werewolf2` and `werewolf3` are both `Skill_Modifier` with
`skillMaxLevel = 12`** — i.e. exactly the shape of the two 1/12 nodes — and **neither appears in the
save's skill list at all**. Their absence is confirmed from the source side, closing G-4 §7.3's largest
sensitivity for the third time.

**REQUEST 3 — the weapon's 18 % Physical→Acid.** `records/items/lootaffixes/prefix/ao006b_poison_02.dbr`,
`conversionInType Physical` → `conversionOutType Poison`, `conversionPercentage 15.0` nominal with
`lootRandomizerJitter 25` ⇒ window **[11.25, 18.75]**; G-6's pinned **18 %** lands inside it.
**Structurally identical to `werewolf1b`'s transmuter** (`conversionInType/OutType/Percentage` on the
same three fields), so **charter §14.6's static-compile ruling applies unchanged**: it compiles into
the kit spec as retyped damage, not as a runtime step. Note the vocabulary trap: the `.dbr` type is
`Poison`; GD renders instant `offensiveBasePoison` as **"Acid"** and the `offensiveSlowPoison` DoT as
**"Poison"** (§2.1) — one conversion feeds both display names.

---

## 5 — Unresolved / carried

| # | Item | Status | What would close it |
|---|---|---|---|
| **U1-1** | **The 15-point life-modifier discrepancy (§3.2)** | **UNRESOLVED — highest value on this list.** Pinned to a unique integer solution from one live datum; the *mechanism* is not identified | **One more `greatestMonsterKilledLifeAndMana` triple from any other GD `.gdc`.** Discriminates "pak value" from "global −15 %" immediately |
| U1-2 | `skillManaCost` on `Skill_Shapeshift`: activation cost or standing reserve? (§1.1) | UNRESOLVED — semantics not in source | A transform tooltip frame, or a character-sheet energy read while transformed |
| U1-3 | The transform tooltip's parenthetical damage bands — "150% Main Hand Damage **(69 – 85)**", "295% Off-Hand **(177 – 181)**" | UNRESOLVED — do not decompose from weapon 14–40 / shield 34 under any composition I tried; the narrow ratios suggest they are not min/max of one channel | GD tooltip-composition source, or one frame at a known gear state |
| U1-4 | Weapon `characterLife` 220 (source, flat) vs 242 (pixels) — `attributeScalePercent = 8` named but gives 237.6 (§2.3c) | UNRESOLVED; residual 2.6 % of the gear step | A 4× re-crop of f323's Health line |
| U1-5 | Armour: source 337 base / ≈380 resolved vs G-6's "109+ read" — three secondary slots disagree (§2.4) | **CONTESTED** — source is the stronger instrument, but this is 3.5× and `mitigation_delta` rides on it | **REQUEST to galadriel:** one 4× crop each of the shoulder / legs / boots Armor lines |
| U1-6 | Amulet "+21 %" vs flat 18; weapon duration "+64 %" vs flat 50; torso suffix's two-roll behaviour (§2.6a–c) | UNRESOLVED — small, named | Re-crops; or a second save with the same affixes at a different seed |
| U1-7 | Whether the elemental `magicalDamageEquation` Intelligence term applies to *monster* cold damage | UNRESOLVED — Cold figures in §3.3 are floors | Not worth closing before U1-1 |
| U1-8 | Onslaught's 83 flat Cold and 158 % weapon damage at rank 13 | **INERT by ruling** (charter §13) — extracted, must not enter any damage model | — |

**Carried unchanged from G-5a:** the damage-side composition operator (§1f, inferred by contradiction),
skill-level truncation, weapon-wielder base damage, attack cadence in seconds, Veteran mode. **None of
those is touched by this note** — U1-1 is a *life*-side finding only.

---

## 6 — Artifacts

`agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-u1/`:

| File | Role |
|---|---|
| `u1_lib.py` | multi-archive `.arz` resolver with expansion-override precedence (gdx3 > gdx2 > gdx1 > base) + **rank-array indexer** (`at()`, `nonzero()`), wrapping the G-7 `arz_index.Arz` low-level reader. Nothing rebuilt. |
| `u1_gear.py` / `gear_stats.json` | all-12-slot base/prefix/suffix stat extraction with `lootRandomizerJitter` roll windows, driven off G-7's `gear_resolved.json` |
| `u1_boss.py` | **G-5a five-record chain, implemented** — bio equations, rank-indexed passives, the Normal/1P pak, OA/DA from `combatformulas`. Reproduces G-5a's Warden ph.1 (26,155 HP / 106 armor / OA 523) and `zombie_a01` (181 HP) — i.e. it is faithful to the published rule, which is what makes §3.2's miss a finding about the rule and not about the tool. |

**Upstream reused, not re-derived:** `legolas/scratch/2026-07-28-gdc-parse-g7/{arz_index.py,
gear_resolved.json, parsed.json}` · `research/scripts/gd_arz_adapter_2026_07_24.py`.

---

*Downstream: **gandalf** (RUN-CONDUCTOR — §3.2 is a ruling-grade finding and §2.3d moves the gear-step
closure to ≈96 %); **gamora** (§3.3 phase structure, §1.5 sustain channel, §2.2 shield block);
**galadriel** (U1-5 re-crop request); **elrond** if any of this is curated. No canonical doc amended
by this note.*

**Signed:** legolas (UNKNOWN-RESEARCHER), 2026-07-28.





