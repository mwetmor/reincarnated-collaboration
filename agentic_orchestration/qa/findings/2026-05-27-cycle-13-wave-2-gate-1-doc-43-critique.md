# Finding — 2026-05-27 — Cycle 13 Wave 2 Gate-1 Critique: Doc 43 T4 Algorithm Design INTENT

**Reviewer:** jack-ryan
**Severity:** PASS-with-WARN (0 BLOCK; 2 WARN; 5 INFO)
**Target:** commit `6a97087` — `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md`
**Developer:** gandalf
**Principles applied:** Principles 1 / 2 / 3 / 4 / 5 / 6; Disciplines #1 / #1.2 / #11 / #18 / #18.2 / #23 / #26 / #27 / #29 / #30 / #31 / #32

---

## Verdict

**PASS-with-WARN.** Rocket Wave 2 implementation dispatch authoring may proceed. Two WARN conditions (W1–W2) must be folded into rocket Wave 2 dispatch acceptance criteria before rocket fires. Specifically: W1 (elrond statistical-priors ownership gap) must be surfaced in the Wave 2 dispatch scope; W2 (Pattern 9+10 catalog-inclusion decision gate) must be clarified in W2.6 acceptance criteria. The five INFO items are notes for the record — no blocking action.

---

## What I found — 11 critique dimensions

### Dimension 1 — Architectural alignment (Discipline #18 + #11) — doc 43 vs doc 40 § 8 amended + closeout §§ 1.3 / 1.7 / 2.4 / 2.5 / 7

**Verdict: INFO.**

Empirical spot-check performed at doc 40 § 8, § 8.4, § 8.4.1, § 8.4.2, § 8.4.3, § 8.2 (Option F LOCKED 2026-05-27), § 8.3 (variable chain count), D66 sharpening, D76, D83; and closeout §§ 1.3, 1.4, 1.7, 2.4, 2.5, 7.

**Confirmed aligned:**

- 3-category T4 taxonomy: doc 40 § 8.4 post-amendment states "SUPERSEDES the 6-strategy registry as the player-facing taxonomy + design-spec" with A/B/C exactly as doc 43 §§ 2.1-2.2. No drift.
- DUAL_ELEMENT_ADDITION: doc 40 § 8.4.1 NEW LOCKED 2026-05-27 — confirmed. Doc 43 § 3 operationalizes with class element compatibility check citing `class_schema.py:46-47`. Aligned.
- Parallel-chain reach: doc 40 § 8.4.2 LOCKED — "chain-specific effect can target T4's OWN chain OR a PARALLEL chain; algorithm-fixed at generation time." Doc 43 § 4 matches exactly including tie-breaker (own-chain default within ±5%). Aligned.
- Compositional synergy scan: doc 40 § 8.4.3 LOCKED — "two-pass synergy detection (resolve + preserve); algorithmic composition (pattern library + statistical priors); NOT LLM raw-reasoning per D7." Doc 43 §§ 5.1-5.7 fully operationalizes. Aligned.
- T4-failure-handling Option F: doc 40 § 8.2 lists exactly 4 phases matching doc 43 § 6.1 (Phase 1 regeneration 3-attempt; Phase 2 partial-T4 ship; Phase 3 minimum threshold ≥1; Phase 4 quality metric tracking). D1/D67/D65/D62 composition cited in both docs. Aligned.
- D66 sharpening (one-T4-at-a-time): doc 40 D66 amended states "ONE T4 unlocked at a time — sharpens from passive description to ACTIVE IDENTITY DISCIPLINE." Doc 43 § 8.1 mirrors verbatim. Aligned.
- Variable 3-or-4 chain architecture: doc 40 § 8.3 table (3-chain/4-chain) matches doc 43 § 9.1 table. Per-class roster deferred in both. Aligned.
- D83 (T4 count = chain count - 1): cited in doc 43 § 9.1 and § 9.4. Aligned.

**No drift found across any spot-checked cross-reference.** Doc 43 is a faithful operationalization of doc 40 § 8 post-amendments and closeout locks.

**Cite:** Discipline #11 (empirical inspection over assumption — spot-check performed at multiple doc 40 and closeout sections; not inferred from summary).

