# Multi-Dim Convergence Algorithm — QD-Engine W1.13 Architectural Spec

**Status:** v1.1 — amended 2026-05-21 with legolas ARPG-canon survey findings + Matt-flagged Tier 1 playability constraint + Q4 substrate-availability framing + procedural-seasonal-arc deliberate-departure framing
**v1 history:** v1 authored 2026-05-21; legolas commission concurrent (per `agentic_orchestration/dispatches/2026-05-21-legolas-arpg-skill-architecture-canon-survey.md`); v1.1 folds 8 amendment areas
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
- `agentic_orchestration/legolas/research/arpg-skill-architecture-canon-survey-2026-05-21/` — ARPG canon survey informing v1.1 parameter choices

---

## v1.1 amendment summary

Eight amendments fold legolas ARPG-canon research + Matt-flagged constraints + Q4 substrate framing into v1:

| # | Amendment | Priority | Source |
|---|---|---|---|
| 1 | Tier 4 nodes = mechanic-altering keystones (NOT pure-scaling rewards) | HIGH | legolas SD-1 |
| 2 | Trigger/conditional interaction layer added (1-2 per chain) | HIGH | legolas SD-3 |
| 3 | **Tier 1 cost/cooldown playability constraint** (NEW — chains must start with L1-playable skills) | HIGH | Matt 2026-05-21 |
| 4 | Soft-preference gate values 3/5/8 → 2/4/7 (canon-aligned; keystone-rusher enablement) | MEDIUM | legolas SD-2 |
| 5 | Active skill slot cap 5-8 → 5-6 (mobile-first canon) | LOW | legolas SD-4 |
| 6 | Endgame tuning surface departure acknowledged explicitly | LOW | legolas SD-5 |
| 7 | Q4 substrate-availability framing — current state + P1 closure path | INFO | session synthesis |
| 8 | Reincarnated's 10-15 nodes + 2-4 chains as v1 STARTING STATE (substrate-availability-driven) with v2 CANONICAL-PARITY EXPANSION TARGET (24-30 nodes / 3-5 chains post-Profile-A-ship per Matt 2026-05-21 late-amendment) | INFO | Matt 2026-05-21 late clarification |

---

## 0. TL;DR

**The empirical mandate:** Track C synthesis (2026-05-21) + W0.10 re-sweep (2026-05-21) confirmed that boss-tier WR convergence is mathematically underdetermined under scalar-modifier-only optimization. Low-modifier kits (≤0.33) cannot escape boss-zero floor via parametric tuning of existing flat-skill kits.

**The architectural fix:** procedural skill tree node population per class per season + multi-dim convergence over per-node SP allocation × Tier-4 mechanic-altering keystone selection × trigger/conditional interaction selection × tier-specific scaling × scalar modifier × gear affix modifiers (5-6 dimensions instead of 1).

**The scope target — Scope D-refined (post-legolas):** 
- Preserves canonical chain × tier shape + 120 SP budget + per-skill cap 15 (all canon-aligned)
- **Tier 1 nodes MUST be playable at L1** (low cost + low cooldown — canonical ARPG design pattern; Matt 2026-05-21)
- Tier 4 nodes are **MECHANIC-ALTERING keystones** (qualitative regime changes, not scaling-amplification — canonical ARPG fun pattern per legolas SD-1)
- **Trigger/conditional interaction layer ADDED** — 1-2 trigger nodes per chain producing multiplicative scaling above additive (legolas SD-3 closure)
- Hard tier-unlock gates relaxed to soft preferences (math + engineering wins); gate values 2/4/7 (canon-aligned per legolas SD-2)
- Active slot cap 5-6 (mobile-friendly per legolas SD-4)
- Per-skill scaling variance + cross-chain rules deferred to v2
- Tier-specific scaling coefficients PRESERVED for ranks within chosen Tier 4 keystones

**Important framing (Matt 2026-05-21, refined late-amendment):** Reincarnated's 10-15 nodes + 2-4 chains is v1 STARTING STATE — below the canonical 24-30 / 3-5 ARPG median. This is current-state due to substrate availability (number of classes + number of skills currently in catalog), NOT a final design target. **v2 work post-Profile-A-ship will plan canonical-parity expansion (target: 24-30 nodes / 3-5 chains) as substrate grows.** Reincarnated DOES aspire to canonical ARPG depth at endgame; v1 scales as substrate grows.

**Q4 substrate-availability framing:** current engine has substrate gaps across 4 of 7 BC axes per legolas Phase 1 audit. P1 substrate enrichment (W1.1-W1.6 + W1.11) closes the gaps to support ~168+ unique skill templates per season — gate for W1.13 implementation start.

**Critical algorithm components (unchanged from v1):**
- WR-skew gradient: per-tier WR-delta drives per-node SP adjustment direction
- Multi-tier voting: 5 tiers vote on per-node SP changes proportional to wr_delta × node-contribution
- Soft-preference tier-unlocks: UX shows canonical gates; engine optimizes smoothly underneath
- Local optima escape: random restart on stagnation
- Substrate-as-cohesion: nodes are substrate-AGNOSTIC at generation; cohesion-judge themes post-generation

---

## 1. Provenance and the ARPG-canon-research caveat

### 1.1 Document genesis

This math note emerged from an extended session between Matt and gandalf 2026-05-21 covering:

1. The 5-6-dimensional convergence problem framing (post-legolas extension from 4-dim)
2. The architectural choice between minimum-viable scope (A), full canonical scope (B), and hybrid Scope D
3. Per-tier scaling coefficient preservation (load-bearing for math; concern 1)
4. ARPG-canon research scope (concern 2 — legolas commission)
5. Tier 1 playability constraint (Matt 2026-05-21)
6. Substrate availability validation (Q4)

Matt's explicit caveat (2026-05-21):
> *"ARPG knowledge and related decisions may transform scope D beyond recognizability, but it is a good structure."*

**Post-legolas reality:** Scope D's structural shape stands (canonical-aligned); ALGORITHM gets meaningful enhancement (Tier 4 mechanic-altering + trigger interaction layer); PARAMETER VALUES validated (mostly within canon; some refinements).

### 1.2 The empirical foundation — why this work matters

The recompose-hive findings (2026-05-19/20) + Track C synthesis (2026-05-21) + W0.10 re-sweep (2026-05-21) jointly establish:

- **Pattern-A is universal at boss tier under scalar-modifier-only optimization** (100% Pattern-A across all 7 substrates at same calibration; Track C)
- **The arena-side fix (W0.9 + W0.10) discharges the HIGH-modifier band** (≥0.64) — physical_grappler + hunter both boss_wr 0.000→1.000 post-fix
- **The LOW-modifier band (≤0.33) remains at 0.000** — modifier-scaling gap requires multi-dim convergence (P1 W1.13 mandate)

This document specifies the algorithm that addresses the low-modifier residual.

### 1.3 The ARPG-canon validation (post-legolas)

Per `agentic_orchestration/legolas/research/arpg-skill-architecture-canon-survey-2026-05-21/`:

**Validated canonical-aligned parameters (no change needed):**
- 120 SP budget — squarely canonical (PoE ~121-127 closest)
- Per-skill cap 15 — matches D4; below D2/PoE/LE median of 20 but defensible for shorter-arc game
- Tier-specific scaling per rank (1.05→1.25) — implicit-canonical pattern (D2 row-deeper-is-stronger; D4 Key Passive nodes; PoE keystone-distance-pays-off)

