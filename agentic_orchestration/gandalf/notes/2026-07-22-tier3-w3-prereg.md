# Tier-3 W3 Pre-Registration — T3-F4 Gate Instrument (FROZEN on jack-ryan check)

**Author:** gandalf `RUN-CONDUCTOR` (SPEC-AUTHOR beat), 2026-07-22 — ruling **L-14**.
**Status:** DRAFT → freezes on jack-ryan prereg check (charter §4 PREREG row). After freeze, NO parameter on this sheet changes through W3; a violated invariant is a red-flag, not a silent adjust.
**Empirical inputs (verified by conductor):** gamora PREREG report `agentic_orchestration/gamora/notes/2026-07-22-tier3-prereg-baselines-report.md` + `…-prereg-baselines.json` (131 per-kit baselines, 524 fights, seeds {20260722–25}, dmod=1.0, 0 errors) + `…-w2-fit-output-v2.json` (1068 rows; scoring_basis {full 524, era_only 544} — conductor cross-checked exact; tier×4 arithmetic exact). Substrate: corpus.db md5 `d091881d` + membership sidecar (commit `6dd43161`). Engine HEAD at baselines: `a3671d4` (harness paths unchanged from `b34a14b`; verified delta = export/output/tests only).

---

## §1 — Scoring weights: FROZEN UNCHANGED (adjust-once right DECLINED)

L-13(a) reserved one adjustment against baseline evidence. **Declined; v0 stands:** `fit_score = 0.50·verb + 0.30·topology + 0.20·shelf`.

**Reasoning (recorded so the decline is auditable):** the re-join's 6.1× variance expansion (era_only stdev 0.043 → full 0.265, range [0.1, 1.0]) came from **family resolution feeding the verb+topology terms**, not from any weight defect. The known within-era shelf near-degeneracy is a **no-op for W3**: selection (§5) is *within-era* argmax/argmin, and a near-constant term shifts all candidates in a deck uniformly — it cannot reorder them. Adjusting weights now would spend the un-gameability of the freeze to buy nothing decision-relevant.

## §2 — The delta instrument (what one observation IS)

For a sampled **(kit, encounter)** pair, in each of the 4 shared seeds:
`Δ_m(seed) = m(encounter fight) − m̄(kit's neutral baseline)` per metric m, where m̄ = the kit's 4-seed `open_arena` mean from `…-prereg-baselines.json`.
Per-pair per-metric effect: **`d_m = mean_over_4_seeds(Δ_m) / sd_pool(m)`**, with `sd_pool(m)` = the **between-cell pool stdev** from the baselines JSON (`pool_metric_variance_decomposition`): mobs_killed 12.82 · total_aoe_hits 12.82 · player_damage_total 6370.

**Why the 16-cell fighter proxy does NOT invalidate the gate:** the encounter run uses the *identical* BC→cell→PlayerClass fighter, seed set, and dmod as the kit's baseline. The fighter term **cancels in Δ**; the manipulated variable is encounter geometry alone. The proxy limits *between-kit* resolution (which §5 does not require), not *within-kit contrast* (which the gate measures). The finer per-corpus-kit baseline stays flagged as a rocket-seam task — NOT a W3 dependency.

**Instrument invariants (hard):** same seeds {20260722–25} · dmod=1.0 uniform · mob-count parity **40 total** per encounter (formation shapes geometry, not budget; a builder that cannot hold 40 → red-flag the pair, do not normalize silently) · engine HEAD stamped at W3 fire; any mid-W3 HEAD move re-verified against `simulation/spatial_gauntlet/` + `generation/` before continuing.

## §3 — X (effect-size threshold): **X = 0.5** standardized

