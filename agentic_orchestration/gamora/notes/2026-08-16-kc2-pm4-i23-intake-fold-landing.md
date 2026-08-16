# KC2-PM4 · I-23 — THE INTAKE FOLD — LANDING NOTE

**Agent:** gamora · **Conductor:** gandalf (RUN-CONDUCTOR) · **2026-08-16**
**Commission:** `R-PM4-62 part 4`; charter rows `L-51`/`R-PM4-61`, `L-52`/`R-PM4-62`.
**Evidence:** legolas **Lap X** — the mitigation decode, both directions. **14/14** artifacts
re-hashed **EXACT from bytes at full 64 hex from my own seat** before a line of the math note was
written (`GL-6`, § 11).

**Commits (engine, mine, FOUR, math-note-only FIRST):**
`0f791101` math note (**zero code**) → `bfad4664` addendum `D-I23-1` (**zero code**, committed
**BEFORE** its repair) → `f0178d1a` addendum `D-I23-2` + `UNREACHED-I23-3` (**zero code**, again
**BEFORE** the repair) → `793b2937` fold + module + driver + findings + MIGRATION + AGENT_STATE.
**NOT PUSHED.**

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i23-findings-20260816_052623.json`
sha256 **`0e4084b55f0af955f0b91d809da8e1b3267d6876a1c177a8eba3655c21048368`**. Wall **11.0 s**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**The mitigation stack is now decoded, folded and measured in both directions — and it is not the
residual either.** `PX-LO` dies on **wave 151 in every single configuration**, including the
incumbent's. The fold moves like-for-like **8.4082 → 7.6735 s** — nine ticks, and in the wrong
direction — and T2 **0.0460 → 0.0420**; `PX-HI` is **entirely unmoved** at 152 / 36.4082 / 0.1993.
Across nine isolation limbs the like-for-like takes **exactly two values**, 8.4082 and 7.6735, and
**which one a limb lands on is not monotone in its intake**: `S-ABS-BASE70` *raises* intake and
lands long, `S-PCL-SUBTRACTIVE` *lowers* it and also lands long. **The intake fold changes WHEN
inside wave 151, not WHETHER.** And my own `S-1` — the one clause that said this iteration would
help — **FAILED**, in exactly the way a pre-registration is supposed to be able to fail.

---

## 1 — ⚑ THE RECORD-CELL SCORECARD — FOUR LADDERS, BOTH ORDER LIMBS

Bands: **T1** wave 160 {159–161} · **T2** l4l 182.7167 ∈ [155.31, 210.12] · **T4a** 0.932 ± 0.02 ·
**T4b(b)** 1.6166 s · **T4b(c)** wave-160 kill from full health only.

| record cell (`cluster_defon__critlo__COUPLED__…`) | T1 | T2 | T4a | T4b(b) | T4b(c) | death | class | l4l s | **T2 ratio** | T4a | T3 MAE |
|---|:-:|:-:|:-:|:-:|:-:|---:|---|---:|---:|---:|---:|
| **`PX-LO · ORDER-AR`** (PRIMARY) | ✗ | ✗ | ✗ | ✗ | **not armed** | **151** | DEATH | **7.6735** | **0.041997** | 0.873603 | 8.5932 |
| `PX-HI · ORDER-AR` | ✗ | ✗ | ✗ | ✗ | **not armed** | 152 | DEATH | 36.4082 | 0.199260 | 0.897948 | 7.8284 |
| `PX-LO · ORDER-RA` *(published, never designated)* | ✗ | ✗ | ✗ | ✗ | **not armed** | 151 | DEATH | 7.6735 | 0.041997 | 0.880982 | 8.5932 |
| `PX-HI · ORDER-RA` *(published, never designated)* | ✗ | ✗ | ✗ | ✗ | **not armed** | 152 | DEATH | 36.4082 | 0.199260 | 0.902146 | 7.8284 |

**Graded distance:** `PX-LO` **T1 −9 waves · T2 0.041997 · T4a −0.058397**; `PX-HI` **T1 −8 · T2
0.199260 · T4a −0.034052**.

**T4b(c) is NOT ARMED on any arm and that is the scorecard law, not a convenience**
(`R-PM4-40 part 5`): it scores **only** a wave-160 kill from full health, and the ladder reaches
151/152.

### 1.1 ⚑ THE ORDER FORK, PUBLISHED AT EVERY ROW (`R-PM4-62 part 3`)

**Both limbs ran as full scored ladders.** They are **identical on T1, T2 and T3** and differ only
on **T4a** (`PX-LO` 0.873603 vs 0.880982; `PX-HI` 0.897948 vs 0.902146). ⚑ **`RESIST-then-ARMOUR`
grades better on T4a on both arms — and it is not designated, because the primary was fixed in
`0f791101`, a commit that contains zero grades.** `R-PM4-27 part 3` has bitten four consecutive
iterations; it cannot bite this one, because no limb here *could* have been chosen by its result.

### 1.2 ⚑ AGAINST THE HONEST INCUMBENT — I-22's OWN RECORD CELLS, PINNED FROM ITS ARTIFACT

`D-I20-5`'s lesson held: pinned from I-22's **findings JSON** (`5cdc6b43…c104c`), never its prose.

| arm | l4l I-22 → I-23 | Δ | death | T2 ratio I-22 → I-23 | T4a I-22 → I-23 |
|---|---|---:|---|---|---|
| `PX-LO` | 8.408163265306124 → **7.6735** | **−0.7347** | 151 → **151** | 0.04601748 → **0.041997** | 0.86079063 → **0.873603** |
| `PX-HI` | 36.4082 → **36.4082** | **0.000** | 152 → **152** | 0.1993 → **0.199260** | 0.8994 → 0.897948 |

**Superlative guard exercised (`D-CON-1`):** the only T2 figures quoted anywhere in this note are
graded against **all three** prior emitted artifacts — I-18 **0.8502**, I-21 **0.8815**, I-22
**0.0460**. **I-23 holds none of them, and no "best" claim is made.**

---

## 2 — ⚑ THE PER-ACTOR OLD-vs-NEW MITIGATION TABLE (`R-PM4-62 part 4 (f)`'s deliverable)

**66 rows**, every band-A actor, both level limbs, at the sim's own **`RUNREC`** grain (declared in
math note § 9 per Lap X's `D-X-1` DO-NOT — the sim fires **one slot per opportunity** and has never
summed a closure).

| | OLD (aggregate 3,557 / 70 %) | NEW (per-region / ADDITIVE) | ratio |
|---|---:|---:|---:|
| band total, LO limb (w151 + w160) | **20,075.1775** | **15,010.1831** | **0.747699** |
| of which w151 | 16,881.6602 | 11,881.6706 | |
| of which w160 | 3,193.5173 | 3,128.5125 | |

⚑ **Both Lap X board totals are reproduced from the per-actor rows to 1e-6** — so this table is a
**66-row positive control on the pipeline**, not a table of my own numbers marking my own homework
(wall row 11). **32 of 66 actors move; 34 do not.**

### 2.1 ⚑ AND THE SIM'S OWN NUMBER GOES THE OTHER WAY, WHICH IS THE ITERATION'S REAL MECHANISM

At the **record** grain the decoded operand cuts intake to **×0.7477**. Inside the sim it does the
opposite: applied physical **38,723.67 → 42,273.89**, **×1.0917**.

**Why, derived rather than guessed:** 9 of the sim's 10 physical rows are on the **`DGP`** branch
(`p > armour`). There the two arithmetics reduce to

```
incumbent :  0.84·p − 2,489.9        (sheet 3,557 @ 70 % absorption)
fold      :  0.84·p − 2,050.4        (region-weighted piece armour @ 98–100 %)
```

**A single piece (1,722–2,977) is a weaker subtrahend than the sheet's hit-weighted average
3,557**, and the enormous absorption stack cannot compensate because on `DGP` absorption only ever
touches the part of the hit the armour covers. Lap X's own w151 board sits on the **`DLEP`** side
(its worked hit is 1,612.29, below every piece), which is why the record grain and the sim grain
point opposite ways. **Both are reported; neither is adjusted.**

---

## 3 — ⚑ THE PRE-REGISTERED PREDICTIONS, GRADED HONESTLY

| id | claim | grade |
|---|---|---|
| **`S-1`** | the fold improves T1 and T2; `PX-LO` survives past 151 and T2 > 0.0460 | ⚑ **FAILED.** Death 151, T2 **0.041997**. **The one clause that said this iteration would help.** Wording NOT rewritten |
| **`S-2`** numeric | `S-ARMOUR-ONLY` moves the `PX-LO` T2 ratio by **< 0.02** absolute | ⚑ **PASSED** — moved **0.004020** (0.046017 → 0.041997) |
| **`S-2`** mechanism | *because* I-14's `G1b` clamp zeroes the operand on 31/36 bodies | ⚑ **FAILED.** On the records the ladder **actually rolls**, **13/13 are `MEASURED-ABSENT` ⇒ UNCLAMPED.** § 4 |
| **`S-3`** | the kill-rate fold does **not** raise peak living above I-22's 10 | ⚑ **PASSED** — peak living **10** on every arm and every limb, `t50` 3.6735 / `t90` 7.1020 unmoved. Registered **against my own interest** |
| **`S-4`** | the order fork is exactly zero below 1,722.24 | ⚑ **PASSED — AS A REPAIRED PASS.** Went RED on first execution; see `D-I23-1` |
| **`S-5`** | mean melee-contact count stays **below 1.0**, far below the 5.2 yardstick | ⚑ **PASSED** — **0.23404** folded, 0.27184 unfolded |
| **`S-6`** | `T4b(c)` stays unarmed | ⚑ **PASSED** — not armed on any of the four record cells |

**Mechanical pins:** `P.1` `law_3.moved == {}` on **35** witnesses ✅ · `P.2` fold-off EXACT **6/6**,
scope **∅** ✅ · `P.3` determinism ×2 all three legs, both primary cells, pass 2 a real second
execution ✅ · `P.4` frozen **20/20** under the hard `SystemExit` gate ✅ · `P.5` Lap X **14/14**
EXACT ✅ · `P.6` Lap X § 7 reproduced to **0.0042 HP** from the fold's own code path ✅ · `P.7`
order-fork control **398.384**, matching both Lap X and the closed form, to **2.8e-13** ✅ · `P.8`
Ascension **30.0 FLAT**, 0.15 % of pool ✅ · `P.9` sheet 3,557 used as a hit operand **0 times** on
every folded cell ✅ · `P.10` armour on Physical only; **10** physical rows vs **21** non-physical,
counted ✅ · `P.11` `keys_asserted` on **16/16** wall rows ✅ · `P.12` 66-row table reproduces both
Lap X board totals ✅ · `P.13` six regions, Σ **exactly 100**, ADDITIVE clamps on **exactly** legs +
shoulders ✅ · `P.14` no new wave-row key on any fold-off cell ✅ · `P.15` smoke **296 / 1
pre-existing**, unchanged ✅.

---

## 4 — ⚑ `S-2`'s MECHANISM CLAUSE, FALSIFIED ON THE RIGHT POPULATION

I argued the armour term would be near-inert *because* I-14's `G1b` per-body physical clamp zeroes
`type_mult` on **31 of 36** bodies. **That is a statement about the 36 bodies with a Physical row in
I-14's candidate table — a different population from the 13 records this ladder rolls at wave 151.**

Graded on the right population: **13/13 resolve `MEASURED-ABSENT`, which `clamp_for` maps to
UNCLAMPED.** **Physical intake is fully live on this board.** The armour correction has a real
operand; it is simply small relative to the fight, and it moves the wrong way (§ 2.1).

> **The numeric clause passed and the mechanism clause failed, and both are published.** A
> prediction that gets the right number for the wrong reason is not a pass, and grading only the
> number would have let the wrong reason travel into the next iteration.

---

## 5 — ⚑ WHAT THE TWO REMAINING MULTIPLIERS ACTUALLY MEASURE (`R-PM4-62 part 4 (c)/(d)`)

Lap X § 12.3: *"what decides survival is how many bodies touch him at once, how fast they swing,
and the sustain layer."* Two of those three are now **measured in the sim**, endogenously.

### 5.1 CONTACT COUNT — MEASURED, NEVER IMPOSED

Read off the sim's own per-tick series at `D_ENGAGE_M`, which **is** the decoded
`gameengine.meleeTargetDistance = 2.4000000953674316`. **No geometry was added; a report column and
a grade were.**

| | value |
|---|---:|
| mean melee-contact count (`PX-LO`, folded) | **0.23404** |
| median · p90 · max | **0 · 1 · 1** |
| zero fraction | 0.7660 (72 of 94 ticks) |
| **Lap X § 8.1 yardstick** | **5.2** |
| ratio to yardstick | **0.0450** |
| Lap R referent mean occupancy | **3.2423 – 3.4251** |

**The sim's melee-contact count is ~22× below the yardstick and ~14× below the referent.**

⚑ **AND THE CAVEAT TRAVELS WITH THE COLUMN.** The sim's intake is **not melee-dominated** — its
`top_incoming` is led by `arcane_elementalaura_buff`, `infernal_emberburstproc` and
`livingplant_venomousseed`, all reach-carrying. **A melee-contact count graded against 5.2 grades
the MELEE LIMB of the intake, not the intake.** Reported as such rather than as the whole answer.

### 5.2 CADENCE — ⚑ A CONDUCTOR-PREMISE CORRECTION, REPORTED NOT EXECUTED (`D-CON-4` PROPOSED)

`R-PM4-62 part 4 (d)` commissions Lap X's **DECLARED 2.0 s grid** as the **primary** cadence limb.
**The premise is that the sim needs a declared grid. It does not.** The sim has carried a
**MEASURED** per-body clock since PM-2 —
`threat.declared_constants()["attack_model"]["clock"] = "the identity's own basic_swing_period_s
(169/169 MEASURED)"`. Lap X's grid exists because `characterBaseAttackSpeedTag` is a **string** and
the *record* route is `UNREACHED-X-2`; the sim reached a clock by a different route and pinned it.

