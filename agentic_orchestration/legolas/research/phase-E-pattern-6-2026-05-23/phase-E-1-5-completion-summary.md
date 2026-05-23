# Phase E-1.5 Completion Summary — Sensitivity Sweep (min_cluster_size ∈ {10, 15, 20, 30})

**Author:** legolas
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-5-sensitivity-sweep-min-cluster-size.md`
**Tag:** `legolas/phase-E-1-5-sensitivity-sweep-2026-05-23` (local only; seam-prefix per ADR-001)

---

## Execution Summary

**4 sweep variants executed without panic.** All acceptance criteria met.

| Variant | Cluster count | Purity | F6 count | DB writes | Status |
|---|---|---|---|---|---|
| mcs=10 | 125 | 0.9444 | 0 | OFF | ACCEPTANCE |
| mcs=15 | 103 | 0.9412 | 0 | OFF | ACCEPTANCE |
| mcs=20 | 85 | 0.9287 | 0 | OFF | ACCEPTANCE |
| mcs=30 | 65 | 0.9177 | 0 | OFF | ACCEPTANCE |

**Preflight confirmation:**
- `pip install psutil` → psutil 7.2.2 installed (sub-carry 9.10-G.1 RESOLVED)
- RSS guard: active and confirmed (0.014 GiB at baseline interpreter; 1.11–1.14 GiB at HDBSCAN.fit — well under 6 GiB threshold)
- Production DB (Phase E-2-DB canonical labels at mcs=10): **VERIFIED UNCHANGED** post-sweep (clusters=125, membership=48,430, id=3 → cluster_id=116 "European Uncurated-Period Spear Family" intact)

**Pipeline additions (dispatch § D):**
- `--no-db-writes` flag: added; skips `populate_db_with_provenance()` + round-trip smoke; logs "DB writes: DISABLED" at pipeline start
- `--variant-tag <str>` flag: added; suffixes `phase-E-1-clusters-<tag>.md` + `phase-E-1-pipeline-results-<tag>.json` for each variant
- `write_clusters_subsample()` updated to accept `variant_tag=` parameter
- Results JSON now includes full `cluster_characterization` dict per variant (enables downstream programmatic analysis)

---

## Hypothesis Verdicts Table

| Hypothesis | Prediction | Result | Verdict |
|---|---|---|---|
| Memory invariant across variants | ~600-700 MB (+ ~500 MB Python baseline = ~1.1 GiB) | 1.11–1.14 GiB at HDBSCAN.fit; < 30 MB spread | CONFIRMED |
| Cluster count inversely correlated with mcs | mcs↑ → clusters↓ for all pairs | 125 → 103 → 85 → 65 (strictly decreasing) | CONFIRMED |
| Cluster 62 does NOT split via mcs variation | N=4,807 persists; no weapon-form split | mcs=10/15/20 N=4,807; mcs=30 N=4,992 (GREW, absorbed marginals); NO split at any mcs | CONFIRMED |
| Form-bundling/prefix-bundling ratio stable | ~25:1 form-bundled:prefix-bundled persists | 48% → 48% → 46% → 38% form-bundled; qualitative stability holds through mcs=20, mild erosion at mcs=30 | CONFIRMED (qualified) |
| Oceanic/n.am.indigenous below resolution gate at mcs=30 | No home cluster at mcs=30 | No home cluster at ANY mcs tested (even mcs=10) | CONFIRMED AND EXTENDED |
| Rare-lineage home clusters are Mode-B dominated | Modern military hardware, not cultural-tradition items | arctic cluster = Russian/Swedish missile systems; south_am cluster = Chilean military + Apache missile | CONFIRMED |
| Subsample composition stable across variants | Same composition regardless of mcs | REFUTED — floor=mcs×2 causes subsample to vary; arctic: 27 → 56 rows from mcs=10 to mcs=30 | REFUTED (design artifact) |

---

## Cluster 62 Split Behavior (Abyssal Bane Mega-Family)

**Result: NO SPLIT at any tested mcs value.**

| mcs | Cluster-62-equiv | N | Top reps (sample) |
|---|---|---|---|
| 10 | Cluster 62 | 4,807 | Abyssal Bane Chakram (v.rare), Abyssal Bane Knuckle Duster (rare + v.rare) |
| 15 | Cluster 40 | 4,807 | Abyssal Bane Chakram (v.rare), Abyssal Bane Knuckle Duster (rare + v.rare) |
| 20 | Cluster 34 | 4,807 | Abyssal Bane Chakram (v.rare), Abyssal Bane Knuckle Duster (rare + v.rare) |
| 30 | Cluster 29 | **4,992** (+185) | Abyssal Bane Chakram (v.rare), Abyssal Bane Knuckle Duster (v.rare), Abyssal Bane Maul (rare) |

Cluster 62 is stable across mcs=10/15/20 at N=4,807. At mcs=30, it grows by 185 rows (absorbs adjacent marginal clusters). Its weapon-form bundling (chakram, knuckle duster, maul, etc. under "Abyssal Bane" prefix) is driven by axis-1 dominance (kind_named_template + fantasy_generic), not cluster density. Splitting requires additional PCA axes or a targeted sub-clustering pass — both out of scope for mcs variation.

**Correspondence method used:** top-3 rep canonical_name overlap (≥2 shared = match). Applied successfully — "Abyssal Bane Chakram (very rare variant)" appears as top-1 rep in mcs=10/15/20/30 equivalents; "Abyssal Bane Knuckle Duster (rare variant)" appears as top-2 in three of four.

---

## Form-Bundling vs Prefix-Bundling Robustness Verdict

**Form-bundling vs prefix-bundling distribution is ROBUST across mcs ∈ {10, 15, 20} and mildly erodes at mcs=30.**

| mcs | Form-bundled clusters | Total clusters | Form-bundled ratio | Prefix-bundled clusters |
|---|---|---|---|---|
| 10 | 61 | 125 | 48.8% | 1 (Cluster 62) |
| 15 | 49 | 103 | 47.6% | 1 |
| 20 | 39 | 85 | 45.9% | 1 |
| 30 | 25 | 65 | 38.5% | 1 |

The prefix-bundled mega-family (Cluster 62 equivalent) is a singleton across all variants. The form-bundled cluster ratio is stable at ~46-49% for mcs=10/15/20, dropping to 38.5% at mcs=30. The drop at mcs=30 reflects small form-bundled families (boutique weapon types with N < 30 subsample rows) dissolving below the resolution gate — the large dominant form-bundled families (Battleaxe, Wand, Dagger, Staff, Longsword, Halberd, etc.) persist at all tested mcs values.

---

## Rare-Lineage Outcomes

| Lineage | Full-pool N | Home cluster at any mcs? | Mode-B dominated? |
|---|---|---|---|
| oceanic | 39 | NO (none at mcs=10, 15, 20, 30) | N/A — no cluster |
| north_american_indigenous | 29 | NO (none at mcs=10, 15, 20, 30) | N/A — no cluster |
| arctic_circumpolar | 56 | YES at mcs=10, 15; NO at mcs=20, 30 | YES — Russian/Swedish missile systems |
| mesoamerican | 83 | NO (none at mcs=10, 15, 20, 30) | N/A — no cluster |
| south_american_indigenous | 197 | YES at mcs=10, 15, 20; NO at mcs=30 | YES — Chilean military arms + Apache missile |

**Key finding:** No mcs value in the tested range reveals a culturally-coherent Mode-A cluster for any of the 5 marginal lineages. This empirically validates the marginal-lineage tagging pattern meta-record's thesis that mcs parameter variation alone cannot substitute for substrate re-tag (9.11-D → 9.11-E). The corrective path is upstream substrate cleanup, not clustering parameter tuning.

**Note on subsample floor coupling:** Arctic_circumpolar loses its home cluster at mcs=20 partly because the subsample floor grows (all 56 rows in subsample at mcs=30 but STILL no cluster — this is a STRONGER null result: even with all arctic rows available for HDBSCAN, the Mode-B military hardware content scatters across axis space and doesn't form a coherent density peak).

---

## 9.13-A Anomaly Carry-Over Status

**Status: PERSISTS structurally across all 4 variants.**

`weapon_knowledge_entries.id=3` (PMD series mines; european / unknown period) falls into the "European/unknown" cluster at each mcs value. The top reps for this cluster are identical across all variants: GYATA-64 mine, Round shield, M111 grenade. This is a highly stable structural cluster driven by the `european × unknown_period` axis interaction.

The anomaly label ("European Uncurated-Period Spear Family" in the production DB) is a Phase E-2 gandalf canonical-labeling artifact — the provisional description was correctly "european unknown mixed weapons" but the canonical label override introduced "Spear Family" language. The structure of PMD mines → this cluster is not a clustering error; it is a substrate-tagging consequence (all uncurated european/unknown-period items cluster together regardless of weapon type). Noted for elrond's 9.11-D review.

**Production DB verification post-sweep:**
- `clusters`: 125 (unchanged)
- `cluster_membership`: 48,430 (unchanged)
- `weapon_knowledge_entries.cluster_id` populated: 48,430 (unchanged)
- id=3 → cluster_id=116 "European Uncurated-Period Spear Family" (unchanged)

---

## Acceptance Criteria Verification

| Criterion | Status |
|---|---|
| psutil installed + RSS-guard active | PASS — psutil 7.2.2; RSS 1.11-1.14 GiB (< 6 GiB at all fires) |
| 4 sweep variants executed without panic | PASS — all 4 fired; ~60-65 sec each; no OOM; no panic |
| Per-variant artifacts on disk with distinct filenames | PASS — `phase-E-1-clusters-mcs{10,15,20,30}.md` + `phase-E-1-pipeline-results-mcs{10,15,20,30}.json` |
| No DB writes — production state preserved | PASS — `--no-db-writes` active; production DB state verified unchanged |
| Comparison report authored | PASS — `phase-E-1-5-sensitivity-sweep-comparison-report.md` + companion JSON |
| Cluster 62 split behavior documented | PASS — NO split at any mcs; documented with N per variant |
| Form-bundling vs prefix-bundling distribution compared | PASS — ratio stable through mcs=20; mild erosion at mcs=30 |
| Rare-lineage outcomes documented | PASS — per-lineage × per-mcs table above |
| Discipline #19 — cheapest refuting test per hypothesis | PASS — each hypothesis tested with minimum empirical check; 1 refutation (subsample stability) identified |
| Completion summary + tag | PASS |

---

## HM-Prep Arc Impact

With Phase E-1.5 complete:
- **HM-prep 3 (weapon substrate work):** advances further toward closure. Outstanding items are 9.11-D (elrond substrate-tagging-artifact review) and 9.11-E (elrond cultural-vs-geographic re-tag). These are elrond dispatches.
- **Phase E-1.5 findings directly input to elrond's 9.11-D:** the European/unknown cluster structure (GYATA-64 mine / Round shield / M111 grenade top reps) is concrete evidence for the tagging-artifact review.
- **Phase E-2-DB canonical state:** preserved. mcs=10 remains the production-authoritative clustering.
- **No re-labeling warranted** unless substrate changes from 9.11-D/9.11-E meaningfully alter axis space. If re-labeling is commissioned, mcs=10 or mcs=15 are the data-supported options.

---

## Artifacts Produced

| Artifact | Path |
|---|---|
| Math note (Discipline #1) | `phase-E-1-5-sensitivity-sweep-math-note.md` |
| Per-variant clusters (mcs=10) | `phase-E-1-clusters-mcs10.md` |
| Per-variant results JSON (mcs=10) | `phase-E-1-pipeline-results-mcs10.json` |
| Per-variant clusters (mcs=15) | `phase-E-1-clusters-mcs15.md` |
| Per-variant results JSON (mcs=15) | `phase-E-1-pipeline-results-mcs15.json` |
| Per-variant clusters (mcs=20) | `phase-E-1-clusters-mcs20.md` |
| Per-variant results JSON (mcs=20) | `phase-E-1-pipeline-results-mcs20.json` |
| Per-variant clusters (mcs=30) | `phase-E-1-clusters-mcs30.md` |
| Per-variant results JSON (mcs=30) | `phase-E-1-pipeline-results-mcs30.json` |
| Cross-variant comparison report (MD) | `phase-E-1-5-sensitivity-sweep-comparison-report.md` |
| Cross-variant comparison report (JSON) | `phase-E-1-5-sensitivity-sweep-comparison-report.json` |
| Run logs (4 variants) | `scripts/full-run-log-2026-05-23-phase-E-1-5-mcs{10,15,20,30}.txt` |
| Completion summary | `phase-E-1-5-completion-summary.md` (this file) |

All artifacts at: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/`

---

**Cross-references:**
- Dispatch: `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-5-sensitivity-sweep-min-cluster-size.md`
- Math note: `phase-E-1-5-sensitivity-sweep-math-note.md` (this directory)
- Comparison report: `phase-E-1-5-sensitivity-sweep-comparison-report.md` (this directory)
- 9.11-A completion summary: `9-11-A-completion-summary.md` (this directory)
- Phase E-2 completion summary: `phase-E-2-completion-summary.md` (this directory)
- Marginal-lineage meta-record: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Phase E-1 math-note (frame-revision): `phase-E-1-math-note-frame-revision-addendum.md` (this directory)
- Discipline #1 (math-before-code), Discipline #18 (substrate-voting-is-binding), Discipline #19 (forensic-conclusion-discipline)
- ADR-001 (tag protocol; seam-prefix LOCAL ONLY)

---

**Signed:** legolas
**Status:** Phase E-1.5 sensitivity sweep COMPLETE. All acceptance criteria PASSED. Production DB state preserved. Tag cut.
