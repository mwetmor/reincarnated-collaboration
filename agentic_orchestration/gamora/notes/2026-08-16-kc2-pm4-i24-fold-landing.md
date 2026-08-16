# KC2-PM4 · I-24 — **THE FOLD** — LANDING NOTE

**THREE AMENDMENTS IN ONE FOLD · THE FALSIFIER FIRED · THE ANSWER IS STRUCTURAL**

**Agent:** gamora · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** `R-PM4-65 part 4` + `R-PM4-66 part 4`; charter rows `L-53`/`R-PM4-63`,
`R-PM4-64`, `L-55`/`R-PM4-65`, `L-56`/`R-PM4-66`.
**Base:** my I-23 intake fold (`793b2937`) + my I-24-D census instrumentation (`d4ff7e8b`).

**Commits (engine, mine, FOUR — the first THREE are zero code):**
`0cfe660c` math note **ALONE** → `27d2d1b9` addendum #1 `D-I24-2` (**before** its repair) →
`732914f8` addendum #2 `D-I24-3` (**before** the artifact reporting it) → `79aceb7b` the fold
(`kc2/ring.py` NEW · `kc2/kinematics.py` NEW · `intake.py` · `run.py` · `engagement.py` ·
`player_locomotion.py` · driver · findings · MIGRATION · AGENT_STATE). **NOT PUSHED.**

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i24-findings-20260816_072225.json`
sha256 **`e7c2f1ba111b3be782d1dca034807c8db56365af7fc71ce6741f0887037d1993`**. Wall **13.0 s**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**`F-I24` FIRED.** The falsifier I pre-registered in a commit containing zero grades asked one
question — *does matching the referent's kinematics raise ring occupancy?* — and the answer is
**no, and it lowers it.** `S-Z-ONLY` (ring repair alone) reaches mean occupancy **0.26596** on
`PX-LO`; `ALL` (all three amendments) reaches **0.17857**, against a criterion of ≥ 2× and max > 2.
The player's straightness moved **0.2229 → 0.1107** toward the referent's 0.060 — the kinematics
fold *worked* — and the board still did not converge on him. **The serialisation of arrivals at
contact range is STRUCTURAL, not kinematic**, and per the pre-registration this fold **REPORTS**
it: no parameter was adjusted, no shape was swapped, no limb was re-declared, and `K-MILL` stands
character for character as the math note specified it.

⚑ **The falsifier was symmetric on purpose, and it convicted all three of its targets in one
measurement: the conductor's `R-PM4-65 part 2` hypothesis, my own § 5.2 lineage reading, and this
amendment.**

---

## 1 — THE T-SCORECARD, ALL FOUR TARGETS, BEFORE → AFTER

`FOLD-OFF` **is** I-23, byte-for-byte and to the seventeenth digit.

| | `FOLD-OFF` (= I-23) | `ALL` (record) | Δ |
|---|---:|---:|---|
| **`PX-LO` T1** death wave | 151 (`player_death`) | 151 (`player_death`) | **unmoved** |
| **`PX-LO` T2** l4l · ratio | 7.6735 s · 0.04200 | **9.1429 s · 0.05004** | **+1.47 s** |
| **`PX-LO` T3** MAE | 8.5932 s | **7.1238 s** | **−1.47 s** |
| **`PX-LO` T4a** mean hp frac | 0.8736 | 0.8530 | −0.021 (target 0.932) |
| **`PX-LO` T4b(b)/(c)** | ✗ / ✗ | ✗ / ✗ | unmoved |
| **`PX-HI` T1** death wave | 152 | **151** | ⚑ **WORSE — `E-10` FAILED** |
| **`PX-HI` T2** l4l · ratio | 36.4082 s · 0.19926 | 9.7959 s · 0.05361 | **−26.6 s** |
| **`PX-HI` T3** MAE | 7.8284 s | 6.4708 s | −1.36 s |
| **`PX-HI` T4a** | 0.8979 | 0.8607 | −0.037 |

⚑ **AND THE BEST NUMBER SITS ON AN ARM WITHOUT THE KINEMATICS FOLD.** `S-YZ · PX-HI` — amendments
(a) + (b), no `K-MILL` — reaches **l4l 160.1633 s, death wave 156, T2 ratio 0.87657**, four waves
further than anything else this iteration. It is **not designated** and it is **not a run best**:
I-21 holds 0.8815, pinned from its own artifact. **`R-PM4-27 part 3`, sixth consecutive iteration
in which the best number sits on an arm the run may not carry.**

`T4b(c)` **armed and UNFIRED on every cell** (`R-PM4-40 part 5`): no cell died on wave 160, the law
was checked cell-by-cell inside `scorecard_of` rather than from this driver, and `⚑ LAW_HELD` is
asserted on wall row 17. **`E-9` HELD.**

---

## 2 — OCCUPANCY AND CONTACT COUNT vs THE CENSUS BASELINE

| `PX-LO` | I-24-D baseline | `S-Y-ONLY` | `S-Z-ONLY` | `S-K-ONLY` | **`ALL`** |
|---|---:|---:|---:|---:|---:|
| mean ring occupancy | **0.23404** | 0.22330 | **0.26596** | 0.18349 | **0.17857** |
| max occupancy | 1 | 1 | 1 | 2 | **2** |
| kills | 4 | 5 | 4 | 5 | 5 |
| realised straightness | 0.2229 | 0.2231 | 0.2229 | 0.1228 | **0.1107** |
| `R_kill_ring` | 0.39096 | — | — | — | **0.43750** |

| `PX-HI` | I-24-D baseline | `S-Z-ONLY` | `S-YZ` | **`ALL`** |
|---|---:|---:|---:|---:|
| mean ring occupancy | 0.33632 | **0.43284** | 0.37717 | 0.31667 |
| max occupancy | 2 | **3** | 3 | 2 |

**Referent (Lap R, bracket NOT ruled): 3.2423 – 3.4251, median 3.** The record cell sits **~18×
below** it. `S-Z-ONLY` is the only limb that moves occupancy in the right direction on both arms,
and it moves it by **+14 % / +29 %**, not by the order of magnitude the gap needs.

---

## 3 — ⚑ THE FALSIFIER'S VERDICT, AND WHAT IT RESTS ON

**KINEMATIC or STRUCTURAL? — STRUCTURAL.**

The reading is stronger than the single number because the adjudication was made **before any code
existed**, from my own I-7 `ring_joint` emission (math note § 5.1, re-derived from the pinned I-7
bytes at run time so it is checkable):

| | I-7 `cluster_defon` | I-7 `camp_defoff` |
|---|---:|---:|
| **max ring occupancy** | **19** | **20** |
| arc-capacity sum at max ring | 1.2739 (**> 1 = geometrically impossible**) | 1.2860 |
| median radius of ring occupants | 0.600 m | 0.520 m |
| **ring saturates at** | **12.4 bodies** | **14.4 bodies** |

**The arc-capacity hypothesis is REFUTED, not merely disfavoured.** This sim has already put 19 and
20 bodies inside the 2.400 m ring, on two different player policies, and its own instrument flagged
the packing as impossible rather than as full. `E-4` HELD live on this fold too: `arc < 1.0` at
every tick with `n_ring ≤ 3`, on **every** limb. With I-24-D's `BLOCKED = 0`, nothing anywhere
refuses a body entry.

So the ring is not capacity-limited, the player's kinematics now match the referent's measured
straightness to within the referent's own spread, and occupancy **still** does not rise. **What
serialises arrivals is upstream of both.** `NAMED-Z-3` (the engine's 7°-half-angle gather vs the
sim's 360° disc) cannot be it — the sim is the *more* permissive shape.

⚑ **AND THE SEED ENSEMBLE IS THE CAVEAT THAT TRAVELS WITH THE VERDICT.** `E-7`'s *verdict* is
invariant — `F-I24` fires on **5/5** declared seeds — but the *numbers* are not:

| salt | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| mean occupancy | 0.17857 | **0.44178** | 0.14433 | 0.36620 | 0.14151 |
| max occupancy | 2 | **4** | 1 | 3 | 2 |
| like-for-like | 9.14 s | **115.67 s** | 7.92 s | 52.16 s | 8.65 s |
| death wave | 151 | **156** | 151 | 153 | 151 |

**A single-seed record cell is not representative of this policy.** The full ensemble is published;
**no seed is selected**, and the record cell remains salt 0 because that is what the math note
declared.

---

## 4 — THE THREE AMENDMENTS, EACH ON ITS OWN

### 4.1 (a) THE LAP Y ARMOUR OPERAND — landed, direction as decoded

`sumProtectionDV(s) = A_s + 992.16`. **Imported by IDENTITY, never by rendering.** The closure that
makes the transcription checkable: this module's derived operands reproduce Lap Y's own grid values
**read from `pm4y_armour_operand.json`'s bytes** —
`A1 = 2472.87456` EXACT · `C1 = 3465.03456` EXACT · `C2 = 3465.03456` EXACT · `|C1 − C2| = 0.0`.

**`E-1` HELD:** applied physical **falls** on **6/6** folded cells (e.g. `S-Y-ONLY · PX-HI`
198,441.0 vs 236,425.5 under the incumbent operand), on boards where 46/50 and 12/13 physical rows
sit on the `DGP` branch. **The direction is a consequence of the decode, not a reason for it.**

### 4.2 (b) THE RING-PREDICATE REPAIR — `D-I24D-1` DISCHARGED ON DECODE AUTHORITY

**The representation the sim adopts, published with Lap Z's Δ table and my basis:**

```
in_ring(b, p)  ⟺  (bx−px)² + (by−py)²  ≤  fl32(r32²) = 5.7600002288818359375   (hex ec51b840)
equivalent boundary radius = 2.4000000476837156
```

| candidate | Δ vs the engine's tested boundary |
|---|---:|
| the sim's incumbent `2.4` | **−4.768372E-8 m** |
| the run's published `2.4000000953674316` (the **stored operand**) | **+4.768372E-8 m** |
| **adopted** | **0** |

**THE BASIS IS NOT "BECAUSE GRIM DAWN SQUARES IT"** — Lap Z DO-NOT 2 forbids that non-reason and
fork (b) is provably inert at double precision. The basis is **representability**: `fl32(r32²)` is
exactly representable in binary64 and its root is not (`math.sqrt(T)**2 != T`, verified), so the
squared form carries the engine's float32 rounding **deliberately** and adds none of its own, while
the rooted form would add a rounding the engine never performs. `S-Z-ROOTED` ran and is **INERT**
on this board — reported, not assumed.

**No fresh literal enters the fold.** `kc2/ring.py` reconstructs `r32` from Lap Z's published bit
pattern `9a991940` with `struct` and asserts the round-trip against `ec51b840` read out of
`pm4z_operand.json`. I-23's literal is **corrected in place, not deleted**, renamed
`MELEE_TARGET_DISTANCE_STORED_OPERAND_M` with `D-I24D-1`'s travel path in its comment.

⚑ **SEMANTIC SHIFT, NAMED (Discipline #12):** the sim's **two** ring predicates become **one**.
`P-INST` (`hypot ≤ D`) and `P-SEEK` (`d² ≤ D²`) — which I-24-D § 6 measured disagreeing on 1/5
ticks — both become `d² ≤ T`. That changes what *"in the ring"* MEANS. `E-2`'s fork retires as a
side-effect.

⚑ **NO BIT-IDENTITY IS CLAIMED** (Lap Z DO-NOT 3): the threshold side is exact, the distance side
is not — the engine accumulates float32 per axis from a **box**-clamped delta (`NAMED-Z-1`), which
this fold does **not** propagate and which changed **no body geometry** (DO-NOT 4).

⚑ **THE HALT RADIUS DID NOT MOVE, AND THE REASON IS DECODE SCOPE.** Lap Z decoded the **gather**;
the halt consumer is `UNREACHED-Z-1`. `S-Z-HALT-R32` ran anyway — see `E-8` / `E-8b` in § 6.

**`E-2` FAILED.** I-24-D § 10's arithmetic predicted `0.234 → ~0.372`; the measurement is
**0.26596**. My `E-9`-derived estimate over-predicted by ~40 %, and saying so is the point of
having registered a band.

### 4.3 (c) THE PLAYER-KINEMATICS FOLD — the honest negative

**`K-MILL`: episodic straight legs inside a tethered disc, specular reflection at the tether.**
Shape **DECLARED** in the math note's zero-grade commit, with four alternatives named — `K-CRW`
(ran as `S-K-CRW`), `K-ORBIT` (rejected, 2 unpinned parameters), `K-SEEK-MILL` (rejected, 1
unpinned), `K-REPLAY` (**UNAVAILABLE** — Lap U `B-4` declares the integrated trajectory not used).

**The basis for `K-MILL` over `K-CRW` is a MEASUREMENT, not a grade:** at the sim's `dt = 4/49 s`,
matching the referent's wave-grain straightness with a per-tick heading walk requires **negative**
mean-cosine on 7 of 10 waves (w159: `c = −0.512`, ~12 reversals/second), which contradicts Lap R
§ 4.3's **86 sustained episodes** (median 1.26 s, longest 8.68 s). Every `K-MILL` parameter is a
Lap U / Lap R measurement carrying a **provenance digest**, and the derivations reproduce Lap R's
published values exactly (86 episodes · 143.8664 s moving · median leg 1.2583 s · longest leg
8.6833 s · longest stationary gap **1.7333 s** against the published 1.73, asserted as a positive
control that HALTS on disagreement).

**`E-6` HELD**: realised wave-grain straightness **0.1107** (`PX-LO`) / **0.0681** (`PX-HI`),
inside the declared [0.030, 0.130] band, against the referent's 0.060 median. **The fold did what
it was built to do.** Occupancy went down anyway.

**`E-5` FAILED — against my own interest, in the helpful direction.** I predicted a milling
board-blind player would kill *less*; `R_kill_ring` rose **0.39096 → 0.43750**.

---

## 5 — ⚑ `D-I24-1` — MY OWN DEFECT, AND IT NARROWED THE COMMISSION

Disclosed in the math note (`0cfe660c`, § 4.1) **before any I-24 code existed**.

My I-24-D landing § 3 published *"the sim's player walks in a straight line at half again the
referent's speed"* — 5.6719 m/s against Lap U's 3.1–3.8. `R-PM4-65 part 2` carried it forward as
*"1.5× the referent's speed."* **Both quantities are called speed and they are not the same
quantity.** The sim's 5.6719 is `plo.measured_speed(PX-LO)` — **Lap R's moving-episode path
integral, already a measurement of the referent's speed while moving, folded at I-18 limb (a)**.
Lap U's `v̄` is **path ÷ span over ALL frames**.

| comparison | sim | referent | ratio |
|---|---:|---:|---:|
| all-frames mean | 4.2082 | 2.833 – 3.769 | **1.26×** |
| while moving | 5.6719 | 3.781 – 5.754 | **1.22×, INSIDE the range** |

**CONSEQUENCE:** the player's **speed is not the kinematic gap and was not touched by this fold**.
Amendment (c) is a **heading + duty-cycle** fold. **NOT REPAIRED BY REWRITING** — the I-24-D
landing's table is unedited and the correction is published beside it, as `D-I23-3`'s two clauses
were. **The conductor's `R-PM4-65 part 2` row needs the correction; that is reported, not patched.**

---

## 6 — PRE-REGISTERED EXPECTATIONS, GRADED HONESTLY

| id | claim | grade |
|---|---|---|
| `E-1` | (a) applied physical falls on ≥ 90 % of rows | ⚑ **HELD — 6/6 cells** |
| `E-2` | (b) alone moves occupancy into [0.34, 0.40] | ⚑ **FAILED — 0.26596** |
| **`E-3` (`F-I24`)** | matched kinematics raise occupancy ≥ 2× and max > 2 | ⚑ **FAILED → STRUCTURAL. REPORTED, NOT PATCHED** |
| `E-4` | arc never binds at `n_ring ≤ 3` | ⚑ **HELD on every limb** |
| `E-5` | ⚑ *against my own interest* — `K-MILL` makes kills worse | ⚑ **FAILED — 0.391 → 0.4375** |
| `E-6` | realised straightness in [0.030, 0.130] | ⚑ **HELD — 0.1107** |
| `E-7` | `E-3`'s verdict invariant across 5 seeds | ⚑ **HELD (5/5) — but the NUMBERS vary 3×; caveat travels** |
| `E-8` | `S-Z-HALT-R32` collapses occupancy vs `S-Z-ONLY` | graded **AS REGISTERED** (0.17857 vs 0.26596) — **and see `D-I24-3`** |
| **`E-8b`** | the CLEAN isolation: `S-Z-HALT-R32` vs `ALL` | mean occupancy **IDENTICAL (0.17857)**, surface digests **DIFFER** ⇒ the halt fork is **board-visible but occupancy-inert**, i.e. **UNTESTED at the knife edge**, exactly the reading fixed in addendum #2 *before* the number existed |
| `E-9` | ⚑ *against the commission's frame* — `T4b(c)` stays UNARMED | ⚑ **HELD — no cell reached 160** |
| `E-10` | the fold does not move `PX-HI`'s death wave | ⚑ **FAILED — 152 → 151** |

**Mechanical pins:** `P.1` `law_3.moved == {}` on **63** witnesses ✅ · `P.2` frozen **20/20** hard
gate ✅ · `P.3` FOLD-OFF byte-identical, exclusion scope **∅** ✅ · `P.4` determinism ×2 on **three**
legs EXACT ✅ · `P.5` all inputs re-hashed EXACT, HALT armed ✅ · `P.6` wall **19/19 GREEN**,
`keys_asserted` per row ✅ · `P.7` ring-literal AST guard, **site-exact** ✅ · `P.8` Lap Y closure
from Lap Y's own bytes ✅ · `P.9` sheet 3,557 used **0** times ✅ · `P.10` kinematics RNG
off-stream, AST ✅ · `P.11` smoke unchanged ✅ · `P.12` superlatives vs prior artifacts ✅.

---

## 7 — NON-PERTURBATION AND THE WALL

| leg | surface | knot |
|---|---|---|
| **N-1** fold-off | `279460447b519d4912b52176179b645f637fe945e665831c2429f242e897a299` | `4bb04cab65fd5ba1852de89a14e5b9223ad1a1eaa1df466d09816464af4320c8` |
| **N-2** fold-on (`ALL`) | `217f682492847e3a365945c52785573b5871a0c8e03150dc94d19a5a644d1d20` | `d0d818c4211613db012d00e2fa3e173d7cd0b925a3ca22eb896f7925b7531c72` |
| **N-3** fold-on, **real second execution** | **identical** | **identical** |

N-1's knot digest is **byte-identical to I-24-D's `PX-LO` knot** (`4bb04cab…4320c8`) — the fold-off
path is the census cell, proven rather than promised. `⚑ vs_I23_replication` MATCHES: l4l
**7.673469387755103**, death wave **151**.

**`D-I24D-2`'s lesson EXECUTED, not cited:** four mutable objects ride factories (`DefenceField`,
`IntakeFold`, `VectorFold`, `KinematicsFold`) and a **three-way differencing probe** asserts one
digest across three independent constructions of the same configuration. HOLDS.

**Law 3:** `moved == {}` on **63** witnesses, **0** kinematics witnesses without a provenance
digest. The tripwire distinguishes kinematics-parameters-from-Lap-U/R from fitting-toward-T-bands
**by provenance digest** — a witness without one is a free constant and wall row 5 goes RED.

**Smoke:** `296 pass / 1 PRE-EXISTING failure` (`test_AC_10_10`, `secondary_streams.py:136`) —
unchanged from I-23 and I-24-D.

---

## 8 — DEFECT TABLE (all mine; both addenda ALONE and BEFORE their repairs)

| id | defect | disposition |
|---|---|---|
| **`D-I24-1`** | my I-24-D landing compared the sim's Lap-R **moving-episode** speed against Lap U's **all-frames** `v̄` — same name, different quantity — and reported "1.5×" | **DISCLOSED in the math note before any code; NOT REPAIRED BY REWRITING.** Corrected 1.22–1.26× published beside the original. It **narrowed amendment (c)** to heading + duty cycle |
| **`D-I24-2`** | my `P.7` ring-literal AST allow-list was written from memory of my own design note and went RED on its own run (two legitimate survivors, not one) | **REPAIRED by STRENGTHENING** (addendum #1 `27d2d1b9`, alone, before the repair) into a **site-exact** `(module, symbol)` allow-list published in the artifact. The failing version would have passed a second unnamed literal anywhere in `intake.py` |
| **`D-I24-3`** | `E-8`'s comparator differs from its subject in **two** limbs, not one | **DECLARED, NOT REWRITTEN** (addendum #2 `732914f8`, alone, before the artifact). `E-8` graded as registered; **`E-8b`** publishes the clean isolation beside it. Nothing re-run, no limb added |
| **`D-CON-6`** | **the conductor's, sixth, THREE clauses** (math note § 1): Lap U's `v̄` is path/span not speed-while-moving; the 1.73 s stationary run is **Lap R's**, not Lap U's; and Lap Y § 11's six numerals are **CEIL-to-1dp RENDERINGS** whose restatement would have injected up to **+0.08 armour per region** | **DISCLOSED, CORRECTED, AND THE WORK DONE** (the `D-CON-4` pattern) |

> ⚑ **TWO OF MY THREE DEFECTS ARE THE SAME FAILURE: a claim about my own artifact, REMEMBERED
> instead of READ** — the allow-list in addendum #1, the limb matrix in addendum #2. `D-I24D-2`
> said *a population is ENUMERATED, not recognised.* Its sibling, earned twice today: **an
> ISOLATION IS READ OFF THE MATRIX, not recalled from the prose that motivated it.**
> **Fifth consecutive iteration in which my own pre-registration caught my own work before a number
> was reported.**

---

## 9 — `UNREACHED`, NAMED AND NOT APPROXIMATED

* **`UNREACHED-I24-1`** — **no lap has decoded a player movement policy.** `K-MILL` matches two
  measured moments and one measured episode structure. The referent's control law is unknown and
  this fold does not claim it.
* **`UNREACHED-I24-2`** — Lap U's `v̄`/`f` pair and Lap R's episode segmentation are different
  instruments at different thresholds; `v̄/f` mixes them. `S-K-LAPR-F` was declared; the primary
  uses Lap U's own pair throughout.
* **`UNREACHED-I24-3`** — the halt fork is an arithmetic prediction about a knife edge, **and it is
  now also UNMEASURED under the record kinematics** (`E-8b`). Whether the engine's box
  (`NAMED-Z-1`) resolves the same knife edge needs its own lap (per-body ABBox extents).
* **Carried:** `UNREACHED-Z-1` · `NAMED-Z-1` · `NAMED-Z-2` · `NAMED-Z-3` · `UNREACHED-Y-1` ·
  `UNREACHED-X-1` (reshaped) · the 17 unexpressed AI states · `T17` · `D-PDEF-2` · `pools_for`
  default.

---

## 10 — DIGESTS (full 64 hex, `R-PM4-55 part 2`)

### 10.1 Emitted

| artifact | sha256 |
|---|---|
| `output/kc2-pm4-i24-findings-20260816_072225.json` | `e7c2f1ba111b3be782d1dca034807c8db56365af7fc71ce6741f0887037d1993` |
| `math/kc2-pm4-i24-fold-2026-08-16.md` | `3860e9e09c0f3e13a26b76c487ea77e6e5c878d07d152ba400b69ebdcfc67bfb` |
| `math/kc2-pm4-i24-fold-ADDENDUM-2026-08-16.md` | `8476b4c65dfd79fc0650432e13a2b9be119880c1f63962127f4d212e72e2221f` |
| `math/kc2-pm4-i24-fold-ADDENDUM-2-2026-08-16.md` | `757d896b892938fc9dd91b1a6e9433d75f0e8ad285359477e314944937ad8f42` |
| `kc2/ring.py` (**NEW**) | `c15110f3e2759640b795b4b6825862b2063f859418cdcf1a1b6d402ca2ccde07` |
| `kc2/kinematics.py` (**NEW**) | `8268735dcd37f10743d5c12957126e6ac543280119eb888cc7a6e52267a32e13` |
| `kc2/intake.py` | `42fd1cc0ac5d96c4d98dd711693663942b824249fb882e2dc72c8ccfd91954d1` |
| `kc2/run.py` | `14f9dd2b339350ee28f1cd471dca12166edc9c6979c36ce8aa5a87425a9032f1` |
| `kc2/engagement.py` | `4df7415f987bc2a2f910de63ab6a289c31ed61d3fc821b96b9e36ff56f4c148c` |
| `kc2/player_locomotion.py` | `cebfac464d75254ca153d0190279f565276dd603e2728012c36520b06f7353bb` |
| `scripts/gamora_kc2_pm4_i24_fold_2026_08_16.py` | `0ff7ba5c7050fe0517bb19a2d8250166083ac34024c5a1021318731a57b54c4f` |

### 10.2 Consulted — re-hashed EXACT from bytes before any fold code ran (HALT armed; none fired)

| input | sha256 |
|---|---|
| Lap Y `pm4y_findings.md` | `fa2ed53a351011d59edfeb9bba0391afc92584c570ca36101a4ad9d85de57f7d` |
| Lap Y `pm4y_armour_operand.json` | `9115996733f971e10457a217bff1928226d3e102720704492026aaee6b5354c5` |
| Lap Y `pm4y_composition_grid.csv` | `cf6d8cee8de8af0f14b802a31cb5f5ce3a497a331e5f9b4dc9a33ae9ee59dbaa` |
| Lap Z `pm4z_findings.md` | `283cf38b25b9c2ad9444fed9e8f1c972b82f80fd0ccfc6258f389b77dd75ee26` |
| Lap Z `pm4z_operand.json` | `6e689f8a3930dca5b132ae250810f7035273d75515db61f383a7f11b967d1802` |
| Lap Z `pm4z_boundary_arithmetic.csv` | `3a9cac943d61ee42d51041fc6ec6ea48443116da2f9042bcfb9acd4e912f3563` |
| Lap U `pm4u_findings.md` | `f1a34cb11c6015d83169bd2ebbb7fd3ee7ba15bbc20622756f37fbb75fbec6ce` |
| Lap U `pm4u_ramp_analysis.json` | `bd26555e38ebd570fb3f04da36d6a9cea13d4726196c4216f873234720652818` |
| Lap R `pm4r_findings.md` | `c223dfb04653a7e8682d5c1dd42356fc2a8398b06951372445d235a6eff224ea` |
| Lap R `pm4r_movement_episodes.csv` | `dc3173ae53c2a371d9336e95db79c25c4deb04834cebdd4c9318f554d9f576cc` |
| **I-23 findings (the incumbent)** | `0e4084b55f0af955f0b91d809da8e1b3267d6876a1c177a8eba3655c21048368` |
| **I-24-D findings (the census)** | `0e64fe317a46c1ba68dae495c2429e1f3faf794a4fa7f8742853775595a6f0c1` |
| I-7 findings | `d4d0478c94316de53a0a174f31290bb4573938be7afccb9dcab81ad6d2c5ec75` |
| I-7 actor-paths `cluster_defon` | `c8463a22d0116d64a9795ed84e058376a3f27d3fd267d6a50b6f8019bb8266b2` |
| I-7 actor-paths `camp_defoff` | `7adae207aeb5c9c05330c6810b3d8e2af0e5d23379f408eadc76a254bd3591cc` |

Plus Lap X's 14 pins (`intake.verify_substrate`) and Lap R's (`player_locomotion.verify_substrate`)
— **imported, never re-implemented** (`NOTE-9`).

---

## 11 — DO-NOT BLOCKS CARRIED, ENTIRE

Lap V § 7.2 · Lap V-2 § 11.2 · Lap W § 7.2 · Lap X § 12.2 · **Lap Y § 11.6** · **Lap Z § 5** (all
seven clauses). Named because this fold sits closest to them: `2.4000000953674316` is never called
the ring radius; the square is carried **only** to carry the float32 rounding, deliberately; no
bit-identity is claimed; `NAMED-Z-1` changed no body geometry; Lap Z's occupancy-sensitivity
paragraph is context and the occupancy claim is **my measurement**; the shipped tools, decoy
records, constructor defaults and EC-8 searches supply **no number**; `C3` / `C7` /
`UNREACHED-Y-1` are not folded and `UNREACHED-X-1` is not closed by moving a term.

---

## 12 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. **THE RESIDUAL'S TWELFTH NAME IS OWED, AND THE MEASUREMENT NAMES THE SEAM.** Occupancy is
   invariant to mitigation (I-23), to the roster (I-22), to arrival (I-19/20), to pursuit speed
   (I-21), to the ring predicate (0.234 → 0.266) **and now to the player's own kinematics**
   (0.266 → 0.179), while arc capacity is **refuted** as a limiter and `BLOCKED = 0`. Everything
   the run has folded is downstream of whatever spaces arrivals out. **The next question is not a
   fold; it is where the sim's bodies acquire their arrival ORDER** — the spawn-to-node assignment
   and the per-body march clock, which no lap has yet measured *jointly*.
2. **`S-YZ · PX-HI` IS THE ITERATION'S REAL RESULT AND IT IS NOT THE RECORD CELL.** Amendments
   (a) + (b) alone carry `PX-HI` four waves further (l4l 160.16 s, T2 0.8766). If the conductor
   wants that arm characterised it needs its own cell, not a re-designation of this one.
3. **THE SEED VARIANCE IS A COMMISSIONING FACT, NOT A NUISANCE.** A policy whose like-for-like
   spans 7.9 – 115.7 s across five seeds cannot be graded from one run. Any future stochastic
   policy limb should be commissioned **with an ensemble in its record cell**, not with an
   ensemble as a sensitivity.
4. **`NAMED-Z-3` IS NOT THE SUSPECT AND THE FLAG SHOULD SAY SO.** `R-PM4-66 part 2` flagged the
   14° cone for the case where kinematics raise entry rate and occupancy still under-fills. Entry
   rate did **not** rise, and the sim's 360° disc is the *more* permissive shape either way. The
   flag should stand for a different trigger than the one it was written for.
5. **`R-PM4-65 part 2`'s ROW NEEDS `D-I24-1`'s CORRECTION.** *"1.5× the referent's speed"* is
   1.22–1.26×, and the sim's speed sits inside the referent's own range. The sentence is load
   bearing for how the chapter reads.

---

*End of landing note.*
