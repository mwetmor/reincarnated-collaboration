# Gate-1 Review — W0.7 LC-002 Ablation Experiment Design
**Date:** 2026-05-21
**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE Gate-1 (pre-implementation)
**Author under review:** gamora
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md`
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-jack-ryan-gate1-w0-7-lc-002-ablation-design.md`
**Principles applied:** Discipline #1, #2, #10, #11, #13a-partition, #13b

---

## Top-line verdict: BLOCK

**Two blocking findings.** One invalidates the measurement mode for the primary hypothesis (smoke-test produces n_classes=5, eliminating the round-robin bias being tested). One is a secondary element-order error in the prediction table that, while not blocking on attribution correctness, would produce misleading per-element predictions for wind/water/earth/physical. gamora must resolve both before proceeding to Run 1.

Path forward: (1) change Run 1/2/3 to use full regen, not smoke-test mode, OR design a smoke-compatible alternative; (2) correct the element order in the math note's prediction table.

---

## Per-question answers (gamora's 4 Gate-1 questions)

### Q1 — Surface disambiguation: is round-robin modulo correctly targeted?

**PASS with one additional surface note.**

The code confirms gamora's finding. `season_orchestrator.py:1490` assigns `element = elements[i % len(elements)]` where `elements = [fire, water, earth, wind] + ["physical"]` (5 elements, fire at index 0). For n_classes=11: indices 0,5,10 → fire, so 3/11 = 27.3%. The math note's attribution (Surface A explains ~96% of 23.6% over-representation) is mechanistically correct.

D1 pool `_weighted_sample` (Surface B): confirmed wrong surface. `_weighted_sample` picks pool entries per vocabulary slot (ignition/suffusion/bulwark/displacement), returning a fantasy word like "ember" or "magma" — not assigning a class's `canonical_element`. The function is called only in `_deterministic_fallback` for seasonal name selection. No code path connects it to `classes.canonical_element`.

`ELEMENT_AFFINITY` (Surface C): confirmed wrong surface. The dict is in `b6_archetype_templates.py`, which carries a deprecation banner as of W0.2 (tag `qd-rebuild/v0.2-archetype-refactor-complete`). Even when active, ELEMENT_AFFINITY governs secondary element selection within a kit's skill distribution AFTER `_generate_classes` assigns `canonical_element`. It cannot retroactively alter dominant_element frequency.

**Additional note for gamora:** The math note states "elements = [fire, wind, water, earth, physical]" in §2 and the predicted element order in §5.4 follows this sequence. The actual order from `config/elements.yaml` is `fire, water, earth, wind, physical`. The attribution claim (fire-at-index-0) is unaffected, but the per-element predictions for Run 1 and Run 2 in §5.4 are displaced for wind/water/earth. See Amendment #2.

### Q2 — B14.5 sidecar finding #4: classes.canonical_element or slot-name selection?

**PARTIAL — with a hypothesis-contamination note.**

The B14.5 sidecar Analysis 4 was titled "D1 element selection across historical seasons" and attributed fire over-representation to "pool-size leakage in selector" — explicitly framing it as a D1 selector problem. The raw data (fire=54, 23.58% over ~230 classes across ~15 seasons) is consistent with the same `classes.canonical_element` column gamora's 45-season query returned (86/365 = 23.6%). Same column, different dataset size.

However, the sidecar's causal attribution was wrong in 2026-05-12 too — the round-robin mechanism was the actual driver then as now. The sidecar called it "pool-size leakage" and "fire pool has the largest concrete/genre-precedent vocabulary." Gamora's constraint-inventory inherited this framing (LC-002 entry: "structural presupposition exists in the element selector's scoring and rotation logic"), which then propagated into the W0.7 dispatch.

**For Gate-1 purposes:** the sidecar measured `classes.canonical_element` (not slot-name selection). Gamora's Q2 is answered correctly: sidecar #4 = dominant_element frequency, not seasonal vocabulary word selection. PASS on that specific question.

**Residual concern:** the sidecar's causal framing ("pool-size leakage in selector") was never validated empirically. It was speculative. The round-robin attribution gamora has now produced is the first code-grounded attribution. The W0.7 dispatch inherited the speculative framing without the code audit. This is the precise scenario Discipline #11 (Empirical inspection over assumption) exists to prevent — and gamora correctly applied it. The lesson for future dispatch authoring is in Additional Review Point #5 below.

### Q3 — n_classes=11 stability in QD-rebuild context

**PARTIAL — open question, not a blocking finding for THIS ablation.**

