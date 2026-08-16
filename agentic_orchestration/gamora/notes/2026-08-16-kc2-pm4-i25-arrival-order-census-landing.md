# KC2-PM4 · I-25 — **THE ARRIVAL-ORDER CENSUS** — LANDING NOTE

**MEASUREMENT ONLY · ZERO FOLD · ZERO BEHAVIOUR CHANGE · NO REPAIR · NO DESIGNATION · NO SEED SELECTED**

**Agent:** gamora · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** `R-PM4-67 part 6` (charter row `R-PM4-67`; ledger `L-57`).
**Base:** my own I-24 fold, engine `79aceb7b`.

**Commits (engine, mine, THREE — the first TWO are zero code):**
`557fd600` math note **ALONE** → `8c279e06` addendum #1 `D-I25-3` (**ALONE, before its repair**) →
the census (`kc2/arrival_order.py` NEW · driver · findings · MIGRATION · AGENT_STATE).
**NOT PUSHED** — the conductor pushes at banking.

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i25-findings-20260816_075607.json`
sha256 **`708916c13d612220d2f544fd266d08f6bb469bb48f9fce3d58e09aec614ab28b`**. Wall **10.17 s**,
**21/21 GREEN**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**`F-I25` HOLDS: the serialisation is NOT fully attributable to the three sources the twelfth name
points at.** Freezing spawn stagger, spawn-node geometry AND speed spread all at once leaves the
mean consecutive arrival gap at **4.6× – 11.4× what the ring would need** — on **7 of 7 evaluable
cells**, ratio range `[4.61, 11.38]`. Worse for the twelfth name than that: on the long
characterisation cell **freezing any ONE named source makes the spacing LARGER, not smaller**
(`ρ_GEO = −0.077`, `ρ_SPD = −0.040`, `ρ_STAG = −0.037`), while freezing all three together
*reduces* it by 17.7 % — **the three sources INTERACT and no single one of them carries**. And the
ORDER question, which is the one the commission actually asked, has a different and sharper
answer: **spawn-node geometry carries the arrival ORDER** (τ-b vs `L1` falls to **0.859** when its
radial spread is frozen, against 0.935 for speed and 0.964 for stagger) — **but 0.794 of the rank
order survives freezing all three**, and what carries that residual is a **FOURTH source the
commission did not name: the per-body BEARING and its interaction with the player's own track**,
which the `L-GEO` probe deliberately preserved so it could be seen rather than absorbed.

⚑ **The instrument is a replay of the sim's own march clock and it is validated, not asserted:**
median per-tick position deviation **0.000 m** across **21,534** body-ticks on the
characterisation cell, and it reproduces the measured arrival ORDER at **τ-b = 0.998**.

---

## 1 — ⚑ ZERO FOLD, PROVEN AGAINST A PRIOR ARTIFACT

I-25 adds **no `simulate_wave` parameter, no branch, no emission site, no wave-row key and no
simulation constant.** The census consumes only artifacts that already existed: I-24-D's
`run.ring_ledger`, `run.movers`/`run.actors` (since PM-1), and `patrol.entry_index` /
`rg.RingPredicate` **called, never restated**.

**Consequence: non-perturbation is provable against I-24's OWN DIGESTS, not merely against a second
run of myself.** Wall row 6:

| my cell | I-24 cell | surface | knot | l4l | death wave |
|---|---|---|---|---|---|
| `ALL__PX-LO__salt0` | `ALL__ORDER-AR__PX-LO` | **EXACT** | **EXACT** | **EXACT** | **EXACT** |
| `ALL__PX-HI__salt0` | `ALL__ORDER-AR__PX-HI` | **EXACT** | **EXACT** | **EXACT** | **EXACT** |
| `S-YZ__PX-LO` | `S-YZ__ORDER-AR__PX-LO` | **EXACT** | **EXACT** | **EXACT** | **EXACT** |
| `S-YZ__PX-HI` | `S-YZ__ORDER-AR__PX-HI` | **EXACT** | **EXACT** | **EXACT** | **EXACT** |

**N-legs (`E-10`), three, one digest:** census **OFF** / **ON** / **ON, real second execution** all
return surface `217f682492847e3a365945c52785573b5871a0c8e03150dc94d19a5a644d1d20` and knot
`d0d818c4211613db012d00e2fa3e173d7cd0b925a3ca22eb896f7925b7531c72` — **and that surface is
byte-identical to I-24's pinned `ALL·PX-LO`.** Determinism ×2 EXACT; the `D-I24D-2` differencing
probe returns one digest across three independent constructions.

---

## 2 — ⚑ THE CENSUS: EVERY BODY, JOINTLY

**12 cells · 738 body-records · every field measured on the same instrument.** Per body: spawn
tick · spawn position · spawn point · entry-node index and position (reconstructed by calling the
DECODED `patrol.entry_index`) · reassignment counters per tick · the sim's own composed
`speed_m_per_s` · the full distance-to-ring trajectory · ring-entry tick under the **unified I-24
predicate** · ring-exit cause through `engagement.ring_ledger_census`, whose exhaustive partition
**HALTS** if it does not close (it closed on 12/12 cells).

### 2.1 THE SPAWN CLOCK IS TWO-VALUED, AND IT IS MEASURED RATHER THAN ASSUMED

| cell | distinct spawn times | histogram |
|---|---|---|
| `ALL·PX-LO` salt 0 | **`{0.0, 4.0}`** | 24 @ 0.0 · 4 @ 4.0 |
| `S-YZ·PX-HI` | **`{0.0, 4.0}`** | 95 @ 0.0 · 19 @ 4.0 |

The I-22 ambush-burst release law, confirmed by measurement: `P05_FIRST_ARRIVAL_S` with no drip.
**The spawn clock is not a continuum and the decomposition does not treat it as one.**

### 2.2 THE GEOMETRY IS THE WIDE ONE

`ALL·PX-LO`: initial distance `d₀` spans **8.61 – 42.96 m** (median 34.88); speed spans
**1.926 – 4.975 m/s** (median 1.926 — the fallback multiplier). `S-YZ·PX-HI`: `d₀` **13.35 –
82.20 m** (median 42.21), speed **1.833 – 4.736** (median 3.055).

⚑ **The arithmetic that explains the whole board:** at the roster-mean distance (31.42 m) and the
roster-mean speed (2.63 m/s), closing to the ring takes **11.0 s** — against a fought `PX-LO`
window of **9.14 s**. **The bodies that arrive are the ones that are near AND fast. The arrival set
is a joint selection on `d₀` and `v`, and that selection IS the serialisation.**

### 2.3 `E-7` FAILED, HONESTLY, ON EXACTLY ONE CELL

Re-path / retarget churn: `n_patrol_legs_after_entry = 0` on **12/12** cells; `node_reached` never
flips beyond the first; **but `gate_ever_closed_after_open = 3` on `S-YZ·PX-HI`.** `E-7` as
registered demanded *exactly zero* and it is **FAILED**. Magnitude named `UNREACHED`: three
closures on 114 bodies over 160 s cannot carry a 4.6–11.4× spacing gap, and no rung was built for
it — **a rung for a term measured at zero would be a source invented so that something could be
attributed** (math note § 4.3, written before the number existed).

### 2.4 ⚑ AN I-24-D HEADLINE UPDATES ON THE I-24 RECORD CELL — REPORTED, NOT BURIED

I-24-D measured `displaced_player_moved = 0` on **26 exits**, on **I-23's** cell. On the **I-24**
record cell it is **not zero**: `ALL·PX-LO` 2 of 6 exits, `S-YZ·PX-HI` **17 of 113**. The two
measurements do not contradict — they are different cells, and `K-MILL` plus the repaired predicate
landed between them — but *"zero exits are displacement by the player"* is now a statement about a
superseded configuration and should not travel forward unqualified. `died_in_ring` remains the
plurality everywhere (4/6 and 89/113).

---

## 3 — ⚑ THE INSTRUMENT, VALIDATED BEFORE IT IS BELIEVED

The **march-clock replay integrator** re-integrates each body against the **measured player track**
with the sim's own step law, importing the halt radius and the membership predicate **separately
and by identity** (`D-I25-2`).

**PC-a — per-tick position:**

| cell | n body-ticks | median | p75 | p95 | mean | max |
|---|---:|---:|---:|---:|---:|---:|
| `ALL·PX-LO` salt 0 | 2,829 | **0.0000 m** | 0.0000 | 1.8604 | 0.2184 | 4.4161 |
| `S-YZ·PX-HI` | 21,534 | **0.0000 m** | 0.0300 | 0.5973 | 0.1467 | 10.0122 |

**PC-b — entry tick (`E-1`): 11 of 12 cells validated.** Median `|Δ|` **0.0 ticks** on the large
cells; 60–94 % within the declared ±2-tick band.

⚑ **`E-1` FAILED on `ALL·PX-HI` salt 3** (n = 8, 50 % within band, median 3.0 ticks) — **and the
math note's own contingency was executed rather than softened**: that cell's ρ shares are
**published but NOT read as an attribution**, and every aggregate excludes it **by name**
(`⚑ ATTRIBUTION_UNREACHED_CELLS`). No headline moves: the record cell and the entire `PX-LO`
ensemble validated.

---

## 4 — ⚑ THE DECOMPOSITION: WHAT CARRIES THE SPACING

Leave-one-out, each rung differing from `L1` in **exactly one** input.

### 4.1 `ALL·PX-LO` salt 0 — THE RECORD CELL

| probe | N | `G` (s) | `1/λ` (s) | ρ on `G` |
|---|---:|---:|---:|---:|
| **`L1`** (all measured) | 5 | **0.32653** | 1.8286 | — |
| `L-STAG` (stagger frozen) | 5 | 1.79592 | 1.8286 | **−4.500** |
| `L-GEO` (radius frozen, **bearing kept**) | 6 | 0.06531 | 1.5238 | **+0.800** |
| `L-SPD` (speed frozen) | 4 | 0.68027 | 2.2857 | **−1.083** |
| `L0` (all three frozen) | **0** | undefined | — | — |

### 4.2 `S-YZ·PX-HI` — THE CHARACTERISATION CELL (98 arrivals, 160 s)

| probe | N | `G` (s) | ρ on `G` | τ-b vs `L1` |
|---|---:|---:|---:|---:|
| **`L1`** | 98 | **1.58384** | — | — |
| `L-STAG` | 96 | 1.64211 | −0.0368 | 0.9645 |
| `L-GEO` | 90 | 1.70511 | −0.0766 | **0.8588** |
| `L-SPD` | 95 | 1.64742 | −0.0401 | 0.9351 |
| `L0` | 97 | **1.30272** | **+0.1775** | **0.7939** |

⚑ **`NO SINGLE NAMED SOURCE CARRIES THE SPACING.`** Every leave-one-out share is **negative** —
freezing one source makes the gaps *larger*. Freezing all three gives **+0.1775**. The shares sum
to **−0.153** against an all-frozen reduction of **+0.177**: **additivity FAILS by 0.33 against a
declared tolerance of 0.10**, so the census reports the **INTERACTION** rather than a clean split —
the legitimate outcome the math note § 4.4 declared as one before any ρ existed. **Additivity
fails on 9 of 12 cells** — it HOLDS on the three cells with large `L0` arrival counts (`ALL·PX-HI`
salts 2/4, `ALL·PX-LO` salt 1), which is itself informative: the interaction is a small-sample
regime, not a universal one.

### 4.3 ⚑ THE ORDER, WHICH IS THE COMMISSION'S ACTUAL QUESTION

`R-PM4-67 part 6` asks where bodies acquire their arrival **ORDER**. Order is a **rank** question
and spacing is not, and the census answers them separately.

**τ-b(`L1` vs measured) = 0.9984** on the characterisation cell — the replay reproduces the sim's
realised arrival order almost exactly. Freezing each source, the ORDER carrier is the one whose
freezing destroys the most rank correlation:

**`GEOMETRY` on 6 of the 11 attributable cells** — including BOTH deterministic `S-YZ` cells and
`ALL·PX-HI` salts 0/2/4 — with **`SPEED` on 4** and **`STAGGER` on 1**. The geometry lead is
clear on the large-sample cells and is NOT unanimous on the short `PX-LO` ones, and both halves
are reported.

⚑ **AND THE RESIDUAL IS THE FINDING.** τ-b(`L1` vs `L0`) = **0.7939**: **79 % of the arrival order
survives freezing all three named sources.** `L-GEO` freezes the radial spread and **preserves the
bearing** — deliberately, declared in § 4.3 of the math note before any code — precisely so this
residual would be visible instead of absorbed. **What carries the surviving order is the per-body
BEARING and its interaction with the player's own track: a FOURTH source, inside the spawn
geometry, that the twelfth name does not reach.**

---

## 5 — ⚑ WHAT THE RING WOULD NEED (a GRADE, never an input)

`L = λ·W` ⟹ `g_required = W / L_referent`, with `W` the sim's own MEASURED mean ring dwell per
ENTRY INTERVAL and `L_referent` Lap R's bracket `[3.2423, 3.4251]` — **a bracket, NOT ruled**.

| cell | `W` (s) | `g_required` (s) | `g_measured` (s) | **ratio** |
|---|---:|---:|---:|---:|
| `ALL·PX-LO` salt 0 (record) | 0.27211 | `[0.07945, 0.08392]` | **0.59184** | **7.05 – 7.45×** |
| `ALL·PX-HI` salt 0 | 0.51701 | `[0.15095, 0.15946]` | 0.68571 | 4.30 – 4.54× |
| `S-YZ·PX-HI` | 0.53459 | `[0.15608, 0.16488]` | **1.72621** | **10.47 – 11.06×** |

**`E-5` HOLDS** (≥ 5× on the record cell). The measured consecutive-gap **distribution** on
`S-YZ·PX-HI` (89 gaps): min **0.0000** · p25 0.4082 · median **0.7347** · p75 1.7959 · p95
**7.0204** · max **10.3673** s. **The ring does not need a smaller mean. It needs the p95 not to
exist** — one gap in twenty is longer than seven seconds on a board whose required spacing is
0.16 s.

⚑ **THE CAVEAT TRAVELS:** `W` is death-truncated (I-24-D: 96 % of exits are the body dying where it
stands), so `g_required` is *the spacing this sim would need GIVEN ITS OWN kill rate*
(`UNREACHED-I25-3`).

---

## 6 — THE CHARACTERISATION CELL (`R-PM4-67 part 6`, its own cell)

**`S-YZ·PX-HI` — a+b only, kinematics OFF, deterministic. FULL T-SCORECARD.**

| target | value | met |
|---|---|---|
| **T1** death wave | **156** (band {159–161}) | ✗ |
| **T2** l4l · ratio | **160.16327 s** · **0.87657** (band [155.31, 210.12]) | ⚑ **MET** |
| **T3** MAE · median ratio | 13.0561 s · 1.6584 (4 waves UNEVALUABLE) | ✗ |
| **T4a** mean hp frac | 0.89989 (video 0.932 ± 0.02) | ✗ |
| **T4b(b)** strict dwell | 0.0000 s (referent 1.6166) | ✗ |
| **T4b(c)** | ⚑ **ARMED, NOT FIRED** — died at 156, not 160; law asserted cell-by-cell | law HELD |
| ring occupancy mean · max | 0.37717 · **3** | Lap R 3.24–3.43 |

⚑ **`E-9` REPLICATION EXACT.** l4l `160.16326530612247` and death wave `156` reproduce I-24's
pinned values read **from the I-24 findings JSON's own bytes**, never from my landing note's
renderings (`D-CON-6`'s law, applied to my own prior work).

⚑ **NOT A DESIGNATION, AND NOT A RUN BEST.** I-25 folds nothing and therefore designates nothing.
T2 0.87657 is **below I-21's 0.8815**, pinned from its own artifact. **`R-PM4-27 part 3`, seventh
consecutive iteration in which the best number sits on an arm the run may not carry.**

---

## 7 — THE SEED ENSEMBLE, **IN** THE RECORD CELL (`R-PM4-67 part 5`)

| salt | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| `L1` arrivals `N` (`PX-LO`) | 5 | 96 | 2 | 46 | 5 |
| `L0` arrivals `N` | **0** | 97 | **0** | 45 | **1** |
| largest ρ share | GEOMETRY | GEOMETRY | GEOMETRY | GEOMETRY | GEOMETRY |

⚑ **`E-8` HOLDS: the attribution RANKING is invariant 5/5** — GEOMETRY on every seed — **while the
magnitudes are not**, exactly as registered. **NO SEED IS SELECTED.** The record cell remains salt
0 because that is what I-24 declared, and it is labelled a continuity pin rather than a
representative value.

⚑ **AND THE ENSEMBLE PRODUCES A RESULT THE SINGLE SEED COULD NOT.** On salts 0 / 2 / 4 the
all-frozen probe yields **fewer than two in-window arrivals**, so `G(L0)` is **undefined** and
`F-I25` is **UNREACHED** on those cells — not a pass and not a fail. Without salts 1 and 3 the
falsifier would have had **nothing to fire on**. `R-PM4-67 part 5` earned its keep on its first
use.

---

## 8 — PRE-REGISTERED EXPECTATIONS, GRADED HONESTLY

| id | claim | grade |
|---|---|---|
| **`E-1`** | replay reproduces measured entry tick, ≥ 60 % within ±2, median ≤ 4 | ⚑ **FAILED — 11/12 cells hold; `ALL·PX-HI` salt 3 does not.** The contingency was **EXECUTED**, not softened (§ 3) |
| **`E-2`** | **MY LEAN** — geometry carries the largest share | ⚑ **HELD on the record cell** — and the SIGN is published beside it (§ 4.2: on `S-YZ·PX-HI` no share is positive at all) |
| **`E-3` = `F-I25`** | ⚑ **AGAINST THE COMMISSION'S FRAME AND MY OWN LEAN** — `G(L0) ≥ g_required` | ⚑ **HELD on 7/7 evaluable cells, 4.61–11.38×.** 5 cells UNREACHED (undefined `G`) |
| **`E-4`** | `N(L1)/n_bodies < 0.50` on `PX-LO` | ⚑ **HELD — 5/28 = 0.179** |
| **`E-5`** | `g_measured / g_required ≥ 5` on the record cell | ⚑ **HELD — 7.05×** |
| **`E-6`** | ⚑ **AGAINST MY OWN INTEREST** — churn carries less than the smallest named source | ⚑ **FAILED on 11 of 12 cells.** § 9 |
| **`E-7`** | re-path churn exactly zero | ⚑ **FAILED — 3 gate closures on `S-YZ·PX-HI`** (§ 2.3) |
| **`E-8`** | ranking invariant across the ensemble | ⚑ **HELD 5/5**, magnitudes vary; no seed selected |
| **`E-9`** | `S-YZ·PX-HI` replicates I-24 EXACTLY | ⚑ **HELD — exact** |
| **`E-10`** | non-perturbation, three legs | ⚑ **HELD — and against a PRIOR ARTIFACT** |

**Mechanical pins:** `P.1` `law_3.moved == {}` on **46** witnesses, **0** without provenance ✅ ·
`P.2` frozen **20/20** hard gate ✅ · `P.3` N-legs ✅ · `P.4` determinism ×2 ✅ · `P.5` pinned inputs
re-hashed EXACT, HALT armed ✅ · `P.6` `keys_asserted` on every wall row ✅ · `P.7` ring-literal AST
guard, site-exact, 2 named survivors ✅ · `P.8` `gate_open()` called **0** times by any census
module (AST) ✅ · `P.9` zero referent numerals in any branch condition in `kc2/` (AST) ✅ · `P.10`
ZERO FOLD, proven by prior-artifact identity ✅ · `P.11` smoke unchanged ✅ · `P.12` superlatives vs
pinned prior artifacts ✅.

---

## 9 — ⚑ `E-6` FAILED, AND ITS FAILURE IS A SECOND FINDING

Churn — the step from the SCHEDULE (`L1`) to what the sim actually did — moves `G` by
**0.142 – 0.265 s**, which is **larger than the smallest named source on every cell**:

| cell | `ΔG` churn | `ΔG` stagger | `ΔG` geometry | `ΔG` speed |
|---|---:|---:|---:|---:|
| `ALL·PX-LO` salt 0 | **0.2653** | 1.4694 | 0.2612 | 0.3537 |
| `S-YZ·PX-HI` | **0.1424** | 0.0583 | 0.1213 | 0.0636 |

**Step-level interference — blocking, separation displacement, the Gauss-Seidel order — is a real
contributor to the arrival spacing on 11 of 12 cells, and I predicted it would not be.** It does **not** dominate:
stagger moves `G` five times further on the record cell. **The honest reading is mid-rank, and the
prediction that put it last is FAILED.**

---

## 10 — DEFECT TABLE (all mine; the addendum ALONE and BEFORE its repair)

| id | defect | disposition |
|---|---|---|
| **`D-I25-1`** | my I-24-D landing read `PATROL_TO_NODE = 0` as *"expressible, never expressed."* The MECHANISM is that I-21 moved the record cell to `GATE_FIRST`, under which there is **no unconditional spawn→node leg at all** | **DISCLOSED in the math note § 1.2 BEFORE any code. NAMED, NOT REWRITTEN** — the I-24-D table is unedited. ⚑ It **NARROWED THE COMMISSION**: the "spawn-to-node assignment" is not on the arrival path on this board. Measured anyway; never given a rung |
| **`D-I25-2`** | after I-24 (b) the arrival path carries **TWO** radii (halt `D_ENGAGE_M` vs membership `fl32(r32²)`, Δ = 4.768372e-8 m) | **DISCLOSED in the math note § 1.3 BEFORE the replay was written.** Both imported by identity. `D-I24D-1` recognised **in advance** instead of after the fact |
| **`D-I25-3`** | my own law-3 wall check asserted a witness SHAPE I had not enumerated — it went RED on 24 of 45 witnesses that all HAVE provenance, in three valid forms | **REPAIRED BY STRENGTHENING** (addendum #1 `8c279e06`, **ALONE and BEFORE the repair**) into a **GROUP-EXACT provenance-form table** in which an **undeclared sixth group is itself an offender** — a clause the failing version did not have |
| **`D-CON-7`** | ⚑ **NONE.** The I-25 commission text states **no numerals**. `D-CON-6`'s law held one iteration after it was written | **AUDITED CLEAN, and recorded — a clean audit is a measurement too** |

> ⚑ **`D-I25-3` IS THE FOURTH MEMBER OF ONE FAMILY AND I AM NAMING THE FAMILY.** `D-I24D-2` (*a
> population is ENUMERATED, not recognised*), `D-I24-2` (*an allow-list is a claim about the
> codebase*), `D-I24-3` (*an isolation is READ OFF THE MATRIX*), and now `D-I25-3` (*a predicate
> about my own codebase is enumerated group by group, form by form*). **Every one is a claim about
> my own artifacts, REMEMBERED instead of READ. Sixth consecutive iteration in which my own
> pre-registration caught my own work before a number was reported.**

---

## 11 — `UNREACHED`, NAMED AND NOT APPROXIMATED

* **`UNREACHED-I25-1`** — the spawn-to-node assignment is MEASURED but is **not on the arrival
  path** under `GATE_FIRST`. What it would carry under `ZONE_FIRST` is not measured, and I-25 does
  not run a retired limb to find out.
* **`UNREACHED-I25-2`** — ⚑ **LAP AA IS IN FLIGHT, UNLANDED, AND WAS NOT CONSUMED.** I-25 is the
  SIM side of the joint question. Every *"the ring would need"* statement here derives from Lap R's
  OCCUPANCY, not from any decoded referent arrival structure.
* **`UNREACHED-I25-3`** — `W` is death-truncated, so `g_required` is conditional on the sim's own
  kill rate.
* **`UNREACHED-I25-4` (NEW, and it is the one that matters)** — **the BEARING term is MEASURED to
  carry 79 % of the surviving arrival order and is NOT DECODED.** Whether the referent's spawn
  bearings distribute as this arena's six cited emitters do is a Lap AA question, not a sim
  question.
* **Carried:** `UNREACHED-I24-1/2/3` · `UNREACHED-I24D-1` · `UNREACHED-Z-1` · `NAMED-Z-1/2/3` ·
  `UNREACHED-Y-1` · `UNREACHED-X-1` · the 17 unexpressed AI states · `T17` · `D-PDEF-2` ·
  `pools_for` default · `D-I21-1` (quantified, unrepaired).

---

## 12 — DIGESTS (full 64 hex, `R-PM4-55 part 2`)

### 12.1 Emitted

| artifact | sha256 |
|---|---|
| `output/kc2-pm4-i25-findings-20260816_075607.json` | `708916c13d612220d2f544fd266d08f6bb469bb48f9fce3d58e09aec614ab28b` |
| `math/kc2-pm4-i25-arrival-order-census-2026-08-16.md` | `ffe9f1b1233d8ba1362367c52123edf253c07e1b82d63ca4fe5a49eb397ccca9` |
| `math/kc2-pm4-i25-arrival-order-census-ADDENDUM-2026-08-16.md` | `43f5cc0341954422631c8dbf595c525ec357992c4df0c2008caeeb999f24131b` |
| `kc2/arrival_order.py` (**NEW**) | `ab0468d6fde72359a556933714ee2027ae0f81791182ec27a0eed46b65f0d148` |
| `scripts/gamora_kc2_pm4_i25_arrival_order_census_2026_08_16.py` | `422d87a21263cae4e3b8eae4ccc20ce110b975c7d606feaa14a9c3141d2b131a` |

⚑ **NO EXISTING `kc2/` MODULE CHANGED.** `run.py`, `ring.py`, `kinematics.py`, `intake.py`,
`engagement.py`, `player_locomotion.py` are untouched at I-25 — which is what makes wall row 6's
prior-artifact identity possible at all.

### 12.2 Consulted — re-hashed EXACT from bytes before any reducer ran (HALT armed; none fired)

| input | sha256 |
|---|---|
| **I-24 findings (the incumbent)** | `e7c2f1ba111b3be782d1dca034807c8db56365af7fc71ce6741f0887037d1993` |
| **I-24-D findings (the census baseline)** | `0e64fe317a46c1ba68dae495c2429e1f3faf794a4fa7f8742853775595a6f0c1` |
| I-23 findings | `0e4084b55f0af955f0b91d809da8e1b3267d6876a1c177a8eba3655c21048368` |
| Lap R `pm4r_contact_occupancy.csv` (**a GRADE**) | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` |
| Lap R `pm4r_findings.md` | `c223dfb04653a7e8682d5c1dd42356fc2a8398b06951372445d235a6eff224ea` |

