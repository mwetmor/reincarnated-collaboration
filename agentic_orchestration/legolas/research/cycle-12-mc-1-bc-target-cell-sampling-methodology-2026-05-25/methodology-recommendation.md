# Methodology Recommendation — BC-Target Cell Sampling Methodology (MC-1)

**Mode:** A (analytical)
**Commissioner:** knight-rider (orchestrator) / for rocket Layer 2 dispatch authoring
**Date:** 2026-05-25
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-legolas-cycle-12-mc-1-bc-target-cell-sampling-methodology.md`
**Authority basis:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification + Discipline #18 LOAD-BEARING gate
**Sources consulted:** See § 11 (source list)

---

## Summary (5 sentences)

The BC-target cell sampling problem is structurally a stratified-with-coverage-floors selection over a 5-tuple cell space (22 occupied cells from ~25,920 Profile A cells) where three objectives compete: BC-space coverage uniformity, composition-policy register-share fidelity, and substrate-availability respect. Literature from MAP-Elites / Quality-Diversity research, procedural generation for ARPGs, and constrained-knapsack theory all point to the same structural finding: none of the three baseline methods (uniform, composition-policy-weighted, substrate-coverage-aware) alone is sufficient, and a two-stage hybrid — policy-weighted enumeration with substrate-availability pre-filtering — handles the interaction effects most cleanly. The L11 strict 4-tuple matching requirement is load-bearing for the sampling design because it forces the generator to surface substrate availability BEFORE committing to a cell, which directly argues against pure uniform sampling (which would generate kits in substrate-empty cells and hit L6/§4 thin-cell fallback on every critical cell). The recommended method is deterministic per-cell-fired-once enumeration with composition-policy-weighted tie-breaking at shared 4-tuple cell-pairs, preceded by a substrate-coverage pre-filter that marks cells as blocked (zero substrate match under strict L11) or thin (below a configurable floor), with thin cells routed to a named fallback path rather than discarded. The cheapest refuting test is a per-register-share audit on 100 kits: if any register deviates more than ±10pp from its policy v1 § 1 target, the sampling method is mis-calibrated and must be revised before production scale fires.

---

## 1. Problem characterization — what the BC-target cell generator is solving

Before algorithm selection it is necessary to characterize the problem precisely.

### 1.1 The cell space

Per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3:

- Full 8-axis archive: 68,040 cells
- Profile A operational archive (deferred bins excluded — Axis 2A solo-only, Axis 5 HP-econ + starved + gen-spender + steady): 6 × 5 × 1 × 3 × 3 × 3 × 4 × 4 = 25,920 cells
- v1_scope cell coverage (per composition policy v1 § 2.4 + § 4.1): 22 occupied cells from the `canonical/story/v1-bc-target-intent-2026-05-24.md` Sketch A roster

The generator's scope is not 25,920 cells. It is ~22 cells that have design intent, substrate, and architectural coverage behind them. The sampling problem is: given these 22 cells (plus 5 shared 4-tuple pairs per composition policy v1 § 4.2), in what order and with what weighting should the generator instantiate kits?

### 1.2 The 5-tuple coordinate

Per framing brief § 2 + composition policy v1 § 2.4:
- Tuple: `(range, tempo, amplitude, attribute, proxy_density)`
- 5-tuple cell-pair sharing: 5 pairs share a 4-tuple substrate; proxy_density discriminated at form-generation via algorithm § 8.6 (composition policy v1 § 4.2 Table)

The 4-tuple / 5-tuple distinction is load-bearing for L11 strict matching:
- **4-tuple**: `(range, tempo, amplitude, attribute)` — the substrate-binding match key
- **5-tuple**: adds proxy_density — discriminated post-substrate-binding by form-generation algorithm

### 1.3 Substrate availability tiers

Per Cycle 10 wind-down (per-tier counts in the dispatch):
- Tier S: 532 items in v1_scope
- Tier A: 1,431 items in v1_scope
- Tier B: 1,056 items in v1_scope
- Tier C: 23 items in v1_scope
- **Total v1_scope: 3,042 items**

Critical: tier counts are global. **Per-cell** substrate density varies significantly — composition policy v1 § 4.1 documents cells with 0 typed items (Cell 14 Pyromantic Caster, Cell 15 Red Mage, Cell 17 Necromancer Summoner, Cell 23 Monk-archetype) and cells with only 2-8 typed items (Cells 13, 19, 22, 24, 25). Under L11 strict 4-tuple matching, thin cells are not "low-density sampling targets" — they are cells where substrate-binding may fail entirely, requiring routing to named fallback paths.

### 1.4 Optimization objectives

Three objectives are in tension:

| Objective | What it wants | Risk of over-weighting |
|---|---|---|
| **BC-space coverage uniformity** | Equal probability across all 22 cells | Over-represents thin cells; generates substrate-binding failures |
| **Composition-policy fidelity** | Kit register-share matches v1 § 1 targets (historical ~50-55%, fantasy ~30-35%, military_modern ~5-8%) | Over-represents high-substrate historical cells; starves fantasy / WIS cells |
| **Substrate-availability respect** | Weight cells by v1_scope coverage; avoid thin cells | Over-represents thick cells; abandons thin cells that are architecturally important (Cell 14, 15, 17 are CRITICAL per composition policy v1 § 4.1) |

A method that optimizes any single objective in isolation creates pathology on the other two. The correct approach is a prioritized multi-objective design.

---

## 2. Literature scan — sampling methodologies in procedural generation contexts

### 2.1 MAP-Elites / Quality-Diversity (QD) research

The MAP-Elites algorithm (Mouret and Clune 2015; Cully et al. 2015) and its descendants fill an archive by:
1. Sampling from a behavioral space
2. Evaluating generated individuals against BC measurements
3. Placing accepted individuals in the archive cell that matches their measured BC coordinate

**Key finding:** MAP-Elites does NOT pre-sample target cells from the BC space. It generates individuals and DISCOVERS which cells they land in. This is fundamentally different from Reincarnated's Phase 2 problem, where the generator is told which cell to TARGET and must produce a kit that fits that target.

**Literature relevant to cell-targeted generation:** Interactive Constrained MAP-Elites (Alvarez et al. 2019; arxiv 1906.05175) and Deep Surrogate MAP-Elites (Gaier et al. 2018) both deal with structured BC spaces where generation is directed at specific cells. In these approaches, the "which cell to target next" question is answered by:
- **Novelty / emptiness priority**: target empty or under-filled cells preferentially
- **Improvement probability**: target cells where the generator is most likely to produce improvement (similar to Bayesian optimization acquisition functions)
- **Curriculum-based ordering**: target cells in a curriculum order from easiest-to-fill to hardest-to-fill

**For Reincarnated v1**: all 22 cells are "empty" at generation start (new engine; no prior archive). Novelty/emptiness priority collapses to "fill all 22 cells at least once" as the first objective. Improvement probability collapses to zero-knowledge prior at first generation. This means Reincarnated's v1 generation is closest to **deterministic enumeration** with policy-weighted ordering, not stochastic MAP-Elites exploration.

### 2.2 ARPG kit generation precedents

Per the prior methodology consult (`algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` § 1.1), no shipped ARPG uses algorithmically-targeted BC-cell generation. The closest structural analogues:

- **Diablo 4 legendary item generation**: pulls from a filtered substrate pool matching item class + ilvl + affixes; deterministic enumeration of item class × ilvl × affix combinations with randomized affix roll — structurally a stratified enumeration with per-stratum random draw
- **PoE craft bench**: deterministic pool filter (item base × affix tag) with weighted random draw from filtered pool
- **Last Epoch Forging**: deterministic item class filter + weighted random affix draw per tier; explicit floor on affix tier eligibility

**Common structural pattern across shipped ARPGs:** deterministic eligibility filter (must satisfy structural constraints) THEN weighted random draw from eligible pool. None use pure uniform sampling across the unfiltered pool.

### 2.3 Procedural content generation (PCG) theory

From PCG literature (Smith et al. 2011; Shaker et al. 2016):

**Stratified sampling** is the standard approach when a generation space has known strata with different properties. For BC-target cell generation, the strata are the 22 cells. Stratified sampling guarantees each stratum gets at least one draw — directly matching the "all 22 cells filled at least once" v1 objective.

**Rejection sampling** (generate-then-test) is the alternative: generate kits freely, test whether they match a target cell, reject those that don't. This has two failure modes for Reincarnated:
1. Under Architecture B, substrate binding happens at Phase 2 — the generator must SELECT a specific substrate row, not generate freely and test. Rejection sampling would require discarding substrate rows and regenerating, which wastes the substrate-binding design benefit.
2. Thin cells with near-zero substrate availability would produce near-100% rejection rates, making the generator functionally useless for those cells.

**Rejection sampling is not viable for this architecture.**

**Importance sampling** (weight cells by their estimated contribution to the objective) is viable but requires knowing the objectives before generation. Composition policy v1 § 1 provides exactly this: register-share targets and register-share-cap are the objective weights.

### 2.4 Constrained knapsack / constrained sampling theory

The Stage 3 methodology consult (`cycle-10-stage-3-methodology-consult-2026-05-25/methodology-recommendation.md`) characterized the substrate selection problem as a constrained knapsack. The BC-target cell sampling problem is structurally different:

- **Stage 3 (substrate curation)**: select which substrate rows enter v1_scope from 89K candidates — LARGE pool, constrained selection
- **MC-1 (kit generation cell targeting)**: select which cells to generate kits for, in what order, with what substrate draw policy — SMALL set (22 cells), constrained ordering + draw

At 22 cells, the "optimization" overhead of LP or MIP is overkill. The problem is structurally tractable by deterministic enumeration with weighted draw.

---

## 3. Per-methodology analysis — the three baselines

### 3.1 Baseline A: Uniform sampling

**What it does mathematically:** assigns equal probability weight 1/22 to each of the 22 cells. Generator draws a cell uniformly at random for each kit to produce.

**Sampling distribution shape:** flat categorical distribution over {cell_1, ..., cell_22}. With replacement (multi-fire): Poisson distribution per cell at expected count = N_total / 22. Without replacement: one kit per cell guaranteed, then remainder draws uniformly.

**Pros:**
- Maximum BC-space coverage uniformity by design
- Simple to implement and audit
- No parameter decisions required

**Cons:**
- Ignores composition-policy register-share targets entirely — generated register distribution will match substrate availability within cells, not composition policy v1 § 1 targets. If thick historical cells dominate within their cells, kit output register distribution will be historical-heavy regardless of uniform cell weighting.
- Ignores substrate availability — weights Cell 14 (0 typed items pre-gap-fill) equally with Cell 7 (thick DEX ranged substrate). Under L11 strict matching, Cell 14 hits thin-cell fallback immediately; uniform sampling keeps "trying" to instantiate kits in unresolvable cells.
- At 22 cells, uniform sampling produces 1 kit per cell in a per-cell-fired-once run, OR a flat expected distribution in a multi-fire run. Neither respects the composition policy's intent that some cells (proxy-heavy, STR/DEX martial) are architecturally primary and should have higher representation.
- Cannot distinguish the 5 cell-pair shared 4-tuple groups: uniform sampling treats Cell 1 (Heavy Barbarian, proxy=none) and Cell 5 (Ancestor-Warrior, proxy=light) as independent, but they share the same 4-tuple substrate pool. Sampling both uniformly may starve the shared pool.

**Verdict:** Uniform sampling is technically correct only if BC-space coverage uniformity is the SOLE objective. Composition-policy alignment and substrate-availability respect are also required objectives per the dispatch scope. Uniform fails both.

### 3.2 Baseline B: Composition-policy-weighted sampling

**What it does mathematically:** assigns per-cell weights based on composition policy v1 § 1 register-share targets + § 2.4 mechanical-cell weights. Higher-weight cells get more kits in proportion.

**Sampling distribution shape:** categorical distribution with per-cell weights proportional to:
```
w(cell_i) = (register_share_target(cell_i) × attribute_weight(cell_i) × proxy_density_weight(cell_i))
```
Normalized to sum to 1 across the 22 cells.

**Pros:**
- Directly honors composition policy v1 § 1 at the kit-generation scale
- Produces register-share distribution that matches targets at ensemble scale (100+ kits)
- Compatible with the policy's existing structure — uses the same weight table that Stage 3 used for substrate curation
- Per-cell-fired-once variant: weights determine the ORDER in which cells get their first kit, then secondary fires fill in proportionally

**Cons:**
- Ignores substrate availability — high-weight cells that are also thin cells (e.g., Cell 19 Channeling Cleric: WIS cells are structurally thin at Tier S/A per composition policy v1 § 11.1) will be weighted highly but frequently fail under L11 strict matching
- The weight table in composition policy v1 § 2.4 is defined at the SUBSTRATE CURATION level, not per generated kit. There is a level-of-analysis mismatch: the policy targets govern what substrate is IN v1_scope; using those same weights as per-kit generation weights assumes that kit register distribution should match substrate register distribution 1:1. This may not hold — the register-share target at the v1_scope level (~50-55% historical substrate) does not necessarily mean ~50-55% of generated kits should be historically-anchored, because some cells (e.g., all STR/DEX martial cells) draw only from historical/fantasy substrate by construction while INT/WIS cells may have more cross-register options.
- Does not distinguish composition-policy weight from design-intent priority: a cell can be low-weight in the policy (e.g., Cell 17 Necromancer Summoner, fantasy/INT/proxy-heavy) but architecturally CRITICAL (listed as CRITICAL in § 4.1 thin-cell table). Policy-weighted sampling under-generates for CRITICAL cells that happen to have low register-share weight.

**Verdict:** Composition-policy-weighted sampling is better than uniform for register-share alignment, but creates a systematic bias against architecturally-critical thin cells that have low policy weight. Requires augmentation to handle thin cells.

### 3.3 Baseline C: Substrate-coverage-aware sampling

**What it does mathematically:** assigns per-cell weights based on v1_scope substrate availability at the 4-tuple level. Cells with more eligible substrate get proportionally more generation fires.

**Sampling distribution shape:** categorical distribution with per-cell weights proportional to:
```
w(cell_i) = count(v1_scope rows matching 4-tuple(cell_i) under L11 Option α/β/C)
```

Per Cycle 10 wind-down tier counts (S=532, A=1431, B=1056, C=23), applied per-cell:

| Cell type | Substrate availability category |
|---|---|
| STR/DEX martial cells (Options α) | Generally thick — historical/fantasy physical weapons well-covered |
| INT/WIS caster cells (Option β) | Generally thin — Tier S has 0 INT, 8 WIS; Tier A has 8 INT, 21 WIS |
| Critical thin cells (Cell 13, 14, 15, 17, 19, 22, 23, 24, 25) | Near-zero to low typed substrate |

**Pros:**
- Directly avoids substrate-binding failures under L11 strict matching
- Reduces thin-cell fallback invocation by steering generation toward substrate-rich cells
- Self-calibrating: as substrate enrichment fills thin cells (Sidecar B + Stage 3.5 gap-fills), the weights automatically update

**Cons:**
- Severely under-generates for architecturally-critical thin cells — the exact cells that NEED form-generation most (Cell 14 Pyromantic Caster, Cell 15 Red Mage, Cell 17 Necromancer Summoner, Cell 23 Monk) are the cells substrate-coverage-aware sampling deprioritizes most aggressively
- Produces register-share skew toward historical (already the thickest substrate stratum per composition policy v1 § 11.2), directly contradicting the fantasy ~30-35% target
- Ignores design intent: the composition policy's architectural decision to route CRITICAL thin cells through gap-fills + fallbacks is precisely to ensure those cells DO get generated even at thin substrate. Substrate-coverage-aware sampling would abandon that architectural intent silently.

**Verdict:** Substrate-coverage-aware sampling optimizes for the wrong objective when used as a primary weight. It is useful as a PRE-FILTER (block cells with zero eligible substrate under strict L11) but not as a primary weight for cell selection. Its role is gate-keeping (substrate check before commit), not probability assignment.

---

## 4. Hybrid options analysis

### 4.1 Hybrid H1: Uniform-with-composition-policy-bias

**Mechanism:** Start with uniform weights (1/22 per cell). Apply composition-policy weights as a bias term: `w(cell_i) = 1/22 + α × policy_weight(cell_i)` for α ∈ [0, 1]. At α=0, pure uniform; at α=1, pure composition-policy-weighted.

**Assessment:** Maintains BC-space coverage uniformity as the primary objective while adding policy alignment. However, it inherits both parent methods' failure to handle thin cells. At α values that produce meaningful policy alignment, thin cells with low policy weight are still deprioritized. Does not address L11 strict-match substrate failures.

**Verdict:** Partial improvement over uniform. Insufficient — does not address the substrate-availability blocking problem.

### 4.2 Hybrid H2: Substrate-coverage-aware-with-policy-renormalization

**Mechanism:** Start with substrate-coverage-aware weights. Renormalize so that the expected register-share across generated kits matches policy v1 § 1 targets. Cells that are thin by substrate but important by policy get a weight floor (minimum weight regardless of substrate count).

**Assessment:** Better than pure substrate-coverage-aware — the renormalization restores policy fidelity. The weight floor for CRITICAL thin cells preserves architectural intent. However:
- The renormalization requires knowing per-cell register distribution, which is a function of which specific substrate rows are eligible under L11 matching — a non-trivial lookup
- The weight floor for CRITICAL thin cells means the generator will still attempt to instantiate kits in those cells, hitting thin-cell fallback paths per composition policy v1 § 4.1

**Verdict:** Closest to viable of the two baseline hybrids. Still leaves the substrate-availability pre-filter question unresolved (should the generator attempt CRITICAL thin cells before Sidecar B / gap-fill lands?).

### 4.3 Hybrid H3 (Recommended): Deterministic per-cell-fired-once enumeration with substrate pre-filter and policy-weighted ordering

**Mechanism (two-stage):**

**Stage 1 — Substrate pre-filter (runs once at generation start):**
```
for each cell in the 22 v1_scope cells:
    count_eligible = count(v1_scope rows matching 4-tuple(cell) under L11 Option α/β/C)
    if count_eligible == 0:
        cell.status = BLOCKED  # no substrate match possible; route to gap-fill / architectural decision
    elif count_eligible < thin_cell_floor (configurable; suggested: 5):
        cell.status = THIN     # eligible but sparse; route to named fallback path per composition policy v1 § 4
    else:
        cell.status = READY    # eligible for normal generation