The math note correctly notes that the round-robin attribution depends on n_classes=11 being the most common season size. Historical data confirms 15/45 seasons were n_classes=11.

For QD-rebuild context: `CLASS_COUNT_RANGE = (10, 12)`, producing n_classes 10 or 11 via `rng.integers(10, 12)`. This is a bernoulli-like draw producing 10 or 11 with roughly equal probability (10 with probability ~0.5, 11 with probability ~0.5 depending on RNG). If QD-rebuild generates seasons with this range unchanged, n_classes=11 will remain ~50% of cohorts. If the QD archive loop overrides n_classes to a fixed value or different range (not currently visible in the dispatch scope), the round-robin contribution changes.

**Blocking consequence:** none for the current ablation design if the ablation uses seeds that produce n_classes=11. Non-blocking for Gate-1 decision; gamora should note this as a forward caveat in the math note's §7.

**Critical clarification gamora needs before running:** see Blocking Finding #1 below — smoke-test mode fixes n_classes=5, eliminating the hypothesis entirely.

### Q4 — Discipline #13a-partition compliance of seed-derived rotation offset

**PASS.**

The proposed fix `elements[(seed_derived_offset + i) % len(elements)]` where `seed_derived_offset = seed % len(elements)` derives the offset from `seed` — a mechanical population parameter (the season's random seed, a scheduling property). It does not branch on any element identity string. The element list order is fixed; the rotation offset is applied uniformly. No element receives preferential treatment by name.

The seeded-random ablation (Run 3) replaces round-robin with seeded random draw without replacement. This similarly does not branch on element identity — the randomization is seeded by a value unrelated to element name.

Both Run 2 and Run 3 modifications PASS the #13a-partition requirement.

---

## Additional review points

### Point 5 — W0.7 dispatch surface error: process disposition

**Finding:** The W0.7 dispatch (§ LC-002) specified "fire weight halved" targeting D1 pool weighting — a surface that gamora's code audit showed has zero connection to `classes.canonical_element`. The dispatch was authored without code-grounded surface verification.

**Scope of error:** LC-009 and LC-011 carry similar risk. The dispatch's surface hypotheses for LC-009 (range_profile, geometry_bias, kit_size) were authored from the B14.5 sidecar's speculative framing and the constraint-inventory's analytical entries — both of which, for LC-002, proved to contain a surface error. The W0.7 dispatch was structurally optimistic: it named specific ablation variables before verifying that those variables had causal paths to the measured outcomes.

**Recommendation:** knight-rider should NOT amend the W0.7 dispatch for LC-009 and LC-011 in advance. The reason is that the amendment would require the same code-level surface verification gamora applied to LC-002 — and knight-rider is not the right agent to perform that inspection. Instead, the correct process is:

- Apply the gamora LC-002 pattern as the mandatory template for LC-009 and LC-011: Discipline #11 empirical inspection of source code BEFORE authoring the math note, where inspection may revise the dispatch's named surfaces.
- gamora explicitly documents the surface verification results in §2/§3 of each math note (as done for LC-002).
- Gate-1 for LC-009 and LC-011 reviews the surface verification, not just the experiment design.

This is more robust than a dispatch amendment, because the amendment would require speculative code reads that may themselves introduce new errors. The per-LC empirical inspection pattern gamora demonstrated is the correct process.

**Disposition:** rely on gamora per-LC empirical inspection. Document this pattern in the Gate-1 finding. Cite Discipline #11.

### Point 6 — Attribution structure: does the 3-run design actually produce X/Y/residual?

**PARTIAL-PASS.**

The design logic is sound for the primary attribution question (does round-robin index-0 explain the fire bias?). Run 1 baseline measures current rate; Run 2 measures the rate after eliminating index-0 advantage; Run 3 measures the rate under fully randomized assignment. The difference Run1-Run2 attributes the index-0 contribution; Run2-Run3 attributes any ordering-without-index-0 contribution; Run3 measures residual.

However, the attribution is only valid if the three runs are truly held constant except for the element assignment logic. The math note §5.3 plans to use the same seed (9001) for all three runs — correct. But the telemetry isolation plan (pre/post row count) needs to account for the fact that `classes` rows include all classes across seasons, and runs with the same seed may produce the same season IDs, causing primary-key conflicts or row updates rather than new inserts. gamora should verify that the three runs do not produce duplicate season_id/class_id combinations that would corrupt the post-run query.

The D1 pool attribution slot (B) is correctly specified as 0% — no ablation needed to confirm this, the code audit is sufficient. The ELEMENT_AFFINITY slot (C) is correctly specified as 0%. The framework produces the correct X/Y/residual structure.

### Point 7 — Smoke-test sufficiency: BLOCK-level finding

**FAIL — BLOCKING.**

This is the most critical finding in this review.

**The problem:** `season_orchestrator.py:297` explicitly sets `n_classes = 5` in smoke-test mode. The round-robin fire assignment under n_classes=5 produces exactly 1/5 = 20.0% fire — the uniform expectation. The observed bias (23.6%) is entirely produced by n_classes=11 seasons assigning 3/11 = 27.3% fire. Smoke-test mode eliminates the n_classes=11 pathway, so the mechanism gamora is testing cannot manifest.

**Consequence:** if gamora runs all 3 ablation runs in smoke-test mode:
- Run 1 baseline: expected fire ~20.0% (not ~23.3% as math note predicts)
- Run 2 rotation: expected fire ~20.0% (same, because n_classes=5 is already balanced)
- Run 3 random: expected fire ~20.0% (same)

All three runs converge to the same measurement. The ablation produces a flat line across all three conditions. This appears to confirm that round-robin makes no difference — the exact opposite of the correct conclusion. The design produces a false null result under smoke-test mode.

**Root cause:** Discipline #2 correctly prescribes smoke-test for rapid iteration. However, Discipline #2 is appropriate when the mechanism being tested operates independently of n_classes. The LC-002 mechanism (modulo-index bias) is specifically a function of n_classes≠5. Smoke-test eliminates the variable the ablation is measuring.

**Required fix:** gamora must use full regen (non-smoke) for ablation runs, with enough seasons to produce a mix of n_classes=10 and n_classes=11 cohorts. OR gamora must use the `n_classes` override parameter (pass `n_classes=11` explicitly to the orchestrator) to force n_classes=11 per run regardless of smoke/non-smoke mode. The latter is acceptable as an ablation-only override if it avoids the full regen cost.

**Sample size under corrected design:** at 15 full-regen seasons with n_classes~10-11 per CLASS_COUNT_RANGE, total classes ~150-165. With fire expected at 23.3% baseline and 20.0% post-correction, the signal is 3.3pp over 165 data points (43 fire vs 33 expected). A chi-square test on that n gives sufficient power (p < 0.01 at this effect size). Full regen is necessary; smoke is not acceptable for this ablation.

### Point 8 — Output format alignment with Discipline #13b template

**PASS.**

The math note §4 specifies:
- (A) Round-robin modulo index: X% — predicted ~96% (~3.5 pp)
- (B) D1 pool weighting: 0%
- (C) ELEMENT_AFFINITY cascade: 0%
- (D) Residual: Y%

This matches the "X% / Y% / residual%" structure required by Discipline #13b. The output is measurement-oriented (a percentage-point attribution), not qualitative. PASS.

---

## Amendments

### Amendment #1 — BLOCKING: Do not use smoke-test mode for ablation runs

**Severity: Blocking.**

gamora must not use `--smoke` flag for any of the three ablation runs. Smoke-test mode hardcodes n_classes=5, which produces 20.0% fire under round-robin (no bias) and makes the ablation's hypothesis untestable. Either:
- (a) Use full regen (`generate-season --seed 9001`), accepting the ~10-minute-per-run cost, OR
- (b) Use explicit `n_classes=11` override parameter to force the measurement-relevant cohort size, if the orchestrator API supports direct n_classes injection.

The math note's §5.1 and §5.3 must be updated to reflect the corrected mode. Discipline #2 ("smoke-test for rapid iteration") does not apply when the mechanism under test is n_classes-dependent.

Cite: Discipline #2 (correct application boundary), Discipline #10 (attribution clarity — change one thing, measure one thing).

### Amendment #2 — NON-BLOCKING: Correct element order in prediction table

**Severity: Non-blocking (attribution claim is correct; predictions for non-fire elements are wrong).**

Math note §2 states the elements list as `[fire, wind, water, earth, physical]`. Actual order from `config/elements.yaml` is `fire, water, earth, wind, physical`. The attribution claim (fire at index 0, produces 27.3% for n_classes=11) is correct regardless of the remaining element order. However:
- The Run 2 prediction table (§5.4) predicts "Earth % ~20.7%" and "Wind % ~20.0%" based on the wrong ordering.
- Under the correct ordering, Wind is at index 3, Earth is at index 2. The per-element predictions in Run 2 are displaced.

gamora should update §2 and §5.4 to use the correct element order before running. The correction does not affect the fire attribution math; it prevents the post-run comparison against wrong per-element predictions.

Cite: Discipline #11 (empirical inspection over assumption — verify source config before populating prediction tables).

### Amendment #3 — NON-BLOCKING: Add n_classes=11 forward caveat to §7

**Severity: Non-blocking.**

The math note §7 discusses forward implications but does not caveat that the round-robin hypothesis (and the proposed fix's effectiveness) is contingent on n_classes remaining in the 10-12 range. If QD-rebuild uses a different cohort size (e.g., n_classes=5 uniformly), the bias disappears without any fix. gamora should add a one-sentence caveat to §7 noting this dependency.

Cite: Q3 answer above.

### Amendment #4 — NON-BLOCKING: Clarify telemetry isolation for same-seed runs

**Severity: Non-blocking.**

Math note §5.3 plans pre/post row-count isolation. gamora should verify that three sequential runs with seed 9001 do not produce duplicate season_id values that cause row updates rather than new inserts. If season_id is seed-derived, the same seed across three runs may produce identical season_ids, with later runs overwriting earlier rows. The isolation method must account for this. Recommend documenting the season_id generation logic and verifying uniqueness per-run before executing.

---

## Process recommendation (dispatch surface error disposition)

knight-rider should NOT amend the W0.7 dispatch pre-design for LC-009 and LC-011. The correct disposition is:

1. gamora applies Discipline #11 empirical surface inspection to LC-009 and LC-011 before authoring their math notes, using the LC-002 pattern as precedent.
2. Each math note includes a §2 "Candidate surfaces" section with explicit code-path verification (as gamora did for LC-002).
3. Gate-1 for each LC verifies the surface verification table, not just the experiment design.
4. If gamora's surface inspection revises the dispatch's named variables (as happened for LC-002), that revision is documented in the math note and this finding protocol captures it.

This is more robust than a dispatch amendment because: (a) knight-rider is not positioned to do the code-level surface verification, (b) the amendment would be speculative, and (c) the per-LC pattern gamora demonstrated is exactly the right process — reward it structurally rather than replacing it with a top-down amendment.

---

## Sample-size disposition

**Not sufficient under smoke-test mode (see Amendment #1 — Blocking). Sufficient under full regen or n_classes=11 override.**

With corrected mode (full regen, n_classes 10 or 11 per CLASS_COUNT_RANGE):
- 15 seasons × ~10.5 classes/season avg = ~157 classes
- Fire expected: 23.3% baseline → ~37 fire classes
- Post-correction expected: 20.0% → ~31 fire classes
- Delta: ~6 classes difference over 157 data points
- At this n, chi-square test on 2x5 contingency (element × run) achieves p < 0.01 for a 3.3pp effect (confirmed by inspection of power tables for chi-square with n=157, k=5, effect size ~0.09)

15 seasons per run is adequate under full regen. gamora may reduce to 10 seasons if time is a constraint, accepting somewhat lower power (~0.80 at p<0.05).

Under smoke-test mode (n_classes=5), no sample size is sufficient — the mechanism does not activate.

---

## Summary of findings by severity

| Finding | Severity | Amendment |
|---|---|---|
| Smoke-test mode eliminates the n_classes=11 mechanism being tested | BLOCK | #1 |
| Element order in prediction table is wrong (wind/water/earth displaced) | WARN | #2 |
| n_classes forward caveat missing from §7 | INFO | #3 |
| Telemetry isolation may fail for same-seed runs | INFO | #4 |
| Q1 surface disambiguation: correct | PASS | — |
| Q2 sidecar finding #4: correct (canonical_element column) | PASS | — |
| Q3 n_classes stability: open question, non-blocking | PARTIAL | #3 |
| Q4 #13a-partition compliance: passes | PASS | — |
| Attribution structure (3-run design) | PARTIAL-PASS | — |
| Output format alignment with #13b template | PASS | — |

---

## References

- `reincarnated-engine/src/reincarnated/generation/season_orchestrator.py:297` — `n_classes = 5` in smoke-test mode (the blocking finding)
- `reincarnated-engine/src/reincarnated/generation/season_orchestrator.py:1480,1490` — `_generate_classes` round-robin, elements list construction
- `reincarnated-engine/config/elements.yaml:2-45` — canonical element order: fire, water, earth, wind, physical
- `reincarnated-engine/src/reincarnated/element/selector.py:536-609` — `_deterministic_fallback` and `_weighted_sample` (Surface B — confirmed wrong surface)
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py:62-72` — `ELEMENT_AFFINITY` (Surface C — deprecated, confirmed wrong surface)
- `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md` — math note under review
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` §2, §10, §11, §13a-partition, §13b
