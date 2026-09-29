# C-10 — `offensivePhysicalModifier` semantics, and the price of folding it (`C-I14-2`)

**Date:** 2026-09-29 · **Author:** legolas (UNKNOWN-RESEARCHER) · **Commission:** C-10, issued by the
KC2-PLAY conductor (gandalf) under the Commission Rule § 4.
**Boundary:** `C-I14-2` — the wave-level `offensivePhysicalModifier`, MEASURED at −18 % @ w151 →
−25 % @ w171, unfolded by the oracle since I-6. Direction DOWN; the oracle runs HIGH (×1.97).
**Mode:** read-only. No sealed cell opened, re-run or moved. Nothing fitted, nothing tuned (Law 3).

---

## 0 · VERDICT IN ONE PARAGRAPH

`offensivePhysicalModifier` is a **per-element percent-damage grant on the PHYSICAL leg alone** —
the monster-side instance of the player stat the client renders as **`+X% Physical Damage`**. It is
**not** the same stat class as `offensiveTotalDamageModifier`, which the client renders as
**`+X% to All Damage`**; the two sit in different template groups. ⚑ **But they sit in the SAME
ADDITIVE POOL**, and Crate says so in its own client string: every one of the sixteen per-element
character-sheet tooltips ends *"% All Damage is included."* So the composition is **`om += p/100`
into the existing pool, scoped to physical rows — gamora's z5 law exactly, one scope narrower.**
A second multiply is the wrong form. **Priced, it moves the oracle's pooled per-body intake from
4,822.7 to 4,717.5 hp/s/body — ×1.967 → ×1.924 the referent.** ⚑ **It does not close the gap, it
shaves 2.2 % off it, and at waves 159 and 160 it is worth exactly ×1.000** because every priceable
body there is already `physical_clamped` and its physical leg is zeroed before this term can reach
it. **A negative result is a result: `C-I14-2` is not the missing term.**

| | |
|---|---|
| **Semantics** | per-element `% Physical Damage`; instant physical rows only |
| **Grade — semantics** | **MEASURED-TEMPLATE (A)** — Crate's own authoring template, include chain traced end to end |
| **Grade — additive composition** | **DB-CITED + CLIENT-STRING-ATTESTED (B)** — Crate client string, corroborated by community; monster-side binary application NOT byte-verified |
| **Grade — the −18 → −25 values** | **MEASURED-EXACT**, byte-confirmed against the committed CSVs |
| **Crucible applicability** | **YES**, by template identity (§ 3) |
| **Priced effect** | **−2.18 % of instant per-body intake, pooled 151–160; ×1.000 at w159/160** |

---

## 1 · THE TEMPLATE CHAIN — traced end to end, and it closes

Surface 1 was the Crate authoring templates (`…/2026-08-08-kc2-halt-bundle/tpl/`, 808 files).
`offensivePhysicalModifier` appears in **exactly one** of them.

```
balancingadjustment_survivalmode_enemies03.dbr
  └─ gameadjustment.tpl                       ← carries spawnChampionMin/MaxAdj, the fields
     │                                           the survival wave table also carries
     └─ include: attributepak.tpl
        └─ include: Parameters_Offensive.tpl
           └─ Group "Offensive Physical"      ← offensivePhysicalMin / Max / Chance / XOR /
              └─ Variable offensivePhysicalModifier      Global / Modifier / ModifierChance
                   class = "array"   type = "real"   defaultValue = "0"   description = ""
```

**Three distinct groups, three distinct stat classes**, and the separation is Crate's own:

| Group in `Parameters_Offensive.tpl` | Field | Client string | Class |
|---|---|---|---|
| `"Offensive Physical"` | `offensivePhysicalModifier` | `DamageModifierPhysical` = `{%+.0f0}% {^E}Physical Damage` | per-element percent |
| `"Total Damage Modifier"` | `offensiveTotalDamageModifier` | `tagDamageModifierTotalDamage` = `{%+.0f0}% {^E}to All Damage` | all-element percent |
| `"Damage Multiplier"` | `offensiveDamageMultModifier` | `tagDamageModifierDamageMult` = `{^E}Total Damage Modified by {^H}{%.0f0}%` | **true multiplier** |

