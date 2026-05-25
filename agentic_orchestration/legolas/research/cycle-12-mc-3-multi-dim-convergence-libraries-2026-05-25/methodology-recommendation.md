# Methodology Recommendation — Multi-Dim Convergence Implementation Libraries (MC-3)

**Mode:** A (analytical)
**Commissioner:** knight-rider (orchestrator) / for rocket Layer 4 dispatch authoring
**Date:** 2026-05-25
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-legolas-cycle-12-mc-3-multi-dim-convergence-libraries.md`
**Authority basis:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q6 Option B substrate-led methodology consultation timing) + Discipline #18 LOAD-BEARING gate on rocket Layer 4 implementation
**Sources consulted:** See § 12 (source list)

---

## Summary (5 sentences)

The multi-dim convergence problem in math note v1.1 is a mixed-integer-continuous optimization over approximately 15-25 variables (per-node SP integers + Tier 4 keystone discrete selections per chain + trigger interaction discrete selections per chain + scalar modifier + optional gear affix vector), with a convergence target defined by a per-tier win-rate band contract and a hard cap of max_iterations=5 in Cycle 12's scope — a problem structure that is simultaneously too structurally specific (the per-tier WR gradient drives the update direction), too dimensionally small (≤15 nodes per kit at v1), and too reproducibility-constrained (generation_seed determinism required per WARN-7 and framing brief § 4 PlayerClass contract) for scipy's continuous-domain optimizers to be the right primary method. The canonical method from the math note v1.1 § 4.3 is a hand-authored coordinate-descent-style voting algorithm that already specifies the update rule precisely — per-tier WR deltas dotted against per-node BC-axis-contribution weights — meaning the "what update to make" question is already answered by the math spec and does not need a numerical optimizer to discover it; the optimizer would only add overhead, stochastic non-determinism, and an abstraction mismatch. The recommended method is **custom implementation following math note v1.1 § 4.2-4.3 exactly**: three-phase voting loop (Phase 1 continuous SP adjustments via gradient voting, Phase 2 Tier 4 keystone discrete selection via per-candidate scoring, Phase 3 trigger interaction combinatorial selection), with a configurable max_iterations cap (recommend 5 with bump path to 10 for structurally harder kits), deterministic per generation_seed, and no scipy dependency. Scipy is recommended only as a targeted secondary tool for the scalar modifier fine-tuning sub-problem (Dimension 5) after discrete selections are fixed — specifically `scipy.optimize.minimize` with method='bounded' on a one-dimensional continuous interval, which is deterministic and correct — but even this is optional since the 5% nudge rule already specified in math note v1.1 § 4.3 is adequate. The cheapest refuting test is a 30-kit smoke targeting ≥80% convergence rate within max_iterations=5 and per-kit `final_modifier` within the target_win_rate_band [0.45, 0.55] ± a per-tier tolerance, runnable against the Layer 2 + Layer 3 combined output in under 15 minutes of wall time at the 22-kit v1 archive scale.

---

## 1. Problem characterization — what the Layer 4 convergence is solving

### 1.1 The convergence space (math note v1.1 § 5)

Per math note v1.1 § 5.1-5.6, the convergence space has 5-6 dimensions:

| Dimension | Type | Range | Role |
|---|---|---|---|
| 1: Per-node SP allocation | Continuous (integer-valued) | 0-15 per node; sum ≤ 120 | Primary tuning surface; affects per-tier WR via BC-axis-contribution |
| 2: Tier 4 keystone selection | Discrete categorical | 1 of 3-5 candidates per chain, 0-1 per chain | Qualitative regime-change; most build-defining |
| 3: Trigger interaction selection | Discrete categorical | 0-2 combinations per chain | Multiplicative scaling layer |
| 4: Tier-specific scaling coefficients | Continuous (constant per tier) | 1.065/1.10/1.15/1.215 by tier | Set at generation; not tuned during convergence |
| 5: Scalar kit modifier | Continuous | ~0.05-2.0 | Final-calibration nudge; 5% per-iteration adjustments |
| 6: Gear affix vector | Continuous (provisional) | Pending W0.4 verification | Activates only if gear affixes modify skills |

At v1, Dimension 4 is constant (tier-mid coefficients set at generation, not tuned by convergence per math note v1.1 § 5.4). Dimension 6 is provisional. The active tuning dimensions are 1, 2, 3, and 5 — approximately 10-15 integer SP variables + 2-4 chain keystone selections + 2-4 chain trigger interaction selections + 1 scalar.

**Total active variables at v1:** approximately 13-20 (at the low end of "multi-dimensional" by numerical optimization standards; well within hand-authored loop territory).

### 1.2 The objective function

The convergence target is not a single minimization objective but a **multi-constraint feasibility problem**:

```
CONVERGE iff for each tier T in {swarm, magic, elite, mini_boss, boss}:
    target_wr[T].lower ≤ measured_wr[T] ≤ target_wr[T].upper
