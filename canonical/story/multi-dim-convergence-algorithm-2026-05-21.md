# Multi-Dim Convergence Algorithm — QD-Engine W1.13 Architectural Spec

**Status:** v1 DRAFT — authored 2026-05-21; v1.1 amendment expected after legolas ARPG-canon survey completes (1-2 days)
**Author:** gandalf
**Recipient (eventual):** rocket (P1 W1.13 implementation specialist)
**Companions:**
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — QD-engine vision
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC operational spec
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion architecture
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — end-to-end workflow
- `canonical/32-progression-design.md` — Reincarnated's UX/story-driven canonical skill tree spec
- `canonical/story/b6-skill-tree-ui-scoping.md` — B6 UI scoping spec
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` — empirical mandate for multi-dim convergence

---

## 0. TL;DR

**The empirical mandate:** Track C synthesis (2026-05-21) + W0.10 re-sweep (2026-05-21) confirmed that boss-tier WR convergence is mathematically underdetermined under scalar-modifier-only optimization. Low-modifier kits (≤0.33) cannot escape boss-zero floor via parametric tuning of existing flat-skill kits.

**The architectural fix:** procedural skill tree node population per class per season + multi-dim convergence over per-node SP allocation × tier-specific scaling × scalar modifier × gear affix modifiers (4-5 dimensions instead of 1).

**The scope target — Scope D (hybrid):** preserves canonical chain × tier shape + tier-specific scaling coefficients (load-bearing for math); relaxes hard tier-unlock gates into soft preferences (math + engineering wins); defers per-skill scaling variance to v2 (UX polish).

**Important caveat (Matt 2026-05-21):** legolas ARPG-canon survey runs in parallel. Findings may transform Scope D beyond recognizability. Scope D is starting structure, not final commitment. This document is v1; v1.1 amendment fold-in expected within 2-3 days.

**Critical algorithm components:**
- WR-skew gradient: per-tier WR-delta drives per-node SP adjustment direction
- Multi-tier voting: 5 tiers vote on per-node SP changes proportional to wr_delta × node-contribution
- Soft-preference tier-unlocks: UX shows canonical gates; engine optimizes smoothly underneath
- Local optima escape: random restart on stagnation
- Tier-specific scaling PRESERVED: 1.05-1.08 / 1.08-1.12 / 1.12-1.18 / 1.18-1.25 per rank by tier (load-bearing for boss-floor fix)
- Substrate-as-cohesion: nodes are substrate-AGNOSTIC at generation; cohesion-judge themes post-generation

---

## 1. Provenance and the ARPG-canon-research caveat

### 1.1 Document genesis

This math note emerged from an extended session between Matt and gandalf 2026-05-21 covering:

1. The 4/5-dimensional convergence problem framing
2. The architectural choice between minimum-viable scope (A), full canonical scope (B), and hybrid (D)
3. Per-tier scaling coefficient preservation (load-bearing for math; concern 1)
4. ARPG-canon research scope (concern 2 — legolas commission)

Matt's explicit caveat (2026-05-21):
> *"ARPG knowledge and related decisions may transform scope D beyond recognizability, but it is a good structure."*

This document honors that caveat. It locks the ALGORITHM structure and the SOFT-PREFERENCE math reinterpretation of canonical UX gates, but flags specific PARAMETER VALUES (chain count, tier depth, SP budget, cap, scaling coefficients) as subject to legolas research-driven revision.

### 1.2 The empirical foundation — why this work matters

The recompose-hive findings (2026-05-19/20) + Track C synthesis (2026-05-21) + W0.10 re-sweep (2026-05-21) jointly establish:

- **Pattern-A is universal at boss tier under scalar-modifier-only optimization** (100% Pattern-A across all 7 substrates at same calibration; Track C)
- **The arena-side fix (W0.9 + W0.10) discharges the HIGH-modifier band** (≥0.64) — physical_grappler + hunter both boss_wr 0.000→1.000 post-fix
- **The LOW-modifier band (≤0.33) remains at 0.000** — modifier-scaling gap requires multi-dim convergence (P1 W1.13 mandate)

This document specifies the algorithm that addresses the low-modifier residual.

---

## 2. The mathematical convergence problem (formalized)

### 2.1 Problem statement

**Given:**
- A per-class-per-season skill tree (~10-15 nodes; chains × tiers structure per Scope D)
- A BC-cell target (8-axis coordinate)
- Per-tier WR contract: swarm 0.65-0.80; magic 0.55-0.70; elite 0.45-0.60; mini-boss 0.35-0.55; boss 0.30-0.45
- Game-loop simulation (true multi-monster spatial gauntlet per W0.9)
- Player-character stats + base damage + gear affixes available

**Find:**
- Per-node SP allocation (`sp_i` for each node `i`, integer 0-15 per cap)
- Subject to: `sum(sp_i) ≤ 120` (budget); per-node cap; soft tier-unlock preferences; cross-chain rules
- Plus: scalar kit modifier `m` (continuous)
- Plus: gear affix modifier vector `g` (pending W0.4 verification of skill-modifier vs stat-only affix state)
- Such that: per-tier WR within contract bounds AND BC coordinate matches target cell

**This is a mixed-integer-continuous optimization problem with soft-preference constraints and multi-objective output.**

### 2.2 The mathematical underdetermination of scalar-modifier-only optimization

Pre-W1.13, the convergence problem reduces to:
- Find scalar `m` such that 5 per-tier WR constraints are simultaneously satisfied
- 1 unknown vs 5 constraints → systematically underdetermined
- Result: scalar `m` either over-fits one tier and under-fits others (Pattern-A compression observed empirically)

Post-W1.13, the convergence problem has:
- ~10-15 per-node SP integers + scalar `m` + gear affix vector `g` = ~15-25 unknowns
- 5 per-tier WR constraints + per-cell BC matching = 5+ constraints
- Over-determined tuning surface → multi-tier WR contract satisfiable

**The dimensional shift is the architectural fix.**

### 2.3 Why tier-specific scaling coefficients are load-bearing

For low-modifier kits (e.g., fire_mage at modifier=0.10):

- Required boss DPS to clear in 240s: 53,216 HP / 240s = 222 HP/s
- Under uniform scaling 1.10: rank-15 keystone = 4.18× multiplier. Result: 500 × 0.10 × 4.18 = 209 DPS. Marginal/insufficient.
- Under tier-specific scaling 1.25 (Tier-4 keystone): rank-15 keystone = 28.42× multiplier. Result: 500 × 0.10 × 28.42 = 1,421 DPS. Comfortable.

The 6.8× DPS spread between uniform-1.10 and tier-specific-1.25 IS the lever that makes low-modifier kits viable at boss tier through keystone concentration.

**Tier-specific scaling coefficients are LOAD-BEARING for the multi-dim convergence's boss-floor-fix promise.** Scope D preserves them.

---

## 3. Existing canonical structure (preserved)

Per `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md`:

### 3.1 Structural shape

- **Chain count per class**: 2-4 chains (variance allowed)
  - Specialists: 2 chains × 4 tiers = ~8 skills (deep mastery)
  - Balanced: 3 chains × 4 tiers = ~12 skills (default)
  - Generalists: 4 chains × 3 tiers = ~12 skills (wide options)
  - Asymmetric: 1 chain × 4 tiers + 2 chains × 3 tiers = 10 skills (focused with options)

- **Kit size**: 10-15 nodes per class (B9 endgame baseline)
- **SP budget**: 120 (B9 endgame; level 50)
- **Per-skill cap**: `min(15, floor(level/3.33))` — endgame cap = 15
- **Cross-chain rules**: single-element strict (same-chain unlock); multi-element flexible (retired post canonical-6)

### 3.2 Tier-specific scaling coefficients (per rank power gain)

| Tier | Coefficient range | Per-rank power gain interpretation |
|---|---|---|
| Tier 1 (primary) | 1.05-1.08 | Modest per-rank; spammable feel |
| Tier 2 (mid) | 1.08-1.12 | Moderate per-rank |
| Tier 3 (advanced) | 1.12-1.18 | Strong per-rank |
| Tier 4 (keystone) | 1.18-1.25 | Very strong per-rank (build-defining payoff) |

**This is preserved as LOAD-BEARING for math (per § 2.3).**

### 3.3 Per-node schema fields (existing canonical)

Per canonical/32 + B6 templates Stage A1:
- `id` — node identifier
- `tier` — 1-4
- `chain_id` — chain affiliation
- `chain_position` — position within chain
- `parent_skill_ids` — prerequisite chain
- `scaling_coefficient` — per-skill scaling value (within tier's range)

**Schema extensions required by this math note (NEW):**
- `bc_axis_contribution_tags`: dict of axis_id → contribution weight (for gradient signal)
  - axis_1_engagement: float (range × mobility contribution)
  - axis_2_geometry: enum + weight (which geometry bin; how strongly)
  - axis_2A_proxy: float (proxy entity contribution)
  - axis_2B_control: float (control budget contribution)
  - axis_3A_tempo: float (damage tempo contribution)
  - axis_3B_variance: float (per-event variance contribution)
  - axis_4_defensive: float (eHP or avoidance contribution)
  - axis_5_economy: enum + weight (which economy bin; how strongly)

This is the per-node BC-axis-contribution tagging that enables WR-skew gradient signal direction.

---

## 4. The math layer (NEW — what this document adds)

### 4.1 Soft-preference tier-unlock handling

**Canonical UX gates (hard thresholds):**
- Tier 2 unlocks at ≥3 ranks in any Tier 1 parent skill
- Tier 3 unlocks at ≥5 ranks in any Tier 2 parent skill
- Tier 4 unlocks at ≥8 ranks in any Tier 3 parent skill

**Math-side relaxation (soft preferences):**

Instead of hard binary gates, the convergence cost function applies a **soft penalty** for under-investment in prerequisite tiers:

```
soft_unlock_penalty(node, sp_allocation) =
    if node.tier == 1:
        0  (no prerequisite)
    elif node.tier == 2:
        max(0, 3 - max(prereq_rank)) × penalty_scale
    elif node.tier == 3:
        max(0, 5 - max(prereq_rank)) × penalty_scale
    elif node.tier == 4:
        max(0, 8 - max(prereq_rank)) × penalty_scale
