# C-11b — the LINEAGE of a Crucible body's dexterity and intelligence, traced to source

**Date:** 2026-09-30 · **Author:** legolas (UNKNOWN-RESEARCHER) · **Commission:** C-11b (KP-131),
issued by the KC2-PLAY conductor (gandalf); it is C-11a's unpursued **L-C11-2**.
**Boundary:** after the sourced C-11a folds the oracle still takes **×3.17** the referent's landed
intake (w151–159) and dies at 152–156 against the referent's 160. The dominant term is the
**attribute limb** `(dex/245)+1` / `(int/215)+1` (ablation ρ 0.177). Its equation and its scope are
byte-decoded; **the monster dex/int VALUES had never been traced.** The hypothesis under test: *are
they inflated?*
**Mode:** read-only. No sealed cell opened, re-run or moved. Nothing fitted, nothing tuned (Law 3).
**Surfaces:** Mac Edition-II depot `.arz` (`~/depots/…/24346246/`, CRUCIBLE precedence KP-79, mods
included) · Crate authoring templates (`legolas/scratch/2026-08-08-kc2-halt-bundle/tpl/`) ·
Edition-IV `x64/Game.dll` (build 24825149, `~/Games/vendor/grim-dawn-edition-IV-20260929/`) ·
the oracle's own committed substrate (`pm4m_body_chain.csv`, `pm4o_trash_terms.csv`,
`pm4i_wave_damage_modifier.csv`, `pm2_measured_player_sheet.csv`).
**Tooling:** `legolas/scratch/2026-09-30-c11b-attrlineage/` (`arz.py` carried from C-11a, `pools.py`
proxy→pool→creature→level walk, `verify.py` record-by-record attribute re-derivation).

---

## 0 · VERDICT IN ONE PARAGRAPH

⚑ **The monster attribute values are NOT inflated. They are LOW — by ~8–12 % — and the two
departures both point UP.** The lineage is short and fully sourced: a monster record carries
`characterDexterity = 0` and delegates to `characterAttributeEquations` → a **bio record** whose
`characterDexterity` is a `charLevel` equation; the record's own **`charLevel` equation** transforms
the spawn level first; the result is then scaled by `gameengine.dbr :: monsterAttributePak` →
`balancingadjustment_mp+difficulty_enemies01.dbr`, whose **`characterDexterityModifier[8]` and
`characterIntelligenceModifier[8]` are `+10.0` at Ultimate / 1 player**. The oracle omits **both**
the `charLevel` equation (Lap M on 39/39, Lap O on 70 of 183 w151–159 actors) and the +10 % pak
modifier. ⚑ **The Crucible's per-wave balancing arrays contribute EXACTLY ZERO to dex and int** —
`characterDexterity`, `…Modifier`, `characterIntelligence`, `…Modifier` are all scalar `0.0` in all
three `balancingadjustment_survivalmode_enemies0{1,2,3}.dbr`. **There is no champion / hero /
nemesis attribute multiplier anywhere;** tier is carried by *which record spawns*, by that record's
own `charLevel` equation, and by the pool's level-variance equation. Priced on gamora's committed
decomposition, folding the two sourced corrections takes the oracle from **×3.17 → ×3.59**. The one
term that points DOWN — the oracle's level-ceiling promotion — is worth only **×0.98** and is not
adjudicable from source. **This is a negative result on the commission's hypothesis, and it is a
result: the surplus is not in the attribute VALUES.**

