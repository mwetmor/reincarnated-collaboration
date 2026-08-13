# KC2-PM4 · I-5 — landing note: **the batons come back, and the invariant turns out to be a wish.**

> **Run:** KC2-PM4 · **Iteration:** I-5, TICK ORDER · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-13
> **Fired under:** ruling **R-PM4-13** (charter ledger **L-12**) — *"the `step → separate →
> resolve` restructure is AUTHORIZED as ITERATION 5 … a reasoning-boundary structural fix: it makes
> the model tell the truth about where bodies ARE within a tick; it must move NO outcome toward a
> target."*
> **Math note (Discipline #1, written BEFORE the code — commit `5bce39b2`, its own commit, so the
> git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i5-tick-order-2026-08-13.md`
> **Status:** COMPLETE. **No HALT.** Assert wall **16/16 PASS**, determinism ×2 **EXACT (0
> differences)** on all three cells, **three batons FULL at 67/67**, Law-3 witness ELEVEN and
> `moved: {}`. **One ruling request at § 12, not a HALT.**

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> Unless a different source is named inline, every I-5 quantity is read by key path from
> `reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i5-findings-20260813_143608.json`
> · sha256 **`f2b8b650ece1f35280fdb1aa9f605cf31a1b817200d3bf37e950a269210287d0`**, and every I-4
> quantity from `…/kc2-pm4-i4-findings-20260813_131435.json` · sha256
> **`5e3e38b7f980f98e18deb42d22b9722e4d5cd5af4c28850211bd9ad343b8ed18`** (verified from bytes at
> run time by the driver — a wrong digest HALTs the lap). The key path is given with each table.
> **This is the discipline the conductor banked a defect against at L-12** — I-4's prose carried
> "3,237 player damage rows" that no artifact reproduces. There is no unsourced number below.

---

## 0 — The one-paragraph answer

**The tick order was the defect, the fix took two limbs rather than one, and turning baton emission
back on immediately found a second defect that had been in the wire since I-4.** Under
`separate_then_resolve` the sim's emitted path and its emitted event rows are **one trajectory**:
an independent re-implementation of star-lord's own `G-LOCO-ONE-TRAJECTORY` predicate, at the gate's
own DERIVED tolerance, reports **0 rows outside of 4,736 checked** — against **8 outside of 4,564,
worst error 2.392 m**, on the identical fold under the legacy order. `Mover._n_intratick_merges`,
the counter D-I4-2 added for *"two positions on one tick"*, reads **0**: the amendment is dead code
now, which is the sharpest available test that the model tells the truth. **Three batons emitted,
67/67 green, calibration grade FULL** — the first since I-3. And the new instrument this iteration
was obliged to build falsified my own prediction and produced the run's next finding: **R-PM4-8's
non-overlap invariant is approximated, not enforced.** At the instant the weapon resolves, the board
carries **6.184 overlapping body-pairs per tick**, down from **8.997** immediately before the solve
— the 4-pass Jacobi removes **31.3 %** of what it is handed and does not converge. The player still
does not die: all three cells reach `ehp_band_exhausted` at wave **171**, exactly as the commission
expected.

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 12 predictions, 4-layer baseline protocol, 16-check wall) | `simulation/math/kc2-pm4-i5-tick-order-2026-08-13.md` | **`5bce39b2`** |
| 2 | `kc2/run.py` — `tick_order`, the motion-phase closure, `_mark_arrivals`, `_observation_census` | modified | `35c115ba` |
| 3 | `kc2/locomotion.py` — `Mover.displace()`, `_pre_xy` capture, displacement telemetry | modified | `35c115ba` |
| 4 | `export/kc2_run_adapter.py` — `tick_order` spec field + 3 I-5 specs | modified | `35c115ba`, `af411852` |
| 5 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `35c115ba` |
| 6 | **driver + assert wall (16) + determinism + 4 diagnostics + the one-trajectory audit** | `simulation/scripts/gamora_kc2_pm4_i5_tick_order_2026_08_13.py` | `35c115ba`, `af411852` |
| 7 | **D-I5-2 fix** — sequential heal application | `kc2/run.py` | `af411852` |
| 8 | **3 knot supplies + findings** (stamp `20260813_143608`) | `simulation/output/` | `af411852` |
| 9 | **⚑ 3 BATONS, FULL, 67/67** | `src/reincarnated/output/` | `8db4f379` |
| 10 | AGENT_STATE — SESSION 122 | `simulation/AGENT_STATE.md` | `e26f12b0` |

