# Hypothesis Flow + Pattern Library Architecture

> **STATUS:** CANONICAL (load-bearing as of 2026-06-06 per Matt ratification as cemented future-state architecture; promoted from CURRENT 2026-06-01 to CANONICAL 2026-06-06 following multi-iteration design call confirming this doc as the source-of-truth for cell schema + flag enum + pattern-library Phase A-E roadmap + serving as architectural anchor for cosmograph build). **Composes with** `canonical/story/2026-06-06-atomic-substrate-registry.md` (Layer 0 + Layer 0.5 + derivation chains + Naming Layer N1-N4 stack — the upstream substrate this doc's § 3 referenced but did not enumerate). Together they constitute the cemented future-state architecture for engine + cosmograph: Layer 0 + 0.5 (atomic-substrate-registry) + Layer 1 + 1.5 + 2 + 3 (this doc § 3) + Naming Layer N1-N4 (atomic-substrate-registry § 5). **The 55 open questions remain operational refinement work; the foundational architecture is CEMENTED.** Pre-CANONICAL prior status: CURRENT (graduated from PLACEHOLDER to CURRENT canon 2026-06-01 per Matt close-out authorization following 8 refinement iterations).
>
> **2026-06-06 amendment (Matt ratification — cemented future-state + atomic-substrate-registry companion):**
> - STATUS promoted from CURRENT → CANONICAL
> - Companion doc added: `canonical/story/2026-06-06-atomic-substrate-registry.md` (enumerates Layer 0 atomic primitives + Layer 0.5 combinatory operators that this doc's § 3.2 referenced as "designer-writes substrate" but did not itemize)
> - Key Layer 0 additions from atomic-substrate-registry NOT enumerated in this doc's § 3-4:
>   * Race primitives + racial trait primitives (NEW substrate family per Matt 2026-06-06)
>   * Skill-tree-position primitives (T1/T2/T3/T4 capstone × chain-position × node-depth)
>   * Scaling-pattern-per-tier primitives (additive / additive+multiplicative / multiplicative / transformative)
>   * Chain architecture primitives (3-chain vs 4-chain)
>   * Investment-scaling-pattern primitives (6 patterns per canonical 51)
>   * Off-hand item parallel substrate
>   * ~200 weapon-form token primitives (this doc § 3.2 used 6-enum `weapon_type_family` aggregation)
>   * Per-primary flavor-pool registry
>   * Seasonal-substrate-rotation operator (single-axis default + multi-axis escape hatch)
>   * Naming Layer N1-N4 stack (separate downstream identity-naming family; LLM-derived content lives here, NOT in engine substrate)
> - Derivation chains made explicit (Depth 2 textual): `kit_architecture` is DERIVED from element-count (was treated as peer substrate field); `bc_axis_signature` + `weapon_type_family` are emergent compositions from Layer 0 atomic primitives
> - Cosmograph implications: Layer 0 atoms = primitive stars; Layer 0.5 operators = axis-pair edges; Layer 1 derived = labeled overlays; Naming Layer = constellation side-panel content; constellations CROSS LAYERS
>
> **Refinement iteration history (now historical record):** Iter 1: gauntlet provisional + manifestation Phase 1/2 + retroactive + WS1A.4 + three-layer validation. Iter 2: P4 → creation-moment-memorability. Iter 3: 7 mechanism families → three-layer treatment (Layer 1 P1-P5 / Layer 2 mechanism-structural / Layer 3 observational); "Family B gap" framing retired. **Iter 4: multi-axis experiential architecture** per Matt 2026-06-01 observation that 6 primary archetype labels (Bossing / Speedfarm / Push / Generalist / Leveling / League Starter) aren't a flat enum — they decompose into orthogonal axes (Progression-Stage / Target-Pattern / Depth-vs-Breadth) plus additional axes (Mode / Activity-Format / Loot-Focus / Maxroll 5-axis). Axis-type taxonomy (Identity / Viability / Mode / Sub) treats each axis differently; cell shape framework (Specialized / Hybrid / Generalist / Anti-specialization) declares intended profile shape; Leveling-as-viability-axis hypothesis per Reincarnated 50-level + 85%-leveling-only structure (pending playtest validation); genre-relative LE-to-D3 moderate specialization positioning; mutual exclusivity preference framed as substrate-led empirically validated, not pre-imposed. **Iter 5: pipeline placement decision LOCKED** — Phase 5+ LLM naming (per-skill flavor judgment + skill naming + cohesion clustering + Wave A/B naming) fires AFTER Pareto reduction (Option A; on ~30 kits not ~650); cost-efficient (~$1.50-4.50/cycle vs $30-90); cohesion judge n=30 sufficient for meaningful clustering (~3-5 emergent factions); Option B (pre-Pareto naming with faction-aware reduction) deferred to future refinement gated on playtest evidence of natural-faction-loss; substrate-led discipline composes with gauntlet provisional recognition (don't compound provisionality without empirical validation). **Iter 6: Mode axis REMOVED** per Matt observation that Hardcore/Softcore would not differentiate player experience across kits — all kits available within both modes. Mode is player-session-level choice, not kit-architecture-level property. HC-viability (if HC mode added later) becomes higher Survivability threshold within existing Viability axis treatment, NOT a separate axis. Removed: `mode_axis` field; MODE_HARDCORE/MODE_SOFTCORE/MODE_EITHER flags; AXIS_TYPE_MODE classification. Added: `VIABILITY_HC_SURVIVABILITY_PASS` conditional gate within Viability axis flags. **Iter 7: multi-source hypothesis generation across launch lifecycle** — Matt observation that methodology should include real player game telemetry + community-derived telemetry (Reincarnated-hosted community sites + third-party community sites + blogs + social posts) as engine learnings. § 2.4 NEW sub-section covers availability-gated hypothesis source scaling across launch lifecycle (pre-launch → alpha → soft-launch → full launch → mature ecosystem); real-player-telemetry methodology (Stage 1 input expanded; star-lord seam composition); community-derived telemetry ingest architecture (3 channels: Reincarnated-hosted + third-party + distributed); substrate-led discipline applied fractally at post-launch player-experience layer; pre-launch architectural decisions surfaced (telemetry event set / retention policy / community site timing). **Iter 8: endgame content type architecture — player-input procedural map generation (Matt 2026-06-01 PROPOSED)** — Matt observation that Depth-vs-Breadth axis requires multiple endgame content types to be meaningful, plus Matt elegant two-bird-one-stone proposal: extend existing planned procedural map generation with player input modifiers + unlimited scaling via input selection (similar to PoE 1/2 maps but ≤3 multiplicative layers per coupling architecture discipline). Single content design activates 5+ axes (Depth-vs-Breadth + Activity-Format + Target-Pattern + Loot-Focus + Push tier-scaling). Uber-Bosses emerge from boss-input maps (no separate content type needed); infinite-tower equivalent via tier-scaling progression (no separate content type needed). Composes with cascade architecture (anti-faction inputs) + ≤3 layer coupling discipline (LE Monolith pattern target). § 1.8.7 NEW sub-sub-section + § 3.5 Activity-Format axis values stabilized + § 4.1 Activity-Format flags (9 input-category flags) + § 8h 7 new open questions. ARCHITECTURAL COMMITMENT STATUS: PROPOSED PLAYTEST-PENDING (Matt 2026-06-01 game-design proposal; not yet canonically committed; warrant for separate canonical recognition record per Q54). Synthesizes 2026-05-29 ARPG community research sprint output + designer-writes-substrate / player-names-experience principle + 5-property substrate framework + 7-mechanism-family taxonomy + experiential cascade architecture recognition + Matt 2026-05-31 hypothesis-flow methodology articulation + 2026-06-01 refinements. **Not a commitment.** Document is the substrate for ongoing Pattern B refinement conversation that produces the committed architecture.

**Date:** 2026-05-31
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-31 verbatim request for "placeholder canonical hypothesis flow, sequencing and mathematical cell/flag document which I can read and we can refine together before we commit to anything"
**Companion read-required artifacts:**
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle (CURRENT canon)
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — third coordinate axis recognition (CURRENT canon)
- `agentic_orchestration/research/arpg-community-axes-2026-05-29/synthesis-verdict.md` — empirical research synthesis (CURRENT)
- `agentic_orchestration/gandalf/notes/2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html` § 19 (7 mechanism families) + § 22 (5-property framework)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led discipline)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 (T4 architecture)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` (BVV)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (investment scaling)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes)

---

## 0. TL;DR

**The architectural proposal:** invert the engine's relationship to cycling. Today cycling is **production-time search**: generate broadly, validate aggressively, filter for the lucky build-defining outputs. Proposed end-state: cycling is **development-time analysis**: discover patterns once, encode them into generation logic, produce intentionally, validate as confirmation. Production compute scales linearly; quality compounds across cycles; the engine becomes a learning system that increases commercial value over time.

**The validation methodology (Matt's framing):** community-research-led hypotheses about build-defining attribute combinations → engineer the engine to produce candidates exhibiting hypothesized combinations → playtest at three or more character-level/scale planes (Matt + son in Unreal) → confirm or refute the hypothesis empirically → graduate confirmed patterns to the pattern library → encode graduated patterns into generation logic. **Hypothesis-driven engineering of generation is legitimate**; substrate-led discipline binds the *validation* step (only playtest-confirmed patterns enter the library), not the *engineering* step.

**The mathematical structure:** each hypothesized build-defining pattern is a **mathematical cell** in pattern-library space. A cell carries substrate-axis coordinates (designer-writes layer) + experiential-axis coordinates (player-names layer) + mechanism-axis coordinates (5-property scoring + mechanism family + relationship-transform vector) + validation state. **Flags** are bit-marks attached to engine-generated characters indicating which cells they match, enabling downstream stages (Phase 5 LLM cohesion judge; Wave A faction naming; Wave B per-kit identity; spirit-guide content layer; playtest evaluation) to act on the structural identity.

**The sequencing (revised 2026-06-01):** this work gates on (a) Cycle 14 wave-5 **swift snapshot closure** per 2026-06-01 recognition record (gauntlet metrics as provisional hypotheses; days to ~2 weeks); (b) WS1A architectural foundations landing — WS1A.1 substrate axis expansion + WS1A.2 Phase 5 LLM amendment + WS1A.3 flavor element wiring + **WS1A.4 per-skill bounded flavor judgment**; (c) manifestation milestone as **two-phase** — Phase 1 retroactive identity finalization on wave-5 snapshot (~1-2 weeks; single Phase 5+ re-run pass starting after Phase 4 output) + Phase 2 realization in Unreal (3-6 months); (d) playtest cycles validate THREE layers simultaneously (hypothesis cell patterns + gauntlet metric predictions + LLM naming/cohesion outputs). Pattern-library Phase A-E work begins AFTER these gates resolve. Estimated horizon: **4-8 months** from now to begin Phase A (revised down from 6-12 months pre-recognition); 9-15 months to graduate first encoded patterns.

**The risks remaining:** five concrete risks named in § 8. The most architecturally consequential: pattern encoding before substrate-axis expansion completes locks in patterns at incomplete substrate coordinates; failure-mode playtest discipline must be honored to prevent confirmation-biased graduation; small playtest population (Matt + son = 2) limits pattern generalization without supplementary instrument (community research stays load-bearing through all cycles).

---

## 1. Foundational principles — what this architecture rests on

This section locates the proposed architecture against existing canonical commitments. Each principle below is **already canon**; this document does not amend them; it composes them.

### 1.1 Designer writes substrate; Player names the experience

**Canonical anchor:** `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` (CURRENT)

Three-layer architecture:
- **Layer 1** (designer-writes-substrate; engine generative input): BC tuple + cultural lineage + period + register + weapon-type family + element + attribute + T4 strategy + investment profile
- **Layer 1.5** (designer-writes-coupling-architecture; NEW from research sprint): multiplicative loot-substrate layer count + coupling pattern; determines which Layer 2 named experiences survive economically
- **Layer 2** (player-names-experience; community-emergent): Bossing / Speedfarming / Push / Endgame Generalist / Leveling / League Starter primary archetype labels; investment-tier sub-axis (5-level); Magic Find / IIR as sub-axis; activity-specific labels (Pit / Maps / Monolith)
- **Layer 3** (vestigial designer-construct): class/ascendancy labels as secondary descriptive anchors; never primary categorical axes

The pattern library proposed in this document operates **across all three layers**. A cell carries substrate-axis coordinates (Layer 1) + coupling-architecture markers (Layer 1.5) + experiential-archetype targets (Layer 2) + vestigial-class identity for player-facing surface (Layer 3).

### 1.2 Substrate-led discipline (Disc #41)

**Canonical anchor:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41

Substrate votes; designer doesn't pre-impose taxonomy. **Refinement for this work** (per Matt 2026-05-31 pushback): the discipline prohibits *pre-imposing taxonomy onto substrate output* (claiming a cluster "is" Magic Find Rogue when behavior doesn't validate it). It does NOT prohibit *engineering generation* to produce hypothesized combinations. Engineering generation to test hypotheses is legitimate. The discipline binds the *validation* step (encode only playtest-confirmed patterns), not the *engineering* step.

**Operational implication:** the pattern library Stage 4 (generation logic integration) is constrained by substrate-led discipline. Patterns encoded into generation must have graduated through playtest validation (§ 6 below). Pre-encoded patterns from designer assertion alone violate the discipline.

### 1.3 5-property substrate framework

**Canonical anchor:** § 22 of `agentic_orchestration/gandalf/notes/2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html`

Five properties define whether a mechanism produces the player experience of "build-defining":

| Property | Definition |
|---|---|
| **P1 — Identity-axis transformation** | Mechanism changes WHICH axis the character operates on (qualitative shift, not quantitative magnitude). Example: Chaos Inoculation transforms life→ES axis. Counter-example: +5% Fire Damage. |
| **P2 — Multiplicative composition with existing investment** | Mechanism multiplies prior player investments. Example: Marauder 6pc 12,000% per Sentry. Counter-example: flat stat affix. |
| **P3 — System-substitution / decision-elimination** | Once active, some other game-system becomes irrelevant. Example: Mageblood eliminates flask cycling. Counter-example: sword with slightly better DPS. |
| **P4 — Acquisition memorability** | Discrete event the player can name and remember. Example: "the day Enigma dropped." Counter-example: routine stat affix on a yellow drop. |
| **P5 — Composition unlock** | Enables a build not viable without it. Example: Enigma enables Teleport Hammerdin. Counter-example: higher-rolled affix on existing build. |

**Composition rule:** 4-5 properties = canonical "build came online" moments. 2-3 = sub-axis or significant build choice. 0-1 = QoL / routine progression.

**Refinement for this work:** the 5 properties are the **axes of pattern-library cell scoring**. A pattern's "build-defining strength" is its multi-dimensional position in P1-P5 space. Cells with high scores on multiple properties are stronger pattern candidates. Cells with low scores are not build-defining — and per § 22 finding, that's NOT a bug; some patterns are anti-build-defining identity-anchor patterns (Wanderer-style / approachable / one-button) that intentionally score low on P1-P5.

#### 1.3.1 Reincarnated-specific P4 treatment — Matt 2026-06-01 refinement

**P4 (acquisition memorability) was imported from genre conventions** (D2 Enigma drop / D3 Aspect assembly / D4 Codex acquisition / PoE Mageblood drop / GD Devotion shrine selection) where the genre has discrete in-game acquisition events. **Reincarnated structurally does not have these surfaces** within the foreseeable launch-scope game:

- No item drops in the genre-canonical sense (per existing design direction)
- T4 is set at kit generation, not earned post-hoc (per § 22.4 of the HTML doc — "T4 is the kit's identity from L1")
- No Family B mechanism currently exists (per § 1.4 — the dominant P4 surface across D2/D3/D4 is the architectural gap that may close at Cycle 15+ but doesn't exist today)
- No paragon-grinding / set-completion / power-extraction surfaces

**Mapped P4 surface for Reincarnated:** the **character creation / Spirit discovery moment** IS the acquisition event. § 22.4 of the HTML doc named this: "Reincarnated's existing P4 surface is meta-level: receiving the new spirit each season. The seasonal-transition IS the memorable acquisition event."

This refinement makes it explicit: **P4 in Reincarnated cell scoring measures the memorability of the creation-moment, not in-game mechanism acquisition.** Specifically:

| Reincarnated P4 surface | What's being measured |
|---|---|
| Spirit form sculpting (Phase 1 of manifestation milestone) | Did the player engage meaningfully with the sculpting interaction? |
| Manifestation transition (Spirit → realized character) | Was the transition moment memorable and identity-grounding? |
| Emergent kit concept reveal (Wave B per-kit identity per § 1.7.4) | Did the player experience "I made a Necromancer" as the discovery moment? |
| Seasonal acquisition (per-season spirit-arrival) | Does receiving the seasonal spirit feel like a discrete memorable event? |

**Operational implications for cell scoring:**

- `mechanism_p4_score` field stays in schema with revised semantics (see § 3.3)
- Cells score P4 based on **predicted creation-moment memorability** for characters embodying the cell
- High P4 cells (Necromancer / Death Knight / canonical-feeling genre concepts) carry strong emergent-kit-concept reveal at creation
- Low P4 cells (generic / approachable / Wanderer-style) intentionally have low creation-moment specificity — and that's correct for their archetype

**Composition with Hidden-Spirit-Discovery proposal** (§ 23 of HTML doc): if Matt's late-2026-05-29 Hidden-Spirit-Discovery proposal eventually graduates from recognition record to architectural commitment, that would substantially AMPLIFY the P4 surface (per § 23.6 architectural implications). Current treatment: P4 mapped to existing planned creation moment (Spirit sculpting + manifestation transition + emergent concept reveal); future amplification possible if Hidden-Spirit-Discovery lands.

**What this is NOT:** does NOT pre-impose that all Reincarnated cells must score high P4. Wanderer-style / approachable / generic-flavored cells SHOULD score low P4 (their archetype is "no specific creation moment; just a kit you play") and that's correct. The framework just stops pretending P4 measures genre-acquisition; it measures creation-moment-memorability instead.

### 1.4 7 mechanism families — observational layer over substrate-led value axes

**Canonical anchor:** § 19 + § 19.2 of same HTML doc.

**Refinement iteration 3 (Matt 2026-06-01)**: the 7 families were extracted from genre research — empirical categorization of HOW the genre has historically implemented mechanisms. They are **observational categories** of "how the genre solved the build-defining-moment problem." They are NOT substrate axes that Reincarnated must target to deliver build-defining experiences. **Substrate-led discipline (Disc #41) applied at the mechanism layer requires distinguishing observation from substrate.**

The 7 families:

| Family | Pattern | Genre exemplars |
|---|---|---|
| **A** — Intra-skill transformation | Skills change qualitatively via attached transformations | LE Skill Specialization Tree; PoE Support Gem; LA Tripod; PoE2 Meta Gem |
| **B** — Extractable / imbue-able power | Powers extracted from items and imbued elsewhere | D2 Rune Words; D3 Kanai's Cube; D4 Legendary Aspect; D4 Tempering |
| **C** — Class-identity combo | Large bonuses on combo completion | GD Dual Mastery; D3 Class Set 6pc; LA Class Engraving; PoE Ascendancy |
| **D** — Passive-tree capstone | Single-instance two-sided mechanic swap | PoE Keystone; PoE Ascendancy Capstone; GD Devotion Celestial; D4 Paragon Glyph |
| **E** — Item-slot anchor | Singular unique item carrying unique effect | Mageblood; Headhunter; Enigma; Infinity; Tyrael's Might |
| **F** — Consumable / inventory-resident passive | Multiple held items providing cumulative passive | D2 Charms; LE Idols; LE Blessing |
| **G** — Proc-attached celestial / secondary | Chance-to-proc effects linked to other skills | GD Devotion Celestial; PoE Watcher's Eye; D3 Legendary Gem secondary |

#### 1.4.1 The three-layer treatment

What the 7 families REVEAL when distilled properly through substrate-led discipline:

| Layer | What it is | Substrate-axis status |
|---|---|---|
| **Layer 1 — Player-value axes** | The WHY — what player experience each mechanism produces. Already captured by the 5-property framework (P1-P5 per § 1.3): identity-axis transformation / multiplicative composition / system-substitution / creation-moment-memorability / composition-unlock. | **Generation-targetable substrate axes.** Cells are coordinates in this space. |
| **Layer 2 — Mechanism-structural dimensions** | The HOW — mechanical substrate of the mechanism. Per § 19.2 of HTML doc, the 7-family research surfaced four structural dimensions: magnitude pattern (transformative / +X% / fixed-power / +flat-stat), stackability (single / additive / multiplicative), trigger (always-on / on-event / on-condition), scaling (with item-power / with-investment / fixed). | **Generation-targetable substrate axes.** Cells specify mechanism-structural coordinates that determine HOW the mechanism delivers Layer 1 value. |
| **Layer 3 — Observational family flags** | The WHAT-IT-LOOKS-LIKE — post-hoc categorization of "this mechanism structurally resembles genre Family X." | **Descriptive flags only.** NOT generation targets. Cells may carry "resembles Family B" or "resembles Family D" tags for community-recognizability and discoverability, but generation operates at Layer 1 + Layer 2. |

**Reincarnated designs at Layer 1 + Layer 2.** Layer 3 family-similarity is post-hoc characterization.

#### 1.4.2 Why this matters — the "Family B gap" framing was wrong as substrate-led

The previous framing said: *"Family B is the highest-leverage gap-filling candidate; adding a Family B mechanism is the highest-leverage Cycle 15+ design call."* That framing **pre-imposed genre taxonomy** (build Family B!) without empirical evidence that Family B specifically — as opposed to its underlying Layer 1 + Layer 2 property profile — is what delivers the player experience.

Substrate-led refinement of the same observation:

> "Reincarnated currently delivers high P4 + high P5 via the seasonal arc + creation moment + composition unlock; delivers high P1 via spirit-swap differentiation; delivers low-to-medium P2 + P3 because T4 is set at generation and no current Reincarnated mechanism eliminates other gameplay systems. **The highest-leverage gap is the Layer 1 value-axis space (high P2 + high P3 + multiplicative-stackability + on-event-trigger + scales-with-investment Layer 2 coordinates) that no current Reincarnated mechanism covers.** Whether we fill that gap with a Family-B-resembling mechanism, a Family-E-resembling mechanism, or a Reincarnated-native mechanism with no genre analog is a downstream design decision; the substrate-axis gap is what matters, not the family taxonomy."

The genre research is still valuable — it surfaces Layer 2 structural dimensions we wouldn't have catalogued without it. The 7 families themselves become descriptive flags at the output layer, not substrate axes at the generation layer.

#### 1.4.3 Composition with hypothesis-flow methodology

Per § 2 hypothesis-flow methodology, the Stage 1 → Stage 6 cycle operates on **Layer 1 + Layer 2 coordinates**, not Family A-G membership:

| Stage | What's hypothesized at the mechanism layer |
|---|---|
| Stage 1 (hypothesis) | "Cells with high P2 + high P3 + multiplicative stackability + on-event trigger produce build-defining magic-find-rogue archetype" — Layer 1 + Layer 2 coordinates |
| Stage 2 (engineering) | Generation tuned to produce candidates exhibiting those coordinates, using whatever substrate-native machinery delivers them |
| Stage 3 (manifestation) | Realized characters whose mechanisms hit the predicted Layer 1 + Layer 2 coordinates |
| Stage 4 (playtest) | Validates whether the Layer 1 + Layer 2 coordinate profile actually produces the predicted player experience |
| Stage 5 (graduation) | Library-locks Layer 1 + Layer 2 coordinate specifications; family flags emerge as post-hoc descriptors |
| Stage 6 (encoding) | Generation logic encodes Layer 1 + Layer 2 patterns — NOT family-membership targeting |

This is substrate-led discipline applied to the mechanism layer. The 7-families work was necessary to surface Layer 2; the families themselves don't survive as substrate-targeting axes.

**Refinement for this work:** Layer 1 (P1-P5) + Layer 2 (mechanism-structural dimensions) are the substrate axes. Layer 3 (Family A-G) flags become post-hoc descriptors at output time. Cells specify Layer 1 + Layer 2 coordinates; emergent family-similarity is observed AFTER manifestation, not pre-imposed.

### 1.5 Experiential cascade architecture

**Canonical anchor:** `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md`

Third coordinate axis orthogonal to (a) BC mechanical substrate + (b) cultural-tradition lineage: experiential archetype, community-named, post-emergence consumption.

**Refinement for this work:** the experiential axis is the **player-names-experience layer flag set** for pattern-library cells. Each cell carries primary archetype flag (Bossing / Speedfarming / Push / Endgame Generalist / Leveling / League Starter) + sub-axis flags (Magic Find / IIR / etc.) + investment-tier flag + Speedfarm↔Push positioning flag.

### 1.6 ARPG community research sprint (2026-05-29) empirical findings

**Canonical anchor:** `agentic_orchestration/research/arpg-community-axes-2026-05-29/synthesis-verdict.md` (CURRENT)

Empirically validated at 104-build scale across 6 sites × 4 games:
- **6 primary archetype labels STRONG cross-site convergence**: Bossing / Speedfarming / Push / Endgame Generalist / Leveling / League Starter
- **5+1 layer multi-layer loot substrate model** with party-scale 6th layer emergent
- **Coupling architecture (Layer 1.5) is the determinative variable** — PoE 6-layer multiplicative cascade restricts composite-required; LE 3-layer simpler-multiplication preserves single-axis viability
- **Speedfarm↔Push binary as universal variant-splitting axis** (4/4 games, 37% of all variants)
- **Magic Find pattern morphed across genre** — D2/D3 primary archetype dead; PoE2 EA elevates to first-class explicit stat target (100-150% IIR); D4 explicitly retired in favor of Torment Tier
- **Reincarnated recommendation**: ≤3 multiplicative loot substrate layers; LE-style simpler-multiplication; preserve single-axis archetype viability

**Refinement for this work:** the research findings are the **empirical seed corpus** for the hypothesis-flow methodology. Community-research-led hypothesis batches (§ 2 Stage 1) draw from this corpus + ongoing community-research sprints + Matt's lived genre experience. The research is not finished; ongoing legolas Mode A research extends the empirical seed corpus as the work progresses.

### 1.7 Per-skill flavor judgment architecture (WS1A.4)

**Source:** Matt 2026-06-01 refinement during Pattern B dialogue on the manifestation milestone scope.

**The architecture:** in addition to per-kit primary element (substrate) and per-kit sub-element / flavor element selection (WS1A.3), each SKILL within a kit gets an LLM-judged flavor alignment. The LLM judgment is **bounded** — constrained to the kit's substrate-declared element pair — not free invention from the full canonical 2.5 flavor vocabulary.

#### 1.7.1 Single-element kit case (1 primary + 1 sub)

Kit declares:
- **Primary element**: 1 from the canonical 8-element catalog (e.g., earth)
- **Sub / flavor element**: 1 selection from the **primary's flavor pool** (e.g., bone — which lives in earth's flavor pool because bone is earth-substrate-aligned)

> **Important constraint** (Matt 2026-06-01): the sub-element pool is the PRIMARY's flavor pool, NOT the full canonical 2.5 vocabulary. Earth's sub-elements are earth-aligned (bone, stone, ore, root, sand, clay, crystal, mineral, etc.) — NOT shadow, NOT fire, NOT lightning (those are their own canonical elements with their own flavor pools).

Per-skill LLM judgment chooses from **3 bounded options**:

| Option | Meaning | Example (Earth + Bone kit) |
|---|---|---|
| `primary` | Skill aligns with primary element flavor only | Stone Spike (pure earth) |
| `sub` | Skill aligns with sub-element flavor only | Bone Armor (pure bone-sub) |
| `blend` | Skill composes primary + sub flavors | Bone Spear (earth structural + bone-sub aspect) |

LLM does NOT pick from outside this 3-option set per skill. The kit's flavor identity is constrained by its substrate declaration.

#### 1.7.2 Hybrid 2-element kit case (2 primaries + 2 subs)

Kit declares:
- **Primary Element 1** (P1): canonical element (e.g., earth)
- **Primary Element 2** (P2): canonical element (e.g., shadow)
- **Sub / Flavor Element 1** (S1): drawn from P1's flavor pool (e.g., bone, from earth's pool)
- **Sub / Flavor Element 2** (S2): drawn from P2's flavor pool (e.g., umbra, from shadow's pool)

Per-skill LLM judgment chooses from **15 bounded options** — every non-empty subset of {P1, P2, S1, S2}:

| Option | Subset | Example identity (Earth + Shadow / Bone + Umbra kit) |
|---|---|---|
| A | {P1} | Stone Spike (pure earth) |
| B | {P2} | Shadow Drain (pure shadow) |
| C | {P1, P2} | Stone Curse (earth + shadow blended; both primaries) |
| D | {S1} | Bone Armor (pure bone-sub) |
| E | {S2} | Umbral Veil (pure umbra-sub) |
| F | {S1, S2} | Bone Shroud (bone + umbra blended; both subs) |
| G | {P1, S1} | Petrified Marrow (earth + bone; same-primary blend) |
| H | {P1, S2} | Earth Wraith (earth + umbra; cross-primary blend) |
| I | {P2, S1} | Bone Specter (shadow + bone; cross-primary blend) |
| J | {P2, S2} | Shadow Mist (shadow + umbra; same-primary blend) |
| K | {P1, P2, S1} | Bone Spear (earth + shadow + bone; triple) |
| L | {P1, P2, S2} | Umbral Quake (earth + shadow + umbra; triple) |
| M | {P1, S1, S2} | Marrow Wraith (earth + bone + umbra; triple) |
| N | {P2, S1, S2} | Bone Wraith (shadow + bone + umbra; triple) |
| O | {P1, P2, S1, S2} | Soulshatter Bone (all four; full quad blend) |

15 options = 2⁴ - 1 (every non-empty subset of 4 elements). Same bounded discipline — LLM picks from the kit's substrate context, not from arbitrary flavor vocabulary.

#### 1.7.3 Why bounded judgment matters

| Dimension | Unbounded LLM judgment | Bounded {primary/sub pair OR P1/P2/S1/S2 quad} |
|---|---|---|
| Substrate-led discipline | LLM could introduce off-substrate flavor identities | LLM constrained to kit's substrate-declared pair/quad |
| Kit coherence | Risk of element soup; identity fragmentation | All skills root in same substrate identity space |
| LLM API cost | Choice space = canonical 2.5 pool (~30+) per skill | 3 options (single) or 15 options (hybrid) per skill |
| Emergent class concept | Risk of incoherent identity composition | Composition stays within substrate identity; emergent class concept (necromancer, druid, etc.) cleanly emerges from skill flavor composition |
| Cohesion judge inputs | Higher variance; harder to cluster | Lower variance; faction clustering operates on coherent flavor signatures |

The bounded approach preserves substrate-led discipline at the per-skill semantic-identity layer.

#### 1.7.4 Emergent kit concept ("necromancer" emerges without being declared)

Worked example — single-element kit:
- **Substrate**: Primary = Shadow; Sub = Umbra (from shadow's flavor pool); cultural lineage = necromantic-folk; period = early-medieval; register = grim
- **Skills** (4 skill slots from Phase 4 archive, each with mechanical properties)
- **Per-skill LLM judgment**: skill 1 = `blend`, skill 2 = `primary`, skill 3 = `sub`, skill 4 = `blend`
- **Phase 5a skill naming**: Shadow Spear, Umbral Drain, Shadow Veil, Soul Shroud
- **Phase 5b cohesion judge**: clusters with other shadow + umbra + necromantic-folk + grim kits
- **Wave B per-kit identity LLM**: emerges **"Necromancer"** as kit concept

Designer never pre-imposed "necromancer." Substrate declared shadow + umbra + necromantic-folk + grim. LLM per-skill bounded judgment + downstream composition synthesized the kit concept. **Substrate-led discipline preserved end-to-end.**

This is "emergent classes, not abandoned classes" made operational. Compare to designer-imposed alternative ("here's a necromancer class taxonomy; generate necromancer kits") — that violates substrate-led discipline. Per-skill bounded LLM judgment with substrate-declared element scope preserves the discipline AND produces the genre-recognizable kit concept.

#### 1.7.5 Composition with hybrid kits enables much richer emergent concepts

Hybrid kits' 15-option per-skill judgment matrix supports complex emergent identities. Earth + Shadow + Bone + Umbra hybrid produces concepts that single-element kits cannot:

- "Death Knight" (Earth-armor + Shadow-magic + Bone-physical + Umbra-aspect blends)
- "Bone Witch" (Bone-physical + Umbra-spectral focus across skills)
- "Tomb Warden" (Earth-defensive + Bone-physical + Shadow-passive blend)
- "Soul Reaver" (Shadow-active + Bone-projectile + Umbra-finishing blends)

The kit concept emerges from composition of bounded per-skill judgments across the 4-element substrate space. Single-element kits cannot reach these emergent concepts because their 3-option scope is too narrow. Hybrid kits are architecturally richer at the player-experience layer.

This composes with `canonical/story/c-hybrid-cell-and-curation-architecture-2026-05-28.md` — hybrid kits as a deliberate kit-architecture choice that produces richer experiential identity.

#### 1.7.6 Cost analysis

| Kit type | Skills per kit (typical) | Options per skill | Total per-kit judgment cost (LLM calls) |
|---|---|---|---|
| Single-element kit | ~4-6 skills | 3 | ~4-6 LLM judgments per kit |
| Hybrid 2-element kit | ~4-6 skills | 15 | ~4-6 LLM judgments per kit (same call count; richer choice space) |

LLM call count is the same; choice space per call is richer for hybrid. Marginal API cost is comparable. Single-element kits are NOT cheaper to judge; both are bounded by the kit's substrate scope; both produce one judgment per skill.

#### 1.7.7 Composes with Cycle 14 wave-5 retroactive identity finalization

Per § 2 hypothesis-flow methodology refinement (Stage 2.5 identity finalization), the per-skill flavor judgment **runs retroactively** on the wave-5 snapshot archive starting after Phase 4 archive insertion:

- Wave-5 snapshot kits already declare primary element (substrate)
- Sub-element selection per kit (WS1A.3) runs retroactively
- Per-skill flavor judgment (WS1A.4) runs retroactively
- Phase 5b cohesion clustering re-runs with full flavor judgment inputs
- Wave A faction naming + Wave B kit identity naming re-fire with rich semantic inputs

Single Phase 5+ re-run pass against snapshot archive produces full identity-finalized output. ~1-2 weeks horizon as named in § 5.

#### 1.7.8 Pipeline placement decision — Phase 5+ LLM naming fires AFTER Pareto reduction (Option A; iter 5 lock per Matt 2026-06-01)

**Decision:** Phase 5+ LLM naming (Phase 5a' per-skill flavor judgment + Phase 5a skill naming + Phase 5b cohesion clustering + Wave A faction naming + Wave B per-kit identity naming) fires **AFTER** Phase 4 Pareto reduction. On ~30 reduced kits, not on ~650 pre-Pareto kits.

**The three options considered:**

| Option | Order | LLM cost | Cohesion judge n | Faction representation |
|---|---|---|---|---|
| **A (LOCKED)** | math-validate → Pareto-reduce → LLM-name → cluster | LOW (~30 kits; ~150-210 LLM calls; ~$1.50-4.50 per cycle) | Small (~30); ~3-5 emergent factions; ~6-10 kits per faction | Constrained by Pareto-survived population; cluster composition depends on what survived |
| **B (FUTURE REFINEMENT)** | math-validate → LLM-name → cluster → Pareto-per-cluster | HIGH (~650 kits; ~3,250-4,550 LLM calls; ~$30-90 per cycle) | Large (~650); semantic identity informs clustering | Preserves faction representation in final 30 kits (Pareto operates per-cluster) |
| **C (REJECTED)** | math-validate → LLM-name → Pareto-reduce → cluster | HIGH | Small (~30) | Same as A but at B's cost; mostly inferior |

**Why Option A is locked:**

1. **Cost efficiency** — 22× LLM call reduction without obvious quality loss at current stage. Bounded absolute cost ($1.50-4.50/cycle vs $30-90/cycle).
2. **Substrate-led discipline composition with gauntlet provisional recognition (`canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md`)** — Pareto's selection axes (substrate + math-viability) are themselves provisional pending playtest validation; adding semantic axes to Pareto without empirical validation would compound provisionality, not resolve it.
3. **Cohesion judgment scope** — n=30 is sufficient for meaningful clustering; comparable to genre ship scale (D2 has 7 classes; D4 has 6 classes; PoE has ~20 ascendancies; ~3-5 emergent factions per Reincarnated season is appropriate).
4. **Retroactive runs are cheaper** — if we need to re-name later (e.g., per identity-finalization Phase 1 of manifestation milestone), only 30 kits to re-process.
5. **Iteration speed** — smaller LLM batch fires faster; tighter dev loop; faster wave-close turnaround.
6. **Identity emergence is largely predictable from substrate** — BC tuple + cultural lineage + element + period + register strongly constrain emergent identity. Cohesion judge can largely INFER which substrate clusters will produce which emergent identities without running all 650 LLM passes; running on 30 named kits is sufficient signal.

**Counter-argument honestly surfaced:** Option B is more architecturally complete — semantic identity diversity is a substrate-led property that Pareto-on-math-axes can't see. If playtest evidence reveals natural-faction-loss (e.g., expected emergent identity like "Death Knight" failed to surface because its candidate kits were Pareto-eliminated before naming), that's empirical evidence for B. Until that evidence exists, Option A is the substrate-led-disciplined choice.

**Deferral path to Option B if playtest evidence supports:** during manifestation milestone Phase 1 identity finalization + subsequent playtest cycles, if observation surfaces that meaningful identity diversity was lost at the Pareto step, gandalf authors a refinement record + KR routes a pipeline-restructure dispatch + star-lord implements Option B. Until that evidence: Option A is locked.

**Composition with hypothesis-flow methodology:** the Stage 1 → Stage 6 cycle operates on Option A pipeline structure. Hypothesis cells at Stage 1 inform Phase 2 BC discovery; engineering at Stage 2 tunes generation parameters; manifestation at Stage 3 (Phase 1 identity finalization re-runs Phase 5+ on snapshot archive); playtest at Stage 4 validates whether the Phase 5+ outputs feel coherent. Three-layer playtest validation (§ 6.0) includes "did meaningful identity diversity survive Pareto reduction?" as part of Layer 3 (LLM naming + cohesion outputs).

### 1.8 Multi-axis experiential architecture (iter 4 refinement — Matt 2026-06-01)

#### 1.8.1 The decomposition

The 6 primary archetype labels from community research (Bossing / Speedfarming / Push / Endgame Generalist / Leveling / League Starter) are NOT a flat enumeration. Community vocabulary emerged on top of orthogonal underlying axes; compound labels ("Push Bossing" / "Leveling Speedfarm" / "League Starter Mapper") expose the compositional structure.

**Three primary axes (Matt 2026-06-01 decomposition):**

| Axis | Values | Meaning |
|---|---|---|
| **Progression-Stage axis** | Leveling / League Starter / End Game | When in the player journey is the build optimized for? Leveling = L1-50 journey; League Starter = endgame-from-scratch self-sufficient; End Game = true endgame (only ~15% of players reach per working hypothesis) |
| **Target-Pattern axis** | Bossing / Speedfarming | What target pattern does combat optimize for? Bossing = single-strong-high-quality targets; Speedfarming = many-weak-low-quality targets |
| **Depth-vs-Breadth axis** | Push / Generalist | How deep vs how broad? Push = deep specialization into one content type; Generalist = broad coverage across many |

**Additional axes (gandalf 2026-06-01 designer additions; iter 6 amendment: Mode axis REMOVED per Matt observation):**

| Axis | Values | Treatment |
|---|---|---|
| **Activity-Format axis** | Per Reincarnated's TBD endgame structure | Game-specific endgame content type; values determined by what endgame Reincarnated ships |
| **Loot-Focus sub-axis** | Magic-Find / Currency-Farmer / Drop-Density / Generic | Sub-axis within Speedfarming; carries enough identity weight to deserve dimension |
| **Maxroll 5-axis structured rating** | Bossing/Speed/Push/Survivability/Playability | Continuous per-axis scoring (0-10 each); same character can score on multiple simultaneously |

**Mode axis (Hardcore / Softcore) — REMOVED from architecture per Matt 2026-06-01 iter 6 observation:** if Reincarnated ever adds HC/SC mode option, it would NOT differentiate kits/cells — all kits are available within both modes. Mode is a player-session-level choice, not a kit-architecture-level property. Including it as a substrate axis was a category error: substrate axes characterize kit identity; mode characterizes player session. HC-viability (if HC mode is added later) is a higher Survivability threshold gate within the existing Viability axis treatment, NOT a separate axis. Open question 41 (§ 8f) tracks this.

#### 1.8.2 Axis-type taxonomy — Identity vs Viability vs Mode vs Sub

Different axes get different treatment in cell scoring and generation:

| Axis type | Treatment | Examples |
|---|---|---|
| **Identity axis** | Specialize-and-differentiate; per-cell prefer dominance pattern; cells declare axis dominance | Target-Pattern (Bossing vs Speedfarming); Depth-vs-Breadth (Push vs Generalist) |
| **Viability axis** | Universal-adequate-score; gates per minimum threshold; cells gate below threshold | Survivability (Maxroll); Playability (Maxroll); **possibly Leveling per § 1.8.5 hypothesis**; HC-viability if HC mode added (higher Survivability threshold) |
| **Sub-axis** | Within-axis sub-classification | Loot-Focus within Speedfarming |

**Reincarnated designs treat each axis-type differently.** Identity axes get specialization preference and per-cell dominance declaration. Viability axes get minimum-threshold gates (must-pass below threshold). Sub-axes refine within parent axes.

**Iter 6 amendment:** Mode axis (Hardcore/Softcore) REMOVED — mode is player-session-level choice, not kit-architecture-level property. If HC mode is added to Reincarnated, HC-viability is a HIGHER Survivability threshold within existing Viability axis treatment, NOT a separate axis-type category.

#### 1.8.3 Mutual exclusivity preference — substrate-led empirically validated

**Structural fact:** orthogonal axes ENABLE multi-axis membership. A character can score on Bossing AND Speedfarming simultaneously if mechanics support both target patterns. A character can score on Leveling AND End Game if the build scales across the journey. This is just truth about what's possible.

**Designer preference (Reincarnated-specific):** prefer TENDENCY toward mutual exclusivity at identity-axis layer to preserve:

| Preserved | Why |
|---|---|
| Identity clarity | Sharper per-kit Wave B naming (per § 1.7); "Bossing Necromancer" stronger identity than "Bossing-and-Speedfarm-and-Generalist Necromancer" |
| Build-defining moment integrity | Specialization grounds canonical "build came online" experience per § 1.3 P5 |
| Substrate-led signal strength | Strong substrate votes produce identity-strong characters; multi-axis-spanning profiles suggest weak vote |
| Cohesion-judge clustering quality | Specialized profiles cluster cleanly into factions; over-generalist profiles produce mushy boundaries |
| Commercial differentiation | Procedural character diversity is stronger when characters specialize differently; generic-everything characters undercut the value proposition |

**Constraint pulling opposite direction (Reincarnated structural):** 50-level scope + no multiple acts + 85%-never-reach-endgame working hypothesis means:

| Constraint | Implication |
|---|---|
| 50-level leveling scope | Shorter than genre norm (D2's 99-level + 5-act; PoE's 100-level + 10-act); builds must be playable through full leveling |
| No multiple-acts structure | Can't support stage-specific specialization where Act 1 build differs from Act 5 build |
| 85% never reach endgame | Leveling IS the primary experience for majority of player population |
| Single-player solo | Every build must be self-sufficient through full content; no party-composition diversity to absorb over-specialized builds |

**Substrate-led discipline applied:** the mutual exclusivity preference is a HYPOTHESIS that playtest validates. Generation does NOT pre-impose mutual exclusivity through hard constraints; substrate produces cells; playtest evaluates whether identity-strong cells (specialized profiles) or identity-weak cells (multi-axis-spanning profiles) actually feel better. Hypothesis-flow Stage 4 validates per-cycle.

#### 1.8.4 Cell shape framework

Cells declare intended profile shape per their multi-axis coordinates:

| Cell shape | Profile pattern | Generation preference |
|---|---|---|
| **Specialized** | Dominant on 1 identity axis; minimum-adequate on viability axes; sub-dominant or absent on other identity axes | Most common; favored for identity strength; default cell shape |
| **Hybrid** | Significant scores on 2-3 identity axes; intentional cross-axis utility (e.g., Boss-Speed dual-capability build) | Common for hybrid 2-element kits per § 1.7.2; intentional cross-archetype design |
| **Generalist** | Moderate scores across many identity axes; "do everything" archetype | Rare; high-investment-tier; PoE Mageblood-Headhunter-class extreme builds; intentional anti-specialization identity |
| **Anti-specialization** | Intentionally low on identity axes; high on Survivability + Playability; identity-anchor for approachable / one-button archetype | Wanderer-style per § 22 of HTML doc; NOT a bug; intentional design choice for approachable archetype |

Cell shape is declared at cell authoring. Generation parameters can favor specific shapes statistically. Playtest validates whether the predicted shape actually emerges in manifested characters.

#### 1.8.5 Leveling-as-viability-axis hypothesis (Reincarnated-specific; pending playtest validation)

**Hypothesis:** the Progression-Stage axis treats Leveling as a viability axis (universal-adequate-score required), not an identity axis (specialize-and-differentiate). League Starter and End Game remain identity axis values; Leveling becomes a viability gate.

**Reasoning:**
- 50-level scope is shorter than genre norm
- No multiple-acts structure to support stage-specific specialization
- 85%-never-reach-endgame means leveling IS the primary experience for most players
- Single-player solo means every build must be self-sufficient through full leveling

**If validated:** ALL Reincarnated cells must predict adequate Leveling-axis scores; cells below threshold are gate-failed regardless of endgame specialization. Endgame specialization (Push / Generalist + Bossing / Speedfarming + League Starter / End Game) operates on top of universal Leveling viability.

**If refuted:** Progression-Stage axis treats all three values (Leveling / League Starter / End Game) as identity axis values; cells can specialize toward stages including endgame-only builds.

This is a hypothesis-flow Stage 1 hypothesis. Playtest cycles across Leveling + Endgame validate which framework holds for Reincarnated specifically. Decision deferred until empirical evidence (per recognition-validate-commit discipline).

#### 1.8.6 Genre-relative specialization positioning

Quick designer-mode positioning to anchor the Reincarnated specialization preference:

| Game | Specialization norm | Reincarnated relative position |
|---|---|---|
| **D2** | Strong specialization (MF Sorc / Hammerdin / Bone Necromancer all narrow) | Stronger than Reincarnated likely needs |
| **D3** | Broad generalism (most builds do most content; Greater Rift push is specialization layer) | Possibly Reincarnated's closest analog given 50-level scope |
| **D4** | Moderate specialization (Pit Push / Helltide farm / Boss Materials distinguish) | Possibly Reincarnated's other closest analog |
| **PoE** | Very strong specialization (Mapper vs Bosser vs Currency Farmer; Mageblood-Headhunter for extreme generalist) | Genre's extreme; Reincarnated needs distinctness but probably not this restrictive |
| **LE** | Moderate specialization (most builds work for most content; some specialization toward Echo types) | Possibly Reincarnated's closest LE-style positioning |

**Designer hypothesis (pending playtest validation):** Reincarnated targets **LE-to-D3 level moderate specialization** with a strong Leveling viability gate. Specialization at identity-axis layer (Target-Pattern + Depth-vs-Breadth) preserves commercial differentiation + identity strength. Universal viability at Leveling axis honors structural constraints. End-game-tier extreme specialization (PoE-style) reserved for high-investment cells targeting the 15% endgame population.

#### 1.8.7 Endgame content type architecture — player-input procedural map generation (Matt 2026-06-01 iter 8 proposal)

**The prerequisite gate Matt identified:** the Depth-vs-Breadth axis requires multiple endgame content types to be meaningful (Push specializes INTO; Generalist generalizes ACROSS). Without multiple content types, the axis collapses. Same gate applies to Activity-Format axis values and to Target-Pattern endgame specialization.

**Matt's proposed solution (iter 8):** extend the existing planned procedural map generation system to accept **player input modifiers** with **unlimited scaling via input selection** (similar to PoE 1/2 maps, but architecturally thinner per coupling-architecture discipline).

**What's already in plan (existing canonical commitments):**
- Procedural map generation (per existing roadmap)
- Faction + anti-faction themed map elements (per `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md`)

**What this iter 8 proposal ADDS:**
- Player input layer (UI + input selection mechanic at endgame)
- Input-driven generation parameters (engine accepts input modifiers; substrate-led generation responds)
- Scaling progression (tier system via input combinations; unlimited scaling encompasses infinite-tower concept)

**Architectural payoff — single content design activates 5+ axes:**

| Axis | Activation via player-input maps |
|---|---|
| **Depth-vs-Breadth** | Push = high-tier scaling specialization; Generalist = broad input variety mastery |
| **Activity-Format** | Input categories become Activity-Format values (boss-rich / mob-dense / currency-rich / magic-find-rich / anti-faction-rich / etc.) |
| **Target-Pattern** | Bossing = boss-input maps; Speedfarming = mob-density-input maps |
| **Loot-Focus sub-axis** | Magic-find inputs → loot magic-find sub-axis; currency inputs → loot currency sub-axis |
| **Maxroll 5-axis Push score** | Activates via tier-scaling specialization |

**Genre composition:**

| Game | Layer count | Reincarnated alignment |
|---|---|---|
| D4 Pit | ~1 layer (tier selection) | Lighter than target |
| **LE Monolith** | **~3 layers (echo + corruption + modifier)** | **TARGET — matches Reincarnated coupling-architecture per sprint synthesis ≤3 layer recommendation** |
| PoE Maps | 6 layers (map IIR × atlas × scarab × Delirium × pack-size × sextant) | EXCEEDS target — DO NOT replicate |

**Coupling-architecture discipline (per § 1.1.5 Layer 1.5):** Reincarnated's player-input map system MUST stay at **≤3 multiplicative input layers** with **light-multiplicative OR additive coupling** to preserve single-axis archetype viability (per 2026-05-29 ARPG sprint synthesis verdict § 7.5). Avoid PoE-style 6-layer exponential cascade. Target LE Monolith 3-layer simpler-multiplication.

**Uber-Bosses-without-separate-content-type (bonus payoff):** boss-input maps spawn pinnacle bosses within the map system. No separate Uber Boss content type required; bosses emerge from input selection. This composes with genre-canonical pattern (PoE Pinnacle Bosses appear in Atlas at high-tier specific encounters; D4 Tormented Echoes integrate with Helltide / Whisper systems; LE Boss Echoes integrate with Monolith).

**Infinite-tower-without-separate-content-type:** the tier-scaling progression via input combinations IS the infinite tower. Climbing the tier scale = climbing the tower. No separate infinite-tower content type required.

**Scope implication:** bounded addition to existing map generation plan. Estimated 3-6 months engineering after manifestation milestone. Composes with existing cascade architecture (faction inputs map to faction theming; anti-faction inputs map to opposition theming).

**Composition with hypothesis-flow methodology:** the player-input layer is a SUBSTRATE for hypothesis generation. Cells can hypothesize "cells with input-selection-A + tier-N performance profile = build-defining X experience"; engineering tunes generation; playtest validates. Same six-stage cycle; richer substrate.

**Architectural commitment status:** **PROPOSED PLAYTEST-PENDING.** This is Matt 2026-06-01 game-design proposal; not yet canonicalized as committed architecture. Pattern B refinement conversation about player-input system specifics + canonical recognition record authoring + cross-seam routing (gamora engine generation + star-lord pipeline + drax UI + gandalf design) compose toward eventual commitment. Open questions in § 8h cover specifics.

**Iter 8 placeholder doc treatment:** Depth-vs-Breadth axis no longer PROVISIONAL pending content type architecture; instead, it's PROPOSED-PENDING the player-input-procedural-map-generation architecture committing. If that architecture commits → Depth-vs-Breadth axis activates fully. If it doesn't commit → Depth-vs-Breadth axis reverts to PROVISIONAL pending alternative content type architecture.

---

## 2. The hypothesis-flow methodology (Matt 2026-05-31 framing)

### 2.1 Six-stage cycle

The proposed methodology is a closed loop:

```
┌────────────────────────────────────────────────────────────────┐
│  STAGE 1 — Multi-source hypothesis generation                   │
│  Inputs (availability-gated per § 2.4 launch lifecycle):        │
│    Pre-launch:                                                  │
│      - Empirical seed corpus (2026-05-29 ARPG sprint)           │
│      - Ongoing legolas Mode A research                          │
│      - Matt genre experience                                    │
│      - Community discourse mining (genre community)             │
│    Soft-launch+:                                                │
│      - Matt + son playtest signal                               │
│      - Cross-cell composition discovery from prior cycles       │
│    Player-launch+:                                              │
│      - Real player game telemetry (star-lord seam)              │
│      - Reincarnated-community-derived telemetry                 │
│      (hosted forums + blogs + social posts + third-party        │
│      community sites — iter 7 addition; per § 2.4)              │
│  Output:   Hypothesized mathematical cell (provisional)         │
│  Discipline: Substrate-led at every available data source       │
│            (community vocabulary votes; telemetry votes)         │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  STAGE 2 — Engineer generation to produce hypothesis            │
│  Input:    Provisional cell                                     │
│  Output:   Engine produces N candidates exhibiting cell         │
│  Discipline: Engineering freedom; tune substrate axes /          │
│              vectors / categorical flags to materialize the     │
│              hypothesized combination                            │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  STAGE 3 — Manifestation in Unreal (single character first;     │
│            scaling later)                                       │
│  Input:    JSON spec from engine output                         │
│  Output:   Realized character in Unreal with modular assembly   │
│            from component library                               │
│  Discipline: Honor modular character architecture; visual       │
│              identity grounds in substrate (period dress,       │
│              energy signature, basic moveset)                   │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  STAGE 4 — Playtest at 3+ character-level/scale planes          │
│  Input:    Manifested character + comparison characters         │
│            (failure-mode playtest)                              │
│  Output:   Playtest evidence per power plane;                   │
│            confirm or refute hypothesis;                        │
│            failure-mode comparison evidence                     │
│  Discipline: Empirical-evidence validation; test absence of     │
│              pattern, not just presence                          │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  STAGE 5 — Graduate or refine                                   │
│  Confirmed across all planes + failure-mode validates? →        │
│        Cell graduates: PROVISIONAL → PLAYTEST-CONFIRMED         │
│        After cross-variation playtest cycles complete →         │
│        Cell graduates: PLAYTEST-CONFIRMED → LIBRARY-LOCKED      │
│  Refuted? → Refine hypothesis; revise Stage 1; re-cycle         │
│  Partial? → Math pattern evolution; refine cell coordinates     │
│  Discipline: Graduation criteria are strict; substrate-led      │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  STAGE 6 — Encode library-locked cells into generation logic    │
│  Input:    Library-locked cells (graduation complete)            │
│  Output:   Generation logic incorporates patterns as weighted    │
│            feature selection / templates / constraints          │
│  Discipline: Encoding restricted to LIBRARY-LOCKED cells only.   │
│              PROVISIONAL or PLAYTEST-CONFIRMED cells DO NOT     │
│              enter generation logic. Substrate-led discipline   │
│              honored at the encoding gate.                       │
└────────────────────────────────────────────────────────────────┘
```

The cycle continues indefinitely. Stage 6 output feeds back into Stage 1 — newly encoded patterns may surface new hypotheses (e.g., "now that Pattern X is encoded, what compositional patterns of multiple X-bearing cells become viable hypothesis candidates?").

### 2.2 Substrate-led discipline at each stage

| Stage | Substrate-led discipline anchor |
|---|---|
| Stage 1 (hypothesis generation) | Community vocabulary votes; hypotheses ground in observed community-named experiences, not designer-fiat invention |
| Stage 2 (engineering) | Engineering is free; substrate-led discipline does NOT bind generation parameter tuning |
| Stage 3 (manifestation) | Modular architecture honors generation output; visual identity grounds in substrate (period + cultural + element + weapon family); designer doesn't impose visual taxonomy beyond substrate vote |
| Stage 4 (playtest) | Empirical evidence is the validation instrument; designer prediction is the null hypothesis tested against player experience |
| Stage 5 (graduation) | Graduation requires multiple cycles of empirical confirmation; failure-mode playtest required (test absence of pattern); single-cycle confirmation is insufficient |
| Stage 6 (encoding) | Only LIBRARY-LOCKED cells enter generation logic; PROVISIONAL cells inform engineering at Stage 2 but do NOT lock generation outputs |

### 2.3 Composition with closed-loop validation (Matt's framing literal)

Matt's articulation: "Community led research suggests that a specific set of early game attributes, transformed in a specific way to produce a 90 degree or 180 degree (inverse) relationship while also delivering a specific KPM, an ability to win across multiple combatant encounter formats and simultaneously delivering on one of the axes of fundamental gameplay experiencial modalities is a build defining event, then we engineer it. After it is engineered and emitted from the engine, my son and I play test it in Unreal combat (ultimately we will need to test at 3 or more character level/scale planes) against the hypothesised build defining event. Our play test confirms or denies the hypothesis, and across play tests we evaluate mathematical patterns to evolve the hypothesis that we test."

Mapped to the six stages:

| Matt's framing element | Maps to |
|---|---|
| "Community led research suggests..." | Stage 1 — hypothesis generation from community-research seed corpus |
| "specific set of early game attributes, transformed in a specific way to produce a 90 degree or 180 degree (inverse) relationship" | Mathematical cell — substrate axis coordinates + mechanism-relationship vector (§ 3 below) |
| "delivering a specific KPM" | Cell field — KPM target (§ 3.4) |
| "ability to win across multiple combatant encounter formats" | Cell field — multi-format winning criteria (§ 3.4) |
| "delivering on one of the axes of fundamental gameplay experiencial modalities" | Cell field — primary experiential archetype flag (§ 4.1) |
| "then we engineer it" | Stage 2 — engineering generation to produce candidates |
| "after engineered and emitted from the engine, my son and I play test in Unreal combat" | Stage 3 (manifestation) + Stage 4 (playtest) |
| "ultimately we will need to test at 3 or more character level/scale planes" | Cell field — power-plane validity (§ 3.4) + Stage 4 cross-plane discipline |
| "play test confirms or denies the hypothesis" | Stage 5 — graduation or refinement |
| "across play tests we evaluate mathematical patterns to evolve the hypothesis" | Stage 5 partial-confirmation branch — math pattern evolution; cell coordinate refinement |

The methodology you named is the methodology this document operationalizes. The six stages are an articulation of your closed loop into discrete steps with substrate-led discipline anchors per step.

### 2.4 Multi-source hypothesis generation across launch lifecycle (iter 7 refinement — Matt 2026-06-01)

**Matt 2026-06-01 observation:** the methodology should also include real player game telemetry + community-derived telemetry (hosted Reincarnated forums + blogs + social posts + third-party community sites) as engine learnings, with implementation of hypotheses regarding play time, retention, etc.

**Affirmation + framing:** not too soon. Designing the methodology WITHOUT anticipating these sources would be the bigger error. Data sources scale with launch lifecycle; methodology stays consistent; substrate-led discipline at the player-experience layer (per `2026-05-29-designer-writes-substrate-player-names-experience-principle.md`) is fundamentally the right frame for community-derived data.

#### 2.4.1 Hypothesis-source availability gates across launch lifecycle

The Stage 1 input list is availability-gated. Different sources become available at different launch phases. The methodology weights hypothesis generation across whatever sources are available at the current gate:

| Lifecycle phase | Available hypothesis sources | Source weighting |
|---|---|---|
| **Pre-launch** (current) | ARPG sprint empirical seed corpus; ongoing legolas Mode A research; Matt genre experience; community discourse mining (GENRE community — D2/D3/D4/PoE/LE/etc.) | Substantial weight on community research; Matt experience anchor |
| **Alpha / private playtest** | + Matt + son playtest signal; + small alpha tester pool (if any) | + playtest signal added |
| **Beta / broader playtest** | + broader playtest population telemetry; + initial community formation | + telemetry signal weighted with playtest |
| **Soft launch** | + real player game telemetry (small player base); + early Reincarnated community emergence | Player telemetry weighted with community research |
| **Full launch** | + full player telemetry; + Reincarnated-hosted community sites; + third-party community sites (if they emerge for Reincarnated) | Full multi-source weighting |
| **Mature ecosystem** | + community-emergent vocabulary (Reincarnated community vocabulary); + blogs + social posts + community-authored guides + streamers | Full ecosystem; community-derived data weighted comparable to or higher than genre community research |

**Substrate-led discipline at each gate:** whatever data sources are available at a gate, the substrate (community vocabulary; telemetry signals; playtest evidence) votes. Designer doesn't pre-impose hypothesis sources; available substrate signals inform hypothesis generation.

#### 2.4.2 Real player game telemetry — methodology

Once Reincarnated has players, the engine collects telemetry events that inform hypothesis generation:

| Telemetry event class | Hypothesis signal | Engine collection responsibility |
|---|---|---|
| **Play time per character** | Which characters players stay with vs abandon → cell graduation signal (high-engagement cells emerge) | Star-lord seam (telemetry collection) |
| **Character creation paths** | Which Spirit sculpting paths players take → emergent design preference signal | Star-lord + Drax (creation UI telemetry) |
| **Retention by character type** | Which character types retain players past day 7 / day 30 / day 90 → cell long-term viability signal | Star-lord |
| **Combat encounter outcomes per character** | Which characters succeed at which encounter types → gauntlet metric validation (refines per gauntlet provisional recognition) | Star-lord + gamora |
| **Build-defining moment frequency** | When do players experience "build came online" moments → P5 composition unlock validation | Star-lord with engine instrumentation |
| **Investment tier progression** | How players invest across tiers → investment scaling validation (doc 51) | Star-lord |
| **Faction membership / loyalty patterns** | Which factions players gravitate to + how long they stay → cohesion judge faction validation | Star-lord with engine instrumentation |
| **Skill usage patterns per character** | Which skills players actually use → per-skill flavor judgment validation (§ 1.7 WS1A.4 hypothesis testing) | Star-lord |

**Composition with star-lord seam:** real-player-telemetry collection IS what star-lord's seam exists for. Pre-launch engine architecture should design telemetry events with this hypothesis-generation methodology in mind. Telemetry isn't just for ops monitoring — it's the engine's empirical-validation instrument at scale.

**Composition with Pi-LLM-proxy architecture (per `canonical/story/2026-05-30-pi-llm-proxy-architecture-recognition.md`):** telemetry aggregation + analysis can run on Pi infrastructure post-launch. Composes with the centralized Pi LLM proxy pattern.

#### 2.4.3 Community-derived telemetry — ingest architecture

Reincarnated-community emergence at the player-names-experience layer produces vocabulary, build guides, social discussion that the engine should ingest as substrate-led hypothesis input. Three ingest channels:

**Channel A — Reincarnated-hosted community sites:**

| Source | Hypothesis signal | Ingest method |
|---|---|---|
| Reincarnated-hosted forums | Community vocabulary emergence; build discussion; archetype labeling | Direct DB query (we own the data) |
| Reincarnated-hosted wiki | Community-authored guides; canonical content as community sees it | Direct query + parsing |
| Reincarnated-hosted build hub | Build submission + rating patterns; community-favored builds | Direct query + statistical analysis |

**Channel B — Third-party community sites (if/when they emerge):**

| Source | Hypothesis signal | Ingest method |
|---|---|---|
| Maxroll-equivalent (if exists) | Tier-list ratings + structured build analysis | Legolas Mode B crawl (per existing methodology); subject to robots.txt + rate-limiting |
| Mobalytics-equivalent (if exists) | Build analysis + tier ratings | Same |
| Reddit r/reincarnated (if exists) | Community discourse vocabulary; community archetype labeling | Reddit API (per existing legolas methodology) |
| Discord community servers | Real-time discussion; emergent vocabulary | Discord API (if community grants access) |

**Channel C — Distributed community content:**

| Source | Hypothesis signal | Ingest method |
|---|---|---|
| Community-authored blogs | Long-form build analysis; designer-vocabulary intersection | Legolas Mode B crawl |
| Social posts (Twitter/X/Reddit/etc.) | Real-time sentiment; emergent vocabulary; community-emergent classifications | Social media API (per platform terms) |
| Streamer / video content | Build demonstration; per-character feel discussion | Manual + LLM analysis of transcripts (post-launch ops) |

**Architectural compositions:**
- Pi infrastructure hosts ingest pipelines (composes with Pi-LLM-proxy + future Postgres recognition)
- Star-lord seam handles ingest tooling (composes with existing Phase 5 LLM call infrastructure)
- Legolas Mode B methodology extends to Reincarnated-community crawling (substrate-led research applied to our own community)
- Elrond seam curates community-derived data (per existing data steward role)

#### 2.4.4 Substrate-led discipline at the player-experience layer (post-launch)

The designer-writes-substrate / player-names-experience principle (`canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`) applies fractally to post-launch:

| Layer | Pre-launch | Post-launch |
|---|---|---|
| Designer-writes-substrate | Substrate library + canonical vocabulary + BC axes | Same; substrate doesn't change because players exist |
| Player-names-experience | Genre community research (other games' player-names-experience) | + Reincarnated community-names-experience (our players' emergent vocabulary) |

Post-launch, the player-experience layer has substantially more data. The methodology consumes that data via Channels A + B + C with the same substrate-led discipline (community vocabulary votes; engine consumes post-emergence; designer doesn't pre-impose).

#### 2.4.5 Pre-launch architectural decisions this surfaces

To support the multi-source methodology, pre-launch decisions are needed:

| Decision | Owner | Pre-launch lock |
|---|---|---|
| What telemetry events to capture (initial set) | star-lord + gandalf + gamora | Pre-soft-launch |
| Telemetry data model + retention policy | star-lord + jack-ryan | Pre-soft-launch |
| Player privacy + GDPR considerations | jack-ryan + Matt | Pre-launch |
| Reincarnated-hosted community site architecture | Matt + future engineer | Pre-launch + post-launch evolution |
| Community ingest pipeline architecture | star-lord + Pi infrastructure | Mid-development; composes with Pi recognition records |
| Substrate-led discipline applied to player data | gandalf + jack-ryan | Continuous; canonical write candidate when ready |

These are forward-looking architectural calls. The hypothesis-flow methodology landing now anticipates them; specific implementations defer to appropriate timing per the recognition-validate-commit discipline.

---

## 3. The mathematical cell — what represents a hypothesis

A **mathematical cell** is one unit of pattern-library content. It represents a single hypothesized build-defining pattern. Cells are the atomic units of the library; they compose into pattern-clusters (multiple cells that frequently co-occur in build-defining outcomes); cluster compositions inform generation logic.

### 3.1 Cell metadata fields

| Field | Type | Definition |
|---|---|---|
| `cell_id` | UUID | Unique identifier; immutable across cell lifecycle |
| `cell_name` | str | Human-readable cell name (Pattern B authoring); e.g., "Magic-Find-Push-Magery" |
| `cell_status` | enum | `PROVISIONAL` / `PLAYTEST-CONFIRMED` / `LIBRARY-LOCKED` / `REFUTED` / `RETIRED` |
| `cell_version` | int | Iteration count of cell refinement |
| `cell_authoring_date` | date | When cell was first proposed |
| `cell_graduation_dates` | dict | Status-transition dates (PROVISIONAL→CONFIRMED→LOCKED) |
| `cell_hypothesis_source` | str | Community research / playtest finding / engineering insight / cross-cell composition |

### 3.2 Substrate-axis coordinates (Layer 1; designer-writes)

These fields specify which engine-substrate region the cell occupies. Cells may specify exact values OR ranges OR distributional preferences.

| Field | Source | Notes |
|---|---|---|
| `bc_axis_signature` | 8-vector (BC tuple) | Per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`; cell may specify exact tuple, modal values per axis, or distribution |
| `cultural_lineage` | 14-enum | `weapon_knowledge_entries.cultural_lineage_canonical` |
| `historical_period` | 9-enum | `historical_period_canonical` |
| `register` | 6-enum | `register_canonical` |
| `weapon_type_family` | 6-enum | `weapon_type_family` |
| `kit_architecture` | enum: `single_element` / `hybrid_2_element` | Per § 1.7; determines per-skill flavor judgment scope (3-option vs 15-option) |
| `kit_primary_element_1` | 8-enum (canonical) | The canonical primary element; ALWAYS present |
| `kit_primary_element_2` | 8-enum (canonical) OR null | Only present for `hybrid_2_element` kits |
| `kit_sub_element_1` | from P1's flavor pool | Sub-element drawn from primary 1's flavor pool (NOT from full canonical 2.5); per WS1A.3 |
| `kit_sub_element_2` | from P2's flavor pool OR null | Only present for hybrid; drawn from primary 2's flavor pool |
| `attribute` | STR / DEX / INT / WIS | Per `attribute-system-2026-05-24.md` (VIT deferred) |
| `t4_strategy` | 6 current + 15 proposed = 21 | Per doc 47 § 4.6 + § 11 proposed; cell may target specific T4 or T4-family |
| `investment_profile` | low / mid / max | Per doc 51 Patterns 1+2 |

