# CORRIGENDUM: v3.9 pass 2 · `V39-NOHUNT` salt 18 is a TICK-CAP STALL, not a survival

**gamora, 2026-10-02.** Raised by the OBS-1 retro-audit (jack-ryan J0/J1 Gate-2, collab `29124a46e` § 4.2). The finding went to Matt as a HALT, and he ruled **"Correct and continue"** (KC2 ledger KP-237). This note corrects the record. **No committed file in this folder was changed;** the corrections are stated here.

## What is wrong
In `pw_C.json` → `results.V39-NOHUNT` (salts 0–19), **salt 18 banked 2 rows (w151, w152), not 10.** Its ladder stopped when **w152 ended `timeout` at the tick cap** (4000 ticks = 326.53 s). The composition stops a ladder by design on a non-clearing, non-death wave. The summary layer reported the salt with `raised` = {} and a leg-A terminal of `None`, so it was **counted as a survivor** (`n_survive_160` = 1). Its per-salt ratio, 0.3935, is computed over those two rows.

## Evidence
1. **From the committed summary.** For waves 151–159, Σ mean_t_s × 20 exceeds `t_s_151_159` by **290.29 s**. Rounding allows at most 0.91 s, and a missing row on wave *w* pushes mean_t_s[w] × N above that wave's total. Salt 18 is the only salt with no death in any wave (`leg_b_death_waves[18]` = []), and its ratio is 0.39, against 1.48–2.36 for the others.
2. **Re-run witness** (`corrigendum_witness_v39_nohunt_s18.py` → `corrigendum_witness_v39_nohunt_s18.json`). This is read-only. It runs `V9.run_one("V39-NOHUNT", (18,))` through the **unmodified** v3.9 oracle, engine `f4a9948e`, with an innermost observer that records each wave's raw outcome. It **reproduces the committed per-salt ratio 0.3935, terminal `None`, 2 rows.**
   - **w151:** cleared, 37.06 s.
   - **w152:** `timeout` at 326.53 s.
   - **The one surviving body that gates the clear:** `thornedhorrorfrost_b01` (res_physical 0, so killable). It is ring-halted, was never contacted and took **0 player hits**.
   - **Also alive:** three physically-immune `trap_lightningspike_hero_a01` hazard pets (res_physical 500, res_bleeding 0), with 0 hits.
   - The same shape as J0 A-SECOND's stall, a ring-halted killable body the pilot never reaches. **Here the pilot is the no-hunt pilot** (V39-NOHUNT), not P-MOVE.

## Which grades rest on it (`prereg_grading.json`), not to be quoted
- **Q7** (V39-NOHUNT ratio ×1.798, graded HIT). The pooled ratio includes the truncated salt. **Not to be quoted.**
- **Q8** (w152 first death 18/20, graded deaths HIT; w152 mean duration 51.8 s, graded MISS). The `"None": 1` is the stall, read as a survival. The 51.8 s mean includes the 326.53 s timeout. **Not to be quoted.**
- **Also touched, on their V39-NOHUNT side.** **Q13** (the 1.287× occupancy ratio has V39-NOHUNT's disc occupancy as its denominator), **Q14** (V39-NOHUNT standing fraction, 0.584), **Q15** (V39-NOHUNT closing speed, 0.002 m/s) and **Q16** (V39-NOHUNT disc-empty fraction, 0.650) all pool instruments over the cell, including the 326.5 s stalled wave. Their **V39-NOHUNT values are not to be quoted**. The V39-FULL values in those rows are unaffected: V39-FULL passes the summary check.

## What is not affected
- Every other configuration in this folder (`pw_A`, `pw_B`, the other `pw_C` configs, `graded_V39-FULL.json`) passes the summary-form completeness check.
- **V39-NOHUNT `salts_0_4`** (×1.8178) does not contain salt 18.
- The oracle of record is v3.11 (`V311-FULL`). The retro-audit re-ran it with the same observer and found **all 20 pw salts and all five graded arms complete**; every survivor is a genuine w160 clear.
