# Pattern A-deep design-fit critique — Algorithm § 8 BC-shift validation sweep FAIL

**Date:** 2026-05-25
**Author:** gandalf (story-and-design steward)
**Invoking agent:** knight-rider (Cycle 11 Wave 3b ESCAPE-HATCH diagnostic; hive-mind state active)
**Pattern:** A-deep
**Companion diagnostic agents (parallel):** rocket (architecture side), legolas (methodology side)
**Cycle:** 11
**Wave:** 3b ESCAPE-HATCH

---

## 0. Top-line verdict

**Selected option: (a) — architecture is sound; test is misaligned. Recommend test redesign + re-fire; § 8 ships for v1 as-is after the test redesign clears.**

The FAIL is NOT evidence of an architectural problem with § 8. The FAIL is evidence that the cheapest-refuting-test was implemented with a **substituted measurement instrument** that does not measure the load-bearing claim. Specifically:

- The methodology spec (legolas § 5.2) asked: "does the alteration shift the kit's measured BC profile on the predicted axis?"
- The test implementation measured: "does the balance-loop `final_modifier` change between baseline and altered convergence?"
- These are not the same quantity. The substitution was acknowledged inline in the script (`bc_shift_validation_sweep.py:269-272`: *"Using win_rate delta as proxy for BC-shift (actual BC measurement requires the full QD archive pipeline; win_rate shift is the loadout-observable proxy)"*).

The `final_modifier` is the balance-loop's multiplicative scalar adjustment to hit the target win-rate band. It is the wrong instrument for measuring whether a kit's BC coordinates have shifted because:
1. It is a scalar; BC coordinates are an 8-axis vector
2. It is computed by the balance loop AFTER an alteration is already baked into the kit's behavior — its job is to renormalize against alteration, not to surface alteration
3. The balance loop converges modifier to whatever value makes win-rate hit ~50%, which is by construction insensitive to the *kind* of behavior change the alteration produced

Pattern B (magnitude-near-zero) is not an architectural finding. It is a **definitional consequence of using `final_modifier` as the proxy**: if the balance loop successfully re-balances the altered kit (which it largely did — see § 3.2 win-rate evidence), then `final_modifier` will be near baseline by construction, because the loop is doing its job.

Pattern A (strategy-selection mismatch in 7/12) is also not a clean architectural finding. The `expected_strategy` field in `KIT_SPECS` is a **test designer's prior expectation**, not a derivation from the strategy registry's `opportunity_scan` logic. Several of the prior expectations are themselves over-simplifications (see § 4 per-case audit). The 5 cases where η-scoring selected the same strategy the test designer expected are actually a STRONG signal that the η-scoring is working for clean-archetype cases.

**The architecture is intact; the test is the failure surface.** Cycle 11 T4 post-mortem readiness milestone is **NOT at risk** under Option (a); it IS at risk if the FAIL is over-interpreted as architectural and § 8 is re-designed (Option c) instead of the test being re-aligned.

**Discipline check:** I am applying Discipline #23 framing-audit Pattern A-deep three-question protocol explicitly in § 6. The framing the dispatch invocation handed me ("Cycle 11 T4 post-mortem at risk") contained an unstated assumption — that the BC-shift sweep was measuring BC-shift. The empirical refutation (reading the test script) takes ~5 minutes and surfaces the substitution.

---

## 1. The methodology spec vs the test implementation

### 1.1 What legolas § 5.2 specified

Per `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` § 5.2:

> **Procedure:**
> 1. Generate kits using Phase 2 algorithm with § 8 active; record `AlterationOutput` per kit
> 2. Run Phase 3 convergence WITHOUT the alteration active (baseline BC measurement)
> 3. Run Phase 3 convergence WITH the alteration active (altered BC measurement)
> 4. For each kit: compute `bc_shift = altered_bc - baseline_bc` on the axis most predicted to shift
> 5. Verify: for the alteration type committed, the predicted shift direction matches observed shift direction

Steps 2 and 3 are explicit: they require a **BC measurement** — i.e., the kit's 8-axis BC coordinates re-projected from its observed behavior. The "baseline BC measurement" and "altered BC measurement" produce vectors in 8-axis BC-space (per `qd-engine-bc-axes-lock-2026-05-20.md`).

