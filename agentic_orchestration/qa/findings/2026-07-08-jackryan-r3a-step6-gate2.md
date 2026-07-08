# Finding — 2026-07-08 — r3a-step6-cert-repoint-magicpack-audit

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: **PASS-WITH-FOLLOWUP**)
**Target:** tag `gamora/v-r3a-step6-cert-repoint-magicpack-audit-1` (commit `b30c4ae`)
**Developer:** gamora (simulation seam)
**Mode:** DEV-MODE (Gate-2, BLOCK authority per ADR-004)
**Principles applied:** Review Principle 1 (math-before-code), 2 (smoke-gate), 4 (decisions-log/criterion as truth), 5 (severity matters); Disciplines #1, #11, #12, #13, rider-4 (anti-Goodhart); ADR-004 (within-seam, no MIGRATION)
**Discharges:** DESIGN-MODE CONDITION 1 (magic_pack band audit) + CONDITION 2 (boss no-touch) from `qa/findings/2026-07-08-jackryan-s4-reframe-review.md`.

## Verdict
**PASS-WITH-FOLLOWUP.** All five verification points hold under independent source-level check. The diff is exactly one tuple + a provenance comment; part (a) is genuinely zero-code; boss semantics are untouched; the trimodal content finding is real and correctly left as a FLAG, not curve-fit away. The single follow-up (thin ceiling margin) is a revisit-if-it-rails watch, not a block. **step-4-bis is CLEARED to fire.**

## What I found (5 points, independently verified — not taken on trust)

**1. Part (a) WR-gradient = genuinely ZERO code.** VERIFIED. `_shell_result_passed` (`gauntlet_sim.py:826-862`) splits exactly two ways: boss shells → `survive_kill_rate >= floor` (:830); clear shells → `cohort_band[0] <= t2_kpm <= cohort_band[1]` (:862). A pure range check, no WR term. Grep of the seam for `gradient`/`mid_mass`/`mid-mass` in any `.py` gating path returns ZERO real hits — every `gradient` occurrence is either a comment, an unrelated eHP term (`combatant.py:753/761`), or a search-gradient term (`reduced_spatial_substrate.py:31`). The §4 WR-gradient was only ever an overlay in gandalf's note. Aligning the criterion to existing code IS the correct outcome, not a missed requirement.

