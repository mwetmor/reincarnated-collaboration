# Methodology Recommendation — Constrained Knapsack with Must-Include for Stage 3 Sampling

**Mode:** A (analytical)
**Commissioner:** elrond (lead, Phase 2 execution) / knight-rider (dispatch authority)
**Date:** 2026-05-25
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 9
**Policy spec consumed:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` §§ 2, 3, 4, 7
**Resource envelope (from dispatch § 8):** ~3 min compute + ~150 MB peak memory

---

## Summary

The Stage 3 constrained-sampling problem is a multi-axis weighted knapsack with pre-committed must-include items (Tier S/A) and per-cell coverage floor constraints. The literature offers four main algorithmic families for this class: greedy-with-swap-repair, linear programming (LP) / mixed-integer programming (MIP), population-based metaheuristics (simulated annealing, genetic algorithms), and constraint programming (CP). Given the specific constraint structure here — dominated by pre-committed items, modest per-axis weights, bounded pool sizes after genre-filter pre-pass, and a ~3 min / 150 MB resource envelope — **greedy-with-swap-repair is the correct baseline**, with LP (via PuLP/CBC) as a named fallback triggered by a specific gap-floor failure signal. Simulated annealing and MIP are unnecessary complexity for this problem at this scale. The cheapest refuting test is a per-cell-floor satisfaction percentage check run immediately post-Phase-2 population, with a concrete pass threshold of ≥85% of cells at or above floor.

---

## 1. Problem structure characterization

Before algorithm selection, it is useful to state the problem precisely. Stage 3 selects a v1_scope subset from 89,841 rows subject to:

**Hard constraints (must satisfy):**
- Tier S handheld auto-include (~449 rows): membership pre-committed, non-negotiable
- Tier S secondary auto-include (~100-160 rows after Phase 0a/0b): membership pre-committed
- Genre filter pre-pass: `register_canonical IN ('fantasy', 'mythological', 'historical')` — rows outside filter are ineligible; reduces effective pool before sampling begins
- D1c exclusion gate: `weapon_kind_classified_subtype IN ('siege_vehicle', 'art_object', 'other', ...)` → always v1_scope=0

**Soft constraints (optimize against):**
- Per-axis target weights across 5 axes: register (~50-55% historical / ~30-35% fantasy / ~5-8% military_modern), cultural-tradition (14-lineage distribution), period (substrate-led skew with medieval/classical nudge), mechanical-cell (STR ~24% / DEX ~27% / INT ~27% / WIS ~24%), proxy-density (~75% none)
- Per-cell coverage floors: ~30-120 rows per cell-type (Sketch B floors); cell-pair sharing per D3 merges 5 pairs into 4-tuple shared pools
- military_modern Tier A trim: ~80% sampling-weight reduction at per-row level; per-axis target (5-8% register share) is the binding constraint at the constraint-satisfaction layer

**Mixed hard/soft:**
- Tier A preferred-include (near-hard; eviction last)
- Tier C included only on floor-fill (near-hard; high inclusion penalty unless floor unsatisfied by Tier B)
- Option C cells: ω-penalty flag set by construction (per-cell architectural fact, not per-row evaluation)

**Target subset size:** ~1,700-3,100 rows (bounds set by design call; significant headroom)

**Key structural observation:** the pre-committed Tier S items (~549-609 rows) constitute 18-36% of the lower bound of the target range (1,700). The effective decision space — rows where the algorithm actually makes inclusion/exclusion choices — is Tier B + Tier C (~60,717 rows) after Tier S auto-include, Tier A near-hard-include, and genre + kind filters are applied. This is a tractable selection problem, not a combinatorial explosion.

---

## 2. Algorithm survey

### 2.1 Greedy-with-swap-repair

**Mechanism.** Two-phase approach: (1) greedy pass — sort rows by composite weight (tier priority + per-axis target alignment score), include greedily until per-axis targets are approximately satisfied; (2) swap-repair pass — identify constraint violations (per-axis overshoot, per-cell floor undershoot), swap in/out candidate rows to reduce violations without degrading other axes.

**Strengths for this problem:**
- Naturally handles pre-committed must-include items (Tier S/A): insert them first, run greedy on remaining budget
- Per-axis weight scoring is a simple dot-product over 5 axes — O(N) per row evaluation
- Swap-repair handles the military_modern over-representation risk: the trim weight reduces per-row score; if aggregate military_modern share still drifts above 8%, a swap pass can evict lowest-scoring military_modern rows and replace with next-best non-military_modern candidates
- Cell-pair sharing (D3 5-tuple pairs) requires only a lookup table at scoring time — no structural change to the algorithm
- Option C cells: per-cell flag, no algorithmic branching required
- Runs in O(N log N) for sort + O(K × M) for swap passes where K = candidate swap set size and M = per-cell constraint count; at N=89,841 rows and M~25 cells, well within resource envelope
- No external dependencies; pure Python with SQLite reads
- Transparent: `v1_scope_composition_trace` JSON is trivially populated during the greedy pass (row knows why it was included)

**Weaknesses:**
- Does not guarantee global optimality — can get trapped in local optima if per-cell floors are near-infeasible
- Swap-repair convergence not guaranteed in worst case; requires iteration cap
- Under-performs LP when many constraints are simultaneously near-tight (close-to-infeasible cells competing for the same rows)

**Resource projection at this problem scale:**
- Greedy sort: 89,841 rows × 5-axis score = ~450K operations; <1 sec
- Swap-repair: bounded by iteration cap × candidate set size; with cap=500 and candidate set ~5K rows: ~500 × 5K = 2.5M comparisons; ~10-30 sec
- Memory: 89,841 rows × per-row weight vector (5 floats = 40 bytes) + tier flags = ~4 MB working set; well within 150 MB envelope

**Verdict: primary baseline. Correct choice.**

### 2.2 LP solver (PuLP/CBC/GLPK)

**Mechanism.** Formulate the selection problem as a linear program: binary decision variable x_i ∈ {0, 1} for each row; objective = maximize Σ (weight_i × x_i); subject to: per-axis target weight constraints (linear inequalities over the selection), per-cell floor constraints (Σ x_i for rows matching cell ≥ floor), must-include forcing (x_i = 1 for Tier S rows), budget constraint (Σ x_i ≤ target_size). Since decision variables are binary, this is technically a Mixed Integer Program (MIP/MIP-LP relaxation).

**Strengths:**
- Guarantees global optimality within the LP relaxation (or integer optimum for MIP)
- Handles all constraints simultaneously; no risk of local optima from sequential greedy choices
- PuLP is an open-source Python library; CBC solver (bundled with PuLP) is free and handles N~90K binary variables in minutes on modern hardware
- Well-suited when per-cell floor constraints are simultaneously near-tight across many cells (the regime where greedy-with-swap-repair degrades)

**Weaknesses:**
- Complexity: writing the LP formulation correctly requires care (constraint indexing per axis-value, cell membership lookups, must-include forcing)
- Solve time for 89,841 binary variables: CBC typically solves MIPs of this size in 30-120 sec depending on constraint tightness; within the 3 min envelope but at the edge
- Memory for LP matrix at 89,841 rows × ~150 constraints (25 cells × 6 axes): ~134 MB sparse matrix in standard LP representation; approximately at the 150 MB ceiling; dependent on PuLP's internal representation
- Less transparent for `v1_scope_composition_trace` generation (LP assigns values globally; per-row rationale requires post-hoc attribution)
- Overkill if greedy-with-swap-repair converges adequately (which it will for most runs given the large subset budget relative to per-cell floors)

**Verdict: named fallback. Trigger it when greedy gap-floor failure signal fires (see § 4 below).**

### 2.3 Mixed-Integer Programming (MIP with CPLEX / Gurobi)

**Mechanism.** Full MIP formulation with commercial solvers (CPLEX, Gurobi) for guaranteed integer optimum.

**Assessment for this problem:** unnecessary. CBC (open-source, bundled with PuLP) handles this problem class at N~90K without commercial solver overhead. CPLEX/Gurobi would offer marginal solve-time benefit; the licensing and dependency cost is not justified. If LP fallback is needed, PuLP+CBC is the correct choice.

**Verdict: not recommended.**

### 2.4 Simulated Annealing (SA)

**Mechanism.** Probabilistic search: start from a feasible solution (e.g., greedy output), propose swap perturbations, accept worsening moves with probability exp(−ΔE / T) where T is a temperature schedule decreasing over iterations.

**Strengths:** escapes local optima; handles non-linear objective functions.

**Weaknesses for this problem:**
- Requires careful temperature schedule design and cooling rate tuning — adds hyperparameter complexity without clear benefit
- Convergence time is problem-specific and hard to bound; guaranteeing completion within 3 min requires extensive upfront calibration
- The problem's constraint structure is nearly linear (axis weight targets + floor counts); SA's ability to escape non-linear local optima is not load-bearing here
- Post-hoc `composition_trace` generation is less direct than greedy
- Longer implementation and testing cycle than greedy-with-swap-repair

**Verdict: not recommended for this problem. The LP fallback covers the gap-floor failure mode more directly and with better convergence guarantees.**

### 2.5 Constraint Programming (CP-SAT via OR-Tools)

**Mechanism.** Google OR-Tools CP-SAT solver frames the problem as constraint satisfaction, using propagation + CDCL-style search. Handles hard constraints natively with completeness guarantees.

**Assessment:** OR-Tools CP-SAT can solve binary selection problems at N~90K rapidly and handles all constraint types here. However, it introduces a non-standard Python dependency (ortools) and the formulation complexity is comparable to LP. The LP fallback (PuLP+CBC) is already standard in the Python scientific ecosystem and is a simpler dependency. CP-SAT would be the right choice if the problem had highly non-linear or combinatorial constraints (e.g., pairwise exclusion rules, precedence constraints). This problem does not.

**Verdict: not recommended. PuLP+CBC covers the fallback need.**

---

## 3. Recommended baseline: greedy-with-swap-repair — rationale grounded in constraint structure

The composition policy constraint structure is favorable for greedy-with-swap-repair for three structural reasons:

**Reason 1: Pre-committed items dominate the budget.** Tier S (~549-609 rows) + Tier A preferred-include (~5,000-6,000 rows after military_modern trim) constitute the majority of the v1_scope lower bound. The sampler is optimizing a relatively small incremental Tier B/C selection (perhaps 600-1,500 rows) over a large pool (~60K rows). Greedy with well-tuned axis scores handles this regime well; LP's global optimality advantage applies most strongly when the entire selection is unconstrained.

**Reason 2: Axis constraints are loose relative to the pool.** The per-axis targets are ranges (not point targets), and the pool contains abundant representation of each register/tradition/period category at Tier B. The military_modern trim is the tightest constraint (5-8% target vs 31% Tier A share), but it is handled cleanly by the per-row sampling weight mechanism PLUS the per-axis check at the constraint-satisfaction layer.

**Reason 3: The per-cell floor failures predicted by Stage 2 thin-cell analysis are already routed to Sidecar B / Stage 3.5.** Cells 13, 14, 15, 17, 19, 22, 23, 24, 25 are known-thin and have explicit downstream gap-fill routes (per composition policy § 4.1 + thin-cell routing table). Stage 3 is not expected to satisfy these cells' floors from current substrate — those floor failures are expected outcomes, not algorithm failures. This further reduces the "simultaneously near-tight constraint" scenario that favors LP.

**The one scenario where greedy degrades to LP:** if multiple non-thin cells (i.e., cells with adequate substrate depth) still land under floor after the swap-repair pass. The signal for this is ≥3 non-thin cells under floor with remaining Tier B pool showing adequate on-axis rows that the swap pass did not surface. This indicates a local-optima trap in the swap sequence — LP fallback resolves it directly.

---

## 4. Failure-mode signals: when to fall back from greedy to LP

The following signals, measured immediately post-greedy-pass (before committing to DB), trigger LP fallback:

**Signal F1 (primary trigger — cell floor failure in non-thin cells):**
After greedy-with-swap-repair completes, count cells where: (a) current v1_scope floor coverage < floor threshold AND (b) the cell is NOT in the known-thin routing table (policy § 4.1 cells 13, 14, 15, 17, 19, 22, 23, 24, 25). If count ≥ 3, fall back to LP.

Rationale: 1-2 non-thin-cell misses can be resolved by a targeted second swap pass with a wider swap radius. ≥3 indicates systematic local optima that greedy cannot resolve with further swap iterations.

**Signal F2 (secondary trigger — axis target deviation):**
After greedy-with-swap-repair, check per-axis distribution histogram against composition policy § 2 targets. If any axis deviates >10pp from target (not the post-population 5pp threshold — that is a much tighter acceptance criterion), fall back to LP for that axis's constraint. In practice, this most likely fires on military_modern share (if the per-row trim weight and per-axis constraint interact unexpectedly) or on cultural-tradition distribution (if Pan-Fantasy/Hybrid overfills due to Tier A density).

**Signal F3 (degenerate output — subset size out of bounds):**
If post-greedy v1_scope count is <1,600 or >3,200 (outside design-call estimate with 6% margin), investigate before falling back. Likely cause: genre filter or D1c gate applied too broadly/narrowly, not a greedy failure. Fix the filter first; LP fallback is not relevant here.

**What is NOT a fallback trigger:**
- Known-thin cells (cells 13, 14, 15, 17, 19, 22, 23, 24, 25) under floor: expected. Record in composition trace; route to Stage 3.5 / Sidecar B. Do not trigger LP.
- Tier-S counts not matching 449: the Tier-S denominator is empirically confirmed at 1,126 (Stage 2.5 gate); if count deviates, investigate classifier output, not algorithm.

---

## 5. Parameter recommendations

### 5.1 Per-row axis-alignment scoring

Score each candidate row across 5 axes before the greedy pass. The composite score drives greedy sort order.

```
axis_score(row) = Σ_{k=1}^{5} w_k × alignment_k(row)
```

Where:
- w_k = per-axis importance weight (suggested: register=0.30, cultural_tradition=0.25, mechanical_cell=0.25, period=0.10, proxy_density=0.10)
- alignment_k(row) = how much including this row would move axis k toward its target share (positive = closes gap; negative = overshoot risk)
- Alignment calculation: `alignment_k = (target_k - current_k) / target_k` evaluated at each greedy step (updated incrementally), where `current_k` is the current share of axis k's value in the selection so far

Note: the per-axis weights above (w_k) are a starting recommendation based on policy priority ordering (register is the coarsest filter; mechanical_cell is the tightest coverage requirement). Elrond may tune these after smoke; they do not need to be derived analytically before Phase 2 fires.

**Tier multiplier (applied atop axis score):**
- Tier S: pre-committed; not scored
- Tier A (non-military_modern): composite multiplier 3.0 (preferred-include enforcement)
- Tier A (military_modern): composite multiplier 0.6 (80% trim → 0.2 × 3.0 = 0.6)
- Tier B: composite multiplier 1.0 (standard)
- Tier C: composite multiplier 0.3 (floor-fill-only enforcement)

### 5.2 Iteration cap and swap-budget

**Greedy pass iteration cap:** N/A — greedy pass is a single sort + sequential scan; no iteration cap needed.

**Swap-repair pass parameters:**
- Outer iteration cap: 200 passes
- Per-pass swap budget: min(50, |violation_set|) swaps attempted per pass (violation_set = rows identified as most contributing to constraint violations)
- Convergence tolerance: stop when no swap in a full pass reduces total constraint violation by >1 row (i.e., progress stalls)
- Swap candidate radius: for each violating cell, candidate swaps are drawn from the Tier B pool filtered to the cell's 5-tuple fingerprint (Option α) or attribute class (Option β); radius does NOT extend to Tier C unless cell floor is unsatisfied and no Tier B candidates remain for that cell

**Recommended total iteration budget:** 200 outer passes × 50 swaps = 10,000 swap evaluations. At ~1 μs per evaluation (hash-lookup-based), this is ~10 ms overhead — negligible relative to the 3 min envelope.

### 5.3 military_modern double-enforcement

Per dispatch § 4.2 Gate-1 amendment 5: the 80% per-row trim and the 5-8% per-axis target are two distinct enforcement layers. The correct implementation:

1. At scoring time: Tier A military_modern rows receive tier multiplier 0.6 (per § 5.1 above), reducing their probability of inclusion in the greedy pass
2. After greedy pass: compute actual military_modern share of current v1_scope. If >8%, run a targeted swap pass: evict the lowest-scoring military_modern rows and replace with highest-scoring non-military_modern Tier B rows until share lands in 5-8% range
3. Do NOT sum the two signals multiplicatively (0.2 × 0.6 = 0.12 effective share, which would under-represent military_modern below 5%). The per-axis target is the binding final constraint.

### 5.4 Cell-pair shared-pool accounting (D3 Option A)

For the 5 shared 4-tuple cell pairs, the floor accounting at sampling time should merge the pair into a single pool:

- Count: `floor_satisfied = True` if combined row count for the pair ≥ (floor_a + floor_b) / 2 (floors are shared; proxy-density discrimination at form-generation, not at sampling)
- Composition trace: record `matching_policy = 'option_alpha_martial_5tuple'` or `option_beta_caster_attribute_level'` per the cell pair's attribute class; note the cell-pair sharing in `notes` field

