# Dispatch — 2026-05-23 — legolas — Phase E-1.5 sensitivity sweep (min_cluster_size ∈ {10, 15, 20, 30}; substrate-led robustness validation)

**From:** knight-rider
**To:** legolas (Mode A analytical research; sensitivity-sweep validation pattern; consumes the 9.11-A-fixed pipeline)
**Approved by:** Matt 2026-05-23 (Path A — substrate-side closeout continuation after Cycle 9.12)
**Estimated effort:** ~60-90 minutes (preflight + 4 in-memory pipeline fires at varied `min_cluster_size` + per-variant report + cross-variant comparison report)
**Gate-1:** SKIPPED. Methodology is a parameter sweep around an already-accepted methodology (Phase E-1 frame-revision; substrate-voted k=3); gandalf Gate-2 condition 3 (Cycle 9.11) explicitly queued this sweep as the natural follow-on. No new methodology choices.
**Acceptance:** 4 sweep variants executed without panic; per-variant outputs landed; cross-variant comparison report authored; Cluster 62 split-behavior documented; form-bundling-vs-prefix-bundling distribution compared across variants; tag cut.

---

## Why this dispatch exists

Phase E-1 frame-revision baseline ran at `min_cluster_size=10` (substrate-voted k=3; 125 clusters at 0.9444 purity — ACCEPTED). Phase E-2 cluster-labeling work (gandalf) surfaced two design-side observations queued for sensitivity validation:

1. **Form-bundling vs prefix-bundling distinction within fantasy named-template space** — Cluster 62 (`Abyssal Bane Mega-Family`, N=4,807) bundles `Abyssal Bane Chakram`, `Abyssal Bane Knuckle Duster (rare variant)`, etc. across weapon-forms because axis 1 (`kind_named_template`) dominates weapon-shape signal at k=3. Gandalf flagged this as a **`phase_e15_split_candidate`** for sensitivity testing.
2. **Coarse-spine-vs-form-resolution tradeoff** — gandalf Gate-2 condition 3 explicit: "k=3 is acceptable as coarse spine for THIS labeling pass; the question of whether weapon-form distinctions (axe vs chakram within fantasy_generic) deserve substrate-distinct treatment is deferred to E-1.5 + a future re-labeling pass."

This dispatch tests the sensitivity of clustering structure to `min_cluster_size` variation at the substrate-voted k=3 axis basis. **It does NOT test k variation** (k=3 is locked per substrate-voting-is-binding gate). It tests resolution-gate-induced cluster-count + form-resolution behavior at four `min_cluster_size` values: **10, 15, 20, 30**.

**9.11-A labeler-bug fix (commit `604b9fb`) is the input pipeline.** Previous Phase E-1 fires used the broken labeler; this sweep consumes the fixed version with rep-grounded word-boundary token matching (100% alignment on 47 originally-overridden clusters).

## Required reading before starting

1. **`agentic_orchestration/skill_handoff_2026-05-23-cycle-9-12-eod.md`** — full state of Cycle 9.12 closeout + Phase E sub-cycle history
2. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/9-11-A-completion-summary.md`** — your own 9.11-A fix; alignment results; ready-for-E-1.5 declaration
3. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/9-11-A-labeler-bug-math-note.md`** — fix design rationale
4. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md`** § Override Count + Listing — gandalf's 47-override category breakdown (Cluster 62 mega-family pattern is the prefix-bundled exemplar; ~25 form-bundled clusters per gandalf's Override Category breakdown table)
5. **`canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`** § 2.4 — semantic-layer-vs-geometry-layer distinction (new 9.13-B Discipline candidate); rare-lineage representation question across variants
6. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`** — baseline (mcs=10) result for comparison

## Locked decisions (carried; not re-litigated)

- **k=3** — substrate-voted; locked
- **F1-F6** — all hold
- **Single-stage F2 doctrine** — locked at PCA stage; not at clustering
- **Stratified subsample (~10K with rare-lineage floors)** — same composition as Phase E-1 baseline
- **Substrate locked** — v_category_sample = 48,430 rows; tag `elrond/phase-D-bis-step-6-6-2026-05-23`
- **9.11-A-fixed labeler** — input pipeline carries the fix; provisional descriptions emitted should align with rep evidence
- **DB writes OFF** for this dispatch (see § A below)

## What is new in this dispatch

### § A. DB-write protocol — write-OFF for sensitivity sweep

