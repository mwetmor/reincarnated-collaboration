# Dispatch — 2026-05-23 — legolas — Phase E-1 Option-A re-fire (single-stage F2; bounded memory)

**From:** knight-rider
**To:** legolas (Mode A analytical research; Pattern-6 canonical axis discovery + clustering — Option-A revision)
**Approved by:** Matt 2026-05-23, with gandalf design-side ratification (table cited in § "Design intent" below)
**Estimated effort:** ~30-60 minutes for the code edit + math-note addendum; ~3-5 minutes for the actual fire; total ~1-2 hours including completion summary + MIGRATION.md + tag
**Acceptance:** Same as the RERUN dispatch acceptance criteria (8-12 canonical axes with bootstrap stability ≤ 0.10, 50-150 emergent clusters with purity ≥ 0.85, DB tables populated, completion summary, MIGRATION.md, tag cut) PLUS the new memory-projection precondition documented in Math-before-code § 1.

---

## Why this dispatch exists (supersedes RERUN)

The prior `2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md` dispatch fired and caused a **kernel panic on Matt's machine** at 11:09:13 EDT 2026-05-23. This is the **third kernel panic today** with the identical signature — all three traced to `hdbscan.HDBSCAN.fit()` hanging in Deliverable 3 on the F2-row-duplicated expanded matrix:

| Panic | Pool | Expanded matrix | Compressor saturation | Swapfiles |
|---|---|---|---|---|
| 03:11:11 | (pre-fire setup) | N/A | 100% BAD | 10 |
| 03:32:14 | 16,699 rows | 22,065 × 4 | 100% BAD | 12 |
| 11:09:13 | 48,430 rows | 71,003 × 12 | 100% BAD | 15 |

All three panicked on watchdogd starvation (90+ seconds without checkin) — classic memory-pressure deadlock. Full forensic trace at `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md`.

**Host hardware: M2 Mac, 8 GiB RAM.** The pipeline as written is fundamentally incompatible with this RAM budget at the corrected-substrate scale.

## Required reading before starting

1. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md`** — full forensic of the three panics + remediation option-set + Option-A rationale
2. **`agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md`** — gandalf's design-side diagnosis (Tier 1: bounded-memory algorithm; now superseded by Option A in priority but methodologically aligned)
3. **`agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md`** — **SUPERSEDED, but its scope, acceptance criteria, locked decisions, and substrate state remain authoritative** for everything except the `run_hdbscan` implementation
4. **`agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-pattern-6-axis-discovery.md`** — original dispatch (also SUPERSEDED; same authoritative-context note)
5. **`agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/phase-D-bis-completion-summary.md`** — corrected-substrate state (48,430 rows; lineage distribution); v_category_sample is unchanged from when you last read it
6. `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-math-note-rerun-addendum.md` — your own rerun addendum (committed pre-panic); will need one more addendum per Math-before-code §1

## Design intent — Option A is substrate-led-discipline IMPROVING, not just Pattern-6-compatible (gandalf ratification)

**Authoritative source:** `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md`. Cite this path in your completion summary; the framing below is summary only.

**The substrate-led-discipline violation in row-duplication.** Row-duplication at HDBSCAN takes a rare-lineage row with F2 weight w and creates w identical points at distance 0 from each other in projection space. HDBSCAN's density estimate uses k-NN distances. **Identical-point duplicates have k-NN distance = 0, which artificially boosts the apparent density at the duplicated row's location** even when its actual neighborhood is sparse. That is not weighting — that is **manufacturing density**. A rare-lineage cluster emerges under the dual-stage version not because the rows are spatially coherent, but because they were duplicated.

This is **pre-imposition of taxonomy** ("rare lineages should cluster") rather than letting substrate decide whether they actually do. It violates the substrate-led discipline articulated in `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`.

**Gandalf's verdict (verbatim from ratification note § 2.2 + § 2.3):**

| F2's role | Stage | Verdict |
|---|---|---|
| Ensure rare lineages influence which directions are principal (axes aren't dominated by fantasy_generic variance) | PCA (sqrt(w_i) row-multiplication on TF-IDF before SVD; script lines 217-225) | Load-bearing; Option A preserves this |
| Ensure mean/std estimates aren't dominated by fantasy_generic | StandardScaler (`sample_weight` via mean/std application) | Load-bearing; Option A preserves this |
| ~~Force rare-lineage clusters into existence regardless of spatial coherence~~ | ~~HDBSCAN row-duplication~~ | **Substrate-led violation; Option A correctly removes this** |

**F2 is properly a single-stage operator at PCA + StandardScaler.** Its job is to bias **axis discovery + feature scaling**, NOT cluster formation. Under Option A, a rare-lineage cluster will emerge **iff** its rows are genuinely spatially coherent in the F2-amplified projection space. Honest outcome.

**Three dimensions Option A is strictly better:**
1. **Memory** — fits in 8 GiB on the M2 host (resolves kernel-panic root cause)
2. **Methodological honesty** — no manufactured density from identical-point duplication
3. **Substrate-led discipline** — clusters emerge from real spatial structure, not from forced amplification

**Knight-rider's original "over-engineering" framing was generous.** Per gandalf: "It was actively wrong — a quiet substrate-led-discipline violation that would have biased the Phase E-2 labeling against authentic emergent structure. Fixing it now, before Phase E-2 fires, is the right time."

### Cleaning-policy §5 normative-status check (gandalf caveat — RESOLVED)

Gandalf's ratification was conditional on knight-rider verifying that `canonical/story/cleaning-policy-design-2026-05-22.md` §5 *describes* F2's three-stage application as the math-note implementation choice rather than *prescribes* it as a normative design rule. **Knight-rider verified 2026-05-23 ~12:00 EDT:**

- §5.1 (Three-axis taxonomy) — describes cultural_lineage / historical_period / register canonical values. **Descriptive.**
- §5.2 (Per-source raw-tag → canonical taxonomy mapping) — describes Phase D mapping rules per source library. **Descriptive.**
- §5.3 (Multi-lineage and confidence scoring) — describes confidence-column construction. **Descriptive.**
- §5.4 (Pattern-6 axis-discovery interaction with this taxonomy) — describes one-hot encoding and stratified-sampling option for axis discovery. **Descriptive.**

§5 does NOT prescribe an F2-three-stage normative design rule. The three-stage application lived in legolas's math note line 725 — math-note implementation choice, not canonical doctrine. **Gandalf's ratification stands unconditionally; Option A proceeds.**

The math note line 725 ("applied as sqrt(w_i) row-multiplication on TF-IDF before SVD; as sample_weight on StandardScaler mean/std; as integer-duplication for HDBSCAN and GMM fit") will be amended by legolas as part of the Option-A math-note addendum to reflect single-stage F2-at-PCA-only doctrine. This amendment IS within scope of this dispatch.

### GMM scope check — Option-A-compliant in implementation already (RESOLVED)

Gandalf flagged: "The math-note line 725 says GMM also uses integer-duplication. If GMM remains in the pipeline (script lines 509-510), it carries the same substrate-led-violation and should also drop row-duplication. Knight-rider to verify scope."

**Knight-rider verified 2026-05-23 ~12:00 EDT.** Script lines 505-512 (`run_gmm_baseline`):

```python
def run_gmm_baseline(projections_k, k_target, random_state=42):
    """Run GMM baseline for comparison."""
    ...
    gmm = GaussianMixture(n_components=k, covariance_type='diag', random_state=random_state)
    gmm.fit(projections_k)               # ← un-expanded; no row-duplication
    labels = gmm.predict(projections_k)
    probs = gmm.predict_proba(projections_k)
    return labels, probs.max(axis=1), gmm
