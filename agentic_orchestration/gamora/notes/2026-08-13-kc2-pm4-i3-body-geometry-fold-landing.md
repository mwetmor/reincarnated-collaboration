# KC2-PM4 · I-3 — landing note: the geometry was never the term. **THE CONTACT RESPONSE IS.**

> **Run:** KC2-PM4 (replicate waves 150–160 faithfully) · **Iteration:** I-3, the MEASURED
> body-geometry fold · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Author:** gamora (simulation
> seam) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (ledger **L-6**)
> **Substrate:** legolas Lap F — `pm4f_body_radii.csv`, sha256 `80517e39…`, **digest-verified at
> FULL hash before load** (GL-6), vendored byte-identical as `data/kc2/pm4_body_radii.csv`
> **Math note (Discipline #1, written BEFORE the code, twelve pre-registered numeric predictions):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i3-body-geometry-fold-2026-08-13.md`
> **Rulings honoured:** R-PM4-7 (LO limb by explicit column) · R-PM4-8 (non-overlapping discs, 14
> ghosts, hit test UNCHANGED) · R-PM4-9 (player 0.32 m)
> **Status:** COMPLETE. Assert wall **14/14 PASS**, determinism ×2 **EXACT** on all three cells at
> BOTH layers with **ZERO masked diffs**, gate wall **67/67** on each of three batons at **FULL**,
> **20/20** batons re-gate green. **No HALT was hit. No constant was tuned.**

---

## 0 — The one-paragraph answer

**Lap F pre-registered a null: the measured radii would not make 54 co-resident bodies impossible
and might not re-discriminate the matrix. Lap F is right on its own basis and wrong on the sim's,
and I can now say exactly how much of each.** The disc-area ceiling binds on **7 of 864** contact
ticks — Lap F's argument, reproduced. But **56.49 % of I-2's co-resident PAIRS overlapped and
16.01 % were at exactly zero separation**, because pets materialised inside their summoners and
because `d_engage` collapses the board onto a 1-D ring whose capacity (21.5 at the wave-160 pet
mode) is **3.9× tighter** than the disc's. So the bound binds, hard: the reference cell's
overlapping-pair fraction goes **56.49 % → 0.01 %**, coincident **16.01 % → 0.00 %**, bodies
standing inside the player **20.29 % → 0.00 %**, max occupancy **54 → 23**, and **the share of kill
work above any packing ceiling is now exactly zero.** ⚑ **And then the fight came apart.** The
reference cell survives to **wave 169** in **556 s**; waves 151–160 alone take **326.78 s against
the measured 186 s (+75.7 %)**; CAMP dies on **wave 152**. **T1 MISSED, T2 MISSED, T3 MISSED.**
**§ 5 is the reading that matters, and it is not about radii:** running the **same invariant, the
same measured radii and the same everything else** through the *other* contact response — Jacobi
push-apart instead of block-and-dwell — puts the reference cell back on **wave 160 at 198.20 s
(+6.6 %)** with **max occupancy 32, zero coincident pairs and zero kill work above the ceiling.**
**R-PM4-8 ruled the INVARIANT. It did not rule the CONTACT RESPONSE — and the contact response,
which is nowhere in Lap F's substrate, is the dominant term.** That is the finding, and it is a
conductor ruling, not mine.

---

## 1 — ⚑ THE DEFECT THAT VOIDED MY FIRST MATRIX, AND ANOTHER SEAM'S GATE FOUND IT

Before any numbers: **I ran this matrix twice, and the first run is VOID.** I am putting this first
because the void numbers would otherwise be the interesting ones.

`max_admissible_travel` evaluated the already-overlapping ("non-worsening") arm through the
quadratic, on my own math-note argument that substituting `s = ‖w‖` collapses it to `D = (w·u)²`
and yields both arms from one formula. **Algebraically true. Numerically false.** With
`s = sqrt(w2)`, `w2 − s*s` is not exactly zero in binary floating point — **measured at the failing
pair: `+1.39e-17`** — so `root` can land a few ULP **above** `|w·u|`, which flips the "blocker is
behind" test (`t₂ ≤ 0`), sends the code down the clamp arm, and **returns `travel = 0` for a body
moving AWAY from its blocker.**

**Consequence, measured:** two roster bodies whose wave-roll scatter overlapped
(`ghost_b03`/`ghost_b04`, 0.316 m apart needing 0.700) blocked each other on **379 of 379 steps**
and neither ever moved.

**How it was caught: `R-LOCO-1`, star-lord's own gate, REFUSED the emission** —
*"5 of 116 actors span time without moving … 0 of those spawned INSIDE `d_engage_m=2.4` … 5 are
unexplained and RED."* The gate's own halt text says *"nothing here is repaired by widening a
tolerance"*, and nothing was: the gate was right, my solver was wrong, and no baton had been
written. **A gate in another seam found a simulation-seam defect, on its first contact with a
model change it had never seen.** Filed as **D-I3-3, mine.**

**The repair** drops the algebraic cleverness and evaluates the degenerate arm exactly —
already-overlapping and moving away or tangentially ⇒ unconstrained; moving toward ⇒ travel 0.
Unit-proved on the exact pair that deadlocked (away 0.200 allowed / toward 0.000 / tangent 0.200).
Math note **§ C.2.1** carries the correction with **the falsified paragraph left standing**: a
pre-registered claim is part of the record, not something to quietly edit.

**⚑ THE VOID NUMBERS, PUBLISHED SO THE CORRECTION IS AUDITABLE:** the first matrix read death on
**wave 156** at 213.88 s, CAMP failing to clear wave 151 at the tick cap, max occupancy 11, N_eff
2.19, overlap 0.65 %. **Every one of those was produced by frozen bodies, not by the measured
geometry. They are not this lap's result and they are not quoted anywhere else in this note.**

---

## 2 — What landed

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code, twelve pre-registered predictions; § C.2.1 appended post-hoc) | `simulation/math/kc2-pm4-i3-body-geometry-fold-2026-08-13.md` | `33b11c8e` / `284f95d0` |
| 2 | **the geometry module** — loader, limb-by-column, ghost/zero census, the analytic non-worsening clip, deterministic shell placement + constructed ray fallback, the exactness-preserving spatial index, ring/disc capacity arithmetic, `separate_overlaps` (diagnostic) | `simulation/kc2/geometry.py` **(new)** | `33b11c8e` |
| 3 | `Mover.radius_m` / `.ghost` / blocked-step instrumentation + `step(blockers=…)` | `simulation/kc2/locomotion.py` | `33b11c8e` |
| 4 | blocker sets, the three order-pinned loops, pet placement, the player clip, `waves[].body_geometry` | `simulation/kc2/run.py` | `33b11c8e` |
| 5 | **`PetActor.entity_radius_m`** (additive, nullable) | `export/baton_v1_schema.py` | `33b11c8e` |
| 6 | `body_geometry` + `contact_response` spec fields · `_geometry_kwargs()` · 3 specs · `entity_radius_m` on actors AND pets · inventory rows | `export/kc2_run_adapter.py` | `33b11c8e` / `284f95d0` |
| 7 | **driver + assert wall (14) + determinism + census + three diagnostics** | `simulation/scripts/gamora_kc2_pm4_i3_body_geometry_fold_2026_08_13.py` | `33b11c8e` |
| 8 | **vendored substrate**, byte-identical, SHA-pinned | `data/kc2/pm4_body_radii.csv` | `33b11c8e` |
| 9 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `33b11c8e` |
| 10 | **D-I3-3 repair** + math note § C.2.1 + adapter re-pin | as above | `284f95d0` |
| 11 | **3 batons + 3 knots supplies + findings** | `src/reincarnated/output/`, `simulation/output/` | (artifact commit) |