```

Where `penalty_scale` is calibrated such that:
- Hard-gated behavior emerges if penalty_scale → ∞ (canonical UX feel)
- Smooth optimization emerges if penalty_scale → 0 (engineering ease)
- **Calibration target: penalty_scale produces ~80-95% of optimal solutions respecting canonical gates, with 5-20% allowed boundary-flexibility for convergence smoothness**

**Player-facing UX impact:** ZERO. The UI continues to show canonical hard gates. The engine's convergence optimizer operates underneath on the smooth landscape; the resulting kits land 95%+ within canonical gate constraints.

**Why this matters:** the optimizer can find a globally-better solution that's "1 rank short of canonical gate" without being trapped in a local optimum at the exact gate threshold.

### 4.2 WR-skew gradient mechanism

**Core insight:** per-tier WR-delta from target IS the gradient signal direction.

For each tier T in {swarm, magic, elite, mini_boss, boss}:
```
wr_delta[T] = measured_wr[T] - target_wr[T]
```

If `wr_delta[T] > 0`: tier T is over-performing → reduce SP in nodes that contribute to tier T's performance
If `wr_delta[T] < 0`: tier T is under-performing → increase SP in nodes that contribute to tier T's performance
If `wr_delta[T] ≈ 0`: tier T is at target → preserve current SP in tier-T-contributors

**Per-tier contribution attribution:**

Each node has BC-axis-contribution tags (per § 3.3). Each TIER of the WR contract is more sensitive to specific BC axes:

| Tier | Most-sensitive BC axes | Why |
|---|---|---|
| Swarm | Axis 2 (geometry: AOE-favoring), Axis 3A (tempo) | Many entities; AOE damage is force-multiplier |
| Magic | Axis 2 (geometry: small/large-AOE balanced), Axis 4 (defensive) | Mid-density; survivability matters |
| Elite | Axis 4 (defensive), Axis 3A (tempo), Axis 2 (geometry) | Sustained engagement; defense + sustained damage |
| Mini-boss | Axis 3B (variance: spike-favoring), Axis 4 (defensive), Axis 5 (economy) | Burst windows matter; resource economy under pressure |
| Boss | Axis 3B (variance: spike-favoring), Axis 4 (defensive) | Single target; burst damage; survivability |

**This tier-axis sensitivity matrix (T_AXIS_SENS[T][axis]) is calibrated against ARPG-canon + empirical telemetry. Specific values flagged for legolas research input (§ 16).**

### 4.3 Multi-tier voting algorithm

Pseudocode:

```python
def multi_tier_voting_adjustment(kit, tier_wr_deltas, tier_axis_sensitivity, nodes):
    """
    Compute per-node SP adjustment direction from multi-tier WR deltas.
    Returns dict of {node_id: adjustment_signed_int} respecting budget conservation.
    """
    votes = {node.id: 0.0 for node in nodes}
    
    for tier in [swarm, magic, elite, mini_boss, boss]:
        wr_delta = tier_wr_deltas[tier]  # measured - target
        sensitivity = tier_axis_sensitivity[tier]  # dict of axis → sensitivity weight
        
        for node in nodes:
            # Compute node's contribution to this tier's performance
            tier_contribution = 0.0
            for axis_id, axis_contribution in node.bc_axis_contribution_tags.items():
                tier_contribution += axis_contribution * sensitivity[axis_id]
            
            # Vote: under-performing tier wants MORE in contributing nodes; over-performing wants LESS
            votes[node.id] += -wr_delta * tier_contribution
            #                 ^^^^^^^^^^^^^^^^^^^^^^^^^
            #                 Negative wr_delta (under) → positive vote (more SP)
            #                 Positive wr_delta (over) → negative vote (less SP)
    
    # Normalize votes to respect total budget (Σ adjustments = 0)
    total_positive = sum(v for v in votes.values() if v > 0)
    total_negative = sum(v for v in votes.values() if v < 0)
    
    if total_positive > 0 and total_negative < 0:
        # Scale positives to match negatives in magnitude (zero-sum redistribution)
        scale = min(abs(total_negative) / total_positive, 1.0)
        for node_id in votes:
            if votes[node_id] > 0:
                votes[node_id] *= scale
    
    # Convert continuous votes to integer SP adjustments (one rank per iteration)
    adjustments = {}
    for node_id, vote in votes.items():
        if abs(vote) > VOTE_THRESHOLD:
            adjustments[node_id] = +1 if vote > 0 else -1
        else:
            adjustments[node_id] = 0
    
    return adjustments