⚑ **THE NAME COLLISION THAT WOULD HAVE MIS-RULED THIS COMMISSION.** Two different fields carry the
English words *"total damage"*. Community sources say *"there are a few multiplicative things like
total damage"* — **that sentence is about `offensiveDamageMultModifier`, not
`offensiveTotalDamageModifier`.** The Crucible per-wave record carries the latter and **does not
carry the former at all** (it is absent from the record's nonzero field set and from the pinned
`pm4i_wave_damage_modifier.csv`). Reading the community line onto our field would have produced a
multiplicative composition from a source that was describing a different stat. The client strings
are what separate them, and they are named here so the next reader does not have to re-derive it.

`class = "array"` confirms the per-wave indexing C-6 F-1 decoded for the sibling fields.

---

## 2 · THE COMPOSITION RULE — additive into the pool, physical scope

**Crate's client string, verbatim, `tagCharStatsPhysicalPercentDmgInfo`:**

> *"The percent bonus to all Physical Damage dealt by attacks and spells, not including the bonus
> from Cunning. **% All Damage is included.**"*

Three claims in one sentence, all load-bearing:

1. **"all Physical Damage dealt by attacks and spells"** → the scope is the physical leg, and it
   covers **both** weapon rows and skill rows. Not weapon-only.
2. **"not including the bonus from Cunning"** → the **attribute** multiplier is a *separate stage*
   from this percent pool. This independently corroborates the oracle's `a_mult` architecture.
3. ⚑ **"% All Damage is included."** → the sheet's per-element percent figure **sums in** the
   `% All Damage` term. The two are **one additive pool**, not two multiplies.

The pattern is uniform across all sixteen families (Acid, Aether, Bleed, Burn, Chaos, Cold,
Frostburn, Electrocute, Fire, Internal Trauma, Lightning, **Physical**, Pierce, Poison, Vitality,
Vitality Decay) — sixteen independent strings, one rule, zero exceptions. And the authors
deliberately mark where the rule does *not* hold: the retaliation twin of every one of those
strings says *"% All Damage does **not** affect Retaliation damage."* **A source that distinguishes
its own exceptions is worth more than one that only states the rule.**

**Community corroboration (attested, secondary):** *"% damage is additive, and is applied after
conversion regardless if it's % all or damage type specific"*; *"+10% fire damage is the exact same
as 10% all damage"*; *"the only damage multipliers in the game are +n% Damage to &lt;Monster Type&gt; and
+n% Crit Damage."* Consistent across independent threads and consistent with the client string.

**Official Crate guide** (`grimdawn.com/guide/gameplay/combat/`): carries *"Percent Damage bonuses
affect all damage dealt of that type, which includes skills and weapon attacks"* — which
corroborates scope (claim 1) and **is silent on additive-vs-multiplicative.** Recorded as ABSENT
rather than stretched.

### The rule, in the oracle's own notation

```
instant rows:  om = M_inst + own_add                       (z5, unchanged)
               om += p/100   FOR damage_type == "Physical" ONLY     ← C-I14-2
               p = D_offensivePhysicalModifier + U_offensivePhysicalModifier
dot rows:      unchanged — M_dot[family] and nothing else
PCL rows:      unchanged — om = 1.0
leech rows:    unchanged — dropped from the health path (G3)
```

**The wrong form, named so it cannot be shipped by accident:**
`om = (M_inst + own_add) × (1 + p/100)`. At w151 on an inert body that is ×0.9 on a 1.82 pool
(1.638) where the correct form gives 1.64 — close here, and **not** close on a body with a large
own term: `nemesis_wendigo_01` at w160 has `own = 109`, where the wrong form removes 0.613 of pool
against the correct form's 0.21, a **2.9× over-read of the term's own size**.

**No clamp arises.** The pool minimum over the band is `1.82 − 0.18 = 1.64` on an inert body; it
never approaches zero, so the "does it floor?" question has no referent in band and **no clamp
should be written** (same reasoning `offense.dot_mult` already applies to `M_dot`).

---

## 3 · CRUCIBLE APPLICABILITY (KP-79) — YES, and the warrant is template identity

The values are read from `balancingadjustment_survivalmode_enemies03.dbr` — a **SurvivalMode**
archive record, i.e. mode-scoped to Crucible *by construction*. Under KP-79's CRUCIBLE precedence
(`… < SurvivalMode < SM1 < SM2 < SM3`, whole-record replacement) this record is the winner for the
path, and the W2e rowset already stamps `precedence_mode: "CRUCIBLE"` on the z3 wave rows.

