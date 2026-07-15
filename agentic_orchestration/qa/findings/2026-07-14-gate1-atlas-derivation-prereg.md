# Finding — 2026-07-14 — Gate-1 methodology review of atlas-derivation pre-registration

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1 peer review — pre-registration is binding only if reviewed before results exist)
**Severity:** PASS-WITH-AMENDMENTS (7 amendments; none is a methodological veto — the four-family design is sound)
**Target:** `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` v1
**Charter:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md`
**Author under review:** gandalf (SPEC-AUTHOR)
**Executor:** elrond
**Principles applied:** Review-Principle #1 (math-before-code), #2 (smoke-before-full — here: diagnostics-before-freeze), #4 (decisions-log/register as truth); Discipline #1 (math-before-code), #8 (schema-validation at boundaries), #11 (empirical-over-assumption); ADR-006 (read-only external systems — honored, SELECT-only spot-checks)

---

## What I found

The plan is methodologically strong and, unusually for a first pin, mostly self-defending against post-hoc tuning: the four method families are the right four for 470×13 all-categorical data (MCA/CATPCA is the textbook first choice; Gower→classical MDS is the correct distance-based cross-check for mixed/nominal coordinates; Leiden-CPM and LCA-by-BIC are legitimate independent witnesses); Greenacre over Benzécri is the correct call; MFA block-weighting to defuse cardinality dominance is exactly right; permutation-null dimension retention (not Kaiser) is the disciplined choice; the negatives-as-supplementary and unknowns-as-passive treatments are correct and prevent the corpses from bending the axes they exist to validate. The decision rule ("no tuning-until-pass; one diagnosed amendment cycle; else honorable fallback") is genuinely tight and the fallback is pre-committed, which is what makes the whole instrument credible.

Seven things are under-pinned or threshold-fragile enough that, left as written, they would leave wiggle-room for a failed map to look like a passed one — or would fail a *real* structure on an artifact of small-N. None is a defect in the choice of method; all are defects of specification precision. The most serious three: (1) **the Gate-A labeled subset has no materialized definition** — I verified the DB has no group-label column (`mobile_key_group` is the DEPRECATED mobile-Claude scaffold the register itself bans on line 6; its values are cell-id strings like `DRHFSI-HMDD-SP-PH-~~`, not the six groups), so "the 6-group labeling" is a judgment-laden artifact that must be frozen *before* clustering or Gate A is retro-fittable; (2) **"franchise" is undefined** — the DB has 19 games and no franchise column; a franchise rollup yields 11 (Diablo 160 / PoE 122 … Hades 13), and the two grouping choices give materially different Gate-C R² and Gate-D LOFO behavior; (3) **plane diameter is used as the Gate-D denominator but never defined**, so the ≤10%-displacement gate has an undefined scale.

DB facts I confirmed this session (SELECT-only): `canon_corpus` 524 rows / 38 negatives; `canon_engine_key` 487 rows (470 combat + 17 system), `cell_key` materialized on all 470; passive-category load on the four just-materialized coords (ctrl_function, economy_model, activation_val, dependency_val) = 17/470 each (~3.6%), geometry 24, def_bin 23, delivery 9 — all within the ranges the prereg cites; games distribution severely unequal (poe1 88 → tl1 2). No blocking data-state problem; the snapshot will be analyzable once A.5 lands.

## Rationale

The three headline gaps map to Discipline #8 (schema-validation at boundaries — the Gate-A label and the franchise field are boundary inputs the pipeline consumes but the prereg never binds to a column) and Discipline #11 (empirical-over-assumption — the prereg *assumes* a "6-group labeling" and "~12 franchises" exist as data; they do not, they are constructions). Pre-registration integrity (charter §9 / prereg header) requires that anything a gate consumes be pinned before results exist; a gate whose ground-truth labels or grouping variable are constructed after the analyst has seen embeddings is not pre-registered, regardless of intent. The threshold-fragility items (Gate A silhouette on n=7/n=8 groups; Gate C R² sanity under extreme franchise imbalance; Gate B per-law N) are Review-Principle #1: the math that justifies each threshold must exist before the code runs, and three of the six thresholds currently have no stated power/vacuity check at *this* N.

Two items are genuine statistical hazards at this sample size, not mere wording:
- **Silhouette ≥ 0.2 for AURA (n=8) and MINION/PET (n=7)** in a retained space of unknown dimensionality is a coin-flip: silhouette on ≤8-point clusters is high-variance and sensitive to a single misassigned point (one point flipping can move a small-group silhouette by >0.1). The "≥5 of 6 groups" escape hatch mostly absorbs this — but only if the two small groups are the *permitted* failures. As written, nothing says which group may be the one that fails, so a run could pass by sacrificing a *large* well-populated group (e.g. TOTEM/SENTRY n=26) while the small ones squeak through on noise. That is a vacuity.
- **PERMANOVA franchise R² ≤ 0.15** with 11–19 wildly unequal groups: adonis2 R² is sensitive to group-size imbalance and dispersion heterogeneity (PERMANOVA confounds location with dispersion). With Diablo+PoE = 282/470 (60%) of the mass, a low R² can be produced by imbalance *masking* real franchise structure, or a high R² can be inflated by one small idiosyncratic game's dispersion. R² ≤ 0.15 is a reasonable *target* but is not by itself interpretable without a companion dispersion check (betadisper/PERMDISP) and without pinning the grouping level.

## Verdict

**PASS-WITH-AMENDMENTS.** The four families, the corrections, the retention rule, the supplementary/passive treatments, and the decision rule are all sound and should execute as designed. Apply the seven amendments below (each is a specific edit to a specific section) before elrond executes; none requires re-thinking the method, only tightening the specification so a failed map cannot ship as a passed one and a real structure cannot fail on a small-N artifact. Tooling is feasible in Python for all four families (MCA via SVD-on-indicator, LCA via EM multinomial mixture, MDS via classical eigendecomposition are all standard); only Leiden has a hard library dependency — see A7.

---

## Amendments (numbered so gandalf can apply verbatim)

**A1 — Pin the Gate-A labeled subset as a frozen artifact (§1 + §5 Gate A).** BLOCKING for pre-registration integrity. Add to §1 (Data snapshot): *"The 6-group membership labeling is frozen as an explicit `kit_id → group` table (`atlas_gateA_labels_2026_07_14`), authored by gandalf and committed BEFORE any decomposition runs; `mobile_key_group` is DEPRECATED (register §6 line) and MUST NOT be used. The table lists exactly which kit_ids constitute each of WHIRLWIND(15)/TOTEM-SENTRY(26)/TRAP-MINE(24)/CHANNELED-BEAM(9)/AURA(8)/MINION-PET(7); membership rationale is one line per group. Kits not in any group are the unlabeled remainder and receive no Gate-A label."* Rationale: no group-label column exists in the DB; without a frozen table the ground-truth against which ARI is computed is constructible after seeing embeddings → Gate A is not pre-registered.

**A2 — Define "franchise" and pin the grouping level for Gates C & D (§1 + §5 Gates C/D).** BLOCKING. Add to §1: *"'franchise' for Gates C–D is the game-series rollup (PoE=poe1∪poe2; Diablo=d2∪d3∪d4∪di; TitanQuest=tq∪tq2; Hades=hades1∪hades2; Torchlight=tl1∪tl2∪tli; all others = own game), materialized as column `franchise_rollup` at Stage 0 → 11 franchises. Gate C PERMANOVA and Gate D LOFO both group on `franchise_rollup`, NOT on raw `game`."* Rationale: DB has 19 games, no franchise column; the prereg says "~12 franchises" without pinning which. The rollup vs raw-game choice materially changes both R² and the LOFO count; it must be fixed pre-execution.

**A3 — Constrain WHICH Gate-A group may be the permitted failure (§5 Gate A threshold).** Replace *"silhouette ≥ 0.2 for ≥ 5 of 6 groups"* with: *"silhouette ≥ 0.2 for ≥ 5 of 6 groups, AND the four large groups (WHIRLWIND, TOTEM-SENTRY, TRAP-MINE, CHANNELED-BEAM) must ALL clear 0.2; the single permitted sub-threshold group may only be AURA or MINION-PET (n≤8, where silhouette is intrinsically high-variance). A large-group silhouette failure fails Gate A outright."* Rationale: as written, the escape hatch could be spent on a well-populated group while noise carries the small ones — vacuity. This closes it and simultaneously acknowledges the honest small-N sensitivity.

**A4 — Add a PERMDISP companion to Gate C and state the interpretation guard (§5 Gate C).** Add a row/clause: *"Report betadisper/PERMDISP (dispersion homogeneity across franchises) alongside the PERMANOVA. R² ≤ 0.15 is the pass threshold ONLY if PERMDISP is non-significant (p ≥ 0.05) OR the gate report explicitly flags that a significant dispersion difference is present and gandalf rules on whether the low R² reflects genuine behavior-not-origin mixing vs an imbalance/dispersion artifact. With Diablo+PoE ≈ 60% of mass, R² alone is not self-interpreting."* Rationale: PERMANOVA confounds location and dispersion; at this imbalance a bare R² is not a trustworthy franchise-mixing verdict.

**A5 — Pin the plane-diameter definition (§5 Gate D + §6).** Add to §6 frozen artifacts and reference from Gate D: *"'plane diameter' = the maximum pairwise Euclidean distance between any two active (non-supplementary) kit coordinates in the retained-dimension space of the frozen basis, computed once on the full fit. All Gate-D displacement percentages use this scalar as denominator."* Rationale: Gate D's ≤10% threshold has an undefined scale without this; two defensible diameter definitions (max-pairwise vs bounding-box diagonal vs 2×RMS-radius) give different pass/fail lines.

**A6 — Pin Gate-B behavior when a red law has < 5 corpses, and the active-N of the permutation null (§5 Gate B).** Add: *"Red laws with < 5 keyed corpses are reported descriptively and EXCLUDED from the pass/fail decision (underpowered); the Gate-B verdict rests on the Fisher-combined p across only the laws with ≥ 5 corpses. The 10,000-permutation null draws 'k random corpus kits' from the ACTIVE (non-negative, non-supplementary) projected set, k = the corpse count of the law under test."* Rationale: §5 Gate-B row says "per red law with ≥ 5 corpses" but §A.4 tallies intrinsic-RED at only ~6 kit-deaths *total* across three laws — so ≥ 1 law will be under-powered; the decision must state it doesn't quietly drive the gate. Also the null's sampling frame ("38 random corpus kits") is ambiguous — pin it to the active set at the per-law k.

**A7 — Pin the Leiden library dependency and its permitted substitution (§4 row 2c + §9).** Add to 2c: *"Leiden requires `leidenalg`+`python-igraph`. If unavailable in the execution environment, substitution to Louvain (via `python-louvain`/`networkx`) is a §9 PROTOCOL AMENDMENT — logged with timestamp, NOT a silent swap — because Louvain optimizes modularity (resolution-limited, non-CPM) and can merge small communities the CPM objective would keep separate, which directly bears on recovering AURA/MINION-PET. MCA/LCA/MDS have no hard external dependency (implementable via SVD-on-indicator, EM multinomial mixture, and classical eigendecomposition respectively) and need no substitution clause."* Rationale: (e) tooling feasibility — this is the one family whose faithful implementation has a real dependency risk, and its substitute is not behavior-equivalent for exactly the small groups Gate A stresses.

---

## What I did NOT flag (and why — so gandalf can trust the silence)

- **Four-family choice:** correct. Nothing statistically embarrassing. MCA/CATPCA for categorical dimensionality reduction, Gower-MDS as distance cross-check, Leiden/LCA as partition witnesses — this is the right triangulation for 470×13 nominal.
- **Greenacre correction, MFA weighting, permutation-null retention, ordinal-only-on-tempo/commit, rare-category fusing at n<10 once-for-all-families:** all correct and disciplined. The CATPCA-vs-MCA divergence-as-diagnostic framing is a nice touch.
- **ARI ≥ 0.6:** appropriate and non-vacuous — ARI is chance-corrected, so 0.6 is a genuinely substantial-agreement bar that noise will not clear at this N. No change.
- **Bootstrap ≤10% displacement and LOFO/reweight Procrustes ≥0.85:** correct stability battery; ≥0.85 Procrustes is a sensible, non-trivial bar. Only the plane-diameter denominator (A5) and the LOFO grouping level (A2) needed pinning.
- **Decision rule:** the "one diagnosed amendment cycle max, else fallback, second attempt needs fresh v2 prereg with jack-ryan review" is tight. The only wiggle-room a failed map could exploit was the under-defined Gate-A label (A1) and Gate-C interpretation (A4) — closed by the amendments. No structural loophole remains.
- **Fallback clause (charter §10):** honorable and pre-committed. Good.

## Action

- [ ] gandalf (SPEC-AUTHOR): apply amendments A1–A7 to the prereg verbatim; A1 (frozen Gate-A label table) and A2 (franchise rollup column) are the two that must land as *artifacts* before elrond executes, not just as prose.
- [ ] elrond (executor): after A2, materialize `franchise_rollup` at Stage 0; consume the `atlas_gateA_labels_2026_07_14` table for Gate A; log any Leiden→Louvain substitution as a §9 amendment (A7).
- [ ] Matt: no decision needed at Gate-1 — this is a PASS-WITH-AMENDMENTS, all seven are specification-tightening within gandalf's authorship authority (ADR-002 doc-tier). Matt's ratification is owed at Edition-I freeze (charter §9), not here.

## References

- `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` — document under review
- `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` — governance frame
- `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` — input register (§6 line 6: `mobile_key_group`/`mobile_cell_id` DEPRECATED — grounds A1)
- `agentic_orchestration/gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` §A — 38-negative taxonomy + 6-group definitions (grounds A1, A6); §A.4 red-law tally = ~6 intrinsic deaths (grounds A6 under-power concern)
- `agentic_orchestration/research/curated/corpus.db` — DB facts verified this session: 524/38 (canon_corpus); 487/470/17 (canon_engine_key, cell_key on all 470); 19 games / 11-franchise-rollup, distribution poe1=88…tl1=2 (grounds A2); passive load 17–24/470 on materialized coords; no group-label column exists (grounds A1)