**2. magic_pack re-band + CONDITION 1 + anti-curve-fit.** VERIFIED. Math-note precedes code (Discipline #1) — `math/r3a-step6-magicpack-band-audit-2026-07-08.md` §0-§4 authored before the `:462` tuple change; same density-anchored method as step-5 (`KPM = mob_count·60/clear_s`), not a new ad-hoc one. I re-ran her distribution against the cited source data (`src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260708_134518.json`, n=189): min=8.7, max=144.0, **p90≈101.5**. Geometry ceiling **102.86 lands ~1.4 KPM ABOVE p90 (101.48)** — honest-anchor signature confirmed, not curve-fit-on-p90. The stale 100.0 sat on/below p90 (4-mob-era residue) — confirmed. The anti-curve-fit claim holds.

**3. CONDITION 2 — boss shells untouched.** VERIFIED. Diff touches only the `magic_pack` clear-shell tuple; `_BOSS_SHELL_GATE_TYPES`, `SURVIVAL_FLOOR_BY_COHORT`, and the boss branch are byte-identical. I ran the smoke myself: `boss_with_adds` with KPM=999 / survival<floor → **FAILS**; survival>=floor / KPM=0 → PASSES. KPM is provably ignored on boss shells. No KPM-primacy leaked onto boss rooms.

**4. Trimodal content finding correctly FLAGGED, not curve-fit.** VERIFIED + endorsed. Source data confirms LOW<12.52 = **117**, in-band = **54**, above = **18** — matching the note's 117/54/18 exactly. The 117 timeout non-clears reject below-floor under BOTH 18.61 and 12.52 (they cluster at 8.7–11), so the floor re-derivation is density-honest WITHOUT admitting them. This is the correct call: the re-band does NOT curve-fit the floor down to green the timeouts. Analogous to the boss_with_adds non-viability finding, this is a legitimate below-floor content finding that stays flagged (via `tier_1_reject_breakout.reject_below_floor`) for the parallel content lane. Do NOT let step-4-bis silently absorb it.

**5. Smoke + regression.** VERIFIED by re-running, not by reading her claim. Smoke script (`scripts/gamora_r3a_step6_..._smoke_2026_07_08.py`) exercises the changed path — line 69 asserts the newly-admitted 102 tail passes (rejected under old 100.0), lines 75-78 assert boss KPM=999 fails. Smoke **PASS**. Regression `test_cycle13_wave5_gauntlet_sim.py` + `test_spatial_gauntlet_scenarios.py` = **77 passed** (ran from canonical `tests/`; note a stray `.claude/worktrees/…` copy causes a conftest collision if globbed — cosmetic, not a defect in this work).

## Rationale
Part (a) satisfies Review Principle 4: the code IS the truth, and the criterion now matches it. Part (b) satisfies Discipline #1 (math-first), #13 (inherited-uncalibrated drift correctly diagnosed), and rider-4 (geometry primary, percentile cross-check, ceiling lands above p90). CONDITION 2 satisfies the DESIGN-MODE no-touch guard. Within-seam per ADR-004 — NO MIGRATION correctly called (one clear-shell constant, no star-lord-consumed interface changed).

## Follow-up (non-blocking — does NOT gate the chain)
- **Thin ceiling margin (~1.4 KPM above p90).** gamora self-flagged this as a coarse brisk-sweep estimate on a shallow-clustered room, thinner than step-5 choke's funnel-throughput derivation. It is NOT a Gate-2 blocker because (a) the anti-curve-fit test passes, and (b) the floor — not the ceiling — governs the load-bearing 117 rejects, which are floor-insensitive. **Watch:** if magic_pack later rails at the 102.86 ceiling (all fast-clears pinned at hi), revisit with a finer per-bite AOE-throughput model. Same class as my step-5 INFO note on the 24s choke ceiling.

## Note (INFO, not a defect)
The frozen-data `tier_1_reject_breakout` re-aggregates to `{entered:36, above:18, below:135}` because it buckets `entered_tier2` from the OLD PROVISIONAL_PASS routing decisions; the true 54-in-band only materializes on a re-run where `_route_tier_1` re-decides. gamora surfaced this correctly (Disc #11). The 54/117/18 pure-KPM projection is the honest read; step-4-bis (if re-run) realizes the 54. I confirmed 54/117/18 directly from source data, so the projection is sound.

## Action
- [x] gamora: CONDITION 1 (magic_pack density-anchored re-derivation) — DISCHARGED and verified.
- [x] gamora: CONDITION 2 (boss no-touch) — CONFIRMED.
- [ ] gamora/gandalf: carry the magic_pack LOW-mode 117-timeout non-viability as a FLAGGED content finding into the R4 content lane (parallel to boss_with_adds); it must not silently emission-gate.
- [ ] gamora (deferred watch): if magic_pack rails at the 102.86 ceiling on a future run, tighten the fast-sweep estimate.
- [ ] knight-rider: step-4-bis is CLEARED to fire.
- [ ] Matt: no decision needed — PASS-WITH-FOLLOWUP, not a BLOCK.

## References
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — :462 (magic_pack tuple), :826-862 (`_shell_result_passed`: boss survival bit :830, clear KPM band :862)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/r3a-step6-magicpack-band-audit-2026-07-08.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_r3a_step6_magicpack_cert_repoint_smoke_2026_07_08.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260708_134518.json` (source data; n=189, p90≈101.5, LOW/MID/HIGH = 117/54/18 confirmed)
- `agentic_orchestration/gamora/notes/2026-07-08-r3a-step6-cert-repoint-magicpack-audit.md`
- `agentic_orchestration/qa/findings/2026-07-08-jackryan-s4-reframe-review.md` (DESIGN-MODE conditions discharged)
