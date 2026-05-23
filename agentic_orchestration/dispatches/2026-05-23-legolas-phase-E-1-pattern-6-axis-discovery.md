# Dispatch — 2026-05-23 — legolas — Phase E-1 Pattern-6 canonical axis discovery + clustering (Mode A analytical)

> **⚠️ SUPERSEDED 2026-05-23 by Phase-D-bis findings.** If you are legolas opening a fresh session today, **DO NOT EXECUTE THIS DISPATCH.** Pick up `dispatches/2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md` instead. This dispatch's methodology + acceptance criteria are still authoritative AS REFERENCED BY THE RERUN — but firing this dispatch against the pre-Phase-D-bis pool (16,699 rows) would re-execute on a substrate now known to be a `weapon_kind` filter artifact (per elrond E1 audit 2026-05-23). The corrected pool is 48,430 rows; the RERUN dispatch covers the fire against it.
>
> This file is preserved as historical record + reference (the RERUN dispatch points at this file's scope and acceptance criteria as the methodology anchor; only the pool changes).

---

**From:** knight-rider
**To:** legolas (Mode A analytical research; PCA + factor analysis + clustering)
**Approved by:** Matt 2026-05-23 (Phase D complete + verified; Phase E authorized)
**Estimated effort:** 2-3 days (Pattern-B session)
**Acceptance:** 8-12 canonical axes with loadings + 50-150 emergent clusters + per-axis interpretability check + cluster_membership table populated + designer-labeling-ready output; commit + tag

---

## Context

Phase D cleaning pipeline complete (`elrond/phase-D-cleaning-pipeline-2026-05-23`). All 4 math-anchored cleanliness gates pass empirically. The clean substrate is at:

| Surface | Count | Purpose |
|---|---|---|
| `v_category_sample` (engine-sampleable) | **16,699 rows** | Phase E primary input |
| `dedup_status='canonical'` | 6,621 | Canonical-of-record entities |
| `dedup_status='merged_into'` | 19,146 | Specimens absorbed into canonicals |
| `dedup_status='unprocessed'` | 64,074 | Mostly museum sources not in TRPG/MMO/ARPG routing; engine filter via view |
| `knowledge_entry_canonical_merge` | 1,194 components | F1 RA TIERED + F4 cross-source merges |

Gandalf's § 7.2 hybrid sequencing called for a pre-clean dirty-probe (legolas Mode A) + post-clean canonical run. **The pre-clean probe was skipped** (Phase D fired before the probe could run). Phase E-1 is the post-clean canonical Pattern-6 run on the post-Phase-D clean substrate — the load-bearing axis-discovery work.

Per gandalf cleaning-policy-design § 4.1 (algorithmic touchpoints):
- **Method primary:** PCA on per-row feature vectors (Matt F5-locked)
- **Method secondary:** Factor analysis (interpretable rotations); NMF (non-negative substrate features) optional
- **Input:** text-embedding (~384-768 dim) + structured-feature-vector (~30-50 dim after one-hot) per row
- **Output:** ~8-12 canonical axes with loadings; designer-labelable in Phase E-2
- **Stability anchor:** N=16,699 well above N≥10p threshold; top-k loadings expected stable

Per hive-mind-protocol § 6 Phase 3:
- **Clustering method candidates:** HDBSCAN (density-based; no k pre-specification), Gaussian Mixture Models (parametric with soft assignment), k-means (baseline)
- **Input:** derived axis loadings from PCA (8-12 dim) + categorical encodings (`weapon_kind`, `cultural_lineage_canonical`, `historical_period_canonical`, `register_canonical`)
- **Output:** 50-150 emergent clusters per acceptance criterion
- **Stability anchor:** HDBSCAN min_cluster_size=20-50 for substrate this size; cluster purity ≥ 0.85 per gandalf § 4.3

## Required reading before starting

1. **`canonical/story/cleaning-policy-design-2026-05-22.md`** — gandalf framework; read § 4.1 (algorithm touchpoints), § 5 (canonical taxonomy), § 7 (sequencing rationale)
2. **`agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md`** — Phase D state-of-substrate post-cleaning; especially § 7.3 (recall variance — affects how you interpret merged_into vs unprocessed)
3. **`agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-flagged-clusters.md`** — borderline clusters elrond flagged; affects your understanding of cross-source merge boundaries
4. **`agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md`** — schema delta + per-consumer impact assessment
5. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/per-source-quality.md` — per-source classification distributions
6. `agentic_orchestration/weapon-library-import-hive-mind-state.md` — Cycle 9.5-9.6 live state
7. Schema (post-Phase-D): `weapon_knowledge_entries` now includes `wieldable_humanoid`, `weapon_kind`, `dedup_status`, `variant_relationship`, `cultural_lineage_canonical`, `historical_period_canonical`, `register_canonical`, `cultural_lineage_confidence`, `template_quality_score`. View `v_category_sample` is your primary query surface.

## Math-before-code

Yes. Per Discipline #1, required BEFORE analytical code fires:

### Math note — Phase E-1 execution plan

Author at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-math-note.md`. Required content:

1. **Feature engineering plan.** What features per row do you compute? Text-embedding source (which model; legolas Q5-equivalent decision); structured-feature-vector composition (which columns, one-hot or ordinal encoding, normalization). Total feature dimensionality.
2. **PCA chunk strategy.** N=16,699 × p≈800 ≈ 13M cells — fits in memory but plan if not. Algorithm choice (randomized PCA / truncated SVD / full PCA). Top-k retention strategy (variance-explained ≥ 80% OR scree-plot kink).
3. **Per-axis loading interpretability check.** How do you verify each axis loads meaningfully (not on noise / single-feature)? Loading magnitude floors; top-N loading features per axis.
4. **HDBSCAN parameter selection.** min_cluster_size + min_samples + cluster_selection_epsilon. Anchor to substrate scale (16,699 rows → cluster_size ~20-50 per gandalf § 4.3).
5. **Stability check.** Bootstrap or cross-validation strategy: how do you verify top-k axes are stable across 5-10 bootstrap resamples?
6. **F2 inverse-frequency weighting application.** Per Matt F2-locked: cultural-lineage axis bias correction. How do you apply weights (per-row weight = 1/freq(lineage) normalized)? On PCA only? On clustering too?
7. **Acceptance gate verification queries.** Pre-author the checks that verify Phase E-1 acceptance.

The math note is jack-ryan Gate-2 reviewable at your discretion. Knight-rider recommends Gate-2 if you adopt non-trivial algorithm choices.

## Cross-seam contract change? (Principle 6 gate)

**Partial yes — populating new tables.** Per ADR-004:
- New rows written to: `clusters` table (cluster definitions + axis loadings JSON) and `cluster_membership` table (per-row cluster assignment + soft-assignment probability).
- No schema migration (tables exist from Phase 0; schema v1.1.0). No ALTER TABLE.
- No row modification on `weapon_knowledge_entries` (you populate `cluster_id` foreign key on those rows but do not modify other columns).

**MIGRATION.md required if cluster_id population on `weapon_knowledge_entries` affects any downstream consumer.** Document per ADR-004 at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`. Forward-compat declaration expected (cluster_id was NULL pre-Phase-E; now populated; existing readers unaffected).

**Round-trip smoke:** Required. Production-path fixture: 100-row sample from v_category_sample; pass through your axis-loading + clustering pipeline; verify each row has cluster_id populated AND axis-loading JSON parses; verify `clusters` table has 50-150 rows.

## Locked decisions (apply; do not re-open)

| ID | Decision | Operational |
|---|---|---|
| F2 | Cultural-lineage weighted inverse-frequency | Apply per-row weights during PCA + clustering; not stratified sampling |
| F5 | Pattern-6 starting method | PCA primary; factor analysis for interpretable rotation; HDBSCAN primary clustering. If empirical evidence shows PCA insufficient (e.g., bimodal loadings; non-linear structure), document as Phase E-1-bis flag for Matt review — do NOT switch methods unilaterally. |
| F6 | Sample-pool size N=20-50 for category sampling | Phase E-1 emits clusters that downstream consumes at N=20-50 per cluster; if any cluster has <20 members, flag for cluster-merging-or-split decision in Phase E-2 |
| Phase-D output schema | All canonical columns populated per Phase D completion | DO NOT re-derive cultural_lineage / historical_period / register — use the canonical columns from Phase D |
| Phase-D `merged_into` semantics | Specimens absorbed; canonical-of-record represents the cluster | Operate on `v_category_sample` (canonical + unprocessed) — do not include merged_into rows; they are downstream consumption-time joined |

## Scope (Phase E-1 deliverables)

### Deliverable 1 — Feature engineering

Author at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-features.md` documenting:
- Text-embedding model used (with reproducibility hash if applicable)
- Structured-feature-vector composition (which columns, encoding, normalization)
- Total dimensionality + per-component dimensionality
- Feature-coverage check (how many rows have full feature vectors vs imputed defaults)
- Inverse-frequency weight vector per cultural_lineage_canonical bucket (F2-locked)

### Deliverable 2 — Axis discovery output

Run PCA + factor analysis on the 16,699-row × p-dim feature matrix (weighted per F2). Output at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-discovery.md` + structured JSON at `phase-E-1-axis-loadings.json`.

Per axis:
- Index (1-12)
- Variance explained
- Top-N loading features (rank-ordered by loading magnitude)
- Loading distribution (heavy-on-one-feature vs spread)
- Bootstrap stability score (mean cosine-distance from bootstrap-resample loadings)
- Provisional axis-name proposal (legolas's first-pass interpretation; gandalf labels canonically in Phase E-2)

Target: **8-12 canonical axes** retained (above variance + stability floors per math note).

### Deliverable 3 — Clustering output

Run HDBSCAN + GMM-baseline + k-means-baseline on the axis-loading projections (8-12 dim) + categorical features. Output at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-clusters.md`.

Per cluster:
- Cluster ID
- Member count
- Centroid axis loadings
- Top-3 representative rows (highest soft-assignment probability)
- Per-cluster characteristic features (which structured features dominate; which canonical taxonomy values concentrate)
- Provisional cluster description (legolas's first-pass; gandalf labels in Phase E-2)

Target: **50-150 emergent clusters** with HDBSCAN min_cluster_size=20-50.

### Deliverable 4 — Database population

Populate two tables:
1. `clusters` table — one row per discovered cluster; columns include cluster_id, axis_loadings JSON, characteristic_features JSON, member_count, provisional_description
2. `cluster_membership` table — one row per (weapon_knowledge_entries.id, cluster_id) pair with soft-assignment probability

Additionally update `weapon_knowledge_entries.cluster_id` column (FK to clusters) for v_category_sample rows.

### Deliverable 5 — Phase E-1 completion summary

Author at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-completion-summary.md`:
- Per-deliverable artifact path
- Acceptance gate verification (see below)
- Phase E-2 (gandalf labeling) hand-off notes
- Any anomalies or unexpected axes (flagged for Matt+gandalf review)

## Acceptance criteria

- [ ] Math note authored at `phase-E-1-math-note.md` BEFORE analytical code fires
- [ ] MIGRATION.md authored (or declared not-applicable with cluster_id consumer verification)
- [ ] Feature engineering deliverable authored with reproducibility hash
- [ ] 8-12 canonical axes discovered with loadings + bootstrap stability scores
- [ ] Per-axis bootstrap stability mean cosine-distance ≤ 0.10 (per gandalf § 4.2 PCA stability anchor)
- [ ] 50-150 emergent clusters with HDBSCAN min_cluster_size=20-50
- [ ] Per-cluster purity ≥ 0.85 (per gandalf § 4.3 HDBSCAN purity floor)
- [ ] `clusters` + `cluster_membership` tables populated
- [ ] `weapon_knowledge_entries.cluster_id` populated for v_category_sample rows
- [ ] Round-trip smoke: 100-row sample passes axis-loading + clustering; cluster_id populated; loadings JSON parses
- [ ] F2 inverse-frequency weighting applied + documented
- [ ] Phase E-1 completion summary authored with Phase E-2 hand-off notes
- [ ] Round-trip smoke artifact + completion record appended to this dispatch file
- [ ] Tag: `legolas/phase-E-1-axis-discovery-2026-05-23`

## Out of scope (explicit non-goals)

- **DO NOT** modify gandalf's policy docs, elrond's Phase D scripts, or Phase D acceptance gates
- **DO NOT** re-execute Phase D cleaning steps (those are durable; you read post-Phase-D state)
- **DO NOT** assign canonical semantic labels to axes or clusters (gandalf's Phase E-2 job; you provide provisional first-pass interpretations only)
- **DO NOT** decide on the borderline G2-class cross-source clusters (elrond's `phase-D-flagged-clusters.md` surfaces them; gandalf disposes in Phase E-2)
- **DO NOT** lock the methodology if PCA shows non-linear-structure evidence — surface the evidence as a Phase E-1-bis flag; preserve F5 lock until Matt re-opens
- **DO NOT** populate Phase 5 substrate-density precomputation (separate dispatch; elrond owns)
- **DO NOT** push tags to origin — per ADR-001 only Matt approves tag-promotion; you create local tags only

## Open questions for you to resolve + document

1. **Text-embedding model choice.** Phase D elrond pivoted to sklearn TF-IDF cosine due to sentence-transformers unavailability (~700MB torch install). Does Phase E-1 install sentence-transformers (worth the dependency for better axis discovery) OR continue with TF-IDF? Document choice + reproducibility implications.
2. **Imputation strategy for unprocessed rows.** Most museum rows are `dedup_status='unprocessed'` but in v_category_sample. Do you treat them as canonical-of-record for Phase E-1 (since v_category_sample is your input)? Document.
3. **Multi-cluster soft-assignment threshold.** HDBSCAN naturally produces noise points (cluster_id = -1). Do you assign noise to nearest-cluster via soft-assignment probability, or leave as cluster_id NULL? Document.
4. **PCA whitening + scaling.** Standard-scale features before PCA? Per-feature variance can dominate without scaling. Document choice.
5. **Cluster-purity measurement.** "Purity" against what label? Cultural_lineage? Historical_period? Multi-axis composite? Document the purity-measurement-key.
6. **Provisional axis-name proposals.** Are you allowed to propose semantic names (e.g., "edged-vs-blunt")? Yes, but mark them PROVISIONAL — gandalf's Phase E-2 is canonical authority. Make sure your axis-names doc is annotated `PROVISIONAL — gandalf reviews in Phase E-2` in the header.
7. **Phase E-1-bis trigger.** If PCA loadings show non-linear / multi-modal structure (e.g., 2 separate modes per axis instead of a unimodal distribution), surface as Phase E-1-bis-flag for Matt review. The F5 lock holds PCA as starting method; if it's empirically insufficient, the lock can be re-opened by Matt with evidence.

## References

### Phase D upstream (load-bearing)
- `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md`
- `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-flagged-clusters.md`
- `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md`
- `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md`

### Phase B + Phase B-2 framework
- `canonical/story/cleaning-policy-design-2026-05-22.md` (gandalf § 4, § 5, § 7)
- `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` (gandalf 26-cluster policy)

### Phase A baseline
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/per-source-quality.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/cleanliness-baseline.md`

### Disciplines
- #1 math-before-code — math note authored first
- #11 audit-preservation — cluster assignments preserved with soft-probability for re-runnability
- #19 right tool / smoke-test discipline — round-trip smoke on 100-row sample before full fire

### Prior tags in campaign chain
- `elrond/phase-D-cleaning-pipeline-2026-05-23` (Phase D final; local-only; awaiting Matt push)
- `knight-rider/cycle-9-5-phase-D-gate-1-passed-2026-05-23`
- `gandalf/variant-cluster-policy-2026-05-23`
- `gandalf/cleaning-policy-design-review-2026-05-22`
- `legolas/phase-A-substrate-audit-2026-05-22`

---

## Tag at completion

```
legolas/phase-E-1-axis-discovery-2026-05-23
```

(Seam-prefix per ADR-001; intermediate analytical artifact; not Matt-milestone tag. Milestone-tag candidate after Phase E-2 + E-3 + E-4 complete is `v0.3-weapon-library-pattern-6-locked` — requires Matt approval.)

## Phase E chain (E-2, E-3, E-4 — knight-rider authors after your return)

| Phase | Owner | Scope | Estimated effort |
|---|---|---|---|
| E-1 | **legolas (THIS DISPATCH)** | Axis discovery + clustering + cluster_membership population | 2-3 days |
| E-2 | gandalf | Designer labeling of 8-12 axes + 50-150 clusters | 1 day |
| E-3 | Matt (synchronous review) | Lock canonical axis names + cluster labels | 1 session |
| E-4 | elrond | Substrate-density precomputation (`substrate_density` table per hive-mind-protocol § 0 acceptance) | 1 day |

Phase E-2 dispatch will reference your Phase E-1 outputs (axis loadings + cluster definitions) so gandalf can semantically label them.

---

## What happens after you return

Knight-rider:
1. Reads your Phase E-1 completion summary + reviews axis loadings + cluster definitions
2. Surfaces any Phase E-1-bis flags (non-linear structure evidence; cluster boundary anomalies) to Matt for methodology re-open decision
3. Authors Phase E-2 gandalf dispatch (designer labeling)
4. Coordinates Matt-side review at Phase E-3 (label-locking + milestone-tag promotion)
5. Authors Phase E-4 elrond dispatch (substrate-density precomputation)

After Phase E-4 lands and Matt approves milestone tag promotion, the weapon-library substrate is **Pattern-6 locked** and ready for engine consumption (rocket's content-gen seam).

---

**Signed:** knight-rider (dispatch authored 2026-05-23 ~03:00 EDT; Phase E-1 fires next)
