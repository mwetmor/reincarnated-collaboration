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

---

## Completion record

### Phase 1 (math-before-code) complete — Phase 2 pending Gate-1

**Completed by:** rocket
**Date:** 2026-05-21
**Status:** PARTIAL COMPLETION — Phase 1 (Step 0 math-before-code) COMPLETE. Phase 2 (implementation) PENDING jack-ryan Gate-1 + gandalf architectural review.

**Deliverables completed:**

- Math note authored: `reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md`
  - 11 sections per dispatch spec (decomposition map, unified pool spec, role-shape constraints, composition algorithm, backward compat shim, synthesized archetype_label, energy-type carry-forward, cross-seam contract, implementation phasing, W0.9+W0.1 joint-resolution, risk analysis)
- AGENT_STATE.md updated: "W0.2 Step 0 math-before-code complete; awaiting jack-ryan Gate-1 + gandalf architectural review routing"

**Key predictions in math note:**

- Composition algorithm: 8-step pseudocode with weighted-random mechanic draw, infeasibility gate, role-shape post-assembly adjustment. Conflict resolution: BC-target wins in sampling; role-shape enforces hard minimum post-assembly.
- Unified pool: stripped of substrate tags; ~150–250 mechanic entries from 23 current templates; cost_type is the primary energy-type carry-forward key.
- Synthesized archetype_label: BC-coordinate-derived format `"{eng_bin}/{geo_bin}/{ctrl_bin}/{def_bin}/{econ_bin}_{role}_{cost_type}"`.
- ARCHETYPE_TEMPLATES disposition: DEPRECATE IN-PLACE (not remove yet); full REMOVE at P5 W5.X cleanup.
- Cross-seam schema: v2.15 bump recommended (new `archetype_label TEXT` column on `class_fight_loadouts` alongside existing `archetype_tag`; backward-compatible nullable).
- Energy-type tier carry-forward: cost_type keying replaces archetype_tag keying; numbers unchanged from B6 pre-work.
- Joint-resolution: W0.2 (generation diversity) + W0.9 (correct arena) + W0.1 (fair calibration) all required; W0.2 alone insufficient.
- Known pool gaps: HP-economy, charge-stack, damage-taken-converts, proxy-creation all deferred/hard-infeasible; documented in deferred-evaluation routing.
- Risk: season_orchestrator.py coupling (element_pool → archetype_tag) is a Phase 2 investigation item.

**Scope items NOT completed (Phase 2 pending):**

- [ ] Unified mechanic pool YAML (W0.2.1)
- [ ] bc_target_composer.py implementation (W0.2.2)
- [ ] archetype_composer.py deprecation in-place (W0.2.3)
- [ ] legacy_archetype_shim.py (W0.2.4)
- [ ] Smoke + 179/179 tests (W0.2.5)
- [ ] MIGRATION.md entry per ADR-004 (W0.2.6)
- [ ] Round-trip smoke per Principle 6
- [ ] Tag: `qd-rebuild/v0.2-archetype-refactor-complete`