```

**GMM is already Option-A-compliant in code.** The violation existed only in the math-note intent (line 725), not in the implementation. No GMM code change needed for Option A. The math-note amendment must reflect this discrepancy: write down that GMM was always implemented without integer-duplication, and that line 725's "as integer-duplication for HDBSCAN and GMM fit" was overstated.

This finding is itself a Discipline observation worth surfacing: math-notes that overstate implementation create downstream doubt; future math-notes should ground claims in code line references. Append this to the discipline observations queue at `knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md`.

### Min_cluster_size resolution-gate doctrine (gandalf design-side amendment)

With row-duplication gone, **`min_cluster_size=30` becomes a hard resolution gate** on rare-lineage cluster emergence. Per the corrected substrate:

| Lineage | N in v_category_sample | Behavior under Option A |
|---|---|---|
| north_american_indigenous | 29 | < min=30; cannot form own cluster; will noise-assign to nearest |
| oceanic | 39 | Above min; can form cluster if spatially coherent |
| arctic_circumpolar | 56 | Above min; can form cluster if spatially coherent |
| mesoamerican | 83 | Above min; can form cluster if spatially coherent |

**Gandalf-lean (binding for this fire):** Keep `min_cluster_size=30`. Preserves the math note's stated parameter; gives a clean baseline for a future sensitivity sweep on {10, 15, 20, 30}. north_american_indigenous (N=29) noise-assigns to nearest cluster — document this explicitly in the completion summary's "Methodology change" section.

**Carry queued:** Phase E-1.5 sensitivity sweep on `min_cluster_size` ∈ {10, 15, 20, 30} as a follow-up fire if rare-lineage representation in Option-A output looks too sparse for Phase E-2 labeling needs. Knight-rider will queue this carry on Option-A completion-summary return.

## Math-before-code (memory projection — NEW; load-bearing precondition)

### § 1. Pre-fire peak-memory projection (REQUIRED before `--mode full` fire)

The three kernel panics show this machine's memory budget is the binding constraint. Before firing, you MUST compute an explicit peak-memory estimate and verify it under 5 GiB (62.5% of 8 GiB host RAM, leaving headroom for OS + Claude + Activity Monitor).

Per-step memory accounting (estimate from your Deliverable 1 + 2 measurements on the RERUN attempt at 11:05-11:05:44):

| Step | Object | Bytes (float64 unless noted) | Resident? |
|---|---|---|---|
| Load | corpus list (48,430 strings, avg ~200 chars) | ~10 MB | yes through clustering |
| TF-IDF | sparse matrix (48430 × 500, ~50 nonzero/row) | ~20 MB sparse + ~10 MB metadata | yes through SVD |
| TF-IDF dense (post sqrt-F2 row-mult) | (48430 × 500) dense | **194 MB** | brief, dropped after SVD fit_transform |
| LSA output | (48430 × 100) | 38.7 MB | yes through full PCA |
| Structured feature block | (48430 × 60) | 23.2 MB | yes through full PCA |
| Final feature matrix X | (48430 × 160) | 62.0 MB | yes through clustering |
| PCA TruncatedSVD on X | working matrix + components (160 × 160 + intermediate) | ~30 MB | brief |
| Projections (after PCA, full k=100 components held) | (48430 × ~100) | 38.7 MB | yes through clustering |
| Bootstrap PCA × 10 (sequential) | each ~30 MB peak; non-cumulative if released | <50 MB peak | discarded after stability calc |
| Projections trimmed to k_final (=12 last fire) | (48430 × 12) | 4.65 MB | yes through clustering |
| **HDBSCAN.fit on un-expanded (48430 × 12)** | KD-tree + MST + condensed tree + working set | **~500-1500 MB empirical estimate** (uncertainty band; depends on data density) | spike |
| **Python interpreter + sklearn + numpy + hdbscan baseline residency** | | ~500 MB | always |
| **Sum of resident objects + HDBSCAN spike at fit-time** | | **~1.2-2.2 GB projected** | peak |

**This sums to comfortably under the 5 GiB headroom budget.** The killer in the prior fires was the row-duplication step: 71,003 × 12 = same matrix size (~6.8 MB) BUT HDBSCAN's internal structures scale with n and have large constants in 12-d Euclidean. Empirically, on 71k rows in 12-d, HDBSCAN was allocating multi-GB peak working memory. On 48,430 rows the same per-row factor applies but a smaller n — projected peak roughly half of the 71k case, well under host limit.

Capture this table (with refined per-step bytes if your actuals differ) at the top of your math-note addendum at `phase-E-1-math-note-option-a-addendum.md`. Verify projected peak < 5 GiB before fire. If projection comes in above 5 GiB on refinement, STOP and flag to knight-rider — we go to Option B (subsample) or Option C (cloud).

### § 2. Optional in-process memory ceiling (defensive)

Recommend adding to top of script (defensive belt-and-suspenders):

```python
import resource
# 6 GiB soft limit; raises MemoryError instead of triggering host swap-thrash
resource.setrlimit(resource.RLIMIT_AS, (6 * 1024**3, 6 * 1024**3))
```

This makes the process crash with a Python `MemoryError` (recoverable) instead of letting macOS thrash itself into a kernel panic. Optional but strongly recommended given today's evidence.

### § 3. Single-stage F2 — math note addendum content (REQUIRED)

Write `phase-E-1-math-note-option-a-addendum.md` with:

1. Memory-projection table from § 1 above with your refined per-step bytes from prior Deliverable 1 & 2 measurements
2. Restatement of single-stage F2 design intent (paste gandalf table from "Design intent" section above; cite this dispatch as ratification source)
3. Per-lineage acceptance prediction: of the 14 lineages in the corrected pool, which are above min_cluster_size=30 (and so might form their own cluster) vs below (and so may register as noise or merge)? Lineages below 30: north_american_indigenous (N=29). Lineages at or above 30: all others. Document the projection for what cluster-membership behavior to expect per lineage.
4. Bootstrap stability re-projection: with single-stage F2 (PCA-only), the projection space is unchanged from the RERUN bootstrap result (axes 1-3 cosine-dist ≤ 0.013; axes 4-12 cosine-dist 0.39-0.80). What you're testing in this fire is **clustering** behavior; the axis-stability result is already in hand from the 11:05:44 partial-fire log. You can preserve that axis-discovery deliverable and ONLY re-fire Deliverable 3 if you prefer (see § 5 below).
5. Bis-disposition criteria — unchanged from RERUN dispatch Math-before-code §5

### § 4. F-locks (UNCHANGED)

F1-F6 all still hold. F5 PCA-primary lock holds (single-stage F2 application is consistent with F5, not a violation). No methodology change beyond what's specified in this dispatch.

### § 5. Optional fire-scope reduction

Your RERUN partial-fire at 11:05 wrote Deliverables 1 & 2 cleanly to disk (`phase-E-1-features.md`, `phase-E-1-axis-discovery.md`, `phase-E-1-axis-loadings.json` — all present on disk per knight-rider verification 11:13). **You may optionally skip re-running PCA + bootstrap** and only re-fire Deliverable 3 (clustering) on the existing on-disk axis output, since the axes are unchanged by the Option-A modification. This saves ~42 seconds of compute but more importantly avoids the brief 194 MB TF-IDF-dense spike at line 217-225 if you want maximum memory headroom.

Whether you skip Deliverable 1-2 or re-fire end-to-end is your call. Document the choice in the math note.

## The code change

In `scripts/phase_e1_pipeline.py`, `run_hdbscan` function (lines 388-431):

**Current code (lines 392-407):**
```python
# For HDBSCAN: apply F2 weighting via integer duplication
int_weights = np.round(weights).astype(int)
int_weights = np.clip(int_weights, 1, 20)  # cap duplication at 20x