**The applicability warrant is stronger than precedence alone, and it is this:**
`offensiveTotalDamageModifier` and `offensivePhysicalModifier` are **fields of the same record, at
the same array index (`wave − 1`), reached through the same template include chain, in the same
template file.** `offensiveTotalDamageModifier` from that record is already folded, load-bearing,
and measured to work (`M_inst = 1.82 / 1.83`, verified below). **There is no reading on which one
of those two fields applies to these bodies and the other does not.** Whatever mechanism delivers
the attribute-pak to a Crucible monster delivers both.

---

## 4 · THE VALUES — byte-exact against the committed CSVs

Confirmed independently in **two** committed artifacts (gladiator = `enemies03`):

`…/legolas/scratch/2026-08-08-kc2-halt-bundle/halt9_survival_wave_scaling_full.csv` and the
oracle's pinned `reincarnated-engine/data/kc2/pm4i_wave_damage_modifier.csv`.

| wave | `offensivePhysicalModifier` | `offensiveTotalDamageModifier` (D) | U pak | `M_inst` |
|---:|---:|---:|---:|---:|
| 151 | **−18.0** | 42.0 | 40.0 | 1.82 |
| 152 | −18.0 | 42.0 | 40.0 | 1.82 |
| 153–155 | −19.0 | 42.0 | 40.0 | 1.82 |
| 156–158 | −20.0 | 43.0 | 40.0 | 1.83 |
| 159–160 | −21.0 | 43.0 | 40.0 | 1.83 |
| 161 | −21.0 | 44.0 | 40.0 | — |
| **171** | **−25.0** | 56.0 | 40.0 | — |
| 200 | −50.0 | 130.0 | 40.0 | — |

**gamora's MEASURED −18 @ w151 → −25 @ w171 is confirmed exactly.** The I-6 declaration text in
`offense.py:284` reads *"−21.0 % per-type"* — that is the **w159/160** value, correct for the wave
it was written at and not a contradiction.

⚑ **The Ultimate pak's `offensivePhysicalModifier[8]` (Ultimate, solo) is `0.0` — a MEASURED ZERO.**
So the wave D term is the **only** unfolded instant-physical term. There is no second limb hiding.

### Sibling check — the DoT family is ALREADY folded, and there is no gap there

The same record carries `offensiveSlow{Bleeding,Cold,Fire,Life,Lightning,Physical,Poison}Modifier`
at **−61 @ w151 → −65 @ w171** — far deeper than the instant term, and the first thing that looks
like a second hole. **It is not one.** `offense.py:DOT_FAMILY_COLUMN` maps all seven into
`M_dot(family, w) = 1 + (D_family + U_offensiveSlowAllTypes)/100`, and the oracle folds them.
Nothing is owed on the DoT limb. Named here because its magnitude invites exactly the wrong
conclusion, and silence would have read as absence.

---

## 5 · THE PRICE — computed, not fitted

### 5.1 Instrument

gamora's W2e static pricing walk, **replicated limb for limb** — same loader
(`threat.load_profiles(dot_corrections=True)`), same candidate population
(`wave_engine.pools_for(w, bonus_spawns_enabled=True)`), same `threat.py:1826–1966` arithmetic,
same weapon-swing inclusion, same leech drop, pre-mitigation. **Replication verified on her own
published control:** `n_priced` matches her `⚑ per_wave_measure` at **all ten waves**
(151:16 · 152:20 · 153:21 · 154:13 · 155:12 · 156:19 · 157:27 · 158:18 · 159:6 · 160:9).

One thing is added and one only: the **physical split** of the fold-ON instant sum.

### 5.2 Result

| wave | `p` % | instant rows | of which Physical | **physical share of instant sum** | ratio A | **ratio B** |
|---:|---:|---:|---:|---:|---:|---:|
| 151 | −18 | 102 | 43 | 0.3937 | 0.9291 | **0.9683** |
| 152 | −18 | 154 | 57 | 0.3224 | 0.9420 | **0.9743** |
| 153 | −19 | 137 | 52 | 0.3877 | 0.9263 | **0.9681** |
| 154 | −19 | 83 | 29 | 0.1309 | 0.9751 | **0.9889** |
| 155 | −19 | 120 | 37 | 0.2354 | 0.9553 | **0.9800** |
| 156 | −20 | 119 | 50 | 0.2790 | 0.9442 | **0.9755** |
| 157 | −20 | 232 | 84 | 0.3571 | 0.9286 | **0.9691** |
| 158 | −20 | 117 | 45 | 0.3946 | 0.9211 | **0.9659** |
| **159** | −21 | 68 | **32** | ⚑ **0.0000** | **1.0000** | **1.0000** |
| **160** | −21 | 119 | **36** | ⚑ **0.0000** | **1.0000** | **1.0000** |
| **pooled** | | **1,251** | **465** | **0.25984** | 0.950165 | **0.978191** |