| question | answer | grade |
|---|---|---|
| **where do dex / int come from?** | bio record's `characterDexterity`/`…Intelligence` charLevel equations, via the monster record's own `charLevel` equation | **DB-SOURCED-VERBATIM (A)**, Edition-II |
| monster record's own `characterDexterity` | **0.0** on every board record examined | DB-SOURCED (A) |
| skill grants of dex / int | ⚑ **ZERO on all 344 Lap-O actors** (`dex_skill_add == int_skill_add == 0.0`), MEASURED by Lap O | MEASURED (A) |
| Crucible per-wave arrays (`…survivalmode_enemies03`) | ⚑ **ZERO** — scalar `0.0`, not an array | **DB-SOURCED-EXACT (A)** |
| difficulty / player-count adjustment | ⚑ **+10 % dex and +10 % int** at Ultimate / 1 player, and the oracle does not apply it | **DB-SOURCED-EXACT (A)** + **BYTE-DECODED** composition (Edition-IV) |
| hero / champion / nemesis tier multiplier | ⚑ **NONE EXISTS.** Searched negative | **SEARCHED-ABSENT (A)** |
| spawn LEVEL for w151–160 | pool `levelVarianceEquation` on `averagePlayerLevel` = 99–106 at APL 100; the oracle sits at proxy **+3** | **DB-SOURCED (A)** for the equations; ⚑ the **+3 is SOURCE-UNLOCATED** |
| is the oracle's level the same? | no: **+3** over the source equations, and **−4** against them plus `monsterLevelGapFixer` | **MEASURED-vs-SOURCE (A)** |
| **priced effect on landed intake** | ⚑ **×3.17 → ×3.59** (both sourced corrections, UP) | arithmetic on gamora's committed decomposition |

---

## 1 · THE LINEAGE, RECORD BY RECORD

Worked on `ghost_b01.dbr` (wave 151, trash, `Champion` classification), read from the depot with
Crucible precedence. Every field below is verbatim.

```
records/creatures/enemies/ghost_b01.dbr        [SurvivalMode.arz]
    charLevel                      = 'charLevel*1'
    characterAttributeEquations    = 'records/creatures/enemies/bios/bio_ghost_02.dbr'
    characterDexterity             = 0.0          characterDexterityModifier    = 0.0
    characterIntelligence          = 0.0          characterIntelligenceModifier = 0.0
    monsterClassification          = 'Champion'

records/creatures/enemies/bios/bio_ghost_02.dbr [database.arz]
    templateName        = 'database/templates/characterattributeequations.tpl'
    characterDexterity      = '(charLevel*7.0)+45'
    characterIntelligence   = '(charLevel*6.4)+38'
    characterStrength       = '(charLevel*6)+30'
    characterOffensiveAbility = '(charLevel*6)+60'
```

**The chain, stated as a formula:**

```
L    = spawn level                                (pool levelVarianceEquation; § 3)
cl   = <monster record>.charLevel   evaluated at L          e.g. 'charLevel*1', 'charLevel*1+5',
                                                                 '(charLevel*1.1)+2'
dex  = <bio>.characterDexterity(cl)  +  <monster record>.characterDexterity   [ = 0 on the board ]
       + skill grants                                        [ = 0 on all 344, MEASURED by Lap O ]
       + Crucible per-wave array                             [ = 0, scalar, § 2 ]
dex  = dex × (1 + characterDexterityModifier/100)            [ = ×1.10, § 2 — MISSING FROM ORACLE ]
```

**Corroborations for the "no other source" clauses, each a measurement rather than an assumption:**
- `pm4o_trash_terms.csv`, all 344 actors: `dex_source` is `<bio>.dbr::characterDexterity` on
  **344/344** — one source, no exceptions — and `dex_skill_add == int_skill_add == 0.0` on
  **344/344**, with the per-row basis string *"ABSENT on all N own skill slots"*.
- `gameengine.dbr` carries exactly three attribute paks — `monsterAttributePak`, `petAttributePak`,
  `playerAttributePak`. **No champion, hero, nemesis or Crucible pak exists.** The only
  champion/hero fields in `gameengine.dbr` are `championMonsterColor` and `heroMonsterColor`.

⚑ **The tier mechanism, since there is no tier multiplier: it is the record's own `charLevel`
equation.** Over Lap O's 183 w151–159 actors, **111 carry `charLevel*1`** (identity) and **70 carry
a non-identity transform** — `charLevel*1+1` (25), `charLevel*1+5` (17), `(charLevel*1.1)+2` (10),
`charLevel*1+3` (8), `(charLevel*1)+2` (6), `charLevel*1+2` (4). Heroes and nemeses sit in the
non-identity set. **This is the one place a "hero is stronger" adjustment lives, and the oracle
drops it (§ 4).**

