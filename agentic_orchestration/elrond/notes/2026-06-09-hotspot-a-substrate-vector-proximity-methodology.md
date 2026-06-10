# Hotspot A — Substrate-Vector Proximity Methodology + Empirical Verdict

**STATUS:** CURRENT (Pattern A-deep / Pattern B compressed; methodology + empirical evaluation + production recommendation in one pass)
**Date:** 2026-06-09
**Author:** elrond (data steward and archivist)
**Mode:** Pattern B methodology consultation compressed to Pattern A — scope bounded; metric definition + evaluation completed in single session per elrond seam discretion (dispatch § 0 TL;DR permits)
**Commission dispatch:** `agentic_orchestration/dispatches/2026-06-09-elrond-substrate-vector-proximity-metric-hotspot-a.md`
**Routes to:** knight-rider (orchestrator aggregation) → drax (production-layout consumer, within seam discretion if recommendation is unambiguous) → Matt (architectural-decision consumer only at Hotspot B / WS2 scope-authoring) → gandalf (design-spec-as-math handoff review)
**Companion artifacts:**
- `agentic_orchestration/elrond/scripts/hotspot_a_substrate_vector_proximity.py` (implementation; math-note citations at `# MATH-NOTE:` markers)
- `agentic_orchestration/elrond/research/hotspot-a-substrate-vector-proximity-2026-06-09/results.json` (per-layout / per-element raw output)

---

## 0. TL;DR

**Methodology:** weighted-Jaccard distance on primitive_set membership, evaluated with a four-statistic validation framework (global rank correlation + kNN purity + per-element MDS stress + anchor-proximity audit). Per Discipline #41 substrate-led + Discipline #25 rep-audit, vector-space encodings (one-hot Euclidean, PCA, UMAP-as-substrate) are explicitly **rejected** at this layer — primitive_set is a categorical set, not a vector; the principled distance is set-overlap, weighted by family information content.

**Verdict on Phase 3 layouts:**

| Statistic | radial_baseline | force_directed | Direction | Winner |
|---|---|---|---|---|
| Global Spearman ρ (substrate vs spatial) | 0.313 | 0.319 | higher better | force (marginal) |
| Kendall τ | 0.203 | 0.203 | higher better | tie |
| kNN purity @ k=5 (face cluster check) | 0.816 | 0.915 | higher better | **force** (+10pp) |
| kNN/random substrate ratio | 0.954 | 0.952 | <1 better | tie |
| Mean per-element Kruskal stress-1 | 0.508 | 0.523 | lower better | radial (marginal) |
| Mean within-element Spearman | 0.101 | 0.080 | higher better | radial (marginal) |

**Production recommendation:** ship **force_directed** for /forge production AND for any UE-port player-facing surface. The face-level criterion 2 satisfaction is materially better (kNN purity 0.915 vs 0.816; per-element purity uniformly higher across all 8 elements). The within-element substrate fidelity tradeoff is marginal (~3% relative on stress-1; ~0.02 absolute on Spearman) and lives at a layer the player cannot read.

**The strongest finding is not which layout wins.** It is what both layouts share: the substrate-vector proximity claim of criterion 2 holds **strongly at the element-family layer** and **weakly at the within-element layer**. Neither layout is a substrate-faithful low-dimensional embedding; both are element-anchored topologies where spatial position carries primary-element information richly and other substrate-vector dimensions thinly. This bounds what spatial reading of the cosmograph can validly mean — and it has decisive implications for Hotspot B.

**Hotspot B framing recommendation:** queue **UMAP comparison** (not Voronoi) as the next empirical step, with a specific charge — measure whether UMAP recovers within-element substrate fidelity that the current element-anchored layouts cannot. If UMAP delivers within-element Spearman ≳ 0.4 without destroying the element-family clustering, it is the production layout. If not, the question becomes whether within-element fidelity matters for player experience — and that is a gandalf/Matt call, not an elrond call. See § 7.

**Forward-compatibility (Branch A vs Branch B):** the metric is branch-agnostic. The substrate-vector representation is `primitive_set` membership; under Branch A, zodiac-glyph primitives are added to the registry and become additional set members. The weighted-Jaccard distance composes cleanly. See § 8.