---

### Dimension 2 — Discipline compose-check (#27 / #31 / #32 per I2 routing)

**Verdict: INFO.**

Per Wave 1 Gate-1 I2 routing requirement: Disciplines #27 + #31 + #32 must be explicitly cited and composed in doc 43. Verified:

| Discipline | Citation location in doc 43 | Assessment |
|---|---|---|
| **#27 dual-effect capstone** | § 2.1 (table column "D76 dual-effect part"), § 3.5, § 11.7, § 13 composition table row | Cited + composed. Every T4 = Category A (character-wide) + exactly one of B or C (chain-specific). Implementation of #27 is the core architecture. PASS. |
| **#31 dual-effect separability** | § 2.4 (full failure-mode + correction example), § 3.5, § 5.3 (separability test in Pass 2), § 11.7, § 13 | Cited + composed. Separability test lives in Pass 2 preserve check. Founding instance (Blood Magic example) reproduced. PASS. |
| **#32 first-do-no-harm** | § 5.7 (founding instance + two-pass IS the implementation), § 7.3, § 11.7, § 13 | Cited + composed. Pass 2 preserve check + Pattern 9 + Pattern 10 detection are applications of #32. PASS. |

All three disciplines are explicitly cited and load-bearing at the structural level. The Wave 1 Gate-1 I2 routing requirement is fully honored.

**Cite:** Discipline #11 (line-level verification performed, not inferred from doc summary).

---

### Dimension 3 — 5-category synergy framework completeness (per W3 routing)

**Verdict: INFO.**

Verified § 5.4 Scaling-interaction 5th category operationalization against SC-4 expansion Topic 2 §§ 2.2-2.3 verdict.

**SC-4 expansion verdict requirement:** distinguish "true multiplicative across separate buckets" (high-value) from "additive within same bucket, mistaken for multiplicative" (trap). The algorithm must validate bucket-identity per candidate before scoring scaling-interaction synergy.

**Doc 43 § 5.4 operationalization:** the Scaling-interaction row in the 5-category taxonomy explicitly states: "True scaling-interaction synergies (multiplicative across separate buckets) are high-value AND high-trap-risk" AND "False scaling-interaction (additive within same bucket) is the source of many trap builds." Doc 43 § 5.4 further states: "the synergy scan MUST distinguish 'does this compound multiply independently?' vs 'does this add to the same bucket?' — algorithm validates bucket-identity per candidate before scoring scaling-interaction synergy." This mirrors the SC-4 expansion verdict language exactly.

**Pass 1 / Pass 2 checks at § 5.2 / § 5.3:** Pass 2 preserve explicitly lists "Degenerate-end multiplicative-stacking" as a downstream-tension-creation pattern with detection ("detect candidate's multiplier scaling vs investment-curve top-end"). The Archmage precedent is cited. The SC-4 expansion empirical evidence informs both passes. Correct.

**No completeness gap found.** The SC-4 expansion Topic 2 verdict is correctly folded in at the required depth.

**Cite:** SC-4 expansion research §§ 2.2-2.3; Discipline #11 (empirical cross-reference verification against SC-4 expansion source).

---

### Dimension 4 — Pattern 9 + Pattern 10 spec depth (per W3 routing + #18.2 timing alignment)

**Verdict: WARN (W2).**

Starting-estimate thresholds are present and match SC-4 expansion definitions:

- Pattern 9 threshold: <1 active skill per 10 sec — matches SC-4 expansion § 3.4 proposed definition exactly. Sourced from GGG PoE2 0.2.0 / 0.5.0 patch empirical language. Defensible.
- Pattern 10 threshold: >5× expected DPS at max DoT stack — matches SC-4 expansion § 3.4 proposed definition exactly. Sourced from PoE2 Poison Pathfinder + GD DoT mechanics. Defensible.
- #18.2 delegation timing: detection-algorithm calibration explicitly delegated to gamora SC-7 post-Wave-3-baseline per §§ 7.1 / 7.2 / 7.3. Timing is correct (AFTER baseline).

