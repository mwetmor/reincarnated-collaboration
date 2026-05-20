# Dispatch — 2026-05-21 — rocket — W0.2: Archetype template Path-a refactor (LC-001) — REMOVE templates entirely under substrate-as-cohesion-only

**From:** knight-rider
**To:** rocket (generation seam)
**Approved by:** **Matt 2026-05-21 substrate-as-cohesion-only ratification "1 = yes / 2 = yes / 3 = yes / all 3 confirmed. Free to write."** (gandalf attestation 2026-05-21 § 3.3 — implicit approval via substrate-as-cohesion recommitment); per activation dispatch § 2.0 + § 4 Step 4 W0.2; protocol § 6.1.5 (structural change normally requires Matt; ratification carried by substrate-as-cohesion approval)
**Status:** PENDING — ACTIVE (rocket may execute when launched)
**Estimated effort:** ~most of P0 duration (~1-2 weeks; the largest structural change in P0)
**Acceptance:** `ARCHETYPE_TEMPLATES` hardcoded dict REMOVED; generation is pure BC-target-driven composition from unified substrate-AGNOSTIC mechanic pool; role-shape constraints applied as composition objectives; no substrate tagging at generation; tag `qd-rebuild/v0.2-archetype-refactor-complete`.

---

## Context — the architectural recommitment

Per `canonical/story/substrate-design-supplement-2026-05-21.md` § 5.1: **W0.2 becomes EVEN SIMPLER than the original protocol framing.** The original framing called for refactoring `ARCHETYPE_TEMPLATES` into substrate × role × BC composition. Under substrate-as-cohesion-only, the right move is to **remove archetype templates entirely**.

**Why simpler:** under substrate-as-cohesion, substrate identity is a cohesion-layer label assigned post-generation by the LLM cohesion-judge. Mechanical generation is substrate-AGNOSTIC and BC-target-driven. There is no architectural reason to maintain per-substrate templates at the generation layer — they would re-create the archetype-lock pathology the QD-engine is designed to break.

**The recompose-hive empirical finding** (kit-composition pathology IS the load-bearing problem; 100% Pattern-A across all 7 substrates at same calibration per Alt A + Track C) confirms this: archetype-lock prevents the engine from generating diverse kit compositions to populate BC space. Removing templates is the architectural fix.

## What this dispatch does — the new generation logic

Per substrate supplement § 5.1, the on-boot composition logic becomes:

```
For each BC-target (cell coordinate from QD-archive Phase 1):
  1. Receive BC-target
  2. Decompose target into per-axis composition objectives:
     - Engagement bin → range + mobility constraints
     - Geometry bin → damage delivery shape requirements
     - Proxy bin → proxy entity count constraint
     - Control bin → CC budget fraction
     - Tempo bin → damage event rate target
     - Variance bin → per-event magnitude variance target
     - Defensive bin → eHP and avoidance requirements
     - Economy bin → resource pattern target
  3. Compose kit from unified substrate-AGNOSTIC mechanic pool to satisfy objectives
  4. Apply role-shape constraints (damage / control / support / hybrid)
  5. Return kit; NO substrate tagging
```

The mechanic pool is unified (no per-element subset). Mechanics are NOT pre-tagged with substrate identity at the generation layer. Substrate identity is assigned in Phase 5 (cohesion coalescence) by the LLM cohesion-judge.

## Implementation steps

### Step 0 — Math-before-code (Discipline #1; REQUIRED)

Author a math note at `reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md`. Cover:

1. **Decomposition map**: per Axis (1, 2, 2A, 2B, 3A, 3B, 4, 5), what composition objective does the bin translate to?
2. **Unified mechanic pool specification**: what's in the pool? (preserved from current archetype templates' mechanic content, but with substrate tags STRIPPED). Inventory the pool.
3. **Role-shape constraint formalization**: damage / control / support / hybrid — what does each constrain in the composition?
4. **Composition algorithm**: pseudocode for the 5-step logic above. Include: how the algorithm picks among candidate mechanics when multiple satisfy an objective; how it handles infeasible BC-targets (return None? Best-effort? Reject?)
5. **Backward compatibility**: existing season generation must continue to produce kits (with implicit BC-targets derived from current archetype defaults). Document the migration shim.

### Step 1 — Inventory existing pool

Pull from `b6_archetype_templates.py` (the dict being removed) + canonical library (`canonical/library/` if equivalent location exists) + any other generation-side template source. Strip substrate tagging from each mechanic. Produce a unified-pool YAML or JSON at `generation/unified_mechanic_pool.yaml` (or equivalent).

