# KC2-PM4 · LAP O — THE TRASH-BOARD DECODE + OA/DA BOTH SIDES OF THE SCREEN

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-14 · **Run:** KC2-PM4, Lap O
**Laws:** READ-ONLY on every source · **GL-12 decode-never-estimate** · **GL-6 full digests** ·
**OUTCOME FIREWALL** (§ 0.2)

---

## 0 — WHAT THIS LAP WAS ASKED, AND WHAT IT RETURNED

### 0.1 Headline

| | asked | returned |
|---|---|---|
| **A · trash-board attribute terms** | close the halt list | **154 / 154 records · 321 / 321 actors CLOSED. Zero ABSENT.** |
| **A · own total-damage passives** | close the halt list | **104 / 104 records · 193 / 193 actors CLOSED. Zero ABSENT — and every single one is NON-ZERO.** |
| **B · monster OA, w151–160** | decode + level-scale | **95 (body × wave) rows, all four named bodies present.** |
| **B · player OA / DA** | derive from the played save | **OA 3,259 · DA 2,591** (sheet totals, gear + attributes included) |
| **B · predicted PTH + tier distribution** | both directions | **both emitted for all 95 bodies. Zero UNDECIDED on PTH itself; one named UNDECIDED on crit-damage COMPOSITION (§ 5.2).** |

**The one-line result.** *The board's trash was never neutral — the identity path the data gate
took (attr × 1.0, own-TDM 0.0) was under-reading the **median** halted actor's damage by
**4.380 × 1.224 = 5.36×** (range **2.96× … 10.70×**, § 2.4) — and the OA/DA picture is violently
asymmetric: **the player literally cannot miss anything on this board (95 / 95 bodies at PTH ≥ 100)
and crits a quarter of the time, while the board misses the player one swing in eight and crits
under 1 %.***

### 0.2 The firewall, stated precisely

The findings JSON was opened **once**, and the reader (`pm4o_lib::halt_list`) touches exactly one
key — `⚑ data_gate` — from which it takes the halt dictionary, the measured-record list, and the
four record/actor counts. No scorecard, no verdict, no `l4l`, no `⚑ death`, no `⚑ predictions_graded`,
no `match_gates`, no `sensitivity`. Nothing in this lap's arithmetic depends on a simulation
outcome, and no target band was consulted.

**Sources, exhaustively:**

| source | sha256 | what for |
|---|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (8 `.arz` + `templates.arc`) | (per-archive, Lap D/I pinned) | every equation, every magnitude |
| `…/simulation/output/kc2-pm4-i14-findings-20260814_094018.json` | `a3c6264cce97e42fbc5cfc2929b174b06c5da70d269f60b01306d4715588017c` | **`⚑ data_gate` ONLY** — the halt list |
| `…/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` | `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` | the FROZEN roster roll — `record_path` / `wave` / `level` / `actor_id` / `display_name` / `threat_tier` only |
| `data/kc2/pe6_crucible_wave_pools_v2.csv` | (my own pe6 emission) | the pool-proxy level basis (sensitivity band, § 6) |
| legolas Lap A `measured-player-sheet.csv` (screenshots 495 / 508) + Lap G `gdc/_EoRWarlGuts/player.gdc` | | the player OA / DA / attributes |
| grimdawn.com/guide/gameplay/combat (accessed 2026-08-14) | | the DOCUMENTED PTH law + crit-tier rules |

**Instruments** (`agentic_orchestration/research/scripts/`):
`pm4o_lib_2026_08_14.py` · `pm4o_emit_2026_08_14.py` · `pm4o_verify_2026_08_14.py`.
The `.arz` reader (`E3`), the equation evaluator (`ev`), the skill-slot walk, the survival wave
arrays, the difficulty pak and `own_total_damage_modifier` are **imported from Lap I / Lap M,
never re-implemented.**

---

## 1 — WHY THE TERMS WERE MISSING (the prior gap, named)

The gate reported attribute terms present on **15 of 169** records. All 15 are `boss&quest/` or
`nemesis/` bodies. That distribution is the whole diagnosis:

