# Phase E-1 — Deliverable 3: Clustering Output

PROVISIONAL — gandalf labels clusters canonically in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Status:** Complete

---

## Summary

| Metric | Value |
|---|---|
| Total rows clustered | 100 |
| HDBSCAN clusters (final) | 8 |
| HDBSCAN min_cluster_size | 30 |
| Originally-noise rows (confidence < 0.5) | 24 |
| F6 flag: clusters < 20 members | 6 |
| Mean cluster purity (cultural_lineage) | 1.0000 (100.00%) |
| Purity PASS (≥ 0.85) | YES |
| F2 inverse-frequency weighting applied | Yes |

---

## Method Comparison

| Method | N clusters |
|---|---|
| HDBSCAN (primary) | 8 |
| GMM baseline | 8 |
| k-means baseline | 8 |

---

## Top 5 Clusters by Member Count

### Rank 1: Cluster 6 (N=45)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional axe/battleaxe weapons (fantasy register; named_template; N=45)
- **Dominant lineage:** fantasy_generic (45 rows)
- **Dominant period:** fictional (45 rows)
- **Dominant register:** fantasy (45 rows)
- **Top weapon types:** axe(11), battleaxe(4), sword(4)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13476 | Abyssal Bane Chakram | fantasy_generic | fictional | 1.0000 |
| 13477 | Abyssal Bane Chakram (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13478 | Abyssal Bane Chakram (very rare variant) | fantasy_generic | fictional | 1.0000 |

---

### Rank 2: Cluster 7 (N=21)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional flail/glaive weapons (fantasy register; named_template; N=21)
- **Dominant lineage:** fantasy_generic (21 rows)
- **Dominant period:** fictional (21 rows)
- **Dominant register:** fantasy (21 rows)
- **Top weapon types:** flail(3), glaive(3), halberd(3)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13488 | Abyssal Bane Flail | fantasy_generic | fictional | 1.0000 |
| 13489 | Abyssal Bane Flail (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13490 | Abyssal Bane Flail (very rare variant) | fantasy_generic | fictional | 1.0000 |

---

### Rank 3: Cluster 2 (N=9)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional dagger/javelin weapons (fantasy register; named_template; N=9)
- **Dominant lineage:** fantasy_generic (9 rows)
- **Dominant period:** fictional (9 rows)
- **Dominant register:** fantasy (9 rows)
- **Top weapon types:** dagger(3), javelin(3), knife(3)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13485 | Abyssal Bane Dagger | fantasy_generic | fictional | 1.0000 |
| 13486 | Abyssal Bane Dagger (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13487 | Abyssal Bane Dagger (very rare variant) | fantasy_generic | fictional | 1.0000 |

---

### Rank 4: Cluster 5 (N=9)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional pike weapons (fantasy register; named_template; N=9)
- **Dominant lineage:** fantasy_generic (9 rows)
- **Dominant period:** fictional (9 rows)
- **Dominant register:** fantasy (9 rows)
- **Top weapon types:** pike(9)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13536 | Abyssal Bane Pike | fantasy_generic | fictional | 1.0000 |
| 13537 | Abyssal Bane Pike (rare variant) | fantasy_generic | fictional | 1.0000 |
| 13538 | Abyssal Bane Pike (very rare variant) | fantasy_generic | fictional | 1.0000 |

---

### Rank 5: Cluster 4 (N=7)

- **Provisional description:** PROVISIONAL: fantasy_generic fictional club weapons (fantasy register; named_template; N=7)
- **Dominant lineage:** fantasy_generic (7 rows)
- **Dominant period:** fictional (7 rows)
- **Dominant register:** fantasy (7 rows)
- **Top weapon types:** club(7)
- **Purity (cultural_lineage):** 1.0000

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
| 13469 | Abominable Club | fantasy_generic | fictional | 1.0000 |
| 13482 | Abyssal Bane Club | fantasy_generic | fictional | 1.0000 |
| 13483 | Abyssal Bane Club (rare variant) | fantasy_generic | fictional | 1.0000 |

---

## F6 Flags: Clusters with < 20 Members

These clusters require merging-or-split decision in Phase E-2 (per F6 lock):

- Cluster 0: N=1 — PROVISIONAL: middle_eastern unknown mixed weapons (historical register; category; N=1)
- Cluster 1: N=2 — PROVISIONAL: unknown unknown mixed weapons (historical register; named_template; N=2)
- Cluster 2: N=9 — PROVISIONAL: fantasy_generic fictional dagger/javelin weapons (fantasy register; named_template; N=9)
- Cluster 3: N=6 — PROVISIONAL: fantasy_generic fictional sword/greatsword weapons (fantasy register; named_template; N=6)
- Cluster 4: N=7 — PROVISIONAL: fantasy_generic fictional club weapons (fantasy register; named_template; N=7)
- Cluster 5: N=9 — PROVISIONAL: fantasy_generic fictional pike weapons (fantasy register; named_template; N=9)

## Full Cluster Roster

| Cluster ID | Member Count | Dominant Lineage | Dominant Period | Top Weapon Type | Purity |
|---|---|---|---|---|---|
| 0 | 1 | middle_eastern | unknown | mixed | 1.0000 |
| 1 | 2 | unknown | unknown | mixed | 1.0000 |
| 2 | 9 | fantasy_generic | fictional | dagger | 1.0000 |
| 3 | 6 | fantasy_generic | fictional | sword | 1.0000 |
| 4 | 7 | fantasy_generic | fictional | club | 1.0000 |
| 5 | 9 | fantasy_generic | fictional | pike | 1.0000 |
| 6 | 45 | fantasy_generic | fictional | axe | 1.0000 |
| 7 | 21 | fantasy_generic | fictional | flail | 1.0000 |
