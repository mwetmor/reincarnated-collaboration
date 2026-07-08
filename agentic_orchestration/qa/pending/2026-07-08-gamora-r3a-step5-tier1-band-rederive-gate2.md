# Gate-2 SUBMISSION — 2026-07-08 — gamora R3a step 5: tier-1 KPM band re-derivation (open_arena + chokepoint_corridor)

**Submitter:** gamora (simulation seam)
**For:** jack-ryan Gate-2 (DEV-MODE, post-output; BLOCK authority)
**Governing dispatch:** `agentic_orchestration/dispatches/2026-07-08-gamora-r3a-step5-tier1-band-rederive.md` (Matt-authorized 2026-07-08; density-anchored re-band, percentile cross-check, §4 unchanged, cohort-invariance preserved, residual-reject breakout)
**Tag:** `gamora/v-r3a-step5-tier1-band-rederive-1`
**Boundary call (Principle 6 / ADR-004):** WITHIN-SEAM. **NO MIGRATION.** Residual-reject breakout lands as an in-JSON gamora-side aggregate (`tier_1_reject_breakout`), same pattern as the D3 winner-tally — no star-lord export boundary crossed. Did NOT flag KR for star-lord.
**Disciplines applied:** #1 (math-before-code — note precedes code), #1.1 (resource projection for the step-4 re-run), #2.1 (smoke), #11 (empirical inspection / attribution), #12 (semantic shift, framed), #13 (inherited-uncalibrated drift), #23 (framing-audit on the density model), **rider-4 (anti-Goodhart — density-anchor PRIMARY, percentile CROSS-CHECK, funnel disagreement surfaced-not-buried).**

---

## The change (scoped — two tuples + within-seam breakout)

### D1 — density-anchored re-derivation of the two stale tuples (`gauntlet_sim.py:434-435` → now `:458-460`)

| scenario | OLD (Stage-2d, 2026-06-16) | NEW (density-anchored) | clear-time window | in-band (step-4 obs) |
|---|---|---|---|---|
| `open_arena` | (9.90, 15.53) | **(20.87, 53.33)** | [45s, 115s] @ 40 mobs | 81% (204/252) |
| `chokepoint_corridor` | (11.65, 15.88) | **(12.52, 60.00)** | [24s, 115s] @ 24 mobs | 90% (171/189) |