> **The attribute terms are not on the creature record. They are one hop away, on the bio record
> the creature points at.**

Every Crucible creature record carries

```
characterAttributeEquations = 'records/creatures/enemies/bios/bio_<something>.dbr'
```

and the bio — a separate `.dbr`, frequently in a **different archive** than the creature — carries
`characterDexterity` / `characterIntelligence` / `characterStrength` /
`characterOffensiveAbility` / `characterDefensiveAbility` as **charLevel equation strings**:

```
records/creatures/enemies/wendigo_a01.dbr          [archive sm1]
  characterAttributeEquations = records/creatures/enemies/bios/bio_wendigo_a01.dbr

records/creatures/enemies/bios/bio_wendigo_a01.dbr [archive gdx1]   ← different archive
  characterDexterity        = (charLevel*6.5)+25
  characterIntelligence     = (charLevel*6.5)+15
  characterStrength         = (charLevel*6)+15
  characterOffensiveAbility = (charLevel*6)+35
  characterDefensiveAbility = (charLevel*4.5)+20
```

An extractor that reads the creature record and stops finds nothing. The 48-file extract landed
the terms for the 15 bodies whose bios happened to be inside it, and for nobody else. The 169
records resolve to **101 distinct bio records**, spread across **all eight archives**
(`gdx1` 98 actors, `sm_mod` 94, `base` 45, `gdx3` 31, `sm1` 26, `gdx2` 23, `sm3` 15, `sm2` 12) —
which is why a partial extract could not have covered them by luck.

**Result of following the hop: 169 / 169 records have a resolvable bio, and every one of those
bios carries all five fields. There is no ABSENT anywhere in the attribute layer.**

---

## 2 — PART A · THE DECODE (`pm4o_trash_terms.csv`, 344 rows × 58 cols)

One row per **roster actor** — all 344, so the halt list is closed actor-by-actor, not just
record-by-record. Each row names the record path of every term it reports.

### 2.1 Halt classes closed

| halt class | actors | records | closed |
|---|---:|---:|---|
| **both** (attr-halted AND own-halted) | 193 | 104 | ✅ 193 / 193 |
| **attr_only** | 128 | 50 | ✅ 128 / 128 |
| none (already measured) | 23 | 15 | — carried for completeness |
| **total** | **344** | **169** | |

By threat tier the halt was overwhelmingly the trash board, exactly as the commission suspected:
trash 211 actors (119 both + 92 attr-only), hero 63, boss 46, nemesis 1.

### 2.2 The attribute terms — magnitude, and what the identity path cost

Over the **321 attr-halted actors**, evaluated at each actor's own spawn level:

| term | min | median | max |
|---|---:|---:|---:|
| `characterDexterity` total | 522.0 | **828.1** | 1,170.0 |
| `characterIntelligence` total | 324.0 | **728.5** | 1,170.0 |
| `characterStrength` total | 555.0 | 733.5 | 912.0 |

These feed `combatformulas.dbr` directly:

```
physicalDamageEquation = physicalDamageDV * ((dexterityDV/245)+1)
pierceDamageEquation   = pierceDamageDV   * ((dexterityDV/245)+1)
magicalDamageEquation  = magicalDamageDV  * ((intelligenceDV/215)+1)
```

so the number a damage consumer actually multiplies by is emitted per row as
`attr_mult_physical_pierce` and `attr_mult_magical`:

| multiplier | min | **median** | max |
|---|---:|---:|---:|
| physical / pierce `1 + dex/245` | 3.131 | **4.380 ×** | 5.776 × |
| every magical family `1 + int/215` | 2.507 | **4.388 ×** | 6.442 × |

⚑ **The identity path (attr multiplier 1.0) under-read the median halted actor's flat damage by
4.38×.** That is not a rounding-scale error; it is the single largest term in the monster attack
chain, and it was set to unity for 321 of 344 actors.

### 2.3 The own total-damage passives — and the record that explains them

Over the **193 own-halted actors**:

| `own_total_damage_modifier_pct` | value |
|---|---:|
| min | **+33 %** |
| p25 | +41 % |
| **median** | **+41 %** |
| p75 | +49 % |
| mean | +53.04 % |
| max | **+121 %** |

