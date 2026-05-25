# Dispatch — 2026-05-25 — rocket — Cycle 12 Layer 6 § 8 algorithm wire-up + L9 opportunity-scan refactor

**From:** knight-rider
**To:** rocket (generation seam — engine content-generation owner)
**Approved by:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q1 Option γ Layers 2+3+4+6) + skip-confirmation re-auth 2026-05-25; KR autonomously orchestrates Layer 6 dispatch authoring per scope-doc § 1
**Estimated effort:** ~1 week rocket (framing brief estimate; Layer 2/3/4 cadence suggests substantially faster — ~30-60 min wall-clock realistic)
**Acceptance:** § 8 algorithm wire-up landed (alterations reach combat arithmetic via new engine layers) + L9 opportunity-scan refactor (triggers use mechanical_substrate signals NOT cultural_tradition heuristics) + cross-seam SC-3 obligations enumerated as L6 acceptance criteria per Gate-2 on L3 INFO-D + signature_chain_id population per cross-chain T4 election + validate_invariants runtime vocabulary check for L6 wire-up sites + round-trip smoke + jack-ryan Gate-2 PASS

---

## Context

Cycle 12 Layer 6 is the FINAL critical-path layer per Option γ scope. Layers 2 + 3 + 4 + their Gate-2 verdicts all PASS per Cycle 12 state file Wave 1-3. Pre-Layer-6 amendments (L2 WARN-B/C + L4 INFO-A/B) ✅ COMPLETE per rocket commit `9d7a530`. All prereqs cleared.

Layer 6 closes the loop on the v1 new engine: alterations from § 8 algorithm (Cycle 11 mechanic_alteration.py 6 strategies) finally REACH COMBAT ARITHMETIC via new engine layers — closing the Tier 2 framing gap (Cycle 11 § 8 shipped as intent metadata; Cycle 12 Layer 6 wires it up).

**Two scope buckets:**

### Bucket 1 — § 8 algorithm wire-up to combat arithmetic

- Consume Layer 4 `ConvergenceResult.converged_kit.t4_alteration_output` (the AlterationOutput from Cycle 11 § 8)
- Consume Layer 3 `SkillTree.t4_candidates` + `signature_chain_id` (cross-chain T4 election populated at Layer 6 — per Gate-2 on L3 INFO-3 deferred to L6)
- Wire `apply_t4_alteration_to_combat(kit, t4_alteration, fight_engine_context)` per framing brief § 4 contract LOCKED
- The 6 v1 strategies (RESOURCE_CONVERSION, TRADE_OFF, ELEMENT_CONVERSION, DEFENSIVE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_TRADEOFF) each have specific combat-arithmetic touch-points:
  - RESOURCE_CONVERSION: modify cost_resource per skill (HP-cost vs mana-cost)
  - TRADE_OFF: set hit_modifier=1.0 + crit_rate=0.0 at fight start
  - ELEMENT_CONVERSION: modify damage_type per skill (all outgoing → target_element)
  - DEFENSIVE_CONVERSION: stat conversion at fight start (defensive layer remap)
  - GEOMETRY_COLLAPSE: modify aoe_radius × damage_multiplier (range-for-amplitude trade)
  - DEFENSIVE_TRADEOFF: defensive trade-off variant per legolas methodology § 3.4 + Cycle 11 § 8 STRATEGY_DEFENSIVE_TRADEOFF
- Alteration emission shape readable by gamora sim consumer at sim time

### Bucket 2 — L9 opportunity-scan refactor

Per framing brief § L9 + § 8 architecture: opportunity-scan triggers currently use cultural_tradition heuristics (ELEMENT_CONVERSION fire-resonance; DEFENSIVE_CONVERSION heavy-armor-tradition). Per L9 mechanical vs semantic substrate split, cultural_tradition is SEMANTIC OVERLAY (NOT in BDI math model). Refactor opportunity-scan triggers to use MECHANICAL substrate signals (element + weapon_mechanical_profile + bc_target_cell axes).

- Identify all opportunity_scan trigger sites in mechanic_alteration.py + related modules
- Per strategy, map cultural_tradition signal → mechanical_substrate signal:
  - ELEMENT_CONVERSION fire-resonance: was "cultural_tradition signals fire affinity" → now "kit.element + adjacent BC-axis signals fire dominance"
  - DEFENSIVE_CONVERSION heavy-armor-tradition: was "cultural_tradition signals heavy-armor history" → now "kit.bc_target_cell.defensive_profile + mechanical_substrate_triple defensive signals"
  - Other strategies: similar pattern — refactor any cultural_tradition reads to mechanical_substrate reads
