# Form-Bias Cadence Strategy — ARPG ↔ Isekai Axis

**Status:** **Canonical-story design strategy.** Authored 2026-05-16 (Day 4) by gandalf on knight-rider's commission `agentic_orchestration/dispatches/2026-05-16-gandalf-form-bias-cadence-strategy.md` (Matt-approved Day 4). Frames Matt's verbatim Q1-Q4 against the engine's pre-LLM substrate inventory + Legolas's five-pass research base.

**Predecessor work this doc consumes (NOT reproduces):**
- `canonical/story/pre-llm-substrate-inventory.md` — the cluster-organized substrate this doc reasons against (Clusters A-E; 53 catalogued items; terminology lock)
- `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md` — item-by-item code citations underneath the inventory
- `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` — Day-4 re-engagement (the terminology lock; the catalogue-coupling insight; the three-layer-model reframe)
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the diagnosis this doc operationalizes into a strategy

**Predecessor design locks this doc honors:**
- Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin) per doc 37 § 4
- Position (ii) (per-season vocabulary carries own mechanical signatures; cipher = resistance-translation only) per doc 37 § 6.2
- Catalogue-based form-bias resolution path per doc 37 § "Catalogue-based form-bias resolution path"
- Style register HD-2D-pixel canonical per `canonical/story/style-register.md`
- Court framing per `canonical/story/court-of-forms.md` + dual-label pattern C8
- Embodiment taxonomy + dual-layer naming per `canonical/story/embodiment-narrative-layer.md`
- Naming triad universal frame per `canonical/story/naming-triad.md`
- Three-layer model (L1 engine substrate / L2 Reincarnated cosmology / L3 per-season content) per `canonical/story/engine-generic-meta-structure.md`

**Parallel-workstream context:** Per Matt's 2026-05-16 parallel-workstream lock (VS2a + VS2b), this strategy doc is the unblocker for **four downstream VS2b workstreams** (per `canonical/16-project-roadmap.md` Substrate Realignment §): S1 (embodiment-axis schema), S2 (pair-structure layer), display work, Pimen full integration. Pre-Day-4 the doc was scheduled to wait for catalogue-mapping experiment findings; Matt's parallel-workstream mandate **superseded** that — Path (b): land now with Q4 cipher-width framework + dependency-deferrals.

**Companion docs (further reading):**
- `canonical/story/season-feel-rubric.md` — what kind of seasons we want this strategy to produce
- `canonical/story/drift-audit.md` — the discipline this strategy is embedded inside
- `canonical/story/engine-balance-stewardship.md` — companion stewardship doc on a parallel (engine-balance) gate cluster

**Pending:**
- knight-rider drafts decisions-log entries from this doc's locks (per ADR-002); jack-ryan Gate 1; Matt approves; commit. Anticipated entries enumerated in § 8.
- Disciplines #13a + #13b + #14 candidates land in `engineering-disciplines.md` against the terminology-locked framing this doc honors.
- Cross-seam dispatch authoring (rocket / star-lord / gamora / drax / elrond) sequenced behind the locks in § 7 + § 8.

---

## 0. TL;DR

**Matt's four questions, answered:**

1. **Q1 (Inventory):** Use the cluster-organized substrate inventory (Clusters A-E; 53 items; pre-LLM-substrate-inventory.md). Path (a) of the commission was chosen — rocket Pattern A pass already filed the code-citations; this doc reasons against the cluster organization, not the 53 items individually.
2. **Q2 (Convergence shape):** The engine produces **three orthogonal patterns** under the terminology lock: (i) a humanoid-presupposing **schema cluster** (Cluster A — gear/loadout, 14 items in one tight cluster); (ii) a form-agnostic-but-named-humanoid **labels-on-mechanics cluster** (Cluster B — 18 items, distributed); (iii) a **universal LLM-drift surface** (Cluster E — every prompt-construction site currently exposes canonical-four labels). These are not aggregated into a single "skew"; each has its own resolution lever.
3. **Q3 (Canon match):** The engine's substrate is **ARPG-canon-comfortable at the schema layer and isekai-canon-incompatible at the embodiment layer.** ARPG canon supports the gear/class/attribute schema as load-bearing (Diablo II, PoE, Last Epoch all share it; player vocabulary depends on it). Isekai canon — particularly the *non-humanoid reincarnation* sub-genre's defining template (Slime / Spider / Spider-template Dragon Hatchling 2024) — explicitly requires embodiment variance that the current schema cannot express. **The gap doc 37 surfaced is real and structural; it is the isekai-side gap specifically.**
4. **Q4 (Push/pull):** The decision framework lands as **explicit-hybrid with two locked sub-positions plus four deferred catalogue-track sub-locks.** Locked: (a) **Phase-0 ARPG-canon-primary at the substrate-mechanical layer** (Cluster A + B mechanics preserved); (b) **Phase-0 Isekai-canon-primary at the narrative-skin and convergence layers** (Position C + cipher architecture + per-embodiment narrative do the isekai work without breaking ARPG mechanics). Deferred-pending-catalogue: cipher-width (Options A/B/C); Foundation layer placement; D1 rubric reconsideration; per-season vocabulary coupling (α/β/γ). All four resolve at named catalogue milestones; the strategic-axis lock above can proceed without them.

**Cadence options (I/II/III) reformulated** against the strategic-axis lock — see § 7. **Cipher-width framework** explicit in § 6 even with cipher-width itself deferred-pending-experiment.

**What this unblocks immediately:** the four VS2b workstreams (S1 embodiment-axis schema; S2 pair-structure layer; display work; Pimen integration); Disciplines #13a/#13b/#14 codification; kit-anchor rename dispatch; D1 element-name pool decision-criteria locking.

**The hat stays on.**

---

## 1. Q1 — Inventory: what carries the bias?

**Path chosen:** **(a)** per the commission's two options. Rocket Pattern A pass already produced the comprehensive code-grounded inventory before this doc's authoring; `pre-llm-substrate-inventory.md` is the cluster-organized successor to doc 37 § 2's starting list; the present doc reasons against the cluster organization rather than re-enumerating the 53 items.

**Why path (a) over path (b):** the substrate inventory work already happened (gandalf + rocket, 2026-05-16). Path (b) would have re-commissioned rocket. The catalogued substrate already meets Q1's "minimum coverage" list verbatim, plus five items discovered during the pass (energy_type vocabulary, range_profile, dominant_element, color hints, Foundation 4+1 validator). Re-commissioning would produce no new structural insight.

### 1.1 The cluster organization (per pre-llm-substrate-inventory.md)

| Cluster | Count | Structural-presupposition tag | Where it concentrates |
|---|---|---|---|
| **A** | 14 | humanoid-presupposing | One tight schema cluster: loadout/gear (`generation/gear_schema.py` + `gear_generation.py` + `gear_catalog.py`) |
| **B** | 18 | form-agnostic-but-named-humanoid | Distributed: element labels, class archetype labels, attribute axes, geometry palette labels, energy-type vocabulary, canonical library names |
| **C** | 9 | form-agnostic | Role-orientation taxonomy, skill role/timing/composition vocabulary, range profile, color hints, abstract geometry labels |
| **D** | 7 | embodiment-orthogonal | Damage/ailment categories, trial naming-triad mechanics, spirit-guide kit-composition framing, trait category enum |
| **E** | (universal) | implementation-vs-intent drift | Every LLM prompt-construction site in the generation seam — `naming.py:26-36`, `naming.py:87`, `naming.py:89`, `selector.py:43-47`, `selector.py:394-446`, `library_generator.py:85` |

### 1.2 The cluster shape IS the inventory's load-bearing finding

The 14 humanoid-presupposing items are **not 14 distributed problems — they are one tight problem.** They concentrate in a single schema cluster (gear and loadout). Outside that cluster, the engine's structural presupposition is largely *form-agnostic-but-named-humanoid* (mechanics form-neutral; labels carry humanoid weight).

This matters because **fixing one cluster is operationally different from fixing 14 distributed surfaces.** A coordinated schema migration that resolves the loadout/gear cluster (per doc 37 § 4 Position C) addresses the schema-shape concentration of humanoid-presupposition in one change. Re-labeling Cluster B's broader form-agnostic-but-named-humanoid surface is a separate, lower-stakes change that stages independently.

### 1.3 Cluster E is a separate kind of finding

Cluster E is **not** a structural-presupposition cluster; it is an *implementation-vs-intent drift inventory* in the precise sense the terminology lock allows. Doc 37 § 6 specified canonical-four-hidden-from-LLM; every LLM call currently exposes them. The drift is universal, not partial. The full cipher migration is ahead, not behind.

This finding is the cleanest drift instance in the project so far because it is observable from code-reading alone. No telemetry needed. No measurement needed. **The code IS the evidence.** Q4's catalogue-track dependencies (§ 6.5 below) do not block Cluster E's resolution; that resolution is mechanical once direction is locked.

### 1.4 The five resolved ambiguities

Per the rocket pass + this doc's cluster framing, the five "uncertain" items from the inventory are resolved:

1. **D1 rubric questions** — empirical-screening effect is **Flag A**; resolves via targeted test (§ 6.5)
2. **`PlayerClass.skills` kit-of-skills framing** — **structurally-incomplete-but-not-presupposition**; resolved by adding `embodiment_tag` field per `embodiment-narrative-layer.md` § "Engine emit requirements"
3. **Anchor vocabulary** — **embodiment-orthogonal at the engine layer**; anchor library contents are L2 Reincarnated cosmology per `engine-generic-meta-structure.md`. (Whether specific anchors are humanoid-themed in their library data is a content-curation question, not a substrate question.)
4. **`rage`/`stamina-as-resource` energy types** — **form-agnostic-but-named-humanoid** (Cluster B). The energy-pool mechanic is form-neutral; the experiential-weight of "rage" and "stamina" is humanoid-coded. Cluster-B treatment applies.
5. **Canonical library names** (`Searing Wave`, `Stone Grasp`, etc.) — **Cluster B with cipher-migration follow-on**. The library names humanoid-fantasy by label; the library lookup mechanic is form-agnostic. The library may need re-generation once the cipher architecture shifts; that's a downstream dispatch, not a Q4 lock.