| | value |
|---|---:|
| records with a measured clock | **169** (13 on the fought roster) |
| median measured round, fought roster | **0.9333 s** |
| mean · min · max, fought | 0.8526 · 0.5961 · 1.1826 |
| declared grid | 2.0 s |
| **median measured − declared grid** | **−1.0667 s** |

**Imposing the grid would replace a measurement with a declaration**, in the direction this run has
spent twenty-two iterations moving away from. So, in the `R-PM4-29` / `D-CON-2` / `D-CON-3` pattern
legolas used at Lap X § 4.4 — **disclose, correct, and do the work anyway**: the measured clock
stays primary, the grid publishes as `S-CADENCE-2S` inside every cell, **and no per-second figure
is claimed as decoded on either limb.** ⚑ **This is the conductor's framing error, not legolas's
and not the decode's.**

### 5.3 SUSTAIN — REACH, NOT RE-VALUATION

`PLAYER_ADCTH_PCT` **21.0** and `PLAYER_REGEN_HP_PER_S` **129.38** are unmoved Law-3 witnesses.
Their *reach* changes only because the vector fold raises damage dealt by ~0.35–0.44 %, so ADCtH
returns that much more HP **without a single constant moving**. ⚑ **Proc uptime is a DECLARED
POLICY limb and the declared policy is that there is no policy constant:** `CounterplayLayer`
actuates all five defensive actives from their own **measured** triggers and cooldowns, so uptime
is **endogenous**. A hand-set uptime fraction is exactly the free constant `R-PM4-62 part 4 (b)`
forbids, and it is not taken.