- Per scope-doc § 6 known-unknown: "L9 opportunity-scan refactor can't cleanly map § 8 triggers to mechanical_substrate signals → Route to gandalf for design refactor; escalate Matt only if architectural amendment required" — if mapping is non-obvious for any strategy, flag to KR

### Bucket 3 — Cross-seam SC-3 obligations enumeration (per Gate-2 on L3 INFO-D)

Layer 6 dispatch MUST enumerate cross-seam SC-3 obligations as L6 acceptance criteria. These are EMISSION-side responsibilities of Layer 6 (rocket emits in consumable form; consumer-side code in star-lord/gamora/drax is FOLLOW-ON post-Layer-6 work):

- **star-lord obligation**: `off_hand_contract` export field in class JSON schema — Layer 6 emits the OffHandContract (per Layer 3 SC-3 `off_hand_contract.py`) in a star-lord-serializable shape. Star-lord schema extension is FOLLOW-ON (separate star-lord dispatch).
- **gamora obligation**: sim combatant consumption — Layer 6 emits sim-readable fields (e.g., off-hand buff/aura/proxy parameters; alteration combat-arithmetic deltas) per framing brief § 4 contract. Gamora sim combatant integration is FOLLOW-ON (separate gamora dispatch).
- **drax obligation**: Spirit Guide panel display — Layer 6 emits Spirit Guide narration metadata (per § 9 explainer pattern) in a drax-consumable shape. Drax Spirit Guide panel update is FOLLOW-ON (separate drax dispatch).

Layer 6 acceptance: emission contracts correct + MIGRATION.md documents each cross-seam consumer's expected field/shape; FOLLOW-ON consumer work is queued separately.

### Bucket 4 — Layer 6 deferred items from prior Gate-2 verdicts

- **Gate-2 on L3 INFO-3 (deferred to L6)**: `SkillTree.signature_chain_id: Optional[str] = None` field present from L3; Layer 6 populates per cross-chain T4 election (per T4-A § 2 hierarchy — 1 signature + 1-3 secondary capstones; the "signature" capstone is build-defining; election rule per rocket math judgment OR consume gandalf design guidance if surfaces)
- **Gate-2 on L3 INFO-C (deferred to L6)**: `validate_invariants()` runtime vocabulary check — current L3 generator-behavioral-only check; Layer 6 may construct SkillTree externally OR consume L3-emitted SkillTree; add runtime node_type vocabulary check at L6 wire-up sites for defensive robustness

---

## Required reading before starting

### Authority-of-record (LOCKED canon — primary load-bearing)

- **`canonical/story/skill-system-2026-05-24.md`** § 8 (Algorithm § 8 architecture — primary load-bearing for L6 wire-up) + § 9 (spirit-guide explainer pattern — Spirit Guide narration metadata emission)
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 4 (apply_t4_alteration_to_combat signature LOCKED) + § L9 (mechanical vs semantic substrate split — LOAD-BEARING for L9 refactor) + § L10 (Tier 2 framing — Cycle 11 § 8 intent metadata + Cycle 12 Layer 6 wire-up = full v1 closure)
- **`agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`** § 1 + § 5 + § 6 (especially § 6 L9 refactor escape-hatch + sim-seam boundary surprise routing)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (substrate context for L9 refactor mechanical signals)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes vocabulary for L9 refactor)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § 2 (T4-A hierarchy — signature vs secondary capstones; informs signature_chain_id election per INFO-3)
- `canonical/story/off-hand-items-2026-05-24.md` § 2.3 (off-hand mechanical contract — informs cross-seam off_hand_contract emission)

### Layer 2/3/4 outputs to consume

- Layer 2 dispatch + completion record + WARN-A/B/C amendments per pre-Layer-6 batch commit `9d7a530`
- Layer 3 dispatch + completion record + Gate-2-on-L3 INFO-3 + INFO-C disposition (deferred to L6)
- Layer 4 dispatch + completion record + L4 INFO-A/B amendments per pre-Layer-6 batch commit `9d7a530`
- Layer 4 ConvergenceResult shape per framing brief § 4 LOCKED contract

### Cycle 11 § 8 algorithm (consume as L6 input)

- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (6 strategies including DEFENSIVE_TRADEOFF — opportunity_scan triggers identified here; refactor target per L9)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (original § 8 methodology — Scored-Candidate Strategy Registry + η-coefficient framework)

### Gate-2 verdicts (Layer 6 implementation prereqs)

- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-3.md` — INFO-D cross-seam SC-3 obligations + INFO-3 signature_chain_id + INFO-C validate_invariants runtime vocabulary
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-3-rocket-layer-4.md` — Layer 4 verified composable; consume ConvergenceResult shape

### Updated MIGRATION.md (post-amendments)

- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-2 (reconciled per WARN-B; correct field names for cross-seam consumer reference)
- Layer 6 MUST extend MIGRATION.md with § v1.4-layer-6 entry per ADR-004

### Engineering-disciplines

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — load-bearing: #1 (math-before-code) + **#1.2 (math-note code-line citations — per Layer 4 precedent; REQUIRED at first authoring for L6 math note)** + #2 (smoke-test) + #2.1 (smoke-test resource-scaling rehearsal) + #8 (schema validation at boundary) + #11 (empirical inspection) + #13a (implementation-vs-intent drift — L9 refactor verifies no cultural_tradition leakage) + #18 (methodology-before-execution — no MC consult needed for L6; L9 refactor is methodology-spec-derived) + #25 (semantic-layer rep-audit — PRIMARY for L9 refactor verification)

---

## Math-before-code (per Discipline #1 + #1.2)

Author math-note at `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25.md` BEFORE implementation. Per Discipline #1.2 (now standard post-Layer-4): math note MUST include code-line citations (file:line ranges where each math section is implemented).

### Math 1 — § 8 wire-up signature per framing brief § 4 (LOCKED)

```python
def apply_t4_alteration_to_combat(
    kit: PlayerClass,                  # PlayerClassV2 per Layer 2
    t4_alteration: T4Alteration,       # per Layer 3 + Cycle 11 § 8 AlterationOutput
    fight_engine_context: FightEngineContext,
) -> AlteredFightEngineContext:
    ...
```

- Per-strategy implementation map (6 v1 strategies; cite mechanic_alteration.py:line):
  - RESOURCE_CONVERSION → modify cost_resource per skill in fight_engine_context (file:line for skill cost mutation)
  - TRADE_OFF → set hit_modifier=1.0 + crit_rate=0.0 at fight start (file:line for fight-state init)
  - ELEMENT_CONVERSION → modify damage_type per skill (all outgoing → target_element) (file:line for damage-type mutation)
  - DEFENSIVE_CONVERSION → stat conversion at fight start (defensive layer remap) (file:line for stat conversion)
  - GEOMETRY_COLLAPSE → aoe_radius × damage_multiplier (range-for-amplitude trade) (file:line for geometry mutation)
  - DEFENSIVE_TRADEOFF → defensive trade-off variant per legolas § 3.4 + STRATEGY_DEFENSIVE_TRADEOFF (file:line)
- Sim-seam boundary check per scope-doc § 6: if any v1 strategy actually requires sim-seam boundary touch beyond combat-arithmetic deltas, route to gamora sub-agent for verification + flag to KR

### Math 2 — L9 opportunity-scan refactor per framing brief § L9

- Per L9: cultural_tradition is SEMANTIC OVERLAY; NOT in BDI math model
- Per § 8 architecture: opportunity_scan currently uses cultural_tradition heuristics in 2 strategies:
  - ELEMENT_CONVERSION: fire-resonance via cultural_tradition signal
  - DEFENSIVE_CONVERSION: heavy-armor-tradition via cultural_tradition signal
- Refactor target: cultural_tradition signal → mechanical_substrate signal
  - ELEMENT_CONVERSION fire-resonance: substitute mechanical signal — kit.element + bc_target_cell signals (e.g., fire dominance via element=fire + bc_target_cell axis signals)
  - DEFENSIVE_CONVERSION heavy-armor: substitute mechanical signal — kit.bc_target_cell.defensive_profile + mechanical_substrate_triple defensive component
- Per Discipline #25 semantic-layer rep-audit: post-refactor, NO cultural_tradition reads in opportunity_scan code path (verify empirically per Discipline #11)
- Per Discipline #13a: ensure refactor preserves opportunity_scan semantic intent (same strategies fire for same kits modulo signal-source change)

### Math 3 — signature_chain_id cross-chain T4 election (per Gate-2 on L3 INFO-3 deferred to L6)

