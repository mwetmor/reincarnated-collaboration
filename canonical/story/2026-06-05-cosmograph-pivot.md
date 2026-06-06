# Recognition Record — Chernoff Celestial Body as Cosmograph (architectural pivot)

**STATUS:** CURRENT (recognition record; load-bearing architectural commitment)
**Date:** 2026-06-05
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-05 verbatim ratification: "Confirm. And I want to add that it solves for a key question that I had about the creation process. What does a player do when presented with a blank canvas?"
**Type:** load-bearing architectural recognition — the chernoff-celestial-body's true rendering form is an interactive cosmograph, not a cinematic constellation animation

---

## 0. TL;DR

The chernoff-celestial-body concept — the load-bearing player-facing visualization of substrate-as-emergent-character-form — should be rendered as an **interactive cosmograph (force-directed graph of BC cells / vector points / labels)**, NOT as a cinematic video sequence as previously prototyped via Veo 3.1.

The cosmograph:
- IS the chernoff substrate visualization (the video was an approximation)
- Eliminates Veo's rendering limitations (text garbling, count drift, structural reflexes)
- Solves the **blank-canvas onboarding problem** for the character creation UX
- Composes cleanly with the engine's actual high-dimensional substrate architecture
- Remains compatible with cinematic Veo work for the post-confirmation materialization payoff

This recognition emerged through 4 video-iteration attempts that surfaced increasingly clear evidence that the abstraction was wrong, not that the prompts needed more refinement.

---

## 1. The recognition path (how we got here)

Iteration history feeding this recognition:

1. **Original Veo prompt (2026-06-03):** painterly cosmic constellation materialization to L1 apprentice — landed beautifully and validated the painterly cosmic register as the right aesthetic anchor.

2. **Clip 1 v1 (substrate-input phase, 2D palette + cursor):** failed text rendering across HUD + palette labels. Diagnosed as "image-gen models can't reliably render technical text."

3. **Clip 1 v2 (cosmograph-adjacent, 6 planets + orbiting icons):** rendered 4-5 of 6 planets; added invented central sun; orbital path ellipses appeared despite negative constraint; ring proliferation across multiple planets despite single-ring directive.

4. **Clip 1 v3 (compass directions enumerated):** position-shorthand strings ("upper-LEFT") rendered as overlay text labels ("UL", "UR", "MR", "LL"); reintroduced text failure mode.

