# Statistical Methodology Brief — ARPG Community Research Sprint Statistical Validation

> **STATUS:** CURRENT — Authored by elrond 2026-05-29 evening late per single-batch elrond statistical-analysis dispatch. Sits between R4 synthesis verdict (gandalf) and Task 2 statistical execution (elrond). Surfaces methodology decisions for gandalf design-steward review per Disc #18 math hotspot consultation pattern.

**Date:** 2026-05-29 evening late
**Author:** elrond (catalogue DB + abstraction-analysis steward)
**Authority:** Matt 2026-05-29 evening late ("fire single-batch elrond dispatch") + gandalf design-steward Disc #18 math hotspot consultation pattern
**Companion artifacts (this dir):**
- `research.db` — populated SQLite (13 tables; 104 builds; 92 loot vocab; 37 convergence; 30 composite assessments; 164 skills; 95 gear; 61 stat targets; 64 activities; 83 variants; 313 pros/cons; 28 perf claims; 33 summaries; 24 structured ratings)
- `synthesis-verdict.md` — gandalf R4 synthesis (the qualitative claims this brief operationalizes for statistical testing)
- `schema.sql` — DB schema (note: schema.sql does NOT include `composite_archetype_assessment` table that exists in research.db; minor schema/code drift to flag at brief commit time)

---

## 0. Purpose and framing

The R4 synthesis verdict asserts qualitative claims (STRONG/MODERATE/WEAK convergence labels; "composite-required" patterns per game; "Speedfarm ↔ Push binary universal" claim; "[Skill]×[Class]×[Activity] naming STRONG at 6 sites"). This brief operationalizes those qualitative claims as testable statistical hypotheses with explicit pre-registered methods, sample-size diagnostics, and multiple-testing correction.

The brief explicitly subordinates qualitative narrative to statistical rigor: where the corpus is too small for asymptotic inference, exact methods are preferred; where multiple sources weight unevenly (Maxroll 81/104; PoE-Vault 5/104), per-source-conditional analyses are surfaced alongside pooled analyses; where the synthesis verdict's "STRONG convergence" rests on site-counts that cross beyond the builds corpus (e.g., concept #1 "Bossing" cites 6 sites including ssegold, tigerjek, games_gg_le, 4rsgolds, exitlag — sites not represented in `builds`), the methodology distinguishes between the convergence-table's site population (n=6 site-categorical observations) and the builds corpus (n=104, 6 source_sites of which 4 dominate).

This distinction matters: Cohen's kappa over the 37 convergence rows operates on a different sample than chi-square over the 64 build_activities rows. The brief is explicit about which statistic answers which empirical claim.

## 1. Disc #18 math hotspot consultation surface

Per Disc #18 (math-hotspot consultation pattern), the following methodology decisions are surfaced for gandalf design-steward review before Task 2 fires:

1. **Multiple-testing correction approach** (§ 4): I propose Benjamini-Hochberg FDR (q=0.10) over Bonferroni. Justification below. Gandalf may overrule with Bonferroni (more conservative) if the synthesis-verdict findings need to survive the stricter bar.
2. **Convergence-label inter-rater agreement** (Analysis 1): Cohen's kappa requires two independent raters labeling the SAME items. The DB has a single `convergence_strength` label per concept. I propose substituting **per-concept site-count cross-validation** (using `sites_observed_count` as a continuous proxy for convergence strength, and Spearman rank correlation against the STRONG/MODERATE/WEAK ordinal label) PLUS **chi-square independence of activity_name × source_site** on the builds corpus. This is methodologically defensible but is NOT classic Cohen's kappa. Gandalf may direct toward an alternative if the synthesis verdict's "inter-site agreement" claim requires a different operationalization.
3. **Analysis 4 clustering n=16** (stat-target builds only): only 16 of 104 builds have stat targets. Hierarchical clustering on 16 builds is feasible but yields silhouette coefficients with very wide confidence intervals. I will proceed but flag this as UNCERTAIN-on-low-n rather than VALIDATES/REFUTES.
4. **Analysis 5 market-basket support floor**: the dispatch specifies min support 0.05. With 31 builds-with-skills × 34 builds-with-gear (joined intersection unknown until queried), support=0.05 ≈ 1.5 builds — too low for meaningful patterns. I will raise floor to support=0.10 if the joined corpus is <50 builds, and surface this calibration choice.
5. **Schema/code drift**: `composite_archetype_assessment` table exists in research.db but is missing from `schema.sql`. Flagged for jack-ryan / star-lord-equivalent owner attention. Not blocking for this analysis.

If gandalf wishes to overrule any of (1)-(5) before Task 2 fires, the surface is here.

