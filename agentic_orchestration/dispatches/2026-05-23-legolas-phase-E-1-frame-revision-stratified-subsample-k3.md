# Dispatch — 2026-05-23 — legolas — Phase E-1 Frame Revision (stratified subsample, k=3, substrate-voted)

**From:** knight-rider
**To:** legolas (Mode A analytical research; Pattern-6 canonical axis discovery + clustering — frame-revision resize)
**Approved by:** Matt + gandalf joint 2026-05-23 ~12:00 EDT; full reasoning in `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`
**Estimated effort:** ~30-45 minutes for code addition + math-note addendum + fire + completion summary; total ~1-1.5 hours
**Acceptance gating:** **≥50 clusters AND mean per-lineage purity ≥ 0.70** across the substrate → Phase E-2 proceeds. **<50 clusters OR purity < 0.70** → Alternative 2 (substrate expansion) is next; NOT cloud-bigger-HDBSCAN. Full operationalization (including partial-acceptance and pathological branches) in § B.6. "Meaningful clusters" is shorthand for the conjunction; the conjunction is binding.

---

## Why this dispatch exists

The OPTION-A dispatch was empirically refuted on two fronts at 11:40-11:43 EDT:

1. **Substrate dimensionality:** bootstrap stability 3 of 12 axes pass (axes 1-3 at 0.0011-0.0131; axes 4-12 at 0.39-0.80). The substrate voted k=3, not k=12.
2. **Memory budget:** HDBSCAN.fit on un-expanded (48,430 × 12) kernel-panicked the M2/8GiB host (4th panic at 11:43:45 EDT). Even without row-duplication, 48K × 12 exceeds the memory budget at clustering.

The frame-revision resize (Matt + gandalf 2026-05-23 ~12:00 EDT) reframes the experiment:

- **Use the 3 substrate-stable axes** (1-3) for clustering, not the 12-axis tail.
- **Stratified subsample (~10K rows with rare-lineage floors)** for HDBSCAN, not full 48K. Subsample fits trivially in memory.
- **Assign-noise-to-nearest for the remaining 38K** to produce full-pool coverage on the cluster_membership table.
- **No cloud fire.** Cloud only becomes warranted if Alternative 2 (substrate expansion) is exhausted AND production-grade full-pool validation is needed.

Frame-revision rationale is in `knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md` — read this before starting.

## Required reading before starting

1. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`** — full reframe + Matt's acceptance tree + gandalf's owned-up Option-A ratification-discipline failure (§ 3) + Discipline #18 amendment candidate (§ 4)
2. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-math-note-option-a-addendum.md`** (your own; §4 bootstrap stability table is now authoritative for the 3 stable axes)
3. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-discovery.md`** + **`phase-E-1-axis-loadings.json`** — on-disk D2 output from 11:40 EDT fire (axes 1-12 with loadings + stability). You will load this and project onto axes 1-3 only.
4. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md`** — full forensic of panics 1-3 (forensic note on panic 4 forthcoming via gandalf addendum)
5. **`agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md`** — single-stage-F2 doctrine still authoritative for axis discovery; resize narrows the scope further, does not contradict it
6. **`agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-OPTION-A-single-stage-F2.md`** — SUPERSEDED but its acceptance vocabulary (cluster purity, F6 flag, DB round-trip smoke) is still authoritative

## Locked decisions (carried from prior dispatches; not re-litigated)

- **F1-F4 / F5 (PCA-primary) / F6** — all hold.
- **Single-stage F2 doctrine** (gandalf ratification 2026-05-23 11:26 EDT) — F2 applied at PCA only; not at clustering. This dispatch preserves single-stage F2 trivially (clustering operates on axes-1-3 projections that already encode F2 amplification).
- **Substrate locked.** v_category_sample = 48,430 rows from elrond Phase-D-bis tag `elrond/phase-D-bis-step-6-6-2026-05-23`. Do NOT re-cut or modify the substrate in this dispatch.
- **D1 (TF-IDF + LSA + structured features) need not re-fire.** The current `phase-E-1-features.md` is correct under both the OPTION-A and frame-revision frames. You may EITHER re-fire D1 (clean rebuild; ~8 sec) OR skip-and-reuse (the on-disk file is authoritative). Document choice.
- **D2 axes 1-3 are authoritative.** Loadings on disk at `phase-E-1-axis-loadings.json` for axes 1-3 are the cluster basis. Do NOT re-fire bootstrap on full pool.

## What is new in this dispatch

### A. Pipeline code addition (real change, not a parameter pass)

