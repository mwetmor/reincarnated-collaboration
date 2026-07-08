# R3a step-4 — §4 gradient verdict + next-move recommendation (the levers-spent fork)

**Author:** gandalf (DRIFT-CRITIC on §4; SPEC-AUTHOR/ELICITOR on the next-move fork)
**Date:** 2026-07-08
**Trigger:** KR routed the measured R3a step-4 after-side re-run for my §4 verdict + a Matt-ready next-move read. §4 is my authored criterion; the next-lever call is my §5 taxonomy.
**Inputs (all verified this session):**
- My design read §§1-6 + §5.2-AMEND: `agentic_orchestration/gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md`
- gamora forensics (transcribed in run-state KR DELTA + commit `b87d394`): corrected 603-cell surface, both anomalies resolved, the tier-1-reject byproduct
- Source, read this session: `t4_sim_cycling.py:1801-1840` (the `TIER_1_REJECT → continue` site — tier-2 never runs) + `_route_tier_1` `:699-760` (the `band_override` CLEAR-shell path)
- §6 ruling proposal: `qa/pending/2026-07-08-kr-decisions-log-proposal-s6-spatial-difficulty-ruling.md`
- Run-state deltas: `batch2-run-state-2026-07-06.md` (tail)

▶ ROLE: DRIFT-CRITIC — judging the step-4 build against my own §4 spec.

---

## 1. Official §4 verdict — FAIL

**The §4 anti-Goodhart gradient criterion is NOT met.** One clear line:

> On the authoritative surface — the **603 genuinely-simulated cells** (gamora stripped the 594 unrun 0.0-default cells) — the distribution is **482 ceiling / 120 floor / 1 mid = 0.0017 mid-fraction.** The criterion demands meaningful WR mass in (0.05, 0.95) with per-kit differentials present as *spread, not rails.* One cell is not mass. The surface is still a step function. **§4 FAILS.**

Robust under both readings (raw 1197-cell → 0.001; corrected 603-cell → 0.0017) — the correction moved the number in the *non-rescuing* direction, so there is no reading of this run that passes. The two authorized R3a levers (Option-A un-stack + serial-engagement) **redistributed which cells sit at which rail** (open_arena/chokepoint pushed around, elite_pack all-ceiling, magic_pack still floored) without producing a gradient. The lever budget is spent; the instrument still does not discriminate. This is a clean, uncontested FAIL — not a confounded one.

---

## 2. Why the levers didn't gradient the surface — my original diagnosis was RIGHT-BUT-INCOMPLETE

The tier-1-reject finding does not overturn §§1-3. It reveals the diagnosis was **correct in mechanism, incomplete in scope.** Precisely:

- **§1 was right and stands over-determined.** "HP is not the discriminant; engagement geometry is" — confirmed. magic_pack still floors at the lowest HP; the un-stack (a pure HP-budget move) predictably did nothing for the floored rooms. Nothing about the tier-1 finding rescues HP as the lever.
- **§2's engagement-geometry read was right for the rooms it could reach.** Serial-engagement IS the correct grammar for total-field alpha-strike. But it is a **tier-2** fix — it changes how a pack activates *once the gauntlet fight runs.*
- **The scope error I could not see from the band report alone:** open_arena (252 cells) and chokepoint_corridor (189 cells) — the two worst scenarios, 441 cells — **never reach tier-2. They reject at tier-1** (`_route_tier_1` `band_override` path: their tier-1 quick-estimate KPM falls outside the calibrated `ENCOUNTER_COHORT_KPM_BAND`, so `TIER_1_REJECT → continue`, tier-2 is never simulated, survival reads floor by the 0.0 dataclass-default at `:411`). **A tier-2 engagement-geometry lever is structurally incapable of moving a scenario that dies at tier-1.** I authored a lever for a fight these two rooms never get to have.