## 2. Per-analysis test selection

| # | Synthesis claim being tested | Primary test | Effect-size statistic | Sample-size profile |
|---|---|---|---|---|
| 1 | Cross-site vocabulary convergence labels (STRONG/MODERATE/WEAK) are coherent | Spearman rank correlation (sites_observed_count vs ordinal convergence_strength); chi-square independence (activity_name × source_site) | Cramér's V (chi-square); Spearman ρ | convergence: n=37; activities pooled: n=64 |
| 2 | Game determines composite-vs-single-axis pattern (PoE 10/0/0; LE 0/0/7) | Fisher's exact test (game × pattern_observed); chi-square as supplement | Cramér's V | n=30; expected cell counts small → Fisher exact preferred |
| 3 | Multi-layer count drives composite-restriction severity (causal claim) | Spearman rank correlation (per-game layer-count and Shannon entropy vs per-game composite_required proportion) | Spearman ρ + 95% CI | n=4 games only — TOO SMALL for inferential statistics; descriptive only |
| 4 | Stat-target patterns cluster on archetype | Hierarchical clustering (Ward linkage) + PCA (2-component); silhouette coefficient | Silhouette; cluster-archetype contingency Cramér's V | n=16 builds with stat targets — small |
| 5 | Skill+gear co-occurrence forms recognizable composition signatures | Apriori market-basket | Lift; support; confidence | items pooled across builds; transactions = per-build itemsets |
| 6 | "[Skill]×[Class]×[Activity]" naming pattern is empirically prevalent | NLP tokenization + pattern-matching; one-proportion z-test (or exact binomial) against null=0.50 | Proportion + Wilson 95% CI | n=104 names |
| 7 | Investment-tier vocabulary canonicalizes cross-game | chi-square (game × investment_tier_label) | Cramér's V | depends on how many builds have investment-tier signal in available fields |
| 8 | Speedfarm ↔ Push binary is universal at all 4 games (variant-axis claim) | Per-game multinomial frequency over activity_focus; pairwise (speedfarm, push) presence/absence as binary universality test | Per-game presence-rate; pooled proportion | n=83 variants |

### Test-selection justifications

**Fisher's exact (Analysis 2) over chi-square**: when expected cell counts < 5 (which is the case for the 4×3 game × pattern_observed contingency — game=poe2 hybrid=3, single_axis_viable=0, expected counts well below 5 in several cells), Fisher's exact is the rigorous choice. Chi-square asymptotic p-values are unreliable under sparse cells.

**Spearman over Pearson (Analyses 1 + 3)**: the convergence_strength label is ordinal (STRONG > MODERATE > WEAK > NO), not interval; Spearman respects the ordinal structure without assuming linearity of intervals.

**Apriori over FP-Growth (Analysis 5)**: mlxtend's Apriori is sufficient at this scale; FP-Growth's memory advantage matters only at much larger transaction counts.

**Wilson interval over normal approximation (Analysis 6)**: at proportions far from 0.5 the Wilson interval has correct coverage even at n=100; normal approximation breaks down.

**Hierarchical clustering with Ward linkage (Analysis 4)**: Ward minimizes within-cluster variance; appropriate for the stat-target space where stats are continuous. Alternative KMeans was considered but requires pre-specifying k; hierarchical permits dendrogram inspection. The full distance matrix at n=16 is 16×16 = 256 cells — trivially small RAM. The R48-retirement RAM-awareness operational guideline about hierarchical clustering only matters at n>1000.

## 3. Data preparation steps

### 3.1 Per-analysis joins and null handling

**Analysis 1:**
- vocabulary_convergence direct query (37 rows; no joins needed for primary test).
- Supplement: builds JOIN build_activities ON build_id (inner join; activity_name × source_site contingency).
- Null handling: rows where activity_name IS NULL excluded; activity_layer NULL preserved (orthogonal field, not in primary chi-square).

**Analysis 2:**
- composite_archetype_assessment direct query.
- Null handling: rows where game IS NULL or pattern_observed IS NULL excluded.
- Verify: all 30 rows have game ∈ {poe, d4, poe2, le} and pattern_observed ∈ {composite_required, hybrid, single_axis_viable}.

**Analysis 3:**
- loot_substrate_vocabulary GROUP BY game, layer for per-game-per-layer counts.
- Shannon entropy H = -Σ p_i log p_i where p_i is the proportion of vocab entries at layer i for that game.
- Cross-reference per-game composite_required proportion from Analysis 2.
- Null handling: rows where game IS NULL or layer IS NULL excluded.

