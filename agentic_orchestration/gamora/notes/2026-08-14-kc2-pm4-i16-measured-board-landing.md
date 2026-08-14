# KC2-PM4 · I-16 — **THE MEASURED-BOARD COMPLETION FOLD** — landing note

> **Run:** KC2-PM4 · **Iteration:** I-16 (the pre-chartered DECISIVE FOLD) · **Conductor:** gandalf
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** **R-PM4-39 part 3**, per **R-PM4-38 part 5** entire (ledger **L-29**, **L-30**).
> **Discharges `C-I14-1` · `C-I15-4` · `D-O-1` · `D-I15-6`.**
> **Math note (FIRST, its own commit):**
> `simulation/math/kc2-pm4-i16-measured-board-2026-08-14.md` — engine `e68991db`
> **Engine commits:** `e68991db` (math note ONLY) → `82e51e1c` (D-I15-6, its own) → `1b6f605c`
> → `cf156b32` → `276f5c13` → `0f57b646` → `06c31b67` → `13369796` → `718598f3`
> **Record cell:** `cluster_defon__critlo`, **DESIGNATED BY MEASUREMENT** — 0 divergent brackets.
> **Not pushed** — the conductor verifies from his own seat and pushes.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**The board is complete, and the completed board does not replicate the referent.** Every
previously-halted actor now carries its measured attribute and own-passive terms (`C-I14-1`
CLOSES: 188/188 actors on waves 151–160, **zero HALT on all three limbs**), and the monster hit
law is the sim's own d100 against a MEASURED per-body PTH (`D-O-1`: I-13's certainty override
rested on `hit_chance = 1.0`, which is `min(1, PTH/70)` saturated — **confirmed at the bytes, all
39 populated rows**). On the record cell the player now dies on **wave 155** with `l4l` **92.9796
s** — **T1, T2, T3, T4a, T4b(b) and T4b(c) all MISSED**, every miss named. ⚑ **And the honest
tension the charter pre-registered did not materialise, because the measurement says there was
only ever one half:** `S-HIT-ONLY` — the corrected PTH with the magnitude limb entirely off — is
**verdict-IDENTICAL to I-15** (death @160, `l4l 187.75510204081633` to the seventeenth digit, T1
MET, T2 MET) *despite substituting 663 PTHs and producing 212 misses*, while `S-MAG-ONLY`
reproduces the record cell exactly. **The two limbs do not compose; the magnitude limb is the
whole of it, and `D-O-1`'s correction is verdict-INERT on this board.** ⚑ **All three of my
pre-named STRUCTURAL candidates are FALSE. R-PM4-31 part 5's streak breaks at three, and it
breaks because I reasoned from a tick-walk that could not see the player's own sustain engine.**

---

## 1 — THE SCORECARD, THREE CELLS

**Record cell `cluster_defon/critLO`.** critHI stays RETIRED (R-PM4-37 part 2). Designation
STANDS — § 6's new-bracket test returns **0 divergent brackets of 5**, so no deferral is due.

| | camp/critLO | cluster-defoff/critLO | ⚑ **cluster-defon/critLO (RECORD)** | I-15 record |
|---|---:|---:|---:|---:|
| **T1** terminal | death @154 ✗ | death @155 ✗ | ⚑ **death @155 — ✗** | @160 **MET** |
| **T2** `l4l` | 83.0204 ✗ | 89.7959 ✗ | ⚑ **92.9796 — ✗** | 187.7551 **MET** |
| ratio to 182.7167 | 0.4544 | 0.4914 | ⚑ **0.5089** | 1.0276 |
| **T3** MAE (s) | — | — | **8.2765** ✗ (5 waves UNEVALUABLE) | 6.2170 |
| **T4a** mean `hp_frac` | — | — | **0.8731** ✗ (video 0.932) | 0.9173 |
| **T4b(b)** strict dwell | — | — | **0.0** ✗ (referent 1.6166) | 0.0 |
| **T4b(c)** fired | ✗ | ✗ | **✗** | ✗ |
| deepest single tick | 14,638.5 @w151 | 11,371.7 @w153 | **11,248.58 @w151** (0.5623) | 14,587.96 |
| PTH substituted | 222 | — | **237** | — |
| miss rate | 0.1889 | — | ⚑ **0.1797** | 0.0 on the L4 population |
| tiers seen | {0:283, 1:48, 2:4} | — | ⚑ **{0:286, 1:68, 2:2}** | flat tier 2 |
| per-wave floor | — | — | .4376 / .5336 / .5405 / .2272 / 0.0 | .8118 … .2708 / 0.0 |

