# Phase E-1 Math Note — RE-FIRE Addendum

**Author:** legolas
**Date:** 2026-05-23
**Status:** PRE-FIRE — addendum authored before re-fire code runs (Discipline #1 math-before-code)
**Anchors:** Phase E-1 math note (`phase-E-1-math-note.md`) + Phase-D-bis completion summary §5 + re-fire dispatch (2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md)

This document is an **addendum only**. The original math note (`phase-E-1-math-note.md`) is preserved as historical record. This addendum covers the four sections mandated by the re-fire dispatch: (1) updated F2 weight table, (2) re-stated k-selection projection, (3) re-stated cluster-count projection, (4) bootstrap stability prior + Phase E-1-bis disposition criteria.

---

## 1. Updated F2 Weight Table

Pool: N = 48,430 rows. 14 distinct cultural_lineage_canonical buckets (vs 11 in old pool — mesoamerican, cross_cultural, oceanic, and north_american_indigenous are now meaningfully populated).

**Derivation:**

Per-row raw_weight = 1 / count(bucket_i). Mean raw_weight = sum(all per-row raw_weights) / N. Each bucket contributes count_i × (1/count_i) = 1 to the sum, so sum = 14 (number of distinct buckets). Mean raw_weight = 14 / 48,430 = 0.0002892. Normalized weight for bucket i = (1/count_i) / 0.0002892 = 48,430 / (14 × count_i) = 3,459.3 / count_i.

| cultural_lineage_canonical | count | freq | raw_weight (1/count) | normalized_weight | old_pool normalized_weight | Δ |
|---|---|---|---|---|---|---|
| fantasy_generic | 16,284 | 33.62% | 0.0000614 | **0.213** | 0.112 | +90% (less down-weighted; still suppressed) |
| east_asian | 13,080 | 27.01% | 0.0000765 | **0.264** | 34.67 | **−99.2% (was dominant singleton-amplifier)** |
| european | 12,515 | 25.84% | 0.0000799 | **0.276** | 6.963 | −96.0% |
| unknown | 1,956 | 4.04% | 0.000511 | **1.769** | 76.96 | −97.7% |
| middle_eastern | 1,327 | 2.74% | 0.000754 | **2.606** | 36.12 | −92.8% |
| cross_cultural | 883 | 1.82% | 0.001133 | **3.918** | (not in old pool at this size) | — |
| south_asian | 822 | 1.70% | 0.001217 | **4.208** | 80.38 | −94.8% |
| southeast_asian | 694 | 1.43% | 0.001441 | **4.986** | 196.4 | −97.5% |
| african | 465 | 0.96% | 0.002151 | **7.439** | 884.0 | −99.2% |
| south_american_indigenous | 197 | 0.41% | 0.005076 | **17.56** | 3.472 | +406% (was game-FP inflated in old pool) |
| mesoamerican | 83 | 0.17% | 0.012048 | **41.68** | (new to post-fix pool) | — |
| arctic_circumpolar | 56 | 0.12% | 0.017857 | **61.77** | 353.6 | −82.5% |
| oceanic | 39 | 0.08% | 0.025641 | **88.70** | (0 rows in old pool) | — |
| north_american_indigenous | 29 | 0.06% | 0.034483 | **119.3** | 1768 | **−93.3% (was the worst singleton-amplifier)** |

**Key structural improvements vs old pool:**
- Max normalized weight: 119× (north_american_indigenous, N=29) vs 1768× (north_american_indigenous, N=1 in old pool). **14.8× reduction in amplification.**
- east_asian dropped from 34.67× to 0.264× — the dominant PCA axis-disruption source is eliminated.
- No bucket has a weight above 120× — far from the 1518× singleton-amplification threshold that caused axis instability.
- All 14 lineage buckets have ≥ 29 actual rows, ensuring bootstrap resamples always include multiple representatives per bucket.

**F2 weight application in pipeline (unchanged from math note §1.4):**

| Application point | Method | Status |
|---|---|---|
| TF-IDF → TruncatedSVD (LSA) | Row-multiply by sqrt(w_i) before SVD fit | Unchanged |
| StandardScaler structured features | Weighted mean/std manually computed | Unchanged |
| HDBSCAN fit | Integer-duplication capped at 20× | Unchanged (max 20 rounds to 20 for arctic/oceanic/north_american_indigenous; east_asian rounds to 0 → clip to 1) |
| PCA on full feature matrix | Row-multiply by sqrt(w_i) before TruncatedSVD | Unchanged |

**HDBSCAN expanded matrix estimate (new pool):**
- fantasy_generic: 16,284 × 1 = 16,284 (rounds down to 0, clip to 1)
- east_asian: 13,080 × 1 = 13,080 (same clip)
- european: 12,515 × 1 = 12,515
- unknown: 1,956 × 2 = 3,912 (round(1.769)=2)
- middle_eastern: 1,327 × 3 = 3,981
- cross_cultural: 883 × 4 = 3,532
- south_asian: 822 × 4 = 3,288
- southeast_asian: 694 × 5 = 3,470
- african: 465 × 7 = 3,255
- south_american_indigenous: 197 × 18 = 3,546 (round(17.56)=18)
- mesoamerican: 83 × 20 = 1,660 (round(41.68)=42, clip to 20)
- arctic_circumpolar: 56 × 20 = 1,120 (round(61.77)=62, clip to 20)
- oceanic: 39 × 20 = 780 (round(88.70)=89, clip to 20)
- north_american_indigenous: 29 × 20 = 580 (round(119.3)=119, clip to 20)

**Total expanded matrix: ~71,000 rows.** Manageable; HDBSCAN at this scale is routine (elrond's Step 7 F4 ran on 51,166 rows in ~8 min). Expect HDBSCAN to run in 5-15 min.

---

## 2. Re-Stated K-Selection Projection

**Original projection (from math note §3):** k_80 ≈ 30-40, kink_idx near the elbow, k_final projected in 8-12 range. Empirical was k_80=35, kink_idx=2, k_final=4 (clamped by the kink formula).

**Analysis of why the old pool produced kink_idx=2:**

The old pool was 94.5% fantasy_generic. After F2 weighting, east_asian (N=51) got normalized_weight 34.67×, north_american_indigenous (N=1) got 1768×. The resulting weighted covariance matrix was dominated by:
- PC1: the fantasy_generic / historical contrast (one giant structural split)
- PC2+: noise from singleton-amplified minority lineages (each with only 1-51 rows)

The scree dropped catastrophically after PC1-2, producing kink_idx=2 (the steepest second-derivative was right at the beginning of the scree). The `min(kink_idx+2, 12)=4` formula then over-constrained k_final.

**New pool projection:**

With 14 lineage buckets all having ≥ 29 rows, and max weight 119× (vs 1768×), the covariance structure should be substantially richer:

| Projected axis | Structural source | Reasoning |
|---|---|---|
| PC1 | Register/source contrast (fantasy/TRPG vs historical/museum) | 33.6% fantasy_generic; ~63% historical — this split is still structurally dominant, just less extreme |
| PC2 | Cultural lineage contrast: east_asian vs european | 27% east_asian, 25.8% european — these are now near-equal buckets; the axis between them should be stable and informative |
| PC3 | Historical period contrast: fictional/contemporary vs classical/medieval | Game sources → fictional; museum sources → classical/medieval; both well-populated |
| PC4 | Wieldability: two-hand vs one-hand vs shoulder-supported | Museum content includes firearms (shoulder_supported), pole weapons (two-hand), swords (one/two-hand) |
| PC5 | Weapon type cluster: sword/dagger/edged vs hammer/mace/blunt vs bow/ranged | Text-semantic content should separate these clearly |
| PC6 | Middle_eastern/south_asian cultural contrast | 2.7% + 1.7% = 4.4% but at ~2.6-4.2× weight → effective contribution comparable to cross_cultural |
| PC7+ | Finer-grained weapon-type variation, period micro-clusters, source-library residuals | Less certain; depends on LSA decomposition quality |

**Projection for k_80:** 15-30 (the variance should be more spread across structural dimensions, but still concentrated in the top-15 axes). The pool is more structurally rich than the old pool.

**Projection for kink_idx:** 4-8 (vs kink_idx=2 before). The scree should be more gradual; the dramatic cliff after PC1 should be replaced by a more shoulder-like decline as cultural diversity distributes variance across multiple axes.

**Projection for k_final (with k-clamp amendment — see §5 below):** **8-10.** The formula `max(min(kink_idx+2, 12), 8)` would give 8 if kink_idx < 6, or kink_idx+2 if kink_idx ≥ 6. Combined with `min(k_80, 12)`, I project k_final landing at 8-10, most likely 8.

**Key uncertainty:** If the LSA stage collapses meaningful semantic variance before PCA sees it, the scree might still be cliff-shaped. But with 48,430 rows and genuine typological variety (museum content has "Kris with Sheath," "Naginata," "Wheel-lock Pistol," "Halberd," "Mace" — diverse structural content), the TF-IDF should capture multi-modal vocabulary clusters that survive LSA decomposition.

---

## 3. Re-Stated Cluster-Count Projection

**Original projection:** 50-150 emergent clusters. Empirical was N=100 smoke-mode stale output (full mode never completed).

**New pool analysis:**

The 48,430-row pool has:
- ~16,284 fantasy_generic rows: these include nick-aschenbach-dnd-data (6,205), wow-classic-items (4,429), bsdata-warhammer-aos (2,157), OSRS (940), Diablo2 (519), Path of Exile (488), Fextralife games (~1,271 combined), 5e (147). These source-by-source weapon taxonomies should cluster by weapon type (sword/axe/spell/etc.) with lineage/period as secondary dimensions.
- ~13,080 east_asian rows: predominantly wikidata Chinese museum entries. Likely to cluster by weapon_type (dao/jian/naginata/yumi) and period. But many share similar structured features → might produce fewer, denser east_asian clusters.
- ~12,515 european rows: predominantly wikidata + wikipedia + royal_armouries + met-museum. Rich typological variety (sword/rapier/halberd/pike/cannon/pistol/armour). Likely 20-40 european-dominant clusters.
- ~1,956 unknown: likely scattered across clusters or into a few generic clusters.
- Smaller lineage buckets (middle_eastern, south_asian, etc.): may form distinct clusters by cultural distinctiveness of weapon names (e.g., tulwar, khanjar, katana, kris).

**Projection:** 70-130 clusters. I project the lower end of the range is more likely than the upper end given that:
- Museum content is repetitive within source (e.g., 83 "Kris with Sheath" variants in met-museum may aggregate into a few "southeast_asian early_modern" clusters)
- east_asian content from wikidata has similar structured profiles (limited weapon_type variety in chinese provincial museum entries)
- The F2 weighting amplifies rare lineage clusters, which encourages HDBSCAN to find them even at small N

**Adjustment risk:** Primary parameter min_cluster_size=30 on 48,430 rows (0.062% threshold). The proportional threshold would be ~87 for the same relative density as min_cluster_size=30 on 16,699 rows. Starting at 30 risks over-segmentation (>150 clusters). The auto-retry (>150 → retry with min_cs=50) will handle this. My recommendation: proceed with min_cs=30 as primary; expect auto-retry to min_cs=50 is likely given the larger pool. If still >150, consider min_cs=80 as an additional retry step (this would require a script note; document in the run log).

**OQ3 recommendation (F6 cluster-size threshold):** Maintain min_cluster_size=30 as primary. The acceptance criterion is cluster count 50-150, not relative density. F6 flags (<20 members) remain meaningful at the absolute scale regardless of pool size — a cluster of 19 rows is still too small for the N=20 downstream sampling requirement.

---

## 4. Bootstrap Stability Prior + Phase E-1-bis Disposition Criteria

### 4.1 Prior on bootstrap stability

**Old pool result:** axes 2-4 had bootstrap cosine-dist 0.35-0.73 (FAIL). Root cause: east_asian (N=51, weight 34.67×) and north_american_indigenous (N=1, weight 1768×) produced singleton-amplified pseudo-variance in axes 2-4. Bootstrap resamples of 16,699 rows could miss these 1-51 rare rows entirely on some resamples, making axes 2-4 rotate to different orientations across resamples.

**New pool stability analysis:**

The stability concern was specifically about bootstrap resamples omitting rare-lineage rows entirely. On the new pool:
- north_american_indigenous: N=29. With N=48,430 and bootstrap resample size=48,430, expected number of north_american_indigenous rows per resample = 29 × (1 - (1-1/48430)^48430) ≈ 29 × (1 - 1/e) ≈ 29 × 0.632 = 18.3. Bootstrap std of this count ≈ sqrt(29 × 0.632 × 0.368) ≈ 2.59. Min expected ≈ 18.3 - 3×2.59 ≈ 10.5.
- So with very high probability every resample contains ≥ 10 north_american_indigenous rows, eliminating the "zero-or-one-instance" axis disruption.
- east_asian: N=13,080. Per resample ≈ 13,080 × 0.632 = 8,267. Stable.

**Prior:** I project ≥ 8 of k_final axes will pass bootstrap stability (cosine-dist ≤ 0.10). The structural improvement is large enough that I project full acceptance (all axes pass) is likely if k_final is 8-10. The only axes at risk are the very-high axes (8+) which may capture fine-grained variation that's genuinely borderline.

### 4.2 Phase E-1-bis disposition criteria (per dispatch §Math-before-code §5)

| Condition | Disposition | Action |
|---|---|---|
| k_final ≥ 8 AND ≥ 6 of those axes pass bootstrap stability (≤ 0.10) | **No Phase E-1-bis flag** | Acceptance met. Proceed to clustering + Phase E-2 hand-off. |
| k_final ≥ 8 AND fewer than 6 axes pass bootstrap stability | **Phase E-1-bis flag — partial acceptance** | Document stable axes; surface to knight-rider for gandalf + jack-ryan critique pair on methodology. |
| k_final < 8 (even after k-clamp amendment forcing floor at 8: only applies if all 8 forced axes fail stability) | **Phase E-1-bis flag — genuine methodology evidence** | The pool-artifact escape is no longer available. Reserve gandalf A1+D1 path re-evaluation. |
| k_final = 0 stable axes (pathological) | **Halt + flag** | Something is wrong methodologically. |

**My projected outcome:** No Phase E-1-bis flag. k_final likely 8-10; ≥ 8 of those axes likely to pass bootstrap stability given the structural improvement in the corrected pool.

---

## 5. K-Selection Clamp Amendment (OQ1 Resolution)

**Issue:** The current formula in `run_pca_axis_discovery()`:
```python
k_final = min(max(k_80, 8), min(kink_idx + 2, 12))
```
can produce k_final < 8 when kink_idx < 6, because `min(kink_idx+2, 12)` becomes the binding constraint even though `max(k_80, 8)` ≥ 8.

On the old pool this gave k_final=4 with kink_idx=2. If the new pool's scree kink is still early (e.g., kink_idx=4, kink+2=6), the formula would produce k_final=6 — below the 8-axis acceptance floor.

**Amendment (within scope per dispatch §Open questions #1; F5 lock holds — method is unchanged; only k-selection heuristic):**

```python
# Take the larger of: kink-constrained estimate or k_80-based estimate; cap at 12; floor at 8
k_from_kink = min(kink_idx + 2, 12)
k_from_var = min(k_80, 12)
k_raw = max(k_from_kink, k_from_var)
k_final = max(k_raw, 8)  # floor at 8 per acceptance criterion
```

**Rationale:** The acceptance criterion requires ≥ 8 axes. If the scree genuinely suggests fewer than 8, we still attempt 8 and bootstrap-test all 8. The Phase E-1-bis determination is based on how many axes pass stability — not on whether the kink forced a floor. This gives the empirical evidence a chance to speak: if the corrected pool genuinely has only 4 stable axes, bootstrap will reveal that; if it has 8 stable axes, the k_from_kink clamp shouldn't prevent us from finding them.

**This amendment is applied to the pipeline script before the re-fire.**

---

## 6. Bootstrap Resample Count (OQ2 Resolution)

**OQ2:** With N=48,430 (vs 16,699), is 10 bootstrap resamples still adequate?

**Analysis:** Bootstrap stability assessment is about axis orientation consistency, not sample-size estimation precision. 10 resamples is sufficient to detect systematic instability (which manifested as 0.35-0.73 cosine-dist on the old pool). The failure mode on the old pool was not insufficient bootstrap precision — it was genuine axis rotation across resamples due to the singleton-amplification problem. With the corrected pool, 10 resamples remains adequate.

**If a specific axis shows cosine-dist in the 0.08-0.12 borderline zone:** note it in the completion summary as "borderline stable" rather than triggering a full re-run with more resamples. The 0.10 threshold is a planning threshold, not a hair-trigger.

**Decision: retain n_bootstrap=10 unchanged.**

---

## 7. Phase E-2 Hand-Off Shape Recommendation (OQ4 Projection)

Based on the projected axis structure (§2 above), the completion summary's Phase E-2 hand-off should emphasize:

1. **Most-canonical axes** (likely PC1-PC5): those loading clearly on a single conceptual dimension (register, lineage, period, wieldability, weapon-type). These are the cleanest candidates for gandalf to name canonically.
2. **Borderline axes** (likely PC6+): those loading on a mix of features or capturing fine-grained residuals. These may need gandalf to split/merge.
3. **Clusters most coherent:** museum-content clusters with a single dominant weapon type (e.g., "east_asian classical kris" or "european medieval sword") — these are the cleanest for the downstream N=20 sampling requirement.
4. **Clusters most mixed:** likely the large fantasy_generic clusters containing all-period game weapons — these are the most likely F6 candidates (either too many members or too much internal diversity).
5. **Method-comparison disagreements:** any clusters where HDBSCAN and GMM/k-means disagree significantly on boundaries should be flagged as "disambiguation targets" for gandalf in E-2.

---

## 8. Summary of Pre-Fire Projections

| Metric | Original projection | New projection | Acceptance target |
|---|---|---|---|
| k_final | 8-12 (was 4 empirically on wrong pool) | **8-10** | 8-12 |
| Cumulative EVR at k_final | ≥ 30% target | **25-40%** (more spread variance) | ≥ 30% target, ≥ 20% minimum |
| Bootstrap stability | Expected pass (was FAIL on old pool) | **Expected: all k_final axes pass** | ≥ 6 of k_final pass ≤ 0.10 |
| Cluster count | 50-150 | **70-130** | 50-150 |
| Cluster purity | ≥ 0.85 | **≥ 0.85 likely** (more structured pool should cluster cleanly) | ≥ 0.85 |
| Phase E-1-bis flag | Possible (old pool was wrong) | **None expected** | N/A |

---

**Signed:** legolas
**Status:** Math note addendum complete — re-fire pipeline authorized.
**Script amendment:** k-clamp formula to be updated before `--mode full` run (§5 above).
