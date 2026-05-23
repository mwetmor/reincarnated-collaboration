# Phase E-1.5 Sensitivity Sweep Math Note

**Author:** legolas
**Date:** 2026-05-23
**Status:** PRE-FIRE — authored before pipeline code changes (Discipline #1 math-before-code)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-5-sensitivity-sweep-min-cluster-size.md`
**Anchors:**
- `phase-E-1-math-note-frame-revision-addendum.md` (baseline Phase E-1 memory projection; unchanged)
- `9-11-A-completion-summary.md` (fixed labeler; 100% alignment on 47 overrides)
- `phase-E-2-completion-summary.md` (gandalf Phase E-2 labels; override category breakdown)

All projections committed before code begins.

---

## § 1. Preflight: psutil RSS-Guard Activation + Memory Projection

### § 1.1 psutil install confirmation

Sub-carry 9.10-G.1 resolved in this dispatch.

```
pip install psutil
→ Successfully installed psutil-7.2.2
```

RSS guard verification:
```python
import psutil
psutil.Process().memory_info().rss  # → 0.014 GiB at interpreter baseline
```

**Guard status: ACTIVE.** The pipeline's `check_rss_guard()` function will now execute the `psutil.Process().memory_info().rss` branch rather than the "psutil not available" warning branch. This is the first actual execution of the guard after 3 prior cycles of deferral.

**Guard threshold:** 6 GiB (same as Phase E-1 frame-revision). Will log RSS at HDBSCAN.fit entry for each variant. If any variant exceeds 6 GiB, pipeline raises MemoryError and halts; surface to knight-rider for Alternative 2.

### § 1.2 Peak-memory projection per variant

All 4 variants run at the SAME N=10K subsample × d=3 projection space. Memory behavior is **invariant with `min_cluster_size`** — the mcs parameter controls cluster resolution gate, not the input data shape fed to HDBSCAN. Each variant's HDBSCAN processes the same (10000, 3) array.

Per Phase E-1 frame-revision math-note § 1 (authoritative baseline, unchanged):

| Object | Shape | Size estimate | Resident? |
|---|---|---|---|
| Python baseline (sklearn + numpy + hdbscan imports) | — | ~500 MB | always |
| Full-pool rows from DB | 48430 tuples | ~25 MB | yes through D1 |
| TF-IDF sparse matrix | (48430, 500) | ~20 MB | yes through LSA |
| LSA output dense | (48430, 100) | ~38.7 MB | yes through D2 |
| Structured feature block | (48430, 60) | ~23.2 MB | yes through D2 |
| Feature matrix X | (48430, 160) | ~62.0 MB | yes through projection |
| Full-pool projections_3 | (48430, 3) | ~1.2 MB | yes through assign |
| Subsample projections | (10000, 3) | ~240 KB | yes during HDBSCAN |
| HDBSCAN.fit on (10000, 3) | KD-tree + MST | ~5–50 MB peak | spike |
| Centroid matrix | (~100–150, 3) | ~40 KB | yes during assign |
| **Estimated peak** | | **~600–700 MB** | |

**mcs variation effect on memory:** NONE. The mcs parameter only changes which density peaks HDBSCAN recognizes as clusters. With a larger mcs, fewer clusters form, but the HDBSCAN internal data structures (KD-tree, MST, condensed tree) are proportional to N (the number of input points), not to the number of output clusters. All 4 variants process N=10K at d=3 → memory is effectively identical.

**Cheapest refuting test (Discipline #19):** `check_rss_guard()` logs actual RSS at HDBSCAN.fit entry for each variant. If any variant deviates materially (>50 MB difference), surface as anomaly. Expected: all 4 RSS readings within 10 MB of each other.

**Go/no-go: PROCEED for all 4 variants.** Peak is ~8-9% of 8 GiB available. No risk.

---

## § 2. Per-Variant Projections

The 4 sweep values are: mcs ∈ {10, 15, 20, 30}.

**Baseline for comparison:** mcs=10 → 125 clusters, purity=0.9444 (Phase E-1 frame-revision ACCEPTED).

### § 2.1 Cluster count direction

**Hypothesis:** cluster count is inversely correlated with mcs. Lower mcs = lower minimum density threshold = more (smaller) clusters; higher mcs = higher minimum density threshold = fewer (larger) clusters.

| mcs | Projected cluster count direction | Rationale |
|---|---|---|
| 10 (baseline) | 125 (known) | Phase E-1 frame-revision result |
| 15 | ~90–115 (fewer) | Higher resolution gate merges marginal small clusters |
| 20 | ~60–90 (fewer) | Many of the 125 sub-20-member clusters in baseline won't form; some 20-30 member clusters may merge |
| 30 | ~40–70 (fewest) | The original pre-frame-revision target; likely produces fewer than 50 clusters (recall: the whole point of choosing mcs=10 was to stay above the ≥50 acceptance threshold) |

**Note on mcs=30:** Per the Phase E-1 frame-revision math-note §4, mcs=30 was the pre-frame-revision target and was expected to produce very few clusters (acceptance threshold concern). The frame-revision dropped to mcs=10 specifically because the acceptance criterion requires ≥50 clusters. At mcs=30, the count may fall below 50 — this is expected and informative, not a failure of the sweep.

**Cheapest refuting test:** count unique cluster labels in final `all_labels` array for each variant. If mcs=20 produces MORE clusters than mcs=15, the inverse-correlation hypothesis is refuted for that pair.

### § 2.2 F6 floor interpretation at mcs≥20

The F6 criterion flags clusters with < 20 members as merge-candidates. At mcs=10, any cluster that forms has ≥10 members (the HDBSCAN minimum), so clusters can exist with 10-19 members → F6 flags them as merge-candidates.

At mcs=20, HDBSCAN requires ≥20 members to form a cluster. The F6 floor (< 20 members) becomes **equal to or below the resolution gate itself**. This means:

- At mcs=20: any cluster HDBSCAN forms natively has ≥20 members → F6 flag should trigger on ZERO native clusters (all native clusters satisfy F6 by construction).
- At mcs=30: same logic — all native clusters have ≥30 members → F6 (< 20) never triggers for native clusters.

**Interpretation choice:** At mcs≥20, the F6 flag as currently implemented (< 20 members) loses meaning as a "clustering-just-barely-formed-this" signal — it can only trigger on noise-assigned clusters or rounding artifacts. For this sweep's comparison report, I will note the F6 count per variant but flag that at mcs=20/30, F6 is **structurally zero or near-zero** by construction (not because quality improved, but because the gate is absorbed by the resolution parameter). A more informative signal at mcs=20/30 would be a scaled floor: `< 2 × mcs` — but this changes the criterion across variants, complicating comparison. Recommendation in report: use raw F6 count (< 20 members) for cross-variant comparison, with a footnote that at mcs=20/30 the floor is effectively satisfied by HDBSCAN design.

### § 2.3 Cluster 62 (Abyssal Bane Mega-Family) split behavior

**Cluster 62 profile (mcs=10 baseline):** N=4,807 (of 48,430 full pool), `fantasy_generic` / `fictional` / `fantasy` / `named_template`. Contains `Abyssal Bane Chakram`, `Abyssal Bane Knuckle Duster`, `Abyssal Bane [many weapon forms]` across weapon-form variation under the "Abyssal Bane" prefix. Flagged `fantasy_named_template_cross_form` + `phase_e15_split_candidate` by gandalf.

**Hypothesis:** Cluster 62 will NOT split via mcs variation alone.

**Reasoning:** Cluster 62 is N=4,807 — well above any mcs value in the sweep {10, 15, 20, 30}. Its bundling is axis-1-dominance-driven: the 3-axis PCA projection places all `fantasy_generic / fictional / named_template` items in a tight region of axis-1 space (axis 1 = kind_named_template dimension per Phase E-1 axis discovery). "Abyssal Bane Chakram" and "Abyssal Bane Knuckle Duster" are geometrically close to each other in 3-axis space because they share lineage (fantasy_generic), period (fictional), register (fantasy), and kind (named_template). Their weapon-form difference (chakram vs knuckle duster) is captured only in the 30-token multi-hot weapon-type dimensions of the structured feature block — a sparse, binary signal that contributes only marginally to the 160-dimensional feature space relative to the dominant categorical signals.

**Result of increasing mcs:** At mcs=15, 20, or 30, the density minimum required for a cluster to form is higher — meaning marginal small clusters near boundary regions dissolve, but large high-density clusters like Cluster 62 (N=4,807) remain intact, possibly absorbing the dissolved marginal clusters. Cluster 62's interior density is far above any tested mcs threshold.

**Prediction:** Cluster 62 equivalent appears in all 4 variants, with N≥4,807 at higher mcs values (absorbs previously-separate marginal clusters) and N≈4,807 at mcs=10 baseline.

**Cheapest refuting test:** after each variant run, identify the cluster with the highest count of "Abyssal Bane" top-reps. If NO such cluster exists at a given mcs (meaning Abyssal Bane rows scatter across multiple clusters), the hypothesis is refuted. If Cluster-62-equivalent at mcs=20 has N > 4,807, it absorbed additional rows (predicted).

**Cross-variant correspondence method:** Match Cluster 62 across variants by top-3 rep canonical_name overlap. The variant cluster that shares ≥2 of Cluster-62-mcs10's top-3 representative canonical names is the "corresponding" cluster at that variant. If no variant cluster shares ≥2 top-3 reps, use ≥1 top-5 rep overlap as fallback. Document this method for the comparison report.

### § 2.4 Form-bundling vs prefix-bundling distribution stability

From Phase E-2, gandalf identified:
- ~25 form-bundled clusters (Battleaxe family, Wand family, Shield family, etc.) — clusters where weapon-form is coherent across many name prefixes.
- 1 prefix-bundled cluster (Cluster 62 Abyssal Bane mega-family) — clusters where a single name prefix spans many weapon-forms.
- 13 clusters with `mixed_form_within_cluster` flag.

**Hypothesis:** The form-bundled vs prefix-bundled distinction is STABLE across mcs variants.

**Reasoning:** Form-bundled clusters (e.g., all battleaxes regardless of name prefix) form because the weapon-type multi-hot features (particularly `type_battleaxe`, `type_axe`) pull those items into a tight region of feature space. This is independent of mcs — the density of that region is determined by the substrate (how many battleaxe items exist and how similar they are), not by the mcs parameter. Similarly, prefix-bundled Cluster 62 is driven by the shared lineage/period/register/kind profile that makes all "Abyssal Bane X" items geometrically close regardless of weapon-form.

Increasing mcs from 10 to 20 will not split a 200-member battleaxe family into separate clusters because the interior density of the battleaxe region exceeds any mcs threshold tested. It may dissolve a 12-member boutique family (< mcs=20) into nearest-centroid assignment, reducing the total count of form-bundled clusters — but the dominant form-bundled clusters will persist.

**Prediction:** Form-bundled cluster count will DECREASE with increasing mcs (small form-bundled families dissolve below resolution gate), but the large ones persist. The form-bundled vs prefix-bundled structural pattern (∼25:1) will remain qualitatively stable.

**Cheapest refuting test:** For each variant, count clusters whose top-3 reps share the same weapon-form token (form-bundled) vs clusters where top-3 reps span multiple weapon-forms (form-heterogeneous). Compare to the mcs=10 baseline count of ~25 form-bundled. If mcs=20 shows significantly FEWER form-bundled clusters (not just smaller absolute count, but a different ratio), the stability hypothesis is weakened.

### § 2.5 Rare-lineage cluster emergence

Per Phase E-1 frame-revision math-note §3.2, the stratified subsample includes all rare lineages above the floor:

| Lineage | Subsample rows | Full-pool rows |
|---|---|---|
| oceanic | ~24 | 39 |
| north_american_indigenous | ~22 | 29 |
| arctic_circumpolar | ~27 | 56 |
| mesoamerican | ~33 | 83 |
| south_american_indigenous | ~56 | 197 |

These are the marginal lineages. Their subsample counts are close to or below the tested mcs values:

| Lineage | Subsample N | mcs=10 | mcs=15 | mcs=20 | mcs=30 |
|---|---|---|---|---|---|
| oceanic | ~24 | above (can cluster) | above (can cluster) | at threshold (barely) | BELOW (cannot form) |
| north_american_indigenous | ~22 | above | above | at threshold | BELOW |
| arctic_circumpolar | ~27 | above | above | above | BELOW |
| mesoamerican | ~33 | above | above | above | above |
| south_american_indigenous | ~56 | above | above | above | above |

**Key prediction:** At mcs=30, `oceanic` (N=~24 subsample) and `north_american_indigenous` (N=~22 subsample) fall BELOW the resolution gate. Their subsample items will NOT form native HDBSCAN clusters — they will be assigned via nearest_centroid to existing clusters. This means these two lineages' rows scatter across other clusters at mcs=30.

**Note on marginal-lineage tagging artifact (per `marginal-lineage-tagging-pattern-2026-05-23.md`):** The phase-E-1.5 sweep is a diagnostic: "does any tested mcs surface a culturally-coherent sub-cluster without re-tag?" Per §5 of the marginal-lineage meta-record, this sweep validates whether mcs variation alone (without substrate cleanup) can recover cultural-tradition cluster coherence. The expected answer is NO — the tagging artifact (Mode B/C/D content) dominates the axis-space positioning regardless of mcs threshold. A cultural-tradition cluster would require re-tag first. But we verify empirically.

**Prediction for rare-lineage coherent-home clusters:**
- mcs=10/15: oceanic, arctic, n.am.indigenous may form their OWN small clusters (since subsample N is above mcs). But given tagging artifact dominance (Mode B/C/D content), these "home clusters" are likely dominated by modern military hardware, not cultural-tradition items — consistent with mcs=10 baseline where Cluster 24 (arctic) was Russian/Swedish/French missile systems.
- mcs=20: oceanic (N~24) is at the resolution gate boundary; may or may not form a cluster depending on local density.
- mcs=30: oceanic and n.am.indigenous BELOW resolution gate — no native cluster formation.

**Cheapest refuting test:** For each variant, check whether any cluster has `dominant_lineage = 'oceanic'` or `dominant_lineage = 'north_american_indigenous'`. At mcs=10/15, expect YES (even if the cluster is Mode-B-dominated). At mcs=30, expect NO (these lineages scatter to nearest-centroid).

---

## § 3. Comparison Metrics

The cross-variant comparison report will compute and tabulate the following metrics for each variant {mcs=10, 15, 20, 30}:

1. **Cluster count** — total unique cluster labels in full-pool assignment
2. **Mean per-lineage purity** — `compute_purity()` over all 48,430 rows (same as Phase E-1 acceptance metric)
3. **F6 count** — clusters with < 20 members per variant (with footnote on F6 floor interpretation at mcs=20/30)
4. **Cluster-62-equivalent disposition** — N and split count for the "Abyssal Bane Mega-Family" cluster at each variant; correspondence confirmed via top-3 rep name overlap
5. **Form-bundled cluster count** — clusters where top-3 reps share the same weapon-form token (proxy for the ~25 form-bundled clusters in mcs=10 baseline)
6. **Prefix-bundled cluster count** — clusters where top-3 reps span multiple weapon-forms but share a name prefix (proxy for Cluster 62 pattern)
7. **Rare-lineage emergence** — per each of the 5 marginal lineages, does the variant produce a coherent home cluster? (any cluster with that lineage as dominant)
8. **9.13-A anomaly carry-over** — does `weapon_knowledge_entries.id=3` (Soviet PMD landmines) remain in an "European Uncurated-Period Spear Family" or equivalent anomalous cluster?
9. **Subsample composition stability** — verify `random_state=42` produces the same subsample indices across all 4 variants (mcs variation does not affect `build_stratified_subsample`'s index selection, only the HDBSCAN step downstream). If subsample composition differs, surface as anomaly.

---

## § 4. Discipline #19 Application — Cheapest Refuting Test per Hypothesis

| Hypothesis | Cheapest refuting test | Refutation criterion |
|---|---|---|
| Memory is ~600-700 MB for all variants | `check_rss_guard()` RSS log at HDBSCAN.fit entry; compare across 4 variant logs | If any variant RSS > 1 GiB at HDBSCAN.fit entry, hypothesis refuted; if variants differ by > 50 MB, surface as anomaly |
| Cluster count inversely correlated with mcs | Count unique labels in final assignment per variant | If any adjacent pair (mcs=10/15, 15/20, or 20/30) shows higher count at higher mcs, inverse-correlation hypothesis refuted for that pair |
| Cluster 62 does NOT split via mcs variation | Identify highest-count "Abyssal Bane" cluster per variant via top-3 rep overlap | If no single cluster at any mcs has ≥2 of the mcs=10 Cluster-62 top-3 reps, split hypothesis refuted (Cluster 62 fragments) |
| Form-bundling/prefix-bundling distribution is stable | Count form-bundled clusters per variant; compare to mcs=10 baseline ratio | If mcs=20 or mcs=30 shows a qualitatively different form-bundled:total ratio (not just fewer absolute clusters due to small-cluster dissolution), stability hypothesis weakened |
| Oceanic/n.am.indigenous below resolution gate at mcs=30 | Check `dominant_lineage` of all mcs=30 clusters | If any mcs=30 cluster has dominant_lineage='oceanic' or 'north_american_indigenous', the "below resolution gate" prediction is refuted |
| Rare-lineage clusters are Mode-B dominated | Inspect top-3 reps of any rare-lineage home cluster | If top-3 reps include Pre-Columbian/traditional cultural items rather than modern military hardware, tagging-artifact hypothesis partially weakened |
| Subsample composition stable across variants | Confirm `subsample_per_lineage` counts identical across all 4 runs | Any difference in subsample composition → surface as anomaly; would require re-evaluation of cross-variant comparability |

---

## § 5. Open Questions Resolved

| Question | Resolution |
|---|---|
| F6 floor interpretation at mcs=20/30 | Use raw < 20 members for consistency; footnote that at mcs=20/30 it is structurally satisfied by HDBSCAN design. A scaled alternative `< 2 × mcs` would be more informative but complicates comparison. Use raw; document. |
| Cross-variant cluster identity correspondence | Match by top-3 rep canonical_name overlap (≥2 shared = correspondence); fallback to top-5 with ≥1. Document per-variant in comparison report. |
| Comparison report format | Both markdown (human read) and JSON (programmatic). Markdown at `phase-E-1-5-sensitivity-sweep-comparison-report.md`; JSON at `phase-E-1-5-sensitivity-sweep-comparison-report.json`. |
| Rare-lineage distribution per variant | Documented in § 2.5; inspected in comparison report per lineage × variant cell. |
| Subsample composition stability | Verified by comparing `subsample_per_lineage` dict across all 4 variant log outputs. |

---

## § 6. Pipeline Code Changes Required

Per dispatch § D:

1. **`--no-db-writes` flag** — default `False` (preserves existing behavior). When `True`, skip `populate_db_with_provenance()` entirely. Also skip the round-trip smoke (smoke requires DB state). Log "DB writes: DISABLED (--no-db-writes flag active)" at pipeline start when flag is set.

2. **`--variant-tag <string>` flag** — default: empty string (existing behavior; output files use standard names). When set (e.g., `--variant-tag mcs10`), suffix output artifact filenames: `phase-E-1-clusters-mcs10.md` instead of `phase-E-1-clusters.md`, `phase-E-1-pipeline-results-mcs10.json` instead of `phase-E-1-pipeline-results.json`. The axis discovery + features.md files are NOT tagged (they are shared across variants; identical per run). The per-variant outputs are: clusters.md + pipeline-results.json.

   Additionally, for the sweep comparison, each variant should write a **per-variant summary JSON** at `phase-E-1-5-mcs<N>-results.json` containing: mcs, cluster count, purity, F6 count, and per-lineage dominant cluster mapping.

3. **Implementation locations:**
   - `argparse` section in `main()` — add both flags
   - `subsample_mode` branch in `main()` — add skip block for `populate_db_with_provenance()` + smoke when `--no-db-writes` is set
   - `write_clusters_subsample()` call site — pass variant-tagged output filename when `--variant-tag` is set
   - Results JSON path — append variant tag when set

**Code change is < 50 lines per dispatch requirement. No methodology change.**

---

**Signed:** legolas
**Status:** Math-note complete — pipeline code changes + sweep execution may proceed.
**RANDOM_STATE=42 reproducibility commitment confirmed (subsample stratification is mcs-independent).**
