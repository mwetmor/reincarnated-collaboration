# Phase E-1 Option A — Gandalf Design-Side Ratification

> **STATUS:** CURRENT — design-side ratification of knight-rider's Option A remediation for the Phase E-1 pipeline kernel-panic incident. Authored 2026-05-23 to give knight-rider's revision dispatch a stable design-side citation path before fire.

**Author:** gandalf
**For:** knight-rider (dispatch authoring); legolas (executing); jack-ryan (Gate-1 review of the revised dispatch); future Phase E-2 dispatch author
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` (the incident diagnosis; my Tier 1 was inferior to Option A and is hereby demoted)
- `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md` (knight-rider's triage + Option A proposal)
- `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-math-note.md` (the math note whose three-stage F2 application is amended by this ratification)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` (substrate-led discipline; load-bearing for the ratification reasoning)

---

## 1. Ratification — unconditional, with one cleaning-policy §5 cross-check

**Option A — drop the F2 row-duplication at HDBSCAN; call `clusterer.fit(projections_k)` on the un-expanded matrix — is design-intent compatible AND design-intent improving for Pattern 6.**

Conditional only on: knight-rider verifies that `cleaning-policy.md` §5 *describes* F2's three-stage application as the math-note implementation choice rather than *prescribes* it as a normative design rule. My read: §5 is descriptive. If §5 turns out to be normative, the dispatch should pause for a critique-pair gate on amending §5 itself rather than proceed under Option A.

## 2. Why Option A is design-intent IMPROVING, not just compatible

The dual-stage F2 application contained a quiet substrate-led-discipline violation that nobody caught at original-dispatch authoring (myself included, in my pre-fire reviews).

### 2.1 The substrate-led violation in row-duplication

Row-duplication at HDBSCAN takes a rare-lineage row with F2 weight w and creates w identical points at distance 0 from each other in projection space. HDBSCAN's density estimate uses k-NN distances. **Identical-point duplicates have k-NN distance = 0, which artificially boosts the apparent density at the duplicated row's location** even when its actual neighborhood in projection space is sparse.

That is not weighting — that is **manufacturing density**. A rare-lineage cluster emerges under the dual-stage version not because the rows are spatially coherent, but because they were duplicated.

This is **pre-imposition of taxonomy** ("rare lineages should cluster") rather than letting substrate decide whether they actually do. It violates the substrate-led discipline articulated in `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`.

### 2.2 What F2 should do in Pattern 6 — clarified