Plus Lap Z (`ring.py`), Lap Y (`intake.py`), Lap U + Lap R (`kinematics.py`), Lap K
(`arrival.py`), Lap X (`intake.verify_substrate`) — **re-verified by the modules that own them**,
never by this driver (`NOTE-9`).

---

## 13 — THE WALL — **21/21 GREEN**, `keys_asserted` ON EVERY ROW

1 pinned inputs EXACT · 2 frozen **20/20** hard `SystemExit` · 3 `law_3.moved == {}` ·
4 **46** witnesses, **0** without provenance in their group's declared form, **no undeclared
group** · 5 every declared reducer parameter is a witness · 6 ⚑ **census-ON digests byte-identical
to the PINNED I-24 digests, 4/4 cells, surface AND knot** · 7 N-1/N-2/N-3 · 8 determinism ×2 ·
9 the `D-I24D-2` differencing probe · 10 the exhaustive exit partition closes on **12/12** ·
11 PC-a emitted with its full distribution · 12 PC-b graded against the declared band ·
13 additivity CHECKED, interaction REPORTED · 14 `gate_open()` **0** calls (AST) · 15 ring literals
(AST) · 16 referent numerals in branch conditions **0** (AST) · 17 `E-9` EXACT · 18 T4b(c) law ·
19 superlatives vs prior artifacts · 20 **ZERO FOLD** · 21 smoke unchanged.