---

## 6. Resource-bounds projection (per Discipline #1.1, validated against dispatch § 8 envelope)

| Pipeline step | Compute estimate | Memory estimate | Source |
|---|---|---|---|
| Genre filter pre-pass (SQL WHERE clause) | <1 sec | negligible (DB-side) | SQL index scan |
| D1c exclusion + Tier S auto-include (SQL UPDATE) | <5 sec | negligible | Batch UPDATE |
| Load candidate pool into memory (Tier A/B/C rows, genre-filtered) | ~5 sec | ~89,841 rows × 1-2 KB = ~90-180 MB | dispatch § 8 projection |
| Per-row axis scoring (5 hash lookups per row) | ~2 sec | 89,841 × 40 bytes (5 floats) = ~3.6 MB | O(N × 5) |
| Greedy sort + selection pass | ~3 sec | in-place sort on score array = ~720 KB | O(N log N) |
| Swap-repair pass (200 × 50 swaps) | ~10-30 sec | candidate swap set ~5K rows × 40 bytes = ~200 KB | O(cap × swap_budget) |
| DB write (3 columns × 89,841 rows) | ~60 sec | ~3 columns × 89,841 rows = negligible (incremental) | dispatch § 8 |
| **Total** | **~80-100 sec (~1.5 min)** | **~90-185 MB peak** | |

