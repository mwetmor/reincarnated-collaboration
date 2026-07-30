# WR2-ENCGEO WARN-discharge micro-cell — four items closed, one WARN's count corrected, and half of WARN-3 declared unreachable from the tree

**Cell:** WR2-ENCGEO-2026-07-29 / WARN-discharge micro-cell. **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Author:** gamora. **Date:** 2026-07-30.
**Governing:** jack-ryan Gate-2 on Cell BAT — `qa/findings/2026-07-29-gate2-gamora-wr2-cell-bat.md`
(**his finding is the contract**). Prior seam note:
`gamora/notes/2026-07-29-wr2-cell-bat-battery-of-record.md`.
**Scope:** WARN-1, WARN-3, WARN-4, INFO-2. **Class: DOC / BANK ONLY.**
**Gate:** this cell gates the **AFTER-baton** to drax (WARN-1's pre-baton gate).

**Engine commits (`~/Games/reincarnated-engine`, `main`, NOT pushed):**

| item | commit | files |
|---|---|---|
| WARN-1 | **`36ea2a5c`** | `src/reincarnated/simulation/MIGRATION.md` |
| WARN-4 | **`33c134b2`** | `src/reincarnated/simulation/wr2_cell_bat_2026_07_29.py` (comment only) |
| WARN-3 | **`74a5a5c5`** | `output/kitcal_g5/wr2_battery_after/wr2_bat_f_wr2_4_ring_life_distances.json` (new) |
| INFO-2 | **`54536c30`** | `tests/test_bq3_calibration_override_door.py` (comment only) |

**Meta commit:** see §6.

> **ZERO LINES OF EXECUTED SIMULATION LOGIC WERE TOUCHED.** The four commits comprise one `.md`,
> two comment-only hunks, and one added JSON artifact. No engine module's behaviour, no constant, no
> flag, no emission, no banked trace, no banked leg report.

---

## 1 — WARN-1: the ADR-004 MIGRATION entry — **DISCHARGED** (`36ea2a5c`)

**What the WARN said.** `21abff12` added three additive keys consumed **outside this seam** —
`presentation_units`, `movement_speed_ms` / `movement_speed_provenance`, `nova_per_projectile_hp` —
and never touched `MIGRATION.md`, while code comments cite an entry that does not exist. Filed as
*"the landing's only real process defect"*; **WARN not BLOCK** because the keys are additive, the
baseline move was already declared in-payload, and the ADR-004 handoff moment (the AFTER-baton) had
not happened, so no consumer had been misled. **Gated to discharge before the baton ships. Content
pre-approved under ADR-002 as documentation-only.**

**What I wrote.** A full entry at the top of `MIGRATION.md`, following the file's existing
newest-first format and the Cell C / Cell D entry structure:

| § | content |
|---|---|
| header | run / authority / **introducing commit `21abff12`** / consumers (**drax** presentation seam, **star-lord** export seam) / "NOTHING IS OWED TO SHIP" |
| §1 | every key by **exact name, type and unit** — the `presentation_units` block (14 paths), the two `FightRecord` fields, the `a_dmg1` sub-key |
| §2 | **the provenance semantics**, which is the WARN's substantive ask: `"kit"` = the kit declared the field; `"engine-default-ungraded"` = `entity_from_class_dict` filled the slot **from its own `5.75` literal**, which is **neither M nor D**. Derived from the class dict's KEY SET, so the harness never transcribes 5.75. Measured 900/900 ungraded on the battery of record. Consumer consequence stated: `T = 2.3188 s`, the 3.09× duration change and the 1.57 s tell delta are **DEFAULT-SPECIFIC** |
| §3 | **drax's decomposer named as the consumer that stops hard-coding 207.40 / 235.40**, why no such constant exists in the engine, why the unit is a SET with a `constant` flag, the six-leg measured table, and the two traps (`nova_unit_payload_hp` ≠ `telegraph.damage_amount`; `n_nova_crossings: 0` + empty list can only mean no crossing) |
| §4 | **star-lord**: the flag-OFF report baseline moves to `21abff12`; trace content, `run_spatial_fight`'s result dict, fight behaviour and the RNG stream all unaffected; **telemetry is owed NOTHING** (no `SpatialFightResult` field, no column, no schema bump) |
| §5 | ⚑ the `movement_speed_ms` **name collision** — Cell D's CONDITIONAL trace field (every entity) vs this entry's UNCONDITIONAL report field (player only). Same quantity, different scope and conditionality, **not interchangeable joins** |
| §6 | why the fields are per-fight and not per-leg only |
| §7 | grep-the-predicate producer map (INFO-4's convention) + the count erratum below |

### 1.1 ⚑ WARN-1's citation count is WRONG, and I measured rather than transcribed it

WARN-1 states *"four comment sites in `kitcal_g5_harness.py` read 'ADDITIVE — MIGRATION.md
2026-07-30 WR2-ENCGEO Cell BAT entry'"*. Measured at HEAD:

```
$ grep -rn "MIGRATION" spatial_gauntlet/kitcal_g5_harness.py
606:  ... ADDITIVE `FightRecord` field (MIGRATION.md 2026-07-29).            # exists
680:  ... ADDITIVE — MIGRATION.md 2026-07-29 entry.                          # exists
687:  ... ADDITIVE — MIGRATION.md 2026-07-29 WR2-ENCGEO Cell B entry.        # exists
700:  ... ADDITIVE — MIGRATION.md 2026-07-30 WR2-ENCGEO Cell BAT entry.      # THIS ENTRY
2110: ... (MIGRATION.md 2026-07-29 M-6 entry §2).                            # exists
```

**Exactly ONE site cites this entry.** Five comments cite `MIGRATION.md` at all; the other four name
**2026-07-29** entries, every one of which is present in the file. The three other Cell BAT emission
sites carry ruling citations (`R-WR2-15(2)`, charter §8.24, Gate-2 Cell D INFO-1) but **no**
`MIGRATION.md` pointer, so they were never dangling.

**The ADR-004 gap WARN-1 found is real and is the one I closed.** Only the multiplicity was wrong.
Recorded in the entry itself (§7) and here for the same reason WARN-5 was recorded: *true where
measured, wrong where labelled* — a count on record that nobody re-measures becomes a premise. The
micro-cell brief repeated the "four comments" figure, so it would have propagated to a third hand.

---

## 2 — WARN-4: the self-refuting comment — **DISCHARGED** (`33c134b2`)

**What the WARN said.** `wr2_cell_bat_2026_07_29.py:82-84` claimed the harness label-suffix order is
*"derived, not transcribed"*. `AFTER_SUFFIX = "_dec_bsep_mv2_ntv2"` is a **string literal**, so it is
transcribed, and the comment named the exact hazard ("a second source of truth for a filename") that
the line below instantiates. Cell BAT §2.2 and `f1ab3b09`'s message both **correctly reported** the
claim as wrong; neither corrected it; charter §8.29 then recorded that the cell *"corrected two wrong
comment claims"* — **zero** were corrected and there was only **one** (the crossing-ledger index item
was confirmed CORRECT, never a wrong claim). Prescribed fix: restate as TRANSCRIBED and name the
verification site.

**What I changed.** The comment now reads **TRANSCRIBED**, names the verification site
(`kitcal_g5_harness.py:2378-2394`, the `label += "_dec" / "_bsep" / "_mv2" / "_ntv2"` chain), and
supplies the **grep that survives line drift** per INFO-4's convention. A ⚑ erratum block states
that the STRING was and remains correct — only the claim about how it got there was wrong — so no
reader can mistake this for a value change, and it names the family (Cell C WARN-1, Cell D WARN-1).

**Verification.** `AFTER_SUFFIX` / `BEFORE_SUFFIX` re-read from the imported module after the edit:
`'_dec_bsep_mv2_ntv2'` / `'_dec'`, unchanged. All six `leg_dir(...)` paths still resolve onto the
existing banked leg directories (3 AFTER + 3 BEFORE, all `OK`), so no artifact path moved.

**⚑ Side effect, recorded because it is INFO-4 proving itself inside one day:** this comment added
ten lines, so the BQ-3 door call site moved **`:462` → `:472`**. Nothing about the site changed.

---

## 3 — WARN-3: F-WR2-4's substrate — **HALF DISCHARGED BY MEASUREMENT, HALF DECLARED UNREACHABLE** (`74a5a5c5`)

**What the WARN said.** §5.2's three-row resolution table is F-WR2-4's whole ground and exists
nowhere but the cell note; `wr2_bat_statistics.json`'s clause-2 arm banks `crossing_r_star_m: []` for
`after_m3` and no distances at all. *"A banked conductor finding has no banked evidence."* Fix: emit
the per-ring `(t_s, dist_to_origin, rho)` rows **for both M-3 arms** as a sibling artifact.

### 3.1 What I banked

`output/kitcal_g5/wr2_battery_after/wr2_bat_f_wr2_4_ring_life_distances.json` (717 KB), a sibling of
the existing `wr2_bat_s7_firings.json` / `wr2_bat_statistics.json` /
`wr2_bat_residual_counters_four_tier.json` bank, in the same naming family.

| arm | evidence class | firings | crossed | `dist_to_origin` envelope over ring life | tick-grid `r*` |
|---|---|---|---|---|---|
| **AFTER_prod** (dec+bsep+mv2+ntv2, M-3 dark) | BANKED + git-TRACKED | **132** (44 × 3 legs) | **132** | **[4.061857242637549, 5.335767806064837] m** | 4.430557933863834 |
| **BEFORE_prod** (dec only, M-3 dark) | ⚑ on disk, **UNTRACKED** (Gate-2 INFO-4), deterministically regenerable | **132** | **132** | **[5.206090523869769, 6.816090523869766] m** | 5.901075563… |

Every firing carries its **full per-tick sample list** — `{tick, t_s, dist_to_origin_m, rho_m,
gap_m, alive}` — plus `dist_first/last/min/max`, `player_beyond_death_radius_whole_ring_life`,
`crossed_on_tick_grid`, `t_star_s_tickgrid`, `r_star_m_tickgrid`, and the firing's origin / onset /
`fire_t_s` / `wind_up_s` / `radius_m`.

**Method: READ-ONLY RE-DERIVATION FROM BANKED TRACES.** No fight was simulated. `rho(t)`, the ring
velocity (14.0 m/s) and the death radius (12.0 m) are **imported** from
`gd_nova.PRIMORDIAN_FRIGIDRING` at extraction time, never transcribed (the C-4 lesson). Firings
selected and the player joined by the **MIGRATION §6 contract** (`record_type: "event"` /
`event: "telegraph"` / `":nova:"`; header `is_player` → `entity_id`).

### 3.2 The verification the brief asked for: **the extraction reproduces the PROD limb exactly**

jack-ryan's Gate-2 §4.1 PROD-AFTER limb: *"the player sits at **4.06 → 5.34 m** from the ring origin
across the ring life and **44 of 44** firings per leg cross (delivery 1.0000, three legs,
**132/132**)"*, with his tick-grid estimate **4.4306**. My extraction: **4.061857242637549 /
5.335767806064837**, **132/132 crossed**, `r*` **4.430557933863834**. **Reproduced at every printed
digit, on an instrument written independently of his.**

The cell note's `4.09 → 4.93` window is shown to be a **narrower sub-window** of the true ring life
(it starts one tick later and stops at the resolve tick), which is why its endpoints sit inside this
envelope. Named in the artifact, not reconciled away. **Both `r*` grades ride in the payload** — the
engine's sub-tick solve (4.6867, from `NovaScheduler.resolve_tick`'s bracketed solve) and the
tick-grid estimate — because that exact ambiguity is what WARN-3 was filed to remove.