**Law 3:** `moved == {}` on **46** witnesses across five groups — `PIN_FLOAT` 11 ·
`DICT_NOTE_OR_SOURCE` 35 — **0 offenders**. I-25 adds **three** constants and all three are
DECLARED REDUCER PARAMETERS (`PC_TICK_BAND` 2, `PC_MEDIAN_BAND` 4, `ADDITIVITY_TOL` 0.10) that
enter **no** simulation arithmetic.

**Smoke:** `296 pass / 1 PRE-EXISTING failure` (`test_AC_10_10` bare-30.0 AST guard,
`secondary_streams.py:136`) — **unchanged from I-23, I-24-D and I-24.**

---

## 14 — DO-NOT BLOCKS CARRIED, ENTIRE

Lap V § 7.2 · Lap V-2 § 11.2 · Lap W § 7.2 · Lap X § 12.2 · Lap Y § 11.6 · Lap Z § 5 (all seven
clauses). `2.4000000953674316` is never called the ring radius; no bit-identity is claimed;
`NAMED-Z-1` changes no body geometry; `NAMED-Z-3` stands as fidelity carry only (`R-PM4-67 part
4`); Lap R's occupancy bracket is a **GRADE**, carried as a bracket everywhere and asserted absent
from every branch condition in `kc2/` (wall row 16); the shipped tools, decoy records, constructor
defaults and EC-8 searches supply **no number**.