Note: cross-references for substrate identity (`config/substrate_identities/`) are PRESERVED — they're cohesion-layer reference docs now per § 5.3 of substrate supplement. They DO NOT constrain generation.

### Step 2 — Implement composition algorithm

Target files:
- `src/reincarnated/generation/b6_archetype_templates.py` — REMOVE `ARCHETYPE_TEMPLATES` dict (or DEPRECATE in-place with all references gated to fall through to new path; choice yours)
- New file: `src/reincarnated/generation/bc_target_composer.py` (or equivalent) — the composition logic
- `src/reincarnated/generation/class_generator.py` — call new composer
- `src/reincarnated/foundation/foundation.py` — verify validator still passes under new generation (likely just D5-aligned 7-substrate count is sufficient; coordinate with W0.3)

### Step 3 — Backward compatibility shim

Existing tests + season fixtures use archetype-template-based generation. For migration:
- If existing test calls `archetype_template_for("water_mage", level=1)` → translate to "BC-target derived from water_mage's defaults" → return kit via new composer
- Migration shim file at `generation/legacy_archetype_shim.py` that translates between old archetype names and BC-target equivalents
- Existing tests must still PASS during migration (179/179)

The shim is TEMPORARY — slated for removal at P5 W5.X when cohesion-judge is operational and substrate labels coalesce naturally. Document the removal trigger.

### Step 4 — Smoke + tests

