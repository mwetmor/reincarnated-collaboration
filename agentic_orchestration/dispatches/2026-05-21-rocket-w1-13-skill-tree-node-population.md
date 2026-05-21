# Dispatch — Rocket W1.13: Procedural Skill Tree Node Population + Multi-Dim Convergence

**Date:** 2026-05-21 (pre-staged); FIRE-GATE closed + rescope landed 2026-05-22 by critique-pair (gandalf design + jack-ryan process) under Matt pre-authorization D
**Author:** gandalf (original); 2026-05-22 rescope by critique-pair
**Recipient:** rocket (engine generation seam)
**Status:** **FIRE-GATE CLOSED 2026-05-22; STILL GATED on P1 substrate enrichment + Matt W1.13 framing approval per § 9 timing.** Rescope per Scenario B (dual-witness + Surface A footnote); see `canonical/story/w1-13-rescope-disposition-2026-05-22.md` for full disposition record.
**Priority:** HIGH (load-bearing architectural commitment under dual-witness + BDI + T4 mandate; empirical urgency reduced post-recovery; architectural urgency preserved)
**Estimated effort:** 2-4 weeks (math note v1.1 § 9 implementation; canon-validated parameters; unchanged from pre-rescope)

---

## 0.0 FIRE-GATE — **CLOSED 2026-05-22**

The two FIRE-GATE conditions added 2026-05-21 evening are now SATISFIED:

### Condition 1 — LC-011 attribution-complete ✅ SATISFIED

The 45-season LC-011 ablation recovery completed 2026-05-22 morning under Matt's prolonged-autonomy mandate. Summary artifact at `~/Games/reincarnated-engine/logs/w07_lc011_ablation_recovery_summary.json`:

- Run 1 baseline (post-W0.10 stack; current calibration): 3/60 mage_controller FAILED = **5.0%** (boundary signal — NOT historical 41.8% floor-lock)
- Run 2 observational: 2/60 = 3.3%
- Run 3 Surface A ablation (skill_power_tier 50→42): 1/60 = **1.7%**
- **Surface_A% = 66.67%; Residual% = 33.33%; formula well-defined; disposition `ATTRIBUTION_COMPUTED`**

This is **Scenario B** per critique-pair dispatch `agentic_orchestration/dispatches/2026-05-22-critique-pair-post-recovery-w07-gate2-w113-rescope-p0-close.md` § 1.2 (Surface A meaningful attribution at reduced magnitude). LC-011 reframed as Surface A footnote (5% boundary signal with recovery-grade two-way attribution); historical 41.8% rate confirmed as era-stratified to a calibration regime superseded by the post-W0.10 stack.

### Condition 2 — Math note v1.1 § 1.2 reconciled ✅ SATISFIED

Math note v1.1 § 1.2 revised 2026-05-22 from TRIPLE-WITNESS (Track C + W0.10 + LC-011) to **DUAL-WITNESS + Surface A footnote** per critique-pair dispatch § 4. LC-011 demoted from primary witness to footnote with recovery-grade attribution. Architectural mandate stands on:
1. Track C scalar-modifier underdetermination (unchanged)
2. W0.10 LOW-modifier band residual (unchanged)
3. BDI formalism rank-3 substrate-richness requirement (new anchor; `canonical/story/build-defining-resonance-formula-2026-05-21.md`)
4. Tier 4 mechanic-altering keystone framing (new anchor; math note § 3.4)

**FIRE-GATE § 0.0 closes.** Critique-pair (gandalf design + jack-ryan process) attests; β autonomous path executed under Matt pre-authorization D.

### Remaining gates (unchanged)

The FIRE-GATE closure does NOT trigger immediate W1.13 implementation. The original sequencing conditions still apply per § 9 timing:

