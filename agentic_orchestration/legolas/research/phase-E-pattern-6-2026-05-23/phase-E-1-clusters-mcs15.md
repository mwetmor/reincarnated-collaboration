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
| HDBSCAN clusters (final) | 103 |
| HDBSCAN min_cluster_size | 15 |
| HDBSCAN training subsample N | 10000 |
| Subsample rows (hdbscan_native) | 10000 |
| Non-subsample rows (nearest_centroid) | 38430 |
| Originally-noise rows within subsample (confidence < 0.5) | 8070 |
| F6 flag: clusters < 20 members | 0 |
| Mean cluster purity (cultural_lineage, all rows) | 0.9412 (94.12%) |
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

### Rank 1: Cluster 71 (N=10087)

- **Provisional description:** PROVISIONAL: east_asian unknown mixed weapons (historical register; category; N=10087)
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
| 1017 | Q132526367 | east_asian | unknown | 1.0000 |
| 1018 | Q132526368 | east_asian | unknown | 1.0000 |

---

### Rank 2: Cluster 40 (N=4807)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional mixed weapons (fantasy register; named_template; N=4807)
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
| 13528 | Abyssal Bane Maul (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13533 | Abyssal Bane Nunchaku | fantasy_generic | fictional | 1.0000 |

---

### Rank 3: Cluster 89 (N=2063)

- **Provisional description:** PROVISIONAL: european modern mixed weapons (historical register; category; N=2063)
- **Dominant lineage:** european (2054 rows)
- **Dominant period:** modern (1539 rows)
- **Dominant register:** historical (2063 rows)
- **Top weapon types:** rifle(8), spear(2)
- **Purity (cultural_lineage):** 0.9956

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 203 | Maltese Ring | european | modern | 1.0000 |
| 4373 | Seax of Beagnoth | european | medieval | 1.0000 |
| 5028 | M2 machine gun at Musee de l'Armée | european | modern | 1.0000 |
| 22774 | Rimfire self-loading magazine carbine | european | modern | 1.0000 |
| 22812 | Telescopic sight | european | modern | 1.0000 |

---

### Rank 4: Cluster 43 (N=1959)

- **Provisional description:** PROVISIONAL: fantasy_generic classical mixed weapons (fantasy register; named_template; N=1959)
- **Dominant lineage:** fantasy_generic (1948 rows)
- **Dominant period:** classical (1934 rows)
- **Dominant register:** fantasy (1959 rows)
- **Top weapon types:** mace(61), rifle(44), spear(24)
- **Purity (cultural_lineage):** 0.9944

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13771 | Arrow of Teleportation | fantasy_generic | classical | 1.0000 |
| 13792 | Assassin's Arrow | fantasy_generic | classical | 1.0000 |
| 14484 | Chicken Chucker (Common) | fantasy_generic | classical | 1.0000 |
| 14485 | Chicken Chucker (Legendary) | fantasy_generic | classical | 1.0000 |
| 14486 | Chicken Chucker (Rare) | fantasy_generic | classical | 1.0000 |

---

### Rank 5: Cluster 56 (N=1921)

- **Provisional description:** PROVISIONAL: european contemporary mixed weapons (military_modern register; category; N=1921)
- **Dominant lineage:** european (1907 rows)
- **Dominant period:** contemporary (1921 rows)
- **Dominant register:** military_modern (1921 rows)
- **Top weapon types:** rifle(7), bow(1)
- **Purity (cultural_lineage):** 0.9927

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 172746 | mild steel zweihänder | european | contemporary | 1.0000 |
| 172806 | kriegsmesser | european | contemporary | 1.0000 |
| 172807 | mild steel kriegsmesser | european | contemporary | 1.0000 |
| 172822 | Enfield No. 4 bayonet | european | contemporary | 1.0000 |
| 173397 | Bren 5.56x45mm carbine | european | contemporary | 1.0000 |

---

## Per-Lineage Cluster Disposition

| Lineage | Rows in pool | Rows in subsample | Clusters containing this lineage | Dominant cluster (if any) |
|---|---|---|---|---|
| fantasy_generic | 16284 | 3274 | 41 | Cluster 40 (4807 rows) |
| east_asian | 13080 | 2634 | 40 | Cluster 71 (10087 rows) |
| european | 12515 | 2521 | 64 | Cluster 89 (2054 rows) |
| unknown | 1956 | 414 | 34 | Cluster 96 (1183 rows) |
| middle_eastern | 1327 | 289 | 36 | Cluster 61 (414 rows) |
| cross_cultural | 883 | 200 | 10 | Cluster 62 (441 rows) |
| south_asian | 822 | 188 | 29 | Cluster 51 (140 rows) |
| southeast_asian | 694 | 163 | 26 | Cluster 91 (149 rows) |
| african | 465 | 117 | 29 | Cluster 102 (100 rows) |
| south_american_indigenous | 197 | 63 | 21 | Cluster 100 (47 rows) |
| mesoamerican | 83 | 41 | 15 | Cluster 88 (19 rows) |
| arctic_circumpolar | 56 | 35 | 7 | Cluster 48 (30 rows) |
| oceanic | 39 | 32 | 9 | Cluster 62 (21 rows) |
| north_american_indigenous | 29 | 29 | 15 | Cluster 56 (7 rows) |

## F6 Flags: Clusters with < 20 Members

These clusters are merge-candidates for Phase E-2 designer review (F6 lock):

- None. All clusters have ≥ 20 members.

## Full Cluster Roster

| Cluster ID | Member Count | Dominant Lineage | Dominant Period | Top Weapon Type | Purity |
|---|---|---|---|---|---|
| 0 | 214 | fantasy_generic | fictional | axe | 1.0000 |
| 1 | 94 | fantasy_generic | fictional | dagger | 0.9255 |
| 2 | 143 | fantasy_generic | classical | dagger | 0.9441 |
| 3 | 279 | fantasy_generic | fictional | axe | 0.9642 |
| 4 | 239 | fantasy_generic | fictional | sword | 1.0000 |
| 5 | 148 | fantasy_generic | fictional | wand | 1.0000 |
| 6 | 145 | cross_cultural | contemporary | pistol | 0.9034 |
| 7 | 226 | fantasy_generic | fictional | sword | 1.0000 |
| 8 | 317 | fantasy_generic | fictional | sword | 1.0000 |
| 9 | 131 | fantasy_generic | fictional | javelin | 1.0000 |
| 10 | 267 | fantasy_generic | fictional | dagger | 1.0000 |
| 11 | 292 | fantasy_generic | fictional | knife | 1.0000 |
| 12 | 367 | fantasy_generic | classical | staff | 0.9973 |
| 13 | 388 | fantasy_generic | classical | hammer | 0.9175 |
| 14 | 1274 | fantasy_generic | fictional | spear | 0.9906 |
| 15 | 76 | fantasy_generic | classical | bow | 1.0000 |
| 16 | 55 | fantasy_generic | fictional | sword | 0.9455 |
| 17 | 437 | fantasy_generic | fictional | staff | 1.0000 |
| 18 | 98 | european | contemporary | pistol | 0.4898 |
| 19 | 149 | fantasy_generic | fictional | staff | 0.9597 |
| 20 | 465 | fantasy_generic | fictional | bow | 1.0000 |
| 21 | 115 | fantasy_generic | fictional | glaive | 1.0000 |
| 22 | 152 | fantasy_generic | fictional | halberd | 1.0000 |
| 23 | 237 | fantasy_generic | fictional | scimitar | 1.0000 |
| 24 | 342 | fantasy_generic | fictional | bow | 0.9825 |
| 25 | 143 | fantasy_generic | fictional | pike | 1.0000 |
| 26 | 410 | fantasy_generic | fictional | sword | 0.9829 |
| 27 | 352 | fantasy_generic | fictional | hammer | 1.0000 |
| 28 | 434 | fantasy_generic | fictional | axe | 1.0000 |
| 29 | 160 | fantasy_generic | fictional | bow | 1.0000 |
| 30 | 87 | fantasy_generic | fictional | axe | 1.0000 |
| 31 | 110 | fantasy_generic | fictional | flail | 1.0000 |
| 32 | 223 | fantasy_generic | fictional | rapier | 1.0000 |
| 33 | 131 | fantasy_generic | classical | hammer | 0.8855 |
| 34 | 175 | fantasy_generic | classical | bow | 0.9714 |
| 35 | 114 | fantasy_generic | fictional | lance | 1.0000 |
| 36 | 68 | fantasy_generic | fictional | rifle | 0.9853 |
| 37 | 294 | fantasy_generic | fictional | club | 0.9728 |
| 38 | 160 | fantasy_generic | fictional | mace | 1.0000 |
| 39 | 271 | fantasy_generic | fictional | spear | 0.9963 |
| 40 | 4807 | fantasy_generic | fictional | axe | 1.0000 |
| 41 | 101 | cross_cultural | contemporary | bow | 0.9109 |
| 42 | 175 | fantasy_generic | fictional | sword | 0.6400 |
| 43 | 1959 | fantasy_generic | classical | mace | 0.9944 |
| 44 | 192 | unknown | contemporary | shotgun | 0.8125 |
| 45 | 1255 | east_asian | contemporary | rifle | 0.9793 |
| 46 | 137 | south_asian | contemporary | sword | 0.5182 |
| 47 | 76 | african | contemporary | shotgun | 0.5132 |
| 48 | 34 | arctic_circumpolar | contemporary | lance | 0.8824 |
| 49 | 739 | european | contemporary | spear | 0.9946 |
| 50 | 269 | middle_eastern | contemporary | rifle | 0.7026 |
| 51 | 192 | south_asian | contemporary | pistol | 0.7292 |
| 52 | 102 | southeast_asian | contemporary | rifle | 0.9804 |
| 53 | 120 | cross_cultural | contemporary | rifle | 0.9833 |
| 54 | 74 | african | contemporary | rifle | 0.6757 |
| 55 | 220 | european | modern | sword | 0.6545 |
| 56 | 1921 | european | contemporary | rifle | 0.9927 |
| 57 | 190 | european | early_modern | bow | 0.6105 |
| 58 | 221 | european | industrial | sword | 0.7692 |
| 59 | 109 | unknown | contemporary | pistol | 0.4771 |
| 60 | 171 | east_asian | early_modern | sword | 0.5673 |
| 61 | 557 | middle_eastern | contemporary | rifle | 0.7433 |
| 62 | 508 | cross_cultural | contemporary | shotgun | 0.8681 |
| 63 | 162 | european | early_modern | sword | 0.8827 |
| 64 | 86 | east_asian | industrial | dagger | 0.3023 |
| 65 | 279 | european | industrial | pistol | 0.8100 |
| 66 | 318 | european | early_modern | pistol | 0.8616 |
| 67 | 197 | south_asian | early_modern | dagger | 0.4365 |
| 68 | 331 | european | early_modern | pistol | 0.8973 |
| 69 | 158 | european | modern | pistol | 0.7152 |
| 70 | 184 | southeast_asian | early_modern | knife | 0.6630 |
| 71 | 10087 | east_asian | unknown | rifle | 1.0000 |
| 72 | 110 | south_asian | industrial | spear | 0.6273 |
| 73 | 147 | south_asian | early_modern | sword | 0.5714 |
| 74 | 250 | east_asian | contemporary | rifle | 0.9720 |
| 75 | 394 | east_asian | early_modern | musket | 0.7995 |
| 76 | 238 | european | early_modern | rifle | 0.5882 |
| 77 | 1388 | european | early_modern | musket | 0.9971 |
| 78 | 213 | east_asian | classical | sword | 0.9859 |
| 79 | 137 | african | classical | halberd | 0.5109 |
| 80 | 95 | african | unknown | mace | 0.9474 |
| 81 | 156 | east_asian | medieval | rifle | 0.7179 |
| 82 | 339 | east_asian | modern | spear | 1.0000 |
| 83 | 118 | european | industrial | shotgun | 0.4915 |
| 84 | 204 | european | classical | sword | 0.3676 |
| 85 | 1007 | european | classical | sword | 0.9563 |
| 86 | 108 | unknown | classical | lance | 0.3519 |
| 87 | 338 | european | industrial | rifle | 0.8314 |
| 88 | 115 | european | modern | shotgun | 0.3652 |
| 89 | 2063 | european | modern | rifle | 0.9956 |
| 90 | 165 | middle_eastern | classical | halberd | 0.6788 |
| 91 | 151 | southeast_asian | unknown | musket | 0.9868 |
| 92 | 169 | south_asian | unknown | sword | 0.6982 |
| 93 | 201 | east_asian | industrial | sword | 0.9204 |
| 94 | 1273 | european | industrial | spear | 0.9615 |
| 95 | 126 | southeast_asian | modern | musket | 0.6349 |
| 96 | 1212 | unknown | unknown | rifle | 0.9761 |
| 97 | 185 | middle_eastern | modern | spear | 0.8919 |
| 98 | 133 | european | modern | rifle | 0.9023 |
| 99 | 264 | middle_eastern | unknown | rifle | 0.6477 |
| 100 | 66 | south_american_indigenous | modern | sabre | 0.7121 |
| 101 | 1235 | european | unknown | spear | 1.0000 |
| 102 | 117 | african | modern | rifle | 0.8547 |
