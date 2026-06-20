# Dispatch — 2026-06-19 — jack-ryan — Gate-2: STR 9-pass-floor all-18 clear-room harness

**From:** knight-rider
**To:** jack-ryan (QA gatekeeper, DEV-MODE / Gate-2)
**Approved by:** Matt 2026-06-19 ("agreed, route it" — gandalf routing handoff). gandalf brief §6 names jack-ryan Gate-2 as the BINDING gate before he consumes the result.
**Estimated effort:** multi-hour (reproduce-on-disk per your standing discipline — V1–V6 harness correctness, two-lens pass-tally reproduction, no-gate-regression confirmation).
**Acceptance:** a Gate-2 finding at `agentic_orchestration/qa/findings/2026-06-19-gamora-str-9pass-floor-all18-harness-gate2.md` with a clear verdict (PASS / PASS-WITH-INFO / WARN / BLOCK). The headline gandalf consumes (STR clear-room pass count of 14, per cohort + per clear-type) must be reproduced first-hand before it is blessed as data.

**STATUS: HELD until gamora delivers.** Do NOT execute this Gate-2 until gamora's harness extension + output land (the gamora dispatch `2026-06-19-gamora-str-9pass-floor-all18-clearroom-harness.md` completes with a completion record). KR will confirm when this dispatch is active. If you pick this up at session-start and gamora's output artifact does not yet exist on disk, this dispatch is NOT yet active — do not self-author or stub the review.

---

## Context (why this Gate-2 exists)

gandalf is settling STR's combat-efficacy disposition: ship STR as a clear-room specialist, or flag a kit fix as load-bearing. The decision hinges on ONE empirical read — **does STR pass ≥ 9 of the 14 clear-room shells?** gamora is extending the (your-Gate-2-blessed) `clean_boss_numbers_harness_2026_06_19.py` from 2 boss shells to all 18 reference-gauntlet shells, tier_1-bypassed, so STR's clear-room KPM is MEASURED, never defaulted to 0.0. gandalf consumes the result against a pre-registered disposition table — but ONLY after your Gate-2 PASS (brief §5 endorse-criterion 2 + §6 hand-back; you blessed the numbers on the two prior runs of this exact workstream, and gandalf binds on that pattern).

You have already Gate-2-PASSED the two precursors (carry the anchors forward, do not re-derive):
- Clean boss-numbers harness (commit `2f9c5c8`, your finding `2026-06-19-gamora-clean-boss-numbers-harness-gate2.md`): V1 verified at source + 1,056-cell invariant; you corrected the gate citation to `gauntlet_sim.py:1019`.
- DPS instrumentation (engine `26a6f27`, your finding `2026-06-19-gamora-dps-instrumentation-gate2.md`): V1–V5 + no-gate-regression; INFO-1 = the `spatial_gauntlet/` subdir path note.

## What to verify (the harness-correctness gates — V1–V6, reproduce first-hand)