5. **Clip 1 v4 (hexagonal ring framing + explicit no-central-object):** improved but the structural reflexes (Veo's "solar system diagram" training) persisted as background noise.

**The recognition** (Matt 2026-06-05): instead of fighting Veo's training biases on every iteration, render the substrate visualization through a tool whose primitives MATCH the chernoff principle natively. Cosmograph.app (https://cosmograph.app) does exactly this — force-directed graph layouts on high-dimensional embeddings, native lasso interaction, WebGL performance for large node counts.

---

## 2. Why the cosmograph is structurally right

### 2.1 Architectural fidelity

The engine's substrate IS a high-dimensional space (cycle 14 Pareto reduction work, canonical 39 Architecture B substrate-bound generation, canonical 43/44 multi-T4 chain architecture). Cells in `kit_archive.db` have coordinates across element_primary, archetype, role_orientation, damage_focus, survivability_tier, mitigation_profile, cultural_tradition, period, and others.

A cosmograph rendered from dimensionality-reduction (UMAP/t-SNE/PCA) of these coordinates produces a 2D embedding that:
- Preserves substrate-neighborhood structure (similar kits cluster)
- Visualizes categorical labels (cluster shapes communicate "boss-killers here, supports there")
- Honors the substrate-led discipline (Phase E-2 cluster-labeling work, Discipline #59 substrate-coverage)
- Maps directly to canonical 39's substrate-BOUND Phase 2 architecture

The video was always an artistic representation of this. The cosmograph IS this.

### 2.2 Eliminates Veo's rendering limitations

Four iterations exposed four failure modes that are NOT prompt-engineering problems but training-bias problems:
- Text-rendering unreliability (any string in the prompt risks becoming visible label text)
- Count drift (Veo "summarizes" longer enumerations to fewer rendered objects)
- Structural reflexes (solar-system associations pull toward central suns, orbital path lines, Saturn rings)
- Attention dilution at longer prompts (icon detail degrades as constraints accumulate)

A purpose-built graph visualization eliminates all four. We render exactly what we specify; the count is deterministic; there are no training biases for substrate-visualization to fight.

### 2.3 The blank-canvas player-experience win (Matt 2026-06-05)

The character creation UX faces a known onboarding-design problem: a player presented with a blank-canvas selection system must make multiple commitments before seeing what they're building. Risk: dropout before reaching gameplay.

Trait-by-trait commit pattern (what we'd been designing):
- Empty canvas
- Click an icon → some abstract change
- Click another → more abstract change
- Click a third → still abstract
- Player asks: "where's my character?"
- Risk: confusion, boredom, annoyance, dropout

Cosmograph + lasso pattern (the pivot):
- The substrate landscape IS the activity from frame one
- The cosmograph is visually engaging on its own (cluster shapes communicate semantic groupings)
- Lasso a region → immediately see which cells got selected AND which categorical labels result AND a placeholder spirit form
- Player can experiment freely: lasso here, lasso there, see differences
- Iteration is low-friction: re-lasso, swap selections, modify
- No "blind groping" — every action has immediate compositional preview
- Engagement is intrinsic to the activity, not delayed until materialization

This is not a marginal UX improvement. The trait-by-trait pattern carries known dropout risk at the "3 random clicks, no payoff" beat. The cosmograph pattern carries continuous payoff from frame one because the substrate landscape itself is informative and the lasso gives immediate compositional feedback.

### 2.4 Composability with downstream architecture

The cosmograph becomes a real player surface that plugs into the engine, not a one-shot validation video:
- Live URL demonstrable to peers (drax-owned, deployable to Vercel like loadout)
- Real substrate data from kit_archive.db (elrond-curated)
- Replays/extends as future seasons add cells (no re-shoot needed)
- Composes with the existing loadout app (could replace or extend featured-picks)
- Provides a real chernoff-celestial-body interaction primitive for the entire game's character lifecycle, not just MM-P1 validation

---

## 3. What is preserved from the Veo work

The Veo iteration is NOT wasted. It contributed:

1. **The original materialization prompt (2026-06-03)** — the constellation-to-L1-apprentice cinematic — remains LOAD-BEARING for the post-confirmation **materialization payoff**. After the player lassos a substrate region in the cosmograph and confirms, the resolved selection should materialize into the apprentice character via a cinematic moment. The original Veo prompt does this beautifully.

2. **The L50 reveal cinematic** remains the right vehicle for ascension. The character at mastery is a character-design moment that wants a rendered image or short cinematic, not a graph visualization.

3. **The painterly cosmic register** as the aesthetic anchor for both materialization and reveal cinematics carries forward.

4. **The substrate vocabulary** (BC cells, vector points, categorical labels, derived classifications like BOSS-KILLER) developed during the trait-iteration design surfaces directly into the cosmograph's node identities + side-panel labels.

5. **The four iteration learnings** about Veo's strengths and limits inform future cinematic prompts (when we re-engage Veo for the materialization payoff).

---

## 4. Recontextualized architecture

### 4.1 Critical runtime boundary — engine pre-generates; game selects

The runtime flow is **substrate-selection → character-LOOKUP**, NOT substrate-selection → character-generation. Architectural boundary:

- **Engine (Python; offline/batch)** pre-generates the kit corpus via QDX/EAA/etc. pipelines and packages it as a JSON packet (`kit_archive.db` + downstream export)
- **Game-side (web client at runtime)** receives the JSON packet, renders the cosmograph from each shipped kit's substrate-trace vector, listens for player lasso, and DOES THE MATCHING — finds the nearest pre-generated character to the lassoed centroid
- "Materialization" in this document means **game-side lookup-and-display of the matched pre-generated character**, NOT runtime character generation. The engine has already derived everything (categorical labels, identity name, T4 selection, kit content); the game READS what the engine produced and displays it

This composability is honest to canonical 39 Architecture B substrate-BOUND: the engine binds substrate to content during Phase 2 generation; the game's runtime job is selection, not generation.

### 4.2 Player journey + tool stack

```
PLAYER JOURNEY:
[Cosmograph substrate exploration] → [Lasso region] → [Game looks up nearest
                                                       pre-generated character +
                                                       displays matched spirit preview]
        ↓ player iterates (re-lasso, swap, modify)
[Player confirms]
        ↓
[Cinematic materialization payoff — Veo's original constellation→apprentice prompt,
 either pre-rendered per kit or runtime-fired with matched kit's substrate as input]
        ↓
[Gameplay: the matched apprentice plays through the seasonal journey]
        ↓
[L50 ascension cinematic — short Veo clip or rendered image]
```

| Layer | Tool | Owner | Generation timing | Status |
|---|---|---|---|---|
| Kit corpus generation | Engine (Python; QDX/EAA pipelines) | rocket + gamora + elrond + star-lord | OFFLINE / BATCH | Existing; substrate-thin per QDX-5 governance lapse |
| JSON packet export | Engine export pipeline | star-lord | OFFLINE | Existing |
| Substrate exploration + lasso UX | Cosmograph (web, React) | drax (frontend); elrond (data) | RUNTIME (client-side) | NEXT — to scope and commission |
| Substrate-to-character lookup | Cosmograph app frontend logic | drax | RUNTIME (client-side) | NEXT — game-side matching, NOT engine generation |
| Spirit preview display | Side panel reading pre-computed kit fields | drax | RUNTIME (client-side) | NEXT — reads `name`, `categorical_labels`, `t4_selection`, etc. from matched kit |
| Post-confirm materialization cinematic | Veo 3.1 (original prompt as foundation) | gandalf (prompt design) + Matt (executes via veo_runner) | RUNTIME or pre-rendered (TBD) | PARKED — re-engage after cosmograph milestone |
| L50 ascension cinematic | Veo 3.1 or rendered image | gandalf + Matt | RUNTIME or pre-rendered (TBD) | PARKED — re-engage after materialization |

---

## 5. Pre-milestone scoping framework (the 5 questions before commissioning)

The minimum-viable cosmograph milestone needs scope answers BEFORE drax can commission anything:

1. **Substrate data source.** Which existing data feeds the cosmograph? Options:
   - 37 QDX-5 kits in `kit_archive.db` (most recent; thin per governance lapse)
   - 25 historical EAA-5 v2 archived kits
   - Combined corpus (~60 cells)
   - Synthetic test data while real substrate gets curated
2. **Coordinate-axis selection.** Which substrate axes drive dimensionality reduction into 2D? All ~13? A curated load-bearing subset?
3. **Visual encoding rules.** Node color by what axis? Node size by what saliency? Edge rules (substrate-similarity links) yes or no?
4. **Spirit-preview behavior.** Minimum: side-panel text showing selected categorical labels. Stretch: placeholder humanoid silhouette. Full: hook for Veo cinematic to fire after confirmation.
5. **Hosting + integration with loadout app.** Standalone deployment? Sub-route on existing loadout? Replaces featured-picks?

These are Pattern B design-call territory before drax commissioning.

---

## 6. Composition with prior decisions

This recognition supersedes:
- The 5-clip Veo manifestation arc design (24s chernoff + 8s customization + 8s ascension) — replaced by cosmograph+materialization+ascension architecture
- The trait palette + cursor selection pattern — replaced by lasso-over-substrate-region
- The HUD coordinate display + derived labels overlay — natural in the cosmograph side panel
- The cursor-as-player-surrogate metaphor — replaced by direct lasso (player's selection action IS the input)

This recognition composes with:
- canonical/29-design-overview.md (strategic anchor; chernoff-celestial-body as core concept)
- canonical 39-qd-engine-end-to-end-workflow-2026-05-24.md (Architecture B substrate-BOUND)
- canonical 43/44 (multi-T4 chain architecture; substrate axes that feed the cosmograph)
- canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md (Realm Expansion content rhythm; cosmograph is the player-facing surface for each Realm Expansion)
- agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md (top-1 Duskweaver remains the worked example through the cinematic payoff)
- agentic_orchestration/gandalf/notes/2026-06-02-mm-p1-top-1-rename-duskweaver.md (Duskweaver identity unchanged)
- agentic_orchestration/gandalf/notes/2026-06-02-mm-p1-self-validation-video-production-playbook.md (production playbook — now recontextualized as cinematic-payoff playbook, not main-validation playbook)

This recognition DOES NOT supersede:
- The substrate-led discipline (Discipline #59)
- The chernoff-celestial-body concept itself (only its rendering surface changes)
- The Realm Expansion architecture
- Duskweaver as the worked-example character
- The original Veo materialization prompt (preserved for post-confirm cinematic)

---

## 7. Disposition / next steps

1. **DONE (this record):** architectural recognition captured to canonical/story/
2. **NEXT:** Pattern B scoping design call on the 5 questions in § 5
3. **AFTER SCOPING:** commission drax with a clean spec to build the minimum cosmograph as a web app
4. **PARKED until cosmograph milestone lands:** Veo iteration work (Clip 1 v4 in clips/ remains as artifact; no further Veo Clip 1 iterations); the materialization-payoff cinematic re-engaged when cosmograph confirms a substrate selection

The Veo harness (duskweaver-mm-p1/veo_runner.py) is preserved for the post-confirm cinematic work. The pre-milestone artifacts in clips/ + prompts/ stand as research evidence for this recognition record.

---

## 8. Sign-off

**Authored:** gandalf 2026-06-05 per Matt verbatim ratification of cosmograph pivot
**Anchor evidence:** 4 Veo Clip 1 iterations (v1-v4) demonstrating structural rendering biases that are training-level not prompt-level; Matt's identification of the blank-canvas player-experience problem as load-bearing
**Routing:** informs next Pattern B scoping design call (5 questions); informs drax commissioning post-scoping; informs elrond substrate-data curation for cosmograph feed
**Empirical-evidence trigger for re-engaging Veo cinematic work:** cosmograph lasso → confirm flow lands in pre-milestone build; gandalf re-engaged to design the post-confirm materialization cinematic from the original Veo prompt foundation

**End of recognition record.**

---

## 9. Amendment 2026-06-06 — primitive-star + kit-as-constellation refinement + architectural-anchor lock

**Authority:** Matt 2026-06-06 multi-iteration design call ratifying Pattern A-deep verdict at `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md` + architectural anchoring on the cemented-future-state architecture

### 9.1 Star granularity REFINED — primitive-as-star + kit-as-constellation

The original cosmograph-pivot record treated kits as the rendered nodes. Per Matt 2026-06-06 pushback ("wouldn't it be better if each star represented a point within the engine's generative space"), the architectural verdict is:

- **Stars are PRIMITIVES** (Layer 0 atomic substrates per the atomic-substrate-registry doc § 1)
- **Constellations are KITS** — named patterns of primitives the engine has connected into Pareto-balanced compositions (the kit's name = the constellation's name; e.g., "Driftstone Warden of the Broken Reach")
- **Brightest stars in a constellation = the load-bearing primitives** (BDI β-driving per `bdi-omega-tau-tables-v1-2026-05-22.md`)
- **Faction overlays group multiple constellations** into shared mythological context

This is substrate-led discipline applied at the generative-substrate layer. The cosmograph mirrors what the engine actually produces (primitives composed into named kits), not just the engine's filtered output.

### 9.2 DP1-DP4 amendments

- **DP1 (data source) AMENDED:** combined QDX-5 + EAA-5 v2 corpus EXPANDED to include the full cycle-14 wave-5 seasons 001+002+003 corpus (~150 kits) PLUS Layer 0 + Layer 0.5 primitive registry per `canonical/story/2026-06-06-atomic-substrate-registry.md`. Per Matt 2026-06-06 Move B authorization: ~850 PROVISIONAL-status simulated constellations populate the cosmograph alongside the ~150 real named-bearers, with explicit demarcation (dotted-line constellations + placeholder identifiers; NO LLM-named identities per D7).
- **DP2 (embedding axes) AMENDED:** the 2D embedding is over PRIMITIVE space, not BC tuple space — UMAP/t-SNE over the ~300-400 first-class atomic primitive stars per atomic-substrate-registry § 6.1.
- **DP3 (visual encoding) AMENDED:** stars are primitives; constellations are kits; element_primary tint applies to primitives via element-attribute coupling; T4 strategies are extra-bright primitives (capstone-keystones); skill-tree-position primitives weighted by tier (T4 capstone brightest).
- **DP4 (spirit-preview) AMENDED:** lasso → primitive set → constellation-overlap scoring → matched kit's pre-computed identity (per verdict § 4.3 algorithm; composite_score = 0.4 × coverage_fraction + 0.3 × density_score + 0.3 × β-weighted overlap).
- **DP5 (hosting at /forge) PRESERVED.**

### 9.3 Architecture-anchor lock

This cosmograph commitment is ARCHITECTURALLY ANCHORED on TWO load-bearing canonical docs:

1. **`canonical/story/2026-06-06-atomic-substrate-registry.md`** — Layer 0 + Layer 0.5 + derivation chains + Naming Layer N1-N4 stack
2. **`canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md`** — Layer 1 + Layer 1.5 + Layer 2 + Layer 3 + cell schema + flag enum + pattern-library Phase A-E roadmap (CANONICAL status as of 2026-06-06)

Together they form the cemented future-state architecture. The cosmograph is the player-facing manifestation of the pattern library; pattern-library cells render as constellations; atomic substrate primitives render as stars; cell_status (PROVISIONAL / PLAYTEST-CONFIRMED / LIBRARY-LOCKED) renders as visual brightness gradient.

### 9.4 Move B simulation strategy (Option B AMENDMENT 2026-06-06: ALL PROVISIONAL simulated)

**Option B amendment per Matt 2026-06-06:** cycle 14 wave-5 named-bearer kits were NOT generated against the future-engine substrate vocabulary (race + ~65-100 mechanic primitives + skill-tree-position + canonical 47/51 additions + atomic-substrate-registry § 1 additions). Force-mapping them as constellations defined over future-engine primitives would CLAIM substrate membership they don't have, violating substrate-led discipline. Therefore: **cosmograph at /forge is FORWARD-LOOKING — renders the future-engine substrate vocabulary as ALL ~1000 simulated PROVISIONAL constellations.** Cycle 14 named-bearer corpus stays at /loadout as empirical-current-state showcase.

| Constellation status | Source | Visual encoding | Lasso behavior |
|---|---|---|---|
| LIBRARY-LOCKED | cell graduated through playtest validation per hypothesis-flow § 6.6 (FUTURE; cycle 15+) | Solid bright constellation lines; full name + narrative in side panel | Resolves normally |
| PLAYTEST-CONFIRMED-CROSS-PLANE | mid-validation per hypothesis-flow § 6.6 (FUTURE) | Medium-opacity solid lines; full name + narrative | Resolves normally |
| PLAYTEST-CONFIRMED-LOW | partial validation (FUTURE) | Lighter solid lines + "PRELIMINARY" badge in side panel | Resolves normally |
| **PROVISIONAL (Phase A — ~1000 simulated)** | **Move B fill; random primitive subsets BDI ω+τ weighted for plausibility per Option B amendment** | **DOTTED constellation lines + "PROVISIONAL — engine has not yet composed this pattern" badge; NO human-readable name (bc_cell_id-style placeholder per D7)** | **Resolves; side panel notes simulated status; q-scores hidden** |

**Cycle 14 named-bearer corpus disposition (Option B amendment):** Duskweaver + 36 others remain showcased at `/loadout` (cycle-18 wave-close empirical artifact). They are NOT rendered as constellations at /forge in Phase A. Future cycle 15+ regeneration against future-engine substrate produces "real" kits that become real constellations at /forge progressively.

**Empirical-evidence trigger to strip simulated kits:** if Phase A Vercel preview review surfaces D7 violation OR validation muddiness OR substrate-led-discipline violation → flip elrond config flag to reduce sim count.

### 9.5 Sequencing per 2026-06-06 ratification

1. ✅ DONE — atomic-substrate-registry doc authored (`canonical/story/2026-06-06-atomic-substrate-registry.md`)
2. ✅ DONE — hypothesis-flow doc CANONICAL amendment (this doc + hypothesis-flow doc both updated)
3. ✅ DONE — cosmograph-pivot architectural-anchor lock (this § 9 amendment)
4. PENDING — ground-state oracle update with all three commitments
5. PENDING — Matt + gandalf primitive-vocabulary-lock design-call (Q2 from verdict § 8)
6. PENDING — elrond commission spec authoring (consumes atomic-substrate-registry § 1 + hypothesis-flow § 4 flag enum)
7. PENDING — drax commission spec authoring (consumes constellation-overlap scoring + Move B demarcation rules)

### 9.6 Sign-off on amendment

**Authored:** gandalf 2026-06-06 per Matt verbatim ratification across multi-iteration design call (NA-substrate-blind framing-audit recognition + kit-as-star vs primitive-as-star Pattern A-deep verdict + hypothesis-flow doc identification as cemented future-state + atomic-substrate-registry authoring + race + skill-tree-position + seasonal-substrate-rotation + Depth-2 derivation + Naming Layer stack + Move B simulation authorization)

**End of 2026-06-06 amendment.**