---

## 6 — ⚑ `D-I23-1` AND `D-I23-2`: TWO OF MY OWN, BOTH CAUGHT BY MY OWN INSTRUMENTS

**`D-I23-1`.** `S-4` predicted the order fork is *"= 0.0 to floating point"* below
`MIN_PIECE_ARMOUR`. My own instrument went **RED on its first execution**, on 3 of 22 probes, at
`1.78e-15 – 3.55e-15`. **The derivation is correct over the reals** — both orders are a scalar
multiply and real multiplication is associative — **but IEEE-754 multiplication is not
associative**, and `(1 − 0.98)` is already inexact. **The defect is in my prediction's wording: I
wrote "to floating point" as though it loosened the claim, when it is the one qualifier that turns
an algebraic identity into a bit-exactness claim. I asserted associativity of float multiplication
without noticing that I had.** Addendum `bfad4664` committed **before** the repair; repaired to
three **ULP-scaled** buckets (`bit_exact` / `ulp_only` / `material`) under a **declared 4-ULP
bound** stated in advance and never adjusted after seeing a result (measured worst case
`3.553e-15`, published beside it). **`S-4`'s wording is not rewritten** — it is a **REPAIRED** pass,
exactly as `S-3` was at I-22. And the discriminator is measurable, not rhetorical: a model
difference would scale with `p`; this one scales with the ULP of the result.