Per your standing discipline (Review Principle #6 — reproduce on disk, do NOT take gamora's report on trust; the Gate-1 lesson on this exact workstream), confirm each:

- **V1 (tier_2 actually ran on all 18) — LOAD-BEARING. THE TRAP GENERALIZED.** This is THE one. Confirm the harness drove `w4g2_tier_2_full_sim` on EVERY one of the 18 shells × 4 cohorts × population, with **NO defaulted-0.0 KPM masquerading as a measured miss.** The production path short-circuits tier_2 at `gauntlet_sim.py:1019` (`if t1_routing == TIER_1_REJECT:` → `continue` at `:1029`, skipping the tier_2 call at `:1032`) — a clear shell that tier_1-rejects would default `tier_2_kpm` to 0.0 and fabricate "STR fails all clears." Confirm the harness bypasses this (calls tier_2 directly, never the caller `continue`) and that **every cell's `observed_kpm` came from an executed batch** (e.g., `batch.n_fights == expected_n` per cell; no `n_fights == 0` / unset-KPM cells). Recompute this invariant independently across all cells from the raw cell array (mirror the 1,056-cell recompute you did on the boss harness — now across the wider 18-shell run). If any clear-shell cell carries a 0.0 that did NOT come from an executed batch → that is a BLOCK (the table is built on a false signal).
- **V2 (faithful power):** max-profile investment (flip #3 default ON, decisions-log 2026-06-18). Confirm the harness drives the default chain without overriding `apply_max_profile_investment` (you confirmed this holds by construction on the boss harness — re-confirm for the widened run).
- **V3 (proxy-inclusive KPM):** `observed_kpm` = `mobs_killed`/min, `mobs_killed = sum(1 for m in self.mobs if not m.is_alive)` (`spatial_gauntlet/spatial_engine.py:1740`) — attribution-agnostic by construction.
- **V4 (clear-shell win condition) — LOAD-BEARING for the 14 clear shells.** The 14 clear encounters resolve on `all_mobs_killed` (pack clear) and KPM = `mobs_killed`/min — NOT a boss shell mislabeled. Confirm the clear shells' win condition and that the clear-shell integrity check (`Σ termination_counts == n_fights`) holds. Confirm the boss-shell V1 self-consistency (`b_dead == wins == winner_player`) is RETAINED + scoped to the 4 boss shells (it does not over-apply to clear shells).
- **V5 (single regime):** current spatial sim only, current mobs/min, faithful power. NO old-scale KPM mixed in (the phase3 regime-mix failure: old-scale rows + current metadata, ~8× `in_band` disagreement). Confirm the regime fingerprint in the output metadata.
- **V6 (measurement-only / NO PRODUCTION GATE REGRESSION) — the cross-seam gate.** Confirm the tier_1-bypass is measurement-only: NO edits to `gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, the tier_1 routing, `gauntlet_pass`/`eligible_encounters_passed`, or any persisted telemetry schema. The harness must write ONLY its own diagnostic JSON/TXT. Confirm via git status that the production gate files are untouched (mirror your boss-harness check: the bypass is achieved by calling the standalone tier_2 directly, never executing the caller-gate `continue`). This is the binding cross-seam-safety confirmation (Principle #3).

## Also confirm (the consumed-number integrity)

- **The band-fit classification is correct.** gamora looks up `ENCOUNTER_COHORT_KPM_BAND[shell][cohort]` (`gauntlet_sim.py:316-322`) and classifies each cell below-floor / in-band / above-ceiling. Confirm the in-band predicate matches the LIVE production gate's range-check semantics (the `_route_tier_1` direct-range-check inclusivity at `gauntlet_sim.py`) — a band-fit lens that uses different boundary inclusivity than the live gate would mis-count STR's pass total. Spot-check a few cells' classification against the raw `observed_kpm` and the band by hand.
- **The headline reproduces.** Independently re-aggregate STR's clear-room pass count of 14 (per cohort + per clear-type — open_arena / chokepoint_corridor / magic_pack / elite_pack) from the raw cells, and the in-band / below-floor / above-ceiling split. It must match gamora's `aggregations` block. This is the single fact gandalf rules on; it must be reproduced, not trusted.
- **The two-lens `eligible_encounters_passed` is correct** per cohort (current-code 18-wide KPM-band vs doctrine 14-clear KPM-band + 4-boss survive+kill). Confirm both lenses compute as defined.
- **The free boss-shell re-run reconfirms STR's 4 auto-fails** (survive+kill 0.000, timeout-dominant). If STR suddenly survives+kills a boss, the harness drifted regime → that is a quarantine-the-run signal (flag it; do not bless).
- **The dex/int/wis CONTROLS clear competently.** If a known-competent control craters on clears, the harness is suspect, not STR (consistency rail).
- **n per cell ≥ boss-harness cell sizes** (brief endorse-criterion 5; the boss run drove all 4 cohorts unconditionally at n_fights=20).
- **Math-note discipline (#1):** V1–V6 confirmed-from-code with line citations BEFORE the table is read as data. Confirm gamora fixed the prior INFO-1 (cite `spatial_gauntlet/` subdir paths, not bare `simulation/`).

## Severity guidance (Review Principle #5)

- **BLOCK:** V1 fails (a clear-shell cell carries a defaulted-0.0 KPM that did not come from an executed batch — the table is a false signal); OR V6 fails (production gate modified — a measurement-only run touching the live ship gate); OR the boss re-run shows STR survive+killing bosses (regime drift, quarantine).
- **WARN:** a verify-gate is confirmable but the harness has a correctness wrinkle that affects a consumed number's trustworthiness without invalidating the whole table.
- **INFO:** cosmetic / documentation (e.g., a stale docstring, a metadata-key glitch in the smoke payload only, a path imprecision) — does not touch any consumed number or gate. (Mirror your prior two findings' INFO calls.)

## Out of scope (do NOT gate on these)
- **The disposition RULING is gandalf's.** Your finding blesses the NUMBERS (and the harness correctness), NOT the verdict (ship-as-specialist vs kit-fix). Do not rule the disposition (brief §6: "gandalf consumes → STR disposition ruling"). Descriptive observation about the numbers is fine (you did this on the prior two); the RULING is gandalf's.
- **The pre-registered interpretation** (`2026-06-19-str-9pass-floor-pre-registered-interpretation.md`) is gandalf's read, NOT a gate — you do not verify against it.
- **The band values themselves** — `ENCOUNTER_COHORT_KPM_BAND` is read as-is (not a re-fit; not your call to re-band). Confirm the harness READS them correctly; do not assess whether the bands are right.
- **DPS as a verdict** — measured-never-gated; not the headline.

## Hand-back (what KR needs)
Append a completion record / point to the finding with:
- The verdict (PASS / PASS-WITH-INFO / WARN / BLOCK).
- V1–V6 each PASS/FAIL with the line cited (V1 + V6 especially).
- Confirmation the headline (STR clear-room pass count of 14, per cohort + per clear-type, with failure-SIDE split) reproduces first-hand.
- Confirmation of no production-gate regression (V6) + the git-status check.
- Confirmation the boss re-run reconfirms the 4 auto-fails + controls clear competently (consistency rails).
- Any INFO/WARN/BLOCK items with severity rationale.
- The decisions-log disposition (if any entry is warranted — e.g. a measurement-semantic note; your call per ADR-002).

## References
- gamora dispatch (the work under review): `agentic_orchestration/dispatches/2026-06-19-gamora-str-9pass-floor-all18-clearroom-harness.md`
- Run brief (§4 verify-gates, §5 endorse, §6 hand-back): `agentic_orchestration/gandalf/requests/2026-06-19-str-9pass-floor-clear-room-run-brief.md`
- Your two prior Gate-2 findings (reuse confirmed anchors): `agentic_orchestration/qa/findings/2026-06-19-gamora-clean-boss-numbers-harness-gate2.md` + `2026-06-19-gamora-dps-instrumentation-gate2.md`
- THE TRAP: `gauntlet_sim.py:1019` (`if t1_routing == TIER_1_REJECT:` → `continue` `:1029`, skipping tier_2 `:1032`)
- Bands: `gauntlet_sim.py:316-322` (`ENCOUNTER_COHORT_KPM_BAND`, cohort-invariant `:298-302`); floor `:158`
- The 18-catalog: `generation/endgame_encounter_catalog.py:161` (`len==18` `:50`)
- Instrument: `t4_sim_cycling.py:1199`; proxy-inclusive KPM `spatial_gauntlet/spatial_engine.py:1740`