**Not one halted actor measured zero.** The `ABSENT-MEASURED-ZERO` list is empty. The reason is
structural, and it is worth banking:

| source record | actors carrying it |
|---|---:|
| `records/skills/nonplayerskills/passive/damage_totaladjuster.dbr` | **193 / 193 — every one** |
| `…/passive/armorbase04.dbr` | 62 |
| `…/passive/armorbase03.dbr` | 55 |
| `…/passive/armorbase05.dbr` | 35 |
| `…/passive/armorbase02.dbr` | 29 |
| `…/genericphysical_charge` | 25 |
| `…/passive/armorbase01.dbr` | 12 |
| body-specific (`sharzul_laststand` +35, `alkamos_laststand` +50, `factoryguardian_enrage` +40, `cultistsummoner_rally` +35, `aetherrage1_zombiemutant`) | 1–2 each |

Every source is emitted with its **full record path, its array index, the value read and the
index state** — e.g. for `wendigo_a01` @ lv103:

```
records/skills/nonplayerskills/passive/damage_totaladjuster.dbr::offensiveTotalDamageModifier[3]=16.0(IN-RANGE,rank=4)
records/skills/nonplayerskills/passive/armorbase03.dbr::offensiveTotalDamageModifier[102]=25.0(IN-RANGE,rank=103)
records/skills/nonplayerskills/attackcharge/genericphysical_charge.dbr::offensiveTotalDamageModifier[4]=75.0(CLAMPED-HIGH,rank=26)
```

⚑ **Out-of-range reads are named, not silently clamped.** Across all 344 rows the own-TDM layer
performed **702 IN-RANGE** reads and **19 CLAMPED-HIGH** reads (19 actors carry at least one) —
the familiar GD condition where a skill's `skillMaxLevel` exceeds its own array length. Lap I's
`_idx` rule is carried unchanged and the state rides in the source string, so a consumer can
re-decide the clamp.

`damage_totaladjuster` is a **universal** slot on this board — every Crucible body carries it, at a
rank set by the body's own `skillLevel{i}` equation, and its `offensiveTotalDamageModifier` array
is read at that rank. `armorbase01..05` — the "For Bosses / For Champions" defensive passives Lap M
already met on the armour side — carry a total-damage rider too. **A body's own total-damage grant
is the rule on this board, not the exception**, which is why an identity default of 0.0 is never
right here.

Composed with the two terms Lap I already measured (ultimate pak `[8]` = **+40 %**, survival
`enemies03[w-1]` = **+42 %** on waves 151–157 / **+43 %** on 158–160), the median halted actor's
total-damage stack at wave 160 is **40 + 43 + 41 = +124 %**, i.e. **×2.24** — against the **×1.83**
the identity path produced. That is a **1.224×** under-read sitting on top of the **4.380×**
attribute under-read.

### 2.4 The compound under-read, stated exactly

| | attribute factor | total-damage factor | **compound** |
|---|---:|---:|---:|
| softest halted actor (magical family, own-TDM +33 %) | 2.507 × | 1.180 × | **2.96 ×** |
| **median halted actor** | **4.380 ×** | **1.224 ×** | **5.36 ×** |
| hardest halted actor (magical family, own-TDM +121 %) | 6.442 × | 1.661 × | **10.70 ×** |

*(The total-damage factor is `(1 + (40 + G(w) + own)/100) / (1 + (40 + G(w))/100)` — the ratio of the
measured stack to the identity stack. It is computed at wave 160; at waves 151–157 `G(w) = 42` and
the factor moves by under 0.002.)*

⚑ **Grade carried from Lap I § 1.4, unchanged:** the three total-damage terms are each MEASURED
(named record, named field, named index); that they compose **ADDITIVELY** is
`DERIVED-SUM-ADDITIVE-BY-PARALLEL` with the life chain, not independently measured on the damage
field. Every component rides beside the sum so a consumer can recombine under another rule.

### 2.5 The ABSENT list

