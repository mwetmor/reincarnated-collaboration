# Phase E-1 — Deliverable 3: Clustering Output (subsample-k3 frame revision)

PROVISIONAL — gandalf labels clusters canonically in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Mode:** subsample-k3 (frame-revision dispatch 2026-05-23)
**Status:** Complete

---

## Summary

| Metric | Value |
|---|---|
| Total rows assigned (full pool) | 48430 |
| HDBSCAN clusters (final) | 125 |
| HDBSCAN min_cluster_size | 10 |
| HDBSCAN training subsample N | 10000 |
| Subsample rows (hdbscan_native) | 10000 |
| Non-subsample rows (nearest_centroid) | 38430 |
| Originally-noise rows within subsample (confidence < 0.5) | 8052 |
| F6 flag: clusters < 20 members | 0 |
| Mean cluster purity (cultural_lineage, all rows) | 0.9444 (94.44%) |
| Purity PASS (≥ 0.70) | YES |
| Purity PASS (≥ 0.85, original threshold) | YES |
| k axes used | 3 (substrate-voted) |
| F2 inverse-frequency weighting applied | Yes (at PCA + StandardScaler stages) |
| GMM baseline | N/A (skipped in subsample-k3 mode) |
| k-means baseline | N/A (skipped in subsample-k3 mode) |

**Acceptance gate status:**
- ≥ 50 clusters: **PASS** ✓
- Mean purity ≥ 0.70: **PASS** ✓

**Assignment provenance (MIGRATION.md §4 requirement):**
- `hdbscan_native`: rows in the ~10000-row stratified subsample; cluster_id assigned by HDBSCAN density-based clustering on the 3-axis projection subspace.
- `nearest_centroid`: remaining ~38430 rows; cluster_id assigned by nearest-centroid distance in the 3-axis projection space. These rows have lower clustering confidence (confidence_score < 0.5 range). Phase E-2 label-quality work MUST NOT assume equal density-based confidence across all rows.

---

## Top 5 Clusters by Member Count

### Rank 1: Cluster 90 (N=10087)

- **Provisional description:** PROVISIONAL: east_asian unknown rifle/spear weapons (historical register; category; N=10087)
- **Dominant lineage:** east_asian (10087 rows)
- **Dominant period:** unknown (10086 rows)
- **Dominant register:** historical (10087 rows)
- **Top weapon types:** rifle(12), spear(1), sabre(1)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 158 | H/AKJ-16 | east_asian | unknown | 1.0000 |
| 723 | Q132210441 | east_asian | unknown | 1.0000 |
| 1004 | Teppô | east_asian | unknown | 1.0000 |

---

