# A/B Comparison Protocol — Cycle 14 Close (Option α Substrate-Led Emergence vs Doc 48 Pre-Authored Baseline)

> **STATUS:** CURRENT — protocol authored, awaiting Wave 5 production-season output to execute. Fires at Wave 5 close after the canonical-promoted production season passes the audit-gate. Consumes Wave 5 ExportFactionCluster + ExportFactionRelationship + kit_archive + phase7_kit_verdict_log + phase7_cluster_aggregate_log output and compares against doc 48 VESTIGIAL baseline.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 pre-ratification #3 (6 measurement dimensions LOCKED verbatim) + KR dispatch `2026-05-27-gandalf-ab-comparison-protocol-wave-5-close.md`
**Companion docs:**
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — VESTIGIAL doc 48; the A baseline (10 candidate archetype-shapes; § 1 table; § 3.1 BC-axis coverage; § 4.1 substrate-anchoring table)
- `canonical/00-ground-state.md` — no-classes architectural recommitment
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` — Sketch F + Q2 D-Sharpened theoretical framework (§ 2 G-B + § 3 F-C specs)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` § 5 (risk register; new risk additions appended here)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` lines 563-832 — `ExportFactionCluster` + `ExportFactionRelationship` + `RELATIONSHIP_TYPE_ENUM` schemas
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_db.py` lines 73-205 — `phase7_kit_verdict_log` + `phase7_cluster_aggregate_log` DDL
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Disciplines #11 + #41 + #43 + #45
- `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` — Phase 7 joint-gate design spec (HELD verdict logging cross-reference)

---

## 0. TL;DR

Six measurement dimensions, each with operational definition + measurement procedure + acceptance criterion + drift-watch criterion + empirical data source. The protocol resolves a single decision: **does Option α (substrate-led emergence, Wave 5 production season) produce a generative-architecture output equal to or better than the doc 48 designer-curated baseline?** Each dimension renders a verdict; the dimensions together render a composite verdict (A passes / B passes / inconclusive).

**Composite verdict semantics:**

- **B-PASS** — Option α produces (a) ≥80% archetype-shape coverage of doc 48 baseline, (b) substrate-anchor distribution within target band, (c) high-distance faction pair separation, (d) personage-convergence signal consistent with substrate-anchored Sketch F architecture, (e) at least one surprise emergence beyond doc 48, (f) ≤15% throwaway clusters. Option α ratified for v1.
- **A-PASS** — doc 48 baseline meaningfully outperforms Option α on coverage + anchor distribution; Option α should be revisited or augmented before v1 lock.
- **INCONCLUSIVE** — sample size at Wave 5 (n=22-40 kits; 1 production season) insufficient to resolve. Defer composite verdict to Cycle 15 with k=3-5 production-season replication; render per-dimension verdicts only.

