# KC2-PM4 · I-24-D — THE ENGAGEMENT CENSUS — LANDING NOTE

**MEASUREMENT-ONLY · ZERO FOLD · NO REPAIR · NO POLICY CHANGE · NO SCORED-LADDER CLAIM**

**Agent:** gamora · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** `R-PM4-63 part 5`; charter rows `L-51`/`R-PM4-61`, `L-52`/`R-PM4-62`,
`L-53`/`R-PM4-63`. **Base:** my own I-23 fold, engine `793b2937`.

**Commits (engine, mine, FIVE — the first FOUR are zero code):**
`6145d835` math note **ALONE** → `bb22f97c` addendum #1 `D-I24D-1` (**before** anything) →
`089795a3` addendum #2 `D-I24D-2` (**before** its repair) → `34125a3d` addendum #3 `D-I24D-2(b)`
(**before** the second repair) → `d4ff7e8b` census + module + driver + findings + MIGRATION +
AGENT_STATE. **NOT PUSHED** — the conductor pushes at banking.

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i24d-findings-20260816_060527.json`
sha256 **`0e64fe317a46c1ba68dae495c2429e1f3faf794a4fa7f8742853775595a6f0c1`**. Wall **2.55 s**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**The ring is not being emptied. It is never occupied.** Across both arms the census recorded
**26 ring exits** and **25 of them are the body dying where it stands**. There are **ZERO**
exits caused by the player moving away, **ZERO** retargets, and **ZERO** unlabelled exits. The
engage-state census says why: on `PX-LO` the board spends **2,301 body-ticks in `PURSUE` and 25 in
`HALT_AT_ENGAGE`** — **zero** in patrol, **zero** parked, **zero** blocked — and the only
transitions that exist anywhere in the run are `PRESPAWN→PURSUE`, `PURSUE→HALT_AT_ENGAGE`,
`HALT_AT_ENGAGE→DEAD`. **The engagement state machine has exactly one exit and it is dying.**
Nothing pushes bodies out of the ring because **there is nothing in it to push out**: the board is
permanently closing, arrives one body at a time, parks on the radius to within one ULP, and is
killed there.

⚑ **And my `E-3` — registered against the commission's own frame — PASSED.** `R-PM4-63 part 3`
named the player's own travel as a candidate for what empties the ring. **It empties it zero
times.**

---

## 1 — ⚑ (a) THE RING LEDGER, WITH ITS EXHAUSTIVE PARTITION ASSERTED

| | `PX-LO` | `PX-HI` |
|---|---:|---:|
| bodies on the fought roster | 28 | 45 |
| ever entered the ring | **4** | **22** |
| never entered | 24 | 23 |
| intervals · exits · censored | 4 · 3 · 1 | 23 · 23 · 0 |
| re-entries | 0 | **1** |

### 1.1 EXIT-CAUSE DISTRIBUTION — **THE PARTITION CLOSES, AND IT IS ASSERTED IN CODE**

| cause | `PX-LO` | `PX-HI` | combined share |
|---|---:|---:|---:|
| **`died_in_ring`** | **3 (100 %)** | **22 (95.65 %)** | **25 / 26 = 96.15 %** |
| `displaced_body_moved` | 0 | 1 (4.35 %) | 1 / 26 |
| **`displaced_player_moved`** | **0** | **0** | **0** |
| **`retargeted`** | **0** | **0** | **0** |
| `displaced_both_moved` · `displaced_neither_moved` · `other_named` | 0 | 0 | **0** |

**`A-1`, the proof obligation the commission names, ASSERTED AND HOLDING:** `Σ_c exits[c] ==
n_exits` — 3 == 3 and 23 == 23, raised as `CensusPartitionError` on failure, **wall row 17 on both
arms**. `A-2` intervals == exits + censored (4 == 3+1, 23 == 23+0) · `A-3` bodies == entered +
never (28, 45) · `A-4` per-body interval sum · `A-5` labeller **TOTAL** with `other_named = 0` and
the reason list emitted empty rather than absent.

**`A-6` — the cross-instrument check, and it is the one that makes this a measurement:** the
ledger's per-tick occupancy reproduces `locomotion_census` column 0 **tick for tick, 0 ticks
differing**, and its zero bucket reproduces `ring_density.hist_engage["0"]` — **72 == 72**.
*A new instrument that disagrees with the old one is a claim; one that reproduces it is a
measurement.*

### 1.2 ⚑ THE NEVER-ENTERED, AND THE CLOSEST-APPROACH DISTRIBUTION THAT EXPLAINS EVERYTHING

| | `PX-LO` | `PX-HI` |
|---|---:|---:|
| min closest approach | **2.3999999999999995** (`D` − 1 ULP) | 1.0699995672656022 |
| **median** closest approach | 9.5154 | ⚑ **2.4000000000000004** (`D` + 1 ULP) |
| bodies ever within 3.0 m | 5 | 36 |
| **of those, within 1e-9 m of `D`** | **5 / 5 = 1.00** | 21 / 36 = 0.583 |
| separations within **8 ULP** of `D` | **25** | **87** |

⚑ **On `PX-HI` the MEDIAN body of a 45-body roster ends its closest approach one ULP OUTSIDE the
ring.** Bodies do not approach the ring gradually and mill about in it. They arrive, the arrival
clamp `travel = min(v·dt, max(0, dist − D_ENGAGE_M))` puts them **on** the radius, and whether
they count as "in" is decided by the last bit of a double.

---

## 2 — ⚑ (b) THE KILL RATE, JOINED TO RING MEMBERSHIP — AND THE QUESTION ANSWERED

| | `PX-LO` | `PX-HI` |
|---|---:|---:|
| seconds (measured clock, `D-CON-4`) | 7.6735 | 36.4082 |
| kills total · **in ring** · at reach | 4 · **3** · 1 | 35 · **22** · 13 |
| **`R_kill_ring`** bodies/s | **0.39096** | **0.60426** |
| `R_entry` bodies/s | 0.52128 | 0.63173 |
| **`R_kill_ring` / `R_entry`** | **0.750** | **0.957** |
| mean ring occupancy | 0.23404 | 0.33632 |
| Lap X decoded solo kill rate (**context, a GRADE**) | 1.796 – 2.161 | same |
| ratio to the bracket's floor | **0.218** | **0.336** |

> **THE ANSWER TO THE COMMISSION'S QUESTION IS THAT THE QUESTION HAS THE WRONG SHAPE.** The player
> does not empty the ring faster than arrival refills it. `R_kill_ring / R_entry` is **0.75 and
> 0.96** — kills and entries are the *same* flow — while mean occupancy is **0.234 / 0.336**.
> **The ring is a throughput channel of capacity ≈ 0, not a pool being drained.** A body enters,
> occupies for a handful of ticks, and dies; the next one has not arrived yet.

And the kill rate is **not** the binding term either: `R_kill_ring` is **4.6× and 3.0× BELOW**
Lap X's decoded solo floor. The player is not clearing the ring too fast. **The ring is not being
filled.**

---

## 3 — ⚑ (c) `D-I21-1` QUANTIFIED AT LAST, AND IT IS TOTAL

Computed **post-hoc** off `run.tracks.player_path_*`, which has existed since PM-1 — **zero new
instrument, therefore zero perturbation by construction.**

| declared window | `PX-LO` STATIONARY / MILLS / TRAVERSES / AMBIG | verdict |
|---|---|---|
| **`W` = 12** (the pre-registered primary) | 0 / **0** / **78** / 4 | **TRAVERSES-DOMINANT** |
| `W` = 6 (sensitivity) | 5 / **0** / **83** / 0 | TRAVERSES-DOMINANT |
| `W` = 25 (sensitivity) | 0 / **0** / **44** / 25 | TRAVERSES-DOMINANT |

⚑ **ZERO MILLS WINDOWS AT EVERY WINDOW SIZE, ON BOTH ARMS** (`PX-HI`: 15 MILLS / 351 TRAVERSES,
95.9 % traverses). The thresholds `S_MILL` 0.30 / `S_TRAV` 0.70 were declared as a symmetric pair
in a commit containing zero series, and the **raw per-tick step and heading series are published**
so anyone can re-run the classification at other cut points.

**The tick-grain numbers, `PX-LO` wave 151:**

| | sim | Lap U referent |
|---|---:|---:|
| **median heading change** | **0.000 rad** | — (0.060 straightness) |
| mean heading change | 0.1425 rad | — |
| heading-change rate | 1.7197 rad/s | — |
| moving fraction | 0.7419 | 0.64 – 0.83 |
| **speed while moving** | **5.6719 m/s** | **3.1 – 3.8 m/s** |
| path / net / straightness (**wave grain**, Lap U's own) | 31.948 / 7.120 / **0.2229** | 40.2–83.0 / 1.99–11.27 / **0.060** |
| longest stationary run | 0.6531 s | 1.73 s |

> **The sim's player walks in a straight line at half again the referent's speed and turns a median
> of exactly zero.** `D-I21-1` said *"the sim's player traverses where the referent mills."* At
> tick grain it is not a tendency — **it is the entire distribution.**

⚑ **AND IT STILL DOES NOT EMPTY THE RING** (§ 1.1). Both facts are true, and holding them together
is the finding: **the player over-travels, and the over-travel is not what keeps the ring empty.**

---

## 4 — ⚑ (d) THE ENGAGE-STATE CENSUS

### 4.1 THE BOARD IS IN PERMANENT PURSUIT

`PX-LO` body-ticks (2,632 total): **`PURSUE` 2,301 (87.4 %)** · `DEAD` 114 · `PRESPAWN` 192 ·
**`HALT_AT_ENGAGE` 25 (0.95 %)** · **`PATROL_TO_NODE` 0** · **`PARK_AT_NODE` 0** · **`BLOCKED` 0**.
`PX-HI`: `PURSUE` 6,036 · `HALT_AT_ENGAGE` 192 · the same three zeros.

**Every transition observed anywhere in the run:**

| transition | `PX-LO` | `PX-HI` |
|---|---:|---:|
| `PRESPAWN → PURSUE` | 4 | 7 |
| `PURSUE → HALT_AT_ENGAGE` | **5** | 33 |
| `HALT_AT_ENGAGE → DEAD` | **4** | 32 |
| `HALT_AT_ENGAGE → PURSUE` | 0 | **1** |
| `PURSUE → DEAD` | 0 | 3 |

⚑ **There is exactly ONE transition out of engagement that is not death, in the whole census, and
it happened once.** The gate reconstruction (never `gate_open()` — wall row 22 asserts **zero**
calls, by AST) reports the gate OPEN for **28/28** and **45/45** bodies, agreeing with
`gate_ever_opened` with **zero disagreements**. **`RETARGET_BINDING_CLAUSE` is the empty dict: no
body ever failed view, leash or memory.**

Dwell: mean **0.786** ticks in ring per body, **24 of 28 bodies with zero**; ticks at the boundary
(within 8 ULP) mean 0.893, **5 bodies with any** — one more than ever entered, which is the
5th `PURSUE→HALT_AT_ENGAGE` transition landing on the outside of the predicate.

### 4.2 THE LAP V-2 MAPPING — **7 EXPRESSED, 17 `UNREACHED`, AND THE GAP IS THE DELIVERABLE**

Against Lap V-2 § 6's 15 ICF-shared scanning states + 9 incapacitated states
(`3aeccfe9…b7c1`): `Attack` and `WaitToAttack` → `HALT_AT_ENGAGE` · `Pursue` → `PURSUE` ·
`Patrol`/`Move` → `PATROL_TO_NODE` · `Return`/`Idle` → `PARK_AT_NODE`.

**`UNREACHED` (17), NAMED AND NOT APPROXIMATED:** `Roam`, `Wander`, `DodgeAttack`, `JumpAttack`,
`RepositionForAttack`, `FollowLeader`, `DefendLeader`, `Trapped`, and **all nine incapacitated
states** — the sim has **no monster-side crowd control at all**. **No state was invented to fill a
row.**

⚑ **AND THREE OF THE SEVEN "EXPRESSED" STATES HAVE ZERO TICKS.** `PATROL_TO_NODE`, `PARK_AT_NODE`
and `BLOCKED` are expressible and never expressed on this board. The sim's *realised* state
vocabulary on the record cell is **four states**: prespawn, pursue, halt, dead.

---

## 5 — ⚑ (e) THE OCCUPANCY CURVE, GRADED (A GRADE, NEVER AN INPUT)

| | `PX-LO` | `PX-HI` | Lap R referent |
|---|---:|---:|---:|
| mean occupancy at 2.400 m | **0.23404** | **0.33632** | **3.2423 / 3.3519 / 3.4251** (bracket **NOT ruled**) |
| ratio to bracket | **0.0722 – 0.0683** | **0.1037 – 0.0982** | — |
| median · max | 0 · 1 | 0 · 2 | 3.0 (at R300) |
| dry fraction | 0.7660 | 0.7108 | 0.1989 – 0.2063 |
| longest dry run | **4.163 s** | **5.469 s** (w151) / 2.204 s (w152) | **2.75 s** |
| per-wave vs Lap R `R150` | w151 0.2340 vs 0.871 (**−0.637**) | w151 0.2790 (−0.592) · w152 0.4803 (−0.290) | — |

**~14× below the referent on `PX-LO`, ~10× on `PX-HI`**, and the *shape* misses too: the sim's
longest dry run is 1.5–2.0× the referent's on a board that is supposed to be denser.

⚑ **`PX-HI` reaches occupancy 2 for 16 + 5 ticks.** That is the highest ring occupancy this run
has ever measured, and it is still less than the referent's median.

---

## 6 — ⚑ THE TWO PREDICATES: `E-2` PASSED, AND HERE IS THE EXACT TICK

Math note § 2 named a hazard before any code: three live sites test the same ring with **two
different float predicates**.

```
P-INST  (every instrument, run.py)       hypot(b − p)      <= D_ENGAGE_M
P-SEEK  (player_locomotion, the player)  dx*dx + dy*dy     <= D_ENGAGE_M * D_ENGAGE_M
```

**Measured disagreements: 1 on `PX-LO` (of 2,326 live pairs), 5 on `PX-HI` (of 6,228). All in the
same direction — `P-INST` says IN, `P-SEEK` says OUT.** The exact case:

```
run_tick 86 · w151_a025 · hypot = 2.4  EXACTLY
   d²  = 5.760000000000001        D²  = 5.76
   P-INST = True                  P-SEEK = False