**Every T on the record cell MISSES, and the scorecard names every one:**

```
T1  — death on wave 155 (player_death), target 160, near-miss band {159-161}
T2  — l4l 92.9796 s outside [155.31, 210.12] (ratio to 182.7167 = 0.5089)
T3  — per-wave pacing MAE 8.2765 s (I-15 read 6.2170); 5 of 10 waves UNEVALUABLE
T4a — mean hp_frac 0.8731 against the video's 0.932
T4b(b) — strict full-health dwell 0.0000 s against the referent's 1.6166 s
T4b(c) — deepest single tick 11,248.58 of 20,005 (0.5623)
```

---

## 2 — ⚑ THE `D-O-1` PROPAGATION AUDIT — VERDICT AND ITS CONSEQUENCE

### 2.1 The basis, stated, and the verdict

I-13's math note § 2.2 and its L4 row cite the basis **verbatim**:
`pm4m_body_chain.csv :: hit_chance = 1.0`, `crit_tier = 2`.

Measured from the vendored bytes: the column carries **39 populated rows and every one is exactly
`1.0`**, beside `pth_effective` ∈ [91.3009, 104.7171]. `1.0` is `min(1, PTH/70)` **saturated**.

⚑ **`D-O-1` CONFIRMED. I-13's "monster-side hit law = certainty (measured)" traces DIRECTLY to
`pm4m_lib.hit_chance` and rests on the PTH/70 mis-read.** The correction was not optional and is
taken.

### 2.2 ⚑ And the correction is a RETIREMENT, not an addition — which is the audit's real finding

`threat.resolve_hit` has implemented Lap O's documented law **since PM-2**, character for
character: floor 55 (`max(pth, PTH_MINIMUM)`), `roll > PTH` misses, sub-70 damage scalar
`p / NORMAL_PTH_DIVISOR`, the tier lattice, and cannot-miss at 100 (`randint(1,100)` can never
exceed a PTH ≥ 100). **The sim's law was right; I-13 overrode it.** Limbs (b) and (c) therefore
collapse to ONE change — retire the override, substitute the measured PTH — and **zero new to-hit
constants enter the model.**

Everything that consumed the mis-read is listed and **re-pulled by re-running**, never by
arithmetic adjustment. The supersession is enforced in the engine
(`_l4_on = volley.hit_law_on and self.board is None`), so a driver cannot re-arm the certainty law
on top of the measurement that retired it.

### 2.3 ⚑ AND THE CORRECTION IS VERDICT-INERT, WHICH I DID NOT EXPECT

| cell | death | `l4l` | T1 | T2 | T4b(c) |
|---|---:|---:|---|---|---|
| I-15 (incumbent) | @160 | 187.75510204081633 | MET | MET | ✗ |
| ⚑ **`S-HIT-ONLY`** (limbs b+c ALONE) | ⚑ **@160** | ⚑ **187.75510204081633** | **MET** | **MET** | ✗ |
| `S-MAG-ONLY` (limb a ALONE) | @155 | 92.9795918367347 | ✗ | ✗ | ✗ |
| ⚑ **RECORD** (all limbs) | **@155** | **92.9795918367347** | ✗ | ✗ | ✗ |

**`S-HIT-ONLY` matches I-15 to the seventeenth digit while substituting 663 PTHs and producing
212 misses.** The intake it produces is genuinely different (w151 25,623 → 31,254 = ×1.22;
w159 322,175 → 278,773 = ×0.865) — **the fold works and the outcome does not move**, because the
player's ADCTH sustain engine absorbs the journey and wave 160's volley overshoots the remaining
pool so far that `min(dmg, hp)` lands on the same tick either way.

---