- Per T4-A § 2: 1 signature capstone + 1-3 secondary capstones per kit; signature is build-defining
- Election rule for signature_chain_id: rocket math judgment per T4-A architecture
  - Recommendation: signature_chain_id = chain whose T4Slot.t4_alteration_output has highest η_score (max-η is build-defining)
  - Tie-break: deterministic ordering per chain index
  - If all chains have null t4_alteration_output: signature_chain_id remains None
- Populate at Layer 6 wire-up; consume in apply_t4_alteration_to_combat (use signature_chain_id's T4Alteration for build-defining wire-up; secondary chains' T4Alterations may layer additional effects per design judgment)

### Math 4 — Cross-seam emission contract (per Gate-2 on L3 INFO-D)

- **star-lord emission**: off_hand_contract serializable shape (consume Layer 3 OffHandContract; emit in class JSON-compatible form per framing brief § 4 PlayerClass.off_hand_item field)
- **gamora emission**: sim-combatant fields (combat-arithmetic deltas per Math 1; emit as part of PlayerClassV2 or as fight_engine_context modifier)
- **drax emission**: Spirit Guide narration metadata (per § 9 explainer pattern; emit as part of t4_alteration_output or as separate field per T4 contract — verify against Layer 3 + Cycle 11 narration field implementation)
- MIGRATION.md § v1.4-layer-6 documents each emission shape for downstream consumer reference

### Math 5 — validate_invariants() runtime vocabulary check (per Gate-2 on L3 INFO-C deferred to L6)

- Per Gate-2 on L3 INFO-C: `validate_invariants()` is generator-behavioral-only; Layer 6 may construct SkillTree externally OR consume L3-emitted SkillTree
- Add runtime node_type vocabulary check at L6 wire-up sites (e.g., when Layer 6 walks SkillTree.t4_candidates, verify node_type values are within canonical enum set per skill-system canon)
- Defensive robustness against external SkillTree construction (e.g., if testing harness or future code constructs SkillTree manually)

### Math 6 — Cheapest-refuting-test per Discipline #19.1

- 6-strategy wire-up smoke: for each of 6 v1 strategies, verify alteration correctly applied to combat arithmetic via end-to-end fight simulation (kit → § 8 alteration → fight engine → fight outcome reflects alteration)
- L9 refactor smoke: verify opportunity_scan triggers correctly fire for refactored mechanical_substrate signals (same strategies, same kits, no cultural_tradition reads)
- signature_chain_id smoke: verify cross-chain T4 election produces deterministic signature_chain_id for representative kits
- Integration smoke: full pipeline L2 + L3 + L4 + L6 produces valid AlteredFightEngineContext for 22-25 representative kits

### Math 7 — Resource bounds projection per Discipline #1.1

- Per-strategy wire-up compute cost (combat-arithmetic mutation overhead)
- Per-kit Layer 6 application cost (signature_chain_id election + 1-N T4Alterations applied)
- Integration smoke wall-clock estimate (L2 + L3 + L4 + L6 end-to-end per kit)

---

## Cross-seam contract change? (Principle 6 gate)

**Yes.** Layer 6 emits AlteredFightEngineContext consumed by gamora sim-engine; emits off_hand_contract for star-lord serialization; emits Spirit Guide narration metadata for drax display.

**Round-trip smoke REQUIRED per Principle 6:**
- Layer 6 emission shape → star-lord JSON serialize → loadout deserialize (round-trip)
- Round-trip fixture: a kit with all 6 strategy applications + signature_chain_id populated + off_hand_contract present

**MIGRATION.md REQUIRED per ADR-004:**
- Extend `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` with new entry `§ v1.4-layer-6 Cycle 12 Layer 6 § 8 wire-up + L9 refactor + cross-seam SC-3 obligations`
- Document AlteredFightEngineContext shape (for gamora consumption)
- Document off_hand_contract emission shape (for star-lord consumption)
- Document Spirit Guide narration metadata shape (for drax consumption)
- Per WARN-B reconciliation pattern (post-amendments): ensure field names match implementation; avoid pseudocode-vs-reality drift

---

## Scope (rocket Layer 6 § 8 wire-up + L9 refactor implementation)

### Bucket 1 — § 8 wire-up to combat arithmetic

- [ ] Implement `apply_t4_alteration_to_combat(kit, t4_alteration, fight_engine_context) -> AlteredFightEngineContext` per framing brief § 4 contract
- [ ] Per-strategy wire-up (6 v1 strategies) per Math 1
- [ ] Sim-seam boundary check: if any strategy requires sim-seam touch beyond combat-arithmetic deltas, flag to KR (escape-hatch per scope-doc § 6)

