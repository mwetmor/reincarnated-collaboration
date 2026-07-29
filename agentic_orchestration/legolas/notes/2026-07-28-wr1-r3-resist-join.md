# WR1-EXT-R3JOIN — the R3-regime gear resistance join (Edition-II corpus × parsed save)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-29 (cell chartered 2026-07-28)
**Cell:** WR1-EXT-R3JOIN · **Run:** WR1-2026-07-28 · **Conductor:** gandalf
**Discharges:** M-1 spec **R-M1-4** — *"the R3 resistance vector is a MEASURED input, never a fitted one…
Owed input: an R3-regime gear-record join (legolas)"*
(`gandalf/design-inputs/2026-07-28-wr1-m123-specs.md` §1.7)
**Charter:** `gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` §1 (S-5 join, S-6 corpus), §8
**Predecessor:** `legolas/notes/2026-07-28-wr1-extraction.md` (cited **EXT §n**) — **this note CORRECTS its §2.3/§2.4**
**Class:** evidentiary — measured extraction from primary source
**Mode:** read-only. Corpus `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` untouched.
**Method lineage:** reuses `legolas/scratch/2026-07-28-gdc-parse-g7/{lib_corpus,arz_index}.py` and
`gear_resolved.json` / `gear_named.json` (the S-5 join). New probes in
`legolas/scratch/2026-07-29-wr1-r3resist/` (`p1`…`p15`). Nothing rebuilt.

**Grading key:** **M** = read verbatim from a named `.arz` record or `.gdc` block · **D** = derived,
operator shown · **U** = unresolved · **CANNOT-ANSWER** = probe named, corpus silent.

---

## §0 — THE ONE-LINE ANSWER, AND THE FINDING THAT OUTRANKS IT

**R3 cold resistance = 14 % (nominal, MEASURED).** Cap 80 %, not binding, no overcap. One source:
the helm prefix `records/items/lootaffixes/prefix/ad003a_res_cold_01.dbr`, `defensiveCold = 14.0`.

**The finding that outranks it:** the M-1 spec's own reachability arithmetic (§1.7) requires
`r_cold_R3 ≥ 0.730` for G-A to read 2.12. The measured value is **0.14** — short by a factor of
**≈ 4.9**. Re-solved against the measured armour and without the spec's phantom conversion channel
(§4), the requirement is `r_cold ≥ 0.688`; the gap is unchanged in kind.

> **G-A is EVALUABLE — and the measured R3 vector falsifies the spec's prediction.**
> R-M1-4's honorable fallback (*"if the R3 resistance vector cannot be measured, G-A is
> NOT-EVALUABLE"*) **does not fire.** The vector is measured. It says the fixture's R2→R3 gear step
> carried **no elemental-resistance movement at all** on the cold channel — because the *only*
> cold-resist item in the terminal set is a single 14 % helm prefix, and there is no second one to
> arrive at the boundary. **The step is a pure HP step (×2.117) plus armour that is already
> saturated against the nova.** Against the death-2 nova the composed model returns **524.31 HP
> delivered in both regimes** (§5) ⇒ `W_pre / W_post = 1.000`.
>
> That is the same 1.000 the sim produced. **The sim was not wrong about this number.** Whether the
> fixture's measured `fall ÷ EHP = 2.12` therefore reflects *encounter composition* rather than
> *mitigation* is a question for the conductor — I flag it in §7 and do not rule it.

---

## §1 — WHICH REGIME THE SAVE ACTUALLY IS (a correction to EXT §0/§2.3)

EXT §0 carried the save as *"the level-13 end-state… any player-side item figure below is the save's
gear, not provably the death-2 gear."* That caveat was right and understated. The save is **not an
imperfect R2 proxy — it is the R3 regime, exactly.**

| Instrument | Value | Grade | Source |
|---|---|---|---|
| Save `play_stats.playTime` | **7096 s** | M | `.gdc` `play_stats` block (G-7 parse, `parsed.json`) |
| G-8 terminal orb frame f352 | `1607 / 1607` at `play_time` **7088** | M | galadriel G-8 §... (`f352-hp-dbg.png`) |
| R2 window | `play_time` 1134–**6052** | M | kit-spec v2 §1.7 |
| Death 2 | `play_time` **5453** | M | EXT §0 |

**⇒ the save is 1,043 s past the R2/R3 boundary and 8 s past the frame that measured `POOL_R3 = 1607`.
The equipped set in `gear_resolved.json` IS the R3 gear set.** (M)

**And there is a hard, source-side R2/R3 discriminator on one item (M + D):**

