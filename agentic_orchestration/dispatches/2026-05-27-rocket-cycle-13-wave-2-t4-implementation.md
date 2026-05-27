# Dispatch — 2026-05-27 — rocket — Cycle 13 Wave 2 T4 Algorithm Implementation (W2.0-W2.9 Bundled)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 2 Gate-1 verdict PASS-with-WARN (commit `f9ead71`) on doc 43 + jack-ryan Wave 1 Gate-2 I1 carryover (legendary_t0_5) + W2 + I1 + I3 amendments folded into THIS dispatch + elrond concurrent dependency for W2.4 priors per I2
**Estimated effort:** ~16-32 hrs bundled implementation (10 sub-waves W2.0-W2.9; mirror Wave 1 bundled pattern; rocket may sub-checkpoint per logical chunk)
**Acceptance:** Wave 2 T4 algorithm implementation landed per doc 43 (§ 10 sub-wave structure); 3-category T4 taxonomy + DUAL_ELEMENT_ADDITION strategy + parallel-chain reach + compositional synergy scan two-pass + T4-failure-handling Option F + Pattern 9+10 generation-time detection + one-T4-at-a-time gating + variable 3-or-4 chain architecture + integration with Wave 1 partition schema + round-trip smoke per Principle 6 including legendary_t0_5 rarity

## Context

Cycle 13 Wave 2 = T4 algorithm Phases 1-2 implementation per framing brief § 3 Wave 2 + doc 43 (gandalf-authored INTENT canonical; commit `6a97087`) + jack-ryan Wave 2 Gate-1 PASS-with-WARN verdict (commit `f9ead71`).

**Per jack-ryan Wave 2 Gate-1 fold-ins (REQUIRED in THIS dispatch per next-action sequence):**

- **W2 amendment (WARN — KR fold-in):** W2.6 acceptance criteria must EXPLICITLY state "Pattern 9+10 are design-intent stubs at starting-estimate thresholds; v1 vs v1.1 catalog inclusion is gamora SC-7 decision post-Wave-3-baseline." Rocket MUST NOT over-commit on Pattern 9+10 implementation depth beyond design-intent stubs at this Wave 2.

- **I1 INFO (KR fold-in):** 13-entry starter pattern-library cross-validation scope for W2.4 compositional synergy scan. Rocket implements W2.4 against gandalf-curated 13-entry pattern library (per doc 43 § 5 + closeout § 2.5 + AI-tell discipline D7); not LLM raw-reasoning.

- **I2 INFO (CONCURRENT dependency):** elrond statistical co-occurrence priors are a W2.4 concurrent dependency per AI-tell line (D7) — pattern library (gandalf-curated) + statistical co-occurrence priors (elrond) + algorithmic composition. Elrond statistical priors dispatch fires in parallel with rocket Wave 2 implementation; rocket integrates elrond's output at W2.4 implementation step. If elrond priors not yet landed when rocket reaches W2.4, rocket implements W2.4 with stub-priors interface (load-from-file pattern) + flags integration handoff for elrond return.

- **I3 INFO (KR fold-in):** LLM T4 naming scope allocation: clarify whether rocket Wave 2 implementation allocates LLM T4 naming OR defers to Wave 4+/Phase 5 (Cycle 14+). Per closeout: Phase 5 cohesion coalescence + Discipline #28 spirit-guide-pacing land in Cycle 14+. Wave 2 implementation should produce T4 STRUCTURE (Category A/B/C + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan output); T4 NAMING is downstream Phase 5 LLM cohesion-judge work. Rocket Wave 2 implementation: structure only; no LLM T4 naming.

**Carryover from Wave 1 Gate-2 I1 (legendary_t0_5):** W2.9 round-trip smoke + § 12 close criterion EXPLICITLY include `legendary_t0_5` rarity coverage per doc 43 (gandalf honored).

**Discipline #11 WARN-pattern full-closure target:** per jack-ryan Wave 1 Gate-2 classification "next Gate-2 = 0 empirical assertion failures." Rocket Wave 2 implementation post-script empirical count assertions MUST be 100% accurate — no count understatements or overstatements. This is the WARN-pattern full-closure opportunity.

**Doc 43 § 10 sub-wave structure W2.0-W2.9:** authoritative implementation guidance.