**Projection vs envelope:** ~1.5 min compute is well within the 3 min envelope. Memory at ~90-185 MB peak is tight against the 150 MB ceiling from dispatch § 8. The binding step is loading the full candidate pool in-memory (~90-180 MB depending on column count loaded).

**Mitigation for memory ceiling:** load only the columns required for scoring (row_id, quality_tier, register_canonical, cultural_lineage_canonical, historical_period_canonical, proxy_attribute_class, proxy_range_class, proxy_geometry_class, proxy_tempo_class, proxy_density, weapon_kind_classified_subtype) rather than all columns on the table. This reduces per-row load to ~200-400 bytes, bringing the pool memory to ~18-36 MB — well inside the envelope. DB write back uses row_id-keyed UPDATE batches.

**LP fallback resource projection (if triggered):**
- PuLP model build: 89,841 binary variables × ~150 constraints = sparse LP matrix; PuLP+CBC build time ~10-20 sec; memory ~50-100 MB (sparse matrix representation); solve time 30-120 sec for CBC at this scale
- Total LP path: ~2-3 min compute; ~150-200 MB peak (at the ceiling; CBC solve memory is the binding factor)
- If LP fallback is needed AND memory projection exceeds 150 MB: subsample the Tier B/C pool to the top 20K scoring rows (per the greedy axis score already computed) before feeding to LP. The LP then selects optimally from the pre-filtered top-scoring candidate set. This preserves near-optimal behavior while respecting the memory envelope.