**Engine `36809fd3 → e26f12b0`, six commits, PUSHED.**

### Artifacts of record (basis: findings `knot_artifacts` + the emit driver's stdout)

| what | sha256 |
|---|---|
| **findings** | `f2b8b650ece1f35280fdb1aa9f605cf31a1b817200d3bf37e950a269210287d0` |
| knots CAMP/DEF-OFF | `c30d9b34e839462b4f7277ffc952bd4f0abcc616c678d6e73f1a3057ab5eaa2f` |
| knots CLUSTER/DEF-OFF | `5f60189a424020e2b7925adeabafbf699b821b191359008ab8f887f6819ce5a8` |
| **knots CLUSTER/DEF-ON** ← reference | `0b6dd036a975e96863d0b87012473742e713fdbfbc80191a19fb80c53c530e80` |
| **baton** CAMP/DEF-OFF | `6b01a18744f8b7f0cbc087dcf1d678dc1097739097b8fcb6171fc2086b237022` |
| **baton** CLUSTER/DEF-OFF | `392e09e3dc750e3d3a4b7bb7a3891ee6ac797dd7c4cb054fffb0eabb0aff5090` |
| **baton** CLUSTER/DEF-ON ← reference | `4afd8319d6f828cc29903eb4ea360dc05d246b5d3d2560961c9d3586bf35c131` |

---

## 2 — ⚑ THE DELTA IS ONE ARGUMENT, AND THE BASELINE PROTOCOL PROVES IT RATHER THAN CLAIMING IT

R-PM4-13 anticipated that the restructure "invalidates check 1's baseline by construction." **Under
a *versioned* order it does not have to** — the legacy order stays the default, so the predecessor
remains reproducible at HEAD and the mandate's byte-exactness requirement becomes a running
assertion instead of a hope. Four layers, run FIRST, HALTing on mismatch (basis:
`baseline_protocol` on the findings; the driver prints each line):

| check | configuration | requirement | result |
|---|---|---|---|
| **1a** | fold-OFF, `separate`, **legacy** | byte-EXACT vs the pre-I-4 clean worktree at `7b5c31b9` | **3/3 EXACT** |
| **1b** | fold-OFF, `block`, **legacy** (D-I4-2's own check 15) | byte-EXACT vs the same worktree | **2/2 EXACT** |
| **1c** | **FULL I-4 fold**, **legacy** | byte-EXACT vs the predecessor | **3/3 EXACT — against a RE-MEASURED pre-I-5 worktree; see § 5** |
| **1d** | fold-OFF, `block`, **NEW** order | ⚑ DIVERGENT BY CONSTRUCTION | declared in the math note § F **before it ran**; newly pinned |

**1d's divergence was named in advance, not discovered.** Under `block` there is no separation at
all, so S-1's mechanism is absent; the divergence is entirely **S-2** (arrivals evaluated in the
observation phase, against a player who has already moved) and **S-3** (pet TTL leaving before the
disc). New pins: camp/def-off `17e2d30756f455f6…`, cluster/def-on `6ba8ea6f350110c4…`.

### 2.1 — the one rider I designed OUT, and why it is a Law-3 matter

Moving the **whole** pet phase above the disc would have been the tidier code change. It would also
have handed the player one extra tick of disc exposure per summon — **1,224 placements** on the
reference ladder (`cells.cluster_defon.geometry.placements`) — and that rider shortens duration
**toward** T2's band. Instead the pet **step** moved up (it is motion; separation must follow all
motion) and the pet **spawn** stayed below the disc, which leaves the exposure schedule
arithmetically identical: the disc sees a pet after *n* steps at tick *k+n* under **both** orders.
Math note § C.1 carries the two-column proof. **A rider that moves an outcome toward a target is
designed out, not declared.**

---

