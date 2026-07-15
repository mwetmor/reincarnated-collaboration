# Atlas Derivation — Pre-Registration (pinned analysis plan)

**Date:** 2026-07-14 · **Author:** gandalf (SPEC-AUTHOR) · **Status:** v1.1 — PINNED. jack-ryan Gate-1 review returned **PASS-WITH-AMENDMENTS** (`agentic_orchestration/qa/findings/2026-07-14-gate1-atlas-derivation-prereg.md`, 7 amendments A1–A7); all seven applied in v1.1 BEFORE execution (§ 9 log). Execution is authorized against THIS version.
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
- **[A1] Gate-A labeled subset — FROZEN ARTIFACT.** The 6-group membership labeling is frozen as an explicit `kit_id → group` table: `agentic_orchestration/gandalf/design-inputs/2026-07-14-gate-a-group-labels.csv` (86 kits; WHIRLWIND 15 · TOTEM-SENTRY 24 · TRAP-MINE 23 · CHANNELED-BEAM 9 · AURA 8 · MINION-PET 7), authored by gandalf and committed BEFORE any decomposition runs. Derivation: deterministic FCA concept extents (script `gate-a-labels-extract.py`, POC lineage, post-A.5 snapshot, negative=0, N=469), matched to the confirmed View-2 signatures; the 3 double-membered kits resolved by **most-specific-intent** (d2-auradin → AURA; tl2-bot-engineer + tli-moto-bots → MINION-PET) — hence TOTEM-SENTRY 26→24 and TRAP-MINE 24→23 vs the View-2 counts (View-2 double-counted the overlaps). `mobile_key_group` is DEPRECATED (register §6) and MUST NOT be used. Kits not in the table are the unlabeled remainder and receive no Gate-A label. elrond loads this CSV into table `atlas_gateA_labels_2026_07_14` at Stage 0, byte-verbatim.
- **[A2] "Franchise" — PINNED.** For Gates C–D, franchise = the game-series rollup, materialized as column `franchise_rollup` at Stage 0: **PoE** = poe1 ∪ poe2 · **Diablo** = d2 ∪ d3 ∪ d4 ∪ di · **TitanQuest** = tq ∪ tq2 · **Hades** = hades1 ∪ hades2 · **Torchlight** = tl1 ∪ tl2 ∪ tli · all others (gd, le, vs, chronicon, hot, undecember) = own franchise → **11 franchises**. Gate C PERMANOVA and Gate D LOFO both group on `franchise_rollup`, NEVER on raw `game`.

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
| 2c | **Leiden communities** | kNN graph on Gower distance, **k = 10**; Leiden with **CPM objective**, resolution scan **0.5–2.0** in steps of 0.1; consensus across 100 seeds per resolution; report the resolution plateau (stable partition count across ≥ 3 consecutive steps). **[A7] Dependency pin:** requires `leidenalg`+`python-igraph` (or `python-igraph`'s native `community_leiden` with CPM). If unavailable, substitution to Louvain is a **§ 9 PROTOCOL AMENDMENT** — logged with timestamp, NOT a silent swap — because Louvain optimizes modularity (resolution-limited, non-CPM) and can merge exactly the small communities Gate A stresses (AURA/MINION-PET). MCA/LCA/MDS have no hard external dependency (SVD-on-indicator, EM multinomial mixture, classical eigendecomposition) and need no substitution clause. |
| 2d | **Latent Class Analysis** | Standard LCA on the 13 categorical coordinates; **k = 2..12**; selection by **BIC** (AIC + sample-size-adjusted BIC reported alongside; BIC governs); 50 random starts per k; entropy-based class-separation reported. |

**Triangulation rule:** the candidate map basis comes from 2a (or 2b if 2a fails retention); 2c and 2d are *independent witnesses*. Agreement measure: ARI between Leiden partition / LCA classes / k-means-on-retained-dimensions. **Agreement across families is evidence; disagreement is a reported finding, not a tuning invitation.**

## 5. Stage 3 — the four gates (all must pass to freeze Edition I)

| Gate | Test | Pinned threshold |
|---|---|---|
| **A — group recovery** | The 6 confirmed cross-franchise groups per the **[A1] frozen label table** (WHIRLWIND 15 · TOTEM-SENTRY 24 · TRAP-MINE 23 · CHANNELED-BEAM 9 · AURA 8 · MINION-PET 7; 86 labeled kits) must re-emerge unsupervised. ARI between derived clustering and the frozen labeling (on the labeled subset only); per-group silhouette in the retained space. | **ARI ≥ 0.6** AND **[A3]** silhouette ≥ 0.2 for ≥ 5 of 6 groups, where **the four large groups (WHIRLWIND, TOTEM-SENTRY, TRAP-MINE, CHANNELED-BEAM) must ALL clear 0.2** — the single permitted sub-threshold group may only be AURA or MINION-PET (n ≤ 8, silhouette intrinsically high-variance). A large-group silhouette failure fails Gate A outright. |
| **B — negative geography** | Project the 38 negatives (supplementary; partial keys → passive per Stage 0). **[A6] as applied to the post-A.5 death_class census (intrinsic-red = 5 TOTAL — no single red law reaches n=5):** the pass/fail test is the **POOLED intrinsic-red set** (k=5, meets the ≥5 evaluability bar); per-law tests are reported **descriptively only** (all underpowered); **extrinsic-tuning corpses (k=6) run as a SECONDARY reported test** (their §A.2 locational prediction: rooted/channel + shield-verb territory) — informative, NON-gating, because ambers are recoverable-by-design, not danger zones. Test statistic: mean pairwise distance among the test set vs permutation null — **null = 10,000 draws of k kits from the ACTIVE (non-negative, non-supplementary) projected set, k matched to the test set**. | **p < 0.05** on the pooled intrinsic-red test |
| **C — franchise mixing** | PERMANOVA (adonis2-style) of **`franchise_rollup` [A2]** on the retained-space distances. The map must organize by behavior, not by game of origin. **[A4] PERMDISP companion:** report betadisper/PERMDISP (dispersion homogeneity across franchises) alongside. | **franchise R² ≤ 0.15**, interpretable as a pass ONLY if PERMDISP p ≥ 0.05; if PERMDISP is significant, the gate report flags it and gandalf rules whether the R² reflects genuine mixing vs an imbalance/dispersion artifact (Diablo+PoE ≈ 60% of mass — R² alone is not self-interpreting). |
| **D — stability** | (i) 1000× bootstrap at 90% subsample, Procrustes-aligned: **median kit displacement ≤ 10% of plane diameter [A5]**. (ii) Leave-one-**franchise_rollup**-out **[A2]**, refit, Procrustes correlation vs full fit: **≥ 0.85 for every held-out franchise**. (iii) Inverse-√franchise-size reweighted refit, Procrustes vs unweighted: **≥ 0.85**. **[A5] plane diameter** = the maximum pairwise Euclidean distance between any two ACTIVE (non-supplementary) kit coordinates in the retained-dimension space of the frozen basis, computed once on the full fit; all Gate-D displacement percentages use this scalar as denominator. | all three |

**Decision rule (pinned):**
- **All four pass** → freeze Edition I on the 2a basis (or 2b per § 4 triangulation rule). gandalf names axes from loadings. Matt ratifies the freeze.
- **Any gate fails** → NO tuning-until-pass. One protocol-amendment cycle is permitted (§ 9) IF the failure diagnosis identifies a pinnable cause (e.g., a fusing error); otherwise → **fallback clause**: exact lattice at meso-grain ships as the census dashboard + published negative finding. A second full re-derivation attempt requires a fresh pre-registration (v2) with jack-ryan review.

## 6. Stage 4 — freeze + naming

- Frozen artifacts: rotation/loading matrices, category coordinates, retained-dimension count, **plane diameter (per the [A5] definition — max pairwise active-point distance in retained space)**, all gate statistics → versioned in the corpus DB + emitted into `atlas.json` (derived-basis block per renderer-spec § 2 amendment).
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

**2026-07-14 (pre-execution, v1 → v1.1) — Gate-1 amendments A1–A7 applied.** jack-ryan DESIGN-MODE review returned PASS-WITH-AMENDMENTS (findings: `agentic_orchestration/qa/findings/2026-07-14-gate1-atlas-derivation-prereg.md`); all seven applied before any decomposition ran: A1 frozen Gate-A label table (§1 — artifact committed: `2026-07-14-gate-a-group-labels.csv`, 86 kits, overlap-resolved most-specific-intent); A2 franchise_rollup pinned (§1, 11 franchises); A3 large-groups-must-all-clear silhouette constraint (§5 Gate A); A4 PERMDISP companion + interpretation guard (§5 Gate C); A5 plane-diameter definition (§5 Gate D + §6); A6 Gate-B pooling — **applied in POOLED form** because the post-A.5 death_class census (landed in parallel with the review) shows intrinsic-red = 5 TOTAL, so jack-ryan's per-law ≥5 criterion is met only at the pooled level; extrinsic-tuning added as secondary non-gating test (flagged for jack-ryan visibility — a refinement within A6's intent, pinned pre-execution); A7 Leiden dependency pin + Louvain-substitution-as-amendment clause (§4 2c). No results existed when these landed.

*(Execution-time deviations land below with timestamp, what changed, why, and jack-ryan visibility.)*

---

**Signed:** gandalf (SPEC-AUTHOR) — pinned 2026-07-14, pre-execution.
**Gate-1:** jack-ryan methodology review owed BEFORE elrond executes. This document is binding only if reviewed before results exist.
