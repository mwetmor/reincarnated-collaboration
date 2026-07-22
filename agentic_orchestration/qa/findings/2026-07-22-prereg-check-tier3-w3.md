# Finding — 2026-07-22 — Tier-3 W3 Pre-Registration Check (T3-F4 gate instrument)

**Reviewer:** jack-ryan (DESIGN-MODE, chartered PRE-REGISTRATION CHECK gating W3)
**Verdict:** **PASS-WITH-CONCERNS**
**Target:** prereg `2026-07-22-tier3-w3-prereg.md` (L-14), empirical input `2026-07-22-tier3-prereg-baselines.{md,json}`
**Author under check:** gandalf `RUN-CONDUCTOR` (SPEC-AUTHOR beat)
**Charter predicate:** v1.2 §4 PREREG row ("prereg doc pinned pre-results") + W3 row
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate), #4 (decisions/rulings-log as truth), #5 (severity matters); Disciplines #1, #2, #18; run rulings L-3, L-13, L-14
**Concerns:** C1 (WARN), C2 (WARN), C3 (INFO), C4 (INFO), C5 (INFO)

---

## Verdict rationale

The instrument is sound, decidable, and substantially un-gameable. Every load-bearing number in the sheet was re-derived first-hand against the source JSON and is exact (see per-dimension detail). X and Y stand on genuinely separate evidential legs — L-3 is discharged. The proxy-cancellation argument is valid. No concern rises to FAIL: none of them can flip a gate leg or open a post-hoc degree of freedom that survives the round-robin + argmax/argmin determinism. Two WARNs (C1, C2) obligate a one-line pin each BEFORE freeze; three INFOs record limits that travel into the W3 result read, not the freeze. The conductor amends; I re-verify the two WARN pins at freeze.

---

## (a) L-3 DISCHARGE — Y's basis independent of X's data · binomial arithmetic

**Finding: DISCHARGED (with one INFO).** Y's basis (§4) rejects the null via P(≥24 correct of 32 | p=0.5). I re-computed it: `sum(C(32,k)·0.5^32 for k in 24..32) = 0.003500` — matches "≈0.0035" exactly. `0.75×32 = 24` exact. The basis uses only (i) per-pair null probability p=0.5 and (ii) pooled sample size 32. It touches **none** of the Part-2 between-cell variance numbers that set X (§3). The two thresholds are computed from disjoint inputs — X from `pool_metric_variance_decomposition`, Y from binomial structure. This is the exact separation L-3 demanded. **L-3 obligation satisfied.**

