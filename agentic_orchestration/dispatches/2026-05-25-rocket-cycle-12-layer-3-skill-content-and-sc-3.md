# Dispatch — 2026-05-25 — rocket — Cycle 12 Layer 3 skill content + SC-3 off-hand mechanical contract

**From:** knight-rider
**To:** rocket (generation seam — engine content-generation owner)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — Q4 Option B parallel-after-Gate-1 + Q5 SC-3 absorbed into Layer 3; KR autonomously orchestrates Layer 3 dispatch authoring per scope-doc § 1)
**Estimated effort:** ~2-3 weeks rocket (parallel with Layer 2)
**Acceptance:** Skill tree topology generator + node anatomy generator + T4 candidate slot generator per framing brief § 4 contract; ~130 substrate templates per L8 P1 enrichment items shipped (W1.1-W1.6 + W1.11); SC-3 off-hand mechanical contract designed + implemented; jack-ryan Gate-2 PASS

---

## Context

Cycle 12 (full new engine parallel-build per Option γ) opens with rocket parallel-firing Layer 2 (kit identity — separate dispatch) and Layer 3 (skill content) per framing brief § 8 + scope-doc § 1. **Layer 3 produces the skill content** — `SkillTree` + `Skill` + `SkillChain` instances per framing brief § 4 contract, plus the ~130 substrate templates per L8 P1 enrichment items, plus the SC-3 off-hand mechanical contract design (absorbed per Q5 ratification).

**All 5 pre-Layer-2/3 gate prereqs ✅ CLEARED** (jack-ryan Gate-1; legolas MC-1; legolas MC-2; gandalf comp-policy § 4; elrond pre-Layer-2 prep) — see Layer 2 dispatch + Cycle 12 state file Wave 0/0.5 for closeouts.

Layer 3 consumes the PlayerClass shape Layer 2 emits (per framing brief § 4 contract). Both layers compose against the LOCKED interface contract; Layer 3 stub on Layer-2-populated fields (`bc_target_cell`, `element`, `energy_type`, `mechanical_substrate_triple`, etc.) until Layer 2's actual implementation lands; Layer 3 emits skill_tree + t4_candidates that Layer 4 (later) + Layer 6 (later) consume.

Fires in PARALLEL with Layer 2 dispatch (same rocket seam — independent sub-agent instances; coordinated via LOCKED § 4 contract).

---

## Required reading before starting

### Authority-of-record (LOCKED canon)

- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** — § 4 SkillTree + Skill + SkillChain + T4Slot + T4Candidate + T4Alteration contracts (LOCKED) + § 2 (Layer 3 scope) + § L1 (BDI math model — context for `bc_axis_contribution` per-node weighting)
- **`agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`** — § 1 + § 5 + § 6
- **`canonical/story/skill-system-2026-05-24.md`** — primary load-bearing reference (10-15 node skill tree architecture; § 2 chain hierarchy; § 8 Algorithm § 8 architecture; § 9 spirit-guide explainer pattern; § 12 cohesion-judge naming; § 13 substrate-AGNOSTIC Phase 2)
- **`canonical/story/tier-4-architecture-defaults-2026-05-22.md`** — T4-A architecture (T4Candidate + T4Slot + T4Alteration shape; per-chain T4 slot structure; 1 signature + 1-3 secondary capstones; max arity ≤ 5-6 derivable from chain hierarchy)
- **`canonical/story/off-hand-items-2026-05-24.md`** — Main/Secondary architecture (primary load-bearing for SC-3 off-hand mechanical contract design); § 2.3 mechanical contract layer (off_hand_buff_geometry; off_hand_aura_tempo; etc.)
- **`canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`** v1.1 — math note for `bc_axis_contribution` per-node weighting (§ 3.6 axis-id vocabulary: axis_1_engagement, axis_2_geometry, axis_2A_proxy, axis_2B_control, axis_3A_tempo, axis_3B_variance, axis_4_defensive, axis_5_economy; § 4.2-4.3 Layer 4 multi-tier voting consumes bc_axis_contribution as dict)
- **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`** § 3 (Option α/β/C; relevant for SC-3 off-hand routing) + § 5 (per-cell coverage)
- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** — 8 BC axes vocabulary

### W1.13 dispatch substrate enrichment items + invariants

- **`agentic_orchestration/dispatches/2026-05-21-rocket-w1-13-skill-tree-node-population.md`** § 2.1 (P1 substrate enrichment items source list) + § 3.1 (skill content invariants — primary load-bearing for Layer 3 invariant enforcement):
  - W1.1 Ability schema extensions
  - W1.2 HP-economy substrate (~25 templates)
  - W1.3 damage-taken-converts substrate (~25 templates)
  - W1.4 charge-stack substrate (~25 templates)
  - W1.5 Movement-skill variety expansion (~30 templates)
  - W1.6 Player-side proxy substrate (~25 templates)
  - W1.11 Element-specific substrate enrichment
  - Total: ~130 substrate templates
- W1.13 dispatch § 0.0 original FIRE-GATE is PROCEDURALLY CLOSED per Cycle 12 framing brief § 0 — multi-dim convergence (Layer 4) fires per Cycle 12 scope, not via the original dispatch. But § 2.1 substrate enrichment items + § 3.1 invariants remain canonical references for Layer 3 implementation

### Gate-1 amendments (REQUIRED at L3 dispatch consumption per jack-ryan finding)

- **`agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md`** — primary action items for L3:
  - **WARN-1**: `off_hand_item` field comment cites `SC-3 (Cycle 12); substrate per off-hand-items-2026-05-24.md` (NOT "Sidecar B" which is Cycle 10 closed work)
  - **WARN-3**: `bc_axis_contribution` is `dict[str, float]` keyed by axis ID per math note v1.1 § 3.6 (8 keys), NOT `list[float]`
  - **WARN-5**: `t4_candidates` max arity ≤ 5-6 (derivable from T4-A § 2: chain_count × 1 signature + up to 3 secondary across 2-4 chains); enforce per-chain slot structure

### Methodology + critique-pair inputs

- legolas MC-2 thin-cell-fallback cascade — same applies to skill content substrate if any L8 substrate template is thin
- gandalf comp-policy § 4 verdict — relevant for SC-3 off-hand routing if off-hand item substrate uses similar cell-routing structure

### Engineering-disciplines + cross-seam

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — load-bearing: #1 (math-before-code) + #2 (smoke-test) + #8 (schema validation) + #11 (empirical inspection) + #13a (implementation-vs-intent drift — for SC-3 framing) + #25 (semantic-layer rep-audit — confirm bc_axis_contribution is mechanical-layer per L9)
- `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (rocket seam state)
- ADR-004 MIGRATION.md cross-seam requirement (Layer 3 emits SkillTree shape; star-lord JSON serialization; loadout consumption)

---

## Math-before-code (per Discipline #1)

Author math-note at `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-3-skill-content-and-sc-3-2026-05-25.md` BEFORE implementation, covering:

### Math 1 — Skill tree topology (chain hierarchy)

