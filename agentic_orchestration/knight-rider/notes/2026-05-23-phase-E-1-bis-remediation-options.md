# Phase E-1-bis remediation options — knight-rider option-set for design-fit review

**Author:** knight-rider
**Date:** 2026-05-23
**For:** gandalf (Pattern-A design-fit assessment) → Matt decision
**Status:** Pre-decision option-set; no commitment made

---

## Situation

Phase E-1 full-mode partial-fire (terminated mid-Deliverable-3 ~03:29 EDT). Deliverables 1 & 2 produced real full-data PCA output; Deliverable 3 (HDBSCAN) never finished writing. The empirical PCA result on N=16,699:

- **k_final = 4** (driven by clamp `min(kink_idx+2, 12) = min(2+2, 12) = 4`; floor of 8 overridden)
- **Cumulative variance at k=4: 20.59%**
- **Only Axis 1 (register: historical-vs-fantasy) bootstrap-stable** at cosine-dist 0.0258
- **Axes 2–4 bootstrap-unstable** at 0.35 / 0.64 / 0.73 (threshold ≤ 0.10)

Cross-validates against the smoke (N=100) result. The crash-triage handoff's "smoke artifact" hypothesis is refuted. This is a real Phase E-1-bis case — the substrate does not have the canonical 8–12-axis structure the dispatch acceptance criteria assumed.

Root-cause hypothesis (knight-rider, not validated): substrate is too monocultural (`fantasy_generic` = 94.46%) for F2 inverse-frequency weighting to rescue rare lineages, because the smallest lineages have 1–5 rows each and F2 amplification (up to 1518×) is amplifying within-row noise rather than revealing lineage structure.

## What survived

- **Axis 1 (register).** Robust separator: `register_historical +0.39 / register_fantasy −0.39 / period_fictional −0.37 / kind_category +0.36 / kind_named_template −0.36`. This is a real, interpretable, repeatable axis.
- **Pipeline plumbing.** End-to-end correctness validated by smoke; full-mode reproduced the same shape.
- **F2 weight calibration.** Math correct, just under-powered for the small-N rare lineages.

## What didn't

- 8–12 stable axes (got 1)
- Cumulative variance for top-k worth differentiating on (got 20.59% at k=4)
- Deliverable 3 cluster output (script killed mid-fit; clusters.md still stale smoke content from 03:06)

## Remediation option families

Ordered cheapest → most disruptive. Each marked with knight-rider lean and critique-pair requirement.

### Family A — Accept-and-reframe

**A1. Treat "1 robust axis + N emergent clusters" as the actual answer.** The substrate has one canonical axis (register) plus cluster structure. Re-frame Phase E from "discover 8–12 axes" to "anchor on register + cluster freely." Phase E-2 gandalf labels the one axis + the clusters; Phase E-4 elrond uses cluster_id as primary discriminator.

- **Cost:** lowest. Re-run only the clustering step on a sensible feature space.
- **Risk:** none methodologically — honors what the data says.
- **Critique pair:** YES (jack-ryan for F5-bis disposition: "answer found, not method failed"; gandalf for design-satisfiability with 1 axis).
- **Knight-rider lean:** STRONG. Possibly THE answer.

### Family B — Stay within F5 (PCA-primary); tweak inputs

**B1. Cap F2 weighting.** `w_i = sqrt(1/max(freq, 0.01))`. Cap upweight at 100× instead of 1518×.

- **Cost:** one config line; ~30s re-run.
- **Risk:** less aggressive rare-lineage rescue.
- **Critique pair:** light — F2 parameter change, not lock break.
- **Knight-rider lean:** MEDIUM — try as 10-min spike before committing to A1.

**B2. Drop F2 entirely.** Un-weighted PCA. Reflects `fantasy_generic` internal structure honestly.

- **Cost:** one flag; ~30s re-run.
- **Risk:** rare lineages disappear from axis space; loses original rescue intent.
- **Critique pair:** YES — breaks F2 lock language.
- **Knight-rider lean:** LOW unless A1 + B1 fail.

**B3. Drop LSA text features; use only structured 60-d.** Hypothesis: text adds noise; canonical structure lives in lineage/period/register/kind/wield/type one-hots.

- **Cost:** one flag; faster re-run.
- **Risk:** discards information that might distinguish weapon families within the same structured tags.
- **Critique pair:** light.
- **Knight-rider lean:** LOW — text features cost nothing to keep; ablation should be evidence-driven not speculative.

**B4. Stratified sub-sample `fantasy_generic`.** Downsample from 15,774 → ~3,000–5,000 to rebalance. Re-run PCA on the balanced subset.