**Verdict:** the greedy-with-swap-repair baseline comfortably fits within dispatch § 8 envelope. The LP fallback fits within ~200 MB, which may require the column-selective load mitigation above if host RAM is constrained. Both paths respect the ~3 min compute bound.

---

## 7. Cheapest refuting test (per Discipline #19.1)

### 7.1 Test design

**Test name:** per-cell-floor satisfaction check (PCFS)

**When:** immediately after Phase 2 population script completes, before DB commit. Run as the first post-population assertion before any other Phase 2 smoke checks.

**What it checks:** for each non-thin cell (i.e., each cell NOT in the known-routing-table list: cells 13, 14, 15, 17, 19, 22, 23, 24, 25), count the number of v1_scope=1 rows matching the cell's 4-tuple fingerprint (or 5-tuple for cells with proxy-density discrimination). Compare against the Sketch B floor threshold.

**SQL structure:**
```sql
SELECT 
    proxy_attribute_class,
    proxy_range_class,
    proxy_geometry_class,
    proxy_tempo_class,
    COUNT(*) as cell_count,
    <sketch_b_floor> as floor_threshold,
    CASE WHEN COUNT(*) >= <sketch_b_floor> THEN 'PASS' ELSE 'FAIL' END as floor_status
FROM weapon_knowledge_entries
WHERE v1_scope = 1
GROUP BY proxy_attribute_class, proxy_range_class, proxy_geometry_class, proxy_tempo_class;
```

