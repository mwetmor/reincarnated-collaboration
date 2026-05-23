# Phase E-1 Frame-Revision Note — 2026-05-23

**Author:** knight-rider
**For:** legolas (next-fire dispatch); gandalf (design-side anchor); jack-ryan (Discipline #18 amendment); future cycle reviewers
**Trigger:** Matt + gandalf joint resize at ~12:00 EDT 2026-05-23 following the 4th kernel panic of the day at 11:43:45 EDT
**Status:** Live methodology anchor. Supersedes the OPTION-A dispatch's experiment frame. Does NOT supersede F1–F4 / F6 locks.

---

## 1. Why this note exists

The Phase E-1 fires this cycle (smoke + RERUN + OPTION-A) have empirically refuted **two** premises of the original Phase E-1 dispatch experiment frame:

| Premise | Refuted by | Evidence |
|---|---|---|
| The substrate supports clustering at k=12 across all 14 cultural-lineage buckets | OPTION-A D2 output 11:40:15 EDT | Bootstrap stability: 3 of 12 axes pass cosine-dist ≤ 0.10 (axes 1-3: 0.0011, 0.0118, 0.0131); axes 4-12 all in 0.39-0.80 range |
| HDBSCAN.fit on un-expanded (48,430 × 12) fits in 8 GiB on M2 host | 4th kernel panic 11:43:45 EDT | watchdogd starvation 90+s; 100% compressor saturation; 4th panic of the day with identical signature |

The bootstrap-stability finding at 11:40:15 was the substrate **voting** on dimensionality — it voted k=3, not k=12. The OPTION-A dispatch proceeded past that vote and fired anyway, treating it as a flag rather than a methodology gate. The host then kernel-panicked at the clustering stage. Two separate failure modes, one converging diagnosis: **we were running the wrong experiment.**

## 2. The resize (Matt + gandalf joint verdict 2026-05-23 ~12:00 EDT)

**New experiment frame:**

- **Dimensionality:** k=3 (substrate-voted), not k=12 (heuristic-chosen). Cluster on axes 1-3 from the on-disk D2 output. Axes 4-12 are not retained for clustering.
- **Pool scale:** Stratified subsample ~10K (with rare-lineage floors), not full 48,430. The full-pool fire is not load-bearing for the experiment — it was load-bearing only for the speculative k=12 clustering the substrate doesn't support.
- **Compute target:** This host (M2 / 8 GiB). Cloud fire is **cancelled** unless the subsample experiment surfaces a substrate-coverage bottleneck AND the team chooses production-validation-at-scale.
- **F2 weighting:** Preserved at axis discovery (already baked into the on-disk D2 output via sqrt-row-multiplication on TF-IDF before SVD). Not re-applied at clustering. Single-stage-F2 doctrine from OPTION-A still holds; the resize narrows the scope further.

**Acceptance tree (Matt 2026-05-23):**

1. **Alternative 1 result ≥ 50 meaningful clusters across the substrate** → real Phase E-1 deliverable; Phase E-2 cluster labeling proceeds on that output; cloud question evaporates entirely.
2. **Alternative 1 result < 50 meaningful clusters OR clusters non-meaningful (e.g., trivial single-lineage shards, no cross-lineage cohesion)** → substrate-coverage bottleneck confirmed; next move is **Alternative 2 (substrate expansion via targeted rare-lineage crawls)**, NOT cloud-bigger-HDBSCAN. Cloud doesn't fix substrate-coverage problems.
3. **Cloud fire warranted only if:** (a) the team wants production-grade clustering at full 48K scale on the stable 3 axes for validation; (b) future substrate growth pushes Alternative 1's subsample-clustering past local memory budget.

## 3. Gandalf's owned Option-A ratification-discipline failure

Per gandalf 2026-05-23 ~12:00 EDT (verbatim where possible):

> "My ratification at 11:26 EDT had access to the smoke-frame artifact result from the 03:11 run (k=4, 1-of-4 stable axes). I treated that as a sample-frame artifact and didn't escalate. The 11:05 fire's bootstrap stability (3-of-12 stable, before the kernel panic) was further empirical confirmation that the substrate isn't supporting the dimensionality the methodology was assuming. Both signals were available before I ratified Option A. I should have flagged 'the experiment frame may be wrong' then and didn't.
>
> That's a Pattern A-deep ratification discipline failure on my part. The substrate-led discipline I've been advocating for in canonical docs says: let the substrate vote on dimensionality, not the methodology's k-selection heuristic. The bootstrap-stability check IS the substrate voting. It voted k=3. I logged that vote as a flag and ratified a re-fire at k=12 anyway because compute-remediation was the visible problem."

Gandalf has committed to authoring an addendum at `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` (or a new sibling note) recording this. The frame-revision dispatch cites this note as authoritative; if the addendum is not yet on disk at dispatch-author time, that's an open carry, not a blocker.

## 4. Discipline #18 amendment candidate (gandalf-flagged; jack-ryan to absorb)

Per gandalf: bootstrap-stability results at axis discovery are a **methodology gate**, not a **flag**. If `k_stable < k_chosen` by a substantial margin (e.g., factor of 2+), the methodology must **re-cut at k_stable before clustering fires.** A logged flag with continued execution at k_chosen is a substrate-led discipline violation.

**Candidate framing for jack-ryan ratification:**

> "Discipline #18 amendment (substrate-voting-is-binding): When a substrate-driven measurement (bootstrap-stability at axis discovery, scree-kink at PCA, silhouette at clustering) produces a value substantially below the methodology's chosen parameter, the chosen parameter must be cut to the substrate-driven value before the next stage fires. Substrate measurement is a gate, not a flag. A logged flag with continued execution at the original parameter is a substrate-led discipline violation regardless of compute-remediation framing."

This candidate is added to the discipline-observations queue at `knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md` for jack-ryan to absorb in the next disciplines-doc revision pass.

## 5. Anchor for the frame-revision dispatch

The Pattern-B dispatch at `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-frame-revision-stratified-subsample-k3.md` operationalizes this note. It is the live target for legolas's next fire. Prior dispatches (original, RERUN, OPTION-A, CONTINUATION) are all SUPERSEDED.

The dispatch covers:
- Pipeline code addition: stratified-subsample mode with rare-lineage floors, on-disk D2 axes load, k=3 projection, HDBSCAN at appropriate min_cluster_size for ~10K subsample
- Math-before-code with **real** peak-memory projection (the projection at k=3, N≈10K is single-digit MB — no risk)
- Stratified-subsample composition design (lineage floors; rare-lineage representation guaranteed)
- Acceptance gates: ≥50 meaningful clusters, per-lineage purity, full-pool noise-assign for coverage check
- Decision tree at completion per § 2 above
- Out-of-scope: NO full-48K k=12 retry; NO cloud fire; NO k_final override beyond 3

## 6. What was NOT refuted by today's fires

- F1 (corpus + vocabulary hash): clean
- F2 weighting via sqrt-row-mult at PCA: clean (gandalf ratification stands)
- F3 (StandardScaler weighted via sample_weight): clean
- F4 (TruncatedSVD components 100 LSA + structured 60): clean
- F5 (PCA-primary lock): clean
- F6 (cluster purity / merge-candidate flag at < 20 members): unchanged

Axis discovery output (k=3 stable subset) is the **real Phase E-1 D2 deliverable**. The k=4-12 unstable tail is empirically a non-deliverable; it is methodology-driven over-extension of dimensionality, not substrate signal.

## 7. Cycle 9.9 carries (added by this resize)

| ID | Carry | Owner | Status |
|---|---|---|---|
| **9.9-A** | Frame-revision dispatch fire (Alternative 1: stratified subsample k=3) | legolas | PENDING Matt fire after Gate-1 ratification |
| 9.9-B | Gandalf addendum to kernel-panic-diagnosis note recording ratification-discipline failure | gandalf | COMMITTED; not yet on disk |
| 9.9-C | Discipline #18 amendment candidate (substrate-voting-is-binding) | jack-ryan | QUEUED in discipline-observations-for-jack-ryan.md |
| 9.9-D | Alternative 2 (substrate expansion via targeted rare-lineage crawls) — conditional on Alternative 1 outcome | legolas-Mode-B / elrond | DORMANT pending Alternative 1 result |
| 9.9-E | Cloud-bigger-HDBSCAN — conditional on production-grade validation need | star-lord (if it fires) | DORMANT |

---

## 8. Forensic record: 4 kernel panics in one day

| # | Time (EDT) | Pool | Expanded | Stage | Diagnosis |
|---|---|---|---|---|---|
| 1 | 03:11:11 | (pre-fire setup) | N/A | environment / first attempt | memory exhaustion; baseline residency too high |
| 2 | 03:32:14 | 16,699 rows | 22,065 × 4 | HDBSCAN.fit on F2-duplicated | row-duplication + HDBSCAN at smaller pool |
| 3 | 11:09:13 | 48,430 rows | 71,003 × 12 | HDBSCAN.fit on F2-duplicated | row-duplication + larger pool |
| 4 | 11:43:45 | 48,430 rows | 48,430 × 12 (un-expanded) | HDBSCAN.fit, single-stage F2 | **un-expanded HDBSCAN on 48K × 12 still exceeds 8 GiB**; refutes OPTION-A's memory hypothesis |

The setrlimit defensive ceiling (math-note §2) failed silently at process start with `WARNING: Could not set RLIMIT_AS: current limit exceeds maximum limit — proceeding without memory ceiling`. The belt-and-suspenders safety net was never engaged.

## 9. Discipline observation: confident framing on partial evidence (recurring pattern today)

Both today's framing failures share a structure:

| Framing call | When | What was claimed | What evidence justified |
|---|---|---|---|
| Smoke-frame artifact (knight-rider 03:25 EDT crash-triage handoff) | post-1st-panic | "k=4, 1-of-4 stable IS sample-frame artifact" | "smoke is N=100 monoculture; methodology test is full-mode" — hypothesis-only |
| Option-A memory comfort (knight-rider 11:15 EDT kernel-panic-triage note) | post-3rd-panic | "Option A should comfortably fit in 8 GB" | "half of >8 GB is still potentially >4 GB; HDBSCAN at n=48K, d=12 is unprofiled on this host" — hypothesis-only |

Both calls were confident framings on partial evidence; both cost a fire cycle to refute. Discipline-observation pattern: **forensic conclusions framed as confident causal explanations should be supported by evidence that the cheapest refuting test has been run.** This is already candidate Discipline #19; today's 4th panic + the resize-reframe is the third datapoint, escalating its priority.

---

**Signed:** knight-rider, post-resize 2026-05-23 ~12:00 EDT. Frame-revision dispatch authoring follows this note.