### ★ THE THREE SIBLING BATONS — FULL grade, **67/67 each**

| cell | file (`src/reincarnated/output/`) | sha256 |
|---|---|---|
| CAMP / DEF-OFF (control) | `kc2-baton-v1-…-pm4-i3-camp-defoff-20260813_081026.json` | `7e28552b5eed22f56b0f4dd26992a0be1821cd94ab1aa0abd15517435ca8d9d2` |
| CLUSTER / DEF-OFF (isolation) | `…-pm4-i3-cluster-defoff-20260813_081033.json` | `c627ac872ae899d83441524c374cdedfabf4db5964622f7a6dd76267de383dbe` |
| **CLUSTER / DEF-ON** ← reference | `…-pm4-i3-cluster-defon-20260813_081040.json` | `23ba0d4418b8b0e0c807a9e7e03e7183f372938b40a13f64cf2c59341ea45a79` |

Knots supplies (`simulation/output/`, stamp `20260813_080807`): `6c90d859…` / `341687b7…` /
`7211d480…`; findings `kc2-pm4-i3-findings-20260813_080807.json` `37a0b302e2b87d24…`.

**All seventeen prior batons verified from bytes, read read-only, never written, and
`20 / 20 re-gate GREEN`** (67/67 each) against the post-I-3 code surface — so the additive
`PetActor.entity_radius_m` cost nothing anywhere.

---

## 3 — ⚑ THE ONE DELTA, **PROVED** RATHER THAN ASSERTED (assert-wall check 1)

Every prior lap claimed its delta was one thing. **This one measures it.** Each of the three cells
was replayed with the geometry arguments **absent** (not `None` — absent, so `simulate_wave` takes
its pre-I-3 default arm) and the full emitted sim surface digested:

| cell | fold-OFF surface digest | I-2's recorded digest | |
|---|---|---|---|
| CAMP/DEF-OFF | `b6f279dc8ba73b42…` | `b6f279dc8ba73b42…` | **EXACT** |
| CLUSTER/DEF-OFF | `4d54e75d0ecd7882…` | `4d54e75d0ecd7882…` | **EXACT** |
| CLUSTER/DEF-ON | `b846f73b0f7d1126…` | `b846f73b0f7d1126…` | **EXACT** |

**This is the check that makes the rest of the note readable.** It proves that the new module, the
new spec fields, the new schema field, the new wire keys **and both iteration-order pins** (movers
and pets are now stepped in `sorted(actor_id)` because non-penetration makes those loops
order-dependent) are **inert when the fold is off**. It also runs FIRST in the driver, before a
single cell of record, and HALTs the lap on mismatch.

---

## 4 — Determinism ×2 (charter law, FG-10), at BOTH layers — **ZERO masked diffs**

**SIM layer** — each cell replayed twice, full emitted surface deep-compared:

| cell | surface digest | leaves | differences | verdict |
|---|---|---:|---:|---|
| CAMP/DEF-OFF | `0393ebbe34f4b3a3…` | 47,426 | 0 | **EXACT** |
| CLUSTER/DEF-OFF | `ca9ccc5bcc6eac8c…` | 286,369 | 0 | **EXACT** |
| CLUSTER/DEF-ON | `17976582014ec3b9…` | 271,031 | 0 | **EXACT** |

*(digests above are from the pre-repair run's structure; the post-repair run re-ran all three and
also returned 0 differences on every cell — the driver HALTs on any mismatch and did not.)*

**BATON layer — using star-lord's `mask_volatile()`, the seam's ONE application, imported not
restated:**

