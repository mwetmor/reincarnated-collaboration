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
| HDBSCAN clusters (final) | 65 |
| HDBSCAN min_cluster_size | 30 |
| HDBSCAN training subsample N | 10000 |
| Subsample rows (hdbscan_native) | 10000 |
| Non-subsample rows (nearest_centroid) | 38430 |
| Originally-noise rows within subsample (confidence < 0.5) | 8102 |
| F6 flag: clusters < 20 members | 0 |
| Mean cluster purity (cultural_lineage, all rows) | 0.9177 (91.77%) |
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

### Rank 1: Cluster 44 (N=10087)

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

### Rank 2: Cluster 29 (N=4992)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional mixed weapons (fantasy register; named_template; N=4992)
- **Dominant lineage:** fantasy_generic (4991 rows)
- **Dominant period:** fictional (4987 rows)
- **Dominant register:** fantasy (4992 rows)
- **Top weapon types:** lance(103), rifle(65), axe(15)
- **Purity (cultural_lineage):** 0.9998

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13478 | Abyssal Bane Chakram (very rare variant) | fantasy_generic | fictional | 1.0000 |
| 13514 | Abyssal Bane Knuckle Duster (very rare variant) | fantasy_generic | fictional | 1.0000 |
| 13528 | Abyssal Bane Maul (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13533 | Abyssal Bane Nunchaku | fantasy_generic | fictional | 1.0000 |
| 13534 | Abyssal Bane Nunchaku (rare variant) | fantasy_generic | fictional | 1.0000 |

---

### Rank 3: Cluster 9 (N=2097)

- **Provisional description:** PROVISIONAL: fantasy_generic classical club weapons (fantasy register; named_template; N=2097)
- **Dominant lineage:** fantasy_generic (2017 rows)
- **Dominant period:** classical (1946 rows)
- **Dominant register:** fantasy (2097 rows)
- **Top weapon types:** mace(62), rifle(46), spear(27)
- **Purity (cultural_lineage):** 0.9619

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13792 | Assassin's Arrow | fantasy_generic | classical | 1.0000 |
| 13944 | Birchwood Club (Rare) | fantasy_generic | classical | 1.0000 |
| 13976 | Blade of Broken Mirrors | fantasy_generic | classical | 1.0000 |
| 14040 | Blood Rime (Legendary) | arctic_circumpolar | fictional | 1.0000 |
| 14041 | Blood Rime (Rare) | arctic_circumpolar | fictional | 1.0000 |

---

### Rank 4: Cluster 30 (N=2068)

- **Provisional description:** PROVISIONAL: european contemporary mixed weapons (military_modern register; category; N=2068)
- **Dominant lineage:** european (1909 rows)
- **Dominant period:** contemporary (2067 rows)
- **Dominant register:** military_modern (2068 rows)
- **Top weapon types:** rifle(9), bow(3), musket(2)
- **Purity (cultural_lineage):** 0.9231

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 172751 | zweihänder | european | contemporary | 1.0000 |
| 172811 | tempered steel kriegsmesser | european | contemporary | 1.0000 |
| 172822 | Enfield No. 4 bayonet | european | contemporary | 1.0000 |
| 173470 | SIG Pro .40 | european | contemporary | 1.0000 |
| 182724 | Bebradrone Ukrainian Unmanned Aerial Vehicle (UAV) | european | contemporary | 1.0000 |

---

### Rank 5: Cluster 57 (N=2068)

- **Provisional description:** PROVISIONAL: european modern mixed weapons (historical register; category; N=2068)
- **Dominant lineage:** european (2054 rows)
- **Dominant period:** modern (1542 rows)
- **Dominant register:** historical (2068 rows)
- **Top weapon types:** rifle(13), spear(2), sabre(1)
- **Purity (cultural_lineage):** 0.9932

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 203 | Maltese Ring | european | modern | 1.0000 |
| 4373 | Seax of Beagnoth | european | medieval | 1.0000 |
| 5028 | M2 machine gun at Musee de l'Armée | european | modern | 1.0000 |
| 22774 | Rimfire self-loading magazine carbine | european | modern | 1.0000 |
| 22812 | Telescopic sight | european | modern | 1.0000 |

---

## Per-Lineage Cluster Disposition

| Lineage | Rows in pool | Rows in subsample | Clusters containing this lineage | Dominant cluster (if any) |
|---|---|---|---|---|
| fantasy_generic | 16284 | 3198 | 28 | Cluster 29 (4991 rows) |
| east_asian | 13080 | 2579 | 28 | Cluster 44 (10087 rows) |
| european | 12515 | 2470 | 43 | Cluster 57 (2054 rows) |
| unknown | 1956 | 427 | 23 | Cluster 60 (1177 rows) |
| middle_eastern | 1327 | 305 | 23 | Cluster 31 (414 rows) |
| cross_cultural | 883 | 219 | 8 | Cluster 32 (596 rows) |
| south_asian | 822 | 207 | 20 | Cluster 27 (141 rows) |
| southeast_asian | 694 | 183 | 22 | Cluster 59 (149 rows) |
| african | 465 | 138 | 25 | Cluster 56 (100 rows) |
| south_american_indigenous | 197 | 86 | 18 | Cluster 56 (40 rows) |
| mesoamerican | 83 | 64 | 12 | Cluster 47 (22 rows) |
| arctic_circumpolar | 56 | 56 | 7 | Cluster 32 (30 rows) |
| oceanic | 39 | 39 | 8 | Cluster 32 (22 rows) |
| north_american_indigenous | 29 | 29 | 12 | Cluster 30 (7 rows) |

## F6 Flags: Clusters with < 20 Members

These clusters are merge-candidates for Phase E-2 designer review (F6 lock):

- None. All clusters have ≥ 20 members.

## Full Cluster Roster

| Cluster ID | Member Count | Dominant Lineage | Dominant Period | Top Weapon Type | Purity |
|---|---|---|---|---|---|
| 0 | 214 | fantasy_generic | fictional | axe | 1.0000 |
| 1 | 312 | fantasy_generic | fictional | axe | 0.9936 |
| 2 | 256 | fantasy_generic | fictional | dagger | 0.9102 |
| 3 | 375 | fantasy_generic | fictional | knife | 1.0000 |
| 4 | 413 | fantasy_generic | fictional | dagger | 1.0000 |
| 5 | 317 | fantasy_generic | fictional | sword | 1.0000 |
| 6 | 224 | fantasy_generic | fictional | sword | 1.0000 |
| 7 | 239 | fantasy_generic | fictional | sword | 1.0000 |
| 8 | 362 | fantasy_generic | classical | bow | 0.9144 |
| 9 | 2097 | fantasy_generic | classical | mace | 0.9619 |
| 10 | 455 | fantasy_generic | fictional | staff | 0.9956 |
| 11 | 1303 | fantasy_generic | fictional | spear | 0.9893 |
| 12 | 355 | fantasy_generic | classical | staff | 1.0000 |
| 13 | 437 | fantasy_generic | fictional | staff | 1.0000 |
| 14 | 411 | fantasy_generic | fictional | sword | 0.9830 |
| 15 | 267 | fantasy_generic | fictional | halberd | 1.0000 |
| 16 | 464 | fantasy_generic | fictional | bow | 1.0000 |
| 17 | 143 | fantasy_generic | fictional | pike | 1.0000 |
| 18 | 353 | fantasy_generic | fictional | hammer | 1.0000 |
| 19 | 1258 | east_asian | contemporary | rifle | 0.9777 |
| 20 | 346 | fantasy_generic | classical | bow | 0.9393 |
| 21 | 333 | fantasy_generic | fictional | rapier | 1.0000 |
| 22 | 434 | fantasy_generic | fictional | axe | 1.0000 |
| 23 | 237 | fantasy_generic | fictional | scimitar | 1.0000 |
| 24 | 342 | fantasy_generic | fictional | bow | 0.9825 |
| 25 | 365 | fantasy_generic | fictional | club | 0.9781 |
| 26 | 163 | fantasy_generic | fictional | mace | 1.0000 |
| 27 | 260 | south_asian | contemporary | pistol | 0.5423 |
| 28 | 271 | fantasy_generic | fictional | spear | 0.9963 |
| 29 | 4992 | fantasy_generic | fictional | lance | 0.9998 |
| 30 | 2068 | european | contemporary | rifle | 0.9231 |
| 31 | 623 | middle_eastern | contemporary | rifle | 0.6645 |
| 32 | 695 | cross_cultural | contemporary | rifle | 0.8576 |
| 33 | 525 | european | early_modern | pistol | 0.6133 |
| 34 | 618 | european | industrial | sword | 0.5566 |
| 35 | 288 | cross_cultural | contemporary | pistol | 0.3750 |
| 36 | 697 | european | early_modern | pistol | 0.6370 |
| 37 | 510 | european | early_modern | sword | 0.7020 |
| 38 | 257 | east_asian | contemporary | rifle | 0.9533 |
| 39 | 138 | south_asian | contemporary | sword | 0.5145 |
| 40 | 811 | european | contemporary | spear | 0.9100 |
| 41 | 193 | unknown | contemporary | shotgun | 0.8135 |
| 42 | 268 | middle_eastern | contemporary | rifle | 0.7052 |
| 43 | 367 | east_asian | early_modern | musket | 0.7902 |
| 44 | 10087 | east_asian | unknown | rifle | 1.0000 |
| 45 | 247 | european | early_modern | bow | 0.5870 |
| 46 | 246 | east_asian | classical | halberd | 0.9472 |
| 47 | 147 | european | modern | shotgun | 0.3333 |
| 48 | 95 | african | unknown | mace | 0.9474 |
| 49 | 491 | east_asian | modern | rifle | 0.9104 |
| 50 | 317 | european | early_modern | rifle | 0.4511 |
| 51 | 1588 | european | early_modern | musket | 0.8974 |
| 52 | 1161 | european | classical | sword | 0.8389 |
| 53 | 457 | european | industrial | rifle | 0.7309 |
| 54 | 271 | middle_eastern | classical | hammer | 0.4391 |
| 55 | 197 | east_asian | industrial | sword | 0.9137 |
| 56 | 1408 | european | unknown | rifle | 0.8771 |
| 57 | 2068 | european | modern | rifle | 0.9932 |
| 58 | 306 | middle_eastern | unknown | rifle | 0.5588 |
| 59 | 150 | southeast_asian | unknown | sabre | 0.9933 |
| 60 | 1210 | unknown | unknown | rifle | 0.9727 |
| 61 | 300 | middle_eastern | modern | rifle | 0.5467 |
| 62 | 149 | south_asian | unknown | sword | 0.7919 |
| 63 | 148 | southeast_asian | modern | musket | 0.5405 |
| 64 | 1331 | european | industrial | sword | 0.9256 |