```

⚑ **The player's own contact test rejects a body that is sitting at exactly the melee-target
distance, because squaring rounded up by one ULP.** On that tick the seek policy does not take its
*"in contact: stand and kill"* branch; it takes the *"close on the nearest"* branch, whose arrival
clamp then moves him ≈ 0.

**NAMED, NOT FIXED.** `R-PM4-63 part 5`: *"If the census surfaces an obvious cause with an obvious
fix — NAME it, do not fix it."* No predicate was changed under any outcome. **And it is NOT the
residual**: 1 and 5 ticks cannot move a 14× occupancy gap.

---

## 7 — ⚑ NON-PERTURBATION: PROVEN, NOT ASSERTED

| leg | `PX-LO` surface | `PX-LO` knot |
|---|---|---|
| **N-1** ledger OFF | `d23962a9a6b622b0273e7c0b7b6266378375331acea2ea66001e0901b2885c35` | `4bb04cab65fd5ba1852de89a14e5b9223ad1a1eaa1df466d09816464af4320c8` |
| **N-2** ledger ON | **identical** | **identical** |
| **N-3** ON, real second execution | **identical** | **identical** |

`PX-HI`: `85b77930c0bdd7d22e662216f97424c8253cf199b420bc26f0d3439d0fd76cfc` /
`f6540ccb7ccf08296397876d09c6c53b44cfcd735760bdb24512b301fc2c22d7`, likewise identical ×3.

**Replication check (math note § 9, NOT a grade and labelled as such in the artefact):** `PX-LO`
death **151**, l4l **7.673469387755103**; `PX-HI` death **152**, l4l **36.40816326530613** —
**exactly I-23's**, to the seventeenth digit. **The census cell IS I-23's cell.**

---

## 8 — ⚑ THE PRE-REGISTERED EXPECTATIONS, GRADED HONESTLY

| id | claim | grade |
|---|---|---|
| **`E-1`** | ≥ 50 % of bodies reaching 3.0 m park within 1e-9 m of `D` | ⚑ **PASSED — 100 %** (5/5 `PX-LO`) |
| **`E-2`** | `P-SEEK` and `P-INST` disagree ≥ once | ⚑ **PASSED** — 1 / 5 |
| **`E-3`** | ⚑ **AGAINST MY LEAN AND THE COMMISSION'S FRAME:** `displaced_player_moved` < 25 % | ⚑ **PASSED — 0.0 %, on 26 exits** |
| **`E-4`** | `died_in_ring` is the plurality (> 40 %) | ⚑ **PASSED — 100 % / 95.65 %** |
| **`E-5`** | ⚑ **AGAINST MY OWN PARKING STORY:** `retargeted` ≤ 2 % | ⚑ **PASSED — 0.0 %** |
| **`E-6`** | `R_kill_ring` < 1.796 **and** mean occ < 1.0 | ⚑ **PASSED** — 0.391, 0.234 |
| **`E-7`** | TRAVERSES-dominant at `W` = 12 | ⚑ **PASSED** — 78/0, and at every window |
| **`E-8`** | censoring ≤ 10 % of intervals | ⚑ **FAILED — 25 %** (1 of 4 on `PX-LO`). § 9 |
| **`E-9`** | (addendum #1) **zero** separations in `[2.4, 2.4000000953674316)` | ⚑ **FAILED — 13 (`PX-LO`) / 58 (`PX-HI`)**. § 10 |

**Mechanical pins:** `P.1` `law_3.moved == {}` on **21** witnesses ✅ · `P.2` frozen **20/20** hard
gate ✅ · `P.3` N-1…N-4 ✅ · `P.4` A-1…A-6 ✅ · `P.5` inputs re-hashed **6/6** EXACT ✅ · `P.6` wall
**16/16 GREEN**, `keys_asserted` per row ✅ · `P.7` smoke **296 pass / 1 PRE-EXISTING**, unchanged
from I-23 ✅ · `P.8` no new `waves[0]` key ✅ · `P.9` zero referent numerals in any `If`/`While`/
`IfExp` test in the `kc2` package ✅ · `P.10` zero fold ✅.

---

## 9 — ⚑ `E-8` FAILED, AND ITS FAILURE IS THE SAME FACT AS `D-I24D-4`

25 % of `PX-LO`'s intervals are censored — 1 of 4 — because the player dies at tick 94 with a body
still in the ring. On the small `PX-LO` sample every share in § 1.1 must therefore be read
conditionally, **which is exactly what `E-8` was registered to force me to say.** `PX-HI` censors
**zero** of 23, and its distribution agrees with `PX-LO`'s, so the conclusion survives — but it
survives **because `PX-HI` exists**, not because `PX-LO` was clean.

**And the same fact, from the other side, convicts my own taxonomy — `D-I24D-4`.** My math note
§ 4.1 declared `halted_outside` as *"the body stopped and did not close"*. **24 `PX-LO` bodies got
that label and NOT ONE of them stopped**: `PATROL_TO_NODE` = 0, `PARK_AT_NODE` = 0, `BLOCKED` = 0,
`PURSUE` = 2,301. They were **all still closing when the fight ended at 7.67 s**.

⚑ **THE LABEL IS NOT REWRITTEN.** Rewriting a pre-registered taxonomy after seeing its output is
the thing pre-registration exists to prevent. The corrected reading —
**`FIGHT_ENDED_WHILE_CLOSING`** — is published beside the emitted key, exactly as `D-I23-3`'s two
clauses were published side by side.

---

## 10 — ⚑ `E-9` FAILED: `D-I24D-1` IS A **MEASUREMENT** DEFECT, NOT A LABELLING ONE

Addendum #1 (`bb22f97c`, committed **before any census result**) found that my math note § 2 — and
I-23's emitted `d_engage_m` field, and my I-23 landing § 5.1, and charter row `L-53` — all name the
ring radius **`2.4000000953674316`**, while the simulation tests at `locomotion.D_ENGAGE_M` =
**`2.4`**. The root cause is mine: at I-23 I declared `intake.MELEE_TARGET_DISTANCE_M` as a fresh
literal instead of importing by identity, so **a pinned constant acquired a second value at a site
of mine**.

I predicted the gap could not matter (`E-9`, registered before any series existed). **It matters:**

| | `PX-LO` | `PX-HI` |
|---|---:|---:|
| separations in `[2.4, 2.4000000953674316)` | **13** | **58** |
| in-ring ticks actually measured | 22 | 192 |

⚑ **Had the ring been tested at the radius I published, `PX-LO`'s occupancy ticks would have been
~35 instead of 22 — a ~59 % change.** The parking hypothesis is *why*: the mass sits exactly where
the two constants disagree.

**It does not move the verdict** — 0.372 instead of 0.234 is still ~9× below Lap R — and saying so
is part of the report, so that nobody reads this as *"the residual was a float bug."*
**NOT REPAIRED** (`R-PM4-63 part 5` forbids it; moving the constant is a Law-3 move).

**`UNREACHED-I24D-1`, NAMED NOT DECODED:** is the engine's `meleeTargetDistance` operand the
float32 the DB stores, promoted (`2.4000000953674316`), or the DB-CITED display value (`2.4`)?
Both readings are honest; the sim runs on the second. **A record question, worth ~9.5e-8 m, and it
has gone twenty-four iterations unnoticed.**

---

## 11 — DEFECT TABLE (all mine; every addendum committed BEFORE its repair)

| id | defect | disposition |
|---|---|---|
| **`D-I24D-1`** | the published ring radius is not the one the sim tests at; root cause is a re-stated pinned constant at my own I-23 site | **NAMED, NOT REPAIRED.** Addendum `bb22f97c` ALONE and before any result; `E-9` registered there and **FAILED**, promoting it to a MEASUREMENT defect. Travel path reported (I-23 findings → I-23 landing § 5.1 → `L-53`) |
| **`D-I24D-2 (a)`** | one `DefenceField` shared across N-1/N-2/N-3; its accumulators reach `waves[0]` and so the digest surface | **REPAIRED.** Addendum `089795a3` before the repair. Caught by my own N-3 leg |
| **`D-I24D-2 (b)`** | **my repair was incomplete** — `IntakeFold` and `VectorFold` were shared too | **REPAIRED.** Addendum `34125a3d` before the second repair. ⚑ **Lesson: a shared-mutable-state defect has a POPULATION, and a population is ENUMERATED by a differencing probe, not RECOGNISED by reading.** Discipline #11 failing inside my own defect handling |
| **`D-I24D-3`** | wall row 22 claimed an AST check and was a substring count; it convicted its own docstrings | **REPAIRED IN-ITERATION by STRENGTHENING it** into the AST check it claimed to be. The `D-I23-4` class: the guard was right, my implementation was the wrong shape |
| **`D-I24D-4`** | my declared `halted_outside` label over-claims; 24 bodies were pursuing, not halted | **DECLARED, NOT REWRITTEN.** Corrected reading published beside the emitted key (§ 9) |

> ⚑ **LEG N-3 IS THE WHOLE STORY OF THIS ITERATION'S DEFECTS.** With two legs I would have reported
> N-1 ≠ N-2 as an instrument perturbation that does not exist. The third leg — a *real second
> execution of the instrumented configuration*, declared in math note § 9.2 before any code — is
> what turned a false HALT into two real driver defects. **Fourth consecutive iteration in which my
> own pre-registration caught my own work before a number was reported.**

---

## 12 — DIGESTS (full 64 hex, `R-PM4-55 part 2`)

### 12.1 Outputs

| artefact | sha256 |
|---|---|
| `output/kc2-pm4-i24d-findings-20260816_060527.json` | `0e64fe317a46c1ba68dae495c2429e1f3faf794a4fa7f8742853775595a6f0c1` |
| `math/kc2-pm4-i24d-engagement-census-2026-08-16.md` | `116063c557575ab74eae5225ae5652ed8de3e21b5a3923a97d62df31b1e10719` |
| `math/kc2-pm4-i24d-engagement-census-ADDENDUM-2026-08-16.md` | `7f9dc94b6013174241ff236f2c88d8c674452d14358ee0abd36405f44c01c424` |
| `math/kc2-pm4-i24d-engagement-census-ADDENDUM-2-2026-08-16.md` | `dbff7d7d4e9c9bdab117d7692d0d1b8caef21acfc7647645c90eeb478abafd54` |
| `math/kc2-pm4-i24d-engagement-census-ADDENDUM-3-2026-08-16.md` | `0262fafb4e6f405f46636529436e59693af77bd0db6215373403df4e61c363bd` |
| `kc2/engagement.py` (**NEW**) | `48a9f54f2cbe8cefd066fd005319bf7a6953e8a53866344e3981a5d98017a0c4` |
| `kc2/run.py` | `9a760076f143635bf657159374fd22e1ba28de8615d4ea4e3a97c9d38e63306e` |
| `scripts/gamora_kc2_pm4_i24d_engagement_census_2026_08_16.py` | `c2e5d2c9bb3bc5661a9ec164d6a29740ac507765fa21157818799d6eee0a2804` |

### 12.2 Inputs, re-hashed EXACT from bytes before a reducer ran — **6/6** (HALT armed; none fired)

| input | sha256 |
|---|---|
| Lap R `pm4r_contact_occupancy.csv` | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` |
| Lap R `pm4r_findings.md` | `c223dfb04653a7e8682d5c1dd42356fc2a8398b06951372445d235a6eff224ea` |
| Lap R `pm4r_movement_episodes.csv` | `dc3173ae53c2a371d9336e95db79c25c4deb04834cebdd4c9318f554d9f576cc` |
| Lap V-2 `pm4v2_findings.md` | `3aeccfe9ec8b38ba486212ae78e84b1a0aeb3493d838d3d90c5a80ac9601b7c1` |
| Lap U `pm4u_findings.md` | `f1a34cb11c6015d83169bd2ebbb7fd3ee7ba15bbc20622756f37fbb75fbec6ce` |
| **I-23 findings (the incumbent, pinned to the ARTIFACT)** | `0e4084b55f0af955f0b91d809da8e1b3267d6876a1c177a8eba3655c21048368` |

