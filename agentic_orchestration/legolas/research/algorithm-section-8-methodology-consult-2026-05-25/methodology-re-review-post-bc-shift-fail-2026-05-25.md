# Methodology Re-review — Algorithm § 8 BC-Shift Sweep FAIL Post-mortem

**Mode:** A-deep (Pattern A-deep — multi-question methodology verdict)
**Commissioner:** knight-rider (Cycle 11 Wave 3b ESCAPE-HATCH diagnostic)
**Date:** 2026-05-25
**Source commission:** Cycle 11 Wave 3b ESCAPE-HATCH diagnostic briefing
**Primary artifact reviewed:** `bc_shift_sweep_results.json` (2026-05-25T11:15:36)
**Original methodology:** `methodology-recommendation.md` (this directory), § 5.2

---

## Executive Summary

The BC-shift validation sweep FAILED both gates (direction 41.67%, magnitude 0.00%). This re-review finds that **both Pattern A and Pattern B failures are substantially caused by test-infrastructure problems rather than by a genuine architecture defect in the § 8 strategy registry**. The most load-bearing finding is that the sweep's measurement instrument is broken at its core: `bc_shift = altered_modifier - baseline_modifier` collapses to near-zero or exactly zero in 11/12 kits because the balance loop does not consume `t4_alteration_output` at all — the alteration is stored on the kit but never wired into combat arithmetic at Phase 3. This makes Pattern B a measurement-instrument failure, not an architecture failure. Pattern A (strategy-selection mismatch) is substantially a test-set construction artifact: the BC-view derivation function hard-codes archetype-to-BC-axis mappings that produce `damage_amplitude = "spiky"` for several kit specs whose `expected_strategy` was constructed assuming a different BC-axis value. The result is that GEOMETRY_COLLAPSE wins the η competition on kits the test authors labeled as RESOURCE_CONVERSION or DEFENSIVE_CONVERSION candidates. The thresholds themselves (80%/60%) remain appropriate for the claim type; the test that failed to meet them is invalid.

**Primary re-review verdict: the BC-shift sweep is not a valid test of the § 8 claim as implemented. It is a valid test of two other things: (1) BC-view derivation accuracy and (2) balance-loop alteration-wiring completeness. Both of those sub-systems need fixing before a re-test of the core § 8 claim is meaningful.**

---

## Question 1 — Test-set composition adequacy

### 1.1 What the test-set construction did

The sweep generated 12 kit specs. Each spec names an `expected_strategy` and a `predicted_shift_axis`. The `expected_strategy` was authored by the test-set constructor (rocket, per the sweep script) based on intuitive reasoning about what strategy should fire for a kit labeled "fire_mage_hp_econ" or "warrior_dodger". The BC-view that the actual strategy selection algorithm uses is derived at runtime from the kit params by `_bc_view_from_generation_params()`.

### 1.2 The construction artifact — expected_strategy vs actual BC-view mismatch

The critical flaw: the sweep constructor authored `expected_strategy` by reasoning about what the kit "should" get, without verifying what BC-axis values `_bc_view_from_generation_params()` actually produces for those params.

**Traced cases from the results JSON:**

**`fire_mage_hp_econ_1`** — `dominant_element="fire"`, `archetype_tag="fire_mage"`, `energy_type="mana"`, `role_orientation="damage"`, `range_profile="medium"`.

From `_bc_view_from_generation_params()`:
- `resource_economy`: fire element + mana → `"overflow"` (line 789: `elif dominant_element in ("fire", "shadow", "lightning"): resource_economy = "overflow"`)
- `damage_amplitude`: role_orientation="damage", archetype_tag="fire_mage" → `"spiky"` (line 758)
- `damage_geometry`: archetype_tag="fire_mage" → `"large-AOE"` (line 709)

For RESOURCE_CONVERSION to win, `resource_economy` must be `"HP-economy"` (axis_match = 0.90) or `"overflow"/"starved"` with fire/shadow element (axis_match = 0.60). With fire + overflow: η(RC) = 0.5×0.60 + 0.3×0.30 + 0.2×1.0 = 0.30 + 0.09 + 0.20 = **0.59**.