- **Cost:** medium. Adds sampling step.
- **Risk:** under-samples dominant culture's internal variance; fantasy_generic clusters in E-3 coarser.
- **Critique pair:** YES — substrate framing change.
- **Knight-rider lean:** MEDIUM — interesting but adds sample-frame discipline tax.

### Family C — Break F5 explicitly; replace PCA

**C1. NMF (non-negative matrix factorization).** Well-suited to TF-IDF + non-negative one-hot features. Additive "topic" components rather than orthogonal axes; components stay interpretable.

- **Cost:** medium. New algorithm, new bootstrap-stability protocol, updated plumbing.
- **Risk:** components aren't orthogonal — overlap can muddy gandalf labeling.
- **Critique pair:** YES — full F5 lock revisit; pattern-B Gate-1 dispatch warranted.
- **Knight-rider lean:** RESERVE — hold for if A1 + B1 both fail.

**C2. Mixed-effects PCA with explicit lineage stratification.** Decompose: global mean + per-lineage offset + residual. PCA on residual. Separates "what's universal" from "what's lineage-specific."

- **Cost:** high. Significant new implementation.
- **Risk:** experimental.
- **Critique pair:** YES — full pattern-B Gate-1.
- **Knight-rider lean:** RESERVE — exotic; only if simpler paths exhausted.

### Family D — Skip axis discovery; jump straight to clusters

**D1. HDBSCAN directly on the 160-d (or 60-d structured-only) feature matrix.** Skip Deliverable 2 entirely. Cluster on the original features; gandalf interprets cluster centroids in E-2 rather than labeling axes.

- **Cost:** low — pipeline already implements this; just bypass the PCA-projection input.
- **Risk:** curse-of-dimensionality in 160-d (less severe in 60-d). But categorical structure is strong.
- **Critique pair:** YES — re-frames Phase E rationale (sold E-1 on "axes + clusters"; strips axes).
- **Knight-rider lean:** MEDIUM — overlaps with A1 in practice (A1 keeps Axis 1 as anchor; D1 abandons axes entirely).

## Decision shape

Not all options are mutually exclusive. Likely sequence under any disposition:

1. **B1 spike** (cheap; ~10 min) — test whether capped F2 stabilizes axes 2–4. If yes, structure is salvageable within F5.
2. **If B1 doesn't move the bootstrap stability into PASS for axes 2–4:** commit to A1 (or A1+D1 hybrid: keep Axis 1 as canonical anchor, cluster freely in feature space without trying to extract further axes).
3. **C1 (NMF)** held in reserve as legitimate F5 lock-revisit if A1 + B1 are both unsatisfying after gandalf review of cluster output.

## What knight-rider is asking gandalf for

Specifically:

1. **Design-intent fidelity.** Which of A1 / B1–B4 / C1–C2 / D1 honor the design intent of Phase E (per your variant-cluster-policy + hive-mind-protocol-weapon-library-import authoring)? Which damage it?
2. **Goal of the exercise.** What was Phase E *for* in your conception — is the goal "structure discovery so we know what we have" (in which case A1 fully satisfies — we discovered the structure, it's 1 axis + clusters) or "produce a multi-axis basis the engine can use as differentiating features" (in which case A1 is undersized and we need B1/C1)?
3. **Acceptable axis count.** Is 1 canonical axis (register) sufficient for downstream Phase E-4 substrate-density precomputation + variant-cluster policy? Or does Phase E-4 functionally require ≥ N axes for some N?
4. **F5 lock posture.** From your design-side seat, is the F5 PCA-primary lock load-bearing on design grounds (and should be defended), or is it a methodology preference that can be relaxed if the data demands it?
5. **Recommendation.** Your ranked preference among the seven options (A1, B1, B2, B3, B4, C1, C2, D1), with reasoning anchored on the design-side canonical docs you've authored.

Knight-rider explicitly NOT asking for technical / process critique — that's jack-ryan's lane and will follow gandalf's verdict if the path chosen requires F5 lock-revisit.

---

**Files for gandalf's read-set:**

1. `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-discovery.md` — empirical result (Deliverable 2)
2. `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-features.md` — feature space + F2 weight calibration
3. `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-pattern-6-axis-discovery.md` — original dispatch (acceptance criteria, F-locks)
4. `agentic_orchestration/skill_handoff_2026-05-23-phase-E-1-crash-triage.md` — crash-triage handoff (with caveat that its "smoke artifact" conclusion is now refuted by full-data result)
5. This file — the option-set being assessed.

Gandalf's own canonical authoring (variant-cluster-policy, hive-mind-protocol-weapon-library-import, downstream-delivery-strategy) is the design-side anchor — gandalf knows where to find it.

**Expected output:** design-fit verdict per option + ranked recommendation + any options gandalf surfaces that knight-rider didn't list. File to `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md` or returned inline; gandalf's call.
