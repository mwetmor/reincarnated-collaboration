# Dispatch — 2026-05-19 — rocket + gamora — VS2a S2 B6 main work (class kit composition + hierarchical skill tree)

**From:** knight-rider
**To:** rocket (generation seam — pre-work + tree-structure generator OWNER) + gamora (simulation seam — tree-aware convergence + per-tier validation OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when F2 lands + rocket pre-work complete + S1 partial progress (or S1 complete depending on F2 path)
**Estimated effort:** ~1–2 weeks engine (tree structure generator + tree-aware convergence + per-tier validation) + drax consumer wiring (F4 UI surface; separately tracked)
**Acceptance:** Per § Acceptance below + B6 design criteria per `canonical/28-engine-arpg-rebalance-design.md`. Tag fires: `vs2a/v0.8-b6-main-work-complete`.
**Hive context:** VS2a hive ACTIVE; F2 (kit-redesign approach) + rocket pre-work (energy-type-aware tier assignment) + F1 (`geometry_type` schema field) + S1 partial progress are upstream context. F4 (drax skill-tree UI surface) consumes S2 data contract.

---

## Context

Per `canonical/28-engine-arpg-rebalance-design.md` B6 EXTENSION (hierarchical skill tree with dimensional threading; added 2026-05-11):

- Each class kit generates as TREE structure (not flat skill list)
- Tree structure encodes archetype identity through multiple dimensions: mathematical (power tiers + rank thresholds), geometric (parent-child unlocks), thematic (chains), color (chain palettes), power curves (tier-specific coefficients)
- 4 tiers (vertical / power axis)
- Per-skill metadata: `tier` (1–4), `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`
- Tree validation: chain structure consistent; per-chain tier coverage; aggregate kit-size in 10–15 target
- Co-designed with B10 (gauntlet structure) + B7 (gear variance check)

**F2 interaction (per scope-of-work-vs2a § 2.3):** If F2 chooses path (a) hand-redesign, S2 proceeds as currently scoped under rocket pre-work + gamora main work. If F2 chooses path (b) R8-inversion, B6 main work may shape differently — skill tree emerges from converged class composition rather than authored as constraint-input. **S2 dispatch covers both interpretations.**

**Rocket pre-work** (energy-type-aware tier assignment) shipped earlier per `scope-of-work-vs2a.md` § 2.3 "pre-work dispatch authored." This dispatch picks up from rocket pre-work completion.

---

## Required reading

In order:
1. `canonical/28-engine-arpg-rebalance-design.md` B6 EXTENSION (full section)
2. `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` (F2 disposition; reshapes S2 if path (b))
3. F1 dispatch + completion record (`geometry_type` schema)
4. S1 dispatch + completion record (kit-redesign branch outcomes — feeds class composition into tree structure)
5. F4 dispatch + drax design dispatch (`agentic_orchestration/dispatches/2026-05-19-drax-b6-skilltree-ui-decomposition-design.md` once authored) — particularly § 7 data contract for skill-tree rendering
6. Rocket pre-work dispatch + completion record (energy-type-aware tier assignment; shipped earlier)
7. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` + `simulation/AGENT_STATE.md`
8. `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.3 (S2)
9. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Rocket scope (tree structure generator)

- [ ] Generator extension: emit class kits as TREE structure with per-skill metadata fields (`tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`)
- [ ] Class element distribution determination → locks cross-chain unlock rule
- [ ] Chain count + depths per archetype (variance allowed; novel archetypes emerge)
- [ ] Tree validation logic (chain structure consistent; per-chain tier coverage; aggregate kit-size 10–15)
- [ ] Schema migration: skill JSON schema extends with new fields (additive)
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
- [ ] **§ 7 data contract** (from F4 drax design dispatch) honored — tree structure surfaces fields drax UI needs
- [ ] `geometry_type` (F1) preserved on tree-skill nodes
- [ ] AGENT_STATE.md updated

### Gamora scope (tree-aware convergence + per-tier validation)

- [ ] Balance loop extended: per-tier coefficient validation; tree-aware convergence (tier-specific power curves; per-chain coverage in convergence run)
- [ ] Per-tier validation pass: each tier's expected DPS/burst/sustain/AOE coefficient honored
- [ ] R1 sprint re-run consumer (post-S1): tree-structured catalogue's per-tier WR partition validated
- [ ] Telemetry surface: per-tier convergence metrics captured (star-lord coordination if needed)
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- [ ] AGENT_STATE.md updated

### Joint scope

- [ ] B6 criteria per `canonical/28` met: tree-structure validation; per-chain tier coverage; aggregate kit-size 10–15; archetype identity encoded through dimensions
- [ ] Cross-seam fixture: rocket generator emits tree → schema validator accepts → gamora simulator consumes tree-aware → telemetry captures per-tier coverage → star-lord export → drax (F4 UI) renders. Field-presence + integrity checks at each boundary.
- [ ] Hypothesis test per `canonical/28` B6 criteria (kit-size target 10–15; chain coverage; tier coefficients)
- [ ] Tag fire request: `vs2a/v0.8-b6-main-work-complete`

---

## Cross-seam contract change? (Principle 6 gate)

**YES — joint cross-seam contract change.** Skill JSON schema extends additively; balance loop extends; telemetry extends; UI consumer reads new contract.

**MIGRATION.md REQUIRED at both seams:**
- `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (rocket; tree fields)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (gamora; tree-aware convergence)
- `reincarnated-demo/MIGRATION.md` (drax appends if F4 UI consumes; coordinated)

**Round-trip smoke REQUIRED.** End-to-end: generator emits tree → validator → simulator consumes → telemetry → export → drax UI render. Field-presence at each boundary.

---

## Acceptance criteria

- [ ] Rocket: generator emits tree-structured skill catalogue; schema additive; tree-validation operational
- [ ] Gamora: balance loop extended; per-tier convergence operational; per-tier validation pass GREEN on at least 1 representative class
- [ ] Joint: cross-seam round-trip smoke GREEN
- [ ] MIGRATION.md at generation + sim + demo (if F4 consumes)
- [ ] B6 hypothesis test per `canonical/28` criteria passes (kit-size 10–15; chain coverage; tier coefficients)
- [ ] AGENT_STATE.md updated both seams
- [ ] Hive log: STATE on start each seam + HANDOFF on rocket → gamora handoff + HANDOFF on gamora → telemetry → drax + completion STATE
- [ ] Tag: `vs2a/v0.8-b6-main-work-complete`

---

## Out of scope

- F4 drax UI surface (separate dispatch; consumes S2 contract)
- S1 kit-redesign sprint (separate; upstream)
- B10 V2 sequential-room semantics (in-flight gamora work per AGENT_STATE; not gating S2)
- B7 gear-variance check (post-S2; separate workstream — file 28 co-design)
- Per-class hand-tuning beyond per-tier convergence (S1 territory)
- B6 design spec amendments (gandalf if surface needed; not S2 implementation scope)

---

## Open questions for the agents

- **Tree visualization data shape per F4 § 7 contract** — L1 rocket; rocket reads drax's F4 design dispatch + adapts tree-structure emission to match the data contract drax surfaces
- **Per-tier coefficient calibration** — L1 gamora per B6 criteria; if balance loop convergence reveals tier coefficients are unstable, surface to gandalf for spec amendment via hive log
- **Chain count + depth per archetype** — L1 rocket per `canonical/28` "variance allowed; novel archetypes emerge"; rocket decides per archetype + may amend in F2 path (b) regeneration if emergent shapes differ
- **Cross-chain unlock rule for multi-element classes** — L1 rocket per `canonical/28` "Determine class element distribution (single vs multi) → locks cross-chain unlock rule"
- **F2 path (b) interaction** — if F2 chose R8-inversion, S2 main work consumes the regenerated catalogue (tree structure may emerge differently); coordinate with rocket S1 work. If F2 chose path (a), S2 proceeds against hand-redesigned catalogue
- **B7 gear-variance interaction** — B7 is downstream per file 28 co-design; surface to knight-rider if B7 work surfaces during S2 (likely VS2b territory)

---

## References

- `canonical/28-engine-arpg-rebalance-design.md` B6 EXTENSION
- `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` (F2)
- F1 dispatch + S1 dispatch + F4 design dispatch (sibling VS2a docs)
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` + rocket pre-work completion
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.3 (S2)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** F2 disposition landed + rocket pre-work complete + F1 schema field operational + S1 partial progress (at minimum first batch landed; full S1 not required for S2 to start in path (a); in path (b) S1 + S2 may collapse).

**Post-activation:** rocket + gamora L1 within seams; gandalf L2 consult on B6 criteria interpretation. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. S2 builds the tree. The catalogue becomes hierarchical; the player gets an unlock structure; drax has a surface to render.*