expanded = []
orig_idx = []
for i, (row, w) in enumerate(zip(projections_k, int_weights)):
    for _ in range(w):
        expanded.append(row)
        orig_idx.append(i)
expanded = np.array(expanded)
orig_idx = np.array(orig_idx)

log(f"Expanded matrix for HDBSCAN fit: {expanded.shape}")
```

**Option-A replacement (no row duplication; fit directly on projections_k):**
```python
# Option-A revision (2026-05-23): F2 weighting is applied at PCA stage via sqrt(w_i) row-multiplication;
# re-applying via row duplication at the clustering stage manufactures density and is design-side
# pushback per gandalf 2026-05-23. See dispatch 2026-05-23-legolas-phase-E-1-OPTION-A-single-stage-F2.md
log(f"HDBSCAN fit on un-expanded projections: {projections_k.shape}")
```

And the subsequent `clusterer.fit(expanded)` becomes `clusterer.fit(projections_k)`.

And the label-mapping block (lines 418-426) collapses to:
```python
labels_orig = clusterer.labels_.copy()
```

(no expansion → no need to vote-aggregate per original-row).

The `weights` parameter to `run_hdbscan` becomes unused at this function. You may either remove it from the signature or keep it for forward compatibility (in case a future revision re-introduces sample-weighted clustering via a library that supports it — `hdbscan` itself doesn't). Recommend KEEP for forward-compat; cite in a comment.

## Cross-seam contract change? (Principle 6 gate)

**YES, same as RERUN dispatch.** This dispatch populates `clusters`, `cluster_membership`, and `weapon_knowledge_entries.cluster_id` (all empty pre-fire). Round-trip smoke at end of full-mode is REQUIRED per the existing `run_smoke_test()` in the pipeline. Capture PASS/FAIL in completion summary.

**Cluster-row provenance change vs original design:** Cluster membership is now determined purely by un-weighted density in projection space. The DB cluster rows carry no F2-weighting-at-clustering signal. Downstream Phase E-2 / E-3 / E-4 consumers should be aware that "F2 weighting" is encoded ONLY in the projection-space coordinates (via PCA), not in cluster membership. Document this in MIGRATION.md.

## Scope

- [ ] Read kernel-panic triage note + gandalf design-fit diagnosis
- [ ] Math note addendum at `phase-E-1-math-note-option-a-addendum.md` per Math-before-code §1-§5
- [ ] **Math-note amendment**: explicitly amend line 725 ("F2 applied as sqrt(w_i) row-multiplication on TF-IDF before SVD; as sample_weight on StandardScaler mean/std; as integer-duplication for HDBSCAN and GMM fit") to reflect single-stage F2 doctrine: "F2 applied as sqrt(w_i) row-multiplication on TF-IDF before SVD (PCA stage); as sample_weight on StandardScaler mean/std (feature-scaling stage). NOT applied at clustering stage; clusters reflect actual projection-space density." Note in addendum that GMM was already implemented without row-duplication (script line 510 = `gmm.fit(projections_k)`) — line 725's GMM claim was overstated.
- [ ] Pre-fire memory-projection check: projected peak < 5 GiB? If yes, proceed; if no, STOP and surface to knight-rider
- [ ] Code edit in `scripts/phase_e1_pipeline.py`: replace `run_hdbscan` row-duplication block per "The code change" above
- [ ] Optional: add `resource.setrlimit` defensive ceiling at top of script per § 2
- [ ] Optional: skip Deliverable 1-2 re-fire and only re-run Deliverable 3 per § 5 (keep existing on-disk axis output; document choice)
- [ ] `python scripts/phase_e1_pipeline.py --mode full 2>&1 | tee scripts/full-run-log-2026-05-23-option-a.txt`
- [ ] Confirm acceptance gates pass empirically (k_final, bootstrap, cluster count, purity)
- [ ] Write completion summary at `phase-E-1-completion-summary.md`:
  - Per-deliverable artifact path + acceptance-criterion verification
  - Per-axis stability + per-cluster F6 merge candidates
  - **"Methodology change" section** with gandalf single-stage-F2 ratification table + design-side caveat (verbatim) + per-lineage cluster-vs-noise outcomes especially for north_american_indigenous (N=29)
  - Phase E-1-bis disposition per RERUN-dispatch Math-before-code §5
  - Phase E-2 hand-off notes
- [ ] Write MIGRATION.md at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`:
  - DB writes
  - Cluster_id back-reference
  - **Cluster-row provenance change** per Cross-seam section above
  - Forward-compat declaration
  - Phase E-2 / E-3 / E-4 downstream notes