### 1.5 The two decision-critical-and-unknowable flags

Per the rocket pass, two findings block specific dispatches and must resolve before this doc's recommendations land as decisions-log entries:

- **Flag A — D1 rubric structurally screens for humanoid-fantasy compounds.** `element/selector.py:282-296`. Whether the rubric reliably under-scores non-humanoid-cosmology candidates is an empirical question. Targeted test commission scoped at § 6.5.
- **Flag B — Foundation model validator and cipher architecture extension.** `foundation/foundation.py:39-43` hard-codes 4-rotating + 1-physical. Any cipher expansion requires this validator to update. The architectural question (does Foundation grow with the cipher, or decouple to a separate L2 cosmology concept) is an L1/L2 layer-placement decision that resolves at § 6.5's catalogue gates.

Both flags are explicit-deferred to catalogue-track. The strategic-axis lock in § 5 can proceed regardless.

---

## 2. Q2 — Convergence shape: what the engine produces, with attribution honesty

Matt's terminology lock (2026-05-16) bars the word *skew* until per-variable evidence exists. This section names what the engine **produces** in descriptive terms; it does NOT attribute the production to individual variables; it names the **patterns** that downstream form-bias work can use as shared vocabulary.

### 2.1 The three patterns, named

The engine's pre-LLM substrate produces three distinct patterns under the terminology lock. Each has its own resolution lever; the form-bias work does not collapse them into a single "skew" surface.

#### Pattern P1 — The schema-cluster humanoid-presupposition pattern (Cluster A)

**Description:** Cluster A's 14 humanoid-presupposing items concentrate in `Loadout` + `GearInstance` + `gear_catalog.py`. The schema's *shape* — explicit `weapon`/`off_hand`/`armor`/`accessory` fields; `handedness` 1h/2h gating; `_BASE_TYPE_STAT_AFFINITY` mapping medieval-humanoid equipment categories to STR/DEX/INT — presupposes humanoid anatomy.

**Convergence-shape implication:** every season generates 5-6 player-classes, each instantiated against this schema. The engine cannot produce a class whose mechanical identity is "a swarm with no hands and a distributed offensive surface that doesn't reduce to weapon/off_hand." It can only produce humanoid-shaped equipment that happens to be flavored differently. The PackProxy entity (B10.2 ship) shows the engine *can* hold non-humanoid composition in simulation; the player-class schema does not yet.

**Genre-precedent grounding:** ARPG canon has this presupposition load-bearing. Diablo II, Diablo IV, Path of Exile, Last Epoch, Grim Dawn all carry weapon/armor/accessory schemas; player vocabulary across the genre depends on these. Isekai canon — specifically the *non-humanoid reincarnation* sub-genre per Legolas Pass 1 (Slime / Spider / Dragon Hatchling 2024) — has an opposite presupposition: the protagonist's body is *the* defining feature, and equipment slots presupposing arms/torso would break the genre's contract.

**Resolution lever:** Position C migration (slot-as-functional-mechanic + embodiment-as-narrative-skin). Locked in doc 37 § 4; operationalized in `embodiment-narrative-layer.md`. One coordinated schema migration resolves the cluster. The migration's mechanical-substrate stays ARPG-canon-comfortable; the narrative-skin layer becomes isekai-canon-compatible.

#### Pattern P2 — The labels-on-mechanics distributed pattern (Cluster B)

**Description:** Cluster B's 18 items share a pattern — *the mechanic is form-agnostic; the label carries humanoid weight*. Canonical-four element names; class archetype labels (warrior/mage/rogue/hunter); attribute labels (STR/DEX/INT/WIS/VIT); geometry labels (`melee_strike`, `ground_slam`, `leap_strike`); energy-type labels (`rage`, `stamina-as-resource`); canonical library names (`Searing Wave`, `Iron Rend`).

**Convergence-shape implication:** every LLM naming call in `naming.py` receives these labels as prompt context. The LLM generates *against* them. Class names lean humanoid-fantasy because the prompt's labels lean humanoid-fantasy. The B14.5 sidecar finding that fire is over-represented at 23.6% vs 20% uniform expected (per memory note `project_b14_5_sidecar_analyses.md`) is one observational candidate consistent with this pattern, but **the terminology lock bars attributing that observation to Cluster B without per-variable evidence**. Cluster B's *structural presupposition* is observable in the prompt-construction code; the *contribution-to-fire-over-representation* is unmeasured.

**Genre-precedent grounding:** ARPG canon has *most* of Cluster B's labels as canonical-genre vocabulary. PoE has fire/cold/lightning (genre canonical); D2 has Barbarian/Sorceress/Necromancer/Paladin (genre canonical); STR/DEX/INT are universal across Diablo / PoE / Last Epoch / Grim Dawn. Isekai canon is *less* committed to these specific labels — the genre's defining works (Mushoku Tensei, Slime, Re:Zero) layer system narratives that can absorb any vocabulary the system commits to. The labels in Cluster B are **ARPG-genre-correct but isekai-genre-neutral**; isekai can take them or leave them; ARPG breaks if they go.

**Resolution lever:** three options per cluster sub-category (each label admits a different treatment):
- **Hide from LLM-visible surfaces** (Discipline #14 candidate). The cipher architecture does this for canonical-four element labels.
- **Rename to form-neutral vocabulary** at the engine layer. "rage" → "intensity"; "warrior" → "front-line." Risk: clinical/sterile.
- **Keep humanoid labels** and accept the bias as Phase-0 calibration. Phase-0 ships ARPG-canon-comfortable; post-Phase-0 work expands.

The strategic-axis lock in § 5 drives which sub-cluster gets which treatment.

#### Pattern P3 — The universal LLM-drift surface (Cluster E)

**Description:** Every LLM call in the generation seam exposes canonical-four labels. `naming.py:32-35` literally prepends `"Seasonal elements: fire={name}, wind={name}, water={name}, earth={name}"` to every class/monster/gear naming prompt. `selector.py:43-47` system-prompts "the season's four canonical role-slots (fire, wind, water, earth)" to the LLM. Doc 37 § 6's cipher architecture specifies these hidden; the code does not yet implement.

**Convergence-shape implication:** every per-season vocabulary the LLM produces is generated against canonical-four context. The cipher's "per-season vocabulary doesn't echo Earth-realm classical elements" intent is unenforced at the code surface. Per-season cosmologies that *should* be genuinely alien (Yomi's threshold; Deep Trench's pressure cosmology; the hypothetical music-spirit world) may quietly default-back toward fire/water/earth/wind analogs because that's what the prompt context is feeding.

**This is the cleanest implementation-vs-intent drift instance in the project.** The terminology lock allows the word *drift* here precisely: doc 37 § 6 specifies; the code contradicts; the comparison IS the drift. No measurement needed.

**Genre-precedent grounding:** both ARPG and isekai canons are agnostic to this. Neither genre depends on this drift being resolved or not. It is a *project-internal* discipline question — the cipher architecture was locked in doc 37 to enable cross-season cosmology variance; that architecture is not yet implemented. Resolving the drift unblocks cosmological variance the project itself wants.

**Resolution lever:** Discipline #14 candidate (Internal-vs-generative schema separation). The migration is mechanical once direction is locked — every LLM prompt-construction site is touched; canonical-four labels are stripped; per-season vocabulary fills the slot. Broad-surface change, low conceptual difficulty.

### 2.2 What we don't claim, per the terminology lock

The B14.5 sidecar findings (`project_b14_5_sidecar_analyses.md`) surface five aggregate observations:

1. Convergence iterations highest for controllers/mages, lowest for rogue/hunter
2. Hunter archetype has 1.82 modifier range — least consistent shape across seeds
3. Fight outcome distribution: draws 0.06%
4. Fire element over-represented at 23.6% vs 20% expected uniform
5. Close-range controllers exist (earth/fire/wind) — mage range constraint extension candidates

**Per the terminology lock, these are convergence-shape observations, not attributions.** We do not claim Cluster B's humanoid labels cause hunter's 1.82 modifier range. We do not claim canonical-four-in-prompt causes fire's 23.6% over-representation. These are candidate hypotheses; per-variable evidence does not exist. The form-bias work proceeds against the cluster-shape framing + the named patterns above, not against attribution claims.

If, after Position C migration + cipher migration + Cluster B labels-on-mechanics resolution, the convergence shape changes meaningfully (hunter's modifier range tightens; fire's over-representation closes; convergence-iteration distribution flattens), **that change becomes the evidence**. The staging discipline (§ 7) produces the comparison by design.

### 2.3 The PackProxy precedent — what it argues for

PackProxy (B10.2 ship) is the codebase's existing non-humanoid composite entity — a swarm modeled as a single mechanical opponent without per-individual schema. This is a precedent that the engine **can** hold non-humanoid composition. It argues the form-bias problem is **implementation-default**, not **architecturally inherent**.

The PackProxy precedent applies to the simulation seam (gamora's territory), not the generation seam (rocket's). The simulation can hold non-humanoid entities; generation cannot yet emit them as player-classes. The form-bias work's task is to extend the generation-seam precedent to match what simulation has already proven.

---

## 3. Q3 — Canon match: how the engine's substrate compares to ARPG and Isekai canons

Two parallel characterizations, each grounded in Legolas's five-pass research base. Citations are specific; per gandalf-design-lineage.md, vague comparisons are worse than no comparison.

### 3.1 Q3a — ARPG canon match

**ARPG canon's relationship to embodiment:** humanoid form is **load-bearing for the player vocabulary the genre depends on**. Across the genre's shipping reference points:

| Game | Hero embodiment | Class labels | Equipment vocabulary | Attribute vocabulary |
|---|---|---|---|---|
| Diablo II (2000) | Humanoid only | Barbarian / Sorceress / Necromancer / Paladin / Druid / Amazon / Assassin | weapon / armor / shield / amulet / ring / charm | STR / DEX / VIT / ENR |
| Diablo III | Humanoid only | Barbarian / Wizard / Witch Doctor / Monk / Demon Hunter / Crusader / Necromancer | weapon / off-hand / chest / pants / boots / etc. | STR / DEX / INT |
| Diablo IV | Humanoid only | Barbarian / Sorceress / Druid / Rogue / Necromancer / Spiritborn | weapon / off-hand / chest / pants / boots / etc. | STR / DEX / INT / WIL |
| Path of Exile | Humanoid only | Marauder / Witch / Ranger / Templar / Duelist / Shadow / Scion | weapon / off-hand / body armor / etc. | STR / DEX / INT |
| Last Epoch | Humanoid only | Acolyte / Mage / Primalist / Rogue / Sentinel (each with masteries) | weapon / off-hand / body armor / etc. | STR / DEX / INT / ATT / VIT |
| Grim Dawn | Humanoid only | Soldier / Demolitionist / Occultist / Nightblade / Arcanist / Shaman / Inquisitor / Necromancer / Oathkeeper | weapon / shield / chest / etc. | Physique / Cunning / Spirit |

**ARPG canon's relationship to elements:** the *exact* element-set varies, but a 5-7-type mechanical substrate is the modern reference. PoE has fire / cold / lightning / chaos / physical (5). D4 has fire / cold / lightning / poison / shadow / physical (6). Last Epoch has fire / cold / lightning / physical / poison / necrotic / void (7). Grim Dawn has 9 (physical / pierce / fire / cold / lightning / acid / vitality / aether / chaos). **None ship with a four-element substrate** — the canonical four is project-specific to Reincarnated, narrower than every shipping ARPG (per the canonical-elements one-pool thread analysis).

**ARPG canon's relationship to gear schema:** the weapon/armor/accessory schema is **inherited from D2 (2000)** and stable across all major shipping ARPGs through 2026. PoE's "uniques" are named items in this schema; D2's runewords are stat-bundles into this schema; Last Epoch's affixes layer onto this schema. The schema is **the player vocabulary**. Build identity is *expressed* through it. Players who came from any prior ARPG are fluent in it. Removing it would not be experimentation; it would be exit from the genre.

**Where the engine's current substrate sits relative to ARPG canon:**

- **Schema cluster (Cluster A):** **canon-aligned**. The weapon/armor/accessory schema is genre-correct. STR/DEX/INT attribute gating is genre-correct. Handedness 1h/2h is genre-correct. The engine reads as ARPG-canonical here.
- **Label cluster (Cluster B):** **mostly canon-aligned** with two notable narrowings. Class archetype labels (warrior/mage/rogue/hunter) sit in the genre's archetype taxonomy. STR/DEX/INT match every shipping ARPG. **The canonical-four element substrate is narrower than every shipping ARPG**; this is a project-specific narrowing (per the canonical-elements thread; per `engine-generic-meta-structure.md` cipher-licensee-configurable noting). The geometry labels (`melee_strike`, `ground_slam`, etc.) are genre-correct for ARPG combat verbs.
- **Form-agnostic cluster (Cluster C):** **canon-neutral**. Role-orientation taxonomy (damage / control / hybrid) is form-abstract; ARPG canon doesn't require it specifically. Skill role vocabulary (`primary_attack`, `burst_damage`, etc.) is genre-correct ARPG mechanical taxonomy.
- **LLM-drift surface (Cluster E):** **canon-orthogonal**. ARPG canon doesn't depend on cipher architecture being implemented.

**Net Q3a finding:** the engine's pre-LLM substrate is **ARPG-canon-comfortable**. It does not over-shoot genre conventions (no "ten-attribute system" or "exotic damage-type pool unlike anything in the genre"). It does not under-shoot in ways that would read as inexplicable to ARPG-fluent players (no missing the gear-slot vocabulary). The one narrowing (canonical-four substrate; Reincarnated's project-specific choice) is acknowledged in `engine-generic-meta-structure.md` as licensee-configurable, signaling the project knows the choice is project-specific.