---

## 2 · ⚑ THE DIFFICULTY PAK — `+10 %` DEX AND INT, WIRED BY NAME, AND ABSENT FROM THE ORACLE

`records/game/gameengine.dbr` (`database.arz`):

```
monsterAttributePak = 'records/game/balancingadjustment_mp+difficulty_enemies01.dbr'
```

That record is `Class = 'AttributePak'`, `templateName = database/templates/attributepak.tpl`, and
its arrays are **12 long = 3 difficulties × 4 player counts**. Verbatim:

```
characterDexterityModifier    = [-5, -4, -4, -3,  5, 5.5, 6, 6.5,  10, 11, 11.5, 12]
characterIntelligenceModifier = [-5, -4, -4, -3,  5, 5.5, 6, 6.5,  10, 11, 11.5, 12]
characterStrengthModifier     = [-5, -4, -4, -3,  4, 4.5, 5, 5.5,   5,  6,  6.5,  7]
offensiveTotalDamageModifier  = [-25 ×4,            25 ×4,           40 ×4        ]
characterDexterity = 0.0      characterIntelligence = 0.0      (scalars — the FLAT slots are empty)
```

**The index is already on the oracle's own wire and it is index 8.** `pm4i_wave_damage_modifier.csv`
carries, in its own `basis` column for every row 151–170:

> `records/game/balancingadjustment_survivalmode_enemies03.dbr@sm_mod [index wave-1] +
> records/game/balancingadjustment_mp+difficulty_enemies01.dbr@base [index 8 = Ultimate/1-player]`

and its `U_offensiveTotalDamageModifier_pct = 40.0` is exactly `offensiveTotalDamageModifier[8]`.
⚑ **So the oracle already reads row 8 of this pak for damage, OA, DA, life, speed, crit and the
slow-modifiers — and does not read `characterDexterityModifier` / `characterIntelligenceModifier`
from the same row.** They are not in the emitted CSV at all.

### 2.1 · The Crucible per-wave arrays are a measured ZERO on dex and int

All three of `records/game/balancingadjustment_survivalmode_enemies0{1,2,3}.dbr` (`SurvivalMode.arz`,
`gameadjustment.tpl`, 628 fields each) carry:

```
characterDexterity 0.0   characterDexterityModifier 0.0
characterIntelligence 0.0  characterIntelligenceModifier 0.0      — SCALARS, not 200-entry arrays
```

against 23 fields that *are* 200-entry per-wave arrays (`characterLifeModifier`,
`characterOffensiveAbility`, `offensiveTotalDamageModifier`, `defensivePercentCurrentLife`,
`retaliationTotalDamageModifier`, the seven `offensiveSlow*Modifier`s, …).
**The Crucible scales a monster's damage, life, OA, DA and speed by wave. It does not touch its
attributes.** That closes the commission's second candidate as a searched negative.

### 2.2 · The composition form, BYTE-DECODED (Edition-IV `x64/Game.dll`)

The pak's application site is
`AttributePak::GetCharAttributes(CharAttributeAccumulator&, unsigned int, float)` `0x180044930` —
the `unsigned int` is the array index. The accumulator has **three** slots per attribute type, and
their setters are named:

| setter | slot | export |
|---|---|---|
| `CharAttributeAccumulator::AddValue` | `+0x000` | `0x1800bc840` |
| `CharAttributeAccumulator::AddModifier` | `+0x0e8` | `0x1800bc850` |
| `CharAttributeAccumulator::AddMultiplier` | `+0x1d0` | `0x1800bc890` |

`CharAttributeAccumulator::GetValue` (`0x1800bc8b0`) composes them. Read instruction for
instruction, with the three `.rdata` constants resolved (`0x18077712c = 1.0`,
`0x18077720c = 100.0`, `0x1807770a0 = 0.01`):

