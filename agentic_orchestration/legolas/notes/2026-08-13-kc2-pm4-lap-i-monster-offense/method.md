# KC2-PM4 · Lap I · METHOD — the monster-OFFENSE limb + the band-C extension

> **Run:** KC2-PM4 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Ruling:** R-PM4-14 (charter L-12)
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> **Laws:** READ-ONLY on every source · **GL-12 decode-never-estimate** · **NOTE-9** every quantity
> asserts its basis · **OUTCOME-FIREWALLED** (§ 0.2)

---

## 0 — Preliminaries

### 0.1 What this lap is

Ruling R-PM4-14 resolves the substrate boundary by **extension, not exhaustion**. Lap D gave the
band-B monsters their *bodies* back and declared `damage_grade = NOT-IN-SCOPE` on all 791 rows
(cliff **C-D4**). This lap is the other limb: **what the monsters HIT WITH**, plus the band past
wave 170 that cliff **C-D2** parked.

Four targets, four decodes. Each is graded MEASURED with a named file / record / field / index, or
graded as a **declared gap**. Nothing is interpolated. Where a decode ran out, § 5 says so.

### 0.2 The firewall, stated precisely

This lap read **no** sim output, **no** findings JSON, **no** gamora landing note, **no** baton
produced after the frozen roster roll. The single baton it reads is
`kc2-baton-v1-E-s09-cp150-20260809_052836.json`, which is a **roster basis** — which record was
drawn at which wave — and is the same basis Lap D used. It is not a sim outcome.

Sources, exhaustively:

| source | what for |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (8 `.arz` archives) | every magnitude |
| `…/resources/Text_EN.arc :: tags_ui.txt` | DoT **display names** and the two convention strings in § 5.1 |
| `reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv` | pool/roster basis (a legolas pe6 emission — **re-verified against the proxy `.dbr` records here**, § 4.2) |
| `…/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` (`actors[]` only) | the rolled 151–160 population |
| Lap D's own emissions | **positive control only** (§ 6.1) |

### 0.3 Instruments

`agentic_orchestration/research/scripts/`:
`pm4i_lib_2026_08_13.py` · `pm4i_emit_2026_08_13.py` · `pm4i_verify_2026_08_13.py` ·
`pm4i_bandc_spawn_2026_08_13.py` · `pm4i_boarddot_2026_08_13.py`. Logs: `emit.log`, `verify.log`,
`spawn.log`. Machine summaries: `pm4i_emit_summary.json`, `pm4i_verify_summary.json`,
`pm4i_bandc_spawn_summary.json`.

The life chain is **imported**, never re-implemented — `resolve` / `Chain` / `ev` from
`gamora_kc2_c1_closure_ed3_2026_08_08.py`, `lv_formula_table` / `floor_set` / `pool_slot_proxies` /
`APL_B_PRIME` from `gamora_kc2_stat_fold_ed3_2026_08_08.py`, and `summon_closure_extended` /
`is_body` from my own `pm4d_lib_2026_08_13.py` (Lap D, with IS-B2 / IS-B3 already fixed). Reader is
`Ed.winner()` — **whole-record replacement**, the L-33 / C-9 overlay law — never `merged()`.

---

## 1 — TARGET 1: the wave-G DAMAGE modifier · **MEASURED**

**Deliverable:** `pm4i_wave_damage_modifier.csv` (50 rows × 34 cols, waves 151–200) ·
companion `pm4i_survival_wave_arrays_full.csv` (1,350 rows — every array field × every wave, long
form, so nothing is hidden by my column selection).

### 1.1 The decode

The paired damage modifier is on **the same record Lap D read the life modifier from**:

```
records/game/balancingadjustment_survivalmode_enemies03.dbr        [archive sm_mod]
  .offensiveTotalDamageModifier   — 200 cells, read at index w-1
```

That record carries **27** arrays of length > 1, all 200 cells, all wave-indexed under the same
**§ 10.7 / L-33 array-lookup law** Lap D established (fighting wave `w` reads the cell **labelled**
`w`, i.e. index `w-1`). `surv_at` is **total on [1, 200] with no clamp** — the same refusal-to-
extrapolate `G_at` carries.

