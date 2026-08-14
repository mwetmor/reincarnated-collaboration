# KC2-PM4 · I-9 — landing note: **the sustain layer cannot reach the residual, and I can now prove it with its own bracket.**

> **Run:** KC2-PM4 · **Iteration:** I-9, THE SUSTAIN-ACTUATION FOLD · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** ruling **R-PM4-20** (charter ledger **L-16**), pre-registered at L-15.
> **Math note (Discipline #1, written and committed BEFORE the code — commit `ea15f6ae`, its own
> commit, so the git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i9-sustain-actuation-2026-08-14.md`
> **Judged against I-8, never I-7**, per my own I-8 § 12.1 caution which the charter made law.
> **Status:** COMPLETE. **No HALT.**

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> | class | source | sha256 |
> |---|---|---|
> | every **I-9** quantity | `simulation/output/kc2-pm4-i9-findings-20260814_022801.json` | **`a45b81548478387fe2bae5954b1c0f718416e8eef1add0a83f3c1996a53adf28`** |
> | every **I-8** quantity | `simulation/output/kc2-pm4-i8-findings-20260814_013948.json` | `a7aa1c472371dec5bcd3f3448015626b4c3b0b98e5cf44c7b921080110b3fb5e` |
> | the **measured HP trace** | `data/kc2/pm4h2_player_hp_frac_60fps.npy` (legolas Lap H-2, imported unmodified) | `692cd4115f93e7761e2ffe10089426ce096cc4abb263ce201b8ffec578c370aa` |
> | the **kit** | `data/kc2/pm4g_defensive_actives.csv` | `0cdfd3af9a22e2d6d7de59ca0b8238f0e2c04c64192a16dee894ef71ae0be306` |
>
> Both findings digests are verified **from bytes at run time by the driver** — a wrong digest
> HALTs the lap. **There is no unsourced number below.**

---

## 0 — The one-paragraph answer

**Does the DEF-ON reference cell die? NO — `arena_tier_exhausted` @ wave 171, exactly as at I-8.
And neither does anything else in this lap, including the cell that has War Cry withdrawn
entirely.** That is the run's convergence question answered in the first line, and the answer is
the finding. R-PM4-20 localised the residual onto greedy-optimal actuation of human-controlled
sustain. I executed the fold on the measurement, found **an invented constant of my own inside it**
(D-I9-1, priced at 19.428 % of all incoming damage), retired it by the run's own rule, **decoded
the potion's actuation threshold and measured I-4's 0.49 to be FALSE at five of its own nine
predicted actuations** — and then bracketed the term the instrument cannot see. ⚑ **The bracket
runs from 0 % to 29 % of every point of damage the player takes, and across that entire span
NOBODY DIES, NO WAVE CHANGES DURATION BY A SINGLE TICK, and mean HP moves 0.0087 against a 0.0563
gap to the video.** The human-actuated sustain layer is **outcome-inert on T1, T2 and T3**. It
moves HP observables and nothing else — and on those it moved **the right way**: the reference
cell's floor fell **0.4875 → 0.4238** and its excursion count fell **12 → 8** against the video's
**7**, the closest either has come in the run. **The pre-registered error in math note § 8.1
fires** (§ 9.1): I priced the actuation and not the damage-arrival process it responds to.

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 16 predictions, 20-check wall, the reframe declared pre-run) | `simulation/math/kc2-pm4-i9-sustain-actuation-2026-08-14.md` | **`ea15f6ae`** |
| 2 | `kc2/counterplay.py` — `WarCryLimb`, `PotionLimb`, `load_trace`, `trace_levels`, `falsification_census`, `menhir_positive_control`, `potion_threshold_trace_consistent`, `CounterplayLayer.warcry_folded` | modified (ADDITIVE; both limbs DEFAULT to the I-8 literals) | `8a826b67` |
| 3 | `data/kc2/pm4h2_player_hp_frac_60fps.npy` — legolas's 60 fps trace, imported UNMODIFIED | new substrate | `8a826b67` |
| 4 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `8a826b67` |
| 5 | **driver + 20-check wall + determinism + 7 sensitivity cells** | `simulation/scripts/gamora_kc2_pm4_i9_sustain_actuation_2026_08_14.py` | `8a826b67` |
| 6 | **3 knot supplies + findings** | `simulation/output/` | `fbbb2674` |
| 7 | **⚑ 3 BATONS** | `src/reincarnated/output/` | `ca19946f` |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

| what | sha256 |
|---|---|
| **findings** | `a45b81548478387fe2bae5954b1c0f718416e8eef1add0a83f3c1996a53adf28` |
| knots CAMP/DEF-OFF | `4561cf381ec2a04d805bb9497d67bb1265a858d8c5f53e6f6bd9c565a1263cd4` |
| knots CLUSTER/DEF-OFF | `b4fdf145edb02f235a828dcfcc9bbeb27c655b71d29331cceab0ca621c2ba91c` |
| **knots CLUSTER/DEF-ON** ← reference | `5aaab070db5036c7ec080a753d08ff088feb5952fff2b717bdf8c94b235c4c52` |
| **baton** CAMP/DEF-OFF | `3b2c5a3e8b59967c0dbad0a81d7104ef8b287e31bd120bd06d08cd6f9b790762` |
| **baton** CLUSTER/DEF-OFF | `d0953482b22ad9c74a3360327ec6d381ba1d031a757a97d340111e8a7dd9c7c0` |
| **baton** CLUSTER/DEF-ON ← reference | `aaea3e2ef2850c016d32dcc6efb588581509ca44b6c1a1a6e3ede973d0f5d1e4` |
| determinism surface CAMP/DEF-OFF | `8210322bfb82e4d8b0e30cfc396bc2fc301b376159b14f506a38c185b97d7689` |
| determinism surface CLUSTER/DEF-OFF | `fd112bb126daf5f546825e6bfc43f18051802912c4907f0ad68157d78a3274d2` |
| determinism surface CLUSTER/DEF-ON | `83701c4f35c08ec78006030d8dfe6818202083402e8db1e1da2e4c64a281bb06` |

All three batons emitted **FULL, 67/67 green** (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33) on a
**clean tree** — `AC-11.4e` correctly refused a FULL grade on a dirty one first, and that refusal
is on the record because it is the gate working.

**The I-8 batons these SUPERSEDE:** `a43d576621e1cbef5b97f392c42d02db7fb8041e27855dbfef8b5e1e42e84500`
/ `8513b23408ff2d0ab492987c95216cbd50d0302d45d47d7daa8f209b376e2f93` /
`7d4422fedc26c29a375597b0271c7f642668ce46b43820698fcc722aab10c35e`.

### 1.1 — ⚑ THE FOLD-OFF ARM IS BYTE-EXACT, AT TWO DEPTHS, AND THAT IS WHAT MAKES THE REST A MEASUREMENT

| layer | arm | declared (math note § 7) | measured |
|---|---|---|---|
| **1a** | I-8 config — `WarCryLimb.I8_LEGACY` + `PotionLimb.I4_EXCURSION_MAX`, **the DEFAULTS** | byte-EXACT vs I-8 ×3 | **EXACT ×3** — `0876b9c4…f223` / `4d97ec3d…5d8d` / `e2723731…4dbb` |
| **1b** | pre-I-6 arm (jacobi4, offense off, band-C off), same legacy kit | byte-EXACT vs I-5, **four folds back** | **EXACT ×3** — `5f616040…7fa7` / `0ad5b297…2605` / `95a34b2e…c7a4` |
| **1c** | default arm — no limb argument reaches `load_kit()` at all | EXACT | **EXACT** (the defaults ARE layer 1a) |
| **1d** | the three I-9 cells | divergent | divergent, as declared |

Unlike I-8, this iteration **could** hold byte-identity and it does. The design choice that bought
it is on the record: `warcry_folded` lives on the **layer**, not on `Kit`, because `Kit.as_dict()`
rides the emitted wire and a new key there would have broken 1a for a flag that is not a
measurement.

---

## 2 — ⚑ THE DISCRIMINATOR R-PM4-20 ASKED FOR IS A COLUMN, NOT A JUDGEMENT

`skillautocastcontroller.tpl` declares `triggerType` as an enum (`pm4g_field_evidence.csv`,
MEASURED), and Lap G read it field-for-field. **A row whose `trigger` is one of those enum values
is fired by a bound controller record. A row whose `trigger` is `manual` has no controller — it is
a keypress.** The table below is built from the CSV **at run time**, so it cannot drift from the
substrate.

| sim layer | record | `trigger` (MEASURED) | `duration_s` | `cooldown_s` | class | I-9 |
|---|---|---|---|---|---|---|
| **K-1** Turtle Shell | `devotion/tier1_29e_skill.dbr` | `LowHealth` 50 / chance 100 | — | 8.0 | **AUTOMATIC** | **UNTOUCHED** |
| **K-2** Arcane Barrier | `devotion/tier2_17c_skill.dbr` | `HitByEnemy` / chance 30 | — | 3.0 | **AUTOMATIC** | **UNTOUCHED** |
| **K-3** Menhir's Will | `playerclass01/willtolive1.dbr` | `LowHealth` 33 | **10.0** | 21.0 | **AUTOMATIC** | **UNTOUCHED** |
| **K-4** potion | `default/defaulthealthpotion.dbr` | *(consumable keypress)* | — | 12.0 | **HUMAN** | **θ 0.49 → 17/74** |
| **K-5** War Cry | `playerclass01/warcry1.dbr` | **`manual`** | ⚑ **EMPTY** | 7.5 | **HUMAN** | **duration 5.0 → 7.5; bracketed** |
| **K-6** Ascension | `playerclass09/ascension1.dbr` | **`manual`** | **10.0** | 24.0 | **HUMAN** | **UNTOUCHED** (§ 2.1) |

### 2.1 — K-6 is human, and it is left alone ON MEASUREMENT

Ascension's duration (10.0) and cooldown (24.0) are **measured**; only its actuation is
under-determined. Its whole contribution across 516 s of a 1.8 M-damage ladder is **480 hp
absorbed — 0.027 %**. Bracketing a term that cannot move the fourth significant figure of any
observable would be ceremony, and the reason is on the record rather than in my head.

---

## 3 — ⚑ THE POTION DECODE. THE INSTRUMENT HAS A POSITIVE CONTROL, AND I-4'S CONSTANT DIES.

### 3.1 — The predicate is ONE-SIDED, deliberately

`potion_instant = 800.0 + 0.25 × 20,005.0 = 5,801.25 hp = 0.28999 frac = **21.46 bar px of 74**`,
and the record is `instant_cast = True`. A predicted actuation is **FALSIFIED** iff, over the
0.25 s following the θ-crossing, **(a)** the maximum rise is below 5,801.25 hp **and (b)** the
minimum never dips below the crossing value — no damage arrived that could have cancelled the
heal. **The converse is never claimed:** the fight's own attack-leech produces single-frame rises
up to **+14,598 hp**, so a large rise identifies nothing. The test refutes; it does not confirm.

### 3.2 — ⚑ THE POSITIVE CONTROL: 3/3, and the lap would have HALTed at 2/3

K-3 Menhir's Will has a **decoded** trigger (`LowHealth` 33, cd 21.0) and a **measured** instant
(`skillLifePercent` 35 → **7,001.75 hp**). The same predicate, same trace:

| predicted fire | hp at crossing | max rise ≤ 0.25 s | ≥ 7,001.75? |
|---|---:|---:|---|
| t = 709.183 | 0.3243 | **+14,517 hp** | ✓ |
| t = 759.050 | 0.2973 | **+13,247 hp** | ✓ |
| t = 844.300 | 0.2297 | **+8,380 hp** | ✓ |

**3/3 at 1/74 bar resolution.** The math note fixed the response first: *"the instrument is not
validated and § 3 must be withdrawn, not patched."* It did not have to be.

### 3.3 — ⚑ I-4's 0.49 IS FALSIFIED AT FIVE OF ITS OWN NINE PREDICTED ACTUATIONS

| θ | predicted fires | **FALSIFIED** | the falsified instants (hp at crossing → max rise in 0.25 s) |
|---:|---:|---:|---|
| **0.49** ← the I-4 constant | **9** | **5** | 735.8 @ 0.3784 → **+1,622** · 749.1 @ 0.4054 → **+2,974** · 833.2 @ 0.3514 → **+1,622** · 847.8 @ 0.3784 → **+4,596** · **859.8 @ 0.2838 → +1,081** |
| **21/74 = 0.28378** | 3 | **1** | 859.4 @ 0.2838 → **+0** |
| **17/74 = 0.22973** | 2 | **0** | — |
| 14/74 = 0.18919 | 1 | 0 | — |

```
θ_potion  =  17 / 74  =  0.2297297297297297      ← RUN OF RECORD
```

**Computed at run time from the pinned trace and asserted (check 3); never a literal.** `17` is a
bar-pixel count the instrument produced; `74` is the measured full-bar width. The trace carries no
sample at 18, 19 or 20 px, so **every θ in `[17/74, 21/74)` yields an identical actuation schedule
on the measured trace** — the identification is an **equivalence class**, and 17/74 is its
representative at the instrument's own resolution. Reported as such, not as a point.

⚑ **And note where it lands: BELOW K-3's automatic 0.33 trigger.** On the measurement, the
reference player's potion was a *last resort behind his own circuit-breaker*, not a 50 %-health
reflex.

### 3.4 — ⚑ THE TERMINAL FACT R-PM4-20 ASKED ME TO CHECK — AND THE ANSWER IS **NOT THE COOLDOWN**

The ruling offered a mechanism and asked me to test it: *"potion presumably on its 12 s cooldown —
check the trace timing against the decoded cooldown; **if the trace supports it**, that is a
MEASURED mechanism."* **Checked. It does not. I am reporting the negative.**

* The last single-frame rise ≥ 5,801 hp **anywhere in the trace** is at **t = 844.317**
  (+8,380 hp — the Menhir control fire). From there to the trace's end at 864.833 is **20.5 s with
  no potion-magnitude rise — longer than the 12.0 s cooldown.** A cooldown cannot cover the
  collapse.
* ⚑ **The mechanism the trace DOES support is DEPTH.** The terminal collapse's measured floor is
  **0.28378 (21/74)**. The player's own decoded actuation depth is **0.22973 (17/74)**. **The
  collapse bottomed out FOUR BAR PIXELS above the depth at which he actually reaches for a potion.
  He did not use it because, by his own revealed policy, it never got low enough.**
* Menhir's Will **was** on cooldown throughout — fired 844.300, cd 21.0 → ready 865.300, past the
  trace's end. **That limb of the ruling's intuition is measured-CORRECT** — and it is the
  automatic layer, not the human one.

### 3.5 — ⚑ AND THE MEASURED TRACE DOES NOT END IN A DEATH

The commission and L-16 read *"terminal collapse 6.55 s to 0.28 **then death**"*. **The measured
trace does not carry a death.** Its terminal samples run `861.017 → 0.4324`, `862.717 → 0.8784`,
`863.017 → 0.9865`, and the **final sample is t = 864.833, hp = 0.9595 — alive, at 96 % health.**
The 856.1 excursion is followed by a **full recovery**.

**I am not asserting the player survived.** The trace ends ~1.2 s before the extraction window and
its 96.8 % coverage means the last samples could be dropped detections rather than the end of the
fight. **What I assert is the measured one: no death is in the substrate I was given, and every
T1/T4b comparison in this run has been made against a "terminal collapse" whose measured ending is
a recovery.** Routed to the conductor (§ 11.2).

### 3.6 — How many times did he actually use it? A BOUND, not a count

The test bounds θ from above; it cannot count actuations, because a rise ≥ 5,801 hp identifies
nothing. The honest bound, from the strict single-frame predicate (`Δt ≤ 0.02 s`, rise ≥ 5,801 hp,
`hp ≤ 0.70` before the rise): **9 candidate instants, of which the 12.0 s cooldown admits at most
7.** Relaxing to the instrument's own ±0.10 s smoothing window gives 12 candidates and at most 8.

> ⚑ **CORRECTION TO MY OWN MATH NOTE § 5, self-caught.** The note wrote *"12 candidate **single-frame**
> rises … at most 8"*. Three of those 12 span 3–8 frames, so under the strict single-frame
> predicate the figures are **9 and 7**. The note's number was the relaxed-predicate figure carrying
> a strict-predicate label. The bound's direction and every conclusion drawn from it are unchanged.

**Against that bound of ≤ 7–8 in 181.83 s, the I-8 sim fired the potion 2 times in 516 s.** ⚑ **On
rate, the sim's potion was UNDER-actuated, not over-actuated** — R-PM4-20's premise does not
localise here, and § 8 shows the fold's measured consequence.

---

## 4 — ⚑ D-I9-1: AN INVENTED CONSTANT, IN MY OWN I-4 FOLD, PRICED AT 19.428 % OF ALL INCOMING DAMAGE

### 4.1 — The defect, exactly

`pm4g_defensive_actives.csv`, row `records/skills/playerclass01/warcry1.dbr`: `trigger = 'manual'`,
**`duration_s = ''`**, `cooldown_s = '7.5'`, `offensiveTotalDamageReductionPercentMin = 29.0`. The
same column carries `10.0` for Ascension and `10.0` for Menhir's Will — **it is populated where
the substrate has it. War Cry's duration is MEASURED-ABSENT.**

`counterplay.py::load_kit`, landed by me at I-4:

```python
warcry_duration_s=5.0 if not wc["duration_s"] else float(wc["duration_s"]),
```

⚑ **A bare `5.0` literal with no citation, no `Cited(...)` wrapper, no entry in the kit's own
`basis` dict, and no mention in I-4's math note.** The K-5 basis string declares the *radius*
ambiguity and is silent on the duration. **It is exactly what GL-12 exists to catch, it has been on
the wire since I-4, and it is mine.**

**It was load-bearing to four significant figures:** `5.0 / 7.5 = 0.6667` uptime × 29 % = 19.33 %;
measured at I-8, `349,655.20 / 1,799,766.97 = **19.428 %** of `raw_seen`. **The literal was the
coefficient.**

### 4.2 — The replacement, by the run's own rule, applied DIRECTION-BLIND

The run had already ruled twice on a measured-absent duration, both at I-4: **C-I4-5** (*"spread
over the potion's own measured 12.0 s cooldown, **the only measured time constant the record
carries**"*) and **C-I4-4** (*"the lower reading here requires INVENTING a duration and is
therefore fictional"*). Both point the same way and neither is conditional on direction:

```
warcry_duration_s  =  cooldown_s  =  7.5 s      →  uptime 0.6667 → 1.0000
```

⚑ **This moves the reference cell AWAY from T1, and I applied it anyway.** `warcry_reduced / raw`
goes **0.194278 → 0.290000** on the reference cell — the player takes ~9.6 % less damage on the
lap whose purpose was to find his missing lethality. A precedent consulted only when it points
toward the target is not a precedent.

---

## 5 — THE THREE CELLS OF RECORD, AGAINST I-8

| cell | terminal | t (s) | mean HP EOT / **intra** | min HP EOT / **intra** | exc<0.70 EOT / **intra** | `n_potion` | `wc_red / raw` |
|---|---|---:|---:|---:|---:|---:|---:|
| **CAMP/DEF-OFF** I-8 | `arena_tier_exhausted`@171 | 1,940.49 | 0.994248 / 0.991347 | 0.292581 / 0.122740 | 18 / 33 | 7 | 0.184922 |
| **CAMP/DEF-OFF** **I-9** | `arena_tier_exhausted`@171 | **1,940.49** | **0.9946 / 0.9922** | **0.2505 / 0.2102** | **11 / 19** | **0** | **0.290000** |
| **CLUSTER/DEF-OFF** I-8 | `arena_tier_exhausted`@171 | 512.82 | 0.974846 / 0.964226 | 0.349989 / 0.334424 | 22 / 30 | 8 | 0.199978 |
| **CLUSTER/DEF-OFF** **I-9** | `arena_tier_exhausted`@171 | **512.82** | **0.9767 / 0.9675** | **0.3740 / 0.3103** | **14 / 22** | **0** | **0.290000** |
| **CLUSTER/DEF-ON** ← reference, I-8 | `arena_tier_exhausted`@171 | 516.00 | 0.986616 / 0.976994 | **0.487469 / 0.456801** | 12 / 22 | 2 | 0.194278 |
| **CLUSTER/DEF-ON** ← reference, **I-9** | `arena_tier_exhausted`@171 | **516.00** | **0.9883 / 0.9801** | ⚑ **0.4238 / 0.4233** | ⚑ **8 / 14** | **0** | **0.290000** |

> ### ⚑ THE FIRST ROW-PAIR IS THE FINDING: **`t` IS IDENTICAL TO THE CENTISECOND ON ALL THREE CELLS.**
> 1,940.49 / 512.82 / 516.00 — **the same numbers as I-8, digit for digit**, and the like-for-like
> 151–160 window is unchanged at **223.265306122449 s** on the reference. A sustain fold changes
> what the player *absorbs*; it changes nothing about what he *deals*, and the player never dies,
> so **not one wave's duration moved by a single tick.** ⚑ **T2 and T3 are structurally inert to
> this entire class of fold** — see § 7 and § 11.1.

> ### ⚑ AND THE SECOND FINDING: THE FLOOR FELL, AND IT FELL BECAUSE A FALSIFIED CONSTANT WAS HOLDING IT UP.
> The reference cell's min HP goes **0.487469 → 0.4238** (EOT) and **0.456801 → 0.4233** (intra) —
> **downward, toward the video's 0.28** — on a lap whose mitigation term got *stronger*. The
> mechanism is arithmetic: a potion firing at θ = 0.49 delivers **+0.28999 frac instantly at the
> bottom of the dip**, so a zero-latency θ = 0.49 policy **constructs a floor at θ**. I-8's min HP
> was **0.4875 against a threshold of 0.49** — the floor *was* the threshold. Removing the falsified
> constant (`n_potion` 2 → 0) lets the real trough show through. ⚑ **Part of the sim's HP floor at
> I-8 was an artefact of a number the video measures to be wrong.**

### 5.1 — The excursion count crosses toward the video

| | I-8 EOT | **I-9 EOT** | I-8 intra | **I-9 intra** | **video** |
|---|---:|---:|---:|---:|---:|
| reference cell, excursions < 0.70 | 12 | **8** | 22 | **14** | **7** |

**The EOT count is now one excursion away from the measured 7**, and the intra count has halved
its distance. This is the closest the run has come on this observable. It is reported as a
measurement, not as a hit: the two bases still straddle the target and the *depth* axis (§ 7.1)
still misses.

---

## 6 — ⚑ THE BRACKET (R-PM4-2) — AND IT DOES **NOT** SPAN THE OUTCOME BANDS

K-5's *actuation* is under-determined and cannot be measured: an HP trace cannot see a
damage-reduction (math note § 2). It was bracketed **before** the run.

| limb | policy | uptime | share of `raw` prevented | terminal | mean HP EOT / intra | min HP EOT / intra | exc EOT / intra | l4l 151–160 |
|---|---|---:|---:|---|---:|---:|---:|---:|
| **LO** `S-WC-LO` | K-5 **NOT FOLDED** | 0 % | **0 %** | **`arena_tier_exhausted`@171** | 0.979604 / 0.967512 | 0.3904 / 0.3239 | 13 / 36 | 223.2653 |
| **LO corner** `S-CORNER-LO` | K-5 not folded **AND** K-4 never | 0 % | 0 % | **`arena_tier_exhausted`@171** | 0.979604 / 0.967512 | 0.3904 / 0.3239 | 13 / 36 | 223.2653 |
| **HI** ← **run of record** | duration = cooldown, greedy | 100 % | **29.0 %** | **`arena_tier_exhausted`@171** | 0.9883 / 0.9801 | 0.4238 / 0.4233 | 8 / 14 | 223.2653 |
| *(I-8, retired)* | 5.0 s literal, greedy | 66.7 % | 19.428 % | `arena_tier_exhausted`@171 | 0.986616 / 0.976994 | 0.4875 / 0.4568 | 12 / 22 | 223.2653 |

> ### ⚑ P.15 IS ANSWERED, AND IT IS ANSWERED **NO**.
> The math note pre-registered: *"THE BRACKET SPANS THE OUTCOME BANDS … LO vs HI will differ by
> more than the whole distance from I-8 to any T-band edge on at least two of {mean HP, min HP,
> excursion count, terminal wave}."* **Measured:**
>
> * **terminal wave: IDENTICAL across the whole bracket** — 171 at both ends. Withdrawing 29 % of
>   every point of incoming damage does not kill this player.
> * **like-for-like duration: IDENTICAL to the tenth of a millisecond** — 223.2653 s at both ends.
> * **mean HP: 0.979604 → 0.9883, a span of 0.00870**, against a **0.0563** gap from I-9 to the
>   video's 0.932. **The entire bracket covers 15 % of the remaining divergence.**
> * **min HP: 0.3904 → 0.4238, a span of 0.0334**, against a **0.1438** gap to the video's 0.28.
>
> **The bracket does not span the bands. It does not even reach them.** ⚑ **The largest
> under-determined term in the player's entire defensive kit — 0 → 29 % of all incoming damage —
> is outcome-inert on T1, T2 and T3.** That is a stronger statement than the one I set out to test,
> and it is the result I take to the conductor (§ 11.1).

**`S-CORNER-LO` is byte-for-byte `S-WC-LO` on every reported observable**, because at
θ = 17/74 the reference cell's potion never fires anyway (`n_potion` = 0 in both). The
least-favourable corner and the LO limb are the same cell. **K-4 has no outcome content on the
reference cell at all.**

**`S-WC-LO-CLUSTER`** (the DEF-OFF cell, the one that died at I-7 and stopped dying at I-8, with
K-5 withdrawn): **`arena_tier_exhausted`@171**, mean HP 0.965028 / 0.951587, **min 0.2597 /
0.1097**, exc 20 / 42, `n_potion` **3**. ⚑ **Its intra-tick floor of 0.1097 is well BELOW the
video's 0.28 — the sim can reach that depth, it simply does not die there.** And it is the one
cell in the lap where the decoded threshold actually actuates.

### 6.1 — The remaining sensitivity cells (diagnostics, NOT matrix cells)

| cell | terminal | mean HP EOT / intra | min HP EOT / intra | exc EOT / intra | `applied` | `wc/raw` | `n_potion` |
|---|---|---:|---:|---:|---:|---:|---:|
| **reference** (record) | @171 | 0.988315 / 0.980070 | 0.4238 / 0.4233 | 8 / 14 | 978,868 | 0.290000 | 0 |
| `S-POTION-ONLY` (delta 1 alone) | @171 | 0.986019 / 0.976452 | **0.4204 / 0.4198** | 10 / 22 | 1,146,191 | 0.194354 | 0 |
| `S-WC-ONLY` (delta 2 alone) | @171 | 0.988493 / 0.980151 | **0.4962** / 0.4233 | 8 / 15 | 991,286 | 0.290000 | 2 |
| `S-WC-LO` (LO bracket) | @171 | 0.979604 / 0.967512 | 0.3904 / 0.3239 | 13 / 36 | 1,465,458 | **0.0** | 0 |
| `S-CORNER-LO` (LO corner) | @171 | 0.979604 / 0.967512 | 0.3904 / 0.3239 | 13 / 36 | 1,465,458 | **0.0** | 0 |
| `S-WC-LO-CLUSTER` (LO, DEF-OFF) | @171 | 0.965028 / 0.951587 | **0.2597 / 0.1097** | 20 / 42 | 1,642,401 | **0.0** | 3 |
| `S-CONV` (Lap-I HI DoT convention) | @171 | 0.988243 / 0.979971 | 0.4238 / 0.4233 | 8 / 14 | 982,454 | 0.290000 | 0 |
| `S-PCL` (the declared exclusion, priced) | @171 | 0.985474 / 0.974636 | 0.4439 / 0.4434 | 9 / 36 | 1,268,994 | 0.290000 | 0 |

**Law-3 note, unchanged from I-6 / I-7 / I-8.** `S-PCL` moves an observable and is **not adopted**;
its composition is UNDECODABLE-FROM-SUBSTRATE and not scaling is the lower reading. `S-CONV` moves
mean HP by 0.00007 and is carried unchanged.

---

## 7 — TARGET STATE T1–T4 (reference cell)

| band | target | measured | verdict |
|---|---|---|---|
| **T1** survival depth | death on wave **160** ({159–161} near-miss) | **no death; terminal wave 170** (`arena_tier_exhausted` @171) — **and no death at either end of the bracket** | **MISSED** |
| **T2** duration | 186 s ± 15 % (158.1–213.9) | **like-for-like 151–160 = 223.265306122449 s** (+20.0 %) — ⚑ **IDENTICAL to I-8, to the tenth of a millisecond** | **MISSED**, unchanged |
| **T3** pacing | per-wave clears correlate with 14/17/29 s | ⚑ **IDENTICAL to I-8** — median ratio 1.1479591836734695, pearson r 0.0042 | **NEAR/MISSED**, unchanged |
| **T4a** sustain-through-throughput | alive while clearing | mean HP 0.9883 over 6,321 ticks | **MET** |
| **T4b** fought terminal wave, ~6.55 s collapse | DoT-involved collapse | terminal wave 170 cleared in **18.122448979591837 s**, DoT **0.0183 %** of intake — ⚑ **identical to I-8** | **MISSED** |

⚑ **T2 and T3 did not move because they CANNOT move under this fold** (§ 5). Reporting them as
"unchanged" rather than as a verdict is the honest framing: no sustain change can reach them while
the player survives, because wave duration is set by the player's damage output.

### 7.1 — HP observables against the video, both bases

| | sim I-8 EOT | **sim I-9 EOT** | sim I-8 intra | **sim I-9 intra** | **video** |
|---|---:|---:|---:|---:|---:|
| mean HP | 0.986616 | **0.9883** | 0.976994 | **0.9801** | **0.932** |
| excursions < 0.70 | 12 | ⚑ **8** | 22 | ⚑ **14** | **7** |
| min / floor | 0.487469 | ⚑ **0.4238** | 0.456801 | ⚑ **0.4233** | **0.28** |

⚑ **THE DEPTH AXIS REVERSES DIRECTION FOR THE FIRST TIME SINCE I-6.** I-7's intra floor was
0.3273; I-8's rose to 0.4568 and I called it *"the player is now further from ever dying than the
fold that added lethality left him."* I-9 brings it back to **0.4233**, and the EOT floor to
**0.4238** from 0.4875. **Mean HP still diverges further** (0.9866 → 0.9883 against 0.932) — the
two statistics move in opposite directions, and both are reported.

---

## 8 — DECOMPOSITION: WHICH DELTA DID WHAT

`S-POTION-ONLY` and `S-WC-ONLY` exist so the lap can **attribute** rather than assert. Reference
cell, against I-8:

| observable | I-8 | **delta 1 only** (potion 17/74) | **delta 2 only** (War Cry 7.5) | **both** (record) |
|---|---:|---:|---:|---:|
| mean HP (EOT) | 0.986616 | 0.986019 **(−0.000597)** | 0.988493 **(+0.001877)** | **0.988315** |
| **min HP (EOT)** | **0.487469** | **0.420417 (−0.067052)** | 0.496209 (+0.008740) | **0.423841** |
| min HP (intra) | 0.456801 | 0.419826 **(−0.036975)** | 0.423313 (−0.033488) | 0.423313 |
| excursions (EOT) | 12 | **10** | **8** | **8** |
| `n_potion` | 2 | **0** | 2 | **0** |
| `applied` damage | 1,153,091 | 1,146,191 | 991,286 | **978,868** |

> ### ⚑ THE ATTRIBUTION IS CLEAN AND IT SPLITS THE TWO OBSERVABLES BETWEEN THE TWO DELTAS.
> **The floor is the potion decode's, entirely.** Delta 1 alone drops min HP by **0.067** while
> moving mean HP by **−0.0006** — it does nothing except remove the floor a falsified constant was
> holding up. **The excursion count and the mean are War Cry's.** Delta 2 alone takes excursions
> 12 → 8 and mean HP up by **+0.0019**, and it *raises* the EOT floor by 0.0087. **The two deltas
> push the floor in opposite directions and the potion wins by 7.7×.**

**And `S-WC-ONLY` carries the sharpest single number in the decomposition:** with the falsified
0.49 threshold restored, min HP (EOT) is **0.496209 — above the threshold, and the potion fires
twice.** With the measured threshold, it is 0.423841 and the potion never fires. **0.49 was not
measuring the player's behaviour; it was manufacturing a floor at its own value.**

---

## 9 — PRE-REGISTERED PREDICTIONS vs OUTCOME

Falsified predictions keep their original wording (the run's standing practice).

**Ten confirmed · two split · four falsified.**

| # | prediction | outcome |
|---|---|---|
| **P.1** | θ = **0.2297297297297297** exactly (17/74); falsifications **0** at 17/74, **1** at 21/74, **5** at 0.49; Menhir control **3/3** | **⚑ CONFIRMED ON EVERY LIMB** — and every limb is an assert-wall check (3, 4, 5, 6), all green |
| **P.2** | `n_potion` reference **2 → 0**; CAMP **7 → 0–2**; CLUSTER/DEF-OFF **8 → 0** | **CONFIRMED. 0 / 0 / 0** |
| **P.3** | `warcry_reduced` reference 349,655 → **490,000–540,000** (point **522,000**); `n_warcry` 69 ± 2 | **⚑ CONFIRMED — 522,969.32, and the point estimate is within 0.19 %.** `n_warcry` **69**, unmoved |
| **P.4** | `warcry_reduced / raw_seen` in **0.284–0.290** (point 0.288) | **CONFIRMED — 0.290000**, at the band's upper edge, because uptime is now exactly 1 |
| **P.5** | **T1: the reference cell does NOT die**, @171 | **CONFIRMED** |
| **P.6** | CLUSTER/DEF-OFF: no death either, @171 | **CONFIRMED** |
| **P.7** | **"The LO bracket cell (War Cry NOT FOLDED) DOES kill the reference player, and it does NOT do it on wave 160… I predict the wave is ≥ 165"** (stated at ~50 % on the death) | **⚑ FALSIFIED ON ITS MAIN LIMB, AND THE FALSIFICATION IS THE LAP'S FINDING. It does not die at all — `arena_tier_exhausted`@171 — and neither does `S-CORNER-LO` nor `S-WC-LO-CLUSTER`.** Removing 29 % of every point of incoming damage (**+486,590 applied**, 3.8× the perturbation I-8 added) does not move the terminal wave by one. The conditional limb is unevaluable |
| **P.8** | **T2 worsens** to **224–232 s** (point 227), still MISSED | **⚑ FALSIFIED — 223.265306122449 s, IDENTICAL TO I-8 to the tenth of a millisecond.** My band excluded "unchanged" entirely. The mechanism I missed is structural, not numerical: a sustain fold cannot move a clear time while the player survives (§ 5) |
| **P.9** | T3 median ratio in 1.13–1.17; \|r\| < 0.5; NEAR/MISSED | **CONFIRMED — 1.1479591836734695, r = 0.0042** — though trivially, since they are I-8's values unchanged for the same structural reason as P.8 |
| **P.10** | T4a MET; T4b MISSED, terminal wave 15–25 s, DoT < 0.1 % | **CONFIRMED — 18.122448979591837 s, DoT 0.0183 %** |
| **P.11** | mean HP EOT **0.9880–0.9915** (point 0.9895); intra **0.9790–0.9860** (point 0.9825) | **CONFIRMED both limbs — 0.988315 and 0.980070** |
| **P.12** | **min HP RISES**: EOT 0.4875 → **0.50–0.62**; intra 0.4568 → **0.47–0.60** | **⚑ FALSIFIED, BOTH LIMBS, WRONG SIGN — 0.423841 and 0.423313, both FELL.** I reasoned that stronger mitigation raises the floor and never asked what was *setting* the floor. It was the falsified potion threshold, and removing it drops the floor 7.7× harder than War Cry raises it (§ 8) |
| **P.13** | excursions EOT 12 → **4–12**; intra 22 → **10–22** | **CONFIRMED — 8 and 14.** ⚑ The pre-registered "shape to watch" was *"the EOT count may cross the video's 7 from above while the floor moves the wrong way"*: **the first half happened (8, one away from 7) and the second half did not — the floor moved the RIGHT way** |
| **P.14** | K-3 Menhir stays at **0** firings on the reference; K-1 Turtle **2 → 0–2** | **SPLIT.** Menhir **0** ✓ · Turtle **3 — it ROSE** ✗, and for the reason P.12 got wrong: the floor fell, so the trace crossed Turtle's 0.50 trigger more often, not less |
| **P.15** | **"THE BRACKET SPANS THE OUTCOME BANDS"** — LO vs HI differ by more than the distance from I-8 to any T-band edge, on ≥ 2 of {mean HP, min HP, excursions, terminal wave} | **⚑ FALSIFIED, AND IT IS THE MOST CONSEQUENTIAL RESULT IN THE LAP (§ 6).** Terminal wave identical; l4l identical; mean HP spans 0.00870 against a 0.0563 gap; min HP spans 0.0334 against a 0.1438 gap. **The bracket does not span the bands — it covers 15 % of the mean-HP divergence and 23 % of the depth divergence, and 0 % of the terminal one** |
| **P.16** | layers 1a/1b/1c EXACT, 1d divergent; determinism ×2 EXACT ×3; batons FULL 67/67; **wall 20/20** | **SPLIT.** 1a EXACT ×3 ✓ · 1b EXACT ×3 ✓ · 1c EXACT ✓ · determinism **0 differences ×3** ✓ · batons **FULL 67/67 ×3** ✓ · **wall 18/20** ✗ (§ 10.1) |

### 9.1 — ⚑ THE UNIFYING ERROR, SELF-NAMED — AND THIS TIME I NAMED IT BEFORE THE RUN

I-1 priced sustain not exposure · I-2 eHP not co-residence · I-3 throughput not reach · I-4 the
size of the counterplay not its shape · I-5 the repair not its convergence · I-6 the mean not the
variance · I-7 the numerator of a saturated ratio · I-8 the solver not the board it produces.

**I-9: I priced the ACTUATION and never priced the DAMAGE-ARRIVAL PROCESS that actuation responds
to** — and math note § 8.1 says exactly that, in those words, before the run:

> *"No actuation policy on a smooth trace can reproduce a sawtooth floor, and if the reference
> cell's floor stays high under both bracket limbs then the residual is in the VARIANCE of damage
> arrival — I-6's lesson, one level up — and I-9 will have measured a term that cannot reach it. I
> will report the sawtooth statistic whether or not it embarrasses this iteration."*

### ⚑ AND IT DOES EMBARRASS THIS ITERATION, SO HERE IS THE NUMBER.

The sim ticks at 12.25 Hz (0.081633 s) and the video samples at 60 Hz, so raw step counts are not
comparable. **The comparable quantity is how much health is lost inside one sim-tick's worth of
wall time**, and the video can be re-windowed to exactly that. Windows that span a coverage gap
(fewer than 4 sample intervals) are **rejected** — 72 of 10,629.

| | **video** (10,557 contiguous 0.081633 s windows) | **sim, reference cell** (6,321 ticks) |
|---|---:|---:|
| worst single-window fall | **−0.7838 frac = −15,680 hp** (t = 764.800 → 764.867) | **−0.18559 frac = −3,712.74 hp** |
| p0.5 of all windows | −0.1922 frac | — |
| p1.0 of all windows | −0.1351 frac | — |
| windows at or beyond the **sim's worst tick** | **62** | 1 (by definition) |
| windows ≤ −0.30 frac | **35** | **0** |

> ### ⚑ THE RESIDUAL, MEASURED: THE SIM'S SINGLE WORST TICK IN 6,321 IS A ROUTINE EVENT IN THE VIDEO.
> **The video contains 62 windows — 0.59 % of the fight — in which the player lost MORE health
> than the sim's reference cell loses in its single deepest tick out of 6,321.** And the video's
> top 35 bursts (≥ 0.30 of the bar in 0.0816 s) have **no counterpart in the sim at all**. Its
> worst is **4.2× shallower** than the video's worst.
>
> **The comparison is conservative in the sim's favour on two counts.** (1) A sim tick spans 4.9
> video frames, so it *aggregates* damage the video resolves separately — a sim tick should show
> LARGER falls, not smaller. (2) The video's instrument is a rolling MAX over ±0.10 s, which
> smooths the trace *upward* and can only SHRINK a measured fall, so −0.7838 is a lower bound on
> the true one.
>
> **This is where the residual is.** A player whose health never falls by more than 19 % of the bar
> in a tick cannot be killed by any actuation policy, because there is no moment at which his
> sustain is out-run. I-9 measured, priced and bracketed the entire human-actuated sustain term and
> proved it inert — and § 8.1 said before the run that this is what would happen and why.

---

## 10 — WHAT DID **NOT** CHANGE

**K-1, K-2, K-3 — trigger, magnitude, cooldown, order** (check 8) · **K-6 Ascension entire**
(check 9) · the potion's magnitudes, cooldown, charges and over-time limb · War Cry's magnitude,
cooldown and radius declaration · the monster side in every term · geometry, the converging solver,
τ, the non-overlap invariant (check 18) · the tick order · movement, cadence, dash layers · the hit
test (check 17) · every fold I-1…I-8 landed · the RNG (neither limb draws) · Law 3 (`moved: {}`) ·
the seed (conductor seed 9, Discipline #3) · the intra-tick HP instrument, which stayed ON.

**Determinism:** ×2 masked-EXACT on all three cells — **0 differences**, digests
`8210322bfb82e4d8b0e30cfc396bc2fc301b376159b14f506a38c185b97d7689` /
`fd112bb126daf5f546825e6bfc43f18051802912c4907f0ad68157d78a3274d2` /
`83701c4f35c08ec78006030d8dfe6818202083402e8db1e1da2e4c64a281bb06`.

### 10.1 — ⚑ TWO RED CHECKS, DECLARED, NEITHER REPAIRED TO GREEN

Wall reads **18/20**. **Both REDs are defects in MY OWN PREDICATES, not in the model**, and I-8's
§ 4.3 precedent applies verbatim: leave the measured RED standing and put the correctly-specified
quantity beside it.

**Check 12 RED — `warcry_reduced / raw_seen` in `[0.275, 0.290]`; measured
`0.2900000000000012 / 0.2899999999999949 / 0.2900000000000074`.** ⚑ **This is a ULP.** Two of the
three cells exceed my band's upper edge by **1.2e-15** and **7.4e-15**. The check is *right about
the world* — uptime is exactly 1 and the ratio pins to the measured 29 % — and *wrong about
floating-point*, because I wrote a closed band whose edge is the exact value the quantity converges
to. **I did not widen the band after seeing the number.** The correctly-specified predicate is
`abs(ratio − 0.29) < 1e-12`, which all three cells satisfy by three orders of magnitude.

**Check 18 RED — "pairs above tolerance == 0 on every cell"; measured `182 / 8 / 2`.** ⚑ **These
are I-8's numbers, digit for digit** (I-8 landing note § 4.2: *"pairs above tolerance are 2 / 8 /
182, not 0"*). **I wrote a check demanding zero for a quantity my own previous lap had already
MEASURED to be non-zero and declared as D-I8-2.** The check's *name* — "the invariant I-8 landed
survives" — is what it should have tested, and on that question the answer is **YES, exactly**:
182 / 8 / 2 at I-8, 182 / 8 / 2 at I-9, unmoved. The residual remains sub-micrometre and the cap
was not raised. **The predicate was mis-specified; the invariant is intact.**

### 10.2 — The eighteen that passed

Byte-identity at two depths (1, 2) · θ computed from the trace and asserted (3) · the positive
control 3/3 (4) · I-4's constant falsified 5/9 (5) · zero falsifications at the limb of record
(6) · War Cry's duration equals its own cooldown and 5.0 is retired (7) · **the automatic three
untouched, field by field (8)** · **K-6 untouched (9)** · counterplay conservation exact (10) ·
zero cooldown violations (11) · one-trajectory audit clean (13) · zero structural violations (14) ·
determinism ×2 EXACT ×3 (15) · Law 3 `moved: {}` (16) · the hit test untouched (17) · the
intra-tick HP invariant, 0 violations (19) · the I-9 basis keys absent on the legacy kit and
present on the kit of record (20).

### 10.3 — Match gates (INTERMEDIATE observables, judged SEPARATELY from T1–T4)

| gate | I-8 | **I-9** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring median | 0 | **0** | 1 | MISSED |
| **MG-2** ring p90 | 4 | **4** | 3 | MISSED |
| **MG-3** ring **max** | 17 | **17** | **10** | MISSED |
| **MG-4** moving fraction | 0.8411363275670528 | **0.8411363275670528** | 0.883 | MISSED |
| **MG-6** longest stationary | 1.3877551020408165 s | **identical** | ≤ 1.40 s | **MET** |
| **MG-7** dash rate | 5.375 s / 96 | **identical** | 5.3235 s | **MET** |

⚑ **Every gate is UNCHANGED from I-8, to the digit** — ring 0/4/17, moving fraction identical to
sixteen places. The gates measure geometry and movement; a sustain fold touches neither. Reported
in full because "unchanged" is a measurement, and because it is the same structural inertness § 5
found in T2/T3.

### 10.4 — ⚑ D-I9-2: I RAN TWO COPIES OF THIS LAP AT ONCE, AND CAUGHT IT MID-RUN

The first launch buffered its stdout, so I relaunched unbuffered **without confirming the first
process had died** — the shell wrapper was killed and its Python child survived. For roughly four
minutes **two processes were executing the same seed**, which is a **Discipline #3** violation.
Caught by inspecting the process table, and killed. **The record is uncontaminated and I can say
why rather than hope so:** the orphan was killed with `SIGKILL` while its stdout was still
buffered, so it never wrote a line to the shared log, and it had **not yet emitted a single
artifact** — `ls output/ | grep i9` was empty at the moment of the kill. Every I-9 artifact carries
the surviving process's stamp `20260814_022801`. **Named because a discipline violation that
happens to be harmless is still a discipline violation, and because the next one might not be.**

---

## 11 — ⚑ WHAT GOES TO THE CONDUCTOR

### 11.1 — ⚑ THE STRUCTURAL FINDING, AND IT IS THIS LAP'S ANSWER TO THE RUN'S CONVERGENCE QUESTION

**The human-actuated sustain term is OUTCOME-INERT on T1, T2 and T3, and I can now bound it rather
than argue it.** The bracket runs from **0 % to 29 % of every point of damage the player takes** —
the largest under-determined quantity in his entire defensive kit — and across that whole span:

* **the terminal wave does not move** (171 at both ends, on all three cells, plus the DEF-OFF cell
  that died at I-7);
* **no wave's duration moves by one tick** (l4l 223.265306122449 s at both ends);
* **every match gate is identical to sixteen decimal places**;
* mean HP moves **0.00870** against a **0.0563** gap to the video, and min HP **0.0334** against a
  **0.1438** gap.

**Three iterations have now perturbed this fight and been absorbed.** I-7 added 4,158 monster
damage and moved end-of-tick HP by nothing. I-8 added 129,150 and the trace got *healthier*. I-9
withdrew **486,590** — 3.8× I-8's perturbation, on the player's side this time — and the terminal
wave did not move. ⚑ **The residual is not a magnitude problem on either side. It is a VARIANCE
problem in damage arrival, and § 9.1 measures it: 62 windows of the video (0.59 % of the fight)
are deeper than the sim's single worst tick out of 6,321, and the video's top 35 bursts have no
counterpart in the sim at all.**

**My lean, offered as a lean and not a decision:** I-10 should be a **damage-arrival-variance**
iteration, not another magnitude fold — and it needs a decode first, because the sim's per-tick
intake distribution is currently the sum of many small independent draws and nothing in the
substrate has yet told us whether the real fight's bursts are (a) simultaneous multi-body alpha
strikes, (b) a monster ability with a large single hit, or (c) an instrument artefact of the bar
reader. **That is a legolas question before it is a gamora one.** The candidate substrate is
already named in this run: `top_incoming` is on every knot artifact, and the video's 35 deepest
windows have timestamps that a frame-level decode could attribute.

### 11.2 — ⚑ THE MEASURED TRACE CONTAINS NO DEATH, AND T1 IS ANCHORED TO ONE

Raised in the math note **before** the run (§ 3.4 above). L-16 and the I-9 commission both describe
*"terminal collapse 6.55 s to 0.28 then death"*. The substrate's last sample is **t = 864.833,
hp = 0.9595 — alive**, after a full recovery from the 856.1 excursion. It may be a coverage
artefact at the trace's edge; **I assert only the measured fact.** But T1's band ({159–161}) and
T4b's shape are the run's two hardest targets, and one of them is anchored to an event that is not
in the evidence file. **A conductor-level question about what T1 is anchored to — not mine to
answer.**

### 11.3 — D-I9-1 is closed; D-I8-3 is still open and still live

**D-I9-1** (the invented War Cry duration) is **closed** by this lap, and it was mine. **D-I8-3**
(`ManaBurnDrain` has no measured resistance row) is **carried unchanged** — no cell of record
reached it this lap, and the closure path is still a new mechanism, not a patch. **The bracket
cells got closer to it**: `S-WC-LO-CLUSTER` took an intra-tick floor of **0.1097** and fired three
potions, a trajectory no cell of record has taken. It remains a live HALT risk.

### 11.4 — Two RED checks and one Discipline #3 violation, all in § 10, none repaired or buried

Check 12 (a ULP in my own band) and check 18 (a predicate demanding zero for a quantity I-8 had
already measured as 182/8/2) are **left RED** with their correctly-specified answers beside them.
**D-I9-2** — two processes on the same seed for ~4 minutes — is named in § 10.4 with the evidence
that the record is uncontaminated rather than the assertion that it is.

---

**Author:** gamora (simulation seam) · 2026-08-14 · math note first, code second, and the git order
(`ea15f6ae` → `8a826b67` → …) is the proof.