**An ARPG-fluent player approaching Reincarnated finds nothing structurally alarming about the substrate.** They find familiar gear slots, familiar archetypes, familiar attribute vocabulary. The substrate does not displace them.

### 3.2 Q3b — Isekai canon match

**Isekai canon's relationship to embodiment:** the genre's defining narrative beat is *reincarnation-as-not-self*. Per Legolas Pass 1, the non-humanoid reincarnation sub-genre is one of three major contemporary sub-genres alongside villainess and slow-life isekai:

> *"Non-Humanoid Reincarnation (Slime / Spider / Dragon pattern). Protagonist reincarnates as a creature at the bottom of the power hierarchy, then evolves upward. Structural beats shared across this sub-genre: 1. Spawn/hatch with minimal power, RPG status screen confirms weakness. 2. Hunt weaker enemies → absorb abilities (slime) or level up (spider, dragon). ... Audience expectation: RPG-style progression (stat screens visible), evolution/class-change moments as narrative climaxes, eventual revelation that protagonist is among the most powerful in the world."*

**Specific isekai-genre embodiments shipped:** Rimuru Tempest (slime; Slime franchise's flagship protagonist), Kumoko (spider; So I'm a Spider, So What?), Catarina Claes (humanoid villainess; My Next Life as a Villainess), Dragon Hatchling 2024 (dragon at hatching), Vending Machine (literal vending machine; multiple light novel adaptations), Sword (sword; Reincarnated as a Sword), Slimy / monster / construct / undead lineages across the genre.

**Isekai canon's relationship to mechanics:** the genre **layers system narratives** on top of game-style stat displays. The protagonist gets a `"Skill: [Predation]"` or `"Title: [Demon Lord]"` and the system explains it. Per Legolas Pass 1: *"Audience expectation: RPG-style progression (stat screens visible), evolution/class-change moments as narrative climaxes."* Mechanics are *narrated*; the framing is meta-aware. This is the *opposite* of ARPG canon's "mechanics are mechanics; flavor decorates them" division.

**Isekai canon's relationship to embodiment vocabulary:** the genre's vocabulary explicitly admits non-humanoid frames. Slime's "viscosity" is a stat. Spider's "webs" are equipment. Dragon Hatchling's "scales" mature into armor over time. Vending Machine's "stock" is its skill kit. The vocabulary is per-embodiment, not universal-humanoid.

**Isekai canon's relationship to identity continuity:** per Layer 5 of `gandalf-design-lineage.md` (drawing on Studio Bind / Mushoku Tensei's work + 8bit / Slime's work): *the protagonist's internal voice is preserved across embodiment-shift.* Rudeus's pre-life and post-life voices are one continuous identity expressed through a different body. Rimuru's protagonist-voice is the same human-businessman-narrating-experience even when the body is amorphous. **The Earth Self framing in Reincarnated is recognizably this genre move.**

**Where the engine's current substrate sits relative to Isekai canon:**

- **Schema cluster (Cluster A):** **canon-incompatible.** The weapon/armor/accessory schema cannot express what Slime's viscosity or Spider's webs or Dragon Hatchling's scales-maturing-into-armor or Vending Machine's stock would be. The schema's shape presupposes humanoid anatomy. **This is the load-bearing structural gap doc 37 surfaced.**
- **Label cluster (Cluster B):** **canon-incompatible at the embodiment-narrative-vocabulary layer; canon-neutral at the mechanical-mathematical layer.** STR/DEX/INT as numbers can support any embodiment (a slime's "intelligence" is meaningful in-genre as a stat; the genre's audience reads stat screens fluently). STR/DEX/INT as *labels in player-facing surfaces* are humanoid-coded; isekai canon expects per-embodiment narrative.
- **LLM-drift surface (Cluster E):** **canon-tangential.** Cluster E is a project-internal discipline question; isekai canon doesn't depend on it.
- **Naming triad mechanics (Cluster D):** **canon-aligned.** Per `naming-triad.md`, Trial / Mirror / Passage are the universal frame; per-season variants are isekai-genre-canonical narrative skin. The Yomi pomegranate example in `naming-triad.md` is the level of cosmological-resonance the isekai genre's mainstream-medium register expects.

**Net Q3b finding:** the engine's pre-LLM substrate is **isekai-canon-incompatible at the embodiment layer, specifically at the schema-shape cluster (Cluster A)**. Outside that cluster, the engine is either isekai-canon-neutral (Cluster B mechanics; Cluster C) or already isekai-canon-aligned (Cluster D's naming-triad work).

**An isekai-fluent player approaching Reincarnated finds the *premise* genre-correct (reincarnation; spirit guide; seasonal-form-as-self; named Earth Self; samsaric structure) but the *mechanical substrate* genre-incompatible at the moment of embodiment variance.** When the game offers them a slime form, they encounter a schema that presupposes hands they don't have. The genre's contract is broken at exactly the moment isekai promised it would deliver — the embodiment moment.

**The project's name is Reincarnated. The gap is at the reincarnation moment specifically.** This is the structural finding doc 37 was reaching for.

### 3.3 Q3 synthesis — the gap is asymmetric

The engine's substrate is **ARPG-canon-comfortable across the board** and **isekai-canon-incompatible at one specific cluster** (Cluster A — gear/loadout schema). Outside that cluster, the isekai-incompatibility is either neutral or already partly-resolved.

**This is not a project-wide structural problem; it is a cluster-localized structural problem.** The fix is correspondingly localized: resolve Cluster A via Position C migration (doc 37 § 4); leave the ARPG-canon-comfortable parts in place; layer the isekai-narrative work at the embodiment-skin and convergence layers per `embodiment-narrative-layer.md`.

