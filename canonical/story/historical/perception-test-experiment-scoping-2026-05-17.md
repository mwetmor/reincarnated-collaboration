# Phase-1 P1a Perception Test — Experiment Scoping

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authority:** gandalf (story-and-design steward), per Legolas Mode A literature pass top recommendation.
**Status:** Phase-1 P1a prerequisite experiment scoping. **Must complete before Layer-3 (mirror-match diversity gate) is coded.**
**Companion artifacts:** `substrate-identity-declarations-2026-05-17.md` (the 7 declarations the experiment exercises); `archetype-coupling-archaeology-2026-05-17.md` (the convergence vectors the experiment validates); `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` (Legolas Finding A + B — the motivating literature).
**Coordination:** gandalf (design + experiment authorship); drax (session-running); jack-ryan (measurement protocol + analysis); Matt (subject participant; possibly recruits son for additional perspective).

**Reading order:** § 0 TL;DR → § 1 Why this experiment is needed → § 2 Hypothesis → § 3 Method → § 4 Subjects + sessions → § 5 Measurement → § 6 Decision criteria → § 7 Risks + mitigations → § 8 Phase-1 P1a positioning → § 9 Cross-references.

---

## § 0 — TL;DR

**Hypothesis:** Mechanical-parameter distinctness in archetype composition (Layer 2 output) does NOT guarantee player-perceived distinctness in play. Per Legolas Mode A Finding A: "Computational diversity metrics regularly misalign with player-perceived distinctness."

**Experiment:** Generate 4-6 archetype pairs that are *mechanically parametrically distinct* per Layer-2 composition outputs. Have human player(s) play each pair in short focused sessions. Measure whether players perceive the archetypes as distinct.

**Decision output:** Determine whether Layer-3 mirror-match diversity gate should use *mechanical-parameter vector distance* (cheap; what the engine has) or *play-trace feature distance* (more expensive; requires per-fight feature extraction; necessary if the cheap metric proves perceptually invalid).

**Cost:** 1-2 days. Smallest possible empirical pass that prevents building the wrong gate.

**Positioning:** Phase-1 P1a prerequisite — runs *before* Layer-3 is coded.

---

## § 1 — Why this experiment is needed

The five-layer diversity architecture's Layer 3 (mirror-match diversity gate) measures similarity between archetypes and rejects candidates above a threshold T to push apart converging shapes. **Similarity is measured against some metric.** The architecture specifies that the metric should be in play-trace feature space — not mechanical-parameter vector space — but does not yet commit to a specific metric.

The Legolas Mode A literature pass surfaced two relevant findings:

- **Finding A — Diversity-metric/perception gap.** Chand et al. (2024) and the 2024 OpenReview perceptual-metrics paper explicitly document that computational diversity metrics regularly misalign with player-perceived distinctness. **There is no validated single metric.**
- **Top recommendation.** Before implementing Layer 3, run a brief empirical test — generate mechanically-distinct archetype pairs, have human player(s) session them, measure perceived distinctness. If players don't perceive distinction, ground the similarity metric in play-trace feature space before coding the gate.

**The cost of skipping this experiment:** building Layer 3 against a mechanical-parameter metric, shipping Phase-1 P1, discovering in P1 retrospective that the diversity gate was gating on a perceptually-invalid axis. Engineering time burned for no diversity payoff. Worst case: the diversity architecture ships nominally complete but produces archetypes that *the engine* thinks are distinct and *the player* doesn't.

**The cost of running this experiment:** 1-2 days. Trivial relative to Phase-1 P1 timeline.

---

## § 2 — Hypothesis

### § 2.1 — Primary hypothesis

**H1:** Player-perceived archetype distinctness is **NOT** monotonically predicted by mechanical-parameter vector distance. Some mechanically-distinct archetypes will be perceived as similar; some mechanically-similar archetypes will be perceived as distinct.

**If H1 is supported (likely per Legolas finding):** Layer-3 similarity metric must be grounded in play-trace feature space. Author secondary spec for feature extraction before gate code.

**If H1 is rejected:** Layer-3 similarity metric can use mechanical-parameter vector distance. Cheaper; faster to ship. Unlikely but possible outcome.

### § 2.2 — Secondary hypothesis

**H2:** Per-substrate iconic vocabulary at Layer 4 (LLM flavor) significantly affects perceived distinctness, *independently* of mechanical composition. Two archetypes with identical mechanical composition but different per-substrate iconic vocabulary will be perceived as more distinct than two archetypes with different mechanical composition but identical generic vocabulary.

**Test approach:** Include a vocabulary-paired control archetype set alongside the mechanical-paired set. (See § 3.3.)