---

## 13 — THE WALL — **16/16 GREEN, `keys_asserted` ON EVERY ROW**

1 inputs 6/6 EXACT · 2 frozen **20/20** hard `SystemExit` · 3 `law_3.moved == {}` · 4 **21**
witnesses, every engagement witness `moved: False` · **17** A-1 exhaustive partition ×2 arms ·
**18** A-2/A-3 conservation ×2 · **19** A-5 labeller totality ×2 · **20** A-6 cross-instrument
agreement tick-for-tick ×2 · **21** N-1…N-4 non-perturbation · **22** `gate_open` called **0**
times (AST, both census sites) · **23** zero referent numerals in any branch condition ·
**24** ZERO FOLD.

**Law 3:** `moved == {}` on 21 witnesses including `D_ENGAGE_M` **2.4** (imported by identity),
`LAP_R_MEAN_OCCUPANCY` (**a grade, never an input**), `LAP_X_SOLO_KILL_RATE` (**context**),
`W_TICKS` / `S_MILL` / `S_TRAV` / `BOUNDARY_ULP` (**declared classifier parameters — published,
never simulated**) and `⚑ ZERO_FOLD`. **ZERO free constants; ZERO constants entering simulation
arithmetic.**

**Smoke:** `296 pass / 1 PRE-EXISTING failure` — the `test_AC_10_10` bare-30.0 AST guard whose
offender is `secondary_streams.py:136`. **Unchanged from I-23.**