- **P1 substrate enrichment must complete first** — W1.1 schema extensions + W1.2-W1.6 substrate creation + W1.11 element-specific enrichment must close Q4 substrate gap (~168+ unique skill templates per season; all 7 BC axes meeting 5× sufficiency rule)
- **W0.4 gear-affix verification** must complete (specialist code audit; status of gear affix architecture state)
- **Matt W1.13 framing approval** must land (per protocol § 7.1; this is a NEW scope approval gate distinct from math note v1.1 ratification which already stands)

### Cross-references

- `agentic_orchestration/dispatches/2026-05-22-critique-pair-post-recovery-w07-gate2-w113-rescope-p0-close.md` — critique-pair dispatch authorizing FIRE-GATE closure + rescope
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md` — full rescope disposition record (Scenario B; BDI/T4 alignment preserved)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 1.2 (2026-05-22 revision) — dual-witness reframing
- `~/Games/reincarnated-engine/logs/w07_lc011_ablation_recovery_summary.json` — recovery summary artifact
- `agentic_orchestration/matt-briefing-2026-05-22-lc-011-option-c-strong-confirm.md` — Matt-briefing escalation memo
- `agentic_orchestration/p0-closure-note-2026-05-21.md` § 4.1 — fire-gated downstream conditions
- `agentic_orchestration/gandalf/notes/2026-05-21-lc-011-reframing-disposition-w1-13-routing.md` Appendix A — original LC-011 disposition framing

---

---

## 0. TL;DR

W1.13 implements the **multi-dim convergence algorithm + procedural per-class-per-season skill tree node population** per math note v1.1.

This is the empirically-mandated architectural fix for the Pattern-A pathology that W0.9 + W0.10 arena-side fixes couldn't address for low-modifier kits. Track C verdict (2026-05-21) + W0.10 re-sweep confirm: arena migration discharges HIGH-modifier band; multi-dim convergence (THIS workstream) discharges LOW-modifier band.

**Authoritative inputs (must read before implementation):**
1. `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — math note v1.1 (algorithmic spec)
2. `agentic_orchestration/legolas/research/arpg-skill-architecture-canon-survey-2026-05-21/` — ARPG-canon validation of parameter choices

---

## 1. Why this work

### 1.1 The empirical mandate — DUAL-WITNESS + Surface A footnote (revised 2026-05-22)

**Per Track C synthesis (`canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md`):** Pattern-A is universal at boss tier under scalar-modifier-only optimization. 100% Pattern-A across all 7 substrates at same calibration. The single-scalar tuning surface is mathematically underdetermined for 5-tier WR contract.

**Per W0.10 re-sweep:** arena migration alone discharges HIGH-modifier band (physical_grappler + hunter both boss_wr 0.000→1.000). LOW-modifier kits (≤0.33) remain at 0.000. Modifier-scaling gap = multi-dim convergence territory.

**Per BDI formalism (`canonical/story/build-defining-resonance-formula-2026-05-21.md`):** rank-3 substrate-richness expression requires interaction-term dominance over linear terms. γ_{abc} > β_{ab} > α_a is structurally inexpressible in scalar-modifier-only space; multi-dim convergence is the dimensional precondition for rank-3 build-defining moments.

**Per Tier 4 mechanic-altering keystone framing (math note v1.1 § 3.4):** Tier 4 keystones as qualitative regime-change require categorical-discrete selection × continuous SP × discrete trigger-interaction selection; not collapsible to scalar.

**Per LC-011 reframed (Surface A footnote; recovery-grade attribution 2026-05-22):** post-W0.10 stack boundary signal is 5% (not historical 41.8%); skill_power_tier (Surface A) accounts for 66.67% of boundary-signal reduction under ablation; residual 33.33% includes era-stratification effects + other post-W0.10 stack contributions. Historical 41.8% floor-lock rate was era-stratified to a calibration regime that no longer applies. Skill_power_tier surfaces as a **causally active authorship parameter** for Tier 4 elemental keystone design (T4-B implication; not an active generation-time pathology).