```

Where the per-tier WR contract is:
- swarm: 0.65-0.80
- magic: 0.55-0.70
- elite: 0.45-0.60
- mini_boss: 0.35-0.55
- boss: 0.30-0.45

This is a **constraint-satisfaction problem**, not a pure minimization problem. The objective can be stated as minimizing max over tiers of |measured_wr[T] - target_wr[T]|, but the algorithm terminates on FEASIBILITY (all within band), not on minimization. This distinction matters for library selection: scipy optimizers are designed for scalar minimization, not multi-constraint feasibility; the mapping is possible but introduces an artificial scalar to minimize that the math note's per-tier voting mechanism already handles more directly.

### 1.3 The update rule is pre-specified

**Critical observation for library selection:** math note v1.1 § 4.2-4.3 already specifies the update rule precisely:

```
votes[node.id] += -wr_delta[T] × tier_contribution[node]
where tier_contribution[node] = sum(node.bc_axis_contribution[axis] × T_AXIS_SENS[T][axis] for axis in axes)
```

This is a **gradient-free directed descent** rule, not a black-box query to a library optimizer. The update direction is not discovered by the optimizer — it is derived analytically from the per-tier WR deltas and the per-node BC-axis-contribution tags. This is the most important structural fact about the problem: the "search" in this algorithm is not exploration of an unknown landscape; it is deterministic directed adjustment guided by domain-specific signal.

Libraries like scipy's minimize or differential_evolution are designed to **discover** a gradient or explore a landscape when the objective structure is unknown. Here, the gradient equivalent is known (the wr_delta × contribution computation). Using a library optimizer would replace this known update with a black-box query, adding overhead without benefit.

### 1.4 The max_iterations=5 constraint (Cycle 12 scope)

The framing brief § 4 ConvergenceResult contract specifies:

```python
max_iterations: int = 5  # may bump higher per L4 implementation
```

And the dispatch confirms: max_iterations=5 is the Cycle 12 primary target, with bump path to higher values per scope-doc § 6 (non-convergence escape-hatch routes to gamora + rocket collaboration; bump max_iterations if helpful).

**Analysis:** 5 iterations is a very tight cap. The math note v1.1 § 9.3 integration tests specify "convergence iteration count median <20" as the acceptance target — suggesting the algorithm authors anticipated needing ~10-20 iterations in typical cases. Max_iterations=5 means:
- For easy kits (BC-target well-covered by substrate; good initial keystone selection): likely convergent within 5 iterations
- For harder kits (thin substrate; suboptimal initial keystone; tight per-tier targets): 5 iterations may not suffice

This recommends a configurable cap (not hard-wired to 5) with documented bump behavior. The implementation should accept `max_iterations` as a constructor or call-time parameter, defaulting to 5 per the contract but bumping to a configurable value when the escape-hatch path routes to gamora + rocket collaboration. Recommended bump: 10 (doubles the budget; still fast enough for foreground operation at 22-kit scale).

---

## 2. Literature scan — convergence methods for mixed-integer constrained problems

### 2.1 scipy.optimize — minimize variants

**scipy.optimize.minimize** provides several methods suitable for different problem shapes:

**Nelder-Mead (derivative-free simplex):**
- Handles continuous problems; no gradient required
- Does NOT natively handle integer constraints; standard workaround is rounding to nearest integer (produces non-differentiable discontinuities at each rounding boundary)
- No native support for categorical discrete variables (Tier 4 keystone, trigger interaction)
- Reproducibility: deterministic for given initial conditions; but initial conditions are the primary source of variation; seed propagation requires wrapping the optimizer call
- Does NOT expose per-iteration state for diagnostic introspection at the algorithm level (opaque iteration internals)
- 5-iteration cap: scipy's stop_criteria are based on function-value tolerance (`xatol`, `fatol`) and max-function-evaluations, not a semantic "run exactly 5 multi-tier-voting passes"; translating the per-tier WR convergence check into scipy stop-criteria requires non-trivial callback engineering

**Powell (derivative-free line search):**
- Minimizes over coordinate directions sequentially (similar in spirit to coordinate descent)
- Like Nelder-Mead: continuous domain; integer/categorical handling requires wrapping
- Line-search-based minimization does not map cleanly to the "per-node vote normalization" update the math note specifies

**SLSQP (Sequential Least Squares Programming):**
- Gradient-based; constraint-aware (can handle equality/inequality constraints)
- Requires gradient; problem is not analytically differentiable (run_spatial_gauntlet is a discrete simulation, not a differentiable function)
- Not applicable without a differentiable objective or gradient approximation (finite differences would require ~13-20 extra gauntlet calls per iteration just for gradient estimation — multiplying wall time by ~15-20×)

**BFGS / L-BFGS-B:**
- Quasi-Newton gradient-based
- Same gradient-requirement problem as SLSQP; not applicable
- L-BFGS-B supports bounded continuous variables — useful ONLY if all dimensions were continuous and differentiable

**COBYLA (Constrained Optimization BY Linear Approximations):**
- Derivative-free; handles inequality constraints
- Pure continuous domain; no categorical support
- Multi-constraint feasibility target translates naturally to COBYLA's constraint syntax (one constraint per WR bound)
- However: like Nelder-Mead, integer variables require rounding wrappers with discontinuity problems

**Overall assessment of scipy.optimize.minimize:** none of the minimize methods natively support the mixed-integer-categorical structure of the Layer 4 problem. All require workarounds for discrete variables; all expose iteration control at the function-evaluation level rather than at the semantic multi-tier-voting-pass level; none provide the per-iteration diagnostic introspection (Tier 4 keystone selection changes per iteration; trigger interaction activation/deactivation per iteration) that the math note v1.1 § 9.1 specifies as required telemetry. The mapping from scipy's minimization semantics to the algorithm's feasibility-check semantics adds complexity without reducing implementation burden.

### 2.2 scipy.optimize.differential_evolution (global optimizer)

**differential_evolution** is a population-based global stochastic search algorithm:
- Handles continuous bounded domains; supports discrete variable workarounds via `integrality` parameter (scipy >= 1.9.0)
- Global search: explores the full feasible space rather than hill-climbing from an initial point
- Stochastic: reproducible ONLY with fixed `seed` parameter; non-deterministic across calls without explicit seed passing
- Very high function-evaluation count (population × generations × dimension calls); for a 22-kit × 5-iteration budget, differential_evolution would require significantly more than 5 gauntlet calls per kit to converge (typical: hundreds of function evaluations for even simple problems)
- The `integrality` parameter handles integer dimensions; categorical Tier 4 keystone and trigger interaction require mapping to integer encoding with post-call decoding

**Reproducibility analysis:** scipy.differential_evolution with `seed=generation_seed` is reproducible per call. However, the algorithm's stochastic nature means convergence behavior varies with population initialization. With max_iterations=5 as a budget, differential_evolution would typically not converge — its intended use is long-horizon global search, not tight-budget hill-climbing.

**Assessment:** differential_evolution is designed for global-search problems where the landscape has many local optima and the budget is large (hundreds to thousands of function evaluations). The multi-dim convergence problem is NOT a global search problem — the update rule is directed by domain knowledge (per-tier WR deltas), and the search is expected to converge in median <20 iterations per the math note. differential_evolution's overhead is not justified, and its stochastic exploration would work AGAINST the tight max_iterations budget.

**One valid niche:** if the escape-hatch behavior (scope-doc § 6: structural non-convergence routed to legolas Mode A for methodology refinement) surfaces that some kit types systematically fail to converge via the directed voting loop, differential_evolution COULD be used as a last-resort fallback for those specific kits — applied with a seed and a generous function-evaluation budget. This is a contingency path, not the primary method.

### 2.3 Custom implementation (hand-rolled per math note v1.1 § 5)

A custom implementation follows math note v1.1 § 4.2-4.3 directly:

**Algorithm structure:**
```
for iteration in range(max_iterations):
    per_tier_wr = run_spatial_gauntlet(kit)
    if all_within_contract(per_tier_wr, per_tier_targets):
        return ConvergenceResult(converged=True, ...)
    
    # Phase 1: continuous SP voting
    kit = apply_sp_voting_adjustments(kit, per_tier_wr, T_AXIS_SENS)
    
    # Phase 2: Tier 4 keystone discrete selection
    kit = update_tier4_keystone_selections(kit, per_tier_wr)
    
    # Phase 3: trigger interaction discrete selection
    kit = update_trigger_interaction_selections(kit, per_tier_wr)
    
    # Scalar modifier nudge
    scalar_modifier *= nudge_factor(per_tier_wr)
    
    # Escape: restart if stagnant (within max_iterations if budget allows)
    if stagnant(best_score, current_score):
        kit = random_restart_with_bc_bias(tree, bc_target)

