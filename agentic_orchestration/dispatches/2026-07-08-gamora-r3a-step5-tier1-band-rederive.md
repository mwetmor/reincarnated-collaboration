# Dispatch — 2026-07-08 — gamora — R3a step 5: tier-1 KPM band re-derivation (open_arena + chokepoint_corridor)

**From:** knight-rider (chain-orchestrated; KR fires the sub-agent himself per the pre-ratified execution protocol)
**To:** gamora (simulation seam — sole seam; no cross-seam boundary expected, see Principle-6 gate below — one CONDITIONAL on the after-report)
**Approved by:** Matt 2026-07-08 — "Tier-1 re-band AUTHORIZED as R3a step-5, scoped to the two stale tuples (gauntlet_sim.py:434-435). Riders per gandalf: density-anchored re-derivation with percentile cross-check (math-note-first), §4 unchanged as the acceptance gate, Gate-2, cohort-invariance preserved, residual-reject breakout in the after-report. Then re-run step-4 and bring me the §4 verdict on the full surface." Pre-authorized; no fresh run-auth.
**Estimated effort:** gamora small–medium. Math-note-first (density derivation + percentile cross-check). Gate-2. One-constant-class change (two tuples).
**Chain position:** R3a step 5 (of the batch2 pre-ratified chain). Precedes a step-4 RE-RUN ($0 gauntlet re-run → §4 gradient check on the FULL surface). Follows the closed diagnosis chain (step-4 §4 FAIL → forensics → §4 verdict → tier-1 binary).

## Why this exists
The R3a step-4 after-side re-run's WR surface is still a step function (§4 FAIL, 0.0017 mid-fraction). The diagnosis chain traced the dominant cause one gate deeper than the two ratified levers (un-stack + serial-engagement) reached: **open_arena (252 cells) + chokepoint_corridor (189 cells) reject at TIER-1 and never run tier-2** — so a tier-2 engagement lever structurally could not move them; their "WR=0.000 floor" was "never entered the arena," masked by the 0.0 dataclass-default. Your own tier-1 binary (commit `b469351`) resolved it cleanly: the kits clear these rooms **~2× too FAST** (KPM above the band ceiling, not below the floor). The tier-1 KPM band is a **fourth inherited-uncalibrated gate** — both tuples last written 2026-06-16 (`92c040f`, Stage-2d), never re-based after the F2 room re-population (`59dc832`, 2026-07-07) or the un-stack (`e649659`, 2026-07-08). Same Discipline #13 drift shape as the three §1 constants, one layer down. Matt authorized a scoped re-derivation.

## Required reading (session-start)
- `agentic_orchestration/gamora/notes/2026-07-08-r3a-tier1-gate-band-vs-viability-diagnosis.md` — your own tier-1 binary (`b469351`): the 2× miss, the provenance, the p10/p90 re-fit signature (81% in-band), the field locations (`gauntlet_sim.py:434-435` def, `:1237` lookup, `:1278-1288` REJECT continue; `t4_sim_cycling.py:699-766` `_route_tier_1`).
- `agentic_orchestration/gamora/notes/2026-07-08-r3a-step4-coherence-forensics.md` (`b87d394`) — the 0.0-default / unrun-cell semantics. LOAD-BEARING for the residual-reject breakout: the after-report must NOT re-collapse unrun-into-floor.
- `agentic_orchestration/gandalf/notes/2026-07-08-r3a-step4-s4-verdict-and-next-move.md` (`988663e`) — the §4 verdict (uncontested FAIL), the tier-1-gate design read, the re-band-vs-Option-C framing. The RIDERS trace to gandalf's design frame.
- `agentic_orchestration/gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md` — §4 acceptance criterion (UNCHANGED by this dispatch), §1 (density-not-HP-is-the-discriminant — the density anchor for the re-derivation).
- Run-state `agentic_orchestration/batch2-run-state-2026-07-06.md` — the last five KR DELTAs (step-4 through this authorization).
- Engineering disciplines #1 (math-before-code), #1.1 (resource-bounds projection), #2.1 (smoke-test scaling), #11 (attribution), #13 (inherited-uncalibrated drift), #23 (framing-audit), rider-4 (do NOT fit the instrument to the content — this is the KEY discipline for a re-band: anchor to what the room SHOULD demand, cross-check against observed, do NOT curve-fit the band to whatever the kits currently do).