Per Discipline #2:
- `pytest tests/` full suite — 179/179 PASS (or current baseline)
- `--smoke` regen on a 5-class smoke season — verify new composer produces valid kits + no crashes
- Compare new-composer kit BC distribution vs old-template kit BC distribution — document differences (Discipline #11.1: cold-start canonical convergence on both)

### Step 5 — MIGRATION.md (cross-seam)

The archetype removal affects how downstream consumers identify kits. Specifically:
- **gamora (simulation)**: skill metadata reads — does sim read `archetype_name` field anywhere? Most likely yes (logging, telemetry). Coordinate at boundary.
- **star-lord (telemetry/export)**: `class_fight_loadouts` table likely has archetype column → schema implication
- **drax (demo)**: archetype name surfaces in player-facing UI? Likely yes (class selection screens; spirit-guide narration)

MIGRATION.md entry per ADR-004. The substitution: in the migration period, kits carry a synthesized `archetype_label` derived from the composition's mechanical signature; at P5 (cohesion coalescence), the cohesion-judge supersedes the synthesized label with a properly-themed substrate-cohesion label.

### Step 6 — Tag

Intermediate tag: `qd-rebuild/v0.2-archetype-refactor-complete` (after Step 5 ships + cross-seam consumers confirmed via R11(b) round-trip).

## Required reading before starting

- `canonical/story/substrate-design-supplement-2026-05-21.md` (full document — operative architecture)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` § 2 Phase 2 (BC-target-driven generation; critical principle: "Substrate is NOT an input to this phase")
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.0 (architectural recommitment)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-001 entry
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` (the pre-substrate-as-cohesion archaeology of archetype templates; useful for understanding what's being removed)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` (uniform-depth substrate enrichment confirmed; differentiated archetype templates rejected by data)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1, #2, #11.1, #13a, R11(b))
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (your prior records)

## Math-before-code (REQUIRED for this dispatch)

See Step 0 above. The math note is the gate — author it FIRST. Knight-rider will route the math note for gandalf review (architectural alignment — does the composer satisfy substrate-as-cohesion?) + jack-ryan review (implementation correctness; design intent verification) BEFORE code change starts.

## Cross-seam contract change? (Principle 6 gate)

**YES** — archetype removal affects how gamora / star-lord / drax identify kits.

**Round-trip smoke: in-migration period, kits carry synthesized `archetype_label` derived from composition mechanical signature. Production-path fixture: convergence run of 1 kit through new composer → balance loop → telemetry → demo consumer. Consumer boundary exercised: each downstream seam reads the (synthesized OR cohesion-assigned) label field without error. Field-presence check: `archetype_label` populates in `class_fight_loadouts` for the test kit; downstream consumers handle non-substrate-bound label correctly.**

MIGRATION.md entry per ADR-004 — see Step 5.

## Scope

- [ ] Math-before-code note authored (Step 0; route through knight-rider for gandalf + jack-ryan review BEFORE code change)
- [ ] Unified mechanic pool inventoried (Step 1; YAML/JSON deliverable)
- [ ] Composition algorithm implemented (Step 2)
- [ ] Backward compatibility shim implemented (Step 3)
- [ ] Smoke + 179/179 tests PASS (Step 4)
- [ ] MIGRATION.md entry per ADR-004 (Step 5)
- [ ] Round-trip smoke per Principle 6
- [ ] AGENT_STATE.md updated
- [ ] Tag: `qd-rebuild/v0.2-archetype-refactor-complete`

## Acceptance criteria

- [ ] `ARCHETYPE_TEMPLATES` dict REMOVED or DEPRECATED + unreferenced
- [ ] Generation produces kits via BC-target-driven composition from unified substrate-AGNOSTIC mechanic pool
- [ ] No substrate tagging at generation (kits emerge substrate-blind; substrate label assigned at Phase 5 cohesion-judge)
- [ ] Role-shape constraints (damage / control / support / hybrid) applied as composition objectives
- [ ] Existing tests + smoke seasons PASS (179/179 baseline preserved)
- [ ] Round-trip smoke: synthesized `archetype_label` field populates + downstream consumers handle it
- [ ] Math note vs measurement: documented (Discipline #1)
- [ ] BC distribution comparison (new-composer kits vs old-template kits): documented (Discipline #11.1)

## Out of scope

- Skill tree node population (W1.13; P1)
- Gauntlet architecture migration (W0.9; gamora)
- Foundation validator update (W0.3; rocket; separate dispatch)
- Cohesion-judge integration (P5)
- Multi-dim convergence optimizer (P2/P3)
- Profile A/B/C/D filtering (P6)
- Theme library refactor (P5 W5.2)
- LLM-side prompt construction changes (separate scope from this dispatch's mechanical-generation refactor; though LC-006 + LC-014 may surface as drift candidates during inspection)

## Open questions for the agent to resolve

- **ARCHETYPE_TEMPLATES disposition**: REMOVE entirely vs DEPRECATE + leave for archaeology? Document choice with reasoning. Recommendation: DEPRECATE in-place + leave for archaeology (per recompose-hive precedent of preserving infrastructure under soft-disable); fully REMOVE at P5 W5.X cleanup.
- **Synthesized `archetype_label` format**: should it be a string like `"close-fast/large-AOE/tank/HP-economy"` (BC-coordinate-derived) or something more human-readable? Per substrate supplement § 5.4, P5 cohesion-judge supersedes this — so it's transitional. Recommendation: BC-coordinate-derived for unambiguous mapping; document format in MIGRATION.md.
- **Hybrid mechanical compositions** (per substrate supplement § 3 Principle 3): how does the composer handle "vampiric warrior" (shadow + physical mechanical signature)? Test case: ensure the composer can produce hybrid kits — they should be natural outputs, not exceptional cases. Document handling.
- **Infeasible BC-target handling**: when can a BC-target not be satisfied by any composition? Document — likely: cells in deferred-bin regions (proxy-light/heavy; HP-economy; etc.) that require P4 sim extensions. The composer should route those to deferred-evaluation pool (per protocol § 6.1.4 deferred-evaluation rule).
- **Energy-type-aware tier semantics carry-forward**: the 2026-05-16 B6 pre-work shipped tier-shifts for rage/physical archetypes (`rocket/v1.3-b6-energy-type-tiers`). Under substrate-AGNOSTIC composition, does the energy-type tier-shift carry forward as a generation property of certain mechanic types (those associated with "rage" pillar) regardless of substrate label? Document handling; coordinate with W0.1 (B14.5 V2; gamora simulation; energy-type lever in primary recompose loop).

## Critique-pair structure

- **gandalf** reviews architectural alignment (substrate-as-cohesion preservation; cross-substrate hybrid handling; recompose-hive empirical finding alignment; Track C uniform-depth alignment)
- **jack-ryan** reviews implementation correctness (LC-001 closure verified; LC-007 + LC-008 drift implications surfaced; cross-seam round-trip per R11(b); Discipline #13a drift check)
- **Matt approval already on record** for the substrate-as-cohesion architectural framing this dispatch implements

## References

- `canonical/story/substrate-design-supplement-2026-05-21.md` § 5.1 (the architectural simplification)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` § 2 Phase 2 (BC-target-driven generation operational spec)
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.0 + § 4 Step 4 W0.2
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.2 + § 6.1.5 (Matt-approval normally; carried by substrate-as-cohesion ratification here)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-001
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` (pre-refactor archaeology)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` (Track C empirical reinforcement)
- `agentic_orchestration/dispatches/2026-05-16-rocket-b6-pre-work-energy-type-aware-tiers.md` (energy-type tier-shift carry-forward question)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-21 QD-rebuild activation entry (substrate-as-cohesion recommitment ratification)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1, #2, #11.1, #13a, R11(b), Pattern P7)
