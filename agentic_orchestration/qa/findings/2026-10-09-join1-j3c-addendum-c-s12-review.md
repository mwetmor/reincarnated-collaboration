# Finding — 2026-10-09 — JOIN-1 KP-410 · DESIGN-MODE review of J3c inventory ADDENDUM C (rounding audit, S-12)

**Reviewer:** jack-ryan (DESIGN-MODE, before Matt rules on S-12)
**Severity:** PASS-WITH-NOTES (1 WARN, 5 INFO); the G-A form at `:6890` is **ACCEPTED** with conditions
**Target:** godot `a53e8a8` (Addendum C + `evidence/join1/j3c-hook/rounding-audit/`); RED evidence `4f78b74` (`l01-RED/`). The runtime was read at `f414985`, the oracle at sealed `969fbd8d`.
**Developer:** drax
**Principles applied:** 1, 3, 5

## Checks

**(1) Audit completeness: two float-time families are missing. Both are SAME on inspection.**
- **R8 Resilience windows.** Port `kc2rt_fight.gd:4922–4945` (`r8_t_s = run_tick*_period_s()`, `t < active_until`, `active_until = t + dur`). Oracle `player_kit_residual.py:248/357/359/405` with `t_s = rt*period` (`run.py:3623`). **Same expressions.**
- **MovementPolicy accumulators.** Port `kc2rt_movement.gd:224–295` against oracle `movement.py:421–516`: `+= dt_s`, then `>=` / `-=`, with the stationary-run increment before the check on both sides (`_stationary_advance`). **Same order.**
- No other seconds↔ticks family surfaced. I checked:
  - every `/ ticks_per_s` and `* _period_s()` use in `kc2rt_fight.gd`. The `/tps` uses at `:1771`, `:2075` and `:2727` are report-only; `:2259` and `:2331` are the CONTROL and non-oracle branches;
  - the oracle's 13 `spawn_t_s` sites, which include the 5 `spawn_t_s > t` complements (`:2636/2846/3117/3405/4353`) that the inventory doesn't list. `t = k*period` (`run.py:2289`).
- **INFO-1:** add both families as audit rows, and cite the port code for C5 and C8. In `audit.py` those two rows compute oracle and port with the **same function**, so they are SAME by construction rather than by comparison.

**(2) The SAME verdicts are numerically confirmed.** I re-ran `audit.py` and it reproduces `audit.txt` byte for byte. I spot-checked the port-side transcriptions against the source; all match: B1 `:3479`, B8 `:4162`, B10 `:4698`, C4 `:2859`/`:2923`, C6 `:4581`, and `Kc2RtQuant.half_to_even_ticks` = `max(1, half_even(s*tps))` (`kc2rt_quant.gd:111`).

**(3) The fix reproduces the oracle.**
- At 300, `75·P = 3.9999999999999996` gives oracle 76, while `ceil(4/P) = 75`. The naive ceil fails, as drax says.
- **The mirror loop equals the oracle's first-k law at every integer X from 50 to 1000**, for s ∈ {0, 0.2, 0.333, 1, 2.5, 4, 7, 10}: 0 mismatches.
- The current port law differs from the oracle at s = 4 on **381 of those 951 clocks**. 196 and 200 are lucky exact cases.
- **Conditions:**
  - the mirror's `P` must be S-9a's `0.16*(100.0/X)` bits, asserted in the unit limb;
  - the mirror drops the port's `max(1, …)` floor. That is moot at s = 4; declare it.

**(4) The G-A form at `:6890` is ACCEPTED.** It follows the S-10 precedent: the null line `var want_ambush := half_to_even_ticks(…)` still executes and is then overwritten by the guarded line. That is acceptable **because that expression is pure** (static, no RNG, no counter), and nothing reads `want_ambush` in between. **Conditions:**
- **(a)** Guard on **`board != null and board.rulebook != null`**, the same object the board consults, not on `clock.rulebook`. Otherwise a pack path where the S-9b wiring line is skipped would let the report and the board disagree. That fails loudly (the V11-RELEASE-2 HALT), but it is avoidable.
- **(b)** The hunk audit must check that the G-A block is adjacent to the null line and touches no other line.
- **(c)** PREDICTIONS part 2 adds an S-12 row. S-12 is guarded on rulebook **presence**, not on `world_clock_moved()`, so **it runs under JOIN at 196 too, returning 49 = the null value.** P4b 7/7 then exercises it at the defaults. State that.