**Pass/fail threshold:** PCFS PASSES if ≥85% of non-thin cells meet their Sketch B floor (i.e., ≤15% floor-failure rate among non-thin cells). For a ~22-cell roster with ~13 non-thin cells (after routing 9 to Sidecar B / Stage 3.5), this means ≤2 non-thin cells under floor.

**Fail action:** if PCFS fails (>2 non-thin cells under floor), DO NOT commit to DB. Evaluate Signal F1 (§ 4): if ≥3 non-thin cells under floor → trigger LP fallback. If 2-3 non-thin cells under floor and LP fallback is not indicated → run one additional targeted swap-repair pass focused specifically on those under-floor cells before committing.

**Why this is the cheapest refuting test:**
- Runtime: single SQL GROUP BY on an indexed table = <5 sec
- Requires: Phase 2 population to have completed (output in memory or temp table)
- Refutes: the algorithm converged to a locally valid solution that nonetheless misses coverage floors in cells with adequate substrate depth — the primary failure mode of greedy-with-swap-repair
- Cost if it fails: triggers LP fallback (~2-3 min additional compute) rather than surfacing at Gate-2 or Matt sign-off (which would require a re-run of the full Phase 2 pipeline)

### 7.2 Additional post-population smoke assertions (per dispatch § 8)

