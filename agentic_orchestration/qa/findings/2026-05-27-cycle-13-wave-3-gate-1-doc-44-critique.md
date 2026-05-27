# Finding — 2026-05-27 — Cycle 13 Wave 3 Gate-1 Critique: Doc 44 T4 Algorithm Phase 3 Design INTENT

**Reviewer:** jack-ryan
**Severity:** PASS-with-WARN (0 BLOCK; 1 WARN; 5 INFO)
**Target:** commit `a80044a` — `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md`
**Developer:** gandalf
**Principles applied:** Principles 1 / 2 / 3 / 4 / 5 / 6; Disciplines #1 / #1.2 / #11 / #18 / #18.2 / #23 / #26 / #27 / #29 / #31 / #32

---

## Verdict

**PASS-with-WARN.** Rocket Wave 3 implementation dispatch authoring may proceed. One WARN condition (W1 — "multiplier strategies" key ambiguity in `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` dict) must be folded into rocket Wave 3 dispatch acceptance criteria before rocket fires. Five INFO items are notes for the record — no blocking action. This doc successfully implements the Wave 2 Gate-1 W1 lesson (§ 11 framing-audit INCLUDED FROM START; not an amendment-pattern repeat). All 11 critique dimensions assessed.

---

## What I found — 11 critique dimensions

### D1 — Architectural alignment (Discipline #18 + #11) — doc 44 vs doc 40 § 8.2 + closeout §§ 1.3 / 1.4 / 2.4

**Verdict: INFO.**

Empirical spot-check performed at doc 40 § 8.2 Phase 3 framing (D81 canonical form), closeout §§ 1.3 (one-T4-active; D66 sharpening), 1.4 (variable 3-or-4 chains), 2.4 (3-category taxonomy substrate), and Wave 2 Gate-2 finding (PASS + WARN-pattern REMEDIATED milestone).

**Confirmed aligned:**

- Phase 3 = "biggest design risk" framing: doc 40 § 8.2 Phase 3 column states "Character-wide vs chain-wide scope dimension (variance generator; biggest design risk)." Doc 44 § 0 TL;DR and § 2.3 operationalize this framing explicitly. Aligned.
- D81 canonical form (4 phases, all in Cycle 13): doc 40 D81 confirms "all 4 phases in Cycle 13." Doc 44 § 10 states "Wave 3 IS Phase 3 of the 4-phase canonical form; Wave 3 close unlocks Phase 4." Aligned.
- Closeout § 1.3 (one-T4-active): doc 44 § 5.3 mitigation 3 operationalizes one-T4-active gating as a complexity bound on scope-dimension. D66 sharpening cited. Aligned.
- Closeout § 1.4 (variable 3-or-4 chains): magnitude downscaling formula `1 / sqrt(class_chain_count)` in doc 44 § 4.5 correctly parameterizes for both 3-chain and 4-chain cases. Aligned.
- Closeout § 2.4 (3-category taxonomy substrate): doc 44 §§ 2.1-2.2 preserves the 3-category taxonomy as orthogonal layer (not superseded). Aligned.
- WARN-pattern REMEDIATED milestone: doc 44 § 8.3 + § 7 W3.5 gate + Wave 3 close criterion all include "WARN-pattern REMEDIATED milestone PRESERVED" as explicit CRITICAL requirement. Aligned.

**No drift found across any spot-checked cross-reference.** Doc 44 is a faithful operationalization of doc 40 § 8.2 Phase 3 + closeout locks.

**Cite:** Discipline #11 (empirical inspection performed at doc 40 + closeout doc sections; not inferred from doc 44 summary).

---

### D2 — Scope-dimension orthogonality verification (§ 2 + § 11 Q3 framing)

**Verdict: INFO.**

The character-wide vs chain-wide scope dimension is presented as orthogonal to the Wave 2 3-category taxonomy: every T4 candidate carries BOTH a category (A/B/C) and a scope value (CHARACTER_WIDE / CHAIN_WIDE_OWN / CHAIN_WIDE_PARALLEL). Verified:

- Orthogonality claim (§ 2.1): Category A scope FIXED at character-wide (no scope selection branch); Categories B/C scope eligible per strategy flags. The category × scope cell space is 3 × 3 = 9 cells, not 3 (Wave 2 only) and not 21 (all strategies × scope). The structural constraint (Category A scope is FIXED) reduces this to 1 + 4 × 2 = meaningful compression of the search space.
- Non-redundancy with Wave 2 parallel-chain reach: doc 44 § 3.3 + § 6 composition table cleanly distinguishes chain-wide-PARALLEL (Wave 2 W2.3 `ParallelChainTarget.PARALLEL`) from character-wide (Wave 3 new). The scope-dimension collapses rather than duplicates parallel-chain reach by making CHAIN_WIDE_PARALLEL the unified scope value for both Wave 2 and Wave 3 reads. Non-redundant; compositionally coherent.
- § 11 Q3 alternative-framing: the 5-category framing alternative (scope-as-category vs scope-as-dimension) is resolved with 4-point reasoning that holds. Point 1 (Wave 2 3-category intactness), Point 2 (player-facing comprehensibility), Point 3 (implementation cost), and Point 4 (parallel-chain composition coherence) are each independently load-bearing. No contradiction with locked Wave 2 taxonomy.