### Rank 2: Cluster 62 (N=4807)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/greataxe weapons (fantasy register; named_template; N=4807)
- **Dominant lineage:** fantasy_generic (4807 rows)
- **Dominant period:** fictional (4806 rows)
- **Dominant register:** fantasy (4807 rows)
- **Top weapon types:** axe(12), greataxe(9), battleaxe(2)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13478 | Abyssal Bane Chakram (very rare variant) | fantasy_generic | fictional | 1.0000 |
| 13513 | Abyssal Bane Knuckle Duster (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13514 | Abyssal Bane Knuckle Duster (very rare variant) | fantasy_generic | fictional | 1.0000 |

---

### Rank 3: Cluster 112 (N=2062)

- **Provisional description:** PROVISIONAL: european modern rifle/spear weapons (historical register; category; N=2062)
- **Dominant lineage:** european (2054 rows)
- **Dominant period:** modern (1539 rows)
- **Dominant register:** historical (2062 rows)
- **Top weapon types:** rifle(8), spear(2)
- **Purity (cultural_lineage):** 0.9961

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 203 | Maltese Ring | european | modern | 1.0000 |
| 4373 | Seax of Beagnoth | european | medieval | 1.0000 |
| 5028 | M2 machine gun at Musee de l'Armée | european | modern | 1.0000 |

---

### Rank 4: Cluster 50 (N=1907)

- **Provisional description:** PROVISIONAL: european contemporary bow weapons (military_modern register; category; N=1907)
- **Dominant lineage:** european (1907 rows)
- **Dominant period:** contemporary (1907 rows)
- **Dominant register:** military_modern (1907 rows)
- **Top weapon types:** bow(1)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 172751 | zweihänder | european | contemporary | 1.0000 |
| 172752 | zweihänder | european | contemporary | 1.0000 |
| 172810 | hardened steel kriegsmesser | european | contemporary | 1.0000 |

---

### Rank 5: Cluster 52 (N=1819)

- **Provisional description:** PROVISIONAL: fantasy_generic classical spear/musket weapons (fantasy register; named_template; N=1819)
- **Dominant lineage:** fantasy_generic (1811 rows)
- **Dominant period:** classical (1810 rows)
- **Dominant register:** fantasy (1819 rows)
- **Top weapon types:** spear(24), musket(12), mace(4)
- **Purity (cultural_lineage):** 0.9956

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13771 | Arrow of Teleportation | fantasy_generic | classical | 1.0000 |
| 13792 | Assassin's Arrow | fantasy_generic | classical | 1.0000 |
| 14484 | Chicken Chucker (Common) | fantasy_generic | classical | 1.0000 |

---

## Per-Lineage Cluster Disposition

| Lineage | Rows in pool | Rows in subsample | Clusters containing this lineage | Dominant cluster (if any) |
|---|---|---|---|---|
| fantasy_generic | 16284 | 3303 | 51 | Cluster 62 (4807 rows) |
| east_asian | 13080 | 2656 | 43 | Cluster 90 (10087 rows) |
| european | 12515 | 2542 | 73 | Cluster 112 (2054 rows) |
| unknown | 1956 | 411 | 35 | Cluster 119 (1177 rows) |
| middle_eastern | 1327 | 284 | 39 | Cluster 71 (414 rows) |
| cross_cultural | 883 | 194 | 13 | Cluster 68 (441 rows) |
| south_asian | 822 | 182 | 35 | Cluster 117 (118 rows) |
| southeast_asian | 694 | 156 | 28 | Cluster 116 (149 rows) |
| african | 465 | 110 | 31 | Cluster 115 (100 rows) |
| south_american_indigenous | 197 | 56 | 20 | Cluster 114 (47 rows) |
| mesoamerican | 83 | 33 | 16 | Cluster 111 (19 rows) |
| arctic_circumpolar | 56 | 27 | 8 | Cluster 23 (30 rows) |
| oceanic | 39 | 24 | 10 | Cluster 68 (21 rows) |
| north_american_indigenous | 29 | 22 | 15 | Cluster 69 (7 rows) |

## F6 Flags: Clusters with < 20 Members

These clusters are merge-candidates for Phase E-2 designer review (F6 lock):

- None. All clusters have ≥ 20 members.

## Full Cluster Roster

| Cluster ID | Member Count | Dominant Lineage | Dominant Period | Top Weapon Type | Purity |
|---|---|---|---|---|---|
| 0 | 46 | cross_cultural | contemporary | staff | 0.7391 |
| 1 | 105 | cross_cultural | contemporary | pistol | 0.9714 |
| 2 | 214 | fantasy_generic | fictional | axe | 1.0000 |
| 3 | 91 | european | contemporary | pistol | 0.5165 |
| 4 | 31 | fantasy_generic | fictional | club | 0.9355 |
| 5 | 77 | fantasy_generic | fictional | dagger | 0.9351 |
| 6 | 149 | fantasy_generic | fictional | wand | 1.0000 |
| 7 | 59 | fantasy_generic | fictional | pike | 1.0000 |
| 8 | 249 | fantasy_generic | fictional | axe | 1.0000 |
| 9 | 155 | fantasy_generic | classical | dagger | 0.8839 |
| 10 | 80 | fantasy_generic | fictional | javelin | 1.0000 |
| 11 | 76 | fantasy_generic | fictional | sword | 0.9211 |
| 12 | 266 | fantasy_generic | fictional | dagger | 1.0000 |
| 13 | 72 | fantasy_generic | classical | wand | 1.0000 |
| 14 | 83 | fantasy_generic | fictional | pistol | 1.0000 |
| 15 | 135 | fantasy_generic | fictional | knife | 1.0000 |
| 16 | 224 | fantasy_generic | fictional | sword | 1.0000 |
| 17 | 317 | fantasy_generic | fictional | sword | 1.0000 |
| 18 | 239 | fantasy_generic | fictional | sword | 1.0000 |
| 19 | 68 | east_asian | early_modern | sword | 0.9559 |
| 20 | 66 | european | industrial | sword | 0.7121 |
| 21 | 123 | cross_cultural | contemporary | sword | 0.9268 |
| 22 | 1256 | east_asian | contemporary | rifle | 0.9793 |
| 23 | 34 | arctic_circumpolar | contemporary | lance | 0.8824 |
| 24 | 361 | fantasy_generic | classical | pike | 0.9197 |
| 25 | 410 | fantasy_generic | fictional | sword | 0.9829 |
| 26 | 244 | fantasy_generic | classical | staff | 1.0000 |
| 27 | 1301 | fantasy_generic | fictional | spear | 0.9885 |
| 28 | 437 | fantasy_generic | fictional | staff | 1.0000 |
| 29 | 76 | fantasy_generic | classical | bow | 1.0000 |
| 30 | 77 | south_asian | contemporary | pistol | 0.6234 |
| 31 | 194 | southeast_asian | contemporary | rifle | 0.5155 |
| 32 | 121 | cross_cultural | contemporary | rifle | 0.9752 |
| 33 | 54 | fantasy_generic | fictional | sword | 0.9444 |
| 34 | 468 | fantasy_generic | fictional | bow | 1.0000 |
| 35 | 152 | fantasy_generic | fictional | halberd | 1.0000 |
| 36 | 115 | fantasy_generic | fictional | glaive | 1.0000 |
| 37 | 133 | fantasy_generic | fictional | staff | 1.0000 |
| 38 | 349 | fantasy_generic | fictional | hammer | 1.0000 |
| 39 | 143 | fantasy_generic | fictional | pike | 1.0000 |
| 40 | 237 | fantasy_generic | fictional | scimitar | 1.0000 |
| 41 | 342 | fantasy_generic | fictional | bow | 0.9825 |
| 42 | 434 | fantasy_generic | fictional | axe | 1.0000 |
| 43 | 114 | fantasy_generic | fictional | lance | 1.0000 |
| 44 | 72 | african | contemporary | pike | 0.6806 |
| 45 | 110 | fantasy_generic | fictional | flail | 1.0000 |
| 46 | 223 | fantasy_generic | fictional | rapier | 1.0000 |
| 47 | 107 | european | fictional | scimitar | 0.5140 |
| 48 | 68 | fantasy_generic | classical | rifle | 0.9265 |
| 49 | 68 | fantasy_generic | fictional | rifle | 0.9853 |
| 50 | 1907 | european | contemporary | bow | 1.0000 |
| 51 | 75 | fantasy_generic | classical | mace | 0.9867 |
| 52 | 1819 | fantasy_generic | classical | spear | 0.9956 |
| 53 | 161 | fantasy_generic | fictional | bow | 1.0000 |
| 54 | 85 | fantasy_generic | fictional | axe | 1.0000 |
| 55 | 65 | fantasy_generic | classical | sword | 0.8462 |
| 56 | 117 | fantasy_generic | classical | axe | 0.9829 |
| 57 | 160 | fantasy_generic | fictional | mace | 1.0000 |
| 58 | 76 | east_asian | industrial | pistol | 0.5132 |
| 59 | 129 | fantasy_generic | classical | hammer | 0.9147 |
| 60 | 127 | fantasy_generic | classical | bow | 0.9921 |
| 61 | 272 | fantasy_generic | fictional | spear | 0.9926 |
| 62 | 4807 | fantasy_generic | fictional | axe | 1.0000 |
| 63 | 187 | european | industrial | sword | 0.8396 |
| 64 | 59 | fantasy_generic | fictional | musket | 0.8814 |
| 65 | 232 | fantasy_generic | fictional | club | 1.0000 |
| 66 | 103 | unknown | unknown | pistol | 0.4078 |
| 67 | 238 | european | modern | sword | 0.5966 |
| 68 | 502 | cross_cultural | contemporary | shotgun | 0.8785 |
| 69 | 77 | european | contemporary | rifle | 0.7792 |
| 70 | 77 | european | contemporary | lance | 0.5584 |
| 71 | 423 | middle_eastern | contemporary | club | 0.9787 |
| 72 | 327 | european | industrial | pistol | 0.7645 |
| 73 | 315 | european | early_modern | pistol | 0.8857 |
| 74 | 115 | southeast_asian | early_modern | dagger | 0.3043 |
| 75 | 76 | south_asian | early_modern | dagger | 0.7500 |
| 76 | 183 | european | early_modern | sword | 0.7705 |
| 77 | 65 | unknown | unknown | pistol | 0.6462 |
| 78 | 311 | european | early_modern | pistol | 0.9518 |
| 79 | 116 | european | modern | pistol | 0.9569 |
| 80 | 192 | southeast_asian | early_modern | knife | 0.6302 |
| 81 | 250 | east_asian | contemporary | rifle | 0.9720 |
| 82 | 104 | southeast_asian | contemporary | rifle | 0.5288 |
| 83 | 33 | south_asian | contemporary | sword | 0.6667 |
| 84 | 734 | european | contemporary | spear | 1.0000 |
| 85 | 44 | african | contemporary | musket | 0.8864 |
| 86 | 36 | south_american_indigenous | contemporary | shotgun | 0.9444 |
| 87 | 190 | unknown | contemporary | shotgun | 0.8105 |
| 88 | 63 | european | contemporary | rifle | 0.9365 |
| 89 | 211 | middle_eastern | contemporary | spear | 0.8957 |
| 90 | 10087 | east_asian | unknown | rifle | 1.0000 |
| 91 | 161 | south_asian | early_modern | sword | 0.5280 |
| 92 | 92 | unknown | early_modern | lance | 0.5435 |
| 93 | 380 | east_asian | early_modern | musket | 0.8000 |
| 94 | 164 | european | early_modern | rifle | 0.6463 |
| 95 | 1305 | european | early_modern | spear | 0.9985 |
| 96 | 187 | european | early_modern | bow | 0.5936 |
| 97 | 218 | east_asian | classical | sword | 0.9862 |
| 98 | 107 | south_asian | industrial | spear | 0.5981 |
| 99 | 82 | european | early_modern | musket | 0.9146 |
| 100 | 144 | african | classical | bow | 0.4861 |
| 101 | 64 | unknown | industrial | lance | 0.5156 |
| 102 | 56 | european | industrial | shotgun | 0.9107 |
| 103 | 95 | african | unknown | mace | 0.9474 |
| 104 | 491 | east_asian | modern | rifle | 0.9104 |
| 105 | 218 | european | classical | sword | 0.3028 |
| 106 | 984 | european | classical | bow | 0.9817 |
| 107 | 337 | european | industrial | rifle | 0.8309 |
| 108 | 112 | unknown | classical | lance | 0.3929 |
| 109 | 159 | middle_eastern | classical | halberd | 0.7107 |
| 110 | 191 | east_asian | industrial | spear | 0.9162 |
| 111 | 115 | european | modern | shotgun | 0.3565 |
| 112 | 2062 | european | modern | rifle | 0.9961 |
| 113 | 257 | middle_eastern | unknown | spear | 0.6654 |
| 114 | 95 | south_american_indigenous | modern | rifle | 0.4947 |
| 115 | 1335 | european | unknown | spear | 0.9251 |
| 116 | 151 | southeast_asian | unknown | sabre | 0.9868 |
| 117 | 127 | south_asian | unknown | musket | 0.9291 |
| 118 | 1262 | european | industrial | spear | 0.9699 |
| 119 | 1205 | unknown | unknown | rifle | 0.9768 |
| 120 | 115 | southeast_asian | modern | musket | 0.6957 |
| 121 | 65 | african | industrial | sword | 0.6462 |
| 122 | 133 | european | modern | rifle | 0.9023 |
| 123 | 130 | middle_eastern | modern | spear | 0.9692 |
| 124 | 56 | middle_eastern | medieval | rifle | 0.6786 |
