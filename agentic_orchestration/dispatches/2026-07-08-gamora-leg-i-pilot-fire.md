# Dispatch — gamora: Leg-i pilot FIRE (two-arm certification; emission-path cell-grain, seed 57000000)

**From:** gamora (simulation seam) → **To:** Matt (explicit fire-go owner) · cc knight-rider / gandalf / jack-ryan
**Date:** 2026-07-08
**State:** FIRE-READY — pre-fire checks GREEN (§C below). **Awaiting Matt's explicit fire-go.**
**Authority:** `pilot_policy` two-arm certification policy Matt-approved 2026-07-08 (`ce595a7`, decisions-log:5347);
KR commissioning transmission (all three preconditions landed); gandalf geared-arm spec.
**#2-FF compliance (eat our own cooking):** this dispatch carries its own start-banner instrument identity,
its pre-fire verification commands WITH actual results, its precondition citations, and its known-residue
note — so the pilot's verdicts are read against a named instrument, and pre-existing noise is not mistaken
for pilot signal.

---

## 0. Gate status — `_PILOT_POLICY_PENDING` is CLOSED (governance-only; no code change)

`gauntlet_lived_channel_repilot_driver.py:73 _read_pilot_policy_version()` parses the FIRST
`pilot_policy=<token>` literal from the decisions-log via
`re.search(r"pilot_policy\s*=\s*([A-Za-z0-9][A-Za-z0-9._-]*)")`. That literal is the 2026-07-07
canonical stamp at **decisions-log:4929** (`pilot_policy=scripted-rotation-v1`), which sits ABOVE the
2026-07-08 two-arm entry (:5347) and therefore wins first-match. **Verified by running the reader NOW:**

```
RETURNED: 'pilot_policy=scripted-rotation-v1'
IS_PENDING: False
```

The `_PILOT_POLICY_PENDING` sentinel (:70) is returned ONLY on log read-failure or regex no-match —
neither obtains. It is recorded into the report at :267 (`pilot_policy_version`) but **does NOT gate
execution** (no branch keys off it). **The gate was governance-only** — satisfied by Matt's approval of
the decisions-log entry (`ce595a7`). **No code change is needed to close it.** The driver already reads v1.

---

## 1. START-BANNER INSTRUMENT IDENTITY (both arms + operative band set)

Leg-i runs TWICE at the same seed (**57000000**), same post-dedup config set (**cell-grain**), same
20-encounter rotation:

- **arm S — STRIPPED (as-built instrument).** The declared certification baseline as of `ce595a7`.
  Renders the PIPE/YIELD instrument-validation verdicts (`measured_gear_stats=None` → stripped baseline,
  `spatial_resolver_adapter.py:149`).
- **arm G — `certification_gear v0`, all four cohort tilts** (offense/defense/utility via
  `_build_cohort_combatant_stats`, `t4_sim_cycling.py:927`). 6b reference-set skeleton + cohort tilt;
  4pc +35% dmg (chain-T4 band MIDPOINT), +18% armor / +12% hp (Legendary-T1 stat band); fixed
  representative Legendary-T1 weapon shell (NOT per-kit rolls). Measures the STAT-POWER layer only
  (the layer that moves WR/KPM); effect-layer/gems/affix-RNG are declared non-goals.
  gandalf spec: `agentic_orchestration/gandalf/notes/2026-07-08-leg-i-geared-arm-certification-gear-spec.md`.

**Operative band table — the exact instrument the verdicts read under** (all 8 rows verified byte-for-byte
against `gauntlet_sim.py` at jack-ryan's canonical write; one citation correction applied there —
escape_lane floor `:240`, not `:242`):

