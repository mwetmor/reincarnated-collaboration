# KC2-PM4 · I-17 — **THE SUSTAIN FOLD** — landing note

> **Run:** KC2-PM4 · **Iteration:** I-17 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** **R-PM4-41 part 2** (ledger **L-32**), per **R-PM4-40 parts 2–6** (ledger L-31).
> **Folds onto:** the **I-16 INCUMBENT** board (`e68991db..718598f3`). Nothing in I-16 reverted.
> **Discharges `C-I16-1` · `C-I16-2`. Re-examines `D-I12-5`.**
> **Math note (FIRST, its own commit, ZERO code):**
> `simulation/math/kc2-pm4-i17-sustain-fold-2026-08-14.md` — engine `abba92b2`
> **Engine commits:** `abba92b2` (math note ONLY) → `d6e280be` → `d8d25eff` → `6199fc6e`
> → `b2f4da1e` → `01050e7c` → `fd902e05`
> **Not pushed** — the conductor verifies from his own seat and pushes.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**The sustain engine was decoded, folded, and it does not set T1.** On the record geometry the
player dies on **wave 155** with `l4l` **92.9795918367347** — **I-16's number to the seventeenth
digit** — under **BOTH** arms of the U-P-N-1 bracket, after a **×2.6** (DECOUPLED) and a **×10.6**
(COUPLED) cut to his heal stream. ⚑ **The bracket COLLAPSED on the four pre-registered verdict
keys**, so by the rule written down in the math note before any number existed, **no designation
is deferred and Lap Q's trigger is NOT met.** What the fold *did* move is **depth, not the
terminal**: record-cell mean HP **0.8731 → 0.8669 / 0.8090**, per-wave floors down 0.13–0.16,
offered heal 24.6 M → 6.34 M / 1.84 M. ⚑ **And the collapse must be read with `D-I17-6` beside
it: the verdict-key tuple is saturated at all-FALSE on this board, so "verdict-identical" barely
discriminates — 16 of 16 sensitivity limbs return it, including two that move the death from wave
155 to wave 151.** Wall **26/26 GREEN**. `law_3.moved == {}`, 23 witnesses, zero new free
constants. **Structural 2/3 — S-1 FALSE and reported false.**

---

## 1 — ⚑ THE BRACKET VERDICT TABLE — BOTH ARMS × ALL T TARGETS

**Record geometry `cluster_defon__critlo`.** critHI stays RETIRED (R-PM4-37 part 2).

| | ⚑ **COUPLED** | ⚑ **DECOUPLED** | I-16 incumbent | referent |
|---|---:|---:|---:|---:|
| **T1** terminal | **death @155 ✗** | **death @155 ✗** | @155 ✗ | 160 |
| **T2** `l4l` | **92.9795918367347 ✗** | **92.9795918367347 ✗** | 92.9795918367347 | 182.7167 |
| ratio to 182.7167 | 0.5089 | 0.5089 | 0.5089 | 1.0 |
| **T3** MAE (s) | **8.27647591836735 ✗** | **8.27647591836735 ✗** | 8.2765 | — |
| T3 waves UNEVALUABLE | 5 of 10 | 5 of 10 | 5 of 10 | — |
| **T4a** mean `hp_frac` | ⚑ **0.8089747588819975 ✗** | ⚑ **0.8668775591486296 ✗** | 0.8730850 | 0.932 |
| **T4b(b)** strict dwell | **0.0 ✗** | **0.0 ✗** | 0.0 | 1.6166 |
| **T4b(c)** (SCORECARD LAW) | **✗** | **✗** | ✗ | wave-160 kill from full |
| deepest single tick | 11,129.43 @w151 (0.5563) | 11,248.58 @w151 (0.5623) | 11,248.58 @w151 | ≥20,005 |
| ⚑ heal OFFERED | **1,836,929** | **6,343,978** | ~24.6 M | — |
| ⚑ heal LANDED | **578,377** | **594,864** | — | — |
| ⚑ zero-heal hit rows | **1,495** (all by resistance) | 1,408 (all by immunity) | 0 | — |
| per-wave floor 151→155 | .3087/.2967/.4232/.1609/0 | .4376/.4227/.5393/.2272/0 | .4376/.5336/.5405/.2272/0 | — |