```

**Per-iteration loop:**

```python
def multi_dim_converge(class_seed, bc_target, per_tier_targets, max_iter=50):
    tree = generate_tree(class_seed)  # per W1.13 substrate generation
    sp_allocation = initialize_sp_allocation(tree, bc_target, budget=120)
    scalar_modifier = 1.0
    
    no_improvement_count = 0
    best_score = float('inf')
    
    for iteration in range(max_iter):
        # Run gauntlet
        per_tier_wr = run_spatial_gauntlet(tree, sp_allocation, scalar_modifier)
        
        # Check convergence
        if all_within_contract(per_tier_wr, per_tier_targets):
            return ConvergedKit(tree, sp_allocation, scalar_modifier, per_tier_wr)
        
        # Compute score for stagnation detection
        score = sum(abs(per_tier_wr[t] - per_tier_targets[t]) for t in tiers)
        if score < best_score - EPSILON:
            best_score = score
            no_improvement_count = 0
        else:
            no_improvement_count += 1
        
        # Escape local optimum if stagnant
        if no_improvement_count >= ESCAPE_THRESHOLD:
            sp_allocation = random_restart_with_bc_target_bias(tree, bc_target)
            scalar_modifier = 1.0
            no_improvement_count = 0
            continue
        
        # Multi-tier voting → per-node adjustments
        adjustments = multi_tier_voting_adjustment(
            kit=sp_allocation,
            tier_wr_deltas={t: per_tier_wr[t] - per_tier_targets[t] for t in tiers},
            tier_axis_sensitivity=T_AXIS_SENS,
            nodes=tree.nodes
        )
        
        # Apply adjustments with soft-preference penalty + budget + cap constraints
        sp_allocation = apply_adjustments_with_constraints(
            sp_allocation,
            adjustments,
            budget=120,
            cap_per_node=15,
            soft_unlock_penalty_scale=SOFT_PENALTY_SCALE,
            tier_unlock_thresholds={2: 3, 3: 5, 4: 8}
        )
        
        # Scalar modifier nudge (small per-iteration)
        scalar_modifier *= (1 - 0.05 * sign(sum(per_tier_wr[t] - per_tier_targets[t])))
    
    return ConvergenceFailed(tree, sp_allocation, scalar_modifier, per_tier_wr)