**No orthogonality failure found.**

**Cite:** Discipline #11 (spot-check of §§ 2.1, 3.3, 6 against Wave 2 doc 43 § 4 precedent; not inferred). Principle 4 (Q3 resolution consistent with Wave 2 locked decisions).

---

### D3 — Per-category scope-dimension applicability (§ 3)

**Verdict: INFO.**

Verified § 3 against the 3-category taxonomy locked in Wave 2 doc 43 § 2 and rocket's `t4_category_schema.py` CATEGORY_A_STRATEGIES / CATEGORY_B_STRATEGIES / CATEGORY_C_STRATEGIES constants (empirically inspected: 4 Category A strategies, 2 Category B strategies (GEOMETRY_COLLAPSE + skill-specific TRADE_OFF via flag), 2 Category C strategies (ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION)).

**Applicability matrix (§ 3.1):**

- Category A scope FIXED at character-wide: correct. Category A strategies (RESOURCE_CONVERSION, DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, class-wide TRADE_OFF) are character-wide by category definition per Wave 2. Adding chain-wide scope to Category A would violate Discipline #31 separability (chain-wide effect = restatement of character-wide effect). Correctly excluded.
- Categories B/C default chain-wide-OWN, eligible for character-wide or chain-wide-PARALLEL: correct. Preserves Wave 2 default surface.

**Per-strategy eligibility (§ 3.2):**

- GEOMETRY_COLLAPSE excluded from character-wide: correct and well-reasoned. "All your skills become projectiles" would produce unplayable kits — the genre precedent (PoE geometry-based keystones are always per-skill-type, never all-skill) supports this.
- ELEMENT_CONVERSION and DUAL_ELEMENT_ADDITION eligible for character-wide: correct per PoE "all skills deal cold" / D4 Aspect of Frozen Wake precedent.
- Skill-specific TRADE_OFF and Multiplier strategies eligible for character-wide (with magnitude downscaling): consistent with PoE keystones (Elemental Overload, Resolute Technique) that are character-wide.

**No contradiction with Wave 2 implementation found.**

**Cite:** Discipline #11 (empirical inspection of `t4_category_schema.py` CATEGORY_A/B/C_STRATEGIES constants at lines 79-97 against § 3.1/3.2 applicability claims).

---

### D4 — Scope-dimension selection algorithm depth (§ 4)

**Verdict: INFO (implementation-ready).**

6-step algorithm assessed for rocket-fire-without-re-clarification standard:

| Step | Spec completeness | Assessment |
|---|---|---|
| Step 1 — Applicability bound | Branch per category (A → fixed; B/C → eligible set per § 3.2) | Fully specified. Rocket can implement directly. |
| Step 2 — Cohort-archetype prior | Prior weights table (4 cohorts × 3 scopes) | Fully specified as starting estimates; gamora SC-7 delegation per #18.2 correctly noted. |
| Step 3 — Per-scope synergy scan candidate gen | Pass 1 scope-coverage-fit entry + Pass 2 scope-promotion-trap + scope-dilution-trap | Fully specified. Pattern entries are gandalf-curated; rocket extends existing catalogs. |
| Step 4 — Cohort-weighted score selection + tie-breaker | `score × (1 + prior_weight)`; tie-breaker within ±5% → chain-wide-OWN default | Fully specified. Formula is arithmetic; tie-breaker consistent with Wave 2 doc 43 § 4.5. |
| Step 5 — Magnitude downscaling | `1 / sqrt(class_chain_count)` for multiplier + DUAL_ELEMENT_ADDITION + TRADE_OFF gain; ELEMENT_CONVERSION = no change | Fully specified. Starting estimate with gamora SC-7 delegation per #18.2. |
| Step 6 — Option F Retry 4 scope-flip | scope-flip ordering per § 4.6 (character-wide if eligible → PARALLEL → OWN) | Fully specified. Retry count extends to 4; OPTION_F_PHASES count PRESERVED at 4 (Phase 1 internal retry count expands — no phase count change). |

**No clarification dispatch required.** Rocket can fire from § 4 spec.

**Minor note (INFO, not WARN):** cohort prior weight application formula in Step 4 (`score × (1 + prior_weight)`) means the prior is multiplicative-on-top-of-net-synergy-score. For candidates with negative net synergy score (resolve < create), multiplying by `(1 + prior_weight)` makes the score MORE negative for preferred cohorts. This may produce unintuitive ordering when all scope candidates have negative net synergy scores (all fail Pass 2 threshold). Doc 44 does not specify the fallback behavior when ALL scope candidates produce negative cohort-weighted scores. This is an edge-case behavior question for rocket to resolve at W3.3 implementation time; gamora SC-7 calibration will surface whether this occurs empirically. Not blocking.