## 3 — ⚑ THE CONTRACT: WHAT THE ITERATION EXISTED TO DO

Basis: `cells.<cell>.one_trajectory` and `cells.<cell>.displacement`;
`diagnostics.legacy_order_FULL_FOLD_with_census.one_trajectory` for the comparator.

| instrument | legacy order, identical fold | **I-5** | I-4's published residual |
|---|---:|---:|---:|
| `G-LOCO-ONE-TRAJECTORY` rows checked | 4,564 | **4,736** | — |
| **rows OUTSIDE the derived tolerance** | **8** | **0** | 61 (after attempt 2) / 76 (before) |
| worst absolute error | **2.3923 m** | **4.44 × 10⁻¹⁶ m** | "up to 0.09 m" |
| `Mover._n_intratick_merges` | > 0 | **0** | > 0 |
| `extract_paths` structural violations | 0 | **0** | 0 |
| one-vertex-per-tick, re-derived from the emitted rows | — | **PASS** | — |
| **batons** | — | **3 × FULL, 67/67 green** | **NONE (D-I4-5)** |

The audit is an **independent re-implementation** of `baton_v1_validator._g_loco_one_trajectory`,
not an import of it — importing star-lord's helper would make the audit agree with the gate by
construction, and the point is that two implementations reach the same verdict. Its tolerance is
DERIVED the same way the gate derives it (`2 × 10^-position_dp + 1e-9`, `position_dp = 3` →
`0.002000001 m`), and it **refuses a vacuous pass**: zero rows examined reports FAIL.

⚑ **The 2.392 m worst error on the legacy arm is worth pausing on.** D-I4-5 reported the residual as
"up to 0.09 m", which is the *displacement* scale. The *interpolation* error is thirty times larger,
because between two knots a body whose per-tick displacement changes every tick is not on the line
the polyline draws. That is the knot-density limb, and it is why the order fix alone would not have
cleared the gate.

### 3.1 — the second limb, and the reason it is owed rather than optional

I-4 had already falsified "fix the order and pick a vertex": pinning the tick's vertex to the
hit-test position moved `damage-row-outside` **76 → 61** and stopped. The residual is knot
**density**, exactly as the gate's own docstring predicts — *"more knots are owed. Do not widen the
tolerance to make it pass."*

**Nothing was widened.** `Mover.displace()` records the two exact endpoints of the segment a
separation displacement bends: `sep_from` at tick − 1 and `separate` at tick. Math note § E.2 proves
the vertex set makes interpolation exact at every tick rather than asserting it.

Cost, measured (basis: `cells.cluster_defon.knot_statistics`): total knots **25,538 → 27,266**,
a factor of **1.068** — against 13,252 displaced roster body-ticks each nominally owing two
vertices. Almost all of them collapse into vertices the bend recorder was already emitting
(`bend` 24,128 → 24,051). **My prediction of a 1.5×–4.0× growth is falsified and the reason is that
I priced the vertices and never priced the dedup.**

---

## 4 — ⚑ D-I5-1: **R-PM4-8's NON-OVERLAP INVARIANT IS APPROXIMATED, NOT ENFORCED**

This is the finding, and it came out of the instrument the iteration was obliged to build to
justify its own central claim. Basis: `cells.cluster_defon.census` and
`diagnostics.legacy_order_FULL_FOLD_with_census.census`, over 6,097 censused ticks.

| quantity | before the solve | **after the solve = what the weapon observes** |
|---|---:|---:|
| overlapping body-pairs **per tick** | **8.997** | **6.184** |
| worst penetration | **1.4824 m** | **0.9470 m** |
| pairs in which the **PLAYER's own body** overlaps a monster (whole ladder) | **1,161** | **605** |
| **solver reduction** | | **31.3 %** |

**The 4-pass Jacobi solve does not converge on this board.** The configuration the disc resolves
against is *repaired-by-one-solve*, not *non-overlapping*. A consumer — or a future iteration —
reading "living bodies are non-overlapping discs" as a guarantee will be wrong by about six pairs a
tick.

**⚑ The pass count was NOT raised.** Driving that number to zero by choosing a constant is exactly
the fitting the charter bars, and the number is upstream of the outcome bands (C-I5-1). The residual
is reported and the ruling request is at § 12.