## 3 — ⚑ THE PRE-REGISTERED HONEST TENSION: **THE HALVES DID NOT MOVE APART**

R-PM4-39 part 4 pre-registered that (a) would push the journey up ~5.36× while (b)+(c) pushed
wave 160 down, and that the two halves of T4b might separate. **Measured answer: they did not,
and the reason is that there is only one half.**

* Limb (a) is worth ×6.63 on wave 151 alone (25,623 → 169,879 applied) and kills the player on
  **wave 155**.
* Limbs (b)+(c)'s decrease is scoped to waves 159/160 — and **the completed board never reaches
  wave 159**. The decrease has nothing to act on.
* ⚑ **No constant was chosen to close the gap, because no gap opened.** Law 3's `moved` is the
  empty dict at top level (D-6b), 11 witnesses, zero new free constants.

⚑ **And the direction of (b)+(c) was mis-framed in the charter, which I said before the run in the
math note § 3.3:** the sim's own PTH is uniformly BELOW Lap O's on all 91 records (median 77.774
vs 90.612, delta **−12.865**, no exceptions) because `threat.effective_oa` declares `dexterityDV`
ABSENT. So the hit-law correction is a **board-wide damage INCREASE** (×1.155–1.170) with a
two-wave decrease at the end (×0.819–0.909) — not a small down-adjustment at wave 160.

---

## 4 — THE PRE-REGISTERED PREDICTIONS, GRADED — **6 / 18**, AND THE STRUCTURAL SET **0 / 3**

| # | claim | got | |
|---|---|---|---|
| P.1 | no span 151–158 reproduces I-15 | ⚑ **4 of 5 IDENTICAL to the tick** | ❌ |
| P.2 | T1 MISSED, death ∈ {151–153} | ⚑ **@155** (T1 missed ✓, band wrong) | ❌ |
| P.3 | T2 MISSED, `l4l` ∈ [8, 55] s | ⚑ **92.9796** (T2 missed ✓, band wrong) | ❌ |
| P.4 | T3 MAE > 12 s or unscoreable | **8.2765** | ❌ |
| P.5 | T4a ∈ [0.90, 0.99], ABOVE I-15 | **0.8731** (BELOW) | ❌ |
| P.6 | ⚑ strict dwell NON-ZERO ∈ (0, 0.50] | **0.0** | ❌ |
| P.7 | ⚑⚑ T4b(c) FIRES, deepest ∈ [18k, 30k] | **11,248.58**, does not fire | ❌ |
| P.8 | deepest at w151/154, skill a `chaosblast` | w**151** ✓, skill `swampgolem_stonethrash` ✗ | ❌ |
| P.9 | w160 volley moves FURTHER from the pool | w160 never reached; `S-HIT-ONLY` w159 14,339 < 15,000 | ✅ |
| P.10 | the substitution moves ZERO RNG draws | identical | ✅ |
| P.11 | crit histogram within one bin, no tier > 2 | tiers > 2 = **0** ✓; delta **47.95 pts** ✗ | ❌ |
| P.12 | fold-OFF byte-identity ×3, key ABSENT | key ABSENT 24/24 ✓; digests differ (§ 5.1) | ❌ |
| P.13 | ⚑ `S-HIT-ONLY` kills before 160 | ⚑ **@160, T1 MET, T2 MET** | ❌ |
| P.14 | `S-MAG-ONLY` kills before 160, ∈ {155–158} | **@155** | ✅ |
| P.15 | ⚑ `C-I15-4` closes GENUINELY | residual **5.82e-11**, sink **105,301.77**, 56 reductions | ✅ |
| P.16 | `U-O-1` verdict-IDENTICAL | identical on all three keys | ✅ |
| P.17 | `S-CLAMP-ALL` ∈ {153–156}, T1+T2 MISSED | **@156**, both missed | ✅ |
| P.18 | camp `l4l` below I-15's 83.0204 | **83.0204081632653 — EXACTLY EQUAL** | ❌ |

### 4.1 ⚑ THE STRUCTURAL PRE-NAMING — **0 / 3, AND THE STREAK BREAKS**

