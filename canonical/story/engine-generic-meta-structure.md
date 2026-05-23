# Engine-Generic Meta-Structure

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical.** Authored 2026-05-15 by gandalf as the engine-substrate companion to `cosmology-reincarnated.md`. Serves dual audiences: **future licensing studios** (per `pitch-2026-05-18/one-pager.md` B2B middleware path) and **the Reincarnated team itself** (clarity on which design choices are project-specific vs which are engine substrate).

**Why this doc exists:** the pitch frames Reincarnated as Engine + Game = two combinable products. The pitch's B2B claim — *"License engine to other studios. Game becomes demo, not revenue product"* — presupposes a clean separation between what the engine IS and what Reincarnated-the-game adds on top. Without that separation explicit, both the licensing pitch and the internal-project-discipline drift. This doc operationalizes the separation.

**Companion docs:**
- `cosmology-reincarnated.md` — the project-specific cosmology that consumes this substrate (the Wheel, the Earth Self, the Rift, the third-faction — all Reincarnated-specific)
- `style-register.md` — register lock; consumed by the project layer, not part of the engine substrate
- `naming-triad.md` — Trial / Mirror / Passage names are Reincarnated-specific; the underlying mechanical patterns are engine substrate (see § "The body-swap mechanic family" below)
- `embodiment-narrative-layer.md` — embodiment narrative skin is Reincarnated-and-isekai-shaped; the embodiment axis architecture is engine substrate
- `enemy-visual-legibility.md` — generic player-perception architecture; largely engine-layer
- `court-of-forms.md` — Court framing is Reincarnated-specific; the form-library data model is engine substrate
- File 29 § "Architecture: two engines" — strategic framing for Engine 1 + Engine 2; this doc operationalizes the contract at the Engine 1 layer
- File 30 — engine current-state (what's shipped today); this doc is grounded in current-state
- File 31 — engine future-state projection (what's coming via Track A); referenced where relevant
- Engineering disciplines (12) — meta-process substrate; also licensable

**Pending:**
- knight-rider to draft a decisions-log entry capturing the layer separation pattern (per ADR-002; cross-seam framing impact + pitch readiness)

---

## What this doc is — and isn't

**It is** the canonical reference for what's *engine substrate* (licensable; reusable across hypothetical client games) vs what's *Reincarnated-specific cosmology* (this game's mythology; not part of an engine license). It supports the pitch's engine-licensing claim by making the separation defensible.

**It is not** a feature-list of the engine (file 30 covers current state; file 31 covers future state). This doc operates one layer up — *naming which features are engine-layer vs project-layer*, not enumerating each feature's mechanical detail.

**It is not** a licensing contract or commercial proposal. It is design-intent for what would BECOME the basis of a licensing offer if Matt pursues that path.

---

## The three-layer model

The project's design content separates into three layers. Cleanly distinguishing them is the doc's load-bearing move.

| Layer | What it is | Owner | Licensable? |
|---|---|---|---|
| **L1 — Engine substrate** | The generic, reusable infrastructure: dimensional generation pipeline, balance loop, telemetry, anchor-and-element systems, cipher architecture, embodiment axis, body-swap mechanic family, form-library data model, naming pipeline, simulation engine. Form-agnostic; cosmology-agnostic; licensee-configurable. | rocket / gamora / star-lord seams (engine code) | **Yes** — this is what a licensee gets |
| **L2 — Project cosmology** | Reincarnated-specific: the Wheel, the Earth Self, the Rift, the third-faction, the Court framing, Spirit Guide character, isekai-genre commitment, samsaric / Buddhist influences, naming-triad player-facing labels, Reincarnated-specific anchor library contents. | gandalf (canonical/story/) | **No** — this is Reincarnated-the-game |
| **L3 — Per-season content** | LLM-generated against L2: each season's anchor + elemental vocabulary + class names + monster names + trial-boss flavor + gear flavor + (forthcoming) per-season triad variants and embodiment-narrative modulations. | LLM (via star-lord prompts; rocket generation) | **N/A** — generated at runtime; not licensed |

The L1 / L2 boundary is the load-bearing separation. The L2 / L3 boundary is well-understood already (the engine generates L3 content; the project's L2 cosmology gives the LLM prompt context that shapes generation).

**A licensee gets L1 + the LLM infrastructure that generates L3.** They bring their OWN L2 cosmology — whether that's a different reincarnation framing, a different mythological substrate (Norse / Aztec / Egyptian / sci-fi), a different genre entirely (cyberpunk-bodyswap, mecha-pilot-rotation, etc.). The engine doesn't care about the cosmology; it cares about the *shape* of the cosmology, which the cipher architecture (doc 37 § 6) preserves abstractly.

---

## What's at the L1 engine substrate layer

The engine, today (current state per file 30 with shipped 5 production seasons + Yomi + demo1), delivers the following licensable components. Each is configurable at engine-instantiation time but otherwise generic.

### Generation infrastructure

- **Seasonal anchor system** — library-based place-anchor selection from a curated set (130 entries in Reincarnated's library; a licensee provides their own curated set in their cosmology's register). Deterministic from seed + history. No LLM call at selection time.
- **Element flavor substitution** — LLM-driven per-season vocabulary generation against a canonical-four resistance cipher (per doc 37 § 6). Generic over the canonical four; the licensee can substitute (water → "data" in a cyberpunk reskin; fire → "void" in a sci-fi reskin; the cipher continues to function as long as the four-element resistance structure is preserved).
- **Dimensional class generation** — five axes (element, energy_type, range_profile, role_orientation, armor_weight) with a configurable validity matrix. Produces playable classes + act-bosses. Generic over what the classes ARE; constrained by the validity matrix the licensee configures.
- **Skill generation** — geometry × element × role sampling against archetype-allowed combinations. Geometry palette (16 active types currently; expanding to 25-30 per file 31). Generic over content; constrained by palette + archetype constraints.
- **Monster generation** — multi-tier (swarm / magic / trash / elite / mini-boss / boss / act-boss) with stat templates and skill kits per tier. Generic over content.
- **Trial boss generation** — class-as-trial-boss pattern (the boss IS a player-class-shaped opponent, tuned harder). Reusable across any game where the meta-progression involves "face an opponent who could be you."
- **Gear generation** — 5-tier gradient (common / uncommon / rare / epic / legendary); 10-slot loadout architecture; class-fit profile via 5-axis dimensional fit weights; smart-loot 70/30 hybrid model. Generic.
- **Naming pipeline** — multi-stage LLM cascade (anchor → element flavor → class names → skill names → monster names → trial boss names → gear epic/legendary names). Generic over content; the LLM produces names against whatever cosmology the licensee provides.

### Simulation infrastructure

- **Combat math** — damage resolver, percentage armor + dodge + crit + block + status ailment system. Generic.
- **Convergence balance loop** — multi-band (3 bands: L17/L33/L50 per B14); per-class damage_modifier tuning to target win-rates. Generic over content; configurable per licensee for target-win-rate, band count, and convergence tolerance.
- **Recompose-first iterative tuning** (B14.5) — composition-cycling before numeric-scaling; produces classes that differ by COMPOSITION not by NUMBERS. Generic algorithm.
- **Doppelganger / Mirror validation** — class-vs-self mirror-match validation at three bands per class. Generic mechanical pattern (the Mirror NAME is Reincarnated-specific; the mechanism is engine).
- **Multi-tier monster gauntlet** — tier-diverse encounter composition (per B10 work). PackProxy entity for swarm pack semantics. Generic.
- **Per-skill geometry and timing** — cast_time, damage_resolution_time, i_frame_window, geometry parameters (collision_mode, angle_distribution, sweep_shape, damage_falloff per B11+B13). Generic.

### Meta-progression infrastructure

- **Body-swap data model** — three-path framework (transformation-path / preservation-path / death-offered-transformation-path). Per-encounter choice. Pool dynamics for within-content body-swap targets. Generic over what the paths are *called* (Reincarnated's Trial / Mirror / Passage are L2 labels; the underlying structure is engine substrate).
- **Form library / accumulated-identity data model** — per-content-cycle ascension event; persistent meta-layer accumulation of generated identities. Generic over what the meta-layer IS narratively (Reincarnated's Court is L2; the data model is L1).
- **Skill point and trait progression** — per-class budget (currently 120 SP + per-class trait pool); shaped-balance composition pattern. Generic.
- **Resistance system** — percentage resistance per canonical-four; flat armor for physical. Within-content cap (Reincarnated: +75%); cross-content reset. Generic.
- **Spirit Guide engine API** — marginal-value analysis surface for gear-swap recommendations and skill-allocation recommendations. The mathematical surface is L1; the *character* of the Spirit Guide (Reincarnated's Beatrice-register future-self) is L2. A licensee can wire any in-fiction guide character into the same engine API.

### Architectural patterns (load-bearing; licensable as design substrate)

- **Cipher architecture** (doc 37 § 6) — hide canonical-four labels from LLM-visible surfaces; expose abstract pair-structure layer (Primary Opposition + Secondary Opposition); per-content vocabulary generates against the abstract structure. Generic pattern applicable to any game with cipher-style cosmology.
- **Embodiment axis** (doc 37 § 4) — Position C: slot-as-functional-mechanic + embodiment-as-narrative-skin. Mechanical sameness across forms; narrative variance via per-form skin. Generic to any multi-form game (isekai, mecha-rotation, body-swap-thriller, even simple skin systems).
- **Three-layer naming pattern** — universal mechanical (L1) + cosmology skin (L2) + per-content variant (L3). Established across `naming-triad.md`, `embodiment-narrative-layer.md`, and this doc.
- **Discipline #13 candidate (implicit-pillar drift)** — pattern: design intent unobstructed-by-structural-enforcement drifts during implementation. Counter: structural enforcement of load-bearing pillars (schema, tests, dispatch gates, decisions-log). Generic to any iterative development effort.
- **Discipline #14 candidate (internal-vs-generative schema separation)** — LLM-visible mechanical labels should NOT include canonical-four element names, archetype names, mechanical-property names, or attribute axis labels. Per-instance vocabulary only. Generic.

### Telemetry + LLM infrastructure

- **Per-content telemetry** — generation runs, LLM calls, convergence metrics, fight-log granularity. SQLite-based. Generic schema; configurable extensions.
- **LLM integration** — Anthropic SDK based; consolidated single-call-per-entity pattern (one JSON response producing name + flavor + visual_prompt); cost tracking; retry handling. Generic over the LLM provider (current Anthropic; portable to other providers with prompt-template adaptation).
- **JSON output packet contract** — versioned (`season_manifest_version`); the contract between Engine 1 generation and downstream consumers (renderer, loadout, simulation). Generic format; configurable schema.

### Engineering disciplines (also licensable as process substrate)

The 12 engineering disciplines (`reincarnated-engine/design/working-agreement/engineering-disciplines.md`) are process substrate that a licensee inherits from. These are not generation features; they are working-agreement that makes the engine maintainable. Generic.

---

## What's at the L2 Reincarnated cosmology layer

The project-specific content is canonicalized in `cosmology-reincarnated.md` and its companion canonical/story/ docs. Briefly inventoried here for the layer-separation clarity:

**The cosmology:**
- The Wheel (impersonal fate-mechanism; Reincarnated's specific name)
- The Earth Self (player's persistent identity; player-named at first play)
- The Spirit Guide (Beatrice-register future-self; partial-presence; mythic register)
- The seasonal journey as descent + ascension as return
- The Rift (post-Phase-0 liminal between-state)
- The third-faction (beings not of Earth or Seasonal realms)

**The naming triad** (player-facing labels for the body-swap mechanic family):
- The Trial (act-end ritualized encounter)
- The Mirror (preservation-path opponent; Reincarnated's Mirror name; the mechanism is engine-substrate doppelganger-validation)
- The Passage (death-offered transformation; Reincarnated's Passage name)

**The Court of Forms** (presentational frame for the form library):
- Court as Solo-Leveling-Shadow-Army-inspired navigable assembly
- Named retainers with stations
- Voiced characters emerging over time
- Per-form class-role labeling (dual-label per court-of-forms.md C8)

**The embodiment narrative layer** (per `embodiment-narrative-layer.md`):
- Eight canonical isekai-coded embodiments (humanoid / slime / beast / dragonling / swarm / construct / spirit / plant)
- Per-embodiment vocabulary lookups for gear slots, class roles, body parts, action verbs, injury/death, communication

**The visual style register:**
- Hand-drawn pixel-art (HD-2D-shaped)
- Two fidelity tiers (combat / narrative-moment)
- Single register throughout

**The anchor library specifics:**
- The 130-entry curated place library (the *system* of anchor selection is L1 engine substrate; the *contents* are L2 Reincarnated-specific)

**The player-perception architecture** (largely engine-substrate; but Reincarnated-specific in some details):
- Enemy visual legibility canonical anti-pattern (the rule is generic; the specific tier vocabulary and Mirror-fight exception are coupled to Reincarnated's naming)

A licensee replaces all of L2 with their own cosmology. The mechanical patterns above continue to operate; the *labels and characters and worldbuilding* are theirs.

---

## What an L1 licensee gets vs doesn't get

### What they get

- The full Engine 1 generation pipeline (current state per file 30; near-term roadmap improvements per file 31)
- The convergence balance loop + simulation engine
- The telemetry infrastructure
- The naming pipeline (LLM-based; provider-agnostic with prompt-template adaptation)
- The cipher architecture, embodiment axis, body-swap mechanic family as architectural patterns
- The dimensional class generation framework with configurable validity matrix
- The 16-30 geometry palette with associated VFX-rendering schema
- The 5-tier gear gradient with smart-loot pattern
- The Spirit Guide engine API surface
- The JSON output packet contract
- The engineering disciplines as working-agreement substrate

### What they don't get

- Reincarnated's cosmology content (Wheel / Earth Self / Spirit Guide character / Rift / third-faction)
- Reincarnated's anchor library (the 130 specific entries — they author their own)
- Reincarnated's naming triad player-facing labels (Trial / Mirror / Passage — they choose their own)
- Reincarnated's embodiment vocabulary lookups (humanoid / slime / etc. — they author their own per their genre)
- Reincarnated's visual style register lock (HD-2D pixel — they choose their own per their game)
- Reincarnated's Court framing (they architect their own meta-layer presentation)
- Reincarnated's seasonal anchor library specifics
- Reincarnated's 5 production seasons + Yomi as consumable content (these are demo artifacts; not licensed deliverables)
- The Reincarnated game itself (the loadout web app, the demo, the world-generation work for Engine 2, etc.)

### What they configure at instantiation

- Number of acts per content cycle (Reincarnated locks 3; configurable)
- Level cap (Reincarnated locks 50; configurable)
- Canonical-four element identity (Reincarnated uses fire / water / earth / wind; configurable — the licensee can use any four-element resistance system; the cipher architecture preserves the abstract pair-structure regardless)
- Number of playable classes per content cycle (Reincarnated targets ~5-6 + 3 act-bosses; configurable)
- Geometry palette extensions (Reincarnated's locked palette is broadly genre-correct; licensees can add their own genre-specific geometries)
- Anchor library contents (license provides empty schema; licensee populates)
- Per-archetype validity matrix (license provides framework; licensee configures their permitted combinations)
- LLM provider + prompt templates (license is Anthropic-default but portable)
- Telemetry retention + extension fields (license provides base schema; licensee extends)

---

## Configuration points worth highlighting for the pitch

For the 2026-05-18 pitch specifically, three points are worth being ready to articulate:

### 1. "The engine is genre-agnostic at the architecture layer"

The pitch claims engine licensability to "live-service studios." Likely listener question: *"But this is built for Reincarnated, an isekai ARPG. Does it actually work for non-isekai content?"*

Answer: **the dimensional generation framework is genre-agnostic.** Reincarnated configures it for an ARPG (5 axes producing class kits). A cyberpunk-bodyswap game could configure it with different axes (faction / cybernetic-load / netrunner-rating / etc.) producing class kits in that genre. A mecha-rotation game could configure it with mecha-class axes. **The framework is configurable; the configuration produces the genre.** Reincarnated's configuration is one instance.

### 2. "The cipher architecture protects against LLM lore-bias drift"

Likely listener question: *"How do you keep the LLM from defaulting to fantasy-cliche outputs?"*

Answer: **the cipher architecture (doc 37 § 6).** Canonical-four element labels are hidden from LLM prompts; the LLM works against abstract pair-structure labels; per-content vocabulary is generated against that structure with anti-bias scaffolding. This is a generic pattern. A licensee inherits it and applies it to their own cosmology — preventing LLM-default-fantasy bleed into their own non-fantasy content.

### 3. "The simulation-balance gate is what the procgen-content market doesn't have"

This is the pitch's headline already. Worth being ready to articulate that the simulation engine + convergence balance loop are the load-bearing differentiation. Most procgen content engines produce content that needs hand-balancing; this engine simulates the content against canonical encounters until it converges. **The simulation IS the validation gate.** No hand-balancing required at ship time.

---

## What this enables for the pitch

The pitch one-pager already names the engine claim:

> *"Procedural content engine that generates and simulation-balances a full ARPG season in 41 minutes for under $1."*

This doc strengthens that claim with **layer-separation clarity:**

- The pitch's *engine-only B2B path* now has a defensible answer to *"what specifically are you licensing?"* — the L1 inventory above.
- The pitch's *vertical-integration path* ("Ship the game as flagship demo of the engine; license engine to non-competing genres") has a defensible answer to *"what's the non-competing-genre boundary?"* — anything that swaps L2 cosmology while preserving L1 substrate.
- The pitch's *engine vs game separation* claim ("Either can stand alone") has a defensible answer to *"how can either stand alone if they share infrastructure?"* — the engine stands alone with L1; the game adds L2; both are independent of L3 generation.

The talking-points doc says Matt may field questions like *"Are you building an engine or a game?"* The locked answer: **both, but separable.** This doc makes the separation defensible.

---

## Open questions

These do not block the canonical lock. They surface if licensing work moves forward.

### Q1 — Engine 2 (world generation) licensing layer

The pitch references both Engine 1 (content generation; this doc's primary focus) and Engine 2 (world generation; per file 29 — not started). When Engine 2 lands, the L1 substrate will extend: town/hub architecture, quest generation, dungeon generation, NPC dialogue infrastructure. These will need the same layer-separation analysis. Reincarnated-specific quest content vs engine-generic quest-generation substrate; etc. Out of scope for this doc; surfaces when Engine 2 work begins.

### Q2 — License-shape decisions

Concrete licensing options the pitch one-pager mentions (B2B middleware, recurring license + per-call billing) are commercial decisions not in scope here. This doc supports the *technical* layer-separation that any commercial structure would inherit from. The commercial structure is Matt's call when licensing work moves from pitch-feedback to real conversation.

### Q3 — Multi-tenant infrastructure

The pitch's Phase 2 references "Engine multi-tenant SaaS prototype." Multi-tenant adds infrastructure concerns (per-tenant data isolation, per-tenant LLM cost attribution, per-tenant telemetry, etc.) that are not currently in scope. The current engine is single-project; multi-tenant is roadmap. Surfaces in Phase 2.

### Q4 — Open-source vs proprietary

File 29 mentions *"consider open-source release of engines if they prove robust and useful, post-ship consideration."* If the engine goes open-source, the L1 inventory becomes the OSS scope; L2 + L3 stay proprietary to Reincarnated. The layer-separation supports this option cleanly. Decision-space; not committed.

### Q5 — Per-licensee documentation

If licensing happens, each licensee gets a customized version of this doc (their L2 substituted; their configuration choices articulated). The Reincarnated-as-licensor maintains this doc as the canonical reference; per-licensee docs are derived. Operational concern when licensing happens.

---

## Cross-references

- `cosmology-reincarnated.md` — the L2 project layer this doc separates from
- `style-register.md`, `naming-triad.md`, `embodiment-narrative-layer.md`, `court-of-forms.md`, `enemy-visual-legibility.md` — additional L2 content with L1 substrate components highlighted within
- File 29 — strategic anchor (two-engine architecture; this doc operationalizes Engine 1 contract)
- File 30 — engine current state (what L1 actually does today)
- File 31 — engine future state (what L1 will do post-Track-A)
- File 19 — LLM call map (the L1 LLM infrastructure surface)
- Doc 37 — form-bias structural realignment (the work that surfaced L1 / L2 separation explicitly)
- Engineering disciplines (12; in `reincarnated-engine/design/working-agreement/`) — L1 process substrate
- AGENTS.md — team topology; defines who owns L1 vs L2 work
- `pitch-2026-05-18/one-pager.md` — the engine-licensing claim this doc supports
- `pitch-2026-05-18/talking-points.md` — the talking-point reference Matt walks the listener through

---

## Maintenance protocol

When licensing conversations move forward:

1. Per-licensee version of this doc derived from this canonical reference.
2. L2 substituted per licensee's cosmology.
3. Configuration choices made explicit.
4. Commercial structure (licensing model, pricing, support) added at the licensee-specific level.

When new engine capabilities ship (Track A maturation; Engine 2 future work):

1. L1 inventory extends with the new capability.
2. The L1 / L2 / L3 separation is checked for the new capability — is the new feature generic substrate or project-specific?
3. If genuinely project-specific, it moves to L2 instead.
4. The cross-reference chain is updated.

When future canonical design docs reach decisions that affect engine substrate:

1. Reference this doc.
2. Be explicit about whether the new content is L1 (extending substrate), L2 (extending project cosmology), or L3 (per-content generation).
3. Drift between layers is a Discipline #13 instance and should be flagged.

— gandalf, with Matt's standing approval on the layer-separation pattern (2026-05-15)