**What the ordering change bought on its own, and it is the I-2/I-3 concern answered:**
player-inside-a-monster pairs at weapon-resolution time fall **1,145 → 605, a 47 % cut**
(legacy-order comparator vs I-5 reference, same fold, same instrument, same ladder). I-3 measured
that *"20.29 % of I-2's kill work came from bodies the player was standing inside"*; ordering alone
halves the instants on which that can happen.

---

## 5 — ⚑ D-I5-2: THE DEFECT THAT ONLY EXISTED BECAUSE THE BATONS WERE OFF

The **first** emit attempt on the I-5 specs went red, and not on a gate I was watching:

> `AC-11.7e — events.rows[3356] (heal_tick, target=player): hp_after 14643.71 does not reconcile
> against previous 8808.44 + 5801.25 = 14609.69 (tol 0.010000001)`

`run.py`'s counterplay block applied the **sum** of every heal component in one `min()` clamp and
then emitted two or more rows all carrying the post-**total** `hp_after`. The missing **34.022** is
the potion's over-time drip landing on the same tick as its instant.

⚑ **The defect is I-4's, and it was invisible because I-4 emitted no batons.** D-I4-5 stopped the
artifact; the artifact is what would have found this. That is the argument for turning emission back
on, stated as a fact rather than as a hope — and it is the second time in two laps that a star-lord
gate has found a simulation-seam defect.

**Fixed at the source** by sequential application — each component applied and *then* emitted, so
every row's `hp_after` is the HP after *that* row. No tolerance widened, no row dropped. **The HP
trajectory is provably identical**: `min` is monotone over non-negative components, so
`min(c, min(c, h+a)+b) == min(c, h+a+b)`.

**⚑ It moves check 1c's pin, and I measured the move rather than asserting it was small.** A
`git worktree` at pre-I-5 HEAD `36809fd3` was replayed against HEAD under the identical
legacy-order full-fold configuration and `deep_diff` enumerated the **entire** divergence:

| cell | differences | rows |
|---|---:|---|
| camp/def-off | **2** | `.events[4287][11]`, `.events[22593][11]` |
| cluster/def-off | **1** | `.events[23677][11]` |
| cluster/def-on | **1** | `.events[3648][11]` |

Column 11 is `hp_after`; every delta is exactly **34.022108843538** =
`(20005 × 25/100) / 12.0 × 0.0816327`, the potion's HoT for one tick. **Nothing else in a 20-wave
emitted surface moved** — no position, no damage magnitude, no death, no duration, no wave boundary.
Check 1c now pins the measured post-fix digests and carries I-4's published ones alongside as
`1c_reference_PRE_D_I5_2`, so the record shows both.

---

## 6 — ⚑ THE MATCH GATES (INTERMEDIATE observables, judged SEPARATELY from T1–T4)

Basis: `match_gates` on the findings (reference cell); I-4 column from `match_gates` on the I-4
findings. The **⚑ NOTE-9 basis caveat carried unchanged from I-4**: `ground px → m` is a DECLARED
GAP (OBS-H2-9); the video's 150-ground-px ring and the sim's radii are **not equated numerically
anywhere**. The correspondence is SEMANTIC (video "sprites abut the player" ↔ the DB's own
`meleeTargetDistance` = `D_ENGAGE_M`). **No pixel scale is invented in this iteration either.**

| gate | I-4 | **I-5** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring density median (d_engage) | 0 | **0** | 1 | MISSED |
| **MG-2** ring density p90 | 4 | **4** | 3 | MISSED |
| **MG-3** ring density **max** | 19 | **19** | **10** (R150) · 12 (R180) | MISSED, ratio 1.9× |
| MG-3 ring density **mean** | 1.1438 | **1.1819** | — | ⚑ **rose** — see § 7 |
| **MG-4** moving fraction | 0.8420 | **0.8366** | **0.883** | MISSED (sim under) |
| **MG-6** longest stationary | 1.3878 s | **1.3878 s** | ≤ 1.40 s | **MET** |
| **MG-7** dash rate | 5.353 s | **5.3517 s** (93 dashes) | 5.3235 s | **MET** |