---

## 15 — CAVEATS THAT TRAVEL WITH THE NUMBERS

* **`PX-LO` at salt 0 is FIVE arrivals.** Every `PX-LO` share is reported beside the 98-arrival
  characterisation cell for exactly this reason, and the ensemble is in the cell for exactly this
  reason.
* **`G` is computed on in-window arrivals** and is therefore truncation-sensitive; `1/λ` is
  published beside it on every rung as the truncation-robust companion. **The pre-registered
  primary is unchanged and graded as written.**
* **Additivity FAILS on 9 of 12 cells.** No share here should be read as "source X carries Y % of
  the serialisation." The measurement supports **rankings** and **interaction**, not apportionment.
* **The replay is validated on 11/12 cells, not 12/12**, and the twelfth is excluded by name.
* **Lap AA is not consumed.** Nothing here is a statement about the referent's arrival structure.

---

## 16 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. ⚑ **THE TWELFTH NAME IS INCOMPLETE AND THE CENSUS NAMES WHAT IT MISSES.** `R-PM4-67 part 1`
   renamed the residual **THE ARRIVAL SCHEDULE — the spawn-to-node assignment and the per-body
   march clock.** Measured jointly: the spawn-to-node assignment is **not on the arrival path at
   all** on this board (`D-I25-1`), and the march clock's three named sources **do not carry the
   spacing** — freezing all three leaves it 4.6–11.4× above what the ring needs. **What does carry
   the ORDER is the per-body BEARING inside the spawn geometry, and 79 % of the order survives
   freezing everything the name points at.** If the residual gets a thirteenth name I would put it
   on **the spawn BEARING distribution**, not on the schedule.