**Validated structurally distinct (deliberate departure):**
- 10-15 nodes per class design space — below 24-30 canonical median for classic ARPGs; closest to Diablo Immortal (mobile-first). **Deliberate procedural-seasonal-arc tuning per Reincarnated meta-architecture** (see § 8.3.1).
- 2-4 chains per class — below 3-5 canonical median; closest to D2 3-tab. **Deliberate procedural-seasonal-arc tuning** (see § 8.3.1).

**Refined parameters (legolas-recommended adjustments folded into v1.1):**
- Gate values: 3/5/8 → 2/4/7 (more canon-aligned; enables keystone-rusher build pattern)
- Active slot cap: 5-8 → 5-6 (mobile-first genre consensus)
- Tier 4 semantics: pure-scaling → mechanic-altering (canonical ARPG fun pattern)
- Synergy model: pure-additive → additive + 1-2 trigger nodes per chain (canonical multiplicative-interaction-layer)

---

## 2. The mathematical convergence problem (formalized)

### 2.1 Problem statement

**Given:**
- A per-class-per-season skill tree (~10-15 nodes; chains × tiers structure per Scope D-refined)
- A BC-cell target (8-axis coordinate)
- Per-tier WR contract: swarm 0.65-0.80; magic 0.55-0.70; elite 0.45-0.60; mini-boss 0.35-0.55; boss 0.30-0.45
- Game-loop simulation (true multi-monster spatial gauntlet per W0.9 + W0.10)
- Player-character stats + base damage + gear affixes available

**Find:**
- Per-node SP allocation (`sp_i` for each node `i`, integer 0-15 per cap)
- Tier 4 keystone selection per active chain (discrete; pick which mechanic-altering keystone)
- Trigger/conditional interaction selection (discrete; pick which 0-2 interactions per chain)
- Scalar kit modifier `m` (continuous)
- Gear affix modifier vector `g` (pending W0.4 verification of skill-modifier vs stat-only affix state)
- Subject to: `sum(sp_i) ≤ 120` (budget); per-node cap 15; soft tier-unlock preferences with gates 2/4/7; cross-chain rules; **Tier 1 nodes playable at L1 via low cost/cooldown constraint**
- Such that: per-tier WR within contract bounds AND BC coordinate matches target cell

**This is a mixed-integer-continuous optimization problem with discrete-categorical Tier-4-keystone + trigger-interaction selections, soft-preference constraints, and multi-objective output.**

### 2.2 The mathematical underdetermination of scalar-modifier-only optimization

Pre-W1.13, the convergence problem reduces to:
- Find scalar `m` such that 5 per-tier WR constraints are simultaneously satisfied
- 1 unknown vs 5 constraints → systematically underdetermined
- Result: scalar `m` either over-fits one tier and under-fits others (Pattern-A compression observed empirically)

Post-W1.13, the convergence problem has:
- ~10-15 per-node SP integers + Tier-4 keystone discrete selections per chain + 0-2 trigger interaction selections per chain + scalar `m` + gear affix vector `g`
- Total dimensionality: ~15-25+ optimization variables
- 5 per-tier WR constraints + per-cell BC matching = 5+ constraints
- Over-determined tuning surface → multi-tier WR contract satisfiable

**The dimensional shift is the architectural fix.**

### 2.3 Why tier-specific scaling coefficients are load-bearing (preserved from v1)

For low-modifier kits (e.g., fire_mage at modifier=0.10):

- Required boss DPS to clear in 240s: 53,216 HP / 240s = 222 HP/s
- Under uniform scaling 1.10: rank-15 keystone = 4.18× multiplier. Result: 500 × 0.10 × 4.18 = 209 DPS. Marginal/insufficient.
- Under tier-specific scaling 1.25 (Tier-4 keystone): rank-15 keystone = 28.42× multiplier. Result: 500 × 0.10 × 28.42 = 1,421 DPS. Comfortable.

The 6.8× DPS spread between uniform-1.10 and tier-specific-1.25 IS the lever that makes low-modifier kits viable at boss tier through keystone concentration.

**Tier-specific scaling coefficients are LOAD-BEARING for the multi-dim convergence's boss-floor-fix promise.** Scope D-refined preserves them — applied to ranks 1-15 WITHIN a chosen Tier 4 mechanic-altering keystone (per Amendment 1).

---

## 3. Existing canonical structure (preserved + refined)

Per `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` + Matt 2026-05-21 amendments:

### 3.1 Structural shape

- **Chain count per class**: 2-4 chains (variance allowed)
  - Specialists: 2 chains × 4 tiers = ~8 skills (deep mastery)
  - Balanced: 3 chains × 4 tiers = ~12 skills (default)
  - Generalists: 4 chains × 3 tiers = ~12 skills (wide options)
  - Asymmetric: 1 chain × 4 tiers + 2 chains × 3 tiers = 10 skills (focused with options)

- **Kit size**: 10-15 nodes per class (B9 endgame baseline; deliberate procedural-seasonal-arc tuning per § 8.3.1)
- **SP budget**: 120 (B9 endgame; level 50; canon-aligned)
- **Per-skill cap**: `min(15, floor(level/3.33))` — endgame cap = 15 (canon-aligned with D4)
- **Cross-chain rules**: single-element strict (same-chain unlock); multi-element flexible (retired post canonical-6)
- **Active skill slot cap**: 5-6 (refined from 5-8 per legolas SD-4 — mobile-first canonical consensus)

### 3.2 Investment gates (soft-preference; canon-refined values)

**v1.1 refinement per legolas SD-2:** gate values shifted from 3/5/8 to 2/4/7 (canon-aligned; enables keystone-rusher build pattern per canonical/32 § 8.3 build pattern recognition).

| Tier | Unlock requirement (v1.1) | Previous v1 |
|---|---|---|
| Tier 1 | Available from L1 (always) | unchanged |
| Tier 2 | ≥2 ranks in any Tier 1 parent | was ≥3 |
| Tier 3 | ≥4 ranks in any Tier 2 parent | was ≥5 |
| Tier 4 (keystone) | ≥7 ranks in any Tier 3 parent | was ≥8 |

**Engine interpretation (per § 4.1):** soft-preference penalty in convergence optimizer. UX displays as canonical hard-gate visual. Engine convergence can accept solutions slightly below gates if WR contract demands.

**Why soften:** D2's 1-point prereq is permissive; D4 uses level-gates; PoE has no explicit investment gate. 3/5/8 is steeper than the entire canon. 2/4/7 is closer to canon while preserving meaningful per-chain commitment.

### 3.3 Tier-specific design constraints (with NEW Tier 1 playability constraint per Matt 2026-05-21)

| Tier | Scaling coefficient (per-rank power gain) | NEW: cost / cooldown / playability constraint |
|---|---|---|
| **Tier 1 (primary)** | 1.05-1.08 | **MUST be playable at L1: low resource cost, short cooldown (≤2s typical), spammable, no prerequisite** — canonical ARPG pattern (D2 Spark/Frost Bolt; D3 Generator skills; D4 Basic cluster; PoE starter gems; LE basic attack skills) |
| Tier 2 (mid) | 1.08-1.12 | Moderate resource cost; medium cooldown (3-8s typical); unlocked at ≥2 Tier-1 ranks; mainline rotation skill |
| Tier 3 (advanced) | 1.12-1.18 | Higher resource cost; longer cooldown (8-20s typical); unlocked at ≥4 Tier-2 ranks; build-significant skill |
| **Tier 4 (keystone)** | **Variable coefficient 1.18-1.25 PLUS qualitative-regime-change effect** | High cost or unique resource mechanic; long cooldown (20-60s typical) OR specialized mechanic; unlocked at ≥7 Tier-3 ranks; **MECHANIC-ALTERING build-defining payoff (Amendment 1; per legolas SD-1)** |

