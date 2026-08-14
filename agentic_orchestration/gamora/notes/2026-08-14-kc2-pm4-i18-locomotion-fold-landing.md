# KC2-PM4 · I-18 — **THE LOCOMOTION FOLD** — landing note

> **Run:** KC2-PM4 · **Iteration:** I-18 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** **R-PM4-43 part 3** (ledger **L-34**), limbs (a)–(h).
> **Folds onto:** the **I-17 INCUMBENT** (`abba92b2..fd902e05`), **BOTH `U-P-N-1` arms riding.**
> **Math note (FIRST, its own commit, ZERO code):**
> `simulation/math/kc2-pm4-i18-locomotion-fold-2026-08-14.md` — engine `95fdb3a8`
> **Engine commits:** `95fdb3a8` (math note ONLY) → `6c14f384` → `77ee6302` → `2052f145`
> → `fcbfd053` → `3ce75894` → `4d444320`
> **Not pushed** — the conductor verifies from his own seat and pushes.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

⚑ **The commission's premise was false on two of three cells, and the math note said so before any
code existed.** "The player currently never moves" is exactly true of `camp_defoff` (moving
fraction **0.0000**) and exactly false of both cluster cells, which already ran **0.7532 / 0.7663**
at a mean tick speed of **6.06 / 6.23 m/s** against the referent's **0.7948**. So I-18 is not an
unpinning; it is a re-aiming, a re-pricing and a coverage extension. ⚑ **And it moves the board
further than any fold since I-13: `l4l` 92.98 → 165.31 on the record cell, T2's ratio to 182.7167
from 0.5089 to 0.9047, T2 MET on three of the four record arms, and the death wave gains one.**
⚑ **`U-P-N-1` is VERDICT-DIVERGENT for the first time in this run** — `D-I17-6`'s saturation broke
because the *fold* moved the board, not because the *instrument* was changed. Wall **26/26 GREEN**,
fold-off byte identity **EXACT ×6**, determinism ×2 zero-diff **×12**, `law_3.moved == {}` with
**34 witnesses**. **Predictions 17/23, structural 1/3 — and the failures carry the content.**

---

## 1 — ⚑ THE RECORD-CELL SCORECARD — ALL FOUR ARMS, WITH THE GRADED-DISTANCE COLUMNS

**`cluster_defon__critlo`.** critHI stays retired (R-PM4-37 part 2).

| | COUPLED · PX-LO | ⚑ COUPLED · PX-HI | ⚑ DECOUPLED · PX-LO | ⚑ DECOUPLED · PX-HI | I-17 | referent |
|---|---:|---:|---:|---:|---:|---:|
| **T1** death wave | 152 ✗ | **156** ✗ | **156** ✗ | **156** ✗ | 155 ✗ | 160 |
| ⚑ **T1 Δ waves** | **−8** | ⚑ **−4** | ⚑ **−4** | ⚑ **−4** | −5 | 0 |
| **T2** `l4l` (s) | 50.0408 ✗ | ⚑ **155.3469 ✓** | ⚑ **165.3061 ✓** | ⚑ **155.5102 ✓** | 92.9796 ✗ | 182.7167 |
| ⚑ **T2 ratio** | 0.2739 | **0.8502** | ⚑ **0.9047** | **0.8511** | 0.5089 | 1.0 |
| **T3** MAE (s) | 8.7621 | 12.2262 | 15.5187 | 12.1990 | 8.2765 | — |
| **T4a** mean `hp_frac` | 0.9050 ✗ | ⚑ **0.9123 ✓** | 0.9649 ✗ | 0.9599 ✗ | 0.8669 | 0.932 |
| ⚑ **T4a Δ** | −0.0270 | ⚑ **−0.0197** | +0.0329 | +0.0279 | −0.0651 | 0 |
| **T4b(b)** strict dwell | 0.0 ✗ | 0.0 ✗ | 0.0 ✗ | 0.0 ✗ | 0.0 ✗ | 1.6166 |
| **T4b(c)** (SCORECARD LAW) | ✗ | ✗ | ✗ | ✗ | ✗ | w160 kill from full |

⚑ **`COUPLED · PX-HI` is the first cell in this run's history to hold T2 AND T4a simultaneously
without a compensating-error diagnosis attached** (I-15's all-green board was re-graded at
R-PM4-40 as standing on identity-path trash intake against a never-decoded sustain constant; this
board's terms are a measured speed, a measured killable predicate and 169/169 measured monster
speeds). **T1 is still missed by four waves and I am not calling this convergence.**

### 1.1 ⚑ THE TWO BRACKETS

| bracket | arms | divergent? | designation |
|---|---|---|---|
| ⚑ **`U-P-N-1`** (at PX-LO) | COUPLED `T2_MET=false` · DECOUPLED `T2_MET=true` | ⚑ **YES — `T2_MET`** | **DEFERRED** |
| **px→m** (at DECOUPLED) | PX-LO / PX-HI agree on all four keys | no | **COLLAPSED — arms agree** |

⚑ **`U-P-N-1` was carried at R-PM4-42 part 1 as PHYSICALLY-UNDECIDED / VERDICT-INERT. It is not
inert any more.** The leech-resistance question now separates a cell that dies on 152 with `l4l`
50.04 from one that dies on 156 with `l4l` 165.31. **Lap Q's discriminator becomes live by the
rule as pre-registered, and the call is the conductor's.**

⚑ **The px bracket COLLAPSED on the keys while its graded distances differ by 9.80 s of `l4l`
(165.3061 vs 155.5102) — which is exactly why R-PM4-42 part 2 exists.** Reporting, not scoring.

### 1.2 The other two geometries, for completeness

| cell | COUPLED PX-LO | COUPLED PX-HI | DECOUPLED PX-LO | DECOUPLED PX-HI |
|---|---|---|---|---|
| `camp_defoff` | @151, 6.5306 | @151, 6.5306 | @152, 23.5918 | @152, 23.5918 |
| `cluster_defoff` | @152, 50.0408 | @156, 155.3469 | @156, 165.3061 | @156, 155.5102 |

`cluster_defoff` and `cluster_defon` are **identical on every arm** — defences are inert on this
board under the fold, unchanged from I-17.

---

## 2 — ⚑ THE REFERENT-YARDSTICK DIAGNOSTIC TABLE (R-PM4-43 part 3 (e)) — **NOTHING ADJUSTED**

| cell | ring dry @2.4 m | longest dry run | mean occ | moving frac | longest still | damage-landed dry |
|---|---:|---:|---:|---:|---:|---:|
| camp COU PX-LO/HI | 0.9750 | 6.3673 | 0.0250 | 0.0000 | 6.4490 | 0.9625 |
| camp DEC PX-LO/HI | 0.7509 | 6.3673 | 0.4567 | 0.0000 | 23.4286 | 0.6055 |
| cluster COU PX-LO | 0.5808 | 4.5714 | 0.8548 | 0.5385 | 1.3878 | 0.5139 |
| ⚑ cluster COU PX-HI | 0.5596 | 11.1837 | 1.0914 | 0.5261 | 1.3878 | 0.4771 |
| ⚑ cluster DEC PX-LO | 0.5531 | **15.6735** | 1.1180 | 0.5211 | 4.0000 | 0.4844 |
| ⚑ cluster DEC PX-HI | 0.5601 | 11.1837 | 1.0903 | 0.5261 | 1.3878 | 0.4777 |
| ⚑ **REFERENT** | ⚑ **0.1989–0.2063** | ⚑ **2.75** | ⚑ **3.2423–3.4251** | ⚑ **0.7948** | ⚑ **1.73** | ⚑ **0.1653** |
| I-17 record cell | *never measured* | *never measured* | *never measured* | 0.7663 | 1.3878 | 0.4118 |