| wave | `offensiveTotalDamageModifier` | Ultimate `[8]` | **additive sum** | `G` (life, cross-check) |
|---:|---:|---:|---:|---:|
| 151 | 42.0 | 40.0 | **82.0** | 306.0 |
| 159 | 43.0 | 40.0 | **83.0** | 322.0 |
| **160** | **43.0** | **40.0** | **83.0** | 324.0 |
| 170 | 45.0 | 40.0 | 85.0 | 344.0 |
| 171 | 56.0 | 40.0 | 96.0 | 420.0 |
| 180 | 75.0 | 40.0 | 115.0 | 510.0 |

### 1.2 ⚑ The finding that re-frames the target

**The Crucible's damage modifier is FLAT where its life modifier is steep.** Over the reference
band the damage term moves **+42 → +43 %** (ten waves, one point) while `G` moves **+306 → +324 %**.
Across the whole ladder the damage array runs 0 → +130 % while life runs +95 → +990 %.

And, measured across the three Crucible difficulty paks:

> `offensiveTotalDamageModifier` is **byte-identical on `enemies01`, `enemies02` and `enemies03`**
> (Aspirant / Challenger / Gladiator). **Crucible difficulty scales monster LIFE and does not
> scale monster DAMAGE at all.**

(`enemies01/02/03.characterLifeModifier` at wave 160 = 118 / 229 / **324**; the damage array is the
same 200 cells in all three. `emit.log`, `damage_array_identical_across_crucible_difficulties`.)

Lap D's difficulty-of-record choice was **re-checked from this seat, not carried**: `enemies03`
reproduces G(150/160/170) = 304 / 324 / 344.

### 1.3 The rest of the offense surface, all MEASURED

| field @ w160 | value | reading |
|---|---:|---|
| `offensiveCritDamageModifier` | +27.0 % | 27 → 33 across the ladder |
| `characterOffensiveAbility` | +50.0 % | + Ultimate flat +50.0 |
| `characterOffensiveAbilityModifier` | +3.5 % | + Ultimate **−8.0** |
| `characterAttackSpeedModifier` | +11.0 % | + Ultimate 0.0 |
| `characterSpellCastSpeedModifier` | +11.0 % | + Ultimate **+5.0** |
| `skillCooldownReduction` | 0.0 % | first non-zero at wave 180 |
| `retaliationTotalDamageModifier` | +74.0 % | + Ultimate −15.0 |
| `offensivePhysicalModifier` | **−21.0 %** | negative, deepening to −50 at w200 |
| `offensiveSlow*Modifier` (all 7 DoT types) | **−63.0 %** | see § 3.4 |

### 1.4 Grade on the composition rule — read this

