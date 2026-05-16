# Request to knight-rider — No-seed cosmology-generation empirical test

**From:** gandalf
**To:** knight-rider (to dispatch onward to rocket + star-lord when appropriate)
**Date:** 2026-05-16
**Priority:** **Not urgent.** Captured for the right moment per Matt's direction. Land when (a) capacity allows for the rocket pipeline configuration work, (b) capacity allows for star-lord observer LLM call template work, and (c) the experiment's findings would meaningfully inform near-term work (e.g., pre-pitch validation; pre-Stage-A2 architecture decisions; or simply when there's appetite to resolve a known high-stakes open question).
**Type:** Cross-seam empirical experiment with gandalf review on findings.

---

## What's being requested

Run a one-time empirical experiment that resolves the **residual-bias open question** named in `canonical/37-form-bias-diagnosis-and-recovery.md` § 6.5 (high-stakes open):

> *"Residual bias. Even told 'two opposition pairs for a deep-sea cosmology, do not echo Earth-realm classical elements,' the LLM may still reach for water/air/fire/earth analogs because those patterns are deeply trained in. Reliability of anti-bias scaffolding under generation drift (across thousands of calls per season) is unknown without empirical test."*

The experiment: **run the seasonal generation pipeline WITHOUT anchor-driven cosmological seed, then reverse-derive D1 (cosmological register) from the generated D2-D9 content.** The outcome of the experiment determines whether the engine is a *cosmology generator* (produces novel coherent cosmologies from minimal input) or a *cosmology amplifier* (requires seeded cosmology to produce coherent content) or a *training-default leaker* (defaults to fantasy-cliche when anti-bias scaffolding isn't reinforced by the seed).

## Background context

**Locked canonical reference:** `canonical/story/season-feel-rubric.md` § "Reverse-validation — the convergence-pattern applied to D1" — locked 2026-05-16. Names this experiment as Variant 2 (no-seed reverse-test) of the reverse-validation methodology. Articulates the three diagnostic outcomes.

**The architectural claim this experiment tests:**

Per `canonical/story/engine-generic-meta-structure.md` § "The three-layer model": the engine is currently framed as L1 substrate + L2 cosmology + L3 per-season content. A licensee gets L1 + LLM infrastructure; they bring their own L2 cosmology.

If the experiment surfaces **Outcome 1 (coherent cosmology emerges without seed)**, this framing is too conservative. The engine has cosmology-generation capability the current pitch doesn't claim. The licensing surface shifts — a licensee may *choose which cosmologies to ship from the engine's outputs* rather than *author their own L2 cosmology.* That's a meaningfully different product positioning.

If **Outcome 2 (cosmology-amplifier confirmed)**, the current framing is correct.

If **Outcome 3 (training-default leakage)**, the cipher architecture's anti-bias scaffolding is weaker than doc 37 § 6 admits. The architecture needs hardening before scaling to many seasons; the seed is doing more work than the architecture credits.

**Why the experiment matters even when not urgent:**

- One of the few project-wide opens where a single empirical test directly resolves the question
- Outcome shapes pitch-defensibility claims (engine genuinely generates cosmologies vs requires substrate authoring)
- Outcome shapes near-term work priorities (anti-bias scaffolding hardening if Outcome 3; cosmology-curation tooling if Outcome 1; current pipeline maturation only if Outcome 2)
- Resolves a doc 37 § 10.1 high-stakes open question (named as needing empirical prototyping, not further conceptual work)

## Experiment scope

### What the experiment runs

**One-time test, three configurations:**

1. **Baseline run** — generate a season with the current standard pipeline (anchor-driven cosmological seed). This is the control; D2-D9 generated against a known cosmology. Already producible from the existing engine; no new code required.
2. **No-seed run** — generate a season with the anchor-driven cosmological seed REMOVED (or stubbed to maximum anti-bias scaffolded abstract-only input). Only the cipher's Primary / Secondary opposition labels (per doc 37 § 6) provide structure. **This is the experimental configuration; requires rocket pipeline work.**
3. **Cross-comparison reverse-derivation** — for BOTH runs, an independent (context-isolated) LLM call ingests only the generated D2-D9 content and reverse-derives D1. Outputs structured (cosmological articulation paragraph + register keywords + world-mythology framework comparison). **Requires star-lord observer LLM call template work.**

### What rocket provides

- Pipeline configuration for the no-seed run mode (could be a flag on the season-generation CLI or a separate test-only entry point; rocket's call which serves better)
- Documentation of what's removed in no-seed mode vs what stays (the cipher's abstract pair-structure must persist; the canonical-four cipher persists for resistance translation; what's removed is the anchor-as-cosmological-prompt-context)
- Confirmation that the no-seed run produces a complete D2-D9 output (the same export-packet shape; just without the anchor's cosmological seed influence)

Estimated rocket work: ~2-4 hours. Mostly configuration; possibly a small LLM-prompt-context conditional.

### What star-lord provides

- Observer LLM call template that ingests a season's D2-D9 export packet
- Context isolation: separate API call; no shared context with the generator
- Anti-bias scaffolding in observer prompt (per Discipline #14 candidate): no canonical-four labels, no archetype labels, no mechanical-property names, no attribute axis labels — observer works from per-instance vocabulary and content only
- Structured output spec: (a) cosmological articulation paragraph; (b) register keywords; (c) world-mythology framework comparison; (d) confidence-and-coherence categorical (high / mixed / low)
- Cost tracking on the observer call
- Ideally: a different LLM model for the observer than the generator (strongest independence)

Estimated star-lord work: ~3-5 hours. Template authoring + integration with the existing pipeline.

### What gandalf provides

- Review the outputs of all three configurations
- Apply the outcome categorization (Outcome 1 / 2 / 3 per `season-feel-rubric.md` § "Reverse-validation")
- Author findings memo at `agentic_orchestration/gandalf/findings/2026-05-XX-no-seed-cosmology-test-findings.md`
- Recommend decisions-log entry capturing the resolution of doc 37 § 6.5

Estimated gandalf work: 1-2 hours (review + memo), assuming runs produce inspectable outputs.

### Total cross-seam scope

~6-11 hours of focused work across three seams + gandalf review. Not large; just needs coordination + Matt's authorization for the LLM-cost-budget (the experiment runs ~3-5 LLM calls for generation + 2 observer calls; total expected cost: ~$5-15 for the full experiment).

## Direct-dialogue option

Per Matt's standing pattern (same as Elrond catalogue-rubric commission + this earlier engine-balance-stewardship commission): if either rocket or star-lord wants to dialogue directly with gandalf during the experiment setup or output interpretation, that pattern is available. Knight-rider can coordinate timing but does not need to be present.

Specifically useful:
- For rocket: discussing what "anchor-driven cosmological seed removal" means in concrete pipeline-configuration terms — gandalf can clarify the intent
- For star-lord: discussing the observer LLM call's anti-bias scaffolding — gandalf wrote the scaffolding intent and can refine prompt language
- For gandalf review: discussing edge cases in the output (e.g., if the no-seed run produces partial-coherence; if the baseline and no-seed runs both reverse-derive to similar cosmologies — these are interesting findings that warrant conversation rather than categorical labeling)

## What this commission unblocks

When the experiment runs and findings land:

- **Doc 37 § 6.5 residual-bias open is resolved.** Decisions-log entry captures the resolution.
- **Engine commercialization framing is sharpened.** Per Outcome 1/2/3, pitch claims about engine generative-capability are calibrated against empirical evidence.
- **Pre-flight quality-gate viability is confirmed.** If the seeded reverse-test (Variant 1) works at scale, the per-season pre-flight gate can be operationalized in production.
- **Anchor-prose-notes acceleration becomes feasible.** Per `season-feel-rubric.md` § "Reverse-validation — What both reverse-tests unlock" item 4: generated-seasons-per-anchor + reverse-derivation could seed the 130-anchor `seasonal-anchor-prose-notes.md` long-term work.

## Cross-references

- `canonical/story/season-feel-rubric.md` § "Reverse-validation — the convergence-pattern applied to D1" — the canonical reference for this experiment's design
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6.5 — the open question this experiment resolves
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 10.1 — broader high-stakes opens this experiment touches
- `canonical/story/engine-generic-meta-structure.md` § "The three-layer model" — the architectural claim this experiment tests
- `canonical/story/embodiment-narrative-layer.md` — the form-bias work this experiment validates against
- `canonical/story/naming-triad.md` § "Generation integration" — the per-season-cosmological-vocabulary call architecture this experiment runs against
- AGENTS.md § "Authority tiers" — rocket + star-lord as C-tier implementers; gandalf as A-tier senior critic; coordination through knight-rider
- Decisions-log 2026-05-07 § "Convergence pattern as quality assurance mechanism" — the architectural pattern this experiment instantiates
- File 19 § Phase 02 — the LLM call infrastructure this experiment extends

## What knight-rider should do with this

1. **Read this request** at next invocation; surface to Matt during team-state briefing as a parked experiment.
2. **Sequence the dispatch** when ALL of the following align:
   - Rocket has capacity (not blocked by Stage A2 priority work)
   - Star-lord has capacity (not blocked by current dispatches)
   - The experiment's findings would meaningfully inform near-term decisions (pre-pitch defensibility; pre-Stage-A2 architecture confirmation; or simply available appetite)
3. **Format the dispatch** per Pattern B (longer task; dedicated session) — author dispatch files at `agentic_orchestration/dispatches/` with the rocket + star-lord scope split.
4. **Honor the direct-dialogue request** — include the instruction that rocket and star-lord can invoke gandalf directly during experiment setup or output interpretation.
5. **Authorize LLM-cost-budget** — confirm with Matt that the ~$5-15 experiment LLM-cost is acceptable; this is small but worth Matt's explicit per-statement authorization per ADR-006.
6. **Decisions-log entry on findings** — when the experiment lands, knight-rider drafts; jack-ryan reviews; Matt approves; entry resolves doc 37 § 6.5 + clarifies engine architectural claim.

## Maintenance protocol

- This request file lives at `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`
- When the dispatch is authored by knight-rider, this file gets a status update noting the dispatch tag/path
- When the experiment runs and findings land, this file is closed out
- The findings memo at `agentic_orchestration/gandalf/findings/` becomes the durable reference
- The decisions-log entry resolving doc 37 § 6.5 becomes the canonical lock

— gandalf, requesting 2026-05-16