### 3.3 ⚑ FLAG — the 12.1944–12.7789 m row is **NOT EXTRACTABLE FROM ANY BANKED FILE**

**Per the brief's instruction: I did not reconcile silently. I am flagging it prominently.**

The brief asked me to verify that my extracted values reproduce the **12.19–12.78 m** range cited in
F-WR2-4. **They do not, and they cannot** — and this is a **scope fact, not a numeric discrepancy**:

* **12.1944 → 12.7789 m** and **6.6999 → 8.4248 m** are the **`after_m3` / `before_m3` arms** — the
  **M-3 (`piloted_competence`) paired arms**.
* **M-3 is DARK on the battery of record by charter design** (`wave_regime.piloted_competence_m3:
  null`). The clause-2 arms are constructed **in process** by
  `wr2_cell_bat_2026_07_29._fight_engine_direct_flagged` and write **no trace directory**.
* **Verified rather than assumed:** no `*m3*` root exists anywhere under `output/kitcal_g5/`; the
  only trace corpora on disk are the two PROD arms above (456 tracked files under the AFTER root,
  455 untracked traces under the BEFORE root).
* The banked 450 AFTER traces are the **M-3-dark production** arm, which is why they yield
  **4.06 → 5.34 m** and not 12.19 → 12.78 m. **Both figures are jack-ryan's own**, on adjacent rows
  of his §4.1 table — the finding is internally consistent; the *extractability* is what differs.

