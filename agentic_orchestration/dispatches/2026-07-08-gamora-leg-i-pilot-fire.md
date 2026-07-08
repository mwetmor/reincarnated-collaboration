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