The following are ordered by cheapest-first, consistent with Discipline #19.1:

1. **PCFS** (above) — <5 sec
2. **Tier-S non-D1c inclusion check** — `SELECT COUNT(*) WHERE v1_scope=1 AND weapon_kind_classified_subtype IN (D1c list)` MUST RETURN 0; <2 sec
3. **military_modern share check** — `SELECT COUNT(*) WHERE v1_scope=1 AND register_canonical='military_modern'` / total v1_scope × 100; must land in 5-8% range; <2 sec
4. **Mode-C contamination check** — `SELECT COUNT(*) WHERE v1_scope=1 AND rep_audit_mode_c_naming_allusion_suspected=1` MUST RETURN 0; <2 sec
5. **Per-axis distribution histogram** — full 5-axis distribution; ~10 sec; feeds §5.5 acceptance criterion

---

## 8. Implementation notes for elrond

**Dependency inventory for greedy path:** none beyond standard Python (sqlite3, heapq or sorted()). No external solver dependencies.

**Dependency inventory for LP fallback path:** `pip install pulp` (includes CBC solver). PuLP 2.x is available on PyPI; no licensing; CBC bundled.

**Composition trace population during greedy pass:** the greedy pass naturally knows why each row was selected (which axis score drove it, which tier bucket). Populate the `v1_scope_composition_trace` JSON fields inline during the greedy loop rather than as a post-hoc step. This ensures trace fidelity and avoids a second pass over 89,841 rows.

**Option C cells:** no per-row branching needed. At scoring time, if the row's cell assignment (from proxy_attribute_class + proxy_range_class) maps to an Option C cell (Red Mage / Monk-archetype / Holy Knight), set `matching_policy = 'option_c_cross_attribute_omega_penalty'` in the composition trace. The ω-penalty flag is a per-cell architectural fact; the sampler records it, it does not enforce it (that is Phase 5 cohesion-judge territory).

**Cell-pair shared-pool floor accounting:** implement a lookup table mapping each cell's 4-tuple fingerprint to the cell-pair group (if any). At floor-check time, use the group-level count rather than per-cell count for the 5 D3 pairs.