return ConvergenceResult(converged=False, ...)  # cap hit
```

**Reproducibility:** fully deterministic per `generation_seed`:
- `random_restart_with_bc_bias` seeds from `generation_seed + iteration_count` — deterministic
- No scipy stochastic internals to manage
- Same kit + same seed = same convergence path on every run

**Diagnostic introspection:** full per-iteration access to all intermediate state:
- Per-iteration WR deltas
- SP adjustment vectors at each phase
- Tier 4 keystone selection changes (which candidate was chosen; why)
- Trigger interaction activation/deactivation decisions
- Scalar modifier trajectory
- Stagnation counters + restart events

This is exactly the telemetry schema math note v1.1 § 9.1 specifies must be captured. With a library optimizer, this introspection requires hooking callbacks or instrumenting wrapper functions. With a custom implementation, it is native.

**Mixed-type support:** native. The algorithm's three phases (SP adjustment, keystone selection, trigger selection) handle each dimension type correctly by construction:
- SP: integer votes normalized to budget-conserving integer adjustment
- Tier 4 keystone: per-candidate scoring loop with argmax selection
- Trigger interaction: combinatorial search over 0-2 combinations per chain

**Maintenance burden:** real but manageable. The custom implementation will be ~300-600 lines of Python. This is not a trivial amount of code, but it is:
- Directly readable against the math spec (each section of code traces to a math note section)
- Testable at unit-test granularity (each phase independently testable)
- Not dependent on external library versions or deprecation risks

**Assessment:** custom implementation is the clear primary recommendation. It is the ONLY method that (a) faithfully implements the update rule the math note specifies, (b) handles mixed types natively, (c) is deterministic per generation_seed, (d) provides full diagnostic introspection, and (e) fits naturally within the max_iterations=5 / max_iterations=10 (bumped) budget.

### 2.4 Hybrid: scipy for Dimension 5 (scalar modifier) + custom for all other dimensions

After Phases 1-3 (SP + keystone + trigger selections) have run on an iteration, the scalar modifier (Dimension 5) can optionally be fine-tuned as a one-dimensional continuous optimization:

```python
# After Phase 1-3 adjustments:
from scipy.optimize import minimize_scalar
result = minimize_scalar(
    fun=lambda m: abs(aggregate_wr(kit, scalar_modifier=m) - target_wr),
    bounds=(0.05, 2.0),
    method='bounded'
)
kit.scalar_modifier = result.x
```

`scipy.optimize.minimize_scalar` with `method='bounded'` is:
- Deterministic (Brent's method; fully deterministic given bounds)
- Correct for a one-dimensional continuous bounded problem
- Fast: typically converges in ~5-20 function evaluations for smooth monotonic objectives
- No integer/categorical complications

**However:** the math note v1.1 § 4.3 already specifies the scalar nudge as `scalar_modifier *= (1 - 0.05 × sign(sum(wr_delta)))` — a simple 5% directional nudge. This is not a precise optimization; it is a calibration convenience that converges adequately over the iteration loop. Replacing it with `minimize_scalar` adds a scipy dependency for a sub-problem that the math note's simple nudge already handles.

**Recommendation for Dimension 5:** use the math note's 5% nudge rule by default; introduce `minimize_scalar` ONLY if empirical testing (the cheapest refuting test, § 7) shows that Dimension 5 is systematically the last unclosed constraint after max_iterations fires. This is a post-smoke-test refinement, not a v1 default.

### 2.5 Summary of library/method assessment

| Method | Handles mixed types natively | Deterministic per seed | Diagnostic introspection | max_iterations=5 compatibility | Recommended |
|---|---|---|---|---|---|
| scipy.minimize (Nelder-Mead / Powell) | No (workarounds required) | Yes (for fixed initial conditions) | No (opaque) | Mismatched semantics | No |
| scipy.minimize (SLSQP / BFGS) | No (gradient required) | Yes | Partial | Incompatible (requires gradient) | No |
| scipy.minimize (COBYLA) | No | Yes | Partial | Mismatched semantics | No |
| scipy.differential_evolution | Partial (integrality param) | Yes (with seed) | No | Incompatible (needs hundreds of evals) | No (contingency only) |
| Custom (math note v1.1 § 4.3) | Yes (native per dimension type) | Yes (per generation_seed) | Yes (full per-iteration) | Compatible (exact semantic match) | YES (primary) |
| Hybrid: custom + minimize_scalar for Dim 5 | Yes | Yes | Yes | Compatible | Optional refinement |

---

## 3. Per-dim ordering — coordinate descent vs full gradient

### 3.1 What the math note specifies

Math note v1.1 § 4.3 specifies a **sequential three-phase structure per iteration**:
- Phase 1: SP voting (all continuous SP dimensions updated together, then normalized)
- Phase 2: Tier 4 keystone selection (all chains' keystone selections evaluated + updated together)
- Phase 3: Trigger interaction selection (all chains' interaction combinations evaluated + updated together)

This is **within-type grouped update**, not simultaneous full-gradient or strict coordinate-by-coordinate descent. It is the correct structure because:

1. SP adjustments are budget-coupled (normalization must happen over all nodes simultaneously to conserve the 120 SP budget). Updating one node at a time without normalization would leave the budget constraint violated at each sub-step.

2. Keystone selections are per-chain categorical choices. Evaluating all chains' keystone candidates in one pass (rather than per-chain sequentially) avoids ordering dependency (the effect of chain A's keystone selection on chain B's WR profile is captured when both are updated in the same evaluation round).

3. Trigger interaction selections are combinatorial (0-2 per chain); evaluating all interaction combinations within a phase is necessary because inter-chain interactions are defined in the trigger interaction spec (see math note v1.1 § 4.5 trigger "Chain Reaction" example: cross-chain effect).

### 3.2 Coordinate descent vs full gradient — verdict

**Coordinate descent (one dimension at a time):**
- Slower convergence rate in principle (ignores cross-dimensional dependencies)
- But for this problem, the math note's three-phase grouped structure IS a form of blocked coordinate descent (update SP block together; keystone block together; trigger block together)
- The correct interpretation: the algorithm IS coordinate-descent-by-type (group each dimension type; update group together; move to next group)

**Full gradient (all dimensions simultaneously):**
- Requires a unified gradient across continuous and discrete dimensions — not naturally definable for categorical selections
- Would require relabeling categorical dimensions as integers and computing a single update — not recommended because Phase 2 and Phase 3 require per-candidate evaluation, not a gradient-direction update

**Verdict:** the math note's three-phase blocked grouped update is the correct structure. Do not change it to either strict coordinate-by-coordinate descent (breaks budget conservation) or full simultaneous gradient (incompatible with categorical dims). Implement exactly as math note § 4.3 specifies.

---

## 4. Multi-tier voting integration with the chosen method

### 4.1 How voting integrates with custom implementation

The multi-tier voting mechanism (math note § 4.2-4.3) is the algorithmic heart — it converts per-tier WR deltas into per-node adjustment vectors. Under the custom implementation:

**Phase 1 — SP voting:**
```python
votes = {node.id: 0.0 for node in tree.rank_scaling_nodes}
for tier in TIERS:
    wr_delta = measured_wr[tier] - target_wr_midpoint[tier]
    for node in tree.rank_scaling_nodes:
        tier_contribution = sum(
            node.bc_axis_contribution[axis] * T_AXIS_SENS[tier][axis]
            for axis in T_AXIS_SENS[tier]
        )
        votes[node.id] -= wr_delta * tier_contribution

# Normalize votes to integer SP adjustments (budget-conserving)
sp_adjustments = normalize_to_integer_delta(votes, current_sp=kit.sp_allocation, budget=120, cap_per_node=15)
kit.sp_allocation = apply_adjustments(kit.sp_allocation, sp_adjustments)
```

**Phase 2 — Keystone selection:**
```python
for chain in tree.chains:
    candidates = chain.available_tier_4_keystones  # 3-5 per chain per math note § 5.2
    current_keystone = chain.tier_4_selection
    
    best = current_keystone
    best_score = score_keystone_fit(current_keystone, measured_wr, per_tier_targets, kit)
    
    for candidate in candidates:
        if candidate == current_keystone:
            continue
        score = score_keystone_fit(candidate, measured_wr, per_tier_targets, kit)
        if score > best_score:
            best_score = score
            best = candidate
    
    chain.tier_4_selection = best
    if best != current_keystone:
        emit_telemetry(iteration, chain.id, "keystone_changed", current_keystone, best)
```

**Phase 3 — Trigger interaction selection:**
```python
for chain in tree.chains:
    candidates = chain.available_trigger_interactions  # 1-2 per chain
    # Evaluate all 0-2-combinations (maximum 3 combinations for 1 interaction available; 
    # maximum 4 combinations for 2 interactions: {}, {i1}, {i2}, {i1,i2})
    best = chain.active_trigger_interactions
    best_score = score_interaction_combination(best, measured_wr, per_tier_targets, kit)
    
    for combo in iter_combinations(candidates, max_size=2):
        if combo == best:
            continue
        score = score_interaction_combination(combo, measured_wr, per_tier_targets, kit)
        if score > best_score:
            best_score = score
            best = combo
    
    chain.active_trigger_interactions = best
