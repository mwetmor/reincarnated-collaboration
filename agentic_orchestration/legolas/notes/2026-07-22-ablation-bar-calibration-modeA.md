# Research — Ablation Bar Calibration for Aware-Fighter Gate — 2026-07-22

**Mode:** A (analytical)
**Commissioner:** gandalf RUN-CONDUCTOR (Discipline #18 methodology consult)
**Commission context:** prereg for aware-fighter ablation gate; feeds D2 (relative-% margin) and D3 (noise-multiple floor) on ledger L-23
**Sources consulted:** arXiv, AAAI AIIDE proceedings, Sony AI blog/papers, Google Research blog, OpenReview, Semantic Scholar, ResearchGate, slidetodoc.com — all accessed 2026-07-22

---

## Summary (4 sentences)

The published game-AI and RL evaluation literature does not have a single agreed relative-% margin convention for "this sensor earned its keep" — but the empirical record from the closest precedents (influence-map kiting, MOBA ablation, wargame observation abstractions) clusters into two regimes: massive margins in scripted/rule-based comparisons where the sensor enables behavior that was qualitatively impossible without it (win rates jumping from 0–18% to 85–98%), and moderate margins in neural-agent component ablations (roughly 5–25 percentage points on win rate, or lap-time/finishing-position qualitative differences). The RL evaluation methodology literature (Agarwal et al. 2021 "Statistical Precipice," AdaStop 2023) does not prescribe a minimum detectable effect or noise multiple; it recommends stratified bootstrap 95% CIs and IQM as the reporting norm, with improvement declared meaningful when the CI does not overlap the baseline. No paper was found that explicitly sets a k× noise floor as a preregistered bar for a game-AI ablation; this construct is Reincarnated's own design and will need its k calibrated from first principles against the observed seed-to-seed variance in the actual metric. The closest direct structural analog is the Black & Darken 2024 (arXiv:2408.13328) wargame study, which is the right lineage but its specific reward-margin numbers are not retrievable from abstract-level access.

---

## Q1 — Relative-margin conventions in game-AI evaluation and agent-ablation studies

### What counts as meaningful

**Finding:** There is no published consensus "% threshold" for declaring an observation channel earned its keep in game-AI or agent-ablation contexts. What exists instead:

1. **Binary-capability framing (most common in scripted/influence-map work):** The comparison is not "how much did performance improve" but "did the agent acquire a capability it previously lacked." Uriarte & Ontañón 2012 (§Q3a below) is the cleanest example: the default agent wins 0% of kiting scenarios; with influence maps it wins 85–98%. The margin is not the point — the qualitative regime-shift is. This framing does NOT calibrate D2/D3 because the aware vs blind comparison is nearly all-or-nothing.

2. **Component ablation in neural agents (closer analog):** MOBA ablation (Honor of Kings, AAAI 2020 / Tencent AI Lab) reports win-rate drops of 15–50 pp when individual components are removed (Target Attention alone: 90% → 75%; action masking: 90% → 50.5%). Multi-UAV air combat HRL paper (PMC 2024): full method 0.647 win rate vs QMIX 0.588 (4v4), a ~10 pp difference. microRTS: invalid action masking 82% vs 0% (extreme); Verifier module ablation −18 pp; VLM ablation −64 pp. These suggest that in competitive game-AI, meaningful single-component contributions range from roughly **5–20 pp absolute** in well-trained neural agents.

3. **RL benchmarks in general (rliable framing):** The rliable / Precipice framing does not prescribe a minimum %-margin. It prescribes *interval estimates*: an improvement is provisionally meaningful when the 95% stratified bootstrap CI on the aggregate metric (IQM preferred) does not overlap the baseline CI. No absolute % threshold.

4. **A/B testing / online experimentation practice:** The minimum detectable effect (MDE) framework (PowerUp!, Statsig docs) sets the bar at the smallest effect a study has 80–90% power to detect given N. With 32 cells × 4 seeds = 128 observations, MDE is inversely proportional to sqrt(N). This is the most principled framework for preregistration but requires a variance estimate first.

**Confidence:** MEDIUM — the range (5–20 pp absolute in neural-agent ablations) is grounded in observed data; the absence of a published convention is a confirmed null finding, not a gap in search.

---

## Q2 — Noise-floor conventions: noise estimator and k values

### What the literature actually uses

**Finding:** No paper found uses an explicit k× noise-floor gate as a preregistered evaluation bar. The constructs used in practice:

| Practice | What is used | k equivalent | Source |
|---|---|---|---|
| Stratified bootstrap 95% CI | CI half-width is the noise estimate; improvement meaningful if CIs non-overlapping | Not stated as k×; but non-overlap at 95% ≈ 2σ for normal distributions | Agarwal et al. 2021 (arXiv:2108.13264) |
| AdaStop sequential testing | Adaptive family-wise error control; stops when accumulated evidence is sufficient | Not k-sigma; FWER-controlled | Mathieu et al. 2023/2024 (arXiv:2306.10882) |
| k=2 sigma band (noted in one industry context) | "improvements within [0, 2σ]...confounded with noise...accepted after re-runs; above 2σ accepted directly" | k=2 | Surfaced in a web result for a game balance evaluation study (AAU Master's thesis, Andersen 2022) — secondary source, not independently verified |
| Cohen's d conventions (psychology-origin, used in ML) | d=0.2 small, d=0.5 medium, d=0.8 large | Not k-sigma; standardized mean difference | Cohen 1988; cited in AI eval papers (multiple) |

**What is the noise estimator when a seed-level floor is computed:**
No paper prescribes a specific formula for "noise estimator in a cross-seed game-AI ablation." The closest practices:
- **Pooled standard deviation across seeds** (Cohen's d denominator): standard in A/B testing and psychology
- **Seed-to-seed SD of per-cell mean**: appropriate when cell = primary unit of randomization (this is the Reincarnated setup: 32 cells × 4 seeds, so SD of the mean across 4 seeds per cell is one level; pooled SD across all 128 obs is another)
- **MAD (median absolute deviation)**: more robust under non-normal distributions; used in rliable's IQM framing implicitly
- **Bootstrap CI half-width**: what rliable directly recommends

**Practical implication for D3:** No published game-AI paper was found that preregisters "margin must exceed k× [seed SD] where k=[value]." This is a design choice Reincarnated is originating. The k=2 reference (if the AAU source is accurate) corresponds to a 2σ threshold — equivalent to the traditional 95% CI non-overlap standard. k=3 would be more conservative (99.7% under normality). Given 4 seeds (very few), noise estimates will themselves be noisy; k=2 against a 4-seed SD is likely the practical floor.

**Confidence:** MEDIUM on k=2 as a plausible calibration anchor. LOW on the AAU source (it was a secondary reference in a search snippet, not independently verified). The bootstrap CI approach (Agarwal et al.) is HIGH confidence.

---

## Q3 — Observation-ablation precedent margins: the four cited papers

### (a) Black & Darken 2024, arXiv:2408.13328

**Citation verifies:** YES — paper exists, correct authors (Scotty Black, Christian Darken, Naval Postgraduate School), correct subject area.

**What it actually is:** "Localized Observation Abstraction Using Piecewise Linear Spatial Decay for Reinforcement Learning in Combat Simulations." The paper proposes a spatially-decayed local observation window (7×7 grid with piecewise-linear decay away from the agent) as an alternative to global observation, trained in the Atlatl combat simulation (a simple 2D military combat environment at NPS).

**What the ablation is:** Localized observation (agent sees nearby units with decaying weight) vs. global observation (agent sees all units with equal weight). This is structurally analogous to the Reincarnated aware vs blind comparison — it is the formation-AWARE vs formation-BLIND equivalent.

**Quantitative results:** NOT RETRIEVABLE from abstract-level access. The abstract states localized "consistently outperforms" global "across increasing scenario complexity levels." Preliminary notes surface in web search ("global-observation agent learns very slowly while local-observation agents learn relatively quickly"), but no specific win-rate or reward numbers are publicly readable from abstract pages or cached HTML. Full PDF required; PDF fetch returned binary.

**Flag:** The citation is valid and the paper is directly relevant. However, no margin numbers can be attributed with confidence. Do not use this paper to anchor D2 numbers without retrieving the full PDF.

**Confidence on citation verification:** HIGH. **Confidence on numbers:** NOT OBTAINED.

---

### (b) Uriarte & Ontañón 2012, AIIDE

**Citation verifies:** YES — paper exists, correct authors, correct venue, correct topic.

**What it actually is:** "Kiting in RTS Games Using Influence Maps," AIIDE 2012. Tests influence maps for kiting behavior in StarCraft (Vultures vs Zealots). Evaluates four settings: (1) default attack-move, (2) IM enemy field, (3) IM enemy + walls, (4) IM + target selection.

**Quantitative results (VERIFIED from presentation slides):**

| Scenario | Setting 1 (blind) | Setting 2 (IM enemy) | Setting 3 (IM+wall) | Setting 4 (IM+target) |
|---|---|---|---|---|
| 1v6 Vulture/Zealot | 0% | 24.9% | 85.5% | 95.2% |
| 4v6 Vulture/Zealot | 0% | 98.8% | 100% | 100% |
| Full game | 17.6% | — | — | 96.0% |

**Margin interpretation for D2:** The margin here (17.6% → 96.0% in full game = +78.4 pp; 0% → 85–95% in micro) reflects a capability regime-shift — influence maps enabled kiting that was previously impossible. This is NOT a calibration anchor for a subtle margin bar. If the aware-fighter gate shows this kind of margin, the bar is trivially passed. If the gate is looking for a modest advantage (e.g., +5–15 pp damage reduction), this paper doesn't calibrate it.

**Damage/HP data:** The paper also measured mean HP remaining, described qualitatively as "higher with IM" in the presentation charts, but specific numbers were not extractable from available sources.

**Flag for Reincarnated:** The Uriarte & Ontañón 2012 result is the correct lineage (spatial-awareness ablation in turn-by-turn combat) but represents a maximally favorable ablation scenario. Real formation-AWARE vs formation-BLIND margins in a trained agent will be smaller. Treat these numbers as ceiling evidence, not central calibration.

**Confidence on citation:** HIGH. **Confidence on numbers:** HIGH (slide source directly extracted).

---

### (c) GT Sophy vision-only variant (Sony AI, arXiv:2406.12563 and arXiv:2504.09021)

**Citation verifies:** PARTIALLY — the GT Sophy vision-based papers exist. However:
- arXiv:2406.12563 (2024): "A Super-human Vision-based RL Agent for Autonomous Racing in Gran Turismo" — this is a vision-based agent paper, not primarily a vision-ablation paper. The ablation it contains compares training architecture variants (asymmetric vs symmetric critic) and local-feature subsets (no velocity, no acceleration, no image, grayscale vs color, 32×32 vs 64×64).
- arXiv:2504.09021 (2025): "A Champion-level Vision-based RL Agent for Competitive Racing in Gran Turismo 7" — similar structure.

**What the ablation actually shows:**
- Removing image entirely: "agent unable to drive" (total failure — analogous to kiting regime-shift).
- Removing velocity: measurable performance decrease.
- Symmetric training (critic sees images instead of global features): "consistently failed to achieve first place in most evaluations."
- Removing RNN: "complete failure, agent unable to overtake any opponents."
- These results are reported qualitatively via box plots of finishing position; specific lap-time or win-rate numbers are NOT tabulated in the text.

**What is NOT in these papers:** A direct comparison of vision-only Sophy vs original state-based Sophy on a common metric. The 2024 paper establishes the vision agent achieves comparable performance to GT Sophy (super-human at Monza, Tokyo, Spa), but this is a competitiveness claim, not a controlled ablation with quantified margins.

**Flag for the citation claim:** The original commission describes "GT Sophy vision-only variant" as if there is a measured delta between Sophy-with-vision and Sophy-without-vision. The papers do not present this as a head-to-head ablation with % margins. The 2024/2025 papers are about achieving super-human performance with a vision-only agent, not about quantifying how much worse it would be without vision. The ablation sections cover architecture choices within the vision system.

**Confidence on citation:** MEDIUM (papers exist and are relevant but the framing as "vision ablation with quantified delta" is imprecise). **Confidence on numbers:** NOT OBTAINED — box plots reported without extracted lap-time deltas.

---

### (d) Liu et al. 2017, arXiv:1703.06275

**Citation verifies:** MISMATCH. arXiv:1703.06275 is "Evolving Game Skill-Depth using General Video Game AI Agents" by Jialin Liu et al. — this is about evolving game difficulty parameters in a space-battle game using RMHC and MABRMHC algorithms. It is NOT about emergent multi-agent coordination and does NOT contain observation-channel ablation studies.

**What it actually contains:** The paper adapts a space-battle game to the GVG-AI framework and uses hill-climbing algorithms to evolve game parameters. Agent coordination and spatial-awareness observation ablation are not part of this work.

**Flag:** The citation "Liu et al. 2017, arXiv:1703.06275 (emergent multi-agent coordination / observation variants)" does not match the paper at that arXiv ID. Either the arXiv ID is wrong or the paper description is wrong. Do not use this citation as a source for observation-ablation precedent. The arXiv paper about emergent multi-agent coordination the commission may have intended is possibly Mordatch & Abbeel 2018 ("Emergence of Grounded Compositional Language") or Lowe et al. 2017 ("Multi-Agent Actor-Critic") — neither ID matches.

**Confidence:** HIGH on the mismatch. LOW on what the intended citation was.

---

## Q4 — Additional published cases: spatial-awareness ablation with quantified performance delta

### Strong additional precedents found

**1. Hierarchical RL with influence maps in StarCraft micromanagement (arXiv:2606.30092)**
- **Ablation:** HRL with influence-map hashing vs without (HRL-CBS); flat RL vs both.
- **Margin observed:** On scenario sce-1: full model 0.999 win rate vs no-influence-map 0.97 (~3 pp); on sce-3m (complex): full model 0.925 vs no-IM ~0.85 (~7 pp).
- **Interpretation:** This is a trained neural-agent ablation, not a scripted-agent comparison. The margins are modest (3–7 pp) but the paper characterizes them as "markedly" improving win rate. This range is a plausible calibration anchor for a formed-trained-agent aware-vs-blind gate.
- **Source:** arXiv:2606.30092 (accessed 2026-07-22 via HTML). MEDIUM confidence on the specific numbers (extracted from a WebFetch summary; table values are reported as approximations from the paper text).

**2. Multi-agent communication ablation (Closed-Loop Vision-Language Planning, arXiv:2502.10148 — cited in search)**
- Win rate drop from 0.57 to 0.06 when communication (spatial propagation of awareness) is disabled.
- **Margin:** −51 pp (0.57 → 0.06). Again a regime-shift rather than a subtle margin.
- Source: web search summary; full paper not fetched. LOW confidence on exact numbers; HIGH confidence that a large margin was reported.

**3. Multi-UAV air combat HRL ablation (PMC 2024, Liu et al.)**
- Full model (spatial + hierarchical): win rate 0.647 (4v4), 0.829 (8v8).
- QMIX baseline: 0.588 (4v4), 0.818 (8v8).
- **Margin:** 5.9 pp (4v4), 1.1 pp (8v8). Very small at 8v8.
- **Interpretation:** The spatial/hierarchical advantage shrinks as scenario complexity grows — possibly because other strategic factors dominate. This is a cautionary data point: a well-designed ablation may show small margins even when the mechanism is genuinely useful.
- **Source:** PMC10891071 (fetched directly). HIGH confidence.

**4. microRTS competition agent (arXiv:2402.08112)**
- Invalid action masking ablation: 82% win rate with masking, 0% without.
- This is not a spatial-awareness ablation but illustrates that even in trained neural agents, a single enabling component can be all-or-nothing.
- **Source:** arXiv:2402.08112v2 (fetched directly). HIGH confidence.

**5. Honor of Kings MOBA (AAAI 2020, arXiv:1912.09729)**
- Component ablation: target attention removed → 90% → 75% (−15 pp); LSTM removed → 90% → 73% (−17 pp); full rollouts vs partial → 70–80% improvement.
- This is component ablation in a complex learned policy, not a spatial-input ablation specifically.
- **Source:** ar5iv HTML of 1912.09729 (fetched directly). HIGH confidence.

---

## Synthesis: what the literature would set

This section presents calibration evidence for D2 and D3. It does not recommend final numbers — that is the conductor's and Matt's call.

### Candidate relative-% margin (D2)

**From the literature record:**

| Context | Observed margin | Type |
|---|---|---|
| Influence-map kiting, scripted (Uriarte 2012) | +78 pp absolute (17.6% → 96.0%) | Regime-shift; ceiling |
| HL-IM StarCraft micromanagement, trained NN (arXiv 2606.30092) | +3 to +7 pp absolute | Subtle trained-agent advantage |
| Multi-UAV HRL vs QMIX, trained NN (PMC 2024) | +1 to +6 pp absolute | Very subtle |
| MOBA component ablation, trained NN (HoK AAAI 2020) | +15 to +17 pp absolute per component | Moderate |
| Multi-agent communication ablation | +51 pp | Regime-shift |
| Action masking microRTS | +82 pp | Regime-shift |

**Pattern:** Scripted/rule-based ablations cluster at regime-shift margins (>50 pp). Trained-neural-agent spatial-awareness component ablations cluster at **3–15 pp absolute**. The Reincarnated gate is a trained-rule-based agent (not purely neural, not purely scripted), so the applicable reference class is ambiguous — probably between the two.

**For a relative-% margin (D2) in damage-intake terms:** The literature does not directly report relative-% damage-intake improvement for spatial-awareness ablations. The win-rate data above is the closest proxy. If a 10 pp win-rate advantage is "meaningful" in the neural-agent literature (as suggested by HoK ablation framing), a reasonable translation to damage-intake relative % would be: **if the noise is, say, ±5% of mean damage-intake (from seed-to-seed variance), a 10–15% relative reduction in damage-intake would be a plausible "earned its keep" bar**. This is not literature-derived; it is an inference from the win-rate data.

**Direct literature anchor:** No published paper sets a relative-% damage-intake bar for a formation-aware combat agent. The Reincarnated prereg is originating this. The 5–15% relative margin range is grounded in the trained-agent ablation literature as the regime where effects are detectable and non-trivial.

**Confidence:** MEDIUM on the 5–15% range as a calibration window. LOW on any specific number within that range.

### Candidate k (D3)

**From the literature record:**

| Framework | k equivalent | Notes |
|---|---|---|
| Stratified bootstrap 95% CI non-overlap (rliable) | ~2σ under normality | Standard in RL evaluation |
| AdaStop FWER control | Adaptive; not k-sigma | Requires many runs; adaptive stopping |
| Industry game-balance k=2σ (AAU 2022, unverified) | k=2 | Improvement in [0, 2σ] re-run; above 2σ accepted |
| Cohen's d "medium" effect | d=0.5 (0.5σ) | Small = 0.2, large = 0.8 |

**Practical anchor:** With 4 seeds per cell, the seed-to-seed SD is itself noisy (estimated from 3 degrees of freedom). Using k=2 means the margin must exceed 2× the estimated seed SD — conservative given how noisy that estimate is, but the only tractable floor without a larger seed count. k=3 would require the effect to be clearly above a 3σ boundary, which is more demanding but defensible given the small seed count (avoids false positives from noisy SD estimates).

**Recommended calibration anchors:**
- k=2 corresponds to ~95% confidence under normality; practical for this seed count
- k=3 is more conservative and defensible when the noise estimator is uncertain

**Confidence:** MEDIUM on k=2 as the lower bound; LOW on k=3 as the upper bound (no specific game-AI precedent for k=3 as a preregistered bar).

### Candidate noise estimator

No game-AI paper was found that specifies a noise estimator formula for this kind of gate. The three candidates:

| Estimator | What it measures | Appropriate if |
|---|---|---|
| Pooled SD across all 128 observations (32 cells × 4 seeds) | Overall outcome variance | Cells are exchangeable (similar noise level) |
| Seed-to-seed SD of per-cell means (per cell, then aggregated) | Within-cell noise; averages across cells | Cells are not exchangeable; noise varies by scenario |
| Bootstrap CI half-width on the arm-level mean | Direct uncertainty on the aggregate comparison | Want uncertainty on the cross-arm comparison directly |

**Literature alignment:** rliable recommends bootstrap CI half-width. If Reincarnated uses a simpler formula, pooled SD is more standard than per-cell SD (it has more degrees of freedom given the small seed count). MAD is valid but less familiar in this context.

---

## Knowledge gaps not resolved

1. **Black & Darken 2024 (arXiv:2408.13328) specific numbers:** The PDF is binary-only for this tool; no HTML version on arXiv. The specific win-rate or reward improvement from localized vs global observation in the Atlatl combat simulation was not obtained. This is the single most relevant citation for D2 calibration. Manual PDF access is needed.

2. **Liu et al. 2017 arXiv:1703.06275 citation mismatch:** The paper at that ID is not about multi-agent coordination or observation ablation. The intended citation source is unknown; the number appears wrong. No observation-ablation data can be drawn from this ID.

3. **GT Sophy quantified lap-time or win-rate delta between configurations:** The 2024/2025 Sony papers report ablation results as box plots; specific numerical margins were not tabulated in accessible text. The claim that GT Sophy was tested in a controlled "vision-only vs state-based" ablation with a reported % margin is not supported by what these papers actually contain.

4. **Damage-intake as a primary metric in published ablations:** No paper was found that uses damage-intake as the primary metric for an observation-ablation gate. All published cases use win rate, reward, or lap time. The translation from win-rate margins to damage-intake margins requires an additional modeling step.

5. **k-sigma preregistered evaluation bars in game AI:** No paper found that preregisters a k× noise-multiple floor for a game-AI ablation gate. Reincarnated is likely the first to do so explicitly in this form. This is a null finding that justifies grounding D3 in adjacent statistical conventions (bootstrap CI, Cohen's d) rather than in domain precedent.

---

## Source list

| Reference | URL | Access date | Role |
|---|---|---|---|
| Black & Darken 2024, arXiv:2408.13328 | https://arxiv.org/abs/2408.13328 | 2026-07-22 | Direct citation — verified, numbers not obtained |
| Uriarte & Ontañón 2012, AIIDE | https://ojs.aaai.org/index.php/AIIDE/article/view/12544 | 2026-07-22 | Direct citation — verified |
| Uriarte & Ontañón 2012 slides | https://slidetodoc.com/kiting-in-rts-games-using-influence-maps-alberto/ | 2026-07-22 | Quantitative data source |
| GT Sophy 2024, arXiv:2406.12563 | https://arxiv.org/abs/2406.12563 | 2026-07-22 | Direct citation (vision-based, ablation section) |
| GT Sophy 2025, arXiv:2504.09021 | https://arxiv.org/abs/2504.09021 | 2026-07-22 | Additional GT Sophy citation |
| Liu 2017, arXiv:1703.06275 | https://arxiv.org/pdf/1703.06275 | 2026-07-22 | MISMATCH — not multi-agent coordination |
| Agarwal et al. 2021 "Statistical Precipice", arXiv:2108.13264 | https://arxiv.org/abs/2108.13264 | 2026-07-22 | Noise estimator / evaluation methodology |
| rliable Google Research blog | https://research.google/blog/rliable-towards-reliable-evaluation-reporting-in-reinforcement-learning/ | 2026-07-22 | Summary of precipice methodology |
| AdaStop, arXiv:2306.10882 | https://arxiv.org/abs/2306.10882 | 2026-07-22 | Sequential testing for RL agent comparison |
| HRL with influence maps StarCraft, arXiv:2606.30092 | https://arxiv.org/html/2606.30092v1 | 2026-07-22 | Additional precedent — trained-agent spatial ablation |
| Multi-UAV HRL ablation, PMC10891071 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10891071/ | 2026-07-22 | Additional precedent — win rate table |
| Honor of Kings MOBA ablation, arXiv:1912.09729 | https://ar5iv.labs.arxiv.org/html/1912.09729 | 2026-07-22 | Additional precedent — component ablation win rates |
| microRTS competition agent, arXiv:2402.08112 | https://arxiv.org/html/2402.08112v2 | 2026-07-22 | Additional precedent — action masking ablation |