```
records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr   (the Primordian)
    lootMisc2Item1 = records/items/loottables/gearaccessories/tdyn_necklace_b01_slithnecklace.dbr
                          └─ lootName1 = records/items/gearaccessories/necklaces/b001_necklace.dbr
```
`b001_necklace.dbr` carries `FileDescription = "Wightmire Slith Boss"`, and a whole-corpus reference
sweep finds it in **exactly one loot table, referenced from exactly one creature** (2 refs, both the
same table, `database` + `GDX1`). **The amulet — *Menacing Putrid Necklace of Protection*, +25 Poison
resistance, +220 base Health — is the Primordian's own monster-infrequent.** It cannot have been worn
at death 2; it arrived from the boss the player later beat.

> **D — this is the first item in the whole run that is *provably* R3-only, and it is a resistance
> item.** It also itemizes ≥ 220 of the +848 HP step from the source side rather than from a tooltip.

**R2 gear set: CANNOT-ANSWER (L-1).** Probe run: (i) the `.gdc` carries one equipment array, the
terminal one — there is no history block; (ii) galadriel's G-6 gear tooltips are frames f296–f333,
and frame ID is monotone in `play_time` (f68 → 960 s, f314 → 6445 s, f348 → 7079 s), so **every gear
tooltip in the 313-still set is at `play_time` ≥ ~5800 and the whole f323–f333 cluster is post-boundary
R3**; (iii) no third instrument exists. **No artifact in this run captured the R2 equipment set.**
Everything EXT §2.4 and M-1 spec §1.6 label "R2 regime" is **R3 gear used as an R2 proxy** — including
the 14 % cold resist and the `A = 342.36`. Stated so it is not re-inherited silently.

---

## §2 — THE VECTOR (R3 regime, `_Fresh Character 01`, `play_time` 7096, level 13)

Equipped set: 10 armour/accessory slots (`attached = 1` on all ten), weapon set 1 (mace + shield),
**medal and relic slots empty**, **weapon set 2 empty**, **`useAlternate = 0`** (M, `.gdc` `inventory`
block). **Zero components, zero augments** on every slot (M, G-7 §3.1 — re-verified this pass).

### 2.1 — Per-element resistance vector

| Element (`defensive*` field) | Raw sum | Cap | **Capped effective** | Overcap? | Sources |
|---|---|---|---|---|---|
| **Cold** `defensiveCold` | **14.0 %** | 80 | **14.0 %** | none | helm prefix |
| **Poison / Acid** `defensivePoison` | **40.0 %** | 80 | **40.0 %** | none | amulet base 25 + shield base 15 |
| **Aether** `defensiveAether` | **18.0 %** | 80 | **18.0 %** | none | legs prefix 8 + belt suffix 10 |
| **Bleeding** `defensiveBleeding` | **10.0 %** | 80 | **10.0 %** | none | torso suffix |
| **Vitality** `defensiveLife` | **8.0 %** | 80 | **8.0 %** | none | shoulders prefix |
| **Chaos** `defensiveChaos` | **8.0 %** | 80 | **8.0 %** | none | amulet prefix |
| **Fire** `defensiveFire` | **0.0** | 80 | **0.0** | — | *none* |
| **Lightning** `defensiveLightning` | **0.0** | 80 | **0.0** | — | *none* |
| **Pierce** `defensivePierce` | **0.0** | 80 | **0.0** | — | *none* |
| **Physical** `defensivePhysical` | **0.0** | 80 | **0.0** | — | *none* |

**Every CC / utility resist is 0.0** — `defensiveFreeze`, `defensiveStun`, `defensiveSleep`,
`defensivePetrify`, `defensiveTrap`, `defensiveKnockdown`, `defensiveConfusion`, `defensiveFear`,
`defensiveDisruption`, `defensiveManaBurn`, `defensiveSlowLifeLeach`, `defensiveReflect`,
`defensiveConvert`, `defensiveCrowdControl`, `defensivePercentCurrentLife`. (M — exhaustive sweep of
all five item parts × 12 slots.) **This re-confirms EXT §1.5: the nova's 1.3–1.8 s freeze lands at
full duration in R3 as well as R2.**

**Aggregate / overcap fields, all absent (M):** no `defensiveElementalResistance`, no
`defensiveAllResistance`, and **no `defensive*MaxResist` on any equipped part** — so the 80 % ceiling
is unmodified. **The cap is not binding on any element; raw = effective throughout.**

### 2.2 — Per-item provenance (every number, every path)

