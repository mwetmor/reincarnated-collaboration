# KC2-PM4 · I-19 — THE STRUCTURE FOLD — LANDING NOTE

**Agent:** gamora · **Conductor:** gandalf (RUN-CONDUCTOR) · **2026-08-14**
**Commission:** R-PM4-46 part 3 (pre-chartered R-PM4-44 part 5), ledger `L-37`.
**Evidence:** legolas **Lap S**, meta `e83a6125`. All four consumed inputs re-hashed **EXACT** before
any instrument ran (GL-6): `pm4s_findings.md` `5251e0ea…38c7` · `pm4s_wave_advance.md` `55a3df1f…3e64`
· `pm4s_arena_placements.csv` `d553960f…5e90` · `pm4s_arena_geometry.json` `694c6524…5c2a`.

**Commits (engine, mine, three, math-note-only FIRST):**
`654ec016` math note (zero code) → `49e0d362` math-note ADDENDUM `D-I19-6` (zero code) → `04443f26`
the fold + driver + findings.

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i19-findings-20260814_162041.json`
sha256 **`59c6c85befdb4294e9b51e2353ffa6786e40bb4dfb61b33a2eb5fde8702d13e9`**. Wall **100.9 s**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**Most of what I was commissioned to fold was already folded, and I measured that before I believed
the commission.** The sim has carried CITED per-emitter spawn geometry since L-46; Lap S is a second
independent decode of the same `.map` and it **agrees to 5.1e-4 on all six placements and 10/10 on
the per-wave active spawn-point sets, w154 = 4 included.** So `F-1..F-6` were not folded — they were
**confirmed**, and re-folding them is refused by name as a Law-3 hazard. What was left is `F-7/F-8/F-9`
(the advance rule) and `U-S-2` (the march comparator), and those landed. **T2 goes green on three
arms and one of them overshoots the referent for the first time in the run (ratio 1.0669 against
I-18's best 0.9047); T4b(b) fires for the first time ever; all three brackets are verdict-divergent,
so `U-S-2` is verdict-relevant on its first outing.** The knot leg is back in the determinism digest,
zero-diff ×2 on all three legs, 16/16. **Both of the conductor's structural pre-namings FAILED, and
so did one of mine — and the alignment I rejected on decode grades better than the one I adopted.
The pre-registration stands anyway.**

---

## 1 — ⚑ THE RECORD-CELL SCORECARD — EIGHT ARMS

Band references: **T1** wave 160 {159–161} · **T2** l4l 182.7167 ∈ [155.31, 210.12] · **T4a** 0.932 ± 0.02
· **T4b(b)** 1.6166 s · **T4b(c)** wave-160 kill from full health only (R-PM4-40 part 5).

| record cell (`cluster_defon__critlo__…`) | T1 | T2 | T4a | T4b(b) | T4b(c) | death | l4l s | **T2 ratio** | T4a | T3 MAE |
|---|:-:|:-:|:-:|:-:|:-:|---:|---:|---:|---:|---:|
| `COUPLED__PX-HI__NEAR` | ✗ | ✗ | **✓** | ✗ | ✗ | 152 | 35.1837 | 0.1926 | 0.9151 | 6.400 |
| `COUPLED__PX-HI__RING` | ✗ | ✗ | ✗ | ✗ | ✗ | 152 | 45.9592 | 0.2515 | 0.8841 | 8.032 |
| `COUPLED__PX-LO__NEAR` | ✗ | ✗ | **✓** | ✗ | ✗ | 152 | 51.6735 | 0.2828 | 0.9309 | 9.578 |
| `COUPLED__PX-LO__RING` | ✗ | ✗ | **✓** | ✗ | ✗ | 155 | 139.9184 | 0.7658 | 0.9176 | 12.444 |
| `DECOUPLED__PX-HI__NEAR` | ✗ | ✗ | ✗ | **✓** | ✗ | **154 ⚑** | 74.0408 | 0.4052 | 0.9548 | 8.925 |
| `DECOUPLED__PX-HI__RING` | ✗ | **✓** | ✗ | ✗ | ✗ | 155 | 166.2857 | 0.9101 | 0.9728 | 17.717 |
| ⚑ `DECOUPLED__PX-LO__NEAR` | ✗ | **✓** | ✗ | ✗ | ✗ | 156 | **194.9388** | **1.0669** | 0.9764 | 21.274 |
| `DECOUPLED__PX-LO__RING` | ✗ | **✓** | ✗ | ✗ | ✗ | 156 | 169.5510 | 0.9279 | 0.9654 | 12.825 |

### 1.1 What moved against I-18

| arm | l4l I-18 → I-19 | Δ | death I-18 → I-19 |
|---|---|---:|---|
| COU·PX-HI·NEAR | 155.3469 → 35.1837 | **−120.16** | 156 → 152 |
| COU·PX-HI·RING | 155.3469 → 45.9592 | −109.39 | 156 → 152 |
| COU·PX-LO·NEAR | 50.0408 → 51.6735 | +1.63 | 152 → 152 |
| COU·PX-LO·RING | 50.0408 → **139.9184** | **+89.88** | 152 → **155** |
| DEC·PX-HI·NEAR | 155.5102 → 74.0408 | −81.47 | 156 → 154 |
| DEC·PX-HI·RING | 155.5102 → 166.2857 | +10.78 | 156 → 155 |
| ⚑ DEC·PX-LO·NEAR | 165.3061 → **194.9388** | **+29.63** | 156 → 156 |
| DEC·PX-LO·RING | 165.3061 → 169.5510 | +4.24 | 156 → 156 |

> **⚑ THE FOLD IS NOT A UNIFORM IMPROVEMENT AND I AM NOT REPORTING IT AS ONE.** It moves l4l by
> −120 s on one arm and +90 s on another. **T2 count is 3/8 green, the same count as I-18's 3/4 —
> but the best ratio moves 0.9047 → 1.0669, i.e. the run has crossed the referent for the first
> time and now overshoots.** T1 gains nothing: **no arm reaches 159.**

### 1.2 ⚑ T2 AND T4a ARE NOW ANTI-CORRELATED, AND THAT IS A REGRESSION TO NAME

I-18's `COU·PX-HI` held **T2 and T4a together** (0.9123). **No I-19 arm holds both.** The three T2
greens all sit at T4a 0.965–0.976 (too healthy); the three T4a greens all sit at T2 ratio 0.19–0.77
(too short). The fold bought l4l by keeping the player alive at higher HP, which is exactly the
trade the referent does not make.

---

## 2 — ⚑ THE THREE BRACKETS — **ALL VERDICT-DIVERGENT, ALL DEFERRED**

Decided pairwise over matched record-cell pairs (the I-18 `bracket_of` indexed by arm NAME, which
three brackets over eight cells breaks; the pairwise form is **strictly stricter** and § 5 says so).

| bracket | matched pairs | divergent keys | designation |
|---|---:|---|---|
| `U-P-N-1` {COUPLED, DECOUPLED} | 4 | `T2_MET`, `T4a_MET` | **DEFERRED** |
| `px` {PX-LO, PX-HI} | 4 | `T2_MET`, `T4a_MET` | **DEFERRED** |
| ⚑ `U-S-2` {NEAR, RING} | 4 | `T2_MET`, `T4a_MET` | **DEFERRED** |

> **⚑ `U-S-2` IS VERDICT-RELEVANT ON ITS FIRST OUTING — NOT INERT.** `COU·PX-LO` flips from
> death@152 / ratio 0.2828 (NEAR) to death@155 / ratio 0.7658 (RING); `DEC·PX-HI` flips T2 from
> ✗ (0.4052) to ✓ (0.9101). **The march comparator the run has been carrying as a silent default
> since R-LOCO-6 is worth up to three waves and 0.48 of T2 ratio.**
>
> **AND IT IS NOT RESOLVED BY THAT.** R-PM4-27 part 3, pre-registered in the math note § 9 before
> any number existed: `U-S-2` resolves ONLY by a decoded `PatrolPoint_Attack`-to-player relation
> (`U-S-4`, DRM-blocked), **NEVER by which arm grades better.** RING grades better on the DECOUPLED
> COUPLED-PX-LO limbs and worse on `COU·PX-HI`; neither arm is the decoded truth — NEAR is maximal
> dispersion (11 destinations), RING maximal concentration (1), and the truth sits between.

`U-P-N-1` stays verdict-divergent, as it became at I-18. **Lap Q did not land during this fold, so
nothing was injected mid-run (NOTE-9 honored).**

---

## 3 — ⚑ THE PRE-REGISTERED PREDICTIONS, GRADED HONESTLY

### 3.1 STRUCTURAL — **0 of 3 clean, and the failures are the lap's real content**

**`S-1` — w154 collapses below 30 s (and the conductor's first pre-naming with it). ⚑ FAILED.**

| | I-18 | I-19 (reaching arms) | referent |
|---|---:|---:|---:|
| w154 span | **46.1224 s** | **40.9796 s** (DEC·PX-LO both arms, DEC·PX-HI·RING) · **36.9796 s** (COU·PX-LO·RING) | **14.20 s** |
| ratio | 3.267 | 2.886 / 2.604 | 1.0 |

The fold moves w154 by **−5.14 s**, not by −32. **The pet gate was a carrier, not THE carrier.**
My mechanism was right about the sign and badly short on magnitude — the fourth time in this run a
throughput walk has been right on sign and short on size (`T-1` at I-18 named exactly this habit).

⚑ **AND THE ISOLATION LIMB SAYS WHERE THE REST WENT:** `S-GATE-ONLY` (F-9 alone) gives w154 =
**33.9592 s** — a **−12.16 s** move. The FULL fold gives 40.98. **Adding the poll made w154 LONGER
than the gate fold alone**, because the earlier waves end earlier, the ladder arrives at 154 with a
different board and a different player, and the terms do not decompose. `P.7` predicted they would
sum to within a tick; they do not.

**`S-2` — ring-dry falls toward 0.199–0.206 (the conductor's second pre-naming). ⚑ FAILED, AND SO
DID MY OWN REPLACEMENT FOR IT — IN THE OTHER DIRECTION.**

| arm | I-18 defon | I-19 NEAR | I-19 RING | RING − NEAR | referent |
|---|---:|---:|---:|---:|---:|
| COU·PX-HI | 0.5531–0.5808 | 0.7146 | 0.6288 | **−0.0858** ✓ | 0.199–0.206 |
| COU·PX-LO | " | 0.5798 | 0.5933 | **+0.0135** ✗ (wrong sign) | " |
| DEC·PX-HI | " | 0.6461 | 0.5832 | **−0.0629** ✓ | " |
| DEC·PX-LO | " | 0.6252 | 0.6004 | −0.0248 ✗ (right sign, under 0.05) | " |

* I predicted NEAR ∈ **[0.35, 0.56]**. **Every NEAR arm is ABOVE 0.56** (0.5798–0.7146). **Dryness got
  WORSE, not better** — the falsifier I wrote for the conductor's version caught mine too.
* I predicted RING below NEAR by ≥ 0.05. **2 of 4 pairs pass; one has the wrong sign entirely.**
* Neither side reaches the referent band. **The convergence-target hypothesis is WEAKLY SUPPORTED at
  best and is NOT established.**

**`S-3` — the fold cannot move T2 much (l4l Δ < 25 s on arms surviving to the same wave). ⚑ FAILED.**
`DEC·PX-LO·NEAR` survives to 156 exactly as it did at I-18 and moves l4l **+29.63 s**. My own
falsifier fires. The poll term alone (`S-POLL-ONLY`) moves l4l **−3.10 s** against I-18's matched arm
(152.41 vs 155.51), which is inside my ±8 s sub-claim — **so the sub-claim survives and the headline
does not: the l4l move came from the GATE, not the heartbeat.**

### 3.2 POINT PREDICTIONS — **10 of 17 clean, 2 dead by my own arithmetic, 3 unevaluable**

| # | claim | result |
|---|---|---|
| P.1 | `law_3.moved == {}`, ≥ 12 witnesses | **PARTIAL** — `moved == {}` ✓, **11 witnesses** ✗. The shortfall is the witness list's, not a moved constant's; reported rather than rounded up |
| P.2 | fold-OFF EXACT ×6, exclusion scope ∅ | ✅ **EXACT 6/6**, scope `[]` |
| P.3 | determinism ×2 zero-diff on BOTH legs | ✅ **16/16 on ALL THREE legs** (surface, knots, joint) |
| P.4 | frozen `E-s09-cp150` pins intact | ✅ |
| P.5 | `wave_advance` ABSENT (not `None`) on fold-off rows | ✅ 0 rows carry the key |
| P.6 | `S-SUMMONS-GATE` reproduces I-18's w154 to the tick | ✅ **`46.122448979591844` EXACT**, l4l `155.5102` EXACT |
| P.7 | gate-only + poll-only spans sum to the full fold within a tick | ❌ **FAILED** — −12.16 + 0.90 ≠ −5.14; **the terms do not decompose** |
| P.8 | every fold wave ends on `run_tick ≡ 0 (mod 49)` | ❌ **FALSIFIED-BY-CONSTRUCTION** (`D-I19-6`) — 40 of 58; the period is 4/49, not 1/49 |
| P.9 | latency ∈ (0, 1.0] s, mean ∈ [0.35, 0.65] | ✅ **as written**: observed **0.0816 – 0.8980**, mean-of-means **0.5125**. (`P.9′`'s wider band was not needed — no cell reached it) |
| P.10 | `node_assignment` on every row, matching the arm | ✅ 8/8 cells single-valued and correct |
| P.11 | RING mean ∈ [30,37] m; NEAR ∈ [11,17] m | ✅ RING median **32.82** mean 29.51; NEAR median **12.67** mean 12.28 |
| P.12 | T4b(c) fires on no wave but 160 | ✅ fired nowhere |
| P.13 | `D-I18-4` like-for-like columns on 100 % of cells | ✅ 16/16, both quantities, both sides |
| P.14 | F-10 ramp evaluable on ≥ 6 of 10 waves | ❌ **2–6 of 10** — the ladders die before wave 157; only `DEC·PX-LO·RING` reaches 6 |
| P.15 | death wave ∈ {154..160} on ≥ 1 record arm | ✅ **five arms** (154/155/155/156/156) |
| P.16 | p05 ambush points take no patrol leg | ✅ (`AC-10.11`, unchanged) |
| P.17 | `S-RING-ONLY` moves w154 by < 2 s | ⚠️ **UNEVALUABLE** — `S-RING-ONLY` dies at 152 |

---

## 4 — ⚑ THE ISOLATION LIMBS, AND THE ONE THAT INDICTS MY OWN PRE-REGISTRATION

| limb | death | l4l s | ring-dry | w154 s |
|---|---:|---:|---:|---:|
| `S-SUMMONS-GATE` (both limbs off = I-18) | 156 | **155.5102** | 0.5601 | **46.1224 — EXACT to I-18** |
| `S-GATE-ONLY` (F-9 only) | 156 | 172.0816 | 0.6494 | 33.9592 |
| `S-POLL-ONLY` (F-8 only) | 156 | 152.4082 | 0.5388 | 47.0204 |
| `S-RING-ONLY` (U-S-2 RING, advance fold OFF) | **152** | 48.8980 | 0.6010 | unreached |
| ⚑ `S-POLL-WAVE-ALIGNED` (the alignment I REJECTED) | **156** | **181.2245** | 0.6505 | 35.0204 |

### 4.1 The gate and the arm INTERACT — they are not separable terms

`S-RING-ONLY` **kills the player at 152** (l4l 48.90) where the incumbent NEAR arm reached 156.
**RING alone is catastrophic; RING plus the folded gate reaches 155–156 and produces two of the three
T2 greens.** Any account that prices `U-S-2` as an additive term is wrong, and `P.7`'s failure is the
same fact seen from the w154 side.

### 4.2 ⚑ THE REJECTED ALIGNMENT GRADES BETTER, AND THE PRE-REGISTRATION STANDS

At the matched configuration (`DEC · PX-HI · NEAR`) the fold of record dies at **154** with
l4l **74.04**. The **wave-aligned** poll — the alignment the math note § 3 REJECTED on decode —
reaches **156** with l4l **181.22**. **That is +107 s of l4l and two whole waves, in favour of the
option I ruled out before the run.**

> **IT DOES NOT MOVE.** `Script.RegisterForUpdate` fires **once per event**, and `SpawnNext` is
> called **from inside an `Update`** (Lap S consequence A-5) — the timer is never re-registered at a
> wave boundary. That is a decoded property of the referent, and R-PM4-27 part 3's principle is not
> reserved for brackets: **a term fixed by decode may not be re-designated because the alternative
> scores better.** The 107 s is what the pre-registration cost, it is published here at full size,
> and it is the conductor's to rule on — not mine to quietly adopt.

---

## 5 — INSTRUMENTS: THE KNOT LEG, AND ONE STRICTER BRACKET

**⚑ `R-PM4-45 part 3` DISCHARGED.** The determinism digest hashes `_surface()` **and** the `r.movers`
knot polylines (`actor_id`-sorted, vertex-ordered, `repr()` floats, kind-tagged), plus a joint leg.
**All three zero-diff ×2 on all 16 primary cells.** Pre-named in the math note § 10 as instrument, so
it landed as instrument.

**The bracket comparator got stricter, and it had to.** I-18's `bracket_of` indexed the verdict map by
arm NAME, which works when two brackets over four cells make each arm one cell. **Three brackets over
eight cells breaks it** — `COUPLED` is now four cells, not one. `bracket_over` compares **matched
pairs** (every pair differing in exactly this axis, agreeing on the other two) and is divergent if
**any** pair disagrees on **any** key. Stated so nobody reads an I-19 collapse as the I-18 test passing.

---

## 6 — ⚑ THE FOLD-OFF PROOF AND THE FROZEN SUBSTRATE

| I-18 cell | recomputed fold-OFF digest | |
|---|---|---|
| `camp_defoff__critlo__COUPLED` | `723591794095abe226d6956470e8d8cce9f675ef309520a12419dbd477cc0dfa` | **EXACT** |
| `camp_defoff__critlo__DECOUPLED` | `b5e1fcf2f5d05ecd9daec458655cb09672a6b19041c2b62b05296862f47345b3` | **EXACT** |
| `cluster_defoff__critlo__COUPLED` | `d9824d9075dfc1061d4400c4f2417b7da79fc0e9a6c115361bff99a61e8f3d43` | **EXACT** |
| `cluster_defoff__critlo__DECOUPLED` | `6db2f698b29d31a873488a28290a92e682ad062cb006f498086b386927103c7a` | **EXACT** |
| `cluster_defon__critlo__COUPLED` | `d1698fc32ffb1150715b2ba9e2fce6bab5c8f7f22564b5b9cb2a7eaf8cf30e81` | **EXACT** |
| `cluster_defon__critlo__DECOUPLED` | `3bcf7c7fbb1864a1e2a13cf10ba7d6420a11b7130384ac8a345dea4a59ae42c6` | **EXACT** |

**Declared exclusion scope: `[]` — EMPTY, and the emptiness is the claim.** `wave_advance` is
ABSENT-not-None on every fold-off wave row (the thirteenth use). Frozen `E-s09-cp150` pins intact.
296 kc2 tests pass with **the same one pre-existing failure** recorded at I-18R
(`test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface` — `secondary_streams.py:136`).
**`export/` untouched** (star-lord's re-emission cell is seam-clean and parallel); the banked
`…145832` artifacts are unmodified.

---

## 7 — ⚑ DEFECTS, ALL SELF-CAUGHT, NONE REPAIRED MID-LAP (NOTE-9)

**`D-I19-6` — MY OWN TICK ARITHMETIC WAS WRONG AND MY OWN GUARD CAUGHT IT.**
Math note § 3 asserted *"period = 1/49 s, so 1.000 s = 49 ticks EXACTLY"*. False:
`ticks_per_s = 12.25`, `period = 4/49`, **1.000 s = 12.25 ticks and cannot be made whole.** I divided
I-18's w154 span by the wrong period and read the denominator back out as the answer.
`WaveAdvanceFold.ticks_per_poll` RAISED on the first execution with a message I had written before
the value was known. **The instrument built to stop a silently-rounded heartbeat stopped one, and the
person it stopped was me.** Addendum committed (`49e0d362`) **before** the repair, quoting the error;
`P.8` graded FALSIFIED-BY-CONSTRUCTION; `P.9`'s band graded **as written**. The repaired model — grid
in TIME, observed at tick granularity — is **more** faithful, because the referent's poll is a wall
clock with no relationship to this sim's channel rate.

**⚑ `D-I19-8` — THE DEFENCE AXIS OF THE RECORD MATRIX IS INERT, AND IT WAS INERT AT I-18 TOO.**
`cluster_defoff` and `cluster_defon` are **identical to the digit** on all four I-18 arms
(155.3469 / 50.0408 / 155.5102 / 165.3061, T4a 0.9123 / 0.9050 / 0.9599 / 0.9649) **and** on all four
matched I-19 arms. **One column of the run's matrix has been carrying no information for at least two
iterations.** Found by reading my own output rather than by a check; **reproduced, not repaired**
(it is not this fold's mechanism and repairing it would confound every column). **Routed.**

**`D-I19-7` — A NON-DEATH TERMINAL, AND IT IS A REAL CONSEQUENCE OF THE FOLD.**
`DEC · PX-HI · NEAR` terminates at wave 154 with `LocomotionInvariantError: player is 80.000 m from
the arena centroid, past the declared sane bound 80.0 m`. It is **not** a player death and is not
reported as one. The fold re-times every wave boundary, so the player enters 154 from a different
place; the seek policy then walks him to the bound. Reported as the terminal it is.

**`D-I19-3` — TWO DECODES OF ONE `.map` DISAGREE ON PATROL POINTS.**
Same file, same convention, same count (11), spawn points agreeing to **5.1e-4** — and the patrol
nodes differ by **0.45 – 13.28 m** (median 3.44), centroid **2.65 m** apart. Hypothesis (**not**
verified, deliberately): the sim's L-46 reader takes the head-section inline `Patrol Points` group,
Lap S's takes placement-array `patrolpoint_01.dbr` rows. Costs **< 6 %** on a 2.2× bracket; **cannot
flip it.** D-flagged, routed, **not repaired** — a substrate swap mid-fold would make I-18 unreachable.

**`D-I19-1` — the `45.06 m` in the commission chain is a BOUND, not a disc radius.** It is
`PLAYER_SANE_BOUND_M`'s comment. L-35's narrative (mine) and Lap S § 2.3 (legolas, from the
comparators the commission handed down) both read it as a distribution parameter. **R-PM4-46 part 1
corrected the narrative from SIZE to STRUCTURE; the structure was there too.**

**`D-I19-2` — the declared gap that survives, with its sign IN THE CODE.** F-7 gates on **all**
proxy-dispensed bodies; this sim gates on the **killable** ones (`D-I11-1` — one damage stream). A
literal F-7 makes waves 152/154/157 unendable. **The sim's gate is LOOSER, so its waves end EARLIER
than the referent's would on the same board.**

**`D-I19-4` — beacons (F-12) NOT folded, named as a SIGNED bias.** 5/arena, 0.36 m from the spawn
points, shipped comment *"accelerate monster movement in their spawn areas"*, magnitude
**UNREACHED-S2**. **No speed boost invented.** The sim prices the monster march near spawn **too
slow**, so arrivals are late and head-of-wave dry intervals are long — which pushes **against** the
ring-dry prediction on both arms and **hardest on RING**, whose marches are 2.5× longer. **This is a
live candidate explanation for `S-2`'s failure and it is named, not asserted.**

**`U-I19-1` — `placementExtents` as a SQUARE half-width.** The sim scatters `uniform(−8, +8)` per
axis (corner reach 11.31 m); Lap S describes an 8.0 m **disc**. The field name says *extents*; neither
reading is decoded. **Incumbent kept, undecided, named.**

**Jitter (`F-11`): ZERO LINES TOUCHED.** `C-I18-1` closed as fold-nothing (R-PM4-46 part 2).

---

## 8 — F-10 ARRIVAL RAMP, LIKE-FOR-LIKE — **THE SIM'S BOARD BUILDS 3–5× TOO SLOWLY**

Referent (Lap S § 3.4, living-nameplate counts, a lower bound): median **t→50 % 3.27 s**,
**t→90 % 4.97 s**. Sim counterpart is **arrived-and-alive** (`contact_t_s ≤ t ∧ alive`), never
spawned — the referent's frustum tops out at 11.08–11.64 m (V-B1), so a marching body has no plate.

| arm | n waves eval | median t→50 % | median t→90 % |
|---|---:|---:|---:|
| COU·PX-HI·NEAR | 2 | 5.80 | 6.49 |
| COU·PX-HI·RING | 2 | 10.20 | 10.24 |
| COU·PX-LO·NEAR | 2 | 7.80 | 11.55 |
| COU·PX-LO·RING | 5 | 15.02 | 18.04 |
| DEC·PX-HI·NEAR | 3 | 10.61 | 15.27 |
| DEC·PX-HI·RING | 5 | 16.73 | 20.98 |
| DEC·PX-LO·NEAR | 5 | 12.73 | 16.65 |
| DEC·PX-LO·RING | 6 | 15.39 | 18.08 |
| **referent** | 10 | **3.27** | **4.97** |

> **⚑ AND THE RING ARM IS SLOWER THAN NEAR ON EVERY MATCHED PAIR — pre-registered in the math note
> § 8 and CONFIRMED.** The board takes 5.8–16.7 s to reach half its peak against the referent's
> 3.27 s. **This is the strongest single signature the lap produced, it points at `D-I19-4`
> (unmodelled beacons) and at `U-S-4` (group-pathing), and it is a validation curve, never a target.**

`P.14` fails on evaluability (2–6 of 10) because the ladders die by 156 — **the ramp instrument is
starved by T1, not broken.**

---

## 9 — ⚑ `D-I18-4` LIKE-FOR-LIKE DRYNESS — **STANDARD FROM THIS FOLD**, 16/16 CELLS

Both quantities, both sides, on every cell (R-PM4-46 part 3 (g)). Record arms:

| arm | ring-occupancy dryness (ref **0.1989–0.2063**) | damage-landed dryness (ref **0.1653**) |
|---|---:|---:|
| COU·PX-HI·NEAR / RING | 0.7146 / 0.6288 | 0.5684 / 0.5204 |
| COU·PX-LO·NEAR / RING | 0.5798 / 0.5933 | 0.4976 / 0.5163 |
| DEC·PX-HI·NEAR / RING | 0.6461 / 0.5832 | 0.5039 / 0.5179 |
| DEC·PX-LO·NEAR / RING | 0.6252 / 0.6004 | 0.5611 / 0.5330 |

**Both quantities got worse than I-18** (ring 0.5531–0.5808 → 0.5798–0.7146; damage-landed 0.48–0.51 →
0.4976–0.5684). The run's dry-shape residual is **not** addressed by this fold and is now the largest
open gap on the board after T1.

---

## 10 — ⚑ THE ADVANCE RULE AS MEASURED

* Latency observed **0.0816 – 0.8980 s**, mean-of-means **0.5125 s** — inside the decoded `(0, 1]`
  on **58 of 58 gated waves**, mean inside the pre-registered `[0.35, 0.65]`.
* **Gate re-openings: 0** across every cell (published even though expected zero — an instrument that
  only reports when surprised cannot be trusted when it is not).
* **Killable summons freed from the gate:** the fold's effect size, per cell, on the wire
  (`⚑ killable_summons_that_would_have_gated`) — these are exactly the bodies the incumbent gate was
  still waiting on. `S-SUMMONS-GATE` runs the incumbent so the two are differenceable, and it
  reproduces I-18 **to the seventeenth digit**.

---

## 11 — DIGESTS (FULL 64 hex, GL-6)

**Findings:** `59c6c85befdb4294e9b51e2353ffa6786e40bb4dfb61b33a2eb5fde8702d13e9`

**Record-cell determinism, pass 1 = pass 2 on all three legs:**

| arm | `surface` | `knots` |
|---|---|---|
| COU·PX-HI·NEAR | `d4ae4b6e0fec13a439a5ac25350c3fb365482c810446b2e79c891157cb08cbd2` | `1c2b5dfe657f8b6a8a4d0107c1c4091bdb03e5627b00fb497fafb42a3917ec44` |
| COU·PX-HI·RING | `e30286104d65de05e6825476c141d2e78c4653b182436a783e7ca471ce582a13` | `5736d46071500426b4bfbd3297ae2299ea3f6dc079bed450e30b52bfcd7ae670` |
| COU·PX-LO·NEAR | `e939394429d3f9e04bba5e4dd8b1d944e1b979ad896f439316398a6f7c2a586f` | `ae87e9d7ed56d661ec2c70a08be2d9d93695c01e18111e57e28e402c40a3b7b9` |
| COU·PX-LO·RING | `d375d26efa13cf514bb3a32d30ff3a0f9b55e5cb2c8d2bcaa2c6cb882a77f6f4` | `0fb03af214c9232a7075800055fa066e6d6f1fff49b84ff94b06f0c50d170b71` |
| DEC·PX-HI·NEAR | `852880da6c99df4461a6e12c0dfb79acff8d34ea1300790232b054c0e861567f` | `366cc6cf156b2d750e014a11bfbc9d02005e7d2c3d4cd2e69740f61066b0f26d` |
| DEC·PX-HI·RING | `4296898e993b1aff833a3ce0d4b9691219ecba1e737d13e4041cade1b0f3a14a` | `c5b8c380399268685cba32148a7b77a9febc3e3a94b42c0f018989a32eee0f80` |
| ⚑ DEC·PX-LO·NEAR | `630678be06f938262e68d87650fb70d6776d40a840a74a9cdaf49ee2fbe1080f` | `7f2ac55963cc90948c47f30832869f815bf183464987887618b91a5ee9d4916d` |
| DEC·PX-LO·RING | `3c873accd1f789df8a4a67e6e823ab78af5b672b61e09e9d82318a6386d26af6` | `d6f3c7fde6d2a22b2fa0bd871a8ccbe46511dc3b1f3521e76000651c53886769` |

---

## 12 — `U-S-1` PER-ARENA SENSITIVITY — **SIDE TABLE, NEVER MATRIX ARMS**

Which arena Matt played is `UNREACHED-S3`. Legolas published all twenty and imposed none; the sim's
declared selection is `sm1/survivalworld_a` (L-46, **forced** by tier-16 p01 availability, not chosen
by fit). The pooled spread the declaration sits inside, recomputed here from Lap S's rows:

| comparator | min | median | max |
|---|---:|---:|---:|
| spawn → patrol centroid, per-arena median (**RING**) | 29.72 | **37.39** | 44.07 |
| spawn → nearest patrol, per-arena median (**NEAR**) | 6.57 | **17.20** | 22.82 |

The sim's own arena gives RING 32.82 / NEAR 12.67 — **inside both spreads, on the low side of both.**
**Reported as sensitivity. Not folded. Not carried as arms** (R-PM4-46 part 3 (b), verbatim).

---

## 13 — TO THE CONDUCTOR

1. **Both of your structural pre-namings failed.** w154 moved −5.14 s, not to 14.20; ring-dry rose,
   it did not fall. **The mechanisms are named** — the pet gate carried only part of w154 (`S-GATE-ONLY`
   isolates −12.16 s and the terms do not decompose), and `D-I19-4`'s unmodelled beacons plus
   `U-S-4`'s group-pathing are the standing candidates for the dry shape.
2. **`U-S-2` is verdict-relevant on its first outing and is DEFERRED, not resolved.** Worth up to
   three waves and 0.48 of T2 ratio. It resolves only by a decoded `PatrolPoint_Attack`-to-player
   relation — which `UNREACHED-S1`'s DRM blocker also blocks.
3. **The rejected poll alignment grades better by two waves and 107 s of l4l.** I did not adopt it.
   **That is your call to make and I have priced it in full rather than burying it.**
4. **`D-I19-8` is the one I would spend the next lap on.** The defence axis of the record matrix has
   been inert since at least I-18. Four cells of every matrix have been duplicates.
5. **`D-I19-6` is mine and it is on the record before the repair, not after.**
6. **Nothing in `export/` was touched.** Star-lord's parallel cell is seam-clean.
7. **Push is yours** (CL-10). Engine `654ec016..04443f26`, three commits, the first two zero-code.