Per knight-rider's Explore-agent audit of `scripts/phase_e1_pipeline.py`, the script does NOT support: stratified subsample, on-disk D2 axis load, D3-standalone, CLI `--k_final`, or CLI `--min_cluster_size`. **You will add these.**

**Required additions:**

1. **New mode** `--mode subsample-k3` (or rename if you prefer; document in math note). Distinct from existing `--mode smoke` and `--mode full`.

2. **On-disk D2 axes loader:** read `phase-E-1-axis-loadings.json` from the deliverables dir; reconstruct axes 1-3 components matrix from the loadings JSON. If the JSON format does not preserve raw components, regenerate axes 1-3 via a minimal PCA re-fire on the (48430 × 160) feature matrix (~8 sec; acceptable).

3. **Full-pool projection onto axes 1-3:** compute `projections_3 = X @ axes_1_to_3.T` where `X` is the full feature matrix; result shape (48430 × 3); ~1.2 MB. Cache to disk as `phase-E-1-projections-k3.npz` to support re-firing the clustering step alone in future iterations without re-computing D1+D2.

4. **Stratified subsample with rare-lineage floors:**
   - **Math-design choice you make in math-note §3 below.**
   - Recommended starting structure: per-lineage floor of `max(min_cluster_size × 2, all_available)`; remaining budget filled proportionally by population share.
   - For target N=10,000 subsample on the 14-lineage substrate, this gives roughly: oceanic/arctic/n.am.indigenous take all available (29+39+56=124 rows); other 11 lineages each get max(floor, proportional). Exact composition decided in math note.
   - Use NumPy with `random_state=42` for reproducibility.

5. **CLI overrides:**
   - `--k_final` (default: heuristic; override allowed; required for this dispatch with value 3)
   - `--min_cluster_size` (default: 30; required override for subsample fire — likely 10 or 15; you choose in math note)
   - `--subsample_n` (default: 10000; can override for sensitivity)

6. **HDBSCAN at subsample scale:** `clusterer.fit(subsample_projections_3)`. Memory budget: negligible (~5-10 MB peak).

7. **assign-noise-to-nearest for remaining 38K:** the existing `run_assign_noise_to_nearest` (if present) operates on noise points within the clustered set; for this dispatch it must additionally assign the 38K **non-subsampled** rows to their nearest cluster centroid (or sample-leader) in the (48430 × 3) projection space. This produces full-pool cluster_membership for the DB write.

8. **DB writes** as in prior dispatches; round-trip smoke test on `clusters` / `cluster_membership` / `weapon_knowledge_entries.cluster_id` after fire.

9. **Cosmetic markdown-template fixes (low priority):** the `min_cluster_size=30` and `min_df=3` hardcoded values in `write_deliverable_3` / `write_deliverable_1` should reflect actual runtime values. Fix if you want.

### B. Math-before-code requirements (REQUIRED — write to `phase-E-1-math-note-frame-revision-addendum.md`)

#### § 1. Pre-fire peak-memory projection

Target: < 1 GiB peak (well within budget). Show that nowhere in this pipeline does any working object exceed 100 MB. Trivial; document anyway per Discipline #1.

| Step | Object | Size estimate |
|---|---|---|
| Load D1 features (re-fire or skip-and-reuse from on-disk) | (48430 × 160) dense | 62 MB |
| Load D2 axes 1-3 (or regen via mini PCA) | (160 × 3) components | <1 MB |
| projections_3 = X @ axes.T | (48430 × 3) | 1.2 MB |
| Stratified subsample mask + extract | (N≈10000 × 3) | ~240 KB |
| HDBSCAN.fit on (10000 × 3) | KD-tree + MST + condensed-tree | empirically ~5-50 MB peak |
| Nearest-cluster assign for remaining 38K | distance to ~50-150 centroids | trivial |
| Python baseline residency | | ~500 MB |
| **Estimated peak** | | **~600-700 MB** — well under 5 GiB ceiling |

The `resource.setrlimit` defensive ceiling that failed at 11:39 should NOT be retried — it's a no-op on this macOS configuration. Replace with an in-script `psutil`-based peak-memory check that raises if RSS exceeds 6 GiB (defensive belt for unexpected scenarios). Optional but recommended.

#### § 2. Substrate-voting-is-binding application

Document explicitly:
- Bootstrap stability 11:40 EDT fire showed k_stable=3 from k_chosen=12.
- Per Discipline #18 amendment candidate (frame-revision note §4), this is a methodology gate, not a flag.
- This dispatch operationalizes the gate by setting `--k_final 3`.
- Cite gandalf's owned-up ratification-discipline failure (frame-revision note §3) as the precedent for why this gate is now binding rather than advisory.

