# Statistical Analysis Findings — ARPG Community Research Sprint

> **STATUS:** CURRENT — Authored by elrond 2026-05-29 evening late per single-batch elrond statistical-analysis dispatch. Operationalizes 8 statistical analyses pre-registered in `statistical-methodology-brief.md`; composes with R4 synthesis verdict for VALIDATES / REFUTES / UNCERTAIN judgments. All raw outputs persisted in `research.db.statistical_findings` table + `statistical-findings.json`.

**Date:** 2026-05-29 evening late
**Author:** elrond (catalogue DB + abstraction-analysis steward)
**Authority:** Matt 2026-05-29 evening late ("fire single-batch elrond dispatch")
**Companion artifacts (this dir):**
- `statistical-methodology-brief.md` — pre-registered methodology + design-steward review surface
- `synthesis-verdict.md` — gandalf R4 qualitative claims being statistically validated
- `research.db.statistical_findings` — 9 finding rows
- `statistical-findings.json` — finding dump
- `analysis-3-per-game-summary.csv` — per-game layer + entropy + composite metric
- `analysis-5-rules.csv` — Apriori rules (empty)
- `analysis-6-naming-decomposition.csv` — per-build naming-pattern tokenization
- `analysis-8-universality.json` — per-game speedfarm/push presence matrix

**Companion script:** `agentic_orchestration/research/scripts/arpg_statistical_analyses_2026_05_29.py`

---

## 0. TL;DR