**The architectural fix:** procedural skill tree node population + multi-dim convergence over 5-6 dimensions instead of 1. The fix is mandated by Track C + W0.10 + BDI + Tier 4 architecture; LC-011 is the footnote-tier Surface A anchor for any future calibration work.

See `canonical/story/w1-13-rescope-disposition-2026-05-22.md` for full disposition rationale of the dual-witness reframing.

### 1.2 The architectural commitment (math note v1.1 § 0)

| Layer | What ships |
|---|---|
| Tree generation | Procedural per-class-per-season ~10-15 nodes / 2-4 chains / 3-4 tiers |
| Per-node anatomy | BC-axis-contribution tags + cost/cooldown + node-type enum + Tier 1 playability invariant |
| Tier 4 nodes | MECHANIC-ALTERING keystones (qualitative regime changes, not pure scaling) |
| Trigger interactions | 1-2 per chain (multiplicative scaling layer above additive) |
| Convergence algorithm | WR-skew gradient + multi-tier voting + soft preferences + local optima escape |
| Convergence dimensions | 5-6 (SP + Tier 4 selection + trigger selection + scalar + gear-provisional + tier-coefficients) |
| Reference build output | Every archive entry stores kit_specification block (per math note § 7) |

### 1.3 Reincarnated's v1 scope vs v2 trajectory

Per math note v1.1 § 8.3 + Matt 2026-05-21 late-amendment:

- **v1 (THIS workstream):** 10-15 nodes / 2-4 chains — current substrate supports this scope
- **v2 (post-Profile-A-ship; substrate-growth-gated):** 24-30 nodes / 3-5 chains — canonical-parity expansion as more classes + skills generated

**v1 algorithm structure is parameter-shift-robust** — v2 transition is parameter shift, not algorithmic shift. Implementation effort transfers cleanly to v2 scope.

---

## 2. Pre-requisites (MUST be complete before W1.13 fires)

### 2.1 Q4 substrate-gating check

Per math note v1.1 § 8.3.1 + legolas Phase 1 substrate audit (2026-05-20):

**Current engine substrate state (P0 close):**
- 4 of 7 BC axes have PARTIAL or GAP coverage relative to 5× sufficiency rule
- HP-economy, charge-stack, damage-converts substrate categories at 0
- Multiple Ability schema fields absent

**Required for W1.13:**
- ~168+ unique skill templates per season for full archive diversity
- All 7 BC axes meeting 5× sufficiency rule
- Ability schema complete with v1.1 fields per math note § 3.6

**P1 workstreams that close the gap (MUST complete before W1.13):**
- **W1.1** Ability schema extensions — adds v1.1 fields (`node_type`, `cost`, `cooldown_seconds`, `playable_at_level_1`, `interaction_metadata`, `keystone_effect`, BC-axis-contribution tags)
- **W1.2** HP-economy substrate creation (~25 templates)
- **W1.3** damage-taken-converts substrate creation (~25 templates)
- **W1.4** charge-stack substrate creation (~25 templates)
- **W1.5** Movement-skill substrate variety expansion (~30 templates)
- **W1.6** Player-side proxy substrate creation (~25 templates)
- **W1.11** Element-specific substrate enrichment (uniform comprehensive depth per Track C verdict)

**Knight-rider sequencing: P1 substrate enrichment (W1.1-W1.6 + W1.11) must complete before W1.13 fires.**

### 2.2 W0.4 gear-affix verification

Per math note v1.1 § 5.7 (gear affix dimension PROVISIONAL):
- If gear affixes directly modify skills: dimension 6 activates (per-skill modifier vector `g`)
- If gear affixes only modify stats: dimension 6 collapses; algorithm functions unchanged

**Knight-rider needs W0.4 specialist code audit verification before W1.13 final parameter calibration** (status of gear affix architecture state).

### 2.3 Matt approval gates

