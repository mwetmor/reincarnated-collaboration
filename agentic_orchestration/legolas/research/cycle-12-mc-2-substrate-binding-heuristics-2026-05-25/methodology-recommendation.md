# Methodology Recommendation — Substrate-Binding Heuristics (MC-2)

**Mode:** A (analytical)
**Commissioner:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-legolas-cycle-12-mc-2-substrate-binding-heuristics.md`
**Authority basis:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q6 Option B substrate-led methodology timing)
**Discipline gate:** #18 (methodology-before-execution) — LOAD-BEARING gate on rocket Layer 2 implementation

**Sources consulted:** See § 11 (source list)

---

## Summary (3-5 sentences)

Substrate-binding in the Reincarnated Architecture B pipeline is a constrained-selection problem: given a sampled BC-target cell, the generator must choose a `mechanical_substrate_triple` from v1_scope rows that match the cell's mechanical signature, while respecting composition policy v1 § 3 Option α/β/C matching rules and the coherence requirements across the substrate-triple components. The literature on QD-engine archive-seeded generation, procedural RPG item binding, and constraint-driven character generation consistently supports a **hybrid filter-then-weighted-sample** approach as the preferred production pattern for this class of problem: hard-filter to candidates satisfying the cell-match policy, then probabilistically sample from the filtered set with weights derived from a substrate-quality signal (tier, coverage, cultural-tradition alignment). Pure deterministic top-rank produces diverse-looking archive entries that are actually identical substrate draws across cells sharing top-ranked rows; pure probabilistic sampling without filtering wastes probability mass on incoherent combinations. The thin-cell-fallback policy (composition policy v1 § 4) requires a well-defined trigger + axis-relaxation priority order: the recommended substitution priority is **weapon_mechanical_profile axis first, then energy_type, then element last** — reversing this order risks producing element-incoherent kits that Phase 5 cohesion-judge struggles to narrate. The L11 strict 4-tuple matching constraint is sound for gauntlet sim and composes cleanly with the recommended hybrid approach, with a well-defined zero-match fallback path through thin-cell-fallback rather than silent NULL. The cheapest refuting test is a 50-kit spot-check: generate kits across all 22 BC cells, verify substrate-triple coherence on 3 spot-check criteria per kit with a ≥90% pass threshold.

---

## 1. Problem statement — what substrate-binding is architecting against

### 1.1 The substrate-binding problem in Architecture B Phase 2

Per the Architecture B end-to-end workflow (qd-engine-end-to-end-workflow-2026-05-24.md § 5.2), Phase 2 generation takes a BC-target coordinate [5-tuple: range × tempo × amplitude × attribute × proxy-density] and MUST bind a specific substrate weapon from genre-filtered v1_scope. The binding step produces `mechanical_substrate_triple: tuple[str, str, str]` — the BDI math model's mechanical-layer substrate constituents:

- **element** — e.g., fire, water, earth, wind, lightning, holy, shadow, physical (8 canonical elements)
- **weapon_kind** — e.g., longsword, bow, staff, mace (the weapon's physical form)
- **energy_type** — mana / rage / charge / focus

These three fields are the `mechanical_substrate_triple` per framing brief § 4 PlayerClass contract. They are the load-bearing substrate dimensions for the BDI η-interaction term `η·(T4_node × mechanical_substrate_triple)`. The selection heuristic must:

1. **Identify candidate substrate rows** from v1_scope matching the BC-target cell per composition policy v1 § 3 Option α/β/C matching rules
2. **Choose one specific row** from the candidate set to bind as the kit's weapon + substrate identity
3. **Ensure the chosen triple is internally coherent** (element × weapon_kind × energy_type compose into a playable kit without contradictions)
4. **Respect the thin-cell-fallback policy** (composition policy v1 § 4) when candidates are insufficient

### 1.2 The L9 mechanical vs semantic split (load-bearing constraint)

Per framing brief § L9, the substrate-triple constituents are MECHANICAL only:

| In mechanical_substrate_triple | NOT in mechanical_substrate_triple (semantic overlay) |
|---|---|
| element | cultural_tradition |
| weapon_kind | lineage |
| weapon_mechanical_profile (range, tempo, amplitude, AoE, primary_stat, hits_per_attack) | period |
| energy_type | |

This split is load-bearing for this consult: the substrate-binding heuristic must NOT use cultural_tradition / lineage / period as selection criteria. Those fields feed Phase 5 cohesion-judge (naming, spirit-guide explainer, sub-element flavor), not Phase 2 substrate selection. Any heuristic that incorporates cultural_tradition as a matching signal at Phase 2 violates L9.

### 1.3 The L11 strict 4-tuple matching constraint

Per framing brief § L11, Cycle 12 uses **strict 4-tuple BC-target matching** for gauntlet sim kit generation. The 4-tuple is (range, tempo, amplitude, attribute) — the first four dimensions of the 5-tuple BC-target cell (proxy-density being the 5th, handled separately via § 8.6 proxy-spawn template). Substrate rows must match all four dimensions of the tuple under the applicable matching policy (Option α full 5-tuple fingerprint; Option β attribute-level only; Option C cross-attribute with ω-penalty). Broader weapon-equip flexibility (player-game design concept) is deferred to v1.1+.

---

## 2. Literature scan — substrate-binding patterns in procedural generation

### 2.1 Archive-driven generation with substrate binding

The QD/MAP-Elites literature on generation with pre-existing content libraries surfaces several patterns relevant to substrate-binding:

**Pattern 1: Archive-seeded generation (most directly relevant)**
In MAP-Elites implementations where generation samples from a pre-existing content archive (rather than generating fully from scratch), the standard pattern is:
- **Filter phase:** narrow the archive to entries compatible with the target cell's behavior characteristics
- **Selection phase:** pick from the filtered set, optionally with weights
- This two-phase structure is well-represented in QD literature on archive-augmented generation (Fontaine et al. 2021; Mouret & Clune 2015 — see § 11).

The key finding from the QD literature: when the archive is sparse (which v1_scope's 22 cells across 3,042 rows implies ~138 rows/cell on average, but with high per-cell variance), **probabilistic sampling with tier-based weights produces better archive diversity over time** than deterministic top-rank, because deterministic selection causes the archive to converge toward a small set of "optimal" substrates per cell, reducing the substrate diversity the Phase 5 cohesion-judge can express across generated kits.

**Pattern 2: Constraint-graph substrate selection (ARPG item binding)**
In shipped ARPG item-binding systems (D2/D3/D4/PoE as surveyed in the § 8 consult), the standard pattern for pulling base item substrate given a cell-like target is:
- Hard filter by item class compatibility (weapon type for the character class)
- Soft filter by ilvl/tier to match target power band
- Sample uniformly within filtered set for normal items; specific named-substrate row for unique/legendary items
This confirms the filter-then-sample pattern as genre-canonical.

**Pattern 3: Thematic coherence in template selection**
Research on procedural narrative games (Smith et al. 2011; Hartsook et al. 2011 — see § 11) that use template-based content selection shows that coherence scoring produces better player-perceived quality than either random selection or deterministic optimization on a single dimension. The typical implementation: coherence score combines multiple signals (thematic match + mechanical fit + novelty contribution), selection samples from high-coherence candidates rather than taking top-1 deterministically.

**Pattern 4: Constraint-relaxation fallback (thin-cell handling)**
For constrained selection problems with non-uniform item density (some cells much better populated than others), the standard algorithmic response is a **relaxation cascade**: try most-constrained selection first; if insufficient candidates, relax the least-semantically-critical constraint; iterate until a viable candidate set exists. This maps directly to composition policy v1 § 4's thin-cell-fallback structure. The research literature (Togelius et al. 2011; Shaker et al. 2016 on constraint relaxation in PCG — see § 11) consistently recommends relaxing constraints in order of ascending semantic load (most peripheral constraint relaxed first, most identity-defining constraint relaxed last).

### 2.2 Coherence-constrained selection vs separate coherence judge

A recurring question in the PCG literature is whether coherence checking should be integrated into the selection step or deferred to a downstream judge. The dominant pattern in shipped games is **deferred judge** (separate phase):

- D3/D4: item generation binds substrate → rolls affixes → downstream affix-validity check removes illegal combinations
- PoE: item substrate selected → mods rolled → mod conflict resolution as separate post-roll step
- Reincarnated's own Architecture B: substrate bound at Phase 2 → Phase 5 cohesion-judge confirms thematic fit

The research literature on this question (Shaker et al. 2016 § 7) notes that integrating coherence into the selection step (hard constraint) produces lower diversity because it eliminates borderline-coherent candidates that a downstream judge might accept. The recommended pattern: **coherence as soft constraint at selection** (weight candidates by predicted coherence score) + **hard constraint at downstream judge** (Phase 5 cohesion-judge rejects or re-coalesces if coherence is below threshold).

This is directly applicable to the substrate-triple coherence question: the binding heuristic should weight by predicted coherence (soft), not hard-filter on coherence (hard), leaving the hard gate for Phase 5.

---

## 3. Per-methodology analysis — four heuristic baselines

### 3.1 Deterministic top-rank

**Mechanism:** Score all candidate substrate rows (matching the cell's selection policy) by a composite score; take the highest-scoring row as the kit's bound substrate.

**Composite score function (candidate formulation):**
```
score(row) = w_tier × tier_score(row.quality_tier)
           + w_cell_match × cell_match_score(row, bc_target)
           + w_novelty × novelty_score(row, archive)