**Analysis 4:**
- build_stat_targets JOIN builds ON build_id (inner join; only builds-with-stats).
- Pivot: long-form (build × stat × value) → wide-form (build × stat_name columns).
- Null handling: stats not measured per-build = 0 in wide form (interpretation: "not targeted" not "targeted at zero" — methodological note). Z-score normalization per-stat column.
- Standardize stat_name vocabulary (`critical_strike_chance` vs `critical_hit_chance` are duplicates; will merge under canonical `crit_chance`).

**Analysis 5:**
- build_skills GROUP BY build_id (skill itemset per build).
- build_gear GROUP BY build_id (gear itemset per build).
- COMBINED: per build, the union of {skill:name, gear:name} as transaction.
- Null handling: builds with empty skills AND empty gear excluded.
- Item normalization: lowercase, strip whitespace, prefix with skill:/gear: to disambiguate same-named entries.

**Analysis 6:**
- builds.build_name direct query; optional join to build_summary for descriptors.
- Tokenization: lowercase, split on whitespace, strip punctuation.
- Pattern: (skill_token ∈ skill_vocab) × (class_token ∈ class_vocab) × (activity_token ∈ activity_vocab OR "Build"/"Endgame"/"Leveling"/"League Starter" suffix).
- skill_vocab built from build_skills.skill_name (distinct, lowercased).
- class_vocab built from builds.class_or_ascendancy (distinct, lowercased).
- activity_vocab built from build_activities.activity_name (distinct, lowercased) PLUS suffix-vocab {endgame, leveling, build, guide, league starter, starter}.

**Analysis 7:**
- builds + build_pros_cons + build_summary inspection for investment-tier vocabulary.
- The schema has no explicit `investment_tier` column; will pattern-match on tagline + summary text + pros/cons text for token matches against {extreme, low_budget, low, medium, mid, high, mageblood, mageblood_required, starter, budget}.
- This analysis is dependent on extractable signal; if signal is thin, will surface as UNCERTAIN with low-power explanation.

**Analysis 8:**
- build_variants.activity_focus distinct values per game (via JOIN builds ON build_id).
- Per-game presence/absence of {speedfarm, push} variants tested.
- "Universal at all 4 games" claim = both speedfarm AND push must appear in ≥1 variant for every game ∈ {d4, poe, poe2, le}.

### 3.2 Categorical encoding

