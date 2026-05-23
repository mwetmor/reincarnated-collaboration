# Phase E-1 — Deliverable 1: Feature Engineering

PROVISIONAL — gandalf reviews axes in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Mode:** A (analytical)
**Status:** Complete

---

## Text Embedding

**Model:** TF-IDF (sklearn TfidfVectorizer) + TruncatedSVD (LSA) — 100 components
**Rationale for TF-IDF over sentence-transformers:** sentence-transformers requires ~700MB torch install (unavailable); consistent with Phase D Q5 pivot; reproducible without external model checkpoint.

**TF-IDF configuration:**
- max_features: 500
- min_df: 3
- max_df: 0.95
- sublinear_tf: True
- ngram_range: (1, 2)
- Input text: canonical_name + description_text (capped 2000 chars) + cultural_lineage_tags

**LSA configuration:** TruncatedSVD(n_components=100, n_iter=10, random_state=42)
**Vocabulary hash (SHA-256[:16]):** `03eeccc2b8e4f6b1`
**Post-LSA normalization:** L2 per row

**F2 weighting application:** Row-multiply TF-IDF matrix by sqrt(w_i) before SVD fit (equivalent to weighted PCA).

---

## Structured Feature Vector

**Dimensions:** 60 total (11 lineage + 8 period + 5 register + 2 kind + 4 wield + 30 weapon-type)

| Feature group | Source columns | Encoding | Dimensions |
|---|---|---|---|
| Cultural lineage | cultural_lineage_canonical | One-hot | 11 |
| Historical period | historical_period_canonical | One-hot | 8 |
| Register | register_canonical | One-hot | 5 |
| Weapon kind | weapon_kind | One-hot | 2 |
| Wieldability | wieldable_humanoid | One-hot | 4 |
| Weapon type | canonical_name (regex match) | Multi-hot binary | 30 |

**Normalization:** StandardScaler (weighted mean/std using F2 weights)
**DO NOT re-derive canonical columns** — sourced from Phase D Step 6.5 output.

---

## Total Feature Dimensionality

| Component | Dimensions |
|---|---|
| LSA text-semantic | 100 |
| Structured | 60 |
| **Total** | **160** |

---

## Feature Coverage

| Field | Rows covered | Coverage % |
|---|---|---|
| description_text (non-null, non-empty) | 43901 | 90.65% |
| structured_properties (non-empty) | 48224 | 99.57% |
| cultural_lineage_canonical | 46474 | 95.96% (excl unknown) |
| Total rows | 48430 | 100% |

Rows with NULL/empty description_text (4529, 9.35%) are imputed with canonical_name + structured_properties weapon_type.

---

## F2 Inverse-Frequency Weight Vector

Per cultural_lineage_canonical bucket (math note §1.4):

| cultural_lineage_canonical | count | freq | raw_weight (1/freq_count) | normalized_weight |
|---|---|---|---|---|
| fantasy_generic | 16284 | 0.33624 | 0.000061 | 0.2124 |
| east_asian | 13080 | 0.27008 | 0.000076 | 0.2645 |
| european | 12515 | 0.25841 | 0.000080 | 0.2764 |
| unknown | 1956 | 0.04039 | 0.000511 | 1.7686 |
| middle_eastern | 1327 | 0.02740 | 0.000754 | 2.6068 |
| cross_cultural | 883 | 0.01823 | 0.001133 | 3.9177 |
| south_asian | 822 | 0.01697 | 0.001217 | 4.2084 |
| southeast_asian | 694 | 0.01433 | 0.001441 | 4.9846 |
| african | 465 | 0.00960 | 0.002151 | 7.4393 |
| south_american_indigenous | 197 | 0.00407 | 0.005076 | 17.5598 |
| mesoamerican | 83 | 0.00171 | 0.012048 | 41.6781 |
| arctic_circumpolar | 56 | 0.00116 | 0.017857 | 61.7730 |
| oceanic | 39 | 0.00081 | 0.025641 | 88.6996 |
| north_american_indigenous | 29 | 0.00060 | 0.034483 | 119.2857 |

**Normalization:** weights divided by mean(raw_weight) so mean normalized_weight = 1.0
**Application (Single-Stage F2 Doctrine — Option-A 2026-05-23):** F2 applied as sqrt(w_i) row-multiplication on TF-IDF before SVD (PCA stage); as sample_weight on StandardScaler mean/std (feature-scaling stage). NOT applied at clustering stage; clusters reflect actual projection-space density in the F2-amplified coordinate system. (Note: GMM was always implemented without row-duplication — script line 510: gmm.fit(projections_k). The original math note §1.4 claim of "integer-duplication for GMM fit" was overstated vs actual code implementation.) See design-side ratification: gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md

---

**Reproducibility:** Python 3.x + sklearn 1.8.0 + numpy 1.26.2 + hdbscan
Corpus hash (vocabulary SHA-256[:16]): `03eeccc2b8e4f6b1`
DB path: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