*A = separate multiply on the physical leg (REFUTED by § 2). B = additive into the pool (SURVIVING).*

**Hand-check (Discipline #11), w151:** `1 − 0.18 × 0.393743 = 0.929126` — matches column A to six
places. B runs higher than A because bodies carrying a large `own_add` have a larger pool, so the
same −18 is a smaller *fraction* of it; that divergence is the signature of the additive form and
is why the two candidates price differently at all.

### 5.3 ⚑ THE FINDING INSIDE THE FINDING — the term is worth exactly nothing at w159 and w160

The zeros at 159/160 are **not** missing data. Those waves price **32 and 36 physical rows**. Every
priceable body at both waves has `folds_attr = True` **and** `physical_clamped = True`, so
`type_mult = 0.0` zeroes the whole physical leg *before* `offensivePhysicalModifier` could touch it:

- **w159** (6 bodies, all clamped): `chthonianservitor_lunalvalgoth`, `humanwendigo_darkwood_01`,
  `korvaakmessenger_02b`, `skeletalgolem_stepsoftorment_01`, `wendigo_ancient_namadea`,
  `witchgod_finalboss`
- **w160** (9 bodies, all clamped): `statue_korvaaktombguardian` and the eight `nemesis_*` records

**The terminal boss board is exactly where the term cannot bite.** Compare w151, where all sixteen
priced bodies are `clamped = False` and the physical leg carries 39 % of the instant sum. **This
term is a trash-wave term.** Any expectation that it would help at the wave the referent dies on
is refuted by measurement.

### 5.4 Applied to the oracle

Against gamora's pooled sealed-cell figure (`SEALED-KMILL | SEP-ON`, salts 0–4, Leg B):

| | per-body intake | × referent (~2,452) |
|---|---:|---:|
| incumbent — term unfolded | 4,822.7 | ×1.967 |
| **B · additive into pool (SURVIVING)** | **4,717.5** | **×1.924** |
| A · separate multiply (refuted, for contrast) | 4,582.4 | ×1.869 |

⚑ **READ THIS AS AN UPPER BOUND ON THE EFFECT, NOT AS THE EFFECT.** The ratio is computed on the
**instant leg, pre-mitigation, supply-weighted**. gamora's realised 4,822.7 also contains DoT and
`percent_current_life` intake — and PCL alone was **43.26 %** of gross on the I-5 reference cell —
**neither of which this term touches.** Scaling the whole intake by an instant-only ratio therefore
*overstates*. The honest statement:

> **Folding `C-I14-2` correctly moves the oracle's pooled per-body intake into
> `[4,717.5, 4,822.7]` hp/s/body — i.e. `×[1.924, 1.967]` the referent. It removes AT MOST 2.18 %
> of the surplus.**

The referent comparator 2,451.8 remains **a ratio of two lower bounds** (gamora's own caveat,
carried forward unchanged).

---

## 6 · WHAT THIS DOES AND DOES NOT SETTLE

**Settles:** the semantics, the scope, the composition rule, the Crucible applicability, the values,
and the sibling DoT question. `C-I14-2` can be lifted from `SOURCE-UNLOCATED` to **priced and
foldable**, with the form written out in § 2.

**Does not settle — and this is the headline for the conductor:** ⚑ **`C-I14-2` is not the
explanation for the ×1.97.** It was the standing candidate because its direction was DOWN and the
oracle runs HIGH. Priced, it is worth ≤ 2.18 %, and at the two terminal waves it is worth **zero**.
**A ×1.97 surplus survives folding it at ×1.92.** Whatever is making the oracle over-lethal is
somewhere else, and this commission's most useful output is that one candidate can now be crossed
off on measurement rather than left open on plausibility.

### ⚑ A cross-seam inconsistency, flagged and NOT ruled on (not my seam)

`gd_boss_kit.OutgoingStage` (WR3 seam, `R-WR3-24(3)`) models this exact field as
**`physical_rider`, a SEPARATE MULTIPLY riding on top of `total_factor`** —

> *"`physical_rider` is the pool's per-element `offensivePhysicalModifier` and rides ON TOP, on the
> physical leg alone."* — `gd_boss_kit.py:198`

That is **candidate A**, which § 2's client strings refute. The scope call is right (physical leg
alone); **the composition call appears to be the wrong form.** `STAGE_S2_FULL` prices it at
`×1.06` for a `+6.0` grant where the additive form would give `+0.06` into a `0.2625`-based pool.
I do not rule on this — `gd_boss_kit`'s stages are a **pre-registered enum** chosen by the
conductor precisely so they cannot be dialled, and re-basing one re-bases the WR1/WR2/WR3 evidence
chain that was measured under it. **Routed, not decided.** It is named here because a semantics
finding that corrected one seam and left its twin unexamined would be half a finding.

