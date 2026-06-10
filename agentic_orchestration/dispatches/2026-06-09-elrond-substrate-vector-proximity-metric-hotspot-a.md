# Elrond Hotspot A Commission — Substrate-Vector Proximity Metric Definition

**STATUS:** ACTIVE (commission ready to fire — Pattern B scope)
**Date authored:** 2026-06-09
**Author:** knight-rider (orchestrator)
**Authority:** Discipline #18.2 trigger FIRED per gandalf design review of Drax /forge Phase 3 close (commit `150adb8`); empirical-evidence trigger per Drax Phase 3 dispatch § 9 "Phase 3 close report surfaces methodology hotspots → elrond methodology consultation per Discipline #18.2 (fires post-baseline)"
**Mode:** Pattern B methodology consultation (post-baseline timing per Discipline #18.2)
**Audience:** elrond (executor), drax (downstream consumer for any Phase-3-amendment work), gandalf (design-spec-as-math handoff review), Matt (architectural-decision consumer at WS2 commission scope authoring + canonical primitive-curation Pattern B downstream)

**Companion docs (read first):**
- `agentic_orchestration/drax/notes/2026-06-09-forge-phase-3-close-report.md` (Drax Phase 3 close; Hotspot A surfaced at § "Methodology Hotspots" Hotspot A)
- `agentic_orchestration/gandalf/notes/2026-06-09-drax-forge-phase-3-close-design-review.md` § 3 (gandalf design review; trigger FIRED per #18.2)
- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-3-two-layer-buffer-space-prototype.md` § 1.4 + § 5.1 (methodology framing at dispatch authoring)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (20 primitive families; 570 primitives in /forge corpus)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 amendment 2026-06-06 (primitive-as-star + kit-as-constellation)
- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/` (Phase A delivery packet — substrate-trace extraction including primitive_registry.parquet + kit_constellations.parquet + region_labels.json)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Disciplines #18 + #18.2 + #25 + #41 load-bearing)

---

## 0. TL;DR

**Mission:** define a substrate-vector proximity metric that can rigorously evaluate Drax Phase 3 criterion 2 — "Spatial proximity reflects substrate-vector relationship (kits near their primary primitive)" — and apply the metric to the current Phase 3 layouts (baseline radial + force-directed) to produce empirical validation of the spatial-proximity-reflects-substrate claim.

**Hotspot A trigger:** Drax Phase 3 placed kits near primary element anchors by CONSTRUCTION (radial: fixed-anchor + radial-projection sunflower spiral) or by ANCHOR-SPRING (force-directed: spring physics toward primary anchor). Neither method uses actual substrate-vector distance metrics to validate that spatial proximity reflects substrate similarity. Criterion 2 passes on FACE (element neighborhoods visible) but the substrate-similarity claim is NOT rigorously validated.

**Per Discipline #18.2 post-baseline timing:** methodology consultation fires AFTER baseline at extension hotspots. Phase 3 IS the baseline (radial + force-directed both shipped); this commission is the post-baseline consultation.

**Downstream gates:**
- Elrond defines the metric + framework
- Elrond evaluates current Phase 3 layouts (radial + force-directed) against the metric
- Returns verdict on which layout better satisfies criterion 2 + recommendations for production layout choice
- Output feeds Hotspot B (UMAP vs Voronoi comparison) which queues post-Hotspot-A completion (per gandalf design review § 3 Hotspot B disposition)

**Estimated wall-clock:** Pattern B — 1-3 wall-clock days. May compress to Pattern A scope if elrond determines metric definition + evaluation is bounded; elrond discretion to declare and surface.

---

## 1. Methodology consultation scope

### 1.1 What "substrate-vector" means in this context

Each kit in the /forge corpus carries a substrate-trace per the Phase A delivery packet — element coupling, T4 strategy, mechanic flag families, BC bin assignments, substrate primitives composed. The "substrate-vector" is the high-dimensional vector representation of this trace.

Each primitive in atomic-substrate-registry similarly carries a substrate-vector — its position in the 20-primitive-family space (or higher-dimensional embedding if elrond's methodology choice extends).

**The substrate-vector proximity metric** measures: given two entities (kit-to-kit OR kit-to-primitive-anchor OR primitive-to-primitive), how "close" are they in substrate-trace space?

Elrond decides the dimensional space + distance metric (Euclidean / cosine / Mahalanobis / Wasserstein / Jaccard at categorical layers / hybrid).

### 1.2 What criterion 2 validates

Drax dispatch criterion 2: "Spatial proximity reflects substrate-vector relationship (kits near their primary primitive)"

Verification step (current): substrate-trace data overlay (existing /forge analyst toggle) confirms spatial relationships AT FACE LEVEL — element-neighborhoods are visibly clustered near their element anchors.

**What's missing:** rigorous validation that the SPATIAL distance metric (Euclidean pixel distance in the 11000×8500 world) correlates with the SUBSTRATE-VECTOR distance metric. If kits A and B are 200px apart spatially, are they substrate-similar? If they're 2000px apart spatially, are they substrate-dissimilar?

The metric should produce a quantitative answer of the form:
- Pearson / Spearman correlation between (spatial_distance_kit_A_kit_B) and (substrate_vector_distance_kit_A_kit_B)
- Stress / Kruskal-Wallis statistic if doing MDS-style fidelity analysis
- Per-element-family clustering quality metric (silhouette / Davies-Bouldin / Calinski-Harabasz)
- Whatever methodology elrond determines is appropriate

### 1.3 Application to current Phase 3 layouts

Two layouts shipped at Phase 3:
- **Baseline radial:** fixed-anchor + radial-projection sunflower spiral; min NN 40.7px in primary zones / 29.7px in buffer zones; deterministic
- **Force-directed:** 80 iterations + anchor-spring K=0.006 + inter-kit repulsion K=8000 + spatial bucketing BUCKET=450px; min NN 94.5px overall; better kit separation per drax observation

Elrond should evaluate BOTH against the substrate-vector proximity metric to produce empirical evidence on:
- Which layout better preserves substrate-vector proximity (criterion 2 satisfaction)
- Whether either layout has substrate-vector-proximity-preservation acceptable for production
- Whether a third methodology (UMAP / Voronoi / other) might better satisfy if the current two don't
- Surface tradeoff: does the layout with better kit separation (force-directed) also preserve substrate-vector proximity, or is there a tradeoff?

### 1.4 Methodology choice — within elrond seam authority

Per hive-mind decision-routing § 3.9 + Discipline #18.2 — elrond decides methodology within seam authority. Categories of choice elrond will surface:

| Methodology family | Properties |
|---|---|
| **Distance metric** | Euclidean / cosine / Mahalanobis / Wasserstein / Jaccard / hybrid |
| **Vector space** | Raw substrate-vector / PCA-reduced / embedding-based / categorical-encoded |
| **Validation framework** | Correlation-based / MDS-fidelity / clustering-quality / pairwise-rank-based |
| **Aggregation** | Per-pair / per-element-family / global / hybrid |

**Elrond surfaces methodology + rationale + verdict — KR does not pre-impose.**

---

## 2. Substrate consumption

### 2.1 Required substrate (already exists)

- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/primitive_registry.parquet` — 570 primitives + substrate-trace metadata
- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/kit_constellations.parquet` — 1000 sim PROVISIONAL kits + substrate-trace metadata
- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/region_labels.json` — BC bins + tier + scaling + emergent mechanic-family
- Phase 3 layout outputs (radial baseline + force-directed) — request from drax if not already in delivery packet

### 2.2 Layout files (request from drax if needed)

Phase 3 produces JSON layout files (0.13MB baseline / 0.15MB force-directed) per drax close-report § "Positioning Algorithm Tradeoffs". Coordinate with drax at session-start to confirm layout file paths or request export to elrond workspace.

---

## 3. Acceptance criteria

| # | Criterion | How validated |
|---|---|---|
| 1 | Substrate-vector proximity metric defined with explicit methodology + dimensional space + distance function + rationale | Elrond authoring; surfaces methodology at design-spec-as-math handoff format |
| 2 | Metric applied to both Phase 3 layouts (radial baseline + force-directed) | Empirical evaluation; reproducible computation |
| 3 | Per-layout verdict: which better preserves substrate-vector proximity | Quantitative metric output (correlation / stress / clustering-quality) per layout |
| 4 | Production recommendation: which layout to ship for /forge production, or whether neither suffices and a third methodology needed | Substantive recommendation with rationale |
| 5 | Hotspot B (UMAP vs Voronoi) framing: if Hotspot A surfaces that current layouts are insufficient, recommend whether UMAP or Voronoi is the next empirical step | Methodology framing at queuing layer |
| 6 | Discipline #25 rep-audit check: does the metric correctly handle per-element-family vs per-primitive-family substrate-vector distinctions (without conflating element-coupling with primitive-composition layers)? | Methodology validation against rep-audit discipline |
| 7 | Composition with Branch A vs Branch B architectural-decision (Tal Rasha recognition record): does the metric work identically under both branches, or does Branch A introduce additional substrate-vector dimensions (glyph-as-primitive)? | Forward-compatibility note at output |

---

## 4. Quality criterion

**Game-quality goal this dispatch serves:** Players reading the cosmograph spatial layout interpret spatial proximity as substrate-similarity meaningfully — when two kits are visually close, they ARE substrate-similar (not just same-element by construction). The /forge spatial layout earns the substrate-led discipline at the rigor layer that Phase 3 acceptance verification surfaced as unvalidated.

**Refutation conditions** (sub-agent surfaces if any apply):
- This dispatch contradicts canonical anchor X
- Alternative execution Y serves the named quality goal better
- Acceptance criteria can pass without advancing the quality goal
- Dispatch framing pre-commits to a decision Matt has not ratified
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40)
- **Hotspot A specific refutation:** the metric I would define is methodologically incoherent against current substrate-trace data (e.g., element-coupling encoding is sparse; categorical fields aren't easily distance-functioned without arbitrary encoding choices that themselves require Pattern B with Matt)

---

## 5. Discipline citations

### 5.1 Discipline #18.2 (methodology consultation timing at extension hotspots)
This commission IS the post-baseline consultation. Phase 3 fired baseline first (radial + force-directed); now methodology is consulted with concrete pain surfaced. Per #18.2 refinement, this timing is correct.

### 5.2 Discipline #25 (semantic-layer rep-audit)
Metric must handle per-element-family vs per-primitive-family substrate-vector distinctions correctly. Rep-audit at metric-definition layer.

### 5.3 Discipline #41 (substrate-led)
Methodology emerges from substrate data; no pre-imposed metric. Elrond examines what the substrate-trace data SUPPORTS as distance-coherent, then defines the metric.

### 5.4 Discipline #19 (Agent-tool-not-for-waiting)
KR fires this commission with `run_in_background=true`; elrond executes autonomously; KR does not poll.

### 5.5 Discipline #11 (empirical inspection over assumption)
Inspect actual layout JSON files + actual substrate-trace data; do not assume what the data looks like. Verify any column-encoding assumptions before computing distances.

### 5.6 Discipline #1 (math-before-code)
Math note required if implementing the metric in code: define metric formally; specify computation; cite alternatives considered; then implement.

---

## 6. What this commission does NOT include (explicitly out of scope)

- ❌ UMAP comparison (Hotspot B; queued post-Hotspot-A per gandalf design review § 3 disposition)
- ❌ Voronoi territory partitioning evaluation (same — Hotspot B queue)
- ❌ Layout re-rendering or modification (drax seam; KR routes any layout amendment as separate commission)
- ❌ Substrate corpus enrichment or rare-lineage kit generation (YELLOW 1 disposition; engine-side commission per gandalf design review recommendation 6)
- ❌ Canonical primitive-curation lock (DEFERRED to Pattern B with Matt post-Legolas + post-Phase-3; this commission may inform but does not commit)
- ❌ Branch A vs Branch B architectural-decision call (post-Legolas; this commission's output should be forward-compatible per criterion 7)
- ❌ WS2 (Niagara) commission scope authoring (DEFERRED per gandalf design review § 5 — post-Legolas-final + Branch-A/B-Matt-call)
- ❌ Implementation of metric in production engine (separate downstream commission if needed)

---

## 7. Composition with prior work

| Prior work | Composition |
|---|---|
| Drax /forge Phase 3 close report | Hotspot A surfaced; this commission addresses |
| Gandalf design review § 3 Hotspot A | Trigger fired per #18.2; this commission fires |
| Phase A elrond delivery packet (2026-06-06) | Substrate-trace data source; commission consumes |
| Atomic substrate registry (2026-06-06) | 20 primitive families; substrate-vector dimensional space anchor |
| Cosmograph pivot § 9 amendment (2026-06-06) | Primitive-as-star + kit-as-constellation architectural commitment |
| Tal Rasha recognition record (2026-06-09) | Branch A/B forward-compatibility per criterion 7 |
| Legolas zodiac corpus Mode B (in flight) | Zodiac substrate may extend primitive registry post-Branch-A-confirmation; metric must be forward-compatible |

---

## 8. Deliverables

1. **Methodology note** at `agentic_orchestration/elrond/notes/2026-06-XX-hotspot-a-substrate-vector-proximity-methodology.md` (date per actual close) including:
   - Methodology choice + rationale (dimensional space + distance metric + validation framework)
   - Alternatives considered + why rejected
   - Discipline #1 math-note compliance if code implementation included
   - Discipline #25 rep-audit verification
2. **Empirical evaluation output** with quantitative results for both Phase 3 layouts (radial + force-directed):
   - Per-layout substrate-vector-proximity-preservation metric value
   - Per-element-family breakdown
   - Tradeoff observations
3. **Production recommendation:** which layout to ship for /forge production, or whether a third methodology is needed
4. **Hotspot B framing recommendation:** if Hotspot A surfaces current layouts are insufficient, recommend whether UMAP or Voronoi is the next empirical step (this informs the next commission KR authors)
5. **Forward-compatibility note** for Branch A vs Branch B architectural-decision composition
6. **Code (if implemented)** at `agentic_orchestration/elrond/scripts/` per your seam convention; auto-commit per CLAUDE.md addendum

---

## 9. Sign-off

**Authored:** knight-rider (orchestrator) 2026-06-09 per Discipline #18.2 trigger FIRED at gandalf design review of Drax Phase 3 close.

**Authority:** KR orchestration scope per CLAUDE.md addendum + hive-mind decision-routing § 3.9. Elrond decides methodology within seam authority; KR routes the commission.

**Routing:** elrond executes Pattern B; surfaces methodology + verdict + recommendation; KR aggregates downstream:
- Hotspot B queueing decision per output
- Production layout recommendation surface for Matt-call (or drax direct if recommendation is unambiguous and in drax seam discretion)
- WS2 commission scope authoring composition (downstream gandalf lane)

**Empirical-evidence triggers:**
- Hotspot A closure → Hotspot B queueing decision fires
- Hotspot A production recommendation → potentially drax-amendment to /forge production layout (per drax seam discretion)
- Hotspot A forward-compatibility verdict → composes with Branch A/B Matt-decision-call when Legolas completes

**Composition with prior canonical commitments:** all preserved (Atomic substrate registry 2026-06-06 + Cosmograph pivot 2026-06-05 + Tal Rasha recognition 2026-06-09 + Earth-Avatar Creation Moment Architecture 2026-06-07 + Drax /forge Phase 3 GREEN close + Federated PC team 2026-06-07).

**End of commission.**