**Empty on both terms.** No record on the halt list failed to yield `characterDexterity`,
`characterIntelligence`, or a measured `offensiveTotalDamageModifier`. Every row nonetheless
carries `own_tdm_slots_checked` — the full list of skill records interrogated — so an ABSENT, had
one occurred, would have been evidenced rather than asserted.

---

## 3 — PART B · THE LAW (documented, and how much of it is documented)

### 3.1 The equations, from `records/game/combatformulas.dbr` [archive `base`]

```
offensiveAbilityEquation = (offensiveAbilityDV + (characterLevelDV*12) + ((dexterityDV + bonusDV)*0.5))
                             * (1 + (offensiveAbilityModifierDV/100)) + 53
defensiveAbilityEquation = (defensiveAbilityDV + (characterLevelDV*12) + ((strengthDV + bonusDV)*0.5))
                             * (1 + (defensiveAbilityModifierDV/100)) + 53
probabilityToHitEquation = ((((offensiveAbilityDV/((defensiveAbilityDV/3.5)+offensiveAbilityDV))*300)*0.3)
                           + (((((offensiveAbilityDV*3.25)+10000) - (defensiveAbilityDV*3.25))/100)*0.7)) - 50
normalPTHEquation        = probabilityToHitDV/70
pthMinimum               = 55
pthThreshold1..6         = 70 / 90 / 105 / 120 / 130 / 135
pthDamageModifier1..6    = 1.0 / 1.1 / 1.2 / 1.3 / 1.4 / 1.5
```

### 3.2 The citation, and the exact agreement

**grimdawn.com — Guide → Gameplay → Combat** (`https://www.grimdawn.com/guide/gameplay/combat/`,
accessed 2026-08-14) states the PTH equation **character-for-character identically** to the record:

> "Probability To Hit (PTH) = ((((Attacker's OA / ((Defender's DA / 3.5) + Attacker's OA)) * 300) *
> 0.3) + (((((Attacker's OA * 3.25) + 10000) – (Defender's DA * 3.25)) / 100) * 0.7)) – 50"

and adds four rules this lap relies on, each quoted:

1. > "PTH cannot go below 55 for you or your enemies, meaning that no matter how much Defensive
   > Ability you or your foe may have, you will never have a lower than 55 % chance to hit them."
   → **PTH is the percentage chance to hit**, floored at 55. (`pthMinimum = 55` in the record.)
2. > "At PTH 100 and above, you cannot miss your target."
   → hit chance `= min(1, PTH/100)`.
3. > "If your PTH is lower than 70, any attacks that land will do reduced damage. The damage
   > reduction multiplier is equal to your PTH / 70 (ex. if your PTH is 65, you will do 92.86 % of
   > normal damage on a hit, or 65/70)."
   → **`normalPTHEquation` is a DAMAGE scalar, not a hit chance.**
4. > "When your PTH reaches 90 and beyond, you will begin to see critical hits."
   → agrees with `pthThreshold2 = 90`.

⚑ **DEFECT CAUGHT AND BANKED — D-O-1.** Lap M's `hit_chance(p) = min(1, p/70)` read
`normalPTHEquation` as the hit chance. Rules 1–3 above settle it: `PTH/70` is the sub-70 **damage**
scalar, and the hit chance is `PTH/100`. The two differ materially in exactly the band this board
sits in (a PTH of 87 is an 87 % hit chance, not a certainty). Lap M's *damage* conclusions are not
affected — it used `hit_chance` only as a per-swing scalar and reported maxima — but any consumer
that pulled `hit_chance` out of `pm4m_lib` should re-pull it from here. **This lap's numbers use the
documented `PTH/100`.**

The crit **mass** rule comes from the community mechanics writeups (Grim Dawn Wiki `Game_Mechanics`;
Steam guide *Grim Dawn — Game Mechanics Guide*, id 596728673), which state the roll explicitly —
a uniform 1..100 roll decides hit/crit — and give the tier-1 mass with two worked examples:
"the chance to critically strike is PTH − 90" (PTH 95 → 5 %; PTH 110 → 20 %).

### 3.3 The model this lap predicts from, term by term, with its grade

