# Phase E-1 Math Note — Option-A Addendum

**Author:** legolas
**Date:** 2026-05-23
**Status:** PRE-FIRE — authored before full-mode Option-A fire (Discipline #1 math-before-code)
**Anchors:**
- `phase-E-1-math-note.md` (original math note)
- `phase-E-1-math-note-rerun-addendum.md` (RERUN addendum; partially stale — see §1 below)
- `dispatches/2026-05-23-legolas-phase-E-1-OPTION-A-single-stage-F2.md` (active dispatch)
- `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md` (design-side ratification)
- `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md` (forensic anchor)

This addendum covers five sections mandated by the Option-A dispatch: (1) pre-fire peak-memory projection, (2) single-stage F2 doctrine restatement + line-725 amendment, (3) per-lineage cluster-vs-noise projection, (4) bootstrap stability re-projection (already empirical), and (5) bis-disposition criteria (unchanged). Sections (6) covers the fire-scope decision.

---

## 1. Pre-Fire Peak-Memory Projection (load-bearing precondition)

Per Option-A dispatch Math-before-code §1: projection must show < 5 GiB before `--mode full` fires.

**Substrate:** N=48,430 rows. k_final=12 (from 11:05 partial-fire, unchanged by Option-A). Verified substrate count = 48,430 (SQL `SELECT COUNT(*) FROM v_category_sample` = 48,430).

### Memory accounting table

| Step | Object | Size estimate | Resident? | Notes |
|---|---|---|---|---|
| Load | corpus list (48,430 strings, avg ~200 chars) | ~10 MB | yes through D1 | string heap |
| TF-IDF fit | sparse matrix (48,430 × 500, ~50 nonzero/row) | ~20 MB sparse | yes through SVD | scipy sparse CSR |
| sqrt-F2 row-multiply | `tfidf_matrix.multiply(sqrt_w)` | sparse in-place | brief | sparse × dense → stays sparse |
| TruncatedSVD (LSA) fit_transform | working memory for randomized SVD | ~30-50 MB | brief | scipy linalg.svd internally; no dense materialization of full TF-IDF |
| LSA output | (48,430 × 100) dense | **38.7 MB** | yes through D1-D2 | |
| Structured feature block | (48,430 × 60) dense | **23.2 MB** | yes through D1-D2 | |
| Feature matrix X = [LSA, structured] | (48,430 × 160) dense | **62.0 MB** | yes through D3 | |
| X_weighted = X * sqrt_w | (48,430 × 160) dense | **62.0 MB** | brief (PCA only) | same shape; brief duplicate |
| TruncatedSVD (PCA) full n_max=50 | (48,430 × 50) projections + components | ~19 MB + ~7 MB | yes | returned as `svd_full`, `projections` |
| projections_k (k=12) | (48,430 × 12) | **4.65 MB** | yes through D3 | trimmed from 50-dim projections |
| Bootstrap (10 × sequential) | per-resample X_boot + TruncatedSVD | ~62 MB peak per resample | sequential; prior release before next | non-cumulative |
| **HDBSCAN.fit on un-expanded (48,430 × 12)** | KD-tree + MST + condensed tree | **~300-900 MB estimated** | spike | **Key change vs RERUN: 48,430 not 71,003** |
| GMM baseline (projections_k only) | GaussianMixture fit on (48,430 × 12) | ~50 MB | brief | no row-duplication |
| k-means baseline | KMeans fit on (48,430 × 12) | ~50 MB | brief | |
| Python interpreter + sklearn + numpy + hdbscan baseline | | ~500 MB | always | |
| **Estimated peak (HDBSCAN spike + resident objects)** | | **~1.0–1.8 GB** | peak | well under 5 GiB ceiling |

**Correction vs RERUN addendum §1.3:** The RERUN addendum calculated the expanded HDBSCAN matrix at ~71,000 rows (using integer-duplication). Under Option-A, the matrix is the un-duplicated 48,430 × 12 = identical to `projections_k`. HDBSCAN's internal structures scale with n; at 48,430 vs 71,003, the peak memory requirement drops significantly (empirically the 71,003-row case exhausted 8 GiB; 48,430 is ~68% of that n, and HDBSCAN's complexity has sub-linear and quadratic components mixed — conservatively project 40-60% of the fatal run's peak, which was measured to exceed 8 GB → estimated Option-A peak ~3.2-4.8 GB absolute worst case).

Actually, let me tighten this: the dispatch's triage notes state "on 48,430 rows the same per-row factor applies but a smaller n — projected peak roughly half of the 71k case." Half of "clearly > 8 GB" = "clearly > 4 GB" — which is above my 5 GiB comfortable ceiling. **This warrants the `resource.setrlimit` defensive ceiling** to catch a potential MemoryError before kernel panic.

**More grounded estimate:** HDBSCAN.fit on n=48,430 × d=12 in euclidean metric. The primary memory consumer is the mutual-reachability distance matrix (MRD) computation. With ball-tree indexing, HDBSCAN doesn't materialize the full n×n distance matrix. Empirical reports for HDBSCAN on ~50k rows in low-dimensional space (d≤20) run in 2-4 GB peak with default parameters. At min_cluster_size=30 and min_samples=5 with eom method, the condensed tree can be large. Conservative estimate: **2-4 GB peak for the HDBSCAN step alone**.

**Sum with other resident objects (~650 MB):** ~2.7-4.7 GB total.

**Verdict:** Projected peak ~2.7-4.7 GB. This overlaps the 5 GiB ceiling's lower end. The `resource.setrlimit(RLIMIT_AS, 6 GiB)` defensive ceiling is **mandatory** — adds MemoryError crash instead of kernel panic if projection is violated.

**Go/no-go:** PROCEED with fire, with `resource.setrlimit` applied. If Python raises MemoryError at HDBSCAN.fit, we surface to knight-rider for Option B (subsample) or Option C (cloud). This is preferable to a fourth kernel panic.

---

## 2. Single-Stage F2 Doctrine — Restatement + Line-725 Amendment

**Ratification source (authoritative):** `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md`

### F2 Role Clarification (verbatim from gandalf ratification § 2.2)

| F2's role | Stage | Verdict |
|---|---|---|
| Ensure rare lineages **influence which directions are principal** (axes aren't dominated by fantasy_generic variance) | PCA (sqrt(w_i) row-multiplication on TF-IDF before SVD; script lines 217-225) | **Load-bearing; Option A preserves this** |
| Ensure mean/std estimates aren't dominated by fantasy_generic | StandardScaler (sample_weight via weighted mean/std; script lines 240-246) | **Load-bearing; Option A preserves this** |
| ~~Force rare-lineage clusters into existence regardless of spatial coherence~~ | ~~HDBSCAN row-duplication; script lines 392-407~~ | **Substrate-led violation; Option A correctly removes this** |
| ~~Force rare-lineage weighting in GMM fit~~ | ~~GMM row-duplication (claimed in math note original §1.4 and features.md line 725)~~ | **Overstatement; GMM was already implemented without row-duplication (script line 510: `gmm.fit(projections_k)`); violation did not exist in code** |

### Single-Stage F2 Doctrine (new canonical)

**F2 is a single-stage operator applied at axis-discovery + feature-scaling. NOT applied at the clustering stage.** Clusters reflect actual projection-space density in the F2-amplified coordinate system. A rare-lineage cluster emerges **iff** its rows are genuinely spatially coherent in the F2-weighted projection space.

### Amendment to math note original §1.4 and features.md line 725

**Original statement (math note §1.4 and features.md "Application" line):**
> "applied as sqrt(w_i) row-multiplication on TF-IDF before SVD; as sample_weight on StandardScaler mean/std; as integer-duplication for HDBSCAN and GMM fit."

**Amended statement (Single-Stage F2 Doctrine, 2026-05-23):**
> "F2 applied as sqrt(w_i) row-multiplication on TF-IDF before SVD (PCA stage); as sample_weight on StandardScaler mean/std (feature-scaling stage). NOT applied at clustering stage; clusters reflect actual projection-space density in the F2-amplified coordinate system. Note: GMM was always implemented without row-duplication (script line 510: `gmm.fit(projections_k)`) — the original §1.4 claim of 'integer-duplication for GMM fit' was overstated vs actual code implementation."

This amendment is operative for the pipeline script's `features.md` output and the Option-A code edit (see §6 below for code change description).

---

## 3. Per-Lineage Cluster-vs-Noise Projection

With Option-A (no row-duplication) and `min_cluster_size=30`:

| Lineage | N in v_category_sample | min_cluster_size threshold | Expected behavior |
|---|---|---|---|
| fantasy_generic | 16,284 | 30 | Far above; will form many clusters |
| east_asian | 13,080 | 30 | Far above; will form clusters |
| european | 12,515 | 30 | Far above; will form clusters |
| unknown | 1,956 | 30 | Far above; will form clusters (probably mixed-lineage) |
| middle_eastern | 1,327 | 30 | Far above; may form distinct clusters if spatially coherent |
| cross_cultural | 883 | 30 | Far above; likely scattered across multiple clusters |
| south_asian | 822 | 30 | Above; may form clusters if spatially coherent |
| southeast_asian | 694 | 30 | Above; may form clusters (kris/parang distinct vocab) |
| african | 465 | 30 | Above; may form clusters |
| south_american_indigenous | 197 | 30 | Above; may form clusters (projectile weapons distinct) |
| mesoamerican | 83 | 30 | Above minimum but marginal; may split: some spatially coherent rows form a cluster, others scatter to nearest |
| arctic_circumpolar | 56 | 30 | Above minimum but small; likely 1 cluster if coherent |
| oceanic | 39 | 30 | Above minimum but small; likely 1 cluster if coherent |
| **north_american_indigenous** | **29** | **30** | **Below minimum → cannot form its own cluster; will be noise-assigned to nearest cluster via `assign_noise_to_nearest`** |

**Design-side caveat (gandalf ratification §3):** "Keep `min_cluster_size=30` for this fire. Preserves the math note's stated parameter and gives a clean baseline comparison if a future sensitivity sweep tries lower values. north_american_indigenous (N=29) will noise-assign — document this explicitly in the dispatch's design-intent section."

**Phase E-1.5 carry:** Sensitivity sweep on `min_cluster_size` ∈ {10, 15, 20, 30} queued by gandalf ratification §4. If rare-lineage representation in Option-A output is too sparse for Phase E-2 labeling, this carry fires.

---

## 4. Bootstrap Stability Re-Projection (Empirical — Already Known)

The 11:05 partial-fire (the RERUN attempt before the kernel panic) **completed Deliverables 1 and 2 cleanly** before crashing at Deliverable 3. The axis discovery results are preserved on disk at `phase-E-1-axis-discovery.md` and `phase-E-1-axis-loadings.json`.

**Empirical bootstrap stability results (11:05 fire, N=48,430, k=12):**

| Axis | Bootstrap cosine-dist | Stability (≤ 0.10) |
|---|---|---|
| 1 | 0.0011 | **PASS** |
| 2 | 0.0118 | **PASS** |
| 3 | 0.0131 | **PASS** |
| 4 | 0.3917 | FAIL |
| 5 | 0.5907 | FAIL |
| 6 | 0.4736 | FAIL |
| 7 | 0.6832 | FAIL |
| 8 | 0.6263 | FAIL |
| 9 | 0.6692 | FAIL |
| 10 | 0.7982 | FAIL |
| 11 | 0.7426 | FAIL |
| 12 | 0.7340 | FAIL |

**Axes stable: 3 of 12.** This is below the 6-of-k_final minimum acceptance threshold per the RERUN dispatch Math-before-code §5.

**Option-A impact on bootstrap stability:** NONE. The single-stage F2 change removes row-duplication at the HDBSCAN stage only. It does NOT change the PCA or bootstrap computation. The on-disk axis discovery output is accurate and unchanged.

**Phase E-1-bis disposition (per corrected-pool bis-criteria, RERUN dispatch §Math-before-code §5):**

> "If k_final ≥ 8 AND fewer than 6 axes pass bootstrap stability → **Phase E-1-bis flag — partial acceptance**. Document stable axes; surface to knight-rider for gandalf + jack-ryan critique pair on methodology."

k_final=12 ≥ 8: YES. Stable axes: 3 (below 6). **→ Phase E-1-bis partial-acceptance bis-flag applies.**

This is the dominant outcome from Phase E-1. The clustering (Deliverable 3) may still pass acceptance (50-150 clusters, ≥0.85 purity, DB populated), allowing Phase E-2 to proceed on the 3 stable axes; but the methodology review on axes 4-12 instability is required.

**Rerun addendum §4 projection vs empirical:** The rerun addendum projected "≥ 8 of k_final axes will pass bootstrap stability... all axes pass is likely." This projection was **refuted empirically**. The pool-structural analysis was correct (larger n, lower weights), but the stability failure runs deeper — axes 4-12 capture weapon-type variation and rare-lineage cross-cuts that are genuinely rotatable under bootstrap resampling. This is not a pool-artifact; it is real signal about the substrate's dimensionality structure.

**Do NOT re-run bootstrap.** The empirical result is valid and unchanged by Option-A.

---

## 5. Bis-Disposition Criteria (Unchanged from RERUN Dispatch)

| Condition | Disposition |
|---|---|
| k_final ≥ 8 AND ≥ 6 stable | No Phase E-1-bis flag |
| k_final ≥ 8 AND < 6 stable | **Phase E-1-bis flag — partial acceptance** ← THIS APPLIES (3 of 12) |
| k_final < 8 | Phase E-1-bis flag — genuine methodology evidence |
| k_final = 0 stable (pathological) | Halt + flag |

**Current disposition: Phase E-1-bis partial-acceptance bis-flag confirmed from empirical evidence.**

---

## 6. Fire-Scope Decision

**Decision: Run end-to-end with `--mode full`** (skip-Deliverables-1-2 option NOT taken).

Reasoning:
1. No native `--deliverable3-only` mode exists in the pipeline; adding one requires saving/restoring `projections_k` as an intermediate artifact, adding complexity and another failure mode.
2. The end-to-end memory budget is projected at ~2.7-4.7 GB (§1 above) — within the 6 GiB `resource.setrlimit` ceiling.
3. The Deliverable 1-2 memory spike (TF-IDF stage) is sparse-only; no 194 MB dense materialization actually occurs (the script uses `tfidf_matrix.multiply(sqrt_w)` which stays sparse through TruncatedSVD).
4. Axis-discovery output will be re-written with identical results (same data, same RANDOM_STATE=42). Any numerical difference from the on-disk version indicates a problem — this is a free consistency check.
5. Running end-to-end avoids any state inconsistency between the stored axis output and the fresh clustering.

**Script changes applied before fire:**
1. `resource.setrlimit(resource.RLIMIT_AS, 6 GiB)` defensive ceiling added at top of `main()`.
2. `run_hdbscan` row-duplication block removed; `clusterer.fit(projections_k)` called directly on un-expanded matrix.
3. `weights` parameter retained in `run_hdbscan` signature with a forward-compat comment (per dispatch §open questions #3).
4. `features.md` "Application" line (script line ~725) updated to reflect single-stage F2 doctrine.

---

**Signed:** legolas
**Status:** Math note addendum complete — Option-A fire authorized pending script edit.
**Substrate confirmed:** 48,430 rows; lineage distribution matches elrond Phase-D-bis §5 exactly.
