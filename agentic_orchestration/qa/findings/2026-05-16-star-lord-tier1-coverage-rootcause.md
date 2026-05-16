# Findings — Tier-1 Telemetry Coverage Root Cause
**Date:** 2026-05-16  
**Author:** star-lord  
**Dispatch:** `2026-05-16-star-lord-tier1-coverage-investigation.md`  
**Season analyzed:** `season_001005`

---

## Executive summary

The 3.4% Tier-1 column coverage in `season_001005` is **not a code bug**. It is the combined result of two data-timing factors: pre-migration rows that predate the V2.0 schema (expected, unfixable without regen) and a partial regen that covered 10 of 11 classes. The code path in `fight_engine.py`, `balance_loop.py`, and `recorder.py` correctly writes Tier-1 fields for every row it produces. Drax's leading hypothesis ("the fight sim apparently still doesn't write them") is **incorrect**.

---

## Step 1 — Empirical reproduction

Query results on `data/telemetry.db`, `season_001005`:

| Metric | Value |
|---|---|
| Total fight rows | 1,541,700 |
| `duration_seconds` non-null | 52,800 (3.42%) |
| `a_heals_received` non-null | 52,800 (3.42%) |
| `a_potions_used` non-null | 52,800 (3.42%) |
| class×monster pairs with any Tier-1 | 120 / 230 |

Drax's numbers confirmed. The 52,800 rows are identical across all three columns (same rows).

---

## Step 2 — Temporal analysis: the critical signal

The 52,800 Tier-1 rows form a **contiguous block by row ID**:

- Tier-1 block: IDs 1,955,781 – 2,008,580 (the most recent write in the entire DB)
- Pre-Tier-1 block: IDs 1 – 1,955,780 (all NULL for Tier-1 columns)
- No rows exist after ID 2,008,580 (Tier-1 block is the most recent write)

The 52,800 rows cover iterations 0–6 (seven iterations), uniformly 528 rows per fight_index (100 fight indices × 528 class×monster×iteration combos). All rows in this block have Tier-1 data populated — the code works correctly for every row it generates post-migration.

---

## Root cause #1 — Pre-migration data (explains 96.6% null)

The V2.0 schema migration (star-lord, `baa3bed`, 2026-05-16) added three columns:
- `duration_seconds REAL`
- `a_heals_received REAL`
- `a_potions_used INTEGER`

The 1,488,900 rows written **before** this migration have `NULL` in all three columns. SQLite column additions default to NULL for existing rows (no backfill). This is expected and correct.

**These rows cannot be backfilled.** `duration_seconds`, `a_heals_received`, and `a_potions_used` are fight-runtime values produced by the fight simulator. They cannot be recomputed from the stored `loadout_json` or any other persisted field.

---

## Root cause #2 — Partial post-migration regen (explains class_0011 gap)

The 52,800 post-migration rows came from the **B10.4 Option 2 full regen** (gamora, commit `540160c`, 2026-05-16). That regen generated **10 classes** (not 11) for seed 1005.

Evidence:
- Tier-1 block contains classes `class_0001` through `class_0010` — exactly 10 classes
- `class_0011` has **zero rows** in the Tier-1 block (max ID = 1,796,300, well before block start)
- The B10.4 regen commit message says "10/10 classes converged" — consistent with a 10-class run

**Why 10 instead of 11?** `CLASS_COUNT_RANGE = (10, 12)` in `season_orchestrator.py` (line 51). The count is drawn by `rng.integers(*CLASS_COUNT_RANGE)`, which for numpy is exclusive of the upper bound, sampling from {10, 11}. The B10.4 regen's RNG state (which may have shifted relative to the original run due to code changes altering RNG consumption) drew 10 for seed 1005. The original season had drawn 11.

`class_0011` is an experimental archetype (fire, close-range, mana, `final_modifier=0.0723`, `would_pass_clamp=false`). It was never part of the B10.4 regen — not excluded by a filter, but simply not generated in that run.

---

## Step 3 — Code path inventory (recorder + fight_log)

### `balance_loop.py` — fight_log population

The `balance_class()` method populates `fight_log` entries in **two code paths**:

**Path A: Primary convergence loop (lines 462–484)**
```python
fight_log.append({
    ...
    "duration_seconds": fight.duration_seconds,      # present
    "a_heals_received": fight.a_heals_received,      # present
    "a_potions_used": fight.a_potions_used,          # present
})
```

**Path B: Rejection gate re-run (lines 537–559)**
```python
fight_log.append({
    ...
    "duration_seconds": fight.duration_seconds,      # present
    "a_heals_received": fight.a_heals_received,      # present
    "a_potions_used": fight.a_potions_used,          # present
})
```

Both paths include all three Tier-1 fields. No code path omits them.

### `recorder.py` — `record_class_fight_loadouts()` (lines 410–463)

```python
rows.append((
    ...
    entry.get("duration_seconds"),    # line 447
    entry.get("a_heals_received"),    # line 448
    entry.get("a_potions_used"),      # line 449
))
```

INSERT at lines 452–460 correctly includes all three fields. No recorder bug.

### `season_orchestrator.py` — class loop (lines 333–358)

Both experimental (`_balance_experimental_with_retry`) and non-experimental (`balance_class`) paths call `recorder.record_class_fight_loadouts(season_id, player_class.id, result.fight_log)`. No class type is skipped at the recording level.

---

## Step 4 — Reconciliation with drax's framing

**Drax said:** "those 52,800 rows correspond to the first 6 balance loop iterations only"  
**Corrected:** The 52,800 rows span **iterations 0 through 6 (7 iterations)**. The B10.4 regen for all 10 classes converged at or before iteration 6, so no class produced rows at iterations 7–9. There is no code-level cutoff at iteration 6.

**Drax said:** "The fight sim apparently still doesn't write them"  
**Corrected:** The fight sim correctly writes Tier-1 fields for every fight it runs post-migration. The null values for 96.6% of rows are from pre-migration data, not a write failure.

**Drax said:** "120 / 242 class×monster pairs have any Tier-1 data"  
**My query:** 120 / 230 class×monster pairs. The discrepancy (242 vs 230) is a query-framing difference or drax was counting from a different filter.

---

## Mitigation path

### Option (a) — Authorize a fresh full regen [recommended]

A fresh full season regen for seed 1005 (authorized by Matt per ADR-006 LLM batch policy) will produce complete Tier-1 coverage. The new rows will cover all classes, all iterations, and all fight indices. Old pre-migration rows remain in the DB (no deletion needed — they're still valid for win-rate analysis).

**Note for the regen script:** Pass `n_classes=11` explicitly (or whatever count the original season used) to ensure the regenerated season includes class_0011's slot. Relying on `CLASS_COUNT_RANGE` RNG may produce 10 classes again if the RNG state shifts.

### Option (b) — Backfill [rejected]

Not possible. Tier-1 fields are fight-runtime measurements. They cannot be recomputed from `loadout_json` or any stored field.

### Option (c) — NOT NULL constraints [deferred]

Adding `NOT NULL DEFAULT 0.0` constraints to Tier-1 columns would prevent future null writes, but (a) can't fix historical data, and (b) would be a schema-breaking migration. NOT NULL is semantically wrong for pre-migration rows anyway (null = "data not available," 0.0 = "zero heals received"). Keep columns nullable.

---

## Code changes needed

**None.** The code is correct. This is a data-timing issue, not a code defect.

---

## Impact on drax's encounter analytics

Drax's v0.7 viz correctly pivoted to `Damage × Win Rate` as a fallback. Once a full regen runs:
1. Tier-1 columns will be populated for all class×monster pairs
2. Drax should author a follow-on dispatch to switch the encounter_analytics projection back to the intended `Damage × Time-to-Kill` form
3. Until then, the fallback viz is functionally correct

---

## Open items surfaced

1. **class_0011 data gap is permanent** for the pre-migration era. Post-regen it will be covered.
2. **CLASS_COUNT_RANGE RNG variance** can cause regen class counts to differ from original generation. Consider passing `n_classes` explicitly for validation regens to match the original season's class count.
3. **Drax encounter analytics** is blocked on Tier-1 data completeness → gated behind next authorized regen.