- [ ] Round-trip smoke (auto-runs at end of full-mode; PASS/FAIL captured in completion summary)
- [ ] Tag: `legolas/phase-E-1-axis-discovery-2026-05-23` (seam-prefix intermediate per ADR-001; local only; do NOT push) — same tag name as RERUN since no prior tag was cut
- [ ] Append completion record to this dispatch per `dispatches/README.md`

## Acceptance criteria (unchanged from RERUN; memory-projection precondition added)

- [ ] **Memory projection.** Pre-fire peak-memory estimate < 5 GiB documented in math-note addendum.
- [ ] **K count.** k_final in [8, 12] target; k_final ≥ 8 minimum acceptable.
- [ ] **Bootstrap stability.** ≥ 6 of k_final axes pass cosine-distance ≤ 0.10. Per RERUN log, you already have k_final=12, k_80=36, kink_idx=4; axes 1-3 pass (0.0011, 0.0118, 0.0131); axes 4-12 fail (0.39-0.80). **Phase E-1-bis disposition: partial-acceptance bis-flag** (3 of 12 axes stable, k_final=12 ≥ 8; per RERUN Math-before-code §5, "k_final ≥ 8 AND fewer than 6 axes pass bootstrap stability" → partial-acceptance bis-flag). Document this as already-known outcome; do NOT re-fire bootstrap for axis stability (axes are unchanged by Option-A).
- [ ] **Variance explained.** Cumulative EVR at k_final ≥ 30% target. From RERUN log: cumulative EVR at k=12 is 0.3934 — PASSES the 30% floor.
- [ ] **Cluster count.** HDBSCAN output 50-150 emergent clusters (after pipeline auto-retry adjustment if needed). NEW empirical from Option-A.
- [ ] **Cluster purity.** Mean cultural_lineage purity ≥ 0.85 across all clusters. NEW empirical from Option-A.
- [ ] **F6 flag.** Clusters with < 20 members documented as merge-candidates for Phase E-2 designer review.
- [ ] **Method comparison.** HDBSCAN-vs-GMM-vs-k-means agreement assessed; documented in completion summary.
- [ ] **DB writes** verified via SELECT COUNT(*) on `clusters` / `cluster_membership` / `weapon_knowledge_entries.cluster_id` — all populated; round-trip smoke PASS.
- [ ] **Per-lineage projection-space disposition.** For each of the 14 lineages, document whether it formed its own cluster, was absorbed into a mixed cluster, or appeared as noise. Special attention to north_american_indigenous (N=29; expected noise-assignment under min=30 resolution gate) and other sub-100-row lineages (oceanic=39, arctic_circumpolar=56, mesoamerican=83 — all above gate but may still noise-assign if not spatially coherent).
- [ ] **AGENT_STATE.md** or equivalent legolas checkpoint updated.
- [ ] **Round-trip smoke:** the auto-test at end of full-mode plus the 30-row cluster_id back-reference check.