#### § 3. Stratified subsample composition design

**Resolved-before-coding requirement (jack-ryan Gate-1 Finding 1 fold-in):** This section must be **fully resolved in the math-note addendum BEFORE writing pipeline code.** The open questions below are math-design questions, not implementation questions. Discipline #1 (math-before-code) requires resolution at the math stage; the dispatch's acceptance criteria depend on the resolved composition (e.g., "all 14 lineages have at least `min_cluster_size` representation" cannot be verified without the floor choice committed).

**Required outputs in math note § 3:**

1. **Floor formula committed.** Pick: `max(min_cluster_size × 2, available)` OR `max(min_cluster_size, available)` OR another formula. Defaults to 2× per recommendation below but the choice MUST be stated as a committed decision, not a "document choice" open hook.
2. **N_target committed.** Default 10,000; override allowed with documented reasoning.
3. **Per-lineage count table** showing exact subsample count per lineage given the committed floor + N_target + corrected-pool distribution. Sum must equal N_target.
4. **All 14 lineages above `min_cluster_size`** in the resulting subsample — verify in the table.
5. **random_state=42** reproducibility commitment.

Recommended starting structure (legolas may override with reasoning):
- Floor f = max(`min_cluster_size` × 2, available) per lineage
- Remaining budget = 10000 - sum(floors); allocate proportional to share among lineages above the floor
- Rare lineages (oceanic, arctic_circumpolar, n.am.indigenous) take all available

Recommendation rationale: 2× floor (clearer-than-noise) over 1× floor (just-over-threshold) because density-based clustering needs density margin above the resolution gate to produce a stable cluster boundary. 1× floor is plausible but marginal-risk if the subsample's coordinate distribution happens to noise-cluster the rare lineage.

**Committed choice required in math note before code starts.** If legolas wants to explore alternatives, document them in math note § 3, choose one, and proceed. No deferral to runtime.

#### § 4. min_cluster_size choice for ~10K subsample

Default of 30 was calibrated for N=48K. For N≈10K (5× smaller), proportional scaling gives min_cluster_size=6. Conservative-density-leaning choice: 10. Aggressive-density-leaning: 15. Pick one with reasoning; document the choice.

The gandalf-approved Phase E-1.5 sensitivity sweep candidate is {10, 15, 20, 30}. This dispatch fires at ONE choice; the sensitivity sweep can fire as Phase E-1.5 if Alternative 1 succeeds and Phase E-2 wants robustness validation.

#### § 5. Bootstrap stability at k=3 on subsample (optional but valuable)

The full-pool bootstrap showed axes 1-3 at 0.0011-0.0131 cosine-distance — far below the 0.10 threshold. On a stratified-subsample of N=10K, this should remain stable BUT the cheapest sanity check is to re-fire a 5-bootstrap-resample on the subsample axes 1-3. If they remain < 0.10, the k=3 frame is empirically reinforced. If they don't, surface to knight-rider before clustering.

This step is OPTIONAL because the full-pool bootstrap result is already in hand. Skip if your math-before-code shows it's unnecessary; include if you want belt-and-suspenders.

#### § 6. Bis-disposition criteria (frame-revision specific)

| Condition | Disposition |
|---|---|
| ≥50 clusters formed AND mean per-lineage purity ≥ 0.70 (lowered from 0.85 because subsample density is lower) | **Acceptance.** Phase E-2 cluster labeling proceeds. |
| 50 ≤ clusters < 100 AND purity 0.50-0.70 | **Partial acceptance.** Phase E-2 proceeds with merge-candidate review (F6 flag at < 20 members + cross-cluster lineage-mixing review). |
| < 50 clusters formed OR purity < 0.50 | **Substrate-coverage bottleneck.** Alternative 2 (substrate expansion via targeted rare-lineage crawls) is the next move. NOT cloud-bigger-HDBSCAN; cloud does not fix substrate-coverage. |
| Pathological: clusters dominated by single-lineage trivial shards (e.g., 50+ clusters but all fantasy_generic) | **Methodology re-review.** Surface to knight-rider for critique-pair (gandalf + jack-ryan) before any next fire. |

## Scope