### 1.1 ⚑ THE VERDICT KEYS, AND THE RULE APPLIED WITHOUT DISCRETION

| key | COUPLED | DECOUPLED | divergent? |
|---|---|---|---|
| `T1_MET` | false | false | **no** |
| `T2_MET` | false | false | **no** |
| `T4a_MET` | false | false | **no** |
| `T4b_c_fired` | false | false | **no** |

⚑ **`verdict_divergent = false` → designation `COLLAPSED — arms agree` → `lap_Q_trigger_met =
false`.** The rule was pre-registered in the math note § 3.2 before the run and is applied as
written. **No constant moved, and no arm was preferred.**

### 1.2 The other two cells, for completeness — **and they are NOT collapsed physically**

| cell | COUPLED | DECOUPLED |
|---|---|---|
| `camp_defoff__critlo` | ⚑ **death @152**, `l4l` 24.6531, T4a 0.8828 | death @154, `l4l` 83.0204, T4a 0.8505 |
| `cluster_defoff__critlo` | death @155, `l4l` 89.7143, T4a 0.7925 | death @155, `l4l` 89.7959, T4a 0.8751 |

⚑ **The camp control loses two whole waves under COUPLED.** All four verdict keys are FALSE on
both, so the *bracket* does not register it — which is exactly `D-I17-6`.

---

## 2 — ⚑ THE FOLD-OFF BYTE-IDENTITY PROOF, AND `C-I16-1` DISCHARGED

I-16's check 1 went RED because the same math note commissioned `C-I15-4`, a deliberate change to
the very wire the predicate demanded be byte-identical. **The repair the landing routed was a
DECLARED EXCLUSION SCOPE, and it is implemented as data, not prose:**

```
FOLDOFF_EXCLUSION_SCOPE: Tuple[str, ...] = ()      # ⚑ EMPTY — I-17 repairs no shared wire
```

| cell | fold-OFF digest (this lap) | I-16 recorded | |
|---|---|---|---|
| `camp_defoff` | `33a53f1e045a2733d080430c4e633333d2d72e7f2137d4bca5bb9a694b36b1ca` | same | ⚑ **EXACT** |
| `cluster_defoff` | `c9f1bae5e72f90e5b1a88e8f275d2ac29cb031d09faf84c76f69c7a0c9571188` | same | ⚑ **EXACT** |
| `cluster_defon` | `9f02be56e3b19b66cbbc290ca247cb39578e6dd2864fb5417e3f7e9df435a0cf` | same | ⚑ **EXACT** |

`player_sustain` **ABSENT on 14/14** fold-off waves (ABSENT-not-None, the eleventh use).
⚑ **This is the first clean fold-off byte identity since I-15, and the predicate now names its
own scope so it can never again be unsatisfiable by construction.**

---

## 3 — DETERMINISM ×2 — **ZERO DIFFERENCES ON ALL SIX PRIMARY CELLS**

| cell | pass-1 digest = pass-2 digest |
|---|---|
| `camp_defoff__critlo__COUPLED` | `723591794095abe226d6956470e8d8cce9f675ef309520a12419dbd477cc0dfa` |
| `camp_defoff__critlo__DECOUPLED` | `b5e1fcf2f5d05ecd9daec458655cb09672a6b19041c2b62b05296862f47345b3` |
| `cluster_defoff__critlo__COUPLED` | `d9824d9075dfc1061d4400c4f2417b7da79fc0e9a6c115361bff99a61e8f3d43` |
| `cluster_defoff__critlo__DECOUPLED` | `6db2f698b29d31a873488a28290a92e682ad062cb006f498086b386927103c7a` |
| ⚑ `cluster_defon__critlo__COUPLED` | `d1698fc32ffb1150715b2ba9e2fce6bab5c8f7f22564b5b9cb2a7eaf8cf30e81` |
| ⚑ `cluster_defon__critlo__DECOUPLED` | `3bcf7c7fbb1864a1e2a13cf10ba7d6420a11b7130384ac8a345dea4a59ae42c6` |

---

