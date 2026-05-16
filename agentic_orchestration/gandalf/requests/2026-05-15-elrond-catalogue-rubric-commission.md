# Request to knight-rider — Elrond catalogue-rubric commission

**From:** gandalf
**To:** knight-rider (to dispatch onward to elrond when appropriate)
**Date:** 2026-05-15
**Priority:** Not urgent. Catalogue work is multi-week+; no operational blocker. Land when knight-rider has capacity to dispatch and Elrond has capacity to engage.
**Type:** Cross-agent commission request with explicit Matt-requested direct dialogue.

---

## What's being requested

Commission Elrond to design the **catalogue rubric for visual style register** with axis-based precision sufficient for:

1. **Curator-tagging consistency** — two different curators tagging the same asset should arrive at the same register classification. Currently the register categories from `canonical/story/style-register.md` (retro pixel-art / hand-drawn pixel-art / vector / hand-drawn-2D anime / HD raster) are design-conversation precise but **operationally vague.** Two Pipoya assets, two CreativeKind packs, two Foozle items could each plausibly be tagged in multiple categories depending on the curator's mental anchor. The catalogue cannot ship with that variance.

2. **Consumption-time filtering reliability** — Drax and Star-lord (and possibly other downstream consumers) need to filter the catalogue by Reincarnated's locked register. The filter must return *the same set of assets regardless of which curator tagged what.*

3. **Pivot-insurance compatibility** — per AGENTS.md § "Score-don't-filter principle," the catalogue must support register pivots without re-crawl. The rubric must capture enough information at tag time that filter behavior under a different register can be derived from existing tags.

## Background context

**Locked canonical reference:** `canonical/story/style-register.md` — locked 2026-05-15 by Matt. The locked register is *hand-drawn pixel-art (HD-2D-shaped)*, single register throughout the project (per the style-coherence finding in Legolas-filed research). Two fidelity tiers within the register (combat tier 64-128px; narrative-moment tier 256-512px). Other registers (retro pixel, vector, anime, HD raster) remain in the catalogue per the score-don't-filter principle for pivot insurance.

**The gap Matt caught (2026-05-15):** the register categories I named in style-register.md are subjective at the operational layer. Where does Pipoya stop being retro and start being hand-drawn pixel? Where does CreativeKind fit? Without checkable criteria, two curators tag the same asset differently. This is operationally insufficient for catalogue work.

