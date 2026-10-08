# JOIN-1 · J3 · P-J2-5 calibration, step 1 (ADDENDUM-E1 A-8; Matt KP-356; conductor KP-357)

gamora, 2026-10-08.

**Prereg:** engine `d33da377`, committed ALONE before any run.
**Instrument:** `src/reincarnated/simulation/scripts/gamora_join1_pj25_calib_2026_10_08.py`.
**Pin fix:** `9cc189b7`.

## Question

Does the OA/DA table's own decomposition reproduce the DA of the **74 measured** offense-path pairs?

**The law is the one Lap O's emitter applied** (`research/scripts/pm4o_lib_2026_08_14.py:263`):

`DA = (flat + L·12 + attr·0.5)·(1 + mod/100) + 53`

The decomposition is rebuilt from the table's own columns:
- `flat` is the sum of `da_flat_bio`, `da_flat_own_skills`, `da_flat_wave_surv` and `da_flat_ultimate_pak`;
- `L` is `spawn_level`;
- `attr·0.5` is `da_attr_term`;
- `mod` is `da_mod_pct_total`.

**Tolerance, pre-registered:** `B_row`, the 4-dp rounding bound on DA, on 3 additive inputs, and on `mod`.

## Result: THE DECOMPOSITION HOLDS (`calib_step1.json`)

| | n | within `B_row` | bit-exact | max \|Δ\| | max \|Δ\| / `B_row` |
|---|---|---|---|---|---|
| **P-CAL-1**: the 74 measured path pairs | 74 | **74** | 42 | **4.5e-13** | 3.7e-10 |
| **P-CAL-2**: all 95 table rows | 95 | **95** | 58 | 4.5e-13 | 3.7e-10 |

**What the result shows:**
- The rows that are not bit-exact differ by float evaluation order only (≤ 4.5e-13).
- The rounded inputs leave no visible error, because they were already stored at 4 dp before DA was computed from them.
- **The law and the table's columns are complete and consistent. No hidden term remains.**

## The first run (kept): an integrity-pin defect in my prereg, not in the data

- **What failed.** Run 1 at `d33da377` (`calib_step1.run1-d33da377-pin-defect.json`) failed **only** its table-integrity check.
- **Why.** I copied the prefix `5c559980` from `measured_board.py:498`'s provenance **prose**, which mis-states the sealed code's own full pin `5c55998d…c564` at `measured_board.py:54`.
- **The file is fine.** It is the sealed, clean, committed one (sha `5c55998d0127ed77…c564`), and its numbers are identical in both runs.
- **The fix.** `9cc189b7` pins the code's full sha. Predictions are unchanged.
- **A new finding:** the sealed prose at `:498` has a typo. That is informational; the oracle is frozen, so it is not edited.

## What this does NOT show (the input to step 2)

- A pass says the **law and its decomposition** reproduce the measured DA. It says nothing about whether the **component sources** (bio values, own skills, wave survival arrays, ultimate PAK, level basis) are available, or correct, for the **112 records the table never measured**.
- Those records include bosses, bounties and summons.
- Step 2 must re-derive their components from those sources (the Lap O library: `bio_of`, `skill_stat_sum`, `survival_arrays`, `difficulty_pak`) under its own prereg, and print each record's level basis.
- **Not started:** the conductor confirms first.