The **three terms** are each MEASURED (named record, named field, named index). That they
**combine additively** is asserted **by parallel with the life chain** (L-65: "the life stack is
ADDITIVE-within-field"), and is **not independently measured on the damage field**. Every summed
column therefore carries the grade string
`DERIVED-SUM-ADDITIVE-BY-PARALLEL`, and the components ride beside it so a consumer can recombine
under a different rule. This is a *named* soft joint, not a hidden one.

The third additive term — the creature's own granted `offensiveTotalDamageModifier` — is decoded
per record by `own_total_damage_modifier()`, the exact structural parallel of `Chain.passive_pct`.
Worked example (`verify.log` V7), `nemesis_wendigo_01` at L = 109:

```
ultimate 40.0  +  wave 43.0 (w160)  +  own 109.0  =  192.0 %
own sources:  damage_totaladjuster.dbr[10] = 44.0 · armorbase05.dbr[108] = 25.0 · wendigo_enrage.dbr = 40.0
```

---

## 2 — TARGET 2: the Ultimate difficulty offense paks · **MEASURED**

**Deliverable:** `pm4i_ultimate_offense_paks.csv` (733 rows — 61 arrays × 12 cells + the non-zero
scalars).

**Record:** `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` [archive `base`],
**`Class = AttributePak`** — the game's own word for the thing the commission asked for.

### 2.1 The 12-cell layout, DECODED not assumed

`characterLifeModifier = [50 ×4, 320 ×4, 580 ×4]` fixes the outer block as **difficulty**
(Normal / Elite / Ultimate) and Lap D's `580.0` fixes cell **[8]** as the first Ultimate cell.
`characterLifeMultModifier = [0, 90, 180, 270] ×3` — the multiplayer life scaling — fixes the inner
index as **player count 1…4**. So **cell [8] = Ultimate, 1 player**, which is what Matt played.

### 2.2 Ultimate / solo offense cells, in full

| field | `[8]` | | field | `[8]` |
|---|---:|---|---|---:|
| `offensiveTotalDamageModifier` | **+40.0** | | `offensiveSlowPoisonModifier` | **−28.0** |
| `characterOffensiveAbility` | **+50.0** | | `offensiveSlowBleedingModifier` | −28.0 |
| `characterOffensiveAbilityModifier` | −8.0 | | `offensiveSlowFireModifier` | −28.0 |
| `characterAttackSpeedModifier` | 0.0 | | `offensiveSlowColdModifier` | −28.0 |
| `characterSpellCastSpeedModifier` | +5.0 | | `offensiveSlowLightningModifier` | −28.0 |
| `offensivePhysicalModifier` | 0.0 | | `offensiveSlowLifeModifier` | −28.0 |
| `offensivePierceModifier` | 0.0 | | `offensiveSlowPhysicalModifier` | −28.0 |
| `offensiveAetherModifier` / `ChaosModifier` / `LifeModifier` | 0.0 | | `offensiveSlowLifeLeachModifier` | 0.0 |
| `offensiveStunModifier` | +25.0 | | `offensiveSlowDamageMultModifier` | **+40.0** |
| `offensiveFreezeModifier` / `PetrifyModifier` / `TrapModifier` | +10.0 | | `retaliationTotalDamageModifier` | −15.0 |

Scalar (not difficulty-indexed): `defensiveReflect = −5.0`.

**⚑ The shape of Ultimate:** every *instant* elemental modifier is **0** on Ultimate (they are −20
on Normal), while every *duration* (DoT) modifier is **−28**. Ultimate's monster-offense boost is
delivered almost entirely through the single `offensiveTotalDamageModifier = +40` term, its
crowd-control terms (`Stun +25`, `Freeze/Petrify/Trap +10`), and `+50` flat Offensive Ability —
**not** through per-type damage.

---

## 3 — TARGET 3: DoT riders on the waves-151–160 board · **MEASURED**, with one declared gap

**Deliverables:** `pm4i_dot_riders.csv` (264 rows × 39 cols) ·
`pm4i_terminal_wave_dot_ranking.csv` (9 rows) · `pm4i_board_dot_by_wave.csv` (10 rows).

### 3.1 Population (NOTE-9)

| id | basis | n |
|---|---|---:|
| **P-ROLLED-10** | frozen baton `actors[]`, wave ∈ [151,160] | **188 actors / 91 records** |
| **+ summon closure** | `summon_closure_extended` (IS-B2/IS-B3 restored), to fixpoint, layers [36, 2] | **+38 pet bodies = 129 bodies** |
| bodies carrying ≥ 1 DoT component | | **90** (71 roster + 19 pet) |
| bodies MEASURED-ZERO on DoT | level present, no DoT field on any skill in the closure | **37** |
| bodies with **no level source at all** | declared gap, § 5.2 | **2** |

`188` and `91` reproduce Lap D's P-ROLLED-10 exactly. `actors ≠ records` throughout and every
count says which it is.

### 3.2 The instrument

For each body, the **full skill closure** is walked to fixpoint (`skill_closure`, depth ≤ 8):

- **depth 0** = the creature's own `skillName{i}` / `skillLevel{i}` pairing. Rank =
  `int(ev(skillLevel_i, L))` — **the identical expression the life chain evaluates**, so a DoT rank
  and a life-passive rank on the same slot are read at the same index. Graded `MEASURED-RANK`
  (243 rows).
- **depth > 0** = nested `buffSkillName` / `autoCastSkill` / `petSkillName` / `skillName{i}` on a
  skill record. These carry no rank of their own; the referring skill's rank is propagated and the
  row is graded **`DERIVED-INHERITED-RANK`** (21 rows). **This is a model choice about rank
  propagation, not a decode**, and it is on the row so a consumer can filter it out.
- `spawnObjects*` targets are **not** followed here — a spawned body is a separate body with its
  own life and skills, and enters through the summon closure instead. No body is double-counted.

Levels: the record's own pool level set (index-paired slot law, `APL_B_PRIME = 103.4`) —
`MEASURED-SET` on 229 rows; a summon inherits its summoner's set — `DERIVED-INHERITED` on 35.
Magnitudes are emitted at **both** the LO and HI level limbs.

### 3.3 The eight DoT families decoded, with display names read from the game's own text

Display strings decoded from `resources/Text_EN.arc :: tags_ui.txt`, never spelled from memory:

| stem | tag | display | rows |
|---|---|---|---:|
| `offensiveSlowPoison*` | `DamageDurationPoison` | Poison Damage | 66 |
| `offensiveSlowBleeding*` | `DamageDurationBleeding` | Bleeding Damage | 49 |
| `offensiveSlowFire*` | `DamageDurationFire` | Burn Damage | 30 |
| `offensiveSlowLife*` | `DamageDurationLife` | Vitality Decay Damage | 18 |
| `offensiveSlowCold*` | `DamageDurationCold` | Frostburn Damage | 14 |
| `offensiveSlowPhysical*` | `DamageDurationPhysical` | Internal Trauma | 10 |
| `offensiveSlowLightning*` | `DamageDurationLightning` | Electrocute Damage | 6 |
| `offensiveSlowLifeLeach*` | `DamageDurationLifeLeach` | Life Leech | 5 |
| `offensivePoison*` (**instant**) | — | **Acid** — `is_dot = False` | 66 |

**The commission says "poison/acid". In this corpus they are two different fields**: `DefensePoison`
= "Poison **&** Acid Resistance" is one resistance, but ACID is the *instant* `offensivePoison*`
family and POISON is the *over-time* `offensiveSlowPoison*` family. Both are emitted; `is_dot`
separates them and every ranking uses `is_dot = True` only.

**Deliberately EXCLUDED and named** (same `offensiveSlow*` prefix, not damage):
`TotalSpeed`, `RunSpeed`, `AttackSpeed`, `CastSpeed`, `OffensiveAbility`, `DefensiveAbility`,
`OffensiveReduction`, `DefensiveReduction`, `DamageMult`, `ManaBurn`.

### 3.4 ⚑ The Crucible SUPPRESSES monster DoT, hard

| term | w160 | basis |
|---|---:|---|
| `survivalmode_enemies03.offensiveSlowPoisonModifier[159]` | **−63.0 %** | wave term |
| `mp+difficulty_enemies01.offensiveSlowPoisonModifier[8]` | **−28.0 %** | Ultimate/solo |
| additive sum (grade: `DERIVED-SUM-ADDITIVE-BY-PARALLEL`) | **−91.0 %** | |

Identical −63 / −28 on all seven DoT types. Meanwhile the same two records give **+43 / +40** on
`offensiveTotalDamageModifier`. **On the wave-160 board, Crucible + Ultimate together push
instant damage UP by +83 points and pull damage-over-time DOWN by −91 points.** Whether
`offensiveTotalDamageModifier` *also* applies to DoT is engine behaviour and is **not in the
record** — see § 5.3.

### 3.5 The terminal-wave ranking (waves 159 + 160), MEASURED

Per-body DoT load, each body's own summon closure included, at the LO level limb:

**Wave 159** (9 actors, 5 records):

| # | record | actors | families | Σ dps *if total* | Σ dps *if per-second* | heaviest single |
|---:|---|---:|---|---:|---:|---|
| **1** | `humanwendigo_darkwood_01` | 2 | Bleeding · Vitality Decay · Life Leech | **1,560.9** | 2,772 | Bleeding 641 / 3.0 s |
| **2** | `chthonianservitor_lunalvalgoth` | 2 | Bleeding | **1,453.3** | 2,611 | Bleeding 923 / 1.0 s |
| **3** | `skeletalgolem_stepsoftorment_01` | 2 | Burn · Vitality Decay | 539.6 | 1,306 | Burn 396 / 2.0 s |
| 4 | `korvaakmessenger_02b` | 1 | Burn | 386.8 | 1,325 | Burn 667 / 3.0 s |
| 5 | `witchgod_finalboss` | 2 | Poison · Life Leech | 358.2 | 1,478 | **Poison 890 / 5.0 s** |

**Wave 160** (5 actors, 4 records):

| # | record | actors | families | Σ dps *if total* | Σ dps *if per-second* |
|---:|---|---:|---|---:|---:|
| **1** | `nemesis_wendigo_01` | 1 | Bleeding · Life Leech | **650.0** | 1,040 |
| **2** | `statue_korvaaktombguardian` | 2 | Frostburn · Electrocute · **Poison** | 423.9 | **1,778** ← #1 on the other convention |
| 3 | `nemesis_aetherialvanguard_01` | 1 | Burn | 114.8 | 780 |
| 4 | `nemesis_kymon_01` | 1 | Burn | 85.6 | 428 |

**Convention sensitivity, measured and reported rather than smoothed** (§ 5.1): top-3 intersection
is **2/3 at wave 159** and **3/3 at wave 160**, with **2 rank flips in each**. At wave 160 the #1
slot itself flips (`nemesis_wendigo_01` ↔ `statue_korvaaktombguardian`). **The verdict "which body
is #1 on wave 160" is CONVENTION-DEPENDENT and I do not assert it.** The verdict "these two are
the wave-160 DoT carriers" is stable and I do assert it.

### 3.6 ⚑ Wave 159 is the DoT spike — and it is BLEEDING, not poison

`pm4i_board_dot_by_wave.csv`, actor-weighted over the whole rolled board:

| wave | actors | board DoT (if-total) | **per actor** | poison | bleeding |
|---:|---:|---:|---:|---:|---:|
| 151 | 28 | 3,622 | 129 | 1,149 | 2,215 |
| 152 | 18 | 4,559 | 253 | 3,240 | 0 |
| **153** | 24 | **12,924** ← board peak | 538 | **7,998** ← poison peak | 3,295 |
| 154 | 13 | 5,443 | 419 | 0 | 2,505 |
| 155 | 18 | 6,295 | 350 | 3,280 | 0 |
| 156 | 19 | 6,307 | 332 | 4,300 | 1,590 |
| 157 | 21 | 3,999 | 190 | 959 | 1,745 |
| 158 | 33 | 3,836 | 116 | 848 | 1,429 |
| **159** | **9** | 8,211 | **912** ← per-actor peak, 1.7× the next wave | 559 | **5,309** |
| 160 | 5 | 1,698 | 340 | 404 | 181 |

Matt's banked testimony is *"some kind of poison/dot seemed to effect me in a major way on my last
wave"*. The measured answer, stated exactly:

- **The DoT-per-body spike on the terminal waves is REAL and it is on wave 159** — 912 per actor,
  1.7× wave 154's 419 and 2.7× wave 160's 340. Nine bodies carrying a board's worth of DoT.
- **Its dominant family is BLEEDING (5,309 of 8,211 = 65 %), not poison (559 = 7 %).**
- **Poison's actual board peak is wave 153** (7,998), six waves earlier.
- The *only* poison on the terminal pair is `witchgod_finalboss` (890 / 5.0 s, wave 159) and
  `statue_korvaaktombguardian` (wave 160).

I report the discrepancy; I do not reconcile it. "Poison" in player testimony may well name the
*sensation* of a DoT rather than the damage type, and that is a judgement for the conductor.

---

## 4 — TARGET 4: band C (waves 171–180) · **MEASURED** — and C-D2 resolves

**Deliverables:** `pm4i_band_c_ehp_by_wave.csv` (4,010 rows) · `pm4i_band_c_roster.csv` (410 rows) ·
`pm4i_band_c_wave_composition.csv` (50 rows, bands B and C side by side).

### 4.1 The band exists in the substrate. It always did.

Lap D's band stopped at wave 170 because **the frozen baton stops there**
(`arena_tier_exhausted`), **not because the corpus does**:

- `records/proxies/tier01waves` … **`tier20waves`** — **20 content tiers × 10 waves = 200 waves**,
  enumerated from the archive index, not assumed.
- `wave_engine.MAX_WAVE = 200` (R-KC2-4 / U-8, already closed).
- `pe6_crucible_wave_pools_v2.csv` carries `global_wave` **1 … 200**.
- The survival arrays are **200 cells**; `G(171) = 420` … `G(180) = 510` are real cells of the same
  array Lap D read, at the same index law.

So band C is a **decode**, not an extrapolation, and `surv_at` still refuses to read past 200.

### 4.2 The pool basis was re-verified, not inherited

`pe6_crucible_wave_pools_v2.csv` is my own earlier emission. For band C, every distinct
`(proxy_record, pool_record)` pair over waves 171–180 was re-checked against the proxy `.dbr`'s own
spawn-pool references: **112 confirmed / 0 not-confirmed of 112**.

### 4.3 Coverage and residuals

| | |
|---|---:|
| band-C pool records (waves 171–180) | **331** over 98 pools |
| + summon closure to fixpoint (layers [74, 5]) | **410 bodies** |
| `life_grade = MEASURED` | **401 / 410 = 97.8 %** |
| named gaps | **9** — all listed below, all zero-magnitude |
| structural: monotone-in-wave violations · negative eHP · `hi < lo` | **0 · 0 · 0** |

**The nine named gaps, in full** (`verify.log` V4):

| record | reason |
|---|---|
| `boss&quest/wight_scarfelldepths_01/02/03.dbr` | **`RECORD-ABSENT`** — cited by a band-C pool, **present in no Edition-III archive**. Three bodies the Crucible's own tables reference and the corpus does not contain. |
| `chthonianabomination_tentacles_a01` · `chthonianfiend_a01_summon` · `korvaakservant_b01/b02_korvaaksummon` · `swampcrab_a00_summon` | `NO-LEVEL-SOURCE` — summon bodies whose summoner is itself a summon with no pool level set |
| `skills/nonplayerskills/summoning/warden_aethertrap01.dbr` | `NO-characterAttributeEquations` — the band-C analogue of Lap D's `krieg_aethertrap.dbr` (C-D3), same shape, same trap family |

All nine are emitted as rows with **empty magnitude columns**. No sibling fill, no modal fill, no
interpolation.

### 4.4 The eHP surface

| | wave 171 | wave 180 |
|---|---:|---:|
| bodies | 401 | 401 |
| min / median / max eHP (LO limb) | 165 / 488,757 / 4,216,311 | 178 / 525,081 / 4,531,746 |
| Σ eHP | **320,798,692** | **344,777,998** |

Each row also carries `D_total_damage_modifier_pct` and the per-record
`total_damage_modifier_pct_lo/hi` so band C ships with **both** limbs, unlike band B.

### 4.5 ⚑ C-D2 RESOLVED: 171 is a REGIME STEP, not a scaling break or a loop

The question C-D2 parked was whether `G(171) = 420` (a +76 jump from 344) means waves 171+ are a
different *regime*. Measured across **every** tier boundary on the ladder (`verify.log` V6):

```
(wave, ΔLife, ΔDamage) at each tier boundary:
 (11,0,0) (21,0,0) (31,2,0) (41,1,0) (51,3,0) (61,1,0) (71,1,0) (81,1,1) (91,2,1)
 (101,1,1) (111,2,1) (121,2,0) (131,3,0) (141,4,0) (151,2,0) (161,2,1)
 (171, 76, 11)   (181, 46, 11)   (191, 65, 6)
```

**The verdict:** the boundary at 171 is **the same 200-cell arrays and the same `tier<NN>waves`
authoring structure** — no loop, no wrap, no missing table. But it is unambiguously a **regime
step**, and it is the *first* one on the ladder: every boundary from 11 to 161 steps life by 0–4
points; 171 steps it by **76**, and 181 and 191 continue at 46 and 65. The **within-band** slope
changes too: life +2.0/wave over 151–170 → **+10.0/wave** over 171–180; damage +0/+1 per wave over
151–170 → +1/wave with an **+11 step at the boundary**.

The roster turns over hard as well: **wave-170 pool records 23 · wave-171 pool records 47 · shared
only 8**; over the bands, 466 band-B pool records drop and 134 are new in C. Wave 170 is
`BOSS`-only; wave 171 is `BOSS | HERO | trash`.

**So: decodable, decoded, and materially different. A consumer that linearly extended band B past
170 would have understated life by 22 % at wave 171 and by 48 % at wave 180.** The table's refusal
to extrapolate was correct.

---

## 5 — DECLARED GAPS (GL-12: a measured negative is a finding; an estimate is not)

### 5.1 ⚑ DECLARED GAP — the DoT magnitude convention (total-over-duration vs per-second)

`offensiveSlowPoisonMin[rank] = 890` with `offensiveSlowPoisonDurationMin = 5.0`. Is 890 the
**total** dealt over 5 s (→ 178 dps), or the **per-second** rate for 5 s (→ 890 dps)? The `.dbr`
does not say, and I could not decide it from substrate. I looked, and here is exactly what I found
in `Text_EN.arc :: tags_ui.txt`:

| tag | string | what it decides |
|---|---|---|
| `tagCharStatsPoisonAbsDmgInfo` | "The Poison Damage done **per second** over 5 seconds applied per hit with your weapon attacks" | the **character-sheet** stat is a per-second rate |
| `tagCharStatsPoisonDurationInfo` | "The percent bonus to the duration of your Poison Damage attacks. **The damage per second is not increased.**" | duration bonuses extend the window at fixed dps |
| `DamageDurationPoison` + `DamageSingleFormatTime` | "{value} Poison Damage" + " over {dur} Seconds" | the **tooltip** is silent on which the value is |

These constrain the *display*; **none of them pins the `.dbr` field**. Writing an ARC/format-string
evaluator to settle it would be a separate lane.

**How this is handled, rather than guessed:** every DoT row carries `magnitude_min_lo`,
`duration_min_s`, **and both** `dps_if_field_is_total_lo` and `dps_if_field_is_per_second_lo`. Every
ranking is emitted **twice**, once per convention, and § 3.5 reports where the two disagree. Where
they agree the verdict is asserted; where they disagree it is not. **The gap is bracketed, and the
bracket is at most a factor equal to the duration (1–8 s in this population).**

### 5.2 DECLARED GAP — two DoT bodies with no level source

`chthonianfiend_a01_summon` (summoner `chthonianminion_b01_summon`) and `insectswarm_a01_summon`
(summoner `bonerat_witchgod_b01_summon`). Both resolve a life chain (`chain = OK`) but neither they
nor their summoners are in a band-B pool, so there is **no measured level set** to evaluate their
skill-rank equations at. Rather than fill from a sibling or a modal level, they are **excluded from
the DoT emission and named here**. They are 2 bodies of 129, both second-order summons, and neither
is on the terminal waves.

### 5.3 UNDECODABLE-FROM-SUBSTRATE — DoT stacking semantics

The commission asks for "stacking rule if decodable". **It is not decodable from the records.**
What the `.dbr` *does* carry, and is emitted per row: `offensiveSlow<X>Chance`,
`offensiveSlow<X>Global`, `offensiveSlow<X>XOR`, `offensiveSlow<X>Modifier`,
`offensiveSlow<X>DurationModifier`. What it does **not** carry anywhere: a stack count, a
same-source replacement rule, or a refresh-vs-extend rule. Those live in the engine binary. Every
DoT row therefore carries the literal grade string

> `UNDECODABLE-FROM-SUBSTRATE — the .dbr carries Chance / Global / XOR / DurationModifier but no
> stack-count or same-source-replacement rule; the semantics live in the engine, not the record`

Only **6 of 264** rows carry a `Chance` at all (18–30 %); the rest are unconditional-on-hit. Two
rows carry a skill-level `Modifier` / `DurationModifier`
(`passiveproperties_aetherialbloater`: Poison +10 % dmg / +33 % duration;
`passiveproperties_dranghoulchampion`: Bleeding +30 % / +15 %).

### 5.4 UNDECODABLE-FROM-SUBSTRATE — whether `offensiveTotalDamageModifier` applies to DoT

`+83` points of total-damage modifier and `−91` points of DoT modifier are both on the board at
wave 160 (§ 3.4). Whether the former composes with the latter is an **engine application rule**,
not a record field. Not asserted. Both terms are emitted separately so either composition can be
run.

### 5.5 NOT DECODED — fire rate

The ranking is **damage-per-application**, not damage-per-second-of-combat. Cooldowns, cast times
and AI selection weights exist on the skill records but are not folded here; a body with a 12 s
cooldown and a body with a 1 s cooldown rank identically. This is a **scope statement, not a gap**:
the commission asked for magnitude / duration / stacking, and folding fire-rate would silently
convert a substrate decode into a behavioural model.

---

## 6 — Verification (`verify.log`, `pm4i_verify_summary.json`)

| # | check | result |
|---|---|---|
| **V1** | **POSITIVE CONTROL.** Band-C's life chain re-run at waves 151–170 against Lap D's `pm4d_band_b_ehp_by_wave.csv`, on Lap D's own declared level limbs, demanding EXACT integer agreement | **15,800 EXACT / 0 MISMATCH** of 15,801 rows (the 1 skipped is Lap D's declared zero-magnitude gap row). **PASS** |
| **V2** | wave-modifier table's `G` column vs Lap D's emitted life-modifier table, waves 151–170; Ultimate 580.0 on every row | **20/20 · True. PASS** |
| **V3** | INDEPENDENT RE-READ: 20 sampled DoT rows re-derived straight off the `.arz` bytes by a second code path (raw `ArzArchive`, no library helpers) | **20 EXACT / 0 mismatch. PASS** |
| **V4** | residuals NAMED, not counted: 9 band-C absences · 2 DoT no-level bodies · 37 MEASURED-ZERO bodies | listed in § 4.3 / § 5.2 |
| **V5** | terminal-ranking convention sensitivity quantified | § 3.5 — reported, not smoothed |
| **V6** | 170/171 regime, against **every** tier boundary on the ladder | § 4.5 |
| **V7** | the damage chain's three terms re-read at a named record | § 1.4 |
| — | band-C pool basis vs the proxy `.dbr` records | **112/112 confirmed** |
| — | structural: monotone / negative / limb-order violations on 4,010 band-C rows | **0 / 0 / 0** |