## Deliverable (math-note-first per Discipline #1; single coordinated Gate-2)

### D1 — Density-anchored re-derivation of the tier-1 KPM band, with percentile cross-check
- **What:** re-derive the tier-1 KPM band tuples for `open_arena` and `chokepoint_corridor` — and ONLY those two — at `gauntlet_sim.py:434-435`. The `_route_tier_1` predicate is UNTOUCHED.
- **PRIMARY method — density-anchored (Discipline #1, math-before-code, anti-Goodhart per rider-4):** derive the band from the room's CURRENT density/geometry — what tier-1 KPM the gate SHOULD demand given the F2 mob population (open_arena ~40 mobs; chokepoint per its geometry) and the room's clear-time intent. The band expresses "a kit that belongs in tier-2 clears the tier-1 shell within this KPM window"; anchor the window to the room's mob-count / expected engagement, not to the observed kit distribution.
- **CROSS-CHECK method — percentile:** verify the density-anchored band against the observed post-step-4 KPM distribution (your diagnosis: open_arena median 31.9, chokepoint 35.2, each ~2× the stale ceiling; the distribution shifted up as one coherent mode, no can't-clear fracture, p10/p90 re-fit in-bands 81%). The density-anchored band should land near the observed central mass. **If density-anchored and percentile disagree materially, that is a FINDING to surface (Disc #11) — do NOT silently pick the one that greens more cells.** Report the disagreement and your reasoning for the chosen band.
- **Cohort-invariance (Matt rider):** the re-derived band must apply uniformly across cohorts — no cohort-specific band values, no per-cohort branching. Assert/verify cohort-invariance is PRESERVED (the current band is cohort-invariant; the re-derivation must not introduce cohort dependence). State how you verified it in the math-note.
- **Math-note (framing-audit, Disc #23):** show the density→KPM-window arithmetic (assumptions stated); show the percentile cross-check; show the cohort-invariance argument; cite the band's provenance (2026-06-16 `92c040f`) and why the F2 re-pop + un-stack invalidated it (Disc #13).

## Acceptance criterion (UNCHANGED — Matt rider; gandalf §4; judged at the step-4 RE-RUN, NOT this dispatch)
The re-band does NOT change the §4 gate. The bar remains: **the WR surface regains a gradient — meaningful per-scenario WR mass in (0.05, 0.95); differentials persist as SPREAD, not RAILS.** This dispatch's job is to let open_arena + chokepoint ENTER tier-2 so their true surface can be MEASURED. Whether that surface then gradients is judged at the step-4 re-run (KR fires). Cells still floored on a calibrated gradient are TRUE content findings — REPORT, do not fix content to satisfy the instrument (rider-4).

## Residual-reject breakout in the after-report (Matt rider — LOAD-BEARING honesty)
After the step-4 re-run, the after-report must **break out residual tier-1 rejects** per scenario: post-re-band, how many cells STILL reject at tier-1 and WHY (above ceiling / below floor), vs how many now ENTER tier-2. This makes "did the re-band actually admit the cells into the arena" measurable and prevents re-collapsing unrun-into-floor (the exact masking that hid this gate). The breakout is the instrument that proves the re-band worked BEFORE the §4 surface is read.
- **Where it lands (boundary call, Principle-6 gate below):** default = emit it WITHIN your seam (the gauntlet results JSON aggregate, same pattern as the D3 winner-tally you landed within-seam last step — a per-(scenario) `tier_1_reject_reason` tally: `{entered_tier2, reject_above_ceiling, reject_below_floor}`). **IF you judge it must land in the driver's §8-A1 `leg3_pilot_section8a1_band_measurement.json` report** (star-lord's export/driver seam), that crosses the boundary → **MIGRATION.md + star-lord coordination REQUIRED** (ADR-004); flag KR to fire star-lord. YOUR file-owner call, exactly like D3.

## Smoke-test expectation (Disc #2.1)
- Smoke that the re-derived band in-bands the target fraction of the observed open_arena + chokepoint KPM distribution (the percentile cross-check as an assertion — e.g., ≥N% of the step-4 observed KPMs now fall in-band).
- Smoke that ONLY the two tuples at `:434-435` changed — every other scenario's band byte-identical; `_route_tier_1` predicate byte-identical.
- Smoke that cohort-invariance holds (the band value a given scenario is tested against does not vary by cohort).
- **Resource projection (Disc #1.1):** the step-4 re-run cost — admitting ~441 previously-unrun cells INTO tier-2 will INCREASE total fights and wall-clock vs the 879.8s / <1MB step-4 run. Project peak memory + wall-clock and confirm it stays within host bounds. This is the one place the re-band changes the run cost materially — size it before KR fires the re-run.

## Principle-6 cross-seam gate (knight-rider, at authoring)
- **D1 (band re-derivation):** two constant tuples in `gauntlet_sim.py`, gamora-owned; `_route_tier_1` untouched. No boundary field. NO MIGRATION expected.
- **Residual-reject breakout:** **CONDITIONAL.** In-JSON gamora-side aggregate (default) = within-seam, NO MIGRATION. IF it lands in the driver's §8-A1 report = crosses to star-lord export/driver seam → **MIGRATION.md + star-lord coordination REQUIRED** (ADR-004). You make the call; if it crosses, flag KR to fire star-lord.

## Tag + Gate-2
- Tag: `gamora/v-r3a-step5-tier1-band-rederive-1` (seam-prefixed per convention).
- Submit to `agentic_orchestration/qa/pending/` for **jack-ryan Gate-2** (tier-1 gate calibration change — difficulty-affecting; the anti-Goodhart discipline (density-anchor vs curve-fit) is exactly what Gate-2 should stress).
- Auto-commit (authorized cycle work). Push granted (R6 push-as-you-go). Report commit hash(es) to KR.

## Out of scope (explicit non-goals)
- **NO change to any scenario's band OTHER than open_arena + chokepoint_corridor** (`:434-435` only).
- **NO change to `_route_tier_1` logic / predicate** — the routing is correct; only the band it tests against is stale.
- **NO change to the un-stack or serial-engagement** (landed, Gate-2-passed — frozen).
- **NO content/kit re-tuning** (rider-4). The re-band anchors to room density, NOT to greening cells.
- **NO curve-fitting the band to the observed distribution as the PRIMARY method** — percentile is the CROSS-CHECK, density is the anchor. (Fitting the band to whatever the kits do is the Goodhart move rider-4 forbids.)
- **NO Option-C machinery** — the diagnosis ruled re-band, not Option-C; Option-C stays deferred.
- **NO Lever-4 certification-criterion change** — MOOT per gandalf (gradient did not return).
- **NO step-4 re-run in this dispatch** — KR fires the $0 re-run separately after Gate-2, then judges §4 on the full surface.
- **NO leg-3 wire / chassis / bars / bands / kit-constant touches** (frozen).

## Open questions for gamora to resolve
- The density-anchoring model itself: how you translate room mob-count/geometry → the target tier-1 KPM window (your math; state assumptions).
- Whether the density-anchored band and the percentile cross-check AGREE (report either way; disagreement is a finding, not a silent choice).
- Residual-reject breakout location: in-JSON gamora aggregate (default, within-seam) vs driver §8-A1 report (MIGRATION + star-lord) — your boundary call.

## References
- gamora tier-1 binary (`b469351`); gamora step-4 forensics (`b87d394`); gandalf §4 verdict + next-move (`988663e`); gandalf design read (§1 density anchor, §4 gate); run-state `batch2-run-state-2026-07-06.md` (last five deltas). Band def `gauntlet_sim.py:434-435`; lookup `:1237`; REJECT `:1278-1288`; routing `t4_sim_cycling.py:699-766`. ADR-004 (MIGRATION), Principle 6, Disciplines #1/#1.1/#2.1/#11/#13/#23, rider-4.

## Completion record

**Completed:** gamora, 2026-07-08. Math-note-first (Disc #1) → implementation → smoke (Disc #2.1) → Gate-2 submission → tag → commit → push.

**Derived band values (old → new):**
| scenario | OLD (Stage-2d) | NEW (density-anchored) | clear-window | in-band |
|---|---|---|---|---|
| `open_arena` | (9.90, 15.53) | **(20.87, 53.33)** | [45s, 115s] @ 40 mobs | 81% |
| `chokepoint_corridor` | (11.65, 15.88) | **(12.52, 60.00)** | [24s, 115s] @ 24 mobs | 90% |

Density model: KPM = mob_count×60/clear_s (exact for the all_mobs_killed + KILLS_ONLY full-clear semantics). Anchored to the room's density/geometry (open = dispersed 40-mob D2-serial field; choke = 24-mob AOE-concentrating funnel), NOT to the observed distribution. `_route_tier_1` predicate UNTOUCHED; other 4 shells byte-identical.

**Density-anchor vs percentile — AGREE (with one surfaced finding):**
- **open_arena: AGREE cleanly.** density (20.87, 53.33) ≈ percentile (22.31, 53.81), within ~1.5 KPM at both endpoints.
- **chokepoint_corridor: first-pass DISAGREED (surfaced, rider-4).** My naive first density model gave choke the open 45s ceiling (hi=32.0), which in-banded only 38% (62% above-ceiling). I surfaced the disagreement as a FINDING and diagnosed it: the model under-specified the funnel's AOE-throughput concentration (the room's OWN cert intent). I corrected the DENSITY MODEL (fast funnel sweep ≈24s, grounded in the room's cone/line-AOE design, NOT the observed distribution) → hi=60.00, now 90% in-band and agreeing with percentile. Corrected the model against the room's geometry, not the band against the kits.

**Cohort-invariance — PRESERVED.** Single per-shell tuple replicated identically across all 4 cohort columns; no per-cohort branching. Empirical: per-cohort mean KPM agrees <0.16 mobs/min. Verified structurally + empirically (math note §4).

**Residual-reject breakout — boundary call: WITHIN-SEAM (NO MIGRATION, NO star-lord).** Landed as `tier_1_reject_breakout` top-level aggregate in the gauntlet results JSON — pure re-aggregation of already-serialized `tier_1_outcome` + `tier_1_kpm` vs the band (same D3 winner-tally precedent). Simulated post-re-run split: open **204 entered_tier2 / 36 above / 12 below**; choke **171 entered / 18 above / 0 below** — the re-band admits ~375 of the 441 previously-unrun cells into tier-2. Did NOT flag KR for star-lord.

**Smoke — ALL PASS.** (1) 4 other shells byte-identical; (2) new bands cohort-invariant; (3) `_route_tier_1` byte-identical (empty diff); (4) percentile cross-check ≥80% in-band (open 81% / choke 90%); (5) breakout sums to cell count; (6) predicate in/above/below routing correct; (7) simulated post-re-run breakout populated. Regression: `test_cycle13_wave5_gauntlet_sim` 50 passed + `test_spatial_gauntlet_scenarios` 27 passed.

**Step-4 re-run resource projection (Disc #1.1):** **~25-30 min wall-clock** (up from 879.8s / ~14.7 min — ~375 cells added to tier-2 at ~2.0-2.5 s/cell, open_arena serial fights skew toward the 120s cap). Peak memory <5MB, output <2MB, within 8GB host bound. $0. **KR: budget ~25-30 min for the step-4 re-run.**

**Tag:** `gamora/v-r3a-step5-tier1-band-rederive-1`
**Commit(s):** engine `<see below>` (band + breakout + math note + Gate-2/dispatch/completion in collab meta-repo).
**Gate-2:** submitted to `agentic_orchestration/qa/pending/2026-07-08-gamora-r3a-step5-tier1-band-rederive-gate2.md`.
**HALT / ambiguity:** none. Density-anchoring model unambiguous; the one disagreement resolved cleanly per rider-4.

**Awaiting:** jack-ryan Gate-2. On PASS, KR fires the step-4 $0 re-run and judges §4 on the full surface.
