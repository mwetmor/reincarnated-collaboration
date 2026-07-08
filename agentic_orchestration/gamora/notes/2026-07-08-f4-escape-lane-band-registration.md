# F4-a completion note — escape_lane cert criterion registered (for jack-ryan Lane-3 ratification + Gate-2)

**Author:** gamora (simulation seam)
**Date:** 2026-07-08
**Chain:** batch-2 autonomous chain, step F4-a. Matt-authorized chain-extension (run-state :1151-1161) — the
  un-done half of the Q11 four-family lane; the R4 blocker I diagnosed READ-ONLY last pass.
**Tag:** `gamora/v-batch2-f4-escape-lane-registration-1`
**Reviewer:** jack-ryan (step F4-b) — Lane-3 ratification of the F4 band criterion + Gate-2 on this wiring,
  enforcing gandalf's anti-rubber-stamp rider. Plus the deferred Lane-3 decisions-log entries.

---

## What to review (and gandalf's binding rider)

Matt's ruling carries gandalf's rider: **VERIFY the inherited F4 values (KPM floor 60 / ceiling 150 /
exit-within-window ≥0.80) against escape_lane's actual spawn arithmetic via the step-5 density-anchored method —
do NOT rubber-stamp.** The crux for Gate-2: **did I density-VERIFY, or did I inherit-and-rubber-stamp?**

My answer: I density-verified. §3-§4 of the math note derive what escape_lane's spawn arithmetic HONESTLY demands
(from the lane length, arrival tempo, supply, window, champion elevation) and cross-check the inherited bars
against that. Verdict: **all three CONFIRMED** — but CONFIRMED via arithmetic, not assumed. The reason they
confirm (and step-5/step-6 did NOT) is stated explicitly and is falsifiable: escape_lane was BUILT to the §3-F4
genre spec (the elevation, the ~180 stream, the 55 m lane, the 60 s window are all §3-F4 parameters), so the
genre-anchored bars and the geometry-anchored demand are consistent BY CONSTRUCTION OF THE ROOM. step-5/step-6
were ADJUST because the ROOM had changed underneath a band fit to an OLD population; here the room and the bars
are the same Q11 generation → CONFIRM. **Both outcomes are legitimate under the rider; I report the arithmetic
truth, which happens to be CONFIRM.**

## Deliverables (all landed, engine seam)