```

### 4.4 Local optima escape

Standard hill-climbing gets stuck in local optima. Two safeguards:

1. **Soft-preference relaxation** (per § 4.1): eliminates the major source of optimization cliffs by smoothing hard tier-gates
2. **Random restart on stagnation** (per § 4.3 main loop): if no improvement for N iterations, restart from BC-target-biased random allocation

**Random restart bias:** restart isn't truly random; it biases toward allocations that respect BC-target requirements (e.g., if BC-target is "AOE-favored", restart biases SP toward AOE-contributing nodes per BC-axis-contribution tags).

This pattern is standard in mixed-integer optimization. Random restart frequency calibrated empirically (proposed: every 8-12 iterations without improvement).

---

## 5. The 4/5 convergence dimensions explicitly

### 5.1 Dimension 1 — Per-node SP allocation

- ~10-15 nodes per kit (varies by class shape)
- Integer SP per node, 0-15 cap (per canonical)
- Total budget 120 SP (per canonical)
- Soft-preference tier-unlock penalty (per § 4.1)
- This is the PRIMARY continuous-discrete tuning dimension

### 5.2 Dimension 2 — Tier-specific scaling coefficients

**Preserved as load-bearing (per § 2.3 + § 3.2):**
- Tier 1: 1.05-1.08 per rank
- Tier 2: 1.08-1.12 per rank
- Tier 3: 1.12-1.18 per rank
- Tier 4: 1.18-1.25 per rank

**Engine convergence treats coefficients as constants per the tier-specific range.** Per-skill VARIANCE within a tier's range (e.g., "this Tier-2 skill scales at 1.10 vs 1.08") DEFERRED to v2 for engineering scope reasons (UX polish; not math-load-bearing).

For v1: use tier-mid coefficient (1.065 / 1.10 / 1.15 / 1.215 per tier) uniformly across all skills at that tier.

### 5.3 Dimension 3 — Scalar kit modifier (existing knob)

- Continuous, ~0.05 to ~2.0 typical range (post-Option-A floor widening)
- Final-calibration adjustment after node-level SP optimization
- Small per-iteration nudge (5%) to fine-tune per-tier WR

### 5.4 Dimension 4 — Gear affix per-skill modifiers (provisional)

**Status:** PENDING W0.4 verification of gear architecture state.

If gear affixes directly modify skills (per Matt's late W0.4 question):
- Per-skill affix modifier vector `g` becomes a 4th convergence dimension
- Affix-to-skill pairing is generation-time decision; convergence selects optimal pairing
- Constraint: 1-3 affix slots per gear piece × ~6 gear pieces = ~12 affixes

If gear affixes only modify stats (not skills):
- This dimension collapses
- The 4-dim convergence becomes 3-dim
- Algorithm functions unchanged; just one fewer optimization variable

**v1 algorithm authored with `g` as optional dimension.** W0.4 verification result will inform whether to activate `g` or collapse it.

### 5.5 Dimension 5 — Legendary skill grants (deferred)

Per Matt 2026-05-21: legendary gear is supposed to come with a skill grant; mechanism may not yet be implemented (or fully designed).

**Disposition:** OUT OF W1.13 scope. Legendary skill mechanism is a separate workstream — design + implementation. Future state may add a 5th dimension; v1 algorithm does NOT include it.

---

## 6. Substrate-as-cohesion preservation (architectural test)

Per `canonical/story/substrate-design-supplement-2026-05-21.md`:

**Architectural test:** *"Does this design choice influence mechanical generation, or only thematic coalescence?"*

Multi-dim convergence operates on **MECHANICAL** dimensions only:
- Node selection (mechanical)
- SP allocation (mechanical)
- Tier-specific scaling (mechanical)
- Gear affix modifiers (mechanical)
- Scalar modifier (mechanical)

**Substrate identity (fire / water / shadow / etc.) does NOT enter the convergence algorithm.** Substrate-as-cohesion preserved:
- Chains are abstract mechanical clusters (e.g., "damage-amplification cluster") at generation
- Cohesion-judge themes the kit POST-generation based on selected node-subset signature + flavor (Phase 5 of workflow)

**Chain-naming clarification:**

Canonical fire-mage example uses chain names like "Combustion Chain" / "Heat Chain" / "Defensive Chain." Under substrate-as-cohesion:
- Chains have abstract mechanical IDs at generation (`chain_damage_amplification` / `chain_control_focused` / `chain_defensive`)
- Cohesion-judge themes them per-substrate POST-generation (a fire-themed kit gets "Combustion Chain" labeling; a shadow-themed kit gets "Soul Burn Chain" labeling)
- Same mechanical chain structure → different thematic labels per cohesion-judge inference

This preserves the existing canonical UX/story shape AND the substrate-as-cohesion architectural recommitment simultaneously.

---

## 7. Reference build output (first-class engine deliverable)

Every archive entry stores:

```yaml
ArchiveEntry:
  bc_coordinate: [Axis1..Axis5_bins]              # mechanical BC (8-axis)
  cohesion_coordinate: <substrate + element + theme>  # assigned at P5
  visual_coordinate: <visual-BC>                    # assigned at P6
  
  kit_specification:
    tree_seed: <class_seed_S>                      # for tree regeneration
    chains: [{id, depth, abstract_role}]           # chain structure
    nodes: [...]                                    # full node list (10-15)
    sp_allocation: {node_id: rank}                 # SP investment per node
    scalar_modifier: <float>                       # final calibration
    gear_affix_assignments: [...]                  # per-skill affix bindings (if applicable)
  
  per_tier_wr_outcomes: {swarm, magic, elite, mini_boss, boss}
  convergence_metadata: {iterations, restart_count, final_score}