```

### 4.2 The score_keystone_fit and score_interaction_combination functions

These functions are not fully specified in math note v1.1 — they are implied by the voting mechanism's structure. The recommended operationalization:

```python
def score_keystone_fit(keystone, measured_wr, per_tier_targets, kit):
    """
    Score how well a hypothetical keystone selection would improve convergence.
    Uses predicted WR delta improvement based on keystone's BC-axis profile.
    """
    predicted_delta_reduction = 0.0
    for tier in TIERS:
        current_wr_delta = abs(measured_wr[tier] - per_tier_targets[tier].midpoint)
        keystone_axis_profile = keystone.bc_axis_contribution  # from Layer 3 SkillTree output
        tier_sensitivity = T_AXIS_SENS[tier]
        
        # How much does this keystone push toward the under-performing tiers?
        contribution = sum(
            keystone_axis_profile.get(axis, 0.0) * tier_sensitivity.get(axis, 0.0)
            for axis in tier_sensitivity
        )
        
        # Reward contributions that reduce deltas (sign-aligned with wr_delta direction)
        if measured_wr[tier] < per_tier_targets[tier].lower:
            predicted_delta_reduction += contribution * current_wr_delta  # need higher WR
        elif measured_wr[tier] > per_tier_targets[tier].upper:
            predicted_delta_reduction -= contribution * current_wr_delta  # need lower WR
    
    return predicted_delta_reduction
```

This is a forward-simulation-free scoring function (no additional gauntlet calls per candidate). The scoring is an approximation (it predicts the WR improvement from BC-axis contribution, not from an actual gauntlet run). This is correct: the multi-tier voting mechanism is explicitly an approximation-based directed adjustment, not a precise gradient. One gauntlet call per iteration (to measure the actual per-tier WR) is the limiting cost.

**Critical implication for compute envelope:** ONE gauntlet call per iteration, not one per candidate per dimension. The scoring functions for keystone and trigger selection are forward-simulation-free approximations. This is the key property that makes max_iterations=5 viable — the gauntlet cost is O(max_iterations) per kit, not O(max_iterations × candidates × chains).

---

## 5. max_iterations=5 cap handling and escape-hatch behavior

### 5.1 Is max_iterations=5 realistic?

**Assessment:** for well-conditioned kits (BC-target well-covered by substrate; good initial keystone inference from BC-target bias; moderate per-tier WR targets), 5 iterations may be sufficient. The math note's median-<20 target suggests harder cases. At v1's 22-kit archive scale, the distribution across easy/hard cases is unknown.

**Recommendation:** implement the 5-iteration cap as DEFAULT with configurable bump. The ConvergenceResult contract supports `converged: bool` — a False return at cap-hit is the correct failure signal, not an error.

The relevant framing is: max_iterations=5 is the **v1 acceptance threshold**, not a hard physical limit. The implementation should:
1. Accept `max_iterations: int = 5` as a constructor/call parameter
2. Execute exactly max_iterations iterations if convergence is not achieved earlier
3. Return `ConvergenceResult(converged=False)` on cap hit with `best-found-so-far` state in `converged_kit`
4. Expose `iteration_count` in the result (trivially trackable in the custom loop)

The `best-found-so-far` behavior on cap-hit is the correct fallback: per scope-doc § 6, if convergence fails within cap, the kit is routed to gamora + rocket collaboration. They need to see what the algorithm achieved in 5 iterations as the starting point, not an empty result.

### 5.2 Stagnation detection and escape within the cap

Math note v1.1 § 4.4 specifies random restart on stagnation. Within a 5-iteration budget:

- **If stagnation is detected at iteration 2 (2 iterations without improvement):** restart at iteration 3, leaving 2 more iterations. Total restarts at 5-iter cap: 1-2 maximum.
- **ESCAPE_THRESHOLD recommendation for max_iterations=5 context:** set ESCAPE_THRESHOLD = 2 (restart after 2 non-improving iterations). This gives at least one restart opportunity within the 5-iteration budget.

For bumped runs (max_iterations=10): ESCAPE_THRESHOLD = 4 (restart after 4 non-improving iterations; matches the math note's proposed "8-12 iterations" guidance for full runs, scaled to budget).

### 5.3 Bump-iteration path per scope-doc § 6

Per cycle-12-hive-mind-scope.md § 6:
> "if convergence doesn't converge within max_iterations=5, route to gamora + rocket collaboration; bump max_iterations if helpful; if structural non-convergence, route back to legolas Mode A for methodology refinement"

The implementation should expose a `bump_iterations(new_max: int)` path — either via re-calling `converge_kit` with a higher `max_iterations` OR via a `resume_from_result(prior_result, new_max_iterations)` function that continues from the ConvergenceResult's best-found state. The resume path is preferable (avoids discarding prior iteration work).

**When bump helps:** when the kit is making progress toward the target but hasn't reached it in 5 iterations. Detectable from `per_dim_adjustments` trajectory in `ConvergenceResult` — if the WR deltas are shrinking per iteration, a bump will likely converge; if they are stagnant (stagnation count = ESCAPE_THRESHOLD reached), bump alone won't help.

**When bump doesn't help (structural non-convergence):** when the kit's BC-target cell is thin-substrate (no substrate row can satisfy the WR contract), or when the Tier 4 keystone candidates available to the chain don't have BC-axis profiles compatible with the target. This surfaces the escape-hatch to legolas Mode A for methodology refinement. The ConvergenceResult should capture enough diagnostic state for legolas to identify the failure mode.

---

## 6. Mixed-type support — detailed analysis

### 6.1 Continuous dimension (Dimension 1 — SP)

SP values are integers 0-15 per node with sum ≤ 120. The voting mechanism produces continuous vote sums that must be converted to integer deltas. The recommended conversion:

```python
def normalize_to_integer_delta(votes, current_sp, budget=120, cap_per_node=15):
    """
    Convert continuous vote sums to integer SP adjustments respecting:
    - Budget constraint: sum(new_sp) <= 120
    - Per-node cap: new_sp[i] <= 15, >= 0
    - Budget conservation: total SP allocated = 120 (adjust proportionally if needed)
    """
    # Scale votes to produce at most a max_step_per_iteration change per node
    max_step = 2  # configurable; 2 SP per iteration per node is a sensible v1 default
    scaled = {nid: max(min(v, max_step), -max_step) for nid, v in votes.items()}
    
    # Apply tentative adjustments
    tentative = {nid: current_sp[nid] + round(scaled[nid]) for nid in current_sp}
    
    # Clip to [0, cap_per_node]
    clipped = {nid: max(0, min(cap_per_node, tentative[nid])) for nid in tentative}
    
    # Budget conservation: normalize total to 120
    total = sum(clipped.values())
    if total > budget:
        # Reduce highest-sp nodes proportionally (standard normalization)
        overflow = total - budget
        sorted_nodes = sorted(clipped.items(), key=lambda x: x[1], reverse=True)
        for nid, sp in sorted_nodes:
            reduction = min(sp, overflow)
            clipped[nid] -= reduction
            overflow -= reduction
            if overflow == 0:
                break
    
    return clipped