**The push/pull question (Q4) is not "which canon do we lock to entirely" — it is "where on each layer do we lock to which canon."** That framing produces an explicit-hybrid lock, not a single canonical-side commitment.

---

## 4. Q3.5 — Detour: the Reincarnated audience question, examined

Q4 needs a candidate framing for "audience prioritization" — the commission lists this as a Q4 sub-question. Worth pausing here because *the answer to Q4 depends materially on which audience Phase-0 ships to*.

**Pitch positioning (per `pitch-2026-05-18/one-pager.md`):** Reincarnated is positioned as *"isekai mobile ARPG"*. The hyphenation matters. Not "ARPG with isekai flavor." Not "isekai with ARPG mechanics." Both genres simultaneously, with the project's claim that the **isekai-positioned ARPG is an underserved Western market opening** per gandalf-design-lineage.md Layer 5: *"Western native-language games haven't met it on its own terms."*

**Western ARPG audience expectations (per Legolas Pass 2 + Pass 3 + Pass 4):** familiar gear/class/attribute schema; meaningful build differentiation; loot loop with item identity (D2 unique pattern, PoE unique pattern); endgame velocity meaningful per build (PoE mapping; D4 nightmare dungeons); class fantasy expressed through engagement pattern, not just visual; tolerable difficulty curve with player-skill ceiling.