---

## 14 — CAVEATS THAT TRAVEL WITH THE NUMBERS

* **`PX-LO` is 4 intervals.** It is a small sample and 25 % of it is censored. Every `PX-LO` share
  is reported beside `PX-HI`'s 23 exits for exactly this reason.
* **The `never_entered` reason `halted_outside` OVER-CLAIMS** (`D-I24D-4`). Read it as
  *fight-ended-while-closing* on this board.
* **`E-9`'s failure makes I-23's contact-count LABEL wrong and its magnitude sensitive** at the
  ~59 % level — but not sensitive enough to move a 14× gap. Both halves travel together.
* **`R_kill_ring` and every per-second figure ride the sim's MEASURED clock** (`D-CON-4`); no
  per-second figure is claimed as decoded.
* **Lap R's three-anchor bracket is NOT ruled** and is reported as a bracket everywhere.
* **`D-I21-1` is now quantified but still UNREPAIRED, and the reason is unchanged:** the repair is
  not decoded. Lap U measures the referent's player; it does not decode a seek policy.
* `D-PDEF-2`, `T17`, `UNREACHED-I23-3` (Lap Y in flight) and the `pools_for` default carry
  unchanged.

---

## 15 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. **THE RESIDUAL IS NOT AN EXIT PROBLEM AND THE ENGAGEMENT CHAPTER SHOULD BE RENAMED ON THIS
   MEASUREMENT.** `R-PM4-63 part 3` framed it as *"bodies reach the 2.400 m ring and do not stay in
   it."* **They stay in it until they die — 96 % of exits are death, 0 % are displacement by the
   player, 0 % are retargets.** The board is in `PURSUE` for 87 % of its body-ticks and in contact
   for **0.95 %**. **Nothing removes bodies from the ring. Bodies do not ARRIVE at it — one at a
   time, on a 2.4 m circle, in a fight that lasts 94 ticks.** The eleventh name is not persistence;
   it is **ARRIVAL CONCURRENCY AT CONTACT RANGE**, and it is the same functional I-22 left open
   (peak living inside 11.64 m = 10 vs referent 19–36).

