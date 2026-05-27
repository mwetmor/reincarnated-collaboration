# Dispatch — 2026-05-27 — rocket — Cycle 13 Wave 1 Partition Implementation (W1.0-W1.8 Bundled)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 1 Gate-1 verdict PASS-with-WARN (commit `54bf1b8`) on doc 42 with W2 amendment folded into THIS dispatch + gandalf doc 42 amendment commits `6d4213b` (W1+W3+I1) and pending § 10 D9 leak fix
**Estimated effort:** ~16-32 hrs bundled implementation (8 sub-waves W1.0-W1.8); rocket may sub-checkpoint as appropriate
**Acceptance:** Wave 1 partition implementation landed per doc 42 (amended); modifier-surface enumeration + per-slot affinity matrix + per-rarity grid + tier-restricted modifier surface + per-slot probability normalization per § 9.2 step 2 + minimum-viable trait pool D8 + cross-cohesion validation; integration with existing engine seam (gear generation pipeline) per Principle 6 round-trip smoke

## Context

Cycle 13 Wave 1 is the stat-sheet partition design + implementation cycle — per framing brief § 3 Wave 1 + closeout § 3.2/3.3 + doc 40 § 3.6 + doc 42 (gandalf-authored INTENT canonical; commit `64d1e33` amended `6d4213b`).

Gandalf authored doc 42 partition INTENT (51.8KB; 528 lines) → jack-ryan Gate-1 PASS-with-WARN (commit `54bf1b8`) → gandalf W1+W3+I1 amendments landed (commit `6d4213b`). Rocket implementation against doc 42 is now unblocked.

Doc 42 § 9 provides Wave 1 implementation sub-wave structure W1.0-W1.8. This dispatch bundles all 8 sub-waves for single rocket invocation (sub-checkpoint commits as appropriate).

**Per jack-ryan Gate-1 W2 amendment (FOLDED INTO THIS DISPATCH per next-action sequence):** prefix/suffix binary schema field MUST be REQUIRED W1.2 schema-implementation deliverable. SC-4 Gate 1 states "cannot be retrofitted easily" — must land at schema-time, not bolt-on later.

**Per jack-ryan Gate-1 W3 routing:** Wave-2-informing SC-4 expansion findings (5th Scaling-interaction synergy category + Pattern 9+10 degenerate-state) are explicitly Wave 2 scope, NOT Wave 1. Do not implement here; Wave 2 dispatch authoring (KR work post-Wave-1-close) will invoke them.

**Per jack-ryan Gate-1 I2 routing:** Disciplines #27 / #31 / #32 are Wave 2 scope (T4 algorithm); do not apply to Wave 1 partition implementation.

**Per W1 amendment + § 9.2 step 2 normalization:** affinity matrix tier weights (50/30/15/5) are RELATIVE; raw per-slot sums range ~190-255; implementation MUST normalize per § 9.2 step 2 procedure (`raw_weight / raw_sum`). Foreseeable error if implementation treats tier weights as absolute percentages summing to 100.

## Required reading before starting

1. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` (the design intent canonical; specifically § 2 amended + § 3 per-rarity grid + § 4 tier-restricted surface + § 5 sample modifiers + § 6 6 principles + § 7 SC-4 5 gates closure + § 8 minimum-viable trait + § 9 sub-wave structure W1.0-W1.8 amended + § 9.2 step 2 normalization procedure amended + § 10 close criterion)
2. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md` (jack-ryan Gate-1 critique; W2 amendment specifics for W1.2 schema design)
3. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (post-amendment foundation; capability toolkit + spec-driven gear gen + per-rarity intent)
4. `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid + node-to-level-band mapping)
5. `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (Block C scaffolding; cohort archetypes for cross-cohesion validation per W1.7)
6. `agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md` (legolas SC-4 base research; 5 methodology gates substrate)
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code + #1.2 code-citation + #11 empirical inspection + #18 methodology + #26 playability + Principle 6 round-trip)
8. `agentic_orchestration/operating-procedures/rocket.md` (your operating procedure — generation + engine canonical authority)
9. Existing gear/stat-sheet code paths: `reincarnated-engine/src/reincarnated/generation/` for gear generator + element/anchor/foundation interactions; `reincarnated-engine/src/reincarnated/foundation/` for trait_schema.py / gear_schema.py / class_schema.py (per gandalf D8 minimum-viable trait pool integration)

## Math-before-code (#1 — REQUIRED)

Per Discipline #1 math-before-code, before W1.2 schema-implementation:

- [ ] Document the per-slot normalization math: `raw_weight(S, C) = tier_weight(affinity_tier)` where affinity_tier ∈ {primary 50, secondary 30, tertiary 15, off-affinity 5}; `raw_sum(S) = Σ_C raw_weight(S, C)`; `normalized_weight(S, C) = raw_weight / raw_sum`. Verify against doc 42 § 9.2 step 2 amended pseudocode.
- [ ] Document the per-rarity modifier count math: per § 3 grid (Common 1-2 / Uncommon 2-3 / Rare 3-4 / Epic 4-5 / Legendary T0-T2 4-5 + density gradient / Set T1-T2 endgame-only).
- [ ] Document the tier-restricted modifier surface math: ~10-20% of modifier types tier-restricted per doc 42 § 4; explicit modifier-to-tier mapping schema.
- [ ] Document the prefix/suffix binary partition math per jack-ryan W2: schema field at modifier-instance level; load-bearing at schema-time per SC-4 Gate 1 "cannot be retrofitted easily."

## Cross-seam contract change? (Principle 6 gate)

**Round-trip REQUIRED.** Wave 1 partition implementation introduces NEW schema (per-slot affinity matrix + per-rarity grid + tier-restricted surface + prefix/suffix binary + minimum-viable trait pool). Downstream consumers (existing gear generation pipeline + future Wave 4 spec-driven gear gen + future loadout app gear display) reference this schema.

**Round-trip smoke:** Generate ≥1 gear instance per rarity tier (Common / Uncommon / Rare / Epic / Legendary T0) via implemented partition schema; verify field-presence + type-consistency; verify prefix/suffix binary correctly captured; verify per-slot affinity probability normalizes to 1.0 sum; verify tier-restricted modifier surface enforcement.

**MIGRATION.md required** if schema field renamed / removed from existing gear schema (per ADR-004).

## Scope

### W1.0 — Substrate prep + repo-scaffold

