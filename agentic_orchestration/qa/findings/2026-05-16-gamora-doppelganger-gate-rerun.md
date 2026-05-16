# Findings — gamora — Doppelganger gate re-run (post-B14.5 V1 trigger condition)

**Date:** 2026-05-16
**Author:** gamora
**Status:** COMPLETE
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-gamora-doppelganger-gate-rerun.md`
**Signal class:** HIGH

---

## 1. State verification

### Engine HEAD

Current HEAD: `5d51b5a` (docs: decisions-log — form-bias cadence strategy 5-entry batch)

Ancestry confirmed:
- `b15ecb2` (B10.4 Option 2 — convergence binary-search excludes pack fights): ancestor of HEAD — YES
- `639ac3d` (B6 pre-work — energy-type-aware skill tier assignment): ancestor of HEAD — YES
- `9db2f5a` (B10 V2 — sequential-room semantics with HP/energy/cooldown carryover): ancestor of HEAD — YES

All three required commits are in HEAD. State verification PASSES.

### Season_001005 generation provenance

`season_001005` was generated at engine version `b15ecb2` (2026-05-16 07:05:53 UTC), which is the B10.4 Option 2 commit. The B6 pre-work (`639ac3d`) and B10 V2 (`9db2f5a`) landed at 19:29 and 19:40 UTC respectively — approximately 12 hours AFTER the season regen. The season classes were generated on the pre-B6 substrate.

The fresh regen commissioned by star-lord's 2026-05-16 dispatch ran at the same `b15ecb2` version (it landed at 07:05 UTC, confirmed by the completion record). No regen of season_001005 has occurred since B6 pre-work or B10 V2 landed.

**Status:** Season_001005 was NOT re-generated under the B6 energy-type-aware tier system or B10 V2. The doppelganger gate data reflects the B10.4 Option 2 class substrate only.

### Variance setting

Per-fight variance at ±25% is confirmed active (the setting from KI-B6-1 resolution, unchanged since). Gate ran with this setting as required.

---

## 2. V2-semantic alignment — FINDING (primary cross-seam flag)

The doppelganger gate (`_evaluate_doppelganger()`) runs encounter-level mirror fights using `simulate_fight()`. It does NOT use room-level semantics and never has. Under V2 (B10 V2), `use_room_evaluation=True` changes the BINARY SEARCH convergence metric to per-room non-pack WR — but the doppelganger gate is called AFTER binary search completes and is a separate code path.

**Verified by inspection:** `_evaluate_doppelganger()` is identical at `b15ecb2` and HEAD (`5d51b5a`). No diff in the function or its constants (DOPPELGANGER_HP_BONUS, DOPPELGANGER_DMG_BONUS, DOPPELGANGER_BALANCED_RANGE, DOPPELGANGER_MODIFIER_FLOOR) between those two commits. The function calls `simulate_fight()` per encounter, not `simulate_room()`.

**V2-semantic alignment status: NOT APPLICABLE.** The gate does not have a V2-aware room-level analog — it is inherently encounter-level. This is NOT a bug; it is by design. The gate's question — "can this class beat a slightly stronger version of itself in a 1v1 encounter?" — is orthogonal to the room-carryover question the balance loop binary search targets.

**Flag for knight-rider:** The gate's encounter-level WR is consistent with the memory note's signal thresholds, which were also defined against encounter-level WR (the original KI-B6-1 measurement was encounter-level). No semantic mismatch between gate output and threshold definitions. However, a V2-aware doppelganger gate (room-level mirror match: class must win a 3-encounter room against its doppelganger) would be a meaningful extension post-V2 full regen. This is OUT OF SCOPE for this dispatch per the explicit "do NOT extend the gate infrastructure" constraint; surfaced as a potential future small dispatch.

---

## 3. Per-class doppelganger WR data

Gate configuration: 3 bands (L17, L33, L50); fights_per_band = fights_per_matchup // 2 (from non-smoke invocation); alternating initiative; DOPPELGANGER_HP_BONUS = 1.05; DOPPELGANGER_MODIFIER_FLOOR = 0.30.

| Class | Archetype | Element | Modifier | Status | L17 WR | L33 WR | L50 WR | Avg WR | Gate |
|---|---|---|---|---|---|---|---|---|---|
| class_0001 | hybrid_mage | fire | 0.1094 | CONVERGED | 0.52 | 0.42 | 0.46 | 0.467 | PASS |
| class_0002 | hybrid_mage | water | 0.0945 | CONVERGED | 0.46 | 0.42 | 0.40 | 0.427 | PASS |
| class_0003 | earth_controller | earth | 0.1094 | INTENTIONAL_OUTLIER | 0.44 | 0.56 | 0.42 | 0.473 | PASS |
| class_0004 | hybrid_mage | wind | 0.1094 | CONVERGED | 0.50 | 0.46 | 0.46 | 0.473 | PASS |
| class_0005 | physical_warrior | physical | 0.5250 | CONVERGED | 0.40 | 0.46 | 0.48 | 0.447 | PASS |
| class_0006 | fire_controller | fire | 0.1688 | CONVERGED | 0.36 | 0.46 | 0.36 | 0.393 | PASS |
| class_0007 | water_controller | water | 0.2281 | CONVERGED | 0.40 | 0.38 | 0.40 | 0.393 | PASS |
| class_0008 | hybrid_mage | earth | 0.1391 | INTENTIONAL_OUTLIER | 0.52 | 0.46 | 0.44 | 0.473 | PASS |
| class_0009 | wind_controller | wind | 0.1688 | CONVERGED | 0.58 | 0.38 | 0.50 | 0.487 | PASS |
| class_0010 | experimental | physical | 1.0000 | CONVERGED | 0.54 | 0.42 | 0.54 | 0.500 | PASS |
| class_0011 | experimental | fire | 0.0723 | INTENTIONAL_OUTLIER | 0.54 | 0.48 | 0.50 | 0.507 | PASS |

**All 11 classes pass the gate** (DOPPELGANGER_BALANCED_RANGE = [0.20, 0.80]).

---

## 4. Pure-control archetype summary

From the archetype-gradient table in `qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`, the four pure-control archetypes are: wind_controller, fire_controller, earth_controller, water_controller.

| Archetype | Element | Avg WR | Band | Memory-note signal |
|---|---|---|---|---|
| wind_controller | wind | 0.487 | 30-50% | HIGH |
| earth_controller | earth | 0.473 | 30-50% | HIGH |
| fire_controller | fire | 0.393 | 30-50% | HIGH |
| water_controller | water | 0.393 | 30-50% | HIGH |

All four pure-control archetypes are in the 30-50% band defined by the memory note as the HIGH signal condition.

**Fight termination analysis:** Across all pure-control archetype gauntlet fights in season_001005 (earth_controller: 6,000 fights; fire_controller: 4,800; water_controller: 6,000; wind_controller: 4,800), the timeout rate is effectively 0.0% (one timeout across 21,600 fights). This is a complete reversal from the original KI-B6-1 crisis where wind_controller had 0 knockouts in 60 fights (100% timeout). The ±25% per-fight variance setting, combined with B14.5 V1 recompose-first kit shaping, has given controllers enough damage signature that fights resolve via KO, not timeout attrition.

---

## 5. Signal classification

**SIGNAL: HIGH**

The memory note (`project_ailment_damage_thematic.md` § "Trigger conditions to revisit") states:

> "Post-B14.5 (highest signal): Re-run doppelganger gate at the current ±25% variance setting. If wind_controllers (and other pure-control archetypes) now land at 30-50% win rates because B14.5 composed more damage into their kits → thematic damage is solved at a different layer; defer indefinitely or downgrade to pure design polish item."

All four pure-control archetypes (wind: 0.487, earth: 0.473, fire: 0.393, water: 0.393) land in the 30-50% range. The HIGH signal condition is cleanly met with no ambiguity.

The memory note's Medium signal condition (20-25%) and Urgent signal condition (<20% or >60%) are not triggered.

---

## 6. Cross-component attribution caveat (Discipline #13b)

The gate result reflects the COMPOUNDED effect of B14.5 V1 (recompose-first balance loop) + B6 pre-work (energy-type-aware tier assignment — though this affected the GENERATOR for future seasons, not the current season_001005 class substrate which predates B6) + B10 V2 (sequential-room convergence semantics, which affected binary-search convergence but not the gate itself). The fraction attributable to each work item is NOT isolated here and is NOT in scope for this dispatch.

Specific attribution note: the season_001005 classes were generated BEFORE B6 pre-work landed (B6 changed the class generator; season_001005 classes are pre-B6 in their skill tier calibration). The gate result is therefore most directly attributable to B14.5 V1 (recompose-first kit shaping at the B10.4 Option 2 convergence level). B6 and B10 V2 are part of the "compounded stack" in terms of engine state at measurement time, but did not alter the class substrate or the gate function itself.

---

## 7. Recommendation for knight-rider

### Deferral status

Per the memory note's HIGH signal path: **ailment-damage-signatures deferral STAYS — extend to indefinite.**

The memory note specifies: "Thematic damage is solved at a different layer; defer indefinitely or downgrade to pure design polish."

B14.5 V1's recompose-first balance loop has composed enough damage into controller kits that they operate in the healthy 30-50% mirror-match WR range without needing ailment-damage secondary signatures. The structural problem (control ailments carrying zero damage signature → variance machinery has nothing to act on) has been effectively addressed at the kit-composition layer rather than the ailment-mechanics layer.

### Recommended decisions-log entry shape (HIGH signal path)

Knight-rider should draft a decisions-log entry with the following shape:

- **Decision title:** Ailment-damage-signatures design — deferral extended to indefinite (HIGH signal per doppelganger gate re-run)
- **Content:** Doppelganger gate re-run post-B14.5 V1 confirms HIGH signal (all four pure-control archetypes at 38-49% average mirror-match WR). The recompose-first balance loop has dissolved the original urgency. Deferral extended to indefinite per memory note § "Trigger conditions to revisit" HIGH signal path. Demote to design-polish queue (not engineering queue). Entry 2 of the 2026-05-16 form-bias decisions-log batch retains "Future" framing consistent with this finding.
- **Status:** Active — replaces the provisional "Future" framing on the ailment-damage-signatures item in Entry 2 of 2026-05-16 batch with a firm deferral-indefinite classification.
- **Related:** `project_ailment_damage_thematic.md`; doppelganger gate findings (this file); form-bias cadence strategy § 9.1; 2026-05-16 form-bias decisions-log batch Entry 2.

### V2-semantic flag for knight-rider

As noted in §2: the doppelganger gate does not have a room-level V2 analog. If a future dispatch commissions a V2-aware doppelganger gate (room-level mirror match), it should be a separate small gamora dispatch. The current encounter-level gate is the operative measurement instrument and its thresholds are defined against encounter-level WR — no mismatch.

---

## 8. What did NOT change

- No code changes to any production file
- No MIGRATION.md entry (no schema changes)
- No tag cut (analysis-only per dispatch)
- No modifications to doppelganger gate infrastructure (out of scope per dispatch)

---

*Findings complete — 2026-05-16. Author: gamora.*