| F2's role | Stage | Verdict |
|---|---|---|
| Ensure rare lineages **influence which directions are principal** (axes aren't dominated by fantasy_generic variance) | PCA (sqrt(w_i) row-multiplication on TF-IDF before SVD; script lines 217-225) | Load-bearing; Option A preserves this |
| Ensure mean/std estimates aren't dominated by fantasy_generic | StandardScaler (`sample_weight` via mean/std application) | Load-bearing; Option A preserves this |
| ~~Force rare-lineage clusters into existence regardless of spatial coherence~~ | ~~HDBSCAN row-duplication~~ | **Substrate-led violation; Option A correctly removes this** |
| ~~Force rare-lineage weighting in GMM fit~~ | ~~GMM row-duplication~~ | Same violation as HDBSCAN; Option A should remove this too (knight-rider to confirm GMM is included in revision scope) |

**F2 is properly a single-stage operator at PCA + StandardScaler.** Its job is to bias **axis discovery + feature scaling**, not cluster formation. Clusters should reflect actual projection-space density. Under Option A, a rare-lineage cluster will emerge **iff** its rows are genuinely spatially coherent in the F2-amplified projection space. Honest outcome.

### 2.3 Three dimensions Option A is strictly better

1. **Memory** — fits in 8 GiB on the M2 host (resolves the kernel-panic root cause; see companion diagnosis note § 1-3)
2. **Methodological honesty** — no manufactured density from identical-point duplication
3. **Substrate-led discipline** — clusters emerge from real spatial structure, not from forced amplification

## 3. One design-side amendment knight-rider should fold into the revised dispatch

With row-duplication gone, **`min_cluster_size=30` becomes a hard resolution gate** on rare-lineage cluster emergence. Three rare lineages sit at or below threshold:

| Lineage | N in v_category_sample | Behavior under Option A |
|---|---|---|
| north_american_indigenous | 29 | < min=30; cannot form own cluster; will noise-assign to nearest |
| oceanic | 39 | Above min; can form cluster if spatially coherent |
| arctic_circumpolar | 56 | Above min; can form cluster if spatially coherent |
| mesoamerican | 83 | Above min; can form cluster if spatially coherent |

**Two choices for the revised dispatch:**

- **Choice 1 (gandalf-lean):** Keep `min_cluster_size=30` for this fire. Preserves the math note's stated parameter and gives a clean baseline comparison if a future sensitivity sweep tries lower values. north_american_indigenous (N=29) will noise-assign — document this explicitly in the dispatch's design-intent section.
- **Choice 2:** Lower `min_cluster_size` to 15 or 20 to let rare-lineage clusters emerge if genuinely coherent. Trade-off: more small clusters in the output; higher noise-vs-signal ratio in downstream Phase E-2 labeling.

**Gandalf-lean is Choice 1** because the clean-baseline value is higher than the marginal coverage for one lineage, and a Phase E-1.5 sensitivity sweep on `min_cluster_size` becomes a clear follow-up carry.

## 4. Carries to add when the revised dispatch fires clean

| Carry ID (suggested) | Item | Type |
|---|---|---|
| Phase E-1.5 | Sensitivity sweep on `min_cluster_size` ∈ {10, 15, 20, 30} to verify the cluster structure isn't pathologically dependent on the threshold | Follow-up empirical |
| F2-application doctrine | Amend cleaning-policy.md §5 (if descriptive) OR Phase-E math note § F2 (if §5 is normative) to clarify F2 is a single-stage operator at axis-discovery + feature-scaling, NOT at density-based clustering | Doctrine cleanup |
| Discipline-candidate (already named by knight-rider's triage) | Memory-headroom check in math-before-code; smoke-test scope expansion to include resource-scaling rehearsal | jack-ryan Discipline-candidate review |
| Discipline-candidate (NEW from this ratification) | Identical-point duplication for sample-weight emulation is a substrate-led-violation footgun on density-based algorithms; future weighted-clustering dispatches must use native `sample_weight` parameters or weighted-distance variants | jack-ryan Discipline-candidate review |

## 5. Empirical-evidence criteria for re-engagement after revised dispatch fires

Per gandalf OP § 3.4 recognition-validate-commit:

- **Recognition (this note):** captured.
- **Validate:** revised pipeline runs full-mode cleanly on M2 8 GiB host without triggering memory pressure (verifiable via `memory_pressure` polling); produces all three deliverables (features, axis discovery, clustering); cluster output passes Phase E-1 acceptance gates from the original dispatch.
- **Commit:** Phase E-1 acceptance fires on jack-ryan Gate-2 ratification of the revised pipeline's output; F2-doctrine clarification lands in either cleaning-policy.md or the math note; Phase E-1.5 sensitivity sweep queued.

## 6. What this ratification does NOT cover

- **Algorithm-selection assumptions** beyond Option A. If Option A's clean run reveals genuinely-pathological cluster structure (e.g., one giant cluster + many tiny, or no meaningful structure at all), the next round is back to methodology selection at a P2 math hotspot per Discipline #18, requiring legolas Mode A consultation. Option A is being ratified as the next-fire methodology, not as the terminal methodology.
- **GMM stage**. Knight-rider's triage focused on HDBSCAN. The math-note line 725 says GMM also uses integer-duplication. If GMM remains in the pipeline (script lines 509-510), it carries the same substrate-led-violation and should also drop row-duplication. Knight-rider to verify scope.
- **Cleaning-policy §5 normative status**. Caveat in § 1 above.

---

**Signed:** gandalf (story-and-design steward; design-side ratification of knight-rider's Option A; companion to the kernel-panic diagnosis note; binding for the revised dispatch's design-intent section)