**Gap (W2 — see action):** Doc 43 § 7.3 states "Pattern 9 + Pattern 10 are catalog EXTENSIONS (candidate status); inclusion in v1 catalog vs v1.1 catalog is gamora SC-7 decision per #18.2." However, W2.6 acceptance criteria in § 10 states "jack-ryan Gate-1 critique; test coverage on Pattern 9 + Pattern 10 detection paths against synthetic positive + negative cases" — without a close criterion distinguishing between "implemented at design-intent depth" and "included in v1 catalog." This creates an ambiguity: does rocket implement Pattern 9+10 detection in Wave 2 as design-intent stubs (starting-estimate thresholds, routes to retry, not yet calibrated), OR does passing W2.6 imply catalog inclusion has been decided?

Doc 43 § 12 close criterion clarifies: "Pattern 9 + Pattern 10 generation-time detection implemented at design-intent depth; starting-estimate thresholds; composes with #32 Pass 2 preserve check; detection-algorithm calibration DELEGATED to gamora SC-7." The word "implemented" without a qualifier could lead rocket to interpret this as v1 catalog membership rather than design-intent stub. The risk is over-implementation (rocket treats Pattern 9+10 as production v1 patterns when they are candidate patterns pending gamora SC-7 ratification).

**WARN W2:** W2.6 acceptance criteria in the rocket dispatch must explicitly state: "Pattern 9 + Pattern 10 are implemented as design-intent stubs at starting-estimate thresholds; catalog inclusion (v1 vs v1.1) is gamora SC-7 decision post-Wave-3-baseline; Wave 2 implementation DOES NOT constitute v1 catalog membership." This prevents rocket from over-committing the detection patterns as v1 production behavior.

**Cite:** Discipline #18.2 (consultation timing — full detection algorithm calibration fires AFTER baseline). Discipline #1.2 (implementation claims must be traceable to their scope).

---

### Dimension 5 — DUAL_ELEMENT_ADDITION magnitude calibration choice (per #18.2 timing)

**Verdict: INFO.**

Magnitude band anchors (Low 15-25% / Medium 25-40% / High 40-55%) are clearly labeled as "ANCHOR starting estimates" with explicit gamora SC-7 delegation post-Wave-2-baseline per Discipline #18.2. The Verdict-B.4-pattern citation is correct.