| cell | A ≡ B masked | masked digest | A ≡ **ON-DISK** |
|---|---|---|---|
| CAMP/DEF-OFF | **EXACT** | `ba832cc656aab143…` | **EXACT** |
| CLUSTER/DEF-OFF | **EXACT** | `6451821012725ca4…` | **EXACT** |
| CLUSTER/DEF-ON | **EXACT** | `a5a5f0755df19e29…` | **EXACT** |

⚑ **THE KNOWN DEFECT IS GONE.** At I-1 and I-2 the masked compare of a fresh build against the
on-disk record showed **exactly one** difference per cell
(`sim_pin.tree_state_untracked_entries_excluded`), handed back twice and not taken. Star-lord's
depth-recursive `mask_volatile()` closes it: **zero differences, on all three cells, at both
compare points.** The charter said any diff is a failure; there is none.

---

## 5 — ⚑ THE MATRIX, vs the MEASURED reference truth

> **Reference truth, MEASURED (Lap C, charter Law 4): Matt DIED ON WAVE 160.** Ten waves in
> **186 s** (682 → 868 s), per-wave 14 / 17 / 29 s min/med/max, sharp slowdown on the last two.

| cell | waves | **death wave** | ToD | kills | pets | N_eff | max occ | overlap | coincident | in-player | ring-frac | radial med |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CAMP / DEF-OFF | 2 | **152** | 524.57 s | 315 | 530 | 1.118 | **5** | 0.0000 | 0.0000 | 0.0000 | 0.633 | 2.400 |
| CLUSTER / DEF-OFF | 20 | **170** | 646.45 s | 1,996 | 1,817 | 3.346 | **17** | 0.0000 | 0.0000 | 0.0000 | 0.114 | 2.208 |
| **CLUSTER / DEF-ON** ← reference | 19 | **169** | 556.08 s | 1,833 | 1,655 | 3.368 | **23** | 0.0001 | 0.0000 | 0.0000 | 0.125 | 2.209 |

**vs the I-2 baseline (`…-pm4-i2-cluster-defon`, `355ddfd7…`), same cell:**

| quantity | I-2 | **I-3** | Δ |
|---|---:|---:|---|
| **death wave** | **160** | **169** | **+9 waves** |
| waves cleared | 9 | 18 | +9 |
| **time of death** | 186.12 s | **556.08 s** | ⚑ **not like-for-like — see below** |
| **waves 151–160 ONLY, like-for-like** | **186.12 s** | **326.78 s** | **+75.6 %** |
| bodies killed | 767 | 1,833 | (19-wave basis) |
| pets spawned | 620 | 1,655 | (19-wave basis) |
| **`N_eff`** (rows / contact tick) | **4.764** | **3.368** | **−29.3 %** |
| **max occupancy** | **54** | **23** | **−57.4 %** |
| share of kill work at occ ≥ 10 | 39.1 % | 14.3 % | −63 % |
| share of kill work at occ ≥ 26 | 15.8 % | **0.00 %** | **−100 %** |
| **share at occ ≥ 36 (above ANY ceiling)** | **8.3 %** | **0.00 %** | **−100 %** |
| **overlapping pairs** | **56.49 %** | **0.01 %** | **−99.98 %** |
| **exactly-coincident pairs** | **16.01 %** | **0.0000 %** | **−100 %** |
| **rows from a body inside the player** | **20.29 %** | **0.00 %** | **−100 %** |
| rows at the engage ring (±0.01 m) | 1.85 % | **12.45 %** | **×6.7** |
| radial median of co-resident bodies | 1.662 m | **2.209 m** | +32.9 % |
| mean HP | 96.1 % | 96.8 % | +0.7 pts |
| dry fraction (run) | 0.621 | 0.465 | −25 % |

⚑ **NOTE-9, and it is load-bearing: `time of death` is NOT like-for-like when the death wave
differs.** A 19-wave fight's duration and a 10-wave fight's duration are different quantities
wearing one name. **The honest comparison is the waves-151–160 sub-total: 326.78 s vs the measured
186 s, +75.7 %.** Both numbers are on the wire; the scorecard carries a `like_for_like: false` flag
so the caveat cannot be dropped downstream.

---

## 6 — ⚑ THE T-BAND SCORECARD

| band | verdict | number |
|---|---|---|
| **T1** survival depth (wave 160) | **MISSED** | death on **wave 169** — nine waves too deep. Not a near-miss in either direction of the band {159–161} |
| **T2** duration, ±15 % of 186 s (158.1–213.9) | **MISSED** | ToD **556.08 s**; **like-for-like waves 151–160 = 326.78 s, +75.7 %**. The raw ToD would read "MISSED long" either way, and `like_for_like: false` is on the wire |
| **T3** pacing shape | **MISSED** | median ratio **1.988** over the ten comparable waves; **Pearson r 0.589** (I-2: 0.697 ex-154). Every wave slower; direction of the 158→159 slowdown **reproduced** (31.84 → 52.65 s, ×1.65 vs reference ×1.86) |
| **T4a** sustain-through-throughput | **MET** | mean HP **96.8 %**; **77 / 6,806** ticks below half; ADCtH **128.3 M** offered against **2.01 M** intake |
| **T4b** terminal mechanism | **MISSED (third consecutive)** | ⚑ **but it inverted.** Terminal wave **43.10 s** with **3,237 player damage rows** — the FOUGHT clause is MET for the first time in the run (I-1 and I-2 both had **7 s and ZERO rows**). It fails on **DoT 0.49 %** of its 892,757 intake, and on being wave **169** |

**T4b deserves one more sentence.** For two laps the terminal wave was a 7-second approach burst in
which the player never swung. It is now a 43-second fight in which the player lands 3,237 damage
rows. **The clause that failed changed** — the band now fails on *DoT involvement*, not on
*whether a fight happened*. That is a real movement on a band that no eHP fold could touch, and it
happened for a reason this lap can name: bodies that cannot crowd cannot burst.