**(5) The off-path classifications are sound.** `:6549` (the plant window) lives in `_census` counters only: T-A telemetry, port-only (TA-B-06), not trajectory. INFO-2 is the T-A-at-X note drax gives. `:1586` sits in the non-oracle advance (`run()`), so JOIN takes C8.

**(6) S-12 plausibly explains the whole RED, but this is not yet shown.**
- **For:** G4 is bit-equal on ticks 1–74 and first diverges at 75 in 5/5 salts, which matches the computed port 75 / oracle 76. The unknown `swing_pause.py:51|<seed>` streams (2,361–2,847 draw mismatches) fit bodies entering, and seeding, one tick early.
- **Against:** the tick-75 distance is not a pure one-tick shift (0.33 m apart). That is consistent with a cascade, but it can't be read as one.

**WARN-1 · Run the discriminating control before Matt rules.**
- At 200, A1 agrees (50 = 50) and every other family is SAME. **L01-W@200 at the current J3c tag (S-9, S-10, S-11; no S-12) is therefore predicted ROWSET-GREEN with draws_mm 0.**
  - GREEN isolates the RED at 300 to an X-specific cause, which on the audit can only be A1.
  - RED means a second, non-rounding cause exists, and S-12 is not the whole answer.
- It costs one 25-cell run.
- **Also:** pre-state that after S-12 the L01-P rerun must be 7/7 with draws_mm 0. Any residual HALTs to the conductor; it is not re-fixed in place.
- **Cite:** Disciplines #80 and #87; Principle 1.

**INFO-3 · Use the X ∈ {210, 250} cases as unit vectors.** Add them (53/52, 63/62) to the mirror's unit limb alongside 196/200/300.

**INFO-4 · "max(1, …)" wording.** The conductor's brief writes the port law with `max(1, …)`. It is inside `half_to_even_ticks` (`kc2rt_quant.gd:112`), so the description is right, though the call site doesn't show it.

**INFO-5 · Sealed-line count.** About 12 lines across 5 hunks, M-4 is a new member class instance, and the census is unchanged. That is consistent with what I read at `kc2rt_board.gd:225–233`, `:578–588`, `:748–750` and `kc2rt_fight.gd:6884–6890`.

## Action
- [ ] drax:
  - WARN-1: run L01-W@200 at the current tag first, and state the post-S-12 L01-P prediction with its HALT rule;
  - (4)(a)–(c);
  - INFO-1 (R8 and movement audit rows; port citations for C5/C8);
  - INFO-3.
- [ ] Matt: S-12 as proposed, with `:6890` as G-A guarded on `board.rulebook`, **after** WARN-1's control is GREEN.

## References
- godot:
  - `a53e8a8`: Addendum C; `rounding-audit/audit.py`, `audit.txt`, `g4_tick75_check.txt`
  - `4f78b74`: `l01-RED/RESULTS.md`
  - `kc2_runtime/sim/kc2rt_board.gd` (`:225–233`, `:578–588`, `:748–750`)
  - `kc2rt_fight.gd` (`:2266–2331`, `:2855–2925`, `:3479`, `:4162`, `:4581`, `:4698`, `:4922–4945`, `:6498–6552`, `:6884–6890`)
  - `kc2rt_quant.gd:100–119`, `kc2rt_movement.gd:224–295`
- Sealed `969fbd8d`: `run.py:1244`, `:1515–1540`, `:2289`, the `spawn_t_s` sites, `:3623`; `wave_engine.py:543`, `:624–700`; `player_kit_residual.py:238–438`; `movement.py:421–516`