- [ ] Read frame-revision note + this dispatch + the on-disk D2 output
- [ ] Read forthcoming gandalf addendum to kernel-panic-diagnosis (if on disk at fire time); cite if present
- [ ] Math-note addendum at `phase-E-1-math-note-frame-revision-addendum.md` per § B above (six sections)
- [ ] Pipeline code addition per § A above (new mode + CLI overrides + on-disk D2 load + stratified subsample + nearest-assign for full-pool coverage)
- [ ] `python scripts/phase_e1_pipeline.py --mode subsample-k3 --k_final 3 --min_cluster_size <your-choice> --subsample_n 10000 2>&1 | tee scripts/full-run-log-2026-05-23-frame-revision.txt`
- [ ] Confirm acceptance gates pass empirically (≥50 clusters; per-lineage purity ≥ 0.70 — see §6 disposition table)
- [ ] Write completion summary at `phase-E-1-completion-summary.md` (overwrite if exists from any prior partial run):
  - Per-deliverable artifact path + acceptance-criterion verification
  - Stratified subsample composition table (per-lineage count + floor)
  - HDBSCAN parameters used + cluster count + purity
  - Per-lineage disposition: which formed own cluster; which mixed; which assigned to nearest from outside subsample
  - **Phase E-1-bis disposition** per § B.6 above
  - Phase E-2 hand-off notes IF acceptance is met
  - Alternative 2 surface IF acceptance is not met (no decision tree wandering — flag explicitly and stop)
