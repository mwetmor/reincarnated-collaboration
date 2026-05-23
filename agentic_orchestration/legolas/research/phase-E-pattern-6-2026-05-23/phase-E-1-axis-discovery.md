# Phase E-1 — Deliverable 2: Axis Discovery Output

PROVISIONAL — gandalf reviews and canonically labels axes in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Status:** Complete

---

## Summary

- **Axes retained:** 12
- **Cumulative variance explained (k=12):** 0.3934 (39.34%)
- **Method:** TruncatedSVD (weighted PCA via sqrt(F2-weight) row-multiplication)
- **F2 correction applied:** Yes (inverse-frequency cultural_lineage_canonical weights)
- **Bootstrap stability:** 10 resamples; per-axis mean cosine-distance reported below

---

## Per-Axis Results

### Axis 1

- **Variance explained:** 0.0789 (7.89%)
- **Provisional name:** PROVISIONAL: fantasy register axis
- **Bootstrap stability (mean cosine-dist):** 0.0011
- **Stability PASS (≤0.10):** YES
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| register_fantasy | +0.4262 |
| kind_category | -0.4172 |
| kind_named_template | +0.4172 |
| lineage_fantasy_generic | +0.4090 |
| period_fictional | +0.3944 |
| register_historical | -0.2050 |
| type_staff | +0.0949 |
| type_axe | +0.0848 |
| period_unknown | -0.0838 |
| lineage_unknown | -0.0751 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| register_fantasy | +0.4262 |
| kind_category | -0.4172 |
| kind_named_template | +0.4172 |
| lineage_fantasy_generic | +0.4090 |
| period_fictional | +0.3944 |

---

### Axis 2

- **Variance explained:** 0.0567 (5.67%)
- **Provisional name:** PROVISIONAL: register military modern dominant axis
- **Bootstrap stability (mean cosine-dist):** 0.0118
- **Stability PASS (≤0.10):** YES
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| register_military_modern | +0.4351 |
| period_contemporary | +0.4219 |
| register_historical | -0.3800 |
| wield_two_hand | +0.3358 |
| wield_one_hand | -0.3353 |
| period_early_modern | -0.2432 |
| type_dagger | -0.1707 |
| lineage_arctic_circumpolar | +0.1482 |
| period_industrial | -0.1456 |
| type_knife | -0.1384 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| register_military_modern | +0.4351 |
| period_contemporary | +0.4219 |
| register_historical | -0.3800 |
| wield_two_hand | +0.3358 |
| wield_one_hand | -0.3353 |

---

### Axis 3

- **Variance explained:** 0.0459 (4.59%)
- **Provisional name:** PROVISIONAL: one-handed weapon emphasis
- **Bootstrap stability (mean cosine-dist):** 0.0131
- **Stability PASS (≤0.10):** YES
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| wield_one_hand | +0.4306 |
| wield_two_hand | -0.4298 |
| register_military_modern | +0.3107 |
| period_unknown | -0.2950 |
| period_contemporary | +0.2933 |
| register_historical | -0.2808 |
| type_pistol | +0.2304 |
| period_early_modern | +0.1992 |
| type_dagger | +0.1931 |
| lineage_east_asian | -0.1876 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| wield_one_hand | +0.4306 |
| wield_two_hand | -0.4298 |
| register_military_modern | +0.3107 |
| period_unknown | -0.2950 |
| period_contemporary | +0.2933 |

---

### Axis 4

- **Variance explained:** 0.0276 (2.76%)
- **Provisional name:** PROVISIONAL: period unknown dominant axis
- **Bootstrap stability (mean cosine-dist):** 0.3917
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| period_unknown | +0.4761 |
| lineage_east_asian | +0.3866 |
| period_industrial | -0.3060 |
| type_bow | -0.2626 |
| lineage_unknown | +0.2277 |
| type_crossbow | -0.2102 |
| lineage_north_american_indigenous | -0.2071 |
| type_rifle | -0.2013 |
| period_modern | -0.1866 |
| lineage_european | -0.1737 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| period_unknown | +0.4761 |
| lineage_east_asian | +0.3866 |
| period_industrial | -0.3060 |
| type_bow | -0.2626 |
| lineage_unknown | +0.2277 |

---

### Axis 5

