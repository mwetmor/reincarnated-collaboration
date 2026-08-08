# KC2-SIM — named-HALT bundle micro-probe (L-19) — 2026-08-08

**Agent:** legolas (Mode A — analytical / primary-source probe)
**Conductor:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase B
**Commission:** conductor ruling **L-19** — seven named HALTs bundled into ONE micro-probe
**Disposition:** **7 of 7 addressed. 6 CLOSED · 1 PARTIAL-CLOSED · 0 escalated.**
**Commit:** NONE (charter § 4.7 — conductor commits at gate close)
**Scratch:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-halt-bundle/`

---

## 0 — Corpus provenance (MANDATORY)

**Read tree:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — the Edition-II pin.

| Archive | md5 | bytes |
|---|---|---:|
| `database/database.arz` | `20d47784be5f93124636992f9e5562e2` | 58 338 379 |
| `gdx3/database/GDX3.arz` | `08365db74863744fea2cfc7254666f55` | 47 334 429 |
| `mods/survivalmode/database/SurvivalMode.arz` | `ac4ad3539196ccf26b6f8be6ab7d3a8b` | 7 052 806 |

**The hazard, verified this session.** `/Users/admin/Games/vendor/grim-dawn/` (Edition-I full install)
**has no `gdx3/` directory at all** (`ls: No such file or directory`) and returns pre-FoA records
**silently** — no error, no warning, just an older number. Every `.arz` read in this note went through
the eight-archive Edition-II stack (`base → gdx1 → gdx2 → gdx3 → sm_mod → sm1 → sm2 → sm3`, last-wins).

**One disclosed exception — `templates.arc`.** The Edition-II pin ships **no `.arc` under `database/`**;
`templates.arc` exists **only** in the Edition-I tree (`/Users/admin/Games/vendor/grim-dawn/database/templates.arc`,
780 972 B, ARC v3, 819 `.tpl`). It was opened there, and a **FoA-freshness probe** was run before any
citation was taken from it: all 19 probed 1.3.0.0-era field names — `defensiveCrowdControl`,
`defensiveCrowdControlMaxResist`, `conversionInType`, `conversionPercentage`,
`characterManaLimitReserve(Modifier)`, `projectilePeriod`, `delayMovement`, `skillActiveDuration`,
`offensiveSlow*Modifier`, `defensivePercentCurrentLife`, `defensiveConvert`,
`retaliationTotalDamageModifier`, `offensiveTotalDamageModifier`, `offensivePhysicalModifier`,
`armorDefensiveAbsorption`, `playerRunSpeedCapMax`, `characterRunSpeed(Modifier)` — are **PRESENT**.
The schema is not stale for anything cited here. **Template citations are graded `TPL-CITED (Edition-I
archive, freshness-probed)`; every numeric value in this note comes from the Edition-II `.arz`.**
*(This is the same gap U-9 § flagged: the pin optimised for record content and dropped the archives
that carry record semantics. It should be added to the pin.)*

---

## 1 — FINDINGS TABLE (one read for the conductor)

| HALT | Verdict | Headline | Grade |
|---|---|---|---|
| **HALT-9** | **CLOSED** | Full 200×3 grain emitted. **33** non-zero fields (not ~35): **25 arrays, 8 scalars**. `offensiveTotalDamageModifier` **ramps hard** — the spec's +20 is a wave-100 slice; **wave 160 = +43, wave 200 = +130**. All 9 U-8 columns byte-identical. | DB-CITED |
| **HALT-9(b)** | **CLOSED — F-4 ADJUDICATED** | **Both sources are right at their own wave.** 08-01's "74 Glad / 53–54 lower" is the **wave-150–170 plateau**; P-E6's "+22/+24/+16" is **wave 100**. Ordering flips at **wave 112**. **No mismeasure needed; L-10(b) is not required to explain F-4.** | DB-CITED |
| **HALT-5** | **CLOSED — EXACT** | **982 = 982.** Missing source found: **Presence of Might (component skill) = 300 flat**. Divine Mandate **reserves ZERO**. Residual was rank-understatement, not missing skills. Unique solution over an 81-cell grid; cross-checked by EoR = 26. | DB-CITED + save-CITED |
| **HALT-4** | **PARTIAL-CLOSED** | Weapon term **CONFIRMED** (solved `w = 0.671` vs DB `0.64`, +4.8 %). **`records/game/combatformulas.dbr` supplies the missing multiplier** the spec did not have. **Crit is EXCLUDED** from the window (proved). **ORDER-1 (convert-then-modify) FAVOURED** over ORDER-2 by a 1.26× vs 1.84× residual. | INFERRED-TESTED |
| **HALT-3** | **CLOSED** | **`records/game/combatformulas.dbr` EXISTS in the pin.** `probabilityToHitEquation` verbatim; crit is a **PTH-band** mechanic with 6 thresholds and 6 multipliers, `pthMinimum = 55`. **No external fetch made or needed.** | DB-CITED |
| **HALT-6** | **CLOSED** | Same record + `gameengine.dbr`. Armour: **two-branch equation**, `armorDefensiveAbsorption = 70.0`, per-hit **body-region sampling** (7 regions, weights sum 100). `playerDefenseCap = [80,80,80]`. **No external fetch.** | DB-CITED |
| **HALT-2** | **CLOSED-BY-TYPE** | `characterRunSpeed = 0.92` on both PC records — but it is a **dimensionless multiplier, not m/s** (1 467-record distribution: median exactly 1.0, mode 1.0 n=479, every NPC class at 1.0). Engine-side reference rate in m/s is **NAMED-ABSENT**. `delayMovement` is declared **`type = "bool"`** — there is no magnitude to find. **Fixture is AT the engine run-speed cap (135 = `playerRunSpeedCapMax`).** | DB-CITED |
| **HALT-1** | **CLOSED** | `skill_buffselfshield.tpl` **declares no duration field at all**, nor do its four includes. It is a clone of **`Skill_BuffSelfToggled.tpl`** (`fileNameHistoryEntry`, verbatim). **These shields are absorb-POOLS, not timed buffs.** | TPL-CITED + DB-CITED |
| **HALT-8** | **CLOSED** | Crate's own annotation: **"Delay between projectile launches (seconds)."**, `type = "real"`, `defaultValue = "0.5"`. **0.2 is plain seconds. No ×0.8 conversion.** | TPL-CITED |

---

## 2 — HALT-9 (PRIORITY 1) — full-grain re-emission

### 2.1 Provenance and owner audit

All three records resolve to a **single archive**, `mods/survivalmode/database/SurvivalMode.arz`
(`sm_mod`) — no overlay contention:

```
records/game/balancingadjustment_survivalmode_enemies01.dbr   Aspirant     owners=['sm_mod']
records/game/balancingadjustment_survivalmode_enemies02.dbr   Challenger   owners=['sm_mod']
records/game/balancingadjustment_survivalmode_enemies03.dbr   Gladiator    owners=['sm_mod']
templateName = database/templates/gameadjustment.tpl
```

627 fields per record; **33 carry a non-zero value** in at least one difficulty (the spec's "~35" was
close; the exact count is 33). **25 are 200-element arrays** (one cell per wave) and **8 are scalars**
(no wave dependence possible).

### 2.2 Emission

| File | Shape |
|---|---|
| `scratch/2026-08-08-kc2-halt-bundle/halt9_survival_wave_scaling_full.csv` | 600 rows × 28 cols — `wave, tier, difficulty` + **all 25 array fields**, 200 waves × 3 difficulties |
| `scratch/2026-08-08-kc2-halt-bundle/halt9_survival_scalars.csv` | 24 rows — the **8 scalar** fields × 3 difficulties |

**(c) U-8 cross-check — sanity PASSED.** All 600 rows joined on `(wave, difficulty)`; all **9** U-8
columns compared cell-by-cell: **0 value mismatches, 0 tier-column mismatches.** The new emission is a
strict superset of `u8_survival_wave_scaling.csv`. *(The re-lap did not contradict the prior lane —
it extended it.)*

### 2.3 (a) RAMP vs FLAT — the 24 fields U-8 did not emit

| Field | Shape | w1 | **w100** | **w160** | w200 | Note |
|---|---|---:|---:|---:|---:|---|
| `offensiveTotalDamageModifier` | **RAMP** (identical A/C/G) | 5 | **20** | **43** | **130** | ⚠ **the spec carries the wave-100 value** |
| `offensivePhysicalModifier` | **RAMP, Gladiator only** | 0 | **−15** | **−21** | **−50** | Aspirant/Challenger **FLAT 0 at every wave** |
| `offensiveSlow{Bleeding,Cold,Fire,Life,Lightning,Physical,Poison}Modifier` | **RAMP** ×7, identical within a difficulty | 0 | −30 / −36 / **−40** | −47 / −56 / **−63** | −50 / −58 / **−65** | A / C / **G** |
| `defensivePercentCurrentLife` | **RAMP** (identical A/C/G) | 0 | 5 | **8** | 10 | 11 step points |
| `offensiveCritDamageModifier` | **RAMP** C/G; **VARY** on Aspirant | 0/0/**5** | 0/0/**6** | 14/15/**27** | **0**/18/**33** | ⚠ see § 2.5 |
| `retaliationTotalDamageModifier` | **RAMP** | 0 | 24/16/**22** | 54/53/**74** | 72/77/**110** | see § 2.4 |
| `skillCooldownReduction` | **RAMP** (identical A/C/G) | 0 | 0 | **0** | 10 | first step at **wave 180** |
| `spawnChampionMinAdj` / `MaxAdj` | **RAMP** (identical A/C/G) | 0 | 1 | 1 | 1 | steps to 1 at wave ~91 and holds |
| `defensiveConvert` | **SCALAR 50** | — | — | — | — | **no wave dependence** |
| `defensiveReflectModifier` | **SCALAR −70** | — | — | — | — | " |
| `offensive{Freeze,Petrify,Sleep,Stun,Trap}Modifier` | **SCALAR −40** ×5 | — | — | — | — | " |
| `offensiveSlowDamageMultModifier` | **SCALAR** −15 / −30 / **−40** | — | — | — | — | " — differs by difficulty only |

> ⚠ **CONDUCTOR ACTION — spec § 10.7 / § 10.8.** `offensiveTotalDamageModifier` at the wave-160
> showcase is **+43 %**, not the **+20 %** the spec carries from the index-99 read. That is a **2.15×
> understatement of the monster-damage scalar at the showcase wave**, structurally the *same class of
> error* as FINDING F-2's HP understatement and on the *same* record. **F-2's third order is now
> closed with a number.** At wave 200 the field reaches **+130 %** — a 6.5× move from the wave-100
> slice.
>
> `offensivePhysicalModifier` at wave 160 Gladiator is **−21 %**, not −15 %. This one *reduces* monster
> physical damage and exists **only on Gladiator** — a difficulty-exclusive field.

### 2.4 (b) `retaliationTotalDamageModifier` at full grain — **FINDING F-4 ADJUDICATED**

Full profile, all three difficulties, 200 waves (emitted in the CSV):

| wave | Aspirant | Challenger | **Gladiator** |
|---:|---:|---:|---:|
| 95 | 22 | 13 | 19 |
| **100** | **24** | **16** | **22** | ← **P-E6 § 2.8 read this row** |
| 110 | 29 | 21 | 29 |
| **112** | — | — | — | ← **crossover: Gladiator overtakes Aspirant, once, and never falls back** |
| 130 | 40 | 34 | 48 |
| **150–170** | **54** | **53** | **74** | ← **the 08-01 density note read this plateau** |
| 200 | 72 | 77 | 110 |

**Ruling.** F-4 is **not a source conflict**. Both readings are **exactly correct at their own wave
index**, and the "different ordering" the spec flagged is a **real, wave-dependent property of the
data**: Aspirant genuinely leads Gladiator below wave 112 and genuinely trails it above. The 08-01
figures (74 / 53–54) reproduce **cell-for-cell** at waves 150–170 — a 21-wave plateau that contains the
wave-160 showcase. **No Aspirant/Gladiator mismeasure is required to explain F-4**, and L-10(b) should
not be cited for it. *(L-10(b) may still hold for whatever else it was ruled on; it is simply not
load-bearing here.)*

**Consequence for spec § 6.3:** the monster-retaliation number that is load-bearing at the showcase is
**Gladiator 74 at wave 160**, not 22.

### 2.5 Data anomaly worth logging

**Aspirant `offensiveCritDamageModifier` resets to 0 at wave 171** and stays 0 through wave 200
(steps: … 149→13, 150→14, **171→0**). Challenger and Gladiator continue ramping (→18 and →33). This
is the **only non-monotone cell in the entire 200×3×25 emission**. It reads as a Crate authoring gap
in the Aspirant array past tier 18, not as a designed mechanic. Flagged, not interpreted.

**DB citations:** `records/game/balancingadjustment_survivalmode_enemies0{1,2,3}.dbr` ::
each field named above, index `wave − 1`.
**Script:** `t1_survey.py` → `t2_nonzero.py` → `t3_emit.py`.

---

## 3 — HALT-5 — the ≈982 reservation, **attributed to the unit**

### 3.1 Method

Corpus-wide census first: **82 records in the entire 4-archive campaign DB** carry a non-zero
`characterManaLimitReserve*` field. That is a small enough closed set to enumerate exhaustively, so
the sweep is complete rather than sampled.

**Two whole branches close as NAMED-ABSENT-BY-CENSUS:**

- **`characterManaLimitReserveModifier` is non-zero on ZERO records in the entire corpus.** The
  percent-reserve term in spec § 5.2's formula is a **dead field** in 1.3.0.0. The formula should drop
  it (or keep it and note it is never exercised).
- `characterManaLimitReserveReduction` / `…ReductionModifier`: likewise **zero everywhere**.
- **Devotion: zero of the 82 reserve-bearing records live under `records/skills/devotion/`.** Devotion
  cannot reserve. Branch (iv) of the commission closes empty.

### 3.2 The two corrections

**(1) Divine Mandate reserves NOTHING.**

```
records/skills/playerclass09/divinemandate1.dbr
    Class                              = Skill_BuffSelfToggled
    exclusiveSkill                     = True
    characterManaLimitReserve          = 0.0
    characterManaLimitReserveModifier  = 0.0
