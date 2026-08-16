# KC2-PM4 · I-27 — **THE RING-RESIDENCE CENSUS** — LANDING NOTE

**MEASUREMENT-ONLY · ZERO FOLD · ZERO BEHAVIOUR CHANGE · NO TUNING (Law 3) ·
`F-I27` FAILS AS WRITTEN · THREE OWN DEFECTS, ONE OF THEM OLDER THAN THIS ITERATION ·
ONE REFERENT GRADE REFUSED BY NAME**

**Agent:** gamora · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** `R-PM4-71 part 6` (charter rows `L-60`/`R-PM4-70`, `L-61`/`R-PM4-71`).
**Base:** my own I-26 fold, engine `da6fa957`. Frozen substrate **E-s09-cp150**, unamended.

**Commits (engine, mine, THREE — the first TWO are zero code):**
`e62cc22d` math note **ALONE** (zero code, zero grades) → `c142c1c5` addendum #1
`D-I27-2`/`D-I27-3` (**ALONE, BEFORE both repairs**) → `bf9a822c` the census
(`kc2/residence.py` **NEW** · driver · two findings · MIGRATION · AGENT_STATE). **NOT PUSHED.**

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i27-findings-20260816_095918.json`
sha256 **`2a249f3462da60352c4d21318dae894a444819982c38a3c1534ee76f892b8818`**.
Wall **5.98 s**, **25/25 GREEN**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

⚑ **`F-I27` FAILS: THE RESIDENCE IS NOT A DEATH TIMER.** On the three record salts that carry the
pre-declared evaluability floor, **one of three** satisfies both clauses. On **every** cell with
≥ 19 intervals the displacement-terminated intervals are the **LONGER** kind, and the death share
of ring **body-time** falls **below** the death share of interval **counts** — 0.610 vs 0.667,
0.588 vs 0.700, 0.667 vs 0.737. **`W` is materially a MOVEMENT quantity, not a time-to-kill.**
⚑ **And Little's law closes to `0.0` on 7/7 cells while carrying no information whatsoever**: under
the run's own definitions `N` and `dt` cancel, so `λ·W = L` is **algebra, not a result** — a fact
written into the math note's zero-grade commit precisely so a residual of zero could never be read
as a validation. **Where the account does NOT close is the finding**: the run's two entry
numerators differ by exactly the intervals opening at a wave's first scan, predicted to `1e-12`
before measurement. ⚑ **And the fourteenth name's own referent grade is REFUSED**: `T4b(b)`
1.6166 s is the **player's** time at full health before dying, not a monster's ring residence.

---

## 1 — ⚑ `F-I27`, GRADED EXACTLY AS WRITTEN

**Window** (declared IN the criterion, `R-PM4-71 part 2`): the five record cells
`S-SPAWN × PX-LO` salts 0–4; per cell every wave from 151 to that cell's own board-death wave
inclusive; every ledger scan; terminal wave truncated by `player_death` on all five;
`n_censored` published per cell. **Graded per salt, never pooled across salts.**
**Evaluability floor** `N_int ≥ 10`, declared in advance with the admitted/excluded salts named
from I-26's pinned bytes **before running**.
**Functional**: `S_time(death)` = share of ring **body-time** terminated `died_in_ring`;
`M_death` / `M_disp` = **median** residence of death- and displacement-terminated intervals.

| salt | `N_int` | death wave | `S_time` | ≥ 0.70 | `M_death` s | `M_disp` s | `M_d ≥ M_p` | **holds** | (count share) |
|---|---:|---:|---:|:--:|---:|---:|:--:|:--:|---:|
| 0 | 4 | 151 | 0.7500 | ✓ | 0.6122 | 0.2041 | ✓ | — **EXCLUDED, underpowered** | 0.500 |
| **1** | **114** | 156 | **0.6099** | ✗ | 0.2857 | **0.3673** | ✗ | ⚑ **FAILS** | 0.667 |
| 2 | 7 | 151 | 0.8611 | ✓ | 0.4898 | 0.2041 | ✓ | — **EXCLUDED, underpowered** | 0.714 |
| **3** | **19** | 152 | **0.6667** | ✗ | 0.2449 | **0.5714** | ✗ | ⚑ **FAILS** | 0.737 |
| **4** | **25** | 152 | 0.8140 | ✓ | 0.2449 | 0.1633 | ✓ | **holds** | 0.720 |
| *S-YZ·PX-LO* | *110* | *156* | *0.5879* | *✗* | *0.3265* | *0.4082* | *✗* | *characterisation, **not in the criterion*** | *0.700* |
| *S-YZ·PX-HI* | *7* | *151* | *0.7500* | *✓* | *0.7347* | *0.1633* | *✓* | *characterisation, **not in the criterion*** | *0.714* |

⚑ **THE FAILURE IS COHERENT, NOT NOISY.** Both clauses fail together, on every large cell, in the
same direction, including the 110-interval characterisation arm that is not in the criterion at
all. **The reading the falsifier itself pre-declared:** the ring's residence is terminated
principally by **displacement**, and the next address is the **EXIT CHANNEL** under the I-24(c)
kinematics fold — not the kill rate.

⚑ **AND THE TIME-WEIGHTED SHARE IS *BELOW* THE COUNT SHARE ON EVERY LARGE CELL.** That is the
sharper half. It says displacement-terminated intervals are not merely numerous — they are
**longer**. The criterion was written on body-time *because* the counts were already knowable from
I-26's pinned bytes (math note § 5.1); registering the counts would have been theatre, and the
quantity that had never been measured is the one that decided it.

---

## 2 — ⚑ (c) THE LITTLE'S-LAW ACCOUNT: IT CLOSES, AND THE CLOSURE IS EMPTY

Said in the math note before any code (§ 3.1):

```
λ_int · W  =  [ N/(K·dt) ] · [ B·dt/N ]  =  B/K  =  L          N cancels. dt cancels.
```

**`E-1` HOLDS: residual `0.0` on 7/7 cells.** ⚑ **And the artifact says, in its own wire, that
this validates nothing.** Under the run's own definitions Little's law is an **identity**. It can
factor a measured `L` into a rate and a duration. It **cannot** arbitrate between them.

| cell | death wave | `N_int` | `L` | `λ_int` /s | `W` s | `W` ticks | p25/med/p95 ticks |
|---|---:|---:|---:|---:|---:|---:|---|
| `PX-LO` salt 0 (record) | 151 | 4 | 0.18692 | 0.45794 | 0.40816 | 5.00 | 2.75 / 3.0 / 10.65 |
| `PX-LO` salt 1 | 156 | 114 | 0.49204 | 1.17058 | 0.42034 | 5.15 | 2.0 / 4.0 / 15.0 |
| `PX-LO` salt 2 | 151 | 7 | 0.28571 | 0.68056 | 0.41983 | 5.14 | 4.0 / 5.0 / 8.1 |
| `PX-LO` salt 3 | 152 | 19 | 0.25127 | 0.59074 | 0.42535 | 5.21 | 1.5 / 3.0 / 12.3 |
| `PX-LO` salt 4 | 152 | 25 | 0.26543 | 0.94522 | 0.28082 | 3.44 | 2.0 / 3.0 / 8.4 |
| `S-YZ·PX-LO` | 156 | 110 | 0.41579 | 0.78801 | 0.52764 | 6.46 | 3.0 / 4.5 / 17.0 |
| `S-YZ·PX-HI` | 151 | 7 | 0.50485 | 0.83252 | 0.60641 | 7.43 | 3.5 / 9.0 / 12.4 |

**Resolution stamp, on every quantile:** one scan = `0.0816326530612245 s`; the true continuous
residence of a visit recorded at `n` scans lies in `((n−1)·dt, (n+1)·dt)`.

### 2.1 ⚑ WHERE IT DOES **NOT** CLOSE — AND THAT IS THE COMMISSION'S OWN QUESTION

The run carries **two** entry numerators and always has:

* `N_int` — `engagement._intervals_of`: an interval **may** open at a wave's first scan;
* `N_ent` — `kill_rate_join`: its loop skips `i == 0` (`engagement.py:548-558`) and therefore
  **cannot** see one.

**`E-2` HOLDS:** the gap is exactly `L·(N_int − N_ent)/N_int`, matched to `1e-12` on every cell,
and `N_int − N_ent` equals the count of intervals opening at a first scan, cell by cell. On
`S-YZ·S-SPAWN·PX-LO` that is **one** interval and **3.78e-03** of occupancy — the single
non-closing cell among I-26's twenty-two, identified from that artifact's pinned bytes *before*
this census ran.

⚑ **NEITHER INSTRUMENT IS CHANGED.** `kill_rate_join`'s skip is correct for a **transition**;
`_intervals_of`'s inclusion is correct for an **interval**. Two functionals, not like-for-like by
`R-PM4-71 part 2`'s own law, both standing under their own definitions, neither graded against the
other. **A finding about the measurement definitions, not something to reconcile by adjustment.**

---

## 3 — ⚑ (d) THE KILL-LOCATION CENSUS

Exhaustive over bodies, closes or raises (`E-6` HOLDS 7/7).

| cell | bodies | `died_en_route` | `died_at_entry` | `died_in_residence` | alive, entered | alive, never entered |
|---|---:|---:|---:|---:|---:|---:|
| `PX-LO` s0 | 28 | 3 | 0 | 2 | 0 | 23 |
| `PX-LO` s1 | 114 | **28** | 12 | 64 | 0 | 10 |
| `PX-LO` s2 | 28 | 2 | 0 | 5 | 1 | 20 |
| `PX-LO` s3 | 45 | **14** | 4 | 10 | 0 | 17 |
| `PX-LO` s4 | 45 | **10** | 2 | 16 | 0 | 17 |
| `S-YZ·PX-LO` | 107 | **20** | 10 | 67 | 0 | 10 |
| `S-YZ·PX-HI` | 28 | 0 | 0 | 5 | 1 | 22 |

⚑ **A QUARTER TO A THIRD OF THE BODIES THAT DIE, DIE WITHOUT EVER CROSSING THE BOUNDARY** — the
disc reaches 3.0 m and the ring is 2.4 m, so `died_en_route` is a **reach** kill. And `died_at_entry`
— dead inside the declared **one-scan** first-sample resolution — is **12/114** and **10/107** on
the long boards.

**Time from entry to death** (median · p95, seconds): s1 **0.286 · 1.061** · s3 0.245 · 1.065 ·
s4 0.245 · 0.808 · `S-YZ·PX-LO` 0.327 · 1.061 · `S-YZ·PX-HI` 0.735 · 1.012.

**What kills them, from the code path** (`run.py:2270-2289` the disc; `run.py:2346-2380` the
secondary streams; `run.py:1527`/`2243` the **pet** arm), then verified against the run's own
rows — `E-7` HOLDS on a **non-empty** population after `D-I27-2`:

| cell | `disc_eyeofreckoning1` | `lightning` | `pet` | `pet_ttl_expired` |
|---|---:|---:|---:|---:|
| `PX-LO` s1 | 102 | 2 | 110 | 2 |
| `S-YZ·PX-LO` | 97 | — | 129 | 9 |

**Zero monster-on-monster rows. Zero environmental rows. Every roster kill is the player.**

---

## 4 — ⚑ `OBS-I27-1` — THE GRADE THE COMMISSION OFFERED, **REFUSED BY NAME**

`R-PM4-71 part 5`: *"The referent already carries a banked residence grade — **T4b(b) 1.6166 s
dwell**."*

**It is not a ring residence.** `arrival.py:161` sources it from the Lap K table's
`full_health_dwell_s`; the sim-side instrument (`…i16….py:385-425` `strict_dwell`) *"counts back
from the death tick while `hp_frac >= 0.999`"* on `MO_PLAYER_HP_MAX`. **It is the PLAYER's maximal
contiguous time at FULL HEALTH immediately before the PLAYER dies.** `W` is a **MONSTER's** time
inside the melee boundary. Different quantity, different population, different clock — the
`OBS-I26-1` non-comparison exactly, and what `R-PM4-71 part 2`'s own sharpened law forbids.

⚑ **THE GRADE IS REFUSED AND `W` CARRIES NO REFERENT COMPARATOR ANYWHERE IN THE ARTIFACT**
(wall row 19 asserts both). Had I taken it, a `W` of 0.28–0.61 s against "1.6166 s" would have
read as a clean **~3–6× residence deficit**, and the run would have acquired a convergence story
built on a category error. **Routed to the conductor, not repaired from my seat.**

### 4.1 ⚑ `UNREACHED-I27-1` — AND WHY THE COMMISSION'S SUGGESTED FALSIFIER SHAPE WAS NOT WRITABLE

The occupancy deficit **cannot** be split into a `λ` share and a `W` share: no referent `λ` exists
(**Lap AB DO-NOT 9** inherits `D-U-3` — `pm4u_arrivals.csv` is a strict upper bound, not gradeable
against a sim) and no referent `W` exists (§ 4). Lap R's bracket is an **occupancy**, not a
duration.

A criterion of the shape *"factor X carries the deficit by at least ratio r"* therefore requires
**inventing** a referent factor, which is Law 3's exact prohibition. I said so in the math note
**before** registering anything, registered the sim-internal decomposition that **is** writable,
and published the referent-side split as a **hole with three named missing pins** — a per-body
referent ring-entry time, a per-body referent ring-exit time, a referent body population at the
ring. **Lap AB § 4.4's own move, one lap later.**

---

## 5 — ⚑ `NAMED-I27-1` — THE TWO `L`s, AND THE ONE THIS RUN HAS BEEN QUOTING

| symbol | site | population |
|---|---|---|
| `occupancy_curve(...)["mean_occupancy"]` | `engagement.py:906-933` | **MOVERS ONLY** |
| `waves[0]["ring_density"]["hist_engage"]` | `run.py:2047-2069` | **movers AND pets** |

`E-12` HOLDS: the movers+pets zero bucket reproduces `hist_engage`'s zero bucket **exactly** on
7/7 cells, which is what makes "they differ only by pet ring-scans" a measurement.

| cell | `L` movers-only (**of record**) | `L` pet-inclusive (published) | pet share |
|---|---:|---:|---:|
| `PX-LO` s0 | 0.18692 | 0.27103 | 0.310 |
| `PX-LO` s1 | 0.49204 | **1.08885** | **0.548** |
| `PX-LO` s3 | 0.25127 | 0.31472 | 0.202 |
| `PX-LO` s4 | 0.26543 | 0.33642 | 0.211 |
| `S-YZ·PX-LO` | 0.41579 | **0.84912** | **0.510** |
| `S-YZ·PX-HI` | 0.50485 | 0.66019 | 0.235 |

⚑ **THE DEFINITION OF RECORD IS UNCHANGED.** Every occupancy figure this run has quoted —
including the standing residual — is the movers-only one, and switching the definition of the
run's headline residual **inside a measurement iteration** is not a move a census makes. **No cell
is designated, elected or ranked** (`R-PM4-27 part 3`, ninth consecutive iteration). The fork is
**NAMED and ROUTED**; the conductor rules on whether the referent's own instrument counted summons.

---

## 6 — DEFECT TABLE — **THREE, ALL MINE, ALL SELF-CAUGHT, ADDENDUM ALONE BEFORE BOTH REPAIRS**

| id | defect | disposition |
|---|---|---|
| **`D-I27-2`** | ⚑ **THE BIG ONE, AND OLDER THAN THIS ITERATION.** `E-7` reported **GREEN on all seven cells with an OBSERVED TAG SET OF `{}`**. `engagement.kill_rate_join:562-565` tests `isinstance(ev, dict)` against `run.events` rows that `run._mk_row:251-257` returns as **LISTS** — the branch is unreachable, and `⚑ DEATH_SOURCE_TAGS_enumerated` has been empty on **every cell of every lap since I-24-D**. The unreachable branch is mine; the green-by-absence is also mine, **one iteration after I banked `D-I26-6`** (*a row that cannot go red is a caption*) | addendum #1 **ALONE, before the repair**. Repaired **BY ADDITION** in `kc2/residence.py` (index-based, through `run.EVENT_COLUMNS` imported by identity) and ⚑ **EXPLICITLY NOT in `engagement.py`** — `P.14`'s byte-identity assertion is this census's strongest law_3 tripwire and is not weakened to tidy a reporting field. **Prior artifacts NOT re-graded**; the defect is REPORTED AND ROUTED. New pin **`P.15`** requires the population **non-empty**. The empty field is **still published** as the defect's own evidence, alongside the pre-repair findings artifact |
| **`D-I27-3`** | `pet_ring_census` published `mover_zero_bucket_total: None` — a key with no computation behind it — while the pet arm was recording **hundreds** of in-ring scans | addendum #1 **ALONE**. Repaired by addition; `E-12` now graded on the joint-zero identity, and § 5's fork became visible |
| **`D-I27-1`** | the math note's **five**-bucket kill-location partition conflated a body that **never spawned** with one that spawned and lived — total, but not exhaustive | disclosed in `kc2/residence.py`'s own comment and in the findings; refined to **six** buckets with a **HALT armed** on the case the note's version would have swallowed. `D-I25-3`'s class |
| **`D-CON-9`** | ⚑ **ONE, AND IT IS THE COMMISSION'S.** `R-PM4-71 part 5`'s *"banked residence grade — T4b(b) 1.6166 s dwell"* is a category error (§ 4). Every other numeral in the I-27 commission verifies against the artifact it points at | **ROUTED, NOT REPAIRED.** The grade is refused by name and the conductor rules |

> ⚑ **TENTH CONSECUTIVE ITERATION IN WHICH MY OWN PRE-REGISTRATION CAUGHT MY OWN WORK BEFORE A
> NUMBER WAS REPORTED — AND THE FIRST IN WHICH THE CATCH WAS A GREEN THAT HAD BEEN GREEN FOR FOUR
> LAPS.** `D-I26-6` taught that a row which cannot go red is a caption. I banked that lesson at
> I-26 and shipped its exact twin at I-27 one commit later. The lesson only counts when the guard
> is written to test its own **population**, not merely its own predicate.

---

## 7 — PRE-REGISTERED EXPECTATIONS, GRADED HONESTLY

| id | claim | grade |
|---|---|---|
| `E-1` | the account closes to `1e-12` | ⚑ **HELD 7/7 — and the artifact says the closure is an IDENTITY and validates nothing** |
| `E-2` | the fork is exactly the tick-0 memberships | ⚑ **HELD 7/7, counts agree cell by cell** |
| **`E-3`** | ⚑ **THE TRIPWIRE** — all seven cells reproduce I-26's PINNED surface **and** knot digests | ⚑ **HELD 14/14, EXCLUSION SCOPE ∅** |
| `E-4` | pooled median residence strictly above one scan | ⚑ **HELD** (3–5 scans on the record ensemble) |
| `E-5` | ⚑ **MY LEAN** — per-body ÷ per-interval ≥ 1.2 on the ≥ 100-interval cells | ⚑ **HELD — 1.326 and 1.264. Re-entry is material** |
| `E-6` | kill-location partition exhaustive, closes | ⚑ **HELD 7/7** |
| `E-7` | every death tag inside the allow-list | ⚑ **HELD — but only after `D-I27-2`. As first run it was GREEN BY ABSENCE** |
| `E-8` | the ledger's predicate == `ring.THRESHOLD_SQ_M2`, every wave | ⚑ **HELD, HALT armed** |
| `E-9` | censoring channel empty on the criterion's cells | ⚑ **HELD — `n_censored = 0` on all five record salts** |
| `E-10` | ⚑ **AGAINST MY OWN CONVENIENCE** — truncation visible in `λ` | ⚑ **FAILED.** The one cell with a non-terminal population shows the terminal wave **inside** the non-terminal spread; six cells fight a single wave and report `None`. **Truncation is inert on `λ` here, and that is reported as the negative it is** |
| `E-11` | I-26's pinned exit-cause distribution reproduced | ⚑ **HELD 7/7** |
| `E-12` | the two `L`s differ only by pet ring-scans, published as a count | ⚑ **HELD 7/7 — and the count is 20–55 %** |
| **`F-I27`** | the residence is a death timer | ⚑ **FAILS — 1 of 3 evaluable salts. REPORTED, NOT PATCHED** |

**Mechanical pins:** `P.1` law_3 `moved == {}`, witnesses in declared form, no undeclared group ✅ ·
`P.2` frozen **20/20**, cardinality asserted ✅ · `P.3` `E-3`, exclusion scope **∅** ✅ ·
`P.4` determinism ×2 — three legs including the **census digest**, plus cross-invocation identity
on `cells` / `⚑ GRADES` / `law_3` (only `started_utc` and `wall_s` vary) ✅ · `P.5` pinned artifacts
re-hashed EXACT ✅ · `P.6` wall **25/25**, `keys_asserted` per row ✅ · `P.7` ring-literal AST ✅ ·
`P.9` zero referent numerals in any branch condition — **the list now includes `1.6166`, the grade
`OBS-I27-1` refuses** ✅ · `P.13` `residence.py` draws no RNG and writes no argument (AST) ✅ ·
**`P.14` empty `git diff --name-status` of every pre-existing file in `kc2/` against `da6fa957`** ✅ ·
`P.15` death-tag population non-empty ✅.

**Smoke:** `296 pass / 1 PRE-EXISTING failure` (`test_AC_10_10`, `secondary_streams.py:136`) —
**unchanged from I-23, I-24, I-24-D, I-25 and I-26.**

---

## 8 — (e) PRIOR-MEASUREMENT RECONCILIATION, BY IDENTITY

Every prior number read **from the named artifact's own bytes at run time**, re-hashed first.

1. **I-25's `W` functional is imported, not re-derived.** `mean_ring_dwell_s = Σ ticks_in_ring ·
   dt / n_intervals`. **My `W` reproduces I-26's pinned `W` to full precision on 7/7 cells**
   (`0.408163265…`, `0.420336556…`, `0.419825073…`, `0.425349087…`, `0.280816327…`,
   `0.527643785…`, `0.606413994…`), and my `λ_ent` reproduces its pinned `⚑ R_entry_bodies_per_s`
   and my `L` its pinned `mean_occupancy`, exactly.
2. ⚑ **I-24-D's HEADLINE NO LONGER HOLDS ON THE CURRENT SIM — ATTRIBUTED, NOT CORRECTED.** I-24-D
   banked *"25 of 26 exits are the body dying where it stands"* (**96.15 %**) with **ZERO**
   `displaced_player_moved`. On the I-24(c) base the same census reports **66.7 %** with
   `displaced_player_moved` at **22 of 114** intervals. That movement is **a consequence of the
   I-24(c) player-kinematics fold**, dated and attributed. **Prior artifacts are NOT re-graded**
   (I-26's own precedent); I-24-D's numbers remain true of I-24-D's sim.
3. **The `L` of record is `occupancy_curve`'s, movers-only** — § 5, `NAMED-I27-1`.

**Consulted, re-hashed EXACT from bytes (HALT armed; none fired):** I-26 findings
`3babf0a2…f9bf` · I-25 findings `708916c1…b28b` · I-24-D findings `0e64fe31…f0c1` ·
Lap R `pm4r_contact_occupancy.csv` `913a57a3…20e6` (**a GRADE, a BRACKET, NOT RULED**) ·
Lap AB `pm4ab_findings.md` `a0279b11…07ba`.

---

## 9 — `UNREACHED`, NAMED AND NOT APPROXIMATED

* **`UNREACHED-I27-1`** — the referent-side `λ`/`W` split. **A hole with three named missing pins**
  (§ 4.1). Not estimated, not bracketed, not inferred from `L` by assuming a factor.
* **`UNREACHED-I27-2`** — a displacement exit's *cause* is labelled by the existing geometric test
  (who moved), which is not a claim about **why** the player moved. The player-drive policy's own
  reason is not on the ledger.
* **`OBS-I27-1`** (§ 4) · **`NAMED-I27-1`** (§ 5).
* **Carried:** `UNREACHED-I26-1/2/3` (the alert gate remains a NAMED OMISSION; the sim's absolute
  arrival clock still runs **EARLY**) · `UNREACHED-I25-1/2/3/4` · `UNREACHED-I24-1/2/3` ·
  `UNREACHED-I24D-1` · `UNREACHED-Z-1` · `UNREACHED-Y-1` · `UNREACHED-X-1` ·
  `UNREACHED-AB-1/2/3/4/5/6` · `NAMED-Z-1/2/3` · `NAMED-AA-3/4` · `NAMED-I26-1` · `NAMED-AB-1/2` ·
  `OBS-I26-1` · the 17 unexpressed AI states · `T17` · `D-PDEF-2` · `pools_for` default ·
  `D-I21-1` (quantified, unrepaired).

---

## 10 — DIGESTS (full 64 hex, `R-PM4-55 part 2`) — ⚑ **COMPUTED AFTER THE FINAL WRITE** (`D-AA-5`)

| artifact | sha256 |
|---|---|
| `output/kc2-pm4-i27-findings-20260816_095918.json` | `2a249f3462da60352c4d21318dae894a444819982c38a3c1534ee76f892b8818` |
| `output/kc2-pm4-i27-findings-20260816_095327.json` (⚑ the **pre-repair** artifact, `D-I27-2`'s own evidence, published rather than deleted) | `68aee860b713281be430836a47916039376dc5445bf97ac339c0356e4fb90330` |
| `math/kc2-pm4-i27-ring-residence-census-2026-08-16.md` | `77266f3e36dc36a03a271875eaa3527516c7c9f8c164538ac493a099fa70740f` |
| `math/kc2-pm4-i27-ring-residence-census-ADDENDUM-2026-08-16.md` | `c2b3106f6b32178bb104847875c1087c26ebe55b39535e6670bb68fe7d624ced` |
| `kc2/residence.py` (**NEW — the ONLY change in the package**) | `c2f3f529e87830afc4863349f97261d852a03f047d5156903a5b4846bb30d470` |
| `scripts/gamora_kc2_pm4_i27_ring_residence_census_2026_08_16.py` | `abb6264fdac9a50ab1e41d25da6846c6dc258de4108367f707bab2cf21f5f0bc` |
| `simulation/MIGRATION.md` | `48b8f51d4f1dbd99c1249326791d07a06151bfca59ee85a25a5a9eb0837587e2` |
| `simulation/AGENT_STATE.md` | `28658060aef97c83f8a457c68eeefd39e28aa177a99f9f2963b03616e2073cf4` |

⚑ **The committed blob equals the working tree on every row** — the post-final-write digest law,
re-verified from my own seat with `git show` against the working file.

---

## 11 — DO-NOT BLOCKS CARRIED, ENTIRE

Lap V § 7.2 · Lap V-2 § 11.2 · Lap W § 7.2 · Lap X § 12.2 · Lap Y § 11.6 · Lap Z § 5 (all seven) ·
Lap AA § 6 (all eight) · **Lap AB § 9 (all ten)**.

Named where this census sits closest:

* **AB-9** — `pm4u_arrivals.csv` is **not** used as an arrival rate. It is exactly why § 4.1 is an
  UNREACHED and not a bracket.
* **AB-4** — `F-AB-1`'s failure is cited nowhere as referent compression; § 4.4's peak-living table
  is read as **orientation** and enters no arithmetic here.
* **AB-5/6** — no frames converted to seconds, no alert duration estimated, no immobility claimed;
  the gate remains a NAMED OMISSION and the absolute arrival clock still runs EARLY.
* **Z-1** — `2.4000000953674316` is never called the ring radius; the predicate is read off the
  ledger **and** asserted equal to `ring.THRESHOLD_SQ_M2` on every wave (`E-8`, HALT armed).
* **AA-2** — no pack is ever an area-uniform disc; nothing here touches a sampler.
* Lap R's occupancy bracket carried as a **BRACKET**, never ruled, asserted absent from every
  branch condition in `kc2/` — as is `1.6166`, now on the same list.

---

## 12 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. ⚑ **THE FOURTEENTH NAME SURVIVES, BUT ITS MECHANISM IS THE OPPOSITE OF THE ONE PROPOSED.**
   Occupancy IS bought by staying — and what ends the staying is **displacement**, not death, on
   every cell with power. The exit channel under the I-24(c) kinematics fold is the address this
   measurement points at.
2. ⚑ **`OBS-I27-1` NEEDS A CONDUCTOR RULING.** The run's only banked "residence" grade is the
   player's full-health dwell. If the fourteenth name is to be graded at all, a referent **monster**
   ring-residence has to be commissioned on the referent side, and it does not exist today.
3. ⚑ **`NAMED-I27-1` IS LOAD-BEARING FOR THE RESIDUAL ITSELF.** The standing deficit is quoted on a
   **movers-only** occupancy. The pet-inclusive occupancy on the same boards is up to **1.089**.
   Whether Lap R's video instrument counted summons is a **referent-side** question no lap has
   asked, and it moves the residual's denominator, not its numerator. **I measured both and
   changed neither.**
4. ⚑ **`D-I27-2` IS A REPAIR SOMEONE MUST OWN.** `engagement.kill_rate_join`'s tag enumeration is
   unreachable and has shipped `{}` in three findings artifacts. I refused to fix it inside a
   census whose strongest tripwire is that no pre-existing `kc2/` file moved. It is a one-line
   repair and it belongs in a commit that is allowed to touch that file.
5. ⚑ **THE COMMISSIONING LESSON, OFFERED NOT CLAIMED.** `R-PM4-71 part 2` sharpened the
   like-for-like law to WINDOW **and** FUNCTIONAL. `D-I27-2` suggests a fourth clause: **a
   criterion must also declare its POPULATION'S NON-EMPTINESS**, because a share, a share-of-set,
   or an allow-list check over an empty population is green by construction.

---

*End of landing note.*