**What IS banked for the M-3 limbs** (and worth stating, because it is not nothing):
`wr2_bat_statistics.json → s7_clause2.arms.before_m3.per_leg.*.crossing_r_star_m` = 22 ×
`6.69990598342503` per leg, the **engine's own solve**, which jack-ryan independently reproduced
(`6.699906`); and `after_m3 … crossing_r_star_m: []` with `crossings: 0`, which is itself the
load-bearing fact (**zero resolutions**, not zero-delivery resolutions). What is absent is the
**per-tick distance profile**.

**Residual obligation, routed to the conductor rather than attempted:** closing the M-3 half requires
an **instrumented re-run of `s7_clause2`** — sample the live ring's origin and the player position
each tick of ring life and emit the rows. That is a **driver change plus a simulation execution**,
both outside a doc/bank-only cell. The artifact declares this in its own payload under the key
`"⚑ NOT EXTRACTABLE FROM THE BANKED TREE — the M-3 limbs"`, so a future reader meets the gap in the
bank rather than in a note.

**This does not weaken F-WR2-4.** The load-bearing claim — the front dies at 12.0 m before reaching a
player who is beyond 12.0 m for the *entire* ring life — was independently reproduced by jack-ryan
on his own instrument and confirmed in source at `gd_nova.py:917`
(`if r_star > ring.params.projectile_distance_m: continue`). What remains un-banked is the
digit-level substrate for two rows, not the mechanism.