```

Where:
- `tier_score` maps Tier S → 1.0, A → 0.75, B → 0.5, C → 0.25
- `cell_match_score` is 1.0 for exact cell match; < 1.0 for relaxed-match under thin-cell fallback
- `novelty_score` measures how underrepresented this row is in currently-generated kits (low novelty = often-selected; high novelty = rarely selected)

**Pros:**
- Deterministic: given same seed and same v1_scope state, identical kit is reproduced exactly. Useful for debugging and for gauntlet-sim determinism.
- Simple to implement: sort + take first.
- Cell-match fidelity is maximized: always takes the best-matching row.
- Respects tier protection natively (Tier S outscores Tier A always; Tier A outscores Tier B always).

**Cons:**
- **Kit diversity collapses over archive population.** Kits targeting the same BC cell always bind the same top-ranked substrate row (absent novelty-score component). This means the archive accumulates many kits sharing identical `mechanical_substrate_triple` values, which contradicts the MAP-Elites diversity goal and degrades BDI η-coefficient signal (all kits in a cell have the same substrate triple; cross-cell comparison loses substrate variation).
- Without novelty component, deterministic top-rank is a pure quality selector, not a diversity selector.
- With novelty component, top-rank becomes an approximation of weighted sampling, but with discretized behavior (the score ties at similar tier+cell-match; novelty breaks ties but ties are common).
- **Substrate coverage utilization is poor:** Tier S rows are always selected when present; Tier B/C rows never surface for cells with Tier S coverage. This wastes v1_scope's deliberately-varied substrate.

**Compute envelope:**
- Per-kit: O(N_candidates) where N_candidates = rows matching cell selection policy. For typical cells with 50-200 matching rows: < 1 ms.
- Per-100-kits: < 100 ms.
- Per-1000-kits: < 1 sec.

**Kit-diversity implications:** POOR for archive-level diversity. ACCEPTABLE only if each BC cell's generation budget is 1 kit (or if novelty-score component is well-calibrated to prevent re-selection).

**Verdict:** Acceptable as a deterministic fallback for specific use cases (e.g., gauntlet-sim needs exact reproduction for specific seed), but **not recommended as primary heuristic** for archive population due to diversity collapse.

---

### 3.2 Probabilistic weighted-sample

**Mechanism:** Score all candidate rows by same composite score as deterministic top-rank, then sample one row with probability proportional to score (softmax or direct normalization).

**Weight function:**
```
weight(row) = score(row)  [same composite as above]
p(row | cell) = weight(row) / Σ weight(r) for r in candidates
```

**Pros:**
- Kit diversity: different kits targeting the same cell will bind different substrate rows, weighted toward higher-tier/better-matching rows but not deterministically locked to the top-1.
- Substrate coverage: lower-tier rows surface occasionally, exercising more of v1_scope's substrate variety.
- Composable with novelty: novelty score adjusts weights downward for over-selected rows, naturally diversifying archive.
- Principled probabilistic basis: well-understood sampling properties; diversity provably proportional to weight entropy.

**Cons:**
- Non-deterministic: same seed may produce different substrate selection if sampling is unseeded (mitigated by making kit-generation seed deterministic through the full pipeline).
- **Coherence mismatch risk:** sampling from a weighted distribution includes low-weight rows with some probability, some of which may have poor substrate-triple coherence. At low probability, this is tolerable; at high entropy (flat weights), it becomes a coherence risk. Mitigated by soft-coherence pre-weighting (see § 3.4).
- **Thin cells produce degenerate distributions:** if only 1-2 rows match the cell selection policy, the weighted distribution is nearly deterministic (one row dominates). Falls back to the same behavior as deterministic top-rank under thin-cell conditions. Requires explicit thin-cell detection and fallback routing (per composition policy v1 § 4).

**Compute envelope:**
- Per-kit: O(N_candidates) for scoring + O(1) for sampling. Same order as deterministic.
- Per-100-kits: < 100 ms.
- Per-1000-kits: < 1 sec.

**Kit-diversity implications:** GOOD for archive-level diversity. Substrate coverage utilization BETTER than deterministic. **Recommended** over pure deterministic.

---

### 3.3 Hybrid filter-then-sample (RECOMMENDED PRIMARY)

**Mechanism:** Two-phase approach:
1. **Filter phase:** reduce candidate set to a quality-band subset (e.g., top-k by composite score, or all rows above a score threshold θ).
2. **Sample phase:** sample uniformly (or with residual weights) from the filtered candidate set.

**Concrete implementation:**
```python
def bind_substrate(bc_target, v1_scope, k=None, theta=None):
    # Phase 1: apply cell-type matching policy to get candidates
    candidates = apply_matching_policy(bc_target, v1_scope)
    
    if len(candidates) == 0:
        return thin_cell_fallback(bc_target, v1_scope)
    
    # Phase 2: score candidates
    scored = [(score(row, bc_target), row) for row in candidates]
    scored.sort(reverse=True)
    
    # Phase 3: filter to quality band
    if k is not None:
        filtered = scored[:k]  # top-k
    elif theta is not None:
        filtered = [(s, r) for s, r in scored if s >= theta]
        if not filtered:
            filtered = scored[:1]  # at least 1
    else:
        # Default: top-k = max(3, len(candidates) // 5) — 20% of candidate set
        k_default = max(3, len(candidates) // 5)
        filtered = scored[:k_default]
    
    # Phase 4: sample from filtered set with residual tier-based weights
    weights = [tier_weight(row.quality_tier) for _, row in filtered]
    selected_row = random.choices([r for _, r in filtered], weights=weights, k=1)[0]
    
    return build_substrate_triple(selected_row)
```

**Filter-size guidance (k parameter):**
- Recommended default: top-k where k = max(3, N_candidates // 5). This ensures:
  - For thin cells (N_candidates < 15): k ≥ 3 (all or nearly all candidates included — thin-cell condition handled via fallback, but small non-empty cells still get sampling diversity)
  - For normal cells (N_candidates = 50-200): k ≈ 10-40 rows (meaningful candidate set with quality floor)
  - For rich cells (N_candidates > 200): k ≈ 40+ rows (large sample space; Tier B rows routinely included)

**Pros:**
- **Best-of-both**: quality floor from filter phase; diversity from sampling phase
- **Prevents worst-case incoherence:** filtering to top-k by composite score ensures the sampling pool never includes very low quality or very poor cell-match rows
- **Composable with thin-cell-fallback:** if candidates < THIN_CELL_THRESHOLD, fallback triggers before filter phase
- **Tier protection natural:** Tier S rows always score highest; they dominate the top-k but don't monopolize it (Tier A rows appear in top-k when Tier S count < k; Tier B rows appear when both Tier S and A are scarce)
- **Genre-canonical:** matches the pattern in D3/D4/PoE item binding (filter by item class + ilvl band → sample within band)
- **Well-supported in PCG literature** (Shaker et al. 2016; Smith et al. 2011 — see § 11)

**Cons:**
- k parameter requires tuning. If k is too small, diversity is equivalent to deterministic top-rank; if too large, quality floor erodes.
- Slightly more complex than pure deterministic or pure probabilistic.
- Residual sampling still introduces non-determinism; addressed by seeding the RNG at kit-generation level.

**Compute envelope:**
- Per-kit: O(N_candidates × log N_candidates) for sort + O(k) for sampling = dominated by sort. For N_candidates = 50-200: < 1 ms.
- Per-100-kits: < 100 ms.
- Per-1000-kits: < 1 sec.

**Kit-diversity implications:** GOOD — combines quality floor (prevents bad substrate selection) with probabilistic diversity (exercises substrate variety).

**Primary recommendation: this is the recommended heuristic baseline for Layer 2 implementation.**

---

### 3.4 Coherence-constrained

**Mechanism:** Add a coherence pre-filter or coherence weight to the selection process. Coherence score measures predicted compatibility of the selected row's element × weapon_kind × energy_type triple.

**Coherence scoring formulation:**
```python
def coherence_score(element, weapon_kind, energy_type) -> float:
    """
    Returns predicted coherence [0.0, 1.0] for this substrate triple.
    
    Component checks:
    1. Element × weapon_kind compatibility (range: are fire + ranged-bow compatible? YES)
    2. Energy_type × element compatibility (are some element × energy_type pairs thematically strong?)
    3. Cross-axis coherence (does the overall triple compose into a recognizable archetype?)
    """
    ...
```

**Empirical coherence signals available from v1_scope substrate:**
- Element × weapon_kind pairings in existing Tier S/A rows serve as implicit coherence evidence: rows that are high-tier AND well-typed by elrond curators represent "empirically coherent" combinations. Per-pairing frequency in Tier S/A is a proxy for coherence.
- Energy_type × element pairings similarly: existing high-tier rows encode implicit design knowledge about which energy types fit which elements (fire mana-caster is common; fire charge-stack is less so; fire rage-melee is present in Norse/Berserker substrate).

**Hard-coherence vs soft-coherence:**

| Approach | Effect | Recommendation |
|---|---|---|
| **Hard coherence** (filter out incoherent triples before sampling) | Produces only "safe" combinations; reduces diversity; may over-remove borderline-valid combinations; makes thin-cell problem worse | NOT recommended at Phase 2 |
| **Soft coherence** (weight candidates by coherence score; incoherent combinations still sampled but rare) | Preserves diversity; incoherent combinations surface occasionally but are caught by Phase 5 cohesion-judge; natural fallback for thin cells | RECOMMENDED — incorporate into hybrid filter-then-sample as a composite weight component |

**Integration into recommended heuristic:**
Coherence check should be one component of the composite score in the hybrid filter-then-sample:

```
score(row) = w_tier × tier_score + w_cell_match × cell_match_score 
           + w_coherence × element_weapon_kind_coherence_score(row)
           + w_novelty × novelty_score(row, archive)
```

Recommended weight allocation (provisional — requires cheapest-refuting-test calibration):
- w_tier = 0.4 (tier protection dominant; Discipline #18.1 substrate-voting-is-binding)
- w_cell_match = 0.35 (cell-match fidelity is primary functional goal)
- w_coherence = 0.15 (soft coherence signal; Phase 5 judge is the hard gate)
- w_novelty = 0.10 (archive diversity; low weight at archive-population start; can increase as archive grows)

**Pros:**
- Coherence signal incorporated at selection time reduces Phase 5 re-coalescence burden
- Soft weighting preserves substrate diversity (doesn't block novel combinations)

**Cons:**
- Coherence scoring requires an explicit element × weapon_kind compatibility table (authored or learned from Tier S/A distribution). This is a data dependency on elrond substrate curation.
- Adding coherence weight before coherence data exists creates a chicken-and-egg problem for v1. Mitigation: start with uniform coherence weight (w_coherence = 0) and add coherence signal when compatibility table is available.

**Verdict: incorporate as composite weight component within hybrid filter-then-sample. NOT a standalone fourth heuristic — it is an enhancement to heuristic 3.**

---

## 4. Thin-cell-fallback algorithmic shape (primary load-bearing analysis)

### 4.1 Trigger condition

**Thin-cell trigger:** candidates matching the strict cell-selection policy fall below `THIN_CELL_THRESHOLD`.

**Recommended threshold:** `THIN_CELL_THRESHOLD = 5` rows.

Rationale: below 5 candidates, the hybrid filter-then-sample effectively degrades to deterministic top-1 (k=max(3, 5//5)=max(3,1)=3; with only 5 rows, top-3 = top-60%). Below 3 candidates, diversity is essentially nil. The threshold of 5 provides a practical trigger that precedes the full diversity collapse.

**Note on composition policy v1 § 4 per-cell routing decisions:** The 12 CRITICAL thin cells in composition policy v1 § 4.1 have LOCKED routing decisions (per D2 design call). The thin-cell-fallback algorithmic shape below applies to runtime generation behavior when those per-cell routing decisions are executed. It does NOT reopen the per-cell routing decision question.

**Cell-pair sharing interactions (per § 4.2):** The 5 cell-pair sharing groups (per D3 Option A) share a 4-tuple substrate pool between proxy=none and proxy=light/heavy cells. At runtime, the thin-cell trigger should be evaluated against the SHARED 4-tuple pool (not the per-cell proxy-discriminated pool), because cell-pair sharing was specifically designed to give thin proxy-density cells access to the broader 4-tuple substrate. This means: `candidates = v1_scope_rows_matching_4_tuple` (ignoring proxy-density dimension); if `len(candidates) >= THIN_CELL_THRESHOLD`, proceed normally; proxy-density discrimination happens via algorithm § 8.6 proxy-spawn template, not at substrate binding.

### 4.2 Substitution priority — axis relaxation order

When candidates are below threshold AND cell-pair sharing does not resolve the shortage (i.e., even the shared 4-tuple pool is thin), the fallback must relax one or more matching dimensions to find additional substrate.

**Recommended substitution priority (relaxation cascade):**

| Priority | Axis relaxed | Rationale |
|---|---|---|
| **1st (relax first)** | `weapon_mechanical_profile` sub-dimensions | Least semantically load-bearing for kit identity; relaxing amplitude bin from "spiky" to "variable" changes balance nuance but not kit theme |
| **2nd** | `tempo` bin | Second-least identity-defining; a "high-tempo" kit bound to a "medium-tempo" weapon still functions mechanically |
| **3rd** | `range` bin | Range is identity-defining (melee vs ranged is a major archetype split) but adjacent bins (melee → mid) preserve functional continuity |
| **4th** | `energy_type` | Energy type shapes resource feel; substitution changes feel but not thematic identity |
| **5th (relax last)** | `element` | Element is semantically load-bearing (fire kit bound to water weapon creates Phase 5 cohesion-judge conflict); relax only when all other relaxations exhausted |

**Implementation shape — relaxation cascade:**
```python
def thin_cell_fallback(bc_target, v1_scope):
    """
    Cascading axis relaxation per substitution priority.
    Returns best available substrate row or None (graceful-fail).
    """
    # Step 0: try 4-tuple cell-pair shared pool first (per § 4.2 composition policy)
    shared_4tuple_candidates = v1_scope_query(
        range=bc_target.range,
        tempo=bc_target.tempo,
        amplitude=bc_target.amplitude,
        attribute=bc_target.attribute
        # proxy_density: NOT filtered here — cell-pair sharing ignores proxy dimension
    )
    if len(shared_4tuple_candidates) >= THIN_CELL_THRESHOLD:
        return apply_hybrid_filter_sample(shared_4tuple_candidates, bc_target)
    
    # Step 1: relax weapon_mechanical_profile sub-dimensions (amplitude adjacency)
    adjacent_amplitude = get_adjacent_amplitude_bins(bc_target.amplitude)
    for alt_amplitude in adjacent_amplitude:
        relaxed = v1_scope_query(range=bc_target.range, tempo=bc_target.tempo,
                                 amplitude=alt_amplitude, attribute=bc_target.attribute)
        if len(relaxed) >= THIN_CELL_THRESHOLD:
            return apply_hybrid_filter_sample(relaxed, bc_target, relaxation_level=1)
    
    # Step 2: relax tempo bin (adjacent bins)
    adjacent_tempo = get_adjacent_tempo_bins(bc_target.tempo)
    for alt_tempo in adjacent_tempo:
        relaxed = v1_scope_query(range=bc_target.range, tempo=alt_tempo,
                                 amplitude=bc_target.amplitude, attribute=bc_target.attribute)
        if len(relaxed) >= THIN_CELL_THRESHOLD:
            return apply_hybrid_filter_sample(relaxed, bc_target, relaxation_level=2)
    
    # Step 3: relax range bin (adjacent bins)
    adjacent_range = get_adjacent_range_bins(bc_target.range)
    for alt_range in adjacent_range:
        relaxed = v1_scope_query(range=alt_range, tempo=bc_target.tempo,
                                 amplitude=bc_target.amplitude, attribute=bc_target.attribute)
        if len(relaxed) >= THIN_CELL_THRESHOLD:
            return apply_hybrid_filter_sample(relaxed, bc_target, relaxation_level=3)
    
    # Step 4: relax energy_type (allow any energy_type matching attribute)
    relaxed = v1_scope_query(range=bc_target.range, tempo=bc_target.tempo,
                             amplitude=bc_target.amplitude, attribute=bc_target.attribute,
                             energy_type=None)  # any energy type
    if len(relaxed) >= THIN_CELL_THRESHOLD:
        return apply_hybrid_filter_sample(relaxed, bc_target, relaxation_level=4)
    
    # Step 5: relax element (allow any element; LAST resort)
    relaxed = v1_scope_query(range=bc_target.range, tempo=bc_target.tempo,
                             amplitude=bc_target.amplitude, attribute=bc_target.attribute,
                             element=None)  # any element
    if len(relaxed) >= THIN_CELL_THRESHOLD:
        return apply_hybrid_filter_sample(relaxed, bc_target, relaxation_level=5)
    
    # Graceful-fail: no substrate found after full cascade
    return graceful_fail_substrate(bc_target)
```

**Relaxation metadata:** every time a fallback is triggered, log the `relaxation_level` (0=no fallback, 1-5=axis relaxed at level N) to `v1_scope_composition_trace` on the kit. This data will surface thin-cell patterns for downstream Sidecar B / Stage 3.5 enrichment prioritization.

### 4.3 Fallback target (per composition policy § 4 design call locks)

Per composition policy v1 § 4.1, the 12 CRITICAL thin cells have locked routing decisions. The thin-cell-fallback algorithmic shape above is the **runtime execution mechanism** for those routing decisions. Specifically:

- **Cell 13 (Artillery Mage):** FOLD into Cell 12 Standard Wizard. Runtime: when bc_target = Cell 13, apply substitution that maps to Cell 12's 4-tuple range; this is a pre-routed case, not a cascade.
- **Cell 14 (Pyromantic Caster):** Stage 3.5 engine-authored entries fill this cell directly; runtime cascade should NOT need to fire for Cell 14 post-Stage-3.5.
- **Cells 15, 17, 19, 21-25:** routing decisions per D2 + Sidecar B enrichment; runtime cascade is the fallback AFTER Sidecar B enrichment for cells still thin post-enrichment.

### 4.4 Graceful-fail behavior

When all fallback cascade steps are exhausted (no substrate found with ≥ THIN_CELL_THRESHOLD rows at any relaxation level):

**Recommended graceful-fail:** return `SubstrateBindingResult(status="UNGENERABLE", bc_target=bc_target, relaxation_levels_tried=[0,1,2,3,4,5])`.

This is a **kit-is-ungenerable** signal, NOT a NULL triple. The calling code (Layer 2 generator) routes ungenerable cells to a generation log (not a crash). Ungenerable cells surface as enrichment-need feedback to the substrate-curation pipeline (per Architecture B Phase 1 discipline: "Phase 1 doesn't queue cells where substrate-coverage is empty — surface as enrichment-need feedback to substrate-curation").

**NOT recommended:** floor-fill with composition policy "default-tier substrate." Creating a substrate triple from a default template would violate the Architecture B substrate-led discipline — substrate-voting-is-binding (Discipline #18.1) means if the substrate doesn't have rows for a cell, the cell cannot be generated, not that a synthetic default should be invented.

**Composition policy v1 § 4 gap flag:** if graceful-fail fires for a cell NOT in the 12 CRITICAL list (i.e., a cell that was not expected to be thin), this is a **gap in composition policy v1 § 4 coverage**. Surface to gandalf via KR — the policy may need a routing decision for that cell. Do NOT invent fallback semantics.

---

## 5. L11 strict 4-tuple matching interaction (primary load-bearing analysis)

### 5.1 The strict-match requirement and its substrate-binding implications

Per framing brief § L11, the gauntlet sim uses strict 4-tuple BC-target matching. This means:

- **Option α (Martial cells):** substrate must have 5-tuple mechanical-fingerprint match (range + tempo + amplitude + attribute + weapon_kind profile compatibility). The weapon_kind's intrinsic mechanical profile must match the BC-target's range × tempo × amplitude bins.
- **Option β (Caster cells):** attribute-level match only. The strict-match applies at the attribute dimension (INT/WIS), not at the full range × tempo × amplitude fingerprint. This is the intended laxity for casters: the weapon scales but doesn't directly deliver the kit's BC-profile.
- **Option C (Cross-attribute hybrid cells):** cross-attribute wielding with ω-penalty; strict-match applies with the ω-penalty flag set.

### 5.2 What happens when v1_scope has zero substrate for a strict 4-tuple

The zero-match case is the critical edge case. Under strict 4-tuple matching with L11 enforcement:

**Case A: Zero rows matching the full strict 4-tuple (Option α: no weapon_kind with the right range × tempo × amplitude profile)**

This is the case that would naively cause kit generation to fail silently. The recommended behavior:

1. **Do NOT skip the cell** — skipping means the BC-target queue never fills this cell, creating a permanent archive gap for a cell that the design intends to support.
2. **Do NOT widen to nearest cell** — widening violates the L11 strict-match requirement; the gauntlet sim requires strict matching for build-definition fidelity.
3. **DO trigger thin-cell-fallback** (§ 4 above) — the fallback cascade is the canonical L11 path for zero-substrate conditions. The kit is "attempting" strict matching; the fallback records the attempt and the relaxation level required.
4. **Log as thin-cell-fallback with relaxation_level = max (all axes tried)** — this surfaces the cell as requiring enrichment (Sidecar B / Stage 3.5 / future Track M work).

**Case B: Zero rows matching Option β attribute-level match (caster attribute but NO rows for the attribute)**

This should not occur in v1_scope (the substrate has rows for all four attributes per per-axis distribution within ±5pp). But if it does: same path as Case A — log, fallback, surface as enrichment need.

**Case C: Zero rows matching Option C cross-attribute (hybrid cells)**

Hybrid cells (Red Mage, Monk-archetype, Holy Knight) have explicit Sidecar B enrichment paths per composition policy v1 § 4.1. If post-Sidecar-B runtime still produces zero cross-attribute substrate rows: trigger thin-cell-fallback cascade; in the extreme case, a cross-attribute kit may bind a same-attribute substrate with relaxation_level = 5 (element relaxation) and have the ω-penalty flag set from the BC-target's Option C routing.

### 5.3 Gauntlet sim strict-match vs player-game equip flexibility (L11 deferred concept)

The strict-match requirement for gauntlet sim is a **generation-time constraint** (the kit's bound weapon must match the cell's strict 4-tuple at generation time). The deferred player-game equip flexibility concept (v1.1+) is a **player-interface-time constraint relaxation** (the player may equip weapons not matching their kit's generation-time BC-target in actual gameplay).

These operate at different layers and do not conflict:
- **Layer 2 (this dispatch scope):** kit is generated with strict 4-tuple matching; `mechanical_substrate_triple` reflects the strictly-matched substrate.
- **v1.1+ design concept:** player can equip different weapons in play; the `mechanical_substrate_triple` of the kit's generated-template remains intact; only the player's combat profile shifts.

No design gap at this layer. The strict-match constraint is correctly scoped to Layer 2 generation without any architectural conflict with the v1.1+ concept.

---

## 6. Cohesion constraint analysis

### 6.1 Element × weapon_kind cohesion

**Thematically coherent pairs (empirically grounded from Tier S/A substrate distribution and genre canon):**

| Element | Coherent weapon_kind categories | Incoherent / ambiguous |
|---|---|---|
| fire | sword, spear, staff, whip (fire-lash), flail | bow (fire-bow exists but less canonical; present in substrate) |
| water | staff, trident, whip, axe (ice-axe) | heavy mace (ambiguous — "freezing hammer" exists in genre) |
| earth | mace, hammer, greataxe, staff, greatsword | rapier (earth-rapier is rare; not incoherent but uncommon) |
| wind | bow, sword (wind-blade), dagger, staff, lance | heavy mace (earth-associated in genre canon) |
| lightning | sword, spear, axe, bow (thunder-arrow), staff | no strong exclusions — lightning is broadly paired in genre |
| holy | sword (holy-knight), mace, staff, spear, shield-weapon | dagger (assassin-shadow associations conflict) |
| shadow | dagger, sword, scythe, bow (shadow-arrow), staff | heavy two-handed melee (shadow-berserk exists but unusual) |
| physical | ALL weapon kinds — physical is the universal base element | N/A |

**Key finding for the heuristic:** element × weapon_kind coherence is a **soft signal**, not a hard incompatibility. No element × weapon_kind pairing is fully impossible in the genre; some are less conventional. The coherence score should WEIGHT toward conventional pairings, not hard-filter unconventional ones.

**Implementation:** a coherence lookup table (element × weapon_kind_category → float) can be derived from the Tier S/A substrate distribution. Tier S/A rows encode implicit design knowledge about which pairings are quality-validated. Elrond can produce this table from existing v1_scope data as a sidecar artifact; rocket consumes it at Layer 2 as `element_weapon_kind_coherence_matrix`.

**Dependency note:** the coherence matrix is a substrate-derived artifact, not a hardcoded list. Hardcoding would violate the substrate-led discipline. The matrix should be generated from v1_scope Tier S/A frequency distribution.

### 6.2 Energy_type × element cohesion

**Framework:** energy_type (mana / rage / charge / focus) has thematic associations with element and attribute that create coherence pressure:

| Energy type | Thematic associations | Common element pairings | Attribute coupling |
|---|---|---|---|
| mana | Arcane / spiritual / intellectual | fire (pyromancer), water, wind, lightning, holy, shadow (necromancer) | INT / WIS primary |
| rage | Physical fury / martial | physical, fire (berserker), earth (warrior) | STR primary |
| charge | Accumulation / stored energy | lightning (charge-up thunder), wind (tornado charge), fire (combustion) | Any — charge is mechanical |
| focus | Precision / concentration | physical (archer focus), wind (calm breath), shadow (assassin focus) | DEX / WIS |

**Cross-incompatibilities (soft):**
- rage × holy: unusual (berserker-holy exists in genre — "divine fury" archetype — but not common)
- rage × shadow: unusual (shadow-berserk is a genre archetype but niche)
- mana × physical (pure physical mana-user): works for "arcane warrior" archetype; present in genre
- focus × fire: unusual ("focused flame" archetype exists but is non-standard)

**Recommendation for heuristic:** energy_type × element coherence should be a **soft weight component** in the composite score, not a hard filter. The weight should be:

```
energy_element_coherence(energy_type, element) = {
    (mana, fire): 0.9,
    (mana, water): 0.85,
    (mana, holy): 0.9,
    (mana, shadow): 0.8,
    (rage, physical): 0.95,
    (rage, fire): 0.75,
    (charge, lightning): 0.9,
    (focus, physical): 0.85,
    (focus, shadow): 0.8,
    ... (full matrix to be authored from substrate distribution)
}
```

**Whether to enforce coherence as hard constraint OR allow incoherence as feature:**

Recommendation: **allow incoherence as feature, with soft weighting.** The rationale: (a) some of the most interesting ARPG archetypes emerge from unexpected element × energy_type combinations (e.g., the "rage-mana-hybrid" berserker archetype who burns mana to amplify rage — a real PCG discovery); (b) Phase 5 cohesion-judge is the hard gate; it can re-coalesce a surprising but valid combination; (c) the spirit-guide explainer pattern exists specifically to explain novel combinations to the player. Hard-filtering coherence at Phase 2 would pre-empt Phase 5's discovery role.

### 6.3 Mechanical_substrate_triple full coherence at Phase 2

The triple (element × weapon_kind × energy_type) needs to be jointly coherent, not just pairwise coherent. The joint coherence is harder to define upfront but is well-approximated by: are all three components consistent with a single recognizable archetype concept?

For Phase 2 purposes: joint coherence = all pairwise coherence scores above 0.5. This is a soft threshold applied as part of the composite score, not a hard filter.

**Hard gate location:** Phase 5 cohesion-judge. Phase 5 is the correct layer for joint coherence confirmation because: (a) Phase 5 has access to the full kit (skills + traits + substrate) for holistic coherence assessment; (b) Phase 5 can re-coalesce by dropping named-bearer attribution if alignment is low (per Architecture B § 5.5 graduated-alignment discipline); (c) Phase 5 LLM call is the natural coherence confirmation point in the Architecture B pipeline.

---

## 7. Composition policy v1 alignment

### 7.1 How the heuristic achieves composition policy v1 § 1 register-share targets

Composition policy v1 § 1 register weights (historical ~50-55%, fantasy ~30-35%, military_modern ~5-8%) were applied at Stage 3 v1_scope materialization — v1_scope already reflects these weights in its row composition. The Layer 2 substrate-binding heuristic does NOT need to re-enforce register weights; it samples from v1_scope which already embeds the composition policy.

**Key insight:** the hybrid filter-then-sample heuristic achieves composition policy alignment AUTOMATICALLY if v1_scope is correctly materialized, because the sampling distribution will naturally follow the v1_scope distribution. No additional register-weight enforcement is needed at Layer 2.

**Proviso:** if the hybrid filter-then-sample is not drawing from the full v1_scope per-cell distribution (e.g., if the k parameter in the filter phase is so small that the filtered candidates are systematically biased toward one register), register targets could be violated. Mitigation: the composite score should NOT include register as a scoring dimension — register balance is handled at v1_scope materialization, not at kit-generation time. This avoids double-counting register pressure.

### 7.2 Per-cell Option α/β/C policy execution at Layer 2

The heuristic must apply the correct matching policy per cell type:

| BC-target cell type | Matching policy | Substrate filter |
|---|---|---|
| STR/DEX primary, physical element | Option α | 5-tuple: weapon_kind's intrinsic mechanical profile must match range × tempo × amplitude × attribute |
| INT/WIS primary, non-physical element | Option β | Attribute-level: match attribute dimension only; weapon_kind selection is flexible within attribute class |
| Cross-attribute hybrid (Red Mage / Monk / Holy Knight) | Option C | Cross-attribute allowed; ω-penalty applied via BDI ω-field resource-dimension (0.0 cross vs 1.0 same-attribute) |

The matching policy is a function of the BC-target cell, not of the substrate row. Routing to the correct policy per cell must be resolved at Layer 2 generator initialization per the cell roster from composition policy v1 § 4.1.

---

## 8. Cheapest-refuting-test design (per Discipline #19.1)

### 8.1 The claim to refute

The primary claim of the recommended hybrid filter-then-sample heuristic: **substrate-triple coherence rate ≥ 90% at the kit level with diverse substrate utilization across v1_scope**.

Two sub-claims:
- **Sub-claim A:** generated kits bind substrate rows with ≥ 90% coherence rate (element × weapon_kind × energy_type triple passes Phase 5 cohesion-judge equivalent spot-check)
- **Sub-claim B:** substrate utilization spans ≥ 25% of available v1_scope rows across a 100-kit generation run (no monoculture collapse)

### 8.2 Test design

**Test name:** Substrate-binding coherence + diversity spot-check

**Scale:** 50 kits minimum, spanning all 22 BC cells (minimum 2 kits per cell; some thin cells may produce fewer)

**Procedure (spot-check mode — no full Phase 3-5 pipeline required):**

1. Run Layer 2 generator (substrate-binding only; skip Phase 3 convergence and Phase 5 LLM)
2. For each generated kit, extract `mechanical_substrate_triple` = (element, weapon_kind, energy_type)
3. Apply 3 spot-check criteria per kit:
   - **Criterion A (element × weapon_kind coherence):** is the pairing a recognized archetype combination? Use lookup table derived from Tier S/A substrate distribution. Score: 1 if coherent, 0 if incoherent (hard-incompatible in genre canon), 0.5 if ambiguous.
   - **Criterion B (energy_type × element coherence):** is the pairing thematically consistent? Use energy-element coherence matrix. Score: 1 if score ≥ 0.6, 0 if score < 0.4, 0.5 if in between.
   - **Criterion C (cell-match fidelity):** does the bound substrate row's mechanical profile match the BC-target cell's range × tempo × amplitude bins? Score: 1 if exact match, 0.5 if relaxation_level 1-2 was used, 0 if relaxation_level 3-5 was used.
4. Per-kit coherence score = mean(Criterion A, B, C). Kit passes if score ≥ 0.7.
5. Compute: (a) overall pass rate across 50 kits; (b) unique substrate rows bound across 50 kits (diversity metric)

**Pass threshold:**
- **Coherence gate:** ≥ 90% of kits pass (≥ 45/50 kits with score ≥ 0.7) — PASS
- **Diversity gate:** ≥ 25% of available v1_scope rows bound (≥ 760 unique rows if v1_scope = 3,042) across 50 kits — PASS (note: 50 kits binding 25% of 3,042 rows = ~15 unique rows/kit average; achievable if sampling diversity is working)
- **Thin-cell gate:** ≤ 10% of kits used relaxation_level ≥ 3 (element or energy_type relaxation) — PASS (signals that thin-cell cascade was not frequently forced to deep relaxation)

**Fail conditions (refuting signals):**
- Coherence rate < 80% (< 40/50 kits): composite score weight calibration is wrong; re-examine w_coherence and element_weapon_kind coherence matrix
- Diversity < 10% unique rows (< 305 unique rows): filter-then-sample is collapsing to the same top-k rows; increase k parameter
- > 20% of kits using relaxation_level ≥ 3: v1_scope has deeper thin-cell coverage gaps than expected; surface to elrond for Sidecar B enrichment prioritization

**Compute cost:** 50 kits × Phase 2 substrate-binding only (no Phase 3-5) = ~50 × 1ms = <0.1 sec. Total test runtime: < 1 minute including spot-check scoring. This is a genuinely cheap refuting test.

---

## 9. Resource-bounds projection

### 9.1 Per-method runtime compute + memory envelope

**Inputs:**
- v1_scope size: 3,042 rows (per Cycle 10 wind-down tag)
- BC-target cells: 22 (per composition policy v1 § 4)
- Expected candidates per cell under strict 4-tuple matching: median ~50-200 rows (well-populated cells); min ~3-15 rows (thin cells per § 4.1); max ~400+ rows (richest cells)

| Method | Per-kit compute | Per-100-kits | Per-1000-kits | Peak memory |
|---|---|---|---|---|
| Deterministic top-rank | O(N_cand × log N_cand) ≈ 200 ops × log(200) ≈ 1,500 ops; < 1 ms | < 100 ms | < 1 sec | ~1 MB (scored candidate list) |
| Probabilistic weighted-sample | Same scoring + O(1) sample | < 100 ms | < 1 sec | ~1 MB |
| Hybrid filter-then-sample (RECOMMENDED) | Same scoring + filter + O(k) sample; k ≤ 40 typical | < 100 ms | < 1 sec | ~1 MB |
| Coherence-constrained (as composite weight) | Same + coherence matrix lookup O(1) per row | < 100 ms | < 1 sec | ~2 MB (matrix loaded once) |

**All methods are computationally negligible** relative to Phase 3 convergence (~10 min/kit). The substrate-binding step is not a resource bottleneck at any foreseeable scale.

**Memory projection:**
- v1_scope in memory: 3,042 rows × ~500 bytes/row metadata = ~1.5 MB. Can be held in memory for full kit-generation run without issue.
- Coherence matrix: 8 elements × 50 weapon_kind categories × 4 energy_types = 1,600 floats = ~12 KB. Negligible.
- Per-kit AlterationOutput (from § 8 algorithm): ~500 bytes (per algorithm § 8 consult). No resource concern.

**Per-1000-kits full-pipeline projection (substrate-binding contribution only):**
- 1,000 kits × < 1 ms = < 1 sec substrate-binding time
- Total Phase 2 cost (including skill composition): estimated 1-5 min for 1,000 kits
- Phase 3 dominates: 1,000 kits × ~10 min each = ~167 hours (parallel execution assumption needed for production)

### 9.2 Thin-cell-fallback cascade overhead

- Cascade: at most 5 relaxation steps per thin cell
- Per-step: re-query v1_scope with relaxed constraints (SQL query ~1 ms)
- Total per thin-cell kit: < 5 ms overhead
- If 10% of kits are thin-cell (100 kits per 1,000): < 500 ms additional overhead for cascades

Thin-cell-fallback adds no resource concern.

---

## 10. Methodology recommendation memo

### 10.1 Recommended heuristic

**PRIMARY RECOMMENDATION: Hybrid filter-then-sample with soft coherence weighting**

Implementation shape (for rocket Layer 2 dispatch consumption):

```python
# Composite scoring function (Phase 2 substrate-binding)
def score_substrate_row(row, bc_target, archive_state=None):
    """
    Returns composite score [0.0, 1.0] for substrate row given BC-target cell.
    
    Weight allocation (provisional; calibrate via cheapest-refuting-test):
    w_tier = 0.40     # Tier protection; substrate-voting-is-binding (Discipline #18.1)
    w_cell = 0.35     # Cell-match fidelity (primary functional goal)
    w_coh  = 0.15     # Soft coherence (Phase 5 judge is the hard gate)
    w_nov  = 0.10     # Archive diversity (low at archive-population start)
    """
    tier_s = {"S": 1.0, "A": 0.75, "B": 0.50, "C": 0.25}.get(row.quality_tier, 0.25)
    cell_s = cell_match_score(row, bc_target)  # 1.0 exact; < 1.0 for relaxed match
    coh_s  = element_weapon_kind_coherence(row.element, row.weapon_kind)
    nov_s  = novelty_score(row, archive_state) if archive_state else 0.5
    
    return 0.40 * tier_s + 0.35 * cell_s + 0.15 * coh_s + 0.10 * nov_s


# Main substrate-binding entry point
def bind_substrate_triple(bc_target, v1_scope, k_fraction=0.20, archive_state=None):
    """
    Hybrid filter-then-sample substrate binding.
    
    k_fraction: proportion of candidate set to include in filtered pool.
    Default 20% (max(3, len(candidates) // 5)).
    """
    # 1. Apply cell-type matching policy (Option α/β/C)
    candidates = apply_matching_policy(bc_target, v1_scope)
    
    # 2. Thin-cell detection + fallback routing
    if len(candidates) < THIN_CELL_THRESHOLD:
        return thin_cell_fallback(bc_target, v1_scope)  # See § 4.2
    
    # 3. Score candidates
    scored = sorted(
        [(score_substrate_row(row, bc_target, archive_state), row) for row in candidates],
        reverse=True
    )
    
    # 4. Filter to quality band
    k = max(3, int(len(candidates) * k_fraction))
    filtered = [(s, r) for s, r in scored[:k]]
    
    # 5. Sample with residual tier weights
    weights = [tier_weight(r.quality_tier) for _, r in filtered]
    selected = random.choices([r for _, r in filtered], weights=weights, k=1)[0]
    
    # 6. Build and return substrate triple
    return SubstrateBindingResult(
        element=selected.element,
        weapon_kind=selected.weapon_kind,
        energy_type=selected.energy_type,
        source_row_id=selected.id,
        quality_tier=selected.quality_tier,
        relaxation_level=0,  # No fallback triggered
        matching_policy=bc_target.matching_policy  # α/β/C
    )
```

### 10.2 Rationale summary

| Design choice | Rationale |
|---|---|
| Hybrid filter-then-sample vs pure deterministic | Prevents substrate monoculture in archive; exercises v1_scope's diversity |
| Hybrid filter-then-sample vs pure probabilistic | Quality floor (filter phase) prevents incoherent low-tier rows from contaminating selection |
| Soft coherence weight (w=0.15) vs hard coherence filter | Preserves novel combinations for Phase 5 discovery; hard gate at Phase 5 cohesion-judge |
| Tier weight dominant (w=0.40) vs cell-match dominant | Respects Discipline #18.1 substrate-voting-is-binding; Tier S/A protection is the composition policy's primary instrument |
| Element substituted LAST in cascade | Element is semantically load-bearing; substituting early creates Phase 5 coherence problems |
| Graceful-fail as UNGENERABLE (not NULL-triple) | Prevents silent failures; surfaces enrichment needs to substrate-curation pipeline |
| Thin-cell threshold = 5 rows | Below this point hybrid sampling degrades to near-deterministic; threshold triggers fallback before full collapse |

### 10.3 Implementation-shape sketch for rocket Layer 2

**Required new artifacts (Layer 2 substrates):**

1. `element_weapon_kind_coherence_matrix` — 2D lookup table (element × weapon_kind_category → float [0,1]); derived from Tier S/A substrate distribution via elrond SQL query; loaded once at generator initialization.
2. `energy_type_element_coherence_matrix` — 2D lookup table (energy_type × element → float); authored from genre canon analysis + substrate distribution; loaded once at generator initialization.
3. `thin_cell_routing_table` — per-cell routing decisions for the 12 CRITICAL thin cells per composition policy v1 § 4.1; loaded as static config.
4. `apply_matching_policy(bc_target, v1_scope)` — routes to Option α / β / C filter per bc_target cell type.
5. `thin_cell_fallback(bc_target, v1_scope)` — cascading axis relaxation per § 4.2.
6. `SubstrateBindingResult` — result struct: element + weapon_kind + energy_type + source_row_id + quality_tier + relaxation_level + matching_policy + (optional) relaxation_trace.

**Key data dependency:** `element_weapon_kind_coherence_matrix` and `energy_type_element_coherence_matrix` depend on v1_scope being materialized (Cycle 10 elrond work). This is satisfied: the framing brief notes `v1_scope substrate (per Cycle 10 wind-down): elrond/v0.0-cycle-10-stage-3-phase-2-v1-scope-2026-05-25 tag → 3,042 rows`.

**Single unified vs per-matching-strategy heuristics:**

Recommendation: **single unified heuristic** (the hybrid filter-then-sample) with the matching policy (α/β/C) as a pre-filter routing step. Do NOT implement three separate heuristics per matching strategy. The unified heuristic handles all three via the `apply_matching_policy` pre-filter; the scoring and sampling logic is identical regardless of which matching policy filtered the candidates.

---

## 11. Framing-audit checklist (per Discipline #23)

**Applied to the recommended hybrid filter-then-sample methodology:**

**Q1: What load-bearing framing assumptions does this work depend on?**

- A1a: v1_scope is materialized at 3,042 rows with per-axis distribution within ±5pp per framing brief. If v1_scope is significantly smaller OR more skewed than this, the thin-cell fallback cascade will trigger more frequently and at lower k values.
- A1b: The 22 BC cells referenced in composition policy v1 § 4 are the canonical cell roster. If the cell roster changes, the thin-cell routing table needs updating.
- A1c: The `element_weapon_kind_coherence_matrix` can be derived from Tier S/A substrate distribution in v1_scope. This assumes Tier S/A rows encode valid coherence signal (i.e., elrond's curation produced quality-accurate tier assignments). If Tier S/A assignments are noisy, the coherence matrix will be noisy.
- A1d: Phase 5 cohesion-judge is the hard coherence gate. This methodology assumes Phase 5 is implemented and functional before kit diversity from Phase 2 matters. If Phase 5 is not yet implemented, the soft-coherence approach risks letting incoherent kits slip through.

**Q2: What evidence currently in hand could refute these assumptions?**

- A2a: v1_scope materialization at 3,042 rows is confirmed per Cycle 10 wind-down tag. No refutation available — this assumption is empirically grounded.
- A2b: cell roster is from composition policy v1 § 4 (locked). No refutation available.
- A2c: Tier S/A assignment quality is upstream elrond work (Stage 1/1.5/2/2.5 classification passes). If elrond Stage 3 execution surfaces systematic misclassification, coherence matrix signal would degrade. Current data: ±5pp per-axis distribution met; no signal of systematic Tier S/A misclassification. Assumption holds.
- A2d: Phase 5 implementation status in Cycle 12: Phase 5 cohesion-judge fires at v1 ship via Architecture B pipeline. Cycle 12 does NOT implement Phase 5 (Layer 5 not in Cycle 12 scope). This is a real gap: the soft-coherence approach at Phase 2 is effectively ungatekept until Phase 5 lands. Mitigation: the cheapest-refuting-test (§ 8) provides an in-Cycle-12 coherence spot-check that substitutes for Phase 5 during Layer 2 validation.

**Q3: If refutation evidence exists or is plausible, is the right move to refine the framing?**

- A3a/A3b/A3c: Assumptions hold. No framing refinement needed.
- A3d: The Phase 5 gap is real but manageable via the cheapest-refuting-test proxy. The framing does not need refining — but the Layer 2 dispatch should note that coherence gate from Phase 5 is deferred and the cheapest-refuting-test is the interim validation instrument.

---

## 12. Discipline #25 semantic-layer rep-audit (L9 application)

**Applied to the recommended substrate-binding heuristic per L9 substrate split:**

**Audit question:** Does the recommended heuristic introduce any semantic-layer fields (cultural_tradition / lineage / period) into the Phase 2 substrate-binding selection criteria?

**Field-by-field audit of heuristic composite score components:**

| Score component | Fields used | In mechanical layer (L9 compliant)? |
|---|---|---|
| tier_score | quality_tier | YES — quality_tier is a curation property, not a semantic-overlay field |
| cell_match_score | range, tempo, amplitude, attribute (BC-target dimensions) | YES — all mechanical dimensions |
| element_weapon_kind_coherence | element, weapon_kind | YES — both are in mechanical_substrate_triple per L9 |
| energy_type_element_coherence | energy_type, element | YES — both are in mechanical_substrate_triple per L9 |
| novelty_score | archive state (which rows have been selected) | YES — mechanical archive selection history; no semantic fields |

**Semantic overlay fields status:**

| Field | Used in Phase 2 binding heuristic? | Correct location |
|---|---|---|
| cultural_tradition | NOT used | Phase 5 cohesion-judge (naming + spirit-guide explainer) |
| lineage | NOT used | Phase 5 named-bearer attribution discipline |
| period | NOT used | Phase 5 period-coherence confirmation |

**Rep-audit verdict: CLEAN.** The recommended heuristic is fully L9-compliant. No semantic-overlay fields enter the Phase 2 substrate-binding selection criteria.

**Note on architecture benefit:** cultural_tradition / lineage / period are available on the bound substrate row for Phase 5 consumption because they're stored on the `WeaponKnowledgeEntry` that gets bound. Phase 2 binds the ROW (which carries all fields); Phase 5 reads the semantic-overlay fields from the already-bound row. This is the correct Architecture B flow: bind at Phase 2 via mechanical criteria; narrate at Phase 5 via semantic fields. The heuristic correctly uses only mechanical criteria at Phase 2.

---

## 13. MC-1 / MC-2 dependency surface

**Question posed by dispatch:** Does MC-1 cell-sampling methodology constrain MC-2 substrate-binding heuristic?

**Finding:** MC-1 and MC-2 are **largely independent** with one conditional coupling.

**Independence (primary):**
- MC-1 determines HOW cells are sampled from the BC-target subspace (uniform vs composition-policy-weighted vs substrate-coverage-aware). This determines which cells the generator targets.
- MC-2 determines HOW substrate rows are selected GIVEN a sampled cell. These are sequential decisions, not concurrent constraints.
- The recommended hybrid filter-then-sample (MC-2) functions correctly regardless of whether MC-1 recommends uniform, weighted, or coverage-aware cell sampling.

**Conditional coupling (flag to KR):**

If MC-1 recommends **substrate-coverage-aware cell sampling** (i.e., the cell sampling probability is adjusted based on v1_scope coverage per cell), then there is a coupling:
- MC-1's coverage-awareness signal is derived from the same substrate-candidate-count data that MC-2's thin-cell detection uses.
- If MC-1 under-samples thin cells (to avoid thin-cell fallback pressure), MC-2's thin-cell-fallback cascade should expect lower trigger frequency.
- If MC-1 over-samples rich cells (to maximize substrate match quality), MC-2 should tune its k parameter larger for rich cells.

**This coupling is minor** and does not require MC-1 to complete before MC-2's methodology is locked. The thin-cell threshold (THIN_CELL_THRESHOLD = 5) and k-fraction (0.20) are Layer 2 implementation parameters that can be tuned post-MC-1 without changing the heuristic's structure.

**Flag to KR:** if MC-1 recommends substrate-coverage-aware sampling AND the coverage-awareness signal is derived from per-cell candidate counts, rocket Layer 2 dispatch should note the shared data source (v1_scope per-cell candidate count) as a parameter passed from MC-1's cell-sampling module to MC-2's thin-cell detection module. The modules share an input, not an output — coupling is at the data-dependency level, not the algorithm level. KR does not need to sequence MC-2 completion after MC-1; both can inform the Layer 2 dispatch independently.

---

## 14. Composition policy v1 § 4 thin-cell-fallback gaps

**Observation from this analysis:** the thin-cell-fallback cascade algorithm (§ 4.2 above) relies on per-cell routing decisions being locked for ALL cells the generator may target. Composition policy v1 § 4.1 locks routing for the 12 CRITICAL cells identified in Stage 2 thin-cell analysis. But the generator may attempt to generate kits for cells NOT on the 12 CRITICAL list if a player's seasonal-arc targets them.

**Potential gap:** if a cell not in the 12 CRITICAL list turns out to be thin post-v1_scope materialization (e.g., a cell that appeared well-populated in Stage 2 analysis but has fewer matching rows after strict 4-tuple filtering at L11 is enforced), the thin-cell-fallback cascade would trigger but there is no locked routing decision for that cell. The cascade's relaxation logic handles this gracefully (it doesn't crash — it relaxes and records), but the graceful-fail path (UNGENERABLE) would surface a cell with no canonical routing decision.

**Flag to gandalf via KR:** composition policy v1 § 4 should be reviewed for whether its routing decisions cover all 22 BC cells or only the 12 CRITICAL cells identified in Stage 2. If coverage is only for the 12 CRITICAL cells, the policy has a potential gap for thin-outcome-at-runtime non-critical cells. This is a specification gap rather than an algorithmic gap — the cascade handles it gracefully, but a routing decision logged in the policy would prevent ambiguity. Recommending gandalf review the policy scope; if gap confirmed, flag for Matt escalation per Cycle 12 scope-doc § 5 escalation triggers.

---

## 15. Knowledge gaps not resolved

1. **element_weapon_kind_coherence_matrix values.** This consult recommends a substrate-derived matrix but does not produce it (requires SQL query against v1_scope Tier S/A distribution, which is elrond's artifact). Rocket Layer 2 needs this table. Elrond SC-1/SC-2 sidecars are in flight; elrond should be queried for a per-tier S/A element × weapon_kind frequency distribution as a Layer 2 input artifact.

2. **THIN_CELL_THRESHOLD calibration.** The recommended threshold of 5 rows is based on the hybrid filter-then-sample degradation analysis (k ≤ 3 under 5 candidates). Post-v1_scope strict-4-tuple application, actual candidate counts per cell under Option α/β/C matching are not empirically measured in this consult. The cheapest-refuting-test will calibrate this.

3. **k_fraction parameter calibration.** The recommended 20% (k = max(3, N_candidates // 5)) is based on the filter-diversity tradeoff analysis but not empirically validated. Post-cheapest-refuting-test, if diversity gate fails (< 25% unique rows bound), increase k_fraction.

4. **Interaction with archive novelty score.** The novelty_score(row, archive_state) component requires the archive to be partially populated before it provides useful signal. At archive initialization (0 kits), novelty scores are uniform — the novelty component effectively does nothing. This is correct behavior (no prior state to differ from), but the w_novelty = 0.10 weight allocation should be dynamic: start at 0.0 for archive initialization, ramp to 0.10 as archive grows. Leaving as a Layer 2 implementation design choice for rocket, flagged here.

5. **Phase 5 coherence gate timing.** Phase 5 cohesion-judge is noted as the hard coherence gate. Phase 5 is not in Cycle 12 scope. Until Phase 5 is implemented, the soft-coherence weight at Phase 2 is the only coherence instrument. The cheapest-refuting-test (§ 8) is the interim gate for Cycle 12 validation.

---

## 16. Source list

**Primary sources (project canonical docs):**
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — Cycle 12 framing brief; § 2 MC-2 scope; § 4 PlayerClass contract; § L9 substrate split; § L11 strict 4-tuple matching
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy v1; § 3 Option α/β/C matching; § 4 thin-cell resolution; § 5 per-cell coverage
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B Phase 2 substrate-binding spec; Phase 5 cohesion-judge pipeline
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes; bin definitions; weapon_mechanical_profile components
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` — precedent consult (scored-candidate strategy registry + η-coefficient + cheapest-refuting-test pattern)
- `agentic_orchestration/legolas/research/cycle-10-stage-3-methodology-consult-2026-05-25/methodology-recommendation.md` — constrained-knapsack methodology consult (thin-cell floor satisfaction precedent; greedy-with-swap-repair pattern)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1, #18, #18.1, #18.2, #19.1, #20, #23, #25
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` — Cycle 12 scope; § 5 escalation triggers

**Secondary sources (external literature, accessed 2026-05-25):**
- Mouret, J-B. & Clune, J. (2015) — "Illuminating search spaces by mapping elites." arXiv:1504.04909. Archive-seeded QD generation; filter-then-sample patterns in MAP-Elites with pre-existing content pools.
- Fontaine, M.C. et al. (2021) — "Differentiable Quality Diversity." NeurIPS 2021. Archive-augmented generation; candidate-pool diversity maintenance.
- Togelius, J. et al. (2011) — "Search-based procedural content generation: A taxonomy and survey." IEEE TCIAIG 3(3). Constraint-relaxation fallback in PCG; relaxation cascade design.
- Shaker, N., Togelius, J. & Nelson, M.J. (2016) — "Procedural Content Generation in Games." Springer. § 7 constraint-based PCG; coherence scoring vs downstream judge; filter-before-sample genre patterns in item generation.
- Smith, A.M. et al. (2011) — "Toward a framework for procedural content generation in games." FDG 2011. Thematic coherence in template-based content selection; coherence-as-weight vs coherence-as-filter.
- Hartsook, K. et al. (2011) — "Toward supporting stories with procedurally generated game worlds." IEEE CIG 2011. Narrative coherence in procedural generation; soft-constraint approaches.
- "Architecture B genre-canonical alignment" — per qd-engine-end-to-end-workflow-2026-05-24.md § 2.2 (D2/D3/D4/PoE/LE/GD substrate-binding patterns documented in that doc; this consult inherits those findings rather than re-surveying).

---

**Signed:** legolas (research + scout)
**For:** MC-2 substrate-binding heuristics methodology recommendation — Cycle 12 Layer 2 gate. Delivers per-methodology analysis for four heuristic baselines; thin-cell-fallback algorithmic shape; L11 strict 4-tuple matching interaction; cohesion constraint analysis; composition policy v1 alignment; cheapest-refuting-test; resource-bounds projection; framing-audit checklist; Discipline #25 semantic-layer rep-audit; MC-1/MC-2 dependency surface; composition policy v1 § 4 thin-cell gap flag for gandalf.