2. **THE HIGHEST-LEVERAGE MEASURED CANDIDATE IS THE ONE-AT-A-TIME GEOMETRY, AND IT IS NOT A
   MITIGATION, ROSTER, ARRIVAL-CLOCK OR SPEED TERM.** `max_occupancy` is **1** on `PX-LO` and **2**
   on `PX-HI`. The referent's *median* is 3. Whatever lets three bodies stand on a 2.4 m circle at
   once, this sim does not have it — and I-7's `ring_joint` arc-capacity instrument (already built,
   already emitting) is the existing measurement that speaks to it. **I am naming it, not decoding
   it** (`R-PM4-56 part 4`).

3. **`D-I21-1` IS NOW A QUANTIFIED, TOTAL RESULT (zero MILLS windows at three window sizes) AND IT
   IS STILL NOT THE RESIDUAL'S CARRIER.** If the conductor wants it repaired, it needs its own
   iteration, its own decode of a seek policy, and its own pre-registration — and this census is
   the evidence that it should be sequenced for *fidelity*, not as a residual fix.

4. **`E-2`'s PREDICATE FORK AND `D-I24D-1`'s RADIUS FORK ARE THE SAME BOUNDED RECORD QUESTION** and
   they cost one lap between them: does `gameengine.meleeTargetDistance` operate as float32 or as
   the cited display value, and does the engine's own contact test square or take a root? Both are
   worth ~1e-7 m; together they move `PX-LO`'s occupancy by ~59 % and neither is decidable from
   this seat.

5. **`D-I24D-2`'s lesson is offered for the commissioning discipline** beside `D-CON-2`'s
   FILES-not-counts, `D-CON-3`'s cite-the-sheet and `D-CON-4`'s inventory-what-the-sim-measures:
   **a shared-state defect has a POPULATION, and a population is ENUMERATED, not RECOGNISED.** The
   three-line differencing probe belongs *before* the repair, not after it fails.
