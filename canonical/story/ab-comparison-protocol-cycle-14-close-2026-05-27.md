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

## 3. Dimension #1 — Archetype shape coverage

### 3.1 Operational definition

**Question this dimension answers:** of the 10 candidate archetype-shapes that designer-curation produced in doc 48 (Barbarian / Hoplite / Siege-Master / Assassin / Duelist / Wildhunter / Gunslinger / Skirmisher / Magus / Crusader), how many emerge as recognizable shape-clusters in Wave 5 substrate-led output?

**"Recognizable shape-cluster" means** an emergent grouping of SHIPPED-WORTHY kits whose modal BC-axis signature is within similarity-threshold distance of a doc 48 archetype's BC-axis signature (doc 48 § 3.1 coverage matrix lines 289-298). The similarity-threshold operates on 8 BC axes; match = ≥6 of 8 axes agree (exact or adjacent bin).

**Non-question this dimension does NOT answer:** "did Option α name its emergent clusters with doc 48 vocabulary?" Naming is not the test — Phase 5 PM-2 LLM produces names from substrate evidence, and they SHOULD differ from doc 48 labels. The test is shape (BC-axis signature) match, not label match.

**Discipline #41 framing:** doc 48 baseline is COMPARISON not PRESCRIPTION. A doc 48 archetype that does NOT emerge in Wave 5 is not automatically a Wave 5 failure — it may be a substrate signal that the doc 48 archetype was over-anticipated. The protocol flags non-emergence; the design call on whether non-emergence is failure or insight belongs to gandalf design-quality audit + Matt review.

### 3.2 Measurement procedure

**Step 1 — Extract doc 48 BC-axis signature per archetype (one-time setup).** From doc 48 § 3.1 (lines 289-298), encode each archetype's BC-axis signature as an 8-tuple over the 8 BC axes per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`:

```
doc48_archetypes = {
    "Barbarian":    (engagement="close-fast", damage_geometry="small-AOE",
                     proxy_density="solo", control_density="damage-pure",
                     damage_tempo="medium", amplitude_variance="variable",
                     defensive_profile="tank", resource_economy="charge-stack"),
    "Hoplite":      (engagement="mid-slow", damage_geometry="small-AOE",
                     proxy_density="solo", control_density="mixed",
                     damage_tempo="low", amplitude_variance="flat",
                     defensive_profile="mitigator", resource_economy="steady"),
    # ... (encode all 10 per doc 48 § 3.1)
}
```

Encoded as test fixture in measurement script; reviewed by gandalf at protocol-execution time for fidelity to doc 48.

**Step 2 — Extract Wave 5 SHIPPED-WORTHY kit BC-axis signatures.** Query:

```sql
SELECT k.kit_id, k.bc_cell_id, k.q1, k.q2, k.q3, k.q4, k.q5,
       v.verdict, v.cluster_id, v.cohort
FROM kit_archive k
JOIN phase7_kit_verdict_log v ON v.kit_id = k.kit_id
WHERE v.season_id = :wave_5_season_id
  AND v.verdict = 'SHIPPED-WORTHY'
  AND k.archive_status = 'ACTIVE';
```

Decode `bc_cell_id` to 8-tuple via existing engine `bc_cell_decode()` per BC-axes-lock spec.

**Step 3 — Compute per-archetype shape-match.** For each doc 48 archetype A and each SHIPPED-WORTHY kit K:
- Compute axis-agreement count: `agree(A, K) = sum(A.axis[i] == K.axis[i] OR adjacent(A.axis[i], K.axis[i]) for i in 1..8)`
- Adjacent means immediately adjacent bin in BC-axes-lock bin ordering (e.g., `close-fast` adjacent to `close-medium` and `mid-fast`).
- Match: `agree(A, K) >= 6` (≥6 of 8 axes agree).