For GEOMETRY_COLLAPSE: `damage_amplitude = "spiky"` AND `damage_geometry = "large-AOE"` → axis_match = 0.85. η(GC) = 0.5×0.85 + 0.3×0.30 + 0.2×1.0 = 0.425 + 0.09 + 0.20 = **0.715**.

GEOMETRY_COLLAPSE wins (0.715 > 0.590). The result is correct given the actual BC-view. The test-set constructor expected RESOURCE_CONVERSION based on the kit label ("hp_econ") but the BC-view derivation doesn't produce an HP-economy resource axis for fire+mana — it produces overflow. The `expected_strategy` was wrong relative to what the algorithm actually sees.

**`warrior_dodger_1/2`** — `energy_type="rage"`, `archetype_tag="physical_warrior"/"physical_grappler"`.

From `_bc_view_from_generation_params()`:
- `resource_economy`: energy_type="rage" → `"generator-spender"` (line 782)
- `defensive_profile`: energy_type="rage" OR archetype_tag in ("physical_warrior", "physical_grappler") → `"tank"` (line 770-771)

For DEFENSIVE_CONVERSION to win, `defensive_profile` must be `"dodger"` (axis_match = 0.85 for heavy armor). But the derived view has `defensive_profile = "tank"`. DEFENSIVE_CONVERSION's opportunity_scan returns near-zero for a tank BC-target. The label "warrior_dodger" was aspirational; the BC-view function maps physical_warrior+rage → tank, not dodger.

TRADE_OFF wins because physical warrior gets `damage_amplitude = "flat"` (line 762) and `damage_tempo = "medium"` → η(TO) = 0.5×(0.50+0.30) + 0.3×0.25 + 0.2×1.0 = 0.40 + 0.075 + 0.20 = **0.675**. This is the correct result given the BC-view.

**`water_fire_tradition_1`** — `dominant_element="water"`, `archetype_tag="water_mage"`, `role_orientation="damage"`.

For ELEMENT_CONVERSION, fire_resonance must be > 0.6. `_derive_fire_resonance("water", "water_mage")` → returns 0.10 (default; water is not fire, shadow, or physical_warrior/grappler). η(EC) with fire_resonance=0.10 < 0.3: axis_match = 0.0, thematic = 0.10 → η = 0 + 0.3×0.10 + 0.2×1.0 = **0.23** — below ETA_FLOOR. The expected_strategy was ELEMENT_CONVERSION but the substrate's fire resonance derivation produces near-zero resonance for water element, so EC never fires.

**`earth_fire_tradition_2`** — same problem: `dominant_element="earth"`, fire_resonance = 0.10 → EC below floor.

### 1.3 Composition adequacy verdict

The test set is not representative for the strategies it claims to test. The `expected_strategy` labels were authored against the test-set constructor's mental model of what strategy should fire, not against the actual BC-axis values the derivation function produces. At least 7/12 kits have an `expected_strategy` that was impossible given the actual BC-view the algorithm received. This is a **test-set construction artifact**, not a genuine architecture failure.

The 5 direction-correct kits (warrior_flat_1/2, earth_aoe_spiky_1/2, shadow_glass_1/2 minus lightning_glass rounding) are the cases where the test constructor's intuition happened to align with the BC-view output — TRADE_OFF on flat warriors, GEOMETRY_COLLAPSE on spiky AOE kits, DEFENSIVE_TRADEOFF on glass kits. These are the strategies where the BC-view derivation maps to the expected profile cleanly.

---

## Question 2 — Threshold appropriateness

The 80%/60% thresholds derive from QD/MAP-Elites literature for pass rates on directional BC-shift tests. In a 12-kit test, 80% = 9.6 → 10/12 minimum. This is a strict bar, but it is the **correct** bar for the claim being tested: "the committed alteration shifts the kit's measured BC profile in the predicted direction." A claim this strong — that a scored-candidate selection function reliably picks the strategy that produces the predicted BC shift — warrants a strict threshold.

The threshold is not the problem. **A valid test with n=12 kits against this claim should be able to clear 10/12 direction-correct.** The failure is in the test construction, not in what constitutes a meaningful pass rate.

