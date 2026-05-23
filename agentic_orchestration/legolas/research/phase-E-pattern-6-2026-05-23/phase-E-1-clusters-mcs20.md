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
| HDBSCAN clusters (final) | 85 |
| HDBSCAN min_cluster_size | 20 |
| HDBSCAN training subsample N | 10000 |
| Subsample rows (hdbscan_native) | 10000 |
| Non-subsample rows (nearest_centroid) | 38430 |
| Originally-noise rows within subsample (confidence < 0.5) | 8072 |
| F6 flag: clusters < 20 members | 0 |
| Mean cluster purity (cultural_lineage, all rows) | 0.9287 (92.87%) |
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

### Rank 1: Cluster 54 (N=10087)

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

### Rank 2: Cluster 34 (N=4807)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional mixed weapons (fantasy register; named_template; N=4807)
- **Dominant lineage:** fantasy_generic (4807 rows)
- **Dominant period:** fictional (4806 rows)
- **Dominant register:** fantasy (4807 rows)
- **Top weapon types:** axe(12), greataxe(10), sabre(2)
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

### Rank 3: Cluster 16 (N=2122)

- **Provisional description:** PROVISIONAL: fantasy_generic classical club weapons (fantasy register; named_template; N=2122)
- **Dominant lineage:** fantasy_generic (2049 rows)
- **Dominant period:** classical (1946 rows)
- **Dominant register:** fantasy (2122 rows)
- **Top weapon types:** mace(62), sword(59), rifle(44)
- **Purity (cultural_lineage):** 0.9656

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13771 | Arrow of Teleportation | fantasy_generic | classical | 1.0000 |
| 13792 | Assassin's Arrow | fantasy_generic | classical | 1.0000 |
| 13944 | Birchwood Club (Rare) | fantasy_generic | classical | 1.0000 |
| 13976 | Blade of Broken Mirrors | fantasy_generic | classical | 1.0000 |
| 14040 | Blood Rime (Legendary) | arctic_circumpolar | fictional | 1.0000 |

---

### Rank 4: Cluster 71 (N=2063)

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

### Rank 5: Cluster 43 (N=1918)

- **Provisional description:** PROVISIONAL: european contemporary mixed weapons (military_modern register; category; N=1918)
- **Dominant lineage:** european (1911 rows)
- **Dominant period:** contemporary (1918 rows)
- **Dominant register:** military_modern (1918 rows)
- **Top weapon types:** rifle(7), bow(3), crossbow(2)
- **Purity (cultural_lineage):** 0.9964

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 172746 | mild steel zweihänder | european | contemporary | 1.0000 |
| 172806 | kriegsmesser | european | contemporary | 1.0000 |
| 172807 | mild steel kriegsmesser | european | contemporary | 1.0000 |
| 172822 | Enfield No. 4 bayonet | european | contemporary | 1.0000 |
| 182726 | DroneHunter F700 Ukrainian Unmanned Aerial Vehicle | european | contemporary | 1.0000 |

---

## Per-Lineage Cluster Disposition

| Lineage | Rows in pool | Rows in subsample | Clusters containing this lineage | Dominant cluster (if any) |
|---|---|---|---|---|
| fantasy_generic | 16284 | 3248 | 33 | Cluster 34 (4807 rows) |
| east_asian | 13080 | 2614 | 35 | Cluster 54 (10087 rows) |
| european | 12515 | 2503 | 57 | Cluster 71 (2054 rows) |
| unknown | 1956 | 418 | 30 | Cluster 80 (1181 rows) |
| middle_eastern | 1327 | 294 | 30 | Cluster 44 (414 rows) |
| cross_cultural | 883 | 206 | 9 | Cluster 42 (479 rows) |
| south_asian | 822 | 194 | 26 | Cluster 73 (118 rows) |
| southeast_asian | 694 | 169 | 27 | Cluster 72 (149 rows) |
| african | 465 | 124 | 25 | Cluster 84 (100 rows) |
| south_american_indigenous | 197 | 71 | 19 | Cluster 83 (47 rows) |
| mesoamerican | 83 | 48 | 15 | Cluster 70 (19 rows) |
| arctic_circumpolar | 56 | 43 | 9 | Cluster 37 (30 rows) |
| oceanic | 39 | 39 | 9 | Cluster 42 (21 rows) |
| north_american_indigenous | 29 | 29 | 13 | Cluster 44 (7 rows) |

## F6 Flags: Clusters with < 20 Members

These clusters are merge-candidates for Phase E-2 designer review (F6 lock):

- None. All clusters have ≥ 20 members.

## Full Cluster Roster