### Bucket 2 — L9 opportunity-scan refactor

- [ ] Identify all opportunity_scan trigger sites in mechanic_alteration.py + related modules
- [ ] Refactor ELEMENT_CONVERSION fire-resonance: cultural_tradition signal → mechanical signal (element + bc_target_cell)
- [ ] Refactor DEFENSIVE_CONVERSION heavy-armor: cultural_tradition signal → mechanical signal (bc_target_cell.defensive_profile + mechanical_substrate_triple)
- [ ] Other strategies: refactor any cultural_tradition reads to mechanical_substrate reads
- [ ] Discipline #25 verification: post-refactor empirically grep for cultural_tradition reads in opportunity_scan code path; should be ZERO
- [ ] Discipline #13a verification: opportunity_scan semantic intent preserved (same strategies fire for same kits modulo signal source)
- [ ] If mapping non-obvious for any strategy: STOP + flag to KR per scope-doc § 6 (KR routes to gandalf for design refactor)

### Bucket 3 — signature_chain_id population

- [ ] Implement cross-chain T4 election per Math 3 (max-η rule with deterministic tie-break)
- [ ] Populate SkillTree.signature_chain_id at Layer 6 wire-up
- [ ] Consume signature_chain_id in apply_t4_alteration_to_combat (use for build-defining wire-up; secondary chains' T4Alterations layer additional effects per rocket design judgment)

### Bucket 4 — validate_invariants runtime vocabulary check

- [ ] Add runtime node_type vocabulary check at L6 wire-up sites where SkillTree is consumed
- [ ] Document defensive-robustness rationale in math note

### Bucket 5 — Cross-seam emission contract

- [ ] Emit off_hand_contract in star-lord-serializable shape per Math 4
- [ ] Emit sim-combatant fields (combat-arithmetic deltas) per Math 4
- [ ] Emit Spirit Guide narration metadata per Math 4 + § 9 explainer pattern
- [ ] MIGRATION.md § v1.4-layer-6 documents all 3 emission shapes for downstream consumer reference
- [ ] **CROSS-SEAM CONSUMER WORK IS FOLLOW-ON** (NOT this dispatch scope): star-lord consumer (export schema extension), gamora consumer (sim combatant integration), drax consumer (Spirit Guide panel) are SEPARATE post-Layer-6 dispatches KR fires after L6 + Gate-2 PASS

### Bucket 6 — Smoke + acceptance

- [ ] Cheapest-refuting-test per Math 6 (6-strategy wire-up smoke + L9 refactor smoke + signature_chain_id smoke + integration smoke)
- [ ] Round-trip smoke per Principle 6 (full kit emission → JSON → deserialize)
- [ ] No regression on Cycle 11 § 8 + Layer 2/3/4 tests
- [ ] Discipline #2.1 resource-scaling rehearsal: wall-clock projection per Math 7

### Bucket 7 — Provenance + canonical

- [ ] Math note authored per Discipline #1 + #1.2 (code-line citations REQUIRED)
- [ ] MIGRATION.md extended per ADR-004
- [ ] generation/MIGRATION.md entry appended
- [ ] AGENT_STATE.md updated with Cycle 12 Wave 4 Layer 6 checkpoint
- [ ] Tag: `rocket/v0.1-cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25` (or per-bucket intermediate tags acceptable per rocket discretion)

---

## Out of scope (explicit non-goals)

- Cross-seam CONSUMER work (star-lord export schema extension; gamora sim combatant integration; drax Spirit Guide panel) — Layer 6 emits in consumable form; consumer code changes are FOLLOW-ON post-Layer-6 (separate KR-fired dispatches per seam)
- Layer 7 BDI test framework (DEFERRED to v1.1)
- Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn) — v1.1+
- Performance benchmarking beyond Discipline #2.1 resource-scaling rehearsal
- Architectural amendments to framing brief § 4 contract / canonical authority (LOCKED; escalate to gandalf via KR per scope-doc § 5)
- v1.1+ substrate-curation queue items (per Cycle 12 state file Decisions section)
- T4-B v1 catalogue contents — parallel-track gandalf + Matt design call

---

## Acceptance criteria