---

## 7 — ⚑ THE T-BAND SCORECARD, AND THE MECHANISM I GOT BACKWARDS

> **⚑ TERMINAL REASON: `ehp_band_exhausted` AT WAVE 171 ON ALL THREE CELLS. THE PLAYER DID NOT DIE.**
> Exactly as the commission expected. legolas's **Lap I** is decoding the band extension in
> parallel; **its output was NOT consumed by this iteration.**

Basis: `target_state_scorecard`, `like_for_like_151_160_s`, `cells.<cell>.summary`.

| band | I-4 | **I-5** | verdict |
|---|---|---|---|
| **T1** survival depth (160) | no death by 170 | no death by 170 | **MISSED — and still UNMEASURABLE** |
| **T2** 186 s ±15 % | 508.57 s / 20 waves | **497.71 s / 20 waves** | **MISSED**, `like_for_like: false` |
| T2 on the **like-for-like** 151–160 basis | 227.755 s (+22.4 %) | **233.551 s (+25.6 %)** | outside the band |
| **T3** pacing shape | median ratio 1.189, r +0.020 | **1.165, r +0.142** | **NEAR** |
| **T4a** sustain | 99.19 % | **99.38 %** | **MET** |
| **T4b** terminal mechanism | — | 15.59 s, 503 player rows, DoT 0.26 % | **MISSED — there is still no terminal** |

Cells (basis `cells.<cell>.terminal` + `.summary.t_s`): camp/def-off band@171 1,939.67 s ·
cluster/def-off band@171 521.55 s · **cluster/def-on band@171 497.71 s**.

### 7.1 — ⚑ I predicted the disc would see FEWER bodies. It sees MORE, and the mechanism is nameable.

My mechanism (math note § G.2) was: the repair pushes bodies apart, the player's body is `fixed`,
therefore near the player the repair is net **outward**, therefore disc occupancy falls and waves
lengthen. **The band was right and the mechanism was wrong.** Basis:
`cells.cluster_defon.disc_occupancy`:

| quantity | I-4 | **I-5** |
|---|---:|---:|
| contact-tick fraction | 0.3923 | **0.4207** |
| body hit rows | 10,282 | **10,574** |
| n_eff median over contact ticks | 2 | **3** |
| ring density mean (d_engage) | 1.1438 | **1.1819** |