```
xmm3 = mult[i] + 1.0 ; ×100.0 ; max 0
xmm4 = value[i]
xmm2 = modifier[i]
if value >= 0:   xmm2 = ((modifier × 0.01) + 1.0) × value × xmm3 × 0.01   ; max 0
```

i.e. ⚑ **`total = max(0, value × (1 + modifier/100) × (1 + multiplier))`.**
`characterDexterity` mints a `CharAttributeVal_Dexterity` (vtable `0x1806b6b38`) and
`characterDexterityModifier` a `CharAttributeMod_Dexterity` (vtable `0x1806b65b8`) — the **Val/Mod**
class split *is* the absolute/percent split, and it is the same paired-field convention the oracle
already ruled on for OA (`offense.py` § 1b, on four named pieces of evidence, and
`combatformulas.dbr :: offensiveAbilityEquation`'s own two slots:
`(… + ((dexterityDV + bonusDV)*0.5)) * (1 + (offensiveAbilityModifierDV/100)) + 53`).

⚑ **So `+10.0` is a PERCENT on the accumulated dexterity, not a flat +10.** Grade **A** on the
form, with the standing C-11a caveat that the mechanism is Edition-IV (post-referent) while the
values are Edition-II.

---

## 3 · THE SPAWN LEVEL — sourced to an equation, and the oracle sits +3 above it

**The chain:** Crucible wave *w* → tier `⌈w/10⌉`, wave-in-tier `w−10(t−1)` →
`records/proxies/tier16waves/proxy_w<NN>_p<NN>a.dbr` → `pool1..poolN` →
`records/proxies/poolsbasic…/<pool>.dbr` → per creature slot, `levelVarianceEquation<i>` →
`records/proxies/lv<N>_<name>.dbr`. Verbatim (all `database.arz`):

| equation record | min | max |
|---|---|---|
| `lv2_normal` | `(averagePlayerLevel-1)` | `(averagePlayerLevel)` |
| `lv3_strong` | `(averagePlayerLevel)` | `(averagePlayerLevel)+(averagePlayerLevel/75)` |
| `lv3_strong+` | `(averagePlayerLevel)` | `(averagePlayerLevel+1)+(averagePlayerLevel/90)` |
| `lv4_champion` | `(averagePlayerLevel+1)` | `(averagePlayerLevel+1)+(averagePlayerLevel/75)` |
| `lv4_champion+` | `(averagePlayerLevel+1)` | `(averagePlayerLevel+1)+(averagePlayerLevel/50)` |
| `lv5_elitechampion` | `(averagePlayerLevel+2)` | `(averagePlayerLevel+1)+(averagePlayerLevel/50)` |
| `lv6_hero` | `(averagePlayerLevel+2)+(averagePlayerLevel/50)` | `(averagePlayerLevel+3)+(averagePlayerLevel/50)` |
| `lv7_uber hero` | `(averagePlayerLevel+3)` | `(averagePlayerLevel+3)+(averagePlayerLevel/50)` |
| `lv8_boss+` | `(averagePlayerLevel+4)+(averagePlayerLevel/50)` | *(same)* |

**The referent's player level is 100** — `pm2_measured_player_sheet.csv`, *"screenshot 495;
screenshot 508; gdc header; gdc block2"*, three-way agreement. So at `averagePlayerLevel = 100` the
sourced band for waves 151–160 is **99 … 106**.

### 3.1 · ⚑ The oracle is the source band + 3, exactly, on every record

I walked all 10 waves' tier-16 proxies and compared record by record against
`pm4o_trash_terms.csv :: pool_proxy_levels`. **Every row is source + 3:**

| creature (w151) | equation | source @ APL 100 | oracle `pool_proxy_levels` |
|---|---|---|---|
| `ghost_a01/a02` | `lv2_normal` | 99 – 100 | **102 \| 103** |
| `ghost_b01/b02/b03` | `lv3_strong` | 100 – 101 | **103 \| 104** |
| `ghost_b04` | `lv4_champion` | 101 – 102 | **104 \| 105** |
| `swampgolem_a01` | `lv4_champion+` | 101 – 103 | **103 \| 104 \| 105 \| 106** |
| `wendigo_c01` (w153) | `lv5_elitechampion` | 102 – 103 | **105 \| 106** |
| `swampcrab_ugdenbog_01` (w152) | `lv7_uber hero` | 103 – 105 | **106 \| 107 \| 108** |
| `nemesis_beast_01_p1` (w154) | `lv8_boss+` | 106 | **109** |