**Cite:** Discipline #1.2 (spec claims cross-reference Wave 2 code-line citation pattern: §§ 4.4 cite `1 / sqrt(N)` formula tied to § 8.2 math note requirement — correct; math note required BEFORE W3.1 schema implementation).

---

### D5 — Biggest-design-risk handling (per D81 Phase 3 + 4-mitigation bundle)

**Verdict: INFO.**

4-mitigation bundle assessed for defensibility against the 6 risk vectors enumerated in § 2.3:

| Risk vector | Mitigation coverage | Assessment |
|---|---|---|
| Combinatorial expansion | Mitigation 1: architectural bounding (~50% reduction; 63 → ~30 valid cells) | Solid. Category A scope-fixity alone removes 3 cells (A × OWN + A × PARALLEL + 2 more from GEOMETRY_COLLAPSE). Math is right: 63 nominal cells, ~30 valid per constraints. |
| Parallel-chain reach interaction | § 3.3 composition + § 8.5 schema-coherence Option A coherence rule | Addressed. CHAIN_WIDE_PARALLEL collapses with Wave 2 `ParallelChainTarget.PARALLEL` via coherence rule; `__post_init__` validator enforces. |
| Cohort-archetype preference shaping | Mitigation 2: cohort priors + synergy-scan dominance note | Addressed. Priors shape but do not mandate; synergy scan dominates. R4 refutation criterion in § 11 Q1 names what evidence would invalidate. |
| One-T4-active gating amplification | Mitigation 3: complexity bounded to one scope per active-T4 instance | Addressed. 3^k collapse to 3 cells correctly stated; spirit-guide projection messaging example is helpful for rocket. |
| Pattern 9 / Pattern 10 expanded-scope risk | Mitigation 2 (scope-amplification extension): scope-amplification attribution at expanded-scope effective rates | Addressed. Detection logic extends to `(effective_multiplier × class_chain_count)` check and `(per_chain_DoT × N × max_stack)` check. WARN-not-BLOCK preserved per Wave 2 Gate-2 D2. Pattern count PRESERVED at 2 per Wave 2 WARN-pattern REMEDIATED discipline. |
| Spirit-guide projection surface complexity | § 5.3 messaging example | Addressed at spec-intent level; full implementation is Wave 3 telemetry emission per § 8.6. |

**All 6 risk vectors have identifiable mitigation coverage.** The mitigations are coherently composed and do not contradict each other.

**Cite:** Discipline #11 (empirical cross-check of 6 risk vectors against 4 mitigations performed; not inferred from summary). Discipline #18.2 (gamora SC-7 calibration timing is correctly sequenced AFTER Wave 3 baseline).

---

### D6 — Composition with Wave 2 outputs (§ 6)

**Verdict: INFO.**

§ 6 composition table verified against Wave 2 rocket implementation (commits `2445bad` + `7287b43`):

| Wave 2 surface | Wave 3 composition claim | Verified |
|---|---|---|
| `T4Category` enum (A/B/C) | Preserved unchanged | PASS — scope sits orthogonal; category composition rule unchanged |
| `ALL_T4_STRATEGIES` 7-strategy registry | Preserved; scope eligibility flag added per strategy | PASS — no 8th strategy added; per-strategy flag is additive |
| `ParallelChainTarget` enum (OWN/PARALLEL) | Collapses into `T4Scope` per § 8.5 coherence rule | PASS — Option A preferred; backward-compat maintained |
| `PASS_1_CATALOG` (5 entries) | Extended to 6 (+ scope-coverage-fit) | PASS — module-load `assert len == 6` specified |
| `PASS_2_CATALOG` (8 entries) | Extended to 10 (+ scope-promotion-trap + scope-dilution-trap) | PASS — module-load `assert len == 10` specified |
| `DEGENERATE_DETECTION_PATTERNS` (2 entries) | Detection logic EXTENDED; count PRESERVED at 2 | PASS — scope-amplification is detection-logic extension, not new pattern entry |
| `OPTION_F_PHASES` (4 phases) | Phase count PRESERVED at 4; Phase 1 retry count expands 3 → 4 | PASS — rocket's `max_retries` internal to Phase 1 extends; `OPTION_F_PHASES` length stays 4 |
| `T4CandidateV2` schema | `t4_scope: T4Scope` field added with backward-compat default | PASS — field-addition pattern mirrors W2.3 `parallel_chain_mode` precedent |

**All Wave 2 surfaces preserve contract. No breaking change identified.** MIGRATION.md filing per ADR-004 correctly called out as required (additive contract change; existing consumers unbroken but MIGRATION.md documents the `t4_scope` field addition for downstream consumers of Wave 4+).