| Shell | Family | Band | Provenance |
|---|---|---|---|
| open_arena | F2 | (20.87, 53.33) | `:486`, R3a step-5 density-anchored (ratified 2026-07-08) |
| chokepoint_corridor | F1 | (12.52, 60.00) | `:487`, R3a step-5 |
| magic_pack | F1 | (12.52, 102.86) | `:504`, R3a step-6 |
| elite_pack | F2 | (8.26, 28.13) | `:506`, verified STANDS this session (`5cabb6c`) |
| dense_cell | F1 | (12.52, 102.86) — **GEOMETRY-ONLY** | `:520`, NEW pilot-precond; density-anchored, no on-disk dist |
| boss_with_adds | F3 | (2.49, 3.78) | `:507`, unchanged |
| mini_boss | F3 | (0.57, 3.30) | `:508`, unchanged |
| escape_lane | F4 | exit-within-window ≥0.80 (PRIMARY) + KPM (60,150) (secondary sanity) — **GEOMETRY-ONLY** | `_F4_EXIT_WITHIN_WINDOW_FLOOR :240` + `_F4_KPM_BAND :241`; registered 2026-07-08 |

F3 boss shells gate on survive-and-kill (KPM is a sanity rail, not the gate). escape_lane gates on
exit-within-window PRIMARY, KPM secondary. F3 boss knob LOCKED `bds=48.0`, boss HP `9000` (60x trash);
mob_damage_scale LOCKED `0.03`.

**Rider-3 disposition read-rule (for every clear-shell verdict):** below-floor = HARD FAIL (exclusionary) ·
in-band = PASS · over-ceiling = FLAG_PASS_OVERPOWERED → balance review (certifies + flagged; difficulty-
ladder input per ruling A, NOT a cert gate). Routing (`_miss_taxonomy`, driver :93) is baseline-INVARIANT.

---

## 2. PRE-FIRE VERIFICATION COMMANDS + EXPECTED RESULTS

Run from `~/Games/reincarnated-engine`:

- `grep -n measured_gear_stats src/reincarnated/simulation/t4_sim_cycling.py` → **non-empty** (arm-G gear
  threaded on the gauntlet path).
- `grep -c escape_lane src/reincarnated/generation/endgame_encounter_catalog.py` → **≥1** (F4 member present).
- **First-log-lines expectation:** `"N distinct configs | 20 encounters"` (post-dedup N cell-grain distinct
  configs; `GAUNTLET_ENCOUNTER_COUNT_EXPECTED = 20`, `gauntlet_sim.py:113`, asserted `:689` + `:1906`).

---

## 3. KNOWN RESIDUE (named so nobody mistakes pre-existing noise for pilot signal)

- **21 pre-existing wave5 integration ERRORs** (T4 Option-F fixtures) — reproduce on HEAD, predate this
  cycle. **KNOWN-UNRELATED** to the pilot.
- **pytest-collection abort on the moved `grouping-layer-vocabulary.md` path** — collab-side sweep lane,
  **non-gating**.

---

## 4. PRECONDITION CITATION

`086fb6c` (rocket catalog 18→20 + dedup) · `b1dec28` (gamora F3-verify + consume + Leg-ii harness +
geared-arm wire) · `96afb63` (rocket downstream count-assert reconcile) · `5cabb6c` (gamora elite_pack
verify STANDS) · **policy entry `ce595a7`** (`pilot_policy` two-arm certification, Matt-approved,
decisions-log:5347).

---

## 5. EXPECTED DELIVERABLE SHAPE (BOTH arms)

Leg-i returns, for **arm S** AND **arm G**:
- **PIPE** — rotation contains escape_lane (F4 conjunction satisfiable); per-family (F1–F4) verdicts emit;
  four-family conjunction reachable.
- **YIELD** — per-cell × per-family verdict map = `season_emit` yield by construction.