- `pattern_observed` ordinal encoding: single_axis_viable=0, hybrid=1, composite_required=2 (for Spearman correlation against layer-count).
- `convergence_strength` ordinal encoding: NO=0, WEAK=1, MODERATE=2, STRONG=3.
- `game` left categorical (Fisher's exact).
- `source_site` left categorical (Cramér's V).

### 3.3 Per-source weighting consideration

The corpus is heavily Maxroll-weighted: 81/104 builds = 78%. PoE-Vault contributes 5/104 = 4.8%. This creates two methodological concerns:

1. **Pooled tests may reflect Maxroll editorial conventions rather than community-wide patterns.** For Analyses 1, 6, 7, 8 (which pool across sources), I will report BOTH pooled and per-source-conditional results. Where per-source-conditional reveals divergence > 20 percentage points, I will flag the pooled estimate as Maxroll-biased.
2. **Per-source-conditional tests on PoE-Vault have n=5** — too small for asymptotic chi-square. Per-source effects on PoE-Vault will be reported descriptively only.

This is the **principal methodological caveat of the corpus** and should color interpretation of all "STRONG convergence" claims that pool across sources.

## 4. Multiple-testing correction

**8 primary analyses; multiple sub-tests per analysis** (some analyses fire 2-4 statistical tests). Total expected test count: ~15-20 p-values.

**Choice: Benjamini-Hochberg FDR at q=0.10.**

Justification (gandalf design-steward review surface):
- Bonferroni (controls FWER at α=0.05; α_per_test ≈ 0.003 across 15 tests) is appropriate when ALL tests must be simultaneously correct (e.g., a regulatory submission). It is overly conservative for **exploratory empirical validation of qualitative claims**, where we expect several true effects and care about controlling the proportion of false discoveries among rejected nulls.
- Benjamini-Hochberg controls the expected False Discovery Rate (FDR) at q. At q=0.10, among rejected nulls, ≤10% are expected to be false discoveries.
- The synthesis verdict is exploratory; FDR matches the epistemic situation.

**Decision rule:** rank p-values ascending; reject H0 for p_(i) ≤ (i/m) × q where m = total tests, i = rank.

**Reported statistics per analysis:** raw p-value + BH-adjusted q-value + decision (significant at q=0.10 / not significant).

**Gandalf design-steward review surface:** if synthesis-verdict claims need to survive Bonferroni rigor (e.g., for canonical doc commit), I can re-report with Bonferroni overlay. Default = FDR.

## 5. Assumption tests and diagnostics

| Test | Assumption | Diagnostic | If violated |
|---|---|---|---|
| chi-square independence | expected cell counts ≥ 5 in ≥80% of cells | scipy.stats.chi2_contingency expected counts | switch to Fisher's exact (Analysis 2) or Monte Carlo p-value |
| Fisher's exact | none beyond categorical | n/a | n/a |
| Spearman ρ | monotonic relation | scatterplot + ρ magnitude | report ρ with caution if non-monotonic |
| Apriori | min support / min confidence calibrated to corpus | corpus transaction count | raise support floor if patterns are spurious-singleton |
| Hierarchical clustering | distance metric appropriate | dendrogram inspection + silhouette coefficient | report cluster instability if silhouette < 0.2 |
| One-proportion z-test (Analysis 6) | normal approximation for sample proportion | n*p ≥ 10 and n*(1-p) ≥ 10 | use exact binomial test |

## 6. Sample-size sufficiency assessment per analysis

| # | n | Sufficient for primary test? | Caveats |
|---|---|---|---|
| 1 | convergence: 37; activities: 64 | YES for chi-square asymptotic; CV needed for ordinal | per-source-conditional n<10 for some sites |
| 2 | 30 | YES for Fisher's exact; marginal for chi-square (expected cells small) | Fisher's exact required |
| 3 | 4 (games) | **NO** for inferential — descriptive only | n=4 explicitly disallows inferential generalization |
| 4 | 16 (builds-with-stats) | MARGINAL for clustering | wide CIs on silhouette; report as UNCERTAIN |
| 5 | ≤31 (builds-with-both-skills-and-gear) | MARGINAL for Apriori at support=0.05 | raise floor to support=0.10 if pattern count <5 |
| 6 | 104 | YES (sufficient for binomial test at n=104) | per-source conditional on PoE-Vault n=5 → descriptive only |
| 7 | depends on extractable signal | UNCERTAIN until signal extracted | will surface signal availability before test |
| 8 | 83 | YES for per-game presence; 4 games × ~20 variants each | universal-claim is a property of presence not magnitude |

## 7. Test-statistic reporting standard

Per-analysis findings doc reports for each test:
- Hypothesis being tested (H0 and H1)
- Test statistic name + value
- Degrees of freedom (where applicable)
- Raw p-value
- BH-adjusted q-value
- Effect size with 95% CI
- Sample-size-adequacy verdict
- Plain-language interpretation
- Composition with synthesis verdict claim (VALIDATES / REFUTES / UNCERTAIN)

## 8. Operational discipline composition

| Discipline | Application |
|---|---|
| **Disc #18 math hotspot consultation** | This brief surfaces methodology decisions § 1 for gandalf design-steward review before Task 2 |
| **Disc #19 background processes** | N/A for this dispatch (all analyses run in foreground; RAM-aware sequential per Matt 2026-05-29 evening late) |
| **Disc #42a framing-audit Q1-Q3** | Pre-registered hypotheses prevent post-hoc framing drift; per-source-conditional reporting prevents Maxroll-bias collapse |
| **Disc #45 vocabulary lock** | Stat names canonicalized (crit_chance unifies critical_hit_chance + critical_strike_chance) |
| **Disc retired R48 RAM-awareness** | Operational guidelines per dispatch RAM-section honored: sequential analyses; cursor.fetchmany not relevant at <1000 rows; del df + gc.collect between heavy stages; no transformer NLP for Analysis 6 |
| **Recognition → empirical validation → commit** | Recognition = gandalf synthesis verdict; empirical validation = this dispatch; commit = Cycle 15+ canonical inputs flagged in Task 2 findings doc |

## 9. Sign-off and gandalf review surface

**Authored:** elrond per Matt 2026-05-29 evening late single-batch elrond dispatch.

**For:** statistical methodology pre-registration that operationalizes R4 synthesis verdict qualitative claims as testable hypotheses with explicit sample-size diagnostics and multiple-testing correction.

**Gandalf design-steward review surface (Disc #18):**
1. FDR over Bonferroni — proposed; gandalf may overrule with Bonferroni
2. Cohen's kappa substituted by Spearman + chi-square per § 1 item (2)
3. n=16 Analysis 4 will be UNCERTAIN-flagged rather than VALIDATES/REFUTES
4. Analysis 5 min support 0.05 → 0.10 if joined corpus <50
5. Schema/code drift on composite_archetype_assessment flagged but not blocking

**Default behavior in absence of gandalf overrule:** proceed with proposed methods. Findings doc will explicitly cite this brief and any decisions taken.

**Next: Task 2 execution per this brief.**