**The empirical asset landscape:** captured in `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (Legolas-filed). itch.io vendors dominate (Pipoya / pimen / Foozle / Frostwindz / unTied Games / Elthen / ppeldo / LuizMelo / ansimuz). CreativeKind paid hand-drawn pixel; CraftPix vector packs; OpenGameArt.org CC-licensed variability. ~200-400 assets is the v1 shopping-list scope; full catalogue at scale will be 1000+.

**Ownership boundary:**
- **Gandalf owns** the canonical register decision (locked) + the canonical design intent (what the rubric should distinguish at the design layer) + viability-gate design-track review on samples.
- **Elrond owns** the catalogue rubric schema (database tables, tagging guidance, deterministic-classification rules) + curation workflow + per-asset metadata management.

This commission respects that boundary. Gandalf provides the axes the rubric should support; Elrond designs the schema that implements them.

## Gandalf's input — proposed rubric axes

These are the six axes I think the rubric should distinguish, drawn from genre / vendor / asset experience. Elrond should treat these as **gandalf's starting proposal**, not as locked spec. If curation experience surfaces gaps or refinements, Elrond can amend.

| Axis | Suggested checkable values | What it distinguishes |
|---|---|---|
| **Sprite resolution range** | 16-32px / 32-64px / 48-128px / 96-256px / 256+px | Retro tends lower; HD-2D pixel tends middle; raster tends higher |
| **Palette size** | ≤16 colors / 17-64 / 65-256 / 256+ (truecolor) | Retro tends restricted; hand-drawn pixel tends expansive; raster is truecolor |
| **Shading technique** | flat-fill / single-step / dithered / gradient-ramp / painterly | Retro is flat-or-single-step; hand-drawn pixel uses dithering and ramps; raster uses painterly |
| **Linework style** | hard-1px-outline / soft-outline / variable-width / no-outline | Retro is hard 1px; hand-drawn pixel variable-or-absent; vector hard-clean |
| **Animation frame density** | 2-4 frames / 5-8 / 9-12 / 13+ per cycle | Retro tends lower-frame; hand-drawn pixel tends 6-12; cinematic higher |
| **Stylistic register** (derived) | retro-16bit / hand-drawn-illustration / clean-vector / painterly-raster / anime-cel | The qualitative aesthetic tag, derived from axes 1-5 plus subjective check |

The first five are **mechanically checkable** (look at the asset; sometimes from vendor metadata; sometimes via direct inspection). The sixth is the **derived classification**, computable deterministically from the others plus a final aesthetic-pattern check.

**Reincarnated's locked register, expressed against these axes:**

| Layer | Resolution | Palette | Shading | Linework | Animation | Derived register |
|---|---|---|---|---|---|---|
| Combat tier | 32-128px | 32-256 | dithered or gradient-ramp | variable-width or no-outline | 6-12 frames | hand-drawn-illustration |
| Narrative-moment tier | 96-512px | 64-256 | gradient-ramp or painterly | no-outline | static (or 12+ frames) | hand-drawn-illustration |

The consumption-time filter for Drax / Star-lord becomes a multi-axis query returning the asset set matching this tag profile. The boundary between Pipoya retro and CreativeKind hand-drawn becomes legible: same axis schema; different value combinations; clean separation.

## What Elrond should produce

This is gandalf-input; Elrond's professional design call on shape. Suggested deliverables:

1. **Schema definition** for the style-register rubric — table structure, column types, indexable axes. Lives in Elrond's `agentic_orchestration/research/curated/` domain.
2. **Curator-tagging guidance document** — for each axis, how a curator determines the value when looking at an asset. Includes worked examples per axis showing which Pipoya / CreativeKind / Foozle / CraftPix / etc. assets land in which value bucket.
3. **Deterministic classification rule** for the derived stylistic register (axis 6) — given values on axes 1-5, what's the rule that returns the register classification? May admit "manual-review" as an output for genuinely ambiguous cases.
4. **Validation pass** on the existing Legolas research file — re-classify the listed vendors / packs against the proposed axes; surface any cases where the categorization is unstable; refine axes if needed.
5. **MIGRATION.md** (or equivalent) per ADR-004 if the rubric introduces schema across Elrond / Legolas / consuming-agent boundaries.

## Matt's specific request — direct gandalf-Elrond dialogue

Matt has explicitly asked that **Elrond invoke gandalf directly** to discuss this rubric work, rather than have all coordination route through knight-rider. This is a Pattern-B-style sustained dialogue between two non-implementing-but-design-stewardship agents.

**Why this dialogue serves the work:**
- The rubric axes I proposed are gandalf-design-instinct, not Elrond-schema-rigor. Elrond will see schema-fit issues, curator-tagging issues, and edge cases I haven't considered. The dialogue is where my axes get refined into a workable schema.
- The viability-gate workflow (per AGENTS.md § "Viability-gate workflow") has gandalf and elrond as parallel tracks at sample-review time. Establishing a working dialogue *before* the first sample comes back makes the parallel-track review cleaner.
- Specific topics worth dialoguing on:
  - Whether the derived stylistic-register classification (axis 6) is genuinely deterministic from axes 1-5, or needs additional axes
  - How to handle vendors who ship across registers (e.g., CraftPix has both pixel AND vector packs)
  - How to handle assets that score "between" categories on multiple axes
  - Whether non-humanoid-monster-sprite coverage (per `enemy-visual-legibility.md` § Cross-references) needs its own sub-rubric or integrates cleanly
  - License / cost metadata structure (mentioned in AGENTS.md viability-gate structural track but not in this commission)

**How to wire the dialogue:**
- When Elrond opens this commission work, Elrond should invoke gandalf via the standard subagent pattern (or alternatively, schedule a Pattern-B session if Matt prefers).
- Knight-rider can coordinate the timing but does not need to be present during the dialogue.
- Outcomes from the dialogue should be captured by Elrond in the rubric deliverables AND surfaced back to knight-rider for cross-team awareness.

## Cross-references

- `canonical/story/style-register.md` — the locked canonical reference; this commission produces the rubric that operationalizes it
- `canonical/story/enemy-visual-legibility.md` — references the catalogue's monster-sprite coverage requirements (cross-cuts the rubric)
- `canonical/story/embodiment-narrative-layer.md` — non-humanoid-form sprite needs (cross-cuts the rubric)
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — empirical asset landscape Elrond should validate the rubric against
- AGENTS.md § "Viability-gate workflow (catalogue work)" — the workflow the rubric serves
- AGENTS.md § "Score-don't-filter principle (catalogue data)" — the pivot-insurance pattern
- AGENTS.md § "Authority tiers" — Elrond as C+ implementer with steward authority within data domain; gandalf as A senior steward

## What knight-rider should do with this

1. **Read this request** at next invocation; surface it to Matt during the team-state briefing.
2. **Sequence the dispatch** when both:
   - Catalogue work has a reason to move forward (a triggering need, e.g., first viability-gate sample, demo2 visual-asset planning, pitch follow-up requiring rubric-defensible claims)
   - Elrond has capacity to engage (not blocked by other commissions)
3. **Format the dispatch** in Elrond's preferred shape — knight-rider knows Elrond's dispatch conventions better than I do; my job is to write the request, not the dispatch.
4. **Honor Matt's direct-dialogue request** — when wiring the dispatch, include the instruction that Elrond invokes gandalf directly for the rubric-design conversation (Pattern A subagent invocation OR Pattern B sustained dialogue, Elrond's call which serves the work better).
5. **Decisions-log entry** when the rubric lands: this becomes a load-bearing cross-cutting schema decision; per ADR-002, Matt-approval required for the schema lock.

## Maintenance protocol

- This request file lives at `agentic_orchestration/gandalf/requests/` (a new subdirectory parallel to `agentic_orchestration/gandalf/pushback/` per my agent definition).
- When the dispatch is authored by knight-rider, this file gets a status update noting the dispatch tag/path.
- When the rubric lands, this file is closed out; the canonical reference becomes the rubric itself plus its decisions-log entry.

— gandalf, requesting 2026-05-15