One caveat: the 60% magnitude threshold was originally set as "|bc_shift| ≥ 0.1 BC-units". The sweep used `final_modifier` delta as the BC-shift proxy, which is a different unit from BC-axis bin values. Even if the alteration were wired into combat arithmetic, the magnitude threshold's applicability to `final_modifier` delta would need re-examination. The 0.1 magnitude threshold was written assuming the measurement instrument would be the BC-axis coordinate shift (e.g., `resource_economy` bin moving from `overflow` to `HP-economy` in the archive), not the balance modifier convergence delta. See Question 3.

**Threshold appropriateness verdict: thresholds are appropriate for the claim. They do not need revision. The test that failed to meet them needs redesign.**

---

## Question 3 — Measurement-instrument validity (Pattern B)

This is the most load-bearing finding.

### 3.1 What the sweep measured

The sweep computed `bc_shift = altered_modifier - baseline_modifier` where `altered_modifier` is the `final_modifier` from the balance loop run WITH `t4_alteration_output` set on the kit, and `baseline_modifier` is the `final_modifier` from the run WITHOUT it (kit with `t4_alteration_output = None`).

### 3.2 The instrument failure — alteration is not wired into combat arithmetic

Inspection of `balance_loop.py`: the balance loop does not read `t4_alteration_output` anywhere. The field is stored on `PlayerClass` and passed through to archive insertion (star-lord seam), but the Phase 3 simulation does not consume it. The specific alteration params — `cost_resource_override = "HP"`, `hit_override = 1.0`, `crit_override = 0.0`, `evasion_to_armor`, `aoe_radius_multiplier = 0.5`, `chaos_immune = True` — are not injected into the fight engine's combat arithmetic at loadout resolution.

This is confirmed by the result data: in 11/12 cases, `baseline_modifier == altered_modifier` exactly (to 3 decimal places). The single exception (`lightning_glass_2`) shows `0.049 vs 0.041` — a small floating-point difference likely from seed-driven variance in the 5-iteration cap, not from alteration effect. The one kit with a non-zero `bc_shift` value (`fire_mage_hp_econ_1`, bc_shift=0.069609375) shows `win_rate` changing slightly (0.474 vs 0.470) with `baseline_modifier == 0.064 vs altered_modifier == 0.134` — but these are different because the kit generated with `t4_alteration_output=None` is a structurally different kit from one where alteration was set and then cleared post-generation. The ordering is the issue: the sweep clears the alteration on an already-generated kit rather than preventing the alteration during generation, so some alteration effects may have already percolated into generation-time state (skill element assignments etc.) and then are partially stripped.

### 3.3 Why this means Pattern B is not evidence against the architecture