```

Spec § 3.2 / § 5.2 attribute the reservation regime to "Divine Mandate exclusive-aura". **Exclusivity
and reservation are independent mechanics in this engine**; Divine Mandate has the former and not the
latter. The *behaviour* the spec models (pool reservation) is correct and binding; only the *named
cause* is wrong. **Recommend the spec re-label the regime "the Presence/Field-Command reserve set"
and keep Divine Mandate as the V1 build discriminator it already is.**

**(2) The missing source is a COMPONENT skill, and it is the single largest term.**

```
records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr
    Class                      = Skill_BuffSelfToggled
    skillDisplayName           = tagGDX1CompSkillA101Name        (= "Presence of Might")
    skillMaxLevel              = 1
    characterManaLimitReserve  = 300.0                            <-- flat, rank-independent
```

Spec § 5.1 already lists **Presence of Might** in the fixture's permanent-buff surface (grimtools
`Buffs (4/13)`, ceremony § E `#387`) and correctly names it item-granted. It reserves **300**. P-E1's
sweep was scoped to mastery skills and never reached the component skill tree.

### 3.3 The ledger — **982 exactly**

Total ranks are `allocated + gear-skill-specific + mastery-wide`. Allocated ranks are save-CITED
(save-parse § 2.2). Gear skill-specific bonuses are DB-CITED (summed from `augmentSkillLevel*` across
the 16 equipped base records). The two **mastery-wide** totals — `O` (Oathkeeper) and `S` (Soldier) —
are the only unknowns, because "+N to all skills in X" arrives via components/augments that live in
the `.gdc`, not in the item base DBRs. Sweeping `O × S` over `0..8 × 0..8`:

```
EXACTLY ONE cell in the 81-cell grid reproduces 982:   O = +1,  S = +4
```

| Skill | alloc | +gear | +mastery | **= total** | **reserve** | record :: field |
|---|---:|---:|---:|---:|---:|---|
| Presence of Virtue 1 | 12 | +5 | +1 (O) | **18** | **220** | `playerclass09/presenceofvirtue1_buff.dbr :: characterManaLimitReserve[17]` |
| Presence of Virtue 2 | 9 | 0 | +1 (O) | **10** | **100** | `playerclass09/presenceofvirtue2.dbr :: [9]` |
| Presence of Virtue 3 | 10 | 0 | +1 (O) | **11** | **107** | `playerclass09/presenceofvirtue3.dbr :: [10]` |
| Field Command 1 | 10 | 0 | +4 (S) | **14** | **205** | `playerclass01/fieldcommand1buff.dbr :: [13]` |
| Field Command 2 | 8 | 0 | +4 (S) | **12** | **50** | `playerclass01/fieldcommand2.dbr :: [11]` |
| **Presence of Might** | — | — | — | 1 | **300** | `itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr` |
| Divine Mandate | 12 | 0 | +1 (O) | 13 | **0** | `playerclass09/divinemandate1.dbr` (exclusive, non-reserving) |
| | | | | **TOTAL** | **982** | **vs observed `2576 − 1594 = 982`** |