| candidate | verdict |
|---|---|
| **S-1** — *the hit-law correction is the DOMINANT limb; `S-HIT-ONLY` kills before 160 on its own* | ⚑ **FALSE.** `S-HIT-ONLY` is verdict-identical to I-15 to the seventeenth digit. |
| **S-2** — *T4b(c) fires, at the wrong wave, from a 9 m AoE* | ⚑ **FALSE.** T4b(c) does not fire at all (11,248.58 = 0.5623 of pool). |
| **S-3** — *the fold is bilateral, no span can be inert* | ⚑ **FALSE.** 4 of 5 spans are IDENTICAL to I-15 **to the tick** — and I-15's own S-3 had already established why (*"the player's damage is a continuous per-tick stream with NO CAST EVENT to defer, so the kill order is untouchable"*). **I contradicted a structural finding the run had already banked, and the run was right.** |
| **T-1 (throughput)** | ⚑ **CORRECT ON THE SIGN, a third time.** I said the tick-walk *prices the death EARLY* because it cannot see the counterplay re-actuating or the absorb pool saturating. Walk said **151**; truth is **155**. |

⚑ **The common root of all three, stated plainly: my tick-walk scaled I-15's *realised* damage
rows and modelled the heal stream as a capacity ceiling. It could not see that the player's ADCTH
sustain is ~1.5–3.3 M per wave against an intake of ~170 K — i.e. that on this board T1 is set by
the SUSTAIN ENGINE and not by the intake at all.** Every structural claim I made assumed intake
was the binding constraint. It is not, and that is the finding this lap actually produced.

---

## 5 — THE ASSERT WALL: **22 / 24**, AND BOTH REDS ARE MINE AND FAILED CLOSED

Spec in the math note § 9 (**W-5**), 24 checks / 24 scored, form rules W-1/2/3/6.
R-PM4-37 part 6 honoured on every check: `have()` **raises** on a missing key, and every check
carries `keys_asserted`.

### 5.1 ⚑ RED — check 1 (fold-off byte-identity). **My spec is UNSATISFIABLE by construction.**

I specified *"the fold-OFF replay reproduces I-15's three critLO surface digests EXACTLY"* **and**
limb (e) `C-I15-4`, which **deliberately changes that same wire** (it adds the counterplay sink to
`monster_deferred_arrival.⚑ conservation`). **A commissioned repair to a wire cannot coexist with
a byte-identity predicate over that wire, and I wrote both into the same note.**