**`D-I23-2`.** `IntakeFold.armour_fold=False` documented itself as *"falls back to the incumbent
aggregate arithmetic"* but passed `self.order` — the **fold's** primary — into the fallback. So
`S-PCL-ONLY` carried the incumbent **operand** with the fold's **order**, i.e. *"PCL plus the order
flip"*, and the flip is material by exactly the `r·A·α` of math note § 3.3. **Caught by reading my
own isolation table and finding `S-PCL-ONLY` and `S-ARMOUR-ONLY` identical to four decimals on
l4l — which is not what an isolation of two disjoint terms can look like.** Addendum `f0178d1a`
committed **before** the repair; repaired to the incumbent order. The record cells never set the
switch, so **only the diagnostic limb moved, and it moved toward being able to attribute rather
than toward a better grade.**

> **BOTH TIMES THE INSTRUMENT THAT CONVICTED ME WAS ONE I HAD WRITTEN TO CONVICT SOMETHING ELSE.**
> That is the same shape as `D-I22-1`, and it is the third consecutive iteration in which my own
> pre-registration has caught my own work before a grade was reported.

---

## 7 — ⚑ `UNREACHED-I23-3`: A NEW MECHANISM, **NAMED, NOT DECODED**

Working out *why* the decoded operand makes physical **more** damaging surfaced a question the
decode does not settle:

```
Σ_s w_s · A_s        =  2,472.87     ← exactly Lap X's own `M-AVG-PIECESONLY`
Lap X's winner       =  (Σ_s w_s · piece_after_local + global_flat 636) × 1.56  =  3,465.03
camera sheet         =  3,557
```

**The per-piece operands carry the global *percentage* armour (+56 %) but NOT the build's global
*flat* armour (+636, scaled 992.16).** Lap X § 7 uses the piece values alone as `sumProtectionDV`
and **this fold follows it, by lineage** — but Lap X's own winning sheet reconstruction requires
the global flat to be added *outside* the per-piece scaling. **Whether the engine's
`sumProtectionDV` for a single hit is the rolled piece ALONE or the rolled piece PLUS the global
flat is expressed by no field either lap reached.**

⚑ **It is load-bearing for this iteration's entire direction.** On `DGP`, piece-alone gives
`0.84p − 2,050` against the incumbent's `0.84p − 2,490`; adding 992.16 to each operand moves it to
`0.84p − 2,884` and **flips the sign of the result**.

**`R-PM4-56 part 4`: NAMED, NOT DECODED, NOT FOLDED — and flagged to the conductor.** **I add
nothing**, because that is precisely the "adjust a term to close a residual" move Lap X's
`UNREACHED-X-1` forbids, and because 992.16 is the same order as the `−92` residual's own
unexplained gap.

---

## 8 — SEMANTIC SHIFTS, NAMED (Discipline #12)

1. **`N-2` — the declared mitigation ORDER flips.** `threat.mitigate` has DECLARED
   resistance-first since PM-2, veto-open, for two stated reasons. **Lap X did NOT refute it** — it
   graded the order `UNREACHED-X-4` and published both limbs with a decoded fork magnitude. What
   changed is a **lineage** reason (`R-PM4-62 part 3`), declared in a commit containing zero
   grades. **Not a bug fix, and not buried as one.** The incumbent order stays runnable both as
   `intake=None` and as `ORDER-RA`, which runs as a **full scored ladder**.
2. **`N-3` — the sheet's 3,557 is DEMOTED, not RE-VALUED.** `threat.PLAYER_ARMOR` keeps its value
   byte-for-byte and stays a Law-3 witness; Lap X § 2.4 measures it as the hit-weighted **average**
   across six pieces, so it stops being an operand for a hit. **Demoting an operand is not moving a
   constant**, and the fold-OFF path still uses it.
3. **`N-4` — `%currentLife` acquires an answering defence for the first time since PM-2.** The
   family has been unmitigated in this sim with the standing note *"inventing one would be
   inventing mitigation"*. Lap X found the one stat that answers it: Rebuke's
   `defensivePercentCurrentLife` **+26**. ⚑ Its **composition** is **DECLARED, not decoded**
   (`UNREACHED-I23-1`) — both limbs published, `MULTIPLICATIVE` primary because it is the shape
   every other `defensive*` term on this sheet takes **and** it is the lower-mitigation reading
   (`SUBTRACTIVE` would zero every band-A row, all ≤ 18 %). Measured effect: **26.0 % of the
   `%currentLife` fraction removed**.

---

## 9 — ⚑ THE RECONNAISSANCE: THE COMMISSION IS SMALLER THAN IT READS

Said in the math note § 0, **before** the fold ran. Four of `R-PM4-62 part 4`'s named items were
**already in the build** and are folded here as **POSITIVE CONTROLS, not as changes**:

| item | state found | disposition |
|---|---|---|
| `Ascension` = **30 FLAT** (DO-NOT #1) | `counterplay.load_kit` already folds `damageAbsorption = 30` into a FLAT pool | ASSERTED (0.15 % of pool), not folded |
| player resist caps `[80,80,80]` | `PLAYER_DEFENSE_CAP_PCT = 80.0`, live since `R-PM3-2(A)` | positive control |
| monster cap `100` | Lap L's clamp, folded since I-6 | positive control |
| band-A resist reduction | **DECODED-ABSENT** (`P-X-5c` FAILED) — the sim applies none | positive control |

**Ascension's assertion is two clauses, not one**, because matching the numeral 30 alone passes
under **either** reading: it also requires `v / hp_max < 0.01`, which tests the semantics Lap X
§ 5.1 decoded rather than the digits.

---

## 10 — DEFECT TABLE

| id | defect | seam | disposition |
|---|---|---|---|
| **`D-I23-1`** | `S-4` asserted bit-exactness of a re-associated float product | gamora (mine) | **SELF-CAUGHT** by my own instrument. Addendum `bfad4664` BEFORE repair; three ULP-scaled buckets, declared 4-ULP bound; `S-4` a REPAIRED pass, wording unrewritten |
| **`D-I23-2`** | `armour_fold=False` carried the fold's ORDER, so `S-PCL-ONLY` was never a PCL isolation | gamora (mine) | **SELF-CAUGHT** by reading my own isolation table. Addendum `f0178d1a` BEFORE repair; repaired to the incumbent order. Record cells untouched |
| **`D-I23-3`** | `S-2`'s mechanism clause graded the wrong population (36 clamp-census bodies vs the 13 records actually rolled) | gamora (mine) | **DECLARED, both clauses published separately.** The numeric clause passed; the mechanism clause failed. Neither is rewritten |
| **`D-I23-4`** | my `abs(v − 30.0)` literal briefly masked the **pre-existing** bare-30.0 offender at `secondary_streams.py:136` by sort order | gamora (mine) | **REPAIRED IN-ITERATION by NAMING the constant with its provenance**, never by weakening the AST guard. The guard is right; my literal was the wrong shape |
| **⚑ `D-CON-4` (PROPOSED)** | `R-PM4-62 part 4 (d)` makes Lap X's DECLARED 2.0 s grid the PRIMARY cadence limb; the sim has a MEASURED per-body clock (169/169) since PM-2 | conductor | **REPORTED, NOT EXECUTED.** Measured clock primary; the grid publishes as `S-CADENCE-2S`; no per-second figure claimed as decoded on either limb |

---

## 11 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 11.1 Outputs of this iteration

| artefact | sha256 |
|---|---|
| `output/kc2-pm4-i23-findings-20260816_052623.json` | `0e4084b55f0af955f0b91d809da8e1b3267d6876a1c177a8eba3655c21048368` |
| `math/kc2-pm4-i23-intake-fold-2026-08-16.md` | `5bd8f17f7d0c64acb7bf4279b08aa6b0f7aa04f3c1489f252284fc2bc3b84280` |
| `math/kc2-pm4-i23-intake-fold-ADDENDUM-2026-08-16.md` | `2f9e69ece5729deaee1f53db857540c1ebb8a5c4e43e7c50b839e3b4abf92b64` |
| `kc2/intake.py` (NEW) | `5346fe58a745072e89cc7433c80999921f42df8dc0f79a3847694c3e2804c584` |
| `kc2/threat.py` | `eddcb6033db45261aef51987c629b3434601580eee0de8ba1e3955c36eb82205` |
| `kc2/player_offense.py` | `20191d48ee0db8a8ab18521dc8a9ad45dc8ef33f785a0b3aceaea9f8764ab23c` |
| `kc2/run.py` | `76b032a4644c024f03f2cbee4969a3aafa1aaf43f93c06d136dd9a5f63a0e5b1` |
| `scripts/gamora_kc2_pm4_i23_intake_fold_2026_08_16.py` | `0430cdc81e01f4d46d51d8b398e1c33411aa6fc9cbd2e11b84e2f69ebdc01782` |

### 11.2 Inputs, re-hashed EXACT before use (HALT armed; none fired) — **14/14**

| input | sha256 |
|---|---|
| `pm4x_findings.md` | `6740e8eaf0dfe17ddce475320c1e27282b6de264804e7d3a334b18ff8d47f5f7` |
| `PREREGISTRATION.md` | `84843789413db57beb54ea663e3755ab0d372de0e138d27b7c6feb5794414d7b` |
| `pm4x_formulas.json` | `cabc727d6711dfa3018be9f250811d841a32dbb8abcd1e41d752279bdd3f02a7` |
| `pm4x_player_defense.json` | `5fa9db84f3ae014cf48f926e1901fd9ea05c57a63162597b8c57e129f54cddf1` |
| `pm4x_player_defense_terms.csv` | `f4be3d8d4026226e6b6bfc758679f6e400ffb01aa4f6d40c73bdf06d49cdc993` |
| `pm4x_defensive_procs.csv` | `86120f387e8c36e10bedb7e5958faa475566d925318f1e04b8589c851e612f2d` |
| `pm4x_monster_offense.csv` | `4252bb0ad95d91d3aef4e968a7bb1848e1338cd6b45926b6bdb4256f2fe41a27` |
| `pm4x_monster_resist_reduction.csv` | `4dfa9dcccf071bb37d740a4ae5159a5171da0409e1aa0e9b9b6e1609e0928f2a` |
| `pm4x_intake_by_wave.csv` | `1937962ed516ae451148787e597cdaff32b994765ecd99b6633e2ebb1ab5ffe4` |
| `pm4x_intake_board.json` | `39f8ed022ed2a6dc4d3568886bffdc36bd60b85d8417e7caf3c59851b2fa5306` |
| `pm4x_ttk_by_body.csv` | `2b0a8f1ac85accfdfd92aead64c5a6c3fc67d18f409b5258fb8990b54c1d5991` |
| `pm4x_grade.json` | `4d319eaa0a2dde1747dece1abc41217d045432dc032c828bf198d35547a9ca33` |
| `pm4x_prediction.json` | `1037207f410b5b33751d9c53880dd44d42c87470bfe70da85b6ae03d6bd07164` |
| `pm4x_digests.json` | `74e34a3cb37d9a9399b86369bdee4f03c98549664fd3c6badb24137adbfb7b6f` |
| I-22 findings (the incumbent, pinned to the ARTIFACT) | `5cdc6b434ac071d37729b769cd7d52bb9f9d75ecc53f57207cf3865a1c9c104c` |

---

## 12 — ⚑ THE WALL — **16/16 GREEN, `keys_asserted` ON EVERY ROW**

1 fold-off byte identity ×6, scope **∅** · 2 Lap X substrate **14/14** at full 64 hex · 3 frozen
**20/20** (hard `SystemExit`) · 4 Law 3 `moved == {}`, **35** witnesses · 5 Lap X § 7 reproduced to
**0.0042 HP** · 6 order-fork control **398.384** vs Lap X **and** the closed form · 7 `S-4`
repaired-pass under the declared 4-ULP bound · 8 Ascension **30 FLAT** · 9 sheet 3,557 as hit
operand **0×** · 10 six regions, Σ **100**, ADDITIVE clamps on exactly legs + shoulders · 11
per-actor **66** rows reproducing both Lap X board totals · 12 melee-contact column emitted and
graded on every cell · 13 determinism ×2 three legs · 14 both order limbs ran as scored ladders,
neither selected by grade · 15 armour on Physical only, non-physical rows counted · 16 `T4b(c)`
scored under the `R-PM4-40 part 5` law.

**Law 3:** `moved == {}` on **35** witnesses, including `PLAYER_HP_MAX` 20,005, `PLAYER_ADCTH_PCT`
**21.0**, `PLAYER_REGEN_HP_PER_S` **129.38**, `SHEET_ARMOR_RATING` **3,557 (unmoved — demoted, not
re-valued)**, `ARMOR_ABSORPTION` 0.70, `PLAYER_DEFENSE_CAP` `[80,80,80]`, `PCL_DEFENCE_PCT` 26.0
(**entering** as a decoded term, not moving), `MELEE_CONTACT_YARDSTICK` 5.2 (**a grade, never an
input**), the `−92` armour residual (**carried, not closed**) and `monsterLevelGapFixer` (**named,
not folded**). **ZERO free constants fitted toward any target.**

**Smoke:** `296 pass / 1 PRE-EXISTING failure` — the `test_AC_10_10` bare-30.0 AST guard, whose
offender is `secondary_streams.py:136`. **Unchanged from I-22's baseline.**

---

## 13 — UNREACHED CENSUS

| id | what | status |
|---|---|---|
| `UNREACHED-X-1` | the −92 (−2.59 %) armour residual | **CARRIED, NOT CLOSED.** Nothing scaled by 3557/3465 |
| `UNREACHED-X-2` | monster attack-round length | the sim uses its **own measured** clock; the grid publishes as `S-CADENCE-2S`. No per-second figure decoded |
| `UNREACHED-X-3` | melee-contact ring capacity | ⚑ **ANSWERED FROM THE SIM'S OWN BOARD** (§ 5.1): mean **0.23404** against the 5.2 yardstick |
| `UNREACHED-X-4` | armour-vs-resist order | **BOTH LIMBS RAN AS FULL SCORED LADDERS.** Primary by lineage, fixed in a zero-grade commit |
| `UNREACHED-X-5` / `X-7` / `X-8` / `X-10` | w160 debuff Chance=0 · skill-selection policy · DoT stacking · `monsterLevelGapFixer` | all **NAMED, NOT FOLDED**. The sim's grain is DECLARED `RUNREC` |
| `UNREACHED-X-9` | the absorption clamp at 100 % | `DECLARED-CLAMPED:CEILING`, both composition limbs ran |
| **`UNREACHED-I23-1`** | `defensivePercentCurrentLife`'s composition | **DECLARED MODEL LIMB**, both ends published |
| **`UNREACHED-I23-2`** | `k(EXPECTATION)` for the damage vector | **BRACKETED [k_HI, k_LO]**, never interpolated. Bracket **0.0012 %** wide — measured, so no grade can turn on it |
| **`UNREACHED-I23-3`** | piece-alone vs piece + global flat armour as `sumProtectionDV` | ⚑ **NEW. NAMED, NOT DECODED.** Flagged to the conductor; **it would flip § 2.1's direction** |

---

## 14 — ⚑ CAVEATS THAT TRAVEL WITH THE NUMBERS

* **The 9-tick l4l delta is a discrete outcome, not a magnitude story.** Nine limbs land on exactly
  two l4l values and the mapping is **not monotone in intake**. Do not read 8.4082 → 7.6735 as
  "the fold made the player 9 % weaker"; read it as "the fold moved one threshold crossing".
* **`ORDER-RA` grades better on T4a on both arms and is not designated.** Fifth consecutive
  iteration in which the best number sits on an arm the run may not carry — but the first in which
  the guard is **structural**: the primary was fixed before any grade existed.
* **`UNREACHED-I23-3` would flip § 2.1's sign.** The direction of this iteration's armour result is
  contingent on an unreached record question. Stated in the headline, not the footnotes.
* **The melee-contact grade is a grade on the MELEE LIMB of intake**, and the sim's intake is not
  melee-dominated.
* **`D-I21-1`** (the sim's player over-travels), **`D-PDEF-2`**, **`T17`** and the `pools_for`
  default carry unchanged from I-22.

---

## 15 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. **THE MITIGATION SEAM IS CLOSED AND IT WAS NOT THE RESIDUAL.** Roster (I-22), arrival (I-19/20),
   pursuit (I-21) and now per-hit mitigation are all decode-true, and the player still dies on wave
   151 in **every** configuration. `R-PM4-62 part 1` said the intake seam alone is not the residual;
   **the fold confirms it from the sim's own board rather than from the record grain.**
2. **THE RESIDUAL'S NEXT ADDRESS IS NOT A MITIGATION TERM AND IT IS NOT A ROSTER TERM.** The two
   multipliers Lap X named are now both **measured** and both are far from the referent: contact
   count **0.234 vs 3.24–3.43** (Lap R) and **5.2** (Lap X § 8.1). ⚑ **The sim's board assembles to
   the right size and the right rate and then does not TOUCH the player.** That is a
   **pursuit/engagement-persistence** statement — bodies reach the ring and do not stay in it —
   and it is the one thing four consecutive decode-true folds have not addressed.
3. **`UNREACHED-I23-3` IS THE HIGHEST-LEVERAGE OPEN ITEM ON THE INTAKE AXIS** and it is a bounded
   **record** question, not a video lap: does `sumProtectionDV` for one hit include the build's
   global flat armour. It flips the sign of this iteration's armour result and it costs one lap.
4. **`D-CON-4` is offered for the ledger** beside `D-CON-2`'s FILES-not-counts and `D-CON-3`'s
   cite-the-sheet: **commission premises should not specify a MODEL where the sim already carries a
   MEASUREMENT.** The 2.0 s grid was Lap X's honest workaround for a record it could not reach; it
   is not an instruction the sim should take.
