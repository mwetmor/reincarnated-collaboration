# Request to knight-rider — Catalogue mapping + grouping derivation empirical experiment

**From:** gandalf
**To:** knight-rider (to dispatch onward to star-lord with gandalf for findings review)
**Date:** 2026-05-16 (Day 4)
**Priority:** **Not urgent, but bounded.** Land when (a) star-lord has capacity for ~30-60 min LLM-call template work, (b) Matt authorizes the ~$5-15 LLM-cost budget per ADR-006, and (c) the form-bias-cadence-strategy doc is in active authoring (the experiment's findings directly inform that doc's Q4). The experiment is parked as a sibling to the no-seed cosmology test (`2026-05-16-no-seed-cosmology-generation-test.md`); both resolve specific architectural opens in the catalogue-track + form-bias work.
**Type:** Cross-seam empirical experiment with gandalf review on findings.

---

## What's being requested

Run two coupled LLM experiments that empirically resolve two named architectural opens in the form-bias-cadence-strategy work:

1. **The α/β/γ per-season-vocabulary-coupling question** — surfaced 2026-05-16 (Day 4) in gandalf-Matt dialogue. The question: when the engine generates per-season vocabulary from the cipher's abstract pair-structure, how reliably can that vocabulary be mapped onto the catalogue's deliverable VFX tag space? The answer determines whether per-season vocabulary should be (α) generated free-form with validation-and-regenerate against catalogue, (β) generated within the catalogue's tag space as an in-prompt constraint, or (γ) generated free-form with runtime fallback to closest catalogue tag.