### 3.3 Mechanism-axis coordinates (revised iter 3: three-layer treatment per § 1.4.1)

Specifies the cell's mechanism coordinates across the three-layer treatment: Layer 1 (player-value axes; P1-P5) + Layer 2 (mechanism-structural dimensions) + Layer 3 (observational family descriptors).

**Layer 1 — Player-value axes (P1-P5; substrate-targetable):** see fields below (`mechanism_p1_score` through `mechanism_p5_score`).

**Layer 2 — Mechanism-structural dimensions (substrate-targetable; per § 19.2 of HTML doc):**

| Field | Type | Notes |
|---|---|---|
| `mechanism_magnitude_pattern` | enum: `transformative` / `percentage` / `fixed-power` / `flat-stat` | How the mechanism delivers its effect quantitatively. Transformative = type/axis change (e.g., life→ES); percentage = +X% multiplier; fixed-power = unique-item-class fixed effect; flat-stat = additive constant. |
| `mechanism_stackability` | enum: `single-instance` / `additive` / `multiplicative` | How instances of the mechanism combine when stacked. Single = one per slot; additive = N copies sum; multiplicative = N copies multiply. |
| `mechanism_trigger` | enum: `always-on` / `on-event` / `on-condition` / `on-cooldown` | When the mechanism's effect fires. Always-on = passive; on-event = trigger like on-kill; on-condition = while-active threshold; on-cooldown = periodic refresh. |
| `mechanism_scaling_pattern` | enum: `with-item-power` / `with-investment` / `with-skill-level` / `fixed` | What the mechanism's magnitude scales against. Item-power = unique-class scaling; investment = multiplicative-with-build-investment; skill-level = with-skill-progression; fixed = no scaling. |