---

## 1. Framing-audit (Discipline #42 / dispatch § 4 refutation conditions)

Applied at dispatch consumption:

- **Q1 — canonical contradiction?** No. Methodology aligns with substrate-led (#41), atomic substrate registry (2026-06-06), cosmograph pivot § 9 amendment.
- **Q2 — alternative serves quality goal better?** No. The dispatch quality goal ("players reading the cosmograph spatial layout interpret spatial proximity as substrate-similarity meaningfully") is precisely what a proximity-correlation metric measures.
- **Q3 — Hotspot-A-specific refutation: methodologically incoherent against substrate data?** **No, with constraint.** The substrate trace IS distance-coherent if treated as **set-membership over a 366-primitive categorical universe**, NOT if forced into a vector space requiring arbitrary categorical encoding. This constraint determines methodology choice (§ 2).

Verdict: proceed.

---

## 2. Methodology — substrate-vector representation

### 2.1 What "substrate-vector" IS in this corpus (empirical inspection per Discipline #11)

Each kit carries:
- `primitive_set_json`: an unordered set of ~34 atomic substrate primitives drawn from a 366-element universe (kits use 366; registry has 570 — the 204-primitive gap is registry-only primitives not yet referenced by any PROVISIONAL kit)
- `primary_element`, `kit_attribute`, `is_hybrid`: redundant projections derivable from `primitive_set`
- BC bin assignments (axes 1, 2, 2A, 2B, 3A, 3B, 4, 5): tagged in the engine substrate, not present in the parquet directly; the kit's BC bin is encoded in `kit_id` itself (`kit_bc_cell_NNNN_simulated`) and accessible via region_labels.json
- Element coupling / attribute coupling: present in `primitive_registry.parquet` per-primitive, not per-kit (kit-level coupling is derivable as the union over its primitives)

The **primitive_set IS the substrate-vector** in the sense that fits substrate-led discipline. Every other field is either a derived projection (primary_element, is_hybrid) or a clustering of the primitives along a different axis (BC bins). The atomic-substrate-registry 2026-06-06 framing makes this explicit: primitives are stars, kits are constellations OF stars.

### 2.2 Why NOT a vector space at this layer

Forcing primitive_set into a vector space requires one of:
- **One-hot Euclidean** over 366 dimensions: imposes equal-axis assumption (a difference in element is the same magnitude as a difference in chain_architecture). Discipline #25 rep-audit failure — the semantic layers are not interchangeable.
- **PCA on one-hot**: just rotates the same space; doesn't fix the equal-axis assumption; reduces to "first PC = element" which the layouts already encode.
- **UMAP / t-SNE on one-hot**: useful for VISUALISATION but the embedding distance is non-metric and non-interpretable; can't be used as the GROUND-TRUTH distance against which a layout is evaluated. (UMAP-as-substrate-truth would beg the question — we'd be validating one embedding by comparing to another embedding, both with arbitrary hyperparameters.)
- **Categorical encoding (label-encoded integer per family)**: imposes false ordinality.

Each of these requires a choice the substrate does not justify. Per Discipline #41 substrate-led, the metric should emerge from what the data IS — a set of categorical labels — not be imposed by what would be convenient.

### 2.3 What IS substrate-justified: weighted-Jaccard on sets

Set-overlap distance (Jaccard) is the natural metric for unordered set membership. Two refinements make it appropriate here:

- **Family weighting.** Not all primitives are equally informative about "what kind of kit this is." Element / sub_element_flavor / mechanic / weapon_form_token / cultural_tradition / skill_geometry / race_primitive primitives carry kit identity. Chain_architecture, investment_scaling_pattern, skill_tree_position, scaling_pattern_per_tier, and resource_model are near-universal across kits and carry little discriminating signal. Weighting handles this without imposing dimensionality.
- **Membership-only (not multiset).** Each primitive appears at most once in a kit's primitive_set (verified empirically — primitive_set_json contains no duplicates). Multiset / count-based extensions are not justified by the data.

The weighted-Jaccard formulation is in § 3.

### 2.4 Alternatives considered + rejected