### 3.4 Two independent cross-checks that the solve is not a fit artefact

1. **`O = +1` predicts Eye of Reckoning total rank = 15 (allocated) + 10 (gear-specific, DB-summed:
   head +2, torso +2, hands +2, Gutsmasher +4) + 1 = **26**. The ceremony/grimtools lane MEASURED EoR
   at **26**.** The solve was fitted on the *energy globe* and validated against the *skill tooltip* —
   two unrelated instruments.
2. **`S = +4` decomposes cleanly**: `+3` is DB-visible from base items (`d028_head augmentMasteryLevel
   +1`, `d107_blunt2h +2` on `_classtraining_class01`) and `+1` is the *same* save-side "+1 to all
   skills" source that supplies `O = +1` (Oathkeeper gets **+0** mastery-wide from base items). One
   source explains both offsets. No free parameter was needed.

### 3.5 Corrections to prior art

P-E1's 624 was **not** an enumeration gap in the skill *set* — it had all five correct skills. It was a
**rank understatement**: P-E1 quoted PoV1 @16 (→200) where the true total is 18 (→220), FC1 @11 (→175)
where it is 14 (→205), FC2 @9 (→42) where it is 12 (→50). Corrected class-side total is **682**, and
the genuinely missing source was Presence of Might's **300**. `682 + 300 = 982`.

**Recommend spec § 3.2 and § 5.2 replace the "≈982 / ≈624 / residual ≈358" tables with the § 3.3
ledger.** `reserved = 982` graduates from **BINDING-as-observed** to **BINDING-and-derived**: the sim
can now reproduce it from the DB rather than hard-coding the globe reading, which makes AC-5.2
(deactivating an aura returns exactly its reserve) a *testable* criterion instead of an assertion.

**Scripts:** `t6_reserve.py` (82-record census) → `t7_reserve_fixture.py` (fixture sweep) →
`t8_reserve_solve.py` (ledger solve).

---

## 4 — HALT-3 + HALT-6 — engine constants: **CORPUS-RESIDENT, DB-CITED, no external fetch**

The commission graded this "ABSENT ⇒ EXTERNAL-NOT-FETCHED and STOP". **It is not absent.** Two records
carry it, and neither had been opened by this run.

### 4.1 `records/game/gameengine.dbr` (base archive, 366 fields)

| Field | Value | `.tpl` annotation (verbatim) |
|---|---|---|
| **`armorDefensiveAbsorption`** | **70.0** | *(none)* |
| **`playerDefenseCap`** | **[80, 80, 80]** | *"Index by difficulty 0 to 2"* |
| `monsterDefenseCap` | [100, 100, 100] | *"Index by difficulty 0 to 2"* |
| `playerReflectCap` | 30.0 | *"Index by difficulty 0 to 2"* |
| **`playerAttackSpeedCapMax` / `Min`** | **200.0** / 20.0 | — |
| **`playerRunSpeedCapMax` / `Min`** | **135.0** / 20.0 | *"Index by difficulty 0 to 2"* |
| `absoluteRunSpeedCapMax` / `Min` | 350.0 / [40, 30, 20] | — |
| `damageMagnitude` | 100.0 | *"Decreasing same type duration damage"* |
| `absMaxDamageScaling` | 100.0 | — |
| `2hWeaponDamageFactor` | 1.0 | — |
| `meleeRange` / `shortRange` / `moderateRange` / `longRange` / `maximumRange` / `bossRange` | 1.25 / 4.75 / 9.0 / 15.0 / 18.0 / 32.0 | **world unit is METRES** — see § 5.2 |
| `meleeAutoTargetDistance` / `meleeTargetDistance` / `alertDistance` | 4.0 / 2.4 / 6.0 | — |
| `maxPlayerRotationSpeed` / `minPlayerRotationSpeed` | 30.0 / 19.0 | — |
| `monsterLevelGapFixer` | [0, 5, 7] | — |
| `autoCastEquation` | `procRate * (1 + (cooldown * 81)/100) * (1 - (attackDuration * 11) / 100)` | — |

> **Two fixture facts fall straight out.** The sheet's **Attack Speed 196 %** sits just under
> `playerAttackSpeedCapMax = 200`, and the sheet's **Run Speed 135 %** is **exactly**
> `playerRunSpeedCapMax = 135` — the fixture is **movement-speed-capped**, not coincidentally at 135.
> Both belong in the § 3 / § 2 constants blocks.
>
> **`autoCastEquation` is a free gift to § 9.** It is Crate's own formula for how an item/devotion
> auto-cast's effective proc rate is modified by the host skill's cooldown and attack duration —
> directly relevant to the § 9.3 rate-ceiling column, which currently reasons about proc rates without
> it.

### 4.2 `records/game/combatformulas.dbr` — **HALT-3 closed** (base archive, 44 fields)

Crate's equations, **verbatim from the record**:

```
offensiveAbilityEquation  = (offensiveAbilityDV + (characterLevelDV * 12) + ((dexterityDV + bonusDV) *0.5)) * (1 + (offensiveAbilityModifierDV / 100))+53
defensiveAbilityEquation  = (defensiveAbilityDV + (characterLevelDV * 12) + ((strengthDV  + bonusDV) *0.5)) * (1 + (defensiveAbilityModifierDV / 100))+53

probabilityToHitEquation  = ((((offensiveAbilityDV/((defensiveAbilityDV/3.5)+offensiveAbilityDV))*300)*0.3)+(((((offensiveAbilityDV*3.25)+10000) - (defensiveAbilityDV*3.25))/100)*0.7))-50
normalPTHEquation         = probabilityToHitDV/70

pthMinimum        = 55.0
pthThreshold1..6  =  70.0  90.0  105.0  120.0  130.0  135.0
pthDamageModifier1..6 = 1.0   1.1    1.2    1.3    1.4    1.5
```