Per protocol § 7.1 + math note v1.1 § 9.4:
- **W1.13 framing approval** — Matt approves before implementation fires (NEW scope from protocol v1.1)
- **Math note v1.1 ratification** — math note v1.1 stands per session 2026-05-21; no further Matt approval needed

---

## 3. Implementation scope (per math note v1.1 § 9.1)

### 3.1 Substrate generation work

**Per-class-per-season skill tree generation function:**
- Tree topology: 2-4 chains × 3-4 tiers × ~10-15 total nodes per kit (v1 scope)
- Per-node abstract mechanic class assignment (damage/control/defense/mobility/utility)
- Per-node BC-axis-contribution tagging (5+ floats per node)
- Tier-specific coefficient assignment per node (1.05-1.25 by tier; per math note § 3.3)
- **Tier 4 mechanic-altering keystone CANDIDATES per chain (~3-5 candidates per chain)**
- **Trigger/conditional interaction nodes per chain (1-2 per chain)**
- **Tier 1 playability enforcement** — generator validates each chain has ≥1 L1-playable Tier 1 node before tree finalization (cost ≤ class-budget; cooldown ≤ 2.0s; no prerequisite)

**Critical generation invariants:**
1. **Tier 1 playability** (Matt 2026-05-21 hard requirement) — each chain MUST have at least one Tier 1 node satisfying `cost ≤ L1_resource_budget` AND `cooldown_seconds ≤ 2.0` AND `playable_at_level_1 == True`
2. **Substrate-agnostic generation** — nodes have no fire/water/shadow identity at generation; cohesion-judge themes per substrate POST-generation (per substrate-as-cohesion architecture)
3. **Tree topology validity** — chain prereqs + cross-chain rules + tier structure all consistent per canonical/32 § B6 templates

### 3.2 Convergence algorithm work

**Per math note v1.1 § 4:**

- **WR-skew gradient mechanism** (§ 4.2)
- **Multi-tier voting per-iteration with 3 phases:**
  - Phase 1: continuous SP adjustments
  - Phase 2: Tier 4 keystone discrete selection
  - Phase 3: trigger interaction discrete selection
- **Soft-preference tier-unlock penalty with gates 2/4/7** (§ 4.1; canon-aligned per legolas SD-2)
- **Tier 1 playability runtime safety check** (§ 4.6; generation invariant enforced at convergence)
- **Local optima escape via random restart** (§ 4.4)
- **Budget + cap + topology constraint enforcement**

### 3.3 Telemetry instrumentation

- Per-iteration WR deltas + adjustment vectors
- Convergence iteration count per kit
- **Tier 4 keystone selection changes per iteration** (NEW)
- **Trigger interaction activation/deactivation changes per iteration** (NEW)
- Escape restart count per kit
- Final SP allocation + Tier 4 selection + trigger selections + scalar modifier per archive entry

### 3.4 Reference build output (per math note v1.1 § 7)

Every archive entry stores kit_specification block:

```yaml
kit_specification:
  tree_seed: <class_seed_S>
  chains: [{id, depth, abstract_role}]
  nodes: [...]
  sp_allocation: {node_id: rank}
  tier_4_keystone_selections: {chain_id: keystone_id}    # NEW v1.1
  trigger_interaction_selections: {chain_id: [interaction_id, ...]}  # NEW v1.1
  scalar_modifier: <float>
  gear_affix_assignments: [...]  # provisional pending W0.4
```

### 3.5 Out of scope for W1.13

Per math note v1.1 § 9.2:
- Legendary skill grant mechanism (separate workstream; deferred)
- Per-skill scaling coefficient variance within a tier (v2)
- Cross-chain unlock asymmetry per element (post canonical-6 multi-element retired)
- Smooth rank cap formula (UX-side; not engine-side)
- Spirit Guide build-coach UI (Stage A3 territory)
- Player-facing skill tree UI changes (B6 work; demo-side)
- Endgame tuning surface (deliberate departure per math note § 8.3)