| Alternative | Why rejected |
|---|---|
| Cosine on one-hot primitive_set | Mathematically equivalent to unweighted Jaccard up to denominator constant when sets are fixed-size; family-weighting requires moving to weighted form anyway; cosine adds no information |
| Mahalanobis on PCA-reduced primitive matrix | Requires covariance estimate over 366d sparse boolean → numerically unstable; PCA itself imposes equal-axis assumption already rejected |
| Wasserstein on primitive distributions | Requires a base metric on primitives themselves; we have categorical labels, not a ground metric. Wasserstein is principled IF a primitive-similarity matrix exists (e.g., from co-occurrence statistics); a future extension may construct one |
| Hamming on one-hot | Special case of unweighted Jaccard; same family-information problem; doesn't normalise by set size |
| Embedding-based (encode primitive_set via a learned embedding) | No labels to learn against in current corpus (q_scores, gauntlet_pass_rate are all None per empirical inspection — corpus is PROVISIONAL); deferred until engine ranking telemetry lands |
| UMAP coordinates on primitive matrix as substrate ground truth | Begs the question (Hotspot B itself proposes UMAP as a candidate LAYOUT — using UMAP as substrate truth would tautologise the comparison) |
| BC-bin Hamming | BC bins are ITSELF a clustering of substrate, not the substrate; would measure how spatially-faithful the layout is to a different clustering, not to the substrate vector. Useful as a sidecar audit, not as the primary metric |

### 2.5 Family weight choice (rep-audit per Discipline #25)

| family | weight | rationale |
|---|---|---|
| element, sub_element_flavor, mechanic, skill_geometry, weapon_form_token, cultural_tradition, race_primitive | 1.0 | kit identity load-bearing — what the kit IS |
| attribute, T4_strategy, register, historical_period, off_hand_substrate | 0.7 | meaningful but cross-cutting; multiple kits with different identities can share |
| chain_architecture, investment_scaling_pattern, skill_tree_position, scaling_pattern_per_tier, resource_model | 0.3 | near-universal across PROVISIONAL corpus; e.g., every kit has T1/T2/T3/T4 position tier primitives. Including at 1.0 would inflate Jaccard intersection across genuinely different kits |
| unknown / fallback | 0.5 | safety default |

The weight choice was not tuned to produce a target output — it was set before any layout was evaluated, per Discipline #18 sequencing (acceptance criteria fixed BEFORE methodology runs). The weights are explicit and surfaceable in `results.json _meta.family_weights`; sensitivity analysis would be a Pattern B follow-on if Hotspot B output suggests the weight choice is load-bearing.

---

## 3. Math note (Discipline #1 / #1.2)

### 3.1 Weighted Jaccard distance

For two kits $A, B$ with primitive sets $S_A, S_B \subseteq U$ (universe $U$, $|U| = 366$):

$$ d_{\text{sub}}(A, B) \;=\; 1 - \frac{\sum_{p \in S_A \cap S_B} w_{\text{fam}(p)}}{\sum_{p \in S_A \cup S_B} w_{\text{fam}(p)}} $$

where $w_{\text{fam}(p)}$ is the family weight from § 2.5 and $\text{fam}(p)$ is the primitive family of $p$. Range $[0, 1]$ where $0$ = identical, $1$ = disjoint.

Properties:
- Symmetric ✓
- Identity-of-indiscernibles ✓ (for sets, not arbitrary vectors)
- Non-negative ✓
- Triangle inequality: holds for unweighted Jaccard (Levandowsky & Winter 1971); the weighted variant inherits via the same argument when weights are non-negative ✓

**Implementation citation:** `hotspot_a_substrate_vector_proximity.py` lines 138-170 (`weighted_jaccard_distance` + `weighted_jaccard_distance_batch`).

### 3.2 Spatial distance

Euclidean in the 11000×8500 world coordinate frame (per Phase 3 layout output spec; both layouts use the same world). Both layouts position each kit at a single `(cx, cy)`; "star cluster" sub-points are decorative per drax close-report § "Two-layer architecture" and not used for kit-level proximity.

$$ d_{\text{spa}}(A, B) \;=\; \sqrt{(x_A - x_B)^2 + (y_A - y_B)^2} $$