**Step 4 — Per-archetype emergence verdict.** Archetype A emerges in Wave 5 iff at least 2 SHIPPED-WORTHY kits match A. (Floor of 2 prevents single-kit-noise from counting; see Discipline #11 empirical-inspection — single-kit signal under small-n is not yet evidence of pattern.)

**Step 5 — Coverage tally.** `coverage_count = sum(1 for A in doc48_archetypes if A emerges)`. `coverage_rate = coverage_count / 10`.

### 3.3 Acceptance criterion

| Coverage rate | Verdict | Rationale |
|---|---|---|
| ≥0.80 (≥8 of 10) | B-PASS dim #1 | Substrate-led emergence reproduces broad designer-anticipated coverage |
| 0.60-0.79 (6-7 of 10) | INCONCLUSIVE dim #1 | Partial coverage; non-emergence pattern requires gandalf interpretation (was missing archetype substrate-empty per doc 48 § 3.2 — substrate signal vs. Option α gap?) |
| <0.60 (≤5 of 10) | A-PASS dim #1 | Substrate-led emergence under-produces vs designer-anticipated coverage; Option α impl or substrate enrichment needed |

**Why ≥0.80 threshold:** doc 48 § 3.2 already documents 9 BC-cell gaps DEFERRED to v1.1 (substrate-empty cells). Of the 10 doc 48 archetypes, 8 are anchored to substrate clusters ≥27 named rows (per doc 48 § 4.1); 2 are anchored to ≥149 rows. Reasonable expectation: substrate-led emergence in a single production season reproduces ≥8 of 10 IF Option α is delivering. Falling to 6-7 of 10 suggests Option α is either under-emerging OR substrate-signal-is-thinner-than-doc-48-anticipated (the second is the more interesting finding).

**Why ≤0.60 (≤5 of 10) is A-PASS:** if substrate-led emergence cannot reproduce even half of designer-anticipated archetype-shapes from substrate that explicitly anchors them (doc 48 § 4.1 anchoring table), Option α is not delivering on the substrate-led promise — either the clustering algorithm is mis-tuned (PM-1 GMM k∈{3,4} too coarse) OR the Phase 4 eviction is over-filtering. Routes to PM-1 + Phase 4 architectural re-review.

### 3.4 Drift-watch criterion (Cycle 15+ revisit trigger)

- **DRIFT TRIGGER:** if coverage_rate at Cycle 15+ replication drops below Wave 5 verdict band (e.g., Wave 5 was 0.85 B-PASS; Cycle 15 drops to 0.55 A-PASS), substrate enrichment commissions (Q-S2-12 INT-AoE / Q-S2-13 named-pool re-tagging / Q-S2-14 hybrid-attribute) need re-prioritization.
- **DRIFT TRIGGER:** if a specific archetype (e.g., Crusader) emerges at Wave 5 but disappears at Cycle 15+, Phase 5 cohesion-judge calibration may have shifted; check `phase7_kit_verdict_log` HELD-cohesion-fail-C1/C2/C3 distribution for the missing archetype's BC-cell.
- **DRIFT TRIGGER:** if a NEW doc-48-shape archetype emerges at Cycle 15+ that did NOT emerge at Wave 5, this is positive drift (substrate signal sharpening across seasons); record in design-history but no remediation needed.

### 3.5 Empirical data source

- **PRIMARY:** `kit_archive` table (ACTIVE kits with bc_cell_id + q1-q5 BC-axis position) joined with `phase7_kit_verdict_log` (verdict = SHIPPED-WORTHY filter)
- **SECONDARY:** `ExportFactionCluster.modal_bc_axis_signature` field (cluster-level modal signature for sanity-check)
- **BASELINE:** `canonical/48-cycle-14-class-roster-2026-05-27.md` § 3.1 coverage matrix lines 289-298 (10 archetype × 8 BC-axis signature table)

### 3.6 Output record format

Per-dimension audit emits to `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-wave-5-ab-comparison-dim-1-output.md`:

```
Archetype shape coverage measurement — Wave 5 season <season_id>

| Archetype | Substrate anchor (rows) | Emergence | Matching kits | Verdict |
|---|---|---|---|---|
| Barbarian | ~249 rows (#1+#2+#3+#7) | YES | 4 kits (kit_ids: ...) | EMERGED |
| Hoplite | ~158 rows (#4+#5) | YES | 3 kits | EMERGED |
| ...
| Magus | 149 rows (#27+#29+#30) | NO | 0 kits | NOT-EMERGED |

Coverage count: 8 of 10
Coverage rate: 0.80
Verdict: B-PASS dim #1
```

---

## 4. Dimension #2 — Substrate-anchor distribution

### 4.1 Operational definition

**Question this dimension answers:** what fraction of Wave 5 SHIPPED-WORTHY kits carry a `substrate_anchored_personage` metadata field (named-personage anchor allocated per Sketch F D-Sharpened architecture)?

**Sketch F target:** ~32% of kits carry substrate-anchor metadata per `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` § 2 + PM-2 D-Sharpened spec. Rationale below.

**Discipline #41 framing:** the ~32% target is itself a substrate-vote outcome (Sketch F is the architectural commitment that named-personage anchors are allocated to kits whose substrate aligns with a recognized named-template). It is NOT a pre-authored taxonomy — the named-templates emerge from substrate (cf. Carnwennan for Assassin, Mistilteinn for Hoplite per doc 48 § 1). The target is a DENSITY check, not an enumeration check.

**Non-question this dimension does NOT answer:** "which named-personages are allocated?" (That is dim #4 personage-convergence's question.) Dim #2 only counts.

### 4.2 ~32% Sketch F target rationale documented

**Sketch F architecture (per Path III note § 2):**
- Phase 5 D-Sharpened encoding allocates `substrate_anchored_personage` metadata to kits whose substrate signature is within tight similarity-threshold of a recognized named-template anchor (e.g., a DEX-melee-stealth kit with kris substrate matches Carnwennan named-anchor).
- Allocation is ENGINE-INTERNAL ANALYTICS METADATA (D-Sharp-3) — NEVER LLM-prompt-exposed (D-Sharp-1) — Phase 5 LLM produces uniform player-facing names regardless of anchor (D-Sharp-4 uniformity).
- The ~32% target derives from: (a) substrate's named-template pool size (~50 distinct named-template anchors across cultural-lineage registers per elrond Stage 1 audit), (b) Wave 5 production-season kit count (~22-40 kits surviving Phase 4), (c) expected match-rate at tight similarity-threshold (~30-35% given substrate's natural distribution).

**Why 32% specifically:** Sketch F is the design-intent commitment that substrate-anchor density should be substantial-but-not-dominant — substantial enough that named-template lore surfaces meaningfully in the kit population; not-dominant enough that emergent kits without anchors remain the majority (preserving substrate-led emergence over named-template-replay). A 32% target encodes the substantial-but-not-dominant intent operationally.

**Acceptance band:** 22% - 42% (target ±10 percentage points; honest small-n band per Wave 5 n=22-40).

### 4.3 Measurement procedure

**Step 1 — Query Wave 5 kits with substrate-anchor allocation.** From `ExportFactionCluster.substrate_anchored_personages`:

```python
# ExportFactionCluster has list[ExportFactionCluster] per season
# Each cluster has substrate_anchored_personages: list[dict] | None
# Each dict shape: {kit_id: str, personage_name: str, anchor_lineage: str}

total_shipped_kits = count_kits_in_phase7_kit_verdict_log_where(
    season_id=wave_5_season_id, verdict='SHIPPED-WORTHY'
)
anchored_kit_ids = set()
for cluster in ExportFactionCluster.where(season_id=wave_5_season_id):
    if cluster.substrate_anchored_personages:
        for anchor_record in cluster.substrate_anchored_personages:
            anchored_kit_ids.add(anchor_record['kit_id'])

anchor_distribution = len(anchored_kit_ids) / total_shipped_kits
```

**Step 2 — Compute per-cluster anchor density.** Distribute the anchor count across the 3-4 clusters for cluster-level granularity:

```python
per_cluster_anchor_density = {}
for cluster in ExportFactionCluster.where(season_id=wave_5_season_id):
    anchor_count = len(cluster.substrate_anchored_personages or [])
    member_count = cluster.member_count
    per_cluster_anchor_density[cluster.cluster_id] = anchor_count / member_count
```

**Step 3 — Sanity-check vs `kit_archive` substrate-anchor field.** If kit_archive also carries substrate_anchor metadata at the per-kit layer (D-Sharp-3 engine-internal), cross-validate ExportFactionCluster aggregation against kit_archive direct count. Discrepancy >5% triggers data-pipeline integrity check (star-lord routing).

### 4.4 Acceptance criterion

| Anchor distribution | Verdict | Rationale |
|---|---|---|
| 0.22 - 0.42 | B-PASS dim #2 | Within Sketch F target band; substrate-anchor allocation operating per design intent |
| 0.15 - 0.21 OR 0.43 - 0.50 | WARN dim #2 | Adjacent-to-band; investigate but not refuting (small-n at Wave 5 expected to widen distribution) |
| <0.15 | A-PASS dim #2 | Substrate-anchor allocation under-performing; either D-Sharpened impl is broken OR Sketch F target was over-anticipated |
| >0.50 | A-PASS dim #2 | Substrate-anchor allocation over-performing → risk that named-template-replay dominates emergent kit identity; the "substantial-but-not-dominant" intent violated |

**Symmetric A-PASS bands (both <0.15 AND >0.50):** Sketch F's design intent has TWO failure modes — too few anchors (named-template lore doesn't surface; kits feel anonymous) AND too many anchors (named-template dominates; emergent identity is replay-of-templates rather than substrate-led emergence). Both fail B-PASS; both route to design-call.