---

## 7 · KNOWLEDGE GAPS NOT RESOLVED — searched, and declared

1. **Monster-side binary application is NOT byte-verified.** The additive-pool rule is established
   from Crate's **player character-sheet** tooltips plus community attestation. The player and
   monster damage paths are the same code in GD as far as any surface here shows, and the sibling
   field from the same record demonstrably applies — but *"the sheet sums them"* is a statement
   about the sheet. A `Game.dll` probe of the damage-composition site would lift this from **B** to
   **A**. Precedent exists (the `invincible` gates at `Character+0x1844`). **Not attempted here;**
   the commission's surfaces were exhausted first, and the answer they gave is consistent.
2. **Official Crate documentation is silent on additive-vs-multiplicative.** Searched the official
   combat guide; recorded ABSENT rather than stretched. This is a **searched** absence.
3. **`offensivePhysicalModifierChance`** rides beside the field in the same template group and is
   **not** in the survival wave table. Whether an absent `…Chance` means *always* or *never* is the
   same undecidable as `offense.py`'s own note on `chance_pct` (blank on 3,934/4,035 rows read as
   NO GATE). Consistent with that incumbent reading; not independently established.
4. **The `physical_clamped` class-modal rule** (`10/10 nemesis bodies with a Physical row measure
   CLAMPED`) is load-bearing for § 5.3's zeros. It is the oracle's own MEASURED/CLASS-MODAL call,
   consumed here as given, not re-derived. If that clamp is ever narrowed, § 5.3's zeros move.

---

## 8 · SOURCE LIST

**Primary — Crate authoring templates** (`…/legolas/scratch/2026-08-08-kc2-halt-bundle/tpl/`):
`parameters_offensive.tpl` (Groups "Offensive Physical" L426–497, "Total Damage Modifier" L1532–
1573, "Damage Multiplier" L1626–1667) · `attributepak.tpl` (include chain) · `gameadjustment.tpl`.

**Primary — Crate client strings** (`resources/Text_EN.arc :: tags_ui.txt`, via
`…/legolas/scratch/2026-08-08-kc2-ed3-diff/tags_all.json`, 20,471 tags, build III):
`tagCharStatsPhysicalPercentDmgInfo` · `tagCharStatsPhysicalPercentRetInfo` ·
`DamageModifierPhysical` · `tagDamageModifierTotalDamage` · `tagDamageModifierDamageMult` ·
and the 15 sibling per-element `tagCharStats*PercentDmgInfo` strings.

**Primary — depot records under CRUCIBLE precedence (KP-79):**
`records/game/balancingadjustment_survivalmode_enemies03.dbr` (gladiator) and
`records/game/balancingadjustment_mp+difficulty_enemies01.dbr` (Ultimate pak), via committed
`halt9_survival_wave_scaling_full.csv`, `halt9_survival_scalars.csv`,
`data/kc2/pm4i_wave_damage_modifier.csv`, `data/kc2/pm4i_ultimate_offense_paks.csv`.

**Internal (oracle, read-only):** `kc2/offense.py` · `kc2/global_magnitude.py` ·
`kc2/discrete_volley.py` · `kc2/threat.py` · `simulation/gd_boss_kit.py` ·
`scripts/gamora_kc2_upn5_global_magnitude_lift_2026_09_29.py` ·
`math/kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md` + ADDENDUM ·
`output/kc2-play-w2e-oracle-intake-per-body-151-160-20260929.json` ·
`output/kc2-lifted-rows-KC2PLAY-SEALLAP-W2e-global-magnitude-fold-20260929_060558.json`.

**Tertiary — community mechanics** (corroboration only, never load-bearing alone; accessed
2026-09-29): Steam Community, Grim Dawn General Discussions —
`steamcommunity.com/app/219990/discussions/0/592899068297007760/` and sibling threads.
**Secondary — official Crate guide:** `grimdawn.com/guide/gameplay/combat/` (silent; recorded).

**Signed:** legolas, UNKNOWN-RESEARCHER.