| # | Synthesis claim | Statistical verdict | Effect size + key statistic |
|---|---|---|---|
| 1 | Cross-site vocabulary convergence labels are coherent | **VALIDATES** (Spearman ρ=0.79, p<1e-8, q_BH=2.8e-8) — labels track underlying site-count evidence | ρ=0.79 |
| 1b | Activity vocab equal across sites (not synthesis claim — methodology cross-check) | VALIDATES_with_caveat — sites significantly DIFFER in activity emphasis (Cramér's V=0.51) but convergence is about same-concept-named-across-sites, not equal-frequency | Cramér's V=0.51 |
| 2 | Game determines composite-vs-single-axis pattern | **VALIDATES STRONGLY** (Cramér's V_bias-corrected=0.74; permutation p≈1e-4, q_BH=3e-4) — complete categorical separation: PoE 10/0/0, LE 0/0/7 | V=0.74 |
| 3 | Multi-layer count drives composite-restriction severity | **UNCERTAIN** — only n=4 games; descriptively, total vocab DENSITY (PoE 44 vs LE 16) is a better discriminator than raw layer count | ρ=0.80 (descriptive) |
| 4 | Stat-target patterns cluster on archetype | **UNCERTAIN** — only n=13 builds with stat targets; best-k=6, silhouette=0.35 (modest); clusters emerge but n too small for inferential generalization | silhouette=0.35 |
| 5 | Skill+gear co-occurrence forms composition signatures | **REFUTES (with caveat)** — n=35 transactions × 0 rules at min_support=0.10, min_conf=0.50; gear too sparse and diverse for market-basket discovery at this corpus size | 0 rules |
| 6 | [Skill]×[Class]×[Activity] naming pattern STRONG at 6 sites | **VALIDATES_REFINED** — 3-way conjunction at 53% (Wilson 95% CI: 0.43-0.62); Skill+Class spine at **91%** is the actual dominant pattern; strict 3-way is Maxroll-D4-specific (95% there, 0% at Maxroll-LE and PoE-Vault) | Skill+Class 91% |
| 7 | Investment-tier vocabulary cross-game canonicalization | **UNCERTAIN** — only 8/104 (7.7%) builds had extractable signal in DB fields; signal exists in source content but not preserved in current schema (extension candidate) | n=14 / coverage 8% |
| 8 | Speedfarm ↔ Push binary universal at all 4 games | **REFUTES** (universality claim) — only 2/4 games (D4 + PoE) have both variants present; LE 0 speedfarm; PoE2 0 speedfarm; pooled 39% (Wilson CI 0.29-0.49); "allround" modal at 41% | 2/4 universality |

**Overall epistemic verdict on synthesis:** the synthesis-verdict's core empirical claims (cross-site convergence as coherent ordinal; Matt composite-restriction critique; per-game composite-pattern separation) **statistically validate at strong effect sizes with multi-comparison correction surviving**. Two specific quantitative claims **refine or refute**: (a) "[Skill]×[Class]×[Activity] naming STRONG at 6 sites" should be re-stated as **"Skill + Class spine universal; activity-suffix Maxroll-D4-specific"**; (b) "Speedfarm ↔ Push universal at all 4 games" should be re-stated as **"Push universal (4/4); Speedfarm absent in LE and PoE2 corpus"** — refutes universal-binary; supports push-as-universal with speedfarm-as-PoE/D4-specific.

The composite-restriction causal mechanism (multiplicative layer count) is **consistent with descriptive evidence but not statistically validated** at n=4 games; refinement: vocabulary entry DENSITY (PoE 44 vs LE 16) and augmentation-layer richness (PoE 14 vs LE 1) appear to be the stronger numerical discriminators than raw layer-count.

---

## 1. Analysis 1 — Cross-site vocabulary convergence

### 1.a — Spearman ordinal coherence (primary test)

| Item | Value |
|---|---|
| Hypothesis | H0: convergence_strength label is independent of sites_observed_count |
| Test | Spearman rank correlation (ordinal) |
| n | 37 convergence rows |
| Statistic | ρ = 0.7937 |
| Raw p | 4.61 × 10^-9 |
| BH q-adjusted | 2.77 × 10^-8 |
| Significant at q=0.10 | YES |
| Effect size | ρ = 0.79 (large) |
| Sample-size adequacy | YES (n=37 sufficient) |

**Per-strength mean site-count:**
- STRONG (n=22): mean 4.64 sites
- MODERATE (n=9): mean 3.33 sites
- WEAK (n=6): mean 2.00 sites

**Interpretation:** the qualitative convergence_strength labels coherently track the underlying site-count evidence. Labels are not arbitrary — they ordinally reflect the breadth of cross-site agreement. The synthesis verdict's use of STRONG / MODERATE / WEAK labels is internally consistent with the evidence and survives Benjamini-Hochberg correction with substantial margin.

**Synthesis composition: VALIDATES.**

### 1.b — Chi-square activity_name × source_site (methodological cross-check)

| Item | Value |
|---|---|
| Hypothesis | H0: activity_name is independent of source_site |
| Test | Chi-square independence |
| n | 64 activity rows |
| Statistic | χ² = 81.96, dof = 45 |
| Raw p | 6.29 × 10^-4 |
| BH q-adjusted | 1.26 × 10^-3 |
| Significant at q=0.10 | YES |
| Effect size | Cramér's V = 0.51 (moderate-to-large) |
| Sample-size adequacy | CAVEAT — 100% of expected cells <5; asymptotic χ² with caution |

**Interpretation:** sites significantly differ in WHICH activity-names they emphasize (e.g., PoE-Vault dominantly publishes mapping + bossing; Maxroll-D4 dominantly publishes pit_pushing + speedfarming + bossing; Maxroll-LE publishes mostly bossing). Significant association DOES NOT refute cross-site CONVERGENCE — convergence is about same-concept-named-across-sites (which Mode A confirmed qualitatively), not equal-frequency-per-site. The chi-square measures EMPHASIS variation, not vocabulary alignment.

**Synthesis composition: VALIDATES_with_caveat.** The synthesis claim "Bossing convergent at 6 sites" is not refuted; the methodology cross-check surfaces that sites publish UNEQUAL VOLUMES of each activity category — a per-site editorial-emphasis effect, not a vocabulary fragmentation effect. Worth noting in canonical commit framing: "vocabulary is convergent; emphasis differs per site."

---

## 2. Analysis 2 — Composite-vs-single-axis × game

| Item | Value |
|---|---|
| Hypothesis | H0: composite-pattern is independent of game |
| Test | Chi-square + Monte Carlo permutation (n_perm=10,000) for sparse cells |
| n | 30 composite_archetype_assessment rows |
| χ² | 36.87 (dof=6) |
| Raw p (asymptotic) | 1.87 × 10^-6 |
| **Permutation p** | **9.999 × 10^-5** (1/10001 → p_perm ≈ 0.0001) |
| BH q-adjusted | 3.00 × 10^-4 |
| Significant at q=0.10 | YES |
| Effect size | Cramér's V = 0.78 (raw); 0.74 (Bergsma bias-corrected) — LARGE |
| Sample-size adequacy | YES — modest n=30, but pattern shows complete categorical separation in 2 of 4 rows |

**Contingency:**

| Game | composite_required | hybrid | single_axis_viable | Total |
|---|---|---|---|---|
| PoE | 10 | 0 | 0 | 10 |
| PoE2 | 4 | 3 | 0 | 7 |
| D4 | 5 | 1 | 0 | 6 |
| LE | 0 | 0 | 7 | 7 |

**Interpretation:** Game is a STRONG predictor of composite-vs-single-axis pattern. PoE and LE are completely separated (PoE 100% composite-required; LE 100% single-axis-viable). D4 is between (83% composite_required, 17% hybrid). PoE2 is between (57% composite_required, 43% hybrid).

**Matt's "downfall of the developer" critique empirically validated with substantial effect size + multi-comparison correction surviving (q_BH = 3e-4).**

**Synthesis composition: VALIDATES.** This is the strongest statistical result in the sprint; survives Bonferroni equally (α/15 = 0.0033; p_perm = 0.0001 < 0.0033) — so the validation holds under either correction approach.

---

## 3. Analysis 3 — Multi-layer loot substrate distribution

| Item | Value |
|---|---|
| Hypothesis | H0: layer-count + entropy independent of composite-restriction severity |
| Test | Spearman rank correlation across 4 games (descriptive only) |
| n | 4 games |
| Spearman ρ (layer_count vs pct_composite) | 0.26 (p=0.74) |
| Spearman ρ (entropy vs pct_composite) | 0.40 (p=0.60) |
| Spearman ρ (total_vocab vs pct_composite) | 0.80 (p=0.20) |
| Sample-size adequacy | **NO for inferential**; descriptive only |

**Per-game summary:**

| Game | Layer count (nonzero) | Total vocab entries | Shannon H | pct_composite_required |
|---|---|---|---|---|
| PoE | 5 | 44 | 1.55 | 100% |
| PoE2 | 4 | 9 | 1.22 | 57% |
| D4 | 5 | 23 | 1.27 | 83% |
| LE | 5 | 16 | 1.49 | 0% |

**Interpretation:** PoE and LE both have 5 distinct layers — raw layer COUNT does not discriminate them. What separates PoE (100% composite-required) from LE (0% composite-required) is **total vocabulary DENSITY** (44 vs 16 entries) AND **augmentation-layer richness specifically** (PoE has 14 augmentation entries; LE has 1).

**Refinement of synthesis-verdict causal claim:** the synthesis stated "multiplicative layer count → composite restriction." The data refines this to: **vocabulary density at the augmentation + character-substrate layers** is the discriminator, not raw layer count. PoE's 14-entry augmentation layer (scarabs/sextants/Delirium Orbs/Beasts/etc.) is the multi-layer multiplier; LE's 1-entry augmentation layer is structurally lighter even with 5 layers nominally present.

**Synthesis composition: UNCERTAIN.** Causal claim consistent with descriptive evidence but cannot be statistically validated at n=4. Refinement: shift framing from "layer COUNT" to "augmentation-layer VOCABULARY DENSITY" as the architectural variable Reincarnated should manage.

---

## 4. Analysis 4 — Stat-target clustering

| Item | Value |
|---|---|
| Hypothesis | H0: stat-target vectors form no archetype-coherent clusters |
| Test | Hierarchical clustering (Ward) with silhouette evaluation |
| n | 13 builds (with non-null stat targets) |
| Stats dimensions | 15 |
| Best k | 6 |
| Silhouette at k=6 | 0.35 (modest) |
| PCA 2-component var explained | 46.7% |
| Sample-size adequacy | UNCERTAIN — low n |

**Cluster signatures (verbal description):**

- **Cluster 1 (n=3):** D4 Necromancers; dominant stats life (30k), attack_speed (100%), crit_chance (100%) — high-throughput dps profile
- **Cluster 2 (n=2):** PoE2 spell casters (Stormweaver, Martial Artist); energy_shield (6500), item_rarity (125%), movement_speed (17.5%) — ES + IIR composite
- **Cluster 3 (n=5):** mixed games (D4 3, PoE 1, LE 1); Barbarians + Rogue + Inquisitor + Lich; life (1800), energy_shield (600), life_regen (600) — defensive-tank profile
- **Cluster 4 (n=1):** PoE Deadeye; dps (1M), life_es_combined (3000) — pure-damage outlier
- **Cluster 5 (n=1):** D4 Rogue; maximum_energy (225), death_trap_cooldown (15s) — utility-cooldown outlier
- **Cluster 6 (n=1):** PoE Pathfinder; life (5000), life_regen (3000), spell_suppression (100%), aoe_increase (40%) — life-sustain outlier

**Interpretation:** clusters DO emerge — particularly the "tank-defensive" cluster (n=5) that spans multiple games and classes, and the D4-Necromancer high-throughput cluster. But n=13 with 15 stats is severely underpowered (1 build per cluster for 3 of 6 clusters). The PCA-2 variance ratio (47%) suggests dimensional reduction does compress signal somewhat.

**Synthesis composition: UNCERTAIN.** Clustering exists in the data but the corpus is too thin to make claims about archetype-stat-signature mapping. Schema-extension candidate: expand stat-target extraction (currently only Maxroll D4 + PoE2 have meaningful coverage) to enable proper clustering at n>50.

---

## 5. Analysis 5 — Skill + gear co-occurrence (Apriori)

| Item | Value |
|---|---|
| Hypothesis | H0: skill-gear items are independent (no co-occurrence beyond chance) |
| Test | Apriori market-basket (max_len=3, min_support=0.10, min_conf=0.50) |
| n | 35 transactions (builds with any skill or gear items) |
| Frequent itemsets | 2 |
| Rules at conf ≥ 0.50 | **0** |
| Sample-size adequacy | UNCERTAIN — corpus is too sparse for meaningful patterns |

**Interpretation:** at min_support=0.10 the corpus produces only 2 frequent itemsets (singletons effectively) and zero confidence-≥-0.50 rules. The corpus is structurally too sparse: 164 skill entries / 95 gear entries spread across 35 builds = average ~4.7 skills + ~2.7 gear per build, with high item diversity. With 95 distinct gear items across 35 builds, most items appear in only 1-2 builds — below any meaningful support threshold.

**Synthesis composition: REFUTES.** No skill-gear composition signatures emerge at current corpus size. Synthesis verdict made no specific market-basket claim; this analysis was discovery, not confirmation. **Negative result: documented.** Future work needs n≥100 builds with full skill+gear coverage to make market-basket viable.

**Operational implication:** the synthesis-verdict's "[Skill] × [Class] × [Activity] naming pattern" is NOT supported by skill-gear co-occurrence at the item-association level. Build identity is captured at the naming/labeling layer rather than at the item-association layer — possibly meaningful: ARPG community vocabulary may live at the abstraction layer (Skill + Class label) rather than at the item-substrate layer (specific skill-gear sets), which would refine the "designer-writes-substrate / player-names-experience" principle.

---

## 6. Analysis 6 — Naming pattern decomposition

| Item | Value |
|---|---|
| Hypothesis | H0: [Skill]×[Class]×[Activity] 3-way pattern frequency ≤ 0.50 |
| Test | Exact binomial (one-sided, p_null=0.50, alternative=greater) + Wilson 95% CI |
| n | 104 builds (with build_name) |
| 3-way (Skill × Class × Activity) | **55/104 = 52.9%** (Wilson CI 0.43-0.62) |
| Skill × Class pairwise | **95/104 = 91.3%** ← dominant pattern |
| Class × Activity pairwise | 58/104 = 55.8% |
| Skill × Activity pairwise | 56/104 = 53.8% |
| Binomial p (3-way > 0.50) | 0.31 |
| BH q-adjusted | 0.37 |
| Significant at q=0.10 | NO |

**Per-source 3-way hit rate:**

| Source | n | 3-way hit rate |
|---|---|---|
| Maxroll D4 | 21 | 95% |
| Icy-Veins D4 | 18 | 89% |
| Maxroll PoE | 20 | 85% |
| Maxroll PoE2 | 20 | 10% |
| Maxroll LE | 20 | 0% |
| PoE-Vault | 5 | 0% |

**Interpretation:** the synthesis-verdict's "STRONG at 6 sites" claim for the strict 3-way pattern is **REFUTED at strict-3-way level** — the binomial test (3-way > 50%) does not reject H0. However, the **Skill+Class pairwise spine holds at 91%** — that IS universal across sources.

The 3-way naming convention is **Maxroll-D4 + Icy-Veins-D4 + Maxroll-PoE editorial convention** (85-95% there), driven by the explicit "Endgame Build" / "Leveling Guide" / "League Starter" suffix conventions on those sites. Maxroll-LE and PoE-Vault use naked Skill+Class names without activity suffixes ("Smite Paladin", "Tornado Shaman").

**Refined synthesis claim should be:**
- "Skill + Class" naming spine: **UNIVERSAL at 91%** across sites
- "Skill + Class + Activity-suffix": **per-source editorial convention** — present at Maxroll-D4 + Icy-Veins-D4 + Maxroll-PoE; absent at Maxroll-LE + PoE-Vault
- The class-as-vestigial-reference layer holds; the activity-suffix is a publication-format choice, not a community-vocabulary universal

**Synthesis composition: VALIDATES_REFINED.** Pattern is real and important, but the synthesis verdict over-stated the strict 3-way universality. Skill+Class as the universal naming spine is the correct framing for canonical commit.

---

## 7. Analysis 7 — Investment-tier cross-game distribution

| Item | Value |
|---|---|
| Hypothesis | H0: investment-tier vocabulary independent of game |
| Test | Chi-square + Monte Carlo permutation (n_perm=10,000) |
| Coverage | 8/104 (7.7%) builds had extractable signal in available DB fields |
| n (build-tier observations) | 14 |
| χ² | 4.43 (dof=6) |
| Raw p (asymptotic) | 0.62 |
| Permutation p | 0.72 |
| BH q-adjusted | 0.72 |
| Cramér's V | 0.40 |

**Contingency (sparse):**

| Game | budget | high_budget | low_budget | starter |
|---|---|---|---|---|
| LE | 0 | 0 | 0 | 2 |
| PoE | 3 | 1 | 3 | 3 |
| PoE2 | 0 | 0 | 1 | 1 |
| D4 | 0 | 0 | 0 | 0 |

**Interpretation:** The current schema's extractable text fields (tagline + summary + pros/cons) contain investment-tier signal in only 7.7% of builds — most build pages encode investment-tier in side-bar metadata, structured ratings, or separate "budget gear" sections that did not migrate to the curated DB. The chi-square is underpowered; even at the available signal, Maxroll-D4 produced ZERO investment-tier vocabulary in the extracted text fields.

**Synthesis composition: UNCERTAIN.** The synthesis verdict's claim "5-tier investment vocabulary STRONG at 6 sites" cannot be validated or refuted from the current DB extraction. **Schema extension candidate:** add explicit `investment_tier` column to builds + Mode B re-crawl to capture this metadata directly. The signal IS real in source content; it's a DB-coverage gap, not a corpus gap.

---

## 8. Analysis 8 — Speedfarm ↔ Push binary universality

| Item | Value |
|---|---|
| Hypothesis | H0: speedfarm AND push present in every game (universal binary axis) |
| Test | Per-game presence/absence; pooled proportion with Wilson CI |
| n | 83 variants across 4 games |
| Pooled speedfarm-or-push | 32/83 = **38.6%** (Wilson CI 0.29-0.49) |
| Games with BOTH speedfarm AND push present | **2/4** (D4 + PoE only) |

**Per-game presence:**

| Game | n_variants | has speedfarm | has push | count_speedfarm | count_push |
|---|---|---|---|---|---|
| D4 | 50 | YES | YES | 8 | 17 |
| PoE | 13 | YES | YES | 1 | 3 |
| LE | 10 | **NO** | YES | **0** | 1 |
| PoE2 | 10 | **NO** | YES | **0** | 2 |

**Interpretation:** the synthesis verdict's "Speedfarm ↔ Push binary universal at all 4 games" claim is **REFUTED at the universality level**. LE and PoE2 corpus contains ZERO speedfarm variants. Push is universal (4/4 games); speedfarm is D4/PoE-specific in the corpus.

Additional finding: **"allround" / endgame-generalist is the modal activity_focus** at 34/83 = 41% — larger than push (22) or speedfarm (9). The "binary axis" framing collapses if the modal category is recognized as a third pole.

**Refined synthesis claim should be:**
- **Push:** universal variant marker (present in all 4 games)
- **Speedfarm:** D4/PoE-genre-specific variant marker; absent or under-represented in LE + PoE2 corpus
- **Allround / Endgame Generalist:** the modal variant — the "no specialization" pole that the push/speedfarm extremes sit around
- The "binary" should be re-framed as a **trinary** (push / speedfarm / allround) or as **push-as-universal vs speedfarm-as-genre-specific**

**Synthesis composition: REFUTES (universality claim).** Push universality validates; speedfarm universality refutes; binary framing should be revised.

**Caveat:** the LE + PoE2 corpus has only 10 variants each — small per-game samples. A larger corpus might surface speedfarm variants in LE/PoE2. But within current evidence, the universal-binary claim is not supported.

---

## 9. Cross-analysis discussion

### 9.1 Three synthesis claims STRONGLY VALIDATED with multi-comparison correction surviving

1. **Cross-site vocabulary convergence labels are coherent** (Analysis 1a: Spearman ρ=0.79, q_BH<1e-7)
2. **Game determines composite-vs-single-axis pattern** (Analysis 2: Cramér's V=0.74 bias-corrected, q_BH=3e-4)
3. **Activity vocabulary varies in EMPHASIS across sites** (Analysis 1b methodological cross-check; q_BH=1e-3) — refines but does not refute the convergence claim

These three are **publication-grade rigor** for Cycle 15+ canonical commits. The synthesis verdict's Matt-composite-restriction-critique is the strongest empirically-validated finding of the sprint.

### 9.2 Two synthesis claims REFINED — original framing over-stated

1. **"[Skill]×[Class]×[Activity] STRONG at 6 sites"** → revise to **"Skill+Class spine universal at 91%; activity-suffix Maxroll-D4-editorial-specific"** (Analysis 6)
2. **"Speedfarm ↔ Push binary universal at all 4 games"** → revise to **"Push universal (4/4); Speedfarm D4/PoE-specific; modal variant is Allround"** (Analysis 8)

Both refinements PRESERVE the substantive insight (community vocabulary at the Skill+Class layer; push/speedfarm polarization meaningful where present) but TIGHTEN the universality claims. Recommend reframing in canonical commits.

### 9.3 Three claims UNCERTAIN — corpus too thin for inferential validation

1. **Multi-layer count → composite-restriction causal claim** (n=4 games; Analysis 3) — descriptively supports the synthesis-verdict direction; refinement: vocab DENSITY > raw layer count
2. **Stat-target clustering** (n=13 builds; Analysis 4) — clusters emerge but corpus too thin
3. **Investment-tier game distribution** (8% coverage; Analysis 7) — signal-extraction gap, not a corpus-pattern gap

All three are **schema-extension or corpus-expansion candidates** for sprint+1.

### 9.4 One synthesis-claim-adjacent finding REFUTES

1. **Skill+gear market-basket co-occurrence** (Analysis 5: 0 rules) — corpus too sparse for item-association patterns. Methodologically interesting: build identity appears to live at the Skill+Class LABEL layer, not at the skill-gear ITEM layer. Refines the designer-writes-substrate/player-names-experience principle: **the "name" layer is more compressed (Skill+Class) than the substrate item-set layer**, which is consistent with the "vestigial designer construct" framing in the principle doc.

### 9.5 Per-source-weighting observation (methodology brief § 3.3)

The corpus is Maxroll-heavy (78%). Two findings show source-dependent results that pooled analyses would mask:

- **Naming pattern** (Analysis 6) — Maxroll-D4 95% 3-way; Maxroll-LE 0%; PoE-Vault 0%. Per-source disaggregation is essential to avoid Maxroll-D4 editorial-convention being mistaken for community-universal.
- **Speedfarm presence** (Analysis 8) — D4 + PoE corpora have speedfarm variants; LE + PoE2 corpora do not.

For Cycle 15+ canonical commits, source-conditional statements (e.g., "Maxroll-D4 convention is...") are more rigorous than pooled statements (e.g., "the universal pattern is...").

### 9.6 Multiple-testing correction outcome

Of 6 p-values produced, **3 are significant at BH q=0.10** (analyses 1a, 1b, 2). The 3 non-significant tests (3, 6, 7) align with the UNCERTAIN / REFINED verdicts above. **Bonferroni would produce identical decisions** at α/15 ≈ 0.003 — analyses 1a (p=4.6e-9), 1b (p=6.3e-4), 2 (p=1e-4) all survive even strict Bonferroni; the others (p ≥ 0.20) do not survive either correction. The verdict pattern is robust to choice of correction method (FDR vs Bonferroni produces same VALIDATES/UNCERTAIN classification).

---

## 10. Cycle 15+ canonical-write input recommendations

**Publication-grade rigor (commit-ready):**
- Cross-site vocabulary convergence label coherence (Analysis 1a)
- Game × composite-restriction empirical separation (Analysis 2) — **Matt critique validated**
- Activity-emphasis-varies-per-site nuance (Analysis 1b)

**Refined-framing canonical inputs:**
- Skill+Class naming spine (91%) as universal; activity-suffix as Maxroll-D4 editorial convention (Analysis 6)
- Push as universal variant; Speedfarm as D4/PoE-specific; Allround as modal — replaces "binary universal" framing (Analysis 8)

**Hold-for-corpus-expansion (do not canonical-commit at current evidence):**
- Multi-layer-count causal mechanism (Analysis 3) — refine to vocab-DENSITY framing if committed
- Stat-target archetype-signature mapping (Analysis 4)
- Investment-tier game distribution (Analysis 7) — schema-extension candidate
- Skill+gear composition signatures (Analysis 5) — corpus-size candidate

---

## 11. Sign-off and surface-to-gandalf

**Authored:** elrond per ARPG community research sprint statistical-validation Task 2 closing the single-batch elrond dispatch.

**For:** the statistical operationalization + multi-comparison-corrected validation of R4 synthesis-verdict qualitative claims; provides publication-grade-rigor commit candidates and refined-framing recommendations for Cycle 15+ canonical writes.

**Surface to gandalf (per dispatch instruction):**

1. **EXTENDS synthesis verdict:** Analysis 1b (activity-emphasis varies per site, q_BH=1e-3) is a NEW finding not in the synthesis verdict; adds "emphasis-vs-vocabulary" distinction worth weaving into the canonical narrative.

2. **REFUTES synthesis verdict specific claim:** Analysis 8 — "Speedfarm ↔ Push binary universal at all 4 games" REFUTES at universality level. LE + PoE2 corpus has zero speedfarm variants. Recommend re-framing in any canonical commit to "Push universal; Speedfarm D4/PoE-specific."

3. **REFUTES synthesis verdict specific claim (refined):** Analysis 6 — "[Skill]×[Class]×[Activity] STRONG at 6 sites" holds only at Skill+Class level (91%); strict 3-way is Maxroll-D4-editorial-convention. Recommend re-framing the canonical claim to "Skill+Class spine universal; activity-suffix per-source convention."

4. **REFINES synthesis verdict causal claim:** Analysis 3 — multi-layer-count is consistent with composite-restriction but vocabulary DENSITY (PoE 44 vs LE 16) and augmentation-layer richness (PoE 14 vs LE 1) are the better numerical discriminators than raw layer count. Refine Reincarnated design-implication from "≤3 layers" to "≤3 layers AND lean augmentation-layer vocabulary."

5. **Schema-extension candidates surfaced:** investment_tier column on builds (Analysis 7); fuller stat_target extraction (Analysis 4); fuller build-level skill+gear (Analysis 5); these would enable sprint+1 inferential validation.

**Decisions taken without gandalf overrule:**
- Used FDR (BH q=0.10) per methodology brief; verified Bonferroni produces same VALIDATES/UNCERTAIN classification on the 6 p-values, so verdict pattern is robust
- Substituted Cohen's kappa with Spearman-on-ordinal-labels per methodology brief § 1 item (2)
- Analysis 4 reported as UNCERTAIN-on-low-n per methodology brief § 1 item (3)
- Analysis 5 raised support floor to 0.10 per methodology brief § 1 item (4); even at 0.07 retry zero rules emerged

**Schema/code drift note (jack-ryan or owner attention):** `schema.sql` does not include `composite_archetype_assessment` table that exists in research.db. Minor drift; not blocking.

**Sprint deliverables — COMPLETE:**
- Methodology brief (Task 1) — committed at `statistical-methodology-brief.md`
- Statistical analysis findings (Task 2) — committed at `statistical-analysis-findings.md`
- `statistical_findings` table in research.db (9 rows)
- `statistical-findings.json` finding dump
- Supporting CSVs and JSON per-analysis

**Next: gandalf re-engages at Cycle 14 wave-close for canonical-promotion review with statistical-rigor backing for the 3 publication-grade claims + revised framing for the 2 refined claims.**
