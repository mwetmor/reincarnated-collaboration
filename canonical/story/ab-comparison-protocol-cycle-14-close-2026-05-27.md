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

## 7. Dimension #5 — Surprise-emergence count

### 7.1 Operational definition

**Question this dimension answers:** how many Wave 5 emergent shape-clusters do NOT match any doc 48 candidate archetype-shape — that is, how many novel archetype-shapes did substrate-led emergence produce that designer-curation did not anticipate?

**"Surprise emergence" means** a SHIPPED-WORTHY kit-cluster (group of ≥2 kits with shared BC-axis signature within similarity-threshold per dim #1 § 3.2) whose BC-axis signature does NOT match any of the 10 doc 48 archetype signatures at the ≥6-of-8 axes agreement threshold.

**Discipline #41 framing:** surprise emergence is the POSITIVE outcome that justifies the substrate-led architectural commitment. If Option α only reproduces doc 48 (zero surprises), the substrate-led commitment delivers nothing beyond what designer-curation produced — Option α architectural commitment is computationally expensive ceremony. Some level of surprise emergence is what makes substrate-led emergence load-bearing for the generative-architecture decision.

**Q-AB-2 surfaces here:** how LOW can surprise count be before B-PASS is undermined?

### 7.2 Q-AB-2 resolution — Acceptance criterion for surprise-emergence count

**Decision: surprise count ≥1 at Wave 5 is acceptance threshold for B-PASS; zero surprises is NOT automatic A-PASS but flags FOLLOW-UP-DEFER.**

**Reasoning:**

The doc 48 baseline has 10 archetype-shapes. Wave 5 production season produces ~3-4 substrate-clusters (per PM-1 GMM k∈{3,4}). The fundamental scale mismatch (10 baseline shapes vs 3-4 Wave 5 clusters) means:
- Wave 5 cannot REPRODUCE 10 doc 48 archetypes — there is only room for 3-4 cluster identities.
- The dim #1 archetype-coverage measurement asks "of the 10 doc 48 archetypes, how many emerge as SHIPPED-WORTHY kit-shapes within 3-4 clusters?" (Multiple archetypes can share a cluster if their BC signatures are adjacent.)
- The dim #5 surprise-emergence measurement asks the converse: "of the 3-4 Wave 5 clusters, how many have a modal shape that doesn't map to any doc 48 archetype?"

**At Wave 5 expected output (3-4 clusters), surprise-emergence count can range from 0 to 4.**

| Surprise count | Verdict at Wave 5 (1 season) | Rationale |
|---|---|---|
| 0 | FOLLOW-UP-DEFER dim #5 | Wave 5 reproduced doc 48 shapes within its 3-4 clusters; absence of surprise at single-season is NOT refutation (small-n; novel emergence may appear at Cycle 15 replications); flag for Cycle 15 watch but does not block composite verdict |
| 1 | B-PASS dim #5 | Substrate-led emergence produced novel shape designer did not anticipate; substrate-led architectural commitment delivers value beyond designer-curation reproduction |
| 2-3 | B-PASS dim #5 (with gandalf interpretation) | Multiple surprises; each surprise requires gandalf design-quality audit to distinguish (a) substrate-led discovery of meaningful new archetype-shape from (b) substrate-noise producing thin incoherent cluster that happens to not match doc 48 |
| 4 (all clusters surprise) | A-PASS dim #5 | Wave 5 reproduced ZERO doc 48 shapes; this is the inverted failure mode — substrate-led emergence is producing only novel shapes AND missing all designer-anticipated coverage; signals PM-1 clustering or Phase 4 eviction is over-rejecting designer-recognized substrate patterns; routes to math note re-review |

**Why ≥1 (not ≥2) is B-PASS threshold:** at Wave 5 single-season, even 1 substrate-discovered novel archetype is empirical evidence that substrate-led emergence produces signal beyond designer-curation. Demanding ≥2 at single-season would require Wave 5 to half-not-match doc 48 at a sample size that cannot reliably distinguish "novel emergence" from "noise"; ≥1 threshold is the small-n-honest floor.

**Why 0 surprises is FOLLOW-UP-DEFER (not A-PASS):** zero surprises at single-season is consistent with (a) substrate genuinely matches doc 48 anticipation OR (b) novel emergence is rare and Wave 5 happened to not surface any. Cannot distinguish at n=1 season. Defer to Cycle 15 replications: if 3-5 production seasons consistently produce 0 surprises, Option α architectural commitment is NOT delivering value beyond designer-curation; that pattern at sample size n=3-5 IS A-PASS evidence. Single-season zero is not enough to refute.

**Why 4-all-surprises is A-PASS (not B-PASS):** if EVERY Wave 5 cluster is novel and ZERO doc 48 shapes emerge, the failure mode is symmetric to dim #1 ≤0.60 coverage A-PASS. Substrate-led emergence has decoupled from substrate-evidence that designer-curation could read directly. Either the algorithm is mis-tuned (rejecting recognizable patterns) OR substrate has shifted away from designer-anticipated cluster definitions. Routes to PM-1 + Phase 4 architectural re-review.

**Q-AB-2 verdict:** the protocol structure embeds a quality-asymmetry — high surprise count is mostly good (substrate-led discovery), zero is deferred (could be either-direction), all-surprises is bad (architectural decoupling). The asymmetry honors the substrate-led architectural commitment WHILE recognizing that disconnection from designer-recognizable substrate patterns IS a failure mode.

### 7.3 Measurement procedure

**Step 1 — Reuse dim #1 kit-to-doc-48-archetype matching output.** For each SHIPPED-WORTHY kit, dim #1 § 3.2 Step 3 computed which doc 48 archetypes it matches (≥6 of 8 axes agreement). Carry forward to dim #5.

**Step 2 — Identify Wave 5 clusters via `phase7_kit_verdict_log.cluster_id`.** Group SHIPPED-WORTHY kits by cluster_id; each cluster is a candidate substrate-led-emergent shape.

**Step 3 — Compute per-cluster modal-shape match.** For each cluster, compute:
- The cluster's modal doc 48 archetype match (the doc 48 archetype that ≥50% of cluster kits match)
- If no doc 48 archetype is matched by ≥50% of cluster kits → cluster is a SURPRISE.

**Step 4 — Surprise-emergence count.** `surprise_count = sum(1 for cluster if cluster.modal_match is None)`.

**Step 5 — Per-surprise gandalf interpretation hook.** For each surprise cluster, record:
- Modal BC-axis signature (the 8-tuple that defines the surprise shape)
- Modal cultural lineage
- Modal substrate seed (which substrate seeds drove this cluster's existence)
- Cohesion score (from `phase7_cluster_aggregate_log.cluster_compactness`)
- Discrimination from doc 48: which doc 48 archetype was closest BUT failed the ≥6-of-8 threshold?

This per-surprise record enables gandalf design-quality audit to distinguish substrate-led discovery (meaningful new shape worth canonical recognition) from substrate noise (thin incoherent cluster that happens not to match anything).

### 7.4 Acceptance criterion

(See Q-AB-2 resolution table in § 7.2 above — repeated here for execution convenience)

| Surprise count | Verdict | Composite verdict contribution |
|---|---|---|
| 0 | FOLLOW-UP-DEFER dim #5 | INCONCLUSIVE for composite (defers to Cycle 15) |
| 1 | B-PASS dim #5 | B contribution |
| 2-3 | B-PASS dim #5 (interpretation-gated) | B contribution conditional on gandalf design-quality audit verdict per surprise |
| 4 (all clusters) | A-PASS dim #5 | A contribution |

### 7.5 Drift-watch criterion (Cycle 15+ revisit trigger)

- **DRIFT TRIGGER:** if Wave 5 surprise count = 0 and Cycle 15 replications (3-5 production seasons) consistently produce 0 surprises, Option α architectural commitment is not delivering value beyond designer-curation; trigger architectural reconsideration (Pattern B with Matt).
- **DRIFT TRIGGER:** if Wave 5 surprise count = 1 B-PASS but Cycle 15 surprises explode to 4+ across multiple seasons, substrate-led emergence has decoupled from doc 48 baseline; either substrate-curation pipeline has drifted OR PM-1 clustering parameters are now over-discriminating.
- **DRIFT TRIGGER:** if a surprise archetype-shape emerges at Wave 5, gets gandalf design-quality interpretation as "meaningful new shape," but does NOT reappear at Cycle 15 replications, the Wave 5 surprise was substrate-noise rather than substrate-signal; recognition record amended.

### 7.6 Empirical data source

- **PRIMARY:** `phase7_kit_verdict_log` (verdict = SHIPPED-WORTHY filter; cluster_id grouping) joined with `kit_archive` BC-axis signature decode
- **SECONDARY:** `phase7_cluster_aggregate_log.cluster_compactness` (cohesion-score input to surprise-cluster interpretation)
- **BASELINE:** `canonical/48-cycle-14-class-roster-2026-05-27.md` § 3.1 (10 archetype × 8 BC-axis signature table; same as dim #1)
- **REUSE:** dim #1 § 3.2 Step 3 kit-to-doc-48-archetype matching output (no recomputation needed)

### 7.7 Output record format

```
Surprise-emergence count measurement — Wave 5 season <season_id>

Wave 5 cluster count: 3
Per-cluster modal-shape match:
| Cluster | Member count | Modal doc 48 match | Match fraction | Surprise? |
|---|---|---|---|---|
| 1 | 10 | Barbarian | 7 of 10 (0.70) | NO |
| 2 | 8 | Gunslinger | 6 of 8 (0.75) | NO |
| 3 | 14 | (none ≥50%) | best: Crusader 5 of 14 (0.36) | YES |

Surprise count: 1
Verdict: B-PASS dim #5

Surprise cluster #3 detail (for gandalf design-quality audit):
- Modal BC signature: (engagement="mid-medium", damage_geometry="multi-hit",
  proxy_density="solo", control_density="mixed", damage_tempo="medium",
  amplitude_variance="flat", defensive_profile="dodger",
  resource_economy="generator-spender")
- Modal cultural lineage: middle-eastern (5/14) + south-asian (4/14)
- Modal substrate seeds: shamshir (12 rows) + chakram (5 rows) + tonfa (3 rows)
- Cluster compactness: 0.78 (high)
- Closest doc 48 archetype: Crusader (5-of-8 axis agreement — below ≥6 threshold)
- Gandalf design-quality interpretation: pending (audit at Wave 5 close)
```

---

## 8. Dimension #6 — Throwaway-cluster count

### 8.1 Operational definition

**Question this dimension answers:** how many Wave 5 emergent clusters are thin (few member kits) AND incoherent (low cluster_compactness) — that is, are substrate-tagging artifacts rather than meaningful substrate-emergent shapes?

**"Throwaway cluster" means** a cluster that fails BOTH:
- (a) `member_kit_count` floor — too few kits to constitute a meaningful shape
- (b) `cluster_compactness` floor — too low to constitute a coherent shape

A cluster failing only (a) but high on (b) is a "thin coherent cluster" — small but well-shaped; potentially a substrate-edge discovery; NOT a throwaway. A cluster failing only (b) but high on (a) is a "fat incoherent cluster" — large but ill-shaped; potentially over-clustering artifact; flag separately.

**Discipline #41 framing:** throwaway clusters indicate that PM-1 clustering produced more clusters than the substrate actually supports — substrate-tagging artifact where k=4 was selected by BIC but only 2-3 meaningful clusters exist. Substrate-led architectural commitment is undermined when emergence produces noise-clusters; the protocol distinguishes substrate-led discovery from substrate-tagging noise.

**Q-AB-3 surfaces here:** what are the operational thresholds for "too few kits" + "too low compactness"?

### 8.2 Q-AB-3 resolution — Throwaway-cluster threshold operational definition

**Decision: dual-floor threshold with substrate-led-tolerance band.**

**Floor (a) — member_kit_count:** cluster member_count < max(3, floor(0.10 × total_shipped_kits)).
- Rationale: cluster with fewer than 3 kits is statistically unreliable as a "cluster" (a single substrate-noise kit can dominate the modal signal); cluster with fewer than 10% of total SHIPPED-WORTHY kits is below "meaningful population share" floor.
- At Wave 5 with ~22-40 SHIPPED-WORTHY kits, this evaluates to 3-4 kits minimum per cluster.

**Floor (b) — cluster_compactness:** cluster_compactness < 0.40.
- Rationale: cluster_compactness is computed at PM-1 via silhouette-or-equivalent on 0.0-1.0 scale (per ExportFactionCluster schema line 622); a compactness <0.40 indicates cluster boundary is poorly defined (members are nearly as close to other clusters as to their own).
- Threshold 0.40 derives from: silhouette score interpretation literature (>0.7 strong; 0.5-0.7 moderate; 0.25-0.5 weak; <0.25 no substantial structure); the 0.40 mid-weak-band threshold catches clusters whose substrate-cohesion is questionable BEFORE they become full anti-cluster (<0.25).

**Throwaway verdict:** cluster is throwaway iff BOTH (a) AND (b) fail. Either floor alone is WARN; both is THROWAWAY.

**Asymmetric verdict structure:**

| Member count | Compactness | Verdict |
|---|---|---|
| ≥ floor(a) | ≥ 0.40 | HEALTHY |
| < floor(a) | ≥ 0.40 | THIN-COHERENT (substrate-edge discovery candidate; gandalf interpretation) |
| ≥ floor(a) | < 0.40 | FAT-INCOHERENT (over-clustering artifact; PM-1 parameter review) |
| < floor(a) | < 0.40 | **THROWAWAY** (substrate-tagging artifact) |

**Why asymmetric instead of single-floor:** small-coherent clusters and large-incoherent clusters are different failure modes with different remediation paths. Collapsing both into "throwaway" loses signal. The dual-floor structure surfaces the substrate-state honestly.

**Q-AB-3 verdict:** thresholds (a) max(3, 10% of total) AND (b) 0.40 compactness are the operational definitions; both must fail for throwaway classification; thin-coherent and fat-incoherent are recorded separately as WARN signals for substrate-led-tolerance interpretation.

### 8.3 Measurement procedure

**Step 1 — Query Wave 5 cluster aggregates from `phase7_cluster_aggregate_log`.**

```sql
SELECT cluster_id, member_kit_count, cluster_compactness,
       cohort_composition_json, shipped_worthy_count,
       held_cohesion_fail_count, held_mechanical_fail_count
FROM phase7_cluster_aggregate_log
WHERE season_id = :wave_5_season_id;
```

**Step 2 — Compute total_shipped_kits and floor(a).**

```python
total_shipped_kits = sum(row.shipped_worthy_count for row in cluster_aggregates)
floor_a = max(3, int(0.10 * total_shipped_kits))
```

**Step 3 — Classify each cluster.**

```python
for cluster in cluster_aggregates:
    member_count_pass = cluster.member_kit_count >= floor_a
    compactness_pass = cluster.cluster_compactness >= 0.40
    if member_count_pass and compactness_pass:
        cluster.verdict = "HEALTHY"
    elif not member_count_pass and compactness_pass:
        cluster.verdict = "THIN-COHERENT"
    elif member_count_pass and not compactness_pass:
        cluster.verdict = "FAT-INCOHERENT"
    else:
        cluster.verdict = "THROWAWAY"
```

**Step 4 — Tally throwaway_count + WARN signals.**

```python
throwaway_count = sum(1 for c in cluster_aggregates if c.verdict == "THROWAWAY")
thin_coherent_count = sum(1 for c in cluster_aggregates if c.verdict == "THIN-COHERENT")
fat_incoherent_count = sum(1 for c in cluster_aggregates if c.verdict == "FAT-INCOHERENT")
total_clusters = len(cluster_aggregates)
throwaway_rate = throwaway_count / total_clusters
```

**Step 5 — Cross-check with substrate-tagging artifacts via `held_cohesion_fail_count`.** A throwaway cluster should also show high held_cohesion_fail_count (cluster's kits failed Phase 7 cohesion gate at high rate); discrepancy (throwaway-by-floor but low cohesion-fail) suggests the protocol's floors may need recalibration.

### 8.4 Acceptance criterion

| throwaway_rate | Verdict | Rationale |
|---|---|---|
| ≤0.15 (≤15% of clusters) | B-PASS dim #6 | Substrate-led emergence produces predominantly meaningful clusters; tagging artifacts are minority |
| 0.16 - 0.30 | WARN dim #6 | Substantive substrate-tagging artifact rate; PM-1 parameter tuning may improve cluster quality; investigate at design-quality audit |
| >0.30 (>30% of clusters) | A-PASS dim #6 | Substrate-led emergence is producing more noise than signal at cluster layer; PM-1 BIC selection or cluster compactness threshold needs re-calibration; routes to math note re-review |

**At Wave 5 with 3-4 clusters:**
- 3 clusters: 0/3 = 0.00 → B-PASS; 1/3 = 0.33 → A-PASS (any throwaway is borderline)
- 4 clusters: 0/4 or 1/4 = 0.25 → B-PASS-to-WARN boundary; 2/4 = 0.50 → A-PASS

The thresholds compose with k∈{3,4} reality: at k=3, even one throwaway is concerning; at k=4, one throwaway is acceptable.

**Composite signal:** dim #6 verdict + dim #3 verdict (faction pairwise-distance) compose meaningfully — if dim #3 is ALL-CLOSE AND dim #6 has high throwaway count, the season substrate is genuinely homogeneous (clusters are forced into existence by k≥3 BIC selection but lack substrate support); record as substrate-vote evidence. If dim #3 is HIGH-DISTANCE but dim #6 has throwaway count, then k was selected too high; meaningful primary-pair tension exists with thin-noise satellites; PM-1 might benefit from k=2 binary mode in this substrate regime.

### 8.5 Drift-watch criterion (Cycle 15+ revisit trigger)

- **DRIFT TRIGGER:** if throwaway_rate consistently exceeds 0.15 across Cycle 15 replications (3-5 production seasons), PM-1 clustering parameters need re-calibration (BIC over-selecting k; or compactness floor should be raised); fires methodology consultation per Discipline #18.
- **DRIFT TRIGGER:** if THIN-COHERENT count is consistently ≥1 per season across Cycle 15+, substrate-edge discovery is a recurrent pattern; consider raising k cap to k=5 to give substrate-edge shapes their own cluster identity rather than orphaning them as thin.
- **DRIFT TRIGGER:** if FAT-INCOHERENT count is consistently ≥1 per season, PM-1 is under-discriminating; consider lowering k floor to k=2 OR adding cluster-split refinement step to PM-1 algorithm.

### 8.6 Empirical data source

- **PRIMARY:** `phase7_cluster_aggregate_log` table (member_kit_count + cluster_compactness + cohort_composition_json + held_cohesion_fail_count fields per cluster per season)
- **SECONDARY:** `ExportFactionCluster.cluster_compactness` (cross-validation of compactness measurement; should equal phase7_cluster_aggregate_log value)
- **BASELINE:** doc 48 baseline does NOT apply directly (doc 48 is per-archetype, not per-cluster-quality); dim #6 is substrate-emergence quality self-evaluation; A counterpart would be "did designer-curation produce any throwaway archetypes?" which is a Yes-by-different-mechanism question (designer can over-curate; substrate-led just makes the same failure visible differently). Recorded as Wave-5-internal structural check, similar to dim #3.

### 8.7 Output record format

```
Throwaway-cluster count measurement — Wave 5 season <season_id>

Total SHIPPED-WORTHY kits: 32
floor(a) = max(3, int(0.10 * 32)) = max(3, 3) = 3

| Cluster | Member count | Compactness | Verdict |
|---|---|---|---|
| 1 | 10 | 0.71 | HEALTHY |
| 2 | 8 | 0.58 | HEALTHY |
| 3 | 14 | 0.42 | HEALTHY |
| 4 | 2 | 0.31 | THROWAWAY |

throwaway_count: 1
thin_coherent_count: 0
fat_incoherent_count: 0
total_clusters: 4
throwaway_rate: 0.25
Verdict: WARN dim #6 (0.25 in 0.16-0.30 band)

Cross-check: cluster 4 held_cohesion_fail_count = 4 of 6 evaluated
(consistent with throwaway designation — cohesion gate detected the
noise pattern independently)

Composite signal note: dim #3 verdict was HIGH-DISTANCE (B-PASS); meaningful
primary-pair tension exists; cluster 4 is thin-noise satellite. PM-1 might
benefit from k=3 cap consideration in this substrate regime; queued for
Cycle 15 watch.
```

---

## 9. Composite verdict synthesis

### 9.1 Per-dimension verdict aggregation rules

Each dimension produces one of these verdicts:
- B-PASS / LEAN-B → counts toward Option α architectural commitment
- A-PASS / LEAN-A → counts against Option α
- WARN / FOLLOW-UP-DEFER / INCONCLUSIVE / UNDER-POWERED-DEFER → uninformative

### 9.2 Composite verdict computation

**B-PASS composite:** at least 4 of 6 dimensions B-PASS or LEAN-B, AND zero dimensions A-PASS.

**A-PASS composite:** at least 2 of 6 dimensions A-PASS, OR (any single A-PASS on dim #1 OR dim #4 — these are the architectural-load-bearing dimensions).

**INCONCLUSIVE composite:** any other outcome. Specifically:
- 3 or fewer B-PASS without compensating A-PASS evidence → not enough positive signal
- Mixed A-PASS + B-PASS without clear dominance → genuine ambiguity
- High proportion of UNDER-POWERED-DEFER → sample size insufficient

**Why dim #1 and dim #4 are weighted as architectural load-bearing:**

- **Dim #1 (archetype coverage):** if substrate-led emergence cannot reproduce designer-recognizable substrate patterns, the architectural commitment to substrate-led has decoupled from substrate-evidence-readability. This is a fundamental failure mode.
- **Dim #4 (personage convergence):** if Sketch F substrate-anchor metadata does not converge on substrate-cluster identity, the D-Sharpened architectural commitment is not delivering mechanically. This is a fundamental architectural test.

The other dimensions (#2 anchor distribution, #3 pairwise distance, #5 surprise emergence, #6 throwaway clusters) are tuning + quality dimensions; their A-PASS verdicts route to parameter recalibration. The architectural-load-bearing dimensions (#1, #4) route to architectural reconsideration if they A-PASS.

### 9.3 Composite verdict consumers

**B-PASS composite outcome:**
- Discipline #43 gandalf design-quality audit at Wave 5 close → PASS contribution
- KR commits Wave 5 closure record + ratifies Option α for v1 generative architecture
- Matt notification: Option α verdict B-PASS; Cycle 15 planning proceeds on substrate-led foundation
- Doc 48 STATUS confirmed as VESTIGIAL (no resurrection)

**A-PASS composite outcome:**
- Discipline #43 gandalf design-quality audit at Wave 5 close → DRIFT-DETECTED contribution
- KR holds Wave 5 closure record
- Pattern B engagement with Matt: substrate-led architectural commitment did not deliver at Wave 5 close; routes to Option β/γ reconsideration OR to substrate enrichment + Option α retry
- Doc 48 status reconsideration: PRESERVED-FOR-COMPARISON status may need re-elevation pending substrate-led path forward

**INCONCLUSIVE composite outcome:**
- Discipline #43 gandalf design-quality audit at Wave 5 close → CONDITIONAL PASS
- KR commits Wave 5 closure record AS PHASE-CLOSE-WITHOUT-ARCHITECTURAL-VERDICT
- Cycle 15 planning includes 3-5 production-season replications to resolve INCONCLUSIVE dimensions
- Pattern B engagement with Matt: timeline expectation set — composite verdict deferred to Cycle 15 close

### 9.4 Per-dimension execution order

Run dimensions in this order to minimize compute waste on data-pipeline failures:

1. **Dim #3** (faction pairwise-distance) — fastest; reads single ExportFactionCluster field; if data missing, halts entire protocol
2. **Dim #6** (throwaway-cluster count) — reads phase7_cluster_aggregate_log; if cluster data unhealthy, dim #1 + #5 results are interpretation-conditional
3. **Dim #2** (substrate-anchor distribution) — reads ExportFactionCluster.substrate_anchored_personages; checks D-Sharpened pipeline integrity early
4. **Dim #1** (archetype coverage) — needs kit_archive + phase7_kit_verdict_log join; produces kit-to-doc-48-archetype matching that dim #5 reuses
5. **Dim #5** (surprise-emergence count) — reuses dim #1 matching output + clusters
6. **Dim #4** (personage convergence Bayesian test) — highest-stakes inference; runs after data-pipeline integrity confirmed by dims #2, #3, #6; reuses anchor + cluster mapping

### 9.5 Composite verdict output record format

```
Composite A/B verdict — Wave 5 season <season_id>

Per-dimension verdicts:
| Dim | Verdict | Contribution |
|---|---|---|
| #1 archetype coverage | B-PASS (0.85) | B |
| #2 substrate-anchor distribution | B-PASS (0.34) | B |
| #3 faction pairwise-distance | B-PASS (HIGH-DISTANCE 1.85) | B |
| #4 personage convergence | B-PASS (BF=4.2) | B |
| #5 surprise-emergence | B-PASS (1 surprise) | B |
| #6 throwaway-cluster | WARN (0.25) | uninformative |

B-PASS count: 5 of 6
A-PASS count: 0 of 6
Composite verdict: B-PASS

Discipline #43 design-quality audit input: PASS contribution
KR action: commit Wave 5 closure record; ratify Option α for v1
Doc 48 status: VESTIGIAL confirmed
Cycle 15 watch items: dim #6 WARN (PM-1 k-cap recalibration consideration)
```

---

## 10. Risks + Watch Items (failure-modes register additions)

Per dispatch closure obligation, the following items are added to `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` § 5 (or § 1 if § 5 not yet present; section-add as needed at execution time):

### F-11. A/B composite verdict premature commitment under small-n

**Pattern:** Wave 5 single-season produces a B-PASS composite verdict from 4-5 B dimensions with high LEAN-B influence; KR commits Option α ratification; subsequent Cycle 15 replications produce divergent verdicts revealing Wave 5 was a sample-of-1 favorable seed. Composite verdict over-committed at insufficient sample size.

**Watch:** any Wave 5 composite verdict B-PASS that derives ≥2 of its B-contributions from LEAN-B (rather than B-PASS) dimensions triggers a Cycle 15 replication-validation phase before final ratification; gandalf design-quality audit notes the LEAN-B contributions in the closure record.

**Counter:** composite verdict semantics include explicit "Wave 5 single-season B-PASS-with-LEAN-B contributions = Wave 5 B-PASS-CONDITIONAL pending Cycle 15 3-5 production-season replication"; ratification proceeds but is conditional; Cycle 15 replication-validation is a named workstream rather than optional follow-up. Cycle 15 dispatch carries forward the LEAN-B dimensions for explicit re-evaluation.

### F-12. Dim #4 Bayesian methodology mis-application

**Pattern:** Bayesian posterior + Bayes factor methodology requires correct prior specification; mis-specified prior (e.g., wrong concentration parameter; wrong nested-vs-non-nested H1 structure) produces apparently-decisive Bayes factor that does not honestly represent evidence. Wave 5 verdict ratified on methodologically-corrupt BF value.

**Watch:** Wave 5 execution of dim #4 includes prior-sensitivity analysis as standard practice — report BF under α=0.5 (more diffuse prior), α=1 (uniform), α=2 (more concentrated); discrepancy across prior choices >2x triggers methodology consultation (elrond per Discipline #18) before verdict commitment.

**Counter:** dim #4 measurement procedure includes prior-sensitivity reporting requirement; protocol does not commit verdict on single-prior BF computation; any BF verdict derived from a single prior choice is automatically WARN at Wave 5 single-season pending Cycle 15 replication.

### F-13. doc 48 baseline interpretation drift

**Pattern:** dim #1 + dim #5 use doc 48 § 3.1 BC-axis signature encoding as baseline. If gandalf execution-time encoding of doc 48 archetypes drifts from doc 48's intent (e.g., encoder reads "small-AOE (cleave)" as `small-AOE` when doc 48 means a more specific cleave-cluster sub-bin), the A/B comparison measures a strawman doc 48 rather than the actual doc 48 baseline.

**Watch:** encoding step (dim #1 § 3.2 Step 1) is reviewed by gandalf at execution time AND cross-validated against elrond Stage 1 audit § 2.1 substrate-evidence seed mapping; encoding mismatch >2 axes per archetype triggers re-encoding with explicit gandalf sign-off.

**Counter:** dim #1 § 3.2 Step 1 specifies "encoded as test fixture in measurement script; reviewed by gandalf at protocol-execution time for fidelity to doc 48"; the review is a NAMED gate, not "while we're at it" implicit verification. Encoding-review record archived at `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-wave-5-ab-comparison-doc-48-encoding-review.md`.

### F-14. Phase 7 data-pipeline integrity failure cascades into A/B verdict

**Pattern:** A/B comparison protocol depends on phase7_kit_verdict_log + phase7_cluster_aggregate_log + ExportFactionCluster + ExportFactionRelationship being populated cleanly at Wave 5 close. If Phase 7 IMPL (gamora `eca0aa5`) has data-emission bugs (e.g., kit verdicts not all emitting; cluster aggregates missing fields; ExportFactionCluster.pairwise_distance_distribution null where G-B fired), the A/B comparison produces verdict on incomplete data — protocol cannot detect this from within.

**Watch:** dim execution order (§ 9.4) is designed to surface data-pipeline failures early (dim #3 first; dim #6 second); each dimension's measurement procedure includes integrity-check steps (dim #3 Step 4 cross-checks G-B selection rationale vs distance shape; dim #6 Step 5 cross-checks with held_cohesion_fail_count; dim #4 sample-size-floor honesty clause).

**Counter:** at protocol-execution time, the protocol-runner produces a PRE-EXECUTION DATA INTEGRITY REPORT before any dimension runs: count rows in each source table; verify schema fields populated at expected non-null rates; cross-reference ExportFactionCluster cluster_id values with phase7_cluster_aggregate_log cluster_id values; cross-reference ExportFactionCluster.pairwise_distance_distribution length with k. Any integrity failure halts protocol AND surfaces as routing-back to gamora + star-lord for data-pipeline fix BEFORE measurement proceeds. A/B verdict on incomplete data is worse than no A/B verdict at all.

### F-15. dim #5 surprise-emergence interpretation drift (substrate-noise vs substrate-discovery)

**Pattern:** dim #5 § 7.3 Step 5 requires gandalf design-quality interpretation per surprise cluster to distinguish (a) substrate-led discovery of meaningful new archetype-shape from (b) substrate noise producing thin incoherent cluster. Without rigor in this interpretation step, surprise count is reported high (B-PASS dim #5) while the surprises are actually noise — composite verdict elevated on noise interpretation.

**Watch:** any surprise cluster recorded under dim #5 requires per-surprise record (dim #5 § 7.3 Step 5) with: modal BC signature + modal cultural lineage + modal substrate seeds + cluster compactness + discrimination-from-doc-48. The record is reviewed at gandalf design-quality audit; surprise WITHOUT supporting per-surprise record cannot count as B-PASS contribution.

**Counter:** dim #5 measurement procedure mandates per-surprise interpretation record AND requires the record to demonstrate substrate-led discovery semantics — modal substrate seeds must indicate coherent substrate evidence (not random kit collection); modal cultural lineage must be consistent within the cluster; cluster compactness must be ≥0.50 (above the dim #6 floor) for surprise-as-discovery designation. Surprise clusters that fail these supplementary criteria are downgraded to "surprise-but-noise" and do not contribute to B-PASS.

### F-16. Doc 48 VESTIGIAL status retraction creates pressure to deprecate baseline

**Pattern:** Wave 5 close occurs months after doc 48 VESTIGIAL status; intervening canonical maintenance may pressure toward archiving or further-deprecating doc 48 ("we've moved past it; let's clean up"). If doc 48 is archived before A/B comparison executes, the baseline is lost; A/B comparison cannot run; Option α architectural verdict has no comparison surface.

**Watch:** doc 48 STATUS protected as VESTIGIAL-PRESERVED-FOR-A/B-COMPARISON through Wave 5 close + Cycle 15 close (in case INCONCLUSIVE composite defers verdict to Cycle 15); any canonical-maintenance dispatch touching doc 48 between now and Cycle 15 close requires gandalf review + this A/B protocol's preservation requirement cited.

**Counter:** doc 48 STATUS line and § 0 ledger explicitly call out "preserved as A/B baseline through Cycle 15 close at minimum; do not archive without explicit gandalf + Matt sign-off." This protocol's authority chain references doc 48 PRESERVATION as a hard requirement.

---

## 11. Discipline composition

| Discipline | This protocol's application |
|---|---|
| **#11 (empirical inspection over assumption)** | Statistical methodology rigor (§ 2 small-n preamble; § 6 Bayesian framing for dim #4); per-dimension empirical data source specification; PRE-EXECUTION DATA INTEGRITY REPORT (F-14 counter); rejection of chi-squared at violated assumption |
| **#41 (pre-authored taxonomy interrogation)** | Doc 48 baseline framed as COMPARISON not PRESCRIPTION (§ 0 TL;DR + dim #1 § 3.1 + dim #5 § 7.1); non-emergence treated as substrate-vote signal not automatic failure; surprise emergence positively valued as substrate-led architectural commitment justification |
| **#42 (framing-audit at dispatch consumption)** | Pre-authoring framing-audit (Q1/Q2/Q3) executed and recorded in conversation log; vocabulary lock #45 compliance verified at every section |
| **#43 (design-quality audit at wave-close)** | Composite verdict directly feeds Discipline #43 A1-A5 audit (§ 9.3); B-PASS contributes PASS; A-PASS contributes DRIFT-DETECTED; INCONCLUSIVE contributes CONDITIONAL PASS; protocol runs AFTER Phase 7 close + BEFORE KR wave-closure commit per #43 sequencing |
| **#45 (vocabulary lock)** | Doc lives at canonical/story/ — narrative-vocabulary exemption applies BUT measurement specification uses kit/faction/substrate-anchor/cluster vocabulary throughout; references to doc 48 archetypes consistently use "candidate archetype-shape" framing per Discipline #45 anchored example #1; no "class taxonomy" usage in measurement infrastructure |
| **#46 (DB anti-materialization)** | All measurement queries are bounded — per-season filters on season_id (bounded by # kits per season ~22-40); per-cluster queries bounded by k=3-4; no unbounded cross-archive joins; Bayesian computation operates on contingency table (bounded by anchor-lineage × cluster cardinality, max ~7×5=35 cells) |
| **#40 (scaffold-with-pending-decision)** | Protocol is CURRENT (not scaffold); each dimension's acceptance criteria are NOT scaffold values — they are operational decisions per Q-AB-1/2/3 resolutions and per Sketch F architectural commitments. Drift-watch criteria are NOT pending-decisions — they are post-Wave-5 triggers for Cycle 15+ revisit. No scaffold flags. |
| **#18 (math-hotspot routing)** | Bayesian methodology for dim #4 IS a math-hotspot; specified in protocol (Dirichlet-Multinomial conjugacy); methodology-consultation with elrond reserved for F-12 prior-sensitivity discrepancy trigger (not automatic) |

---

## 12. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — A/B comparison protocol authored; READY for Wave 5 close execution
**Authority:** Matt 2026-05-27 pre-ratification #3 (6 measurement dimensions LOCKED) + KR dispatch `2026-05-27-gandalf-ab-comparison-protocol-wave-5-close.md`

**Three open questions resolved within the protocol:**
- **Q-AB-1** (dim #4 statistical test): Bayesian Dirichlet-Multinomial posterior + Bayes factor as PRIMARY; Fisher's exact supplementary; chi-squared REJECTED at violated asymptotic assumption (§ 6.2)
- **Q-AB-2** (dim #5 surprise count acceptance): ≥1 surprise at Wave 5 = B-PASS; 0 = FOLLOW-UP-DEFER (small-n cannot distinguish either-direction); 4-all-surprises = A-PASS (architectural decoupling) (§ 7.2)
- **Q-AB-3** (dim #6 throwaway threshold): dual-floor (member_count < max(3, 10% total) AND compactness < 0.40); BOTH must fail; THIN-COHERENT + FAT-INCOHERENT recorded separately (§ 8.2)

**Composition:**
- With doc 48 VESTIGIAL preservation (A baseline)
- With Phase 7 IMPL (gamora `eca0aa5` — kit_archive → gauntlet_sim bridge + 2-layer joint-gate + verdict emission)
- With G-B primary-pair selection (rocket `a466eb1` + PM-2 § 13 Mahalanobis pairwise distance)
- With F-C Phase 5 inter-faction relationship (star-lord `bf7f659` + Wave 3 dispatch)
- With Sketch F D-Sharpened substrate-anchor architecture (Path III note § 2)
- With Discipline #43 wave-close design-quality audit (composite verdict feeds A1+A2+A4)
- With Discipline #41 substrate-led architectural commitment (doc 48 framed as COMPARISON not PRESCRIPTION)
- With Discipline #45 vocabulary lock (kit/faction/substrate-anchor vocabulary throughout measurement; doc 48 references use candidate-archetype-shape framing)

**For:** the Wave 5 close measurement of whether Option α substrate-led emergence delivers a generative-architecture output equal to or better than doc 48 designer-curated baseline. Composite verdict feeds Discipline #43 design-quality audit, which gates KR wave-closure commit. B-PASS ratifies Option α for v1; A-PASS routes to Pattern B engagement with Matt; INCONCLUSIVE defers composite verdict to Cycle 15 with replication-validation workstream.

**Hand-back:** KR routes A/B comparison execution at Wave 5 close (post canonical-promoted production season at audit-gate PASS). gandalf executes protocol; produces per-dimension audit records at `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-wave-5-ab-comparison-dim-N-output.md` per dimension; produces composite verdict record at `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-wave-5-ab-comparison-composite-verdict.md`; feeds composite verdict into Discipline #43 wave-close design-quality audit record.

**Signed:** gandalf (story-and-design steward)