**Layer 3 — Observational family descriptors (descriptive flags only; NOT substrate-targetable):**

| Field | Type | Notes |
|---|---|---|
| `observed_family_similarity` | list of A-G | Post-hoc characterization — which genre families this cell's mechanism resembles structurally. Computed at manifestation/output time; NOT a generation target. |
| `family_similarity_confidence` | dict | Per-family-flag confidence score from observational analysis (e.g., `{"B": 0.85, "E": 0.42}`). |

**Composition and signatures (unchanged):**

| Field | Source | Notes |
|---|---|---|
| `mechanism_p1_score` | 0 / 0.5 / 1 | Identity-axis transformation |
| `mechanism_p2_score` | 0 / 0.5 / 1 | Multiplicative composition |
| `mechanism_p3_score` | 0 / 0.5 / 1 | System-substitution |
| `mechanism_p4_score` | 0 / 0.5 / 1 | **Creation-moment memorability** (Matt 2026-06-01 refinement per § 1.3.1) — measures predicted memorability of the character creation / Spirit discovery / emergent-kit-concept-reveal moment for characters embodying this cell. NOT genre-style in-game acquisition (which Reincarnated structurally lacks). P4=1 means the emergent kit concept is genre-recognizable AND creation moment is identity-grounding (e.g., Necromancer / Death Knight emergence); P4=0 means generic / approachable archetype with low creation-moment specificity (Wanderer-style; intentionally low and correct). |
| `mechanism_p5_score` | 0 / 0.5 / 1 | Composition unlock |
| `mechanism_total_score` | calculated | Sum (NOT averaged — multiplicative gestalt per § 22.5) |
| `mechanism_relationship_vector` | enum | **Matt 2026-05-31 framing**: structural relationship between component mechanisms — `orthogonal-90` / `inverse-180` / `synergistic-0` / `complementary-270` / `composite` |
| `damage_signature` | str | What mechanism delivers kill speed; e.g., "burst-on-aspect-assembly" / "sustained-multiplicative-aura" / "execution-window-trigger" |
| `defense_signature` | str | What mechanism delivers survival; e.g., "ES-transformation-CI" / "evasion-stacking" / "armor-flat-mitigation" / "lifesteal-on-hit" |
| `mobility_signature` | str | Speed / clear pattern; e.g., "teleport-enabling-aspect" / "passive-movement-speed-stack" / "skill-mobility-on-cooldown" |