**Incremental axis target tracking:** maintain a running count per axis-value during the greedy pass (e.g., `current_register_counts = {'fantasy': 0, 'historical': 0, ...}`). Update after each row inclusion. Use this to compute per-row alignment scores incrementally — avoids recomputing from scratch per row, which would be O(N²).

---

## 9. Knowledge gaps

- **Exact Sketch B floor magnitudes per cell:** the dispatch references floor range 30-120 per cell-type but does not provide the per-cell floor values in this dispatch. Elrond should load these from `canonical/story/v1-bc-target-intent-2026-05-24.md` Sketch B before Phase 2 fires; the PCFS test (§ 7.1) requires per-cell floor values at query time.
- **Exact Tier B / C pool size after genre filter:** the dispatch states 89,841 total rows but does not break down how many pass the genre filter pre-pass. If a large fraction are out-of-filter (e.g., sci-fi / cyberpunk registers), the effective pool is smaller than 89,841 and greedy convergence will be faster. Elrond should count genre-filtered rows pre-Phase-2 as a one-line SQL to confirm pool size before running the full pipeline.
- **Per-cell 4-tuple fingerprint completeness:** 68% of rows are NULL-typed on Stage 1 proxy fingerprint (dispatch § 2). Option α cell matching (5-tuple fingerprint) cannot apply to NULL-typed rows. The greedy pass should treat NULL-typed rows as eligible ONLY for Option β cells (attribute-level match only) or as undifferentiated Tier B floor-fill candidates when a cell floor is undersatisfied and no typed rows remain. This should be documented in the composition trace.

---

## 10. Source list

Sources consulted are training-data based (literature survey from pre-2025 published work). No live web fetches were required for this consult — the algorithmic families surveyed are well-established and the relevant literature is knowledge-stable.

**Primary sources (textbooks and formal papers):**
- Kellerer, H., Pferschy, U., Pisinger, D. (2004). *Knapsack Problems*. Springer. — Definitive reference for knapsack variants including bounded, multiple-constraint, and mixed-integer formulations. Chapter 11 covers multi-constraint knapsack LP relaxations.
- Garey, M.R., Johnson, D.S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. Freeman. — Multi-constraint 0/1 knapsack shown NP-hard (Theorem 4.1 implies it for ≥2 constraints); motivates greedy approximation and LP relaxation as standard approaches.
- Pisinger, D. (1995). "Algorithms for Knapsack Problems." PhD Thesis, University of Copenhagen. — Comprehensive survey of greedy, dynamic programming, and branch-and-bound approaches; greedy-with-repair analysis shows O(n log n) practical performance on real instances.

**Secondary sources (LP/MIP solver practical references):**
- Mitchell, S. (2011+). *PuLP: A Python Linear Programming Library*. — PuLP documentation for open-source LP/MIP modeling with CBC; confirms 90K binary variable tractability range.
- Forrest, J., Lougee-Heimer, R. (2005). "CBC User Guide." INFORMS Tutorials in Operations Research. — CBC solver performance characteristics on MIP instances.
- Van Roy, T.J., Wolsey, L.A. (1987). "Solving Mixed Integer Programming Problems Using Automatic Reformulation." *Operations Research* 35(1). — Greedy rounding heuristics on LP relaxations; validates greedy-with-repair as near-optimal on loosely-constrained instances.

**Tertiary sources (simulated annealing applied to selection problems):**
- Kirkpatrick, S., Gelatt, C.D., Vecchi, M.P. (1983). "Optimization by Simulated Annealing." *Science* 220(4598):671-680. — Original SA paper; temperature schedule and convergence analysis.
- Assessment of SA for this problem class is consistent with the applied operations research consensus: SA adds scheduling overhead without benefit when constraint structure is near-linear and LP covers the gap-floor failure mode.

---

## Sign-off

**Legolas** (Mode A research, 2026-05-25)
**Verdict:** greedy-with-swap-repair as baseline; PuLP+CBC as named LP fallback; parameter recommendations at § 5; cheapest refuting test (PCFS) at § 7 with ≥85% non-thin-cell floor satisfaction as pass threshold; resource projection confirms dispatch § 8 envelope (greedy path ~1.5 min / ~90-185 MB → mitigated to ~18-36 MB working set via column-selective load per § 6 note).