---

## 7 — ⚑ WHERE THE CONSTRAINT ACTUALLY BOUND (the question the conductor asked)

**Not on the disc's area. On the ring, on the approach, and on creation.**

### 7.1 — Lap F's null, confirmed on its own basis

| test | I-2 reference cell | verdict |
|---|---:|---|
| contact ticks violating `Σπrᵢ² ≤ η·π·(R+r_max)²` (Lap F § 6) | **7 / 864 = 0.81 %** | **Lap F is RIGHT: the disc has room on 99.2 % of ticks** |
| centre-in-disc ceiling at the wave-160 pet mode r = 0.35 | **83.1** | 54 observed — not impossible |
| centre-in-disc ceiling at the board median r = 0.50 | **44.4** | Lap F's D-I2-1 correction, reproduced exactly |

### 7.2 — and the capacity Lap F did not compute

Every body's travel is clipped to `max(0, dist − d_engage)`, so **`d_engage` is the circle the
board is driven onto.** Two bodies of radius `r` on that circle need `Δθ ≥ 2·arcsin(r/d_engage)`:

```
N_ring ≤ π / arcsin(r / d_engage)
```

| r (m) | **ring N** | centre-in-disc N | ratio | what carries it |
|---:|---:|---:|---:|---|
| **0.35** | **21.5** | 83.1 | **3.9×** | the whole wave-160 pet board |
| 0.40 | 18.8 | 65.5 | 3.5× | Aleksander's Shard |
| 0.50 | 15.0 | 44.4 | 3.0× | board median |
| 0.60 | 12.4 | 32.6 | 2.6× | ROSTER-169 median |
| **0.75** | **9.9** | 22.7 | 2.3× | **the Korvaak statue, ×2 on wave 160** |

**The ring ceiling is 2.3×–3.9× tighter than the disc's, and it is the ring the kinematics drive
every body onto.** Lap F computed the capacity of the room; the sim seats everybody at one table.

### 7.3 — and the two mechanisms that made 56 % of pairs overlap in the first place

1. **Creation.** `run.py` wrote the summoner's exact coordinates into every new pet, so a 12-burst
   summon made a **twelve-body point stack at zero separation inside the summoner's own body**.
   That one line produced **16.01 % of every co-resident pair**. Post-fold: **1,614 placements,
   1,614 displaced, 0 forced overlaps, 3,038 m of total displacement.**
2. **Freezing.** A body inside `d_engage` has travel identically zero **forever**. Under CLUSTER
   the player walks into the density centroid and drags its 3.0 m disc over a field of frozen
   bodies — which is why **20.29 % of I-2's kill work came from bodies the player was standing
   inside**, and why the co-resident population sat at a radial median of 1.662 m rather than on
   the ring. Post-fold: **0.00 %**, radial median **2.209 m**, ring occupancy **×6.7**.

### 7.4 — the intake side, measured

| | roster | pets | player |
|---|---:|---:|---:|
| blocked steps (reference cell) | **21,331** | **108,004** | **1,983** |
| blocked travel (m) | 5,807 | 28,035 | 819 |

**The approach column is where the mass of the constraint lives** — 108 k blocked pet-steps against
1,983 blocked player-steps.

---

## 8 — ⚑ MATRIX-DISCRIMINATION VERDICT: **IT RE-DISCRIMINATES. Lap F's null is FALSIFIED on this clause, and the conductor's L-4 expectation is CONFIRMED.**

| | I-2 | **I-3** |
|---|---|---|
| CAMP / DEF-OFF | wave 160, 806.61 s | **wave 152, 524.57 s** |
| CLUSTER / DEF-OFF | wave 160, 188.73 s | **wave 170, 646.45 s** |
| CLUSTER / DEF-ON | wave 160, 186.12 s | **wave 169, 556.08 s** |
| **spread, CLUSTER DEF-ON vs DEF-OFF** | **1.40 %** | **16.3 %** (and one wave of depth) |
| **CAMP vs CLUSTER** | same death wave | **17 waves apart** |

At I-2 I wrote that *"a matrix that stops discriminating has stopped being an instrument."* It is
an instrument again. **My P.7 predicted `> 2.5 %` and argued the mechanism from CAMP's worse
stacking; the measured spread is 16.3 % and CAMP now separates by seventeen waves.** The
matrix-redesign trigger the conductor armed at L-4 **does not fire**.

---

## 9 — ⚑ THE READING THAT MATTERS: THE CONTACT RESPONSE, NOT THE RADII

**R-PM4-8 ruled the INVARIANT** — living bodies are non-overlapping discs. **It did not rule the
CONTACT RESPONSE**, and Lap F could not decode one (C-F2: the base collision rule is
engine-internal; C-F6: `pathMass` is emitted and undescribed). I pre-registered **block-and-dwell**
(C-I3-1: a blocked body stops; it does not slide) and declared the risk in math note § C.4.