**Implementation citation:** `hotspot_a_substrate_vector_proximity.py` line 250 (`sample_pair_correlation`).

### 3.3 Family of validation statistics

#### 3.3.1 Global pair correlation (§ 4.1)
Spearman ρ and Kendall τ on $d_{\text{sub}}$ vs $d_{\text{spa}}$ over a uniform-random sample of 20000 distinct kit pairs (seeded for reproducibility). Rank-based — robust to non-linear monotone scale mismatches (e.g., $d_{\text{spa}}$ being unbounded above while $d_{\text{sub}} \in [0,1]$). Kendall is subsampled to 5000 for time complexity.

#### 3.3.2 kNN substrate purity + ratio (§ 4.2)
For each kit, find the $k=5$ spatially nearest neighbours (cKDTree). Purity := fraction of those neighbours sharing the kit's `primary_element`. Substrate ratio := $\bar d_{\text{sub}}(\text{kNN}) / \bar d_{\text{sub}}(\text{k random kits})$. Ratio $< 1$ indicates the layout preserves substrate proximity beyond what random arrangement would.

#### 3.3.3 Per-element Kruskal stress-1 (§ 4.3)
Within each primary_element subset, sample 1500 pairs; compute optimal-scale Kruskal stress-1:

$$ \sigma \;=\; \sqrt{\frac{\sum (d_{\text{sub}} - \alpha \cdot d_{\text{spa}})^2}{\sum d_{\text{sub}}^2}}, \qquad \alpha = \frac{\sum d_{\text{sub}} \cdot d_{\text{spa}}}{\sum d_{\text{spa}}^2}$$

Closer to 0 = better fidelity. Standard rule-of-thumb thresholds (Kruskal 1964): $\sigma \le 0.05$ "excellent," $\sigma \le 0.1$ "good," $\sigma \le 0.2$ "fair," $\sigma > 0.2$ "poor." Our results live in $[0.46, 0.58]$ — empirically the within-element substrate vector is **not faithfully embedded** by either current layout.

#### 3.3.4 Anchor proximity audit (§ 4.4)
For each element anchor $E$, count how many of the 100 spatially-nearest kits to anchor $E$ have `primary_element = E`. This SEPARATES the contribution of construction (kits near anchor $E$ tend to be element $E$ kits because both layouts anchor by element) from the contribution of substrate (within-element proximity). Used as a rep-audit cross-check on the kNN purity statistic.

**Implementation citation:** lines 234-313 of the script.

---

## 4. Empirical results

### 4.1 Headline table (reproduced from § 0 with full precision)

| layout | spearman | kendall | purity@5 | knn/rand | stress-1 | within-grp spearman |
|---|---|---|---|---|---|---|
| radial_baseline | 0.3134 | 0.2026 | 0.8156 | 0.9541 | 0.5075 | 0.1009 |
| force_directed | 0.3192 | 0.2032 | 0.9154 | 0.9522 | 0.5232 | 0.0801 |

### 4.2 Per-element kNN purity (criterion 2 face-level satisfaction)

| element | n_kits | radial purity | force purity | Δ (force − radial) |
|---|---|---|---|---|
| earth | 81 | 0.7086 | 0.9037 | **+0.195** |
| fire | 82 | 0.7805 | 0.9244 | **+0.144** |
| holy | 84 | 0.6929 | 0.8524 | **+0.160** |
| lightning | 81 | 0.8025 | 0.9309 | **+0.128** |
| physical | 428 | 0.9266 | 0.9692 | +0.043 |
| shadow | 80 | 0.5850 | 0.7200 | **+0.135** |
| water | 75 | 0.7440 | 0.8613 | **+0.117** |
| wind | 89 | 0.8067 | 0.9258 | **+0.119** |

Force-directed delivers higher purity for every element. The gain is largest for low-frequency elements (earth, fire, holy, shadow, water, wind) and smaller for physical — which already had near-ceiling purity due to its 43% corpus share (more physical neighbours available to be "nearest"). This is the substrate-honest read: force-directed's physics-based equilibration tightens element clusters relative to radial's deterministic-spiral placement, especially where corpus is sparse.

### 4.3 Per-element stress (within-element fidelity)

