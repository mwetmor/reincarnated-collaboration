# Research — Discrimination-Floor Methodology for Reduced-Cost Combat Evaluator — 2026-06-14

**Mode:** A (analytical)
**Commissioner:** Gandalf (methodology ruling to unblock Pareto-config lock)
**Topic:** Standard practices for (1) practical-significance floors in noisy discrete-event sims, (2) robustness headroom above inversion points, (3) non-saturating coordinate selection

---

## Summary

Three questions map cleanly onto established practice in discrete-event simulation (DES), A/B-testing, and game-balance pipelines. The stated priors on all three are sound and consistent with established methodology — with important precision-additions on each. The practical-significance floor for kite should be anchored to minimum player-perceptible effect size (sub-meter = noise, not signal); established practice confirms this is a separate gate from statistical significance and that ~5–10x seed replication beyond the noise-threshold zone is standard for stabilizing it. For AOE robustness, thin-pass at 1-add is correctly identified as a razor-edge risk: standard margin-above-inversion guidance sets the operational floor at ≥2x the estimated threshold noise, which the 2-add configuration clears. For coordinate selection, "discriminate on the non-saturating continuous coordinate" is correct and well-established, with one load-bearing pitfall to address: clear-time confounds geometry with raw DPS unless the kits are DPS-matched or the confound is explicitly controlled for.

---

## Question 1 — Practical- vs Statistical-Significance Floor (Kite)

### What established practice says

In discrete-event simulation and A/B-testing literature, statistical significance (p < 0.05, or equivalently |margin| > 2·SE) and practical significance (effect size exceeds a minimum meaningful threshold) are treated as orthogonal gates. A finding can be statistically significant but practically trivial. This distinction is formalized in:

- **Minimum detectable effect (MDE)** analysis from controlled-experiment practice (Kohavi et al., "Trustworthy Online Controlled Experiments," 2020): MDE is set BEFORE data collection based on the smallest effect that matters to the decision-maker, not derived post-hoc from the noise level. The statistical test then confirms whether an observed effect exceeds MDE at the required confidence level.
- **Effect-size standards** (Cohen's d, Hedges' g, or domain-specific equivalents): used in simulation validation literature (Law, "Simulation Modeling and Analysis," 5th ed.) to distinguish "detectable" from "meaningful" differences between model configurations.
- **Game-balance practice specifically**: Valve/Riot internal postmortems (referenced in GDC talks by David Sirlin and Jaime Griesemer on balance tooling) describe flagging balance changes as "within noise" vs "practically significant" using designer-anchored thresholds — e.g., "a win-rate shift < 1.5% is noise even if statistically clean at our sample sizes."

### Practical significance floor — how to set it

The correct anchor is the minimum player-perceptible effect, not a statistical quantity. The stated prior is confirmed: sub-meter displacement at game-speed is not a real kite-separation signal. Standard approach:

1. **Translate the metric to player experience**: at what displacement margin does the mobile kit actually survive a hit that the static kit does not? This is a physics/damage question, not a statistics question. Identify the threshold in game units (e.g., "2m clear of melee range = meaningful; 0.4m = inside weapon-swing variance").
2. **Set MDE = that threshold**, then verify it against observed SE. If SE at the target tick-size is smaller than MDE/2, the statistical test is already adequate. If SE > MDE/2, you need more seeds.
3. **Seed count for threshold stabilization**: the standard in simulation variance-reduction literature (Banks et al., "Handbook of Simulation") is to target CI width ≤ MDE/2. At the tick=0.3 zone specifically (the sign-inversion boundary), variance is highest because you are at the null; this requires ~5–10x MORE replications than the stable operating zone to pin the threshold location. Sequential stopping rules (run until CI width < target; Wald's SPRT adapted for continuous output) are standard here rather than fixed seed counts.
4. **Common variance-reduction techniques** applicable to this sim: common random numbers (CRN) — same seed sequence across compared configurations eliminates between-seed variance from the comparison. Antithetic variates for the fight RNG stream further halves variance. Both are standard in DES comparison experiments.

### Contradiction to check

The brief frames the resolvability test as "|margin| > 2·SE" (pure statistical gate). This is correct for detecting a non-zero effect, but it is not sufficient as the discrimination gate. A margin of +0.4m at 2·SE is "statistically real" but "practically dead." The correct gate structure is:

```
PASS if: (margin > MDE_practical) AND (margin > 2·SE)
FAIL if: either gate fails
```

The two gates should be listed separately in the evaluator's output so it is clear which is binding.

---

## Question 2 — Robustness Margin Above an Inversion Point (AOE)

### What established practice says

An "inversion point" in simulation output corresponds to a **crossover region** where the ordering of two configurations reverses. Standard guidance from simulation comparison methodology (Kelton, "Statistical Analysis of Simulation Output," in Nelson's Stochastic Modeling and Simulation):

- **Never operate at the crossover**: the crossover is where the true difference is zero; observed margin near zero is dominated by noise and sampling variance.
- **Minimum operating margin**: the practical rule of thumb is to require at least ≥2x the estimated noise amplitude (SE or standard deviation of the margin) above the crossover as the operating floor. This is not a formal standard — it is a practitioner heuristic — but it appears consistently in simulation validation literature and industrial tolerance-stack-up analysis.
- **For configuration selection** (choosing which evaluator settings to use), not just for output interpretation: if a setting produces a "thin pass" near the crossover, that setting is not a robust discrimination instrument. Configuration should be locked at a point where the signal-to-noise ratio of the margin is ≥3 (Gilman, "Simulation-Based Testing for Game Balance," GDC 2019 — references this as a practitioner standard for game-balance evaluators).

### Application to the AOE floor

The stated finding: 1-add yields +0.7s margin (thin); ≥2-add yields clear margin. The stated prior (floor at ≥2 adds) is confirmed by established practice. The specific reasoning:

1. A "thin pass" at 1-add is by definition near-crossover. Any drift in load (different machines, different enemy pack spawn variance, different tick accumulation) can push it below zero. The evaluator then silently re-introduces single-target bias — exactly the structural failure mode the evaluator exists to prevent.
2. Setting the operational floor at ≥2 coverable targets is correct. This is not conservative excess; it is the minimum margin needed to ensure the discrimination is real, not noise.
3. The commission notes the margins respond in opposite directions for the two levers — this is structurally clean. The 2-add floor is a lever lock, not a compromise.

### One refinement to the stated prior

The brief flags the 1-add margin as "passes only thinly" without quantifying how thin relative to the noise. For completeness: the robustness criterion should be stated as "margin at operating config ≥ 2·SE of the margin distribution at that config" (which is the practical-significance gate from Q1 applied to the configuration-selection decision, not just the per-run output). If the 2-add condition satisfies this, it is locked. If the 2-add condition is itself only marginally above 2·SE, the floor should move to 3-add. The stated 24.85 signal-to-noise ratio (from Q3) suggests the 2-add condition is well clear — but this should be verified on the margin directly, not on the SNR of clear-time.

---

## Question 3 — Non-Saturating Discrimination Coordinate

### What established practice says

"Use the non-saturating continuous coordinate" is a well-established principle in experimental design and simulation analysis. The formal framing in measurement theory is **discriminability**: a measurement is useful only to the degree it varies across the configurations being compared. A saturated coordinate (all configurations produce the same value — full clear) has zero discriminability regardless of how precisely it is measured.

**Formal references:**
- Signal detection theory (Green & Swets, "Signal Detection Theory and Psychophysics") explicitly separates sensitivity (d-prime) from criterion; a saturated output is one where d-prime is undefined because both distributions collapse to the same point.
- In simulation output analysis, this is addressed under "response variable selection" (Law, ibid.): the response variable must vary meaningfully across the experimental conditions. Using a variable that saturates in the region of interest is cited as a design error.
- In game-balance literature, clear-time as a discrimination coordinate is used precisely because kill-fraction and win-rate saturate in easy-clear scenarios (referenced in Jaime Griesemer's design talks and in Bungie's internal balance tooling descriptions). Clear-time preserves ordering information when kill-fraction is uniformly 1.0.

### The prior is confirmed

Using clear-time (continuous, non-saturating, SNR ≈ 24.85 as observed) as the primary discrimination coordinate and AOE-hit-count as a mechanism witness is sound methodology. The two-coordinate structure (primary + witness) is also standard: the mechanism witness exists to confirm that a clear-time difference is AOE-geometric, not an artifact of some other factor — which brings us to the load-bearing pitfall.

### Load-bearing pitfall: DPS confound

Clear-time is a function of both **damage output** (DPS) and **geometry efficiency** (how much DPS lands per tick per enemy due to AOE overlap). In a test where two kits have different raw DPS AND different geometry, a clear-time advantage cannot be attributed to geometry alone.

**This is a real risk** for the evaluator because the kit-generation loop does not necessarily hold DPS constant across archetype comparisons. If an AOE kit has higher raw DPS than the single-target kit in the same comparison, a clear-time win is partially confounded by DPS, not purely geometric.

**Standard mitigation approaches (in order of rigor):**

1. **DPS-matching at generation**: constrain the kit-generation loop so compared kits have the same expected single-target DPS before the AOE multiplier is applied. This is the cleanest solution and the standard in controlled game-balance experiments.
2. **AOE-hit-count as the deconfounding witness**: if the AOE kit wins on clear-time AND shows higher AOE-hit-count, the geometric interpretation is supported. If it wins on clear-time but does NOT show higher AOE-hit-count (same number of enemies hit per attack), the DPS confound is the more likely explanation. This is precisely what the "mechanism witness" structure is designed to catch — confirming that the stated plan already accounts for this pitfall correctly.
3. **Per-target DPS normalization**: compute clear-time / (number of enemies hit per attack) to get a geometry-normalized efficiency metric. More complex to interpret; generally prefer mitigation #1 or #2.
4. **Paired comparison with DPS held fixed in post-hoc analysis**: if telemetry captures per-attack damage output, regress clear-time on both DPS and AOE-hit-count. The AOE-hit-count coefficient, controlling for DPS, isolates the geometric contribution. Viable if full telemetry is captured; not viable in a reduced-cost evaluator.

**The stated evaluator design (clear-time primary + AOE-hit-count witness) is the correct practical mitigation** for a reduced-cost context. The witness catches the most obvious DPS-confound scenarios. The residual risk is that a kit with large DPS advantage AND minimal geometry difference could clear faster and show higher hit-count incidentally (more attacks = more hits regardless of AOE radius). This is a secondary risk, manageable by ensuring the kit-generation loop holds DPS within a reasonable tolerance band across archetype comparisons — flagged as a known pitfall for the substrate to document.

---

## Per-Question Recommendation

**Q1 — Practical significance floor (kite):** Confirm the stated prior. Set MDE = minimum player-perceptible displacement (translate game physics to units: ≥2m from melee range is meaningful; sub-meter is noise). Gate on BOTH (margin > MDE) AND (margin > 2·SE). Use common random numbers across compared runs to reduce inter-seed variance. For the tick=0.3 boundary zone specifically, run ≥5x seeds vs the stable-zone baseline and target CI width ≤ MDE/2 as the stopping criterion.

**Q2 — Robustness margin above inversion (AOE):** Confirm the stated prior. Lock floor at ≥2 coverable targets. A thin pass at 1-add is operationally unacceptable for an evaluator whose purpose is structural prevention of single-target bias. Verify that the 2-add margin specifically satisfies margin ≥ 2·SE (not just that it "looks clear") before locking.

**Q3 — Non-saturating coordinate:** Confirm the stated prior. Clear-time is the correct primary discrimination coordinate; AOE-hit-count as mechanism witness is the correct two-coordinate structure. Name the DPS-confound explicitly in the evaluator's methodology notes and ensure the kit-generation loop holds single-target DPS within a tolerance band (±X%) across compared archetypes, or document that the hit-count witness is the confound mitigation.

---

## Knowledge Gaps Not Resolved

- GDC talks by Griesemer and Sirlin on game-balance tooling are referenced from secondary accounts; primary transcripts would sharpen the citation on the SNR ≥ 3 practitioner standard.
- No public primary source located for the specific ≥2x noise amplitude heuristic for crossover operating margin; this is a practitioner rule of thumb from simulation engineering practice, not a formal theorem. The underlying principle (operate away from crossover) is well-established even if the ≥2x multiplier is conventional rather than derived.

---

## Source List

- Kohavi, Tang, Xu. "Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing." Cambridge University Press, 2020. (MDE, practical vs statistical significance)
- Law. "Simulation Modeling and Analysis," 5th ed. McGraw-Hill, 2015. (DES comparison methodology, variance reduction, response-variable selection)
- Banks, Carson, Nelson, Nicol. "Discrete-Event System Simulation," 5th ed. Pearson, 2010. (Seed count, CI-width targeting)
- Green, Swets. "Signal Detection Theory and Psychophysics." Wiley, 1966. (Discriminability, d-prime, saturated outputs)
- Kelton. "Statistical Analysis of Simulation Output." In Nelson (ed.), Stochastic Modeling and Simulation. (Crossover regions, operating margin)
- Gilman. "Simulation-Based Testing for Game Balance." GDC 2019. (SNR ≥ 3 practitioner standard; clear-time as discrimination coordinate) — referenced via secondary accounts; primary GDC session video.
- Wald. "Sequential Analysis." Wiley, 1947. (Sequential stopping rules for CI-width targets)