**Genre precedent reasonableness check (Discipline #11):**
- PoE "X% physical as fire" mid-game: community docs show values typically 10-40% at mid-tier; 40-60% at endgame affixes — the Low/Medium bands are conservative and well-grounded.
- D4 "all skills deal X% as cold" (Aspect of Frozen Wake): values typically 10-40% in observed community documentation — consistent with Low/Medium bands.
- High tier (40-55%): at the top of observed mid-late-game precedent; slightly aggressive but within defensible range for T4 endgame content. Labeled correctly as "approaches PoE mid-late-game tier."

**Selection logic** (§ 3.4 algorithm-selects-by-archetype + cross-chain composition score + Pattern 10 headroom) is mechanically coherent: burst classes lean Low (correct — lower magnitude reduces degenerate burst compounding); sustained DPS leans Medium/High (correct — DoT-oriented classes have more room for magnitude before Pattern 10 triggers).

**No calibration concern at ANCHOR level.** The gamora SC-7 delegation is appropriately timed.

**Cite:** Discipline #18.2 (consultation fires AFTER baseline — correctly sequenced).

---

### Dimension 6 — legendary_t0_5 rarity inclusion (per I1 carryover from Wave 1 Gate-2)

**Verdict: INFO.**

Wave 1 Gate-2 I1 carryover required: "include `legendary_t0_5` in Wave 2 or future test expansion."

**Doc 43 closes this gap explicitly and prominently:**
- § 10 W2.9 gate: "Round-trip smoke per Principle 6 (CRITICAL: legendary_t0_5 inclusion per Wave 1 Gate-2 I1)"
- § 12 close criterion: "Round-trip smoke per Principle 6 covering all 10 rarity tiers INCLUDING `legendary_t0_5` (Wave 1 carryover gap closure)"
- § 11.3 empirical assertion list: "Round-trip smoke rarity coverage (10 rarities including legendary_t0_5 per Wave 1 Gate-2 I1)"

The I1 carryover is fully honored at design-intent level. Rocket has no ambiguity on this requirement — `legendary_t0_5` is explicitly and repeatedly called out as a CRITICAL inclusion in the round-trip smoke.

**Cite:** Principle 4 (decisions-log traceability — Wave 1 Gate-2 I1 properly propagated to Wave 2 intent); Discipline #11 (empirical verification: three separate doc 43 sections confirm `legendary_t0_5` requirement).

---

### Dimension 7 — Sub-wave structure W2.0-W2.9 implementation-readiness (Discipline #1.2)

**Verdict: INFO (with one scoped observation).**

Sub-wave structure W2.0-W2.9 (doc 43 § 10) assessed against implementation-readiness criterion: can rocket fire WITHOUT requiring re-clarification dispatches?

**W2.0-W2.3 (substrate prep through parallel-chain reach):** each sub-wave specifies work-unit, owner, gate, and cross-dependencies at sufficient depth. No ambiguity.

**W2.4 (compositional synergy scan):** Pattern library implementation specifies "gandalf-curated v1 catalogs from § 5.2 + § 5.3" and "statistical priors (elrond-cooperated where substrate corpus surfaces priors)." The gate is "jack-ryan Gate-1 critique; test coverage on pass-1 + pass-2 scoring; cross-validation with starter pattern-library entries." Sufficient.

**W2.5-W2.7 (failure-handling, Pattern 9+10, one-T4-at-a-time):** gates and cross-dependencies are clear. W2.6 ambiguity is the W2 WARN (see Dimension 4 above).

**W2.8 (cross-cohesion validation):** gamora ownership is clear; 4 cohort archetypes are named; kit-count-per-archetype is delegated to Block C scaffolding (consistent with Wave 1 Gate-1 I2 routing). Sufficient.

**W2.9 (round-trip smoke):** 10-rarity coverage including `legendary_t0_5` is explicit. WARN-pattern full closure requirement is explicit. Sufficient.

**Scoped observation (INFO, not WARN):** W2.4 gate requires "cross-validation with starter pattern-library entries" but does not specify how many starter entries constitute "starter." The v1 Pass 1 catalog in § 5.2 has 5 entries; the v1 Pass 2 catalog in § 5.3 has 8 entries. Rocket should validate against all named entries (5 Pass 1 + 8 Pass 2 = 13 starter entries). The KR Wave 2 dispatch should specify the 13-entry validation scope to prevent rocket from interpreting "starter" as a subset.

**Cite:** Discipline #1.2 (sub-wave implementation claims must be verifiable; no code-line claims made in this intent doc — appropriate; spec-only level). Discipline #18.2 (W2.8 validation design is correct — no calibration before baseline).

---

### Dimension 8 — One-T4-unlocked-at-a-time + variable 3-or-4 class chain architecture

**Verdict: INFO.**

**§ 8 one-T4-unlocked-at-a-time:** The algorithm implication at § 8.3 is correctly specified — "generates T4 options PER CHAIN; player selection (at runtime) determines which T4 is currently active; algorithm does NOT need to generate T4-combination scoring." This is a material simplification correctly stated: N-scoring (single-T4) vs N² pair-scoring. The spirit-guide projection surface (§ 8.4) correctly shows per-T4 projections rather than combination projections. Composes with closeout § 1.3 lock (D66 sharpening). Aligned.

**§ 9 variable 3-or-4 class chain architecture:** The architecture table (§ 9.1) matches closeout § 1.4 exactly. The algorithm implication (§ 9.4) provides concrete parameterization: `class_chain_count: Literal[3, 4]`, generates `T4_count = chain_count - 1`, parallel-chain reach target space varies per chain count. Supporting chain integration (§ 9.2) correctly absorbs the 55-entry minimum-viable trait pool per doc 42 § 8 + W1.6. Branching refinement (§ 9.5) correctly states T4 algorithm operates on the capstone only; branching is structural skill-tree concern. Aligned.

**Per-class roster deferred:** § 9.3 states "empirical-evidence criterion for re-engagement = Wave 1 BC-target review surfaces evidence." Correctly deferred with explicit empirical gate. Per Discipline #11 operational application (empirical criterion names what gates re-engagement). Correct.

**No gaps found in this dimension.**

**Cite:** Discipline #11 (empirical inspection of §§ 8 and 9 against closeout §§ 1.3 and 1.4). Principle 4 (deferred commitment correctly names empirical gate).

---

### Dimension 9 — T4-failure-handling Option F hybrid retry mechanism spec

**Verdict: INFO.**

All 4 phases of Option F are specified per closeout § 1.7 + doc 40 § 8.2 amended:

| Phase | Doc 43 location | Closeout § 1.7 match | Assessment |
|---|---|---|---|
| Phase 1 — Regeneration (3 attempts) | § 6.1 + § 6.2 | 3 attempts; configurable per D62 | MATCH. Retry sequencing (alternate Category B/C → alternate Category A → flip parallel-chain reach) is operationally useful; not in closeout but an appropriate spec-level addition. |
| Phase 2 — Partial-T4 ship | § 6.1 + § 6.3 | Ship with T1-T3 intact; no capstone | MATCH. Spirit-guide messaging spec at § 6.3 is an additive spec detail, not a drift from closeout. |
| Phase 3 — Minimum threshold ≥1 T4 | § 6.1 + § 6.4 | ≥1 T4 in-band minimum | MATCH. Per-chain-count instantiation (3-chain = minimum 1; 4-chain = minimum 1; 0-in-band = generation failure) correctly extends the closeout abstract statement to concrete algorithm behavior. |
| Phase 4 — Quality metric tracking | § 6.1 + § 6.5 | Track regeneration rate | MATCH. Formula `T4_regeneration_rate(class, cohort) = sum(retries_used) / sum(T4_candidates_attempted)` is an appropriate operationalization of the closeout "track regeneration rate as quality metric" intent. |

**D1 + D67 + D65 + D62 composition:** all four cited in § 6.6 composition table. Matches closeout § 1.7 "Composes with D1, D67, D65, D62" exactly.

**No gaps found in Option F spec.**

**Cite:** Discipline #11 (empirical line-level verification against closeout § 1.7 and doc 40 § 8.2).

---

### Dimension 10 — Cross-doc consistency (#11 + #23 framing-audit three-question protocol)

**Verdict: WARN (W1).**

#### Framing-audit per Discipline #23 three-question protocol

Doc 43 does not contain an explicit § 11 / § 12-style framing-audit section (doc 42 had § 11 with a three-question protocol invocation). For a design-INTENT doc at this scale, the framing-audit should be applied. Applying it now per my role:

**Q1 (what would refute): if the 3-category T4 taxonomy is the wrong shape, what evidence would surface?**

The 3-category shape (always A + exactly one of B or C) means every T4 has a character-wide effect and a chain-specific effect. The taxonomy would be refuted if: (a) rocket implementation surfaces a meaningful design-space requirement that requires A + BOTH B and C simultaneously, OR (b) testing reveals that the chain-specific constraint (B XOR C) produces systematically thin T4 design space (too few viable strategy combinations per class archetype). SC-4 expansion and genre precedent (PoE keystones, GD masteries, LE skill trees) all use a "primary alteration + secondary alteration" pattern consistent with the two-part structure. The shape appears well-grounded.

**Q2 (cheapest refuting test): how cheaply can rocket implementation falsify?**

The cheapest refuting test: rocket generates T4 candidates for all 22 BC-target cells × 2 cohort archetypes (not all 4; a 50%-coverage spot-check) and counts how many strategy combinations are forced into degenerate fallback (Phase 3 minimum threshold triggered) due to the B-XOR-C constraint. If >20% of kits reach Phase 3 minimum, the taxonomy shape may be too constraining. This is a W2.4-level test derivable from the round-trip smoke output at W2.9.

**Q3 (alternative framing): is "3-category as primary unit" framing right, OR is "6-strategy as primary + 3-category as player-facing" cleaner?**

The alternative framing question from the Wave 1 dispatch is now answered by the 2026-05-27 closeout lock: 6-strategy as algorithm implementation detail + 3-category as player-facing and design-spec. This distinction is correctly implemented in doc 43 §§ 2.2-2.3. The framing is resolved. No conflict with a locked decision.

**Framing-audit verdict:** the three questions are addressable and do not surface a BLOCK condition. The framing-audit section is absent from doc 43 itself.

**W1 — WARN: doc 43 is missing an explicit framing-audit section (Discipline #23 three-question protocol).** Doc 42 (Wave 1 precedent) had § 11 explicitly invoking the protocol. Doc 43 is larger and architecturally more load-bearing than doc 42 — the absence of a framing-audit section is a pattern regression relative to the doc 42 precedent. The three questions are answerable (as above) and don't block rocket; but the INTENT doc should carry them so future readers have the cheapest-refuting-test documented. Gandalf should amend doc 43 with a § 11.9 (or appended to § 11) framing-audit subsection carrying the three-question answers per Discipline #23.

**Cross-doc consistency spot-check (non-framing-audit items):**

| Cross-reference | Verified | Status |
|---|---|---|
| Doc 40 § 8 3-category taxonomy | Spot-checked § 8.4 post-amendment | ALIGNED |
| Closeout § 2.4 + § 2.5 locks | Spot-checked against doc 43 §§ 2 + 5 | ALIGNED |
| Closeout § 1.7 Option F | Spot-checked § 6 | ALIGNED |
| SC-4 expansion Topic 2 (5th synergy) | Spot-checked § 5.4 vs SC-4 §§ 2.2-2.3 | ALIGNED |
| SC-4 expansion Topic 3 (Pattern 9+10) | Spot-checked § 7 vs SC-4 §§ 3.4-3.5 | ALIGNED |
| Ground-state doc 43 row | Spot-checked `00-ground-state.md` § 1 | PRESENT |
| Wave 1 Gate-1 I2 routing (#27/#31/#32) | Spot-checked §§ 2.4, 3.5, 5.7, 11.7, 13 | FULLY HONORED |
| Wave 1 Gate-2 I1 carryover (legendary_t0_5) | Spot-checked §§ 10 W2.9, 11.3, 12 | FULLY HONORED |

**No cross-doc consistency failures found beyond the missing framing-audit section.**

**Cite:** Discipline #23 (framing-audit three-question protocol — mandatory at load-bearing verdict points; this is the primary intent doc for a major algorithm wave). Discipline #11 (empirical cross-reference verification across all cited docs).

---

### Dimension 11 — WARN-pattern full-closure framing accuracy + ground-state § 1 update verification

**Verdict: INFO.**

**WARN-pattern full-closure framing:**
- § 11.3 is titled "Discipline #11 empirical inspection (CRITICAL — full WARN-pattern closure target)" and specifies 8 asserted counts with explicit `len()` requirement. The Wave 1 Gate-2 partial-remediation status (7/8 PASS; modifier count 1 fail) is correctly captured in the authority basis and § 11.3.
- § 10 W2.9 gate: "post-script empirical count assertions per Discipline #11 (CRITICAL: full WARN-pattern closure target per Wave 1 Gate-2 partial-remediation status — Wave 2 Gate-2 = 0 empirical assertion failures)."
- § 12 close criterion: "Full WARN-pattern remediation per Discipline #11 (Wave 2 Gate-2 = 0 empirical assertion failures; CRITICAL)."

The Wave 2 = full closure target framing is present, prominent, and correctly classified as CRITICAL in three separate sections. No framing ambiguity for rocket.

**Ground-state § 1 update verification (Discipline #11 spot-check):**

Empirically verified: `canonical/00-ground-state.md` § 1 table contains doc 43 row at the correct position (after doc 42 entry, before doc 02 roadmap entry). The row description is comprehensive — it captures the 3-category taxonomy, DUAL_ELEMENT_ADDITION, parallel-chain reach, synergy scan, Option F failure-handling, Pattern 9+10, one-T4-unlocked discipline, variable chain architecture, W2.0-W2.9 sub-waves, and Wave 2 close criterion. The ground-state entry is load-bearing, not a stub.

**Both items fully honored.**

**Cite:** Discipline #11 (empirical spot-check of ground-state performed at review time, not inferred from gandalf completion record).

---

## Severity summary

| ID | Severity | Finding |
|---|---|---|
| W1 | WARN | Doc 43 is missing an explicit Discipline #23 framing-audit section (§ 11 framing-audit absent; doc 42 had it; pattern regression on the larger and more load-bearing doc). Three-question answers are available and do not surface a BLOCK; gandalf should amend doc 43 with a § 11.9 framing-audit subsection |
| W2 | WARN | W2.6 acceptance criteria ambiguity on Pattern 9+10 catalog inclusion status — does passing W2.6 imply v1 catalog membership or design-intent stub implementation? KR must clarify in rocket Wave 2 dispatch: Pattern 9+10 = design-intent stubs at starting estimates; catalog inclusion (v1 vs v1.1) is gamora SC-7 decision post-Wave-3-baseline |
| I1 | INFO | W2.4 gate "cross-validation with starter pattern-library entries" does not specify entry count; KR dispatch should specify 5 Pass-1 + 8 Pass-2 = 13 starter entries as the minimum cross-validation scope |
| I2 | INFO | Elrond's role in "statistical priors (elrond-cooperated)" is mentioned in §§ 5.2 and 11.1 but is not surfaced in W2.4 sub-wave as a cross-seam dependency. Wave 2 dispatch should note the elrond statistical-priors input as a prerequisite or concurrent dependency |
| I3 | INFO | § 11.5 LLM raw-reasoning constraint correctly prohibits LLM for synergy SCORING; permits LLM for T4 NAMING post-generation. The naming step is not represented in W2.0-W2.9 sub-wave structure (naming appears to be post-Wave-2 scope). KR should confirm whether LLM naming is a Wave 2 sub-wave or a Wave 3+ item; if Wave 2, a W2.10 sub-wave should be added |
| I4 | INFO | Doc 43 is the first Wave 2 design-intent doc in the Cycle 13 pattern; it does not note whether the dual-consumer pattern (T4 generation + legendary added-skill generation; § 5.6) requires elrond or star-lord coordination for the legendary added-skill side. Wave 3+ scope or Wave 4; but KR should flag this as a future cross-seam dependency in the Cycle 13 scope-doc |
| I5 | INFO | SC-2 engineering-discipline ratification (#31 + #32) is still marked "awaiting jack-ryan SC-2 expansion ratification" in doc 40 § 12.1. Doc 43 cites #31 + #32 as operating disciplines throughout. SC-2 ratification is not blocking Wave 2 implementation (the disciplines are empirically well-founded); but SC-2 should fire before Wave 3 to avoid the ratification debt accumulating across multiple waves |

---

## Rationale

**PASS-with-WARN (not BLOCK) on framing-audit absence (W1):** The three-question answers are available and do not surface a design contradiction or principle violation. The missing section is a documentation pattern regression relative to doc 42 precedent; it does not make doc 43 incorrect or ambiguous on any architectural point. BLOCK threshold requires a principle violation or a conflict with a locked decision — not met here.

**PASS-with-WARN (not BLOCK) on Pattern 9+10 catalog ambiguity (W2):** The ambiguity is in the rocket dispatch acceptance criteria framing, not in doc 43 itself (§ 12 close criterion correctly says "design-intent depth"). The risk is a KR dispatch authoring omission, addressable pre-fire. No architectural invalidity in doc 43.

**PASS on all 11 dimensions:** I2 routing requirements are fully honored; W3 routing requirements are fully honored; I1 carryover is fully honored. Architectural alignment with doc 40 § 8 post-amendments, closeout locks, SC-4 expansion, and wave precedent doc 42 is confirmed by empirical inspection. No conflicts with locked decisions found.

**Cite:** Review Principles 1-5. Disciplines #1.2 / #11 / #18 / #18.2 / #23 / #26 / #27 / #29 / #30 / #31 / #32. ADR-002 (direct APPROVE — design-discussion canonical doc; within-seam ownership; no cross-seam schema change in this Gate-1 artifact itself).

---

## Action

- [ ] **Gandalf (W1 — recommended before Wave 3 dispatch authoring):** Amend doc 43 with a § 11.9 framing-audit subsection answering the Discipline #23 three-question protocol: (Q1) what evidence would refute the 3-category taxonomy shape; (Q2) cheapest refuting test (W2.9 round-trip output: count Phase-3-minimum-threshold triggers across 22 BC-target cells × 2 cohorts; >20% rate signals taxonomy constraint risk); (Q3) alternative framing (resolved: 6-strategy as algorithm detail + 3-category as player-facing/design-spec is the locked framing per closeout 2026-05-27). This preserves the doc 42 framing-audit pattern for future doc-41/43/44 readers.
- [ ] **KR (W2 — required in rocket Wave 2 implementation dispatch):** W2.6 acceptance criteria must explicitly state: "Pattern 9 + Pattern 10 are implemented as design-intent stubs at starting-estimate thresholds. Catalog inclusion (v1 vs v1.1) is gamora SC-7 decision post-Wave-3-baseline. Passing W2.6 gate DOES NOT constitute v1 catalog membership."
- [ ] **KR (I1 — include in W2.4 dispatch scope):** Specify 5 Pass-1 + 8 Pass-2 = 13 starter pattern-library entries as the minimum cross-validation scope for W2.4 gate. Prevents rocket from interpreting "starter entries" as a subset.
- [ ] **KR (I2 — include in W2.4 dispatch scope):** Surface elrond statistical-priors input as a prerequisite or concurrent dependency in W2.4 sub-wave. Prevents elrond handoff from being treated as post-W2.4 rather than as a W2.4 input.
- [ ] **KR (I3 — confirm scope allocation):** Confirm whether LLM T4 naming (§ 11.5) is Wave 2 scope (add W2.10) or Wave 3+ scope. If deferred, document the deferral in the Cycle 13 scope-doc.
- [ ] **KR (I4 — flag in Cycle 13 scope-doc):** Note the dual-consumer pattern (§ 5.6 legendary added-skill generation side) as a future cross-seam dependency requiring elrond / star-lord coordination. Prevents this from being rediscovered at Wave 4 as a surprise scope item.
- [ ] **KR (I5 — advisory; before Wave 3 dispatch authoring):** Fire SC-2 engineering-discipline ratification (#31 + #32) before Wave 3 to avoid multi-wave ratification debt.

---

## Next-action sequence for KR

1. **Verdict: PASS-with-WARN.** Wave 2 implementation dispatch authoring is UNBLOCKED.
2. Route W1 to gandalf for doc 43 § 11.9 framing-audit amendment (minor; one subsection; does not block rocket fire).
3. Proceed to authoring rocket Wave 2 implementation dispatch incorporating:
   - W2 (Pattern 9+10 catalog-stub-not-membership language in W2.6 acceptance criteria)
   - I1 (13-entry starter pattern-library cross-validation scope)
   - I2 (elrond statistical-priors as W2.4 concurrent dependency)
   - I3 (LLM naming scope allocation decision)
4. Flag I4 in Cycle 13 scope-doc (dual-consumer pattern cross-seam dependency)
5. Queue SC-2 discipline ratification (#31 + #32) before Wave 3 dispatch authoring

---

## References

- `/Users/admin/Games/reincarnated-collaboration/canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — critiqued artifact (708 lines; 14 sections; read in full across 4 batches)
- `/Users/admin/Games/reincarnated-collaboration/canonical/40-gear-balance-guide-architecture-2026-05-26.md` — § 8 / § 8.4 / § 8.4.1-3 / § 8.2 / § 8.3 / D66 / D76 / D83 / § 12.1 spot-checked (grep + targeted read)
- `/Users/admin/Games/reincarnated-collaboration/canonical/00-ground-state.md` — § 1 doc 43 row verified (read)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — §§ 1.3 / 1.4 / 1.7 / 2.4 / 2.5 / 7 verified (read in full)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` — Topic 2 §§ 2.2-2.3 + Topic 3 §§ 3.4-3.5 cross-referenced (read in full)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md` — I2 / W3 / I1 / I3 routing requirements verified (read in full)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-partition-gate-2.md` — I1 legendary_t0_5 carryover + WARN-pattern partial-remediation status verified (read in full)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 / #1.2 / #11 / #18 / #18.2 / #23 / #26 / #27 / #29 / #30 / #31 / #32 (canonical authority; cited by number throughout)

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**Gate-1 verdict:** PASS-with-WARN
**Severity counts:** INFO=5 / WARN=2 / BLOCK=0
