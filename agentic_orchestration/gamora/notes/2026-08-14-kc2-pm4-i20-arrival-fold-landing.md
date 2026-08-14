# KC2-PM4 · I-20 — THE ARRIVAL FOLD — LANDING NOTE

**Agent:** gamora · **Conductor:** gandalf (RUN-CONDUCTOR) · **2026-08-14**
**Commission:** `R-PM4-51 part 5` (pre-chartered `R-PM4-49 part 6`), ledger `L-42`.
**Evidence:** legolas **Lap T**, meta `de9de38e`. All five consumed inputs re-hashed **EXACT**
before any instrument ran (GL-6) — see § 11.

**Commits (engine, mine, three, math-note-only FIRST):**
`280f3c9d` math note (zero code) → `aebdb228` math-note **ADDENDUM**, `D-I20-3` + `D-I20-4`
committed **before** the repairs they describe (zero code) → `42f090e4` the fold + driver +
findings + MIGRATION.

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i20-findings-20260814_174154.json`
sha256 **`dd1d5f905b9bab3a7327d3a6425469f5425da842d626268f81edb40404c63039`**. Wall **18.1 s**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**`U-S-2` is decoded, folded, and MEASURED INERT to the seventeenth digit — and the decode-true
march rate that rode in beside it kills the player on wave 151, the worst T1 the run has produced.**
The isolation limbs make the attribution exact rather than argued: `S-CYCLIC-ONLY` reproduces the
I-19 baseline at l4l **35.183673469387756**, delta **0.0**, while **35 index advances fire and not
one body ever walks a second patrol leg**; `S-MARCH-ONLY` reproduces the wave-151 death exactly.
**The march limb carries the entire effect, and its mechanism is this run's own sustain finding
running backwards** — I-9/I-17 established sustain-through-throughput, so a 19.8–23.6 % slower board
is a drier disc (ring dryness 0.7146 → 0.9308) is less leech, and 20 005 HP is gone in 12.98 s of
wave 151. **The commission's geometry limb folded nothing, and I measured that before I believed the
commission for the fourth time in this run: the CSV I was told to sample is mislabelled, Lap T's own
arithmetic used the right set, and the sim already held it at 5.4e-5 m.**

---

## 1 — ⚑ THE RECORD-CELL SCORECARD — TWO ARMS

Band references: **T1** wave 160 {159–161} · **T2** l4l 182.7167 ∈ [155.31, 210.12] ·
**T4a** 0.932 ± 0.02 · **T4b(b)** 1.6166 s · **T4b(c)** wave-160 kill from full health only.

| record cell (`cluster_defon__critlo__COUPLED__…`) | T1 | T2 | T4a | T4b(b) | T4b(c) | death | l4l s | **T2 ratio** | T4a | T3 MAE |
|---|:-:|:-:|:-:|:-:|:-:|---:|---:|---:|---:|---:|
| `PX-LO` | ✗ | ✗ | ✗ | ✗ | ✗ | **151** | 10.0408 | **0.0550** | 0.8256 | 6.226 |
| `PX-HI` | ✗ | ✗ | ✗ | ✗ | ✗ | **151** | 12.9796 | **0.0710** | 0.8667 | 3.287 |

**The `px` bracket COLLAPSED** — both arms agree on every verdict key, zero divergent keys. First
collapse of the px bracket in the run.

### 1.1 ⚑ AGAINST THE HONEST INCUMBENT, NOT THE RETIRED ONE

I pinned this in the math note § 8 **before the run**, so the landing could not borrow a dead arm's
number: I-19's best COUPLED cell was `COU·PX-LO·**RING**` at ratio 0.7658, and **`RING` no longer
exists** under the Lap T resolution. The honest comparator is I-19's `NEAR` arms.

| arm | l4l I-19 NEAR → I-20 | Δ | death I-19 → I-20 |
|---|---|---:|---|
| `COU·PX-LO` | 51.6735 → **10.0408** | **−41.63** | 152 → **151** |
| `COU·PX-HI` | 35.1837 → **12.9796** | **−22.20** | 152 → **151** |

> **⚑ THIS IS A REGRESSION AND I AM REPORTING IT AS ONE.** Every band moves the wrong way. T4a was
> MET on I-19's `COU·PX-LO·NEAR` (0.9309) and is now 0.8256. **Nothing was adjusted in response.**
> `R-PM4-29`, verbatim: *the direction of a correction is not its justification.*

### 1.2 ⚑ AND THE FOLD IS SPECTACULAR ON THE FAMILY THAT IS NOT THE RECORD

`S-DECOUPLED` — the full fold on the `DECOUPLED` continuity control at `PX-HI` — reaches **wave 156**
with **l4l 195.5102**, a **T2 ratio of 1.0700, comfortably inside [0.85, 1.15]**. Its I-19
counterpart (`DEC·PX-HI·NEAR`) was **74.0408**. **The same fold that costs the record family 22–42 s
buys the continuity family 121 s.**

**It is not designated and it is not a record claim.** `R-PM4-48 part 2` ruled COUPLED on decode, and
`R-PM4-27 part 3` is not reserved for brackets: **a family fixed by decode may not be re-designated
because the alternative scores better.** This is the second time in two iterations that the greens
have landed on the family the run does not carry, it is published at full size, and it is the
conductor's to rule on — not mine to quietly adopt.

---

## 2 — ⚑ COMMISSION-PREMISE CORRECTION #4: THE CSV I WAS TOLD TO SAMPLE IS MISLABELLED

The commission's fold basis (b): *"first-march distances SAMPLED from corrected
`pm4t_map_placements_v2.csv` ROWS per spawn point."* I measured the file before consuming it. Every
number below is **recomputed by the driver at run time** (`⚑ geometry_agreement_v2`), never quoted.

| measurement | result |
|---|---|
| (a) sim's 11 nodes vs rows **labelled** `patrolpoint_01.dbr` | **0.4484 / 3.4420 / 13.2803 m** (min/med/max) |
| (b) sim's 11 nodes vs the **GUID-bearing** rows | **7e-6 / 4.3e-5 / 5.4e-5 m** — *the same points* |
| (c) GUID row at file index (patrol row **+ 1**) | **20 of 20 arenas** |
| (d) F-4 recomputed on the labelled set | 16.7308 |
| (d) F-4 recomputed on the GUID/head set | **16.7992** |
| (d) **Lap T published** | **16.7992** |
| (e) six spawn placements, sim vs v2 | max **5.14e-4 m** (unchanged from I-19) |

**Reading:** the `dbr` column is displaced by one record across GUID-bearing (72-byte) placements.
The tell is that one of `survivalworld_a`'s eleven GUID rows is labelled
**`records/scriptentities/playerspawnpoint.dbr`** — inside a `Patrol Points` group.

**⚑ AND THE VERDICT CUTS IN LAP T'S FAVOUR.** F-4 on the GUID set reproduces Lap T's published
16.7992 to four decimals; the labelled set does not. **Legolas's own arithmetic used the correct
point set and its headlines STAND.** What is false is `R-PM4-51 part 3`'s *stated basis* — the two
point sets have not converged, the labels moved. **`D-I19-3`'s verdict (the sim's reader is right) is
confirmed and strengthened; its basis is not.**

**Consequence for the fold:** the sim's nodes **are** the GUID/head set at 5.4e-5 m, and
`pm4t_geometry_corrected.csv`'s row for `survivalmode1/survivalworld_a.map` reads
`to_nearest_patrol_m = 12.6718` / `to_patrol_centroid_m = 32.8201` — **the same digits the sim
emitted at I-19 § 12.** So limb (b) folds **nothing**, and sampling the CSV by label would have
replaced a verified geometry with a mislabelled one. **Refused by name.** `D-I20-1` / `D-I20-2`
filed, **not repaired** (NOTE-9); legolas's artifacts are untouched.

---

## 3 — ⚑ FIT LAW ON `D-PDEF-1`: THE PARAMETER IS NOT MINE TO DELETE

`R-PM4-50 part 4` commissioned the removal of `simulate_wave`'s `defenses_enabled` on P-DEF's
measurement of **0 AST loads**. That measurement is **correct** — and *"dead inside the callee"* is
not *"dead"*:

* `export/kc2_run_adapter.py:686` — it is star-lord's `RunSpec` **field**;
* `:2720` — **`if spec.defenses_enabled:` is what CONSTRUCTS `field_obj`.** It is the live defence
  selector one level up;
* `:4105` / `:4112` — it gates a schema-declaration branch; **24 uses in `export/`** in total, plus
  **17** of this run's own driver scripts.

**Removing it breaks a seam I do not own** (ADR-004 puts a public-signature break behind a MIGRATION
and star-lord's ruling, not behind an instrument commission). What landed instead:

1. the dead signature **quoted verbatim** in the math note § 6.1 (Discipline #12 discharged);
2. the disposition documented at the parameter's own site in `run.py`;
3. **`waves[].patrol.⚑ defence_wiring`** — the `defenses_enabled` / `defence_field` pair censused on
   every folded wave, so *"a switch that is not a switch"* is visible in every artifact rather than
   only in a probe. Both record cells report `⚑ consistent: true`;
4. a **removal proposal** filed in `MIGRATION.md` for star-lord, with the honest shape named: the
   `RunSpec` keeps its selector and the adapter simply stops forwarding it — a change entirely
   inside `export/`, no simulation-seam edit required.

**Nothing in `export/` was touched.**

`D-PDEF-3` **LANDED** in full: the sane bound is now measured on **both** actors. The player arm is
**unchanged in value and in raise behaviour** (so no banked terminal moves); the board arm **counts
and does not raise**, because `D-PDEF-2` (containment needs decoded arena walls, `UNREACHED-S8`) is
an honest model gap and a raise would dress it as a difficulty signal. Bound trips carry
`⚑ terminal_class: INSTRUMENT`. On both record cells the board census reports **0 bodies beyond
80 m** (max 25.88 / 28.13 m) — the ladders die too early to reach the envelope.

---

## 4 — ⚑ THE ISOLATION LIMBS — THE ATTRIBUTION IS EXACT, NOT ARGUED

| limb | death | l4l s | ring-dry | index advances | **2nd legs** | march base |
|---|---:|---:|---:|---:|---:|---:|
| `S-I19-BASELINE` (both limbs off) | 152 | **35.183673469387756** | 0.7146 | 0 | 0 | — |
| ⚑ `S-CYCLIC-ONLY` | **152** | **35.183673469387756** | **0.7146** | 35 | **0** | 4.0 |
| ⚑ `S-MARCH-ONLY` | **151** | **12.9796** | **0.9308** | 0 | 0 | 3.055412 |
| `S-DECOUPLED` (full fold) | **156** | **195.5102** | 0.6146 | 100 | 3 | 3.055412 |
| `S-RAMP-I19-DEC` (fold off, I-19's DEC arm) | 156 | **194.9387755102041** | 0.6252 | 0 | 0 | — |

**Two exact continuity reproductions**, both to the seventeenth digit against I-19's *findings JSON*
(not its prose): `S-I19-BASELINE` ≡ I-19 `COU·PX-HI·NEAR` **35.183673469387756**, and
`S-RAMP-I19-DEC` ≡ I-19 `DEC·PX-LO·NEAR` **194.9387755102041**. `P.6` PASSES.

**`S-CYCLIC-ONLY` is byte-for-byte the baseline while 35 advances fire.** The decoded traversal rule
is folded, correct, and **does nothing on this board** — which § 1.5 of the math note predicted from
the roster's own numbers before the run.

---

## 5 — ⚑ THE PRE-REGISTERED PREDICTIONS, GRADED HONESTLY

### 5.1 STRUCTURAL — 1 of 3 clean, and the two failures are the lap's real content

**`S-1` — the cyclic limb is nearly inert; the march rate carries the fold. ⚑ PASSED, all three
clauses, and more sharply than predicted.**

| clause | predicted | measured |
|---|---|---|
| bodies walking a **second** patrol leg | < 20 % | **0.0 %** (0 of 24) |
| \|Δl4l\| `S-CYCLIC-ONLY` vs baseline | < 8.0 s | **0.0 s — EXACT** |
| `S-MARCH-ONLY` \|Δl4l\| exceeds `S-CYCLIC-ONLY`'s | yes | **22.204 vs 0.000** |

**`S-2` — the like-for-like ramp closes most of I-19's 3–5× gap. ⚑ FAILED ON SIZE, CONFIRMED ON
SHAPE, AND THE FAILURE IS THE MORE USEFUL HALF.**

Tested the strongest possible way: **one run, two functionals** (`S-RAMP-I19-DEC` = I-19's
`DEC·PX-LO·NEAR` arm; its cumulative median reproduces I-19's published **12.734693877551022**
exactly, so the two readings share a trajectory set with no fold between them).

| | median `t→50 %` |
|---|---:|
| I-19 cumulative form | **12.7347 s** |
| ⚑ living-window form (11.64 m) | **9.7551 s** |
| referent (F-10) | **3.27 s** |

* **ratio 0.766 — I predicted below 0.60. FAILED as written.**
* Shape: **non-monotone on 5 of 6** evaluable waves, **draining to ≤ half peak on 5 of 6** — the
  referent's own peak-and-drain signature, reproduced. I predicted "≥ 7 of 10"; only 6 waves are
  reachable, so **the clause fails on its own arithmetic** and I grade it failed rather than
  rescaling it after the fact.
* ⚑ **THE FINDING: the functional mismatch was REAL and was NOT the carrier.** The repair closes
  **23.4 %** of the gap. The sim's board still builds **2.98×** too slowly, down from 3.89×.
  **I-19's headline survives its own repair, and the residual is still an arrival residual.**

**`S-3` — the march slowdown costs T2; l4l RISES and dryness worsens. ⚑ FAILED, BY MY OWN
FALSIFIER, IN THE DIRECTION I WROTE THE FALSIFIER FOR.**

| clause | predicted | measured |
|---|---|---|
| l4l rises > 10 s on ≥ 1 cell | RISE | **FALLS 41.63 / 22.20 s** ✗ |
| ring dryness worsens on both | rise | **0.7146 → 0.9308** ✓ |

My falsifier was *"l4l falls on either cell ⇒ the slower board is not simply a drier one and the
arrival term interacts with the advance gate in a way I have not named."* **It fires.** I reasoned
that slower arrivals lengthen waves and therefore l4l; what actually happens is that the player
*dies* before the lengthening can be banked. **I had the sign of the throughput term right and
missed that it is load-bearing for survival, not just for pacing** — the fifth time in this run a
throughput walk has been right on sign and wrong on consequence.

### 5.2 POINT PREDICTIONS — 13 of 17 clean, 2 failed, 2 defect-adjusted

| # | claim | result |
|---|---|---|
| P.1 | `law_3.moved == {}`, **13** witnesses | ✅ **`{}` on 13** — `V_REF_M_PER_S` 4.0 and the patrol modulus 11 both UNMOVED |
| P.2 | fold-OFF EXACT ×6, scope ∅ | ✅ **6/6 EXACT**, scope `[]` |
| P.3 | determinism ×2 zero-diff, three legs | ✅ **6/6** (surface, knots, joint × 2 cells) |
| P.4 | frozen `E-s09-cp150` 20/20 | ✅ |
| P.5 | `patrol` key ABSENT on fold-off rows | ✅ 0 rows carry it |
| P.6 | `S-I19-BASELINE` reproduces I-19 to the digit | ✅ **35.183673469387756, delta 0.0**, death 152 — *after* `D-I20-5` re-pinned the check to the artifact instead of the prose |
| P.7 | ⚑ `ALL_ARMS_ZERO_REACH` | ✅ **TRUE** — see § 6 |
| P.8 | 3D ≡ 2D argmin on actual scattered spawns | ✅ **24/24, 100 %** (vertical spread 0.7388 m) |
| P.9 | sim nodes ≤ 1e-3 m from GUID set, > 1 m from labelled | ✅ **5.4e-5 m** vs **13.28 m** |
| P.10 | player rate bit-identical across the march fold | ✅ **by two instruments** — AST census (5 loads of `march_base`, **zero in a player statement**) and `max_seek_step == measured_speed × period` EXACTLY on both cells. ⚑ The *first* instrument was wrong (`D-I20-6`) |
| P.11 | entry march ∈ [3.9, 4.8] s at PX-LO | ❌ **FAILED — median 7.99 s** (march 16.08 m). I multiplied two centres (emitter distance × pooled-median speed); the median of the ratio is not the ratio of the medians, and bodies scatter up to 8 m first |
| P.12 | T4b(c) fires on no wave but 160 | ✅ fired nowhere |
| P.13 | `D-I18-4` like-for-like on 100 % of cells | ✅ both quantities, both sides |
| P.14 | ≥ 1 body beyond `PLAYER_SANE_BOUND_M` | ❌ **FAILED — 0 bodies** (max 25.88 / 28.13 m). The ladders die at 151; the board never gets the waves it needs to walk out. **The instrument is starved by T1, not broken** — P-DEF's 6-of-8 arms ran to 154–156 |
| P.15 | death wave ∈ {152…160} on ≥ 1 record cell | ❌ **FAILED — both at 151**, below the band's floor. Predicted before the run and missed low |
| P.16 | `n_jitter_applied == 0`, no beacon speed term | ✅ 0; `BEACON_DISPOSITION` folds nothing |
| P.17 | 296 pass, 1 pre-existing failure | ✅ **296 passed, 1 failed** (`test_AC_10_10_…`, `secondary_streams.py:136`) — unchanged since I-18 |
| P.18 | *(added by the addendum, flagged post-hoc)* `S-CYCLIC-ONLY` ≡ baseline after the `D-I20-3` repair | ✅ **delta 0.0** — the repair is instrument-only, proved |

---

## 6 — ⚑ THE PRUNING TRIPWIRE — IT HOLDS, AND IT IS ON THE WIRE

`R-PM4-50 part 2` requires the reach census as a standing assert-wall check on every arm.

| record cell | multiplier PRODUCED ≠ 1 | multiplier **CONSUMED** ≠ 1 | `ZERO_REACH` |
|---|---:|---:|:-:|
| `COUPLED·PX-LO` | 6 | **0** | ✅ |
| `COUPLED·PX-HI` | 6 | **0** | ✅ |

**`ALL_ARMS_ZERO_REACH = True`.** The banner's ×2 is PRODUCED six times and CONSUMED zero — P-DEF's
`A′ · INERT BY REACH` mechanism reproduced exactly under a fold that changes every arrival time.
**The defence axis stays pruned.** ⚑ Lap T was named the likeliest un-pruner in the run and it did
not un-prune: the record ladders die on wave 151, so the board has less opportunity to reach the
player inside the aura, not more.

---

## 7 — ⚑ DEFECTS, ALL SELF-CAUGHT, THE ADDENDUM COMMITTED **BEFORE** THE REPAIRS

**`D-I20-1` — the v2 CSV's `dbr` column is displaced by one record across GUID-bearing placements.**
Lap T's headline statistics are UNAFFECTED (they used the GUID/head set); the trap is for downstream
consumers, and the commission instructed me to be exactly that consumer. Two causes named, **neither
verified** (NOTE-9): the reader consumes the string index one record early on 72-byte records, **or**
the level format pairs each `patrolpoint_01` controller with a separate GUID-bearing anchor. **The
operational conclusion is identical under both.** Routed.

**`D-I20-2` — `R-PM4-51 part 3`'s stated basis for closing `D-I19-3` does not survive
re-measurement.** The verdict is confirmed; the basis is not. Filed so the ledger's own arithmetic
is auditable, **not** to reopen the verdict.

**⚑ `D-I20-3` — MY COUNTER DID NOT MEASURE WHAT MY OWN PREDICTION SAYS, AND MY OWN ISOLATION LIMB
CAUGHT IT.** `S-1` predicts *"fewer than 20 % of bodies ever take a **second** patrol leg"*; its
parenthetical operationalised that as `n_patrol_legs ≥ 1`, which the **entry arrival already
satisfies**. The first build reported **91.7 %** where the quantity `S-1` names is **0.0 %**. The
contradiction that exposed it was two emitted numbers that could not both be true: `S-CYCLIC-ONLY`
reproducing the baseline **to the seventeenth digit** while claiming the board cycled. A direct
wrapper on `Mover.step` then returned `{'total': 35, 'while_gate_open': 0, 'first': 35}` — and that
**also priced the `U-T-1` Patrol-vs-Pursue caveat at ZERO on this board**, measured: not one advance
ever fired from the Pursue state. Repair is instrument-only (`n_patrol_legs_after_entry`);
**addendum committed at `aebdb228` before the repair, quoting the error.** `S-1` is graded against
what § 9 *said*, and the parenthetical is named as my drafting error rather than read as the claim.

**⚑ `D-I20-4` — `⚑ terminal_class` LEAKED INTO THE COMPARED SURFACE AND TURNED ALL SIX FOLD-OFF
CELLS RED ON FIRST EXECUTION.** One-line diff: `.terminal.⚑ terminal_class: absent on the LEFT`.
**The instrument built to prove this iteration changed nothing it did not mean to was broken by an
instrument this iteration added** — the same class of defect I-4 filed, re-made by me. The class
moved to `state`; **the exclusion scope stayed EMPTY, because no key was excused — the key moved.**

**`D-I20-5` — a continuity check pinned to prose instead of to the artifact.** `P.6` compared against
the 4-dp literal `35.1837` from I-19's *landing note* and failed by 2.65e-5 on an EXACT reproduction.
Re-pinned to I-19's findings JSON. **A continuity check must be pinned to the artifact, not to the
sentence about it.**

**`D-I20-6` — my first `P.10` instrument was dash-blind.** It measured the player's largest per-tick
displacement and read **11.83 m / 144.9 m/s** — not a leak, the **MEASURED dash layer** (P-DEF:
largest gap 15.995 m = `Violent Delights`' measured 16.0 m; I measured 15.687 m here). A max-step
statistic over a path containing discrete dashes cannot see a 20 % change in the run rate. Replaced
with P-DEF's own AST method turned on my own limb, plus a dash-aware step census.

**`D-I19-2` / `U-I19-1` / `D-PDEF-2` carried, unchanged.** `D-I19-4` **RETIRED** — Lap T closed the
beacon measured-negative and this fold sources no term to it.

---

## 8 — THE FOLD-OFF PROOF, DETERMINISM, AND THE FROZEN SUBSTRATE

**Fold-OFF byte identity: EXACT 6/6** against the I-18/I-19 pinned surface digests
(`camp_defoff`/`cluster_defoff`/`cluster_defon` × COUPLED/DECOUPLED). **Declared exclusion scope:
`[]` — EMPTY, and the emptiness is the claim.** `patrol` is ABSENT-not-`None` on every fold-off wave
row (the fourteenth use). Frozen `E-s09-cp150` **20/20**. **`export/` untouched.**

**Determinism ×2, pass 1 ≡ pass 2 on all three legs, 6/6:**

| cell | `surface` | `knots` |
|---|---|---|
| `COUPLED·PX-LO` | `8eff6c159e4fe8d319449128e3d5fe5673960da1bfd3b498944b1d5c40b48073` | `a0058007c68a5a2a3a396241b157cbb61765d944b834553aa6b374de142eb43a` |
| `COUPLED·PX-HI` | `d3783c5595cca6fbb8b30b53f777fd1cec35469f0dc06279a4c008ea047e9d87` | `06ac76d67cacd7e73ee6fe46dd1d9dd6e89ad89801e62207cd5e7a0e325e7bd1` |

`joint`: `adfd1bea0a42a6e18ebbf7fc49519c7aea7308c6a26013e96574f96c3ec778b6` (PX-LO) ·
`937ff2e6f4ccc2768baf1e658e059c8ec473ebdef520604ab2f2c790ab2599d8` (PX-HI).

---

## 9 — WHAT FOLDED, AND WHAT REFUSED TO

**Folded:** nearest-ENTRY + `(i+1) mod n` cyclic traversal (`0x105230` / `0x0d2710` / `0x1057b0`),
with the traversal **order** decode-sourced from the sim's own head-section `idx` column — `(i+1) mod
n` needs an index and the file supplies it. The march base `v_ref = 4.0` → Route-2 K per px arm
(**PX-LO 3.209466 / PX-HI 3.055412**, the mapping **read** from `pm4t_march_pricing.json`, never
invented — PX-LO is the *faster* monster and the constant's own site says so). Grade
**INFERRED-WITH-EVIDENCE**; `UNREACHED-T1` named. **Two new constants, neither with a free digit.**

**Refused / not folded:** beacons (`UNREACHED-S2` measured-negative — 23 run-speed slots all zero;
`D-I19-4` retired) · first-march distances from the v2 CSV (§ 2) · `characterRunSpeedJitter`
(`C-I18-1`, 0 applied) · monster containment (`D-PDEF-2`) · `U-T-3` · `U-T-4`'s 8.2 % transient
minority · `defenses_enabled` removal (§ 3).

**`U-T-1` carried explicitly with no arm added**, as commissioned — and then **priced at zero by
measurement** (`D-I20-3`, § 7): 0 of 35 advances fired from the Pursue state.

---

## 10 — TO THE CONDUCTOR

1. **The fold is decode-true and the sim grades worse for it — for the second iteration running.**
   T1 152 → **151** on both record cells. The mechanism is named and isolated: `S-MARCH-ONLY`
   reproduces it, `S-CYCLIC-ONLY` is inert to the digit.
2. **⚑ `U-S-2` cost the run nothing and bought it nothing.** It was worth up to three waves and 0.48
   of T2 ratio *as a bracket* at I-19; **decoded, it is exactly inert.** The three-wave spread was
   the RING arm's error, not the rule's information.
3. **⚑ The DECOUPLED family hits T2 at ratio 1.0700, wave 156, under the full fold.** Not
   designated. Second iteration in a row where the greens land off the record family. **Yours to
   rule on; priced at full size rather than buried.**
4. **`U-T-2` is a partial negative and I report it as one.** The like-for-like repair moves
   `t→50 %` 12.73 → 9.76 s, closing 23.4 %. **The sim is still 2.98× the referent.** I-19's arrival
   headline survives its own repair, and arrival is still the residual.
5. **`D-PDEF-1` could not be discharged as written and the reason is in `export/`, not in my
   judgement.** The MIGRATION entry names the shape that would work and needs star-lord's ruling.
6. **The reach tripwire held** — `ALL_ARMS_ZERO_REACH` true, defence axis stays pruned, and the
   census is on the wire so the next lap inherits it automatically.
7. **`D-I20-1` is the one I would spend attention on.** A banked artifact contains a systematic
   label displacement that a downstream consumer will hit, and the commission walked straight into
   it. Lap T's numbers are fine; the CSV's `dbr` column is not.
8. **Push is yours** (CL-10). Engine `280f3c9d..42f090e4`, three commits, the first two zero-code.

---

## 11 — DIGESTS (FULL 64 hex, GL-6)

**Findings:** `dd1d5f905b9bab3a7327d3a6425469f5425da842d626268f81edb40404c63039`

**Lap T inputs, re-hashed EXACT before any instrument ran:**

| artifact | sha256 |
|---|---|
| `pm4t_findings.md` | `de80588a3ae922c6ee7b3ccd3ec2bc901da69fba99efc35ac3f52ef1625b2b4b` |
| `pm4t_march_pricing.csv` | `bb247a48a6041f20170ae7d39a1f8f3bf847a2bcda55dcafcf98d68601f37296` |
| `pm4t_map_placements_v2.csv` | `96306ed09a08ebd8aad6b5b65f953960cd47ecf78930ce490b013e37aac08820` |
| `pm4t_geometry_corrected.csv` | `549842a11bf23a2b9733edd8362383b416dfec886dbff44aec92d34148a552fe` |
| `pm4t_digests.json` | `f6fdf75cfbb2031ae3ef1059409744f42868600df30c45a1401f038599916267` |
| I-19 findings (baseline pin) | `59c6c85befdb4294e9b51e2353ffa6786e40bb4dfb61b33a2eb5fde8702d13e9` |

**Commits:** `280f3c9d` (math note, zero code) · `aebdb228` (addendum, zero code) · `42f090e4`
(fold + driver + findings + MIGRATION).

---

*Landed by gamora, 2026-08-14. Math note first and alone; the addendum before the repairs it
describes; the commission corrected where measurement contradicted it.*
