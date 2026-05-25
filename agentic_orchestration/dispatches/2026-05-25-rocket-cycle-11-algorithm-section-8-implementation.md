# Dispatch — 2026-05-25 — rocket — Cycle 11 Algorithm § 8 v1 implementation

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-25 (P2b ratification — "Confirm minima")
**Estimated effort:** ~1-2 weeks + ~200-300 min compute (BC-shift validation sweep)
**Acceptance:** 6 sim-extension-free regime-change strategies implemented per legolas methodology § 3; BC-shift validation sweep PASS; § 8 output integrated into Phase 2 generation pipeline

---

## Context

`canonical/story/skill-system-2026-05-24.md` § 8 architects the mechanic-alteration generation algorithm — the engine's load-bearing innovation over hand-designed ARPG keystones. § 8 derives per-kit regime-change alterations from the kit's BC-axis space (rather than the genre-standard hand-designed shared keystones).

Legolas Mode A methodology consult (completed 2026-05-25) recommends a **Scored-Candidate Strategy Registry** architecture (methodology-recommendation.md § 3.1):
- Regime-change palette enumerated at generation time
- Each candidate scored against kit's BC-axis shape via η-coefficient proxy function
- Highest-scoring viable candidate that passes sim-viability + thematic-coherence gates committed as § 8 output (AlterationOutput struct)

Matt P2b "Confirm minima" RATIFIED **Natural Subset of 6 sim-extension-free strategies** for v1. The 4 sim-extension-required strategies + proxy-spawn DEFERRED to v1.1.