| Slot | Item (display name, G-7 `.arc` join) | Part | Record | Field | Value | `lootRandomizerJitter` |
|---|---|---|---|---|---|---|
| head | *Sheltering Salvaged Helmet of the Dranghoul* | prefix | `records/items/lootaffixes/prefix/ad003a_res_cold_01.dbr` | `defensiveCold` | **14.0** | 30.0 |
| head | " | base | `records/items/gearhead/a03_head002.dbr` | `defensiveProtection` | 76.0 | — |
| head | " | suffix | `records/items/lootaffixes/suffix/b_ar014_arje.dbr` | `defensiveProtectionModifier` | 4.0 | 28.0 |
| amulet | *Menacing Putrid Necklace of Protection* | base | `records/items/gearaccessories/necklaces/b001_necklace.dbr` | `defensivePoison` | **25.0** | — (base) |
| amulet | " | prefix | `records/items/lootaffixes/prefix/b_ar022_ar.dbr` | `defensiveChaos` | **8.0** | 28.0 |
| torso | *Mystic Salvaged Armor of Menhir's Wall* | suffix | `records/items/lootaffixes/suffix/b_ar002_ar.dbr` | `defensiveBleeding` | **10.0** | 28.0 |
| torso | " | suffix | " | `defensiveProtectionModifier` | 4.0 | 28.0 |
| torso | " | base | `records/items/geartorso/a02_torso002.dbr` | `defensiveProtection` | 58.0 | — |
| legs | *Glacial Patchwork Leggings of the Fox* | prefix | `records/items/lootaffixes/prefix/b_ar030_ar.dbr` | `defensiveAether` | **8.0** | 28.0 |
| legs | " | base | `records/items/gearlegs/a02_legs01.dbr` | `defensiveProtection` | 50.0 | — |
| feet | *Vigorous Reinforced Greaves* | base | `records/items/gearfeet/a02_feet02.dbr` | `defensiveProtection` | 52.0 | — |
| hands | *Stalwart Hide Gloves of Frostbite* | base | `records/items/gearhands/a02_hands01.dbr` | `defensiveProtection` | 29.0 | — |
| ring1 | *Vampiric Silver Band* | — | `records/items/gearaccessories/rings/a001_ring02.dbr` | *(no defensive field)* | — | — |
| ring2 | *Silver Band of Prowess* | — | " | *(no defensive field)* | — | — |
| waist | *Mystic Woven Cord of Soulwarding* | suffix | `records/items/lootaffixes/suffix/b_ar103_ar_a.dbr` **(GDX1)** | `defensiveAether` | **10.0** | 28.0 |
| waist | " | base | `records/items/gearaccessories/waist/a02_waist001.dbr` | `defensiveProtection` | 7.0 | — |
| shoulders | *Magestorm Fur-lined Mantle of Frostbite* | prefix | `records/items/lootaffixes/prefix/b_ar104_ar_a.dbr` **(GDX1)** | `defensiveLife` | **8.0** | 28.0 |
| shoulders | " | base | `records/items/gearshoulders/a03_shoulder01.dbr` | `defensiveProtection` | 65.0 | — |
| weapon | *Poisoned Pusquill's Tail of Corrosion* | prefix | `records/items/lootaffixes/prefix/ao006b_poison_02.dbr` | `conversionInType/OutType/Percentage` | **Physical → Poison, 15.0 %** | 25.0 |
| off-hand | *Bernard's Slightly-Chewed Buckler of Protection* | base | `records/items/gearweapons/shields/b013a_shield.dbr` | `defensivePoison` | **15.0** | — |

**Archive-override audit (M):** all 30 records resolve in **exactly one** archive each (26 `database`,
4 `gdx1`/`gdx3`). No later-archive override shadows any of them, so the read order is not load-bearing.

### 2.3 — Non-gear channels, checked and closed

