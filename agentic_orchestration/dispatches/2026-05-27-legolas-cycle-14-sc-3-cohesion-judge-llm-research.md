# Dispatch — 2026-05-27 — legolas — Cycle 14 SC-3 Mode A cohesion-judge LLM call architecture research

**From:** knight-rider
**To:** legolas (research + catalogue-crawl seam)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified — sidecar list confirmed including SC-3)
**Estimated effort:** ~6-10 hours Mode A analytical research
**Acceptance:** research artifact filed at `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md` with explicit methodology recommendations for Wave 3 cohesion-judge LLM call structure under AI-tell discipline D7

## Context

Cycle 14 Wave 3 implements Phase 5 cohesion-judge LLM architecture per doc 46 Layer 6 (layered cohesion: CORE identity from chain composition weighted toward lower tiers + ENDGAME nod additive). This is a math hotspot per gandalf math-hotspot list (mathematical seam naming, P5 cohesion-judge calibration is canonical hotspot category) and requires methodology consultation per Discipline #18 (methodology-before-execution) BEFORE Wave 3 fires.

This sidecar gates Wave 3 (per framing brief § 5 SC-3 entry: "Wave 3 gate"). Legolas Mode A research informs gandalf's design-spec authoring for the LLM prompt structure + star-lord's LLM integration architecture + rocket's call architecture, all of which compose into Wave 3 implementation.

The narrow research question: across the ARPG genre + LLM-narrative-generation literature, what call-architecture patterns produce **layered narrative cohesion** (CORE thematic identity that holds at L1 with no gear + ENDGAME flavor that nods to T4 paths + legendary/set themes) without producing AI-tell pattern (per discipline D7 — formulaic-sounding-content / pattern-detection-from-repeated-prompt-shape / homogeneous-flavor-text-across-characters)?

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/46-concentration-architecture-2026-05-27.md` § 7 (layered cohesion disciplines: identity-without-gear / T4-choice-independence / endgame-nod-additivity) + § 7.3 (three core disciplines for testing)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — particularly D7 AI-tell discipline + D28-D32 spirit-guide data-oracle
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid; identity-at-L1 cohesion criterion derives from this
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern that the cohesion-judge LLM consumes
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 3 + § 5 SC-3
- `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2 (P5 cohesion-judge calibration is the canonical math hotspot category)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — particularly Discipline #18 methodology-before-execution
- `.claude/skills/reincarnated-legolas-operating-procedure` — Mode A protocol

## Math-before-code

This is the math-note-equivalent research that GATES Wave 3 implementation. Per Discipline #18, methodology selection happens BEFORE execution. Output should make explicit methodology recommendations (per § 7.2 below).

## Cross-seam contract change?

**NO** — this is research output, not code emission. Round-trip not applicable.

## Scope

- [ ] Survey ARPG-narrative literature + LLM-narrative-generation patterns for layered-cohesion call architectures
- [ ] Research questions to answer (per § 7.1 below)
- [ ] Methodology recommendations table (per § 7.2 below)
- [ ] AI-tell mitigation patterns (per § 7.3 below)
- [ ] File research artifact at `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md`
- [ ] Append completion record to this dispatch file per dispatches/README.md
- [ ] Round-trip: not applicable — research output, no cross-seam contract change

## Acceptance criteria

- [ ] Research artifact filed at `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md` with sections per § 7.1 + § 7.2 + § 7.3 below
- [ ] Each methodology recommendation grounded in literature citation + applicability rationale to Reincarnated Phase 5 architecture (doc 46 Layer 6)
- [ ] AI-tell mitigation patterns surveyed (formulaic-sounding-content / pattern-detection / homogeneous-flavor) with concrete countermeasures
- [ ] Completion record appended; commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Out of scope (explicit non-goals)

- Do NOT implement any code or prompts — this is research, not implementation; implementation is Wave 3 work owned by star-lord + rocket + gandalf
- Do NOT author LLM prompt templates — that's gandalf's seam at Wave 3 design-spec authoring (informed by this research)
- Do NOT make calibration / probability calls — that's gamora's methodology consultation seam at Wave 3 integration
- Do NOT enter Mode B catalogue crawl — this is Mode A analytical research only
- Do NOT touch substrate library / DB / external systems — read-only research

## Research questions (legolas resolves)

### 7.1 Architecture patterns

- **Q-SC3-1**: Across LLM-narrative-generation literature, what call-architecture patterns produce **layered narrative identity** where a CORE layer (low-tier-weighted thematic anchor) and an ENDGAME layer (high-tier flavor nod) compose into one coherent character identity? Patterns to survey: hierarchical-prompt-decomposition / chain-of-thought / role-based-multi-pass / structured-output-with-layer-tags / RAG-over-design-substrate.
- **Q-SC3-2**: What patterns produce **identity-at-L1-with-no-gear** cohesion — i.e., the character's narrative identity holds against the chain composition substrate independent of legendary/set themes? Survey: weighted-substrate-prompting / progressive-disclosure / persona-anchor-over-modifiers.
- **Q-SC3-3**: For **T4-choice-independence** (multiple T4 paths cohere with the same CORE identity, just expressed differently per path) — what architecture patterns enable per-T4-variant flavor while preserving core thematic anchor? Survey: variant-generation / conditional-flavor-overlay / branch-aware-prompt-templates.
- **Q-SC3-4**: For **endgame-nod-additivity** (legendary/set themes additively nod to CORE without replacing it) — what call patterns prevent endgame theme from dominating? Survey: anchor-prompt-with-flavor-overlay / explicit-composition-instructions / multi-pass-with-anchor-preservation.

### 7.2 Methodology recommendations table

For each architecture pattern surveyed, recommendation table:

| Pattern | Layered-cohesion fit (1-5) | Identity-at-L1 fit (1-5) | T4-independence fit (1-5) | Endgame-additivity fit (1-5) | Implementation complexity | AI-tell risk | Recommended for Phase 5? |
|---|---|---|---|---|---|---|---|

Top 2-3 recommendations with detailed integration sketch (which LLM model class; prompt structure; output structure; validation method).

### 7.3 AI-tell mitigation

- **Q-SC3-5**: What AI-tell failure modes does the layered-cohesion architecture risk? Survey: formulaic phrasing / pattern-detection from repeated prompt-shape / homogeneous flavor-text across N characters / generic-fantasy-tropes / "and behold" phrasing class / etc.
- **Q-SC3-6**: What mitigation patterns are documented in LLM-narrative-generation literature? Survey: variant-seeding / persona-diversification / anti-pattern-detection-pass / multi-model-consensus / per-character-substrate-anchoring.
- **Q-SC3-7**: How does Phase 5's specific substrate (16 characters × 12 chain skills × 11 gear slots ~ 2,100 calls per season) interact with AI-tell risk at scale? What detection methods at season-emit-time identify AI-tell patterns?

## References

- `canonical/46-concentration-architecture-2026-05-27.md` § 6 Layer 6 (layered cohesion)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` D7 (AI-tell discipline)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 3 + § 9.2 (LLM call budget context: ~2,100 calls per season at $0.50-$5 cost)
- `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2 (P5 hotspot)
- Engineering disciplines #18 + #19 + #11
- Prior legolas Mode A research artifacts at `agentic_orchestration/research/` for tone + format reference