**Reading (structural, stated as inference and marked as such):** GD does **not** roll a separate
crit chance. It computes one **PTH** scalar from OA vs DA, floors it at `pthMinimum = 55`, and the
*magnitude* of PTH selects a **damage-multiplier band** — `≥70 → ×1.0` (normal), `≥90 → ×1.1`,
`≥105 → ×1.2`, `≥120 → ×1.3`, `≥130 → ×1.4`, `≥135 → ×1.5`. Below threshold1 the hit *chance* is
`PTH/70`. **The equations and constants are DB-CITED; the band-selection semantics are INFERRED from
the field names + `.tpl` descriptions (`"if pthChance > threshold2"` etc., which are Crate's own
words) and should be validated by gamora's tests, not taken as law.**

### 4.3 `combatformulas.dbr` — **HALT-6 closed**

```
physicalDamageDefenseEquationDGP    = (sumProtectionDV * (1 - sumAbsorptionDV)) + (physicalDamageDV - sumProtectionDV)
physcialDamageDefenseEquationDLEP   = physicalDamageDV * (1 - sumAbsorptionDV)          [sic — Crate's typo]

shieldDamageReductionEquationDGB    = damageDV - (shieldDefenseDV * (shieldAbsorptionDV / 100))
shieldDamageReductionEquationDLEB   = damageDV * ((100 - shieldAbsorptionDV) / 100 )

physicalDamageEquation              = (physicalDamageDV*((dexterityDV/245)+1))
pierceDamageEquation                = pierceDamageDV*((dexterityDV/245)+1)
magicalDamageEquation               = magicalDamageDV*((intelligenceDV/215)+1)
physicalDurationDamageEquation      = (physicalDamageDV*((dexterityDV/215)+1))
magicalDurationDamageEquation       = magicalDamageDV*((intelligenceDV/200)+1)

combatRegionHeadChance      = 15      combatRegionTorsoChance     = 26
combatRegionShouldersChance = 15      combatRegionLegsChance      = 20
combatRegionArmsChance      = 12      combatRegionFeetChance      = 12
combatRegionUnprotectedChance = 0     combatRegionFullyProtectedChance = 0     (sum = 100)
```

**The armour model, complete.** Two branches keyed on damage-vs-protection: when incoming physical
damage **exceeds** armour (`DGP`), the portion up to armour is reduced by `sumAbsorption` and the
excess passes **unmitigated**; when damage is **at or below** armour (`DLEP`), the whole hit is reduced
by `sumAbsorption`. With `armorDefensiveAbsorption = 70.0` from `gameengine.dbr`, absorption is **70 %**
by default. Per hit the engine **samples a body region** by the eight weights above, which is why
`sumProtection` is per-region and not the sheet's Armor Rating — spec § 6.3 should carry that as a
declared simplification if the sim uses the flat rating.

**Three further gifts to the spec, unrequested:**
- **`physicalDamageEquation` — physical damage scales with cunning**, `× (1 + cunning/245)`. This term
  is absent from spec § 1.3 and it is **large**: at the fixture's Cunning 1219 it is **×5.98**. See § 5.1.
- Duration (DoT) damage uses a *different* divisor (215, not 245) — the EoR bleed lane needs its own
  coefficient.
- `playerDefenseCap = 80` confirms the sheet's five 80 % resistances are **at cap**, so resistance
  headroom is zero and the § 6.3 monster-damage envelope cannot be softened by more resist.

**No community formula was fetched, and none is now needed. Citation-hygiene ruling L-9 is honoured
by corpus-residency, not by abstention.**

---

## 5 — HALT-4 — damage application order

### 5.1 The two-point solve (the only assumption-light test the sheet supports)

Sheet, ceremony § D `#511`: **Weapon Damage `16 972 – 40 930`**, **Eye of Reckoning `43 691 – 59 761`**.
Assume `EoR = w × WeaponDamage + X` with `w, X` constant across the weapon's min–max:

```
w = (59761 − 43691) / (40930 − 16972) = 0.6708
X = 43691 − 0.6708 × 16972              = 32 307
```

**Result 1 — the weapon term of § 1.3 is CONFIRMED.** Solved `w = 0.671` against the DB-CITED
`weaponDamagePct[26] = 50 % + Gutsmasher modifier 14 % = 0.64` — **+4.8 %**. (Against the gated-OFF
Warborn 0.69 it is −2.8 %; the DB reading is the better fit, which independently supports P-E1 § 5.3's
call that `itemSkillModifierControl = [0,0,0,1]` keeps the set bonus **off** at 3 pieces.)

**Result 2 — CRIT IS EXCLUDED from the window.** Sheet Critical Damage is **+57 %**. If the window's
top were a crit of its bottom it would read `43 691 × 1.57 = 68 595`; the sheet reads **59 761**
(−12.9 %). The window's tightness (max/min **1.368**, against the weapon line's **2.412**) is fully
explained by the large constant addend `X`, not by a crit band. **The sim must not fold crit into the
per-tick basis; it is a separate multiplier applied after.**

**Result 3 — the composition in § 1.3 is misweighted.** `X = 32 307` is **74 % of the EoR minimum** and
**54 % of its maximum**. The flat term is the *trunk* of this skill's damage, not a garnish. § 1.3
presents 64 % weapon damage first and "composed flat ≈ 324–344" second; the sheet says the ordering of
importance is the reverse.

### 5.2 Candidate orderings, tested