```

This is the most careful implementation detail in the custom loop — budget conservation must be exact at each iteration to avoid accumulated drift. The math note does not specify this implementation detail; the above is the recommended operationalization.

### 6.2 Discrete categorical dimensions (Dimensions 2, 3 — Tier 4 keystone, Trigger interactions)

Per-candidate scoring via `score_keystone_fit` and `score_interaction_combination` (per § 4.2 above). No integer encoding required — candidates are Python objects (dataclass instances from Layer 3's T4Candidate types). Selection is argmax over scoring loop. Combinatorial search for trigger interactions is bounded: with ≤2 interactions per chain and maximum 2 activation slots, the search space per chain is at most C(2,0) + C(2,1) + C(2,2) = 4 combinations — trivially enumerable.

**MC-3 ↔ Gate-2-on-L2 dependency assessment:** the keystone and trigger selection logic in Phase 2 and Phase 3 requires access to `T4Candidate.bc_axis_contribution` — which Layer 3 emits per the SkillTree contract. Gate-2 on Layer 3 (PASS per jack-ryan findings) confirms the Layer 4 walk simulation passes: `wr_gradient[axis_key] += contribution * sp_rank * tier_coefficient` (Gate-6 test). Gate-2 on Layer 2 is in-flight in parallel with this MC-3. The Layer 4 custom implementation does NOT need to inspect PlayerClassV2's internal shape beyond the framing brief § 4 `converge_kit(kit: PlayerClass)` signature — it consumes `kit.skill_tree` (from Layer 3) and `kit.generation_seed` (from Layer 2). There is NO architectural dependency on Layer 2 Gate-2 outcomes for the MC-3 recommendation. The MC-3 ↔ Gate-2-on-L2 dependency assessment is: **NONE. Both can return independently. Rocket Layer 4 dispatch requires both for completeness, but not for sequential dependency.**

### 6.3 Scalar modifier (Dimension 5)

The 5% directional nudge from math note v1.1 § 4.3:
```python
scalar_modifier *= (1 - 0.05 * sign(sum(wr_delta[t] for t in TIERS)))
```

This converges toward a zero-net-WR-delta state. For low-modifier kits (boss-floor fix cases), the scalar modifier starts near its current value and adjusts iteratively. Within 5 iterations at 5% per step, the scalar can move by approximately:
- 5 iterations at +5%/step: +27.6% maximum upward adjustment
- 5 iterations at -5%/step: -22.6% maximum downward adjustment

For kits near the boundary of the convergence band, this range may be sufficient. For kits far outside the band, the scalar nudge alone won't close the gap — which is why the SP + keystone + trigger adjustments (Phases 1-3) are the primary convergence mechanism, with scalar as final fine-tuning.

---

## 7. Cheapest-refuting-test design (per Discipline #19.1)

### 7.1 The claim to refute

The custom implementation's core claims:
1. **Convergence rate claim:** ≥80% of kits converge within max_iterations=5 (all five per-tier WR within contract bounds)
2. **Feasibility band claim:** for converged kits, `final_modifier` is within the target_win_rate_band (per-tier WR within stated bounds)
3. **Determinism claim:** same kit + same `generation_seed` produces identical `ConvergenceResult` on repeated calls
4. **No regression claim:** the 5% boundary-signal rate on mage_controller kits (current state per § 1.2.4 of math note) does not worsen post-W1.13 implementation

### 7.2 Test design — 30-kit smoke

**Test name:** Layer 4 convergence rate smoke

**Scale:** 30 kits (sufficient to estimate ≥80% convergence rate with ±15% precision at 95% confidence; N=30 gives SE = sqrt(p(1-p)/30) ≈ 0.073 at p=0.8)

**Sampling strategy:** draw from Layer 2 + Layer 3 combined output across the 22 BC-roster cells. Include:
- 5 "easy" kits (thick-substrate cells: STR/DEX martial; Cell 1, 7, 9)
- 5 "medium" kits (INT/WIS caster; moderate substrate coverage)
- 5 "hard" kits (thin-substrate cells or THIN-routed cells per composition policy § 4)
- 5 kits from the mage_controller archetype family (regression check against current 5% boundary signal)
- 10 randomly drawn from the remaining READY cells

**Procedure:**

```
1. Load 30 kit instances from Layer 2 + Layer 3 output (PlayerClass with skill_tree populated)
2. For each kit:
   a. Call converge_kit(kit, target_win_rate_band=(0.45, 0.55), max_iterations=5)
   b. Record: converged bool; iteration_count; per_dim_adjustments; final per-tier WR; final_modifier
3. Compute convergence rate: converged_count / 30
4. For converged kits: verify per-tier WR within contract bounds (all 5 tiers within their respective bands)
5. Determinism check: re-run 5 of the 30 kits with same generation_seed; verify identical ConvergenceResult
6. mage_controller regression: for the 5 mage_controller kits, verify convergence rate ≥ 60% (generous bound; current baseline is 95%; allow 35pp degradation before flagging)
```

**Pass/fail thresholds:**

| Criterion | PASS | FAIL |
|---|---|---|
| Convergence rate (30 kits, max_iter=5) | ≥ 80% (≥ 24/30 converged) | < 80% (< 24/30) → bump to max_iter=10 and re-test |
| Per-kit WR band for converged kits | All 5 per-tier WR within contract bounds | Any converged kit with a tier outside bounds → implementation bug |
| Determinism | 5/5 re-runs identical | Any deviation → seed propagation bug |
| mage_controller regression | ≥ 60% convergence (≥ 3/5) | < 60% → boundary-signal worsening; route to gamora |

**Bumped threshold:** if convergence rate fails at max_iter=5 (< 24/30) but passes at max_iter=10 (≥ 24/30), the recommendation is to ship with max_iterations=10 as default for v1 and revisit the 5-iteration target as a v1.1 optimization after the algorithm is empirically validated.

**What this test does NOT cover:**
- Archive-scale generation (22 kits × N seasons): covered by Layer 6 smoke
- BDI interaction term validation: Cycle 13+ Layer 7 work
- Endgame tuning surface: v2+ work

### 7.3 Compute cost of the cheapest-refuting-test

Per math note v1.1 § 9.3 integration test spec: "convergence iteration count median <20." At 5 iterations per kit:
- Gauntlet calls: 30 kits × 5 iterations × 1 gauntlet call/iteration = 150 gauntlet calls
- Gauntlet wall time: not specified precisely, but prior methodology consults cite Phase 3 as "2-3 min/kit at 20 iterations" → at 5 iterations, approximately 0.5-0.75 min/kit
- **Total wall time estimate: 30 kits × 0.5-0.75 min = 15-22 minutes**

This is foreground-runnable. No background-process (nohup/PID-tracked) overhead needed. The test can be run interactively as a smoke gate before the Layer 4 dispatch commits.

**At max_iterations=10 (bumped):** approximately 30-45 minutes. Still foreground-runnable.

---

## 8. Resource-bounds projection (per Discipline #1.1)

### 8.1 Per-method peak memory

**Custom implementation:**
- Per-kit state: kit object (~10-15 nodes × ~20 fields per node + metadata) = ~10-50 KB per kit
- Per-iteration state: vote sums (one float per node) + adjustment vectors + WR deltas (5 floats) = negligible
- Peak memory: single kit in memory at a time = ~1 MB maximum including gauntlet context
- At 22 kits (full v1 archive): sequential processing keeps peak memory flat at single-kit level

**scipy.optimize.minimize (Nelder-Mead):**
- Simplex state: (N+1) vertices × N dimensions = (N+1) × N floats where N ≈ 15 nodes + 5 scalar modifier degrees = ~20 variables
- Simplex memory: 21 × 20 × 8 bytes = ~3.4 KB; negligible
- Overhead dominates from wrapping the gauntlet call as a scipy objective function

**scipy.differential_evolution:**
- Population state: population_size (default: 15×N) × N dimensions = 15×20×20 × 8 bytes ≈ 48 KB; still negligible
- Much larger function evaluation count is the primary concern (runtime, not memory)

**All methods are memory-safe at 22-kit v1 scale.** No memory concern for any choice. The Mac mini 8 GiB M2 host concern that triggered Discipline #1.1's memory-bounds projection clause (kernel panics in Phase E-1 HDBSCAN at ~71K-row dataset) does not apply here — the convergence algorithm operates on single-kit objects at a time, not on bulk data arrays.

### 8.2 Per-method runtime envelope at 22-25 kits × max_iterations=5

| Method | Gauntlet calls (per kit) | Approx gauntlet cost | Total per kit | 22 kits total |
|---|---|---|---|---|
| Custom (primary) | max_iterations = 5 | 0.5-0.75 min/kit @ 5 iter | 0.5-0.75 min | 11-17 min |
| Custom (bumped to max_iter=10) | 10 | 1.0-1.5 min/kit | 1.0-1.5 min | 22-33 min |
| scipy.minimize (Nelder-Mead) | ~50-200 function evals | Each eval = 1 gauntlet call → 50-200× cost | 25-150 min | impractical |
| scipy.differential_evolution | ~hundreds of evals | Population × generations = hundreds of gauntlet calls | impractical | impractical |

**The scipy minimize methods multiply gauntlet call count by 10-100× compared to the custom implementation.** This is the primary runtime argument against library optimizers. The gauntlet is the expensive primitive — each call involves simulating the multi-monster spatial gauntlet (W0.9 + W0.10 true multi-monster spatial). Library optimizers treat the objective as cheap to evaluate and compensate with high evaluation count. The custom implementation makes the opposite assumption (expensive objective; domain-informed update direction; minimize evaluation count).

### 8.3 Background-process firing pattern

At 22 kits × max_iterations=5 (~11-17 minutes total), the smoke test and the full 22-kit generation run are both foreground-runnable. No nohup/PID-tracked background process is needed for v1 scale.

If v2 expansion to 100+ kits × max_iterations=10 fires, total runtime becomes ~100 kits × 1.0-1.5 min = 100-150 minutes — crossing the foreground session budget. At that scale, Discipline #19 background-process discipline applies (nohup + PID tracking + completion log). This is a v2 concern, not a v1 concern.

---

## 9. Implementation-shape sketch (for rocket Layer 4 dispatch consumption)

This is not implementation code. It is the specification surface rocket's Layer 4 dispatch must implement. Math note v1.1 governs; this sketch adds implementation-detail operationalizations not fully specified in the math note.

```
LAYER 4 MULTI-DIM CONVERGENCE — IMPLEMENTATION SHAPE