## 4 — ⚑ THE PRE-REGISTERED PREDICTIONS, GRADED — **16 / 22**

| # | claim | got | |
|---|---|---|---|
| P.1 | fold-OFF byte-identical, key ABSENT 24/24 | EXACT ×3, ABSENT 14/14 | ✅ |
| P.2 | ⚑ DECOUPLED verdict-identical to I-16 on T1+T2 | **@155, 92.9795918367347** | ✅ |
| P.3 | ⚑ COUPLED kills EARLIER, ∈ {152,153,154} | ⚑ **@155 — it does not kill earlier at all** | ❌ |
| P.4 | ⚑ the bracket is VERDICT-DIVERGENT | ⚑ **COLLAPSED** | ❌ |
| P.5 | T1 missed both arms, neither reaches 159 | @155 / @155 | ✅ |
| P.6 | COUPLED `l4l` ∈ [40, 92]; DECOUPLED = I-16 | COUPLED **92.9796** (above band) | ❌ |
| P.7 | T4a: DEC ∈ [0.83,0.88], COU ∈ [0.55,0.80] | **0.8669 ✓ / 0.8090 ✗** | ❌ |
| P.8 | T4b(b) dwell 0.0 both arms | 0.0 / 0.0 | ✅ |
| P.9 | T4b(c) does not fire; deepest unchanged | 11,248.58 @w151 unchanged (DEC) | ✅ |
| P.10 | ⚑ every survived wave clears in I-16's tick count | **5/5 and 5/5** | ✅ |
| P.11 | ⚑ `D-I12-5` unresolved a seventh time | **UNMOVED, both arms** | ✅ |
| P.12 | mitigation control in the BUILT code | 15,800/15,800, max err **0.005** | ✅ |
| P.13 | heal-composition control in the BUILT code | 31,600/31,600, max err **0.00175** | ✅ |
| P.14 | coverage ZERO absent | 95 pairs, **0 absent** | ✅ |
| P.15 | Resilience conditional EXERCISED | 384/79 (COU), 448/27 (DEC) | ✅ |
| P.16 | `S-D-P2-REGEN` verdict-identical | identical both arms | ✅ |
| P.17 | ⚑ `S-UPN4-EOR` identical under DEC, divergent under COU | **identical under BOTH** | ❌ |
| P.18 | `S-UPN3-AGG` kills before 152 both arms | **@151 (COU) / @155 (DEC)** | ❌ |
| P.19 | `S-CADENCE-LO` moves T1 on neither arm | @155 / @155 | ✅ |
| P.20 | `law_3.moved == {}`, ≥12 witnesses | `{}`, **23** | ✅ |
| P.21 | determinism ×2 zero differences ×6 | 6/6 | ✅ |
| P.22 | clamp 4/10, EoR not clamped, caps 0 | 4/10, 0.57, 0 | ✅ |

### 4.1 ⚑ THE STRUCTURAL PRE-NAMING — **2 / 3**, AND THE ONE THAT FAILED IS THE HEADLINE

| candidate | verdict |
|---|---|
| **S-1** — *the sustain engine is saturated, so a ×2.6 cut is worth nothing; **COUPLED at ×0.32-of-pool stops saturating and moves T1*** | ⚑ **FALSE.** COUPLED reproduces I-16's `l4l` **to the seventeenth digit** exactly as DECOUPLED does. **The saturation MECHANISM was right and the THRESHOLD was wrong** — cutting the heal to 9.4 % of the incumbent moved mean HP by 6.4 points and per-wave floors by 0.13–0.16 **and did not move the terminal by a single tick.** |
| **S-2** — *the spans are untouchable; every wave either arm survives clears in exactly I-16's tick count* | ⚑ **TRUE. 5/5 and 5/5 on the record geometry.** I-15's own S-3 said this; I contradicted it at I-16 and was wrong; I bet with the run this time and the run was right again. |
| **S-3** — *`D-I12-5` cannot be resolved by sustain, against the conductor's stated expectation at R-PM4-40 part 6* | ⚑ **TRUE.** w154 = **38.12244897959184 s**, ratio **2.700540426136037**, identical to the tick under **both** arms. **Unmoved a seventh time.** |
| **T-1 (throughput)** | ⚑ **CORRECT ON THE SIGN, a fourth time** — and by more than it has ever been. The walk priced COUPLED's death at "earlier than 152" and set the band at {152–154} to correct for it; truth is **155**, i.e. the walk was short by *at least* three waves and the correction was still not enough. |