With `P = max(55, PTH)` and thresholds `T₂..T₆ = 90/105/120/130/135`:

```
P(miss)          = max(0, 100 − P)/100                     MEASURED-OR-DOCUMENTED (rules 1,2)
P(tier ≥ k)      = clamp((P − T_k)/100, 0, 1)              k=2 DOCUMENTED · k=3..6 DERIVED-BY-PARALLEL
P(exact tier k)  = P(≥T_k) − P(≥T_{k+1})
P(normal ×1.0)   = P(hit) − P(≥T₂)                         (only when P ≥ 70)
if P < 70:  no crit mass; every landed hit carries the flat scalar P/70      DOCUMENTED (rule 3)
E[mult | hit]    = Σ_k P(exact k)·mult_k / P(hit)
```

⚑ **The one DERIVED step, named.** That the identical "mass = PTH − T_k" rule extends to
T₃…T₆ (105/120/130/135) is **not** independently documented. The record stores the six thresholds in
one uniform array against one uniform multiplier array, and the k=2 case is documented with two
worked examples; extending the same rule to k=3..6 is the minimal reading, and it is the only
reading under which the mass conserves. Every tier-distribution column carries this grade.
`pth_effective` rides beside every distribution so a consumer who rejects the extension can
recombine from the PTH alone.

**Mass conservation was verified, not assumed:** V5 checks
`P(miss) + P(normal) + Σ P(tier k) = 100 %` on all 190 direction-rows — max deviation **0.000e+00**.

---

## 4 — PART B · THE NUMBERS (`pm4o_oa_da.csv`, 96 rows × 82 cols)

95 monster rows = every distinct (body × wave) on waves **151–160** of the frozen roster, plus one
PLAYER row. *(Wave 150 is not in the frozen 20-wave roll, which begins at 151 — stated, not
silently dropped.)*

### 4.1 The player, both abilities