**So I ran the other one as a DIAGNOSTIC — same invariant, same MEASURED radii, same seed, same
board, same everything, resolved by Jacobi push-apart after motion instead of by blocking during
it. The player absorbs no displacement, so a diagnostic about monster crowding cannot become a
change to the player model (that is Iteration 4's).**

| | I-2 (no geometry) | **I-3 matrix of record** (block) | **DIAGNOSTIC** (separate) | reference truth |
|---|---:|---:|---:|---:|
| **death wave** | 160 | **169** | **160** | **160** |
| **ToD** | 186.12 s | 556.08 s | **198.20 s (+6.6 %)** | **186 s** |
| waves 151–160 | 186.12 s | 326.78 s | **198.20 s** | 186 s |
| `N_eff` | 4.764 | 3.368 | **4.220** | — |
| max occupancy | **54** | 23 | **32** | — |
| share of kill work ≥ 36 | **8.3 %** | 0.00 % | **0.00 %** | — |
| exactly-coincident pairs | **16.01 %** | 0.00 % | **0.00 %** | — |
| overlapping pairs | **56.49 %** | 0.01 % | 10.09 %¹ | — |
| rows inside the player | **20.29 %** | 0.00 % | 11.06 % | — |
| CAMP control | 806.61 s / w160 | **524.57 s / w152** | **806.61 s / w160** | — |

¹ the Jacobi residual at 4 passes — push-apart converges, it does not enforce. **The blocking
response enforces the invariant more strictly (0.01 %); the separating response reproduces the
fight.** Both facts are reported; neither is chosen here.

**⚑ THE STATEMENT, AS PLAINLY AS I CAN PUT IT.** Giving the bodies their MEASURED space back
removes **100 % of the physically-impossible density** — occupancy ≥ 36 goes from 8.3 % of kill
work to zero, coincident pairs from 16.01 % to zero — **under BOTH responses.** What decides
whether the fight still replicates is **which contact response you pick**, and that choice is
**not in the substrate**. Under block-and-dwell the sim's straight-line pursuit has no way around
an obstacle, so the board becomes a **single-file queue**: CAMP's stationary player is besieged by
a line that cannot spread (max occupancy **5**, 63 % of rows exactly on the ring), and CLUSTER's
player survives nine waves too long because bodies that cannot crowd cannot burst.

**This is a conductor ruling, not mine.** I have implemented, measured and published both; I have
not chosen. The queue is not a defect to patch — it is the honest composition of two DECLARED
simplifications (straight-line locomotion, no contact response), and **the correct next move is a
ruling about which response R-PM4-8 intends, not a tuning pass.**

---

## 10 — ⚑ THE PLAYER-BODY ISOLATION (R-PM4-8's "…and vs the player")

Ghosting **only** the player, changing nothing else:

| | reference cell | **player ghosted** |
|---|---:|---:|
| death wave | **169** | **156** |
| ToD | 556.08 s | **144.65 s** |
| `N_eff` | 3.368 | 2.877 |
| rows from a body inside the player | 0.00 % | **16.36 %** |
| radial median | 2.209 m | 1.763 m |

**The player's own 0.32 m body is not a rounding — it is worth thirteen waves of survival.** A
player that can be body-blocked stays at the crowd's edge; a player that cannot walks into the
middle, takes 16 % of its kill work from bodies it is standing inside, and dies. **R-PM4-8's
symmetric arm is load-bearing, and had I implemented the asymmetric rule (monsters blocked, player
free) this lap would have reported a very different fight for a reason nobody could have seen.**

---

## 11 — ⚑ THE HI-LIMB SENSITIVITY (R-PM4-7: reported, NOT run — no second matrix)

| quantity | LO (of record) | HI (sensitivity) | Σ effect |
|---|---:|---:|---|
| board median radius | **0.500** | 0.600 | **×1.20** |
| ROSTER-169 median | 0.600 | 0.810 | ×1.35 |
| SUMMON-128 median | 0.360 | 0.404 | ×1.12 |
| board maximum | 2.000 | 2.250 | ×1.13 |
| ring capacity at the pet mode | **21.5** | 18.6 | **−13.2 %** |
| ring capacity at the board median | **15.0** | 12.4 | **−16.9 %** |
| centre-in-disc ceiling at the board median | 44.4 | 32.6 | −26.6 % |

**⚑ AND THE SHARPEST EDGE IS NOT A MAGNITUDE — IT IS A STRUCTURAL INCONSISTENCY, AND IT IS AN
ARGUMENT FOR THE LO LIMB THAT R-PM4-7 DID NOT HAVE WHEN IT RULED.**

A body of radius `r` can stand at `d_engage` from the player only if `r + 0.32 ≤ 2.400`, i.e.
`r ≤ 2.080`.

* **LO limb: 0 of 297 records are blocked from their own engagement distance.** The board maximum
  is `aetherialcommander_01` at **2.000**, and `2.000 + 0.320 = 2.320 ≤ 2.400` — a margin of
  **0.080 m** on the worst body in the corpus. The limb of record composes with the sim's own
  DB-cited `D_ENGAGE_M` **exactly, with room to spare.**
* **HI limb: exactly ONE record is blocked — `statue_korvaaktombguardian` at 2.250**, whose
  `2.250 + 0.320 = 2.570 > 2.400`. **It could never reach `meleeTargetDistance`.**

R-PM4-7 chose LO because it is conservative for the term under test. **It is also the only limb
under which every body can occupy the distance the game tells it to occupy.** Two independent
reasons, one limb. *(This is a consistency finding, NOT a decode of `scale` — Lap F's C-F1 stands:
four discriminators, none decisive.)*

---

## 12 — ⚑ THE KORVAAK STATUE ON THE TERMINAL WAVE (explicitly flagged by R-PM4-7)

**The wave-160 roster is five bodies on four records, and `statue_korvaaktombguardian` rolls
twice** (`w160_a003`, `w160_a004`) — the board's only `scale = 3.0`.

| actor | record | **LO** | HI | ring arc `2·arcsin(r/2.4)` | share of the ring |
|---|---|---:|---:|---:|---:|
| `w160_a000` | `nemesis_kymon_01` | 0.500 | 0.675 | 0.4200 rad | 6.7 % |
| `w160_a001` | `nemesis_wendigo_01` | 0.700 | 0.980 | 0.5946 rad | 9.5 % |
| `w160_a002` | `nemesis_aetherialvanguard_01` | 0.400 | 0.540 | 0.3352 rad | 5.3 % |
| **`w160_a003`** | **`statue_korvaaktombguardian`** | **0.750** | **2.250** | **0.6356 rad** | **10.1 %** |
| **`w160_a004`** | **`statue_korvaaktombguardian`** | **0.750** | **2.250** | **0.6356 rad** | **10.1 %** |
| | **roster total** | | | **2.6179 rad** | **41.7 %** |

Plus the 30 pets it spawns: 12 × `wraith_b01_summon` (0.350) + 12 × `wraith_c01_summon` (0.350) +
6 × `aetherialvanguard_crystal` (0.400 — Aleksander's Shard).

**Under the LO limb of record the two statues consume 1.271 rad = 20.2 % of the engage ring between
them**, and every wave-160 body can reach the ring. **Under HI neither statue could reach it at
all** — they would be held **0.170 m outside the circle they are walking toward, permanently, on
the death wave.** ⚑ **The camera-measure escalation R-PM4-7 named is NOT fired: the LO limb
produces no terminal-wave residual that implicates it.**

---

## 13 — ⚑ PRE-REGISTERED PREDICTIONS vs OUTCOME — **four confirmed, one split, seven falsified**

| # | prediction (written before the code) | outcome |
|---|---|---|
| **P.1** | coincident pairs → **0**; overlapping pairs 56.49 % → **< 3 %** | **CONFIRMED.** 0.0000 % and **0.01 %**. The residue is exactly what I said it would be — configurations frozen before the constraint could act (§ 15 C-I3-5) |
| **P.2** | max occupancy 54 → **20–32**, centre 26 | **CONFIRMED. 23.** The one magnitude I got right, and I got it from the ring formula rather than the disc formula |
| **P.3** | mean `N_eff` 4.764 → **3.6–4.4**, centre 4.0 | **FALSIFIED on the low side, direction right.** **3.368**, under my floor. I under-priced how much of the crowd the queue keeps outside the disc |
| **P.4** | **THE HEADLINE — ToD 205–250 s, T2 MISSED LONG** | **⚑ FALSIFIED on magnitude, right on sign and verdict.** Like-for-like waves 151–160 = **326.78 s**, 31 % above my ceiling; raw ToD 556.08 s over 19 waves. § D.1's occupancy-cap arithmetic said the packing channel alone could only pay ×1.08 and predicted ~200 s if the other channels were zero. **They were not zero — they were the whole thing** |
| **P.5** | T1 holds at **wave 160** | **⚑ FALSIFIED, and in the direction I did not consider.** **Wave 169.** I reasoned only about the fight getting slower and never asked what a body that cannot reach the player does to INTAKE. It stops dealing damage |
| **P.6** | T4b MISSED; terminal 5–11 s, **0** player rows, intake 19–23 k | **FALSIFIED on every clause except the verdict.** **43.10 s, 3,237 player rows, 892,757 intake.** The verdict is right for a completely different reason, which is the least useful way to be right |
| **P.7** | **⚑ I DISSENT FROM LAP F: it re-discriminates.** Spread > 2.5 % | **CONFIRMED, and by 6.5×.** Spread **16.3 %**; CAMP separates by **seventeen waves**. Lap F's null is falsified on this clause and the conductor's L-4 expectation holds |
| **P.8** | rows inside the player 20.29 % → **< 3 %**; ring rows 1.85 % → **> 8 %**; radial median → 2.0+ | **CONFIRMED on all three clauses.** **0.00 % · 12.45 % · 2.209 m** |
| **P.9** | all waves slow; T3 median ratio **1.20–1.60**; wave 159 → **30–50 s** | **FALSIFIED, both narrowly, both in the predicted direction.** Median ratio **1.988**; wave 159 **52.65 s** |
| **P.10** | T4a MET; ADCtH 40–47 M | **SPLIT.** Verdict **MET** ✓; magnitude **128.3 M** ✗ — but on a 19-wave basis my band was computed for a 10-wave fight, which is a NOTE-9 error in my own prediction |
| **P.11** | kills rise to **800–950** | **FALSIFIED. 1,833** — same basis error as P.10 |
| **P.12** | CAMP: 2 capped waves, ToD **> 806.61 s** | **FALSIFIED.** CAMP **died on wave 152 at 524.57 s** — it never got the chance to cap |

**The unifying error, and it is a NEW shape.** At I-1 I priced sustain and never priced exposure.
At I-2 I priced eHP and never priced co-residence. **Here I priced the player's THROUGHPUT and
never priced the monsters' REACH.** Every one of P.3/P.4/P.5/P.6/P.11/P.12 is wrong because I asked
"how fast can the player kill a crowd it cannot pack" and never asked **"what happens to a body
that can no longer get to the player at all."** The answer is that it stops attacking, the player
stops taking damage, and the whole fight inverts. **§ D.1's arithmetic was correct and irrelevant:
it bounded the channel I was looking at.**

---

## 14 — ⚑ DEFECTS AND UNDER-READS (Discipline #11)

| # | what | how found | effect |
|---|---|---|---|
| **1** | **⚑ D-I3-3, MINE, AND THE MATH NOTE'S OWN ARGUMENT IS WHAT PRODUCED IT.** The non-worsening arm evaluated through the quadratic freezes a body moving AWAY from its blocker, because `w2 − s*s` with `s = sqrt(w2)` is not exactly zero (+1.39e-17 measured) | **star-lord's `R-LOCO-1` gate REFUSED the emission** — "5 of 116 actors span time without moving, unexplained" | Two overlapping spawn-mates deadlocked for **379 of 379 steps**. **The first I-3 matrix is VOID** (§ 1). Repaired exactly; math note § C.2.1 carries the correction with the falsified paragraph left standing |
| **2** | **⚑ D-I3-1 — a spatial cull sized for the WRONG position.** `place_body`'s blocker set was queried at the spawn ORIGIN, but depenetration WALKS: a 12-burst summon's far end leaves any neighbourhood queried at the origin | the non-overlap census showed 14 `springscrab_a00_summon` pairs still at **exactly zero separation** after the fold claimed to have removed them | The placement now pays the exact O(N) blocker set (placements are hundreds per run against millions of step-clips, so the cull stays where it is safe). **A cull that is exact for the query it was sized for is not exact for a query that moves.** |
| **3** | **D-I3-2 — a body spawned this tick was in `live` but not in the spatial index**, so a stepping pet was never even OFFERED it as a blocker and walked through it | same census, after fixing D-I3-1 and finding a smaller residue | The index is now rebuilt after the summon loop. **Both of these were found by the independent `O(N²)` sweep over EMITTED positions — the incremental solver reported success both times** |
| **4** | **⚑ MY OWN SCORECARD READ THE WRONG EVENT FAMILY.** T4b's intake filtered `event_type == "damage_taken"` — a family the schema **does not have**. `R-25` puts DIRECTION on `target_id`: incoming damage is `damage_dealt` with `target_id="player"` | the terminal-wave DoT share read **100.0 %**, which is exactly the kind of number that becomes a finding | The first draft of this scorecard would have reported "the terminal wave is pure DoT" — the T4b band's own clause — **off a basis error.** Corrected to 0.49 %; caught by the sum disagreeing with `summary.damage_total` |
| **5** | **CLIFF C-I3-5, declared not fixed.** 20 of 3,369 roster pairs (**0.59 %**) are ALREADY overlapping when the wave roll scatters them, worst penetration 1.48 m | the census residue, traced pair by pair | This is the **entire** residue of the non-overlap invariant. The roster's scatter is a SIM-ROLLED position with provenance that `actors[].spawn_x/spawn_y` and every knot path ride on; re-placing it is a larger semantic shift than this iteration's scope. **The size of what I decline to touch is a number, not a hand-wave** |
| **6** | **The I-2 findings artifact's digest in the charter lineage did not match its bytes** (`9236e17de25c30af6b…` quoted vs `9236e17de25c30af68…` on disk) | GL-6 verification, which HALTed the driver on the first run | The two agree on the first 16 hex characters and diverge at the 17th. **A prefix compare would have accepted it.** I pinned the byte-verified value and this is exactly why the charter says FULL hash |

---

## 15 — DECLARED ASSUMPTIONS + CLIFFS (every one on the wire)

**⚑ C-I3-1 — NO CONTACT RESPONSE BEYOND STOPPING, AND IT IS NOW THE DOMINANT TERM.** A blocked body
advances as far as it can along the direction it already had and halts; it does not slide, push or
re-route. Contact response is **not in Lap F's substrate** — C-F2 (base collision rule is
engine-internal, a hostility relation with no table anywhere) and C-F6 (`pathMass` emitted,
undescribed) — so inventing one is a GL-12 violation. **§ 9 measures what it costs.**

**⚑ C-I3-3 — SPAWN PLACEMENT IS A MODEL ADDITION, NOT A DECODE**, and a Discipline #12 semantic
shift: `waves[].pets[].spawn_x/spawn_y` were "the summoner's position" and are now "the nearest
admissible position to the summoner". Deterministic, **no length constant** (every shell radius is
a sum of MEASURED radii; every shell's bearing count is the same `π/arcsin(r/ρ)` formula as the
capacity bound; the phase is the player→summoner bearing), with a constructed ray-sweep fallback
that **cannot fail** — `forced_overlap_spawns` is **0** on every cell and that is asserted, not
hoped.