MODULE: generation/converge.py  (new module in rocket seam)

IMPORTS:
  - math note v1.1 constants: T_AXIS_SENS (calibrated per § 10 below), ESCAPE_THRESHOLD
  - Layer 3 types: SkillTree, T4Candidate, TriggerInteraction (from skill_tree.py)
  - Layer 2 types: PlayerClass (from bc_target_subspace_generator.py)
  - Gauntlet interface: run_spatial_gauntlet (existing; W0.9 + W0.10 multi-monster spatial)
  - ConvergenceResult dataclass (new; per framing brief § 4)

CONSTANTS (calibratable; set before Layer 4 fires based on empirical tuning):
  - T_AXIS_SENS: dict[tier, dict[axis, float]] — tier-axis sensitivity matrix (see § 10)
  - ESCAPE_THRESHOLD: int = 2 (for max_iterations=5 default; 4 for max_iterations=10 bumped)
  - MAX_SP_STEP_PER_ITERATION: int = 2 (maximum SP change per node per iteration)
  - SCALAR_NUDGE_RATE: float = 0.05 (5% per-iteration nudge per math note v1.1 § 4.3)

PRIMARY ENTRY POINT:
  def converge_kit(
      kit: PlayerClass,
      target_win_rate_band: tuple[float, float] = (0.45, 0.55),
      max_iterations: int = 5,
  ) -> ConvergenceResult:

    rng = seeded_rng(kit.generation_seed)  # deterministic RNG from PlayerClass seed
    
    best_state = copy_kit_state(kit)
    best_score = float('inf')
    no_improvement_count = 0
    iteration_log = []
    
    for iteration in range(max_iterations):
      # Step 1: Measure current per-tier WR
      per_tier_wr = run_spatial_gauntlet(kit)
      
      # Step 2: Check convergence (FEASIBILITY, not minimization)
      if all_within_contract(per_tier_wr, per_tier_targets):
        return ConvergenceResult(
          converged_kit=kit,
          final_modifier=kit.scalar_modifier,
          iteration_count=iteration + 1,
          converged=True,
          per_dim_adjustments=summarize_adjustments(iteration_log),
        )
      
      # Step 3: Stagnation check
      score = sum(max(0, per_tier_wr[T] - per_tier_targets[T].upper) +
                  max(0, per_tier_targets[T].lower - per_tier_wr[T])
                  for T in TIERS)
      if score < best_score - EPSILON:
        best_score = score
        best_state = copy_kit_state(kit)
        no_improvement_count = 0
      else:
        no_improvement_count += 1
      
      # Step 4: Escape if stagnant
      if no_improvement_count >= ESCAPE_THRESHOLD:
        kit = random_restart_with_bc_bias(tree=kit.skill_tree, bc_target=kit.bc_target_cell, rng=rng)
        no_improvement_count = 0
        continue
      
      # Step 5: Phase 1 — SP voting adjustment
      wr_deltas = {T: per_tier_wr[T] - per_tier_targets[T].midpoint for T in TIERS}
      kit = apply_sp_voting(kit, wr_deltas, T_AXIS_SENS, MAX_SP_STEP_PER_ITERATION)
      
      # Step 6: Phase 2 — Tier 4 keystone selection
      kit = update_tier4_keystone_selections(kit, wr_deltas, per_tier_targets, T_AXIS_SENS)
      
      # Step 7: Phase 3 — Trigger interaction selection
      kit = update_trigger_interaction_selections(kit, wr_deltas, per_tier_targets, T_AXIS_SENS)
      
      # Step 8: Scalar modifier nudge
      net_delta = sum(wr_deltas.values())
      kit.scalar_modifier *= (1 - SCALAR_NUDGE_RATE * sign(net_delta))
      
      iteration_log.append(capture_iteration_state(iteration, per_tier_wr, kit))
    
    # Cap hit without convergence
    return ConvergenceResult(
      converged_kit=best_state,  # return best-found-so-far, not final state
      final_modifier=best_state.scalar_modifier,
      iteration_count=max_iterations,
      converged=False,
      per_dim_adjustments=summarize_adjustments(iteration_log),
    )

RESUME ENTRY POINT (for bump-iteration path):
  def resume_convergence(
      prior_result: ConvergenceResult,
      additional_iterations: int,
  ) -> ConvergenceResult:
    # Continue from prior_result.converged_kit with additional_iterations budget
    # Preserves prior iteration_log for full diagnostic trace
    ...

TELEMETRY REQUIRED (per math note v1.1 § 9.1):
  - Per-iteration WR deltas + adjustment vectors
  - Convergence iteration count per kit
  - Tier 4 keystone selection changes per iteration (chain_id, from, to)
  - Trigger interaction activation/deactivation changes per iteration
  - Escape restart count per kit
  - Final SP allocation + Tier 4 selection + trigger selections + scalar modifier