→ **C3 (INFO):** the per-pair null p=0.5 is only *exactly* 0.5 if the ≥2-of-3-metric sign rule (§4) behaves like a fair coin under H0. The three primary metrics are positively correlated (§5 states this and defends ≥2-of-3 as a robustness device, not an independence claim). Positive correlation makes the ≥2-of-3 event *more* deterministic per pair, which under H0 pushes the realized per-pair p toward 0/1 rather than 0.5 — i.e. the true pooled null is somewhat *wider*-tailed than pure Binomial(32, 0.5), so 0.0035 is a **lower bound on significance strength / an approximation, not an exact α.** This does not break L-3 (the leg is still structural and X-independent) and does not weaken the gate direction (correlation cannot manufacture sign-correctness where geometry carries no signal). It should be recorded as the honest characterization of the 0.0035 figure. Verified at: W3 result read (the conductor's DRIFT-CRITIC pass), not at freeze.

## (b) X HONESTY — between-cell anchor vs understated floor · magnitude meaningfulness

**Finding: DEFENSIBLE.** The report's own caveat (baselines report L-145..151; JSON `prereg_caveat`) declares the within-seed floor an **understated lower bound** because cell-sharing hides per-kit shape noise. Anchoring X to the between-cell spread rather than that floor is the conservative reading of that caveat — it refuses to buy a tight threshold on a noise estimate the report itself flags as too small. I verified the margin: `0.5×12.82 / 0.073 = 87.8×` above the reported mobs_killed floor (prereg claims "~88×"); even at a 10× floor understatement the margin is still `8.8×` — an order of magnitude survives. X=0.5 standardized is a Cohen-medium effect; in raw units `0.5×12.82=6.41` mobs/aoe and `0.5×6370=3185` damage — all match §3. These are non-trivial magnitudes against a pool that spans [0,40] and [0,19575]. **X is honestly anchored and meaningful.**

Nuance (not a concern): X standardizes by the between-cell sd, which is also the scale on which encounter deltas will land. This is a *fixed denominator declared pre-results*, not a quantity fit to the outcome — so it introduces no circularity; it is the correct Cohen-d construction.

## (c) PROXY-CANCELLATION ARGUMENT — soundness + limits

**Finding: SOUND.** The gate observation is `Δ_m = m(encounter) − m̄(kit baseline)` with the **identical** BC→cell→PlayerClass fighter, seed set {20260722–25}, and dmod=1.0 on both sides (§2). The fighter's contribution to the mean enters both terms and cancels in the difference; the only manipulated variable is encounter geometry. The stated limit is correct: the 16-cell proxy caps *between-kit* resolution, which §5 selection does **not** require (selection is within-era argmax/argmin on fit_score, and the gate measures *within-kit* contrast). The finer per-corpus-kit baseline is correctly held as a rocket-seam flag, not a W3 dependency. This matches L-14(e) and the report's honest-limitation block (report L-98..106).

→ **C4 (INFO):** cancellation is clean for the **mean shift** (numerator of d). The **denominator** `sd_pool(m)` is still cell-resolved, so it inherits the understated-floor caveat — but (b) already neutralizes this by anchoring to the *between-cell* sd rather than the within-seed floor, giving the order-of-magnitude margin. The two caveats interlock correctly: numerator cancels the fighter, denominator is deliberately the conservative (larger) spread. This interlock is the reason the proxy is admissible; recording it makes the argument's completeness explicit. No action; documents the mechanism.

## (d) SAMPLE RULE — decidable · un-gameable · residual DoF

**Finding: DECIDABLE, two small residual degrees of freedom.** Un-gameable core confirmed: candidate pool is `scoring_basis=full` only (§5.1, era_only's flat 0.5-band declared ineligible — I confirmed the split is {full 524, era_only 544} in the JSON lineage); high=argmax, low=argmin (deterministic given the frozen fit_score); family round-robin caps the TOTEM/TRAP skew structurally (I confirmed per-era skew II 0.49 / IV 0.48 / III 0.40 / I 0.33 against the JSON `totem_trap_fraction`); courts≥3 with a defined swap; `membership_tier` recorded per pair. Pair arithmetic is internally consistent: 4 high × 4 eras = 16, 4 low × 4 eras = 16, total 32 → 128 fights.

Two residual DoFs that could be exploited post-hoc **in principle** (both small; both closable by one clause):
1. **Multi-family draft key.** L-13 flagged 12 multi-family kits (the 131-vs-132 distinct-count correction). The round-robin drafts on the family *working label* — but the prereg does not state which family a multi-family kit counts as when it is drafted. An unspecified tiebreak here is a lever on *which* kit fills a slot.
2. **"Least-extreme" swap tiebreak.** §5.4's courts-swap replaces "the least-extreme pick" — undefined if two candidate picks tie on |fit_score − band-center| (or on rank distance from the argmax/argmin frontier). A tie with no rule is a choice left to the executor after seeing candidates.

→ **C1 (WARN):** pin both keys before freeze — (1) the multi-family draft-key rule (e.g. "the kit's *active* sidecar row governs its draft family, precedence RATIFIED > PROPAGATED > DOCKET per L-13"), and (2) the swap tiebreak (e.g. "on |fit| tie, take the lower `kit_id`"). Neither changes the instrument's power; both remove executor discretion so the sample is reproducible from the sheet alone. Verified at: freeze (I re-read §5 for the two clauses).

## (e) GATE VERDICT LOGIC — three legs decidable · no-partial-pass airtight

**Finding: FULLY DECIDABLE.** All three legs (§6) compute from data with no interpretive slack: (1) showcase median composite d over 16 high pairs ≥ +0.5; (2) stress median over 16 low ≤ −0.5; (3) direction ≥75% of 32 sign-correct per the §4 ≥2-of-3 rule. "Composite = median of the 3 per-metric d's per pair" and "median over 16 pairs" are standard order statistics (16 even → mean of 8th/9th; unambiguous). The no-partial-pass clause is airtight: "A partial result (e.g. 2 of 3 legs) is a FAIL with the same routing — no post-hoc leg-dropping" (§6). PASS ⇒ RD-1; FAIL ⇒ honorable fallback routing to W4 + lane queues. The verdict is a pure conjunction of three data-decidable predicates. **No slack.**

→ **C5 (INFO):** §6 gates *both* the effect-size legs (showcase/stress) *and* the direction leg on the same primary triple. The showcase/stress legs use the *magnitude* of the composite d; the direction leg uses the *sign* via ≥2-of-3. These are not independent tests of the hypothesis (same metrics, same pairs) — a genuine geometric signal should satisfy all three together, and a null should fail the magnitude legs even if direction squeaks by, so the conjunction is *conservative* (harder to pass), which is the right failure-safe posture. Recording that the three legs are correlated-by-construction (not three independent confirmations) keeps the PASS claim honest in the review book. No action.

## (f) FREEZE DISCIPLINE — adjust-once declined · invariants · unpinned load-bearing item

**Finding: DISCIPLINED, one load-bearing pin missing.** The L-13(a) adjust-once right is **declined with recorded, auditable reasoning** (§1): the 6.1× variance expansion came from family resolution feeding verb+topology, not a weight defect, and the shelf near-degeneracy is a within-era no-op (a near-constant term cannot reorder an argmax/argmin deck). I concur — this reasoning is sound and the decline spends nothing decision-relevant. Instrument invariants are hard and correctly enumerated: seeds {20260722–25}, dmod=1.0 uniform, mob-parity 40 (with red-flag-don't-normalize on a builder that can't hold 40), HEAD stamped + re-verified against `simulation/spatial_gauntlet/` + `generation/` on any mid-W3 move. I verified engine HEAD is `a3671d4` right now — matching both the prereg §0 stamp and the baselines report's declared run-HEAD.

→ **C2 (WARN):** the prereg pins the HEAD-move *procedure* ("re-verified against the subtrees before continuing") but does not pin the **invariant it protects**: the fighter is only identical on both sides of Δ (dimension (c)) if the HEAD W3 runs the encounters at shares `simulation/spatial_gauntlet/` **and** `generation/` byte-state with the baseline HEAD `a3671d4`. If a mid-W3 HEAD move touched either subtree, the proxy-cancellation argument breaks (different fighter behind baseline vs encounter) and Δ is no longer a clean geometry contrast. State it as a hard invariant, not just a check: *"W3 encounters run at a HEAD whose `spatial_gauntlet/` + `generation/` are byte-identical to baseline HEAD `a3671d4`; a subtree delta in either is a red-flag halt, not a continue."* This is the pin most load-bearing to the gate's validity. Verified at: freeze (I re-read §2/§7 for the invariant statement).

---

## Action

- [ ] **Conductor (C1, WARN):** add two clauses to §5 — multi-family draft-key rule + "least-extreme" swap tiebreak. Removes executor discretion; sample reproducible from sheet alone.
- [ ] **Conductor (C2, WARN):** promote the HEAD-subtree check from procedure to hard invariant in §2/§7 — W3 encounter HEAD must share `spatial_gauntlet/` + `generation/` byte-state with baseline `a3671d4`; subtree delta = red-flag halt. Protects proxy-cancellation.
- [ ] **Conductor (C3/C4/C5, INFO):** carry the three characterizations into the W3 result read / review book — (C3) 0.0035 is an approximate lower bound under metric correlation; (C4) numerator-cancels / denominator-conservative interlock is why the proxy is admissible; (C5) the three legs are correlated-by-construction, hence a conservative conjunction, not three independent confirmations. No pre-freeze action.
- [ ] **jack-ryan:** re-verify the two WARN pins (C1, C2) at the freeze beat; on both present, verdict converts to clean PASS and the sheet freezes verbatim. No re-review of the INFO items.

## References

- `agentic_orchestration/gandalf/notes/2026-07-22-tier3-w3-prereg.md` (instrument under check, L-14) — §1 weights-freeze, §2 delta+proxy, §3 X, §4 Y, §5 sample rule, §6 gate, §7 freeze
- `agentic_orchestration/gamora/notes/2026-07-22-tier3-prereg-baselines-report.md` — L-98..106 honest limitation, L-123..138 S/N table, L-145..151 noise-floor caveat, L-154..173 per-era feasibility + skew
- `agentic_orchestration/gamora/notes/2026-07-22-tier3-prereg-baselines.json` — `pool_metric_variance_decomposition` (sds re-derived first-hand), `per_era_baselines` (feasibility n + courts + skew), `prereg_caveat`
- `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-state.md` — L-3, L-13, L-14
- `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` v1.2 — §4 PREREG + W3 done-predicates, §8 preregistration safety
- engine HEAD `a3671d4` (verified current; matches prereg §0 stamp)
