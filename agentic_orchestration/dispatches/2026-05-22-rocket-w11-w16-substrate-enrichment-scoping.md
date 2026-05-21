# Dispatch — rocket: P1 W1.1-W1.6 Substrate Enrichment Scoping + W1.15-LITE Spec-Pickup

**Date:** 2026-05-22
**Author:** knight-rider
**Recipient:** rocket (engine generation seam owner)
**Authority:** Matt 2026-05-22 (prolonged-autonomy mission; pre-authorized P1 work; LITE path canonical)
**Priority:** HIGH (load-bearing for P1 critical path; required regardless of W1.13 final disposition)
**Estimated effort:** 1-2 weeks scoping + math-before-code; implementation begins next session
**Fire condition:** P0 milestone tag fired (gated on LC-011 ablation recovery + critique-pair disposition); can begin scoping now in parallel

---

## 0. TL;DR

P1 opens once P0 closes (recovery + critique-pair disposition). When that lands, rocket's first work-package is **substrate enrichment scoping** for W1.1-W1.6 + W1.11 + W1.15-LITE per math note v1.1 + gandalf-authored gear-archetype rule-table v1.

This dispatch is **scoping-only** — math-before-code per Discipline #1. Implementation follows in subsequent dispatches after jack-ryan Gate-1 approves the math notes.

**Six discrete scoping deliverables** (independent; can be sequenced however serves your craft):

| ID | Workstream | Math-before-code output | Effort |
|---|---|---|---|
| W1.1 | Ability schema extensions | v1.1 fields spec (node_type, cost, cooldown_seconds, playable_at_level_1, interaction_metadata, keystone_effect, BC-axis-contribution tags) | 1-2 days |
| W1.2 | HP-economy substrate creation | Template catalogue spec (~25 templates) + BC-axis coverage map | 2-3 days |
| W1.3 | Damage-taken-converts substrate | Template catalogue spec (~25 templates) + BC-axis coverage | 2-3 days |
| W1.4 | Charge-stack substrate | Template catalogue spec (~25 templates) + BC-axis coverage | 2-3 days |
| W1.5 | Movement-skill substrate expansion | Template catalogue spec (~30 templates) + BC-axis coverage | 2-3 days |
| W1.6 | Player-side proxy substrate | Template catalogue spec (~25 templates) + BC-axis coverage | 2-3 days |
| W1.11 | Element-specific enrichment | Per-element substrate parity audit + enrichment spec (uniform comprehensive depth per Track C verdict) | 3-5 days |
| W1.15-LITE | signature_gear_archetype derivation | Implementation spec from gandalf rule-table v1 (canonical/story/gear-archetype-rule-table-v1-2026-05-22.md) | 1 day spec; 3-5 days implementation |

Total scoping effort: ~2-3 weeks. Implementation effort (post Gate-1): ~3-5 weeks. P1 total per math note v1.1 estimate: 4-6 weeks.

---

## 1. Why this is load-bearing for P1

P1 substrate enrichment is the **precondition for W1.13** under any disposition (β rescope or α deprecation). Even if W1.13 deprecates, the substrate enrichment is required for:

- Profile A's archive depth target (per math note v1.1 § 8.3.1; ~168+ unique skill templates per season)
- 7 BC axes meeting 5× sufficiency rule (per legolas Phase 1 audit)
- The 8-axis BC archive's structural integrity at the post-W1 boundary
- Tier 4 keystone authorship's substrate space (per BDI rank-3 framing)
- Cohesion-judge's substrate-recognition signal at production scale (probe at 4.35 was at TRANSITIONAL substrate state; production needs full enrichment)

**Substrate enrichment is unconditionally load-bearing**; W1.13 disposition is conditional on top of it.

---

## 2. Authoritative inputs (read first)

Per Discipline #1 (math-before-code), rocket reads these before authoring any math note:

1. `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 — math note (especially § 3.6 schema fields, § 8.3.1 substrate-availability framing)
2. `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/` — legolas Phase 1 audit (gap identification per BC axis)
3. `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` — Track C verdict (uniform-depth comprehensive enrichment per W1.11)
4. `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate identity framework + § 2.1 element-trade-off thesis
5. `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` — gandalf rule-table v1 (when committed; pre-condition for W1.15-LITE)
6. `canonical/story/build-defining-resonance-formula-2026-05-21.md` — BDI formalism (informs substrate-richness target for rank-3 depth)
7. `~/Games/reincarnated-engine/src/reincarnated/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE canonical (W1.15-LITE input verification)

---

## 3. Math-before-code requirements per workstream

### W1.1 — Ability schema extensions

Math note must specify:
- Field additions (node_type enum, cost, cooldown_seconds, playable_at_level_1 invariant, interaction_metadata structure, keystone_effect structure, per-axis BC-contribution float vector)
- Schema migration plan (existing skills + new fields default values)
- Tier 1 playability invariant enforcement (per math note v1.1 § 3.3)
- Telemetry impact (new fields persistent to telemetry.db)
- Cross-seam impact (MIGRATION.md required for star-lord / drax consumers)

### W1.2-W1.6 — Substrate creation workstreams

Each math note must specify:
- Template catalogue scope (~25-30 templates per substrate, per gandalf review)
- BC-axis coverage map (which axes each template populates; targeting 5× sufficiency)
- Per-element distribution (uniform comprehensive depth per Track C verdict)
- Sim-viability verification plan (each template generates valid kits in spatial gauntlet)
- Foundation library integration plan

### W1.11 — Element-specific enrichment

Math note must specify:
- Per-element substrate parity audit (current state per legolas Phase 1)
- Enrichment targets per element (closing gaps to uniform depth)
- Cross-element BC-axis coverage validation
- Integration with W1.2-W1.6 (substrate creations enriched per-element)

### W1.15-LITE — signature_gear_archetype derivation

Math note must specify:
- Function signature: `signature_gear_archetype(dominant_element, role_orientation, range_profile, stat_distribution_signature) → gear_archetype`
- Rule-table consumption (from gandalf-authored v1 doc)
- Telemetry column addition (per-class persistence)
- Sim-viability verification for each archetype in rule-table value-set
- Cross-seam: gear-archetype field becomes available to demo (Pixi.js) + Unity + loadout (React) per gear-as-substrate LITE
- Implementation effort: 3-5 days (per gear-as-substrate § 0.5.6 + protocol amendments § 2.3)

---

## 4. Critique-pair structure

Per math note v1.1 § 9.4 canonical pattern:

- **gandalf reviews architectural alignment** (Gate-1) — substrate-as-cohesion preservation; BDI rank-3 substrate-richness target met; gear-archetype rule-table consumption correct; Tier 1 playability invariant enforced
- **jack-ryan reviews implementation correctness** (Gate-1) — schema extension correctness; cross-seam impact captured (MIGRATION.md per ADR-004); Discipline #11 cold-start measurement plans clean; Discipline #13a drift detection plans clean

Each math note routes through both gates before implementation begins.

---

## 5. Out of scope

- **Implementation work** (separate dispatches per workstream after Gate-1 approves each math note)
- **W1.13 multi-dim convergence implementation** (still fire-gated; critique-pair will disposition rescope; this dispatch only delivers the substrate-enrichment precondition)
- **W0.4 gear-affix architecture audit** (separate W0.4 dispatch; not in this work-package)
- **B6 skill tree UI scoping** (drax/canonical-32 work; not engine-side)
- **BDI hypothesis test infrastructure** (rocket-adjacent; separate dispatch)

---

## 6. Cross-seam coordination

W1.1's schema extensions trigger MIGRATION.md authoring (per ADR-004) for:
- **star-lord** — telemetry recorder + export pipelines consume new fields
- **drax** — demo + loadout consume `signature_gear_archetype` (W1.15-LITE; cross-seam from class generation to player surfaces)

Rocket flags cross-seam impacts in each math note's "Cross-seam impact" section. Knight-rider relays for MIGRATION.md authoring coordination.

---

## 7. Timing

- **Earliest fire (scoping):** parallel to P0 close (now; no fire-gate)
- **Earliest fire (implementation):** post Gate-1 approval of each math note + post P0 milestone tag
- **Duration (scoping):** 2-3 weeks
- **Duration (implementation):** 3-5 weeks
- **Total P1 substrate enrichment:** 4-6 weeks (per math note v1.1 estimate)

---

## 8. Cross-references

- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/`
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md`
- `canonical/story/build-defining-resonance-formula-2026-05-21.md`
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` (when committed by gandalf)
- `agentic_orchestration/dispatches/2026-05-22-critique-pair-post-recovery-w07-gate2-w113-rescope-p0-close.md` — P0→P1 transition gate
- `agentic_orchestration/dispatches/2026-05-22-gandalf-protocol-v13-foldin-plus-BDI-B-plus-G1-LITE-plus-T4-A.md` — gandalf parallel work-package
- `agentic_orchestration/dispatches/2026-05-21-rocket-w0-2-archetype-template-path-a-refactor.md` — W0.2 predecessor (substrate-agnostic generation function; foundation for W1.x enrichment)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #1 (math-before-code; this work instantiates); #11 (empirical inspection); #13a (drift detection)

---

**Signed:** knight-rider (orchestrator under prolonged-autonomy mandate)
**For:** P1 substrate enrichment scoping work-package; load-bearing precondition for W1.13 and Profile A archive depth regardless of W1.13 final disposition.