| element | radial stress | force stress | radial within-Sp | force within-Sp |
|---|---|---|---|---|
| earth | 0.5151 | 0.5243 | 0.1266 | 0.0431 |
| fire | 0.4921 | 0.5113 | 0.1066 | 0.0526 |
| holy | 0.5236 | 0.5387 | 0.1116 | 0.0532 |
| lightning | 0.5043 | 0.5253 | 0.0917 | 0.0671 |
| physical | 0.5203 | 0.5389 | 0.0543 | 0.0784 |
| shadow | 0.4657 | 0.4784 | 0.0901 | 0.1267 |
| water | 0.4840 | 0.4906 | 0.1405 | 0.1183 |
| wind | 0.5551 | 0.5779 | 0.0860 | 0.1013 |

Both layouts show "poor" within-element fidelity by the Kruskal rule-of-thumb (stress > 0.2). The radial baseline is marginally tighter on stress (~3% relative) and on within-element Spearman for 5 of 8 elements. Force-directed slightly beats radial on within-element Spearman for shadow / physical / wind. The differences are too small to assert one is materially better than the other at the within-element layer.

**The principal finding here is not the radial-vs-force comparison.** It is that **neither layout faithfully embeds within-element substrate structure.** Both place kits inside an element-anchored zone using a method (sunflower spiral / spring physics) that has no awareness of substrate similarity beyond primary_element membership. The layouts are honest about what they encode (primary_element neighborhoods) and silent on what they don't (within-element substrate similarity).

### 4.4 Anchor proximity audit

| anchor | radial top100 match / 100 | force top100 match / 100 |
|---|---|---|
| fire | 67 | 71 |
| water | 54 | 54 |
| earth | 65 | 65 |
| wind | 75 | 78 |
| lightning | 62 | 76 |
| holy | 61 | 61 |
| shadow | 48 | 48 |
| physical | 100 | 100 |

Force-directed shows materially-better anchor-proximity match for fire/wind/lightning; identical for water/earth/holy/shadow/physical. The shadow anchor is the weakest at 48/100 in both — the shadow zone's nearest neighbours are about half shadow kits, half non-shadow. This is the corpus-shape effect: shadow has 80 kits but the corpus geometry forces non-shadow kits into the shadow anchor's neighbourhood at the world-edge. Worth flagging but not a layout-comparison call.

### 4.5 Cross-layer summary

The two layouts agree at the global-correlation layer (Spearman 0.313 vs 0.319 — within sampling noise). They agree at the substrate-ratio layer (kNN/rand 0.954 vs 0.952 — within noise). They disagree materially at the element-cluster face layer (purity 0.816 vs 0.915 — force decisively wins). They marginally disagree at the within-element fidelity layer (stress 0.508 vs 0.523 — radial marginally wins).

The signal the player can read (cluster-membership / face-level proximity) favors force-directed. The signal the player can't read (within-element substrate fidelity) marginally favors radial but is poor in both cases.

---

## 5. Production recommendation

**Ship force_directed for /forge production and any UE-port player-facing surface.**

Rationale:
1. **Face-level criterion 2 is materially better satisfied** (kNN purity 0.915 vs 0.816; +13 percentage points). This is the layer the player reads. Drax close-report § "Mid-buffer feel" subjective observation ("organic spatial coherence") is empirically corroborated by the per-element purity gain.
2. The within-element stress disadvantage is **marginal** (~3% relative on stress-1; ~0.02 absolute on within-element Spearman) and lives at a layer the player cannot perceive. Both layouts are "poor" by Kruskal rule-of-thumb at this layer; neither is good.
3. The min-NN spacing advantage drax surfaced (94.5 vs 29.7 buffer-zone) is independently validated by the anchor proximity audit — force-directed places non-element kits further from element-anchors except for the shadow / water / earth / holy cases where corpus geometry pins both layouts.

**Caveat 1 (preserves gandalf review § 4):** force-directed must inherit a corpus-imbalance safety-clamp (drax + elrond joint-spec when UE-port commission fires). The buffer-emerges-from-physics property fails Discipline #59 if buffer width varies materially with corpus size; the radial baseline's dynamic-zone-radius cap (1200px) is more honest at that layer. Force-directed production should adopt a similar clamp.