- **Variance explained:** 0.0260 (2.60%)
- **Provisional name:** PROVISIONAL: bow-type weapon prominence
- **Bootstrap stability (mean cosine-dist):** 0.5907
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| type_bow | +0.5795 |
| type_crossbow | +0.5517 |
| lineage_unknown | +0.2195 |
| period_modern | -0.2083 |
| period_unknown | +0.1823 |
| lineage_south_american_indigenous | -0.1650 |
| period_classical | -0.1625 |
| period_industrial | +0.1555 |
| lineage_east_asian | +0.1467 |
| lineage_arctic_circumpolar | -0.1433 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| type_bow | +0.5795 |
| type_crossbow | +0.5517 |
| lineage_unknown | +0.2195 |
| period_modern | -0.2083 |
| period_unknown | +0.1823 |

---

### Axis 6

- **Variance explained:** 0.0253 (2.53%)
- **Provisional name:** PROVISIONAL: sword-type weapon prominence
- **Bootstrap stability (mean cosine-dist):** 0.4736
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| type_sword | +0.5863 |
| type_longsword | +0.3418 |
| type_greatsword | +0.3350 |
| type_shortsword | +0.2805 |
| period_industrial | +0.2447 |
| type_axe | -0.2318 |
| type_greataxe | -0.1612 |
| type_battleaxe | -0.1574 |
| lineage_unknown | +0.1550 |
| type_musket | +0.1446 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| type_sword | +0.5863 |
| type_longsword | +0.3418 |
| type_greatsword | +0.3350 |
| type_shortsword | +0.2805 |
| period_industrial | +0.2447 |

---

### Axis 7

- **Variance explained:** 0.0243 (2.43%)
- **Provisional name:** PROVISIONAL: lineage unknown dominant axis
- **Bootstrap stability (mean cosine-dist):** 0.6832
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| lineage_unknown | +0.4631 |
| period_early_modern | -0.3517 |
| type_pistol | +0.3438 |
| period_modern | +0.2417 |
| lineage_south_asian | -0.2397 |
| lineage_southeast_asian | -0.2389 |
| type_club | -0.2192 |
| lineage_north_american_indigenous | -0.1856 |
| lineage_arctic_circumpolar | -0.1774 |
| lineage_south_american_indigenous | +0.1662 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| lineage_unknown | +0.4631 |
| period_early_modern | -0.3517 |
| type_pistol | +0.3438 |
| period_modern | +0.2417 |
| lineage_south_asian | -0.2397 |

---

### Axis 8

- **Variance explained:** 0.0241 (2.41%)
- **Provisional name:** PROVISIONAL: axe-type weapon prominence
- **Bootstrap stability (mean cosine-dist):** 0.6263
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| type_axe | +0.4917 |
| type_greataxe | +0.3492 |
| type_battleaxe | +0.3356 |
| period_industrial | +0.3079 |
| period_modern | -0.2582 |
| type_musket | +0.2528 |
| type_rifle | +0.2185 |
| lineage_south_american_indigenous | -0.2025 |
| lineage_south_asian | +0.1918 |
| type_crossbow | -0.1746 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| type_axe | +0.4917 |
| type_greataxe | +0.3492 |
| type_battleaxe | +0.3356 |
| period_industrial | +0.3079 |
| period_modern | -0.2582 |

---

### Axis 9

- **Variance explained:** 0.0228 (2.28%)
- **Provisional name:** PROVISIONAL: axe-type weapon prominence
- **Bootstrap stability (mean cosine-dist):** 0.6692
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| type_axe | +0.3664 |
| type_greataxe | +0.2750 |
| type_crossbow | +0.2730 |
| type_sword | +0.2718 |
| type_battleaxe | +0.2642 |
| period_modern | +0.2350 |
| period_industrial | -0.2298 |
| type_bow | +0.2253 |
| type_rifle | -0.2213 |
| type_musket | -0.2144 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| type_axe | +0.3664 |
| type_greataxe | +0.2750 |
| type_crossbow | +0.2730 |
| type_sword | +0.2718 |
| type_battleaxe | +0.2642 |

---

### Axis 10