### 4.5 Per-cluster anchor density check (secondary)

Per-cluster density distribution provides additional signal:
- If ALL clusters have 0% anchor density (no cluster has any anchored kits): D-Sharpened allocation may be broken at clustering layer (anchors not flowing through PM-1 → PM-2 → ExportFactionCluster pipeline). Routes to rocket + star-lord data-pipeline check.
- If ONE cluster has 100% anchor density and others have 0%: anchor-allocation is collapsing into a single cluster; named-template lore concentrating rather than distributing. Routes to PM-1 clustering parameter check (k might be wrong; or anchor-allocation is shadowing cluster boundaries).
- Healthy distribution: 2-4 clusters each with 20-50% anchor density.

### 4.6 Drift-watch criterion (Cycle 15+ revisit trigger)

- **DRIFT TRIGGER:** if anchor distribution shifts >10 percentage points across Cycle 15+ seasons (e.g., Wave 5 = 32%; Cycle 15 season 1 = 45%; Cycle 15 season 2 = 18%), substrate-anchor allocation algorithm is unstable. Investigate D-Sharpened thresholding.
- **DRIFT TRIGGER:** if Wave 5 anchor distribution lands at 0.32 B-PASS but per-cluster density consistently collapses into 1-2 clusters across multiple seasons, the cluster-collapse pattern is a Sketch F architectural concern even at headline-target B-PASS. Route to gandalf design review.
- **DRIFT TRIGGER:** if substrate enrichment commissions (Q-S2-12/13/14) execute and anchor distribution shifts as a result, re-baseline the target band — enrichment is expected to expand named-template pool, which may shift natural anchor-allocation rate upward to 40-50% range.