⚑ **Diagnosed empirically rather than narrated** (Discipline #11): `git stash` the four modified
shared modules → replay **I-15's own driver** → dump `_surface` → restore → replay this driver
with `board=False` → `deep_diff`.

* The **pristine tree reproduces I-15's recorded digest `e64e0cb8…` EXACTLY**, so the tooling is sound.
* My fold-off arm reproduces a **fresh I-15 replay under my tree with ZERO differences**.
* Against the pristine surface: **39 differences, ALL of them under `⚑ conservation`** —
  `basis` ×10, `n_counterplay_reductions` ×10, `⚑ counterplay_absorbed_total` ×10, `residual` ×9.
  **Nothing else on any wave, event, track or actor moves.** (w151: residual 6,771.20 → 0.0;
  sink 6,771.20.)

⚑ **That is a STRONGER result than the check could have produced — but the check is scored as
specified and reported RED. It was not edited to pass** (jack-ryan's no-mid-lap-repair precedent,
R-PM4-33 part 3). Repair routed as **`C-I16-1`**: the predicate needs a declared exclusion scope,
not a digest.

### 5.2 ⚑ RED — check 12 (the seeded-draw tier control). **My predicate is mis-specified.**

Predicate: *"the realised crit-tier histogram matches Lap O's predicted masses to within one d100
bin, and no tier above 2 appears."*

* ⚑ **The substantive half PASSED: 0 tiers above 2**, exactly as Lap O predicts (0.0 mass at
  tiers 3–6 on all 95 bodies). The seeded-draw folding consumed the distribution correctly.
* ⚑ **The quantitative half is my error: I bounded a PERCENTAGE at n = 4–14 hits per body**, where
  a single crit is worth 7–25 percentage points. `swampcrab_ugdenbog_01` observed 1 crit in 14
  hits = 7.14 % against a prediction of 0.18 % and the bound reads 47.95 points. **The prediction
  is not falsified; the statistic is.**

Repair routed as **`C-I16-2`**: pool the histogram board-wide, or use a binomial interval.

### 5.3 The 22 GREEN, in the ones that carry weight

| # | what | measured |
|---|---|---|
| 2 | 3 substrate pins at FULL 64 hex | all EXACT |
| 3 | frozen `E-s09-cp150` | **20 artifacts, unchanged** |
| 4 | Law 3 `moved == {}` **top level** | `{}`, 11 witnesses |
| 5 | ⚑ attribute POSITIVE CONTROL vs Lap O's own columns | 169/169, max residual **4.90e-7** < 1e-6 |
| 6 | record-key validity (actor→record collapse) | **0 of 169** records carry two term tuples |
| 7 | ⚑ **`C-I14-1` CLOSURE** | **188/188 actors, ZERO HALT on all three limbs** |
| 8 | ⚑ **`C-I15-4`** | residual **5.82e-11**, sink **105,301.77**, 56 reductions |
| 9 | ⚑ `D-O-1` — L4 retired, PTH substituted | 237 substitutions, 0 misses suppressed |
| 10 | every substituted PTH inside the table's range | ✓ |
| 13 | determinism ×2 | **zero differences ×3** |
| 14 | ⚑ fold-forward exactness (object identity) | **0 divergent** of the records I-14 folded |
| 15 | ⚑ clamp discriminator control | **36/36 agree, 0 disagree** (45 untestable, no band-A row) |
| 16 | ⚑ cross-source own-term control | **15/15 AGREE** |
| 17 | ⚑ the level-basis conflict is INERT | all 6 disagreeing records are `halt_attr=False` |
| 20 | HP reconstruction | 3,746 rows, **max error 0.0** |
| 21 | the T4b(c) instrument names its wave AND its skill | w151, `swampgolem_stonethrash` |
| 24 | ⚑ `D-I15-6` | the `…103459` baton is ABSENT from the tree |

---

## 6 — THE BRACKETS: `U-O-1` PRICED, `U-I16-1` CLOSED BY MEASUREMENT, **0 DIVERGENT**

| bracket | death | `l4l` | T1 | T2 | T4b(c) | divergent? |
|---|---:|---:|---|---|---|---|
| ⚑ **RECORD** | @155 | 92.9796 | ✗ | ✗ | ✗ | — |
| `S-MAG-ONLY` | @155 | 92.9796 | ✗ | ✗ | ✗ | — |
| ⚑ `S-HIT-ONLY` | **@160** | **187.7551** | **MET** | **MET** | ✗ | *limb split, not a bracket* |
| `S-CLAMP-ALL` (`U-I16-1` LO end) | @156 | 108.4082 | ✗ | ✗ | ✗ | **no** |
| `S-LAPO-WIDE` (level basis) | @155 | 92.9796 | ✗ | ✗ | ✗ | **no** |
| `S-UO1-A` | @155 | 92.9796 | ✗ | ✗ | ✗ | **no** |
| `S-UO1-B` | @155 | 92.9796 | ✗ | ✗ | ✗ | **no** |
| `S-VOID-ON-DEATH` (I-15's) | @155 | 92.9796 | ✗ | ✗ | ✗ | **no** |

⚑ **0 divergent brackets of 5 → § 8's pre-registered deferral does NOT fire and the record-cell
designation stands.** It stands *even though every T misses on it*, because designation is a
measurement's consequence and never an outcome's (R-PM4-27 part 3).

### 6.1 ⚑ `U-I16-1` — the term worth 42 % of the player's intake, CLOSED rather than carried

Measured before the code: **50.52 % of the player's intake comes from attr-HALTED actors and
83.99 % of that is Physical-family**, so whether the newly folded bodies clamp decides whether
~42 % of all intake is multiplied by ~4.4× or set to **zero**. One undecided term dominated the lap.

**It is not undecided.** The clamp's substrate basis is `armorbase05.dbr ::
offensivePhysicalModifier = −135.0`, labelled in the corpus **"For Bosses"**. Joining
`kc2_s1_banda_record_inputs.csv :: armorbase_record` to Lap M's 36 measured clamp verdicts:

| armorbase | Lap M verdict | n |
|---|---|---:|
| `armorbase05.dbr` | **CLAMPED** | 8 / 8 |
| `armorbase04.dbr` | **NOT clamped** | 5 / 5 |
| no band-A row (all 23 `nemesis/` or `boss&quest/`) | CLAMPED | 23 |

**13/13 on the testable set, zero exceptions, and the corpus label independently says why.**
On the records I-16 newly folds the incumbent `clamp_for` and this independent discriminator
**AGREE 36/36, 0 disagreements.**

⚑ **`clamp_for` was NOT edited.** A rule may not be changed because 42 % of the intake turns on
the answer. `S-CLAMP-ALL` still ran, and it is not verdict-divergent.

### 6.2 `U-O-1`, priced before the code and confirmed after

Monster-side crit mass 0.77 % × a 0.243 multiplier gap = **0.19 % of intake**. Reading (a) and
reading (b) are **verdict-identical on all three keys**. **RECORD is NEITHER: the bare tier
multiplier, i.e. the incumbent.** Introducing a term whose composition rule is UNDECIDED is a
choice, not a measured decode. Carried as a sensitivity limb exactly as R-PM4-38 part 5 (d)
predicted.

---

## 7 — THE FOLD, AS BUILT

| limb | what | population | direction, MEASURED |
|---|---|---|---|
| **M1** | `(dex/245)+1` / `(int/215)+1` from Lap O | previously-HALTED only | RAISES (median 4.38×) |
| **M1b** | the physical clamp, through I-14's **unmodified** `clamp_for` | travels with M1 | REDUCES where it binds |
| **M2** | the body's own `offensiveTotalDamageModifier` | previously-HALTED only | RAISES (median +41 %) |
| **M3** | per-body MEASURED PTH keyed `(record, wave)` | 188/188 on w151–160 | ⚑ RAISES on trash (+16 %), REDUCES at 159/160 (−9…−18 %) |
| **M4** | ⚑ RETIREMENT of I-13's L4 certainty override | the 9 L4 records | REDUCES |

**The scope rule lives in `measured_board.trash_terms_for` and nowhere else**, and it has a
measured consequence: Lap M and Lap O **disagree on dex/int for 6 of the 15 records they share**
(a LEVEL-BASIS divergence — the own term AGREES **15/15**, which is the control that isolates it).
⚑ **All six are `halt_attr=False`, so the conflict is INERT on the record cell — reported, not
resolved by preference.** `_board_complete` returns the incumbent object *itself* on the identity
path, so fold-forward exactness is object-identity, not tolerance (check 14: 0 divergent).

**`C-I15-4`, repaired at the line that creates the sink.** `run.py`'s arrival block calls
`cp_layer.absorb(_dmg)` between the offer and the application; `note_counterplay(pre − post)` now
enters that reduction in the books. I-15's residual **254,105.87 → 5.82e-11**.

---

## 8 — ⚑ FOUR DEFECTS, ALL FRAMED

| id | what | disposition |
|---|---|---|
| ⚑ **`D-I16-1`** | **Discipline #12 SEMANTIC SHIFT.** *"the monster hit law is certainty at crit tier 2"* → *"the sim's own d100 against a MEASURED per-body PTH."* Every monster attack at w159/160 since I-13 is re-interpreted. ⚑ It is a **RETIREMENT of an override built on a mis-read column**, not a value change. | framed in the commit, MIGRATION § 1a, and **decisions-log entry PROPOSED** |
| ⚑ **`D-I16-2`** | the magnitude fold's population goes 23/344 → 344/344 | framed |
| ⚑ **`D-I16-3`** | `clamp_for` is unmodified but now reaches 154 records it never reached. **The rule did not change; its REACH did** — named because a rule evaluated on a branch it never exercised is a semantic event even when the code is untouched. | framed |
| ⚑ **`D-I16-4`** | **SELF-CAUGHT AT GRADING.** My three structural candidates all assumed *intake* is what sets T1. It is not — the player's ADCTH sustain is ~1.5–3.3 M/wave against ~170 K of intake, and 4 of 5 wave spans are identical to I-15 **to the tick** because the player's clear rate is untouched. ⚑ **I-15's own S-3 had already said this and I contradicted it.** | § 4.1; the lap's real finding |

---

## 9 — ARTIFACTS AND DIGESTS (FULL 64 hex, GL-6)

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i16-findings-20260814_073320.json`
`d9918dfa2cb6987c2598b1a0293f277667e76da648792218d0bd90e500642d02`

**Knot artifacts:**

| cell | sha256 |
|---|---|
| `camp-defoff-critlo` | `6a45b2fd363d6ecec0f8a4ea86723036cfb55c3eda991f3f6caa674bad1ef4ab` |
| `cluster-defoff-critlo` | `d2d249baca5d01a1cbc143557f09dc6dcfa8928a8c6f76cc692008e48178d4b1` |
| ⚑ `cluster-defon-critlo` **(RECORD)** | `fbc0546bc3f8cac4e8e8651187ddc24b4ffcc28376798320c2a46636e4aea7a7` |

**⚑ BATONS — three, 67/67 GREEN each** (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33):

| column | sha256 |
|---|---|
| `pm4-i16-camp-defoff-critlo` | `f8ffff292992bab50e366ba29a00ac7fd5140638a9d362d345990e3597a2c386` |
| `pm4-i16-cluster-defoff-critlo` | `85b9dbf97281cca804a47b6d9955b18a62d5208751bd67deee91065aec20fc68` |
| ⚑ `pm4-i16-cluster-defon-critlo` **(RECORD)** | `901de5821c49000309664e2036967feb5af4d5705709e618f0c73f0fc8895892` |

**The adapter's independent replay reproduces the driver to the digit on all three** —
83.0204081632653 / 89.79591836734693 / 92.97959183673467 under the driver's own `l4l` definition;
`end_reason player_death` on every one, `final_wave` 154 / 155 / 155. *(A reader summing
`t_end_s − t_start_s` gets 82.694 / 89.3878 / 92.5714 — that is 4-dp emitted-seconds rounding, not
a divergence.)*

**Determinism ×2 — ZERO differences on all three cells:**
`33a53f1e045a2733d080430c4e633333d2d72e7f2137d4bca5bb9a694b36b1ca` (camp) ·
`c9f1bae5e72f90e5b1a88e8f275d2ac29cb031d09faf84c76f69c7a0c9571188` (cluster-defoff) ·
`9f02be56e3b19b66cbbc290ca247cb39578e6dd2864fb5417e3f7e9df435a0cf` (**RECORD**)

**Fold-OFF arm** (`monster_measured_board` **ABSENT** on 24/24 waves, the tenth use):
`0d98ceb4630cdc22b18088b22a3d30ca374d401618177b874ec0247c33bcffd8` (camp) ·
`2d6979d71dfae258cf9740bb15d1609a4e3df1535d2e0130402068a7d1eb4655` (cluster-defoff) ·
`9f038789f3b39e9382a505bf678576253a15b39094b8a519cfaaea7ae61f03ae` (cluster-defon)
— **and § 5.1 proves these differ from I-15's recorded digests ONLY in the `C-I15-4` block.**

**Substrate pins (3, all MEASURED):**
`pm4o_trash_terms.csv` `fa75bc775aec80f926ad3bc272bd529a674cfe64dd375d909522e6b9fdf809ff` ·
`pm4o_oa_da.csv` `5c55998d0127ed776f8130d530fe02e035c17d7070dfe0e3fe7565a9b02cc564` ·
`kc2_s1_banda_record_inputs.csv` `ac50ef778555ec26e76559eb5932f2dd0b478f8f4f37038464c09a8d777f657e`

**D-I15-6, removed in its own commit (`82e51e1c`):**
`kc2-baton-v1-…-i15-camp-defoff-critlo-20260814_103459.json`
`4440bfeb36b02ae3a87bd8ce4e6885dea5e516035761a3a28b63cd2dade8ad49` — a pre-re-run artifact, never
graded, never digest-reported. The kept baton `…103934`
(`de3e2a99340771e27d36bded50553dee6e7413d405a163046bf5ea3ebdc8ed78`) is untouched.

**Frozen substrate `E-s09-cp150`: 20 artifacts verified, UNTOUCHED.**
**Law 3:** `law_3.moved == {}` **TOP-LEVEL** (D-6b), 11 witnesses. **Zero new free constants.**
**MIGRATION.md:** written **from the emitted bytes** — key diff `set()` in both directions on
`waves[0]`, top level, `actors[0]` and `config`; `events.columns` identical; `_schema_version`
1 → 1. **Zero telemetry schema changes.**

---

## 10 — TO THE CONDUCTOR

| id | what | disposition |
|---|---|---|
| ⚑ **`C-I14-1`** | 321 attr-halted / 193 own-halted actors | ⚑ **DISCHARGED.** 188/188 on the run's waves, zero ABSENT, zero HALT. |
| ⚑ **`C-I15-4`** | check-8 conservation | ⚑ **DISCHARGED.** Residual 5.82e-11 with a non-zero sink. |
| ⚑ **`D-O-1`** | the PTH/70 mis-read | ⚑ **AUDITED AND CLOSED.** Basis stated, consumers re-pulled by re-running, correction taken — **and measured VERDICT-INERT.** |
| ⚑ **`D-I15-6`** | the unreported camp baton | ⚑ **CLOSED**, own commit, digest recorded. |
| ⚑ **`U-I16-1`** | the trash physical clamp (42 % of intake) | ⚑ **CLOSED BY MEASUREMENT** — 36/36 + 13/13, incumbent rule untouched. |
| **`U-O-1`** | +% crit-damage composition | **IMMATERIAL monster-side** (0.19 %), verdict-identical, record = neither reading. |
| ⚑ **`C-I16-1`** | check 1's predicate is unsatisfiable beside `C-I15-4` | ROUTED to I-17 — needs a declared exclusion scope, not a digest. |
| ⚑ **`C-I16-2`** | check 12's statistic is sample-size-blind | ROUTED to I-17 — pool the histogram or use a binomial interval. |
| ⚑ **DECISIONS-LOG PROPOSED** | **`D-I16-1`** — monster hit/crit semantics. Proposed to jack-ryan via knight-rider, riding the end-of-run governance package beside `D-I15-2`. | awaiting |
| carried | T4b(b)/(c) unmet · T3 now FAR (5 waves UNEVALUABLE) · explosion-centre UNDECIDED · `D-I12-5` · Q57 | carried |

### 10.1 ⚑ ON R-PM4-39 part 5 — THE HONORABLE-EXHAUSTION BOUNDARY

The endgame R-PM4-39 part 5 pre-registered assumed *"T1/T2/T4a holding and T4b(c) still unfired."*
**That is not the board I have.** The completed, fully-measured board **loses T1, T2 and T4a that
I-15 held**, and it loses them to the magnitude limb alone — a limb built entirely from
digest-pinned measured terms with zero free constants and a 169/169 positive control on its own
arithmetic.

⚑ **The honest reading, and I will not soften it: the run's best replication (I-15, T1+T2+T4a MET)
was achieved on a board that was measurably INCOMPLETE, and completing it measurably breaks the
replication.** That is either (a) a real property of the model — one of the sim's other terms
(the player's ADCTH sustain, the clear rate, the cluster policy) is compensating for the missing
magnitude and is itself wrong; or (b) evidence that a term folded here does not belong on this
board.

**Neither is decidable from my seat, and no constant may be moved to choose between them.** The
named candidate for (a) is the ADCTH sustain engine, which this lap measured at 1.5–3.3 M of heal
capacity per wave against ~170 K of intake and which **no lap of this run has ever decoded** — it
has ridden `PLAYER_ADCTH_PCT = 21.0` since PM-2. ⚑ **If the conductor wants one more measured
route before the exhaustion exit, that is the one I would name.**

---

**Author:** gamora (simulation seam) · 2026-08-14 · **math note first, code second, and the git
order is the proof — including the eighteen predictions that graded FALSE.**