### 3.4 Mechanical performance fields

Specifies the predicted gauntlet / playtest behavior at hypothesis time.

| Field | Type | Notes |
|---|---|---|
| `kpm_target_low_plane` | int | Kills per minute target at low-power plane (L1-12) |
| `kpm_target_mid_plane` | int | KPM at mid-power plane (L13-25 or L26-38; per power-curve granularity) |
| `kpm_target_high_plane` | int | KPM at high-power plane (L39-50) |
| `multi_format_winning_criteria` | dict | Which encounter formats must succeed: e.g., `{"swarm": true, "boss_single": true, "elite_trio": true, "endless_wave": false}` |
| `power_plane_validity` | list | Which power planes the pattern must hold across; minimum 3 per Matt framing |
| `failure_mode_comparison_target` | str | Description of what character should NOT exhibit this pattern; the failure-mode playtest counter-example |

### 3.5 Experiential-axis coordinates (Layer 2; player-names-experience; revised iter 4 per § 1.8)

Specifies the player-experience profile the cell targets. **Iter 4 refinement (Matt 2026-06-01)**: the 6 primary archetype labels decomposed into multi-axis coordinates per § 1.8.1; cells specify CONTINUOUS scores along orthogonal axes rather than single-label categorical assignment.

**Identity axes (substrate-targetable; specialize-and-differentiate per § 1.8.2):**

| Field | Type | Notes |
|---|---|---|
| `target_pattern_bossing_score` | 0-10 continuous | Predicted Bossing axis score (single-strong-target combat optimization) |
| `target_pattern_speedfarming_score` | 0-10 continuous | Predicted Speedfarming axis score (many-weak-target combat optimization) |
| `depth_breadth_push_score` | 0-10 continuous | Predicted Push axis score (deep specialization into one content type) |
| `depth_breadth_generalist_score` | 0-10 continuous | Predicted Generalist axis score (broad coverage across many content types) |

**Viability axes (substrate-targetable; universal-adequate-threshold per § 1.8.2):**