**Why.** Jacobi splits a pair's penetration symmetrically along the line joining the two bodies. In
a crowd arranged radially around a fixed player, the **inner** member of an overlapping radial pair
is pushed *inward* — toward the player — by its outer neighbour, and the player's own body only
corrects that on a later pass, of which there are four and they do not converge (§ 4). So the
repaired configuration is, on net, **tighter** at the ring than the unrepaired one, not looser. The
disc sees more bodies, the player kills faster over the whole ladder (497.71 s vs 508.57), and waves
151–160 nevertheless get *longer* because the wave-by-wave redistribution is not uniform (wave 161
alone falls 15.7 s while wave 160 rises 6.0 s — basis `cells.cluster_defon.per_wave_s` against the
I-4 artifact's).

---

## 8 — PRE-REGISTERED PREDICTIONS vs OUTCOME — **eight confirmed, one split, three falsified**

The falsified ones keep their original wording (the run's standing practice).

| # | prediction | outcome |
|---|---|---|
| **P.1** | `_n_intratick_merges` = 0 on all three cells | **CONFIRMED. 0/0/0.** D-I4-2's amendment is dead code |
| **P.2** | one-trajectory audit: 0 rows outside, non-vacuously | **CONFIRMED. 0 of 4,736**, worst error 4.4e-16 m; legacy arm 8 of 4,564 at 2.392 m |
| **P.3** | three batons FULL, 67/67, no tolerance widened | **CONFIRMED.** VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33 ×3 |
| **P.4** | checks 1a (3/3), 1b (2/2), 1c (3/3) byte-EXACT | **SPLIT.** 1a and 1b EXACT as written. **1c EXACT only against a re-measured pre-I-5 worktree** — D-I5-2 moved I-4's published digest by 2/1/1 `hp_after` rows. I did not see that coming and it is enumerated in § 5 rather than smoothed |
| **P.5** | determinism ×2, 0 differences, all cells | **CONFIRMED** |
| **P.6** | like-for-like 151–160 in **228–260 s**, point estimate 238 | **CONFIRMED on the band (233.551 s) — ⚑ AND THE MECHANISM I GAVE FOR IT IS FALSIFIED.** § 7.1 |
| **P.7** | MG-3 ring max **falls** into 15–19 | **FALSIFIED on the clause that matters.** It stayed at 19 and the ring **mean rose** 1.1438 → 1.1819 |
| **P.8** | MG-1 median stays 0; MG-2 p90 3 or 4 | **CONFIRMED** (0 and 4) |
| **P.9** | T4a MET ≥ 97 %; terminal still `ehp_band_exhausted` @171 | **CONFIRMED** (99.38 %, band @171) |
| **P.10** | MG-4 moving fraction moves by ≤ 0.010 | **CONFIRMED.** 0.8420 → 0.8366, Δ = 0.0054 |
| **P.11** | knots grow ×1.5–4.0 | **FALSIFIED. ×1.068** (25,538 → 27,266). I priced the vertices and never priced the dedup |
| **P.12** | observation-time overlap falls > 90 % | **⚑ FALSIFIED, AND THE FALSIFICATION IS THE FINDING.** 31.3 % per solve; the invariant is approximated, not enforced (D-I5-1, § 4) |

**The unifying error, and it is a new shape.** I-1: priced sustain, not exposure. I-2: priced eHP,
not co-residence. I-3: priced throughput, not the monsters' reach. I-4: priced the size of the
counterplay, not its shape. **Here I priced the REPAIR and never priced its CONVERGENCE.** Every one
of P.7 and P.12 is wrong because I reasoned about push-apart as though it *achieved* the invariant
in one application and as though its net effect near a fixed body were outward. Measured, it does
neither: it removes 31 % of the overlaps it is handed, and in a radial crowd it moves the inner
body of a pair toward the player. **The fix I shipped is still exactly what R-PM4-13 authorised —
the weapon now resolves against the board the model believes in — but the board the model believes
in is not the board R-PM4-8 describes.**

---

## 9 — DECLARED ASSUMPTIONS + CLIFFS

**New this lap:** **C-I5-1** the Jacobi solver's 4 passes are carried UNCHANGED; the non-convergence
residual is a REPORTED NUMBER, not a target (§ 4) · **C-I5-2** the two new knot kinds
(`separate`, `sep_from`) are additive; the baton's `PathWaypoint` carries no kind field, so no
schema enum is touched · **C-I5-3** the legacy order stays supported and reachable — twenty frozen
batons were produced under it and deleting it would make them unreproducible · **C-I5-4** the
player's body remains `fixed` in the solve, unchanged from the arm R-PM4-12 ruled on ·
**S-1/S-2/S-3** the three semantic shifts, on the wire under `waves[].tick_order`.

**Carried unchanged:** C-I4-1 … C-I4-7 · C-I3-5 · C-I2-1 · C-E3 · C-D2 / C-D3 / R-PM4-6 ·
C-F1 / C-F3 / C-F4 / C-F5 · C-G3 · C-G6 · **OBS-H2-9 (ground px → m)** · wave 154's travel outlier,
undiagnosed for a **sixth** lap.

**⚑ LAW 3 — check 11, `moved: {}`, over ELEVEN constants.** No constant is added, removed or moved
anywhere in this iteration. No CSV is added. No fold is folded. The only argument that changed is
`tick_order`, and § 2 proves it.

---

## 10 — SEAM WORK

**star-lord** — ⚑ **a fourth gate catch across two laps, and it was right again.** `AC-11.7e` found
D-I5-2 within seconds of emission being re-enabled. **No schema change is requested and none is
needed** — no baton field, no enum member, no validator predicate, no gate-wall pin, no tolerance.
Two additive wave-dict keys (`waves[].tick_order`, `waves[].observation_census`), both keyed only
when active, neither inside `waves[].body_geometry`; one additive spec field (`tick_order`). Both
MIGRATION files carry the detail. **One thing to carry forward: D-I5-1 is a caveat on a ruling, not
on a field — a consumer must not read R-PM4-8 as a guarantee.**

**drax / scene consumers** — the crowd shape is unchanged from I-4 (a ring that spreads laterally),
but two things a renderer will care about are now true: **the emitted path and the emitted damage
rows are one trajectory** — a body drawn from the path is where the damage happened, to within
4.4e-16 m — and **bodies overlap**, by ~6 pairs per tick with worst penetration 0.947 m. A renderer
that assumes discs never interpenetrate will pop.

**rocket** — nothing. **jack-ryan** — Disciplines #1, #2, #3, #11, #12 exercised and named;
**#12 is the whole iteration**.

---

## 11 — ⚑ SELF-ATTACK SURFACES

1. **The biggest number in this note is a number I did not predict and cannot yet act on.** D-I5-1
   says the invariant three iterations have been built on is approximate. I measured it, refused to
   tune it, and routed it — but I-3's and I-4's landing notes both read as though the invariant
   held, and neither of them had this instrument. **The instrument should have existed at I-3.**
2. **1c is the check I most wanted to be byte-exact and it is the one that moved.** It moved for a
   good reason and I enumerated the move exactly, but "EXACT against a worktree I built this
   afternoon" is a weaker sentence than "EXACT against the published predecessor", and the record
   should say so plainly.
3. **The `i5_no_player_fold_baseline` diagnostic dies on wave 160 at 188.00 s** against a measured
   186 s — a 1.08 % miss on T2 and an exact hit on T1. **That is not a result and I am not
   reporting it as one.** It is R-PM4-12's arm with the player's hands cut off, and Lap G proved
   Matt had his hands. I flag it because it is the kind of number that gets quoted out of context,
   and because it is the arm the run's own reference cell would have to become to reach the bands
   — which would mean deleting a measured limb.
4. **The ring density did not move toward its match target and the moving fraction moved further
   from its own.** Two of seven match gates still MET, same as I-4.
5. **My mechanism reasoning was backwards on the term the iteration is named after** (§ 7.1). I got
   the band right by luck of magnitude, not by understanding.

---

## 12 — ⚑ WHAT I PUT TO THE CONDUCTOR — **one ruling request, no HALT**

**D-I5-1 — is R-PM4-8's non-overlap invariant a HARD constraint or a SOFT one?**

The ruling reads as hard: *"living bodies are non-overlapping discs (centre distance ≥ rᵢ + rⱼ)."*
The implementation is soft: 6.184 overlapping pairs per tick at weapon-resolution time, worst
penetration 0.947 m, 31.3 % removed per solve. Three options, and **I have deliberately not chosen
between them, because two of the three are constant-choices whose effect lands upstream of the
outcome bands:**

- **A — the invariant is SOFT and stays soft.** Ruled as an approximation, reported on the wire
  (it now is), and the residual carried as a declared property of the model. **Zero new numbers,
  zero Law-3 exposure.** My lean, on the argument that the real game's response is a declared gap
  (C-F2/C-F6) and a solver that half-repairs is no less faithful than one that fully repairs.
- **B — raise the pass count until it converges.** Cheap to run, and it is **exactly the shape the
  charter reserves**: a constant chosen for its effect on an observable that sits upstream of
  duration and death. If the conductor wants it, it should be ruled and the pass count pre-registered
  before it is measured, not chosen after.
- **C — a different solver** (Gauss–Seidel with the player resolved last, or projection to hard
  non-penetration). A model change, not a constant, and therefore an ITERATION.

**Nothing else is blocked.** Batons are flowing, the path contract holds, the matrix discriminates
(497.71 / 521.55 / 1,939.67 s), and the run's largest measured divergence is unchanged from L-12:
**sim mean HP 99.38 % against the video-measured 0.932 with seven excursions below 0.70 and a
6.55 s terminal collapse.** That is the monster-offense limb, and it is legolas's Lap I.

**No constant was tuned. Nothing was aimed at a band. I predicted the disc would see fewer bodies
and it sees more; I predicted the repair would clear the board and it clears a third of it.**