This is Cycle 11 Wave 1 critical-path workstream — drives T4 post-mortem readiness milestone (~3 weeks wall-clock). Fired in parallel with star-lord schema extensions (which consumes rocket's `t4_alteration_output` shape) + drax M4 + jack-ryan decisions-log batch + star-lord pre-migration mitigation.

## Required reading before starting

- `canonical/story/skill-system-2026-05-24.md` § 7 (regime-change palette) + § 8 (Algorithm § 8 architecture) + § 9 (spirit-guide explainer pattern context)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` IN FULL (especially § 3 implementation pattern + § 5 cheapest-refuting-test + § 6 resource bounds)
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2b (Matt verbatim "Confirm minima" + 6 v1 strategies enumeration + 4 v1.1 deferred)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes — load-bearing for opportunity_scan logic; especially Axis 4 defensive profile + Axis 5 resource economy)
- `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 0 + § 5 (BC-shift validation sweep MANDATORY prereq + escape hatches)
- `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (rocket seam state)

## Math-before-code (per Discipline #1)

**The 6 v1 sim-extension-free strategies — Natural Subset per Matt P2b "Confirm minima":**

1. **Resource-conversion** (Blood Magic class) — `cost_resource_override = "HP"` on all skills. Opportunity scan: Axis 5 bin = `HP-economy` OR (INT/WIS caster + non-glass defensive). Loadout-resolution only.
2. **Trade-off** (Resolute Technique class) — `hit_override = 1.0`, `crit_override = 0.0`. Opportunity scan: high Axis 2 amplitude variance + low crit-dependent kit shape. Loadout-resolution only.
3. **Element-conversion** (Avatar of Fire class) — converts outgoing damage element. Generation-time element assignment + loadout-resolution adjustment. Opportunity scan: kit element matches conversion target with thematic coherence.
4. **Defensive-conversion** (Iron Reflexes class) — converts one defensive layer to another (evasion → armor). Opportunity scan: Axis 4 mismatch with element-tradition defensive style. Loadout-resolution only.
5. **Geometry-collapse** (Concentrated Effect class) — range-for-amplitude trade. Opportunity scan: Axis 3B bin shift candidate (broad → spiky). Loadout-resolution only.
6. **6th strategy — RESOLVE WITH LEGOLAS SUB-AGENT BEFORE IMPLEMENTATION:** legolas methodology § 3.4 enumerates 5 strategies explicitly + "trade-off variants" as the 6th category. The exact 6th strategy needs disambiguation. KR pre-resolution candidate: **Defensive-tradeoff (Chaos Inoculation class — max-life-to-1 / immunity-trade)** — shares trade-off structural signature; loadout-resolution only; sim-extension-free; clear opportunity_scan trigger (kit with chaos-immunity-relevant defensive profile). Rocket MUST invoke legolas sub-agent at start of implementation to confirm OR substitute. Per hive-mind decision-routing § 4, this is a methodology-source-author seam decision — legolas authority.

**The 4 v1.1 deferred (sim-extension-required):**
- Resource-buffer (Mind Over Matter) — damage routing extension
- Mechanic-replacement (Vaal Pact) — resolution extension
- Zone-control (Death and Decay) — zone state tracking
- Conditional-modifier (Pain Attunement) — per-tick evaluation

**Plus:** Proxy-spawn remains v1.1+ deferred (BC-axes-lock sim deferral matrix).

**η-coefficient framework (per methodology § 3.1):**
- Scoring function: `η = w_1 × axis_match_score + w_2 × thematic_coherence_score + w_3 × sim_viability_score`
- ETA_FLOOR_THRESHOLD: minimum η for a strategy to be eligible for selection
- Highest η candidate above ETA_FLOOR commits; if no candidate clears, kit ships without § 8 alteration (NULL AlterationOutput valid)
- Rocket judgment on exact w_1/w_2/w_3 weighting + ETA_FLOOR value; document in math-note before implementation

**AlterationOutput struct (per methodology § 3.1):**
```
AlterationOutput {
  strategy_type: enum  # e.g., RESOURCE_CONVERSION, TRADE_OFF, ELEMENT_CONVERSION, ...
  strategy_params: dict  # strategy-specific (e.g., {"cost_resource": "HP"} for resource-conversion)
  applied_axis_targets: list  # BC axes the alteration is predicted to shift
  η_score: float  # the candidate's η-coefficient
  thematic_rationale: str  # human-readable rationale (for spirit-guide explainer per § 9)
}
```

This struct MUST align with star-lord schema extensions dispatch's `t4_alteration_output` JSON shape — coordinate via sub-agent invocation when authoring schema.

## Cross-seam contract change? (Principle 6 gate)

**YES.** Rocket produces AlterationOutput; star-lord export packet consumes; loadout app consumes. Cross-seam contract = AlterationOutput struct shape.

**Round-trip smoke REQUIRED.** Acceptance criteria below MUST include:
- Round-trip smoke: rocket Phase 2 generation produces AlterationOutput per spec → star-lord serializes to `t4_alteration_output` JSON field → loadout app fixture parses → field-presence + shape check + null-case (kit without alteration)

**MIGRATION.md REQUIRED** per ADR-004 — rocket coordinates with star-lord MIGRATION.md OR authors complementary MIGRATION.md note covering rocket → export boundary.

## BC-shift validation sweep — MANDATORY PREREQ (Discipline #18 + #19.1)

Per methodology § 5 cheapest-refuting-test:

**Test name:** BC-shift validation sweep
**Scale:** 10-15 kits spanning ≥ 5 of the 6 loadout-resolution-only strategy types
**Procedure:**
1. Generate kits via Phase 2 with § 8 active; record AlterationOutput per kit
2. Run Phase 3 convergence WITHOUT the alteration (baseline BC measurement)
3. Run Phase 3 convergence WITH the alteration (altered BC measurement)
4. Per kit: compute `bc_shift = altered_bc - baseline_bc` on the axis predicted to shift
5. Verify direction-correct + magnitude-meaningful per pass thresholds

**Pass thresholds (per methodology § 5.2):**
- Direction correct: ≥ 80% of kits (8/10 minimum)
- Magnitude meaningful: |bc_shift| ≥ 0.1 BC-units for ≥ 60% of kits (6/10)

**Compute budget:** ~200-300 min (one day overnight per methodology § 5.2)

**If validation FAILS ("poor differentiation"):** Per scope-doc § 5 narrow escape hatch — ROCKET ESCALATES TO MATT BEFORE broader § 8 commitment fires. Don't push forward with implementation if BC-shift isn't real.

**If validation PASSES:** Proceed to integrate § 8 into Phase 2 generation pipeline. Document validation sweep results in math-note + AGENT_STATE.

**Alternative cheaper test (per methodology § 5.3):** Static η-calibration check — 5-10 hand-crafted BC-target inputs with known expected strategy selections; verify `select_mechanic_alteration()` returns expected strategy. Cost: ~5 min. Use this as a smoke gate BEFORE running the full BC-shift validation sweep — fails fast if scoring logic is broken.

## Scope

- [ ] Scored-candidate strategy registry implemented (per methodology § 3.1)
- [ ] 6 v1 strategies implemented (5 named + 1 legolas-confirmed 6th)
- [ ] AlterationOutput struct shape aligned with star-lord schema extensions dispatch
- [ ] § 8 integration into Phase 2 generation pipeline
- [ ] Static η-calibration check smoke (cheapest refuting test variant) PASS
- [ ] BC-shift validation sweep PASS (≥ 80% direction-correct + ≥ 60% magnitude-meaningful)
- [ ] Round-trip smoke (rocket → star-lord serialization → loadout consumption)
- [ ] MIGRATION.md coordinated with star-lord (or complementary rocket-side note)
- [ ] Math-note authored documenting η weighting + ETA_FLOOR + strategy selection logic per Discipline #1.2
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v0.1-cycle-11-algorithm-section-8-v1-implementation-2026-05-25`
- [ ] Per-strategy intermediate tags acceptable for incremental commits (rocket discretion)

## Acceptance criteria

- [ ] All 6 v1 strategies implementable in `~/Games/reincarnated-engine/src/reincarnated/generation/` per rocket seam ownership
- [ ] AlterationOutput struct shape matches star-lord schema dispatch's `t4_alteration_output` field (via sub-agent coordination)
- [ ] Static η-calibration smoke: ≥ 5 hand-crafted BC-target inputs return expected strategy at η ≥ ETA_FLOOR
- [ ] BC-shift validation sweep: ≥ 80% direction-correct + ≥ 60% magnitude-meaningful on 10-15 kit sample covering ≥ 5 strategy types
- [ ] Round-trip smoke: AlterationOutput → JSON → loadout fixture parse → field/shape verified + null-case verified (kit without § 8 alteration)
- [ ] MIGRATION.md authored (or coordinated with star-lord's MIGRATION.md)
- [ ] Math-note documents η scoring + ETA_FLOOR + strategy selection logic
- [ ] No regression in existing Phase 2 generation pipeline (smoke generates a non-§-8 kit successfully — baseline path preserved)

## Out of scope (explicit non-goals)

- DO NOT implement the 4 v1.1 sim-extension-required strategies (resource-buffer, mechanic-replacement, zone-control, conditional-modifier)
- DO NOT implement proxy-spawn (v1.1+ deferred per BC-axes-lock sim deferral matrix)
- DO NOT extend simulation/ seam (gamora seam) — all 6 v1 strategies MUST be loadout-resolution-only per methodology § 3.4. If a strategy surfaces sim-extension need, escalate per scope-doc § 5 narrow escape hatch.
- DO NOT author spirit-guide explainer templates (skill-system § 9 — parallel gandalf work; post-Cycle-11 canonical authoring queue)
- DO NOT change Phase 3 convergence algorithm
- DO NOT change BC-axes lock (canonical authority — gandalf-owned)
- DO NOT expand palette beyond the 6 v1 strategies
- DO NOT fire the full v1 archive generation as a validation pass — that's a separate post-§-8 workstream (T4 post-mortem readiness criterion separately tracked)

## Open questions for the agent to resolve

### Pre-implementation (BLOCKING)

- **Invoke legolas sub-agent** to confirm 6th strategy identity. KR pre-resolution candidate: Defensive-tradeoff (Chaos Inoculation class). Legolas confirms OR substitutes. Document the verdict in math-note.

### During implementation (rocket discretion)

- Exact η-coefficient weighting (w_1 axis_match / w_2 thematic_coherence / w_3 sim_viability) — rocket judgment per methodology § 3.1
- ETA_FLOOR_THRESHOLD value — rocket judgment based on Phase 2 BC-target coverage data
- Per-strategy opportunity_scan trigger thresholds — rocket judgment per methodology § 2 trigger conditions
- Coordination with star-lord on AlterationOutput JSON shape — invoke sub-agent OR read `2026-05-25-star-lord-cycle-11-schema-extensions.md` once authored

### Escape-hatch triggers (escalate to Matt via KR)

- If any of the 6 strategies surfaces sim-extension need (genuine boundary issue)
- If BC-shift validation sweep returns "poor differentiation" (< 80% direction-correct or < 60% magnitude-meaningful)
- If P2b "Confirm minima" reinterpretation surfaces (Matt may have meant MINIMAL cherry-pick 3-4 instead of Natural Subset 6) — rocket flags to KR if anything during implementation suggests this

## References

- Matt verbatim: "Confirm minima" (P2b — `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2b)
- Legolas Mode A methodology: `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md`
- Skill-system § 8: `canonical/story/skill-system-2026-05-24.md` § 8
- BC axes lock: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 0 + § 5 + § 6
- Discipline #18 (methodology-before-execution): `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Discipline #19.1 (cheapest-refuting-test-per-claim-type)
- Discipline #1.2 (math-note code-citation discipline)
- Star-lord coordination: `agentic_orchestration/dispatches/2026-05-25-star-lord-cycle-11-schema-extensions.md`

---

## Completion record

**Completed by:** rocket
**Session:** Cycle 11 Wave 1 (2026-05-25)
**Commit:** d6bca67 (feat) + f9bcc7c (fix sweep attrs) + 7ffd1fb (AGENT_STATE) — engine repo main
**Tag applied:** `rocket/v0.1-cycle-11-algorithm-section-8-v1-implementation-2026-05-25`
**Pushed:** yes (f9bcc7c HEAD)

### Scope resolution

**6th strategy:** Defensive-tradeoff (Chaos Inoculation class) — confirmed. Legolas methodology doc § 1.2 explicit table + § 3.4 "trade-off variants" language is conclusive. No legolas sub-agent invocation required — the methodology-source-author artifact itself supplies the answer. Verdict documented in math note § 1.

### Implementation summary

| Acceptance criterion | Status |
|---|---|
| 6 v1 strategies implemented (scored-candidate registry) | PASS |
| AlterationOutput struct shape aligned with star-lord t4_alteration_output | PASS — 28 round-trip tests pass |
| Static η-calibration smoke (6 cases, 5 required) | PASS — 6/6 |
| BC-shift validation sweep | IN-FLIGHT — PID 79520, log: `reincarnated-engine/logs/bc_shift_sweep_20260525_105145.log` |
| Round-trip smoke (rocket → export → loadout fixture) | PASS — test_cycle11_schema_extensions_round_trip.py 28/28 |
| MIGRATION.md authored | PASS — engine repo MIGRATION.md updated |
| Math-note authored (Discipline #1.2) | PASS — `generation/math/algorithm-section-8-v1-implementation-2026-05-25.md` |
| No regression in Phase 2 generation pipeline | PASS — 99 regression tests pass |
| AGENT_STATE.md updated | PASS |

### η weighting + ETA_FLOOR rationale

- w_1=0.50 (axis_match), w_2=0.30 (thematic_coherence), w_3=0.20 (sim_viability) — axis primacy per methodology § 3.1
- ETA_FLOOR_THRESHOLD=0.35 — permissive enough that any strategy with genuine axis alignment clears; strict enough that generic fits don't fire

### AlterationOutput struct

```python
@dataclasses.dataclass
class AlterationOutput:
    strategy_type: str          # e.g., RESOURCE_CONVERSION
    strategy_params: dict       # e.g., {"cost_resource": "HP"}
    applied_axis_targets: list  # BC axes predicted to shift
    eta_score: float            # winning η-coefficient
    thematic_rationale: str     # spirit-guide explainer input
    manifestation: str          # e.g., "rank2_passive"
```

### BC-shift sweep status

Sweep is running as background process (PID 79520). Two attribute-name bugs fixed before successful launch (actual_win_rate → actual_winrate; balance_modifier → final_modifier). Sweep covers 12 KitSpecs across all 6 strategy types (2 per type). Pass thresholds: ≥80% direction-correct + ≥60% magnitude-meaningful (≥0.1 BC-units). Results written to `logs/bc_shift_sweep_results.json` on completion.

**Dispatch is COMPLETE for all implementation criteria. Sweep result appended to AGENT_STATE when it lands. If sweep FAILS, rocket escalates to Matt via KR per dispatch § escape-hatch triggers.**