**Critical framing:** doc 48 baseline is **COMPARISON** not **PRESCRIPTION** (Discipline #41). The protocol does not validate Option α by asking "did it reproduce doc 48?" That would invert the substrate-led commitment. The protocol asks "did substrate-led emergence produce coverage at least as broad as a designer would have produced, with novel emergence signal beyond what a designer would have anticipated?" Coverage parity + surprise-emergence are co-conditions for B-PASS.

---

## 1. Composition with Phase 7 HELD verdict logging (Discipline #43 audit data feed)

Phase 7 IMPL (gamora `eca0aa5`) emits per-kit verdict records to `phase7_kit_verdict_log` and per-cluster aggregate records to `phase7_cluster_aggregate_log`. Both tables are LOAD-BEARING substrate for the A/B comparison protocol — they provide the per-kit + per-cluster verdict granularity required for dim #1 (archetype coverage), dim #2 (substrate-anchor distribution), dim #5 (surprise emergence), dim #6 (throwaway clusters).

**Data flow at Wave 5 close:**

```
Wave 5 production season fires
  → kit_archive populated (Phase 4 ACTIVE/DOMINATED/EVICTED kits)
  → PM-1 clustering (rocket a466eb1) produces faction clusters
  → G-B primary-pair selection populates ExportFactionCluster.primary_pair_flag + pairwise_distance_distribution
  → Phase 5 PM-2 LLM (or placeholder under faction_visibility=invisible) populates faction_label_canonical
  → Phase 5 F-C produces ExportFactionRelationship records (k=3 → 3 rows; k=4 → 6 rows)
  → Phase 7 2-layer joint-gate evaluates each kit (gamora eca0aa5)
  → phase7_kit_verdict_log emits per-kit verdict row (SHIPPED-WORTHY / HELD-cohesion-fail-C1/2/3 / HELD-mechanical-fail-archive/floor/band / HELD-both-fail)
  → phase7_cluster_aggregate_log emits per-cluster aggregate row
  → audit-gate PASS gates canonical-promotion of production season
  → gandalf design-quality audit fires (Discipline #43; A1-A5 questions)
  → A/B comparison protocol executes (this doc)
```

**Per-dimension data source mapping:**

| Dim | Primary data source | Secondary data source |
|---|---|---|
| #1 Archetype coverage | `kit_archive` ACTIVE kits + `phase7_kit_verdict_log` SHIPPED-WORTHY filter | `ExportFactionCluster` cluster centroids |
| #2 Substrate-anchor distribution | `ExportFactionCluster.substrate_anchored_personages` field | `kit_archive` substrate-anchor metadata (analytics-only per D-Sharpened) |
| #3 Faction pairwise-distance distribution | `ExportFactionCluster.pairwise_distance_distribution` field | `ExportFactionRelationship.pairwise_distance` per pair |
| #4 Personage convergence test | `kit_archive` substrate-anchor metadata + kit BC-axis position | `ExportFactionCluster.substrate_anchored_personages` per cluster |
| #5 Surprise-emergence count | `phase7_kit_verdict_log` SHIPPED-WORTHY kits + doc 48 § 1 archetype-shape list | `ExportFactionCluster` cluster identity vs doc 48 anchoring table § 4.1 |
| #6 Throwaway-cluster count | `phase7_cluster_aggregate_log.member_kit_count` + `cluster_compactness` + `held_cohesion_fail_count` | `ExportFactionCluster.cluster_compactness` |

**Discipline #43 audit composition:** all 6 dimensions feed gandalf's wave-close A4 (substrate-led architectural composition) + A2 (pre-authored taxonomy introduction check). A B-PASS verdict from this protocol supports a Discipline #43 PASS verdict at Wave 5 close. An A-PASS verdict from this protocol triggers DRIFT-DETECTED escalation to Matt as Pattern B engagement (Option α did not deliver; revisit substrate-led commitment OR revisit Option α impl).

---

## 2. Sample size + statistical power preamble

**Wave 5 produces 1 production season:** ~22-40 kits surviving Phase 4 eviction; 3-4 emergent faction clusters; 3-6 inter-faction relationship records.

**Implications for statistical methodology:**
- All per-kit dimensions (#1, #5) operate on n=22-40 — small-n; use exact methods (Fisher's exact, exact binomial) over asymptotic methods (chi-squared, z-test).
- All per-cluster dimensions (#2, #6) operate on n=3-4 — too small for meaningful distribution-fitting; descriptive statistics + threshold tests only.
- Per-pair dimension (#3) operates on n=3-6 pairwise distances — descriptive + ranking test (Wilcoxon signed-rank if comparing distributions) NOT t-test.
- Personage-convergence test (#4) is the highest-stakes inference — requires Bayesian posterior method to honestly represent uncertainty at small-n (Q-AB-1 resolution below).

**Cycle 15 power expansion:** if Wave 5 sample size cannot resolve dim #4 (low Bayes factor), defer composite verdict + replicate at k=3-5 production seasons in Cycle 15 (pooled n=66-200 kits; gain power). The protocol explicitly supports per-dimension verdicts while withholding composite verdict (INCONCLUSIVE) at Wave 5 if dim #4 underpowered.

---