- [ ] Math note authored per Discipline #1 + #1.2 (code-line citations)
- [ ] Bucket 1 § 8 wire-up: 6 v1 strategies correctly applied to combat arithmetic per Math 1
- [ ] Bucket 2 L9 refactor: opportunity_scan triggers use mechanical_substrate signals (zero cultural_tradition reads post-refactor per Discipline #25)
- [ ] Bucket 3 signature_chain_id: cross-chain T4 election deterministic + correct per Math 3
- [ ] Bucket 4 validate_invariants runtime vocabulary check at L6 wire-up sites
- [ ] Bucket 5 cross-seam emission contracts present (off_hand_contract + sim-combatant fields + Spirit Guide narration metadata)
- [ ] Bucket 6 smoke gates PASS (6-strategy wire-up + L9 refactor + signature_chain_id + integration)
- [ ] Round-trip smoke PASS per Principle 6
- [ ] MIGRATION.md § v1.4-layer-6 authored per ADR-004
- [ ] No regression on Cycle 11 § 8 + Layer 2/3/4 tests
- [ ] AGENT_STATE.md updated
- [ ] Tag: `rocket/v0.1-cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25`

---

## Open questions for the agent to resolve

- Whether signature_chain_id election rule (max-η with deterministic tie-break per Math 3) is canonically correct OR T4-A § 2 specifies different election (rocket consults canon; if non-trivial, flag to KR for gandalf consultation)
- Whether secondary chains' T4Alterations should layer additional effects (per Math 3 rocket design judgment) OR be ignored at L6 wire-up (signature-only-wire-up alternative; recommend layer per T4-A hierarchy spirit; rocket judgment)
- Whether AlteredFightEngineContext is a new type OR mutated fight_engine_context (per framing brief § 4 contract — rocket judgment per simplicity vs traceability)
- Whether L9 refactor surfaces mapping that requires gandalf design consultation (per scope-doc § 6 escape-hatch) OR all 6 strategies cleanly map (rocket judgment per implementation)
- Whether 6th strategy (DEFENSIVE_TRADEOFF) requires distinct wire-up beyond what's implied by trade-off structural signature (rocket consults mechanic_alteration.py for STRATEGY_DEFENSIVE_TRADEOFF class implementation)

---

## Cross-seam impact

Round-trip: REQUIRED per Principle 6 — Layer 6 emits AlteredFightEngineContext + off_hand_contract + Spirit Guide narration metadata for cross-seam consumption.

If Layer 6 surfaces sim-seam boundary touch requirement for any v1 strategy: escape-hatch per scope-doc § 6 (route to gamora sub-agent for verification; if confirmed boundary, escalate to Matt for scope amendment — 4 of 6 strategies in v1 acceptable, 1 moved to v1.1 if needed).

---

## References

- `canonical/story/skill-system-2026-05-24.md` § 8 + § 9 (primary)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 + § L9 + § L10
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` § 1 + § 5 + § 6
- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (Cycle 11 § 8 — 6 strategies; L9 refactor target)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (original § 8 methodology)
- Layer 2 + Layer 3 + Layer 4 dispatches + completion records + Gate-2 findings
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-3.md` (INFO-D + INFO-3 + INFO-C deferred to L6)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-3-rocket-layer-4.md` (Layer 4 composability)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (§ v1.4-layer-2 post-amendments + § v1.4-layer-6 to author)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § 2 (signature_chain_id election authority)
- `canonical/story/off-hand-items-2026-05-24.md` § 2.3 (off_hand_contract emission shape)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q1 Option γ Layers 2+3+4+6) + skip-confirmation re-auth 2026-05-25 + KR autonomously orchestrates per scope-doc § 1
**Status:** FIRE — FINAL critical-path layer per Option γ; pre-Layer-6 amendments ✅ cleared; Layer 6 fires immediately

**Matt-touch sequence:** rocket Layer 6 implementation lands → jack-ryan Gate-2 validates → if PASS, KR coordinates: (1) Wave 5 integration smoke (L2 + L3 + L4 + L6 end-to-end through gauntlet); (2) jack-ryan Gate-2 on full new engine; (3) cross-seam follow-on dispatches per consumer seam (star-lord + gamora + drax) — these can fire in parallel as Wave 5 sidecars; (4) KR auto-closes Cycle 12 wind-down per skip-confirmation re-auth → T4 post-mortem readiness milestone. If Layer 6 surfaces sim-seam boundary requirement for any v1 strategy OR L9 refactor mapping non-obvious, route to escape-hatch per scope-doc § 5/§ 6