Step 4 then computes the delta on the **predicted axis** (e.g., for resource-conversion, the predicted axis is Axis 5 resource_economy; we expect the kit's resource_economy bin assignment to shift toward `HP-economy`).

### 1.2 What `bc_shift_validation_sweep.py` actually did

Lines 269-276:

```python
# Using win_rate delta as proxy for BC-shift (actual BC measurement requires
# the full QD archive pipeline; win_rate shift is the loadout-observable proxy).
# Win rate shift direction: altered kit should show a shift in the predicted axis
# reflected as a change in convergence behavior (balance_modifier delta).
baseline_modifier = baseline_result.final_modifier if hasattr(baseline_result, 'final_modifier') else 1.0
altered_modifier = altered_result.final_modifier if hasattr(altered_result, 'final_modifier') else 1.0

bc_shift = altered_modifier - baseline_modifier
```

This is a **two-step substitution**:

| Step | Specified | Implemented |
|---|---|---|
| Step 1 (measurement target) | BC vector on predicted axis | Scalar balance-loop modifier |
| Step 2 (refutation comparison) | Shift on predicted axis above magnitude threshold (≥ 0.1 BC-units) | Modifier delta above magnitude threshold (≥ 0.1 modifier-units) |

The inline comment acknowledges the substitution and names a reason ("actual BC measurement requires the full QD archive pipeline"). The reason is real — but the substitution still breaks the test's load-bearing claim.

### 1.3 Why `final_modifier` is the wrong instrument

The balance loop is, per `engineering-disciplines.md` named-pattern "B14.5 V1 primary loop architecture" + `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` Phase 3:

> A convergence loop that adjusts a multiplicative modifier on damage/HP to converge the kit's measured win-rate against a target band (~50%).

The modifier IS the balance loop's adaptive output. Its definitional purpose is to **absorb behavioral variance** in the service of win-rate target. When an alteration changes a kit's behavior:

- **If the alteration changed kit behavior in a way that affects win-rate**, the balance loop adjusts modifier to compensate → modifier shifts.
- **If the alteration changed kit behavior in a way that does NOT affect win-rate** (e.g., shifts the kit's BC-coordinate without changing how often it wins), modifier stays approximately at baseline.

For most well-designed alterations from the § 8 palette, the second case is the GOOD case. A resource-conversion alteration (mana→HP) should change how the kit pays for its skills, change its BC-coordinate on Axis 5 (resource_economy), and produce identifiable Architecture-B-driven thematic identity ("Blood Magic"). But it should NOT necessarily change how often the kit wins fights — the balance loop will rebalance through modifier adjustment to keep win-rate at the target.

**Magnitude-near-zero in 11/12 cases is the predicted outcome of using `final_modifier` as the proxy when the balance loop is working.** This is not an architectural finding. It's the loop doing its job.

---

## 2. Pattern A (strategy-selection mismatch) — per-case audit

The 7/12 mismatch cases need to be examined individually. The "expected_strategy" field is the **test designer's prior** for what the η-scoring should select. Some priors are reasonable; some are over-simplifications.

### 2.1 Strategy-selection results

| Kit | Expected | Actual | Audit |
|---|---|---|---|
| fire_mage_hp_econ_1 | RESOURCE_CONVERSION | GEOMETRY_COLLAPSE | Ambiguous — see § 2.2 |
| shadow_mage_hp_econ_2 | RESOURCE_CONVERSION | DEFENSIVE_TRADEOFF | Ambiguous — see § 2.2 |
| warrior_flat_1 | TRADE_OFF | TRADE_OFF | ✅ match |
| warrior_flat_2 | TRADE_OFF | GEOMETRY_COLLAPSE | Ambiguous — earth_caster has AoE; collapse-to-spike is a reasonable selection |
| water_fire_tradition_1 | ELEMENT_CONVERSION | TRADE_OFF | Test design issue — see § 2.3 |
| earth_fire_tradition_2 | ELEMENT_CONVERSION | GEOMETRY_COLLAPSE | Test design issue — see § 2.3 |
| warrior_dodger_1 | DEFENSIVE_CONVERSION | TRADE_OFF | Test design issue — see § 2.4 |
| warrior_dodger_2 | DEFENSIVE_CONVERSION | TRADE_OFF | Test design issue — see § 2.4 |
| earth_aoe_spiky_1 | GEOMETRY_COLLAPSE | GEOMETRY_COLLAPSE | ✅ match |
| wind_aoe_spiky_2 | GEOMETRY_COLLAPSE | GEOMETRY_COLLAPSE | ✅ match |
| shadow_glass_1 | DEFENSIVE_TRADEOFF | DEFENSIVE_TRADEOFF | ✅ match |
| lightning_glass_2 | DEFENSIVE_TRADEOFF | DEFENSIVE_TRADEOFF | ✅ match |

**5 of 12 are clean matches.** All 5 are the kits where the test-designer prior is unambiguous (warrior_flat_1, earth_aoe_spiky_1, wind_aoe_spiky_2, shadow_glass_1, lightning_glass_2). This is a strong signal that η-scoring works on clean cases.

### 2.2 HP-economy kits (fire_mage_hp_econ_1, shadow_mage_hp_econ_2)

The test designer's prior is: HP-economy kits should select RESOURCE_CONVERSION.

This prior is questionable. Per `skill-system-2026-05-24.md` § 8.3 + legolas § 2.1, RESOURCE_CONVERSION's opportunity_scan trigger is:

> `if bc_target.resource_economy == "HP-economy" OR (bc_target.attribute IN ["INT","WIS"] AND bc_target.defensive_profile != "glass")`

These kits qualify for RESOURCE_CONVERSION, but they ALSO qualify for other strategies (the OR-condition in the scan trigger). The actual selection depends on η-score COMPETITION across all qualifying strategies. If a kit happens to ALSO be a strong GEOMETRY_COLLAPSE candidate (e.g., the kit's geometry+amplitude profile genuinely favors collapse), η-scoring may legitimately prefer it.

**The "expected_strategy" field encodes a test-designer assumption that "HP-economy → ALWAYS RESOURCE_CONVERSION".** That assumption is itself a design oversimplification. The real question for these cases is: does GEOMETRY_COLLAPSE / DEFENSIVE_TRADEOFF make design sense for these specific kit profiles? Without seeing the full kit generation output (skill composition, BC-target details), I cannot say definitively — but the η-scoring's selection is not prima facie wrong. It's just different from the prior.

### 2.3 ELEMENT_CONVERSION kits (water_fire_tradition_1, earth_fire_tradition_2)

The methodology § 2.5 opportunity_scan trigger for ELEMENT_CONVERSION is:

> `if bc_target.element != "fire" AND substrate.cultural_tradition.fire_resonance_score > threshold`

These test cases have non-fire element (water, earth), but they have **no substrate binding** in the test setup (kits are generated via `ClassGenerator.generate()` with element parameter only, no substrate.cultural_tradition signal). The test code does not pass any substrate cultural-tradition that would surface "fire resonance" — the test designer's prior assumes the algorithm would auto-derive fire-resonance from element-element compatibility heuristics, which is not how the methodology specifies the scan should work.

**This is a test design issue, not an architectural issue.** ELEMENT_CONVERSION requires substrate-context per Architecture B (`canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`). The test does not provide it. The η-scoring correctly does not fire ELEMENT_CONVERSION without substrate signal.

### 2.4 DEFENSIVE_CONVERSION kits (warrior_dodger_1, warrior_dodger_2)

The methodology § 2.6 opportunity_scan trigger for DEFENSIVE_CONVERSION is:

> `Axis 4 bin = dodger in BC-target BUT substrate cultural-tradition is heavy-armor-associated`

Same structural problem as ELEMENT_CONVERSION: the trigger requires substrate cultural-tradition context. The test generates these kits without substrate-binding to a heavy-armor cultural-tradition. η-scoring correctly cannot fire DEFENSIVE_CONVERSION without the substrate signal that the trigger requires.

**Both ELEMENT_CONVERSION and DEFENSIVE_CONVERSION test cases are testing the wrong thing**: they're testing whether the algorithm can derive substrate-conditional alterations without substrate. By methodology design, it cannot — that's the Architecture B benefit (substrate-bound at Phase 2) being tested in reverse.

### 2.5 Strategy-selection verdict

Of the 7 "mismatch" cases:

- **2 are arguably correct** (HP-economy kits where η-scoring picked a different but reasonable strategy)
- **4 are test-design-broken** (ELEMENT_CONVERSION + DEFENSIVE_CONVERSION cases that require substrate context the test does not provide)
- **1 is borderline** (warrior_flat_2 / earth_caster with AoE → GEOMETRY_COLLAPSE is reasonable for an AoE-flat kit)

The clean-match rate, properly counted, is actually **5/8** (excluding the 4 substrate-broken cases) = 62.5%. Still below the 80% direction-correct threshold, but **the gap is in test cases that were designed without substrate context, not in the algorithm**.

---

## 3. Win-rate behavior (the genuinely informative signal in the JSON)

While `final_modifier` is the wrong proxy for BC-shift, the raw `baseline_win_rate` and `altered_win_rate` fields ARE informative for a different question: did the alteration actually change the kit's combat behavior at all?

### 3.1 Win-rate deltas per kit

| Kit | baseline_win_rate | altered_win_rate | Δwin_rate |
|---|---|---|---|
| fire_mage_hp_econ_1 | 0.474 | 0.470 | -0.004 |
| shadow_mage_hp_econ_2 | 0.496 | 0.472 | -0.024 |
| warrior_flat_1 | 0.386 | 0.382 | -0.004 |
| warrior_flat_2 | 0.526 | 0.502 | -0.024 |
| water_fire_tradition_1 | 0.500 | 0.492 | -0.008 |
| earth_fire_tradition_2 | 0.250 | 0.246 | -0.004 |
| warrior_dodger_1 | 0.104 | 0.168 | **+0.064** |
| warrior_dodger_2 | 0.486 | 0.514 | +0.028 |
| earth_aoe_spiky_1 | 0.618 | 0.620 | +0.002 |
| wind_aoe_spiky_2 | 0.752 | 0.762 | +0.010 |
| shadow_glass_1 | 0.726 | 0.746 | +0.020 |
| lightning_glass_2 | 0.470 | 0.478 | +0.008 |

### 3.2 What this tells us

The win-rate deltas are **mostly within ±2-3%**, which is consistent with: the balance-loop is mostly converging both kits to approximately their target win-rate band, and the alteration is producing a small residual difference that the loop didn't fully absorb.

**Notable exceptions:**
- `warrior_dodger_1` shifted from 10.4% → 16.8% (+0.064). This is a substantial win-rate change. The alteration (TRADE_OFF: Resolute Technique — never crit, never miss) produced a meaningful behavioral change in this kit; the loop's modifier did not fully absorb it.
- `earth_fire_tradition_2` ran at 25% win-rate baseline → 24.6% altered. The kit is far below win-rate target (50%); the alteration didn't help. This is a kit-generation issue, not a § 8 issue.

**The actually-load-bearing observation**: the alterations ARE changing kit behavior in detectable ways for several kits. The signal magnitude is small for most (because the balance loop is doing its job), but non-zero. The architecture is producing differentiated kits; the test's measurement instrument is insensitive to the differentiation.

### 3.3 Hidden FAIL signal — the kits that didn't reach target win-rate

Several kits never approached the 50% win-rate band even at baseline:

| Kit | Baseline win-rate | Distance from 50% target |
|---|---|---|
| warrior_flat_1 | 0.386 | -0.114 |
| earth_fire_tradition_2 | 0.250 | **-0.250** |
| warrior_dodger_1 | 0.104 | **-0.396** |
| shadow_glass_1 | 0.726 | +0.226 |
| earth_aoe_spiky_1 | 0.618 | +0.118 |
| wind_aoe_spiky_2 | 0.752 | **+0.252** |

The balance loop ran at `max_iterations=5` (line 170) "reduced for sweep speed." With only 5 iterations on kits this far from convergence, the loop never fully resolved any of these. Several kits would need many more iterations to reach the target band. The `final_modifier` for these kits is therefore the loop's intermediate state, not its converged state. **This makes the `final_modifier` an even noisier proxy** than it would be at full convergence.

This is a SECONDARY test-design issue: even within the substituted-instrument framing, the instrument was used in a poorly-converged regime. Re-firing at higher `max_iterations` would change the modifier values but probably not the architectural conclusion (still wrong instrument).

---

## 4. Per-question structured answer

### Q1: Is the test asking the right question?

**No.** The test is asking: "does the balance-loop final modifier change between baseline and altered runs?" The load-bearing § 8 design claim is: "does the algorithmically-derived alteration shift the kit's BC profile in a predicted direction, producing per-kit differentiation in the BC-coordinate space?"

These are different questions. The test's question can be answered "no" even when the design claim is true (balance loop absorbs the behavioral variance into modifier baseline; BC coordinates shift while modifier doesn't).

The right test would measure the kit's BC coordinates on the predicted axis at baseline vs altered. That requires re-projecting the kit's observed behavior into 8-axis BC space. Per the inline comment, doing so "requires the full QD archive pipeline" — which is the actual architectural infrastructure for BC measurement.

### Q2: Is "expected_strategy" a test artifact or genuine design failure?

**Mostly test artifact, partly genuine design oversimplification.**

The "expected_strategy" field encodes a test designer's prior. Of the 7 mismatch cases:
- 4 require substrate context the test does not provide (ELEMENT_CONVERSION + DEFENSIVE_CONVERSION) — pure test artifact
- 2 are cases where the prior assumes a single-axis trigger (HP-economy → RESOURCE_CONVERSION ALWAYS) when the methodology's opportunity_scan supports multiple competing strategies — partly oversimplification, but the η-scoring may still be working correctly
- 1 is borderline (warrior_flat_2 → GEOMETRY_COLLAPSE is reasonable for an AoE-flat kit)

The HP-economy → RESOURCE_CONVERSION ALWAYS assumption is the most interesting one to interrogate: is the design intent that HP-economy kits should always get blood-magic alteration? Per § 8.3 opportunity_scan_dimensions table, Axis 5 (Resource economy) has multiple alteration patterns available: "Convert mana→HP cost; convert STR→DEX scaling; share resource between actives." Plus, kits with HP-economy ALREADY exist in a particular resource regime — converting again may be a redundant alteration. The η-scoring's selection of GEOMETRY_COLLAPSE for fire_mage_hp_econ_1 might reflect: "this kit is already HP-economy; the highest-η alteration opportunity is on geometry, not resource." That's a legitimate design read.

### Q3: Is the magnitude-near-zero pattern an architecture problem or a test-measurement problem?

**Test-measurement problem, fully.** Per § 1.3 above:

The 6 loadout-resolution-only strategies (resource-conversion, trade-off, element-conversion, defensive-conversion, geometry-collapse, defensive-tradeoff — see legolas § 3.4) modify build-time stat properties. They do not modify the balance-loop modifier. They modify the kit's combat-arithmetic in ways that the balance loop then renormalizes against. By construction, `final_modifier` is the wrong instrument to detect their effect.

The 4 sim-extension strategies (resource-buffer, mechanic-replacement, zone-control, conditional-modifier) would produce per-hit or per-tick behavioral changes that COULD surface in modifier shifts — but the v1 implementation per legolas § 3.4 + dispatch focuses on the 6 loadout-resolution-only strategies, so these aren't in the test.

The test instrument is structurally insensitive to the alterations being tested. The 11/12 zero-magnitude result is the correct output of the substituted measurement, not a finding about the architecture.

### Q4: Design-fit verdict

**Option (a) — Architecture is sound but test is misaligned. Recommend test redesign + re-fire; § 8 ship-as-is for v1.**

Specifically:
1. Test redesign should restore the methodology's actual specification: measure BC coordinates on the predicted axis, not balance-loop modifier
2. The test redesign requires Phase 3 BC-projection infrastructure. If that infrastructure does not yet exist (per the inline comment), the dependency unblocks first
3. Re-fire the sweep with the corrected instrument
4. ALSO: substrate-context test cases (ELEMENT_CONVERSION, DEFENSIVE_CONVERSION) need to be re-designed to provide substrate context per Architecture B
5. ALSO: balance-loop should run to higher convergence (max_iterations > 5) for kits not in baseline win-rate target band

Alternative path if BC-projection infrastructure is not ready and post-mortem timeline matters: use the legolas § 5.3 cheapest-refuting-test alternative — **static η-calibration check**. This tests strategy selection without Phase 3 convergence. ~5 minutes compute. Would surface the strategy-selection correctness question separately from the magnitude question.

I am NOT recommending Option (c) — § 8 re-design. The FAIL does not surface a § 8 architectural issue. The architecture (scored-candidate strategy registry per legolas § 3.1) remains the right pattern.

I am NOT recommending Option (d) — ship § 8 as-is with acknowledged limitations as if the FAIL signal were ambiguous. The FAIL signal is NOT ambiguous — it's a clean test-misalignment finding. We should re-do the test, not ship around it.

I am NOT recommending Option (b) — rocket calibration pass. There may be calibration refinement work to do on η-thresholds (legolas § 9 lists this as a knowledge gap) — but that work depends on having the right measurement instrument first. Calibrating against a wrong instrument doesn't help.

### Q5: Anti-pattern guard — architectural recognition vs scope-discipline test?

**Scope-discipline test.** Per `cycle-11-hive-mind-scope.md` § 5: "Algorithm § 8 BC-shift validation sweep finding 'poor differentiation' — if validation shows the algorithm produces insufficient keystone differentiation, escalate before broader rocket commitment fires." This is the right escalation trigger to have fired.

The escape-hatch DID fire, and that's correct discipline. The question for Matt is now: **is the FAIL signal architectural or test-design?** My read: test-design, decisively. The math reveals refinement need on the TEST, not re-think need on the architecture.

Per scope-discipline § 5.3 anti-pattern guard ("ambiguity defaults in-scope; KR is not over-pivoting on a single empirical signal"), KR is correctly NOT autonomously firing § 8 re-design. KR escalated to Matt via this critique-pair diagnostic, which is right. My role is to surface that the empirical signal is actually about the test, not the architecture, before Matt decides.

---

## 5. Framing-audit (Discipline #23 Pattern A-deep three-question protocol)

Applying the framing-audit explicitly per gandalf OP § 4.1:

| Q | Question | Audit finding |
|---|---|---|
| **Q1** | What load-bearing framing assumptions does this work depend on? | (a) That `final_modifier` proxies for BC-shift adequately. (b) That `expected_strategy` per kit is the authoritative correct selection. (c) That test cases without substrate context can validate substrate-context-dependent strategies. (d) That `max_iterations=5` produces converged balance-loop outputs. |
| **Q2** | What evidence currently in hand (or surfaceable in current scope) could refute these assumptions? | Reading the test script (`bc_shift_validation_sweep.py`) refutes (a) via inline comment (lines 269-272 acknowledge the substitution). Reading the methodology spec (§ 5.2) refutes (a) by showing the spec asked for actual BC measurement. Reading the legolas opportunity_scan triggers for ELEMENT_CONVERSION + DEFENSIVE_CONVERSION refutes (c) by showing the triggers require substrate. Reading the per-kit win-rates refutes (d) — multiple kits are 10-25 percentage points off target band. |
| **Q3** | If refutation evidence exists, is the right move to refine the framing rather than execute the work as-framed? | YES. Refining the framing reveals: the FAIL is about test design, not architecture. Acting on the as-framed interpretation (§ 8 re-design) would be acting on the wrong load-bearing claim. |

**Framing-audit outcome:** the dispatch invocation handed me a framing ("BC-shift sweep FAILED both gates → § 8 ship gate at risk → escalate to Matt before broader commitment fires"). Reading the test script in ~5 minutes surfaces that the gates are misaligned. Per OP § 4.5 first-canonical-example pattern: sub-hour-latency framing-audit catches pre-imposed-assumption failure at minimum cost.

**This is the SECOND canonical operational example** (after gamora Pattern-A query on Q-A verdict W1.13 baseline 2026-05-23) of the framing-audit discipline catching a pre-imposed-assumption failure on a load-bearing decision before downstream commitment fires.

---

## 6. Confounders explicit per the discipline-check ask

The dispatch invocation asked: "are there confounders in the test design that invalidate the FAIL signal?" Yes — three confounders, in decreasing order of severity:

1. **Measurement-instrument substitution** (severe): `final_modifier` ≠ BC-coordinate shift. Invalidates the magnitude-near-zero FAIL signal entirely.
2. **Missing substrate context in 4 of 12 cases** (substantial): ELEMENT_CONVERSION and DEFENSIVE_CONVERSION opportunity-scan triggers require substrate.cultural_tradition signal that the test doesn't provide. Invalidates the strategy-selection FAIL signal for those 4 cases.
3. **Balance-loop under-convergence** (moderate): `max_iterations=5` produces unconverged balance-loop outputs for kits not in baseline win-rate target band. Adds noise to the `final_modifier` signal even within its (wrong) framing.

**Combined effect:** the FAIL signal as currently surfaced does not provide reliable evidence about § 8 architectural soundness. It does provide evidence that the test needs redesign.

---

## 7. Recommended Matt-decision framing

Matt's decision surface, ranked by my preference:

**Recommended (Tier 1):**
Test redesign → re-fire sweep → § 8 ships per v1 timeline.

Decision: "Re-do the BC-shift sweep with the methodology's actual measurement (BC-coordinate re-projection on predicted axis), substrate-context-provided test cases, and full balance-loop convergence. Hold the § 8 ship decision until corrected sweep returns. T4 post-mortem milestone gates on corrected sweep clearance, not original FAIL signal."

Cost: ~1-2 days additional (depends on whether BC-projection infrastructure exists in current form). Schedule-impact to T4 post-mortem: minor; well within Cycle 11 ~3-week scope estimate.

**Alternative (Tier 2):**
Run the legolas § 5.3 alternative cheapest-refuting-test (static η-calibration check) + accept it as the v1 gate.

Decision: "Use the static η-calibration check (5-minute compute) to validate strategy selection. Ship § 8 to v1 on its clearance. Move BC-coordinate magnitude validation to v1.1 when QD archive pipeline matures."

Cost: ~5 minutes compute + ~1 hour for test authoring. T4 post-mortem milestone unaffected.

This is acceptable because the static η-calibration check tests the load-bearing strategy-selection claim (without the substituted-instrument problem) and the magnitude claim is currently bottlenecked on infrastructure, not architecture. Deferring magnitude validation is a known-acceptable scope-trade.

**Reject (Tier 3 — explicitly not recommended):**
Re-design § 8 in response to the current FAIL signal. The FAIL signal does not justify this; would burn 1-2 weeks of rocket time on a wrong-problem fix.

---

## 8. Cycle 11 T4 post-mortem readiness milestone risk assessment

**Per current FAIL signal interpretation: T4 post-mortem milestone is at risk.**
**Per this critique's interpretation: T4 post-mortem milestone is NOT at risk.**

If Matt elects Tier 1 (test redesign + re-fire): ~1-2 day delay; absorbable within Cycle 11's ~3-week scope. Milestone preserved.

If Matt elects Tier 2 (static η-calibration substitute): zero delay. Milestone preserved.

If Matt elects to interpret FAIL as architectural and trigger § 8 re-design: 1-2 week delay minimum; milestone slips.

**The decisive question for milestone risk is: which interpretation does Matt accept?** My role here is to surface that the test-design interpretation is the empirically-supported reading. Matt makes the call.

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-25
**Pattern:** A-deep verdict per OP § 2 Pattern A-deep mode
**Anchor docs cited:**
- `canonical/story/skill-system-2026-05-24.md` § 7-9 (regime-change palette + Algorithm § 8 + spirit-guide explainer)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC measurement coordinate system)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B; Phase 3 convergence definition)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` § 5 (cheapest-refuting-test design)
- `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 5 (escape-hatch trigger)
- `~/Games/reincarnated-engine/scripts/bc_shift_validation_sweep.py` (test implementation; lines 269-276 acknowledge substitution)
- `~/Games/reincarnated-engine/logs/bc_shift_sweep_results.json` (FAIL signal)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #18 (methodology-before-execution), #18.2 (methodology-consultation timing at extension hotspots), #19.1 (cheapest-refuting-test), #23 (framing-audit Pattern A-deep three-question protocol)

