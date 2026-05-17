# Research — Five-Layer Procedural Diversity Architecture: Literature & Industry Precedent Pass — 2026-05-17

**Mode:** A (analytical)
**Commissioner:** gandalf (design pre-work, architecture-adjustment inputs)
**Sources consulted:** Academic PCG literature 2022-2026; GGG/PoE postmortem material; Hades II design analysis; Last Epoch mastery-system coverage; Diablo IV live-service telemetry case material; LLM-PCG integration surveys; QD/novelty-search literature; player-cognition research; industry practitioners on LLM costs and vendor risk.

---

## 1. Executive Summary

**Top three surprises from the literature pass:**

1. **The diversity-metric/perception gap is unsolved and fundamental.** The field has no validated single metric for "perceptually distinct" content. Existing diversity metrics (edit distance, behavior descriptors, MAP-Elites archive coverage) are regularly shown to misalign with player-perceived distinctness. An architecture that gates on a mirror-match similarity score (Layer 3) is therefore gating on a proxy that has not been empirically validated against player perception — and the field has documented this gap explicitly (Chand et al., "Measuring Diversity of Game Scenarios," 2024).

2. **LLM flavor-layer dependency is much costlier than a surface read suggests.** The blockers to mainstream LLM adoption in games are not just hallucination. They are: context window insufficiency for long-session coherence, per-player API cost at scale, fundamental instruction-adherence failures under multi-constraint prompts, and the "1,000x effort from proof-of-concept to production" gap (Marek Rosa, 2024). Layer 4 sits entirely on this foundation. Its risk profile is higher than the architecture currently acknowledges.

3. **Identity-constrained composition produces combinatorial thinness, not just starvation.** The failure mode the literature most consistently surfaces is not "zero valid archetypes" but "a few valid archetypes, repeated across many seeds." This is structurally distinct from starvation: the generator is technically valid but explores a narrow effective space. The Grim Dawn dual-class system (acknowledged design success) shows that even a combinatorially large space (15 masteries = ~105 pairings) collapses to ~5-8 dominant build patterns in practice. Mechanical validity does not guarantee breadth of actual play patterns.

**Top three failure-mode risks the architecture has not fully addressed:**

1. **Layer 3's similarity metric is not grounded in player-perceptible behavior.** The architecture specifies a distance threshold T but does not specify what the distance is measuring. If it measures mechanical-parameter vectors, not play-trace outputs, technically distinct archetypes will still feel identical in play.

2. **Layer 5 will oscillate unless it has an explicit damping mechanism.** The live-service balance literature documents overcorrection as the dominant failure mode (The First Descendant, 2024; Diablo IV seasonal oscillation). A feedback loop that increases diversity pressure after convergence will overshoot if there is no damping coefficient.

3. **The meta-arc rhythm is in direct tension with Layer 4 diversity pressure.** Reincarnated's Earth Self meta-progression rewards returning to familiar forms across seasons. Layer 4 pushes each season's archetypes to be surface-vocabulary-novel. These pull in opposite directions; the architecture does not address this explicitly.

**Top recommendation:** Before implementing Layer 3, define the similarity metric in terms of play-trace features (not mechanical-parameter vectors), and validate it against player perception in a small study. An architecture that gates diversity on an unvalidated proxy will generate a system that is technically diverse but perceptually identical.

---

## 2. Per-Layer Failure-Mode Review

### Layer 1 — Substrate Identity Declaration

**What the field says:** Designer-authored constraint systems are a well-validated pattern. The PoE ascendancy class system, Hades II's god-identity boon categories, and Last Epoch's mastery architecture all demonstrate that designer-authored identity declarations can produce genuine mechanical distinctness. The pattern is not itself suspect. What the field has identified are the maintenance and governance failure modes.

**Failure mode 1.1 — Semantic drift between declaration and generation behavior.**
Academic PCG literature consistently notes that when generators evolve and constraint systems don't, the constraints become stale. This is the equivalent of software test rot: the declaration says "forbidden_mechanics includes area-of-effect" but post-v4 primitive additions have quietly introduced radial geometry that is functionally AoE. No paper uses exactly this framing, but the design-centric PCG analysis literature (McMaster University PCG analysis, archived) treats constraint-generator sync as a first-class maintenance problem. In shipped games: PoE's skill-gem system accumulated enough cross-gem interactions over years that the original class-identity constraints became contradicted by emergent combinations. GGG's response has been periodic "rework" leagues that re-ground identity declarations — an acknowledgment that drift happens and requires active intervention.

**Failure mode 1.2 — Ownership contention / design-by-committee drift.**
The identity declaration for "what holy means mechanically" is the kind of question that attracts revision from multiple stakeholders (game director, balance lead, narrative lead). Without a single owner and a formal change-management gate, identity declarations accumulate amendments that quietly erode their mechanical distinctness. This is not documented in academic literature (it is a production governance problem, not an algorithmic one), but it is visible in Diablo IV's development: class fundamentals shifted between beta and release and continued shifting through Seasons 1-3 as different teams iterated, resulting in player perception of class identity instability that Blizzard's own forums document extensively (2023-2024 forum threads on class distinctness).