`combatformulas.dbr` supplies the multiplier the desk-math was missing. Permanent, always-on,
DB-summed from the Edition-II records at the § 3.3 total ranks:

| Term | Value | Source |
|---|---:|---|
| `× (1 + cunning/245)` | **×5.976** | `combatformulas.physicalDamageEquation`, Cunning 1219 (ceremony § D) |
| Σ `%Physical`, permanent | **+1100 %** | gear +853 (11 items) · `divinemandate1@13` +143 · `playerclass01/passive3@12` +104 |
| Σ `%TotalDamage`, permanent | **+120 %** | `b201e_necklace` +35 · `fieldcommand2@12` +85 |
| ⇒ combined | **×13.20** | |

*(Excluded as non-permanent: `fightingspirit1` +95 % total, `ascension1` +38 % total, `blitz2` +128 %
physical — the last is a Blitz modifier, not an EoR term.)*

| Model | Form | Predicts | vs `X = 32 307` |
|---|---|---:|---|
| **shape test** — cunning term **multiplicative** | `flat × (1+cun/245) × (1+Σ%)` | 25 556 | **1.26× short** |
| shape test — cunning term **additive** | `flat × (1+cun/245+Σ%)` | 5 889 | 5.49× short — **REJECTED** |
| **ORDER-1** convert-then-modify (138 Fire → Physical, *then* `%Physical`) | | **25 556 – 27 134** | **1.19 – 1.26× short** |
| **ORDER-2** modify-then-convert (138 × `(1+254 % Fire)`, *then* → Physical) | | 17 590 | **1.84× short** |

### 5.3 Verdict — **PARTIAL-CLOSED, ORDER-1 FAVOURED**

The ordering that best reproduces the sheet window is:

```
per_tick = weaponDamagePct × WeaponDamage_composed                     # w = 0.64 DB, 0.671 solved
         + Σ(skill-side flat, CONVERTED FIRST)                         # ORDER-1
           × (1 + cunning/245)                                         # combatformulas
           × (1 + Σ%Physical/100 + Σ%TotalDamage/100)                  # additive within the bracket
                                                                       # crit applied AFTER, excluded
                                                                       # from the tooltip window
```

**Why this is FAVOURED and not PROVEN.** Both orders *under*-produce, and the un-enumerated sources —
**55 devotion nodes** and the **save-resident components/augments** — can only **add** to the
multiplier. ORDER-1 needs those to supply a further **+26 %** on the multiplier (≈ +345 percentage
points of Physical); ORDER-2 needs **+84 %** (≈ +1 110 points). For an 11-constellation devotion map
plus a dozen component slots, the first is routine and the second is not. **The discrimination is
real but the margin is one of plausibility, not arithmetic.**

**Grade: INFERRED-TESTED.** The residual signal separating the two orders is **1 024 per tick = 3.2 %
of `X`**, which sits *below* the ~20 % un-enumerated remainder. **What would close it exactly:** one
enumeration of the fixture's devotion + component `%Physical` / `%TotalDamage` stack — a bounded,
nameable follow-on, not a HALT. *(The alternative closer is one grimtools character-tab frame showing
the composed `% Physical Damage` line.)*

### 5.4 Source correction the conductor should hold

The ceremony note's line-210 aside cites *"the character's `+396 % Physical` / `+293 % Bleeding`"*.
**`+396 %` cannot be the composed character-sheet `%Physical`:** the fixture's **base items alone**
sum `offensivePhysicalModifier = +853 %` across 11 pieces (`d114_relic` +110, `d108_waist` +76,
`d206_hands` +65, `d110_ring` +66, `d107_blunt2h` +200, and six more), before any skill. Divine Mandate
at total rank 13 adds **+143 %** on its own. Whatever `+396 %` was read from, it is **not** the composed
figure, and any desk-math that leans on it will be wrong by ≥2.2×. **Flagged as a source correction,
not adjudicated here.** The `%Bleeding` figure is untested by this probe.

**Scripts:** `t9_flatstack.py`, `t10_halt4_solve.py`.

---

## 6 — HALT-2 — player base movement rate + `delayMovement`

### 6.1 The base rate — DB-CITED, but the unit is the finding

```
records/creatures/pc/malepc01.dbr      Class = Player,  templateName = database/templates/player.tpl
records/creatures/pc/femalepc01.dbr    (identical on all speed fields)

    characterRunSpeed              = 0.92
    characterRunSpeedModifier      = 0.0
    characterRunSpeedJitter        = 0.0
    characterAttackSpeed           = 1.25
    characterSpellCastSpeed        = 1.25
    characterBaseAttackSpeedTag    = CharacterAttackSpeedAverage
```

**`characterRunSpeed` is a dimensionless MULTIPLIER, not a rate in m/s.** Evidence — a census of
**1 467 creature records** carrying a non-zero value:

| statistic | value |
|---|---|
| median | **exactly 1.00** |
| mode | **1.00** (479 records) |
| range | 0.36 – 3.00 |
| every `Npc*` class (216 + 25 + 6 + 3 + 1 + 1) | median **1.00** |
| `Player` (2 records) | **0.92** |

A field whose modal and median value across 1 467 records is *exactly* 1.0, and whose every NPC class
sits at 1.0, is a multiplier against an engine-side reference. `parameters_character.tpl` types it
`class="array" type="real"` with an **empty `description`** — no unit is declared.

**The reference rate in m/s is NAMED-ABSENT.** It is not in `gameengine.dbr`, not in
`combatformulas.dbr`, not annotated in any of the 819 `.tpl`, and not in the pc records.

**But the sim does not need it as a HALT — it needs it as ONE declared free parameter,** because every
*ratio* is now DB-CITED:

```
v_player = v_ref × 0.92 × (RunSpeed% / 100)          RunSpeed% ≤ playerRunSpeedCapMax = 135
         = v_ref × 0.92 × 1.35   for the fixture     (the fixture is AT the cap)
         = v_ref × 1.242
v_monster = v_ref × characterRunSpeed(monster)       per-record, DB-CITED, 0.36 – 3.00
```

**Recommend HALT-2 be re-dispositioned from "named HALT" to "one DECLARED free parameter `v_ref`",**
alongside § 10.6's emitter positions. Relative closing speeds — which is what the § 2 moving circle
actually needs — are fully determined without it.

**World unit is METRES, DB/TPL-CITED.** `templates.arc` annotates distance fields *"in meters"*
throughout (`maxRange` *"Maximum range of the beam (in meters)"*, `distance` *"Distance the attack
travels (meters)"*, `detectionRadius`, `travelSpeed` *"in meters per second"*, `worldDescOffset`
*"World space(meters)"*). So `gameengine.meleeRange = 1.25 m` and — the one the spec cares about —
`eyeofreckoning1.skillTargetRadius = 3.0` **is 3 metres**. § 2's "3 m disc" is now DB-CITED, not
assumed.

### 6.2 `delayMovement` — **CLOSED BY TYPE**

```
skill_attackradiusspin.tpl        (the EoR class template)
    Variable {
        name         = "delayMovement"
        class        = "variable"
        type         = "bool"
        description  = ""
        defaultValue = "0"
    }
```
```
records/skills/playerclass09/eyeofreckoning1.dbr  ::  delayMovement = True
```

**It is declared `bool`.** There is no magnitude field, in this template or any other — the search is
not "unfound", it is **structurally void**. Whatever the movement penalty is, it is a hard-coded engine
constant with no DBR surface. **HALT-2's second half should be closed as NAMED-ABSENT-BY-TYPE and
modelled as a declared binary: while channelling, movement is engine-delayed by an unstated amount;
the sim declares its own value and names it.**

---

## 7 — HALT-1 — `Skill_BuffSelfShield` lifetime

### 7.1 The template, verbatim

`skill_buffselfshield.tpl` (819-file `templates.arc`), in full, is four includes plus one three-field
group plus the header:

```
	Variable { name = "Include File" ... defaultValue = "database\Templates\TemplateBase\Skill_Base.tpl"      }
	Variable { name = "Include File" ... defaultValue = "database\Templates\TemplateBase\Skill_Activated.tpl" }
	Variable { name = "Include File" ... defaultValue = "database\Templates\TemplateBase\Skill_Buff.tpl"      }
	Variable { name = "Include File" ... defaultValue = "database\Templates\TemplateBase\Skill_Bonus.tpl"     }

	Group { name = "Header"       ... Variable { name = "Class" class = "static" defaultValue = "Skill_BuffSelfShield" } }
	Group { name = "Skill Config" type = "list"
		Variable { name = "instantCast"          class = "variable" type = "bool" defaultValue = "0" }
		Variable { name = "skillActiveLifeCost"  class = "array"    type = "real" defaultValue = ""  }
		Variable { name = "skillActiveManaCost"  class = "array"    type = "real" defaultValue = ""  }
	}
}

fileNameHistoryEntry
{
	"Templates\Copy of Skill_BuffSelfToggled.tpl"
}
```

### 7.2 Answer

**The template declares NO duration, and neither does any of its four includes.** Verified field-by-field:
`Skill_Base.tpl` (69 names), `Skill_Activated.tpl` (28), `Skill_Buff.tpl` (30), `Skill_Bonus.tpl` (9)
— **`skillActiveDuration` appears in none of them.** `skillActiveDuration` is declared in **31 other
templates**, including a sibling **`skill_buffselfduration.tpl`**. Crate maintains two distinct
buff-self classes: a **timed** one and a **shield** one, and gave the shield class no timer.

**What `Skill_Buff.tpl` gives it instead is `damageAbsorption` and `damageAbsorptionPercent`** —
capacity, not lifetime. And `fileNameHistoryEntry` records that the template was **cloned from
`Skill_BuffSelfToggled.tpl`** — a class whose whole semantic is "on until turned off".

**Ruling: these shields are absorb-POOLS. They end when the pool is spent (or on re-cast), not on a
timer.** The absence of `skillActiveDuration` from all 15 records is not a gap in the fetch — it is
the class being correctly authored.

### 7.3 The two fixture records, and a bonus for § 9.3

```
records/skills/devotion/tier1_29e_skill.dbr     FileDescription = "Turtle - Turtle Shell"
    Class            = Skill_BuffSelfShield          instantCast      = True
    damageAbsorption = [25] 500 → 6100              (max rank 25 → 6100 — matches the spec)
    skillCooldownTime= [25]  32 →    8              (DECLINES with rank; 8 s at max)
    templateAutoCast = records/controllers/itemskills/cast_@selfat50%health_100%.dbr
    (no damage-type qualifiers → absorbs ALL damage types)

records/skills/devotion/tier2_17c_skill.dbr     FileDescription = "Crab - Arcane Barrier"
    Class            = Skill_BuffSelfShield          instantCast      = True
    damageAbsorption = [20] 300 → 2900              (max rank 20 → 2900 — matches the spec)
    skillCooldownTime= 3.0                          (scalar)
    templateAutoCast = records/controllers/itemskills/cast_@selfonanyhit_30%.dbr
    aetherDamageQualifier / chaosDamageQualifier / elementalDamageQualifier /
    lifeDamageQualifier / poisonDamageQualifier = True
```

**Two things § 9.3 does not currently carry:**

