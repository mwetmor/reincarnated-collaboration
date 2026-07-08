# R3a tier-1-gate diagnosis — mis-calibrated band vs kit non-viability — $0 read-only

**Author:** gamora (simulation seam)
**Date:** 2026-07-08
**Mode:** $0 read-only forensic diagnosis. NO gauntlet run, NO code change. Existing artifacts + source only.
**Trigger:** closes the R3a step-4 diagnosis loop. gandalf's §4 FAIL verdict + next-move note traced the step-function surface one layer below the two authorized (tier-2) levers: open_arena + chokepoint_corridor **reject at tier-1** (`_route_tier_1` band_override → `TIER_1_REJECT → continue`), so a tier-2 engagement lever structurally could not move them. gandalf's hypothesis: the tier-1 KPM band is a fourth inherited-uncalibrated gate (Discipline #13 drift). This note answers the binary for Matt's re-band-vs-Option-C fork.
**Artifacts / source read:** `output/cycle-13-gauntlet-sim-results-20260708_065352.json` (1197 encounter_results); `gauntlet_sim.py:300-442` (ENCOUNTER_COHORT_KPM_BAND) + `:1232-1288` (band lookup + REJECT `continue`); `t4_sim_cycling.py:_route_tier_1 :699-766`; my step-4 forensics `b87d394`; gandalf verdict `988663e`; git-blame of the band lines.

---

## 1. What band, and how far off — QUANTIFIED

The run gates tier-1 against **`ENCOUNTER_COHORT_KPM_BAND`** (`gauntlet_sim.py:1237`, the `_T1_BAND_OVERRIDE_ENC_TYPES` path — mobs/min, per-shell cohort-invariant). The two rejected shells' bands (`:434-435`):

| shell | tier-1 band (lo, hi) | observed KPM p10 / med / p90 | in-band | **direction** |
|---|---|---|---|---|
| open_arena | (9.90, **15.53**) | 22.3 / 31.9 / 53.8 | **0 / 252** | 100% ABOVE ceiling |
| chokepoint_corridor | (11.65, **15.88**) | 23.3 / 35.2 / 57.1 | **0 / 189** | 100% ABOVE ceiling |

**The miss is NOT "kits can't clear."** Every one of the 441 cells rejects by being **ABOVE** the ceiling — min observed 18.1 (open) / 16.8 (choke), both already over their `hi`. The kits clear these rooms **too fast**: median KPM is **2.05×** the open_arena ceiling and **2.22×** the chokepoint ceiling. Corroborated by the raw R2-calibration warns (`w3_batch1_run_log.txt`): open_arena / chokepoint WR=1.000 ceiling on the same shells — trivially cleared, not failed. This is a throughput-over-ceiling rejection, the exact opposite of non-viability (which would read as WR-floor / KPM-below-floor).

## 2. Provenance — last calibrated 2026-06-16, never re-based after the 2026-07-07 re-population

Git-blame on `gauntlet_sim.py:434-435`: both band lines last written **2026-06-16 23:37** (commit `92c040f`, "KPM-band spatial recalibration Stage-2d"). The header (`:402-405`) states the fit is anchored to the **2026-06-16 determined-slice population** (`kpm-band-spatial-recal-full-20260616_232152.json`) and self-flags: *"RE-FIT CANDIDATE if MOB_HP_DIFFICULTY_MULTIPLIER changes."* Since then the room population changed underneath it:
- **F2 full-pop re-lock — commit `59dc832`, 2026-07-07 16:52** (mob-population / mob_damage_scale re-lock).
- **MOB_HP un-stack + serial-engagement — commit `e649659`, 2026-07-08 02:28** (the R3a step-3 levers).

The band was fit to the pre-re-population room, never re-based for it. That is precisely the Discipline #13 inherited-uncalibrated-constant shape gandalf named — same family as §1's three constants, one gate deeper.

## 3. Re-band signature confirmed (not viability)

A plain p10/p90 re-fit to the **current** KPM distribution — the same estimator that produced the existing band — would in-band **203/252 = 81%** (open) and **153/189 = 81%** (choke). The whole distribution shifted up roughly ×2 and stayed a coherent single mode; it did not fracture into a can't-clear tail. Fix = re-fit two band tuples (open_arena, chokepoint_corridor rows, `gauntlet_sim.py:434-435`); the `_route_tier_1` predicate is untouched — the same one-constant shape as the un-stack.

## BOTTOM LINE — the binary

**(a) MIS-CALIBRATED TIER-1 BAND — a cheap re-band. Applies to BOTH scenarios identically.** open_arena and chokepoint_corridor reject 100% ABOVE their tier-1 KPM ceilings (median 2.0–2.2× hi, 0 cells below), because the band (`ENCOUNTER_COHORT_KPM_BAND["open_arena"]=(9.90,15.53)`, `["chokepoint_corridor"]=(11.65,15.88)`, `gauntlet_sim.py:434-435`) was last fit 2026-06-16 and never re-based after the 2026-07-07 F2 re-population + 2026-07-08 un-stack raised clear throughput. A p10/p90 re-fit to the current distribution recovers 81% in-band on both — the drift signature, not a viability tail. **Field(s) to change: the two band tuples at `gauntlet_sim.py:434-435` (open_arena + chokepoint_corridor rows).** This is a re-band of the same one-constant class as the un-stack, NOT Option-C. There is **no evidence of genuine kit non-viability** on either scenario — the failure mode is over-clear (WR-ceiling / KPM-over-band), the inverse of non-clear.

*(Per dispatch: diagnosis only. No change made, none recommended — this lands the (a)-vs-(b) binary for Matt's re-band-vs-Option-C fork.)*