So the honest verdict on my own §5: the un-stack + serial-engagement diagnosis was **right-but-insufficient**, and for the two worst scenarios the tier-1 gate was the real bottleneck **all along.** My §5 taxonomy was built on the band report, which reads a tier-1-rejected cell and a tier-2-death cell as the *same* WR=0.000 floor — the band surface cannot distinguish "died in the arena" from "never entered the arena." That collapse is exactly what hid the tier-1 gate. gamora's tier-split byproduct is the input §5 lacked, and it is a genuine new finding, not a correction I should have pre-empted from the data I had.

**This is Discipline #13 drift caught one layer down:** an implicit pillar (the tier-1 KPM band, calibrated for a *different* regime) was silently governing outcomes while everyone tuned the tier-2 layer above it. Same shape as the three-inherited-uncalibrated-constants pattern in §1 — a fourth inherited-uncalibrated gate, this one structural rather than numeric.

---

## 3. Next-move recommendation for Matt — ONE next thing

The authorized lever budget is spent, §4 is unmet, and this is a genuinely un-pre-ruled fork. First: **the conditional Lever-4 touchpoint is MOOT.** It was framed "gradient returns + structural fails persist → rule the certification criterion with data." The gradient did NOT return. Ruling the certification criterion now would be tuning the *gate that judges the surface* while the surface itself is still broken by a mechanism we just identified — that is ruling on an artifact. Lever-4 stays parked; do not spend a Matt touchpoint on it.

The realistic forks, ranked:

**(RECOMMENDED) — a $0 tier-1-gate structural investigation, scoped to the 441 tier-1-rejected cells, BEFORE any further lever spend.** One read-only gamora pass: *why* do open_arena + chokepoint tier-1 KPM estimates fall outside the band — is the `ENCOUNTER_COHORT_KPM_BAND` for these two scenarios itself an inherited-uncalibrated constant (calibrated pre the 2026-07-07 F1/F2 re-population, like the leash and the ×1.5 were), or are these kits genuinely non-viable in these rooms? This is the §5-analog diagnostic I ran for the floor-saturation finding, one level deeper. **Cost: $0, minutes, read-only, no Matt touchpoint to authorize a read.** It is the direct continuation of the "still rails → diagnose before any further lever move, no schedule-bending" branch KR already took. We do not know whether the fix is "re-band tier-1 for the re-populated regime" (cheap, one constant) or "these rooms need Option-C" (structural) until we read the gate. **Spending Option-C or re-opened magnitudes before this read is buying a lever without knowing which lock it fits** — the exact joint-state-never-re-ruled error that produced this whole saturation in the first place (§1). Do it once more, correctly, one layer down.

**(deferred, gated on the investigation) — Option-C per-scenario difficulty-spec block.** From my §3 and the §6 proposal, Option-C (HP factor + density + clock + *and now: tier-1 band* as one governed per-scenario structure) is the right *eventual* shape if the scenario family keeps growing. It is a real answer — but it is more machinery than we've earned, and it should absorb the tier-1 band as a governed field, which is precisely what the investigation tells us. Option-C *after* the read is well-targeted; Option-C *before* it is speculative scope.

**(reject) — re-open lever magnitudes.** The un-stack was a binary scope-retirement (no magnitude); serial-engagement radii come from room geometry, not a dial we can turn harder. There is no magnitude to re-open that would reach the tier-1-rejected rooms. This fork is a non-starter by mechanism.

**The ONE next thing:** authorize the $0 read-only tier-1-gate investigation (gamora, minutes) — is the tier-1 KPM band for open_arena + chokepoint a fourth inherited-uncalibrated constant, or true kit non-viability. **Cost: $0, no run, no Matt touchpoint required to fire a read.** Its output is a *targeted* fork for Matt — re-band (cheap) vs Option-C (structural) — instead of the raw options menu we'd hand him now. That keeps the next real Matt touchpoint (still R5 band-sheet values) clean and lets the next lever be aimed at the lock we've actually identified.

**Sign-off:** gandalf, 2026-07-08. §4 = FAIL (603-cell, 0.0017 mid-fraction). Original diagnosis right-but-insufficient; tier-1 gate was the bottleneck for the two worst scenarios all along. Recommended next: $0 tier-1-gate structural read before any further lever spend; conditional Lever-4 is moot (gradient did not return).