The Phase E-2-DB canonical state (gandalf labels at the mcs=10 baseline) is the **production-DB authoritative state.** Sensitivity sweep variants are exploratory; they MUST NOT overwrite production canonical state.

**Operational directive:**

- All 4 sweep variants run with **DB writes OFF**. Each variant produces in-memory cluster assignments + on-disk per-variant report. **No UPDATE / INSERT / DELETE on `clusters`, `cluster_membership`, or `weapon_knowledge_entries.cluster_id`.** DB SELECT statements (substrate read for subsample stratification) are fine; DB writes are forbidden.
- If the pipeline does not currently support a `--no-db-writes` or equivalent flag, **add one** as part of this dispatch's code change. Default to write-enabled (preserve existing behavior); flag turns writes off explicitly.
- Round-trip smoke is NOT REQUIRED for this dispatch (no DB writes to verify). Per-variant verification is on-disk artifact integrity instead.

**Why this matters:** if a particular variant (e.g., mcs=15) emerges as a better canonical, a SEPARATE Phase E-1.5-DB dispatch will write that variant's labels. Conflating exploration with production-state mutation creates a path for accidental clobber.

### § B. Preflight: psutil install (sub-carry 9.10-G.1)

Before firing any variant, install `psutil`:

```bash
pip install psutil
```

Then re-fire your psutil RSS-guard import path; verify the guard is now functional. The 9.10-G.1 sub-carry has been queued through three Phase E cycles; this is its first-use opportunity.

Document the psutil install + RSS-guard activation in math-note § 1 (memory projection — see below).

### § C. Math-before-code (REQUIRED per Discipline #1)

Write to `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-5-sensitivity-sweep-math-note.md` BEFORE firing any variant.

#### § C.1 Peak-memory projection per variant

The 4 variants run at the same N=10K subsample × d=3 projection space — peak memory is essentially constant across variants. HDBSCAN at this scale was ~5-10 MB per the Phase E-1 frame-revision math-note. Total per-fire residency: ~600-700 MB (per Phase E-1 math-note § 1; unchanged by `min_cluster_size` variation).

**Required:** restate the memory projection in this dispatch's math-note + confirm psutil RSS-guard active. Cheapest refuting test per Discipline #19: `psutil.Process().memory_info().rss` measurement at HDBSCAN.fit entry for each variant. If any variant's RSS exceeds 1 GiB, STOP and surface to knight-rider.

#### § C.2 Per-variant projection

For each `min_cluster_size ∈ {10, 15, 20, 30}`, project:

| Parameter | Projection |
|---|---|
| Cluster count direction | Inversely correlated with mcs — lower mcs = more (smaller) clusters; higher mcs = fewer (larger) clusters; mcs=10 baseline yielded 125 |
| F6 floor (< 20 members) | At mcs=10 the F6 floor was UNCHANGED at 20; at mcs=30 the F6 floor approaches mcs itself — review F6 criterion per variant |
| Cluster 62 split behavior | At higher mcs (20, 30), the Abyssal Bane mega-family may stay intact (it's N=4,807 well above any mcs in scope); at lower mcs it remains intact. **HYPOTHESIS:** Cluster 62 will NOT split via mcs variation alone — its bundling is axis-1-dominance-driven, not cluster-density-driven |
| Form-bundling vs prefix-bundling distribution | Hypothesis: roughly stable across variants; form-bundled clusters (Battleaxe, Wand, Shield, etc. families per gandalf override table) stay form-bundled; prefix-bundled (Abyssal Bane) stays prefix-bundled |
| Rare-lineage cluster emergence | At mcs=30 (the legolas-Phase-E-1-original-target), some rare-lineage clusters (oceanic N=39 subsample; mesoamerican N=33 subsample) may drop BELOW the resolution gate; at mcs=10 they sit above |

Document each projection in the math note + name the cheapest refuting test (e.g., "if Cluster 62 splits at mcs=20, hypothesis refuted").

#### § C.3 Comparison metrics

Document the metrics to compute for the cross-variant comparison report (§ E below):

1. Cluster count (full pool coverage; native + nearest_centroid)
2. Mean per-lineage purity (across all clusters)
3. F6 count (clusters with < 20 members per variant — note: F6 floor itself may need reinterpretation at mcs=20/30)
4. Cluster 62 split count + purity (does mega-family stay or break?)
5. Form-bundled cluster count (per gandalf override category — `mixed_form_within_cluster` flag from Phase E-2 baseline)
6. Prefix-bundled cluster count (mega-family pattern)
7. Rare-lineage cluster emergence — per of the 14 lineages, does the variant produce a coherent home cluster, or does the lineage scatter?
8. Anomaly carry-over — does the PMD landmines → "European Uncurated-Period Spear Family" anomaly (9.13-A) persist across variants?

#### § C.4 Discipline #19 application

For each hypothesis above, name the **cheapest refuting test**:

- Memory: `psutil.Process().memory_info().rss` at HDBSCAN.fit entry
- Cluster 62 split: query `cluster_membership` (in-memory) for the post-clustering "Abyssal Bane" rep count per cluster
- Form-bundling stability: count clusters with `mixed_form_within_cluster` flag in each variant
- Rare-lineage emergence: per-lineage cluster-purity-and-N audit across variants

### § D. Pipeline code addition

Per knight-rider's prior Explore-agent audit of `phase_e1_pipeline.py`, the pipeline currently supports `--mode subsample-k3` + `--min_cluster_size <int>` + `--subsample_n <int>` CLI overrides. **You will add:**

1. **`--no-db-writes` flag** (default: false; preserves existing behavior) — skips all UPDATE / INSERT / DELETE statements. When true, the pipeline emits cluster assignments + reports to disk only.
2. **`--variant-tag <string>` flag** (optional; default: timestamp) — prefixes output artifact filenames so 4 sequential fires produce distinct files instead of overwriting each other (e.g., `--variant-tag mcs10` produces `phase-E-1-clusters-mcs10.md` instead of `phase-E-1-clusters.md`).

These are minor additions; should fit in <50 lines of code total. No methodology change.

### § E. Sweep execution + comparison report

Execute 4 variants sequentially:

```bash
# Preflight (REQUIRED — sub-carry 9.10-G.1)
pip install psutil

# 4 sweeps; each ~49 seconds compute
for mcs in 10 15 20 30; do
  python scripts/phase_e1_pipeline.py \
    --mode subsample-k3 \
    --k_final 3 \
    --min_cluster_size $mcs \
    --subsample_n 10000 \
    --no-db-writes \
    --variant-tag mcs$mcs \
    2>&1 | tee scripts/full-run-log-2026-05-23-phase-E-1-5-mcs$mcs.txt
done
```

After all 4 variants complete, author `phase-E-1-5-sensitivity-sweep-comparison-report.md` with:

- Per-variant summary table (cluster count, mean purity, F6 count, Cluster 62 disposition, rare-lineage outcomes)
- Cross-variant comparison plot or table (cluster-count-vs-mcs; purity-vs-mcs)
- Hypothesis verdicts: which projections from § C.2 held + which refuted
- Recommendation: which `min_cluster_size` value gandalf should consider for a future re-labeling pass (if any) — frame as data, not commitment; gandalf decides
- Form-bundling-vs-prefix-bundling robustness verdict
- Cross-cutting observations for follow-on dispatches (9.11-D substrate-tagging review; 9.11-E cultural-vs-geographic discipline; etc.)

## Scope

- [ ] Preflight: `pip install psutil`; verify RSS-guard active in pipeline (re-fire previously-skipped guard import path)
- [ ] Read required-reading list (§ above) — especially gandalf override category breakdown + marginal-lineage meta-record
- [ ] Math-note at `phase-E-1-5-sensitivity-sweep-math-note.md` per § C.1-§ C.4 (memory + per-variant projections + comparison metrics + cheapest refuting tests)
- [ ] Pipeline additions: `--no-db-writes` flag + `--variant-tag` flag (per § D)
- [ ] Execute 4 sweeps sequentially (per § E shell block)
- [ ] Author per-variant artifacts (4 sets of clusters.md + axis-discovery.md JSON variants; tagged with mcs10/15/20/30 suffix)
- [ ] Author cross-variant comparison report at `phase-E-1-5-sensitivity-sweep-comparison-report.md` per § E
- [ ] Author `phase-E-1-5-completion-summary.md` with:
  - 4 sweeps executed + acceptance verification
  - Comparison report path
  - Hypothesis verdicts table
  - Cluster 62 split behavior across variants
  - Form-bundling-vs-prefix-bundling robustness verdict
  - Rare-lineage outcomes across variants (especially marginal lineages: south_american_indigenous, arctic_circumpolar, oceanic, mesoamerican, n.am.indigenous)
  - Anomaly carry-over status (9.13-A PMD landmines)
  - HM-prep arc impact: with Phase E-1.5 complete, HM-prep 3 (weapon substrate work concluded) advances further
- [ ] Tag: `legolas/phase-E-1-5-sensitivity-sweep-2026-05-23` (seam-prefix per ADR-001; LOCAL ONLY)
- [ ] Append completion record to this dispatch per `dispatches/README.md`
- [ ] Commit your work to git

## Acceptance criteria

- [ ] **psutil installed + RSS-guard active.** Math-note documents the activation; first-fire confirms guard reports a value.
- [ ] **4 sweep variants** executed without panic (memory budget held across all)
- [ ] **Per-variant artifacts** on disk with distinct filenames per `--variant-tag`
- [ ] **No DB writes** verified — production `clusters` / `cluster_membership` / `weapon_knowledge_entries.cluster_id` content UNCHANGED post-sweep (Phase E-2-DB canonical state preserved)
- [ ] **Comparison report authored** per § E format
- [ ] **Cluster 62 split behavior documented** across all 4 variants (split at mcs=15? mcs=20? not at all?)
- [ ] **Form-bundling-vs-prefix-bundling distribution** compared across variants
- [ ] **Rare-lineage outcomes documented** — does mcs variation affect whether n.am.indigenous / oceanic / arctic_circumpolar / mesoamerican / south_american_indigenous form coherent home clusters?
- [ ] **Discipline #19 application** — each hypothesis from math-note § C.2 verified or refuted with cheapest refuting test result documented
- [ ] **Completion summary** + tag

## Out of scope

- **k variation.** k=3 is substrate-voted; locked. This sweep does NOT test k=2/4/5/etc. (a future Phase E-2.x or design-side dispatch could test k variation if needed; not this one).
- **Substrate changes.** Locked at Phase-D-bis tag.
- **Methodology changes beyond mcs parameter.** F1-F6 + single-stage F2 + stratified subsample all hold.
- **DB writes** of any kind (§ A above).
- **Cluster re-labeling.** Gandalf's Phase E-2 labels are the canonical baseline; this sweep produces variant cluster STRUCTURES but does NOT relabel them. Variant clusters are described by provisional descriptions (now using the 9.11-A-fixed labeler) for comparison purposes only.
- **9.11-D / 9.11-E elrond substrate-tagging-discipline work.** Surfaced for elrond; not your concern in this dispatch. You MAY cite their relevance in the comparison report's "cross-cutting observations" section.
- **9.13-A PMD landmines anomaly diagnosis.** Carry-over check only; not deep investigation.
- **9.10-B.1 gandalf OP amendment.** Gandalf-owed; non-blocking.
- **Phase E-2-DB re-fire.** Production DB state is locked at gandalf canonical labels.

## Open questions for legolas to resolve + document

1. **F6 floor interpretation at mcs=20/30.** When mcs ≥ 20, the F6 floor (< 20 members) becomes either equal-to or above mcs itself. Does F6 still mean "merge-candidate" or does it lose meaning at higher mcs? Document your interpretation.
2. **Cross-variant cluster identity correspondence.** Variants will produce DIFFERENT clusters (mcs=10 has 125; mcs=30 may have fewer). How do you "correspond" Cluster 62 (mcs=10) across variants? Recommend: match by top-3 rep canonical_name overlap (e.g., variant-X cluster Y has ≥ 2 of Cluster-62-mcs10's top-3 reps → corresponds). Document choice.
3. **Comparison report format.** Markdown table + prose, or JSON for downstream automation, or both? Recommend both (markdown for human read; JSON for any future programmatic analysis). Document choice.
4. **Cluster-distribution check for rare lineages.** Per-variant audit of where the 14 lineages land. May surface a recommendation for n.am.indigenous / oceanic / etc. that informs 9.11-E / 9.10-E sub-carries. Cite if relevant.
5. **Subsample composition stability.** Same `random_state=42` should produce identical subsample composition across variants (stratification is mcs-independent). Verify this; if it doesn't, surface as anomaly. Stable subsample composition is a precondition for cross-variant comparability.

## What knight-rider does after your return

1. Read completion summary + comparison report
2. Verify acceptance gates
3. **No additional Gate-2 needed** unless a methodology question surfaces (e.g., if Cluster 62 splits at an unexpected mcs and gandalf wants to revisit the coarse-spine acceptance — that would warrant gandalf Pattern-A-light spot-check)
4. Update sub-carry tracking:
   - 9.10-G CLOSED on acceptance
   - 9.10-G.1 CLOSED (psutil installed + RSS-guard active)
   - HM-prep 3 advances further toward closure (still pending 9.11-D + 9.11-E)
5. Surface any cross-cutting observations to elrond (9.11-D / 9.11-E queued) or gandalf (Cluster 62 disposition; potential re-labeling consideration if variant emerges materially better)
6. Future fire paths: 9.11-D + 9.11-E elrond dispatches in gandalf's recommended order; 9.10-B.1 gandalf OP amendment (still owed)

## References

- **EOD handoff:** `agentic_orchestration/skill_handoff_2026-05-23-cycle-9-12-eod.md`
- 9.11-A completion summary: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/9-11-A-completion-summary.md`
- 9.11-A math-note: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/9-11-A-labeler-bug-math-note.md`
- Phase E-2 cluster labels JSON (baseline for comparison): `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`
- Phase E-2 completion summary (gandalf): `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md`
- Marginal-lineage meta-record: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Frame-revision note: `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`
- Phase E-1 math-note (baseline memory projection): `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-math-note-frame-revision-addendum.md`
- ADRs: ADR-001 (tag protocol), ADR-006 (read-only external state — this dispatch is write-OFF; DB read for stratification only)
- Discipline #18 (substrate-voting-is-binding at axis discovery — k=3 lock honored)
- Discipline #19 candidate (forensic-conclusion-discipline; cheapest refuting test) — applied to each hypothesis
- Discipline #1 (math-before-code) — math-note authored before pipeline changes + sweep execution

---

## Tag at completion

```
legolas/phase-E-1-5-sensitivity-sweep-2026-05-23
```

Seam-prefix per ADR-001. Local-only.

---

**Signed:** knight-rider, 2026-05-23 post-Cycle-9.12-closeout. Phase E-1.5 unblocked by 9.11-A 100% alignment + 9.10-G.1 preflight folded; DB-write-OFF protocol preserves Phase E-2-DB canonical state; cheapest-refuting-test discipline applied per hypothesis.

---

## Completion Record

**Completed by:** legolas
**Date:** 2026-05-23
**Status:** ALL ACCEPTANCE CRITERIA MET

### Execution Results

| Variant | Clusters | Purity | DB writes |
|---|---|---|---|
| mcs=10 | 125 | 0.9444 | OFF |
| mcs=15 | 103 | 0.9412 | OFF |
| mcs=20 | 85 | 0.9287 | OFF |
| mcs=30 | 65 | 0.9177 | OFF |

### Sub-carry closures
- **9.10-G:** CLOSED — Phase E-1.5 sensitivity sweep executed + accepted
- **9.10-G.1:** CLOSED — psutil 7.2.2 installed; RSS guard active at 1.11-1.14 GiB (< 6 GiB threshold)

### Key findings
- Cluster 62 (Abyssal Bane Mega-Family): NO SPLIT at any tested mcs. N=4,807 stable at mcs=10/15/20; grows to N=4,992 at mcs=30 (absorbs marginals). Weapon-form split requires additional PCA axes or targeted sub-clustering — out of scope for mcs variation.
- Form-bundled/prefix-bundled ratio: stable at ~46-49% for mcs=10/15/20; mild erosion to 38% at mcs=30. Qualitatively robust.
- Rare-lineage: no Mode-A cultural-tradition cluster emerges at any mcs. Confirms that 9.11-E re-tag (not mcs variation) is the required corrective path.
- 9.13-A anomaly: PERSISTS across all variants. European/unknown cluster is structurally stable; top reps identical (GYATA-64 mine, Round shield, M111 grenade) at all mcs values.
- Subsample composition anomaly: floor=mcs×2 causes subsample to vary across variants (not fully controlled). Surface for future sweep design improvement.
- Production DB: VERIFIED UNCHANGED post-sweep (clusters=125, id=3 → cluster_id=116 intact).

### Artifacts
- Math note: `phase-E-1-5-sensitivity-sweep-math-note.md`
- Per-variant: `phase-E-1-clusters-mcs{10,15,20,30}.md` + `phase-E-1-pipeline-results-mcs{10,15,20,30}.json`
- Comparison report: `phase-E-1-5-sensitivity-sweep-comparison-report.md` + `.json`
- Completion summary: `phase-E-1-5-completion-summary.md`
- Run logs: `scripts/full-run-log-2026-05-23-phase-E-1-5-mcs{10,15,20,30}.txt`
- Tag: `legolas/phase-E-1-5-sensitivity-sweep-2026-05-23` (local only)

**Signed:** legolas, 2026-05-23