⚑ **What S-1 got wrong, stated as mechanism rather than as an apology.** I computed the heal
offered per **contact** tick and compared it to the pool. That is the right comparison for
*overheal*, and the wrong one for *death*. The player dies in **dry** stretches — `dry_fraction`
0.41 whole-run, 0.33 over the final 200 ticks — where the heal is regen alone (**10.56 HP/tick**)
under **every** arm including the incumbent. Cutting a stream that is already zero at the moment
of death cannot move the moment of death. ⚑ **T1 on this board is set by the DRY FRACTION and the
burst ticks, not by the heal multiplier — and that is this lap's real finding.**

---

## 5 — THE ASSERT WALL: **26 / 26 GREEN**

Spec in the math note § 8 (**W-5**), 26 checks / 26 scored, form rules W-1/2/3/6.
R-PM4-37 part 6 honoured on every check: `have()` **raises** on a missing key; every check carries
`keys_asserted`; **check 26 verifies that every earlier check did.**

| # | what | measured |
|---|---|---|
| 1 | ⚑ fold-OFF byte identity, **exclusion scope ∅** (`C-I16-1` repair) | 3/3 EXACT, ABSENT 14/14 |
| 2 | 3 Lap P pins at FULL 64 hex | all EXACT |
| 3 | frozen `E-s09-cp150` | **20 artifacts, unchanged** |
| 4 | ⚑ `law_3.moved == {}` top level | `{}`, **23 witnesses** |
| 5 | ⚑ **mitigation positive control** | **15,800/15,800**, max err 0.005 |
| 6 | ⚑ **heal-composition control vs Lap P's own columns** | **31,600/31,600**, max err 0.00175 |
| 7 | ⚑ ADCTH: 5 rows → 20.0 exactly; sheet 21.0; D-P1 = 1.0; **fold constant == `threat.PLAYER_ADCTH_PCT`** | all hold |
| 8 | ⚑ 44 MEASURED-INACTIVE points ABSENT from the total | 44.0, absent |
| 9 | ⚑ >100 %WD clamp over all 10 rows | **4 clamp**, EoR 0.57, 0 mismatches |
| 10 | ⚑ `n_caps_applied == 0` (no cap invented) | 0 on all 6 cells |
| 11 | ⚑ coverage — zero ABSENT | 95 pairs, 0 |
| 12 | ⚑ ladder reproduced | 8 tiers exact, 7,900 rows |
| 13 | ⚑ `adcth_mult_DECOUPLED == 1.0` | 7,900/7,900 |
| 14 | ⚑ zero-life census 480 ∪ 230 = **490** | Lap P's own number, re-derived |
| 15 | ⚑ **the Resilience conditional is EXERCISED** | both 1.22 and 1.46, n > 0, all cells |
| 16 | ⚑ **limb (f)** — zero orphan heal ticks | **0** on all 6 cells |
| 17 | ⚑ player misses heal nothing — MEASURED-ABSENT control | `HIT_CHANCE == 1.0`, 27 immune records |
| 18 | ⚑ overkill proration live and sized | 235 rows, 1,174,662 forgone |
| 19 | ⚑ crit inertness (`U-P-N-5`) | `crit_mult == 1.0` on **100 %** of calls |
| 20 | determinism ×2 | zero differences ×6 |
| 21 | ⚑ the bracket + the designation rule | consistent, no discretion |
| 22 | ⚑ **T4b(c) SCORECARD LAW** (R-PM4-40 part 5) | enforced in the instrument |
| 23 | ⚑ **`C-I16-2` REPAIR** | pooled n=356, Wilson 95 % |
| 24 | ⚑ `D-I12-5` re-examination | reports, does not gate |
| 25 | MIGRATION from the emitted bytes | `added == ["player_sustain"]` |
| 26 | ⚑ every check carries `keys_asserted` | 25/25 |

