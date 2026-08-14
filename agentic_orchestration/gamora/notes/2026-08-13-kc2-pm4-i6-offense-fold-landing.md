# KC2-PM4 · I-6 — landing note: **the circuit-breakers fire, and the shape is wrong in a new way.**

> **Run:** KC2-PM4 · **Iteration:** I-6, THE OFFENSE FOLD · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-13
> **Fired under:** ruling **R-PM4-16** (charter ledger **L-13**). **R-PM4-15 also binding** —
> D-I5-1 stays SOFT; the Jacobi solver and its pass count are **UNTOUCHED**.
> **Math note (Discipline #1, written and committed BEFORE the code — commit `c6a15934`, its own
> commit, so the git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i6-offense-fold-2026-08-13.md`
> **Status:** COMPLETE. **No HALT.** Assert wall **18/18 PASS**, determinism ×2 **EXACT (0
> differences)** on all three cells, **three batons FULL at 67/67**, Law-3 witness ELEVEN and
> `moved: {}`. **Two cliffs and one ruling request at § 12, not a HALT.**

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> Unless a different source is named inline, every I-6 quantity is read by key path from
> `reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i6-findings-20260813_231731.json`
> · sha256 **`2acf01299a565271ee26eb4a200448bf4609983a631f3b4e45637983c10ed2d6`**, and every I-5
> quantity from `…/kc2-pm4-i5-findings-20260813_143608.json` · sha256
> **`f2b8b650ece1f35280fdb1aa9f605cf31a1b817200d3bf37e950a269210287d0`** (verified from bytes at
> run time by the driver — a wrong digest HALTs the lap). **There is no unsourced number below**
> (the L-12 defect, still being paid down).

---

## 0 — The one-paragraph answer

**The monsters' weapons were at vendor strength for six iterations, and giving them the Crucible's
own modifier woke the player's counterplay stack up for the first time in the run.** `M_inst` ×1.830
and `M_dot` ×0.090 at wave 160, read per `(family, wave)` from Lap I with zero free parameters,
raise gross intake **×1.417** and take mean HP **0.9938 → 0.9863**. **Turtle Shell fires 2 (was 0),
Menhir's Will fires 1 (was 0), the potion fires 2 (was 1)** — I-4's and I-5's headline "HP never
reached 50 %" is retired. But **the shape is wrong in a NEW way**: the sim now has **twelve
excursions below 0.70 against the video's seven**, while its **mean HP is still 5.4 points too
high**. The run's largest divergence has changed character from *magnitude* to *variance*. Two
measurements taken **before** specifying changed the fold itself: Lap I's DoT population is a
**strict subset** of the one the sim already simulates (folding its magnitudes would double-count),
and **the band-C wall is arena geometry, not eHP** — wave 170 is the last wave with measured spawn
geometry on any Crucible arena in the corpus. **The player still does not die.**

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 14 predictions, 18-check wall) | `simulation/math/kc2-pm4-i6-offense-fold-2026-08-13.md` | **`c6a15934`** |
| 2 | **`kc2/offense.py`** — the modifier laws, the family map, the stacking policy, the DoT-rider instrument | new | `b7fdc9b5` |
| 3 | `kc2/monster_stats.py` — band C (171–180) + the nine named gaps | modified | `b7fdc9b5` |
| 4 | `kc2/threat.py` — `ThreatEngine.offense`, magnitude application, stack policy | modified | `b7fdc9b5` |
| 5 | `kc2/run.py` — `simulate_wave(offense_fold=…)` + the additive wave-dict key | modified | `b7fdc9b5` |
| 6 | `export/kc2_run_adapter.py` — `offense_fold` / `band_c_ehp` spec fields + 3 I-6 specs | modified | `b7fdc9b5` |
| 7 | **4 pinned CSVs** (Lap I) | `data/kc2/pm4i_*.csv` | `b7fdc9b5` |
| 8 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `b7fdc9b5` |
| 9 | **driver + 18-check wall + determinism + 3 sensitivity cells + the arena probe** | `simulation/scripts/gamora_kc2_pm4_i6_offense_fold_2026_08_13.py` | `b7fdc9b5` |
| 10 | **3 knot supplies + findings** (stamp `20260813_231731`) | `simulation/output/` | *(this landing)* |
| 11 | **⚑ 3 BATONS, FULL, 67/67** | `src/reincarnated/output/` | *(this landing)* |
| 12 | AGENT_STATE — SESSION 123 | `simulation/AGENT_STATE.md` | *(this landing)* |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6; L-13's own banked lesson)

| what | sha256 |
|---|---|
| **findings** | `2acf01299a565271ee26eb4a200448bf4609983a631f3b4e45637983c10ed2d6` |
| knots CAMP/DEF-OFF | `e463f6aebef0e5ad7777426b4c80b7e14b3860beb876ab6506b7e439f5f9d515` |
| knots CLUSTER/DEF-OFF | `8f4a465e145e68432932f586e4d314674fc29fa548c4189bf8f3a32fd3908c25` |
| **knots CLUSTER/DEF-ON** ← reference | `e05d282270153a8fcac8e74552ebfd38d3a46b1b786f3c2c7cefd48ac4ec1689` |
| **baton** CAMP/DEF-OFF | `caf5e72caf8748c09893c1f869b81f0603d44ca02599f6ea5521fc83ef8124ca` |
| **baton** CLUSTER/DEF-OFF | `9ef07b2c02459998b3ea467c1b08635dfe3baf8512c6e8e5d1f548835da1de38` |
| **baton** CLUSTER/DEF-ON ← reference | `c2ad90da9c52b8c5bb69acf3f8c299748be38d9d56cbbfb8371e26cc32f5db6b` |
| determinism surface CAMP/DEF-OFF | `e96c8101770a26735f5b46268b0ba8b28f176a5627b01698f4445b8262f82637` |
| determinism surface CLUSTER/DEF-OFF | `9bf4785b9951a06238ca681f3dfcf2b9092698dfdea07ebad13d4ebbec9dbeea` |
| determinism surface CLUSTER/DEF-ON | `0a0c140d988438094e74834b629091904b38112553b4f5aa02a0acab0dafb808` |

**New pinned substrate** (Lap I, FULL hashes, matching the conductor's own CL-10 verification):
`pm4i_wave_damage_modifier.csv` `f0852cec35a0362c101618b2a269446c4fba658ee0b80821aa5e4ae47eab910b` ·
`pm4i_dot_riders.csv` `2dc3e380a3800b3afd14f1923d1e2a32efe9263f4ee2eaec7c69c753ed7f6ce1` ·
`pm4i_band_c_ehp_by_wave.csv` `9f7fd070fa2a557d2a220656616e009bc06158240adfc37847d4d7b1240f153e` ·
`pm4i_band_c_roster.csv` `d442d41f260e3a2415c0fbe221a784ae5f8c63d10e1c73107ab63315674d0ecd`

---

## 2 — ⚑ THE SEMANTIC SHIFT, FRAMED AND NOT BURIED (Discipline #12)

**This is not a bug fix, and no value was wrong.** A whole **measured term was ABSENT**: every
monster damage magnitude this simulation has ever resolved was the **raw skill-record value at the
body's rank**, un-multiplied by the Crucible's own per-wave `offensiveTotalDamageModifier` or by the
Ultimate difficulty pak's `[8]` cell, **in either direction**, for six iterations. Lap D gave the
bodies their life back at I-1; their **weapons** were at vendor strength until now.

Three laws, zero free parameters, read per `(family, wave)` — never as a w160 constant, which is
R-PM4-1's shape applied to the damage limb for the same reason it was applied to the life limb:

| # | law | w151 | **w160** | w170 | w180 |
|---|---|---:|---:|---:|---:|
| **D1** | `M_inst(w) = 1 + sum_total_damage_modifier_pct(w)/100` | 1.820 | **1.830** | 1.850 | 2.150 |
| **D2** | `M_dot(fam,w) = 1 + (D_slow<fam> + U_slowAll)/100` | 0.110 | **0.090** | 0.070 | 0.070 |
| **D3** | band-C eHP, `G` | — | — | 344 | 510 |

Basis, carried verbatim onto the wire:
`balancingadjustment_survivalmode_enemies03.dbr@sm_mod [index wave-1]` +
`balancingadjustment_mp+difficulty_enemies01.dbr@base [index 8 = Ultimate/1-player]`. Grade, also
verbatim: `MEASURED (components); sum_* = DERIVED-SUM-ADDITIVE-BY-PARALLEL` — Lap I's cliff **C-I3**,
a *named* soft joint, with the components riding beside every sum so a consumer can recombine.

> ⚑ **The Crucible SUPPRESSES monster DoT, hard.** At wave 160 it pushes instant damage **UP by +83
> points** and pulls damage-over-time **DOWN by −91**. Anyone reasoning "the offense fold raises
> everything" is wrong about DoT by an order of magnitude: **DoT falls from 3.06 % of gross intake
> to 0.198 %.** Matt's banked testimony is *"some kind of poison/dot seemed to effect me in a major
> way on my last wave"* — and the measured substrate, folded honestly, makes DoT **smaller**. That
> tension is § 11.3 and I do not resolve it here.

---

## 3 — ⚑ THE MEASUREMENT THAT CHANGED THE RULING'S ITEM 2, TAKEN BEFORE ANY CODE

R-PM4-16 item 2 reads *"DoT riders per body — from `pm4i_dot_riders.csv`"*. Before writing that fold
I joined Lap I's DoT population against the DoT rows **the sim already carries** from PM-2's Lap B
decode, on `(record, skill_record, family)`, lower-cased and slash-normalised. Basis:
`⚑ dot_rider_join` on the findings, re-run at run time (assert-wall check 8), never transcribed.

| quantity | value |
|---|---:|
| Lap I `is_dot=True` rows | **198** |
| PM-2 `kind="dot"` keys the sim already resolves | **374** |
| **intersection** | **198** |
| **⚑ Lap I keys NOT already in the sim** | **0** |
| Lap I DoT records ⊆ PM-2 DoT records | **85 / 85** |

> ### ⚑ **LAP I'S DoT POPULATION IS A STRICT SUBSET OF THE ONE THE SIM ALREADY SIMULATES.**
> Folding `pm4i_dot_riders.csv` **as a damage source** would not add a rider. It would add a
> **second copy** of 198 riders the fight already resolves, and leave the other 176 unmodified — a
> double-count on part of the board and a no-op on the rest.

So the ruling's *content* — "the offense side gets the terms Lap I measured" — is delivered by **D2**:
the −91-point modifier applied to the riders that are already there. The CSV is consumed as what it
actually is for this seam: a **coverage, convention and materiality instrument**, digest-pinned and
cross-joined at run time. **This is § 12's first item, put to the conductor rather than decided
quietly.**

**And the ruling's column selection is already satisfied at HEAD.** Lap I § 5.1 brackets the DoT
magnitude convention; `threat._mk_damage_rows` reads `dot_dps_if_field_is_total` — the **lower**
reading — under **R-PM2-1**, and has since PM-2. Nothing moves. The HI limb runs as **S-CONV**
(§ 8). The 102/198 magnitude differences on the intersection are a **rank-basis** difference, not a
convention one (Lap I at the pool level set, rank 27; PM-2 at `level_used=109`, rank 28 —
`aetherialworm_b01_summon` Poison 201.0 vs 210.0, +4.5 %). Reported, not reconciled.

---

## 4 — ⚑ CLIFF C-I6-2: **THE BAND-C WALL IS ARENA GEOMETRY, NOT eHP**

R-PM4-16's premise is *"band-C extension 171–180 … so **T1 is measurable**"*. Before writing the
loader I checked whether the sim can **spawn** a wave-171 board. **It cannot**, and the reason was
already enumerated in the sim's own source (`locomotion.P01_TIER_COVERAGE_NOTE`). Re-measured at run
time from the cited geometry table (assert-wall check 16; basis `⚑ arena_wall_C_I6_2`):

| | |
|---|---:|
| maximum `p01_tier<NN>` on **any** of the sixteen cited Crucible arena geometries | **17** |
| content tier of wave 171 (`ceil(171/10)`) | **18** |
| band-C waves 171–180 whose pool rows use spawn point **1** (the tier-keyed emitter) | **10 of 10** |
| `sm1/survivalworld_a.map` (arena of record) at tier 18 | `KeyError: has no p01_tier18` |

> ### ⚑ **WAVE 170 IS THE LAST WAVE WITH MEASURED SPAWN GEOMETRY. THE BAND-C eHP FOLD DOES NOT, BY ITSELF, MAKE T1 MEASURABLE ABOVE 170.**
> Lap I decoded band-C **eHP, roster and composition**. It did **not** decode arena emitter
> placements for content tiers 18–20 — that surface is the Edition-I `Maps.arc` decode, a different
> instrument. What D3 changes is **which wall the ladder hits**: `ehp_band_exhausted` @171 becomes
> `arena_tier_exhausted` @171. **This was pre-registered as P.8 before the run and confirmed.**

**Nothing is invented to get past it.** Reusing tier 17's p01 placement for tier 18 would be an
extrapolation of measured geometry — and it would be a *small* one (the placement moves ~0.7 m
between tiers 16 and 17), which is exactly why GL-12 bars it regardless of size. Routed at § 12.

**The band is still folded, because it is measured**: 401/410 bodies MEASURED, 4,010 cells,
`G(171)=420` … `G(180)=510`, structural violations 0/0/0, per-`(record, wave)` at the LO limb by
explicit column (R-PM4-1/2 unamended). The **nine named zero-magnitude gaps** are carried as
declared gaps exactly as C-D3 / R-PM4-6 ruled for `krieg_aethertrap.dbr` — absent from the eHP dict
(so a lookup yields a declared zero), **present** in the basis dict (so the absence is named on the
wire), counted in coverage. ⚑ The gaps live in the **roster** table, not the eHP table; a loader
reading only the eHP table would report 401/401 coverage and silently lose nine declared absences.

---

## 5 — ⚑ THE DELTA IS THREE LAWS, AND THE PROOF IS SHARPER THAN BYTE-IDENTITY

**Check 1** — the three cells replayed at I-6 HEAD with `offense_fold` and `band_c_ehp` absent
reproduce **I-5's three surface digests byte-exactly**: `5f6160405d06d993…`, `0ad5b29704a4fbcb…`,
`95a34b2e4fd5cdef…`. **It went RED on the first run** and the wall did its job: my fold-off arm
short-circuited at wave 171 with a *paraphrased* terminal `detail` string instead of letting the
band-B lookup raise its own `ValueError`. A paraphrased terminal message is a moved surface. Fixed
by removing the short-circuit; the fold-off arm now takes the identical exception path.

**Check 9 is the sharper one.** `M_inst` / `M_dot` multiply magnitudes **after** every `uniform()`
and `randint()` call in `resolve_attack`, and add no branch above a draw. So the threat RNG must be
consumed identically fold-on and fold-off — and it is, on all three cells. The consequences are
measured, not argued:

| observable | I-5 | **I-6** | |
|---|---:|---:|---|
| like-for-like 151–160, all three cells | 816.0816 / 231.1837 / 233.5510 s | **816.0816 / 231.1837 / 233.5510 s** | **IDENTICAL** |
| per-wave clear times, 151–170 | — | — | **IDENTICAL to the tick** (check 10) |
| ring density engage med/p90/max | 0 / 4 / 19 | **0 / 4 / 19** | IDENTICAL |
| ring density engage **mean** | 1.1818927341315402 | **1.1818927341315402** | IDENTICAL to 16 digits |
| ring density disc med/p90/max | 0 / 5 / 32 | **0 / 5 / 32** | IDENTICAL |
| overlapping pairs/tick (post-solve) | 6.1840 | **6.1840** | IDENTICAL |
| K-2 barrier procs / rolls | 110 / 398 | **110 / 398** | IDENTICAL |
| K-5 War Cry / K-6 Ascension firings | 67 / 21 | **67 / 21** | IDENTICAL |

> **⚑ The offense fold can move HP and nothing else. T2 and T3 could not have moved, and they did
> not.** That is a structural fact about this iteration, established before the run as P.7 and
> confirmed — and it means **T2's and T3's verdicts carry over from I-5 unchanged, on identical
> numbers.** An iteration that could not have touched two of the four target bands should say so
> plainly rather than re-report them as if they were evidence about the fold.

---

## 6 — ⚑ THE RESULT: THE COUNTERPLAY STACK WAKES UP

Basis: `cells.<cell>.hp_excursions`, `cells.<cell>.counterplay.telemetry`, `cells.<cell>.offense`.

| quantity | I-5 | **I-6 (reference cell)** | video-measured |
|---|---:|---:|---:|
| **mean HP** | 0.9938 | **0.9863** | **0.932** |
| **min HP** | — | **0.3915** | 0.28 (terminal floor) |
| **excursions below 0.70** | **0** | **⚑ 12** | **7** |
| excursions below 0.90 | — | 30 | — |
| excursions below 0.50 | 0 | **3** | — |
| ticks below 0.50 | **0** | **13** | — |
| **K-1 Turtle Shell firings** | **0** | **⚑ 2** (12,200 absorbed) | — |
| **K-3 Menhir's Will firings** | **0** | **⚑ 1** (7,001.75 instant + 1,204.90 regen) | — |
| **K-4 potion firings** | 1 | **2** (11,602.50 instant + 10,070.54 HoT) | — |
| counterplay healed total | 10,836.52 | **29,879.69** | — |
| counterplay absorbed total | 256,506.47 | **285,310.99** | — |

**L-12's headline sentence is retired.** I-4 reported *"K-1 Turtle Shell fired 0 … HP never reached
50 %"*. It reaches it now, thirteen ticks' worth, and the decoded triggers fire on their own decoded
thresholds with no policy added.

### 6.1 — ⚑ The HP trace is END-OF-TICK, and the K-3 firing proves it under-reports the depth

Menhir's Will triggers at `hp_frac ≤ 0.33`. The reference cell's **minimum end-of-tick HP is
0.3915** — above the trigger. Both are true: the counterplay chain evaluates its triggers on HP
*inside* the tick, after the damage event and before the tick's heals land, and `tracks.player_hp`
records the *end-of-tick* value. **So the true intra-tick minimum is deeper than 0.3915, and K-3's
single firing is the proof.** The excursion instrument is therefore a **lower bound on depth**, and
every excursion count in this note should be read as one. Named because the two numbers look
contradictory and a reader is owed the reconciliation rather than left to find it.

### 6.2 — Where the damage went, against the projection I wrote before the run

Basis: `cells.cluster_defon.offense.damage_by_kind` vs math note § 6.

| term | I-5 | **projected** (§ 6) | **I-6 measured** | ratio |
|---|---:|---:|---:|---:|
| `damage_direct` | 582,165.51 | 1,067,109 | **1,071,841.38** | ×1.8412 |
| `damage_leech` | 59,171.00 | 108,461 | **108,848.48** | ×1.8395 |
| `damage_dot` | 36,599.12 | 3,404 | **3,344.70** | **×0.0914** |
| `damage_percent_current_life` | 516,887.51 | 516,888 | **509,086.50** | ×0.9849 |
| **`damage_total`** | **1,194,823.13** | **1,695,862** | **1,693,121.06** | **×1.4170** |
| `heal_landed` | 703,340.09 | — | **1,056,676.09** | ×1.5024 |

**The static projection was accurate to 0.16 % on the total.** The one term that moved off it is
`percent_current_life` (−7,801, −1.5 %) — and that is the **negative feedback I named in advance**:
pcl damage is a fraction of *current* HP, so a lower HP trace produces less of it. It is the only
place in this note where I predicted a mechanism and the mechanism behaved.

---

## 7 — THE THREE CELLS, AND THE MATRIX STILL DISCRIMINATES

| cell | terminal | t_s | mean HP | min HP | exc <0.70 | K-1 | K-3 | K-4 | intake |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CAMP/DEF-OFF | `arena_tier_exhausted`@171 | 1,939.67 | 0.9946 | 0.3604 | 16 | 4 | 1 | 6 | 1,810,898 |
| CLUSTER/DEF-OFF | `arena_tier_exhausted`@171 | 521.55 | **0.9802** | **⚑ 0.0521** | 20 | 4 | 1 | 5 | 1,927,210 |
| **CLUSTER/DEF-ON** ← reference | `arena_tier_exhausted`@171 | 497.71 | 0.9863 | 0.3915 | 12 | 2 | 1 | 2 | 1,693,121 |

**⚑ CLUSTER/DEF-OFF reaches 5.2 % HP and does not die.** That is the closest any cell in this run
has come to the reference outcome, and it is the *defences-off* cell — the one Matt did **not**
play. The defensive sheet is worth roughly the difference between 0.05 and 0.39 at the floor.

---

## 8 — SENSITIVITY CELLS (diagnostics, NOT matrix cells)

Basis: `sensitivity`. Adding a matrix cell is the conductor's ruling, not the sim's.

| cell | what | mean HP | **Δ vs reference** | min HP | exc <0.70 | DoT | intake |
|---|---|---:|---:|---:|---:|---:|---:|
| reference | run-of-record | 0.986275 | — | 0.3915 | 12 | 3,344.7 | 1,693,121 |
| **S-PCL** | scale `percent_current_life` too | 0.984593 | **−0.001682** | 0.3833 | **17** | 3,344.7 | **2,106,970** |
| **S-CONV** | HI DoT magnitude convention (per-second) | 0.986210 | −0.000065 | 0.3909 | 12 | 9,001.0 | 1,698,728 |
| **S-STACK** | P-STACK-B refresh on `(source_actor, family)` | 0.986281 | **+0.000006** | 0.3916 | 12 | 2,914.9 | 1,692,698 |

**P.10 CONFIRMED** — the declared exclusion is worth more than either policy choice, by 26× over
S-CONV and by 280× over S-STACK. **P.11 CONFIRMED** — **the stacking policy is immaterial**
(Δ mean HP **+0.000006**), and it is immaterial *because* `M_dot` shrinks the whole DoT term to
0.198 % of intake. That is the honest answer to R-PM4-16's materiality question: **a policy graded
POLICY-NOT-MEASUREMENT turns out not to matter at the measured modifier**, and it would have
mattered at the unmodified one.

**⚑ Law-3 note on S-PCL.** It is the only sensitivity that moves an outcome meaningfully (17
excursions vs 12), and it moves it **toward** the video. It is **NOT** adopted. The reason it is not
adopted is unchanged from the math note, written before it was measured: whether
`offensiveTotalDamageModifier` composes with a proportion-of-pool term is
UNDECODABLE-FROM-SUBSTRATE, and not scaling is the lower reading. **Adopting it now, because it
moves an observable toward a target, is precisely the shape Law 3 bars.** It is reported, priced,
and left for a decode.

---

## 9 — ⚑ THE MATCH GATES: UNMOVED, BY CONSTRUCTION, AND SAID SO IN ADVANCE

Basis: `match_gates` (reference cell). The **NOTE-9 caveat carried unchanged**: `ground px → m` is a
DECLARED GAP (OBS-H2-9); the video's ring and the sim's radii are **not equated numerically**
anywhere. No pixel scale is invented in this iteration either.

| gate | I-5 | **I-6** | video target | verdict |
|---|---:|---:|---:|---|
| **MG-1** ring density median | 0 | **0** | 1 | MISSED |
| **MG-2** ring density p90 | 4 | **4** | 3 | MISSED |
| **MG-3** ring density **max** | 19 | **19** | **10** (R150) | MISSED, ratio **1.9×** |
| **MG-4** moving fraction | 0.8366 | **0.8365970051012013** | **0.883** | MISSED (sim under) |
| **MG-6** longest stationary | 1.3878 s | **1.3877551020408165 s** | ≤ 1.40 s | **MET** |
| **MG-7** dash rate | 5.3517 s / 93 | **5.351766513056837 s / 93** | 5.3235 s | **MET** |

**Every gate reproduces I-5 to the last digit** — P.12, pre-registered and confirmed. **This is not
a result about the offense fold**; it is the fold proving it stayed inside its own boundary. Two of
seven MET, unchanged for a third iteration.

---

## 10 — ⚑ THE D-I5-1 RING-GATE TRIGGER INPUTS THE CONDUCTOR ASKED FOR

R-PM4-15 gated the converging-solver iteration behind a pre-registered two-clause trigger: *"if
after I-6 the ring-density gate (1/3/10) still misses **AND** overlap pairs are measurably
implicated in the miss, C fires as I-7."* Both clauses, measured:

**Clause 1 — does the ring gate still miss?** **YES**, and by exactly the same amount: 0 / 4 / **19**
against 1 / 3 / **10**, mean 1.1818927341315402 — identical to I-5 to sixteen digits, because the
offense fold cannot move geometry (§ 5).

**Clause 2 — are overlap pairs measurably implicated?** Here is the measurement, computed from
`geometry.radii_of_record()` (Lap F, LO limb, R-PM4-7) and `D_ENGAGE_M = 2.4`. A ring of `n` bodies
at the engage distance is non-overlapping only if every body's radius `r ≤ d_engage · sin(π/n)`:

| ring occupancy `n` | required `r_max` | measured records EXCEEDING it |
|---:|---:|---|
| **10** (the video's max) | 0.7416 m | 92 / 297 = 31.0 % |
| 12 | 0.6212 m | 103 / 297 = 34.7 % |
| 15 | 0.4990 m | 152 / 297 = 51.2 % |
| **19** (the sim's max) | **0.3950 m** | **196 / 297 = 66.0 %** |

And the reciprocal statement: **ring capacity at the board's MEDIAN radius (0.500 m) is 14.97
bodies**; at the pet mode radius (0.360 m) it is 20.86; at the player's own 0.32 m it is 23.49.

> ### ⚑ **THE SIM'S RING MAX OF 19 IS NOT ACHIEVABLE WITHOUT OVERLAP AT THE BOARD'S MEDIAN BODY SIZE.**
> Two-thirds of measured records are too large to sit 19-abreast at `d_engage` without
> interpenetrating, and the observation-time census carries **6.1840 overlapping pairs per tick**
> (pre-solve 8.9969, solver reduction **31.26 %**, worst penetration **0.9470 m**, 605
> player-overlap pairs over 6,097 censused ticks). **Clause 2 reads MET on this measurement.**

**I am reporting the inputs, not the verdict.** The trigger is the conductor's to fire, and I note
one honest counter-argument against my own reading: at the **pet mode** radius (0.360 m, 52 of 297
records) the capacity is 20.86 and a ring of 19 is geometrically legal — so *if* the ring's peak
occupancy is dominated by small summon bodies, overlap is implicated less than the median figure
suggests. **I did not measure the joint distribution of ring occupancy against body size**, and I
will not assert a verdict I have not measured. If the conductor wants clause 2 decided rather than
argued, that joint is a one-instrument addition and I will build it.

---

## 11 — PRE-REGISTERED PREDICTIONS vs OUTCOME — **nine confirmed, one split, four falsified**

The falsified ones keep their original wording (the run's standing practice).

| # | prediction | outcome |
|---|---|---|
| **P.1** | mean HP in **0.955–0.985**, point 0.972 | **⚑ FALSIFIED. 0.9863** — outside the top of my own band by 0.0013. Named as the one I most expected to be wrong, and it was, in the direction I named |
| **P.2** | the player does NOT die by wave 170 | **CONFIRMED** |
| **P.3** | K-1 fires **0–3** (point 0) and **K-3 fires 0** | **⚑ FALSIFIED, AND THE FALSIFICATION IS THE FINDING.** K-1 = 2 (inside the band, point estimate wrong); **K-3 = 1**, which is the stated falsifier. The counterplay stack woke up |
| **P.4** | K-4 potion fires ≥ 1 | **CONFIRMED** (2) |
| **P.5** | **ZERO** ticks below 0.70 | **⚑ FALSIFIED, AND HARD. 87 ticks / 12 excursions** — and the sim now OVERSHOOTS the video's seven |
| **P.6** | DoT falls to ≤ 0.35 % of gross intake | **CONFIRMED. 0.198 %** (3,344.70 / 1,693,121.06) |
| **P.7** | per-wave times identical to I-5; like-for-like reproduces 233.551 s exactly | **CONFIRMED**, on all three cells, to the tick |
| **P.8** | terminal becomes `arena_tier_exhausted` @171 | **CONFIRMED** on all three cells — C-I6-2 pre-registered before it was hit |
| **P.9** | `damage_total` in 1.30×–1.45× of I-5 | **CONFIRMED. ×1.4170** (projection ×1.419 — 0.16 % off) |
| **P.10** | S-PCL moves mean HP more than S-STACK and S-CONV | **CONFIRMED** (−0.001682 vs +0.000006 vs −0.000065) |
| **P.11** | S-STACK moves mean HP by < 0.002 | **CONFIRMED. +0.000006** |
| **P.12** | match gates do not move at all | **CONFIRMED**, every gate to the last digit |
| **P.13** | three batons FULL, 67/67, nothing widened | **CONFIRMED.** VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33 ×3 |
| **P.14** | fold-off reproduces I-5's baton digests | **SPLIT — and the caveat is mine to state.** The three I-5 specs re-emitted at I-6 HEAD differ from their published batons in **exactly two keys each**: `sim_pin.engine_version_full` and `…_sha`. Every event row, actor, position and HP value is identical. But a baton **pins its own commit**, so a raw digest match across a commit is impossible by construction; the byte-exact statement about the *simulation* is check 1's surface digest, and I should have written P.14 that way |

### ⚑ 11.1 — The unifying error, and it is a NEW shape

I-1: priced sustain, not exposure. I-2: priced eHP, not co-residence. I-3: priced throughput, not
the monsters' reach. I-4: priced the size of the counterplay, not its shape. I-5: priced the repair,
not its convergence. **Here I priced the MEAN and never priced the VARIANCE.**

My § 6 arithmetic projected the totals to 0.16 %. It said **nothing** about the distribution, and
every one of P.1, P.3 and P.5 is wrong for the same reason: I reasoned about intake as a rate
against a healing rate, and the thing that produces excursions is **bursts landing in dry stretches**
— which I *named* in the math note (`dry_fraction_whole_run` = 0.5793) and then did not put into a
prediction. **The mechanism was in front of me, written down, and I forecast the mean anyway.**

### 11.2 — ⚑ The finding this iteration actually produced

| | sim (I-6) | video |
|---|---:|---:|
| mean HP | 0.9863 | **0.932** |
| excursions below 0.70 | **12** | **7** |

**The sim now has MORE excursions than the video and a HIGHER mean.** Those two facts together are a
**shape** statement, not a magnitude one: the sim's trace is *near-full with occasional deep spikes*;
the video's is *persistently depressed*. Closing the mean by adding more burst damage would push the
excursion count further past seven. **The residual is no longer "not enough intake" — it is "intake
arrives in the wrong distribution", and that re-prices what the next iteration should be.** The
terms most likely to produce *sustained* rather than *bursty* pressure are the ones § 12.4 names:
to-hit (+50 flat OA against a 23.7 % miss rate) and attack speed (+11 %), both of which raise the
*frequency* of intake rather than its per-event magnitude.

### 11.3 — The DoT tension, reported and not reconciled

Matt: *"some kind of poison/dot seemed to effect me in a major way on my last wave."* Lap I: the
Crucible pulls DoT down −91 points. The sim, folded honestly: DoT is **0.198 %** of intake and
**0.0149 %** of the terminal wave's. Lap I already reported the adjacent discrepancy (wave 159's DoT
spike is 65 % **bleeding**, 7 % poison) and declined to reconcile it. **I decline too, on the same
grounds, and note only that the sim's terminal wave is not the reference's terminal wave** — ours is
170 and cleared; his was 160 and killed him.

---

## 12 — ⚑ WHAT GOES TO THE CONDUCTOR — two cliffs, one ruling request, no HALT

1. **§ 3 — the DoT-rider fold is a double-count and I did not run it.** Lap I's 198 DoT keys are a
   strict subset of the 374 the sim already resolves. R-PM4-16 item 2 is delivered as the **−91
   modifier on the existing riders**. If the conductor intended a *replacement* of PM-2's DoT
   surface by Lap I's (narrower population, different rank basis), **that is a different iteration
   and I have not improvised it.**
2. **⚑ C-I6-2 — the arena wall at content tier 18.** Band-C eHP alone does not make T1 measurable
   above 170. Options, and **I adopt none of them on my own authority**:
   **(a)** accept `arena_tier_exhausted` @171 as the honest ceiling and judge T1 only in the
   death-by-≤170 branch; **(b)** fire a **Lap J** `Maps.arc` decode of `p01_tier18..20` placements
   (legolas, the Lap-F / L-46 instrument); **(c)** rule tier-17 geometry as carried forward — which
   I flag as an **extrapolation of measured geometry** and will not adopt myself.
   **My lean: (a) now, (b) if the run intends to reach a death above 170.** Note that (a) costs
   nothing today: the player does not die at any wave, so the wall is not currently what stops T1
   from being met.
3. **C-I6-1 — the record's own damage modifier is UNMEASURED for band B**, and on Lap I's one worked
   example (`nemesis_wendigo_01`, L=109) the own term (**109**) is **larger than the wave and
   Ultimate terms combined** (83). Lap I emits it on the band-C roster only; Lap D declared damage
   NOT-IN-SCOPE on all 791 band-B rows (C-D4). Folding it for C and not B would manufacture an
   instrument artifact at 171, so it is folded **nowhere**. Closure path: a band-B own-term emission,
   the exact analogue of the band-C column that already exists. **This is very likely the largest
   single unfolded offense term in the run.**
4. **The three adjacent offense terms, named and priced, NOT folded** (math note § 2.4): to-hit
   (`characterOffensiveAbility` +50 % wave + **flat +50** Ultimate) against a measured **23.7 % miss
   rate** (433 of 1,828 resolutions) · attack/cast speed **+11 %** against 6,067 attack
   opportunities · crit damage +27 % against **zero measured crits** (provably cannot bind). ⚑ Per
   § 11.2, **to-hit and attack speed are exactly the shape the residual now calls for** — they raise
   intake *frequency*, which is what closes a mean without widening the excursion tail.
5. **§ 10 — the D-I5-1 trigger inputs are supplied and the verdict is yours.** Clause 1 MET
   (unchanged 0/4/19). Clause 2 reads MET on the median-body measurement, with my own
   counter-argument stated. If you want clause 2 decided rather than argued, the missing instrument
   is the joint distribution of ring occupancy against body radius, and I will build it.

---

## 12b — ⚑ REGRESSION, ANSWERED BY DEPENDENCY CLOSURE + WORKTREE REPLAY (Discipline #11)

The full suite on I-6 HEAD reports **59 failed / 10,487 passed / 21 errors**. That number is
alarming on its face and it is **entirely pre-existing**. Rather than assert that, here is the
proof, in two parts.

**(1) The change surface is fully green.** Every test file in `tests/` that references `kc2`,
`monster_stats`, `kc2_run_adapter` or `baton_v1` — **15 files, 480 tests — is 480/480 PASS.**
(`kc2`-selected alone: 297/297.)

**(2) Nothing outside that selection can reach the changed code.** The reverse-dependency closure of
every module I touched (`kc2/offense.py` new, `kc2/monster_stats.py`, `kc2/threat.py`, `kc2/run.py`,
`export/kc2_run_adapter.py`, `data/kc2/pm4i_*.csv`) is: other `kc2/` modules ·
`export/kc2_baton_emit.py` · `export/kc2_run_adapter.py` · simulation **scripts** (drivers, not
tests). The only test file reaching any of those is `tests/test_kc2_run_adapter.py`, **already
inside the 480**. `comm -23` of the reverse-dependency test set against the 480-selection is
**empty**.

**(3) And the reds were replayed on the predecessor, same instrument.** A `git worktree` at pre-I-6
HEAD **`e26f12b0`** running the two files that carry the reds reports
**33 failed + 21 errors** — identical counts, identical test IDs, to I-6 HEAD:

| file | pre-I-6 `e26f12b0` | I-6 HEAD | seam |
|---|---:|---:|---|
| `test_cycle12_layer4_convergence.py` | **33 failed** | 33 failed | rocket (`skill_tree.py:422 NotImplementedError`) |
| `test_cycle13_wave5_season_generation.py` | **21 errors** | 21 errors | rocket (`season_generation_pipeline.py` cell-grain contract) |

⚑ **What I did NOT do, stated rather than implied:** I did not complete a full-suite run on the
pre-I-6 worktree for a total-count diff. Two concurrent 10.5k-test runs stalled and I killed them
rather than let them burn the lap. The regression question is answered by (1)+(2) — a dependency
closure plus a green surface is a **stronger** argument than two matching totals, because it says
*why* nothing else could move — and (3) supplies the direct before/after on the tests that are
actually red. **The 26 failures not itemised in the table above sit in files that cannot import
anything I changed.**

---

## 13 — DECLARED ASSUMPTIONS + CLIFFS

**New this lap:** **C-I6-1** own damage modifier unmeasured for band B (§ 12.3) · **C-I6-2** arena
tier-18 geometry absent (§ 4) · **P-STACK-A** declared as run-of-record, POLICY-NOT-MEASUREMENT
(immaterial at Δ +0.000006) · `percent_current_life` NOT scaled, declared, priced at S-PCL ·
`M_inst` does NOT compose with `M_dot` (Lap I § 5.4, the lower DoT reading) · `SlowLifeLeach` /
`SlowManaLeach` carry `M_dot = 1.0` **by name, not by prefix match** · **no clamp on `M_dot`** (min
additive sum over 151–200 is −93.0 ⇒ ≥ 0.07; a clamp that never fires is a constant nobody can
audit, and below zero the loader raises so the fold is ruled, not floored).

**Carried unchanged:** C-I5-1…C-I5-4 (the Jacobi pass count untouched per **R-PM4-15**) ·
C-I4-1…C-I4-7 · C-I3-5 · C-I2-1 · C-E3 · C-D1/C-D2 (**C-D2 now RESOLVED by decode**) / C-D3 /
R-PM4-6 · C-F1/C-F3/C-F4/C-F5 · C-G3 · C-G6 · **OBS-H2-9 (ground px → m)** · Lap I's C-I1
(convention) / C-I2 (three absent wight records) / C-I3 (damage-chain additivity) / C-I4 (pets and
the damage fold) · wave 154's travel outlier, undiagnosed for a **seventh** lap.

**⚑ LAW 3 — `moved: {}`, over ELEVEN witnesses.** No constant is added, removed or moved. Four CSVs
are added; every one is a measured table consumed by explicit column. **No number in this iteration
was chosen for its effect on T1–T4.** The one sensitivity that moves an outcome toward the video
(S-PCL) is reported and **not adopted**, for a reason written down before it was measured.

---

## 14 — SEAM WORK

**star-lord** — **no schema change is requested and none is needed.** No baton field, no enum
member, no validator predicate, no gate-wall pin, no tolerance. One additive wave-dict key
(`waves[].offense_fold`, keyed only when active, not inside `waves[].body_geometry`); two additive
spec fields; three specs. `hp_max_basis` gains new **values** on the existing parametric-`str`
column (`MEASURED-BAND-C-LO@w<NNN>` + three `GAP:ABSENT:*` forms) — the shape band B introduced at
I-1, policed by the boundary validator you placed there. Both MIGRATION files carry the detail.
⚑ **`AC-11.4e` refused the first FULL-grade emission on `engine_tree_state == 'dirty'`.** The code
was committed and the batons re-emitted rather than downgraded to PARTIAL — recorded because the
refusal is the gate behaving exactly as designed on the seam most tempted to shortcut it. ⚑ One
thing to carry forward: **if a gate ever sees an I-6 baton whose geometry differs from its I-5
sibling, the fold has leaked past its own boundary** — check 9 says it cannot, and that is a
falsifiable claim a consumer can hold me to.

**drax / scene consumers** — the crowd shape, positions and pacing are **byte-identical to I-5**;
nothing a renderer draws has moved. What HAS moved is the player's HP curve: it now dips, twelve
times below 70 % and three times below 50 %, with a floor of 39 % on the reference cell and **5 %**
on CLUSTER/DEF-OFF. A health bar that was effectively static now has something to animate. D-I5-1's
caveat stands unchanged: **bodies overlap**, ~6 pairs per tick, worst penetration 0.947 m.

**rocket** — nothing. **legolas** — Lap I consumed; the DoT-rider subset finding (§ 3) and the
arena-geometry gap (§ 4) are the two things a follow-on lap would want. **jack-ryan** — Disciplines
#1, #2, #3, #11, #12 exercised and named; **#12 is the whole iteration** and **#11 caught D-I6-1**.

---

## 15 — ⚑ SELF-ATTACK SURFACES

1. **I predicted the mean and the mean is the one thing I got right.** § 6.2's projection lands
   within 0.16 % of the measured total — and P.1, P.3 and P.5 are all wrong, because a total says
   nothing about a distribution. The variance was the whole finding and I had written its driving
   number (`dry_fraction` 0.5793) into my own math note without predicting from it.
2. **P.14 was badly worded and I only noticed when it was time to grade it.** A baton pins its own
   commit; "reproduces the baton digest byte-exactly" is unachievable across a commit **by
   construction**, and I wrote it as a prediction anyway. The measurement I actually wanted is
   check 1's, which passed.
3. **D-I6-1 is mine.** `terminal_shape` divided by a tick PERIOD instead of multiplying and reported
   the terminal wave as **2,339.75 s** — a number wrong by a factor of 150 that still reads as
   seconds. Caught by cross-summing against `per_wave_s[-1]` (15.59 s) before publication, not by a
   test. **The same class as I-4's "3,237" prose defect**, one lap after the conductor banked it
   against me, and the only reason it did not ship is that I cross-checked a number I had no
   specific reason to doubt.
4. **§ 10's clause-2 verdict is the one place I could have overclaimed and I have flagged it
   myself.** The median-radius argument is real, but the joint distribution of ring occupancy
   against body size is what actually decides it, and I did not measure it.
5. **Check 1 went RED on the first run because of my own paraphrase.** The fold-off arm invented a
   terminal message instead of reproducing the exception path. The wall caught it in one run — but
   I wrote the short-circuit in the first place, and a short-circuit that changes an emitted string
   is exactly the kind of "harmless" convenience this run keeps punishing.
6. **The run's largest divergence is smaller but not closer.** Mean HP 0.9938 → 0.9863 against a
   measured 0.932 is a 12 % reduction in the gap; twelve excursions against seven is an
   **overshoot** in a direction that did not previously exist. I do not think this iteration
   converged anything. I think it changed what the residual is made of.

---

*No constant was tuned. Nothing was aimed at a band. The one sensitivity that moves an outcome
toward the video was measured, priced, and left unadopted.*
