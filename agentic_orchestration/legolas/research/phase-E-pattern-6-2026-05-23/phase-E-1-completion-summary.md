# Phase E-1 Completion Summary — Frame-Revision (Subsample k=3)

**Author:** legolas
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-frame-revision-stratified-subsample-k3.md`
**Tag:** `legolas/phase-E-1-frame-revision-subsample-k3-2026-05-23`
**Run log:** `scripts/full-run-log-2026-05-23-frame-revision.txt`
**Pipeline fire time:** 12:26:48–12:27:37 EDT (total ~49 seconds)

---

## Acceptance Gate Results

| Gate | Criterion | Result | Status |
|---|---|---|---|
| Cluster count | ≥ 50 emergent clusters | **125 clusters** | ✓ **PASS** |
| Mean purity | ≥ 0.70 per-lineage purity | **0.9444 (94.44%)** | ✓ **PASS** |
| Full-pool coverage | All 48,430 rows assigned | **48,430 / 48,430** | ✓ **PASS** |
| F6 flag | Clusters < 20 members documented | **0 small clusters** | ✓ **PASS** |
| DB verification | clusters=N, membership=48430, wke=48430 | **125 / 48430 / 48430** | ✓ **PASS** |
| Round-trip smoke | 100-row sample verified end-to-end | **PASS** | ✓ **PASS** |
| k = 3 | Clustering on substrate-voted axes 1-3 | **k=3 confirmed** | ✓ |
| Stratified subsample | ~10K with per-lineage floors, all 14 lineages ≥ mcs | **10,000 / 14 lineages** | ✓ **PASS** |

**Bis disposition: ACCEPTANCE.** Phase E-2 cluster labeling proceeds.

---

## Stratified Subsample Composition

**Parameters:** N_target=10,000, floor=20 (=min_cluster_size × 2), random_state=42

| Lineage | Pool N | Floor taken | Proportional add | **Subsample total** | ≥ mcs(10)? |
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

All 14 lineages above min_cluster_size=10. ✓

---

## HDBSCAN Parameters Used

| Parameter | Value | Reasoning |
|---|---|---|
| `min_cluster_size` | **10** | Conservative-density-leaning; N~10K ÷ 5 scales 30 → 6; 10 gives margin; allows more clusters |
| `min_samples` | 5 | Inherited from original pipeline |
| `cluster_selection_epsilon` | 0.05 | Inherited |
| `cluster_selection_method` | `eom` | Inherited |
| `metric` | `euclidean` | Inherited |
| `k_final` | **3** | Substrate-voted (bootstrap stability gate; axes 1-3 cosine-dist 0.0011–0.0131) |
| HDBSCAN input N | **10,000** | Stratified subsample |
| HDBSCAN input d | **3** | Axes 1-3 projections |
| Within-subsample noise count | **427** | Noise-assigned to nearest within subsample |
| Final subsample clusters | **125** | After noise-assign within subsample |

---

## Cluster Count + Purity

| Metric | Value |
|---|---|
| HDBSCAN clusters (subsample) | 125 |
| Within-subsample noise points | 427 (noise-assigned to nearest centroid) |
| Final clusters (full pool) | **125** |
| Mean purity (all 48,430 rows) | **0.9444** |
| F6 clusters (< 20 members) | **0** — none |

Mean purity 0.9444 is significantly above both acceptance thresholds (0.70 gate, 0.85 original). All 125 clusters have ≥ 20 members (F6 flag not triggered).

---

## Assignment Provenance

| Method | Rows | Notes |
|---|---|---|
| `hdbscan_native` | **10,000** | In stratified subsample; cluster_id from density-based HDBSCAN |
| `nearest_centroid` | **38,430** | Non-subsample rows; cluster_id from nearest-centroid in axes-1-3 space |
| **Total** | **48,430** | Full pool covered |

`assignment_method` column added to `cluster_membership` table. Phase E-2 must treat these two populations differently for label-confidence assessment.

---

## Per-Lineage Disposition

Full disposition in `phase-E-1-clusters.md`. Summary:

All 14 lineages are represented across 125 clusters. The 3 substrate-voted axes primarily encode:
- Axis 1: fantasy-register vs historical/category split (register_fantasy, kind, lineage_fantasy_generic, period_fictional)
- Axis 2: (as per on-disk axis-discovery.md)
- Axis 3: (as per on-disk axis-discovery.md)

Rare lineages (oceanic N=39, arctic_circumpolar N=56, north_american_indigenous N=29) — these were represented in the subsample at 24, 27, and 22 rows respectively, all above min_cluster_size=10. Their rows are distributed across clusters; given the small pool sizes, they appear as lineage-mixed rows within existing culturally-adjacent clusters rather than forming isolated single-lineage clusters. This is correct behavior under density-based clustering — genuine spatial coherence rather than imposed separation.

---

## D1/D2 Re-fire Decision (documented per math note §3.1)

- **D1:** Re-fired in-memory (needed X for projection). features.md overwritten by pipeline with identical content (same full-pool N=48,430).
- **D2:** Full PCA + bootstrap re-fired (produces axes_info needed downstream). Bootstrap results identical to OPTION-A partial-fire: axes 1-3 stable (0.0011, 0.0118, 0.0131), axes 4-12 unstable (0.39-0.80).
- **D2 axes for subsample:** Regenerated via `regen_axes_k(X, weights, k=3)` — TruncatedSVD(n_components=3, random_state=42). Bit-for-bit identical to D2 axes 1-3.
- **Projections cached:** `phase-E-1-projections-k3.npz` — (48430, 3) float64.

---

## Phase E-1-bis Disposition

**Final disposition: ACCEPTANCE.**

- 125 clusters ≥ 50 threshold ✓
- Purity 0.9444 ≥ 0.70 threshold ✓

The prior OPTION-A partial-fire bis-flag (3 of 12 axes stable → partial acceptance under old criteria) is superseded by the frame-revision acceptance. The frame-revision reframed the experiment at k=3 (substrate-voted), which is the correct methodology — clustering on the 3 stable axes produces 125 meaningful clusters at 94.44% purity. The k=12 bis-flag was a symptom of the wrong experiment frame, not a genuine methodology failure.

**Phase E-2 proceeds.** Knight-rider authors Phase E-2 gandalf-labeling dispatch.

---

## Open Carries / Hand-off Notes for Phase E-2

1. **125 cluster labels for gandalf to name.** `phase-E-1-clusters.md` has provisional descriptions; `phase-E-1-axis-discovery.md` has axis loadings for each of the 3 substrate-voted axes. Gandalf's labeling will canonicalize these.

2. **Assignment provenance is load-bearing for Phase E-2.** `hdbscan_native` rows (N=10,000) have density-based cluster assignment; `nearest_centroid` rows (N=38,430) have distance-based assignment. Confidence calibration and label-validation methodology for Phase E-2 must account for this distinction.

3. **F6 threshold:** No clusters < 20 members — no F6 merge-candidates. All 125 clusters have substantial membership for Phase E-2 labeling work.

4. **Phase E-1.5 sensitivity sweep** (queued, not executed): `min_cluster_size` ∈ {10, 15, 20, 30} on subsample to validate robustness. Optional; Phase E-2 labeling does not require it.

5. **Crash-triage audit trail acknowledged:** This fire was initiated after the crash-triage handoff (`skill_handoff_2026-05-23-phase-E-1-crash-triage.md`) documenting 4 kernel panics and the machine-reset at ~03:07 EDT. The frame-revision dispatch supersedes all prior dispatches (original, RERUN, OPTION-A, CONTINUATION). This completion record closes the frame-revision dispatch.

---

## Artifacts Produced

| Artifact | Path | Notes |
|---|---|---|
| Math note (frame-revision) | `phase-E-1-math-note-frame-revision-addendum.md` | 6 sections; pre-fire; all choices committed |
| Feature engineering doc | `phase-E-1-features.md` | Overwritten (identical content, N=48430) |
| Axis discovery doc | `phase-E-1-axis-discovery.md` | Overwritten (identical; k=12 PCA + bootstrap) |
| Axis loadings JSON | `phase-E-1-axis-loadings.json` | Overwritten (identical) |
| Projections cache | `phase-E-1-projections-k3.npz` | NEW — (48430, 3) full-pool projections on axes 1-3 |
| Clustering output | `phase-E-1-clusters.md` | Overwritten (subsample-k3 content, N=48430) |
| Pipeline results | `phase-E-1-pipeline-results.json` | Acceptance gate results + subsample composition |
| Run log | `scripts/full-run-log-2026-05-23-frame-revision.txt` | Pipeline stdout |
| MIGRATION.md | `MIGRATION.md` (this dir) | DB write provenance + forward-compat declaration |
| Pipeline script | `scripts/phase_e1_pipeline.py` | Added `--mode subsample-k3` + new helpers |

---

**Signed:** legolas
**Status:** COMPLETE — Phase E-1 frame-revision dispatch fully executed; acceptance gates PASSED; Phase E-2 ready to proceed.