⚑ **The dry SHAPE did not converge — it got worse, and the mechanism is the one priced pre-code.**
The referent's longest dry stretch in 181 s is **2.75 s**; the sim's is **4.57–15.67 s**. The math
note § 3.3 priced a single 20 m traversal at **4.37–4.59 s** at the measured speed and said
in advance that *"the minimal structure cannot reproduce the referent's 2.75 s ceiling on a board
whose spawn radius reaches 45 m."* **That is `S-3`, TRUE, and it is a finding about the STRUCTURE:
closing it needs a spawn-geometry decode (Lap R `UNREACHED-1`), not a policy constant.**

⚑ **`D-I18-4`, self-caught and mine to report.** The run has been comparing the sim's
**damage-landed** dryness (0.4118) against the referent's **ring-occupancy** dryness
(0.1989–0.2063). The referent's damage-landed number is **0.1653**. The direction of L-34's
finding survives and is *worse* than quoted (2.49× rather than 2.0×), but the pairing was never
like-for-like. **The 0.4118 is my number, so the correction is my debt.** Both quantities are now
emitted side by side on every cell; nothing was adjusted toward anything.

---

## 3 — ⚑ `D-I12-5` — THE EIGHTH EXAMINATION, AND ITS SHAPE INVERTS

| | I-17 | ⚑ I-18 record cell | referent |
|---|---:|---:|---:|
| w154 span | 38.12244897959184 s | ⚑ **46.122448979591844 s** | ⚑ **14.20 s** |
| ratio to referent | 2.7005 | 3.2672 | 1.0 |
| ⚑ post-last-kill tail | ⚑ **21.2246 s** | ⚑ **0.8163 s** | — |
| ⚑ killable survivors left UNTOUCHED | ⚑ **17** | ⚑ **0** | — |
| survivors killable-and-unreached | 17 | **2** | — |
| survivors unkillable-by-design | 8 | **12** | — |
| classification | — | ⚑ **BOTH** | — |

⚑ **The pet-TTL wait is DISSOLVED and the wave is LONGER.** Under I-17 the player stood in a pile
of physically-immune `loghorrean_void` bodies for 21.2 s while **17 killable stationary shards sat
13.5–26 m away with `hp_end == hp_max`, untouched.** Under the killable filter he goes and kills
all of them — the tail collapses from 21.22 s to 0.82 s and the untouched count goes 17 → 0 — but
walking to them at the **measured (slower)** speed costs more than the wait did.

⚑ **This is reported as a NAMED WAVE-ADVANCE DIVERGENCE per R-PM4-43 part 3 (f), with the
referent's 14.20 s beside it, and the classification is BOTH: 2 killable-unreached + 12
unkillable-by-design.** The wave-advance rule did **not** change in this fold — `gates_clear` is
read, never rewritten. **Lap S is pre-named and the call is the conductor's.**

---

## 4 — THE FOLD-OFF BYTE-IDENTITY PROOF — **EXACT ×6, EXCLUSION SCOPE ∅**

Declared scope is **EMPTY** and the declaration is load-bearing: `D-I17-5`'s repair lives in the
DRIVER's comparison reporting and touches nothing inside `simulate_wave`; the new ring series is a
**run ATTRIBUTE**, invisible to `_surface()`. I-18 repairs no shared wire.

| I-17 cell | fold-OFF digest (this lap) | I-17 recorded | |
|---|---|---|---|
| `camp_defoff__critlo__COUPLED` | `723591794095abe226d6956470e8d8cce9f675ef309520a12419dbd477cc0dfa` | same | **EXACT** |
| `camp_defoff__critlo__DECOUPLED` | `b5e1fcf2f5d05ecd9daec458655cb09672a6b19041c2b62b05296862f47345b3` | same | **EXACT** |
| `cluster_defoff__critlo__COUPLED` | `d9824d9075dfc1061d4400c4f2417b7da79fc0e9a6c115361bff99a61e8f3d43` | same | **EXACT** |
| `cluster_defoff__critlo__DECOUPLED` | `6db2f698b29d31a873488a28290a92e682ad062cb006f498086b386927103c7a` | same | **EXACT** |
| `cluster_defon__critlo__COUPLED` | `d1698fc32ffb1150715b2ba9e2fce6bab5c8f7f22564b5b9cb2a7eaf8cf30e81` | same | **EXACT** |
| `cluster_defon__critlo__DECOUPLED` | `3bcf7c7fbb1864a1e2a13cf10ba7d6420a11b7130384ac8a345dea4a59ae42c6` | same | **EXACT** |

`player_locomotion` **ABSENT on 26/26** fold-off waves (ABSENT-not-None, the twelfth use).

⚑ **The predicate earned its keep this lap: it went RED first, and what it caught is `D-I18-7`
(§ 8).**

---

## 5 — DETERMINISM ×2 — **ZERO DIFFERENCES ON ALL TWELVE PRIMARY CELLS**

| cell | pass-1 digest = pass-2 digest |
|---|---|
| `camp_defoff__critlo__COUPLED__PX-LO` | `91bc610737fe617780dcda2d28630d36005818a87e2e4647ee00a5c644c9c1ff` |
| `camp_defoff__critlo__COUPLED__PX-HI` | `d9d4320b550c50da80e6c38e8299034d075dde01aa8066586a8751279ab47369` |
| `camp_defoff__critlo__DECOUPLED__PX-LO` | `fc33f6bc99769a8168c42dcb50dcc86f384f3442d2c251b92cc84754a1b8ad1e` |
| `camp_defoff__critlo__DECOUPLED__PX-HI` | `9fab1e4c0d55bef8b180ff1ab8a7e44451976f7e179ba31f38c9456a6c392d8c` |
| `cluster_defoff__critlo__COUPLED__PX-LO` | `c6381674e4e9de3eae0adc87aeb8c2e9506b69365eacde4f565fa9cd1d449f06` |
| `cluster_defoff__critlo__COUPLED__PX-HI` | `8fc58798944dab2147d19ed3f22f3cdd55f391be83b2b47ec699f6f805f5825c` |
| `cluster_defoff__critlo__DECOUPLED__PX-LO` | `709f7221abda5f69eddda4fca9d7d999be0b20caf8939b0046406e8238a837c9` |
| `cluster_defoff__critlo__DECOUPLED__PX-HI` | `126a49f5f593362348506ec17ed54799db0ad7446fe01564efd3d84a8296f0c9` |
| ⚑ `cluster_defon__critlo__COUPLED__PX-LO` | `095a86d7e96f9c662b5c40532225b4d7832e9c584585545f15ea047c8ac962a9` |
| ⚑ `cluster_defon__critlo__COUPLED__PX-HI` | `f73086714184622daa0bdad22e1c786fac9b5026ec35cd375acd073d7aecbb8e` |
| ⚑ `cluster_defon__critlo__DECOUPLED__PX-LO` | `b410c56819a535c34df0e88a7374eaa1ea67ebab8979a0e87fc4d78332b36176` |
| ⚑ `cluster_defon__critlo__DECOUPLED__PX-HI` | `85d01c49b3ea506b02f527d531131ed2504937c569b870249230567725764c6e` |

---

## 6 — ⚑ THE PRE-REGISTERED PREDICTIONS, GRADED — **17 / 23**