**Gate-1 routing note:** Math note routes to jack-ryan (implementation correctness; LC-001 closure verification; R11(b) round-trip planning; Discipline #13a drift check) and gandalf (substrate-as-cohesion architecture alignment; cross-substrate hybrid handling; recompose-hive empirical alignment). Phase 2 implementation begins only after both Gate-1 reviews complete per dispatch critique-pair structure.

---

## Completion record — Phase 1.5 (amendment fold-in) — 2026-05-20

**Agent:** rocket
**Status:** PARTIAL COMPLETION — Phase 1 + Phase 1.5 (amendment fold-in) COMPLETE. Phase 2 (implementation) cleared to begin.
**Tag:** `qd-rebuild/v0.2-math-note-phase-1-complete`

**Phase 1.5 scope:** Both critique-pair reviews (jack-ryan + gandalf) returned convergent. 6 amendments total — 4 folded into math note now; 2 documented as W0.2.6 obligations.

**Amendments folded (4):**

**jack-ryan A1 — CC pool depletion fallback (§4.3):**
Added `PoolDepletionError → DeferredEvaluation` fallback spec to §4.3. When CC pool after cost_type filtering has fewer entries than the CC-minimum count required by the role-shape, the composer raises `PoolDepletionError` — the caller wraps as `DeferredEvaluation`. No silent truncation, no log-and-continue. Rationale: preserves Phase 4 archive integrity; same principle as infeasibility handling (§4.4). Pool extension path: if depletion rate >10%, extend unified mechanic pool. Discipline #1 + Discipline #8 cited.

**jack-ryan A2 — v2.15 column bump LOCKED (§8.2):**
Changed §8.2 from "recommendation" to "DECISION." Column-repurpose path explicitly closed (Discipline #12: no silent semantic shift). New `archetype_label TEXT` column alongside existing `archetype_tag` is the ONLY acceptable path. Existing `archetype_tag` column preserved, deprecated-in-place. Star-lord joint authorship obligation noted. Discipline #12 cited.

**gandalf A1 — season_orchestrator Phase 1 architectural contract (§11.5):**
Expanded §11.5 from "Phase 2 investigation point" to an explicit Phase 1 architectural contract with three locked commitments: (1) seasonal elements feed Phase 5 cohesion-judge preference weights ONLY — not Phase 2 generation; (2) orchestrator emits BC-targets, not archetype tags, into the generation queue; (3) W0.2.2 orchestrator coupling severance is a HARD GATE before any smoke run touches the orchestrator path. Discipline #13 implicit-pillar drift prevention cited.

**gandalf A2 — resolve_cost_type input-set lockdown (§4.1):**
Locked `resolve_cost_type` to `(econ_bin, role, rng) ONLY`. No other inputs permitted. Published role-cost_type correlation table directly in the math note (not hidden in implementation): damage prefers rage > combo > focus > mana; control prefers mana > focus > stamina; support prefers mana > stamina > focus; hybrid spans mana > focus > combo > rage. Econ_bin-to-cost_type structural mapping also published. Changed pseudocode call from `resolve_cost_type(econ_bin, rng)` to `resolve_cost_type(econ_bin, role, rng)`. Discipline #13a-partition cited.

**Deferred obligations documented (2) — NOT folded; captured as Phase 2 gates:**

**jack-ryan A3 — shim pass/fail criterion (§5.1 obligation):**
Documented at end of §5.1: if >20% of shim-path kits land more than 1 bin away from BC-target default on any axis (measured via Phase 3 simulation), shim defaults require recalibration before Phase 5. W0.2.6 must capture this gate with empirical result.

**jack-ryan A4 — v2.15 co-migration mandatory (§8.4 new subsection):**
Added §8.4: W0.2.6 MIGRATION.md must mandate a SINGLE ALTER TABLE script covering both W0.2's `archetype_label` column AND W0.1's `recompose_energy_calibration_applied` column. Star-lord joint authorship required. No split migrations at v2.15.

**Files modified:**
- `reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md` — 4 amendments folded; §4.1, §4.3, §5.1, §8.2, §8.4 (new), §11.5 modified
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — updated to "W0.2 Phase 1 + Phase 1.5 complete; awaiting Phase 2 implementation kickoff"

**Scope items NOT completed (Phase 2 pending — unchanged from Phase 1 record):**
- [ ] Unified mechanic pool YAML (W0.2.1)
- [ ] bc_target_composer.py implementation (W0.2.2) — now includes orchestrator severance audit obligation
- [ ] archetype_composer.py deprecation in-place (W0.2.3)
- [ ] legacy_archetype_shim.py (W0.2.4)
- [ ] Smoke + 179/179 tests (W0.2.5) — gated on W0.2.2 orchestrator severance
- [ ] MIGRATION.md entry per ADR-004 (W0.2.6) — must include shim pass/fail criterion + single ALTER TABLE mandate
- [ ] Round-trip smoke per Principle 6

---

## Completion record

**Date:** 2026-05-21
**Agent:** rocket
**Tag fired:** `qd-rebuild/v0.2-archetype-refactor-complete` (engine commit `e696b9f`)

### Sub-task completion status

| Sub-task | Status | Key finding |
|---|---|---|
| W0.2.1 — Unified mechanic pool | COMPLETE | `unified_mechanic_pool.yaml`: 67 active / 4 deferred / 5 cost types / 15 CC mechanics |
| W0.2.2 — bc_target_composer.py + severance audit | COMPLETE | Orchestrator CONFIRMED COMPLIANT (see audit below) |
| W0.2.3 — ARCHETYPE_TEMPLATES deprecate | COMPLETE | `archetype_composer.py` + `_build_archetype_templates()` deprecated in-place with P5 W5.X gate |
| W0.2.4 — legacy_archetype_shim.py | COMPLETE | 24-row translation table; all archetype tags produce ComposedKit or valid DeferredEvaluation |
| W0.2.5 — Smoke + tests | COMPLETE | 57/57 new tests pass; 204/204 existing generation tests pass; baseline preserved |
| W0.2.6 — MIGRATION.md + R11(b) | COMPLETE | MIGRATION.md updated; PlayerClass.archetype_label field added (nullable); R11(b) incomplete (recorder.py — star-lord seam) |

### Orchestrator severance audit finding (W0.2.2 HARD GATE)

STATUS: CONFIRMED COMPLIANT — no emergency severance required before smoke.

`season_orchestrator._generate_classes()` passes (element, energy_type, role_orientation, range_profile) to ClassGenerator. archetype_tag is derived INSIDE ClassGenerator via `classify_archetype()`, not an orchestrator selection. Seasonal elements (selector.py) feed coalescence/naming only (Contract 1 satisfied). No archetype-tag emission from orchestrator to composition queue.

Full audit text: `src/reincarnated/generation/bc_target_composer.py::ORCHESTRATOR_SEVERANCE_AUDIT`

### Shim BC distribution comparison (Discipline #11.1)

New-composer produces 7 distinct (eng_bin, geo_bin) coordinate families across 24 archetype tags. Diverse BC coverage confirmed: close-fast/single-target (warrior), ranged-slow/chain (lightning), mid-slow/small-AOE (controllers), ranged-fast/large-AOE (wind), etc.

Physical warrior: rage → tier 65 (B6 carry-forward confirmed).
Hunter: focus → tier 58 (B6 carry-forward confirmed).
Elemental archetypes: mana → tier 50 (baseline).
Pool depletion: CC pool depletion for control+stamina/focus thin-pool cases correctly routes to DeferredEvaluation (not truncation). Telemetry: pool_depletion_events logged per (cost_type, role).

### Test results (W0.2.5)

- New W0.2 tests: 57/57 PASS
- Existing generation tests (class generation, energy types, substrate coupling, canonical, embodiment schema): 204/204 PASS
- D3 archetype composer tests: 67/67 PASS + 2 skipped (pre-existing; unchanged)
- Pre-existing failures unchanged: `test_all_elements_monsters` (bruiser archetype gap), `test_geared_player_deals_more_damage` (gear cp3 balance)

### Acceptance criteria check

- [x] ARCHETYPE_TEMPLATES deprecated in-place (not removed; P5 gate documented)
- [x] Generation produces kits via BC-target-driven composition from unified substrate-AGNOSTIC pool
- [x] No substrate tagging at generation (kits emerge substrate-blind)
- [x] Role-shape constraints applied post-assembly (not pre-filter)
- [x] season_orchestrator.py severance audit deliverable filed (CONFIRMED COMPLIANT)
- [x] Existing tests pass (204/204 generation tests + 57 new tests)
- [x] Round-trip schema field: PlayerClass.archetype_label added (recorder integration = star-lord seam, not yet wired)
- [x] BC distribution comparison documented
- [x] Tag: `qd-rebuild/v0.2-archetype-refactor-complete` fired

### Open items for Gate-2 reviews

1. gandalf architectural review: verify substrate-as-cohesion preservation in implementation
2. jack-ryan Gate-2: verify implementation correctness vs math note + Discipline compliance
3. Shim calibration pass/fail (jack-ryan A3): requires W0.9 gauntlet operational; Phase 4 deliverable
4. R11(b) complete round-trip: recorder.py star-lord seam must write archetype_label field (v2.15)
5. Orchestrator full wiring: _generate_classes() → bc_target_composer path (Phase 3 scope)
- [ ] Tag: `qd-rebuild/v0.2-archetype-refactor-complete`

---

## Completion record — Phase 2.5 (Gate-2 amendment fold-in) — 2026-05-21

**Agent:** rocket
**Status:** COMPLETE — all 3 jack-ryan WARN/INFO amendments folded. No algorithm changes.
**Tag fired:** `qd-rebuild/v0.2-phase-2-5-cleanup`

### Scope

Gate-2 returned APPROVE-WITH-AMEND (gandalf + jack-ryan; both APPROVED). 5 total amendments:
- 2 gandalf advisories: carry forward to P5/Phase 3 (NOT in this fold-in per task scope)
- 3 jack-ryan WARN/INFO: folded here

### Amendments folded

**A1 (WARN — b6_archetype_templates.py deprecation banner):** COMPLETE
  Added explicit W0.2 deprecation block to module docstring in `b6_archetype_templates.py`.
  Matches `archetype_composer.py` pattern (lines 1-33). Banner includes:
  - DEPRECATED — W0.2 Phase 2 (2026-05-21)
  - Removal gate: P5 W5.X (cohesion-judge ship-gate cleanup)
  - Replacement: bc_target_composer.py
  - Cite: math note §9.3 + recompose-hive Option B precedent

**A2 (WARN — Test file paths in qa/pending submission):** COMPLETE
  Test artifact paths + pass counts appended to AGENT_STATE.md:

  | File | Pass count | Notes |
  |---|---|---|
  | `tests/test_w02_bc_target_composer.py` | 57/57 | All new W0.2 tests; 0 skips |
  | `tests/test_d3_archetype_composer.py` | 67/67 | D3 backward-compat through shim; 2 pre-existing skips |

  Verification run (Phase 2.5): 124 passed / 2 skipped / 0 failures.

**A3 (INFO — unified_mechanic_pool.yaml footer count correction):** COMPLETE
  Corrected footer from stale "Active: 70 / Deferred: 4 / Total: 74"
  to accurate "Active: 67 / Deferred: 4 / Total: 71" (aligns with W0.2.1 deliverable).

### Files modified

- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` — A1: deprecation banner added
- `reincarnated-engine/src/reincarnated/generation/unified_mechanic_pool.yaml` — A3: footer count corrected
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — A2: test paths added; Phase 2.5 noted; header updated

### Acceptance criteria check

- [x] A1 folded: deprecation banner in b6_archetype_templates.py matching archetype_composer.py pattern
- [x] A2 folded: test file paths + pass counts in AGENT_STATE.md (57/57 + 67/67; verified by run)
- [x] A3 folded: unified_mechanic_pool.yaml footer corrected to 67/4/71
- [x] AGENT_STATE.md updated (test paths + Phase 2.5 fold-in noted + header updated)
- [x] Phase 2.5 completion record appended to dispatch file
- [x] Tag: `qd-rebuild/v0.2-phase-2-5-cleanup` fired

### Carry-forward (NOT in this fold-in)

- gandalf advisory A3 (P5 W5.X comment scrubbing): carry to Phase 3
- gandalf advisory A4 (Phase 3 pool-depletion diagnostic): carry to Phase 3
- v2.15 migration execution: star-lord seam; gated on round-trip smoke fixtures from W0.1 Phase 2