- [ ] Write MIGRATION.md at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`:
  - DB writes (clusters, cluster_membership, weapon_knowledge_entries.cluster_id) covering all 48,430 rows via subsample-cluster + nearest-assign
  - **Native-vs-nearest-assigned split (jack-ryan Gate-1 Finding 3 fold-in):** declare explicitly that all 48,430 cluster_ids are substrate-voted at k=3, AND partition the assignment provenance: rows in the ~10K subsample are **cluster-native** (HDBSCAN on subsample produced the cluster_id directly); remaining ~38K rows are **nearest-assigned** (cluster_id derived by nearest-centroid distance in axes-1-3 projection space). Downstream Phase E-2 / E-3 / E-4 consumers MUST NOT assume cluster_id reflects equal density-based confidence across all rows. Phase E-2 label-quality work in particular needs to know which rows had density-based assignment vs distance-based assignment. ADR-004 + Discipline #8 cited.
  - Frame-revision provenance: cluster_id assigned at k=3, not k=12; this is intentional per the substrate-voted resize (cite frame-revision note + Discipline #18 amendment candidate)
  - Forward-compat declaration for Phase E-2 / E-3 / E-4
  - Recommended: add a column or sidecar table marking row-provenance (e.g., `cluster_assignment_method` ∈ {`hdbscan_native`, `nearest_centroid`}) — if schema constraints prevent that, document the partition in MIGRATION.md text so downstream consumers can reconstruct it
- [ ] Round-trip smoke (auto-runs at end of mode; PASS/FAIL captured in completion summary)
- [ ] Tag: `legolas/phase-E-1-frame-revision-subsample-k3-2026-05-23` (seam-prefix per ADR-001; local only; do NOT push)
- [ ] Append completion record to this dispatch per `dispatches/README.md`

## Acceptance criteria

- [ ] **Memory projection.** Pre-fire peak-memory estimate < 1 GiB documented in math-note addendum.
- [ ] **k = 3.** Clustering operates on axes 1-3 only. No k=12 retry, no k_final heuristic override.
- [ ] **Stratified subsample.** ~10K rows with documented per-lineage floors; all 14 lineages have at least `min_cluster_size` representation.
- [ ] **Cluster count.** ≥ 50 emergent clusters across the substrate after subsample HDBSCAN + nearest-assign (see § B.6 disposition).
- [ ] **Cluster purity.** Mean per-lineage purity ≥ 0.70 across all clusters (relaxed from 0.85 per § B.6 rationale).
- [ ] **F6 flag.** Clusters with < 20 members documented as merge-candidates for Phase E-2 designer review.
- [ ] **Full-pool coverage.** All 48,430 rows assigned to a cluster (either via HDBSCAN on subsample or nearest-assign for remaining 38K).
- [ ] **DB writes** verified via SELECT COUNT(*) on `clusters` / `cluster_membership` / `weapon_knowledge_entries.cluster_id` — all 48,430 covered; round-trip smoke PASS.
- [ ] **Per-lineage projection-space disposition.** For each of the 14 lineages, document whether it formed its own cluster, was absorbed into a mixed cluster, or appeared as noise. Special attention to rare lineages (oceanic, arctic_circumpolar, n.am.indigenous, mesoamerican).
- [ ] **Bis-disposition** declared explicitly per § B.6.

## Out of scope (load-bearing)

- **NO full-48K HDBSCAN fire.** Past evidence (4 panics) is sufficient.
- **NO k > 3 clustering.** Bootstrap-stability gate is binding.
- **NO cloud fire.** Substrate-led discipline says: if Alternative 1 surfaces a substrate-coverage bottleneck, the move is Alternative 2 (substrate expansion), not bigger-compute.
- **NO Phase D / Phase-D-bis substrate changes.** Substrate is locked.
- **NO Phase E-2 designer labeling** (hand-off notes only).
- **NO DB push to origin.** Local-only.
- **NO Phase E-1.5 sensitivity sweep** in this fire. Queued for future Phase E-1.5 dispatch if Alternative 1 succeeds and Phase E-2 wants robustness validation.
- **NO Step 6.6.c wikipedia fictional-weapon recovery** (~70 rows; deferred).
- **NO `resource.setrlimit` retry.** Failed silently at 11:39 fire; use `psutil` RSS-check instead if you want a defensive guard.
- **NO full-pool bootstrap re-fire on D2 (jack-ryan Gate-1 Finding 5 fold-in).** § B.5 above offers an optional bootstrap-stability re-fire on the **subsample axes 1-3** as a sanity check; that is in scope. A full-pool (N=48,430) bootstrap re-fire on D2 is **out of scope** — the existing on-disk bootstrap result is authoritative and a full-pool re-fire would consume the compute budget this dispatch is explicitly avoiding.

## Open questions for legolas to resolve + document in math note

1. **Skip D1 re-fire or re-fire fresh?** Document choice.
2. **Stratified subsample floor: at `min_cluster_size` exactly or `min_cluster_size × 2`?** Recommend 2×; document choice.
3. **min_cluster_size for ~10K subsample: 10, 15, 20, or other?** Document choice + reasoning. Phase E-1.5 sweep can vary this later.
4. **Optional bootstrap-stability re-fire on subsample axes 1-3?** Skip-with-rationale OK; include-with-result OK.
5. **psutil RSS-guard at top of script?** Recommend yes; small effort.
6. **Cache `projections_k3` to disk?** Recommend yes (`phase-E-1-projections-k3.npz`) — enables future D3-only re-firing without D1+D2 recompute.

## What knight-rider does after your return

1. Read completion summary + acceptance-gate results + bis-disposition + per-lineage outcomes
2. **If acceptance is met (≥50 clusters, purity ≥0.70):**
   - Phase E-1 deliverable is real. Author Phase E-2 gandalf-labeling dispatch.
   - Queue Phase E-1.5 sensitivity-sweep carry on `min_cluster_size` as a future optional fire.
3. **If acceptance is NOT met (substrate-coverage bottleneck):**
   - Surface to gandalf + jack-ryan critique pair for Alternative 2 framing.
   - Author Alternative 2 dispatch for legolas Mode-B (substrate expansion via targeted rare-lineage crawls) — or for elrond if the gap is in cleaning rather than acquisition.
   - Cloud fire is NOT on the table at this branch.
4. **Discipline observations queue update:** add the substrate-voting-is-binding amendment to the jack-ryan queue (already done by the frame-revision note §4 reference).

## References

- **Frame-revision note (authoritative for the resize):** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`
- Gandalf design-side ratification (single-stage F2): `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md`
- Gandalf kernel-panic-diagnosis + addendum: `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` (addendum forthcoming)
- Kernel-panic triage (panics 1-3): `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md`
- OPTION-A dispatch (SUPERSEDED): `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-OPTION-A-single-stage-F2.md`
- RERUN dispatch (SUPERSEDED): `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md`
- Original Phase E-1 dispatch (SUPERSEDED): `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-pattern-6-axis-discovery.md`
- CONTINUATION dispatch (SUPERSEDED): `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-CONTINUATION-full-mode-fire.md`
- Phase-D-bis completion summary: `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/phase-D-bis-completion-summary.md`
- Substrate tag: `elrond/phase-D-bis-step-6-6-2026-05-23`
- Cleaning-policy (design-side canonical): `canonical/story/cleaning-policy-design-2026-05-22.md` § 5
- ADRs: ADR-001 (tag protocol), ADR-004 (cross-seam coordination via MIGRATION.md), ADR-006 (read-only external state default)

---

## Tag at completion

```
legolas/phase-E-1-frame-revision-subsample-k3-2026-05-23
```

Seam-prefix per ADR-001. Local-only. Distinct tag name from the SUPERSEDED dispatches' `phase-E-1-axis-discovery-2026-05-23` because the deliverable is different (subsample k=3, not full-pool k=12).

---

**Signed:** knight-rider, 2026-05-23 post-Matt+gandalf frame-revision resize ~12:00 EDT. Gate-1 jack-ryan ratification of this dispatch is run by knight-rider after authoring (Pattern-A-light, DESIGN-MODE); findings will be folded as edits before legolas fires. Matt + gandalf design-side approval already in hand for the resize itself.