### 5.1 ⚑ `C-I16-2` DISCHARGED — the statistic was falsified, never the prediction

I-16's check 12 bounded a **percentage** at n = 4–14 hits per body, where one crit is worth 7–25
points. The repair pools board-wide and uses a binomial interval:

```
pooled n = 356   observed crit rate = 0.0056180 (2 of 356)
predicted mass   = 0.0119469        Wilson 95 % = [0.0015420, 0.0202498]   ⚑ INSIDE
tiers seen       = {0: 286, 1: 68, 2: 2}        tiers above 2 = 0
```

⚑ **I-16's substantive half — zero tiers above 2 — PASSED then and passes now unchanged.**

---

## 6 — THE FOLD, AS BUILT, AND THE TWO CONTROLS THAT MAKE IT MEASURED

| limb | what | worth (median ratio to the incumbent heal) |
|---|---|---|
| **a** | ADCTH **21 %** SHEET-GOVERNED — 5 rows → 20.0, D-P1 residual 1.0, sheet governs | ×1.000 (**the constant did not move**) |
| **b** | weapon-damage fraction `0.57 × D_weapon` through the sim's OWN armour chain | ⚑ **×0.3098** |
| **c** | healing increase ×1.22 (+24 % Resilience below 66 %) | ×1.220 |
| **d** | leech-resistance ladder — **COUPLED** only | ⚑ **×0.250** (median), **0** on 490 body-waves |
| **e** | regen 129.38 hp/s, sheet-governed | unchanged |
| **f** | hit rate — the basis rides the existing `po_hits`-gated hit loop | by construction |
| | **DECOUPLED total** | **×0.37792** |
| | **COUPLED total** | **×0.09448** |

**Two positive controls, both stated in the math note BEFORE the module existed and both held in
the built code:**

* `applied_damage(0.57 × D_weapon, …)` reproduces Lap P's `weapon_portion_applied_LO/HI` on
  **15,800 / 15,800** cells, **max absolute error 0.005** — Lap P's own 2-dp publication precision,
  and **7,900/7,900 records resolve in the sim's mitigation table, zero ABSENT**.
* `0.21 × weapon_portion_applied × 1.22 × adcth_mult` reproduces Lap P's four `heal_per_hit`
  columns on **31,600 / 31,600** cells, **max error 0.00175** — i.e. **my fold and Lap P's table
  are the same arithmetic**, not two arithmetics that happen to agree.

⚑ **`D-I17-2`, the overkill proration, is a DECISION and is named as one.** The incumbent got
"overkill is not damage dealt" free from `applied = min(dmg, hp_body)`; the weapon-portion basis is
blind to remaining HP and had to be told. 235 prorated rows, 1,174,662 of basis forgone — reported
rather than assumed.

---

## 7 — THE SENSITIVITIES: **16 LIMBS, ZERO VERDICT-MATERIAL — AND THAT IS `D-I17-6`**

| limb | COUPLED | DECOUPLED | verdict-material? |
|---|---|---|---|
| `S-UPN4-EOR` (`U-P-N-4`) | @155, `l4l` 92.9796, T4a 0.8452 | @155, 92.9796, 0.8702 | no |
| `S-UPN2-RAW` (`U-P-N-2`) | @155, 92.9796, 0.8200 | @155, 92.9796, 0.8684 | no |
| ⚑ `S-UPN3-AGG` (`U-P-N-3`) | ⚑ **@151**, 7.9184, 0.8882 | @155, 92.9796, 0.8486 | **no** (all keys FALSE) |
| `S-CADENCE-LO` (limb f band) | @155, 93.3878, 0.8101 | @155, 93.2245, 0.8581 | no |
| ⚑ `S-WEAPON-LO` | ⚑ **@151**, 10.5306, 0.8218 | @155, 92.9796, 0.8563 | **no** (all keys FALSE) |
| `S-WEAPON-HI` | @155, 92.9796, 0.8366 | @155, 92.9796, 0.8703 | no |
| `S-D-P2-REGEN` (`D-P2`) | @155, 92.9796, 0.8075 | @155, 92.9796, 0.8662 | no |
| `S-HI-FLAT` (limb c isolation) | @155, 92.9796, 0.8004 | @155, 92.9796, 0.8658 | no |