2. ⚑ **THE RING DOES NOT NEED A SMALLER MEAN GAP. IT NEEDS THE p95 NOT TO EXIST.** Median measured
   gap 0.735 s against a requirement of 0.16 s is a 4.6× problem; **p95 = 7.02 s and max = 10.37 s
   are a different problem**, and they are what the dry runs I-24-D measured are made of. A fold
   aimed at the mean would not touch them.
3. ⚑ **`R-PM4-67 part 5` EARNED ITS KEEP ON ITS FIRST USE, AND IN A WAY WORTH BANKING.** On three
   of five seeds `F-I25` is **UNREACHED** because the falsifier's statistic is undefined; on the
   other two it fires. **A single-seed commission would have returned "undefined" and called it a
   result.** The rule should be sharpened: a stochastic limb's ensemble is where a falsifier
   becomes *evaluable*, not merely where its numbers get error bars.
4. ⚑ **`E-6`'s FAILURE IS A CANDIDATE LIMB AND IT IS CHEAP.** Step-level interference (blocking,
   separation displacement, Gauss-Seidel order) moves the arrival gap by 0.14–0.27 s — larger than
   the smallest named source. It is already instrumented (`n_blocked_steps` per body, per tick, on
   the ledger). **I am naming it, not decoding it** (`R-PM4-56 part 4`).
5. **`I-24-D`'s ZERO-DISPLACEMENT HEADLINE NEEDS THE § 2.4 QUALIFIER** before it travels further:
   on the I-24 record cell `displaced_player_moved` is 2/6 and 17/113, not 0/26. Different cell,
   different number, and the chapter reads differently with it.

---

*End of landing note.*