---

## 4. Math-before-code gates (per Discipline #1)

Before implementation begins, math note v1.1 § 10 specifies:

1. `penalty_scale` value for soft-preference tier-unlock (empirical calibration target: 80-95% canonical-gate respecting)
2. `T_AXIS_SENS` matrix values (calibrated against ARPG-canon + empirical telemetry)
3. `VOTE_THRESHOLD` value (minimum vote magnitude to trigger SP adjustment)
4. `ESCAPE_THRESHOLD` value (iterations without improvement before restart)
5. Initial `kit` state distribution (bias toward BC-target + initial Tier 4 keystone inference + initial trigger interaction inference)
6. `MAX_ITER` budget (per-kit convergence iteration cap)
7. **Tier 1 playability bounds per class element** (cost / cooldown thresholds parametrized per substrate; NEW v1.1)
8. **Tier 4 keystone candidate set size** (per-chain candidate count; proposed: 3-5; NEW v1.1)
9. **Trigger interaction effect multiplier range** (per-chain interaction magnitude; proposed: 1.15-1.50× multiplicative; NEW v1.1)

**Pre-implementation math-note Phase 1 work** (rocket authors):
- Detailed pseudocode for each algorithm phase (§ 4.3 main loop)
- Calibration plan for parameters 1-9
- Discipline #11 cold-start measurement plan
- Math-before-code review by jack-ryan Gate-1 before implementation begins

---

## 5. Verification approach (per math note v1.1 § 9.3)

### 5.1 Unit tests

- WR-skew gradient computes correct direction on synthetic per-tier deltas
- Multi-tier voting respects budget conservation
- Soft-preference penalty produces 80-95% canonical-gate-respecting solutions
- **Tier 1 playability invariant enforced at generation time** (NEW v1.1)
- **Tier 4 keystone categorical selection converges to high-WR-fit** (NEW v1.1)
- **Trigger interaction combinations selected appropriately** (NEW v1.1)
- Local optima escape triggers on stagnation

### 5.2 Integration tests

- End-to-end convergence on 5-10 representative test kits (one per substrate)
- Per-tier WR convergence within contract bounds for 80%+ of test kits
- All test kits have L1-playable Tier 1 nodes per chain
- Convergence iteration count median <20

### 5.3 Empirical validation — revised 2026-05-22 (Scenario B baseline)

**Baseline reference revised** per Scenario B disposition: current 5% mage_controller boundary signal (Run 1 of recovery) replaces the historical 41.8% floor-lock rate as the empirical baseline. The architectural fix's value-add is **supporting BDI rank-3 expression + Tier 4 mechanic-altering authorship + closing W0.10 LOW-modifier band residual** — not "discharge a 42% pathology."

**Validation criteria:**

- Re-run Track C-style same-calibration ablation across all 7 substrates (UNCHANGED — Track C signal stands; scalar-modifier underdetermination is a formalism property)
- LOW-modifier kits (≤0.33 modifier) previously at 0.000 boss WR exit zero-floor via keystone-concentration + trigger interactions (W0.10 residual closure target — UNCHANGED)
- **Pattern-A measurement** — pre-W1.13 100% Pattern-A across substrates; post-W1.13 v1 expected 20-40%; v2 target 5-15% (UNCHANGED — measures cross-substrate convergence-time compression, not floor-lock generation failures)
- **Mage_controller generation pass-rate** — post-W1.13 expected 0-2% boundary signal against 5% Run-1 baseline (REVISED from "≥80% against 42% baseline"; ~3 percentage-point modest improvement expected from Surface A residual + multi-dim convergence dimensionality, not a 38-point discharge)
- **BDI hypothesis test re-run** — post-W1.13 archive should empirically materialize rank-3 γ-dominance per BDI H1, H4 success criteria (NEW; tied to BDI hypothesis tests W1.20-W1.22)
- **Tier 4 keystone discrete-selection convergence** — categorical Tier 4 selection per chain should converge cleanly under multi-tier WR voting (NEW; tied to T4-A architecture defaults and T4-B catalogue authorship)
- **Trigger interaction discrete-selection convergence** — 0-2 trigger interactions per chain should converge under multi-tier voting (NEW; tied to legolas SD-3)