| Field | Type | Notes |
|---|---|---|
| `survivability_score` | 0-10 continuous; gate at ≥X threshold | Per Maxroll 5-axis rating; viability axis — cells below gate threshold fail viability regardless of identity-axis scores |
| `playability_score` | 0-10 continuous; gate at ≥X threshold | Per Maxroll 5-axis rating; viability axis |
| `leveling_viability_score` | 0-10 continuous; gate at ≥X threshold | **Per § 1.8.5 hypothesis (pending playtest validation):** treated as VIABILITY axis for Reincarnated (50-level scope + 85%-never-reach-endgame); cells must score adequately regardless of endgame specialization |

**Progression-Stage axis (TBD identity OR viability per § 1.8.5 playtest validation):**

| Field | Type | Notes |
|---|---|---|
| `progression_stage_target` | enum: `Leveling` / `League_Starter` / `End_Game` | Which stage of player journey the build optimizes for; treatment depends on § 1.8.5 hypothesis validation |
| `progression_stage_classification` | enum: `identity_axis` / `viability_axis_per_18_5` | Per-cell declaration of how this axis is treated; hypothesis-pending |

**Mode axis — REMOVED per § 1.8 iter 6 amendment.** Mode (HC/SC) is player-session-level choice, not kit-architecture-level property. If Reincarnated adds HC mode, HC-viability is a higher Survivability threshold (`hc_survivability_threshold_pass` viability gate within existing Viability axis treatment), NOT a kit-level field.

**Activity-Format axis (per § 1.8.7 PROPOSED player-input procedural map generation):**

| Field | Type | Notes |
|---|---|---|
| `activity_format_target` | enum: input category labels (e.g., `boss_rich` / `mob_dense` / `currency_rich` / `magic_find_rich` / `anti_faction_rich` / `mixed` / `tier_scaling_high` / `tier_scaling_broad`) | Per § 1.8.7 iter 8 PROPOSED architecture: Activity-Format values are input category identifiers within the player-input map system. Values stabilize when player-input architecture commits canonically. |

**Loot-Focus sub-axis (within Speedfarming):**

| Field | Type | Notes |
|---|---|---|
| `loot_focus_sub_axis` | enum: `Magic_Find` / `Currency_Farmer` / `Drop_Density` / `Generic` / `Not_Applicable` | Sub-axis classification within Speedfarming; Not_Applicable for non-Speedfarm cells |

**Maxroll 5-axis structured rating prediction (continuous per axis):**

| Field | Type | Notes |
|---|---|---|
| `maxroll_5axis_prediction` | dict {Bossing, Speed, Push, Survivability, Playability} → 0-10 | Per § 4.3 of HTML doc; cells predict full 5-axis profile; observation at playtest validates predictions |

**Cell shape declaration (per § 1.8.4):**

| Field | Type | Notes |
|---|---|---|
| `cell_shape_target` | enum: `Specialized` / `Hybrid` / `Generalist` / `Anti_Specialization` | Intended profile shape per § 1.8.4; declared at cell authoring; validated at playtest |

**Investment + cognitive load + accessibility (preserved from prior iteration):**

| Field | Type | Notes |
|---|---|---|
| `investment_tier` | 5-level | Extreme / Low / Medium / High / Mageblood-required |
| `cognitive_load_target` | low / medium / high | Per § 4.6 CLI framework |
| `gear_dependency_index` | low / medium / high | Per § 4.6 GDI framework |
| `execution_skill_floor` | low / medium / high | Per § 4.6 |
| `execution_skill_ceiling` | low / medium / high | Per § 4.6 |
| `playstyle_geometry_tag` | ranged / melee / all-rounder | Per PoE-Vault community vocabulary |

**Emergent archetype label (output-time observation; NOT generation target):**

| Field | Type | Notes |
|---|---|---|
| `emergent_archetype_label` | str | Post-hoc observed label inferred from multi-axis profile dominance (e.g., "Bossing Push End Game" / "Leveling Speedfarm Generalist"); NOT a generation input; emerges from continuous axis scores via profile-dominance pattern recognition |

### 3.6 Layer 1.5 coupling-architecture markers

Specifies the coupling-architecture context the cell occupies.

| Field | Type | Notes |
|---|---|---|
| `coupling_layer_count` | int 1-6 | How many multiplicative loot-substrate layers the cell composes against; Reincarnated target ≤3 |
| `coupling_strength` | enum | `additive` / `light-multiplicative` / `heavy-multiplicative` |
| `single_axis_viability` | bool | Does the cell remain viable under single-axis specialization (LE-style) OR require composite (PoE-style)? |

### 3.7 Layer 3 vestigial-class identity (player-facing surface)

Specifies the vestigial-class label the cell's instances should carry in player-facing surface for community-vocabulary anchoring.

| Field | Type | Notes |
|---|---|---|
| `vestigial_class_label` | str | Emergent class label; e.g., "Whirlwind Barbarian" / "Magic-Find Sorceress" / "Pirate Aeromancer"; substrate-derived, NOT designer-pre-imposed; consumed by Wave A / Wave B LLM naming |
| `class_lineage_coherence_signal` | float | Cohesion-judge signal for how cleanly the cell's substrate composes into a recognizable vestigial-class identity |

### 3.8 Validation state fields

Tracks the cell's progression through Stages 4-5.

| Field | Type | Notes |
|---|---|---|
| `playtest_cycles_completed` | int | Total playtests against this cell |
| `playtest_results` | list | Per-cycle pass/fail with notes |
| `failure_mode_playtest_completed` | bool | Has absence-of-pattern playtest been done? |
| `failure_mode_playtest_result` | str | Did the comparison character correctly NOT exhibit the pattern? |
| `cross_plane_validation` | dict | Per-power-plane validation results |
| `cross_variation_validation` | dict | Per-character-variation results within power plane |
| `graduation_decision` | str | Authorization for status transition |
| `graduation_authorizer` | str | gandalf / Matt / jack-ryan |

### 3.9 Cell relationships

Cells don't exist in isolation; they compose into clusters and oppose other cells.

| Field | Type | Notes |
|---|---|---|
| `co_occurring_cells` | list | Other cells frequently observed together in generation output OR playtest evidence |
| `opposing_cells` | list | Cells that structurally exclude each other (e.g., Bossing-Push vs Speedfarm-Clear) |
| `parent_cluster` | str | Which pattern-cluster does this cell belong to (if any)? |
| `composition_strength` | float | How strong is the cell's tendency to co-occur with cluster siblings? |

### 3.10 Per-skill flavor judgment fields (per § 1.7 WS1A.4)

Specifies the cell's prediction for how per-skill bounded LLM judgment distributes across the kit's substrate-declared element scope.

**For single-element kit cells:**

| Field | Type | Notes |
|---|---|---|
| `skill_flavor_alignment_distribution` | dict | Predicted distribution across `{primary, sub, blend}` for the cell's typical skill composition; e.g., `{primary: 2, sub: 1, blend: 2}` for 5 skills |
| `predicted_emergent_kit_concept` | str | What kit concept the LLM should produce at Wave B per-kit identity step; e.g., "Necromancer" / "Stoneward" / etc. |

**For hybrid 2-element kit cells:**

| Field | Type | Notes |
|---|---|---|
| `skill_flavor_alignment_distribution` | dict | Predicted distribution across the 15-subset space `{P1, P2, S1, S2, {P1,P2}, ..., {P1,P2,S1,S2}}`; same skill-count total |
| `predicted_emergent_kit_concept` | str | What kit concept the LLM should produce; hybrids unlock richer concepts (e.g., "Death Knight" / "Bone Witch" / "Tomb Warden" / "Soul Reaver") |
| `cross_primary_blend_count` | int | Cells targeting specifically cross-primary blends (e.g., P1+S2 or P2+S1 subsets); higher counts predict more unusual emergent identities |

**Validation field (shared across single/hybrid):**

| Field | Type | Notes |
|---|---|---|
| `actual_emergent_concept_observed` | str | What Wave B LLM actually produced at identity-finalization; compared to `predicted_emergent_kit_concept` for cell validation |
| `concept_match_score` | float 0-1 | Cohesion between predicted and observed emergent concept; per playtest signal on identity coherence |

---

## 4. The flag enum — what gets attached to generated characters

Flags are the engine-side instrument that connects pattern-library cells to generated characters. When the engine generates a character, the cohesion-judge or post-generation analyzer evaluates which cells the character matches and attaches the corresponding flag set. Downstream stages act on flags.

### 4.1 Experiential-axis flags (axis-grouped families per § 1.8 multi-axis architecture; revised iter 4)

**Iter 4 refinement (Matt 2026-06-01):** the flat `PRIMARY_*` enum from prior iterations is RETIRED. Per § 1.8.1 multi-axis decomposition, flags now group by orthogonal axis. A cell carries flags from MULTIPLE axis families simultaneously (one flag per Identity axis it specializes on; viability flags if scored; Mode flag; sub-axis flag if applicable).

**Target-Pattern axis flags (Identity axis):**

| Flag | Notes |
|---|---|
| `TARGET_PATTERN_BOSSING` | Single-strong-target combat specialization; cell scores ≥7/10 on `target_pattern_bossing_score` |
| `TARGET_PATTERN_SPEEDFARMING` | Many-weak-target combat specialization; cell scores ≥7/10 on `target_pattern_speedfarming_score` |
| `TARGET_PATTERN_BALANCED` | No dominant target-pattern; both scores in 4-6 range |

**Depth-vs-Breadth axis flags (Identity axis):**

| Flag | Notes |
|---|---|
| `DEPTH_PUSH` | Deep specialization into one content type; cell scores ≥7/10 on `depth_breadth_push_score` |
| `BREADTH_GENERALIST` | Broad coverage across many content types; cell scores ≥7/10 on `depth_breadth_generalist_score` |
| `DEPTH_BREADTH_BALANCED` | Both scores in 4-6 range |

**Progression-Stage axis flags (Identity OR Viability per § 1.8.5 hypothesis):**

| Flag | Notes |
|---|---|
| `PROGRESSION_LEVELING` | Optimized for Levels 1-50 journey |
| `PROGRESSION_LEAGUE_STARTER` | Self-sufficient endgame-from-scratch capability |
| `PROGRESSION_END_GAME` | True endgame specialization (per § 1.8 hypothesis, only ~15% of players reach this; cells targeting this are end-game-tier-investment) |
| `PROGRESSION_LEVELING_VIABILITY_GATE` | Per § 1.8.5 hypothesis: this cell adequately covers Leveling-axis viability gate; gate-pass marker |

**Mode axis flags — REMOVED per § 1.8 iter 6 amendment.** HC-viability (if HC mode added) handled as `VIABILITY_HC_SURVIVABILITY_PASS` within Viability axis treatment below.

**Viability axis flags (gate markers):**

| Flag | Notes |
|---|---|
| `VIABILITY_SURVIVABILITY_PASS` | Cell scores ≥X on Maxroll Survivability axis (gate threshold) |
| `VIABILITY_PLAYABILITY_PASS` | Cell scores ≥X on Maxroll Playability axis |
| `VIABILITY_LEVELING_PASS` | Per § 1.8.5 hypothesis: cell scores ≥X on Leveling-axis viability gate |
| `VIABILITY_HC_SURVIVABILITY_PASS` | (Conditional — if Reincarnated adds HC mode) Cell scores ≥X+threshold on Survivability for HC viability gate; higher threshold than baseline VIABILITY_SURVIVABILITY_PASS |
| `VIABILITY_GATE_FAILED` | Cell fails at least one viability gate; flagged for review or refutation |

**Loot-Focus sub-axis flags (within Speedfarming):**

| Flag | Notes |
|---|---|
| `LOOT_MAGIC_FIND_FOCUSED` | IIR-targeted (legacy in D4; alive in PoE2) |
| `LOOT_CURRENCY_FARMER` | PoE-specific currency-stack farming |
| `LOOT_DROP_DENSITY_FOCUSED` | High-mob-density loot farming |
| `LOOT_GENERIC_SPEEDFARM` | No loot specialization within Speedfarm |

**Activity-Format axis flags (per § 1.8.7 PROPOSED player-input procedural map generation; iter 8):**

| Flag | Notes |
|---|---|
| `ACTIVITY_FORMAT_BOSS_RICH` | Cell targets boss-input maps (Bossing endgame specialization) |
| `ACTIVITY_FORMAT_MOB_DENSE` | Cell targets mob-density-input maps (Speedfarming endgame specialization) |
| `ACTIVITY_FORMAT_CURRENCY_RICH` | Cell targets currency-rich input maps (loot-currency sub-axis focus) |
| `ACTIVITY_FORMAT_MAGIC_FIND_RICH` | Cell targets magic-find-rich input maps (loot-magic-find sub-axis focus) |
| `ACTIVITY_FORMAT_ANTI_FACTION_RICH` | Cell targets anti-faction-input maps (cascade architecture composition) |
| `ACTIVITY_FORMAT_MIXED` | Cell performs across mixed input compositions (Generalist) |
| `ACTIVITY_FORMAT_TIER_SCALING_HIGH` | Cell targets high-tier input combinations (Push specialization; infinite-tower-equivalent depth) |
| `ACTIVITY_FORMAT_TIER_SCALING_BROAD` | Cell targets broad-tier coverage (sustained-performance Generalist) |
| `ACTIVITY_FORMAT_PRE_ARCHITECTURE_COMMITMENT` | Marker flag for cells authored BEFORE player-input architecture commits canonically; reactivate-on-commit |

**Emergent archetype labels (OBSERVATIONAL only; output-time post-hoc):**

| Flag | Notes |
|---|---|
| `EMERGENT_LABEL_DECLARED` | Post-hoc archetype label inferred from multi-axis profile dominance (e.g., "Bossing Push End Game"); NOT a generation target; emerges from continuous axis scores |
| `EMERGENT_LABEL_AMBIGUOUS` | Multi-axis profile produces no dominant archetype label; cell is over-generalized OR identity-anchor (Anti-specialization shape per § 1.8.4) |

### 4.2 Sub-axis flags (within primary archetype)

| Flag | Notes |
|---|---|
| `SUB_MAGIC_FIND` | Within Speedfarm or Currency Farmer; IIR-stat-targeted |
| `SUB_CLEAR_SPEED` | PoE-Vault verbatim sub-axis within Speedfarm |
| `SUB_BUDGET_EXTREME` | Investment-tier 1 (within Speedfarm or League Starter) |
| `SUB_MAGEBLOOD_REQUIRED` | Investment-tier 5 (within Push or Endgame) |
| `SUB_CRIT_STACKING` | Within damage-signature mechanism family |
| `SUB_ES_TRANSFORMATION` | Within defense-signature; CI-pattern |
| `SUB_ASPECT_ASSEMBLY` | Family B composition pattern |

### 4.3 Investment-tier flags (5-level)

| Flag | Maxroll PoE | LE | D4 | Notes |
|---|---|---|---|---|
| `INVESTMENT_EXTREME_BUDGET` | "Extreme Budget" (Surface 1) | — | — | 5th investment tier; barely-functional / theoretical |
| `INVESTMENT_LOW` | "Low" | "Budget" | "Pre-Item-Power-925" | Bare-minimum functional |
| `INVESTMENT_MEDIUM` | "Above Average" | "Mid" | "Mid-Item-Power" | Most-builds-most-of-the-time |
| `INVESTMENT_HIGH` | "Difficult" | "Late" | "Maxroll-Tier" | Endgame-optimized |
| `INVESTMENT_MAGEBLOOD_REQUIRED` | "Mageblood-required" | "Whisper-tier" | "Mythic-Required" | Beyond-realistic / theoretical |

### 4.4 Variant-axis flag (universal binary)

| Flag | Position | Notes |
|---|---|---|
| `VARIANT_SPEEDFARM` | -1.0 polarity | Clear-rate × loot-find optimization |
| `VARIANT_BALANCED` | 0.0 position | Generalist; no strong polarity |
| `VARIANT_PUSH` | +1.0 polarity | Content-depth × specialization-peak |

Universal across 4 games per research sprint findings (37% of all multi-variant builds).

### 4.5 Coupling-architecture flags (Layer 1.5)

| Flag | Notes |
|---|---|
| `COUPLING_LIGHT_3_LAYER` | LE-style; recommended for Reincarnated |
| `COUPLING_MEDIUM_4_5_LAYER` | D4 / between LE and PoE |
| `COUPLING_HEAVY_6_PLUS_LAYER` | PoE-style; NOT recommended for Reincarnated |
| `COUPLING_SINGLE_AXIS_VIABLE` | Single-axis archetype remains economically viable |
| `COUPLING_COMPOSITE_REQUIRED` | Composite-axis required for economic viability |

### 4.6 Substrate-signature flags

| Flag | Notes |
|---|---|
| `SUBSTRATE_<BC_TUPLE_HASH>` | Hash of the cell's BC tuple signature; enables clustering of substrate-similar characters |
| `SUBSTRATE_<CULTURAL_LINEAGE>` | One per cultural lineage (14-enum) |
| `SUBSTRATE_<HISTORICAL_PERIOD>` | One per period (9-enum) |
| `SUBSTRATE_<REGISTER>` | One per register (6-enum) |
| `SUBSTRATE_<WEAPON_TYPE_FAMILY>` | One per weapon family (6-enum) |
| `SUBSTRATE_<ELEMENT>` | One per canonical element (8-enum) + flavor elements |
| `SUBSTRATE_<ATTRIBUTE>` | STR / DEX / INT / WIS |

### 4.7 T4 strategy flags

| Flag | Notes |
|---|---|
| `T4_<STRATEGY_NAME>` | One per T4 strategy (6 current + 15 proposed = 21) |
| `T4_BUILD_DEFINING_HIGH` | Cell's T4 scores 4-5/5 on 5-property framework |
| `T4_BUILD_DEFINING_MEDIUM` | T4 scores 2-3/5 |
| `T4_IDENTITY_ANCHOR` | T4 scores 0-1/5 (intentional anti-build-defining; Wanderer-style) |

### 4.8 Mechanism family flags (OBSERVATIONAL only per § 1.4.1 Layer 3 — revised iter 3)

**Status:** these flags are **descriptive output-time tags**, NOT substrate-targetable generation inputs. Per the three-layer treatment in § 1.4.1, generation operates on Layer 1 (P1-P5 player-value axes) + Layer 2 (mechanism-structural dimensions per § 3.3 Layer 2 fields). Family flags are attached AFTER manifestation as post-hoc observation of "this cell's mechanism structurally resembles genre Family X."

| Flag | Family | Genre exemplars |
|---|---|---|
| `OBSERVED_RESEMBLES_FAMILY_A` | Intra-skill transformation | LE Specialization / PoE Support / LA Tripod |
| `OBSERVED_RESEMBLES_FAMILY_B` | Extractable / imbue-able power | D2 Runewords / D3 Cube / D4 Aspect |
| `OBSERVED_RESEMBLES_FAMILY_C` | Class-identity combo | GD Dual Mastery / D3 Class Set / LA Engraving |
| `OBSERVED_RESEMBLES_FAMILY_D` | Passive-tree capstone | PoE Keystone / Reincarnated T4 |
| `OBSERVED_RESEMBLES_FAMILY_E` | Item-slot anchor | Mageblood / Headhunter / Enigma |
| `OBSERVED_RESEMBLES_FAMILY_F` | Consumable / inventory-resident | D2 Charms / LE Idols |
| `OBSERVED_RESEMBLES_FAMILY_G` | Proc-attached celestial | GD Devotion / PoE Watcher's Eye |
| `OBSERVED_NOVEL_NO_GENRE_ANALOG` | Reincarnated-native mechanism not resembling any existing family | NEW — Reincarnated may produce mechanisms with no genre analog; this flag captures that case |