---

## 4 — INFO-2: the falsifier citation — **DISCHARGED** (`54536c30` + the meta erratum)

**What the INFO said.** The BQ-3 discharge wrote *"Verified with `T8b_the_sweep_is_not_vacuous`
green, so the entry cannot have blinded the detector."* **T8b never reads `_DOOR_ALLOW_LIST`** — it
re-implements the AST predicate over a **synthetic source string**, so it speaks to the *detector*,
not to *blinding*. What proves non-blinding is the **set-difference structure plus the enumeration**.

**Re-run, not transcribed** (I executed the sweep with and without the entry):

```
ALL door-opening sites in the shipped tree (4, exhaustive):
   src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py:882
   src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py:153
   src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py:205
   src/reincarnated/simulation/wr2_cell_bat_2026_07_29.py:472
allow-list entries: 3
offenders WITH the Cell BAT entry :  []
offenders WITHOUT the Cell BAT entry: [('…/wr2_cell_bat_2026_07_29.py', 472)]
dead allow-list entries (paths not on disk): none
```

`T8` computes `offenders = all_sites − allow_listed_sites`, so an entry can only remove the sites it
**names**; removing this one yields **exactly one** offender at the line it declares. A path-prefix
or glob entry would announce itself as **extra** sites vanishing — which is *why* the enumeration is
the falsifier.

**Two sites fixed, one immutable:**

1. **The durable home** — the `_DOOR_ALLOW_LIST` Cell BAT declaration comment in
   `tests/test_bq3_calibration_override_door.py` now carries the set-difference argument, the
   enumeration, and WARN-6's line (*run the containment suite against any newly added `src/` module
   before it produces evidence*). Comment-only: membership unchanged (3 entries, same paths),
   `_door_opening_sites()` unchanged, no assert touched.
2. **The site jack-ryan quotes** — cell note §9.1, corrected as an **append-not-rewrite erratum**
   (the struck sentence stays visible because a consumer may already have inherited it), including
   the `:462 → :472` line-number note.