| quantity | value | basis |
|---|---:|---|
| level | 100 | sheet · gdc header · gdc block2 (three-way agreement, Lap A) |
| Physique / **Cunning** / Spirit | 914 / **1,219** / 398 | sheet totals (base + gear + skills) |
| **Offensive Ability** | **3,259** | sheet TOTAL, screenshots 495 / 508 — gear flat + gear % + skills + attributes already folded in |
| **Defensive Ability** | **2,591** | sheet TOTAL, screenshots 495 / 508 (the same DA Lap M's defence sheet used) |
| +% Critical Damage | +57 % | screenshot 511 |

Run forward through the game's own `offensiveAbilityEquation`, the **structural** part of the
player's OA is `100×12 + 1219×0.5 + 53 = 1,862.5`, leaving **1,396.5 OA-units** contributed by gear
flat OA, gear/skill % OA and skill grants. Likewise DA: structural `100×12 + 914×0.5 + 53 = 1,710`,
leaving **881 DA-units**. Those residuals are **carried, not decomposed**: the character sheet
reports a total, and flat-vs-% is not separable from a total alone. The CSV marks both
`UNDECOMPOSED`. **The totals themselves are MEASURED and are what the PTH law consumes**, so no
prediction is degraded by the non-decomposition.

**Conditional OA modifiers, named but NOT folded into the headline** (they are proc-gated, and
folding a proc into a steady-state prediction would be an estimate):
* **Fighting Spirit** rank 5 — +108 OA, 30 % on-hit, 6.2 s. Against the wave-160 nemesis DA 2,611.8
  this lifts player PTH **107.96 → 110.85** (crit mass 17.96 % → 20.85 %).
* **Field Command** rank 14 — +100 OA / +100 DA, always-on passive; already inside the sheet totals.
* **Shifting Sands** (devotion tier3_20e, dev 15) — applies **−140 OA to the enemy**. Against the
  wave-160 nemesis this drops monster→player PTH **95.16 → 91.19** (crit mass 5.16 % → 1.19 %).

### 4.2 The four named bodies (spawn level applied, wave-160 survival + Ultimate-solo pak folded)

| body | wave | lvl | **OA** | **DA** | m→p PTH | m→p hit | m→p crit | m→p E[mult]/swing | p→m PTH | p→m hit | p→m crit | p→m E[mult]/swing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `nemesis_kymon_01` | 160 | 109 | 2,772.52 | 2,611.81 | **95.16** | 95.16 % | 5.16 % | 0.9568 | **107.96** | **100 %** | 17.96 % | 1.0209 |
| `nemesis_aetherialvanguard_01` | 160 | 109 | 2,772.52 | 2,611.81 | **95.16** | 95.16 % | 5.16 % | 0.9568 | **107.96** | **100 %** | 17.96 % | 1.0209 |
| `nemesis_wendigo_01` | 160 | 109 | 2,945.19 | 2,770.09 | **99.98** | 99.98 % | 9.98 % | 1.0098 | **103.54** | **100 %** | 13.54 % | 1.0135 |
| `statue_korvaaktombguardian` | 160 | 108 | 2,696.71 | 2,521.07 | **93.02** | 93.02 % | 3.02 % | 0.9332 | **110.50** | **100 %** | 20.50 % | 1.0260 |

*(`nemesis_kymon_01` and `nemesis_aetherialvanguard_01` share `bio_boss_nemesis_01.dbr` and carry
identical `characterOffensiveAbilityModifier` stacks, hence identical OA/DA. `nemesis_wendigo_01`
runs a richer bio. Both facts are in the CSV's term columns, not inferred.)*

### 4.3 The board, both directions — the headline asymmetry

Actor-weighted across all 188 wave-151–160 actors:

| | **monster → player** | **player → monster** |
|---|---:|---:|
| PTH range across bodies | **77.15 … 99.98** | **103.54 … 124.89** |
| PTH, actor-weighted mean | **87.32** | **115.46** |
| hit chance, mean | **87.32 %** | **100.00 %** |
| bodies that cannot miss (PTH ≥ 100) | **0 / 95** | **95 / 95** |
| bodies floored at `pthMinimum` 55 | 0 / 95 | 0 / 95 |
| crit mass (any tier), mean | **0.77 %** | **25.46 %** |
| ×1.1 tier | 0.77 % | 14.99 % |
| ×1.2 tier | 0.00 % | 10.08 % |
| ×1.3 tier | 0.00 % | 0.39 % |
| ×1.4 / ×1.5 tiers | 0.00 % | 0.00 % |
| **E[damage multiplier] per swing** | **0.874** | **1.036** |

Extremes, named: the board's **weakest attacker** into the player is `swampcrab_a01` @ w158 lv103
(PTH 77.15 — 22.85 % miss, zero crit); its **strongest** is `nemesis_wendigo_01` @ w160 lv109
(PTH 99.98 — 0.02 % miss, 9.98 % crit; the only body on the board that is one-fiftieth of a point
from unmissable). The player's **hardest target** is that same `nemesis_wendigo_01` (p→m PTH 103.54,
13.54 % crit); the **softest** is `chthoniandevourer_a01` @ w157 lv102 (PTH 124.89, **34.89 %** crit
mass, of which 4.89 points are ×1.3).

**Read plainly:** on this board the player's to-hit roll is a formality and roughly a quarter of
their swings crit; the board's swings land seven times in eight and essentially never crit. A
per-swing multiplier of **0.874 inbound vs 1.036 outbound** is a **1.19× structural offense
advantage to the player** before a single damage magnitude is considered — and it is entirely a
consequence of OA/DA, not of the damage tables.

---

## 5 — HONEST GAPS

### 5.1 ABSENT — none

Both Part-A terms resolved on every halt-list record. The empty ABSENT list is a real result, not
an omission: § 1 explains why (the bio hop always resolves) and § 2.3 explains why the own-TDM term
is never zero (`damage_totaladjuster` is universal on this board).

### 5.2 UNDECIDED — one, named

**U-O-1 · The composition of +% Critical Damage with the tier multiplier.** The player's sheet
carries **+57 % Critical Damage**; the wave-160 survival record carries
`offensiveCritDamageModifier[159] = +27 %` on the monster side. The Grim Dawn Wiki says only that
"+% Critical damage will be added to PTH Threshold multipliers" — which admits **two** readings:

* **(a) additive on the whole multiplier:** `1.1 → 1.1 + 0.57 = 1.67`
* **(b) additive on the crit BONUS only:** `1.1 → 1 + 0.1×(1+0.57) = 1.157`

I could not settle this from the records: `offensiveCritDamageModifier` is stored as a bare
percentage with no composition rule beside it, and `combatformulas.dbr` carries no equation for it.
**Both readings are named; neither is imputed.** Every crit-tier column in `pm4o_oa_da.csv` is the
**base** tier multiplier, and `wave_crit_damage_modifier_pct` rides beside it so a consumer can
apply whichever rule it can justify. The reading matters: at the player's 25.46 % crit mass, (a)
raises E[mult] from **1.0363** to **1.1814** while (b) raises it to **1.0570**.

This is the only UNDECIDED in the lap. **PTH itself, and the hit/miss split, are decided in both
directions for all 95 bodies.**

### 5.3 Deliberately out of scope (stated so it is not mistaken for a gap)

Flat-vs-% decomposition of the player's 1,396.5 OA-unit and 881 DA-unit gear residuals (the sheet
reports totals; the totals are what PTH consumes). Wave 150 (not in the frozen 20-wave roll).
DA-reduction debuffs the player's own skills apply beyond Shifting Sands. Any monster-side
avoidance layer (the player's is 0/0/0 per Lap A frame 519).

---

## 6 — ⚑ THE LEVEL-BASIS DIVERGENCE (a finding, not a nuisance)

Two level bases exist for this roster and **they disagree for 175 of 344 actors**:

* **Primary (used for the headline):** the frozen roster's own per-actor `level` — a spawn property
  of the roll, the same class of field as `record_path` and `wave`. Lap M confirmed **109** for the
  wave-160 nemesis against the referent's own on-screen monster banner.
* **Secondary:** Lap D's INDEX-PAIRED pool-proxy law (`lv7_uber hero` → {106,107,108}, etc.,
  `APL_B_PRIME = 103.4`).