The +3 is Lap D's `APL_B_PRIME = 103.4`, named in Lap O's findings § 6 as its secondary basis.
**It is not in any record.** `averagePlayerLevel` is 100.

### 3.2 · `monsterLevelGapFixer` would give +7, not +3 — and the measured banner rules both out

`gameengine.dbr :: monsterLevelGapFixer = [0, 5, 7]`, and `gameengine.tpl`'s own description is
**"Index by difficulty 0 to 2 - adds to monster level"**. At Ultimate (2) that is **+7**, which
would place the w160 nemesis at **113**.

⚑ **The referent's own on-screen monster banner reads 109** for the wave-160 nemesis (Lap M,
reproduced by Lap O § 6). So:

- source equations alone → **106**  ✗
- source equations + `monsterLevelGapFixer[2]` → **113**  ✗
- the oracle (APL′ 103.4) → **109**  ✓ against the one measurement that exists

**I also checked the obvious escape and it is closed:** `proxylevelvarianceequation.tpl` declares
`min/maxVarianceEquationEpic` and `min/maxVarianceEquationLegendary` slots — Ultimate would read
`Legendary` — and **every `lv*.dbr` authors only the `Normal` pair.** There is no per-difficulty
level equation. Searched negative.

**Ruling: the +3 is `SOURCE-UNLOCATED`, and it is now a SEARCHED `SOURCE-UNLOCATED`.** The oracle's
level basis is anchored to the one measured body and I will not fit the rest. What survives as a
finding is the second half of Lap O § 6, which I can now price:

⚑ **186 of 344 actors carry level 109 — the ceiling — including 98 trash bodies the proxy law would
place at 102–107.** That is the only term in this note that points DOWN, and it is worth
**×1.015 on the attribute multiplier** (mean over Lap O's 183 w151–159 actors; max ×1.05).

---

## 4 · ⚑ THE ORACLE-vs-SOURCE COMPARISON, RECORD BY RECORD

Re-derived from the depot with `verify.py`: for each body, read its own `charLevel` equation, apply
it to the level the oracle used, evaluate the bio equation, and compare with the oracle's committed
value. **No reconstruction: the oracle's own level is the input, so only the transform is under
test.**

### 4.1 · Lap M (`pm4m_body_chain.csv`, the 39 MEASURED bodies — bosses, heroes, nemeses)

**Convention test, four candidates, 39 bodies:**

| what the oracle appears to compute | exact matches |
|---|---:|
| bio equation at `level_lo`, `charLevel` eq applied | 4 / 39 |
| bio equation at `level_hi`, `charLevel` eq applied | 11 / 39 |
| bio equation at `level_lo`, **raw** | 16 / 39 |
| ⚑ **bio equation at `level_hi`, `charLevel` eq NOT applied** | **39 / 39** |

**So Lap M evaluates the bio equation at the raw spawn level and skips the record's own `charLevel`
equation.** On the 4 bodies whose `charLevel` is the identity (`nemesis_kymon_02`,
`…orderdeathsvigil_01`, `…outlaw_01`, `…undead_02b`) the two agree exactly, which is the positive
control.

| body | `charLevel` eq | oracle dex | source dex | source ×1.10 pak |
|---|---|---:|---:|---:|
| `nemesis_kymon_01` | `(charLevel*1.1)+2` | 1,170.0 | **1,299.0** | **1,428.9** |
| `nemesis_aetherialvanguard_01` | `charLevel*1+5` | 1,170.0 | 1,220.0 | 1,342.0 |
| `nemesis_outlaw_01` | `charLevel*1` | 1,170.0 | 1,170.0 | 1,287.0 |
| `wendigocannibal_h01…h05` (hero) | `(charLevel*1)+2` | 922.2 | 939.0 | 1,032.9 |
| `aetherial_fleshhulk_mine` | `(charLevel*1.1)+2` | 988.0 | **1,096.8** | **1,206.5** |
| `statue_korvaaktombguardian` | `charLevel*1` | 919.0 | 919.0 | 1,010.9 |
| `witchgod_finalboss` | `charLevel*1+5` | 973.0 | 1,015.5 | 1,117.1 |

**Mean attribute-multiplier ratio, source (charLevel eq + 10 % pak) ÷ oracle, over all 39:
×1.127** (min ×1.079, max ×1.185).

### 4.2 · Lap O (`pm4o_trash_terms.csv`, the trash/hero/boss board, 183 actors at w151–159)

Same test at Lap O's own `spawn_level`: **113 of 183 reproduce exactly** and **70 do not** — and the
70 are precisely the actors with a non-identity `charLevel` equation (`swampgolem_h01/h02/h05`
`(charLevel*1.1)+2`: oracle 930.6 vs source 1,039.0; `livingplant_a01` `charLevel*1+5`: 700.8 vs
731.8; `swampgolem_a01`: 689.0 vs 766.4). ⚑ **Lap O emits the equation in a `charlevel_equation`
column and then does not apply it.** Same single cause as Lap M.

**Mean attribute-multiplier ratio, source ÷ oracle, over the 183: ×1.089** (min ×1.067, max ×1.185).

### 4.3 · Which way, and by how much — the answer to the commission's question

| departure | direction | mean effect on `a` |
|---|---|---|
| **A** — the record's own `charLevel` equation, dropped by both laps | oracle **LOW** | ×1.010 (trash 1.006 · hero 1.022 · boss 1.014) |
| **B** — `characterDexterityModifier/…Intelligence…[8] = +10 %`, never read | oracle **LOW** | **×1.077** |
| **A + B** | oracle **LOW** | **×1.089** |
| **C** — the 109 level-ceiling promotion (186/344), source-unlocated | oracle **HIGH** | ×1.015 |

⚑ **Net: the oracle's monster attributes are about 7 % low. The hypothesis that they are inflated
is FALSE, and the falsification is a measurement, not an opinion.**

---

## 5 · THE PRICE — arithmetic on gamora's committed decomposition, nothing fitted

**Inputs, all from her C-11a fold ADDENDUM § A (FOLDED arm, salts 0–19, pooled w151–159, landed,
Leg B) and C-11 FINDINGS § 2:** landed by class hero 995 · trash 2,324 · boss 715 · champion 499 ·
champion-bounty 337 · summon 202 · nemesis 5 (**Σ 5,077**); referent **1,605.6**; **×3.175**.
Limb-removal divisors: hero 33 · champion-bounty 40 · champion 9.6 · trash 7.0 · boss 2.25 ·
summon/nemesis ≈ 1.

**Method (stated so it can be refused).** A divisor is the intake ratio when `a` is driven to 1.
With the per-class mean `a` computed from Lap O's own committed dex/int (trash 4.105 · hero 5.048 ·
boss 4.828), each class's local elasticity is `ε = ln(divisor) / ln(a)` — trash 1.38 · hero 2.16 ·
champion 1.60 · champion-bounty 2.61 · boss 0.52 — and a small change in `a` moves that class's
landed intake by `(a′/a)^ε`. **The elasticities are read off HER measured divisors and HER
attribute values; nothing is tuned.** ε > 1 is her own finding, not mine: the counterplay kit
absorbs flat amounts, so intake grows faster than linearly in per-hit size.

| # | correction | landed hp/s | **× referent** |
|---|---|---:|---:|
| — | **BASE** (v3.6 folded, her ADDENDUM) | 5,077 | **×3.162** |
| **A** | the record's own `charLevel` equation applied | 5,161 | **×3.215** |
| **B** | the `+10 %` Ultimate/1-player attribute modifier applied | 5,663 | **×3.527** |
| **A+B** | ⚑ both sourced corrections | **5,762** | ⚑ **×3.589** |
| C | level ceiling 109 → proxy-low (**not source-adjudicable**) | 4,969 | ×3.095 |
| A+B+C | all three at once (`charLevel` eq evaluated at the proxy-low level, then the pak) | 5,640 | ×3.513 |