NO SCIPY IMPORTS REQUIRED IN PRIMARY PATH.
Optional scipy.optimize.minimize_scalar import for Dimension 5 refinement if smoke reveals
scalar modifier as the bottleneck dimension — but not in v1 primary path.
```

---

## 10. T_AXIS_SENS calibration note

The tier-axis sensitivity matrix `T_AXIS_SENS` (math note v1.1 § 4.2) is described as "calibrated against ARPG-canon + empirical telemetry" but specific values are not authored in math note v1.1. This is the most important calibration parameter for the Layer 4 implementation.

**Recommended v1 initial values** (from ARPG-canon framing in math note § 4.2):

| Tier | axis_2_geometry | axis_2A_proxy | axis_2B_control | axis_3A_tempo | axis_3B_variance | axis_4_defensive | axis_5_economy | axis_1_engagement |
|---|---|---|---|---|---|---|---|---|
| swarm | 0.30 | 0.15 | 0.10 | 0.25 | 0.05 | 0.05 | 0.05 | 0.05 |
| magic | 0.20 | 0.10 | 0.15 | 0.20 | 0.10 | 0.15 | 0.05 | 0.05 |
| elite | 0.15 | 0.05 | 0.15 | 0.20 | 0.15 | 0.20 | 0.05 | 0.05 |
| mini_boss | 0.10 | 0.05 | 0.10 | 0.15 | 0.25 | 0.20 | 0.10 | 0.05 |
| boss | 0.05 | 0.05 | 0.05 | 0.15 | 0.30 | 0.25 | 0.10 | 0.05 |

**Calibration note:** these values encode the intuition from math note § 4.2 (swarm = AOE geometry + tempo; boss = spike variance + defense). They are NOT empirically validated at this stage — they are the v1 starting point for Discipline #17 calibration sweeps during Layer 4 implementation. Rocket should parametrize these values (not hard-code them) so they can be swept post-Layer 4 landing. A single-parameter sweep (Discipline #24) over individual axis weights while holding others constant is the recommended calibration procedure.

**Dependency flag:** the T_AXIS_SENS matrix is an internal Layer 4 parameter. Its specific values do NOT depend on the shape of PlayerClassV2 from Layer 2 Gate-2. This is NOT an MC-3 ↔ Gate-2-on-L2 dependency.

---

## 11. Framing-audit checklist (per Discipline #23)

**Q1: What load-bearing framing assumptions does this methodology recommendation depend on?**

1. **The gauntlet (run_spatial_gauntlet) is callable with a single kit object** and returns per-tier WR in a form that the convergence loop can consume. If the gauntlet interface has changed since Layer 3 Gate-2 (which verified `bc_axis_contribution` walkability via a simulated walk, not an actual gauntlet call), the Layer 4 implementation must verify the actual gauntlet call interface before firing. This is the primary MC-3 ↔ Gate-2-on-L2 dependency to flag: Layer 2 must produce a PlayerClass consumable by the gauntlet. Gate-2 on Layer 2 is verifying this; MC-3 does not depend on Gate-2-on-L2's return, but rocket's Layer 4 implementation should confirm the gauntlet interface is intact before firing the convergence loop.

2. **Layer 3's bc_axis_contribution dict uses exactly the 8 keys from math note v1.1 § 3.6.** Confirmed by Gate-2 on Layer 3 (jack-ryan: "BC axis keys are locked to the 8-key vocabulary from math note v1.1 § 3.6"). Not at risk.

3. **T4Candidate objects are accessible from the SkillTree with their bc_axis_contribution populated.** Gate-2 on Layer 3 confirms T4 candidates per chain ≥ 5 (Gate 3 test: "T4 candidates ≥ 5"). Not at risk.

4. **max_iterations=5 is adequate for ≥80% convergence rate.** This is the cheapest-refuting-test claim — the 30-kit smoke will either confirm or refute it. NOT yet empirically validated. If the smoke returns convergence rate < 80% at max_iter=5, the recommended adjustment is to default max_iterations=10 (not to change the algorithm).

5. **The T_AXIS_SENS initial values in § 10 produce convergent behavior for most kit types.** These are calibration-start values, not validated values. Discipline #17 calibration sweeps during implementation will adjust them. If convergence rate smoke fails at the T_AXIS_SENS initial values, recalibration (not algorithm change) is the recommended first response.

6. **One gauntlet call per iteration is the correct measurement granularity** (not one per Phase 2 keystone candidate or per Phase 3 trigger combination). The Phase 2 and Phase 3 scoring functions are forward-simulation-free approximations. This means the Phase 2 and Phase 3 selection quality is bounded by the approximation quality. If the approximation is systematically wrong (scoring a bad keystone as good), convergence may fail even within the voting mechanism. The cheapest refuting test (30-kit smoke) will surface this if Phase 2/3 selections are consistently counter-productive.

**Q2: What evidence currently in hand could refute these assumptions?**

1. Assumption 1 (gauntlet interface): refutable by reading `~/Games/reincarnated-engine/src/reincarnated/simulation/` gauntlet interface. Evidence available; not currently in hand for this Mode A consult (read-only research). Rocket should verify at Layer 4 dispatch start.

2. Assumption 4 (max_iterations=5 adequate): refutable by the 30-kit smoke (§ 7). Not yet in hand.

3. Assumption 5 (T_AXIS_SENS initial values): refutable by single-parameter sweep (Discipline #24) during implementation. Not yet in hand.

4. Assumption 6 (scoring approximation quality): refutable by inspecting per-iteration Phase 2/3 selection changes against WR delta trajectories. Capturable from the iteration_log in the implementation.

**Q3: If refutation evidence exists or is plausible, is the right move to refine the framing rather than execute as-framed?**

The two refinements recommended before Layer 4 implementation fires:

- **Verify gauntlet interface call signature** (Assumption 1): a 5-minute read of the gauntlet module before the convergence loop is written avoids interface mismatch discovery mid-implementation. Rocket should fire this verification at Layer 4 dispatch start.

- **T_AXIS_SENS initial values as configurable parameters from the start** (Assumption 5): do not hard-code. Parametrize and expose via the math-before-code section of the Layer 4 math note. This allows sweep without code change.

Neither of these refinements is in scope for legolas Mode A research (Mode A is read-only; implementation decisions are rocket's). Surfacing here per Discipline #23 Q3 as pre-implementation framing recommendations.

**Surprises beyond framing brief assumptions:**

One surprise worth flagging: math note v1.1 § 10 explicitly names 9 parameters that "must be settled" before W1.13 implementation (penalty_scale; T_AXIS_SENS values; VOTE_THRESHOLD; ESCAPE_THRESHOLD; initial kit state; MAX_ITER; Tier 1 playability bounds; T4 candidate set size; trigger interaction effect multiplier range). The framing brief's max_iterations=5 specification resolves #6 (MAX_ITER). The other 8 parameters require Discipline #17 calibration sweeps during Layer 4 implementation. The rocket Layer 4 dispatch should include a math-before-code section specifying initial values for all 9 parameters and a sweep plan for the empirically-calibratable ones. MC-3 does not resolve these — it recommends the implementation approach; parameter calibration is Layer 4 implementation work.

---

## 12. Methodology recommendation summary

**Recommended implementation method:** custom implementation following math note v1.1 § 4.2-4.3 exactly. No scipy primary dependency.

**Rationale summary:**
- The update rule is pre-specified by domain knowledge (wr_delta × contribution voting); no optimizer needed to discover it
- Mixed-type support is native to the three-phase loop structure
- Deterministic per generation_seed by construction (no stochastic library internals)
- Full diagnostic introspection available (per-iteration log captures all WR delta, SP adjustment, keystone change, trigger change data)
- max_iterations=5 is naturally expressed as a loop termination condition
- Library optimizers (scipy) are 10-100× more expensive in gauntlet calls due to their high function-evaluation requirements
- Custom implementation is directly readable against the math note (each code section traces to a math note section)

**scipy use cases (secondary; optional):**
- `scipy.optimize.minimize_scalar` method='bounded' for Dimension 5 (scalar modifier) fine-tuning if smoke reveals scalar as bottleneck — deterministic, correct, minimal scope
- `scipy.optimize.differential_evolution` as last-resort fallback for kits that fail structural non-convergence at max_iterations=10 — with explicit seed, for global-search escape on problematic kit types only

**Per-dim ordering:** three-phase blocked grouped update per math note v1.1 § 4.3 (Phase 1: all SP together; Phase 2: all keystone selections; Phase 3: all trigger selections). Do not change to strict coordinate-by-coordinate (breaks budget conservation) or full simultaneous gradient (incompatible with categorical dims).

**max_iterations cap:** implement as configurable parameter defaulting to 5, with bump path to 10 via resume_convergence entry point. Return best-found-so-far on cap hit (not empty/error). ESCAPE_THRESHOLD = 2 at default max_iterations=5; 4 at max_iterations=10.

**MC-3 ↔ Gate-2-on-L2 dependency:** NONE. Recommendation does not depend on PlayerClassV2 shape from Layer 2. Rocket Layer 4 dispatch should verify gauntlet call interface as a pre-implementation step independent of Gate-2-on-L2 outcome.

**Cheapest refuting test:** 30-kit smoke, ≥80% convergence rate within max_iterations=5, 15-22 minutes wall time. PASS threshold: ≥24/30 converged; per-kit WR within all 5 tier contract bounds; determinism verified on 5 re-runs; mage_controller regression ≥3/5.

**Resource bounds:** peak memory < 1 MB per kit at v1 scale; no kernel-panic risk; foreground-runnable at 22-kit archive scale (11-17 min); background-process pattern not needed until v2 100+ kit scale.

---

## 13. Knowledge gaps not resolved

1. **Gauntlet call interface** — the exact function signature and return type of `run_spatial_gauntlet` as it exists in the current engine. This is a code-read, not a Mode A research item. Rocket verifies at Layer 4 dispatch start.

2. **T_AXIS_SENS empirical values** — the 9 calibration parameters from math note v1.1 § 10 are all pending Discipline #17 sweeps. This is post-implementation calibration work, not a pre-implementation blocker.

3. **Phase 2/3 scoring approximation quality** — whether `score_keystone_fit` and `score_interaction_combination` (forward-simulation-free) produce selections that are consistently productive. Empirically evaluable from the 30-kit smoke iteration log. Not determinable from Mode A research alone.

4. **Gear affix dimension (Dimension 6)** — pending W0.4 verification. If gear affixes modify skills, Dimension 6 activates and an additional Phase 4 in the voting loop is needed. The framing brief treats Dimension 6 as provisional. Layer 4 dispatch should implement with Dimension 6 gated by a configuration flag (activate when W0.4 confirms; collapse when it doesn't).

5. **score_keystone_fit's handling of the T4 regime-change semantics** — the MECHANIC-ALTERING nature of Tier 4 keystones (per math note v1.1 § 3.4) means that a keystone's BC-axis contribution is not a direct linear predictor of WR improvement — it changes the underlying resource model or geometry, producing non-linear WR effects. The scoring approximation in § 4.2 is linear. Whether this linear approximation is adequate for keystone selection within 5 iterations is an empirical question answered by the smoke test.

---

## 14. Source list

**Primary sources (project canonical docs):**
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 — primary algorithm specification; especially § 2 (problem formalization), § 3.6 (bc_axis_contribution schema), § 4.1-4.6 (math layer: voting, soft-preference, local optima escape, trigger interactions, Tier 1 playability), § 5.1-5.6 (5-6 dimensional space specification), § 9.1-9.3 (implementation guidance + verification approach), § 10 (calibration parameters)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — § 4 (ConvergenceResult contract LOCKED; max_iterations=5 default; PlayerClass + converge_kit signatures) + § 2 MC-3 scope statement + § L9 (mechanical vs semantic split — convergence operates on mechanical dims only) + § 5.1-5.3 algorithm pseudocode
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` — § 6 pre-resolved known-unknowns (Layer 4 non-convergence escape-hatch routing)
- `agentic_orchestration/dispatches/2026-05-25-legolas-cycle-12-mc-3-multi-dim-convergence-libraries.md` — dispatch scope, acceptance criteria, open questions
- `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md` — MC-1 precedent (same Mode A methodology consult pattern; especially § 7 cheapest-refuting-test design + § 9 resource-bounds projection)
- `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md` — MC-2 precedent (substrate-binding heuristic; layer consumed by Layer 4 convergence; especially §§ 2-3 literature scan pattern)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-3.md` — Gate-2 on Layer 3 PASS; confirms bc_axis_contribution 8-key vocabulary locked; confirms Gate-6 Layer 4 walk simulation; confirms T4 candidates per chain ≥ 5
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-2-bc-target-subspace-generator.md` — Layer 2 dispatch (PlayerClass shape Layer 4 consumes; confirms MC-1 + MC-2 methodology consumed)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code + resource-bounds projection clause) + #18 (methodology-before-execution) + #18.2 (extension hotspot timing) + #19/#19.1 (cheapest-refuting-test operationalization + background-process firing) + #23 (framing-audit checklist) + #24 (single-parameter sweep isolation)