2. **The multiple-canonical-groupings architecture question** — surfaced 2026-05-16 (Day 4) in the same dialogue. The question: rather than committing to one fixed canonical-four (or canonical-seven, or canonical-nine) cipher, can the catalogue's tag space support **multiple valid opposition groupings** that the engine selects from per-season? If yes, the cipher becomes a **three-layer model** (substrate / grouping / vocabulary) where the substrate is the catalogue's tag space, the grouping is the active per-season opposition structure, and the vocabulary is the LLM-generated names. The substrate is wide (catalogue's full coverage); the per-season grouping is narrow (4-5 active tags); cross-season comparability happens at the substrate layer.

The two experiments share infrastructure and run cleanly back-to-back. The findings shape:
- Form-bias-cadence-strategy doc's Q4 deliverable (the refined-Option-A recommendation gets empirical grounding or refutation)
- Pre-LLM substrate inventory doc's Catalogue-track-dependencies section
- The cipher-width decision (Options A/B/C from the parked canonical-elements thread) resolves through these findings rather than through more conceptual work

## Background context

**Locked canonical references:**
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 (cipher architecture) — Position (ii) locked: per-season vocabulary carries own mechanical signatures; cipher is resistance-translation only
- `canonical/37-form-bias-diagnosis-and-recovery.md` § "Catalogue-based form-bias resolution path" (2026-05-16) — catalogue-based mapping locked as primary implementation strategy
- `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` § "Day 4 re-engagement" — full dialogue trace including terminology lock + per-season-vocab coupling question
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` — Pimen's 9 elements (fire/water/earth/wind/ice/holy/dark/thunder/acid) as current catalogue substrate

**Strategic context — the white-wizard read (2026-05-16 Day 4):** No shipping ARPG ships above ~6-7 simultaneously-active mechanical damage types because the player-cognition ceiling on working combat memory is empirically ~5-7. D4 deliberately reduced from D3 (7 → 6); PoE held at 5 across a decade and through PoE 2's redesign; Last Epoch (7) and Grim Dawn (9) have community discourse on mechanical overlap. The constraint is player-cognition bandwidth, not designer-tuning bandwidth.

Reincarnated's procedural-seasonal-generation primitive enables a **bandwidth multiplier** the genre hasn't tried: wide engine substrate × narrow per-season grouping. The seasonal rotation absorbs the expansion cost the genre normally pays. Genre-internal precedent: Solo Leveling's Shadow Army (100+ accumulated; 5-8 active per fight); Hollow Knight's charms (45 charms; 5-8 notch-equipped at a time). The pattern works when the active set per session passes mechanical-distinctness and role-coverage filters.

This experiment validates whether the catalogue's tag space can actually produce multiple valid groupings that pass those filters, or whether the genre constraint reasserts and we should land on a single fixed grouping (refined-Option-A as one fixed grouping; not multiple).

## Experiment scope

### Experiment 1 — α/β/γ mapping test

**What it tests:** Given the catalogue's known tag space (Pimen's 9 elements as current substrate), can a Claude API call reliably map novel per-season vocabulary words onto the substrate?

**Candidate vocabulary list** (15-20 candidates spanning cosmological diversity):

*Earth-realm-fantasy-default cosmology (expected to map cleanly):*
- ember, flame, scorch
- frost, glacier, freeze
- tremor, stone, ore
- gust, gale, breath

*Non-fantasy-default cosmology (mixed difficulty):*
- pressure, vacuum, bioluminescence (deep-sea)
- void, matter, radiation (cosmic)
- glacier, aurora, permafrost (ice-age)
- rust, oil, static, friction (rust-tech)

*Genuine-failure candidates (expected to fail mapping):*
- harmony, dissonance, melody, rhythm (music-spirit — no Pimen analog)
- ego, shadow-self, dream-logic (psychological)
- silence, echo, gravity (abstract-physical)

*Distinctness-collapse candidates (expected to map to the same tag):*
- scorch + ember (both Pimen-fire)
- glacier + permafrost (both Pimen-ice or split fire/ice)
- void + dark (both Pimen-dark, probably)

**Per-candidate LLM call:**
```
You are mapping a fantasy-cosmology vocabulary word onto a fixed set of
available element categories. Given:

  Vocabulary word: {WORD}
  Available element categories: fire, water, earth, wind, ice, holy, dark,
                                thunder, acid

Choose the SINGLE best mapping. Output JSON only:

{
  "chosen_tag": "...",
  "confidence": 0.0 to 1.0,
  "reasoning": "1-2 sentences on why this tag best fits the word's mechanical
                and cosmological associations",
  "alternatives_considered": [
    {"tag": "...", "confidence": 0.0 to 1.0, "reason_not_chosen": "..."}
  ],
  "preservation_quality": "high|medium|low — does the mapping preserve the
                           cosmological meaning of the word or is it lexical
                           fallback?"
}
```

**Runs per candidate:** 4. Different seeds; same prompt. Captures consistency.

**Scoring per candidate** (gandalf-side, post-run):
- *Map success rate:* % of 4 runs producing `confidence ≥ 0.6`
- *Map consistency:* % of 4 runs choosing the same `chosen_tag`
- *Map quality:* avg `preservation_quality` (high/medium/low → 3/2/1) across runs
- *Ambiguity:* avg count of alternatives with `confidence ≥ 0.4` (proxy for split mappings)

**Aggregate signal:**
- If most candidates score *high success + high consistency + high quality + low ambiguity:* **γ fallback is viable.** Free-form vocabulary generation + runtime mapping works.
- If candidates map but quality is lexical-fallback only: **α validation+regenerate.** Reject low-quality maps; the regeneration cost is the seasonal failure rate.
- If many candidates fail outright or split ambiguously: **β in-prompt constraint.** Vocabulary generation must live inside the tag space, not be mapped post hoc.

### Experiment 2 — Multiple-groupings derivation

**What it tests:** Given the catalogue's tag space, can a Claude API call propose multiple thematically-coherent AND mechanically-distinct AND role-orientation-complete opposition groupings?

**Single LLM call** (run 4-5 times for consistency):
```
You are designing opposition groupings for an action RPG's elemental system.
Given these 9 available element tags:

  fire, water, earth, wind, ice, holy, dark, thunder, acid

Propose 3-5 distinct opposition groupings, where each grouping selects 4-5 of
the 9 tags and defines their oppositions. Each grouping should:

1. Be thematically coherent (the selected tags share a cosmological logic)
2. Be mechanically distinct (each tag in the grouping must have a different
   combat feel — DoT vs control vs burst vs sustain — NOT two tags that
   would feel mechanically similar in play)
3. Cover the role-orientation taxonomy (damage / control / hybrid). At least
   one tag suited to each role.

Output JSON only:

{
  "groupings": [
    {
      "name": "...",
      "active_tags": ["...", "...", "...", "..."],
      "primary_opposition": ["tag_a", "tag_b"],
      "secondary_opposition": ["tag_c", "tag_d"],
      "cosmological_logic": "1-2 sentences",
      "mechanical_signatures": {
        "tag_a": "DoT|control|burst|sustain|... — and why",
        ...
      },
      "role_coverage": {
        "damage": "tag_a, tag_c",
        "control": "tag_b",
        "hybrid": "tag_d"
      },
      "genre_recognition": "Would a Diablo / PoE player recognize this
                            grouping's archetypes? 1 sentence."
    }
  ]
}
```

**Scoring per proposed grouping** (gandalf-side, post-run):
- *Mechanical-distinctness:* are the 4-5 tags' mechanical signatures genuinely different, or does the LLM produce two similar-feeling tags? (Reject groupings with overlap.)
- *Role-orientation coverage:* does each grouping cover damage + control + hybrid? (Reject groupings missing a role.)
- *Genre-recognition:* would a D2 / PoE / D4 player feel the archetypes viscerally, or just learn them intellectually? (Down-weight low-recognition groupings.)
- *Consistency across runs:* are similar groupings proposed across 4-5 runs? (High-consistency groupings are robust; one-off proposals may be noise.)

**Aggregate signal:**
- If 3-5 robust groupings emerge that all pass the three filters: **multiple-groupings architecture is viable.** Refined-Option-A as a wide-substrate / narrow-grouping cipher is empirically grounded.
- If only 1-2 groupings pass filters: **single fixed grouping is the right shape.** Refined-Option-A collapses to a specific 4-5-tag cipher (the surviving grouping); the wider substrate exists for catalogue coverage but only one grouping is active across all seasons.
- If 0 groupings pass filters: the genre constraint reasserts. Stay at canonical-four; the catalogue maps onto it via curation; no architectural change beyond hiding labels from LLM per doc 37 § 6.

### Cross-experiment synthesis

After Experiments 1 and 2 land, re-run Experiment 1's candidate-vocabulary tests against EACH grouping from Experiment 2. Some candidates may map well in one grouping but poorly in another. The synthesis tells us:

- Which grouping best handles the diversity of cosmologies we'd want to ship
- Whether per-season grouping selection should be driven by anchor cosmology (anchor → grouping → vocabulary) or by other criteria
- Which candidate vocabulary words to seed deliberately into seasonal generation for stress-testing the architecture

## What rocket provides

Nothing — this experiment runs out-of-pipeline. It does not require generation-seam changes. Rocket may be consulted for "is this candidate vocabulary list aligned with what the per-season generator would actually produce?" but is not on the critical path.

## What star-lord provides

- LLM call template for Experiment 1 (15-20 candidates × 4 runs = 60-80 calls)
- LLM call template for Experiment 2 (single prompt × 4-5 runs = 4-5 calls)
- Context isolation: separate API calls; no shared context between candidates
- Anti-bias scaffolding in prompts (per Discipline #14 candidate): the experiment prompts should NOT expose canonical-four labels as "the underlying truth." The available tags are presented as Pimen's tag space, not as canonical-four-mapped categories. Important: this is the experiment's whole point — what does the LLM do when given the catalogue's actual coverage as the substrate?
- Cost tracking
- Output structured to JSON spec above; saved to `agentic_orchestration/research/experiments/2026-05-XX-catalogue-mapping-results/` (one file per candidate for Experiment 1; one file per run for Experiment 2)

Estimated star-lord work: ~1-2 hours. Template authoring + integration with existing LLM client + result-file structuring.

## What gandalf provides

- Review all outputs against the scoring rubrics defined above
- Author findings memo at `agentic_orchestration/gandalf/findings/2026-05-XX-catalogue-mapping-experiment-findings.md`
- Recommend α/β/γ choice + single-vs-multiple-groupings architectural choice based on findings
- Update the form-bias-cadence-strategy doc's Q4 with empirical grounding
- Recommend decisions-log entry capturing the resolution

Estimated gandalf work: 1-2 hours (review + memo + strategy-doc update), assuming runs produce inspectable outputs.

## Total cross-seam scope

~3-5 hours of focused work across star-lord and gandalf + Matt's authorization for the LLM-cost-budget. The experiment runs:
- Experiment 1: ~20 candidates × 4 runs × ~400 tokens per call ≈ 32,000 tokens ≈ ~$5 at Claude Sonnet pricing
- Experiment 2: ~5 runs × ~600 tokens per call ≈ 3,000 tokens ≈ ~$1
- Cross-experiment synthesis: ~20 candidates × ~3 active groupings × 1 run each ≈ 24,000 tokens ≈ ~$4

Total expected cost: ~$10-15. Small but worth Matt's explicit per-statement authorization per ADR-006.

## Direct-dialogue option

Per Matt's standing pattern: if star-lord wants to dialogue directly with gandalf during template authoring or output interpretation, that pattern is available. Knight-rider can coordinate timing but does not need to be present.

Specifically useful:
- Star-lord may want to refine the prompt templates to ensure they don't accidentally expose canonical-four bias (the prompt's whole point is to NOT expose canonical-four as substrate truth)
- Gandalf may want to refine candidate vocabulary list based on rocket-inventory findings if any additional candidates surface during the inventory doc authoring
- Gandalf review may surface edge cases (e.g., a candidate that maps cleanly in two of four runs and ambiguously in two others — what does that signal mean?)

## What this commission unblocks

When findings land:

- **Per-season vocabulary coupling policy** (α/β/γ) resolves with empirical grounding
- **Multiple-groupings vs single-grouping architectural choice** resolves with empirical grounding
- **Refined-Option-A recommendation** in form-bias-cadence-strategy doc Q4 gets empirical defense or refutation
- **Cipher-width decision** (Options A/B/C from the parked canonical-elements thread) resolves into the strategy doc's locked outcome
- **Foundation layer placement** (Flag B from rocket inventory) gets architectural framing — Foundation either grows with the substrate or decouples
- **D1 pool reconsideration** can be scoped against the resolved cipher architecture rather than against canonical-four assumptions

## Cross-references

- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 — cipher architecture (resistance-translation cipher; Position (ii) lock)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § "Catalogue-based form-bias resolution path" — catalogue-based mapping as primary
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 10.1 #1 — mechanical-signature pool open (shared / per-season / hybrid) — this experiment empirically informs
- `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` — full Day-4 dialogue trace
- `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` — sibling parked experiment; the no-seed test resolves residual-bias, this experiment resolves substrate-mapping
- `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md` — rocket inventory findings; Flag A (D1 rubric) and Flag B (Foundation layer placement) both informed by this experiment
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` — Pimen's 9 elements as current substrate
- `canonical/story/season-feel-rubric.md` § "Reverse-validation" — the experimental methodology pattern this experiment instantiates
- `canonical/story/engine-generic-meta-structure.md` § "The three-layer model" — L1 / L2 / L3 separation; the multiple-groupings architecture proposes a refinement of this model
- Genre-precedent context: D2 (5 elements), D3 (7, with overlap criticism), D4 (6, deliberate reduction), PoE 1 & 2 (5 across 12 years), Last Epoch 1.0 (7, with overlap), Grim Dawn (9, with overlap). Player-cognition ceiling ~5-7 simultaneously-active.

## What knight-rider should do with this

1. **Read this request** at next invocation; surface to Matt during team-state briefing as a parked experiment.
2. **Sequence the dispatch** when:
   - Star-lord has capacity (~1-2 hours; not blocked by current dispatches)
   - Matt has authorized the LLM-cost budget per ADR-006
   - The form-bias-cadence-strategy doc is in active authoring (so findings land while the doc can absorb them)
3. **Format the dispatch** per Pattern B (longer task; dedicated session) — author dispatch file at `agentic_orchestration/dispatches/` with the star-lord scope.
4. **Honor the direct-dialogue request** — include the instruction that star-lord can invoke gandalf directly during template authoring or output interpretation.
5. **Authorize LLM-cost-budget** — confirm with Matt that the ~$10-15 experiment LLM-cost is acceptable; small but worth explicit per-statement authorization per ADR-006.
6. **Decisions-log entry on findings** — when the experiment lands, knight-rider drafts; jack-ryan reviews; Matt approves; entry resolves the α/β/γ + single-vs-multiple-groupings opens.

## Maintenance protocol

- This request file lives at `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`
- When the dispatch is authored by knight-rider, this file gets a status update noting the dispatch tag/path
- When the experiment runs and findings land, this file is closed out
- The findings memo at `agentic_orchestration/gandalf/findings/` becomes the durable reference
- The decisions-log entry resolving α/β/γ + multiple-groupings becomes the canonical lock
- The form-bias-cadence-strategy doc absorbs the findings into Q4 at the time of authoring

— gandalf, requesting 2026-05-16 (Day 4)