* ⚑ **`D-P2` is INERT, exactly as priced** (33.58 hp/s = 2.741 HP/tick against a 20,005 pool):
  T4a moves 0.0015. **Reported either way, as the commission required.**
* ⚑ **`U-P-N-4` is NOT verdict-material under either arm** — P.17 predicted it would divide them
  and it does not. The two readings of the weapon basis differ by a factor of 1.84 and land on the
  same terminal.
* ⚑ **`U-P-N-3` and `S-WEAPON-LO` move the death by FOUR WAVES under COUPLED and still register as
  "verdict-identical."** That is the instrument's saturation, not agreement.

---

## 8 — ⚑ `D-I12-5` — RE-EXAMINED AT THE SUSTAIN FOLD, PER R-PM4-40 PART 6

| | COUPLED | DECOUPLED | I-16 |
|---|---|---|---|
| w154 span | **38.12244897959184 s** | **38.12244897959184 s** | 38.12244897959184 s |
| w154 ratio | **2.700540426136037** | **2.700540426136037** | 2.7005 |
| identical to I-16 | ⚑ **yes, to the tick** | ⚑ **yes, to the tick** | — |
| resolved by sustain | ⚑ **NO** | ⚑ **NO** | — |

⚑ **UNMOVED A SEVENTH TIME. The conductor's expectation at R-PM4-40 part 6 is NOT met, and I
pre-registered that it would not be (S-3) before running.** The mechanism is I-12's and it has not
changed: **51.2 % of wave 154 is a pet-TTL wait** — 19.51 s in which there is nothing left on the
board the player can kill. A heal multiplier changes no kill order, no clear predicate and no
targeting decision. **The debt carries, and it carries to the targeting/locomotion surface
(R-CPB-4), not to any offence or sustain limb.**

---

## 9 — ⚑ DEFECTS, ALL SELF-CAUGHT, ALL FRAMED

| id | what | disposition |
|---|---|---|
| ⚑ **`D-I17-1`** | **Discipline #12 SEMANTIC SHIFT.** *"ADCTH is 21 % of the player's applied damage"* → *"21 % of the mitigated, resistance-gated WEAPON PORTION, scaled by healing increase."* Every heal row since PM-2 is re-interpreted. ⚑ **The constant did not move; the quantity it multiplies did.** | math note § 9, MIGRATION § 1a, commit |
| ⚑ **`D-I17-2`** | overkill proration becomes EXPLICIT on the heal path | framed, counted on the wire |
| ⚑ **`D-I17-3`** | the heal multiplier is now **STATE-DEPENDENT** (reads player HP) | framed; wall check 15 requires it be exercised |
| ⚑ **`D-I17-4`** | a body can now be **UNLEECHABLE** — 490 of 7,900 body-waves | framed |
| ⚑ **`D-I17-5`** | **SELF-CAUGHT AT GRADING.** `spans_vs_I16` compares **every** cell against the **RECORD** cell's I-16 span vector, so the camp and cluster-defoff rows are not like-for-like (camp reads 0/2 and 1/4 for that reason alone). ⚑ **The record-cell rows — the ones S-2 and P.10 are graded on — ARE correct.** Not repaired mid-lap (NOTE-9). | ROUTED |
| ⚑ **`D-I17-6`** | **SELF-CAUGHT AT GRADING, AND THE CONDUCTOR NEEDS IT BEFORE READING § 1.** The four verdict keys are **saturated at all-FALSE** on this board, so "verdict-identical" has almost no discriminating power: **16/16 sensitivity limbs return it**, two of them while moving the death by four waves. ⚑ **The bracket's COLLAPSE is a statement about the KEYS, not about the physics** — the arms differ by a whole death wave on camp, 0.08 s of `l4l` on cluster-defoff, 6 points of mean HP on the record cell, and 47 baton events. | ROUTED — § 11 |

---