| # | claim | got | |
|---|---|---|---|
| P.1 | fold-OFF EXACT ×6, key ABSENT | EXACT ×6, 26/26 | ✅ |
| P.2 | determinism ×2 zero-diff ×12 | 12/12 | ✅ |
| P.3 | `law_3.moved == {}`, ≥12 witnesses | `{}`, **34** | ✅ |
| P.4 | 66-record overlap, 0 disagreements | **0** | ✅ |
| P.5 | roster coverage complete, 0 fallbacks | 0 absent | ✅ |
| P.6 | ⚑ limb (a) INERT on camp | ⚑ **NOT inert** — digests differ | ❌ |
| P.7 | ⚑ w154 collapses below 30 s | ⚑ **46.12 s — it got LONGER** | ❌ |
| P.8 | w154 never reaches 14.20 s | never | ✅ |
| P.9 | ring dry < damage-landed dry | ⚑ **0.5531 > 0.4844** | ❌ |
| P.10 | ⚑ longest dry run > 2.75 s every cluster cell | 4.57–15.67 s | ✅ |
| P.11 | mean occupancy rises, stays < 3.24 | 0.85–1.12 | ✅ |
| P.12 | moving fraction FALLS vs 0.7663 | **0.5211–0.5385** | ✅ |
| P.13 | ⚑ `S-NO-KILLABLE-FILTER` reproduces I-17's w154 to the tick | ⚑ **54.12 s — test CONFOUNDED** | ❌ |
| P.14 | ⚑ aim moves `l4l` more than rate | seek Δ 59.67 vs speed Δ **0.0** | ✅ |
| P.15 | PX arms verdict-identical, distances differ | collapsed; 9.80 s apart | ✅ |
| P.16 | T1 missed, death ∈ {153…157} | @156 | ✅ |
| P.17 | ⚑ T2 ratio RISES above 0.5089 | ⚑ **0.9047** | ✅ |
| P.18 | ⚑ T4a FALLS vs I-17 | ⚑ **0.8669 → 0.9649 — it ROSE** | ❌ |
| P.19 | T4b(b) 0.0; T4b(c) never fires | 0.0 / none | ✅ |
| P.20 | M-2 cap fires more often | reported | ✅ |
| P.21 | zero invariant raises | zero | ✅ |
| P.22 | wall ≥26 checks, all scored, `keys_asserted` | 26/26 | ✅ |
| P.23 | ⚑ `D-I18-3` EXERCISED ≥ once | ⚑ **0 clips — never exercised** | ❌ |

### 6.1 ⚑ THE STRUCTURAL PRE-NAMING — **1 / 3**, AND BOTH FAILURES ARE INSTRUCTIVE