### 4.7 Empirical data source

- **PRIMARY:** `ExportFactionCluster.substrate_anchored_personages` field (list[dict] per cluster; null when no anchored kits in cluster)
- **SECONDARY:** `kit_archive` substrate-anchor metadata (D-Sharp-3 engine-internal; cross-validation only)
- **BASELINE:** Sketch F architectural commitment (~32% target ±10pp band)
- **GROUND-TRUTH:** `phase7_kit_verdict_log.verdict = 'SHIPPED-WORTHY'` filter for kit-population denominator

### 4.8 Output record format

```
Substrate-anchor distribution measurement — Wave 5 season <season_id>

Total SHIPPED-WORTHY kits: 32
Anchored kits: 11
Anchor distribution rate: 0.344
Verdict band: 0.22-0.42 → B-PASS dim #2

Per-cluster anchor density:
| Cluster ID | Member count | Anchored | Density |
|---|---|---|---|
| 1 | 10 | 3 | 0.30 |
| 2 | 8 | 4 | 0.50 |
| 3 | 14 | 4 | 0.29 |

Cluster-collapse check: distributed across all 3 clusters → healthy.
```

---

## 5. Dimension #3 — Faction pairwise-distance distribution

### 5.1 Operational definition

**Question this dimension answers:** are Wave 5 emergent factions structurally distinct from each other (high-distance signal) OR all-close (faction concept collapsing into single shape)?

**Pairwise-distance** is Mahalanobis distance computed at G-B primary-pair selection time (rocket `a466eb1` / PM-2 § 13.2 algorithm); populated into `ExportFactionCluster.pairwise_distance_distribution` field (list of all pairwise distances per season, sorted descending; length k*(k-1)/2; k=3 → 3 values; k=4 → 6 values).

**High-distance signal:** the max pairwise distance is meaningfully larger than the min pairwise distance (e.g., max/min ratio ≥1.5); the season has a primary tension pair AND a less-tense pair, producing narrative structure.

**All-close signal:** max pairwise distance is within 5% of min pairwise distance (max/min ratio <1.05); all factions are equidistant; no meaningful primary-pair tension exists; G-B tie-break logic fires (per F-8 failure mode in `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md`).

**Discipline #41 framing:** the spread of pairwise distances is the substrate's vote on whether faction emergence is producing meaningfully different factions OR variations on a single theme. All-close signal is not a code failure; it is a substrate-signal that the season substrate is uniform. The protocol surfaces the signal honestly.

### 5.2 Measurement procedure

**Step 1 — Extract pairwise-distance distribution for Wave 5 season.** Since `ExportFactionCluster.pairwise_distance_distribution` is duplicated on every cluster record (analyst convenience per PM-2 § 13.5), read from any single cluster record:

```python
clusters = ExportFactionCluster.where(season_id=wave_5_season_id)
distances = clusters[0].pairwise_distance_distribution  # sorted descending
k = len(clusters)
expected_pair_count = k * (k - 1) // 2  # k=3 → 3; k=4 → 6
assert len(distances) == expected_pair_count, "G-B distribution length integrity check"
```

**Step 2 — Compute distribution summary statistics.** At Wave 5 small-n (3 or 6 distances), descriptive statistics only:

```python
d_max = distances[0]          # largest pairwise distance
d_min = distances[-1]         # smallest pairwise distance
d_median = distances[len(distances)//2]
ratio_max_min = d_max / d_min if d_min > 0 else float('inf')
ratio_max_median = d_max / d_median if d_median > 0 else float('inf')
spread_iqr = numpy.percentile(distances, 75) - numpy.percentile(distances, 25)
```

**Step 3 — Classify distribution shape.**

| Shape | Condition | Interpretation |
|---|---|---|
| **HIGH-DISTANCE** | `ratio_max_min >= 1.50` | Primary-pair meaningfully distinct from background-pairs; faction structure has tension architecture |
| **MODERATE-DISTANCE** | `1.05 <= ratio_max_min < 1.50` | Some pairwise separation; primary-pair selection meaningful but background-pairs not negligible |
| **ALL-CLOSE** | `ratio_max_min < 1.05` | Factions equidistant; primary-pair tie-break fires; F-8 risk realized |

**Step 4 — Cross-check with G-B selection rationale.** Read `ExportFactionCluster.gb_selection_rationale`:
- `highest_substrate_distance` → consistent with HIGH-DISTANCE or MODERATE-DISTANCE shape
- `lineage_diversity_tiebreak` / `named_anchor_tiebreak` / `geometry_divergence_tiebreak` → consistent with ALL-CLOSE shape (tie-breaks fired)
- `degenerate_single_cluster` → k=1 fallback; dim #3 inapplicable; record separately

Integrity check: if shape is HIGH-DISTANCE but rationale is a tiebreak, OR shape is ALL-CLOSE but rationale is highest_substrate_distance, data-pipeline integrity issue. Route to rocket + star-lord for G-B output validation.

### 5.3 Acceptance criterion

| Shape | Verdict | Rationale |
|---|---|---|
| HIGH-DISTANCE (ratio ≥1.50) | B-PASS dim #3 | Substrate-led emergence is producing structurally distinct factions; G-B primary-pair selection meaningful |
| MODERATE-DISTANCE (1.05 ≤ ratio < 1.50) | WARN dim #3 | Factions distinct but tension architecture muted; design call on whether moderate is sufficient for player narrative |
| ALL-CLOSE (ratio <1.05) | A-PASS dim #3 | Faction emergence has collapsed into single shape with variations; either substrate uniformity (substrate-vote signal — surface honestly) OR PM-1 clustering parameters mis-tuned (k might need k=2 binary forced) |

**Why ratio thresholds, not absolute distance:** Mahalanobis distance is scale-dependent on cluster covariance; absolute distance values are not comparable across seasons with different substrate. Ratio of max-to-min within a season is scale-invariant and captures the "is there meaningful structure" question directly.

**Why ≥1.50 ratio for B-PASS:** if primary pair is 50% farther apart than the closest pair, the primary-pair tension has narrative force — players experience the central conflict as central. Below 1.50 ratio, primary pair feels arbitrary even if statistically selected.

### 5.4 Drift-watch criterion (Cycle 15+ revisit trigger)

- **DRIFT TRIGGER:** if ratio_max_min consistently drops across Cycle 15+ seasons (e.g., Wave 5 = 1.85; Cycle 15 averaging 1.25), substrate may be homogenizing across seasons; investigate substrate-curation pipeline (elrond Phase D cleaning artifacts).
- **DRIFT TRIGGER:** if tie-break rationale fires >20% of seasons across Cycle 15+ (per F-8 watch threshold), G-B algorithm needs refinement (widen tolerance OR add additional tie-breaker per F-8 counter).
- **DRIFT TRIGGER:** if a season fires `degenerate_single_cluster` rationale, PM-1 clustering produced k=1 — investigate whether substrate is collapsing OR PM-1 BIC selection drifted (math note review).

### 5.5 Empirical data source

- **PRIMARY:** `ExportFactionCluster.pairwise_distance_distribution` field (duplicated on every cluster row; list[float] sorted descending)
- **SECONDARY:** `ExportFactionCluster.gb_selection_rationale` field (G-B selection rationale enum)
- **CROSS-CHECK:** `ExportFactionRelationship.pairwise_distance` field (per-pair distance; should equal corresponding entry in pairwise_distance_distribution)
- **BASELINE:** doc 48 does NOT carry pairwise-distance baseline (doc 48 is per-archetype curation, not pairwise). Dim #3 is a Wave 5-internal structural check; doc 48 baseline does not apply.

