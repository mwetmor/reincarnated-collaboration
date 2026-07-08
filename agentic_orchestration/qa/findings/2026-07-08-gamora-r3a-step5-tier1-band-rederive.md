# Finding — 2026-07-08 — gamora R3a step-5 tier-1 KPM band re-derivation (open_arena + chokepoint_corridor)

**Reviewer:** jack-ryan (DEV-MODE Gate-2, BLOCK authority — difficulty-affecting calibration)
**Severity:** PASS (INFO-level notes only; no WARN, no BLOCK)
**Target:** tag `gamora/v-r3a-step5-tier1-band-rederive-1` / commit `649ff6a`
**Developer:** gamora (simulation seam)
**Principles applied:** Review Principle 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity). Disciplines #1, #1.1, #2.1, #11, #12, #13, #23, rider-4. ADR-004 / Principle-6 (boundary).

## What I found

A clean, scope-contained, genuinely density-anchored re-band. Every quantitative claim reproduces exactly against the raw step-4 data, and the crux — the corrected chokepoint funnel model — is geometry-grounded, NOT curve-fit-in-disguise. Verdict: PASS. KR may fire the step-4 re-run.

### Scope containment (verify #1) — CONFIRMED
- Commit `649ff6a` touched exactly 3 files: `gauntlet_sim.py`, the math note, `AGENT_STATE.md`. No `t4_sim_cycling.py`, no star-lord export/driver files, no `leg3_pilot_section8a1_band_measurement.json`.
- `_route_tier_1` predicate (`t4_sim_cycling.py`): `git diff` **empty** — byte-identical, verified.
- Only the two functional tuples changed: `open_arena` (9.90,15.53)→(20.87,53.33); `chokepoint_corridor` (11.65,15.88)→(12.52,60.00). The other 4 shells (`magic_pack`/`elite_pack`/`boss_with_adds`/`mini_boss`) byte-identical, verified in-diff.

### THE CRUX (#2) — density-anchor vs curve-fit — geometry-grounded, NOT curve-fit
This is where the Gate-2 earns its keep. Judgment: the corrected chokepoint funnel model is defensible **independent of the target it hits**. Three independent lines of evidence:

1. **Structural room difference is real, in source.** `SCENARIO_OPEN_ARENA` sets `serial_activation_radius_m=12.0` (arena.py:525 — serial gating: peak concurrent ~4, ~3-4 sequential bites → slower clear). `SCENARIO_CHOKEPOINT` sets it to `None` (arena.py:589-609 — NO serial gating; the funnel geometry concentrates the queue instead). Live-object check confirms: open=40 mobs/serial=12.0; choke=24 mobs/serial=None. The first-pass model was wrong for a verifiable reason — it applied open_arena's serial 45s clear-shape to a room that has no serial gating. The correction follows from a structural difference that exists in the room definition, predating this dispatch.
2. **The room's OWN documented cert intent grounds the AOE-concentration term.** arena.py:594-595 "Certifies confined-space clear throughput / AOE-vs-swarm economy at a chokepoint"; :540 "Corridor geometry (x-clamping) concentrates mobs for AOE advantage"; :564 "cone/line AOE probe." A concentrated queue hit by cone/line AOE clears faster than a dispersed field of equal count — the room is designed to reward exactly this. The funnel-throughput term is the room's density signature, not a kit artifact.
3. **The corrected ceiling sits ABOVE the observed p90 — the anti-curve-fit signature.** choke density hi = 60.00 KPM (24.0s); observed p90 = 57.14 KPM (25.2s). The density ceiling is ~2.9 KPM *faster* than any observed cell. A curve-fit to the percentile would land *on* p90; an independent geometry anchor with headroom lands *past* it. It lands past it. (open_arena density hi 53.33 vs p90 53.81 = essentially coincident, the clean-agreement case.)

The surfaced first-pass disagreement is real, not narrative: I reproduced choke @ first-pass (12.52, 32.0) → 72/189 = 38% in-band, 117 above (62%), matching the note verbatim. gamora honored rider-4: corrected the density MODEL against the room's geometry, not the band against the kits.

### Cohort-invariance (#3) — PRESERVED
Structural, verified in-diff: single per-shell tuple replicated identically across all 4 cohort columns (DPS-min-maxer/Balanced/Defensive/Hybrid) for both shells; no per-cohort branching introduced. `compute_tier_1_reject_breakout` reads `next(iter(band_by_cohort.values()))` — correct given invariance.

### Residual-reject breakout boundary (#4) — WITHIN-SEAM, correct
`compute_tier_1_reject_breakout` is a pure re-aggregation of already-serialized fields (`scenario_shell_id`, `tier_1_outcome`, `tier_1_kpm`) into a top-level `tier_1_reject_breakout` JSON key. No new export-schema field, no `spatial_fight_results` DB column, no §8-A1 report touch. Crosses no star-lord boundary. NO MIGRATION correct per ADR-004 / Principle-6 — D3 winner-tally precedent applies cleanly.