---

## 7 — Self-corrections banked openly (NOTE-9 / Discipline #11)

1. **My verify instrument crashed twice on Lap D's own declared gap row** — `pm4d_band_b_ehp_by_wave.csv`
   carries the `krieg_aethertrap.dbr` row with empty `wave` / `ehp_lo` (correctly — that is C-D3's
   named gap), and my first two `int()` calls assumed every row was populated. Patched to *skip and
   count* rather than coerce. Banked because the failure mode — an instrument that assumes a
   fully-populated table — is exactly the class of bug that turns a declared gap into a silent zero.
2. **My first DoT walk was one hop deep.** It reached the creature's `skillName{i}` slots only and
   would have missed every nested `buffSkillName` / `autoCastSkill` carrier — the same IS-B2 defect
   I found in band A's summon closure at Lap D, reproduced by me on the skill side one lap later.
   Caught by probing three bosses before emitting: `witchgod_finalboss` reaches 15 skills of which
   **3 are depth ≥ 1**. Fixed to a fixpoint closure with the inherited-rank grade on the row.
3. **I nearly ranked the terminal waves on one magnitude convention.** The instability is real
   (wave 160's #1 flips), and had I emitted a single ranking the conductor would have inherited a
   confident wrong ordering. Both conventions ship; the ordering claim is scoped to where they agree.
4. **I did not carry Lap D's difficulty-of-record choice.** `enemies03` was re-checked from this
   seat against G(150/160/170).

## 8 — Cliffs filed, not improvised past

- **C-I1 — the DoT magnitude convention (§ 5.1).** Closable by an ARC/format-string evaluator or by
  one controlled in-game observation. Until then every downstream DoT number must travel with its
  convention label. **Disposition: conductor.**
- **C-I2 — three band-C pool records absent from the corpus** (`wight_scarfelldepths_01/02/03`).
  The Crucible's own tables cite bodies Edition-III does not contain. Whether this is an
  Edition-III pin artifact or a genuine dangling reference in the shipped data is **not decided
  here**. **Disposition: conductor.**
- **C-I3 — the damage chain's additivity (§ 1.4)** is asserted by parallel with the life chain, not
  independently measured on the damage field. Closable by a controlled in-game reading; until then
  the components ride beside every sum.
- **C-I4 — pets and the damage fold.** Lap D's C-D1 (two folds on one board, life side) has a
  damage-side twin: this lap emits pet DoT at the pet's inherited level but does **not** rule
  whether the Crucible wave term and the Ultimate pak apply to a summoned body's *output*. Same
  open question, other limb. **Disposition: conductor.**

## 9 — Laws observed

- **READ-ONLY** on the vendor corpus, the engine tree and every baton. Writes are confined to this
  notes directory and `research/scripts/`.
- **OUTCOME-FIREWALLED** — sources enumerated exhaustively in § 0.2. No sim output was opened.
- **GL-12 decode-never-estimate** — every magnitude traces to a record + field + index. Three
  declared gaps (§ 5.1–5.3), two named-scope exclusions (§ 5.4–5.5), eleven zero-magnitude named
  gaps (§ 4.3, § 5.2). Nothing interpolated, nothing sibling-filled, nothing modal-filled.
- **NOTE-9** — five populations declared by name; every ratio says which one it is over; actors are
  never reported as records.
- **Instrument schemas declared** in the module docstrings.
- **Cliffs filed** (§ 8) rather than resolved by preference.
