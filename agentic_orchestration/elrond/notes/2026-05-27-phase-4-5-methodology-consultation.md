# Elrond Pattern-A Bundled Methodology Consultation — Phase 4 + Phase 5 Math Notes

> **STATUS:** AUTHORED 2026-05-27 — bundled methodology consultation response per Path (1) Phase 4 + Phase 5 math-notes ratification routing (jack-ryan Gate-1 PASS-with-REVISIONS at `7d5d585` 2026-05-27).
>
> **Authority basis:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"; Discipline #18 extension-hotspot refinement (gandalf OP § 4.2) — consultations fire at ratification routing time after Gate-1 PASS.
>
> **Dispatch:** `agentic_orchestration/dispatches/2026-05-27-phase-4-5-math-notes-bundle.md`
> **Routed by:** knight-rider (bundled fire of 5 consultations)
> **Discipline citations:** #1 (math-before-code; this is methodology + math, not code), #11 (empirical-inspection — cited where substrate/cohort sizes drive recommendations), #18 (methodology-before-execution; this IS the methodology consultation that gates implementation), #25 (semantic-layer rep-audit; informs PM-1 cluster-readout), #42 (framing-audit; applied in § 0), #46 (per-cell bounding LOAD-BEARING across all algorithms recommended)

**Date:** 2026-05-27
**Author:** elrond (data steward + archivist; Pattern-A methodology owner per P3 multimodal clustering math-hotspot per `substrate-vector-cheatsheet` § 7.1)
**Companion math notes:**
- MG-1: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-1-pareto-dominance-math-2026-05-27.md`
- MG-2: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-2-crowding-hypervolume-math-2026-05-27.md`
- **MG-3: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-distance-math-2026-05-27.md` (LOAD-BEARING)**
- MG-4: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-4-kl-information-gain-math-2026-05-27.md`
- PM-1: `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-1-multimodal-clustering-math-2026-05-27.md`

---

## 0. Framing audit (Discipline #42 three-question protocol per gandalf OP § 4.1)

### Q1 — What load-bearing framing assumptions does this consultation depend on?