- **Variance explained:** 0.0217 (2.17%)
- **Provisional name:** PROVISIONAL: lineage north american indigenous dominant axis
- **Bootstrap stability (mean cosine-dist):** 0.7982
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| lineage_north_american_indigenous | +0.5155 |
| type_club | +0.4610 |
| lineage_south_asian | -0.3236 |
| type_dagger | -0.2752 |
| type_knife | +0.2679 |
| lineage_arctic_circumpolar | -0.2089 |
| lineage_east_asian | -0.1712 |
| type_musket | -0.1700 |
| lineage_unknown | +0.1651 |
| lineage_southeast_asian | +0.1569 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| lineage_north_american_indigenous | +0.5155 |
| type_club | +0.4610 |
| lineage_south_asian | -0.3236 |
| type_dagger | -0.2752 |
| type_knife | +0.2679 |

---

### Axis 11

- **Variance explained:** 0.0211 (2.11%)
- **Provisional name:** PROVISIONAL: period early modern dominant axis
- **Bootstrap stability (mean cosine-dist):** 0.7426
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| period_early_modern | +0.3351 |
| lineage_unknown | +0.2961 |
| type_knife | -0.2770 |
| type_spear | +0.2686 |
| lineage_east_asian | -0.2644 |
| lineage_north_american_indigenous | -0.2519 |
| lineage_arctic_circumpolar | -0.2345 |
| lineage_south_american_indigenous | -0.2206 |
| type_club | +0.1820 |
| lineage_european | +0.1819 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| period_early_modern | +0.3351 |
| lineage_unknown | +0.2961 |
| type_knife | -0.2770 |
| type_spear | +0.2686 |
| lineage_east_asian | -0.2644 |

---

### Axis 12

- **Variance explained:** 0.0190 (1.90%)
- **Provisional name:** PROVISIONAL: lineage european dominant axis
- **Bootstrap stability (mean cosine-dist):** 0.7340
- **Stability PASS (≤0.10):** FAIL
- **Single-feature flag:** No
- **Purely text (no structured in top-5):** No
- **Purely structured (no text in top-5):** YES

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
| lineage_european | +0.5377 |
| period_classical | -0.4165 |
| lineage_african | -0.3941 |
| type_dagger | -0.2562 |
| lineage_south_asian | -0.1953 |
| type_rifle | +0.1871 |
| lineage_southeast_asian | +0.1783 |
| type_pistol | +0.1539 |
| period_medieval | +0.1450 |
| period_early_modern | +0.1402 |

**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
| lineage_european | +0.5377 |
| period_classical | -0.4165 |
| lineage_african | -0.3941 |
| type_dagger | -0.2562 |
| lineage_south_asian | -0.1953 |

---

## Phase E-1-bis Flags

- Axis 4: UNSTABLE (bootstrap cosine-dist = 0.3917 > 0.10)
- Axis 5: UNSTABLE (bootstrap cosine-dist = 0.5907 > 0.10)
- Axis 6: UNSTABLE (bootstrap cosine-dist = 0.4736 > 0.10)
- Axis 7: UNSTABLE (bootstrap cosine-dist = 0.6832 > 0.10)
- Axis 8: UNSTABLE (bootstrap cosine-dist = 0.6263 > 0.10)
- Axis 9: UNSTABLE (bootstrap cosine-dist = 0.6692 > 0.10)
- Axis 10: UNSTABLE (bootstrap cosine-dist = 0.7982 > 0.10)
- Axis 11: UNSTABLE (bootstrap cosine-dist = 0.7426 > 0.10)
- Axis 12: UNSTABLE (bootstrap cosine-dist = 0.7340 > 0.10)

## Variance Explained Table

| Axis | EVR | Cumulative EVR | Stability |
|---|---|---|---|
| 1 | 0.0789 | 0.0789 | 0.0011 |
| 2 | 0.0567 | 0.1356 | 0.0118 |
| 3 | 0.0459 | 0.1815 | 0.0131 |
| 4 | 0.0276 | 0.2091 | 0.3917 |
| 5 | 0.0260 | 0.2351 | 0.5907 |
| 6 | 0.0253 | 0.2604 | 0.4736 |
| 7 | 0.0243 | 0.2847 | 0.6832 |
| 8 | 0.0241 | 0.3088 | 0.6263 |
| 9 | 0.0228 | 0.3316 | 0.6692 |
| 10 | 0.0217 | 0.3533 | 0.7982 |
| 11 | 0.0211 | 0.3744 | 0.7426 |
| 12 | 0.0190 | 0.3934 | 0.7340 |