**Doc 48 baseline N/A note:** dim #3 is the dimension where the A/B comparison framing diverges most explicitly — doc 48 baseline carries NO pairwise-distance signal because designer-curation does not compute pairwise BC-distance between curated archetypes. The dim #3 verdict is therefore a Wave 5 self-evaluation (substrate-led emergence produces structurally meaningful factions OR it doesn't), with no A counterpart. This is honest: the doc 48 baseline cannot answer this question because designer-curation does not compute pairwise-distance signal at all.

### 5.6 Output record format

```
Faction pairwise-distance distribution measurement — Wave 5 season <season_id>

k = 3 clusters → 3 pairwise distances
Distances (sorted descending): [4.82, 3.15, 2.61]
d_max: 4.82  d_min: 2.61  d_median: 3.15
ratio_max_min: 1.85
ratio_max_median: 1.53
Shape: HIGH-DISTANCE
G-B selection rationale: highest_substrate_distance
Integrity check: PASS (shape consistent with rationale)
Verdict: B-PASS dim #3
```

---

## 6. Dimension #4 — Personage convergence test (Q2 D-Sharpened H1 vs H2)

### 6.1 Operational definition

**Question this dimension answers:** does the named-personage anchor metadata (D-Sharpened D-Sharp-3) correlate with the substrate-cluster identity of the kits it anchors? That is — when Sketch F allocates Carnwennan to a kit, is that kit in a substrate-cluster whose other anchored kits share a thematic-anchor neighborhood with Carnwennan (assassin-stealth-dagger neighborhood), OR is Carnwennan allocated randomly across substrate-clusters with no correlation?

**H1 — null hypothesis:** substrate-anchor allocation is uncorrelated with substrate-cluster membership. Carnwennan is as likely to anchor a kit in cluster 1 (DEX-melee-stealth) as in cluster 3 (WIS-channel-aura). D-Sharpened metadata is noise; named-personage anchors do not converge on thematically-coherent clusters.

**H2 — alternative hypothesis:** substrate-anchor allocation correlates with substrate-cluster membership. Carnwennan reliably anchors kits in the DEX-melee-stealth cluster; Mistilteinn reliably anchors kits in the STR-polearm cluster; etc. D-Sharpened metadata IS signal; named-personage anchors converge on thematically-coherent clusters.

**Discipline #41 framing:** H2 is the Sketch F architectural prediction. If Wave 5 substrate-led emergence is operating as designed, the substrate signal that surfaces Carnwennan as a Sketch F anchor (DEX-melee-stealth-dagger BC signature) should ALSO surface a cluster of related kits, AND Carnwennan should anchor a kit WITHIN that cluster — not in a random cluster. H1 vs H2 empirical verdict is the test of whether Sketch F architecture is mechanically delivering on its design intent at substrate-led-emergence layer.

**Why this is Q2 D-Sharpened:** Sketch F D-Sharpened encoding (PM-2 § 2.7) commits to allocating anchors as ENGINE-INTERNAL ANALYTICS metadata; the test asks whether that metadata carries actionable signal (correlated to cluster identity = signal) or noise (random allocation = noise). Q2 from the Path III note is the convergence-test question that gates whether D-Sharpened survives Cycle 14 close.

### 6.2 Q-AB-1 resolution — Statistical test choice