### 4.9 5-property score flags

| Flag | Notes |
|---|---|
| `P1_IDENTITY_AXIS_HIGH` | Cell's P1 score is 1.0 |
| `P1_IDENTITY_AXIS_PARTIAL` | P1 score 0.5 |
| `P2_MULTIPLICATIVE_COMPOSITION_HIGH` | P2 score 1.0 |
| `P3_SYSTEM_SUBSTITUTION_HIGH` | P3 score 1.0 |
| `P4_ACQUISITION_MEMORABILITY_HIGH` | P4 score 1.0 or 2.0 (high-friction acquisition) |
| `P5_COMPOSITION_UNLOCK_HIGH` | P5 score 1.0 |
| `BUILD_DEFINING_CANONICAL` | 4-5 properties high; canonical "build came online" candidate |
| `BUILD_DEFINING_SUB_AXIS` | 2-3 properties high; significant build choice |
| `BUILD_DEFINING_ABSENT` | 0-1 properties high; routine progression OR intentional identity-anchor |

### 4.10 Power-plane flags

| Flag | Plane | Notes |
|---|---|---|
| `PLANE_L1_12` | Low | Early-game; leveling stages |
| `PLANE_L13_25` | Mid-low | Mid-leveling |
| `PLANE_L26_38` | Mid-high | Late-leveling / early-endgame |
| `PLANE_L39_50` | High | Endgame-cap |
| `PLANE_HOLDS_ACROSS_ALL` | Cross-plane | Pattern holds at all 4 planes |
| `PLANE_HIGH_ONLY` | Endgame-locked | Pattern only valid at L39-50 |

### 4.11 Validation-status flags

| Flag | Notes |
|---|---|
| `VALIDATION_PROVISIONAL` | Hypothesis posted; no playtest yet |
| `VALIDATION_PLAYTEST_CONFIRMED_LOW` | 1 playtest cycle confirmed |
| `VALIDATION_PLAYTEST_CONFIRMED_CROSS_PLANE` | 3+ playtest cycles across power planes confirmed |
| `VALIDATION_PLAYTEST_CONFIRMED_FAILURE_MODE` | Failure-mode comparison confirmed |
| `VALIDATION_LIBRARY_LOCKED` | All graduation criteria met; cell encoded into generation logic |
| `VALIDATION_REFUTED` | Playtest evidence refutes hypothesis |
| `VALIDATION_RETIRED` | Cell deprecated (e.g., substrate refactor invalidated coordinates) |

### 4.12 Cognitive-load + accessibility flags (per § 4.6 of HTML doc)

| Flag | Notes |
|---|---|
| `COGNITIVE_LOAD_LOW` | One-button / passive-stack / simple-rotation |
| `COGNITIVE_LOAD_MEDIUM` | Standard rotation + situational decisions |
| `COGNITIVE_LOAD_HIGH` | Multi-skill rotation + reactive decisions + positional awareness |
| `GEAR_DEPENDENCY_LOW` | Functional on common gear |
| `GEAR_DEPENDENCY_HIGH` | Requires specific item or set |
| `EXECUTION_FLOOR_LOW` | Approachable; works without execution skill |
| `EXECUTION_CEILING_HIGH` | Rewards execution mastery |

### 4.13 Kit architecture flags (per § 1.7 WS1A.4)