**C-I3-5 — roster spawn positions are NOT re-placed** (§ 14 defect 5). **0.59 % of pairs**,
measured.

**C-F1 — `scale` is undecided** (Lap F: four discriminators, none decisive). The run rides LO by
R-PM4-7; § 11 prices HI; § 12 prices the korvaak fork.

**C-F3 — `collisionShape` is unset on 297/297.** This fold rides discs, which is the abstraction
the sim already runs. **C-F4 — the 17 MEASURED zero-radius bodies enter as POINTS and are never
back-filled.** **C-F5 — `actorHeight` is measured and unused; the disc is 2-D.**

**Carried unchanged from I-2:** C-I2-1 pet population is still Lap-B's 70 of 128 · C-E3
`monsterLevelGapFixer` still parked · C-E1 · C-D2 / C-D3 / R-PM4-6 (the named gap did not roll) ·
pet damage on the PM-2 threat fold · `percent_current_life` still unverifiable · wave 154's
38.12 s travel outlier, **undiagnosed since PM-2 and unchanged again** · `max_ticks = 4000`.

**⚑ LAW 3 — check 11, `moved: {}`, over NINE constants:** `PLAYER_ADCTH_PCT` 21.0 ·
`PLAYER_HP_MAX` 20,005.0 · `PLAYER_REGEN_HP_PER_S` 129.38 · `player_damage_per_tick` 51,726.0 ·
`disc_radius_m` 3.0 · `max_ticks` 4000 · `GLOBAL_PET_LIMIT` 12 · **`D_ENGAGE_M` 2.4** ·
**`EOR_RADIUS_M` 3.0** — the last two added this lap because this is the first iteration that could
have moved either toward a T-band. **There is no fitted number anywhere in this lap.**