3. **`d05535f9`'s commit message carries the same wrong citation and is immutable.** Not amended
   (never amend); the erratum in §9.1 is the pointer a reader following the commit will land on.

---

## 5 — Verification evidence

**Cheap-suite-first (WARN-6), fired before anything else and again after the last edit:**

```
pytest tests/test_bq3_calibration_override_door.py -q -p no:randomly
  → 39 passed in 9.30s   (pre-edit baseline)
  → 39 passed in 9.07s   (post-edit, final tree)
```

**Seam slice:**

```
pytest tests/test_wr2_b_body_separation.py tests/test_wr2_c_movement_policy.py \
       tests/test_wr2_d_nova_telegraph.py tests/test_kitcal_g5_harness.py -q -p no:randomly
  → 185 passed in 1.00s
```

**Parse + import (the brief's explicit ask):**

```
python3 -m py_compile wr2_cell_bat_2026_07_29.py test_bq3_calibration_override_door.py \
                      kitcal_g5_harness.py            → OK
import reincarnated.simulation.wr2_cell_bat_2026_07_29                        → OK
import reincarnated.simulation.spatial_gauntlet.kitcal_g5_harness             → OK
import reincarnated.simulation.gd_nova                                        → OK
```

**Semantic no-op checks:**

* `AFTER_SUFFIX` / `BEFORE_SUFFIX` unchanged post-edit; all 6 `leg_dir(...)` paths resolve `OK`.
* `_DOOR_ALLOW_LIST` = 3 entries, unchanged; 4 door sites, 0 offenders, 0 dead entries.
* Banked artifact parses; `git status -uno` before commit showed **exactly three** modified tracked
  files and **no** modified trace or leg report.

**No full regression run, and none is owed:** the landing touches one `.md`, two comment hunks and
one added JSON file. Discipline #2 — a ~20-minute regression on a doc/bank-only cell buys nothing the
9-second containment suite and the 1-second seam slice do not already prove. **No simulation was
executed in this cell**, so Discipline #3 (no parallel regen of the same seed) is vacuous here.

---

## 6 — Laws observed, and what is NOT in scope

* **Doc/bank-only.** Zero executed simulation logic touched. No constant, flag, threshold,
  convergence criterion or gate predicate moved, so **Discipline #1 (math-before-code) has no
  hotspot in this cell** — there is no math change to note.
* **Findings reported, never repaired in-cell.** §1.1's count correction and §3.3's extractability
  flag are **reported**, not reconciled.
* **No amend.** `d05535f9`'s wrong citation stands in history with an erratum pointing at it.
* **Committed, NOT pushed** — the conductor pushes.
* **⚑ TWO items from jack-ryan's §14 gamora list are NOT in this cell's scope** and remain **OPEN**,
  flagged here so they are not assumed closed by the AFTER-baton:
  * **WARN-5** — strike "spawn-adjacency" from cell note §1's gate table (§6's "post-solver overlap
    in emitted frames" is the correct form and is already there). Cell-note edit, undischarged.
  * **INFO-5** — loosen §4.2's "±1%" band to the measured **−2.5% (pre) / −3.0% (post)** on trash.
    Cell-note edit, undischarged.

  The micro-cell brief scoped me to four items (WARN-1/-3/-4, INFO-2) and instructed me not to
  expand scope; jack-ryan's finding lists six for gamora. **Divergence recorded rather than
  resolved unilaterally** — both are one-line cell-note edits and I will take them the moment the
  conductor says so.

---

## 7 — What the conductor may want to rule on

1. **§3.3 — the M-3 half of WARN-3.** Accept the PROD-limb bank plus the declared gap, or authorize
   an instrumented `s7_clause2` re-run to close the 12.19–12.78 m rows. The latter is a driver change
   + a simulation execution, i.e. a real cell, not a discharge.
2. **§1.1 — WARN-1's citation count.** One comment site, not four. Third instance in this run of the
   *true-where-measured, wrong-where-labelled* shape, and the second where the count came from a
   Gate-2 finding. Possibly a line in the run's own lessons.
3. **§6 — WARN-5 and INFO-5.** Undischarged by scope. Ruling wanted on whether they ride before the
   baton or after.

*Cell note closes. — gamora*
