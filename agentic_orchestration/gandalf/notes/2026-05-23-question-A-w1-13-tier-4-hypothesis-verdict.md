# Question A — W1.13 + Tier 4 Build-Defining Hypothesis Test Verdict (Pattern A-deep)

> **STATUS:** CURRENT — gandalf verdict on Matt's Question A (raised 2026-05-23 morning interrupted session; companion verdict to Question B; authored 2026-05-23 evening after Phase E-2 spot-check). Pattern A-deep multi-question verdict authored at Matt direct invocation ("Path 1, author the verdict").

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct Pattern A-deep invocation
**Status:** **Design-spec-as-math.** Mathematical model + hypothesis test methodology framework + acceptance gates + decision tree + seam routing for Tier 4 build-defining-node mathematical scoping. Architectural commitments deferred per § 9 empirical-evidence criteria.
**Companion docs:**
- `canonical/00-ground-state.md` § 1 (current-truth oracle)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` (D1-D10)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-B-gear-armor-legendary-verdict.md` (Question B companion verdict — gear / armor / legendary class / combinatorial-strength testing)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4-A architecture; 1 signature + 1-3 secondary; rank-3 completer; hand-authored catalogue ~30-50)
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md` (W1.13 rescope; BDI/T4 alignment; dual-witness sim methodology; Surface A footnote)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (substrate-vector axes; BC convergence)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #18 methodology-before-execution; Discipline #1 math-before-code; Discipline #11 empirical-inspection)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (W1.13 + BDI + T4 lineage)
- `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5 (framing-audit checklist — applied to this verdict authoring per § 1.3 below)

---

## 0. TL;DR — top-line verdict

Matt's Question A contains four interlocking sub-questions about the mathematical scoping of Tier 4 build-defining nodes and the hypothesis-test framework needed to validate them. Top-line verdict per sub-question:

| Sub-question | Verdict |
|---|---|
| **A-1: Tier 4 build-defining node mathematical scope — how do we model "build-defining-ness" mathematically?** | **Build-defining-ness lives in an INTERACTION TERM, not an additive term.** Mathematical model: `kit_power = α·(class) + β·Σ(substrate_pairs) + γ·substrate_triple + δ·T4_node + η·(T4_node × substrate_triple) + ε`. The build-defining-ness IS the η coefficient. δ is decorative-additive; η is build-defining-multiplicative. A T4 node with η ≈ 0 (only δ contribution) is NOT build-defining — it's flavor. A T4 node with η > 0 (interaction with substrate-triple) IS build-defining. Plus two distribution-shape signatures (mode-shift on kit_power; differential effect across clusters). Three properties P1-P3 detailed in § 2. |
| **A-2: Whose seam?** | **Mathematical design-spec scoping = gandalf** (this verdict). **Hypothesis test execution = gamora** (engine simulation seam per AGENTS.md). **Tier 4 catalogue authoring = gandalf + Matt design call** (T4-B catalogue work; ~30-50 entries per T4-A § 4). **Methodology consultation = legolas Mode A** (required BEFORE gamora executes per Discipline #18 — interaction-term modeling + distribution-shape analysis are both math hotspots). **Critique-pair Gate-1 = gandalf + jack-ryan** (BLOCK authority on methodology). Detailed routing in § 3. |
| **A-3: Are hypothesis tests set appropriately to find synergistic multiplicity?** | **No — the existing BDI H1-H5 framework cannot detect multiplicity.** H1-H5 operate on linear-effect substrate-rank expression (γ-pair-vs-β-triple coefficient comparisons). Multiplicative interactions (η coefficient in the model above) are EXPLICITLY OUTSIDE the linear-effect model's scope. Need framework extension: proposed **H8 hypothesis** with three test methodologies (interaction-term ANOVA primary; substrate-triple-vs-pair-doubled comparison confirmatory; decision-tree variable importance tertiary). Methodology consultation via legolas Mode A required. Detailed in § 4. |
| **A-4: Are hypothesis tests set appropriately to find bimodal enhancement?** | **No — the existing BDI H1-H5 framework cannot detect bimodality.** H1-H5 measure mean and variance against build-input axes (unimodal-ish distribution assumption). A genuinely bimodal kit-power distribution ("build is off" vs "build is on") gets averaged into wider variance and appears as "noisy linear effect," not as "two distinct regimes." Need framework extension: proposed **H9 hypothesis** with three test methodologies (Hartigan's dip test as gate; GMM model selection if dip rejects; quantile-gap analysis for design interpretation). Methodology consultation via legolas Mode A required. Detailed in § 5. |

**Critical caveat (load-bearing for the whole verdict):** the extended hypothesis-test framework's viability is **conditional on W1.13 BDI H1-H5 baseline results from gamora.** If H1-H5 show non-significant linear effects (signal-to-noise too low), higher-order interaction tests cannot succeed either; methodology must adapt before H8/H9 fire. This verdict captures design-intent + recognition; the architectural commitments fire on substrate-led validation per § 9.

**Note on Question B intersection:** Question B's § 5 A/B paired sim methodology + BDI H6/H7 extension proposals operate within the SAME mathematical framework this verdict scopes. Where Question B is about named-mythological signature WR-band deltas (specific T4 catalogue content), this verdict is about the GENERAL mathematical model + hypothesis-test framework that validates T4 build-defining-ness regardless of catalogue content. The two verdicts compose: Question A's framework + Question B's named-mythological catalogue + ongoing T4-B catalogue authoring = complete v1 Tier 4 validation scope.

---

## 1. Question A verbatim + sub-question decomposition + framing-audit application

### 1.1 Question A — reconstructed from session context

The verbatim text of Question A was lost with Question B in the interrupted-session of 2026-05-23 11:05:57 EDT. Reconstructed from Matt's 2026-05-23 evening framing ("the skill and tier 4 build-defining node mathematical scoping; whose seam; are hypothesis tests set appropriately to find synergistic multiplicity/bimodal enhancement"):

> A) Skill and Tier 4 build-defining node mathematical scoping. How should we model build-defining-ness mathematically? Whose seam owns the work? Are the W1.13 hypothesis tests (BDI H1-H5) set appropriately to find synergistic multiplicity (multiplicative compound effects beyond additive substrate stacking) and bimodal enhancement (distribution-shape mode-shifts indicating "build is off" vs "build is on" regimes)?

### 1.2 Sub-question decomposition

- **A-1:** Mathematical scope — what's the math model for "build-defining-ness"?
- **A-2:** Seam routing — who owns mathematical scoping vs hypothesis test execution vs catalogue authoring vs methodology consultation?
- **A-3:** Synergistic multiplicity — are existing tests adequate? If not, what extension is needed?
- **A-4:** Bimodal enhancement — are existing tests adequate? If not, what extension is needed?

The four sub-questions are interlocking. A-1 (the math model) IS the substrate the hypothesis tests probe. A-3 + A-4 test specific properties of A-1. A-2 is the operational routing for executing A-1 + A-3 + A-4.

### 1.3 Framing-audit application (per addendum § 9.5)

**Q1: What load-bearing framing assumptions does this verdict depend on?**

1. **T4-A architecture is correct** — 1 signature + 1-3 secondary capstones; rank-3 completer; gear-anchored when signature_gear_archetype present; hand-authored catalogue ~30-50 entries
2. **BDI H1-H5 framework is the right base to extend** — linear-effect substrate-rank expression provides the baseline against which interaction terms are tested
3. **Engine simulation can produce kit-power measurements at sufficient sample size for higher-order statistical tests** (interaction-term ANOVA + Hartigan's dip + GMM selection all require N ≥ several hundred to several thousand kit samples per cell)
4. **Substrate-led discipline applies to methodology selection** — let the data vote on whether multiplicity/bimodality exists; don't pre-impose interpretive frame
5. **W1.13 rescope's dual-witness + Surface A footnote framework is intact** — the rescope didn't break anything load-bearing for hypothesis testing

**Q2: What evidence currently in hand could refute these assumptions?**

1. If W1.13 H1-H5 baseline results (gamora seam; status: unknown to this verdict; needs gamora confirmation) show non-significant linear effects, signal-to-noise may be too low for higher-order interaction tests to succeed. Refutation evidence: H1-H5 p-values + effect sizes from gamora.
2. If Phase E-2 cluster output (substrate-descriptive-only labels; coarse-spine k=3) shows weak weapon-form coherence per cluster, Tier 4 catalogue keyed to cluster identity may be premature. Refutation evidence: cluster-labeling spot-check (just completed — labels are honest but coarse; form-bundling vs prefix-bundling distinction emerged; Phase E-1.5 sensitivity sweep deferred).
3. If sample-size requirements for interaction-term ANOVA exceed engine simulation feasibility (e.g., need N=10,000 kit samples per substrate-triple × T4-node cross-product cell), methodology must adapt to bounded-sample-size variants (Bayesian model comparison; permutation tests; mixed-effects models).

**Q3: If refutation evidence exists or is plausible from current scope, refine the framing rather than execute the work as-framed?**

The framework as scoped in this verdict is **conditional on W1.13 H1-H5 baseline validation from gamora.** If H1-H5 succeed, the extended framework (H8 + H9 + differential-effect) is the right path. If H1-H5 fail or show degenerate behavior, methodology re-examination via legolas Mode A is the right next step BEFORE extending the framework. This verdict captures the conditional-extension structure rather than committing to unconditional execution.

The Phase E-2 cluster output's coarse-spine k=3 framing means Tier 4 catalogue authoring keyed to cluster identity should operate at coarse-spine resolution initially, with refinement following Phase E-1.5. This is a downstream consideration for T4-B catalogue work, not for this verdict's hypothesis-test framework — but worth flagging.

---

## 2. Sub-question A-1 — Tier 4 build-defining node mathematical scope

### 2.1 What "build-defining" means mathematically

A Tier 4 build-defining node is mathematically distinct from a "Tier 4 flavor signature" by exhibiting three properties simultaneously:

**P1 — Multiplicative interaction with substrate-triple effects.**

Adding a build-defining T4 node to a kit should produce kit_power_total **strictly greater than the sum** of individual contributions:

```
kit_power(class + substrate_triple + T4_node) > 
  kit_power(class + substrate_triple) + kit_power(class + T4_node) - kit_power(class alone)
```

If equality holds (within statistical tolerance), the T4 node is purely additive (decorative). If strict greater-than holds, the T4 node compounds with substrate-triple identity (build-defining).

This is the **multiplicity property**. Detection methodology in § 4.

**P2 — Mode-shifting effect on kit performance distribution.**

A build-defining T4 node should shift the kit's performance regime — moving from one performance-distribution mode to another. Mathematically:

```
distribution(kit_power | T4_node absent) is one shape
distribution(kit_power | T4_node present + matched substrate_triple) is a DIFFERENT shape
```

Where "different shape" means specifically: either bimodality emerges (split into "off-mode" + "on-mode") OR unimodal-mean-shift exceeds variance-of-distribution (the entire performance regime moves). The genre-canonical signature is **bimodality emerges** — without the build-defining node, the kit's distribution is unimodal (sometimes high, sometimes low, smooth distribution); WITH the node and matched substrate-triple, the distribution splits into "build broken" (player missed the synergy) vs "build working" (player landed it).

This is the **bimodality property**. Detection methodology in § 5.

**P3 — Differential effect across substrate-vector clusters.**

A build-defining T4 node tied to one substrate-cluster identity should produce **strong effects in matched-cluster kits** and **weak effects in unrelated-cluster kits.** Mathematically:

```
η_coefficient(T4_node × substrate_triple) >> η_coefficient(T4_node × non-matched substrate_triple)
```

If η is uniform across clusters, the T4 node isn't truly "build-defining" for any particular build — it's class-wide. The build-defining-ness REQUIRES substrate-anchoring.

This is the **differential-effect property**. Detection methodology in § 4.3.

### 2.2 The mathematical model

Putting all three properties into a unified model:

```
kit_power = α·(class) 
          + β·Σ(substrate_pairs) 
          + γ·substrate_triple 
          + δ·T4_node 
          + η·(T4_node × substrate_triple)  ← BUILD-DEFINING-NESS LIVES HERE
          + ε
```

Where:
- **α** = class baseline coefficient (existing BDI framework)
- **β** = substrate-pair coefficient vector (existing BDI framework; pair-rank-2 effects)
- **γ** = substrate-triple coefficient (existing BDI framework; rank-3 substrate-richness effect)
- **δ** = T4-node additive coefficient (the decorative-flavor contribution; what a non-build-defining T4 node would have)
- **η** = T4-node × substrate-triple interaction coefficient (the build-defining-multiplicative contribution; the load-bearing term for build-defining-ness)
- **ε** = residual variance

The existing BDI H1-H5 hypothesis tests measure α, β, γ. They do NOT measure δ or η independently, nor do they distinguish between δ-only contribution (decorative) and (δ + η)-contribution (build-defining).

**Build-defining-ness null hypothesis:**
```
H_null: η = 0 (T4 node is purely additive; decorative flavor only)
```

**Build-defining-ness alternative hypothesis:**
```
H_alt: η > 0 AND η produces measurable mode-shift in kit_power distribution AND 
       η is differential across substrate clusters
```

The three conjunctive conditions in H_alt map to P1 (multiplicity), P2 (bimodality), P3 (differential).

### 2.3 What this model does NOT cover (out-of-scope deferrals)

- **Higher-order interactions** (T4 × T4 between multiple T4 nodes; or T4 × substrate-pair beyond triple). v1 model assumes one T4 signature per kit (per T4-A § 2). If T4 signature + secondary capstone interactions become relevant at v1.1+, the model extends.
- **Non-parametric effects** (T4 effects that don't fit linear-coefficient framing — e.g., regime-changes that introduce new mechanics entirely). The η-coefficient framing captures "compound damage scaling" cleanly; it captures "ability behavior fundamentally changes" only as a linear approximation. Some T4 mechanics (per T4-A § 3.3 examples) genuinely change kit behavior in ways the linear model approximates rather than describes. Hartigan's dip + GMM in § 5 partially compensate by surfacing non-linearity through distribution shape.
- **Temporal dynamics** (T4 effects that scale with fight duration, resource accumulation, or combo state). The v1 model treats kit_power as a single scalar; temporal-dynamics work is downstream.

These limitations are acknowledged. The model is **load-bearing for v1 Tier 4 validation**, not terminal.

---

## 3. Sub-question A-2 — Seam routing

Per Discipline #18 mathematical-layer routing + AGENTS.md seam definitions:

| Sub-task | Seam | Notes |
|---|---|---|
| **Mathematical design-spec scoping** (this verdict — the model + hypothesis statements + acceptance criteria) | **Gandalf** (story-and-design steward; design-spec-as-math owns) | Discipline #18 § 3.2 — design-spec-as-math lives at gandalf |
| **Hypothesis test execution** (run sims; measure α/β/γ/δ/η; statistical analysis; produce test results) | **Gamora** (engine simulation seam) | AGENTS.md — simulation/balance loop/BDI hypothesis tests gamora territory; gamora consumes this verdict as execution spec |
| **Methodology consultation at math hotspot** (which interaction-term model? which bimodality test? which sample-size criteria?) | **Legolas Mode A** (analytical research) | Discipline #18 — methodology selection at math hotspots requires legolas Mode A BEFORE specialist execution; interaction-term modeling + distribution-shape analysis are both math hotspots |
| **Critique-pair Gate-1 on methodology** | **Gandalf (design) + jack-ryan (process)** | Critique-pair gate protocol; BLOCK authority if methodology unsound; ratifies legolas Mode A output before gamora executes |
| **Tier 4 catalogue authoring** (the specific build-defining-node entries — names, regime-change mechanics, sim-viability flags; ~30-50 v1 entries per T4-A § 4) | **Gandalf + Matt design call** | T4-A § 3.3 workflow; gandalf authors design-intent + cohesion-judge naming; Matt approves architectural commitments; rocket implements sim-viability flag checks |
| **Sim-viability flag execution** (per T4-A § 3.3 step 5; rocket runs sim-viability check per catalogue entry; jack-ryan Gate-2 reviews) | **Rocket + Jack-ryan** | T4-A § 3.3 workflow |
| **Decisions-log entries** (when architectural commitments fire per § 9 empirical-evidence criteria) | **Jack-ryan** (decisions-log writing authority per AGENTS.md) | Other agents propose entries via knight-rider routing; jack-ryan writes canonical entries |
| **Cross-seam handoff documentation** (MIGRATION.md per ADR-004 when work-units cross seams) | **Owner of producing-seam** | Per ADR-004; gandalf produces this verdict; downstream seam consumers cite via MIGRATION.md |

### 3.1 Execution sequence (work-unit shape)

```
Gandalf authors this verdict (DONE) 
    ↓
Knight-rider routes to legolas Mode A for methodology consultation
    ↓
Legolas Mode A consultation produces methodology recommendations
    (interaction-term ANOVA implementation; Hartigan's dip + GMM 
     implementation; sample-size analysis)
    ↓
Critique-pair Gate-1: gandalf + jack-ryan review methodology
    (BLOCK authority on methodology unsoundness)
    ↓ PASS
Knight-rider routes to gamora for execution dispatch
    ↓
Gamora executes H8 + H9 + differential-effect tests against v1 T4 
    catalogue (T4-B work — separate prerequisite track)
    ↓
Critique-pair Gate-2: gandalf + jack-ryan review results
    (BLOCK authority on result interpretation)
    ↓ PASS
Decisions-log entries proposed; Matt approves architectural locks
```

### 3.2 Prerequisite dependencies

- **W1.13 H1-H5 baseline results from gamora** must be available before H8/H9 fire (per § 1.3 framing-audit Q2 #1)
- **T4-B v1 catalogue (~30-50 entries)** must be authored before H8/H9 have specific T4_node values to test against (T4-A § 3.3 workflow; gandalf + Matt design call)
- **Phase E-2 cluster output landed** (current state: labels authored; awaiting jack-ryan Gate-2 ratification; DB UPDATE queued); T4-B catalogue keys to cluster identity at coarse-spine k=3 resolution per Phase E-2 acceptance

### 3.3 Discipline #18 routing — math hotspots in this work

Both H8 (interaction-term modeling) and H9 (distribution-shape analysis) are math hotspots. Legolas Mode A consultation is **mandatory before gamora executes**, not optional. The consultation must cover:

- **Interaction-term ANOVA implementation** (sklearn vs statsmodels vs custom; sample-size requirements per cell; multiple-comparison correction; effect-size metrics)
- **Hartigan's dip test implementation** (`diptest` Python package; alternative implementations; p-value interpretation at sample-size scales we'll have)
- **GMM model selection** (BIC vs AIC vs cross-validation; covariance structures; identifiability concerns at small sample sizes)
- **Differential-effect testing** (interaction-term comparison across substrate-cluster cells; effect-size threshold for "significantly larger")
- **Sample-size analysis** (does engine simulation produce sufficient kit_power samples at the substrate × T4 cross-product scale? if not, what bounded-sample methodologies adapt?)

---

## 4. Sub-question A-3 — Synergistic multiplicity hypothesis tests

### 4.1 What the existing H1-H5 framework covers (and doesn't)

Per W1.13 rescope-disposition § 3 (BDI/T4 alignment) + decisions-log W1.13 entries, BDI H1-H5 tests target:

- H1-H3: **Linear-effect substrate-rank expression** — does rank-3 substrate-triple produce measurably larger kit-power effect than rank-2 substrate-pair than rank-1 single-substrate?
- H4: **Coefficient dominance** — does γ (rank-3 coefficient) dominate β (rank-2 coefficient) sum across substrate-pairs?
- H5: **Substrate-triple expression at sim scale** — does the rank-3 effect hold up against random-baseline kits at large sample sizes?

**These tests operate on linear-effect additive models.** They CANNOT detect:

- Multiplicative interactions between T4 node and substrate-triple (η coefficient is outside the model)
- Compound-effect signatures where two synergies produce > sum of individual contributions
- Triple-synergy regime changes where adding the third element transforms the kit's identity

H1-H5 measure the substrate-rank expression of kit-power. They don't measure whether T4 nodes amplify that expression multiplicatively.

### 4.2 Proposed H8 hypothesis

```
H8 (build-defining-multiplicity hypothesis):
    The interaction-term coefficient η in the model
        kit_power = α·class + β·Σ(pairs) + γ·triple + δ·T4 + η·(T4 × triple) + ε
    is significantly different from zero (p < 0.05) AND of meaningful effect size 
    (Cohen's d > 0.5 OR partial η² > 0.06) when:
        - The T4 node is hand-authored as "build-defining" per T4-A § 3.3
        - The substrate-triple matches the T4 node's substrate-anchoring per the catalogue entry
    
    Null hypothesis (H8_null): η = 0 — T4 nodes are purely additive (decorative)
    Alternative hypothesis (H8_alt): η > 0 with meaningful effect size — T4 nodes 
        are multiplicatively build-defining at the substrate-triple intersection
```

### 4.3 Test methodologies (3 candidates; legolas Mode A consultation selects primary)

| Method | What it measures | Detection sensitivity | Recommended role |
|---|---|---|---|
| **Interaction-term ANOVA** | Fits main-effects (α, β, γ, δ) + interaction-term (η) model on kit_power; F-test on interaction-term significance; partial η² effect size | Detects pairwise/triplewise interactions explicitly; clean p-value framing; sample-size requirements are calculable | **PRIMARY** — clean statistical rigor; cited heavily in design-spec-as-math literature; gamora can execute via statsmodels |
| **Substrate-triple-vs-pair-doubled comparison** | Direct empirical test: kit_power(triple_ABC + T4) vs kit_power(pair_AB + T4) + kit_power(pair_BC + T4) − kit_power(single_B + T4); positive value = multiplicity | Intuitive design language; surfaces the multiplicity in build terms; less statistical rigor than ANOVA | **CONFIRMATORY** — gives intuitive interpretation of what ANOVA's η coefficient MEANS in build-design language |
| **Decision-tree variable importance** | Tree-based methods (gradient boosting / random forest) naturally capture multiplicative interactions; feature importance ranks combinations vs singletons | Detects high-order interactions including triple+ interactions; harder to interpret which specific synergies are firing; black-box | **TERTIARY** — useful if H8 fails to detect ANOVA-modeled multiplicity; surfaces whether multiplicity exists in higher-order structure the linear model misses |

### 4.4 Differential-effect gate (P3 from § 2.1)

H8 alone tests whether the interaction-term is significant across all kits with T4 node + matched substrate-triple. It does NOT test whether the interaction is **DIFFERENTIAL** across substrate-cluster cells.

Proposed extension to H8 — **H8.diff:**

```
H8.diff (differential-effect hypothesis):
    The interaction-term coefficient η is significantly LARGER in kits where 
    T4 node matches the substrate-triple identity than in kits where T4 node 
    is "off-anchor" (T4 present but substrate-triple is unrelated).
    
    Operationalization: split kit_power samples into "matched" (T4_node matches 
    substrate-triple per catalogue entry) and "non-matched" (T4_node present but 
    substrate-triple unrelated). Compute η coefficient in each split. Test for 
    significant difference between η_matched and η_non_matched (e.g., bootstrap 
    confidence intervals; permutation test on the difference).
    
    Null hypothesis (H8.diff_null): η_matched = η_non_matched
        — T4 node's multiplicative effect is uniform across substrate-cluster 
          cells (T4 isn't substrate-anchored; class-wide effect)
    Alternative hypothesis (H8.diff_alt): η_matched > η_non_matched with 
        meaningful effect size
        — T4 node's multiplicative effect is substrate-anchored (build-defining 
          for the SPECIFIC build identity, not class-wide)
```

H8 + H8.diff together test P1 + P3 from § 2.1 (multiplicity + differential).

### 4.5 Why all three methodologies (not just ANOVA)

ANOVA gives statistical rigor (p-value on η; partial η² effect size). But interpretation in design terms requires the substrate-triple-vs-pair comparison ("what does this MEAN for what the player feels?"). And decision-tree provides empirical cross-check ("if ANOVA fails to detect multiplicity but the data clearly has compound structure, decision-tree variable importance will surface it").

The combination provides:
- **Statistical pillar** (ANOVA — H8 passes/fails with rigor)
- **Design-language pillar** (substrate-triple-vs-pair-doubled — what the multiplicity FEELS like)
- **Robustness pillar** (decision-tree — catches multiplicity ANOVA misses)

Legolas Mode A consultation selects which combination is feasible at the sample sizes engine simulation can produce.

### 4.6 Math hotspot — Discipline #18 requirements

H8 + H8.diff are math hotspots. Legolas Mode A methodology consultation is mandatory BEFORE gamora executes. Specific consultation scope:

- Sample-size requirements per substrate-triple × T4-node cell for ANOVA to detect η with adequate power (target: 80% power at α=0.05 for Cohen's d=0.5)
- Multiple-comparison correction protocol (Bonferroni? FDR?) given the ~30-50 v1 catalogue entries each testing H8 + H8.diff
- Implementation library selection (statsmodels OLS with interaction terms vs sklearn LinearRegression with polynomial features vs explicit interaction-design-matrix construction)
- Alternative methodologies if sample-size is insufficient (mixed-effects models; Bayesian model comparison; permutation tests)

---

## 5. Sub-question A-4 — Bimodal enhancement hypothesis tests

### 5.1 What bimodal enhancement means in genre context

Per ARPG genre canon, build-defining mechanics produce **bimodal kit-power distributions**:

- **"Build is off" mode** — the kit without the build-defining synergy operating; performance distribution clustered at a lower kit-power range
- **"Build is on" mode** — the kit with the build-defining synergy operating; performance distribution clustered at a higher kit-power range
- **Gap between modes** — the build-defining-ness IS the gap

Genre-canonical examples:
- **Diablo 2** — Enigma rune word: builds without it are unviable for endgame; builds with it are strong. Bimodal kit_power distribution: no-Enigma vs Enigma.
- **Path of Exile** — Mjolner build (Mjolner unique mace + Cast on Crit support gems + specific skill choices): without the unique, the build is non-functional; with it + the supporting items, the build deletes content. Bimodal distribution.
- **Last Epoch** — unique-anchored builds (Apostate's Mantle for warlock; Shattered Lance for paladin; etc.): build-defining uniques flip the kit from "decorative" to "regime-shifting."
- **Lost Ark** — class-engraving builds (Hit Master engraving for damage classes): engraving present or absent determines build viability.

In each case, the player's **moment of recognition** is "I found my build's key item" — the moment when the kit flips from off-mode to on-mode. This is the player-experience signature that makes ARPG itemization economically meaningful.

If a Reincarnated Tier 4 build-defining node doesn't produce bimodal enhancement, the build-defining-ness is invisible to the player. The kit gets stronger smoothly with investment; there's no "I found it" moment. The genre-canonical depth experience is missing.

### 5.2 What the existing H1-H5 framework covers (and doesn't) — distribution-shape

Per W1.13 rescope + BDI documentation, H1-H5 measure:
- Mean kit-power
- Variance of kit-power
- Linear coefficient relationships

These statistics ASSUME unimodal-ish distribution. A genuinely bimodal distribution gets averaged into:
- A mean that's intermediate between the two modes (artifactual — corresponds to no actual kit)
- A variance that's much wider than either mode's variance (artifactual — hides the true distribution shape)

The framework reports these as "noisy linear effect" or "high-variance regime." It does NOT report them as "two distinct modes." H1-H5 cannot distinguish bimodality from large-variance unimodality.

### 5.3 Proposed H9 hypothesis

```
H9 (bimodal-enhancement hypothesis):
    The kit_power distribution for kits where T4 build-defining node is present 
    AND matches the substrate-triple identity exhibits significant non-unimodal 
    structure (Hartigan's dip test rejects unimodality at p < 0.05) OR 
    Gaussian-mixture model selection identifies ≥ 2 components via BIC/AIC.
    
    Null hypothesis (H9_null): kit_power distribution is unimodal — T4 node 
        contribution is smooth/additive within distribution
    Alternative hypothesis (H9_alt): kit_power distribution is non-unimodal — 
        T4 node creates regime-shift in distribution shape (genre-canonical 
        build-defining signature)
```

### 5.4 Test methodologies (3 candidates; legolas Mode A consultation selects primary)

| Method | What it measures | Detection sensitivity | Recommended role |
|---|---|---|---|
| **Hartigan's dip test** | Tests unimodality directly; null hypothesis = unimodal; rejection = ≥bimodal (no commitment to specific mode count) | Statistically rigorous; specific to detecting non-unimodality; well-established library implementation (`diptest`) | **PRIMARY GATE** — does bimodality exist? Sharp yes/no answer |
| **Gaussian-mixture model selection** | Fits 1-component vs k-component GMM; selects k via BIC/AIC | Identifies number of modes; gives mode means/variances/weights for design interpretation; assumes Gaussian component shape | **CHARACTERIZATION** — fires if Hartigan rejects; tells us HOW MANY modes and WHERE they sit |
| **Quantile-gap analysis** | Examines whether high-percentile and low-percentile distributions differ in shape/variance, not just magnitude | Operationally simpler than GMM; surfaces "broken build vs working build" pattern directly; less statistically rigorous but more interpretable in design language | **DESIGN INTERPRETATION** — fires after Hartigan + GMM; translates statistical bimodality into design-language ("the build's off-mode is at kit_power=X; on-mode is at kit_power=Y; gap is Z") |

### 5.5 Why all three methodologies

Hartigan's dip gives the gate ("is bimodality present at all?"). GMM gives the characterization ("how many modes; where?"). Quantile-gap gives the design interpretation ("what does it MEAN for player experience?"). Together they answer:

1. Does the T4 node produce non-unimodal distribution? (Hartigan)
2. If yes, how many modes and where? (GMM)
3. What's the design-significance of the modes? (Quantile-gap)

A T4 node that passes (1) but produces 5 modes (per GMM) isn't doing build-defining work — it's noisy. A T4 node that passes (1) with 2 modes (per GMM) where the gap is small (per quantile-gap) isn't doing strong build-defining work — it's flavor with mild mode-shift. A T4 node that passes (1) with 2 modes and the gap is large IS doing genre-canonical build-defining work.

### 5.6 Mode-separation effect-size threshold

For bimodality to be design-significant (not just statistically detectable), the modes need to be **separated enough that the player can distinguish them.** Proposed threshold:

```
Mode separation effect size ≥ 0.5 × (off-mode mean kit_power)
    — the on-mode mean is at least 1.5× the off-mode mean kit_power
```

This is a tunable threshold. Legolas Mode A consultation should validate against genre canon (what's the actual mode-separation ratio in D2 Enigma builds vs no-Enigma? In PoE Mjolner vs no-Mjolner? In Last Epoch unique-anchored builds?). The threshold should align with what genre players empirically experience as "build-defining."

### 5.7 Math hotspot — Discipline #18 requirements

H9 is a math hotspot. Legolas Mode A consultation mandatory BEFORE gamora executes. Specific consultation scope:

- Hartigan's dip test implementation (`diptest` Python package; alternative implementations; p-value calibration at sample sizes ≥1000)
- GMM model selection criteria (BIC vs AIC vs cross-validation; covariance type — full vs diagonal vs spherical vs tied; identifiability concerns)
- Quantile-gap implementation (5th-95th percentile gap; 10th-90th; alternatives)
- Mode-separation effect-size threshold validation against genre-canon
- Sample-size requirements for reliable bimodality detection (Hartigan needs N≥500 for adequate power per standard literature)

---

## 6. How synergistic multiplicity + bimodal enhancement interact

Both patterns can co-exist — and SHOULD co-exist for genre-canonical Tier 4 build-defining work:

| Multiplicity (H8) | Bimodality (H9) | Interpretation |
|---|---|---|
| ✅ PASS | ✅ PASS | **Genre-canonical build-defining T4 node.** The interaction-term compounds AND the distribution mode-shifts. Player experiences both the synergistic depth AND the "build is on" recognition moment. |
| ✅ PASS | ❌ FAIL | **Additive-strong but not regime-shifting.** T4 node adds linear value compounded with substrate-triple, but doesn't gate the kit's identity. Solid signature but not regime-defining; consider demoting to Tier 3 OR revising for stronger interaction effects. |
| ❌ FAIL | ✅ PASS | **Bimodal for non-multiplicative reasons.** Distribution has two modes but the interaction-term doesn't fire — could be RNG-driven (some procs activate the on-mode), could be other categorical effect. T4 isn't substrate-anchored; re-examine anchoring or move T4's identity elsewhere. |
| ❌ FAIL | ❌ FAIL | **Decorative.** No multiplicity, no mode-shift. T4 node is flavor signature; not build-defining at all. Demote, revise, or remove from catalogue. |

Plus the differential-effect gate (H8.diff):

| H8.diff | Interpretation |
|---|---|
| ✅ PASS | T4 node's effect is **substrate-anchored** — strong in matched-cluster kits, weak in unrelated-cluster kits. Build-defining for the SPECIFIC build identity. |
| ❌ FAIL | T4 node's effect is **class-wide** — uniform across substrate-cluster cells. Not truly "build-defining" for any particular build; consider re-anchoring or accepting as class-baseline signature. |

### 6.1 The full per-entry acceptance matrix

For each Tier 4 build-defining-node entry in the v1 catalogue:

| Gate | Pass criterion |
|---|---|
| **G1 — Multiplicity (H8)** | η coefficient p-value < 0.05 AND effect size (Cohen's d > 0.5 OR partial η² > 0.06) in matched-substrate-triple kits |
| **G2 — Bimodality (H9)** | Hartigan's dip test rejects unimodality (p < 0.05) for matched-substrate-triple kits with T4 node present, AND GMM 2-component selected over 1-component via BIC |
| **G3 — Mode separation** | On-mode mean ≥ 1.5× off-mode mean kit_power (or threshold per legolas Mode A consultation) |
| **G4 — Differential effect (H8.diff)** | η_matched significantly larger than η_non_matched (bootstrap CI; permutation test) |

**Pass-all-gates**: T4 entry validated; folds into v1 catalogue locked.
**Pass-3-of-4**: T4 entry flagged for design review; possible revision.
**Pass-≤2**: T4 entry not doing build-defining work; demote to Tier 3 OR remove from catalogue OR revise for next iteration.

---

## 7. Cross-references to existing canon this verdict integrates

### 7.1 Canon this verdict preserves unchanged

- **T4-A architecture** (`canonical/story/tier-4-architecture-defaults-2026-05-22.md`): 1 signature + 1-3 secondary, hand-authored catalogue, gear-anchored signature, T4-A → T4-E phasing. This verdict provides the math model + acceptance gates that validate T4-A's "build-defining-ness" claim empirically.
- **W1.13 rescope-disposition** (`canonical/story/w1-13-rescope-disposition-2026-05-22.md`): dual-witness sim methodology; Surface A footnote; BDI/T4 alignment preservation. This verdict extends BDI H1-H5 with H8 + H9 + H8.diff without amending W1.13's existing structure.
- **BDI hypothesis test framework** (in-flight gamora work): H1-H5 remain the baseline. H8 + H9 + H8.diff are EXTENSIONS, not replacements. Prerequisite that H1-H5 baseline lands first.
- **Discipline #18 mathematical-layer routing** (`engineering-disciplines.md`): methodology consultation at math hotspots; legolas Mode A required before specialist execution.
- **Substrate-led discipline** (`canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`): let data vote on whether multiplicity/bimodality exists; don't pre-impose interpretive frame. The acceptance gates fire on empirical evidence, not on pre-commitment to "T4 must work because we said so."

### 7.2 Canon this verdict augments (proposes addition)

- **BDI hypothesis test framework**: proposed extension H8 (multiplicity) + H8.diff (differential-effect) + H9 (bimodality). Specific test methodologies named with primary/confirmatory/tertiary roles. Methodology consultation via legolas Mode A required.
- **T4-A § 3.3 workflow**: catalogue authorship workflow now includes G1-G4 gates per § 6.1 above. Each catalogue entry receives multiplicity-pass / bimodality-pass / mode-separation-pass / differential-pass flags before lock.
- **Discipline-candidate amendment** (for jack-ryan's queue): "Hypothesis-test framework extensions at math hotspots must include EFFECT-SIZE thresholds, not just p-value thresholds, before being scoped as load-bearing." Companion to Discipline #18's methodology-before-execution.

### 7.3 Decisions-log entries to propose (post-empirical-validation)

When § 9 empirical gates fire clean, the following decisions-log entries are warranted (jack-ryan owns writing):

- "Adopt interaction-term ANOVA + Hartigan's dip + GMM as canonical hypothesis-test framework for Tier 4 build-defining-node validation; extends BDI H1-H5 with H8 + H8.diff + H9; methodology consultation via legolas Mode A required per Discipline #18"
- "Adopt G1-G4 acceptance gates per § 6.1 as v1 Tier 4 catalogue lock criteria"
- "Adopt mode-separation effect-size threshold of [N×] off-mode mean kit_power as bimodality design-significance criterion (specific value pending legolas Mode A genre-canon validation)"

### 7.4 Question B intersection

- **Question B § 5.5 BDI H6/H7 extension** (named-mythological rank-3 γ-dominance) operates within H1-H5 linear-effect framework. H6/H7 extend to named-mythological-substrate-vector intersection.
- **This verdict's H8 + H9 + H8.diff** operate on the same mathematical model but test DIFFERENT properties (multiplicity + bimodality + differential, vs Question B's substrate-rank dominance).
- **They compose**: Question B's H6/H7 validates that named-mythological signatures EXPRESS at rank-3 substrate-richness; this verdict's H8 + H9 + H8.diff validates that named-mythological signatures (and substrate-only signatures) are BUILD-DEFINING (multiplicative + bimodal + differential).
- Together they form the complete v1 Tier 4 validation scope.

---

## 8. Ranked recommendation tier table

Per Pattern A-deep spec, explicit ranking:

| Tier | Path | Rationale | Sequence |
|---|---|---|---|
| **Tier 1 (must-fire; load-bearing for v1 T4 validation)** | Mathematical model per § 2.2 (η coefficient + interaction term) | Discipline-#18 design-spec-as-math; build-defining-ness has no clean mathematical home without it | Now (this verdict captures); referenced by all downstream work |
| **Tier 1 (must-fire; load-bearing for v1 T4 validation)** | H8 + H8.diff hypothesis tests (multiplicity + differential) per § 4 | Discipline-#11 empirical-inspection over assumption; without H8 + H8.diff, T4 build-defining claim is unvalidated | Post-W1.13 H1-H5 baseline + legolas Mode A methodology consultation + critique-pair Gate-1 |
| **Tier 1 (must-fire; load-bearing for v1 T4 validation)** | H9 hypothesis test (bimodality) per § 5 | Genre-canonical build-defining signature requires bimodal mode-shift; without H9, build-defining "feel" is unvalidated | Post-W1.13 H1-H5 baseline + legolas Mode A methodology consultation + critique-pair Gate-1 |
| **Tier 1 (must-fire; load-bearing for v1 T4 validation)** | G1-G4 acceptance gates per § 6.1 | Without per-entry pass/fail criteria, T4 catalogue authoring has no validation discipline | Applied during T4-B catalogue authorship workflow |
| **Tier 2 (primary methodology; legolas Mode A selects)** | Interaction-term ANOVA (H8 primary) + Hartigan's dip + GMM (H9 primary) | Statistical rigor + standard literature implementations | Legolas Mode A consultation outcome |
| **Tier 2 (confirmatory methodology)** | Substrate-triple-vs-pair-doubled comparison (H8 confirmatory) + quantile-gap analysis (H9 design-interpretation) | Design-language interpretation of statistical results | Legolas Mode A consultation outcome |
| **Tier 3 (tertiary methodology; robustness)** | Decision-tree variable importance (H8 robustness check) | Catches multiplicity ANOVA misses; black-box but useful | Fires if H8 ANOVA fails to detect but data suggests multiplicity exists |
| **Reserve** | Alternative methodologies — mixed-effects models, Bayesian model comparison, permutation tests | Backup if standard methodologies hit sample-size or identifiability issues | Legolas Mode A consultation surfaces if needed |
| **Reject** | Pure linear-effect testing (H1-H5 framework alone) | Cannot detect multiplicity (η outside model) or bimodality (distribution-shape outside scope) | Empirically refuted by sub-questions A-3 + A-4 |
| **Reject** | Pre-imposed "T4 is build-defining because we said so" without empirical validation | Substrate-led discipline violation; same shape as retired Pattern 4-5-6 | Do not pursue |

---

## 9. Empirical-evidence criteria for re-engagement + architectural commitment

Per OP § 3.4 recognition-validate-commit + substrate-led discipline:

| Verdict element | Empirical-evidence criterion to fire architectural lock |
|---|---|
| § 2 mathematical model (η coefficient as build-defining-ness home) | W1.13 BDI H1-H5 baseline results land from gamora; α/β/γ/δ coefficients measurable at engine simulation scale; signal-to-noise sufficient for interaction-term ANOVA per legolas Mode A consultation |
| § 4 H8 + H8.diff hypothesis tests | Legolas Mode A consultation completes; critique-pair Gate-1 ratifies methodology; gamora executes against v1 T4-B catalogue entries; results per § 6.1 G1 + G4 gates measured |
| § 5 H9 hypothesis test | Legolas Mode A consultation completes; critique-pair Gate-1 ratifies methodology; gamora executes against v1 T4-B catalogue entries; results per § 6.1 G2 + G3 gates measured; mode-separation effect-size threshold validated against genre canon |
| § 6.1 G1-G4 acceptance gates | Each v1 T4-B catalogue entry receives explicit pass/fail flags before catalogue locks; entries failing ≥2 gates revised, demoted, or removed |
| Decisions-log entries per § 7.3 | All gates fire clean; Matt approves architectural locks; jack-ryan writes canonical entries |

**Architectural lock criterion (binding for the whole verdict):** when § 9 gates above fire clean, this verdict's design-spec-as-math upgrades from "recognition + design intent" to "load-bearing canon for v1 Tier 4 validation." Status updates from "recognition" to "validated framework."

**If H1-H5 baseline fails (signal-to-noise too low for higher-order tests):** methodology re-examination via legolas Mode A is the next step BEFORE H8/H9 fire. Possible adaptations:
- Bounded-sample-size variants (Bayesian; permutation tests)
- Engine-simulation sample-size scaling (run more sims per condition)
- Methodology refinement (different model specification; different effect-size metrics)

The verdict's mathematical model + acceptance gates structure persists; the specific methodology adapts to engine-simulation reality.

---

## 10. What this verdict explicitly does NOT touch

Surface-level discipline — preventing scope creep:

- **Specific Tier 4 catalogue contents** (which build-defining nodes exist; their regime-change mechanics; their substrate-anchoring per cluster). T4-B catalogue authorship workflow per T4-A § 3.3; gandalf + Matt design call; separate from this verdict.
- **W1.13 H1-H5 baseline execution** (gamora seam; already in flight or queued separately; prerequisite for H8/H9 to fire).
- **Phase E-2 cluster output details** (substrate-descriptive-only labels per spot-check just completed; T4-B catalogue will key to cluster identity at coarse-spine k=3 resolution; refinement post-Phase-E-1.5 sensitivity sweep).
- **Cultural-aesthetic mapping question** (separate Pattern B sustained dialogue; tonight surfaced as deferred work; not in this verdict).
- **Earth-Self vs Spirit-Form naming architecture** (separate territory surfaced tonight; not in scope).
- **Higher-order interactions** (T4 × T4 between multiple T4 nodes; T4 × substrate-pair beyond triple); v1 model assumes one T4 signature per kit.
- **Non-parametric T4 effects** (T4 mechanics that don't fit linear-coefficient framing — regime-changes introducing new mechanics entirely); v1 model approximates these; not designed to fully model them.
- **Temporal dynamics** (T4 effects scaling with fight duration, resource accumulation, combo state); v1 model treats kit_power as scalar.
- **Synergy multiplicity beyond v1** (e.g., engine v1.1+ Tier 5 super-signatures, cross-class synergies, season-specific modifiers); not in scope.

---

## 11. Sign-off

**Author:** gandalf (story-and-design steward)
**Pattern:** Pattern A-deep verdict per OP § 2 (multi-question; multi-page reasoning; per-sub-question assessment; explicit ranked recommendation; anchor-doc citations by section)
**Authority for the verdict:** Matt 2026-05-23 direct invocation ("Path 1, author the verdict")
**Authority for architectural lock:** **Deferred** per § 9 empirical-evidence criteria. This verdict captures design-intent + recognition; the architectural commitments fire on substrate-led validation (W1.13 H1-H5 baseline + legolas Mode A consultation + critique-pair Gate-1 + gamora execution + G1-G4 per-entry gates).
**Framing-audit applied:** § 1.3 — three load-bearing assumptions identified; refutation evidence enumerated; conditional-extension structure adopted rather than unconditional execution commitment.
**Co-attestation:** none required at this layer (verdict, not decisions-log entry). When § 9 gates fire clean, jack-ryan writes decisions-log entries per § 7.3.
**Companion verdicts:**
- `2026-05-23-question-B-gear-armor-legendary-verdict.md` (gear / armor / legendary class / combinatorial-strength testing — companion at the named-mythological-binding layer)

---

**Signed:** gandalf
**For:** the design-side verdict on Matt's Question A (skill + Tier 4 build-defining node mathematical scoping + seam routing + hypothesis-test framework extension for synergistic multiplicity + bimodal enhancement). Authored 2026-05-23 evening per Pattern A-deep discipline. Closes the "engage both, pattern A-deep" companion-verdict pair (Question B authored 2026-05-23 11:37 EDT; Question A this verdict).