```

**Stage 2 — Ordered enumeration with policy-weighted priority:**
```
# Order READY cells by generation priority:
# Primary: composition-policy register-share targets (highest-weight cells first)
# Secondary: per-attribute balance (ensure STR/DEX/INT/WIS cells interleave)
# Tertiary: alphabetical cell ID (deterministic tie-breaking)

priority_order = sort(READY_cells, key=policy_weight_descending)

# Fire each cell exactly once (per-cell-fired-once):
for cell in priority_order:
    substrate_row = draw_substrate(cell, v1_scope, L11_matching_policy)
    kit = generate_kit(bc_target=cell, substrate=substrate_row)
    emit(kit)

# Handle THIN cells after READY cells complete:
for cell in THIN_cells:
    # Invoke composition policy v1 § 4.1 routing (fold / gap-fill / fallback per cell's named action)
    # Example: Cell 13 (Artillery Mage) → fold into Cell 12 via T4 alteration (per § 4.1 Table)
    # Example: Cell 14 (Pyromantic Caster) → Stage 3.5 gap-fill substrate → generate once gap-fill lands
    handle_thin_cell(cell, routing=composition_policy_v1_section_4_table)

# BLOCKED cells: surface to gandalf + KR for architectural decision
report_blocked_cells(BLOCKED_cells)
```

**Stage 2B — Multi-fire extension (if N_kits > 22):**
For generating more than one kit per cell (e.g., 100 kits total across 22 cells):
```
# Assign per-cell quota proportional to policy weight:
total_quota = N_kits - 22  # first 22 fires consumed by per-cell-fired-once above
for cell in READY_cells:
    additional_quota(cell) = round(total_quota × policy_weight(cell))

