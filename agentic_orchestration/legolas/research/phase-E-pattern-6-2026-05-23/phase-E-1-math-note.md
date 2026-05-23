# Phase E-1 Math Note — Pattern-6 Axis Discovery + Clustering

**Author:** legolas  
**Date:** 2026-05-23  
**Status:** PRE-FIRE — authored before any analytical code runs (Discipline #1 math-before-code)  
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-pattern-6-axis-discovery.md`

---

## 1. Feature Engineering Plan

### 1.1 Text-embedding source (OQ1 resolution)

**Decision: TF-IDF on concatenated text, NOT sentence-transformers.**

Rationale:
- sentence-transformers requires ~700MB torch install; elrond documented this pivot in Phase D (Q5 resolution) and successfully used sklearn TF-IDF cosine for Step 7 cross-source merge.
- Consistency with Phase D substrate: using the same embedding space as Phase D means the feature vectors are comparable and reproducible without an external model checkpoint.
- The v_category_sample text quality (description_text coverage 91.98%, avg length ~700 chars) is sufficient for TF-IDF to capture meaningful vocabulary-level axis separations.
- Reproducibility: TF-IDF vocabulary is derived from the corpus itself; no external model version dependency; corpus hash pins the vocabulary.

**TF-IDF configuration:**
- Input text: concatenation of `canonical_name` + `description_text` (space-separated) + `cultural_lineage_tags` (JSON-decoded, joined). For rows with NULL description_text (1,339 rows, 8.02%): use `canonical_name` + `structured_properties` (weapon_type field if present).
- Vectorizer: `TfidfVectorizer(max_features=500, min_df=3, max_df=0.95, sublinear_tf=True, analyzer='word', ngram_range=(1,2))`
- Post-vectorization dimensionality reduction: TruncatedSVD (LSA) to 100 components before combining with structured features. This produces a dense 100-dim semantic embedding per row.
- Reproducibility hash: SHA-256 of (sorted canonical_name list + vectorizer vocabulary) captured in Deliverable 1 artifact.

### 1.2 Structured feature vector composition

Structured features extracted per row (all from Phase-D canonical columns — DO NOT re-derive):

| Feature group | Columns | Encoding | Dimensions |
|---|---|---|---|
| Cultural lineage | `cultural_lineage_canonical` | One-hot (11 values) | 11 |
| Historical period | `historical_period_canonical` | One-hot (8 values) | 8 |
| Register | `register_canonical` | One-hot (5 values) | 5 |
| Weapon kind | `weapon_kind` | One-hot (2 values in v_category_sample: category/named_template) | 2 |
| Wieldability | `wieldable_humanoid` | One-hot (4 values: one_hand/two_hand/either/shoulder_supported) | 4 |
| Weapon type (from canonical_name) | Extracted by regex matching 30 known weapon type tokens | Multi-hot binary (30 dim) | 30 |

Total structured features: 60 dimensions.

**Weapon type token set (30):** sword, longsword, greatsword, shortsword, rapier, scimitar, sabre, axe, battleaxe, greataxe, hammer, mace, flail, club, staff, wand, bow, crossbow, javelin, spear, lance, pike, halberd, glaive, dagger, knife, pistol, rifle, musket, shotgun. Applied as binary flags on canonical_name (case-insensitive substring match).

**Normalization:** All one-hot/multi-hot columns are already in [0,1]. TF-IDF LSA output is L2-normalized per row before concatenation. Structured block is standardized (StandardScaler) independently. Final feature matrix = L2-norm(LSA-100) || StandardScaler(structured-60) concatenated horizontally = 160 dimensions total.

**Total feature dimensionality: 160** (100 text-semantic + 60 structured).

### 1.3 Missing value imputation strategy (OQ2 resolution)

**Decision: unprocessed rows in v_category_sample are treated as canonical-of-record for Phase E-1.**

Rationale: The v_category_sample view definition explicitly includes `dedup_status IN ('canonical','unprocessed')`. This is by design — unprocessed museum rows that passed wieldability and weapon_kind filters are valid category-sampling substrate. Phase D §7.5 confirms Step 6.5 gap-filled wieldable_humanoid for these rows. They have 99.86% cultural_lineage_canonical coverage (Step 6.5 populated these via source-driven rules).

For the 1,339 rows (8.02%) with NULL or empty description_text: impute text field as `canonical_name || ' ' || COALESCE(json_extract(structured_properties,'$.weapon_type'),'')`. This ensures all rows contribute to TF-IDF vocabulary; zero-length strings are excluded from vocabulary building but still get a sparse zero vector (which projects to near-zero in LSA — acceptable for structured-only rows).

### 1.4 F2 inverse-frequency weighting application (F2-locked)

**Per-row weight = 1 / freq(cultural_lineage_canonical) for that row's lineage bucket, then normalized so weights sum to N (preserve total effective sample size).**

Empirical lineage frequencies (from v_category_sample, total 16,699):

| cultural_lineage_canonical | count | raw_freq | raw_weight (1/freq) | normalized_weight |
|---|---|---|---|---|
| fantasy_generic | 15,774 | 0.94519 | 1.0578 | 0.1120 |
| south_american_indigenous | 509 | 0.03048 | 32.79 | 3.472 |
| european | 254 | 0.01521 | 65.74 | 6.963 |
| east_asian | 51 | 0.00305 | 327.4 | 34.67 |
| middle_eastern | 49 | 0.00293 | 341.2 | 36.12 |
| unknown | 23 | 0.00138 | 726.9 | 76.96 |
| south_asian | 22 | 0.00132 | 759.1 | 80.38 |
| southeast_asian | 9 | 0.000539 | 1855 | 196.4 |
| arctic_circumpolar | 5 | 0.000299 | 3339 | 353.6 |
| african | 2 | 0.000120 | 8350 | 884.0 |
| north_american_indigenous | 1 | 0.0000599 | 16,699 | 1768 |

Note: fantasy_generic dominates at 94.5% pre-weighting. Post F2-weighting, fantasy_generic rows receive weight ~0.112 (down from 1.0 equal-weight) while rare lineages receive weights up to 1768x. The normalization factor is: sum_of_raw_weights = 16699 × (sum of per-row 1/freq values) / 16699 = weighted_average(1/freq). Normalization: each w_i = (1/freq_i) / mean(1/freq over all rows) × 1.0.

**Application scope:** Apply as `sample_weight` parameter during:
1. TruncatedSVD fit (note: sklearn's TruncatedSVD does not accept sample_weight directly; workaround: row-multiply feature matrix by sqrt(w_i) before SVD, equivalent to weighted PCA).
2. StandardScaler fit (use `sample_weight` parameter, sklearn ≥1.0 supports this).
3. HDBSCAN: no native sample_weight support; apply by duplicating high-weight rows at integer weight rounded (rows with w > 2 get duplicated; the duplicated matrix is used for fit-only, then assignments mapped back to original 16,699 rows).
4. GMM baseline: `weights_` initialization influenced by `fit` on weighted-duplicated matrix same as HDBSCAN.

This weighting scheme ensures PCA axes are not captured entirely by the fantasy_generic vocabulary axis (which would otherwise dominate PC1).

### 1.5 PCA chunk strategy

**Algorithm: TruncatedSVD (sklearn) with n_components=50 in first pass, then scree-plot truncation.**

Rationale for TruncatedSVD over full PCA:
- N=16,699 × p=160 dense matrix: 16,699 × 160 × 8 bytes = ~21.4MB. Fits in memory easily.
- However, the weighted matrix (after row-multiplication by sqrt(w)) has the same dimensionality but different scale; still fits in memory.
- TruncatedSVD from sklearn is numerically equivalent to PCA on centered data and handles our dense feature matrix efficiently.
- `n_iter=10` for numerical stability on the weighted matrix.

**Top-k retention strategy:**
1. First fit with n_components=50; capture explained_variance_ratio_.
2. Compute cumulative explained variance; find k_80 where cumsum first crosses 80%.
3. Apply scree-plot kink detection: compute second-derivative of explained_variance_ratio_; the kink (inflection) is at the index of maximum second-derivative drop.
4. Final k = min(k_80, kink_index + 2, 12) — capped at 12 per dispatch target.
5. Minimum: k ≥ 8 per acceptance criterion. If scree kink suggests < 8, retain top-8 regardless.

### 1.6 Per-axis loading interpretability check

Per axis retained:
1. Compute top-20 feature loadings by absolute magnitude.
2. Verify "spread condition": top-1 loading should not account for >60% of the total loading L2-norm of top-20. If a single feature dominates one axis (>60%), flag that axis as a "single-feature axis" for Phase E-2 review.
3. Verify "cross-block condition": at least 1 of top-5 loadings should come from each block (text vs structured). If an axis is purely text or purely structured, note it — acceptable but warrants gandalf labeling attention.
4. Bootstrap stability (see §1.7).

### 1.7 Stability check

**Bootstrap strategy:**
- 10 bootstrap resamples of the 16,699-row weighted matrix (resample with replacement, preserving F2 weights).
- For each resample: fit TruncatedSVD with same k; extract top-k component vectors.
- Stability metric per axis i: mean cosine-distance between the i-th component vector on the full fit vs all 10 bootstrap fits. Cosine-distance = 1 - |cos(θ)| (absolute-value because PCA sign is arbitrary).
- Acceptance: mean cosine-distance ≤ 0.10 per gandalf §4.2.
- If any axis has mean cosine-distance > 0.10: flag as "unstable axis" for Phase E-1-bis review. Do not drop unilaterally — surface for Matt.

### 1.8 HDBSCAN parameter selection

**Primary parameters (anchor to N=16,699):**

| Parameter | Value | Rationale |
|---|---|---|
| `min_cluster_size` | 30 | Center of gandalf §4.3 guidance band (20-50); N=16,699 → 30 gives ~556 clusters max possible; at 50-150 target, this is the right scale |
| `min_samples` | 5 | Conservative noise-tolerance; reduces noise-point count while maintaining density sensitivity |
| `cluster_selection_epsilon` | 0.05 | Post-cluster-selection merge threshold; prevents over-splitting at high-density regions |
| `cluster_selection_method` | `'eom'` | Excess of Mass — more stable cluster boundaries than 'leaf' for uneven density distributions |
| `metric` | `'euclidean'` | On the PCA-projected (8-12 dim) space + standardized categorical features |

**If primary parameters yield < 50 clusters:** try min_cluster_size=20 (lower bound of band).
**If primary parameters yield > 150 clusters:** try min_cluster_size=50 (upper bound of band).
Document parameter sweep in Deliverable 3.

**Noise point treatment (OQ3 resolution):**

**Decision: assign noise points to nearest cluster via soft-assignment probability; do NOT leave as cluster_id NULL.**

Rationale:
- F6 requires N=20-50 per cluster for downstream sampling; noise points left NULL would reduce effective sample pool.
- For noise points: compute distance to each cluster centroid in the projection space; assign cluster_id = argmin(distance); set confidence_score = 1 / (1 + min_distance) normalized to [0, 0.5) — explicitly flagged below 0.5 so downstream consumers can identify originally-noise-assigned rows.
- MIGRATION.md will document this convention (confidence_score < 0.5 = originally HDBSCAN noise).

### 1.9 PCA whitening + scaling (OQ4 resolution)

**Decision: StandardScale structured features; L2-normalize LSA output; NO whitening on PCA output.**

Rationale:
- Pre-PCA scaling prevents high-variance structured features (particularly the weapon-type multi-hot block) from dominating axes.
- Post-PCA whitening (dividing by singular values) would equalize all axes' variance, making low-variance axes artificially prominent. Since our goal is discovering the naturally dominant axes, whitening is counterproductive.
- The F2 row-weighting already reshapes the effective covariance; post-whitening on top of that would over-correct.

### 1.10 Cluster purity measurement (OQ5 resolution)

**Decision: primary purity key = `cultural_lineage_canonical`; secondary validation = `register_canonical`.**

Rationale:
- Cultural lineage is the primary axis the F2 weighting is designed to correct for; it is the most semantically meaningful per-cluster label available.
- Purity formula: for cluster j with N_j members, purity_j = max_lineage(count(lineage_l in cluster j)) / N_j.
- Mean purity = weighted mean of purity_j across all clusters (weighted by N_j).
- Acceptance threshold: ≥ 0.85 per gandalf §4.3.
- Secondary validation: same formula applied to `register_canonical`; report alongside primary purity in Deliverable 3.

Note: the v_category_sample distribution is 94.5% fantasy_generic. A trivial cluster of all fantasy_generic rows achieves purity = 0.945. The F2 weighting during clustering is specifically designed to prevent this — clusters that emerge should be distinguished by weapon-type / period / wieldability axes, not primarily by the fantasy_generic dominance. Post-clustering purity is therefore expected to be driven by the weapon-type/period axis structure, not by lineage monoculture.

### 1.11 GMM-baseline and k-means-baseline

**GMM:** `GaussianMixture(n_components=k_gmm, covariance_type='diag', random_state=42)` where k_gmm is the HDBSCAN-determined cluster count (if in 50-150 range; else use 80 as default). Soft-assignment probabilities from `predict_proba()` used as confidence_score for comparison.

**k-means:** `KMeans(n_clusters=k_hdbscan, random_state=42, n_init=10)`. Hard assignment; confidence_score = 1.0 / (1 + dist_to_centroid / mean_dist_to_centroid).

Both baselines are used for **comparison and validation only**; HDBSCAN is the primary output written to DB per dispatch.

### 1.12 Acceptance gate verification queries (pre-authored)

```sql
-- Gate A: clusters table populated
SELECT COUNT(*) FROM clusters;
-- PASS condition: COUNT >= 50 AND COUNT <= 150

-- Gate B: cluster_membership populated
SELECT COUNT(*) FROM cluster_membership;
-- PASS condition: COUNT = 16699 (one row per v_category_sample row)

-- Gate C: weapon_knowledge_entries.cluster_id populated
SELECT COUNT(*) FROM weapon_knowledge_entries 
WHERE cluster_id IS NOT NULL;
-- PASS condition: COUNT = 16699 (matches v_category_sample)

-- Gate D: no orphaned cluster_id references
SELECT COUNT(*) FROM weapon_knowledge_entries w
LEFT JOIN clusters c ON w.cluster_id = c.id
WHERE w.cluster_id IS NOT NULL AND c.id IS NULL;
-- PASS condition: COUNT = 0

-- Gate E: F6 flag — clusters with < 20 members
SELECT id, label, member_count FROM clusters WHERE member_count < 20;
-- These clusters flagged for Phase E-2 merge/split decision

-- Gate F: purity check (requires post-run query on cluster_membership + weapon_knowledge_entries)
-- Computed in Python post-clustering; target >= 0.85

-- Gate G: axis count
SELECT COUNT(*) FROM -- (axes stored in phase-E-1-axis-loadings.json, not in DB table)
-- PASS condition: 8 <= k <= 12

-- Gate H: bootstrap stability
-- All per-axis mean cosine-distance <= 0.10 (stored in phase-E-1-axis-discovery.md)
```

---

## 2. Open Question Resolutions Summary

| OQ | Resolution |
|---|---|
| OQ1 Embedding model | TF-IDF + TruncatedSVD (LSA); NOT sentence-transformers (unavailable; consistent with Phase D Q5 decision) |
| OQ2 Unprocessed rows | Treated as canonical-of-record per v_category_sample design; canonical columns populated by Step 6.5 |
| OQ3 Noise point treatment | Assign to nearest cluster; confidence_score < 0.5 flags originally-noise rows |
| OQ4 PCA whitening/scaling | StandardScale pre-PCA; L2-norm LSA output; NO post-PCA whitening |
| OQ5 Cluster purity key | cultural_lineage_canonical (primary); register_canonical (secondary validation) |
| OQ6 Provisional axis names | Yes, PROVISIONAL; header annotated; gandalf is canonical authority in Phase E-2 |
| OQ7 Phase E-1-bis trigger | Bimodal loadings per axis (second mode >20% of first mode L2-norm), or any bootstrap cosine-distance >0.10, or cluster count significantly outside 50-150 range |

---

## 3. Sequencing Constraint Verification

Strict sequence:
1. Math note (THIS DOCUMENT) — complete before code fires
2. Deliverable 1: Feature engineering (TF-IDF fit + structured features + F2 weight vector)
3. Deliverable 2: Axis discovery (TruncatedSVD on weighted matrix + bootstrap stability)
4. Deliverable 3: Clustering (HDBSCAN on axis projections + baselines)
5. Deliverable 4: DB population (clusters + cluster_membership + weapon_knowledge_entries.cluster_id)
6. Deliverable 5: Completion summary

Round-trip smoke (100-row sample) fires between Deliverable 3 and Deliverable 4 to verify pipeline before full write.

---

**Signed:** legolas  
**Status:** Math note complete — analytical code authorized to fire.