1. **Arcane Barrier's 2900 is TYPE-GATED.** Its five `*DamageQualifier` flags admit Aether, Chaos,
   Elemental, Life and Poison — and therefore **exclude Physical, Pierce and Bleed**. Against the
   Crucible's physical opposition its contribution to *this* fixture is far smaller than its face
   value. Turtle Shell carries **no qualifiers** and absorbs everything. **§ 9.4's envelope arithmetic
   for row 5 should be re-run with the gate applied.**
2. **The rate ceilings are DB-CITED and asymmetric**: Turtle Shell **8 s** at rank 25 with a
   *100 % @ 50 % health* trigger; Arcane Barrier **3 s** with a *30 % on any hit* trigger. Those two
   `templateAutoCast` controller records are the § 9.3 trigger column, stated by the DB.

**Corpus-wide:** exactly **15** records carry `Class = Skill_BuffSelfShield`; **none** of the 15 has
any duration-class field. Confirmed by exhaustive scan of the 4-archive campaign stack.

---

## 8 — HALT-8 — Soulfire `projectilePeriod` unit

**CLOSED. Crate's own English, from the template EoR-2 actually uses:**

```
skillsecondary_attackprojectileorbiting.tpl        ( = Class SkillSecondary_AttackProjectileOrbiting,
                                                       which is eyeofreckoning2.dbr's Class )
	Variable {
		name         = "projectilePeriod"
		class        = "variable"
		type         = "real"
		description  = "Delay between projectile launches (seconds)."
		defaultValue = "0.5"
	}
```

The identical annotation appears on `skill_attackprojectileorbiting.tpl` (the non-secondary twin).

**`projectilePeriod = 0.2` is 0.2 SECONDS. It does NOT take the ×0.8 ms-unit conversion.** Soulfire
launches at **5 projectiles/second**, on its own cadence, independent of the disc. Spec § 1.4's
parenthetical *"(typed `real`, plain seconds)"* was right and is now **TPL-CITED rather than inferred**;
the `defaultValue = 0.5` (= 2/s) is a further consistency check that the number lives in the
seconds-scale, not the millisecond-scale.

---

## 9 — What this probe did NOT resolve

| Item | Status | What would close it |
|---|---|---|
| Engine reference movement rate in **m/s** | **NAMED-ABSENT** (not in `.arz`, not in 819 `.tpl`) | one movement-calibration frame — **or** re-disposition as a declared free parameter `v_ref` (§ 6.1, recommended) |
| `delayMovement` magnitude | **NAMED-ABSENT-BY-TYPE** — field is `bool`; no magnitude exists in any DBR | engine-side only; sim declares its own and names it |
| HALT-4 exact ordering (ORDER-1 vs ORDER-2) | **FAVOURED, not proven** — 3.2 % signal under a ~20 % residual | enumerate the 55 devotion nodes' + components' `%Physical`/`%TotalDamage`, **or** one grimtools character-tab frame |
| Whether the PTH **band-selection** semantics are as read | equations DB-CITED; **band semantics INFERRED** | gamora's tests, per § 4.2 |
| `%Bleeding +293 %` (ceremony line 210) | untested by this probe | — |
| **HALT-7** (boss-skill rank binding per wave) | **NOT FIRED** — pre-registered G-D contingency, per L-19 | unchanged |

**No value in this note was estimated. Everything is DB-CITED, TPL-CITED, save-CITED, solved-exactly,
or explicitly NAMED-ABSENT.**

---

## 10 — Artefacts

**Emissions (the deliverables):**
- `.../scratch/2026-08-08-kc2-halt-bundle/halt9_survival_wave_scaling_full.csv` — 600 × 28, all 25 wave-varying fields
- `.../scratch/2026-08-08-kc2-halt-bundle/halt9_survival_scalars.csv` — 24 × 3, the 8 scalars

**Reproduction chain (read-only, all under `.../scratch/2026-08-08-kc2-halt-bundle/`):**

| Script | Purpose |
|---|---|
| `t1_survey.py` | owner audit + 627-field survey of the three balancing records |
| `t2_nonzero.py` | 33 non-zero fields, RAMP/FLAT/VARY classification → `t2_nonzero_fields.json` |
| `t3_emit.py` | full-grain CSV emission + U-8 byte-match + retaliation profile |
| `t4_tpl.py` | crack `templates.arc` (818/819 extracted) + FoA-freshness probe → `tpl/`, `t4_tpl_index.json` (18 999 names) |
| `t5_query.py` | template-annotation query for the HALT fields |
| `t6_reserve.py` | corpus-wide 82-record reserve census → `t6_reserve_census.json` |
| `t7_reserve_fixture.py` | fixture sweep: allocated skills · 16 gear · gear-granted skills · devotion |
| `t8_reserve_solve.py` | the 81-cell ledger solve → 982 exact |
| `t9_flatstack.py` | flat/% damage enumeration from base items + active buffs |
| `t10_halt4_solve.py` | two-point solve, crit-exclusion test, ordering discrimination |

*(One of 819 `.tpl` failed decompression — an unnamed zero-length entry. No template relevant to any
HALT was affected; all seven target templates extracted cleanly.)*

---

**Signed:** legolas, 2026-08-08.

The commission expected two of these seven to come back as *EXTERNAL-NOT-FETCHED*. Neither did.
`records/game/combatformulas.dbr` was sitting in the base archive the whole run — Crate's hit
equation, crit bands, armour model and per-hit body-region weights, in plain text, in a corpus we
already had. The lesson is the same one U-9 filed and it is now filed twice: **before grading a value
EXTERNAL, open the records whose names describe the question.** The second lesson is narrower and
sharper — HALT-5's residual was never a missing skill. It was five skills read at the wrong rank plus
one component nobody had opened, and the moment the ranks were solved from the DB instead of assumed,
the number closed to the unit and then validated itself against an unrelated instrument. **A residual
is a hypothesis about where you have not looked, not a quantity.**