# Draw substrate without replacement up to v1_scope coverage for that cell;
# if quota exceeds unique substrate rows, draw with replacement (multi-instance from same substrate base)
for cell in READY_cells:
    for i in range(additional_quota(cell)):
        substrate_row = draw_substrate_nth(cell, i, v1_scope, replacement_policy)
        kit = generate_kit(bc_target=cell, substrate=substrate_row)
        emit(kit)
```

**Why H3 is the correct recommendation:**

1. **L11 strict-match compatibility**: the substrate pre-filter runs BEFORE any kit generation commitment. BLOCKED cells never reach the generation loop. THIN cells route to their named fallback per composition policy v1 § 4.1 rather than hitting ad-hoc fallback silently. This matches the framing brief § L11 + § L6 design intent.

2. **Composition-policy alignment**: the policy-weighted ordering ensures that kits are generated in priority order by register-share weight. If generation halts early (system resource limit; time cap), the highest-priority cells have been filled. Register-share targets are achieved at ensemble scale because per-cell quota is proportional to policy weight.

3. **BC-space coverage uniformity**: per-cell-fired-once guarantees every READY cell gets at least one kit. This is the correct uniformity guarantee given that cells are architecturally equal in importance-of-existence (every cell should exist in the archive), not equal in frequency-of-occurrence (composition policy targets govern frequency).

4. **Deterministic**: the ordering is fully deterministic given fixed inputs (v1_scope contents, policy weights, thin_cell_floor value). This supports Disciplines #10 (change one thing, measure one thing) and #6 (tag intermediate states — deterministic generation is reproducible at any intermediate tag).

5. **THIN cell handling preserves architectural intent**: routing THIN cells to their named fallback per composition policy v1 § 4.1 table means the thin-cell architectural decisions (fold Cell 13 into Cell 12; gap-fill Cell 14; Option C for Cell 15; etc.) are CONSUMED by the generator rather than bypassed.

6. **Separates two concerns cleanly**: (a) which cells to attempt (substrate pre-filter governs); (b) in what order and proportion (policy weights govern). These are different decisions and should not be conflated in a single weight function.

---

## 5. Interaction with L11 strict 4-tuple matching

L11 strict 4-tuple matching (framing brief § L11) mandates that kit generation + gauntlet sim uses strict 4-tuple BC-target matching per composition policy v1 § 3 Option α/β/C matching strategies.

**The sampling design must accommodate two distinct failure modes under strict matching:**

### 5.1 Failure mode A: Cell blocked (zero substrate)

Cells with zero v1_scope rows matching their 4-tuple under the applicable matching policy cannot be instantiated under strict L11 without violating the constraint. These cells must be identified by the substrate pre-filter BEFORE the generator commits to instantiating a kit.

**Cells currently blocked or near-blocked** (per composition policy v1 § 4.1 and § 11.1):

| Cell | Status | v1_scope rows (approx) | L11 action |
|---|---|---|---|
| 14 Pyromantic Caster `(mid, low, spiky, INT)` | CRITICAL (0 typed) | 0 pre-gap-fill | BLOCKED until Stage 3.5 gap-fill lands; then THIN → READY |
| 15 Red Mage/Spellsword `(melee, high, flat, INT)` | CRITICAL (0 typed) | 0 typed; Option C allows STR-melee substrate | THIN via Option C — cross-attribute with ω-penalty |
| 17 Necromancer Summoner `(mid, low, spiky, INT, heavy)` | CRITICAL (0 typed) | 0 typed | BLOCKED until Sidecar B fantasy-coinage Necro lands |
| 23 Monk-archetype `(melee, high, variable, WIS)` | CRITICAL (0 typed) | 0 typed | THIN via Option C (quarterstaff cross-attribute) after Stage 4 rescue |

**Generator behavior for BLOCKED cells:** do not attempt generation; surface to KR for routing per composition policy v1 § 4.1 named action. Do not silently skip — BLOCKED cells must be reported, because a missing cell in the archive is an architectural gap that affects BDI test framework readiness (Cycle 13+).

### 5.2 Failure mode B: Cell thin (substrate present but sparse)

Cells with substrate but below a floor threshold create a different risk: the generator can instantiate kits, but diversity within the cell is limited (all kits from the same small pool of substrate rows). Under Mahalanobis duplicate detection at Phase 4 archive insertion, kits from thin-cell substrate may be rejected as duplicates.

**Implication for H3 design:** the `thin_cell_floor` parameter in the substrate pre-filter should be set relative to the minimum required substrate variety for meaningful within-cell diversity. Per `qd-engine-bc-axes-lock-2026-05-20.md` § 6 (Substrate variety rule: ≥5× per axis, ~25 templates per bin), a thin_cell_floor of 5 (at minimum 5 distinct eligible substrate rows) is the minimum viable floor for a single kit per cell. For multi-fire generation, the floor should scale with kit quota: `thin_cell_floor = max(5, kit_quota_for_cell)`.

### 5.3 Interaction with cell-pair sharing

The 5 shared 4-tuple cell-pairs (composition policy v1 § 4.2 Table) have a single substrate pool shared across both cells in the pair:

| Pair | Cell A (proxy=none) | Cell B (proxy=light/heavy) | Shared pool implication |
|---|---|---|---|
| 1 | Cell 1 Heavy Barbarian | Cell 5 Ancestor-Warrior | Both cells draw from `(melee, low, spiky, STR)` substrate |
| 2 | Cell 7 Archer | Cell 10 Falconer | Both from `(ranged, high, flat, DEX)` |
| 3 | Cell 12 Standard Wizard | Cell 16 Arcane-Familiar Mage | Both from `(ranged, medium, variable, INT)` |
| 4 | Cell 14 Pyromantic Caster | Cell 17 Necromancer Summoner | Both from `(mid, low, spiky, INT)` — BOTH currently BLOCKED |
| 5 | Cell 19 Channeling Cleric | Cell 25 Witch Doctor Petmaster | Both from `(mid, medium, variable, WIS)` |

**Sampling implication for shared pools:** if both cells in a pair are generated independently, they draw from the same v1_scope substrate pool. Without coordination:
- Both kits may draw the same substrate row (duplicate substrate in two different cells)
- The shared pool may be exhausted if thin (Cell 14/17 pair: BOTH blocked; Cell 19/25 pair: BOTH listed as CRITICAL)

**H3 behavior for shared-pool cell-pairs:** the substrate pre-filter must be computed at the 4-tuple level (shared pool), not per-cell:
```
for each 4-tuple in the 5 shared pairs:
    count_eligible_in_pool = count(v1_scope rows matching 4-tuple)
    mark both cells' substrate availability from this shared count
    if count_eligible_in_pool < 2 × thin_cell_floor:
        mark both cells as THIN (shared pool too thin to differentiate both kits)
    elif count_eligible_in_pool == 0:
        mark both cells as BLOCKED