---

## § 3 — Method

### § 3.1 — Archetype generation (gandalf + drax authoring)

Generate **4 archetype pairs (8 archetypes total)** plus a **control quartet (4 archetypes)**:

**Mechanical-distinctness pairs** (Pair-Type A — same role, same substrate, parametrically different):
- Pair A1: two fire_damage archetypes with **statistically distinct kit-shape vectors** (geometry distribution, cooldown profile, ailment distribution different by ≥2σ across all axes)
- Pair A2: two water_controller archetypes, same axes
- Pair A3: two earth_caster archetypes, same axes
- Pair A4: two wind_controller archetypes, same axes

These pairs test: *can players perceive mechanical distinctness within the same substrate × role pair when the parametric vectors are statistically different?*

**Vocabulary-control quartet** (Pair-Type B — different mechanics, identical generic vocabulary):
- Quad B: four archetypes, one per canonical substrate (fire/water/earth/wind), each mechanically distinct (different role) but with **deliberately generic vocabulary** (no substrate-iconic verbs; LLM forbidden from using substrate-specific phrasings).

This quad tests: *do players perceive substrate distinctness when LLM flavor is suppressed?*

### § 3.2 — Engine support

Pair generation can use the **current canonical-four engine** (no Layer-2 composition refactor needed). Use existing archetype templates with deliberately tuned parameters to produce statistically-distinct kit vectors within each pair. The experiment does not require canonical-7 substrate expansion or the diversity architecture's full Layer-1 declarations — it validates the *metric*, not the architecture.

Drax provides:
- Demo1 (Pixi.js) session-runner with each archetype loadable in a brief fight context
- Per-fight telemetry capture (already in V2 schema)
- Per-archetype short presentation surface (loadout-side)

### § 3.3 — Session structure

Each player session has 12 fights (8 mechanical-distinctness pair fights + 4 vocabulary-control quad fights), in randomized order. Each fight is 60-90 seconds against a fixed reference monster. Player drives the archetype's primary actions; pickup is minimal because the test isn't about depth — it's about *first-pass perceived identity*.

Between fights, the player rates the just-played archetype on three dimensions:
- **Distinctness** (vs prior archetypes played in this session): 1-7 scale
- **Identity** (one-sentence answer: "what kind of archetype was that?")
- **Vocabulary perception** (one-sentence answer: "what did it FEEL like playing?")

After all 12 fights, the player completes a **pair-grouping task**: presented with the 8 mechanical-pair-type archetypes, group them into pairs they perceived as "the same kind of thing." Match against the engineered pairs (A1-A4). Compute pair-recovery accuracy.

### § 3.4 — Session length

~30-45 minutes per player. 12 × 90sec fights = 18 min + inter-fight ratings + pair-grouping task.

---

## § 4 — Subjects + sessions

### § 4.1 — Recruitment

**Phase 1 (minimum viable):** Matt + Matt's son (per `user_role.md` collaborative pattern) = 2 subjects.

This is *not* a statistically powered sample. It is a *signal-detection* sample. If both subjects pair-recover accurately (≥3/4 mechanical pairs recovered) AND rate same-pair archetypes as significantly more similar than cross-pair archetypes, **the metric likely passes.** If they don't, **the metric likely fails** and the gate needs play-trace grounding.

**Phase 2 (if Phase 1 is ambiguous):** Recruit 2-4 additional subjects from the gaming community. Threshold: same protocol; majority agreement on pair-recovery accuracy.

### § 4.2 — Subject prep

- 10-minute orientation explaining the experiment's purpose at a high level ("we're checking whether the engine can produce archetypes that *feel* distinct, not just look distinct on paper")
- Confirm subject understands the rating scale and pair-grouping task
- Provide control practice (one warm-up fight with a non-experimental archetype)

### § 4.3 — Bias controls

- **Randomize fight order** per session
- **Counterbalance pair order** across subjects (Subject 1: A1-first; Subject 2: A4-first; etc.)
- **Withhold substrate names** from the player during sessions (the archetype is presented with neutral display name like "Class 3" or "Build B")
- **Withhold mechanical-parameter information** (no tooltip-level kit details visible)

The player perceives only what *plays in their hands.* That is the perception we are testing.

---

## § 5 — Measurement

### § 5.1 — Primary metric: Pair-recovery accuracy