### Smoke + regression (#5) — REPRODUCED
Independently recomputed against `cycle-13-gauntlet-sim-results-20260708_065352.json` (the step-4 full-surface run):
- Density arithmetic (`KPM = mob_count×60/clear_s`): all four endpoints reproduce exactly (open 20.87/53.33 @ [115s,45s]; choke 12.52/60.00 @ [115s,24s]).
- Percentiles: open p10/med/p90 = 22.31/31.89/53.81; choke 23.39/35.20/57.14 — match note verbatim.
- In-band: open 204/252 = 81% (36 above / 12 below); choke 171/189 = 90% (18 above / 0 below) — match submission's breakout split exactly.
- Old-band diagnosis: 100% of cells reject ABOVE the stale ceiling on BOTH shells — the "~2× too fast / stale ceiling not non-viability" claim is confirmed real.
- Regression: `test_cycle13_wave5_gauntlet_sim.py` + `test_spatial_gauntlet_scenarios.py` = **77 passed** (50+27), matching gamora's claim. (Note: a broad `pytest tests/` collection hits 4 pre-existing errors in naming/vocabulary test files from a `grouping-layer-vocabulary.md` path-resolution issue — unrelated to this change, which touches neither module.)

### §4 gate untouched (#6) — CONFIRMED
The commit contains no §4-gradient-criterion logic file; the acceptance criterion is untouched by construction. The re-band only re-bases the tier-1 admission window so the two scenarios ENTER tier-2 and their surface can be measured at the step-4 re-run. §4 is judged there, not here.

## Rationale
Rider-4 (anti-Goodhart) is the load-bearing discipline for a calibration re-band, and it is satisfied: the band is anchored to what the room's density/geometry SHOULD demand (Disc #1, #23), cross-checked against — not fitted to — the observed distribution (Disc #11), with the one material disagreement surfaced and resolved by a source-grounded model correction, not a silent pick-the-greener-one. Scope is contained to the two constant tuples (Disc #13 drift repair, one gate deeper than the §1 constants). Boundary call within-seam per ADR-004 / Principle-6. Cohort-invariance (Matt rider) preserved structurally and empirically.

### INFO notes (for the record; non-blocking)
- **Floors are timeout-anchored, not density-anchored.** Both `lo` values invert from ~115s (just inside the 120s KILLS_ONLY cap), not from a density model per se. Honestly labeled as "slowest viable clear near timeout" and it is the conservative choice (admits any kit that clears; below-floor = genuine non-clear). Matt should note the floors are anchored to the timeout, the ceilings to geometry.
- **`24s` chokepoint ceiling is a coarse round-number anchor.** It is defensible (geometry-grounded, headroom above p90), but it is a single-point "brisk AOE sweep" estimate rather than a mob-by-mob throughput derivation. Fine for admitting the arena; if the step-4 re-run shows the choke surface railing at the ceiling, revisit the funnel-throughput term with a finer model.
- **Breakout `else` branch conflates two reject types.** In-band-KPM-but-REJECT (completion-gate fail on the clear-shell domain-guard) is bucketed into `reject_below_floor`. Defensible as "an honest non-clear bucket," but it means `reject_below_floor` is not purely a KPM-below-floor count for shells with a completion route. Not load-bearing for open/choke (neither uses the completion gate here), so no action; noting for interpretation of the breakout on other shells.

## Action
- [x] Developer (gamora): none required. Work PASSES Gate-2.
- [ ] Matt: no decision needed. This is a within-seam, cohort-invariant, geometry-anchored calibration; the ADR-002 tiered-approval + Matt-rider set is satisfied. FYI on the three INFO notes above (floors timeout-anchored; 24s coarse; breakout `else`-bucket) — none blocking.
- [ ] KR: cleared to fire the step-4 $0 re-run (budget ~25-30 min wall-clock per gamora's Disc #1.1 projection) and judge §4 on the full surface. Residual-reject breakout is the instrument to read FIRST (proves the ~375 cells entered the arena) before reading the §4 gradient.

## References
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (bands `:456-460`; `compute_tier_1_reject_breakout` `:475-533`; payload wiring `~:1632`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` (`_route_tier_1` — byte-identical, empty diff)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (SCENARIO_OPEN_ARENA `:497-526`, serial=12.0; SCENARIO_CHOKEPOINT `:589-609`, serial=None; choke geometry `:547-586`; cert intent `:591-595`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/r3a-step5-tier1-band-rederive-2026-07-08.md` (math note)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260708_065352.json` (step-4 observed data — percentiles + in-band reproduced against this)
- Dispatch: `agentic_orchestration/dispatches/2026-07-08-gamora-r3a-step5-tier1-band-rederive.md`
- Submission: `agentic_orchestration/qa/pending/2026-07-08-gamora-r3a-step5-tier1-band-rederive-gate2-CLEARED.md`