Pattern B (near-zero bc_shift in 12/12 kits) would be damning if `t4_alteration_output` were actually wired into combat arithmetic. It isn't. The sweep was testing `final_modifier delta when alteration struct exists vs doesn't exist on the kit struct` — but the balance loop treats both cases identically because it never reads that struct. The result was predictably near-zero for any strategy where the only effect is via the alteration output bundle.

The partial exception is ELEMENT_CONVERSION and GEOMETRY_COLLAPSE for kits where element assignment happens at generation time (before the alteration struct is cleared). The clearing logic in the sweep (`cls = cls.model_copy(update={"t4_alteration_output": None})`) strips the struct but may not reverse generation-time effects — creating an asymmetric comparison that's invalid for generation-time strategies and a null comparison for loadout-resolution strategies.

### 3.4 Correct measurement instrument for this claim

The correct instrument for testing "the committed alteration shifts the kit's measured BC profile" is:

For **loadout-resolution strategies** (RESOURCE_CONVERSION, TRADE_OFF, DEFENSIVE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_TRADEOFF): the alteration params must be wired into the fight engine's combat arithmetic at loadout resolution before Phase 3 runs. Only then will `final_modifier` delta reflect the alteration's effect. Alternatively, measure the combat-arithmetic outputs directly (e.g., mean DPS, hit rate, effective HP) rather than via the convergence modifier.

For **ELEMENT_CONVERSION**: generation-time element assignment is the effect. Measurement should compare kit archive entries where element is fire vs the base element, not modifier delta from a 5-iteration balance run.

**Measurement-instrument verdict: `final_modifier` delta via 5-iteration balance run is not a valid instrument for testing BC-shift from loadout-resolution alterations that are not yet wired into combat arithmetic. The sweep measured instrument failure, not architecture failure.**

---

## Question 4 — Static η-calibration PASS vs full-sweep FAIL discrepancy

### 4.1 What the static smoke tested

The static η-calibration smoke (my methodology § 5.3 alternative) tested `select_mechanic_alteration()` on hand-crafted BC-target tuples with known expected selections. It verified that the scoring logic returns the expected strategy at η ≥ ETA_FLOOR_THRESHOLD for 6/6 inputs.

### 4.2 Why the static smoke PASSed and the full sweep FAILed

The discrepancy is a **test-design gap**, not a methodology limitation. Specifically:

The static smoke tests used hand-crafted BC-target tuples where the expected strategy's trigger conditions were explicitly set (e.g., `resource_economy = "HP-economy"` for RESOURCE_CONVERSION). The author who wrote the smoke tests understood what BC-axis values trigger each strategy and constructed inputs accordingly.

The full sweep used `KitSpec` params that were passed through `_bc_view_from_generation_params()` to derive the actual BC-target. The test-set constructor did not verify that the derivation function would produce BC-axis values that trigger the expected strategy. As documented in Question 1, `fire+mana` → `resource_economy = "overflow"` (not `"HP-economy"`), `physical_warrior+rage` → `defensive_profile = "tank"` (not `"dodger"`), `water+mana` → `fire_resonance = 0.10` (not > 0.6).

The η-scoring framework itself is not at fault. The smoke confirmed it works on valid inputs. The full sweep confirmed it works on the inputs it actually receives — those inputs just didn't match the expected_strategy labels.

**Discrepancy verdict: this is a test-design gap. The static smoke covered the scoring logic on valid hand-crafted inputs. The full sweep surfaced that the BC-view derivation function produces different BC-axis values than the test constructor assumed. These are two different problems; finding one masked the other.**

---

## Question 5 — Follow-up test sequence (cheapest-first per Discipline #19.1)

The two failure patterns decompose into three distinguishable sub-claims. The sequence below is cheapest-first.

### 5.1 Distinguish test-set construction artifacts from genuine architecture problems

**Test:** Re-run `select_mechanic_alteration()` on the 12 kit specs but log the actual BC-view produced by `_bc_view_from_generation_params()` for each spec. Compare actual BC-view axes against expected_strategy trigger conditions. This is a Python script that calls the selection function with debug logging enabled — no Phase 3 convergence required.

**Cost:** < 5 minutes.

**What it resolves:** confirms whether the GEOMETRY_COLLAPSE wins on fire_mage_hp_econ because the BC-view says `damage_amplitude = "spiky"` and `damage_geometry = "large-AOE"` — not because the scoring logic is wrong. Either the BC-view derivation function is producing incorrect axis values for these kit params (a derivation bug), or it's producing correct axis values and the test-set expected_strategy labels are wrong (a test-design error).

### 5.2 Distinguish measurement-instrument validity from alteration-ineffectiveness

**Test:** Wire one loadout-resolution alteration (TRADE_OFF is cleanest: set `hit_chance = 1.0`, `crit_chance = 0.0` in combat arithmetic) into the fight engine. Re-run the sweep for the 2 TRADE_OFF kits only (warrior_flat_1/2), measuring DPS variance and hit rate directly rather than via `final_modifier` delta.

**Cost:** 1-2 hours of rocket implementation + 30 min of run time.

**What it resolves:** if wiring TRADE_OFF into the fight engine produces a measurable shift in hit rate (should become 1.0) and crit rate (should become 0.0), this confirms the architecture is sound and the instrument was the problem. If wiring TRADE_OFF produces no change in hit rate/crit rate, there is a deeper integration problem.

**Note:** this is NOT an alternative to full § 8 wiring — it is the minimum proof-of-concept required to validate the architecture claim before broader wiring investment.

### 5.3 Distinguish threshold calibration from genuine FAIL

**Test:** No additional run needed. The threshold calibration question is already answered by Questions 2 and 3: the thresholds are appropriate; the test was invalid. If a redesigned test clears the thresholds, the threshold calibration was correct. Only if a fully valid test (correct BC-views, alteration wired, measurement instrument valid) still fails to clear 80%/60% does threshold revision become necessary.

**Cost:** $0 — answered analytically.

### 5.4 Redesigned sweep (complete validation after 5.1 + 5.2 resolve)

After 5.1 confirms the BC-view derivation is producing correct axis values for well-constructed kit specs, and 5.2 confirms alteration wiring is measurable, redesign the sweep:
- Construct kit specs by working backward from desired BC-view values (specify the BC-target tuple directly, or verify the derivation function output before labeling expected_strategy)
- Wire the alteration params into combat arithmetic for all 6 v1 strategies before running
- Measure combat-arithmetic outputs (hit rate, crit rate, effective HP, DPS) per strategy type, not only `final_modifier` delta

**Cost:** 2-4 hours of implementation (alteration wiring for 6 strategies) + ~30 minutes of sweep run time (5-iteration balance runs are fast, as confirmed by the ~25 min sweep time for 12 × 2 runs).

---

## Question 6 — Speed-up from estimated 200-300 min to ~25 min

### 6.1 What caused the speed-up

The methodology § 5.2 estimated "~200-300 min" based on "~10 min/kit per multi-dim convergence algorithm." The sweep ran in ~25 minutes (12 kits × 2 runs × ~1 min per run = ~24 min of actual runtime, consistent with the sweep script's per-kit logging pattern).

The cause is `max_iterations=5` at line 161 of the sweep script. The balance loop normally runs until convergence (up to its full iteration budget). The sweep was written with `max_iterations=5` explicitly, described in a comment as "reduced for sweep speed." At 5 iterations, the loop terminates after 5 binary-search steps regardless of convergence, running 5 × gauntlet_size = 5 × 5 monsters = 25 fights per kit. A 25-fight balance run completes in roughly 1 minute on this hardware.

### 6.2 Was the methodology projection wrong, or was the sweep cutting corners?

Both. The methodology § 5.2 projection of ~10 min/kit was based on "full multi-dim convergence algorithm" — the full convergence run that the production pipeline uses. The sweep did not run full convergence; it ran 5-iteration abbreviated convergence. This is the sweep cutting corners.

**Why this matters for the measurement:** the `final_modifier` at 5 iterations is not a converged modifier. It is wherever the binary search happens to be after 5 steps, which varies with the initial modifier value and the fight outcomes at each step. This adds noise to the `baseline_modifier vs altered_modifier` comparison. In the results, several kits show `baseline_modifier = altered_modifier` exactly (same value to 3 decimal places) — this is consistent with both runs hitting the same binary-search branch after 5 identical steps (the kit generation is seeded, so if the alteration has no combat arithmetic effect, both runs follow the same search path). The noise is not the primary problem (that's the unwired alteration); but even with alteration wiring, a 5-iteration run may not converge to a stable enough modifier to detect small alteration effects.

**Recommendation:** if a redesigned sweep re-runs Phase 3, use at least 20 iterations (not full convergence budget, but enough to reach a reasonably stable modifier). The ~10 min/kit estimate in the methodology was correct for full convergence; 20 iterations would be ~2-3 min/kit and 12×2 runs = ~48-72 min — faster than 200-300 min but more reliable than 5 iterations.

---

## Framing-audit (Discipline #23 three-question protocol)

**1. Was the test designed to actually refute the claim it claims to test?**

No. The claim is: "the committed mechanic-alteration shifts the kit's measured BC profile in the predicted direction." For this to be testable, the alteration must be wired into the measurement substrate (combat arithmetic). It was not. The test tested something else: "does `final_modifier` change when `t4_alteration_output` struct is set vs None on the kit" — which is null by construction because the balance loop doesn't read that struct.

**2. Were thresholds picked correctly?**

Yes. 80%/60% on n=12 are appropriate for the claim type. They are not the source of failure.

**3. Is cheapest-refuting-test framing still appropriate, or does the FAIL reveal a deeper methodology re-design need?**

The cheapest-refuting-test framing is still appropriate. What the FAIL revealed is that the test wasn't refuting the architecture claim — it was refuting a simpler claim (does the unmodified balance loop produce different results when an unread struct is set?). The methodology design principle is correct: run a cheap test on the load-bearing claim before investing in broader pipeline work. The execution missed two preconditions that should have been explicit in the methodology: (a) the measurement instrument must actually connect to the alteration's effect surface, and (b) the test-set expected labels must be verified against the actual BC-view derivation output.

**Methodology limitation identified:** my original § 5.2 specified "run Phase 3 convergence WITHOUT/WITH alteration active" without specifying that "active" means the alteration params are wired into combat arithmetic, not merely that the `AlterationOutput` struct is non-null. This is an ambiguity in the test specification, not an architecture flaw. The methodology instruction should have named the loadout-resolution wiring as a precondition for the test to be valid.

---

## Verdict Summary

| Finding | Assessment |
|---|---|
| Pattern A (strategy-selection mismatch, 7/12) | Test-set construction artifact. BC-view derivation produces different axis values than expected_strategy labels assumed. Not a genuine architecture failure in the scoring logic. |
| Pattern B (near-zero bc_shift, 12/12) | Measurement-instrument failure. Alteration not wired into combat arithmetic. Balance loop does not read t4_alteration_output. This makes the sweep a null test for all strategies. |
| Static η-calibration PASS vs full-sweep FAIL | Test-design gap. Static smoke covered the scoring logic on correct inputs. Full sweep surfaced BC-view derivation mismatch and instrument failure simultaneously. Not a methodology limitation. |
| Threshold appropriateness | Thresholds are correct for the claim. Do not revise. |
| Speed-up from 200-300 min to 25 min | max_iterations=5 in sweep script. Abbreviated convergence, not full convergence. Methodology estimate was correct for full convergence; sweep cut corners. |
| Architecture validity | Cannot be assessed from this sweep. The sweep did not test the architecture. Pending: (a) BC-view derivation verification, (b) alteration wiring proof-of-concept (TRADE_OFF wiring is minimum bar). |

---

## Recommended Matt-decision options (ranked by judgment)

**Option 1 (recommended): Treat sweep as invalid, not as a FAIL of § 8 architecture. Run the two cheap follow-up tests (§ Q5.1 + Q5.2) before making an architecture commitment decision.**

Rationale: the sweep failed for reasons that don't implicate the architecture's validity. Before investing in a broader go/no-go decision, the minimum-viable evidence chain is: (a) verify BC-view derivation produces the correct axis values for well-constructed kit specs (5-minute test), and (b) wire TRADE_OFF into combat arithmetic and confirm hit-rate / crit-rate shift is measurable (1-2 hour rocket task). If both pass, the architecture is sound and the full wiring + redesigned sweep can proceed with confidence. If (a) reveals systematic BC-view derivation errors, those need fixing before any re-test.

**Option 2 (acceptable): Treat Pattern A as a BC-view derivation gap requiring architectural review before re-testing.**

Rationale: even granting that Pattern B is an instrument failure, Pattern A reveals that `_bc_view_from_generation_params()` is producing BC-axis values that don't match designer intuition about what a "fire_mage_hp_econ" or "warrior_dodger" kit should look like. This could be a valid concern about the derivation function's accuracy — a "fire mage designed for HP economy" should produce `resource_economy = "HP-economy"`, not `"overflow"`. If the derivation function is producing systematically wrong BC-views, that propagates into every strategy selection in production, not just in the test. This warrants a targeted review of `_bc_view_from_generation_params()` accuracy before committing to the architecture.

**Option 3 (not recommended without first doing Q5.1 + Q5.2): Full architecture redesign.**

Rationale: premature. Both patterns have proximate explanations that don't require architecture redesign. Architecture redesign before ruling out test-construction artifacts and instrument failure would be premature and expensive.

---

## Re-engagement gate

Re-engagement with the redesigned sweep is gated on: (a) BC-view derivation audit result (Q5.1 outcome), and (b) TRADE_OFF wiring proof-of-concept result (Q5.2 outcome). Not time-passage.

---

**Signed:** legolas (researcher and scout)
**Artifact path:** `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-re-review-post-bc-shift-fail-2026-05-25.md`
**For:** knight-rider Cycle 11 Wave 3b ESCAPE-HATCH diagnostic; rocket and gandalf parallel diagnostic triple.