**The empirical urgency is reduced (no 42% pathology to discharge); the architectural urgency stands (Track C + W0.10 + BDI + T4 mandate all preserved).** See `canonical/story/w1-13-rescope-disposition-2026-05-22.md` § 2.3 for the full success-criteria revision rationale.

---

## 6. Critique-pair structure (per math note v1.1 § 9.4)

- **gandalf reviews architectural alignment** before implementation begins (Gate-1):
  - Substrate-as-cohesion preservation
  - Reference build output completeness
  - ARPG-canon thematic anchor strength
  - Tier 4 mechanic-altering authenticity
  - Trigger interaction multiplicative scaling
  - Tier 1 playability enforcement

- **jack-ryan reviews implementation correctness** at cumulative Gate-2:
  - BC-axis-contribution tagging integrity
  - Coefficient curve sensibility
  - Topology constraint enforcement
  - Discipline #13a drift check
  - Gate value 2/4/7 correctness
  - Categorical-selection optimization correctness

- **Matt approves W1.13 framing** before implementation fires (per protocol § 7.1; NEW scope from protocol v1.1)

---

## 7. Cross-references

**Authoritative inputs:**
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — math note v1.1 (algorithmic spec) — **READ FIRST**
- `agentic_orchestration/legolas/research/arpg-skill-architecture-canon-survey-2026-05-21/` — ARPG-canon parameter validation

**Architectural foundation:**
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md`
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `canonical/story/substrate-design-supplement-2026-05-21.md`
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md`

**Reincarnated canonical UX/story spec (preserved):**
- `canonical/32-progression-design.md`
- `canonical/33-progression-skeleton.md`
- `canonical/story/b6-skill-tree-ui-scoping.md`

**Empirical foundation:**
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md`
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md`
- `reincarnated-engine/src/reincarnated/simulation/math/w0-10-boss-ai-leash-reset-fix.md`

**Hive coordination:**
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.10 — math note v1.1 + legolas survey awareness
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.2 W1.13 — workstream description

**Engineering disciplines:**
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code (this work instantiates); #11 empirical inspection; #13a drift detection; #17 empirical calibration

---

## 8. Authority + escalation

- **Implementation choices within math note v1.1 spec:** rocket autonomous
- **Math note v1.1 spec ambiguity:** route to gandalf; gandalf authors clarification or v1.2 amendment
- **Parameter calibration choices (per § 4):** rocket proposes; jack-ryan reviews; calibrated via empirical sweeps
- **If implementation surfaces a finding that suggests math note v1.1 needs structural revision:** flag immediately to gandalf for v1.2 framing decision; Matt approves any structural pivot
- **Discovery of canonical-32 incompatibility:** flag immediately; gandalf reconciles with canonical UX/story spec or proposes spec revision

---

## 9. Timing

- **Fire condition:** P1 substrate enrichment complete (W1.1-W1.6 + W1.11) + W0.4 gear-affix verification complete + Matt W1.13 framing approval
- **Earliest fire date:** P1 progress dependent; estimated 5-8 weeks post-P0-close (after substrate enrichment)
- **Duration:** 2-4 weeks of focused implementation
- **Phase 1 (math-before-code):** ~3-5 days — rocket authors detailed pseudocode + calibration plan; jack-ryan + gandalf Gate-1 review
- **Phase 2 (implementation):** ~2-3 weeks — generation + convergence + telemetry + reference build output
- **Phase 3 (verification):** ~3-5 days — unit + integration + empirical validation

---

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine's multi-dim convergence + skill tree node population architectural fix, ready for P1 W1.13 fire.
