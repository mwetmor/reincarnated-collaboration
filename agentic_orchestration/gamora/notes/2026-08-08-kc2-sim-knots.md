# KC2 Phase E — SIM-KNOTS for `actors[].path[]`: the trajectory, written down

**Date:** 2026-08-08
**Author:** gamora (simulation seam)
**Commission:** **R-L80-2** (ledger L-80(c)) — conductor-fired, named-agent.
**Supplies:** star-lord fork **F5-E** (`actors[].path[]` + `path_model`); supply side of drax's
**OBJ-1**, which gates the Phase-E emit.
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/kc2-mover-knots-2026-08-08.md`.

> **DETERMINISM VERDICT: EXACT.** Three legs, 115,218 leaves compared, zero differences, identical
> SHA-256 on the recorder-OFF and recorder-ON surfaces. No HALT. The artifact of record was opened
> **READ-ONLY** and is unchanged on disk; knots land beside it.

---

## 1 · What the commission was, and what was actually missing

`Mover` computes spawn → patrol-node → engage **every tick** and records three scalars off it
(`contact_t_s`, `engage_t_s`, `death_t_s`) plus a running `path_len_m`. The walked polyline existed
in memory for one tick at a time and was then overwritten. **Nothing had to be derived; something
had to be written down.**

The rejected fallback is the reason the standard is high. EVENT-ROW-UNION would have built the path
from positions already on `spawn` and `damage_dealt` rows — every number sim-emitted, nothing
invented — and would still have been *a subsample presented as a trajectory*: under L-A zone-first a
non-ambush body walks to its patrol node **first**, and **no event fires at the turn**. This run
measures that turn on **283 of 344 bodies**. A 2-knot union path would have asserted a straight line
for all 283 of them.

## 2 · The knot predicate (math note § C)

A knot is emitted at every **direction change** of the walked path, at the **start and end of every
dwell**, at the **spawn** point, at the **contact / engage** markers, and at the **terminal** vertex
(death or wave end). Linear interpolation between consecutive knots **is** the sim's position
function.

* **Bend threshold `1e-9` rad.** Bearing float-noise at this build's position scale is ≲ 1.4e-14 rad,
  so the threshold sits ~5 orders above it and a straight leg does not shatter into a knot per tick.
  Because `_last_dir` is refreshed **only at a recorded knot**, deviation cannot accumulate: a
  suppressed bend departs the emitted segment by at most `L·ε ≤ 125 m × 1e-9 = 1.25e-7 m`.
* **MEASURED fidelity:** polyline length vs the length the sim accumulated tick by tick,
  **max |Δ| = 2.1e-13 m** over all 344 bodies — 6 orders inside the computed bound.
* **Dedup is on the `(tick, x, y)` triple, never on position alone.** Two knots at one place and two
  times are a **dwell**; 12 bodies wait 44–70 ticks at the engage ring before dying, and dedup on
  position would have deleted that wait.
* **One declared sub-tick disagreement, and it is a measurement.** The `spawn` knot carries
  `tick` = LAST-STILL-TICK (exactly the F5-M / R-L80-1(M) ruling already taken for
  `actors[].spawn_tick`) and `t_s` = the MEASURED p05 drip instant. They differ by ≤ 1 tick
  (81.6 ms), one-signed, and that difference **is** the drip (AC-10.6). Declared in the artifact,
  not smoothed away. Every other knot has `t_s == tick × tick_period_s` identically — and getting
  that identity to hold required computing the pre-step time as `(k−1)×dt` rather than `t_s − dt`,
  which differ by an ULP at `k = 99`. A test caught it; the note now carries the arithmetic.

## 3 · The determinism verification law (L-80(c)) — asserted, not eyeballed

| leg | what was compared | leaves | verdict |
|---|---|---:|---|
| **1** | the **UNMODIFIED** Phase-E driver's `execute_run(9, cp150)` vs the committed artifact, deep + recursive + exact, **value AND type** (`1 == 1.0` in Python; a type change is still a change to what a consumer reads) | 526 | **EXACT**, 0 diffs |
| **2** | recorder **OFF vs ON**: actors, waves, all 1,900 event rows, every track column, composition, run scalars **and the terminal `Mover` state** (`contact/engage/death_t_s`, `path_len_m`, `node_reached`, the three gate flags — simulated quantities a perturbing recorder would move first) | 114,680 | **EXACT**, 0 diffs, **identical SHA-256** `fcf57111…` |
| **3** | the counts ledger row **L-80** already published for this run | 12 | **EXACT**, 12/12 |

**One exclusion, by name, printed rather than assumed: `wall_s`** — a wall-clock reading of the
host, not a simulated quantity. There is no tolerance parameter anywhere in the driver, and adding
one would be the whole failure it exists to prevent.

LEG-2 is the direct test of the additivity argument (math note § F): no RNG draw, no float
feedback, no control flow outside `if _knots is not None`, no signature break. A separate test
asserts the sharpest form of it — **identical rosters and identical scatter coordinates** OFF vs ON,
which is what a disturbed RNG stream would break first.

## 4 · What the knots measure

**995 knots over 344 actors** — min 2 · median 3 · mean 2.89 · max 5. Histogram `{2: 61, 3: 271,
5: 12}`. Kinds: `spawn` 344 · `start` 339 · `bend` 283 · `contact` 344 · `death` 344 · `engage` 18 ·
`halt` 12.

* **283 paths bend; 61 walk straight.** The split is *exactly* the ambush partition: all 61 straight
  paths are p05 ambush bodies, which take **no patrol leg** (AC-10.11), and every one of the 283
  non-ambush bodies bends **at its own patrol node** (bend position within the 0.5 m node tolerance
  the motion law itself uses). AC-10.11 is now readable off the trajectory rather than off the flag
  that produced it.
* **Max 1 bend per body.** No gate flapping on this run: nothing re-targets node → player → node.
* **The 5 two-knot ambush bodies with `n_steps == 1` and `path_len_m == 0`** spawned *already inside*
  `d_engage` and never moved — spawn and terminal at one point. Honest, and visible.
* **The 12 five-knot paths are the interesting ones:** spawn → bend at node → contact → engage+halt
  at the ring → death 44–70 ticks later. Those are the bodies tough enough to survive the approach.
* **`engage` fires only 18 times** because most bodies die at the disc radius before reaching
  `d_engage` at all — `contact` and `death` land on the same tick and merge into one knot.
* **`path[]` payload: 155.5 B/actor** as compact `{t_s, x, y}` triples, against R-LOCA-1's MEASURED
  price of **357 B/actor** (L-51 corrigendum). **Inside the ruling; no re-pricing needed.** A
  regression to per-tick knots is caught by a test, not by a hope.

## 5 · The seed corrigendum — annotated in place (L-80(d))

My selection-slate note § 3 printed `seed_first_wave 601008` for `E-s09-cp150`. That is
**`E-s09-w1`'s** first-wave seed — a transcription carry from the wave-1 limb. The seed law and the
artifact both read **751008** (`600_000 + 151×1000 + 8`). Raised by star-lord (§ 5), accepted at
L-80(d), routed to my seam. The slate note is **annotated corrigenda-style, not rewritten** — the
wrong value stays visible, struck, with the correction and the pointer beside it. Nothing downstream
consumed it (the adapter *imports* `engine_seed`), and it is not an input to any filter, rank key or
tie-break. Pinned by a test that asserts **both** numbers, so the confusion cannot recur silently.

## 6 · What this does NOT claim

* **It does not close OBJ-1.** This is the sim side of F5-E. The union re-law is star-lord's seam and
  drax's countersign.
* **It validates no motion parameter.** `v_ref` remains `DECLARED-FREE-PARAMETER` (HALT-2); the
  § 10.9a D region is still EMPTY and calibration is still HALTED. A faithfully recorded path
  through a declared-parameter model is a faithful record of *that model*.
* **It derives no heading.** F5-D / F5-F stay DECLARED conventions per R-L80-1.
* **It says nothing about summons.** No `Mover`, no path — OUT-OF-MODEL (R-L53-2). A missing path
  there is an absence, not a gap to fill.
* **It does not re-open the slate.** The re-run reproduces the ranked row exactly; the selection is
  re-verified, not re-decided.

## 7 · Artifacts, tests, hand-off

**The artifact of record is byte-identical to HEAD, and that is CHECKED rather than asserted:**
`kc2-phase-e-seeded-batch-full-20260808_205104.json` — working-tree SHA-256
`a3652a72a60ced603cc98e4a608c17dbec24d54d37a0c45f044adcc592fc3d8d`, identical to
`git show HEAD:<path>`; `git diff HEAD` is empty on that path.

**Side artifact (ADDITIVE; the results JSON of record was NOT rewritten):**
`reincarnated-engine/src/reincarnated/simulation/output/kc2-phase-e-actor-paths-E-s09-cp150-R-L80-2-20260809_025245.json`
(409,813 B — header + provenance + the full three-leg determinism block + knot semantics + per-actor
polylines). Re-running the driver reproduces this file **byte-identically apart from `started_utc`
and `wall_s`** — checked, not assumed, on a second execution.

**Code:** `simulation/kc2/locomotion.py` (`PathKnot`, the recorder, `KNOT_BEND_EPS_RAD`,
`build_mover(record_path=…)`) · `simulation/kc2/run.py` (`simulate_wave(record_actor_paths=…)`, the
marker + terminal knot sites) · `simulation/scripts/gamora_kc2_actor_path_knots_2026_08_08.py`.

**Tests:** `tests/test_kc2_actor_path_knots.py` — **29 new**, all passing. KC2 + locomotion suites
re-run whole (11 files): **260 passed / 0 failed.** **Blast radius enumerated rather than assumed**
(Discipline #10): the **15** test files that reference `kc2` / `locomotion` / `simulate_wave` at all
are the complete set a change confined to `simulation/kc2/` can reach; the other **4** —
`test_baton_v1` · `test_br2_trace_stage_1` · `test_telegraph_value_set_census` ·
`test_wr3_kite_commit_stage2b` — run **166 passed / 0 failed**. **426 / 426 green across the whole
reachable set.** The full-suite red tree (63 F / 21 E at the L-74(d) non-gating baseline, parent
`84996d29`) is unchanged by construction: none of those nodes import this seam.

**MIGRATION.md** entry filed for star-lord with the seven consumer semantics that are *not* obvious
from the field names — chiefly: `tick` is wave-local, the spawn knot's `tick`/`t_s` disagreement is
the drip and must not be snapped to the grid, and a 2-knot path here is a measured straight walk
rather than the subsample that was rejected.

**Tree:** engine COMMIT-ONLY, NO PUSH (R-KC2-10 — the conductor pushes at fold).

---

**Refs:** L-79(e)(h) · L-80(a)(b)(c)(d) · R-L80-1(M) · R-L80-2 · R-KC2-13 · R-LOCA-1 / L-51
corrigendum · R-L53-2 · spec § 10.9a A/C/E · § 11.3 / § 11.3.1 · AC-10.6 · AC-10.11 · JC-G1 / JC-G9
· F5-E · OBJ-1 · Disciplines #1, #2, #11, #12.