```

**This `kit_specification` block IS the player-adoptable reference build.** Canonical ARPG build-guide pattern (D2 Hammerdin guides specify skill levels; D3 build templates specify 6 actives + 4 passives + rune choices; D4 build templates specify aspect choices + paragon glyphs).

**Profile A ships this content** — players see "the engine-discovered Hammerdin equivalent for this season" with explicit SP allocation + scalar modifier + gear preferences.

---

## 8. Scope decision documentation

### 8.1 Three scope options evaluated

| Scope | Description | Build cost | Convergence math | Thematic alignment | Cluster diversity |
|---|---|---|---|---|---|
| **A — Minimum viable** | N nodes × per-node SP × axis-tags | ~2-4 weeks | STRONG (smooth landscape) | WEAK (no archetypal structure) | WEAK (uniform-attractor risk) |
| **B — Full canonical** | Chain×tier×SP×gates×cross-rules×per-skill-coefficients | ~5-8 weeks | MEDIUM (non-smooth at gates) | STRONG (canon-shaped) | STRONG (specialist/generalist/keystone emergence) |
| **D — Hybrid (THIS SCOPE)** | Chain×tier×SP×soft-preferences×tier-coefficients-preserved | ~3-5 weeks | STRONG (soft preferences smooth landscape) | STRONG (canon-shaped) | STRONG (canonical archetype emergence) |

### 8.2 Scope D specifics — what's preserved, what's relaxed, what's deferred

**Preserved from canonical (load-bearing):**
- Chain count variance (2-4 chains per class)
- Tier depth variance (3-4 tiers per chain)
- Kit size 10-15 nodes
- 120 SP budget + per-skill cap 15
- **Tier-specific scaling coefficients (1.05-1.25 by tier)** — LOAD-BEARING per § 2.3
- Build pattern variants (specialist/generalist/keystone-rusher emerge from structure)

**Relaxed from canonical (math + engineering wins):**
- Hard tier-unlock gates 3/5/8 → soft-preference penalties (per § 4.1)
- UX still shows canonical hard gates; engine optimizes smoothly underneath

**Deferred from canonical (v2 polish):**
- Per-skill scaling coefficient variance within a tier (uniform tier-mid for v1)
- Cross-chain unlock asymmetry per element (multi-element retired post canonical-6 anyway)
- Smooth rank cap formula (use flat cap 15 for engine convergence; player-level scaling is post-Profile-A UX)

**Added for math (necessary):**
- Per-node BC-axis-contribution tags (§ 3.3 schema extension)
- WR-skew gradient mechanism (§ 4.2)
- Multi-tier voting algorithm (§ 4.3)
- Soft-preference tier-unlock handling (§ 4.1)
- Local optima escape (§ 4.4)

### 8.3 Matt's caveat — Scope D is starting structure, not final

**Per Matt 2026-05-21:**
> *"ARPG knowledge and related decisions may transform scope D beyond recognizability, but it is a good structure."*

Legolas ARPG-canon survey (fired 2026-05-21; ~1-2 days) may surface that canonical ARPG best-practice diverges meaningfully from current Reincarnated spec on:
- Chain count distributions
- Tier depth conventions
- Per-skill rank caps
- SP budget magnitudes
- Tier-scaling coefficient patterns
- Active slot conventions
- Unlock gate mechanisms

**If legolas surfaces structural divergence,** this math note becomes v1.1 with Scope D refined per canon best-practice. The ALGORITHM (§ 4) is robust to specific parameter shifts; the STRUCTURAL shape may pivot.

**Possible Scope D transformations:**

| Possible legolas finding | Possible Scope D revision |
|---|---|
| Canon converges on 5-7 chains per class | Increase Reincarnated chain count from 2-4 |
| Canon uses level-based gating (not rank-based) | Replace 3/5/8 gates with character-level gating |
| Canon uses 1.10-1.15 per-tier scaling uniformly | Revise tier-coefficient curve flatter |
| Canon uses 60-80 SP budget | Reduce budget; force more focused builds |
| Canon uses per-skill cap 20-30 | Increase cap; allow deeper keystone investment |
| Canon allows multiclassing or paragon-style endgame | Add 5th convergence dimension for paragon-equivalent |

**v1 STANDS regardless of legolas outcome.** Knight-rider can fire W1.13 implementation against v1 if P1 opens before research returns. v1.1 amendment folds in mid-flight if needed.

---

## 9. Implementation guidance for W1.13 specialist (rocket)

### 9.1 What gets built in P1 W1.13

**Substrate generation (substrate-agnostic):**
- Per-class-per-season skill tree generation function
- Tree topology: 2-4 chains × 3-4 tiers × ~10-15 total nodes per kit
- Per-node abstract mechanic class assignment (damage/control/defense/mobility/utility)
- Per-node BC-axis-contribution tagging (5 floats per node)
- Tier-specific coefficient assignment per node (per § 5.2)

**Convergence algorithm:**
- WR-skew gradient mechanism (§ 4.2)
- Multi-tier voting per-iteration (§ 4.3)
- Soft-preference tier-unlock penalty (§ 4.1)
- Local optima escape via random restart (§ 4.4)
- Budget + cap + topology constraint enforcement

**Telemetry instrumentation:**
- Per-iteration WR deltas + adjustment vectors
- Convergence iteration count per kit
- Escape restart count per kit
- Final SP allocation + scalar modifier per archive entry

**Reference build output:**
- Archive entry kit_specification block (per § 7)

### 9.2 What this work does NOT include

- Legendary skill grant mechanism (separate workstream; deferred)
- Per-skill scaling coefficient variance within a tier (v2)
- Cross-chain unlock asymmetry per element (post canonical-6 multi-element retired)
- Smooth rank cap formula (UX-side; not engine-side)
- Spirit Guide build-coach UI (Stage A3 territory)
- Player-facing skill tree UI changes (B6 work; demo-side)

### 9.3 Verification approach

Smoke tests + Discipline #17 calibration:

1. **Unit tests:**
   - WR-skew gradient computes correct direction on synthetic per-tier deltas
   - Multi-tier voting respects budget conservation
   - Soft-preference penalty produces 80-95% canonical-gate-respecting solutions
   - Local optima escape triggers on stagnation (N iterations without improvement)

2. **Integration tests:**
   - End-to-end convergence on 5-10 representative test kits (one per substrate)
   - Per-tier WR convergence within contract bounds for 80%+ of test kits
   - Convergence iteration count median <20

3. **Empirical validation:**
   - Re-run Track C-style same-calibration ablation across all 7 substrates
   - Predict: low-modifier kits previously at 0.000 boss WR exit zero-floor via keystone-concentration
   - Pattern-A 100% → expected ~10-30% post-W1.13 (residual due to BC-target-mismatched kit attempts; expected)

### 9.4 Critique-pair structure

- **gandalf reviews architectural alignment** (substrate-as-cohesion preservation; reference build completeness; ARPG-canon thematic anchor strength)
- **jack-ryan reviews implementation correctness** (BC-axis-contribution tagging integrity; coefficient curve sensibility; topology constraint enforcement; #13a drift check)
- **Matt approves W1.13 framing** before implementation fires (NEW scope from protocol v1.1)

---

## 10. Critical math-before-code gate (per Discipline #1)

Before W1.13 implementation begins, the following math must be settled:

1. **`penalty_scale` value** for soft-preference tier-unlock (§ 4.1) — empirical calibration target: 80-95% canonical-gate respecting
2. **`T_AXIS_SENS` matrix values** (§ 4.2) — tier-axis sensitivity weights — pending legolas research input + empirical telemetry
3. **`VOTE_THRESHOLD` value** (§ 4.3) — minimum vote magnitude to trigger SP adjustment
4. **`ESCAPE_THRESHOLD` value** (§ 4.4) — iterations without improvement before restart
5. **Initial `sp_allocation` distribution** — bias toward BC-target via axis-contribution matching; uniform vs concentrated initialization
6. **`MAX_ITER` budget** — per-kit convergence iteration cap; balance against per-archive-cell budget at scale

These are all empirically calibratable; v1 algorithm provides skeleton; specific values land via Discipline #17 calibration sweeps during W1.13 implementation.

---

## 11. Open questions for legolas research + W0.4 verification

### 11.1 Pending legolas research (fired 2026-05-21; ~1-2 days)

Per dispatch `2026-05-21-legolas-arpg-skill-architecture-canon-survey.md`, awaiting:
1. Per-skill rank caps across genre
2. Total SP budgets
3. Tier-scaling coefficient patterns
4. Chain count + depth distributions
5. Per-class active-skill counts
6. Investment gate mechanisms
7. Keystone vs spreading patterns
8. Synergy mechanisms
9. Stat / trait integration
10. Endgame progression mechanisms

**Expected v1.1 amendment scope:** parameter value refinements + potential Scope D structural pivot if research surfaces canon-divergence.

### 11.2 Pending W0.4 verification (gear affix architecture state)

- Do gear affixes directly modify skills, or only modify stats?
- Is legendary tier item generation operational?
- Is legendary-skill-grant mechanism implemented OR designed?

**Math note v1 treats gear affix dimension as PROVISIONAL.** If W0.4 confirms gear affixes are skill-modifier-capable, dimension 4 activates. Otherwise, dimension 4 collapses.

### 11.3 Spec gaps surfaced during this authoring

- BC-axis-contribution tagging schema (§ 3.3) needs implementation review — does the engine currently support per-node metadata extensions?
- Tier-axis sensitivity matrix `T_AXIS_SENS` — initial values from gandalf white-wizard intuition; needs legolas calibration
- Substrate identity propagation — confirmed substrate-AGNOSTIC at generation per § 6; rocket confirms in implementation

---

## 12. Cross-references

- **Empirical foundation:**
  - `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md`
  - `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md`
  - `reincarnated-engine/src/reincarnated/simulation/math/w0-10-boss-ai-leash-reset-fix.md`

- **Architectural foundation:**
  - `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md`
  - `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
  - `canonical/story/substrate-design-supplement-2026-05-21.md`
  - `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md`

