# Atlas Derivation — Pre-Registration (pinned analysis plan)

**Date:** 2026-07-14 · **Author:** gandalf (SPEC-AUTHOR) · **Status:** v1 — PINNED pending jack-ryan Gate-1 methodology review (binding only if reviewed BEFORE execution)
**Authority:** Matt 2026-07-14 — "adopted. let's proceed." (charter: `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md`)
**Executor:** elrond (corpus DB seam) — executes, returns numbers + gate report, **no interpretation**
**Reader of results:** gandalf (DRIFT-CRITIC)

> **Pre-registration discipline:** every parameter below is pinned BEFORE any decomposition runs. Deviations during execution are PROTOCOL AMENDMENTS — logged in § 9 with timestamp + reason, never silent. No peeking at embeddings before gates are computed. If a pinned parameter proves impossible (e.g., a library limitation), the amendment names the substitute and why it is the nearest neighbor of the pinned choice.

---

## 1. Data snapshot (Stage 0)

- **Corpus:** the keyed corpus AFTER curation batch A.5 lands (elrond's open curation batch). Snapshot is tagged in the corpus DB (`atlas_prereg_2026_07_14` or elrond's equivalent convention) — the pipeline runs against the tag, not against a moving head.
- **Unit of analysis:** the **keyed kit** (~470 rows expected post-batch; exact N recorded in the gate report). NOT the strict cell (457) — cell collapse happens via the key, not by pre-aggregation; duplicate-cell kits are legitimate repeated observations of a genre-validated point.
- **Variables:** the 13 Class-A coordinates of `coordinate-register-2026-07-13.md` § table. Class B (element/race/culture/etc.) and Class C (attribute) are EXCLUDED from derivation; franchise/game-id is retained as a *grouping label for Gates C–D only*, never as an input variable.
- **Unknowns:** unknown/unkeyed coordinate values = **passive categories** — they receive coordinates in the space but contribute **zero inertia** to axis derivation (standard MCA passive treatment). No imputation. No row deletion for partial unknowns.
- **Negatives:** the 38 graveyard kits (`canon_corpus.negative = 1`) are **excluded from derivation entirely** and projected **supplementary-only** for Gate B. Corpses may not shape the axes they exist to validate.
- **Rare-category fusing:** any category with **n < 10** active observations fuses into its register-defined parent bucket (per Greenacre's recommendation for MCA stability). Fusing map is emitted as a table in the gate report; fusing happens ONCE at Stage 0, identically for all four method families.

## 2. Block structure (for MFA weighting)

The 13 coordinates form **14 blocks**: each coordinate = 1 block, EXCEPT coordinate #5, which splits into 2 blocks per the register's two-facet structure. Block weighting per MFA standard: each block normalized by its first singular value, so no coordinate dominates axis formation by cardinality arithmetic alone.

- **Ordinal constraints:** **tempo** and **commit** ONLY (the two register coordinates with defensible order). All other coordinates treated nominal. (CATPCA branch applies the ordinal spline; MCA branch treats all nominal — divergence between the two is itself a diagnostic.)

## 3. Stage 1 — diagnostics (computed and reported BEFORE decomposition)

1. **Per-coordinate entropy** (normalized, 0–1) — flags near-constant coordinates (entropy < 0.1 → reported; NOT auto-dropped; gandalf rules with Matt visibility).
2. **Pairwise association matrix** — Cramér's V AND mutual information for all 78 coordinate pairs, with **Benjamini-Hochberg FDR at q = 0.05**. Near-duplicate pair (V > 0.8, significant) → reported as redundancy candidate; both retained for v1 derivation (demotion is an Edition-II decision, evidence-gated).
3. **Category frequency tables** post-fusing — the gate report shows the exact input the decomposition sees.

## 4. Stage 2 — the four method families (all four run; none is "the" method until gates rule)

| # | Family | Pinned parameters |
|---|---|---|
| 2a | **MCA / CATPCA** | Indicator-matrix MCA with **Greenacre-corrected inertia** (Benzécri correction rejected as over-optimistic; Greenacre adjusted rates reported). MFA block weighting per § 2. CATPCA twin with ordinal splines on tempo + commit. Dimension retention: **parallel analysis vs 1000 column-permutation null datasets** — retain dimensions whose corrected inertia exceeds the 95th percentile of the null. (Kaiser-style thresholds banned.) |
| 2b | **Gower → classical MDS** | Gower distance on the 13 coordinates (passive unknowns = missing per Gower's handling; equal coordinate weights — block weighting is § 2's job in 2a, not double-applied here). Classical (Torgerson) MDS; eigenvalue scree + same permutation-null retention rule. |
| 2c | **Leiden communities** | kNN graph on Gower distance, **k = 10**; Leiden with **CPM objective**, resolution scan **0.5–2.0** in steps of 0.1; consensus across 100 seeds per resolution; report the resolution plateau (stable partition count across ≥ 3 consecutive steps). |
| 2d | **Latent Class Analysis** | Standard LCA on the 13 categorical coordinates; **k = 2..12**; selection by **BIC** (AIC + sample-size-adjusted BIC reported alongside; BIC governs); 50 random starts per k; entropy-based class-separation reported. |

**Triangulation rule:** the candidate map basis comes from 2a (or 2b if 2a fails retention); 2c and 2d are *independent witnesses*. Agreement measure: ARI between Leiden partition / LCA classes / k-means-on-retained-dimensions. **Agreement across families is evidence; disagreement is a reported finding, not a tuning invitation.**

## 5. Stage 3 — the four gates (all must pass to freeze Edition I)

| Gate | Test | Pinned threshold |
|---|---|---|
| **A — group recovery** | The 6 confirmed cross-franchise groups (WHIRLWIND n=15, TOTEM/SENTRY n=26, TRAP/MINE n=24, CHANNELED BEAM n=9, AURA n=8, MINION/PET n=7) must re-emerge unsupervised. ARI between derived clustering and the 6-group labeling (on labeled subset); per-group silhouette in the retained space. | **ARI ≥ 0.6** AND **silhouette ≥ 0.2 for ≥ 5 of 6 groups** |
| **B — negative geography** | Project the 38 negatives (supplementary). Test: mean pairwise distance among red-law corpses vs permutation null (10,000 permutations of 38 random corpus kits). Corpses of the same red law must sit closer than chance. | **p < 0.05** (per red law with ≥ 5 corpses; Fisher-combined across laws reported) |
| **C — franchise mixing** | PERMANOVA (adonis2-style) of franchise label on the retained-space distances. The map must organize by behavior, not by game of origin. | **franchise R² ≤ 0.15** |
| **D — stability** | (i) 1000× bootstrap at 90% subsample, Procrustes-aligned: **median kit displacement ≤ 10% of plane diameter**. (ii) Leave-one-franchise-out, refit, Procrustes correlation vs full fit: **≥ 0.85 for every held-out franchise**. (iii) Inverse-√franchise-size reweighted refit, Procrustes vs unweighted: **≥ 0.85**. | all three |

**Decision rule (pinned):**
- **All four pass** → freeze Edition I on the 2a basis (or 2b per § 4 triangulation rule). gandalf names axes from loadings. Matt ratifies the freeze.
- **Any gate fails** → NO tuning-until-pass. One protocol-amendment cycle is permitted (§ 9) IF the failure diagnosis identifies a pinnable cause (e.g., a fusing error); otherwise → **fallback clause**: exact lattice at meso-grain ships as the census dashboard + published negative finding. A second full re-derivation attempt requires a fresh pre-registration (v2) with jack-ryan review.

## 6. Stage 4 — freeze + naming

- Frozen artifacts: rotation/loading matrices, category coordinates, retained-dimension count, plane diameter, all gate statistics → versioned in the corpus DB + emitted into `atlas.json` (derived-basis block per renderer-spec § 2 amendment).
- **Axis naming:** gandalf reads the top-loading categories per retained dimension and names axes from what the data says. **Placeholder names (Tempo × Footprint etc.) are banned** — those were mobile-Claude's invented axes; the whole point of this instrument is that we don't get to invent them.
- **Inertia badge:** the chart carries "this plane explains X% of corrected inertia" — visible on every render, both skins.

## 7. Deliverables (elrond returns)

1. **Reproducible script** — lineage of `family-discovery-poc-rerank.py` (same repo home, same style: pinned seed, single entrypoint, runs against the snapshot tag). Every number in the gate report must regenerate from one command.
2. **Gate report** (markdown, `agentic_orchestration/elrond/…`) — Stage 1 diagnostics tables; per-family results; the four gate statistics with pass/fail; fusing map; N accounting (active/passive/supplementary). **Numbers only — interpretation is gandalf's.**
3. **`atlas.json` derived-basis block** draft (if gates pass) for star-lord/drax consumption.

## 8. Explicitly out of scope for this run

- Ghost-field enumeration (waits on the feasibility-cuts register — decoupled by charter § 4).
- Any sim input whatsoever (engine-native epoch only — charter § 7).
- Feel-layer / build-guide annotations (Legolas commission; overlay candidate, never axis input).
- Coordinate demotion/merge (Edition-II, evidence-gated).
- t-SNE/UMAP/force-directed anything (refused as map; permitted as exploratory appendix figures ONLY if labeled non-canonical).

## 9. Protocol-amendment log

*(empty at pin time — every deviation during execution lands here with timestamp, what changed, why, and jack-ryan visibility)*

---

**Signed:** gandalf (SPEC-AUTHOR) — pinned 2026-07-14, pre-execution.
**Gate-1:** jack-ryan methodology review owed BEFORE elrond executes. This document is binding only if reviewed before results exist.