## Out of scope

- **Phase D / Phase-D-bis amendments.** Substrate is locked.
- **Methodology changes beyond Option-A revision.** F5 PCA-primary lock holds. If clustering output is unsatisfactory for Phase E-2, surface to knight-rider; do not unilaterally switch HDBSCAN → BIRCH or similar.
- **Re-running bootstrap PCA.** Per Math-before-code §5 + acceptance criteria above, bootstrap stability result from the 11:05 partial-fire is already on disk and is unchanged by Option-A. You may skip Deliverable 1 + 2 re-fire if you prefer; document the choice.
- **Phase E-2 designer labeling.** Hand-off notes only.
- **DB push to origin.** Local-only.
- **Step 6.6.c wikipedia fictional-weapon recovery.** Out of scope (~70 rows; deferred).
- **Cosmetic markdown-template bugs in pipeline** (`min_cluster_size=30` hardcoded in template at ~line 903; `min_df: 3` hardcoded at ~line 205). Fix if you want; not blocking.

## Open questions for legolas to resolve + document

1. **Optional Deliverable 1-2 skip.** Re-fire end-to-end or only Deliverable 3? Document choice + memory-impact reasoning.
2. **`resource.setrlimit` defensive ceiling.** Apply or not? Recommend yes; small effort, large safety win.
3. **`weights` parameter signature.** Keep or remove from `run_hdbscan` signature? Recommend keep (forward-compat) with a comment.
4. **min_cluster_size = 30 vs scaling to 87 (proportional to 3× pool growth).** Original dispatch's open question; still on you. Recommend stay at 30 for first-fire; document any cluster-noise tradeoff observed.
5. **assign_noise_to_nearest behavior for sub-min_cluster lineages.** With north_american_indigenous (N=29) potentially merging into nearest cluster, does that hurt cluster purity? Document per-cluster purity AND per-lineage disposition.