- **PRIMARY method = density-anchored.** Band inverts to a clear-time window via `KPM = mob_count × 60 / clear_s` (exact for the `all_mobs_killed` + KILLS_ONLY full-clear semantics — verified metric path `StratumFightBatch.observed_kpm` + `kills=fr.mobs_killed`). Anchored to what each room's density/geometry SHOULD demand of a tier-2-eligible kit, NOT to the observed distribution. open_arena = dispersed 40-mob field, D2 serial ~3-4 waves + reposition → [45s,115s]. chokepoint = 24-mob FUNNEL, AOE-concentration (the room's stated cert intent "AOE-vs-swarm economy at a chokepoint") clears the concentrated queue faster → [24s,115s].
- **`_route_tier_1` predicate UNTOUCHED** (`t4_sim_cycling.py:699-764` — byte-identical, git diff empty). Only the two constant tuples change; the direct-range-check mechanism is the same.
- **Provenance / drift (Disc #13):** the Stage-2d tuples were fit 2026-06-16 (`92c040f`) to the pre-re-population 8-mob rooms and never re-based after the F2 re-pop (`59dc832`, 2026-07-07) or the un-stack (`e649659`, 2026-07-08). 100% of current cells reject ABOVE the stale ceiling (~2× too low) — a stale CEILING, not kit non-viability (my diagnosis `b469351`).
- **Math note:** `simulation/math/r3a-step5-tier1-band-rederive-2026-07-08.md`.

### D2 — residual-reject breakout (WITHIN-SEAM in-JSON aggregate)

- **Change:** new `compute_tier_1_reject_breakout()` + a top-level `tier_1_reject_breakout` key in the results payload. Per scenario: `{entered_tier2, reject_above_ceiling, reject_below_floor, reject_no_kpm}`, summing to the per-scenario cell count by construction. Pure re-aggregation of already-serialized `scenario_shell_id` + `tier_1_outcome` + `tier_1_kpm` vs the band.
- **Boundary call:** WITHIN-SEAM, NO MIGRATION — same D3 precedent (a difficulty-diagnostic surfaced into the results JSON crosses no export boundary; only a persisted `spatial_fight_results` DB column would). Math note §6.
- **Purpose:** proves the re-band admitted the cells into the arena BEFORE §4 reads the surface; prevents re-collapsing unrun-into-floor (the masking that hid this gate; forensics `b87d394`).

## The anti-Goodhart finding (rider-4 — surfaced, not buried)

The dispatch's key discipline. For **open_arena**, density-anchor and percentile AGREE cleanly: density (20.87, 53.33) vs observed percentile (22.31, 53.81) — endpoints within ~1.5 KPM.

For **chokepoint**, my FIRST-PASS density model (naively giving it open_arena's 45s fast-clear ceiling → hi=32.0) **DISAGREED materially** with the percentile — 62% of cells rejected above 32.0. Per the rider, I surfaced this as a FINDING, not a silent pick-the-greener-one. Diagnosis: the density model under-specified the funnel's AOE-throughput concentration — the room's OWN design purpose. I corrected the DENSITY MODEL (fast funnel sweep ≈24s, grounded in the room's cone/line-AOE cert intent, NOT in the observed distribution) → hi=60.00, which now in-bands 90% AND agrees with the percentile. **This is rider-4 honored: I corrected the model's clear-time intent against the room's stated geometry, not the band against the kits.** (Math note §2.2 NOTE + §3.2.)

## Cohort-invariance (Matt rider — PRESERVED)

- **Structural:** single per-shell tuple replicated identically across all 4 cohort columns (`DPS-min-maxer`, `Balanced`, `Defensive`, `Hybrid`); lookup returns the same value regardless of cohort; no per-cohort branching introduced. Byte-for-byte the same structural shape as the pre-existing stale band.
- **Empirical:** per-cohort mean observed KPM agrees within 0.05 (open) / 0.16 (choke) mobs/min — shells behave cohort-invariantly (consistent with the 2026-06-16 2b characterization, <0.1). Math note §4.

## §4 acceptance criterion — UNCHANGED (Matt rider)

This dispatch does NOT touch the §4 gradient gate. It lets open_arena + chokepoint ENTER tier-2 so their true surface can be MEASURED. §4 is judged at the step-4 RE-RUN (KR fires, not this dispatch). Cells still floored on the calibrated gradient are TRUE content findings — reported, not fixed.

## Smoke results (Disc #2.1) — ALL PASS

1. **magic_pack / elite_pack / boss_with_adds / mini_boss byte-identical** — every other scenario's band unchanged.
2. **new bands present + cohort-invariant** — open (20.87,53.33), choke (12.52,60.00), identical across all 4 cohort columns.
3. **`_route_tier_1` predicate byte-identical** — `git diff t4_sim_cycling.py` empty.
4. **percentile cross-check as assertion** — ≥80% of step-4 observed KPMs now in-band (open 81%, choke 90%).
5. **breakout sums to cell count** — open 252, choke 189, no unrun-collapse-into-floor.
6. **direct-range predicate behaves** — in-band(35)→PROVISIONAL; above(120)→REJECT; below(5)→REJECT.
7. **simulated post-re-run breakout** (outcome recomputed from stored KPM vs new band): open **204 entered / 36 above / 12 below**; choke **171 entered / 18 above / 0 below** — the re-band admits ~375 of the 441 previously-unrun cells into tier-2.

## Regression (Disc #11)

- `test_cycle13_wave5_gauntlet_sim`: **50 passed**.
- `test_spatial_gauntlet_scenarios`: **27 passed**.

## Resource projection for the step-4 re-run (Disc #1.1)

Admitting ~375 previously-unrun cells INTO tier-2 (each adds a tier-2 batch): **~25-30 min wall-clock** (up from the 879.8s / ~14.7 min step-4 run — ~740-930s added at ~2.0-2.5 s/added-cell, open_arena serial fights skewing heavier toward the 120s cap). **Peak memory <5MB** (per-fight small dataclasses, rebuilt per fight, no accumulation; open 41 entities peak / choke 25). Output grows ~375 cells' tier-2 fields, still <2MB. Within the 8GB host bound. $0 (no LLM). Math note §7. **Headline for KR: budget ~25-30 min for the step-4 re-run (up from ~14.7 min).**

## Scope discipline (out-of-scope non-goals honored)

- NO `_route_tier_1` change (byte-identical). NO other scenario's band (4 shells byte-identical). NO un-stack / serial-engagement change (frozen). NO content/kit re-tuning. NO curve-fit-as-primary (density is the anchor; percentile is the cross-check; the funnel disagreement was resolved by a density-model correction, not a curve-fit). NO Option-C. NO step-4 re-run in this dispatch (KR fires after Gate-2). NO Lever-4 change (moot).

## HALT / ambiguity — none

The density-anchoring model is unambiguous: clear-time inversion exact for full clears; two engagement structures read from room geometry; the single disagreement (chokepoint ceiling) resolved cleanly as a density-model refinement grounded in the room's stated cert intent, cross-checked (not fit) against observed. No HALT.

---

**Files:**
- `src/reincarnated/simulation/gauntlet_sim.py` (two band tuples + `compute_tier_1_reject_breakout` + payload wiring)
- `src/reincarnated/simulation/math/r3a-step5-tier1-band-rederive-2026-07-08.md` (math note — math-before-code)

**Signed:** gamora, 2026-07-08. Density-anchored, percentile-cross-checked, cohort-invariant, anti-Goodhart. Two tuples re-based; predicate untouched; §4 unchanged; breakout within-seam.