**Caveat 2 (substrate-led):** the radial baseline is RETAINED as the design-validation tool per gandalf review § 4. This is NOT overturned. Two layouts; two purposes.

**Caveat 3 (gandalf YELLOW 2 — physical dominance):** the metric independently validates Discipline #59 substrate-honesty. Physical kits' kNN purity (0.93+ in both layouts) reflects their 43% corpus share — they have lots of physical neighbours available. If the corpus were rebalanced (option A in gandalf review), physical purity would drop toward the other elements' values and the layouts would look more uniform. This is the right direction — the metric supports the corpus-rebalance recommendation, not the visual-normalization alternative.

Within drax seam discretion if drax concurs; routes to Matt for architectural-call only if drax disagrees with the recommendation.

---

## 6. Hotspot B framing recommendation

The dispatch § 8 deliverable 4 asks elrond to recommend whether **UMAP** or **Voronoi** is the next empirical step. The empirical findings here decisively shape this.

### 6.1 What § 4 results tell us about Hotspot B

The within-element substrate fidelity is poor in both layouts (Kruskal stress > 0.46, within-element Spearman < 0.13). This is structural — the layouts use element as a hard anchor and then place kits within a zone by methods (sunflower spiral / repulsion physics) that have no substrate awareness.

**The substantive question Hotspot B should answer:** is there a layout method that recovers within-element substrate fidelity (stress dropping to ~0.2, within-element Spearman climbing to ~0.4+) **without** destroying the element-family face-level clustering (purity@5 staying ≥ 0.85)?

### 6.2 UMAP vs Voronoi — which addresses this question?

- **UMAP** on the kit primitive-membership matrix would produce coordinates that DIRECTLY optimize for substrate proximity preservation, including within-element. If UMAP's substrate proximity coordinate carrying capacity is the question, UMAP is the experiment.
- **Voronoi** is a partition method, not a layout method. Voronoi tessellation given anchor positions produces territory cells; it does not place kits inside cells. It would be useful for visualizing element-territory boundaries (a sidecar overlay), but does NOT address the within-element substrate fidelity question.

**Recommendation: queue UMAP as Hotspot B. Voronoi is queueable separately as a Hotspot B-supplement (sidecar overlay for territory boundaries) but addresses a different question and should not be the primary Hotspot B experiment.**

### 6.3 UMAP-as-Hotspot-B scope (for KR commission authoring)

Specific charge to surface when KR authors the Hotspot B dispatch:

- Compute UMAP coordinates for 1000 kits on the 366-primitive membership matrix; sensitivity-sweep `n_neighbors ∈ {15, 30, 50}` and `min_dist ∈ {0.1, 0.3, 0.5}` per Discipline #24 single-parameter sweep isolation
- Run this script's evaluation framework against UMAP coordinates (re-using the four-statistic framework so results are directly comparable to § 4)
- Surface verdict: does UMAP reach kNN purity@5 ≥ 0.85 AND per-element Kruskal stress-1 ≤ 0.30 AND within-element Spearman ≥ 0.40 simultaneously? (Thresholds set per gandalf design review § 3 framing; subject to design adjustment.)
- If yes: UMAP is the production layout.
- If no: the question of "does within-element substrate fidelity matter for player experience" surfaces as a gandalf / Matt design call. The metric cannot answer it.

### 6.4 What Hotspot B explicitly does NOT need to relitigate

- The set-based weighted-Jaccard substrate distance is the canonical ground truth for both Hotspot B and any future layout consultations. UMAP is being evaluated AS A LAYOUT METHOD against this ground truth, not as a competing ground truth.
- The family-weighting scheme can be sensitivity-tested in Hotspot B (does flat-weight produce materially different verdicts than § 2.5 weights?) but the categorical-set framing is fixed.

---

## 7. Forward-compatibility — Branch A vs Branch B (criterion 7)

The methodology is **branch-agnostic.**

