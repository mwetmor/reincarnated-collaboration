# 37 — Form-bias diagnosis and structural realignment

> **STATUS:** DEAD BRANCH (primary framing superseded — substrate-as-cohesion architecture lock 2026-05-19; form-bias is no longer the engine's core problem) — do NOT consult as current truth. See `canonical/00-ground-state.md`

**Status:** Working document, **draft 3**. Draft 2 incorporated jack-ryan Gate 1 findings + Matt's first round of position-locks. Draft 3 adds the catalogue-based form-bias resolution path (Matt's 2026-05-16 design decision) and notes the open questions it empirically grounds or closes.

**Last updated:** 2026-05-16 (draft 3)

**Authors:** Matt (Senior Architect) + knight-rider (Opus orchestrator).

**Gate 1 review:** jack-ryan DESIGN-MODE, findings filed at `agentic_orchestration/qa/findings/2026-05-14-humanoid-bias-design-mode-review.md` — verdict PASS WITH FLAGS, all flags addressed in draft 2.

## What changed from draft 2 (2026-05-16)

- **Catalogue-based resolution path LOCKED** as the primary implementation strategy for the form-bias work (see new section below). Replaces the 3-consumer CV-3D-generation approach (file 29's highest-risk item) as the primary path. CV-3D may still be revisited later but is no longer load-bearing.
- **Score-don't-filter principle** locked for catalogue data. The locked style register (gandalf's domain — see `canonical/story/style-register.md` once authored) becomes a *consumption-time filter*, not a crawl-scope constraint. Pivot flexibility preserved.
- **Three new agents created** to execute the catalogue work: gandalf (story/design steward including style-register decisions), legolas (researcher and catalogue crawler), elrond (data steward and abstraction analyst). See AGENTS.md for topology details.
- **Open questions partially closed by catalogue path** noted in § 10 — specifically § 10.2 #4 (unit of embodiment variation) and § 6.3 (mechanical-signature pool) gain empirical grounding mechanisms via emergent-grouping analysis on catalogue data.

## What changed from draft 1

- **Framing tightened:** "recovery" → "structural realignment / realizing latent intent" throughout. The work is realizing intent that was always present but never structurally enforced — not reverting to a documented prior state. Scope is multi-seam schema migration (ADR-004 territory), not documentation cleanup.
- **Three-layer abstraction — Position C LOCKED:** slot is a functional mechanic at the role layer; slot's name/visual/narrative comes from the embodiment layer. Mechanical contribution identical across embodiments; *which augmentations get equipped* varies.
- **Element cipher — Position (ii) LOCKED:** per-season vocabulary carries its own mechanical signatures; canonical four serve only as the resistance-translation cipher.
- **Smart-loot / spirit-conversion split — LOCKED:** in-season smart loot, post-Phase-0 spirit-conversion for cross-season trading.
- **Body-swap gear rules — LOCKED:** three distinct paths (Trial / doppelganger / death) with three distinct outcomes.
- **STR/DEX/INT explicitly acknowledged** as math-bearing humanoid-bias vector.
- **Engineering-discipline candidate split:** architectural pattern → decisions-log; reviewable process check → engineering-disciplines.md as Discipline #14 candidate.
- **Triggerable Gate-1 questions added** for both discipline candidates.
- **Ailment-damage-signatures dependency surfaced:** the 2026-05-12 deferred design is now load-bearing under Position (ii) for doppelganger-gate resolution.

## How this doc relates to others

This is a **diagnosis and framing** doc. It identifies a structural bias in the engine, frames the appropriate response, captures locked design positions, and surfaces open questions.