**Why Tier 1 playability matters:** every ARPG ensures starter skills are immediately usable — players can't engage the game without spammable basics. Cosmetically equivalent to: D2 row-1 skills at L1; D3 Generator slot; D4 Basic cluster. **Generation MUST enforce: each chain has at least 1 node with `cost ≤ low_threshold` AND `cooldown ≤ 2.0s` placed at Tier 1.**

### 3.4 Tier 4 nodes — MECHANIC-ALTERING semantics (v1.1 Amendment 1 per legolas SD-1)

**Pre-v1.1 implicit framing:** Tier 4 nodes were "high-coefficient scaling rewards" (1.18-1.25 per rank).

**v1.1 correction:** Tier 4 nodes are **QUALITATIVE regime-change keystones**, not pure scaling. Per legolas SD-1: every high-rated ARPG produces build diversity through mechanic-altering keystones, not coefficient-amplification rewards.

**Canonical Tier 4 examples (from legolas survey):**
- PoE *Blood Magic*: removes mana entirely, skills cost HP — fundamental resource model change
- PoE *Resolute Technique*: 100% hit chance, no crits — accuracy/damage trade redefined
- D3 *Tempest Rush — Run-and-Punch rune*: ground effect targets instead of self — geometry redefined
- D4 *Lord of Hatred Diamond variant*: skill behavior transformation
- Last Epoch *Fire Wall persistent variant*: temporal regime change

**Reincarnated Tier 4 examples (provisional; W1.13 generation produces season-specific):**
- "Vampiric Strike" — convert 30% of damage dealt to HP (resource-model alteration)
- "Glacial Cascade" — frost spells now apply chain-freeze (geometry alteration)
- "Berserker's Hunger" — base damage scales with missing HP percentage (resource-coupling alteration)
- "Aegis Inversion" — defensive stats become offensive (axis-domain alteration)

**Algorithmic treatment:** Tier 4 keystone selection is a **DISCRETE CATEGORICAL choice** per chain (pick which keystone if any is invested in this chain). Coefficient scaling 1.18-1.25 applies to ranks 1-15 WITHIN a chosen Tier 4 keystone — but the BUILD IDENTITY comes from WHICH keystone is chosen, not from rank investment alone.

### 3.5 Trigger/conditional interaction nodes (v1.1 Amendment 2 per legolas SD-3)

**Pre-v1.1 implicit assumption:** convergence operates purely on additive scaling across nodes.

**v1.1 correction:** Add **1-2 trigger/conditional interaction nodes per chain** as a new node category that produces multiplicative scaling above additive. Per legolas SD-3: every high-rated ARPG has at least one multiplicative-interaction layer above additive stacking; without it, build diversity is fundamentally limited.

**Canonical trigger-interaction examples (from legolas survey):**
- PoE support gems (multiplicative via 6-link socket)
- D3 set 6-piece bonuses (trigger-conditional: "when X happens, Y triggers")
- D4 Legendary Aspects (gear-layer behavior modification)
- Grim Dawn Devotion celestial powers (trigger-bound to skills)
- Last Epoch per-skill tree multiplicative scaling