```

For THIN shared-pool pairs, the generator should draw without replacement across both cells: Cell A draws first from the shared pool, Cell B draws second from the remaining pool. This maximizes substrate diversity within the pair's coverage.

---

## 6. Composition policy v1 alignment analysis

### 6.1 Level-of-analysis distinction: substrate curation vs kit generation

The register-share targets in composition policy v1 § 1 (historical ~50-55%, fantasy ~30-35%, military_modern ~5-8%) were designed as constraints on the SUBSTRATE CURATION selection (Stage 3 — which rows enter v1_scope). They are NOT necessarily the correct targets for the kit GENERATION distribution.

This distinction matters because:

- **At the substrate curation level**: register-share targets govern the composition of the v1_scope pool from which kits draw.
- **At the kit generation level**: the register distribution of generated kits depends on (a) which cells are generated and (b) what substrate exists in those cells.

If all STR/DEX martial cells (Option α) contain predominantly historical substrate (true per composition policy v1 § 11.2: "Tier S over-represents historical at 82%"), then even if the generator weights STR/DEX cells at exactly their policy-specified share, the kit register distribution will skew historical beyond the policy target — because the substrate within those cells is historical-dominated.

**Recommendation for policy alignment:** the generator should track register distribution of GENERATED kits (not just cell weights) and compare against policy v1 § 1 targets. The per-register-share audit in the cheapest refuting test (§ 8) provides the feedback signal. If generation produces a historical-heavy kit distribution despite correct cell weights, the appropriate correction is at the SUBSTRATE level (further fantasy substrate enrichment for martial cells), not by overriding the generator's cell weights.

**The generator should not apply composition-policy register-share targets as generation-time rejection filters** — that would be Discipline #13a-partition drift (partitioning by substrate identity at the generation layer). The targets are post-hoc diagnostic criteria for the audit, not pre-hoc rejection gates.

### 6.2 Option α/β/C alignment

Per composition policy v1 § 3 and framing brief § L11:

- **Option α (martial cells — STR/DEX primary):** 5-tuple mechanical-fingerprint match required. Generator must pull a weapon from v1_scope where `weapon_mechanical_profile` matches the BC-target 4-tuple (range × tempo × amplitude × attribute).
- **Option β (caster cells — INT/WIS primary):** attribute-level match only. Generator pulls any weapon from v1_scope where `proxy_attribute_class == attribute`.
- **Option C (hybrid cells — Red Mage, Monk, Holy Knight):** cross-attribute wielding with ω-penalty. Generator may pull from the dominant attribute's pool with explicit ω-penalty flag.

**Generator substrate draw procedure per matching policy:**
```python
def draw_substrate(cell, v1_scope, L11_matching_policy):
    if L11_matching_policy == "option_alpha":
        # Strict 5-tuple mechanical-fingerprint match
        eligible = v1_scope.filter(
            proxy_range_class=cell.range,
            proxy_tempo_class=cell.tempo,
            proxy_geometry_class=cell.amplitude,  # geometry maps to amplitude in BC
            proxy_attribute_class=cell.attribute
        )
    elif L11_matching_policy == "option_beta":
        # Attribute-level match only
        eligible = v1_scope.filter(proxy_attribute_class=cell.attribute)
    elif L11_matching_policy == "option_c":
        # Cross-attribute with ω-penalty flag
        eligible = v1_scope.filter(proxy_attribute_class=cell.attribute)
        eligible = eligible.union(
            v1_scope.filter(proxy_attribute_class=cell.cross_attribute_secondary)
                    .mark(omega_penalty=True)
        )
    # Tier-priority draw within eligible pool:
    return tier_priority_draw(eligible)  # Tier S first; Tier A preferred; Tier B standard; Tier C floor-only
