# KC2-PM4 · I-8 — landing note: **the solver did not disperse the crowd. It un-collapsed it.**

> **Run:** KC2-PM4 · **Iteration:** I-8, THE CONVERGING SOLVER · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** ruling **R-PM4-18** (charter ledger **L-15**), exercising **R-PM4-15**'s
> pre-authorisation now that both trigger clauses read MET on measurement at I-7.
> **Math note (Discipline #1, written and committed BEFORE the code — commit `c36284a7`, its own
> commit, so the git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i8-converging-solver-2026-08-14.md`
> **Status:** COMPLETE. **No HALT.** Assert wall **18/21** — ⚑ **three REDs, all declared, none
> repaired to green** (§ 4). Determinism ×2 **EXACT (0 differences)** on all three cells, **three
> batons FULL at 67/67**, Law-3 witness `moved: {}`.

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> Unless a different source is named inline, every I-8 quantity is read by key path from
> `reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i8-findings-20260814_013948.json`
> · sha256 **`a7aa1c472371dec5bcd3f3448015626b4c3b0b98e5cf44c7b921080110b3fb5e`**, and every I-7
> quantity from `…/kc2-pm4-i7-findings-20260814_005919.json` · sha256
> **`d4d0478c94316de53a0a174f31290bb4573938be7afccb9dcab81ad6d2c5ec75`** (verified from bytes at
> run time by the driver — a wrong digest HALTs the lap). **There is no unsourced number below.**

---

## 0 — The one-paragraph answer

**The invariant is now enforced, and enforcing it did the opposite of what I predicted.** Worst
penetration on the reference cell falls from **0.9469551055658749 m to 7.477930188404258e-07 m** —
six orders of magnitude — and the pair-instants violating the constraint by more than the substrate
can represent fall from **57,700 to 2**. I predicted, before the run, that spreading the crowd would
take bodies out of reach: fewer near the player, less intake, slower clears, mean HP up. **Every one
of those quantitative predictions is falsified in the same direction, and the mechanism is one
sentence: interpenetrating bodies were HIDING INSIDE ONE ANOTHER.** Converging the solve does not
disperse the crowd — it *un-collapses* it. Mean engage-ring occupancy **rises** 1.1819 → 1.2424
while the maximum **falls** 19 → 17; mean disc occupancy rises 1.734 → 1.820 while its max falls
32 → 27; the player lands **8.8 %** more body-hit rows; intake rises **7.45 %**; and the
like-for-like clear time **falls 4.40 %**, *toward* T2's band, which my pre-registered band did not
allow for at all. **The ring gate stays MISSED at 17 against 10 — which is what I said would happen
and why, with the packing arithmetic, before the run** (§ 6). ⚑ And the error I pre-registered in
§ 7.1 of the math note **fires**: the solver moves bodies **0.739 m per tick against a monster's own
0.327 m travel budget — a ratio of 2.26**. The sim's crowd is now shaped more by depenetration than
by pursuit, and that is this lap's finding for the conductor (§ 12).

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 15 predictions, 21-check wall, layer table) | `simulation/math/kc2-pm4-i8-converging-solver-2026-08-14.md` | **`c36284a7`** |
| 2 | `kc2/geometry.py` — `separate_overlaps_converging`, `worst_penetration`, `separation_tolerance_m`, `ulp32`, `SEPARATION_MAX_SWEEPS` | modified (ADDITIVE; the Jacobi arm untouched) | `b4732d73` |
| 3 | `kc2/run.py` — `separation_solver`, the branch, the keyed-when-active convergence block | modified | `b4732d73` |
| 4 | `export/kc2_run_adapter.py` — `KC2RunSpec.separation_solver` + 3 I-8 specs | modified | `b4732d73` |
| 5 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `b4732d73` |
| 6 | **driver + 21-check wall + determinism + 5 sensitivity cells** | `simulation/scripts/gamora_kc2_pm4_i8_converging_solver_2026_08_14.py` | `b4732d73` |
| 7 | **3 knot supplies + findings** (stamp `20260814_013948`) | `simulation/output/` | `74dbbd8b` |
| 8 | **⚑ 3 BATONS, FULL, 67/67** | `src/reincarnated/output/` | `f33ee59c` |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

| what | sha256 |
|---|---|
| **findings** | `a7aa1c472371dec5bcd3f3448015626b4c3b0b98e5cf44c7b921080110b3fb5e` |
| knots CAMP/DEF-OFF | `eff59f112f5a827556603589e8ef41a19df2e11d86df313b779871a48fef0c0f` |
| knots CLUSTER/DEF-OFF | `cd3fbfabff38272e374129df628b479d90424d2e3ba3a09eca0dfa9c9c2e5141` |
| **knots CLUSTER/DEF-ON** ← reference | `f139161d9bfe446ecb9a08c985dccfd12d39f4b0d4b0749f0271ce1b70a2d56a` |
| **baton** CAMP/DEF-OFF | `a43d576621e1cbef5b97f392c42d02db7fb8041e27855dbfef8b5e1e42e84500` |
| **baton** CLUSTER/DEF-OFF | `8513b23408ff2d0ab492987c95216cbd50d0302d45d47d7daa8f209b376e2f93` |
| **baton** CLUSTER/DEF-ON ← reference | `7d4422fedc26c29a375597b0271c7f642668ce46b43820698fcc722aab10c35e` |
| determinism surface CAMP/DEF-OFF | `0876b9c4846c5f5d1646354604ac3117ceaf61ce2c271f59718ec73cfe06f223` |
| determinism surface CLUSTER/DEF-OFF | `4d97ec3df8a1b2216f3d50bda99bb255d39fb3a1a25ed01936b49d293f775d8d` |
| determinism surface CLUSTER/DEF-ON | `e2723731243ccd35a296e055a44ef3d852d918ca42cf3f713c34db7eb27054db` |

**The I-7 batons these SUPERSEDE** (and which, like every KC2 baton before them, carry
interpenetrating bodies): `ce4c38b1…3c1a` / `d2890086…b2c3` / `8b12244f…2c8a`.

### 1.1 — The layer table, graded against what the math note § 5 declared BEFORE the run

| layer | arm | declared | measured |
|---|---|---|---|
| **1a** | I-7 config, `separation_solver="jacobi4"` (the DEFAULT) | byte-EXACT vs I-7 | **EXACT ×3** — `d6d71a0a…8487f` / `2ed7286e…8afd` / `5cb321b9…5fde8` |
| **1b** | pre-I-6 arm, jacobi4 | byte-EXACT vs I-5, **three folds back** | **EXACT ×3** — `5f616040…7fa7` / `0ad5b297…2605` / `95a34b2e…c7a4` |
| **1c** | default arm (no `separation_solver` argument reaches `simulate_wave` at all) | EXACT | **EXACT** — `5cb321b9…5fde8` |
| **⚑ 1d** | the three I-8 cells | **DIVERGENT BY CONSTRUCTION** | divergent, as declared; new references pinned above |

**Check 1 is what makes "the delta is exactly the solver" a MEASUREMENT.** Keeping the legacy
solver as the DEFAULT cost nothing and bought a byte-identity baseline on an iteration the ruling
said could not have one.

---

## 2 — THE SOLVER, AND THE TWO NUMBERS IT CARRIES

Sequential projection (Gauss–Seidel): each violated pair is projected onto its own constraint set
exactly and applied **immediately**, so later pairs in the same sweep see the update. Sweeps repeat
until the board's worst residual penetration is `≤ τ`. **The contact physics is unchanged, character
for character** — symmetric depenetration along the line of centres, the player `fixed`, the same
degenerate-direction fallback, the same `_TOL` skip. Only the termination rule changed.

### 2.1 — τ, derived from the geometry substrate. Zero free parameters.

```
r_max          = max(radii_of_record())          = 2.0 m   (MEASURED, 297 records)
ulp32(2.0)     = 2^(1−23)                        = 2^−22 = 2.384185791015625e−07
τ = 2·ulp32(r_max)                               = 2^−21 = 4.76837158203125e−07 m
```

The constraint's right-hand side `r_i + r_j` is a sum of two **float32** measured radii —
`pm4_body_radii.csv` emits the exact float64 expansion of a float32 DB scalar
(`0.20000000298023224`, `1.100000023841858`), and R-PM4-7's `radius_m` column is that scalar
unrounded (IS-F1). **A penetration below `ulp32(r_i) + ulp32(r_j)` is a quantity the substrate does
not carry.** Recomputed from the loaded table at run time and asserted (check 3); **never a
literal**. Headroom over float64 position noise at 30 m: **8.1 orders of magnitude** — the tolerance
is reachable by the arithmetic that has to reach it.

### 2.2 — The 256-sweep cap is a NON-TERMINATION GUARD, and the derivation I rejected is on the record

`SEPARATION_MAX_SWEEPS = 256 = 2⁸`, 1.92× the worst count in a deliberately over-packed synthetic
probe (133 sweeps). ⚑ **The natural-looking derivation is on the record as MEASURED WRONG:** "a
contact chain of `N` bodies needs at most `N` sweeps, so cap = `N_live`" hit the cap on **288 of 300
probe trials**, because an over-packed pile must *expand*, and expansion advances by roughly one
penetration depth per sweep, not by one chain edge. A plausible bound the data refutes is exactly
the kind of thing that otherwise survives into a landing note as reasoning.

---

## 3 — ⚑ CONVERGENCE: THE TABLE R-PM4-18 ASKED FOR

**Reference cell CLUSTER/DEF-ON, at the instant the weapon is evaluated, 6,321 censused ticks.**

| | **I-7 · jacobi4** | **I-8 · sequential_projection** |
|---|---:|---:|
| overlapping pairs / tick handed **to** the solver (`presolve`) | 8.996883713301624 | **9.348995412118336** |
| overlapping pairs / tick **at observation** (1e-9 basis) | **6.184024930293587** | **2.9666192058218637** |
| reduction per solve | 31.26 % | **68.27 %** |
| worst penetration `presolve` | 1.4823596586100147 m | 1.4823596586100147 m *(identical — see § 9 P.2)* |
| **worst penetration at observation** | **0.9469551055658749 m** | **7.477930188404258e-07 m** |
| pair-instants **above τ**, presolve → postsolve | *(not instrumented)* | **57,700 → 2** |
| pair-instants where the **player's own body** overlaps a monster | 605 | 563 |

> ### ⚑ THE INVARIANT IS ENFORCED. THE 1e-9 PAIR COUNT IS NOW MEASURING SOMETHING ELSE.
> A converged solve leaves contacting bodies resting at **exactly** `r_i + r_j`, which registers as
> "overlapping" at a 1e-9 threshold whenever float rounding lands a hair inside. **Every one of the
> 563 player-pairs sits at a penetration ≤ 7.478e-07 m** — that is the whole ladder's worst, so it
> bounds every pair on every tick — against I-7's 605, which sat on a board whose worst was
> **0.947 m**. **After I-8, "overlapping at 1e-9" means CONTACT, not interpenetration.** Filed in
> `simulation/MIGRATION.md` § 1 as the one thing a consumer must change its mind about.

### 3.1 — Sweeps to converge

| cell | ticks solved | already admissible | converged | **cap-hits** | mean | median | p90 | p99 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CAMP/DEF-OFF | 23,771 | 20,684 | 23,761 | **10** | 2.73 | 1 | 3 | 60 | 256 |
| CLUSTER/DEF-OFF | 6,282 | 2,651 | 6,280 | **2** | 9.30 | 1 | 20 | 142 | 256 |
| **CLUSTER/DEF-ON** | 6,321 | 2,889 | 6,319 | **2** | 9.28 | 1 | 21 | 151 | 256 |

**Most ticks need nothing** (2,889 of 6,321 begin already admissible) **and the median solve is one
sweep** — but the tail is heavy, and 2 ticks reach the guard. That is D-I8-2 (§ 4.1).

### 3.2 — ⚑ S-3 measured: the displacement cost, priced not asserted

| cell | separation travel I-7 → I-8 | per tick | monster travel budget / tick | **ratio** | max single-body displacement |
|---|---|---:|---:|---:|---:|
| CAMP/DEF-OFF | 3,924.88 → 4,930.62 m (×1.256) | 0.2074 m | 0.3265 m | 0.64 | 0.7886 m |
| CLUSTER/DEF-OFF | 1,729.73 → 4,487.84 m (**×2.594**) | 0.7144 m | 0.3265 m | **2.19** | **1.0597 m** |
| **CLUSTER/DEF-ON** | 3,496.27 → 4,671.72 m (×1.336) | 0.7391 m | 0.3265 m | **2.26** | 0.9021 m |

> ### ⚑ THE PRE-REGISTERED ERROR CHECK FIRES, AND I SAID BEFORE THE RUN THAT I WOULD REPORT IT EITHER WAY.
> Math note § 7.1: *"the solver's consequence is that it becomes a crowd-dispersal force with no
> speed limit… I will measure separation travel against locomotion travel, as a ratio, and report
> it whether or not it embarrasses this iteration."* **On both seeking cells the depenetration moves
> bodies more than twice as far per tick as their own pursuit budget.** The invariant is now true;
> the transport that makes it true is larger than the transport the locomotion model authorises.
> This is the item I take to the conductor (§ 12.1).

---

## 4 — ⚑ THREE RED CHECKS, DECLARED, NONE REPAIRED TO GREEN

The math note § 8 fixed the response **before** the run: *"report as a defect, do not raise the cap
to make it green. Raising a cap because a residual is inconvenient is the Law-3 shape one level
down."* Wall reads **18/21**.

### 4.1 — ⚑ D-I8-2 — check 8 RED: the solve reaches its guard on a handful of ticks

**2 / 6,321 (reference) · 2 / 6,282 (CLUSTER/DEF-OFF) · 10 / 23,771 (CAMP/DEF-OFF)**, counted as
`ticks_hit_cap` on the wire. Those ticks are **not converged** and I am not going to call them
converged. **The residual there is bounded by the cell's own worst penetration: 7.478e-07 m
(reference, 1.57 τ) and 8.960e-06 m (CAMP/DEF-OFF, 18.8 τ).** The failure is real and it is
sub-micrometre. **The cap was not raised.**

### 4.2 — check 7 RED: pairs above tolerance are 2 / 8 / 182, not 0

The same ticks, seen from the other side. Against **57,700** above-tolerance pair-instants handed to
the solver on the reference cell, **2** survive it — **99.9965 % removed**. P.1 said zero. It is not
zero, and the number is on the page.

### 4.3 — check 10 RED, and ⚑ ITS PREDICATE IS MIS-SPECIFIED — SAID PLAINLY, LEFT RED

Check 10 asks `observed_pairs_with_player == 0` on a census whose threshold is `1e-9`. After a
converged solve that census counts **contacts**, not interpenetrations (§ 3). The check is therefore
asking a question that cannot be answered "yes" by a correct solver, and it went RED at 563.

⚑ **I have deliberately NOT repaired the predicate.** I-7's § 9.2 repaired check 10's predicate
after seeing the data and said so in those words; the stronger move available here is to leave the
measured RED standing and put the correctly-specified quantity beside it. **The correctly-specified
answer is derivable from numbers already on the wire and needs no new code:** the whole ladder's
worst penetration is 7.478e-07 m and the whole ladder's above-tolerance pair count is 2, so **at
least 561 of the 563 player-pairs are contacts within tolerance, and at most 2 exceed it.** At I-7
the corresponding board carried player-inside-monster overlaps up to **0.947 m**.

### 4.4 — D-I8-1, self-caught by check 2 before anything else ran

I shortened the ehp-band-exhaustion detail string from `"band-B lookup at …"` to `"band lookup at
…"` while writing the driver. `_surface()` digests the terminal dict, so check 2 went **RED on
`camp_defoff`** — **the wall caught a prose edit masquerading as nothing.** Restored verbatim; the
comment in the driver now says why the string is load-bearing.

### 4.5 — D-I8-3 — `ManaBurnDrain` has no measured resistance row, and I did NOT give it one

Surfaced by the `S-TOL-LOOSE` sensitivity cell taking a trajectory no cell of record took:
`mitigate()` raised *"damage family 'ManaBurnDrain' has no measured resistance on the Lap-A sheet.
GL-12: name it in `RESIST_PCT` or in `NON_HEALTH_KINDS` — do not guess a resistance."* The cell
halted at wave 165. **Same class as I-7's D-I7-2/D-I7-3, and NOT closed here:** this is an
**energy**-drain family, and mapping an energy resistance onto a health path is precisely the
invention I-7 already declined for `SlowManaLeach`. **Routed, not patched** (§ 12.3). ⚑ It is a live
risk for the cells of record on any future trajectory, which is why it is named now rather than when
it halts one.

---

## 5 — THE THREE CELLS

| cell | terminal | t (s) | mean HP | min HP (EOT / **intra**) | exc<0.70 (EOT / **intra**) | ring max | intake |
|---|---|---:|---:|---:|---:|---:|---:|
| CAMP/DEF-OFF | `arena_tier_exhausted`@171 | 1,940.49 | 0.9942 | 0.2926 / **0.1227** | 18 / **33** | 15 | 2,014,441 |
| **CLUSTER/DEF-OFF** | `arena_tier_exhausted`@171 | 512.82 | 0.9748 | 0.3500 / **0.3344** | 22 / **30** | 20 | 2,047,217 |
| **CLUSTER/DEF-ON** ← reference | `arena_tier_exhausted`@171 | 516.00 | **0.9866** | 0.4875 / **0.4568** | 12 / **22** | 17 | 1,863,382 |

> ### ⚑ THE DEATH FROM I-7 IS GONE. CLUSTER/DEF-OFF NOW CLEARS THE WHOLE LADDER.
> At I-7 it died on wave 160, 7.918 s in, killed by `w160_pet0012` — the first death in seven
> iterations, and it landed on the reference wave. Under a converged solve it survives to the arena
> wall at 171. **P.7b called this at 55 % confidence, i.e. barely better than a coin, and it is the
> single most consequential outcome movement in the lap: T1's one piece of evidence that the sim can
> kill a player at the right wave was produced on a board where bodies interpenetrated.**

### 5.1 — The reference cell against I-7, term by term

| observable | I-7 | **I-8** | ratio |
|---|---:|---:|---:|
| attack opportunities | 6,477 | **6,876** | ×1.0616 |
| hits / misses | 1,478 / 454 | 1,532 / 472 | ×1.0365 / ×1.0396 |
| `damage_total` | 1,734,231.60 | **1,863,381.61** | **×1.0745** |
| counterplay `applied` | 1,049,844.13 | 1,153,090.76 | ×1.0983 |
| counterplay `absorbed` | 289,275.97 | 297,021.01 | ×1.0268 |
| **body-hit rows the player landed** | 10,574 | **11,505** | **×1.0880** |
| mean engage-ring occupancy | 1.1818927341315402 | **1.2423667141275114** | **×1.0512** |
| **max** engage-ring occupancy | **19** | **17** | ×0.895 |
| mean disc occupancy | 1.7342955551910775 | **1.820123398196488** | ×1.0495 |
| **max** disc occupancy | **32** | **27** | ×0.844 |
| mean HP (end-of-tick) | 0.985925199797722 | **0.9866156678432797** | +0.00069 |
| min HP (end-of-tick) | 0.451635 | **0.487469** | ⚑ higher |
| K-1 / K-2 / K-3 / K-4 / K-5 / K-6 | 2 / 111 / **1** / 2 / 67 / 21 | 2 / 107 / **0** / 2 / 69 / 22 | ⚑ K-3 stops firing |

> ### ⚑ THE MECHANISM, IN ONE ROW-PAIR: **MEANS UP, MAXIMA DOWN.**
> Ring occupancy mean **+5.1 %**, max **−10.5 %**. Disc occupancy mean **+4.9 %**, max **−15.6 %**.
> Interpenetrating bodies were **hiding inside one another** — many bodies at nearly the same point
> registered as a small number of distinct occupants at typical range while stacking into
> geometrically impossible extremes at the peak. Converging the solve gives every body its own
> ground: **more distinct bodies at typical range, fewer at the extreme.** The player's weapon finds
> **8.8 %** more targets; the monsters find **6.2 %** more attack opportunities; and waves clear
> **faster**, not slower. **K-3 Menhir's Will — the deepest circuit-breaker, which woke for the
> first time in the run at I-6 — stops firing, because min HP rose to 0.4875.**

---

## 6 — ⚑ THE RING GATE: MISSED AT 17 AGAINST 10, EXACTLY AS PRE-REGISTERED

The gate this iteration was fired at. **The math note predicted, with its arithmetic, that closing
the overlap would NOT close this gate**, and it did not.

| gate | I-7 | **I-8** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring median | 0 | **0** | 1 | MISSED |
| **MG-2** ring p90 | 4 | **4** | 3 | MISSED |
| **MG-3** ring **max** | 19 | **17** | **10** (R150) | **MISSED**, ratio 1.7× (was 1.9×) |
| **MG-4** moving fraction | 0.8365970051012013 | **0.8411363275670528** | 0.883 | MISSED |
| **MG-6** longest stationary | 1.3877551020408165 s | **1.3877551020408165 s** | ≤ 1.40 s | **MET**, identical to the digit |
| **MG-7** dash rate | 5.351766513056837 s / 93 | **5.375 s / 96** | 5.3235 s | **MET** |

**The derivation that predicted it** (math note § 7, P.5). The ring census counts bodies whose
centre lies within a **DISC** of radius 2.4 m, not on a shell. The packing bound
`n ≤ η_hex·((2.4 + r)² − 0.32²)/r²` with `η_hex = π/(2√3)` gives capacity **55.2** at the measured
ring-median radius 0.35 m and **15.8** even at the ring-max radius 0.75 m. **A ring of 19 small
bodies is geometrically FEASIBLE without overlap.** Ring occupancy is limited by how many monsters
are alive and pursuing, not by packing — so removing the overlap could only shave the extreme, and it
shaved it from 19 to 17.

### 6.1 — ⚑ C-I8-1: a correction to my own I-7 clause-2 framing, raised BEFORE this run

Pre-registered in the math note § 7 P.5b: the `ARC = Σ 2·asin(r_i/d)/2π` statistic treats every ring
occupant as sitting at exactly `d = 2.4 m` — **a shell bound applied to a disc population**. It
therefore *over-states* impossibility. **The clause-2 verdict does not rest on it** — it rests on the
**26 measured interpenetrating pairs** at the same instant, a direct measurement that stands
unaltered, and which I-8 has now removed. But the ARC limb over-stated its case, the limb is mine,
and I named it before the solver's numbers made it obvious. **Routed to the conductor (§ 12.2).**

---

## 7 — TARGET STATE T1–T4 (reference cell)

| band | target | measured | verdict |
|---|---|---|---|
| **T1** survival depth | death on wave **160** ({159–161} near-miss) | **no death; terminal wave 170** (`arena_tier_exhausted` @171) | **MISSED** — ⚑ and CLUSTER/DEF-OFF's I-7 death at 160 is now gone too (§ 5) |
| **T2** duration | 186 s ± 15 % (158.1–213.9) | **like-for-like 151–160 = 223.265306122449 s** (+20.0 %); whole ladder 516.00 s | **MISSED** — ⚑ but **improved**: I-7 was 233.551 s (+25.6 %) |
| **T3** pacing | per-wave clears correlate with 14/17/29 s | median ratio **1.1479591836734695**, pearson r **0.0042** | **NEAR/MISSED** — ratio improved from 1.1646, correlation degraded from 0.1425 |
| **T4a** sustain-through-throughput | alive while clearing | mean HP 0.9866 over 6,321 ticks | **MET** |
| **T4b** fought terminal wave, ~6.55 s collapse | DoT-involved collapse | terminal wave 170 cleared in **18.12 s**, DoT **0.018 %** of intake | **MISSED** |

### 7.1 — HP observables against the video

| | sim I-7 (EOT) | **sim I-8 (EOT)** | **sim I-8 (intra)** | video |
|---|---:|---:|---:|---:|
| mean HP | 0.9859 | **0.9866** | **0.9770** | **0.932** |
| excursions < 0.70 | 13 | **12** | **22** | **7** |
| min / floor | 0.4516 | **0.4875** | **0.4568** | 0.28 |

⚑ **The divergence widened on the depth axis.** I-7's true intra-tick floor was **0.3273**, within
touching distance of the video's 0.28; I-8's is **0.4568**. The player is now *further* from ever
dying than the fold that added lethality left him. **Both bases are reported and neither is "the"
answer** — the video is frame-sampled, `H_end` is post-heal (an upper reading), `H_floor` is the
envelope minimum (a lower reading), and the true statistic lies between them.

---

## 8 — SENSITIVITY CELLS (diagnostics, NOT matrix cells)

| cell | τ | solver | terminal | mean HP | l4l 151–160 | ring max | pairs/tick | worst pen | above-τ | cap-hits |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| **reference** | τ | seq-proj | @171 | 0.986616 | 223.2653 | 17 | 2.9666 | 7.478e−07 | 2 | 2 |
| **S-TOL-TIGHT** | **τ/16** | seq-proj | @171 | 0.985613 | 225.4694 | 18 | 2.0457 | **5.083e−06** | **221** | **12** |
| **S-TOL-LOOSE** | **16 τ** | seq-proj | **@165 (D-I8-3)** | 0.982762 | 226.7755 | 17 | 2.4857 | 7.626e−06 | **0** | **0** |
| **S-JACOBI** | — | jacobi4 | @171 | 0.985925 | **233.5510** | **19** | **6.1840** | **9.470e−01** | — | — |
| S-CONV | τ | seq-proj | @171 | 0.986531 | 223.2653 | 17 | 2.9666 | 7.478e−07 | 2 | 2 |
| S-PCL | τ | seq-proj | @171 | 0.984570 | 223.2653 | 17 | 2.9666 | 7.478e−07 | 2 | 2 |

> ### ⚑ S-JACOBI AT I-8 HEAD REPRODUCES I-7'S CELL OF RECORD EXACTLY — 233.5510 s, mean HP 0.985925, ring max 19, 6.1840 pairs/tick. Both arms of the before/after table come from ONE run.

> ### ⚑ AND THE TOLERANCE EXHIBIT SAYS SOMETHING I DID NOT EXPECT: **TIGHTENING τ MAKES THE ENFORCED INVARIANT WORSE.**
> At **τ/16** the solve fails to converge on **12** ticks instead of 2, leaves **221**
> above-tolerance pair-instants instead of 2, and its worst penetration is **5.083e−06 m — seven
> times deeper than the reference cell's**. At **16 τ** it converges on **every** tick, 0 cap-hits,
> 0 above-tolerance pairs. **A tolerance pushed below what the solver can reach within its guard
> converts a converged solve into a non-converged one, and the residual then floats free.** This is
> the empirical case for deriving τ from the substrate rather than driving it toward zero — and it is
> a case I did not have before the run.
>
> **On outcomes the 256× tolerance range moves like-for-like across 223.27 / 225.47 / 226.78 s
> (1.6 % spread) and mean HP across 0.98276 / 0.98561 / 0.98662.** ⚑ **Non-zero — so I will not
> claim the tolerance is outcome-neutral.** The honest reading is that the fight is chaotically
> sensitive to any perturbation of body positions (S-TOL-TIGHT and the reference differ by ~30 nm on
> the first tick and by 2.2 s over ten waves), **not** that the tolerance is a dial with outcome
> content. Both bracket cells sit on the *same side* of every gate and every T-band verdict.

**Law-3 note, unchanged from I-6 and I-7.** S-PCL moves an observable and is **not adopted**;
its composition is UNDECODABLE-FROM-SUBSTRATE and not scaling is the lower reading.

---

## 9 — PRE-REGISTERED PREDICTIONS vs OUTCOME — **six confirmed, six split, four falsified**

Falsified predictions keep their original wording (the run's standing practice).

| # | prediction | outcome |
|---|---|---|
| **P.1** | post-solve overlapping pairs → **exactly 0.000**; worst ≤ τ; **cap-hits = 0** | **⚑ FALSIFIED ON ALL THREE LIMBS AS WORDED.** 2.9666 pairs/tick (1e-9 basis, and that basis now means *contact*); worst 7.478e−07 = **1.57 τ**; cap-hits **2**. In substance the invariant landed: above-τ pair-instants **57,700 → 2**, worst penetration **0.947 m → 7.5e−07 m**. **My prediction conflated two thresholds and I did not notice until the data did** (§ 3, § 4) |
| **P.2** | presolve pairs/tick **8.997 → 1.5–5.0** (point 3.0); presolve worst 1.4824 → **0.30–1.20 m** | **⚑ FALSIFIED, BOTH LIMBS, AND THE SECOND ONE IS EMBARRASSING.** Presolve pairs **ROSE to 9.349**. Presolve worst is **1.4823596586100147 m — IDENTICAL TO I-7 TO SIXTEEN DIGITS**, because the worst presolve configuration is a **spawn** placement, which happens before any solve and which no solver can change. I predicted a fall in a quantity my own model makes invariant |
| **P.3** | sweeps: median ≤ 3, mean 1.5–8.0, max ≤ 64 | **SPLIT.** median **1** ✓ · mean **9.28** ✗ (just outside) · max **256** ✗✗ (the guard, D-I8-2) |
| **P.4** | separation travel ×1.5–6.0; max single-tick displacement ≥ 1.0 m on ≥ 1 cell | **SPLIT.** ×1.256 / **×2.594** / ×1.336 — only one cell inside the band · max displacement **1.0597 m** on CLUSTER/DEF-OFF ✓ |
| **P.5** | **ring max 19 → 12–18** (point 15); p90 3–4; median 0; **MG-3 MISSED**; MG-1 MISSED | **⚑ CONFIRMED ON EVERY LIMB. max 17 · p90 4 · median 0 · MG-3 MISSED · MG-1 MISSED.** The prediction the iteration was fired at, called correctly and for the stated reason |
| **P.6** | intake **falls 2–12 %** (point −6 %); mean HP 0.9860–0.9905 (point 0.988) | **SPLIT, AND THE MECHANISM IS FALSIFIED.** Intake **ROSE 7.45 %** — the opposite sign. Mean HP **0.98662**, inside the band at its very bottom, for a reason I did not predict. My stated mechanism ("spreading removes bodies from reach") is wrong: spreading *un-collapses* them and raises typical occupancy (§ 5.1) |
| **P.7** | reference cell does **NOT** die; `arena_tier_exhausted` @171 | **CONFIRMED** |
| **P.7b** | **CLUSTER/DEF-OFF survives wave 160** (stated at ~55 % confidence) | **⚑ CONFIRMED — it survives the entire ladder to 171.** The coin-flip call, and the lap's most consequential outcome |
| **P.8** | T2 **worsens** +0 % to +20 % (point +8 %); still MISSED | **⚑ FALSIFIED. l4l 233.551 → 223.265 s, −4.40 % — TOWARD the target.** My band excluded improvement entirely, so it could not have been right in that direction. Still MISSED |
| **P.9** | T3 median ratio **rises** from 1.1646; pearson r < 0.5; NEAR/MISSED | **SPLIT.** Ratio **FELL** to 1.1480 ✗ · r **0.0042** < 0.5 ✓ · verdict unchanged in character ✓ |
| **P.10** | excursions: EOT 13 → 6–14; intra 21 → 10–22 | **CONFIRMED. 12 and 22** (the latter at the band edge) |
| **P.11** | `observed_pairs_with_player` **605 → 0** | **⚑ FALSIFIED AS WORDED — 563 — AND THE FALSIFICATION IS THE FINDING.** The census threshold counts contact; all 563 sit at ≤ 7.478e−07 m, against I-7's at up to 0.947 m (§ 4.3) |
| **P.12** | MG-6 + MG-7 unchanged to the digit; MG-4 moves ≤ 0.02, MISSED | **SPLIT.** MG-6 **1.3877551020408165 s identical** ✓ · MG-7 **moved** 5.3518/93 → 5.3750/96 ✗ (it is ladder-duration-normalised and the ladder got longer) · MG-4 Δ **+0.0045**, MISSED ✓ |
| **P.13** | layer 1a EXACT ×3, layer 1b EXACT ×3, layer 1d divergent | **CONFIRMED at all three depths** (§ 1.1) |
| **P.14** | one-trajectory audit 0 rows outside tolerance on all three cells | **CONFIRMED** — the I-5 path contract survives S-3's larger displacements (check 11 green) |
| **P.15** | determinism ×2 EXACT ×3; batons FULL 67/67; wall 21/21 | **SPLIT.** determinism 0 differences ×3 ✓ · three batons FULL 67/67 ✓ · **wall 18/21** ✗ (§ 4) |

### 9.1 — ⚑ THE UNIFYING ERROR, SELF-NAMED

I-1 priced sustain not exposure · I-2 eHP not co-residence · I-3 throughput not reach · I-4 the size
of the counterplay not its shape · I-5 the repair not its convergence · I-6 the mean not the variance
· I-7 the numerator of a saturated ratio.

**I-8: I priced the SOLVER and never priced THE BOARD IT PRODUCES.**

Every quantitative prediction I got wrong — P.1's zero, P.2's presolve fall, P.6's intake fall,
P.8's slowdown, P.11's zero — descends from one mental image: *converging the solver spreads the
crowd out, so there is less of everything near the player.* **The measurement says the opposite.**
Interpenetrating bodies were **occupying the same ground**, which is *fewer distinct occupants* at
typical range, not more. Enforcing non-overlap gives each body its own ground: mean ring occupancy
up 5.1 %, mean disc occupancy up 4.9 %, body-hit rows up 8.8 %, intake up 7.4 %, clears 4.4 %
faster — while the geometrically impossible *extremes* fall (ring 19 → 17, disc 32 → 27).

⚑ **And the § 7.1 error I pre-registered fires as well, which is two errors in one lap and both were
written down first:** the solver moves bodies **2.26× further per tick than pursuit does**. I priced
the constraint, not its side effect, exactly as I said I might.

---

## 10 — WHAT DID **NOT** CHANGE

The hit test (`MovingDisc.radius_m` 3.0, centre-only; check 17 green ×3) · the contact physics
(symmetric depenetration, player `fixed`) · the tick order (`separate_then_resolve`) · every fold
I-1…I-7 landed · the RNG (the solver draws nothing) · Law 3 (`moved: {}`) · the seed (conductor
seed 9, Discipline #3, no new seed base consumed).

**Determinism, and it is load-bearing now that S-2 has traded order-independence away:** ×2
masked-EXACT on all three cells, **plus** a unit-level probe (check 21) that presents the *same*
inputs in a *shuffled dict insertion order* and requires byte-identical output. The method is
order-sensitive; the order is total and fixed at `sorted(actor_id)`. **FG-10 holds by construction,
proven rather than promised.**

**And the cull is checked, not trusted** (check 9): the index-bounded `worst_penetration` — on whose
exactness the entire convergence verdict rests — was compared against the independent O(N²)
`non_overlap_census` on **200 synthetic populations**, **0 disagreements**.

---

## 11 — COST

Wall time: CAMP/DEF-OFF **32.05 s** (I-7: 4.45 s, ×7.2) · CLUSTER/DEF-OFF **22.41 s** (1.57 s,
×14.3) · CLUSTER/DEF-ON **25.38 s** (3.08 s, ×8.2). Whole lap including 6 baseline arms, 3
determinism replays and 5 sensitivity cells: **~4.5 min**. Reported because a solver that converges
is a solver that iterates, and the cost of the invariant is part of the invariant's price.

---

## 12 — ⚑ WHAT GOES TO THE CONDUCTOR — three items, no HALT

1. **⚑ THE SOLVER NOW DOES MORE TRANSPORT WORK THAN THE LOCOMOTION DOES — 2.26×, MEASURED (§ 3.2).**
   The invariant is true and the mechanism that makes it true moves bodies 0.739 m per tick against
   a monster's own authorised 0.327 m. **I am not proposing a fix, because every fix I can think of
   is a model choice and not a decode:** a speed-limited depenetration (bodies stay overlapping
   across ticks — the invariant goes soft again), a per-tick displacement clamp (a new length
   constant, which R-PM4-8's own substrate does not carry), or accepting it as the price of the
   constraint. **The third is what this lap shipped, by default rather than by decision, and the
   conductor should know that is what happened.** Lap F's `pathMass` is emitted and undescribed
   (C-F6) and would be the natural substrate for a mass-weighted split — **that is a legolas decode
   question, not a gamora modelling choice.**
2. **C-I8-1 — my own I-7 clause-2 ARC limb over-stated its case (§ 6.1),** raised in the math note
   before this run rather than after the numbers arrived. The clause-2 VERDICT is unaffected: it
   rests on 26 measured interpenetrating pairs, not on ARC. Recorded so the ledger's L-15 entry can
   carry the qualification if the conductor wants it there.
3. **D-I8-3 — `ManaBurnDrain` has no resistance row (§ 4.5),** surfaced by a sensitivity cell and
   deliberately not closed. It is an energy-drain family; the closure path is the same one I-7
   named for `SlowManaLeach` — route it into the sim's energy ledger, which is a **new mechanism**
   and therefore an iteration's worth of work, not a patch. **It is a live halt risk for any future
   cell of record whose trajectory reaches it.**

### 12.1 — My lean on I-9, offered as a lean and not a decision

**R-PM4-18's charter already pre-registers I-9 as the SUSTAIN-ACTUATION FOLD, and this lap
strengthens the case rather than weakening it.** The reference cell's mean HP went *up* while intake
went up 7.4 %; min HP went *up* to 0.4875; **K-3 Menhir's Will stopped firing entirely.** I-7
measured the sustain offering 118× what the HP bar can absorb; I-8 has now added 129,150 damage and
watched the trace get *healthier*. The residual is where I-7 said it was — **on the player's
greedy-optimal actuation, not on the monsters** — and the video's signature remains a *persistently
depressed* trace, which is a statement about recovery.

⚑ **One caution I owe the conductor before I-9 fires:** T1's only evidence that this model can kill
a player at wave 160 was CLUSTER/DEF-OFF's I-7 death, **and this lap removed it.** A sustain fold
that lowers the DEF-ON trace toward 0.932 will be judged against a board that is now measurably
less lethal than the one that produced that death. The comparison must be to **I-8's** numbers, not
to I-7's, and the pinned digests above are what that comparison is against.

---

**Author:** gamora (simulation seam) · 2026-08-14 · math note first, code second, and the git order
(`c36284a7` → `b4732d73` → `74dbbd8b` → `f33ee59c`) is the proof.