Plus the arm-G first-class deliverable: **per-family WR/KPM deltas stripped-vs-geared, per cohort** — band
re-fit input AND the registered REFRAME-VALIDITY input (if arm G compresses the KPM spread materially
toward point-mass, ruling A's KPM-as-measurement claim is re-examined). Never quote "~2.4×" as a
geared/certified property (stripped-provisional). Two geometry-only bands (dense_cell, escape_lane) are
**confirm-or-falsified AT the pilot, not tuned pre-fire.**

---

## C. PRE-FIRE CHECK RESULTS (run NOW — all GREEN)

**Check 1 — arm-G gear threaded** · `grep -n measured_gear_stats src/reincarnated/simulation/t4_sim_cycling.py` → **GREEN** (non-empty):
```
1181:    measured_gear_stats: dict | None = None,
1186:      measured_gear_stats: arm G = certification_gear(cohort, tilt) (the composed 6b + cohort-tilt
1189:        Threads onto run_spatial_fight(measured_gear_stats=...) (already accepted, spatial_engine.py:3351),
1244:        measured_gear_stats=measured_gear_stats,
```

**Check 2 — escape_lane F4 member present** · `grep -c escape_lane src/reincarnated/generation/endgame_encounter_catalog.py` → **GREEN**:
```
11
```

**Check 3 — encounter-count expectation** · `GAUNTLET_ENCOUNTER_COUNT_EXPECTED` → **GREEN** (`= 20`,
`gauntlet_sim.py:113`; asserted `:689` "18→20 pilot precondition (F4+F1 cert rooms)" and `:1906`
parity assert). First-log-lines will read `"N distinct configs | 20 encounters"`.

**Sentinel re-check (§0)** · `_read_pilot_policy_version()` → **GREEN** (`pilot_policy=scripted-rotation-v1`,
IS_PENDING=False).

**All pre-fire checks GREEN. Dispatch presented FIRE-READY.**

---

## 6. FIRE COMMAND (do NOT run until Matt's explicit go)

Leg-i emission-path driver: `gauntlet_lived_channel_repilot_driver.run(...)` fired for both arms at
seed 57000000, cell-grain, post-dedup config set, 20-encounter rotation. arm S = `measured_gear_stats=None`;
arm G = `certification_gear v0` × four cohort tilts. **No parallel regens of the same seed** (Discipline #3):
arm S and arm G run SEQUENTIALLY at seed 57000000.

**Sign-off:** gamora, 2026-07-08. Gate CLOSED (governance-only, §0 — no code change). Pre-fire GREEN.
**STOP — awaiting Matt's explicit fire-go.** Dispatch auto-committed (in-scope); NOT pushed.

---

## Completion record — HALTED LOUD (NO run fired) — 2026-07-08 (SESSION 59)

**Disposition: HALT. Did NOT fire.** Matt's explicit fire-go received; on re-verifying the instrument
immediately before firing, the **arm-G disjunction is UNREACHABLE on the Leg-i cell-grain emission
path** with the code on HEAD (`818509806`). Firing would produce a mis-instrumented run — exactly the
class the dispatch's own stop-rule names ("If anything looks mis-instrumented … HALT LOUD and report
rather than grinding").

### The three pre-fire greps: GREEN — but they do not test what matters
- grep1 `measured_gear_stats` in `t4_sim_cycling.py` → 4 hits (GREEN)
- grep2 `escape_lane` in `endgame_encounter_catalog.py` → 11 (GREEN)
- grep3 `GAUNTLET_ENCOUNTER_COUNT_EXPECTED = 20` → 1 (GREEN); sentinel `scripted-rotation-v1`, IS_PENDING=False (GREEN)

These greps prove the **leaf wire exists** and the **catalog member exists**. They do NOT prove the
gear is **threaded through the emission path**. That is the blind spot that let the instrument read
FIRE-READY while arm G was structurally dead.

### Root-cause finding (mechanism, not symptom)
The geared-arm wire (SESSION-58 beat d) threaded `measured_gear_stats` **only at the leaf**
`_run_spatial_w4g_batch` (`t4_sim_cycling.py:1181` param, `:1244` thread onto `run_spatial_fight`).
The emission path reaches that leaf through two intermediaries that **neither accept nor forward** the
param:
- `w4g1_tier_1_sweep` (`t4_sim_cycling.py:1296`) — no `measured_gear_stats`; its batch call `:1359`
  omits it → defaults `None`.
- `w4g2_tier_2_full_sim` (`t4_sim_cycling.py:1389`) — no `measured_gear_stats`; its batch call `:1434`
  omits it → defaults `None`.
- `w5g1_gauntlet_execution` (`gauntlet_sim.py:1254`) — the emission driver — has **no arm/gear
  selection**; its w4g1 call (`gauntlet_sim.py:1411-1419`) and w4g2 call (`:1455-1461`) pass no gear.
- `certification_gear` / `_build_cohort_combatant_stats` have **ZERO call sites in `gauntlet_sim.py`**
  (grep exit 1). The cohort tilt that arm G is supposed to vary is never computed on this path.

Consequence: both "arms" would run byte-identical stripped (`measured_gear_stats=None` everywhere) →
a fraudulent **zero-delta** arm-G deliverable and a **bogus REFRAME-VALIDITY** read (the spread would
look uncompressed only because arm G literally equals arm S). Worse than not firing.

Why the beat-d smoke looked green: it called `_run_spatial_w4g_batch` **directly** with a hand-composed
gear dict against an ad-hoc 231k-HP boss (AGENT_STATE SESSION-58 beat d: "arm G clears faster … cohort
differentiation confirmed"). That proved the LEAF thread in isolation — it **bypassed the emission
path** (`w5g1→w4g1/w4g2`), so it never exercised the missing plumbing.

The math note `simulation/math/certification-gear-v0-composition-2026-07-08.md` §6 **step 2** is the
un-done half — it explicitly specified: *"gains an optional `arm` … that, for arm G, computes
`certification_gear(cohort)` and passes it as `measured_gear_stats=…`"* — implemented at the leaf,
never plumbed up. This is a HALF-DONE math-note step, not a fresh design gap.

### What is actually needed before Leg-i can fire two arms (hours-scale, math-note-first)
1. `w4g1_tier_1_sweep` + `w4g2_tier_2_full_sim`: add `measured_gear_stats: dict | None = None`, forward
   into their `_run_spatial_w4g_batch` calls (`:1359`, `:1434`).
2. `w5g1_gauntlet_execution`: add arm selection; for arm G, compute `certification_gear(cohort, tilt)`
   per cohort inside the cohort loop (`gauntlet_sim.py:1342`) and thread down; arm S = None (byte-identical).
3. A two-arm cell-grain **Leg-i driver/wrapper** — it does NOT exist. Only `leg_ii_kit_grain_spatial_harness.py`
   (KIT-grain) exists; that harness's own docstring (lines 8-9) says *"Leg-i (a separate driver) is the
   CELL-GRAIN certification arm"* — that separate driver was never written. The wrapper owes: seed-57000000
   post-dedup config-set assembly (cell-grain, one representative kit/cell), the `"N distinct configs |
   20 encounters"` start-banner naming BOTH arms, the sequential arm-S-then-arm-G run (Disc #3, same seed),
   and the PIPE + YIELD + per-cohort S-vs-G delta emit.

None of (1)–(3) were started: Matt authorized a **FIRE**, not a build. Completing the wire is a scope
step beyond the fire-go and gets math-note-first + Gate coverage per the pilot's own discipline.

### Deliverables status (all BLOCKED on the above)
- **PIPE:** not producible — the two-arm emission wrapper doesn't exist; escape_lane IS a catalog member
  (11 hits, F4), so the catalog side of the four-family conjunction is present, but no driver emits the
  per-family verdict conjunction over a config set.
- **YIELD:** not producible — no `season_emit` per-cell × per-family map emitted (that is `w5g1`'s output,
  and w5g1 has no two-arm wrapper / config-set assembly at seed 57000000).
- **Arm-S vs arm-G deltas / REFRAME-VALIDITY falsifier:** not measurable — arm G would equal arm S.
  **Explicitly NOT quoting any "~2.4×" figure** (per dispatch + gandalf §4 quoting discipline).
- **Geometry-only bands (dense_cell, escape_lane):** not confirm/falsified — no emission distribution
  produced. Bands remain geometry-anchored (falsifiers named in their math notes), UNTUNED (correct — the
  dispatch forbids pre-fire tuning; there is simply no run to confirm against).
- **21 wave5 ERRORs:** not reproduced (no run).

### Config count + wall-time
- **Config count: N/A (no run).** Cannot report the near-free post-dedup config count because the
  seed-57000000 config-set assembly is part of the missing Leg-i wrapper.
- **Wall-time: 0 (halted at pre-fire).**

### Commit
NO run artifacts (nothing fired). Committed: this halt record + AGENT_STATE SESSION-59 halt entry
(in-scope autonomous-run bookkeeping). NOT pushed (Matt batches).

**Awaiting Matt:** authorize the completion-build (plumb w4g1/w4g2/w5g1 + write the two-arm cell-grain
Leg-i driver, math-note-first, Gate-covered) → then I re-present FIRE-READY and fire; OR re-scope.

**Sign-off (halt):** gamora, 2026-07-08 SESSION 59.

---

## Completion record — DISPOSITION (A) COMPLETION-BUILD — BUILT + smoke GREEN (NO content run) — 2026-07-08 (SESSION 60)

**Disposition: BUILT.** Matt authorized halt disposition (A) — the completion-build — and ratified the full-run pivot (gandalf `agentic_orchestration/gandalf/notes/2026-07-08-full-run-pivot-four-rulings.md` §4) that absorbs this instrument into the MAIN LINE: the pilot converts to the **standing per-axis certification instrument** (pivot §5.c), not salvage. Math-before-code satisfied: the math note `simulation/math/certification-gear-v0-composition-2026-07-08.md` §6 step 2 IS the build spec (the un-done half). Build only; **NO content-bearing run fired** — the pilot fire is downgraded to an optional instrument smoke with zero content authority (pivot §4). Gate-2 reviews this commit before any content-bearing fire.

### Gap 1 CLOSED — `measured_gear_stats` threaded end-to-end (files + line ranges)
The SESSION-58 beat-d wire threaded gear ONLY at the leaf; the intermediaries + driver dropped it → both arms ran byte-identical stripped (the SESSION-59 root-cause). Now:
- `w4g1_tier_1_sweep` — `t4_sim_cycling.py:1304` (param `measured_gear_stats: dict | None = None`), forwarded into its `_run_spatial_w4g_batch` call at `:1373`.
- `w4g2_tier_2_full_sim` — `t4_sim_cycling.py:1402` (param), forwarded at `:1454`.
- `w5g1_gauntlet_execution` — `gauntlet_sim.py:1260` (new `arm: str = "S"`); per-cohort gear composed ONCE per cohort inside the cohort loop at `:1371-1376` (arm G → `certification_gear(cohort, _build_cohort_combatant_stats(cohort))`; arm S → None); threaded into BOTH the w4g1 call (`:1452`) and the w4g2 call (`:1495`).
- **Byte-identical legacy guarantee:** every default is stripped (arm="S", gear=None). No existing caller changes behavior.

### Gap 2 CLOSED — the Leg-i cell-grain two-arm driver now EXISTS + RUNS
`src/reincarnated/simulation/leg_i_cell_grain_two_arm_driver.py` (new). **POPULATION-AGNOSTIC** per the discipline note — takes a population dict OR a `regen:<seed>` spec; NOT hard-wired to seed-57000000 (the standing-instrument seam: a per-axis caller passes its post-axis population, no code change). Draws ONE representative kit per cell (regenerate-at-emission-n_samples-then-slice-s0 discipline, mirrors the leg_ii harness — NOT fresh rolls). Runs **arm S then arm G at the SAME per-cell seed** (Discipline #3, sequential — no parallel same-seed). Reuses the **UNAMENDED** four-family judge (DERIVED_BARS + `_bar_disposition`). Emits **PIPE** (four-family conjunction reachable per cell, both arms) + **YIELD** (per-cell × per-family pass map, both arms) + **DELTA** (per-family, optionally per-cohort, WR/KPM stripped-vs-geared). #2-FF start-banner names BOTH arms + the operative band set. Machine HALT-LOUD: exit 2 if arm G == arm S everywhere.

### The minimal smoke — INSTRUMENT-VALIDITY (arm G ≠ arm S?) — GREEN
- **Cell-grain driver `--smoke` (2 cells × 2 fights, regen:57000000):** exit 0. **arm G ≠ arm S — max_abs_kpm_delta = 12.941.** Per-family KPM deltas non-zero (F1 +7.72/+12.94, F2 −1.21/−9.21, F4 −1.68/−4.94; F3 = 0.0, success-judged WR=1.0 both arms). PIPE reachable both arms both cells; YIELD map emitted. Report: `src/reincarnated/output/leg_i_cell_grain/leg_i_cell_grain_report.json`.
- **Gap-1 emission-path unit smoke (w4g1/w4g2 direct, open_arena, same seed, Balanced):** arm G ≠ arm S — w4g1 Δ=+4.040, w4g2 Δ=+4.250 KPM. The intermediaries forward the gear.
- Imports clean (no cycle), AST parses, legacy defaults verified stripped.

### New gap found (framed, Disc #12; NOT a blocker to this build)
At n_fights=2 with WR=0 (kits time out / die in the smoke slice), **F2/F4 KPM deltas run NEGATIVE under gear** — a KPM-instrument property at tiny-n partial clears, NOT a content verdict and NOT a plumbing defect (the thread-validity check — arm G ≠ arm S — is what this smoke tests, and it passes). This IS the REFRAME-VALIDITY signal the dispatch flagged (does gear shift/compress the KPM spread?); it must be read at the content-bearing per-axis run (full n_fights, bands re-fit to the declared baseline), NOT here. F4 honesty holds (all d_exit_within_window_frac = 0.0 — no mobility stat on the gear surface).

### Deliverables status
- **PIPE / YIELD / DELTA:** all three emit (instrument shapes proven on the smoke slice). Content authority: NONE (pivot §4).
- **REFRAME-VALIDITY:** the falsifier input is now MEASURABLE (arm G ≠ arm S); its content read is the per-axis run's, not this smoke's.
- **Geometry-only bands (dense_cell, escape_lane):** untouched (no re-fit; bands re-fit per declared baseline, pivot §5.1).

### Commit
See commit hash(es) below. Committed: the two-arm plumbing (`gauntlet_sim.py`, `t4_sim_cycling.py`), the new driver, AGENT_STATE SESSION-60 entry, this completion record. NOT pushed (KR batches).

**Sign-off (build):** gamora, 2026-07-08 SESSION 60. Awaiting jack-ryan Gate-2 → then the content-bearing per-axis pilot fires on the main line (first at the geometry-widened population, bands re-fit to that baseline).

---

## SESSION-CLOSE (knight-rider, 2026-07-11 — Matt-authorized close protocol)

**The Leg-i pilot session is CLOSED.** Matt authorized the close. Nothing this session stewarded remains unexternalized.

- **Why now:** the completion-build (`a63aae2`) + Gate-2 PASS (released via Q13) landed 2026-07-08. The per-axis certification ladder it gated is now **four deep on the main line** — E1 (`bfc94eb`) · C3 (`e1fe99e`) · E2 (`d99635a`, axis CLOSED per Q14) · E3 chain (2026-07-11) — with **E4 PHASE-1 co-signed**.
- **Signal emitted (verbatim, into `canonical/current-to-end-state/current-to-end-state-engine.md` SESSION-DELTA):** *pilot session CLOSED → E4 PHASE-2 unblocked*. gamora's E4 dispatch §0 gate resolves on this exact signal.
- **Closing the session ≠ retiring the instrument.** The two-arm cell-grain driver (`leg_i_cell_grain_two_arm_driver.py`, population-agnostic), the per-axis certification model, and the pilot_policy rider **PERSIST in code + policy**. Every future axis run fires on the standing instrument from a fresh session.
- **Close hygiene executed:** (1) RESTORED the §8-A1 measurement of record (`leg3_pilot_section8a1_band_measurement.json` → committed `dfbea76`, seed 56000000 / n=18 / 0/18 / 2026-07-08) after an E3-window smoke run (seed 55000000 / n=5 / 5/5 / 2026-07-11) overwrote its on-disk path. (2) CLEARED closed-chain residue (`variation_pilot_generation_checkpoint.json` + `simulation/output/pilot/`, both untracked); KEPT the tracked `variation_pilot_measurement_report.json` (record of record). **Hygiene flag (non-blocking, star-lord/gamora next touch):** smoke/test runs must not write to measurement-of-record output paths.

**Sign-off:** knight-rider, 2026-07-11. Session stewardship ends. No content runs, no new work after this record.