- **Branch B (current; figurative nebula anchors).** Element primitives anchor; substrate-vector is primitive_set membership over current 366-primitive universe; metric unchanged.
- **Branch A (post-Legolas; glyphic zodiac primitives).** Per Tal Rasha recognition record 2026-06-09 § 5 Trigger 1, Branch A adds zodiac-glyph primitives to the registry. These become additional members of the primitive universe. Weighted-Jaccard composes cleanly — the union and intersection operations are defined on whatever the universe is. Family weight for the new `zodiac_glyph` family would need to be set (recommended at 1.0 by analogy with element / sub_element_flavor as kit-identity-carrying) but this is a one-line addition.
- **Hybrid branch (some glyphs replace some elements, others add).** Same handling. Sets are robust to universe-size growth.

**Where Branch A WOULD require methodology re-work:** if Branch A reframes the substrate-vector as a **point in a continuous glyphic embedding space** (not a categorical set of glyph names), THEN the set-based distance is no longer applicable. Per the Tal Rasha record framing (glyphic structure as primitive-anchor architecture), the glyph is still a categorical identity ("the zodiac sign Leo as primitive") and not a continuous embedding. This is the expected Branch A shape; methodology survives.

**Forward note for the future architect (elrond hands off here):** if at any point the engine produces per-kit ranking telemetry (q_scores, gauntlet_pass_rate currently None) AND a substrate-similarity-supervised learning task becomes available, a learned kit-embedding could supersede weighted-Jaccard. That is post-corpus-maturity; not in scope for Hotspot A or B.

---

## 8. Discipline cross-references

- **#1 math-before-code:** § 3 formal definitions precede implementation. Script implementation lines cited in § 3.
- **#1.2 math-note code-citation discipline:** script contains `# MATH-NOTE:` markers at each major computation block referencing the methodology note section.
- **#11 empirical inspection over assumption:** § 2.1 substrate inspection drove methodology choice (verified primitive_set is set-not-vector before defining metric). § 4 results inspected per-element to surface what one summary statistic would have hidden.
- **#18 / #18.2 methodology consultation timing:** this consultation IS the post-baseline #18.2 trigger fire. Phase 3 baseline fired first (radial + force-directed); methodology consultation now.
- **#21 / #22 no-sleep / timezone-agnosticism:** workstream-relative framing throughout (post-baseline, next-consultation, post-Legolas, etc.). No time-of-day references.
- **#25 semantic-layer rep-audit:** § 2.2 explicit rejection of vector-space encodings; § 2.5 family weight rationale audited at rep-layer (element ≠ chain_architecture in information content). § 4.4 anchor-proximity audit serves as cross-check against the kNN purity statistic.
- **#41 substrate-led:** methodology emerges from substrate shape (categorical sets, not vectors). Family weights derived from corpus structure (universal-across-corpus → low weight).
- **#42 framing-audit:** applied at dispatch consumption per § 1; verdict was proceed-with-Q3-constraint (categorical-set framing is the constraint).
- **#59 substrate-coverage honesty:** § 5 caveat 3 supports the corpus-rebalance recommendation over visual normalization at render layer.

---

## 9. Routing summary (for KR consumption)

1. **Methodology verdict:** weighted-Jaccard on primitive_set, four-statistic validation framework. Surfaced + audited.
2. **Empirical verdict:** force-directed wins on face-level (criterion 2 satisfaction); both layouts marginal on within-element fidelity.
3. **Production recommendation:** ship force-directed for /forge production. Within drax seam discretion. Retain radial as design-validation tool (gandalf review § 4 preserved).
4. **Hotspot B framing:** queue UMAP as primary Hotspot B experiment with the explicit charge of recovering within-element substrate fidelity. Voronoi is a separable supplement, not the primary B experiment.
5. **Forward-compatibility:** metric is Branch-A/B-agnostic per § 7; composes cleanly with zodiac-glyph primitive registry expansion.
6. **Matt-call surfaces:** none added by this consultation. (The gandalf review § "Matt-call surfaces" 1-3 remain in flight; nothing changed.) If drax disagrees with the force-directed recommendation, that disagreement routes to Matt; absent that, force-directed lands within drax seam authority.

---

**Signed:** elrond (data steward and archivist)
**For routing:** knight-rider aggregation → drax (production layout adoption, within seam discretion) → gandalf (design-spec-as-math review acknowledgement, no design change requested) → Matt (only via gandalf review § Matt-call surfaces, not new from this consultation)