**Reading, stated and not smoothed.** Every sourced correction available in this lap makes the
oracle **more** lethal. The surplus is not in the attribute values, and it is not in the Crucible's
per-wave arrays, which do not touch attributes at all. Combined with C-11a — where the retaliation
gate and the duration divisors both had **zero population** and only the aura re-model moved
anything — ⚑ **four consecutive sourced corrections have now failed to close the ×3 gap, and three
of the last five point the wrong way.** That is itself a finding about where to look next: not at
the attribute limb's inputs.

---

## 6 · WHAT GAMORA WOULD CHANGE — stated, not made

Each item alters the oracle's reference. **That is Matt's HALT. Nothing is proposed as an action.**

1. ⚑ **Apply the monster record's own `charLevel` equation before evaluating the bio equation.**
   Sourced, exact, mechanically trivial, and it is a *substrate re-emission* (Lap M's and Lap O's
   CSVs both need the column recomputed), not a coefficient change. Worth ×1.02 on landed intake.
   **It is also the only place a hero/nemesis "tier bonus" exists in GD**, so dropping it flattens
   a distinction the referent has.
2. ⚑ **Fold `characterDexterityModifier[8] = +10` and `characterIntelligenceModifier[8] = +10`**
   from `gameengine.dbr :: monsterAttributePak`. This is the larger item (×1.12 on landed intake)
   and it is **the same pak row, index 8, the oracle already reads for six other columns** — so it
   is a missing column in `pm4i_wave_damage_modifier.csv`, not a new source. The composition is
   byte-decoded: `value × (1 + modifier/100)`.
3. **Do NOT fold `monsterLevelGapFixer`.** `[0,5,7]` with the template's own *"adds to monster
   level"* would put the w160 nemesis at 113 against a measured on-screen **109**. It is contra-
   indicated by the only level measurement we have. Leave U-5 open.
4. **Re-grade the level basis, do not change it.** The oracle's `+3` over the sourced proxy
   equations is `SOURCE-UNLOCATED` and now **searched**. Keep it (it matches the measured banner);
   record that the 109 ceiling on 98 trash bodies is worth ×0.985 and is the only DOWN lever found.
5. **Record the zero.** `balancingadjustment_survivalmode_enemies0{1,2,3}` contribute **nothing** to
   dex/int. Worth adding as a measured zero so the question is not re-asked.

---

## 7 · KNOWLEDGE GAPS NOT RESOLVED

- ⚑ **The `+3` level offset (`APL_B_PRIME = 103.4`).** Searched: the proxy equations, the
  per-difficulty `Epic`/`Legendary` equation slots (unauthored everywhere), `monsterLevelGapFixer`,
  the three Crucible balancing records, `gameengine.dbr`, and the mp+difficulty pak. **Not
  recoverable from the records.** Closing it needs either a `Monster::SetLevel`-class decode in the
  Edition-IV binary or a second on-screen monster-banner reading from the footage at a *trash*
  body — which would also settle the 109-ceiling question in one shot. **That is the cheapest
  remaining lift in this area and it is a galadriel/T30 item, not mine.**
- Whether `AttributePak::GetCharAttributes`'s `float` third parameter scales the pak's contribution
  (it is passed by the caller; I did not trace the call site). If it is not 1.0 for monsters, the
  +10 % is a bound rather than a value. **Grade B on the magnitude for that reason; grade A on the
  sign and on the field's existence.**
- The Edition-IV caveat from C-11a travels unchanged: § 2.2's mechanism is post-referent; §§ 1–3's
  values are Edition-II / CRUCIBLE precedence.
- I did not re-derive whether the oracle's `level_hi`-over-`level_lo` choice for Lap M is itself
  correct; I took it as the input under test and varied only the transform.