---

## 16 — COVERAGE, counted from the emission (#70)

| | |
|---|---:|
| Lap-F table rows | **299** (297 board + 2 player) |
| board records, grade census | **297 / 297 MEASURED** (169 ROSTER-169 + 128 SUMMON-128) |
| records rolled or summoned by any cell, **absent from the table** | **0** |
| ghosts (`FORCE-NO-COLLISION`) | **14** |
| MEASURED zero-radius bodies | **17** (13 of them independently flagged as ghosts) |
| player radius | **0.3199999928474426** (MEASURED, unrounded — R-PM4-9's 0.32 at float32, delta −7.2e-9 m, asserted) |
| `entity_radius_m` non-NULL on the reference baton | **340 / 340 actors · 1,655 / 1,655 pets** |
| I-2 batons, same field | **0 / 188 actors · 0 / 620 pets** — the conductor's L-4 `None`s |

---

## 17 — SEAM WORK

**star-lord** — one additive nullable field (`PetActor.entity_radius_m`), one adapter row that had
claimed a permanent NULL, two `KC2RunSpec` fields, three specs. **No schema version, no enum
member, no validator predicate, no gate-wall pin moved. 20/20 batons re-gate green.** Two calls
filed, neither taken: (a) should `G-PETS` gain a boundary check on `entity_radius_m`; (b)
**`Actor.entity_radius_m` has had NO boundary validation since `R-17` because it was always NULL —
it is not NULL any more, and that is new coverage the gate wall does not have.**
⚑ **And a thank-you that is also a measurement: `R-LOCO-1` caught D-I3-3 before a byte was
written** (§ 1). The gate's halt text — *"nothing here is repaired by widening a tolerance"* — was
correct and was obeyed.

**drax / scene consumers** — ⚑ **the picture changes materially.** I-2 put **20–54 bodies inside a
3.0 m circle with 56 % of pairs interpenetrating and 16 % exactly coincident**; a cell of record now
puts **at most 23**, **zero coincident**, and every body at its MEASURED radius, with
`entity_radius_m` populated on **both** `actors[]` and `waves[].pets[]` so a renderer no longer has
to guess. **Read C-I3-1 before drawing an approach:** under the shipped contact response the crowd
forms a **queue**, not a ring — 63 % of CAMP's kill rows land on bodies sitting exactly at
`d_engage`.

**rocket** — nothing. **jack-ryan** — Disciplines #1, #2, #3, #11, #12 exercised and named.

---

## 18 — PINS

**At launch:** engine HEAD `8061d40a` · 17 frozen batons + I-2 findings verified from bytes ·
4 substrate CSVs digest-verified at FULL hash.
**At landing:** HEAD after `33b11c8e` (fold) → `284f95d0` (D-I3-3 repair) → artifact commit,
**PUSHED**. Every commit by **explicit path**; **no `git add -A` anywhere in this lap.**

---

## 19 — ⚑ SELF-ATTACK SURFACES

1. **⚑ MY PRE-REGISTERED CONTACT RESPONSE IS THE WRONG ONE AND § 9 SAYS SO WITH NUMBERS.** The
   matrix of record is graded on the model I registered, and it misses three bands. The diagnostic
   that changes **only** the contact response — not one radius, not one constant — meets T1 and T2.
   **I will not present the block-and-dwell result as "what the measured geometry does to the
   fight", because § 9 measures that it is mostly what my own unmeasured choice does to it.**
2. **The separating diagnostic leaves a 10.09 % overlap residue.** Jacobi push-apart at 4 passes
   converges toward the invariant; it does not enforce it. **So neither response is strictly
   better: one enforces the ruling and breaks the fight, the other reproduces the fight and only
   approximately enforces the ruling.** That is the fork, stated without a thumb on it.
3. **T2's "MET" in the void first matrix was a coincidence I nearly published.** 213.88 s against a
   213.9 s ceiling, produced by frozen bodies. **§ 1 exists so nobody reads it anywhere else.**
4. **P.5 is the prediction I should have got.** I wrote four paragraphs (§ D.3) arguing that no
   channel ran toward "faster" and never noticed that the same argument, applied to the monsters'
   side, says the player takes less damage. **I checked the sign of one term and called it the sign
   of the model.**
5. **T4b has failed three times and its failing clause has now changed twice.** It is still
   unreachable from the board side, exactly as I-1 § 6, I-2 § 6 and Lap F § 10.5 all said.
6. **Wave 154's 38.12 s travel outlier survives a fourth lap undiagnosed** — and it is now the ONE
   wave whose duration is *identical* across I-1, I-2 and I-3 (38.12 s in every cell of all three),
   which is itself a measurement nobody has followed up.

---

## 20 — WHAT I WOULD PUT TO THE CONDUCTOR (a ruling, not a queue item)

**The largest remaining measured divergence is no longer a substrate gap. It is an unruled model
choice.** Three iterations of measured-decode substrate completion have now given the roster its
life, the summons their life, and every body its space — and the run's own instrument says the
next term is **how two bodies in contact resolve**, which Lap F proved is **not decodable from the
corpus** (C-F2 dead-ended on a hostility relation with no table anywhere).

That makes it a **ruling**, and it is exactly the shape R-PM4-8 already took: *the geometric bound
is the sim's own abstraction*. § 9 puts both realisations on the table with numbers.

**Everything else prices out below it:** C-E3 still parked · the HI limb is a ×1.20 median move
against a term that just moved the death wave by nine · and **T4b remains reachable only from
Lap G's limb** (kit / dash / potions), unchanged and unanticipated by this lap.

**No HALT was hit. Nothing required inventing an unmeasured quantity. There is no fitted constant
anywhere in this lap, and nothing was aimed at a band — I predicted 224 s and the matrix of record
returned 326.78 s on the like-for-like basis.**