```

### 6.3 Thin-cell fallback alignment

Composition policy v1 § 4.1 specifies named actions for each CRITICAL thin cell. The generator must consume these routing decisions, not invent its own:

| Cell | Policy-specified action | Generator implementation |
|---|---|---|
| Cell 13 Artillery Mage | FOLD into Cell 12 via T4 alteration | Cell 13 maps to Cell 12 substrate draw; T4 alteration applied at § 8 algorithm |
| Cell 14 Pyromantic Caster | Stage 3.5 engine-author gap-fill | BLOCKED until gap-fill lands; then draw from gap-fill entries |
| Cell 15 Red Mage | Option C (STR-melee substrate + INT-flavored kit) | Option C cross-attribute draw with ω-penalty |
| Cell 17 Necromancer Summoner | Sidecar B fantasy-coinage Necro + § 8.6 proxy-spawn | BLOCKED until Sidecar B lands; then draw from new substrate |
| Cell 19 Channeling Cleric | Sidecar B WIS-broad enrichment | THIN; draw from available WIS substrate; re-evaluate when Sidecar B lands |
| Cell 22 Storm Caller/Druid | Sidecar B Celtic/Druidic enrichment | THIN; similar to Cell 19 |
| Cell 23 Monk-archetype | Sidecar B East-Asian fist-and-staff + Option C | THIN via Option C; draw from quarterstaff cross-attribute |
| Cell 24 Druid Beastmaster | Sidecar B Celtic/Pacific + proxy-spawn | THIN; limited draw from available WIS substrate |
| Cell 25 Witch Doctor Petmaster | Sidecar B Sub-Saharan-African + proxy-spawn | THIN; shared pool with Cell 19 per pair 5 |

**Generator must not invent fallback routing for CRITICAL cells** — the named actions above are design decisions locked at the Stage 3 design call. Any deviation from the named routing requires escalation to gandalf per cycle-12-hive-mind-scope.md § 5.

---

## 7. Deterministic vs probabilistic — recommendation

The dispatch asks: should the recommended method be **deterministic** or **probabilistic**?

**Recommendation: deterministic per-cell-fired-once enumeration for v1; probabilistic multi-fire extension for N_kits > 22.**

**Rationale for deterministic at v1:**

1. **All 22 cells must be generated** — at v1, the primary constraint is ensuring every architecturally-designed cell exists in the archive. This is a coverage guarantee, not a distribution optimization. Deterministic per-cell-fired-once is the only method that makes this guarantee by construction.

2. **Reproducibility** — a deterministic generator with a fixed seed produces the same kit for the same cell on every run. This supports Discipline #10 (attribution clarity) and Discipline #6 (tag intermediate states): each intermediate tag represents a specific, reproducible kit set.

3. **Cheapest-refuting-test compatibility** — the cheapest refuting test (§ 8) runs 100 kits and audits register-share distribution. With a deterministic generator, the 100-kit output is stable across audit runs. With a probabilistic generator, different audit runs may produce different register distributions — making the ±10pp threshold hard to evaluate without statistical aggregation.

4. **Small archive at v1** — with 22 cells (possibly 37 forms per `canonical/story/v1-bc-target-intent-2026-05-24.md` Sketch A), the kit set is small enough that deterministic enumeration is not a computational burden. Stochastic exploration is valuable in MAP-Elites when the archive is sparse relative to a large cell space (per BC-axes-lock § 7.2: "sparse-by-design exploration"). At v1 with 22 target cells, there is no exploration benefit — the cells are architecturally designed, not discovered.

**Rationale for probabilistic at multi-fire (N_kits > 22):**

Once all 22 cells have been generated once, additional kit generation within each cell benefits from stochastic substrate draw (sampling different substrate rows from within the same cell's eligible pool). This produces within-cell diversity — kits in the same BC-target cell with different cultural traditions, named-bearer anchors, and element compositions. The policy-weighted quota per cell (Stage 2B in H3 mechanism above) provides the structural constraint; the substrate draw within quota is random with tier-priority weighting.

**Per-cell-fired-once vs multi-fires — recommendation:**

- **v1 initial generation:** per-cell-fired-once (one kit per cell; 22 kits total for the 22 cells)
- **Multi-fire extension:** governed by Stage 2B quota allocation proportional to policy weights; substrate draw within quota is random-with-replacement after available unique substrates are exhausted
- **Whether cells in different tiers warrant different behavior:** YES. Tier-S substrate kits should be the first draw from each cell (highest fidelity; legendary-tier exemplars per Architecture B § 5.5); Tier-A draws second; Tier-B/C fill multi-fire quota. This means the per-cell-fired-once initial draw is also the Tier-S draw.

---

## 8. Cheapest-refuting-test design (per Discipline #19.1)

### 8.1 The claim to refute

The H3 recommended methodology's core claim: **the per-cell-fired-once enumeration with substrate pre-filter and policy-weighted ordering produces a kit register distribution within ±10pp of composition policy v1 § 1 targets at 100-kit scale.**

Secondary claim: **all BLOCKED cells are correctly identified and surfaced (no silent failures); all THIN cells route to their named fallback rather than causing generation errors.**

### 8.2 Test design

**Test name:** BC-target cell sampling register-share audit

**Scale:** 100 kits total (sufficient for register-share measurement at ±10pp resolution; at N=100, a ±1 kit = ±1pp, so ±10pp is measurable with a single pass)

**Procedure:**

1. Run H3 generator on the 22 v1_scope READY cells (substrate pre-filter applied; BLOCKED/THIN cells logged separately)
2. For multi-fire to reach 100 kits: apply Stage 2B quota allocation with policy weights; draw additional kits per quota
3. For each generated kit: record `register_canonical` of the bound substrate row (historical / fantasy / military_modern / mythological)
4. Compute per-register share: `register_share[r] = count(kits where substrate.register == r) / 100`
5. Compare against policy v1 § 1 targets:
   - historical: target 50-55%, floor 45%, ceiling 60%
   - fantasy: target 30-35%, floor 25%, ceiling 40%
   - military_modern: target 5-8%, floor 0%, ceiling 12%
   - mythological: target ~1% (only ~30 rows in v1_scope after Stage 4 rescue)

**Pass thresholds:**
- **PASS**: all four register shares within ±10pp of their target midpoint (historical: 45-65%; fantasy: 20-45%; military_modern: 0-18%; mythological: 0-11%)
- **FAIL (register-share)**: any register share outside the ±10pp band → sampling method is mis-calibrated; revise Stage 2B quota allocation or composition policy weight table
- **FAIL (silent blocked)**: any BLOCKED or THIN cell that does not appear in the pre-filter report → pre-filter is incomplete; review substrate availability query
- **FAIL (routing error)**: any CRITICAL thin cell that routes to a non-policy-specified fallback action → generator is inventing fallback behavior; fix to consume composition policy v1 § 4.1 table

**Compute cost:** 100 kits × Phase 2 generation cost. Phase 2 § 8 algorithm scan is < 2 ms/kit (per prior methodology consult § 6.1). Phase 3 convergence is NOT required for this test — the claim being tested is about substrate binding and register-share, not about balance convergence. The cheapest test measures ONLY the sampling + substrate draw step, not the full generation pipeline.

**Estimated wall time:** < 5 minutes at 100 kits × Phase 2 cost only. If Phase 3 is added: ~100 kits × 2-3 min/kit (abbreviated convergence per prior methodology § Q6.2: 20 iterations) = ~200-300 min. For the cheapest refuting test, Phase 3 is excluded.

**Why this is the cheapest refuting test:** The alternative (full pipeline run with Phase 3 convergence on 100 kits) costs ~200-300 min and tests many things simultaneously. The register-share claim is testable at Phase 2 output only — no convergence required. The ±10pp threshold is concrete and binary (pass/fail), not a distribution requiring statistical significance. 100 kits is sufficient for ±1pp resolution at the register-share measurement.

### 8.3 Alternative cheapest-refuting-test (if Phase 2 generation is not yet implemented)

**Static pre-filter verification:** before any kit generation, query the v1_scope substrate DB for each of the 22 cells and verify:
- READY cells have ≥ thin_cell_floor eligible rows under the applicable L11 matching policy
- BLOCKED cells have 0 eligible rows
- THIN cells have < thin_cell_floor eligible rows

This is a SQL audit, not a generation run. Cost: ~5 minutes of SQL queries against `~/Games/reincarnated-loadout/data/telemetry.db`. This validates the pre-filter logic without requiring any Layer 2 implementation.

---

## 9. Resource-bounds projection

### 9.1 Per-method compute envelope

| Component | H1 Uniform | H2 Composition-weighted | H3 Hybrid (recommended) |
|---|---|---|---|
| Substrate pre-filter | Not present | Not present | 1 SQL query per cell (22 queries); < 1 sec total |
| Cell ordering | O(1) (uniform = no ordering) | O(22 log 22) sort by weight | O(22 log 22) sort by weight |
| Per-kit substrate draw | O(N_eligible) scan per cell | O(N_eligible) scan per cell | O(N_eligible) scan per eligible cell only |
| Thin-cell routing | Ad-hoc (not specified) | Ad-hoc | Deterministic lookup in policy v1 § 4.1 table |
| Multi-fire quota | Uniform across cells | Proportional to policy weight | Proportional to policy weight |

For all three methods, Phase 2 kit generation cost dominates: each kit requires the § 8 strategy registry scan (< 2 ms), substrate draw (< 1 ms DB query), and skill kit composition. Phase 2 total per-kit cost is on the order of milliseconds. The sampling methodology itself contributes negligible overhead.

### 9.2 Per-100-kits scaling

| Method | Sampling overhead | Phase 2 per-kit | Phase 2 × 100 kits | Phase 3 per-kit (if included) | Phase 3 × 100 kits |
|---|---|---|---|---|---|
| H1 Uniform | < 5 ms total | < 5 ms | < 500 ms | 2-3 min (20 iter) | 200-300 min |
| H2 Composition-weighted | < 10 ms total | < 5 ms | < 500 ms | 2-3 min | 200-300 min |
| H3 Hybrid (recommended) | < 50 ms total (includes pre-filter SQL) | < 5 ms | < 500 ms | 2-3 min | 200-300 min |

**All three methods are compute-equivalent for Phase 2 sampling overhead.** The methodology choice has zero impact on runtime at any foreseeable kit scale. The 50 ms additional overhead for H3's substrate pre-filter is a one-time cost at generation start (not per-kit).

### 9.3 Per-1000-kits scaling

At 1,000 kits, Phase 3 convergence dominates entirely (1,000 × 2-3 min = 33-50 hours if run serially). The sampling methodology contributes < 1 second of additional overhead at any scale. **The methodology choice is not a resource concern at any foreseeable kit count.**

**Memory envelope:** H3's pre-filter result (22 cells × availability count + BLOCKED/THIN status) fits in < 1 KB. Policy weight table (22 cells × 5 axis weights) fits in < 1 KB. No memory concern.

### 9.4 Per-tier kit generation scaling (Cycle 10 wind-down tier counts: S=532, A=1431, B=1056, C=23 in v1_scope)

The substrate draw within each cell applies tier-priority ordering (Tier S first). At v1_scope counts:
- Tier S draws are available for approximately 22 × (532/22) ≈ 24 items per cell on average (but unevenly distributed — martial cells are thick; caster/WIS cells are near-zero)
- Tier A draws: 1,431 / 22 ≈ 65 items per cell on average
- Total v1_scope depth (3,042 items) means approximately 138 items per cell on average — sufficient for meaningful multi-fire diversity in thick cells; not sufficient for thin cells

**No per-tier quota adjustment is needed at the sampling methodology level.** Tier priority is handled within the substrate draw function (draw Tier S before Tier A before Tier B before Tier C). The sampling methodology governs CELL ORDERING, not tier ordering within cells.

---

## 10. Framing-audit checklist (per Discipline #23)

**Q1: What load-bearing framing assumptions does this methodology recommendation depend on?**

1. The 22 cells in `v1-bc-target-intent-2026-05-24.md` Sketch A are the authoritative v1 cell roster. If cells are added or removed post-ratification, the pre-filter and quota allocation must be recomputed.

2. Composition policy v1 § 1 register-share targets (historical ~50-55%, fantasy ~30-35%, military_modern ~5-8%) are the correct generation-time targets. As noted in § 6.1, these targets were designed for substrate CURATION, not kit generation. The cheapest refuting test (§ 8) will empirically surface whether applying them at generation-time produces out-of-band register distributions.

3. L11 strict 4-tuple matching is FIXED for Cycle 12 gauntlet sim. If this is amended to allow broader matching, the substrate pre-filter logic changes (eligible pool per cell grows; fewer BLOCKED cells).

4. The thin_cell_floor parameter (suggested: 5 eligible substrate rows) is a design choice, not a derived value. If the archive quality requirement changes (e.g., per BC-axes-lock § 6 the 5× rule requires ~25 distinguishable templates per bin), the floor should increase. For v1 initial generation, a floor of 5 is sufficient for one diverse kit per cell; for multi-fire generation the floor should scale with quota.

5. This recommendation assumes Sidecar B + Stage 3.5 gap-fills WILL land before the generator attempts BLOCKED cells. If they do not land before Layer 2 fires, BLOCKED cells remain unresolvable and the generator emits a documented gap rather than an error.

**Q2: What evidence currently in hand could refute these assumptions?**

1. Assumption 1 (22-cell roster): refutable by reading `v1-bc-target-intent-2026-05-24.md` Sketch A. Evidence currently in hand — the doc is readable. This report is anchored to that roster as-authored. If the roster differs, the pre-filter query set must be updated.

2. Assumption 2 (composition-policy targets at generation time): the cheapest refuting test (§ 8) will empirically refute or confirm this at 100-kit scale. Evidence currently NOT in hand — the test has not been run.

3. Assumption 3 (L11 strict matching fixed): confirmed by framing brief § L11 (Matt 2026-05-25). Not refutable within Cycle 12 scope.

4. Assumption 4 (thin_cell_floor = 5): refutable by running the static pre-filter SQL audit (§ 8.3) on `telemetry.db`. Evidence is available via DB query; not currently in hand.

5. Assumption 5 (Sidecar B + gap-fills land before BLOCKED cells are attempted): refutable by checking elrond SC-1/SC-2 and Stage 3.5 gap-fill completion status at generator fire time. Not currently in hand.

**Q3: If refutation evidence exists or is plausible, is the right move to refine the framing rather than execute as-framed?**

The two most actionable refinements:

- **Assumption 2 (register-share at generation time):** run the cheapest refuting test BEFORE Layer 2 generator implementation is complete — i.e., as a metadata-only audit (SQL query against v1_scope by cell and register). If the per-cell register distribution within v1_scope reveals that the majority of cells have historically-dominated eligible substrate, then policy-weighted cell ordering will not fix the generation-time register skew. This surfaces BEFORE code is written.

- **Assumption 4 (thin_cell_floor):** run the static pre-filter SQL audit NOW (5-minute DB query). This will surface exactly which cells are BLOCKED and which are THIN under current v1_scope state, and will inform whether thin_cell_floor = 5 is appropriate or should be adjusted.

**Neither of these pre-code checks is in scope for legolas Mode A research.** They are DB queries against live substrate data — appropriate for elrond or rocket to execute as part of Layer 2 dispatch setup. Surfacing this here as a pre-code framing refinement recommendation per Discipline #23 Q3.

---

## 11. MC-1 ↔ MC-2 dependency flag

**Assessment: MC-1 and MC-2 have a PARTIAL dependency that does not block either consult from returning independently, but creates a potential re-synthesis need.**

**Where the dependency surfaces:** H3's substrate draw procedure (§ 4.3, Stage 1 pre-filter + Stage 2 policy-weighted enumeration) specifies the CELL SELECTION logic but does not fully specify HOW the substrate row is drawn from within the eligible pool at the chosen cell. This within-cell substrate binding is MC-2's subject (substrate-binding heuristics: which specific weapon row from the eligible pool does the generator pull?).

**Concretely:** MC-1 recommends `draw_substrate(cell, v1_scope, L11_matching_policy)` as a function; it specifies the L11 matching policy and tier-priority ordering within the eligible pool. MC-2 will specify whether the within-cell draw is:
- Random with tier-priority (likely MC-2 recommendation)
- Deterministic (first eligible row by some ordering)
- Importance-weighted by cultural-tradition (matching cell's policy weights from composition policy v1 § 2.2)
- Guided by prior archive contents (diversity-seeking draw)

**Implication:** if MC-2 recommends a draw strategy that conflicts with H3's tier-priority assumption (e.g., MC-2 recommends importance-weighted by cultural-tradition, which may produce draws that deviate from tier-priority ordering), the within-cell draw procedure in H3 Stage 2 will need revision.

**KR routing recommendation:** MC-1 and MC-2 can return independently. KR should review both returns before authoring the Layer 2 rocket dispatch, and flag any MC-1 ↔ MC-2 conflict at the dispatch authoring step. The two consults are NOT sequentially dependent (neither needs the other's output to complete), but the Layer 2 dispatch authoring requires BOTH to have returned before the full Phase 2 generation procedure is specified.

---

## 12. Implementation-shape sketch (for Layer 2 rocket dispatch consumption)

This sketch is not implementation code — it is a specification surface for the Layer 2 dispatch. Rocket implements; this sketch governs what the implementation must do.

```
BC-TARGET CELL SAMPLING — IMPLEMENTATION SHAPE (H3 HYBRID)