**Reincarnated trigger-interaction examples (provisional):**
- "Chain Reaction" — when [Skill A in this chain] is cast, [Skill B in another chain] deals +25% damage for 5s
- "Resonance Cascade" — every Nth cast of [Skill A], [Skill B's] resource cost is reduced by Y%
- "Tactical Retreat" — when player HP drops below 30%, [defensive ability] auto-triggers with refunded cost
- "Elemental Bond" — when two element-tagged skills cast within 2s, both gain +X% damage

**Algorithmic treatment:** trigger interaction selection is a **DISCRETE CATEGORICAL choice** per chain (0-2 trigger nodes activated per chain). Each interaction has prerequisite SP investment in the connected skill(s). Convergence optimizer treats this as a 5th tuning dimension (per § 5.5).

### 3.6 Per-node schema fields (existing canonical + v1.1 extensions)

Per canonical/32 + B6 templates Stage A1 + v1.1 additions:

**Existing schema fields (canonical):**
- `id` — node identifier
- `tier` — 1-4
- `chain_id` — chain affiliation
- `chain_position` — position within chain
- `parent_skill_ids` — prerequisite chain
- `scaling_coefficient` — per-skill scaling value (within tier's range)

**v1 schema extensions (BC-axis-contribution tagging):**
- `bc_axis_contribution_tags`: dict of axis_id → contribution weight (for gradient signal)
  - axis_1_engagement, axis_2_geometry, axis_2A_proxy, axis_2B_control, axis_3A_tempo, axis_3B_variance, axis_4_defensive, axis_5_economy

**v1.1 schema extensions (NEW):**
- `node_type`: enum {`rank_scaling`, `mechanic_altering_keystone`, `trigger_conditional`} — distinguishes node category per Amendments 1+2
- `cost`: resource cost — REQUIRED for Tier 1 playability check per Amendment 3
- `cooldown_seconds`: skill cooldown — REQUIRED for Tier 1 playability check per Amendment 3
- `playable_at_level_1`: bool — derived (true iff cost ≤ L1_cost_budget AND cooldown ≤ 2.0s AND tier == 1)
- `interaction_metadata` (for trigger_conditional nodes only):
  - `trigger_condition`: string describing the trigger (e.g., "skill_a_cast", "low_hp_threshold")
  - `target_node_ids`: list of nodes the interaction affects
  - `effect_multiplier`: float (multiplicative scaling magnitude)
  - `duration_seconds`: float (if temporal)
- `keystone_effect` (for mechanic_altering_keystone nodes only):
  - `effect_class`: enum {`resource_alteration`, `geometry_alteration`, `temporal_alteration`, `axis_domain_alteration`, `synergy_alteration`}
  - `effect_description`: string (LLM-generated cohesion-themed description)

These extensions enable Generation + Cohesion-judge + Convergence all to operate on a unified per-node specification.

---

## 4. The math layer (NEW — what this document adds)

### 4.1 Soft-preference tier-unlock handling (v1.1 with refined gate values 2/4/7)

**Canonical UX gates (hard thresholds; v1.1 refined values):**
- Tier 2 unlocks at ≥2 ranks in any Tier 1 parent skill
- Tier 3 unlocks at ≥4 ranks in any Tier 2 parent skill
- Tier 4 unlocks at ≥7 ranks in any Tier 3 parent skill

**Math-side relaxation (soft preferences):**

Instead of hard binary gates, the convergence cost function applies a **soft penalty** for under-investment in prerequisite tiers:

```
soft_unlock_penalty(node, sp_allocation) =
    if node.tier == 1:
        0  (no prerequisite; always L1-playable per Amendment 3)
    elif node.tier == 2:
        max(0, 2 - max(prereq_rank)) × penalty_scale
    elif node.tier == 3:
        max(0, 4 - max(prereq_rank)) × penalty_scale
    elif node.tier == 4:
        max(0, 7 - max(prereq_rank)) × penalty_scale
```

Where `penalty_scale` is calibrated such that:
- Hard-gated behavior emerges if penalty_scale → ∞ (canonical UX feel)
- Smooth optimization emerges if penalty_scale → 0 (engineering ease)
- **Calibration target: penalty_scale produces ~80-95% of optimal solutions respecting canonical gates, with 5-20% allowed boundary-flexibility for convergence smoothness**

**Player-facing UX impact:** ZERO. The UI continues to show canonical hard gates. The engine's convergence optimizer operates underneath on the smooth landscape; the resulting kits land 95%+ within canonical gate constraints.

**Why 2/4/7 vs 3/5/8 (per legolas SD-2):** D2 uses 1-point prereq (permissive); D4 uses level-gates (no investment gate); PoE has no explicit investment gate. 3/5/8 was steeper than the canon's most-strict pattern. 2/4/7 is closer to canon while preserving meaningful per-chain commitment AND enabling the canonical "keystone-rusher" build pattern explicitly named in canonical/32 § 8.3.

**Budget math at 2/4/7:** minimum 2+4+7 = 13 SP invested across one chain to reach Tier 4 keystone. Leaves 107 SP for the rest of the kit. Permissive — enables rushing to one Tier-4 keystone early while spreading the remainder; matches D2 keystone-rusher feel.

### 4.2 WR-skew gradient mechanism (unchanged from v1)

**Core insight:** per-tier WR-delta from target IS the gradient signal direction.

For each tier T in {swarm, magic, elite, mini_boss, boss}:
```
wr_delta[T] = measured_wr[T] - target_wr[T]
```

If `wr_delta[T] > 0`: tier T is over-performing → reduce SP in nodes that contribute to tier T's performance
If `wr_delta[T] < 0`: tier T is under-performing → increase SP in nodes that contribute to tier T's performance
If `wr_delta[T] ≈ 0`: tier T is at target → preserve current SP in tier-T-contributors

**Per-tier contribution attribution:**

Each node has BC-axis-contribution tags (per § 3.6). Each TIER of the WR contract is more sensitive to specific BC axes:

| Tier | Most-sensitive BC axes | Why |
|---|---|---|
| Swarm | Axis 2 (geometry: AOE-favoring), Axis 3A (tempo) | Many entities; AOE damage is force-multiplier |
| Magic | Axis 2 (geometry: small/large-AOE balanced), Axis 4 (defensive) | Mid-density; survivability matters |
| Elite | Axis 4 (defensive), Axis 3A (tempo), Axis 2 (geometry) | Sustained engagement; defense + sustained damage |
| Mini-boss | Axis 3B (variance: spike-favoring), Axis 4 (defensive), Axis 5 (economy) | Burst windows matter; resource economy under pressure |
| Boss | Axis 3B (variance: spike-favoring), Axis 4 (defensive) | Single target; burst damage; survivability |

**This tier-axis sensitivity matrix (T_AXIS_SENS[T][axis]) is calibrated against ARPG-canon + empirical telemetry. Specific values calibrated per legolas survey input + Discipline #17 empirical sweeps.**

### 4.3 Multi-tier voting algorithm (v1.1 with discrete-categorical Tier 4 + trigger selections)

Pseudocode (extends v1 with discrete categorical selections per Amendments 1+2):

```python
def multi_tier_voting_adjustment(kit, tier_wr_deltas, tier_axis_sensitivity, tree):
    """
    Compute per-node SP adjustments + Tier 4 keystone selection + trigger interaction selection
    from multi-tier WR deltas. Returns updated kit state respecting budget conservation.
    """
    # Phase 1: continuous SP adjustments (per v1)
    votes = {node.id: 0.0 for node in tree.rank_scaling_nodes}
    
    for tier in [swarm, magic, elite, mini_boss, boss]:
        wr_delta = tier_wr_deltas[tier]
        sensitivity = tier_axis_sensitivity[tier]
        
        for node in tree.rank_scaling_nodes:
            tier_contribution = sum(
                node.bc_axis_contribution_tags[axis_id] * sensitivity[axis_id]
                for axis_id in sensitivity
            )
            votes[node.id] += -wr_delta * tier_contribution
    
    # Normalize for budget conservation
    sp_adjustments = normalize_votes_to_integer_adjustments(votes, budget=120)
    
    # Phase 2: Tier 4 keystone discrete selection (NEW per Amendment 1)
    for chain in tree.chains:
        if chain.has_tier_4_investment:
            current_keystone = chain.tier_4_selection
            keystone_candidates = chain.available_tier_4_keystones
            
            # Evaluate each candidate against current per-tier WR profile
            best_keystone = current_keystone
            best_score = score_keystone_fit(current_keystone, tier_wr_deltas, kit)
            
            for candidate in keystone_candidates:
                if candidate == current_keystone:
                    continue
                hypothetical_score = score_keystone_fit(candidate, tier_wr_deltas, kit)
                if hypothetical_score > best_score:
                    best_score = hypothetical_score
                    best_keystone = candidate
            
            if best_keystone != current_keystone:
                kit.update_tier_4_selection(chain, best_keystone)
    
    # Phase 3: Trigger interaction discrete selection (NEW per Amendment 2)
    for chain in tree.chains:
        if chain.has_interaction_prerequisites_met:
            current_interactions = chain.active_trigger_interactions  # 0-2 per chain
            interaction_candidates = chain.available_trigger_interactions
            
            # Combinatorial selection: which 0-2 interactions activate
            best_interactions = current_interactions
            best_score = score_interaction_combination(current_interactions, tier_wr_deltas, kit)
            
            for candidate_combination in iter_combinations(interaction_candidates, max_size=2):
                if candidate_combination == current_interactions:
                    continue
                hypothetical_score = score_interaction_combination(candidate_combination, tier_wr_deltas, kit)
                if hypothetical_score > best_score:
                    best_score = hypothetical_score
                    best_interactions = candidate_combination
            
            if best_interactions != current_interactions:
                kit.update_trigger_interactions(chain, best_interactions)
    
    # Phase 4: enforce Tier 1 playability constraint (NEW per Amendment 3)
    for chain in tree.chains:
        if not chain.has_l1_playable_tier_1_node():
            # This is a generation-time invariant; should not fire at convergence-time
            # but enforced here as safety check
            raise ConvergenceInvariantViolation(f"Chain {chain.id} lacks L1-playable Tier 1 node")
    
    return kit
```

**Per-iteration loop (extends v1):**

```python
def multi_dim_converge(class_seed, bc_target, per_tier_targets, max_iter=50):
    tree = generate_tree(class_seed)  # per W1.13 substrate generation; respects Tier 1 playability
    kit = initialize_kit_with_bc_target_bias(tree, bc_target, budget=120)
    
    # Initial Tier 4 + trigger selections (discrete; from BC-target inference)
    kit.initial_tier_4_keystone_selections = infer_initial_keystones(tree, bc_target)
    kit.initial_trigger_interactions = infer_initial_interactions(tree, bc_target)
    
    scalar_modifier = 1.0
    no_improvement_count = 0
    best_score = float('inf')
    
    for iteration in range(max_iter):
        # Run gauntlet (W0.9 + W0.10 true multi-monster spatial)
        per_tier_wr = run_spatial_gauntlet(kit, scalar_modifier)
        
        # Check convergence
        if all_within_contract(per_tier_wr, per_tier_targets):
            return ConvergedKit(tree, kit, scalar_modifier, per_tier_wr)
        
        # Compute score for stagnation detection
        score = sum(abs(per_tier_wr[t] - per_tier_targets[t]) for t in tiers)
        if score < best_score - EPSILON:
            best_score = score
            no_improvement_count = 0
        else:
            no_improvement_count += 1
        
        # Escape local optimum if stagnant
        if no_improvement_count >= ESCAPE_THRESHOLD:
            kit = random_restart_with_bc_target_bias(tree, bc_target)
            scalar_modifier = 1.0
            no_improvement_count = 0
            continue
        
        # Apply multi-tier voting → SP + Tier 4 + trigger adjustments
        kit = multi_tier_voting_adjustment(
            kit=kit,
            tier_wr_deltas={t: per_tier_wr[t] - per_tier_targets[t] for t in tiers},
            tier_axis_sensitivity=T_AXIS_SENS,
            tree=tree
        )
        
        # Scalar modifier nudge
        scalar_modifier *= (1 - 0.05 * sign(sum(per_tier_wr[t] - per_tier_targets[t])))
    
    return ConvergenceFailed(tree, kit, scalar_modifier, per_tier_wr)
```

### 4.4 Local optima escape (unchanged from v1)

Standard hill-climbing gets stuck in local optima. Two safeguards:

1. **Soft-preference relaxation** (per § 4.1): eliminates the major source of optimization cliffs by smoothing hard tier-gates
2. **Random restart on stagnation** (per § 4.3 main loop): if no improvement for N iterations, restart from BC-target-biased random allocation; PRESERVES Tier 1 playability invariant + chain structure

**Random restart bias:** restart isn't truly random; it biases toward allocations that respect BC-target requirements (e.g., if BC-target is "AOE-favored", restart biases SP toward AOE-contributing nodes per BC-axis-contribution tags).

This pattern is standard in mixed-integer optimization. Random restart frequency calibrated empirically (proposed: every 8-12 iterations without improvement).

### 4.5 Trigger/conditional interaction nodes (NEW per Amendment 2, legolas SD-3)

**Definition:** A subset of tree nodes (1-2 per chain typical) are TRIGGER NODES with `node_type == "trigger_conditional"`. These don't accept rank investment in the same scaling-coefficient way; instead, they ACTIVATE (binary) when their prerequisite SP investment is met.

**Generation requirements:**
- Per-chain placement: 1-2 trigger nodes per chain, typically at Tier 2 or Tier 3 position
- Prerequisite SP investment: ~3-6 SP in connected skills to activate (modest commitment)
- Interaction targets: trigger affects 1-3 other nodes (within same chain or cross-chain)
- Multiplicative effect: typically 1.15-1.50× multiplier on target skills (canonical PoE support gem range)
- Cohesion-judge themes the interaction post-generation (e.g., "Soul Burn → activates when shadow skill X is cast; ignites target with X% bleed for 5s")

**Convergence treatment:**
- Trigger activation is BINARY (active or not)
- Multi-tier voting computes WR-delta impact of activation vs deactivation
- Best 0-2 trigger combinations per chain selected per iteration

**Build diversity impact:**
- Canonical PoE support gem pattern (multiplicative): exponential power from specific combinations → high build diversity
- Reincarnated's adaptation: per-chain trigger nodes preserve chain identity while providing multiplicative cross-skill interaction

**Example interaction flow:**
- Chain: Combustion damage chain
- Trigger: "Chain Reaction" — when Tier 2 Fireball cast, Tier 3 Inferno gains +30% damage for 8s
- Prerequisite: ≥3 SP in Fireball + ≥3 SP in Inferno → trigger activates
- Result: chains 'remember' player's recent casts; cross-skill multiplicative scaling emerges

### 4.6 Tier 1 playability enforcement (NEW per Amendment 3, Matt 2026-05-21)

**Generation invariant:** Each chain MUST contain at least one Tier 1 node with:
- `cost ≤ L1_resource_budget` (e.g., 30 mana for caster classes)
- `cooldown_seconds ≤ 2.0` (or instant-cast)
- `playable_at_level_1 == True` (no prerequisite gating)

**Generation enforcement (P1 W1.13):**
- Tree generator validates: `all(chain.has_l1_playable_tier_1_node() for chain in tree.chains)` before tree finalization
- Cost/cooldown bounds parametrized per class element (caster classes have higher resource budgets; martial classes have higher cooldown tolerance)

**Convergence safety check:** runtime safety check during convergence (should not fail if generation invariant holds; fails noisily if it does).

**Why this matters:**
- Canonical ARPG design: D2 Spark/Frost Bolt at L1; D3 Generator slot mandatory; D4 Basic skill cluster auto-active; PoE starter gems immediately usable
- Without this constraint, generated kits could be unusable at L1 (Tier 1 nodes too expensive/long-cooldown for starting character)
- Player experience: "I can play my character from level 1" is a non-negotiable canonical ARPG promise

---

## 5. The 5-dimensional convergence space (extends v1's 4-dim)

### 5.1 Dimension 1 — Per-node SP allocation (continuous)

- ~10-15 nodes per kit (varies by class shape)
- Integer SP per node, 0-15 cap (per canonical)
- Total budget 120 SP (per canonical)
- Soft-preference tier-unlock penalty (gates 2/4/7 per § 4.1)
- Tier 1 nodes always L1-playable (per § 4.6)
- This is the PRIMARY continuous-discrete tuning dimension

### 5.2 Dimension 2 — Tier 4 keystone selection (NEW: discrete categorical per Amendment 1)

**v1.1 refinement:** Tier 4 nodes are MECHANIC-ALTERING keystones, not pure-scaling rewards. Selection is discrete per chain.

- Per-class-per-season generation: ~3-5 Tier 4 keystone CANDIDATES per chain
- Convergence selects 0-1 per chain (pick which mechanic alteration is invested in)
- Within chosen keystone: ranks 1-15 with scaling coefficient 1.18-1.25 per rank (preserved from v1)
- Multi-tier voting Phase 2 (per § 4.3) evaluates keystone candidates against WR profile

**This is the build-defining choice that produces archetype identity** (per legolas SD-1 + canonical ARPG fun pattern).

### 5.3 Dimension 3 — Trigger/conditional interaction selection (NEW: discrete categorical per Amendment 2)

**v1.1 addition:** trigger interaction nodes per § 4.5.

- Per-chain: 1-2 trigger nodes available
- Convergence selects 0-2 per chain (which interactions to activate)
- Activation prerequisite: SP investment in connected skills (typically 3-6 SP)
- Multiplicative effect: ~1.15-1.50× on target skills
- Multi-tier voting Phase 3 (per § 4.3) evaluates interaction combinations

**This is the canonical multiplicative-interaction layer** (per legolas SD-3 + PoE support gem pattern + D3 set bonus pattern).

### 5.4 Dimension 4 — Tier-specific scaling coefficients (preserved from v1)

**Engine treats coefficients as constants per the tier-specific range.** Per-skill VARIANCE within a tier's range DEFERRED to v2 (UX polish; not math-load-bearing).

For v1.1: use tier-mid coefficient (1.065 / 1.10 / 1.15 / 1.215 per tier) uniformly across all skills at that tier. **Within a chosen Tier 4 keystone, ranks 1-15 use 1.215 coefficient.**

### 5.5 Dimension 5 — Scalar kit modifier (existing knob)

- Continuous, ~0.05 to ~2.0 typical range (post-Option-A floor widening)
- Final-calibration adjustment after node-level SP optimization + Tier 4 + trigger selections
- Small per-iteration nudge (5%) to fine-tune per-tier WR

### 5.6 Dimension 6 — Gear affix per-skill modifiers (PROVISIONAL pending W0.4)

**Status:** PENDING W0.4 verification of gear architecture state.

If gear affixes directly modify skills (per Matt's late W0.4 question):
- Per-skill affix modifier vector `g` becomes a 6th convergence dimension
- Affix-to-skill pairing is generation-time decision; convergence selects optimal pairing
- Constraint: 1-3 affix slots per gear piece × ~6 gear pieces = ~12 affixes

If gear affixes only modify stats (not skills):
- This dimension collapses
- The 6-dim convergence becomes 5-dim
- Algorithm functions unchanged; just one fewer optimization variable

**v1.1 algorithm authored with `g` as optional dimension.** W0.4 verification result will inform whether to activate `g` or collapse it.

### 5.7 Dimension 7 — Legendary skill grants (deferred)

Per Matt 2026-05-21: legendary gear is supposed to come with a skill grant; mechanism may not yet be implemented (or fully designed).

**Disposition:** OUT OF W1.13 scope. Legendary skill mechanism is a separate workstream — design + implementation. Future state may add a 7th dimension; v1.1 algorithm does NOT include it.

---

## 6. Substrate-as-cohesion preservation (architectural test)

Per `canonical/story/substrate-design-supplement-2026-05-21.md`:

**Architectural test:** *"Does this design choice influence mechanical generation, or only thematic coalescence?"*

Multi-dim convergence operates on **MECHANICAL** dimensions only:
- Node selection (mechanical)
- SP allocation (mechanical)
- Tier 4 keystone selection (mechanical regime-change; substrate-neutral)
- Trigger interaction selection (mechanical interaction; substrate-neutral)
- Tier-specific scaling (mechanical)
- Gear affix modifiers (mechanical)
- Scalar modifier (mechanical)

**Substrate identity (fire / water / shadow / etc.) does NOT enter the convergence algorithm.** Substrate-as-cohesion preserved:
- Chains are abstract mechanical clusters (e.g., "damage-amplification cluster") at generation
- Tier 4 keystones are abstract mechanic-altering effects (e.g., "resource alteration: HP-cost-for-power") at generation
- Trigger interactions are abstract multiplicative-conditional effects (e.g., "Tier-2-cast-triggers-Tier-3-boost") at generation
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
    tier_4_keystone_selections: {chain_id: keystone_id}  # NEW v1.1 — per-chain selection
    trigger_interaction_selections: {chain_id: [interaction_id, ...]}  # NEW v1.1 — per-chain
    scalar_modifier: <float>                       # final calibration
    gear_affix_assignments: [...]                  # per-skill affix bindings (if applicable)
  
  per_tier_wr_outcomes: {swarm, magic, elite, mini_boss, boss}
  convergence_metadata: {iterations, restart_count, final_score}
```

**This `kit_specification` block IS the player-adoptable reference build.** Canonical ARPG build-guide pattern (D2 Hammerdin guides specify skill levels; D3 build templates specify 6 actives + 4 passives + rune choices; D4 build templates specify aspect choices + paragon glyphs).

**Profile A ships this content** — players see "the engine-discovered Hammerdin equivalent for this season" with explicit SP allocation + Tier 4 keystone + trigger interactions + scalar modifier + gear preferences.

---

## 8. Scope decision documentation

### 8.1 Three scope options evaluated (refined post-legolas)

| Scope | Description | Build cost | Convergence math | Thematic alignment | Cluster diversity |
|---|---|---|---|---|---|
| **A — Minimum viable** | N nodes × per-node SP × axis-tags | ~2-4 weeks | STRONG (smooth landscape) | WEAK (no archetypal structure) | WEAK (uniform-attractor risk) |
| **B — Full canonical** | Chain×tier×SP×gates×cross-rules×per-skill-coefficients | ~5-8 weeks | MEDIUM (non-smooth at gates) | STRONG (canon-shaped) | STRONG (specialist/generalist/keystone emergence) |
| **D-refined (THIS SCOPE; v1.1)** | Chain×tier×SP×soft-preferences×Tier4-mechanic-altering×trigger-interaction×tier-coefficients-preserved×Tier1-playable | ~3-5 weeks | STRONG (soft preferences smooth landscape; categorical selections handled discretely) | STRONG (canon-shaped + canonical mechanic-altering Tier 4 + canonical trigger interactions) | STRONG (canonical archetype emergence + multiplicative-interaction diversity) |

### 8.2 Scope D-refined specifics — what's preserved, what's relaxed, what's deferred, what's NEW

**Preserved from canonical (load-bearing):**
- Chain count variance (2-4 chains per class)
- Tier depth variance (3-4 tiers per chain)
- Kit size 10-15 nodes
- 120 SP budget + per-skill cap 15
- **Tier-specific scaling coefficients (1.05-1.25 by tier)** — LOAD-BEARING per § 2.3
- Build pattern variants (specialist/generalist/keystone-rusher emerge from structure)

**Relaxed from canonical (math + engineering wins):**
- Hard tier-unlock gates 3/5/8 → soft-preference penalties with values 2/4/7 (per § 4.1)
- UX still shows canonical hard gates; engine optimizes smoothly underneath

**Deferred from canonical (v2 polish):**
- Per-skill scaling coefficient variance within a tier (uniform tier-mid for v1)
- Cross-chain unlock asymmetry per element (multi-element retired post canonical-6 anyway)
- Smooth rank cap formula (use flat cap 15 for engine convergence; player-level scaling is post-Profile-A UX)

**Added for math (necessary; v1 baseline):**
- Per-node BC-axis-contribution tags (§ 3.6 schema extension)
- WR-skew gradient mechanism (§ 4.2)
- Multi-tier voting algorithm (§ 4.3)
- Soft-preference tier-unlock handling (§ 4.1)
- Local optima escape (§ 4.4)

**Added in v1.1 (post-legolas + Matt-flagged):**
- **Tier 4 mechanic-altering keystones (Amendment 1; legolas SD-1)** — qualitative regime-change semantics, not pure scaling
- **Trigger/conditional interaction layer (Amendment 2; legolas SD-3)** — multiplicative scaling layer above additive
- **Tier 1 cost/cooldown playability constraint (Amendment 3; Matt 2026-05-21)** — canonical ARPG L1-playability invariant
- Gate refinement 3/5/8 → 2/4/7 (Amendment 4; legolas SD-2)
- Active slot cap tightened 5-8 → 5-6 (Amendment 5; legolas SD-4)
- Endgame tuning surface departure acknowledged explicitly (Amendment 6; legolas SD-5)

### 8.3 The v1 starting state vs v2 canonical-parity target (Amendment 8, REFINED per Matt 2026-05-21 late-amendment)

**Per legolas survey:** Reincarnated's 10-15 nodes per class + 2-4 chains is below the 24-30 / 3-5 canonical median for classic ARPGs.

**Per Matt 2026-05-21 (late v1.1 amendment clarification):**
> *"Note that we will return after we have more classes and more skills. Then we will plan to gain parity with AVG/Canonical skill tree depth."*

**This reframes Reincarnated's structural choice:**

**v1 starting state (current; this math note):**
- 10-15 nodes per class design space
- 2-4 chains per class
- **Current state determined by substrate availability** (number of generated classes + number of generated skill templates)
- W1.13 implementation operates on this v1 scope

**v2 canonical-parity target (post-Profile-A-ship; substrate-growth-gated):**
- Target: 24-30 nodes per class (canonical median)
- Target: 3-5 chains per class (canonical median)
- **Gated on substrate growth** — more classes generated + more skill templates in catalog enable wider design space per class
- v2 work scheduled post-Profile-A-ship (per § 8 + § 13.1)

**Why this matters:**

Reincarnated DOES aspire to canonical ARPG depth at endgame. The 10-15 / 2-4 v1 numbers are NOT a permanent design choice rejecting canon; they're a current-state-reflects-current-substrate decision that scales toward canonical parity as substrate grows.

**The canonical ARPG patterns that v2 will enable:**
- "Maxed 3 keystones; rest at 1-3 points" investment pattern (canonical D2 specialization feel)
- Build-identity-per-character is rich AND build-variety-per-meta-game is rich (vs v1 where per-meta-game richness substitutes for per-character depth)
- Specialist deep-chain vs generalist wide-multi-chain vs keystone-rusher patterns all viable at expanded scope

**The hybrid arc (v1 → v2):**

- **v1 (current):** 10-15 nodes × 2-4 chains; player invests broadly; per-meta-game variety carries
- **v2 (future):** 24-30 nodes × 3-5 chains; player invests narrowly; per-character build identity carries
- **Trajectory:** as substrate grows (more classes, more skill templates per season), the tree expands toward canonical depth; build-identity-per-character matures

**v2 work scope (post-Profile-A-ship):**
- Generate additional class templates beyond current canonical roster
- Generate additional skill templates per substrate × axis × bin
- Re-author math note as v2 with canonical-parity parameters
- Convergence algorithm structure UNCHANGED (algorithm is parameter-shift-robust); specific parameter values + tree generation logic updates

**This is a deliberate trajectory, not a permanent deviation.** Reincarnated's design intent IS canonical-ARPG-depth at endgame; v1 simply ships what current substrate supports while substrate matures toward parity scope.

### 8.3.1 Substrate availability framing (Amendment 7, NEW)

Per Q4 synthesis 2026-05-21:

**Current engine substrate state** (per legolas Phase 1 substrate-sufficiency audit 2026-05-20):
- 4 of 7 BC axes have PARTIAL or GAP coverage relative to 5× sufficiency rule
- Ability schema lacks several required metadata fields
- Some substrate categories at 0 (HP-economy, charge-stack, damage-converts, player-side proxies)

**Required for W1.13 implementation:**
- ~168+ unique skill templates per season for full archive diversity (7 classes × 12 nodes × variety factor)
- All 7 BC axes meeting 5× sufficiency rule
- Ability schema complete with BC-axis-contribution tags + cost/cooldown fields

**Path to W1.13 substrate readiness:**
- **P1 W1.1** — Ability schema extensions including all v1.1 fields per § 3.6
- **P1 W1.2-W1.6** — Substrate creation: HP-economy (W1.2), damage-taken-converts (W1.3), charge-stack (W1.4), movement variety (W1.5), player-side proxies (W1.6)
- **P1 W1.7** — Legolas Phase 2 substrate audit depth pass
- **P1 W1.11** — Element-specific substrate enrichment (uniform comprehensive depth per Track C verdict)

**W1.13 implementation gate:** P1 substrate enrichment must close gaps before W1.13 fires. Estimated 5-8 weeks of P1 work post-P0-close.

### 8.4 Matt's caveat — Scope D is starting structure, refined post-legolas (not transformed beyond recognizability)

**Per Matt 2026-05-21:**
> *"ARPG knowledge and related decisions may transform scope D beyond recognizability, but it is a good structure."*

**Post-legolas reality:** Scope D's STRUCTURAL SHAPE stands (canonical-aligned chain × tier × SP × cap × budget). ALGORITHM gets meaningful enhancement (Tier 4 mechanic-altering + trigger interaction layer + Tier 1 playability constraint + gate refinement). PARAMETER VALUES validated within canon (with refinements to gates + active slot cap).

**Not transformed beyond recognizability. Refined into Scope D-refined.** The math note v1 → v1.1 amendment captures the refinement.

**v1.1 STANDS regardless of further research findings.** Knight-rider can fire W1.13 implementation against v1.1 once P1 substrate enrichment closes the Q4 gap. Further refinements (v1.X) fold in based on empirical W1.13 outcomes.

---

## 9. Implementation guidance for W1.13 specialist (rocket)

### 9.1 What gets built in P1 W1.13 (refined per v1.1)

**Substrate generation (substrate-agnostic; per Tier 1 playability invariant per Amendment 3):**
- Per-class-per-season skill tree generation function
- Tree topology: 2-4 chains × 3-4 tiers × ~10-15 total nodes per kit
- **Tier 1 playability enforcement** — generator validates each chain has ≥1 L1-playable Tier 1 node (cost ≤ class-budget; cooldown ≤ 2.0s; no prerequisite)
- Per-node abstract mechanic class assignment (damage/control/defense/mobility/utility)
- Per-node BC-axis-contribution tagging (5+ floats per node)
- Tier-specific coefficient assignment per node (per § 5.4)
- **Tier 4 mechanic-altering keystone CANDIDATES per chain (~3-5 candidates; pick one at convergence)**
- **Trigger/conditional interaction nodes per chain (1-2 per chain; activated at convergence)**

**Convergence algorithm:**
- WR-skew gradient mechanism (§ 4.2)
- Multi-tier voting per-iteration with 3 phases: SP adjustment + Tier 4 selection + trigger selection (§ 4.3)
- Soft-preference tier-unlock penalty with gates 2/4/7 (§ 4.1)
- Tier 1 playability runtime safety check (§ 4.6)
- Local optima escape via random restart (§ 4.4)
- Budget + cap + topology constraint enforcement

**Telemetry instrumentation:**
- Per-iteration WR deltas + adjustment vectors
- Convergence iteration count per kit
- Tier 4 keystone selection changes per iteration
- Trigger interaction activation/deactivation changes per iteration
- Escape restart count per kit
- Final SP allocation + Tier 4 selection + trigger selections + scalar modifier per archive entry

**Reference build output:**
- Archive entry kit_specification block (per § 7) including v1.1 fields

### 9.2 What this work does NOT include

- Legendary skill grant mechanism (separate workstream; deferred)
- Per-skill scaling coefficient variance within a tier (v2)
- Cross-chain unlock asymmetry per element (post canonical-6 multi-element retired)
- Smooth rank cap formula (UX-side; not engine-side)
- Spirit Guide build-coach UI (Stage A3 territory)
- Player-facing skill tree UI changes (B6 work; demo-side)
- Endgame tuning surface (paragon/glyph/atlas-equivalent) — deliberate departure per § 8.3.1

### 9.3 Verification approach

Smoke tests + Discipline #17 calibration:

1. **Unit tests:**
   - WR-skew gradient computes correct direction on synthetic per-tier deltas
   - Multi-tier voting respects budget conservation
   - Soft-preference penalty produces 80-95% canonical-gate-respecting solutions
   - Tier 1 playability invariant enforced at generation time
   - Tier 4 keystone categorical selection converges to high-WR-fit
   - Trigger interaction combinations selected appropriately
   - Local optima escape triggers on stagnation (N iterations without improvement)

2. **Integration tests:**
   - End-to-end convergence on 5-10 representative test kits (one per substrate)
   - Per-tier WR convergence within contract bounds for 80%+ of test kits
   - All test kits have L1-playable Tier 1 nodes per chain
   - Convergence iteration count median <20

3. **Empirical validation:**
   - Re-run Track C-style same-calibration ablation across all 7 substrates
   - Predict: low-modifier kits previously at 0.000 boss WR exit zero-floor via keystone-concentration + trigger interactions
   - Pattern-A 100% → expected ~5-15% post-W1.13 (residual due to BC-target-mismatched kit attempts; expected)

### 9.4 Critique-pair structure

- **gandalf reviews architectural alignment** (substrate-as-cohesion preservation; reference build completeness; ARPG-canon thematic anchor strength; Tier 4 mechanic-altering authenticity; trigger interaction multiplicative scaling; Tier 1 playability enforcement)
- **jack-ryan reviews implementation correctness** (BC-axis-contribution tagging integrity; coefficient curve sensibility; topology constraint enforcement; #13a drift check; gate value 2/4/7 correctness; categorical-selection optimization correctness)
- **Matt approves W1.13 framing** before implementation fires (NEW scope from protocol v1.1)

---

## 10. Critical math-before-code gate (per Discipline #1)

Before W1.13 implementation begins, the following math must be settled:

1. **`penalty_scale` value** for soft-preference tier-unlock (§ 4.1) — empirical calibration target: 80-95% canonical-gate respecting
2. **`T_AXIS_SENS` matrix values** (§ 4.2) — tier-axis sensitivity weights — calibrated against ARPG-canon + empirical telemetry
3. **`VOTE_THRESHOLD` value** (§ 4.3) — minimum vote magnitude to trigger SP adjustment
4. **`ESCAPE_THRESHOLD` value** (§ 4.4) — iterations without improvement before restart
5. **Initial `kit` state distribution** — bias toward BC-target via axis-contribution matching + initial Tier 4 keystone inference + initial trigger interaction inference
6. **`MAX_ITER` budget** — per-kit convergence iteration cap; balance against per-archive-cell budget at scale
7. **Tier 1 playability bounds per class element** — cost / cooldown thresholds parametrized per substrate
8. **Tier 4 keystone candidate set size** — per-chain candidate count (proposed: 3-5)
9. **Trigger interaction effect multiplier range** — per-chain interaction magnitude (proposed: 1.15-1.50× multiplicative)

These are all empirically calibratable; v1.1 algorithm provides skeleton; specific values land via Discipline #17 calibration sweeps during W1.13 implementation.

---

## 11. Open questions for legolas Phase 2 research + W0.4 verification

### 11.1 Legolas Phase 2 (substrate audit depth pass; future)

Beyond ARPG canon survey (complete), Phase 2 audits substrate variety per axis × bin. Informs W1.11 element-specific enrichment.

### 11.2 Pending W0.4 verification (gear affix architecture state)

- Do gear affixes directly modify skills, or only modify stats?
- Is legendary tier item generation operational?
- Is legendary-skill-grant mechanism implemented OR designed?

**Math note v1.1 treats gear affix dimension as PROVISIONAL.** If W0.4 confirms gear affixes are skill-modifier-capable, dimension 6 activates. Otherwise, dimension 6 collapses.

### 11.3 Spec gaps surfaced during v1.1 amendment

- BC-axis-contribution tagging schema (§ 3.6) needs implementation review — does the engine currently support per-node metadata extensions?
- Tier-axis sensitivity matrix `T_AXIS_SENS` — initial values from gandalf white-wizard intuition; needs legolas calibration data
- Substrate identity propagation — confirmed substrate-AGNOSTIC at generation per § 6; rocket confirms in implementation
- Tier 1 playability bounds — class-element-specific cost/cooldown thresholds need empirical calibration

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

- **v1.1 ARPG-canon research:**
  - `agentic_orchestration/legolas/research/arpg-skill-architecture-canon-survey-2026-05-21/` (complete; 10 questions × 10+ games surveyed)

- **Active commissions:**
  - `agentic_orchestration/dispatches/2026-05-21-legolas-arpg-skill-architecture-canon-survey.md` (complete)
  - `agentic_orchestration/dispatches/2026-05-21-monster-thematic-depth-assessment.md` (queued)

- **Engineering disciplines:**
  - `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code (this doc instantiates); #11.1 state-space conditioning; #13a drift detection; #17 empirical calibration; #18 joint-gate candidate

---

## 13. Maintenance and revision protocol

### 13.1 Versioning

- **v1** (committed 2026-05-21 commit `09b2ca2`): initial spec with white-wizard intuition + canonical structure preservation + math layer
- **v1.1** (THIS DOC; 2026-05-21): post-legolas-research + Matt-flagged amendments — 8 amendment areas folded
- **v1.X**: minor refinements during W1.13 implementation (empirical calibration adjustments)
- **v2**: post-Profile-A-ship enhancement — **PRIMARY GOAL: canonical-parity expansion (10-15 nodes → 24-30 nodes; 2-4 chains → 3-5 chains)** per Matt 2026-05-21 late-amendment clarification. Substrate-growth-gated (more classes + more skill templates required). Plus secondary: per-skill scaling variance + cross-chain rules if multi-element returns + endgame tuning surface if scope shifts

### 13.2 Authoring authority

- **gandalf** authors revisions
- **Matt approves** structural changes (Scope D pivots; new architectural commitments)
- **knight-rider** drafts decisions-log entries
- **jack-ryan** reviews against existing decisions and disciplines

### 13.3 Living-document conventions

Algorithm specification is locked at v1.1; specific parameter values are calibratable. Empirical-calibration findings from W1.13 implementation may surface refinements that update v1.X.

---

## 14. Closing — the wizard reads

**This math note v1.1 operationalizes the architectural commitment Matt and gandalf developed during 2026-05-21, refined post-legolas ARPG-canon survey + Matt-flagged Tier 1 playability constraint.** The multi-dim convergence algorithm is the empirically-mandated fix for the boss-floor pathology that arena-side fixes (W0.9 + W0.10) couldn't fully address for low-modifier kits.

**Scope D-refined is the pragmatic engineering-aware + canonically-validated target:**
- Preserves what's load-bearing for math (tier-specific scaling, 120 SP budget)
- Preserves what's load-bearing for thematic + diversity (chain × tier shape + Tier 4 mechanic-altering + trigger interactions)
- Preserves what's load-bearing for player experience (Tier 1 L1-playability, canonical ARPG feel)
- Relaxes what creates optimization cliffs (hard gates → soft preferences with refined 2/4/7 values)
- Defers what's UX polish (per-skill variance) or strategically out-of-scope (endgame tuning surface)

**The architectural decoupling is preserved:** substrate identity coalesces post-mechanical-generation per substrate-as-cohesion architecture; convergence operates on mechanical dimensions only; cohesion-judge themes the resulting kit signature.

**Reincarnated's deliberate departure from canonical design space is honored:** 10-15 nodes + 2-4 chains is procedural-seasonal-arc tuning aligned with form-library-accumulation + Earth-Meta-Layer architecture. Not a deficit; a different shape for a different game.

**The W1.13 specialist (rocket) has a complete spec.** When P1 opens and substrate enrichment (W1.1-W1.6 + W1.11) closes the Q4 substrate gap, knight-rider fires W1.13 implementation against v1.1.

**The road continues to be walked correctly.**

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine's mathematical heart, made explicit + canon-validated + Matt-refined before P1 W1.13 fires.