Gate magnitude is **d = 0.5** (half the pool's between-cell spread; a Cohen-medium effect). In raw units: ≈ 6.4 mobs_killed / 6.4 aoe_hits / ≈ 3,185 damage — meaty, visible, unfakeable by seed luck.

**Caveat handling (the report's own flag, honored):** the within-seed noise floor (e.g., 0.073 mobs_killed) is an *understated lower bound* (cell-sharing hides per-kit shape noise). X is therefore anchored to the **between-cell spread**, not the noise floor — X=0.5 sits ~88× above the reported floor for mobs_killed, so even a 10× floor understatement leaves an order-of-magnitude margin. An X derived from the floor was rejected for exactly this reason.

## §4 — Y (direction-consistency) — basis stated separately per L-3

**Per-pair correctness:** a pair is *sign-correct* if **≥2 of the 3 primary metrics** (§5's metric subset) have the predicted d-sign (high-fit pairs predict +, low-fit predict −).
**Gate: Y = 75% pooled across all 32 pairs** (per-era consistency reported descriptively, NOT gated — n=8/era is binomially weak alone).

**Y-basis (independent of the baseline variance data, discharging L-3):** under the null (fit carries no geometric signal), sign-correctness is p=0.5 per pair; P(≥24 correct of 32 | p=0.5) ≈ **0.0035**. Y=75% is thus a null-rejection at α<0.005 on the pooled sample. The basis is pure binomial structure + sample size — it does not touch the Part-2 variance numbers that set X, so X and Y stand on separate evidential legs.

## §5 — Sample rule (32 pairs; skew-handled; courts-represented)

**Metric subset (declared):** primary gate triple = `mobs_killed` · `total_aoe_hits` · `player_damage_total` (S/N 176–389). Flanking metrics + `elapsed_s` recorded descriptively; the 12 null-on-this-config fields are out of scope. (Correlation within the triple is acknowledged; the ≥2-of-3 rule is a robustness device, not an independence claim.)

**Selection, per era (×4):**
1. Candidate pool = v2 fit rows for that era with `scoring_basis=full` **only** (era_only rows carry a flat 0.5-band — no selection signal; declared ineligible).
2. **4 HIGH-FIT pairs** = argmax `fit_score` under a **kit-side family round-robin draft**: no family contributes a second kit until every family with ≥1 candidate in that era has contributed one (directly caps the TOTEM/TRAP 44–49% skew; Era II especially).
3. **4 LOW-FIT pairs** = argmin `fit_score`, same round-robin, drafted independently (a kit MAY appear on both sides — specialists legitimately do; record it).
4. **Courts check:** the 8 drafted kits must span **≥3 element-courts**; if violated, swap the least-extreme pick for the next-best candidate from a missing court. (Feasibility verified: all eras carry 5–6 courts at n 20–53.)
5. **Recording per pair:** kit_id · family (working label) · `membership_tier` · fit_score · formation class · court — the resolution-mix travels into the gate record per L-13(c).

**Encounter construction:** each pair's encounter = that kit's argmax (high) / argmin (low) **COMMON-4 formation** (swarm / volley-fan / lane / emplacement) from its era deck — the W2-verified expressible scope. **Strain-4 formations are excluded** (PARTIAL×3 + CANNOT×1 per W2; their requirements live in Lane-2's queue R-1..R-4). Era-deck parameters apply; the era shelf term rides in fit but the arena is era-neutral (geometry is the test, not tuning).

## §6 — Gate verdict (T3-F4), decidable

**PASS requires all three:**
1. **Showcase:** median composite d over the 16 high-fit pairs **≥ +0.5** (composite = median of the 3 per-metric d's per pair);
2. **Stress:** median composite d over the 16 low-fit pairs **≤ −0.5**;
3. **Direction-consistency:** ≥ **75%** of all 32 pairs sign-correct per §4.

**PASS ⇒ RD-1 fires** (conditional leg, T3-V6 — first act-structured run-object as emission-congruent JSON; Lane-1's acceptance fixture). **FAIL ⇒ honorable fallback:** RD-1 does NOT fire; the failure decomposition (which eras/families/metrics missed) routes as findings to the W4 review book + lane queues. A partial result (e.g., 2 of 3 legs) is a FAIL with the same routing — no post-hoc leg-dropping.

## §7 — Freeze + check routing

On jack-ryan prereg check PASS, this sheet freezes verbatim; W3 executes it mechanically (gamora leg: 32 pairs × 4 seeds = 128 fights + census). Conductor judges results as DRIFT-CRITIC against THIS sheet, not against intent recalled later.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22 — L-14, veto-open (T3-V1).