**Secondary sources (literature):**
- Whitley, D. (1994). "A genetic algorithm tutorial." Statistics and Computing 4(2). Mixed-integer evolutionary optimization; integrality handling; relevant to differential_evolution's integrality parameter.
- Nocedal, J., Wright, S. (2006). "Numerical Optimization." Springer. Chapter 9 (derivative-free methods: Nelder-Mead, Powell, COBYLA — pros/cons for non-smooth, non-differentiable objectives). Chapter 15 (constrained optimization with inequality constraints — COBYLA, SLSQP theoretical basis).
- Price, K., Storn, R., Lampinen, J. (2005). "Differential Evolution: A Practical Approach to Global Optimization." Springer. Global search budget requirements; stochastic reproducibility via seed; population-size effect on convergence rate.
- scipy.optimize documentation — https://docs.scipy.org/doc/scipy/reference/optimize.html — function evaluation budgets per method; integrality parameter (differential_evolution, scipy >= 1.9.0); minimize_scalar bounded method (Brent's algorithm, deterministic).
- Auger, A., Hansen, N. (2005). "A restart CMA-ES with increasing population size." IEEE CEC. Random restart behavior in continuous optimization; stagnation-triggered restart patterns — relevant to math note v1.1 § 4.4 random restart design.
- Togelius, J., Yannakakis, G., Stanley, K., Browne, C. (2011). "Search-based Procedural Content Generation: A Taxonomy and Survey." IEEE TVCG 17(6). Derivative-free search for procedural generation objectives; coordinate-descent-style PCG optimization; evaluation-budget considerations for expensive fitness functions.
- Shaker, N., Togelius, J., Nelson, M. (2016). "Procedural Content Generation in Games." Springer. Chapter 5 (search-based methods for PCG with expensive fitness functions; evaluation budget tradeoffs; constraint satisfaction vs minimization framing).
- PoE build mechanics reference — https://www.poewiki.net/wiki/Skill_gem — multiplicative support gem stacking mechanics; trigger interaction design patterns; canonical ARPG multi-tier build diversity mechanism (relevant to Phase 3 trigger interaction scoring rationale).

---

**Signed:** legolas (researcher and scout)
**For:** knight-rider MC-3 return → rocket Layer 4 dispatch authoring (W1.13 multi-dim convergence); fires when MC-3 returns AND Gate-2-on-L2 PASS (per scope-doc § 0 Layer 4 sequencing condition).