| agreement | actors |
|---|---:|
| AGREE | 169 |
| **DIVERGENT** | **175** |
| no proxy | 0 |

⚑ **Every single divergence is a roster level of exactly 109 where the proxy law would place the
body lower** — 186 of 344 actors carry level 109, including **98 trash** actors the proxy law would
place at 102–107. 109 is the ceiling. This has the shape of a **level clamp or ceiling promotion in
the roster roll**, and it is reported as an observation, not diagnosed: I decoded the substrate, not
the roller.

**Neither basis is discarded.** Every Part-A row carries `dex_total_at_proxy_lo/hi`,
`int_total_at_proxy_lo/hi`, `own_tdm_at_proxy_lo/hi`; every Part-B row carries
`OA_at_proxy_lo/hi`, `DA_at_proxy_lo/hi` and PTH at both bounds. **The sensitivity is small and
signed:**

| | baton-level minus proxy-low |
|---|---|
| monster → player PTH | +0.00 … **+1.27 median** … +4.30 |
| player → monster PTH | −3.75 … **−1.20 median** … 0.00 |

i.e. the higher level basis makes the board slightly better at hitting the player and slightly
harder for the player to crit — a **shift of roughly one PTH point either way**. It moves no
qualitative conclusion in § 4.3: under the proxy basis the player still cannot miss any body on the
board, and the board still never reaches a second crit tier.

---

## 7 — VERIFICATION (`pm4o_verify_2026_08_14.py`, ALL PASS)

Six checks, each on a path that does not reuse the emitting code path:

| | check | result |
|---|---|---|
| V1a | every attr-halted record (154) has ≥ 1 emitted row | **PASS** |
| V1b | every own-halted record (104) has ≥ 1 emitted row | **PASS** |
| V1c | row count == roster actor count | **PASS** 344 vs 344 |
| V2 | per-record actor counts reproduce the i14 gate's own counts | **PASS** 0 / 104 mismatches |
| V2b/c | attr-halted 321 actors · own-halted 193 actors | **PASS** exact |
| V3 | attribute equations re-read straight out of the archive and re-evaluated | **PASS** 1,032 comparisons, max │Δ│ = **1.14e-13** |
| V4 | PTH re-derived by textually substituting OA/DA into the record's OWN `probabilityToHitEquation` **string** and `eval`-ing it | **PASS** 190 comparisons, max │Δ│ = **4.89e-05** (= the CSV's own 4-dp half-ULP, 5.0e-05) |
| V5 | every tier distribution conserves probability mass | **PASS** max │Δ│ = **0.000e+00** pct-points |
| V6 | OA/DA re-derived by `eval`-ing the record's own ability-equation **strings** | **PASS** 190 comparisons, max │Δ│ = **5.00e-05** (4-dp half-ULP) |
| V7 | own-TDM total cross-checked against Lap I's independently-written `own_total_damage_modifier` walk (column `own_tdm_lapI_crosscheck`) | **AGREE 344 / 344** |

V4 and V6 are the strong ones: they never call this lap's Python transcription of the formulas —
they substitute numbers into the game's own equation strings and evaluate those. The formulas in
`pm4o_lib` are therefore verified against the substrate, not merely self-consistent.

**Determinism:** the emitter was run twice; both CSV digests were byte-identical.

---

## 8 — DIGESTS (GL-6, FULL 64-hex, never truncated)

| artifact | rows | cols | sha256 |
|---|---:|---:|---|
| `pm4o_trash_terms.csv` | **344** | 58 | `fa75bc775aec80f926ad3bc272bd529a674cfe64dd375d909522e6b9fdf809ff` |
| `pm4o_oa_da.csv` | **96** | 82 | `5c55998d0127ed776f8130d530fe02e035c17d7070dfe0e3fe7565a9b02cc564` |
| `pm4o_digests.json` | — | — | `075b31c05f0022f60d4f4d86a4f45ad28889a415f7050c1b9c50e767b5d02bfc` |

**Inputs:**

| input | sha256 |
|---|---|
| `kc2-pm4-i14-findings-20260814_094018.json` (keys read: `⚑ data_gate` only) | `a3c6264cce97e42fbc5cfc2929b174b06c5da70d269f60b01306d4715588017c` |
| `kc2-baton-v1-E-s09-cp150-20260809_052836.json` (roster fields only) | `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` |

Instrument digests are recorded in `pm4o_digests.json :: instruments`.

---

## 9 — SOURCE LIST

**Primary — game substrate (read-only):**
* `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` — `database/database.arz`,
  `gdx1|gdx2|gdx3/database/*.arz`, `survivalmode1|2|3/database/*.arz`, `database/templates.arc`
* `records/game/combatformulas.dbr` [archive `base`] — every equation in § 3.1
* `records/game/balancingadjustment_survivalmode_enemies03.dbr` — the 200-cell wave arrays
* `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` — the Ultimate/solo pak, cell [8]
* `records/creatures/enemies/bios/*.dbr` — 101 distinct bio records, the attribute equations
* `records/skills/nonplayerskills/passive/damage_totaladjuster.dbr`, `armorbase01..05.dbr` — the
  own-total-damage grants

**Primary — official documentation:**
* Grim Dawn official guide, *Gameplay → Combat* — https://www.grimdawn.com/guide/gameplay/combat/
  (accessed 2026-08-14) — the PTH equation, the 55 floor, "cannot miss at 100", the PTH/70 rule,
  the crit-at-90 rule

**Secondary — community mechanics writeups (used ONLY for the crit-mass rule, § 3.2, and labelled):**
* Grim Dawn Wiki, *Game Mechanics* — https://grimdawn.fandom.com/wiki/Game_Mechanics
* *Grim Dawn — Game Mechanics Guide*, Steam id 596728673 —
  https://steamcommunity.com/sharedfiles/filedetails/?id=596728673

**Own prior laps (imported, not re-derived):** Lap A (player sheet), Lap D (level sets, summon
closure), Lap G (played-save kit), Lap I (wave/pak damage terms, `own_total_damage_modifier`),
Lap M (`.arz` chain, armour law, the player defence sheet).
