# Phase E-1 Math Note — Frame-Revision Addendum (Stratified Subsample k=3)

**Author:** legolas
**Date:** 2026-05-23
**Status:** PRE-FIRE — authored before `--mode subsample-k3` code is written (Discipline #1 math-before-code)
**Dispatch:** `dispatches/2026-05-23-legolas-phase-E-1-frame-revision-stratified-subsample-k3.md`
**Anchors:**
- `phase-E-1-math-note.md` (original)
- `phase-E-1-math-note-rerun-addendum.md` (RERUN addendum)
- `phase-E-1-math-note-option-a-addendum.md` (Option-A addendum; §4 bootstrap-stability table is authoritative)
- `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md` (resize rationale)
- `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` §9 (addendum — 4th panic + Pattern-A-deep ratification failure)

Six sections required by the dispatch. All choices committed before code begins.

---

## § 1. Pre-Fire Peak-Memory Projection

**Target:** < 1 GiB peak (< 5 GiB ceiling). Show no working object exceeds 100 MB.

| Step | Object | Shape | dtype | Size estimate | Resident? | Notes |
|---|---|---|---|---|---|---|
| Load rows from DB | Python list of 48,430 tuples | — | — | ~25 MB | yes through D1 | avg tuple ~500 bytes |
| Build text corpus | list of 48,430 strings | — | — | ~50 MB | yes through TF-IDF | avg ~1000 chars/row |
| TF-IDF fit | sparse matrix | (48430, 500) | float32 | ~20 MB sparse | yes through LSA | scipy CSR |
| sqrt-F2 row-multiply | sparse matrix (in-place) | (48430, 500) | float32 | ~20 MB | brief | stays sparse |
| TruncatedSVD (LSA) | working memory (randomized SVD internals) | — | float64 | ~30-50 MB | brief | no full matrix materialization |
| LSA output | dense | (48430, 100) | float64 | **38.7 MB** | yes through D2 | |
| Structured feature block | dense | (48430, 60) | float32 | **23.2 MB** | yes through D2 | |
| Feature matrix X | dense | (48430, 160) | float64 | **62.0 MB** | yes through D2+proj | |
| X_weighted for PCA | dense | (48430, 160) | float64 | **62.0 MB** | brief | same shape; brief duplicate |
| Minimal PCA (k=3) | (48430, 3) projections + (3, 160) components | — | float64 | ~1.1 MB + 0.004 MB | yes (components only retained) | projections discarded after axes extracted |
| **projections_3** = X @ axes.T | dense | **(48430, 3)** | float64 | **1.2 MB** | yes through subsample + assign | tiny |
| Cache to disk (npz) | file | (48430, 3) | float64 | ~1.1 MB on disk | no (just write) | |
| Stratified subsample indices | int array | (10000,) | int64 | ~80 KB | yes | |
| Subsample projections | dense | **(10000, 3)** | float64 | **~240 KB** | yes during HDBSCAN | |
| HDBSCAN.fit on (10000, 3) | KD-tree + MST + condensed tree | — | mixed | **~5–50 MB peak** | spike | empirical HDBSCAN on N=10K, d=3: well-established lightweight; d=3 is favorable for KD-tree |
| Centroid matrix | dense | (~50–200, 3) | float64 | **~48 KB** | yes during assign | assuming ≤200 clusters |
| Nearest-assign for 38K rows | distance matrix (batch) | (38430, 3) batch | float64 | **~925 KB batch** | brief | batched computation; never full 38K×200 distance matrix at once |
| psutil RSS check | scalar | — | — | trivial | — | |
| Python baseline residency | interpreter + libs | — | — | ~500 MB | always | sklearn + numpy + hdbscan imports |
| **Estimated peak** | **all resident + HDBSCAN spike** | — | — | **~600–700 MB** | — | **WELL UNDER 1 GiB ceiling** |

**Comparison with prior panics:**
- Panic 4 (OPTION-A): HDBSCAN on (48430 × 12) > 8 GiB → panic
- This fire: HDBSCAN on (10000 × 3) ≈ 5–50 MB → trivial

**psutil RSS-guard:** Adding `psutil.Process().memory_info().rss` checkpoint at start of HDBSCAN.fit. Will log RSS and raise if > 6 GiB (belt-and-suspenders; not expected to trigger given above projection). `psutil` is an optional dependency; if not available, log a warning and continue.

**resource.setrlimit:** Not retried. Failed silently on macOS for all 4 panics. `psutil` RSS-check is sufficient.

**Go/no-go: PROCEED.** Peak memory is single-digit-percentage of available 8 GiB. No risk.

---

## § 2. Substrate-Voting-Is-Binding Application

**Rationale for k=3:**

The full-pool fire at 11:05:44 EDT (the OPTION-A partial fire — D1+D2 completed cleanly before panic 4 at 11:43:45) produced bootstrap stability results (N=48,430, 10 resamples, RANDOM_STATE=42):

| Axis | Bootstrap cosine-dist | Stability (≤ 0.10) |
|---|---|---|
| 1 | 0.0011 | **PASS** |
| 2 | 0.0118 | **PASS** |
| 3 | 0.0131 | **PASS** |
| 4 | 0.3917 | FAIL |
| 5 | 0.5907 | FAIL |
| 6 | 0.4736 | FAIL |
| 7–12 | 0.68–0.80 | FAIL |

**k_stable = 3.** The substrate voted 3 stable axes out of 12.

Per the Discipline #18 amendment candidate (frame-revision note §4, gandalf-flagged):
> "When a substrate-driven measurement (bootstrap-stability at axis discovery) produces a value substantially below the methodology's chosen parameter, the chosen parameter must be cut to the substrate-driven value before the next stage fires."

k_stable=3 vs k_chosen=12 is a 4× difference — "substantial margin." This is a **methodology gate**, not a flag. The dispatch operationalizes this gate by setting `--k_final 3`.

The prior Pattern-A-deep ratification-discipline failure (gandalf, 2026-05-23, kernel-panic-diagnosis §9.2): bootstrap-stability at 11:05 was substrate voting; treating it as a flag rather than a gate authorized the OPTION-A re-fire at k=12 → 4th panic. This addendum documents the gate as binding; no future override without explicit redesign rationale.

**`--k_final 3` is the correct and only value for this dispatch.** No heuristic override.

---

## § 3. Stratified Subsample Composition Design

**All choices committed below. Code will not begin until this section is complete.**

### 3.1 Committed choices

| Parameter | Choice | Reasoning |
|---|---|---|
| **min_cluster_size** | **10** | Conservative-density-leaning per dispatch §4. N≈10K is 5× smaller than N=48K; proportional scaling of 30 → 6; conservative padding to 10 (1.67× above proportional). Lower mcs → more clusters → better chance of meeting ≥50 acceptance threshold. Phase E-1.5 sensitivity sweep on {10, 15, 20, 30} queued post-acceptance. |
| **Floor formula** | **`min(available, min_cluster_size × 2)`** = **min(available, 20)** | 2× floor over 1× floor: density-based clustering needs margin above the resolution gate to produce stable cluster boundaries. 1× floor is just-above-threshold; 2× gives clearer-than-noise floor. |
| **N_target** | **10,000** | Per dispatch recommendation. Fits trivially in memory. Represents ~20.7% of the 48,430-row pool — representative without full-pool OOM risk. |
| **random_state** | **42** | Reproducibility commitment. |
| **D1 re-fire decision** | **Re-fire D1 in-memory; skip overwriting features.md** | D1 recomputation is required to build X (no on-disk feature matrix cache exists). features.md is already correct and identical for full-pool mode — skip overwrite. Document this choice here. |
| **D2 axes loader** | **Minimal PCA re-fire (k=3)** | `phase-E-1-axis-loadings.json` stores only top-20 loadings per axis, not full (160,) components vector. Cannot reconstruct axes_1_to_3 from JSON. Re-fire minimal TruncatedSVD(n_components=3) on full X_weighted. Same RANDOM_STATE=42 → bit-for-bit identical to on-disk D2 axes 1–3. ~5-8 seconds; acceptable. |
| **Bootstrap stability re-fire** | **Skip** | Full-pool 10-resample result already authoritative and in hand (Option-A §4 above). Subsample re-fire would add noise at lower N; would not strengthen the already-compelling case for k=3. |
| **Projections cache** | **Write `phase-E-1-projections-k3.npz`** | Enables D3-only re-fire in future iterations without recomputing D1+D2. Negligible size (~1.1 MB). |
| **psutil RSS-guard** | **Yes** | At HDBSCAN.fit entry. Logs RSS; raises if > 6 GiB (will not trigger at k=3; added as a discipline-compliant guard). |

### 3.2 Per-lineage subsample count table

The 48,430-row substrate has 14 distinct `cultural_lineage_canonical` values (per on-disk `phase-E-1-axis-discovery.md` and Option-A addendum §3):

| Lineage | Available (N) | Floor (min(available, 20)) | Prop. share of 9720 budget | **Final subsample count** | All ≥ mcs(10)? |
|---|---|---|---|---|---|
| fantasy_generic | 16,284 | 20 | 3,283 | **3,303** | ✓ |
| east_asian | 13,080 | 20 | 2,636 | **2,656** | ✓ |
| european | 12,515 | 20 | 2,522 | **2,542** | ✓ |
| unknown | 1,956 | 20 | 391 | **411** | ✓ |
| middle_eastern | 1,327 | 20 | 264 | **284** | ✓ |
| cross_cultural | 883 | 20 | 174 | **194** | ✓ |
| south_asian | 822 | 20 | 162 | **182** | ✓ |
| southeast_asian | 694 | 20 | 136 | **156** | ✓ |
| african | 465 | 20 | 90 | **110** | ✓ |
| south_american_indigenous | 197 | 20 | 36 | **56** | ✓ |
| mesoamerican | 83 | 20 | 13 | **33** | ✓ |
| arctic_circumpolar | 56 | 20 | 7 | **27** | ✓ |
| oceanic | 39 | 20 | 4 | **24** | ✓ |
| north_american_indigenous | 29 | 20 | 2 | **22** | ✓ |
| **TOTAL** | **48,430** | **280** | **9,720** | **10,000** | **14/14** |

**Computation notes:**
- Floors sum: 14 × 20 = 280
- Remaining budget: 10,000 − 280 = 9,720
- Remaining pool (post-floor): total 48,430 − 280 = 48,150 rows unselected
- Proportional shares computed as `round(9720 × lineage_remaining / 48150)`
- For each lineage, proportional allocation is capped by `available − floor` (cannot take more than available)
  - oceanic: only 19 rows remaining after floor (take 4 of 19 available — well within cap)
  - north_american_indigenous: only 9 rows remaining after floor (take 2 of 9 available — well within cap)
- Final total: 280 + 9720 = 10,000 ✓

**All 14 lineages ≥ min_cluster_size (10): VERIFIED ✓** (minimum: north_american_indigenous = 22)

### 3.3 Implementation algorithm

```
1. Group row indices by lineage (using actual DB cultural_lineage_canonical values).
2. For each lineage, sample min(available, 20) indices WITHOUT replacement using rng=np.random.RandomState(42).
3. Sum floor samples: 280 selected.
4. Compute remaining budget = 9720.
5. For each lineage, compute proportional_n = round(9720 × remaining_available[lineage] / total_remaining).
6. For each lineage, sample min(proportional_n, remaining_available[lineage]) additional indices WITHOUT replacement.
7. Adjust total to exactly 10000: if sum < 10000, add randomly from pool; if sum > 10000, remove randomly. (Rounding should give exactly 10000 per table above.)
```

Note: `cross_cultural` and `mesoamerican` appear in DB as actual `cultural_lineage_canonical` values despite not being in the `LINEAGE_VALUES` constant (which is used only for structured-feature one-hot encoding). The `compute_f2_weights` function already handles all actual DB values. The subsample computation must also use actual DB values (via `row[5]`), not LINEAGE_VALUES.

---

## § 4. min_cluster_size Choice for ~10K Subsample

**Committed choice: min_cluster_size = 10.**

| Option | Value | Interpretation | Cluster count direction |
|---|---|---|---|
| Proportional scaling | 6 | 30 × (10000/48430) | Baseline |
| **Conservative (chosen)** | **10** | ~1.67× above proportional | More clusters; lower minimum density requirement |
| Aggressive | 15 | 2.5× above proportional | Fewer clusters; higher minimum density requirement |
| Same as original | 30 | 5× above proportional | Very few clusters; almost certainly < 50 acceptance gate |

**Reasoning for 10:** Acceptance criterion requires ≥50 clusters. Lower min_cluster_size allows smaller density regions to crystallize into distinct clusters. Given 14 lineage buckets each contributing dozens to thousands of rows, and a 3-dimensional projection space that captures the substrate's primary variance axes, a min_cluster_size of 10 allows fine-grained cluster discovery without extreme fragmentation. The Phase E-1.5 sensitivity sweep on {10, 15, 20, 30} remains queued post-acceptance for robustness validation.

**Candidate Phase E-1.5 sweep values:** {10, 15, 20, 30} — queued, not executed in this dispatch.

---

## § 5. Bootstrap Stability at k=3 on Subsample (Optional — SKIPPED)

**Decision: Skip.**

The full-pool (N=48,430) bootstrap stability result is already in hand:
- Axis 1: 0.0011 (PASS — exceptionally stable)
- Axis 2: 0.0118 (PASS — very stable)
- Axis 3: 0.0131 (PASS — very stable)

All three are an order of magnitude below the 0.10 threshold. A subsample bootstrap (N=10K) would have higher variance (smaller N → wider bootstrap confidence intervals) and would not strengthen the case for k=3 beyond what is already empirically established. Including it would add ~2-3 minutes of compute with no information gain.

**Rationale for skipping per dispatch §B.5:** "Skip if your math-before-code shows it's unnecessary." The full-pool result is empirically established; subsample bootstrap is unnecessary.

---

## § 6. Bis-Disposition Criteria (Frame-Revision Specific)

The frame-revision reframes the bis-disposition criteria relative to prior dispatches. The correct criteria are those in dispatch §B.6:

| Condition | Disposition |
|---|---|
| ≥ 50 clusters AND mean per-lineage purity ≥ 0.70 | **Acceptance.** Phase E-2 proceeds. |
| 50 ≤ clusters < 100 AND purity 0.50–0.70 | **Partial acceptance.** Phase E-2 with merge-candidate review. |
| < 50 clusters OR purity < 0.50 | **Substrate-coverage bottleneck.** Alternative 2 (substrate expansion) is next. NOT cloud-bigger-HDBSCAN. |
| Pathological: clusters dominated by single-lineage shards | **Methodology re-review.** Surface to knight-rider (gandalf + jack-ryan). |

**Note on purity calculation in subsample context:** The acceptance criterion is evaluated on the full 48,430-row assignment (not just the subsample). Non-subsampled rows are assigned by nearest-centroid; their lineage distribution contributes to per-cluster purity. This is the correct measure for downstream Phase E-2 labeling quality.

**Per-lineage disposition documentation required in completion summary:** For each of the 14 lineages, document whether its rows primarily formed their own cluster(s), were absorbed into mixed clusters, or were assigned as nearest-centroid (for non-subsampled rows). Special attention to rare lineages: oceanic (39), arctic_circumpolar (56), north_american_indigenous (29), mesoamerican (83).

---

## Open Questions — Resolved

All 6 open questions from dispatch §"Open questions for legolas" are resolved above:

| # | Question | Resolution |
|---|---|---|
| 1 | Skip D1 re-fire or re-fire fresh? | Re-fire in-memory; skip overwriting features.md |
| 2 | Stratified subsample floor: mcs exactly or mcs × 2? | **mcs × 2 = 20** |
| 3 | min_cluster_size for ~10K subsample: 10, 15, 20? | **10** (conservative-density-leaning) |
| 4 | Optional bootstrap-stability re-fire on subsample axes 1-3? | **Skipped** — full-pool result authoritative |
| 5 | psutil RSS-guard at top of script? | **Yes** — added at HDBSCAN.fit entry |
| 6 | Cache `projections_k3` to disk? | **Yes** — `phase-E-1-projections-k3.npz` |

---

**Signed:** legolas
**Status:** Math-note addendum complete — `--mode subsample-k3` code implementation may proceed.
**RANDOM_STATE=42 reproducibility commitment confirmed.**