1. **Math note (BEFORE code, Disc #1):** `simulation/math/f4-escape-lane-band-registration-2026-07-08.md`.
   Density-anchored derivation §3; verdict table §4; wiring §5; semantic shift §6; boundary call §7.
2. **Wiring:** `gauntlet_sim.py` — the previously comment-only F4 branch at `_shell_result_passed` is now a real
   branch; 3 module constants added near `_BOSS_SHELL_GATE_TYPES`; `gauntlet_pass` docstring updated (was
   narrating F4's absence).
3. **Smoke (Disc #2):** `simulation/scripts/gamora_f4_escape_lane_registration_smoke_2026_07_08.py` — PASS.
4. **MIGRATION.md:** v1.86 within-seam discharge of the v1.85 "zero emit until Lane-3 registers F4" contract.
5. **Tests:** `tests/test_cycle13_wave5_gauntlet_sim.py` updated to the live contract (52/52 PASS).

## The verification result (the density-anchored verdict — please stress this)

| Bar | Inherited (Lane-3/genre) | Density-anchored demand | Verdict |
|---|---|---|---|
| exit-within-window floor | ≥ 0.80 | viable kit exits ≈0.95-1.0 (55 m lane = 5× travel budget; ×2.0 elevation, fodder <0.5 s); floor 0.80 sits ~0.15-0.20 BELOW with honest headroom | **CONFIRMED** |
| KPM floor | 60 | arrival-tempo sanity rail (~3/s = 180/min raw arrival); <60 ⇒ already walled ⇒ exit already fails (redundant-with-exit) | **CONFIRMED** (secondary sanity) |
| KPM ceiling | 150 | supply ceiling ~192; 150 < 192 (×1.28 headroom) ⇒ reachable overpowered-flag, not inert | **CONFIRMED** |

**Anti-curve-fit cross-check: HONESTLY UNAVAILABLE.** There is NO observed escape_lane exit/KPM distribution on
disk (verified: `grep -rln "exit_within_window_frac\|escape_lane" output/` returns zero four-family metrology
JSON — the F4 branch was dead, so no cert run ever produced one). Per the dispatch I derive from geometry ALONE
and flag the percentile cross-check UNAVAILABLE — I do NOT invent a distribution. The falsifier is named (math
note §4): if the first scored escape_lane run (the R4 sweep) shows a viable-kit exit mode <0.80 or a KPM mode
pinned at 150, this CONFIRM is falsified and the bars revisit.

## Which observable F4 gates on

**exit-within-window ≥0.80 is PRIMARY; KPM ∈[60,150] is SECONDARY sanity.** escape_lane's genre observable is
`escape_reached` (a success/exit metric), exactly as F3 is success-rate-judged, NOT KPM-primary. The wiring
gates on `tier_2_survival_rate >= 0.80` FIRST (primary; returns False below), THEN `KPM in [60,150]` (secondary).

## The load-bearing field-identity (Disc #11 — please verify at source)

I did NOT add a new exit field. The exit-within-window fraction **IS `tier_2_survival_rate`** for an
`escape_reached` room, by an exact win-condition identity:
- `spatial_engine.py:2874-2888`: for escape_lane, `winner == "player"` IFF `self._escape_reached` (die →
  "monster", window-elapsed-without-exit → "timeout").
- `t4_sim_cycling.py:1245`: `player_won = (fr.winner == "player")`.
- `t4_sim_cycling.py:259-262`: `survival_rate = wins / n_fights`.
- ⇒ for escape_lane, `tier_2_survival_rate` = (# escape-reached) / n = the exit fraction. Same quantity the
  metrology driver computes independently as `exit_within_window_frac` (`...driver.py:291-292`, reading
  `escape_reached` off each fight-result).

## The wiring delta (exact)

`gauntlet_sim.py`, new branch in `_shell_result_passed` BETWEEN the boss branch and the clear-shell KPM branch:
```python
if enc_type in _F4_ESCAPE_SHELL_GATE_TYPES:
    exit_frac = getattr(r, "tier_2_survival_rate", None) or 0.0   # = escape-reached fraction
    if exit_frac < _F4_EXIT_WITHIN_WINDOW_FLOOR:
        return False                                             # PRIMARY: exit-within-window
    t2_kpm = getattr(r, "tier_2_kpm", None) or 0.0
    _lo, _hi = _F4_KPM_BAND
    return _lo <= t2_kpm <= _hi                                  # SECONDARY: KPM sanity band
```
plus constants `_F4_ESCAPE_SHELL_GATE_TYPES = frozenset({"escape_lane"})`,
`_F4_EXIT_WITHIN_WINDOW_FLOOR = 0.80`, `_F4_KPM_BAND = (60.0, 150.0)`. Boss branch, clear-shell branch, and the
unbanded fall-through `return False` are byte-identical. escape_lane no longer falls through to the clear-shell
KPM lookup (where it has no band entry → was `return False`); it returns a real verdict here.

**One choice flagged for Gate-2:** the KPM ceiling is here an in-line hard upper (`t2_kpm <= hi` → False above),
matching the pre-existing clear-shell gating convention (`cohort_band[0] <= t2_kpm <= cohort_band[1]`), NOT the
report-only metrology driver's Rider-3 "overpowered = flag not fail" overlay. This is a DELIBERATE consistency
choice: the gating `_shell_result_passed` has always treated above-ceiling clear-shell KPM as out-of-band-False;
the Rider-3 flag-vs-fail doctrine lives in the report-only `_bar_disposition`, not in the gate. F4 follows the
gate convention for symmetry with the clear shells it sits beside. Math note §5 documents this; call it if you
disagree.

## family_certification_pass reachable-True + F1/F2/F3 untouched

- **Reachable-True confirmed:** smoke + `test_f4_registered_certification_reachable_true` prove a cohort passing
  all four families now has `family_certification_pass == True` and `season_emit == True`. The prior universally-
  False-by-F4-dead-code state is lifted. **No manufactured passes:** `test_f4_fails_below_exit_floor` +
  `test_f4_exit_floor_boundary_and_kpm_secondary_band` prove a walled / under-KPM / over-KPM escape_lane still
  fails F4, so a non-viable kit still does not certify.
- **F1/F2/F3 byte-identical:** boss branch (survival validity bit, KPM ignored) untouched; clear-shell branch
  (KPM band) untouched; four-family conjunction structure untouched. Smoke §4 re-proves clear-shell KPM gating
  and boss survival-bit gating are unchanged. T1 6-shell pilot bands (step-5/step-6) untouched.

## Cross-seam MIGRATION: NOT needed (within-seam discharge)

No new star-lord schema. The wiring reuses `tier_2_survival_rate` + `tier_2_kpm` — fields already on
`GauntletEncounterResult` and already serialized. `season_emit` stays a bool (only its truth-condition becomes
reachable-True); rocket's `season_generation_pipeline.py:1681-1816` reads that bool unchanged (its output set can
now be non-empty; no break). star-lord's F4 telemetry consume (schema v2.20, `7d999db`) is unchanged. MIGRATION
v1.86 is a WITHIN-SEAM behavior-discharge record (same class as step-5/step-6), NOT a new ADR-004 cross-seam
schema MIGRATION.

## Regression

- Smoke `gamora_f4_escape_lane_registration_smoke_2026_07_08.py`: PASS.
- `test_cycle13_wave5_gauntlet_sim.py`: 52/52 PASS (retired `test_f4_band_unregistered_blocks_certification_
  pending_lane3` — it asserted the dead-code state; replaced by 3 live-gate tests; helper docstring updated).
- Broad gauntlet+spatial+wave5+cycle13 slice: **887 passed / 1 pre-existing fail** — the failing test is
  `test_wave5_swift_closure_path_x_phase4_feeds_phase5.py::...test_run_phase5_cohesion_judge_accepts_path_x_pm1_
  result_in_smoke` (LLM/P5 seam). **Verified pre-existing this session:** it fails IDENTICALLY with my
  `gauntlet_sim.py` change git-stashed (Disc #11) — not this seam, matches the MIGRATION v1.85 baseline. Plus 4
  pre-existing rocket grouping-vocab-path collection errors (also v1.85 baseline). `gauntlet_sim.py` py_compile OK.

## Deferred Lane-3 decisions-log entries for you (F4-b, run-state :357/:1161)

Per the KR sequence, F4-b also lands the deferred Lane-3 decisions-log entries: R4 cert-contract shift +
open_arena re-base + mobs_killed range + **the F4 registration** (this note's semantic shift: F4 flips from
dead-code-False to a live exit≥0.80 + KPM[60,150] gate; `family_certification_pass`/`season_emit` reachable-
True). jack-ryan owns the log write.

## Out of scope (guard state)

NO F1/F2/F3 change; NO T1-pilot band change; NO boss/mini_boss touch; NO content/kit re-tune; NO season-emission
run (post-R5, Matt touchpoint per R6); NO R4 cert sweep (KR's next step after your Gate-2); NO boss_with_adds /
magic_pack content fix (parallel lane); NO star-lord schema change.

---

**Signed:** gamora, 2026-07-08. F4 escape_lane registered: exit≥0.80 PRIMARY + KPM[60,150] SECONDARY, all three
bars density-CONFIRMED (not rubber-stamped), cross-check honestly UNAVAILABLE. family_certification_pass +
season_emit reachable-True; F1/F2/F3/T1-pilot byte-identical; within-seam (no new star-lord schema). Ready for
your Lane-3 ratification + Gate-2.