**Discipline applied:**
- Discipline #23 framing-audit Pattern A-deep three-question protocol (§ 5)
- Discipline #19.1 cheapest-refuting-test (recognized in test methodology; surfaced its misimplementation)
- gandalf OP § 4.5 first-canonical-example flagging pattern (this is the SECOND canonical instance of framing-audit catching pre-imposed-assumption failure)

**Verdict summary:**
- Selected option: **(a) — architecture sound; test misaligned; redesign test + re-fire**
- Test design is itself the misalignment, NOT a genuine refuting signal against § 8 architecture
- Recommended Matt-decision: Tier 1 (test redesign + re-fire) OR Tier 2 (static η-calibration substitute) — both preserve T4 post-mortem milestone
- T4 post-mortem readiness milestone is NOT at risk under recommended decisions; IS at risk only if FAIL is over-interpreted as architectural

**Anti-pattern guard finding:** the FAIL signal does NOT warrant architectural recognition. KR did the right thing firing escape-hatch (per cycle-11-scope § 5); gandalf-side critique-pair surfaces that the empirical signal is about test, not architecture.

---

**Signed:** gandalf
**For:** the Cycle 11 Wave 3b ESCAPE-HATCH design-fit critique on Algorithm § 8 BC-shift validation sweep FAIL; routes to knight-rider for Matt-escalation framing; T4 post-mortem milestone risk-assessed; test redesign path preferred over architectural re-think.