| Channel | Contribution to the vector | Grade | Evidence |
|---|---|---|---|
| **Devotion** | **zero** | M | `totalDevotionUnlocked = 3`, `devotionPointsUnspent = 3`, all 62 `devotionLevel = 0` (`.gdc` `character_skills`) |
| **Player skills** (5 allocated + mastery bar) | **zero resistances** | M | `_classtraining_class10` · `onslaught1` · `werewolf1` · `werewolf1b` · `passive02` all dumped: **no `defensive*` field of any kind** |
| **Amatok's Pact aura** | **+16 `defensiveProtection` only — no resistances** | M | `records/skills/playerclass10/amatokpact1_buff.dbr`, rank-1 of `[16, 32, 48, …]`. Every other `defensive*` on the record is 0 |
| **Item-granted skills** | **none active** | M | `.gdc` `character_skills.itemSkills = []`. The amulet's `bloodofdreeg1`/`elementalinfusion1` and the belt's `soulscythe1` are `augmentSkillName` **+N-to-skill** bonuses on skills a single-mastery Berserker does not own — they grant nothing |
| **Components / augments** | **none equipped** | M | all 12 slots, `componentName`/`augmentName` empty |
| **`werewolf1b` (Blight of Ch'thon)** | 100 % Pierce → Chaos — **the player's OUTGOING damage** | M | `Skill_Transmuter`, same `conversionInType/OutType/Percentage` triple as the weapon affix (§4) |

**⇒ the vector in §2.1 is complete. Gear is the only source, and it is fully enumerated.**

---

## §3 — CAP AND STACKING LAW, CITED

**Cap (M, exact-original, `records/game/gameengine.dbr`):**
```
playerDefenseCap   = [80.0, 80.0, 80.0]        # indexed by difficulty; the fixture is Normal -> 80.0
monsterDefenseCap  = [100.0, 100.0, 100.0]
playerReflectCap   = 30.0
```
**⇒ player resistance cap = 80 %; monsters cap at 100 %. The asymmetry is a real design fact.**

**Overcap mechanism (M):** the `defensive<Type>MaxResist` family raises the ceiling above 80
(`defensiveColdMaxResist` 508 records, `defensiveFireMaxResist` 508, `defensiveAllMaxResist` 460,
`defensivePhysicalMaxResist` 421, etc.). **None appears on any equipped part of the fixture** ⇒
**effective cap is a flat 80 % on every element, and the fixture's highest value (poison, 40 %) is
half of it.** Nothing in the R3 vector is capped, clipped or wasted.

**Stacking (D — inferred, and the inference is named):** every `defensive<Type>` source found on the
fixture is a plain percentage on an item part; the vector above is their **arithmetic sum**, clamped
to the cap. This is the standard GD reading and it is what the `MaxResist` family presupposes (a
ceiling only makes sense over an additive pool).

> **CANNOT-ANSWER (L-2) — the resistance operator is not in the database.**
> Probe run: `records/game/combatformulas.dbr` dumped in full. It contains **exactly four damage
> equations** — `physcialDamageDefenseEquationDLEP`, `physicalDamageDefenseEquationDGP`,
> `shieldDamageReductionEquationDLEB`, `shieldDamageReductionEquationDGB` — plus PTH, OA/DA, and the
> per-type *offensive* scaling equations. **There is no resistance-application equation for any
> element.** `find . -name "*.tpl"` → 0 hits (EXT CA-3), so no field description exists either.
> The form `taken = raw × (1 − r/100)` is **D**, inferred from (i) the cap being a bare percentage,
> (ii) the UI rendering these as `tab1<Type>ResistanceNumber` rows, (iii) the absence of any other
> consumer. **It is not stated by the corpus. Label it D wherever it is quoted.**

### 3.1 — Jitter: the roll is a band, not a point (U — LOAD-BEARING on precision, not on the verdict)

Affix records carry `lootRandomizerJitter` (a percentage). The `.arz` value is the **nominal**; the
instance's roll is a function of the item `seed`, which the `.gdc` stores but whose PRNG is not in
the corpus.

**Two candidate conventions, and the corpus adjudicates neither:**

| convention | cold-resist band | evidence |
|---|---|---|
| **downward-only** `[v(1−j), v]` | **9.8 – 14.0 %** | the convention EXT §2.3 used; consistent with the tiered affix ladder (`ad003a_res_cold_01…06` = 14/22/30/40/55/68 at jitter 30/20/10/10/10/8 — the tiers tile with gaps) |
| **symmetric** `[v(1−j), v(1+j)]` | **9.8 – 18.2 %** | **fits the G-6 tooltip transcript better:** four read values *exceed* their `.arz` nominal — DA 13 vs 12 (j28), OA 8 vs 7 (j28), belt Health 98 vs 80 (j28), conversion 18 % vs 15 % (j25) — **and not one exceeds `v(1+j)`** |

**I do not rule it.** The competing explanation for all four over-reads is OCR error in the same
transcript that also produced a phantom *"+9 % Pierce"* on an item with no pierce affix and a
*"req. lvl 4"* against a `levelRequirement = 5`. **CANNOT-ANSWER (L-3):** the seed→roll PRNG is in the
binary, not the `.arz`; no `.tpl` states the jitter's sign.

**Consequence, and it is small:** cold resist ∈ **[9.8, 18.2] %** across both conventions.
Against a requirement of ≥ 68.8 % (§5) **the band is immaterial — every point in it fails by ≥ 3.8×.**

**FileDescription is a free cross-check worth banking (M):** on affix records, `FileDescription`
carries the designer's nominal as a string — `ad003a_res_cold_01` reads `'14'` against
`defensiveCold = 14.0`; `a029e_off_dmg%cold_01_ar` reads `'7%'` against `offensiveColdModifier = 7.0`.
**The `.arz` value IS the authored nominal. That much is certain.**

---

## §4 — THE CONVERSION CHANNEL: R-M1-1's third member has no defensive instrument in Grim Dawn

**R-M1-1** requires `mitigation_delta` to itemize *(a)* armour, *(b)* per-element resistance,
*(c)* **conversion / channel-shift**, citing the fixture's own *"18 % Physical→Acid conversion"*
(kit-spec v2 §1.7) as member (c). §1.7 then applies it to the **incoming** nova:
`R3 @ r=5 : phys 298.3 → 244.6 phys + 53.7 acid`.

> **That is a direction error, and it should be corrected before the build reads it.** (D, and the
> derivation is short.)

1. The field triple is `conversionInType` / `conversionOutType` / `conversionPercentage`. The
   **identical triple**, on the **same character**, is `records/skills/playerclass10/werewolf1b.dbr`
   (*Blight of Ch'thon*, `Class = Skill_Transmuter`, `Pierce → Chaos, 100.0`) — which kit-spec v2 §1.5
   establishes as **MEASURED + tooltip-confirmed OUTGOING** (*"claws' 237 flat and charge's 375 flat
   are CHAOS, not pierce"*). One field triple, one semantics.
2. The fixture's weapon affix is `records/items/lootaffixes/prefix/ao006b_poison_02.dbr`:
   **`Physical → Poison, 15.0 %`** (jitter 25) — *not* 18 % Physical→**Acid**. The 18 is a tooltip
   read; the source nominal is **15**, and GD's "Acid" damage is the `Poison` type
   (`offensiveBasePoison*` on the same weapon = the 6–12 Acid line). **Nominal correction: 15 %, band
   [11.25, 18.75] under the symmetric convention — the tooltip's 18 fits, the record's 15 governs.**
3. **GD has no incoming-damage conversion.** Corpus-wide sweep: `conversionPercentage` appears on
   1,247 `/gearweapons/`, 863 armour/accessory and hundreds of skill records — it is a damage-typing
   field on the *wearer's output*. The only defensively-named sibling, **`defensiveConvert`**, is not
   damage conversion at all: it sits almost exclusively on `skills/nonplayerskills*` (75 of ~100
   records) alongside `offensiveConvert*` / `retaliationConvert*`, i.e. **resistance to being
   charmed** — GD's *Convert* verb. No equipped item carries it.

> **⇒ For this fixture, `mitigation_delta` is a TWO-channel object on the defender: armour (physical
> only) and per-element resistance. Channel (c) exists in the kit, but it points the other way — it
> shapes the player's outgoing damage, not the nova's incoming payload.** R-M1-1's structural claim
> survives intact (*armour cannot cut an elemental-dominated hit*); its third member simply does not
> apply here. Flagged for gandalf, veto-open.

---

## §5 — WHAT THE MEASURED VECTOR DOES TO G-A (D — arithmetic over M inputs)

Nova constants from EXT §1.1–1.3 / M-1 spec §5.2, unchanged: per projectile **118 physical + 200 cold**,
`n(r) = 7.64/r + 1`, bands `{[0,2.5) ×0.50 · [2.5,9) ×1.00 · [9,12] ×1.40}`. Armour law
`taken = d − 0.70 × min(d, A)`, `armorDefensiveAbsorption = 70.0` (`combatformulas.dbr` + `gameengine.dbr`).

### 5.1 — Armour, restated from the `.arz` (this is the R3 armour input R-M1-4 also owed)

Sum of `defensiveProtection` over the ten equipped parts = **337.0**.
`defensiveProtectionModifier` = 4.0 (head suffix) + 4.0 (torso suffix) = **8.0 %**.

| reading | value | + Amatok's Pact `+16` |
|---|---|---|
| item-local modifier (R-M1-3's pick) | 342.36 | **358.36** |
| character-global modifier | 363.96 | **381.24** |

**Amatok's Pact was allocated mid-R2 (`play_time` ∈ (2918, 3619], G-6 F-G6-6) ⇒ its +16 was live at
death 2 (5453) and in R3.** (M + D.)

### 5.2 — Delivered payload at the death-2 engagement radii

`r = 5.0 m`, band ×1.00, `n = 2.528` ⇒ raw **298.30 physical + 505.60 cold** (803.90 total):

| A | cold resist | physical taken | cold taken | **TOTAL delivered** |
|---|---|---|---|---|
| **358.36** (`.arz` R3, item-local + aura) | **14 %** | 89.49 | 434.82 | **524.31** |
| 358.36 | 9.8 % (jitter-lo) | 89.49 | 456.05 | 545.54 |
| 358.36 | 18.2 % (jitter-hi) | 89.49 | 413.58 | 503.07 |
| 358.36 | 0 % (no helm) | 89.49 | 505.60 | 595.09 |
| **125.0** (the battery's door value, §6) | 14 % | 210.80 | 434.82 | **645.62** |

`r = 9.0 m`, band ×1.40, `n = 1.849` ⇒ raw 305.44 + 517.69: **536.84** at A = 358.36 / 14 %.

**Both reproduce the measured killing blow (≥ 541, a lower bound — the globe floors at 0) without
fitting, at every engagement radius.** That vindication of the composed model is unchanged.

### 5.3 — The G-A solve, redone on measured inputs

G-A ⟺ `W_pre / W_post = 2.12` (M-1 spec §1.1 identity). With the physical leg **already saturated**
(298.30 < 342.36, so +141 armour moves it by **0.00 HP**, not 16 — the spec's own point, sharpened)
and no defensive conversion channel (§4), the entire budget is the cold leg:

```
W_pre = 524.31   ⇒   W_post ≤ 247.31   ⇒   505.60 × (1 − r_cold) ≤ 157.83
                                        ⇒   r_cold ≥ 0.6878
```

| quantity | value |
|---|---|
| **required** `r_cold_R3` for G-A = 2.12 | **68.8 %** |
| **measured** `r_cold_R3` | **14.0 %** (band 9.8 – 18.2 %) |
| shortfall | **×4.9** (×3.8 at the most generous jitter reading) |
| ceiling at the 80 % cap | `W_post = 190.61` ⇒ `W_pre/W_post = 2.75` — **2.12 is reachable in principle, just not by this gear** |

**And the R2→R3 delta is the number that actually decides it.** The only cold-resist source in the
terminal set is the helm prefix. Two cases, and neither moves G-A:

| case | R2 cold | R3 cold | `W_pre` | `W_post` | **`W_pre/W_post`** |
|---|---|---|---|---|---|
| helm worn at death 2 | 14 % | 14 % | 524.31 | 524.31 | **1.000** |
| helm acquired at the boundary | 0 % | 14 % | 595.09 | 524.31 | **1.135** |

> **⇒ Against the death-2 nova, the fixture's own gear step produces a `W_pre/W_post` of 1.000–1.135.
> Not 2.12.** The sim's 1.000 is not, on this evidence, a modelling failure on the boss-tier
> nova — it is what the fixture's gear does.

---

## §6 — WHAT THE BATTERY DEFINES (answering the R2 half of the brief)

The brief asked for R2 *"if the battery defines resist-relevant gear there too."* **It does not — in
either regime.** (M, `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py`.)

`fixture_class_dict(...)` builds one calibration door (`:266-273`) whose entire content is:
`max_hp` · `armor` · `crit_chance` · `block_chance` · `block_value` · `lifesteal_percent`.

- **There is no player resistance key at all.** `elemental_resistances` is populated on every
  *opposition* row (`:332`, `:359`, `:389`, `:396` — `{"life": 0.10, "poison": 0.15}`) and on no
  player.
- **`armor = 125.0` is pinned identically on BOTH arms** (`:268`), commented
  `# >=109 gear + 16 Amatok aura [MEASURED-partial]`.
- **The R2/R3 difference in the battery is exactly two things:** `max_hp` 759 → 1607 (`:51-52`) and
  the poison DoT (`with_dot`, R3-only, `:227-237`).

> **⇒ the sim's gear step is a pure HP step. It has no resistance channel to move, and its armour
> does not move either.** That is the mechanical reason the S-3 falsification read 1.000 — and §5.3
> now says the *fixture* reads 1.000–1.135 on the nova too.

**One unit conflict to route (INFO, not mine to rule).** The M-1 spec §1.7 composes
`A: 342.36 → 483.36 (+125 Armor, +16 aura)`. But the battery's `125.0` **is the whole gear armour**
under the tooltip reading (`≥109 gear + 16 aura`), not a delta on top of the `.arz` sum of 342.36.
Adding them treats one estimate of total armour as an increment to another. Under the `.arz` reading
the R3 total is **358.36** (item-local) or **381.24** (character-global) — **not 483.36**. The
difference is immaterial to §5's verdict (the physical leg is saturated at every value ≥ 299) but it
should not travel into the build as a number.

---

## §7 — THE INSTRUMENT CONFLICT ON ARMOUR, NAMED AND NOT RESOLVED

Not my cell, but it sits under R-M1-3 and this pass surfaced it, so it is recorded rather than left
to be re-discovered.

| slot | `.arz` `defensiveProtection` | G-6 tooltip read | frame |
|---|---|---|---|
| torso | 58.0 | **58 Armor** ✓ | f324 |
| waist | 7.0 | **7 Armor** ✓ | f299 |
| shoulders | **65.0** | 16 Armor ✗ | f296, f331 |
| legs | **50.0** | 16 Armor ✗ | f325 |
| feet | **52.0** | 12 Armor ✗ | f333 |
| head | 76.0 | *(not read)* | f327 |
| hands | 29.0 | *(not read)* | — |

Two exact agreements and three disagreements of 3–4×. **Evidence on the tooltip side:** GD's
displayed armour really is much lower on shoulders/legs/boots than on chest, and 16/16/12 is what a
level-13 character looks like. **Evidence on the `.arz` side:** the record values are unambiguous, no
archive shadows them, and a corpus-wide sweep of `/gear*/` at `itemLevel 7–15` shows
`defensiveProtection` in the same 37–111 band across *all* slots — i.e. the DBR field is **not**
slot-differentiated the way the game's display is. **I searched for a slot-weight or armour-scaling
record and found none**: `records/game/` holds 200 records and none carries per-slot armour weights;
`gameiteminfo.dbr`, `gamerandomizerweights.dbr` and `combatformulas.dbr`'s six-region table
(Torso 26 / Legs 20 / Head 15 / Shoulders 15 / Arms 12 / Feet 12) **do not reproduce the ratios**
(65×0.15 = 9.75 ≠ 16; 50×0.20 = 10 ≠ 16; 52×0.12 = 6.24 ≠ 12).

> **CANNOT-ANSWER (L-4).** One of the two instruments is wrong about shoulders/legs/feet and the
> corpus does not say which. **Weight on the tooltip side:** the same transcript over-reads four
> affix values and invents a *"+9 % Pierce"* on an item whose prefix carries only
> `characterOffensiveAbility 7`, `defensiveLife 8`, `offensiveAetherModifier 8`,
> `offensiveLightningModifier 8`. **Weight on the `.arz` side:** it agrees exactly on the two items
> galadriel read at highest confidence, and it has no per-slot scaler to hide behind.
> **Consequence: `A_gear` is 337 (`.arz`) or ~109 (tooltip) — a 3× spread, and R-M1-3 pinned 342.36
> on the `.arz` reading while the battery pinned 125.0 on the tooltip reading. Both are live in the
> run simultaneously.** Routed to gandalf (R-M1-3) and galadriel (a re-crop of f296/f325/f333 would
> settle it in minutes). **It does not change §5's verdict** — the physical leg is saturated at 337
> and near-saturated at 125, and the gap G-A must close is on the cold channel either way.

---

## §8 — CANNOT-ANSWER LEDGER (probes named, per L-N)

| # | Question | Probe run | Why it terminates |
|---|---|---|---|
| **L-1** | The **R2 (death-2) gear set** | `.gdc` parsed — one equipment array, terminal state, `playTime 7096`; G-6 gear frames f296–f333 all at `play_time` ≳ 5800 with f323–f333 post-boundary; no third instrument | Nothing in the run captured R2 equipment. **Every "R2" gear figure in EXT §2.4 and M-1 §1.6 is R3 gear used as a proxy** — except the amulet, which §1 proves is R3-only |
| **L-2** | GD's **resistance-application equation** | `combatformulas.dbr` dumped in full — four damage equations, all physical/shield; `find -name "*.tpl"` → 0 | The operator is in the binary. `taken = raw × (1 − r/100)` is **D**, not M |
| **L-3** | The **exact rolled value** behind each jitter'd affix | `lootRandomizerJitter` present on every affix; item `seed` present in the `.gdc`; two conventions tested against the G-6 transcript (symmetric fits 7/7, downward fits 3/7) | The seed→roll PRNG is not in the `.arz`. Cold ∈ **[9.8, 18.2] %**; immaterial to §5 |
| **L-4** | Which instrument is right on **shoulders / legs / feet armour** | `.arz` records dumped; archive-override audit clean; slot-wide `defensiveProtection` distribution swept; `records/game/` enumerated for a slot-weight record; six-region table tested | No armour-scaling record exists in the corpus. 3× spread stands, routed (§7) |
| **L-5** | Does the **shapeshift suppress the shield's `defensivePoison 15`**? | `werewolf1.dbr` re-checked (`Skill_Shapeshift`, four `replacement*`, `activeSkillSet 1`) — no defensive field; G-8 §7.2 measured the block-chance panel row **absent** across `play_time` 2593–5785 | Block was measurably off; whether the shield's *resistance* went with it is unstated. **If it did, poison drops 40 → 25.** Cold is unaffected either way |

---

## §9 — WHAT gamora AND gandalf SHOULD CARRY

1. **R3 per-element resistance vector, MEASURED, complete:**
   `{cold 0.14, poison 0.40, aether 0.18, bleeding 0.10, vitality 0.08, chaos 0.08,
   fire 0, lightning 0, pierce 0, physical 0}`; cap **0.80**, no overcap, nothing capped.
   **Compile it verbatim. It is the R-M1-4 input, and it is not fitted.**
2. **R3 armour, MEASURED:** `.arz` gear sum **337.0**, `defensiveProtectionModifier` 8 %, Amatok
   `+16` ⇒ **358.36** (item-local) / **381.24** (character-global). **Not 483.36** (§6). Carry the
   §7 conflict with it.
3. **G-A is EVALUABLE and its 2.12 predicate is not reachable through the fixture's R3 gear**
   (§5.3): required `r_cold ≥ 0.688`, measured **0.14**. R-M1-4's NOT-EVALUABLE fallback does not
   fire — **the honest grade is a measured MISS with a source-side explanation, not an un-gradeable
   gate.** Whether the fixture's 2.12 therefore reflects *encounter composition* rather than
   *mitigation* is the conductor's question; §5.3's two cases both land at 1.000–1.135 on the nova.
4. **R-M1-1's channel (c) does not apply to this fixture** (§4). The conversion is **15 %
   Physical→Poison on the player's OUTPUT**; GD has **no** incoming-damage conversion. Do not build
   the spec's `phys 298.3 → 244.6 phys + 53.7 acid` step. The structural claim (armour cannot cut an
   elemental-dominated hit) is untouched and now doubly supported.
5. **The R2 vector is CANNOT-ANSWER** (L-1). If the build needs an R2 arm, run it as a **named
   bracket** — cold ∈ {0 %, 14 %} — not as a value. The amulet (poison 25) is **provably absent**
   from R2 (§1), so R2 poison ≤ 15 %.
6. **The freeze lock is uncountered in R3 as well as R2** — `defensiveFreeze = 0` on every equipped
   part. The 1.3–1.8 s action-lock lands at full duration in both regimes.
7. **The battery has no player resistance channel at all** (§6). M-1's build must add one to the
   GD-replica scenarios before the vector in (1) can land; `armor = 125.0` is currently pinned
   identically on both arms, so the sim's gear step is HP-only by construction.

---

## §10 — RECORDS AND ARTIFACTS USED (exact paths)

**Save** `_Fresh Character 01` (T11/G-7) via
`legolas/scratch/2026-07-28-gdc-parse-g7/{parsed.json, gear_resolved.json, gear_named.json}`
(blocks: `character_bio`, `character_skills`, `inventory`, `play_stats`).

**Engine / combat** `records/game/gameengine.dbr` · `records/game/combatformulas.dbr` ·
`records/game/gamerandomizerweights.dbr` · `records/game/gameiteminfo.dbr`

**Equipped bases** `records/items/gearhead/a03_head002.dbr` ·
`records/items/gearaccessories/necklaces/b001_necklace.dbr` ·
`records/items/geartorso/a02_torso002.dbr` · `records/items/gearlegs/a02_legs01.dbr` ·
`records/items/gearfeet/a02_feet02.dbr` · `records/items/gearhands/a02_hands01.dbr` ·
`records/items/gearaccessories/rings/a001_ring02.dbr` (×2) ·
`records/items/gearaccessories/waist/a02_waist001.dbr` ·
`records/items/gearshoulders/a03_shoulder01.dbr` ·
`records/items/gearweapons/blunt1h/b015b_blunt.dbr` ·
`records/items/gearweapons/shields/b013a_shield.dbr`

**Equipped affixes** `records/items/lootaffixes/prefix/{ad003a_res_cold_01, b_ar022_ar, aa006a_spimod_01,
b_ar030_ar, aa007a_lifemod_01, aa010a_damod_01, ao008a_lifeleech_01, aa006b_spimod_01, ao006b_poison_02}.dbr` ·
`records/items/lootaffixes/prefix/{b_ar104_ar_a}.dbr` (GDX1) ·
`records/items/lootaffixes/suffix/{b_ar014_arje, a019b_ch_da_02, b_ar002_ar, a005b_ch_att_cunspi_02,
a029e_off_dmg%cold_01_ar, a001a_ch_att_cun_02, a019a_ch_da_01, a032c_off_dmg%acid_01_we}.dbr` ·
`records/items/lootaffixes/suffix/{b_ar103_ar_a}.dbr` (GDX1)

**Player skills** `records/skills/playerclass10/{_classtraining_class10, amatokpact1, amatokpact1_buff,
onslaught1, werewolf1, werewolf1b, passive02}.dbr` (GDX3) ·
`records/skills/itemskills/item_defenseknockdownnova_01.dbr`

**Monster-infrequent chain** `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` →
`records/items/loottables/gearaccessories/tdyn_necklace_b01_slithnecklace.dbr` → `b001_necklace.dbr`

**Corpus-wide sweeps** all four archives: full field-name census (`defensive|convert|resist`);
`conversionPercentage` / `defensiveConvert` carrier distribution; `/gear*/` `defensiveProtection` ×
`itemLevel` × `armorClassification`; `ad00Na_res_*` affix ladders; whole-corpus reference sweep for
`b001_necklace.dbr`; archive-membership audit on all 30 equipped records.

**Engine** `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py`
(`:51-52`, `:227-237`, `:266-273`, `:332`, `:359`, `:389`, `:396`) — read-only.

**Tooling (new, this cell)** `legolas/scratch/2026-07-29-wr1-r3resist/p{1..15}*.py` →
`legolas/scratch/2026-07-28-gdc-parse-g7/{lib_corpus,arz_index}.py` →
`research/scripts/gd_arz_adapter_2026_07_24.py`. Read-only throughout.

---

*Downstream: gandalf (`RUN-CONDUCTOR`) — R-M1-4 discharged, R-M1-1 channel (c) contested (§4),
R-M1-3's `A` conflict routed (§7); gamora — the vector in §9(1) and the battery gap in §6; galadriel —
an f296/f325/f333 armour re-crop would close L-4; jack-ryan at Gate-2 — §5.3 is the number G-A will be
graded against, and it was measured before the battery ran. No canonical doc amended by this note.*