**Failure mode 1.3 — `cosmological_commitment` phrasings under/over-constrain in non-obvious ways.**
Natural-language fields in a constraint system are an implicit LLM-prompt structure even when no LLM is in the loop. The problem is scope ambiguity: "shadow is the substrate of hidden costs and deferred consequence" can be read by a generator as "shadow archetypes must have delayed effects" (reasonable) or "shadow archetypes cannot have immediate effects" (over-constraining; eliminates burst-damage shadow archetypes). This is structurally analogous to the LLM hallucination problem but in the interpretation layer. The academic literature on Knowledge Management Systems for LLM narrative pipelines (MDPI Systems, 2025 — G-KMS paper) explicitly addresses this: schema-governed generation with normalization-based repair is needed when natural-language fields are used as generative constraints, precisely because natural language is under-specified.

**Failure mode 1.4 — Player customization conflicts.**
Substrate identity declarations constrain generator output; they do not constrain player expectations. If a player's desired build concept (an aggressive, close-range holy paladin) is blocked by the identity declaration (holy has `forbidden_mechanics: melee-range`), the player perceives identity constraints as arbitrary restrictions rather than coherent design. This is documented in PoE community discussion: the prohibition on certain skill-ascendancy combinations that "should thematically fit" has been a recurring friction point since 2019. PoE 2's design response — decoupling skills from class ascendancies more aggressively — is a direct reaction to this failure mode.

---

### Layer 2 — Identity-Constrained Composition

**What the field says:** Constraint-intersection-based archetype generation has sound theoretical grounding. The quality-diversity literature shows that constraint-pruning of a combinatorial search space is preferable to unconstrained search because it prevents the "collapse to mean" problem (Gravina et al., "Quality Diversity: A New Frontier for Evolutionary Computation," Frontiers in Robotics and AI, 2016; Pugh et al., same volume). However, the specific failure modes of intersection-based pruning are well-documented.

**Failure mode 2.1 — Thinness without starvation.**
This is the most commonly missed failure mode. The system produces technically valid archetypes but explores only a narrow slice of the possible space because the intersection `role_primitives ∩ substrate_identity_primitives − forbidden_mechanics` converges on a small effective region. The Grim Dawn case is instructive: 15 masteries yield 105 possible pairings, but community analysis consistently identifies 5-8 dominant play patterns. The Diablo IV Season 10 "build diversity" coverage describes the same phenomenon: multiple technically distinct builds, but the effective game meta converges on 2-3 patterns. The mechanism is not the constraint intersection but the downstream power-level evaluation: certain primitive combinations are structurally stronger, so diversity-gate approval still permits a set that is mechanically over-represented in strong-build territory.

**Failure mode 2.2 — Combinatorial explosion in primitive enumeration.**
If role_primitives are not carefully scoped, adding substrates multiplicatively increases the constraint-intersection search space. Expanding from 4 to 7 substrates is a 75% increase in substrate space; if each substrate adds identity primitives, the intersection computation grows non-linearly. For offline generation this is typically manageable, but if Layer 2 runs at season-generation time with tight latency budgets, the enumeration cost matters. The PCG literature on high-dimensional procedural content (arXiv 2602.18943, 2026) notes this as a scaling concern for constraint-satisfaction PCG.

**Failure mode 2.3 — Identity constraints interact across substrates non-additively.**
Constraints defined independently per substrate may produce unexpected emergent exclusions when combined. If lightning's identity_declaration includes `geometry_affinities: linear-chain` and a support-role archetype's `role_primitives` include `area_sustain`, the intersection may be empty in ways not apparent from reading either constraint in isolation. The G-KMS paper (MDPI Systems, 2025) and the "Constraint Is All You Need" FDG paper (2025) both specifically address this: "normalization-based repair" and "validation loops" are recommended precisely because constraint systems of moderate complexity regularly produce empty or invalid intersections that are not visible from individual constraint inspection.

---

### Layer 3 — Mirror-Match Diversity Gate

**What the field says:** This is the closest layer to a Quality Diversity (QD) algorithm in the academic sense. The mirror-match gate is a novelty-pressure mechanism applied to archetype outputs. The literature on this is rich and has surfaced several specific failure modes.