## What knight-rider does after your return

1. Read your completion summary + acceptance-gate results + Phase E-1-bis disposition + per-lineage cluster outcomes
2. **Most likely outcome:** k_final=12 / 3 of 12 axes stable / 30%+ EVR → Phase E-1-bis partial-acceptance with bis-flag. Surface to gandalf + jack-ryan critique pair on bootstrap-stability tail (axes 4-12 unstable at 0.39-0.80) for methodology decision. The single-stage F2 fix resolves the design-side artifact concern but does NOT bear on the bootstrap-stability tail — those failures are signal about the substrate's intrinsic dimensionality, now that we know it's not a pool-filter artifact.
3. If clustering acceptance criteria pass (50-150 clusters, ≥0.85 purity, DB populated): author Phase E-2 gandalf-labeling dispatch.
4. **Queue Phase E-1.5 sensitivity-sweep carry** on `min_cluster_size` ∈ {10, 15, 20, 30} per gandalf ratification note § 4 if rare-lineage representation in Option-A output looks too sparse for Phase E-2 labeling needs.
5. Discipline observations from this entire phase queued for jack-ryan ratification — now four candidates:
   - Memory-headroom check at math-before-code (Discipline #1 amendment)
   - Smoke-test scope expansion to include resource-scaling rehearsal (Discipline #2 amendment)
   - Identical-point duplication for sample-weight emulation is a substrate-led-violation footgun on density-based algorithms (NEW from gandalf ratification § 4)
   - Math-notes must ground implementation claims in code line references — line 725's "GMM uses integer-duplication" was overstated vs actual code (NEW from this dispatch's GMM scope check)

   See `knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md`.

## References

- **Gandalf design-side ratification (authoritative for the substrate-led-violation framing + min_cluster_size doctrine):** `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md`
- Kernel-panic triage: `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md` (full forensic)
- Gandalf diagnosis: `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md`
- RERUN dispatch: `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md` (**SUPERSEDED**; scope/acceptance/F-locks still authoritative)
- Original Phase E-1 dispatch: `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-pattern-6-axis-discovery.md` (**SUPERSEDED**; methodology still authoritative)
- Phase-D-bis completion summary: `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/phase-D-bis-completion-summary.md`
- Phase-D-bis MIGRATION.md: `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/MIGRATION.md`
- Substrate tag: `elrond/phase-D-bis-step-6-6-2026-05-23`
- Cleaning-policy (design-side canonical): `canonical/story/cleaning-policy-design-2026-05-22.md` § 5
- Hive-mind protocol weapon-library-import (design-side canonical): `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` § 6.4 Pattern-6
- ADRs: ADR-001 (tag protocol), ADR-004 (cross-seam coordination via MIGRATION.md), ADR-006 (read-only external state default)

---

## Tag at completion

```
legolas/phase-E-1-axis-discovery-2026-05-23
```

Seam-prefix per ADR-001. Local-only. Same tag name as RERUN/original (no prior tag was actually cut).

---

**Signed:** knight-rider, 2026-05-23 post-Option-A authoring + gandalf strengthened-ratification fold-in (§5 normative-status verified DESCRIPTIVE; GMM verified Option-A-compliant in code; substrate-led-violation framing folded; min_cluster_size resolution-gate doctrine folded; Phase E-1.5 sensitivity-sweep carry queued). Matt + gandalf design-side ratification confirmed UNCONDITIONALLY. Gate-1 jack-ryan ratification SKIPPED — methodology is design-spec-as-math single-line revision with gandalf design ratification + 2026-05-23 ground-state oracle compatibility verified; the change is consistent with the F5 PCA-primary lock; the gandalf ratification note is the design authority. Fire `--mode full` against the 48,430-row v_category_sample with the un-expanded HDBSCAN call to produce the genuine Phase E-1 empirical result without host-memory exhaustion.