- Per skill-system § 2: 2-4 chains per kit; 10-15 nodes total per tree
- Per W1.13 dispatch § 3.1: Tier 1 playability invariant (every chain's Tier 1 node is independently playable at L1; no cross-chain prereqs at Tier 1)
- Topology validity invariants: DAG structure within chain; no cycles; tier ordering (Tier 1 → Tier 2 → Tier 3 → Tier 4)
- Math-note enumerate per-archetype templates (2-4 chains per archetype; per-archetype cross_chain_rule if any per skill-system canon)

### Math 2 — Node anatomy + bc_axis_contribution

- Per Skill contract shape: tier (1-4), node_type (damage/control/defense/mobility/utility), cost, cooldown_seconds, playable_at_level_1: bool, interaction_metadata, keystone_effect (Optional[KeystoneEffect] for T4 slots)
- **bc_axis_contribution: dict[str, float]** per WARN-3 amendment — 8 keys per math note v1.1 § 3.6: axis_1_engagement, axis_2_geometry, axis_2A_proxy, axis_2B_control, axis_3A_tempo, axis_3B_variance, axis_4_defensive, axis_5_economy
- Math-note define per-node-type axis-contribution patterns (e.g., damage nodes contribute positive to axis_1 + axis_3A; defense nodes to axis_4; etc.)
- Per L9 semantic-layer rep-audit: bc_axis_contribution is mechanical-layer; node thematic text is semantic-layer (separate field)

### Math 3 — T4 candidate slot generator

- Per T4-A § 2: 1 signature + 1-3 secondary capstones per kit
- Per WARN-5 amendment: t4_candidates max arity ≤ 5-6 (chain_count × 1 signature + up to 3 secondary across chains)
- Per-chain T4 slot structure: each SkillChain.tier_4_slot is single T4Slot; cross-chain election (signature vs secondary) is per kit OR per chain — rocket judgment with math-note rationale per T4-A hierarchy
- T4Candidate shape: must reference an AlterationOutput strategy (per Cycle 11 § 8 6 strategies including DEFENSIVE_TRADEOFF); η-score from Layer 2's § 8 opportunity-scan computation
- Layer 3's job: generate T4 SLOTS + candidate AlterationOutput per chain; Layer 6 (later) picks the build-defining one + wires it

### Math 4 — Substrate template population (~130 templates per L8)

- W1.1 Ability schema extensions: extend Skill/T4Alteration shape for new substrate fields per W1.13 dispatch § 2.1
- W1.2 HP-economy substrate (~25 templates): nodes affecting HP-based mechanics (HP-as-resource; HP-trade; HP-regen; etc.)
- W1.3 damage-taken-converts substrate (~25 templates): conversion nodes
- W1.4 charge-stack substrate (~25 templates): charge-stack mechanics
- W1.5 Movement-skill variety expansion (~30 templates): movement node variety
- W1.6 Player-side proxy substrate (~25 templates): proxy mechanics (player-side; pre-§8.6 proxy-spawn deferral)
- W1.11 Element-specific substrate enrichment: element-keyed nodes (fire/water/earth/wind/lightning/etc.)
- Math-note enumerate each substrate template family + invariants + composition rules

### Math 5 — SC-3 off-hand mechanical contract design

- Per Q5 absorbed: SC-3 off-hand mechanical contract design (buff/aura/proxy effects for banner/focus/talisman/tome/horn) lives in Layer 3 dispatch
- Per off-hand-items-2026-05-24 § 2.3: mechanical contract layer (off_hand_buff_geometry; off_hand_aura_tempo; etc.)
- Define mechanical contract shape:
  - Banner: aura emission (geometry + tempo)
  - Focus: buff projection (target + magnitude)
  - Talisman: passive proxy effect (no active emission)
  - Tome: knowledge-based buff (intelligence-scaled)
  - Horn: tempo-altering effect (kit-wide tempo bonus)
- Per Gate-1 cross-cutting finding: verify SC-3 mechanical fields surface on or alongside `WeaponKnowledgeEntry` (the substrate row type for off-hand items)
- Math-note define per-off-hand-type contract; rocket may extend `weapon_sim_props` schema if needed (cross-seam impact — coordinate with star-lord)

---

## Cross-seam contract change? (Principle 6 gate)

**Yes.** Layer 3 generator EMITS SkillTree + Skill + SkillChain + T4Slot + T4Candidate + T4Alteration instances consumed by Layer 4 (later) + Layer 6 (later) + star-lord JSON export + loadout app. Also: SC-3 off-hand mechanical contract may extend `weapon_sim_props` schema.

**Round-trip smoke REQUIRED per Principle 6:**
- Layer 3 emits SkillTree (with skill_tree + t4_candidates + WARN-3 bc_axis_contribution dict + WARN-5 t4_candidates arity-bound)
- Star-lord serializes through JSON export
- Loadout app consumes back (drax T4StrategyType + T4AlterationOutput interfaces; spot-check whether existing types accommodate new fields; coordinate with drax via MIGRATION.md if drax-side schema change needed)
- Round-trip fixture should cover: a class with all chains populated; a class with 2 chains; a class with multiple T4 candidates; an off-hand item case

**MIGRATION.md REQUIRED per ADR-004:**
- Extend `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` with new section (probably alongside Layer 2's `§ v1.4`) — `§ v1.4 Cycle 12 Layer 3 SkillTree shape + SC-3 off-hand mechanical contract` or rocket naming judgment
- Document WARN-1 off_hand_item comment correction (SC-3 reference)
- Document WARN-3 bc_axis_contribution dict-keyed-by-axis-id shape change vs framing brief draft
- Document WARN-5 t4_candidates max arity ≤ 5-6
- Document SC-3 off-hand mechanical contract (banner/focus/talisman/tome/horn shapes) + any weapon_sim_props schema extension
- Document substrate-template families shipped (W1.1-W1.6 + W1.11)

---

## Scope (rocket Layer 3 skill content + SC-3 implementation)

### Gate-1 amendment integration (REQUIRED)

- **WARN-1 — off_hand_item comment:** PlayerClass.off_hand_item field comment must read "if applicable; mechanical contract per SC-3 (Cycle 12); substrate per off-hand-items-2026-05-24.md" (correct sidecar reference)
- **WARN-3 — bc_axis_contribution type:** Skill.bc_axis_contribution is `dict[str, float]` keyed by axis ID per math note v1.1 § 3.6 (8 keys); NOT `list[float]`. Layer 4 multi-tier voting walks the dict by axis ID per math note § 4.2-4.3
- **WARN-5 — t4_candidates max arity:** ≤ 5-6 per T4-A § 2 chain hierarchy (chain_count × 1 signature + up to 3 secondary across 2-4 chains); enforce as runtime invariant

### W1.13 § 3.1 invariant enforcement (REQUIRED)

- Tier 1 playability: every chain's Tier 1 node is independently playable at L1
- Substrate-agnostic generation: generator doesn't require substrate-specific knowledge to produce valid tree (substrate-binding happens via Layer 2)
- Tree topology validity: DAG within chain; no cycles; tier ordering

### Substrate template population (~130 templates per L8)

- W1.1 Ability schema extensions: implement
- W1.2 HP-economy substrate (~25 templates): implement
- W1.3 damage-taken-converts substrate (~25 templates): implement
- W1.4 charge-stack substrate (~25 templates): implement
- W1.5 Movement-skill variety expansion (~30 templates): implement
- W1.6 Player-side proxy substrate (~25 templates): implement
- W1.11 Element-specific substrate enrichment: implement
- All ~130 templates emit valid Skill/T4Alteration shape per § 4 contract

### SC-3 off-hand mechanical contract (absorbed per Q5)

- Design per Math 5 above + off-hand-items-2026-05-24 § 2.3
- Define mechanical contract for banner/focus/talisman/tome/horn
- If `weapon_sim_props` schema extension needed: coordinate with star-lord (cross-seam — MIGRATION.md flag; may require star-lord schema dispatch as follow-on; for v1, can keep in rocket-internal field set if no star-lord schema change is needed)
- Verify SC-3 mechanical fields surface on or alongside `WeaponKnowledgeEntry` per Gate-1 cross-cutting

### T4 candidate slot generator

- Per-chain T4 slot generation: each chain emits 1 T4Slot with N candidates (rocket judgment N=1-3 per chain)
- T4Candidate references AlterationOutput strategy per Cycle 11 § 8 (6 strategies; rocket consumes existing mechanic_alteration.py)
- Total t4_candidates per kit ≤ 5-6 per WARN-5
- Layer 6 (later) picks build-defining T4 + wires it; Layer 3 just generates candidates
- Note INFO-3 (Gate-1 deferred to L6): SkillTree may need `signature_chain_id: Optional[str]` field — Layer 3 can emit this as null at generation; Layer 6 sets it. OR rocket defers field addition to L6 dispatch (rocket judgment)

### Per-archetype templates

- Per skill-system canon + W1.13 § 3.1: per-archetype templates exist (mage / fighter / rogue / cleric / etc.)
- Each archetype template defines: chain count + per-chain node-type distribution + cross_chain_rule if any
- Rocket Layer 3 enumerates archetype templates + applies per kit per archetype assignment

### Smoke + acceptance gates

- **Smoke gate 1**: generator produces SkillTree for a representative PlayerClass stub; verify shape conforms to § 4 contract (with WARN-1/3/5 amendments)
- **Smoke gate 2**: 22 archetype templates produce valid SkillTrees (one per BC roster cell); Tier 1 playability + topology validity invariants PASS
- **Smoke gate 3 (substrate templates)**: ~130 substrate templates emit valid Skill/T4Alteration shape; round-trip JSON serialization PASS
- **Smoke gate 4 (SC-3 off-hand)**: 5 off-hand item types (banner/focus/talisman/tome/horn) emit valid mechanical contract per SC-3 design
- **Smoke gate 5 (round-trip)**: emit SkillTree → star-lord JSON serialize → loadout deserialize → field-presence + shape check
- **Smoke gate 6 (Layer 2 compose)**: SkillTree composes against PlayerClass stub emitted by Layer 2; Layer 4 consumer can walk SkillTree per math note v1.1 § 4.2-4.3

---

## Out of scope (explicit non-goals)

- Layer 2 BC-target subspace generator (separate dispatch fires in PARALLEL)
- Layer 4 multi-dim convergence (fires after L2+L3 lock; MC-3 consult gates L4; bc_axis_contribution dict consumed by L4 not implemented here)
- Layer 6 § 8 wire-up (fires after L4 lands; T4 candidate selection + alteration wiring is L6 not L3)
- Layer 7 BDI test framework (DEFERRED to v1.1 per scope-doc § 0)
- Star-lord schema changes beyond MIGRATION.md flag for SC-3 off-hand mechanical contract (if star-lord schema change needed, that's a star-lord seam dispatch; for v1, rocket may keep contract in rocket-internal field set)
- Loadout app changes (drax consumes new shape per MIGRATION.md; separate seam)
- T4-B v1 catalogue contents — parallel-track gandalf + Matt design call; Layer 3 generates T4 SLOTS but not the populated T4 catalogue entries
- Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn) — v1.1+ per Cycle 11 P2b
- Broader weapon-equip flexibility (L11 deferred) — v1.1+
- Cycle 11 substrate templates that were skipped (W1.7-W1.10 / W1.12 — out of L8 list)
- Architectural amendments to SkillTree / Skill / T4 contracts (LOCKED per framing brief § 4; escalate to gandalf via KR if rocket implementation surfaces contract gap per scope-doc § 5)

---

## Acceptance criteria

- [ ] Math-note authored at `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-3-skill-content-and-sc-3-2026-05-25.md` BEFORE implementation per Discipline #1
- [ ] SkillTree + Skill + SkillChain + T4Slot + T4Candidate + T4Alteration dataclasses implemented per § 4 contract + Gate-1 amendments (WARN-1 + WARN-3 + WARN-5)
- [ ] W1.13 § 3.1 invariants enforced (Tier 1 playability; substrate-agnostic generation; topology validity)
- [ ] ~130 substrate templates shipped per L8 P1 enrichment items (W1.1 + W1.2 + W1.3 + W1.4 + W1.5 + W1.6 + W1.11)
- [ ] SC-3 off-hand mechanical contract designed + implemented per Math 5 (banner/focus/talisman/tome/horn)
- [ ] Per-archetype templates implemented (2-4 chains per archetype + cross_chain_rule)
- [ ] T4 candidate slot generator implemented (1 signature + 1-3 secondary; max 5-6 per kit)
- [ ] Smoke gates 1-6 PASS per § Scope smoke section
- [ ] Round-trip smoke: SkillTree → JSON → consumer back PASS per Principle 6
- [ ] MIGRATION.md authored / extended per ADR-004
- [ ] No regression on existing engine code (regression suite PASS)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v0.1-cycle-12-layer-3-skill-content-and-sc-3-2026-05-25` (or per-sub-component intermediate tags per rocket discretion)

---

## Open questions for the agent to resolve

- Whether `SkillTree.signature_chain_id: Optional[str]` field should be added at Layer 3 (Gate-1 INFO-3 deferred to L6; rocket judgment on whether to add field now nullable OR defer to L6 dispatch)
- Whether SC-3 off-hand mechanical contract requires `weapon_sim_props` schema extension (cross-seam impact — coordinate with star-lord) OR can be implemented in rocket-internal field set for v1
- Whether T4Candidate η-score is computed at Layer 3 (rocket consumes existing mechanic_alteration.py opportunity_scan) OR Layer 6 (T4 candidate generation at L3; η-score computation at L6); recommend Layer 3 generates candidates + Layer 6 scores
- Whether ~130 substrate templates ship as a single sub-component commit OR per-template-family commits (W1.2 HP-economy commit, W1.3 damage-taken-converts commit, etc.); rocket discretion per per-item tag pattern
- Whether per-archetype templates are exhaustive at L3 (covering all 22 BC roster cells × any archetype variants) OR ship a subset for v1 with v1.1+ expansion queue (rocket judgment per substrate availability + effort budget)
- Whether SC-3 mechanical contract should differentiate between Sketch F substrate-missing items (Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh — Cycle 10 wind-down composition policy § 5.2) and stockable substrate items (rocket judgment; recommend treat uniformly per L11 strict 4-tuple)

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (contract LOCKED)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md` (Gate-1 7 WARN + 3 INFO; load-bearing for L3: WARN-1 + WARN-3 + WARN-5 + INFO-3)
- `canonical/story/skill-system-2026-05-24.md` (primary)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (primary for T4)
- `canonical/story/off-hand-items-2026-05-24.md` § 2.3 (primary for SC-3)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 3.6 + § 4.2-4.3 (bc_axis_contribution shape)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes)
- `agentic_orchestration/dispatches/2026-05-21-rocket-w1-13-skill-tree-node-population.md` § 2.1 + § 3.1 (P1 substrate enrichment items + invariants — original FIRE-GATE procedurally closed; references preserved)
- Cycle 12 Layer 2 dispatch (parallel): `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-2-bc-target-subspace-generator.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (6 strategies for T4Candidate reference)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q4 Option B + Q5 SC-3 absorbed into L3) + KR autonomously orchestrates Layer 3 dispatch authoring per scope-doc § 1
**Status:** FIRE — all 5 pre-Layer-2/3 prereqs cleared; fires in parallel with Layer 2 dispatch

**Matt-touch sequence:** rocket Layer 3 implementation lands (~2-3 weeks; parallel with L2) → jack-ryan Gate-2 validates → KR captures in state file; integrates with Layer 2 output for Layer 4 multi-dim convergence sequencing (MC-3 methodology consult fires at Layer 4 start; Layer 4 fires after L2+L3 lock)