**Western isekai-audience expectations (per Legolas Pass 1 + gandalf-design-lineage.md Layer 5):** reincarnation premise honored not subverted; meaningful embodiment variance (genre's non-humanoid sub-template is *core to the genre*, not a fringe); system-narrated mechanics (stat screens are read; skills get titles like `[Predation]`); identity continuity across embodiment shift; mythic register at journey moments (Trial, ascension); seriousness underneath the genre's frame (Mushoku Tensei / Slime mid-life-philosophy register, not KonoSuba's comedy register).

**The two audience expectations overlap meaningfully — and diverge meaningfully at one specific point.**

Overlap: stat screens; loot; mechanical progression; meaningful build identity; clear combat verbs; familiar pacing rhythms. ARPG and isekai audiences both read this fluently. Reincarnated's substrate (largely) honors both.

Divergence: **embodiment variance.** ARPG-audience-only would not require it (Diablo, PoE never have); isekai-audience-without-it walks away (the genre's non-humanoid sub-template is unmissable; "reincarnated as a slime" is the genre's most-cited example).

**Audience-prioritization conclusion (Phase-0):** Reincarnated cannot privilege one audience to the exclusion of the other; *the pitch's positioning fails immediately if it does*. The "isekai mobile ARPG" positioning is the explicit-hybrid commitment. Phase-0 needs:

- ARPG-audience comfort at the substrate-mechanical layer (familiar gear schema; build identity; loot rhythm; combat verbs)
- Isekai-audience commitment at the embodiment-narrative layer (the slime form is *a slime*, not a flavored humanoid; the schema admits it; the narrative skin renders it; the system narrates it)

**This is the locked sub-positions framing for Q4 (§ 5).**

---

## 5. Q4 — Push/pull: the decision framework + the strategic-axis lock

### 5.1 The locked strategic-axis position — explicit-hybrid with two sub-locks

**Strategic-axis lock recommendation (Matt's call to make final):**

> **Phase-0 lands as explicit-hybrid with two locked sub-positions:**
>
> - **(a) ARPG-canon-primary at the substrate-mechanical layer.** Cluster A's mechanical schema preserved as locked in doc 37 § 4 Position C. Cluster B's mechanical math preserved (attribute math; element-tagged scaling; archetype templates). The engine ships with a substrate ARPG-fluent players will recognize at first contact.
> - **(b) Isekai-canon-primary at the narrative-skin and convergence layers.** Embodiment axis added per `embodiment-narrative-layer.md`. Position C's narrative-skin rendering implemented. Cipher architecture (doc 37 § 6) implemented per Discipline #14 candidate. Per-season vocabulary generates against the cipher's abstract pair-structure; canonical-four labels hidden from LLM. The naming triad's per-season variants surface cosmological resonance per `naming-triad.md`.

**Phase-0 vs post-Phase-0 split:**

- Phase-0 (current seasonal-journey portion): the explicit-hybrid lock above. ARPG-mechanics + isekai-narrative-skin.
- Post-Phase-0 (Earth meta-layer; per `cosmology-reincarnated.md` § "Ascension and the Court" + memory note `project_earth_meta_layer.md`): the Court's accumulation pattern is fundamentally isekai (Solo Leveling's Shadow Army precedent per Layer 5 of design-lineage). The form-library mechanism leans *more* isekai-side. Phase-0's ARPG-mechanics-substrate persists; the meta-layer presentation goes deeper into isekai canon.

### 5.2 Position C revisit — recommended NOT to revisit

The commission asked whether Q4's analysis surfaces a Position C revisit. **Recommendation: do not revisit. Reaffirm.**

Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin) is the exact architectural shape this strategic-axis lock requires. It preserves ARPG-canon at the mechanical layer (slot is functional; mechanical contribution identical across embodiments) and admits isekai-canon at the narrative-skin layer (per-embodiment vocabulary; per-season L3 modulation possible).

Position A (mechanically-identical slots + identical labels per embodiment) would over-prioritize ARPG-canon and break isekai-canon at the narrative-skin layer. Rejected.

Position B (mechanically-different per embodiment; e.g., slimes have no offensive slot) would over-prioritize isekai-canon and break the ARPG-canon mechanical-substrate. Rejected in doc 37 § 4; reaffirmed here.

Position C remains operative. The work is *implementing* it, not revisiting it.

### 5.3 The four catalogue-track sub-locks — deferred-pending-experiment

Per `pre-llm-substrate-inventory.md` § 11, four specific locks are explicitly deferred to catalogue-track findings. The strategic-axis lock (§ 5.1) can land without them; the four sub-locks resolve at named catalogue milestones; they each inherit the strategic-axis context.

| Sub-lock | Resolves when | Strategic-axis context |
|---|---|---|
| **Cipher-width** (Options A/B/C from the parked canonical-elements thread) | Elrond's emergent-grouping analysis runs against the full Pimen crawl + any additional Tier-1 catalogue sources | Three-layer model (substrate / grouping / vocabulary) per § 6.2 below. Cipher width is whatever the catalogue's abstraction layer produces; we discover it, we don't pick it. |
| **Foundation layer placement** (Flag B from rocket inventory; `foundation/foundation.py:39-43` hard-codes 4-rotating + 1-physical) | Cipher-width decision + L1/L2 placement decision both land | Foundation either grows with the substrate (cipher-coupled) or decouples (substrate becomes L2 Reincarnated-cosmology concept; Foundation stays as engine-substrate concept). Per `engine-generic-meta-structure.md` three-layer model. |
| **D1 element-name pool reconsideration** | Cipher architecture is determined AND Flag A rubric-screening test runs (§ 6.5) | The 156-entry pool's allow-list / eligible / quarantine structure may or may not survive cipher migration; reconsideration is much larger than entry-by-entry review (the pool approach itself may not survive). |
| **Per-season vocabulary coupling policy** (α validation+regenerate / β in-prompt constraint / γ runtime fallback) | Catalogue-mapping-and-grouping experiment lands findings | Surfaced 2026-05-16 Day 4. Choice depends on empirical mapping behavior of representative per-season vocabulary against catalogue tag space. |

**Note on the "parallel-workstream" mandate:** Matt's 2026-05-16 directive was to **not block VS2b on VS2a**. This strategy doc lands now per Path (b). The four sub-locks above are explicitly NOT blockers for the strategic-axis lock in § 5.1 or for the cadence options in § 7. They are blockers for specific downstream dispatches (cipher-migration dispatch; D1 reconsideration dispatch; per-season vocabulary integration dispatch). The cadence options below name where they enter.

### 5.4 The decision framework — for Matt + future similar work

The commission asked for a decision framework Matt can use. The framework lands as four questions, applied per-cluster:

**Question 1 — Which canon is load-bearing for this cluster?**
- Cluster A: ARPG (audience vocabulary) AND isekai (embodiment variance). Both. Hybrid resolution required.
- Cluster B (mechanics-side): ARPG (familiar math). One canon load-bearing.
- Cluster B (label-side): isekai-friendly with ARPG-genre-readable labels possible. Hybrid resolution possible.
- Cluster C: neither (form-agnostic). No canonical commitment needed.
- Cluster D: aligned with isekai-canon via naming-triad work. Already resolved.
- Cluster E: project-internal discipline question; canon-orthogonal.

**Question 2 — Where does the cluster meet the player?**
- Cluster A: at the equipment moment. Build-identity decision-point. ARPG-audience reads here continuously; isekai-audience reads here at embodiment-shift moments.
- Cluster B: at the class-creation moment, the skill-naming moment, the gear-naming moment. Both audiences read here.
- Cluster C: in the engine's internal logic primarily; player-facing surface is downstream.
- Cluster D: at the encounter-moment (Trial / Mirror / Passage). Both audiences read here; isekai-canon's mythic-register expectation is the higher bar.
- Cluster E: at the LLM-output surface. Both audiences read what the LLM produces; neither audience reads the prompt.

**Question 3 — What resolution lever fits this cluster?**
- Cluster A: schema migration (Position C). One coordinated change.
- Cluster B (mechanics): keep. Math stays form-agnostic.
- Cluster B (labels): three options (hide / rename / accept). Strategic-axis lock drives which.
- Cluster C: no change required.
- Cluster D: maintain the naming-triad work; integrate per-season variants at cipher implementation time.
- Cluster E: prompt-construction filter (Discipline #14).

**Question 4 — What does this cluster's resolution cost in audience-vocabulary disruption?**
- Cluster A: ARPG-vocabulary preserved (slot mechanic stays); isekai-vocabulary added (narrative-skin layer). Low ARPG cost; high isekai gain.
- Cluster B (mechanics): zero cost. Math unchanged.
- Cluster B (labels): cost depends on treatment. *Hide* costs nothing player-facing. *Rename* costs ARPG-vocabulary familiarity. *Keep* costs isekai-vocabulary opportunity.
- Cluster C: zero cost.
- Cluster D: zero cost (the work is already specified).
- Cluster E: cost is internal-discipline-cost (the migration), zero player-facing cost.

**The framework's discipline:** each cluster's resolution lever is applied independently. **Form-bias work does not collapse into a single architectural decision; it's a coordinated bundle of cluster-localized decisions with shared discipline (Discipline #13a/#13b/#14).**

### 5.5 The recommended strategic-axis lock — explicit

**For Matt's approval:**

> **Recommendation:** Lock explicit-hybrid Phase-0 with sub-positions (a) ARPG-canon-primary at substrate-mechanical layer and (b) Isekai-canon-primary at narrative-skin and convergence layers. Reaffirm Position C. Defer the four catalogue-track sub-locks (cipher-width; Foundation layer; D1 reconsideration; per-season vocabulary coupling) to their named gates. Author Disciplines #13a + #13b + #14 candidates against the terminology-locked framing.

This is the strategic-axis lock. Per the commission's instruction, **the final call is Matt's**. The recommendation above is gandalf's design-instinct, grounded in the cluster framing + the canon-match analysis + the audience-prioritization analysis. Knight-rider drafts the decisions-log entry per ADR-002.

---

## 6. The architecture this strategy implies — three-layer model + cipher-width framework

The strategic-axis lock in § 5.1 plus the four deferred sub-locks in § 5.3 are operationally expressed through a refined three-layer architecture that absorbs both the locked work (doc 37 § 6 Position (ii) cipher; Position C; embodiment axis) and the deferred catalogue-track work.

### 6.1 The three layers, refined

Per `pre-llm-substrate-inventory.md` § 10 (which itself refines `engine-generic-meta-structure.md` § "The three-layer model"):

| Layer | What it is | What sees it |
|---|---|---|
| **Substrate** | Catalogue's emergent abstraction tag space. Currently Pimen's 9 (fire/water/earth/wind/ice/holy/dark/thunder/acid); eventually whatever Elrond's abstraction analysis produces from the full Tier-1 crawl set. | Engine-internal only. LLM never sees substrate labels. Resistance translation + visual-coverage map happen here. |
| **Grouping** | The active per-season opposition structure. Selected from a finite set of valid groupings derived empirically from the substrate. 4-5 active tags per season; chosen for thematic coherence + mechanical distinctness + role-orientation coverage. | The LLM may see the grouping *structure* (primary opposition / secondary opposition slots — abstract labels) but not the substrate tag *identities*. The player feels the grouping's archetypes in combat. |
| **Vocabulary** | Per-season LLM-generated names for the grouping's slots. Pressure/vacuum/bioluminescence/decay for deep-sea; harmony/dissonance/melody/rhythm for music-spirit. | Player + the rest of the LLM call chain see this. Player-facing surface lives here. |

This is the **architecture the strategic-axis lock and the catalogue-track work converge on.** It absorbs doc 37 § 6's two-layer cipher (substrate + vocabulary) by adding the grouping layer between. It does NOT contradict doc 37 § 6; it refines it.

**Why three layers and not two (load-bearing):**

The two-layer cipher (substrate + vocabulary) faces the genre-canon constraint that no shipping ARPG ships above ~6-7 simultaneously-active mechanical damage types. The player-cognition ceiling on working combat memory caps simultaneous-active types at 5-7 (per Legolas Pass 4 + Pass 5 + Hollow Knight's 45-charms-but-5-8-active pattern). Substrate-wider-than-7 with all tags active per season violates the ceiling and produces Last Epoch / Grim Dawn-style mechanical overlap that players struggle to distinguish in combat.

The grouping layer absorbs the bandwidth tension. Substrate is wide (catalogue coverage); active grouping is narrow (4-5 tags); player's working combat memory load is genre-canonical. Seasonal rotation across different groupings provides cross-season variety that no shipping ARPG has the procedural-generation primitive to deliver.

**Genre-internal precedents** for the substrate-wide / active-narrow pattern: Solo Leveling's Shadow Army (100+ accumulated; 5-8 active per fight); Hollow Knight's charms (45 charms; 5-8 notch-equipped). The pattern ships when the active set per session passes mechanical-distinctness and role-coverage filters.

### 6.2 The cipher-width framework — explicit even with cipher-width deferred

The cipher-width decision (Options A/B/C from the parked canonical-elements thread) **is one of the four catalogue-track sub-locks deferred to experiment findings**. Per Matt's parallel-workstream mandate, this doc lands the framework now even with the specific decision deferred. When the catalogue-mapping-and-grouping experiment returns, the framework below is applied to its findings.

**Decision criteria for cipher-width (applied when experiment returns):**

1. **Substrate-coverage criterion.** The substrate-layer width is determined by the catalogue's emergent abstraction tag space. Whatever Elrond's analysis produces is what the substrate-layer ships with. We discover the width; we don't pick it.
2. **Grouping-viability criterion.** The grouping-layer width per season is determined by:
   - Mechanical-distinctness (4-5 substrate tags whose mechanical signatures distinguish in combat)
   - Role-orientation coverage (the season's grouping admits damage / control / hybrid orientations against the active tags)
   - Thematic coherence (the season's anchor + cosmology admits the grouping as natural; doesn't feel arbitrary)
   - Genre-recognition (Western ARPG-audience reads the grouping as legible)
3. **Outcome possibilities:**
   - **3-5 robust groupings emerge** passing all three filters → multiple-groupings architecture viable; the seasonal rotation gains cross-season grouping variance as a structural pillar
   - **1-2 groupings survive** → refined-Option-A collapses to a single fixed grouping; the cipher becomes a single 4-5-tag opposition structure derived from the substrate; cross-season variety is in vocabulary + anchor, not in grouping
   - **No grouping survives** → the canonical-four cipher remains operative; catalogue-curation translation handles the substrate-to-VFX mapping at the visualization layer; doc 37 § 6 cipher is unchanged

4. **Strategic-axis context (from § 5.1):** the cipher-width decision lands within the explicit-hybrid Phase-0 lock. Whichever outcome the experiment surfaces, the substrate-layer remains internal (ARPG mechanics preserved); the grouping-layer determines what LLM sees structurally (isekai-narrative-flexibility preserved). All three outcomes are compatible with the strategic-axis lock.

5. **Foundation layer placement** (Flag B): resolves jointly with cipher-width. If the substrate is Pimen-derived (9 tags), Foundation either grows to 9 (Foundation-coupled-to-substrate; engine treats substrate as L1) or decouples (substrate becomes L2 Reincarnated-cosmology concept; Foundation stays at 4-rotating-plus-1-physical as L1 generic). The decision is L1/L2 ownership; the catalogue experiment + Matt's L1/L2 call determines.

### 6.3 The cipher architecture stays operative

Per doc 37 § 6 Position (ii) and the operationalized work in `naming-triad.md` + `embodiment-narrative-layer.md` + `engine-generic-meta-structure.md`:

- Per-season vocabulary carries own mechanical signatures
- Cipher does resistance translation only (not mechanical-signature gating)
- Canonical-four labels hidden from LLM
- Per-season vocabulary is what the LLM generates; LLM sees abstract pair-structure (Primary / Secondary) at the grouping layer
- **Ailment-damage-signatures work flagged as load-bearing for the doppelganger gate under Position (ii) *when per-season vocabulary diversifies into pure-control archetypes*** (amendment 2026-05-16 post-jack-ryan Gate 1 WARN-1; original phrasing "re-activated as load-bearing dependency" was an overcommitment — the memory note `project_ailment_damage_thematic.md` records the design as DEFERRED with a measurement-triggered revisit condition that has not yet been satisfied). Current state: ±25% per-fight variance escalation (KI-B6-1 resolution) is holding the doppelganger gate on canonical-four substrate; B14.5 V1 calibration epoch has landed (2026-05-16 commit `c000d7d`) but the post-V1 doppelganger gate re-run has not yet been run. Deferral-lifting timing pends that re-run per the memory note's high/medium/urgent signal triggers. The coupling is *design-architecturally tight* (Position (ii) requires per-season mechanical signature variety; pure-CC-no-damage signatures break the gate empirically) but *immediate-timing loose* (current variance-escalation is holding); the coupling tightens at future-implementation time when cipher migration produces per-season pure-control-coded vocabulary that variance-escalation alone may not hold against. See also strategy doc § 9.1 (rocket cascade) "Future" framing — that framing is the operative status until the re-run resolves.

The three-layer model **refines** this architecture; it does not replace it. Position (ii) is preserved. The cipher's resistance-translation job is preserved. The new grouping layer adds the per-season opposition selection between substrate and vocabulary.

### 6.4 The five resolution levers — applied per cluster

This is the operational expression of the framework. Per § 5.4's decision framework + § 6.1's three-layer model:

| Cluster | Resolution lever | Layer it touches | Strategic-axis context |
|---|---|---|---|
| **A** | Position C schema migration (gear → augmentation; embodiment axis added; off_hand stays handedness-gated mechanically; player-facing labels per-embodiment) | Engine schema (rocket); JSON contract (star-lord); display (drax) | (a) ARPG-mechanic preserved + (b) isekai-narrative-skin layer added |
| **B (mechanics)** | Keep. STR/DEX/INT math; canonical-four scaling math; archetype templates; geometry mechanics; energy-pool mechanics | Engine internal | (a) ARPG-mechanic preserved |
| **B (labels, LLM-visible)** | Hide canonical-four labels; surface per-season vocabulary at grouping + vocabulary layers; per-embodiment label rendering for attribute axes / class archetypes via embodiment-narrative-layer lookups | LLM prompt-construction (star-lord); display (drax) | (b) isekai-canon-primary at LLM-visible surface |
| **B (labels, internal)** | Keep canonical-four as internal-only field names; keep `archetype_tag` as engine-internal classification; engine math stays form-agnostic-but-named-humanoid; player-facing renames via the embodiment-narrative-layer dual-label pattern | Engine internal | Strategic-axis transparent (internal-only) |
| **C** | No change | n/a | n/a |
| **D** | Maintain naming-triad work; integrate per-season variants at cipher implementation time | LLM prompt-construction (star-lord); display (drax) | (b) isekai-canon-aligned per existing work |
| **E** | Discipline #14 candidate — every LLM prompt-construction site stripped of canonical-four; per-instance vocabulary only; refactor the six named sites (naming.py:26-36, :87, :89; selector.py:43-47, :394-446; library_generator.py:85) | LLM prompt-construction (star-lord) | Project-internal discipline |

### 6.5 The two empirical experiments — their explicit framing

The form-bias work depends on two named empirical experiments, both already-scoped as request files. Their framing under this strategy:

**Experiment 1 — No-seed cosmology generation test** (`agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`)
- **What it tests:** residual-bias under cipher migration. After canonical-four labels are hidden from LLM, does the LLM still default-back to fire/water/earth/wind analogs because those patterns are deeply trained-in?
- **Decision it informs:** whether Cluster E's migration is sufficient on its own, or whether additional anti-bias scaffolding is required at prompt-construction time.
- **Runs at:** Stage-3 gate of the cipher migration (per the staging discipline in § 7). NOT before; the test requires the cipher migration to be in place to be meaningful.
- **Strategic-axis dependency:** none. The test runs regardless of which catalogue-track sub-lock outcome lands.

**Experiment 2 — Catalogue-mapping-and-grouping experiment** (`agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`)
- **What it tests:** per-season vocabulary coupling against catalogue tag space; viability of multiple-groupings architecture; D1 rubric humanoid-fantasy screening (Flag A).
- **Decisions it informs:** all four deferred catalogue-track sub-locks (cipher-width; Foundation layer placement; D1 rubric reconsideration scope; per-season vocabulary coupling α/β/γ choice).
- **Runs at:** soon (when Matt-authorized budget allows). Sibling to this strategy doc per the parallel-workstream mandate.
- **Strategic-axis dependency:** strategic-axis lock unaffected by the outcome. Sub-locks resolve based on outcome; strategic-axis is structurally independent.

**Flag A — D1 rubric screening targeted test:** a small sub-experiment of Experiment 2 OR a separate small commission running the D1 rubric's five yes/no scoring questions on a curated set of non-humanoid-cosmology candidate words (e.g., pressure, vacuum, bioluminescence, decay, entropy, resonance, drift, currents). If the rubric reliably under-scores them (Flag A confirmed), the D1 pool reconsideration needs structural rebuild not entry-by-entry review. If the rubric scores them as expected (Flag A negated), the pool reconsideration is bounded.

---

## 7. Cadence options (I/II/III) reformulated against the strategic-axis lock

The form-bias cadence options (Options I/II/III from doc 37 § "Cadence options" — held pending strategy-doc landing per the dispatch context) are now reformulated against the strategic-axis lock + the three-layer model + the deferred catalogue-track gates.

**Critical reframing:** the cadence work is *staged*, not *paced*. The staging discipline (per the Day-4 re-engagement section in `canonical-elements-one-pool.md`) is the load-bearing discipline; the "cadence options" are now stage-sequencing choices, not delivery-velocity choices.

### 7.1 The four-stage migration sequence (locked across all cadence options)

All cadence options share the same four-stage backbone. The options vary in *when* each stage opens and *what runs in parallel*, not in *what the stages do*.

**Stage 1 — Add embodiment-axis as new optional field. No removals.**
- Engine emits `embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`, `class_role_function`, `gear_slot_labels`, `per_season_narrative_modulation` per `embodiment-narrative-layer.md` § "Engine emit requirements"
- Position C's schema migration shape; existing gear schema stays mechanically; embodiment fields are additive
- Rocket dispatch territory. Schema-additive only. MIGRATION.md required.
- **Verifies:** schema migration mechanics work. Position-C migration's mechanical-substrate stays operative through migration.
- **Strategic-axis dependency:** sub-lock (a) ARPG-canon-mechanical-preserved confirmed by Stage 1 leaving the mechanical schema untouched.

**Stage 2 — Abstract pair-structure (grouping layer) added alongside canonical-four.**
- Engine emits per-season grouping data (Primary Opposition / Secondary Opposition labels) alongside canonical-four; LLM receives both during transition
- Convergence shape compared across the same telemetry frame; "free measurement" of grouping-vs-canonical-four side-by-side
- Rocket + star-lord dispatch territory; schema-additive at engine; prompt-construction-additive at star-lord
- **Verifies:** the grouping layer functions; per-season grouping selection works; LLM produces coherent per-season vocabulary against grouping structure
- **Strategic-axis dependency:** sub-lock (b) isekai-canon-narrative-convergence work begins to land here. The grouping layer is the first cross-cluster commitment to isekai-canon at the LLM-visible surface.

**Stage 3 — Hide canonical-four from LLM (cipher migration).**
- Star-lord dispatch territory. Discipline #14 candidate enforcement at every prompt-construction site.
- `naming.py`, `selector.py`, `library_generator.py` filtered; per-instance vocabulary replaces canonical-four labels in prompts
- The six named drift sites from Cluster E refactored
- **Experiment 1 (no-seed cosmology test) runs at this gate.** If residual-bias is confirmed, additional anti-bias scaffolding lands before Stage 4. If negated, Stage 4 proceeds directly.
- **Verifies:** cipher architecture's cosmology-emergence works; per-season vocabulary is genuinely per-season; canonical-four is fully hidden
- **Strategic-axis dependency:** sub-lock (b) fully landed at the cipher layer. Cluster E drift resolved.

**Stage 4+ — Embodiment-as-narrative-skin in display; gear→augmentation rename; consumer cleanup.**
- Drax dispatch territory primarily; star-lord follow-on for LLM-flavor work.
- Loadout UI rename (weapon → main-hand-augmentation per the active embodiment's L2 vocabulary); demo display per-embodiment lookups; combat-text generation per-embodiment vocabulary
- Engine-internal field renames (gear → augmentation; doppelganger → mirror; optional housekeeping per `naming-triad.md` § "Engine-side telemetry retention")
- D1 pool reconsideration (post Flag A test result; pool restructure OR rebuild per the test outcome)
- Trait architecture per-embodiment narrative skin (humanoid Knight's per-class intrinsic traits vs slime Bulwark's per-class intrinsic traits — same mechanical contribution; per-embodiment narrative naming)
- **Verifies:** the full strategic-axis lock has reached every cluster's resolution surface.

### 7.2 The three reformulated cadence options

The cadence options differ in *what runs in parallel* and *what gates pause for catalogue-track findings*. All three honor the strategic-axis lock from § 5.1.

#### Option I — Sequential (lowest risk; longest calendar)

Stages 1 → 2 → 3 (with Experiment 1) → 4. Each stage completes before the next begins. Catalogue-track sub-locks resolve at their own gates without blocking the migration sequence; if catalogue findings arrive during Stage 2 or 3, they inform Stage 4's content (D1 reconsideration; cipher-width final form).

- **Pros:** lowest coordination cost; each stage's evidence accumulates before the next; minimal multi-seam parallel work
- **Cons:** longest calendar; demo2 dependencies may slip (Position C migration is a Stage 1 prerequisite for demo2 embodiment-aware UI)
- **Best for:** if cross-seam bandwidth is constrained AND demo2 timing has flex
- **Approximate timeline:** 8-12 weeks total against current ~9-entity team capacity

#### Option II — Parallelized (recommended; balanced risk)

Stages 1 + 2 run in parallel after Stage 1 schema work is mid-flight. Stage 3 (cipher migration) starts after Stage 2 lands; Experiment 1 runs at Stage 3 gate. Stage 4 starts after Stage 3 lands. Catalogue-track sub-locks resolve at their gates; if they land during the migration sequence, their outcomes feed into the relevant stage's content.

- **Pros:** balanced calendar; substrate work and cipher-grouping work overlap usefully; Stage 4's content benefits from catalogue findings
- **Cons:** moderate coordination cost; rocket + star-lord coordination required during Stages 1-2 overlap
- **Best for:** the recommended default if no specific constraint dominates
- **Approximate timeline:** 5-8 weeks total against current capacity

#### Option III — Aggressive (highest risk; shortest calendar)

Stages 1 + 2 + Stage-3-prep run in parallel from the start. Stage 3's cipher migration begins as soon as Stage 2's grouping infrastructure is ready, with Experiment 1 running as an early gate inside Stage 3 rather than at its end. Stage 4 may begin opportunistically during Stage 3 on display-side work that doesn't depend on cipher implementation completion.

- **Pros:** shortest calendar; demo2 dependency unblocked earliest; tightest feedback loop on whether the integrated form-bias work converges
- **Cons:** high coordination cost; multi-seam parallel work risk; Experiment 1's results may force re-work if residual-bias confirms; rocket + star-lord + drax simultaneous bandwidth required
- **Best for:** if demo2 dependency is the binding constraint AND team bandwidth supports it
- **Approximate timeline:** 3-5 weeks total against current capacity (with elevated risk of mid-stage rework)

### 7.3 Cadence recommendation

**Recommendation: Option II (Parallelized).** Reasons:

- The strategic-axis lock + the three-layer model + the four-stage sequence are all mature enough to support parallel Stage 1-2 work without ambiguity
- Stage 3's cipher migration depends on Stage 2's grouping infrastructure but does not require Stage 1's embodiment-axis work to complete (they touch different surfaces)
- The catalogue-mapping experiment's results land at a time that naturally informs Stage 4 (D1 reconsideration; per-season vocabulary coupling final policy), not earlier-stage work
- Per the parallel-workstream mandate, Option II preserves throughput without inviting the coordination risk of Option III

**Per Matt's call:** the final cadence choice (I/II/III) is Matt's. The strategic-axis lock from § 5.1 is locked-when-Matt-approves; the cadence choice is the operational sequencing for that lock.

### 7.4 What each stage unblocks

- **Stage 1 completes →** demo2 embodiment-aware display work; B-series engine work that consumes `embodiment_tag`; the kit-anchor rename dispatch's scope clarifies
- **Stage 2 completes →** per-season grouping data available downstream; loadout / drax / Pimen integration can begin consuming the grouping layer; cross-season visual-coverage map is computable
- **Stage 3 completes →** cipher architecture operationally live; cluster E drift resolved; Discipline #14 enforced at every prompt site; Experiment 1's residual-bias finding lands
- **Stage 4 completes →** full strategic-axis lock has reached every cluster; the form-bias work is structurally complete; ongoing maintenance is Discipline #13a/#13b/#14 enforcement at gates, not architectural change

---

## 8. Decisions-log derivation notes (for knight-rider to draft)

Per ADR-002 process: knight-rider drafts; jack-ryan Gate 1; Matt approves; commit. The following entries should derive from this strategy doc.

### 8.1 Strategic-axis lock entry

**Title (suggested):** *Form-bias strategic-axis locked as explicit-hybrid Phase-0: ARPG-canon-primary at substrate-mechanical layer + Isekai-canon-primary at narrative-skin and convergence layers*

**Source sections:** § 5.1 + § 5.2 + § 5.4 + § 5.5
**Authority:** Matt approval; cross-seam framing impact (affects rocket schema + star-lord LLM prompts + drax display + future content authoring)
**Locks:** the explicit-hybrid framing; the two sub-positions; Position C reaffirmation; the four-cluster decision framework

### 8.2 Three-layer model + cipher-width framework entry

**Title (suggested):** *Form-bias architecture lands as three-layer model (substrate/grouping/vocabulary); cipher-width framework explicit with width itself deferred to catalogue-mapping experiment*

**Source sections:** § 6.1 + § 6.2 + § 6.3
**Authority:** Matt approval; refines doc 37 § 6 cipher architecture (preserves Position (ii) lock)
**Locks:** the three-layer model as the operative architecture; the cipher-width decision criteria; the framework's compatibility with all three cipher-width outcomes (Options A/B/C from the parked canonical-elements thread)

### 8.3 Four catalogue-track sub-locks deferred entry

**Title (suggested):** *Four form-bias sub-locks (cipher-width, Foundation layer placement, D1 reconsideration, per-season vocabulary coupling) explicitly deferred to catalogue-track empirical gates*

**Source sections:** § 5.3 + § 6.5
**Authority:** Matt approval; documents the deferred status + the gates that resolve each
**Locks:** the four sub-locks as explicitly deferred (not stale; not lost); the gates that resolve each; the framework that absorbs their resolutions

### 8.4 Disciplines #13a + #13b + #14 codification entry

**Title (suggested):** *Disciplines #13a (implementation-vs-intent drift) + #13b (outcome attribution opacity) + #14 (internal-vs-generative schema separation) codified into engineering-disciplines.md*

**Source sections:** § 1.3 + § 2.1 + the terminology lock from `pre-llm-substrate-inventory.md` § 3
**Authority:** Matt approval; codifies the gate-level checks; routes via jack-ryan for engineering-disciplines.md authorship
**Locks:** the three disciplines as named, the terminology lock as the constraint, the triggerable Gate-1 questions for each

### 8.5 Cadence option lock entry

**Title (suggested):** *Form-bias migration cadence: Option II (Parallelized) locked as the staged sequence; four-stage backbone + per-stage gate definitions*

**Source sections:** § 7
**Authority:** Matt approval; determines cross-seam dispatch sequencing
**Locks:** the four-stage backbone; Option II as the cadence; the per-stage unblock cascade

---

## 9. Cross-seam cascades — what this doc unblocks per seam

Per the form-bias work's documented cross-seam impact (doc 37 § 11), this strategy doc's locks produce specific dispatch-authoring cascades. Each cascade is named here with the strategic-axis context that frames its content.

### 9.1 Rocket cascade

**What unblocks:** the kit-anchor rename dispatch (held pending cadence choice); the embodiment-axis generation dispatch (Stage 1 work); the per-class-per-embodiment L1 starter-gear generation dispatch (Stage 4 work); the cipher-architecture pair-structure layer dispatch (Stage 2 work); the eventual D1 pool reconsideration dispatch (post-Flag-A test).

**Sequencing per Option II:**
1. Stage 1 — embodiment-axis emit fields (`embodiment_tag`, `embodiment_anatomy_tags`, etc.) per `embodiment-narrative-layer.md`
2. Stage 2 — abstract pair-structure layer emission (per-season grouping data alongside canonical-four)
3. Stage 4 — gear → augmentation rename (display-coordinate with drax); D1 reconsideration (post Experiment 2 + Flag-A test)
4. Future — ailment-damage-signatures work (re-activated per doc 37 § 6.4; load-bearing for doppelganger gate under Position (ii))

**Strategic-axis context:** rocket preserves the ARPG-canon-mechanical-substrate (sub-lock a) at every dispatch; the narrative-skin layer (sub-lock b) lands at the schema-emit and display-coordination boundaries.

### 9.2 Star-lord cascade

**What unblocks:** the LLM prompt-leak audit dispatch (Stage 3 work; the six Cluster E drift sites refactored); the per-season cosmological-vocabulary generation dispatch (Stage 2 work; integrates with `naming-triad.md` per-season variant generation); the visual_prompt LLM field work for per-embodiment narrative skin (Stage 4 work).

**Sequencing per Option II:**
1. Stage 2 — per-season cosmological-vocabulary generation call integrated with grouping layer; LLM sees grouping abstract labels, not canonical-four
2. Stage 3 — full Cluster E refactor; every prompt-construction site filtered against Discipline #14 candidate; Experiment 1 runs at this gate
3. Stage 4 — visual_prompt LLM field per-embodiment narrative skin work; per-season L3 modulation generation for embodiment vocabulary (per `embodiment-narrative-layer.md` § "For star-lord")

**Strategic-axis context:** star-lord enforces sub-lock (b) at the LLM-visible surface; the canonical-four is hidden; per-season vocabulary is what reaches the LLM and player.

### 9.3 Gamora cascade

**What unblocks:** the doppelganger-mode validation dispatch under Position (ii) per-season mechanical signatures (Stage 2-3 work; ailment-damage-signatures consumed); the convergence-framework extension for the multi-dimensional divergence framework's player-behavior axis variance check (already locked in the engine-balance-stewardship decisions-log entry; awaits B-series scheduling).

**Sequencing per Option II:**
1. Stage 2 — doppelganger gate validation under per-season mechanical signatures (works without cipher migration; per-season vocabulary is what the gate validates against)
2. Stage 3-4 — convergence-framework extension for multi-dimensional divergence; per-embodiment archetype variance check at class generation time

**Strategic-axis context:** gamora preserves the ARPG-canon-mechanical-balance (sub-lock a) at the simulation layer; per-season mechanical-signature variety is the isekai-canon affordance that the gate must validate without breaking.

### 9.4 Drax cascade

**What unblocks:** the display-leak audit dispatch (Stage 1-4 work; loadout / demo / character-sheet consumers updated as embodiment_tag flows through); the body-swap inventory transition UI work (Stage 4); the embodiment-visualization work (Stage 4; per-embodiment sprite + slot-rendering); the Court / Spirit Guide eventual Earth-Self hub work (post-Phase-0 territory; informed by this strategy).

**Sequencing per Option II:**
1. Stage 1 — display consumers updated to read `embodiment_tag`; per-embodiment lookup from `embodiment-narrative-layer.md` for gear-slot labels in loadout UI
2. Stages 2-3 — per-season vocabulary display flows; canonical-four labels removed from player-facing surfaces (Loadout.tsx:67, Sample.tsx:29, characterSheet.ts:224 — the three drift sites confirmed in the Day-4 re-engagement)
3. Stage 4 — body-swap inventory transition UI; per-embodiment visual register coverage (humanoid / slime / beast / dragonling / swarm / construct / spirit / plant sprites)

**Strategic-axis context:** drax delivers sub-lock (b) at the player-facing surface; per-embodiment narrative skin renders; the player sees the isekai-canon embodiment variance honored at the moment of body-swap.

### 9.5 Elrond cascade

**What unblocks:** the catalogue-mapping-and-grouping experiment authoring (already commissioned per `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`); the substrate-layer abstraction-analysis dispatch (post-experiment; emerges from experiment findings); the cipher-width final form dispatch (post-experiment + Matt's Foundation layer placement decision).

**Sequencing:** parallel to the Option II main migration sequence. Elrond's catalogue work is the supplier of the four deferred sub-lock resolutions; its sequencing is its own (per the catalogue work's gates), with outputs landing at the Stage 4 boundary of the main migration.

**Strategic-axis context:** elrond's work is independent of the strategic-axis lock (the catalogue produces what it produces); the experiment outputs *inform* the sub-lock resolutions; the strategic-axis itself is structurally independent of the experiment outcome.

### 9.6 Legolas cascade

**What unblocks:** the asset-catalogues Tier-1 full crawls (already authorized per the catalogue-based form-bias resolution path in doc 37); the per-embodiment sprite-coverage commission (a known gap per `style-register.md` § "Per-embodiment register awareness"); any follow-on research commissions surfaced by the catalogue experiment's findings.

**Sequencing:** parallel to all other seams. Legolas's catalogue crawl work is the supplier of the catalogue data; the per-embodiment sprite-coverage commission is the supplier of the data drax needs for Stage 4's embodiment-visualization work.

**Strategic-axis context:** legolas's work delivers the substrate the strategic-axis depends on; per the score-don't-filter principle (per AGENTS.md), crawls are broad; consumption-time filters by the locked HD-2D-pixel register handle the surface flow.

---

## 10. What this doc does NOT do

Per the discipline of naming-the-bounds clearly:

- **Does not lock the final cipher-width.** Options A/B/C from the parked canonical-elements thread are framework-ready (§ 6.2 names the criteria); the specific outcome resolves at the catalogue-mapping experiment's findings.
- **Does not lock Foundation layer placement (L1 vs L2).** Flag B is explicit-deferred; the L1/L2 architectural decision resolves jointly with cipher-width.
- **Does not lock the D1 rubric reconsideration's scope.** Flag A test must run before scope clarifies.
- **Does not lock the per-season vocabulary coupling policy (α/β/γ).** Catalogue-mapping experiment informs.
- **Does not commit to a specific cadence (I/II/III).** Recommendation is Option II; Matt's call.
- **Does not author any dispatches.** Each cross-seam cascade in § 9 produces dispatch-shape but the actual dispatch authoring is knight-rider's territory post-strategic-axis-lock.
- **Does not override any locked design positions.** Position C (doc 37 § 4); Position (ii) (doc 37 § 6.2); Style register HD-2D-pixel (`style-register.md`); Court framing (`court-of-forms.md`); Naming triad universal frame (`naming-triad.md`); embodiment taxonomy (`embodiment-narrative-layer.md`); three-layer model (`engine-generic-meta-structure.md`) — all remain operative and this doc explicitly honors them.
- **Does not address post-Phase-0 form-bias work.** The Earth meta-layer Court / Spirit Guide / form-library deepening into isekai canon is named in § 5.1 as the post-Phase-0 split but not designed here; it follows when post-Phase-0 implementation begins.
- **Does not measure the engine's current convergence shape per-variable.** Per the terminology lock, *skew* is off-limits without per-variable evidence; this doc's Q2 names patterns + provides resolution levers; it does not attribute observed convergence to specific variables.
- **Does not pre-empt the catalogue experiment's findings.** The experiment runs; the findings land; the four sub-locks resolve; this doc's framework absorbs the outcomes.

---

## 11. Open questions surfaced by this strategy (not blocking)

These are tracked here for transparency; they do not block the strategic-axis lock.

### Q11.1 — Pitch-2026-05-18 message integration

The 2026-05-18 pitch references engine licensability (per `engine-generic-meta-structure.md` § "What this enables for the pitch"). This strategy doc strengthens the pitch's "what specifically are you licensing?" answer (L1 substrate is form-agnostic; L2 cosmology + form-bias-locked design lives in Reincarnated). Open: should the pitch's talking points incorporate the explicit-hybrid framing as a positioning detail (*"Reincarnated lands ARPG-mechanic-canonical and isekai-narrative-canonical simultaneously; the engine substrate makes this possible"*) — or is this too detailed for pitch register? My instinct: keep pitch high-level; the explicit-hybrid framing is internal-discipline-clarity, not pitch surface.

### Q11.2 — Post-Phase-0 form-bias deepening

The strategic-axis lock notes that post-Phase-0 deepens into isekai canon (Court / form-library). Open: when post-Phase-0 implementation work begins, do additional sub-locks lift the strategic-axis to "isekai-canon-primary across both layers" — OR does the explicit-hybrid persist with the Phase-0 / post-Phase-0 split? Likely a future-design-conversation question; not blocking. Surfaces when Earth meta-layer implementation begins.

### Q11.3 — Demo2's specific form-bias requirements

Per the roadmap-stewardship dispatch's in-session message, Matt asked about a "Demo Vertical Slice 2" milestone with "elements + isekai form-bias" content. Open: does demo2 need Stage 1 + Stage 2 + Stage 3 form-bias work complete before it ships, or can it ship with Stage 1 only (embodiment-axis emit) and accept canonical-four-in-prompt as a transitional state? Likely Stage 1 minimum + Stage 4 display work; gamora / drax sequencing determines. Demo2 dispatch will need to be scoped against this question; not blocking this strategy doc.

### Q11.4 — The post-cipher-migration B-series engine work

Stage 3's cipher migration creates a calibration-epoch boundary (per the engine-balance-stewardship decisions-log entry's pattern); existing converged seasons (1001-1005) are calibrated against canonical-four-in-prompt + canonical-four-internal. Post-Stage-3, the convergence framework's calibration may shift. Open: is this a re-converge-all-seasons cost or a calibration-epoch-handoff? Likely the latter (handle as semantic shift per Discipline #12); not blocking.

### Q11.5 — The seasonal anchor library's L2-vs-L3 placement

Per `engine-generic-meta-structure.md`, the anchor library *system* is L1 engine substrate; the anchor library *contents* (130 entries currently in Reincarnated's library) are L2 Reincarnated-cosmology. Open: under the cipher migration, do the anchor library contents need a humanoid-fantasy screening pass to surface latent humanoid-cosmology bias? Likely yes; this is a future content-curation pass, not blocking this strategy.

---

## 12. Cross-references

- **Predecessor work:**
  - `canonical/story/pre-llm-substrate-inventory.md` — substrate this doc reasons against
  - `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md` — item-by-item code citations
  - `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` — Day-4 re-engagement
  - `canonical/37-form-bias-diagnosis-and-recovery.md` — the diagnosis this strategy operationalizes
- **Design-lock companions:**
  - `canonical/story/embodiment-narrative-layer.md` — Position C operationalized
  - `canonical/story/naming-triad.md` — encounter-moment per-season variant pattern
  - `canonical/story/style-register.md` — HD-2D-pixel locked register
  - `canonical/story/court-of-forms.md` — Court framing + dual-label pattern
  - `canonical/story/cosmology-reincarnated.md` — Reincarnated cosmology this strategy serves
  - `canonical/story/engine-generic-meta-structure.md` — L1/L2/L3 three-layer model
- **Empirical research base:**
  - `agentic_orchestration/research/knowledge/isekai/2026-05-16-isekai-evolution.md` — Pass 1; non-humanoid-reincarnation sub-genre + identity-continuity
  - `agentic_orchestration/research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md` — Pass 2; D1-Immortal arc + gear schema lineage
  - `agentic_orchestration/research/knowledge/poe/2026-05-16-poe-design-philosophy.md` — Pass 3; cipher / element / endgame velocity
  - `agentic_orchestration/research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md` — Pass 4; class-fantasy / build-diversity / community-design discourse
  - `agentic_orchestration/research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md` — Pass 5; Last Epoch / Grim Dawn / Lost Ark / Torchlight
  - `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — catalogue landscape
- **Engineering substrate references:**
  - `canonical/29-design-overview.md` — strategic anchor + two-engine architecture
  - `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` — progression locks this strategy honors
  - `reincarnated-engine/design/decisions/decisions-log.md` — recent locks (engine-balance-stewardship; calibration-epoch; research.db retirement)
  - `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #12 (existing) + #13a/#13b/#14 (candidates from this strategy)
- **Empirical experiments:**
  - `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` — Experiment 1; runs at Stage 3 gate
  - `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md` — Experiment 2; resolves four deferred sub-locks
- **Stewardship surface:**
  - `canonical/16-project-roadmap.md` — Substrate Realignment Workstream section consumes this strategy
  - `canonical/story/drift-audit.md` — Discipline #13 enforcement context
  - `canonical/story/engine-balance-stewardship.md` — companion stewardship doc on parallel gate cluster

---

## 13. Maintenance protocol

This doc holds **open** until:
- (a) Matt approves the strategic-axis lock + cadence choice, AND
- (b) knight-rider drafts the decisions-log entries per § 8, AND
- (c) the first cross-seam form-bias dispatch (per § 9) ships.

While open:
- Any form-bias-related decision (new dispatch authoring; cluster B sub-cluster treatment choice; embodiment-taxonomy amendment; cipher-migration sub-decision) references this doc's strategic-axis lock + the cluster framing
- Drift instances surfaced by knight-rider (per the stewardship-transition dispatch) feed into this doc + the drift-audit; if a drift instance reveals strategy-doc-incompleteness, the doc gets amended; the architecture is appended-to, not rewritten

After landing:
- Decisions-log entries become the primary lock for downstream gate references
- This doc becomes the design-intent expansion of those entries
- Future form-bias work that reaches beyond this doc's framing (e.g., post-Phase-0 deepening; future cluster discovered as the engine evolves) lands as appended sections; preserve canonical-lock-date history

Maintenance is **structurally similar to** `cosmology-reincarnated.md`'s maintenance: append, don't rewrite; preserve history; surface new pillars + drift instances as they appear.

---

## 14. The hat stays on

The form-bias work is large but structured. The strategic-axis is hybrid because the project's positioning is hybrid; the resolution levers are per-cluster because the cluster shape was empirical; the deferred sub-locks resolve at named gates because the catalogue work earns its decisions. The discipline this strategy honors is the same discipline the project is named for: walk the seasonal journey deliberately; ascend the form you chose to live with; let the Court accumulate; do not pretend more is known than is.

This doc commits Phase-0 to a recognizable game on both sides of the genre-pair the pitch positions for. An ARPG-fluent player encounters familiar substrate. An isekai-fluent player encounters honored reincarnation. Both audiences are served at the moments their genre-promises arrive; neither is displaced.

That is what the strategic-axis lock is for.

— gandalf, 2026-05-16 (Day 4)