**Failure mode 3.1 — Behavior descriptor mismatch (the field's most-documented QD failure mode).**
QD algorithms define diversity over a "behavior descriptor" — a set of features chosen to represent the space of possible behaviors. The central challenge is that the choice of descriptor determines what diversity means. If descriptors are mechanical parameters (damage type, range, resource type), two archetypes that are mechanically parametrically distinct can produce identical play experiences. Chand et al. (2024, "Measuring Diversity of Game Scenarios," arXiv:2404.15192) explicitly state: "no such single metric universally captures all dimensions of diversity" and reference Osborn & Mateas's Gamalyzer tool as evidence that computational diversity metrics "often misalign with human perception." The 2024 OpenReview paper "Perceptual Metrics for Video Game Playstyle Similarity and Diversity" develops perceptual kernels rooted in cognitive psychology specifically to address this gap. Both papers are clear: if the mirror-match distance is computed over mechanical-parameter vectors, the gate will approve archetypes that play identically.

**Failure mode 3.2 — Threshold T is a hyper-parameter with no principled calibration method.**
MAP-Elites and related QD approaches require behavioral descriptor resolution choices that have the same sensitivity problem as T. Small changes in grid resolution (or distance threshold) produce large changes in archive coverage. The MAP-Elites literature documents this as a known limitation: "stagnation in regions of unreachable feature space" (EmergentMind MAP-Elites overview, 2024). For a diversity gate, this means T calibrated on one substrate set may be entirely wrong after substrate expansion. The 4→7 substrate expansion will require T recalibration; there is no principled formula for doing so.

**Failure mode 3.3 — Gate over-rejection collapses generation throughput.**
If the effective valid archetype space (after Layer 2 constraints) is small and T is high, the gate will reject most generated archetypes and the generation loop will stall. This is the "novelty search starvation" case: when the constraint space is tight, genuinely novel archetypes are rare, and repeated sampling does not find them. The constrained novelty search literature (Liapis et al., "Constrained Novelty Search: A Study on Game Content Generation," Evolutionary Computation, 2015) specifically documents this: "for large search spaces with multiple constraints, it is hard to find a set of feasible individuals that is both large and diverse." The 4→7 substrate expansion increases constraint space; if identity declarations are tight, this failure mode becomes more likely.

**Failure mode 3.4 — Deceptive fitness in MAP-Elites cells.**
SHINE algorithm comparisons to MAP-Elites (referenced in the MAP-Elites literature survey, 2024) show that MAP-Elites underperforms on problems where the fitness objective is deceptive: cells fill with locally-optimal solutions that block the search from finding globally-novel behaviors. In a diversity gate context: if the distance metric rewards parameter novelty, the gate will fill its "approved" archetype pool with parametrically-varied archetypes that are all locally-optimal damage-dealers (because damage-dealing primitives are the strongest in the power hierarchy), crowding out mechanically-weaker-but-experientially-distinct control archetypes.

---

### Layer 4 — LLM as Flavor Diversifier

**What the field says:** This is the most empirically underexplored layer in the architecture, and the field's evidence on it is cautionary.

**Failure mode 4.1 — Hallucination produces mechanically invalid flavor at non-trivial rates.**
The 2024 PCG-LLM survey (arXiv:2410.15644) and the AI Roguelite case study document that LLMs produce outputs that violate specified constraints even when those constraints are explicit in the prompt. The cited AI Roguelite behavior — "sometimes the AI will decide that you take damage and instantly die just for talking with a friendly NPC" — is an example of instruction-adherence failure under complex constraint prompts. The G-KMS paper (2025) proposes "normalization-based repair" and "engine-aligned knowledge admission" specifically because constraint violations are common enough to require a systematic repair pipeline, not just a retry. Without a repair pipeline, Layer 4 flavor output must be human-reviewed before ingestion.

**Failure mode 4.2 — Output instability across re-generations.**
LLMs are stochastic systems. The same prompt on two consecutive runs can produce qualitatively different outputs. This instability is documented in the Marek Rosa (2024) analysis as a fundamental barrier to production use: "models only attend perfectly to some instructions in the context and often hallucinate." For season generation, this means that the LLM may produce a high-quality ailment-timing vocabulary in Season 3 and a significantly lower-quality one in Season 5 with no change to the prompt. Output quality is not monotone in season number.

**Failure mode 4.3 — LLM bias toward training-data-frequent vocabulary.**
LLMs are trained on corpora where fire/lightning/light archetypes are massively over-represented in fantasy RPG content. Shadow and "holy" as mechanically-distinct-from-light archetypes are rare in training data. This means Layer 4 flavor outputs for shadow and novel substrates will systematically under-diversify: the LLM will reach for fire-adjacent vocabulary and mechanics even when prompted for shadow-specific variants. There is no paper that documents this for archetype generation specifically, but the LLM bias literature (training data frequency effects on output distributions) predicts this behavior. The architecture has no mechanism to detect or correct it.

**Failure mode 4.4 — Token cost is a structural dependency, not a marginal one.**
Marek Rosa (2024) identifies per-player API cost as the primary barrier to LLM integration in shipped games: "using LLM via API means someone has to pay for those thousands of tokens per hour per player." For Reincarnated's per-season archetype generation, the cost profile is different (season-level generation, not per-player-session), but the structural dependency remains: the architecture requires LLM API access to produce season content. If the API is unavailable, deprecated (model versions), or cost-prohibitive in a future pricing environment, Layer 4 fails silently or blocks season generation. Inference prices have fallen dramatically (10x annually; GPT-4 equivalent at $0.40/million tokens in 2026 vs. $20 in 2022), but the dependency on an external vendor for core content generation is a risk category the architecture should name explicitly.

**Failure mode 4.5 — LLM creative drift as models change.**
The architecture does not specify which LLM provides Layer 4 flavor. As models are updated or deprecated, flavor output style will change non-deterministically. Season 3 flavor vocabulary generated with Claude Sonnet 4.5 will not match Season 8 vocabulary generated with a future model. This is not a quality problem in isolation; it is a coherence problem over the multi-season arc that Reincarnated's Earth Self meta-progression depends on.

**Failure mode 4.6 — Prompt injection in player-facing surface.**
If any player-contributed text reaches the Layer 4 LLM prompt (via character names, guild tags, or other user inputs), prompt injection attacks become possible. OWASP's LLM Top 10 (2025 edition) rates prompt injection as the #1 LLM security risk. The architecture does not describe its prompt structure in enough detail to assess this risk, but it is a required consideration before any player-facing deployment.

---

### Layer 5 — Player-Telemetry Adaptation Loop

**What the field says:** Player-telemetry-driven content adaptation is an emerging practice in live-service games. The field documents success cases but also consistent failure modes around feedback loop dynamics.

**Failure mode 5.1 — Oscillation / overcorrection.**
This is the most consistently documented live-service failure mode. The First Descendant (2024) is the clearest documented case: power-inflation feedback caused content-consumption to outpace content-generation, then overcorrection caused player alienation. Diablo IV's community forums document multiple seasons where Blizzard's balance response to telemetry data produced overcorrections perceived as arbitrary nerfs. The general pattern: a feedback loop without a damping coefficient will oscillate because the signal (player build convergence) is collected over a delay window and the correction is applied in discrete season-sized increments. A damping mechanism — limiting the magnitude of per-season identity-weight adjustment — is required and the architecture does not specify one.

**Failure mode 5.2 — Perception lag creates contradictory player experiences.**
Players do not all update simultaneously. When Layer 5 pushes Season 5's archetypes apart because Season 4's builds converged, players who are still playing Season 4 (or are new to the game in Season 5) experience the Season 5 archetypes as unfamiliar without understanding why they changed. This is structurally the same problem that PoE faces every league reset: returning players lose their frame of reference. The PoE design response has been to maintain a set of "evergreen" archetypes that persist across leagues. The Reincarnated architecture has no equivalent mechanism.

**Failure mode 5.3 — Cold start: no data for Seasons 1-3.**
Layer 5 requires accumulated telemetry to produce signal. Seasons 1-2 have no prior telemetry; Season 3 has minimal data. The architecture must specify what Layer 5 does in the cold-start window. The academic literature addresses this for personalized content generation (arXiv:2402.10133, "Zero-Shot Reasoning: Personalized Content Generation Without the Cold Start Problem," 2024), but that paper's solution is zero-shot LLM reasoning as a proxy for telemetry — essentially using Layer 4 to bootstrap Layer 5. The architecture does not describe a cold-start protocol.

**Failure mode 5.4 — Whale/high-engagement overfitting.**
Player telemetry is typically dominated by high-engagement players who complete more build experiments per season. If Layer 5 weights its convergence signal uniformly across all telemetry, it will overfit to high-engagement whale behavior and generate archetype diversity pressure that has no relationship to the casual-player experience. This is not a PCG-specific finding; it is documented broadly in live-service game analytics literature. The architecture does not specify how it will segment the telemetry population.

**Failure mode 5.5 — Feedback produces numbers-diversity without experiential diversity.**
The most subtle and under-documented failure mode: when the feedback loop successfully pushes archetypes "apart" in parameter space, the result may be archetypes that have different number distributions but play identically at the level of player action patterns. This is the same problem as Layer 3's descriptor mismatch, but manifesting in the feedback path. The ixiegaming.com PCG-telemetry article names this directly: "meaningless variety — different layouts, same boring experience" as a failure mode telemetry aims to prevent but does not automatically solve.

---

## 3. Considerations the Architecture Does Not Address

**3.1 — Cognitive load of ~20-28 distinct archetypes.**
Player research literature on choice overload (playerresearch.com, 2024) identifies 7 as the working-memory threshold. Beyond ~7 simultaneous options, choice deferral and post-choice dissatisfaction increase. The architecture's projected output (7 substrates × 4 roles × diversity-gate-pruned = potentially 20-28 mechanically distinct archetypes per season) substantially exceeds this threshold. Critically, the research shows domain-novices are most affected; experienced players handle large option sets better. Reincarnated's seasonal onboarding rhythm means every season introduces new players who will face the full archetype pool as novices. The mitigation strategies identified in the literature are: temporal reduction (show fewer options initially), categorization (group archetypes clearly), and recommendation (Spirit Guide's marginal-value analysis could serve this function). The architecture should specify which of these applies.

**3.2 — Asset pipeline coupling.**
The architecture generates mechanical diversity. Mechanical diversity becomes perceptual diversity only when VFX, character art, and sound are correspondingly distinct. The art pipeline analysis (ixiegaming.com, 2025) notes that procedural content diversity requires corresponding asset system diversity. Reincarnated's current asset strategy (pimen pixel sprites + VFX packs) was not designed around 20-28 mechanically distinct archetypes. If a shadow archetype and a holy archetype share VFX, players will perceive them as mechanically similar regardless of the parameter differences. This is a known decoupling risk in the PCG diversity literature: mechanical diversity is necessary but not sufficient for perceived diversity. The architecture is silent on asset pipeline implications.

**3.3 — Boss and encounter symmetry.**
The architecture addresses player-class generation exclusively. If enemy/boss generation does not have a corresponding identity-constrained architecture, the diversity gate will produce distinct player archetypes that all face the same homogeneous enemy pool. This breaks the diversity value proposition: a shadow-affliction archetype is only experientially distinct if it faces encounters that respond distinctly to affliction mechanics. PoE's encounter design evolved to explicitly incorporate class-mechanic interactions (e.g., ailment-immune bosses forcing build reconsideration). The architecture's value is diminished without a corresponding enemy diversity design.

**3.4 — Balance validation computational cost.**
Gamora's balance loop currently validates a smaller archetype set. Each archetype added by the 4→7 substrate expansion increases the number of mirror-match pairs the balance loop must evaluate. If the diversity gate produces 28 archetypes, mirror-match validation requires O(N²) pair evaluations = 378 pairs. At current balance-loop speeds, this may be computationally expensive at season-generation time. The architecture does not specify whether Layer 3's mirror-match gate is the same infrastructure as gamora's balance loop or an additional validation pass.

**3.5 — The spirit-swap meta-arc tension.**
Reincarnated's Earth Self mechanic accumulates forms across seasons. Players develop attachment to specific archetype shapes. The architecture's diversity pressure (Layer 3 + Layer 5) is designed to push each season's archetypes toward novelty. These goals conflict: novelty-per-season is valuable for discovery; familiarity-across-seasons is valuable for identity. The architecture does not specify where on this tension axis it wants to sit, nor does it have a mechanism for preserving "heritage archetype shapes" that recur across seasons at acceptable similarity distances from prior seasons. The Pokémon game series has addressed a version of this with "legacy" forms; seasonal ARPGs like PoE have addressed it with "evergreen builds." The architecture needs an equivalent.

**3.6 — Long-tail constraint contradiction.**
At 18 months and 50+ accumulated archetypes, the diversity gate's constraint space becomes an active landmine. Archetypes approved in Season 2 establish "occupied" regions of the behavior space; the gate must not only approve new archetypes for internal diversity but ensure they don't resemble any previously approved archetype across all seasons. The gate's effective search space shrinks monotonically as the archetype library grows. The architecture does not specify whether the gate operates only within-season or across the entire accumulated archetype history, and it does not address the increasing starvation risk as the history grows.

**3.7 — LLM vendor dependency as a structural risk.**
Layer 4 requires an LLM vendor. The architecture does not specify whether this is Anthropic, OpenAI, a local model, or an abstraction layer. The vendor dependency risk is real: model deprecations, API pricing changes, and capability regressions across model versions are all documented in the 2024-2025 inference cost and vendor-lock-in literature (Bluebag AI, 2025; Epoch AI inference pricing analysis, 2025). A local fallback (small language model, on-device inference) exists as a mitigation but has documented quality gaps. The architecture should specify the fallback path for Layer 4 when the LLM vendor is unavailable or changes pricing.

---

## 4. Validated Alternatives

**4.1 — Pure designer-authored archetype pools (no composition, no LLM).**
The Slay the Spire model: each character has a fixed card pool designed by hand. Ironclad has the clearest archetype separation; Silent and Defect have more overlap (community analysis, Tao of Gaming, 2021). This produces the strongest experiential distinctness because each archetype is expressly authored for that purpose. Failure mode: does not scale to 7 substrates × 4 roles without proportional authoring cost. Suitable as a supplementary validation pass — Layer 2 outputs could be reviewed against designer-authored "reference archetypes" to check coherence — but not viable as the primary generation method at this team's capacity.

**4.2 — Pure MAP-Elites / QD search (no identity declarations).**
Gravina et al. (2019) and Chand et al. (2024) demonstrate QD approaches to PCG. Without identity declarations, MAP-Elites explores the full behavior space and fills an archive with the most diverse high-quality solutions found. Failure modes: requires a defined behavior descriptor (the descriptor-mismatch problem still applies); computationally intensive at high-dimensional archetype parameter spaces; produces content without cosmological coherence (mechanically novel but narratively incoherent). Not viable as a standalone replacement because it removes the substrate-identity semantic layer that is load-bearing for the game's thematic architecture.

**4.3 — Constraint-satisfaction only (no LLM, no telemetry).**
Layer 2 + Layer 3 without Layers 4 and 5. The "Constraint Is All You Need" paper (FDG 2025) demonstrates that constraint-based generation can produce structurally valid, diverse content without LLM augmentation. Relevant comparison: this is the version of the architecture with the lowest risk profile (no vendor dependency, no feedback oscillation risk), but also the weakest surface-vocabulary diversity. The trade-off is principled: mechanical diversity without surface diversity. This is a viable conservative baseline that Layers 4 and 5 can be added to incrementally.

**4.4 — LLM-only (LLM does full archetype generation).**
Not validated for mechanically coherent archetype generation at production quality. The "Grounding Machine Creativity" paper (arXiv:2603.07101, 2026) demonstrates LLM-driven synthesis of goal-playable patterns under structural constraints; the success rate (>80% playable-novel rate) is promising for level generation but not directly applicable to archetype generation. The Marek Rosa (2024) analysis is clear that LLM-only approaches require "1,000x more effort from proof-of-concept to production" for gameplay-load-bearing content. Not recommended as a standalone approach for the archetype generation core.

**4.5 — Hybrid: constraint-satisfaction core + LLM as validator (not generator).**
This inversion of Layer 4's role is supported by the LLM-PCG literature: rather than using LLM to generate flavor, use LLM to validate that generated flavor satisfies thematic coherence constraints. The G-KMS paper (2025) uses exactly this pattern: LLM as a normalization-and-repair agent rather than a primary generative agent. Risk profile is substantially lower because LLM outputs are constrained to yes/no or repair recommendations, not open-ended generation. Hallucination in a validation role produces a false reject or false pass, both recoverable errors. Hallucination in a generation role produces mechanically invalid content that may pass downstream validation if the validator isn't robust.

**4.6 — Diversity from human feedback (RLHF-style diversity pressure).**
The arXiv paper "Diversity from Human Feedback" (arXiv:2310.06648, 2023) proposes a method where human preference feedback is used to steer generation diversity rather than quality. This is a research-stage approach but is directly relevant to Layer 5's goal. Rather than using play telemetry to signal convergence, this approach uses explicit player diversity preferences. Risk: requires human feedback infrastructure. Benefit: directly captures player-perceptible diversity rather than mechanical-parameter diversity.

---

## 5. Recommended Adjustments

**R1 — Layer 3: Ground the similarity metric in play-trace features before implementing.**
Before coding the mirror-match gate, specify what vectors T operates on. Recommendation: use play-trace features (action pattern distributions, resource-type usage rates, positioning behavior) rather than mechanical-parameter vectors. This requires a simulation pass to generate play traces from generated archetypes, which adds latency but grounds the diversity signal in player-perceptible behavior. If play-trace simulation is too expensive for the gate, at minimum add a "perceptual sanity check" pass after the gate that spot-checks gate-approved archetypes for gameplay similarity. Source: Chand et al. (2024); OpenReview perceptual metrics paper (2024).

**R2 — Layer 3: Add a minimum valid-archetype floor before T recalibration.**
Specify a floor: "if fewer than N archetypes pass the gate, reduce T by δ until N archetypes pass." This prevents starvation during the 4→7 substrate expansion. Separately, document T recalibration as a required step after each substrate addition. Source: MAP-Elites stagnation literature (2024); constrained novelty search starvation (Liapis et al., 2015).

**R3 — Layer 4: Add a post-generation schema validator and repair loop before any LLM flavor output touches the archetype record.**
The G-KMS pattern (2025) is directly applicable: LLM generates flavor → normalization step checks against substrate identity declaration → repair loop corrects violations → engine-aligned admission gate accepts only repaired output. This prevents hallucination-produced mechanical-invalidity from propagating into the archetype pool. Source: G-KMS (MDPI Systems, 2025); "Constraint Is All You Need" (FDG 2025).

**R4 — Layer 4: Specify a model-agnostic abstraction layer with a local-model fallback.**
The Layer 4 prompt chain should be abstracted over an LLM interface, not bound to a specific API. Specify a local small-model fallback (lower quality but zero vendor dependency) that activates when the primary API is unavailable. Document that flavor quality will degrade in fallback mode and that degraded-quality seasons are acceptable. Source: Bluebag AI vendor lock-in analysis (2025); Epoch AI inference pricing trends (2025).

**R5 — Layer 5: Add an explicit damping coefficient to the identity-weight update rule.**
Specify that per-season identity-weight adjustments are capped at ±δ_max regardless of the convergence signal magnitude. This prevents overcorrection oscillation. A reasonable starting value is δ_max ≈ 10-15% of the current weight. Source: The First Descendant overcorrection case (2024); Diablo IV balance oscillation community documentation (2023-2024).

**R6 — Layer 5: Define a cold-start protocol for Seasons 1-3.**
For seasons with insufficient telemetry (threshold: fewer than N complete season-playthroughs), Layer 5 should not run. Instead, use a designer-authored diversity target (a reference set of "maximally distinct" archetype shapes authored manually) as the Season 1-3 diversity constraint. This bootstrap reference set replaces the telemetry signal until data accumulates. Source: arXiv:2402.10133 zero-shot reasoning cold-start mitigation (2024).

**R7 — Add a "heritage archetype" mechanism to address the meta-arc tension.**
Define a small set of archetype shapes (1-2 per substrate) that are designated "heritage" and persist across seasons at controlled similarity distances. These anchor the Earth Self meta-progression by giving returning players a familiar form to anchor to, while non-heritage archetypes rotate freely under the diversity gate. Source: PoE evergreen-build design philosophy; Supergiant's iterative design-as-document approach (GamesRadar, 2024).

**R8 — Layer 1: Specify a formal change-management gate for identity declaration amendments.**
Identity declarations should be versioned. Any amendment to a `forbidden_mechanics`, `mechanical_signature`, or `cosmological_commitment` field should require a documented decision (who, why, what impact on existing archetypes) before merging. This prevents semantic drift and design-by-committee erosion. Source: PCG constraint maintenance analysis; PoE skill-gem rework patterns.

---

## 6. Sources Catalog

| # | Title | Author(s) | Year | URL / Reference |
|---|---|---|---|---|
| S1 | "Measuring Diversity of Game Scenarios" | Chand et al. | 2024 | https://arxiv.org/html/2404.15192v1 |
| S2 | "Procedural Content Generation in Games: A Survey with Insights on Emerging LLM Integration" | Multiple authors | 2024 | https://arxiv.org/html/2410.15644v1 |
| S3 | "Quality Diversity: A New Frontier for Evolutionary Computation" | Pugh, Soros, Stanley | 2016 | https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full |
| S4 | "Constrained Novelty Search: A Study on Game Content Generation" | Liapis et al. | 2015 | https://dl.acm.org/doi/10.1162/EVCO_a_00123 |
| S5 | "Procedural Content Generation through Quality Diversity" | Gravina et al. | 2019 | https://comnplayscience.eu/wp-content/uploads/2019/10/Gravina-et-al.-2019-Procedural-Content-Generation-through-Quality-Dive.pdf |
| S6 | "Abandoning Objectives: Evolution Through the Search for Novelty Alone" | Lehman & Stanley | 2011 | https://dl.acm.org/doi/abs/10.1162/EVCO_a_00025 |
| S7 | "Constraint Is All You Need: Optimization-Based 3D Level Generation with LLMs" | FDG 2025 | 2025 | https://dl.acm.org/doi/10.1145/3723498.3723840 |
| S8 | "Game Knowledge Management System: Schema-Governed LLM Pipeline for Executable Narrative Generation in RPGs" (G-KMS) | Multiple authors | 2025 | https://www.mdpi.com/2079-8954/14/2/175 |
| S9 | "Why haven't we seen any mainstream games utilizing LLM-driven AI NPCs?" | Marek Rosa | 2024 | https://blog.marekrosa.org/2024/05/why-havent-we-seen-any-mainstream-games/ |
| S10 | "Perceptual Metrics for Video Game Playstyle Similarity and Diversity" | Multiple authors | 2024 | https://openreview.net/forum?id=hfAEEsIQ6D |
| S11 | MAP-Elites algorithm overview and failure mode documentation | EmergentMind | 2024 | https://www.emergentmind.com/topics/map-elites-algorithm |
| S12 | CMA-ME: Covariance Matrix Adaptation MAP-Elites | EmergentMind | 2024 | https://www.emergentmind.com/topics/covariance-matrix-adaptation-map-elites-cma-me |
| S13 | DCRL-MAP-Elites (GECCO 2023 Best Paper + ACM TELO 2024) | Adaptive Intelligent Robotics | 2023/2024 | https://github.com/adaptive-intelligent-robotics/DCRL-MAP-Elites |
| S14 | "Diversity from Human Feedback" | Multiple authors | 2023 | https://arxiv.org/html/2310.06648v2 |
| S15 | "Zero-Shot Reasoning: Personalized Content Generation Without the Cold Start Problem" | Multiple authors | 2024 | https://arxiv.org/abs/2402.10133 |
| S16 | "Grounding Machine Creativity in Game Design Knowledge Representations" | Multiple authors | 2026 | https://arxiv.org/html/2603.07101v2 |
| S17 | "Spoiled for choice: The psychology of choice overload in games" | Player Research | 2024 | https://www.playerresearch.com/learn/spoiled-for-choice-the-psychology-of-choice-overload-in-games-and-how-to-avoid-it/ |
| S18 | "How power inflation compromises live service games" | Game Developer | 2024 | https://www.gamedeveloper.com/design/how-power-inflation-compromises-live-service-games-like-the-first-descendant |
| S19 | "PCG + Telemetry in Games: How to Build Scalable, Player-Driven Content" | ixiegaming | 2024 | https://www.ixiegaming.com/blog/pcg-telemetry-the-feedback-loop-that-make-infinite-content-actually-work/ |
| S20 | "How Hades 2 creates build diversity by avoiding generic stats" | Roguelike Ravings | 2024 | https://medium.com/@moonalpacan/how-hades-2-creates-build-diversity-by-avoiding-generic-stats-6befdb258443 |
| S21 | PoE 2 meta analysis — Deadeye meta dominance (32-34% top-player concentration) | maxroll.gg | 2025 | https://maxroll.gg/poe2/meta/the-build-meta |
| S22 | "Diablo 4 reinvented itself by listening to what players want" | PC Gamer | 2023 | https://www.pcgamer.com/games/rpg/diablo-4-reinvented-itself-by-listening-to-what-players-want-but-not-by-doing-everything-they-suggested/ |
| S23 | "How to Avoid LLM Vendor Lock-in When Building AI Agents" | Bluebag AI | 2025 | https://www.bluebag.ai/blog/avoid-llm-vendor-lock-in |
| S24 | LLM inference price trends | Epoch AI | 2025 | https://epoch.ai/data-insights/llm-inference-price-trends |
| S25 | OWASP LLM Top 10 — Prompt Injection | OWASP GenAI Security | 2025 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| S26 | Last Epoch class and mastery introduction | maxroll.gg | 2024 | https://maxroll.gg/last-epoch/resources/class-and-mastery-introductions |
| S27 | "Grim Dawn's Dual Class System Deserves a Double Take" | wyrmpres | 2022 | https://wyrmpres.wordpress.com/2022/01/13/the-dual-class-system-in-grim-dawn-deserves-a-double-take/ |
| S28 | Hades 2 — "The game is the design document" (Supergiant iterative design) | GamesRadar | 2024 | https://www.gamesradar.com/games/hades/the-game-is-the-design-document |
| S29 | "Too Many Words about Slay the Spire, Pt II — The Characters" | Tao of Gaming | 2021 | https://taogaming.wordpress.com/2021/03/13/too-many-words-about-slay-the-spire-pt-ii-the-characters/ |
| S30 | Diablo 4 Season 10 build diversity coverage | itemd2r.com | 2025 | https://www.itemd2r.com/en/blog/diablo-4/diablo-4-season-10-a-new-era-of-build-diversity |
| S31 | "Designing Path of Exile to Be Played Forever" | GDC Vault | 2018 | https://www.gdcvault.com/play/1025784/Designing-Path-of-Exile-to |
| S32 | "A Survey of Search-Based Procedural Content Generation" | Multiple authors | 2023 | https://arxiv.org/pdf/2311.04710 |
| S33 | Quality-Diversity papers list (authoritative bibliography) | quality-diversity.github.io | ongoing | https://quality-diversity.github.io/papers.html |
| S34 | "Automated QA Testing for AI-Generated Game Content" | IJETCSIT | 2025 | https://ijetcsit.org/index.php/ijetcsit/article/view/471 |
| S35 | Balancing Live Service Games | Daantje on Data / Daniela Fontes | 2024 | https://danielafontes.com/2024/06/02/balancing-live-service-games/ |

---

## 7. Open Questions for Further Research

**OQ1 — Can play-trace diversity be measured at archetype-generation time without simulation?**
The recommendation to ground Layer 3's similarity metric in play-trace features assumes a simulation pass is feasible at generation time. If gamora's balance loop can produce play-trace feature vectors as a byproduct of balance validation, the diversity gate can use those vectors. If not, a separate simulation pass adds significant latency. This is a feasibility question for gamora + drax, not a research question.

**OQ2 — What is the effective "perceptual minimum distance" for ARPG archetypes?**
The field has not empirically answered: how different must two archetypes be, measured in what dimensions, before players reliably perceive them as distinct? Player Research's choice overload work gives aggregate thresholds for option sets, not pairwise distinctness thresholds. A small playtest study (5-10 players, 2-3 paired archetype variants) during Layer 3 calibration would generate actionable data the field does not currently provide.

**OQ3 — Is the cold-start problem for Layer 5 actually solved by the zero-shot LLM approach?**
The arXiv:2402.10133 paper proposes LLM zero-shot reasoning as a cold-start mitigation for personalized content generation. Whether this generalizes to archetype diversity pressure (a different problem domain) is not validated. Gandalf should assess whether the designer-authored bootstrap reference set (R6) is sufficient or whether the zero-shot approach is worth investigating for Season 1-2.

**OQ4 — Does the spirit-swap meta-arc rhythm favor stability or novelty more strongly?**
This is a design question, not a research question, but the architecture cannot be fully specified without an answer. If the meta-arc wants returning players to find familiar archetypes (stability preference), the heritage mechanism (R7) should cover a high fraction of archetypes. If the meta-arc wants returning players to find new forms (novelty preference), heritage coverage should be minimal. The tension is real and design must resolve it before Layer 5 weight updates are calibrated.

**OQ5 — What is the balance-loop computational cost of O(N²) mirror-match validation at N=28?**
This is a measurement question for gamora. If current balance-loop runtimes at N=12 archetypes are known, the O(N²) scaling gives an estimate for N=28. If the runtime is prohibitive, Layer 3's gate must run at a more restricted archetype count or use a faster approximate similarity metric.

**OQ6 — Has any game used per-substrate LLM prompt differentiation successfully?**
The specific concern (Layer 4 bias toward training-data-frequent substrates like fire/lightning) has not been directly studied in the literature. A targeted experiment — prompt a frontier LLM with shadow vs. fire substrate identity declarations and measure vocabulary overlap in outputs — would empirically validate or refute the bias hypothesis before investing in Layer 4 infrastructure.