## 10 — ARTIFACTS AND DIGESTS (FULL 64 hex, GL-6)

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i17-findings-20260814_085045.json`
`df5dece1212f12974d314595c3ef1f71bd37ee1bc1bf9245c8bf33dab608f141`

**Knot artifacts (6):**

| cell | sha256 |
|---|---|
| `camp-defoff-critlo-coupled` | `10268892414ffb1da83563bd72e1c7cc11d61666a2ce7203b296ddc37b933a9c` |
| `camp-defoff-critlo-decoupled` | `5a66367d5cf42be51c2e8d84334313e32815cc8a4a7618332abf2e3ca62d100a` |
| `cluster-defoff-critlo-coupled` | `f4e484a4dbc96150c6c66228f051b76f2a4d5c17ef433edbda63b0e065622940` |
| `cluster-defoff-critlo-decoupled` | `3a868ff45bedd293aea342069e7ca1720101d519246ff399a7ffe28f234561cf` |
| ⚑ `cluster-defon-critlo-coupled` | `e9e217cb1abcb1e2f2bfa5dac9fcf25d5484c044fd6fd76adfb0e201f591b59e` |
| ⚑ `cluster-defon-critlo-decoupled` | `89b8c42531f249b37aa03b47e0d4c431ff5c60a722791e8c80563f4e5b5b02a0` |

**⚑ BATONS — six, 67/67 GREEN each** (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33):

| column | sha256 |
|---|---|
| `pm4-i17-camp-defoff-critlo-coupled` | `c1ba89369d390b27ad0d09a37e8e673f637f1a379058c0d9c1f7ddf74fa6644b` |
| `pm4-i17-camp-defoff-critlo-decoupled` | `39df38f39008553075336d9a6bf5a4cfeaef68843be44cf587b233046c89d530` |
| `pm4-i17-cluster-defoff-critlo-coupled` | `54a2ea2c19e9ab05f667612985732924f9fd930f002999fc9bb33dfff73db5a1` |
| `pm4-i17-cluster-defoff-critlo-decoupled` | `cda91df6ff203393734267f917b7ac63dc0a3ea0c1b2eac445cbc327440c47ab` |
| ⚑ `pm4-i17-cluster-defon-critlo-coupled` | `206522ff3e167161c55fdda6ecf2193e241394381c18c3f0b7b8a739f659f851` |
| ⚑ `pm4-i17-cluster-defon-critlo-decoupled` | `32cee2a68585d45a8102685d5d872ec50e7141cb1c4bd1cd5ef1d7dff185eb90` |

The adapter's **independent** replay reproduces the driver's terminal on every column —
`final_wave` 152 / 154 / 155 / 155 / 155 / 155. Summed tick spans read 24.4898 / 82.6939 /
89.3061 / 89.3878 / 92.5714 / 92.5714 against the driver's like-for-like 24.6531 / 83.0204 /
89.7143 / 89.7959 / 92.9796 / 92.9796 — **exactly one tick per wave**, the inclusive/exclusive
boundary convention this run has carried since I-13. *(I-16's own note records the identical
pattern: 92.5714 vs 92.9796.)*

**⚑ CONSUMED INPUTS, ALL RE-HASHED FROM THIS SEAT AND EXACT vs ledger L-32:**

| file | sha256 | rows |
|---|---|---:|
| `pm4p_adcth_sources.csv` | `5cd69906b71bc45a5c1a3c352c419967267dd73ac2415ba7b271d2ce2c7c9768` | 32 |
| `pm4p_attack_kit.csv` | `ebeaa728d09f19dd1178a02f31916184f0fb54cff6b51c91980cd7230d380c0d` | 10 |
| `pm4p_leech_resistance.csv` | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | 7,900 |
| `pm4p_findings.md` (read, not vendored) | `b7468e5c1ff37bff677d841499366c05b5c315af8a54207eb9dd24798edc1dee` | 512 lines |
| I-16 findings (pinned baseline) | `d9918dfa2cb6987c2598b1a0293f277667e76da648792218d0bd90e500642d02` | — |
| I-12 population baton (carried) | `6477057fe4f61bd7b5325fe5a17b93e8525fda0b2e708fc72f17e5a996c6367e` | — |

**Frozen substrate `E-s09-cp150`: 20 artifacts verified, UNTOUCHED.**
**Law 3:** `law_3.moved == {}` **TOP LEVEL**, **23 witnesses**, **zero new free constants** — every
number in `player_sustain.py` traces to a Lap P row or is arithmetic over Lap P rows.
**Test suite:** exit 0, twice.
**MIGRATION.md:** written **from the emitted bytes** — `added_keys == ["player_sustain"]`,
`removed_keys == []`, `EVENT_COLUMNS` identical, `_schema_version` 1 → 1.
**Zero telemetry schema changes.**

---

## 11 — TO THE CONDUCTOR

| id | what | disposition |
|---|---|---|
| ⚑ **`C-I16-1`** | check 1's predicate unsatisfiable beside `C-I15-4` | ⚑ **DISCHARGED.** The predicate now DECLARES its exclusion scope; this lap's is **∅** and the byte identity is EXACT ×3. |
| ⚑ **`C-I16-2`** | check 12's statistic sample-size-blind | ⚑ **DISCHARGED.** Pooled board-wide (n=356) + Wilson 95 %; predicted mass inside the interval; zero tiers above 2. |
| ⚑ **`U-P-N-1`** | the bracket | ⚑ **COLLAPSED on the pre-registered verdict keys → NO deferral, Lap Q's trigger NOT met.** Read with `D-I17-6`. |
| ⚑ **`D-I12-5`** | w154 TTL | ⚑ **UNRESOLVED, a seventh time**, identical to the tick on both arms. Your R-PM4-40 part 6 expectation is not met; S-3 said so before the run. Carries to R-CPB-4's surface. |
| `D-P1` / `D-P2` | Lap P residuals | carried; sheet governs both; `S-D-P2-REGEN` measured **inert** |
| `U-P-N-2/3/4/5` | Lap P undecideds | all four RUN; **none verdict-material**; `U-P-N-5` inert by critHI's retirement (100 % of calls at `crit_mult == 1.0`) |
| ⚑ **`D-I17-5`** | the `spans_vs_I16` cross-cell baseline defect | ROUTED — record-cell rows unaffected |
| ⚑ **`D-I17-6`** | ⚑ **the verdict-key instrument is saturated** | ROUTED — **§ 11.1** |
| ⚑ **DECISIONS-LOG PROPOSED** | **`D-I17-1`** — the ADCTH basis semantics. Rides the end-of-run governance package beside `D-I15-2` and `D-I16-1`. | awaiting |
| carried | `U-O-1` · explosion-centre UNDECIDED · `Q57` | carried |

### 11.1 ⚑ THE NAMED CANDIDATE, AND THE HONEST BOUNDARY

**What this lap removed from the table.** T1 is **not** set by the player's sustain. That was the
last named measured route from I-16's own landing, and it is now measured: cutting the heal by an
order of magnitude leaves the death wave, the `l4l`, the clear spans and the deepest tick all
unmoved. **The sustain engine was the run's hypothesis for the T1 residual and it is falsified.**

**What the measurement points at instead, stated as mechanism and not as a wanted route.** The
player dies in **dry stretches** — `dry_fraction_whole_run` **0.4118**, `final_200_dry_fraction`
**0.33** — where the heal is regen alone under every arm. Sustain scales with *contact*; death
happens in its *absence*. ⚑ **The quantity that sets T1 on this board is how long the player goes
without a body in his disc, which is a TARGETING-AND-LOCOMOTION quantity — the same surface
`D-I12-5` has been pointing at for seven iterations and the same one R-CPB-4 routed to the engine
as movement-while-channeling + pack-seek targeting policy.**

⚑ **I am naming it, not claiming it.** Whether closing that surface moves T1 toward 160 is not
decidable from my seat, and **no constant may move to find out.** If the conductor judges the
measurable limbs exhausted, the residual is: **a fully measured board, a fully decoded sustain
engine, and a player who dies five waves early because the sim's targeting leaves him standing in
an empty disc for 41 % of the fight.**

---

**Author:** gamora (simulation seam) · 2026-08-14 · **math note first, code second, and the git
order is the proof — including the six predictions and the one structural candidate that graded
FALSE.**