- **Reincarnated canonical UX/story spec:**
  - `canonical/32-progression-design.md`
  - `canonical/33-progression-skeleton.md`
  - `canonical/story/b6-skill-tree-ui-scoping.md`

- **Active commissions:**
  - `agentic_orchestration/dispatches/2026-05-21-legolas-arpg-skill-architecture-canon-survey.md`

- **Engineering disciplines:**
  - `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code (this doc instantiates); #11.1 state-space conditioning; #13a drift detection; #17 empirical calibration; #18 joint-gate candidate

---

## 13. Maintenance and revision protocol

### 13.1 Versioning

- **v1 (this doc):** initial spec with white-wizard intuition + canonical structure preservation + math layer
- **v1.1:** post-legolas-research amendment (parameter values; possible Scope D structural pivot)
- **v1.X:** minor refinements during W1.13 implementation
- **v2:** post-Profile-A-ship enhancement (per-skill scaling variance + cross-chain rules if multi-element returns)

### 13.2 Authoring authority

- **gandalf** authors revisions
- **Matt approves** structural changes (Scope D pivots)
- **knight-rider** drafts decisions-log entries
- **jack-ryan** reviews against existing decisions and disciplines

### 13.3 Living-document conventions

Algorithm specification is locked at v1; specific parameter values are calibratable. Empirical-calibration findings from W1.13 implementation may surface refinements that update v1.X.

---

## 14. Closing — the wizard reads

**This math note operationalizes the architectural commitment Matt and gandalf developed during 2026-05-21.** The multi-dim convergence algorithm is the empirically-mandated fix for the boss-floor pathology that arena-side fixes (W0.9 + W0.10) couldn't fully address for low-modifier kits.

**Scope D is the pragmatic engineering-aware target** — preserves what's load-bearing for math (tier-specific scaling), preserves what's load-bearing for thematic + diversity (chain × tier shape), relaxes what creates optimization cliffs (hard gates → soft preferences), defers what's UX polish (per-skill variance).

**Matt's caveat is honored:** Scope D is starting structure. Legolas ARPG-canon survey may transform it beyond recognizability. The ALGORITHM is robust to parameter shifts; the STRUCTURAL shape may pivot.

**The architectural decoupling is preserved:** substrate identity coalesces post-mechanical-generation per substrate-as-cohesion architecture; convergence operates on mechanical dimensions only; cohesion-judge themes the resulting kit signature.

**The W1.13 specialist (rocket) has a starting spec.** When P1 opens, knight-rider fires W1.13 implementation against this v1 — amended to v1.1 post-legolas-research if needed.

**The road continues to be walked correctly.**

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine's mathematical heart, made explicit before P1 W1.13 fires.