For each subject:
- Engineered pairs: {A1, A2, A3, A4}
- Player-recovered pairs: {subject's groupings of the 8 mechanical-pair archetypes}
- Accuracy = (count of correctly-grouped engineered pairs) / 4

**Threshold:** Subjects must achieve ≥75% pair-recovery accuracy (3/4 pairs) for the mechanical-parameter metric to be validated.

### § 5.2 — Secondary metric: Same-pair similarity scoring

For each subject's distinctness ratings:
- Compute average within-pair distinctness rating (rating of archetype to its true pair-mate)
- Compute average cross-pair distinctness rating (rating of archetype to non-pair-mates)
- Within-pair should be LOW (≤3 on 1-7 scale; pair-mates feel similar); cross-pair should be HIGH (≥5 on 1-7 scale; cross-mates feel different)

**Threshold:** Mean within-pair rating < mean cross-pair rating by ≥1.5 points on the 7-point scale.

### § 5.3 — Vocabulary-control measurement

The vocabulary-control quad's distinctness ratings indicate how much LLM flavor affects perception:
- High distinctness across the quad (≥5 on 1-7 scale) despite generic vocabulary → mechanical composition alone produces perceptible distinctness → Layer 4 is augmenting, not load-bearing
- Low distinctness across the quad (≤3 on 1-7 scale) despite different roles/substrates → mechanical composition alone does NOT produce perceptible distinctness; Layer 4 is doing the heavy perceptual lifting → Reflection IV (diversity at scale is textural) is validated; Layer 4 scope-cuts are dangerous

### § 5.4 — Qualitative measurement

Player "identity" and "vocabulary perception" one-sentence answers are analyzed qualitatively:
- Do same-pair archetypes elicit *similar* identity descriptions?
- Do cross-substrate archetypes elicit *different* identity descriptions?
- Are vocabulary-perception answers substrate-coherent (e.g., fire archetypes described with heat-language) or generic?

This is the unstructured-feedback layer that catches edge cases the quantitative metrics miss.

---

## § 6 — Decision criteria

### § 6.1 — Decision tree

```
Pair-recovery accuracy ≥75% AND within-pair < cross-pair by ≥1.5 points?
├── YES → Mechanical-parameter vector metric is PERCEPTUALLY VALID
│         Layer 3 can use mechanical-parameter distance as similarity metric.
│         Cheap; ship.
│         (Note: still recommend Layer 4 LLM flavor as augmentation per Reflection IV.)
│
└── NO  → Mechanical-parameter vector metric is PERCEPTUALLY INVALID
          Layer 3 cannot use mechanical-parameter distance as primary metric.
          ACTION: Author Layer-3 similarity-metric grounded in play-trace features.
                  Surface feature-extraction spec to gamora before gate is coded.
                  Estimated extra Phase-1 P1 scope: 1-2 weeks.
```

### § 6.2 — Vocabulary-control branch

```
Vocabulary-control quad distinctness ≥5?
├── YES → Mechanical composition alone produces perceptible distinctness
│         Layer 4 LLM flavor is augmenting (not foundation)
│         Possible scope-cut candidate for Phase-1 P1 if budget pressured
│
└── NO  → Mechanical composition alone does NOT produce perceptible distinctness
          Layer 4 LLM flavor is FOUNDATION, not augmentation
          Reflection IV validated; Layer 4 scope-cut is dangerous
          Surface to substrate-expansion-decision § 5.7 amendment as architectural commitment
```

### § 6.3 — Edge cases

- **Phase 1 ambiguous (one subject passes, one fails):** recruit Phase 2 subjects per § 4.1
- **Both subjects fail pair-recovery but pass within/cross-pair similarity:** the metric works at coarse level but pair-discrimination fails; suggests substrate-level similarity but archetype-level confusion; surface for more nuanced metric design
- **Vocabulary-control quad outperforms mechanical-pair quartet on distinctness:** LLM vocabulary is providing more perceived distinctness than mechanical parameters; Layer 4 is more load-bearing than expected; strongly support against Layer-4 scope-cuts

---

## § 7 — Risks + mitigations

### § 7.1 — Risk: Subject familiarity bias

Matt and Matt's son know the project deeply; their pair-recovery may be inflated by knowledge of the architecture rather than perception of distinctness.

**Mitigation:** Withhold substrate names + mechanical details during sessions (§ 4.3). The subjects can perceive the architecture's existence; they should not perceive *which substrate or archetype* is being played.

### § 7.2 — Risk: 90-second fight is too short for perception

Some archetypes may have their distinctness emerge only over longer play (multi-fight matchup adaptation; build evolution).

**Mitigation:** Document this limitation explicitly. The experiment measures *first-pass perceived identity*, which is appropriate for the Layer-3 gate (which evaluates archetypes at composition time, not at multi-hour play time). If perception requires longer-play sampling, that itself is a Layer-3 finding worth surfacing.

### § 7.3 — Risk: Reference-monster encounter is unrepresentative

Single reference monster may not exercise all archetype facets.

**Mitigation:** Use a reference monster that requires diverse player responses (some kiting, some commitment, some mobility). Drax to spec the reference monster shape; jack-ryan reviews for representativeness.

### § 7.4 — Risk: Vocabulary-control quad is hard to suppress

LLM may "leak" substrate-specific vocabulary even when prompted to be generic.

**Mitigation:** Pre-review vocabulary outputs before sessions; manual edit any leaks. The experiment is small enough that hand-curation is feasible.

### § 7.5 — Risk: 2-subject sample is too small

Single-pair recovery test with 2 subjects is signal-detection, not validated measurement.

**Mitigation:** Acknowledged in § 4.1. Phase 2 recruits if Phase 1 is ambiguous. The experiment is designed to detect *order-of-magnitude* failure modes, not to publish.

---

## § 8 — Phase-1 P1a positioning

### § 8.1 — Why P1a (prerequisite)

This experiment must run *before* Layer-3 is coded because:

1. The experiment's output determines Layer-3's metric shape (mechanical-parameter vs play-trace feature)
2. Building Layer-3 on the wrong metric and discovering it later is the failure mode the experiment exists to prevent
3. The experiment is 1-2 days; Layer-3 is 1-2 weeks; the experiment is cheap insurance

### § 8.2 — Sequencing

Per substrate-expansion-decision § 6 cascade order extended:

| Step | Item | Status |
|---|---|---|
| 1 | Design doc COMMITTED | ✅ |
| 2 | Decisions-log entry (knight-rider) | NOW DUE |
| 3 | Rocket Drift-14 amendment | ✅ |
| 4 | Pool D1 re-score | ✅ |
| 5 | VS2a + VS2b ship on canonical-four | in flight |
| **6a** | **Substrate identity declarations + spec** (this artifact + spec doc) | **gandalf authoring complete** |
| **6b** | **Perception test experiment** (this doc + execution) | **NEW Phase-1 P1a prerequisite** |
| 7 | Phase-1 P1 dispatch chain | queued after 6a+6b |

### § 8.3 — What blocks what

- Perception test execution is BLOCKED on drax session-runner readiness (not gandalf authorship; drax dispatch needed)
- Layer-3 metric spec authorship is BLOCKED on perception test results
- Layer-3 implementation is BLOCKED on Layer-3 metric spec
- Layer-2 composition refactor (Path a per § 5.7 amendment) is NOT blocked on perception test — can proceed in parallel

### § 8.4 — Estimated effort

| Task | Owner | Effort |
|---|---|---|
| Experiment design (this doc) | gandalf | ✅ done |
| Drax session-runner readiness | drax | ~1 day |
| Generate 4 mechanical pairs + 1 vocabulary quad | gandalf + drax | ~0.5 day |
| Run sessions (2 subjects, Phase 1) | drax + Matt + son | ~1 hour each = 2 hours |
| Analysis + decision call | jack-ryan + gandalf | ~0.5 day |
| Layer-3 metric spec (if needed) | gandalf | ~1 day |
| **Total Phase-1 P1a duration** | | **~3-4 days end-to-end** |

If Phase 2 recruitment is needed, add ~3-5 days for recruit + run + analyze.

---

## § 9 — Cross-references

- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` — Legolas Mode A Finding A (diversity-metric/perception gap) + top recommendation
- `canonical/story/substrate-expansion-decision-2026-05-17.md` § 6.5 — combinatorial-thinness success criterion; this experiment ensures Layer-3 doesn't optimize against an invalid metric
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — the substrate identity foundation that Layer 4 vocabulary draws from
- `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` — Layer-1 spec
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` — the convergence vectors (geometry-bias silent neutralization; stat-allocator fallback) the experiment empirically tests perception of
- `canonical/story/earth-self-diversity-tension-2026-05-17.md` — Court-as-grace; not directly tested but informs interpretation of vocabulary-control results

**Pending downstream:**

- Drax dispatch (knight-rider routing): session-runner readiness + reference-monster spec
- Layer-3 similarity-metric spec (gandalf authorship; depends on experiment results) — Task #7 pending
- Phase-1 P1 cascade re-sequencing (knight-rider; incorporates Phase-1 P1a as new prerequisite step) — Task #11 pending

---

*Authored 2026-05-17 by gandalf, per Legolas Mode A literature pass top recommendation. Phase-1 P1a perception-test experiment scoping. Prevents building Layer 3 on a perceptually-invalid metric. 1-2 day empirical insurance against a 1-2 week-of-engineering loss.*