- It will produce one or more `decisions-log.md` entries once Matt locks all positions and final dispatch sequencing.
- It surfaces two candidate disciplines (#13, #14) for `engineering-disciplines.md`.
- It identifies cross-seam dispatches that will follow once direction is locked.
- It does NOT supersede `29-design-overview.md` (the strategic anchor) — it sharpens the latent intent within it. Where the two disagree on form, this doc wins; where they disagree on scope, file 29 wins.
- It extends file 32 §11 (body-swap mechanics) with embodiment-aware gear-inheritance rules.
- It re-activates the deferred ailment-damage-signatures design (memory note 2026-05-12) as a load-bearing dependency.

## 1. Origin

In a 2026-05-14 design conversation, Matt observed that the engine has been built with structural humanoid-form bias — biasing content generation toward humanoid embodiments and away from the isekai genre's full breadth, which includes non-humanoid reincarnations (slime, dragon, spider, swarm, construct, etc.).

The bias is **structural, not promptural.** Matt's explicit statement: *"There is nothing wrong with the LLM prompting."* The bias entered via the **categorical axes** the engine generates against — gear, class, wields, wears, weapon, armor, accessory. These axes presuppose humanoid form. When the engine asks the LLM for "a class with a weapon and armor," the LLM cannot produce a non-humanoid answer because the input schema already presupposes form. The LLM is following the engine's axes faithfully; the axes themselves are humanoid-shaped.

**Matt's framing of how the bias entered:** human-paradigm bias that Matt brought into the project as a humanoid, compounded by Claude agents' humanoid-default training. The combination meant every design decision reached for humanoid-readable categorical schemas, and no one was structurally positioned to push back.

## 2. What's form-agnostic vs. humanoid-bound

**Caveats on the inventory:** This is at the **pre-LLM** level only (engine schema and data structures, not post-LLM flavor output). It separates **mechanic** from **naming** (something can be mechanically form-agnostic while carrying humanoid linguistic baggage). The inventory was constructed in conversation and is acknowledged to be **non-exhaustive** — a rocket-led generation-internals sweep is needed for completeness before substantive dispatches go out.

**Mechanically form-agnostic surfaces:**

- Damage resolution math (operates on abstract entities)
- HP / energy mechanics (numbers on entities)
- The geometry palette (16-type — abstract shapes; though the labels `lance`/`cone`/`arc` carry humanoid weapon-semantic gravity)
- The PackProxy entity (already a non-1v1 composite; **precedent for non-humanoid composition** in the codebase)
- The doppelganger gate (operates on entity stats, not form — though see § 6.4 on ailment-damage dependency)
- The cohesion gate (validates LLM output coherence; no inherent humanoid presupposition)

**Humanoid-bound surfaces (load-bearing list, not exhaustive):**

- Gear slots (weapon / armor / accessory presuppose hands, body, extremities)
- Class archetypes (warrior / mage / rogue / hunter — human social/martial roles)
- **Attribute axes (STR / DEX / INT) — *math-bearing*, not just labels.** These flow into `can_equip()` and `stat_requirements` (per 2026-05-09 decisions-log entry). An entity embodied as a swarm or crystalline construct has no natural STR. **Under structural realignment these survive as abstract power dimensions divorced from physical interpretation** — the labels stay (for engine math, gear gating, balance) but the LLM-visible narrative reframes them per-embodiment.
- Trait architecture (file 33: per-class intrinsic trait pool is humanoid-archetype-bound)
- Loadout UI (anatomical slot layout)
- Spirit Guide kit-composition framing (presupposes "kit of skills," not e.g. "body-with-properties")
- "Class" as the primary identity unit
- The canonical four elements (fire / water / earth / wind — see § 6)
- The skill verb grammar in flavor output (post-LLM, but seeded by humanoid-bound taxonomy)
- The D1 element-name pool and its rubric (see § 7)

This list will likely grow once a rocket-led generation-internals sweep runs.

## 3. The bias is structural realignment, not pivot

The framing this conversation arrived at: this is **structural realignment to realize latent design intent**, not a new design direction. The latent intent existed from project inception; what's needed is the structural enforcement that was never put in place.

Three pieces of evidence for the latent intent:

1. **The project is literally named "Reincarnated."** The cross-form transition is in the name. Reincarnation in world traditions (Hindu / Buddhist samsara, Egyptian afterlife transit, Native American transformation) spans humans, animals, devas, asuras, ghosts, hells — never just humanoid.
2. **The Spirit Guide subsystem carries mythic non-humanoid valence in its label.** Across world mythology, spirit guides are predominantly animal or otherwise non-humanoid: totem animals, Norse fylgja, Japanese kitsune/tanuki, Odin's ravens and wolves, ancestor spirits in animal forms. Naming the module "Spirit Guide" was already signaling the intent.
3. **The originating game premise was the isekai weekly-reincarnation trope** *("this week I was reincarnated as a slime")*. That genre's defining feature is the breadth of forms one can reincarnate into. Building the engine humanoid-only contradicts the trope at its core.

**What happened during implementation:** the categorical axes drifted humanoid because the implementers (human Matt + Claude collaborators, all trained on humanoid-default content) reached for humanoid-readable schemas (gear/class/wields/wears). **The latent design intent never gained structural enforcement; the drift was unobstructed.** The intent existed in conversation and naming, but not in code, schema, or process gates.

**Scope of the realignment (jack-ryan WARN 1 framing):** This work is a **multi-seam schema migration** (ADR-004 territory, MIGRATION.md required), NOT documentation cleanup. The gear-slot rename, embodiment-axis addition, attribute-axis reframing, and element-cipher refactor all touch:

- The JSON export contract between engine and demos
- The telemetry schema (`gear`, `gear_instances`, `gear_traits` tables)
- The loadout display contract
- Possibly the season manifest version

Implementers picking up dispatches against this doc should treat the work as **structural realignment requiring coordinated migration**, not local renaming. "Realizing latent intent" captures the spirit; "multi-seam schema migration" captures the operational reality.

## 4. Three-layer abstraction — **Position C LOCKED**

Three layers come apart cleanly:

| Layer | What it is | Status in engine |
|---|---|---|
| **Functional role** | What an entity does mechanically (long-range projection + defensive augmentation = hunter-shaped role) | Form-agnostic at the mechanic layer (energy type, range profile, role orientation, etc.) |
| **Embodiment** | How an entity physically manifests (humanoid / slime / swarm / construct / beast / plant / crystalline / cloud / etc.) | **Missing — needs to be added as an explicit axis** |
| **Narrative surface** | How the entity is described to the player | Derives from embodiment × role |

### Locked position on slot ownership (jack-ryan WARN 2)

**Position C: Slot-as-functional-mechanic + embodiment-as-narrative-skin.** Locked 2026-05-14.

The slot is a FUNCTIONAL mechanic at the **role** layer (defensive augmentation, offensive augmentation, accessory augmentation). The slot's NAME / VISUAL / NARRATIVE comes from the **embodiment** layer:

- Humanoid defensive slot → "chest armor"
- Slime defensive slot → "viscosity layer"
- Swarm defensive slot → "carapace ratio among colony members"
- Crystalline construct defensive slot → "resonance buffer"

**Mechanical contribution is identical across embodiments.** Embodiment is mechanically meaningful via *which augmentations get equipped* (a swarm hunter equips different augmentations than a humanoid hunter), but the *slot structure itself* is shared. Cross-embodiment gear is a universal mechanical item with per-embodiment display.

**Trade-off accepted:** cannot express embodiment-level structural constraints (e.g., "slimes have no offensive slot at all because slime nature is purely defensive"). If a future design wants such constraints, they will live as role-level requirements ("offensive role requires offensive augmentation slot") that an embodiment-class pair either supports or doesn't.

### Proposed renames

- "Gear" → "augmentation" (or "investiture") — a base embodiment's capabilities are shaped by what augments it
- "Embodiment" added as a new explicit axis at the foundation/class level, peer to element

These renames will land via a multi-seam schema migration (rocket + star-lord + drax coordinated). MIGRATION.md required.

## 5. The Spirit Guide framing

Matt's vision (verbatim from conversation): a non-humanoid entity, **between transparent and translucent**, **possibly humanoid, possibly animal, possibly mixed**, **possibly from the future**.

Knight-rider's reading (Matt confirmed):

- **Translucence = a different ontological class** from playable embodiments. Playable forms are solid/opaque; spirit guide is partial-presence. A different visual grammar drax can implement (opacity gradient as ontology signal). *Note: this commits a presentation-layer rendering decision; drax should be consulted before it becomes architectural.*
- **Form-ambiguity** = the spirit guide doesn't need to commit to an embodiment. It's free to shift, suggest, echo.
- **"From the future"** is the load-bearing temporal piece. A future-form guide carries **foresight, not memory.** It guides because *it has already been you, further along.*
- **Translucence reads as pre-arrival**, not ghostly-past.
- **Form-ambiguity reads as becoming**, not uncertainty.

### Diegetic unification

The spirit guide is the in-fiction expression of multiple currently-disconnected systems:

- The marginal-value analyzer (`simulation/spirit_guide/`)
- The form library / Earth Self persistence bridge
- The presentation surface that introduces embodiments to the player
- Possibly the bridge between Phase 0 and post-Phase-0 game states

### Phase 0 / post-Phase 0 connection

If the spirit guide is from a future game state — specifically, the post-Phase-0 Earth meta-layer — then it serves as the in-fiction representative of where the project itself is going, not just where the player is going this season. Phase 0 doesn't need to *resolve* the spirit guide's identity; its temporal-otherness is appropriate for a being whose full context is post-Phase-0.

### Form library reframing

- **Past-framing** (rejected): library bounded by what the guide has been
- **Future-framing** (preferred): library is *what you can become* — possibly larger than what the guide has been

The future-framing aligns more naturally with the gacha-accumulation pattern in the Earth meta-layer notes.

## 6. Canonical-four element cipher architecture

Matt's load-bearing statement: *"The only purpose of the four elements is to provide a canonical pairing for the Earth realm so that elemental resistances can decrypt the key pairs. The four canonical elements must be blocked from view of all LLM calls so that more forms can converge/coalesce."*

### 6.1 The architecture

**Internal layer (hidden from LLM):** the canonical four (fire / water / earth / wind) used purely as a **fixed-size resistance-cipher key**. NOT as mechanical-signature archetypes (see § 6.2 locked position).

**Abstract pair-structure layer (LLM-visible):** two opposition labels — provisional names *Primary Opposition* and *Secondary Opposition* — with positions {first, second} in each. The engine maintains the hidden mapping (Primary-1 ↔ fire, Primary-2 ↔ water, Secondary-1 ↔ earth, Secondary-2 ↔ wind).

**Per-season seasonal vocabulary (LLM-generated):** for each season's setting, the LLM generates setting-native vocabulary at each position. Examples:

- Deep-sea cosmology: Primary *pressure ↔ vacuum*; Secondary *bioluminescence ↔ decay*
- Cosmic setting: Primary *void ↔ matter*; Secondary *radiation ↔ entropy*
- Music-spirit world: Primary *harmony ↔ dissonance*; Secondary *melody ↔ rhythm*

### 6.2 Mechanical-signature treatment — **Position (ii) LOCKED**

The canonical four labels bundle **three** different things, with different treatment for each:

1. **Specific labels** (`fire`/`water`/`earth`/`wind`) — **Hide from LLM.**
2. **Pair structure** (which axis opposes which) — **Expose via the abstract pair-structure layer.**
3. **Mechanical properties** — **Position (ii) LOCKED:** abstracted away from the canonical four. Per-season vocabulary carries its own mechanical signatures.

**What Position (ii) means concretely:** Pressure has its own mechanical signature (e.g., crushing burst — high impact, short duration, area-permeating). Internally tagged "fire" purely so water-resistance still applies (cross-season cipher works). But pressure's mechanical *feel* is genuinely different from any other season's fire-tagged axis. The cipher's job is **narrowed** from "labels + mechanical archetypes + resistance" to "resistance translation only."

**Rationale:** Matt's stated intent ("so that more forms can converge/coalesce") requires seasonal vocabulary to mean something *mechanically* different, not just rename. Position (i) (cosmetic-only over fixed mechanics) would not achieve the bias removal — pressure would just BE fire.

### 6.3 Open question following from Position (ii) — HIGH-STAKES

**OPEN:** What is the mechanical-signature pool, and is it shared across seasons or per-season?

- **Shared pool option:** e.g., a fixed pool of ~16 mechanical signatures (DoT, burst, slow, vampiric, propagating, stunning, etc.); each season picks four (one per axis). Pro: balance work is bounded; doppelganger gate has a finite set of mirror cases. Con: per-season feel may be less distinct if the underlying signature pool is shared.
- **Per-season generation option:** each season generates its own four mechanical signatures from scratch. Pro: maximum variety; cosmology-native mechanics. Con: balance work scales with season count; doppelganger gate must validate per-season.

**Hybrid possible:** a base shared pool that per-season generation can extend or parameterize. Resolution requires prototyping more than further conceptual work.

### 6.4 Ailment-damage-signatures dependency — **RE-ACTIVATED**

Under Position (ii), pure-control mechanical signatures (slow, stun, root, fear) would cause stalemate mirror matches in the doppelganger gate. Matt's resolution: **every ailment must have at least some damage component** (Matt position, 2026-05-14).

This **re-activates a 2026-05-12 deferred design item** (per Matt's memory log):

> *Thematic ailment damage signatures — secondary damage signatures on control ailments themed per element (wind cut+bleed, earth thorny root, water cold-burn; fire already has burn DoT); flavor-tier magnitudes (~5-10% of originating skill); would give control archetypes meaningful mirror-match damage and let per-fight variance dial back from ±25% to ±15%. **DEFERRED** because KI-B6-1 was resolved via ±25% variance; revisit after B14.5 lands.*

The deferral reason no longer holds. KI-B6-1 was about *one* failure mode; Position (ii) introduces a *new* one (per-season pure-control signatures → doppelganger stalemates). **The deferred ailment-damage-signatures work becomes a load-bearing dependency of the cipher architecture**, not just a build-diversity nice-to-have.

When this work resumes, the spec is largely in place from the 2026-05-12 design notes; the only adjustment is that magnitudes may need to scale up if ±15% variance proves insufficient for mirror-match resolution under Position (ii).

### 6.5 Two pieces still requiring prototyping

These require **prototyping, not more conceptual work** (Matt's explicit position):

- **Residual bias.** Even told *"two opposition pairs for a deep-sea cosmology, do not echo Earth-realm classical elements,"* the LLM may still reach for water/air/fire/earth analogs because those patterns are deeply trained in. Reliability of anti-bias scaffolding under generation drift (across thousands of calls per season) is unknown without empirical test.
- **Pair-structure exposure shape.** Does the LLM see both pairs simultaneously (and generate four axes at once), or one pair at a time (independently)? Affects whether cross-pair mechanical interactions (e.g., a fire-wind hybrid analog) can be expressed in the seasonal vocabulary. Needs to be specified before prompt design.

## 7. D1 element-name pool — a meta-instance of the same bias

The D1 element-name pool work (per Matt's memory notes: 81 allow-list / 40 eligible / 35 quarantine across 156 entries) was assembled against rubric criteria — `visualizable`, `fantasy-heroic`, `genre-precedent`, proposed `vocabulary_commonness` — that are themselves implicitly Earth-realm-humanoid-fantasy-reader-perspective. Words like bioluminescence, vacuum, pressure, decay, entropy would not score well on those criteria, yet are exactly right for non-humanoid cosmologies.

**Three levels of drift:**

1. **Pool contents** — humanoid-fantasy selection bias in what was proposed at all
2. **Status assignments** (allow / eligible / quarantine) — humanoid-readable judgment
3. **The rubric itself** (`d1_total` and its sub-properties) — encodes humanoid-fantasy-reader perspective

All three drifted without anyone naming the design intent that was being optimized for. This is a second independent instance of the **implicit-pillar drift** pattern (§ 9.1). The pattern is no longer a hypothesis; it is empirical.

**Scope implication for the rocket dispatch eventually following:** The D1 reconsideration is **not** "rebuild the pool with non-humanoid words added." The curated-pool approach itself may not survive the architecture shift. The work is: *decide whether a curated pool is the right tool at all under the new architecture, or whether the rubric-and-pool gets replaced by LLM-output validation against quality criteria.* This is a meaningfully larger piece of work than originally scoped.

## 8. Body-swap gear mechanics under embodiment-as-axis — **LOCKED**

The introduction of embodiment as a new axis interacts with the existing locked body-swap design (file 32 §11). Matt's positions, 2026-05-14.

### 8.1 Smart loot / spirit-conversion split

- **In-season: 100% smart loot.** Drops are pre-tailored to current embodiment. Gear never travels cross-embodiment within a season. Inventory is mono-embodiment.
- **Post-Phase-0 (Earth meta-layer): spirit-conversion engine.** Cross-season trading allows conversion of gear across embodiments. Out of Phase 0 scope; lives in the Earth meta-layer feature set.

**Rationale:** defers the harder mechanic (conversion engine) to the phase where cross-embodiment persistence is already the central problem. Phase 0 stays simple.

### 8.2 Three body-swap paths — gear rules

| Path | Trigger | Gear outcome | Level | Class pool |
|---|---|---|---|---|
| **Doppelganger victory** | Voluntary (Trial-refuse) | Keep yours + gain doppelganger's | Preserved | Preserved (file 32 §11) |
| **Trial body-swap** | Voluntary (Trial-accept) | Lose yours + gain boss's equipped | Preserved | −1 |
| **Death body-swap** | Involuntary (HP→0) | Lose yours + start with L1 default | **Reset to L1** | −1 |

**Design coherence:** the three paths form a meaningful risk/reward gradient. Doppelganger = "pure accumulation if you survive a hard mirror match." Trial body-swap = "transformation, no progress loss." Death = "real failure penalty."

**Smart-loot invariant preserved:** boss's equipped gear is by definition embodiment-appropriate (the boss IS that embodiment), so body-swap inheritance just works. Doppelganger gear is by definition embodiment-matched (the doppelganger is YOU in your current body). No conversion engine needed at the inheritance moment within a season.

### 8.3 Sub-question — OPEN (low-priority follow-on)

**What is the default L1 gear loadout?** Under smart-loot, it must fit the new body's embodiment — likely per-class-per-embodiment, generated alongside the class at season-build time. Rocket dispatch territory when this gets work. Not blocking the broader design work.

## Catalogue-based form-bias resolution path — **LOCKED 2026-05-16**

(Inserted in draft 3 without renumbering subsequent sections to preserve cross-references. This section sits between § 8 and § 9 in reading order.)

### The decision

Matt's design decision, 2026-05-16: the 3-consumer CV-3D-generation approach (file 29's highest-risk item) is **replaced as the primary path** by **catalogue-based mapping** for both 2D and 3D content. The engine's embodiment vocabulary will be derived empirically from what catalogues actually contain, not from procedural 3D generation that may not work.

CV-3D generation may still be revisited as a long-term option, but is no longer load-bearing for the project's near-term viability.

### Why this works

- **Validates against demo1's already-working pattern.** Demo1 successfully maps JSON metadata to pre-packaged 2D sprites. Extending the pattern to a curated catalogue is incremental, not novel.
- **Retires the highest-risk item** in the project (per file 29's risk register).
- **Makes form-bias resolution empirical.** Instead of asking *"what forms should the game support?"*, the engine asks *"what forms can we actually deliver via the catalogue?"*. Embodiment categories emerge from real data, not from designer aspiration.
- **Constraints inform the design, not the other way around.** The catalogue's available forms define what's deliverable; the engine adapts to what exists.

### The structure

**Crawl wide (Legolas Mode B):** systematic catalogue crawl across all major 2D sprite libraries + Unity Asset Store + opengameart.org + itch.io + similar. Per-asset metadata captured: `asset_id`, `source`, `url`, `name`, `category`, `dimensionality` (2d/3d), `style_register`, `style_tags`, `decomposition` (monolithic/decomposed for character/enemy), `file_format`, `license`, `cost`, `crawl_date`. See `~/.claude/agents/legolas.md` Mode B specification.

**Curate (Elrond):** raw extraction structured into queryable form. Catalogue database at `agentic_orchestration/research/curated/catalogue.db` (or similar — Elrond's call). Style-register tagging as curated dimension. Cross-cutting joins to engine telemetry available via SQL ATTACH for analytical work.

**Analyze for emergent groupings (Elrond):** abstraction analysis on the catalogue data. Cluster on visual style, functional role, dimensional category, creator/source patterns. Test whether emergent groupings hold across both 2D and 3D variants — if yes, the abstraction is genuinely about form/role, not medium. If no, two separate abstraction layers needed. Document negative results.

**Use as engine's embodiment vocabulary (rocket, eventually):** once abstraction groupings stabilize, they become the engine's embodiment-axis values. This is the empirical resolution of § 10.2 open #4 (*Unit of embodiment variation*) — the unit is whatever the catalogue's emergent groupings produce.

### Quality gates

- **~25% seasonal failure rate is acceptable.** Generated seasons that can't find sufficient catalogue cohesion get discarded. This is a quality floor, not a compromise.
- **One-week cohesion floor is sufficient.** Players experience one season at a time; approximate visual cohesion over a week is enough. We don't need exact form matches; we need mood/theme cohesion.
- **Three-track viability gate** (per AGENTS.md) gates full catalogue crawls. No source receives full crawl effort without passing structural (Elrond) + wiring (Drax) + design (Gandalf) sample review.

### Score-don't-filter principle

The locked style register (gandalf's domain, captured at `canonical/story/style-register.md` once authored) becomes a **consumption-time filter** applied by the engine and design pipeline — NOT a crawl-scope constraint. Legolas crawls widely across style registers; Elrond tags by register; consumption filters by current locked register. If the project's needs shift (engine, story, design, or experience), the catalogue already contains the data and the pivot is a filter change, not a re-crawl.

### Implications for the locked positions in § 4 and § 6

The catalogue path is **compatible with** the locked positions (Position C, Position ii) but **does not replace them**:

- **Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin)** — catalogue assets get tagged by embodiment-narrative-skin (humanoid, slime, swarm, etc.) and by functional-role suitability. Same mechanical slot vocabulary; different visual manifestation per embodiment.
- **Position ii (per-season vocabulary carries own mechanical signatures; cipher = resistance-translation only)** — catalogue's emergent abstractions inform what mechanical signatures CAN visually express. The cipher continues to handle cross-season resistance translation; catalogue determines what's visually deliverable per signature.

### Structural enforcement of Discipline #13

The catalogue IS the structural constraint. It cannot drift in the way a conversational pillar can. Embodiment categories are emergent properties of real data, not negotiated agreements. This is Discipline #13 (implicit-pillar drift) being structurally enforced by the architecture, not just monitored through process.

### Open questions this path raises (new)

- **Style-register decision** — gandalf authors `canonical/story/style-register.md` during Phase-1 onboarding. Locked register becomes the consumption-time filter. Pivot path: revise the lock, re-filter catalogue.
- **Catalogue source priority** — initial Tier-1 sources in `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`. Order of crawl after viability-gate passes is Elrond's sequencing call.
- **Cross-source cohesion within a season** — when a generated season pulls assets from multiple catalogue sources, does the visual consistency hold? Empirical question; arises during initial generation passes after catalogue is populated.

### Status

Active. Implementation gated on: gandalf style-register decision (Phase-1 onboarding) → legolas first catalogue source sample → three-track viability gate → green-lit full crawls → elrond curation → abstraction analysis → rocket integration into engine's embodiment vocabulary.

Realistic timeline: catalogue work runs in parallel with B-series engine work over the next 6-12 weeks. Abstraction groupings stabilize as the catalogue fills; engine integration follows once the abstraction layer is validated.

## 9. Engineering-discipline candidates

Two candidate patterns surfaced from this conversation. **Per jack-ryan INFO 5:** the originally-proposed Candidate B is split between architectural pattern (decisions-log) and reviewable process check (engineering-disciplines).

### 9.1 Implicit-pillar drift — Discipline #13 candidate

**Pattern:** Design intent that isn't structurally enforced drifts during implementation. Implementers reach for default schemas; the latent intent has no representation in code or process; drift goes unobstructed because there's nothing to alarm against.

**Counter:** Pillars the project considers load-bearing must be **structurally enforced** — by explicit schema constraints, explicit tests, explicit acceptance-criterion items on dispatches, or explicit decisions-log entries. *"We agreed in conversation"* is not structural enforcement.

**Triggerable Gate-1 question (jack-ryan INFO 6):** *"Is the design pillar this work depends on documented in decisions-log as a structural requirement? If not, the pillar must be added BEFORE coding against it."* Reviewer applies at every dispatch authoring.

**Instances observed (empirical, not hypothetical):**

- Spirit-swap as non-humanoid pillar → drifted humanoid via gear/class axes
- Form-agnosticism implicit in project name → drifted humanoid via implementation defaults
- Canonical four = "Earth-realm cipher only" → leaked into seasonal flavor surfaces
- D1 rubric = "Earth-realm humanoid-fantasy element naming" → never named, drifted unexamined

**Status:** Ready for engineering-disciplines.md once Matt approves. Likely numbered #13.

### 9.2 Internal-vs-generative schema separation — **SPLIT** per jack-ryan INFO 5

Originally proposed as a single discipline. Jack-ryan flagged that it conflated an architectural pattern with a process check. **Split:**

#### 9.2a — Architectural pattern (decisions-log entry, not a discipline)

**Pattern:** Mechanical schema needed for engine correctness should be hidden from the generative layer. The generative layer sees per-instance vocabulary (which it generates or selects); the engine resolves the mapping between per-instance vocabulary and mechanical schema internally.

**Application:** the canonical-four cipher architecture (§ 6) is the first concrete instance of this pattern. Future work that introduces LLM-visible mechanical labels should be evaluated against this pattern.

**Lands in:** `decisions-log.md` as a recorded architectural pattern when doc 37 locks.

#### 9.2b — Discipline #14 candidate (engineering-disciplines.md)

**Reviewable check:** When introducing or modifying any LLM-visible category, the prompt-construction code must not expose: (a) canonical-four labels, (b) class-archetype labels, (c) mechanical property names (DoT, defense, etc.), (d) attribute axis labels (STR/DEX/INT). Per-instance vocabulary only.

**Triggerable Gate-1 question:** *"Does this LLM call template expose internal mechanical labels (canonical four, archetype names, mechanical signatures, attribute axes)? If yes, refactor to expose only per-instance vocabulary."* Reviewer applies at every star-lord dispatch and any rocket dispatch touching LLM prompts.

**Status:** Candidate for engineering-disciplines.md #14 once Matt approves.

## 10. Open questions (consolidated and prioritized)

### 10.1 High-stakes — affect dispatch scoping

1. **Mechanical-signature pool: shared, per-season, or hybrid?** (§ 6.3) Determines balance scope and doppelganger-gate work. **Empirical grounding mechanism added 2026-05-16:** catalogue analysis can inform which mechanical signatures have viable visual representation across available assets. The pool's bounds are partly constrained by what the catalogue can express visually.
2. **Pair-structure exposure shape** (§ 6.5) — does the LLM see both pairs at once or one at a time? Affects prompt design.
3. **Residual LLM bias under hidden canonical four** (§ 6.5) — empirical, requires prototyping.

### 10.2 Medium-stakes — affect implementation but not architecture

4. **Unit of embodiment variation.** Per-season (whole roster is slime-variants) / per-class within season (mixed roster) / per-spirit in form library / hybrid. Cascades into generation, simulation, presentation differently. **Partially closed by catalogue path (2026-05-16):** the unit is whatever the catalogue's emergent abstraction groupings produce. Final resolution after Elrond's abstraction analysis completes.
5. **Diegetic vs ambient spirit guide.** Does the player *interact with* the spirit guide as a character, or is it ambient/UI?
6. **Form library ownership.** Spirit guide ("what you can become") or Earth Self ("what you have been")?

### 10.3 Low-stakes follow-on — not blocking

7. **Default L1 gear loadout** (§ 8.3) — needs spec before death-body-swap can be implemented.
8. **Gear → augmentation rename + embodiment axis as a new explicit pillar** (§ 4) — proposed, awaiting explicit confirmation. Probably yes given Position C is locked.

## 11. Cross-seam impact

| Seam | Impact | Initial dispatch shape |
|---|---|---|
| **Rocket** (`generation/`, `element/`, `anchor/`, `foundation/`) | Foundation generation produces per-season vocabulary for abstract pair-structure layer; canonical four hidden in LLM calls; D1 pool reconsideration is large (pool approach may not survive); embodiment axis added; per-class-per-embodiment L1 starter-gear generation; ailment-damage-signatures work re-activated; mechanical-signature pool design | Multiple coordinated dispatches — pair-structure layer first, then D1, then embodiment axis, then mechanical-signature pool, then L1 starter gear |
| **Star-lord** (LLM / prompts / telemetry) | All LLM prompt-construction paths need a filter stripping canonical-four references and other internal mechanical labels (Discipline #14 enforcement); anti-bias scaffolding patterns for per-season vocabulary generation; telemetry schema may need fields for mechanical-signature tags | LLM prompt-leak audit dispatch + anti-bias scaffolding work |
| **Gamora** (`simulation/`) | Doppelganger gate validation under Position (ii) per-season mechanical signatures; ailment-damage-signatures implementation; PackProxy precedent informs eventual non-1v1 embodiment composition | Doppelganger-mode validation dispatch when ailment-damage work resumes |
| **Drax** (loadout, demo) | Display-surface sweep — never show canonical four to the player; loadout UI restructuring once augmentation/embodiment shift lands; translucence as ontological visual signal for spirit-guide presentation; inventory transition UI for body-swap paths | Display-leak audit dispatch + body-swap inventory transition work + later embodiment-visualization work |

**ADR-004 trigger:** This work spans rocket, star-lord, gamora, and drax simultaneously. **MIGRATION.md is required** for the gear-slot rename + embodiment-axis addition + canonical-four hiding + attribute-axis reframing. Single coordinated migration document covering all four seams. Knight-rider authors when direction is fully locked.

## 12. Status and next steps

**Current status:** Draft 3 — catalogue-based resolution path locked as primary implementation strategy (2026-05-16). Earlier locks from draft 2 retained (Position C, Position (ii), smart-loot split, body-swap rules, ailment-damage re-activation). Several open questions remain (§ 10) but now have empirical grounding mechanisms via the catalogue path.

**Next steps (in order):**

1. **Gandalf Phase-1 onboarding** (in progress) — produces preliminary bullet-point deliverable across Overall Game Design / Player Journey / Storytelling-Dramatic Themes. Identifies knowledge gaps for Legolas Phase-2 commission. Authors `canonical/story/style-register.md` style-register decision.
2. **Legolas Mode-A research** commissioned by Gandalf — fills post-training-cutoff knowledge gaps. Findings to `research/knowledge/`.
3. **Gandalf Phase-2 deliverable** — updated bullet points incorporating Legolas research. Authors `canonical/story/gandalf-design-lineage.md`.
4. **Elrond data-architecture audit** — comprehensive baseline at `research/curated/data-architecture-audit-<date>.md`. Grounds all subsequent data work.
5. **Legolas Mode-B catalogue sample** — first catalogue source (Tier-1 priority per `research/knowledge/asset-catalogues/2026-05-16-...`). Three-track viability gate review.
6. **Green-lit full crawls** roll out across Tier-1 catalogue sources. Elrond curates raw extractions into catalogue DB.
7. **Elrond abstraction analysis** on populated catalogue. Emergent groupings tested for 2D/3D coherence.
8. **Rocket integration** of catalogue-derived embodiment vocabulary into engine generation.
9. **Decisions-log entries** for the locked positions in this doc + the internal-vs-generative architectural pattern (§ 9.2a). Knight-rider drafts; jack-ryan reviews.
10. **Engineering-disciplines.md** updated with Discipline #13 + #14. Jack-ryan reviews.
11. **MIGRATION.md** authored covering all four seams' schema changes (gear-slot rename, embodiment-axis addition, canonical-four hiding, attribute-axis reframing).
12. **Per-seam dispatches** authored in sequence. **Implementation begins** — but only after open questions (§ 10.1) are resolved enough to scope the work properly.

**Time horizon:** This is not fast-turnaround work. The diagnosis is large, the architecture is substantial, the catalogue work compounds the timeline (multi-week crawl + curation + abstraction analysis). Realistic estimate: 6-12 weeks of focused effort, interleaved with ongoing B-series engine work. The B-series work itself is **not blocked** by this — sequential rooms (B10 V2), swarm calibration (B10.4), and other engine maturation continues independently.