## Required reading before starting

1. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` (the design intent canonical; specifically § 2 3-category taxonomy + § 3 DUAL_ELEMENT_ADDITION + § 4 parallel-chain reach + § 5 compositional synergy scan two-pass + § 6 T4-failure-handling Option F + § 7 Pattern 9+10 + § 8 one-T4-at-a-time + § 9 variable 3-or-4 chain + § 10 sub-wave structure W2.0-W2.9 + § 11 implementation guidance + § 12 close criterion)
2. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` (jack-ryan Gate-1 verdict; W2 + I1 + I2 + I3 + I5 fold-in specifics)
3. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-partition-gate-2.md` (Wave 1 Gate-2; I1 legendary_t0_5 carryover; WARN-pattern partial remediation → Wave 2 = full closure target)
4. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition schema; Wave 2 T4 algorithm consumes partition modifier surface where applicable)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (architectural foundation)
6. `canonical/41-progression-framework-2026-05-27.md` (cell × node × cohort + L50 hybrid framework)
7. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.3 + § 1.7 + § 2.4 + § 2.5 + § 7 (substantive locks doc 43 operationalizes)
8. `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` (5th Scaling-interaction synergy + Pattern 9+10 substrate; rocket W2.4 + W2.6 references)
9. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code + #1.2 code-citation + **#11 empirical inspection — CRITICAL full WARN-pattern closure target** + #18 + #18.2 + #26 + #27 + #29 + #31 + #32 + Principle 6)
10. `agentic_orchestration/operating-procedures/rocket.md` (operating procedure)
11. Existing engine code paths: `reincarnated-engine/src/reincarnated/generation/` for T4 algorithm existing implementation (Cycle 11 § 8 strategy registry); `reincarnated-engine/src/reincarnated/generation/partition_schema.py` + `partition_modifier_pool.py` + `partition_roller.py` (Wave 1 partition schema integration); `reincarnated-engine/src/reincarnated/foundation/` for trait_schema.py / gear_schema.py / class_schema.py

## Math-before-code (#1 — REQUIRED)

Per Discipline #1 math-before-code, before W2.1 schema-implementation:

- [ ] Document the 3-category T4 taxonomy math: how Category A/B/C selection composes with existing 6-strategy registry; selection logic when generating T4 for a chain
- [ ] Document DUAL_ELEMENT_ADDITION strategy math: secondary element selection algorithm (element-pair compatibility per element_biases.py?); magnitude calibration starting anchors (Low 15-25% / Medium 25-40% / High 40-55% per doc 43 § 3)
- [ ] Document parallel-chain reach math: when chain-specific effect targets own-chain vs parallel-chain; algorithm-fixed-at-generation decision logic
- [ ] Document compositional synergy scan math: Pass 1 resolve-score formula + Pass 2 preserve-score formula + net = resolve - create
- [ ] Document T4-failure-handling Option F math: retry attempt count (3 per closeout § 1.7) + partial-T4-ship gate (≥1 T4 in-band per character) + quality-metric tracking
- [ ] Document Pattern 9 + Pattern 10 generation-time detection math: Pattern 9 = `<1` active skill per 10 sec → KPM proxy threshold; Pattern 10 = `>5×` expected DPS at max DoT stack → DPS-comparison threshold
- [ ] Document one-T4-unlocked-at-a-time gating math: storage representation + player-selection mechanism (deferred to D65 respec mechanism)

## Cross-seam contract change? (Principle 6 gate)

**Round-trip REQUIRED.** Wave 2 T4 algorithm implementation introduces NEW schema (T4 strategy Category A/B/C type field + DUAL_ELEMENT_ADDITION secondary-element field + parallel-chain reach target-chain field + compositional synergy scan output structure + T4-failure-handling Option F state tracking + Pattern 9+10 detection metadata + one-T4-active gating field). Composes with Wave 1 partition schema (T4-attuned legendary gear references T4 strategy categories).

**Round-trip smoke:** Generate ≥1 kit per archetype × per T4 category (Category A / B / C) including DUAL_ELEMENT_ADDITION + parallel-chain reach configurations; verify field-presence + type-consistency; verify compositional synergy scan output structured correctly; verify T4-failure-handling Option F fires correctly when WR-bracket synthetic-failure is injected. **CRITICAL per I1 carryover: include `legendary_t0_5` rarity in round-trip smoke coverage.**

**MIGRATION.md required** if cross-seam contract change per ADR-004.

## Scope (W2.0-W2.9 sub-wave structure per doc 43 § 10)

### W2.0 — Substrate prep + repo-scaffold

- [ ] Review existing T4 algorithm code (Cycle 11 § 8 strategy registry; file + line citations per Discipline #1.2)
- [ ] Identify integration points for 3-category T4 taxonomy + DUAL_ELEMENT_ADDITION strategy + parallel-chain reach + compositional synergy scan + Option F retry mechanism
- [ ] Scaffold new T4 algorithm modules per doc 43 § 10 W2.0 + existing T4 algorithm code structure

### W2.1 — 3-category T4 taxonomy schema

- [ ] Implement Category A/B/C type field on T4 strategy schema per doc 43 § 2
- [ ] Map existing 6-strategy registry to 3-category umbrella per doc 43 § 2.4: A maps RESOURCE_CONVERSION / DEFENSIVE_CONVERSION / DEFENSIVE_TRADEOFF / class-wide TRADE_OFF; B maps skill-specific TRADE_OFF / GEOMETRY_COLLAPSE / multiplier; C maps ELEMENT_CONVERSION + NEW DUAL_ELEMENT_ADDITION
- [ ] Math-note per Discipline #1 BEFORE W2.2 implementation
- [ ] Player-facing 3-category vocabulary + algorithm-implementation 6-strategy detail preserved per doc 43

### W2.2 — DUAL_ELEMENT_ADDITION strategy implementation

- [ ] Add NEW DUAL_ELEMENT_ADDITION strategy to registry per doc 43 § 3
- [ ] Implement secondary element selection algorithm (element-pair compatibility per `element_biases.py`)
- [ ] Implement magnitude calibration with starting anchors per doc 43 § 3: Low 15-25% / Medium 25-40% / High 40-55%
- [ ] Compose with #27 dual-effect (character-wide from Category A pair) + #31 separability (Category C standalone-coherent)
- [ ] Unit test: generated DUAL_ELEMENT_ADDITION T4 instance carries primary + secondary element

### W2.3 — Parallel-chain reach implementation

- [ ] Implement chain-specific effect routing per doc 43 § 4: own-chain vs parallel-chain target
- [ ] Algorithm-fixed at generation time (not player-chosen)
- [ ] Spec which T4 strategies support parallel-chain reach + which are own-chain-only per doc 43
- [ ] Unit test: generated T4 instance carries target-chain field; parallel-chain T4 references valid parallel chain

### W2.4 — Compositional synergy scan implementation (Pass 1 + Pass 2)

**Per W2 amendment + I1 + I2 + Wave 1 Gate-2 + jack-ryan I3:**

- [ ] Integrate **gandalf-curated 13-entry starter pattern library** per I1 (rocket consumes pattern library config; not authors)
- [ ] Integrate **elrond statistical co-occurrence priors** per I2 (CONCURRENT dependency; if elrond priors not landed when rocket reaches W2.4, implement W2.4 with stub-priors interface load-from-file pattern + flag integration handoff for elrond return)
- [ ] Implement Pass 1 resolve-score: algorithm consumes pattern library + statistical priors to score how candidate T4 resolves existing kit tensions; NOT LLM raw-reasoning per AI-tell line D7
- [ ] Implement Pass 2 preserve-score: per #32 first-do-no-harm; algorithm checks downstream-tension-creation
- [ ] Implement net synergy score = resolve - create
- [ ] 5-category synergy framework per doc 43 § 5 + § 5.4 (NEW 5th Scaling-interaction from SC-4 expansion Topic 2): tension-resolution + theme-compound + cross-chain composition + element-gap fill + Scaling-interaction
- [ ] Compositional synergy scan serves BOTH T4 generation AND legendary added-skill generation (same engine; two consumers per closeout § 2.5)
- [ ] Unit test: scan produces sensible scores for known PASS/FAIL synergy examples

### W2.5 — T4-failure-handling Option F hybrid retry mechanism implementation

- [ ] Implement 3-attempt regeneration with alternate strategy selection per doc 43 § 6 Phase 1
- [ ] Implement partial-T4-ship gate per doc 43 § 6 Phase 2 (≥1 T4 in-band per character)
- [ ] Implement regeneration rate quality-metric tracking per doc 43 § 6 Phase 4
- [ ] Compose with D1 + D67 + D65 + D62 per doc 43 § 6
- [ ] Unit test: inject synthetic WR-bracket failure on candidate T4; verify retry + partial-ship + metric logged

### W2.6 — Pattern 9 + Pattern 10 generation-time detection (design-intent stubs only per W2)

**Per W2 amendment (CRITICAL):** Pattern 9 + Pattern 10 are **design-intent stubs at starting-estimate thresholds**, NOT v1 catalog members. V1 vs v1.1 catalog inclusion is gamora SC-7 decision post-Wave-3-baseline per Discipline #18.2. Rocket MUST NOT over-commit beyond stubs.

- [ ] Implement Pattern 9 stub: `<1 active skill per 10 sec` threshold check per doc 43 § 7 starting-estimate
- [ ] Implement Pattern 10 stub: `>5× expected DPS at max DoT stack` threshold check per doc 43 § 7 starting-estimate
- [ ] Stubs return WARN-flag (not BLOCK) at generation time; pattern-9 + pattern-10 detection is design-intent for gamora SC-7 calibration
- [ ] Compose with #32 first-do-no-harm Pass 2 preserve check per doc 43 § 5.7

### W2.7 — One-T4-unlocked-at-a-time gating + variable 3-or-4 chain architecture per class

- [ ] Implement one-T4-active gating field per doc 43 § 8 (storage representation; player-selection mechanism deferred to D65 respec)
- [ ] Implement variable 3-or-4 class chain count generation per doc 43 § 9
- [ ] Supporting chain absorbs class-intrinsic baseline passives per closeout § 2.1 Option C (composes with Wave 1 minimum-viable trait pool D8 implementation)
- [ ] First-pass class roster DEFERRED per Block A2b (architecture supports 3-or-4; specific class roster fires later)

### W2.8 — Cross-cohesion validation per #26 + Block C scaffolding

- [ ] Validate T4 algorithm produces playable kits per Discipline #26 6 sub-gates per doc 43 § 11.7
- [ ] Cross-cohort validation per Block C scaffolding (4 cohorts × N kits sample)
- [ ] Cross-cohesion check: T4 algorithm output composes with Wave 1 partition schema correctly

### W2.9 — Round-trip smoke per Principle 6 + tag-commit

**CRITICAL per I1 carryover: include `legendary_t0_5` rarity in round-trip smoke coverage.**

- [ ] End-to-end smoke: generate N=10-20 kits per archetype × per T4 category (A/B/C) including DUAL_ELEMENT_ADDITION + parallel-chain reach + legendary_t0_5 rarity coverage
- [ ] Verify all fields present + types consistent + T4-failure-handling Option F fires on synthetic failure + Pattern 9+10 stubs return WARN-flag on threshold violation
- [ ] MIGRATION.md if cross-seam contract change per ADR-004
- [ ] AGENT_STATE.md updated per session end
- [ ] Tag intent: `rocket: Cycle 13 Wave 2 T4 algorithm implementation — W2.0-W2.9 bundled per doc 43 + jack-ryan Gate-1 W2+I1+I3 folded`

### Discipline compose-check

- [ ] #1 math-before-code: math-note per § Math-before-code above
- [ ] #1.2 code-citation: all references to existing code (file + line)
- [ ] **#11 empirical inspection (CRITICAL) — POST-SCRIPT EMPIRICAL COUNT ASSERTIONS per WU dimension MUST be 100% accurate.** This is the WARN-pattern full-closure opportunity per jack-ryan Wave 1 Gate-2 verdict. **No count understatements or overstatements.** Verify all numerical claims empirically via grep + len() + Python Counter scan; cite the verification mechanism.
- [ ] #18 + #18.2 methodology: T4 algorithm is math hotspot; gamora SC-7 consultation FULL post-Wave-3-baseline per #18.2
- [ ] #26 playability: W2.8 operationalizes
- [ ] #27 dual-effect capstone: Wave 2 IS the implementation of #27
- [ ] #29 commitment-to-consequence: T4-failure-handling Option F lands with consequence
- [ ] #31 dual-effect separability: Category A + Category B/C effects MUST be INDEPENDENTLY COHERENT per doc 43 § 11.7
- [ ] #32 first-do-no-harm: compositional synergy scan Pass 2 preserve check IS the implementation of #32 per doc 43 § 5
- [ ] Principle 6 round-trip: smoke test PASSes per W2.9

## Acceptance criteria

- [ ] All 10 sub-waves W2.0-W2.9 land
- [ ] 3-category T4 taxonomy operationalized; DUAL_ELEMENT_ADDITION strategy implemented; parallel-chain reach implemented; compositional synergy scan two-pass implemented; T4-failure-handling Option F implemented; Pattern 9+10 stubs implemented; one-T4-active gating implemented; variable 3-or-4 chain architecture implemented
- [ ] **POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE** (Discipline #11 WARN-pattern full-closure target — no count understatements or overstatements; verify empirically)
- [ ] legendary_t0_5 rarity covered in W2.9 round-trip smoke per I1 carryover
- [ ] Round-trip smoke per Principle 6 PASSes
- [ ] MIGRATION.md updated if cross-seam contract change
- [ ] Tagged commit per rocket convention
- [ ] Math notes filed per Discipline #1

## Out of scope (explicit non-goals)

- Pattern 9 + Pattern 10 detection-algorithm calibration BEYOND stubs (gamora SC-7 post-Wave-3-baseline per #18.2)
- DUAL_ELEMENT_ADDITION magnitude empirical iteration BEYOND starting anchors (gamora SC-7 post-Wave-2-baseline per #18.2)
- LLM T4 naming per I3 (Phase 5 cohesion coalescence; Cycle 14+; out of Wave 2 scope)
- First-pass class roster (Block A2b deferred-commitment; architecture supports 3-or-4; specific roster later)
- D9 element/mechanic-gating gear-affix trait surface (Wave 4 scope)
- Wave 3 T4 algorithm Phase 3 (character-wide vs chain-wide dimension)
- Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling
- Wave 5 gauntlet sim + season gen + close
- jack-ryan Gate-2 verification (separate dispatch post-rocket-implementation)
- gamora SC-7 methodology consultation FULL execution (post-Wave-3-baseline per #18.2)
- Modifying doc 40 / doc 41 / doc 42 / doc 43 (cross-seam gandalf authority)
- decisions-log entries (jack-ryan seam if architectural drift surfaces)
- Production telemetry DB migration v2.16 ALTER TABLE per ADR-006

## Open questions for the agent to resolve

- W2 sub-wave sequencing: W2.0 → W2.1 → W2.2 (depends on W2.1) → W2.3 (depends on W2.1) → W2.4 (depends on W2.1 + elrond priors) → W2.5 (depends on W2.1) → W2.6 (depends on W2.5) → W2.7 → W2.8 (depends on W2.1-W2.7) → W2.9. Internal sequencing your seam-owner call
- Elrond statistical-priors handoff: if elrond priors not landed when rocket reaches W2.4, implement W2.4 with stub-priors interface (load-from-file pattern) + flag for elrond integration handoff
- Pattern library 13-entry size: gandalf-curated starting set per I1; if rocket finds additional entries while implementing, flag for gandalf supplementation (don't author)
- MIGRATION.md scope: minimal (new T4 schema fields) vs comprehensive; recommend minimal per Principle 6

## References

- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` (intent canonical)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` (Gate-1 W2 + I1 + I2 + I3 + I5 fold-ins)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-partition-gate-2.md` (Wave 1 Gate-2; I1 legendary_t0_5 carryover; WARN-pattern full-closure target)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition substrate)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (foundation)
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` (5th Scaling-interaction + Pattern 9+10)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #26 + #27 + #29 + #31 + #32 + Principle 6)
- `agentic_orchestration/operating-procedures/rocket.md`

---

**Cycle:** 13
**Wave:** 2 implementation (W2.0-W2.9 bundled)
**Gates:** Wave 2 close = jack-ryan Gate-2 PASS on this implementation + WARN-pattern full-closure verification; unblocks Wave 3 T4 algorithm Phase 3 (character-wide vs chain-wide dimension)
**Priority:** P1 — critical-path Wave 2 close