| Flag | Notes |
|---|---|
| `KIT_SINGLE_ELEMENT` | Kit has 1 primary element + 1 sub-element from primary's flavor pool; per-skill judgment scope = 3 options |
| `KIT_HYBRID_2_ELEMENT` | Kit has 2 primary elements + 2 sub-elements (each from respective primary's pool); per-skill judgment scope = 15 options |

### 4.14 Per-skill flavor judgment flags (per § 1.7 WS1A.4)

Single-element kit per-skill alignment:

| Flag | Notes |
|---|---|
| `SKILL_ALIGNMENT_PRIMARY` | Skill aligns with kit's primary element only |
| `SKILL_ALIGNMENT_SUB` | Skill aligns with kit's sub-element only |
| `SKILL_ALIGNMENT_BLEND` | Skill blends primary + sub |

Hybrid 2-element kit per-skill alignment (15-subset space):

| Flag | Notes |
|---|---|
| `SKILL_ALIGNMENT_P1` | Skill aligns with primary element 1 only |
| `SKILL_ALIGNMENT_P2` | Skill aligns with primary element 2 only |
| `SKILL_ALIGNMENT_P1_P2` | Skill blends both primaries |
| `SKILL_ALIGNMENT_S1` | Skill aligns with sub-element 1 only |
| `SKILL_ALIGNMENT_S2` | Skill aligns with sub-element 2 only |
| `SKILL_ALIGNMENT_S1_S2` | Skill blends both sub-elements |
| `SKILL_ALIGNMENT_P1_S1` | Skill blends primary 1 + sub 1 (same-primary blend) |
| `SKILL_ALIGNMENT_P2_S2` | Skill blends primary 2 + sub 2 (same-primary blend) |
| `SKILL_ALIGNMENT_P1_S2` | Skill blends primary 1 + sub 2 (cross-primary blend) |
| `SKILL_ALIGNMENT_P2_S1` | Skill blends primary 2 + sub 1 (cross-primary blend) |
| `SKILL_ALIGNMENT_P1_P2_S1` | Triple blend (excludes S2) |
| `SKILL_ALIGNMENT_P1_P2_S2` | Triple blend (excludes S1) |
| `SKILL_ALIGNMENT_P1_S1_S2` | Triple blend (excludes P2) |
| `SKILL_ALIGNMENT_P2_S1_S2` | Triple blend (excludes P1) |
| `SKILL_ALIGNMENT_FULL_QUAD` | Full {P1, P2, S1, S2} quad blend |

Per-kit emergent identity:

| Flag | Notes |
|---|---|
| `EMERGENT_KIT_CONCEPT_DECLARED` | Wave B LLM emerged a recognizable kit concept (Necromancer / Druid / Stoneward / Death Knight / etc.) |
| `EMERGENT_KIT_CONCEPT_AMBIGUOUS` | Wave B LLM produced ambiguous output; identity coherence weak |

### 4.15 Layer 2 mechanism-structural flags (per § 1.4.1 — substrate-targetable)

These flags ARE substrate-targetable generation inputs. Per the three-layer treatment, Layer 2 mechanism-structural dimensions are what cells specify as generation targets at the mechanism layer.

Magnitude-pattern flags:

| Flag | Notes |
|---|---|
| `MECHANISM_MAGNITUDE_TRANSFORMATIVE` | Type / axis change (e.g., life→ES); qualitative shift |
| `MECHANISM_MAGNITUDE_PERCENTAGE` | +X% multiplier; quantitative scaling |
| `MECHANISM_MAGNITUDE_FIXED_POWER` | Unique-item-class fixed effect |
| `MECHANISM_MAGNITUDE_FLAT_STAT` | Additive constant |

Stackability flags:

| Flag | Notes |
|---|---|
| `MECHANISM_STACK_SINGLE` | One instance per slot |
| `MECHANISM_STACK_ADDITIVE` | N copies sum |
| `MECHANISM_STACK_MULTIPLICATIVE` | N copies multiply |

Trigger flags:

| Flag | Notes |
|---|---|
| `MECHANISM_TRIGGER_ALWAYS_ON` | Passive; always-active |
| `MECHANISM_TRIGGER_ON_EVENT` | Fires on event like on-kill / on-hit |
| `MECHANISM_TRIGGER_ON_CONDITION` | Active while threshold condition met |
| `MECHANISM_TRIGGER_ON_COOLDOWN` | Periodic refresh |

Scaling-pattern flags:

| Flag | Notes |
|---|---|
| `MECHANISM_SCALES_WITH_ITEM_POWER` | Unique-class scaling with item power |
| `MECHANISM_SCALES_WITH_INVESTMENT` | Multiplicative-with-build-investment |
| `MECHANISM_SCALES_WITH_SKILL_LEVEL` | With-skill-progression |
| `MECHANISM_SCALES_FIXED` | No scaling; constant magnitude |

**Composition pattern:** cells specify these flags in combination. For example, a cell targeting the "high P2 + high P3 + multiplicative-stackability + on-event-trigger + scales-with-investment" gap surfaces in § 1.4.2 carries flags `MECHANISM_STACK_MULTIPLICATIVE` + `MECHANISM_TRIGGER_ON_EVENT` + `MECHANISM_SCALES_WITH_INVESTMENT` at Layer 2 + high `mechanism_p2_score` and `mechanism_p3_score` at Layer 1. Cells composed this way drive generation toward Reincarnated-native mechanisms (no family pre-imposition) that deliver the predicted Layer 1 value through Layer 2 structural choices.

### 4.16 Cell shape flags (per § 1.8.4 multi-axis architecture)

Cell-level declaration of intended profile shape across multi-axis experiential space:

| Flag | Notes |
|---|---|
| `CELL_SHAPE_SPECIALIZED` | Dominant on 1 identity axis; minimum-adequate on viability axes; sub-dominant or absent on other identity axes. Most common cell shape; favored for identity strength; default shape. |
| `CELL_SHAPE_HYBRID` | Significant scores on 2-3 identity axes; intentional cross-axis utility (e.g., Boss-Speed dual-capability). Common for hybrid 2-element kits per § 1.7.2. |
| `CELL_SHAPE_GENERALIST` | Moderate scores across many identity axes; "do everything" archetype. Rare; high-investment-tier; PoE Mageblood-Headhunter-class extreme builds. |
| `CELL_SHAPE_ANTI_SPECIALIZATION` | Intentionally low on identity axes; high on Survivability + Playability; identity-anchor for approachable / one-button / Wanderer-style archetype. Per § 22 of HTML doc; NOT a bug. |

### 4.17 Axis-type classification flags (per § 1.8.2)

Per-axis declaration of how the axis is treated in cell scoring and generation:

| Flag | Notes |
|---|---|
| `AXIS_TYPE_IDENTITY` | Axis treated as identity-and-differentiation; cells prefer dominance pattern; per-axis specialization preferred |
| `AXIS_TYPE_VIABILITY` | Axis treated as universal-adequate-threshold; cells must score above gate threshold; minimum-viability gate applies |
| `AXIS_TYPE_SUB` | Axis treated as within-axis sub-classification of a parent axis |
| `AXIS_TYPE_PROGRESSION_STAGE_TBD` | Progression-Stage axis treatment is hypothesis-pending per § 1.8.5; either AXIS_TYPE_IDENTITY OR AXIS_TYPE_VIABILITY pending playtest validation |

**Note (iter 6 amendment):** `AXIS_TYPE_MODE` REMOVED from enum. Mode (HC/SC) is player-session-level choice; not a kit-architecture axis type.

---

## 5. Sequencing — when this work fires

### 5.1 Current state (2026-05-31)

- Cycle 14 wave-5 in flight (gauntlet sim work; cycle-13-gauntlet-sim-results recompute series)
- Pi-middleware Phase 1 closed ✅
- PC-side infrastructure scaffolded ✅ (mount + SSH + headless Unreal proven)
- Workstream 1A queued (substrate axis expansion + Phase 5 LLM amendment + flavor wiring)
- Manifestation milestone identified as recognition; canonical record not yet authored

### 5.2 Gate sequence

```
Cycle 14 wave-5 close
    ↓
WS1A architectural foundations land
    │
    ├── WS1A.1 Substrate axis expansion (per § 4-9 of HTML doc; experiential archetype + investment tier + Maxroll 5-axis + playstyle geometry tags + GDI + CLI + skill-floor/ceiling + skill-role distribution)
    │   ├── PARTIAL retroactive on wave-5 snapshot (axes can be inferred or extracted)
    │   └── FULL validation requires Cycle 15+ proper generation
    ├── WS1A.2 Phase 5 LLM call architecture amendment (two-stage: skills + flavor BEFORE cohesion clustering)
    ├── WS1A.3 Flavor element vocabulary wiring (per-kit sub-element selection from PRIMARY's flavor pool; canonical 2.5)
    └── WS1A.4 Per-skill flavor judgment (bounded: single-element = 3 options; hybrid 2-element = 15 options; per § 1.7)
    ↓
Manifestation milestone Phase 1 — IDENTITY FINALIZATION (retroactive on wave-5 snapshot archive)
    │
    │ Starts AFTER Phase 4 archive insertion of wave-5 snapshot (the gauntlet-emitted piece).
    │ Substrate stays substrate; identity layer regenerates via WS1A-amended Phase 5+ pipeline.
    │
    │ Pipeline placement (per § 1.7.8 Option A — iter 5 lock): Phase 5+ LLM naming
    │ fires on the ~30 Pareto-reduced kits, NOT on ~650 pre-Pareto kits. Cost
    │ efficient (~$1.50-4.50 per cycle vs $30-90); cohesion judge n=30 sufficient;
    │ retroactive runs cheaper. Option B (pre-Pareto LLM naming with faction-aware
    │ reduction) deferred until playtest evidence of natural-faction-loss supports.
    │
    ├── Re-run Phase 5a' (per-skill flavor judgment, bounded per § 1.7) on ~30 snapshot kits
    ├── Re-run Phase 5a (skill naming consuming per-skill flavor judgments)
    ├── Re-run Phase 5b cohesion judge clustering (richer semantic inputs; ~3-5 emergent factions on n=30)
    ├── Re-run Wave A faction naming
    ├── Re-run Wave B per-kit identity naming
    ├── Snapshot archive transitions: "wave-5 PROVISIONAL (gauntlet metrics)" → "wave-5 PROVISIONAL + IDENTITY-FINALIZED"
    └── Single Phase 5+ re-run pass; ~1-2 weeks horizon; ~150-210 LLM calls total
    ↓
Manifestation milestone Phase 2 — REALIZATION in Unreal
    │
    │ Binds Phase 1 identity-finalized JSON output. Chosen character carries final
    │ skill names, kit identity, faction context for playtest validity.
    │
    ├── Chosen manifestation character with finalized identity (e.g., "Necromancer" emergent from shadow + umbra)
    ├── Modular character architecture established (stock mannequin + armor pieces + materials)
    ├── Initial component library (5-10 base bodies + 50-100 heads + 200-500 armor + 100-300 weapons + 100-200 accessories per modular character research)
    ├── Spirit-form sculpting prototype
    ├── Manifestation transition (Spirit → realized character)
    ├── Basic moveset + combat interaction
    ├── Glimpse of level-50 future-self
    └── Failure-mode comparison character realized (also identity-finalized via Phase 1)
    ↓
PATTERN LIBRARY PHASE A — Pattern Discovery Infrastructure
    │
    ├── Cycling-based analysis capability (separate tooling; not production)
    ├── Initial cell schema codification at engine-side (pattern_library.db or equivalent)
    └── First cell authoring (provisional; no playtest yet)
    ↓
PATTERN LIBRARY PHASE B — Initial Pattern Library
    │
    ├── First hypothesis batch authored (community-research-led)
    ├── ~10-20 provisional cells
    ├── First engineering passes (Stage 2 of hypothesis-flow)
    └── First playtest cycles (Stage 3-4)
    ↓
PATTERN LIBRARY PHASE C — Generation Logic Integration
    │
    ├── First library-locked cells encoded into generation
    ├── Production pipeline runs with partial pattern-aware generation
    └── Backward compat preserved (cells not yet locked stay PROVISIONAL; not pre-encoded)
    ↓
PATTERN LIBRARY PHASE D — Validation and Iteration
    │
    ├── Production output quality measured against pre-pattern-library baseline
    ├── Pattern library cells refined based on production evidence
    └── Hypothesis batch 2 + 3 + N continue feeding library
    ↓
PATTERN LIBRARY PHASE E — Expansion and Maintenance
    │
    ├── Substrate axis expansions trigger new pattern discovery
    ├── Library versioning + pattern-graduation history maintained
    └── Engine continues compounding value
```

### 5.3 Estimated horizon (revised 2026-06-01 per retroactive feasibility recognition)

| Phase | Start | Duration estimate |
|---|---|---|
| Wave-5 swift closure (snapshot per recognition record 2026-06-01) | NOW | days to ~2 weeks |
| WS1A foundations | Post-wave-5-close | 4-8 weeks |
| **Manifestation milestone Phase 1 (identity finalization; retroactive)** | **After WS1A** | **~1-2 weeks** |
| Manifestation milestone Phase 2 (realization in Unreal) | After Phase 1 | 3-6 months |
| Phase A infrastructure | After Phase 2 lands | 4-8 weeks |
| Phase B initial library | Concurrent with A's end | 2-4 months |
| Phase C generation integration | After B reaches ~10 locked cells | 2-4 months |
| Phase D validation + iteration | Continuous from C | Ongoing |
| Phase E expansion | Continuous | Ongoing |

**Net horizon to begin Phase A (revised):** 4-8 months from now (down from 6-12 month range pre-recognition). **Net horizon to first library-locked cells:** 9-15 months. **Net horizon to commercially-meaningful pattern library:** 18-30 months. The work is substantial but proceeds in increments; value emerges progressively as the first cells graduate.

**The horizon shortened because:**
- Wave-5 closes at snapshot, not gauntlet convergence (per 2026-06-01 recognition record)
- Manifestation Phase 1 runs retroactively on snapshot (single Phase 5+ re-run, not full regeneration)
- WS1A.1 substrate axis expansion validated PARTIALLY at manifestation (full validation defers to Cycle 15+ proper without blocking pattern library start)

### 5.4 What does NOT block this sequencing

- Phase 5 LLM call amendment specifics (those are WS1A scope; this work consumes their output)
- Specific manifestation-character choice (any of current Cycle 14 shipped characters works)
- UE seam agent role-definition authoring (gandalf authors when reincarnated-unreal becomes load-bearing; that's Manifestation Milestone time)
- Pi infrastructure Phase 2+ (Postgres, LLM proxy) — independent infrastructure work; composes with but doesn't gate this

### 5.5 What DOES block this sequencing

- Cycle 14 wave-5 close (in flight; ETA depends on simulation work)
- WS1A foundations landing (gates manifestation; gates pattern library coordinates)
- Manifestation milestone (gates playtest infrastructure; gates Stage 4 of hypothesis-flow)
- Substrate axis expansion COMPLETING — pattern cells encoded at incomplete substrate would invalidate when substrate expands; better to wait OR build a library-versioning discipline that handles substrate refactors gracefully

---

## 6. Validation methodology details

### 6.0 Three-layer playtest validation (revised 2026-06-01)

Per the recognition record `canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` + the per-skill flavor judgment refinement (§ 1.7), **playtest cycles validate THREE LAYERS simultaneously** on the same realized character:

| Layer | What playtest validates | Validation evidence |
|---|---|---|
| **Layer 1 — Hypothesis-cell patterns** | Does the cell's predicted build-defining pattern match playtest experience? | Direct hypothesis confirmation per § 6.6 graduation criteria |
| **Layer 2 — Gauntlet metric predictions** | Do gauntlet-predicted KPM, multi-format winning, cohort archetype match playtest observations? | Compare predicted vs observed KPM per power plane; compare predicted multi-format viability vs playtest experience |
| **Layer 3 — LLM naming + cohesion judge outputs + creation-moment P4** | Do the emergent skill names, kit identity, and faction context feel correct? Does "Necromancer" emerge as the kit concept consistently with what playtest reveals? **Does the creation-moment (Spirit sculpting → manifestation transition → emergent kit concept reveal) feel memorable per § 1.3.1 P4 mapping?** | Subjective playtest signal on identity coherence; failure-mode comparison test for identity distinctness; **creation-moment memorability self-report from playtest (Matt + son)** |

Three layers validated in one playtest cycle. Same instrument; three operational benefits per cycle:
- Validates pattern library cell graduation discipline
- Validates gauntlet metrics (currently provisional per 2026-06-01 recognition)
- Validates Phase 5 LLM naming + cohesion judge outputs (currently provisional pending WS1A landing + Phase 1 identity finalization)

The three layers are not separable. A character feels build-defining (Layer 1) when its skills KPM correctly (Layer 2) AND its identity reads as a coherent emergent concept (Layer 3). All three must validate for the cell to graduate.

### 6.1 Community-research-led hypothesis generation

Hypothesis batches are generated through:

1. **Empirical seed corpus consultation** — `research.db` from 2026-05-29 sprint; future sprint extensions
2. **Ongoing legolas Mode A research** — periodic research dispatches surface new community discourse patterns
3. **Matt's lived genre experience** — years of ARPG play across D2/D3/D4/PoE/PoE2/LE/GD/etc.
4. **Cross-cell composition discovery** — once initial cells graduate, observe which combinations of cells in playtest evidence suggest higher-order patterns

A hypothesis batch is typically 10-20 provisional cells covering a coherent design region (e.g., "Speedfarm-Magic-Find cluster at LE-style coupling architecture").

### 6.2 Engineering generation to produce hypothesis candidates

Per Matt 2026-05-31 pushback: this is engineering freedom. Generation parameters / vector weights / categorical flags are tuned to materialize hypothesized combinations. No substrate-led discipline binds at this stage. The engine is the engineer's instrument; tune it.

**Provisional cell** → engine produces N candidates (likely 3-10 per cell per cycle).

### 6.3 Playtest at 3+ character-level/scale planes

Per Matt 2026-05-31 framing literal: minimum 3 power planes; preferably 4 (L1-12, L13-25, L26-38, L39-50). Each plane tested with:

- **Hypothesis-bearing character** (manifested from cell candidate)
- **Failure-mode comparison character** (deliberately NOT bearing the pattern; otherwise similar substrate)
- **Same playtest scenario** across encounter formats (swarm, boss, elite trio, endless wave, sustained vs burst)

**Cycle output:** playtest evidence per plane, with comparative result between hypothesis-bearing and failure-mode characters.

### 6.4 Failure-mode playtest discipline

**This is the most-important refinement** beyond Matt's framing. Without failure-mode playtest, the hypothesis-confirmation cycle confirmation-biases: testers find Pattern X feels build-defining because they expected it to. The discipline:

- Every hypothesis-confirmation playtest must be paired with a failure-mode comparison
- The failure-mode character is generated specifically to be absent-of-pattern but otherwise similar
- Comparison evidence required: "the hypothesis-bearing character feels build-defining; the comparison character does NOT"
- If testers cannot distinguish, the hypothesis is wrong OR the playtest sample is too small

### 6.5 Math pattern evolution across cycles

Per Matt 2026-05-31 framing literal: "across play tests we evaluate mathematical patterns to evolve the hypothesis that we test."

Operational:
- After 3-5 playtest cycles on a cell, math patterns emerge in playtest evidence
- Patterns may suggest the cell's coordinates need refinement (e.g., KPM-target was too aggressive; investment-tier was mis-classified; coupling-architecture was wrong)
- Cell version increments; new version playtested; iteration continues

### 6.6 Graduation criteria

| Transition | Criteria |
|---|---|
| `PROVISIONAL → PLAYTEST-CONFIRMED-LOW` | 1 playtest cycle confirms hypothesis at one power plane + failure-mode comparison confirms |
| `PLAYTEST-CONFIRMED-LOW → PLAYTEST-CONFIRMED-CROSS-PLANE` | 3+ playtest cycles across 3+ power planes confirm + failure-mode comparison at each plane confirms |
| `PLAYTEST-CONFIRMED-CROSS-PLANE → PLAYTEST-CONFIRMED-CROSS-VARIATION` | 3-5 character variations embodying the cell across the cross-plane cycles confirm the pattern generalizes |
| `PLAYTEST-CONFIRMED-CROSS-VARIATION → LIBRARY-LOCKED` | gandalf + Matt + jack-ryan canonical review; authorization to encode into generation logic |

**Refutation path:** any cycle producing failure-mode confirmation OR failing to distinguish hypothesis-bearing from comparison character demotes the cell to `REFUTED` or returns to `PROVISIONAL` with hypothesis refinement.

### 6.7 Playtest population limitation

**Matt + son = 2 testers.** Pattern library encoding from a 2-tester population has limited generalization. Mitigation strategies:

- Cross-genre community-research continues feeding hypothesis batches (community discourse from thousands of players grounds patterns broader than local playtest)
- Library-locked cells should be flagged with `playtest_population_size` so downstream consumers know the empirical depth
- Eventual broader playtest (alpha / beta / commercial) extends the population and re-validates locked cells
- Library-versioning should accommodate "this cell graduated at small-population playtest; needs broader-population revalidation"

---

## 7. The pattern library data structure (placeholder)

### 7.1 Database table sketch

```sql
CREATE TABLE pattern_cells (
    cell_id UUID PRIMARY KEY,
    cell_name TEXT NOT NULL,
    cell_status TEXT NOT NULL CHECK (cell_status IN (
        'PROVISIONAL', 'PLAYTEST-CONFIRMED-LOW', 'PLAYTEST-CONFIRMED-CROSS-PLANE',
        'PLAYTEST-CONFIRMED-CROSS-VARIATION', 'LIBRARY-LOCKED', 'REFUTED', 'RETIRED'
    )),
    cell_version INT NOT NULL DEFAULT 1,
    cell_authoring_date DATE,
    cell_hypothesis_source TEXT,

    -- Substrate-axis coordinates (Layer 1)
    bc_axis_signature JSON,
    cultural_lineage TEXT,
    historical_period TEXT,
    register TEXT,
    weapon_type_family TEXT,
    element TEXT,
    attribute TEXT,
    t4_strategy TEXT,
    investment_profile TEXT,

    -- Mechanism-axis coordinates
    primary_mechanism_family TEXT,
    secondary_mechanism_families JSON,
    mechanism_p1_score REAL,
    mechanism_p2_score REAL,
    mechanism_p3_score REAL,
    mechanism_p4_score REAL,
    mechanism_p5_score REAL,
    mechanism_total_score REAL,
    mechanism_relationship_vector TEXT,
    damage_signature TEXT,
    defense_signature TEXT,
    mobility_signature TEXT,

    -- Performance fields
    kpm_target_low_plane INT,
    kpm_target_mid_plane INT,
    kpm_target_high_plane INT,
    multi_format_winning_criteria JSON,
    power_plane_validity JSON,
    failure_mode_comparison_target TEXT,

    -- Experiential-axis coordinates (Layer 2)
    primary_experiential_archetype TEXT,
    sub_axis_flags JSON,
    investment_tier TEXT,
    speedfarm_push_position REAL,
    cognitive_load_target TEXT,
    gear_dependency_index TEXT,
    execution_skill_floor TEXT,
    execution_skill_ceiling TEXT,
    playstyle_geometry_tag TEXT,

    -- Layer 1.5 coupling architecture
    coupling_layer_count INT,
    coupling_strength TEXT,
    single_axis_viability BOOLEAN,

    -- Layer 3 vestigial-class
    vestigial_class_label TEXT,
    class_lineage_coherence_signal REAL,

    -- Validation state
    playtest_cycles_completed INT DEFAULT 0,
    failure_mode_playtest_completed BOOLEAN DEFAULT FALSE,
    cross_plane_validation JSON,
    cross_variation_validation JSON,
    playtest_population_size INT,
    graduation_decision TEXT,
    graduation_authorizer TEXT
);

CREATE TABLE pattern_cell_playtests (
    playtest_id UUID PRIMARY KEY,
    cell_id UUID REFERENCES pattern_cells(cell_id),
    cell_version_at_test INT,
    playtest_date DATE,
    power_plane TEXT,
    encounter_format TEXT,
    hypothesis_bearing_result TEXT,
    failure_mode_comparison_result TEXT,
    notes TEXT,
    tester_id TEXT
);

CREATE TABLE pattern_cell_flags (
    cell_id UUID REFERENCES pattern_cells(cell_id),
    flag_name TEXT,
    PRIMARY KEY (cell_id, flag_name)
);

CREATE TABLE pattern_cell_relationships (
    cell_id_a UUID REFERENCES pattern_cells(cell_id),
    cell_id_b UUID REFERENCES pattern_cells(cell_id),
    relationship_type TEXT CHECK (relationship_type IN (
        'CO_OCCURRING', 'OPPOSING', 'COMPOSITIONAL'
    )),
    strength REAL,
    PRIMARY KEY (cell_id_a, cell_id_b, relationship_type)
);

CREATE TABLE pattern_clusters (
    cluster_id UUID PRIMARY KEY,
    cluster_name TEXT,
    parent_cells JSON
);

CREATE TABLE pattern_library_versions (
    version_id INT PRIMARY KEY,
    version_date DATE,
    substrate_state_hash TEXT,
    library_locked_cell_count INT,
    notes TEXT
);
```

### 7.2 Flag enum versioning

Flags evolve as substrate expands. The flag enum should support:
- Flag addition (new flags as new mechanisms emerge)
- Flag deprecation (when substrate refactors retire mechanism families)
- Flag aliasing (when community vocabulary evolves; e.g., Magic Find legacy → Speedfarm sub-axis)

### 7.3 Cross-cell relationships

The library captures three relationship types per § 3.9:
- **Co-occurring** — cells frequently observed together in build-defining outputs
- **Opposing** — cells that structurally exclude each other
- **Compositional** — cells whose composition produces emergent higher-order patterns

Higher-order patterns (clusters) compose multiple cells. Generation logic encoding may operate at the cluster level rather than per-cell level.

---

## 8. Open questions for Matt's refinement

This document is intentionally a placeholder. The following questions need Matt's direction before any canonical commitment:

1. **Mechanism-relationship vector enum** — § 3.3's `mechanism_relationship_vector` (orthogonal-90 / inverse-180 / synergistic-0 / complementary-270 / composite). Is this the right vocabulary for what you meant by "90 degree or 180 degree (inverse) relationship"? Are there other relationship types to capture?

2. **Power-plane granularity** — proposed L1-12 / L13-25 / L26-38 / L39-50 (4 planes). Is this the right granularity? You said "3 or more"; should we default to 4 for safety?

3. **Failure-mode playtest scope** — every hypothesis-bearing playtest paired with failure-mode comparison. Is this strict enough or too strict? Could playtest cycles 2-3 skip failure-mode comparison if cycle 1 confirmed it?

4. **Graduation authorizer** — § 6.6 lists "gandalf + Matt + jack-ryan canonical review" for `LIBRARY-LOCKED` transition. Who has graduation authority? Just Matt? jack-ryan with BLOCK power per his role? gandalf advisory?

5. **Cell composition strength threshold for cluster formation** — when do two cells become a cluster? Statistical threshold (co-occurrence frequency > X)? Authoring-time declaration?

6. **Substrate-axis-completion sequencing** — should pattern library wait for substrate axis expansion COMPLETION (WS1A finishes all 13 expansion candidates per § 5-9 of HTML doc) or proceed in parallel with substrate expansion (knowing library-locked cells may need revalidation when substrate expands)?

7. **Family B mechanism design call** — § 1.4 names Family B as the "highest-leverage gap-filling candidate." This is a Cycle 15+ architectural design call distinct from pattern library work but composing with it. Should the pattern library wait for Family B mechanism to land OR proceed without and add Family B coverage when Family B mechanism lands?

8. **Playtest cycle count for cross-plane graduation** — § 6.6 lists "3+ playtest cycles across 3+ power planes." Is 3 cycles per plane sufficient? Should there be statistical-significance threshold (e.g., effect-size > 0.5)?

9. **Encoding mechanism for generation logic** — § 7 doesn't specify HOW locked cells encode into generation. Weighted feature selection vs templates vs constraints vs hybrid (per § 4 of original HTML build-defining-backward-inference doc). Which mechanism do we lead with for first Phase C work?

10. **Manifestation milestone scope vs. pattern library Stage 4 infrastructure** — manifestation milestone (Topic #2) is one realized character. Pattern library Stage 4 needs MULTIPLE characters per cell for playtest. Does manifestation milestone scope expand to support pattern library testing (e.g., 5-10 characters from initial component library) OR is manifestation milestone its own bounded deliverable with pattern library testing requiring additional infrastructure?

11. **Coupling architecture commitment** — research recommends ≤3 multiplicative loot substrate layers; LE-style. Is this a locked architectural decision OR still under consideration? Pattern library cells need to know the coupling target.

12. **Backward inference scope vs. pattern library scope** — the original build-defining-backward-inference doc (Topic #1 source) proposes an end-state where the engine becomes a learning system. The pattern library is one component of this. Does this placeholder document scope cover the full backward-inference architecture, or just the pattern library Phase A-E mechanics?

13. **Cell retirement triggers** — when does a `LIBRARY-LOCKED` cell get retired? Substrate refactor invalidating coordinates? New community research showing the pattern fell out of player community favor? Empirical evidence from broader playtest later disconfirming?

14. **Cell schema location** — does the pattern library live engine-side (`reincarnated-engine/src/reincarnated/pattern_library/`) or meta-side (`canonical/pattern-library.db`)? Suggests engine-side because generation logic consumes it.

15. **Hypothesis batch authoring cadence** — how often are new hypothesis batches generated? Quarterly? Per substrate-axis expansion event? Continuously?

### 8b. Open questions from 2026-06-01 refinement iteration

16. **WS1A.4 per-skill flavor judgment LLM prompt design** (per § 1.7) — what's the LLM prompt template that produces bounded per-skill judgment? Single-element kit prompt vs hybrid 2-element prompt differ in choice space; both need precise prompt engineering to constrain output to the bounded set. Star-lord seam authoring + Matt sign-off; Cycle 15+ work.

17. **Hybrid kit element pair selection criteria** (per § 1.7.2) — when generation creates a hybrid 2-element kit, what determines WHICH 2 primary elements are paired? Designer-declared at substrate level? Substrate-led emergence from BC tuple coordinates? Specific cohesion-judge rules? This is upstream of per-skill flavor judgment but affects what kits become hybrid candidates.

18. **Flavor pool per primary element** (per § 1.7.1) — the canonical 2.5 vocabulary is segmented by primary element. Each canonical primary has its own sub-element flavor pool. Has this segmentation been canonically locked? If not, that's a prerequisite locking step for WS1A.3 + WS1A.4 implementation. (Matt 2026-06-01 correction: earth's flavor pool includes bone/stone/ore/etc., NOT shadow which is its own canonical element.)

19. **Emergent kit concept naming consistency** — Wave B LLM emerges concepts like "Necromancer" / "Death Knight" / "Bone Witch." These names persist as the kit's player-facing identity. Should emergent concepts be drawn from a canonical vocabulary list (curated; ensures genre-recognizable names) OR free LLM generation (richer; risks unrecognizable names)? Tension between substrate-led discipline (free LLM emergence) vs player-recognizability (curated list).

20. **Identity-finalization re-run scope** — Phase 1 manifestation milestone runs identity finalization on full wave-5 snapshot archive OR only on the chosen manifestation character? Full archive is cleaner (everything stays in sync); single character is faster. Tradeoff: faster Phase 1 vs cleaner architecture for cross-cell hypothesis testing.

21. **Three-layer playtest validation co-graduation** (per § 6.0) — if a playtest cycle confirms hypothesis-cell pattern (Layer 1) but the gauntlet metric prediction was wrong (Layer 2), does the cell graduate? Should there be cell-level vs gauntlet-level graduation independence, or co-graduation discipline?

22. **WS1A.1 retroactive inference confidence threshold** — § 5.2 + § 7 note that wave-5 snapshot kits get expanded axes via retroactive inference. What confidence threshold gates "this kit's experiential archetype = Bossing"? LLM-inferred labels carry uncertainty; pattern library needs to know when inference is reliable enough to encode against.

23. **Cell-level flavor judgment distribution prediction** (per § 3.10) — cells predict the distribution of per-skill flavor alignments (e.g., "Necromancer cell predicts {blend: 2, sub: 1, primary: 2}"). Is this distribution a STRONG cell-level constraint OR a SOFT preference? Generation logic at Phase C may need to know how to weight cell-predicted distributions vs LLM judgment freedom.

### 8c. Open questions from iter 3 refinement (three-layer mechanism treatment)

24. **Layer 2 mechanism-structural dimension enums** — proposed 4 dimensions (magnitude pattern / stackability / trigger / scaling) with 3-4 enum values each. Are these the right dimensions? Are there other mechanism-structural axes the genre research surfaced that should be added? (e.g., visibility / interaction-coupling / per-skill-vs-per-kit-application).

25. **Layer 2 vs Layer 1 generation priority** — when generation operates against both Layer 1 (P1-P5 scores) AND Layer 2 (structural enums) coordinates, which takes precedence if they conflict? E.g., if Layer 1 target says "high P2 multiplicative composition" but Layer 2 target says "fixed magnitude no-stacking," are these compatible at all? Probably no — surfaces a constraint-satisfaction question for generation logic.

26. **Family-similarity observational classifier** — how does Layer 3 `observed_family_similarity` get computed? LLM-judgment-based classification? Rule-based pattern matching against the 7-family templates? Statistical similarity scoring against genre exemplar mechanisms? Implementation choice affects how reliably the observational tags fire.

27. **Reincarnated-native mechanisms with no genre analog** — the `OBSERVED_NOVEL_NO_GENRE_ANALOG` flag covers cells whose mechanisms don't fit any of A-G. How does this flag get attached — automatic when none of A-G similarity exceeds threshold, OR explicit author-time declaration? Implementation question.

28. **Reframing Family B "highest-leverage gap" as Layer 1 + Layer 2 coordinate gap** — § 1.4.2 reframes "highest-leverage Cycle 15+ design call" from "build Family B" to "fill the high-P2-P3 + multiplicative-stackability + on-event-trigger + scales-with-investment coordinate gap." Is this reframing complete, or do other sections still carry the old framing that needs retirement? Matt review needed.

### 8d. Open questions from iter 4 refinement (multi-axis experiential architecture)

29. **Leveling-as-viability-axis hypothesis (§ 1.8.5)** — TRUE for Reincarnated (50-level scope + 85%-leveling-only forces universal viability gate) OR FALSE (Progression-Stage works as identity axis like genre)? This is the central iter 4 hypothesis. Playtest validates; decision deferred.

30. **Viability-axis gate threshold values** — what minimum score on each viability axis (Survivability / Playability / possibly Leveling) constitutes "pass"? Designer-asserted starting values, then refined through playtest evidence? Or empirically-derived from genre community-acceptability thresholds (Maxroll's "S-tier" / "A-tier" / etc.)?

31. **Mutual exclusivity preference operationalization** — how do generation parameters target mutual exclusivity? Statistical preference (most cells specialized; some hybrid)? Hard constraint (cells fail if multi-axis-spanning beyond threshold)? Per-cell-shape declaration that generation honors? Tied to § 1.8.4 cell shape distribution targets.

32. **Cell-shape distribution targets per cycle** — what fraction of cells per cycle should be Specialized vs Hybrid vs Generalist vs Anti-specialization? Reincarnated-target distribution (e.g., 70% Specialized + 20% Hybrid + 5% Generalist + 5% Anti-specialization)? Per-power-plane distribution targets (e.g., Anti-specialization more common at low investment tiers; Specialized more common at high investment tiers)?

33. **Activity-Format axis values** — Reincarnated's endgame structure determines the enum values for Activity-Format axis. What endgame structure does Reincarnated ship with? TBD per game design; pattern library waits or uses placeholder enum.

34. **Maxroll 5-axis structured rating prediction precision** — cells predict 5-axis profiles (Bossing/Speed/Push/Survivability/Playability) at hypothesis time. What's the prediction granularity (integer 1-10? Decimal? Range?) and how is prediction-vs-observation match scored at validation?

35. **Cross-axis profile constraints** — are there combinations of multi-axis coordinates that are STRUCTURALLY incompatible (e.g., "high Bossing + high Speedfarming at Specialized cell shape" is contradictory)? Generation needs to know which combinations are valid candidates vs structurally impossible.

36. **Emergent label inference methodology** — § 3.5 `emergent_archetype_label` field is computed post-hoc from multi-axis profile dominance. What's the inference algorithm? Threshold-based (e.g., "if Bossing > 7 AND Push > 7 → 'Bossing Push'")? LLM-based labeling? Statistical clustering? Implementation choice affects label consistency and player-facing surface coherence.

### 8e. Open questions from iter 5 refinement (pipeline placement decision)

37. **Option B deferral evidence threshold** — what specific empirical evidence at manifestation milestone playtest would trigger Option B (pre-Pareto LLM naming with faction-aware reduction)? Concrete criteria needed: e.g., "if 2+ playtest cycles surface 'expected emergent identity X failed to materialize because candidate kits were Pareto-eliminated before naming'" → Option B refinement.

38. **Cost compounding across cycles** — Option A's ~$1.50-4.50/cycle assumes per-cycle LLM cost. Across many cycles (52 seasons/year × multi-year project lifespan), this compounds. Is Pi-LLM-proxy infrastructure (per `canonical/story/2026-05-30-pi-llm-proxy-architecture-recognition.md`) the cost-mitigation answer (caching + provider routing)?

39. **Phase 5b cohesion clustering threshold for n=30** — at n=30 kits with ~3-5 emergent factions, are there minimum-kits-per-faction thresholds that would refute a clustering decision? E.g., a 1-kit cluster is more likely substrate noise than a meaningful faction; should cohesion judge enforce minimum-cluster-size of 3-4?

40. **Pre-Pareto cohesion-judge inference (gandalf hypothesis at § 1.7.8)** — gandalf argued that "identity emergence is largely predictable from substrate (BC tuple + cultural lineage + element + period + register)" without running LLM naming on all 650 kits. Is this empirically testable BEFORE manifestation milestone? E.g., LLM-name a small sample (50 kits) pre-Pareto and post-Pareto; compare identity distributions. If gandalf hypothesis holds, Option A is fully validated; if not, Option B becomes more compelling.

### 8f. Open questions from iter 6 refinement (Mode axis removal)

41. **HC mode inclusion decision** — does Reincarnated ship with Hardcore mode? Per § 1.8 iter 6 amendment, Mode axis was removed because mode is player-session-level choice, not kit-architecture-level property. IF HC mode is added: HC-viability becomes higher Survivability threshold within existing Viability axis (`VIABILITY_HC_SURVIVABILITY_PASS` gate). IF HC mode is not added: the question is moot. Decision-pending per game design call.

42. **HC-Survivability threshold delta** (conditional on Q41 yes) — if HC mode is added, what's the threshold delta between baseline `VIABILITY_SURVIVABILITY_PASS` and `VIABILITY_HC_SURVIVABILITY_PASS`? Designer-asserted starting value, then refined per playtest evidence on HC death rates per kit?

### 8g. Open questions from iter 7 refinement (multi-source hypothesis generation)

43. **Initial telemetry event set** (per § 2.4.2) — which telemetry events does the engine capture from day 1 of Reincarnated player exposure? Comprehensive (every event) or curated (engagement-critical only)? Star-lord + gandalf + gamora design call pre-soft-launch.

44. **Telemetry retention policy** — how long does the engine retain player telemetry? GDPR-compatible retention windows? Aggregation timelines? Star-lord + jack-ryan design call pre-launch.

45. **Reincarnated-hosted community site architecture timing** — when does Reincarnated-hosted community infrastructure go live relative to game launch? Pre-launch community (build hype) vs at-launch vs post-launch? Affects ingest pipeline architecture timing.

46. **Multi-source hypothesis weighting** — when telemetry from multiple sources is available, how does Stage 1 hypothesis generation weight sources? Designer-asserted weights? Empirically-validated weights (which sources produce best hypothesis-graduation rates)? Per-source confidence scoring?

47. **Cross-source signal validation** — when community-derived telemetry suggests Pattern X is build-defining BUT real player telemetry suggests Pattern X is rarely chosen, which signal wins? Substrate-led discipline says "substrate votes" but here multiple substrate channels disagree. Methodology needed for cross-source disagreement resolution.

48. **Substrate-led discipline canonical write at player-experience layer** (per § 2.4.4) — should gandalf author a new canonical refinement of the designer-writes-substrate / player-names-experience principle specifically covering the post-launch player-data layer? Anticipates need; timing TBD.

### 8h. Open questions from iter 8 refinement (endgame content type architecture — player-input procedural map generation)

49. **Player input architecture specifics** (per § 1.8.7) — what's the player-input mechanic? Slot-based (select N input modifiers per map run)? Sequence-based (build up modifier chains)? Resource-based (spend currency to add modifiers)? Tier-pin-based (lock in tier first, then auto-populate modifiers)? Each affects player engagement pattern + cohesion judge clustering.

50. **Input layer count per substrate-led coupling discipline** (per § 1.1.5 + § 1.8.7) — Reincarnated targets ≤3 multiplicative input layers per coupling-architecture recommendation. What are the 3 layers? Initial proposal: (1) base tier; (2) input category; (3) modifier intensity. Alternative: (1) faction theming; (2) content focus; (3) reward focus. Other compositions? Designer call composing with sprint synthesis recommendation.

51. **Tier scaling progression mathematics** — infinite-tower-equivalent scaling via tiers means progression math must scale gracefully. PoE tiers scale ~50% damage + ~30% HP per tier (rough); D4 Pit scales ~40% damage per tier; LE Monolith corruption scales ~25% damage per corruption level. What's Reincarnated's tier scaling rate? Composes with existing damage scaling architecture (doc 47) + investment scaling (doc 51).

52. **Boss emergence within map system** (per § 1.8.7 Uber-Bosses-bonus) — how do pinnacle bosses spawn within input-driven maps? Tier-gate spawn (above tier-X, boss-input maps spawn pinnacle bosses)? Modifier-gate spawn (boss-input modifier presence + adequate tier triggers pinnacle boss)? Pre-authored boss roster + emergence rules? Game-design call.

53. **Anti-faction input composition with cascade architecture** — cascade architecture (canonical) maps player choice to environment morphing + faction opposition. Player-input map architecture extends this — anti-faction inputs spawn anti-faction-themed maps. Per § 1.8.7, this is bonus composition. How exactly do anti-faction inputs intersect with cascade architecture's existing anti-faction emergence?

54. **Canonical recognition record for player-input procedural map generation** — should gandalf author a separate canonical recognition record at `canonical/story/2026-06-01-player-input-procedural-map-generation-recognition.md` capturing Matt's iter 8 proposal independent of the placeholder doc? Substantive game-design proposal warrants canonical capture beyond placeholder inclusion; timing TBD pending Matt direction.

55. **Cross-seam routing for implementation** — implementation requires: gamora (engine generation accepting input modifiers); star-lord (pipeline + Phase 5 integration of input-derived metadata); drax (player-facing input UI); gandalf (design specs); knight-rider (cross-seam coordination); rocket (canonical-doc updates for generation integration). When player-input architecture commits canonically, KR routes implementation dispatches. Timing per Matt direction.

---

## 9. Cross-references

### 9.1 Composes with (existing canon)

- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational three-layer architecture
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — third coordinate axis
- `canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` — gauntlet metric validity recognition; informs three-layer playtest validation framing (§ 6.0); wave-5 swift snapshot closure path
- `canonical/story/2026-05-31-ue-seam-agent-placement-decision.md` — UE seam agent placement; supports manifestation milestone Phase 2 realization
- `canonical/story/c-hybrid-cell-and-curation-architecture-2026-05-28.md` — hybrid kit architecture; foundation for hybrid 2-element kit per-skill judgment (§ 1.7.2)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 — substrate-led discipline (with refinement per § 1.2 above)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — T4 architecture
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — BVV
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — investment scaling
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — Phase 5 prompts (current; WS1A.2 amendment target)
- `agentic_orchestration/research/arpg-community-axes-2026-05-29/synthesis-verdict.md` — empirical research sprint output
- `agentic_orchestration/gandalf/notes/2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html` § 19 + § 22 — mechanism families + 5-property framework
- `matt_notes_handoff_docs/build-defining-backward-inference.md` — original Topic #1 architectural concept

### 9.2 Refines (proposed)

- Discipline #41 substrate-led — refinement per § 1.2 (engineering generation is permitted; validation step binds the encoding gate)
- Design philosophy doc — composition pattern (Designer writes substrate AND coupling-architecture; Player names experience; engine consumes post-emergence community vocabulary; pattern library bridges engineering hypothesis and empirical confirmation)

### 9.3 Anticipates (future canonical)

- Pattern library schema canonical write at engine-side (when Phase A fires)
- Hypothesis-flow methodology Discipline candidate (jack-ryan ratifies after first 3-5 hypothesis cycles complete)
- Flag enum canonical lock (after substrate axis expansion completes and flag set stabilizes)
- Cluster-formation methodology (after first 20+ cells graduate and clusters emerge)
- Library-versioning + substrate-refactor compatibility canonical (after first substrate refactor invalidates encoded cells)

### 9.4 Does NOT replace or amend

- Cycle 14 v1 generation architecture — pattern library is Cycle 15+ scope; v1 unchanged
- Existing substrate canonical commitments — they are inputs, not amended
- Existing T4 architecture — extended, not replaced
- Existing cohesion-judge / Wave A / Wave B LLM prompts — Cycle 15+ extension target, current prompts hold

---

## 10. Sign-off + next steps

### 10.1 Authoring

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-31 verbatim request

**Composed from:** 2026-05-29 ARPG community research sprint output (synthesis-verdict.md + analysis-findings.md + statistical-analysis-findings.md across 90K+ tokens) + designer-writes-substrate / player-names-experience principle (foundational canon) + 5-property substrate framework + 7 mechanism families (§ 22 + § 19 of substrate-axis-expansion HTML) + experiential cascade architecture recognition + Matt 2026-05-31 hypothesis-flow methodology articulation + Matt 2026-05-31 engineering-generation-feasibility clarification

**Discipline composition:**
- Disc #41 substrate-led (refined; engineering generation permitted; encoding gate bound)
- Disc #42a framing-audit (Matt's pushback caught the over-conservative substrate-organic-emergence requirement; this draft incorporates the refinement)
- Disc #18 methodology consultation (flag for Stage 5 graduation methodology — statistical-significance threshold? jack-ryan + legolas Mode A consultation candidate)
- Recognition → empirical validation → commit (this document is the recognition; refinement conversation IS the validation; commitment is the next stage)

### 10.2 What this document IS

- A placeholder architectural draft for Matt review + refinement
- A synthesis of yesterday's substrate research findings + canonical principles + Matt 2026-05-31 methodology articulation
- Substrate for a Pattern B dialogue that produces the committed architecture
- 15 open questions (§ 8) flagging where Matt's direction is needed

### 10.3 What this document IS NOT

- A canonical commitment to the architecture (status: PLACEHOLDER)
- A Cycle 14 v1 amendment (Cycle 15+ scope explicitly)
- A jack-ryan-ratified Discipline (the methodology candidates within would be Disc candidates post-validation)
- A schema commitment for engine-side implementation (§ 7 is a sketch; implementation specifics gate on Phase A)
- A commitment to the time horizon estimates (§ 5.3) — those are scoping signals, not promises

### 10.4 Immediate next moves

1. **Matt reads this document** and surfaces refinement points + answers to § 8 open questions
2. **Pattern B refinement dialogue** between Matt and gandalf addresses each open question; the document iterates through revisions
3. **At refinement convergence**, document graduates from PLACEHOLDER → CURRENT canon (or breaks into multiple companion canonical commitments)
4. **At graduation**, knight-rider routes the architectural commitment to the work queue for Cycle 15+ workstream sequencing
5. **At appropriate gate** (post-Cycle-14-close + post-WS1A + post-manifestation), Phase A infrastructure work fires; pattern library begins accumulating provisional cells

### 10.5 What to push back on as you read

- Any field in § 3 (mathematical cell) that seems wrong or missing
- Any flag in § 4 (flag enum) that's mislabeled, miscategorized, or absent
- Any methodology choice in § 6 (validation) that's too strict, too loose, or wrong-discipline
- Any sequencing assumption in § 5 (gates) that contradicts your project sequencing intent
- Any open question in § 8 that's not actually open OR that's missing
- Any cross-reference in § 9 that's wrong, missing, or mis-classified

This document is most useful when most-marked-up. The refined version emerges from your pushback.

---

## 11. GRADUATION SIGN-OFF — PLACEHOLDER → CURRENT 2026-06-01

**Graduation authorization:** Matt 2026-06-01 close-out directive: "Move the placeholder doc below to canonical."

**Status transition:** PLACEHOLDER FOR REFINEMENT → CURRENT (load-bearing canonical commitment)

**What changed at graduation:** STATUS marker updated; title updated (removed "PLACEHOLDER FOR REFINEMENT" suffix); file renamed (removed `-placeholder` suffix; git tracks the move); this graduation sign-off section appended. Content otherwise unchanged from refinement iteration 8 commit `e04caba`.

**What the graduation MEANS:**

| Dimension | Pre-graduation (PLACEHOLDER) | Post-graduation (CURRENT) |
|---|---|---|
| Architectural commitment | Pre-commitment draft awaiting refinement convergence | Architecture COMMITTED; foundational structure no longer placeholder |
| Parameter commitments | All TBD pending refinement | Multi-axis architecture + cell schema + flag enum + sequencing committed; specific threshold values + content-type proposals are PROPOSED PLAYTEST-PENDING |
| Cross-references | Treated as in-flux | Other canonical docs may reference this as load-bearing |
| Future iterations | Expected to substantially restructure | Expected to refine parameters + answer open questions; not architectural restructure |
| Open questions (55) | Pre-commitment open questions | Pattern-B-refinement open questions; answered through playtest evidence + Matt direction per recognition-validate-commit discipline |

**What the graduation does NOT do:**

- Does NOT close the 55 open questions in § 8a-h
- Does NOT commit specific parameter threshold values (e.g., Survivability gate threshold value; tier scaling rate; cost-cap thresholds)
- Does NOT canonically commit the player-input procedural map generation architecture (per § 1.8.7 — PROPOSED PLAYTEST-PENDING; separate canonical recognition record candidate per Q54)
- Does NOT commit the Leveling-as-viability-axis hypothesis (§ 1.8.5 — pending playtest)
- Does NOT supersede companion canonical commitments (designer-writes-substrate / experiential cascade / gauntlet provisional / etc.)
- Does NOT obviate the manifestation milestone validation gates per recognition-validate-commit discipline

**Iteration history (refinement passes 1-8; 2026-05-31 → 2026-06-01):**

| Iter | Type | What landed |
|---|---|---|
| 0 | Original placeholder | Initial architectural draft; 6 sections + foundational principles + cell schema + flag enum + sequencing + validation + open questions |
| 1 | Consolidated additions | Gauntlet provisional + manifestation Phase 1/2 + retroactive feasibility + WS1A.4 per-skill bounded flavor judgment + three-layer playtest validation |
| 2 | Remap | P4 → creation-moment-memorability (Reincarnated-specific from genre import) |
| 3 | Restructure | 7 mechanism families → three-layer treatment (Layer 1 P1-P5 / Layer 2 mechanism-structural / Layer 3 observational); "Family B gap" framing retired |
| 4 | Decomposition | 6 archetype labels → multi-axis architecture (Progression-Stage / Target-Pattern / Depth-vs-Breadth + Activity-Format / Loot-Focus / Maxroll 5-axis); cell shape framework; Leveling-as-viability hypothesis |
| 5 | Decision lock | Pipeline placement Option A (LLM naming AFTER Pareto reduction; ~30 kits not ~650) |
| 6 | Subtraction | Mode axis REMOVED (category error: session-level vs kit-architecture-level) |
| 7 | Lifecycle extension | Multi-source hypothesis generation across launch lifecycle (real player telemetry + community-derived telemetry; 3 ingest channels; pre-launch architectural decisions) |
| 8 | Content type architecture | Player-input procedural map generation as endgame content type (Matt 2026-06-01 elegant two-bird-one-stone proposal); activates 5+ axes; ≤3 layer coupling discipline per sprint synthesis |

**Authoring:** gandalf (story-and-design steward) per Matt 2026-05-31 → 2026-06-01 Pattern B refinement dialogue (8 iterations) + 2026-06-01 close-out graduation authorization

**Cross-references should now treat this as CURRENT canonical:**
- `canonical/00-ground-state.md` § 1 (CURRENT TRUTH table) — gets a new entry
- Other 2026-06-01 commitments (gauntlet provisional recognition; UE-seam placement decision) — cross-reference adjustments needed where they referenced the placeholder name

**Companion artifact note:** the file location at `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` (no `-placeholder` suffix) is the canonical path. Git-tracked rename preserves history; the prior path is no longer current. Any external references should be updated to the new path.

**End of canonical commitment.**