**Decision: Bayesian posterior method (with Fisher's exact as supplementary report).**

**Reasoning per sample size + question shape:**

| Method | Suitability at Wave 5 n=22-40 kits / ~7-13 anchored kits / 3-4 clusters | Verdict |
|---|---|---|
| **Chi-squared test of independence** | Asymptotic; requires expected cell counts ≥5 per cell. At 3-4 clusters × 7-13 anchored kits, expected cell counts will frequently be <5. Chi-squared assumption violated. | REJECT — wrong tool at this sample size |
| **Fisher's exact test** | Exact small-n method; no expected-count requirement; well-suited to 3×3 or 4×3 contingency table (clusters × anchor-thematic-neighborhoods). Produces p-value. | ACCEPTABLE — but produces only p-value; does not honestly represent uncertainty range |
| **Bayesian posterior over correlation parameter** | Prior + Wave 5 likelihood → posterior over correlation strength; produces credible interval AND Bayes factor BF(H2/H1). Honestly represents small-n uncertainty. Supports Cycle 15+ posterior update with replication data without re-running test. | **PRIMARY** — small-n honesty; supports replication; aligns with Discipline #11 empirical-inspection-over-assumption |

**Decision rationale:** at Wave 5 n=22-40 kits with ~7-13 anchored kits and 3-4 clusters, frequentist p-values lie about precision. A p=0.07 from Fisher's exact at this sample size says "data don't refute H1 at α=0.05" but does NOT say "data favor H1" — it says "we don't have enough data." Bayesian posterior with Bayes factor BF(H2/H1) honestly represents this: BF=1.5 means data weakly favor H2; BF=3.0 means moderate evidence for H2; BF=0.5 means data weakly favor H1; BF=0.95-1.05 means data are uninformative. Cycle 15 replication can update the posterior without re-running the test.

**Fisher's exact as supplementary report:** report p-value alongside Bayes factor for cross-method sanity-check and for readers more familiar with frequentist framing. Discrepancy between Fisher's p-value and Bayes factor verdict triggers methodology review (elrond consultation per Discipline #18 math-hotspot routing).

**Why not chi-squared:** chi-squared at this sample size violates its own asymptotic assumption. Reporting chi-squared p-value at n=22-40 with 3-4 clusters is methodologically dishonest. Reject.

### 6.3 Measurement procedure

**Step 1 — Construct anchor-thematic-neighborhood taxonomy.** For Wave 5 anchored kits, group by anchor_lineage field (from ExportFactionCluster.substrate_anchored_personages dicts). Anchor-lineage groups (per substrate's natural lineage distribution from elrond Stage 1 audit):
- `european-historical` (Charlemagne / Beowulf / Arthur-cycle anchors)
- `european-mythological` (Norse / Celtic mythological anchors including Mistilteinn, Hrunting)
- `middle-eastern` (kris / scimitar / shamshir anchors)
- `south-asian` (kukri / talwar anchors)
- `east-asian` (katana / nodachi anchors)
- `fantasy-generic` (substrate-natural fantasy template anchors)
- `classical` (Greco-Roman anchors)

Taxonomy emerges from substrate, NOT pre-authored. If Wave 5 produces anchor-lineage values outside this list, taxonomy expands (substrate-led discipline preserved).

**Step 2 — Construct cluster-thematic-neighborhood mapping.** For each Wave 5 emergent cluster (3-4 clusters), assign expected anchor-lineage based on cluster's modal substrate signal (from `ExportFactionCluster.modal_cultural_lineage` field + `modal_bc_axis_signature`). Each cluster has 1-2 expected anchor-lineage neighborhoods.

Example (hypothetical Wave 5 with 3 clusters):
- Cluster 1: modal_cultural_lineage = european, BC signature = STR-melee-cleave → expected anchors: european-historical (Charlemagne, Arthur-cycle), european-mythological (Beowulf)
- Cluster 2: modal_cultural_lineage = fantasy_generic, BC signature = DEX-ranged-firearm → expected anchors: fantasy-generic
- Cluster 3: modal_cultural_lineage = mixed (european + middle-eastern), BC signature = DEX-melee-stealth → expected anchors: european-historical (Carnwennan via Arthur-cycle), middle-eastern (kris-lineage), south-asian (kukri-lineage)

Mapping is computed deterministically from cluster modal fields; recorded as test fixture; reviewed by gandalf at execution time for fidelity.

**Step 3 — Compute observed contingency table.** For each anchored kit, record (cluster_id, anchor_lineage) → contingency table of clusters × anchor_lineages.

```
                    cluster_1    cluster_2    cluster_3
european-hist           4            0            1
european-myth           1            0            0
middle-eastern          0            0            2
south-asian             0            0            1
fantasy-generic         0            3            0
```

**Step 4 — H1 vs H2 test under Bayesian framing.**

Model:
- Let `p_{ij}` = probability that an anchored kit with anchor-lineage `i` ends up in cluster `j`.
- H1: `p_{ij}` is uniform across `j` for each `i` (anchor allocation is independent of cluster).
- H2: `p_{ij}` is concentrated on expected-anchor-lineage clusters (anchor allocation is correlated with cluster identity).

Prior:
- Dirichlet prior on `p_i` per anchor-lineage, with concentration parameter α=1 (uniform prior; weak Bayesian commitment to neither H1 nor H2).

Likelihood:
- Multinomial likelihood per anchor-lineage given observed contingency counts.

Posterior:
- Posterior over each `p_i` is Dirichlet (Dirichlet-Multinomial conjugacy).
- Compute posterior probability that each anchor-lineage concentrates on its expected-cluster (per Step 2 mapping): `P(p_{i, expected_cluster_i} > 1/k | data)`.

Bayes factor:
- BF(H2/H1) = ratio of marginal likelihoods under H2 (concentration prior) vs H1 (uniform prior).
- Compute via numerical integration over Dirichlet posterior OR via Savage-Dickey ratio if H1 is nested in H2 prior structure.

**Step 5 — Report posterior verdict + Fisher's exact supplementary.**

```
Bayes factor BF(H2/H1) = X.YZ
- BF >= 3.0 → moderate-to-strong evidence for H2 (Sketch F architecture delivers)
- 1.50 <= BF < 3.0 → weak-to-moderate evidence for H2
- 0.95 <= BF < 1.50 → data uninformative
- 0.33 <= BF < 0.95 → weak-to-moderate evidence for H1
- BF < 0.33 → moderate-to-strong evidence for H1 (D-Sharpened metadata is noise)

Fisher's exact supplementary p-value: X.YZ
Cross-method check: PASS / DISCREPANCY-REVIEW
```

### 6.4 Acceptance criterion

| Bayes factor BF(H2/H1) | Verdict | Rationale |
|---|---|---|
| ≥3.0 | B-PASS dim #4 | Sketch F architecture mechanically delivers; D-Sharpened metadata is signal; substrate-anchor allocation converges on thematic-cluster neighborhoods |
| 1.50 ≤ BF < 3.0 | LEAN-B dim #4 | Weak-to-moderate evidence for H2; consistent with Sketch F intent at small-n; Cycle 15 replication strengthens posterior |
| 0.95 ≤ BF < 1.50 | INCONCLUSIVE dim #4 | Sample size insufficient; defer composite verdict OR replicate at Cycle 15 k=3-5 production seasons |
| 0.33 ≤ BF < 0.95 | LEAN-A dim #4 | Weak-to-moderate evidence for H1; D-Sharpened metadata may be noise; flag for investigation |
| <0.33 | A-PASS dim #4 | Strong evidence for H1; D-Sharpened allocation algorithm is not converging on substrate-cluster identity; Sketch F architectural intent not delivering |

**Sample-size honesty clause:** if Wave 5 anchored-kit count <7 (insufficient data for any meaningful Bayes factor), dim #4 verdict is UNDER-POWERED-DEFER regardless of computed BF; defer to Cycle 15. Threshold of 7 derives from minimum-anchored-kit floor for 3-cluster contingency table to produce non-degenerate posterior.

### 6.5 Drift-watch criterion (Cycle 15+ revisit trigger)

- **DRIFT TRIGGER:** if Wave 5 verdict is B-PASS (BF ≥3.0) but Cycle 15 replications produce BF <1.5 average, D-Sharpened convergence is unstable; investigate whether substrate-anchor pool is fragmenting OR PM-1 clustering parameters are drifting.
- **DRIFT TRIGGER:** if posterior credible interval narrows but stays near BF=1 across Cycle 15 replications, sample-size accumulation is confirming that data are genuinely uninformative; this is a signal that Sketch F architecture's predicted convergence may not be present in substrate-led emergence (architectural reconsideration warranted).
- **DRIFT TRIGGER:** if Fisher's exact and Bayesian posterior produce discrepant verdicts (e.g., Fisher p<0.05 reject-H1 but BF=1.2 uninformative), methodology review (elrond consultation per Discipline #18) is required before next Cycle.

### 6.6 Empirical data source

- **PRIMARY:** `ExportFactionCluster.substrate_anchored_personages` (per-kit anchor-lineage records)
- **PRIMARY:** `ExportFactionCluster.modal_cultural_lineage` + `modal_bc_axis_signature` (per-cluster expected-anchor-lineage mapping)
- **SECONDARY:** `kit_archive` substrate-anchor metadata (per-kit-direct cross-validation)
- **BASELINE:** doc 48 § 4.1 anchoring table (per-archetype substrate seed + lineage signal; serves as the expected-anchor-lineage prior structure for Step 2 cluster mapping)
- **METHODOLOGY:** Bayesian Dirichlet-Multinomial posterior + Bayes factor; Fisher's exact supplementary; chi-squared REJECTED at this sample size

### 6.7 Output record format

```
Personage convergence test (Q2 D-Sharpened H1 vs H2) — Wave 5 season <season_id>

Anchored kit count: 11 (above 7 floor; analysis proceeds)
Contingency table (clusters × anchor-lineages):
                cluster_1   cluster_2   cluster_3
european-hist       4           0            1
european-myth       1           0            0
middle-eastern      0           0            2
south-asian         0           0            1
fantasy-generic     0           3            0

Cluster expected-anchor mapping (from Step 2):
cluster_1: european-hist, european-myth
cluster_2: fantasy-generic
cluster_3: middle-eastern, south-asian, european-hist (Arthur-cycle)

Bayesian posterior:
P(anchors concentrate on expected clusters | data) = 0.91
Bayes factor BF(H2/H1) = 4.2

Fisher's exact supplementary p-value: 0.018
Cross-method check: PASS (both reject H1; consistent verdict)

Verdict: B-PASS dim #4 (BF=4.2 ≥3.0 → moderate-to-strong evidence for H2;
Sketch F architecture mechanically delivers at Wave 5)
```

---