| candidate | verdict |
|---|---|
| **S-1** — *the dryness is an AIMING defect, not a locomotion deficit; the killable filter is the unifying error* | ⚑ **FALSE — because my own falsification test was mis-specified.** `S-NO-KILLABLE-FILTER` was supposed to reproduce I-17's w154 to the tick; it returns **54.12 s**, because that limb still carries limbs (a) and (d). **The test was confounded by my hand, and I am recording that rather than reinterpreting the result.** Its second leg (P.14) held decisively — aim moves `l4l` by 59.67 s where rate moves it by **exactly 0.0** — so the *mechanism* still looks right and the *test* was not clean. It gets a fresh, isolated falsifier next lap or it does not get called true. |
| **S-2** — *the measured speed cannot help and must hurt* | ⚑ **FALSE, AND CLEANLY SO.** `S-SPEED-ONLY` returns `l4l` **92.9795918367347** — I-17's number **to the seventeenth digit** — and death @155. ⚑ **The measured speed alone is VERDICT-INERT: it neither helps nor hurts until the aim changes.** I predicted a monotone worsening and got a null. The honest reading: on this board the player's *rate* is not a binding term at all; his *target* is. |
| **S-3** — *the minimal structure cannot hold the referent's 2.75 s dry ceiling, and the arithmetic says so before the run* | ⚑ **TRUE.** 4.5714 / 11.1837 / 15.6735 s against 2.75 s, traversal-shaped, on every cluster cell under every arm. **Priced at 4.37–4.59 s per 20 m leg in the math note § 3.3 before the code existed.** |
| **T-1 (throughput)** | ⚑ **WRONG ON THE SIGN FOR THE FIRST TIME IN FIVE.** The walk priced the fold as *slower everywhere*; the board came back **73 s longer on `l4l` and one wave deeper**. The correction I applied in advance (predict T2's ratio to RISE) was right for the right reason — removing a 21 s TTL wait removes free survival as well as dead time — but the walk's own sign was wrong, and the streak is broken. |

⚑ **What P.7 and P.18 got wrong, as mechanism rather than apology.** I priced the killable filter
as a *dryness* fix and predicted w154 would shorten and T4a would fall. Both inverted: w154 got
**longer** while its *shape* inverted completely (tail 21.22 → 0.82 s, untouched killables 17 → 0),
and T4a **rose** 0.87 → 0.96. The mechanism I missed is that contact is not a cost on this board —
it is the *income*. Sending the player at things he can kill raises his leech and his clear rate
together; what it costs is **travel**, and travel is exactly what `S-3` says the arena's 45 m
spawn radius makes expensive. **The residual is a geometry residual, not a policy residual.**

---

## 7 — THE ASSERT WALL: **26 / 26 GREEN**

Spec in the math note § 13 (**W-6**). R-PM4-37 part 6 honoured on every check: `have()` **raises**
on a missing key; every check carries `keys_asserted`; **check 26 verifies that every earlier one
did.**

| # | what | measured |
|---|---|---|
| 1 | ⚑ fold-OFF byte identity vs I-17's **six**, scope ∅ | 6/6 EXACT, ABSENT 26/26 |
| 2 | 2 Lap R pins at FULL 64 hex | both EXACT |
| 3 | frozen `E-s09-cp150` | **20 artifacts, unchanged** |
| 4 | ⚑ `law_3.moved == {}` top level | `{}`, **34 witnesses** |
| 5 | ⚑ **speed arithmetic RE-DERIVED from the vendored CSV** | both edges, err ≤ 3.3e-11 |
| 6 | ⚑ **CROSS-INSTRUMENT CONTROL** — Lap R vs the sim's own emission | 66 overlap, **0 disagreements** |
| 7 | ⚑ roster coverage complete, zero modal fallbacks | 0 absent |
| 8 | ⚑ **THE CONSTANT CENSUS** — no hysteresis/cadence/anticipation symbol exists | 0 present, 0 in source |
| 9 | ⚑ trigger **IS** `D_ENGAGE_M`; predicate **IS** `gates_clear` | identity, no reimplementation |
| 10 | ⚑ jitter REFUSED, `n_jitter_applied == 0` | 0 on all 12 |
| 11 | ⚑ zero RNG, zero clock reads, sorted live lists | 0 |
| 12 | ⚑ **movement-while-channeling POSITIVE CONTROL** | 0 penalty terms, 0 non-zero headings |
| 13 | ⚑ the new ring series **agrees with the existing histogram** | 12/12 exact |
| 14 | ⚑ `D-I18-3` clips counted | **0** (reported, not assumed) |
| 15 | ⚑ `D-I18-1` arrival clamp EXERCISED on every seeking cell | > 0 |
| 16 | ⚑ the yardsticks are **DIAGNOSTIC** — zero branch conditions | 0 hits |
| 17 | ⚑ **T4b(c) SCORECARD LAW** (R-PM4-40 part 5) | enforced |
| 18 | determinism ×2 | zero differences ×12 |
| 19 | ⚑ **graded-distance columns** on every cell + limb | present |
| 20 | ⚑ **`D-I17-5` REPAIRED** — per-cell baselines | 0 cross-cell |
| 21 | ⚑ `D-I12-5` with the (f) classification | reports, does not gate |
| 22 | ⚑ the two brackets, no discretion | consistent |
| 23 | ⚑ zero invariant raises, offsets inside the bound | max **80.0 m exactly** — the I-4 dash sane-bound CLIP landing on the bound, not a runaway (the clip is closed-form and counted); `_finish` raises only above it |
| 24 | MIGRATION from the emitted bytes | `+player_locomotion`, `−player_cluster_seek` |
| 25 | ⚑ **`D-I18-4` PUBLISHED** — both dryness definitions side by side | 12/12 |
| 26 | ⚑ every check carries `keys_asserted` | 25/25 |

---

## 8 — ⚑ DEFECTS, ALL SELF-CAUGHT, ALL FRAMED

| id | what | disposition |
|---|---|---|
| ⚑ **`D-I18-1`** | the arrival clamp `dist − D_ENGAGE_M` — **CITED** from the CAMP collect branch, not chosen | framed; wall 15 requires it exercised |
| ⚑ **`D-I18-2`** | tie-break = lowest `actor_id` | framed; counted |
| ⚑ **`D-I18-3`** | a player can be **BLOCKED BY AN UNKILLABLE BODY** | framed; **0 occurrences** — reported either way |
| ⚑ **`D-I18-4`** | ⚑ **the run's two "dry fraction" quantities were never the same quantity.** The 0.4118 is mine and so is the correction | published on 12/12 cells; MIGRATION § 1c |
| ⚑ **`D-I18-5`** | ⚑ **Discipline #12 SEMANTIC SHIFT.** The player's objective changes from *"stand where the most bodies are"* to *"be in contact with something you can kill"*, and the seek **SUPERSEDES** `ClusterSeekPolicy` — so `player_cluster_seek` legitimately leaves the wave dict | math note § 4, MIGRATION § 1a, commit |
| ⚑ **`D-I18-6`** | ⚑ **the player gets SLOWER, on MEASUREMENT** — 5.4 → 3.836 / 4.029 m/s. Every traversal in this run's history was priced at a DERIVED rate | MIGRATION § 1b |
| ⚑ **`D-I18-7`** | ⚑ **SELF-CAUGHT BY MY OWN FOLD-OFF PREDICATE, AND REPRODUCED RATHER THAN REPAIRED.** `MovementPolicy`'s docstring says *"state is PER WAVE"*, but **every driver since I-4 has built it ONCE, outside the wave loop**, so its cadence phase, dash cooldowns and stationary run have persisted across wave boundaries for **eleven iterations**. Building it per wave (what the docstring asks) turned check 1 RED on all four cluster cells. Repairing it here would ride a second unrelated semantic on a locomotion fold and make the I-17 baseline unreachable | **BANKED — § 10** |
| ⚑ **`C-I18-1`** | `characterRunSpeedJitter` **REFUSED** — measured on 137/169 records, law UNDECODED (Lap R `UNREACHED-8`). Folding it would be estimation AND would inject RNG for a term whose sign I cannot state | routed — GL-12 data gate |
| ⚑ **`C-I18-2`** | ⚑ **EIGHT BATONS REFUSED TO WRITE** — § 9 | routed, star-lord's seam named |
| — | three instrument bugs in **my own wall**, found and repaired before landing: a **maximum being SUMMED** across waves; check 22 iterating non-bracket keys; check 24 demanding `removed_keys == []` when `D-I18-5` declares the removal | repaired pre-landing, reported here |

---

## 9 — ⚑ `C-I18-2` — FOUR BATONS SHIP, EIGHT REFUSE, AND THE REFUSAL IS THE FINDING

**Emitted, 67/67 green each (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33):**

| column | sha256 |
|---|---|
| `pm4-i18-camp-defoff-critlo-coupled-px-lo` | `e6c8caaf01b86834ba88f783e5bda6c383a857141c35eb86d6ea6c70b29fd26c` |
| `pm4-i18-camp-defoff-critlo-coupled-px-hi` | `3327f36bd03bbed0436c7c53f4c66c13850b543127fa2381054703ea2e58c5a9` |
| `pm4-i18-camp-defoff-critlo-decoupled-px-lo` | `05656582710adb81d30c2e593c6f4c6b44b63811ed401aa37f6c508a7dd127cd` |
| `pm4-i18-camp-defoff-critlo-decoupled-px-hi` | `f8db42666a454ba6d75a44734747c49f61ecb9407096363a37d561252e534f31` |

**The eight cluster columns RAISE inside `kc2_run_adapter._spawn_tick`:**

```
F5-M/F5-E DISAGREE for 'w152_a000': the sim recorded its spawn vertex at run_tick 370,
the LAST-STILL-TICK arithmetic derives 361.
```

⚑ **Diagnosed, not worked around.** The nine-tick gap is not a rounding preference and not the
drip: **the DRIVER's wave 151 runs 370 ticks and the ADAPTER's independent replay of the same spec
runs 361.** They are running different models on the seeking cells, and the mechanism is
**`D-I18-7`**. Under I-17 the same divergence was worth one tick per wave and the `ceil` arithmetic
absorbed it (I-17's landing note recorded the pattern); under I-18 the seek policy stands still far
more often, the cadence phases separate further, and the interlock fires. ⚑ **The camp columns emit
cleanly precisely because camp carries `movement_fold=False` — no policy object exists, so the two
sides agree exactly. That is the control proving the mechanism.**

⚑ **NOT repaired in this lap (NOTE-9).** The fix is a semantic decision that must be taken once,
deliberately, for both sides: either the drivers adopt per-wave construction, or `run.py` and the
adapter adopt ladder-scoped state. **Routed to the conductor with star-lord named**, since
`_spawn_tick` and the F5-M/F5-E ruling live in `export/`. **Twelve knot artifacts and twelve
determinism digests exist for all twelve cells; what is missing is eight BATONS, and the reason is
on the record.**

---

## 10 — THE SENSITIVITIES: **SEVEN LIMBS, AND TWO OF THEM ARE THE LAP'S REAL RESULT**

| limb | COUPLED | DECOUPLED | verdict-material? |
|---|---|---|---|
| ⚑ `S-SPEED-ONLY` | @155, 92.9796 | ⚑ **@155, 92.9795918367347** | **yes** |
| ⚑ `S-SEEK-ONLY` (incumbent 5.4 m/s) | @151, 14.6122 | ⚑ **@156, 152.6531** | **yes** |
| `S-MONSTER-ONLY` | @152, 23.1837 | @155, 92.5714 | yes |
| ⚑ `S-NO-KILLABLE-FILTER` | @152, 50.0408 | ⚑ **@156, 199.5102**, w154 **54.12 s**, longest dry **26.12 s** | no |
| `S-PX-MID` (122.32 gpx/m) | @151, 6.2041 | @151, 6.2041 | yes |
| ⚑ `S-INCUMBENT-SEEK` | @152, 23.1837 | **@156, 106.6122**, w154 **33.71 s** | yes |
| `S-CAMP-UNPINNED` (reported, never scored) | @152, 23.6735 | @152, 23.6735 | yes |

* ⚑ **`S-SPEED-ONLY` is the cleanest number in the lap.** The measured speed on its own reproduces
  I-17's `l4l` **to the seventeenth digit**. The player's *pace* is not a binding term on this
  board; his *target* is. That falsifies my own `S-2` and it is worth more than the prediction was.
* ⚑ **`S-SEEK-ONLY` at the incumbent 5.4 m/s reaches `l4l` 152.65 and death @156** — i.e. **the
  killable filter carries essentially the whole move**, and the measured speed contributes the
  remaining 12.7 s. Aim, not rate.
* ⚑ **`S-PX-MID` is NOT between its own bracket edges** (@151, 6.20 against @152/@156). **The
  bracket is NOT monotone in the px scale**, so a "bracket mean" is meaningless here and the
  R-PM4-43 part 2 refusal to adopt a point is vindicated by measurement rather than by principle.
  **Banked as a live finding for the conductor.**

---

## 11 — ARTIFACTS AND DIGESTS (FULL 64 hex, GL-6)

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i18-findings-20260814_105832.json`
`8cb394607bb2d492a99ba9987a08918902001ff946a0e326d5e3342b874175bd`

**Knot artifacts (12):**

| cell | sha256 |
|---|---|
| `camp-defoff-coupled-px-lo` | `55f9795c791447c967479613881a89a9d8ffa5ab44174dcff8d4039c917d6b1f` |
| `camp-defoff-coupled-px-hi` | `c31a2a251b6f47a8b11af35c397dcad5e3c87fe5d4fee2d65c2b4f6dc628a78c` |
| `camp-defoff-decoupled-px-lo` | `8c99f9d72d6f42f30a07960143f0b99bd1d6e37d877e0b3217637cf6ac2654a6` |
| `camp-defoff-decoupled-px-hi` | `0bc602391f61fe65bcfbaea98c4e51eea91499e0b316ff698f5735fc87048101` |
| `cluster-defoff-coupled-px-lo` | `e99aab7f9eef330962ed320b6bd39d3cbe536cee17cdb640d737c07208c7cccf` |
| `cluster-defoff-coupled-px-hi` | `252bbd1d062061e7131aea270a824196b0446d0d0a988a8bef741e96d45ab87b` |
| `cluster-defoff-decoupled-px-lo` | `e9b41ca11dca98946bb05b06601cbd60a97246158886c1b1d98f772c9681520f` |
| `cluster-defoff-decoupled-px-hi` | `b51568e038e3a4234abd33ca3dbadf09efc43f183beaa903c2cf2efc32be3b18` |
| ⚑ `cluster-defon-coupled-px-lo` | `217608ab3d00056dd21a4ac74e21e865f5ff31949fe36ecaf3fce68dbf1ee640` |
| ⚑ `cluster-defon-coupled-px-hi` | `d0a2ffba712171bad524f33b5e4d2bf2c1a491e31acca700b101d87e5dc95ba0` |
| ⚑ `cluster-defon-decoupled-px-lo` | `0b9bf3ecd41fa14939fea81754be1ad4c04689aaccd92a552e5325889910f06c` |
| ⚑ `cluster-defon-decoupled-px-hi` | `57c732d09eb5a93b4e50ff8453c6f4637df510f12d992d40b02e76ada1f2e310` |

**⚑ CONSUMED INPUTS, ALL RE-HASHED FROM THIS SEAT AND EXACT vs ledger L-34:**

| file | sha256 | rows |
|---|---|---:|
| `pm4r_movement_episodes.csv` (vendored) | `dc3173ae53c2a371d9336e95db79c25c4deb04834cebdd4c9318f554d9f576cc` | 86 |
| `pm4r_speed_terms.csv` (vendored) | `a16c99300dc5254d55a978685287331abf633e8950f51827cfc538c6b37969d0` | 2,073 |
| `pm4r_contact_occupancy.csv` (read) | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` | 28 |
| `pm4r_findings.md` (read) | `c223dfb04653a7e8682d5c1dd42356fc2a8398b06951372445d235a6eff224ea` | 647 lines |
| `pm4r_fct_gaps.csv` (read) | `636753a7b16c5a63c152a707729be98a4a13727803ec29ebffd87b654612e12e` | 44 |
| `PREREGISTRATION.md` (read) | `dc49d0ba8f176ab1d4814d522e5183867fe2ad56334ed7251e81b3db124cec10` | — |
| I-17 findings (pinned baseline) | `df5dece1212f12974d314595c3ef1f71bd37ee1bc1bf9245c8bf33dab608f141` | — |

**Frozen substrate `E-s09-cp150`: 20 artifacts verified, UNTOUCHED.**
**Law 3:** `law_3.moved == {}` **TOP LEVEL**, **34 witnesses**, **zero new free constants** — every
number in `player_locomotion.py` traces to a Lap R row, is arithmetic over Lap R rows whose formula
is printed in the math note § 3.2 before the code existed, or is one of the sim's own pre-existing
constants imported by identity.
**Test suite:** 296 kc2 tests pass. The one failure
(`test_AC_10_10 :: bare 30.0 in secondary_streams.py`) is **PRE-EXISTING** — verified by stashing
this work and re-running.
**MIGRATION.md:** written **from the emitted bytes** — `added == ["player_locomotion"]`,
`removed == ["player_cluster_seek"]`, `EVENT_COLUMNS` identical, `_schema_version` 1 → 1.
**Zero telemetry schema changes.** **Wall clock: 76.1 s.**

---

## 12 — TO THE CONDUCTOR

| id | what | disposition |
|---|---|---|
| ⚑ **`U-P-N-1`** | the leech-resistance bracket | ⚑ **VERDICT-DIVERGENT for the first time in the run** (`T2_MET`). R-PM4-42 part 1's "verdict-inert" no longer holds. **Lap Q's discriminator is live by the pre-registered rule; the call is yours.** |
| ⚑ **px→m bracket** | R-PM4-43 part 2 | **COLLAPSED** on the keys, **9.80 s apart** on graded distance. ⚑ **And `S-PX-MID` lands OUTSIDE both edges — the bracket is NOT MONOTONE in the px scale, so a point value would have been not merely imprecise but ill-defined.** Your refusal to collapse it is vindicated by measurement. |
| ⚑ **`D-I12-5`** | w154 | ⚑ **DISSOLVED IN SHAPE, WORSE IN SPAN** — tail 21.22 → 0.82 s, untouched killables 17 → 0, span 38.12 → 46.12 s against the referent's 14.20 s. Classified **BOTH**. Reported as a NAMED WAVE-ADVANCE DIVERGENCE. **Lap S is yours to fire.** |
| ⚑ **`C-I18-2`** | eight batons refuse to write | **ROUTED — § 9.** star-lord's `export/` seam owns `_spawn_tick`; the repair is a semantic decision for both sides. |
| ⚑ **`D-I18-7`** | `MovementPolicy` is ladder-scoped in every driver and wave-scoped in `run.py` — for eleven iterations | **BANKED, reproduced not repaired.** |
| ⚑ **`C-I18-1`** | `characterRunSpeedJitter` law undecoded | **ROUTED** — a decode request, not a guess. 137/169 records, values {0,10,15,20,25,30}. |
| ⚑ **`D-I17-5`** | the cross-cell span baseline | ⚑ **REPAIRED** — every cell names its own baseline key, read from the digest-verified I-17 findings; wall check 20. |
| ⚑ **`D-I17-6`** | the saturated verdict keys | ⚑ **DESATURATED BY THE FOLD, not by an instrument change.** Graded-distance columns land on every cell and every limb per R-PM4-42 part 2. |
| ⚑ **DECISIONS-LOG PROPOSED** | **`D-I18-5`** (the objective's semantics) and **`D-I18-6`** (derived → measured player rate). Ride the end-of-run package beside `D-I15-2`, `D-I16-1`, `D-I17-1`. | awaiting |
| carried | `U-P-N-2..5` · `D-P1`/`D-P2` · `U-O-1` · `U-R-2/3/4/6` · explosion-centre · `Q57` | carried |

### 12.1 ⚑ THE NAMED CANDIDATE, AND THE HONEST BOUNDARY

**What this lap removed from the table.** T1 is **not** set by the player's *pace*. `S-SPEED-ONLY`
reproduces I-17's `l4l` to the seventeenth digit; the measured speed is verdict-inert on its own.
T1 is also not set by the *pet-TTL wait* — that wait is now dissolved (tail 21.22 → 0.82 s) and the
death still lands four waves early.

**What the measurement points at instead, stated as mechanism and not as a wanted route.**
⚑ **The residual is now a GEOMETRY residual.** The player's aim is correct, his rate is measured,
his board is measured — and the sim's longest dry stretch at the kill ring is **4.57–15.67 s**
against the referent's **2.75 s**, because the arena scatters bodies across a measured **45.06 m**
spawn radius and a single 20 m leg costs **4.37–4.59 s** at the measured speed. The referent's
board is never that empty near him. ⚑ **Closing that would need Lap R's `UNREACHED-1` — Crucible
spawn geometry, which lives in `.map`/`.lvl` world assets outside the `.arz` record DB — and it
would need it as a DECODE, not as a constant.**

⚑ **I am naming it, not claiming it.** Whether real spawn geometry moves T1 the last four waves is
not decidable from my seat, and **no constant may move to find out.** If you judge the measurable
limbs exhausted, the residual is: **a fully measured board, a fully decoded sustain engine, a
zero-free-constant aim, a video-measured pace — and a player who dies four waves early because the
sim's arena is bigger and emptier than the one Matt actually played in.**

---

**Author:** gamora (simulation seam) · 2026-08-14 · **math note first, code second, and the git
order is the proof — including the six predictions and the two structural candidates that graded
FALSE, one of them because I mis-specified my own test.**

---
---

# ⚑ ADDENDUM — 2026-08-14 · **I-18R, THE HYGIENE-AND-REPAIR CELL**

> **Fired under:** **R-PM4-44 part 4** (charter ledger **R-PM4-44**; the catch is banked at
> **L-35**). **Conductor:** gandalf. **Author:** gamora.
> **Math note (FIRST, its own commit, ZERO code):**
> `simulation/math/kc2-pm4-i18r-ladder-scoped-movement-policy-2026-08-14.md` — engine `e247faa9`
> **Engine commits:** `e247faa9` (math note) → `6c223443` (C-I18-3 + hygiene) → `0c100c16`
> (the repair) → `1bd16b8d` (MIGRATION + AGENT_STATE). **Not pushed.**
>
> **Two obligations: answer `C-I18-3`, and land the sim-side half of the `C-I18-2` / `D-I18-7`
> semantic ruling. Both below, with the failure modes I was told to report honestly if I found
> them. ⚑ I did not find them — but § A.3 records a scope limit in my own determinism claim that
> the conductor's catch is entitled to, and that nobody asked me for.**

---

## A — ⚑ `C-I18-3` ANSWERED: **WHAT THE `…145605` / `…105605` EMISSION IS**

### A.1 — The answer in one line

⚑ **It is the `D-I18-7` PER-WAVE-CONSTRUCTION EXPERIMENT — the run § 8 describes and never
identified on disk. It is a DIFFERENT CONFIGURATION, not a different pass, and the
determinism-×2 claim survives intact.**

**The two emissions are two separate invocations of the same script, 2 min 08 s apart:**

| | run **A** — the experiment | run **B** — ⚑ **THE RECORD** |
|---|---|---|
| `started_utc` | 2026-08-14T**14:55:08**.551168+00:00 | 2026-08-14T**14:57:16**.617954+00:00 |
| `wall_s` | 57.4033 | 76.0667 |
| actor-paths stamp (**UTC**, emitter line 1639) | `20260814_**145605**` | `20260814_**145832**` |
| findings stamp (**LOCAL**, emitter line 1700) | `20260814_**105605**` | `20260814_**105832**` |
| findings sha256 | `51a06f32a81c7de02648bfbd53d2a425098b9a08c98b11992c1ec8758ef5449a` | `8cb394607bb2d492a99ba9987a08918902001ff946a0e326d5e3342b874175bd` |
| **fold-OFF `all_identical`** | ⚑ **`false`** | **`true`** |
| **assert wall** | ⚑ **22 / 26** | **26 / 26** |
| **predictions** | ⚑ **13 / 23** | **17 / 23** |

⚑ **The four-hour stamp skew is my own emitter, not two different days.** `stamp0` is
`datetime.now(timezone.utc)`; the findings stamp is `datetime.now()` — local, UTC−4. The two
families pair **to the second**: `105605 ↔ 145605`, `105832 ↔ 145832`.

### A.2 — ⚑ RUN A CONVICTS ITSELF — its four RED wall checks are exactly the four defects § 8 records

| check | run A | what it is |
|---|---|---|
| **1** — fold-OFF byte identity vs I-17's six | ⚑ **RED**, mismatching on **exactly the four cluster cells**, camp **EXACT** | ⚑ **`D-I18-7` VERBATIM.** § 8: *"Building it per wave … turned check 1 RED on all four cluster cells."* |
| **23** — max abs offset inside `PLAYER_SANE_BOUND_M` | RED at **98.9132 m** > 80.0 | the *"maximum being SUMMED across waves"* instrument bug, § 8's last row |
| **22** — the two brackets | RED | *"check 22 iterating non-bracket keys"*, § 8's last row |
| **24** — MIGRATION from the emitted bytes | RED | *"check 24 demanding `removed_keys == []` when `D-I18-5` declares the removal"*, § 8's last row |

**Run A's fold-OFF cluster digests** (the four that moved), for the record:

| cell | run A got | I-17 recorded (= run B) |
|---|---|---|
| `cluster_defoff__critlo__COUPLED` | `00f32ca05110ff3f6bb53934bd74d675f4278487c4438b09b932f4e8bd75f78b` | `d9824d90…8f3d43` |
| `cluster_defoff__critlo__DECOUPLED` | `0d1a9ce8bf6aa401836a305e59128f5f77e2af98f6e4e38bc7a5fe2c5f4777bd` | `6db2f698…03c7a` |
| `cluster_defon__critlo__COUPLED` | `eaa399ff74c94bd3c3114fdc10d27c4a2f5fe4c41af12e73d2da22be3adf4c6d` | `d1698fc3…f30e81` |
| `cluster_defon__critlo__DECOUPLED` | `9c4cdf1b830212cd84ec11560b1f8004a27d234ee124c27f75cbfc4cbe63972f` | `3bcf7c7f…ae42c6` |

**Camp's two fold-OFF digests are EXACT in run A**, and that is the whole diagnosis in two rows.

### A.3 — ⚑ **CONFIGURATION, NOT A PASS — and the determinism claim's HONEST SCOPE**

**(i) What the canonical determinism digest covers.** `canonical_digest(_surface(runs, term))`,
where `_surface` is **`terminal` + every wave dict + every event row + the player's
`hp` / `path_x` / `path_y` / `energy` / `circle_radius_m` tracks + every actor summary dict**.

**(ii) Where the two passes live.** ⚑ **They share no file, because pass-2 is NEVER SERIALISED.**
Pass-1's runs are kept (`cells[key]["_runs"]`), turned into `rows` by `extract_paths`, and written
to the one actor-paths file per cell per invocation (emitter lines 1642–1664). Pass-2's `runs2`
exists only long enough to produce `det2[key] = canonical_digest(_surface(runs2, term2))`.
⚑ **It is therefore structurally impossible for two files on disk to be pass-1 and pass-2 of the
same configuration.** Both passes of both configurations were zero-diff: **determinism ×2 is
12/12 in run A as well as run B.**

**(iii) The control that settles it empirically** — my own strip-compare, key by key:

| cell | actor count A / B | keys differing between `…145605` and `…145832` |
|---|---:|---|
| camp COU PX-LO | 25 / 25 | ⚑ **`started_utc` ONLY** |
| camp COU PX-HI | 25 / 25 | ⚑ **`started_utc` ONLY** |
| camp DEC PX-LO | 44 / 44 | ⚑ **`started_utc` ONLY** |
| camp DEC PX-HI | 44 / 44 | ⚑ **`started_utc` ONLY** |
| all **eight** cluster cells | 46–116 / 46–116 | `started_utc` + `locomotion_census`, `loco_run_stats`, `clusters`, `T4b_strict_dwell`, `spans_vs_I17`, `conservation`, `graded_distance`, **`actors`** (+ `D_I12_5`, `per_wave_floor` on six) |

⚑ **Camp carries `movement_fold=False` — no `MovementPolicy` object is ever constructed there — and
camp's artifacts are byte-identical across two separate OS processes.** The payload moved on
exactly the cells where a `MovementPolicy` exists and nowhere else. **That is a configuration
difference with a named mechanism, and it is cross-process knot-level determinism besides.**

**(iv) What it cost the board** — the experiment's price, so the conductor can see it was not free:

| cell | run A (per-wave) | run B (ladder, the record) |
|---|---|---|
| `cluster_defon` COU PX-LO | @152, `l4l` 49.7143 | @152, `l4l` 50.0408 |
| `cluster_defon` COU PX-HI | ⚑ **@152, 36.2449** | ⚑ **@156, 155.3469** |
| `cluster_defon` DEC PX-LO | ⚑ **@152, 49.7143** | ⚑ **@156, 165.3061** |
| `cluster_defon` DEC PX-HI | @156, 144.0000 | @156, 155.5102 |
| **all four camp cells** | **identical to B** | **identical to A** |

**(v) ⚑ THE SCOPE LIMIT NOBODY ASKED ME FOR, AND IT IS MINE TO STATE.** I-1's determinism check
hashed **both** the surface **and** the knot rows (`sha256_knots_a` / `_b`). **I-18's hashes the
surface only.** The `r.movers` knot polylines that the actor-paths artifacts serialise are
therefore **outside** the ×2 comparison. The camp byte-identity in (iii) is the empirical backstop
at knot level and it is **partial by construction** — four cells of twelve, and the four with no
policy object. ⚑ **Restoring the knot-row leg of the determinism check is a candidate for the next
lap's instrument, and I am naming it rather than leaving the conductor to find it.**

### A.4 — HYGIENE DISPOSITION (D-I15-6 precedent honoured: on the record, in my own commit)

| artifact | disposition |
|---|---|
| **12 `…145605` actor-paths, COMMITTED in-tree** | ⚑ **REMOVED** (`git rm`, engine `6c223443`). Digests recorded in § A.5 below; **git is the archive** and the bytes stay recoverable. 15 MB of look-alike payload beside the record carries one risk — being mistaken for the record — and now carries none. |
| **1 `…105605` findings, UNTRACKED** | ⚑ **COMMITTED** (engine `6c223443`). 392 KB that carries the entire proof — the RED fold-off table, the wall, the grades. **The evidence is kept; only the bulk look-alikes go.** |
| the pinned `…145832` set + `…105832` findings | **UNTOUCHED.** All twelve re-hashed from this seat and **EXACT** vs § 11. |

### A.5 — THE REMOVED SET'S DIGESTS, FULL 64 HEX (GL-6), SO THE ANSWER OUTLIVES THE FILES

| cell (`…-20260814_145605.json`) | sha256 |
|---|---|
| `camp-defoff-coupled-px-lo` | `35aeec99942c5f3242c711744dc6a1225a285e070ff78a1fdd312f40b58f051e` |
| `camp-defoff-coupled-px-hi` | `733c872733bfb62e8302e1511d3d0ab16f45fedc1879eab44796eaa3a6610488` |
| `camp-defoff-decoupled-px-lo` | `dedd9c35e1a8ea1ca37d2bbad9de51d0d311e009d6b9e4365a309e08629f13a8` |
| `camp-defoff-decoupled-px-hi` | `3aa2bc06cc59f42b783baaf99f217e0b66fd98dfb1ec81f4cdd07df14a2bc378` |
| `cluster-defoff-coupled-px-lo` | `da894e360f9271aef3f9258af49dad7e681a162247cff4fad33b3e5a984d44e2` |
| `cluster-defoff-coupled-px-hi` | `e13d327ae24adf1af469d3949bffa58ef2c9004a534bd1afedd6a3a41ecac572` |
| `cluster-defoff-decoupled-px-lo` | `3aac16485c5c839a4c7e372f12a12f476d2c9bda3c6443b2493098a77ff76712` |
| `cluster-defoff-decoupled-px-hi` | `972820f651a3a33b9e8491bbd511e4f94a16710eed2ca9a4a5e550e25da3b553` |
| `cluster-defon-coupled-px-lo` | `0124f69e3d989afac4a9d51ead6bb4be90a2ad14598a35c55fcccc594ff2e771` |
| `cluster-defon-coupled-px-hi` | `ab57683be464f7ff7254d7411b7a6abdd7e996b2f6a9c998a46bdb662585e0fb` |
| `cluster-defon-decoupled-px-lo` | `56b8fafce6cc498a1f8d014cd8caf8f0ca25f7cb5de44da5aa0eefb8d4d157ec` |
| `cluster-defon-decoupled-px-hi` | `c7333ecab082aedbe9408771761b63a98228c9b7a469103c98e936408a1c6775` |

### A.6 — ⚑ WHY IT HAPPENED, WITHOUT AN EXCUSE ATTACHED

The findings doc was committed **by name** (one path); the actor-paths were committed **by glob**.
The glob caught both emissions and the by-name add caught only one, so run A's payload rode into
`77ee6302` silently while its findings sat untracked. **`D-I15-6` is the same shape and I had
already been shown it once.** The mechanical fix is to stamp an emission set with the invocation
that produced it and add by set, not by glob; the discipline fix is that a landing note must
account for **every** file the lap wrote, not every file the lap **used**.

---

## B — ⚑ `C-I18-2` / `D-I18-7` **REPAIRED, SIM-SIDE: LADDER-SCOPED WINS**

### B.1 — The ruling, and what I did with it

R-PM4-44 part 4: `MovementPolicy` state is **LADDER-SCOPED**. The referent is one continuous fight
(**Matt's longest stationary span is 1.73 s across all ten waves**), and the incumbent lineage has
run ladder-scoped for eleven iterations. **The docstring's "state is PER WAVE" was aspiration, not
measurement.** ⚑ **This is a Discipline #12 SEMANTIC SHIFT and it is framed as one in the code,
not buried as a fix** — the comment that stood at the construction site argued the opposite case in
so many words, and the new comment quotes it before reversing it on measurement.

| # | change | file |
|---|---|---|
| **1** | ⚑ `MovementPolicy` docstring **AMENDED** to ladder-scoped, citing R-PM4-44 part 4 / `D-I18-7` / `C-I18-2`, with the old prose quoted and both deciding measurements named | `kc2/movement.py` |
| **2** | ⚑ `simulate_wave`'s per-wave fallback construction **REPLACED BY A RAISE**. `simulate_wave` is a per-wave entry point with no ladder identity to hang state on, so building there silently handed the player a fresh cadence phase and free cooldown resets at every boundary. **The refusal is in the code so it cannot be undone by a call site** — the same idiom the adjacent `C-I4-7` refusal already uses | `kc2/run.py` |
| **3** | ⚑ `ladder_movement_policy()` added as **THE** canonical construction site, named by the refusal message. Fifteen drivers + the adapter each hand-rolled the same four lines while a **sixteenth**, per-wave one hid in a fallback — duplicated construction is exactly how a scoping divergence survives eleven iterations before F5-M/F5-E trips on it | `kc2/run.py` |

### B.2 — ⚑ THE AFFECTED-CALLER CENSUS — **MEASURED, NOT ASSUMED**

| caller | passed `movement_policy` before? | scope | affected? |
|---|---|---|---|
| the fifteen `i4…i18` drivers | **YES**, once into `fold_kw` outside the wave loop | ladder | **no** |
| `export/kc2_run_adapter._player_fold_state` | **YES**, once per ladder, threaded | ladder | **no** |
| `tests/` | never sets `movement_fold` | — | **no** |

⚑ **The removed branch had NO live caller.** It was the only per-wave construction site in the
tree and the only place the old docstring was actually implemented. **A semantic implemented only
where nothing calls it is a trap, not a policy.**

### B.3 — ⚑ **REPRODUCTION, NOT RE-MODELLING — 12 / 12 BYTE-IDENTICAL**

The record-cell configuration was re-run **once** under the changed code (wall 77.2 s). Since
`started_utc` is the artifact's only time-dependent leaf, it was pinned to the banked
`2026-08-14T14:57:16.617954+00:00` and the file re-serialised through the emitter's own
`json.dumps(..., indent=1, default=str, ensure_ascii=False)`:

| ⚑ **RECORD-CELL ARM** | banked `…145832` = re-emitted | |
|---|---|---|
| `cluster-defon-coupled-px-lo` | `217608ab3d00056dd21a4ac74e21e865f5ff31949fe36ecaf3fce68dbf1ee640` | ⚑ **BYTE-IDENTICAL** |
| `cluster-defon-coupled-px-hi` | `d0a2ffba712171bad524f33b5e4d2bf2c1a491e31acca700b101d87e5dc95ba0` | ⚑ **BYTE-IDENTICAL** |
| `cluster-defon-decoupled-px-lo` | `0b9bf3ecd41fa14939fea81754be1ad4c04689aaccd92a552e5325889910f06c` | ⚑ **BYTE-IDENTICAL** |
| `cluster-defon-decoupled-px-hi` | `57c732d09eb5a93b4e50ff8453c6f4637df510f12d992d40b02e76ada1f2e310` | ⚑ **BYTE-IDENTICAL** |
| the other **eight** cells | § 11's digests | ⚑ **BYTE-IDENTICAL — 12 / 12** |

⚑ **And the whole findings document differs in EXACTLY 26 LEAVES, every one a timestamp
artefact**: 12 filenames, the 12 file-hashes those filenames' embedded `started_utc` perturbs,
`started_utc`, `wall_s`. **Every measured leaf is identical**, verified leaf-by-leaf:

| surface | banked | re-run |
|---|---|---|
| assert wall | 26 / 26 | ⚑ **26 / 26** |
| predictions | 17 / 23 | ⚑ **17 / 23** |
| structural | 1 / 3 | ⚑ **1 / 3** |
| fold-OFF digests (6) | EXACT | ⚑ **identical dict** |
| determinism ×2 digests (12) | zero-diff | ⚑ **identical dict, zero-diff 12/12** |
| `law_3.moved` / witnesses | `{}` / 34 | ⚑ **`{}` / 34** |
| every cell's death wave + `l4l` | § 1 / § 1.2 | ⚑ **to the digit** |
| every sensitivity limb | § 10 | ⚑ **to the digit**, incl. `S-SPEED-ONLY` w154 38.12244897959184 |
| `U-P-N-1` / PX designations | DEFERRED / COLLAPSED | ⚑ **DEFERRED / COLLAPSED** |

**The re-emitted verification artifacts were deleted after comparison** — reported here rather than
left beside the record, which is the entire lesson of § A. Their raw (unpinned) digests are in
engine commit `6c223443`'s working record; the findings doc hashed
`96fee4f3a4c683ae38337cdf91052c88065eb384f3fcde023c4c10187eba10eb`.

### B.4 — LAW 3 AND THE PRE-REGISTERED CLAIMS

**`law_3.moved == {}`, 34 witnesses, re-measured from the emitted bytes.** ⚑ **Zero constants
move** — the diff is a docstring, a comment block, a `raise`, and a constructor that forwards
arguments it does not choose. **No number is typed into Python by this change.**

| # | pre-registered claim (math note § 5) | outcome |
|---|---|---|
| **R.1** | four record-cell artifacts byte-identical | ✅ |
| **R.2** | **all twelve** byte-identical | ✅ |
| **R.3** | wall 26/26, predictions 17/23 | ✅ |
| **R.4** | fold-OFF EXACT ×6 | ✅ |
| **R.5** | `law_3.moved == {}` | ✅ |
| **R.6** | 296 kc2 tests pass; the one PRE-EXISTING `test_AC_10_10` failure still the only failure | ✅ |
| **R.7** | the fallback is unreachable, so removing it changes nothing that runs | ✅ (R.1–R.4 are its evidence) |

⚑ **7 / 7.** Written before the diff existed; the git order is the proof.

### B.5 — WHAT THIS CELL DID **NOT** TOUCH

* ⚑ **`export/` — not one line.** `_spawn_tick`'s LAST-STILL-TICK arithmetic and the eight refused
  batons are **star-lord's** follow-on cell. ⚑ **The batons must REPRODUCE the banked `…145832`
  knot digests, never re-model them** — those digests are now proven reproducible from a
  ladder-scoped sim, so an adapter that agrees with them agrees with the record.
* **No I-18 driver.** The record has to reproduce from the same driver bytes, and it did.
* **No verdict key, scorecard, bracket or sensitivity limb re-opened.**
* **No constant.**

---

## C — TO THE CONDUCTOR

| id | disposition |
|---|---|
| ⚑ **`C-I18-3`** | ⚑ **ANSWERED.** The `…145605`/`…105605` set is the `D-I18-7` per-wave experiment — a **CONFIGURATION**, not a pass. **The determinism-×2 claim SURVIVES**, structurally (pass-2 is never serialised) and empirically (camp byte-identical across two processes; ×2 zero-diff 12/12 in *both* runs). **I-18's adoption should finalise on this answer, not re-open.** |
| ⚑ **determinism SCOPE** | ⚑ **VOLUNTEERED, § A.3(v).** I-18's ×2 digest covers `_surface()` only, **not** the `r.movers` knot polylines. I-1's covered both. **Restoring the knot leg is named as a next-lap instrument candidate.** |
| ⚑ **hygiene** | ⚑ **DONE IN MY OWN COMMIT** (`6c223443`), D-I15-6 precedent honoured: twelve look-alike artifacts removed **with their digests on the record**, the untracked findings **committed** because it carries the proof. Cause named in § A.6 without an excuse attached. |
| ⚑ **`C-I18-2` / `D-I18-7`** | ⚑ **SIM-SIDE REPAIRED** (`0c100c16`), framed as a **Discipline #12 semantic shift**. **Record reproduced 12/12 BYTE-IDENTICAL; 26 differing leaves, all timestamps.** Law 3 `{}` / 34. **`export/` untouched — star-lord's cell is unblocked and its target digests are proven.** |
| ⚑ **MIGRATION** | filed (`1bd16b8d`): **call contract tightened, zero schema changes, zero telemetry migration required.** |
| **push** | **NOT PUSHED.** Engine `e247faa9`, `6c223443`, `0c100c16`, `1bd16b8d` await your seat. |

---

**Author:** gamora (simulation seam) · 2026-08-14 · **the catch was right, the answer is mine, and
the record did not move a single measured byte.**
