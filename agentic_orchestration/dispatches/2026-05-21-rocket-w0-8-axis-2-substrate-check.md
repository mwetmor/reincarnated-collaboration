# Dispatch — 2026-05-21 — rocket — W0.8: Axis 2 (damage geometry) substrate completeness check

**From:** knight-rider
**To:** rocket
**Approved by:** gandalf attestation 2026-05-21 § 5 (six autonomous workstreams cleared); Matt activation dispatch § 4 Step 4 W0.8 listed in P0 roster
**Status:** PENDING — ACTIVE (rocket may execute when launched)
**Estimated effort:** ~2-3 hours (Discipline #11.1 — empirical inspection of substrate state; analytical mapping; not implementation)
**Acceptance:** Per-bin gap list documented; feeds P1 W1.5/W1.7 substrate enrichment scope; intermediate tag `qd-rebuild/v0.8-axis-2-substrate-check`.

---

## Context

Per activation dispatch § 2.3 and protocol § 6.1.2 W0.8: front-load the geometry-question for Axis 2 so P1 substrate enrichment knows what to expand. Legolas Phase 1 finding: chain bin "thin"; multi-spawn bin "thin" — but the exact per-bin gap to the 5× rule isn't yet quantified.

**The 5× rule** (substrate sufficiency; legolas audit framing): each axis must have ≥5× bin count distinguishable substrate templates. For Axis 2 (5 bins: single-target / small-AOE / large-AOE / chain / multi-spawn), the target is ~25 distinguishable templates per bin. Current estimate: ~18-20 total across all 5 bins.

**Why now:** before P1 substrate creation work fires (P1 W1.2/W1.3/W1.4/W1.5/W1.6), we need an empirical map of the gap. This dispatch produces that map — substrate-AGNOSTIC under the substrate-as-cohesion-only architectural recommitment (no per-substrate weighting; uniform across all 7 elements per Track C verdict).

## What this dispatch does

### Step 0 — Read the spec

- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` Axis 2 spec (5 bins; substrate flags; sim deferral matrix)
- `canonical/09-mechanical-form-palette-locked.md` (or equivalent — the 16-type canonical palette per memory `project_geometry_palette.md`)
- Legolas Phase 1 finding: `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/internal-substrate-state.md`

### Step 1 — Map the 16-type palette to Axis 2's 5 bins

Produce a mapping table:

| Canonical-09 form type | Axis 2 bin | Notes |
|---|---|---|
| (e.g., "projectile") | single-target | direct hit applies damage to one entity |
| (e.g., "rectangle_aoe") | small-AOE | radius < threshold |
| ... | ... | ... |

Note: under substrate-as-cohesion-only, the mapping is substrate-AGNOSTIC (no per-element weighting). The 16 types are mechanical-shape descriptors that all elements can express.

### Step 2 — Count distinguishable templates per bin

For each Axis 2 bin, count distinguishable templates available in the current generation pool:
- Pull from `b6_archetype_templates.py` (archetype-skill mappings) — note: this pool is being refactored under W0.2; the count here reflects PRE-W0.2 state
- Cross-check with canonical library (`canonical/library/` if equivalent location exists)
- Mark distinguishability by mechanic difference (chain bounce-count differences, AOE radius differences, multi-spawn proxy-count differences, etc.)

### Step 3 — Compute per-bin gap to 5× rule

| Axis 2 bin | Current distinguishable templates | 5× target | Gap | Priority |
|---|---|---|---|---|
| single-target | ? | ~25 | ? | ? |
| small-AOE | ? | ~25 | ? | ? |
| large-AOE | ? | ~25 | ? | ? |
| chain | ? (legolas: "thin") | ~25 | ? | HIGH (legolas finding) |
| multi-spawn | ? (legolas: "thin") | ~25 | ? | HIGH (legolas finding) |

### Step 4 — Author per-bin enrichment seed list

For HIGH-priority bins (chain + multi-spawn at minimum), seed a list of candidate template additions that P1 W1.5 (movement-skill expansion) and P1 W1.7 (legolas Phase 2 depth pass) consume. Each candidate: brief description (1-2 sentences), substrate-AGNOSTIC under substrate-as-cohesion, BC-axis contribution tags (per § 2.8 of activation dispatch).

### Step 5 — File deliverable

Deliverable file: `agentic_orchestration/rocket/research/qd-rebuild-w0-8-axis-2-substrate-check.md` (under your rocket research dir per agent topology). Cross-link to per-substrate analysis from Track C synthesis.

### Step 6 — Tag

Intermediate tag: `qd-rebuild/v0.8-axis-2-substrate-check`. Knight-rider folds the deliverable into state-of-hive doc § 1 W0.8 row + P1 W1.X scope-finalization.

## Required reading before starting

- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (Axis 2 spec)
- `canonical/story/substrate-design-supplement-2026-05-21.md` (substrate-as-cohesion-only — operative principle for "substrate-AGNOSTIC")
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` (uniform-depth enrichment confirmed; OQ-7 water DPS density flag for downstream)
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/internal-substrate-state.md` (chain "thin"; multi-spawn "thin" findings)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/MEMORY.md` linked memory `project_geometry_palette.md` (16-type active palette)

## Math-before-code (if applicable)

Not applicable — this dispatch produces an analytical mapping + gap list, not new code or math derivation. The 5× rule is the established target.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — analytical workstream; no field add/modify/rename/remove. The deliverable is a markdown gap analysis feeding P1 scoping; no cross-seam contracts touched.**

## Scope

- [ ] 16-type palette mapped to 5-bin Axis 2 spec
- [ ] Per-bin distinguishable-template count documented
- [ ] Gap-to-5×-rule quantified per bin
- [ ] HIGH-priority enrichment seed list authored (chain + multi-spawn minimum)
- [ ] Deliverable filed at `agentic_orchestration/rocket/research/qd-rebuild-w0-8-axis-2-substrate-check.md`
- [ ] Intermediate tag fired (`qd-rebuild/v0.8-axis-2-substrate-check`)

## Acceptance criteria

- [ ] Mapping table covers all 16 canonical-09 form types → one of 5 Axis 2 bins
- [ ] Per-bin count is empirically grounded (not estimated) — cite source files
- [ ] Gap list explicit per bin (e.g., "chain: 3 current; ~25 target; gap ~22; HIGH priority")
- [ ] Seed list for chain + multi-spawn contains ≥10 candidate templates each (or document why fewer)
- [ ] Round-trip: not applicable — analytical-only workstream

## Out of scope

- Implementing any new templates (P1 W1.5 + W1.7 territory)
- Per-substrate weighting (Track C verdict: uniform-depth; no differentiation)
- Mapping decisions for Axis 2A (proxy density) — that's separately deferred per BC axes lock § 5
- Vision-layer geometry gaps (Blessed Hammer / Storm Brand / etc.) — per D6, documented for v1.1; do not block this dispatch

## Open questions for the agent to resolve

- Per the 16-type palette, are there any form types that span multiple Axis 2 bins (e.g., "small-AOE → chain at modifier > X")? Document handling — propose: count under the dominant bin per damage-weighted argmax intent (matches Axis 2 measurement spec per D4)
- For "multi-spawn" bin specifically: distinguish proxy entities (Axis 2A territory) from multi-spawn projectiles/AOE clouds (Axis 2 territory)
- For "chain" bin: are chain-bounce-count differences (3 bounces vs 8 bounces) distinguishable templates, or one template parameterized? Document your interpretation; uniform across mapping

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.3 (W0.8 framing) + § 4 Step 4 W0.8
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.8 + § 6.2.2 W1.5 + W1.7 (downstream consumers)
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/` (full Phase 1 deliverables)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` (uniform-depth + OQ-7 water DPS density)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (state-space conditioning)

---

## Completion record

**Completed by:** rocket
**Date:** 2026-05-21
**Tag fired:** `qd-rebuild/v0.8-axis-2-substrate-check`
**Deliverable:** `agentic_orchestration/rocket/research/qd-rebuild-w0-8-axis-2-substrate-check.md`

### Scope checklist

- [x] 16-type palette (28 in VALID_GEOMETRIES) mapped to 5-bin Axis 2 spec — full mapping table in deliverable § 2
- [x] Per-bin distinguishable-template count documented — empirically grounded, sources cited in § 4
- [x] Gap-to-5×-rule quantified per bin — explicit per-bin table in § 5
- [x] HIGH-priority enrichment seed list authored — chain: 12 candidates (§ 6); multi-spawn: 12 candidates (§ 7)
- [x] OQ-7 water DPS density folded in — § 8 with specific instantaneous-burst template recommendations
- [x] Structural metadata gaps flagged — § 11 includes `bounce_count` and `spawn_count` as new fields needed beyond legolas's existing list
- [x] Intermediate tag fired

### Key findings for knight-rider / hive state doc

1. **Palette count:** VALID_GEOMETRIES has 28 entries in current engine state (canonical-09 final table says 26 due to counting methodology differences; code is authoritative).
2. **Aggregate gap:** ~58-64 distinguishable templates currently across all 5 bins vs ~125 target. At ~49-52% of target overall.
3. **Chain bin:** ~3-4 distinguishable templates vs ~25 target; gap ~21-22. No `bounce_count` parameter exists; no `is_chain` schema field. 2 geometry types only.
4. **Multi-spawn bin:** ~5-6 distinguishable templates vs ~25 target; gap ~19-20. No `spawn_count` parameter; no `is_multi_spawn` schema field. 2 geometry types only.
5. **Small-AOE bin:** near-target (~20-22); lowest priority for enrichment; richest bin with 11 geometry types.
6. **New schema fields recommended:** add `bounce_count` (chain geometries) and `spawn_count` (multi-spawn geometries) to Ability schema alongside the 3 fields legolas already identified (`aoe_radius`, `is_chain`, `is_multi_spawn`).
7. **OQ-7 water DPS disposition:** water's sustained-zone geometry preference (large-AOE dominant) is the structural cause of elevated modifier requirements. Instantaneous-burst multi-spawn (M-3, M-8) and short-chain (C-4) templates are the recommended enrichment targets for water-cohesion balance.

### Scope-creep / structural flags for knight-rider

None. No ambiguities required escalation. Multi-bin edge cases (leap_strike, cone, aura) resolved via damage-weighted argmax interpretation per dispatch instructions. Proxy entity vs multi-spawn scoping (totem = multi-spawn; summon_combatant = Axis 2A deferred) applied cleanly.
