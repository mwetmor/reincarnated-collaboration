# Research — Cohesion-Judge LLM Call Architecture for Phase 5 Layered Narrative — 2026-05-27

**Mode:** A (analytical, Pattern A-deep)
**Commissioner:** knight-rider (SC-3 dispatch: `agentic_orchestration/dispatches/2026-05-27-legolas-cycle-14-sc-3-cohesion-judge-llm-research.md`)
**Wave gate:** Wave 3 (Phase 5 cohesion-judge LLM architecture)
**Authority:** Matt 2026-05-27 framing brief ratification Q5 (SC-3 confirmed)
**Discipline:** #18 — methodology-before-execution; this artifact IS the methodology consultation at the P5 cohesion-judge math hotspot

**Sources consulted:**
- [PANGeA: Procedural Artificial Narrative using Generative AI for Turn-Based Video Games (2024)](https://arxiv.org/abs/2404.19721)
- [ID-RAG: Identity Retrieval-Augmented Generation for Long-Horizon Persona Coherence in Generative Agents (2025)](https://arxiv.org/abs/2509.25299)
- [Echoes in AI: Quantifying lack of plot diversity in LLM outputs — PNAS (2025)](https://arxiv.org/abs/2501.00273)
- [The Price of Format: Diversity Collapse in LLMs (2025)](https://arxiv.org/abs/2505.18949)
- [LLM Output Homogenization is Task Dependent (2025)](https://arxiv.org/abs/2509.21267)
- [A Survey on LLM-as-a-Judge (2024/2025)](https://arxiv.org/abs/2411.15594)
- [Can You Trust LLM Judgments? Reliability of LLM-as-a-Judge (2024)](https://arxiv.org/abs/2412.12509)
- [Judge Reliability Harness: Stress Testing the Reliability of LLM Judges (2025)](https://arxiv.org/abs/2603.05399)
- [SCORE: Story Coherence and Retrieval Enhancement for AI Narratives (2025)](https://arxiv.org/abs/2503.23512)
- [Dynamic Context Adaptation for Consistent Role-Playing Agents with RAG (2025)](https://arxiv.org/abs/2508.02016)
- [Autorubric: Unifying Rubric-based LLM Evaluation (2025)](https://arxiv.org/abs/2603.00077)
- [RULERS: Locked Rubrics and Evidence-Anchored Scoring for Robust LLM Evaluation (2025)](https://arxiv.org/abs/2601.08654)
- [Addressing LLM Diversity by Infusing Random Concepts (2025)](https://arxiv.org/abs/2601.18053)
- Canonical docs: doc 46 §§ 7.1–7.5; doc 40 D7; doc 41; framing brief 2026-05-27; math-hotspot naming 2026-05-23 § 2.3

**Reincarnated-context anchor:** doc 46 Layer 6 defines the layered cohesion architecture this research must serve. The cohesion-judge LLM call at Phase 5 produces character_name + core_identity_narrative (CORE layer, T1-T3 chain composition weighted) + optional endgame_nod_narrative (ENDGAME layer, T4 + Legendary/Set themes additive). The LLM does NOT see raw chain content — it sees structured fields. At ~2,100 calls per season ($0.50–$5 total cost per framing brief § 9.2), the scale is tractable but AI-tell risk is real and compounds per call.

---

## Summary (5 sentences)

The literature strongly supports a **structured-output-with-layer-tags** architecture as the primary pattern for Phase 5, composing a weighted-substrate prompt that foregrounds T1–T3 chain identity as the CORE anchor with T4/gear content as a narrowly-scoped additive field — this directly implements doc 46 § 7.2's weighting hierarchy and is well-grounded in how LLM persona anchoring prevents identity drift. AI-tell failure at scale (~2,100 calls) is a documented phenomenon in the literature with a specific failure pattern: templated prompt structure causes output-space collapse even at high temperature, producing "echoed" outputs where the same phrases and archetypes recur across characters; mitigation requires per-character substrate diversity injection at the prompt-construction layer, not post-hoc generation. Rubric-based LLM judging with locked scoring criteria and multi-sample stochastic stability testing is the calibration methodology with the strongest empirical support for content validation use cases; single-shot judging is insufficient and tail behavior (rare but important edge cases) requires explicit test coverage. RAG-over-design-substrate (ID-RAG pattern) adds structural benefits for long-horizon consistency but introduces complexity that is unnecessary for Phase 5's bounded single-call-per-character shape; the lighter structured-output-with-layer-tags approach captures its benefits without the retrieval overhead. Three open questions for the Wave 3 design call: (1) whether the additive endgame nod is a second LLM pass or a structured field within a single call; (2) the specific rubric criteria for the three core discipline tests (doc 46 § 7.3); and (3) whether per-character substrate context injection is sufficient AI-tell mitigation or whether a post-generation diversity pass is needed at season scale.

---

## Findings

### Q-SC3-1: Architecture patterns for layered narrative identity (CORE + ENDGAME composition)

Four patterns were surveyed for their ability to produce layered identity where a CORE anchor and an ENDGAME nod compose into coherent character identity:

#### Pattern A: Hierarchical Prompt Decomposition (multi-pass)

In this pattern, the LLM runs two separate calls: Call 1 generates the CORE identity from T1–T3 chain content only; Call 2 receives the CORE output as a frozen anchor and generates the ENDGAME nod as a constrained addition. This mirrors the STORYVERSE and COLLABSTORY approach in the story-generation literature, where plot-point abstractions are resolved in separate passes to preserve author-intent across call boundaries.

**Strengths:** The CORE layer is generated with no contamination from gear/T4 content. The identity-without-gear test (doc 46 § 7.3A) passes by construction — the CORE call literally has no gear in scope. The endgame nod is structurally constrained because Call 2 receives CORE as a read-only anchor.

**Weaknesses:** Two LLM calls per character doubles the cost and latency. At 16 characters × 2 passes, the call overhead is manageable (~$1–$10 per season total, still tractable), but error surface doubles. The CORE output must be stable enough to serve as a reliable anchor for Call 2; instability in Call 1 propagates downstream.

**AI-tell risk:** Moderate. Each call is narrower in scope, which reduces the templated-output collapse risk per the diversity-collapse literature. However, Call 2 still receives a formatted CORE string, and the format-anchoring effect can reduce diversity in the endgame nod if CORE text patterns repeat across characters.

**Literature grounding:** Secondary (RPGAgent, CHI 2026; STORYVERSE 2024). No direct primary-source empirical validation of this pattern for game character cohesion.

#### Pattern B: Structured Output with Layer Tags (single-call, field-partitioned)

A single LLM call receives a structured prompt with explicitly labeled fields: CORE_LAYER (T1–T3 chain content), ENDGAME_LAYER (T4 + gear content), SUBSTRATE_CONTEXT (BC cell, element, cohort), THEMATIC_REGISTRY (genre vocabulary). The output is a structured response where the LLM fills narrow, labeled fields: character_name / core_identity_narrative / endgame_nod_narrative (optional, conditional on ENDGAME_LAYER content presence).

This is architecturally the pattern described in doc 46 § 7.4 and aligns directly with the D7 AI-tell discipline: "templated structure with LLM filling narrow blanks." The field-labeled structure constrains output shape without constraining thematic content.

**Strengths:** Single-call economy (cost stays at the ~$0.50–$5 per-season framing brief estimate). The CORE vs ENDGAME distinction is preserved at the prompt level via field labeling, not via separate calls. Conditioning on ENDGAME_LAYER content presence allows the endgame nod to be genuinely optional — if no gear/T4 data is supplied, the field is absent and the LLM produces CORE-only output, directly satisfying the identity-without-gear test.

**Weaknesses:** The LLM sees both CORE and ENDGAME content in the same context window. There is a risk that a rich ENDGAME_LAYER (named legendary item, specific T4 strategy) contaminates the CORE narrative if the LLM weighs those fields too heavily. This requires explicit prompt-level instruction about field weighting.

**AI-tell risk:** Moderate-low. Per the diversity-collapse literature (arXiv:2505.18949), structural tokens in templates constrain output space. The mitigation is per-character substrate diversity injection: the SUBSTRATE_CONTEXT and THEMATIC_REGISTRY fields must be character-specific and lexically varied, not generic fixed strings shared across all 16 characters. This is the primary diversity lever.

**Literature grounding:** Well-supported by structured output generation literature (arXiv:2504.02052 prompt template analysis; StructEval 2025). The PANGeA system uses a structurally similar approach for NPC personality generation with Big Five Personality Model fields injected as structured prompts.

#### Pattern C: Role-Based Multi-Pass (with persona assignment)

In this pattern, the LLM is instructed to "play the role of" a specific archetype persona derived from the character's BC cell + element + cohort before generating the identity narrative. The persona assignment acts as a role-anchoring preamble that shapes all subsequent generation within that call.

The SCORE system (arXiv:2503.23512) demonstrates a related technique: dynamic state tracking + context-aware summarization ground identity generation in a persistent "character state" that informs the LLM's generation without requiring a second call. The BILLY approach (arXiv:2510.10157) uses persona vector merging to blend identity contributions from multiple sources.

**Strengths:** Persona assignment can produce vivid, distinctive outputs when the role framing is well-designed. The Big Five personality-biased NPC approach in PANGeA (2024) demonstrated this effectively. Role assignment creates a natural diversity mechanism — if each character receives a different archetype role based on their BC cell + element, the outputs diverge by construction.

**Weaknesses:** Role-based framing competes with the layered CORE/ENDGAME architecture. The LLM given a "Storm Caller" persona preamble may generate identity from that persona frame rather than from the weighted T1–T3 chain content. This inverts the architecture: the persona would be constituted by the role assignment rather than emerging from chain composition.

**For Reincarnated, this pattern creates a framing inversion risk** — the identity label precedes the identity derivation, which is architecturally backwards per doc 46 § 7.1. The CORE layer should generate the identity from chain content; the identity should not be pre-declared.

**AI-tell risk:** Lower than Patterns A/B for output vividness, but the framing inversion risk means the generated identity may not trace to the actual chain substrate.

**Literature grounding:** Primary for persona stability (PANGeA 2024). Secondary for persona vector merging (BILLY 2025). The framing inversion concern is legolas's analytical addition — not a direct literature citation but follows from doc 46 § 7.1 design intent.

#### Pattern D: RAG over Design Substrate

In this pattern, the LLM call is augmented by a retrieval step: before generating the character identity, a retriever queries the substrate (BC cells, chain skill descriptions, thematic vocabulary, existing set/legendary templates) to inject the most contextually relevant design facts into the prompt context. This is the ID-RAG approach (arXiv:2509.25299) applied to ARPG character generation.

The ID-RAG paper demonstrated that grounding generative agents in a structured identity knowledge graph (beliefs, traits, values) reduced simulation convergence time by 19–58% and improved identity recall over long interaction horizons. The SCORE framework adds hybrid retrieval (TF-IDF + semantic embeddings) to narrative systems with a 23.6% coherence improvement over baseline GPT models.

**Strengths:** Strong theoretical grounding for identity stability. The retrieval step ensures generated content is anchored to actual substrate facts rather than hallucinated or generic ARPG tropes. For multi-season use where sets/legendary themes accumulate over releases, RAG over a growing design library becomes increasingly valuable.

**Weaknesses:** The Phase 5 use case is bounded: at 16 characters per season, the substrate is small enough to fit in structured prompt fields directly (Pattern B) without retrieval infrastructure overhead. RAG adds engineering complexity (retrieval index, similarity search, retrieved-context formatting) that is disproportionate to Phase 5's ~2,100-call bounded scope. The ID-RAG benefits are most pronounced in long-horizon multi-turn interactions; a single-call-per-character generation at season time does not stress the coherence-drift failure mode that RAG addresses.

**AI-tell risk:** Lowest of the four patterns for hallucination/generic-trope risk. However, the diversity-collapse risk from the template structure (arXiv:2505.18949) applies equally here — retrieval diversity does not automatically produce output diversity.

**Literature grounding:** Strong primary sources (ID-RAG 2025; SCORE 2025). But the benefit pattern maps to a different use case than Phase 5.

---

### Q-SC3-2: Identity-at-L1-with-no-gear cohesion patterns

Three techniques were surveyed for ensuring identity holds at L1 with no gear:

**Technique: Conditional field absence (structural)**

The cleanest approach is structural: if no gear/T4 data is supplied to the ENDGAME_LAYER field, the LLM produces CORE-only output by structural definition. No explicit prompt instruction needed — the field is absent. This is a software-layer guarantee rather than a prompt-layer instruction. Implementation in star-lord's call architecture: when generating for a fresh character at L1, pass `ENDGAME_LAYER: null` or omit the field; the structured output schema marks `endgame_nod_narrative` as nullable with a conditional presence rule.

**Technique: Weighted-substrate prompting (explicit weighting)**

An alternative is to include weighting instructions in the prompt: "The CORE_LAYER is the FOUNDATION of this character's identity. The ENDGAME_LAYER is an optional addition that BUILDS ON but NEVER REPLACES the CORE." The literature on instructed weighting (PANGeA's personality-bias prompting; SCORE's hierarchical summarization) supports this as effective when anchoring is explicit and repeated at the instruction and example level. However, it is a softer constraint than conditional field absence.

**Technique: Progressive disclosure (per-character growth)**

PANGeA (2024) used a memory system that supplies contextual information incrementally as narrative unfolds. For Phase 5's batch-at-season-emit pattern, progressive disclosure does not apply directly — all character content emits at season generation time, not across session time. However, the progressive disclosure concept informs test fixture design: generating the same character identity at L1, L25, and L50 and verifying that the CORE identity is recognizable at all three levels is the empirical validation of this principle.

**Recommended approach for Phase 5:** Conditional field absence (structural guarantee) as primary; weighted-substrate prompting as secondary reinforcement in the system prompt for characters where both layers are present.

---

### Q-SC3-3: T4-choice-independence patterns

For the same CORE identity to cohere across multiple T4 strategy variants (e.g., fire-pyromancer with RESOURCE_CONVERSION vs TRADE_OFF), three patterns apply:

**Technique: Variant generation with shared CORE anchor**

The CORE_LAYER field contains only T1–T3 chain content (identical for both T4 variants of the same character). The T4 strategy information goes into the ENDGAME_LAYER field as a narrow additive. If the CORE identity is stable across both LLM calls (one per T4 variant), T4-choice-independence follows structurally. The diversity-collapse literature (arXiv:2505.18949) notes that structural tokens constrain output space — for T4-independence this is a feature, not a bug: the shared CORE_LAYER structure produces similar CORE outputs, while the differing ENDGAME_LAYER produces variant endgame nods.

**Technique: CORE generation before T4 lock (architecture sequencing)**

If the CORE identity is generated independently of T4 content (via conditional field absence as described above), T4-choice-independence is guaranteed by the call architecture itself. The CORE identity does not know which T4 the player eventually selects. This is the strongest architectural guarantee.

**Technique: Conditional-flavor-overlay (post-generation)**

A lighter-weight alternative: generate CORE identity once, store it, and generate T4-specific flavor nods as short additive snippets separately. The endgame nod for RESOURCE_CONVERSION and the endgame nod for TRADE_OFF are generated as separate overlay calls, each receiving the frozen CORE identity as context. This is the hierarchical decomposition approach (Pattern A) applied specifically to the T4-variant problem. The cost at Phase 5 scale: if a character has 2 viable T4 strategies, this doubles the endgame-nod calls for that character (2 calls vs. 1). At 16 characters × ~2 T4 strategies each = ~32 endgame nod calls + 16 CORE calls = 48 LLM calls total for identity generation per season — well within the tractable budget.

**Recommended approach:** CORE-before-T4 architectural sequencing via conditional field absence as primary; T4-specific endgame nods as optional separate additive calls if T4 strategy data is available at season-emit time.

---

### Q-SC3-4: Endgame-nod-additivity patterns (preventing endgame theme dominance)

**Pattern: Explicit field scope constraint with output length cap**

The endgame_nod_narrative output field should have an explicit length constraint in the prompt: "1 sentence maximum, adding to the character's core identity." This prevents the endgame nod from expanding into a paragraph that displaces the CORE narrative's primacy in the player's reading experience. Word-count constraints are a well-documented control in structured LLM output (see StructEval benchmarks and structured generation literature).

**Pattern: Anti-pattern guard in system prompt**

Doc 46 § 7.4 specifies: "the LLM does NOT generate identity from gear stack. If the prompt structure suggests 'describe this character based on their gear,' the prompt is malformed." The equivalent prompt-level enforcement: the system prompt includes an explicit negative example ("Do NOT describe the character as 'the wielder of [legendary item name]' — the legendary item is mentioned as a nod, not as identity-defining"). Negative examples in system prompts are supported by few-shot prompting literature as effective anti-pattern guards.

**Pattern: Anchor-prompt-with-flavor-overlay (PANGeA lineage)**

PANGeA's NPC personality bias patterns demonstrate that when a personality anchor is set in the system prompt, subsequent content generation tends to reinforce rather than replace it. The same principle applied here: establish the CORE identity as a system-level anchor ("This character's identity is: [CORE output]") before presenting the ENDGAME_LAYER for the endgame nod. The endgame nod generation then operates against a fixed identity anchor rather than against raw gear/T4 data.

---

### Q-SC3-5: AI-tell failure modes at Phase 5 scale

The literature identifies four classes of AI-tell failure relevant to Phase 5:

**Failure mode 1: Templated-structure output collapse (most severe for Phase 5)**

The diversity-collapse paper (arXiv:2505.18949) is the highest-relevance primary source here. Its key finding: structural tokens in templates — role markers, section headers, special formatting tokens — constrain the model's output space, producing semantically similar outputs even when temperature is high. This effect "persists even under high-temperature sampling." For Phase 5 at 16 characters × multiple calls = ~2,100 total calls, the collapse manifests as: multiple characters receiving the same archetypal framing despite having different chain substrates. For example, if the CORE_LAYER field consistently leads with "element: fire; chain_1_t1_active_1: [description]", the LLM learns to pattern-match "fire + physical chain = Blaze Knight archetype" and produces variants of that archetype regardless of the actual chain composition variation.

**Mitigation:** Per-character substrate diversity injection. The SUBSTRATE_CONTEXT field must include character-specific distinguishing content (BC cell, resource model type, cohort label, chain composition pattern) that varies meaningfully across characters. The THEMATIC_REGISTRY field should be curated per element × archetype cluster rather than a single shared list. Characters with similar elements but different cohort profiles should receive different THEMATIC_REGISTRY slices.

**Failure mode 2: Echoed plot elements across characters ("Sui Generis" failure)**

The "Echoes in AI" PNAS study (arXiv:2501.00273) found that LLMs generating 100 story continuations from the same prompt produced 50/100 with identical plot elements; cross-model testing showed the echo pattern persists across different LLMs. For Phase 5: if the same character_name style ("Storm-Bound [Noun]") or core_identity_narrative structure ("A [adjective] [element] warrior who [verb phrase] through [noun phrase]") repeats across 16 characters, the output is recognizable as machine-generated. The Sui Generis score introduced by this paper is a novel metric — measuring uniqueness of output elements across alternative generations from the same prompt.

**Mitigation:** The Echoes paper's recommended mitigation (sampling multiple story fragments and selecting highest-Sui-Generis outputs) translates directly to Phase 5: generate N candidates per character identity, compute cross-character overlap at the semantic embedding level, select the top-diversity set. At 3 candidates per character, the call count increases from ~2,100 to ~6,300 (still $1.50–$15 per season — tractable per framing brief § 9.2 budget envelope). The diversity-selection pass can be implemented as a cheap semantic-similarity check (embedding cosine distance between character_name and core_identity_narrative outputs across the 16-character set) before choosing the highest-diversity candidates.

**Failure mode 3: Generic ARPG tropes (fantasy-archetype cliché)**

Without substrate grounding, LLMs default to the training-data distribution for "ARPG character description," which skews toward generic dark-fantasy vocabulary: "wielder of shadow," "master of the arcane," "bound by ancient power." These are recognizable as generic LLM outputs because they match the ARPG training corpus exactly.

**Mitigation:** The THEMATIC_REGISTRY field (per doc 46 § 7.4) injects isekai-specific thematic vocabulary that steers away from generic dark-fantasy toward the game's specific genre register. The vocabulary must be curated by gandalf (per their seam authority on thematic content) and must include both positive examples (appropriate isekai vocabulary) and negative examples (vocabulary to avoid). The "and behold" phrasing class mentioned in the dispatch scope is an example of negative-vocabulary-to-exclude — including explicit negative examples in the THEMATIC_REGISTRY reduces their occurrence.

**Failure mode 4: Position and length bias in LLM judging**

When using the LLM cohesion judge to validate its own outputs (self-evaluation), position bias and verbosity bias are documented failure modes (LLM-as-a-Judge survey, arXiv:2411.15594). The judge tends to favor longer outputs and to be influenced by presentation order. For Phase 5's self-evaluation of generated identities, this means the judge may score more verbose character descriptions higher regardless of actual cohesion quality.

**Mitigation:** Use rubric-based evaluation criteria (see Q-SC3-6) rather than free-form quality scoring. Rubric items reduce the dimensionality of the judging task and reduce susceptibility to verbosity bias.

---

### Q-SC3-6: AI-tell mitigation patterns from literature

**Mitigation 1: Per-character substrate context injection (primary)**

The diversity-collapse paper's finding that minimal formatting yields more diverse outputs suggests a dual strategy: use structured field labeling for the LLM to receive inputs reliably (Pattern B), but inject maximum per-character lexical variety within those fields. If CORE_LAYER content is generated from the same schema but contains character-specific skill descriptions, ability names, and chain-specific flavor, the output diversity follows the input diversity. The structural tokens are constant; the semantic content varies.

**Mitigation 2: Multi-candidate generation with diversity selection**

Sampling 3 candidates per character and selecting the highest-diversity set (per Echoes AI finding) is the most literature-grounded mitigation for cross-character echo. The "effective semantic diversity" framework (arXiv:2504.12522) proposes measuring diversity only among outputs meeting quality thresholds — directly applicable to Phase 5: among 3 candidate character identities that pass the rubric quality check, select the one that maximizes cross-character distinctiveness.

**Mitigation 3: Negative vocabulary injection in THEMATIC_REGISTRY**

Explicitly listing phrasing classes to avoid in the system prompt / THEMATIC_REGISTRY. Known AI-tell phrasing classes from game context (synthesized from literature + domain knowledge):
- "and behold" framing class (narrative revelation phrasing)
- "ancient power" / "arcane mastery" / "shadow's embrace" (generic dark-fantasy tropes)
- "your destiny" / "chosen one" framing (LLM-generated epic trope)
- Passive construction: "is known as" / "is said to be" (distant narrator voice, not character identity voice)
- Sentence openers: "This [class] embodies" / "This warrior represents" (meta-description rather than identity)
- Numericist flavor: "their [X]% crit rate" / "maximizing [stat]" (mechanical optimization language imported from LLM's ARPG training corpus)

Negative examples in system prompts are supported by few-shot prompting literature as effective constrainers.

**Mitigation 4: Temperature and sampling calibration**

The Min-P sampling paper (arXiv:2407.01082, ICLR 2025 oral) demonstrated that min-p values between 0.05 and 0.1 outperform Top-P especially at higher temperatures, producing outputs that balance creativity and coherence better than nucleus sampling alone. For Phase 5's character identity generation: moderate temperature (0.7–0.9) + min-p sampling (0.05–0.1) is better than high temperature + Top-P for producing diverse but coherent character descriptions. This is a model-inference-layer parameter recommendation for star-lord's LLM call architecture.

**Mitigation 5: Cross-character semantic similarity check at season-emit time**

A post-generation detection pass: after all 16 character identities are generated, compute pairwise semantic similarity of character_name and core_identity_narrative across the 16 outputs using embedding cosine distance. Characters whose identities are semantically similar (above a threshold, e.g., cosine similarity > 0.85) are flagged for regeneration. This is the direct application of the Echoes AI Sui Generis score approach adapted for batch character generation. Implementation cost: one embedding call per character (cheap, <$0.001 per call) + pairwise matrix computation.

---

### Q-SC3-7: Phase 5 scale interaction with AI-tell risk (~2,100 calls per season)

The framing brief § 9.2 estimates ~16 characters × ~12 chain skills × ~11 gear slots ≈ 2,100 LLM calls per season. This is a notable scale consideration for AI-tell risk.

**Key scale insight from literature:** The diversity-collapse paper (arXiv:2505.18949) found that output-space collapse is primarily a function of the structural tokens shared across calls, not the total call count. At 2,100 calls with the same prompt template, the collapse risk is proportional to how much of the prompt is shared versus character-specific. If the CORE_LAYER and SUBSTRATE_CONTEXT fields are genuinely varied per character, the 2,100-call scale does not increase the per-character AI-tell risk above what a 16-call generation would produce. The risk scales with prompt-template homogeneity, not call count.

**However:** the 2,100-call figure suggests that calls are not purely per-character identity (16 calls) but also per-skill (flavor naming) and per-gear-slot (gear descriptor). Skill naming and gear naming at this scale are where the Echoes AI "echoed plot elements" failure mode is most likely to manifest — the same archetypal skill-naming pattern ("[Element] [Noun]", "Storm Strike", "Frost Bolt") recurs across characters because the per-skill call context is similar across characters with shared element types.

**Detection at season-emit time:**

1. **Cross-character skill-name collision detection:** compute string edit distance or semantic embedding distance between all skill names across the season's 16 characters. Flag collisions (identical or near-identical names) for regeneration.
2. **Gear descriptor diversity audit:** sample 10% of gear descriptors per rarity tier; compute BLEU self-similarity against the full set; flag if self-BLEU exceeds a threshold (e.g., BLEU > 0.4 across 100 samples indicates formula reuse).
3. **Per-element archetype clustering:** group character identities by element; within each element group, verify that character names and CORE narratives are semantically distinct (cosine similarity check).

**Scale-appropriate model guidance:**

Per the "effective semantic diversity" paper (arXiv:2504.12522), smaller preference-tuned models (not the largest available) often produce higher effective semantic diversity within a fixed sampling budget. For Phase 5's cost envelope ($0.50–$5 per season), using a smaller but well-calibrated model for skill naming and gear descriptors (lower cost, higher variety) while using a larger model for character_name + core_identity_narrative (higher quality, lower count) is a cost-effective architecture.

---

## Methodology Recommendations Table (§ 7.2)

| Pattern | Layered-cohesion fit (1-5) | Identity-at-L1 fit (1-5) | T4-independence fit (1-5) | Endgame-additivity fit (1-5) | Implementation complexity | AI-tell risk | Recommended for Phase 5? |
|---|---|---|---|---|---|---|---|
| **A: Hierarchical Prompt Decomposition (multi-pass)** | 5 | 5 | 5 | 5 | Medium (2 calls per character; error surface doubles) | Moderate | Yes — as optional extension for T4-variant endgame nods |
| **B: Structured Output with Layer Tags (single-call)** | 4 | 5 | 4 | 4 | Low (single call; aligns with doc 46 § 7.4 as-designed) | Moderate-low (with diversity injection) | **Yes — PRIMARY recommendation** |
| **C: Role-Based Multi-Pass (persona assignment)** | 2 | 2 | 2 | 2 | Medium | Low for vividness | No — framing inversion risk |
| **D: RAG over Design Substrate** | 5 | 4 | 4 | 5 | High (retrieval infrastructure; disproportionate for Phase 5 scope) | Low for hallucination | No for Phase 5 v1; Yes for v1.1+ at multi-season scale |

**Scoring rationale:**

- Pattern C scores low on layered-cohesion and identity-at-L1 because persona assignment constitutes identity before chain composition is expressed — this inverts doc 46 § 7.1's architecture. Pattern C is strong for vividness but structurally incompatible with the CORE-from-chain-composition discipline.
- Pattern D scores high on fit but is a deliberate "not yet" — the benefits are real but the use case (long-horizon identity drift prevention) does not apply to Phase 5's bounded single-call-per-character scope. Recommend revisiting Pattern D for multi-season narrative accumulation where a character's identity across seasons becomes a RAG target.
- Pattern A's endgame-additivity fit is 5 because the two-call structure physically prevents endgame content from contaminating CORE generation. For characters with confirmed T4 paths and Legendary/Set themes, Pattern A is superior to Pattern B's single-call approach.
- Pattern B's endgame-additivity fit is 4 (not 5) because the ENDGAME_LAYER content is visible in the same context window as CORE_LAYER; the anti-pattern guard (negative example + field scope constraint) provides a softer constraint than Pattern A's physical separation.

---

## Top 3 Architecture Recommendations with Integration Sketches

### Recommendation 1 (PRIMARY): Pattern B — Structured Output with Layer Tags

**Architecture:**

Single LLM call per character. Input is a structured prompt with labeled fields:

```
SYSTEM: You are a thematic identity synthesizer for an isekai ARPG spirit-chain system. 
Your task is to generate a thematic identity from a character's chain composition. 
The CORE_LAYER is the FOUNDATION — you derive identity primarily from this.
The ENDGAME_LAYER (if present) is an ADDITIVE NOD only — it adds richness but does not define.
[NEGATIVE EXAMPLES: avoid "and behold", "ancient power", "arcane mastery", "wielder of shadow", 
"chosen one", "this character embodies", "is known as", generic-dark-fantasy phrasing]
[THEMATIC_REGISTRY: isekai-appropriate vocabulary per gandalf's curation, element-specific]

USER:
CORE_LAYER (T1–T3 chain composition, weighted HIGHEST):
  chain_1: [mechanic-altering passives and actives at T1, T2, T3]
  chain_2: [if applicable]
  resource_model: [HP-cost / mana / stamina / rage / etc.]
  
ENDGAME_LAYER (optional additive nod, weight LOW):
  t4_strategy: [if unlocked: Category A × B/C × element]
  legendary_capabilities: [at most 1–2 notable capabilities if Tier 1+2]
  set_bonus: [if 4-piece set active]

SUBSTRATE_CONTEXT:
  bc_cell: [BC dimensional identity — key differentiators]
  element: [primary element]
  cohort: [archetype cohort label]
  
THEMATIC_REGISTRY: [element-specific subset, 20–30 terms]
```

Output schema (structured JSON, constrained grammar):

```json
{
  "character_name": "<2–4 word archetypal name>",
  "core_identity_narrative": "<1–2 sentences; MUST derive from CORE_LAYER only>",
  "endgame_nod_narrative": "<1 sentence or null; MUST be additive; omit if ENDGAME_LAYER absent>",
  "skill_flavor_keys": ["<per-skill thematic tag>"],
  "spirit_guide_hooks": ["<projection anchor phrase>"]
}
```

**LLM model class:** moderate-size instruction-tuned model with strong structured-output compliance (e.g., Claude 3.5 Sonnet / GPT-4o mini for skill flavor + gear descriptors at volume; Claude 3.7 Sonnet or equivalent for character_name + core_identity_narrative). Model tiering by field importance reduces cost without sacrificing quality on the load-bearing identity fields.

**AI-tell mitigation:** per-character substrate diversity injection in CORE_LAYER + SUBSTRATE_CONTEXT + per-element THEMATIC_REGISTRY slice; min-p sampling (0.05–0.1) + temperature 0.7–0.9; post-generation cross-character semantic similarity check (embedding cosine distance, flag cosine > 0.85 for regeneration).

**Validation method:** Three test fixtures per doc 46 § 7.3 disciplines:
- Identity-without-gear test: pass same character with ENDGAME_LAYER omitted; verify output is coherent without it
- T4-choice-independence test: pass same character with two different T4 strategies in ENDGAME_LAYER; verify CORE output is recognizably the same identity
- Endgame-nod-additivity test: compare output with and without Legendary content in ENDGAME_LAYER; verify CORE narrative is unchanged

**Composition with star-lord architecture:** star-lord owns the LLM call infrastructure; the structured input/output schema above is the contract. Prompt template authored by gandalf per their seam (design-spec authoring at Wave 3); star-lord implements the call wrapper + structured output parsing + post-generation diversity check.

---

### Recommendation 2 (SUPPLEMENTARY for T4-variant endgame nods): Pattern A — Two-Call Hierarchical Decomposition

**Use case:** characters where T4 strategy matters significantly to narrative flavor. Pattern B's single-call approach is sufficient for most characters; Pattern A is the upgrade path where a character has strongly variant endgame identities across T4 strategies.

**Architecture:**

Call 1 (CORE generation): inputs are CORE_LAYER + SUBSTRATE_CONTEXT + THEMATIC_REGISTRY only. Output: character_name + core_identity_narrative. This call fires once per character regardless of T4 state.

Call 2 (ENDGAME nod generation): inputs are ENDGAME_LAYER + SUBSTRATE_CONTEXT + frozen Call 1 output ("The character's core identity is: [Call 1 core_identity_narrative]"). Output: endgame_nod_narrative (1 sentence, constrained). This call fires once per T4 strategy variant if T4 data is present.

**Call count at season scale:** 16 characters × 1 CORE call + 16 characters × ~1–2 T4 variant calls = 32–48 total identity calls, vs Pattern B's 16. The increase is modest; the cost is negligible within the $0.50–$5 budget.

**Validation method:** Same three test fixtures as Pattern B. Additionally: verify that Call 2 outputs for different T4 strategies of the same character both read as "additions to" rather than "replacements of" the CORE narrative (human spot-check during calibration).

---

### Recommendation 3 (DETECTION at season-emit time): Cross-Character Diversity Audit

This is not a call architecture but a post-generation quality gate that should compose with either Pattern A or B.

**Implementation:**

After all character identities are generated for a season:

1. **Name collision check:** compute pairwise string edit distance across all 16 character names. Flag pairs with Levenshtein distance < 3 (structurally near-identical names).
2. **Narrative embedding distance matrix:** compute sentence embeddings for all core_identity_narratives; compute pairwise cosine similarity 16×16 matrix. Flag pairs with cosine similarity > 0.85 (semantically near-identical narratives despite different characters).
3. **Per-element archetype clustering:** within each element group (fire / water / earth / wind + 3 additional elements), verify that character names and CORE narratives are mutually distinct at the embedding level (within-element pairwise cosine similarity < 0.75).
4. **Skill name echo check:** collect all skill names emitted across the season; compute self-BLEU across all 16 × ~12 = 192 skill names; flag if self-BLEU > 0.35 across the set (indicating formula reuse: "X Strike", "Y Blast" pattern dominating).

**Threshold values are proposed starting points** — the Wave 3 design call should empirically validate against a pilot generation run.

---

## AI-Tell Mitigation Summary

| AI-tell failure mode | Root cause (per literature) | Mitigation (concrete) | Detection at season-emit |
|---|---|---|---|
| Templated output collapse | Structural tokens in prompt constrain output space; persists through temperature adjustment (arXiv:2505.18949) | Per-character CORE_LAYER + SUBSTRATE_CONTEXT lexical variety; per-element THEMATIC_REGISTRY slices; avoid shared generic strings across calls | Cross-character embedding similarity check (cosine > 0.85 flag) |
| Echoed character archetypes | LLMs default to training-corpus ARPG archetypes ("Blaze Knight", "Frost Mage") when input variation is low (PNAS 2025, arXiv:2501.00273) | Substrate-grounded CORE_LAYER injection forces derivation from chain mechanics rather than archetype labels; negative-example vocabulary in THEMATIC_REGISTRY | Cross-character semantic distinctiveness audit |
| Generic dark-fantasy phrasing | LLM training corpus for game flavor text skews dark-fantasy; system prompt has insufficient genre specificity | Explicit negative vocabulary list in system prompt; isekai-register positive vocabulary in THEMATIC_REGISTRY (gandalf's seam to author) | Automated phrasing-pattern scan: flag occurrence of known AI-tell phrases |
| Gear-constitutes-identity inversion | Without explicit weighting, LLM may pattern-match "character with legendary_item X = identity of X" | Anti-pattern guard in system prompt; ENDGAME_LAYER field labeled LOW WEIGHT; endgame_nod_narrative output length cap (1 sentence) | Human spot-check: verify removing endgame nod does not "break" the identity |
| Skill-name formula echo ("Storm Strike", "Frost Bolt", "Shadow Slash") | High-volume per-skill calls with similar element×geometry inputs produce near-identical name patterns | Multi-candidate generation (3 candidates per skill, select most distinctive); per-skill SUBSTRATE_CONTEXT varies by chain + tier + BC axis | Self-BLEU across season's skill names (threshold: > 0.35 flagged) |
| LLM judge self-validation bias | Position bias + verbosity bias in LLM judging; judge scores longer outputs higher (arXiv:2411.15594) | Rubric-based evaluation criteria (not free-form scoring); three explicit binary test fixtures (identity-without-gear / T4-choice-independence / endgame-nod-additivity) | Rubric items are binary pass/fail; no length bias surface |

---

## Knowledge Gaps Not Resolved

1. **No direct primary-source literature on ARPG cohesion-judge LLM systems.** The closest available sources are game NPC generation (PANGeA), multi-agent story systems (RPGAgent, COLLABSTORY), and general narrative coherence (SCORE). None of these systems have the specific "chain-composition-to-identity with endgame-additive" architecture. The recommendations above are derived from first-principles application of general LLM architecture patterns to the specific Phase 5 use case. This is not a literature gap that additional research will close — the specific use case is novel enough that primary sources do not exist yet. The Wave 3 design call is the appropriate venue for translating this literature grounding into Phase 5-specific prompt engineering.

2. **Calibration sample size for Phase 5's three test fixtures.** The LLM-as-judge literature recommends multi-sample evaluation and emphasizes that single-shot judging is insufficient (arXiv:2412.12509; Judge Reliability Harness 2025). Specific sample size recommendations for content cohesion validation (as opposed to text quality evaluation) are not in the surveyed literature. Gamora's seam owns the methodology consultation for calibration specifics (per dispatch scope — gamora handles calibration / probability calls; this is outside legolas Mode A scope). The framing brief §9.2 notes "calibration spec" as a Wave 3 deliverable — the sample-size determination is a gamora+star-lord+gandalf design call item.

3. **The specific THEMATIC_REGISTRY vocabulary is gandalf's seam.** This research identifies that per-element THEMATIC_REGISTRY slices are load-bearing for AI-tell mitigation, and that both positive examples (isekai vocabulary) and negative examples (generic dark-fantasy vocabulary to avoid) are required. The specific vocabulary curation is outside legolas's research scope — gandalf owns that at Wave 3 design-spec authoring.

4. **Multi-season RAG recommendation (Pattern D) is deferred.** The ID-RAG / SCORE approaches become more relevant when character identity needs to persist and evolve across seasons. This research recommends revisiting Pattern D after Phase 5 v1 ships and multi-season narrative accumulation is in scope.

---

## Source List

| Source | Type | Access date | Key application |
|---|---|---|---|
| [PANGeA: Procedural Artificial Narrative using Generative AI for Turn-Based Video Games](https://arxiv.org/abs/2404.19721) | Primary (academic, peer-reviewed) | 2026-05-27 | Structured personality-biased NPC generation; Big Five Personality Model injection; narrative-scope validation layer |
| [ID-RAG: Identity Retrieval-Augmented Generation for Long-Horizon Persona Coherence in Generative Agents](https://arxiv.org/abs/2509.25299) | Primary (academic) | 2026-05-27 | Identity knowledge graph; persona grounding; failure modes (identity drift, belief inconsistency, hallucination propagation); 19–58% convergence improvement |
| [Echoes in AI: Quantifying lack of plot diversity in LLM outputs (PNAS 2025)](https://arxiv.org/abs/2501.00273) | Primary (PNAS, peer-reviewed) | 2026-05-27 | Sui Generis score; echoed narrative elements at scale; 50/100 identical plot elements in GPT-4 generations; multi-candidate diversity selection as mitigation |
| [The Price of Format: Diversity Collapse in LLMs (arXiv:2505.18949)](https://arxiv.org/abs/2505.18949) | Primary (academic) | 2026-05-27 | Structural tokens cause output-space collapse; persists through high temperature; minimal formatting yields more diverse outputs; diversity-aware prompt design |
| [LLM Output Homogenization is Task Dependent (arXiv:2509.21267)](https://arxiv.org/abs/2509.21267) | Primary (academic) | 2026-05-27 | Task-dependent nature of homogenization; reference for scale of output homogenization at batch generation |
| [A Survey on LLM-as-a-Judge (arXiv:2411.15594)](https://arxiv.org/abs/2411.15594) | Primary (academic survey) | 2026-05-27 | Recommended judging architectures; pairwise comparison vs. scoring; bias failure modes (position, verbosity, self-enhancement); mitigation (few-shot, shuffling, standardized output) |
| [Can You Trust LLM Judgments? Reliability of LLM-as-a-Judge (arXiv:2412.12509)](https://arxiv.org/abs/2412.12509) | Primary (academic) | 2026-05-27 | McDonald's omega framework for reliability; limitations of single-shot evaluation; temperature effects on reliability; multi-sample recommendation |
| [Judge Reliability Harness: Stress Testing the Reliability of LLM Judges (arXiv:2603.05399)](https://arxiv.org/abs/2603.05399) | Primary (academic, 2025) | 2026-05-27 | Formatting brittleness; task-dependent reliability failure; asymmetric false-negative/false-positive rates; no judge universally reliable across benchmarks |
| [SCORE: Story Coherence and Retrieval Enhancement for AI Narratives (arXiv:2503.23512)](https://arxiv.org/abs/2503.23512) | Primary (academic, 2025) | 2026-05-27 | Dynamic state tracking + context-aware summarization + hybrid retrieval; 23.6% coherence improvement; 89.7% emotional consistency; modular multi-LLM backend |
| [Autorubric: Unifying Rubric-based LLM Evaluation (arXiv:2603.00077)](https://arxiv.org/abs/2603.00077) | Primary (academic, 2025) | 2026-05-27 | Rubric-based evaluation methodology; recursive decomposition of evaluation criteria; fine-grained dimension scoring |
| [RULERS: Locked Rubrics and Evidence-Anchored Scoring for Robust LLM Evaluation (arXiv:2601.08654)](https://arxiv.org/abs/2601.08654) | Primary (academic, 2025) | 2026-05-27 | Locked rubrics as anti-drift mechanism; evidence-anchored scoring approach |
| [Min-P Sampling for Creative and Coherent LLM Outputs (arXiv:2407.01082)](https://arxiv.org/abs/2407.01082) | Primary (academic, ICLR 2025 oral) | 2026-05-27 | Min-p 0.05–0.1 outperforms Top-P at higher temperatures; balances creativity and coherence better than nucleus sampling |
| [Evaluating Diversity and Quality of LLM Generated Content (arXiv:2504.12522, COLM 2025)](https://arxiv.org/abs/2504.12522) | Primary (academic, 2025) | 2026-05-27 | Effective semantic diversity metric; RL-tuned models produce higher effective diversity than SFT; smaller models outperform larger for unique content within fixed sampling budget |
| [Addressing LLM Diversity by Infusing Random Concepts (arXiv:2601.18053)](https://arxiv.org/abs/2601.18053) | Primary (academic, 2025) | 2026-05-27 | Random concept injection as diversity mechanism; effective for open-ended generation |
| [Dynamic Context Adaptation for Consistent Role-Playing Agents with RAG (arXiv:2508.02016)](https://arxiv.org/abs/2508.02016) | Primary (academic, 2025) | 2026-05-27 | RAG for consistent role-playing agents; context adaptation patterns |
| [From Prompts to Templates: Systematic Prompt Template Analysis (arXiv:2504.02052)](https://arxiv.org/abs/2504.02052) | Primary (academic, 2025) | 2026-05-27 | Template structure analysis; structural token effects on output |
| Reincarnated canonical doc 46 (concentration architecture) | Internal canonical (load-bearing) | 2026-05-27 | Layer 6 layered cohesion architecture; doc 46 §§ 7.1–7.5 |
| Reincarnated canonical doc 40 D7 (AI-tell discipline) | Internal canonical (load-bearing) | 2026-05-27 | AI-tell line definition; templated structure with narrow blanks |
| Reincarnated framing brief 2026-05-27 (gandalf) | Internal canonical | 2026-05-27 | SC-3 scope; ~2,100 calls per season; $0.50–$5 cost envelope; Wave 3 gate |
| Reincarnated math-hotspot naming 2026-05-23 (gandalf) § 2.3 | Internal canonical | 2026-05-27 | P5 cohesion-judge as named math hotspot; owning seams (star-lord/gandalf/gamora) |

---

## Open Questions for Wave 3 Design Call

Three open questions require gandalf + star-lord + gamora + Matt design-call resolution before Wave 3 implementation fires. These are decision points legolas flags but does not lock — per Discipline #18, the methodology-lock is the design call's job.

**OQ-1: Single-call vs two-call architecture (Patterns B vs A)**

Pattern B (single-call, structured fields) is simpler and within doc 46 § 7.4's as-designed framing. Pattern A (two-call hierarchical) provides stronger physical separation of CORE from ENDGAME but doubles the identity-generation call count. The design call should decide: does Pattern A's physical CORE/ENDGAME separation justify the added complexity for Phase 5 v1, or does Pattern B with explicit field weighting + anti-pattern guard suffice?

A hybrid is possible: use Pattern B for most characters, and Pattern A specifically for characters where the T4 strategy significantly diverges from CORE identity (e.g., a physical chain character with ELEMENT_CONVERSION to ice as T4 — the endgame divergence is large enough that physical separation reduces contamination risk). The criteria for "significant T4 divergence warranting Pattern A" would need to be defined in the design-spec.

**OQ-2: Rubric criteria for the three core discipline tests**

The three test fixtures (identity-without-gear, T4-choice-independence, endgame-nod-additivity) need explicit rubric items to be operationalized as test fixtures. The literature supports rubric-based evaluation (Autorubric; RULERS) as more reliable than free-form judging. Proposed starter criteria for gandalf's review:

- **Identity-without-gear test rubric:** (a) Does the character have a recognizable archetype class/role without reading the gear description? (b) Does the character name derive from chain mechanic vocabulary rather than gear vocabulary? (c) Would a player at L1 recognize this as their character's identity?
- **T4-choice-independence test rubric:** (a) Does swapping the T4 strategy in ENDGAME_LAYER change the character_name? (b) Does it change core_identity_narrative? (c) Does the endgame_nod_narrative read as a variant of the same identity vs a different identity?
- **Endgame-nod-additivity test rubric:** (a) Does the endgame nod reference the legendary/set content by name or mechanic? (b) Does removing the endgame nod sentence leave a coherent identity? (c) Does the endgame nod read as "enriching" rather than "overriding"?

These rubric items are proposed for gandalf's review and should be locked as part of the Wave 3 design-spec authoring.

**OQ-3: Calibration validation sample size for the three test fixtures**

How many characters × how many generation runs are needed for the three test fixtures to produce a reliable calibration signal? The LLM-as-judge literature (arXiv:2412.12509) recommends multi-sample evaluation with explicit uncertainty quantification, but sample size for content cohesion (vs text quality) is not established in the surveyed literature. This is gamora's methodology consultation item (calibration sample size and statistical validation approach). Gamora should fire a methodology consultation (per Discipline #18.2 timing — after baseline empirical signal from Pattern B initial runs is available) before the validation protocol locks.

---

**Completion status:** SC-3 research complete. Artifact filed at `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md`. Wave 3 gate findings: Pattern B (structured output with layer tags) is the primary recommendation; Pattern A is the supplementary upgrade for T4-variant endgame nods; post-generation cross-character diversity audit is the primary AI-tell detection mechanism. Three open questions for Wave 3 design call (OQ-1, OQ-2, OQ-3) require gandalf + star-lord + gamora + Matt resolution before Wave 3 implementation fires.