**Cite:** Discipline #11 (empirical read of Wave 2 `t4_category_schema.py` lines 49-100 confirming 7 strategies, 4 Category A, 2+2 Category B/C before verifying § 6 composition claims). ADR-004 (cross-seam contract change — MIGRATION.md required; correctly called out in W3.5 acceptance criteria).

---

### D7 — Sub-wave structure W3.0-W3.5 implementation-readiness (Discipline #1.2)

**Verdict: INFO (with one scoped observation).**

6 sub-waves assessed against rocket-fire-without-re-clarification standard:

**W3.0 (substrate prep):** target scope (review Wave 2 outputs; identify extension points), owner (rocket), gate (substrate prep audit committed). Sufficient. No ambiguity.

**W3.1 (schema extension):** target scope (T4Scope enum + t4_scope field + STRATEGY_CHARACTER_WIDE_ELIGIBILITY constant + math note per #1), owner (rocket), gate (jack-ryan Gate-1 on schema + math note PASS). Sufficient. Math note required BEFORE schema implementation — correctly specified.

**W3.2 (per-category applicability):** target scope (§ 3 applicability matrix encoded; Category A scope FIXED; B/C scope-eligibility branch), owner (rocket), gate (jack-ryan Gate-1; per-category path tests). Sufficient.

**W3.3 (selection algorithm + biggest-design-risk mitigation):** target scope (6-step algorithm + 4 mitigations + catalog extensions + module-load asserts). This is the heaviest sub-wave. Owner (rocket), gate (jack-ryan Gate-1; test coverage per-scope + cohort prior + downscaling + Retry 4 + Pattern 9+10 scope-amplification). The work-unit is densely specified — rocket may need to scope W3.3 into two atomic units (algorithm implementation vs mitigation bundle implementation) at dispatch time. Not a blocking ambiguity; KR should note this in the rocket dispatch.

**W3.4 (cross-cohesion validation):** gamora + jack-ryan dual ownership. Gamora spot-check sim across 4 cohort × 3 scope cells; validation criteria named (per-cohort scope distribution + no structural lockout + Pattern 9+10 WARN-rate <15% per cohort × scope cell). Gate is jack-ryan Gate-2 PASS on cross-cohesion. Sufficient; gamora ownership of sim is clear.

**W3.5 (round-trip smoke):** 10-rarity coverage (legendary_t0_5 explicitly named), scope variants, MIGRATION.md, WARN-pattern REMEDIATED maintenance. Gate is jack-ryan Gate-2 PASS. Sufficient and comprehensive.

**Scoped observation (INFO, not WARN):** W3.3 acceptance criteria does not specify how many tests are sufficient to exercise the cohort-prior weighting path. W2.4 precedent in Wave 2 dispatch was clarified by I1 (13-entry cross-validation scope). KR rocket Wave 3 dispatch should specify minimum: at least 4 cohort × 2 eligible-scope = 8 cohort × scope combinations verified for synergy-score + cohort-prior-weighting path. Prevents rocket from validating a single cohort and declaring the prior implementation sufficient.

**Cite:** Discipline #1.2 (sub-wave work-units are spec-level; no code-line claims made in intent doc — appropriate; rocket authors math note + code-line citations at W3.1).

---

### D8 — § 11 Discipline #23 framing-audit verification (INCLUDED FROM START — verify gandalf claim)

**Verdict: INFO.**

**Claim verified:** § 11 IS included from start in doc 44. Not an amendment-pattern repeat of Wave 2 Gate-1 W1 (which surfaced the absence of framing-audit in doc 43 and required a post-Gate-1 amendment).

**Three-question protocol quality (applied per Discipline #23):**

**Q1 (what would refute):** 5 refutation criteria R1-R5 are named and each meets the standard of being a genuine refutation of the load-bearing framing assumption (orthogonal scope-dimension). R1 (Category-A-scope-variance requirement), R2 (>25% character-wide WARN-rate), R3 (genre precedent refutation), R4 (cohort-archetype scope-preference uniformity), R5 (schema-coherence violation between `t4_scope` and `parallel_chain_mode`). All five are independently meaningful refutations. Quality: PASS.

**Q2 (cheapest refuting test):** refutation cost is explicitly given for each R1-R5. Notably: R2 and R4 costs are "zero" (piggyback on W3.4 + W3.5 existing deliverables per § 8.6 telemetry); R1 and R5 surface at W3.1 design-spec review before W3.2 implementation (15-30 min cost). The cheapest-refuting-test discipline (Discipline #19.1) is honored — refutation is instrument-able from existing sub-wave outputs. Quality: PASS.

**Q3 (alternative framing):** the 5-category alternative is clearly named and resolved with 4-point reasoning (Wave 2 intactness + player-facing comprehensibility + implementation cost + parallel-chain composition). Each point is independently load-bearing. The resolution is an explicit design-call, not a dismissal. Quality: PASS.

**Framing-audit verdict:** the three-question protocol is properly applied at the structural layer. The framing-audit does not surface any BLOCK condition. The "INCLUDED FROM START" claim is accurate and the quality exceeds the doc 43 § 11.9 amendment pattern (which was added post-Gate-1). Doc 44 correctly names this as the "from-start expectation as Wave 3+ baseline."

**Cite:** Discipline #23 (three-question protocol applied; framing-audit at load-bearing-framing-commitment work-unit). Discipline #19.1 (cheapest refuting tests named per R-criterion type; verified against W3.4 + W3.5 telemetry emission spec).

---

### D9 — T4CandidateV2 extension choice (§ 8.5 field-addition Option A)

**Verdict: WARN (W1) — "multiplier strategies" key ambiguity in `STRATEGY_CHARACTER_WIDE_ELIGIBILITY`.**

**Option A selection (keep both fields + coherence rule) — SOUND:** preserves Wave 2 backward compatibility; coherence rule enforced via `__post_init__` validator; mirrors W2.3 `parallel_chain_mode` precedent. Option B correctly rejected (breaking change to Wave 2 consumers). Schema-coherence guidance is clear.

**Issue found (W1):** Doc 44 § 3.2 enumerates "Multiplier strategies" as a character-wide-eligible Category B strategy. However, `ALL_T4_STRATEGIES` in `t4_category_schema.py` (lines 49-58) does NOT have a `STRATEGY_MULTIPLIER` or equivalent discrete string constant. The 7 strategies are: RESOURCE_CONVERSION, TRADE_OFF, ELEMENT_CONVERSION, DEFENSIVE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_TRADEOFF, DUAL_ELEMENT_ADDITION. "Multiplier strategies" does not correspond to a named strategy string.

This creates a key-mapping ambiguity: when rocket authors `STRATEGY_CHARACTER_WIDE_ELIGIBILITY: dict[str, bool]`, what key(s) map to "multiplier strategies"? The Wave 2 CATEGORY_B_STRATEGIES constant contains only GEOMETRY_COLLAPSE and TRADE_OFF (skill-specific via flag). The "multiplier strategies" language in doc 43 § 2.2 ("Multiplier strategies | B | Chain-specific: large multiplicative event") appears to be a conceptual grouping, not a discrete strategy string. Possible interpretations: (a) "multiplier strategies" is TRADE_OFF at Category B when skill-specific; (b) it is intended as a new `STRATEGY_MULTIPLIER` constant to be introduced in Wave 3; (c) it is covered by the skill-specific TRADE_OFF variant with params.

Doc 44 § 8.3 asserts `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count = 4 (TRADE_OFF + Multiplier + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION; GEOMETRY_COLLAPSE = false; Category A strategies = N/A). If "Multiplier" = skill-specific TRADE_OFF (Category B), that gives 4 eligible keys among the B/C strategies — plausible. But the module-load `assert len(STRATEGY_CHARACTER_WIDE_ELIGIBILITY) == 7` (all 7 strategies in the dict) AND `assert true_count == 4` must be reconcilable with the actual strategy constants in the code. Rocket needs explicit guidance on whether "multiplier strategies" is:

- The existing `STRATEGY_TRADE_OFF` when `is_class_wide_trade_off = False` (i.e., skill-specific context); OR
- A NEW `STRATEGY_MULTIPLIER` constant to be introduced in Wave 3 W3.1

If interpretation (a), the true-count = 4 assertion holds but requires TRADE_OFF to count twice in the eligibility dict (once as Category A "class-wide TRADE_OFF" = not eligible; once as Category B "skill-specific TRADE_OFF" = eligible). But the dict is keyed by strategy string — TRADE_OFF is one key. The eligibility flag would need to be True for TRADE_OFF (because it's eligible when Category B) but N/A or False when Category A. This is a context-dependent flag, which a static `STRATEGY_CHARACTER_WIDE_ELIGIBILITY: dict[str, bool]` dict cannot correctly represent without additional context.

If interpretation (b), a new constant must be introduced at W3.1 — but this would extend `ALL_T4_STRATEGIES` from 7 to 8, breaking the doc 44 § 8.3 assertion that `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` keys count = 7. Contradiction.

**WARN W1:** KR must resolve this before rocket fires W3.1. Recommend: KR queries gandalf for clarification (one short design-clarification exchange; not a re-dispatch). Likely intended answer: "multiplier strategies" = skill-specific TRADE_OFF in Category B context (interpretation a); the `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` dict maps `STRATEGY_TRADE_OFF → True` (eligible when used as Category B/C; N/A distinction for Category A is enforced by applicability branch in Step 1, not by the eligibility dict). KR should fold the resolved interpretation into the rocket W3.1 acceptance criteria with explicit language: "STRATEGY_CHARACTER_WIDE_ELIGIBILITY maps all 7 strategy keys; Category A strategies (RESOURCE_CONVERSION, DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, TRADE_OFF when class-wide) are keyed but scope selection is bypassed by Step 1 applicability bound; among Category B/C strategies, eligible keys are: TRADE_OFF (when skill-specific, i.e., Category B), [Multiplier = resolved interpretation], ELEMENT_CONVERSION, DUAL_ELEMENT_ADDITION; GEOMETRY_COLLAPSE = False."

**Cite:** Discipline #11 (empirical read of `t4_category_schema.py` lines 49-100 confirming no STRATEGY_MULTIPLIER constant exists; "multiplier strategies" language in doc 43 § 2.2 + doc 44 § 3.2 is not a discrete strategy string). Discipline #1.2 (implementation claims must be traceable to code-line references; this claim is not yet traceable until W1 is resolved).

---

### D10 — WARN-pattern REMEDIATED preservation

**Verdict: INFO.**

**WARN-pattern REMEDIATED milestone preservation verified across three distinct doc 44 sections:**

- § 8.3 (Discipline #11 empirical inspection): "Every post-script empirical count assertion in completion record MUST verify against actual code state via `len()` or equivalent at write-time." 10 asserted counts enumerated. Module-load `assert len(X) == N` pattern explicitly required. Framing: CRITICAL. Identical to Wave 2 pattern.
- § 7 W3.5 gate: "post-script empirical count assertions per Discipline #11 (CRITICAL: maintain WARN-pattern REMEDIATED milestone — Wave 3 Gate-2 = 0 empirical assertion failures; module-load `assert len()` for all extended catalogs)." CRITICAL classification present.
- Wave 3 close criterion: "WARN-pattern REMEDIATED milestone PRESERVED per Discipline #11 (Wave 3 Gate-2 = 0 empirical assertion failures; module-load `assert len()` enforcement for all extended catalogs; full closure milestone maintained)." Explicit PRESERVED language.

The discipline is maintained with identical rigor to Wave 2. DEGENERATE_DETECTION_PATTERNS count PRESERVED at 2 (not 3 or 4 as might be expected from scope-amplification extension — extension is detection-logic, not new pattern entries). OPTION_F_PHASES count PRESERVED at 4 (Phase 1 retry count internal expansion). These nuanced preservation-vs-extension distinctions are correctly specified and will prevent rocket from introducing false count inflation.

**Cite:** Discipline #11 (empirical inspection: three separate doc 44 sections confirm WARN-pattern REMEDIATED preservation; correct distinction between logic-extension and entry-count-extension for Pattern 9+10 and Option F). Wave 2 Gate-2 finding (REMEDIATED verdict; DEGENERATE_DETECTION_PATTERNS == 2; OPTION_F_PHASES == 4 — both baselines preserved correctly in doc 44).

---

### D11 — Cross-doc consistency + framing-audit quality (Discipline #11 + #23)

**Verdict: INFO.**

Cross-doc consistency spot-check:

| Cross-reference | Verified | Status |
|---|---|---|
| Doc 40 § 8.2 Phase 3 framing (D81 Phase 3 = "biggest design risk") | Spot-checked doc 40 § 8.2 Phase 3 column + D81 row | ALIGNED |
| Closeout § 1.3 (one-T4-active D66 sharpening) | Spot-checked closeout § 1.3 against doc 44 § 5.3 | ALIGNED |
| Closeout § 1.4 (variable 3-or-4 chains) | Spot-checked closeout § 1.4 against doc 44 § 4.5 downscaling formula | ALIGNED |
| Closeout § 2.4 (3-category taxonomy substrate) | Spot-checked closeout § 2.4 against doc 44 §§ 2.1-2.2 | ALIGNED |
| Doc 43 Wave 2 taxonomy + synergy scan + Option F | Spot-checked doc 44 § 6 composition table against doc 43 §§ 2, 5, 6 | ALIGNED |
| Wave 2 Gate-2 REMEDIATED verdict | Spot-checked doc 44 §§ 7 W3.5 + 8.3 + close criterion | ALIGNED |
| Wave 2 Gate-1 W1 (framing-audit amendment lesson) | Spot-checked doc 44 § 11 and § 10 Discipline #23 row | ALIGNED — lesson implemented; doc 44 § 11 is from-start, not amendment |
| Wave 2 Gate-2 W1 (synthetic same-bucket test gap) | Not referenced in doc 44 | NOTED — this was a rocket follow-on amendment item; not a doc 44 scope item; not a gap in doc 44 |
| `t4_category_schema.py:240` (T4CandidateV2 extension point) | Empirically confirmed: `T4CandidateV2` class at lines 239-295; no `t4_scope` field yet (Wave 3 adds it) | ALIGNED — field-addition extension point confirmed; doc 44 § 2.4 citation is accurate |

**No cross-doc consistency failures found beyond the D9 W1 WARN (multiplier strategies key ambiguity).**

Ground-state registration: doc 44 § 12 sign-off instructs `canonical/00-ground-state.md` registration. Not verified at review time (doc 44 is new; ground-state may or may not be updated at commit `a80044a`). INFO item: KR should confirm ground-state includes doc 44 row before rocket Wave 3 dispatch fires.

**Cite:** Discipline #11 (empirical cross-reference spot-check performed at multiple doc 40, closeout, and Wave 2 sources; not inferred from doc 44 summary).

---

## Severity summary

| ID | Severity | Finding |
|---|---|---|
| W1 | WARN | `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count = 4 assertion at § 8.3 is ambiguous because "multiplier strategies" is NOT a discrete strategy string constant in `t4_category_schema.py`; the dict's key-mapping for multiplier strategies is unresolved (TRADE_OFF context-dependent, or new constant?). KR must resolve with gandalf before rocket fires W3.1; folded resolution into rocket W3.1 acceptance criteria |
| I1 | INFO | Step 4 score multiplier formula `score × (1 + prior_weight)` produces unintuitive ordering when ALL scope candidates have negative net synergy scores (all fail Pass 2); fallback behavior unspecified in doc 44; rocket resolves at W3.3 implementation; gamora SC-7 surfaces empirically if this occurs |
| I2 | INFO | W3.3 acceptance criteria does not specify minimum cohort × scope coverage for synergy-score + cohort-prior-weighting path validation; KR rocket dispatch should specify minimum 4 cohort × 2 eligible-scope = 8 combinations as minimum cross-validation scope |
| I3 | INFO | Ground-state registration of doc 44 in `canonical/00-ground-state.md` should be confirmed before rocket Wave 3 dispatch fires; doc 44 § 12 instructs registration but was not verified empirically at review time |
| I4 | INFO | Wave 2 Gate-2 W1 WARN (synthetic same-bucket pair test gap for `_validate_separate_buckets()`) remains open per Wave 2 Gate-2 next-action sequence item 4; this is a follow-on rocket amendment item, not a doc 44 scope item; KR should confirm whether this is folded into Wave 3 dispatch or fires as standalone minor amendment dispatch |
| I5 | INFO | § 5.3 spirit-guide projection messaging spec (per-scope projection emission for spirit-guide consumption) references doc 41 D31 spirit-guide-projection language framework — Wave 3 implementation MUST emit per-scope projection data; this is correctly in W3.5 acceptance criteria; rocket and drax (spirit-guide consumer) coordination may be needed at integration time; KR should note this as a potential cross-seam touch for Wave 3+ |

---

## Rationale

**PASS-with-WARN (not BLOCK) on multiplier strategies ambiguity (W1):** The ambiguity is in the rocket implementation acceptance criteria framing, not in doc 44's architectural intent. The design intent (eligible Category B/C strategies include a multiplier-class strategy) is architecturally sound and well-grounded in genre precedent. The ambiguity is a key-naming precision gap resolvable via a short gandalf clarification before W3.1 fires. BLOCK threshold requires a principle violation or conflict with a locked decision — not met here. Architecture is sound; the gap is in implementation-spec precision.

**PASS on framing-audit verification (D8):** § 11 is from-start, quality is high, all three questions are answered at appropriate depth with named refutation criteria and cheapest-refuting-test costs. Wave 2 Gate-1 W1 lesson is fully implemented.

**PASS on Wave 2 contract preservation (D6):** all Wave 2 consumer surfaces (enum values, catalog counts, phase counts, schema fields) are preserved or additively extended. No breaking changes found. MIGRATION.md correctly required.

**PASS on architectural alignment (D1, D5):** doc 44 faithfully operationalizes doc 40 § 8.2 Phase 3 "biggest design risk" framing; all 6 risk vectors have mitigation coverage; closeout §§ 1.3/1.4/2.4 locks are correctly absorbed.

**Cite:** Review Principles 1-5. Disciplines #1.2 / #11 / #18 / #18.2 / #23 / #31 / #32. ADR-002 (direct APPROVE — design-discussion canonical doc; within-seam gandalf ownership; no cross-seam schema change in this Gate-1 artifact itself; WARN W1 is pre-implementation implementation-spec precision gap, not an architectural failure).

---

## Action

- [ ] **KR (W1 — REQUIRED before rocket W3.1 fires):** Resolve "multiplier strategies" key-mapping with gandalf in one short design-clarification exchange. Likely resolution: TRADE_OFF (skill-specific, Category B context) = the multiplier-class strategy; `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` maps TRADE_OFF → True (character-wide eligible; Step 1 applicability bound gates Category A context out of scope selection; eligibility dict is Category B/C context only). KR folds resolved interpretation into rocket W3.1 acceptance criteria with explicit key-mapping language. Also confirm the true-count assertion (doc 44 § 8.3 says = 4): Category B/C eligible strategies = TRADE_OFF (skill-specific) + [Multiplier = TRADE_OFF per resolution] = 1 unique key, ELEMENT_CONVERSION = 1, DUAL_ELEMENT_ADDITION = 1, GEOMETRY_COLLAPSE = False → actually 3 True keys among Category B/C strategies, not 4. KR should verify this count arithmetic with gandalf as part of the W1 clarification.
- [ ] **KR (I2 — include in W3.3 dispatch scope):** Specify minimum 4 cohort × 2 eligible-scope = 8 combinations as minimum cross-validation scope for cohort-prior-weighting path in W3.3 acceptance criteria. Prevents rocket from validating a single cohort.
- [ ] **KR (I3 — confirm before Wave 3 dispatch fires):** Verify `canonical/00-ground-state.md` includes doc 44 row. If not updated at commit `a80044a`, gandalf should add before rocket dispatch fires.
- [ ] **KR (I4 — sequencing decision):** Decide whether Wave 2 Gate-2 W1 synthetic same-bucket test gap folds into Wave 3 dispatch as a small rocket amendment sub-wave (W3.3 extension) OR fires as standalone minor-amendment dispatch before Wave 3. KR's sequencing call.
- [ ] **KR (I5 — advisory; note in Wave 3 dispatch):** Flag per-scope projection data emission (§ 5.3 + § 8.6) as a potential cross-seam touch requiring spirit-guide consumer (drax) coordination at Wave 3 integration time. Not a blocking item for rocket W3; surfacing for Wave 3+ planning.

---

## Next-action sequence for KR

1. **Verdict: PASS-with-WARN.** Wave 3 implementation dispatch authoring is UNBLOCKED with one pre-fire requirement.
2. **Pre-fire W1 resolution (required):** resolve "multiplier strategies" key-mapping with gandalf; confirm true-count arithmetic (likely 3 not 4); fold into rocket W3.1 acceptance criteria before dispatch fires.
3. Proceed to authoring rocket Wave 3 implementation dispatch incorporating:
   - W1 resolved interpretation in W3.1 acceptance criteria (key-mapping language + true-count assertion corrected)
   - I2 (minimum 8 cohort × scope combination coverage for W3.3 cohort-prior path)
   - I4 (Wave 2 Gate-2 W1 synthetic same-bucket test gap sequencing decision)
4. Note I3 (confirm ground-state doc 44 row before dispatch fires).
5. Note I5 (per-scope projection cross-seam touch for Wave 3+ planning).

---

## References

- `/Users/admin/Games/reincarnated-collaboration/canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` — critiqued artifact (558 lines; 13 sections; read in full across 2 batches)
- `/Users/admin/Games/reincarnated-collaboration/canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — §§ 0-3 spot-checked (Wave 2 precedent; composition verification)
- `/Users/admin/Games/reincarnated-collaboration/canonical/40-gear-balance-guide-architecture-2026-05-26.md` — § 8.2 Phase 3 column + D81 row + D76 row + Phase 3 implementation tag at § 8 bottom verified (grep + spot-check)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — §§ 1.3 / 1.4 / 2.4 verified (read in full)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` — Wave 2 Gate-2 PASS + WARN-pattern REMEDIATED verdict + W1 WARN (synthetic same-bucket gap) + D2 (Pattern 9+10 stubs) verified (read in full)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` — W1 (framing-audit absence) + W2 (Pattern 9+10 catalog ambiguity) + all 11 dimensions verified (read in full)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` — ALL_T4_STRATEGIES (lines 49-58), CATEGORY_A/B/C_STRATEGIES (lines 79-100), T4CandidateV2 (lines 239-295) empirically inspected; no STRATEGY_MULTIPLIER constant found; 7 strategies confirmed
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/t4_option_f.py` — Phase 1 retry_count internal expansion (max_retries = 3 at lines 86+107+117+131; Phase 1 retry count in implementation is 3 currently) empirically inspected; OPTION_F_PHASES count confirmation pending (doc 44 correctly specifies it PRESERVED at 4)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 / #1.2 / #11 / #18 / #18.2 / #19.1 / #23 / #26 / #27 / #29 / #31 / #32 (canonical authority; cited by number throughout)

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**Gate-1 verdict:** PASS-with-WARN
**Severity counts:** INFO=5 / WARN=1 / BLOCK=0
**WARN-pattern REMEDIATED preservation status:** SPECIFIED (doc 44 correctly frames Wave 3 preservation requirement; Gate-2 verifies empirically)
**Framing-audit status:** INCLUDED FROM START — quality PASS; Wave 2 Gate-1 W1 lesson fully implemented
**Key pre-fire action:** W1 "multiplier strategies" key-mapping resolved with gandalf; true-count arithmetic confirmed before rocket W3.1 fires
