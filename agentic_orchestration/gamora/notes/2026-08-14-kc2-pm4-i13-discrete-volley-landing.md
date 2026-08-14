# KC2-PM4 · I-13 — landing note: **T1 is MET, on the measured wave — and the mechanism the lap is named for had nothing to do with it.**

> **Run:** KC2-PM4 · **Iteration:** I-13 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** **R-PM4-34 part 6** (charter ledger **L-25**), on **Lap M** (legolas `4671aa66`).
> **Wall obligations:** **R-PM4-33 part 3** (ledger **L-24**, jack-ryan's wall-of-walls audit).
> **Math note (committed BEFORE the code):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i13-discrete-volley-2026-08-14.md`
> — commit `08570475`, **its own commit. The git order is the proof.**
> **Judged against:** the **L-19 re-derived bands** and the **I-12 critLO** pinned surfaces.

---

## 0 — The one-paragraph answer

**The player dies. On wave 160. 3.5102 s into it. T1 is MET for the first time in this run, on
exactly the wave Lap K measured** — and the like-for-like truncates at that death to **186.6122 s**
against the referent's measured **182.7167**, a ratio of **1.0213×**, the closest T2 the run has
produced. **But the co-landing mechanism the commission is named for did not fire and could not
have:** `max n_coincident == 1` over all **57** ring firings at the record collision-width cap, and
`S-MULT-OFF` — the fold with the multiplicity limb switched off entirely — reproduces the record
cell's l4l **to the digit**. What killed the player is the **magnitude** limb: two MEASURED terms —
the `combatformulas` attribute multiplier and the body's own `offensiveTotalDamageModifier`
passives — that **no monster in this simulation has ever carried, on any wave, since PM-2.** The
lap named for arrival structure closed a decode gap instead, **and I pre-named that exact structural
error as `S-1` in the math note before running.**

---

## 1 — WHAT LANDED

**Engine commit range:** `08570475..47e1ad0d` (5 commits) · **meta:** this note.

| # | commit | what |
|---|---|---|
| 1 | `08570475` | **MATH NOTE**, its own commit, before any code |
| 2 | `c8a40ce2` | the fold — `kc2/discrete_volley.py`, two pinned CSVs, one field on `ThreatEngine`, one keyword on `simulate_wave` |
| 3 | `63e36d73` | driver, six knot artifacts, findings |
| 4 | `0ba9fbdc` | six baton specs + nine additive `KC2RunSpec` fields + `_volley_population()` |
| 5 | `47e1ad0d` | six batons, FULL 67/67 each + `MIGRATION.md` |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

**⚑ BATONS — SIX, FULL 67/67 green (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33):**

| cell | baton sha256 |
|---|---|
| **`cluster_defon__critlo` ← RECORD** | `72339a5aeb4a18147fe40230259f42ec075397550d256fbb618052ede29037c8` |
| `camp_defoff__critlo` | `cb863bd31955e5fcf2e7224e0ba2f505fd5e2f38b59203681936eb83bd3b1fbb` |
| `cluster_defoff__critlo` | `ee913924b394b70f0a6622ff2bdb22f02a55fa3058cff61589e7f7e3e81d6697` |
| `camp_defoff__crithi` | `6c34919619b6c44d4d77625c1066b377b205f1a57c4b8bef1937bd0b6ff0865e` |
| `cluster_defoff__crithi` | `4c9c57b9457a2f10588f471ac213269d719d580d7e56afa182101e56ed00282a` |
| `cluster_defon__crithi` | `8656b4e9087da8bb349f8a5cd82b4e9c001cea802ba82643262c62aaa87ffcda` |

**Findings:** `dd8b76d4786c72dd04ec0caf10838457e848213f8334c3ef486b7f7898b8d5b9`
(`kc2-pm4-i13-findings-20260814_083602.json`)

**Knot supplies:**
`8d789ab2f65ced5aecab20e47b2e9fa1c81ae7f0d0dd5b6fbd7ffa484a3ba034` **cluster-defon/critLO** ·
`d7bdfaeef00919317ca3e2ada4818e1c91c673f96d798b4525b30685879218f5` camp/critLO ·
`98e391bd8237ea1173913fbf6d54c87aaf8c9ab495fd796517c7718a150c4495` cluster-defoff/critLO ·
`1421c57b5892263b779ac40483aaac91a53ce98096d56358f7773f135b3cb723` camp/critHI ·
`b008fe0b6703688307d710f04b5c9dc8c4ba8ccd12dd54e9c9f08bd1008755b8` cluster-defoff/critHI ·
`23d1fc03f212db3d88e16b54aecbfb46ed538a20aba8f3364886d60dc6947af0` cluster-defon/critHI

**Determinism ×2 (0 differences, all six):**
`f811d9d2efe11806608e991b10167f8fa01d505af3134044086e5b9073f5504e` **record** ·
`9fe003dcfdd06930fa375b7c50a0c1dd1e97ea3a5b5fe6f626b48282810e494f` ·
`33794b297e67789b6061c75395def5ed8db926c92a11f539a98638dd858f4f13` ·
`282fa79f75790376270ceed5bc11dee61832e2b1a5bd670d84f2ab392e54f089` ·
`6cec2df9ab6bb331555fb5d9c51b28cbad8be6ad0f1479cfbb136dde5e6e54a6` ·
`c147e59f88c51ed2890e116291f2dfe9d503385e4d802c57e0433aa137316365`

**Lap-M substrate pins, EXACT vs legolas's own `pm4m_digests.json`:**
`fb8624cb0ef4b6c292ad5f1d6b89bdb55ac0ba01eded25e52434c9f4e00a4797` body-chain ·
`5af996789064870486c44d49e9686a8f5245e37b54f11d294456568f3254e0d3` candidate-table

### 1.1 — ⚑ FOLD-OFF BYTE-IDENTITY, EXACT ×3, WITH THE KEY GENUINELY ABSENT

| cell | fold-OFF surface | vs I-12 critLO |
|---|---|---|
| camp_defoff | `ccbab7f9a8d1349ee9f3fad7d0c625439265f67eb6071213c22e13d3dcc705a0` | **EXACT** |
| cluster_defoff | `b6d6fef55c31a69bf111c61e31b99efbaa62f1ad51c7a248bfb73445f8c327b5` | **EXACT** |
| cluster_defon | `05e3c3ff159e48ea6b15efc9c496e37534cf55b1a040b333b77559bb77316c70` | **EXACT** |

`monster_volley` **omitted**, not passed as `None`, on all 30 fold-off waves — the **seventh** use
of ABSENT-not-None in this run.

**⚑ AND CHECK 2 EARNED ITS KEEP ON THE FIRST CELL, BEFORE ANY NUMBER WAS PUBLISHED.** The first
run RED'd it: my ladder had not threaded I-10's `PhaseModel.ENGAGE`, so the fold-off arm was
measuring the arrival model rather than the volley fold. **It failed CLOSED and it failed first.**
That is the argument for running the byte-identity arm before the matrix, every time.

---

## 2 — ⚑ THE SCORECARD vs THE L-19 BANDS (record cell `cluster_defon__critlo`)

| | target | I-12 critLO | **I-13 RECORD** | verdict |
|---|---|---:|---:|---|
| **T1** death wave | **160** {159–161} | `arena_tier_exhausted` @171 | ⚑ **`player_death` @160** | ⚑ **MET — first of the run** |
| **T2** l4l | 182.7167 ∈ [155.31, 210.12] | 205.306 (1.1236×) | ⚑ **186.612 (1.0213×)** | **MET — closest of the run** |
| **T3** MAE | — | **4.462** | 6.331 | worse — **§ 5.1** |
| **T3** median ratio | 1.000 | 1.0656 | 1.0656 | unmoved |
| **T3** w154 ratio | 1.000 | 2.7005 | **2.7005** | unmoved (D-I12-5) |
| **T3** w160 ratio / inverted | 1.000 / no | 0.8556 / no | 0.1353 / **yes** | ⚑ **truncation artefact — § 5.1** |
| **T4a** mean HP | 0.932 | 0.9591 | **0.9107** | **MET**, and now *below* the video |
| **T4b(a)** dwell | 7.4167 s @ 0.2919 | 20.980 s @ 0.2557 | 5 excursions, 1 matching shape | fires |
| **T4b(b)** full-health dwell | 1.6166 s | n/a (no death) | ⚑ **0.0 s** | **MISSED** |
| **T4b(c)** instant kill | ≤1 tick on w160 | did not fire | **did not fire** | **MISSED** |

**Match gates:** MG-1 **MET** · MG-2 MISSED · MG-3 MISSED · MG-4 MISSED · MG-6 **MET** ·
**MG-7 MISSED** (was MET at I-12) — the dash-rate gate flips because the run now ends at 186.6 s
instead of 600.9 s. **A gate measuring a rate over a run that is a third as long is not the same
measurement**, and it is reported as a truncation consequence, not a regression.

### 2.1 — ⚑ THE DEATH, ATTRIBUTED FROM THE WIRE

```
wave 160 · t = 3.5102 s into the wave · run_tick 2286 · 27 live bodies
killing row : aetherialvanguard_arcanemissilenova.dbr (slot chain_initial) — 3,655.90 applied
killing tick cluster : 3,655.90 over ONE row
```

> **⚑ THE PLAYER WAS GROUND DOWN, NOT ONE-SHOT.** The killing blow is a single 3,656 row against a
> 20,005 pool. **T4b(c) is MISSED and the reason is measurable rather than inferred:** the deepest
> single-tick cluster anywhere in the record cell is **14,618.98 at wave 159, from 36 rows, at
> `hp_frac_before = 1.0000`** — the co-landing shape the referent died to, at exactly full health,
> reaching **73.1 %** of the pool and no further. `n_clusters_at_or_above_pool = 0`.

---

## 3 — ⚑⚑ THE LAP'S LARGEST FINDING: THE MECHANISM IS NOT THE COMMISSIONED ONE

### 3.1 The multiplicity limb is a measured NO-OP, and it was pre-registered as one

| | record cap (`r_cap` = player radius 0.32 m) |
|---|---|
| ring firings | **57** |
| `n_coincident` histogram | ⚑ **`{1: 57}`** |
| `max_n_coincident` | ⚑ **1** |

**`S-MULT-OFF` — the entire multiplicity limb switched off — lands l4l `186.6122448979592`, T3 MAE
`6.3312991836734565`, terminal `player_death@160`: the record cell to the last digit.** The
co-landing fold contributes exactly nothing to the run of record.

**This was P.9, and it was written before the code**, together with the reason: at the sim's own
body separation the ring's angular resolution is too coarse. The wendigo nova needs the player
within **0.640 m**; the closest any ring firing came, over 74 firings of the I-12 baton, was
**0.712 m**. **The sim's own non-overlap invariant keeps the player 7 cm too far away.**

### 3.2 What actually killed him — the attribution split, measured

| cell | limbs active | l4l | terminal |
|---|---|---:|---|
| **record** | magnitude + multiplicity + hit law | **186.612** | `player_death@160` |
| `S-MULT-OFF` | magnitude + hit law | **186.612** | `player_death@160` |
| `S-HITLAW-OFF` | magnitude + multiplicity | 187.592 | `player_death@160` |
| `S-MAG-OFF` | multiplicity + hit law | **192.490** | `player_death@160` |

**The magnitude limb is the fold.** Multiplicity is worth 0.000 s; the hit law (removing the miss
limb) is worth −0.980 s; the magnitude terms are worth −5.878 s **and they are what carries the
board from "cannot produce the death" to producing it on the measured wave.**

### 3.3 ⚑ AND THE SIM REPRODUCED LAP M'S HEADLINE NULL RESULT FROM ITS OWN SIDE OF THE WIRE

Lap M: *no single application on the wave-159/160 board reaches 20,005; max 16,813.58.*
This fold, composed independently through the sim's own `mitigate()`: **max single application
16,453.49**, and the difference from Lap M's figure is **360.09 = 0.1 × 3,600.9 — exactly the crit
multiplier on the `PercentCurrentLife` limb**, which Lap M applies and this model never has.
**Two decodes, one firewalled from the other, reconciling to the cent.** The positive control makes
it a wall check: **103 families compared, 0 residuals above 1.1 × 10⁻³, worst 7.18 × 10⁻⁴.**

---

## 4 — ⚑ `C-I13-1` IS VERDICT-DIVERGENT, AND IT WAS DECLARED SO BEFORE THE RUN

The math note § 3.5 stated, before any code existed, that **unlike D-I12-1 and D-I12-2 this bracket
would NOT be verdict-identical**, and that the LOWER limb was of record **because the HIGHER limb
is the one that produces the run's headline target**.

| | **record — `r_cap` = player radius (0.32 m)** | **`S-CAP-HI` — + `projectileExplosionRadius`** |
|---|---|---|
| terminal | `player_death` @ **160** | `player_death` @ **159** |
| l4l | 186.612 | 167.265 |
| `n_coincident` histogram | `{1: 57}` | ⚑ `{1: 33, 3: 7, 12: 1}` |
| max single-tick cluster | 14,618.98 | ⚑ **20,005.00** |
| **T4b(c)** | did not fire | ⚑ **FIRED** |

> **⚑ AND THE HI LIMB REPRODUCES THE REFERENT'S DEATH SHAPE ALMOST EXACTLY.** Its T4b(c) event:
> `hp_before = 1.0000`, `span_s = 0.081633`, wave 159. The referent (L-19): full health → 0 in
> **0.0834 s**, wave 160. **Same shape, one wave early, and it is produced by a single
> 12-projectile `avris_bloodorbnova` co-landing.**

**Routed to the conductor as `C-I13-1`.** The discriminating question — does
`projectileExplosionRadius` measure damage capture along a projectile's *path* or only at its
*terminus*? — is not in the corpus. **I did not resolve it by preference, and the direction of my
preference would have been the flattering one.**

---

## 5 — THE WAVE-SPAN TABLE

| wave | measured (L-19) | I-12 critLO | **I-13 RECORD** | I-13 ÷ measured |
|---:|---:|---:|---:|---:|
| 151 | 16.27 | 18.286 | **18.286** | 1.124 |
| 152 | 16.25 | 16.571 | **16.571** | 1.020 |
| 153 | 14.75 | 16.735 | **16.735** | 1.135 |
| 154 | 14.12 | 38.122 | **38.122** | 2.701 |
| 155 | 16.32 | 14.041 | **14.041** | 0.861 |
| 156 | 20.20 | 22.449 | **22.449** | 1.111 |
| 157 | 18.85 | 15.755 | **15.755** | 0.836 |
| 158 | 13.10 | 11.510 | **11.510** | 0.879 |
| 159 | 26.30 | 29.633 | **29.633** | 1.127 |
| **160** | 25.95 | 22.204 | ⚑ **3.510 (death)** | 0.135 |
| **l4l** | **182.72** | 205.306 | ⚑ **186.612** | **1.021** |

**⚑ Waves 151–159 reproduce I-12 critLO to 0.0 s, all nine.** Wall check 6 asserts the first eight
formally: `n_waves_compared == 8`, `max_abs_span_delta_s == 0.0`. That is not a coincidence and it
is the fold's cleanest structural property — **no folded record appears before wave 159**, so the
entire divergence is confined to where the decode reaches.

### 5.1 — T3 got worse, and the honest reason is arithmetic, not the model

MAE 4.462 → **6.331** and `w160_inverted` flips back to **true**. Both are consequences of the same
fact: **wave 160 is scored at 3.510 s because the player died in it.** The ratio 0.135 is a
truncated wave measured against a complete one. **I am not reporting an improvement I did not earn,
and I am not reporting a regression I did not cause.** The comparable quantity is l4l, which is
`start of w151 → death` on both sides — **186.612 against 182.7167** — and it is directly
comparable for the first time in the run, exactly as R-PM4-34 part 6 anticipated.

---

## 6 — ⚑ THE CRIT BRACKET IS NO LONGER VERDICT-IDENTICAL. R-PM4-28's PREMISE HAS MOVED.

| judged quantity | critLO | critHI | DIVERGES |
|---|---|---|---|
| T1 | MET | MET | no |
| **T2** | **MET (186.612)** | ⚑ **MISSED (155.265)** | ⚑ **YES** |
| **T3 w160 inverted** | true | *n/a — died at w159* | ⚑ **YES** |
| T4a | MET | MET | no |
| T4b(c) | did not fire | did not fire | no |

> **⚑ `cluster_defon__crithi` LANDS l4l = 155.2653 AGAINST THE BAND FLOOR OF 155.3092 — IT MISSES
> T2 BY 0.0439 s, BY BEING TOO FAST.** In thirteen iterations this run has never once failed a band
> by being too quick. **The math note pre-registered exactly this failure mode** (P.4: *"T2's
> verdict is UNCERTAIN and the band's LOWER edge is inside my interval… this is the first lap in
> which T2 is at risk of failing by being TOO FAST"*). I predicted it for the record cell; it
> happened one cell over. **The mechanism was right and the location was wrong.**

**`D-L5` is no longer immaterial.** Two laps measured the bracket verdict-identical and R-PM4-28
designated critLO on that basis. The third measurement breaks it. **The critLO designation is
carried this lap for continuity only, and the conductor should know it is now a choice with
consequences rather than a measured wash.**

---

## 7 — PRE-REGISTERED PREDICTIONS vs OUTCOME

**Graded against the math note § 8 table, pinned in the driver before the run.**

| # | prediction | outcome | verdict |
|---|---|---|---|
| **P.1** | waves 151–158 reproduce I-12 EXACTLY (sum 153.469388) | max delta **0.0 s**, sum 153.469388 | ⚑ **CONFIRMED** |
| **P.2** | the cell dies, on wave **159** | dies on wave **160** | ⚑ **FALSIFIED — and on the measured wave** |
| **P.3** | death 1.0–6.0 s into the wave | 3.5102 s | **CONFIRMED BY BAND, FALSIFIED IN MECHANISM** (§ 7.1) |
| **P.4** | l4l ∈ [154.5, 159.5] | **186.612** | ⚑ **FALSIFIED — by 27 s** (§ 7.2) |
| **P.5** | T4b(c) does NOT fire | did not fire | **CONFIRMED** |
| **P.6** | T4b(b) does NOT fire | dwell 0.0 s | **CONFIRMED** |
| **P.7** | T4a ∈ [0.93, 0.96] | **0.9107** | **FALSIFIED** |
| **P.8** | T3 MAE = 4.69 ± 0.03 over **8** scored waves | 6.331 over **10** | **FALSIFIED** — the run reached w160, so ten scored |
| **P.9** | multiplicity is a NO-OP: `max n == 1` | `{1: 57}`, max 1 | ⚑ **CONFIRMED** |
| **P.10** | `S-CAP-HI` DIVERGES on T1 | @159 vs @160, n=12, T4b(c) fires | ⚑ **CONFIRMED** |
| **P.11** | camp/critLO still dies at w154 | dies @154 | **CONFIRMED** |
| **P.12** | positive control: 103 families, < 1.1e-3 | 103, worst 7.18e-4 | **CONFIRMED** |
| **P.13** | `S-MULT-OFF` reproduces the record EXACTLY | l4l identical to the digit | ⚑ **CONFIRMED** |
| **P.14** | `S-LEECH-INCUMBENT` dies EARLIER | identical to the record | **FALSIFIED** (§ 7.3) |
| **P.15** | fold-OFF byte-identity ×3, key ABSENT | 3/3 EXACT, 0 waves with key | **CONFIRMED** |
| **P.16** | critHI verdict-identical | **DIVERGES on T2 and T3** | ⚑ **FALSIFIED — § 6** |

**8 confirmed / 1 split / 7 falsified.**

### 7.1 — P.3 passed its band on the wrong wave

I predicted 1.0–6.0 s **into wave 159**. The death is 3.5102 s **into wave 160**. The predicate I
pinned compared the offset without the wave, so it graded True. **Reported as a mechanism failure
and not banked as a hit** — the same discipline I applied to I-12's P.3.

### 7.2 — P.4 is the cleanest falsification, and the estimator's flaw is nameable

I priced the death from a tick-walk over I-12's own arrival stream and got 1.143 s into w159. It
landed 30.6 s later in run-time. **The estimator re-priced the folded rows' magnitudes but applied
no counterplay absorption to them** — every I-12 `damage_applied` was already post-absorb, and my
re-priced rows were not. That is exactly the throughput-shaped miss I named as **T-1** in § 8.1 of
the math note, and it is the one place my pre-named *throughput* candidate was right.

### 7.3 — P.14, and why the leech correction is measured immaterial rather than merely declared

`S-LEECH-INCUMBENT` reproduces the record cell to the digit: `n_leech_rows_excluded = 2` over the
whole ladder. **The D-M-1 semantic shift is correct and it is worth nothing on this trajectory** —
Curate Ignus's weapon attacks (where the 13,392.6 leech figure lives) never landed. **The
correction stands on its measurement, not on its consequence**, which is the right way round: I did
not adopt it because it helped, and it did not help.

### 7.4 — ⚑ THE UNIFYING ERROR I PRE-NAMED, AND THIS TIME IT WAS RIGHT

Math note § 8.1 named **S-1 (STRUCTURAL)** first, per R-PM4-31 part 5:

> *"The lap is named for multiplicity and its content is magnitude… whatever the run does, it does
> with the attribute multiplier the sim never had… T1 will have been solved by closing a magnitude
> under-read rather than by modelling coincidence."*

**That is precisely what happened.** After two consecutive laps whose pre-named unifying errors
were themselves wrong in the same throughput-shaped direction, **the conductor's method amendment —
name a STRUCTURAL candidate first — produced a correct prediction on its first application.** The
amendment is worth keeping and the evidence is this row.

---

## 8 — THE MATRIX AND THE SENSITIVITY CELLS

| cell | terminal | l4l | mean HP | T3 MAE | max n | max tick cluster |
|---|---|---:|---:|---:|---:|---:|
| **`cluster_defon__critlo` ← RECORD** | **death@160** | **186.612** | 0.9107 | 6.331 | **1** | 14,619.0 |
| `cluster_defoff__critlo` | death@160 | 178.286 | 0.9132 | 5.795 | 1 | 12,386.7 |
| `camp_defoff__critlo` | death@154 | 83.837 | 0.8833 | 7.126 | 0 | 5,479.8 |
| `cluster_defon__crithi` | death@**159** | ⚑ **155.265** | 0.8918 | 7.167 | 1 | 5,790.3 |
| `cluster_defoff__crithi` | death@160 | 180.408 | 0.9070 | 7.247 | 1 | 11,554.3 |
| `camp_defoff__crithi` | death@159 | 146.612 | 0.8644 | 7.929 | 1 | 5,664.2 |

**⚑ Every cell in the matrix now dies.** Five of six die in {159, 160}; the camp/critLO cell dies at
w154 exactly as it has since I-11 (P.11 CONFIRMED — no folded record appears before w159, so that
cell is the I-12 cell).

| sensitivity | terminal | l4l | max n | T4b(c) | what it measures |
|---|---|---:|---:|---|---|
| ⚑ `S-CAP-HI` | death@**159** | 167.265 | ⚑ **12** | ⚑ **FIRES** | C-I13-1's HI limb — **verdict-divergent** |
| `S-RANGE-R1` | death@160 | 190.041 | 1 | no | C-M2 near limb (×0.70/0.50/0.40) |
| `S-RANGE-R3` | death@160 | 185.633 | 1 | no | C-M2 far limb (×1.30/1.35) |
| `S-MULT-OFF` | death@160 | **186.612** | 0 | no | ⚑ **identical to the record** |
| `S-MAG-OFF` | death@160 | 192.490 | 1 | no | the magnitude limb is worth −5.878 s |
| `S-HITLAW-OFF` | death@160 | 187.592 | 1 | no | the hit law is worth −0.980 s |
| `S-LEECH-INCUMBENT` | death@160 | **186.612** | 1 | no | D-M-1 measured immaterial here |
| `S-PCL-VOLLEY` | death@160 | **186.612** | 1 | no | immaterial while `n == 1` |

**⚑ The C-M2 range bracket is VERDICT-IDENTICAL** (190.041 / 185.633 vs 186.612; no verdict moves).
Reported as Lap M's C-M2 disposition: **immaterial to this run**.

---

## 9 — ⚑ THE ASSERT WALL — 18/20, AND THE FOUR OBLIGATIONS DISCHARGED

**Wall spec landed IN the math note § 9** (W-5) — the first time in this run — with every predicate
written out as an explicit comparison over named quantities.

| obligation (R-PM4-33 part 3) | how it landed |
|---|---|
| **check 14 → full stream** | **check 18** counts `ManaBurnDrain` over **every event of every run** of the record cell and reports `n_events_scanned` beside `n_manaburn_rows`. The `top_incoming(n=8)` truncation is retired. **D-I8-3 is now certified, not asserted.** |
| **predicate-less check → `report`** | **check 21** emits status `report` and is **excluded from the n/N**. Scored wall is 20, not 21. Retires I-12's literal-`True` check 15. |
| **checks 11/12 → restore or justify (W-6)** | **check 15** restores I-11's runtime `n_absent` limb that I-12 silently dropped; **check 7** puts its own numeral (`103`) back in its predicate, repairing the class that let I-12's "79,240" live only in a name. Both narrowings named in the math note. |
| **un-nest `law_3` (D-6b)** | the findings artifact carries `law_3.moved` at the top level, **literally `{}`**, matching the prose. |

### 9.1 — ⚑ TWO REDS, BOTH MINE, BOTH THE WALL SPEC — **AND THE NEW RULE IS WHAT FOUND THEM**

| check | what | why RED |
|---|---|---|
| **1** | "…7 pins, 0 mismatched" | the predicate asserts `n_pins == 7`; the driver hands it the **3** Lap-M pins. `n_mismatched_pins == 0` holds. |
| **5** | "Law 3 — `moved` is the EMPTY dict (**12** witnesses)" | the witness set holds **11**. ⚑ **`moved == {}` HOLDS** — the Law-3 property is intact. |

**Both failed CLOSED. Both underlying properties hold. And both are `W-3` catches** — a numeral in a
check's *name* asserted in its *predicate* and found wrong about the world. **Under I-12's form
neither would have existed to fail.** This is the fifth consecutive lap whose only REDs are my own
wall spec (I-9 {12,18} → I-10 {2,12} → I-11 {7} → I-12 {5} → I-13 {1,5}), and it is also the first
lap where the failure was *manufactured by a rule designed to manufacture it*.

**Not repaired mid-lap**, per jack-ryan's precedent affirmed at R-PM4-33 part 3.

---

## 10 — WHAT GOES TO THE CONDUCTOR

| id | what | disposition |
|---|---|---|
| **⚑ `C-I13-1`** | projectile collision width. **LO (record) → death @160, no T4b(c). HI → death @159, `n=12`, T4b(c) FIRES with the referent's shape (full health → 0 in 0.0816 s vs the measured 0.0834 s).** The first verdict-divergent bracket of the run. | **ROUTED** — both limbs measured; the corpus does not say whether `projectileExplosionRadius` captures along the path or only at the terminus. Not resolved by my preference, and my preference would have been the flattering one. |
| **⚑ `D-L5` / R-PM4-28** | **the crit bracket is NO LONGER verdict-identical**: critHI misses T2 by 0.0439 s, by being too fast. | **ROUTED** — the critLO designation is now a choice with consequences, not a measured wash. |
| **⚑ successor lap** | the attribute + own-passive under-read is **GLOBAL**; this lap closes it on **16 of 344** actors. The other 328 still fight at a ~×10 magnitude under-read. | **ROUTED — the largest un-owned magnitude quantity the run has surfaced.** Note the direction: closing it everywhere will make the board *harder*, on every wave, and may move T2/T3 across the whole ladder. |
| **`D-I13-1`** | R-PM4-34's D-M-3 is wrong on its second clause. `in_frozen_baton_roll` reads NO on **144** rows, `159` on 24 and `160` on 28; the 52 flagged rows are **exactly** the nine roster records I derived independently from the baton. **The flag is EXACT.** | **ROUTED** — ledger correction. The conductor's roster conclusion stands; the defect claim about the column does not. No conclusion of mine leans on the column (the population comes from `actors[].record_path`). |
| **`D-I13-2`** | Lap M § 6.6's *"no projectile speed field exists in the corpus"* is true of the FX records and **false of the skill records**. `projectile_velocity` is populated on **1,222** rows of the sim's own pinned CSV, including **every** Lap M top candidate (9.0 / 10.0 / 9.0 / 14.0 / 12.0). | **ROUTED — `C-M1` retires as a cliff.** It was filed as "the highest-value single measurement left"; it was already in the substrate. |
| **`D-I13-3`** | `offensiveLifeLeech` is treated as health damage **globally** in `threat.py`; this lap corrects it on folded records only, to protect the I-11/I-12 baselines. Measured immaterial here (2 rows). | **ROUTED** — the global correction wants its own lap. |
| **`C-I13-2`** | deferred projectile arrival. `t = d / v` is derivable from two measured columns (instrumented: **57 firings, latency 0.060–3.240 s**), but consuming it is a **TICK-ORDER** change and raises "does damage in flight land after its caster dies?" against this run's own no-swinging-from-beyond-the-grave rule. | **ROUTED** — not improvised inside an offence lap (the I-7 § D-I7-3 precedent). |
| **`D-I12-5`** | w154 = 2.7005×, **unmoved a fourth time**. Still 51.2 % pet-TTL wait. | carried — targeting/locomotion, R-CPB-4's surface |

---

## 11 — ⚑ THE LAW-3 LEDGER, CLOSED HONESTLY

The fold multiplies the direct-family output of 16 actors by ~×10, and those actors sit exactly
where T1's acceptance window sits. **Five discriminators, all checkable, all pre-registered:**

1. **Every term is decoded by an OUTCOME-FIREWALLED lap.** Lap M read no sim output.
2. **The arithmetic is in the math note, before the code.** The 16,453.49 ceiling, the `{1: 57}`
   histogram, the 0.640 m threshold, the ×2.04/×2.86 intake ratios — all computed and pinned first.
3. **Three of six limbs REDUCE damage** (physical clamp: 147 rows clamped · leech exclusion ·
   the record collision cap, measured a no-op) **and the record cap is the limb that does NOT
   produce the death.**
4. **The ring predicate EXCLUDES two rows that would have helped** — the Sentinel's 31,783
   `eldritchrain` and `avris_bloodorbburst`'s 15,768, both on decoded column semantics.
5. **Scope was WIDENED from actor-keyed to record-keyed** specifically to break the coincidence
   with {159–161}. `S-SCOPE-ACTOR` exists to measure it.

**`moved: {}`.** No constant in the Law-3 witness set moved. `player_radius_m()` and
`PTH_MULTIPLIERS[1]` are READ, never set. **Zero new free constants: every magnitude, cadence and
geometry term in this fold traces to a pinned row.**

---

## 12 — WHAT I DID **NOT** TOUCH

The player's offence entire (I-11/I-12) · the two-branch armour law · the crit bracket's own
machinery · the uncapped disc · `TICK_S` and the master clock · the **board-roll RNG** · the
arrival-phase model (I-10 `ENGAGE`) · the converging solver, τ, the non-overlap invariant ·
`TICK_ORDER_I5` · movement, dash, counterplay · I-9's sustain actuation · eHP · the seed
(conductor seed 9) · **DoT rows of folded bodies** (Lap M prices instant arrival only) ·
`generation/`, `element/`, `telemetry/`, `output/` · **⚑ no telemetry schema — VERIFIED from the
emitted bytes, not claimed** (the I-13 record baton's `waves[]` key set is identical to I-12's, key
for key; the D-I12-7 lesson applied). `export/` only via nine additive `KC2RunSpec` fields, one
`_volley_population()` helper and one ABSENT-not-None branch.

**Operational:** the lap ran **sequentially**, end to end, twice (once RED on check 2, once clean).
**No Discipline #3 exposure at any point.**

---

**Author:** gamora (simulation seam) · 2026-08-14 · **math note first, code second, and the git
order is the proof.**