| Cluster ID | Member Count | Dominant Lineage | Dominant Period | Top Weapon Type | Purity |
|---|---|---|---|---|---|
| 0 | 214 | fantasy_generic | fictional | axe | 1.0000 |
| 1 | 313 | fantasy_generic | fictional | axe | 0.9681 |
| 2 | 238 | fantasy_generic | fictional | dagger | 0.9412 |
| 3 | 166 | fantasy_generic | fictional | wand | 1.0000 |
| 4 | 145 | cross_cultural | contemporary | pistol | 0.9034 |
| 5 | 182 | fantasy_generic | fictional | lance | 0.9945 |
| 6 | 267 | fantasy_generic | fictional | dagger | 1.0000 |
| 7 | 371 | fantasy_generic | fictional | knife | 1.0000 |
| 8 | 224 | fantasy_generic | fictional | sword | 1.0000 |
| 9 | 317 | fantasy_generic | fictional | sword | 1.0000 |
| 10 | 239 | fantasy_generic | fictional | sword | 1.0000 |
| 11 | 365 | fantasy_generic | classical | pike | 0.9123 |
| 12 | 407 | fantasy_generic | fictional | sword | 0.9828 |
| 13 | 237 | fantasy_generic | fictional | scimitar | 1.0000 |
| 14 | 342 | fantasy_generic | fictional | bow | 0.9825 |
| 15 | 437 | fantasy_generic | fictional | staff | 1.0000 |
| 16 | 2122 | fantasy_generic | classical | mace | 0.9656 |
| 17 | 333 | fantasy_generic | fictional | rapier | 1.0000 |
| 18 | 434 | fantasy_generic | fictional | axe | 1.0000 |
| 19 | 143 | fantasy_generic | fictional | pike | 1.0000 |
| 20 | 353 | fantasy_generic | fictional | hammer | 1.0000 |
| 21 | 467 | fantasy_generic | fictional | bow | 1.0000 |
| 22 | 116 | fantasy_generic | classical | axe | 0.9914 |
| 23 | 244 | fantasy_generic | classical | staff | 1.0000 |
| 24 | 307 | fantasy_generic | classical | bow | 0.9283 |
| 25 | 115 | fantasy_generic | fictional | glaive | 1.0000 |
| 26 | 152 | fantasy_generic | fictional | halberd | 1.0000 |
| 27 | 1300 | fantasy_generic | fictional | spear | 0.9892 |
| 28 | 109 | european | contemporary | pistol | 0.4679 |
| 29 | 252 | fantasy_generic | fictional | bow | 0.9921 |
| 30 | 216 | fantasy_generic | fictional | staff | 0.9769 |
| 31 | 366 | fantasy_generic | fictional | club | 0.9781 |
| 32 | 163 | fantasy_generic | fictional | mace | 1.0000 |
| 33 | 271 | fantasy_generic | fictional | spear | 0.9963 |
| 34 | 4807 | fantasy_generic | fictional | axe | 1.0000 |
| 35 | 1255 | east_asian | contemporary | rifle | 0.9793 |
| 36 | 167 | european | early_modern | bow | 0.6826 |
| 37 | 158 | cross_cultural | contemporary | rifle | 0.7468 |
| 38 | 99 | south_asian | contemporary | sword | 0.3636 |
| 39 | 206 | south_asian | contemporary | rifle | 0.5146 |
| 40 | 329 | european | modern | sword | 0.5046 |
| 41 | 74 | african | contemporary | rifle | 0.6757 |
| 42 | 557 | cross_cultural | contemporary | lance | 0.8600 |
| 43 | 1918 | european | contemporary | rifle | 0.9964 |
| 44 | 597 | middle_eastern | contemporary | rifle | 0.6935 |
| 45 | 197 | european | early_modern | sword | 0.7259 |
| 46 | 518 | european | early_modern | pistol | 0.6216 |
| 47 | 137 | south_asian | contemporary | sword | 0.5182 |
| 48 | 297 | european | industrial | sword | 0.6364 |
| 49 | 425 | european | early_modern | sword | 0.7365 |
| 50 | 329 | european | industrial | pistol | 0.7538 |
| 51 | 330 | european | early_modern | pistol | 0.4030 |
| 52 | 77 | african | contemporary | shotgun | 0.5065 |
| 53 | 742 | european | contemporary | spear | 0.9933 |
| 54 | 10087 | east_asian | unknown | rifle | 1.0000 |
| 55 | 265 | middle_eastern | contemporary | rifle | 0.7132 |
| 56 | 195 | unknown | contemporary | shotgun | 0.8154 |
| 57 | 386 | east_asian | early_modern | musket | 0.8135 |
| 58 | 257 | east_asian | contemporary | rifle | 0.9455 |
| 59 | 158 | south_asian | early_modern | sword | 0.5380 |
| 60 | 219 | east_asian | classical | sword | 0.9817 |
| 61 | 238 | european | early_modern | rifle | 0.6008 |
| 62 | 1314 | european | early_modern | sabre | 0.9916 |
| 63 | 204 | european | early_modern | musket | 0.4118 |
| 64 | 122 | european | industrial | shotgun | 0.5000 |
| 65 | 95 | african | unknown | mace | 0.9474 |
| 66 | 491 | east_asian | modern | rifle | 0.9104 |
| 67 | 336 | european | industrial | rifle | 0.8333 |
| 68 | 207 | european | classical | sword | 0.2899 |
| 69 | 995 | european | classical | bow | 0.9749 |
| 70 | 143 | european | modern | shotgun | 0.3357 |
| 71 | 2063 | european | modern | rifle | 0.9956 |
| 72 | 152 | southeast_asian | unknown | musket | 0.9803 |
| 73 | 148 | south_asian | unknown | sword | 0.7973 |
| 74 | 148 | southeast_asian | modern | musket | 0.5405 |
| 75 | 1281 | european | industrial | rifle | 0.9555 |
| 76 | 139 | african | classical | bow | 0.4964 |
| 77 | 250 | middle_eastern | classical | hammer | 0.4640 |
| 78 | 200 | east_asian | industrial | sword | 0.9250 |
| 79 | 242 | middle_eastern | unknown | spear | 0.7066 |
| 80 | 1209 | unknown | unknown | rifle | 0.9768 |
| 81 | 130 | european | modern | rifle | 0.9231 |
| 82 | 169 | middle_eastern | modern | spear | 0.9763 |
| 83 | 106 | south_american_indigenous | unknown | rifle | 0.4434 |
| 84 | 1335 | european | unknown | spear | 0.9251 |