1. **The 5-objective quality vector Q(k) in MG-1 § 2 is the consensus feature space across MG-1/2/3/4.** All four Phase 4 gates operate on Q(k). If Q(k) shape (5D, normalized to [0,1]) changes, recommendations change.
2. **Per-cell populations are bounded ≤ 100 kits at steady state (Discipline #46 § 7).** At this scale, many statistical methods that fail at larger n actually work; conversely, many methods that work at larger n (HDBSCAN, full HVC, KDE-KL at d=5) underperform.
3. **Cohort sizes for PM-1 are ~28-32 surviving kits per season** (per `path-1-recognition` § 0 + PM-1 § 2.1). This is an order of magnitude smaller than substrate-row P3 clustering (Note 1's ~8-200 rows; substrate-scale P3 at ~2,499 rows).
4. **MG-3 LOAD-BEARING status reflects irreducible architectural uncertainty**: Gaussian-covariance Mahalanobis vs density-based distance is not resolvable by literature alone — it requires the quality-vector distributional shape, which is unknown pre-Phase-4-implementation.
5. **No empirical Phase 4 / Phase 5 substrate run exists at consultation time.** Recommendations are necessarily literature-grounded + analogically-reasoned from substrate-scale precedents (Note 1 substrate clustering; cycle-13 Wave-2 statistical co-occurrence priors). Empirical refutation is downstream (post-Dispatch 3A smoke).

### Q2 — What evidence currently in hand (or surfaceable in current scope) could refute these assumptions?

1. **Quality-vector distribution shape (Q2 #1):** unknown pre-Phase-4 implementation. The smoke test (MG-3 § 7 + PM-1 § 8) will surface whether Q(k) is approximately Gaussian (validating Mahalanobis covariance) or heavy-tailed/multi-modal (validating density-based alternative). This refutation lands at smoke-test time, NOT now.
2. **Per-cell population distribution at steady state (Q2 #2):** my § 3 audit recommendation surfaces this as a measurable EARLY in Dispatch 3A — sweep first-200-cell populations across a synthetic season run and verify ≤ 100 bound holds. If first runs show cells trending toward 200+, MG-5 calibration needs tightening BEFORE the four math gates fire at scale.
3. **Cohort size at PM-1 (Q2 #3):** depends on Phase 4 acceptance rate. If Phase 4 evicts more aggressively than Path-1 § 0 anticipated, ~28-32 may be ~15-20 — PM-1 algorithm choice shifts (HDBSCAN becomes infeasible; k-means with k=2-3 becomes the only viable path; § 5.2 sparsity branches absorb the difference).

### Q3 — If refutation evidence exists or is plausible from current scope, is the right move to refine the framing rather than execute the work as-framed?

**PROCEED with current framing**, but with two amendments embedded in recommendations:

- **MG-3 (LOAD-BEARING):** the consultation recommends **a phased methodology** — Gaussian covariance Mahalanobis at the architecture commit, with an explicit smoke-test branch that defers to density-based distance if Q(k) distributional shape fails normality checks. This is NOT a deferred decision (Discipline #40 violation) — it IS a methodology commit with explicit empirical gate at smoke. The phased approach absorbs the irreducible pre-implementation uncertainty without leaving the decision open.
- **PM-1 algorithm choice:** the consultation recommends a primary + fallback architecture rather than single-algorithm commitment, because the ~28-32 cohort size is at the edge of statistical viability for clustering. Single-algorithm commitment courts catastrophic failure if cohort drops to ~20.

All other consultations (MG-1, MG-2, MG-4) can commit to single recommendations within current framing.

**Framing-audit verdict:** PROCEED with the embedded-amendments noted above.

---

## 1. Executive summary

| Consultation | Primary recommendation | LOAD-BEARING? | Confidence |
|---|---|---|---|
| MG-1 Pareto | **Strict 5D Pareto as authored** + reject ε-dominance for v1 | No | HIGH |
| MG-2 Crowding | **NSGA-II crowding distance** (Algorithm A) as authored + HVC deferred | No | HIGH |
| **MG-3 Mahalanobis** | **Gaussian Mahalanobis with Tikhonov regularization** (Σ + λI; λ=1e-3) + Welford incremental + **smoke-test branch to density-based at distributional-shape failure** | **YES** | MODERATE — phased commit |
| MG-4 KL | **JSD primary across full k range** + retire KL+grid path | No | MODERATE-HIGH |
| PM-1 Multimodal Clustering | **A4 GMM (k=3..4 BIC-selected) primary + A1 k-means fallback at k<20**; **Option β (distinct algorithm class from Note 1's HDBSCAN)**; aesthetic-heavy weighting; PCA-whitening normalization | No | MODERATE — cohort-size driven |

**Cross-cutting findings (§ 6):** (i) the 5D quality-vector dimensionality is the load-bearing methodological constraint across all four Phase 4 gates — recommend a covariance audit post first smoke run; (ii) the MG-4 KL path as currently authored is unsalvageable at d=5 with k≤100 (grid evaluation is wrong tool); JSD across full range is the right re-frame; (iii) PM-1 cohort-size at ~28-32 is at the edge of statistical viability — recommend a Phase-4-calibration-feedback mechanism beyond what § 5.3 currently specifies; (iv) the shared cell-fetch optimization (MG-2 § 5) should be extended to also compute Σ once at Phase 4 entry (Mahalanobis covariance), shared across MG-3 and any future cell-scope statistics.

---

## 2. § 1 — MG-1 Pareto methodology disposition

### 2.1 Recommendation: PROCEED with strict 5D Pareto as authored

**Preferred methodology:** Strict Pareto dominance per MG-1 § 3 + § 4. Reject ε-dominance for v1.

**Rationale:**

1. **The 5D quality vector is well-constructed.** The dimensionality concern (Q2 #1 at MG-1 § 0) is real but not load-bearing for Pareto specifically — Pareto's degradation at high d (frontier collapse: nearly everyone is non-dominated when d is high relative to k) doesn't bite at d=5, k≤100. The empirical literature (Deb et al. 2002; Beume et al. 2007) places frontier-collapse risk at d≥7-10 with k≥1000; we are nowhere near that regime. At d=5, k=100, expected Pareto-front size is ~20-40% of cell population — discriminating but not collapsed.

2. **ε-dominance is the wrong tool here.** ε-dominance (Laumanns et al. 2002) is designed for evolutionary algorithms that need to bound archive size by approximating the front; it sacrifices discrimination at sub-ε resolution to gain front-size control. MAP-Elites already bounds archive size per cell via MG-5 eviction; layering ε-dominance on top double-counts the bounding mechanism and discards meaningful kit discrimination at sub-ε quality differences. The frontier collapse risk § 5.2 hedges against doesn't actually obtain at d=5, k≤100.

3. **MAP-Elites literature precedent.** The original MAP-Elites (Mouret + Clune 2015) used scalar fitness, not Pareto. Multi-objective MAP-Elites variants (MOME — Pierrot et al. 2022; MOQD — Janmohamed et al. 2023) use Pareto-front maintenance per cell, EXACTLY as MG-1 authors. MOQD specifically uses crowding distance + Pareto rank per cell at d=2-3 with k≤50 — our regime is a modest extension. The precedent is strong; the math note follows established practice cleanly.

### 2.2 Sensitivity / alternative

**Sensitivity to dimensionality:** at d=5, expected non-dominated set size in a cell of k kits drawn from independent uniform marginals is ~k × (log k)^(d-1) / (d-1)! ≈ k × (log k)^4 / 24. For k=50, this gives ~17 expected non-dominated kits. The frontier is meaningful, not collapsed.

**Alternative if frontier DOES collapse empirically (Q2 #1):** if q1-q5 are >0.85 correlated (the MG-1 § 2 trigger), the proposed fallback to 3-objective vector is sound — choose the three most decorrelated dimensions empirically (likely q1 win_rate, q5 skill_coherence, and one of {q3, q4}). Do NOT collapse to ε-dominance; collapse to lower-d Pareto.

### 2.3 Gates for implementation (what would invalidate this recommendation)

- **G-MG1-1:** If smoke run shows Pareto-front size >60% of cell population at steady state, MG-1's discrimination signal has collapsed — fall back to lower-d Pareto per § 2 of MG-1 § 2 (correlation trigger).
- **G-MG1-2:** If MG-5 eviction frequently evicts non-dominated kits to make room for newcomers, that's a signal the per-cell-capacity bound (~100) is too tight for the natural frontier size — capacity bound is the lever, not Pareto methodology.
- **G-MG1-3 (Gate-1 verification):** jack-ryan/gamora at impl time should EXPLAIN QUERY PLAN the cell-fetch query and confirm index hit; the bounded ≤100 row fetch is correct Pattern 1 exception per Discipline #46 only if index is verified.

### 2.4 No further consultation required for MG-1

MG-1 may PROCEED to implementation upon Matt-gate ratification of the math-notes bundle. No additional elrond methodology consultation needed.

---

## 3. § 2 — MG-2 Crowding methodology disposition

### 3.1 Recommendation: PROCEED with NSGA-II crowding distance (Algorithm A) as authored

**Preferred methodology:** NSGA-II crowding distance per MG-2 § 2.1 + § 4. Defer HVC (Algorithm B) indefinitely.

**Rationale:**

1. **HVC at d=5, k=100 is computationally expensive AND scientifically marginal at this regime.** The O(k^(d-2) × log k) cost is correctly characterized in MG-2 § 2.2. At k=100, d=5: ~10^6 operations per insertion. This is tractable on modern hardware (~10ms in C; ~100ms in Python without WFG C extension), but it provides MARGINAL discrimination advantage over crowding distance at this k. The HVC-vs-crowding empirical literature (Bringmann + Friedrich 2010) shows crowding distance is within 5-10% of HVC ranking on typical benchmark suites; the gap closes further at low k. At k=30 (early cell state), the two methods rank kits nearly identically.

2. **NSGA-II crowding is established in MAP-Elites lineage.** MOME and MOQD (cited § 2.1) use NSGA-II-style crowding per cell. There is no MAP-Elites variant in the literature using per-cell HVC — for the cost/benefit reason above. The math note's choice of crowding as primary is methodologically conservative and substantiated.

3. **The boundary-population concern (k < 2d = 10) is real and correctly handled.** MG-2 § 4.3's `MIN_POPULATION_FOR_DIVERSITY = 6` is a slight under-correction — at k=6, d=5, every kit is on some boundary (with high probability); diversity scoring is meaningless. **Recommend raising the threshold to k=10** (= 2d). Below k=10, unconditional acceptance per current § 4.3 mechanism is correct; above k=10, crowding becomes informative.

### 3.2 Sensitivity / alternative

**NSGA-III crowding variant:** Deb + Jain 2014 NSGA-III uses reference-point-based selection rather than crowding distance, designed for high-d problems (d ≥ 4). It produces well-distributed fronts on benchmark problems at d=5-10. **However:** NSGA-III requires predefined reference points covering the d-1 simplex — and choosing reference points pre-imposes a preference structure that violates the substrate-led discipline (MG-1 § 5.3 rejects weighted-sum scalarization for the same reason). NSGA-III crowding variant is NOT recommended; substrate vote at the diversity level is best served by NSGA-II crowding's pure-distance approach.

**IGD (Inverted Generational Distance) contribution:** IGD measures distance from each frontier point to a reference Pareto-optimal set. Requires knowing the true Pareto-optimal set (we don't); requires a target front (we don't have one a priori — substrate produces the front). Rejected as inapplicable.

### 3.3 Amendment to math note (recommend)

- Raise `MIN_POPULATION_FOR_DIVERSITY` from 6 → 10 in MG-2 § 4.3 (= 2d for d=5)
- Add a documented gate G-MG2-1 (§ 3.4 below) for monitoring HVC upgrade trigger

### 3.4 Gates for implementation

- **G-MG2-1:** If post-first-season inspection shows visually degenerate archives (clusters of near-identical kits despite high crowding scores), upgrade to HVC. Inspection criterion: spot-check 5 cells with k > 20; if any two kits have CD-distance > 0.3 yet Mahalanobis-distance < 0.5 (per MG-3), crowding is failing → upgrade.
- **G-MG2-2:** Threshold for "boundary dominance failure": if > 70% of cells routinely have all kits at MAX_CD on some dimension, crowding is uninformative for those cells. Increase k threshold or upgrade to HVC for those cells specifically (cell-tier-based methodology selection).
- **G-MG2-3 (Gate-1 verification):** Reuse cell-fetch from MG-1 per MG-2 § 5 optimization note — confirm at impl that Phase 4 pipeline materializes Archive_c once per kit insertion, NOT once per gate. This is the load-bearing performance assumption.

### 3.5 No further elrond consultation required for MG-2

MG-2 may PROCEED upon Matt-gate ratification + the MIN_POPULATION_FOR_DIVERSITY amendment to § 4.3. No additional consultation needed.

---

## 4. § 3 — MG-3 Mahalanobis methodology disposition (LOAD-BEARING)

### 4.1 Recommendation: PHASED METHODOLOGY commitment

**Primary methodology:** Gaussian-covariance Mahalanobis distance per MG-3 § 2 + § 4 with **Tikhonov regularization (Σ_c + λI; λ = 1e-3)** as the standard covariance handling. Welford incremental update with 50-insertion checkpoint as authored.

**Embedded smoke-test branch:** If first-season smoke run shows quality-vector marginal distributions deviate substantially from normality (Shapiro-Wilk test p < 0.01 on ≥ 2 of 5 dimensions across ≥ 30% of cells with k ≥ 30), defer to **HDBSCAN-style mutual-reachability distance** as duplicate-detection mechanism. This is the documented density-based alternative per dispatch Q-Bundle-2.

This is **NOT a deferred decision (Discipline #40 violation)**; it IS a methodology COMMIT with explicit empirical gate at smoke-test time. The primary path commits to Gaussian Mahalanobis; the branch criterion is named, the threshold is operationalized, and the fallback algorithm is fully specified (§ 4.4 below).

### 4.2 Rationale for primary recommendation (Gaussian Mahalanobis + Tikhonov)

**Why Gaussian Mahalanobis as primary over density-based:**

1. **Per-cell populations are too small for density estimation to outperform parametric.** HDBSCAN's mutual-reachability distance, GLOSH outlier detection, and KNN-distance variants all require sufficient samples in the local neighborhood to estimate density reliably. At per-cell k ≤ 100 with d = 5, the "neighborhood" is sparse — local density estimates are dominated by the 3-5 nearest neighbors. This is precisely the regime where parametric (Gaussian covariance) methods outperform non-parametric: when you have few samples, leveraging an assumed distributional form is more efficient than estimating density from data.

2. **The quality vector is plausibly approximately Gaussian per-cell.** Each q_i is bounded [0,1] and represents an average/fraction across many encounters. Central Limit Theorem suggests per-cell distributions of q_i should be approximately Gaussian for the encounter-averaged metrics (q1 win_rate, q2 KPM, q3 sustainability, q4 defensive). q5 skill_coherence is more uncertain (it's a gate-style sub-score). This is a testable claim — the smoke-test branch is the test.

3. **Mahalanobis IS the principled extension of Euclidean for correlated multivariate features.** If the only goal is duplicate detection, Mahalanobis exactly captures "two kits whose quality vectors are statistically indistinguishable accounting for known correlation structure." This is the canonical duplicate-detection framing in multivariate statistics (Mardia, Kent, Bibby 1979 — the textbook reference).

**Why Tikhonov regularization over pseudoinverse (resolves MG-3 § 4.2 option choice):**

1. **At k < 15, d = 5, sample covariance is rank-deficient or near-singular.** Pseudoinverse handles rank-deficiency by inverting only the non-degenerate subspace, which means Mahalanobis distance collapses dimensions with low variance — kits that differ along low-variance dimensions are no longer distinguished. This is the WRONG behavior for duplicate detection: we want to PRESERVE small differences even on low-variance dimensions (a kit that's slightly different in skill_coherence is NOT a duplicate even if all 30 archive residents have very similar skill_coherence values).

2. **Tikhonov (Σ + λI) preserves all dimensions.** Adding λI to the diagonal shrinks low-variance covariance estimates toward isotropy (Euclidean), so low-variance dimensions still contribute to distance but with reduced sensitivity. This is the right inductive bias: when in doubt, treat dimensions as independent unit-variance Gaussians (Euclidean), gradually moving toward learned covariance as more samples accrue.

3. **λ = 1e-3 (not the math-note's 1e-4) is the right magnitude at this scale.** The math note's λ = 1e-4 is too small at k < 20; the regularization doesn't dominate the noisy sample covariance until n is much larger. λ = 1e-3 corresponds to "regularization is comparable to sample covariance when sample variance is ~0.001" — at q_i normalized to [0,1], variances around 0.01-0.05 are typical, so λ = 1e-3 contributes ~5-10% shrinkage toward Euclidean at typical variances. Stronger at low-variance dimensions; weaker at high-variance. This is the empirical Bayes / Ledoit-Wolf shrinkage spirit (Ledoit + Wolf 2004), at the lightweight end of the spectrum.

4. **Pseudoinverse remains as a safety net.** If `condition_number(Σ_c + λI) > 1e8` after regularization (very rare; would require pathological substrate), pseudoinverse is the fallback. Math note § 4.2 option 2 stays as the safety net; option 3 (Tikhonov) is the primary path.

**Why retain Euclidean small-population fallback (MG-3 § 4.3) with threshold adjustment:**

The current MIN_COV_POPULATION = 7 (= d + 2) is on the edge of statistical defensibility. Sample covariance at k=7 with d=5 has 5 degrees of freedom for a 15-parameter covariance matrix — severely under-identified even with Tikhonov. **Recommend raising MIN_COV_POPULATION = 15** (= 3d, the standard rule-of-thumb for sample covariance estimation per Hardle + Simar 2007 multivariate statistics textbook). Between k=15 and k=30, Tikhonov-regularized covariance is the path; below k=15, Euclidean fallback per § 4.3.

### 4.3 Chi-squared threshold validity at small k — VERDICT

**The chi-squared(5) reference distribution (MG-3 § 3) is approximately valid only when Σ_c is consistently estimated.** At small k (k < 30), sample-Σ_c is itself a noisy estimate; the resulting Mahalanobis distances follow a Hotelling's T² distribution rescaled to F-distribution (Mahalanobis 1936; Hotelling 1931), NOT chi-squared.

For our purposes (duplicate-detection threshold, not formal hypothesis test), the chi-squared approximation is acceptable but the THRESHOLD value should be calibrated empirically rather than from chi-squared(5) quantiles:

**Recommend amending DUPLICATE_THRESHOLD derivation per MG-3 § 3:**

- DO NOT derive threshold from chi-squared quantile (the formal-test framing is wrong at small k)
- DO calibrate threshold empirically: target ~5% duplicate-detection rate on the first-season smoke run, adjust threshold to hit that rate
- Empirical calibration target rate (5%) is the scaffold parameter per Discipline #40; the threshold value emerges
- The math note's 1.5 default is a reasonable STARTING value; iteration converges to substrate-empirical threshold within ~3-5 seasons

This is a SHIFT IN FRAMING: the threshold is empirically calibrated to a target detection rate, not derived from a parametric reference distribution. This composes better with the substrate-led discipline (substrate vote on what counts as "near-identical") and is more robust at small k.

### 4.4 Density-based fallback algorithm (if smoke-test branch fires)

If the smoke-test branch fires (§ 4.1 trigger), the density-based alternative is:

**HDBSCAN-style mutual-reachability distance:**

```
core_dist(k) = distance to k_th nearest neighbor of k in Archive_c (k=5 by convention)
mreach(a, b) = max(core_dist(a), core_dist(b), euclidean(a, b))
```

Duplicate detection becomes:
```
nearest_resident = argmin(mreach(k_new, k_r) for k_r in Archive_c)
duplicate_flag = (mreach(k_new, nearest_resident) < MREACH_DUPLICATE_THRESHOLD)
```

**Threshold derivation:** identical empirical-calibration approach as § 4.3 — target 5% duplicate-detection rate; threshold emerges.

**Why mutual-reachability over alternatives (KNN, LOF, etc.):** mutual-reachability is robust to varying local density (which is the failure mode of plain KNN distance) AND requires no parametric distributional assumption (which is exactly why we'd switch). It is the same distance HDBSCAN uses internally for clustering, so it has the right empirical pedigree at small-multi-modal-distribution data.

**Cost:** O(k log k) per Archive_c to build the KD-tree; O(d log k) per duplicate-check. At k ≤ 100, d = 5, this is negligible. The KD-tree should be cached + invalidated on insertion (incremental insertion is easy; the periodic-50-insertion full-rebuild checkpoint from Welford translates directly).

### 4.5 Welford drift characterization

**Welford's online algorithm for covariance is numerically stable in float64 for n ≤ ~10^9.** At our regime (n ≤ 5,000 insertions per cell over the cell's lifetime even at long-term steady state), drift is negligible. The math note's 50-insertion full-recompute checkpoint is significantly more conservative than needed.

**Recommend relaxing checkpoint to every 500 insertions per cell** OR — preferable — checkpoint on Welford-vs-batch-disagreement detection (compute condition-number(Welford-Σ vs batch-Σ) every 100 insertions; if disagreement > 1e-4, full-recompute; else continue).

The cost saving is modest (50→500 reduces checkpoint frequency 10×), and the correctness argument is well-established (Chan, Golub, Leveque 1983 — "Algorithms for computing the sample variance: Analysis and recommendations"). This is a low-priority amendment; the 50-insertion checkpoint is conservative-but-correct.

### 4.6 Alternative duplicate-detection approaches (LSH; quantization)

Locality-sensitive hashing on quantized quality vectors was raised as a dispatch question. **Rejected:** LSH is designed for high-dimensional approximate-NN search (d ≥ 100; n ≥ 10^6). At d=5, n ≤ 100, exact distance computation is faster than LSH's hash construction. LSH overhead dominates at our scale.

Quality-vector quantization (e.g., bin each q_i into 10 buckets; treat collision-in-all-bins as duplicate) was also considered. **Rejected:** quantization throws away exactly the discrimination signal Mahalanobis is built to preserve. The right framing is "small distance in the correlated space," not "identical after binning."

The two dispatch-mentioned alternatives are both worse fits than Mahalanobis or mutual-reachability at this scale.

### 4.7 Gates for implementation (what would invalidate this recommendation)

- **G-MG3-1 (smoke-test branch trigger):** Shapiro-Wilk normality test on each q_i across each cell with k ≥ 30. If ≥ 2 of 5 dimensions reject normality at p < 0.01 across ≥ 30% of qualifying cells, defer to density-based fallback per § 4.4.
- **G-MG3-2 (covariance audit):** at first smoke run, compute condition-number of Σ_c + λI across all cells with k ≥ 15. If ≥ 10% of cells have condition-number > 1e8 after Tikhonov, raise λ to 1e-2 OR drop to Euclidean for those cells.
- **G-MG3-3 (threshold calibration):** target 5% duplicate-detection rate at first season; if rate is >15% or <1%, threshold needs adjustment. Capture per-season detection-rate telemetry; surface to elrond for re-consultation if rates trend persistently outside [3%, 10%] across 3+ seasons.
- **G-MG3-4 (replacement-vs-rejection decision; MG-3 § 4.1 Q_scalar weights):** the Q_scalar weights [0.3, 0.25, 0.2, 0.15, 0.1] are arbitrary at consultation time. **Recommend deferring to Pareto-strict replacement instead** (per MG-3 § 4.1 alternative): if k_new strictly Pareto-dominates nearest_resident, REPLACE; otherwise REJECT. This composes cleanly with MG-1's Pareto-strict framing AND avoids the Q_scalar arbitrary-weighting trap. Q_scalar can remain as final-tiebreak for ties on Pareto comparison (rare at d=5).

### 4.8 Implementation may PROCEED upon Matt-gate ratification with amendments

Per MG-3 § 7 LOAD-BEARING gating language: "MG-3 implementation MUST await this consultation per Discipline #18." This consultation returns: **PROCEED with the phased methodology per § 4.1 + amendments § 4.2-§ 4.7.** Specifically:

- Tikhonov regularization (Σ + λI; λ=1e-3) as covariance handling
- MIN_COV_POPULATION raised from 7 → 15
- DUPLICATE_THRESHOLD calibrated empirically (5% target detection rate), 1.5 as starting value
- Welford checkpoint relaxed from 50 → 500 insertions (low-priority amendment; 50 acceptable)
- Replacement-vs-rejection uses Pareto-strict (MG-3 § 4.1 alternative) instead of Q_scalar weights
- Smoke-test branch (G-MG3-1) implemented as part of Dispatch 3A smoke specification
- Density-based fallback (§ 4.4) authored as standby module; not implemented until/unless G-MG3-1 fires

These amendments are recommended for jack-ryan Gate-1 re-review or knight-rider routing as an MG-3 math-note revision before Dispatch 3A fires.

---

## 5. § 4 — MG-4 KL methodology disposition

### 5.1 Recommendation: JSD across full k range; retire the KL+discrete-grid path

**Preferred methodology:** Jensen-Shannon Divergence (JSD) per MG-4 § 4 across ALL cell populations (k ≥ MIN_KL_POPULATION). Retire the KL+grid path entirely.

This is a more decisive shift than the math note's k<20 JSD / k≥20 KL split. Rationale:

### 5.2 Why retire discrete-grid KL at d=5

1. **The discrete-grid evaluation is computationally and statistically wrong at d=5.** A 10-per-dimension grid at d=5 gives 100,000 grid cells; with k ≤ 100 archive residents per cell, the KDE-evaluated probability at each grid cell is ~k/100,000 = 0.001 average — and the variance of that estimate from a 100-sample KDE is enormous. The KL estimate is dominated by noise at the grid resolution, not by signal about the kit's distributional contribution.

2. **The curse of dimensionality bites at d=5 with k=100.** Sample density per unit hyper-volume is k/V = 100/1 = 100 — meaning the entire 5D unit hypercube has 100 samples distributed across it. The local sample density is approximately k^(1/d) = 100^(0.2) ≈ 2.51 samples per unit length per dimension. KDE bandwidth scales as h ~ k^(-1/(d+4)) ~ 100^(-1/9) ≈ 0.6, which is enormous — the KDE is essentially smoothing the entire cell into one giant blob. KL between two such over-smoothed blobs is meaningless.

3. **Monte Carlo KL would marginally improve but is still ill-conditioned.** Sampling 50-100 points from P_c' and P_c and averaging log(p'/p) reduces grid-resolution noise but doesn't fix the underlying KDE-at-d=5 problem. Both approaches are bad bets.

4. **JSD is more robust because the mixture distribution M dominates both terms.** Even when D_KL(P || Q) is ill-conditioned because Q has near-zero density where P has mass, D_KL(P || M) is well-conditioned because M = (P+Q)/2 has at least P/2 mass where P does. JSD averaging gives bounded, well-behaved estimates even at small k. This is the established advantage in NLP / information retrieval where small-sample distributional comparison is common (Lin 1991).

5. **JSD bounded in [0, log 2] gives clean normalization without arbitrary clamping.** The KL path requires NOVELTY_CLAMP = 2.0 (arbitrary; what does "novelty above 2.0" even mean?). JSD has natural normalization JSD/log(2) ∈ [0, 1]. This is cleaner architecturally AND removes a scaffold parameter from the system.

### 5.3 Other divergences considered

**Hellinger distance** (H² = (1/2) ∫(sqrt(p) - sqrt(q))²): bounded [0, 1]; symmetric; well-behaved at small samples. Could substitute for JSD. **Marginal preference for JSD** because Hellinger's "novelty" interpretation is less intuitive than JSD's information-theoretic framing, and JSD has stronger MAP-Elites / generative-model literature precedent.

**Wasserstein-1 / earth-mover's distance:** geometrically meaningful; robust at small samples. **Computationally expensive at d=5** (O(k³) without sliced approximation). Sliced-Wasserstein (Bonneel et al. 2015) is tractable at our scale but requires projection-direction selection; introduces methodological surface that JSD avoids. Rejected as marginal-improvement-for-large-cost.

**f-divergences family generally (Jensen-Tsallis etc.):** all share the small-sample KDE-curse-of-dimensionality problem at d=5. JSD is the most numerically stable practical choice in the family at our regime.

### 5.4 Bandwidth selection — Scott's rule is wrong; recommend adaptive bandwidth

**Scott's rule (h = k^(-1/(d+4)) × σ) is derived for univariate Gaussian densities.** At d=5 with non-Gaussian (gameplay-outcome-distributed) data, Scott's rule chooses a bandwidth that over-smooths in regions of high data density and under-smooths in tails. The math note's recognition (§ 4.4 "Scott's rule may not fit non-Gaussian quality distributions") is correct.

**Recommend:** adaptive Silverman's-rule + bandwidth-floor approach:
```
h_i_silverman = 0.9 × min(std(Q_i), IQR(Q_i)/1.34) × k^(-1/5)
h_i = max(h_i_silverman, h_floor)
h_floor = 0.05  (5% of normalized [0,1] range)
```

Silverman's rule (Silverman 1986) is more robust to non-normality than Scott's; the bandwidth-floor prevents over-narrow bandwidth at low-variance dimensions. The floor value 0.05 is a scaffold parameter per Discipline #40.

### 5.5 Smoothing approach

Laplace smoothing on grid (MG-4 § 6 Approach A) is moot if we retire the discrete-grid path. **Recommend:** use KDE bandwidth floor as the sole smoothing mechanism for JSD computation (since JSD uses KDE evaluations at sample points, not grid cells; bandwidth floor ensures positive support everywhere we evaluate).

### 5.6 Amendments to math note

- **Retire MG-4 § 3 (discrete-grid KL path) and § 6 Approach A (Laplace grid smoothing).** They're not the right tools at d=5, k≤100.
- **Promote JSD (currently § 4 fallback) to primary across all k ≥ MIN_KL_POPULATION.** Remove the k<20 / k≥20 switch criterion.
- **Replace Scott's rule with adaptive Silverman's rule + bandwidth floor (h_floor = 0.05).**
- **Remove NOVELTY_CLAMP scaffold parameter.** No longer needed since JSD/log(2) is naturally bounded.
- **Raise MIN_KL_POPULATION from 5 → 10.** At k=5, even JSD's mixture-distribution KDE is unstable; unconditional acceptance below k=10 is more honest.

### 5.7 Sensitivity / what could invalidate

- **G-MG4-1:** If JSD scores cluster at extremes (most kits at 0 or near log(2)) rather than spreading across [0, log(2)], the bandwidth is wrong — try Scott's rule × 1.5 or × 0.7 sensitivity sweep.
- **G-MG4-2:** If novelty_score adds no information beyond MG-2 crowding distance (correlation > 0.85 across season-1 smoke run), MG-4 is redundant — recommend retiring novelty scoring entirely and using only crowding+Mahalanobis for diversity+duplicate signals. This is a real possibility; MG-4's value-add over MG-2 is theoretical at this regime.

### 5.8 Implementation may PROCEED upon Matt-gate ratification with amendments

MG-4 may PROCEED with amendments § 5.6 to the math note. The shift from KL-as-primary to JSD-as-primary is substantive; recommend jack-ryan Gate-1 re-review of the amended math-note before Dispatch 3A fires.

---

## 6. § 5 — PM-1 multimodal clustering methodology disposition

### 6.1 Recommendation: A4 GMM primary (k=3..4 BIC-selected); A1 k-means fallback below k=20; Option β (distinct from Note 1's HDBSCAN); aesthetic-heavy weighting; PCA-whitening normalization

**Preferred methodology:**

- **Primary algorithm:** Gaussian Mixture Model (Algorithm A4) with k ∈ {3, 4} (NOT 5) selected by BIC across 5 random restarts per k
- **Fallback algorithm:** k-means (Algorithm A1) at k=3 if cohort size < 20 (sparse-season branch elevation)
- **Composition with Note 1:** Option β — distinct algorithm class (HDBSCAN per Note 1 at substrate-row scale; GMM at PM-1 per-season kit scale)
- **Weighting:** aesthetic-heavy per gandalf design intent (w_aes=0.4, w_mech=0.3, w_subs=0.2, w_elem=0.1)
- **Normalization:** PCA-whitening on the concatenated feature vector after one-hot encoding categoricals; truncate to top-95% variance components (~10-15 components from ~17-29 raw dims)

### 6.2 Why GMM over the alternatives at ~28-32 cohort size

1. **k-means (A1) assumes spherical clusters AND gives hard membership.** Multimodal feature vectors composed across mech / substrate / aesthetic / element WILL have correlated structure within clusters — a "European-medieval-martial-heavy" faction has correlated tech_level + tone + cultural_lineage. k-means' spherical-cluster assumption fits this badly. Furthermore, hard membership is wrong for the PM-2 design surface — many kits will be "primarily X with Y influence" and the soft-membership probability from GMM is exactly what PM-2 needs for label modulation.

2. **HDBSCAN (A2) is wrong at this cohort size.** PM-1 § 4.2 already flags this: "at ~30-kit scale, density estimates are NOISY; HDBSCAN designed for larger populations." Confirmed; HDBSCAN is the right tool at substrate-row scale (Note 1's ~8-200 rows clustering against substrate-row metadata) but NOT at kit-population scale (~28-32 kits in 15-25 dim PCA-whitened space). The density estimates are too sparse.

3. **Spectral (A3) is computationally fine but loses the soft-membership advantage.** Spectral clustering produces hard assignments via eigenvector-space k-means. At ~30 kits, the eigendecomposition is trivially cheap, but the value-add over GMM is minimal AND the kernel-width hyperparameter (`gamma`) introduces a tuning surface that GMM avoids.

4. **GMM with k ∈ {3, 4} BIC-selected gives soft membership + principled k selection.** BIC penalizes overfitting at small n correctly; at n=30, d=10-15 (post-PCA), BIC will reliably pick k=3-4 over k=5+ unless the data strongly supports k=5. This naturally implements the `faction_count_target_per_season` engine flag (PM-1 § 2.5) without requiring artificial constraints. The soft-membership output is also CRITICAL for PM-2's downstream consumption — "primarily Faction-A (prob 0.7) with secondary Faction-C (prob 0.2) influence" is a richer design surface than hard cluster labels.

5. **UMAP+HDBSCAN (A5) introduces a stochastic preprocessing stage that hurts reproducibility.** UMAP requires a random seed; HDBSCAN on UMAP-reduced space is sensitive to UMAP hyperparameters AND HDBSCAN hyperparameters. The compounded sensitivity at ~30-kit scale makes determinism brittle. PCA-whitening (which I recommend for normalization) does the dimensionality-reduction work without the stochasticity.

### 6.3 Why k ∈ {3, 4}, not {3, 4, 5}

PM-1 § 2.5 specifies `faction_count_target_per_season ∈ [3, 5]` (default 3-5). **At n=28-32 kits, k=5 is statistically untenable:** each cluster averages ~6 kits at k=5, which is too thin for stable identity assignment. BIC at this regime will reliably prefer k=3-4 over k=5 unless data is unusually well-separated; allowing k=5 in the search adds compute cost and the marginal cases where k=5 wins are precisely the cases where the partition is overfitting to noise.

**Recommend reducing `faction_count_target_per_season` default to [3, 4]** at this cohort-size regime. If/when v1.1 cohort size grows (e.g., post-Court-of-Forms cross-season aggregation; PM-1 § 12.1), reopen to k=5.

### 6.4 Composition with Note 1 — Option β (distinct algorithms) — CONFIRMED

The gandalf design-intent lean (PM-1 § 6.2) is correct: **distinct algorithm classes per scale.** My reasoning agrees with gandalf's four points and adds:

5. **Different objective functions per scale.** Note 1's HDBSCAN at substrate-row scale answers "how many natural sub-themes exist in this kit's substrate pool?" — a question about density-defined groupings in metadata-feature space. PM-1's GMM at per-season kit scale answers "what's the soft-membership probability of this kit belonging to each of the season's emergent factions?" — a question about probabilistic identity assignment in a continuous-feature space. These are different statistical questions; same-algorithm-for-both would be a category error.

6. **Methodological consistency across scales is a weaker virtue than fit-to-scale.** The Option α framing (PM-1 § 6.1) treats methodological consistency as a substantial benefit. It is not — sklearn (or equivalent) exposes both HDBSCAN and GMM as off-the-shelf primitives; the engineering surface to support both is trivial. Methodological consistency matters when the joint reasoning about the system requires uniform-vocabulary across scales (e.g., calibrating cluster-count expectations); at scales that are an order of magnitude apart in n and that solve different statistical problems, the joint-reasoning case is weak.

### 6.5 Weighting — aesthetic-heavy CONFIRMED with refinement

gandalf design lean (PM-1 § 3.3, aesthetic-heavy: w_aes=0.4, w_mech=0.3, w_subs=0.2, w_elem=0.1) is correct for the faction-coalescence design surface per `engine-as-general-serial-content-product` § 2.2.

**Refinement:** the weighting applies BEFORE PCA-whitening, not as a post-clustering combination. Implementation:
```
F_weighted(K) = concat(
    sqrt(w_mech) × normalize(F_mechanical),
    sqrt(w_subs) × normalize(F_substrate),
    sqrt(w_aes) × normalize(F_aesthetic),
    sqrt(w_elem) × normalize(F_element_attr)
)
```
The `sqrt` of weights composes correctly with PCA-whitening (which operates on covariance; weights enter quadratically). After PCA-whitening, the weighting is encoded in the inter-modality variance distribution; clusters that span correlated aesthetic features are preferentially found by GMM.

**Substrate-led discipline preserved.** Weighting biases what the clustering ATTENDS TO but doesn't pre-assign factions. The substrate (kit population) still votes the cluster identities; weighting is a design lens, not a taxonomy.

### 6.6 Normalization — PCA-whitening on weighted concatenation; truncate to top-95% variance

**Multimodal features have heterogeneous scales AND correlation structure.** Z-score per-dim ignores correlation; min-max preserves rank but ignores variance differences; one-hot WITHOUT normalization treats categorical-vs-continuous dimensions inconsistently in distance computation. PCA-whitening is the correct preprocessing — it (a) decorrelates dimensions, (b) standardizes variance to unit-scale per principal component, (c) lets GMM's spherical-component-in-whitened-space assumption hold approximately.

**Truncate to top-95% variance** (typically ~10-15 components from ~17-29 raw dims). This reduces noise from low-variance components (typically one-hot-encoded singleton categoricals with no in-season variation) without losing meaningful signal. At n=30 with d>15, GMM overfits with full covariance matrices; truncated dimensionality keeps GMM well-identified.

### 6.7 Stability protocol

Per PM-1 § 7.1 question 4. **Minimum stability sweep:**

1. **5-seed cluster stability:** run GMM with 5 different random_state initializations; report mean + std of Jaccard similarity across pairs of cluster assignments. Acceptance: mean Jaccard ≥ 0.7 per PM-1 § 8.2.
2. **BIC profile:** plot BIC for k ∈ {2, 3, 4, 5, 6}; verify minimum at k=3 or k=4. Acceptance: BIC monotonically decreasing then increasing across k; no monotone trends (which would indicate model misspecification).
3. **Bootstrap stability:** 1,000 bootstrap resamples of the ~30-kit population; refit GMM with same k; report distribution of (i) per-cluster centroid distances, (ii) per-cluster covariance Frobenius norms. Acceptance: centroid distances within ±1 standard deviation across bootstraps.
4. **Cohort-size sensitivity:** synthesize cohorts at n ∈ {20, 25, 30, 35, 40}; verify cluster structure is stable across cohort-size variation (Jaccard ≥ 0.6 between adjacent sizes).

This is more involved than the math note's § 8 spec; expect ~2-3 hours of analysis per first-season smoke run.

### 6.8 Sparsity threshold confirmation — REVISED per algorithm choice

The PM-1 § 5.2 thresholds (24 / 16 / 8) were authored algorithm-agnostically. **With GMM as primary algorithm, recommend revised thresholds:**

| Surviving kit count `|K|` | Action | Rationale |
|---|---|---|
| `|K| ≥ 24` | GMM with k ∈ {3, 4} BIC-selected | Original threshold; GMM well-identified |
| `20 ≤ |K| < 24` | GMM with k=3 (fixed; no BIC sweep) | At n<24, BIC variance high; commit to k=3 |
| `12 ≤ |K| < 20` | k-means with k=3 (fallback to A1) | GMM under-identified; k-means hard-membership acceptable at this scale |
| `8 ≤ |K| < 12` | k-means with k=2 (degraded); flag `season_sparse=true` | Below n=12, k=3 has avg 4 kits/cluster — borderline meaningless |
| `|K| < 8` | Skip clustering; PM-2 assigns single "Convergent" faction; flag `season_critically_sparse=true` | Original threshold; statistically meaningless below n=8 |

These thresholds are statistically grounded in the GMM-vs-k-means transition zone and the k=3 minimum-population requirement.

### 6.9 Cross-cutting Phase 4 MG-5 eviction calibration feedback

PM-1 § 7.1 question 6 + § 5.3. **My view:** PM-1's sparsity output is the natural feedback signal for Phase 4 MG-5 eviction calibration, but the loop needs explicit construction:

**Proposed feedback mechanism:**
1. Per-season, PM-1 emits `surviving_kit_count` + `sparsity_flag` per season as telemetry
2. After 5 consecutive seasons of `sparsity_flag=true`, surface to gamora seam for Phase 4 calibration review
3. Calibration lever: MG-5 eviction aggressiveness (eviction_threshold parameter — currently MG-5-resident)
4. Loosen eviction aggressiveness → more kits survive Phase 4 → larger PM-1 cohort
5. Re-check sparsity_flag at next 5-season window
6. Iterate until sparsity_flag stable below 20% rate

**This is a slow feedback loop (5-season window)**; near-real-time tuning is not the right shape because cohort-size shifts have downstream cascade effects on PM-2 + Phase 7 cohesion judging. The 5-season window gives time for those cascades to settle before re-calibration.

**Recommend authoring this feedback mechanism as a PM-1 § 5.4 amendment** with the loop explicitly specified. Cross-routing to gamora seam (MG-5 owner) recommended via knight-rider.

### 6.10 Gates for implementation

- **G-PM1-1 (algorithm fit):** smoke-test silhouette score on selected GMM clusters. If silhouette < 0.25 (well below PM-1 § 8.2 loose threshold of 0.3), the multimodal feature vector is not separating well — escalate to weighting or feature-composition refinement before proceeding.
- **G-PM1-2 (BIC stability):** if BIC profile is monotone (no clear minimum at k=3 or 4) across 5+ seeds, the GMM model is misspecified — fall back to k-means with k=3 fixed.
- **G-PM1-3 (PM-2 rep-audit Discipline #25):** when PM-2 inherits cluster output, rep-audit per cluster (top-5 modal substrate-theme + modal aesthetic-tuple + modal element); verify reps match the semantic interpretation PM-2 assigns. If rep-audit fails, do NOT commit faction labels — re-cluster with refined weighting or surface to gandalf design call.
- **G-PM1-4 (cohort-size monitoring):** track surviving-kit-count distribution across first 10 seasons; if mean < 20, trigger Phase 4 MG-5 calibration review per § 6.9.

### 6.11 Implementation may PROCEED upon Matt-gate ratification with amendments

PM-1 may PROCEED with amendments § 6.1-§ 6.10 to the math note. The GMM-as-primary commitment is substantive; recommend jack-ryan Gate-1 re-review of the amended math-note before Dispatch 3B fires.

---

## 7. § 6 — Cross-cutting findings across the bundle

### 7.1 The 5D quality-vector is the load-bearing methodological assumption across all four Phase 4 gates

All of MG-1 / MG-2 / MG-3 / MG-4 operate on the same Q(k) = [q1..q5]. The dimensionality choice (5) is at the boundary of where:
- Pareto front sizes start growing toward "everything is non-dominated" (handled by MG-1; not yet at the bad regime)
- Crowding distance boundary-assignment starts dominating (handled by MG-2 § 4.3 + my k≥10 amendment)
- Mahalanobis covariance estimation becomes ill-conditioned (handled by MG-3 Tikhonov)
- KDE-based KL becomes statistically meaningless (the reason MG-4 must shift to JSD)

**Cross-cutting recommendation:** after first smoke run (Dispatch 3A), perform a covariance audit on Q(k) distributions across cells:
- Per-cell sample covariance + condition number profile
- Per-objective marginal distribution shape (Shapiro-Wilk normality)
- Pairwise objective correlation matrix

This single audit informs (i) MG-1 fallback-to-lower-d trigger; (ii) MG-2 HVC upgrade trigger; (iii) MG-3 density-fallback trigger; (iv) MG-4 bandwidth tuning. **One audit serves four gates; should be a named deliverable in Dispatch 3A smoke-test specification.**

### 7.2 Shared cell-fetch + shared per-cell Σ computation

MG-2 § 5 documents shared Archive_c fetch across MG-1/2/3/4 (single DB round-trip per kit insertion). **Extend this to also compute Σ_c once at Phase 4 entry per cell** — MG-3 needs Σ for Mahalanobis; the same Σ informs MG-4 (covariance shape informs KDE bandwidth adaptation) AND a future P5 cohesion-judge calibration loop (knowing per-cell distributional shape of quality vectors informs cohesion-judge prompt construction at star-lord seam).

Implementation: at Phase 4 pipeline entry per cell, materialize a `CellContext` object: `{Archive_c, Σ_c (Tikhonov-regularized), Q_mean_c, sorted_per_dim}`. Pass through MG-1 → MG-2 → MG-3 → MG-4 as shared input. Computational savings are modest (covariance fit is O(k × d²) ≈ 100 × 25 = 2,500 ops per cell), but the architectural cleanliness pays off in maintenance — covariance shape is the load-bearing per-cell statistic for multiple downstream uses.

### 7.3 PM-1 cohort-size at edge of viability — recommend Phase-4-calibration-feedback as load-bearing architectural concern

The ~28-32 cohort assumption is fragile. If Phase 4 acceptance rates are different than Path-1 § 0 anticipated (likely; this is a first-implementation regime), cohort sizes will vary. PM-1 § 5.2 sparsity branches absorb the variance, but the absorption REDUCES the design surface (fewer factions; degraded clustering). The feedback loop § 6.9 is currently in PM-1's math note as a Pattern-A consultation question — recommend promoting it to an architectural commitment in either PM-1 or MG-5 (or a new cross-cutting "Phase-4-PM-1 calibration loop" math note).

This is a recommendation that COULD be deferred to post-first-smoke — let empirical data inform the loop's tuning. But the EXISTENCE of the loop should be architecturally committed now, not deferred.

### 7.4 Discipline #25 (rep-audit) compositional reminder

PM-1's output is geometry-layer (cluster assignments + soft-membership probabilities). PM-2 consumes at semantic-layer (faction labels). Per Discipline #25, rep-audit is non-negotiable at PM-2's consumption. **My recommendation:** PM-2 should NOT emit faction labels for any cluster whose top-5 modal reps don't substantively match the label semantic. If rep-audit fails, the cluster receives a generic placeholder label (e.g., "Emergent Faction Cluster-3") AND surfaces to gandalf design call for inspection.

The cluster-116 precedent (per gandalf OP § 4.4 first-canonical-example) is directly applicable here: substrate vote at geometry level is binding; semantic-label inheritance requires rep-audit at firing. PM-2 implementation should bake this in structurally, not as a downstream check.

### 7.5 Discipline #46 per-cell bounding compliance — VERIFIED across all five notes

All four MG notes (MG-1/2/3/4) operate per BC cell, bounded ≤ 100 kits per cell. PM-1 operates per season, bounded ~28-32 kits per cohort. No global cross-cell or cross-season O(n²) operations. Kernel-panic risk: NONE.

The architectural commitment to per-cell bounding is the foundational protection that makes all the other algorithmic choices tractable. Worth highlighting because it's easy to lose during implementation (e.g., a "let's just compute global Pareto rank for archive analytics" instinct could undo the bound). Recommend Gate-2 grep audit for unbounded `fetchall()` or cross-cell joins at implementation review.

### 7.6 Substrate-led discipline preserved across all five recommendations

None of my recommendations introduce pre-imposed taxonomy or pre-authored weighting that violates substrate-led emergence:
- MG-1: substrate votes Pareto front (no scalarization)
- MG-2: substrate votes diversity via empirical crowding
- MG-3: substrate calibrates duplicate-detection threshold empirically (Discipline #11)
- MG-4: substrate votes novelty via JSD on its own KDE
- PM-1: substrate (kit cohort) votes faction identity; aesthetic-heavy weighting is design LENS not pre-authored faction taxonomy (Discipline #41 preserved); PM-2 rep-audit ensures semantic-label compliance with substrate reps (Discipline #25)

All five Pattern-A consultations compose cleanly with the substrate-led discipline anchor (Discipline #41 + the no-classes architectural recommitment).

---

## 8. Disposition summary table (for knight-rider routing)

| Note | Recommendation type | Implementation gating | jack-ryan Gate-1 re-review needed? |
|---|---|---|---|
| MG-1 | PROCEED as authored | None additional | NO |
| MG-2 | PROCEED + MIN_POPULATION_FOR_DIVERSITY 6→10 amendment | None additional | NO (minor amendment) |
| **MG-3** | **PROCEED with PHASED METHODOLOGY: Gaussian Mahalanobis + Tikhonov (λ=1e-3) + Pareto-strict replacement + empirical threshold calibration; density-based fallback as standby module** | **G-MG3-1 through G-MG3-4 gates baked into Dispatch 3A smoke spec** | **YES — substantive amendments warrant re-review** |
| MG-4 | PROCEED with REFRAMING: JSD across full range; retire grid-KL path; Silverman+floor bandwidth | None additional | YES — substantive reframing warrants re-review |
| PM-1 | PROCEED with: GMM A4 primary (k=3..4 BIC-selected); k-means A1 fallback at n<20; Option β confirmed; aesthetic-heavy weighting; PCA-whitening; revised sparsity thresholds; Phase-4-feedback loop architecturally committed | G-PM1-1 through G-PM1-4 gates baked into Dispatch 3B smoke spec | YES — algorithm commit warrants re-review |

**Cross-cutting amendments warranting consideration:**
- Cross-cutting "post-first-smoke covariance audit" deliverable (§ 7.1) added to Dispatch 3A smoke spec
- Shared `CellContext` materialization at Phase 4 pipeline entry (§ 7.2) added to Dispatch 3A architectural design
- PM-1 ↔ MG-5 feedback loop architecturally committed (§ 6.9, § 7.3) — recommend new math-note OR amendment to PM-1 § 5.4 OR amendment to MG-5

---

## 9. Anti-stall surfacing — none

Per dispatch anti-stall discipline: per-consultation batching; if any consultation surfaces blocking methodology question requiring Pattern B Matt dialogue, STOP and surface to KR.

**No blocking methodology questions surfaced.** The MG-3 Gaussian-vs-density question is resolved by the phased methodology approach (§ 4.1) without requiring Matt dialogue — empirical gate at smoke-test, fallback algorithm fully specified. All five consultations can return decisive recommendations.

---

## 10. Discipline citations

- **Discipline #1 (math-before-code):** this consultation specifies methodology + math, not code. Per-recommendation rationale is grounded in statistical literature + analogical reasoning from substrate-scale precedents. Code implementation gates on Matt-gate ratification of the math-note bundle (with my amendments incorporated) + Dispatch 3A/3B firing.
- **Discipline #11 (empirical-inspection):** cited at § 4.3 (MG-3 threshold empirically calibrated, not parametrically derived); § 4.7 (G-MG3-2 covariance audit at smoke); § 5.7 (G-MG4-1 JSD score distribution sensitivity); § 6.7 (PM-1 stability protocol); § 7.1 (post-first-smoke covariance audit as load-bearing). Recommendations defer to empirical evidence at multiple gates rather than committing to single-point pre-empirical claims.
- **Discipline #18 (methodology-before-execution):** this IS the methodology consultation that gates implementation per the dispatch authoring. The LOAD-BEARING MG-3 consultation specifically composes with the gandalf OP § 4.2 extension-hotspot refinement — consultation fired at ratification routing time after Gate-1 PASS, with empirical evidence from prior baseline work informing the consultation. Returns phased methodology with empirical gate; substrate-led discipline preserved.
- **Discipline #25 (semantic-layer rep-audit):** § 7.4 + § 6.10 G-PM1-3. PM-1 cluster geometry is binding at geometry layer; PM-2 semantic-label assignment requires rep-audit at firing. The cluster-116 precedent (gandalf OP § 4.4) is directly analogous and informs the recommendation.
- **Discipline #40 (canonical decision NOT scaffold):** all five recommendations are committed methodology choices, not scaffold-with-pending-decision. Where empirical gates exist (smoke-test branches), they are named, threshold-operationalized, and have fully-specified fallback algorithms — meeting the Discipline #40 "canonical decision with explicit empirical refinement criterion" pattern.
- **Discipline #41 (pre-authored taxonomy interrogation):** § 7.6 — no recommendation introduces pre-imposed taxonomy. Aesthetic-heavy weighting (PM-1) is design LENS that biases attention; substrate (kit cohort) votes faction identity. Pareto + crowding + novelty all preserve substrate-vote framing.
- **Discipline #42 (framing-audit):** Q1/Q2/Q3 applied at § 0. Framing holds with embedded amendments.
- **Discipline #46 (per-cell bounding + DB anti-materialization):** § 7.5 — verified across all five recommendations. Per-cell or per-cohort scope maintained; no global O(n²) operations introduced. The shared `CellContext` proposal (§ 7.2) consolidates the per-cell-fetch optimization across all four Phase 4 gates.

---

## 11. Cross-references

### Consultation anchors
- `agentic_orchestration/dispatches/2026-05-27-phase-4-5-math-notes-bundle.md` — parent dispatch
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` — Path 1 scope expansion (§ 3.1 + § 3.2 specs)
- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 7 — per-cell bounding LOAD-BEARING

### Math notes consulted
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-1-pareto-dominance-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-2-crowding-hypervolume-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-distance-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-4-kl-information-gain-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-1-multimodal-clustering-math-2026-05-27.md`

### Composition context
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-substrate-clustering-math-2026-05-27.md` — Note 1 substrate clustering (Option β composition question)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — BC axes empirical foundation
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` § 2.2 — Variant C faction-coalescence canonical
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` — Discipline #41 retroactive application

### Disciplines authoritative source
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 + #11 + #18 + #25 + #40 + #41 + #42 + #46

### Skill anchors
- `.claude/skills/reincarnated-elrond-operating-procedure` § 3.4 — math-hotspot routing; P2 + P3 are primary elrond hotspots
- `.claude/skills/reincarnated-substrate-vector-cheatsheet` § 7.1 — P3 multimodal clustering math-hotspot
- `.claude/skills/reincarnated-engineering-disciplines` — discipline reference wrapper
- `.claude/skills/reincarnated-hive-mind-protocol` § 4 (decision routing) + § 7 (math hotspots) + § 5.5 (sub-agent verdict pattern)

### Statistical literature anchors (informal references; not formal citations)
- Beume, Naujoks, Emmerich 2007 — SMS-EMOA hypervolume contribution
- Bonneel et al. 2015 — Sliced Wasserstein distances
- Bringmann + Friedrich 2010 — crowding distance vs hypervolume empirical comparison
- Chan, Golub, Leveque 1983 — Welford's algorithm numerical stability
- Deb et al. 2002 — NSGA-II
- Deb + Jain 2014 — NSGA-III reference-point selection
- Hardle + Simar 2007 — Applied Multivariate Statistical Analysis textbook (sample covariance rule of thumb)
- Hotelling 1931 — Hotelling's T² distribution
- Janmohamed et al. 2023 — MOQD multi-objective quality-diversity
- Laumanns et al. 2002 — ε-dominance
- Ledoit + Wolf 2004 — Shrinkage estimation of covariance
- Lin 1991 — Jensen-Shannon divergence
- Mahalanobis 1936 — Mahalanobis distance original
- Mardia, Kent, Bibby 1979 — Multivariate Analysis textbook
- Mouret + Clune 2015 — MAP-Elites original
- Pierrot et al. 2022 — MOME multi-objective MAP-Elites
- Silverman 1986 — Density Estimation textbook (Silverman's rule)

---

## 12. Sign-off

**Author:** elrond (data steward + archivist; P3 multimodal clustering math-hotspot owner per Pattern-A methodology authority per `substrate-vector-cheatsheet` § 7.1)

**Status:** Methodology consultation COMPLETE. All five consultations return PROCEED dispositions; MG-3 LOAD-BEARING returns phased-methodology commit; MG-2, MG-4, PM-1 amendments recommended for jack-ryan Gate-1 re-review before respective implementation dispatches (3A for Phase 4; 3B for Phase 5).

**For:** the bundled methodology consultation response on Phase 4 math gates (MG-1 Pareto / MG-2 Crowding / MG-3 Mahalanobis LOAD-BEARING / MG-4 KL) and Phase 5 PM-1 multimodal clustering, per Path (1) Cycle 14 scope expansion. Returns: § 1 MG-1 strict Pareto PROCEED + reject ε-dominance; § 2 MG-2 NSGA-II crowding distance PROCEED + raise MIN_POPULATION threshold; § 3 MG-3 phased methodology PROCEED (Gaussian Mahalanobis + Tikhonov regularization λ=1e-3 + empirical threshold calibration + Pareto-strict replacement + density-based fallback as standby module per smoke-test branch); § 4 MG-4 JSD-as-primary PROCEED (retire grid-KL path; Silverman+floor bandwidth); § 5 PM-1 GMM A4 primary PROCEED (k=3..4 BIC-selected + k-means A1 fallback at n<20 + Option β distinct from Note 1 HDBSCAN + aesthetic-heavy weighting + PCA-whitening + revised sparsity thresholds + Phase-4-feedback loop architecturally committed); § 6 cross-cutting findings (5D quality-vector load-bearing assumption + shared CellContext materialization + PM-1 cohort-size edge-of-viability + Discipline #25 rep-audit reminder + Discipline #46 verified + substrate-led discipline preserved). Implementation gating: MG-1 may PROCEED; MG-2 PROCEED with minor amendment; MG-3 PROCEED with substantive amendments warranting re-review; MG-4 PROCEED with substantive reframing warranting re-review; PM-1 PROCEED with substantive algorithm commit warranting re-review. Anti-stall: no blocking methodology questions surfaced. Returns to knight-rider for ratification routing.

**Signed:** elrond (data steward + archivist)