- [ ] Review existing gear generation code (path + line citations per Discipline #1.2); identify schema entry points for partition-aware modifier rolling
- [ ] Scaffold new partition-aware schema modules per doc 42 § 9.1 (schema module structure)

### W1.1 — Schema design

- [ ] Author per-slot affinity matrix schema (9 categories × 11 slots) per doc 42 § 2 (RELATIVE weights with normalization per § 9.2 step 2)
- [ ] Author per-rarity grid schema per doc 42 § 3
- [ ] Author tier-restricted modifier surface schema per doc 42 § 4
- [ ] **Author prefix/suffix binary field at modifier-instance level per W2 amendment** — REQUIRED W1.2 schema-implementation deliverable per jack-ryan Gate-1 next-action; SC-4 Gate 1 "cannot be retrofitted easily"
- [ ] Schema design review (self-critique; spot-check against doc 42 § 6 principles); commit math-note before implementation per #1

### W1.2 — Schema implementation

- [ ] Implement per-slot affinity matrix with normalization per § 9.2 step 2 procedure (`raw_weight → raw_sum → normalized_weight = raw/sum`); UNIT TEST normalization sums to 1.0 per slot
- [ ] Implement per-rarity grid with category-rollable enforcement per § 3
- [ ] Implement tier-restricted modifier surface with enforcement check (modifier type → rarity tier minimum)
- [ ] Implement prefix/suffix binary field per W2
- [ ] Round-trip smoke per Principle 6: generate ≥1 gear instance per rarity tier; field-presence + type-consistency verified

### W1.3 — Per-category implementations: Damage + Defense + Resource + Crit + Speed + Resistance-Penetration + On-trigger + Build-identity + Utility-Meta-progression

- [ ] Per § 5 sample modifier enumerations, implement starter modifier-pool per category per slot family (5-10 modifiers per category per slot family; not exhaustive)
- [ ] Wire modifier-pool to per-rarity grid (which rarities can roll which categories) + per-slot affinity (which categories slot prefers)

### W1.4 — Capability toolkit at Legendary T0-T2

- [ ] Per doc 42 § 7 SC-4 Gate 5 LOCKED HYBRID + Verdict B.2 capability-toolkit-legendary-exclusive: implement capability toolkit surface as legendary-tier-exclusive (not random rare affix pool)
- [ ] Capability toolkit categories per doc 40 (post-amendment): triggered-passive + true-active (extremely rare)
- [ ] Validate cross-ARPG consensus per legolas SC-4 base research (Finding 1)

### W1.5 — Set bonus structure (Set T1-T2 endgame-only)

- [ ] Per doc 42 § 3 + closeout § 3.4: 4-piece sets standard (2pc minor always-active + 4pc full T4-attuned content)
- [ ] Implement set bonus rank schema field; set bonus content composition with T4-attunement annotation per content-compositional attunement (closeout § 3.4 + doc 40 D33+D38+D51 amended)

### W1.6 — Trait integration (D8 ONLY per amended § 9 + § 8 + § 10 amended)

**SCOPE: D8 ONLY.** D9 element/mechanic-gating gear-affix trait surface = Wave 4 scope per § 8 text + § 9 W1.6 amended + § 10 amended.

- [ ] Implement minimum-viable per-class intrinsic trait pool per Verdict D.1 + doc 42 § 8: 55-entry pool; per-archetype composition; class_schema.py:46-47 reference (verify line exists per #1.2)
- [ ] Wire trait pool to class generator (Phase 2a kit composition consumer)
- [ ] Skip D9 (gear-affix element/mechanic-gating) — Wave 4 scope

### W1.7 — Cross-cohesion validation (per doc 42 § 6 principle 6 + § 26 playability)

- [ ] Per doc 42 § 9.5: validate affinity matrix produces build-diversity via spot-check simulation across cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C C_archetype lock); reference Block C scaffolding § 2.3 per-cohort KPM expectation
- [ ] Smoke test: generate N=10-20 gear instances per cohort archetype × per cell sample; verify affinity matrix produces diverse modifier rolls (not degenerate clustering on 1-2 categories)

### W1.8 — Round-trip smoke + tag-commit

- [ ] End-to-end smoke: existing engine consumer (gear generation pipeline) reads new partition schema + generates gear sample; field-presence + type-consistency + normalization correctness verified
- [ ] MIGRATION.md if schema field renamed / removed (per Principle 6); document new schema fields per ADR-004
- [ ] AGENT_STATE.md updated per session end
- [ ] Tag intent: `rocket: Cycle 13 Wave 1 partition implementation — W1.0-W1.8 bundled per doc 42 amended + jack-ryan Gate-1 W2 folded`

### Discipline compose-check

- [ ] #1 math-before-code: math-note per § Math-before-code above
- [ ] #1.2 code-citation: all references to existing code (file + line)
- [ ] #11 empirical inspection: post-script empirical count assertions per WU dimension (CRITICAL — 3rd opportunity to close WARN-pattern per skill_handoff_2026-05-26 § 1 Priority 2)
- [ ] #18 methodology: partition implementation IS the methodology output for Wave 1
- [ ] #26 playability: cross-cohesion validation per W1.7 operationalizes
- [ ] Principle 6 round-trip: smoke test PASSes per W1.2 + W1.8

## Acceptance criteria

- [ ] All 8 sub-waves W1.0-W1.8 land
- [ ] Per-slot affinity matrix normalization PASSes unit test (sums to 1.0 per slot)
- [ ] Prefix/suffix binary field per W2 amendment present in schema
- [ ] Capability toolkit legendary-exclusive enforcement PASSes
- [ ] Minimum-viable trait pool (D8 ONLY) implemented per Verdict D.1
- [ ] Cross-cohesion validation per #26 + Block C scaffolding produces non-degenerate spot-check
- [ ] Round-trip smoke per Principle 6 PASSes
- [ ] MIGRATION.md updated if cross-seam contract change per ADR-004
- [ ] Post-script empirical count assertions per WU dimension (Discipline #11 + WARN-pattern)
- [ ] Tagged commit per rocket convention

## Out of scope (explicit non-goals)

- D9 element/mechanic-gating gear-affix trait surface — Wave 4 scope per doc 42 § 8
- Wave 2 T4 algorithm implementation (Phases 1-2)
- Wave 3 T4 algorithm Phase 3 (character-wide vs chain-wide dimension)
- Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling
- Wave 5 gauntlet sim + season generation
- 5th Scaling-interaction synergy category implementation (per W3 routing — Wave 2 scope)
- Pattern 9+10 degenerate-state catalog implementation (per W3 routing — Wave 4 scope)
- Disciplines #27/#31/#32 implementation (per I2 routing — Wave 2 scope)
- jack-ryan Gate-2 verification (post-rocket-implementation; separate dispatch)
- gamora SC-7 methodology consultation FULL execution (post-Wave-3-baseline per #18.2)
- Modifying doc 40 / doc 41 / doc 42 (cross-seam gandalf authority)
- Production telemetry DB migration v2.16 ALTER TABLE per ADR-006

## Open questions for the agent to resolve

- W1 sub-wave sequencing: W1.0 → W1.1 → W1.2 (depends on W1.1) → W1.3-W1.5 (depend on W1.2) → W1.6 → W1.7 (depends on W1.3-W1.5) → W1.8. Some W1.3-W1.5 + W1.6 can interleave; your seam-owner call
- Schema implementation form: extend existing gear_schema.py vs new partition_schema.py module — your call per existing engine canonical structure
- W1.7 cross-cohesion validation N-sample: 10-20 per cohort × per cell sample recommended; adjust per resource-bounds (#1.1)
- MIGRATION.md scope: minimal (new schema fields) vs comprehensive (cross-seam impact mapping); recommend minimal per Principle 6 unless impact significant

## References

- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` (amended; commits 64d1e33 → 6d4213b)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md` (Gate-1 W2 amendment)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (cohort archetypes for W1.7)
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md` (SC-4 base; Gate 1-5 substrate)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (amended)
- `canonical/41-progression-framework-2026-05-27.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #26 + Principle 6)
- `agentic_orchestration/operating-procedures/rocket.md`

---

**Cycle:** 13
**Wave:** 1 implementation (W1.0-W1.8 bundled)
**Gates:** Wave 1 close = jack-ryan Gate-2 PASS on this implementation + Cycle 13 Wave 2 T4 algorithm Phases 1-2 dispatch authoring unblocked
**Priority:** P1 — critical-path Wave 1 close-gate