INITIALIZATION (once at generator start):
  1. Query telemetry.db: for each of the 22 v1_scope cells,
     count eligible rows in v1_scope under L11 matching policy (Option α/β/C per cell type)
  2. For each shared 4-tuple pair (5 pairs): compute shared pool count
  3. Classify cells:
     BLOCKED: count == 0
     THIN: 0 < count < thin_cell_floor (thin_cell_floor = 5 for v1 initial; configurable)
     READY: count >= thin_cell_floor
  4. Log classification: BLOCKED cells → KR report; THIN cells → composition policy v1 § 4.1 routing table

PER-CELL-FIRED-ONCE PHASE (22 kits, one per READY cell):
  5. Sort READY cells by policy_weight_descending (composition policy v1 § 2 weight table)
  6. For each cell in sorted order:
     a. Draw substrate row from eligible pool (tier-priority: S > A > B > C; random within tier)
     b. Record substrate row ID and cell ID (v1_scope_composition_trace)
     c. Compose skill kit matching cell BC-target (Phase 2 Phase 1-6 per Architecture B § 5.2)
     d. Emit kit

  For shared 4-tuple pairs (where Cell A and Cell B are both READY):
     a. Draw Cell A substrate first (tier-priority)
     b. Draw Cell B substrate from REMAINING eligible pool (without replacement from pair's shared pool)
     c. Ensures substrate diversity within the pair

THIN CELL ROUTING PHASE (deferred; after READY cells complete):
  7. For each THIN cell:
     a. Look up named action in composition policy v1 § 4.1 Table
     b. Execute named action:
        FOLD: route to target cell (e.g., Cell 13 → Cell 12 substrate draw with T4 alteration)
        GAP-FILL: wait for Stage 3.5/Sidecar B substrate; then draw from gap-fill entries
        OPTION-C: cross-attribute draw with ω-penalty flag
     c. Log routing decision with cell ID + named action applied

MULTI-FIRE PHASE (if N_kits > 22):
  8. Compute per-cell additional quota: quota(cell) = round((N_kits - 22) × policy_weight(cell))
  9. For each READY cell, draw additional substrate rows per quota
     (with replacement after unique eligible pool exhausted)
  10. Apply same tier-priority ordering within each additional draw

REPORTING (after all phases complete):
  11. Emit per-register-share audit:
      register_distribution = {r: count(kits where substrate.register == r) / N_kits}
      Compare against policy v1 § 1 targets
      Flag ±10pp deviations (per cheapest-refuting-test thresholds)
  12. Emit BLOCKED cell list (zero eligible substrate)
  13. Emit THIN cell routing log (named fallback actions applied)
  14. Emit per-cell substrate draw trace (cell_id, substrate_row_id, tier, register, cultural_tradition)
```

---

## 13. Methodology recommendation summary

**Recommended method:** Hybrid H3 — Deterministic per-cell-fired-once enumeration with substrate-availability pre-filter (Stage 1) and composition-policy-weighted ordering (Stage 2); multi-fire extension proportional to policy weights (Stage 2B).

**Deterministic vs probabilistic:** Deterministic for v1 initial generation (per-cell-fired-once); probabilistic within-cell substrate draw for multi-fire extension.

**Per-cell-fired-once vs multi-fires:** Per-cell-fired-once as the base; multi-fire quota allocation by policy weight for N_kits > 22.

**Whether separate behavior for Tier-S/A/B/C cells is needed:** YES within each cell (substrate draw ordered Tier S > A > B > C); NO across cells (tier is a within-cell draw priority, not a cross-cell cell-ordering criterion).

**MC-1 ↔ MC-2 dependency:** PARTIAL. H3 specifies cell selection and tier-priority ordering; MC-2 specifies within-cell substrate draw heuristic. KR should review both before Layer 2 dispatch authoring. No blocking dependency — both consults can complete independently.

**Key departure from all three baselines:**
- Not purely uniform (which ignores policy + substrate availability)
- Not purely composition-policy-weighted (which ignores substrate blocking)
- Not purely substrate-coverage-aware (which abandons architecturally-critical thin cells)

H3 is a composition of all three: substrate pre-filter (from Baseline C), policy-weighted ordering (from Baseline B), and guaranteed coverage of all READY cells (from Baseline A's coverage uniformity intent) — with architecturally-correct routing for THIN and BLOCKED cells rather than silent failure or weight suppression.

---

## 14. Knowledge gaps not resolved

1. **Per-cell substrate counts under L11 matching.** This report does not have access to `telemetry.db` to run the substrate pre-filter query. The cell-by-cell BLOCKED/THIN/READY classification is not known from Mode A analysis alone. The static pre-filter SQL audit (§ 8.3) is the cheapest way to resolve this before Layer 2 fires.

2. **Per-cell register distribution within v1_scope.** Whether policy-weighted cell ordering produces register distributions matching policy v1 § 1 targets depends on the per-cell register composition of eligible substrate rows. This is empirically determinable via a SQL query but not from architecture docs alone.

3. **thin_cell_floor calibration.** The suggested floor of 5 is a prior from the BC-axes-lock § 6 substrate variety rule (≥5× per bin). Whether 5 is sufficient for meaningful within-cell diversity depends on how similar the 5 eligible substrate rows are to each other (if they are 5 variants of the same weapon type, within-cell diversity is limited even above the floor). A top-5 rep-audit per thin cell (per Discipline #25 semantic-layer rep-audit) would surface this.

4. **MC-2 within-cell substrate binding heuristics.** The within-cell draw procedure is specified as "tier-priority draw" here. MC-2 will refine this. If MC-2's recommendation differs materially from tier-priority ordering (e.g., adding cultural-tradition-weighted draw within tier), the Stage 2 implementation shape in § 12 will need corresponding amendment.

---

## 15. Source list

**Primary sources (project canonical docs):**
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — Cycle 12 framing brief; § 2 MC-1 scope; § 4 PlayerClass contract; § L6/L9/L11 design locks
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy v1; § 1 register-share targets; § 3 Option α/β/C matching; § 4 thin-cell routing; § 5 per-cell coverage; § 11 empirical grounding
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes; 5-tuple cell coordinate; bin definitions; § 6 substrate variety rules; § 7 Profile A cell count
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B Phase 2 substrate-binding; Option α/β/C policy; substrate-genre-flagging; Phase 1 BC-target queue
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` — Cycle 12 scope; workstream roster; pre-resolved known-unknowns
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` — prior methodology consult pattern; scored-candidate strategy registry; cheapest-refuting-test precedent; resource-bounds projection pattern
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-re-review-post-bc-shift-fail-2026-05-25.md` — Pattern A-deep methodology re-review; test-set construction discipline; measurement-instrument validity framing
- `agentic_orchestration/legolas/research/cycle-10-stage-3-methodology-consult-2026-05-25/methodology-recommendation.md` — constrained knapsack methodology precedent; greedy-with-swap-repair; resource envelope framing
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code; #10 change-one-thing; #18 methodology-before-execution; #18.2 extension hotspot timing; #19.1 cheapest-refuting-test operationalization; #23 framing-audit checklist; #24 single-parameter sweep isolation; #25 semantic-layer rep-audit

**Secondary sources (literature, 2026-05-25):**
- Mouret, Clune (2015). "Illuminating search spaces by mapping elites." arXiv:1504.04909. MAP-Elites original; archive-driven generation pattern.
- Cully, Clune, Tarapore, Mouret (2015). "Robots that can adapt like animals." Nature 521:503. Applied MAP-Elites; behavioral characteristic space design.
- Alvarez, Dahlskog, Font, Togelius, Cooper (2019). "Interactive Constrained MAP-Elites: Analysis and Evaluation of the Expressiveness of the Feature Space." arXiv:1906.05175. Interactive / directed cell-targeting in MAP-Elites; cell-blocked and thin-cell handling.
- Smith, Whitehead, Mateas (2011). "Tanagra: Reactive Planning and Constraint Solving for Mixed-Initiative Level Design." IEEE TVCG. Constraint-solving approach to PCG; deterministic enumeration with soft constraints.
- Shaker, Togelius, Nelson (2016). "Procedural Content Generation in Games." Springer. Chapter 4 (search-based methods) and Chapter 7 (constructive methods); stratified sampling vs rejection sampling in PCG contexts.
- Diablo 4 item generation reference: https://maxroll.gg/d4/resources/item-generation — deterministic eligibility filter + weighted random draw pattern in shipped ARPG.
- PoE craft bench methodology: https://www.poewiki.net/wiki/Crafting — filtered substrate pool + weighted affix draw; structural analogue to Option β caster cell substrate draw.

---

**Signed:** legolas (researcher and scout)
**For:** knight-rider MC-1 return → rocket Layer 2 dispatch authoring (BC-target subspace generator); parallel MC-2 (substrate-binding heuristics) pending before Layer 2 dispatch is fully specified.
